---
work_package_id: WP07
title: 'InstalledVersion routing + #2447 doc tail'
dependencies:
- WP01
requirement_refs:
- FR-010
- FR-011
tracker_refs: []
planning_base_branch: feat/mission-resolver-port-2173
merge_target_branch: feat/mission-resolver-port-2173
branch_strategy: Planning artifacts for this mission were generated on feat/mission-resolver-port-2173. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/mission-resolver-port-2173 unless the human explicitly redirects the landing branch.
subtasks:
- T027
- T028
- T029
history:
- at: '2026-07-08T18:06:06+00:00'
  actor: planner
  action: created
agent_profile: python-pedro
authoritative_surface: src/specify_cli/
create_intent:
- tests/architectural/test_git_matrix_paths_resolve.py
execution_mode: code_change
owned_files:
- src/specify_cli/upgrade/migrations/m_2_1_4_enforce_command_file_state.py
- src/doctrine/skills/spec-kitty-git-workflow/references/git-operations-matrix.md
- tests/architectural/test_git_matrix_paths_resolve.py
role: implementer
tags: []
---

## ⚡ Do This First: Load Agent Profile

Load your agent profile via `/ad-hoc-profile-load` for `python-pedro` (implementer). Then read
`kitty-specs/mission-resolver-port-01KX1C05/spec.md` (FR-010/FR-011), `plan.md` (IC-06 second half), and
`research.md`.

## Objective

Two small same-surface residuals: route the un-routed migration version read through the **existing**
`_CliStatusLike` Protocol (no new port), and fix the shipped-doctrine phantom `#2447` with a guard so it
can't recur.

## Subtasks

### T027 — InstalledVersion routing (FR-010)
- `upgrade/migrations/m_2_1_4_enforce_command_file_state.py:55` has an ad-hoc `_get_cli_version()` read.
  Route it through the already-existing `_CliStatusLike` Protocol (`readiness/upgrade_ux.py:50`) so the
  migration's version read uses the canonical surface. Do NOT introduce a new port — this is a
  finish-the-routing job. Preserve migration behavior exactly (migrations replay against fixtures).

### T028 — #2447 doctrine phantom (FR-011)
- `src/doctrine/skills/spec-kitty-git-workflow/references/git-operations-matrix.md:28` cites the phantom
  `core/mission_detection.py::_detect_from_branch()` (a file/function that never existed). Make the
  doctrine-accuracy call: either (a) repoint the row to the real current-branch surface that calls
  `lanes/branch_naming.py::parse_mission_slug_from_branch`, or (b) remove the row if branch-slug detection
  is no longer a git-command surface. Prefer (a) if a real reader exists; else (b) with a note.
- This is **shipped doctrine** — run `pytest tests/architectural/test_no_legacy_terminology.py` and the
  full `tests/architectural/` locally before considering it done (CI-only shard risk, F7).

### T029 — Path-resolution guard (prevents recurrence)
- New `tests/architectural/test_git_matrix_paths_resolve.py`: assert that **every `src/…` path referenced
  in `git-operations-matrix.md` resolves on disk**. Parse the matrix, extract path-shaped cells, and fail
  if any does not exist. This guards the whole matrix, not just the one row.

## Branch Strategy
Planning branch and merge target: `feat/mission-resolver-port-2173`. Lane worktree per `lanes.json`.

## Definition of Done
- Migration version read goes through `_CliStatusLike`; migration behavior unchanged.
- The phantom row is repointed/removed; the new guard passes and fails on a planted phantom path.
- Terminology guard + full `tests/architectural/` green; `ruff`/`mypy` clean.

## Risks / reviewer guidance
- Doctrine is distributed to user projects — reviewer confirms the row is accurate now and the guard bites.
- Confirm the migration still replays correctly (byte-exact fixture behavior).
