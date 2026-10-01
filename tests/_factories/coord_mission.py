"""Shared coordination-routed Mission fixture harness (WP02, FR-016 / C-005).

Every red-first reproduction in Mission ``coord-artifact-single-home-01M3V4BE``
builds its preconditions from this module instead of hand-rolling git/coord
fixtures per test file. Each builder constructs its documented shape through
the **production create path** (``create_mission_core`` / the
``spec-kitty agent mission create`` CLI) or, where the production path no
longer produces a pre-fix shape, by explicit git plumbing that validates
itself against the production probe before returning.

This WP ships no reproduction: it is the harness only, and its own tests
(``tests/coordination/test_coord_mission_factory.py``) are green at the
current base.

Public API
----------
- :func:`make_coord_mission` -- production create path, both coordination
  topologies, three ``via`` variants (``core`` / ``cli_topology`` /
  ``cli_pr_bound``), optional ``materialized=True`` for a deterministic
  MATERIALIZED coordination surface.
- :func:`make_prefix_coord_mission` -- the **pre-fix shape**: a committed
  root-checkout status log, a coordination branch cut *without* the Mission
  dir, and an absent/empty coordination worktree. Several later WPs assert
  against this shape explicitly because ``create_mission_core`` will stop
  producing it once WP06 lands.
- :func:`make_fork_fixture` -- the four NFR-002 fork shapes shared by WP03,
  WP17 and WP21.
- Pure git-plumbing probes: :func:`event_ids`, :func:`lamports`,
  :func:`commits_touching`, :func:`coord_tree_has`, :func:`index_entry_ids`.

How later WPs use this (research red-first list)
-------------------------------------------------
- R1/R1b/R6/R20 (WP06) -- :func:`make_prefix_coord_mission`.
- R2 (WP05) -- :func:`make_coord_mission`.
- R3/R14/R15/R16 (WP17) -- :func:`make_fork_fixture` (shapes b/c/d).
- R4 (WP09) -- :func:`make_prefix_coord_mission` + :func:`commits_touching`.
- R22/R23/R24 (WP18) -- :func:`make_coord_mission` / :func:`event_ids`.

Caller contract: every builder clones a **fresh** git repo under the
``tmp_path`` it is given (via ``tests._support.git_template.clone_template``).
Two builder calls must never share the same ``tmp_path`` -- pass distinct
subdirectories (``tmp_path / "a"``, ``tmp_path / "b"``) when a single test
needs more than one Mission.
"""

from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Literal
from unittest.mock import patch

import ulid as _ulid_mod
from typer.testing import CliRunner

from kernel.clock import now_utc, now_utc_iso
from mission_runtime import MissionTopology
from specify_cli.cli.commands.agent.mission import app as _mission_app
from specify_cli.core.constants import KITTY_SPECS_DIR
from specify_cli.core.mission_creation import create_mission_core
from specify_cli.coordination.workspace import CoordinationWorkspace
from specify_cli.decisions import store as decision_store
from specify_cli.decisions.models import DecisionStatus, IndexEntry, OriginFlow
from specify_cli.decisions.service import open_decision
from specify_cli.missions._read_path_resolver import CoordState, probe_coord_state
from specify_cli.status.models import Lane, StatusEvent
from specify_cli.status.store import append_event
from tests._factories import provision_test_charter
from tests._support.git_template import clone_template

# Explicitly re-annotated: ``specify_cli.*`` is configured ``follow_imports =
# "skip"`` for narrow-file mypy --strict runs (pyproject.toml), which collapses
# the imported constant to ``Any``. A bare ``Path / KITTY_SPECS_DIR`` would
# therefore make every property below return ``Any`` under ``--strict``
# (``no-any-return``); this one annotated re-binding narrows it back to ``str``.
_KITTY_SPECS_DIR: str = KITTY_SPECS_DIR

__all__ = [
    "COORD_TOPOLOGIES",
    "CoordMission",
    "ForkFixture",
    "coord_tree_has",
    "commits_touching",
    "event_ids",
    "index_entry_ids",
    "lamports",
    "make_coord_mission",
    "make_fork_fixture",
    "make_prefix_coord_mission",
]

#: Both coordination topologies, for ``pytest.mark.parametrize``.
COORD_TOPOLOGIES: tuple[MissionTopology, ...] = (
    MissionTopology.COORD,
    MissionTopology.LANES_WITH_COORD,
)

