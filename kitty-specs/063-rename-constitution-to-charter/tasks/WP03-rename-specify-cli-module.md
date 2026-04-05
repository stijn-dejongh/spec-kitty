---
work_package_id: WP03
title: Rename Specify CLI Constitution Module
dependencies: [WP02]
requirement_refs:
- FR-001
- FR-002
- FR-003
planning_base_branch: 063-rename-constitution-to-charter
merge_target_branch: 063-rename-constitution-to-charter
branch_strategy: Planning artifacts for this feature were generated on 063-rename-constitution-to-charter. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into 063-rename-constitution-to-charter unless the human explicitly redirects the landing branch.
subtasks:
- T013
- T014
- T015
- T016
- T017
- T018
- T019
phase: Phase 1 - Foundation Rename
assignee: ''
agent: ''
shell_pid: ''
history:
- at: '2026-04-05T05:50:00Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: python-implementer
authoritative_surface: src/specify_cli/charter
execution_mode: code_change
lane: planned
owned_files:
- src/specify_cli/charter/**
task_type: implement
---

# Work Package Prompt: WP03 – Rename Specify CLI Constitution Module

## Objectives & Success Criteria

- Rename `src/specify_cli/constitution/` → `src/specify_cli/charter/` (12 Python files, ~2,928 lines)
- Rename all 8 classes mirroring WP02 renames in the CLI wrapper layer
- Rename all functions with "constitution" in their name
- All imports updated, tests pass, ruff clean

## Context & Constraints

- **Spec**: `kitty-specs/063-rename-constitution-to-charter/spec.md`
- **Plan**: Stage 3 of 8. Depends on WP02 (core lib already renamed to `charter.*`).
- **Data Model**: `kitty-specs/063-rename-constitution-to-charter/data-model.md`
- **Constraint C-001**: Migration files must NOT be modified
- **Tactic**: Change Function Declaration (simple mechanics)
- **Key insight**: This module wraps the core lib. After WP02, core imports already point to `charter.*`. This WP updates the CLI wrapper layer to match.

## Branch Strategy

- **Strategy**: Feature branch
- **Planning base branch**: main
- **Merge target branch**: main

**Implementation command**: `spec-kitty implement WP03 --base WP02`

## Subtasks & Detailed Guidance

### Subtask T013 – git mv specify_cli/constitution to specify_cli/charter

- **Purpose**: Rename the CLI wrapper module directory.
- **Steps**:
  1. `git mv src/specify_cli/constitution/ src/specify_cli/charter/`
  2. Verify: `ls src/specify_cli/charter/__init__.py`
- **Files**: `src/specify_cli/constitution/` → `src/specify_cli/charter/`
- **Parallel?**: No.

### Subtask T014 – Rename 8 classes in specify_cli layer

- **Purpose**: Update class names to match core lib renames.
- **Steps**:
  For each file in `src/specify_cli/charter/`:
  1. `compiler.py`: `ConstitutionReference` → `CharterReference`, `CompiledConstitution` → `CompiledCharter`
  2. `context.py`: `ConstitutionContextResult` → `CharterContextResult`
  3. `generator.py`: `ConstitutionDraft` → `CharterDraft`
  4. `interview.py`: `ConstitutionInterview` → `CharterInterview`
  5. `parser.py`: `ConstitutionSection` → `CharterSection`, `ConstitutionParser` → `CharterParser`
  6. `schemas.py`: `ConstitutionTestingConfig` → `CharterTestingConfig`
  7. Update `__init__.py` exports
- **Files**: All `.py` files in `src/specify_cli/charter/`
- **Parallel?**: No (do per-file with T015).

### Subtask T015 – Rename functions in specify_cli layer

- **Purpose**: Update function names.
- **Steps**:
  1. `grep -n "def.*constitution" src/specify_cli/charter/*.py`
  2. Rename each found function: replace `constitution` → `charter` in function name
  3. Update internal cross-references within the module
- **Files**: `src/specify_cli/charter/*.py`
- **Parallel?**: No.

### Subtask T016 – Update src/ imports for specify_cli.constitution.*

- **Purpose**: Fix imports across `src/` referencing the old module.
- **Steps**:
  1. `grep -rn "from specify_cli.constitution\.\|import specify_cli.constitution\.\|from specify_cli.constitution import\|from specify_cli import constitution" src/ --include="*.py" | grep -v upgrade/migrations | grep -v __pycache__`
  2. Replace all: `specify_cli.constitution` → `specify_cli.charter`
  3. Update class name references at import sites (e.g., `from specify_cli.constitution.compiler import CompiledConstitution` → `from specify_cli.charter.compiler import CompiledCharter`)
- **Files**: Any file in `src/` with old imports
- **Parallel?**: Yes (parallel with T017).

### Subtask T017 – Update tests/ imports for specify_cli.constitution.*

- **Purpose**: Fix test file imports.
- **Steps**:
  1. `grep -rn "from specify_cli.constitution\.\|import specify_cli.constitution\.\|specify_cli.constitution" tests/ --include="*.py"`
  2. Replace imports and class name references
  3. Update assertion strings if they reference old names
- **Files**: Test files under `tests/specify_cli/`
- **Parallel?**: Yes (parallel with T016).

### Subtask T018 – Verify specify_cli rename

- **Purpose**: Confirm clean rename.
- **Steps**:
  1. `ruff check src/specify_cli/charter/`
  2. `pytest tests/specify_cli/` — all tests pass
  3. `grep -rn "specify_cli.constitution" src/ tests/ --include="*.py" | grep -v upgrade/migrations | grep -v __pycache__` — zero hits
- **Parallel?**: No.

### Subtask T019 – Commit stage 3

- **Purpose**: Standalone commit.
- **Steps**:
  1. Stage all changed files
  2. `git commit --no-gpg-sign -m "refactor: rename specify_cli/constitution → specify_cli/charter (stage 3/8)"`
- **Parallel?**: No.

## Risks & Mitigations

- **Cross-layer imports**: Some specify_cli modules import from both the core lib (`charter.*`) and CLI wrapper (`specify_cli.charter.*`) — verify both resolve.
- **Lazy imports**: Some modules may use `importlib.import_module("specify_cli.constitution.X")` — search for dynamic imports.

## Review Guidance

- Verify all 8 classes renamed consistently.
- Verify cross-layer imports resolve (core `charter.*` + CLI `specify_cli.charter.*`).
- Verify no migration files modified.

## Activity Log

- 2026-04-05T05:50:00Z – system – Prompt created.
