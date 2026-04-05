---
work_package_id: WP02
title: Rename Core Constitution Library
dependencies: [WP01]
requirement_refs:
- FR-001
- FR-002
- FR-003
planning_base_branch: 063-rename-constitution-to-charter
merge_target_branch: 063-rename-constitution-to-charter
branch_strategy: Planning artifacts for this feature were generated on 063-rename-constitution-to-charter. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into 063-rename-constitution-to-charter unless the human explicitly redirects the landing branch.
subtasks:
- T006
- T007
- T008
- T009
- T010
- T011
- T012
phase: Phase 1 - Foundation Rename
assignee: ''
agent: ''
shell_pid: ''
history:
- at: '2026-04-05T05:50:00Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: python-implementer
authoritative_surface: src/charter
execution_mode: code_change
lane: planned
owned_files:
- src/charter/**
task_type: implement
---

# Work Package Prompt: WP02 – Rename Core Constitution Library

## Objectives & Success Criteria

- Rename `src/constitution/` → `src/charter/` (14 Python files, ~3,253 lines)
- Rename all 9 classes: `CompiledConstitution` → `CompiledCharter`, `ConstitutionReference` → `CharterReference`, `ConstitutionContextResult` → `CharterContextResult`, `ConstitutionDraft` → `CharterDraft`, `ConstitutionInterview` → `CharterInterview`, `ConstitutionSection` → `CharterSection`, `ConstitutionParser` → `CharterParser`, `ConstitutionTestingConfig` → `CharterTestingConfig`, `ConstitutionTemplateResolver` → `CharterTemplateResolver`
- Rename key functions: `build_constitution_context` → `build_charter_context`, `build_constitution_draft` → `build_charter_draft`, `write_constitution` → `write_charter`, `sync_constitution` → `sync_charter`
- All imports updated, tests pass, ruff clean

## Context & Constraints

- **Spec**: `kitty-specs/063-rename-constitution-to-charter/spec.md`
- **Plan**: Stage 2 of 8. Depends on WP01 (doctrine layer already renamed).
- **Data Model**: `kitty-specs/063-rename-constitution-to-charter/data-model.md` — complete class/function rename mapping
- **Constraint C-001**: Migration files must NOT be modified
- **Constraint C-006**: No Python API backward compatibility needed — rename in place
- **Tactic**: Change Function Declaration (simple mechanics — internal API)
- **Directive DIRECTIVE_030**: Tests + static analysis must pass before handoff

## Branch Strategy

- **Strategy**: Feature branch
- **Planning base branch**: main
- **Merge target branch**: main

**Implementation command**: `spec-kitty implement WP02 --base WP01`

## Subtasks & Detailed Guidance

### Subtask T006 – git mv constitution to charter (core)

- **Purpose**: Rename the directory while preserving git history.
- **Steps**:
  1. `git mv src/constitution/ src/charter/`
  2. Verify: `ls src/charter/__init__.py src/charter/compiler.py src/charter/context.py`
- **Files**: `src/constitution/` → `src/charter/`
- **Parallel?**: No — must complete first.

### Subtask T007 – Rename 9 classes in core lib

- **Purpose**: Update all class names from Constitution* to Charter*.
- **Steps**:
  For each file in `src/charter/`:
  1. `compiler.py`: `ConstitutionReference` → `CharterReference`, `CompiledConstitution` → `CompiledCharter`
  2. `context.py`: `ConstitutionContextResult` → `CharterContextResult`
  3. `generator.py`: `ConstitutionDraft` → `CharterDraft`
  4. `interview.py`: `ConstitutionInterview` → `CharterInterview`
  5. `parser.py`: `ConstitutionSection` → `CharterSection`, `ConstitutionParser` → `CharterParser`
  6. `schemas.py`: `ConstitutionTestingConfig` → `CharterTestingConfig`
  7. `template_resolver.py`: `ConstitutionTemplateResolver` → `CharterTemplateResolver`
  8. Update `__init__.py` `__all__` exports if present
  9. Update any `@dataclass`, `TypedDict`, or Pydantic model references
- **Files**: All `.py` files in `src/charter/`
- **Parallel?**: No (do together with T008 per-file).
- **Notes**: Use `replace_all` for mechanical renames within each file. Also catch docstrings and comments.

### Subtask T008 – Rename functions in core lib

- **Purpose**: Update all function names with "constitution" in them.
- **Steps**:
  1. `context.py`: `build_constitution_context` → `build_charter_context`
  2. `generator.py`: `build_constitution_draft` → `build_charter_draft`, `write_constitution` → `write_charter`
  3. `sync.py`: `sync_constitution` → `sync_charter`
  4. Search for any other functions: `grep -n "def.*constitution" src/charter/*.py`
  5. Update all found functions
- **Files**: `src/charter/context.py`, `src/charter/generator.py`, `src/charter/sync.py`, others as found
- **Parallel?**: No (do together with T007 per-file).

### Subtask T009 – Update src/ imports for constitution.*

- **Purpose**: Fix all imports across `src/` that reference the old `constitution.` package.
- **Steps**:
  1. `grep -rn "from constitution\.\|import constitution\.\|from constitution import" src/ --include="*.py" | grep -v upgrade/migrations | grep -v __pycache__`
  2. Replace `from constitution.` → `from charter.`
  3. Replace `import constitution.` → `import charter.`
  4. Also replace class name references at import sites: `from constitution.compiler import CompiledConstitution` → `from charter.compiler import CompiledCharter`
  5. Check for string references: `"constitution."` in log messages, error strings, etc.
- **Files**: Any file in `src/` importing from old package
- **Parallel?**: Yes (parallel with T010).
- **Notes**: Do NOT modify files in `src/specify_cli/upgrade/migrations/`.

### Subtask T010 – Update tests/ imports for constitution.*

- **Purpose**: Fix test file imports referencing the old package.
- **Steps**:
  1. `grep -rn "from constitution\.\|import constitution\.\|from constitution import" tests/ --include="*.py"`
  2. Replace imports and class name references
  3. Update any test assertions that reference old class names
- **Files**: Test files importing from `constitution.*`
- **Parallel?**: Yes (parallel with T009).

### Subtask T011 – Verify core rename

- **Purpose**: Confirm the rename is clean.
- **Steps**:
  1. `ruff check src/charter/`
  2. `pytest tests/constitution/` (these tests still live at old path — will be renamed in WP08)
  3. `grep -rn "from constitution\.\|import constitution\." src/ tests/ --include="*.py" | grep -v upgrade/migrations | grep -v __pycache__` — expect zero hits
- **Files**: N/A
- **Parallel?**: No.

### Subtask T012 – Commit stage 2

- **Purpose**: Create standalone commit.
- **Steps**:
  1. Stage all changed files
  2. `git commit --no-gpg-sign -m "refactor: rename src/constitution → src/charter with class/function renames (stage 2/8)"`
- **Parallel?**: No.

## Risks & Mitigations

- **String references**: Log messages, error messages, and docstrings may contain "constitution" as a string — search broadly.
- **`__init__.py` re-exports**: If `src/constitution/__init__.py` re-exports classes by name, those names must be updated.
- **Circular imports**: The core lib may have internal cross-imports — verify no import cycles are introduced.

## Review Guidance

- Verify all 9 classes are renamed consistently (no mix of old/new names).
- Verify no migration files were modified (C-001).
- Verify grep for `from constitution.` returns zero hits in active code.
- Spot-check that docstrings and comments within the renamed files use "charter" not "constitution".

## Activity Log

- 2026-04-05T05:50:00Z – system – Prompt created.
