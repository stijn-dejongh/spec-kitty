# Work Packages: Rename Constitution to Charter

**Inputs**: Design documents from `kitty-specs/063-rename-constitution-to-charter/`
**Prerequisites**: plan.md (required), spec.md (user stories), research.md, data-model.md, quickstart.md

**Tests**: Included as verification steps within each WP — the rename is behavior-preserving, so all existing tests must pass after each stage.

**Organization**: Fine-grained subtasks (`Txxx`) roll up into work packages (`WPxx`). Each work package is independently deliverable and testable.

**Prompt Files**: Each work package references a matching prompt file in `tasks/`.

## Subtask Format: `[Txxx] [P?] Description`

- **[P]** indicates the subtask can proceed in parallel (different files/components).
- Include precise file paths or modules.

---

## Work Package WP01: Rename Doctrine Constitution Layer (Priority: P0)

**Goal**: Rename `src/doctrine/constitution/` → `src/doctrine/charter/` and update all imports.
**Independent Test**: `ruff check src/doctrine/` passes, no broken imports referencing `doctrine.constitution`.
**Prompt**: `tasks/WP01-rename-doctrine-constitution.md`
**Requirement Refs**: FR-001, C-001
**Agent Profile**: python-implementer
**Estimated Size**: ~250 lines

### Included Subtasks

- [ ] T001 `git mv src/doctrine/constitution/ src/doctrine/charter/`
- [ ] T002 Update all imports referencing `doctrine.constitution` across `src/`
- [ ] T003 Update all imports referencing `doctrine.constitution` across `tests/`
- [ ] T004 Run `ruff check src/doctrine/` and `pytest` for affected tests
- [ ] T005 Commit stage 1

### Implementation Notes

- The doctrine constitution directory contains only `defaults.yaml`.
- Imports may appear in constitution compiler, context, and CLI modules.
- This is the smallest stage — establishes the rename pattern for subsequent WPs.

### Parallel Opportunities

- T002 and T003 can proceed in parallel (different directories).

### Dependencies

- None (starting package).

### Risks & Mitigations

- Hidden transitive imports through `__init__.py` re-exports → grep exhaustively before committing.

---

## Work Package WP02: Rename Core Constitution Library (Priority: P0)

**Goal**: Rename `src/constitution/` → `src/charter/` with all classes, functions, and imports updated.
**Independent Test**: `pytest tests/constitution/` passes (after updating test imports), `ruff check src/charter/` clean.
**Prompt**: `tasks/WP02-rename-core-library.md`
**Requirement Refs**: FR-001, FR-002, FR-003
**Agent Profile**: python-implementer
**Estimated Size**: ~500 lines

### Included Subtasks

- [ ] T006 `git mv src/constitution/ src/charter/`
- [ ] T007 Rename all 9 classes: CompiledConstitution → CompiledCharter, ConstitutionReference → CharterReference, ConstitutionContextResult → CharterContextResult, ConstitutionDraft → CharterDraft, ConstitutionInterview → CharterInterview, ConstitutionSection → CharterSection, ConstitutionParser → CharterParser, ConstitutionTestingConfig → CharterTestingConfig, ConstitutionTemplateResolver → CharterTemplateResolver
- [ ] T008 Rename all functions: build_constitution_context → build_charter_context, build_constitution_draft → build_charter_draft, write_constitution → write_charter, sync_constitution → sync_charter, etc.
- [ ] T009 Update all `from constitution.` / `import constitution.` across `src/` (excluding migrations)
- [ ] T010 Update all `from constitution.` / `import constitution.` across `tests/` (test files that import core lib)
- [ ] T011 Run `ruff check src/charter/` + `pytest tests/constitution/` + verify no remaining `from constitution.` imports in active code
- [ ] T012 Commit stage 2

### Implementation Notes

