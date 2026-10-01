"""Self-tests for the shared coordination-Mission fixture harness (WP02, FR-016).

Pins that each builder in ``tests._factories.coord_mission`` keeps producing
its documented shape at the current base. This WP ships no reproduction --
every assertion here is GREEN by design (analyze C2: red-evidence exempt,
harness only).

How later WPs use this (research red-first list):
    R1/R1b/R6/R20 (WP06) -- ``make_prefix_coord_mission``.
    R2 (WP05)            -- ``make_coord_mission``.
    R3/R14/R15/R16 (WP17) -- ``make_fork_fixture`` (shapes b/c/d).
    R4 (WP09)            -- ``make_prefix_coord_mission`` + ``commits_touching``.
    R22/R23/R24 (WP18)   -- ``make_coord_mission`` / ``event_ids``.
"""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Literal

import pytest

from mission_runtime import MissionTopology
from specify_cli.missions._read_path_resolver import CoordState, probe_coord_state
from tests._factories.coord_mission import (
    COORD_TOPOLOGIES,
    CoordMission,
    ForkFixture,
    coord_tree_has,
    commits_touching,
    event_ids,
    index_entry_ids,
    lamports,
    make_coord_mission,
    make_fork_fixture,
    make_prefix_coord_mission,
)

pytestmark = [pytest.mark.integration, pytest.mark.git_repo]


def _git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True, check=True).stdout.strip()


def _is_ancestor(repo: Path, ancestor_sha: str, descendant_ref: str) -> bool:
    result = subprocess.run(
        ["git", "-C", str(repo), "merge-base", "--is-ancestor", ancestor_sha, descendant_ref],
        capture_output=True,
        text=True,
        check=False,
    )
    return result.returncode == 0


# ---------------------------------------------------------------------------
# T008 -- make_coord_mission, every via x topology
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("via", ["core", "cli_topology", "cli_pr_bound"])
@pytest.mark.parametrize("topology", COORD_TOPOLOGIES, ids=lambda t: t.value)
def test_make_coord_mission_records_requested_topology(
    tmp_path: Path,
    topology: MissionTopology,
    via: Literal["core", "cli_topology", "cli_pr_bound"],
) -> None:
    coord = make_coord_mission(tmp_path, topology, via=via, slug="viacheck")

    assert coord.topology is topology
    assert _git(coord.repo_root, "rev-parse", "--verify", coord.coordination_branch)
    assert _is_ancestor(coord.repo_root, coord.creation_base_sha, coord.target_branch)


def test_make_coord_mission_materialized_true_reaches_materialized(tmp_path: Path) -> None:
    coord = make_coord_mission(tmp_path, MissionTopology.COORD, materialized=True)

    state = probe_coord_state(
        coord.repo_root,
        coord.mission_dir_name,
        coord.mid8,
        coordination_branch=coord.coordination_branch,
    )
    assert state is CoordState.MATERIALIZED
    assert coord.coord_mission_dir.exists()
    # Pre-fix-shaped: no Spec-Kitty-Coordination-Seed trailer on the seed commit.
    log = _git(coord.coord_worktree_path, "log", "-1", "--format=%B")
    assert "Spec-Kitty-Coordination-Seed" not in log


def test_make_coord_mission_protected_primary_marks_target_protected(tmp_path: Path) -> None:
    coord = make_coord_mission(tmp_path, MissionTopology.COORD, via="cli_pr_bound", protected_primary=True)

    config_text = (coord.repo_root / ".kittify" / "config.yaml").read_text(encoding="utf-8")
    assert "protection" in config_text
    assert "main" in config_text


def test_make_coord_mission_unknown_via_raises(tmp_path: Path) -> None:
    # Deliberately outside the `via` Literal, to exercise the runtime
    # fail-closed else-branch a type-correct caller can never reach statically.
    with pytest.raises(ValueError, match="Unknown via"):
        make_coord_mission(tmp_path, MissionTopology.COORD, via="bogus")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# T009 -- make_prefix_coord_mission, every variant
# ---------------------------------------------------------------------------


def _assert_root_log_has_creation_events(coord: CoordMission) -> None:
    ids = event_ids(coord.root_mission_dir / "status.events.jsonl")
    assert ids, "root checkout status log must contain the creation events"


@pytest.mark.parametrize("worktree", ["absent", "empty"])
def test_make_prefix_coord_mission_worktree_variants(tmp_path: Path, worktree: Literal["absent", "empty"]) -> None:
    coord = make_prefix_coord_mission(tmp_path, MissionTopology.COORD, worktree=worktree)

    expected = CoordState.UNMATERIALIZED if worktree == "absent" else CoordState.EMPTY
    state = probe_coord_state(
        coord.repo_root,
        coord.mission_dir_name,
        coord.mid8,
        coordination_branch=coord.coordination_branch,
    )
    assert state is expected
    _assert_root_log_has_creation_events(coord)
    mission_dir_path = f"kitty-specs/{coord.mission_dir_name}"
    assert not coord_tree_has(coord.repo_root, coord.coordination_branch, mission_dir_path)


