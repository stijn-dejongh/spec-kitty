---
work_package_id: WP09
title: Legible duplicate-key guard
dependencies:
- WP03
requirement_refs:
- FR-007
- C-002
planning_base_branch: spec/upgrade-atomicity-recovery
merge_target_branch: spec/upgrade-atomicity-recovery
branch_strategy: Planning artifacts for this mission were generated on spec/upgrade-atomicity-recovery. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into spec/upgrade-atomicity-recovery unless the human explicitly redirects the landing branch.
subtasks:
- T025
- T026
phase: Phase 3 - Prevention
history:
- timestamp: '2026-08-13T00:00:00Z'
  agent: system
  action: Prompt generated via /spec-kitty.tasks
authoritative_surface: src/specify_cli/frontmatter.py
create_intent:
- tests/test_frontmatter_dup_key.py
execution_mode: code_change
owned_files:
- src/specify_cli/frontmatter.py
- tests/test_frontmatter_dup_key.py
tags: []
tracker_refs: []
---

# Work Package Prompt: WP09 – Legible duplicate-key guard

**Priority**: P2 | **Phase**: Phase 3 - Prevention | **Requirement Refs**: FR-007, C-002
**Mission**: `upgrade-atomicity-recovery-01KZWSHC` — see `../spec.md`, `../plan.md` (§Post-Plan Adversarial Revisions is binding), `../research.md`.

## Goal
The already-fail-closed frontmatter boundary raises a legible error naming the duplicate key(s).

## Independent Test
A dual-key artifact raises an error naming the key; allow_duplicate_keys=False is pinned by regression.

## Subtasks
- [ ] T025 Explicit except DuplicateKeyError branch naming the key(s) before the generic handler in src/specify_cli/frontmatter.py:122-127
- [ ] T026 Pin allow_duplicate_keys=False on the YAML() instance (frontmatter.py:83) under regression; consume WP03's raw-text detector to enumerate ALL duplicates

## Code seams (from research.md — verify before editing)
- src/specify_cli/frontmatter.py:83 (YAML() rt instance), :122-127 (generic 'Invalid YAML' wrap swallowing the named DuplicateKeyError).
- WP03 dup_key_repair detector — reuse to enumerate all duplicate keys (a single ruamel raise names only the first).

## Acceptance criteria (ATDD-first — land the failing test before the code)
1. Duplicate-key artifact raises a legible error naming the key(s), not a generic 'Invalid YAML'.
2. allow_duplicate_keys=False pinned by regression test.

## Dependencies
WP03 (genuine dependency edge — gates claiming).

## Risks & notes
Keep the guard in the canonical boundary (C-002). Depends on WP03's detector.

## Definition of Done
- All acceptance criteria pass; new helpers/branches carry focused tests (Sonar new-code coverage).
- **New `test_*.py` files MUST declare a `pytestmark` marker** (marker-convention CI gate — runs only in an integration job the fast local suites skip; a missing marker reds CI).
- `ruff` + `mypy` clean, zero suppressions; complexity <=15; terminology guard green.
- Changes match the corrected requirement wording in `../spec.md` and the binding revisions in `../plan.md`.
