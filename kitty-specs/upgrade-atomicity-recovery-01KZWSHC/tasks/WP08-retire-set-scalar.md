---
work_package_id: WP08
title: Retire the append-on-miss frontmatter writer
dependencies: []
requirement_refs:
- FR-006
planning_base_branch: spec/upgrade-atomicity-recovery
merge_target_branch: spec/upgrade-atomicity-recovery
branch_strategy: Planning artifacts for this mission were generated on spec/upgrade-atomicity-recovery. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into spec/upgrade-atomicity-recovery unless the human explicitly redirects the landing branch.
subtasks:
- T023
- T024
phase: Phase 3 - Prevention
history:
- timestamp: '2026-08-13T00:00:00Z'
  agent: system
  action: Prompt generated via /spec-kitty.tasks
authoritative_surface: src/specify_cli/task_utils/
create_intent:
- tests/task_utils/test_set_scalar_retired.py
execution_mode: code_change
owned_files:
- src/specify_cli/task_utils/support.py
- tests/task_utils/test_set_scalar_retired.py
tags: []
tracker_refs: []
---

# Work Package Prompt: WP08 – Retire the append-on-miss frontmatter writer

**Priority**: P2 | **Phase**: Phase 3 - Prevention | **Requirement Refs**: FR-006
**Mission**: `upgrade-atomicity-recovery-01KZWSHC` — see `../spec.md`, `../plan.md` (§Post-Plan Adversarial Revisions is binding), `../research.md`.

## Goal
The latent set_scalar append-on-miss path can never re-introduce a dual-key.

## Independent Test
No code path appends an inline review_feedback key; set_scalar is retired/fail-closed and its test callers migrated.

## Subtasks
- [ ] T023 Retire or fail-close set_scalar in src/specify_cli/task_utils/support.py:186-204
- [ ] T024 [P] Migrate tests/utils.py:175-177 set_scalar callers to a supported writer

## Code seams (from research.md — verify before editing)
- src/specify_cli/task_utils/support.py:186-204 — set_scalar appends key: value on miss (the legacy dual-write mechanism). Zero production callers.
- tests/utils.py:175-177 — the only remaining callers (lane/agent/assignee) — migrate them.

## Acceptance criteria (ATDD-first — land the failing test before the code)
1. set_scalar cannot append an inline review_feedback key (retired or fail-closed).
2. tests/utils.py callers migrated; suite green.

## Dependencies
None.

## Risks & notes
Only red is the test helper — migrate it in the same WP so nothing goes red on main.

## Definition of Done
- All acceptance criteria pass; new helpers/branches carry focused tests (Sonar new-code coverage).
- `ruff` + `mypy` clean, zero suppressions; complexity <=15; terminology guard green.
- Changes match the corrected requirement wording in `../spec.md` and the binding revisions in `../plan.md`.
