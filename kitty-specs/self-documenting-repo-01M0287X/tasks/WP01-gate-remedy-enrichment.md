---
work_package_id: WP01
title: Gate-remedy enrichment (G1)
dependencies: []
subtasks:
- T001
- T002
- T003
- T004
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
- tests/architectural/test_no_write_side_rederivation.py
- tests/architectural/test_no_inert_schema_slots.py
- tests/docs/test_relative_link_fixer.py
- tests/docs/test_related_validator.py
- tests/architectural/test_gate_remedy_presence.py
wp_code: WP01
---

# Work Package Prompt: WP01 – Gate-remedy enrichment (G1)

## Objective
Add content-anchored remedy text to the architectural/docs gates that genuinely lack it, **derived from each gate's current logic and validated by tripping it** (C-005) — never transcribed from a private note. Pin remedy presence with a meta-test.

## Subtasks
- **T001 Locate + classify.** For each enumerated gate, find its real owning test and classify: remedy-extensible vs not-applicable. Known outcomes (post-plan squad): the shard-registration remedy is **retired** by #2671 auto-cover (`tests/_arch_shard_map.py:46-63`, `default_fallback=True`) → manifest 'behavior retired', no edit; `analysis-report-staleness` (`tests/specify_cli/test_analysis_report_charter_yaml_staleness.py`) is a narrow correctness test → likely not remedy-bearing; `docs-move` → `test_relative_link_fixer.py` + `test_related_validator.py`; `mission-gate-artifact` → locate or drop. Record classifications for WP05's manifest.
- **T002 Enrich.** Add a content-anchored remedy line to each confirmed gate, using `test_golden_count_ban.py` (escape-hatch marker + re-freeze) as the model. Content descriptors only — never file:line / whole-file allowlist (NFR-003 / DIRECTIVE_041).
- **T003 Meta-test.** `tests/architectural/test_gate_remedy_presence.py` asserts each registered gate's assertion contains its remedy substring. Register it wherever the arch suite requires (verify against auto-cover — likely nothing to add).
- **T004 Validate.** Trip each enriched gate in a scratch tree; confirm the message alone suffices.

## Done
SC-001 machine check green; ruff/mypy clean; no snapshot pins broken by the message change.
