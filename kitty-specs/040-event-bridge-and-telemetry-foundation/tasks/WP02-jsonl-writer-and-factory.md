---
work_package_id: "WP02"
subtasks:
  - "T007"
  - "T008"
  - "T009"
  - "T010"
  - "T011"
  - "T012"
title: "JSONL Writer & Factory"
phase: "Phase 1 - Foundation"
lane: "planned"
assignee: ""
agent: ""
shell_pid: ""
review_status: ""
reviewed_by: ""
dependencies: ["WP01"]
history:
  - timestamp: "2026-02-15T00:24:27Z"
    lane: "planned"
    agent: "system"
    shell_pid: ""
    action: "Prompt generated via /spec-kitty.tasks"
---

# Work Package Prompt: WP02 – JSONL Writer & Factory

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

- JsonlEventWriter appends Pydantic events as one JSON object per line to a configurable file path.
- JsonlEventWriter handles write failures gracefully (logs warning, does not crash workflow).
- `load_event_bridge(repo_root)` factory reads `.kittify/config.yaml` and returns appropriate EventBridge.
- Factory returns NullEventBridge when telemetry is disabled, config is missing, or config is malformed.
- Factory returns CompositeEventBridge with JsonlEventWriter when `telemetry.enabled=true`.
- **Tests written FIRST** and achieve ≥80% coverage.
- `ruff check` passes clean.

## Context & Constraints

- **Spec**: FR-005, FR-006, FR-009, FR-010
- **Plan**: JSONL Writer section, Config Schema Extension section, Factory Function section
- **WP01 must be complete**: Event models and bridge ABC must exist.
- **Config pattern**: Follow existing `yaml.safe_load()` pattern from `.kittify/config.yaml`.
- **No new dependencies**: Only stdlib + pydantic + PyYAML (already a dependency).

## Implementation Command

```bash
spec-kitty implement WP02 --base WP01
```

Depends on WP01 — branches from WP01's branch.

## Subtasks & Detailed Guidance

### Subtask T007 — RED: Write Acceptance Tests for JSONL Writer

**Purpose**: Define acceptance criteria for JsonlEventWriter as executable tests. MUST fail initially.

**TDD Phase**: RED

**Steps**:
1. Create directory `tests/specify_cli/telemetry/` with `__init__.py`
2. Create `tests/specify_cli/telemetry/test_jsonl_writer.py`
3. Write tests:

```python
import json
from datetime import datetime, timezone

import pytest

# These imports will fail initially (RED phase)
from specify_cli.telemetry.jsonl_writer import JsonlEventWriter
from specify_cli.core.events import LaneTransitionEvent


@pytest.fixture
def sample_event():
    return LaneTransitionEvent(
        timestamp=datetime(2026, 2, 15, tzinfo=timezone.utc),
        work_package_id="WP01",
        from_lane="planned",
        to_lane="doing",
    )


# test_writes_single_event_as_json_line
# - Create writer with tmp_path / "events.jsonl"
# - Call handle(sample_event)
# - Read file, verify exactly 1 line
# - Parse line as JSON, verify all fields present

# test_appends_multiple_events
# - Write 3 events
# - Read file, verify 3 lines
# - Each line is valid JSON

# test_each_line_is_valid_json
# - Write 5 events with different types (lane_transition, validation, execution)
# - Read file, json.loads() each line — no exceptions
# - Each line has "type" and "timestamp" fields

# test_graceful_failure_on_unwritable_path(caplog)
# - Create writer with path "/nonexistent/dir/events.jsonl"
# - Call handle(sample_event) — no exception raised
# - Assert warning logged containing "Failed to write event"

# test_graceful_failure_on_read_only_directory(tmp_path, caplog)
# - Make tmp_path read-only (os.chmod 0o444)
# - Create writer pointing to file in that dir
# - Call handle(sample_event) — no exception
# - Assert warning logged
# - Restore permissions in finally block

# test_jsonl_no_trailing_comma_or_array_wrapper
# - Write 2 events
# - Read raw file content
# - Assert does not start with "[" or end with "]"
# - Assert no trailing comma on any line
```

