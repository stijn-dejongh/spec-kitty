"""RED: Acceptance tests for JsonlEventWriter (T007)."""

from __future__ import annotations

import json
import os
import stat
from datetime import datetime, timezone

import pytest

from specify_cli.core.events import (
    ExecutionEvent,
    LaneTransitionEvent,
    ValidationEvent,
)
from specify_cli.telemetry.jsonl_writer import JsonlEventWriter


@pytest.fixture
def sample_event():
    return LaneTransitionEvent(
        timestamp=datetime(2026, 2, 15, tzinfo=timezone.utc),
        work_package_id="WP01",
        from_lane="planned",
        to_lane="doing",
    )


class TestJsonlEventWriter:
    """Acceptance tests for JSONL file writing."""

    def test_writes_single_event_as_json_line(self, tmp_path, sample_event):
        log_file = tmp_path / "events.jsonl"
        writer = JsonlEventWriter(log_file)
        writer.handle(sample_event)

        lines = log_file.read_text().strip().splitlines()
        assert len(lines) == 1

        data = json.loads(lines[0])
        assert data["type"] == "lane_transition"
        assert data["work_package_id"] == "WP01"
        assert data["from_lane"] == "planned"
        assert data["to_lane"] == "doing"
        assert "timestamp" in data

    def test_appends_multiple_events(self, tmp_path, sample_event):
        log_file = tmp_path / "events.jsonl"
        writer = JsonlEventWriter(log_file)
        for _ in range(3):
            writer.handle(sample_event)

        lines = log_file.read_text().strip().splitlines()
        assert len(lines) == 3

    def test_each_line_is_valid_json(self, tmp_path):
        log_file = tmp_path / "events.jsonl"
        writer = JsonlEventWriter(log_file)

        events = [
            LaneTransitionEvent(
                timestamp=datetime(2026, 2, 15, tzinfo=timezone.utc),
                work_package_id="WP01",
                from_lane="planned",
                to_lane="doing",
            ),
            ValidationEvent(
                timestamp=datetime(2026, 2, 15, tzinfo=timezone.utc),
                validation_type="dependency_check",
                status="passed",
            ),
            ExecutionEvent(
                timestamp=datetime(2026, 2, 15, tzinfo=timezone.utc),
                work_package_id="WP02",
                tool_id="claude",
                model="sonnet-4",
            ),
        ]
        for event in events:
            writer.handle(event)

        lines = log_file.read_text().strip().splitlines()
        for line in lines:
            data = json.loads(line)
            assert "type" in data
            assert "timestamp" in data

    def test_graceful_failure_on_unwritable_path(self, sample_event, caplog):
        writer = JsonlEventWriter(
            log_path=__import__("pathlib").Path("/nonexistent/dir/events.jsonl")
        )
        writer.handle(sample_event)  # must NOT raise
        assert any("Failed to write event" in rec.message for rec in caplog.records)

    def test_graceful_failure_on_read_only_directory(
        self, tmp_path, sample_event, caplog
    ):
        ro_dir = tmp_path / "readonly"
        ro_dir.mkdir()
        log_file = ro_dir / "events.jsonl"
        os.chmod(ro_dir, stat.S_IRUSR | stat.S_IXUSR)
        try:
            writer = JsonlEventWriter(log_file)
            writer.handle(sample_event)  # must NOT raise
            assert any(
                "Failed to write event" in rec.message for rec in caplog.records
            )
        finally:
            os.chmod(ro_dir, stat.S_IRWXU)

    def test_jsonl_no_trailing_comma_or_array_wrapper(self, tmp_path, sample_event):
        log_file = tmp_path / "events.jsonl"
        writer = JsonlEventWriter(log_file)
        writer.handle(sample_event)
        writer.handle(sample_event)

        content = log_file.read_text()
        assert not content.strip().startswith("[")
        assert not content.strip().endswith("]")
        for line in content.strip().splitlines():
            assert not line.rstrip().endswith(",")
