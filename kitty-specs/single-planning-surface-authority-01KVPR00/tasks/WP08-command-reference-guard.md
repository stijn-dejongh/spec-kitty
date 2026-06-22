---
work_package_id: WP08
title: Command-reference guard + merge.py path-sink
dependencies:
- WP07
requirement_refs:
- FR-008
- FR-016
- NFR-003
tracker_refs: []
planning_base_branch: feat/single-planning-surface-authority
merge_target_branch: feat/single-planning-surface-authority
branch_strategy: Planning artifacts for this mission were generated on feat/single-planning-surface-authority. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/single-planning-surface-authority unless the human explicitly redirects the landing branch.
subtasks:
- T035
- T036
- T037
- T038
agent: claude
history:
- Created by /spec-kitty.tasks
agent_profile: python-pedro
authoritative_surface: tests/architectural/test_command_references.py
create_intent:
- tests/architectural/test_command_references.py
- tests/specify_cli/cli/commands/test_merge_path_sink.py
execution_mode: code_change
owned_files:
- tests/architectural/test_command_references.py
- src/specify_cli/cli/commands/merge.py
- tests/specify_cli/cli/commands/test_merge_path_sink.py
role: implementer
tags: []
---

## ⚡ Do This First: Load Agent Profile
Load + adopt `python-pedro` via `/ad-hoc-profile-load` before implementing.

## Objective
Add the architectural guard that would have caught the #1890 phantom: scan Python literals + ADRs
for `spec-kitty <tokens>` invocations and assert each names a REGISTERED Typer command. Self-validate
it (NFR-003 gate-unmask discipline). Also harden the third #2037 path sink (merge.py).

## Context
The existing guard (`test_docs_cli_reference_parity.py`) scans only doctrine markdown bash-fences —
blind to Python string literals + ADRs, which is why the phantom survived #2008.

## Subtasks
### T035 — Command-reference guard (FR-008)
New `tests/architectural/test_command_references.py`: scan `src/specify_cli/**/*.py` string literals
and `architecture/**/*.md` (ADRs) for `` `spec-kitty <tokens>` `` / `"spec-kitty …"` invocations;
assert each path tuple is a registered Typer command (reuse `_build_live_app` + the registered-path
walk from `test_docs_cli_reference_parity.py`). Restrict the literal scan to strings containing
`spec-kitty ` + a path token (anti-false-positive). Allowlist entries require a rationale comment.

### T036 — Planted-phantom self-test + dry-run (NFR-003)
Add a self-test that PLANTS a bogus `spec-kitty agent nonesuch` in a Python literal and asserts the
guard goes RED (mirrors `test_guard_rejects_planted_nonexistent_command`). Run the FULL
`tests/architectural/` suite as the gate-unmask dry-run and confirm the guard is green on the clean
tree (WP07 must have fixed all strings first — hence the WP07 dependency). NEVER ship a
mission-diff-scoped assertion to main.

### T037 — Harden merge.py:1055 untrusted-path sink (FR-016 / #2037)
Route the CLI-arg `--mission` join at `merge.py:~1055` through
`assert_safe_path_segment`/`ensure_within_any` + a negative test.

### T038 — Campsite #1970
Remediate adjacent debt in the touched files. Bounded.

## Branch Strategy
Base/merge `feat/single-planning-surface-authority`; lane from `lanes.json`. After WP07 (strings fixed).

## #1970 Campsite (ACTIVE)
Remediate adjacent debt in-slice (bounded).

## Definition of Done
- [ ] FR-008: guard scans Python literals + ADRs vs registered commands; green on clean tree.
- [ ] NFR-003: planted-phantom self-test RED on a planted literal; full-suite dry-run run + recorded.
- [ ] FR-016: `merge.py:1055` sink hardened + negative test.
- [ ] `ruff`/`mypy` clean; complexity ≤15; campsite done; no out-of-map edits.

## Reviewer guidance
Confirm the guard genuinely fails on a planted phantom (not a no-op). Confirm it's green on the clean
tree only AFTER WP07 — if RED, a recovery string still names an unregistered command.
