# Implementation Plan: Agent Profile Domain Model

**Branch**: `047-agent-profile-domain-model` | **Date**: 2026-02-21 | **Spec**: `kitty-specs/047-agent-profile-domain-model/spec.md`
**Input**: Feature specification from `kitty-specs/047-agent-profile-domain-model/spec.md`

## Summary

Introduce a rich `AgentProfile` Pydantic domain model as a first-class doctrine entity in `src/doctrine/`. Profiles define behavioral identity (purpose, specialization, collaboration contracts, reasoning modes, directive adherence) and are activated through constitution-level selections. The feature includes a specialization hierarchy with context-based routing, an `AgentProfileRepository` with two-source loading (shipped + project), CLI management commands, and curation flow compatibility for importing new profiles via the pull-based curation pipeline.

## Technical Context

**Language/Version**: Python 3.12+ (constitution requirement)
**Primary Dependencies**: Pydantic >=2.0 (model validation/serialization), ruamel.yaml (YAML parsing), Rich (CLI output), Typer (CLI commands), importlib.resources (package data access)
**Storage**: YAML files — shipped profiles in `src/doctrine/agent-profiles/`, project overrides in `.kittify/constitution/agents/`
**Testing**: pytest (core tier — 80% coverage), mypy, ruff, pre-commit hooks. **ATDD/TDD mandatory** per `src/doctrine/tactics/` (acceptance-test-first, tdd-red-green-refactor)
**Code Style**: Per `src/doctrine/styleguides/python-implementation.styleguide.yaml` — explicit typing for public functions, focused functions with minimal side effects, clear names over abbreviations
**Target Platform**: Cross-platform CLI (Linux, macOS, Windows)
**Project Type**: Monorepo CLI toolkit with doctrine/governance assets
**Performance Goals**: Profile loading <200ms for 50 profiles, CLI operations <2s
**Constraints**: `doctrine` package must have zero import dependencies on `specify_cli` (enforced by CI import scan). Existing `AgentProfile` in `specify_cli.constitution.schemas` must be migrated, not duplicated.
**Scale/Scope**: ~6 core roles with variants, curation pipeline support, constitution activation wiring

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Python 3.12+**: ✅ All new code targets 3.12+
- **Testing (core tier 80%)**: ✅ `src/doctrine/` is classified as core tier. ATDD/TDD practices required per `src/doctrine/tactics/acceptance-test-first.tactic.yaml` and `src/doctrine/tactics/tdd-red-green-refactor.tactic.yaml`
- **mypy + ruff**: ✅ All new Python modules must pass strict type checking and linting
- **Pre-commit hooks**: ✅ All commits go through pre-commit linting
- **CLI <2s**: ✅ Profile loading is pure YAML parsing, well within budget
- **Target branch**: `develop` (per constitution fork context)
- **No violations required**

### Test-First Gate (from doctrine tactics)

All implementation work packages MUST follow:
1. **Acceptance tests first** (`acceptance-test-first.tactic.yaml`): Define acceptance criteria as executable tests before implementation
2. **TDD red-green-refactor** (`tdd-red-green-refactor.tactic.yaml`): Write failing test → minimal implementation → refactor
3. **ZOMBIES ordering** (`zombies-tdd.tactic.yaml`): Zero → One → Many → Boundaries → Interface → Exceptions → Simple scenarios

## Project Structure

### Documentation (this feature)

```
kitty-specs/047-agent-profile-domain-model/
├── spec.md              # Feature specification
├── plan.md              # This file
├── research.md          # Phase 0 output (updated)
├── data-model.md        # Phase 1 output (updated)
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
└── tasks.md             # Phase 2 output (/spec-kitty.tasks)
```

### Source Code (repository root)

