"""Red-first R4 (coord-artifact-single-home-01M3V4BE WP09, #5519, #2533).

FR-003 / FR-003a / FR-016 / SC-002 / US2.1: on a coordination-routed Mission,
``decision open`` -> [another coordination writer populates the coordination
Mission dir] -> ``decision open`` through the real CLI entry points must
leave exactly **one** ``status.events.jsonl``, on the coordination surface,
holding both ``DecisionPointOpened`` events with a strictly increasing
clock -- never a second, forked log in the root checkout.

Base failure (pre-WP09): ``decisions/emit.py::_mission_dir`` and
``decisions/service.py::_mission_dir`` resolved the WRITE location through
``read_dir(STATUS_STATE)``, whose ``EMPTY`` -> PRIMARY leniency (C-002) is a
READ-side affordance. The first ``decision open`` on a pre-fix ``EMPTY``
coordination surface therefore writes its event into the REPOSITORY-ROOT
checkout instead of materializing/seeding the coordination Mission dir. Once
something ELSE makes the coordination Mission dir non-empty (another
writer's content lands there), the SECOND ``decision open`` flips to
``read_dir``'s MATERIALIZED branch and writes into a freshly-created,
un-seeded coordination copy -- orphaning the first event and restarting the
Lamport-proxy clock at line 1 instead of continuing from the root checkout's
prior line count.

**Deviation from the literal T048 fixture (documented, binding correction
discovered during implementation):** T048 names ``tracer-append`` as the
intervening writer between the two ``decision open`` calls. Driving the REAL
``tracer-append`` CLI here reproducibly hits an UNRELATED, pre-existing
defect once the coordination Mission dir holds real content:
``retrospective/tracer_writer.py::_local_staging_path`` resolves its LOCAL
staging path through ``candidate_feature_dir_for_mission`` -- a kind-blind,
coordination-husk-consulting READ primitive -- which, once the coordination
Mission dir is non-empty, returns a path physically INSIDE
``.worktrees/<coord>/...``; ``commit_router._group_files_by_partition`` then
misclassifies that already-coord-anchored path, and
``git/commit_helpers.safe_commit`` refuses it with
``SafeCommitPathPolicyError`` ("refusing to stage path under .worktrees/").
This reproduces with ZERO ``decisions/*`` code involved (a manually seeded
coordination Mission dir + a bare ``tracer-append`` CLI call hits it
identically), so it is independent of this WP's diff -- a pre-existing,
out-of-scope defect in ``retrospective/tracer_writer.py`` (named as WP10's
"migrates it" responsibility in the T048 prompt, which did not anticipate
this specific interaction). Reported, not fixed here (Pre-existing Failure
Reporting Rule) -- see the WP09 activity log / tracer file.

This test instead uses a minimal "sentinel" commit -- plain git, no
production write-seam code -- to populate the coordination Mission dir with
unrelated content, simulating "another coordination-aware writer has
legitimately created content there" with the SAME observable effect on
``decisions/service.py``'s own coordination-state read (the coordination
Mission dir transitions from empty to non-empty) that a correctly-migrated
``tracer-append`` would have. This preserves R4's exact reproduction
mechanism and fidelity without depending on the broken, unrelated CLI path.
Verified RED at WP07's tip (``7afabf4eff``, before this WP's fix): the second
decision's ``event_lamport`` resets to ``1`` and lands in a coordination log
containing only itself, while the first decision + the fixture's scaffold
events are orphaned in the root checkout's log.

Decision rows carry NO Lamport field (brownfield-scout correction, binding):
their keys are ``event_id``, ``at``, ``event_type``
(``"DecisionPointOpened"``), ``payload`` -- no ``lamport_clock``, no
``payload.event_lamport``. The clock is the line-count proxy
``_append_raw_event`` returns, surfaced as ``event_lamport`` in
``decision open --json`` (``decision.py``'s ``_open_response_to_dict``). This
test asserts on that CLI-returned value AND on each event's own line
position in the combined log (T048: "assert on that, or on log position").
"""

from __future__ import annotations

import contextlib
import json
import subprocess
from pathlib import Path
from typing import Any

import pytest
from typer.testing import CliRunner

from mission_runtime import MissionTopology
from specify_cli.cli.commands.agent import app as agent_app
from tests._factories.coord_mission import (
    COORD_TOPOLOGIES,
    CoordMission,
    event_ids,
    make_prefix_coord_mission,
)

pytestmark = [pytest.mark.integration, pytest.mark.git_repo]

runner = CliRunner()

_STATUS_LOG_FILENAME = "status.events.jsonl"
_DECISION_POINT_OPENED = "DecisionPointOpened"


def _invoke(args: list[str], cwd: Path) -> Any:
    with contextlib.chdir(cwd):
        return runner.invoke(agent_app, args, catch_exceptions=True)


def _git(repo: Path, *args: str) -> None:
    subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True, text=True)


def _rows(path: Path) -> list[dict[str, Any]]:
    """Parse every non-blank JSONL line of *path*, or ``[]`` if it is absent."""
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _opened_rows(path: Path) -> list[dict[str, Any]]:
    return [row for row in _rows(path) if row.get("event_type") == _DECISION_POINT_OPENED]


