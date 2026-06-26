---
work_package_id: WP03
title: Lane A — Lanes/core cluster routing + recovery extraction + pin drain
dependencies:
- WP02
requirement_refs:
- FR-001
- FR-002
- FR-008
- NFR-001
tracker_refs: []
planning_base_branch: mission/coord-read-residuals-2185-2186
merge_target_branch: mission/coord-read-residuals-2185-2186
branch_strategy: Planning artifacts for this mission were generated on mission/coord-read-residuals-2185-2186. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into mission/coord-read-residuals-2185-2186 unless the human explicitly redirects the landing branch.
subtasks:
- T017
- T018
- T019
- T020
- T021
- T022
phase: Phase 2 - Lane A (post C-SEQ rebase)
assignee: ''
agent: claude
history:
- at: '2026-06-26T19:00:00Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: python-pedro
authoritative_surface: src/
create_intent: []
execution_mode: code_change
model: ''
owned_files: []
role: implementer
tags: []
task_type: implement
---

# Work Package Prompt: WP03 – Lane A — Lanes/core cluster routing

## ⚡ Do This First: Load Agent Profile
Use `/ad-hoc-profile-load` to load `python-pedro` (implementer).

## Objectives & Success Criteria
- Route the `lanes/` + `core/worktree_topology` PRIMARY reads; extract helpers out of the over-complex `scan_recovery_state` and drop its `# noqa: C901`; drain the lanes/core #2185 pins.

## Context & Constraints
- Depends on WP02 (sequential gate-file chain). C-001/C-002/C-009-mirror as WP02.

## Branch Strategy
- **Planning base branch**: `mission/coord-read-residuals-2185-2186`
- **Merge target branch**: `mission/coord-read-residuals-2185-2186`

## Subtasks & Detailed Guidance
### T017 – `lanes/merge.py:68/:198`
- Route the `read_lanes_json` reads (LANE_STATE) via `resolve_planning_read_dir`.
### T018 – `lanes/recovery.py` extraction + route
- `scan_recovery_state` already carries `# noqa: C901`. **Extract** the PRIMARY-planning read (`:356` lanes/tasks) and the status-events read into named helpers, **drop the `# noqa`**, route the PRIMARY leg, keep the events leg coord-aware. Also route `:611` (LANE_STATE). Add focused tests for the extracted helpers.
### T019 – `lanes/worktree_allocator.py:360`
- Route the `meta.json` read (`_read_coordination_branch`) via `kind=PRIMARY_METADATA` (topology-blind — correct for the chicken-and-egg coord discovery).
### T020 – `core/worktree_topology.py:138`
- Single swap of `:138` to `resolve_planning_read_dir(kind=WORK_PACKAGE_TASK)` co-resolves the three PRIMARY legs (identity `:139`, lanes `:140`, graph `:141`).
### T021 – Drain lanes/core pins (same commit).
### T022 – RED-first per-site tests on the divergent coord fixture.

## Test Strategy
- Focused tests for the recovery helper extraction + per-site RED-first. `ruff`+`mypy` clean; `scan_recovery_state` ≤ 15 after extraction (no noqa).

## Risks & Mitigations
- Extraction changes behavior → keep the helpers pure; the events leg must stay coord-aware (NFR-001).

## Review Guidance
- `reviewer-renata`: confirm the `# noqa: C901` is gone (not re-suppressed), events leg coord-aware, pins drained.

## Activity Log
- 2026-06-26T19:00:00Z – system – Prompt created.
