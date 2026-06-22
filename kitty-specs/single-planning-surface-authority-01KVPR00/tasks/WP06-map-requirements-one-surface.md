---
work_package_id: WP06
title: map-requirements one-surface + diagnostics
dependencies:
- WP05
requirement_refs:
- FR-003
- FR-010
- FR-013
- FR-014
- FR-016
tracker_refs: []
planning_base_branch: feat/single-planning-surface-authority
merge_target_branch: feat/single-planning-surface-authority
branch_strategy: Planning artifacts for this mission were generated on feat/single-planning-surface-authority. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/single-planning-surface-authority unless the human explicitly redirects the landing branch.
subtasks:
- T023
- T024
- T025
- T026
- T027
- T028
agent: claude
history:
- Created by /spec-kitty.tasks
agent_profile: python-pedro
authoritative_surface: src/specify_cli/cli/commands/agent/tasks.py
create_intent: []
execution_mode: code_change
owned_files:
- src/specify_cli/cli/commands/agent/tasks.py
- src/specify_cli/requirement_mapping.py
- tests/specify_cli/cli/commands/agent/test_map_requirements_coord.py
- tests/specify_cli/cli/commands/agent/test_map_requirements_spec_path.py
role: implementer
tags: []
---

## ⚡ Do This First: Load Agent Profile
Load + adopt `python-pedro` via `/ad-hoc-profile-load` before implementing.

## Objective
Make `map-requirements` (write) and `finalize-tasks --validate-only` (read, WP05 owns the read side)
agree on ONE surface for WP `requirement_refs`, surface the parsed FR set on mismatch, harden the
tasks.py path sink, and de-pin the tests that codify the split (#2064 / #2066 / #2037 / #1970).

## Context (live-evidence, #2064)
`map-requirements` writes WP `requirement_refs` to the COORD surface
(`tasks.py:~3633 resolve_feature_dir_for_slug`) while `finalize-tasks --validate-only` reads PRIMARY
— so finalize reports all-unmapped despite map-requirements reporting full coverage. `compute_coverage`
is ALREADY single-source (`requirement_mapping.py:61`) — the split is the READ SURFACE, not the math.

## Subtasks
### T023 — map-requirements writes on the finalize-read surface (FR-003 map half)
Resolve the WP-frontmatter write surface so it matches what `finalize-tasks` reads (WP05). Honor the
PRIMARY-input invariant. Acceptance: after `map-requirements` reports full coverage,
`finalize-tasks --validate-only` reports ZERO `unmapped_functional_requirements` (quickstart R3).

### T024 — Consolidate the READ surface (FR-013, brownfield-corrected)
Consolidate the WP-frontmatter READ path (`read_all_wp_requirement_refs` vs finalize's own dir
resolution) to ONE place. Do NOT touch the already-single `compute_coverage`.

### T025 — Parsed FR-ID set on mismatch (FR-014 / #2066)
When WP refs don't match `spec.md` FR IDs, emit the parsed FR set in the `--json` payload so the
operator sees actual vs expected.

### T026 — Harden tasks.py:1911 untrusted-path sink (FR-016 / #2037)
Route the CLI-arg `--mission` path join at `tasks.py:~1911` through
`assert_safe_path_segment`/`ensure_within_any` + a negative test.

### T027 — De-pin the split-brain tests (FR-010 / #1970) — real two-command sequence (squad N2)
`test_map_requirements_coord.py` and `test_map_requirements_spec_path.py` currently ASSERT the
coord-vs-primary split as the desired state (mock-heavy). Re-point them to assert cross-command surface
COHERENCE using a **real two-command sequence on a real tmp mission** (`map-requirements` write →
`finalize-tasks` read), NOT a mock asserting the same dir twice. The re-pointed test MUST FAIL if the
two surfaces diverge.

### T028 — Campsite #1970
Remediate adjacent debt in the map-requirements region. Keep touched functions ≤15. Bounded.

## Branch Strategy
Base/merge `feat/single-planning-surface-authority`; lane from `lanes.json`. After WP05.

## #1970 Campsite (ACTIVE)
Remediate adjacent debt in the touched surfaces in-slice (bounded).

## Definition of Done
- [ ] FR-003 (map half): map-requirements writes on the finalize-read surface; R3 passes (zero unmapped).
- [ ] FR-013: read surface consolidated (not the coverage math).
- [ ] FR-014: parsed FR-ID set emitted on mismatch.
- [ ] FR-016: `tasks.py:1911` sink hardened + negative test.
- [ ] FR-010: the two map_requirements tests assert cross-command coherence, not the split.
- [ ] `ruff`/`mypy` clean; complexity ≤15; campsite done; no out-of-map edits.

## Reviewer guidance
Confirm R3 is witnessed (real map → real finalize, zero unmapped). Confirm the de-pinned tests now
fail if the surfaces diverge (not mock-faked).
