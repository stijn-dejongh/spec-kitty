# Work Packages: Doctrine Artifact Domain Models

**Inputs**: Design documents from `kitty-specs/046-doctrine-artifact-domain-models/`
**Prerequisites**: plan.md (required), spec.md (user stories), research.md, data-model.md, quickstart.md
**Organization**: Fine-grained subtasks (`Txxx`) roll up into work packages (`WPxx`). Each work package must be independently deliverable and testable. All WPs follow ATDD/TDD methodology.

---

## Work Package WP01: Directive Model & Repository (Priority: P1)

**Goal**: Create the `Directive` Pydantic model, `DirectiveRepository`, and schema validation for directives. Move existing directive YAML files into `shipped/` subdirectory. This is the most complex artifact type (enrichment fields, ID normalization).
**Independent Test**: `DirectiveRepository().list_all()` returns all shipped directives as `Directive` objects; `get("004")` normalizes to `DIRECTIVE_004`.
**Prompt**: `tasks/WP01-directive-model-and-repository.md`
**Estimated size**: ~450 lines

### Included Subtasks

- [ ] T001 Create `src/doctrine/directives/__init__.py` with public exports
- [ ] T002 Create `src/doctrine/directives/models.py` with `Directive`, `Enforcement` enum
- [ ] T003 Create `src/doctrine/directives/repository.py` with `DirectiveRepository`
- [ ] T004 Create `src/doctrine/directives/validation.py` with schema validation utility
- [ ] T005 Move directive YAML files into `src/doctrine/directives/shipped/`
- [ ] T006 Write ATDD/TDD tests in `tests/doctrine/directives/`

### Implementation Notes

- Follow `agent_profiles` pattern exactly for repository structure
- `DirectiveRepository.get()` must accept both `"004"` and `"DIRECTIVE_004"` and normalize
- Use `Draft202012Validator` (not Draft7) per research.md R-005
- Move existing `.directive.yaml` files into `shipped/` subdirectory
- Update `README.md` in `src/doctrine/directives/` to reflect subpackage status

### Dependencies

- None (starting package)

### Risks & Mitigations

- Moving YAML files may break existing `test_schema_validation.py` → update test paths in WP10

---

## Work Package WP02: Tactic Model & Repository (Priority: P1)

**Goal**: Create the `Tactic`, `TacticStep`, `TacticReference` Pydantic models and `TacticRepository`. Move tactic YAML files into `shipped/`.
**Independent Test**: `TacticRepository().get("zombies-tdd")` returns a `Tactic` with 7 steps.
**Prompt**: `tasks/WP02-tactic-model-and-repository.md`
**Estimated size**: ~400 lines

### Included Subtasks

- [ ] T007 Create `src/doctrine/tactics/__init__.py` with public exports
- [ ] T008 Create `src/doctrine/tactics/models.py` with `Tactic`, `TacticStep`, `TacticReference`, `ReferenceType` enum
- [ ] T009 Create `src/doctrine/tactics/repository.py` with `TacticRepository`
- [ ] T010 Create `src/doctrine/tactics/validation.py` with schema validation utility
- [ ] T011 Move tactic YAML files into `src/doctrine/tactics/shipped/`
- [ ] T012 Write ATDD/TDD tests in `tests/doctrine/tactics/`

### Implementation Notes

- `TacticStep` has optional `description`, `examples`, and `references` fields
- `TacticReference` has `name`, `type` (enum), `id`, `when` — all required per schema
- Schema uses `$defs` for reference objects; model `references` field at both tactic and step level

### Dependencies

- None (parallel with WP01)

---

## Work Package WP03: Styleguide Model & Repository (Priority: P1)

**Goal**: Create `Styleguide`, `AntiPattern` models and `StyleguideRepository`. Move styleguide YAML files into `shipped/`.
**Independent Test**: `StyleguideRepository().get("kitty-glossary-writing")` returns a `Styleguide` with `scope == "glossary"`.
**Prompt**: `tasks/WP03-styleguide-model-and-repository.md`
**Estimated size**: ~350 lines

### Included Subtasks

- [ ] T013 Create `src/doctrine/styleguides/__init__.py` with public exports
- [ ] T014 Create `src/doctrine/styleguides/models.py` with `Styleguide`, `AntiPattern`, `StyleguideScope` enum
- [ ] T015 Create `src/doctrine/styleguides/repository.py` with `StyleguideRepository`
- [ ] T016 Create `src/doctrine/styleguides/validation.py` with schema validation utility
- [ ] T017 Move styleguide YAML files into `src/doctrine/styleguides/shipped/` (including `writing/` subdirectory)
- [ ] T018 Write ATDD/TDD tests in `tests/doctrine/styleguides/`