**Files**:
- `tests/specify_cli/telemetry/__init__.py` (new, empty)
- `tests/specify_cli/telemetry/test_jsonl_writer.py` (new, ~100 lines)

**Validation**: `pytest tests/specify_cli/telemetry/test_jsonl_writer.py` — FAIL (ImportError).

---

### Subtask T008 — RED: Write Acceptance Tests for Factory

**Purpose**: Define acceptance criteria for `load_event_bridge()` as executable tests. MUST fail initially.

**TDD Phase**: RED

**Steps**:
1. Create `tests/specify_cli/core/test_events/test_factory.py`
2. Write tests:

```python
# test_returns_null_bridge_when_no_config_file(tmp_path)
# - tmp_path has no .kittify/config.yaml
# - Call load_event_bridge(tmp_path)
# - Assert isinstance(result, NullEventBridge)

# test_returns_null_bridge_when_telemetry_disabled(tmp_path)
# - Create .kittify/config.yaml with telemetry.enabled: false
# - Call load_event_bridge(tmp_path)
# - Assert isinstance(result, NullEventBridge)

# test_returns_null_bridge_when_telemetry_key_missing(tmp_path)
# - Create .kittify/config.yaml with only agents section (no telemetry key)
# - Call load_event_bridge(tmp_path)
# - Assert isinstance(result, NullEventBridge)

# test_returns_composite_bridge_when_enabled(tmp_path)
# - Create .kittify/config.yaml with telemetry.enabled: true, log_path: "events.jsonl"
# - Call load_event_bridge(tmp_path)
# - Assert isinstance(result, CompositeEventBridge)

# test_returns_null_bridge_on_malformed_yaml(tmp_path)
# - Create .kittify/config.yaml with invalid YAML content (e.g., "{{{{")
# - Call load_event_bridge(tmp_path)
# - Assert isinstance(result, NullEventBridge)

# test_factory_resolves_relative_log_path(tmp_path)
# - Create config with telemetry.enabled: true, log_path: ".kittify/events.jsonl"
# - Call load_event_bridge(tmp_path)
# - Emit event through returned bridge
# - Assert (tmp_path / ".kittify" / "events.jsonl").exists()

# test_default_log_path_used_when_not_specified(tmp_path)
# - Create config with telemetry.enabled: true (no log_path)
# - Call load_event_bridge(tmp_path)
# - Assert isinstance(result, CompositeEventBridge) — should use default path
```

**Files**:
- `tests/specify_cli/core/test_events/test_factory.py` (new, ~100 lines)

**Validation**: `pytest tests/specify_cli/core/test_events/test_factory.py` — FAIL (ImportError).

---

### Subtask T009 — GREEN: Create `telemetry/__init__.py`

**Purpose**: Create the telemetry package with public exports.

**TDD Phase**: GREEN

**Steps**:
1. Create directory `src/specify_cli/telemetry/`
2. Create `src/specify_cli/telemetry/__init__.py`:

```python
"""Telemetry consumers for Spec Kitty event system."""

from .jsonl_writer import JsonlEventWriter

__all__ = ["JsonlEventWriter"]
```

**Files**:
- `src/specify_cli/telemetry/__init__.py` (new, ~5 lines)

---

### Subtask T010 — GREEN: Create JsonlEventWriter

**Purpose**: Implement the JSONL file writer. Should make T007 tests pass.

**TDD Phase**: GREEN

**Steps**:
1. Create `src/specify_cli/telemetry/jsonl_writer.py`:

```python
from __future__ import annotations

import logging
from pathlib import Path

from specify_cli.core.events.models import BaseEvent

logger = logging.getLogger(__name__)


class JsonlEventWriter:
    """Appends Pydantic event models as JSONL to a file."""

    def __init__(self, log_path: Path) -> None:
        self.log_path = log_path

    def handle(self, event: BaseEvent) -> None:
        """Append event as single JSON line. Log warning on write failure."""
        try:
            self.log_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.log_path, "a", encoding="utf-8") as f:
                f.write(event.model_dump_json() + "\n")
        except OSError as e:
            logger.warning("Failed to write event to %s: %s", self.log_path, e)
```

