---
work_package_id: WP01
title: Lane B — Identity scan arm + identity routing + canonicalizer floor
dependencies: []
requirement_refs:
- FR-004
- FR-005
- FR-007
- FR-010
- NFR-002
tracker_refs: []
planning_base_branch: mission/coord-read-residuals-2185-2186
merge_target_branch: mission/coord-read-residuals-2185-2186
branch_strategy: Planning artifacts for this mission were generated on mission/coord-read-residuals-2185-2186. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into mission/coord-read-residuals-2185-2186 unless the human explicitly redirects the landing branch.
subtasks:
- T001
- T002
- T003
- T004
- T005
- T006
- T007
- T008
phase: Phase 1 - Lane B (self-contained)
assignee: ''
agent: claude
history:
- at: '2026-06-26T19:00:00Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: python-pedro
authoritative_surface: tests/architectural/test_gate_read_literal_ban.py/
create_intent: []
execution_mode: code_change
model: ''
owned_files: []
role: implementer
tags: []
task_type: implement
---

# Work Package Prompt: WP01 – Lane B — Identity scan arm + identity routing + floor

## ⚡ Do This First: Load Agent Profile

Use the `/ad-hoc-profile-load` skill to load `python-pedro` (implementer) before parsing the rest of this prompt.

- **Profile**: `python-pedro`
- **Role**: `implementer`
- **Agent/tool**: `claude`

## Objectives & Success Criteria

- The dir-read gate gains a **`cli/commands/`-scoped identity-read arm** that flags `resolve_mission_identity(dir)` / `get_mission_type(dir)` whose `dir` is bound from a coord-aware resolver (`resolve_feature_dir_for_mission`/`candidate_feature_dir_for_mission`) without a primary fold — with a committed synthetic-AST non-vacuity self-test (pre-fix snippet flagged, routed snippet not).
- The #2186 identity sites route onto PRIMARY (`primary_feature_dir_for_mission` + `_canonicalize_primary_read_handle`, or `resolve_planning_read_dir`). **Arm + remediation co-land in this WP** (gate-unmask-cannot-self-validate).
- On a divergent coord fixture, lifecycle records carry the PRIMARY `mission_id` and `get_mission_type` returns the PRIMARY type.
- `ROUTED_CANONICALIZER_FLOOR` recomputed strictly-below the post-fix census (before/after recorded).

## Context & Constraints

- Spec [spec.md](../spec.md) (US2, US3, FR-004/005/007/010), [plan.md](../plan.md) IC-01/IC-05, [research.md](../research.md).
- **C-002**: consume the resolver seam; do not edit `_read_path_resolver` internals.
- **C-009-mirror**: touch only the OWNED `workflow.py` identity legs — never the implement-loop ROUTE legs. T003 produces the authoritative ownership table FIRST.
- **C-SEQ**: re-resolve `workflow.py`/`implement.py` citations against post-implement-loop-merge `main` (the sibling rewrites those functions). Lane B's arm is net-new, so this WP is otherwise not blocked on the sibling.

## Branch Strategy

- **Planning base branch**: `mission/coord-read-residuals-2185-2186`
- **Merge target branch**: `mission/coord-read-residuals-2185-2186`

## Subtasks & Detailed Guidance

### T001 – Identity-read scan arm
- **Files**: `tests/architectural/test_gate_read_literal_ban.py`. Add an `ast.Call` arm: match `resolve_mission_identity`/`get_mission_type` whose first arg is a Name bound (in the same function) from a coord-aware resolver and not passed through `_canonicalize_primary_read_handle`/`primary_feature_dir_for_mission`/`resolve_planning_read_dir`. Scope `cli/commands/` only.
### T002 – Non-vacuity self-test [P]
- Mandatory synthetic-AST self-test: a pre-fix snippet (coord-aware → identity read) is flagged; the routed snippet is not. Mirror the existing gate self-test pattern.
### T003 – ROUTE/KEEP ownership table
- Produce a definitive per-site table: every Lane B site → ROUTE / KEEP / owned-by-implement-loop, cross-checked against the sibling's ROUTE+KEEP list and re-resolved on merged main. No site left unaccounted.
### T004 – Route `next_cmd.py:187/:253`
- Primary-anchor the `resolve_mission_identity` reads so lifecycle `started`/`completed` records are written on coord topology (no silent swallow).
### T005 – Route `next_cmd.py:631`
- `get_mission_type` via primary fold → fixes wrong-run-type routing (`get_or_start_run`).
### T006 – Route `implement.py:1389` + owned `workflow.py` legs
- `implement.py:1389`: give it its OWN primary anchor (do not rely on the `:1018` fallback). `workflow.py:1274`/`:2732` are clean standalone anchors; `:1636` is a shared-variable site needing its own anchored variable (not a `feature_dir` re-point).
### T007 – Floor recompute
- Record before/after canonicalizer census; set `ROUTED_CANONICALIZER_FLOOR` strictly-below the post-fix live count in `test_resolution_authority_gates.py`.
### T008 – RED-first identity tests
- On the divergent coord fixture (sentinel husk meta ≠ PRIMARY), assert each routed site returns the PRIMARY id/type; revert → fails.

## Test Strategy

- Arm self-test (T002) + per-site RED-first tests (T008) on the divergent fixture. `ruff` + `mypy` clean.

## Risks & Mitigations

- Arm scope creep beyond `cli/commands/` → red-CI on strangers (sync/acceptance/policy). Keep it bounded.
- A site in the gap between the two missions → T003 table accounts for every site.

## Review Guidance

- Reviewer (`reviewer-renata`): verify the arm has teeth (self-test), the ownership table is complete, no implement-loop leg touched, floor strictly-below census.

## Activity Log

- 2026-06-26T19:00:00Z – system – Prompt created.
