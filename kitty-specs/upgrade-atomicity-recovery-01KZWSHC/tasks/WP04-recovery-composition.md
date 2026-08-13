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
authoritative_surface: tests/upgrade/
create_intent:
- tests/upgrade/test_recovery_composition.py
execution_mode: code_change
owned_files:
- tests/upgrade/test_recovery_composition.py
tags: []
tracker_refs: []
---

# Work Package Prompt: WP04 – Recovery composition — end-to-end, zero-git

**Priority**: P1 | **Phase**: Phase 1 - Recovery | **Requirement Refs**: FR-001, NFR-002
**Mission**: `upgrade-atomicity-recovery-01KZWSHC` — see `../spec.md`, `../plan.md` (§Post-Plan Adversarial Revisions is binding), `../research.md`.

## Goal
Prove FR-002 + FR-008 + FR-012 compose so a wedged project self-recovers (SC-001), including a project not under version control — without minting a new orchestration surface.

## Independent Test
A wedged project (incl. one not under version control) recovers to an upgradable state with zero manual git steps.

## Subtasks
- [ ] T012 Prove recovery composes as a SEQUENCE (doctor --fix -> re-run upgrade) via acceptance tests — this is a VERIFICATION WP (like WP07), owns only its test. Mint upgrade/recovery.py ONLY if a single auto-heal invocation is proven necessary; if so, fold the hook into WP01's runner.py scope (do NOT create a 4th orchestration surface).
- [ ] T013 [P] Acceptance: SC-001 zero manual git recovery (end-to-end sequence)
- [ ] T014 [P] Acceptance: no-VCS wedged-project recovery (on-disk, no git checkpoint)

## Code seams (from research.md — verify before editing)
- Composition of WP01 (schema preserve) + WP03 (doctor --fix repair) + WP01 (FR-012 resume). paula-patterns post-tasks finding: no existing recovery orchestrator and none needed — recovery is the SEQUENCE, so WP04 is a verification WP owning only its acceptance test.
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
- **New `test_*.py` files MUST declare a `pytestmark` marker** (marker-convention CI gate — runs only in an integration job the fast local suites skip; a missing marker reds CI).
- `ruff` + `mypy` clean, zero suppressions; complexity <=15; terminology guard green.
- Changes match the corrected requirement wording in `../spec.md` and the binding revisions in `../plan.md`.
