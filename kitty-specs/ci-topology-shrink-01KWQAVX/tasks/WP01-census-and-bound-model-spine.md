---
work_package_id: WP01
title: 'Census + bound-model spine: construction-derived worklist + additive _gate_coverage relations'
dependencies: []
requirement_refs:
- FR-001
- NFR-001
- NFR-002
- NFR-003
- NFR-006
- C-001
tracker_refs: []
planning_base_branch: main
merge_target_branch: main
branch_strategy: Planning artifacts for this mission were generated on main. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into main unless the human explicitly redirects the landing branch.
base_branch: kitty/mission-ci-topology-shrink-01KWQAVX
base_commit: aa998ede7e31927286e78e7819757e03c2f2c604
created_at: '2026-07-04T21:00:00+00:00'
subtasks:
- T001
- T002
- T003
phase: Phase 1 - Spine
assignee: ''
agent: ''
history:
- at: '2026-07-04T21:00:00Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: python-pedro
authoritative_surface: tests/architectural/_gate_coverage.py
create_intent:
- tests/architectural/ci_topology_census.json
execution_mode: code_change
model: ''
owned_files:
- tests/architectural/_gate_coverage.py
- tests/architectural/ci_topology_census.json
role: implementer
tags: []
task_type: implement
---

# Work Package Prompt: WP01 – Census + bound-model spine

## ⚡ Do This First: Load Agent Profile

Use the `/ad-hoc-profile-load` skill to load the agent profile specified in the frontmatter (or any user-defined profile), and behave according to its guidance before parsing the rest of this prompt.

- **Profile**: `python-pedro`
- **Role**: `implementer`

---

## ⚠️ IMPORTANT: Review Feedback

Check the `review_ref` field in the event log before starting; address all feedback.

---

## Objectives & Success Criteria

Two enablers everything downstream stacks on (C-001 additive — consume the bound `_gate_coverage` model, never rebuild the marker→job substrate):

1. **NFR-006 census (the critical deliverable)**: commit `ci-topology-census.json` as the construction-derived worklist authority WP02's SC-001 test iterates — with a **freshness-guard** so a stale hand-edit reds. The metric must measure coverage, NOT the implementer's constant.
2. **IC-04 parse extension**: extend `tests/architectural/_gate_coverage.py` ADDITIVELY with every parsed relation WP02 consumes (differential-matrix per dir; same-tier per test; always-on arch-job recognition). This file is a single-owner spine: after this WP it is **READ-ONLY** for the rest of the mission (Wave-2 spine lesson).

## Subtasks & Detailed Guidance

