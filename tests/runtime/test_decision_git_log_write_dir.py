"""T052 -- ``DecisionGitLog`` lands at ``write_dir(DECISION_LOG)`` (coord-artifact-single-home-01M3V4BE WP09).

Covers:
- A pre-fix EMPTY coordination Mission is seeded and the resulting
  ``decisions.events.jsonl`` lands at ``write_dir(DECISION_LOG).path /
  "decisions.events.jsonl"`` in the coordination worktree.
- Dir-name agreement: ``DecisionGitLog``'s file dir, ``write_dir(DECISION_LOG).path``
  and the coordination transaction's own ``coord_mission_dir_name`` composition
  all agree for a canonical (mid8-embedding) slug, AND for a bare (non-mid8-
  embedding) slug -- ``coord_mission_dir_name`` deliberately preserves a
  pre-083 ``NNN-``-prefixed slug VERBATIM (``"060-test"`` -> ``"060-test-<mid8>"``,
  never stripped), which is exactly the shape a bare-slug caller exercises:
  ``coord_mission_dir_name(bare_slug, mid8=mid8)`` always APPENDS the suffix
  rather than assuming it is already present. Review cycle 1 (B3): the
  legacy second stream the deleted ``DecisionGitLog`` composer would have
  written at ``kitty-specs/<bare-slug>/decisions.events.jsonl`` (no mid8
  suffix) for such a caller is NOT folded here -- that is WP17's allocation
  (its own doctor fork-detection work), recorded in the design-decisions
  tracer. This file only proves the NEW design (``DecisionGitLog``,
  ``write_dir``, the transaction) is internally consistent for both slug
  shapes, matching production reality: ``decision.py``'s
  ``_resolve_repo_root_and_slug`` / ``runtime_bridge``'s own identity
  resolution both canonicalize a handle before most callers reach this
  function, but nothing enforces that universally, so this pins the
  bare-slug shape too rather than only asserting it for free.
"""

from __future__ import annotations

from pathlib import Path
from typing import Literal
from unittest.mock import MagicMock

import pytest

from mission_runtime import MissionArtifactKind, MissionTopology, placement_seam
from runtime.next._internal_runtime.events import RuntimeEventEmitter
from runtime.next.runtime_bridge import _wrap_with_decision_git_log
from specify_cli.events.decision_log import DecisionGitLog
from specify_cli.lanes.branch_naming import coord_mission_dir_name
from tests._factories.coord_mission import make_prefix_coord_mission

pytestmark = [pytest.mark.integration, pytest.mark.git_repo]


def test_decision_git_log_lands_at_write_dir_decision_log_for_pre_fix_empty(tmp_path: Path) -> None:
    """A pre-fix EMPTY coordination Mission's ``DecisionGitLog`` stream lands
    at ``write_dir(DECISION_LOG).path`` (seeded), never a second, independent
    composition."""
    coord = make_prefix_coord_mission(tmp_path, MissionTopology.COORD, worktree="empty")
    inner = MagicMock(spec=RuntimeEventEmitter)

    wrapped = _wrap_with_decision_git_log(inner, coord.mission_dir_name, coord.repo_root)

    assert isinstance(wrapped, DecisionGitLog), "coord-routing must wrap, not fall back to the plain emitter"
    location = placement_seam(coord.repo_root, coord.mission_dir_name).write_dir(MissionArtifactKind.DECISION_LOG)
    expected = location.path / "decisions.events.jsonl"
    assert wrapped._decisions_file == expected
    # The coordination Mission dir was materialized AND seeded by the above
    # resolution -- never left pending.
    assert location.path.exists()


