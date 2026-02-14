# Feature Specification: Routing Provider Interface

**Feature Branch**: `045-routing-provider-interface`
**Created**: 2026-02-14
**Status**: Draft
**Input**: RoutingProvider ABC with fallback chains. Model selection delegated to the main model provider for context-aware decisions.

## User Scenarios & Testing

### User Story 1 - Route a Task to the Appropriate Model (Priority: P1)

As a spec-kitty orchestrator, when executing a work package, I need to determine which model/endpoint to use based on the task context (complexity, phase, budget), so that the right model handles each task.

**Why this priority**: This is the core routing mechanism. Without it, all tasks go to a single hardcoded model.

**Independent Test**: Configure a RoutingProvider with a primary model. Submit a routing request for a "plan" phase task. Verify a RoutingDecision is returned with the selected model endpoint and reasoning.

**Acceptance Scenarios**:

1. **Given** a configured RoutingProvider, **When** `route_task()` is called with task context (phase="plan", complexity="high"), **Then** a RoutingDecision is returned with a ModelEndpoint and human-readable reasoning.
2. **Given** a RoutingProvider with no special configuration, **When** `route_task()` is called, **Then** the default model endpoint is returned (sensible default behavior).
3. **Given** task context includes budget constraints, **When** `route_task()` is called, **Then** the routing decision respects the budget (e.g., selects a cheaper model for simple tasks).

---

### User Story 2 - Fallback Chain on Provider Failure (Priority: P1)

As a spec-kitty user, when the primary model endpoint is unavailable or returns an error, the system automatically tries the next provider in the fallback chain, so my workflow is not blocked by a single provider outage.

**Why this priority**: Resilience is critical for unattended agent workflows. A single provider failure should not halt a multi-WP execution.

**Independent Test**: Configure a fallback chain with 3 endpoints. Mock the first two as failing. Verify the third is used and the routing decision includes fallback metadata.

**Acceptance Scenarios**:

1. **Given** a fallback chain [ModelA, ModelB, ModelC] and ModelA is unavailable, **When** routing occurs, **Then** ModelB is selected and the decision notes it's a fallback.
2. **Given** all models in the fallback chain are unavailable, **When** routing occurs, **Then** a clear RoutingError is raised with details about each attempted endpoint.
3. **Given** a fallback chain, **When** the primary model succeeds, **Then** no fallback is attempted (short-circuit on success).

---

### User Story 3 - Context-Aware Model Selection via Primary Provider (Priority: P1)

As a project owner, I want model selection to be context-aware — the main model provider analyzes the task and makes an informed decision about which model to use, rather than relying on static rules.

**Why this priority**: This is the user's chosen approach. Static rule-based routing is brittle. Delegating to the primary model for context-aware selection leverages LLM judgment for nuanced decisions.

**Independent Test**: Send a routing request with rich task context (spec content, phase, complexity estimate). Verify the primary model is consulted and returns a selection with reasoning. Verify the reasoning references task-specific factors.

**Acceptance Scenarios**:

1. **Given** a task in "implement" phase with high complexity, **When** the primary provider is consulted, **Then** it returns a routing decision selecting a capable model with reasoning like "implementation requires strong code generation."
2. **Given** a task in "review" phase with low complexity, **When** the primary provider is consulted, **Then** it may select a lighter/cheaper model with appropriate reasoning.
3. **Given** a task where the primary provider cannot determine the best model, **When** consulted, **Then** it returns the default model with reasoning indicating uncertainty.

---

### User Story 4 - NullRoutingProvider for Projects Without Routing (Priority: P2)

As a spec-kitty user who hasn't configured routing, the system uses a NullRoutingProvider that always returns the default model, so existing workflows are unaffected.

**Why this priority**: Backward compatibility. Projects without routing configuration must work exactly as before.

**Independent Test**: Create a project with no routing configuration. Verify the NullRoutingProvider is loaded and always returns the default model endpoint.

**Acceptance Scenarios**:

1. **Given** no routing configuration, **When** `load_routing_provider()` is called, **Then** a NullRoutingProvider is returned.
2. **Given** a NullRoutingProvider, **When** `route_task()` is called with any context, **Then** the default model endpoint is returned with no external calls.
3. **Given** a NullRoutingProvider, **When** `get_fallback_chain()` is called, **Then** an empty list is returned (no fallbacks configured).

