---
work_package_id: WP07
title: 'Wave 4: bulk-edit cutover for src/ code (FR-015 a-d)'
dependencies:
- WP04
- WP06
requirement_refs:
- FR-015
planning_base_branch: main
merge_target_branch: main
branch_strategy: Planning artifacts for this mission were generated on main. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into main unless the human explicitly redirects the landing branch.
subtasks:
- T040
- T041
- T042
- T043
- T044
- T045
agent: claude
history:
- by: claude
  at: '2026-05-23T13:30:00+00:00'
  action: generated
agent_profile: python-pedro
authoritative_surface: src/
execution_mode: code_change
mission_id: 01KSAF14K8FZ56MHYT45EGWHHC
mission_slug: charter-ux-and-org-pack-vocabulary-01KSAF14
owned_files:
- architecture/3.x/adr/2026-05-DD-3-shipped-to-built-in-cutover.md
- src/doctrine/base.py
- src/specify_cli/cli/commands/profiles_cmd.py
- src/charter/drg.py
priority: P1
role: implementer
tags: []
---

## ⚡ Do This First: Load Agent Profile

Invoke `/ad-hoc-profile-load` with argument `python-pedro` before reading further. Pedro's `refactor` + `python` domains carry the Python identifier-rename mechanics. ALSO load the `spec-kitty-bulk-edit-classification` skill — this WP is the first WP in Wave 4, and the bulk-edit gate is active.

## Objective

Execute the `shipped → built-in` rename across all source-code surfaces per `occurrence_map.yaml`. Land ADR-3 (the cutover decision) first. Touch Python identifiers, comments, docstrings, log messages, advisory strings, and JSON values. Tests (`tests/`) are owned by WP08; docs/CHANGELOG by WP09 — DO NOT touch them here.

## Branch strategy

- Planning base branch: `main`
- Merge target branch: `main`
- Execution worktree: allocated by `finalize-tasks`. This WP's worktree may have heavy churn — coordinate with the lane assignment.

## Context

- `kitty-specs/.../occurrence_map.yaml` — authoritative classification per file/category
- `kitty-specs/.../spec.md` — FR-015 a-d (parts e/f are WP08/WP09)
- `kitty-specs/.../research.md` — R-3 (straight cutover, no deprecation), R-9 (advisory text already reworded by WP06)
- `kitty-specs/.../research/mission-brief.md` — §2 Thread C quantification

## Subtask details

### T040 — ADR-3 (`2026-05-DD-3-shipped-to-built-in-cutover.md`)

**Files**: `architecture/3.x/adr/2026-05-DD-3-shipped-to-built-in-cutover.md` (NEW)

Outline:
- **Problem**: Vocabulary asymmetry — on-disk directories use `built-in/` but Python identifiers, JSON values, log messages, and tests use `shipped`.
- **Decision**: Straight cutover with CHANGELOG breaking-change entry (per R-3). No deprecation window.
- **Alternatives considered**: Dual-emit during deprecation period (rejected).
- **Consequences**: Breaks external tooling that pattern-matches `"shipped"`. Documented in CHANGELOG (WP09). Architectural regression test FR-016 (WP08) prevents regression.
- **Cross-references**: `2026-05-16-1-doctrine-layer-merge-semantics.md`.

### T041 — Rename in `src/doctrine/base.py`

**Files**: `src/doctrine/base.py`

Per occurrence_map `code_symbols` row:
- `_shipped_dir` → `_built_in_dir`
- `_load_shipped_items` → `_load_built_in_items`
- `_apply_org_overrides(yaml_parser, shipped)` parameter `shipped` → `built_in` (and all internal references)
- `_apply_project_overrides(yaml_parser, shipped)` same parameter rename
- Docstrings mentioning "shipped → org → project" → "built-in → org → project"
- All log lines (e.g. "Skipping invalid shipped {kind}") → "Skipping invalid built-in {kind}"

### T042 — Rename in `src/specify_cli/charter_lint/` + `cli/commands/charter.py`

**Files**: `src/specify_cli/charter_lint/_drg.py`, `engine.py`, `findings.py`, `src/specify_cli/cli/commands/charter.py`

