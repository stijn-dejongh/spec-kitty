# Implementation Plan: Coord Write-Placement Closure & Birth-Cutover

**Branch**: `feat/coord-write-placement-closure` | **Date**: 2026-07-25 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `kitty-specs/coord-write-placement-closure-01KYCF83/spec.md`

## Summary

Close the coord/primary write-placement residual left after #2874 so the split-brain is unrepresentable across **all** of `src/` (not a 17-module allowlist) and symmetric on the read side, add a cure for pre-existing drift (`agent mission repair`), and make new missions **born runtime-reconciled** (the #2917 birth-cutover) so the dogfood corpus never re-drifts. Approach: extend the existing placement port (do not re-architect it), replace the allowlist ratchet with a whole-tree AST gate, route the remaining writers/readers through the port, reuse `cutover_mission` (the sole `status_phase` writer) at the merge bake hook, and event-source exactly the two authoring paths (#2684) that make a birth-stamp valid. Sequence A→B; front-load the 12 drifted missions first to clear CI.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: typer, rich, ruamel.yaml, jsonschema; `ast`/pytestarch for architectural gates; subprocess-based git (no gitpython)
**Storage**: git branches (coord/primary partitions), append-only `status.events.jsonl`, `meta.json`, `tasks.md`
**Testing**: pytest (ATDD, red-first per DIRECTIVE_041); ruff + mypy zero-warning; architectural gates in `tests/architectural/`; the durable dogfood lock `tests/specify_cli/migration/test_dogfood_corpus_backfilled.py`
**Target Platform**: Linux / macOS / Windows CLI
**Project Type**: single (CLI framework — `src/specify_cli` + `src/mission_runtime`)
**Performance Goals**: the whole-tree AST enforcement gate completes within the existing `tests/architectural/` time budget (seconds, not minutes); zero runtime-path performance regression
**Constraints**: no green-wash of the lock (preserve `verify_backfill` parity); whole-tree coverage with individually-justified sanctioned-primitive exclusions only; fail-loud on partition mismatch; idempotent cutover (deterministic seed ids); reuse `cutover_mission` as the sole `status_phase` writer; no `MissionArtifactHome`/topology re-architecture; no `doctor coordination --fix` growth
**Scale/Scope**: ~9 implementation concerns across `src/mission_runtime/{artifacts,resolution}.py`, `src/specify_cli/{coordination,status,migration,merge,mission_metadata}`, `src/specify_cli/cli/commands/agent/`, and `tests/architectural/`

## Charter Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.* Charter present (`compact` mode; `software-dev-default`). Relevant governing principles and their fit:

- **Single canonical authority** — reinforced, not violated: the mission consolidates writers onto the one placement port and keeps `cutover_mission` the sole `status_phase` writer (C-004). No rival authority is introduced.
- **Architectural alignment** — the fix extends the existing port kind-mapping (FR-002) rather than re-architecting `MissionArtifactHome` (explicitly OUT, C-002).
- **DDD + tiered rigour** — core seams (placement routing, cutover) get full rigour + red-first ATDD; the front-load (IC-01) is a mechanical, deterministic corpus write.
- **ATDD-first / red-first** — every FR ships a red-first test through the real entry point (DIRECTIVE_041); the birth-write repro drives create→implement→merge, not a fixture.
- **Canonical sources** — no improvised substitutes; reuse `cutover_mission`, the placement port, and the existing `doctor coordination --fix` (kept minimized) rather than growing them.

No charter violations → Complexity Tracking not required.

## Project Structure

### Documentation (this mission)

```
kitty-specs/coord-write-placement-closure-01KYCF83/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
└── tasks.md             # Phase 2 (/spec-kitty.tasks — NOT created here)
```

### Source Code (repository root)

