---
work_package_id: WP05
title: File bugs + migration manifest (G5, FR-008)
dependencies:
- WP01
- WP02
- WP03
- WP04
requirement_refs:
- FR-006
- FR-008
- C-004
planning_base_branch: kitty/mission-self-doc-gapclose
merge_target_branch: kitty/mission-self-doc-gapclose
branch_strategy: Planning artifacts for this mission were generated on kitty/mission-self-doc-gapclose. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into kitty/mission-self-doc-gapclose unless the human explicitly redirects the landing branch.
subtasks:
- T014
- T015
- T016
phase: Phase 1
history:
- timestamp: '2026-08-15T08:10:00Z'
  lane: planned
  agent: system
  shell_pid: ''
  action: Prompt generated via /spec-kitty.tasks
authoritative_surface: docs/development/
execution_mode: code_change
mission_id: 01M0287XCV1R9VDEXHSDB0RTYR
create_intent:
- docs/development/agent-memory-migration-manifest.md
- tests/docs/test_migration_manifest_complete.py
tags: []
tracker_refs: []
wp_code: WP05
---

# Work Package Prompt: WP05 – File bugs + migration manifest (G5, FR-008)

## Objective
File the three behavior-quirk bugs (fixes DEFERRED), and write the committed manifest that is the repo-testable proof of migration.

## Subtasks
- **T014 File bugs** (filing only, no fixing): finalize-tasks-clobbers-issue-matrix; move-task double-increments review-cycle counter; status-daemon auto-commits with previous message. Record issue refs.
- **T015 Manifest.** `migration-manifest.md` maps each audited G1–G6 gap-filler (from `work/memory-gap-filler-analysis.md`) → its repo home (file/assertion), its tracking issue, OR an explicit 'behavior retired — delete memory, no repo home' (e.g. shard-registration via #2671). Deletion of the private memory is an operator checklist on #3448, out of mission scope (C-004).
- **T016 Completeness test.** `tests/docs/test_migration_manifest_complete.py` (or an arch test) asserts every enumerated G1–G6 gap-filler appears in the manifest with a resolution.

## Done
SC-005: manifest complete; every gap-filler resolved (home / issue / retired).