- This is the largest single rename stage (~3,253 lines of source).
- The `src/constitution/` package has 14 Python files with 9 classes and multiple functions.
- Use `replace_all` for mechanical class/function renames within each file.
- After directory mv, update `__init__.py` re-exports if they reference module name in strings.

### Parallel Opportunities

- T007 and T008 within the same files — do together per-file.
- T009 and T010 can proceed in parallel (different directories).

### Dependencies

- Depends on WP01 (doctrine layer imports may reference core lib).

### Risks & Mitigations

- String references (e.g., in error messages, log statements) may reference "constitution" → search for string literals too.
- `__init__.py` `__all__` exports may reference old class names → update explicitly.

---

## Work Package WP03: Rename Specify CLI Constitution Module (Priority: P0)

**Goal**: Rename `src/specify_cli/constitution/` → `src/specify_cli/charter/` with all classes and imports.
**Independent Test**: `pytest tests/specify_cli/` passes, `ruff check src/specify_cli/charter/` clean.
**Prompt**: `tasks/WP03-rename-specify-cli-module.md`
**Requirement Refs**: FR-001, FR-002, FR-003
**Agent Profile**: python-implementer
**Estimated Size**: ~450 lines

### Included Subtasks

- [ ] T013 `git mv src/specify_cli/constitution/ src/specify_cli/charter/`
- [ ] T014 Rename all classes mirroring WP02: ConstitutionReference → CharterReference, CompiledConstitution → CompiledCharter, etc. (8 classes in specify_cli layer)
- [ ] T015 Rename functions: resolve, compile, sync functions with constitution in name
- [ ] T016 Update all `from specify_cli.constitution.` / `import specify_cli.constitution.` across `src/` (excluding migrations)
- [ ] T017 Update all test imports in `tests/specify_cli/` referencing the old module path
- [ ] T018 Run `ruff check src/specify_cli/charter/` + `pytest tests/specify_cli/` + verify
- [ ] T019 Commit stage 3

### Implementation Notes

- The specify_cli constitution module (12 files, ~2,928 lines) mirrors the core lib structure.
- This module wraps the core lib for CLI consumption.
- Many files import from both `constitution.` (core) and `specify_cli.constitution.` — after WP02 the core imports already point to `charter.`.

### Parallel Opportunities

- T014 and T015 within the same files — do together per-file.

### Dependencies

- Depends on WP02 (this module imports from core lib, which must already be renamed).

### Risks & Mitigations

- Cross-layer imports: some specify_cli modules may import directly from core `charter.*` (post-WP02) — verify these resolve.

---

## Work Package WP04: CLI Registration, Deprecation Alias, and Dashboard (Priority: P1)

**Goal**: Rename CLI command `constitution` → `charter`, add deprecation alias, update shim, dashboard, and agent workflow.
**Independent Test**: `spec-kitty charter --help` works, `spec-kitty constitution --help` works + emits deprecation warning.
**Prompt**: `tasks/WP04-cli-registration-deprecation.md`
**Requirement Refs**: FR-004, FR-005
**Agent Profile**: python-implementer
**Estimated Size**: ~450 lines

### Included Subtasks

- [ ] T020 `git mv src/specify_cli/cli/commands/constitution.py src/specify_cli/cli/commands/charter.py` — rename file, update internal Typer app name to `"charter"`
- [ ] T021 Update `src/specify_cli/cli/commands/__init__.py` — change import and `app.add_typer()` registration from `constitution` to `charter`
- [ ] T022 Add deprecation alias: register a thin `constitution` Typer group that emits `DeprecationWarning` to stderr then delegates to `charter`
- [ ] T023 Update `src/specify_cli/cli/commands/shim.py` — rename shim entry from `constitution` to `charter`
- [ ] T024 `git mv src/specify_cli/dashboard/constitution_path.py src/specify_cli/dashboard/charter_path.py` — rename function `resolve_project_constitution_path` → `resolve_project_charter_path`
- [ ] T025 Update `src/specify_cli/cli/commands/agent/workflow.py` — rename `_render_constitution_context` → `_render_charter_context`
- [ ] T026 Update all imports and references in dashboard, agent, and CLI test files
- [ ] T027 Run CLI smoke test + `pytest tests/specify_cli/cli/` + `pytest tests/agent/`
- [ ] T028 Commit stage 4

