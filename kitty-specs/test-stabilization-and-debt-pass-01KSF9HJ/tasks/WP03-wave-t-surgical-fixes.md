---
work_package_id: WP03
title: 'Wave T surgical fixes: dashboard scanner + move-task commit-message (FR-003, FR-004)'
dependencies:
- WP01
requirement_refs:
- FR-003
- FR-004
planning_base_branch: kitty/mission-test-stabilization-and-debt-pass-01KSF9HJ
merge_target_branch: main
subtasks:
- T008
- T009
agent: claude
history:
- by: claude
  at: '2026-05-25T14:00:00+00:00'
  action: generated
agent_profile: python-pedro
authoritative_surface: tests/
execution_mode: code_change
mission_id: 01KSF9HJBFKRBC617JVHKZXNE2
mission_slug: test-stabilization-and-debt-pass-01KSF9HJ
owned_files:
- tests/test_dashboard/test_scanner.py
- tests/tasks/test_move_task_git_validation_unit.py
- src/specify_cli/dashboard/scanner.py
- src/specify_cli/tasks/move_task.py
priority: P0
role: implementer
tags: []
---

## ⚡ Do This First: Load Agent Profile

Invoke `/ad-hoc-profile-load` with argument `python-pedro` before reading further. Two surgical fixes, both small assertion/contract drifts.

## Objective

Two unrelated single-test failures, fixed in parallel:

- **T008 / FR-003**: `tests/test_dashboard/test_scanner.py::test_build_event_log_kanban_stats_tolerates_weighted_progress_failure` — tolerance-window assertion fails on a weighted-progress computation that has drifted slightly. Either the test's tolerance is too tight or the production path's tolerance is correct and the test expectation needs widening.
- **T009 / FR-004**: `tests/tasks/test_move_task_git_validation_unit.py::test_move_for_review_from_worktree_does_not_mirror_commit_to_lane_branch` — assertion `'Move WP01 to for_review' in 'Add task file'` fails because the move-task implementation now uses a different commit message ("Add task file" appears to be a different operation's commit). Either the test contract drifted or the implementation changed semantics.

## Branch strategy

- Planning base branch: mission lane branch
- Merge target branch: `main`
- Execution: lane workspace allocated by `finalize-tasks`.

## Context

- [`triage.md`](../triage.md) — verify these are still single-failure clusters per WP01's enumeration.
- [`spec.md`](../spec.md) FR-003, FR-004.

## Subtask details

### T008 — Dashboard scanner tolerance fix [P]

Run the failing test with `--tb=long`:
```bash
PWHEADLESS=1 .venv/bin/pytest tests/test_dashboard/test_scanner.py::test_build_event_log_kanban_stats_tolerates_weighted_progress_failure -x --tb=long
```

Examine the assertion. Likely patterns:
- **Tolerance too tight**: expected value `0.5` vs actual `0.5001` — widen the tolerance with `pytest.approx(..., abs=1e-3)`.
- **Production drift**: the weighted-progress formula in `src/specify_cli/dashboard/scanner.py::build_event_log_kanban_stats` produces a different value than before. Investigate which is correct.

If production is correct, update the test expectation + add a docstring note explaining the formula. If test is correct, fix production with a minimal change. DO NOT change semantics — this WP is surgical, not a redesign.

### T009 — Move-task commit-message assertion fix [P]

Run the failing test:
```bash
PWHEADLESS=1 .venv/bin/pytest tests/tasks/test_move_task_git_validation_unit.py::test_move_for_review_from_worktree_does_not_mirror_commit_to_lane_branch -x --tb=long
```

The assertion `'Move WP01 to for_review' in 'Add task file'` says the move-task code is now committing `'Add task file'` where the test expected `'Move WP01 to for_review'`.

Two possible root causes:
1. **Move-task production code** in `src/specify_cli/tasks/move_task.py` was refactored to use a different commit-message template; test still expects the old format.
2. **Test fixture setup** is creating a `'Add task file'` commit BEFORE the move-task call, and the assertion is matching the wrong commit in the test's history-inspection logic.

Fix the more honest one: if the test's assertion was the contract and production drifted, fix production. If the test was sloppy about which commit it asserts against, fix the test. Document the decision in the commit message.

## Definition of Done

- [ ] T008: `pytest tests/test_dashboard/test_scanner.py -q` reports 0 failures.
- [ ] T009: `pytest tests/tasks/test_move_task_git_validation_unit.py -q` reports 0 failures.
- [ ] Commit message documents which side (test or production) drifted in each case.
- [ ] `ruff check` clean on touched files.

## Risks

- **Tolerance fix that masks a real regression**: if T008 is widening tolerance, document explicitly that the production value is still within a reasonable spec, not just "tests pass now". A tolerance widening with no rationale is a smell.
- **Move-task semantics change**: if T009 reveals that the move-task code path is missing a commit-message branch, that's a deeper issue than this WP can absorb — file a sub-issue and skip the test with a documented `xfail` rationale.

## Reviewer guidance

1. For T008: verify the tolerance change is documented with a unit-tested rationale (formula constants haven't changed).
2. For T009: verify the chosen fix-side (test or prod) is the right one by checking git blame on the suspect line.