**Files**:
- `src/specify_cli/telemetry/jsonl_writer.py` (new, ~25 lines)

**Validation**: `pytest tests/specify_cli/telemetry/test_jsonl_writer.py` — should now PASS.

---

### Subtask T011 — GREEN: Create Factory Function

**Purpose**: Implement `load_event_bridge()` and wire it to JsonlEventWriter. Should make T008 tests pass.

**TDD Phase**: GREEN

**Steps**:
1. Create `src/specify_cli/core/events/factory.py`:

```python
from __future__ import annotations

import logging
from pathlib import Path

import yaml

from .bridge import CompositeEventBridge, EventBridge, NullEventBridge
from specify_cli.telemetry.jsonl_writer import JsonlEventWriter

logger = logging.getLogger(__name__)

DEFAULT_LOG_PATH = ".kittify/events.jsonl"


def load_event_bridge(repo_root: Path) -> EventBridge:
    """Load EventBridge from .kittify/config.yaml telemetry settings.

    Returns NullEventBridge if telemetry is not configured or disabled.
    """
    config_path = repo_root / ".kittify" / "config.yaml"
    try:
        if not config_path.exists():
            return NullEventBridge()

        with open(config_path, encoding="utf-8") as f:
            config = yaml.safe_load(f)

        if not isinstance(config, dict):
            return NullEventBridge()

        telemetry = config.get("telemetry", {})
        if not isinstance(telemetry, dict) or not telemetry.get("enabled"):
            return NullEventBridge()

        log_path_str = telemetry.get("log_path", DEFAULT_LOG_PATH)
        log_path = repo_root / log_path_str

        writer = JsonlEventWriter(log_path)
        bridge = CompositeEventBridge()
        bridge.register(writer.handle)
        return bridge

    except Exception:
        logger.warning("Failed to load event bridge config", exc_info=True)
        return NullEventBridge()
```

2. Update `src/specify_cli/core/events/__init__.py` to export factory:

```python
from .factory import load_event_bridge
# Add to __all__: "load_event_bridge"
```

**Files**:
- `src/specify_cli/core/events/factory.py` (new, ~45 lines)
- `src/specify_cli/core/events/__init__.py` (modified — add factory export)

**Validation**: `pytest tests/specify_cli/core/test_events/test_factory.py` — should now PASS.

---

### Subtask T012 — REFACTOR: Validate & Clean Up

**Purpose**: Run full quality checks on WP02 deliverables.

**TDD Phase**: REFACTOR

**Steps**:
1. Run all WP01 + WP02 tests:
   ```bash
   pytest tests/specify_cli/core/test_events/ tests/specify_cli/telemetry/ -v --tb=short
   ```
2. Run linter:
   ```bash
   ruff check src/specify_cli/core/events/ src/specify_cli/telemetry/ tests/specify_cli/core/test_events/ tests/specify_cli/telemetry/
   ```
3. Verify no regressions:
   ```bash
   pytest tests/ -x -q --ignore=tests/specify_cli/core/test_events/ --ignore=tests/specify_cli/telemetry/
   ```
4. Commit: `feat(telemetry): add JSONL writer and event bridge factory (040-WP02)`

**Validation**: All checks pass clean. No regressions.

---

## Risks & Mitigations

- **PyYAML not available**: PyYAML is already a spec-kitty dependency — verify in pyproject.toml.
- **Config schema conflicts**: The `telemetry:` key is new — no conflict with existing `agents:` key.
- **File permissions**: JSONL writer gracefully handles unwritable paths (FR-006).

## Review Guidance

- Verify factory returns NullEventBridge for all error/disabled cases.
- Verify JSONL output: each line valid JSON, no array wrappers, no trailing commas.
- Verify graceful failure: unwritable paths logged as warnings, no exceptions raised.
- Verify factory resolves relative paths against repo_root.

## Activity Log

- 2026-02-15T00:24:27Z – system – lane=planned – Prompt created.