---

### Edge Cases

- What happens when the routing provider's own API call fails (e.g., primary model is down)? Fall back to the default model endpoint without consulting — the fallback chain handles resilience.
- What happens when routing configuration references a model that doesn't exist? Validation at config load time with a clear error message.
- What happens when budget is exhausted mid-execution? The routing provider returns a RoutingError with budget exhaustion details, allowing the orchestrator to decide (pause, switch to cheaper model, or abort).
- What happens when two routing providers are configured? Only one active provider — configuration validation rejects ambiguous setups.

## Requirements

### Functional Requirements

- **FR-001**: System MUST provide a `RoutingProvider` ABC with `route_task(context: RoutingContext) -> RoutingDecision` and `get_fallback_chain() -> list[ModelEndpoint]` methods.
- **FR-002**: System MUST provide a `NullRoutingProvider` that returns the default model endpoint for all routing requests (null-object pattern, zero external calls).
- **FR-003**: System MUST provide a `ContextAwareRoutingProvider` that delegates model selection to the primary model provider, passing task context for informed decisions.
- **FR-004**: The `ContextAwareRoutingProvider` MUST send a structured prompt to the primary model describing the task (phase, complexity, budget remaining, available models) and parse the model's selection response.
- **FR-005**: System MUST support fallback chains — an ordered list of `ModelEndpoint` alternatives tried sequentially on failure.
- **FR-006**: System MUST provide `RoutingDecision` dataclass containing: selected `ModelEndpoint`, reasoning (human-readable string), is_fallback (bool), and attempted_endpoints (list of failed endpoints, if any).
- **FR-007**: System MUST provide `ModelEndpoint` dataclass containing: provider name, model ID, estimated cost tier (low/medium/high), and capability tags.
- **FR-008**: System MUST provide `RoutingContext` dataclass containing: phase (plan/implement/review/accept), complexity estimate, budget remaining (optional), task summary, and available model endpoints.
- **FR-009**: System MUST provide a factory function `load_routing_provider(repo_root: Path) -> RoutingProvider` that reads configuration from `.kittify/config.yaml` and returns the appropriate provider (NullRoutingProvider if unconfigured).
- **FR-010**: System MUST emit a `RoutingEvent` via the EventBridge (Feature 040) when a routing decision is made, including the selected model, reasoning, and whether a fallback was used.

### Key Entities

- **RoutingProvider (ABC)**: Abstract interface for model/endpoint selection with fallback support.
- **NullRoutingProvider**: Default no-op provider that returns the default model (null-object pattern).
- **ContextAwareRoutingProvider**: Delegates selection to the primary model for context-aware decisions.
- **RoutingDecision**: Immutable result of a routing decision (selected endpoint, reasoning, fallback metadata).
- **ModelEndpoint**: Describes a model/provider endpoint (name, model ID, cost tier, capabilities).
- **RoutingContext**: Task context passed to the routing provider (phase, complexity, budget, available models).
- **RoutingEvent**: Event emitted when routing occurs (for telemetry via Feature 040).

## Success Criteria

### Measurable Outcomes

- **SC-001**: NullRoutingProvider returns a decision in under 1ms (no external calls).
- **SC-002**: ContextAwareRoutingProvider returns a decision with reasoning that references task-specific factors (not generic boilerplate).
- **SC-003**: Fallback chain correctly tries N endpoints and selects the first available one.
- **SC-004**: Projects without routing configuration work identically to pre-045 behavior (zero regressions).
- **SC-005**: RoutingEvents are emitted to the EventBridge for every routing decision.
- **SC-006**: New code achieves at least 90% test coverage.

## Assumptions

- Depends on Feature 040 (EventBridge for RoutingEvent emission).
- Depends on Feature 042 (GovernancePlugin ABC pattern — follows the same ABC + null-object + factory conventions).
- The primary model provider is available and can process structured prompts for model selection.
- Model endpoints are configured in `.kittify/config.yaml` under a `routing` section.
- Cost tiers (low/medium/high) are sufficient for initial routing decisions; exact token pricing is handled by Feature 047.
- The ContextAwareRoutingProvider's prompt to the primary model is a structured system prompt, not a user-facing interaction.