### Implementation Notes

- `writing/kitty-glossary-writing.styleguide.yaml` lives in a subdirectory — repository must scan recursively or use `**/*.styleguide.yaml`
- `AntiPattern` has 4 required fields: `name`, `description`, `bad_example`, `good_example`
- `Scope` enum: `code | docs | architecture | testing | operations | glossary`

### Dependencies

- None (parallel with WP01, WP02)

---

## Work Package WP04: Toolguide & Paradigm Models (Priority: P1)

**Goal**: Create `Toolguide` and `Paradigm` models with repositories. These are the simplest artifact types.
**Independent Test**: `ToolguideRepository().get("powershell-syntax")` returns a `Toolguide`; `ParadigmRepository().get("test-first")` returns a `Paradigm`.
**Prompt**: `tasks/WP04-toolguide-and-paradigm-models.md`
**Estimated size**: ~400 lines

### Included Subtasks

- [ ] T019 Create `src/doctrine/toolguides/__init__.py`, `models.py`, `repository.py`, `validation.py`
- [ ] T020 Move toolguide YAML and companion MD files into `src/doctrine/toolguides/shipped/`
- [ ] T021 Create `src/doctrine/paradigms/__init__.py`, `models.py`, `repository.py`, `validation.py`
- [ ] T022 Create `src/doctrine/schemas/paradigm.schema.yaml` (new schema)
- [ ] T023 Move paradigm YAML files into `src/doctrine/paradigms/shipped/`
- [ ] T024 Write ATDD/TDD tests in `tests/doctrine/toolguides/` and `tests/doctrine/paradigms/`

### Implementation Notes

- Toolguide `guide_path` pattern: `^src/doctrine/.+\.md$` — companion markdown files move into `shipped/` too
- Paradigm schema is new (DD-003): `schema_version`, `id`, `name`, `summary` — all required
- Both are simple models with no nested value objects

### Dependencies

- None (parallel with WP01-WP03)

---

## Work Package WP05: Directive Schema Extension (Priority: P1)

**Goal**: Extend `directive.schema.yaml` with optional enrichment fields (`scope`, `procedures`, `integrity_rules`, `validation_criteria`) while maintaining backward compatibility.
**Independent Test**: Both minimal `test-first.directive.yaml` and an enriched test directive validate against the updated schema.
**Prompt**: `tasks/WP05-directive-schema-extension.md`
**Estimated size**: ~250 lines

### Included Subtasks

- [ ] T025 Update `src/doctrine/schemas/directive.schema.yaml` with optional enrichment fields
- [ ] T026 Update `Directive` model in `src/doctrine/directives/models.py` to include enrichment fields
- [ ] T027 Write backward-compatibility tests (minimal format still validates)
- [ ] T028 Write enriched-format tests (new fields validate correctly)

### Implementation Notes

- All new fields are optional: `scope` (string), `procedures` (array of strings), `integrity_rules` (array of strings), `validation_criteria` (array of strings)
- Use YAML keys with underscores per existing schema convention (not kebab-case for these fields — match `tactic_refs` pattern)
- `additionalProperties: false` must be removed or updated to allow new fields
- Existing minimal directives must continue to validate unchanged

### Dependencies

- Depends on WP01 (Directive model must exist before extending it)

---

## Work Package WP06: DoctrineService (Priority: P1)

**Goal**: Create `DoctrineService` as the lazy aggregation point that holds references to all repositories.
**Independent Test**: `DoctrineService().directives.list_all()` returns directives; `service.agent_profiles.get("implementer")` reuses existing `AgentProfileRepository`.
**Prompt**: `tasks/WP06-doctrine-service.md`
**Estimated size**: ~300 lines

### Included Subtasks

- [ ] T029 Create `src/doctrine/service.py` with `DoctrineService` class
- [ ] T030 Update `src/doctrine/__init__.py` to export `DoctrineService`
- [ ] T031 Write ATDD/TDD tests in `tests/doctrine/test_service.py`

### Implementation Notes

- Lazy initialization: repositories instantiated on first attribute access (use `@property` with `_cache` dict or `functools.cached_property`)
- Constructor: `DoctrineService(shipped_root: Path | None = None, project_root: Path | None = None)`
- Must reuse existing `AgentProfileRepository` (FR-016)
- Each repository's `shipped_dir` derived from `shipped_root / <artifact_type> / shipped`
- Each repository's `project_dir` derived from `project_root / <artifact_type>`

### Dependencies

- Depends on WP01, WP02, WP03, WP04 (all repositories must exist)

---

