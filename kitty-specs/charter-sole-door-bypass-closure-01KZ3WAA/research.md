# Phase 0 Research: Charter as Sole Door: Close Bypass Access Paths

Three parallel research agents were dispatched against the spec's four bypass categories, reading full call
sites (not just the file:line anchors) and, where relevant, git history. Their findings produced four
planning-time corrections to the spec (each confirmed with the operator via `AskUserQuestion` before this
plan was written) plus a set of implementation-level design decisions that did not require operator input.

## Corrections requiring operator decision (resolved)

### D1 — FR-004's original acceptance criterion is unsatisfiable

- **Decision**: Promote `MissionTemplateRepository.default_missions_root()` (`src/doctrine/missions/
  repository.py:98`) as the single missions-root authority; retarget the other two hardcodes onto it. Defer
  the `doctrine.pack_paths.built_in_dir` convergence to `#3091`.
- **Rationale**: `doctrine.pack_paths.built_in_dir` resolves under `packs/built-in/<kind.plural>/`, which has
  no `missions/` subdirectory today — confirmed on disk (`packs/built-in/` contains `directives/ tactics/
  styleguides/ procedures/ paradigms/ agent_profiles/ glossary_packs/ toolguides/ assets/`, no `missions/`).
  `pack_paths.py`'s own docstring names `TEMPLATE`/`MISSION_STEP_CONTRACT`/`ANTI_PATTERN` as kinds with no
  built-in content dir, citing `#3091` (the missions→packs relocation, itself deferred by this mission's
  C-003) as the future work that adds one. `default_missions_root()` was found already correctly
  implemented — `importlib.resources`-based (wheel-safe), with a documented fallback — making it the better
  promotion target than inventing a new shared constant.
- **Alternatives considered**: Drop FR-004 entirely (rejected — operator wanted the duplication closed now,
  not deferred wholesale); retarget onto `pack_paths.built_in_dir` as originally specced (rejected — would
  require the deferred `#3091` relocation to exist first, making the acceptance criterion unsatisfiable).

### D2 — Two `AgentProfileRepository` sites are not doctrine-asset bypasses

- **Decision**: `src/specify_cli/invocation/registry.py:48` and `src/specify_cli/cli/commands/
  profiles_cmd.py:83` are excluded from FR-001's scope (C-006). Both construct `AgentProfileRepository`
  against `.kittify/profiles`, and both already separately call the canonical factory correctly for their
  doctrine-layer data.
- **Rationale (operator)**: "`.kittify` contains local overrides, this slice is to be reworked, do not route
  it." `.kittify/profiles` is a legitimate local-override mechanism outside the doctrine activation model by
  design, not a bug; it is scoped for its own future rework, separate from this mission.
- **Alternatives considered**: Widen the factory's conceptual scope to also cover `.kittify/profiles`
  (rejected by operator — risks conflating two deliberately-separate concerns, and the research found no
  existing factory affordance for that directory to extend from).

### D3 — A real C-001 violation surfaced as a byproduct: two divergent builders

- **Decision**: Fold in unifying `specify_cli.doctrine_service_factory.build_activation_aware_doctrine_
  service` and `charter.doctrine_service_builder._build_activation_aware_doctrine_service` as new scope
  (FR-008), rather than deferring it as a separate issue.
- **Rationale**: The two functions are NOT behaviourally identical. The `charter` builder passes
  `active_languages=infer_repo_languages(repo_root)` into the inner `DoctrineService` construction; the
  `specify_cli` builder omits `active_languages` entirely. `active_languages` flows into every per-kind
  repository (`src/doctrine/service.py:72,82,92,111,148`) for language-scoped filtering, so the two builders
  can return **different catalogs for the same `repo_root`**. Separately, the `charter` builder requires an
  explicit `org_roots` argument (defaulting to `None` → no org layer) while the `specify_cli` builder always
  self-resolves org roots via `resolve_org_roots` — a caller of the `charter` variant who forgets `org_roots`
  silently loses the org layer. This directly undercuts the very "single canonical authority" claim this
  mission's C-001 makes, discovered while doing this mission's own work — domain-matched, unlike the five
  issues confirmed adjacent-but-separate pre-spec.
