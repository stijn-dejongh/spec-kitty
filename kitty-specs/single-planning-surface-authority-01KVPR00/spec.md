# Spec: Single planning-surface authority via a MissionTopology SSOT

**Mission**: `single-planning-surface-authority-01KVPR00`
**Type**: software-dev (architectural seam + structural convergence + new command)
**Driver issues**: #2069 (MissionTopology SSOT seam — *goes first*), #1716 (single surface authority), #1890 (phantom→real worktree-repair verb) · structurally closes #2062, #2063, #2064 · parent epic #2007 / execution-context epic #1619

> **REVISION NOTE (2026-06-22).** This spec was revised after design ticket **#2069**
> finalized. The earlier draft of this mission *adopted* the existing write authority
> (`resolve_placement_only`) and *band-aided* the read path (thread a declared-coord
> signal into a disk-stat heuristic). The operator's decision supersedes that: **the new
> design lands first**, and the #2062/#2063/#2064 family is fixed **structurally** — the
> read path consults an **explicitly stored mission topology**, not a re-inference from
> on-disk worktree existence. Operator's binding principle: *"if storing topology re-opens
> #2062, that proves our prior #2062 fix was non-structural."* (C-004). The codebase-wide
> `CommitTargetKind` eradication + universal resolver adoption are **carved to a follow-on
> Mission B** (C-007) — this mission lands the seam, the structural surface-coherence fix,
> and the independent verb/guard/campsite work.

## Overview

Spec Kitty decides *where* a mission's planning artifacts live (PRIMARY checkout vs
COORDINATION worktree) by **re-inferring the mission's shape, ad-hoc, at many seams** from
scattered on-disk and git signals. A mission can take one of four shapes across the
orthogonal **coordination × lanes** grid, but **no shape is a first-class, stored value**:
each consumer re-derives a slice (`coordination_branch is None ⇒ FLATTENED`,
`read_lanes_json(...)`, `CoordState.MATERIALIZED` from a `stat`), the slices drift, and the
artifact written through one inference is read back through another. That drift **is** the
#2062/#2063/#2064 coord/primary desync class.

This mission lands the **#2069 design** as the structural fix:

1. **Name the shape.** A mission-level `MissionTopology` enum makes the coord×lanes
   cross-product four named values.
2. **Store it, don't guess it.** `topology` is minted into `meta.json` at mission create
   and **read** thereafter — never re-inferred from disk. Legacy missions are backfilled
   once.
3. **One resolver, pure.** `resolve_context_for_mission(mission_id, topology) ->
   ExecutionContext` is a **pure projection** over the existing single construction door
   (`build_execution_context`); the imperative shell parses/persists `meta.json` and passes
   `id + topology`. The per-call derivation heuristic is retired; `CommitTargetKind` becomes
   a derived per-ref projection (deleted at the touched sites).
4. **Adopt structurally.** The planning read/write commands resolve their surface through
   the seam, so a flattened mission resolves PRIMARY because its **stored** topology says so
   — *not* because a band-aid out-voted an on-disk husk. #2062/#2063/#2064 close at the root.

The mission also lands two independent pieces the earlier scope already owned: the **real
`agent worktree repair` verb** (#1890 — recreate a missing coord worktree, prune an orphaned
one) and the **command-reference guard** that would have caught the phantom command (#2008),
plus the active **#1970 campsite** folds on every touched surface.

**Campsite-cleaning directive #1970 is ACTIVE for this mission and every WP** (operator
mandate): adjacent debt in a touched surface is REMEDIATED in-slice, not deferred (C-001;
campsite FRs FR-015..FR-022).

## Domain Language

- **MissionTopology** (canonical) — the mission-level enum naming the four shapes of the
  **coordination × lanes** grid as one stored value:
  `SINGLE_BRANCH` (no coord, no lanes), `LANES` (no coord, lanes), `COORD` (coord, no
  lanes), `LANES_WITH_COORD` (coord, lanes). It classifies the *whole mission shape*, unlike
  the per-ref `CommitTargetKind`.
- **FLATTENED** — a **historical/metadata flag**, NOT a topology value. A mission that
  *was* coord and had its `coordination_branch` dropped is now `SINGLE_BRANCH`/`LANES` with
  a `flattened` provenance mark; the residual `-coord` husk is FR-012's prune concern.
