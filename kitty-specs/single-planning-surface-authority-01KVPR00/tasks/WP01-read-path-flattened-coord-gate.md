---
work_package_id: WP01
title: Read-path flattened-stale-coord gate (safety net)
dependencies: []
requirement_refs:
- FR-004
- FR-012
- FR-017
tracker_refs: []
planning_base_branch: feat/single-planning-surface-authority
merge_target_branch: feat/single-planning-surface-authority
branch_strategy: Planning artifacts for this mission were generated on feat/single-planning-surface-authority. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/single-planning-surface-authority unless the human explicitly redirects the landing branch.
subtasks:
- T001
- T002
- T003
- T004
- T005
agent: claude
history:
- Created by /spec-kitty.tasks
agent_profile: python-pedro
authoritative_surface: src/specify_cli/missions/_read_path_resolver.py
create_intent: []
execution_mode: code_change
owned_files:
- src/specify_cli/missions/_read_path_resolver.py
- src/specify_cli/mission_read_path.py
- tests/missions/test_coord_feature_dir_helpers.py
role: implementer
tags: []
---

## ⚡ Do This First: Load Agent Profile
Before anything else, load your profile via `/ad-hoc-profile-load` (or read + adopt
`src/doctrine/agent_profiles/built-in/python-pedro.agent.yaml`). Do not implement until loaded.

## Objective
Make the read-path leg gate its coord-worktree preference on the **declared** coordination
topology, so a *flattened* mission (primary `meta.json` has NO `coordination_branch`) with a
stale `.worktrees/<slug>-<mid8>-coord/` left on disk resolves the **PRIMARY** surface — matching
`resolve_handle_to_read_path` / `resolve_status_surface_with_anchor`. This is the **safety net**:
land it first; WP02 adds the differential-gate cell that proves it.

## Context (live-evidence, #2062) — read the code carefully, this is NOT a no-op (squad B2)
`_declares_coordination_branch` ALREADY EXISTS (`_read_path_resolver.py:92`) and is ALREADY applied
to the **primary fall-through** (`:277`). The bug is that the **coord-preference branch fires FIRST,
before any declares check**: at `:270-271`, `if coord_state is CoordState.MATERIALIZED: return
coord_feature_dir(...)` returns the coord dir on pure `Path.exists()` MATERIALIZED — a flattened
mission never reaches the `:277` gate. The surface + aggregate legs already gate on
`coordination_branch is None → primary`; the read-path `:270` branch does not. So a flattened mission
leaks STALE-COORD for the `<slug>-<mid8>` / bare-mid8 / full-ULID handles. The stale narration
comment is at `:260-264`. See `quickstart.md` R1. **DO NOT conclude "the helper already exists →
no-op" — the gate exists but is applied to the WRONG branch.**

## Subtasks
### T001 — Gate the `:270` coord-preference branch on declared coordination (FR-004)
Thread a `declares_coordination: bool` signal (read once from primary `meta.json` via the existing
blessed helper, no raw join) so the **`:270` coord-preference branch** (`coord_state is MATERIALIZED
→ return coord_feature_dir`) only fires when `declares_coordination` is True. When flattened
(no `coordination_branch`), MATERIALIZED is necessary-but-not-sufficient → fall through to `:272`
PRIMARY (the existing `:277` declares-gate then handles it). Match create-window (#1718) /
coord-deleted (#1848) — do NOT regress those.

### T002 — Unify probe_coord_state branch-signal threading (FR-012)
`_resolve_existing_for_slug` calls `probe_coord_state(...)` WITHOUT `coordination_branch` while
`_resolve_not_found` supplies it — the asymmetry is the defect. Unify the threading so both paths
pass the same signal. Update the stale comment block at `:260-264` ("No branch is supplied here")
which documents the defect as intentional.

### T003 — Zero-mock unit: flattened-stale-coord → PRIMARY (all handles)
In `tests/missions/test_coord_feature_dir_helpers.py` add a zero-mock unit (real `git init`, real
dirs) for the flattened-stale-coord topology: primary meta with NO `coordination_branch`, a stale
`-coord` worktree on disk; assert `resolve_handle_to_read_path(repo, <handle>, require_exists=True)`
returns the PRIMARY dir for handles {`<slug>-<mid8>`, bare-mid8, full-ULID, bare-human-slug}.
**Mutation-sensitive (binding):** the unit MUST FAIL when the SPECIFIC `:270` gate is reverted (i.e.
restore the unconditional `return coord_feature_dir(...)`) — not merely when the file is unchanged.
Demonstrate the mutation locally and paste the before/after into the WP history.

### T004 — FR-017 (GATED): retire the dead `mission_read_path` shim
Grep the codebase for external consumers of `src/specify_cli/mission_read_path.py`. IF ZERO (only
test imports / the shim itself), delete the shim, repoint the test imports to the canonical
`_read_path_resolver`, and decrement the backcompat-shim allowlist in the architectural baseline
(`tests/architectural/.../_baselines.yaml`, category_4_backcompat_shims 9→8). IF consumers remain,
LEAVE it and record why in the WP history. (Closes the read-path half of #2048.)

### T005 — Campsite #1970 (`_read_path_resolver.py`)
Remediate adjacent debt in the touched file in-slice: dead code, stale comments narrating removed
behavior, lint/type debt, any fakeable assertion. Bounded to this surface. Do NOT touch other WPs'
owned files.

## Branch Strategy
Planning base `feat/single-planning-surface-authority`; final merge target
`feat/single-planning-surface-authority`. Your execution worktree is allocated per the computed
lane from `lanes.json` (`spec-kitty agent action implement WP01 --agent <name>`). Do not reconstruct
the path.

## #1970 Campsite directive (ACTIVE)
When you touch a surface, REMEDIATE adjacent debt there in-slice — never defer with "pre-existing,
out of scope." Bounded to the mission goals.

## Definition of Done
- [ ] FR-004: `_resolve_existing_for_slug` gates coord-preference on `declares_coordination`.
- [ ] FR-012: branch-signal threading unified; stale `:263` comment fixed.
- [ ] T003 unit green and mutation-sensitive (fails with the gate reverted).
- [ ] FR-017 resolved (shim retired + baseline decremented, OR left-with-reason recorded).
- [ ] `ruff` + `mypy` clean on changed files; complexity ≤15; campsite done.
- [ ] No edits outside `owned_files` (small justified out-of-map edit recorded if unavoidable).

## Reviewer guidance
Verify the gate is real (not a tautology): the T003 unit must fail if T001 is reverted. Confirm
create-window (#1718) and coord-deleted (#1848) are NOT regressed. Confirm FR-017 gate honored
(no forced deletion if consumers exist).