### Implementation Notes

- The deprecation alias uses Typer's callback mechanism to print a warning before delegating.
- The shim in `shim.py` dispatches `constitution` as a consumer skill — update to `charter`.
- The dashboard `constitution_path.py` has `resolve_project_constitution_path()` used by the dashboard API.

### Parallel Opportunities

- T020-T023 (CLI) and T024-T025 (dashboard/agent) can proceed in parallel.

### Dependencies

- Depends on WP03 (CLI commands import from specify_cli.charter module).

### Risks & Mitigations

- Deprecation warning format: use `warnings.warn()` with `DeprecationWarning` category so it can be filtered by users.
- Test assertions may check for "constitution" in CLI output — update those assertions.

---

## Work Package WP05: Templates and Skills Rename (Priority: P1)

**Goal**: Rename command templates and skill directory from constitution to charter terminology.
**Independent Test**: Template cleanliness tests pass, skill files reference `charter` consistently.
**Prompt**: `tasks/WP05-templates-skills-rename.md`
**Requirement Refs**: FR-007, FR-008
**Agent Profile**: python-implementer
**Estimated Size**: ~400 lines

### Included Subtasks

- [ ] T029 `git mv src/specify_cli/missions/software-dev/command-templates/constitution.md src/specify_cli/missions/software-dev/command-templates/charter.md` — update content references inside the file
- [ ] T030 Update constitution references in 7 other template files (specify.md, plan.md, analyze.md, task-prompt-template.md across software-dev, documentation, and research missions)
- [ ] T031 `git mv src/doctrine/skills/spec-kitty-constitution-doctrine/ src/doctrine/skills/spec-kitty-charter-doctrine/`
- [ ] T032 Update content in SKILL.md and reference files within the skill directory — replace all `constitution` references with `charter`
- [ ] T033 Update any migration code or template registry that references the old skill name
- [ ] T034 Run template cleanliness tests + verify skill loading
- [ ] T035 Commit stage 5

### Implementation Notes

- Template files are Markdown with embedded bash commands and path references.
- Search for `.kittify/constitution/`, `constitution.md`, `spec-kitty constitution`, `constitution context`, etc.
- The skill SKILL.md is ~600 lines — substantial text replacement needed.

### Parallel Opportunities

- T029-T030 (templates) and T031-T033 (skills) can proceed in parallel.

### Dependencies

- Depends on WP04 (templates reference CLI commands which must already be renamed).

### Risks & Mitigations

- Templates are deployed to user projects via migrations — the migration in WP07 handles user-side template updates.
- Skill references in `.claude/skills/` are generated copies — they'll be updated via upgrade, not here.

---

## Work Package WP06: Glossary, Architecture Docs, and User Docs (Priority: P2)

**Goal**: Update glossary canonical terms, architecture docs, and user documentation to use `charter` terminology.
**Independent Test**: `grep -ri "constitution" docs/ architecture/ src/specify_cli/.contextive/ | grep -v _reference | grep -v curation` returns zero hits on active content.
**Prompt**: `tasks/WP06-glossary-docs-update.md`
**Requirement Refs**: FR-009, FR-010, NFR-002
**Agent Profile**: curator
**Estimated Size**: ~400 lines

### Included Subtasks

