"""The commit router never reports a coordination-dirty status log as ``unchanged``.

Adopted via ``git cherry-pick -x 251bea520f`` (``upstream/test/p0-repro-5513``,
PR #5520). R2 was intentionally red-first against the pre-WP05 router; WP05
(coord-artifact-single-home-01M3V4BE T026) tightens R2's refusal branch to
require a NAMED reason in ``surfaces[*].refused`` and adds R2b, the positive
control proving a genuinely clean coordination copy still reports
``unchanged`` (never over-corrected into always committing).

Invariant: for a coordination-topology mission, a status-kind file
(``STATUS_STATE``: ``status.events.jsonl`` / ``status.json``) whose change exists
only in the coordination worktree (``.worktrees/<slug>-coord/``) and that is routed
through :func:`~specify_cli.coordination.commit_router.commit_for_mission` is
committed on the coordination surface. It is never reported as ``unchanged``
while the coordination copy is still dirty (#5513).

The historical defect: the caller named the status log by its primary-checkout
path (``kitty-specs/<slug>/status.events.jsonl``). The coordination staging
helper (``_stage_artifacts_in_coord_worktree``) skipped every ``STATUS_STATE``
file that was not already inside the coordination worktree, so ``commit_paths``
came back empty. The wrong-surface guard (``_classify_no_commit_paths``) then
inspected only the primary checkout, found it clean, and returned ``unchanged``
/ ``no_op_already_committed``. Nothing was committed, no error surfaced, and
the caller believed the log landed. WP05 T027 fixes this by translating a
root-path STATUS_STATE/DECISION_LOG input to its owning (coordination) copy
instead of skipping it.

Real git fixtures only: a real coord-topology mission
(:func:`tests.terminus.conftest.build_coord_mission`) with its materialised
coordination worktree; no mocks.
"""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

from mission_runtime import MissionArtifactKind
from specify_cli.coordination.commit_outcome import (
    COORDINATION_BRANCH_DELETED,
    PATH_UNROUTABLE,
    PROTECTED_BRANCH_REFUSED,
    STATUS_LOCK_HELD,
)
from specify_cli.git.protection_policy import ProtectionPolicy

if TYPE_CHECKING:
    from specify_cli.coordination.commit_router import CommitRouterResult
    from tests.terminus.conftest import CoordMission

pytestmark = [pytest.mark.git_repo]

_STATUS_EVENTS = "status.events.jsonl"
_COORD_ONLY_ROW = '{"simulated": "row appended only in the coordination worktree (#5513)"}\n'
#: T026 step 3: an outcome other than ``committed`` on the standard fixture
#: passes only if backed by one of these NAMED reasons (never a bare status).
_NAMED_REFUSAL_REASONS = frozenset({PROTECTED_BRANCH_REFUSED, STATUS_LOCK_HELD, COORDINATION_BRANCH_DELETED, PATH_UNROUTABLE})


def _git(cwd: Path, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True, text=True).stdout.strip()


def _porcelain(cwd: Path, rel: Path) -> str:
    return _git(cwd, "status", "--porcelain", "--untracked-files=all", "--", rel.as_posix())


def _build_coord_mission_with_baseline_status_log(tmp_path: Path) -> tuple[CoordMission, Path, Path, Path]:
    """A real coord mission whose status log is committed and CLEAN on both surfaces.

    Returns ``(mission, primary_log, coord_log, coord_worktree)``.
    """
    from specify_cli.coordination.surface_resolver import resolve_status_surface
    from specify_cli.coordination.workspace import CoordinationWorkspace
    from tests.terminus.conftest import build_coord_mission

    mission = build_coord_mission(tmp_path, target_branch="feature/router-5513")
    coord = CoordinationWorkspace.worktree_path(mission.repo, mission.slug, mission.mid8)
    coord_log = resolve_status_surface(mission.repo, mission.slug)
    primary_log = mission.feature_dir / _STATUS_EVENTS
    assert coord_log.is_relative_to(coord), f"fixture must put the canonical status log in the coord worktree: {coord_log}"
    assert primary_log.is_file(), f"fixture must carry a committed primary copy of the status log: {primary_log}"

    coord_rel = coord_log.relative_to(coord)
    _git(coord, "add", "--", coord_rel.as_posix())
    subprocess.run(["git", "commit", "-q", "-m", "baseline"], cwd=coord, check=False, capture_output=True)
    assert _porcelain(coord, coord_rel) == "", "precondition: coord status log starts committed"
    return mission, primary_log, coord_log, coord


