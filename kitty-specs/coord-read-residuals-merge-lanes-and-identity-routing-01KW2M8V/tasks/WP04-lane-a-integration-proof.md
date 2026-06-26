---
work_package_id: WP04
title: Lane A — Coord-topology integration proof (divergent fixture)
dependencies:
- WP02
- WP03
requirement_refs:
- FR-009
- NFR-003
- NFR-004
tracker_refs: []
subtasks:
- T023
- T024
- T025
phase: Phase 3 - Integration proof
assignee: ''
agent: claude
history:
- at: '2026-06-26T19:00:00Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: python-pedro
create_intent: []
model: ''
owned_files: []
role: implementer
tags: []
task_type: implement
---

# Work Package Prompt: WP04 – Lane A — Coord-topology integration proof

## ⚡ Do This First: Load Agent Profile
Use `/ad-hoc-profile-load` to load `python-pedro` (implementer).

## Objectives & Success Criteria
- A real `git worktree` coord-topology integration test proves the routed Lane A reads land on PRIMARY, and **fails if any routed read is reverted to coord-aware**. This is the headline acceptance (SC-001) and the squad's CRITICAL false-green guard.

## Context & Constraints
- Depends on WP02 + WP03 (the routed code under test). NFR-004 integration-over-stubs — no unit stubs handing in a primary dir.

## Branch Strategy
- **Planning base branch**: `mission/coord-read-residuals-2185-2186`
- **Merge target branch**: `mission/coord-read-residuals-2185-2186`

## Subtasks & Detailed Guidance
### T023 – Extend `build_coord` to a DIVERGENT husk
- **Files**: `tests/specify_cli/write_side/topology_fixtures.py`. Make the coord husk `meta.json` carry a **sentinel `mission_id`/identity ≠ PRIMARY**, and seed production-shaped `lanes.json` + `tasks/` on PRIMARY **after** `git worktree add` (so they do not propagate to the coord checkout). Assert the husk lacks `lanes.json`/`tasks/`. (Without divergence the test is non-falsifiable — the squad's CRITICAL finding.)
### T024 – Coord-topology integration test
- **Files**: `tests/integration/test_*.py` (new). Drive the real `_run_lane_based_merge` / `scan_recovery_state` / `materialize_worktree_topology` against the divergent fixture; assert PRIMARY reads; assert STATUS legs read from the husk. Add a guard that reverting a routed read to coord-aware fails.
### T025 – Flat-topology parity [P]
- Assert the routing is a no-op on flat topology (NFR-003); existing flat-topology merge/lanes tests stay green.

## Test Strategy
- This WP *is* the test. Run serially if it touches real ports/daemons; otherwise parallel-safe.

## Risks & Mitigations
- Non-divergent husk = false-green → the divergence assertions in T023 are the guard; review them explicitly.

## Review Guidance
- `reviewer-renata`: confirm the husk genuinely diverges and the revert-fails guard is present and real.

## Activity Log
- 2026-06-26T19:00:00Z – system – Prompt created.
