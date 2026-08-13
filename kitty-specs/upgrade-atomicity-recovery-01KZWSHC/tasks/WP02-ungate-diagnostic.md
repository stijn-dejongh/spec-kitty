---
work_package_id: WP02
title: Ungate the recommended diagnostic
dependencies: []
requirement_refs:
- FR-003
planning_base_branch: spec/upgrade-atomicity-recovery
merge_target_branch: spec/upgrade-atomicity-recovery
branch_strategy: Planning artifacts for this mission were generated on spec/upgrade-atomicity-recovery. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into spec/upgrade-atomicity-recovery unless the human explicitly redirects the landing branch.
subtasks:
- T005
- T006
phase: Phase 1 - Recovery
history:
- timestamp: '2026-08-13T00:00:00Z'
  agent: system
  action: Prompt generated via /spec-kitty.tasks
authoritative_surface: src/specify_cli/compat/
create_intent:
- tests/compat/test_diagnostic_safe_predicate.py
execution_mode: code_change
owned_files:
- src/specify_cli/compat/safety.py
- tests/compat/test_diagnostic_safe_predicate.py
tags: []
tracker_refs: []
---

# Work Package Prompt: WP02 – Ungate the recommended diagnostic

**Priority**: P0 | **Phase**: Phase 1 - Recovery | **Requirement Refs**: FR-003
**Mission**: `upgrade-atomicity-recovery-01KZWSHC` — see `../spec.md`, `../plan.md` (§Post-Plan Adversarial Revisions is binding), `../research.md`.

## Goal
`migrate backfill-runtime-state --dry-run` is reachable on a wedged project — fixes the #3338 circularity.

## Independent Test
On a LEGACY/blocked project the --dry-run diagnostic runs and reports the cause; the mutating form stays blocked.

## Subtasks
- [ ] T005 Register ('migrate','backfill-runtime-state') SAFE via a fail-closed --dry-run predicate in src/specify_cli/compat/safety.py
- [ ] T006 [P] Test: predicate returns SAFE iff --dry-run present; UNSAFE otherwise and on predicate exception

## Code seams (from research.md — verify before editing)
- src/specify_cli/compat/safety.py:86,145-147 — only the bare ('migrate',) path is registered; classify() fails closed on the missing subcommand path -> UNSAFE -> BLOCK.
- src/specify_cli/compat/safety.py:113-134 — register_safety predicate mechanism (predicate receives the Invocation with raw_args).
- src/specify_cli/upgrade/migrations/m_zz_runtime_state_backfill.py:114-116 — the abort message recommends exactly this command.

## Acceptance criteria (ATDD-first — land the failing test before the code)
1. The --dry-run diagnostic is SAFE and runs on a blocked project.
2. The mutating form (no --dry-run) remains UNSAFE (fail-closed); a predicate exception is treated UNSAFE.

## Dependencies
None.

## Risks & notes
Predicate must fail closed — never open the mutating migration path under schema mismatch.

## Definition of Done
- All acceptance criteria pass; new helpers/branches carry focused tests (Sonar new-code coverage).
- **New `test_*.py` files MUST declare a `pytestmark` marker** (marker-convention CI gate — runs only in an integration job the fast local suites skip; a missing marker reds CI).
- `ruff` + `mypy` clean, zero suppressions; complexity <=15; terminology guard green.
- Changes match the corrected requirement wording in `../spec.md` and the binding revisions in `../plan.md`.
