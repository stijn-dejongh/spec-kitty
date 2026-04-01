import json
from pathlib import Path

from specify_cli.dashboard import scanner
from specify_cli.dashboard.constitution_path import resolve_project_constitution_path
from specify_cli.status.models import Lane, StatusEvent
from specify_cli.status.reducer import materialize
from specify_cli.status.store import append_event

import pytest

pytestmark = pytest.mark.fast


def _set_wp_lane(mission_dir: Path, wp_id: str, lane: str) -> None:
    append_event(
        mission_dir,
        StatusEvent(
            event_id=f"TEST{wp_id}{lane.upper()}0000000000000000"[:26],
            mission_slug=mission_dir.name,
            wp_id=wp_id,
            from_lane=Lane.PLANNED,
            to_lane=Lane(lane),
            at="2026-03-31T09:00:00+00:00",
            actor="test",
            force=True,
            execution_mode="direct_repo",
        ),
    )
    materialize(mission_dir)


def _create_mission(tmp_path: Path, slug: str = "001-demo-mission", *, lane: str = "planned") -> Path:
    mission_dir = tmp_path / "kitty-specs" / slug
    (mission_dir / "tasks").mkdir(parents=True)
    (mission_dir / "spec.md").write_text("# Spec\n", encoding="utf-8")
    (mission_dir / "plan.md").write_text("# Plan\n", encoding="utf-8")
    (mission_dir / "tasks.md").write_text("# Tasks\n", encoding="utf-8")

    prompt = """---
work_package_id: WP01
subtasks: ["T1"]
agent: codex
---
# Work Package Prompt: Demo

Body
"""
    (mission_dir / "tasks" / "WP01-demo.md").write_text(prompt, encoding="utf-8")
    _set_wp_lane(mission_dir, "WP01", lane)
    return mission_dir


def test_scan_all_missions_detects_mission(tmp_path):
    mission_dir = _create_mission(tmp_path)
    missions = scanner.scan_all_missions(tmp_path)
    assert missions, "Expected at least one mission"
    assert missions[0]["id"] == mission_dir.name
    assert missions[0]["artifacts"]["spec"]


def test_scan_all_missions_builds_switcher_display_name(tmp_path):
    mission_dir = _create_mission(tmp_path)
    (mission_dir / "meta.json").write_text(
        json.dumps({"friendly_name": "Demo Mission"}),
        encoding="utf-8",
    )

    missions = scanner.scan_all_missions(tmp_path)

    assert missions[0]["name"] == "Demo Mission"
    assert missions[0]["display_name"] == "001 - Demo Mission"


def test_scan_all_missions_display_name_avoids_duplicate_prefix(tmp_path):
    mission_dir = _create_mission(tmp_path)
    (mission_dir / "meta.json").write_text(
        json.dumps({"friendly_name": "001 - Demo Mission"}),
        encoding="utf-8",
    )

    missions = scanner.scan_all_missions(tmp_path)

    assert missions[0]["display_name"] == "001 - Demo Mission"


def test_scan_mission_kanban_returns_prompt(tmp_path):
    mission_dir = _create_mission(tmp_path)
    lanes = scanner.scan_mission_kanban(tmp_path, mission_dir.name)
    assert "planned" in lanes
    assert lanes["planned"], "planned lane should contain prompt data"
    task = lanes["planned"][0]
    assert task["id"] == "WP01"
    assert "prompt_markdown" in task


def test_resolve_active_mission_requires_explicit_selection(tmp_path):
    """resolve_active_mission returns None — auto-detection was removed.

    Since mission_detection was deleted (WP02), the dashboard no longer
    auto-detects the active mission.  Callers must provide an explicit
    --mission flag.  This test confirms the contract: without heuristics,
    resolve_active_mission always returns None.
    """
    missions = [
        {"id": "009-old-mission"},
        {"id": "010-new-mission"},
    ]

    resolved = scanner.resolve_active_mission(tmp_path, missions)
    assert resolved is None, (
        "resolve_active_mission must return None after removal of auto-detection"
    )


def test_project_constitution_propagates_to_all_missions(tmp_path):
    _create_mission(tmp_path, "001-demo-mission")
    _create_mission(tmp_path, "002-another-mission")
    constitution = tmp_path / ".kittify" / "constitution" / "constitution.md"
    constitution.parent.mkdir(parents=True)
    constitution.write_text("# Project Constitution\n", encoding="utf-8")

    missions = scanner.scan_all_missions(tmp_path)
    assert len(missions) == 2
    assert all(m["artifacts"]["constitution"]["exists"] for m in missions)


def test_mission_local_constitution_is_ignored_without_project_constitution(tmp_path):
    first = _create_mission(tmp_path, "001-demo-mission")
    _create_mission(tmp_path, "002-another-mission")
    (first / "constitution.md").write_text("# Legacy Mission Constitution\n", encoding="utf-8")

    missions = scanner.scan_all_missions(tmp_path)
    assert len(missions) == 2
    assert all(not m["artifacts"]["constitution"]["exists"] for m in missions)


def test_legacy_constitution_path_supported(tmp_path):
    _create_mission(tmp_path, "001-demo-mission")
    _create_mission(tmp_path, "002-another-mission")
    legacy = tmp_path / ".kittify" / "memory" / "constitution.md"
    legacy.parent.mkdir(parents=True)
    legacy.write_text("# Legacy Project Constitution\n", encoding="utf-8")

    missions = scanner.scan_all_missions(tmp_path)
    assert len(missions) == 2
    assert all(m["artifacts"]["constitution"]["exists"] for m in missions)


def test_new_path_preferred_when_both_exist(tmp_path):
    _create_mission(tmp_path)
    new_path = tmp_path / ".kittify" / "constitution" / "constitution.md"
    legacy_path = tmp_path / ".kittify" / "memory" / "constitution.md"
    new_path.parent.mkdir(parents=True)
    legacy_path.parent.mkdir(parents=True)
    new_path.write_text("new", encoding="utf-8")
    legacy_path.write_text("legacy", encoding="utf-8")

    resolved = resolve_project_constitution_path(tmp_path)
    assert resolved == new_path


def test_scan_mission_kanban_approved_lane(tmp_path):
    """WPs with canonical lane approved should land in the approved column."""
    _create_mission(tmp_path, "001-demo", lane="approved")
    lanes = scanner.scan_mission_kanban(tmp_path, "001-demo")
    assert len(lanes["approved"]) == 1
    assert len(lanes["planned"]) == 0
    assert lanes["approved"][0]["id"] == "WP01"


def test_scan_mission_kanban_lane_mapping(tmp_path):
    """claimed maps to planned, in_progress maps to doing."""
    mission_dir = tmp_path / "kitty-specs" / "001-demo"
    (mission_dir / "tasks").mkdir(parents=True)
    for wp_id, lane in [("WP01", "claimed"), ("WP02", "in_progress")]:
        (mission_dir / "tasks" / f"{wp_id}.md").write_text(
            f"---\nwork_package_id: {wp_id}\n---\n# Work Package Prompt: {wp_id}\n",
            encoding="utf-8",
        )
        _set_wp_lane(mission_dir, wp_id, lane)
    lanes = scanner.scan_mission_kanban(tmp_path, "001-demo")
    assert len(lanes["planned"]) == 1  # claimed -> planned
    assert len(lanes["doing"]) == 1  # in_progress -> doing
