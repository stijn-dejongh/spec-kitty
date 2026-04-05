# Mission Specification: Rename Constitution to Charter

**Mission Branch**: `063-rename-constitution-to-charter`  
**Created**: 2026-04-05  
**Status**: Draft  
**Input**: GitHub issue #379 — rename `constitution` → `charter` across active surfaces  
**Related**: Epic #364

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Internal API and Module Rename (Priority: P1)

A developer working on spec-kitty imports and calls constitution-related modules, classes, and kernel functions. After this change, all active Python modules, classes, and functions use `charter` naming. The codebase is internally consistent.

**Why this priority**: The Python source is the foundation — CLI, templates, and docs all depend on these names. Everything else follows from this rename.

**Independent Test**: Run `grep -ri "constitution" src/ --include="*.py" | grep -v upgrade/migrations | grep -v __pycache__` and confirm zero hits.

**Acceptance Scenarios**:

1. **Given** the renamed modules exist, **When** a developer imports from `specify_cli.charter`, **Then** all classes and functions resolve correctly.
2. **Given** the path-resolution functions are updated, **When** `resolve_project_charter_path()` is called, **Then** it returns the correct `.kittify/charter/` path.
3. **Given** migration files reference `constitution`, **When** grepping migration files, **Then** they are unchanged (historical preservation).

---

### User Story 2 - CLI Command with Deprecation Alias (Priority: P1)

A user runs `spec-kitty charter` to access charter workflows. A user who still runs `spec-kitty constitution` sees a deprecation warning but the command still works.

**Why this priority**: The CLI is the primary user-facing surface. Users must not be broken by the rename.

**Independent Test**: Run `spec-kitty charter --help` and confirm it works. Run `spec-kitty constitution --help` and confirm it works but emits a deprecation warning to stderr.

**Acceptance Scenarios**:

1. **Given** the CLI is updated, **When** a user runs `spec-kitty charter context`, **Then** the command executes normally.
2. **Given** the backward-compat alias exists, **When** a user runs `spec-kitty constitution context`, **Then** the command executes normally AND a deprecation warning is printed to stderr.

---

### User Story 3 - User Project Migration (Priority: P2)

A user with an existing spec-kitty project has a `.kittify/constitution/` directory. After running `spec-kitty upgrade`, the directory is renamed to `.kittify/charter/` and all internal references are updated.

**Why this priority**: Existing user projects must be migrated cleanly; without this, the kernel path functions would point to a non-existent directory.

**Independent Test**: Create a project with `.kittify/constitution/`, run the migration, confirm `.kittify/charter/` exists and `.kittify/constitution/` does not.

**Acceptance Scenarios**:

1. **Given** a project with `.kittify/constitution/`, **When** `spec-kitty upgrade` runs, **Then** the directory is renamed to `.kittify/charter/`.
2. **Given** a project that already has `.kittify/charter/`, **When** `spec-kitty upgrade` runs, **Then** the migration is a no-op.

---

### User Story 4 - Skill and Template Rename (Priority: P2)

An agent invokes `/spec-kitty.charter` (previously `/spec-kitty.constitution`). All command templates and skill files reference `charter` terminology.

**Why this priority**: Agent-facing surfaces must match the new naming for consistency.

**Independent Test**: Grep active template files for `constitution` references and confirm zero hits (excluding historical files).

**Acceptance Scenarios**:

1. **Given** templates are updated, **When** an agent loads the charter skill, **Then** it resolves correctly.
2. **Given** skill metadata is updated, **When** an agent lists available skills, **Then** `spec-kitty-charter-doctrine` appears (not `constitution`).

---

### User Story 5 - Glossary and Documentation Update (Priority: P2)

The glossary canonical term is updated from `constitution` to `charter`. Architecture and 2.x docs reflect the new terminology.

**Why this priority**: Documentation consistency prevents confusion for contributors and users.

**Independent Test**: Check glossary entries and architecture docs for stale `constitution` references.

**Acceptance Scenarios**:

1. **Given** the glossary is updated, **When** a user looks up governance terminology, **Then** `charter` is the canonical term.
2. **Given** architecture docs are updated, **When** reading 2.x documentation, **Then** all references use `charter`.

---

### User Story 6 - Doctrine Paradigm File Cleanup (Priority: P3)

The misplaced `test-first.paradigm.yaml` file at `src/doctrine/paradigms/` root is moved into `src/doctrine/paradigms/shipped/` so the paradigm repository can discover it. Any other misplaced doctrine files are similarly corrected.

**Why this priority**: Housekeeping — the file is unretrievable in its current location but is not blocking users.

**Independent Test**: Confirm `src/doctrine/paradigms/test-first.paradigm.yaml` no longer exists at root level and exists inside `shipped/`. Confirm the paradigm repository loads it.

**Acceptance Scenarios**:

1. **Given** the file is moved, **When** the paradigm repository scans `shipped/`, **Then** `test-first` paradigm is discoverable.
2. **Given** a review of doctrine directories, **When** checking for other misplaced files, **Then** all paradigms/directives are in their correct subdirectories.

