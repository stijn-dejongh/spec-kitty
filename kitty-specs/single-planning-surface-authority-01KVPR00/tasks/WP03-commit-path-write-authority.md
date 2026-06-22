---
work_package_id: WP03
title: Commit-path write-authority adoption
dependencies:
- WP02
requirement_refs:
- FR-001
- FR-002
- NFR-002
tracker_refs: []
planning_base_branch: feat/single-planning-surface-authority
merge_target_branch: feat/single-planning-surface-authority
branch_strategy: Planning artifacts for this mission were generated on feat/single-planning-surface-authority. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/single-planning-surface-authority unless the human explicitly redirects the landing branch.
subtasks:
- T010
- T011
- T012
- T013
agent: claude
history:
- Created by /spec-kitty.tasks
agent_profile: python-pedro
authoritative_surface: src/specify_cli/cli/commands/safe_commit_cmd.py
create_intent: []
execution_mode: code_change
owned_files:
- src/specify_cli/cli/commands/safe_commit_cmd.py
- src/specify_cli/cli/commands/spec_commit_cmd.py
- tests/specify_cli/cli/commands/test_safe_commit_cmd.py
- tests/specify_cli/cli/commands/test_spec_commit_cmd.py
role: implementer
tags: []
---

## ⚡ Do This First: Load Agent Profile
Load + adopt `python-pedro` via `/ad-hoc-profile-load` before implementing.

## Objective
Route the planning-artifact commit path through the single write authority `resolve_placement_only`
(`src/mission_runtime/resolution.py:761`), and SEPARATE `safe-commit`'s two responsibilities:
mission-aware planning commits resolve placement via the authority; generic operator-file commits
keep their existing behavior (NFR-002). This is the #2063 root: `safe-commit._resolve_commit_target`
currently resolves the destination from the current `HEAD` branch — mission-blind.

## Subtasks
### T010 — safe-commit mission-aware path → resolve_placement_only (FR-001/FR-002)
In `safe_commit_cmd.py:_resolve_commit_target`: when the commit targets a mission artifact
(`kitty-specs/<slug>/` path detected), resolve the destination via `resolve_placement_only` rather
than `HEAD`. Keep the generic (non-mission) operator-file path exactly as-is (NFR-002). Do NOT
overload one function — separate the two responsibilities cleanly.

### T011 — spec-commit routes the same authority (FR-001)
Confirm `spec_commit_cmd.py` routes planning commits through the same authority; consolidate any
duplicate placement-resolution logic shared with safe-commit into the single seam (don't fork it).

### T012 — Tests (FR-001/NFR-002) — bind to a coherence check (squad N1)
- Quickstart R2 coherence: a mission `spec.md` committed via the mission-aware path is then VISIBLE to
  the immediately-following finalize read (not just "a file landed somewhere") — the #2063 close.
- The generic operator-file `safe-commit` path is preserved (regression test — it must NOT become
  mission-aware or break).

### T013 — Campsite #1970
Remediate adjacent debt in safe/spec-commit. NOTE: the `--to-branch` "required in v3.3" deprecation
(`safe_commit_cmd.py:~189-212`) is NOT-DUE at 3.2.x — LEAVE it (record the note); do not remove the
HEAD-inference now.

## Branch Strategy
Base/merge `feat/single-planning-surface-authority`; lane from `lanes.json`. Sequenced after WP02
(read-path safety net green).

## #1970 Campsite (ACTIVE)
Remediate adjacent debt in the touched commit surfaces in-slice (bounded).

## Definition of Done
- [ ] FR-001/FR-002: planning commits route through `resolve_placement_only`; no HEAD-derived write target.
- [ ] NFR-002: generic `safe-commit` operator-file path preserved + tested.
- [ ] Duplicate placement logic consolidated (not forked).
- [ ] `ruff`/`mypy` clean; complexity ≤15; campsite done; no out-of-map edits.

## Reviewer guidance
Verify the two responsibilities are genuinely separated (generic safe-commit unchanged). Confirm no
new placement resolver was introduced (adopt the SSOT — C-003).
