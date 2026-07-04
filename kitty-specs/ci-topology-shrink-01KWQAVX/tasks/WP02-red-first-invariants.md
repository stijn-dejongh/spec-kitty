---
work_package_id: WP02
title: 'Red-first invariants: SC-001 worklist, NFR-002 arch-matrix, NFR-003 uniqueness, C-005 coverage-consumer, FR-011 serial, NFR-005 ceiling'
dependencies:
- WP01
requirement_refs:
- FR-001
- FR-011
- NFR-002
- NFR-003
- NFR-005
- C-005
tracker_refs: []
planning_base_branch: main
merge_target_branch: main
branch_strategy: Planning artifacts for this mission were generated on main. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into main unless the human explicitly redirects the landing branch.
base_branch: kitty/mission-ci-topology-shrink-01KWQAVX
base_commit: aa998ede7e31927286e78e7819757e03c2f2c604
created_at: '2026-07-04T21:00:00+00:00'
subtasks:
- T004
- T005
- T006
phase: Phase 2 - Red-first invariants
assignee: ''
agent: ''
history:
- at: '2026-07-04T21:00:00Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: python-pedro
authoritative_surface: tests/architectural/
create_intent:
- tests/architectural/test_ci_topology_worklist.py
- tests/architectural/test_arch_unblind_matrix.py
- tests/architectural/test_same_tier_uniqueness.py
- tests/architectural/test_coverage_consumer_needs.py
- tests/architectural/test_serial_port_preservation.py
- tests/architectural/test_job_count_ceiling.py
execution_mode: code_change
model: ''
owned_files:
- tests/architectural/test_ci_topology_worklist.py
- tests/architectural/test_arch_unblind_matrix.py
- tests/architectural/test_same_tier_uniqueness.py
- tests/architectural/test_coverage_consumer_needs.py
- tests/architectural/test_serial_port_preservation.py
- tests/architectural/test_job_count_ceiling.py
role: implementer
tags: []
task_type: implement
---

# Work Package Prompt: WP02 – Red-first invariants

## ⚡ Do This First: Load Agent Profile

Use the `/ad-hoc-profile-load` skill to load the agent profile specified in the frontmatter (or any user-defined profile), and behave according to its guidance before parsing the rest of this prompt.

- **Profile**: `python-pedro`
- **Role**: `implementer`

---

## ⚠️ IMPORTANT: Review Feedback

Check the `review_ref` field in the event log before starting; address all feedback.

---

## Objectives & Success Criteria

Author the six NEW architectural invariants the post-tasks squad demanded — **each authored FAILING against today's topology** so WP03 has a red-to-green target that cannot be faked. NEW test files ONLY; the existing `tests/architectural/` suite is UNTOUCHED (`git diff --stat` must show only the six new files). Every invariant pins a BEHAVIORAL RELATION over the parsed model (Directive 041 — refactor-stable), never a workflow line number. All six files are `architectural`-marked so CI selects them.

Consume ONLY the additive relations WP01 added to `_gate_coverage.py` (and the committed census). Do NOT re-derive the bound model here.

## Subtasks & Detailed Guidance

### Subtask T004 [P] – Worklist + arch-unblind matrix
- `test_ci_topology_worklist.py` (**SC-001 / FR-001 / NFR-006**): load the committed `ci-topology-census.json`, ITERATE `worklist[]`, assert each dir maps to a named src-backed filter group AND a focused shard, and that a touch of `src/specify_cli/<dir>/**` does NOT set `unmatched=true`/`run_all`. The floor `t_loc` comes from the artifact, NOT a literal. RED today: every worklist dir currently trips `unmatched`.
- `test_arch_unblind_matrix.py` (**SC-002 / NFR-002**): assert the differential-matrix relation selects the arch/adversarial suite over **100%** of `src/specify_cli/*` dirs (0 blind). RED today: 13 arch-blind dirs.

### Subtask T005 [P] – Same-tier uniqueness + coverage-consumer
- `test_same_tier_uniqueness.py` (**NFR-003 / SC-004**): assert no test is selected by >1 fast shard nor by >1 integration shard (over the same-tier relation). Distinct from the existing report-only cross-tier duplicate warning. Assert `_gate_coverage` orphan count stays 0 and total selected unchanged (baseline totals). RED today: authored against the post-split expectation, may need a fault-injection fixture to prove it bites.
- `test_coverage_consumer_needs.py` (**C-005 / FR-006 / FR-007**): assert coverage-emitting jobs ⊆ `sonarcloud.needs` AND critical-path emitters ⊆ `diff-coverage.needs` (and `mutation-testing.needs` where it consumes them). **Assert the NEGATIVE**: the invariant must NOT intersect `slow-tests.needs` (fast-jobs-only — would red on arrival). RED today: the new WP03 jobs do not yet exist / are not yet in the consumer lists.

### Subtask T006 [P] – Serial-port preservation + job-count ceiling
- `test_serial_port_preservation.py` (**FR-011**): assert every shard whose positional roots include daemon/real-port tests (e.g. `tests/sync/test_orphan_sweep.py`, ports 9400-9449) preserves a `-n0` serial pass and uses `--dist loadfile` (never bare `load`) + per-worker HOME isolation. RED today if WP03's split were to drop the serial pass (author against the post-split shape; use a fault-injection negative to prove it bites).
- `test_job_count_ceiling.py` (**NFR-005**): assert `len(quality-gate.needs) ≤ CEILING`. Pin `CEILING` from the plan's composite design (~57 with composites; today ~45). RED-negative discipline: also prove the test would red if the graph exceeded the ceiling (fault-injection).

## Implementation Notes

- RED-first is a DoD anchor: run each new file on the planning base and RECORD the failing output. Any invariant that is green pre-WP03 is a defect (vacuous) — re-author with a fault-injection fixture until it bites.
- Pin behavioral relations, not line numbers. Where a relation needs a synthetic universe, keep the synthetic size out of the assertion's meaning (do not hard-code the real census count).

## Campsite cleaning (standing rule; ride the WP's normal review)

New files — write them clean from the start: `ruff --select ALL` exit 0, `mypy` Success, docstrings on every test, no `# noqa` unless individually justified. Do not touch files outside the six owned.

## Definition of Done (non-fakeable — every anchor is recorded RED evidence)

- **Six new files exist, `architectural`-marked, RED on the planning base** with the failing output pasted per file in the Activity Log (`AttributeError`/assertion, iterating real census/model data — not a placeholder skip).
- **Zero edits to any pre-existing test file** (`git diff --stat` shows only the six new files).
- Each invariant proven to BITE: fault-injection red-negative recorded for NFR-003/FR-011/NFR-005 (relations that could pass vacuously).
- `ruff` + `mypy` clean on the six files.

## Risks / Reviewer Guidance

- Reject any vacuously-green invariant (passes on today's broken topology) — RED evidence is the gate.
- Reject a coverage-consumer test that intersects `slow-tests.needs` — the C-005 correction is explicit; it must assert the negative.
- Reject any edit to the existing suite — WP02 is new-files-only by contract.

## Activity Log

> Append at the END, chronological. Format: `- YYYY-MM-DDTHH:MM:SSZ – agent_id – <action>`

- 2026-07-04T21:00:00Z – system – Prompt created.