---

### User Story 7 - CLI Subcommand Naming Consistency (Priority: P3)

The `spec-kitty agent mission` CLI currently registers `create-feature` as the subcommand name, but the conceptual model and documentation refer to "missions" not "features" at this level. The subcommand should be renamed to `create-mission` for consistency with the rest of the `agent mission` command group.

**Why this priority**: Naming consistency across the CLI — this is the same class of problem as the constitution→charter rename, but lower impact since it only affects the developer/agent-facing `agent mission` surface.

**Independent Test**: Run `spec-kitty agent mission create-mission --help` and confirm it works. Run `spec-kitty agent mission create-feature --help` and confirm it either emits a deprecation warning or is removed.

**Acceptance Scenarios**:

1. **Given** the CLI is updated, **When** a user runs `spec-kitty agent mission create-mission "slug"`, **Then** the command executes normally.
2. **Given** the old name is removed, **When** a user runs `spec-kitty agent mission create-feature "slug"`, **Then** the command returns an error suggesting `create-mission` as the correct name.

---

### Edge Cases

- What happens when a user project has both `.kittify/constitution/` and `.kittify/charter/`? Migration should detect the conflict and warn rather than overwrite.
- What happens when third-party code imports `specify_cli.constitution`? Not supported — only the CLI alias gets backward compat, not the Python API.
- What happens when migration files internally import from constitution paths? Verify during WP02 that no migration file does a runtime `from constitution.X import Y`. If none found (expected), no action needed. If found, add a thin `src/constitution/__init__.py` re-exporting from `src/charter/`.

## Requirements *(mandatory)*

### Functional Requirements

| ID | Title | User Story | Priority | Status |
|----|-------|------------|----------|--------|
| FR-001 | Rename Python modules | As a developer, I want all active `constitution` modules renamed to `charter` so the codebase uses consistent terminology. | High | Open |
| FR-002 | Rename path-resolution and context functions | As a developer, I want all constitution-named path-resolution and context-rendering functions renamed to `charter` equivalents so callers use the new names. | High | Open |
| FR-003 | Rename classes and types | As a developer, I want all 15+ constitution-named classes renamed to charter equivalents so type references are consistent. | High | Open |
| FR-004 | CLI command rename | As a user, I want `spec-kitty charter` to be the primary command so terminology is consistent. | High | Open |
| FR-005 | CLI deprecation alias | As a user, I want `spec-kitty constitution` to still work with a deprecation warning so I'm not broken by the change. | High | Open |
| FR-006 | User project migration | As a user, I want `spec-kitty upgrade` to rename `.kittify/constitution/` to `.kittify/charter/` so my project stays compatible. | High | Open |
| FR-007 | Skill rename | As an agent, I want the skill renamed from `spec-kitty-constitution-doctrine` to `spec-kitty-charter-doctrine` so skill invocation matches the new terminology. | Medium | Open |
| FR-008 | Template updates | As an agent, I want command templates to use `charter` terminology so generated content is consistent. | Medium | Open |
| FR-009 | Glossary update | As a contributor, I want the glossary canonical term updated to `charter` so terminology is authoritative. | Medium | Open |
| FR-010 | Architecture/2.x docs update | As a contributor, I want architecture and 2.x docs to use `charter` so documentation is consistent. | Medium | Open |
| FR-011 | Doctrine paradigm cleanup | As a developer, I want `test-first.paradigm.yaml` moved to `shipped/` so the paradigm repository can discover it. | Low | Open |
| FR-012 | Doctrine directory audit | As a developer, I want all doctrine files reviewed for correct placement so no other files are misplaced. | Low | Open |
| FR-013 | Rename create-feature to create-mission | As a developer, I want `spec-kitty agent mission create-mission` to be the correct subcommand name so the CLI is internally consistent. | Low | Open |

### Non-Functional Requirements

| ID | Title | Requirement | Category | Priority | Status |
|----|-------|-------------|----------|----------|--------|
| NFR-001 | Zero active constitution references | `grep -ri "constitution" src/ --include="*.py" \| grep -v upgrade/migrations \| grep -v __pycache__` returns zero hits | Consistency | High | Open |
| NFR-002 | Zero active template references | `grep -ri "constitution" src/ --include="*.yaml" --include="*.md" \| grep -v _reference \| grep -v curation` returns zero hits on active templates | Consistency | High | Open |
| NFR-003 | Full test suite passes | All existing tests pass after the rename with no new failures | Reliability | High | Open |

### Constraints

