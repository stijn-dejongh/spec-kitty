---
work_package_id: WP04
title: Status-event emission write-surface
dependencies:
- WP03
requirement_refs:
- FR-006
tracker_refs: []
planning_base_branch: feat/single-planning-surface-authority
merge_target_branch: feat/single-planning-surface-authority
branch_strategy: Planning artifacts for this mission were generated on feat/single-planning-surface-authority. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/single-planning-surface-authority unless the human explicitly redirects the landing branch.
subtasks:
- T014
- T015
- T016
agent: claude
history:
- Created by /spec-kitty.tasks
agent_profile: python-pedro
authoritative_surface: src/specify_cli/status/emit.py
create_intent:
- tests/status/test_emit_write_surface.py
execution_mode: code_change
owned_files:
- src/specify_cli/status/emit.py
- tests/status/test_emit_write_surface.py
role: implementer
tags: []
---

## ⚡ Do This First: Load Agent Profile
Load + adopt `python-pedro` via `/ad-hoc-profile-load` before implementing.

## Objective
Make `emit_status_transition` resolve its write `feature_dir` from the single write authority rather
than accepting an ad-hoc per-caller path, so dep-gate / kanban / review-claim reads and `move-task`
writes converge on one surface (the #2062 status-read symptom).

## Context
`status/emit.py:~399 emit_status_transition(feature_dir=…)` writes wherever the caller passes;
callers pick the surface independently (no central authority). On a flattened/coord-mixed mission
that splits the event log across surfaces.

## Subtasks
### T014 — Resolve the write surface from the authority (FR-006) — enumerate ALL call sites (squad S4)
**Enumerate every in-repo emission call site (`grep -rn 'emit_status_transition(' src/`)** and confirm
each either resolves its `feature_dir` via the single write authority or is internally resolved at the
emission boundary — not a single happy-path caller. Preserve the public signature where external callers
depend on it; resolve internally when the caller does not supply an authority-resolved dir.

### T015 — Tests (the #2062 split must close)
Assert that for a FLATTENED mission the dep-gate/kanban READ and the `move-task` WRITE resolve the
IDENTICAL dir (not merely "a transition writes somewhere"). This is the #2062 status-read convergence —
a tautological single-write test does not satisfy it.

### T016 — Campsite #1970
Remediate adjacent debt in `status/emit.py`. NOTE: the 20-parameter hub (`# NOSONAR`) is a separate
effort — pointer only, do not refactor it here. Clean the lines you touch.

## Branch Strategy
Base/merge `feat/single-planning-surface-authority`; lane from `lanes.json`. After WP03.

## #1970 Campsite (ACTIVE)
Remediate adjacent debt in the touched emission surface in-slice (bounded).

## Definition of Done
- [ ] FR-006: emission write surface resolved by the single authority; call sites converge.
- [ ] Public contract preserved for external callers.
- [ ] `ruff`/`mypy` clean; complexity ≤15; campsite done; no out-of-map edits.

## Reviewer guidance
Confirm no ad-hoc per-caller surface remains for the in-repo emission sites. Confirm the 20-param
hub was left (pointer only), not partially refactored.