def test_make_prefix_coord_mission_remote_only(tmp_path: Path) -> None:
    coord = make_prefix_coord_mission(tmp_path, MissionTopology.COORD, remote_only=True)

    state = probe_coord_state(
        coord.repo_root,
        coord.mission_dir_name,
        coord.mid8,
        coordination_branch=coord.coordination_branch,
    )
    assert state is CoordState.UNMATERIALIZED
    # Local head is gone; only the remote-tracking ref remains.
    local_heads = _git(coord.repo_root, "branch", "--list", coord.coordination_branch)
    assert local_heads == ""


def test_make_prefix_coord_mission_branch_deleted(tmp_path: Path) -> None:
    coord = make_prefix_coord_mission(tmp_path, MissionTopology.COORD, branch_deleted=True)

    state = probe_coord_state(
        coord.repo_root,
        coord.mission_dir_name,
        coord.mid8,
        coordination_branch=coord.coordination_branch,
    )
    assert state is CoordState.DELETED


def test_make_prefix_coord_mission_extra_events_are_uncommitted(tmp_path: Path) -> None:
    coord = make_prefix_coord_mission(tmp_path, MissionTopology.COORD, extra_events=2)

    ids = event_ids(coord.root_mission_dir / "status.events.jsonl")
    assert len(ids) == 4  # MissionCreated + SpecifyStarted + 2 extras
    status = _git(coord.repo_root, "status", "--porcelain")
    rel = f"kitty-specs/{coord.mission_dir_name}/status.events.jsonl"
    assert rel in status


@pytest.mark.parametrize("topology", COORD_TOPOLOGIES, ids=lambda t: t.value)
def test_make_prefix_coord_mission_both_topologies(tmp_path: Path, topology: MissionTopology) -> None:
    coord = make_prefix_coord_mission(tmp_path, topology)
    assert coord.topology is topology


# ---------------------------------------------------------------------------
# T010 -- NFR-002 fork fixtures
# ---------------------------------------------------------------------------


def test_fork_fixture_root_uncommitted_coord_untracked(tmp_path: Path) -> None:
    fixture = make_fork_fixture(tmp_path, "root_uncommitted_coord_untracked")

    root_ids = event_ids(fixture.root_mission_dir / "status.events.jsonl")
    coord_ids = event_ids(fixture.coord_mission_dir / "status.events.jsonl")
    assert root_ids and coord_ids
    root_set, coord_set = set(root_ids), set(coord_ids)
    assert not root_set.issubset(coord_set)
    assert not coord_set.issubset(root_set)
    assert fixture.decision_ids_root != fixture.decision_ids_coord

    root_status = _git(fixture.repo_root, "status", "--porcelain")
    assert f"kitty-specs/{fixture.mission_dir_name}/status.events.jsonl" in root_status
    coord_status = _git(fixture.coord_worktree_path, "status", "--porcelain")
    assert "kitty-specs/" in coord_status  # untracked in the coord worktree


def test_fork_fixture_both_committed(tmp_path: Path) -> None:
    fixture = make_fork_fixture(tmp_path, "both_committed")

    # Both event logs are committed on their respective branches -- neither
    # appears as a pending (untracked/modified) path, regardless of other
    # unrelated scaffold files (.kittify/, spec.md, ...) the create path
    # leaves uncommitted in the root checkout.
    root_status = _git(fixture.repo_root, "status", "--porcelain")
    coord_status = _git(fixture.coord_worktree_path, "status", "--porcelain")
    rel = f"kitty-specs/{fixture.mission_dir_name}/status.events.jsonl"
    assert rel not in root_status
    assert rel not in coord_status
    assert coord_tree_has(fixture.repo_root, fixture.coordination_branch, rel)
    assert coord_tree_has(fixture.repo_root, fixture.target_branch, rel)


def test_fork_fixture_fresh_clone(tmp_path: Path) -> None:
    fixture = make_fork_fixture(tmp_path, "fresh_clone")

    assert fixture.clone_root is not None
    assert not (fixture.clone_root / ".worktrees").exists()
    relpath = f"kitty-specs/{fixture.mission_dir_name}/status.events.jsonl"
    ids = event_ids((fixture.clone_root, fixture.coordination_branch, relpath))
    assert ids


def test_fork_fixture_ledger_only_on_coordination(tmp_path: Path) -> None:
    fixture = make_fork_fixture(tmp_path, "ledger_only_on_coordination")

    assert not (fixture.root_mission_dir / "decisions").exists()
    decisions_path = f"kitty-specs/{fixture.mission_dir_name}/decisions"
    assert coord_tree_has(fixture.repo_root, fixture.coordination_branch, decisions_path)
    index_path = f"{decisions_path}/index.json"
    coord_ids = index_entry_ids((fixture.repo_root, fixture.coordination_branch, index_path))
    assert fixture.decision_ids_coord[0] in coord_ids
    target_ids = index_entry_ids((fixture.repo_root, fixture.target_branch, index_path))
    assert target_ids == set()