_TOPIC_BRANCH = "topic"
_PRIMARY_BRANCH = "main"
_PrefixWorktree = Literal["absent", "empty"]
_ForkShape = Literal[
    "root_uncommitted_coord_untracked",
    "both_committed",
    "fresh_clone",
    "ledger_only_on_coordination",
]
#: A probe source is either a file on disk, or ``(repo, ref, relpath)`` read
#: via ``git show`` (used for refs that have no checked-out worktree, e.g. a
#: ``fresh_clone`` fork fixture).
ProbeSource = Path | tuple[Path, str, str]


# ---------------------------------------------------------------------------
# Value objects
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class CoordMission:
    """A coordination-routed Mission built through the production create path."""

    repo_root: Path
    mission_slug: str
    mid8: str
    mission_dir_name: str
    topology: MissionTopology
    target_branch: str
    coordination_branch: str
    coord_worktree_path: Path
    creation_base_sha: str

    @property
    def root_mission_dir(self) -> Path:
        """``<repo_root>/kitty-specs/<mission_dir_name>/``."""
        return self.repo_root / _KITTY_SPECS_DIR / self.mission_dir_name

    @property
    def coord_mission_dir(self) -> Path:
        """``<coord_worktree_path>/kitty-specs/<mission_dir_name>/``."""
        return self.coord_worktree_path / _KITTY_SPECS_DIR / self.mission_dir_name


@dataclass(frozen=True)
class ForkFixture(CoordMission):
    """A :class:`CoordMission` plus the NFR-002 fork-detection evidence."""

    decision_ids_root: tuple[str, ...] = ()
    decision_ids_coord: tuple[str, ...] = ()
    clone_root: Path | None = None


# ---------------------------------------------------------------------------
# Small git helpers
# ---------------------------------------------------------------------------


def _git(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True,
        text=True,
        check=True,
    )


def _git_rev_parse(repo: Path, rev: str) -> str:
    return _git(repo, "rev-parse", rev).stdout.strip()


def _write_protected_branches(repo: Path, branches: tuple[str, ...]) -> None:
    """Append ``protection.protected_branches: [...]`` to ``.kittify/config.yaml``.

    Mirrors the shape ``ProtectionPolicy.resolve`` reads (see
    ``tests/git/test_protection_config_honoring.py``). Appended as a
    SEPARATE top-level YAML key after ``provision_test_charter``'s
    ``mission_type_activations`` block, which keeps both blocks valid YAML
    without needing a round-trip parse/merge.
    """
    config_path = repo / ".kittify" / "config.yaml"
    existing = config_path.read_text(encoding="utf-8") if config_path.exists() else ""
    protected_lines = "".join(f"    - {branch}\n" for branch in branches)
    block = f"\nprotection:\n  protected_branches:\n{protected_lines}"
    config_path.write_text(existing + block, encoding="utf-8")


def _init_repo_with_target(tmp_path: Path, *, target_branch: str, protected_primary: bool) -> Path:
    """Clone the fast git template, provision the charter, and check out *target_branch*."""
    repo = clone_template(tmp_path / "repo")
    provision_test_charter(repo)
    if protected_primary:
        _write_protected_branches(repo, (target_branch,))
    if target_branch != "main":
        _git(repo, "checkout", "-b", target_branch)
    return repo


def _set_up_bare_remote(repo: Path) -> None:
    """Push *repo*'s current ``origin`` history to a fresh bare remote and set ``origin/HEAD``.

    ``clone_template`` already configures an ``origin`` pointing at the
    process-local template cache, so this re-points ``origin`` (rather than
    adding a second remote) and sets ``origin/HEAD`` -- required for
    ``--pr-bound``'s default-topology resolution (CLAUDE.md "Create-time
    topology").
    """
    bare = repo.parent / f"{repo.name}-origin.git"
    subprocess.run(
        ["git", "init", "--bare", "-b", _PRIMARY_BRANCH, str(bare)],
        capture_output=True,
        text=True,
        check=True,
    )
    _git(repo, "remote", "set-url", "origin", str(bare))
    _git(repo, "push", "origin", _PRIMARY_BRANCH)
    _git(repo, "remote", "set-head", "origin", _PRIMARY_BRANCH)


# ---------------------------------------------------------------------------
# T008 -- production-path factory
# ---------------------------------------------------------------------------