### Subtask T001 – Construction-derived census artifact + freshness-guard
Re-derive the census LIVE (do NOT hand-copy research.md numbers — research is a snapshot; the tree may have moved). Reproduce the research §1.1 command:
```bash
for d in src/specify_cli/*/; do
  n=$(find "$d" -name '*.py' | xargs wc -l 2>/dev/null | tail -1 | awk '{print $1}')
  echo "$n $d"
done | sort -rn
```
Write `tests/architectural/ci_topology_census.json` per data-model.md:
- `t_loc` (int, committed constant — recommended 500; the plan-time floor, NEVER a literal in the WP02 test).
- `rule` (str): `D ∈ worklist ⟺` direct child of `src/specify_cli/` ∧ `sum(LOC *.py under D) ≥ t_loc` ∧ no src-backed dorny group globs `src/specify_cli/<D>/**`.
- `worklist[]`: each `{ dir, loc, cone_roots[], target_group, target_shard }`.
- `mapped_dirs[]`: the already-mapped dirs (the negative-assertion oracle, research §1.2).
- `arch_blind_groups[]`: the 13 Mode-B groups (un-blind targets, research §1.4B).
- `timings_baseline`: `{ fast_core_misc_min, arch_shard_min, critical_path_min, next_lane_min, source_run_id }` (NFR-001 — the 29.4-min baseline; cite the live run id).
- **Freshness-guard**: implement the guard so WP02 (or a self-check in `_gate_coverage.py`) can re-derive the worklist from the LIVE tree and assert `frozen_worklist == live_derived_worklist`. A stale census MUST red. (Either a `--verify-census` mode on the module CLI, or a documented pure function the WP02 test calls — pick the seam that keeps the assertion in WP02's test file, not this module.)

### Subtask T002 – Additive `_gate_coverage.py` parse extensions (additive only)
Read `_gate_coverage.py` end-to-end first (the #2368 mission already extended it with `WorkflowModel`, `filter_groups`, `job_needs`, `job_gating_groups`, `cov_targets`, `diff_cover_critical_paths`). Extend ADDITIVELY (new functions / dataclass fields; do NOT change existing behavior — every existing consumer test must pass untouched):
- **Differential-matrix relation (NFR-002)**: `{ dir → arch_selected: bool }` over every `src/specify_cli/*` dir. Arch-selected iff the dir's touch selects the arch/adversarial suite. With WP03's always-on arch job (no src path filter) every dir is selected by construction; this relation is what proves the job stays unconditional (a regression re-adding a filter-group gate to it reds NFR-002).
- **Same-tier uniqueness relation (NFR-003)**: `{ test → count_fast_shards, count_integration_shards }` over the parsed `Gate` list. Distinct from the existing report-only cross-tier duplicate count (3550).
- **Always-on arch-job recognition**: recognize a group-less `if: always()` suite job (like `lint`) as legitimately absent from `JOB_GROUPS`/`src_backed_groups` — so it does not perturb the FR-010 relations (research §4.2).
Keep it PURE parsing — NO assertions in this module (the invariants live in WP02's test files). Docstring each new surface with the FR/NFR it serves.

### Subtask T003 – Gates
- `PWHEADLESS=1 uv run pytest tests/architectural/test_gate_coverage.py tests/architectural/test_src_filter_coverage.py tests/architectural/test_workflow_coherence.py tests/architectural/test_marker_job_completeness.py -q` — all existing consumers green, UNTOUCHED (`git diff --stat` shows only `_gate_coverage.py` + the census json).
- A self-check script exercising each new parse surface against the LIVE workflows; paste the outputs (worklist size, arch-blind group count, the 8-marker routed set, needs-map sizes, the differential-matrix arch-blind count on TODAY's topology — expected 13) into the Activity Log. **These recorded counts are WP02/WP03's ground truth.**
- Diff-scoped `ruff check` exit 0; `uv run mypy` on the touched file stays Success.

## Campsite cleaning (standing rule; ride the WP's normal review)

Sonar: verify zero open issues in `_gate_coverage.py` before landing. Run a local `ruff --select ALL` census on the touched surface and clear auto-fixables in one `ruff check --fix` pass (SAFE only — no behavior change). Adjudicate anything load-bearing OUT with an inline rationale. Do NOT expand scope beyond the two owned files.

## Definition of Done (non-fakeable — every anchor is a green test or parsed assertion)

- **Census freshness-guard green**: a live re-derivation equals the committed `worklist[]` (a stale census reds). Recorded live self-check output pasted in the Activity Log.
- **Additive relations exist and parse**: differential-matrix returns 13 arch-blind on today's topology (the pre-WP03 red baseline); same-tier relation returns per-test shard counts; always-on-arch recognition returns the current group-less always-on jobs. All exercised by the self-check, counts recorded.
- **Existing consumers untouched-green**: the four listed consumer suites pass with zero edits to them (`git diff --stat` proves only `_gate_coverage.py` + census changed).
- `ruff` + `mypy` clean on the diff.

## Risks / Reviewer Guidance

- The census must be construction-derived: reject any hand-picked worklist — the freshness-guard is the teeth (NFR-006).
- Reject any change to existing parse behavior (additive-only by contract). Any downstream discrepancy in a recorded count is WP01 feedback (re-open), NOT a downstream workaround — the cross-check is explicit.

## Activity Log

> Append at the END, chronological. Format: `- YYYY-MM-DDTHH:MM:SSZ – agent_id – <action>`

- 2026-07-04T21:00:00Z – system – Prompt created.
