---
work_package_id: WP04
title: CLI Registration, Deprecation Alias, and Dashboard
dependencies: [WP03]
requirement_refs:
- FR-004
- FR-005
planning_base_branch: 063-rename-constitution-to-charter
merge_target_branch: 063-rename-constitution-to-charter
branch_strategy: Planning artifacts for this feature were generated on 063-rename-constitution-to-charter. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into 063-rename-constitution-to-charter unless the human explicitly redirects the landing branch.
subtasks:
- T020
- T021
- T022
- T023
- T024
- T025
- T026
- T027
- T028
phase: Phase 2 - CLI Surface
assignee: ''
agent: ''
shell_pid: ''
history:
- at: '2026-04-05T05:50:00Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: python-implementer
authoritative_surface: src/specify_cli/cli/commands
execution_mode: code_change
lane: planned
owned_files:
- src/specify_cli/cli/commands/__init__.py
- src/specify_cli/cli/commands/agent/workflow.py
- src/specify_cli/cli/commands/charter.py
- src/specify_cli/cli/commands/shim.py
- src/specify_cli/dashboard/charter_path.py
task_type: implement
---

# Work Package Prompt: WP04 – CLI Registration, Deprecation Alias, and Dashboard

## Objectives & Success Criteria

- Rename CLI command file and registration: `constitution` → `charter`
- Add deprecation alias: `spec-kitty constitution` still works but emits warning
- Update shim dispatch, dashboard path resolver, and agent workflow function
- `spec-kitty charter --help` works
- `spec-kitty constitution --help` works + prints deprecation warning to stderr

## Context & Constraints

- **Spec**: `kitty-specs/063-rename-constitution-to-charter/spec.md` — User Story 2
- **Plan**: Stage 4 of 8. Depends on WP03 (specify_cli module renamed).
- **Tactic**: Strangler Fig — new `charter` alongside deprecated `constitution`
- **Constraint C-006**: Python import paths have no backward compat — only CLI alias

## Branch Strategy

- **Strategy**: Feature branch
- **Planning base branch**: main
- **Merge target branch**: main

**Implementation command**: `spec-kitty implement WP04 --base WP03`

## Subtasks & Detailed Guidance

### Subtask T020 – git mv constitution.py → charter.py (CLI)

- **Purpose**: Rename the CLI command module.
- **Steps**:
  1. `git mv src/specify_cli/cli/commands/constitution.py src/specify_cli/cli/commands/charter.py`
  2. Inside `charter.py`, update the Typer app:
     ```python
     app = typer.Typer(
         name="charter",
         help="Charter management commands",
         no_args_is_help=True,
     )
     ```
  3. Rename `_resolve_constitution_path()` → `_resolve_charter_path()`
  4. Update all internal references from "constitution" to "charter" in help strings, error messages, docstrings
- **Files**: `src/specify_cli/cli/commands/charter.py` (renamed from constitution.py)
- **Parallel?**: No.

### Subtask T021 – Update CLI registration in `__init__.py`

- **Purpose**: Wire the renamed module into the CLI app.
- **Steps**:
  1. In `src/specify_cli/cli/commands/__init__.py`:
     - Change `from . import constitution as constitution_module` → `from . import charter as charter_module`
     - Change `app.add_typer(constitution_module.app, name="constitution")` → `app.add_typer(charter_module.app, name="charter")`
- **Files**: `src/specify_cli/cli/commands/__init__.py`
- **Parallel?**: No.

### Subtask T022 – Add deprecation alias for constitution CLI

- **Purpose**: Keep `spec-kitty constitution` working with a deprecation warning.
- **Steps**:
  1. In `src/specify_cli/cli/commands/__init__.py`, after registering `charter`, add a deprecated `constitution` alias:
     ```python
     import warnings
     import sys

     _constitution_compat = typer.Typer(
         name="constitution",
         help="[DEPRECATED] Use 'spec-kitty charter' instead.",
         no_args_is_help=True,
         invoke_without_command=True,
     )

     @_constitution_compat.callback(invoke_without_command=True)
     def _constitution_deprecation_warning(ctx: typer.Context):
         warnings.warn(
             "'spec-kitty constitution' is deprecated. Use 'spec-kitty charter' instead.",
             DeprecationWarning,
             stacklevel=2,
         )
         # Forward to charter app
     ```
  2. **Recommended pattern**: Register `charter_module.app` as a second Typer group under the name `"constitution"`, but wrap it with a callback that prints the deprecation warning to stderr before forwarding. Concrete approach:
     ```python
     import sys

     # Primary registration
     app.add_typer(charter_module.app, name="charter")

     # Deprecated alias — re-register the SAME app object under the old name
     # with a callback that emits the deprecation warning
     @app.callback("constitution", invoke_without_command=True, hidden=True)
     def _constitution_compat(ctx: typer.Context):
         print(
             "DeprecationWarning: 'spec-kitty constitution' is deprecated. "
             "Use 'spec-kitty charter' instead.",
             file=sys.stderr,
         )
     ```
     If Typer doesn't support `@app.callback("constitution")`, use the alternative: create a thin Typer subapp that mirrors all subcommands by importing them from `charter_module.app` and adding the warning in its callback. The simplest working approach is to register `charter_module.app` under both names and add a `rich.console.Console(stderr=True).print()` warning in a custom callback for the `constitution` name.
  3. Write a test that invokes the deprecated command and asserts the warning appears on stderr.