## Work Package WP07: Enrich Existing Directives 001-010 (Priority: P2)

**Goal**: Enrich shipped directives 001-010 with substantive content (scope, procedures, integrity_rules, validation_criteria, populated tactic_refs).
**Independent Test**: Loading directive 004 returns a `Directive` with non-empty `scope`, `procedures`, and `tactic_refs` fields.
**Prompt**: `tasks/WP07-enrich-directives-001-010.md`
**Estimated size**: ~500 lines

### Included Subtasks

- [ ] T032 Enrich 001-architectural-integrity-standard
- [ ] T033 Enrich 002-accessibility-first-principle
- [ ] T034 Enrich 003-decision-documentation-requirement (incorporate doctrine_ref/018 traceable decisions)
- [ ] T035 Enrich 004-test-driven-implementation-standard (incorporate doctrine_ref/016 ATDD + 017 TDD)
- [ ] T036 Enrich 005-design-system-consistency-standard
- [ ] T037 Enrich 006-coding-standards-adherence
- [ ] T038 Enrich 007-scalability-assessment-protocol
- [ ] T039 Enrich 008-security-review-protocol
- [ ] T040 Enrich 009-user-centered-validation-requirement
- [ ] T041 Enrich 010-specification-fidelity-requirement (incorporate doctrine_ref/034 spec-driven dev)

### Implementation Notes

- Use `doctrine_ref/directives/` as reference material — adapt content, don't copy verbatim
- Each directive must have: expanded `intent` (>1 sentence), `scope`, at least `procedures` or `validation_criteria`
- Wire `tactic_refs` to existing tactics where applicable (e.g., 004 → acceptance-test-first, tdd-red-green-refactor, zombies-tdd)
- Maintain `enforcement` values unchanged
- All enriched files must validate against updated schema (WP05)

### Dependencies

- Depends on WP05 (schema must support enrichment fields)
- Depends on WP01 (YAML files must be in `shipped/` directory)

---

## Work Package WP08: Enrich Existing Directives 011-019 + test-first (Priority: P2)

**Goal**: Enrich shipped directives 011-019 and `test-first` with substantive content.
**Independent Test**: Loading any directive returns non-stub content; all directives validate against schema.
**Prompt**: `tasks/WP08-enrich-directives-011-019.md`
**Estimated size**: ~450 lines

### Included Subtasks

- [ ] T042 Enrich 011-feedback-clarity-standard
- [ ] T043 Enrich 012-work-package-granularity-standard
- [ ] T044 Enrich 013-dependency-validation-requirement
- [ ] T045 Enrich 014-acceptance-criteria-completeness
- [ ] T046 Enrich 015-research-time-boxing-requirement
- [ ] T047 Enrich 016-finding-documentation-standard
- [ ] T048 Enrich 017-glossary-integrity-standard
- [ ] T049 Enrich 018-doctrine-versioning-requirement
- [ ] T050 Enrich 019-documentation-gap-prioritization
- [ ] T051 Verify test-first.directive.yaml enrichment (already has tactic_refs; add scope/procedures)

### Implementation Notes

- Same enrichment approach as WP07
- Directive 017 already links to glossary-related tactics/styleguides; expand those references
- `test-first.directive.yaml` already has populated `tactic_refs` — add `scope` and `procedures` only

### Dependencies

- Depends on WP05 (schema must support enrichment fields)
- Depends on WP01 (YAML files must be in `shipped/` directory)

### Parallel Opportunities

- WP07 and WP08 can run in parallel (different directive files, no overlap)

---

## Work Package WP09: Create New Shipped Directives (Priority: P2)

**Goal**: Create new shipped directives (020-026) for `doctrine_ref` concepts not yet represented.
**Independent Test**: `DirectiveRepository().list_all()` returns 27+ directives (19 existing + `test-first` + 7 new).
**Prompt**: `tasks/WP09-create-new-directives.md`
**Estimated size**: ~500 lines

### Included Subtasks

- [ ] T052 Create 020-worklog-creation.directive.yaml (from doctrine_ref/014)
- [ ] T053 Create 021-prompt-storage.directive.yaml (from doctrine_ref/015)
- [ ] T054 Create 022-commit-protocol.directive.yaml (from doctrine_ref/026)
- [ ] T055 Create 023-clarification-before-execution.directive.yaml (from doctrine_ref/023)
- [ ] T056 Create 024-locality-of-change.directive.yaml (from doctrine_ref/021)
- [ ] T057 Create 025-boy-scout-rule.directive.yaml (from doctrine_ref/036)
- [ ] T058 Create 026-hic-escalation-protocol.directive.yaml (from doctrine_ref/040)

