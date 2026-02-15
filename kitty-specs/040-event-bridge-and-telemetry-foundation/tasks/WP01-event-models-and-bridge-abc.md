---
work_package_id: "WP01"
subtasks:
  - "T001"
  - "T002"
  - "T003"
  - "T004"
  - "T005"
  - "T006"
title: "Event Models & Bridge ABC"
phase: "Phase 1 - Foundation"
lane: "planned"
assignee: ""
agent: ""
shell_pid: ""
review_status: ""
reviewed_by: ""
dependencies: []
history:
  - timestamp: "2026-02-15T00:24:27Z"
    lane: "planned"
    agent: "system"
    shell_pid: ""
    action: "Prompt generated via /spec-kitty.tasks"
---

# Work Package Prompt: WP01 – Event Models & Bridge ABC

## ⚠️ IMPORTANT: Review Feedback Status

**Read this first if you are implementing this task!**

- **Has review feedback?**: Check the `review_status` field above. If it says `has_feedback`, scroll to the **Review Feedback** section immediately.
- **You must address all feedback** before your work is complete.
- **Mark as acknowledged**: When you understand the feedback, update `review_status: acknowledged`.

---

## Review Feedback

> **Populated by `/spec-kitty.review`** – Reviewers add detailed feedback here when work needs changes.

*[This section is empty initially.]*

---

## Agent Profile

**Python Pedro** — ATDD+TDD (Directives 016 & 017). Follow RED→GREEN→REFACTOR cycle strictly.

## Objectives & Success Criteria

- All event Pydantic models (BaseEvent, LaneTransitionEvent, ValidationEvent, ExecutionEvent) exist, are frozen, and serialize to JSON with correct type discriminators.
- EventBridge ABC, NullEventBridge, and CompositeEventBridge are implemented.
- NullEventBridge silently discards all events (no-op).
- CompositeEventBridge fans out events to all registered listeners with per-listener error isolation.
- **Tests written FIRST** and achieve ≥80% coverage on new code.
- `ruff check` passes clean on all new files.

## Context & Constraints

- **Spec**: `kitty-specs/040-event-bridge-and-telemetry-foundation/spec.md` — FR-001 through FR-004, FR-007, FR-008
- **Plan**: `kitty-specs/040-event-bridge-and-telemetry-foundation/plan.md` — Architecture section, Event Models section
- **Data Model**: `kitty-specs/040-event-bridge-and-telemetry-foundation/data-model.md` — Entity definitions
- **Pydantic**: Already a dependency (pydantic >=2.0). Use `BaseModel` with `ConfigDict(frozen=True)`.
- **No new dependencies**: Only use stdlib + pydantic.
- **Glossary alignment**: Use `tool_id` (not `agent_id`) for CLI tool references, `agent_profile_id` for Doctrine agent identities. See `glossary/README.md` naming decision.

## Implementation Command

```bash
spec-kitty implement WP01
```

No dependencies — branches from target branch directly.

## Subtasks & Detailed Guidance

### Subtask T001 — RED: Write Acceptance Tests for Event Models

**Purpose**: Define the acceptance criteria for event models as executable tests. These MUST fail initially.

**TDD Phase**: RED

**Steps**:
1. Create directory `tests/specify_cli/core/test_events/` with `__init__.py`
2. Create `tests/specify_cli/core/test_events/test_models.py`
3. Write tests for:

**Test cases** (use `@pytest.mark.parametrize` where appropriate):

```python
# test_base_event_has_timestamp_and_type
# - Create a LaneTransitionEvent with all required fields
# - Assert timestamp is a datetime
# - Assert type is "lane_transition"

# test_lane_transition_event_fields
# - Create with: work_package_id="WP01", from_lane="planned", to_lane="doing"
# - Assert all required fields present
# - Assert optional fields (tool_id, agent_profile_id, commit_sha) default to None

# test_validation_event_fields
# - Create with: validation_type="pre_implement", status="pass"
# - Assert directive_refs defaults to empty list
# - Assert duration_ms defaults to 0

# test_execution_event_fields
# - Create with: work_package_id="WP01", tool_id="claude", model="sonnet"
# - Assert optional fields default correctly (cost_usd=0.0, success=True, error=None)

# test_event_is_frozen
# - Create a LaneTransitionEvent
# - Attempt to set a field (e.g., event.from_lane = "other")
# - Assert raises ValidationError (pydantic frozen model)

# test_event_json_serialization_roundtrip
# - Create a LaneTransitionEvent with all fields
# - Call model_dump_json() → get JSON string
# - Parse JSON string → verify all fields match
# - Verify "type": "lane_transition" is in JSON

# test_event_type_discriminator
# - LaneTransitionEvent().type == "lane_transition"
# - ValidationEvent().type == "validation"
# - ExecutionEvent().type == "execution"
```

**Files**:
- `tests/specify_cli/core/test_events/__init__.py` (new, empty)
- `tests/specify_cli/core/test_events/test_models.py` (new, ~120 lines)

