---
work_package_id: WP07
title: Worktree-repair verb + recovery repoint + doctor de-godding
dependencies: []
requirement_refs:
- FR-007
- FR-009
- FR-010
- FR-018
tracker_refs: []
planning_base_branch: feat/single-planning-surface-authority
merge_target_branch: feat/single-planning-surface-authority
branch_strategy: Planning artifacts for this mission were generated on feat/single-planning-surface-authority. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/single-planning-surface-authority unless the human explicitly redirects the landing branch.
subtasks:
- T029
- T030
- T031
- T032
- T033
- T034
agent: claude
history:
- Created by /spec-kitty.tasks
agent_profile: python-pedro
authoritative_surface: src/specify_cli/cli/commands/agent/worktree.py
create_intent:
- src/specify_cli/cli/commands/agent/worktree.py
- src/specify_cli/cli/commands/_coord_recovery.py
- tests/specify_cli/cli/commands/agent/test_worktree_repair.py
execution_mode: code_change
owned_files:
- src/specify_cli/cli/commands/agent/worktree.py
- src/specify_cli/cli/commands/_coord_recovery.py
- src/specify_cli/cli/commands/doctor.py
- src/specify_cli/coordination/surface_resolver.py
- architecture/3.x/adr/2026-06-19-1-coord-empty-surface-fallback.md
- tests/specify_cli/cli/commands/test_doctor_coordination.py
- tests/coordination/test_surface_resolver_coord_empty_warning.py
- tests/specify_cli/coordination/test_surface_resolver.py
- tests/specify_cli/cli/commands/agent/test_worktree_repair.py
role: implementer
tags: []
---

## ⚡ Do This First: Load Agent Profile
Load + adopt `python-pedro` via `/ad-hoc-profile-load` before implementing.

## Objective
Replace the phantom `agent worktree repair` command (named across 7 code sites + an ADR + 2 passing
tests, but never registered) with a REAL recreate-or-prune verb, repoint every recovery hint to a
command that fixes its failure class, and extract the doctor coord-recovery cluster (#2059). #1890
needs RECREATE and #2062 needs ORPHAN-PRUNE — two halves of one verb. **INTERNAL ORDER: T029 → T030
→ T031 → T032** (hoist the constant, extract the cluster, then rename to the real command in one edit).

## Subtasks
### T029 — Hoist the duplicated recovery hint (FR-009 / #2059 S1192)
The `agent worktree repair --mission …` recovery sentence is duplicated 5× in `doctor.py`
(`:3092,:3116,:3209,:3225,:3245`). Hoist to ≤2 named module constants (one per failure class:
coord-recovery vs lane-sparse). Do this FIRST so the rename is a single edit point.

### T030 — Extract the doctor coord-recovery cluster (FR-018 / #2059)
Extract the cohesive worktree/coord-recovery helper cluster (`doctor.py:~3092-3225`, ~5 helpers)
into a new sibling `src/specify_cli/cli/commands/_coord_recovery.py` (mirroring `_doctrine_health.py`)
with a top-of-file `#2059` pointer. Bounded to that cluster — NOT a wider doctor.py split.

### T031 — Register the real verb (FR-007 / #1890)
Add `spec-kitty agent worktree repair --mission <slug>`: recreate a *missing* coord worktree via
`CoordinationWorkspace.resolve()`; prune an *orphaned* coord worktree (flattened mission, dir on
disk); benign no-op + clear message when there is no coordination topology. Register it in the
`agent` Typer app.

### T032 — Repoint recovery hints + ADR (per failure class)
Repoint each hint to the command that ACTUALLY fixes its class: husk → `doctor workspaces --fix`;
coord-missing/empty/orphaned → `agent worktree repair`. Update the `surface_resolver.py`
`_COORD_EMPTY_FALLBACK_WARNING` + `CoordinationBranchDeleted.next_step`, and amend ADR
`2026-06-19-1`. Reconcile to the canonical `SKILL.md` answer.

### T033 — De-pin the phantom-string tests (FR-010)
Re-point the tests that assert the nonexistent string (`test_surface_resolver_coord_empty_warning.py:127`,
`test_surface_resolver.py:276`, `test_doctor_coordination.py:132`) to assert the REAL registered command.

### T034 — Campsite #1970 + verb tests
Add tests for the verb (recreate / prune / benign-no-op). Remediate adjacent debt in touched files.

## Branch Strategy
Base/merge `feat/single-planning-surface-authority`; lane from `lanes.json`. Independent of the
anchor chain (Lane D).

## #1970 Campsite (ACTIVE)
Remediate adjacent debt in the touched files in-slice. The cluster extraction (T030) is REQUIRED.

## Definition of Done
- [ ] FR-009: recovery hint hoisted to ≤2 constants (no ≥3× duplication).
- [ ] FR-018: doctor coord-recovery cluster extracted → `_coord_recovery.py` (#2059 pointer).
- [ ] FR-007: `agent worktree repair --mission` registered; recreate/prune/no-op tested (R4).
- [ ] Every recovery hint + the ADR names a REGISTERED command.
- [ ] FR-010: phantom-string tests assert the real command.
- [ ] `ruff`/`mypy` clean; complexity ≤15; campsite done; no out-of-map edits.

## Reviewer guidance
Confirm the verb is registered (`spec-kitty agent worktree repair --help` works), the extraction is
bounded, and NO recovery string anywhere names an unregistered command (WP08's guard will enforce it).