def _require_topology_match(actual: str, expected: MissionTopology) -> None:
    if actual != expected.value:
        raise AssertionError(f"meta.json topology {actual!r} != requested {expected.value!r}")


def _coord_mission_from_meta(
    repo: Path,
    *,
    slug: str,
    meta: dict[str, object],
    topology: MissionTopology,
    creation_base_sha: str,
) -> CoordMission:
    topology_value = meta["topology"]
    if not isinstance(topology_value, str):
        raise AssertionError(f"meta.json topology is not a string: {topology_value!r}")
    _require_topology_match(topology_value, topology)

    coordination_branch = meta.get("coordination_branch")
    if not isinstance(coordination_branch, str):
        raise AssertionError("expected a coordination branch for a coord-routed topology")

    mid8 = meta["mid8"]
    mission_dir_name = meta["mission_slug"]
    target_branch = meta["target_branch"]
    if not (isinstance(mid8, str) and isinstance(mission_dir_name, str) and isinstance(target_branch, str)):
        raise AssertionError(f"unexpected meta.json field types: {meta!r}")

    worktree_path: Path = CoordinationWorkspace.worktree_path(repo, mission_dir_name, mid8)
    return CoordMission(
        repo_root=repo,
        mission_slug=slug,
        mid8=mid8,
        mission_dir_name=mission_dir_name,
        topology=topology,
        target_branch=target_branch,
        coordination_branch=coordination_branch,
        coord_worktree_path=worktree_path,
        creation_base_sha=creation_base_sha,
    )


def _make_coord_mission_via_core(tmp_path: Path, topology: MissionTopology, *, slug: str, protected_primary: bool) -> CoordMission:
    repo = _init_repo_with_target(tmp_path, target_branch=_TOPIC_BRANCH, protected_primary=protected_primary)
    creation_base_sha = _git_rev_parse(repo, _TOPIC_BRANCH)
    result = create_mission_core(
        repo,
        slug,
        topology=topology,
        target_branch=_TOPIC_BRANCH,
        allow_worktree_context=True,
    )
    meta: dict[str, object] = result.meta
    return _coord_mission_from_meta(repo, slug=slug, meta=meta, topology=topology, creation_base_sha=creation_base_sha)


def _first_json_line(output: str) -> dict[str, object]:
    for raw_line in output.splitlines():
        line = raw_line.strip()
        if not line.startswith("{"):
            continue
        try:
            payload: dict[str, object] = json.loads(line)
        except json.JSONDecodeError:
            continue
        return payload
    raise AssertionError(f"No JSON payload in CLI output: {output!r}")


def _invoke_mission_create_cli(repo: Path, args: list[str]) -> dict[str, object]:
    runner = CliRunner()
    with (
        patch("specify_cli.core.mission_creation.locate_project_root", return_value=repo),
        patch("specify_cli.core.mission_creation.is_worktree_context", return_value=False),
        patch("specify_cli.cli.commands.agent.mission.locate_project_root", return_value=repo),
    ):
        result = runner.invoke(_mission_app, ["create", *args], input="")
    if result.exit_code != 0:
        raise AssertionError(f"mission create CLI failed (exit {result.exit_code}): {result.output}")
    return _first_json_line(result.output)


def _cli_create_args(slug: str, topology: MissionTopology, *extra: str) -> list[str]:
    return [
        slug,
        "--topology",
        topology.value,
        "--branch-strategy",
        "already-confirmed",
        "--json",
        *extra,
        "--friendly-name",
        f"{slug} fixture",
        "--purpose-tldr",
        f"Fixture mission for {slug}.",
        "--purpose-context",
        f"Fixture mission for {slug}, built by the coordination test factory.",
    ]


def _coord_mission_from_cli_payload(
    repo: Path,
    payload: dict[str, object],
    *,
    slug: str,
    topology: MissionTopology,
    creation_base_sha: str,
) -> CoordMission:
    meta_file = payload["meta_file"]
    if not isinstance(meta_file, str):
        raise AssertionError(f"CLI payload missing a string 'meta_file': {payload!r}")
    meta: dict[str, object] = json.loads(Path(meta_file).read_text(encoding="utf-8"))
    return _coord_mission_from_meta(repo, slug=slug, meta=meta, topology=topology, creation_base_sha=creation_base_sha)


