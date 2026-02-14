# Research: EventBridge and Telemetry Foundation

**Date**: 2026-02-14
**Status**: Complete — no open unknowns

## Summary

No significant unknowns required research. All technical decisions were resolved during discovery and planning interrogation.

## Decisions

### 1. Event Serialization Format

- **Decision**: Pydantic BaseModel with `model_dump_json()`
- **Rationale**: Pydantic is already a spec-kitty dependency. Gets schema validation, type coercion, and JSON serialization for free. Frozen models ensure event immutability.
- **Alternatives considered**: `dataclasses.asdict + json.dumps` (lighter but no validation), custom `to_dict()` (more boilerplate)

### 2. Dependency Wiring

- **Decision**: Add EventBridge to ExecutionContext (orchestrator path); direct parameter passing (CLI path); factory function `load_event_bridge()` reads config.
- **Rationale**: Consistent with spec-kitty's dominant pattern of explicit parameter passing and context dataclasses. No singletons or global state.
- **Alternatives considered**: Module-level singleton (rejected — violates existing patterns), separate DI container (over-engineering for current scope)

### 3. JSONL vs Structured DB

- **Decision**: JSONL append-only log as first consumer; SQLite deferred to feature 041.
- **Rationale**: JSONL is simpler, requires no new dependencies, and is trivially parseable. SQLite materialized views add query power but are not needed until the telemetry store feature.
- **Alternatives considered**: SQLite from the start (too much scope for foundation feature), CSV (not suitable for nested event structures)

### 4. Listener Error Isolation

- **Decision**: CompositeEventBridge catches exceptions per-listener, logs them, and continues dispatching to remaining listeners.
- **Rationale**: One bad listener must not break the workflow or prevent other listeners from receiving events. This is standard observer pattern practice.
- **Alternatives considered**: Fail-fast (rejected — violates backward compat), retry (over-engineering for this scope)
