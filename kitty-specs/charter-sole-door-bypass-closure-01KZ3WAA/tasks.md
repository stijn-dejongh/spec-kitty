# Tasks: Charter as Sole Door: Close Bypass Access Paths

**Input**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `contracts/`, `quickstart.md` from
`kitty-specs/charter-sole-door-bypass-closure-01KZ3WAA/`

Subtask completion is event-sourced (`spec-kitty agent tasks mark-status <Txxx> --status done`), not a
markdown checkbox. Rows below are reference only.

## Subtask Index

| ID | Description | WP | Parallel |
|----|---|----|----|
| T001 | Pin lineage/mutation accessor semantics + implement on `charter.resolver.DoctrineService` | WP01 | |
| T002 | Unify the two named builder functions into one (`active_languages` always computed, `org_roots` always self-resolved) | WP01 | |
| T003 | Retarget `org_layer.py:244,275` and `generate.py:56` onto the unified builder; fix fail-open `except ImportError: pass` | WP01 | |
| T004 | Regression test: unified builder identical output across the 3 pre-existing gated kinds + builder kwargs | WP01 | |
| T005 | ATDD test: accessor's two pinned semantics (mutation does not leak through filter; lineage traversal reads raw) | WP01 | |
| T006 | Capture pre-mission p95 baseline for `spec-kitty agent tasks status` on a 100+-WP fixture; record in tracer file | WP02 | |
| T007 | Migrate `runtime_bridge_io.py:576` onto the factory via WP01's accessor | WP02 | [P] |
| T008 | Migrate `projection.py:84` onto the factory via WP01's accessor | WP02 | [P] |
| T009 | Migrate `tasks_status_cmd.py:712,823` onto the factory; re-measure p95, compare against T006 baseline | WP02 | |
| T010 | Migrate `charter/profile_resolution.py:81` onto the factory | WP02 | [P] |
| T011 | Migrate `charter/compiler.py:802` onto the factory | WP03 | [P] |
| T012 | Migrate `_doctrine_asset.py:75` onto the factory | WP03 | [P] |
| T013 | Migrate `_doctrine_collect.py`'s 4 sites onto the factory's unfiltered mode (`pack_context=None`) | WP03 | |
| T014 | Regression test: unfiltered mode returns catalog identical to the raw unwrapped service | WP03 | |
| T015 | Migrate `registry.py:64` off `._inner.agent_profiles` onto WP01's accessor | WP04 | [P] |
| T016 | Migrate `org_profiles.py:117` off `._inner.agent_profiles` onto WP01's accessor | WP04 | [P] |
| T017 | ATDD test: zero `._inner` attribute access remains at either site | WP04 | |
| T018 | Add resolution methods to `charter.resolver.DoctrineService` delegating to `doctrine/resolver.py`'s tier functions | WP05 | |
| T019 | Resolve the construction-contract mismatch for `CharterTemplateResolver`'s one real caller (`repo_root` vs `missions_root`) | WP05 | |
| T020 | Retarget `CharterTemplateResolver` (thin delegate or retire in favour of direct factory use) | WP05 | |
| T021 | Regression test: tier resolution via factory matches the old direct-call result | WP05 | |
| T022 | Make `builtin_missions_root()` a thin delegate to `MissionTemplateRepository.default_missions_root()` | WP06 | [P] |
| T023 | Retarget `runtime/home.py`'s `dev_roots` fallback onto `default_missions_root()` | WP06 | [P] |
| T024 | Equality regression test for both retargeted sites | WP06 | |
| T025 | Document `home.py`'s residual `#2986`-shared risk and the `#3091`-deferred `pack_paths` convergence in the PR description | WP06 | |
| T026 | Add `directives` property to `charter.resolver.DoctrineService` | WP07 | [P] |
| T027 | Add `tactics` property | WP07 | [P] |
| T028 | Add `styleguides` property | WP07 | [P] |
| T029 | Add `toolguides` property | WP07 | [P] |
| T030 | Add `mission_step_contracts` property | WP07 | [P] |
| T031 | Add `glossary_packs` property | WP07 | [P] |
| T032 | Bare-project equality regression test per kind (6 tests): wrapped == unwrapped inner service | WP07 | |
| T033 | Extend WP01's builder-unification regression test (T004) to assert identical output across all 9 gated properties | WP07 | |
| T034 | Add activation filtering to `MissionTypeProfileRepository` / `resolve_mission_type_context()` | WP08 | |
| T035 | Bare-project regression test: set-equality against `builtin_mission_type_id_set()` | WP08 | |
| T036 | Regression test: a subset of activated mission-types returns only that subset | WP08 | |
| T037 | Gate 1: zero-tolerance, qualname-resolving `AgentProfileRepository` gate + composite-key exclusions + self-mutation proof | WP09 | [P] |
| T038 | Gate 2: zero-tolerance, qualname-resolving `DoctrineService` gate + composite-key exclusions + self-mutation proof | WP09 | [P] |
| T039 | Gate 3: `doctrine.resolver` direct-import gate (outside `src/charter/**`) + self-mutation proof | WP09 | [P] |
| T040 | Gate 4: hardcoded missions-root path-literal gate + self-mutation proof | WP09 | [P] |
| T041 | Gate 5: `._inner` attribute-access gate (outside `src/charter/**`) + self-mutation proof | WP09 | [P] |
| T042 | Add `issue-matrix.json` rows for #2986/#3036/#3039/#3091/#3022 (`verdict: deferred-with-followup`) | WP10 | [P] |
| T043 | Post a tracker comment naming this mission on each of the 5 deferred issues | WP10 | [P] |