def _make_coord_mission_via_cli_topology(tmp_path: Path, topology: MissionTopology, *, slug: str, protected_primary: bool) -> CoordMission:
    repo = _init_repo_with_target(tmp_path, target_branch=_TOPIC_BRANCH, protected_primary=protected_primary)
    creation_base_sha = _git_rev_parse(repo, _TOPIC_BRANCH)
    payload = _invoke_mission_create_cli(repo, _cli_create_args(slug, topology, "--target-branch", _TOPIC_BRANCH))
    return _coord_mission_from_cli_payload(repo, payload, slug=slug, topology=topology, creation_base_sha=creation_base_sha)


def _make_coord_mission_via_cli_pr_bound(tmp_path: Path, topology: MissionTopology, *, slug: str, protected_primary: bool) -> CoordMission:
    repo = _init_repo_with_target(tmp_path, target_branch=_PRIMARY_BRANCH, protected_primary=protected_primary)
    _set_up_bare_remote(repo)
    creation_base_sha = _git_rev_parse(repo, _PRIMARY_BRANCH)
    payload = _invoke_mission_create_cli(
        repo,
        _cli_create_args(slug, topology, "--pr-bound", "--start-branch", _TOPIC_BRANCH),
    )
    return _coord_mission_from_cli_payload(repo, payload, slug=slug, topology=topology, creation_base_sha=creation_base_sha)


def _materialize_coord_surface(coord: CoordMission) -> CoordMission:
    """Force a real, production-probe-verified MATERIALIZED coordination surface.

    Uses an actual ``git worktree add`` (never a bare ``mkdir``, which the
    production probe would still read as EMPTY -- see R-M4 / "Shape caveat
    round 5, X2" in the WP). The seeded commit carries no
    ``Spec-Kitty-Coordination-Seed`` trailer: this is a **pre-fix-shaped**
    MATERIALIZED surface, not a post-fix seed (WP03 owns that trailer).
    """
    worktree_path: Path = CoordinationWorkspace.resolve(coord.repo_root, coord.mission_dir_name, coord.mid8)
    coord_dir = coord.coord_mission_dir
    if not coord_dir.exists():
        coord_dir.mkdir(parents=True, exist_ok=True)
        root_events = coord.root_mission_dir / "status.events.jsonl"
        coord_events = coord_dir / "status.events.jsonl"
        coord_events.write_text(
            root_events.read_text(encoding="utf-8") if root_events.exists() else "",
            encoding="utf-8",
        )
        _git(worktree_path, "add", _KITTY_SPECS_DIR)
        _git(worktree_path, "commit", "-m", f"chore({coord.mission_dir_name}): fixture seed")

    state = probe_coord_state(
        coord.repo_root,
        coord.mission_dir_name,
        coord.mid8,
        coordination_branch=coord.coordination_branch,
    )
    if state is not CoordState.MATERIALIZED:
        raise AssertionError(f"materialized=True failed to reach MATERIALIZED (got {state})")
    return coord


def make_coord_mission(
    tmp_path: Path,
    topology: MissionTopology,
    *,
    via: Literal["core", "cli_topology", "cli_pr_bound"] = "core",
    slug: str = "demo",
    protected_primary: bool = False,
    materialized: bool = False,
) -> CoordMission:
    """Create a coordination-routed Mission through the production create path.

    ``via``:
      - ``"core"`` (default): ``create_mission_core`` on a fresh ``topic`` branch.
      - ``"cli_topology"``: ``spec-kitty agent mission create --topology <t>``
        on a fresh ``topic`` branch.
      - ``"cli_pr_bound"``: ``spec-kitty agent mission create --pr-bound
        --start-branch topic`` from ``main``, with a bare ``origin`` and
        ``origin/HEAD`` set (required for default-topology resolution).

    ``protected_primary=True`` configures the created mission's target
    branch as protected (``protection.protected_branches``), for WP06's
    US1.4 test.

    ``materialized=True`` additionally forces a real, production-probe-
    verified MATERIALIZED coordination surface (see
    :func:`_materialize_coord_surface` for the pre-fix-shape caveat).

    The returned shape otherwise carries only shape-agnostic invariants: it
    does NOT assume whether the coordination worktree is materialized by
    ``create`` itself, because that changes once WP06 lands. Tests that need
    a specific coordination topology state should assert it explicitly via
    :func:`~specify_cli.missions._read_path_resolver.probe_coord_state`, or
    use :func:`make_prefix_coord_mission` for the explicit pre-fix shape.
    """
    if via == "core":
        coord = _make_coord_mission_via_core(tmp_path, topology, slug=slug, protected_primary=protected_primary)
    elif via == "cli_topology":
        coord = _make_coord_mission_via_cli_topology(tmp_path, topology, slug=slug, protected_primary=protected_primary)
    elif via == "cli_pr_bound":
        coord = _make_coord_mission_via_cli_pr_bound(tmp_path, topology, slug=slug, protected_primary=protected_primary)
    else:  # pragma: no cover - Literal guards callers; defensive for non-mypy callers.
        raise ValueError(f"Unknown via={via!r}")
    if materialized:
        coord = _materialize_coord_surface(coord)
    return coord


