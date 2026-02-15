---
work_package_id: WP03
title: Orchestrator & CLI Wiring
lane: "done"
dependencies:
- WP01
subtasks:
- T013
- T014
- T015
- T016
- T017
phase: Phase 2 - Integration
assignee: ''
agent: ''
shell_pid: ''
review_status: "approved"
reviewed_by: "Stijn Dejongh"
history:
- timestamp: '2026-02-15T00:24:27Z'
  lane: planned
  agent: system
  shell_pid: ''
  action: Prompt generated via /spec-kitty.tasks
---

# Work Package Prompt: WP03 – Orchestrator & CLI Wiring

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

- `ExecutionContext` dataclass has an `event_bridge` field defaulting to `NullEventBridge`.
- Orchestrator entry point loads the event bridge from config.
- `move_task` CLI command emits `LaneTransitionEvent` after successful lane change.
- All existing spec-kitty tests pass without modification (SC-001).
- NullEventBridge adds negligible overhead to workflow commands (SC-003).
- **Acceptance test written FIRST**: integration test verifying end-to-end lane transition → JSONL event.

## Context & Constraints

- **Spec**: FR-009 (orchestrator accepts optional EventBridge), User Story 1 (lane transitions recorded), User Story 3 (existing workflows unaffected)
- **Plan**: Wiring Strategy section, Integration Points section
- **WP01 & WP02 must be complete**: Models, bridge, factory, and JSONL writer must exist.
- **Backward compatibility is a HARD constraint**: Default to NullEventBridge everywhere.
- **Minimal modifications**: Only touch executor.py, integration.py, and tasks.py.

## Implementation Command

```bash
spec-kitty implement WP03 --base WP02
```

Depends on WP02 — branches from WP02's branch.

## Subtasks & Detailed Guidance

### Subtask T013 — RED: Write Acceptance/Integration Test

**Purpose**: Define the end-to-end acceptance criteria as an executable test. MUST fail initially.

**TDD Phase**: RED

**Steps**:
1. Create `tests/specify_cli/core/test_events/test_integration.py`
2. Write tests:

```python
import json
from datetime import datetime, timezone
from pathlib import Path

import pytest
import yaml


# test_lane_transition_emits_event_to_jsonl(tmp_path)
# Setup:
# - Create .kittify/config.yaml with telemetry enabled
# - Create a minimal WP file in tasks/ with lane: "planned"
# - Load event bridge from config
# - Simulate a lane transition (planned → doing)
# - Emit LaneTransitionEvent through the bridge
# Assert:
# - .kittify/events.jsonl exists
# - Contains exactly 1 line
# - Parsed JSON has type="lane_transition", work_package_id, from_lane="planned", to_lane="doing"
# - Has valid ISO 8601 timestamp

# test_no_event_file_when_telemetry_disabled(tmp_path)
# Setup:
# - Create .kittify/config.yaml with telemetry.enabled: false
# - Load event bridge from config
# - Simulate lane transition, emit event
# Assert:
# - .kittify/events.jsonl does NOT exist
# - No error raised

# test_no_event_file_when_no_config(tmp_path)
# Setup:
# - tmp_path with no .kittify/ at all
# - Load event bridge (should get NullEventBridge)
# - Emit event
# Assert:
# - No events.jsonl file created anywhere in tmp_path

# test_multiple_transitions_produce_ordered_events(tmp_path)
# Setup:
# - Enable telemetry
# - Emit 3 lane transitions: planned→doing, doing→for_review, for_review→done
# Assert:
# - events.jsonl has exactly 3 lines
# - Lines are in order: planned→doing, doing→for_review, for_review→done
# - All timestamps are valid
```

**Files**:
- `tests/specify_cli/core/test_events/test_integration.py` (new, ~100 lines)

**Validation**: `pytest tests/specify_cli/core/test_events/test_integration.py` — tests FAIL (import or assertion errors).

---

### Subtask T014 — GREEN: Add `event_bridge` to ExecutionContext

**Purpose**: Add the EventBridge field to the orchestrator's execution context.

**TDD Phase**: GREEN

**Steps**:
1. Open `src/specify_cli/orchestrator/executor.py`
2. Add imports at top:
   ```python
   from specify_cli.core.events import EventBridge, NullEventBridge
   ```
3. Add field to `ExecutionContext` dataclass:
   ```python
   event_bridge: EventBridge = field(default_factory=NullEventBridge)
   ```
4. **Do not change any other logic** — this is purely additive.

**Files**:
- `src/specify_cli/orchestrator/executor.py` (modified — 2-3 lines added)

**Validation**: Existing orchestrator tests still pass.

