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
tracker_refs:
- '#2187'
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
- T029
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
- Route the `lanes/` + `core/worktree_topology` + `agent_utils/status.py` (`show_kanban_status`, #2187) PRIMARY reads; extract helpers out of the over-complex `scan_recovery_state` and drop its `# noqa: C901`; drain the lanes/core + #2187 pins.

## Context & Constraints
- Depends on WP02 (sequential gate-file chain). C-001/C-002/C-009-mirror as WP02.
- **Owned surface** (governed by `authoritative_surface: src/`): the lanes/core sites above **plus** `src/specify_cli/agent_utils/status.py` (the #2187 `show_kanban_status` site, T029). No other WP touches this file — no ownership overlap.

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
### T029 – `agent_utils/status.py:120/126` (`show_kanban_status`, #2187)
- **Mixed PRIMARY+STATUS site** (same per-leg-split class as #2185). The function currently resolves a single coord-aware `feature_dir = resolve_feature_dir_for_mission(...)` (`:120`) and reuses it for both the PRIMARY `tasks/` glob (`tasks_dir = feature_dir / "tasks"`, `:126`, WORK_PACKAGE_TASK) **and** the STATUS `read_events(feature_dir)` leg (`:151`).
- **Route only the PRIMARY leg**: resolve the `tasks/` directory via `resolve_planning_read_dir(repo_root, mission_slug, kind=WORK_PACKAGE_TASK)` so the WP*.md frontmatter glob reads off PRIMARY, not the `-coord` husk.
- **Keep the STATUS leg coord-aware** (C-001/NFR-001): `read_events` / `reduce` must continue to read the worktree-local event log (the kanban lane data still reflects the event log). The `resolve_mission_identity(feature_dir)` leg is **out of #2187 scope** (identity class) — leave it; do not over-route.
- **Drain the pin**: remove the matching `_DIR_READ_KNOWN_RESIDUALS` entry for `agent_utils/status.py` in the same commit (FR-008). FR-011 preflight (T009) must have confirmed it is present on the rebased base.
- **RED-first test**: on the divergent `build_coord` fixture (PRIMARY-only `tasks/`, husk lacks it), assert `show_kanban_status` renders the correct **non-empty** board; reverting the routed read to the coord-aware resolver must FAIL. A unit stub handing in a primary dir directly does NOT satisfy this (it masks the routing bug — #2187 AC).

## Test Strategy
- Focused tests for the recovery helper extraction + per-site RED-first. `ruff`+`mypy` clean; `scan_recovery_state` ≤ 15 after extraction (no noqa).

## Risks & Mitigations
- Extraction changes behavior → keep the helpers pure; the events leg must stay coord-aware (NFR-001).

## Review Guidance
- `reviewer-renata`: confirm the `# noqa: C901` is gone (not re-suppressed), events leg coord-aware, pins drained.

## Activity Log
- 2026-06-26T19:00:00Z – system – Prompt created.
