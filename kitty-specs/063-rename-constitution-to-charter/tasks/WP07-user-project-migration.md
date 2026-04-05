---
work_package_id: WP07
title: User-Project Migration
dependencies: [WP04]
requirement_refs:
- FR-006
planning_base_branch: 063-rename-constitution-to-charter
merge_target_branch: 063-rename-constitution-to-charter
branch_strategy: Planning artifacts for this feature were generated on 063-rename-constitution-to-charter. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into 063-rename-constitution-to-charter unless the human explicitly redirects the landing branch.
subtasks:
- T042
- T043
- T044
- T045
- T046
- T047
phase: Phase 4 - Migration
assignee: ''
agent: ''
shell_pid: ''
history:
- at: '2026-04-05T05:50:00Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: python-implementer
authoritative_surface: src/specify_cli/upgrade/migrations
execution_mode: code_change
lane: planned
owned_files:
- src/specify_cli/upgrade/migrations/m_*_rename_constitution_to_charter.py
- tests/specify_cli/upgrade/migrations/test_m_*_rename_constitution_to_charter.py
task_type: implement
---

# Work Package Prompt: WP07 – User-Project Migration

## Objectives & Success Criteria

- Create upgrade migration that renames `.kittify/constitution/` → `.kittify/charter/` in user projects
- Migration handles: happy path (rename), no-op (no constitution dir), conflict (both exist → warn)
- Migration is idempotent (running twice is safe)
- All migration tests pass

## Context & Constraints

- **Spec**: `kitty-specs/063-rename-constitution-to-charter/spec.md` — User Story 3
- **Plan**: Stage 7 of 8. Depends on WP04 (kernel paths already point to `.kittify/charter/`).
- **Existing patterns**: See `src/specify_cli/upgrade/migrations/` for migration file conventions.
- **Tactic**: Smallest Viable Diff — one migration file + tests, nothing more.

## Branch Strategy

- **Strategy**: Feature branch
- **Planning base branch**: main
- **Merge target branch**: main

**Implementation command**: `spec-kitty implement WP07 --base WP04`

## Subtasks & Detailed Guidance

### Subtask T042 – Create migration file

- **Purpose**: Add a new migration following the existing naming convention.
- **Steps**:
  1. Check existing migrations to determine the next version number:
     `ls src/specify_cli/upgrade/migrations/m_*.py | tail -5`
  2. Create `src/specify_cli/upgrade/migrations/m_X_Y_Z_rename_constitution_to_charter.py` (use appropriate version)
  3. Follow the migration class pattern used by existing migrations:
     - `description` property
     - `apply(self, project_path, dry_run=False)` method
     - Use `get_agent_dirs_for_project()` if agent directories are involved (per CLAUDE.md guidance)
- **Files**: `src/specify_cli/upgrade/migrations/m_X_Y_Z_rename_constitution_to_charter.py` (new)
- **Parallel?**: No.

### Subtask T043 – Implement migration logic

- **Purpose**: The migration renames the directory and handles edge cases.
- **Steps**:
  1. Core logic:
     ```python
     constitution_dir = project_path / ".kittify" / "constitution"
     charter_dir = project_path / ".kittify" / "charter"

     if not constitution_dir.exists():
         return  # No-op: nothing to migrate

     if charter_dir.exists():
         # Conflict: both exist — warn and skip
         console.print("[yellow]Warning: both .kittify/constitution/ and .kittify/charter/ exist. "
                       "Skipping rename — please resolve manually.[/yellow]")
         return

     if not dry_run:
         constitution_dir.rename(charter_dir)
     ```
  2. Also check for internal file references (e.g., if `constitution.md` inside the dir references its own path)
  3. Log the migration action for user visibility
- **Files**: Migration file from T042
- **Parallel?**: No.

### Subtask T044 – Register migration in sequence

- **Purpose**: Ensure the migration runs during `spec-kitty upgrade`.
- **Steps**:
  1. Find the migration registry (likely in `src/specify_cli/upgrade/` — check `__init__.py` or a `registry.py`)
  2. Add the new migration to the ordered sequence
  3. Verify it's picked up by running `spec-kitty upgrade --dry-run` on a test project (if possible)
- **Files**: Migration registry file
- **Parallel?**: No.

### Subtask T045 – Write migration tests

- **Purpose**: Test all three scenarios: happy path, no-op, conflict.
- **Steps**:
  1. Create test file: `tests/specify_cli/upgrade/migrations/test_m_X_Y_Z_rename_constitution_to_charter.py`
  2. Test cases:
     - **Happy path**: Create `.kittify/constitution/` with `constitution.md` inside → run migration → assert `.kittify/charter/` exists, `.kittify/constitution/` does not, `charter.md` (or `constitution.md`) is inside charter dir
     - **No-op**: No `.kittify/constitution/` → run migration → no error, no `.kittify/charter/` created
     - **Conflict**: Both `.kittify/constitution/` and `.kittify/charter/` exist → run migration → warning emitted, both dirs unchanged
     - **Idempotency**: Run migration twice → second run is no-op
     - **Dry-run**: Run with `dry_run=True` → directory not renamed
  3. Use `tmp_path` fixture for filesystem isolation
- **Files**: `tests/specify_cli/upgrade/migrations/test_m_X_Y_Z_rename_constitution_to_charter.py` (new)
- **Parallel?**: No.

### Subtask T046 – Verify migration tests

- **Purpose**: Run the tests.
- **Steps**:
  1. `pytest tests/specify_cli/upgrade/migrations/test_m_X_Y_Z_rename_constitution_to_charter.py -v`
  2. Verify all 5 test cases pass
- **Parallel?**: No.

### Subtask T047 – Commit stage 7

- **Purpose**: Standalone commit.
- **Steps**: `git commit --no-gpg-sign -m "feat: add upgrade migration to rename .kittify/constitution → .kittify/charter (stage 7/8)"`
- **Parallel?**: No.

## Risks & Mitigations

- **Data loss on conflict**: If both directories exist, never overwrite — the migration warns and skips. User must resolve manually.
- **Windows compatibility**: Use `pathlib.Path.rename()` for cross-platform safety. On Windows, `rename()` may fail if the target exists — the conflict check prevents this.
- **Internal file references**: Files inside `.kittify/constitution/` may reference their own path in content — the migration only renames the directory, not file contents. This is acceptable for now.

## Review Guidance

- Verify the conflict case emits a warning (not an exception).
- Verify idempotency: running the migration twice is safe.
- Verify the migration follows existing patterns in the upgrade directory.
- Check the migration version number fits the sequence.

## Activity Log

- 2026-04-05T05:50:00Z – system – Prompt created.
