"""EventBridge abstraction and implementations.

EventBridge ABC defines the contract for structured event emission.
NullEventBridge silently discards events (default).
CompositeEventBridge fans out to registered listeners with error isolation.
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any

from .models import ExecutionEvent, LaneTransitionEvent, ValidationEvent

logger = logging.getLogger(__name__)


class EventBridge(ABC):
    """Abstract base for structured event emission."""

    @abstractmethod
    def emit_lane_transition(self, event: LaneTransitionEvent) -> None: ...

    @abstractmethod
    def emit_validation_event(self, event: ValidationEvent) -> None: ...

    @abstractmethod
    def emit_execution_event(self, event: ExecutionEvent) -> None: ...


class NullEventBridge(EventBridge):
    """Default: silently discards all events."""

    def emit_lane_transition(self, event: LaneTransitionEvent) -> None:
        pass

    def emit_validation_event(self, event: ValidationEvent) -> None:
        pass

    def emit_execution_event(self, event: ExecutionEvent) -> None:
        pass


class CompositeEventBridge(EventBridge):
    """Fan-out to registered listeners with error isolation."""

    def __init__(self, listeners: list[Callable] | None = None) -> None:
        self._listeners: list[Callable] = list(listeners) if listeners else []

    def register(self, listener: Callable) -> None:
        """Add a listener to receive events."""
        self._listeners.append(listener)

    def _dispatch(self, event: Any) -> None:
        for listener in self._listeners:
            try:
                listener(event)
            except Exception:
                logger.warning(
                    "Listener %s failed for event %s",
                    listener,
                    type(event).__name__,
                    exc_info=True,
                )

    def emit_lane_transition(self, event: LaneTransitionEvent) -> None:
        self._dispatch(event)

    def emit_validation_event(self, event: ValidationEvent) -> None:
        self._dispatch(event)

    def emit_execution_event(self, event: ExecutionEvent) -> None:
        self._dispatch(event)