## Work Packages

### WP01 — Unify construction paths + lineage/mutation accessor (Priority: P1)

**Goal**: One canonical builder function; one new factory accessor for lineage/mutation operations.
**Requirements**: FR-008, FR-001 (accessor design), FR-010 (accessor design), C-001.
**Independent test**: construct the unified builder from both former call sites' inputs — identical output.
**Subtasks**: T001-T005. **Dependencies**: none. **Estimated size**: ~350 lines.
**Risks**: the accessor's two semantic questions are pinned in `contracts/charter-doctrine-service-contract.md`
— implement against that text, do not re-derive.

### WP02 — Migrate `AgentProfileRepository` sites + NFR-005 measurement (Priority: P1)

**Goal**: Close the 5 in-scope direct `AgentProfileRepository` construction sites; prove no perf regression.
**Requirements**: FR-001, NFR-005.
**Independent test**: grep confirms zero direct construction at these 5 sites; p95 latency within 10% of baseline.
**Subtasks**: T006-T010. **Dependencies**: WP01. **Estimated size**: ~400 lines.
**Risks**: T006 MUST run before T009 touches `tasks_status_cmd.py` — the baseline is worthless captured after.

### WP03 — Migrate raw `DoctrineService` sites (Priority: P1)

**Goal**: Close the 9 in-scope raw `DoctrineService` construction sites (6 original + 3 found by the
post-plan squad), using the factory's unfiltered mode where diagnostic completeness requires it.
**Requirements**: FR-002.
**Independent test**: grep confirms zero raw construction outside the factory/builder; `_doctrine_collect.py`
diagnostics still see the full unfiltered catalog.
**Subtasks**: T011-T014. **Dependencies**: WP01. **Estimated size**: ~350 lines.
**Risks**: a plain activation-aware swap on `_doctrine_collect.py` silently narrows doctor/health output —
must use `pack_context=None` explicitly.

### WP04 — Close the `._inner` reach-around (Priority: P1)

**Goal**: Eliminate the escape hatch that would otherwise defeat every other WP's gating.
**Requirements**: FR-010.
**Independent test**: zero `._inner` attribute access on a `charter.resolver.DoctrineService` outside `src/charter/**`.
**Subtasks**: T015-T017. **Dependencies**: WP01. **Estimated size**: ~200 lines.

### WP05 — Route the template/command resolver axis through the factory (Priority: P1)

**Goal**: `CharterTemplateResolver`'s one real caller stops importing `doctrine.resolver` directly.
**Requirements**: FR-003.
**Independent test**: no consumer outside `src/charter/**` imports `doctrine.resolver`; tier resolution results unchanged.
**Subtasks**: T018-T021. **Dependencies**: WP01 (T018 adds methods to `src/charter/resolver.py`, which WP01
exclusively owns — a sequenced, dependency-gated out-of-map edit, not a declared overlap).
**Estimated size**: ~350 lines.
**Risks**: `doctrine/resolver.py`'s tier functions must NOT move; `doctrine.template_catalog` and
`runtime/resolver.py`'s tier 1-4 reimplementation are explicitly OUT of scope — do not touch them.

### WP06 — Consolidate missions-root path hardcodes (Priority: P1)

