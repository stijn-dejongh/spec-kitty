# Research: Worktree-Aware Root Resolution & Verdict Parity

Phase 0 output. Each decision is grounded against `upstream/main` (`31798b6bd9`) via a code-anchor verification pass (2026-08-18). No new dependencies are introduced (see Supply-Chain note), so this file focuses on root-cause decisions and the already-fixed grounding.

## Decision 1 — Single checkout-kind classifier owns the primary/worktree/clone distinction

**Decision**: Add one classifier (`CheckoutKind`) and route the four resolver functions through it, rather than patching each independently.

**Rationale (verified)**: The clone-vs-primary mis-classification is isolated but **mirrored in four places**, all of which treat *any* `.git` directory as a valid primary:
- `resolve_canonical_root` — `core/paths.py:392`, **rule 1 at `:428-430`**: *"`.git` is a directory: this is a regular repo (or the main repo of a worktree set); return that ancestor."* Nothing checks whether it is a *secondary* clone.
- `find_repo_root` — `task_utils/support.py:45` → `locate_project_root` then `get_main_repo_root` (`:63-65`); re-anchors a worktree to primary and treats any `.git` dir as main.
- `locate_project_root` — real definition at `core/paths.py:182` (Tier 1 `SPECIFY_REPO_ROOT` env override at `:224`; Tier 2 ancestor-walk `:233-265` gated only on `.kittify` presence). Two secondary wrappers exist (`__init__.py:67`, `core/project_resolver.py:8`).
- `is_worktree_context` — `core/paths.py:281` (used by `mission_creation.py:483`): the **good** guard, but it returns `False` for a bare clone (`.git` is a dir → `break`, not a worktree). So `specify` refuses worktrees but **not clones**.

Centralizing the distinction (single canonical authority, charter) is cheaper and safer than four parallel patches that would drift.

**Alternatives considered**: (a) Patch each resolver inline — rejected: guarantees drift, violates single-authority. (b) Environment-variable override only (`SPECIFY_REPO_ROOT`) — rejected: does not fix the default path and is not discoverable by operators.

## Decision 2 — Write-target resolution mirrors `is_worktree_context`, extended to clones

**Decision**: Writing commands consume a write-target resolver that either writes into the invoking checkout or refuses **naming the path**. Generalize the existing `is_worktree_context` refusal pattern (already proven in `mission_creation.py:483`) to also cover standalone clones.

**Rationale (verified)**: `intake._resolve_repo_root` (`intake.py:57/60`) returns `find_repo_root(Path.cwd())` and is consumed at `:187` — so intake re-anchors to primary and writes the shared **untracked** slot there (brief §4; slots gitignored at `.gitignore:204-205`, so C-003 reframes the hazard as a shared-slot clobber, not tracked-diff). The refusal message must name the target path (NFR-003), matching the message `specify` already emits.

**Alternatives considered**: Silent write-into-invoking-checkout with no refusal option — rejected for `intake --force` against a shared slot without an identity check (FR-002 requires the identity check).

## Decision 3 — Hoist `_parse_review_result_json` + the `for_review` gate into a shared, topology-aware seam

**Decision**: Move the verdict parser and the commit-gate to a shared location consumed by both `agent status emit` and `orchestrator-api transition`; make the gate topology-aware.

**Rationale (verified)**:
- `orchestrator_api/commands.py`: `_parse_review_result_json` at `:1297` (called `:1399`); `_enforce_for_review_commit_gate` at `:1257` (called `:1413`) **uses `predict_lane_worktree`** (`:1281`) — which fails a clone on topology rather than commit state (FR-011).
- `cli/commands/agent/status.py`: `emit` params `:223-264` have **no `--review-result-json`**; `TransitionRequest` (`:317-332`) is built **without** `review_result`; the misleading `--help` example (`:274`) routes a verdict into `--evidence-json`, never into the `review_result` slot (FR-010, FR-012).
- `#1734` (in_review→approved guard) shares this root: both surfaces lack a `ReviewResult` path — the #3547 parity fix *is* the #1734 fix.

**Alternatives considered**: Add `--review-result-json` to `emit` with a *copy* of the parser — rejected: two validators drift (violates single-authority; the whole point of parity is identical validation).

## Decision 4 — Audit registration + round-trip, but NOT projection or destruction (already fixed)

**Decision**: Register `review_result` in the shape registry, add a round-trip property test, and de-tautologize the drift test. Do **not** touch the reducer projection or the repair row preservation.

**Rationale (verified)**:
- Reducer projection **already implemented** — `status/reducer.py:210-215` (last-wins + carry-forward; verdict-lookup helpers at `:557`, `:595`). **C-001: do not re-implement.**
- Repair preservation **already fixed** — `migration/mission_state.py:1879` `_build_canonical_row` keeps `review_result` (flagged as a hard FSM guard input). **C-002: no destruction fix.**
- Residual is real: `audit/shape_registry.py` `status_event_row` (`:90-111`) frozenset does **not** include `review_result` → `UNKNOWN_SHAPE` INFO noise (FR-014). The drift test `tests/audit/test_shape_registry_writer_parity.py` asserts only that writer keys are a **subset** of registered keys — a tautology that cannot catch a *persisted-but-unregistered* shape (FR-016).
- Coordination-key shape is `META_COORDINATION_KEYS` (`shape_registry.py:53`); the writer migration (FR-018) is its own WP (C-004).

