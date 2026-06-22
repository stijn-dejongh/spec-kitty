# Implementation Plan: Single planning-surface authority + worktree repair

**Mission**: `single-planning-surface-authority-01KVPR00`
**Branch**: `feat/single-planning-surface-authority` (planning base = merge target; later PR to `main`)
**Driver**: #1890 + #1716 · folds #2062 / #2063 / #2064 · parent epic #2007 · campsite #1970

## Summary

Adopt the **existing** single write-surface authority (`resolve_placement_only`,
`src/mission_runtime/resolution.py:761`) across the planning commands so artifacts are
read back from the surface they were written to, gate the one read-path leg that still
trusts an orphaned coord worktree, and replace the never-registered `agent worktree
repair` recovery command with a real recreate-or-prune verb. This is a **strangler-style
adoption** of an SSOT (same shape as the #2065 read-side mission) — **not** a new resolver
(C-003). #1970 campsite-cleaning is active for every WP.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: typer, rich, ruamel.yaml (CLI surfaces); pytest, pytest-xdist, mypy, ruff (gates); `spec_kitty_events` / `spec_kitty_tracker` public imports only (shared-package boundary)
**Storage**: filesystem — `kitty-specs/<slug>/` (primary checkout) and `.worktrees/<slug>-<mid8>-coord/` (coordination worktree); `status.events.jsonl` append-only log; `meta.json` identity
**Testing**: pytest (`tests/`), parallel `-n auto --dist loadfile` with per-worker HOME isolation; the differential equivalence gate `tests/missions/test_surface_resolution_equivalence.py`; architectural gates under `tests/architectural/`
**Target Platform**: Linux/macOS dev CLI (Spec Kitty toolkit)
**Project Type**: single (Python CLI package `src/specify_cli` + `src/mission_runtime`)
**Performance Goals**: no measurable regression in resolver hot-path (pure-path happy path preserved — no new git/subprocess on the common case)
**Constraints**: ruff + mypy zero-issue on new/changed code; cyclomatic complexity ≤15; no new S1192; behavior-preserving adoption for already-correct topologies; live-evidence proof for #2062
**Scale/Scope**: 6 implementation concerns across ~10 source surfaces + 2 new files (a CLI command module + an architectural guard); refactor mission with expected linearized shared-surface overlap

## Charter Check

*GATE: software-dev-default, compact mode (DIR-001..013). Re-checked post-design.*

- **DIR-001 (architectural integrity / separation of concerns)**: PASS — the mission's
  whole intent is to collapse two incompatible surface-resolution primitives onto one
  authority and to separate `safe-commit`'s two responsibilities (NFR-002). No new
  parallel resolver (C-003).
- **DIR (testing standards)**: PASS — every behavior WP adds focused tests; the
  differential gate gains the `flattened-stale-coord` row (FR-005); the new guard carries
  a planted-phantom self-test (NFR-003).
- **DIR (canonical sources / no improvisation)**: PASS — adopt `resolve_placement_only`
  and `CoordinationWorkspace.resolve()`; reconcile docs/ADR to the canonical `SKILL.md`.
- **Terminology canon**: the doctrine-prompt edit (Lane E) runs
  `tests/architectural/test_no_legacy_terminology.py` pre-push.
- No charter conflicts; no gate waivers required.

## Project Structure

### Documentation (this mission)
```
kitty-specs/single-planning-surface-authority-01KVPR00/
├── spec.md              # committed (5d409fe)
├── plan.md              # this file
├── research.md          # Phase 0 (decisions/rationale)
├── data-model.md        # Phase 1 (entities: surface authority, coord state, repair verb)
├── quickstart.md        # Phase 1 (the live flattened-mission repro recipe)
└── tasks.md             # Phase 2 (/spec-kitty.tasks — NOT created here)
```

### Source Code (repository root) — surfaces touched
```
src/mission_runtime/resolution.py                  # write authority SSOT (anchor)
src/specify_cli/missions/_read_path_resolver.py    # #2062 read-leg gate + FR-012 (anchor)
src/specify_cli/missions/_substantive.py           # is_committed 3-leg OR collapse (FR-011)
src/specify_cli/cli/commands/agent/mission.py      # setup_plan + finalize_tasks (anchor, god-module)
src/specify_cli/cli/commands/agent/tasks.py        # map-requirements (Lane B)
src/specify_cli/cli/commands/safe_commit_cmd.py    # write-authority adoption (Lane A)
src/specify_cli/cli/commands/spec_commit_cmd.py    # write-authority adoption (Lane A)
src/specify_cli/status/emit.py                     # event write-surface (FR-006)
src/specify_cli/cli/commands/agent/worktree.py     # NEW recreate-or-prune verb (Lane D)
src/specify_cli/cli/commands/doctor.py             # recovery-hint hoist + repoint (Lane D)
src/specify_cli/coordination/surface_resolver.py   # recovery strings repoint (Lane D)
architecture/3.x/adr/2026-06-19-1-...md            # ADR amend (Lane D)
src/doctrine/missions/mission-steps/software-dev/charter/prompt.md  # safe-commit→spec-commit (Lane E)
tests/missions/test_surface_resolution_equivalence.py  # flattened-stale-coord cell (Lane C)
tests/architectural/<new command-reference guard>  # NEW (Lane D, FR-008)
```

## Complexity Tracking

No charter-gate violations to justify. The one structural risk is collapsing the
`is_committed` 3-leg OR (FR-011): it is a **load-bearing workaround** and its collapse is
gated on (a) the write-authority adoption (IC-02) landing AND (b) a live flattened-mission
repro (NFR-001) — sequenced after the safety net, never before.

## Implementation Concern Map

Linearization law (NFR refactor overlap): the shared anchors —
`mission_runtime/resolution.py`, `missions/_read_path_resolver.py`,
`cli/commands/agent/mission.py` — are touched by multiple ICs and MUST land on a
linearized chain; the rest parallelize on disjoint owned_files. **#1970 is active for
every IC: remediate adjacent debt in the touched surface in-slice (never defer).**

### IC-01 — Read-path flattened-stale-coord gate + differential cell (SAFETY NET, sequence FIRST)
- **FRs**: FR-004, FR-005, FR-012. **Surfaces**: `missions/_read_path_resolver.py`,
  `tests/missions/test_surface_resolution_equivalence.py`.
- Thread `declares_coordination` into `_resolve_existing_for_slug` so
  `CoordState.MATERIALIZED` is necessary-but-not-sufficient; a flattened mission resolves
  PRIMARY on all legs × all handle forms. Unify the asymmetric `probe_coord_state`
  branch-signal threading vs `_resolve_not_found` (FR-012); fix the stale `:263` comment.
- Add the `flattened-stale-coord` topology row to the differential gate (without weakening
  `type(a) is type(b)` AND `error_code`). This is the convergence safety net — it must be
  green before IC-05.
- **Campsite**: de-pin the surface-resolver coord-empty / coord tests that codify the
  split (FR-010 share).
- **Live-evidence (NFR-001/C-002)**: prove on a real flattened-mid-flight mission repro.

### IC-02 — Write-authority adoption across planning commits
- **FRs**: FR-001, FR-002, FR-006, **FR-019** (extract touched mission.py placement/commit
  helpers → `coordination/commit_router.py`). **Surfaces**: `mission_runtime/resolution.py`
  (anchor), `cli/commands/safe_commit_cmd.py`, `spec_commit_cmd.py`, `status/emit.py`,
  `cli/commands/agent/mission.py` (setup_plan write path), `coordination/commit_router.py`.
- Route every planning-artifact commit + status-event emission through
  `resolve_placement_only`; no command resolves a write target from `HEAD`. Separate
  `safe-commit`'s generic-operator-file responsibility from the mission-aware path
  (NFR-002 — keep generic intact + tested).
- **Campsite**: none new beyond the reroute; behavior-preserving (NFR-004).

### IC-03 — map-requirements / finalize-tasks one WP-frontmatter surface + coverage consolidation
- **FRs**: FR-003, FR-013. **Surfaces**: `cli/commands/agent/tasks.py` (map-requirements),
  `cli/commands/agent/mission.py` (finalize read region — LINEARIZE after IC-02 anchor
  edits).
- Both read+write WP `requirement_refs` through one surface (primary INPUT, staged to
  coord at commit-time per finalize's documented invariant). Consolidate the duplicated
  coverage computation to one body over one surface (FR-013).
- **Campsite**: de-pin `test_map_requirements_coord.py` / `test_map_requirements_spec_path.py`
  to assert cross-command coherence, not the split (FR-010 share).

### IC-04 — Real worktree-repair verb + recovery-string repoint + command-reference guard
- **FRs**: FR-007, FR-008, FR-009, **FR-018** (extract the `doctor.py` coord-recovery cluster
  `:3092-3225` → NEW `cli/commands/_coord_recovery.py`, #2059 pointer). **Surfaces**: NEW
  `cli/commands/agent/worktree.py`, NEW `cli/commands/_coord_recovery.py`, `doctor.py`,
  `coordination/surface_resolver.py`, ADR `2026-06-19-1`, NEW architectural guard.
  **Internal order**: FR-009 hoist → FR-018 cluster extract → FR-007 verb rename (one edit point).
- Register `agent worktree repair --mission <slug>` (recreate via
  `CoordinationWorkspace.resolve()` + prune orphaned). Repoint each recovery hint to the
  command that fixes its class (husk → `doctor workspaces --fix`; coord-missing/empty/
  orphaned → `worktree repair`). Hoist the 5× doctor hint to ≤2 named constants (FR-009).
- New guard scans `src/specify_cli/**/*.py` literals + `architecture/**/*.md` for
  `spec-kitty <tokens>` vs registered Typer commands, with a planted-phantom self-test.
- **Gate-unmask discipline (NFR-003)**: the guard catches offenders only post-land — pair
  with a full-suite dry-run + the planted-phantom self-test proving it FAILS on a planted
  literal before relying on it. Never ship a mission-diff-scoped assertion to main.
- **Campsite**: de-pin `test_doctor_coordination.py` + the surface-resolver phantom-string
  tests (FR-010 share).

### IC-05 — Collapse is_committed 3-leg OR (DEPENDS IC-02 + live repro)
- **FR**: FR-011. **Surface**: `missions/_substantive.py:317-412`.
- Reduce to a single-surface check on the resolved placement ref; remove the multi-surface
  diagnostics workaround. **Gated**: only after IC-02 makes write-authority singular AND
  the IC-01 safety net (incl. live repro) is green — this is the load-bearing-workaround
  collapse (top risk).

### IC-06 — Doctrine prompt migration (safe-commit → spec-commit)
- **FR**: FR-002 (doctrine half). **Surface**:
  `src/doctrine/missions/mission-steps/software-dev/charter/prompt.md`.
- Migrate the charter prompt off `safe-commit` to mission-aware `spec-commit`. Run
  `tests/architectural/test_no_legacy_terminology.py` + the full `tests/architectural/`
  sweep pre-push (CI-only doctrine gates).

## Lane mapping (for /spec-kitty.tasks)

- **Linearized chain (shared anchors, sequential)**: IC-01 (read-path) → IC-02 (write
  authority) → IC-05 (is_committed collapse). These share `_read_path_resolver.py` /
  `resolution.py` / `mission.py` / `_substantive.py`.
- **Disjoint parallel lanes** (after the anchors they depend on): IC-03 (Lane B, linearize
  after IC-02's mission.py edits) · IC-04 (Lane D, fully disjoint: new worktree.py + doctor
  + guard) · IC-06 (Lane E, doctrine prompt).
- Sequence IC-01 FIRST (safety net); IC-05 LAST (after live repro).

## Risks

1. **Load-bearing-workaround collapse (TOP).** The `is_committed` 3-leg OR and the
   coord-aware/primary-blind reads mask the authority gap; flattened, coord-fresh, and
   legacy (no-mid8) missions each hit a different leg. Convergence MUST be proven on a real
   flattened-mid-flight repro and gated by the equivalence matrix + the new
   `flattened-stale-coord` row (NFR-001). IC-05 is sequenced last for this reason.
2. **Dogfooding hazard.** This mission is itself PR-bound / coord-topology, so the implement
   loop will exercise the exact coord/primary surface bugs under fix (flatten friction,
   stale-coord status reads, spec/plan surface split). Expect to drive status commits from
   the authoritative surface and to flatten if the loop wedges — carry the live-evidence
   rule throughout. (Already seen this class repeatedly in prior missions.)
3. **safe-commit overload regression (NFR-002).** Making the planning path mission-aware
   must not break `safe-commit`'s legitimate generic-operator-file use — separate the two
   responsibilities, keep generic tested.
4. **New-guard self-validation gap (NFR-003).** FR-008's guard only catches offenders after
   it lands; without a planted-phantom self-test + full-suite dry-run it could ship green
   while a real phantom slips. Pair them.

## Campsite directive (#1970) — ACTIVE

Operator-mandated for this mission and every WP: remediate adjacent debt in a touched
surface IN-SLICE (FR-009..FR-013 + any found in-flight), bounded to the mission goals.
No "pre-existing, out of scope" hand-waving for issues inside a touched surface.

## Post-planning brownfield checks

Two-agent brownfield sweep (randy-reducer foldable/split-brain/deprecation +
architect-alphonso tech-debt-ticket scan), 2026-06-22.

### Folded INTO scope (cheap, in-surface, within goals)
- **#2066 → FR-014** — surface the parsed FR-ID set on coverage mismatch (same coverage
  surface as FR-003/FR-013).
- **#1891 (preamble leg) → FR-015** — clean single `--json` doc on setup-plan/finalize-tasks;
  the map-requirements serialization leg is already fixed (regression-assert only).
- **#2037 (3/4 sinks) → FR-016** — harden `mission.py:312` / `tasks.py:1911` / `merge.py:1055`
  CLI-arg path joins via `assert_safe_path_segment`/`ensure_within_any`; leave `decision.py:464`.
- **#2048 (gated) → FR-017** — retire the dead `mission_read_path` shim IF the FR-004 read-path
  adoption proves zero external consumers (deletes shim + repoints test imports + reverses a
  `_baselines.yaml` ratchet bump 9→8).
- **#2059 → FR-018 (REQUIRED de-godding, Lane D)** — extract the `doctor.py` coord-recovery
  cluster (`:3092-3225`, ~5 helpers) into `cli/commands/_coord_recovery.py` (mirroring
  `_doctrine_health.py`) with a #2059 pointer, as Lane D builds the worktree-repair verb.
- **#2056 → FR-019 (REQUIRED de-godding, anchor IC-02)** — extract the touched `mission.py`
  placement/commit helpers (the ones edited for write-authority routing) into the canonical
  `coordination/commit_router.py` seam with a #2056 pointer.
  *(Both are bounded to the seam the mission already rewrites — local de-godding, not a
  wholesale split. `tasks.py` #2058 gets a pointer ONLY, no extraction — maxCC 178 risk.)*

### Spec corrections from the sweep
- **FR-013 retargeted** — `compute_coverage` is already single-source (`requirement_mapping.py:61`);
  the real split-brain is the WP-frontmatter **read surface**, not the coverage math. FR-013
  reworded so an implementer doesn't chase a non-duplication.
- **Sequencing (record in tasks):** FR-009 (hoist the recovery-hint to a constant) MUST land
  BEFORE the #1890 verb rename (FR-007), so the rename is a single edit point. Lane D internal
  order: FR-009 → FR-007.

### Split-brain / LOC
- All known split-brain captured by FR-011 (is_committed 3-leg OR) / FR-012 (probe_coord_state
  asymmetry) / FR-013 (read surface) / FR-009 (hint dup). God-modules (`doctor.py` 3329,
  `mission.py` 3965, `tasks.py` 4527 maxCC 178) handled via C-001 LOCAL extraction of touched
  seams only — NO wholesale decomposition.

### Deprecations — none due now (LEAVE all)
- `safe_commit_cmd.py:189-212` `--to-branch` "required in v3.3" — NOT-YET-DUE (current 3.2.2);
  removing the HEAD-inference now is a premature breaking change. LEAVE.
- `src/specify_cli/next/` shim ("removed in 3.3.0") — not a touched surface. LEAVE.
- `mission.py` `--mission-type`/`--include-tasks` aliases, `tasks.py:1256` legacy-field bridge —
  no operator-set removal version (no-version-prescription). LEAVE.

### Explicitly left OUT (each its own mission-sized effort)
#1357 (CoordinationWorkspace.resolve lock redesign), #2049 (broad audit-allowlist shrink),
#1887 (squash-merge dup artifacts — merge path, not resolver), #2031 (post-merge analyzer),
full #2056/#2058/#2057/#2026 god-module decompositions. Seeds #1623/#1622/#1624 are already
CLOSED (superseded by #2059/#2056/#2058).

### Relationship to epic #645 — ORTHOGONAL (separate architectural track)
#645 = "Stable Application API Surface (UI/CLI/MCP/SDK)" — a consumer/transport read-API
epic (FastAPI/OpenAPI, `MissionRegistry`+cache #956, resource endpoints #957/#958,
`src/dashboard/services/`). This mission = internal **git-topology placement authority**
(`resolve_placement_only`, `_resolve_existing_for_slug`, `CommitTarget`). **Zero file/seam
overlap**; the only literal collision is the token "worktree." Both say "single surface" but
mean different layers (consumer HTTP contract vs. which checkout/worktree an artifact is
written to). **No mission FR or campsite fold advances #645**, and #645's children are all
out of scope. **Tracker action: cross-reference only, do NOT parent under #645** — the
mission's anchors remain #2007 (functional driver) → #1716 (P0 child) → #1619 (parent
execution-context epic). One indirect, non-blocking adjacency: a coherent write-surface
upstream makes a future #956 registry read deterministic — informational only, no dependency
edge either way.