# ---------------------------------------------------------------------------
# T009 -- pre-fix shape builder
# ---------------------------------------------------------------------------


def _append_extra_root_events(coord: CoordMission, count: int) -> None:
    """Append *count* uncommitted lane-transition events to the root checkout's log."""
    for _ in range(count):
        event = StatusEvent(
            event_id=str(_ulid_mod.ULID()),
            mission_slug=coord.mission_dir_name,
            wp_id="WP01",
            from_lane=Lane.PLANNED,
            to_lane=Lane.CLAIMED,
            at=now_utc_iso(),
            actor="fixture",
            force=False,
            execution_mode="direct_repo",
        )
        append_event(coord.root_mission_dir, event)


def _convert_branch_to_remote_only(coord: CoordMission) -> None:
    """Push the coordination branch to a bare remote, then delete the local head.

    #4970: the branch stays reachable only via ``refs/remotes/<remote>/...``.
    """
    remote_dir = coord.repo_root.parent / f"{coord.repo_root.name}-coord-remote.git"
    subprocess.run(
        ["git", "init", "--bare", "-b", _PRIMARY_BRANCH, str(remote_dir)],
        capture_output=True,
        text=True,
        check=True,
    )
    _git(coord.repo_root, "remote", "add", "coord-remote", str(remote_dir))
    _git(coord.repo_root, "push", "coord-remote", coord.coordination_branch)
    _git(coord.repo_root, "fetch", "coord-remote", coord.coordination_branch)
    _git(coord.repo_root, "branch", "-D", coord.coordination_branch)


def _expected_prefix_state(*, worktree: _PrefixWorktree, remote_only: bool, branch_deleted: bool) -> CoordState:
    if branch_deleted:
        return CoordState.DELETED
    if remote_only:
        return CoordState.UNMATERIALIZED
    if worktree == "empty":
        return CoordState.EMPTY
    return CoordState.UNMATERIALIZED


def _assert_prefix_shape(
    coord: CoordMission,
    *,
    worktree: _PrefixWorktree,
    remote_only: bool,
    branch_deleted: bool,
) -> None:
    expected = _expected_prefix_state(worktree=worktree, remote_only=remote_only, branch_deleted=branch_deleted)
    actual = probe_coord_state(
        coord.repo_root,
        coord.mission_dir_name,
        coord.mid8,
        coordination_branch=coord.coordination_branch,
    )
    if actual is not expected:
        raise AssertionError(
            f"make_prefix_coord_mission built {actual} but expected {expected} (worktree={worktree!r}, remote_only={remote_only}, branch_deleted={branch_deleted})"
        )
    if not branch_deleted:
        mission_dir_path = f"{_KITTY_SPECS_DIR}/{coord.mission_dir_name}"
        if coord_tree_has(coord.repo_root, coord.coordination_branch, mission_dir_path):
            raise AssertionError("coordination branch unexpectedly contains the mission dir")


