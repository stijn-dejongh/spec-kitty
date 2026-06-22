---
work_package_id: WP05
title: 'mission.py anchor: setup_plan/finalize routing + de-godding'
dependencies:
- WP03
- WP04
requirement_refs:
- FR-001
- FR-003
- FR-015
- FR-016
- FR-019
- NFR-004
tracker_refs: []
planning_base_branch: feat/single-planning-surface-authority
merge_target_branch: feat/single-planning-surface-authority
branch_strategy: Planning artifacts for this mission were generated on feat/single-planning-surface-authority. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/single-planning-surface-authority unless the human explicitly redirects the landing branch.
subtasks:
- T017
- T018
- T019
- T020
- T021
- T022
agent: claude
history:
- Created by /spec-kitty.tasks
agent_profile: python-pedro
authoritative_surface: src/specify_cli/cli/commands/agent/mission.py
create_intent:
- tests/coordination/test_commit_router_placement_helpers.py
execution_mode: code_change
owned_files:
- src/specify_cli/cli/commands/agent/mission.py
- src/specify_cli/coordination/commit_router.py
- tests/specify_cli/cli/commands/agent/test_mission_planning_entry.py
- tests/coordination/test_commit_router_placement_helpers.py
role: implementer
tags: []
---

## ⚡ Do This First: Load Agent Profile
Load + adopt `python-pedro` via `/ad-hoc-profile-load` before implementing.

## Objective
The `agent/mission.py` god-module (`setup_plan` + `finalize_tasks`) is a shared anchor. Route its
planning write/read through the single authority, extract the touched placement/commit helpers into
the canonical `coordination/commit_router.py` seam (FR-019 / #2056), emit clean `--json`, and harden
its untrusted-path sink. Bounded to the seams this WP touches — NOT a wholesale `mission.py` split.

## Subtasks
### T017 — setup_plan write path → resolve_placement_only (FR-001)
Route the `setup_plan` planning-commit destination through the write authority (consume WP03's seam).

### T018 — finalize-tasks read region → single WP-frontmatter surface (FR-003 finalize half)
The finalize read MUST resolve the same surface `map-requirements` writes (WP06 owns the map half).
Honor finalize's documented invariant (planning INPUT on PRIMARY, staged to coord at commit-time).

### T019 — Extract touched placement/commit helpers → commit_router.py (FR-019 / #2056)
Move ONLY the placement/commit helpers this WP edits into `coordination/commit_router.py` (the
strangler target), with a top-of-file `#2056` pointer. Local de-godding of touched seams only.

### T020 — Clean `--json` document (FR-015 / #1891 preamble leg)
`setup-plan` and `finalize-tasks` `--json` MUST emit a single clean JSON document — no human preamble
before the JSON on stdout. (The map-requirements serialization leg is already fixed — not here.)

### T021 — Harden mission.py:312 untrusted-path sink (FR-016 / #2037)
Route the CLI-arg `--mission` path join at `mission.py:~312` through
`assert_safe_path_segment`/`ensure_within_any`; add a negative test.

### T022 — Campsite #1970 + complexity
Keep every touched function ≤15 complexity (extract small helpers). Remediate adjacent debt
(`# noqa: BLE001` broad-catch at the placement fallback — tighten if safe). Bounded.

## Branch Strategy
Base/merge `feat/single-planning-surface-authority`; lane from `lanes.json`. After WP03 + WP04.

## #1970 Campsite (ACTIVE)
Remediate adjacent debt in `mission.py`/`commit_router.py` in-slice. Partial de-godding (T019) is
REQUIRED, not optional — but bounded to the touched seam.

## Definition of Done
- [ ] FR-001: setup_plan writes via `resolve_placement_only`.
- [ ] FR-003 (finalize half): finalize reads the single WP-frontmatter surface.
- [ ] FR-019: touched placement/commit helpers extracted → `commit_router.py` with #2056 pointer.
- [ ] FR-015: clean single `--json` doc on setup-plan/finalize-tasks.
- [ ] FR-016: `mission.py:312` sink hardened + negative test.
- [ ] All touched functions ≤15 complexity; `ruff`/`mypy` clean; campsite done; no out-of-map edits.

## Reviewer guidance
This is the god-module anchor — confirm the extraction is bounded (no wholesale split), the routing
consumes the SSOT (no new resolver), and the `--json` is genuinely single-document (no preamble).
