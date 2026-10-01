"""Red-first: status writes across coordination-surface states.

Mission coord-artifact-single-home-01M3V4BE, WP07, T037. Pins the
user-observable contract through pre-existing entry points BEFORE any fix
(charter ATDD-First, C-005, ADR 2026-07-17-1):

* The remote-only and deleted-branch refusals are driven through the full
  ``spec-kitty agent tasks move-task`` CLI (the real move-task entry point).
* The materialize/seed/second-call/forked scenarios are driven through
  ``emit_status_transition_transactional`` -- the SAME transactional shell
  ``move-task`` itself calls for the lane-hop write (``status_transition.py``,
  contracts/emit-pipeline.md Sec.2) -- rather than through the full CLI.
  move-task's own pre-write precondition (``_mt_current_event_lane``, via the
  documented-sanctioned read-side residual ``_read_contract_from_transaction_
  target``) reads a WP's "current lane" via ``git show <coordination_branch>:
  ...`` whenever the branch exists locally but its worktree is not yet
  materialized -- a genuinely pre-fix (never-seeded) coordination branch has
  no committed Mission dir there at all, so that READ-side precondition
  always draws a blank for such a mission regardless of this WP's write-side
  fix (pre-existing, unrelated to coord_seed/write_dir; out of scope here).
  Driving these scenarios one layer below the CLI's own orchestration still
  exercises the real ``BookkeepingTransaction`` / ``establish_coord_write_
  location`` write path end-to-end against real git state.

Fixtures come from the shared WP02 harness (``tests._factories.coord_mission``).
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest
import ulid as _ulid_mod
from typer.testing import CliRunner

from kernel.clock import now_utc_iso
from mission_runtime import MissionTopology
from specify_cli.cli.commands.agent.tasks import app
from specify_cli.coordination.status_transition import emit_status_transition_transactional
from specify_cli.lanes.models import ExecutionLane, LanesManifest
from specify_cli.lanes.persistence import write_lanes_json
from specify_cli.status.models import Lane, StatusEvent, TransitionRequest
from specify_cli.status.store import append_event
from tests._factories.coord_mission import (
    CoordMission,
    event_ids,
    make_fork_fixture,
    make_prefix_coord_mission,
)

pytestmark = [pytest.mark.integration, pytest.mark.git_repo]

runner = CliRunner()

_STATUS_LOG = "status.events.jsonl"
_COORD_TOPOLOGIES = (MissionTopology.COORD, MissionTopology.LANES_WITH_COORD)


def _claim_request(coord: CoordMission) -> TransitionRequest:
    return TransitionRequest(
        feature_dir=coord.root_mission_dir,
        mission_slug=coord.mission_dir_name,
        wp_id="WP01",
        to_lane=Lane.CLAIMED,
        actor="testbot",
        reason="WP07 T037 red-first probe",
        execution_mode="worktree",
        repo_root=coord.repo_root,
        # The transition pipeline derives ``from_lane`` through the SAME
        # read-side residual the module docstring names
        # (``_read_contract_from_transaction_target``): for a pre-fix
        # EMPTY/UNMATERIALIZED-with-a-local-branch mission that read reads
        # ``git show <coordination_branch>:...`` and finds nothing (the
        # Mission dir was never committed there pre-seed), so it reports
        # "genesis" regardless of the WP's real root-checkout state --
        # "genesis -> claimed" is otherwise illegal. ``force`` bypasses the
        # legality check the same way ``tests/utils.py::_seed_canonical_wp_
        # state`` does for the identical pre-existing situation; it does not
        # touch anything this WP's write-location fix governs.
        force=True,
    )


def _in_progress_request(coord: CoordMission) -> TransitionRequest:
    return TransitionRequest(
        feature_dir=coord.root_mission_dir,
        mission_slug=coord.mission_dir_name,
        wp_id="WP01",
        to_lane=Lane.IN_PROGRESS,
        actor="testbot",
        reason="WP07 T037 red-first probe (second call)",
        execution_mode="worktree",
        repo_root=coord.repo_root,
    )


def _repo_root_coord_dir_porcelain(coord: CoordMission) -> str:
    relpath = f"kitty-specs/{coord.mission_dir_name}"
    return subprocess.run(
        ["git", "-C", str(coord.repo_root), "status", "--porcelain", "--", relpath],
        capture_output=True,
        text=True,
        check=True,
    ).stdout


# ---------------------------------------------------------------------------
# UNMATERIALIZED + local branch: the worktree is materialized first, and the
# event lands there -- never on the repository root checkout (US2.3).
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("topology", _COORD_TOPOLOGIES)
def test_transactional_emit_unmaterialized_local_branch_materializes_and_writes_coord(
    tmp_path: Path, topology: MissionTopology
) -> None:
    """``make_prefix_coord_mission(worktree="absent")`` is UNMATERIALIZED with a
    never-seeded (pre-fix) coordination branch: once the worktree is
    materialized, the Mission dir is still absent from the branch (EMPTY), so
    the seed carries the root records over exactly as the pre-fix EMPTY
    scenario does -- this test's distinguishing assertion is the
    materialization itself (US2.3), not an absence of carried content.
    """
    coord = make_prefix_coord_mission(tmp_path, topology, worktree="absent")
    before_coord_worktree_exists = coord.coord_worktree_path.exists()
    root_status_before = _repo_root_coord_dir_porcelain(coord)

    event = emit_status_transition_transactional(_claim_request(coord))

    assert str(event.to_lane) == str(Lane.CLAIMED)
    assert coord.coord_worktree_path.exists()
    assert not before_coord_worktree_exists
    coord_log = coord.coord_mission_dir / _STATUS_LOG
    assert coord_log.exists()
    assert event.event_id in coord_log.read_text(encoding="utf-8")
    # The root copy is restored (clean): no new untracked/modified COORD
    # residue beyond whatever pre-existing fixture state the baseline carries.
    assert _repo_root_coord_dir_porcelain(coord) == root_status_before


# ---------------------------------------------------------------------------
# Pre-fix EMPTY: root records are carried over ONCE (the seed), the new event
# is appended after them, and the logical clock continues (US2.4/US2.5).
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("topology", _COORD_TOPOLOGIES)
def test_transactional_emit_prefix_empty_seeds_then_writes_coord(tmp_path: Path, topology: MissionTopology) -> None:
    coord = make_prefix_coord_mission(tmp_path, topology, worktree="empty")
    root_ids_before = event_ids(coord.root_mission_dir / _STATUS_LOG)
    assert root_ids_before
    root_status_before = _repo_root_coord_dir_porcelain(coord)

    event = emit_status_transition_transactional(_claim_request(coord))

    assert str(event.to_lane) == str(Lane.CLAIMED)
    coord_ids_after = event_ids(coord.coord_mission_dir / _STATUS_LOG)
    # coord log = carried root events + the new event.
    assert set(root_ids_before) <= set(coord_ids_after)
    assert event.event_id in coord_ids_after
    assert len(coord_ids_after) == len(root_ids_before) + 1
    assert len(coord_ids_after) == len(set(coord_ids_after))  # no duplicate event ids
    # The coordination branch carries exactly one seed commit.
    trailer = subprocess.run(
        [
            "git",
            "-C",
            str(coord.repo_root),
            "log",
            "--format=%(trailers:key=Spec-Kitty-Coordination-Seed,valueonly)",
            coord.coordination_branch,
        ],
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    seed_lines = [line for line in trailer.splitlines() if line.strip()]
    assert len(seed_lines) == 1, trailer
    # The root copy is restored (clean): no new untracked/modified COORD
    # residue beyond whatever pre-existing fixture state the baseline carries.
    assert _repo_root_coord_dir_porcelain(coord) == root_status_before


def test_transactional_emit_second_call_after_seed_carries_nothing_new(tmp_path: Path) -> None:
    coord = make_prefix_coord_mission(tmp_path, MissionTopology.COORD, worktree="empty")
    root_status_before = _repo_root_coord_dir_porcelain(coord)

    first = emit_status_transition_transactional(_claim_request(coord))
    assert str(first.to_lane) == str(Lane.CLAIMED)
    ids_after_first = event_ids(coord.coord_mission_dir / _STATUS_LOG)

    second = emit_status_transition_transactional(_in_progress_request(coord))
    assert str(second.to_lane) == str(Lane.IN_PROGRESS)
    ids_after_second = event_ids(coord.coord_mission_dir / _STATUS_LOG)

    assert set(ids_after_first) <= set(ids_after_second)
    assert len(ids_after_second) == len(set(ids_after_second))  # no duplicate event ids
    assert len(ids_after_second) == len(ids_after_first) + 1
    assert _repo_root_coord_dir_porcelain(coord) == root_status_before


# ---------------------------------------------------------------------------
# Remote-only branch: refused before anything is written (#4970 parity).
# Driven through the full move-task CLI (the real entry point) -- this
# scenario's branch does not exist LOCALLY, so move-task's own read-side
# precondition degrades to the primary checkout (unaffected by the read-side
# residual noted in the module docstring) and this WP's write-side refusal is
# reached cleanly.
# ---------------------------------------------------------------------------


def _write_wp01_task_file(coord: CoordMission) -> None:
    tasks_dir = coord.root_mission_dir / "tasks"
    tasks_dir.mkdir(parents=True, exist_ok=True)
    (tasks_dir / "WP01-fixture.md").write_text(
        "---\n"
        "work_package_id: WP01\n"
        "title: Fixture WP01\n"
        "execution_mode: code_change\n"
        "agent: testbot\n"
        "subtasks: []\n"
        "---\n\n# WP01\n\n## Activity Log\n",
        encoding="utf-8",
    )
    write_lanes_json(
        coord.root_mission_dir,
        LanesManifest(
            version=1,
            mission_slug=coord.mission_dir_name,
            mission_id=None,
            mission_branch=f"kitty/mission-{coord.mission_dir_name}",
            target_branch=coord.target_branch,
            lanes=[
                ExecutionLane(
                    lane_id="lane-a",
                    wp_ids=("WP01",),
                    write_scope=("src/wp01/**",),
                    predicted_surfaces=(),
                    depends_on_lanes=(),
                    parallel_group=0,
                )
            ],
            computed_at="2026-01-01T00:00:00+00:00",
            computed_from="dependency_graph+ownership",
            planning_commit_sha="a" * 40,
        ),
    )
    # Register WP01's canonical ``planned`` status (what ``finalize-tasks``
    # does): move-task's own ``_mt_current_event_lane`` precondition reads
    # this through ``primary_checkout`` for a mission whose coordination
    # branch does not exist LOCALLY (remote-only / deleted) -- distinct from
    # the read-side residual the module docstring names, which affects only
    # a LOCAL, never-materialized branch.
    append_event(
        coord.root_mission_dir,
        StatusEvent(
            event_id=str(_ulid_mod.ULID()),
            mission_slug=coord.mission_dir_name,
            wp_id="WP01",
            from_lane=Lane.GENESIS,
            to_lane=Lane.PLANNED,
            at=now_utc_iso(),
            actor="fixture",
            force=False,
            execution_mode="worktree",
        ),
    )
    subprocess.run(
        ["git", "-C", str(coord.repo_root), "add", "kitty-specs"],
        check=True,
        capture_output=True,
    )
    subprocess.run(
        ["git", "-C", str(coord.repo_root), "commit", "-q", "-m", "add WP01"],
        check=True,
        capture_output=True,
    )


def _move_task_claimed(
    coord: CoordMission, monkeypatch: pytest.MonkeyPatch
) -> tuple[int, str, dict[str, object] | None]:
    monkeypatch.chdir(coord.repo_root)
    result = runner.invoke(
        app,
        [
            "move-task",
            "WP01",
            "--to",
            "claimed",
            "--mission",
            coord.mission_dir_name,
            "--agent",
            "testbot",
            "--force",
            "--json",
        ],
        catch_exceptions=False,
    )
    stdout = result.stdout or ""
    payload: dict[str, object] | None = None
    if stdout.strip().startswith("{"):
        try:
            payload = json.loads(stdout)
        except json.JSONDecodeError:
            payload = None
    return result.exit_code, stdout, payload


def test_move_task_remote_only_branch_refuses_before_any_write(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    coord = make_prefix_coord_mission(tmp_path, MissionTopology.COORD, remote_only=True)
    _write_wp01_task_file(coord)
    root_status_before = _repo_root_coord_dir_porcelain(coord)

    exit_code, stdout, payload = _move_task_claimed(coord, monkeypatch)

    assert exit_code != 0
    assert "is unmaterialized" in stdout
    assert _repo_root_coord_dir_porcelain(coord) == root_status_before
    assert not coord.coord_worktree_path.exists()


# ---------------------------------------------------------------------------
# DELETED branch: refused loudly with a recovery hint (US2.8).
# ---------------------------------------------------------------------------


def test_move_task_deleted_branch_refuses_with_recovery_hint(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    coord = make_prefix_coord_mission(tmp_path, MissionTopology.COORD, branch_deleted=True)
    _write_wp01_task_file(coord)
    root_status_before = _repo_root_coord_dir_porcelain(coord)

    exit_code, stdout, payload = _move_task_claimed(coord, monkeypatch)

    assert exit_code != 0
    assert "declared in meta.json but deleted from git" in stdout
    assert _repo_root_coord_dir_porcelain(coord) == root_status_before


# ---------------------------------------------------------------------------
# MATERIALIZED-forked (#5519 shape, fork builder (a)): the write succeeds and
# the event lands on the coordination log -- no COORD_SEED_FORK_REFUSED
# lockout (the seed only runs on EMPTY).
# ---------------------------------------------------------------------------


def test_transactional_emit_materialized_forked_mission_is_not_locked_out(tmp_path: Path) -> None:
    fixture = make_fork_fixture(tmp_path, "both_committed", MissionTopology.COORD)
    coord_ids_before = event_ids(fixture.coord_mission_dir / _STATUS_LOG)

    event = emit_status_transition_transactional(_claim_request(fixture))

    assert str(event.to_lane) == str(Lane.CLAIMED)
    coord_ids_after = event_ids(fixture.coord_mission_dir / _STATUS_LOG)
    assert set(coord_ids_before) <= set(coord_ids_after)
    assert event.event_id in coord_ids_after
    assert len(coord_ids_after) == len(coord_ids_before) + 1
