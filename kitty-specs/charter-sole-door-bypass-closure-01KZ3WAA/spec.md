# Mission Specification: Charter as Sole Door: Close Bypass Access Paths

**Mission Branch**: `feat/charter-sole-door-bypass-closure`
**Created**: 2026-08-03
**Status**: Draft
**Input**: User description: "Go for item 2 [charter-as-sole-door bypass closure], see if the others can be (partially) folded in. Launch a research squad to ground the work, then proceed to spec."

## User Scenarios & Testing *(mandatory)*

The users are the **runtime** (the code paths that reach provisioned doctrine assets while executing a
mission) and the **maintainer** who needs one enforced answer to "how does the runtime reach a doctrine
asset?" The failure today: `charter.resolver.DoctrineService` (`src/charter/resolver.py:57-139`) is a
*canonical factory* that activation-gates only 3 of 10 doctrine-artifact kinds (`paradigm`, `procedure`,
`agent_profile`) and forwards the other 7 (`directive`, `tactic`, `styleguide`, `toolguide`,
`mission_step_contract`, `glossary_pack`, and the `mission-type` token) unfiltered via `__getattr__`. Worse,
it is *one of many* entry points: roughly 20 call sites across four categories reach doctrine assets
without going through the factory at all — some with code comments explicitly citing reasons for avoiding
it (a "runtime→charter→doctrine boundary ratchet"). This is the G1 done-bar named in
`docs/plans/3-2-x-open-core-delivery-plan.md` §2.2 item 1: "All provisioned assets reachable by the runtime
*through* the charter — charter as the sole door. This is a *no-bypass* condition: any path that reaches
assets around the charter is a second seam that leaks internals and forces a *second* break later."

