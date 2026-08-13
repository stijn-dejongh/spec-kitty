---
work_package_id: WP08
title: Retire the append-on-miss frontmatter writer
dependencies: []
requirement_refs:
- FR-006
planning_base_branch: spec/upgrade-atomicity-recovery
merge_target_branch: spec/upgrade-atomicity-recovery
branch_strategy: Planning artifacts for this mission were generated on spec/upgrade-atomicity-recovery. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into spec/upgrade-atomicity-recovery unless the human explicitly redirects the landing branch.
base_branch: kitty/mission-upgrade-atomicity-recovery-01KZWSHC
base_commit: 92053ea8bc0a05d72ba591a8af17b37b6f759172
created_at: '2026-08-13T09:12:08.724399+00:00'
subtasks:
- T023
- T024
- T025b
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
- tests/utils.py
- tests/task_utils/test_set_scalar_retired.py
tags: []
tracker_refs: []
---

# Work Package Prompt: WP08 – Retire the append-on-miss frontmatter writer

**Priority**: P2 | **Phase**: Phase 3 - Prevention | **Requirement Refs**: FR-006
**Mission**: `upgrade-atomicity-recovery-01KZWSHC` — see `../spec.md`, `../plan.md` (§Post-Plan Adversarial Revisions is binding), `../research.md`.

## Goal
The latent set_scalar append-on-miss path can never re-introduce a dual-key; the live writer stays single-key.

## Independent Test
No code path appends an inline review_feedback key; set_scalar is fail-closed; two review cycles yield exactly one review_feedback key.

## Subtasks
- [ ] T023 FAIL-CLOSE set_scalar in src/specify_cli/task_utils/support.py:186-204 (keep the symbol so task_utils/__init__.py + workflow.py re-exports stay valid; neutralize only the append-on-miss branch)
- [ ] T024 [P] Migrate tests/utils.py:175-177 set_scalar callers (lane/agent/assignee) to a supported writer
- [ ] T025b [P] SC-003 clause-1 pin: two consecutive review cycles on one WP produce exactly one review_feedback key (guards the live pointer-based writer against regression)

## Code seams (from research.md — verify before editing)
- src/specify_cli/task_utils/support.py:186-204 — set_scalar appends key: value on miss (the legacy dual-write mechanism). Zero production callers; re-exported by task_utils/__init__.py:28,54 + workflow.py:110 (so PREFER fail-close over delete to keep those imports valid).
- tests/utils.py:175-177 — the only remaining callers (lane/agent/assignee) — migrate them.

## Acceptance criteria (ATDD-first — land the failing test before the code)
1. set_scalar cannot append an inline review_feedback key (fail-closed; symbol retained).
2. tests/utils.py callers migrated; suite green.
3. SC-003 clause 1: two consecutive review cycles on one WP produce exactly one review_feedback key.

## Dependencies
None.

## Risks & notes
Prefer FAIL-CLOSE over deletion — deleting the symbol breaks unowned re-exports (task_utils/__init__.py, workflow.py). Only red is the test helper — migrate it in the same WP.

## Definition of Done
- All acceptance criteria pass; new helpers/branches carry focused tests (Sonar new-code coverage).
- **New `test_*.py` files MUST declare a `pytestmark` marker** (marker-convention CI gate — runs only in an integration job the fast local suites skip; a missing marker reds CI).
- `ruff` + `mypy` clean, zero suppressions; complexity <=15; terminology guard green.
- Changes match the corrected requirement wording in `../spec.md` and the binding revisions in `../plan.md`.
