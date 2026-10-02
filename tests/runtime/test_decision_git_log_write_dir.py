"""T052 -- ``DecisionGitLog`` lands at ``write_dir(DECISION_LOG)`` (coord-artifact-single-home-01M3V4BE WP09).

Covers:
- A pre-fix EMPTY coordination Mission is seeded and the resulting
  ``decisions.events.jsonl`` lands at ``write_dir(DECISION_LOG).path /
  "decisions.events.jsonl"`` in the coordination worktree.
- Dir-name agreement: ``DecisionGitLog``'s file dir, ``write_dir(DECISION_LOG).path``
  and the coordination transaction's own ``coord_mission_dir_name`` composition
  all agree for a canonical (mid8-embedding) slug -- the shape
  ``_wrap_with_decision_git_log`` is actually reached with in production
  (``decision.py``'s ``_resolve_repo_root_and_slug`` / ``runtime_bridge``'s
  own identity resolution both canonicalize the handle before it reaches this
  function). The non-canonical (bare-slug) variant is not exercised here --
  see the WP09 final report for why.
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
