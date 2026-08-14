# Implementation Plan: Mission-Artifact Write-Path Integrity

**Branch**: `mission/write-path-integrity` | **Date**: 2026-08-14 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `kitty-specs/write-path-integrity-01KZZD69/spec.md`

## Summary

Fix the coord/topology write-path cluster (#3371 P0, #2549, #3128, #3373; conditional #2570) by
installing fail-closed refusals at **two mandatory write chokepoints** rather than patching commands
one at a time:

- **Seam A — partition purity** at the shared write seam (`_run_planning_artifact_commit` /
  `commit_router._group_files_by_partition`): a batch that would route a PRIMARY kind to a coord ref (or
  a COORD kind to a lane ref) fails loud. This is where the P0 (#3371) and its mirror (#2549) are fixed.
- **Seam B — checkout-identity** at the true `implement`/`review` WP-write call sites (keyed on
  write-intent, not action-name): a WP write from a checkout that is not the mission's declared execution
  workspace is refused.

#3373 (unify the triplicated git-topology primitive) is the **substrate** and lands first, because
Seam B's path comparison is only sound with one symlink-canonicalization contract on both sides.

**Out of scope** (fixed during authoring): #3372 upgrade-wedge (shipped by mission #3383) and #2702
record-analysis (confirmed closed + guarded; ticket closed with evidence).

## Technical Context

**Language/Version**: Python 3.11+ (spec-kitty CLI internals).
**Primary Dependencies**: `typer`, `rich`, `ruamel.yaml`, git plumbing via `subprocess`; internal:
`mission_runtime` (resolution/artifacts), `specify_cli.coordination` (commit_router/coherence/
transaction), `specify_cli.lanes` (worktree_allocator), `specify_cli.cli.commands.implement`.
**Storage**: git (branches/worktrees; one object store shared across primary/coord/lane), `meta.json`,
`lanes.json`, `status.events.jsonl`.
**Testing**: `pytest` (unit + integration + `tests/architectural/` gates + real-git fixtures);
ATDD-first / red-first per charter; parallel `-n auto --dist loadfile`, real-port/daemon tests serial.
**Target Platform**: Linux/macOS dev + CI. **Project Type**: single (CLI library).
**Performance Goals**: Seam-B refusal is O(1) path comparison, zero extra git subprocesses (NFR-004).
**Constraints**: no topology redesign (#1878 non-goal); preserve coord-descent Assert A'
(ADR 2026-07-29-1); read from stored `meta.json`, no live re-derivation (ADR 2026-06-22-1);
`meta.json`/`target_branch` read from repository-root checkout (ADR 2026-06-24-2).
**Scale/Scope**: ~6 source modules + 4 probe call-sites; regression fixtures for the coord/PR-bound P0.

## Charter Check

*GATE: must pass before design; re-check after design.*

- **Single canonical authority / architectural alignment**: placement stays a **kind partition** (the two
  frozensets in `mission_runtime/artifacts.py`), routed via the existing seam — no new write-only
  resolver, no per-caller topology `if` (ADR 2026-06-24-1 C-006). ✅ Design routes through
  `_group_files_by_partition` / `_partition_files_for_commit`.
- **ATDD-first / red-first**: every FR gets a failing acceptance test first (the P0 reproduction, the
  cross-partition scan, the foreign-checkout refusal, the primitive-unification behavior parity). ✅
- **Architectural gate discipline**: a new `tests/architectural/` gate (FR-011) plus NFR-003 "no new
  arch-gate regressions vs merge-base". ✅
- **Terminology adherence**: Mission (not feature); no `feature*` aliases introduced. ✅
- **Tiered rigour**: P0 partition correctness is tier-1 (real-git integration proof); the primitive
  unification is behavior-preserving refactor (parity tests). ✅

No charter violations → Complexity Tracking not required.

## Project Structure

### Documentation (this mission)

```
kitty-specs/write-path-integrity-01KZZD69/
├── spec.md          # committed
├── plan.md          # this file
├── data-model.md    # entities: CommitTarget/partition, WorkspaceFragment fields, git-topology probe
├── quickstart.md    # repro of the coord/PR-bound P0 + the foreign-checkout refusal
├── contracts/       # partition-commit seam contract; checkout-identity refusal contract
└── tasks.md         # /spec-kitty.tasks output (not created here)
```

### Source Code (repository root — real paths touched)

```
src/specify_cli/cli/commands/
├── implement.py                 # FR-001 partition-aware auto-commit; FR-005 Seam-B refusal call site
├── implement_cores.py           # FR-005 swallow-site audit (except ActionContextError: return None :635)
└── agent/mission_record_analysis.py  # FR-005 swallow-site audit (:125, suppress(Exception) :347) [read-only]
src/specify_cli/coordination/
├── commit_router.py             # Seam A: _group_files_by_partition, PrimaryKindReachedCoordStagingError
├── coherence.py                 # is_self_bookkeeping_churn (single meta.json exemption authority)
└── transaction.py               # commit_idempotent (per-partition, skip-empty)
src/specify_cli/lanes/worktree_allocator.py   # FR-004: _merge_recorded_planning_commit conflict-free
src/specify_cli/tasks/…move_task…             # FR-003: route move-task --force through Seam A
src/mission_runtime/resolution.py             # build_execution_context; workspace_path; read_dir_for (#3373)
src/specify_cli/core/checkout_ownership.py    # #3373 probe consolidation (non-authoritative fast-path)
src/specify_cli/git/commit_helpers.py         # #3373 probe consolidation
src/specify_cli/workspace/context.py          # #3373 probe consolidation
src/charter/resolution.py                     # #3373 probe: canonical cached resolver (hot path — careful)

tests/
├── architectural/               # FR-011 Axis-B gate; NFR-003 baseline
├── integration/                 # coord + PR-bound P0 repro; foreign-checkout refusal (local fixture)
├── coordination/ lanes/ specify_cli/…        # unit + parity tests
```

**Structure Decision**: single-project CLI library; changes are surgical at named seams. No new
top-level packages. The git-topology primitive's new home is a small shared module consumed by the four
existing probe sites (exact module name decided in IC-01).

## Implementation Concern Map

> Concerns are NOT work packages. `/spec-kitty.tasks` translates these into executable WPs.

### IC-01 — Unify the git-topology primitive (substrate)

- **Purpose**: Collapse four semantically-distinct re-implementations of the git-common-dir/toplevel
  probe into one primitive with a single symlink-canonicalization contract, so Seam B's path comparison
  and the nested/toplevel classifier have one authority that cannot drift.
- **Relevant requirements**: FR-008, FR-009, FR-010; SC-005, SC-007, SC-008; C-005.
- **Affected surfaces**: `charter/resolution.py` (cached canonical resolver — **hot path**, ~20 callers;
  preserve caching + not-a-repo classification + `.git`-interior detection), `core/checkout_ownership.py`,
  `git/commit_helpers.py`, `workspace/context.py`; the `effective_root ? legacy : compose_meta_json_path`
  fork (~12×) in `mission_runtime/resolution.py` → one `read_dir_for(...)`.
- **Sequencing/depends-on**: none. **Substrate for IC-04.**
- **Risks**: the four probes answer different questions (root vs is-worktree vs linkage vs ownership) —
  unify the *primitive*, not the *semantics*; preserve each call site's contract. `charter/resolution.py`
  already `.resolve()`s — do not "add" canonicalization there, unify the contract. Behavior-parity tests
  (charter caching, not-a-repo, NESTED refusal) MUST stay green (SC-005).

### IC-02 — Partition-correct the P0 planning-artifact auto-commit (+ #2570 impact analysis)

- **Purpose**: Stop `implement.py`'s verbatim `placement_ref` arm from committing a mixed PRIMARY+COORD
  batch to one (coord) ref; route each file to its kind's partition; never construct an empty commit;
  recover a crash between the two commits by idempotent re-drive.
- **Relevant requirements**: FR-001, FR-004; NFR-001; SC-001, SC-002; C-004, C-006, C-008.
- **Affected surfaces**: `implement.py` (`_commit_planning_artifacts_transaction` :890-902,
  `_partition_files_for_commit` :714), `coordination/transaction.py` (`commit_idempotent`, skip-empty),
  `coordination/coherence.py` (`is_self_bookkeeping_churn` for `meta.json`), `lanes/worktree_allocator.py`
  (proves the add/add is gone). **#2570**: impact-analyze FR-001's commit-split on the allocator
  self-write timing; fold the #2570 fix only if mechanism-compatible + low-complexity, else follow-on.
- **Sequencing/depends-on**: IC-01 (shared partition/canonicalization).
- **Risks**: (R-D) `commit_idempotent` raises on an empty staged set — MUST skip-empty, order
  classify→exclude-self-bookkeeping→test-empty→commit-or-skip. (R-C) do NOT swap the write mechanism to
  `commit_for_mission` — keep `BookkeepingTransaction`, per-partition atomicity. (R-E/R6) `meta.json`
  co-travels coord writes — one predicate, applied before kind classification. Reverses the pinned
  `test_effective_destination_ref_is_placement_ref_verbatim` — rewrite it to assert the split (C-004).

### IC-03 — Seam-A partition guard on the write path + #2549 routing

- **Purpose**: Give `PrimaryKindReachedCoordStagingError` teeth at the planning-commit entry so a
  PRIMARY→coord or COORD→lane mis-route fails loud; route `move-task --force` through the same seam so
  `status.*` lands on coord (not the lane).
- **Relevant requirements**: FR-002, FR-003; NFR-001; SC-002, SC-006.
- **Affected surfaces**: `commit_router.py` (guard reach), `_run_planning_artifact_commit`,
  `tasks/…move_task…` (route #2549), `coherence.py` (self-bookkeeping exclusion).
- **Sequencing/depends-on**: IC-01, IC-02.
- **Risks**: the guard must classify staged *paths* by kind at commit time (the kind-agnostic
  `BookkeepingTransaction.commit` cannot) and exclude self-bookkeeping churn first, or it false-refuses a
  legitimate coord status commit carrying `meta.json`. Add a positive test (coord commit + `meta.json`
  succeeds). Respect withdrawn Trigger A (status→coord under coord topology is correct).

### IC-04 — Seam-B checkout-identity refusal for `implement`/`review`

- **Purpose**: Refuse a WP-execution write when the invoking checkout ≠ the mission's declared execution
  workspace, keyed on explicit write-intent (not action-name), without false-refusing reads or planning.
- **Relevant requirements**: FR-005; NFR-004; SC-004; C-001, C-007.
- **Affected surfaces**: `mission_runtime/resolution.py` (`workspace_path`; a write-intent signal from
  the true `implement`/`review` write sites), `implement.py`/`implement_cores.py` (call site + swallow
  audit :635), `mission_record_analysis.py` (swallow audit :125/:347 — read path, must stay unrefused).
- **Sequencing/depends-on**: IC-01 (symlink canonicalization, else `/var`→`/private/var` false-refusals).
- **Risks**: (R1) `resolve_action_context(action="tasks")` is a read vehicle (~20 callers) — key the
  refusal on WP-write intent, never action-name. (R3) planning runs from any checkout resolving to
  `primary_root` — compare against `primary_root` for planning, `workspace_path` for WP writes.
  (MF-4/R2) raise a distinct exception NOT subclassing `ActionContextError`; narrow the swallow sites or
  the refusal degrades to the legacy fallback silently. (MF-8) `resolve_ownership_claim` is
  repo-membership, not mission-identity — use the mission's own `workspace_path`, treat ownership-claim
  as a non-authoritative fast path.

### IC-05 — Architectural gates + regression pins

- **Purpose**: Make the P0 class un-reintroducible in CI and pin the crash-recovery + false-refusal
  invariants.
- **Relevant requirements**: FR-011; NFR-001, NFR-003; SC-006.
- **Affected surfaces**: `tests/architectural/` (static call-shape: every `_run_planning_artifact_commit`
  batch passes through `_partition_files_for_commit`; **negative**: no `lanes.json` on any coord ref),
  `tests/integration/` (repo scan SC-002; crash-between-commits pin R5).
- **Sequencing/depends-on**: IC-02, IC-03.
- **Risks**: a static AST gate cannot observe a runtime file-set — assign the runtime guarantee to the
  SC-002 repo scan; the static gate asserts the call-shape + the negative `lanes.json`-on-coord property.

## Design Decisions (key)

1. **Two seams, not one door** — verified: `build_execution_context` holds only a ref-only
   `placement_ref`, so per-file partition cannot live there. Partition → write seam; identity → WP-write.
2. **Reverse the C-004 verbatim deferral** — sanctioned by this mission; the pinned test is rewritten to
   assert the partition split, not deleted.
3. **Keep `BookkeepingTransaction`** for atomicity; per-partition commits via `commit_idempotent` with
   skip-empty; crash-recovery by idempotent re-drive (no cross-ref atomicity claim).
4. **One `meta.json` exemption predicate** (`is_self_bookkeeping_churn`) consumed by the guard, the split,
   and the SC-002 scan — applied before kind classification.
5. **Write-intent signal** for Seam B, threaded from the true `implement`/`review` write sites; planning
   and reads never carry it. Distinct refusal exception outside the `ActionContextError` hierarchy.

## Risks & Mitigations (carried from the adversarial review)

| Risk | Mitigation | Owner IC |
|------|------------|----------|
| Empty COORD group hard-fails (`commit_idempotent` raises) | skip-empty; classify→exclude→test-empty→commit-or-skip | IC-02 |
| Crash between the two commits strands coord residue on primary (#2702 shape) | idempotent re-drive; regression pin | IC-02/IC-05 |
| `meta.json` co-travel false-refused | single predicate before classification; positive test | IC-02/IC-03 |
| Seam B false-refuses reads / planning-from-lane | write-intent keying (not action-name); compare `primary_root` for planning | IC-04 |
| Refusal swallowed by `except ActionContextError`/`suppress` | distinct exception; narrow swallow sites | IC-04 |
| `resolve_ownership_claim` classifies foreign same-repo lane as OWNED | compare mission's own `workspace_path` | IC-04 |
| Symlink false-refusal (`/var`→`/private/var`) | IC-01 lands first; one canonicalization contract | IC-01→IC-04 |
| Charter hot-path resolver regressions | behavior-parity tests; unify primitive not semantics | IC-01 |

## Test Strategy (ATDD, red-first)

- **P0 acceptance (SC-001)**: an integration test that reproduces the coord + PR-bound `--start-branch`
  mission through finalize + `implement WP01`, asserting no `PlanningCommitMergeConflictError` and clean
  `git status --porcelain`. Written RED first against current code (reproduces `c3d92a364`'s add/add).
- **Cross-partition scan (SC-002/NFR-001)**: a real-git lifecycle fixture asserting zero PRIMARY files on
  coord and zero COORD files on lane (`meta.json` excluded), across `implement` and `move-task --force`.
- **Foreign-checkout refusal (SC-004)**: local two-mission fixture; assert refuse from foreign lane,
  proceed from own lane, proceed for planning-from-root and pure reads. No `spec-kitty-saas` dependency.
- **Primitive parity (SC-005)**: the existing charter-caching / not-a-repo / NESTED-refusal suite stays
  green after unification; add the one-copy static gates (SC-007/SC-008).
- **Arch gate (FR-011/SC-006)**: static call-shape + negative `lanes.json`-on-coord.
- **Guardrail**: run `pytest tests/architectural/test_no_legacy_terminology.py` before push (doctrine/
  prose touch); full `tests/architectural/` via CI. Baseline-red gotcha honored (attribute failures to
  merge-base before treating as ours).