- **Alternatives considered**: File as a separate GitHub issue and leave the mission's original FR list
  unchanged (rejected by operator — the divergence is inside the exact factory this mission is making the
  sole door, so leaving it standing would ship a mission that claims C-001 while visibly violating it).

### D4 — `mission-type` does not fit the mechanical 9-kind pattern

- **Decision**: Gate the `mission-type` token via `charter.mission_type_profile_repository.
  MissionTypeProfileRepository` / `charter.mission_type_profiles.resolve_mission_type_context()` (FR-006),
  not via a new property on `charter.resolver.DoctrineService`. Per operator decision, do the real work
  rather than narrowing the "all 10 kinds" claim to 9.
- **Rationale**: `PackContext.activated_mission_types` (`src/charter/pack_context.py:120`) is a plain
  `frozenset[str]`, never `None` — `_read_activated_mission_types` (`pack_context.py:601-619`) already
  collapses "key absent" to `builtin_mission_type_id_set()` at construction time, so the three-state
  semantics (`None`/`frozenset()`/`{ids}`) the other 6 kinds use don't apply here; the default is baked in
  before any resolver sees it. Separately, `src/doctrine/service.py` has no `mission_types` property at all
  (confirmed by grepping every `@property` on the raw service: directives, tactics, styleguides, toolguides,
  paradigms, procedures, mission_step_contracts, glossary_packs, assets, agent_profiles — no mission-type
  entry) — mission-type resolution has always lived entirely outside `DoctrineService`, in a separate
  repository. There is nothing for `charter.resolver.DoctrineService.__getattr__` to even unfilteredly
  forward for this token the way it does for the other 7 — the "ungated passthrough" framing doesn't fit.
- **Alternatives considered**: Narrow to 9/10 real `ArtifactKind` gating, name `mission-type` as an explicit
  carve-out matching how `TEMPLATE`/`ASSET`/`ANTI_PATTERN` are already carved out via
  `_NON_AUGMENTATION_ELIGIBLE_KINDS` (rejected by operator — "extend to `MissionTypeProfileRepository` too,
  your original intent").

## Design decisions resolved without operator input

### R1 — `_resolve_directives_selection` clarifies, does not contradict, the "3 of 10 gated" premise

`charter/resolver.py::_resolve_directives_selection` (lines 233-298) already implements the exact
three-state semantics for `directive` and reads `PackContext.activated_directives` directly — but it is
private, used only inside the separate `resolve_project_governance()` function, and is **not** wired to
`charter.resolver.DoctrineService`'s properties (which are exactly `paradigms`, `procedures`,
`agent_profiles` — confirmed by grepping `@property` in the file). It is the fallback-source *exemplar* to
copy the three-state logic from for FR-005's 6 mechanical kinds, not evidence that `directive` gating
already exists on the factory. The spec's "3 of 10 gated" premise stands correctly.

### R2 — FR-005's 6 mechanical kinds require zero `PackContext` schema changes

`PackContext` (`src/charter/pack_context.py:100-259`) already carries a three-state `activated_<kind>` field
for every one of `directive` (144), `tactic` (152), `styleguide` (155), `toolguide` (158),
`mission_step_contract` (170), `glossary_pack` (173) — each populated via a dedicated `_read_activated_*`
reader (lines 622-676), structurally identical to the readers already wired for `paradigms`/`procedures`/
`agent_profiles`. `src/doctrine/service.py` confirms matching raw properties for all 6: `directives` (57),
`tactics` (66), `styleguides` (76), `toolguides` (86), `mission_step_contracts` (115), `glossary_packs`
(124). Extending `resolver.py` for these 6 is copy-paste of the existing property pattern — no new
`PackContext` field, no new raw-service property, no activation-engine change.

### R3 — The "boundary ratchet" comment is a red herring for this migration

