# Implementation Plan: Charter as Sole Door: Close Bypass Access Paths

**Branch**: `feat/charter-sole-door-bypass-closure` | **Date**: 2026-08-03 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `kitty-specs/charter-sole-door-bypass-closure-01KZ3WAA/spec.md`

The planner did not begin until all planning questions were answered — captured below (spec-time operator
scope decisions + a Phase 0 research squad that surfaced four planning-time corrections, each resolved with
the operator before this plan was written; see spec.md's "Revised at planning time" notes per user story).

## Summary

Make `charter.resolver.DoctrineService` (`src/charter/resolver.py`) the sole, fully-gated access path to
provisioned doctrine assets. The mission (a) eliminates 5 of 7 flagged direct `AgentProfileRepository`
construction sites plus all 6 raw `DoctrineService` construction sites — excluding 2 sites that turned out
to access a legitimately separate `.kittify/profiles` directory (C-006) — (b) adds resolution methods to the
factory so the 5-tier template/command resolver axis and 2 additional in-charter sites stop importing
`doctrine.resolver` directly, (c) consolidates 3 duplicate missions-root path hardcodes onto one promoted
authority (deferring full `pack_paths` convergence to `#3091`), (d) extends factory activation-gating to 6
mechanical kinds and separately gates the structurally-different `mission-type` token via
`MissionTypeProfileRepository`, (e) unifies two divergent "canonical" builder functions discovered as a
byproduct, and (f) ships non-vacuous, zero-tolerance architectural gates so none of this quietly regresses.
Five adjacent GitHub issues (#2986, #3036, #3039, #3091, #3022) are confirmed out of scope and stay deferred.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: existing only — typer, ruamel.yaml, pydantic/dataclasses (`PackContext`,
  `ArtifactKind`), `importlib.resources` (`MissionTemplateRepository.default_missions_root()`); no new
  third-party dependencies
**Storage**: files — `.kittify/charter/charter.yaml`, `.kittify/profiles/` (explicitly untouched, C-006),
  `packs/built-in/`, `src/doctrine/missions/`
**Testing**: pytest; targeted surfaces per WP (see Project Structure below); existing named gates read but
  not duplicated — `tests/architectural/test_org_activation_seam.py`,
  `tests/architectural/test_layer_rules.py`, `tests/architectural/test_runtime_charter_doctrine_boundary.py`
  (referenced to confirm the "boundary ratchet" comment doesn't trip it); new non-vacuous gates per FR-007
**Target Platform**: Linux/macOS/Windows CLI
**Project Type**: single project (`src/{charter,doctrine,specify_cli,runtime,mission_runtime}/`)
**Performance Goals**: NFR-005 — p95 `spec-kitty agent tasks status` render latency on a 100+-WP fixture
  project stays within 10% of pre-mission baseline
**Constraints**: C-001 (one canonical factory, one unified builder); C-002 (zero exceptions for in-scope
  sites); C-003 (five issues + #3101 stay untouched); C-004 (PRs only, coord hygiene); C-005 (red-main
  discipline); C-006 (`.kittify/profiles` out of scope)
**Scale/Scope**: 9 FRs across 6 implementation concerns; 11 direct-construction sites (5 profile-repo + 6
  raw-service) + 3-consumer resolver axis + 3 hardcoded-path sites + 6 mechanical kinds + 1 separate
  mission-type repository + 1 builder unification + zero-tolerance gates for all four categories

## Charter Check

*GATE: Must pass before Phase 0 research. Re-checked after Phase 1 design.*

- **Single canonical authority** (Governing Principle; DIR-044). ✅ The mission's spine: `charter.resolver.
  DoctrineService` becomes the one factory every in-scope site routes through, built by one unified builder
  (FR-008) — the two-builder divergence found during planning is exactly the kind of second-authority drift
  this principle exists to close, and it is folded in rather than left standing.
- **Architectural alignment** (DIR-001). ✅ Respects the sanctioned `charter → doctrine` import direction;
  `doctrine/resolver.py`'s tier functions stay where they are (their own documented rationale for living
  there), only the entry point moves onto the factory (FR-003) — extends the existing pattern already proven
  at `specify_cli/runtime/resolver.py`'s tier-5 routing, rather than inventing a second charter-layer resolver
  object.
- **ATDD-first** (C-011). ✅ Every implementation WP commits a failing-first test (a red assertion that the
  bypass call exists, or that the ungated kind leaks unfiltered data) before the routing/gating change lands.
- **Non-vacuous gates** (DIR-043). ✅ FR-007's gates ship with self-mutation proofs per category, frozen
  zero-tolerance baselines (no allowlist, per C-002) — mirrors the WP10/WP11 idiom from
  `doctrine-charter-split-unification-01KZ0SRB`, extended rather than duplicated.
- **Fold only domain-matched debt** (Standing Order #2). ✅ FR-008 (builder unification) is folded in because
  it is the same factory this mission is already making the sole door; the five adjacent issues (#2986,
  #3036, #3039, #3091, #3022) are confirmed NOT domain-matched (research squad) and stay deferred; the
  `.kittify/profiles` sites are confirmed a different concern (C-006) and are excluded, not force-fitted.
- **Terminology canon.** ✅ Mission (not Feature) throughout; no `--feature` flags touched.
- **Git/workflow discipline** (DIR-045). ✅ Draft-PR-first; operator merges; coord topology
  (`kitty/mission-charter-sole-door-bypass-closure-01KZ3WAA`); issue-matrix row per folded issue.

No violations → Complexity Tracking empty.

## Project Structure

### Documentation (this mission)

```
kitty-specs/charter-sole-door-bypass-closure-01KZ3WAA/
├── plan.md              # This file
├── spec.md              # Mission spec (9 FR + 5 NFR + 6 C), revised post-Phase-0
├── research.md          # Phase 0 — the four planning-time corrections + design decisions
├── data-model.md        # Phase 1 — ArtifactKind→gating-owner map, three-state contract, builder contract
├── contracts/           # Phase 1 — DoctrineService public-surface contract, MissionTypeProfileRepository
│                         #   activation contract, unified-builder contract
├── quickstart.md         # Phase 1 — how to verify the sole-door property post-mission
└── tasks.md             # Phase 2 (/spec-kitty.tasks — NOT created here)
```

### Source Code (repository root)

```
src/
├── charter/
│   ├── resolver.py                    # THE factory (FR-002/003/005): +6 mechanical kind properties,
│   │                                   #   +resolution methods for the 5-tier axis, +unfiltered mode
│   ├── resolution.py                  # retarget onto new factory methods (FR-003)
│   ├── context_renderers/template_include.py  # retarget onto new factory methods (FR-003)
│   ├── template_resolver.py           # CharterTemplateResolver — becomes a thin delegate or is retired
│   │                                   #   in favour of direct factory use (FR-003)
│   ├── profile_resolution.py          # route :81 through the factory (FR-001)
│   ├── compiler.py                    # route :802 through the factory (FR-002)
│   ├── mission_type_profile_repository.py  # builtin_missions_root() → promoted authority (FR-004);
│   │                                   #   MissionTypeProfileRepository gains activation filtering (FR-006)
│   ├── mission_type_profiles.py       # resolve_mission_type_context() activation-aware (FR-006)
│   ├── doctrine_service_builder.py    # unify with specify_cli's builder (FR-008)
│   └── pack_context.py                # read-only reference — activated_<kind> fields already exist (FR-005)
├── doctrine/
│   ├── resolver.py                    # UNCHANGED — tier functions stay here (FR-003 rationale)
│   ├── service.py                     # read-only reference — raw per-kind properties already exist
│   └── missions/repository.py         # MissionTemplateRepository.default_missions_root() — PROMOTED
│                                       #   to single authority (FR-004), no code change, just new callers
├── specify_cli/
│   ├── doctrine_service_factory.py    # unify with charter's builder (FR-008)
│   ├── invocation/registry.py         # UNCHANGED at :48 (.kittify/profiles, C-006)
│   ├── runtime/home.py                # dev_roots :107-108 → promoted authority (FR-004)
│   ├── tool_surface/profiles/projection.py  # route :84 through factory + new lineage accessor (FR-001)
│   └── cli/commands/
│       ├── profiles_cmd.py            # UNCHANGED at :83 (.kittify/profiles, C-006)
│       ├── agent/tasks_status_cmd.py  # route :712,:823 through factory; NFR-005 latency measurement (FR-001)
│       ├── _doctrine_asset.py         # route :75 through factory (FR-002)
│       └── _doctrine_collect.py       # route :191,:281,:418,:826 through factory UNFILTERED mode (FR-002)
├── runtime/next/runtime_bridge_io.py  # route :576 through factory (FR-001)
tests/architectural/
├── test_org_activation_seam.py        # existing — extended, not duplicated
├── test_layer_rules.py                # existing — read-only reference
├── test_runtime_charter_doctrine_boundary.py  # existing — read-only reference (confirms non-blocking)
└── <new> test_charter_sole_door_*.py  # zero-tolerance gates, one per closed bypass category (FR-007)
```

**Structure Decision**: Single-project layered `src/` — no new top-level trees. All in-scope construction,
resolution, and path-authority changes land inside the existing `charter`/`doctrine`/`specify_cli` layers;
nothing crosses the sanctioned `charter → doctrine` direction upward, and the two `.kittify/profiles` sites
are deliberately left untouched in place (C-006) rather than moved.

## Complexity Tracking

*No charter-check violations — none.*

## Implementation Concern Map

> Concerns are NOT work packages. `/spec-kitty.tasks` translates these into executable WPs — one concern may
> become several WPs, and small concerns may merge.

### IC-01 — Direct construction sites eliminated + builder unification

- **Purpose**: Close the 11 in-scope direct-construction bypasses (5 `AgentProfileRepository` + 6 raw
  `DoctrineService`) and the single-canonical-authority gap between the two builder functions that construct
  the factory itself.
- **Relevant requirements**: FR-001, FR-002, FR-008, NFR-001, NFR-005, C-002, C-006.
- **Affected surfaces**: `runtime_bridge_io.py:576`, `projection.py:84`, `tasks_status_cmd.py:712,823`,
  `charter/profile_resolution.py:81`, `charter/compiler.py:802`, `_doctrine_asset.py:75`,
  `_doctrine_collect.py:191,281,418,826`, `charter/doctrine_service_builder.py`,
  `specify_cli/doctrine_service_factory.py`.
- **Sequencing/depends-on**: unify the builders (FR-008) FIRST — every other site in this concern constructs
  through the (about-to-be-unified) builder, so fixing the divergence after routing sites through it would
  mean touching them twice. `projection.py:84`'s new lineage accessor is a small factory addition that should
  land alongside the builder unification, before its call site is migrated.
- **Risks**: `projection.py:84` and `runtime_bridge_io.py:576` need capabilities (mutation, lineage
  composition) the filtered wrapper doesn't expose today — a naive swap breaks them; the accessor design
  needs a focused ATDD test proving lineage/mutation still works post-migration. The two
  `tasks_status_cmd.py` sites need the NFR-005 latency measurement BEFORE claiming the fix is complete, not
  as an afterthought. `_doctrine_collect.py`'s 4 sites must use the unfiltered mode explicitly — a plain
  activation-aware swap there is a silent regression (narrows doctor/health output), not a fix.

### IC-02 — Template/command resolver axis routed through the factory

- **Purpose**: Give `charter.resolver.DoctrineService` resolution methods for the 5-tier axis so
  `CharterTemplateResolver` and the 2 additional in-charter sites found during planning stop importing
  `doctrine.resolver` directly.
- **Relevant requirements**: FR-003, NFR-001, SC-002.
- **Affected surfaces**: `charter/resolver.py` (new methods), `charter/template_resolver.py`,
  `charter/resolution.py`, `charter/context_renderers/template_include.py`.
- **Sequencing/depends-on**: independent of IC-01; can run in parallel.
- **Risks**: `doctrine/resolver.py`'s tier functions must NOT move — moving them fights the module's own
  documented rationale for living there (charter needs to import doctrine, not vice versa). The
  `specify_cli/runtime/resolver.py` tier-1-4 reimplementation is a noted semantic-drift risk but is
  explicitly OUT of this concern's scope (not a bypass; do not touch it here).

### IC-03 — Missions-root path consolidation

- **Purpose**: Retarget the 3 duplicate missions-root hardcodes onto one promoted authority.
- **Relevant requirements**: FR-004, NFR-004, C-003, SC-003.
- **Affected surfaces**: `charter/mission_type_profile_repository.py:66`, `specify_cli/runtime/home.py:
  107-108`; `doctrine/missions/repository.py:98` (read-only — the promoted authority, no code change).
- **Sequencing/depends-on**: independent; small, mechanical.
- **Risks**: do not claim convergence with `doctrine.pack_paths.built_in_dir` in the PR description — that is
  `#3091`'s to deliver (NFR-004 requires this be stated explicitly, not implied away).

### IC-04 — Factory activation-gating extended to all 10 kinds (two shapes of work)

- **Purpose**: Close the "3 of 10 gated" gap — 6 kinds mechanically on the factory, 1 token (`mission-type`)
  structurally elsewhere.
- **Relevant requirements**: FR-005, FR-006, NFR-004, SC-004.
- **Affected surfaces**: `charter/resolver.py` (6 new properties, copy-paste of the `paradigms` pattern),
  `charter/mission_type_profile_repository.py` / `charter/mission_type_profiles.py` (new, non-mechanical
  filtering).
- **Sequencing/depends-on**: FR-005 (mechanical) and FR-006 (mission-type) are independent of each other;
  FR-005 can run in parallel with IC-01/IC-02/IC-03. FR-006 should NOT be estimated or scheduled as if it
  were the same size as FR-005's six kinds — it is a different repository with no existing three-state
  precedent to copy.
- **Risks**: a bare-project regression per kind is mandatory (mirrors the `charter-pack-usage-journey`
  bare-project pin) — the classic failure mode here is a naive `sorted(activated or frozenset())` that
  silently empties a project that never activated anything.

### IC-05 — Durability gates + deferred-issue documentation

- **Purpose**: Ship the zero-tolerance, self-mutation-proven gates for all four bypass categories, and record
  the five confirmed-deferred issues in the PR description.
- **Relevant requirements**: FR-007, FR-009, NFR-003, SC-005, SC-006.
- **Affected surfaces**: `tests/architectural/` (new gate files), PR description.
- **Sequencing/depends-on**: MUST run AFTER IC-01/IC-02/IC-03/IC-04 land — a zero-tolerance gate written
  before the bypasses are closed would either be vacuous (pass despite the bypasses) or immediately red
  (fail before any fix lands); neither is useful. Land last.
- **Risks**: the WP10 lesson applies directly — a gate that doesn't actually walk in-function/nested-scope
  constructs is worse than no gate (manufactures false confidence). Each new gate needs its own self-mutation
  proof, not a shared one.
