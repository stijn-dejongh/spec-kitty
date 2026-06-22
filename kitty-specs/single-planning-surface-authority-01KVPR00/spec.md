# Spec: Single planning-surface authority + worktree repair

**Mission**: `single-planning-surface-authority-01KVPR00`
**Type**: software-dev (refactor / convergence + new command)
**Driver issues**: #1890 (phantom→real worktree-repair verb), #1716 (write-authority adoption) · folds #2062, #2063, #2064 · parent epic #2007

## Overview

Spec Kitty resolves *where* a mission's planning artifacts live with **two incompatible
primitives**: `primary_feature_dir_for_mission` (PRIMARY checkout, topology-blind) and
`resolve_feature_dir_for_slug` / `resolve_handle_to_read_path` (topology-aware,
coord-preferring, **husk-trusting** — it prefers a coord worktree by on-disk existence).
The mission-surface *read* side was converged by mission `01KVN754` (#2065). The
**write authority is already single** — `resolve_placement_only`
(`src/mission_runtime/resolution.py:761`, documented "byte-identical to what the full
resolver assembles") — but sibling write/read commands **do not adopt it**. That
non-adoption is the live split-brain: artifacts written through one authority are read
back through the other.

This mission **adopts the existing write authority** across the planning commands
(it does NOT build a new resolver — same strangler shape as the read-side mission),
gates the one read-path leg that still trusts an orphaned coord worktree, and replaces
a recovery command advertised everywhere but never registered (`agent worktree repair`)
with a **real recreate-or-prune verb** — because #1890 needs *recreate* and #2062 needs
*orphan-prune*: two halves of one missing verb.

**Campsite-cleaning directive #1970 is ACTIVE for this mission and every WP** (operator
mandate): adjacent debt in a touched surface is REMEDIATED in-slice, not deferred — see
C-001 and the campsite FRs (FR-009..FR-013).

## Domain Language

- **Surface authority** (canonical) — the single resolver (`resolve_placement_only`)
  deciding which on-disk surface (primary checkout vs coordination worktree) a mission
  artifact is written to / read from. "Planning-surface authority" = its adoption across
  the planning commands.
- **Flattened mission** — `coordination_branch` removed from the primary `meta.json`; the
  primary checkout is authoritative. A flattened mission may leave a stale coord worktree
  on disk.
- **Orphaned coord worktree / husk** — a `.worktrees/<slug>-<mid8>-coord/` directory left
  on disk after flatten/teardown, carrying stale status; must NOT be a read authority.
- **Planning INPUT artifacts** — `spec.md`, `plan.md`, `tasks/`, `meta.json`: authored on
  the PRIMARY checkout, staged to the coord surface only at commit time (finalize-tasks'
  own documented invariant).
- **Recreate-or-prune** — the worktree-repair verb: re-materialize a *missing* coord
  worktree (via `CoordinationWorkspace.resolve()`) and remove an *orphaned* one.

## User Scenarios & Testing

### Primary — planning artifacts read back from the surface they were written to
An operator runs `/spec-kitty.specify` then `/spec-kitty.tasks` on a coord-topology
mission. `spec.md` is committed through the mission-aware path and lands on the surface
the next command reads. `/tasks` and `finalize-tasks --validate-only` both see `spec.md`
and the WP files — no "spec.md not found" / "Tasks directory not found" divergence. *(#2063)*

### Primary — requirement coverage agrees across commands
An operator runs `map-requirements` (reports full coverage) then `finalize-tasks
--validate-only`. Both read and write WP `requirement_refs` through the same surface, so
finalize reports **zero** `unmapped_functional_requirements` — the two commands never
disagree about where the WP frontmatter lives. *(#2064)*

### Primary — a flattened mission never reads a stale coord worktree
A mission flattened mid-flight (coordination_branch removed from primary meta) with a
stale `-coord` worktree still on disk resolves its status from the **PRIMARY** surface on
**all three read legs** (read-path, surface, aggregate) for **every** handle form
(`<slug>-<mid8>`, bare-mid8, full ULID, bare human slug). The dep-gate, kanban, and
review-claim no longer report stale `planned` lanes. *(#2062 read leg)*

### Primary — recovery commands actually exist and work
When the resolver/doctor diagnose a missing or orphaned coord worktree, the operator runs
`spec-kitty agent worktree repair --mission <slug>`: a **registered** command that
recreates a missing coord worktree and prunes an orphaned one. No operator-facing recovery
hint names a command that does not exist. *(#1890)*

### Exception / edge cases
- **create→first-write window** (coord declared, worktree not yet materialized) still
  resolves PRIMARY on every leg — the #1718 contract is preserved (regression-guarded).
- **coord-deleted** (declared branch deleted from git) still hard-fails
  `CoordinationBranchDeleted` (#1848 data-loss carve-out) — unchanged.
- **Legacy / no-mid8 missions** must not regress: each topology (flattened, coord-fresh,
  legacy) hits a *different* resolver leg today, so convergence is proven against ALL of
  them via the differential equivalence gate.
- A `worktree repair` on a mission with no coordination topology is a benign no-op with a
  clear message (not an error).

## Functional Requirements

| ID | Requirement | Status |
| --- | --- | --- |
| FR-001 | **Single write-surface authority.** Every planning-phase artifact commit (`spec.md`, `plan.md`, `tasks/`, WP `requirement_refs` frontmatter, lifecycle status events) MUST resolve its write destination through `resolve_placement_only` (or its projection). No planning command may resolve a write target from the current `HEAD` branch independently. | proposed |
| FR-002 | **`safe-commit` retired from planning prompts.** Planning-artifact commits in all mission-step prompts MUST use the mission-aware `spec-commit`; the charter prompt (`src/doctrine/missions/mission-steps/software-dev/charter/prompt.md:198`) MUST be migrated off `safe-commit`. Generic `safe-commit` is retained for non-mission operator files (do NOT overload it). | proposed |
| FR-003 | **`map-requirements` and `finalize-tasks` share one WP-frontmatter surface.** `map-requirements` writes and `finalize-tasks --validate-only` reads WP `requirement_refs` through the SAME surface authority (honoring finalize-tasks' documented invariant: planning INPUT artifacts authored on PRIMARY, staged to coord at commit-time). A successful `map-requirements` MUST be visible to the immediately-following `finalize-tasks --validate-only`. | proposed |
| FR-004 | **Flattened mission must not prefer an orphaned coord worktree (read-path leg).** `missions/_read_path_resolver._resolve_existing_for_slug` MUST consult the declared-coord signal (primary `meta.json` `coordination_branch` presence) so `CoordState.MATERIALIZED` is necessary-but-not-sufficient: a flattened mission (no `coordination_branch`) MUST resolve PRIMARY, matching `resolve_handle_to_read_path` / `resolve_status_surface_with_anchor`. Closes the #2062 read leg (composed / bare-mid8 / ULID handles; fold the bare-human-slug surface-leg quirk). | proposed |
| FR-005 | **Differential gate covers the flattened-stale-coord topology.** `tests/missions/test_surface_resolution_equivalence.py` MUST add a `flattened-stale-coord` topology (primary meta with NO `coordination_branch` + a stale `-coord` worktree on disk) × every handle form, asserting all three legs return the PRIMARY dir — without weakening the existing `type(a) is type(b)` AND `error_code` assertion. | proposed |
| FR-006 | **Status-event emission resolves its write surface from the single authority.** Every `status.emit.emit_status_transition` call site MUST pass a `feature_dir` resolved by the canonical write authority, not an ad-hoc per-caller path — so dep-gate / kanban / review-claim status reads and `move-task` writes converge on one surface. | proposed |
| FR-007 | **Real `worktree repair` verb.** Register `spec-kitty agent worktree repair --mission <slug>` that **recreates** a missing coord worktree (via `CoordinationWorkspace.resolve()`) and **prunes** an orphaned one. Repoint every operator-facing recovery hint to a command that actually fixes its failure class (husk → `doctor workspaces --fix`; coord-missing/empty/orphaned → `worktree repair`); amend ADR `2026-06-19-1`; reconcile the Python/ADR copies to the canonical `SKILL.md` answer. No remediation string may name an unregistered command. Closes #1890. | proposed |
| FR-008 | **Command-reference guard.** An architectural test MUST scan `src/specify_cli/**/*.py` string literals and `architecture/**/*.md` (ADRs) for `spec-kitty <tokens>` invocations and assert each names a REGISTERED Typer command (reuse the `_build_live_app`/registered-path machinery in `test_docs_cli_reference_parity.py`), with a planted-phantom self-test. Allowlist entries require a rationale comment. | proposed |
| FR-009 | **(Campsite #1970) Hoist duplicated recovery hints.** The worktree-repair recovery sentence duplicated 5× in `doctor.py` (`:3092,:3116,:3209,:3225,:3245`) MUST be hoisted to ≤2 named module constants (one per failure class) so no recovery sentence is duplicated ≥3× (Sonar S1192). | proposed |
| FR-010 | **(Campsite #1970) De-pin fakeable / split-brain-codifying tests.** Tests that assert the phantom string (`test_surface_resolver_coord_empty_warning.py:127`, `test_surface_resolver.py:276`, `test_doctor_coordination.py:132`) and tests that codify the coord-vs-primary split as desired (`test_map_requirements_coord.py`, `test_map_requirements_spec_path.py`) MUST be re-pointed to assert the REAL command and **cross-command surface coherence** — no test pins a nonexistent command or the split-brain. | proposed |
| FR-011 | **(Campsite #1970) Collapse `is_committed` 3-leg OR.** Once FR-001 holds, `missions/_substantive.is_committed` (`:317-412`) MUST reduce from a 3-surface OR to a single-surface check on the resolved placement ref; the multi-surface diagnostics workaround is removed. | proposed |
| FR-012 | **(Campsite #1970) Unify `probe_coord_state` branch-signal threading.** The asymmetric branch-signal threading between `_resolve_existing_for_slug` (omits it) and `_resolve_not_found` (supplies it) MUST be unified; the stale `:263` comment ("No branch is supplied here") that documents the defect as intentional MUST be corrected. | proposed |
| FR-013 | **(Campsite #1970) Consolidate the WP-frontmatter READ SURFACE.** `compute_coverage` is ALREADY single-source (`requirement_mapping.py:61`, imported by both commands) — the real split-brain is the SURFACE each command reads WP `requirement_refs` from (`map-requirements`' `read_all_wp_requirement_refs` vs `finalize-tasks`' own dir resolution). Consolidate that READ SURFACE so both read frontmatter from ONE place; do NOT chase the (already-shared) coverage math. *(brownfield-corrected)* | proposed |
| FR-014 | **(Campsite-fold #2066) Surface the parsed FR-ID set on coverage mismatch.** When WP `requirement_refs` don't match `spec.md` FR IDs, `map-requirements` / `finalize-tasks` `--json` MUST emit the parsed FR set so the operator can see the actual vs expected IDs (same coverage surface as FR-003/FR-013). | proposed |
| FR-015 | **(Campsite-fold #1891) Clean `--json` document on the touched commands.** `setup-plan` and `finalize-tasks` `--json` MUST emit a single clean JSON document (no human preamble before the JSON on stdout). The `map-requirements` `CommitResult`-serialization leg is already fixed — add a regression assert, do not re-fix. (The `agent action implement --json` leg is out of scope — untouched surface.) | proposed |
| FR-016 | **(Campsite-fold #2037) Harden the 3 in-surface untrusted-path sinks.** Route the CLI-arg `--mission` path joins at `agent/mission.py:312`, `agent/tasks.py:1911`, `cli/commands/merge.py:1055` (3 of #2037's 4 sinks — all in touched surfaces) through `assert_safe_path_segment` / `ensure_within_any` with a negative test each. Leave `decision.py:464` (untouched surface). | proposed |
| FR-017 | **(Campsite-fold #2048, GATED) Retire the dead `mission_read_path` shim.** IF the FR-004 read-path adoption confirms ZERO external consumers of `src/specify_cli/mission_read_path.py`, delete the shim, repoint its test imports, and decrement the `tests/architectural/.../_baselines.yaml` backcompat-shim allowlist (9→8). IF consumers remain, LEAVE it and record why (do not force). | proposed |
| FR-018 | **(Partial de-godding #2059) Extract the `doctor.py` coord-recovery cluster.** As Lane D adds the worktree-repair verb + repoints recovery hints, the cohesive worktree/coord-recovery helper cluster in `doctor.py` (~`:3092-3225`, ~5 helpers) MUST be extracted into a sibling module `cli/commands/_coord_recovery.py` (mirroring `_doctrine_health.py`) with a top-of-file `#2059` pointer. This is a REQUIRED in-slice extraction of the seam the mission already rewrites — not optional, and bounded to that one cluster (no wider `doctor.py` decomposition). | proposed |
| FR-019 | **(Partial de-godding #2056) Extract the touched placement/commit helpers from `agent/mission.py`.** The placement/commit helpers in `setup_plan` / `finalize_tasks` that this mission edits for write-authority routing (FR-001/FR-003) MUST be extracted into the canonical `coordination/commit_router.py` seam (the strangler target #2056 names) with a `#2056` pointer — REQUIRED for the seams the mission touches, bounded to those helpers (no wider `mission.py` decomposition). | proposed |

## Non-Functional Requirements

| ID | Requirement | Status |
| --- | --- | --- |
| NFR-001 | **Live-evidence convergence proof.** The write/read convergence MUST be proven on a REAL flattened-mid-flight mission repro (the #2062 topology), not by static reading; the differential equivalence gate (incl. the new `flattened-stale-coord` row) MUST be green at every WP boundary. #2062 is NOT marked fixed without a witnessed live repro. | proposed |
| NFR-002 | **No regression of generic `safe-commit`.** `safe-commit`'s legitimate non-mission operator-file commit path MUST remain functional and tested (the two responsibilities are separated, not overloaded). | proposed |
| NFR-003 | **Gate-unmask discipline.** The FR-008 command-reference guard only catches offenders after it lands — it MUST be paired with a full-suite dry-run in this mission and a planted-phantom self-test proving it fails on a planted Python-literal phantom BEFORE reliance. No mission-diff-scoped assertion is shipped to main. | proposed |
| NFR-004 | **Behavior-preserving adoption.** Write-authority adoption reroutes (FR-001/FR-002/FR-006) are behavior-preserving for already-correct topologies (coord-fresh, create-window, no-coord, coord-deleted) — proven by the equivalence gate + the preserved #1718/#1848 guards. | proposed |
| NFR-005 | **Clean static analysis.** All new/changed code passes `ruff` and `mypy` with zero issues/warnings; cyclomatic complexity ≤15; repeated non-trivial literals hoisted (no new S1192). No suppression added to pass. | proposed |

## Constraints

| ID | Constraint | Status |
| --- | --- | --- |
| C-001 | **#1970 campsite-cleaning is ACTIVE for every WP.** Adjacent debt in a touched surface is REMEDIATED in-slice (FR-009..FR-019 and any found in-flight), bounded to mission goals — never deferred/adjudicated with "pre-existing, out of scope". Each WP prompt MUST carry this directive. **Partial de-godding is REQUIRED, not optional (FR-018/FR-019):** the `doctor.py` coord-recovery cluster → `_coord_recovery.py`, and the touched `mission.py` placement/commit helpers → `coordination/commit_router.py`, are extracted in-slice (each bounded to the seam the mission already rewrites + a tracker pointer). This is local de-godding of touched seams — NOT a wholesale module split (the full `doctor.py`/`mission.py`/`tasks.py` decompositions #2059/#2056/#2058 remain their own efforts; `tasks.py` gets a pointer only, no extraction — maxCC 178 risk). | active |
| C-002 | **No close-on-static for #2062.** #2062 stays OPEN until a live flattened-mission repro witnesses all legs resolving PRIMARY. | active |
| C-003 | **Adopt, do not rebuild.** `resolve_placement_only` is the canonical write authority — adopt it; do NOT introduce a second/parallel write resolver (the non-adoption IS the bug). | active |
| C-004 | **Linearize shared anchors.** `mission_runtime/resolution.py`, `missions/_read_path_resolver.py`, and `cli/commands/agent/mission.py` (god-module) are shared surfaces — land them on a linearized chain before the disjoint lanes; expected refactor overlap. | active |
| C-005 | **Preserve the #2065 read-side contract.** Keep `CoordAuthorityUnavailable`/typed errors/`CoordinationBranchDeleted` (#1848) and the create-window (#1718) intact; this mission extends, never regresses, the read-side convergence. | active |
| C-006 | **No version prescription.** The PO assigns release/patch numbers at release time; frame work as focus/milestone, not a version. | active |

## Success Criteria

- **SC-001** For a coord-topology mission, `spec.md` committed through the planning flow is
  visible to the immediately-following `/spec-kitty.tasks` and `finalize-tasks
  --validate-only` reads — no "spec.md not found" divergence (#2063, witnessed).
- **SC-002** After `map-requirements` reports full coverage, `finalize-tasks --validate-only`
  reports **zero** `unmapped_functional_requirements` for the same mission (#2064, witnessed).
- **SC-003** A flattened mission with a stale `-coord` worktree resolves status from the
  PRIMARY surface on **all 3 legs × all 4 handle forms** (witnessed live; #2062).
- **SC-004** `spec-kitty agent worktree repair --mission <slug>` is a registered command that
  recreates a missing coord worktree and prunes an orphaned one; **every** operator-facing
  recovery hint names a registered command (#1890).
- **SC-005** The differential equivalence gate includes a `flattened-stale-coord` topology row
  asserting all legs agree on PRIMARY, with the type+error_code assertion unweakened.
- **SC-006** The FR-008 guard **fails** on a planted Python-literal phantom (self-test) and
  finds **zero** unregistered `spec-kitty` invocations across `src/specify_cli/**` + ADRs.
- **SC-007** No recovery sentence is duplicated ≥3× (S1192 clean); the previously-fakeable
  phantom-string + split-brain tests assert the real command and cross-command coherence.
- **SC-008** `is_committed` is reduced to a single-surface check; the full test suite is green
  including the preserved #1718/#1848 guards.

## Key Entities

- **Surface authority** — `resolve_placement_only` (`mission_runtime/resolution.py:761`),
  the single write-destination resolver the planning commands must adopt.
- **Planning surface** — primary checkout vs coordination worktree; the artifact's home.
- **Coordination worktree state** — materialized / empty / orphaned-after-flatten / missing
  (the recreate-or-prune verb operates on the last two).
- **Differential equivalence gate** — `test_surface_resolution_equivalence.py`; the
  deletion/convergence safety net, extended with the `flattened-stale-coord` topology.

## Assumptions

- `resolve_placement_only` is genuinely byte-identical to the full resolver's placement
  (verified by mission `01KVGCE8`/`01KVN754`); adoption is a reroute, not a redesign.
- `CoordinationWorkspace.resolve()` is the canonical coord-worktree materializer that
  `spec-commit` already uses on demand; the new `worktree repair` verb forwards to it.
- The PR-bound coordination topology of THIS mission is itself a dogfooding hazard for the
  exact bugs under fix — flatten / coord-friction is expected during implement; carry the
  live-evidence rule (NFR-001) and prefer running status commits from the authoritative
  surface.

## Issue Matrix References

#1890 (driver — phantom→real verb), #1716 (write-authority adoption epic facet), #2062
(read-path leg residual — OPEN, no close without live repro), #2063, #2064, #2007 (parent
epic), #1970 (campsite directive — process reference). **Campsite-advanced (brownfield
squad, in-surface cheap folds):** #2066 (FR-014), #1891 partial (FR-015), #2037 partial —
3/4 sinks (FR-016), #2048 gated (FR-017). **Partial de-godding REQUIRED (FR-018/FR-019):**
#2059 doctor coord-recovery cluster → `_coord_recovery.py`, #2056 mission.py placement/commit
helpers → `commit_router.py`. **Explicitly left out** (own mission-sized efforts): #1357
(lock redesign), #2049 (broad audit), #1887 (merge path), #2031, #2058 + the *full*
`doctor.py`/`mission.py` decompositions (only the touched seams are extracted), the v3.3
`--to-branch` / `next/` shim deprecations (not due at 3.2.x).
