---
work_package_id: WP07
title: Event-log / reducer integrity after recovery
dependencies:
- WP01
- WP05
requirement_refs:
- NFR-005
planning_base_branch: spec/upgrade-atomicity-recovery
merge_target_branch: spec/upgrade-atomicity-recovery
branch_strategy: Planning artifacts for this mission were generated on spec/upgrade-atomicity-recovery. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into spec/upgrade-atomicity-recovery unless the human explicitly redirects the landing branch.
subtasks:
- T021
- T022
phase: Phase 2 - Atomicity
history:
- timestamp: '2026-08-13T00:00:00Z'
  agent: system
  action: Prompt generated via /spec-kitty.tasks
authoritative_surface: tests/status/
create_intent:
- tests/status/test_reducer_recovery_integrity.py
execution_mode: code_change
owned_files:
- tests/status/test_reducer_recovery_integrity.py
tags: []
tracker_refs: []
---

# Work Package Prompt: WP07 – Event-log / reducer integrity after recovery

**Priority**: P1 | **Phase**: Phase 2 - Atomicity | **Requirement Refs**: NFR-005
**Mission**: `upgrade-atomicity-recovery-01KZWSHC` — see `../spec.md`, `../plan.md` (§Post-Plan Adversarial Revisions is binding), `../research.md`.

## Goal
Recovery never breaks reducer determinism or append-only integrity.

## Independent Test
reduce() over the recovered log == pre-abort log ∪ committed events; a re-run appends no duplicate transitions.

## Subtasks
- [ ] T021 Half-applied-backfill fixture builder in tests/
- [ ] T022 Assert reducer-determinism + event_id de-dup + detect()-gating idempotency

## Code seams (from research.md — verify before editing)
- src/specify_cli/status/reducer.py — reduce()/materialize; event_id de-dup.
- runtime_state_cutover detect()/_mission_needs_cutover — idempotency gate (already-cut-over missions skipped).

## Acceptance criteria (ATDD-first — land the failing test before the code)
1. reduce() over recovered log == pre-abort ∪ committed events (no divergence).
2. Re-run after partial backfill appends no duplicate transitions.

## Dependencies
WP01, WP05 (genuine dependency edge — gates claiming).

## Risks & notes
Verification WP (fixtures + asserts, no product code). Depends on WP01+WP05.

## Definition of Done
- All acceptance criteria pass; new helpers/branches carry focused tests (Sonar new-code coverage).
- **New `test_*.py` files MUST declare a `pytestmark` marker** (marker-convention CI gate — runs only in an integration job the fast local suites skip; a missing marker reds CI).
- `ruff` + `mypy` clean, zero suppressions; complexity <=15; terminology guard green.
- Changes match the corrected requirement wording in `../spec.md` and the binding revisions in `../plan.md`.