## Decision 5 — Repair clone re-anchor is `_anchor_repair_root`

**Decision**: Make `_anchor_repair_root` clone-aware so `doctor mission-state --fix` in a clone rewrites the clone (or refuses), and make the repair manifest enumerate every field it touches.

**Rationale (verified)**: `_anchor_repair_root` at `migration/mission_state.py:504` re-anchors via `resolve_canonical_root(repo_root)` (`:532`), called from `repair_repo`/audit (`:547`, `:738`). This is the spine's clone re-anchor inside the repair path (FR-009). Manifest honesty is additive.

## Decision 6 — Review-cycle write-side kind-flip; `resolve_review_verdict_facts` is elsewhere

**Decision**: Flip the `review/cycle.py` write-side default off `WORK_PACKAGE_TASK`; migrate the verdict-facts resolver and re-verify the rehome test.

**Rationale (verified + correction to brief)**: `_review_cycle_wp_dir` (`review/cycle.py:71`) defaults `kind=WORK_PACKAGE_TASK` (`:76`); the `REVIEW_CYCLE` branch (`:179-197`) still falls back to `WORK_PACKAGE_TASK` read. **Correction:** `resolve_review_verdict_facts` lives at `cli/commands/agent/tasks_verdict_persistence.py:404`, **not** in `review/cycle.py` (the brief located it loosely). The rehome test to re-verify is `test_analysis_report_rehome` (FR-017, #3563).

## Supply-Chain Security & Adversarial Evidence

**Dependency posture**: This mission adds/upgrades/removes **no** dependencies — it is an internal-resolver + CLI-parity fix. Registry-authenticity / freshness / lifecycle-script / Node-LTS checks are therefore **N/A by inspection**, not skipped silently (per `051-supply-chain-install-safety`). If any WP later pulls a new import, that WP re-runs this check.

**Adversarial evidence**: No security-impacting dependency decision is made, so no adversarial-squad challenge on dependencies is required at plan time. A post-plan adversarial squad still runs against the *design* (scope leakage, missed re-anchor sites, verdict-parity gaps) per the mission workflow; its dispositions will be recorded here if any finding is contested.

## Confirmed anchor table (for the tasks phase)

| Concern | Anchor (verified) | FR |
|--------|-------------------|-----|
| Clone mis-classification | `core/paths.py:428-430` (rule 1) + mirrors in `support.py:45`, `paths.py:182`, `paths.py:281` | FR-001 |
| intake write target | `intake.py:57/60/187` | FR-002 |
| doctor tool-surfaces --fix | `_command_surface_doctor.py:755/776`, `tool_surface/repair.py` | FR-003 |
| doctor mission-state --fix | `_mission_state_doctor.py:~227/261` → `repair_repo` | FR-004, FR-009 |
| backfill-runtime-state | `migrate_cmd.py`, `migration/backfill_runtime_state.py` | FR-005 |
| setup-plan branch | `agent/mission_setup_plan.py:169`, `mission_branch_context.py` | FR-006 |
| --owned-checkout | `agent/mission_create.py` → `mission_creation.py:482-508` | FR-007 |
| .kittify containment | `core/paths.py` rule 3 (`:433-444`) | FR-008 |
| repair clone re-anchor | `migration/mission_state.py:504/532`; manifest in `_build_canonical_row:1858-1879` | FR-009 |
| emit --review-result-json | `cli/commands/agent/status.py:223-264/274/317-332` | FR-010, FR-012 |
| shared gate + parser | `orchestrator_api/commands.py:1257/1281/1297/1399/1413` | FR-011, FR-013 |
| shape registry | `audit/shape_registry.py:90-111` (row), `:53` (coord keys) | FR-014, FR-016 |
| round-trip test | new test against `status/reducer.py` replay | FR-015 |
| coordination-key writer | writer of `META_COORDINATION_KEYS` rows | FR-018 |
| review-cycle kind-flip | `review/cycle.py:71/76/179-197`; facts at `tasks_verdict_persistence.py:404` | FR-017 |

## Existing tests to extend (not duplicate)

`tests/unit/workspace/test_root_resolver.py`, `tests/contract/test_canonical_root_when_in_worktree.py`, `tests/integration/migration/test_audit_primary_anchor.py`, `tests/integration/test_sc008_topology_resolution.py`, `tests/coordination/test_verdict_dir_co_resolution.py`, `tests/audit/test_shape_registry_writer_parity.py`, `tests/core/test_mission_creation_topology.py`.