**Goal**: Retarget the 3 duplicate missions-root hardcodes onto one promoted authority.
**Requirements**: FR-004.
**Independent test**: equality regression test — both retargeted sites resolve identically to
`default_missions_root()`.
**Subtasks**: T022-T025. **Dependencies**: none (parallel). **Estimated size**: ~250 lines.
**Risks**: do not claim `pack_paths.built_in_dir` convergence — that's `#3091`'s to deliver.

### WP07 — Extend factory activation-gating to 6 mechanical kinds (Priority: P1)

**Goal**: `charter.resolver.DoctrineService` gates `directive`/`tactic`/`styleguide`/`toolguide`/
`mission_step_contract`/`glossary_pack`, mirroring the existing `paradigms` pattern exactly.
**Requirements**: FR-005, FR-008 (proof extension).
**Independent test**: a bare project's catalog for each of the 6 kinds equals the raw unwrapped service's output.
**Subtasks**: T026-T033. **Dependencies**: WP01, WP05 (T026-T031 edit `src/charter/resolver.py`, exclusively
owned by WP01; sequenced after WP05 too, so this WP never runs in parallel with either — a dependency-gated
out-of-map edit, not a declared overlap). T033 also touches WP01's test file, same rationale.
**Estimated size**: ~450 lines.
**Risks**: T032's assertion MUST be equality against the unwrapped service, not an existence check
(a partial leak passes an existence check).

### WP08 — Mission-type activation gating (Priority: P1)

**Goal**: Gate the `mission-type` token via `MissionTypeProfileRepository`, not `DoctrineService`.
**Requirements**: FR-006.
**Independent test**: a bare project's mission-type set equals `builtin_mission_type_id_set()`; an activated
subset returns only that subset.
**Subtasks**: T034-T036. **Dependencies**: none (parallel). **Estimated size**: ~250 lines.
**Risks**: T035's assertion MUST be set-equality against `builtin_mission_type_id_set()`, not a fakeable
subset check ("at least these 4 types").

### WP09 — Durability gates for all five bypass categories (Priority: P2)

**Goal**: Ship non-vacuous, zero-tolerance, qualname-resolving architectural gates so none of WP01-08's
closures can silently regress.
**Requirements**: FR-007, NFR-001, NFR-003.
**Independent test**: each gate's self-mutation proof (function-local/nested injection) fails when the
guarded shape is reintroduced, naming the offending site.
**Subtasks**: T037-T041. **Dependencies**: WP01, WP02, WP03, WP04, WP05, WP06, WP07, WP08 (must run LAST —
a gate written before the bypasses close is either vacuous or immediately red).
**Estimated size**: ~500 lines.
**Risks**: the WP10-precedent lesson applies directly — a gate using `pytestarch`/module-level-only scanning
is worse than no gate. `.kittify/profiles` and `_doctrine_collect.py` exclusions MUST be composite-key
(file+qualname+line), never whole-file.

### WP10 — Deferred-issue tracker hygiene (Priority: P2)

**Goal**: Give the five confirmed-deferred issues a durable tracker trace, not just PR-description prose.
**Requirements**: FR-011.
**Independent test**: each of #2986/#3036/#3039/#3091/#3022 carries an `issue-matrix.json` row and a tracker
comment naming this mission.
**Subtasks**: T042-T043. **Dependencies**: none (fully independent of code; can run any time).
**Estimated size**: ~120 lines.

## Sequencing Summary

```
WP01 ─┬─> WP02 ────────────────┐
      ├─> WP03 ────────────────┤
      ├─> WP04 ────────────────┤
      └─> WP05 ──> WP07 ───────┤──> WP09 (durability gates, last; depends on WP01-08)
WP06 ────────────────────────┤
WP08 ────────────────────────┘
WP10 (fully independent, any time)
```

Note: `src/charter/resolver.py` is edited by WP01 (accessor), WP05 (tier-axis methods), and WP07 (6
mechanical properties) — WP01 is its sole *declared* owner; WP05 and WP07's edits there are sequenced,
dependency-gated out-of-map additions (WP05 depends on WP01; WP07 depends on WP01 AND WP05), never
parallel, so no ownership conflict reaches `finalize-tasks`'s lane computation.

MVP scope: WP01-04 (the direct-construction closure + accessor) delivers the largest single chunk of the
"sole door" claim independently of WP05-08's gating/axis work.
