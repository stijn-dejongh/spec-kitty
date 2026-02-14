# Implementation Plan: EventBridge and Telemetry Foundation

**Branch**: `040-event-bridge-and-telemetry-foundation` | **Date**: 2026-02-14 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `kitty-specs/040-event-bridge-and-telemetry-foundation/spec.md`

## Summary

Add structured event emission to Spec Kitty's lifecycle. An `EventBridge` abstraction emits events at key workflow points (lane transitions, validations, tool executions). A `NullEventBridge` ensures zero impact for users who don't enable telemetry. A JSONL file writer in `src/specify_cli/telemetry/` provides the first concrete consumer. Pydantic BaseModel is used for event schema, giving schema validation and `model_dump_json()` for serialization.

## Technical Context

**Language/Version**: Python 3.11+ (existing spec-kitty codebase)
**Primary Dependencies**: pydantic >=2.0 (already a dependency), typing, pathlib, logging, json, datetime
**Storage**: Append-only JSONL file at `.kittify/events.jsonl` (when enabled)
**Testing**: pytest (existing test infrastructure)
**Target Platform**: Cross-platform (Linux, macOS, Windows via WSL)
**Project Type**: Single (extends existing CLI package)
**Performance Goals**: <1ms overhead for NullEventBridge; <10ms per JSONL append
**Constraints**: Zero behavioral change for existing users; no new mandatory dependencies
**Scale/Scope**: ~10 new files, ~500-700 lines of production code, ~400-600 lines of test code

## Constitution Check

*Constitution file not present. Skipped.*

## Project Structure

### Documentation (this feature)

```
kitty-specs/040-event-bridge-and-telemetry-foundation/
├── spec.md              # Feature specification
├── plan.md              # This file
├── research.md          # Phase 0 output (minimal — no unknowns)
├── data-model.md        # Phase 1 output (event schema)
├── meta.json            # Feature metadata
├── checklists/
│   └── requirements.md  # Spec quality checklist
└── tasks/               # Work packages (created by /spec-kitty.tasks)
```

### Source Code (repository root)

```
src/specify_cli/
├── core/
│   └── events/                    # NEW: Event ABCs and models
│       ├── __init__.py            # Public API exports
│       ├── bridge.py              # EventBridge ABC, NullEventBridge, CompositeEventBridge
│       ├── models.py              # Pydantic event models (LaneTransitionEvent, etc.)
│       └── factory.py             # load_event_bridge(repo_root) factory
│
├── telemetry/                     # NEW: Telemetry consumers
│   ├── __init__.py                # Public API exports
│   └── jsonl_writer.py            # JsonlEventWriter — appends events to JSONL file
│
├── orchestrator/
│   └── executor.py                # MODIFIED: Add event_bridge to ExecutionContext
│
└── cli/commands/agent/
    └── tasks.py                   # MODIFIED: Emit LaneTransitionEvent from move_task

tests/specify_cli/
├── core/
│   └── test_events/               # NEW: Event system tests
│       ├── test_bridge.py         # EventBridge, NullEventBridge, CompositeEventBridge tests
│       ├── test_models.py         # Event model serialization tests
│       └── test_factory.py        # Factory loading tests
│
└── telemetry/
    └── test_jsonl_writer.py       # JSONL writer tests (write, failure handling, format)
```

**Structure Decision**: New code lives in two packages — `core/events/` for the abstraction layer and `telemetry/` for the concrete JSONL consumer. This follows spec-kitty's existing pattern where `core/` holds foundational abstractions and domain-specific packages sit alongside.

## Architecture

### Event Flow

```
Lane Transition (move_task CLI or orchestrator)
    │
    ▼
EventBridge.emit_lane_transition(event)
    │
    ├──► NullEventBridge: discard (default)
    │
    └──► CompositeEventBridge: fan-out
              │
              ├──► JsonlEventWriter.handle(event) → .kittify/events.jsonl
              ├──► [Future: DashboardNotifier]
              └──► [Future: CostTracker]
```

### Wiring Strategy

**Orchestrator path** (`run_orchestration_loop` → `execute_wp`):
- Add `event_bridge: EventBridge` field to `ExecutionContext` dataclass (default: `NullEventBridge()`)
- The orchestrator's entry point (`start_orchestration_async`) calls `load_event_bridge(repo_root)` and passes the result when constructing `ExecutionContext`

**CLI path** (`move_task` command):
- `move_task` calls `load_event_bridge(repo_root)` at the start
- After updating the lane in frontmatter, emits `LaneTransitionEvent` via the bridge
- Direct parameter passing — consistent with existing move_task signature pattern

