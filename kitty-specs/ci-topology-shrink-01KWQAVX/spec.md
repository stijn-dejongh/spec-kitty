# Mission Specification: CI Topology Shrink & Guard Un-Blinding

**Mission**: `ci-topology-shrink-01KWQAVX` (mission_id `01KWQAVXZGH1G36HB9QKWMYXGD`)
**Created**: 2026-07-04
**Status**: Draft
**Input**: User description: "spec a remediation mission for Slice C — CI-topology shrink (#2378 shard-side + #1933 group-side, sequenced as siblings). it is hurting us, hard."
**Closes**: #2378 (shard-side split) · #1933 (group-side shrink) · a new arch-un-blind issue (to be filed) — all under epic #1931.
**Out of scope**: #2283 factors (b)/(c) · #2077 CT7 · #2071 audit · the marker→job model itself (#2034/#2368 substrate — consumed, not rebuilt).

## Context & Problem (why "hurting us, hard")

`.github/workflows/ci-quality.yml` routes CI via three coupled authorities (dorny filter block, the `core_misc` catch-all group, and the FR-010 fail-closed `unmatched→run_all` alarm), all modeled by `tests/architectural/_gate_coverage.py` and pinned by the 8 invariants the #2368 CI suite-map mission bound. Live ground truth (3-lens pre-spec squad, 2026-07-04):

