---
work_package_id: WP03
title: Duplicate-key detect + repair
dependencies: []
requirement_refs:
- FR-008
- NFR-002
- NFR-004
- C-004
planning_base_branch: spec/upgrade-atomicity-recovery
merge_target_branch: spec/upgrade-atomicity-recovery
branch_strategy: Planning artifacts for this mission were generated on spec/upgrade-atomicity-recovery. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into spec/upgrade-atomicity-recovery unless the human explicitly redirects the landing branch.
base_branch: kitty/mission-upgrade-atomicity-recovery-01KZWSHC
base_commit: 92053ea8bc0a05d72ba591a8af17b37b6f759172
created_at: '2026-08-13T08:30:27.839496+00:00'
subtasks:
- T007
- T008
- T009
- T010
- T011
phase: Phase 1 - Recovery
history:
- timestamp: '2026-08-13T00:00:00Z'
  agent: system
  action: Prompt generated via /spec-kitty.tasks
authoritative_surface: src/specify_cli/status/
create_intent:
- src/specify_cli/status/dup_key_repair.py
- tests/status/test_dup_key_repair.py
execution_mode: code_change
owned_files:
- src/specify_cli/status/dup_key_repair.py
- src/specify_cli/migration/mission_state.py
- src/specify_cli/status/doctor.py
- src/specify_cli/cli/commands/_mission_state_doctor.py
- tests/status/test_dup_key_repair.py
tags: []
tracker_refs: []
---

# Work Package Prompt: WP03 – Duplicate-key detect + repair

**Priority**: P1 | **Phase**: Phase 1 - Recovery | **Requirement Refs**: FR-008, NFR-002, NFR-004, C-004
**Mission**: `upgrade-atomicity-recovery-01KZWSHC` — see `../spec.md`, `../plan.md` (§Post-Plan Adversarial Revisions is binding), `../research.md`.

## Goal
Heal legacy dual-key review_feedback artifacts before an upgrade trips over them.

## Independent Test
Doctor scan lists malformed artifacts; opt-in --fix repairs them batch-atomically to valid YAML without discarding recorded state.

## Subtasks
- [ ] T007 New small module src/specify_cli/status/dup_key_repair.py — raw-text duplicate-key DETECTOR (read_frontmatter fails closed, so scan raw text)
- [ ] T008 Surface detection as a check_* Finding in status/doctor.py (thin delegation; do not grow the #1623 god-module)
- [ ] T009 Implement REPAIR by extending src/specify_cli/migration/mission_state.py (repair_repo/RepairReport/FileChange/atomic_write); keep-last-non-empty policy
- [ ] T010 Wire opt-in --fix through cli/commands/_mission_state_doctor.py
- [ ] T011 [P] Unit tests: detector, batch-atomic repair, non-destructive invariant

## Code seams (from research.md — verify before editing)
- src/specify_cli/frontmatter.py:83,122-127 — read() fails closed on duplicate keys (ruamel DuplicateKeyError); detection therefore CANNOT use read_frontmatter — scan raw text.
- src/specify_cli/migration/mission_state.py:281,286-392,535,589 — repair_repo/RepairReport/FileChange/atomic_write/dry-run — the ADR 2026-05-10-1 repair framework to REUSE (not reinvent).
- src/specify_cli/status/doctor.py — diagnostic-only (check_* -> list[Finding]); mutation must live in mission_state, surfaced via _mission_state_doctor.py.

## Acceptance criteria (ATDD-first — land the failing test before the code)
1. Detection lists every dual-key artifact under kitty-specs/**/*.md.
2. --fix repairs batch-atomically (NFR-004) and non-destructively (NFR-002; recorded state preserved), yielding valid YAML.
3. Repair is opt-in (doctor is unconditionally SAFE).

## Dependencies
None.

## Risks & notes
Riskiest MANDATORY WP. Reuse the ADR repair machinery; keep detection in a small module (complexity <=15, focused tests) rather than growing doctor.py.

## Definition of Done
- All acceptance criteria pass; new helpers/branches carry focused tests (Sonar new-code coverage).
- **New `test_*.py` files MUST declare a `pytestmark` marker** (marker-convention CI gate — runs only in an integration job the fast local suites skip; a missing marker reds CI).
- `ruff` + `mypy` clean, zero suppressions; complexity <=15; terminology guard green.
- Changes match the corrected requirement wording in `../spec.md` and the binding revisions in `../plan.md`.