def test_make_fork_fixture_unknown_shape_raises(tmp_path: Path) -> None:
    # Deliberately outside the `shape` Literal, to exercise the runtime
    # fail-closed else-branch a type-correct caller can never reach statically.
    with pytest.raises(ValueError, match="Unknown fork fixture shape"):
        make_fork_fixture(tmp_path, "bogus-shape")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# T010 -- pure probe tests on a tiny hand-made repo
# ---------------------------------------------------------------------------


@pytest.fixture
def tiny_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "tiny"
    repo.mkdir()
    subprocess.run(["git", "init", "-q", "-b", "main"], cwd=repo, check=True)
    subprocess.run(["git", "config", "user.email", "t@test.com"], cwd=repo, check=True)
    subprocess.run(["git", "config", "user.name", "T"], cwd=repo, check=True)
    (repo / "README.md").write_text("seed\n", encoding="utf-8")
    subprocess.run(["git", "add", "README.md"], cwd=repo, check=True)
    subprocess.run(["git", "commit", "-q", "-m", "seed"], cwd=repo, check=True)
    return repo


@pytest.mark.fast
@pytest.mark.unit
def test_commits_touching_empty_when_path_never_changed(tiny_repo: Path) -> None:
    assert commits_touching(tiny_repo, "HEAD", "never-existed.txt") == []


@pytest.mark.fast
@pytest.mark.unit
def test_commits_touching_non_empty_when_path_changed(tiny_repo: Path) -> None:
    (tiny_repo / "touched.txt").write_text("x\n", encoding="utf-8")
    subprocess.run(["git", "add", "touched.txt"], cwd=tiny_repo, check=True)
    subprocess.run(["git", "commit", "-q", "-m", "touch"], cwd=tiny_repo, check=True)

    shas = commits_touching(tiny_repo, "HEAD", "touched.txt")
    assert len(shas) == 1


@pytest.mark.fast
@pytest.mark.unit
def test_coord_tree_has_true_and_false(tiny_repo: Path) -> None:
    assert coord_tree_has(tiny_repo, "main", "README.md")
    assert not coord_tree_has(tiny_repo, "main", "does-not-exist.md")


@pytest.mark.fast
@pytest.mark.unit
def test_event_ids_and_lamports_tolerate_missing_fields(tmp_path: Path) -> None:
    jsonl = tmp_path / "events.jsonl"
    jsonl.write_text(
        '{"event_id": "A", "lamport_clock": 2}\n{"event_id": "B", "payload": {"event_lamport": 5}}\n{"event_id": "C"}\n',
        encoding="utf-8",
    )

    assert event_ids(jsonl) == ("A", "B", "C")
    assert lamports(jsonl) == (2, 5, None)


@pytest.mark.fast
@pytest.mark.unit
def test_event_ids_absent_file_returns_empty_tuple(tmp_path: Path) -> None:
    assert event_ids(tmp_path / "missing.jsonl") == ()
    assert index_entry_ids(tmp_path / "missing-index.json") == set()


# ---------------------------------------------------------------------------
# T011 -- pytest fixture smoke tests (no clash with existing fixtures in this dir)
# ---------------------------------------------------------------------------


def test_coord_mission_fixture_both_topologies_parametrized(coord_mission: CoordMission) -> None:
    assert coord_mission.topology in COORD_TOPOLOGIES
    assert coord_mission.coordination_branch


def test_prefix_coord_mission_fixture_default_is_empty(prefix_coord_mission: CoordMission) -> None:
    state = probe_coord_state(
        prefix_coord_mission.repo_root,
        prefix_coord_mission.mission_dir_name,
        prefix_coord_mission.mid8,
        coordination_branch=prefix_coord_mission.coordination_branch,
    )
    assert state is CoordState.EMPTY


@pytest.mark.parametrize("prefix_coord_mission", [{"worktree": "absent"}], indirect=True)
def test_prefix_coord_mission_fixture_indirect_override(
    prefix_coord_mission: CoordMission,
) -> None:
    state = probe_coord_state(
        prefix_coord_mission.repo_root,
        prefix_coord_mission.mission_dir_name,
        prefix_coord_mission.mid8,
        coordination_branch=prefix_coord_mission.coordination_branch,
    )
    assert state is CoordState.UNMATERIALIZED


@pytest.mark.parametrize("fork_fixture", ["both_committed"], indirect=True)
def test_fork_fixture_indirect_shape(fork_fixture: ForkFixture) -> None:
    assert fork_fixture.decision_ids_root
    assert fork_fixture.decision_ids_coord