def make_prefix_coord_mission(
    tmp_path: Path,
    topology: MissionTopology,
    *,
    worktree: _PrefixWorktree = "empty",
    remote_only: bool = False,
    branch_deleted: bool = False,
    extra_events: int = 0,
) -> CoordMission:
    """Build the **pre-fix shape**: Mission created before this fix.

    The root checkout's ``status.events.jsonl`` (``MissionCreated`` +
    ``SpecifyStarted``) is committed on the target branch; the coordination
    branch is cut at the commit BEFORE that scaffold commit, so it never
    contains the Mission dir. This is exactly what ``create_mission_core``
    already produces at the current base (WP06 has not landed), so this
    builder reuses :func:`make_coord_mission` for construction and only adds
    the explicit worktree/remote/deletion variants on top -- then validates
    the result against the production probe, never trusting its own
    construction silently (NFR-002 "fail loud").

    ``worktree="empty"`` (default) materializes the coordination worktree
    (its Mission dir stays absent -> ``EMPTY``). ``worktree="absent"`` never
    touches the worktree (-> ``UNMATERIALIZED``). ``remote_only=True`` and
    ``branch_deleted=True`` override the worktree variant (a deleted/
    remote-only branch cannot have a materialized worktree).
    """
    coord = _make_coord_mission_via_core(tmp_path, topology, slug="prefix", protected_primary=False)
    if extra_events:
        _append_extra_root_events(coord, extra_events)
    if remote_only:
        _convert_branch_to_remote_only(coord)
    elif branch_deleted:
        _git(coord.repo_root, "branch", "-D", coord.coordination_branch)
    elif worktree == "empty":
        CoordinationWorkspace.resolve(coord.repo_root, coord.mission_dir_name, coord.mid8)
    _assert_prefix_shape(coord, worktree=worktree, remote_only=remote_only, branch_deleted=branch_deleted)
    return coord


# ---------------------------------------------------------------------------
# T010 -- NFR-002 fork fixtures
# ---------------------------------------------------------------------------


def _to_fork_fixture(
    coord: CoordMission,
    *,
    decision_ids_root: tuple[str, ...] = (),
    decision_ids_coord: tuple[str, ...] = (),
    clone_root: Path | None = None,
) -> ForkFixture:
    return ForkFixture(
        repo_root=coord.repo_root,
        mission_slug=coord.mission_slug,
        mid8=coord.mid8,
        mission_dir_name=coord.mission_dir_name,
        topology=coord.topology,
        target_branch=coord.target_branch,
        coordination_branch=coord.coordination_branch,
        coord_worktree_path=coord.coord_worktree_path,
        creation_base_sha=coord.creation_base_sha,
        decision_ids_root=decision_ids_root,
        decision_ids_coord=decision_ids_coord,
        clone_root=clone_root,
    )


def _open_decision(repo_root: Path, mission_slug: str, *, slot_key: str, question: str, actor: str) -> str:
    response = open_decision(
        repo_root,
        mission_slug,
        origin_flow=OriginFlow.SPECIFY,
        input_key=slot_key,
        question=question,
        slot_key=slot_key,
        actor=actor,
    )
    decision_id: str = response.decision_id
    return decision_id


def _commit_root_events(coord: CoordMission, message: str) -> None:
    rel = (coord.root_mission_dir / "status.events.jsonl").relative_to(coord.repo_root)
    _git(coord.repo_root, "add", str(rel))
    _git(coord.repo_root, "commit", "-m", message)


def _commit_coord_events(coord: CoordMission, message: str) -> None:
    _git(coord.coord_worktree_path, "add", _KITTY_SPECS_DIR)
    _git(coord.coord_worktree_path, "commit", "-m", message)


def _build_diverging_decision_pair(tmp_path: Path, topology: MissionTopology, *, commit: bool) -> tuple[CoordMission, str, str]:
    """Build the (a)/(b) fork shapes: a root decision, then a diverging coord decision.

    The two decisions are opened through ``open_decision`` against the SAME
    ``repo_root`` -- the first while the coordination surface is
    UNMATERIALIZED (routes to the root checkout), the second after the
    coordination Mission dir is created on disk (routes to the coordination
    worktree). Neither event-id sequence is a prefix of the other because
    they land in two different files.
    """
    coord = make_prefix_coord_mission(tmp_path, topology, worktree="absent")
    decision_root = _open_decision(
        coord.repo_root,
        coord.mission_dir_name,
        slot_key="root-slot",
        question="Root decision?",
        actor="fixture-root",
    )
    if commit:
        _commit_root_events(coord, f"chore({coord.mission_dir_name}): fixture root decision")

    CoordinationWorkspace.resolve(coord.repo_root, coord.mission_dir_name, coord.mid8)
    coord.coord_mission_dir.mkdir(parents=True, exist_ok=True)
    decision_coord = _open_decision(
        coord.repo_root,
        coord.mission_dir_name,
        slot_key="coord-slot",
        question="Coord decision?",
        actor="fixture-coord",
    )
    if commit:
        _commit_coord_events(coord, f"chore({coord.mission_dir_name}): fixture coord decision")
    return coord, decision_root, decision_coord


