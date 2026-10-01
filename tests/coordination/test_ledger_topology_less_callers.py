"""C-008: topology-less callers' verdict for decision-ledger paths (WP12, #5023).

Six call sites classify a path's coordination-residue status WITHOUT passing
an explicit ``topology`` -- ``consolidation/executor.py`` (via
``is_toolchain_generated_churn(path, mission_slug=...)``),
``cli/commands/agent/tasks_move_task.py``, ``cli/commands/agent/tasks_shared.py``,
``cli/commands/implement.py`` (two call sites), ``lanes/auto_rebase.py`` and
``coordination/commit_router.py::partition_for_mission_path`` (via
``is_coord_residue_churn(path, mission_slug=...)``). ``is_coord_residue_churn``'s
``topology=None`` default is an EXPLICIT, documented backward-compatible
``MissionTopology.COORD`` projection (see its own docstring).

**Finding (recorded as the design-decisions tracer entry for this WP):**
``kind_is_coordination_residue`` derives PURELY from a kind's partition
membership — ``routes_through_coordination(topology)`` gates first, kind
membership in the COORD partition decides second. Once WP12 (T065) moves
``DECISION_LEDGER`` out of the COORD partition, ``kind_is_coordination_residue``
returns ``False`` for it **regardless of which topology value is fed in** — the
membership check that would have returned ``True`` no longer exists. This means
EVERY one of the six topology-less callers above gets the correct "new PRIMARY
rule" (an uncommitted ledger is real work, never residue) automatically, for
EVERY actual mission topology, with **no code change in ``coherence.py``** —
confirmed empirically by this file (brownfield scout: "T065 step 2 ...
needs no code change"; this file extends that same conclusion one layer up, to
``is_coord_residue_churn``/``is_toolchain_generated_churn`` themselves).

This file is therefore the "single predicate point" characterization the WP
calls for: it pins each caller's OWN call shape directly, over every
:class:`MissionTopology` member (the forced-``COORD`` default never actually
diverges per-topology for this kind), proving the fix is already complete.
"""

from __future__ import annotations

import functools

import pytest

from mission_runtime import MissionArtifactKind, MissionTopology, kind_for_mission_file
from specify_cli.coordination.coherence import (
    is_coord_residue_churn,
    is_toolchain_generated_churn,
)

pytestmark = [pytest.mark.unit, pytest.mark.fast]

_MISSION_SLUG = "some-mission"
_LEDGER_PATHS = (
    f"kitty-specs/{_MISSION_SLUG}/decisions/index.json",
    f"kitty-specs/{_MISSION_SLUG}/decisions/DM-01M1VRA2ABCDEFGHJKMNPQRS.md",
)


@pytest.fixture(autouse=True, params=list(MissionTopology))
def _any_stored_topology(request: pytest.FixtureRequest) -> MissionTopology:
    """Parametrize every test in this module over every real stored topology.

    None of the six callers below ever passes this value in explicitly -- it
    stands for "whatever the mission's REAL stored topology happens to be",
    proving the blind ``topology=None`` default's answer does not vary by it.
    """
    topology: MissionTopology = request.param
    return topology


@pytest.mark.parametrize("path", _LEDGER_PATHS)
def test_commit_router_partition_for_mission_path_shape(path: str, _any_stored_topology: MissionTopology) -> None:
    """``commit_router.py::partition_for_mission_path`` call shape (``mission_slug``, no topology)."""
    assert is_coord_residue_churn(path, mission_slug=_MISSION_SLUG) is False


@pytest.mark.parametrize("path", _LEDGER_PATHS)
def test_tasks_move_task_bare_call_shape(path: str, _any_stored_topology: MissionTopology) -> None:
    """``tasks_move_task.py::_drop_lane_coord_residue`` call shape (bare path, no slug, no topology).

    "A caller that passes neither topology nor slug: list it and keep the base
    behaviour" -- the base behaviour (COORD-projected, kind-membership-derived)
    is what this pins; it is unaffected by the mission's real stored topology
    because the call never threads it.
    """
    assert is_coord_residue_churn(path) is False


@pytest.mark.parametrize("path", _LEDGER_PATHS)
def test_tasks_shared_bare_call_shape(path: str, _any_stored_topology: MissionTopology) -> None:
    """``tasks_shared.py`` call shape (bare path, no slug, no topology)."""
    assert is_coord_residue_churn(path) is False


@pytest.mark.parametrize("path", _LEDGER_PATHS)
def test_implement_py_bare_call_shape(path: str, _any_stored_topology: MissionTopology) -> None:
    """``implement.py``'s two call sites (``_partition_files_for_commit`` /
    ``_guard_planning_commit_partition``), both bare (no slug, no topology)."""
    assert is_coord_residue_churn(path) is False


@pytest.mark.parametrize("path", _LEDGER_PATHS)
def test_auto_rebase_bare_call_shape(path: str, _any_stored_topology: MissionTopology) -> None:
    """``lanes/auto_rebase.py`` call shape (bare path, no slug, no topology).

    For the now-PRIMARY ledger, an uncommitted ``decisions/`` file at a
    coordination Mission is real work, not residue -- the deliberate widening
    this WP's binding corrections call for "at every caller, including
    move-task, implement and auto-rebase".
    """
    assert is_coord_residue_churn(path) is False
    kind = kind_for_mission_file(path)
    assert kind is MissionArtifactKind.DECISION_LEDGER


@pytest.mark.parametrize("path", _LEDGER_PATHS)
def test_consolidation_executor_post_merge_invariant_shape(path: str, _any_stored_topology: MissionTopology) -> None:
    """``consolidation/executor.py``'s post-merge invariant gate call shape
    (``is_toolchain_generated_churn(path_part, mission_slug=run.mission_slug)``,
    no topology)."""
    is_residue = functools.partial(is_toolchain_generated_churn, mission_slug=_MISSION_SLUG)
    assert is_residue(path) is False