- [ ] T036 Update 3 glossary entries in `src/specify_cli/.contextive/governance.yml`: Constitution Compiler → Charter Compiler, Constitution Interview → Charter Interview, Constitution Validation → Charter Validation
- [ ] T037 [P] Update ~25 architecture files in `architecture/` — replace `constitution` with `charter` in active content (preserve historical context where appropriate)
- [ ] T038 [P] Update ~23 documentation files in `docs/` — replace `constitution` with `charter`
- [ ] T039 Update the plan template `Constitution Check` section heading if referenced generically
- [ ] T040 Run verification grep to confirm zero stale references in active docs
- [ ] T041 Commit stage 6

### Implementation Notes

- Use targeted text replacement — not blind find/replace. Some architectural docs may reference "constitution" in historical context or quotes.
- The glossary in `governance.yml` uses YAML structure — update term names and descriptions carefully.
- Architecture ADRs that describe past decisions about the constitution system should update terminology to charter but may keep historical notes about the rename itself.

### Parallel Opportunities

- T037 and T038 can proceed in parallel (different directories).

### Dependencies

- Depends on WP05 (template content references should already be updated).

### Risks & Mitigations

- Over-zealous replacement in historical context → review each file for context before replacing.
- YAML formatting in governance.yml → use ruamel.yaml-safe editing or careful manual edits.

---

## Work Package WP07: User-Project Migration (Priority: P2)

**Goal**: Create upgrade migration that renames `.kittify/constitution/` → `.kittify/charter/` in user projects.
**Independent Test**: Migration unit tests pass for: fresh project (no-op), project with constitution dir (renamed), project with both dirs (warning).
**Prompt**: `tasks/WP07-user-project-migration.md`
**Requirement Refs**: FR-006
**Agent Profile**: python-implementer
**Estimated Size**: ~350 lines

### Included Subtasks

- [ ] T042 Create new migration file in `src/specify_cli/upgrade/migrations/` following existing naming convention
- [ ] T043 Implement migration logic: rename `.kittify/constitution/` → `.kittify/charter/`, handle edge cases (both exist → warn, neither exists → no-op)
- [ ] T044 Register migration in the migration sequence
- [ ] T045 Write unit tests for the migration: happy path, no-op, conflict case
- [ ] T046 Run `pytest tests/specify_cli/upgrade/` to verify
- [ ] T047 Commit stage 7

### Implementation Notes