Rename all comments / log messages referencing "shipped" as the layer label. Verify no symbol drift with WP01 (the `GraphState.BUILT_IN_ONLY` value already uses the target term).

Particular hot-spots:
- `charter.py::charter_lint` (line ~3082) — comments and the per-layer marker block (the human banner already prints `[built-in]`, so no banner change; comments above the block reference "shipped" — rename).
- `_drg.py` lazy-import comments.

### T043 — Rename across remaining `src/` Python files

**Files**: All other `src/` Python files matching `grep -rn shipped src/ --include='*.py'` per the occurrence_map's `code_symbols` action.

Bound the change to identifier renames, comment updates, and docstring fixes. Do NOT change:
- The `built-in/` directory names on disk (already correct).
- Any test file (WP08).
- Any doc file (WP09).
- Variables/functions in `architecture/.../adr/*-2026-05-16-1-*.md` historical text (preserve-historical).

Verify with `grep -rn shipped src/ --include='*.py' | grep -v __pycache__` returning 0 matches in scope.

### T044 — Update user-facing log/advisory strings

**Files**: same as T041-T043

Coordinate with WP06's advisory rewording (`_intent_aware_collision_messages` already uses "built-in" per `contracts/pack-validator-advisory.md`). Verify that:
- Every error/warning message containing "shipped" as a layer label is updated.
- No regression in WP06's wording.

### T045 — `profiles_cmd.py` + delete `_warn_project_override` conversion

**Files**: `src/specify_cli/cli/commands/profiles_cmd.py`, `src/charter/drg.py`

In `profiles_cmd.py` line ~56:
```python
# OLD:
source = "project_local" if getattr(p, "_source", None) == "project" else "shipped"
# NEW:
source = "project_local" if getattr(p, "_source", None) == "project" else "built-in"
```

In `src/charter/drg.py` line ~322-336 (`_warn_project_override`):
```python
# OLD:
layer_label = "shipped" if existing_provenance == "built-in" else existing_provenance
_logger.warning("Project doctrine overrides %s node ...", layer_label, ...)

# NEW: drop the conversion entirely — emit the provenance directly.
_logger.warning(
    "Project doctrine overrides %s node %r (was provenance=%r). "
    "This is allowed by design (project > org > built-in precedence); "
    "flag here for operator visibility.",
    existing_provenance,
    urn,
    existing_provenance,
)
```

The conversion is dead per occurrence_map `dead_code_or_drift` — delete, don't merely rename.

## Definition of Done

- [ ] ADR-3 file exists and cross-references `2026-05-16-1`.
- [ ] `src/doctrine/base.py` has no `shipped` identifier; comments updated.
- [ ] `src/specify_cli/charter_lint/` and `cli/commands/charter.py` have no `shipped` references except inside preserved-historical text (none expected).
- [ ] All other `src/` Python files clean of `shipped` per occurrence_map.
- [ ] `profiles_cmd.py` emits `"built-in"` JSON value.
- [ ] `_warn_project_override` conversion deleted (not merely renamed).
- [ ] `mypy --strict` and `ruff check` pass.
- [ ] `pytest tests/` passes — but cross-cutting test failures from this rename are EXPECTED here and are owned by WP08.

## Risks

- **Test cascade**: many tests assert `"shipped"` literally. Cross-cutting failures appear here; they will be fixed in WP08. Communicate this clearly in commit messages and notes — do NOT bend tests in this WP to keep them green.
- **WP06 sequencing**: WP06's reworded advisory text uses "built-in" already, so no conflict. Confirm by visual inspection of `pack_validator.py` after WP06 merges.
- **Bulk-edit gate**: every commit MUST trace to an occurrence_map row. Use small, focused commits aligned with the categories.

## Reviewer guidance

1. Verify the conversion in `_warn_project_override` is **deleted**, not renamed (occurrence_map `dead_code_or_drift`).
2. Verify the `profiles_cmd.py` JSON value emits `"built-in"` and existing tests for that command are flagged for WP08 attention.
3. Spot-check that no historical ADR/CHANGELOG/spec text was modified.