| ID | Title | Constraint | Category | Priority | Status |
|----|-------|------------|----------|----------|--------|
| C-001 | Preserve migration history | Migration files (`upgrade/migrations/m_*_constitution_*.py`) must NOT be renamed — they document history | Technical | High | Open |
| C-002 | Preserve migration tests | Migration test files must NOT be renamed — they test migration behavior | Technical | High | Open |
| C-003 | Preserve kitty-specs archives | `kitty-specs/` planning artifacts must NOT be renamed — they are historical archives | Technical | High | Open |
| C-004 | Preserve changelog | Changelog entries referencing `constitution` must NOT be changed — historical record | Technical | High | Open |
| C-005 | Preserve legacy agent configs | Legacy agent config files (`.cursor/`, `.codex/`, etc.) must NOT be renamed — deprecated copies | Technical | Medium | Open |
| C-006 | Python API no backward compat | The Python import paths do NOT need backward compatibility — only the CLI alias | Technical | Medium | Open |

### Key Entities

- **Charter** (formerly Constitution): The project governance document compiled from interviews, references, and directives. Lives at `.kittify/charter/`.
- **Deprecation Alias**: A CLI-level alias that maps `spec-kitty constitution` → `spec-kitty charter` with a stderr warning.
- **User Project Migration**: An upgrade migration that renames the filesystem directory in existing user projects.

## Operational Guidelines

The following doctrine procedures and tactics govern how this refactoring is executed:

### Governing Procedures

- **Refactoring** (`refactoring.procedure`): The overarching workflow — identify the smell, select the appropriate tactic, apply changes in safe increments, verify behavior preservation after each step, and commit the refactoring separately from feature work.
- **Test-First Bug Fixing** (`test-first-bug-fixing.procedure`): When any stage reveals broken behavior (e.g., imports that fail after a module rename, or a paradigm that doesn't load after relocation), write a failing test that reproduces the issue *before* fixing it. The reproduction test and the fix are committed together. This transforms unexpected breakage into a verifiable, regression-proof correction.

### Applicable Tactics

- **Change Function Declaration** (`refactoring-change-function-declaration`): Applies to renaming the 7 kernel API functions and 15+ classes. Use *simple mechanics* (rename + update all call sites in one pass) for internal functions. Use *migration mechanics* (new function → delegate old → deprecate → remove) for the CLI command surface.
- **Strangler Fig** (`refactoring-strangler-fig`): Applies to the CLI deprecation alias. Build the `charter` command alongside `constitution`, reroute callers, then deprecate the old path with a warning. The legacy entry point remains functional but emits a deprecation notice.
- **Move Field** (`refactoring-move-field`): Applies to relocating `test-first.paradigm.yaml` from the paradigms root into `shipped/`. Verify the paradigm repository discovers it after the move.
- **Smallest Viable Diff** (`change-apply-smallest-viable-diff`): Cross-cutting discipline for all stages. Each stage should be the minimal diff that achieves its goal. Do not reformat, reorganize, or improve adjacent code. Verify tests after each stage before proceeding to the next.

### Governing Directives

- **DIRECTIVE_001 — Architectural Integrity Standard** (required): Maintain clear separation of concerns and well-defined component boundaries. The rename must preserve existing module boundaries — renaming a module does not change its responsibility or its interface contract. Cross-boundary interactions must remain mediated by explicit interfaces.
- **DIRECTIVE_025 — Boy Scout Rule** (advisory): Leave touched areas in a slightly better state when safe and local to the active task. During the rename, minor cleanup in touched files (dead imports, stale comments) is permitted and encouraged. Boy Scout improvements are compatible with smallest-viable-diff discipline — each cleanup is simply its own small, targeted commit rather than being bundled into the rename commit.
- **DIRECTIVE_029 — Agent Commit Signing Policy** (required): Agent-authored commits must use `--no-gpg-sign` or `commit.gpgsign=false`. Do not assume signing keys are available in worktrees or CI.
- **DIRECTIVE_030 — Test and Typecheck Quality Gate** (required): Each stage must pass the relevant test suite and static analysis (ruff, mypy) before handoff. New code meets coverage targets. Pre-existing failures are recorded separately from newly introduced failures.
- **DIRECTIVE_031 — Context-Aware Design** (required): The rename from `constitution` to `charter` is itself a ubiquitous language alignment. All identifiers in renamed code must use the new term consistently within each bounded context. The glossary must be updated to reflect the canonical term change.

### Staging Discipline

Each rename stage is a standalone commit with tests verified green before moving to the next stage. If a stage breaks tests, apply the test-first bug fixing procedure: write a failing test that reproduces the breakage, then fix. This follows the refactoring procedure's "apply in smallest viable steps" principle.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Zero `constitution` references in active source files (verified by grep commands in NFR-001 and NFR-002)
- **SC-002**: `spec-kitty charter` CLI command works identically to the old `spec-kitty constitution`
- **SC-003**: `spec-kitty constitution` emits a deprecation warning and delegates to `charter`
- **SC-004**: Existing test suite passes with no new failures after the rename
- **SC-005**: User projects with `.kittify/constitution/` are migrated cleanly by `spec-kitty upgrade`
- **SC-006**: `test-first.paradigm.yaml` is discoverable by the paradigm repository after relocation
- **SC-007**: `spec-kitty agent mission create-mission` works as the primary subcommand name
