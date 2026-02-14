# Feature Specification: Doctrine Governance Provider

**Feature Branch**: `043-doctrine-governance-provider`
**Created**: 2026-02-14
**Status**: Draft
**Input**: Concrete GovernancePlugin implementation that loads and evaluates Doctrine artifacts.

## User Scenarios & Testing

### User Story 1 - Doctrine Directives Evaluated at Lifecycle Boundaries (Priority: P1)

As a team using Agentic Doctrine, when I move through spec-kitty's lifecycle, relevant directives are loaded and evaluated against the current work state, and I see advisory or blocking feedback referencing specific directive numbers.

**Why this priority**: This is the core value — connecting Doctrine's behavioral governance to Spec Kitty's workflow.

**Independent Test**: Create a minimal doctrine/ tree with one directive (e.g., "017: TDD required"). Configure the plugin. Run pre_implement validation on a WP without tests. Verify the result references directive 017.

**Acceptance Scenarios**:

1. **Given** a doctrine/ subtree with directive 017 (TDD), **When** pre_implement runs on a WP with no test plan, **Then** the result is "warn" with directive_refs=[17] and a suggested action to add tests.
2. **Given** a doctrine/ subtree with directives, **When** pre_plan runs, **Then** only planning-relevant directives are loaded and evaluated (lazy loading).
3. **Given** no doctrine/ directory in the project, **When** the plugin is loaded, **Then** it falls back to NullGovernancePlugin behavior (no errors, no checks).

---

### User Story 2 - Precedence Resolution Between Constitution and Directives (Priority: P1)

As a project owner, my Constitution can narrow or extend Doctrine rules for my specific project, and the system correctly resolves conflicts by following the precedence hierarchy.

**Why this priority**: The "two-masters" problem is the top architectural risk. Precedence resolution is essential for trust.

**Independent Test**: Create a Constitution that says "test coverage minimum: 60%" and a directive that says "80% coverage required". Verify the system uses the Constitution's value (Constitution narrows the directive).

**Acceptance Scenarios**:

1. **Given** a Constitution that narrows directive 017 to "60% coverage", **When** pre_implement evaluates, **Then** the 60% threshold is used (Constitution overrides directive detail).
2. **Given** a Constitution that contradicts a General Guideline, **When** the plugin loads, **Then** a "warn" is emitted identifying the contradiction and advising the user to update their Constitution.
3. **Given** no Constitution or .doctrine-config/, **When** the plugin loads, **Then** directives apply at their default values.

---

### User Story 3 - Opt-in Blocking Mode (Priority: P2)

As a team lead who wants strict governance, I can enable --enforce-governance so that "block" results actually halt the workflow, forcing the team to address governance issues before proceeding.

**Why this priority**: Advisory-only (042) provides visibility. Blocking mode provides enforcement. Both are needed for adoption.

**Independent Test**: Configure a plugin that returns "block" for pre_review. Run review with --enforce-governance. Verify the workflow halts with an error message.

**Acceptance Scenarios**:

1. **Given** --enforce-governance is set and a plugin returns "block", **When** the lifecycle command runs, **Then** the command exits with a non-zero status and displays the blocking reasons.
2. **Given** --enforce-governance is NOT set (default) and a plugin returns "block", **Then** the result is displayed as a warning but the workflow continues (advisory mode from 042).
3. **Given** --enforce-governance and --skip-governance both set, **Then** --skip-governance takes precedence (skip wins).

---

### User Story 4 - Lazy Directive Loading (Priority: P2)

As a developer, the governance plugin only loads directives relevant to the current lifecycle phase, keeping context overhead minimal.

**Why this priority**: Token budget is a real constraint. Loading all directives for every check wastes context.

**Independent Test**: Run pre_plan validation and verify only planning-relevant directives were loaded (not implementation or review directives).

**Acceptance Scenarios**:

1. **Given** 20 directives in doctrine/, **When** pre_plan runs, **Then** only directives tagged for planning phase are loaded (typically 3-5).
2. **Given** directives were loaded for pre_plan, **When** pre_implement runs next in the same session, **Then** implementation directives are loaded (may overlap, may be different set).