**Validation**: `pytest tests/specify_cli/core/test_events/test_models.py` — all tests FAIL (ImportError — modules don't exist yet).

---

### Subtask T002 — RED: Write Acceptance Tests for Bridge

**Purpose**: Define acceptance criteria for EventBridge, NullEventBridge, and CompositeEventBridge as executable tests.

**TDD Phase**: RED

**Steps**:
1. Create `tests/specify_cli/core/test_events/test_bridge.py`
2. Write tests for:

**Test cases**:

```python
# test_null_event_bridge_discards_lane_transition
# - Create NullEventBridge
# - Call emit_lane_transition(event) — no error, no side effect
# - Verify returns None

# test_null_event_bridge_discards_validation_event
# - Same pattern for emit_validation_event

# test_null_event_bridge_discards_execution_event
# - Same pattern for emit_execution_event

# test_composite_bridge_fans_out_to_all_listeners
# - Create CompositeEventBridge with 2 mock listeners
# - Emit a LaneTransitionEvent
# - Assert both listeners were called with the event

# test_composite_bridge_isolates_listener_errors
# - Create CompositeEventBridge with 3 listeners
# - Second listener raises RuntimeError
# - Emit event
# - Assert first and third listeners still received the event
# - Assert warning was logged (use caplog fixture)

# test_composite_bridge_register_adds_listener
# - Create empty CompositeEventBridge
# - Register a listener
# - Emit event
# - Assert listener was called

# test_composite_bridge_no_listeners_is_silent
# - Create CompositeEventBridge with empty listener list
# - Emit event — no error
```

**Files**:
- `tests/specify_cli/core/test_events/test_bridge.py` (new, ~100 lines)

**Validation**: `pytest tests/specify_cli/core/test_events/test_bridge.py` — all tests FAIL (ImportError).

---

### Subtask T003 — GREEN: Create `core/events/__init__.py`

**Purpose**: Create the package with public API exports.

**TDD Phase**: GREEN (start making tests pass)

**Steps**:
1. Create directory `src/specify_cli/core/events/`
2. Create `src/specify_cli/core/events/__init__.py`:

```python
"""Structured event emission for Spec Kitty lifecycle."""

from .bridge import CompositeEventBridge, EventBridge, NullEventBridge
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
]
```

**Files**:
- `src/specify_cli/core/events/__init__.py` (new, ~20 lines)

---

### Subtask T004 — GREEN: Create Event Models

**Purpose**: Implement Pydantic frozen models for all event types. This should make T001 tests pass.

**TDD Phase**: GREEN

**Steps**:
1. Create `src/specify_cli/core/events/models.py`
2. Implement:

```python
from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict


class BaseEvent(BaseModel):
    """Base for all lifecycle events."""
    model_config = ConfigDict(frozen=True)

    timestamp: datetime
    type: str  # Overridden by subclass Literal


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
```

**Files**:
- `src/specify_cli/core/events/models.py` (new, ~50 lines)

**Validation**: `pytest tests/specify_cli/core/test_events/test_models.py` — should now PASS.

---

### Subtask T005 — GREEN: Create EventBridge ABC & Implementations

**Purpose**: Implement the bridge abstraction and concrete implementations. This should make T002 tests pass.

**TDD Phase**: GREEN

**Steps**:
1. Create `src/specify_cli/core/events/bridge.py`
2. Implement:

```python
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
```

**Files**:
- `src/specify_cli/core/events/bridge.py` (new, ~65 lines)

**Validation**: `pytest tests/specify_cli/core/test_events/test_bridge.py` — should now PASS.

---

### Subtask T006 — REFACTOR: Validate & Clean Up

**Purpose**: Run full quality checks on WP01 deliverables.

**TDD Phase**: REFACTOR

**Steps**:
1. Run all WP01 tests:
   ```bash
   pytest tests/specify_cli/core/test_events/ -v --tb=short
   ```
2. Run linter:
   ```bash
   ruff check src/specify_cli/core/events/ tests/specify_cli/core/test_events/
   ```
3. Fix any issues found.
4. Verify no existing tests broken:
   ```bash
   pytest tests/ -x --ignore=tests/specify_cli/core/test_events/ -q
   ```
5. Commit with message: `feat(events): add event models and EventBridge ABC (040-WP01)`

**Validation**: All checks pass clean. No regressions.

---

## Risks & Mitigations

- **Pydantic version**: spec-kitty requires pydantic >=2.0 — verify before starting.
- **`core/` directory**: May not have an `__init__.py`. Create if needed.
- **Import conflicts**: Existing `events/` and `spec_kitty_events/` directories exist at the package root. Our new code is at `core/events/` — different path, no conflict.

## Review Guidance

- Verify all event models are frozen (try mutating in test).
- Verify CompositeEventBridge error isolation — one bad listener must not block others.
- Verify `model_dump_json()` produces valid JSON with `type` discriminator.
- Check that `__init__.py` exports match the public API surface.

## Activity Log

- 2026-02-15T00:24:27Z – system – lane=planned – Prompt created.
