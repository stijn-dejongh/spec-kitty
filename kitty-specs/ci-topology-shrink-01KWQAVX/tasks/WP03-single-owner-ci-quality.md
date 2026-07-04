---
work_package_id: WP03
title: 'Single-owner ci-quality.yml surgery: composite groups, fast-matrix split, always-on de-serialized arch pole, needs-lists'
dependencies:
- WP02
requirement_refs:
- FR-002
- FR-003
- FR-004
- FR-005
- FR-006
- FR-007
- FR-009
- FR-010
- FR-011
- FR-012
- FR-013
- NFR-004
- C-002
- C-003
tracker_refs:
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
- T007
- T008
- T009
- T010
- T011
phase: Phase 3 - Workflow surgery
assignee: ''
agent: ''
history:
- at: '2026-07-04T21:00:00Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: python-pedro
authoritative_surface: .github/workflows/ci-quality.yml
create_intent: []
execution_mode: code_change
model: ''
owned_files:
- .github/workflows/ci-quality.yml
role: implementer
tags: []
task_type: implement
---

# Work Package Prompt: WP03 – Single-owner `ci-quality.yml` surgery

## ⚡ Do This First: Load Agent Profile

Use the `/ad-hoc-profile-load` skill to load the agent profile specified in the frontmatter (or any user-defined profile), and behave according to its guidance before parsing the rest of this prompt.

- **Profile**: `python-pedro`
- **Role**: `implementer`

---

## ⚠️ IMPORTANT: Review Feedback

Check the `review_ref` field in the event log before starting; address all feedback.

---

## Objectives & Success Criteria

You are the **SOLE owner** of `.github/workflows/ci-quality.yml` (C-003 — a `lanes` allocator rejects overlapping `owned_files`; per-slice WPs cannot co-own this file, so ALL topology edits land here). Turn WP02's six RED invariants GREEN while keeping the 8 #2368 WP04 invariants green throughout (NFR-007). This is the fat WP — inherent to C-003.

The load-bearing insight (all 3 post-spec lenses): **un-blind (US2) and wallclock (US3) are the SAME arch-pole move (FR-013)** — de-serializing the arch shard from `fast-tests-core-misc` moves its tail 29.4→12.3 min AND runs it on 100% of PRs. Realize it as an **always-on arch job that adds NO filter group** (Option A) so the FR-010 parsed relations stay untouched (C-001 additive).

## Subtasks & Detailed Guidance

