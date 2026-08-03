# Contract: `charter.resolver.DoctrineService` public surface (post-mission)

This is the internal contract every in-scope call site (FR-001/002/003) must construct/consume against.
Not a network API — an internal Python object contract, enforced by the FR-007 gates.

## Construction

Exactly one path constructs the activation-aware instance: the unified builder (FR-008). No call site
outside `src/charter/resolver.py` and that one builder constructs `doctrine.service.DoctrineService`
directly (NFR-001).

```
DoctrineService(inner: doctrine.service.DoctrineService, pack_context: PackContext | None)
```

- `pack_context` set (normal case) → every gated property below applies three-state filtering.
- `pack_context=None` (diagnostic case, FR-002/R4) → every gated property returns the raw inner catalog,
  unfiltered. Callers using this mode MUST carry an inline comment naming the diagnostic reason.

## Gated properties (9 of 10 kinds)

`paradigms`, `procedures`, `agent_profiles` (pre-existing) plus `directives`, `tactics`, `styleguides`,
`toolguides`, `mission_step_contracts`, `glossary_packs` (FR-005, new). Each follows the three-state
contract in `data-model.md`. None of these properties differ in filtering shape from each other — a
reviewer diffing any two of the 9 getters should see the same structure modulo the kind name.

## New resolution methods (FR-003)

Method names are an implementation choice for the tasks phase, but the contract is: every one of the 5
resolver tiers (OVERRIDE, LEGACY, GLOBAL_MISSION, GLOBAL, PACKAGE_DEFAULT) and the mission-config resolution
remains reachable ONLY via a method on this class from outside `src/charter/**`. `doctrine/resolver.py`'s
`_resolve_asset`/`resolve_mission` functions are the implementation these methods delegate to; they are not
moved, renamed, or duplicated.

## Explicitly NOT on this class

- `mission_types` — no property exists, and none is added. The `mission-type` token is gated separately by
  `MissionTypeProfileRepository` (see the sibling contract file). Do not add a `mission_types` property here
  as a shortcut; that would contradict R (D4)'s finding that the token has no matching raw-service property
  to filter.
- Lineage/mutation operations (`register_overlay`, `get_ancestors`, `resolve_profile`) on `agent_profiles` —
  these require the new lineage/mutation accessor named in R5, a second, explicitly-named accessor, not a
  widening of the `agent_profiles` property's return type.

## Non-regression obligations

- A bare project (no activated packs) must see its full built-in default catalog on every gated property —
  proven per-kind by a dedicated regression test (FR-005's bare-project pin).
- `pack_context=None` construction must return the identical catalog a raw, unwrapped
  `doctrine.service.DoctrineService` would have returned — proven by an equality regression test, since this
  mode exists specifically to preserve pre-mission diagnostic behaviour.
