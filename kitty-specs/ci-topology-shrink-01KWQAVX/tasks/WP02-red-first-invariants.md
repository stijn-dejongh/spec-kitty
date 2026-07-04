---
work_package_id: WP02
title: 'Red-first invariants: SC-001 worklist, NFR-002 arch-matrix, NFR-003 uniqueness, C-005 coverage-consumer, FR-011 serial, NFR-005 ceiling, FR-013 arch-pole-deserialized, SC-003a shard-universe-bounded'
dependencies:
- WP01
requirement_refs:
- FR-001
- FR-011
- FR-013
- NFR-002
- NFR-003
- NFR-005
- NFR-006
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
- T016
- T017
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
- tests/architectural/test_arch_pole_deserialized.py
- tests/architectural/test_shard_universe_bounded.py
execution_mode: code_change
model: ''
owned_files:
- tests/architectural/test_ci_topology_worklist.py
- tests/architectural/test_arch_unblind_matrix.py
- tests/architectural/test_same_tier_uniqueness.py
- tests/architectural/test_coverage_consumer_needs.py
- tests/architectural/test_serial_port_preservation.py
- tests/architectural/test_job_count_ceiling.py
- tests/architectural/test_arch_pole_deserialized.py
- tests/architectural/test_shard_universe_bounded.py
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

Author the eight NEW architectural invariants the post-tasks squad demanded — **each authored FAILING against today's topology** so WP03 has a red-to-green target that cannot be faked. NEW test files ONLY; the existing `tests/architectural/` suite is UNTOUCHED (`git diff --stat` must show only the eight new files). Every invariant pins a BEHAVIORAL RELATION over the parsed model (Directive 041 — refactor-stable), never a workflow line number. All eight files are `architectural`-marked so CI selects them.

Consume ONLY the additive relations WP01 added to `_gate_coverage.py` (and the committed census). Do NOT re-derive the bound model here.

## Subtasks & Detailed Guidance

### Subtask T004 [P] – Worklist + arch-unblind matrix
- `test_ci_topology_worklist.py` (**SC-001 / FR-001 / NFR-006**): load the committed `tests/architectural/ci_topology_census.json`, ITERATE `worklist[]`, assert each dir maps to a named src-backed filter group AND a focused shard, and that a touch of `src/specify_cli/<dir>/**` does NOT set `unmatched=true`/`run_all`. The floor `t_loc` comes from the artifact, NOT a literal. RED today: every worklist dir currently trips `unmatched`.
  - **Freshness-guard assertion (NFR-006 seam — closes SC-001 vacuous-pass gaming)**: add a GREEN `architectural`-marked assertion `census.worklist == live_derived_worklist()` that calls WP01's pure re-derivation function (the seam WP01 exposes for this test) and re-derives the worklist from the LIVE tree. A hand-trimmed or stale census then REDS in CI — the freshness check is a pytest-collected assertion, NOT pasted prose in an Activity Log. This is the mechanized replacement for the "pasted live self-check output" anchor.
- `test_arch_unblind_matrix.py` (**SC-002 / NFR-002**): assert the differential-matrix relation selects the arch/adversarial suite over **100%** of `src/specify_cli/*` dirs (0 blind). RED today: 13 arch-blind dirs.

### Subtask T005 [P] – Same-tier uniqueness + coverage-consumer
- `test_same_tier_uniqueness.py` (**NFR-003 / SC-004**): assert no test is selected by >1 fast shard nor by >1 integration shard (over the same-tier relation). Distinct from the existing report-only cross-tier duplicate warning. Assert `_gate_coverage` orphan count stays 0 and total selected unchanged (baseline totals). RED today: authored against the post-split expectation, may need a fault-injection fixture to prove it bites.
- `test_coverage_consumer_needs.py` (**C-005 / FR-006 / FR-007**): assert coverage-emitting jobs ⊆ `sonarcloud.needs` AND critical-path emitters ⊆ `diff-coverage.needs` (and `mutation-testing.needs` where it consumes them). **Assert the NEGATIVE**: the invariant must NOT intersect `slow-tests.needs` (fast-jobs-only — would red on arrival). RED today: the new WP03 jobs do not yet exist / are not yet in the consumer lists.

### Subtask T006 [P] – Serial-port preservation + job-count ceiling
- `test_serial_port_preservation.py` (**FR-011**): assert every shard whose positional roots include daemon/real-port tests (e.g. `tests/sync/test_orphan_sweep.py`, ports 9400-9449) preserves a `-n0` serial pass and uses `--dist loadfile` (never bare `load`) + per-worker HOME isolation. RED today if WP03's split were to drop the serial pass (author against the post-split shape; use a fault-injection negative to prove it bites).
- `test_job_count_ceiling.py` (**NFR-005**): assert `len(quality-gate.needs) ≤ CEILING`. Pin `CEILING` from the plan's composite design (~57 with composites; today ~45). RED-negative discipline: also prove the test would red if the graph exceeded the ceiling (fault-injection).

