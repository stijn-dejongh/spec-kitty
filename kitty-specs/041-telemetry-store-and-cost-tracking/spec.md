# Feature Specification: Telemetry Store and Cost Tracking

**Feature Branch**: `041-telemetry-store-and-cost-tracking`
**Created**: 2026-02-14
**Status**: Draft
**Input**: Lightweight query layer over JSONL event log with basic LLM cost tracking.

## User Scenarios & Testing

### User Story 1 - Query Lane Transition History (Priority: P1)

As a Spec Kitty operator, I can query the event log to see when each work package moved between lanes, so I can audit the timeline of a feature's development.

**Why this priority**: Timeline visibility is the most basic telemetry need. If the query layer works for lane transitions, it works for all event types.

**Independent Test**: Emit several lane transition events to a JSONL log, then query by work_package_id and verify the returned events match in correct chronological order.

**Acceptance Scenarios**:

1. **Given** a JSONL event log with lane transition events for multiple WPs, **When** I query by work_package_id="WP01", **Then** I receive only WP01's events in chronological order.
2. **Given** a JSONL event log, **When** I query by timeframe (start_date, end_date), **Then** I receive only events within that range.
3. **Given** an empty or missing JSONL file, **When** I query, **Then** I receive an empty result set (no error).

---

### User Story 2 - View Cost Summary by Agent and Model (Priority: P1)

As a team lead, I can see how much each AI agent has cost (by token usage and estimated USD) across a feature or timeframe, so I can manage my LLM spending.

**Why this priority**: Cost visibility is the primary business value of telemetry. Teams need to understand their LLM spend.

**Independent Test**: Create a JSONL log with ExecutionEvents containing token counts and costs, then query cost aggregation by agent and verify totals are correct.

**Acceptance Scenarios**:

1. **Given** execution events for agents "claude" and "codex", **When** I query cost summary grouped by agent, **Then** I see total input_tokens, output_tokens, and cost_usd per agent.
2. **Given** execution events, **When** I query cost summary grouped by model, **Then** I see totals per model (e.g., claude-sonnet-4, gpt-4o).
3. **Given** execution events, **When** I query with a timeframe filter, **Then** only events within that timeframe are aggregated.

---

### User Story 3 - Estimate Cost from Token Counts (Priority: P2)

As a developer, when an ExecutionEvent records token counts but not cost_usd, the system can estimate the cost using a pricing table, so I get cost visibility even when the agent doesn't report costs directly.

**Why this priority**: Not all agents report costs. A pricing table lets the system fill in estimates, improving cost visibility coverage.

**Independent Test**: Create an ExecutionEvent with tokens but zero cost, configure a pricing table with the model's rates, query cost summary and verify the estimated cost is calculated correctly.

**Acceptance Scenarios**:

1. **Given** an ExecutionEvent with input_tokens=1000, output_tokens=500, cost_usd=0.0, model="claude-sonnet-4", **When** the pricing table has rates for claude-sonnet-4, **Then** the query result includes an estimated cost calculated from the pricing table.
2. **Given** an ExecutionEvent with cost_usd=0.15 (already set), **When** queried, **Then** the reported cost uses the event's value, not the pricing table estimate.
3. **Given** a model not in the pricing table, **When** queried, **Then** the cost is reported as 0.0 with a warning flag.

---

### User Story 4 - CLI Cost Report Command (Priority: P2)

As a developer, I can run a CLI command to see a formatted cost report for the current project, so I can quickly check spending without building custom tooling.

**Why this priority**: A CLI command makes telemetry immediately accessible. Without it, users must parse JSONL manually.

**Independent Test**: Run the CLI command against a project with events and verify it outputs a readable table with agent names, token counts, costs, and totals.

**Acceptance Scenarios**:

1. **Given** a project with telemetry enabled and events logged, **When** I run the cost report command, **Then** I see a formatted table with per-agent cost breakdown and a total.
2. **Given** a project with no telemetry events, **When** I run the cost report command, **Then** I see a message indicating no events found.

---

### Edge Cases

- What happens when the JSONL file is very large (>100MB)? The query should stream-parse rather than loading the entire file into memory.
- What happens when JSONL lines are malformed (e.g., partial write from crash)? Skip malformed lines with a warning, return valid results.
- What happens when the pricing table YAML is missing or malformed? Use zero costs and log a warning.
- What happens when querying a feature that has no events? Return empty results, not an error.

## Requirements

### Functional Requirements

- **FR-001**: System MUST provide a query function that reads JSONL event logs and returns filtered, typed event objects.
- **FR-002**: System MUST support filtering events by: event type, work_package_id, agent, timeframe (start/end datetime).
- **FR-003**: System MUST provide cost aggregation that groups ExecutionEvents by agent and/or model and sums token counts and costs.
- **FR-004**: System MUST support a YAML-based pricing table that maps model identifiers to per-token input/output costs.
- **FR-005**: System MUST estimate costs for ExecutionEvents that have token counts but no cost_usd, using the pricing table.
- **FR-006**: System MUST prefer the event's own cost_usd when present over pricing table estimates.
- **FR-007**: System MUST handle malformed JSONL lines gracefully (skip with warning, continue parsing).
- **FR-008**: System MUST stream-parse JSONL files to avoid loading entire files into memory.
- **FR-009**: System MUST provide a CLI command for cost reporting (formatted table output via Rich).
- **FR-010**: The pricing table MUST be configurable in `.kittify/config.yaml` under a `telemetry.pricing` key.

### Key Entities

- **TelemetryQuery**: Query parameters (event_type, work_package_id, agent, start_time, end_time).
- **CostSummary**: Aggregated cost report (agent, model, total_input_tokens, total_output_tokens, total_cost_usd, event_count).
- **PricingTable**: Model-to-cost mapping (model_id -> cost_per_1k_input, cost_per_1k_output).

## Success Criteria

### Measurable Outcomes

- **SC-001**: Queries over a 10,000-line JSONL file complete in under 2 seconds.
- **SC-002**: Cost aggregation matches manual calculation within rounding tolerance (0.01 USD).
- **SC-003**: Malformed JSONL lines are skipped without crashing; valid events are still returned.
- **SC-004**: CLI cost report renders correctly for projects with 0, 1, and 100+ events.
- **SC-005**: New code achieves at least 90% test coverage.

## Assumptions

- Depends on Feature 040 (EventBridge and JSONL event log).
- ExecutionEvents are not yet emitted by spec-kitty itself (they will be in future features). Tests use synthetic events.
- SQLite materialized views are explicitly out of scope — deferred to a future feature if JSONL query performance becomes insufficient.
- The pricing table ships with reasonable defaults for major LLM providers (Anthropic, OpenAI) but is user-configurable.
- Log rotation is out of scope (deferred).
