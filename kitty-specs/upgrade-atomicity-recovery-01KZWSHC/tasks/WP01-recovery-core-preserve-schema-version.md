---
work_package_id: WP01
title: Recovery core — preserve schema_version + resumable re-run
dependencies: []
requirement_refs:
- FR-002
- FR-012
- NFR-001
- NFR-002
planning_base_branch: spec/upgrade-atomicity-recovery
merge_target_branch: spec/upgrade-atomicity-recovery
branch_strategy: Planning artifacts for this mission were generated on spec/upgrade-atomicity-recovery. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into spec/upgrade-atomicity-recovery unless the human explicitly redirects the landing branch.
base_branch: kitty/mission-upgrade-atomicity-recovery-01KZWSHC
base_commit: 92053ea8bc0a05d72ba591a8af17b37b6f759172
created_at: '2026-08-13T07:56:43.464511+00:00'
subtasks:
- T001
- T002
- T003
- T004
phase: Phase 1 - Recovery
history:
- timestamp: '2026-08-13T00:00:00Z'
  agent: system
  action: Prompt generated via /spec-kitty.tasks
authoritative_surface: src/specify_cli/upgrade/
create_intent:
- tests/upgrade/test_schema_version_recovery.py
execution_mode: code_change
owned_files:
- src/specify_cli/upgrade/runner.py
- src/specify_cli/upgrade/metadata.py
- tests/upgrade/test_schema_version_recovery.py
tags: []
tracker_refs: []
---

# Work Package Prompt: WP01 – Recovery core — preserve schema_version + resumable re-run

**Priority**: P0 | **Phase**: Phase 1 - Recovery | **Requirement Refs**: FR-002, FR-012, NFR-001, NFR-002
**Mission**: `upgrade-atomicity-recovery-01KZWSHC` — see `../spec.md`, `../plan.md` (§Post-Plan Adversarial Revisions is binding), `../research.md`.

## Goal
A failed migration never advances schema_version; a re-run is a safe no-op — closing the #3334 P0.

## Independent Test
A red-first regression (synthetic failing migration) is red pre-fix / green post-fix; legacy/None and <REQUIRED projects never get the target schema stamped; FR-012 re-run applies zero migrations.

## Subtasks
- [ ] T001 Author the #3334 red-first regression (@pytest.mark.regression, synthetic always-failing migration; trigger-agnostic) in tests/upgrade/
- [ ] T002 Preserve/restore the pre-run schema_version on the abort path in src/specify_cli/upgrade/runner.py (capture before the loop; restore on break — do NOT blanket-finally-stamp the target)
- [ ] T003 Stop ProjectMetadata.save() erasing schema_version on the failure path (src/specify_cli/upgrade/metadata.py:188-210)
- [ ] T004 [P] Assert FR-012 resumable no-op: a re-run after restoration applies zero migrations

## Code seams (from research.md — verify before editing)
- src/specify_cli/upgrade/runner.py:181-190,489 — _stamp_schema_version is guarded by result.success and writes the TARGET schema (REQUIRED_SCHEMA_VERSION). Move to preserve-captured-value on failure, stamp target only on success.
- src/specify_cli/upgrade/metadata.py:188-210,32-35 — save() rewrites metadata.yaml from a fixed dict omitting schema_version; :172-173 masked compare excludes it.
- src/specify_cli/migration/schema_version.py:22-27 — REQUIRED_SCHEMA_VERSION=MIN_SUPPORTED_SCHEMA=3 (the value a naive finally would wrongly stamp).

## Acceptance criteria (ATDD-first — land the failing test before the code)
1. #3334 repro red pre-fix, green post-fix, FORCED via a synthetic always-failing migration (independent of the dup-key trigger and FR-008 — no masking).
2. Invariant: a legacy/None or <REQUIRED project whose migration aborts does NOT have schema_version advanced.
3. FR-012: after restoration, re-running upgrade applies zero migrations (safe no-op/resume).

## Dependencies
None.

## Risks & notes
_stamp_schema_version writes the TARGET schema — restore the captured pre-run value, never the target, on failure. This is the correctness crux the post-plan squad flagged (would otherwise open the gate on a half-backfilled corpus).

## Definition of Done
- All acceptance criteria pass; new helpers/branches carry focused tests (Sonar new-code coverage).
- **New `test_*.py` files MUST declare a `pytestmark` marker** (marker-convention CI gate — runs only in an integration job the fast local suites skip; a missing marker reds CI).
- `ruff` + `mypy` clean, zero suppressions; complexity <=15; terminology guard green.
- Changes match the corrected requirement wording in `../spec.md` and the binding revisions in `../plan.md`.
