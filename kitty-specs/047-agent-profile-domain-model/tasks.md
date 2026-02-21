# Work Packages: Agent Profile Domain Model

**Inputs**: Design documents from `kitty-specs/047-agent-profile-domain-model/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, quickstart.md

**Tests**: Core tier (80% coverage). ATDD/TDD mandatory per `src/doctrine/tactics/`.

**Code Style**: Per `src/doctrine/styleguides/python-implementation.styleguide.yaml`.

**Organization**: Fine-grained subtasks (`Txxx`) roll up into work packages (`WPxx`). Each work package is independently deliverable and testable.

---

## Work Package WP01: AgentProfile Pydantic Model & Value Objects (Priority: P0) MVP

**Goal**: Define the rich `AgentProfile` Pydantic model with all 6-section value objects and `Role` enum in `src/doctrine/agent-profiles/profile.py`. Define `RoleCapabilities` in `capabilities.py`.
**Independent Test**: Create an `AgentProfile` from a dict, serialize to YAML, deserialize back, verify round-trip fidelity. Required field enforcement rejects incomplete profiles.
**Prompt**: `tasks/WP01-agent-profile-model.md`
**Estimated Size**: ~450 lines

### Included Subtasks

- [x] T001 Create `src/doctrine/agent-profiles/__init__.py` with public API exports
- [x] T002 Define `Role` StrEnum with controlled vocabulary + custom role support
- [x] T003 Define value objects: `Specialization`, `CollaborationContract`, `SpecializationContext`, `ContextSources`, `ModeDefault`, `DirectiveRef`
- [x] T004 Define `AgentProfile` Pydantic BaseModel with all fields and validators
- [x] T005 Define `TaskContext` Pydantic model (input for matching)
- [x] T006 Define `RoleCapabilities` in `src/doctrine/agent-profiles/capabilities.py`
- [x] T007 Write acceptance + unit tests in `tests/doctrine/test_profile_model.py` and `test_capabilities.py`

### Dependencies

- None (starting package).

---

## Work Package WP02: AgentProfileRepository (Priority: P0) MVP

**Goal**: Implement `AgentProfileRepository` in `src/doctrine/agent-profiles/repository.py` with two-source loading, field-level merge, hierarchy traversal, and weighted context matching.
**Independent Test**: Load shipped + project profiles, verify merge, query by role, find best match, validate hierarchy (no cycles).
**Prompt**: `tasks/WP02-profile-repository.md`
**Estimated Size**: ~500 lines

### Included Subtasks

- [x] T008 Implement repository class with two-source YAML loading (shipped via `importlib.resources` + project dir)
- [x] T009 Implement field-level merge semantics (project overrides shipped)
- [x] T010 Implement `list_all()`, `get()`, `find_by_role()` query methods
- [x] T011 Implement hierarchy traversal: `get_children()`, `get_ancestors()`, `get_hierarchy_tree()`
- [x] T012 Implement `validate_hierarchy()` — cycle detection, orphaned references, duplicate IDs
- [x] T013 Implement `find_best_match(context: TaskContext)` with weighted scoring (DDR-011). Test scenarios: (1) workload penalties (0-2 tasks=1.0, 3-4=0.85, 5+=0.70), (2) complexity adjustments (low/medium/high multipliers), (3) language/framework/file pattern matching weights
- [x] T014 Implement `save()` and `delete()` for project-dir profiles
- [x] T015 Write acceptance + unit tests in `tests/doctrine/test_profile_repository.py` — include test scenario for zero-profile repository (returns empty list, no crash), test with Architect Alphonso and Python Pedro profiles for hierarchy validation

### Dependencies

- Depends on WP01.

---

## Work Package WP03: YAML Schema Expansion (Priority: P0)

**Goal**: Expand `src/doctrine/schemas/agent-profile.schema.yaml` to match the rich 6-section model. Add schema validation utility and tests.
**Independent Test**: Valid profile passes schema. Incomplete profile fails with actionable error.
**Prompt**: `tasks/WP03-schema-expansion.md`
**Estimated Size**: ~300 lines

### Included Subtasks

- [x] T016 Expand `src/doctrine/schemas/agent-profile.schema.yaml` with all 6-section fields
- [x] T017 Add schema validation utility function
- [x] T018 Create valid and invalid fixture YAML files
- [x] T018b Test schema utility rejects non-.agent.yaml files (file extension validation)
- [x] T019 Write schema validation tests in `tests/doctrine/test_profile_schema_validation.py`

### Dependencies

- Depends on WP01.

---

## Work Package WP04: Shipped Reference Profiles (Priority: P1)

**Goal**: Create 7 shipped reference profiles in `src/doctrine/agent-profiles/shipped/` for core roles.
**Independent Test**: All shipped profiles load via repository, pass schema validation, form valid hierarchy.
**Prompt**: `tasks/WP04-reference-profiles.md`
**Estimated Size**: ~400 lines

### Included Subtasks

- [ ] T020 Create `src/doctrine/agent-profiles/shipped/` directory
- [ ] T021 [P] Create `architect.agent.yaml`
- [ ] T022 [P] Create `designer.agent.yaml`
- [ ] T023 [P] Create `implementer.agent.yaml`
- [ ] T024 [P] Create `reviewer.agent.yaml`
- [ ] T025 [P] Create `planner.agent.yaml`
- [ ] T026 [P] Create `researcher.agent.yaml` and `curator.agent.yaml`
- [ ] T027 Write profile catalog integration test

### Dependencies

- Depends on WP01 and WP03.

---

## Work Package WP05: Constitution Wiring (Priority: P1)

**Goal**: Move `AgentProfile` out of `specify_cli.constitution.schemas` into doctrine. Update `resolver.py` to consume rich profiles from repository.
**Independent Test**: `resolve_governance()` returns rich profiles. Shallow `AgentProfile` no longer exists in `schemas.py`.
**Prompt**: `tasks/WP05-constitution-wiring.md`
**Estimated Size**: ~350 lines

### Included Subtasks

- [ ] T028 Remove `AgentProfile` class from `src/specify_cli/constitution/schemas.py`
- [ ] T029 Add import of `AgentProfile` from `doctrine.agent_profiles.profile`
- [ ] T030 Update `resolver.py` to use rich profiles and `profile_id` keying
- [ ] T031 Update `GovernanceResolution` downstream consumers
- [ ] T032 Write resolver tests in `tests/unit/specify_cli/constitution/test_resolver_rich_profiles.py`
- [ ] T033 Write migration test in `tests/unit/specify_cli/constitution/test_schemas_migration.py`

### Dependencies

- Depends on WP02.

---

## Work Package WP06: ToolConfig Rename (Priority: P1)

**Goal**: Rename `AgentConfig` → `ToolConfig` with backward-compatible alias.
**Independent Test**: Both old and new import paths work. Deprecation warning on old path. `config.yaml` with `agents:` key loads.
**Prompt**: `tasks/WP06-toolconfig-rename.md`
**Estimated Size**: ~350 lines

### Included Subtasks

- [ ] T034 Create `src/specify_cli/orchestrator/tool_config.py` with renamed classes
- [ ] T035 Replace `agent_config.py` content with deprecation alias
- [ ] T036 Update imports in `agent_utils/directories.py`
- [ ] T037 [P] Update imports in `orchestrator/scheduler.py`, `monitor.py`, `config.py`
- [ ] T038 [P] Update imports in `cli/commands/init.py`, `agent/config.py`
- [ ] T039 [P] Update import in `upgrade/migrations/m_0_14_0_centralized_feature_detection.py`
- [ ] T040 Write tests in `tests/unit/specify_cli/orchestrator/test_tool_config.py`

### Dependencies

- None (independent — can start anytime).

---

## Work Package WP07: CLI Profile Commands (Priority: P2)

**Goal**: Implement `spec-kitty agents profile list|show|create|hierarchy` CLI commands.
**Independent Test**: Each CLI command produces formatted output. Profile creation writes to `.kittify/constitution/agents/`.
**Prompt**: `tasks/WP07-cli-profile-commands.md`
**Estimated Size**: ~400 lines

### Included Subtasks

- [ ] T041 Create `src/specify_cli/cli/commands/agents/profile.py` with Typer command group
- [ ] T042 [P] Implement `list` subcommand — Rich table
- [ ] T043 [P] Implement `show <profile_id>` subcommand
- [ ] T044 [P] Implement `create --from-template <profile_id>` subcommand
- [ ] T045 [P] Implement `hierarchy` subcommand — Rich Tree
- [ ] T046 [P] Implement `create --interactive` subcommand — prompt for each profile section (FR-5.5)
- [ ] T047 Register profile command group in CLI app
- [ ] T048 Write CLI tests (supporting tier — 55% coverage)

### Dependencies

- Depends on WP02.

---

## Work Package WP08: Curation Flow Compatibility (Priority: P1)

**Goal**: Validate curation pipeline supports `agent-profile` as target type. Document adaptation flow. Write end-to-end test.
**Independent Test**: ImportCandidate with `target_type: agent-profile` validates. Resulting artifact links to valid `.agent.yaml`.
**Prompt**: `tasks/WP08-curation-compatibility.md`
**Estimated Size**: ~350 lines

### Included Subtasks

- [ ] T048 Verify/update `agent-profile` in import-candidate schema target_type
- [ ] T049 Create example import candidate fixture for agent profile
- [ ] T050 Document `.agent.md` → `.agent.yaml` adaptation mapping in curation README — include section-to-YAML algorithm
- [ ] T051 Write end-to-end curation test in `tests/doctrine/test_curation_agent_profile.py`. Test scenarios: (1) round-trip conversion (.md → .yaml → validate → compare content fidelity), (2) ImportCandidate classification, (3) adoption flow
- [ ] T052 Validate `resulting_artifacts` linkage in test

### Dependencies

- Depends on WP01 and WP03.

---

## Work Package WP09: User Journey Documentation (Priority: P2)

**Goal**: Create a comprehensive UserJourney document describing the end-to-end flow of adding a new agent profile through the curation pipeline.
**Independent Test**: Journey document exists, covers all steps from ImportCandidate creation through adoption, includes example with Architect Alphonso or Python Pedro profile.
**Prompt**: `tasks/WP09-user-journey-curation.md`
**Estimated Size**: ~200 lines

### Included Subtasks

- [ ] T054 Create `kitty-specs/047-agent-profile-domain-model/user-journey-curation.md` document
- [ ] T055 Document step 1: Creating ImportCandidate for new agent profile (YAML structure, required fields)
- [ ] T056 Document step 2: Classification as `target_type: agent-profile` (validation rules, schema checks)
- [ ] T057 Document step 3: Adaptation from `.agent.md` to `.agent.yaml` (section mapping, field conversion)
- [ ] T058 Document step 4: Adoption into `src/doctrine/agent-profiles/shipped/` (file placement, naming conventions)
- [ ] T059 Document step 5: Verification (load via repository, schema validation, queryability)
- [ ] T060 Include complete example using a concrete profile (e.g., "Security Specialist" or "Data Engineer")
- [ ] T061 Add troubleshooting section (common errors, validation failures, recovery steps)

### Dependencies

- Depends on WP08 (curation flow must be implemented to document accurately).

---

## Dependency & Execution Summary

```
Wave 0 (foundation):
  WP01 (model) ─── no dependencies
  WP06 (ToolConfig) ─── no dependencies (independent)