def _decision_open(mission_slug: str, repo_root: Path, *, slot_key: str, input_key: str, question: str) -> dict[str, Any]:
    result = _invoke(
        [
            "decision",
            "open",
            "--mission",
            mission_slug,
            "--flow",
            "specify",
            "--slot-key",
            slot_key,
            "--input-key",
            input_key,
            "--question",
            question,
            "--actor",
            "test-r4",
        ],
        repo_root,
    )
    assert result.exit_code == 0, f"decision open failed (exit={result.exit_code}): output={result.output!r} exc={result.exception!r}"
    payload: dict[str, Any] = json.loads(result.output.strip().splitlines()[-1])
    return payload


def _another_writer_populates_coord_mission_dir(coord: CoordMission) -> None:
    """Simulate a different coordination-aware writer landing content between
    the two decision opens (the T048 ``tracer-append`` role -- see the module
    docstring's documented deviation). Plain git only: no production
    write-seam code, so this neither depends on nor masks the decision
    writers' own ``write_dir`` migration under test.
    """
    coord.coord_mission_dir.mkdir(parents=True, exist_ok=True)
    (coord.coord_mission_dir / "SENTINEL.txt").write_text("another writer's content\n", encoding="utf-8")
    _git(coord.coord_worktree_path, "add", "-A")
    _git(coord.coord_worktree_path, "commit", "-q", "-m", "chore(fixture): another coordination writer's content")


@pytest.mark.parametrize("topology", COORD_TOPOLOGIES)
def test_decision_tracer_decision_keeps_one_log_and_monotonic_clock(tmp_path: Path, topology: MissionTopology) -> None:
    """R4 (#5519): decision open -> [another coordination writer] -> decision open; one coordination log, monotonic clock."""
    coord: CoordMission = make_prefix_coord_mission(tmp_path, topology, worktree="absent")

    root_log = coord.root_mission_dir / _STATUS_LOG_FILENAME
    coord_log = coord.coord_mission_dir / _STATUS_LOG_FILENAME
    pre_root_event_ids = set(event_ids(root_log)) if root_log.exists() else set()

    first = _decision_open(coord.mission_slug, coord.repo_root, slot_key="s.a", input_key="a", question="A?")
    _another_writer_populates_coord_mission_dir(coord)
    second = _decision_open(coord.mission_slug, coord.repo_root, slot_key="s.b", input_key="b", question="B?")

    # The root checkout's log gained NO decision event (compare event ids to
    # the pre-test snapshot) -- the scaffold events it already carried are
    # untouched, but no DecisionPointOpened landed there.
    post_root_event_ids = set(event_ids(root_log)) if root_log.exists() else set()
    assert post_root_event_ids == pre_root_event_ids, (
        f"the root checkout's status log gained new events: "
        f"{post_root_event_ids - pre_root_event_ids!r} (a decision event forked onto the root checkout)"
    )
    root_opened = _opened_rows(root_log)
    assert not root_opened, f"root checkout log unexpectedly holds DecisionPointOpened rows: {root_opened!r}"

    # Exactly one of {root, coordination} log carries DecisionPointOpened
    # events, and it is the COORDINATION one.
    coord_opened = _opened_rows(coord_log)
    assert coord_opened, "coordination log holds no DecisionPointOpened rows -- the fork landed elsewhere or nothing was written"

    # It holds BOTH opened events, matched by decision_id (== input_key's
    # decision_id from each CLI response).
    opened_decision_ids = {row["payload"]["decision_point_id"] for row in coord_opened}
    assert first["decision_id"] in opened_decision_ids, f"first decision {first['decision_id']!r} missing from coordination log"
    assert second["decision_id"] in opened_decision_ids, f"second decision {second['decision_id']!r} missing from coordination log"

    # No event id appears twice in the coordination log.
    coord_event_ids = event_ids(coord_log)
    assert len(coord_event_ids) == len(set(coord_event_ids)), f"duplicate event_id in coordination log: {coord_event_ids!r}"

    # Clock: decision rows carry no persisted Lamport field (binding
    # correction) -- assert on the CLI-returned line-count proxy
    # (``event_lamport``) AND on each event's own line position in the
    # combined coordination log, which must agree and strictly increase.
    assert first["event_lamport"] is not None
    assert second["event_lamport"] is not None
    assert second["event_lamport"] > first["event_lamport"], (
        f"clock did not strictly increase across the coordination log: first={first['event_lamport']!r} second={second['event_lamport']!r}"
    )

    all_rows = _rows(coord_log)
    first_positions = [i for i, row in enumerate(all_rows, start=1) if (row.get("payload") or {}).get("decision_point_id") == first["decision_id"]]
    second_positions = [i for i, row in enumerate(all_rows, start=1) if (row.get("payload") or {}).get("decision_point_id") == second["decision_id"]]
    assert first_positions, f"first decision's opened row not found by position in {coord_log}"
    assert second_positions, f"second decision's opened row not found by position in {coord_log}"
    assert max(first_positions) < min(second_positions), "the first decision's row does not precede the second's in the combined coordination log"
