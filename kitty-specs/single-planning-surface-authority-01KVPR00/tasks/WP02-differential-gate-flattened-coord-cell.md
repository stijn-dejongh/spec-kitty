---
work_package_id: WP02
title: 'Differential gate: flattened-stale-coord cell + live repro'
dependencies:
- WP01
requirement_refs:
- FR-005
- NFR-001
tracker_refs: []
planning_base_branch: feat/single-planning-surface-authority
merge_target_branch: feat/single-planning-surface-authority
branch_strategy: Planning artifacts for this mission were generated on feat/single-planning-surface-authority. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/single-planning-surface-authority unless the human explicitly redirects the landing branch.
subtasks:
- T006
- T007
- T008
- T009
agent: claude
history:
- Created by /spec-kitty.tasks
agent_profile: python-pedro
authoritative_surface: tests/missions/test_surface_resolution_equivalence.py
create_intent: []
execution_mode: code_change
owned_files:
- tests/missions/test_surface_resolution_equivalence.py
role: implementer
tags: []
---

## ⚡ Do This First: Load Agent Profile
Load + adopt `src/doctrine/agent_profiles/built-in/python-pedro.agent.yaml` via
`/ad-hoc-profile-load` before implementing.

## Objective
Extend the differential equivalence gate to FEED the `flattened-stale-coord` topology it currently
never tests, so the convergence is provably green for the exact case #2062 hits. This is the
deletion/convergence safety net (NFR-001) — without it, a green gate is only a partial proof (the
same under-feeding class as the #2065 bare-mid8 BLOCKER).

## Context
`tests/missions/test_surface_resolution_equivalence.py` covers topologies `no-coord`, `coord-fresh`,
`coord-behind`, `coord-empty`, `coord-deleted` only — NOT flattened-with-stale-coord-worktree. The
`_build_topology` builder + the `_MATRIX` rows drive all three legs and assert
`type(a) is type(b)` AND `error_code` equality (or identical dir). Do NOT weaken that assertion.

## Subtasks
### T006 — Add the topology to `_build_topology` (FR-005)
Add a `flattened-stale-coord` arm: primary `meta.json` with NO `coordination_branch`, a stale
`.worktrees/<slug>-<mid8>-coord/kitty-specs/<slug>-<mid8>/status.events.jsonl` (lane `planned`) on
disk, primary canonical at `approved`. Production-shaped ULID identity (real 26-char + mid8).

### T007 — Add the matrix rows (all handle forms)
Add `flattened-stale-coord` × every handle form (bare-slug, `<slug>-<mid8>`, bare-mid8, full-ULID),
asserting all three legs (read-path/surface/aggregate) return the PRIMARY dir. Strict rows (no
xfail). The assertion stays `type(a) is type(b)` AND `error_code` — unweakened.

### T008 — Live flattened-mid-flight repro (NFR-001, quickstart R1)
Add a witnessed end-to-end repro test driving the real topology through all three legs (per
`quickstart.md` R1) — this is the live-evidence proof #2062 requires (C-002: no close on static).

### T009 — Campsite #1970
De-stale the module docstring if it narrates the old topology set; remove any dead `_XFAIL_*`
narration. Bounded to this file.

## Branch Strategy
Base/merge `feat/single-planning-surface-authority`; lane allocated from `lanes.json`.

## #1970 Campsite (ACTIVE)
Remediate adjacent debt in this test surface in-slice.

## Definition of Done
- [ ] FR-005: `flattened-stale-coord` topology + all-handle rows added; gate green (N passed / 0 xfailed).
- [ ] Assertion NOT weakened (type-identity + error_code).
- [ ] NFR-001: live flattened-mid-flight repro witnessed (depends on WP01's gate landed).
- [ ] `ruff`/`mypy` clean; campsite done; no out-of-map edits.

## Reviewer guidance
Confirm the new rows FAIL if WP01's gate is reverted (the cell must observe real resolver output,
not be a tautology). Confirm the type+error_code assertion is intact.