Wave 1 (parallel after WP01):
  WP02 (repository) ─── depends on WP01
  WP03 (schema) ─── depends on WP01

Wave 2 (parallel after wave 1):
  WP04 (profiles) ─── depends on WP01, WP03
  WP05 (constitution) ─── depends on WP02
  WP07 (CLI) ─── depends on WP02
  WP08 (curation) ─── depends on WP01, WP03

Wave 3 (documentation):
  WP09 (user journey) ─── depends on WP08
```

**MVP Scope**: WP01 + WP02 + WP03 + WP04

**Critical path**: WP01 → WP02 → WP05

---

## Subtask Index

| ID | Summary | WP | P? |
|----|---------|----|----|
| T001 | Create agent-profiles `__init__.py` | WP01 | No |
| T002 | Define Role StrEnum | WP01 | No |
| T003 | Define value objects | WP01 | No |
| T004 | Define AgentProfile model | WP01 | No |
| T005 | Define TaskContext model | WP01 | No |
| T006 | Define RoleCapabilities | WP01 | Yes |
| T007 | Write model tests | WP01 | No |
| T008 | Implement repository with loading | WP02 | No |
| T009 | Implement field-level merge | WP02 | No |
| T010 | Implement query methods | WP02 | No |
| T011 | Implement hierarchy traversal | WP02 | No |
| T012 | Implement hierarchy validation | WP02 | No |
| T013 | Implement find_best_match with test scenarios | WP02 | No |
| T014 | Implement save/delete | WP02 | No |
| T015 | Write repository tests (incl. zero-profile, Alphonso/Pedro) | WP02 | No |
| T016 | Expand YAML schema | WP03 | No |
| T017 | Add validation utility | WP03 | No |
| T018 | Create test fixtures | WP03 | Yes |
| T018b | Test file extension validation (.agent.yaml) | WP03 | No |
| T019 | Write schema tests | WP03 | No |
| T020 | Create shipped/ directory | WP04 | No |
| T021-T026 | Create 7 reference profiles | WP04 | Yes |
| T027 | Write catalog test | WP04 | No |
| T028 | Remove AgentProfile from schemas.py | WP05 | No |
| T029 | Add doctrine import | WP05 | No |
| T030 | Update resolver.py | WP05 | No |
| T031 | Update GovernanceResolution | WP05 | No |
| T032 | Write resolver tests | WP05 | Yes |
| T033 | Write migration test | WP05 | Yes |
| T034 | Create tool_config.py | WP06 | No |
| T035 | Create deprecation alias | WP06 | No |
| T036-T039 | Update imports (7 files) | WP06 | Yes |
| T040 | Write ToolConfig tests | WP06 | No |
| T041 | Create CLI profile.py | WP07 | No |
| T042-T045 | Implement CLI subcommands | WP07 | Yes |
| T046 | Implement create --interactive (FR-5.5) | WP07 | Yes |
| T047 | Register command group | WP07 | No |
| T048 | Write CLI tests | WP07 | No |
| T049 | Verify agent-profile target_type | WP08 | No |
| T050 | Create import fixture | WP08 | Yes |
| T051 | Document adaptation in README (with algorithm) | WP08 | Yes |
| T052 | Write curation e2e test (incl. round-trip) | WP08 | No |
| T053 | Validate resulting_artifacts | WP08 | No |
| T054 | Create user-journey-curation.md | WP09 | No |
| T055 | Document step 1: Creating ImportCandidate | WP09 | Yes |
| T056 | Document step 2: Classification | WP09 | Yes |
| T057 | Document step 3: Adaptation (.md → .yaml) | WP09 | Yes |
| T058 | Document step 4: Adoption into shipped/ | WP09 | Yes |
| T059 | Document step 5: Verification | WP09 | Yes |
| T060 | Include complete concrete example | WP09 | Yes |
| T061 | Add troubleshooting section | WP09 | Yes |

<!-- status-model:start -->
## Canonical Status (Generated)
- WP01: for_review
- WP02: for_review
- WP03: for_review
<!-- status-model:end -->
