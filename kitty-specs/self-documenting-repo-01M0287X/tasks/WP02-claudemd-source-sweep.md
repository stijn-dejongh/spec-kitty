---
work_package_id: WP02
title: CLAUDE.md source-location sweep (G2)
dependencies: []
subtasks:
- T005
- T006
phase: Phase 1
history:
- timestamp: '2026-08-15T08:10:00Z'
  lane: planned
  agent: system
  shell_pid: ''
  action: Prompt generated via /spec-kitty.tasks
authoritative_surface: ''
execution_mode: code_change
mission_id: 01M0287XCV1R9VDEXHSDB0RTYR
owned_files:
- CLAUDE.md
- tests/architectural/test_claudemd_template_source.py
wp_code: WP02
---

# Work Package Prompt: WP02 – CLAUDE.md source-location sweep (G2)

## Objective
Correct EVERY stale `src/doctrine/missions/…` reference in CLAUDE.md to `packs/built-in/missions/…` (verified: src/doctrine/missions/mission-steps no longer exists). Guard against regression.

## Subtasks
- **T005 Sweep.** Fix all occurrences: the 'Template Source Location' table, the flow diagram, and the 'Use Canonical Sources' section (the squad found ≥2 refs). `grep -n 'src/doctrine/missions' CLAUDE.md` must end empty.
- **T006 Guard.** `tests/architectural/test_claudemd_template_source.py` asserts 0 `src/doctrine/missions/` occurrences in CLAUDE.md.

## Done
Terminology guard passes; grep-guard green.
