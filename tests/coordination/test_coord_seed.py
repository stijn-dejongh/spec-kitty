"""Red-first state-matrix tests for the write-location core (mission coord-artifact-single-home-01M3V4BE, WP03).

See ``contracts/write-location-accessor.md`` / ``contracts/seed.md``. Fixtures
come from the shared harness (``tests/_factories/coord_mission.py``, WP02).
"""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from mission_runtime import Establishment, MissionArtifactKind, MissionTopology, TopologySurface, placement_seam
from specify_cli.coordination.coord_seed import (
    COORD_SEED_TRAILER,
    CoordSeedForkRefused,
    establish_coord_write_location,
)
from specify_cli.coordination.surface_resolver import CoordinationBranchDeleted, CoordinationWorktreeUnmaterialized
from specify_cli.missions._read_path_resolver import CoordState, probe_coord_state
from specify_cli.status.locking import feature_status_lock
from tests._factories.coord_mission import (
    CoordMission,
    event_ids,
    make_coord_mission,
    make_fork_fixture,
    make_prefix_coord_mission,
)

pytestmark = [pytest.mark.fast]

_STATUS_LOG = "status.events.jsonl"

_TOPOLOGIES = (MissionTopology.COORD, MissionTopology.LANES_WITH_COORD)


def _refs(coord: CoordMission) -> tuple[str, str]:
    target = subprocess.run(
        ["git", "-C", str(coord.repo_root), "rev-parse", coord.target_branch],
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()
    branch = subprocess.run(
        ["git", "-C", str(coord.repo_root), "rev-parse", coord.coordination_branch],
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()
    return target, branch


def _trailer_mission_ids(coord: CoordMission) -> set[str]:
    result = subprocess.run(
        ["git", "-C", str(coord.repo_root), "log", f"--format=%(trailers:key={COORD_SEED_TRAILER},valueonly)", coord.coordination_branch],
        capture_output=True,
        text=True,
        check=False,
    )
    return {line.strip() for line in result.stdout.splitlines() if line.strip()}


# ---------------------------------------------------------------------------
# T012: the write-side assertion through the pre-existing entry point (C-002).
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("topology", _TOPOLOGIES)
def test_write_side_uses_coord_dir_while_read_dir_keeps_the_empty_fallback(tmp_path: Path, topology: MissionTopology) -> None:
    """The write side diverges from today's read-side EMPTY fallback (C-002 stays green)."""
    coord = make_prefix_coord_mission(tmp_path, topology, worktree="empty")

    # Today's read-side EMPTY fallback: no coordination Mission dir yet, so
    # ``read_dir`` degrades to the repository root checkout.
    read_dir = placement_seam(coord.repo_root, coord.mission_dir_name).read_dir(MissionArtifactKind.STATUS_STATE)
    assert read_dir == coord.root_mission_dir

    location = establish_coord_write_location(coord.repo_root, coord.mission_dir_name, MissionArtifactKind.STATUS_STATE, owned=None)

    assert location.path == coord.coord_mission_dir
    assert location.surface is TopologySurface.COORD
    assert location.establishment is Establishment.SEEDED
    assert (location.path / _STATUS_LOG).exists()
    assert event_ids(location.path / _STATUS_LOG) == event_ids(coord.root_mission_dir / _STATUS_LOG)


# ---------------------------------------------------------------------------
# T017: state-row matrix.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("topology", _TOPOLOGIES)
def test_materialized_is_side_effect_free(tmp_path: Path, topology: MissionTopology) -> None:
    coord = make_coord_mission(tmp_path, topology, materialized=True)
    before_target, before_branch = _refs(coord)

    location = establish_coord_write_location(coord.repo_root, coord.mission_dir_name, MissionArtifactKind.STATUS_STATE, owned=None)

    assert location.establishment is Establishment.NONE
    assert location.coord_state_before is CoordState.MATERIALIZED
    after_target, after_branch = _refs(coord)
    assert (before_target, before_branch) == (after_target, after_branch)


@pytest.mark.parametrize("topology", _TOPOLOGIES)
def test_unmaterialized_local_head_materializes(tmp_path: Path, topology: MissionTopology) -> None:
    coord = make_prefix_coord_mission(tmp_path, topology, worktree="absent")
    assert probe_coord_state(coord.repo_root, coord.mission_dir_name, coord.mid8, coordination_branch=coord.coordination_branch) is CoordState.UNMATERIALIZED

    location = establish_coord_write_location(coord.repo_root, coord.mission_dir_name, MissionArtifactKind.STATUS_STATE, owned=None)

    assert coord.coord_worktree_path.exists()
    assert location.establishment is Establishment.SEEDED
    assert location.coord_state_before is CoordState.UNMATERIALIZED


@pytest.mark.parametrize("topology", _TOPOLOGIES)
def test_remote_only_branch_refuses_and_writes_nothing(tmp_path: Path, topology: MissionTopology) -> None:
    coord = make_prefix_coord_mission(tmp_path, topology, remote_only=True)

    with pytest.raises(CoordinationWorktreeUnmaterialized):
        establish_coord_write_location(coord.repo_root, coord.mission_dir_name, MissionArtifactKind.STATUS_STATE, owned=None)

    assert not coord.coord_worktree_path.exists()


@pytest.mark.parametrize("topology", _TOPOLOGIES)
def test_deleted_branch_refuses(tmp_path: Path, topology: MissionTopology) -> None:
    coord = make_prefix_coord_mission(tmp_path, topology, branch_deleted=True)

    with pytest.raises(CoordinationBranchDeleted):
        establish_coord_write_location(coord.repo_root, coord.mission_dir_name, MissionArtifactKind.STATUS_STATE, owned=None)


@pytest.mark.parametrize("topology", _TOPOLOGIES)
def test_prefix_empty_seeds(tmp_path: Path, topology: MissionTopology) -> None:
    coord = make_prefix_coord_mission(tmp_path, topology, worktree="empty")

    location = establish_coord_write_location(coord.repo_root, coord.mission_dir_name, MissionArtifactKind.STATUS_STATE, owned=None)

    assert location.establishment is Establishment.SEEDED
    assert location.seed is not None
    assert location.seed.coord_commit is not None
    mission_meta_id = _read_mission_id_for(coord)
    assert mission_meta_id in _trailer_mission_ids(coord)


def _read_mission_id_for(coord: CoordMission) -> str:
    import json

    meta = json.loads((coord.root_mission_dir / "meta.json").read_text(encoding="utf-8"))
    return str(meta["mission_id"])


@pytest.mark.parametrize("topology", _TOPOLOGIES)
def test_post_fix_empty_restores_from_branch_with_loud_warning(tmp_path: Path, topology: MissionTopology, caplog: pytest.LogCaptureFixture) -> None:
    coord = make_prefix_coord_mission(tmp_path, topology, worktree="empty")
    # First establish: pre-fix EMPTY -> SEEDED (the Mission becomes post-fix).
    establish_coord_write_location(coord.repo_root, coord.mission_dir_name, MissionArtifactKind.STATUS_STATE, owned=None)
    assert probe_coord_state(coord.repo_root, coord.mission_dir_name, coord.mid8, coordination_branch=coord.coordination_branch) is CoordState.MATERIALIZED

    # Simulate the regression: the Mission dir is removed from the worktree.
    import shutil

    shutil.rmtree(coord.coord_mission_dir)
    assert probe_coord_state(coord.repo_root, coord.mission_dir_name, coord.mid8, coordination_branch=coord.coordination_branch) is CoordState.EMPTY

    with caplog.at_level("WARNING"):
        location = establish_coord_write_location(coord.repo_root, coord.mission_dir_name, MissionArtifactKind.STATUS_STATE, owned=None)

    assert location.establishment is Establishment.RESTORED_FROM_BRANCH
    assert (coord.coord_mission_dir / _STATUS_LOG).exists()
    assert any("missing from worktree" in record.message for record in caplog.records)


# ---------------------------------------------------------------------------
# Fork refusal (NFR-002).
# ---------------------------------------------------------------------------


def test_fork_refuses_and_writes_nothing(tmp_path: Path) -> None:
    fixture = make_fork_fixture(tmp_path, "root_uncommitted_coord_untracked", MissionTopology.COORD, stream="status_log")
    root_before = (fixture.root_mission_dir / _STATUS_LOG).read_bytes()
    coord_before = (fixture.coord_mission_dir / _STATUS_LOG).read_bytes()

    with pytest.raises(CoordSeedForkRefused) as excinfo:
        establish_coord_write_location(fixture.repo_root, fixture.mission_dir_name, MissionArtifactKind.STATUS_STATE, owned=None)

    # The divergence is reported by the row's own ``event_id`` (the prefix/fork
    # classifier's unit), not the decision-payload id the fixture tracks
    # separately -- just assert both sides are named and genuinely differ.
    assert excinfo.value.first_divergence_root is not None
    assert excinfo.value.first_divergence_coord is not None
    assert excinfo.value.first_divergence_root != excinfo.value.first_divergence_coord
    assert excinfo.value.coord_ref == fixture.coordination_branch
    assert fixture.mission_dir_name in excinfo.value.coord_path
    assert (fixture.root_mission_dir / _STATUS_LOG).read_bytes() == root_before
    assert (fixture.coord_mission_dir / _STATUS_LOG).read_bytes() == coord_before


# ---------------------------------------------------------------------------
# Idempotence.
# ---------------------------------------------------------------------------


def test_second_call_is_idempotent(tmp_path: Path) -> None:
    coord = make_prefix_coord_mission(tmp_path, MissionTopology.COORD, worktree="empty")
    first = establish_coord_write_location(coord.repo_root, coord.mission_dir_name, MissionArtifactKind.STATUS_STATE, owned=None)
    assert first.seed is not None and first.seed.coord_commit is not None

    before_ids = event_ids(coord.coord_mission_dir / _STATUS_LOG)
    _, branch_before = _refs(coord)

    second = establish_coord_write_location(coord.repo_root, coord.mission_dir_name, MissionArtifactKind.STATUS_STATE, owned=None)

    _, branch_after = _refs(coord)
    assert branch_before == branch_after
    assert second.seed is None
    after_ids = event_ids(coord.coord_mission_dir / _STATUS_LOG)
    assert after_ids == before_ids
    assert len(set(after_ids)) == len(after_ids)


# ---------------------------------------------------------------------------
# Atomicity.
# ---------------------------------------------------------------------------


def test_rename_failure_leaves_only_a_temp_dir_and_next_call_heals(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    coord = make_prefix_coord_mission(tmp_path, MissionTopology.COORD, worktree="empty")

    import os as os_module

    real_rename = os_module.rename
    calls = {"n": 0}

    def _flaky_rename(src: str | Path, dst: str | Path) -> None:
        calls["n"] += 1
        if calls["n"] == 1:
            raise OSError("simulated rename failure")
        real_rename(src, dst)

    monkeypatch.setattr(os_module, "rename", _flaky_rename)

    with pytest.raises(OSError, match="simulated rename failure"):
        establish_coord_write_location(coord.repo_root, coord.mission_dir_name, MissionArtifactKind.STATUS_STATE, owned=None)

    assert probe_coord_state(coord.repo_root, coord.mission_dir_name, coord.mid8, coordination_branch=coord.coordination_branch) is CoordState.EMPTY
    stale = list((coord.coord_worktree_path / "kitty-specs").glob(f".{coord.mission_dir_name}.seed-*"))
    assert len(stale) == 1

    monkeypatch.undo()
    location = establish_coord_write_location(coord.repo_root, coord.mission_dir_name, MissionArtifactKind.STATUS_STATE, owned=None)
    assert location.establishment is Establishment.SEEDED
    assert not list((coord.coord_worktree_path / "kitty-specs").glob(f".{coord.mission_dir_name}.seed-*"))


# ---------------------------------------------------------------------------
# Root restoration.
# ---------------------------------------------------------------------------


def test_root_restoration_untracked_extra_events_removed(tmp_path: Path) -> None:
    coord = make_prefix_coord_mission(tmp_path, MissionTopology.COORD, worktree="empty", extra_events=1)
    root_path = coord.root_mission_dir / _STATUS_LOG
    status_before = subprocess.run(
        ["git", "-C", str(coord.repo_root), "status", "--porcelain", "--", str(root_path.relative_to(coord.repo_root))],
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    assert status_before.strip().startswith("M") or "M" in status_before  # tracked + dirty (extra uncommitted event appended)

    location = establish_coord_write_location(coord.repo_root, coord.mission_dir_name, MissionArtifactKind.STATUS_STATE, owned=None)

    assert location.seed is not None
    assert str(root_path.relative_to(coord.repo_root)) in location.seed.restored_root
    status_after = subprocess.run(
        ["git", "-C", str(coord.repo_root), "status", "--porcelain", "--", str(root_path.relative_to(coord.repo_root))],
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    assert status_after.strip() == ""


# ---------------------------------------------------------------------------
# Lock reentrancy.
# ---------------------------------------------------------------------------


def test_lock_reentrancy_no_deadlock(tmp_path: Path) -> None:
    coord = make_prefix_coord_mission(tmp_path, MissionTopology.COORD, worktree="empty")

    with feature_status_lock(coord.repo_root, coord.mission_dir_name, timeout=5.0):
        location = establish_coord_write_location(coord.repo_root, coord.mission_dir_name, MissionArtifactKind.STATUS_STATE, owned=None)

    assert location.establishment is Establishment.SEEDED


# ---------------------------------------------------------------------------
# NFR-002: event counts never shrink.
# ---------------------------------------------------------------------------


def test_nfr002_event_count_never_reduced(tmp_path: Path) -> None:
    coord = make_prefix_coord_mission(tmp_path, MissionTopology.COORD, worktree="empty", extra_events=2)
    root_ids_before = event_ids(coord.root_mission_dir / _STATUS_LOG)

    location = establish_coord_write_location(coord.repo_root, coord.mission_dir_name, MissionArtifactKind.STATUS_STATE, owned=None)

    coord_ids_after = event_ids(location.path / _STATUS_LOG)
    assert set(root_ids_before) <= set(coord_ids_after)
    assert len(set(coord_ids_after)) == len(coord_ids_after)


# ---------------------------------------------------------------------------
# C-008 controls: non-coordination topologies pass through unchanged.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("topology", [MissionTopology.LANES, MissionTopology.SINGLE_BRANCH])
def test_coordless_topology_is_primary_and_side_effect_free(tmp_path: Path, topology: MissionTopology) -> None:
    from specify_cli.core.mission_creation import create_mission_core
    from tests._factories import provision_test_charter
    from tests._support.git_template import clone_template

    repo = clone_template(tmp_path / "repo")
    provision_test_charter(repo)
    subprocess.run(["git", "-C", str(repo), "add", ".kittify"], check=True, capture_output=True)
    subprocess.run(["git", "-C", str(repo), "commit", "-m", "chore(fixture): provision charter"], check=True, capture_output=True)
    subprocess.run(["git", "-C", str(repo), "checkout", "-b", "topic"], check=True, capture_output=True)
    create_mission_core(repo, "flat", topology=topology, target_branch="topic", allow_worktree_context=True)

    before = subprocess.run(["git", "-C", str(repo), "status", "--porcelain"], capture_output=True, text=True, check=True).stdout

    location = establish_coord_write_location(repo, "flat", MissionArtifactKind.STATUS_STATE, owned=None)

    assert location.surface is TopologySurface.PRIMARY
    assert location.establishment is Establishment.NONE
    assert location.coord_state_before is None
    after = subprocess.run(["git", "-C", str(repo), "status", "--porcelain"], capture_output=True, text=True, check=True).stdout
    assert before == after


# ---------------------------------------------------------------------------
# Negative test (round 5, X1): a pre-fix MATERIALIZED Mission (#5519 shape)
# with an extra uncommitted COORD record never gets a phantom seed commit.
# ---------------------------------------------------------------------------


def test_materialized_pre_fix_with_uncommitted_extra_record_never_seeds(tmp_path: Path) -> None:
    coord = make_coord_mission(tmp_path, MissionTopology.COORD, materialized=True)
    assert (
        COORD_SEED_TRAILER
        not in subprocess.run(
            ["git", "-C", str(coord.repo_root), "log", coord.coordination_branch],
            capture_output=True,
            text=True,
            check=True,
        ).stdout
    )

    # Append an UNCOMMITTED extra row directly into the coordination copy.
    extra_row = '{"event_id": "01EXTRAUNCOMMITTEDROW0"}\n'
    with (coord.coord_mission_dir / _STATUS_LOG).open("a", encoding="utf-8") as handle:
        handle.write(extra_row)

    before_target, before_branch = _refs(coord)
    location = establish_coord_write_location(coord.repo_root, coord.mission_dir_name, MissionArtifactKind.STATUS_STATE, owned=None)
    after_target, after_branch = _refs(coord)

    assert location.establishment is Establishment.NONE
    assert location.seed is None
    assert (before_target, before_branch) == (after_target, after_branch)
    assert not _trailer_mission_ids(coord)
    # The uncommitted row is untouched -- establish never commits, never discards it.
    assert extra_row.strip() in (coord.coord_mission_dir / _STATUS_LOG).read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# Defensive: a PRIMARY-partition kind returns the primary location (no probe).
# ---------------------------------------------------------------------------


def test_primary_kind_returns_primary_location_defensively(tmp_path: Path) -> None:
    coord = make_coord_mission(tmp_path, MissionTopology.COORD)

    location = establish_coord_write_location(coord.repo_root, coord.mission_dir_name, MissionArtifactKind.SPEC, owned=None)

    assert location.surface is TopologySurface.PRIMARY
    assert location.establishment is Establishment.NONE
    assert location.path == coord.root_mission_dir
