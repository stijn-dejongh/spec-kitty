"""Tests for event models — RED phase (ATDD).

These tests define acceptance criteria for event models.
They MUST fail initially (ImportError) until models are implemented.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from specify_cli.core.events import (
    ExecutionEvent,
    LaneTransitionEvent,
    ValidationEvent,
)


@pytest.fixture
def now() -> datetime:
    return datetime(2026, 2, 15, 12, 0, 0, tzinfo=timezone.utc)


class TestLaneTransitionEvent:
    def test_has_timestamp_and_type(self, now: datetime) -> None:
        event = LaneTransitionEvent(
            timestamp=now,
            work_package_id="WP01",
            from_lane="planned",
            to_lane="doing",
        )
        assert isinstance(event.timestamp, datetime)
        assert event.type == "lane_transition"

    def test_required_fields(self, now: datetime) -> None:
        event = LaneTransitionEvent(
            timestamp=now,
            work_package_id="WP01",
            from_lane="planned",
            to_lane="doing",
        )
        assert event.work_package_id == "WP01"
        assert event.from_lane == "planned"
        assert event.to_lane == "doing"

    def test_optional_fields_default_to_none(self, now: datetime) -> None:
        event = LaneTransitionEvent(
            timestamp=now,
            work_package_id="WP01",
            from_lane="planned",
            to_lane="doing",
        )
        assert event.tool_id is None
        assert event.agent_profile_id is None
        assert event.commit_sha is None

    def test_optional_fields_can_be_set(self, now: datetime) -> None:
        event = LaneTransitionEvent(
            timestamp=now,
            work_package_id="WP01",
            from_lane="planned",
            to_lane="doing",
            tool_id="claude",
            agent_profile_id="python-pedro",
            commit_sha="abc123",
        )
        assert event.tool_id == "claude"
        assert event.agent_profile_id == "python-pedro"
        assert event.commit_sha == "abc123"

    def test_is_frozen(self, now: datetime) -> None:
        event = LaneTransitionEvent(
            timestamp=now,
            work_package_id="WP01",
            from_lane="planned",
            to_lane="doing",
        )
        with pytest.raises(ValidationError):
            event.from_lane = "other"  # type: ignore[misc]

    def test_json_serialization_roundtrip(self, now: datetime) -> None:
        event = LaneTransitionEvent(
            timestamp=now,
            work_package_id="WP01",
            from_lane="planned",
            to_lane="doing",
            tool_id="claude",
        )
        json_str = event.model_dump_json()
        parsed = json.loads(json_str)
        assert parsed["type"] == "lane_transition"
        assert parsed["work_package_id"] == "WP01"
        assert parsed["from_lane"] == "planned"
        assert parsed["to_lane"] == "doing"
        assert parsed["tool_id"] == "claude"
        assert "timestamp" in parsed


class TestValidationEvent:
    def test_required_fields(self, now: datetime) -> None:
        event = ValidationEvent(
            timestamp=now,
            validation_type="pre_implement",
            status="pass",
        )
        assert event.type == "validation"
        assert event.validation_type == "pre_implement"
        assert event.status == "pass"

    def test_defaults(self, now: datetime) -> None:
        event = ValidationEvent(
            timestamp=now,
            validation_type="pre_implement",
            status="pass",
        )
        assert event.directive_refs == []
        assert event.duration_ms == 0

    def test_directive_refs_can_be_set(self, now: datetime) -> None:
        event = ValidationEvent(
            timestamp=now,
            validation_type="pre_review",
            status="warn",
            directive_refs=[17, 23],
            duration_ms=150,
        )
        assert event.directive_refs == [17, 23]
        assert event.duration_ms == 150


class TestExecutionEvent:
    def test_required_fields(self, now: datetime) -> None:
        event = ExecutionEvent(
            timestamp=now,
            work_package_id="WP01",
            tool_id="claude",
            model="sonnet-4",
        )
        assert event.type == "execution"
        assert event.work_package_id == "WP01"
        assert event.tool_id == "claude"
        assert event.model == "sonnet-4"

    def test_defaults(self, now: datetime) -> None:
        event = ExecutionEvent(
            timestamp=now,
            work_package_id="WP01",
            tool_id="claude",
            model="sonnet-4",
        )
        assert event.input_tokens == 0
        assert event.output_tokens == 0
        assert event.cost_usd == 0.0
        assert event.duration_ms == 0
        assert event.success is True
        assert event.error is None
        assert event.agent_profile_id is None
        assert event.agent_role is None

    def test_all_fields(self, now: datetime) -> None:
        event = ExecutionEvent(
            timestamp=now,
            work_package_id="WP02",
            tool_id="opencode",
            agent_profile_id="python-pedro",
            agent_role="implementer",
            model="gpt-4",
            input_tokens=1000,
            output_tokens=500,
            cost_usd=0.05,
            duration_ms=3000,
            success=False,
            error="Timeout",
        )
        assert event.agent_profile_id == "python-pedro"
        assert event.agent_role == "implementer"
        assert event.cost_usd == 0.05
        assert event.success is False
        assert event.error == "Timeout"


@pytest.mark.parametrize(
    "event_cls,event_type,kwargs",
    [
        (LaneTransitionEvent, "lane_transition", {"work_package_id": "WP01", "from_lane": "planned", "to_lane": "doing"}),
        (ValidationEvent, "validation", {"validation_type": "pre_plan", "status": "pass"}),
        (ExecutionEvent, "execution", {"work_package_id": "WP01", "tool_id": "claude", "model": "sonnet"}),
    ],
)
def test_type_discriminator(event_cls, event_type, kwargs, now: datetime) -> None:
    event = event_cls(timestamp=now, **kwargs)
    assert event.type == event_type
    parsed = json.loads(event.model_dump_json())
    assert parsed["type"] == event_type
