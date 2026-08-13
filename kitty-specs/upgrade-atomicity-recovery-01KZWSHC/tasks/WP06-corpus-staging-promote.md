---
work_package_id: WP06
title: Corpus staging-promote (OPTIONAL)
dependencies:
- WP05
requirement_refs:
- FR-004
- C-004
planning_base_branch: spec/upgrade-atomicity-recovery
merge_target_branch: spec/upgrade-atomicity-recovery
branch_strategy: Planning artifacts for this mission were generated on spec/upgrade-atomicity-recovery. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into spec/upgrade-atomicity-recovery unless the human explicitly redirects the landing branch.
subtasks:
- T018
- T019
- T020
phase: Phase 2 - Atomicity
history:
- timestamp: '2026-08-13T00:00:00Z'
  agent: system
  action: Prompt generated via /spec-kitty.tasks
authoritative_surface: src/specify_cli/upgrade/
create_intent:
- src/specify_cli/upgrade/staging.py
- tests/migration/test_corpus_staging.py
execution_mode: code_change
owned_files:
- src/specify_cli/upgrade/staging.py
- src/specify_cli/upgrade/migrations/m_zz_runtime_state_backfill.py
- src/specify_cli/migration/runtime_state_cutover.py
- tests/migration/test_corpus_staging.py
tags: []
tracker_refs: []
---

# Work Package Prompt: WP06 – Corpus staging-promote (OPTIONAL)

**Priority**: P2 | **Phase**: Phase 2 - Atomicity | **Requirement Refs**: FR-004, C-004
**Mission**: `upgrade-atomicity-recovery-01KZWSHC` — see `../spec.md`, `../plan.md` (§Post-Plan Adversarial Revisions is binding), `../research.md`.

## Goal
True 'mutate nothing on abort' + SIGKILL crash-atomicity via the staging-promote pattern.

## Independent Test
Abort/SIGKILL mid-run leaves zero missions mutated; status.events.jsonl promotion is append-preserving.

## Subtasks
- [ ] T018 Stage -> validate -> os.replace promote per ADR 2026-04-17-2
- [ ] T019 Append-preserving event-log staging (staged = prior ∪ appended, verified monotonic) to protect NFR-005
- [ ] T020 [P] Test: SIGKILL mid-commit recoverable

## Code seams (from research.md — verify before editing)
- ADR docs/adr/3.x/2026-04-17-2-charter-synthesizer-atomicity.md — stage under .staging/<runid>/, validate, os.replace promote, preserve .failed/cause.yaml.
- status.events.jsonl is append-only (sole reducer authority) — a whole-file os.replace must be append-preserving to not violate NFR-005.

## Acceptance criteria (ATDD-first — land the failing test before the code)
1. Abort/SIGKILL leaves zero missions mutated.
2. Event-log promotion preserves append-only/reducer determinism.

## Dependencies
WP05 (genuine dependency edge — gates claiming).

## Risks & notes
Contradicts the intentional per-mission design (D-03) — justify via the ADR. DEFERRABLE: dropping this removes SIGKILL-edge coverage (spec documents this).

## Definition of Done
- All acceptance criteria pass; new helpers/branches carry focused tests (Sonar new-code coverage).
- **New `test_*.py` files MUST declare a `pytestmark` marker** (marker-convention CI gate — runs only in an integration job the fast local suites skip; a missing marker reds CI).
- `ruff` + `mypy` clean, zero suppressions; complexity <=15; terminology guard green.
- Changes match the corrected requirement wording in `../spec.md` and the binding revisions in `../plan.md`.
