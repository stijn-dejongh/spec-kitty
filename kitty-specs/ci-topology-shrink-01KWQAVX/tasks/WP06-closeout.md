---
work_package_id: WP06
title: 'Closeout: ratchet baseline refresh (totals unchanged) + issue-matrix terminal verdicts + #1931 rollup + closeout comments'
dependencies:
- WP04
- WP05
requirement_refs:
- NFR-007
- C-006
tracker_refs:
- '#1931'
- '#2378'
- '#1933'
- '#2383'
planning_base_branch: main
merge_target_branch: main
branch_strategy: Planning artifacts for this mission were generated on main. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into main unless the human explicitly redirects the landing branch.
base_branch: kitty/mission-ci-topology-shrink-01KWQAVX
base_commit: aa998ede7e31927286e78e7819757e03c2f2c604
created_at: '2026-07-04T21:00:00+00:00'
subtasks:
- T015
phase: Phase 6 - Closeout
assignee: ''
agent: ''
history:
- at: '2026-07-04T21:00:00Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: python-pedro
authoritative_surface: tests/architectural/_gate_coverage_baseline.json
create_intent: []
execution_mode: code_change
model: ''
owned_files:
- tests/architectural/_gate_coverage_baseline.json
- docs/changelog/CHANGELOG.md
role: implementer
tags: []
task_type: implement
---

# Work Package Prompt: WP06 – Closeout

## ⚡ Do This First: Load Agent Profile

Use the `/ad-hoc-profile-load` skill to load the agent profile specified in the frontmatter (or any user-defined profile), and behave according to its guidance before parsing the rest of this prompt.

- **Profile**: `python-pedro`
- **Role**: `implementer`

---

## ⚠️ IMPORTANT: Review Feedback

Check the `review_ref` field in the event log before starting; address all feedback.

---

## Objectives & Success Criteria

Close the mission: refresh the ratchet baseline (totals MUST stay unchanged), set every issue-matrix verdict to a terminal value, post closeout comments, and the #1931 rollup. Run the full NFR-007 invariant sweep on the merged tree to confirm all 8 #2368 invariants + the new relations are green.

## Subtasks & Detailed Guidance

### Subtask T015 – Baseline refresh + issue-matrix + closeout comments
- **Baseline refresh**: `uv run python -m tests.architectural._gate_coverage --update-baseline`. `total_tests` and `orphan_test_count` MUST stay **28573 / 0** — the carve + same-tier uniqueness add NO orphan and drop NO test. If a total changed, that is a REAL orphan/duplication regression (investigate before committing), NOT a rekey. `duplicate_test_count` may shift with the same-tier consolidation — record the delta.
- **Coordinate-note**: #2072 also re-keys `_gate_coverage_baseline.json`. Flag this shared-file coordinate in the closeout comment so a later agent does not clobber our refresh.
- **Issue-matrix terminal verdicts** (`issue-matrix.md`): set #2378 → `fixed` (shard-side split landed), #1933 → `fixed` (group-side shrink; cite the #1933-intent statement from WP05's C-006 decision), #2383 → `fixed` (arch un-blind landed), #1931 → `fixed` (rollup, terminal at closeout). The context/substrate rows (#2368/#2370/#2379) and out-of-scope rows (#2283/#2077/#2071) already carry terminal verdicts from planning — confirm they are unchanged. Zero `unknown`/`in-mission` rows may remain.
- **Closeout comments**: post on #2378 (shard-side split, PR link), #1933 (group-side shrink + the intent statement + intact escape hatches/nightly over-cover), #2383 (arch un-blind), and the #1931 rollup. Use `unset GITHUB_TOKEN` if `gh` hits a scope error (keyring token).
- **CHANGELOG**: append the mission entry to `docs/changelog/CHANGELOG.md` (root `CHANGELOG.md` is a symlink → this file — edit the target).

## Campsite cleaning (standing rule; ride the WP's normal review)

Data + docs files — keep JSON schema-consistent and the CHANGELOG entry in the existing format. No scope creep to the workflow/test files (owned by WP03/WP04/WP05).

## Definition of Done (non-fakeable — every anchor is a green test or a terminal record)

- **`_gate_coverage_baseline.json` refreshed with `total_tests`=28573 and `orphan_test_count`=0 UNCHANGED**, asserted by the orphan ratchet (`test_gate_coverage.py`) staying green on the merged tree — recorded run output.
- **NFR-007 sweep GREEN**: all 8 #2368 invariants + NFR-002/003/005 + C-005 green on the merged tree (`PWHEADLESS=1 uv run pytest tests/architectural/ -q`) — recorded output.
- **`issue-matrix.md` has zero non-terminal rows** — every verdict is `fixed`/`verified-already-fixed`/`deferred-with-followup`.
- Closeout comments posted (links recorded); #1931 rollup terminal; #2072 shared-baseline coordinate flagged.
- CHANGELOG entry appended via the symlink target.

## Risks / Reviewer Guidance

- A baseline rekey that changes totals masks a real orphan → assert totals unchanged as the DoD anchor.
- #2072 concurrently rekeys the same baseline → the closeout comment must flag the coordinate.
- Reviewer confirms no non-terminal issue-matrix row remains (mission cannot reach `done` otherwise).

## Activity Log

> Append at the END, chronological. Format: `- YYYY-MM-DDTHH:MM:SSZ – agent_id – <action>`

- 2026-07-04T21:00:00Z – system – Prompt created.
