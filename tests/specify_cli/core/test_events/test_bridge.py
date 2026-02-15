"""Tests for EventBridge implementations — RED phase (ATDD).

These tests define acceptance criteria for NullEventBridge and CompositeEventBridge.
They MUST fail initially (ImportError) until bridge is implemented.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from unittest.mock import MagicMock

import pytest

from specify_cli.core.events import (
    CompositeEventBridge,
    LaneTransitionEvent,
    NullEventBridge,
    ValidationEvent,
)


@pytest.fixture
def sample_lane_event() -> LaneTransitionEvent:
    return LaneTransitionEvent(
        timestamp=datetime(2026, 2, 15, 12, 0, 0, tzinfo=timezone.utc),
        work_package_id="WP01",
        from_lane="planned",
        to_lane="doing",
    )


@pytest.fixture
def sample_validation_event() -> ValidationEvent:
    return ValidationEvent(
        timestamp=datetime(2026, 2, 15, 12, 0, 0, tzinfo=timezone.utc),
        validation_type="pre_implement",
        status="pass",
    )


class TestNullEventBridge:
    def test_discards_lane_transition(self, sample_lane_event: LaneTransitionEvent) -> None:
        bridge = NullEventBridge()
        result = bridge.emit_lane_transition(sample_lane_event)
        assert result is None

    def test_discards_validation_event(self, sample_validation_event: ValidationEvent) -> None:
        bridge = NullEventBridge()
        result = bridge.emit_validation_event(sample_validation_event)
        assert result is None

    def test_discards_execution_event(self) -> None:
        from specify_cli.core.events import ExecutionEvent

        bridge = NullEventBridge()
        event = ExecutionEvent(
            timestamp=datetime(2026, 2, 15, tzinfo=timezone.utc),
            work_package_id="WP01",
            tool_id="claude",
            model="sonnet",
        )
        result = bridge.emit_execution_event(event)
        assert result is None


class TestCompositeEventBridge:
    def test_fans_out_to_all_listeners(self, sample_lane_event: LaneTransitionEvent) -> None:
        listener1 = MagicMock()
        listener2 = MagicMock()
        bridge = CompositeEventBridge(listeners=[listener1, listener2])
        bridge.emit_lane_transition(sample_lane_event)
        listener1.assert_called_once_with(sample_lane_event)
        listener2.assert_called_once_with(sample_lane_event)

    def test_isolates_listener_errors(
        self, sample_lane_event: LaneTransitionEvent, caplog: pytest.LogCaptureFixture
    ) -> None:
        listener1 = MagicMock()
        listener2 = MagicMock(side_effect=RuntimeError("boom"))
        listener3 = MagicMock()
        bridge = CompositeEventBridge(listeners=[listener1, listener2, listener3])

        with caplog.at_level(logging.WARNING):
            bridge.emit_lane_transition(sample_lane_event)

        listener1.assert_called_once_with(sample_lane_event)
        listener3.assert_called_once_with(sample_lane_event)
        assert "failed" in caplog.text.lower()

    def test_register_adds_listener(self, sample_lane_event: LaneTransitionEvent) -> None:
        bridge = CompositeEventBridge()
        listener = MagicMock()
        bridge.register(listener)
        bridge.emit_lane_transition(sample_lane_event)
        listener.assert_called_once_with(sample_lane_event)

    def test_no_listeners_is_silent(self, sample_lane_event: LaneTransitionEvent) -> None:
        bridge = CompositeEventBridge()
        bridge.emit_lane_transition(sample_lane_event)  # No error

    def test_validation_event_fans_out(self, sample_validation_event: ValidationEvent) -> None:
        listener = MagicMock()
        bridge = CompositeEventBridge(listeners=[listener])
        bridge.emit_validation_event(sample_validation_event)
        listener.assert_called_once_with(sample_validation_event)

    def test_execution_event_fans_out(self) -> None:
        from specify_cli.core.events import ExecutionEvent

        listener = MagicMock()
        bridge = CompositeEventBridge(listeners=[listener])
        event = ExecutionEvent(
            timestamp=datetime(2026, 2, 15, tzinfo=timezone.utc),
            work_package_id="WP01",
            tool_id="claude",
            model="sonnet",
        )
        bridge.emit_execution_event(event)
        listener.assert_called_once_with(event)
