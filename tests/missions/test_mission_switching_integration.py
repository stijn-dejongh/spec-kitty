#!/usr/bin/env python3
"""CLI-backed integration tests for mission system (per-feature model v0.8.0+).

Tests mission_list/current/info use the 0.x MissionConfig schema.
On 2.x, mission files use v1 State Machine DSL format which MissionConfig
cannot parse. The switch/blocked tests still work on 2.x (they test error paths).
"""

from __future__ import annotations

from pathlib import Path

import pytest

pytestmark = pytest.mark.git_repo

def test_mission_switch_shows_helpful_error(clean_project: Path, run_cli) -> None:
    """Legacy mission switch surface should fail with current command guidance."""
    result = run_cli(clean_project, "mission", "switch", "research")

    assert result.returncode == 2
    output = result.stdout + result.stderr
    assert "No such command 'mission'" in output
    assert "mission-type" in output

def test_mission_switch_blocked_by_worktrees_via_cli(project_with_worktree: Path, run_cli) -> None:
    """Legacy mission switch surface should still fail with current guidance."""
    result = run_cli(project_with_worktree, "mission", "switch", "research")

    assert result.returncode == 2
    output = result.stdout + result.stderr
    assert "No such command 'mission'" in output
    assert "mission-type" in output
