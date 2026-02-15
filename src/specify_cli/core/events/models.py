"""Event models for Spec Kitty lifecycle events.

Pydantic frozen models for structured event emission.
All events are immutable and serialize to JSON via model_dump_json().
"""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict


class BaseEvent(BaseModel):
    """Base for all lifecycle events."""

    model_config = ConfigDict(frozen=True)

    timestamp: datetime
    type: str


class LaneTransitionEvent(BaseEvent):
    """Records a work package moving between kanban lanes."""

    type: Literal["lane_transition"] = "lane_transition"
    work_package_id: str
    from_lane: str
    to_lane: str
    tool_id: str | None = None
    agent_profile_id: str | None = None
    commit_sha: str | None = None


class ValidationEvent(BaseEvent):
    """Records a governance validation check result."""

    type: Literal["validation"] = "validation"
    validation_type: str
    status: str
    directive_refs: list[int] = []
    duration_ms: int = 0


class ExecutionEvent(BaseEvent):
    """Records a tool execution."""

    type: Literal["execution"] = "execution"
    work_package_id: str
    tool_id: str
    agent_profile_id: str | None = None
    agent_role: str | None = None
    model: str
    input_tokens: int = 0
    output_tokens: int = 0
    cost_usd: float = 0.0
    duration_ms: int = 0
    success: bool = True
    error: str | None = None
