---
work_package_id: WP12
title: Mission-create checkout restore
dependencies: []
requirement_refs:
- FR-011
planning_base_branch: spec/upgrade-atomicity-recovery
merge_target_branch: spec/upgrade-atomicity-recovery
branch_strategy: Planning artifacts for this mission were generated on spec/upgrade-atomicity-recovery. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into spec/upgrade-atomicity-recovery unless the human explicitly redirects the landing branch.
base_branch: kitty/mission-upgrade-atomicity-recovery-01KZWSHC
base_commit: 92053ea8bc0a05d72ba591a8af17b37b6f759172
created_at: '2026-08-13T09:25:04.070096+00:00'
subtasks:
- T031
- T032
phase: Phase 5 - Hygiene
history:
- timestamp: '2026-08-13T00:00:00Z'
  agent: system
  action: Prompt generated via /spec-kitty.tasks
authoritative_surface: src/specify_cli/core/
create_intent:
- tests/core/test_mission_create_checkout_restore.py
execution_mode: code_change
owned_files:
- src/specify_cli/core/mission_creation.py
- tests/core/test_mission_create_checkout_restore.py
tags: []
tracker_refs: []
---

# Work Package Prompt: WP12 – Mission-create checkout restore

**Priority**: P3 | **Phase**: Phase 5 - Hygiene | **Requirement Refs**: FR-011
**Mission**: `upgrade-atomicity-recovery-01KZWSHC` — see `../spec.md`, `../plan.md` (§Post-Plan Adversarial Revisions is binding), `../research.md`.

## Goal
A failed mission-create restores the operator's branch/checkout and leaves no orphan branch.

## Independent Test
A mission-create that fails after creating a branch restores the original checkout with no orphan branch.

## Subtasks
- [ ] T031 Restore branch/checkout on mission-create failure
- [ ] T032 [P] Test: failed create -> original branch, no orphan branch

## Code seams (from research.md — verify before editing)
- mission-create git side-effects (#3339) — coordinate with #3328's mission-create git-side-effect rework to avoid double-fixing.

## Acceptance criteria (ATDD-first — land the failing test before the code)
1. A failed mission-create restores the original checkout and leaves no orphan branch.

## Dependencies
None.

## Risks & notes
External-coordination risk (#3328).

## Definition of Done
- All acceptance criteria pass; new helpers/branches carry focused tests (Sonar new-code coverage).
- **New `test_*.py` files MUST declare a `pytestmark` marker** (marker-convention CI gate — runs only in an integration job the fast local suites skip; a missing marker reds CI).
- `ruff` + `mypy` clean, zero suppressions; complexity <=15; terminology guard green.
- Changes match the corrected requirement wording in `../spec.md` and the binding revisions in `../plan.md`.