```
src/mission_runtime/
├── artifacts.py            # kind→partition maps; PRIMARY_METADATA commit_target (FR-002); decisions/traces classification (FR-003/006)
└── resolution.py           # placement_seam / resolve_placement_only / read_dir — read-surface authority (FR-004)

src/specify_cli/
├── coordination/
│   ├── commit_router.py    # partition-split write chokepoint (route remaining writers here)
│   └── status_transition.py# close the HEAD-derived fallback #1716 (FR-003)
├── status/
│   ├── emit.py             # status write surface; status_phase's only reader (lane mirror)
│   └── bookkeeping…        # decision_log.py / bookkeeping_commit.py routing (FR-003)
├── migration/
│   └── runtime_state_cutover.py  # sole status_phase writer — reused at birth (FR-009, C-004)
├── merge/
│   ├── ordering.py         # _bake_mission_number_into_mission_branch — birth-cutover hook (FR-009)
│   ├── executor.py         # _phase_bake_and_pre_target_done — invocation point
│   └── bookkeeping_projection.py # coord→target projection writer (route via port) (FR-003)
├── mission_metadata.py     # write_meta — partition-aware target (FR-002)
└── cli/commands/agent/     # new `mission repair` command (FR-005)

tests/architectural/
├── test_no_write_side_rederivation.py   # replace 17-module allowlist → whole-tree (FR-001)
├── test_safe_commit_import_boundary.py  # extend to check target= seam-derivation (FR-001)
└── test_read_surface_placement_guard.py # NEW read-side enforcement gate (FR-004)
```

**Structure Decision**: single-project CLI framework; changes are surgical extensions of existing seams under `src/mission_runtime` and `src/specify_cli`, plus architectural gates under `tests/architectural/`. No new top-level packages.

## Implementation Concern Map

> Concerns, not work packages. `/spec-kitty.tasks` translates these into WPs.

### IC-01 — Front-load the drifted corpus (unblock CI)

- **Purpose**: run the one-time backfill over the 12 drifted missions and commit the flips so `test_dogfood_corpus_backfilled` passes and 3.2.6 is unblocked.
- **Relevant requirements**: FR-007; SC-001 (initial green).
- **Affected surfaces**: `kitty-specs/**` (committed corpus); `migrate backfill-runtime-state` (`migrate_cmd.py`).
- **Sequencing/depends-on**: none — independent, lands first.
- **Risks**: must exclude the self-mission; deterministic byte-stable seeds; run against the branch that becomes the corpus.

### IC-02 — Whole-tree write-placement enforcement

- **Purpose**: replace the 17-module `_CHECKOUT_GRAMMAR_MODULES` allowlist with a whole-tree AST gate; extend `test_safe_commit_import_boundary` to assert `target=CommitTarget(...)` is seam-derived — so a bypass anywhere in `src/` reds.
- **Relevant requirements**: FR-001; NFR-001; NFR-004; SC-002.
- **Affected surfaces**: `tests/architectural/test_no_write_side_rederivation.py`, `test_safe_commit_import_boundary.py`; a documented, individually-justified sanctioned-primitive exclusion list.
- **Sequencing/depends-on**: informs IC-03/IC-04 (they must satisfy the widened gate).
- **Risks**: false positives on genuine sanctioned primitives; the exclusion list must be small + justified, not a new allowlist.

### IC-03 — Partition-aware meta.json routing

- **Purpose**: give `PRIMARY_METADATA` a partition-aware write target (extend the port kind-mapping) so `write_meta` / `_flip_phase` / `_bake_mission_number` express a coord/primary two-partition write instead of a single ambient `feature_dir`.
- **Relevant requirements**: FR-002; SC-005 (enabling).
- **Affected surfaces**: `mission_runtime/artifacts.py`, `resolution.py`; `mission_metadata.py::write_meta`.
- **Sequencing/depends-on**: prerequisite for IC-08 (birth-write).
- **Risks**: `meta.json` is PRIMARY while seed events are COORD — the routing must split cleanly; must not re-architect `MissionArtifactHome` (C-002).

### IC-04 — Close the emit fork + unscanned writers + classify decisions/traces