### Implementation Notes

- Each new directive uses the enriched format from the start (scope, procedures, integrity_rules, validation_criteria)
- Adapt `doctrine_ref` content to fit YAML schema; strip markdown formatting, convert to structured fields
- Wire `tactic_refs` where applicable — may require creating new tactics (see WP11)
- IDs follow pattern: `DIRECTIVE_020`, `DIRECTIVE_021`, etc.
- Files placed in `src/doctrine/directives/shipped/`

### Dependencies

- Depends on WP05 (schema must support enrichment fields)
- Depends on WP01 (repository must exist to validate)

### Parallel Opportunities

- Can run parallel with WP07, WP08 (different files)

---

## Work Package WP10: Consistency Tests & Existing Test Updates (Priority: P2)

**Goal**: Create cross-artifact consistency tests; update existing tests broken by file relocation.
**Independent Test**: `pytest tests/doctrine/test_consistency.py` passes; every `tactic_ref` in every shipped directive resolves to an existing tactic.
**Prompt**: `tasks/WP10-consistency-tests.md`
**Estimated size**: ~350 lines

### Included Subtasks

- [ ] T059 Create `tests/doctrine/test_consistency.py` — cross-artifact reference integrity
- [ ] T060 Create `tests/doctrine/test_enriched_directives.py` — enriched content validation
- [ ] T061 Update `tests/doctrine/test_schema_validation.py` for new file paths
- [ ] T062 Update `tests/doctrine/test_artifact_compliance.py` for new file paths
- [ ] T063 Verify all existing doctrine tests pass with relocated files

### Implementation Notes

- Consistency test: scan all shipped directives, extract `tactic_refs`, verify each resolves to a tactic file
- Enriched directive test: verify no shipped directive has single-sentence `intent`, all have `scope` field
- Update path references in existing tests from `src/doctrine/directives/*.yaml` to `src/doctrine/directives/shipped/*.yaml`

### Dependencies

- Depends on WP01-WP04 (file relocation must be complete)
- Depends on WP07, WP08, WP09 (enriched directives must exist)

---

## Work Package WP11: New Tactics & Supporting Artifacts (Priority: P3)

**Goal**: Create new tactic, styleguide, or toolguide YAML files where directive enrichment or new directives reference operational patterns not yet captured.
**Independent Test**: Every `tactic_ref` in every shipped directive resolves to a tactic file in `src/doctrine/tactics/shipped/`.
**Prompt**: `tasks/WP11-new-tactics-and-supporting-artifacts.md`
**Estimated size**: ~400 lines

### Included Subtasks

- [ ] T064 Audit all enriched and new directives for unresolved `tactic_refs`
- [ ] T065 [P] Create new tactic YAML files in `src/doctrine/tactics/shipped/` for unresolved references
- [ ] T066 [P] Create new styleguide YAML files in `src/doctrine/styleguides/shipped/` if needed
- [ ] T067 [P] Create new toolguide YAML files in `src/doctrine/toolguides/shipped/` if needed
- [ ] T068 Validate all new artifacts against their respective schemas

### Implementation Notes

- Audit output from WP07/WP08/WP09 drives this WP
- New tactics follow `doctrine_ref/tactics/` as reference material — adapt to existing tactic schema
- Minimum viable tactic: `schema_version`, `id`, `name`, `steps` (at least 1 step)
- Only create artifacts that are actually referenced by a directive — don't speculatively create unused artifacts

### Dependencies

- Depends on WP07, WP08, WP09 (enriched directives must be finalized to know which refs are needed)
- Depends on WP02, WP03, WP04 (repositories must exist for validation)

---

## Dependency & Execution Summary

```
Phase 1 (Foundation - parallel):
  WP01 ─┐
  WP02 ─┤
  WP03 ─┼──→ WP06 (DoctrineService, needs all repos)
  WP04 ─┘
  WP05 ────→ (depends on WP01)

Phase 2 (Content - parallel after WP05):
  WP07 ─┐
  WP08 ─┼──→ WP10 (Consistency tests, needs enriched content)
  WP09 ─┘──→ WP11 (New tactics, needs directive audit)

Execution order:
  [WP01, WP02, WP03, WP04] → [WP05, WP06] → [WP07, WP08, WP09] → [WP10, WP11]
```

- **Parallelization**: WP01-WP04 can all run simultaneously. WP07-WP09 can run simultaneously.
- **MVP Scope**: WP01-WP06 deliver the core domain models, repositories, and service (User Stories 1-4, 6).
- **Content Scope**: WP07-WP11 deliver directive enrichment and consistency (User Stories 5, 7).

