---
work_package_id: WP05
title: 'Coverage-topology + timing verification: FR-006 emit-consume ownership test + NFR-001 acceptance observation + C-006 nightly decision'
dependencies:
- WP03
requirement_refs:
- FR-006
- NFR-001
- C-006
tracker_refs: []
planning_base_branch: main
merge_target_branch: main
branch_strategy: Planning artifacts for this mission were generated on main. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into main unless the human explicitly redirects the landing branch.
base_branch: kitty/mission-ci-topology-shrink-01KWQAVX
base_commit: aa998ede7e31927286e78e7819757e03c2f2c604
created_at: '2026-07-04T21:00:00+00:00'
subtasks:
- T013
- T014
phase: Phase 5 - Verification
assignee: ''
agent: ''
history:
- at: '2026-07-04T21:00:00Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: python-pedro
authoritative_surface: tests/release/
create_intent:
- tests/release/test_coverage_topology_ownership.py
- tests/release/ci_topology_timings_postshrink.json
execution_mode: code_change
model: ''
owned_files:
- tests/release/test_coverage_topology_ownership.py
- tests/release/ci_topology_timings_postshrink.json
role: implementer
tags: []
task_type: implement
---

# Work Package Prompt: WP05 – Coverage-topology + timing verification

## ⚡ Do This First: Load Agent Profile

Use the `/ad-hoc-profile-load` skill to load the agent profile specified in the frontmatter (or any user-defined profile), and behave according to its guidance before parsing the rest of this prompt.

- **Profile**: `python-pedro`
- **Role**: `implementer`

---

## ⚠️ IMPORTANT: Review Feedback

Check the `review_ref` field in the event log before starting; address all feedback.

---

## Objectives & Success Criteria

Two verification deliverables (both non-fakeable):
1. **FR-006 emit⇒consume by construction**: a coverage-ownership test asserting every new shard's `coverage-<D>.xml` is matched by the aggregator's `coverage-*.xml` wildcard consumer — a distinct guard from WP02's C-005 needs-list membership (needs-list vs glob-consumption are two different silent-drop vectors).
2. **NFR-001 acceptance observation**: measure the post-shrink core-misc critical-path lane against the committed 29.4-min baseline (WP01's census `timings_baseline`) in a committed timings artifact; confirm no nightly blind spot; make the C-006 nightly decision iff the measured PR critical path still >~15 min.

## Subtasks & Detailed Guidance

### Subtask T013 [P] – Coverage-topology ownership test (FR-006)
Author `tests/release/test_coverage_topology_ownership.py`: parse `ci-quality.yml` (reuse `_gate_coverage`'s model — do NOT re-parse by hand), assert every job emitting a `coverage-*.xml` has a name matched by the aggregator's wildcard download pattern (emit⇒consume by construction). RED-negative: prove the test would red if a shard emitted `coverage-orphan-<D>.xml` outside the glob. This runs in parallel with WP04 (disjoint files).

### Subtask T014 – Post-shrink timings artifact + C-006 decision (NFR-001)
- Trigger a full `run_all` CI run on the mission branch (or read a representative post-WP03 run). Record `tests/release/ci_topology_timings_postshrink.json`:
  - measured `fast_core_misc_lane_min` (matrix, parallel), `arch_adversarial_min` (de-serialized), `core_misc_critical_path_min`, `next_longest_lane_min`, `source_run_id`.
  - `verdict`: critical path ≤ 55% × 29.4 (≤16.2) AND ≤ next-longest lane (≈13.6) ⇒ effective ceiling ≈13.6 min (NFR-001).
- **C-006 nightly decision**: if the measured PR critical path is still >~15 min, evaluate a THIN nightly-schedule option in-mission; else record that the shrink satisfies #1933's INTENT (fast, targeted PR CI) with escape hatches (`ci:full`/`ready-for-ci`/`workflow_dispatch`) + nightly `run_all` over-cover intact (FR-009 no new blind spot).
- Confirm no nightly blind spot: the nightly `run_all` still over-covers every worklist dir + the sub-`T_LOC` catch-all-safe tail.

## Implementation Notes

- NFR-001 is a plan/verify ACCEPTANCE OBSERVATION recorded in the committed artifact, NOT a flaky standing timing unit gate.
- The timings artifact is SEPARATE from WP01's census (owned-file disjointness): WP01 holds the pre-mission 29.4-min baseline; WP05 holds the post-mission measurement.

## Campsite cleaning (standing rule; ride the WP's normal review)

New test file — `ruff --select ALL` exit 0, `mypy` Success, docstring the test. The timings artifact is data (JSON) — schema-consistent with the census `timings_baseline` shape.

## Definition of Done (non-fakeable — every anchor is a green test or a committed measurement)

- **`test_coverage_topology_ownership.py` GREEN** with a recorded RED-negative proving it bites (a mis-named `coverage-orphan-*.xml` reds).
- **`ci-topology-timings-postshrink.json` committed** with a measured critical path ≤ the NFR-001 ceiling and a cited `source_run_id` (a live measurement, not a projection).
- **C-006 decision recorded**: nightly option taken iff measured >15 min, else the #1933-intent statement + intact escape hatches + nightly over-cover.
- `ruff` + `mypy` clean on the new test file.

## Risks / Reviewer Guidance

- Measured critical path still >ceiling → record honestly and trigger the C-006 nightly evaluation; do NOT paper over with a projection.
- A coverage XML silently dropped → the ownership test reds; this complements (does not duplicate) WP02's needs-list invariant.

## Activity Log

> Append at the END, chronological. Format: `- YYYY-MM-DDTHH:MM:SSZ – agent_id – <action>`

- 2026-07-04T21:00:00Z – system – Prompt created.
