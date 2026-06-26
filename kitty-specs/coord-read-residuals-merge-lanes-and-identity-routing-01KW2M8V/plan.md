# Implementation Plan: Coord-Read Residuals — Merge/Lanes Planning Reads + Identity-Read Routing

**Branch**: `mission/coord-read-residuals-2185-2186` | **Date**: 2026-06-26 | **Spec**: `kitty-specs/coord-read-residuals-merge-lanes-and-identity-routing-01KW2M8V/spec.md`
**Input**: Feature specification (#2185 Lane A + #2186 Lane B; children of epic #2160, siblings of #2115).

## Summary

Route the PRIMARY-partition reads that still resolve through coord-aware resolvers (landing on the empty `-coord` status husk after #2106) onto the existing read-path seam. **Lane A (#2185)**: ~10 sites in `merge/`, `lanes/`, `core/worktree_topology` reading `lanes.json`/`tasks/`/`meta.json` → `resolve_planning_read_dir(kind=...)`, with per-leg splits where one resolved dir feeds both a PRIMARY and a STATUS leg. **Lane B (#2186)**: command-layer identity/type reads (`next_cmd.py`, owned `workflow.py` legs, `implement.py:1389`) → `primary_feature_dir_for_mission` + `_canonicalize_primary_read_handle`, plus a **net-new command-layer identity-read scan arm** (the existing dir-read gate is structurally blind to function-call identity reads). The technical approach is **consume-not-author**: the resolver seam already exists and is in production use; this mission only re-points call sites and extends the gate. Lands after the implement-loop sibling (inherits its whole-`src` scanner widening + #2185 pin hand-off; re-resolves line citations against merged `main`).

## Technical Context

**Language/Version**: Python 3.11+ (CLI; `ruff` + `mypy` clean, McCabe complexity ≤ 15)
**Primary Dependencies**: the read-path resolver seam — `specify_cli.missions._read_path_resolver` (`resolve_planning_read_dir`, `primary_feature_dir_for_mission`, `_canonicalize_primary_read_handle`); `mission_runtime` partition authority (`MissionArtifactKind`, `is_primary_artifact_kind`); `typer`, `rich` (existing CLI stack). No new runtime dependency.
**Storage**: filesystem planning artifacts (`kitty-specs/<mission>/`: `meta.json`, `lanes.json`, `tasks/`, `status.events.jsonl`) across PRIMARY checkout vs. `-coord` git-worktree husk. No database.
**Testing**: `pytest`; architectural ratchet gates (`tests/architectural/test_gate_read_literal_ban.py`, `test_resolution_authority_gates.py`); real `git worktree` coord fixture (`tests/specify_cli/write_side/topology_fixtures.py::build_coord`, extended for husk-divergence per FR-009). Integration-over-stubs (NFR-004).
**Target Platform**: Linux / macOS / Windows CLI (loopback/local only; no network).
**Project Type**: single (library + CLI; `src/specify_cli/`).
**Performance Goals**: behavioral parity — read-routing only; no measurable runtime change. PRIMARY routing is a no-op on flat topology (NFR-003).
**Constraints**: STATUS-partition reads stay coord-aware (C-001); no silent fallback on ambiguous/coord-deleted handles (C-002, #1848); consume the resolver, never edit its internals (C-002); surface exclusivity vs. the implement-loop ROUTE surface (C-009-mirror); `scripts/tasks/` legacy reader untouched (C-EXCL-2167); does not remove the `implement.py:1018` fallback (C-EXCL-FALLBACK); lands after the implement-loop sibling (C-SEQ).
**Scale/Scope**: Lane A ≈ 10 sites (3 mixed PRIMARY+STATUS needing per-leg split) + 1 coord-topology integration test; Lane B ≈ 6 command-layer identity sites + 1 net-new gate arm (with synthetic-AST non-vacuity self-test) + floor recompute. Estimated 5–7 WPs.

## Charter Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Integration-over-stubs (NFR-004)**: the #2185 acceptance proof drives real code against a real `git worktree` coord fixture with a **divergent** husk — PASS by design (FR-009). Unit stubs handing in a primary dir are explicitly disallowed.
- **Gate-can't-self-validate**: the net-new identity arm (Lane B) and its remediation co-land in this mission, validated by a pre-merge full-gate dry run + a committed synthetic-AST non-vacuity self-test — PASS (US3/FR-007/FR-008).
- **Terminology canon**: prose uses "Mission"; no `feature*` aliases on active domain objects — PASS.
- **Sonar/complexity**: read-routing edits keep touched functions ≤ 15; per-leg split extractions get focused tests — PASS by constraint.
- **Realistic test data**: the coord fixture seeds production-shaped `lanes.json`/`tasks/`/`meta.json` (real ULIDs, real WP ids) — PASS (FR-009).
- **Canonical sources**: consumes the documented resolver seam; no improvised path reconstruction — PASS (C-002).

No charter violations requiring Complexity Tracking.

## Project Structure

### Documentation (this mission)

```
kitty-specs/coord-read-residuals-merge-lanes-and-identity-routing-01KW2M8V/
├── spec.md              # committed (revised post-squad)
├── issue-matrix.md      # committed (#2185/#2186 in-mission)
├── plan.md              # this file
├── research.md          # Phase 0 (3-agent code-state research, summarized below)
├── data-model.md        # Phase 1 — the artifact-kind partition + per-site route table
├── contracts/           # Phase 1 — resolver-consumption contract + identity-arm contract
└── tasks.md             # Phase 2 (/spec-kitty.tasks)
```

### Source Code (repository root)

```
src/specify_cli/
├── merge/                  # Lane A: forecast.py, executor.py (mixed), resolve.py, done_bookkeeping.py (mixed)
├── lanes/                  # Lane A: merge.py, recovery.py (mixed:356), worktree_allocator.py
├── core/worktree_topology.py   # Lane A: single swap co-resolves 3 PRIMARY legs
├── cli/commands/
│   ├── merge.py            # Lane A: :269 meta.json
│   ├── next_cmd.py         # Lane B: :187/:253/:631 identity/type
│   ├── implement.py        # Lane B: :1389 (shared-variable, own anchor)
│   └── agent/workflow.py   # Lane B: owned identity legs ONLY (re-resolve vs merged main)
└── missions/_read_path_resolver.py   # CONSUMED ONLY — not edited (C-002)

tests/
├── architectural/test_gate_read_literal_ban.py        # FR-006 verify + FR-007 new identity arm
├── architectural/test_resolution_authority_gates.py   # FR-010 floor recompute
├── integration/  (merge coord-topology test, FR-009)
└── specify_cli/write_side/topology_fixtures.py        # extend build_coord (divergent husk)
```

**Structure Decision**: single project. Edits are confined to the owned surfaces above; the resolver seam and the implement-loop ROUTE surface (`tasks.py`, `workflow.py` route legs, `tasks_dependency_graph.py`, `workspace/context.py`, …) are out of scope (C-009-mirror).

## Phase 0 — Research (summary; full findings in research.md)

Three independent code-state agents verified against `main`:
- **Kind corrections confirmed**: 6 of 10 #2185 issue labels are wrong (3 sites read `meta.json` not LANE_STATE; 1 reads `lanes.json` not `tasks/`); `executor`/`done_bookkeeping`/`recovery:356` are mixed PRIMARY+STATUS (debugger fully traced `executor.py` `feature_dir`→`run.feature_dir`→`status_feature_dir` at `:503`/`:560`). Route by real partition.
- **Husk failure mode real**: `meta.json`/`lanes.json`/`tasks/` are PRIMARY-only; `next_cmd.py:187/253` swallow `FileNotFoundError` (silent drop); `:631` falls back to default `software-dev` type (wrong-routing).
- **Gate blindness confirmed**: scanner matches only `resolver / "tasks"|"lanes.json"|"*.md"` joins; identity reads (function-call shape) escape both arms → new arm needed.
- **#2115 sequencing**: `implement.py:1389` is correct only via the `:1018` fallback; guards must precede fallback removal (C-EXCL-FALLBACK).

## Implementation Concern Map

> Concerns are NOT work packages. `/spec-kitty.tasks` translates these into WPs.

### IC-01 — Foundational gate: identity-read arm + floor

- **Purpose**: Build the command-layer (`cli/commands/`-scoped) identity-read scan arm with a synthetic-AST non-vacuity self-test, and recompute `ROUTED_CANONICALIZER_FLOOR`. This is the detector that makes Lane B observable and ratchet-enforced; both Lane B routing and the floor depend on it.
- **Relevant requirements**: FR-006 (verify inherited scope), FR-007, FR-010, FR-011 (pin-presence preflight).
- **Affected surfaces**: `tests/architectural/test_gate_read_literal_ban.py`, `test_resolution_authority_gates.py`.
- **Sequencing/depends-on**: none (foundational). Mirrors the sibling's dedicated gate WP to avoid a shared-ratchet-file merge race; all routing concerns drain pins against this.
- **Risks**: arm scope creep beyond `cli/commands/` would red-CI on out-of-scope strangers (sync/acceptance/policy) — bound it. Gate-can't-self-validate → pair with a pre-merge full-gate dry run.

### IC-02 — Lane A: merge cluster routing

- **Purpose**: Route the `merge/` PRIMARY reads by real kind, splitting the mixed sites per-leg (STATUS stays coord-aware), and drain the matching #2185 pins.
- **Relevant requirements**: FR-001, FR-002, FR-003, FR-008.
- **Affected surfaces**: `merge/forecast.py` (`:153`+`:159`), `merge/executor.py` (mixed split), `merge/resolve.py` (`:98` PRIMARY_METADATA), `merge/done_bookkeeping.py` (`:237` WP-path leg + comment removal, keep status-transactional legs on primary), `cli/commands/merge.py` (`:269`).
- **Sequencing/depends-on**: IC-01 (gate present to drain against); rebase onto post-implement-loop `main` first.
- **Risks**: over-routing a STATUS leg (NFR-001); `done_bookkeeping` status legs must stay on the meta-bearing primary dir, not be coord-ified.
- **Brownfield refinement**: `executor.py` already computes a PRIMARY `target_feature_dir` at `:887` — **thread it through to `:976`** rather than swap-and-recompute the coord-aware `feature_dir`. In `merge/resolve.py` route only `:98` (meta read); leave `:63` (handle→dir-name canonicalization at the no-silent-fallback boundary) on `candidate_`. Do not reintroduce the silent `main` target-branch fallback (#2139 neighborhood).

### IC-03 — Lane A: lanes/core cluster routing

- **Purpose**: Route the `lanes/` + `core/worktree_topology` PRIMARY reads; `recovery.py:356` per-leg split; drain #2185 pins.
- **Relevant requirements**: FR-001, FR-002, FR-008.
- **Affected surfaces**: `lanes/merge.py` (`:68`/`:198`), `lanes/recovery.py` (`:356` mixed, `:611` LANE_STATE), `lanes/worktree_allocator.py` (`:360` meta.json), `core/worktree_topology.py` (`:138` single swap co-resolves three PRIMARY legs).
- **Sequencing/depends-on**: IC-01.
- **Risks**: `worktree_allocator` chicken-and-egg (reads meta to discover coord) — `kind=PRIMARY_METADATA` is topology-blind and correct.
- **Brownfield refinement (sizing)**: `lanes/recovery.py::scan_recovery_state` already carries `# noqa: C901` (over the complexity ceiling). The per-leg split must **extract the PRIMARY-planning read and the status-events read into named helpers + drop the `# noqa` + add focused tests** — not add another branch. **Guardrail:** `candidate_feature_dir_for_mission` is the C-005 STATUS primitive — re-point PRIMARY reads off it, never remove or "converge away" the coord-aware primitive (would break C-001).

### IC-04 — Lane A: coord-topology integration proof

- **Purpose**: Extend `build_coord` to a **divergent husk** (sentinel-identity coord `meta.json`; PRIMARY-only `lanes.json`/`tasks/` seeded post-worktree-add; assert husk lacks them) and add a real merge/recovery/topology integration test that fails if any routed read reverts to coord-aware.
- **Relevant requirements**: FR-009, NFR-004, SC-001.
- **Affected surfaces**: `tests/specify_cli/write_side/topology_fixtures.py`, `tests/integration/` (new coord-topology merge test).
- **Sequencing/depends-on**: IC-02/IC-03 (the routed code under test). The fixture extension may land first so the routing WPs assert against it.
- **Risks**: a non-divergent husk silently passes a broken routing (the squad's CRITICAL finding) — the divergence assertion is the guard.

### IC-05 — Lane B: identity routing + ownership table

- **Purpose**: Emit a definitive per-site ROUTE/KEEP/owned-by-implement-loop table (cross-checked vs the sibling's ROUTE+KEEP list, re-resolved against merged `main`), then primary-anchor the genuinely-owned identity sites — including the shared-variable mixed sites with their own anchor.
- **Relevant requirements**: FR-004, FR-005, FR-007 (consumes IC-01 arm), FR-008 (Lane B co-land).
- **Affected surfaces**: `cli/commands/next_cmd.py` (`:187`/`:253`/`:631`), `cli/commands/implement.py` (`:1389` own anchor), `cli/commands/agent/workflow.py` (owned identity legs `:1274`/`:2732` clean; `:1636` shared-variable own anchor) — only legs NOT inside the implement-loop ROUTE scope.
- **Sequencing/depends-on**: IC-01 (the arm must exist before its sites can be ratchet-validated); rebase onto merged `main` to re-resolve citations.
- **Risks**: a site falling into the gap between the two missions (neither routes it) — the ownership table must account for every Lane B site, no "verify later".