- **Stored topology** — the `topology` field in `meta.json`: authoritative, read at resolve
  time, never re-inferred from worktree existence or `coordination_branch is None`.
- **`resolve_context_for_mission`** — the pure SSOT resolver
  `(mission_id, topology: MissionTopology) -> ExecutionContext`; a thin projection over
  `build_execution_context` (the sole construction door), with no filesystem I/O.
- **ExecutionContext / ActionContext** — the real op-composite value object
  (`src/mission_runtime/context.py:177`) bundling the branch refs, primary/coord surfaces,
  status surfaces, artifact placement, and identity fragments. (#2069 corrected the
  operator's working name "MissionContext" — that type does not exist.)
- **Orphaned coord worktree / husk** — a `.worktrees/<slug>-<mid8>-coord/` directory left on
  disk after flatten/teardown; must NEVER be a read authority. With stored topology it
  simply isn't consulted.
- **Recreate-or-prune** — the `worktree repair` verb: re-materialize a *missing* coord
  worktree (via `CoordinationWorkspace.resolve()`) and remove an *orphaned* one.

## User Scenarios & Testing

### Primary — a mission's shape is a stored value, resolved once
At `mission create`, the mission's `MissionTopology` is recorded in `meta.json`. Every later
read/write resolves the surface by calling `resolve_context_for_mission(mission_id,
stored_topology)` and reading the returned `ExecutionContext` — no command re-infers the
shape from `coordination_branch is None`, `lanes.json` presence, or a worktree `stat`.

### Primary — a flattened mission never reads a stale coord worktree (#2062, structural)
A mission flattened mid-flight (its `meta.json` topology is now `SINGLE_BRANCH`/`LANES`, with
a `flattened` provenance flag) with a stale `-coord` worktree still on disk resolves its
status from the **PRIMARY** surface on **all read legs** for **every** handle form
(`<slug>-<mid8>`, bare-mid8, full ULID, bare human slug) — because the **stored** topology
drives the read path, so the on-disk husk is structurally irrelevant. The dep-gate, kanban,
and review-claim never report a stale `planned` lane.

### Primary — planning artifacts read back from the surface they were written to (#2063)
An operator runs `/spec-kitty.specify` then `/spec-kitty.tasks` on a coord-topology mission.
`spec.md` is committed through the seam-resolved placement and lands on the surface the next
command reads. `/tasks` and `finalize-tasks --validate-only` both see `spec.md` and the WP
files — no "spec.md not found" / "Tasks directory not found" divergence.

### Primary — requirement coverage agrees across commands (#2064)
`map-requirements` (reports full coverage) and the following `finalize-tasks --validate-only`
read and write WP `requirement_refs` through the same seam-resolved surface, so finalize
reports **zero** `unmapped_functional_requirements` — the two commands never disagree about
where the WP frontmatter lives.

### Primary — recovery commands actually exist and work (#1890)
When the resolver/doctor diagnose a missing or orphaned coord worktree, the operator runs
`spec-kitty agent worktree repair --mission <slug>`: a **registered** command that recreates
a missing coord worktree and prunes an orphaned one. No operator-facing recovery hint names
a command that does not exist.

### Exception / edge cases
- **create→first-write window** (topology `COORD`/`LANES_WITH_COORD` declared, coord
  worktree not yet materialized) still resolves PRIMARY on every leg — the #1718 contract is
  preserved (regression-guarded). The stored topology says "coord", but the transient
  not-yet-materialized state is discriminated by the existing probe, NOT by the enum.
- **coord-deleted** (declared coord branch deleted from git) still hard-fails
  `CoordinationBranchDeleted` (#1848 data-loss carve-out) — unchanged. These transient
  on-disk×git states are **orthogonal to the 4 enum cells** and are NOT subsumed by stored
  topology (C-006).
- **Legacy / no-`mid8` / no-`topology` missions** are backfilled once; until backfilled,
  the shell falls back to the legacy derivation exactly once to *compute and persist* the
  topology, then reads the stored value (FR-003).
- A `worktree repair` on a mission whose stored topology has no coordination (`SINGLE_BRANCH`
  / `LANES`) is a benign no-op with a clear message (not an error).

## Functional Requirements

### A. Topology SSOT seam — the foundation (lands first, #2069)

| ID | Requirement | Status |
| --- | --- | --- |
| FR-001 | **`MissionTopology` enum.** Add a mission-level enum `MissionTopology {SINGLE_BRANCH, LANES, COORD, LANES_WITH_COORD}` in `src/mission_runtime/context.py`, naming the orthogonal **coordination × lanes** 2×2 grid as one value. `FLATTENED` is NOT an enum member — it is a separate historical/metadata flag (provenance), never a shape value. The enum is the single place the lanes-vs-coord cross-product is named. | proposed |
| FR-002 | **Store the topology in `meta.json`.** `topology` MUST be minted into `meta.json` at `mission create` (`src/specify_cli/core/mission_creation.py`) and READ thereafter — never re-inferred from disk/git at resolve time. The stored value is authoritative; a `flattened` provenance flag records history without changing the shape value. | proposed |
| FR-003 | **Backfill legacy missions once.** Add `spec-kitty migrate backfill-topology` (mirroring the `backfill-identity` precedent) that computes each legacy mission's topology from the current signals and PERSISTS it to `meta.json`, plus a `spec-kitty doctor topology --json` audit. **Sequencing landmine (dogfooding):** THIS mission's own `meta.json` MUST be backfilled with its `topology` BEFORE any caller reads the stored field. Until a mission is backfilled, the shell computes-and-persists the topology exactly once via the legacy derivation, then reads the stored value. | proposed |
| FR-004 | **Pure `resolve_context_for_mission` SSOT resolver.** Add `resolve_context_for_mission(mission_id: str, topology: MissionTopology) -> ExecutionContext` on the canonical `mission_runtime` seam as a **PURE** projection over the existing single construction door `build_execution_context` (functional core / imperative shell): it performs NO filesystem or git I/O; the shell parses/persists `meta.json` and passes `id + topology`. `topology` is an authoritative input (optional input-assertion: fail-closed on a supplied-vs-resolved mismatch). The per-call derivation heuristic `_resolve_coordination_branch`/`resolution.py:705-718` (`coordination_branch is None ⇒ FLATTENED`) MUST be retired in favor of the stored value. | proposed |
| FR-005 | **Delete `CommitTargetKind` at the touched sites → derived projection.** `CommitTargetKind` MUST become a `MissionTopology`-derived per-ref projection (a `routes_through_coordination(...)` predicate). The ≤8 `.kind is COORDINATION` branch sites in the surfaces this mission touches MUST be re-expressed against the derived projection; the remaining codebase-wide `CommitTargetKind` references are CARVED to Mission B (C-007). No site may independently re-infer the per-ref kind. | proposed |

### B. Structural surface-coherence adoption (closes #2062/#2063/#2064 at the root)

| ID | Requirement | Status |
| --- | --- | --- |
| FR-006 | **Read path consults the STORED topology (structural #2062).** `missions/_read_path_resolver._resolve_existing_for_slug` (and the read-path legs it feeds) MUST resolve the surface from the seam / stored topology, so `CoordState.MATERIALIZED` (a disk `stat`) is NO LONGER the deciding signal. A mission whose stored topology is `SINGLE_BRANCH`/`LANES` resolves PRIMARY regardless of a stale `-coord` husk on disk. This REPLACES the prior declared-coord band-aid: the on-disk husk is structurally not consulted, so #2062 cannot re-open (C-004). The stale `:263` comment ("No branch is supplied here") documenting the defect as intentional MUST be corrected/removed. | proposed |
| FR-007 | **Single write-surface authority.** Every planning-phase artifact commit (`spec.md`, `plan.md`, `tasks/`, WP `requirement_refs` frontmatter, lifecycle status events) MUST resolve its write destination through the seam (`resolve_context_for_mission` placement projection). No planning command may resolve a write target from the current `HEAD` branch independently (`safe-commit._resolve_commit_target` is the #2063 root). `safe-commit`'s two responsibilities are SEPARATED: mission-aware planning commits resolve via the seam; generic operator-file commits keep their existing behavior (NFR-002). | proposed |
| FR-008 | **`map-requirements` and `finalize-tasks` share one WP-frontmatter surface.** Both commands MUST read/write WP `requirement_refs` through the SAME seam-resolved surface (honoring the documented invariant: planning INPUT artifacts authored on PRIMARY, staged to coord at commit-time). A successful `map-requirements` MUST be visible to the immediately-following `finalize-tasks --validate-only` (zero `unmapped_functional_requirements`). The READ surface (`map-requirements`' `read_all_wp_requirement_refs` vs finalize's own dir resolution) MUST be consolidated to one place; `compute_coverage` is already single-source — do NOT chase the coverage math. | proposed |
| FR-009 | **Status-event emission resolves its write surface from the seam.** Every `status.emit.emit_status_transition` call site MUST pass a `feature_dir` resolved by the seam, not an ad-hoc per-caller path — so dep-gate / kanban / review-claim status reads and `move-task` writes converge on one surface (the #2062 status-read leg). | proposed |
| FR-010 | **Differential gate: stored-topology equivalence + retained on-disk legs.** `tests/missions/test_surface_resolution_equivalence.py` MUST (a) add a **pure** input→output cell feeding `(mission_id, topology)` for all four `MissionTopology` values and asserting the returned `ExecutionContext` surface fields; AND (b) RETAIN the on-disk `flattened-stale-coord` topology × every handle form (primary meta `SINGLE_BRANCH`/`LANES` + a stale `-coord` worktree on disk) asserting all legs return PRIMARY — until those legs are deleted. The existing `type(a) is type(b)` AND `error_code` assertion MUST NOT be weakened. The pure cell is an ADDITIONAL proof, never a REPLACEMENT for the live on-disk proof (C-002, NFR-001). | proposed |
| FR-011 | **(Campsite #1970) Collapse `is_committed` 3-leg OR.** Once the read/write surface is structurally single (FR-006/FR-007 via stored topology), `missions/_substantive.is_committed` (`:317-412`) MUST reduce from a 3-surface OR to a single-surface check on the resolved placement ref; the multi-surface diagnostics workaround is removed. Gated on the FR-010 live convergence proof (NFR-001/C-002) — the 3-leg OR is a load-bearing workaround for the surface split and must not be collapsed before the split is structurally gone. | proposed |

### C. Independent work — verb, guard, de-godding, campsite (survive the revision)

| ID | Requirement | Status |
| --- | --- | --- |
| FR-012 | **Real `worktree repair` verb (#1890).** Register `spec-kitty agent worktree repair --mission <slug>` that **recreates** a missing coord worktree (via `CoordinationWorkspace.resolve()`) and **prunes** an orphaned one. Repoint every operator-facing recovery hint to a command that actually fixes its failure class (husk → `doctor workspaces --fix`; coord-missing/empty/orphaned → `worktree repair`); amend ADR `2026-06-19-1`; reconcile the Python/ADR copies to the canonical `SKILL.md` answer. No remediation string may name an unregistered command. | proposed |
| FR-013 | **Command-reference guard (#2008).** An architectural test MUST scan `src/specify_cli/**/*.py` string literals and `architecture/**/*.md` (ADRs) for `spec-kitty <tokens>` invocations and assert each names a REGISTERED Typer command (reuse the `_build_live_app`/registered-path machinery in `test_docs_cli_reference_parity.py`), with a planted-phantom self-test. Allowlist entries require a rationale comment. | proposed |
| FR-014 | **`safe-commit` retired from planning prompts.** Planning-artifact commits in all mission-step prompts MUST use the mission-aware `spec-commit`; the charter prompt (`src/doctrine/missions/mission-steps/software-dev/charter/prompt.md:198`) MUST be migrated off `safe-commit`. Generic `safe-commit` is retained for non-mission operator files (do NOT overload it). | proposed |
| FR-015 | **(Campsite #1970) Hoist duplicated recovery hints.** The worktree-repair recovery sentence duplicated 5× in `doctor.py` (`:3092,:3116,:3209,:3225,:3245`) MUST be hoisted to ≤2 named module constants (one per failure class) so no recovery sentence is duplicated ≥3× (Sonar S1192). | proposed |
| FR-016 | **(Campsite #1970) De-pin fakeable / split-brain-codifying tests.** Tests that assert the phantom string (`test_surface_resolver_coord_empty_warning.py:127`, `test_surface_resolver.py:276`, `test_doctor_coordination.py:132`) and tests that codify the coord-vs-primary split as desired (`test_map_requirements_coord.py`, `test_map_requirements_spec_path.py`) MUST be re-pointed to assert the REAL command and **cross-command surface coherence** — no test pins a nonexistent command or the split-brain. | proposed |
| FR-017 | **(Campsite-fold #2066) Surface the parsed FR-ID set on coverage mismatch.** When WP `requirement_refs` don't match `spec.md` FR IDs, `map-requirements` / `finalize-tasks` `--json` MUST emit the parsed FR set so the operator can see actual vs expected IDs. | proposed |
| FR-018 | **(Campsite-fold #1891) Clean `--json` document on the touched commands.** `setup-plan` and `finalize-tasks` `--json` MUST emit a single clean JSON document (no human preamble before the JSON on stdout). Add a regression assert for the already-fixed `map-requirements` `CommitResult` leg; do not re-fix. (`agent action implement --json` is out of scope.) | proposed |
| FR-019 | **(Campsite-fold #2037) Harden the 3 in-surface untrusted-path sinks.** Route the CLI-arg `--mission` path joins at `agent/mission.py` (the setup-plan/finalize-tasks join), `agent/tasks.py:1911`, `cli/commands/merge.py:1126` (3 of #2037's 4 sinks — all in touched surfaces) through `assert_safe_path_segment` / `ensure_within_any` with a negative test each. Leave `decision.py:464` (untouched surface). | proposed |
| FR-020 | **(Campsite-fold #2048, GATED) Retire the dead `mission_read_path` shim.** IF the FR-006 read-path adoption confirms ZERO external consumers of `src/specify_cli/mission_read_path.py`, delete the shim, repoint its test imports, and decrement the backcompat-shim allowlist (9→8). IF consumers remain, LEAVE it and record why. | proposed |
| FR-021 | **(Partial de-godding #2059) Extract the `doctor.py` coord-recovery cluster.** As FR-012 adds the verb + repoints recovery hints, the cohesive worktree/coord-recovery helper cluster in `doctor.py` (~`:3092-3225`, ~5 helpers) MUST be extracted into a sibling `cli/commands/_coord_recovery.py` (mirroring `_doctrine_health.py`) with a `#2059` pointer. REQUIRED in-slice, bounded to that one cluster (no wider `doctor.py` split). | proposed |
| FR-022 | **(Partial de-godding #2056) Extract touched `mission.py` placement/commit helpers → `commit_router.py`.** The placement/commit helpers in `setup_plan` / `finalize_tasks` that this mission edits for seam routing (FR-007/FR-008) MUST be extracted into the canonical `coordination/commit_router.py` seam (#2056) with a pointer. This co-locates with the FR-005 `CommitTargetKind` projection (the `.kind is COORDINATION` branches live there). REQUIRED in-slice, bounded to those helpers (no wider `mission.py` split). | proposed |

## Non-Functional Requirements

| ID | Requirement | Status |
| --- | --- | --- |
| NFR-001 | **Live-evidence convergence proof.** The write/read convergence MUST be proven on a REAL flattened-mid-flight mission repro (the #2062 topology), not by static reading and not solely by the FR-010 pure cell. The differential equivalence gate (incl. the on-disk `flattened-stale-coord` row) MUST be green at every WP boundary. #2062 is NOT marked fixed without a witnessed live repro. | proposed |
| NFR-002 | **No regression of generic `safe-commit`.** `safe-commit`'s legitimate non-mission operator-file commit path MUST remain functional and tested (the two responsibilities are separated, not overloaded). | proposed |
| NFR-003 | **Gate-unmask discipline.** The FR-013 command-reference guard only catches offenders after it lands — it MUST be paired with a full-suite dry-run in this mission and a planted-phantom self-test proving it fails on a planted Python-literal phantom BEFORE reliance. No mission-diff-scoped assertion is shipped to main. | proposed |
| NFR-004 | **Behavior-preserving adoption.** The seam adoption (FR-006/FR-007/FR-009) and the `CommitTargetKind` derivation (FR-005) are behavior-preserving for already-correct topologies (coord-fresh, create-window, single-branch, coord-deleted) — proven by the equivalence gate + the preserved #1718/#1848 guards. | proposed |
| NFR-005 | **Clean static analysis.** All new/changed code passes `ruff` and `mypy` with zero issues/warnings; cyclomatic complexity ≤15; repeated non-trivial literals hoisted (no new S1192). No suppression added to pass. | proposed |
| NFR-006 | **Resolver isolation.** `resolve_context_for_mission` MUST be unit-testable with zero filesystem/git fixtures — feed `(mission_id, topology)`, assert the returned `ExecutionContext` fields. Any FS/git access lives in the imperative shell, never in the resolver. | proposed |

## Constraints

| ID | Constraint | Status |
| --- | --- | --- |
| C-001 | **#1970 campsite-cleaning is ACTIVE for every WP.** Adjacent debt in a touched surface is REMEDIATED in-slice (FR-015..FR-022 and any found in-flight), bounded to mission goals — never deferred with "pre-existing, out of scope". Each WP prompt MUST carry this directive. Partial de-godding is REQUIRED, not optional (FR-021/FR-022): the `doctor.py` coord-recovery cluster → `_coord_recovery.py`, and the touched `mission.py` placement/commit helpers → `commit_router.py`, each bounded to the seam the mission already rewrites + a tracker pointer. NOT a wholesale module split (`tasks.py` gets a pointer only — maxCC 178 risk). | active |
| C-002 | **No close-on-static for #2062.** #2062 stays OPEN until a live flattened-mission repro witnesses all read legs resolving PRIMARY. The FR-010 pure cell ADDS a proof; it does NOT replace the live repro. | active |
| C-003 | **Project over the door, do not rebuild.** `resolve_context_for_mission` MUST be a thin projection over the existing `build_execution_context` construction door (the way `resolve_placement_only` already is — "one authority, two projections"). Do NOT introduce a parallel resolver that re-reads `meta.json`/`lanes.json`/git independently. | active |
| C-004 | **Structural, not symptomatic (binding).** The #2062/#2063/#2064 fix MUST be structural: the read path consults the STORED topology, never re-inferring the shape from on-disk worktree existence. If storing the topology would re-open #2062, that proves a prior fix was a symptom patch — the resolution is to make the read path stop inferring from disk, NOT to re-add a band-aid. | active |
| C-005 | **Linearize shared anchors.** `mission_runtime/context.py` (enum), `mission_runtime/resolution.py` (seam + derivation retirement), `missions/_read_path_resolver.py` (read leg), `core/mission_creation.py` (mint), and `cli/commands/agent/mission.py` (god-module) are shared surfaces — land them on a linearized chain before the disjoint lanes; expected refactor overlap. | active |
| C-006 | **Transient on-disk×git states are NOT subsumed by the enum.** The create-window (#1718, topology=COORD but worktree not yet materialized) and coord-deleted (#1848, declared branch gone) states are orthogonal to the 4 enum cells and MUST stay discriminated by the existing probe (`probe_coord_state` with the branch signal) — the stored topology does not replace them. Preserve `CoordAuthorityUnavailable` / typed errors / `CoordinationBranchDeleted` and the #2065 read-side contract intact. | active |
| C-007 | **Scope split — Mission B carve.** Codebase-wide `CommitTargetKind` eradication (≈152 refs / 41 files beyond the ≤8 touched branch sites) and universal resolver adoption (≈29 `resolve_placement_only` + 28 `resolve_action_context` call sites beyond the touched planning commands) are a follow-on **Mission B** — too large for one mission. THIS mission lands the enum, the stored field + backfill, the pure resolver, the derivation retirement, the `CommitTargetKind` deletion at the ≤8 touched sites, and the structural surface-coherence fix. A Mission-B follow-up tracker ticket MUST be carved. | active |
| C-008 | **No version prescription.** The PO assigns release/patch numbers at release time; frame work as focus/milestone, not a version. | active |

## Success Criteria

- **SC-001** `MissionTopology` exists as a stored `meta.json` value (minted at create,
  backfilled for legacy via `migrate backfill-topology`); no resolve-time path re-infers the
  shape from `coordination_branch is None` or a worktree `stat` — the legacy derivation at
  `resolution.py:705-718` is retired.
- **SC-002** `resolve_context_for_mission(mission_id, topology)` returns a correct
  `ExecutionContext` for all four topology values in a **pure** unit test with **zero** FS/git
  fixtures (NFR-006), and is a projection over `build_execution_context` (no parallel
  resolver — C-003).
- **SC-003** A flattened mission with a stale `-coord` worktree resolves status from the
  PRIMARY surface on **all read legs × all 4 handle forms** (witnessed live; #2062), because
  the stored topology drives the read path (C-004).
- **SC-004** For a coord-topology mission, `spec.md` committed through the planning flow is
  visible to the immediately-following `/spec-kitty.tasks` and `finalize-tasks
  --validate-only` reads — no "spec.md not found" divergence (#2063, witnessed).
- **SC-005** After `map-requirements` reports full coverage, `finalize-tasks --validate-only`
  reports **zero** `unmapped_functional_requirements` for the same mission (#2064, witnessed).
- **SC-006** `CommitTargetKind` is a derived projection of `MissionTopology` at every touched
  site (≤8 branch sites); the differential gate includes both the pure stored-topology cell
  and the on-disk `flattened-stale-coord` row, with the type+error_code assertion unweakened.
- **SC-007** `spec-kitty agent worktree repair --mission <slug>` is a registered command that
  recreates a missing coord worktree and prunes an orphaned one; **every** operator-facing
  recovery hint names a registered command (#1890); the FR-013 guard **fails** on a planted
  Python-literal phantom and finds **zero** unregistered `spec-kitty` invocations.
- **SC-008** `is_committed` is reduced to a single-surface check; the full test suite is green
  including the preserved #1718/#1848 guards (NFR-004); the Mission-B carve ticket exists.

## Key Entities

- **MissionTopology** — `src/mission_runtime/context.py`; the stored 4-cell mission-shape enum.
- **`topology` (meta.json field)** — the stored, authoritative shape value (+ `flattened`
  provenance flag).
- **`resolve_context_for_mission`** — the pure SSOT resolver projecting `build_execution_context`.
- **ExecutionContext / ActionContext** — `context.py:177`; the returned op-composite VO.
- **`CommitTargetKind`** — retired at the touched sites into a `MissionTopology`-derived
  per-ref projection (`routes_through_coordination`).
- **Differential equivalence gate** — `test_surface_resolution_equivalence.py`; extended with
  the pure stored-topology cell + the retained on-disk flattened-stale-coord row.

## Assumptions

- `build_execution_context` / `_assemble_core_fragments` is genuinely the single construction
  door (verified by mission `01KVGCE8`/`01KVN754`); `resolve_context_for_mission` projects it,
  it does not redesign it.
- The four `MissionTopology` cells exhaustively cover the coord×lanes grid; FLATTENED is
  representable as `SINGLE_BRANCH`/`LANES` + a provenance flag without information loss.
- `CoordinationWorkspace.resolve()` is the canonical coord-worktree materializer `spec-commit`
  already uses on demand; the new `worktree repair` verb forwards to it.
- The transient create-window (#1718) and coord-deleted (#1848) states require a probe the
  stored topology does not encode — they remain the probe's responsibility (C-006).
- The PR-bound coordination topology of THIS mission is itself a dogfooding hazard for the
  exact bugs under fix; its `meta.json` MUST be topology-backfilled before any caller reads
  the field (FR-003) — flatten/coord-friction is expected during implement (carry NFR-001).

## Issue Matrix References

#2069 (design driver — MissionTopology seam, goes first), #1716 (single surface authority
epic facet), #1890 (driver — phantom→real verb), #2062 (read-path leg — OPEN, no close
without live repro; closed STRUCTURALLY here), #2063, #2064, #2007 (parent epic), #1619
(execution-context epic), #1970 (campsite directive — process reference). **Campsite-advanced
(brownfield squad, in-surface cheap folds):** #2066 (FR-017), #1891 partial (FR-018), #2037
partial — 3/4 sinks (FR-019), #2048 gated (FR-020). **Partial de-godding REQUIRED:** #2059
doctor coord-recovery cluster → `_coord_recovery.py` (FR-021), #2056 mission.py
placement/commit helpers → `commit_router.py` (FR-022). **Carved to Mission B (C-007):**
codebase-wide `CommitTargetKind` eradication + universal `resolve_context_for_mission`
adoption (≈152 refs/41 files; 29+28 call sites) — a follow-on tracker ticket. **Explicitly
left out** (own mission-sized efforts): #1357 (lock redesign), #2049 (broad audit), #1887
(merge path), #2031, #2058 + the *full* `doctor.py`/`mission.py`/`tasks.py` decompositions,
the v3.3 `--to-branch` / `next/` shim deprecations (not due at 3.2.x).
