"""RED: Acceptance tests for event bridge factory (T008)."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from specify_cli.core.events import CompositeEventBridge, NullEventBridge
from specify_cli.core.events.factory import load_event_bridge


def _write_config(repo_root: Path, content: str) -> None:
    config_dir = repo_root / ".kittify"
    config_dir.mkdir(parents=True, exist_ok=True)
    (config_dir / "config.yaml").write_text(content, encoding="utf-8")


class TestLoadEventBridge:
    """Acceptance tests for load_event_bridge factory."""

    def test_returns_null_bridge_when_no_config_file(self, tmp_path):
        result = load_event_bridge(tmp_path)
        assert isinstance(result, NullEventBridge)

    def test_returns_null_bridge_when_telemetry_disabled(self, tmp_path):
        _write_config(
            tmp_path,
            "telemetry:\n  enabled: false\n",
        )
        result = load_event_bridge(tmp_path)
        assert isinstance(result, NullEventBridge)

    def test_returns_null_bridge_when_telemetry_key_missing(self, tmp_path):
        _write_config(tmp_path, "agents:\n  available:\n    - claude\n")
        result = load_event_bridge(tmp_path)
        assert isinstance(result, NullEventBridge)

    def test_returns_composite_bridge_when_enabled(self, tmp_path):
        _write_config(
            tmp_path,
            "telemetry:\n  enabled: true\n  log_path: events.jsonl\n",
        )
        result = load_event_bridge(tmp_path)
        assert isinstance(result, CompositeEventBridge)

    def test_returns_null_bridge_on_malformed_yaml(self, tmp_path):
        _write_config(tmp_path, "{{{{")
        result = load_event_bridge(tmp_path)
        assert isinstance(result, NullEventBridge)

    def test_factory_resolves_relative_log_path(self, tmp_path):
        _write_config(
            tmp_path,
            "telemetry:\n  enabled: true\n  log_path: .kittify/events.jsonl\n",
        )
        bridge = load_event_bridge(tmp_path)
        from specify_cli.core.events import LaneTransitionEvent

        event = LaneTransitionEvent(
            timestamp=datetime(2026, 2, 15, tzinfo=timezone.utc),
            work_package_id="WP01",
            from_lane="planned",
            to_lane="doing",
        )
        bridge.emit_lane_transition(event)
        assert (tmp_path / ".kittify" / "events.jsonl").exists()

    def test_default_log_path_used_when_not_specified(self, tmp_path):
        _write_config(
            tmp_path,
            "telemetry:\n  enabled: true\n",
        )
        result = load_event_bridge(tmp_path)
        assert isinstance(result, CompositeEventBridge)