```
src/
├── doctrine/                              # Existing top-level package
│   ├── __init__.py                        # Existing
│   ├── agent-profiles/                    # UPGRADED: model + repository + shipped profiles
│   │   ├── __init__.py                    # NEW: public API exports
│   │   ├── profile.py                     # NEW: AgentProfile Pydantic model + value objects
│   │   ├── capabilities.py               # NEW: RoleCapabilities, canonical verbs
│   │   ├── repository.py                 # NEW: AgentProfileRepository (loading, hierarchy, matching)
│   │   └── shipped/                       # NEW: shipped reference profiles
│   │       ├── architect.agent.yaml
│   │       ├── designer.agent.yaml
│   │       ├── implementer.agent.yaml
│   │       ├── reviewer.agent.yaml
│   │       ├── planner.agent.yaml
│   │       ├── researcher.agent.yaml
│   │       └── curator.agent.yaml
│   ├── schemas/                           # Existing
│   │   └── agent-profile.schema.yaml      # Existing → expanded for rich 6-section model
│   ├── curation/                          # Existing — no structural changes
│   │   └── ...                            # agent-profile becomes a valid target_type
│   ├── missions/                          # Existing — no changes
│   ├── directives/                        # Existing — no changes
│   ├── tactics/                           # Existing — no changes
│   ├── paradigms/                         # Existing — no changes
│   ├── templates/                         # Existing — no changes
│   ├── styleguides/                       # Existing — no changes
│   └── toolguides/                        # Existing — no changes
├── specify_cli/
│   ├── constitution/
│   │   ├── schemas.py                     # MODIFIED: AgentProfile removed, imports from doctrine
│   │   └── resolver.py                    # MODIFIED: uses rich AgentProfile from doctrine
│   ├── orchestrator/
│   │   ├── agent_config.py                # DEPRECATED → alias to tool_config.py
│   │   └── tool_config.py                 # NEW: renamed from agent_config.py
│   └── cli/commands/
│       └── agents/
│           └── profile.py                 # NEW: CLI profile management commands

tests/
├── doctrine/                              # Existing dir
│   ├── test_profile_model.py              # NEW: AgentProfile Pydantic model tests
│   ├── test_capabilities.py              # NEW: RoleCapabilities tests
│   ├── test_profile_repository.py         # NEW: Repository loading/merge/hierarchy tests
│   ├── test_profile_schema_validation.py  # NEW: YAML schema validation tests
│   └── test_curation_agent_profile.py     # NEW: Curation flow for agent-profile target
├── unit/
│   └── specify_cli/
│       ├── constitution/
│       │   ├── test_resolver_rich_profiles.py  # NEW: resolver with rich profiles
│       │   └── test_schemas_migration.py       # NEW: verify AgentProfile moved out
│       └── orchestrator/
│           └── test_tool_config.py             # NEW: ToolConfig rename tests
```

**Structure Decision**: The `src/doctrine/agent-profiles/` directory becomes a Python subpackage containing the domain model (`profile.py`, `hierarchy.py`, `capabilities.py`), repository (`repository.py`), and shipped reference profiles (`shipped/*.agent.yaml`). This co-locates the model with its data, keeping agent profile concerns self-contained within the doctrine package.

## Key Design Decisions (updated from research.md)

### Decision 1 (REVISED): Modeling Approach — Pydantic

**Decision**: Use Pydantic `BaseModel` for `AgentProfile` and all value objects.

**Rationale**: The existing `AgentProfile` in `specify_cli.constitution.schemas` already uses Pydantic. Moving to Pydantic for the rich model provides built-in validation, serialization, JSON Schema generation, and YAML round-trip support without manual `to_dict()`/`from_dict()` boilerplate. The `doctrine` package's zero-import constraint on `specify_cli` is unaffected since Pydantic is a standalone dependency.

**Migration**: The shallow `AgentProfile` in `src/specify_cli/constitution/schemas.py` is replaced by the rich model in `src/doctrine/model/profile.py`. The constitution schemas module re-exports or adapts as needed.

### Decision 2 (unchanged): Single Distribution

`src/doctrine/` remains a subpackage within the `spec-kitty-cli` PyPI distribution.

### Decision 3 (unchanged): ToolConfig Rename — Alias-First

Create `tool_config.py`, replace `agent_config.py` with deprecated alias module.

### Decision 4 (unchanged): Pure YAML Format

Shipped profiles use `.agent.yaml`. The `.agent.md` format (as in Python Pedro reference) is the human-readable curation source that gets adapted to `.agent.yaml` during the curation import flow.

### Decision 5 (unchanged): importlib.resources

Use `importlib.resources` for locating shipped profiles within installed packages.

### Decision 6 (REVISED): Curation Flow as Acceptance Path