**Edge Cases**:
- If `ExecutionContext` uses `__slots__`, ensure `event_bridge` is added to slots.
- If it's a `NamedTuple` instead of dataclass, adjust pattern accordingly.

---

### Subtask T015 — GREEN: Wire Factory in Orchestrator Entry Point

**Purpose**: Load the event bridge at orchestration start and pass to ExecutionContext.

**TDD Phase**: GREEN

**Steps**:
1. Open `src/specify_cli/orchestrator/integration.py`
2. Add import:
   ```python
   from specify_cli.core.events import load_event_bridge
   ```
3. In the function that constructs `ExecutionContext` (likely `run_orchestration_loop` or `start_orchestration_async`):
   - Before constructing context: `event_bridge = load_event_bridge(repo_root)`
   - Pass to context: `ExecutionContext(..., event_bridge=event_bridge)`
4. **Minimal change** — only add the bridge loading and passing.

**Files**:
- `src/specify_cli/orchestrator/integration.py` (modified — 3-5 lines added)

**Validation**: Existing orchestrator tests still pass. With telemetry disabled (default), behavior is identical.

---

### Subtask T016 — GREEN: Emit LaneTransitionEvent from `move_task`

**Purpose**: After a successful lane change in the CLI, emit a LaneTransitionEvent. This should make the integration test pass.

**TDD Phase**: GREEN

**Steps**:
1. Open `src/specify_cli/cli/commands/agent/tasks.py`
2. Add imports:
   ```python
   from datetime import datetime, timezone
   from specify_cli.core.events import load_event_bridge, LaneTransitionEvent
   ```
3. Find the `move_task` function. After the lane change succeeds (after `set_scalar` or equivalent updates the frontmatter):
   ```python
   # Emit lane transition event
   try:
       event_bridge = load_event_bridge(repo_root)
       event = LaneTransitionEvent(
           timestamp=datetime.now(timezone.utc),
           work_package_id=task_id,
           from_lane=old_lane,
           to_lane=target_lane,
           tool_id=None,  # Could be enhanced later
       )
       event_bridge.emit_lane_transition(event)
   except Exception:
       pass  # Event emission must never crash the workflow
   ```
4. Wrap in try/except to ensure event emission never crashes the workflow (spec requirement).

**Files**:
- `src/specify_cli/cli/commands/agent/tasks.py` (modified — ~10 lines added)

**Validation**: 
- `pytest tests/specify_cli/core/test_events/test_integration.py` — should now PASS
- All existing tests still pass

**Edge Cases**:
- `repo_root` must be available in `move_task` scope — check how it's determined (likely from git rev-parse or passed as parameter)
- If `old_lane` variable doesn't exist, capture it before the lane change: `old_lane = current_lane` before calling set_scalar

---

### Subtask T017 — REFACTOR: Full Suite Validation

**Purpose**: Run complete test suite, verify backward compatibility, clean up.

**TDD Phase**: REFACTOR

**Steps**:
1. Run ALL event tests:
   ```bash
   pytest tests/specify_cli/core/test_events/ tests/specify_cli/telemetry/ -v --tb=short
   ```
2. Run FULL test suite (backward compatibility — SC-001):
   ```bash
   pytest tests/ -x -q
   ```
3. Run linter on all modified files:
   ```bash
   ruff check src/specify_cli/orchestrator/executor.py src/specify_cli/orchestrator/integration.py src/specify_cli/cli/commands/agent/tasks.py
   ```
4. Verify no new files created in .kittify/ when telemetry disabled:
   ```bash
   # Run any workflow command, verify no events.jsonl
   ```
5. Commit: `feat(events): wire EventBridge into orchestrator and CLI (040-WP03)`

**Validation**: All checks pass. SC-001 (backward compatibility) confirmed.

---

## Risks & Mitigations

- **Breaking existing tests**: NullEventBridge is default — no existing code path changes behavior.
- **Import cycle**: `core.events` imports nothing from `orchestrator` or `cli` — no cycle possible.
- **Performance**: NullEventBridge methods are empty `pass` statements — negligible overhead.
- **move_task scope**: If `repo_root` isn't available, derive from `git rev-parse --show-toplevel` or function parameter.

## Review Guidance

- **Critical check**: Run the full existing test suite. Any failure is a blocker.
- Verify NullEventBridge is used when no telemetry config — no new files should appear.
- Verify the try/except in move_task prevents event emission from crashing the workflow.
- Check that event emission happens AFTER the lane change succeeds (not before).

## Activity Log

- 2026-02-15T00:24:27Z – system – lane=planned – Prompt created.
- 2026-02-15T01:00:59Z – unknown – lane=done – Moved to done