def _clone_repo_with_branches(repo: Path, clone_root: Path, branches: tuple[str, ...]) -> None:
    """Clone *repo* and ensure each of *branches* exists locally, tracking ``origin/<branch>``.

    ``git clone`` already materializes a local branch for the source repo's
    checked-out HEAD branch (tracking its ``origin/<branch>``); only the
    remaining branches need an explicit local head created from their
    fetched remote-tracking ref.
    """
    subprocess.run(
        ["git", "clone", str(repo), str(clone_root)],
        capture_output=True,
        text=True,
        check=True,
    )
    existing = {line.strip().lstrip("* ") for line in _git(clone_root, "branch", "--format=%(refname:short)").stdout.splitlines() if line.strip()}
    for branch in branches:
        if branch not in existing:
            _git(clone_root, "branch", branch, f"origin/{branch}")


def _seed_ledger_only_fixture(coord: CoordMission) -> str:
    """Write the decision ledger directly onto the coordination branch (pre-fix #3928).

    Uses the production ``decisions.store`` read/write primitives, pointed
    explicitly at the coordination worktree's Mission dir -- never through
    ``placement_seam``, which (post #4966 AC-D2) routes the ledger to the
    PRIMARY partition. Built with git plumbing because the current
    production routing cannot reproduce this placement any more.
    """
    CoordinationWorkspace.resolve(coord.repo_root, coord.mission_dir_name, coord.mid8)
    coord_dir = coord.coord_mission_dir
    coord_dir.mkdir(parents=True, exist_ok=True)
    meta: dict[str, object] = json.loads((coord.root_mission_dir / "meta.json").read_text(encoding="utf-8"))
    mission_id = meta["mission_id"]
    if not isinstance(mission_id, str):
        raise AssertionError(f"meta.json missing a string mission_id: {meta!r}")

    entry = IndexEntry(
        decision_id=str(_ulid_mod.ULID()),
        origin_flow=OriginFlow.SPECIFY,
        slot_key="ledger-only-slot",
        input_key="ledger-only-key",
        question="Ledger-only fixture question?",
        status=DecisionStatus.OPEN,
        created_at=now_utc(),
        mission_id=mission_id,
        mission_slug=coord.mission_dir_name,
    )
    decision_store.append_entry(coord_dir, entry)
    decision_store.write_artifact(coord_dir, entry)
    _commit_coord_events(coord, f"chore({coord.mission_dir_name}): ledger-only fixture")
    decision_id: str = entry.decision_id
    return decision_id


def _fork_fixture_root_uncommitted(tmp_path: Path, topology: MissionTopology) -> ForkFixture:
    coord, decision_root, decision_coord = _build_diverging_decision_pair(tmp_path, topology, commit=False)
    return _to_fork_fixture(coord, decision_ids_root=(decision_root,), decision_ids_coord=(decision_coord,))


def _fork_fixture_both_committed(tmp_path: Path, topology: MissionTopology) -> ForkFixture:
    coord, decision_root, decision_coord = _build_diverging_decision_pair(tmp_path, topology, commit=True)
    return _to_fork_fixture(coord, decision_ids_root=(decision_root,), decision_ids_coord=(decision_coord,))


def _fork_fixture_fresh_clone(tmp_path: Path, topology: MissionTopology) -> ForkFixture:
    base = _fork_fixture_both_committed(tmp_path / "base", topology)
    clone_root = tmp_path / "clone"
    _clone_repo_with_branches(base.repo_root, clone_root, (base.target_branch, base.coordination_branch))
    return _to_fork_fixture(
        base,
        decision_ids_root=base.decision_ids_root,
        decision_ids_coord=base.decision_ids_coord,
        clone_root=clone_root,
    )


def _fork_fixture_ledger_only(tmp_path: Path, topology: MissionTopology) -> ForkFixture:
    coord = make_prefix_coord_mission(tmp_path, topology, worktree="absent")
    decision_id = _seed_ledger_only_fixture(coord)
    return _to_fork_fixture(coord, decision_ids_coord=(decision_id,))


