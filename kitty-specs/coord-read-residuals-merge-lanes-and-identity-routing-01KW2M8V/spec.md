# Mission Specification: Coord-Read Residuals — Merge/Lanes Planning Reads + Identity-Read Routing

**Mission Branch**: `mission/coord-read-residuals-2185-2186`
**Created**: 2026-06-26
**Status**: Draft (revised after post-spec adversarial squad — facts verified sound; fixture-falsifiability, gate-narrative, and ownership revisions folded in)
**Input**: Issues #2185 + #2186 (children of epic #2160, siblings of #2115). The parallel, out-of-loop half of the coord-authority read-routing cleanup — the surfaces the implement-loop mission (`implement-loop-coord-authority-completion-01KW2E7A`) is boundary-forbidden (C-009) from touching.

## Context & Problem

`#2106` (merged 2026-06-24) made planning artifacts — `meta.json` (PRIMARY_METADATA), `lanes.json` (LANE_STATE), `tasks/` (WORK_PACKAGE_TASK) — live **only on the PRIMARY checkout** for every topology. Under coordination (`coord`) topology the materialized `-coord` worktree is a **status-only husk**: it carries no PRIMARY-partition artifacts.

Multiple read sites still resolve those PRIMARY-kind artifacts through **coord-aware** resolvers (`candidate_feature_dir_for_mission`, `resolve_feature_dir_for_mission`), which land on the husk. On a coord-topology mission those reads silently return empty/stale data, raise resolver errors, or fall back to defaults. This Mission routes the two residual classes the implement-loop Mission is forbidden from touching:

