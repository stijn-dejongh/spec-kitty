# Implementation Plan: Single planning-surface authority via a MissionTopology SSOT

**Mission**: `single-planning-surface-authority-01KVPR00`
**Branch**: `feat/single-planning-surface-authority` (planning base = merge target; later PR to `main`)
**Driver**: #2069 (MissionTopology seam — *goes first*) + #1716 + #1890 · structurally closes #2062 / #2063 / #2064 · parent epic #2007 / #1619 · campsite #1970

> **REVISION NOTE (2026-06-22).** This plan was rewritten after design ticket #2069
> finalized and the operator ruled "the new design goes first." The earlier plan adopted
> the existing `resolve_placement_only` authority and band-aided the read path. This plan
> instead lands the **MissionTopology SSOT seam** as the foundation and makes the
> #2062/#2063/#2064 fix **structural** — the read path consults a **stored** topology, never
> re-inferring shape from on-disk husk existence (C-004). Codebase-wide `CommitTargetKind`
> eradication + universal resolver adoption are carved to a follow-on **Mission B** (C-007).

## Summary

Land the **#2069 design** as the structural fix for the coord/primary surface-desync class:
name the four mission shapes (`MissionTopology`), **store** the shape in `meta.json`, resolve
it **once** through a **pure** `resolve_context_for_mission(mission_id, topology) ->
ExecutionContext` projection over the existing `build_execution_context` door, and retire the
per-call derivation heuristic + delete `CommitTargetKind` (at the ≤8 touched sites). Then the
planning read/write commands adopt the seam, so a flattened mission resolves PRIMARY because
its **stored** topology says so — not because a band-aid out-voted an on-disk husk. The
mission also lands the real `agent worktree repair` verb (#1890), the command-reference guard
(#2008), and the active #1970 campsite folds. **This is a projection over an SSOT door (C-003)
— not a new resolver.** #1970 campsite-cleaning is active for every WP.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: typer, rich, ruamel.yaml (CLI surfaces); pytest, pytest-xdist, mypy, ruff (gates); `spec_kitty_events` / `spec_kitty_tracker` public imports only (shared-package boundary)
**Storage**: filesystem — `kitty-specs/<slug>/` (primary checkout) and `.worktrees/<slug>-<mid8>-coord/` (coordination worktree); `status.events.jsonl` append-only log; `meta.json` identity + **new `topology` field** (stored mission shape)
**Testing**: pytest (`tests/`), parallel `-n auto --dist loadfile` with per-worker HOME isolation; the differential equivalence gate `tests/missions/test_surface_resolution_equivalence.py` (extended with a **pure** stored-topology cell + the retained on-disk flattened-stale-coord row); architectural gates under `tests/architectural/`
**Target Platform**: Linux/macOS dev CLI (Spec Kitty toolkit)
**Project Type**: single (Python CLI package `src/specify_cli` + `src/mission_runtime`)
**Performance Goals**: no measurable regression — the pure resolver removes per-call git/derivation on the resolve hot-path (stored topology read once); no new subprocess on the common case
**Constraints**: ruff + mypy zero-issue on new/changed code; cyclomatic complexity ≤15; no new S1192; behavior-preserving adoption for already-correct topologies; live-evidence proof for #2062; the resolver is PURE (no FS/git I/O — NFR-006)
**Scale/Scope**: the topology SSOT seam (enum + stored field + backfill migration + pure resolver + CommitTargetKind deletion at ≤8 sites) + structural surface adoption across ~6 planning surfaces + the independent verb/guard/de-godding/campsite work. Refactor mission with expected linearized shared-surface overlap. Codebase-wide CommitTargetKind eradication + universal adoption are CARVED to Mission B (C-007).

## Charter Check

*GATE: software-dev-default, compact mode (DIR-001..013). Re-checked post-#2069-design.*

- **DIR-001 (architectural integrity / separation of concerns)**: PASS — the mission names
  the mission-shape cross-product as one stored value and resolves it through one pure door,
  collapsing N ad-hoc per-seam inferences. The resolver is a pure functional core; FS/git
  live in the imperative shell (NFR-006). No parallel resolver (C-003).
- **DIR (testing standards)**: PASS — the differential gate gains a pure stored-topology cell
  AND retains the on-disk flattened-stale-coord row (FR-010); the new guard carries a
  planted-phantom self-test (NFR-003); the pure resolver is unit-testable with zero fixtures.
- **DIR (canonical sources / no improvisation)**: PASS — project over `build_execution_context`;
  reuse `CoordinationWorkspace.resolve()`, the `backfill-identity` migration precedent, and
  the `test_docs_cli_reference_parity` registered-path machinery; reconcile docs/ADR to the
  canonical `SKILL.md`.
- **Terminology canon**: the doctrine-prompt edit runs `tests/architectural/test_no_legacy_terminology.py` pre-push.
- No charter conflicts; no gate waivers required.

## Project Structure

### Documentation (this mission)
```
kitty-specs/single-planning-surface-authority-01KVPR00/
├── spec.md              # committed (1b8340c — revised seam-first)
├── plan.md              # this file
├── research.md          # Phase 0 (decisions/rationale; #2069 design record)
├── data-model.md        # Phase 1 (MissionTopology enum, stored field, ExecutionContext projection)
├── quickstart.md        # Phase 1 (the live flattened-mission repro + pure-resolver unit recipe)
├── research/observations.md  # dogfooding observations (carried)
└── tasks.md             # Phase 2 (/spec-kitty.tasks — NOT created here)
```

### Source Code (repository root) — surfaces touched
```
# --- A. Topology SSOT seam (foundation) ---
src/mission_runtime/context.py                     # NEW MissionTopology enum; CommitTargetKind→derived (anchor)
src/mission_runtime/resolution.py                  # resolve_context_for_mission projection; retire :705-718 derivation (anchor)
src/specify_cli/core/mission_creation.py           # mint topology into meta.json at create
src/specify_cli/migrate/<backfill_topology>.py     # NEW backfill migration (backfill-identity precedent)
src/specify_cli/cli/commands/doctor.py             # NEW `doctor topology` audit (+ FR-015 hoist, FR-021 extract)
# --- B. Structural surface-coherence adoption ---
src/specify_cli/missions/_read_path_resolver.py    # read path consults stored topology (#2062 structural; anchor)
src/specify_cli/cli/commands/safe_commit_cmd.py    # seam-resolved write target (FR-007)
src/specify_cli/cli/commands/spec_commit_cmd.py    # seam-resolved write target (FR-007)
src/specify_cli/cli/commands/agent/tasks.py        # map-requirements one surface (FR-008)
src/specify_cli/cli/commands/agent/mission.py      # setup_plan/finalize_tasks seam routing (anchor, god-module)
src/specify_cli/status/emit.py                     # event write-surface via seam (FR-009)
src/specify_cli/missions/_substantive.py           # is_committed single-surface collapse (FR-011)
tests/missions/test_surface_resolution_equivalence.py  # pure cell + retained on-disk row (FR-010)
# --- C. Independent (verb, guard, de-godding, campsite) ---
src/specify_cli/cli/commands/agent/worktree.py     # NEW recreate-or-prune verb (FR-012)
src/specify_cli/cli/commands/_coord_recovery.py    # NEW doctor coord-recovery cluster extract (FR-021)
src/specify_cli/coordination/surface_resolver.py   # recovery strings repoint (FR-012)
src/specify_cli/coordination/commit_router.py      # mission.py placement/commit helpers extract (FR-022)
architecture/3.x/adr/2026-06-19-1-...md            # ADR amend (FR-012)
src/doctrine/missions/mission-steps/software-dev/charter/prompt.md  # safe-commit→spec-commit (FR-014)
tests/architectural/test_command_references.py     # NEW command-reference guard (FR-013)
cli/commands/merge.py                              # FR-019 path-sink (1126)
```

## Complexity Tracking

No charter-gate violations to justify. Two structural risks:
1. **`is_committed` 3-leg OR collapse (FR-011)** is a load-bearing workaround; its collapse
   is gated on the structural surface-singularity (FR-006/FR-007 via stored topology) AND a
   live flattened-mission repro (NFR-001) — sequenced after the seam + adoption, never before.
2. **Backfill sequencing (FR-003)** — THIS mission's own `meta.json` must be topology-backfilled
   BEFORE any caller reads the stored field, else the dogfooding loop reads an absent field.

## Implementation Concern Map

Linearization law (NFR refactor overlap): the shared anchors — `mission_runtime/context.py`
(enum + CommitTargetKind), `mission_runtime/resolution.py` (seam + derivation retirement),
`missions/_read_path_resolver.py` (read leg), `core/mission_creation.py` (mint),
`cli/commands/agent/mission.py` (god-module) — are touched by multiple ICs and MUST land on a
linearized chain; the rest parallelize on disjoint owned_files. **#1970 is active for every
IC: remediate adjacent debt in the touched surface in-slice (never defer).**

**Phase ordering: A (seam) → B (structural adoption) → C (independent).** The seam lands
first because every B adoption resolves through it; C is fully independent and parallelizes.

### IC-01 — MissionTopology enum + CommitTargetKind derivation (SEAM, sequence FIRST)
- **FRs**: FR-001, FR-005. **Surfaces**: `mission_runtime/context.py` (anchor).
- Add the `MissionTopology {SINGLE_BRANCH, LANES, COORD, LANES_WITH_COORD}` enum (FLATTENED =
  history flag, not a value). Re-express `CommitTargetKind` as a `MissionTopology`-derived
  per-ref projection (`routes_through_coordination`), deleting the kind at the ≤8 touched
  branch sites; the codebase-wide eradication is Mission B (C-007).

### IC-02 — Store + backfill the topology (SEAM, after IC-01)
- **FRs**: FR-002, FR-003. **Surfaces**: `core/mission_creation.py` (mint), NEW
  `migrate/backfill_topology`, `doctor.py` (`doctor topology` audit).
- Mint `topology` into `meta.json` at create; `migrate backfill-topology` computes+persists
  for legacy missions (backfill-identity precedent) + `doctor topology --json` audit.
- **Sequencing landmine (dogfooding):** backfill THIS mission's `meta.json` BEFORE any caller
  reads the stored field. Until backfilled, the shell computes-and-persists once via the
  legacy derivation, then reads the stored value.

### IC-03 — Pure resolve_context_for_mission + retire the derivation (SEAM, after IC-01/IC-02)
- **FRs**: FR-004. **Surfaces**: `mission_runtime/resolution.py` (anchor),
  `mission_runtime/context.py` (return VO).
- Add the PURE `resolve_context_for_mission(mission_id, topology) -> ExecutionContext` as a
  thin projection over `build_execution_context` (no FS/git I/O — NFR-006; shell passes
  id+topology). Optional input-assertion: fail-closed on supplied-vs-resolved mismatch. Retire
  the `_resolve_coordination_branch` / `resolution.py:705-718` derivation heuristic.

### IC-04 — Read path consults stored topology (STRUCTURAL #2062) + differential gate
- **FRs**: FR-006, FR-010. **Surfaces**: `missions/_read_path_resolver.py` (anchor),
  `tests/missions/test_surface_resolution_equivalence.py`.
- `_resolve_existing_for_slug` (and the legs it feeds) resolve via the seam/stored topology;
  `CoordState.MATERIALIZED` is no longer the deciding signal — a `SINGLE_BRANCH`/`LANES`
  mission resolves PRIMARY regardless of an on-disk husk (C-004 structural). Correct the stale
  `:263` "No branch is supplied here" comment.
- Differential gate: add the PURE input→output cell (feed (id, topology) for all 4 cells,
  assert ExecutionContext fields) AND RETAIN the on-disk flattened-stale-coord row × every
  handle form (until those legs are deleted); type+error_code assertion unweakened.
- **Live-evidence (NFR-001/C-002):** prove on a real flattened-mid-flight repro; the pure cell
  ADDS a proof, never replaces the live one.
- **Campsite (FR-016 share):** de-pin the surface-resolver coord-empty/coord tests.

### IC-05 — Write-authority adoption across planning commits
- **FRs**: FR-007, FR-009, **FR-022** (extract touched mission.py placement/commit helpers →
  `coordination/commit_router.py`, #2056; co-locates with FR-005's CommitTargetKind projection).
  **Surfaces**: `cli/commands/safe_commit_cmd.py`, `spec_commit_cmd.py`, `status/emit.py`,
  `cli/commands/agent/mission.py` (setup_plan write path), `coordination/commit_router.py`.
- Route every planning-artifact commit + status-event emission through the seam; no command
  resolves a write target from `HEAD` (#2063 root: `safe-commit._resolve_commit_target`).
  Separate `safe-commit`'s generic-operator-file responsibility from the mission-aware path
  (NFR-002 — keep generic intact + tested).

### IC-06 — map-requirements / finalize-tasks one WP-frontmatter surface
- **FRs**: FR-008. **Surfaces**: `cli/commands/agent/tasks.py` (map-requirements),
  `cli/commands/agent/mission.py` (finalize read region — LINEARIZE after IC-05 anchor edits).
- Both read+write WP `requirement_refs` through one seam-resolved surface (primary INPUT,
  staged to coord at commit-time). Consolidate the duplicated READ surface to one place;
  `compute_coverage` is already single-source — do NOT chase the coverage math.
- **Campsite (FR-016 share):** de-pin `test_map_requirements_coord.py` /
  `test_map_requirements_spec_path.py` to assert cross-command coherence, not the split.

### IC-07 — Collapse is_committed 3-leg OR (DEPENDS IC-04 + IC-05 + live repro)
- **FR**: FR-011. **Surface**: `missions/_substantive.py:317-412`.
- Reduce to a single-surface check on the resolved placement ref; remove the multi-surface
  diagnostics workaround. **Gated**: only after the seam adoption makes the surface
  structurally singular (IC-04/IC-05) AND a live flattened repro is green (top risk).

### IC-08 — Real worktree-repair verb + recovery-string repoint + guard (INDEPENDENT)
- **FRs**: FR-012, FR-013, **FR-021** (extract the `doctor.py` coord-recovery cluster
  `:3092-3225` → NEW `cli/commands/_coord_recovery.py`, #2059), FR-015 (hoist 5× recovery hint).
  **Surfaces**: NEW `cli/commands/agent/worktree.py`, NEW `_coord_recovery.py`, `doctor.py`,
  `coordination/surface_resolver.py`, ADR `2026-06-19-1`, NEW `test_command_references.py`.
  **Internal order**: FR-015 hoist → FR-021 cluster extract → FR-012 verb rename (one edit point).
- Register `agent worktree repair --mission <slug>` (recreate via `CoordinationWorkspace.resolve()`
  + prune orphaned). Repoint each recovery hint to the command that fixes its class. New guard
  scans `src/specify_cli/**/*.py` literals + `architecture/**/*.md` for `spec-kitty <tokens>`
  vs registered Typer commands, with a planted-phantom self-test.
- **Gate-unmask discipline (NFR-003):** the guard catches offenders only post-land — pair with
  a full-suite dry-run + the planted-phantom self-test proving it FAILS on a planted literal
  before relying on it. Never ship a mission-diff-scoped assertion to main.
- **Campsite (FR-016 share):** de-pin `test_doctor_coordination.py` + the surface-resolver
  phantom-string tests.

### IC-09 — Doctrine prompt migration + campsite folds (INDEPENDENT)
- **FRs**: FR-014 (safe-commit→spec-commit doctrine), FR-017 (#2066 parsed FR-ID set), FR-018
  (#1891 clean --json), FR-019 (#2037 3 path-sinks: `mission.py` / `tasks.py:1911` /
  `merge.py:1126`), FR-020 (#2048 gated shim retire). **Surfaces**: charter prompt, the touched
  command --json paths, the 3 path sinks, `mission_read_path.py` (gated).
- Migrate the charter prompt off `safe-commit`. Run `test_no_legacy_terminology.py` + the full
  `tests/architectural/` sweep pre-push (CI-only doctrine gates). Fold the cheap in-surface
  campsite items where their surface is touched.

## Lane mapping (for /spec-kitty.tasks)

- **Linearized seam chain (sequential, lands FIRST)**: IC-01 (enum/kind) → IC-02 (store/backfill)
  → IC-03 (pure resolver/derivation retirement). Shared anchors `context.py` / `resolution.py`.
- **Structural adoption (after the seam)**: IC-04 (read path, anchor `_read_path_resolver.py`) →
  IC-05 (write authority, anchor `mission.py`) → IC-06 (map/finalize, linearize after IC-05) →
  IC-07 (is_committed collapse, LAST, gated on live repro).
- **Independent parallel lanes**: IC-08 (verb + guard + doctor de-godding) · IC-09 (doctrine +
  campsite folds). Fully disjoint from the seam/adoption surfaces.
- **WP slicing is NOT 1:1 with ICs** — slice for reasonable size (3–7 subtasks each); split
  large ICs (e.g. IC-08) and keep disjoint owned_files.

## Risks

1. **Load-bearing-workaround collapse (TOP).** The `is_committed` 3-leg OR masks the surface
   split; its collapse (IC-07) is sequenced last, gated on the structural seam adoption AND a
   real flattened-mid-flight repro (NFR-001).
2. **Backfill sequencing landmine (dogfooding).** FR-003 must backfill THIS mission's `meta.json`
   topology BEFORE any caller reads the stored field; the implement loop runs on a coord-topology
   mission that itself exercises the bugs under fix. Flatten friction expected — carry the
   live-evidence rule throughout.
3. **Enum does NOT subsume transient states (C-006).** The create-window (#1718) and coord-deleted
   (#1848) states are orthogonal to the 4 cells; they MUST stay probe-discriminated. A re-route
   that assumes stored topology answers "is the coord worktree materialized / branch alive?"
   regresses #1718/#1848 — keep the probe.
4. **safe-commit overload regression (NFR-002).** The mission-aware planning path must not break
   `safe-commit`'s generic-operator-file use — separate the two responsibilities, keep generic tested.
5. **New-guard self-validation gap (NFR-003).** FR-013's guard only catches offenders after it
   lands; pair it with a planted-phantom self-test + full-suite dry-run.
6. **Scope creep into Mission B (C-007).** The temptation to eradicate ALL `CommitTargetKind`
   references / adopt the resolver at ALL 29+28 sites in-mission must be resisted — this mission
   touches ≤8 branch sites + the planning commands only; the rest is Mission B.

## Campsite directive (#1970) — ACTIVE

Operator-mandated for this mission and every WP: remediate adjacent debt in a touched surface
IN-SLICE (FR-015..FR-022 + any found in-flight), bounded to the mission goals. No "pre-existing,
out of scope" hand-waving for issues inside a touched surface. Partial de-godding is REQUIRED
(FR-021 doctor cluster → `_coord_recovery.py`; FR-022 mission.py helpers → `commit_router.py`).

## Post-planning brownfield checks

Two-agent brownfield sweep (randy-reducer foldable/split-brain/deprecation + architect-alphonso
tech-debt-ticket scan), 2026-06-22, carried from the pre-revision plan (still valid — the
touched surfaces are a superset).

### Folded INTO scope (cheap, in-surface, within goals)
- **#2066 → FR-017** — surface the parsed FR-ID set on coverage mismatch.
- **#1891 (preamble leg) → FR-018** — clean single `--json` doc on setup-plan/finalize-tasks
  (map-requirements leg already fixed — regression-assert only).
- **#2037 (3/4 sinks) → FR-019** — harden `mission.py` / `tasks.py:1911` / `merge.py:1126`
  CLI-arg path joins; leave `decision.py:464`.
- **#2048 (gated) → FR-020** — retire the dead `mission_read_path` shim IF the FR-006 read-path
  adoption proves zero external consumers (deletes shim + repoints test imports + reverses a
  `_baselines.yaml` ratchet bump 9→8).
- **#2059 → FR-021 (REQUIRED de-godding, IC-08)** — extract the `doctor.py` coord-recovery cluster
  into `cli/commands/_coord_recovery.py` (mirroring `_doctrine_health.py`).
- **#2056 → FR-022 (REQUIRED de-godding, IC-05)** — extract the touched `mission.py`
  placement/commit helpers into `coordination/commit_router.py`. Co-locates with FR-005's
  CommitTargetKind projection.
  *(Both bounded to the seam the mission already rewrites — local de-godding, not a wholesale
  split. `tasks.py` #2058 gets a pointer ONLY — maxCC 178 risk.)*

### New brownfield consideration for the seam
- **Backfill migration is a NEW surface.** It mirrors `migrate backfill-identity`; reuse that
  command's structure + the `doctor identity`/`doctor topology` audit pairing. Do NOT hand-roll
  a parallel migration framework.
- **CommitTargetKind has codebase-wide reach (~152 refs/41 files).** Deleting it wholesale is
  Mission B (C-007); this mission deletes/derives only the ≤8 touched branch sites and leaves
  the rest behind a derived projection so the codebase still compiles.

### Deprecations — none due now (LEAVE all)
- `safe_commit_cmd.py:189-212` `--to-branch` "required in v3.3" — NOT-YET-DUE (current 3.2.2). LEAVE.
- `src/specify_cli/next/` shim ("removed in 3.3.0") — not a touched surface. LEAVE.

### Explicitly left OUT (each its own mission-sized effort)
#1357 (CoordinationWorkspace.resolve lock redesign), #2049 (broad audit-allowlist shrink), #1887
(squash-merge dup artifacts), #2031 (post-merge analyzer), the full `doctor.py`/`mission.py`/`tasks.py`
decompositions, **and the codebase-wide CommitTargetKind eradication + universal resolver adoption
(Mission B, C-007)**.

### Relationship to epic #645 — ORTHOGONAL (separate architectural track)
#645 = "Stable Application API Surface (UI/CLI/MCP/SDK)" — a consumer/transport read-API epic. This
mission = internal **git-topology placement authority** (now a stored `MissionTopology` + pure
projection). **Zero file/seam overlap**; the only literal collision is the token "worktree." **No
mission FR or campsite fold advances #645.** Tracker action: cross-reference only, do NOT parent under
#645 — anchors remain #2007 → #1716 → #1619, with #2069 as the design driver.
