# Research: Rename Constitution to Charter

## Decision: Staged vs Big-Bang Rename

**Decision**: Staged rename (bottom-up dependency order)
**Rationale**: The codebase has a layered import structure: `src/doctrine/` → `src/constitution/` → `src/specify_cli/constitution/` → CLI commands. Renaming bottom-up means each stage's imports resolve correctly against already-renamed dependencies. This follows the refactoring procedure's "apply in smallest viable steps" principle and allows each stage to be independently tested and committed.
**Alternative rejected**: Big-bang rename (all at once). Rejected because: harder to review, harder to bisect if something breaks, no incremental test verification.

## Decision: CLI Backward Compatibility Pattern

**Decision**: Typer deprecated alias with stderr warning
**Rationale**: Typer supports registering multiple command groups. Register `charter` as the primary group, then register a thin `constitution` wrapper that emits `warnings.warn()` with `DeprecationWarning` before delegating to the same implementation. This is the Strangler Fig tactic — new path alongside old, gradual migration, eventual removal.
**Alternative rejected**: Python `__getattr__` module-level alias. Rejected because: CLI is the public surface, not the Python API (C-006).

## Decision: User-Project Migration Strategy

**Decision**: Filesystem directory rename via upgrade migration
**Rationale**: User projects store constitution data in `.kittify/constitution/`. The migration renames this to `.kittify/charter/`. If both exist (edge case), warn and skip to avoid data loss. This is consistent with existing migration patterns in `src/specify_cli/upgrade/migrations/`.
**Alternative rejected**: Symlink from old to new. Rejected because: adds complexity, cross-platform issues (Windows), and doesn't cleanly resolve in all git operations.

## Decision: create-feature → create-mission Rename

**Decision**: Rename the CLI subcommand, no backward-compat alias
**Rationale**: This is a developer/agent-facing command, not a user-facing one. The existing architecture initiative (`architecture/2.x/initiatives/2026-04-mission-nomenclature-reconciliation/`) already documents this rename as planned. Since it's low-traffic and agent-invoked, a clean rename without alias is sufficient.
**Alternative rejected**: Deprecation alias (like constitution→charter). Rejected because: the command is only called by spec-kitty's own templates and agent workflows, which we control and can update simultaneously.

## Decision: Test File Rename Strategy

**Decision**: Rename `tests/constitution/` → `tests/charter/` in the final cleanup stage
**Rationale**: Test files import from the source modules. Renaming tests before source modules would break imports. Renaming them in the final stage (after all source renames) means a single pass of import updates in test files.
**Alternative rejected**: Rename test files alongside each source stage. Rejected because: tests often import across module boundaries (e.g., constitution CLI tests import from core constitution), so partial renames would create import errors mid-stage.

## Decision: Paradigm File Relocation

**Decision**: `git mv` to `shipped/` subdirectory
**Rationale**: The paradigm repository scans `shipped/` for discoverable paradigms. The `test-first.paradigm.yaml` file at the root of `src/doctrine/paradigms/` is not in this scan path. A simple move with `git mv` preserves history and makes it discoverable. Apply Move Field tactic.
**Alternative rejected**: Adding root-level scanning to the paradigm repository. Rejected because: the `shipped/` convention exists for a reason (separation of proposed vs shipped), and the file belongs in `shipped/`.
