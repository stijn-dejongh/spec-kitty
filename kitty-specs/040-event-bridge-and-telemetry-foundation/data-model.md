# Data Model: EventBridge and Telemetry Foundation

**Date**: 2026-02-14

## Entities

### BaseEvent

Base class for all lifecycle events.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| timestamp | datetime | Yes | When the event occurred (UTC) |
| type | str (Literal) | Yes | Event discriminator, set by subclass |

### LaneTransitionEvent (extends BaseEvent)

Records a work package moving between kanban lanes.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| type | Literal["lane_transition"] | Yes | Always "lane_transition" |
| work_package_id | str | Yes | WP identifier (e.g., "WP01") |
| from_lane | str | Yes | Source lane (planned, doing, for_review, done) |
| to_lane | str | Yes | Target lane |
| agent | str | None | No | Acting agent identifier |
| commit_sha | str | None | No | Git commit SHA at time of transition |

### ValidationEvent (extends BaseEvent)

Records a governance validation check result. Defined now, emitted by future features (042+).

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| type | Literal["validation"] | Yes | Always "validation" |
| validation_type | str | Yes | Check type: pre_plan, pre_implement, pre_review, pre_accept |
| status | str | Yes | Result: pass, warn, block |
| directive_refs | list[int] | No | Directive numbers that triggered this check |
| duration_ms | int | No | Validation duration in milliseconds |

### ExecutionEvent (extends BaseEvent)

Records an agent work execution. Defined now, emitted by future features (042+).

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| type | Literal["execution"] | Yes | Always "execution" |
| work_package_id | str | Yes | WP being executed |
| agent | str | Yes | Agent performing the work |
| model | str | Yes | LLM model used |
| input_tokens | int | No | Input token count |
| output_tokens | int | No | Output token count |
| cost_usd | float | No | Estimated cost in USD |
| duration_ms | int | No | Execution duration in milliseconds |
| success | bool | No | Whether execution succeeded (default: true) |
| error | str | None | No | Error message if failed |

## Relationships

```
BaseEvent
    ├── LaneTransitionEvent
    ├── ValidationEvent
    └── ExecutionEvent

EventBridge (ABC)
    ├── NullEventBridge         (discards all events)
    └── CompositeEventBridge    (fans out to listeners)
                                     │
                                     └──► JsonlEventWriter (appends to JSONL file)
```

## State Transitions

Events are **immutable** (frozen Pydantic models). There are no state transitions on the events themselves.

The **lane transition** recorded by `LaneTransitionEvent` reflects the WP state machine:

```
planned → doing → for_review → done
                       ↓
                    planned  (review rejection)
```

## Serialized Format (JSONL)

Each event is serialized as a single JSON line:

```json
{"type":"lane_transition","timestamp":"2026-02-14T22:00:00Z","work_package_id":"WP01","from_lane":"planned","to_lane":"doing","agent":"claude","commit_sha":"abc123"}
{"type":"lane_transition","timestamp":"2026-02-14T22:30:00Z","work_package_id":"WP01","from_lane":"doing","to_lane":"for_review","agent":"claude","commit_sha":"def456"}
```

## Config Schema

```yaml
# .kittify/config.yaml (extension)
telemetry:
  enabled: false                        # Default: disabled
  log_path: ".kittify/events.jsonl"     # Relative to repo root
```
