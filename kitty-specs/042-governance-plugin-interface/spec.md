# Feature Specification: Governance Plugin Interface

**Feature Branch**: `042-governance-plugin-interface`
**Created**: 2026-02-14
**Status**: Draft
**Input**: GovernancePlugin ABC with lifecycle hooks and advisory-only validation.

## User Scenarios & Testing

### User Story 1 - Governance Checks Run at Lifecycle Boundaries (Priority: P1)

As a Spec Kitty operator with a governance plugin configured, when I move through the spec-driven lifecycle (plan, implement, review, accept), the system runs governance validation checks at each boundary and reports results as advisories.

**Why this priority**: The lifecycle hooks are the core value of this feature. Without them, governance has no attachment point.

**Independent Test**: Configure a test governance plugin that returns "warn" for pre_plan. Run the planning workflow and verify the warning is displayed and logged but does not block progression.

**Acceptance Scenarios**:

1. **Given** a governance plugin that returns "warn" for pre_plan, **When** the user runs `/spec-kitty.plan`, **Then** the warning is displayed in the console output and the plan proceeds.
2. **Given** a governance plugin that returns "pass" for all hooks, **When** any workflow command runs, **Then** no governance output appears (silent pass).
3. **Given** no governance plugin configured, **When** any workflow command runs, **Then** behavior is identical to pre-042 (NullGovernancePlugin, no overhead).

---

### User Story 2 - Validation Results Are Structured and Actionable (Priority: P1)

As a governance plugin developer, when my plugin returns a validation result, it includes structured information (status, reasons, directive references, suggested actions) so the operator knows exactly what to fix.

**Why this priority**: Structured results are what distinguish governance from a linter. Plugin developers need a clear contract.

**Independent Test**: Create a validation result with status=warn, reasons=["Missing test plan"], directive_refs=[17], suggested_actions=["Add test plan to spec"]. Verify it serializes correctly and displays in a readable format.

**Acceptance Scenarios**:

1. **Given** a validation result with status "warn", reasons, and suggested actions, **When** displayed to the user, **Then** the output shows each reason and its corresponding suggested action.
2. **Given** a validation result with directive_refs, **When** displayed, **Then** the output references the directive numbers for traceability.

---

### User Story 3 - Governance Events Flow to EventBridge (Priority: P2)

As a telemetry consumer, when a governance check runs, a ValidationEvent is emitted to the EventBridge so that governance compliance is tracked over time.

**Why this priority**: Connects governance to the telemetry pipeline (040). Governance checks become auditable events.

**Independent Test**: Configure a governance plugin and an event listener. Run a lifecycle command. Verify a ValidationEvent with the correct validation_type and status is received by the listener.

**Acceptance Scenarios**:

1. **Given** a governance plugin and an EventBridge with a listener, **When** pre_plan validation runs, **Then** a ValidationEvent with validation_type="pre_plan" and the plugin's status is emitted.
2. **Given** no EventBridge configured (NullEventBridge), **When** governance runs, **Then** no error occurs (events silently discarded).

---

### User Story 4 - Skip Governance for Fast Iteration (Priority: P2)

As a developer in a tight iteration loop, I can skip governance checks with a flag so they don't slow me down during rapid prototyping.

**Why this priority**: Governance must not frustrate developers. A skip flag is essential for adoption.

**Independent Test**: Run a workflow command with --skip-governance. Verify no governance checks execute.

**Acceptance Scenarios**:

1. **Given** a governance plugin configured, **When** I run a command with --skip-governance, **Then** no validation hooks fire and the command proceeds normally.
2. **Given** --skip-governance is used, **When** telemetry is enabled, **Then** no ValidationEvent is emitted.

---

### Edge Cases

- What happens when a governance plugin raises an unexpected exception? Catch it, log a warning, treat as "pass" (do not block the workflow due to plugin bugs).
- What happens when multiple governance plugins are configured? Run all of them sequentially; aggregate results (any "block" → overall "block", any "warn" → overall "warn", else "pass"). Note: blocking mode is deferred to 043 but the aggregation logic should be ready.
- What happens when governance hooks are slow (>5s)? Log a performance warning. No timeout enforcement in this feature.

## Requirements

### Functional Requirements

- **FR-001**: System MUST provide a `GovernancePlugin` abstract base class with methods: `validate_pre_plan`, `validate_pre_implement`, `validate_pre_review`, `validate_pre_accept`.
- **FR-002**: Each validation method MUST accept a context object describing the current workflow state and MUST return a `ValidationResult`.
- **FR-003**: `ValidationResult` MUST contain: status (pass/warn/block), reasons (list of strings), directive_refs (list of ints), suggested_actions (list of strings).
- **FR-004**: System MUST provide a `NullGovernancePlugin` that returns "pass" for all hooks (default when no plugin configured).
- **FR-005**: In this feature, all governance results are advisory-only — "block" results are logged as warnings but do not halt the workflow.
- **FR-006**: System MUST call the appropriate governance hook before each lifecycle phase transition in the orchestrator.
- **FR-007**: System MUST emit a `ValidationEvent` to the EventBridge after each governance check (depends on Feature 040).
- **FR-008**: System MUST support a `--skip-governance` flag on workflow commands to bypass all governance checks.
- **FR-009**: System MUST catch exceptions thrown by governance plugins and treat them as "pass" with a logged warning.
- **FR-010**: Governance plugin loading MUST be configurable in `.kittify/config.yaml` under a `governance:` key.

### Key Entities

- **GovernancePlugin**: ABC for pluggable governance validation at lifecycle boundaries.
- **ValidationResult**: Structured output from governance checks (status, reasons, directive_refs, suggested_actions).
- **ValidationStatus**: Enum with values: pass, warn, block.
- **NullGovernancePlugin**: Default no-op implementation.
- **GovernanceContext**: Context passed to validation hooks — includes phase, feature_slug, work_package_id, tool_id (which tool is executing), agent_profile_id (Doctrine agent identity), agent_role (implementer/reviewer).

## Success Criteria

### Measurable Outcomes

- **SC-001**: All existing spec-kitty tests pass without modification (100% backward compatibility).
- **SC-002**: Governance hooks fire at correct lifecycle points when a plugin is configured.
- **SC-003**: NullGovernancePlugin adds less than 1ms overhead to any command.
- **SC-004**: ValidationResults display in a human-readable format with actionable guidance.
- **SC-005**: --skip-governance bypasses all governance entirely.
- **SC-006**: New code achieves at least 90% test coverage.

## Assumptions

- Depends on Feature 040 (EventBridge for ValidationEvent emission).
- Blocking enforcement is deferred to Feature 043 (Doctrine provider). This feature is advisory-only.
- Only one governance plugin is supported initially (no multi-plugin aggregation in v1, though the interface doesn't preclude it).
- The GovernanceContext objects will be simple dataclasses with fields extracted from existing spec-kitty state (spec content, WP metadata, review comments).
- Plugin discovery is config-driven, not dynamic (no entry_points or plugin registries).
