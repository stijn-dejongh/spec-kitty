---
work_package_id: WP10
title: Doctrine charter prompt off safe-commit
dependencies:
- WP03
requirement_refs:
- FR-002
tracker_refs: []
planning_base_branch: feat/single-planning-surface-authority
merge_target_branch: feat/single-planning-surface-authority
branch_strategy: Planning artifacts for this mission were generated on feat/single-planning-surface-authority. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/single-planning-surface-authority unless the human explicitly redirects the landing branch.
subtasks:
- T042
- T043
- T044
agent: claude
history:
- Created by /spec-kitty.tasks
agent_profile: python-pedro
authoritative_surface: src/doctrine/missions/mission-steps/software-dev/charter/prompt.md
create_intent: []
execution_mode: code_change
owned_files:
- src/doctrine/missions/mission-steps/software-dev/charter/prompt.md
role: implementer
tags: []
---

## ⚡ Do This First: Load Agent Profile
Load + adopt `python-pedro` via `/ad-hoc-profile-load` before implementing.

## Objective
Migrate the charter mission-step prompt off `safe-commit` to the mission-aware `spec-commit` (the
doctrine half of FR-002). The specify prompt already uses `spec-commit`; the charter prompt
(`charter/prompt.md:~198`) is the remaining drift that lets planning artifacts land on the wrong
surface (#2063). **Edit the SOURCE template only** (`src/doctrine/...`), never the generated agent
copies.

## Subtasks
### T042 — Migrate charter/prompt.md off safe-commit (FR-002 doctrine)
Replace the `safe-commit` planning-commit instruction (`:~198`, `:~207`) with the mission-aware
`spec-commit` invocation, matching the specify prompt's pattern.

### T043 — Pre-push gates
Run `pytest tests/architectural/test_no_legacy_terminology.py` (CI-only forbidden-term gate) AND the
full `tests/architectural/` sweep before handoff — doctrine/prose edits trip CI-only gates.

### T044 — Campsite #1970
Remediate adjacent stale references in the touched prompt (e.g. any other non-canonical command
mention). Bounded to this file.

## Branch Strategy
Base/merge `feat/single-planning-surface-authority`; lane from `lanes.json`. After WP03 (spec-commit
adoption confirmed).

## #1970 Campsite (ACTIVE)
Remediate adjacent debt in-slice (bounded to the prompt).

## Definition of Done
- [ ] FR-002 (doctrine): charter prompt uses `spec-commit`, not `safe-commit`.
- [ ] Terminology guard + full `tests/architectural/` sweep green pre-push.
- [ ] SOURCE template edited (not generated agent copies); campsite done; no out-of-map edits.

## Reviewer guidance
Confirm the edit is on the `src/doctrine/` SOURCE (not `.claude/`/`.codex/` copies). Confirm no
forbidden terms introduced (the terminology gate is CI-only).