- **Wallclock:** `fast-tests-core-misc` is a single **unsharded 16.9-min** job; `integration-tests-core-misc (architectural)` (12.2 min) runs `needs`-sequentially behind it → a **~29-min critical path = ~85% of the 34-min pipeline, 33% of all CI compute** — one grab-bag, 6.3× the median focused shard, un-parallelizable without a cut.
- **Mode A — 37 UNMAPPED src dirs (68.5k LOC):** `auth` (5.1k), `migration` (5.5k), `tracker` (4k), `dossier` (3.2k), `retrospective` (6.8k), `orchestrator_api`, `bulk_edit`, `tasks`, `doctor`, etc. are in **no** named filter group → every touch trips `unmatched→run_all` (the *entire* pipeline reruns). Fail-safe but maximally expensive.
- **Mode B — 13 MAPPED-but-ARCH-BLIND dirs (120k LOC, incl. `cli` 58k, `sync` 17.7k, `upgrade` 15.9k, `merge` 6.3k):** `tests/architectural` + `tests/adversarial` run **only** via the `{core_misc, execution_context, acceptance}` groups, so an isolated change to `cli/`, `sync/`, `merge/`, `upgrade/` merges green with the dead-module / stale-symbol / terminology / status-boundary gates **never firing**. This is the root cause of the orphan-coverage bugs the team whack-a-moled all session (#2370 `m_3_2_4`, acceptance/state, #2379 migration) — those only got caught when an *unrelated* path happened to drag the arch shard in.
- **Failure isolation is near-zero:** a red `fast-tests-core-misc` names one job covering a dozen slices and cascades to skip ~11 downstream jobs.

The suite is 0-orphan **today only because** the whole-tree catch-all sweeps mask everything — coverage rides on the grab-balls, not on focused routing. That is the fragility this mission removes.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Focused CI for a single-area change (Priority: P1)

A spec-kitty developer changes one source area (e.g. `src/specify_cli/auth/**`) and CI runs **only** that area's focused shard(s) plus the always-on gates — instead of re-running the entire pipeline because the dir was unmapped and tripped the fail-closed catch-all.

**Why this priority**: This is the acute, everyday pain (Mode A) and the foundational half — the named groups this delivers are the substrate the split (US3) and the arch-un-blind (US2) build on. Delivered alone it already removes the `run_all` tax on the hottest dirs.

**Independent Test**: For each worklist dir, a path-filter fixture test asserts a PR touching only that dir routes to its named group + focused shard and does **not** set `unmatched=true`/`run_all`.

**Acceptance Scenarios**:

1. **Given** `auth/**` is promoted to a named filter group wired to a focused shard, **When** a PR touches only `src/specify_cli/auth/**`, **Then** the `changes` job routes to the `auth` group, only the auth shard(s) + unconditional lint/architectural gates run, and `run_all` is **not** triggered.
2. **Given** a worklist dir with tests split across two roots (e.g. `migration` → `tests/migration` + `tests/specify_cli/migration`), **When** its shard is carved, **Then** both roots are consolidated into that shard and the `@slow` perf test remains excluded (runs only in `slow-tests`), with no double-run.
3. **Given** a src path still unmapped (a future dir), **When** it is touched, **Then** the fail-closed catch-all still forces coverage (fail-safe preserved).

---

### User Story 2 - Architectural guards never silently skip (Priority: P1)

A change confined to a previously arch-blind package (`cli/`, `sync/`, `upgrade/`, `merge/`, …) can **no longer** merge green with the architectural + adversarial suite skipped. The dead-module, stale-symbol, terminology, and status-boundary gates run on **every** source change.

**Why this priority**: This is the correctness root cause of the session's recurring orphan-coverage bugs (Mode B, 120k LOC blind). It is the single highest-*correctness*-leverage change; a wallclock win that still lets real defects merge silently would be a hollow victory.

**Independent Test**: For each of the 13 arch-blind dirs, a fixture asserts a touch selects the architectural + adversarial suite. A differential matrix test asserts arch/adversarial coverage over **100%** of `src/specify_cli/*` dirs (0 blind).

**Acceptance Scenarios**:

1. **Given** `cli/**` was arch-blind, **When** a PR touches only `src/specify_cli/cli/**`, **Then** `tests/architectural` + `tests/adversarial` are selected and the dead-module / stale-symbol / terminology / status-boundary gates execute.
2. **Given** a PR that would introduce a new dead module or a legacy-terminology regression in a formerly-blind dir, **When** CI runs, **Then** the relevant architectural gate fails the PR (it is not silently skipped).

---

### User Story 3 - Core-misc is no longer the pipeline long pole (Priority: P2)

The 16.9-min unsharded `fast-tests-core-misc` monolith is subdivided into a matrix of focused shards so the core-misc critical path is no longer the pipeline's long pole, and a red result names the specific slice that broke.

**Why this priority**: The wallclock + failure-isolation win. P2 because it rides on the named-group substrate from US1; the shard carve and the group mapping land together per slice, but the *primary correctness value* is in US1/US2.

**Independent Test**: Measure per-shard wallclock on a `run_all`; assert no single shard collects the full catch-all universe and the core-misc critical path is ≤ the next-longest independent lane (numeric ceiling set from fresh plan-time timings). Assert a deliberately-failed shard names its slice.

**Acceptance Scenarios**:

1. **Given** `fast-tests-core-misc` is matrix-sharded, **When** `run_all` executes, **Then** the core-misc critical path is ≤ the next-longest independent lane and no shard collects the whole catch-all universe.
2. **Given** a test fails in one carved slice, **When** CI reports, **Then** the failing job names that slice (not an opaque grab-bag).

---

### Edge Cases

- **Windows split-brain**: a carved test file that is also in `ci-windows.yml`'s static 19-file list — must update that list in the same commit or FR-003c reds.
- **Real-port / daemon serial tests**: `tests/sync/test_orphan_sweep.py` binds ports 9400-9449 and runs `-n0` serially — any slice containing daemon/real-port tests must preserve the serial pass; never blanket `-n auto`.
- **`dossier` latent gap**: `tests/dossier` is `core_misc`-globbed but in no integration matrix shard — carving it *fixes* a real hole; verify against the 0-orphan baseline.
- **Nested test roots**: `tests/specify_cli/<D>` slices (`orchestrator_api`, `bulk_edit`) need the integration matrix `ignore_args` updated by hand (not covered by FR-012's whole-tree check).
- **Coverage drop**: a new `fast-tests-<D>` forgotten from `sonarcloud.needs`/`slow-tests.needs` silently drops that slice's coverage XML from Sonar with no red — must be closed by construction.
- **Dir with no test cone**: a src dir mapped to a group but with no tests — must not orphan or produce a vacuous shard.
- **Job-count explosion**: promoting ~15 dirs to dedicated `fast-`+`integration-` jobs balloons `quality-gate.needs` (~45 already) — composite groups cap this.

## Requirements *(mandatory)*

### Functional Requirements

| ID | Title | User Story | Priority | Status |
|----|-------|------------|----------|--------|
| FR-001 | Promote every hot unmapped src dir to a named dorny filter group (auth, migration, tracker, dossier, retrospective, orchestrator_api, bulk_edit, tasks, doctor, + remaining Mode-A dirs) so none falls to `unmatched→run_all`. | US1 | High | Open |
| FR-002 | Register each new group across ALL bound-model surfaces atomically: dorny filter glob, `changes.outputs` row, `unmatched` enumeration loop, ≥1 test-job `if:`, and the `JOB_GROUPS` table — no surface hand-added beside the model. | US1 | High | Open |
| FR-003 | Subdivide `fast-tests-core-misc` into a matrix of focused shards (mirroring the existing `integration-tests-core-misc` matrix); each shard owns coherent, non-overlapping test roots. | US3 | High | Open |
| FR-004 | Update the `fast-tests-core-misc` `--ignore` mirror list in lockstep with every shard carve (FR-012 ignore-mirror invariant), and update the integration-matrix `ignore_args` for nested `tests/specify_cli/<D>` slices. | US3 | High | Open |
| FR-005 | Make `tests/architectural` + `tests/adversarial` run on 100% of src changes (un-blind the 13 Mode-B dirs) — via an always-on cheap arch trigger or the union of all src-backed groups. | US2 | High | Open |
| FR-006 | Each new shard emits its own `--cov`/`coverage-*.xml` so coverage topology is preserved per slice. | US3 | Medium | Open |
| FR-007 | Register every new test job in ALL consuming needs-lists: `quality-gate`, `slow-tests`, `sonarcloud`, `mutation-testing`, `diff-coverage`. | US3 | High | Open |
| FR-008 | Propagate new group/job names to the second-layer surfaces: `ci-windows.yml` static list, `scripts/ci/quality_gate_decision.py` JOB_GROUPS, `drift-detector.yml`, `release.yml` — closing the split-brain. | US1 | High | Open |
| FR-009 | Preserve fail-safe selection: carve-outs only NARROW; an unmapped or newly-added src path still triggers coverage; nightly `run_all` still over-covers (no new blind spot). | US1 | High | Open |
| FR-010 | Use composite groups (e.g. `agent_surface` = orchestrator_api+tracker+dossier; `lifecycle` = migration+doctor+bulk_edit) where they cap job-count while still removing dirs from the unmapped set. | US1 | Medium | Open |
| FR-011 | Preserve real-port serial `-n0` passes, `--dist loadfile` (never bare `load`), and per-worker HOME isolation on every new shard. | US3 | High | Open |
| FR-012 | The `migration` shard consolidates `tests/migration` + `tests/specify_cli/migration` and preserves the `and not slow` marker exclusion (the `@slow` perf test runs only in `slow-tests`). | US1 | High | Open |

### Non-Functional Requirements

| ID | Title | Requirement | Category | Priority | Status |
|----|-------|-------------|----------|----------|--------|
| NFR-001 | Core-misc critical path | Reduce the core-misc critical-path lane from ~29 min (16.9m fast + 12.2m arch, sequential) to **≤ the next-longest independent lane** (baseline `integration-tests-next` ~13.5m); exact numeric ceiling fixed from fresh per-shard timings at plan time. | Performance | High | Open |
| NFR-002 | Architectural coverage completeness | Architectural + adversarial guards execute on **100%** of `src/specify_cli/*` dirs (from 120k LOC / 13 dirs blind → **0** blind), asserted by a differential-matrix architectural test. | Correctness | High | Open |
| NFR-003 | Coverage preservation | Total selected-test count for a `run_all` is unchanged (carve-outs narrow, never drop); the `_gate_coverage` orphan count stays **0** (baseline 28,573 tests, 0 orphans). | Reliability | High | Open |
| NFR-004 | Feedback isolation | A single-area PR runs only its focused shard(s) + always-on gates (not the full matrix), and a failing shard names its slice. | Usability | Medium | Open |
| NFR-005 | Invariant integrity | All 8 #2368 WP04 architectural invariants (FR-010c enumeration + 2nd arm, FR-010 boolean, FR-012 ignore-mirror, FR-003b/c, FR-011 JOB_GROUPS≡if, marker-completeness) remain green through every WP. | Reliability | High | Open |

### Constraints

| ID | Title | Constraint | Category | Priority | Status |
|----|-------|------------|----------|----------|--------|
| C-001 | Consume, don't rebuild the substrate | Do not rebuild the marker→job model or the fail-closed catch-all (#2034/#2368) — extend the bound `_gate_coverage` model additively. | Technical | High | Open |
| C-002 | No split-brain derived surfaces | Every derived surface (catch-all OR-list, JOB_GROUPS, ci-windows static list) is asserted-against-parsed-source or the build rejects (Decision 8). | Technical | High | Open |
| C-003 | Single-owner hot file | `ci-quality.yml` edits are dependency-sequenced across per-slice WPs (no two lanes edit it in parallel); owned-file disjointness is the merge guard (per #2368 lesson). | Technical | High | Open |
| C-004 | Scope fence | Keep #2283 factors (b)/(c), #2077 CT7, #2071 audit, new markers, gate rewrites, and WIP-title semantics OUT of scope. | Business | High | Open |
| C-005 | Needs-list integrity by construction | Add a new architectural invariant binding the hand-maintained needs-lists (`{test jobs} ⊆ sonarcloud.needs ∩ slow-tests.needs`) so a forgotten job cannot silently drop coverage. | Technical | High | Open |
| C-006 | Nightly-move deferred | #1933's literal nightly-scheduled-full-suite is OUT (shrink interpretation only); offer a thin nightly-schedule option in-mission ONLY if fresh timings show the post-shrink PR critical path still > ~15 min. | Technical | Medium | Open |

### Key Entities

- **Filter group** (dorny `changes` job): a named path→group mapping; may be src-backed (globs `src/**`) or test-only. Src-backed groups participate in the `unmatched` enumeration.
- **Shard job** (`fast-tests-<D>` / `integration-tests-<D>` / a matrix entry): a CI job running a coherent slice of test roots under a fixed marker expression; gated by a group's `if:`; emits its own coverage XML.
- **Bound model** (`_gate_coverage.py` + `_gate_coverage_baseline.json`): the parsed authority that asserts every derived surface equals its source; the 8 invariants live here.
- **`unmatched`/`run_all` catch-all**: the fail-closed alarm — `any_src AND NOT any(named src-backed group)` → full run; a loud alarm, not steady state.
- **Needs-list**: a job's `needs:` dependency set (`quality-gate`, `slow-tests`, `sonarcloud`, `mutation-testing`, `diff-coverage`); only `quality-gate` is currently invariant-bound.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: **0** worklist src dirs fall to `unmatched→run_all` — a mechanized architectural test asserts each maps to a named group AND a focused shard (not `run_all`).
- **SC-002**: Architectural + adversarial guards run on **100%** of `src/specify_cli/*` dirs (from 13 blind → 0), proven by a differential-matrix test that fails if any dir is arch-blind.
- **SC-003**: The core-misc critical path is **≤ the next-longest independent lane** (from ~29 min; exact ceiling set from fresh plan-time timings) and no single shard collects the full catch-all universe.
- **SC-004**: The `_gate_coverage` orphan count remains **0** and the total `run_all` selected-test count is unchanged (coverage preserved; carve-outs only narrow).
- **SC-005**: All 8 #2368 WP04 invariants remain green AND the new needs-list-subset invariant (C-005) is green — no silent coverage drop is possible.
- **SC-006**: For each carve-out dir, a path-filter fixture test demonstrates a single-area PR triggers only its focused shard(s) + always-on lint/architectural gates.
