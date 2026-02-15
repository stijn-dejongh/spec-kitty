"""RED: Integration tests for EventBridge wiring (T013)."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


def _write_config(repo_root: Path, content: str) -> None:
    config_dir = repo_root / ".kittify"
    config_dir.mkdir(parents=True, exist_ok=True)
    (config_dir / "config.yaml").write_text(content, encoding="utf-8")


class TestLaneTransitionEventIntegration:
    """End-to-end: config → factory → bridge → JSONL file."""

    def test_lane_transition_emits_event_to_jsonl(self, tmp_path):
        _write_config(
            tmp_path,
            "telemetry:\n  enabled: true\n  log_path: .kittify/events.jsonl\n",
        )
        from specify_cli.core.events import LaneTransitionEvent, load_event_bridge

        bridge = load_event_bridge(tmp_path)
        event = LaneTransitionEvent(
            timestamp=datetime(2026, 2, 15, 10, 30, 0, tzinfo=timezone.utc),
            work_package_id="WP01",
            from_lane="planned",
            to_lane="doing",
        )
        bridge.emit_lane_transition(event)

        log_file = tmp_path / ".kittify" / "events.jsonl"
        assert log_file.exists()
        lines = log_file.read_text().strip().splitlines()
        assert len(lines) == 1

        data = json.loads(lines[0])
        assert data["type"] == "lane_transition"
        assert data["work_package_id"] == "WP01"
        assert data["from_lane"] == "planned"
        assert data["to_lane"] == "doing"
        assert "timestamp" in data

    def test_no_event_file_when_telemetry_disabled(self, tmp_path):
        _write_config(
            tmp_path,
            "telemetry:\n  enabled: false\n",
        )
        from specify_cli.core.events import LaneTransitionEvent, load_event_bridge

        bridge = load_event_bridge(tmp_path)
        event = LaneTransitionEvent(
            timestamp=datetime(2026, 2, 15, tzinfo=timezone.utc),
            work_package_id="WP01",
            from_lane="planned",
            to_lane="doing",
        )
        bridge.emit_lane_transition(event)
        assert not (tmp_path / ".kittify" / "events.jsonl").exists()

    def test_no_event_file_when_no_config(self, tmp_path):
        from specify_cli.core.events import LaneTransitionEvent, load_event_bridge

        bridge = load_event_bridge(tmp_path)
        event = LaneTransitionEvent(
            timestamp=datetime(2026, 2, 15, tzinfo=timezone.utc),
            work_package_id="WP01",
            from_lane="planned",
            to_lane="doing",
        )
        bridge.emit_lane_transition(event)
        # No JSONL file should exist anywhere
        jsonl_files = list(tmp_path.rglob("*.jsonl"))
        assert len(jsonl_files) == 0

    def test_multiple_transitions_produce_ordered_events(self, tmp_path):
        _write_config(
            tmp_path,
            "telemetry:\n  enabled: true\n  log_path: .kittify/events.jsonl\n",
        )
        from specify_cli.core.events import LaneTransitionEvent, load_event_bridge

        bridge = load_event_bridge(tmp_path)
        transitions = [
            ("planned", "doing"),
            ("doing", "for_review"),
            ("for_review", "done"),
        ]
        for from_lane, to_lane in transitions:
            event = LaneTransitionEvent(
                timestamp=datetime(2026, 2, 15, tzinfo=timezone.utc),
                work_package_id="WP01",
                from_lane=from_lane,
                to_lane=to_lane,
            )
            bridge.emit_lane_transition(event)

        log_file = tmp_path / ".kittify" / "events.jsonl"
        lines = log_file.read_text().strip().splitlines()
        assert len(lines) == 3

        for i, (from_lane, to_lane) in enumerate(transitions):
            data = json.loads(lines[i])
            assert data["from_lane"] == from_lane
            assert data["to_lane"] == to_lane


class TestExecutionContextHasEventBridge:
    """ExecutionContext should accept an event_bridge field."""

    def test_execution_context_defaults_to_null_bridge(self):
        from specify_cli.core.events import NullEventBridge
        from specify_cli.orchestrator.executor import ExecutionContext

        ctx = ExecutionContext(
            wp_id="WP01",
            feature_slug="040-test",
            invoker=None,  # type: ignore[arg-type]
            prompt_path=Path("/tmp/test.md"),
            role="implement",
            timeout_seconds=300,
            repo_root=Path("/tmp"),
        )
        assert isinstance(ctx.event_bridge, NullEventBridge)

    def test_execution_context_accepts_custom_bridge(self):
        from specify_cli.core.events import CompositeEventBridge
        from specify_cli.orchestrator.executor import ExecutionContext

        bridge = CompositeEventBridge()
        ctx = ExecutionContext(
            wp_id="WP01",
            feature_slug="040-test",
            invoker=None,  # type: ignore[arg-type]
            prompt_path=Path("/tmp/test.md"),
            role="implement",
            timeout_seconds=300,
            repo_root=Path("/tmp"),
            event_bridge=bridge,
        )
        assert ctx.event_bridge is bridge