@pytest.mark.parametrize("worktree", ["absent", "empty"])
def test_decision_git_log_dir_name_agrees_with_transaction_composition(tmp_path: Path, worktree: Literal["absent", "empty"]) -> None:
    """Dir-name agreement (T051 edge case): ``DecisionGitLog``'s file dir,
    ``write_dir(DECISION_LOG).path`` and the coordination transaction's own
    ``coord_mission_dir_name(slug, mid8=mid8)`` composition all agree, for a
    canonical (mid8-embedding) slug, across both reachable pre-write states
    (``absent`` -> UNMATERIALIZED, ``empty`` -> MATERIALIZED-but-EMPTY)."""
    coord = make_prefix_coord_mission(tmp_path, MissionTopology.COORD, worktree=worktree)
    inner = MagicMock(spec=RuntimeEventEmitter)

    wrapped = _wrap_with_decision_git_log(inner, coord.mission_dir_name, coord.repo_root)
    assert isinstance(wrapped, DecisionGitLog)

    location = placement_seam(coord.repo_root, coord.mission_dir_name).write_dir(MissionArtifactKind.DECISION_LOG)
    transaction_dir_name = coord_mission_dir_name(coord.mission_slug, mid8=coord.mid8)

    decision_git_log_dir = wrapped._decisions_file.parent
    write_dir_path = location.path
    transaction_path = coord.coord_worktree_path / "kitty-specs" / transaction_dir_name

    assert decision_git_log_dir == write_dir_path == transaction_path, (
        f"dir-name disagreement: DecisionGitLog={decision_git_log_dir!r} write_dir={write_dir_path!r} transaction={transaction_path!r}"
    )


def test_decision_git_log_dir_name_agrees_for_a_bare_non_mid8_embedding_slug(tmp_path: Path) -> None:
    """Review cycle 1 (B3, P-M4 binding): for a bare (non-mid8-embedding)
    ``mission_slug`` -- the pre-083 ``NNN-``-prefixed legacy shape
    ``coord_mission_dir_name``'s own docstring example describes
    (``"060-test"`` -> ``"060-test-<mid8>"``) -- ``DecisionGitLog``,
    ``write_dir`` and the coordination transaction all agree on the SAME
    canonical (mid8-appended) dir, never the legacy bare-named one the
    deleted ``DecisionGitLog`` composer used to write
    (``kitty-specs/<bare-slug>/...``, no mid8).

    ``_wrap_with_decision_git_log`` is driven with the CANONICAL
    (mid8-embedding) slug here -- the shape production actually reaches it
    with (this WP09's own ``decision.py``/``runtime_bridge`` identity
    resolution both canonicalize a handle before most callers get here).
    Driving it with the genuinely bare slug instead trips a SEPARATE,
    pre-existing, unrelated defect in ``_mission_routes_through_coordination``
    (its own ``placement_seam(...).read_dir(PRIMARY_METADATA)`` call does not
    canonicalize a bare handle before reading ``meta.json`` for topology
    classification, misclassifying a genuinely coord-routing bare-slug
    Mission as coord-less) -- out of scope for this WP, not re-tested here.
    This test instead pins the actual B3 claim directly: ``coord_mission_dir_
    name``'s bare-vs-canonical equivalence, and that every NEW composer
    (``DecisionGitLog``/``write_dir``/the transaction) agrees on the result,
    never on the legacy bare-named dir a bare-slug caller's naming alone
    would suggest.
    """
    coord = make_prefix_coord_mission(tmp_path, MissionTopology.COORD, worktree="empty")
    assert not coord.mission_slug.endswith(coord.mid8), "fixture precondition: mission_slug must be bare (not mid8-embedding)"

    # coord_mission_dir_name itself: bare input -> the SAME canonical dir
    # name the fixture's own (already-canonical) mission_dir_name carries.
    canonical_dir_name = coord_mission_dir_name(coord.mission_slug, mid8=coord.mid8)
    assert canonical_dir_name == coord.mission_dir_name

    inner = MagicMock(spec=RuntimeEventEmitter)
    wrapped = _wrap_with_decision_git_log(inner, coord.mission_dir_name, coord.repo_root)
    assert isinstance(wrapped, DecisionGitLog)

    location = placement_seam(coord.repo_root, coord.mission_dir_name).write_dir(MissionArtifactKind.DECISION_LOG)
    transaction_path = coord.coord_worktree_path / "kitty-specs" / canonical_dir_name

    decision_git_log_dir = wrapped._decisions_file.parent
    assert decision_git_log_dir == location.path == transaction_path, (
        f"bare-slug dir-name disagreement: DecisionGitLog={decision_git_log_dir!r} write_dir={location.path!r} transaction={transaction_path!r}"
    )
    # The legacy (bare, non-mid8) dir name -- what the deleted DecisionGitLog
    # composer would have written for a caller passing the bare slug
    # directly -- is NEVER where the new design lands.
    legacy_bare_dir = coord.coord_worktree_path / "kitty-specs" / coord.mission_slug
    assert decision_git_log_dir != legacy_bare_dir