### Subtask T016 [P] – Arch-pole de-serialization structural gate (FR-013)
- `test_arch_pole_deserialized.py` (**FR-013 / structural**): parse the arch/adversarial job's `needs` set from the bound model and assert it contains **NO fast-lane job** (e.g. `fast-tests-core-misc`). This is the structural gate the squad demanded because `if: always()` + `needs: [fast-tests-core-misc]` is STILL serialized — `always()` ≠ parallel; the job still waits on the fast lane's timeline before starting. Only DROPPING the edge de-serializes it (FR-013). **NATURAL RED today** (the serialization edge is present); flips GREEN when WP03 drops `needs: fast-tests-core-misc`. Pin the BEHAVIORAL relation (parsed `needs` set excludes any fast-lane job), never a workflow line number.

### Subtask T017 [P] – Shard-universe boundedness (SC-003a)
- `test_shard_universe_bounded.py` (**SC-003a / structural**): over the parsed shard-command set, assert that NO single shard collects the full catch-all universe — e.g. the max single-shard selected-test-count is strictly `< total`, OR the shard count is `≥ N` (the pinned shard-count from the composite design). Rationale: same-tier uniqueness (NFR-003) alone does NOT imply the monolith was split — one giant shard trivially satisfies uniqueness. This invariant closes that gap (SC-003a was previously unowned). **NATURAL RED today** (one monolithic `fast-tests-core-misc` shard collects the universe); GREEN post-split. Pin the relation over the parsed shard set, not a line number.

## Implementation Notes

- RED-first is a DoD anchor: run each new file on the planning base and RECORD the failing output. Any invariant that is green pre-WP03 is a defect (vacuous) — re-author with a fault-injection fixture until it bites.
- Pin behavioral relations, not line numbers. Where a relation needs a synthetic universe, keep the synthetic size out of the assertion's meaning (do not hard-code the real census count).

## Campsite cleaning (standing rule; ride the WP's normal review)

New files — write them clean from the start: `ruff --select ALL` exit 0, `mypy` Success, docstrings on every test, no `# noqa` unless individually justified. Do not touch files outside the eight owned.

## Definition of Done (non-fakeable — every anchor is recorded RED evidence)

- **Eight new files exist, `architectural`-marked, reds captured on WP01's tip** (census + `_gate_coverage` additive relations present, WP03 absent) — NOT the bare planning base. This makes the reds genuine topology-reds (edge present / monolith unsplit / dirs arch-blind), not missing-substrate `ImportError`/`FileNotFoundError` errors. Paste the failing output per file in the Activity Log (assertion/`AttributeError` iterating real census/model data — not a placeholder skip).
- **`test_arch_pole_deserialized` (FOLD 1) is a NATURAL red today**: the parsed arch/adversarial `needs` set still contains a fast-lane job (`fast-tests-core-misc`) because `if: always()` ≠ parallel; it flips green only when WP03 drops that edge (FR-013 de-serialized).
- **`test_shard_universe_bounded` (FOLD 3) is a NATURAL red today**: one monolithic shard collects the full catch-all universe; green only post-split (SC-003a).
- **`census.worklist == live_derived_worklist()` assertion is GREEN** in `test_ci_topology_worklist.py` (calls WP01's pure re-derivation function) — a stale/hand-trimmed census reds in CI (NFR-006 freshness-guard is a pytest-collected assertion, not pasted prose; closes the SC-001 vacuous-pass gaming).
- **Zero edits to any pre-existing test file** (`git diff --stat` shows only the eight new files).
- Each invariant proven to BITE: fault-injection red-negative recorded for NFR-003/FR-011/NFR-005 (relations that could pass vacuously). `test_arch_pole_deserialized` and `test_shard_universe_bounded` bite naturally (real topology reds, no fault-injection needed).
- `ruff` + `mypy` clean on the eight files.

## Risks / Reviewer Guidance

- Reject any vacuously-green invariant (passes on today's broken topology) — RED evidence is the gate.
- Reject a coverage-consumer test that intersects `slow-tests.needs` — the C-005 correction is explicit; it must assert the negative.
- Reject any edit to the existing suite — WP02 is new-files-only by contract.

## Activity Log

> Append at the END, chronological. Format: `- YYYY-MM-DDTHH:MM:SSZ – agent_id – <action>`

- 2026-07-04T21:00:00Z – system – Prompt created.