- **Files**: `src/specify_cli/cli/commands/__init__.py`
- **Parallel?**: No.
- **Notes**: The key requirement is: `spec-kitty constitution context --action specify --json` must work AND emit a warning to stderr. Use `print(..., file=sys.stderr)` rather than `warnings.warn()` for reliable stderr output in CLI context.

### Subtask T023 – Update shim dispatch

- **Purpose**: Update the shim to dispatch `charter` instead of `constitution`.
- **Steps**:
  1. In `src/specify_cli/cli/commands/shim.py`, find the `@app.command(name="constitution")` block (~line 201)
  2. Rename to `@app.command(name="charter")`
  3. Update function name: `shim_constitution` → `shim_charter`
  4. Update the `_run("constitution", ...)` call to `_run("charter", ...)`
  5. Add a deprecated `constitution` shim that forwards to charter (if the shim layer also needs backward compat)
- **Files**: `src/specify_cli/cli/commands/shim.py`
- **Parallel?**: No.

### Subtask T024 – git mv constitution_path.py → charter_path.py

- **Purpose**: Rename dashboard path resolver module.
- **Steps**:
  1. `git mv src/specify_cli/dashboard/constitution_path.py src/specify_cli/dashboard/charter_path.py`
  2. Rename function: `resolve_project_constitution_path` → `resolve_project_charter_path`
  3. Update docstring and internal path references (`.kittify/constitution/` → `.kittify/charter/`)
  4. Update all importers of this function across `src/`
- **Files**: `src/specify_cli/dashboard/charter_path.py`, importers
- **Parallel?**: Yes (parallel with T025).

### Subtask T025 – Rename _render_constitution_context

- **Purpose**: Update the agent workflow helper function.
- **Steps**:
  1. In `src/specify_cli/cli/commands/agent/workflow.py`, rename `_render_constitution_context` → `_render_charter_context` (~line 116)
  2. Update all callers of this function within the same file
  3. Update any string references to "constitution" in the function body (help text, path references)
- **Files**: `src/specify_cli/cli/commands/agent/workflow.py`
- **Parallel?**: Yes (parallel with T024).

### Subtask T026 – Update dashboard/agent/CLI test imports

- **Purpose**: Fix test files that import the renamed modules.
- **Steps**:
  1. `grep -rn "constitution_path\|constitution_cli\|_render_constitution_context\|shim_constitution" tests/ --include="*.py"`
  2. Update all found imports and references
  3. Update any test assertions checking for "constitution" in CLI output — ensure deprecation tests check for warning
- **Files**: `tests/specify_cli/cli/commands/test_constitution_cli.py` (rename or update), `tests/agent/test_workflow_constitution_context.py`, `tests/test_dashboard/test_api_constitution.py`
- **Parallel?**: No.

### Subtask T027 – CLI smoke test + pytest

- **Purpose**: Verify the CLI works end-to-end.
- **Steps**:
  1. `spec-kitty charter --help` — must work
  2. `spec-kitty constitution --help` — must work + emit deprecation warning
  3. `pytest tests/specify_cli/cli/` — all CLI tests pass
  4. `pytest tests/agent/` — agent workflow tests pass
  5. `pytest tests/test_dashboard/` — dashboard tests pass
- **Parallel?**: No.

### Subtask T028 – Commit stage 4

- **Purpose**: Standalone commit.
- **Steps**: `git commit --no-gpg-sign -m "refactor: rename CLI constitution → charter with deprecation alias (stage 4/8)"`
- **Parallel?**: No.

## Risks & Mitigations

- **Typer deprecation pattern**: Typer may not natively support command aliases with warnings — may need a callback-based approach or a thin wrapper Typer app.
- **Shim backward compat**: The shim layer may also need a `constitution` entry for `spec-kitty` shim dispatch — investigate.
- **Test assertions**: Tests may assert on CLI output strings containing "constitution" — update to match new output.

## Review Guidance

- Test both `spec-kitty charter` and `spec-kitty constitution` manually.
- Verify deprecation warning appears on stderr (not stdout).
- Verify the shim dispatches correctly for both names.
- This is the critical gate — if Stage 4 passes, the rest is text replacement.

## Activity Log

- 2026-04-05T05:50:00Z – system – Prompt created.
