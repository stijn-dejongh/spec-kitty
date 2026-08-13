---
work_package_id: WP11
title: Remediation body survives --json
dependencies: []
requirement_refs:
- FR-010
planning_base_branch: spec/upgrade-atomicity-recovery
merge_target_branch: spec/upgrade-atomicity-recovery
branch_strategy: Planning artifacts for this mission were generated on spec/upgrade-atomicity-recovery. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into spec/upgrade-atomicity-recovery unless the human explicitly redirects the landing branch.
subtasks:
- T029
- T030
phase: Phase 5 - Hygiene
history:
- timestamp: '2026-08-13T00:00:00Z'
  agent: system
  action: Prompt generated via /spec-kitty.tasks
authoritative_surface: src/specify_cli/cli/commands/agent/
create_intent:
- tests/specify_cli/cli/commands/agent/test_mission_create_json_remediation.py
execution_mode: code_change
owned_files:
- src/specify_cli/cli/commands/agent/mission.py
- tests/specify_cli/cli/commands/agent/test_mission_create_json_remediation.py
tags: []
tracker_refs: []
---

# Work Package Prompt: WP11 – Remediation body survives --json

**Priority**: P3 | **Phase**: Phase 5 - Hygiene | **Requirement Refs**: FR-010
**Mission**: `upgrade-atomicity-recovery-01KZWSHC` — see `../spec.md`, `../plan.md` (§Post-Plan Adversarial Revisions is binding), `../research.md`.

## Goal
The CHARTER_PACK_CONFIG_INVALID remediation body is present in `agent mission create --json`.

## Independent Test
Invalid charter pack -> --json failure envelope carries the remediation body.

## Subtasks
- [ ] T029 Carry the remediation body on the mission-create --json envelope
- [ ] T030 [P] Test: remediation body present in --json

## Code seams (from research.md — verify before editing)
- mission-create --json path (charter-pack-invalid) — the remediation body is currently discarded by --json (#3337).

## Acceptance criteria (ATDD-first — land the failing test before the code)
1. The --json failure envelope carries the remediation body.

## Dependencies
None.

## Risks & notes
Good-first-issue scope (#3337); keep narrow.

## Definition of Done
- All acceptance criteria pass; new helpers/branches carry focused tests (Sonar new-code coverage).
- `ruff` + `mypy` clean, zero suppressions; complexity <=15; terminology guard green.
- Changes match the corrected requirement wording in `../spec.md` and the binding revisions in `../plan.md`.