def make_fork_fixture(tmp_path: Path, shape: _ForkShape, topology: MissionTopology = MissionTopology.COORD) -> ForkFixture:
    """Build one of the four NFR-002 fork shapes (SC-004: 0 entries/events lost, no id twice).

    - ``"root_uncommitted_coord_untracked"`` (the #5519 shape): a decision
      opened in the root checkout (uncommitted), then a second, diverging
      decision opened once the coordination Mission dir exists (untracked
      in the coordination worktree).
    - ``"both_committed"``: like (a), but both copies are committed on their
      respective branches.
    - ``"fresh_clone"``: a ``git clone`` of (b), with both branches fetched
      as local branches and no coordination worktree.
    - ``"ledger_only_on_coordination"``: ``decisions/index.json`` +
      ``decisions/DM-<id>.md`` committed only on the coordination branch
      (the pre-fix #3928 placement), absent from the root checkout.
    """
    if shape == "root_uncommitted_coord_untracked":
        return _fork_fixture_root_uncommitted(tmp_path, topology)
    if shape == "both_committed":
        return _fork_fixture_both_committed(tmp_path, topology)
    if shape == "fresh_clone":
        return _fork_fixture_fresh_clone(tmp_path, topology)
    if shape == "ledger_only_on_coordination":
        return _fork_fixture_ledger_only(tmp_path, topology)
    raise ValueError(f"Unknown fork fixture shape: {shape!r}")  # pragma: no cover - Literal guards callers.


# ---------------------------------------------------------------------------
# T010 -- pure probes
# ---------------------------------------------------------------------------


def _read_source(source: ProbeSource) -> str:
    """Return the text content a probe source names, or ``""`` when absent."""
    if isinstance(source, Path):
        return source.read_text(encoding="utf-8") if source.exists() else ""
    repo, ref, relpath = source
    result = subprocess.run(
        ["git", "-C", str(repo), "show", f"{ref}:{relpath}"],
        capture_output=True,
        text=True,
        check=False,
    )
    return result.stdout if result.returncode == 0 else ""


def _jsonl_rows(content: str) -> list[dict[str, object]]:
    return [json.loads(line) for line in content.splitlines() if line.strip()]


def event_ids(source: ProbeSource) -> tuple[str, ...]:
    """Return the ``event_id`` of every row in a JSONL event log."""
    return tuple(str(row["event_id"]) for row in _jsonl_rows(_read_source(source)))


def _row_lamport(row: dict[str, object]) -> int | None:
    """Extract a row's logical clock, tolerating its absence (brownfield CORRECTION).

    Status rows may carry ``lamport_clock`` (lifecycle envelope); decision
    rows may carry ``event_lamport`` under ``payload``; ``MissionCreated``
    and plain lane-transition rows carry neither.
    """
    if "lamport_clock" in row:
        value = row["lamport_clock"]
        return int(value) if isinstance(value, int) else None
    payload = row.get("payload")
    if isinstance(payload, dict) and "event_lamport" in payload:
        value = payload["event_lamport"]
        return int(value) if isinstance(value, int) else None
    return None


def lamports(source: ProbeSource) -> tuple[int | None, ...]:
    """Return each row's logical clock (``None`` where the row carries none)."""
    return tuple(_row_lamport(row) for row in _jsonl_rows(_read_source(source)))


def commits_touching(repo: Path, rev_range: str, relpath: str) -> list[str]:
    """Return the commit SHAs in *rev_range* that touched *relpath*, newest first."""
    result = subprocess.run(
        ["git", "-C", str(repo), "log", "--format=%H", rev_range, "--", relpath],
        capture_output=True,
        text=True,
        check=True,
    )
    return [line for line in result.stdout.splitlines() if line]


def coord_tree_has(repo: Path, branch: str, relpath: str) -> bool:
    """Return whether *branch*'s tree contains *relpath* (file or directory)."""
    result = subprocess.run(
        ["git", "-C", str(repo), "ls-tree", branch, "--", relpath],
        capture_output=True,
        text=True,
        check=False,
    )
    return bool(result.stdout.strip())


def index_entry_ids(source: ProbeSource) -> set[str]:
    """Return every ``decision_id`` in a ``decisions/index.json`` document."""
    content = _read_source(source)
    if not content.strip():
        return set()
    data = json.loads(content)
    return {str(entry["decision_id"]) for entry in data.get("entries", [])}