`git log -p -S 'boundary ratchet'` traces the `tasks_status_cmd.py:712,823` comments to commit `873832aa1`.
The stated fear — a direct doctrine import tripping the boundary ratchet — is checked by
`tests/architectural/test_runtime_charter_doctrine_boundary.py`, which only scans **module-level**
`from doctrine.*` imports (lines 98-102 of that test explicitly exclude lazy/function-local imports). Both
the existing `AgentProfileRepository` import and the factory's internal `DoctrineService` import are
function-local at these sites, so routing through the factory does **not** trip this gate — the comment's
named concern does not reappear. The real, previously-unmeasured risk is construction cost (the factory adds
`PackContext.from_config` + `resolve_org_roots` + a wrapper vs. today's bare `AgentProfileRepository()`),
covered by NFR-005's latency measurement, not an architectural blocker.

### R4 — `_doctrine_collect.py`'s 4 diagnostic sites need the factory's *unfiltered* mode, not the filtered path

`_collect_profile_health`, `_collect_glossary_pack_health`, `_collect_doctrine_collisions`, and
`_build_selection_block` all deliberately need the unfiltered, all-layer view — activation-aware filtering
would silently narrow doctor/health output for deactivated packs, which is exactly the anti-pattern the
spec's Acceptance Scenario 2 (User Story 1) warns against. Fix: wrap with
`charter.resolver.DoctrineService(inner, pack_context=None)` — same class, explicit unfiltered construction,
satisfying C-001 (one factory) without regressing diagnostic completeness.

### R5 — `projection.py:84` and `runtime_bridge_io.py:576` need capabilities the filtered wrapper doesn't expose

`projection.py:84` (`default_profile_repository`) needs `register_overlay()` (mutation) and `get_ancestors()`
(lineage) — neither exists on the filtered dict `charter.resolver.DoctrineService.agent_profiles` returns.
`runtime_bridge_io.py:576` needs `repo.resolve_profile(profile_id)` (lineage composition), also absent from
the filtered dict. Both currently reach around the gate via `svc._inner.agent_profiles` (already used at
`registry.py:64`) — a private-attribute reach-around that works but isn't a real public contract. **Design
decision**: add one new public accessor to `charter.resolver.DoctrineService` for "the mutable/lineage-
capable repository, still activation-aware for read paths" before migrating these two call sites, so the
mission doesn't trade one reach-around for a proliferation of `_inner` accesses at every migrated site.

### R6 — FR-003's tier functions stay in `doctrine/resolver.py`; only the entry point moves

`doctrine/resolver.py::_resolve_asset`/`resolve_mission` are pure filesystem-tier functions, unrelated to the
`DoctrineService` object the factory wraps. An existing correct precedent already solves this exact shape:
`src/specify_cli/runtime/resolver.py` reimplements tiers 1-4 itself (pure `.kittify`/`~/.kittify` filesystem
checks) and routes only tier 5 (package-default) through `charter.template_resolver.CharterTemplateResolver`
— its own comment states the intent: *"Keep this call routed through charter so runtime never binds directly
to doctrine's repository shape."* (Landed under `charter-mediated-doctrine-selection-01KRTZCA`, WP07.)
**Design decision**: add resolution methods to `charter.resolver.DoctrineService` that internally call
`doctrine.resolver.resolve_command`/`resolve_template`/`resolve_mission` (legal — `charter → doctrine` is the
sanctioned direction); `CharterTemplateResolver` becomes a thin delegating shim or is retired in favour of
direct factory use by its one real caller. Two additional in-scope importers were found during this research
and folded into FR-003: `src/charter/resolution.py` (facade re-export) and `src/charter/context_renderers/
template_include.py` (lazy `ResolutionTier` import) — both already inside `src/charter/**` but still
bypassing the new factory methods.

**Explicitly out of scope, noted as debt**: `specify_cli/runtime/resolver.py`'s own tier-1-4
reimplementation is a second, parallel filesystem-tier implementation (not a `doctrine.resolver` import, so
not a literal bypass) with already-observed semantic drift from `doctrine/resolver.py` (different exception
handling: catches only `FileNotFoundError` vs. `doctrine.resolver`'s `(FileNotFoundError, ImportError)`).
Flagged for a future mission; not folded in here (would expand IC-02's blast radius well beyond the named
FR-003 anchor).

### R7 — `profile_resolution.py:81`'s `repo_root is None` branch is a genuine bootstrap case

The module's `repo_root is None` branch is the process-wide cached built-in-only fast path used when there is
no repo context to build a factory instance from — the bootstrap/circularity case the spec's Edge Cases
section already anticipated. It is not a site this mission routes through the factory; it is the legitimate
absence-of-context case C-002 already carves out by design (surfaced, not silently allowlisted).
