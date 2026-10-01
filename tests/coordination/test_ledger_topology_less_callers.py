"""C-008: topology-less callers' verdict for decision-ledger paths (WP12, #5023).

Six call sites classify a path's coordination-residue status WITHOUT passing
an explicit ``topology`` to :func:`~specify_cli.coordination.coherence.
is_coord_residue_churn` / :func:`~specify_cli.coordination.coherence.
is_toolchain_generated_churn` -- its ``topology=None`` default is an EXPLICIT,
documented backward-compatible ``MissionTopology.COORD`` projection (see its
own docstring). Four of the six pass NEITHER a ``topology`` NOR a
``mission_slug`` at all (the truly "blind" shape):

- ``cli/commands/agent/tasks_move_task.py::_drop_lane_coord_residue``
- ``cli/commands/agent/tasks_shared.py::_list_wp_branch_mission_specs_changes``
- ``cli/commands/implement.py::_partition_files_for_commit`` /
  ``_guard_planning_commit_partition`` (two call sites, same file)
- ``lanes/auto_rebase.py::_is_coordination_owned_artifact``

Two pass ``mission_slug`` but not ``topology``:

- ``coordination/commit_router.py::partition_for_mission_path`` (deliberately
  topology-blind by its own docstring, to agree with
  ``_group_files_by_partition``'s grouping);
- ``consolidation/executor.py``'s post-merge invariant gate (via
  ``is_toolchain_generated_churn(path_part, mission_slug=run.mission_slug)``).

This file drives the FIRST FOUR plus ``commit_router`` through their own real
entry points (DIRECTIVE_041: assert the reader's observable decision, never
the shared predicate directly) on a REAL coordination Mission built through
WP02's production-create-path factory. ``consolidation/executor``'s shape is
covered in ``tests/mission_runtime/test_decision_ledger_reader_flips.py::
test_injected_residue_predicate_treats_ledger_as_real_work``.

**C-008 status (binding correction, escalated to the operator -- see the
``design-decisions`` tracer entry for the ruling this file currently
reflects):** once ``DECISION_LEDGER`` leaves the COORD partition (T065), NO
topology value makes ``kind_is_coordination_residue`` return True for it --
the membership check the forced-COORD default relied on no longer exists. So
every one of the six callers above returns "real work, never residue" for a
coordination Mission (asserted below). The ruling's OTHER half -- what a
``lanes`` / ``single_branch`` Mission should observe at these SAME blind call
sites -- is NOT yet resolved (the recorded ruling text is self-contradictory:
"keep today's verdict" + "no compatibility set" cannot both hold once the
kind's own partition has moved) and is deliberately NOT characterized here
pending that ruling. Do not add a lanes/single_branch characterization to this
file, and do not change ``coherence.py``'s resolution logic, until the operator
amendment lands.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from mission_runtime import MissionTopology
from tests._factories.coord_mission import make_coord_mission

pytestmark = [pytest.mark.unit, pytest.mark.git_repo]


def test_tasks_move_task_keeps_ledger_as_real_work(tmp_path: Path) -> None:
    """``tasks_move_task.py::_drop_lane_coord_residue`` (~L824), the truly blind
    shape (no mission_slug, no topology): a dirty ``decisions/index.json`` must
    be KEPT in the lane deliverable set, not dropped as coordination residue.
    """
    from specify_cli.cli.commands.agent.tasks_move_task import _drop_lane_coord_residue

    coord = make_coord_mission(tmp_path, MissionTopology.COORD)
    index_path = coord.root_mission_dir / "decisions" / "index.json"
    index_path.parent.mkdir(parents=True, exist_ok=True)
    index_path.write_text('{"entries": []}\n', encoding="utf-8")

    kept = _drop_lane_coord_residue(coord.repo_root, (index_path,))

    assert index_path in kept, (
        "decisions/index.json was dropped as coordination residue by "
        "_drop_lane_coord_residue -- the PRIMARY-partition ledger is real "
        "lane work and must survive the Seam-A filter (FR-009, #5023)"
    )


def test_implement_partition_files_for_commit_classifies_ledger_primary(tmp_path: Path) -> None:
    """``implement.py::_partition_files_for_commit`` (~L905), the truly blind
    shape (bare path string, no mission_slug, no topology): the ledger joins
    the PRIMARY group, not the COORD-residue group.
    """
    from specify_cli.cli.commands.implement import _partition_files_for_commit

    coord = make_coord_mission(tmp_path, MissionTopology.COORD)
    rel = f"kitty-specs/{coord.mission_dir_name}/decisions/index.json"

    primary_files, coord_files = _partition_files_for_commit([rel])

    assert primary_files == [rel], (primary_files, coord_files)
    assert coord_files == []


def test_implement_guard_refuses_ledger_reaching_coord_seam(tmp_path: Path) -> None:
    """``implement.py::_guard_planning_commit_partition`` (~L947), the truly
    blind shape: a PRIMARY-kind ledger path reaching a COORD-destination
    commit seam is now the FORBIDDEN PRIMARY→coord route (it was the
    permitted same-partition route pre-WP12); reaching a PRIMARY destination
    is the permitted route.
    """
    from specify_cli.cli.commands.implement import _guard_planning_commit_partition
    from specify_cli.coordination.commit_router import PrimaryKindReachedCoordStagingError

    coord = make_coord_mission(tmp_path, MissionTopology.COORD)
    rel = f"kitty-specs/{coord.mission_dir_name}/decisions/index.json"

    with pytest.raises(PrimaryKindReachedCoordStagingError):
        _guard_planning_commit_partition([rel], destination_is_coord=True)

    # The mirror route (PRIMARY destination) is permitted -- no raise.
    _guard_planning_commit_partition([rel], destination_is_coord=False)


def test_auto_rebase_does_not_treat_ledger_as_coordination_owned(tmp_path: Path) -> None:
    """``lanes/auto_rebase.py::_is_coordination_owned_artifact`` (~L225), the
    truly blind shape (bare rel path): the ledger is neither surface residue
    nor managed PRIMARY layout, so auto-rebase does NOT take-theirs resolve a
    conflict on it -- it surfaces as a real (Manual-halt-eligible) conflict,
    matching "an uncommitted ledger file is real work, not residue."
    """
    from specify_cli.lanes.auto_rebase import _is_coordination_owned_artifact

    coord = make_coord_mission(tmp_path, MissionTopology.COORD)
    rel = f"kitty-specs/{coord.mission_dir_name}/decisions/index.json"

    assert _is_coordination_owned_artifact(rel) is False


def test_commit_router_partition_for_mission_path_classifies_ledger_primary(tmp_path: Path) -> None:
    """``commit_router.py::partition_for_mission_path`` (~L768/937): passes
    ``mission_slug`` but deliberately never ``topology`` (its own docstring:
    topology-blind on purpose, to agree with ``_group_files_by_partition``'s
    grouping). The ledger now classifies "primary".
    """
    from specify_cli.coordination.commit_router import partition_for_mission_path

    coord = make_coord_mission(tmp_path, MissionTopology.COORD)
    index_path = coord.root_mission_dir / "decisions" / "index.json"
    index_path.parent.mkdir(parents=True, exist_ok=True)
    index_path.write_text('{"entries": []}\n', encoding="utf-8")

    assert partition_for_mission_path(coord.repo_root, coord.mission_dir_name, index_path) == "primary"