New agent profiles enter the system through the curation pipeline (`src/doctrine/curation/`). The `agent-profile` is a valid `target_type` for `ImportCandidate`. The manual acceptance test imports a profile via this flow end-to-end — from candidate creation through adoption to `resulting_artifacts` linkage.

## Parallel Work Analysis

### Dependency Graph

```
WP01 (model + value objects)
  ├──→ WP02 (repository + hierarchy traversal + matching) [depends on WP01]
  └──→ WP03 (schema expansion)     [depends on WP01]

WP02 + WP03 can run in parallel after WP01.

WP04 (reference profiles)         [depends on WP01 + WP03]
WP05 (constitution wiring)        [depends on WP02]
WP06 (ToolConfig rename)          [independent — can start anytime]
WP07 (CLI commands)               [depends on WP02]
WP08 (curation compatibility)     [depends on WP01 + WP03]
```

### Work Distribution

- **Sequential foundation**: WP01 must complete first (all other WPs depend on the model)
- **Parallel wave 1**: WP02, WP03, WP06 (independent of each other)
- **Parallel wave 2**: WP04, WP05, WP07, WP08 (depend on wave 1 outputs)

### Coordination Points

- **After WP01**: Model API frozen — all downstream WPs can begin
- **After WP02**: Repository API frozen — CLI (WP07) and constitution (WP05) can wire in
- **After WP03**: Schema frozen — reference profiles (WP04) and curation (WP08) can validate
- **Integration**: Each WP has its own acceptance tests; final integration verified by WP08 (curation end-to-end)

## Phase Plan

### Phase 0: Research & Baseline Alignment

1. Update research.md Decision 1 from frozen dataclasses to Pydantic (done in this plan)
2. Verify `src/doctrine/` package structure against current codebase state (done — structure confirmed)
3. Confirm `src/doctrine/agent-profiles/` is the profile location (not `agents/`)
4. Verify glossary alignment for all terms in spec (agent profile, tool, toolconfig, etc.)
5. Confirm no circular import risk between `doctrine.model` and `specify_cli.constitution`

**Outputs**: Updated `research.md`, confirmed baseline

### Phase 1: Design & Contracts

1. Update `data-model.md` to reflect Pydantic models (not frozen dataclasses)
2. Define YAML schema contract for `.agent.yaml` files (expand `agent-profile.schema.yaml`)
3. Define `AgentProfileRepository` API contract
4. Define constitution resolver integration contract (how `resolve_governance()` consumes rich profiles)
5. Define curation target type contract (`agent-profile` as valid `target_type`)

**Outputs**: Updated `data-model.md`, `contracts/`, `quickstart.md`

## Risks and Mitigations

- **Risk**: Pydantic model in `doctrine` creates implicit dependency direction from `specify_cli.constitution` → `doctrine`
  - **Mitigation**: This direction is intentional — constitution *consumes* doctrine. The constraint is that `doctrine` never imports from `specify_cli`.
- **Risk**: ToolConfig rename breaks downstream consumers silently
  - **Mitigation**: Alias-first approach with deprecation warnings. All 7 import sites identified and updated with passing tests at each step.
- **Risk**: Curation flow doesn't accommodate profile-specific adaptation steps
  - **Mitigation**: WP09 validates the full curation flow as an acceptance test. Schema validation ensures curated profiles are machine-valid.
- **Risk**: Reference profiles drift from doctrine structure (directives, tactics not yet populated)
  - **Mitigation**: Directive references stored as metadata only. Profiles remain valid even if referenced directives don't exist yet. Governance hooks (feature 044) validate availability at runtime.

## Implementation Readiness Checklist

- [x] Spec is populated with curation flow acceptance criteria (FR-017, FR-018)
- [x] Research updated for Pydantic decision
- [x] Data model documented with entity relationships and merge semantics
- [x] Constitution check passes (no violations)
- [x] Test-first gate acknowledged (ATDD + TDD + ZOMBIES per doctrine tactics)
- [x] Plan is concrete with dependency graph and parallel work analysis
- [ ] Tasks decomposition generated (`tasks.md` + WP files)

## Next Command

Proceed with task decomposition:

```bash
/spec-kitty.tasks
```
