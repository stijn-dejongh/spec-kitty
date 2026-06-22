---
work_package_id: WP09
title: Collapse is_committed 3-leg OR (last, gated)
dependencies:
- WP05
- WP02
requirement_refs:
- FR-011
tracker_refs: []
planning_base_branch: feat/single-planning-surface-authority
merge_target_branch: feat/single-planning-surface-authority
branch_strategy: Planning artifacts for this mission were generated on feat/single-planning-surface-authority. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/single-planning-surface-authority unless the human explicitly redirects the landing branch.
subtasks:
- T039
- T040
- T041
agent: claude
history:
- Created by /spec-kitty.tasks
agent_profile: python-pedro
authoritative_surface: src/specify_cli/missions/_substantive.py
create_intent:
- tests/specify_cli/missions/test_substantive_is_committed.py
execution_mode: code_change
owned_files:
- src/specify_cli/missions/_substantive.py
- tests/specify_cli/missions/test_substantive_is_committed.py
role: implementer
tags: []
---

## ⚡ Do This First: Load Agent Profile
Load + adopt `python-pedro` via `/ad-hoc-profile-load` before implementing.

## Objective
Collapse `_substantive.is_committed`'s 3-leg OR (coord-ref / HEAD / primary-target-branch,
`:317-412`) to a SINGLE-surface check on the resolved placement ref, and remove the multi-surface
diagnostics workaround — now that the write authority is singular (WP03/WP05). **This is the
load-bearing-workaround collapse — gated, sequenced LAST.**

## GATE (binding — do not start until both hold)
1. WP05 has landed (write-authority singular: every planning write resolves one surface).
2. WP02's live flattened-mission repro is GREEN (NFR-001) — convergence proven, not assumed.
Each topology (flattened, coord-fresh, legacy/no-mid8) hits a different leg today; collapsing before
convergence is proven would regress live missions mid-flight.

## Subtasks
### T039 — Collapse to a single-surface check (FR-011) — keep the caller compiling (squad F2)
`is_committed` already takes `placement: CommitTarget | None` (`:324`); the 3-leg OR (`:371/390/397`)
is the `placement is None` fallback. Reduce to checking the single resolved placement ref and remove
the 3-leg OR + the `diagnostics` sink (`:366/385/392/404`). **The ONLY caller is `mission.py:2131`
(owned by WP05, which lands BEFORE this WP) and it passes `diagnostics=`.** Keep the `diagnostics`
parameter BACK-COMPATIBLE (optional, accepted-and-ignored or still populated) so WP05's call site is
NOT stranded — do not change the signature in a way that breaks `mission.py:2131`.

### T040 — Prove against all topologies
Test `is_committed` for coord-fresh, create-window (#1718), flattened, and legacy/no-mid8 missions —
all must report correctly via the single check. Tie the acceptance to the WP02 gate being green.

### T041 — Campsite #1970
Remediate adjacent debt in `_substantive.py`. Bounded.

## Branch Strategy
Base/merge `feat/single-planning-surface-authority`; lane from `lanes.json`. LAST in the anchor chain.

## #1970 Campsite (ACTIVE)
Remediate adjacent debt in-slice (bounded).

## Definition of Done
- [ ] **GATE (machine-checkable, squad B3):** paste the NAME of WP02's T008 live-repro test
      (`tests/missions/test_surface_resolution_equivalence.py::<live-repro id>`) into WP history AND
      run `pytest <that id> -q` FRESH in THIS WP's session, showing green — not a reference to WP02's
      earlier run. If the named test does not exist or is not green, STOP (do not collapse).
- [ ] FR-011: `is_committed` is a single-surface check; 3-leg OR + diagnostics sink removed.
- [ ] F2: `diagnostics` param kept back-compatible — `mission.py:2131` (WP05) still compiles + tests pass.
- [ ] All topologies (coord-fresh/create-window/flattened/legacy) report correctly.
- [ ] `ruff`/`mypy` clean; complexity ≤15; campsite done; no out-of-map edits.

## Reviewer guidance
**Re-run WP02's named live-repro test yourself — approval is BLOCKED if it does not exist or is not
green at review time.** Confirm `mission.py:2131` still compiles (the `diagnostics` param stayed
back-compatible). Confirm no topology regressed (the 3-leg OR existed for a reason).
