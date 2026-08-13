---
work_package_id: WP05
title: Report-on-abort for the bulk cutover
dependencies: []
requirement_refs:
- FR-005
- NFR-003
planning_base_branch: spec/upgrade-atomicity-recovery
merge_target_branch: spec/upgrade-atomicity-recovery
branch_strategy: Planning artifacts for this mission were generated on spec/upgrade-atomicity-recovery. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into spec/upgrade-atomicity-recovery unless the human explicitly redirects the landing branch.
subtasks:
- T015
- T016
- T017
phase: Phase 2 - Atomicity
history:
- timestamp: '2026-08-13T00:00:00Z'
  agent: system
  action: Prompt generated via /spec-kitty.tasks
authoritative_surface: src/specify_cli/upgrade/migrations/
create_intent:
- tests/upgrade/test_backfill_report_on_abort.py
execution_mode: code_change
owned_files:
- src/specify_cli/upgrade/migrations/m_zz_runtime_state_backfill.py
- src/specify_cli/upgrade/migrations/base.py
- tests/upgrade/test_backfill_report_on_abort.py
tags: []
tracker_refs: []
---

# Work Package Prompt: WP05 – Report-on-abort for the bulk cutover

**Priority**: P1 | **Phase**: Phase 2 - Atomicity | **Requirement Refs**: FR-005, NFR-003
**Mission**: `upgrade-atomicity-recovery-01KZWSHC` — see `../spec.md`, `../plan.md` (§Post-Plan Adversarial Revisions is binding), `../research.md`.

## Goal
A non-atomic abort enumerates every mission/file already written — no silent partial write.

## Independent Test
Backfill over a fixture where mission K fails -> abort output lists every mission/file already written.

## Subtasks
- [ ] T015 Stop discarding _cutover_corpus results on abort in src/specify_cli/upgrade/migrations/m_zz_runtime_state_backfill.py::apply (:284-286)
- [ ] T016 Add a machine-readable partial-write account (extend MigrationResult, upgrade/migrations/base.py:11-16)
- [ ] T017 [P] Test: graceful-abort enumeration matches what was written

## Code seams (from research.md — verify before editing)
- src/specify_cli/upgrade/migrations/m_zz_runtime_state_backfill.py:196-227,284-286 — _cutover_corpus returns (results, abort_message); apply() DISCARDS results on abort. Feed them into the failure MigrationResult.
- src/specify_cli/upgrade/migrations/base.py:11-16 — MigrationResult has no partial-write channel; add one.
- src/specify_cli/migration/runtime_state_cutover.py:94-99 — CutoverResult carries slug/flipped/seeded_count (derive file paths per mission).

## Acceptance criteria (ATDD-first — land the failing test before the code)
1. Graceful abort enumerates every mission/file written (FR-005/NFR-003).
2. Successful run reports a truthful count.

## Dependencies
None.

## Risks & notes
Scope to GRACEFUL abort. SIGKILL/durable cross-run accounting is WP06/#2933 territory. Recovery is roll-forward (detect()-gated re-run).

## Definition of Done
- All acceptance criteria pass; new helpers/branches carry focused tests (Sonar new-code coverage).
- `ruff` + `mypy` clean, zero suppressions; complexity <=15; terminology guard green.
- Changes match the corrected requirement wording in `../spec.md` and the binding revisions in `../plan.md`.
