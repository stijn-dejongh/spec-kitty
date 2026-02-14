# Feature Specification: EventBridge and Telemetry Foundation

**Feature Branch**: `040-event-bridge-and-telemetry-foundation`
**Created**: 2026-02-14
**Status**: Draft
**Input**: Add structured event emission infrastructure to Spec Kitty's orchestrator lifecycle.

## User Scenarios & Testing

### User Story 1 - Lane Transition Events Are Recorded (Priority: P1)

As a Spec Kitty operator, when work packages move between lanes (planned -> doing -> for_review -> done), the system records each transition as a structured event so that I can later audit what happened and when.

**Why this priority**: Lane transitions are the most frequent lifecycle event in Spec Kitty. If events work for lane transitions, the architecture is proven for all other event types.

**Independent Test**: Can be fully tested by moving a WP between lanes and verifying a JSONL file contains the transition event with correct timestamps, WP ID, from/to lanes, and agent identity.

**Acceptance Scenarios**:

1. **Given** a project with EventBridge configured and a JSONL listener registered, **When** a work package moves from "planned" to "doing", **Then** a LaneTransitionEvent is appended to the JSONL log with timestamp, work_package_id, from_lane="planned", to_lane="doing", and the acting agent.
2. **Given** a project with no EventBridge configuration (default), **When** a work package moves between lanes, **Then** no error occurs, no event file is created, and the lane transition completes normally (NullEventBridge behavior).
3. **Given** a JSONL listener is registered, **When** multiple lane transitions occur in sequence, **Then** events are appended in order and no events are lost.

---

### User Story 2 - Multiple Listeners Receive Events (Priority: P2)

As a plugin developer, I can register multiple event listeners (e.g., a JSONL writer and a future dashboard notifier) on the same EventBridge, and all listeners receive every event.

**Why this priority**: Fan-out to multiple consumers is the key architectural property that makes the EventBridge useful for governance, cost tracking, and dashboards in future features.

**Independent Test**: Can be tested by registering two in-memory listeners, emitting an event, and verifying both listeners received it.

**Acceptance Scenarios**:

1. **Given** an EventBridge with two registered listeners, **When** a LaneTransitionEvent is emitted, **Then** both listeners receive the event.
2. **Given** an EventBridge with one listener that raises an exception, **When** an event is emitted, **Then** the other listener still receives the event and the exception is logged but does not crash the workflow.

---

### User Story 3 - Existing Workflows Are Unaffected (Priority: P1)

As an existing Spec Kitty user who has not configured any telemetry, all my current commands and workflows work exactly as before with no new files created and no performance degradation.

**Why this priority**: Backward compatibility is a hard constraint. The EventBridge must be invisible to users who don't opt in.

**Independent Test**: Run the full spec-kitty test suite with no telemetry configuration. All tests pass. No new files appear in .kittify/ or project root.

**Acceptance Scenarios**:

1. **Given** a project initialized before this feature existed, **When** I upgrade spec-kitty and run any workflow command, **Then** behavior is identical to the previous version.
2. **Given** no telemetry configuration in .kittify/config.yaml, **When** any orchestrator command runs, **Then** no events.jsonl file is created and no telemetry-related output appears.

---

### User Story 4 - JSONL Events Are Machine-Readable (Priority: P2)

As a developer building tooling on top of Spec Kitty, I can parse the JSONL event log with standard JSON tools (jq, Python json module) to build custom reports, dashboards, or integrations.

**Why this priority**: The JSONL format is the primary persistence mechanism. If it's not reliably parseable, downstream features (telemetry store, dashboard) can't build on it.

**Independent Test**: Parse every line of a generated events.jsonl file with `json.loads()`. Every line is valid JSON. Every event has a `type` field and a `timestamp` field.

**Acceptance Scenarios**:

1. **Given** an events.jsonl file with recorded events, **When** I parse each line as JSON, **Then** every line is valid JSON containing at minimum: `type` (event class name), `timestamp` (ISO 8601), and event-specific fields.
2. **Given** a LaneTransitionEvent in the JSONL log, **When** I parse it, **Then** it contains `work_package_id`, `from_lane`, `to_lane`, `agent` (nullable), and `commit_sha` (nullable).