**Factory function** (`load_event_bridge`):
```python
def load_event_bridge(repo_root: Path) -> EventBridge:
    """Load EventBridge from .kittify/config.yaml telemetry settings.

    Returns NullEventBridge if telemetry is not configured or disabled.
    """
```
- Reads `telemetry.enabled` and `telemetry.log_path` from config
- If disabled or absent: returns `NullEventBridge()`
- If enabled: returns `CompositeEventBridge` with `JsonlEventWriter` registered

### Event Models (Pydantic)

```python
class BaseEvent(BaseModel):
    """Base for all lifecycle events."""
    model_config = ConfigDict(frozen=True)

    timestamp: datetime
    type: str  # Discriminator — set automatically by each subclass

class LaneTransitionEvent(BaseEvent):
    type: Literal["lane_transition"] = "lane_transition"
    work_package_id: str
    from_lane: str
    to_lane: str
    tool_id: str | None = None           # Which tool triggered this (e.g., "claude")
    agent_profile_id: str | None = None  # Agent identity (e.g., "python-pedro")
    commit_sha: str | None = None

class ValidationEvent(BaseEvent):
    type: Literal["validation"] = "validation"
    validation_type: str  # pre_plan | pre_implement | pre_review | pre_accept
    status: str           # pass | warn | block
    directive_refs: list[int] = []
    duration_ms: int = 0

class ExecutionEvent(BaseEvent):
    type: Literal["execution"] = "execution"
    work_package_id: str
    tool_id: str                          # Which tool executed (e.g., "claude", "opencode")
    agent_profile_id: str | None = None   # Agent identity if assigned
    agent_role: str | None = None         # Role: "implementer", "reviewer", etc.
    model: str
    input_tokens: int = 0
    output_tokens: int = 0
    cost_usd: float = 0.0
    duration_ms: int = 0
    success: bool = True
    error: str | None = None
```

### EventBridge ABC

```python
class EventBridge(ABC):
    @abstractmethod
    def emit_lane_transition(self, event: LaneTransitionEvent) -> None: ...

    @abstractmethod
    def emit_validation_event(self, event: ValidationEvent) -> None: ...

    @abstractmethod
    def emit_execution_event(self, event: ExecutionEvent) -> None: ...

class NullEventBridge(EventBridge):
    """Default: silently discards all events."""
    def emit_lane_transition(self, event): pass
    def emit_validation_event(self, event): pass
    def emit_execution_event(self, event): pass

class CompositeEventBridge(EventBridge):
    """Fan-out to registered listeners with error isolation."""
    def __init__(self, listeners: list[Callable] = None): ...
    def register(self, listener: Callable) -> None: ...
    # Each emit_* method calls all listeners, catching and logging exceptions per-listener
```

### Config Schema Extension

Addition to `.kittify/config.yaml`:

```yaml
telemetry:
  enabled: false                        # Default: off (NullEventBridge)
  log_path: ".kittify/events.jsonl"     # JSONL output path (relative to repo root)
```

### JSONL Writer

```python
class JsonlEventWriter:
    """Appends Pydantic event models as JSONL to a file."""

    def __init__(self, log_path: Path):
        self.log_path = log_path

    def handle(self, event: BaseEvent) -> None:
        """Append event as single JSON line. Log warning on write failure."""
        try:
            with open(self.log_path, "a", encoding="utf-8") as f:
                f.write(event.model_dump_json() + "\n")
        except OSError as e:
            logger.warning(f"Failed to write event to {self.log_path}: {e}")
```

### Integration Points (Modified Files)

**`src/specify_cli/orchestrator/executor.py`** — `ExecutionContext`:
- Add field: `event_bridge: EventBridge = field(default_factory=NullEventBridge)`
- No changes to `execute_wp` in this feature (events emitted from lane transition code, not executor)

**`src/specify_cli/cli/commands/agent/tasks.py`** — `move_task`:
- After line ~646 (where `set_scalar(wp.frontmatter, "lane", target_lane)` succeeds):
  - Call `event_bridge.emit_lane_transition(LaneTransitionEvent(...))`
  - Construct event from `old_lane`, `target_lane`, `task_id`, `tool_id`, current git HEAD

**`src/specify_cli/orchestrator/integration.py`** — `run_orchestration_loop`:
- Load event bridge at entry: `event_bridge = load_event_bridge(repo_root)`
- Pass to `ExecutionContext` construction

## Risk Mitigation

| Risk | Mitigation |
|------|-----------|
| JSONL write failure breaks workflow | All writes wrapped in try/except with logger.warning |
| Listener exception cascades | CompositeEventBridge catches per-listener, logs, continues |
| Config parsing failure | Factory returns NullEventBridge on any config error |
| Performance regression | NullEventBridge is a no-op; benchmark in tests |
| Pydantic schema changes break JSONL consumers | Event models use Literal type discriminators; schema is append-only |

## Complexity Tracking

No constitution violations. No unnecessary complexity introduced — all code directly serves spec requirements.
