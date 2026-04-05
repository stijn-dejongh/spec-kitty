---
work_package_id: WP01
title: Rename Doctrine Constitution Layer
dependencies: []
requirement_refs:
- FR-001
- C-001
planning_base_branch: 063-rename-constitution-to-charter
merge_target_branch: 063-rename-constitution-to-charter
branch_strategy: Planning artifacts for this feature were generated on 063-rename-constitution-to-charter. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into 063-rename-constitution-to-charter unless the human explicitly redirects the landing branch.
subtasks:
- T001
- T002
- T003
- T004
- T005
phase: Phase 1 - Foundation Rename
assignee: ''
agent: ''
shell_pid: ''
history:
- at: '2026-04-05T05:50:00Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: python-implementer
authoritative_surface: src/doctrine/charter
execution_mode: code_change
lane: planned
owned_files:
- src/doctrine/charter/defaults.yaml
task_type: implement
---

# Work Package Prompt: WP01 – Rename Doctrine Constitution Layer

## Objectives & Success Criteria

- Rename `src/doctrine/constitution/` → `src/doctrine/charter/`
- Update all imports referencing `doctrine.constitution` across the codebase
- All tests pass, `ruff check src/doctrine/` is clean
- No remaining `doctrine.constitution` imports in active code (excluding migrations)

## Context & Constraints

- **Spec**: `kitty-specs/063-rename-constitution-to-charter/spec.md`
- **Plan**: `kitty-specs/063-rename-constitution-to-charter/plan.md` — Stage 1 of 8
- **Data Model**: `kitty-specs/063-rename-constitution-to-charter/data-model.md` — full rename mapping
- **Constraint C-001**: Migration files (`upgrade/migrations/m_*_constitution_*.py`) must NOT be modified
- **Tactic**: Move Field — relocate directory, update references
- **Directive DIRECTIVE_029**: Use `--no-gpg-sign` for commits
- **Directive DIRECTIVE_030**: Tests and static analysis must pass before handoff

This is the smallest and first stage. It establishes the rename pattern for all subsequent WPs. The `src/doctrine/constitution/` directory contains only `defaults.yaml`.

## Branch Strategy

- **Strategy**: Feature branch
- **Planning base branch**: main
- **Merge target branch**: main

**Implementation command**: `spec-kitty implement WP01`

## Subtasks & Detailed Guidance

### Subtask T001 – git mv doctrine/constitution to doctrine/charter

- **Purpose**: Rename the directory while preserving git history.
- **Steps**:
  1. Run `git mv src/doctrine/constitution/ src/doctrine/charter/`
  2. Verify the directory exists at new location: `ls src/doctrine/charter/defaults.yaml`
- **Files**: `src/doctrine/constitution/` → `src/doctrine/charter/`
- **Parallel?**: No — must complete before import updates.

### Subtask T002 – Update src/ imports for doctrine.constitution

- **Purpose**: Fix all Python imports that reference the old module path.
- **Steps**:
  1. Search: `grep -rn "doctrine.constitution\|doctrine\.constitution\|from doctrine.constitution\|from doctrine import constitution" src/ --include="*.py" | grep -v upgrade/migrations | grep -v __pycache__`
  2. For each hit, replace `doctrine.constitution` → `doctrine.charter`
  3. Also check for string references: `grep -rn "'doctrine.constitution'\|\"doctrine.constitution\"" src/ --include="*.py" | grep -v upgrade/migrations`
- **Files**: Any Python file in `src/` that imports from `doctrine.constitution`
- **Parallel?**: Yes (parallel with T003).
- **Notes**: Exclude migration files per C-001.

### Subtask T003 – Update tests/ imports for doctrine.constitution

- **Purpose**: Fix test file imports that reference the old module path.
- **Steps**:
  1. Search: `grep -rn "doctrine.constitution\|from doctrine.constitution\|from doctrine import constitution" tests/ --include="*.py"`
  2. Replace all occurrences with `doctrine.charter`
- **Files**: Any test file referencing `doctrine.constitution`
- **Parallel?**: Yes (parallel with T002).

### Subtask T004 – Verify doctrine rename

- **Purpose**: Confirm the rename is clean with no broken imports.
- **Steps**:
  1. Run `ruff check src/doctrine/`
  2. Run `pytest` for any tests that exercise doctrine constitution/charter functionality
  3. Run `grep -rn "doctrine.constitution" src/ tests/ --include="*.py" | grep -v upgrade/migrations | grep -v __pycache__` — expect zero hits
- **Files**: N/A (verification only)
- **Parallel?**: No — must run after T002 and T003.

### Subtask T005 – Commit stage 1

- **Purpose**: Create a standalone commit for this rename stage.
- **Steps**:
  1. `git add src/doctrine/charter/ src/` (affected files only)
  2. `git commit --no-gpg-sign -m "refactor: rename doctrine/constitution → doctrine/charter (stage 1/8)"`
- **Files**: All changed files
- **Parallel?**: No.

## Risks & Mitigations

- **Hidden transitive imports**: Some modules may import `doctrine.constitution` indirectly through `__init__.py` re-exports → grep exhaustively before committing.
- **String references in YAML**: The `defaults.yaml` file may be referenced by path string in other config files → search for `"doctrine/constitution"` path strings too.

## Review Guidance

- Verify no migration files were touched (C-001).
- Verify `defaults.yaml` content is unchanged (only directory moved).
- Verify grep for `doctrine.constitution` returns zero hits in active code.

## Activity Log

- 2026-04-05T05:50:00Z – system – Prompt created.