- **Purpose**: close the `_current_branch` HEAD-derived fallback (#1716); route `bookkeeping_projection` / `bookkeeping_commit` / `decision_log` through the port; classify `decisions.events.jsonl` and `traces/` in the partition SSOT.
- **Relevant requirements**: FR-003; FR-006; SC-006.
- **Affected surfaces**: `coordination/status_transition.py`, `merge/bookkeeping_projection.py`, `git/bookkeeping_commit.py`, `events/decision_log.py`, `mission_runtime/artifacts.py` (SSOT maps).
- **Sequencing/depends-on**: satisfies IC-02's widened gate.
- **Risks**: the emit fallback is reached in the pre-`meta.json` create window — the replacement must not deadlock; `traces/` reclassification (PRIMARY→COORD) may move existing writes.

### IC-05 — Read-side placement enforcement

- **Purpose**: route every mission-artifact read through `artifact_home_for(kind).read_surface` and fail loud on a partition mismatch — the symmetric completion of #2874.
- **Relevant requirements**: FR-004; NFR-002; SC-003.
- **Affected surfaces**: `mission_runtime/resolution.py` (read authority); read call sites; a NEW `tests/architectural/test_read_surface_placement_guard.py`.
- **Sequencing/depends-on**: none hard; pairs with IC-02 for the symmetric gate.
- **Risks**: reads are more numerous than writes; the fail-loud must not break legitimate degrade paths (e.g. the lenient diagnose path #2906 already governs) — reconcile with existing read-gate guards.

### IC-06 — `agent mission repair` (Gap-2 cure)

- **Purpose**: a new command that detects a pre-existing content split-brain and forward-only repairs it (fail-loud with a diff otherwise) — distinct from `doctor coordination --fix`.
- **Relevant requirements**: FR-005; NFR-005; SC-004.
- **Affected surfaces**: `src/specify_cli/cli/commands/agent/mission_*.py` (new subcommand); reuse the strict-ancestor/clean-worktree primitives from `_coordination_doctor.py`.
- **Sequencing/depends-on**: none.
- **Risks**: must never force-overwrite divergence; keep `doctor coordination --fix` minimized (C-002/C-003).

### IC-07 — Event-source the two authoring paths

- **Purpose**: event-source exactly the claim fields (`shell_pid`/`agent`) and subtask-completion (`tasks.md` checkboxes) so nothing un-seeded accrues to frontmatter/`tasks.md` (extends #2684).
- **Relevant requirements**: FR-008.
- **Affected surfaces**: `coordination/status_transition.py` (claim), `core/subtask_rows.py` / `tasks_*` (subtask completion), `frontmatter.py`.
- **Sequencing/depends-on**: prerequisite for IC-08 and IC-09; scope strictly the two paths (C-002).
- **Risks**: the runtime reader must stay correct; do NOT broaden into the #1619 dual-write program.

### IC-08 — Birth-time runtime cutover

- **Purpose**: stamp `status_phase` and reconcile residual runtime at land via `cutover_mission`, at the `_bake_mission_number` hook, routed through IC-03's port — so missions are born reconciled.
- **Relevant requirements**: FR-009; NFR-003; C-004.
- **Affected surfaces**: `merge/ordering.py` (adjacent to the mission_number bake), `merge/executor.py`, `runtime_state_cutover.py` (reuse).
- **Sequencing/depends-on**: **after IC-03 and IC-07** (C-001).
- **Risks**: fire only after the target commit is durable (merge-abort/`--resume` safety); coord/flat two-partition placement is the crux; idempotent with the one-time migration.

### IC-09 — Re-key the acceptance lock + migration coexistence

- **Purpose**: re-key `test_dogfood_corpus_backfilled` to an event-log birth invariant (every mission whose event log carries runtime, excluding the self-mission, is `status_phase>=1` + non-empty snapshot); add a regression that the one-time migration still cuts over a legacy corpus.
- **Relevant requirements**: FR-010; NFR-006; C-003; SC-001 (durable green).
- **Affected surfaces**: `tests/specify_cli/migration/test_dogfood_corpus_backfilled.py`; a migration-coexistence test.
- **Sequencing/depends-on**: **after IC-07** (authoring retirement changes the eligible set); preserve the `verify_backfill` parity assertion (no green-wash).
- **Risks**: re-keying must not shrink coverage (the green-wash trap) — key on the event log, not frontmatter eligibility.