def _coord_mission_with_coord_only_dirty_log(tmp_path: Path) -> tuple[CoordMission, Path, Path, Path]:
    """A real coord mission whose status log is dirty ONLY in the coordination worktree.

    Returns ``(mission, primary_log, coord_log, coord_worktree)``. Both copies of the
    log start committed and clean; then one row is appended to the coordination copy
    only, so the primary checkout stays clean.
    """
    mission, primary_log, coord_log, coord = _build_coord_mission_with_baseline_status_log(tmp_path)
    coord_rel = coord_log.relative_to(coord)

    with coord_log.open("a", encoding="utf-8") as fh:
        fh.write(_COORD_ONLY_ROW)

    assert _porcelain(coord, coord_rel) != "", "precondition: coord status log is dirty"
    primary_rel = primary_log.relative_to(mission.repo)
    assert _porcelain(mission.repo, primary_rel) == "", "precondition: primary status log is clean (dirty ONLY on coord)"
    return mission, primary_log, coord_log, coord


def _route_status_log(mission: CoordMission, primary_log: Path) -> CommitRouterResult:
    from specify_cli.coordination.commit_router import commit_for_mission

    return commit_for_mission(
        mission.repo,
        mission.slug,
        (primary_log,),
        "chore(status): commit the mission status log (#5513 reproduction)",
        ProtectionPolicy.resolve(mission.repo),
        kind=MissionArtifactKind.STATUS_STATE,
    )


def test_router_never_reports_a_coord_only_dirty_status_log_as_unchanged(tmp_path: Path) -> None:
    """R2 (#5513): a status log dirty only in the coord worktree is committed there, never ``unchanged``.

    Tightened (WP05 T026, post-tasks squad R-M8/FR-016 R2 adoption): on this
    STANDARD fixture (healthy coordination worktree, no lock contention), the
    router must commit outright -- there is no legitimate reason to refuse
    here. A result other than ``committed`` would need a NAMED reason in
    ``surfaces[*].refused`` (never a bare status label) to be defensible at
    all; this fixture has none of those conditions, so anything but
    ``committed`` is a defect.
    """
    mission, primary_log, coord_log, coord = _coord_mission_with_coord_only_dirty_log(tmp_path)
    coord_rel = coord_log.relative_to(coord)
    coord_head_before = _git(coord, "rev-parse", "HEAD")

    result = _route_status_log(mission, primary_log)

    coord_dirty_after = _porcelain(coord, coord_rel)
    coord_head_after = _git(coord, "rev-parse", "HEAD")

    assert result.status != "unchanged", (
        f"commit_for_mission reported status={result.status!r} reason={result.reason!r} "
        f"placement_ref={result.placement_ref!r} for a status log that is dirty in the "
        f"coordination worktree ({coord_rel.as_posix()}: {coord_dirty_after!r}); nothing was "
        f"committed (coord HEAD unchanged: {coord_head_after == coord_head_before}) and no error "
        f"surfaced (#5513 silent skip)."
    )

    if result.status != "committed":
        named_reasons = {fate.reason for surface in result.surfaces for fate in surface.refused}
        assert named_reasons & _NAMED_REFUSAL_REASONS, (
            f"a non-committed result must carry a NAMED refusal reason in surfaces[*].refused "
            f"(one of {sorted(_NAMED_REFUSAL_REASONS)}); got status={result.status!r} "
            f"surfaces={result.surfaces!r}"
        )
        pytest.fail(
            f"the standard fixture (healthy worktree, no contention) must commit outright; "
            f"got status={result.status!r} with named reasons {named_reasons & _NAMED_REFUSAL_REASONS!r} "
            f"-- investigate why this healthy fixture hit a refusal path at all."
        )

    assert coord_head_after != coord_head_before, "a 'committed' result must advance the coordination branch"
    assert coord_dirty_after == "", f"a 'committed' result must leave the coord status log clean: {coord_dirty_after!r}"
    committed = _git(coord, "show", f"HEAD:{coord_rel.as_posix()}")
    assert committed.endswith(_COORD_ONLY_ROW.rstrip("\n")), "the coord-only row must be in the committed log"


def test_clean_coordination_copy_reports_unchanged(tmp_path: Path) -> None:
    """R2b (positive control): a genuinely CLEAN coordination copy still reports ``unchanged``.

    Proves R2's tightened assertion did not over-correct into "always commit" --
    a status log that is clean on BOTH surfaces is a genuine no-op.
    """
    mission, primary_log, coord_log, coord = _build_coord_mission_with_baseline_status_log(tmp_path)
    coord_rel = coord_log.relative_to(coord)
    coord_head_before = _git(coord, "rev-parse", "HEAD")

    result = _route_status_log(mission, primary_log)

    assert result.status == "unchanged", f"a clean coordination copy must report unchanged, got {result!r}"
    assert _git(coord, "rev-parse", "HEAD") == coord_head_before, "a genuine no-op must not advance the coordination branch"
    assert _porcelain(coord, coord_rel) == "", "the coordination copy must stay clean"