- Follow existing migration patterns (see `src/specify_cli/upgrade/migrations/` for examples).
- Use `pathlib.Path.rename()` for the directory move.
- Edge case: if `.kittify/charter/` already exists AND `.kittify/constitution/` exists, emit a warning and skip (don't overwrite).
- Migration must be idempotent — running it twice is safe.

### Parallel Opportunities

- None — single cohesive unit.

### Dependencies

- Depends on WP04 (kernel path functions must already point to `charter/`).

### Risks & Mitigations

- Data loss if both directories exist → detect and warn, never overwrite.
- Windows path handling → use `pathlib` exclusively.

---

## Work Package WP08: Cleanup — Paradigm, CLI Subcommand, Test Renames (Priority: P3)

**Goal**: Move misplaced paradigm file, rename `create-feature` → `create-mission`, rename test directories, final acceptance sweep.
**Independent Test**: `test-first` paradigm discoverable, `spec-kitty agent mission create-mission --help` works, full test suite green, NFR-001 and NFR-002 acceptance greps pass.
**Prompt**: `tasks/WP08-cleanup-final-sweep.md`
**Requirement Refs**: FR-011, FR-012, FR-013, NFR-001, NFR-002, NFR-003
**Agent Profile**: python-implementer
**Estimated Size**: ~450 lines

### Included Subtasks

- [ ] T048 `git mv src/doctrine/paradigms/test-first.paradigm.yaml src/doctrine/paradigms/shipped/test-first.paradigm.yaml`
- [ ] T049 Verify paradigm repository discovers `test-first` after relocation
- [ ] T050 Rename `create-feature` → `create-mission` in `src/specify_cli/cli/commands/agent/feature.py` (command decorator name)
- [ ] T051 Update any references to `create-feature` in templates, docs, and tests
- [ ] T052 Rename `tests/constitution/` → `tests/charter/` and update all internal imports
- [ ] T053 Update scattered test files (~30 files) that reference `constitution` in imports or assertions
- [ ] T054 Audit doctrine directories for other misplaced files (FR-012)
- [ ] T055 Run full test suite: `pytest tests/`
- [ ] T056 Run acceptance greps: NFR-001 (`grep -ri "constitution" src/ --include="*.py" | grep -v upgrade/migrations | grep -v __pycache__`) and NFR-002
- [ ] T057 Commit stage 8

### Implementation Notes

- The paradigm file move is a simple `git mv` — verify the repository's `shipped/` scanner picks it up.
- `create-feature` is registered in `feature.py` line ~533 as `@app.command(name="create-feature")`. Change to `name="create-mission"`.
- The test directory rename (`tests/constitution/` → `tests/charter/`) is large (14 files) but mechanical.
- The scattered test references (~30 files) need targeted import and string replacement.
- Final acceptance sweep should confirm zero false positives in the grep exclusions.

### Parallel Opportunities

- T048-T049 (paradigm), T050-T051 (CLI), and T052-T053 (tests) are independent and can proceed in parallel.

### Dependencies

- Depends on WP06 and WP07 (all active renames must be complete before final sweep).

### Risks & Mitigations

- Missing scattered references → the acceptance greps (T056) catch any stragglers.
- Paradigm repository scanner may have hardcoded paths → verify by running the scanner test.

---

## Dependency & Execution Summary

```
WP01 (doctrine) → WP02 (core lib) → WP03 (specify_cli) → WP04 (CLI)
                                                              ↓
                                                          WP05 (templates/skills)
                                                              ↓
                                                          WP06 (docs)
                                                              ↓
                                                          WP07 (migration)
                                                              ↓
                                                          WP08 (cleanup)
```

- **Sequence**: WP01 → WP02 → WP03 → WP04 → WP05 → WP06 → WP07 → WP08
- **Parallelization**: Limited — the import dependency chain requires sequential stages. Within each WP, subtasks on different directories can parallel.
- **MVP Scope**: WP01–WP04 (core rename + CLI working). WP05–WP08 are polish and documentation.

---

## Requirements Coverage Summary

| Requirement ID | Covered By Work Package(s) |
|----------------|----------------------------|
| FR-001 | WP01, WP02, WP03 |
| FR-002 | WP02, WP03 |
| FR-003 | WP02, WP03 |
| FR-004 | WP04 |
| FR-005 | WP04 |
| FR-006 | WP07 |
| FR-007 | WP05 |
| FR-008 | WP05 |
| FR-009 | WP06 |
| FR-010 | WP06 |
| FR-011 | WP08 |
| FR-012 | WP08 |
| FR-013 | WP08 |
| NFR-001 | WP08 (acceptance gate) |
| NFR-002 | WP08 (acceptance gate) |
| NFR-003 | WP08 (acceptance gate) |
| C-001 | All WPs (exclusion enforced) |
| C-002 | All WPs (exclusion enforced) |
| C-003 | All WPs (exclusion enforced) |
| C-004 | WP06 (exclusion enforced) |
| C-005 | WP05 (exclusion enforced) |
| C-006 | WP04 (Python API has no backward compat) |

---

## Subtask Index (Reference)

| Subtask ID | Summary | Work Package | Priority | Parallel? |
|------------|---------|--------------|----------|-----------|
| T001 | git mv doctrine/constitution → charter | WP01 | P0 | No |
| T002 | Update src/ imports for doctrine.constitution | WP01 | P0 | Yes |
| T003 | Update tests/ imports for doctrine.constitution | WP01 | P0 | Yes |
| T004 | Verify doctrine rename (ruff + pytest) | WP01 | P0 | No |
| T005 | Commit stage 1 | WP01 | P0 | No |
| T006 | git mv constitution → charter (core) | WP02 | P0 | No |
| T007 | Rename 9 classes in core lib | WP02 | P0 | No |
| T008 | Rename functions in core lib | WP02 | P0 | No |
| T009 | Update src/ imports for constitution.* | WP02 | P0 | Yes |
| T010 | Update tests/ imports for constitution.* | WP02 | P0 | Yes |
| T011 | Verify core rename (ruff + pytest) | WP02 | P0 | No |
| T012 | Commit stage 2 | WP02 | P0 | No |
| T013 | git mv specify_cli/constitution → charter | WP03 | P0 | No |
| T014 | Rename 8 classes in specify_cli layer | WP03 | P0 | No |
| T015 | Rename functions in specify_cli layer | WP03 | P0 | No |
| T016 | Update src/ imports for specify_cli.constitution.* | WP03 | P0 | Yes |
| T017 | Update tests/ imports for specify_cli.constitution.* | WP03 | P0 | Yes |
| T018 | Verify specify_cli rename (ruff + pytest) | WP03 | P0 | No |
| T019 | Commit stage 3 | WP03 | P0 | No |
| T020 | git mv constitution.py → charter.py (CLI) | WP04 | P1 | No |
| T021 | Update CLI registration in __init__.py | WP04 | P1 | No |
| T022 | Add deprecation alias for constitution CLI | WP04 | P1 | No |
| T023 | Update shim dispatch | WP04 | P1 | No |
| T024 | git mv constitution_path.py → charter_path.py | WP04 | P1 | Yes |
| T025 | Rename _render_constitution_context | WP04 | P1 | Yes |
| T026 | Update dashboard/agent/CLI test imports | WP04 | P1 | No |
| T027 | CLI smoke test + pytest | WP04 | P1 | No |
| T028 | Commit stage 4 | WP04 | P1 | No |
| T029 | git mv constitution.md → charter.md (template) | WP05 | P1 | Yes |
| T030 | Update 7 other template files | WP05 | P1 | Yes |
| T031 | git mv skill directory | WP05 | P1 | Yes |
| T032 | Update skill content (SKILL.md + refs) | WP05 | P1 | Yes |
| T033 | Update template registry/migration refs | WP05 | P1 | No |
| T034 | Verify templates + skills | WP05 | P1 | No |
| T035 | Commit stage 5 | WP05 | P1 | No |
| T036 | Update 3 glossary entries | WP06 | P2 | No |
| T037 | Update ~25 architecture files | WP06 | P2 | Yes |
| T038 | Update ~23 docs files | WP06 | P2 | Yes |
| T039 | Update plan template section headings | WP06 | P2 | No |
| T040 | Verification grep for stale refs | WP06 | P2 | No |
| T041 | Commit stage 6 | WP06 | P2 | No |
| T042 | Create migration file | WP07 | P2 | No |
| T043 | Implement migration logic | WP07 | P2 | No |
| T044 | Register migration | WP07 | P2 | No |
| T045 | Write migration tests | WP07 | P2 | No |
| T046 | Verify migration tests | WP07 | P2 | No |
| T047 | Commit stage 7 | WP07 | P2 | No |
| T048 | git mv paradigm to shipped/ | WP08 | P3 | Yes |
| T049 | Verify paradigm discovery | WP08 | P3 | No |
| T050 | Rename create-feature → create-mission | WP08 | P3 | Yes |
| T051 | Update create-feature references | WP08 | P3 | Yes |
| T052 | git mv tests/constitution → tests/charter | WP08 | P3 | Yes |
| T053 | Update scattered test references | WP08 | P3 | No |
| T054 | Audit doctrine directories | WP08 | P3 | Yes |
| T055 | Full test suite run | WP08 | P3 | No |
| T056 | Acceptance grep sweep (NFR-001, NFR-002) | WP08 | P3 | No |
| T057 | Commit stage 8 | WP08 | P3 | No |
