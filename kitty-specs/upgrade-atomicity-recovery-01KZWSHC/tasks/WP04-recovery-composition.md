---
work_package_id: WP04
title: Recovery composition — end-to-end, zero-git
dependencies:
- WP01
- WP03
requirement_refs:
- FR-001
- NFR-002
planning_base_branch: spec/upgrade-atomicity-recovery
merge_target_branch: spec/upgrade-atomicity-recovery
branch_strategy: Planning artifacts for this mission were generated on spec/upgrade-atomicity-recovery. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into spec/upgrade-atomicity-recovery unless the human explicitly redirects the landing branch.
subtasks:
- T012
- T013
- T014
phase: Phase 1 - Recovery
history:
- timestamp: '2026-08-13T00:00:00Z'
  agent: system
  action: Prompt generated via /spec-kitty.tasks
authoritative_surface: src/specify_cli/upgrade/
create_intent:
- src/specify_cli/upgrade/recovery.py
- tests/upgrade/test_recovery_composition.py
execution_mode: code_change
owned_files:
- src/specify_cli/upgrade/recovery.py
- tests/upgrade/test_recovery_composition.py
tags: []
tracker_refs: []
---

# Work Package Prompt: WP04 – Recovery composition — end-to-end, zero-git

**Priority**: P1 | **Phase**: Phase 1 - Recovery | **Requirement Refs**: FR-001, NFR-002
**Mission**: `upgrade-atomicity-recovery-01KZWSHC` — see `../spec.md`, `../plan.md` (§Post-Plan Adversarial Revisions is binding), `../research.md`.

## Goal
Compose FR-002 + FR-008 + FR-012 so a wedged project self-recovers (SC-001), including a project not under version control.

## Independent Test
A wedged project (incl. one not under version control) recovers to an upgradable state with zero manual git steps.

## Subtasks
- [ ] T012 Wire the recovery flow (no new command unless proven necessary); adopt ADR 2026-05-10-1 non-destructive+deterministic principles
- [ ] T013 [P] Acceptance: SC-001 zero manual git recovery
- [ ] T014 [P] Acceptance: no-VCS wedged-project recovery (on-disk, no git checkpoint)

## Code seams (from research.md — verify before editing)
- Composition of WP01 (schema preserve) + WP03 (artifact repair) + WP01 (FR-012 resume). No net-new command unless FR-002+FR-008+re-run is proven insufficient.
- ADR docs/adr/3.x/2026-05-10-1-deterministic-historical-mission-state-repair.md — principles + mission_state machinery.

## Acceptance criteria (ATDD-first — land the failing test before the code)
1. SC-001: wedged project recovers with zero manual git steps.
2. No-VCS project recovers on-disk without requiring a git checkpoint.

## Dependencies
WP01, WP03 (genuine dependency edge — gates claiming).

## Risks & notes
Keep FR-001 scoped as composition/wiring — not a parallel unknown. Depends on WP01+WP03.

## Definition of Done
- All acceptance criteria pass; new helpers/branches carry focused tests (Sonar new-code coverage).
- `ruff` + `mypy` clean, zero suppressions; complexity <=15; terminology guard green.
- Changes match the corrected requirement wording in `../spec.md` and the binding revisions in `../plan.md`.