---

## Subtask Index (Reference)

| Subtask | Summary | WP |
|---------|---------|-----|
| T001 | Create `directives/__init__.py` | WP01 |
| T002 | Create `directives/models.py` (Directive, Enforcement) | WP01 |
| T003 | Create `directives/repository.py` (DirectiveRepository) | WP01 |
| T004 | Create `directives/validation.py` | WP01 |
| T005 | Move directive YAML files into `shipped/` | WP01 |
| T006 | Write ATDD/TDD tests for directives | WP01 |
| T007 | Create `tactics/__init__.py` | WP02 |
| T008 | Create `tactics/models.py` (Tactic, TacticStep, TacticReference) | WP02 |
| T009 | Create `tactics/repository.py` (TacticRepository) | WP02 |
| T010 | Create `tactics/validation.py` | WP02 |
| T011 | Move tactic YAML files into `shipped/` | WP02 |
| T012 | Write ATDD/TDD tests for tactics | WP02 |
| T013 | Create `styleguides/__init__.py` | WP03 |
| T014 | Create `styleguides/models.py` (Styleguide, AntiPattern, StyleguideScope) | WP03 |
| T015 | Create `styleguides/repository.py` (StyleguideRepository) | WP03 |
| T016 | Create `styleguides/validation.py` | WP03 |
| T017 | Move styleguide YAML files into `shipped/` | WP03 |
| T018 | Write ATDD/TDD tests for styleguides | WP03 |
| T019 | Create `toolguides/__init__.py`, `models.py`, `repository.py`, `validation.py` | WP04 |
| T020 | Move toolguide YAML + companion MD into `shipped/` | WP04 |
| T021 | Create `paradigms/__init__.py`, `models.py`, `repository.py`, `validation.py` | WP04 |
| T022 | Create `paradigm.schema.yaml` | WP04 |
| T023 | Move paradigm YAML files into `shipped/` | WP04 |
| T024 | Write ATDD/TDD tests for toolguides and paradigms | WP04 |
| T025 | Update `directive.schema.yaml` with enrichment fields | WP05 |
| T026 | Update Directive model with enrichment fields | WP05 |
| T027 | Write backward-compatibility tests | WP05 |
| T028 | Write enriched-format tests | WP05 |
| T029 | Create `service.py` with DoctrineService | WP06 |
| T030 | Update `doctrine/__init__.py` exports | WP06 |
| T031 | Write ATDD/TDD tests for DoctrineService | WP06 |
| T032 | Enrich directive 001 | WP07 |
| T033 | Enrich directive 002 | WP07 |
| T034 | Enrich directive 003 | WP07 |
| T035 | Enrich directive 004 | WP07 |
| T036 | Enrich directive 005 | WP07 |
| T037 | Enrich directive 006 | WP07 |
| T038 | Enrich directive 007 | WP07 |
| T039 | Enrich directive 008 | WP07 |
| T040 | Enrich directive 009 | WP07 |
| T041 | Enrich directive 010 | WP07 |
| T042 | Enrich directive 011 | WP08 |
| T043 | Enrich directive 012 | WP08 |
| T044 | Enrich directive 013 | WP08 |
| T045 | Enrich directive 014 | WP08 |
| T046 | Enrich directive 015 | WP08 |
| T047 | Enrich directive 016 | WP08 |
| T048 | Enrich directive 017 | WP08 |
| T049 | Enrich directive 018 | WP08 |
| T050 | Enrich directive 019 | WP08 |
| T051 | Verify test-first directive enrichment | WP08 |
| T052 | Create directive 020 (worklog creation) | WP09 |
| T053 | Create directive 021 (prompt storage) | WP09 |
| T054 | Create directive 022 (commit protocol) | WP09 |
| T055 | Create directive 023 (clarification before execution) | WP09 |
| T056 | Create directive 024 (locality of change) | WP09 |
| T057 | Create directive 025 (boy scout rule) | WP09 |
| T058 | Create directive 026 (HiC escalation protocol) | WP09 |
| T059 | Create `test_consistency.py` | WP10 |
| T060 | Create `test_enriched_directives.py` | WP10 |
| T061 | Update `test_schema_validation.py` paths | WP10 |
| T062 | Update `test_artifact_compliance.py` paths | WP10 |
| T063 | Verify all existing tests pass | WP10 |
| T064 | Audit directives for unresolved tactic_refs | WP11 |
| T065 | Create new tactic YAML files | WP11 |
| T066 | Create new styleguide YAML files | WP11 |
| T067 | Create new toolguide YAML files | WP11 |
| T068 | Validate all new artifacts against schemas | WP11 |