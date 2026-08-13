---
work_package_id: WP10
title: Honest dry-run preview
dependencies: []
requirement_refs:
- FR-009
planning_base_branch: spec/upgrade-atomicity-recovery
merge_target_branch: spec/upgrade-atomicity-recovery
branch_strategy: Planning artifacts for this mission were generated on spec/upgrade-atomicity-recovery. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into spec/upgrade-atomicity-recovery unless the human explicitly redirects the landing branch.
subtasks:
- T027
- T028
phase: Phase 4 - Observability
history:
- timestamp: '2026-08-13T00:00:00Z'
  agent: system
  action: Prompt generated via /spec-kitty.tasks
authoritative_surface: src/specify_cli/compat/
create_intent:
- tests/compat/test_dry_run_parity.py
execution_mode: code_change
owned_files:
- src/specify_cli/cli/commands/upgrade.py
- src/specify_cli/compat/planner.py
- src/specify_cli/compat/messages.py
- src/specify_cli/upgrade/detector.py
- tests/compat/test_dry_run_parity.py
tags: []
tracker_refs: []
---

# Work Package Prompt: WP10 – Honest dry-run preview

**Priority**: P2 | **Phase**: Phase 4 - Observability | **Requirement Refs**: FR-009
**Mission**: `upgrade-atomicity-recovery-01KZWSHC` — see `../spec.md`, `../plan.md` (§Post-Plan Adversarial Revisions is binding), `../research.md`.

## Goal
`upgrade --dry-run` reports the real pending set (drive the preview through the real detector).

## Independent Test
On a project with M pending migrations, --dry-run reports exactly those M.

## Subtasks
- [ ] T027 Route the dry-run/--json preview through MigrationRegistry.get_applicable (upgrade/detector.py) instead of the divergent planner path (compat/planner.py:1027)
- [ ] T028 [P] Test: preview pending set == real applied set

## Code seams (from research.md — verify before editing)
- src/specify_cli/cli/commands/upgrade.py:688-694,751 — dry-run/--json short-circuits into the planner; the real run uses MigrationRegistry.get_applicable.
- src/specify_cli/compat/planner.py:1027 — pending_migrations gated on BLOCK_PROJECT_MIGRATION (returns () otherwise).
- src/specify_cli/compat/messages.py:147-159 — render_json emits [] (the 'null' framing is stale — fix the divergence, not the serializer).

## Acceptance criteria (ATDD-first — land the failing test before the code)
1. Preview pending set equals the real applied set (drive preview through the same detector).
2. Block-decision semantics preserved.

## Dependencies
None.

## Risks & notes
Unify the computation without regressing the block decision.

## Definition of Done
- All acceptance criteria pass; new helpers/branches carry focused tests (Sonar new-code coverage).
- `ruff` + `mypy` clean, zero suppressions; complexity <=15; terminology guard green.
- Changes match the corrected requirement wording in `../spec.md` and the binding revisions in `../plan.md`.