- **Lane A (#2185)** — the **merge / finalize / recovery / lanes / topology** path reads of `lanes.json`, `tasks/`, and `meta.json`.
- **Lane B (#2186)** — **identity / telemetry / lifecycle** reads of `meta.json` in the command layer (the `next_cmd` telemetry-drop class and the post-#2115 fallback-dependent identity probes).

The canonical fix already exists and is in production use (introduced by the #2106 gate-read work): route PRIMARY-partition reads through `resolve_planning_read_dir(repo_root, slug, kind=...)` (which folds the handle and resolves PRIMARY topology-blind via `primary_feature_dir_for_mission`), or anchor directly on `primary_feature_dir_for_mission(repo_root, _canonicalize_primary_read_handle(repo_root, slug))`. STATUS-partition reads **must stay coord-aware**.

> **Research correction (binding for this Mission):** the artifact "kind" labels in the issue tables are partly wrong. The actual partition (verified against `mission_runtime.is_primary_artifact_kind`) is restated per-site in the Surface Inventory below. Several sites the issues label `LANE_STATE` actually read `meta.json` (PRIMARY_METADATA); several "pure" sites are **mixed** PRIMARY+STATUS and require a per-leg split. The Mission routes by the *real* kind, not the issue label.

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Merge/finalize/recovery works on a coord-topology mission (Priority: P1)

As an operator merging or recovering a **coord-topology** mission, I want the merge/forecast/finalize/recovery/topology code to read `lanes.json`, `tasks/`, and `meta.json` from the PRIMARY checkout, so that forecasts, lane resolution, WP-path lookup, abort teardown, recovery scans, and worktree-topology materialization see real planning data instead of the empty `-coord` husk.

**Why this priority**: Today these paths silently lose lane/WP/identity data or raise resolver errors on coord topology — the merge/recovery surface is where data loss is most destructive (wrong branch, skipped WPs, failed teardown).

**Independent Test**: Build a real `coord` topology (`git worktree`-backed, via `tests/specify_cli/write_side/topology_fixtures.py::build_coord`) **extended so PRIMARY-only artifacts genuinely diverge from the husk** (see FR-009): seed production-shaped `lanes.json` + `tasks/` on PRIMARY *after* the worktree is created (so they do not propagate to the coord checkout), and assert the `-coord` husk lacks them. Drive the real `_run_lane_based_merge` / `scan_recovery_state` / `materialize_worktree_topology` paths; assert each reads from `primary_feature_dir` and returns the seeded lanes/WPs, and that reverting any read to the coord-aware resolver makes the test fail (the husk has no such artifact). Unit stubs that hand in a primary dir directly are explicitly disallowed (they mask the routing bug).

**Acceptance Scenarios**:
1. **Given** a coord-topology mission whose `-coord` husk has no `lanes.json`, **When** `merge/forecast.py` builds a forecast, **Then** it reads `lanes.json` (and the review-artifact `tasks/` preflight) off PRIMARY and forecasts the real WP set.
2. **Given** the same mission, **When** `_run_lane_based_merge` (executor) runs, **Then** the `lanes.json` / `meta.json` legs resolve PRIMARY while the `status_feature_dir` STATUS leg stays coord-aware.
3. **Given** a recovery scan (`lanes/recovery.py::scan_recovery_state`), **When** it reads lanes (LANE_STATE) and tasks (WORK_PACKAGE_TASK), **Then** those legs resolve PRIMARY while the `status.events.jsonl` leg stays coord-aware.
4. **Given** `_mark_wp_merged_done` (`merge/done_bookkeeping.py`), **When** it resolves the WP markdown path, **Then** it uses `resolve_planning_read_dir(kind=WORK_PACKAGE_TASK)` and the misleading "do not use the read-path resolver" comment is removed; the status-transactional legs are unchanged.

### User Story 2 — Identity/telemetry survives coord topology (Priority: P1)

As a maintainer relying on lifecycle telemetry and mission-type routing, I want `next_cmd.py` identity reads (and the other unguarded command-layer identity probes) to anchor on PRIMARY, so that lifecycle records are written and `get_or_start_run` routes on the real mission type even under coord topology.

**Why this priority**: `next_cmd.py:631` (`get_mission_type` → `get_or_start_run`) is **routing**, not just telemetry — a husk miss starts the run with the wrong/default mission type (runtime-behavioral, not merely observability). `:187`/`:253` silently drop lifecycle records.

**Independent Test**: On a coord topology whose **husk `meta.json` carries a sentinel identity distinct from PRIMARY** (FR-009 — otherwise a husk-landing read returns the same `mission_id` and the test is non-falsifiable), invoke the `next` lifecycle-record and answer-handling paths; assert the lifecycle record is written with the **PRIMARY** `mission_id` (not the sentinel) and `get_mission_type` returns the PRIMARY type (not the husk/default). Reverting the read to the coord-aware resolver must surface the sentinel/default and fail the test.

**Acceptance Scenarios**:
1. **Given** a coord-topology mission, **When** `_pair_previous_lifecycle_record` / `_write_issuance_lifecycle_record` run, **Then** `resolve_mission_identity` reads `meta.json` off PRIMARY and the `started`/`completed` records are written (not silently swallowed).
2. **Given** the same mission, **When** `_handle_answer` resolves mission type, **Then** `get_mission_type` returns the real type and `get_or_start_run` starts the correct run.
3. **Given** any remaining unguarded command-layer identity probe relying on the `implement.py:1018` primary-anchor fallback, **When** that probe runs, **Then** it carries its own PRIMARY anchor and does not depend on the fallback.

### User Story 3 — Residual classes become observable and regression-proof (Priority: P2)

As a maintainer, I want the architectural dir-read gate to *see* the identity-read residual class, so that the fixes are ratchet-enforced and a future regression (or the eventual removal of the `implement.py:1018` fallback) cannot silently re-introduce the husk-read bug.

**Why this priority**: The existing dir-read scanner matches only `resolver / "tasks"|"lanes.json"|"*.md"` path-joins; a `meta.json`/identity read is a **function-call** shape (`resolve_mission_identity(dir)` / `get_mission_type(dir)`) that is **structurally invisible to both scan arms** — even after the implement-loop Mission widens scan *scope* to whole-`src`. So the dir-join coverage for `merge/`/`lanes/`/`core/` (Lane A) is **inherited** from the implement-loop Mission (C-SEQ), while the identity-read class (Lane B) has **no detector at all** and must be built here. This is the automated backstop for the #2115 fallback-removal sequencing risk.

**Independent Test**: (a) Confirm the inherited whole-`src` scan flags a deliberately-wrong PRIMARY dir-join in `merge/`/`lanes/`/`core/` (Lane A). (b) Add the new identity-read arm, then an unguarded `resolve_mission_identity(coord_dir)` in the command layer; assert the arm flags it; remove it; assert green. The identity arm ships with a committed synthetic-AST non-vacuity self-test (mirroring the existing gate pattern), so its teeth are an automated regression, not a manual ritual.

**Acceptance Scenarios**:
1. **Given** the implement-loop Mission's inherited whole-`src` dir-read scan scope, **When** a Lane A site reads a PRIMARY kind off a coord-aware resolver, **Then** the (inherited) gate fails — this Mission *verifies* that coverage rather than re-adding it.
2. **Given** the **new command-layer identity-read scan arm** built by this Mission, **When** a `cli/commands/` `resolve_mission_identity`/`get_mission_type` resolves off a coord-aware resolver without a primary fold, **Then** the gate fails; the arm carries a synthetic-AST non-vacuity self-test.
3. **Lane A:** **Given** the implement-loop Mission has deposited `_DIR_READ_KNOWN_RESIDUALS` pins citing #2185, **When** this Mission routes each site, **Then** the matching pin is removed in the same change and the ratchet stays green. **Lane B:** the existing scanner cannot flag identity reads, so **no #2186 pin pre-exists** — the new arm (FR-007) and the Lane B routing **co-land in this Mission** (gate-unmask-cannot-self-validate: the arm and its remediation ship together, validated by a pre-merge full-gate dry run).

### Edge Cases

- **Mixed PRIMARY+STATUS single resolver call** (`merge/executor.py`, `merge/done_bookkeeping.py`, `lanes/recovery.py:356`): a single `feature_dir` feeds both a PRIMARY leg and a STATUS leg. Splitting must route only the PRIMARY leg and leave the STATUS leg coord-aware — never collapse both onto PRIMARY (would break C-001 status semantics).
- **Ambiguous / coord-deleted handle**: routing must preserve the structured hard-fail (`MissionSelectorAmbiguous`, #1848) — no silent fallback (C-002).
- **Flat (non-coord) topology**: PRIMARY routing must be a no-op behavioral change (PRIMARY == primary on flat topology); existing flat-topology tests must stay green.
- **Chicken-and-egg in `worktree_allocator._read_coordination_branch`**: it reads `meta.json` (which lives on PRIMARY) via a coord-aware resolver to *discover* coord — route to `resolve_planning_read_dir(kind=PRIMARY_METADATA)`, which is topology-blind and correct.

## Requirements *(mandatory)*

### Surface Inventory *(authoritative — kinds restated from the real partition)*

**Lane A — #2185 (merge/lanes/core; this Mission owns these files):**

| Site | Real kind(s) | Shape | Route |
|------|--------------|-------|-------|
| `merge/forecast.py:153` (+ uncited `:159` review-artifact preflight) | LANE_STATE (+ WORK_PACKAGE_TASK) | pure PRIMARY | `resolve_planning_read_dir(kind=LANE_STATE / WORK_PACKAGE_TASK)` |
| `merge/executor.py:976,981,997,1003` | PRIMARY_METADATA + LANE_STATE; `feature_dir` also reused as `status_feature_dir` | **mixed** | per-leg split: PRIMARY legs → resolver; status leg stays coord-aware |
| `merge/resolve.py:98` | PRIMARY_METADATA (issue mislabels LANE_STATE) | pure PRIMARY | `kind=PRIMARY_METADATA` |
| `merge/done_bookkeeping.py:237` | WORK_PACKAGE_TASK (issue says meta.json) | **mixed** | WP-path leg → `kind=WORK_PACKAGE_TASK`; remove misleading comment; status-transactional legs unchanged |
| `cli/commands/merge.py:269` | PRIMARY_METADATA (issue mislabels LANE_STATE) | pure PRIMARY | `kind=PRIMARY_METADATA` |
| `lanes/merge.py:68,198` | LANE_STATE | pure PRIMARY | `kind=LANE_STATE` |
| `lanes/recovery.py:356` | LANE_STATE + WORK_PACKAGE_TASK + STATUS | **mixed** | split: lanes/tasks → resolver; events leg coord-aware |
| `lanes/recovery.py:611` | LANE_STATE (issue mislabels WORK_PACKAGE_TASK) | pure PRIMARY | `kind=LANE_STATE` |
| `lanes/worktree_allocator.py:360` | PRIMARY_METADATA (issue mislabels LANE_STATE) | pure PRIMARY | `kind=PRIMARY_METADATA` |
| `core/worktree_topology.py:138,140,141` | PRIMARY_METADATA + LANE_STATE + WORK_PACKAGE_TASK | pure PRIMARY | single swap of `:138` co-resolves all three |

**Lane B — #2186 (identity/telemetry; this Mission owns the command-layer identity class):**

| Site | Read | Impact | Route |
|------|------|--------|-------|
| `cli/commands/next_cmd.py:187,253` | `resolve_mission_identity` (meta.json) | lifecycle record silently swallowed | primary-anchor the identity read |
| `cli/commands/next_cmd.py:631` | `get_mission_type` (meta.json) | **routing**: wrong run type started | `resolve_planning_read_dir`/primary fold |
| `cli/commands/agent/workflow.py:1274,2732` | `resolve_mission_identity` (inline own resolve) | mission_id empty in review-prompt / preflight | clean standalone primary-anchor |
| `cli/commands/agent/workflow.py:1636` | `get_mission_type` — **shared-variable mixed** (reuses `feature_dir` from `:1387` that also feeds coord-aware review context `:1388`/sub-artifact `:1620`) | research-branch type miss | needs its **own** primary-anchored variable — NOT a `feature_dir` re-point |
| `implement.py:1389` | `resolve_mission_identity` — **shared-variable**, correct only via the `:1018` fallback | identity drop once fallback retired | give it its **own** anchor so it survives fallback removal |

> **Squad-verified ownership (architect lens):** the `workflow.py` identity legs are genuinely the out-of-loop #2186 class — the implement-loop Mission disclaims this class (its C-009/C-008) and its ROUTE/KEEP lines (`:2110/2116/2121/2124`, review-cycle `:2610/2647`, KEEP `:1015`) are **line-disjoint** from these identity legs. So they STAY in this Mission. **But:** they live *inside* functions the implement-loop Mission rewrites, so (1) all Lane B line citations MUST be **re-resolved against post-implement-loop-merge `main`** before editing (C-SEQ); and (2) the **plan must emit a definitive per-site ROUTE / KEEP / owned-by-implement-loop table** covering every Lane B site, cross-checked against the implement-loop Mission's actual ROUTE+KEEP list — no "verify later" deferral, no site left in the gap between the two missions (FR-005).

### Functional Requirements

| ID | Title | User Story | Priority | Status |
|----|-------|------------|----------|--------|
| FR-001 | Route pure-PRIMARY Lane A sites onto `resolve_planning_read_dir(kind=...)` by real kind | US1 | High | Open |
| FR-002 | Per-leg split mixed Lane A sites (`executor` — squad-confirmed `feature_dir`→`run.feature_dir`→`status_feature_dir` at `:503`/`:560`; `done_bookkeeping`; `recovery:356`): PRIMARY legs → resolver, STATUS legs stay coord-aware; keep `done_bookkeeping` status-transactional legs on the **primary** (meta-bearing) dir | US1 | High | Open |
| FR-003 | Remove the self-contradicting "do not use the read-path resolver" comment in `done_bookkeeping.py` and route the WP-path leg | US1 | Medium | Open |
| FR-004 | Primary-anchor the `next_cmd.py` identity/type reads (`:187`, `:253`, `:631`) | US2 | High | Open |
| FR-005 | Emit (at plan) a **complete per-site ROUTE/KEEP/owned-by-implement-loop table** for every Lane B site, cross-checked against the implement-loop ROUTE+KEEP list and re-resolved against post-merge `main`; route the genuinely-owned probes — incl. the **shared-variable mixed** sites (`workflow.py:1636`, `implement.py:1389`) with their **own** primary anchor (not a `feature_dir` re-point) so they survive fallback removal | US2 | High | Open |
| FR-006 | **Verify** the implement-loop Mission's inherited whole-`src` dir-read scan scope covers `merge/`/`lanes/`/`core/` and that the #2185 pins are present on the branch base; extend scope only if it regressed (do NOT re-add scope already owned by implement-loop FR-007) | US3 | Medium | Open |
| FR-007 | Build a **command-layer (`cli/commands/`-scoped) identity-read scan arm**: flag `resolve_mission_identity`/`get_mission_type` resolved off a coord-aware resolver without a primary fold; ship a committed synthetic-AST non-vacuity self-test. Scope bounded to the command layer so it does not red-CI on out-of-scope strangers (`sync/`, `acceptance/`, `policy/`, `orchestrator_api/` — those are follow-on) | US3 | High | Open |
| FR-008 | **Lane A:** drain each `_DIR_READ_KNOWN_RESIDUALS` pin the implement-loop Mission deposited for #2185 in the same change that routes the site. **Lane B:** no #2186 pin pre-exists (scanner is blind to identity reads) — FR-007's arm and the Lane B routing co-land in this Mission, validated by a pre-merge full-gate dry run | US3 | High | Open |
| FR-009 | Add a coord-topology **merge/recovery/topology integration test** on an **extended `build_coord`**: husk `meta.json` carries a sentinel identity ≠ PRIMARY, and production-shaped `lanes.json` + `tasks/` are seeded PRIMARY-only (post-worktree-add) with an assertion the husk lacks them — so a husk-landing read returns observably-wrong data and reverting a routed read to coord-aware FAILS the test (real `git worktree`, no stubs) | US1 | High | Open |
| FR-010 | Recompute `ROUTED_CANONICALIZER_FLOOR` strictly-below the post-fix live census, backed by a before/after canonicalizer census recorded in the WP (unconditional — no "only if it shifts" escape hatch) | US3 | Medium | Open |
| FR-011 | **Pre-flight:** assert the `_DIR_READ_KNOWN_RESIDUALS` set on the branch base actually contains the #2185 pins before any Lane A drain begins (otherwise FR-008/SC-004 are vacuously satisfiable) | US3 | High | Open |

### Non-Functional Requirements

| ID | Title | Requirement | Category | Priority | Status |
|----|-------|-------------|----------|----------|--------|
| NFR-001 | No STATUS-read regression | Every STATUS-partition read (`status.events.jsonl`, status surface) remains coord-aware; zero STATUS legs re-routed to PRIMARY (asserted by tests) | Reliability | High | Open |
| NFR-002 | No silent fallback | Ambiguous/coord-deleted handles keep the structured hard-fail (`MissionSelectorAmbiguous`, #1848); no new best-effort swallow | Reliability | High | Open |
| NFR-003 | Flat-topology behavioral parity | On non-coord topology the change is a no-op; existing flat-topology merge/lanes/next tests stay green | Compatibility | High | Open |
| NFR-004 | Integration over stubs | The #2185 acceptance test drives real code against a real `git worktree` coord fixture; unit stubs handing in a primary dir directly are not accepted as proof | Test Integrity | High | Open |

### Constraints

| ID | Title | Constraint | Category | Priority | Status |
|----|-------|------------|----------|----------|--------|
| C-001 | STATUS stays coord-aware | STATUS-partition reads must remain on the coord-aware resolver; only PRIMARY-partition legs route | Technical | High | Open |
| C-002 | Resolver consumed, not re-authored | This Mission only *consumes* `resolve_planning_read_dir` / `primary_feature_dir_for_mission` / `_canonicalize_primary_read_handle`; it must not edit resolver internals (mirror implement-loop C-003/C-007) | Technical | High | Open |
| C-003 | Strategy consistency | Identity routing must match the implement-loop Mission's chosen seam model (handle-blind primitive + caller-side canonicalization; no silent fallback) | Technical | High | Open |
| C-009-mirror | Surface exclusivity | This Mission owns ONLY `merge/`, `lanes/`, `core/worktree_topology` (#2185) + the `meta.json` identity-read class incl. `next_cmd.py` (#2186). It must NOT touch the implement-loop ROUTE surface (`tasks.py`, `workflow.py` route legs, `tasks_dependency_graph.py`, `workspace/context.py`, etc.) — the inverse of the implement-loop C-009 | Technical | High | Open |
| C-EXCL-2167 | Legacy reader untouched | The repo-root `scripts/tasks/` pre-3.0 legacy reader is **#2167** — pin-and-cite only; never route or delete | Technical | High | Open |
| C-EXCL-FALLBACK | Do not remove the fallback | This Mission adds guards so the `implement.py:1018` primary-anchor fallback *can* be retired later; it does NOT remove the fallback (separate follow-on) | Technical | High | Open |
| C-SEQ | Landing sequence | Land after the implement-loop Mission deposits the #2185 pins + whole-`src` scanner widening (gate visibility + Lane A pin hand-off); branch from / rebase onto post-implement-loop-merge main, then re-resolve all line citations and (FR-011) assert the #2185 pins are present before draining. Lane B builds its own detector and routes in-mission (no inherited #2186 pin). Spec/plan proceed in parallel now; landing serializes after implement-loop | Process | High | Open |

### Key Entities

- **`resolve_planning_read_dir(repo_root, slug, *, kind)`** — kind-aware seam (`missions/_read_path_resolver.py`); PRIMARY kinds fold the handle + resolve topology-blind, STATUS kinds stay coord-aware.
- **`primary_feature_dir_for_mission` + `_canonicalize_primary_read_handle`** — handle-blind PRIMARY primitive + caller-side canonicalizer pairing.
- **`MissionArtifactKind`** — partition authority (`is_primary_artifact_kind`): PRIMARY = META/LANE_STATE/WORK_PACKAGE_TASK; STATUS = STATUS_STATE/ACCEPTANCE_MATRIX/ISSUE_MATRIX.
- **`_DIR_READ_KNOWN_RESIDUALS` + dir-read scanner** (`tests/architectural/test_gate_read_literal_ban.py`) — the ratchet. Lane A dir-join coverage is inherited from implement-loop (FR-006 verify-only); the command-layer **identity-read arm is net-new here** (FR-007); #2185 pins drained as routed (FR-008/FR-011).
- **`build_coord` coord fixture** (`tests/specify_cli/write_side/topology_fixtures.py`) — real `git worktree` topology for the integration test.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: On the **divergent** `build_coord` fixture (PRIMARY-only `lanes.json`/`tasks/`, husk lacks them), the merge/recovery/topology integration test is green and **fails** if any routed Lane A read is reverted to the coord-aware resolver (the husk has no such artifact → observable failure).
- **SC-002**: On a coord topology whose husk `meta.json` carries a sentinel identity ≠ PRIMARY, lifecycle records are written with the **PRIMARY** `mission_id` and `get_mission_type` returns the PRIMARY type (Lane B) — reverting to coord-aware surfaces the sentinel/default and fails the test. Zero silent telemetry/routing drops.
- **SC-003**: 100% of the Surface Inventory sites are routed by their *real* kind; every STATUS leg stays coord-aware (NFR-001) — no over-routing.
- **SC-004**: The new command-layer identity-read arm (with its synthetic-AST non-vacuity self-test) flags an injected unguarded identity probe and the inherited whole-`src` scan flags an injected PRIMARY-off-coord dir-join in `merge/`/`lanes/`/`core/`; all #2185 `_DIR_READ_KNOWN_RESIDUALS` pins are drained (FR-008/FR-011); `ROUTED_CANONICALIZER_FLOOR` recomputed strictly-below the post-fix census (FR-010).
- **SC-005**: `ruff` + `mypy` clean on all touched surfaces; full `tests/architectural/` green (incl. no new un-pinned identity-arm strangers — arm scoped to `cli/commands/`); flat-topology parity preserved (NFR-003).

## Traceability

- **Epic (parent, reference-only — never claim/close):** #2160
- **Originating issue:** #2115 (claimed by the implement-loop Mission; closes when it lands)
- **This Mission addresses:** **#2185** (Lane A) + **#2186** (Lane B)
- **Sibling in-loop Mission (boundary partner):** `implement-loop-coord-authority-completion-01KW2E7A` — C-009 forbids it from these surfaces; this Mission is its inverse
- **Cause:** #2106 (merged) — kind-aware write-surface placement
- **Explicitly excluded:** #2167 (repo-root `scripts/tasks/` legacy reader — pin-and-cite only); removal of the `implement.py:1018` fallback (separate follow-on)
- **Sequencing:** lands after the implement-loop Mission (pin hand-off + hardened scanner + recomputed resolution-gate floor)
