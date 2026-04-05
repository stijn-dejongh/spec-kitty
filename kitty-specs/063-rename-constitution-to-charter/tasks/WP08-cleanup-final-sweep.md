---
work_package_id: WP08
title: Cleanup — Paradigm, CLI Subcommand, Test Renames
dependencies:
- WP06
requirement_refs:
- FR-011
- FR-012
- FR-013
- NFR-001
- NFR-002
- NFR-003
planning_base_branch: 063-rename-constitution-to-charter
merge_target_branch: 063-rename-constitution-to-charter
branch_strategy: Planning artifacts for this feature were generated on 063-rename-constitution-to-charter. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into 063-rename-constitution-to-charter unless the human explicitly redirects the landing branch.
subtasks:
- T048
- T049
- T050
- T051
- T052
- T053
- T054
- T055
- T056
- T057
phase: Phase 5 - Cleanup
assignee: ''
agent: ''
shell_pid: ''
history:
- at: '2026-04-05T05:50:00Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: python-implementer
authoritative_surface: tests/charter
execution_mode: code_change
lane: planned
owned_files:
- src/doctrine/paradigms/shipped/test-first.paradigm.yaml
- src/specify_cli/cli/commands/agent/feature.py
- tests/charter/**
task_type: implement
---

# Work Package Prompt: WP08 – Cleanup — Paradigm, CLI Subcommand, Test Renames

## Objectives & Success Criteria

- Move `test-first.paradigm.yaml` from paradigms root to `shipped/` — paradigm discoverable
- Rename `create-feature` → `create-mission` CLI subcommand
- Rename `tests/constitution/` → `tests/charter/` and update all scattered test references
- Audit doctrine directories for other misplaced files
- Full test suite passes
- Acceptance greps (NFR-001, NFR-002) confirm zero stale references

## Context & Constraints

- **Spec**: `kitty-specs/063-rename-constitution-to-charter/spec.md` — User Stories 6, 7
- **Plan**: Stage 8 of 8 (final). Depends on WP06 and WP07.
- **Tactic**: Move Field (paradigm), Change Function Declaration (CLI subcommand), Smallest Viable Diff (test renames)
- **Directive DIRECTIVE_025**: Boy Scout Rule — clean up touched areas, each as its own small commit.

## Branch Strategy

- **Strategy**: Feature branch
- **Planning base branch**: main
- **Merge target branch**: main

**Implementation command**: `spec-kitty implement WP08 --base WP07`

(Note: WP08 depends on both WP06 and WP07. If WP06 completed on a different branch, merge it first.)

## Subtasks & Detailed Guidance

### Subtask T048 – git mv paradigm to shipped/

- **Purpose**: Move the misplaced paradigm file to the correct location.
- **Steps**:
  1. `git mv src/doctrine/paradigms/test-first.paradigm.yaml src/doctrine/paradigms/shipped/test-first.paradigm.yaml`
  2. Verify: `ls src/doctrine/paradigms/shipped/test-first.paradigm.yaml`
- **Files**: `src/doctrine/paradigms/test-first.paradigm.yaml` → `src/doctrine/paradigms/shipped/`
- **Parallel?**: Yes (independent of T050, T052).

### Subtask T049 – Verify paradigm discovery

- **Purpose**: Confirm the paradigm repository discovers the file at its new location.
- **Steps**:
  1. Run paradigm repository tests: `pytest tests/doctrine/procedures/test_repository.py -v` (or equivalent paradigm tests)
  2. If there's a paradigm listing command: `spec-kitty doctrine paradigms list` (or equivalent)
  3. Confirm "test-first" appears in the discoverable paradigm list
- **Files**: N/A (verification)
- **Parallel?**: No (depends on T048).

### Subtask T050 – Rename create-feature → create-mission

- **Purpose**: Fix CLI subcommand naming inconsistency.
- **Steps**:
  1. In `src/specify_cli/cli/commands/agent/feature.py`, find `@app.command(name="create-feature")` (~line 533)
  2. Change to `@app.command(name="create-mission")`
  3. Optionally rename function `create_feature` → `create_mission` for consistency
  4. Update help string if it says "feature"
- **Files**: `src/specify_cli/cli/commands/agent/feature.py`
- **Parallel?**: Yes (independent of T048, T052).

### Subtask T051 – Update create-feature references

- **Purpose**: Fix references to the old command name.
- **Steps**:
  1. `grep -rn "create-feature\|create_feature" src/ tests/ docs/ architecture/ --include="*.py" --include="*.md" --include="*.yaml" | grep -v __pycache__ | grep -v upgrade/migrations`
  2. Update template references (e.g., in `specify.md`, `plan.md` if they show `create-feature` usage examples)
  3. Update test assertions that check for "create-feature" in CLI output
  4. Update documentation that references the command
- **Files**: Templates, tests, docs as found
- **Parallel?**: Yes (after T050).

### Subtask T052 – git mv tests/constitution → tests/charter

- **Purpose**: Rename the main constitution test directory.
- **Steps**:
  1. `git mv tests/constitution/ tests/charter/`
  2. Update all internal imports in the renamed test files:
     `grep -rn "from constitution\.\|import constitution\.\|from charter\." tests/charter/ --include="*.py"`
  3. Ensure imports point to `charter.*` (core lib, already renamed in WP02)
- **Files**: `tests/constitution/` → `tests/charter/` (14 test files)
- **Parallel?**: Yes (independent of T048, T050).

### Subtask T053 – Update scattered test references

- **Purpose**: Fix ~30 test files outside `tests/charter/` that reference constitution.
- **Steps**:
  1. `grep -rln "constitution" tests/ --include="*.py" | grep -v upgrade/migrations | grep -v __pycache__`
  2. For each file:
     - Update imports: `from constitution.` → `from charter.`, `from specify_cli.constitution.` → `from specify_cli.charter.`
     - Update class references: `CompiledConstitution` → `CompiledCharter`, etc.
     - Update assertion strings: `"constitution"` in expected output → `"charter"`
     - Update path references: `.kittify/constitution/` → `.kittify/charter/`
     - Update test file names if they contain "constitution" (e.g., `test_workflow_constitution_context.py` → `test_workflow_charter_context.py`)
  3. Key files:
     - `tests/agent/test_workflow_constitution_context.py`
     - `tests/agent/cli/commands/test_constitution_cli.py`
     - `tests/specify_cli/cli/commands/test_constitution_cli.py`
     - `tests/test_dashboard/test_api_constitution.py`
     - `tests/init/test_constitution_runtime_integration.py`
     - `tests/merge/test_profile_constitution_e2e.py`
- **Files**: ~30 test files
- **Parallel?**: No (depends on T052 for import paths to be stable).

### Subtask T054 – Audit doctrine directories

- **Purpose**: Check for other misplaced files (FR-012).
- **Steps**:
  1. List files at root of each doctrine subdirectory:
     ```
     ls src/doctrine/paradigms/*.yaml (should only be __init__.py and shipped/)
     ls src/doctrine/directives/*.yaml (check for files outside shipped/)
     ls src/doctrine/tactics/*.yaml (check for files outside shipped/ and refactoring/)
     ls src/doctrine/procedures/*.yaml (check for files outside shipped/)
     ```
  2. Any `.yaml` files at root level (not in `shipped/` or `_proposed/`) are misplaced
  3. If found: move to appropriate subdirectory, verify tests pass
- **Files**: `src/doctrine/*/`
- **Parallel?**: Yes (independent).

### Subtask T055 – Full test suite run

- **Purpose**: Confirm everything works end-to-end.
- **Steps**:
  1. `pytest tests/ --timeout=120` — full suite
  2. Note any pre-existing failures vs newly introduced failures
  3. All new test failures must be resolved before handoff (DIRECTIVE_030)
- **Parallel?**: No.

### Subtask T056 – Acceptance grep sweep

- **Purpose**: Final acceptance gates per NFR-001 and NFR-002.
- **Steps**:
  1. NFR-001: `grep -ri "constitution" src/ --include="*.py" | grep -v upgrade/migrations | grep -v __pycache__` → zero hits
  2. NFR-002: `grep -ri "constitution" src/ --include="*.yaml" --include="*.md" | grep -v _reference | grep -v curation` → zero hits on active templates
  3. If any hits remain, investigate and fix
- **Parallel?**: No.

### Subtask T057 – Commit stage 8

- **Purpose**: Final commit.
- **Steps**: `git commit --no-gpg-sign -m "refactor: paradigm relocation, create-mission rename, test cleanup, final acceptance (stage 8/8)"`
- **Parallel?**: No.

## Risks & Mitigations

- **Paradigm repository scanner**: May have hardcoded paths or only scan specific subdirectories — verify by running the actual scanner.
- **Scattered test references**: The ~30 files with scattered references are the highest risk for missed renames — the acceptance grep (T056) is the safety net.
- **create-feature in automation**: If any CI scripts or external tools call `create-feature`, they'll break — check `.github/workflows/` for references.

## Review Guidance

- Verify paradigm is discoverable (T049 output).
- Verify `spec-kitty agent mission create-mission --help` works.
- Verify acceptance greps return zero hits.
- Verify no migration files or kitty-specs archives were modified.
- This is the final WP — all success criteria from the spec should be met.

## Activity Log

- 2026-04-05T05:50:00Z – system – Prompt created.