### Subtask T007 – Composite filter groups + 5-edit surfaces 1-3 (FR-001/002/010)
For each census worklist dir, register it into a **composite** src-backed filter group (FR-010 caps job-count under the NFR-005 ceiling; the research §3 design proposes `auth_audit_git`, `lifecycle`, `agent_surface`, `closeout`, `governance`, `platform` — WP01's census is the authoritative member map). Land the 5-edit atomic registration surfaces 1-3 per group IN ONE COMMIT (research §4.4):
1. dorny `filters:` block — group + `src/specify_cli/<members>/**` globs.
2. `changes.outputs.<group>` row — the exact `(run_all || …unmatched…) && 'true' || …filter…` shape.
3. `unmatched` enumeration loop (`:309-329`) — add `"${{ steps.filter.outputs.<group> }}"`.
Keep FR-010c enumeration (`test_unmatched_refs_equal_parsed_filter_groups_live`) and FR-010 boolean (`test_unmatched_boolean_semantics`) green.

### Subtask T008 – Fast-matrix split + ignore mirror + nested roots (FR-003/004/012)
- Subdivide `fast-tests-core-misc` (`:1321-1376`) into a focused matrix mirroring the `integration-tests-core-misc` shards (FR-003). Each shard owns coherent, non-overlapping test roots (NFR-003).
- Update the `fast-tests-core-misc` `--ignore` mirror in LOCKSTEP with every carve (FR-012 invariant `test_catch_all_ignore_lists_mirror_owned_roots_live`) — carve a shard ⇒ add `--ignore=tests/<root>` AND give the root a positional home, together.
- Update the integration-matrix `ignore_args` for nested `tests/specify_cli/<D>` roots (orchestrator_api, bulk_edit) by hand (FR-004 — NOT covered by FR-012's whole-tree check).
- Consolidate the `migration` double-root (`tests/migration` + `tests/specify_cli/migration`) into ONE home preserving `and not slow` (the `@slow` perf test runs only in `slow-tests`) (FR-012).
- Carve `dossier` (globbed in core_misc but in NO integration shard — fixes a latent hole).

### Subtask T009 – Always-on de-serialized arch pole (FR-005/006/013/011/009)
- Extract the `architectural` matrix shard (`tests/adversarial tests/architectural tests/architecture tests/lint`, marker `not windows_ci and (git_repo or integration or architectural)`) into a STANDALONE job (proposed `arch-adversarial`).
- `if: always()` (like `lint`) — unconditional, references NO dorny filter output → it does NOT enter `JOB_GROUPS`, `src_backed_groups`, or the `unmatched` loop → FR-010/FR-011 relations untouched (C-001). **CRITICAL**: the job must carry NO filter-group `if:` or it perturbs `src_backed_groups` and reds FR-010 + NFR-002.
- Drop `needs: fast-tests-core-misc` (`:1433`) — de-serialize (FR-013). Arch tail ≈12.3 min from t=0.
- Emit `coverage-*.xml` under the glob-consumed name so the aggregator wildcard download picks it up (FR-006).
- Preserve `-n0` serial passes + `--dist loadfile` + per-worker HOME isolation on every new shard (FR-011). Preserve the fail-closed catch-all so an unmapped/new src path still forces coverage and nightly `run_all` still over-covers (FR-009).

### Subtask T010 – JOB_GROUPS heredoc + all needs-lists (FR-002 surfaces 4-5, FR-007, C-005, C-002)
- 5-edit surfaces 4-5 per group: wire each group into ≥1 test-job `if:` and add its `JOB_GROUPS` heredoc row (`:3219-3258`) — keep `test_job_groups_table_equals_parsed_if_gating_live` green.
- Register every new test job (incl. `arch-adversarial`) into `quality-gate.needs`, `sonarcloud.needs` (`:2517-2552`), `diff-coverage.needs` (`:2370-2387`), and `mutation-testing.needs` (`:2485-2503`, `if: false` but parsed) — per FR-007 + C-005.
- **NEVER** add integration/arch jobs to `slow-tests.needs` (`:2152-2168`, fast-jobs-only — would red on arrival). This is the sharpest latent hazard (research §4.5).
- Every derived surface stays asserted-against-parsed-source (C-002 / Decision 8) — no hand-added surface beside the model.

### Subtask T011 – Gates + probe evidence
- WP02's six invariants flip RED→GREEN: `test_ci_topology_worklist`, `test_arch_unblind_matrix`, `test_same_tier_uniqueness`, `test_coverage_consumer_needs`, `test_serial_port_preservation`, `test_job_count_ceiling`.
- The 8 #2368 invariants stay green: `PWHEADLESS=1 uv run pytest tests/architectural/test_src_filter_coverage.py tests/architectural/test_workflow_coherence.py tests/architectural/test_marker_job_completeness.py tests/architectural/test_gate_coverage.py -q`.
- `_gate_coverage` orphan count stays 0, total `run_all` selected count unchanged (SC-004).
- A probe PR per representative slice (e.g. touch only `src/specify_cli/auth/**`) demonstrates focused routing + always-on gates and NO full-matrix run (SC-006). Paste probe evidence in the Activity Log.

## Campsite cleaning (standing rule; ride the WP's normal review)

`ci-quality.yml` is YAML, not Python — Sonar/ruff campsite is N/A here, but keep the file coherent: no orphaned anchors, no dead filter globs (`test_every_filter_glob_is_live` covers this file). Do NOT expand scope to `ci-windows.yml` (WP04 owns it) or the baseline (WP06 owns it).

## Definition of Done (non-fakeable — every anchor is a green test)

- **WP02's six invariants GREEN** (recorded run output).
- **8 #2368 invariants GREEN** (recorded run output); orphan count 0, total selected unchanged.
- Each composite group's 5 surfaces landed atomically (FR-002) — no partial registration (a partial reds FR-010c/FR-011).
- The `arch-adversarial` job is always-on, group-less, de-serialized, and coverage-wired (NFR-002 asserts it selects 100% of dirs).
- Probe-PR evidence recorded: a single-area PR routes to its focused shard + always-on gates, not a full-matrix run (SC-006).

## Risks / Reviewer Guidance

- **C-003 topology**: if per-slice workflow edits become unavoidable, STOP and escalate to flatten the mission to `single_branch` with linearized shared-surface edits — do NOT split this file across lanes.
- The always-on arch job MUST carry no filter-group `if:` — reviewer verifies NFR-002 stays green (it proves the job stays unconditional).
- Reviewer confirms `slow-tests.needs` gained NO integration/arch job (C-005 correction).

## Activity Log

> Append at the END, chronological. Format: `- YYYY-MM-DDTHH:MM:SSZ – agent_id – <action>`

- 2026-07-04T21:00:00Z – system – Prompt created.