---

### Edge Cases

- What happens when the doctrine/ subtree is outdated (old version)? The plugin validates against whatever version is present. Version checking is informational only.
- What happens when a directive file is malformed? Skip it with a warning, continue with remaining directives.
- What happens when the Constitution references directives that don't exist? Log a warning, ignore the reference.
- What happens when directive evaluation is ambiguous? Default to "pass" — governance should not block on uncertainty.

## Requirements

### Functional Requirements

- **FR-001**: System MUST provide a `DoctrineGovernancePlugin` that implements the `GovernancePlugin` ABC from Feature 042.
- **FR-002**: The plugin MUST load Doctrine artifacts from a `doctrine/` directory at the project root (distributed via git subtree).
- **FR-003**: The plugin MUST load `.doctrine-config/` overrides and Constitution (`constitution.md`) when present.
- **FR-004**: The plugin MUST resolve precedence: General Guidelines > Operational Guidelines > Constitution/.doctrine-config > Directives > Mission guidance > Tactics.
- **FR-005**: The plugin MUST detect and warn on Constitution-vs-Guideline contradictions.
- **FR-006**: The plugin MUST implement lazy loading — only directives relevant to the current lifecycle phase are loaded per check.
- **FR-007**: System MUST support `--enforce-governance` flag that makes "block" results halt the workflow with a non-zero exit code.
- **FR-008**: System MUST fall back to NullGovernancePlugin behavior when doctrine/ is not present.
- **FR-009**: Each validation result MUST include directive_refs identifying which directives triggered the result.
- **FR-010**: The plugin MUST be configurable in `.kittify/config.yaml` under `governance.provider: doctrine`.
- **FR-011**: The plugin MUST load agent profiles from `doctrine/agents/*.agent.md` when present.
- **FR-012**: When an agent profile is loaded for the assigned agent, the plugin MUST filter directives to the profile's `required_directives` and validate that the agent's `capabilities` match the task requirements.
- **FR-013**: Agent-to-profile mapping MUST be configurable in `.doctrine-config/config.yaml` under `agent_profiles:` (mapping SK agent keys to doctrine profile IDs).
- **FR-014**: When no agent profile matches the assigned agent, the plugin MUST proceed with all applicable directives (graceful degradation).

### Key Entities

- **DoctrineGovernancePlugin**: Concrete GovernancePlugin that loads and evaluates Doctrine artifacts.
- **DoctrineLoader**: Reads doctrine/ directory structure, parses guidelines, directives, approaches, and agent profiles.
- **PrecedenceResolver**: Resolves conflicts between governance layers per the Doctrine hierarchy.
- **DirectiveEvaluator**: Evaluates individual directives against lifecycle context.
- **AgentProfile**: Parsed agent profile defining role identity, capabilities, required directives, and handoff patterns.

## Success Criteria

### Measurable Outcomes

- **SC-001**: Governance checks complete in under 500ms per validation (lazy loading of directives).
- **SC-002**: Precedence resolution is deterministic — same inputs always produce same output.
- **SC-003**: Governance overhead is less than 6K tokens of context per phase (lazy loading).
- **SC-004**: Projects without doctrine/ directory work unchanged (zero regressions).
- **SC-005**: --enforce-governance correctly blocks on "block" results.
- **SC-006**: New code achieves at least 90% test coverage.

## Assumptions

- Depends on Feature 042 (GovernancePlugin ABC and hook callsites).
- Depends on Feature 040 (EventBridge for ValidationEvent emission).
- Doctrine artifacts follow the Agentic Doctrine directory structure (doctrine/guidelines/, doctrine/directives/, doctrine/approaches/, doctrine/agents/).
- Directive files include metadata (front matter or structured comments) indicating which lifecycle phases they apply to.
- The `spec-kitty init --doctrine` flag for bootstrapping is deferred to Feature 050 (docs and migration).
