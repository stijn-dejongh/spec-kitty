"""Structured event emission for Spec Kitty lifecycle."""

from .bridge import CompositeEventBridge, EventBridge, NullEventBridge
from .factory import load_event_bridge
from .models import (
    BaseEvent,
    ExecutionEvent,
    LaneTransitionEvent,
    ValidationEvent,
)

__all__ = [
    "BaseEvent",
    "CompositeEventBridge",
    "EventBridge",
    "ExecutionEvent",
    "LaneTransitionEvent",
    "NullEventBridge",
    "ValidationEvent",
    "load_event_bridge",
]