A pre-spec research squad enumerated the concrete bypass list (this spec's FR anchors), extracted the
established "make X the sole door" pattern from `charter-pack-usage-journey-01KYWWTF`, extracted the
non-vacuous-gate idiom from `doctrine-charter-split-unification-01KZ0SRB` (WP10/WP11), and assessed five
adjacent GitHub issues (#2986, #3036, #3039, #3091, #3022) for fold-in — all five came back
**ADJACENT-BUT-SEPARATE**: same governing principle or same "gate enforces the bug it should catch" shape,
but a different code surface, violation class, or track (import-direction ratchets, doctrine-content
shippability, doctrine-tree relocation, pack extraction) than access-path bypass closure. They stay
deferred as their own missions (C-003).

### User Story 1 — Direct repository/service construction goes through the factory, no exceptions (Priority: P1)

Seven call sites construct `AgentProfileRepository(...)` directly, and six construct the raw
`doctrine.service.DoctrineService(...)` directly, bypassing `charter.resolver.DoctrineService` entirely.
Two of the `AgentProfileRepository` sites (`src/specify_cli/cli/commands/agent/tasks_status_cmd.py:712,823`,
dashboard status icons) carry code comments explicitly justifying the bypass as avoiding a
"runtime→charter→doctrine boundary ratchet"; `src/specify_cli/cli/commands/profiles_cmd.py:83` is documented
as a deliberately-ungated CLI display surface. Per operator decision, this mission does **not** grandfather
these as exceptions — it eliminates every site, which means first understanding and resolving whatever
concern each comment names (e.g., a lazy-construction, caching, or import-timing reason), not just deleting
the comment and routing through the factory blindly.

**Why this priority**: this is the largest concrete bypass count (13 of ~20 sites) and the one with the most
"this bypass exists for a stated reason" risk — get it wrong and either a regression ships (the avoided
ratchet reappears) or the "no exceptions" decision quietly regresses into a new allowlist.

**Independent Test**: grep `src/` for `AgentProfileRepository(` and `DoctrineService(` outside
`src/charter/resolver.py` and its two builder functions
(`specify_cli.doctrine_service_factory.build_activation_aware_doctrine_service`,
`charter.doctrine_service_builder._build_activation_aware_doctrine_service`) — zero matches.

**Acceptance Scenarios**:

1. **Given** the dashboard status-icon renderer (`tasks_status_cmd.py:712,823`), **When** it needs an agent
   profile, **Then** it resolves through `charter.resolver.DoctrineService`, and the concern the removed
   comment named (the boundary ratchet) is proven not to reappear — either because it was never a real risk
   for this call shape, or because the underlying cause (e.g. eager construction cost) is fixed.
2. **Given** `profiles_cmd.py`'s CLI display surface, **When** it lists agent profiles, **Then** it resolves
   through the factory and still displays every profile a raw, ungated read would have shown (a display
   surface must not silently narrow what it shows as a side effect of gating).
3. **Given** `src/charter/compiler.py:802` and the four `_doctrine_collect.py` sites, **When** they read
   `.agent_profiles` / `.glossary_packs` from a raw `DoctrineService`, **Then** they read the same data
   through `charter.resolver.DoctrineService` instead.

---

### User Story 2 — The 5-tier template/command resolver axis goes through the factory (Priority: P1)

`src/doctrine/resolver.py::_resolve_asset` resolves templates/commands across five tiers (OVERRIDE, LEGACY,
GLOBAL_MISSION, GLOBAL, PACKAGE_DEFAULT), and `resolve_mission` duplicates four of those tiers again for
mission-type resolution. Neither routes through the charter factory; `charter.template_resolver.
CharterTemplateResolver` calls the raw resolver directly. This axis has no activation concept at all today.

**Why this priority**: it is a whole resolution axis, not a single call site — every template/command
render in the product currently bypasses the sole door.

**Independent Test**: `CharterTemplateResolver` and any other consumer of `doctrine/resolver.py`'s tier
functions reach them only via the charter factory; a direct import of `doctrine.resolver` from outside
`src/charter/**` is the new bypass-door signature this mission eliminates.

**Acceptance Scenarios**:

1. **Given** a project with an OVERRIDE-tier template, **When** `CharterTemplateResolver` resolves it,
   **Then** the resolution call passes through the charter factory and returns the same template a direct
   `doctrine.resolver` call would have.
2. **Given** `resolve_mission`'s duplicated tier logic, **When** it is retargeted, **Then** the duplication
   with `_resolve_asset` is resolved through the factory without silently diverging tier semantics between
   the two call paths.

---

### User Story 3 — Hardcoded source-tree paths resolve through the canonical path authority (Priority: P1)

Two sites hardcode a doctrine-asset root instead of using `doctrine.pack_paths.built_in_dir`:
`src/charter/mission_type_profile_repository.py:66::builtin_missions_root()`
(`Path(__file__).resolve().parents[1]/"doctrine"/"missions"`) and
`src/specify_cli/runtime/home.py:107-108`'s `dev_roots` fallback tuple.

**Why this priority**: a hardcoded path is a silent, hard-to-grep bypass that survives even after every
repository-construction site is fixed — and it is exactly the kind of thing `#3091`'s eventual
`missions/` → `packs/built-in` relocation would silently break if left in place.

**Independent Test**: neither file contains a literal `Path(__file__)`-relative doctrine-asset-root
construction; both resolve through `doctrine.pack_paths`.

**Acceptance Scenarios**:

1. **Given** a standard install, **When** `builtin_missions_root()` is called, **Then** it returns the same
   path `doctrine.pack_paths.built_in_dir` would resolve, proven by an equality regression test (not just
   "still returns a path").
2. **Given** a dev checkout, **When** `runtime/home.py` resolves its dev-root fallback, **Then** it uses the
   canonical resolver instead of the duplicated literal tuple.

---

### User Story 4 — The factory activation-gates all 10 doctrine-artifact kinds (Priority: P1)

`charter.resolver.DoctrineService` filters exactly 3 properties (`paradigms`, `procedures`,
`agent_profiles`); every other property falls through `__getattr__` to the raw inner service, unfiltered.
Per operator decision, this mission extends activation-gating to the remaining 7 kinds (`directive`,
`tactic`, `styleguide`, `toolguide`, `mission_step_contract`, `glossary_pack`, plus the `mission-type`
token), so "sole door" and "gated" are not two different claims — routing every call site through the
factory (User Stories 1-3) would otherwise still leak ungated data for 7 of 10 kinds.

**Why this priority**: without this, User Stories 1-3 make the factory the sole *path* without making it a
real *gate* for most of what travels through that path — the "3 of 10 kinds" gap is the other half of the
G1 done-bar, not a separate concern.

**Independent Test**: for each of the 7 currently-ungated kinds, a project with that pack tier deactivated
returns a filtered (non-empty-catalog-default or explicitly-empty, per the three-state semantics below)
result from the factory property, not the raw unfiltered catalog.

**Acceptance Scenarios**:

1. **Given** a bare project with no activated packs, **When** the factory resolves a previously-ungated
   kind (e.g. `directives`), **Then** it returns the same three-state semantics already proven for
   `directives` resolution elsewhere in the codebase (`None` → catalog default; `frozenset()` → explicit
   opt-out, empty; `{ids}` → filtered) — not a naive `sorted(activated or frozenset())` regression that
   silently empties a bare project's default catalog.
2. **Given** a project with a subset of `glossary_pack`s activated, **When** the factory resolves
   `glossary_packs`, **Then** only the activated subset is returned.

---

### User Story 5 — A new bypass cannot be silently reintroduced (Priority: P2)

Closing today's ~20 bypass doors is only durable if a future PR cannot casually reopen one. This mirrors
the charter's architectural-gate-discipline standing order and the WP10 (`test_charter_no_specify_cli_
import.py`) / WP11 (`test_charter_path_literal_authority.py`) precedent from `doctrine-charter-split-
unification-01KZ0SRB` — except here the operator has chosen a **zero-tolerance frozen baseline**, not a
shrink-only allowlist, because User Story 1 already rejected keeping any site as a permitted exception.

**Why this priority**: P2, not P1 — it is the durability guarantee on top of User Stories 1-4's actual
closure, not the closure itself; a mission that closes the doors without a gate still delivers the SC-001
outcome, just without the anti-regression guarantee.

**Independent Test**: reintroduce any one of the four closed bypass shapes (a raw `AgentProfileRepository(`
construction, a raw `DoctrineService(` construction, a direct `doctrine.resolver` import from outside
`src/charter/**`, or a hardcoded doctrine-asset-root literal) in a scratch module and confirm the new
gate(s) go red, naming the exact site — proving the gate is non-vacuous (mirrors NFR-004 of the WP10/WP11
precedent).

**Acceptance Scenarios**:

1. **Given** the gate(s) shipped by this mission, **When** a self-mutation test reintroduces each closed
   bypass shape, **Then** the relevant gate fails and names the offending file/line.
2. **Given** `tests/architectural/test_org_activation_seam.py` and `tests/architectural/test_layer_rules.py`
   (existing, narrower coverage), **When** the new gates are added, **Then** they extend rather than
   duplicate that existing coverage — no two gates assert the same fact.

### Edge Cases

- What happens when a project has activated **no** packs at all? Extending activation-gating to the 7
  previously-unfiltered kinds (User Story 4) must preserve the existing three-state semantics
  (`None`/`frozenset()`/`{ids}`) proven for the 3 already-gated kinds — a bare project must keep seeing its
  full built-in default catalog for those 7 kinds, not silently see it empty out.
- What happens when a call site needs a doctrine asset **before** the charter factory itself is
  constructible (e.g., during the charter compilation pass that produces the very config the factory reads,
  or during agent-profile resolution used to pick which profile loads the charter)? This bootstrap/circularity
  case is the most likely reason a "no exceptions" site turns out to be genuinely irreducible — the mission
  must surface this to the operator as a scoped finding rather than silently allowlisting it (C-002).
- How does the system handle a dashboard render loop calling the factory at a frequency where the earlier
  bypass comment's stated concern (a "boundary ratchet") was actually a real performance guard, not just
  caution? NFR-005 requires measuring this, not assuming it away.

## Requirements *(mandatory)*

### Functional Requirements

| ID | Requirement | Status |
|----|-------------|--------|
| FR-001 | Eliminate the 7 direct `AgentProfileRepository(...)` construction sites outside `charter.resolver.DoctrineService` and its two builder functions: `src/specify_cli/invocation/registry.py:48`, `src/runtime/next/runtime_bridge_io.py:576`, `src/specify_cli/tool_surface/profiles/projection.py:84`, `src/specify_cli/cli/commands/profiles_cmd.py:83`, `src/specify_cli/cli/commands/agent/tasks_status_cmd.py:712` and `:823`, `src/charter/profile_resolution.py:81`. Per operator decision (no allowlist exceptions): for the two sites whose comments cite avoiding a "runtime→charter→doctrine boundary ratchet," first investigate and resolve the underlying concern (lazy construction, caching, or import-timing) so the site can route through the factory without regressing whatever it was avoiding; a site proven genuinely infeasible is a blocking finding for the operator (C-002), not a silent allowlist entry. | Draft |
| FR-002 | Eliminate the 6 unwrapped raw `doctrine.service.DoctrineService(...)` construction sites — `src/charter/compiler.py:802`, `src/specify_cli/cli/commands/_doctrine_asset.py:75`, `src/specify_cli/cli/commands/_doctrine_collect.py:191`, `:281`, `:418`, `:826` — routing each through `charter.resolver.DoctrineService` instead of the raw inner service. | Draft |
| FR-003 | Retarget the 5-tier template/command resolver axis (`src/doctrine/resolver.py::_resolve_asset`, tiers OVERRIDE/LEGACY/GLOBAL_MISSION/GLOBAL/PACKAGE_DEFAULT, ~lines 164-213) and its duplicated tier logic in `resolve_mission` (~lines 284-342) so `charter.template_resolver.CharterTemplateResolver` — and any other consumer — reaches these tiers only through the charter factory, never by importing `doctrine.resolver` directly from outside `src/charter/**`. | Draft |
| FR-004 | Retarget the two hardcoded source-tree paths onto the canonical path authority: `src/charter/mission_type_profile_repository.py:66::builtin_missions_root()` (currently `Path(__file__).resolve().parents[1]/"doctrine"/"missions"`) onto `doctrine.pack_paths.built_in_dir`; `src/specify_cli/runtime/home.py:107-108`'s hardcoded `dev_roots` fallback tuple onto the same canonical resolver. Ship an equality regression test proving both now resolve identically to the canonical resolver's output, not merely "still return a path." | Draft |
| FR-005 | Extend `charter.resolver.DoctrineService` (`src/charter/resolver.py:57-139`) to activation-gate the 7 currently-unfiltered kinds — `directive`, `tactic`, `styleguide`, `toolguide`, `mission_step_contract`, `glossary_pack`, and the `mission-type` token — replacing the `__getattr__` unfiltered passthrough (lines 136-139) for those kinds with the same three-state activation-aware filtering (`None`=catalog default / `frozenset()`=explicit empty opt-out / `{ids}`=filtered) already proven for the 3 existing gated kinds. Ship a bare-project regression test per newly-gated kind proving the default catalog is NOT silently emptied (mirrors the `charter-pack-usage-journey` bare-project pin). | Draft |
| FR-006 | Ship non-vacuous architectural gate(s) (AST-walk or call-site-census style, self-mutation proven, per the WP10 idiom) for each of the four closed bypass categories (FR-001/002/003/004), with a frozen **zero-tolerance** baseline — no shrink-only allowlist, per the operator's "no exceptions" decision (C-002). Extend `tests/architectural/test_org_activation_seam.py` and `tests/architectural/test_layer_rules.py` where their existing coverage is adjacent; do not re-assert what they already prove. | Draft |
| FR-007 | Record in the PR description, as explicit deferred follow-ons (not silently dropped), that #2986, #3036, #3039, #3091, and #3022 were assessed by a pre-spec research squad and confirmed adjacent-but-separate — each with its one-line reason (different pair/violation-class/track) — so a later reader does not mistake "closed the bypass doors" for "closed those issues too." | Draft |

### Non-Functional Requirements

| ID | Requirement | Threshold / Measure | Status |
|----|-------------|---------------------|--------|
| NFR-001 | Zero raw bypass call sites remain, provably. | `grep -rn` for `AgentProfileRepository(` and `DoctrineService(` across `src/` returns zero matches outside `src/charter/resolver.py` and its two builder functions; a committed architectural test asserts this (not a one-time manual grep). | Draft |
| NFR-002 | No new lint/type regressions. | `ruff` + `mypy --strict` zero new issues on all changed modules; no new `# noqa` / `# type: ignore` / per-file ignore additions. | Draft |
| NFR-003 | Every new gate is non-vacuous. | Each gate shipped under FR-006 has a self-mutation test that reintroduces the exact closed bypass shape and asserts the gate fails naming the offending site — proven for all four categories, not a sample. | Draft |
| NFR-004 | Behaviour change is explicit, not slipped. | CHANGELOG entry (per DIR-009) documents that the factory now activation-gates all 10 kinds (previously 3) — a project that activates a subset of a newly-gated kind's packs will see a narrower result than before this mission; this is named as an intentional behaviour change, not discovered later as a regression. | Draft |
| NFR-005 | No unmeasured performance regression on the sites the "boundary ratchet" comments were guarding. | p95 render latency for `spec-kitty agent tasks status` on a fixture project with 100+ work packages stays within 10% of the pre-mission baseline measured on the same fixture; if it regresses beyond that, the underlying cause named in FR-001 (e.g. eager construction cost) is fixed architecturally (caching, lazy init) rather than accepted. | Draft |

### Constraints

| ID | Constraint | Status |
|----|------------|--------|
| C-001 | **One canonical factory, extended — not a second one invented.** `charter.resolver.DoctrineService` is the single canonical factory every access path in this mission routes through. Reconcile / extend it (governing principle: single canonical authority); do not introduce a parallel wrapper, adapter, or second "activation-aware" factory. | Active |
| C-002 | **No shrink-only allowlist; zero exceptions.** Per operator decision, every identified bypass site (FR-001-004) must be eliminated outright. A site that cannot be resolved without a proven, unavoidable behaviour change (e.g. a genuine bootstrap/circularity case per the Edge Cases section) is a blocking finding surfaced to the operator during planning or implementation — never a silently added allowlist entry, and never grounds for skipping FR-006's zero-tolerance gate. | Active |
| C-003 | **Out of scope — confirmed adjacent-but-separate, stays deferred.** #2986 (runtime→doctrine import-ratchet's own function-local-import blind spot, 61 sites/30 files, different pair), #3036 (a doctrine-content-shippability gate contradiction, different domain), #3039 (a test-file reorganisation unrelated to access-path enforcement), #3091 (relocate `src/doctrine/missions/` to `packs/built-in`, packaging track), and #3022 (extract built-in packs into `spec-kitty-packs-open`, packaging/distribution track) are untouched by this mission's diff. The #3101 kernel→doctrine→charter wheel-cutover track (and its ADR, `docs/adr/3.x/2026-08-02-1-charter-wheel-assessment.md`) is likewise untouched. | Active |
| C-004 | **PRs only; operator merges; coord topology hygiene.** Every folded issue gets an issue-matrix row + tracker comment naming the mission; reviewer ≠ implementer; no direct push to `main`. | Active |
| C-005 | **Red-main discipline.** Classify any red test against the merge-base before treating it as pre-existing; never green-wash an honest red; file per DIR-013 if a pre-existing failure is newly encountered. | Active |

### Key Entities

- **`charter.resolver.DoctrineService`** (`src/charter/resolver.py:57-139`) — the canonical, activation-aware
  factory this mission makes the *sole* access path; currently gates 3 of 10 kinds.
- **`doctrine.service.DoctrineService`** — the raw inner service; must never be constructed directly outside
  the factory and its two builder functions after this mission.
- **`ArtifactKind`** (`src/doctrine/artifact_kinds.py:128-139`) — the 10-kind (9 charter-activatable kinds +
  `mission-type` token) universe the factory must fully gate.
- **`AgentProfileRepository`** — the profile-loading repository; 7 direct construction sites eliminated.
- **`doctrine.resolver` 5-tier axis** (`_resolve_asset`, `resolve_mission`) — the template/command resolution
  tiers (OVERRIDE, LEGACY, GLOBAL_MISSION, GLOBAL, PACKAGE_DEFAULT) retargeted through the factory.
- **`doctrine.pack_paths.built_in_dir`** — the canonical path authority the two hardcoded source-tree paths
  are retargeted onto.
- **The five deferred issues** (#2986, #3036, #3039, #3091, #3022) — explicitly out of scope (C-003).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Zero unwrapped `doctrine.service.DoctrineService(...)` constructions and zero direct
  `AgentProfileRepository(...)` constructions remain anywhere in `src/` outside `charter.resolver.
  DoctrineService` and its two builder functions — gate-enforced, not a point-in-time grep.
- **SC-002**: The 5-tier template/command resolver axis and its `resolve_mission` duplicate are reachable
  only through the charter factory from outside `src/charter/**`; no other consumer imports
  `doctrine.resolver` directly.
- **SC-003**: Both previously-hardcoded source-tree paths resolve identically to `doctrine.pack_paths.
  built_in_dir`'s output, proven by an equality regression test.
- **SC-004**: `charter.resolver.DoctrineService` activation-gates all 10 doctrine-artifact kinds (up from 3);
  a bare project with no activated packs still sees its full built-in default catalog for every kind (no
  silent emptying regression).
- **SC-005**: A non-vacuous, self-mutation-proven architectural gate exists for each of the four bypass
  categories, with a frozen zero-tolerance baseline (no allowlist entries).
- **SC-006**: #2986, #3036, #3039, #3091, and #3022 remain untouched by this mission's diff and are named as
  explicit deferred follow-ons in the PR description, each confirmed still open at merge time.