---

### Edge Cases

- What happens when the JSONL log file is not writable (permissions, disk full)? The event emission must not crash the workflow -- log a warning and continue.
- What happens when a listener is registered after events have already been emitted? It receives only future events, not past ones (no replay).
- What happens when the EventBridge is used from multiple threads? Thread safety is not required in this feature (Spec Kitty orchestrator is single-threaded), but the design must not preclude adding it later.
- What happens when the JSONL file grows very large? This feature does not implement rotation -- that is deferred to the telemetry store feature (041).

## Requirements

### Functional Requirements

- **FR-001**: System MUST provide an `EventBridge` abstract base class in `src/specify_cli/core/events/` with methods for emitting lane transition, validation, and execution events.
- **FR-002**: System MUST provide frozen dataclasses for `LaneTransitionEvent`, `ValidationEvent`, and `ExecutionEvent` in `src/specify_cli/core/events/`.
- **FR-003**: System MUST provide a `NullEventBridge` implementation that silently discards all events and is used as the default when no telemetry is configured.
- **FR-004**: System MUST provide a `CompositeEventBridge` that fans out events to zero or more registered listener callables.
- **FR-005**: System MUST provide a JSONL event log writer in `src/specify_cli/telemetry/` that appends serialized events to a configurable file path.
- **FR-006**: The JSONL writer MUST handle write failures gracefully (log warning, do not crash the workflow).
- **FR-007**: The `CompositeEventBridge` MUST isolate listener failures -- one listener's exception MUST NOT prevent other listeners from receiving the event.
- **FR-008**: All event dataclasses MUST include a `timestamp` field (datetime) and a `type` field (string) for identification in serialized form.
- **FR-009**: The orchestrator's lane transition code paths MUST accept an optional EventBridge parameter, defaulting to NullEventBridge.
- **FR-010**: The JSONL writer MUST serialize events as one JSON object per line, with no trailing commas or array wrappers.

### Key Entities

- **EventBridge**: Abstract protocol for emitting structured lifecycle events. Core extension point.
- **LaneTransitionEvent**: Records a work package moving between kanban lanes. Fields: timestamp, work_package_id, from_lane, to_lane, agent (optional), commit_sha (optional).
- **ValidationEvent**: Records a governance validation check result. Fields: timestamp, validation_type, status, directive_refs, duration_ms.
- **ExecutionEvent**: Records an agent work execution. Fields: timestamp, work_package_id, agent, model, input_tokens, output_tokens, cost_usd, duration_ms, success, error (optional).
- **NullEventBridge**: Default implementation that discards all events (null-object pattern).
- **CompositeEventBridge**: Fan-out implementation that dispatches events to registered listeners.
- **JsonlEventWriter**: JSONL file appender that serializes events as one JSON object per line.

## Success Criteria

### Measurable Outcomes

- **SC-001**: All existing spec-kitty tests pass without modification after this feature is integrated (100% backward compatibility).
- **SC-002**: Events emitted during lane transitions contain all required fields and can be parsed by standard JSON tools.
- **SC-003**: The NullEventBridge adds less than 1ms overhead to any workflow command (negligible performance impact).
- **SC-004**: The JSONL writer correctly persists events across at least 1000 sequential writes without data loss.
- **SC-005**: Listener isolation works -- a deliberately failing listener does not prevent other listeners from receiving events.
- **SC-006**: New code achieves at least 90% test coverage.

## Assumptions

- The Spec Kitty orchestrator is single-threaded; thread safety is not required for this feature.
- The JSONL file path defaults to `.kittify/events.jsonl` when telemetry is enabled.
- Log rotation and archival are out of scope (deferred to feature 041).
- The ValidationEvent and ExecutionEvent dataclasses are defined now but will only be actively emitted by future features (042+). This feature emits LaneTransitionEvents only.
- The EventBridge configuration will be added to `.kittify/config.yaml` under a `telemetry:` key.
