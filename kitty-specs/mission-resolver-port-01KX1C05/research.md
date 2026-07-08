# Phase 0 — Research

Mission `mission-resolver-port-01KX1C05` · #2173 Phase-2 MissionResolver port.
Primary source: `docs/plans/engineering-notes/2173-infra-logic-separation/00-SYNTHESIS.md`. Grounding
established by the 3-lens pre-spec squad (architect-alphonso, paula-patterns, researcher-robbie) — full
findings in the `tracer-*.md` files. This file records the decisions the plan rests on.

## D-Q1 — Which `resolve_mission` is the canonical single walk?

- **Decision**: `src/specify_cli/context/mission_resolver.py::resolve_mission` (returns `ResolvedMission`;
  walks `kitty-specs/` via `_build_index`). This is the identity authority the port faces.
- **Rationale**: `src/specify_cli/runtime/resolver.py` has **no** `resolve_mission` — it resolves
  *template/config paths* (`resolve_command_template_path`, `resolve_content_template_path`,
  `resolve_mission_config_path`). The scout's "two `resolve_mission` functions" was imprecise; they are
  different concerns, not rivals. The `_read_path_resolver` canonicalizer already *delegates* to the
  context resolver (`_read_path_resolver.py:503`), confirming it is the single identity walk.
- **Alternatives considered**: unifying with the runtime path resolver — rejected: different return type
  and concern (path vs identity); merging would create the exact god-resolver the synthesis warns against.

## D-Q2 — Where does the port live?

- **Decision**: co-locate `MissionResolver` (Protocol), `FsMissionResolver`, and `FakeMissionResolver` in
  `src/specify_cli/context/mission_resolver.py`, alongside the existing `resolve_mission`,
  `ResolvedMission`, `_build_index`, and error taxonomy.
- **Rationale**: (1) the walk, its value object, and its errors already live there — splitting the
  Protocol into `mission_runtime` fragments the seam; (2) `mission_runtime` submodules are
  external-import-forbidden (the MR-1/2/3 surface gate), but tests and CLI code must import the Fake
  freely; (3) the `mission_runtime → specify_cli` dependency direction is already established
  (`resolution.py:327/344/394…`), so the shell importing the port from `specify_cli.context` is
  consistent, not a new coupling.
- **Alternatives considered**: define the Protocol in `mission_runtime` (strict hexagonal port ownership)
  and re-export from the package root — rejected as over-engineering here: `mission_runtime` already
  depends on `specify_cli`, so the pure-hexagon benefit is absent, and the re-export dance complicates
  the Fake's test imports for no gain.

## D-01 — Seam location (from squad, binding)

- **Decision**: inject `resolver: MissionResolver | None = None → resolver or FsMissionResolver()` at the
  imperative shell `_assemble_core_fragments` (and the `_resolve_mission_id` :913 / `_resolve_mission_slug`
  :303 reads it feeds). **Never** on `build_execution_context` (the pure, FS-free projection door) and
  **never** on the frozen `MissionExecutionContext`.
- **Rationale**: a frozen value object carrying a mutable I/O collaborator breaks its immutability
  invariant — ADR `2026-06-26-1` records the "context is a proto-DI container" framing as a category
  error. `build_execution_context` must stay FS-free (that is what the Fake exploits for NFR-001).

## D-02 — No cache in Phase-2 (from squad, binding)

- **Decision**: the resolver is request-scoped; any memoization is instance-lifetime only. Module/process
  `@lru_cache` is forbidden (C-005).
- **Rationale**: `merge/ordering.py` mutates the scanned surface under the global merge lock, and the
  dashboard daemon is long-lived — a persistent cache would serve stale indexes (a correctness bug). The
  Phase-2 value is the *seam* (Fake → FS-free builder test), not perf.

## D-03 — #2139 is a sibling reconcile, not a resolver method (from squad, binding)

- **Decision**: route the 4 stragglers onto the existing `read_target_branch_from_meta` authority
  (`core/paths.py:655`) and delete the divergent `"main"`/`""`/`KeyError` defaults; deliver as its own WP.
- **Rationale**: `target_branch` extraction is a *field read* on an already-resolved mission — a different
  granularity from handle→mission resolution. Making it a resolver method widens the port past its
  concern (violates "one adapter per port").

## D-04 — Clock is 3 helpers, not 1 (from squad, binding)

- **Decision**: collapse the 12 byte-identical isoformat copies into one `now_utc_iso() -> str`; keep a
  format-preserving stamp helper for the 2 `%Y-%m-%dT%H:%M:%SZ` callers and a `now_utc() -> datetime`
  helper for the 2 `decisions/*` callers.
- **Rationale**: the stamp callers serialize to a different, second-precision `...Z` format and the
  decisions callers return `datetime`; folding them would change on-disk timestamps (NFR-004).

## D-05 — Fail-closed, no legacy branch (from squad + ADR 2026-07-01-1, binding)

- **Decision**: cold-miss → structured not-found naming `spec-kitty migrate backfill-identity`; ambiguity
  → `MissionSelectorAmbiguous`/`AmbiguousHandleError`. No `if <canonical> is None: <fallback>` or
  `mission_id or slug` branch. Fake fixtures are canonical-shaped.
- **Rationale**: the motivating incident (PR #2277) proved the reflexive `is None` branch was wrong; the
  real root was stale non-canonical fixtures. Forbidden shape is an existing binding ADR.

## D-06 — Bind by construction (from squad)

- **Decision**: ship an ADR + a new AST call-site gate naming `FsMissionResolver` the sole sanctioned
  `kitty-specs/` walker (token-keyed allowlist), copying `test_protection_resolver_call_sites.py`.
- **Rationale**: without a structural gate the "one walk" invariant is reviewer-vigilance and walker #7
  reappears. Allowlist keyed on tokens/symbols, never line numbers (they drift on merge — F5).

## Adopt-don't-duplicate (reuse, verified)

- `PlacementSeam` (`mission_runtime/resolution.py:1266`) — yield dirs through its grammar, never compose paths.
- `_canonicalize_primary_read_handle` (`_read_path_resolver.py:1243`) — handle-form canonicalization delegates here; the port does identity→dir only, and stays OUT of the blind primitive `primary_feature_dir_for_mission` (C-007).
- `resolve_mid8` / `mission_dir_name` (`lanes/branch_naming.py`) — the mid8 SSOT.
- DI idiom: `RuntimeEventEmitter` Protocol + `NullEmitter` (`runtime/next/_internal_runtime/events.py:67/95`); wiring `emitter or NullEmitter()` (`engine.py:191`).

## Arch-gate green-list (must not regress — NFR-002)

`test_no_raw_mission_spec_paths.py`, `test_protection_resolver_call_sites.py`,
`test_single_mission_surface_resolver.py`, `test_resolution_authority_gates.py`
(`CANONICALIZER_FLOOR`/`ROUTED_CANONICALIZER_FLOOR`/`COORD_AUTHORITY_WRITE_FLOOR`),
`test_coord_read_residuals_closeout.py` (duplicate canonicalizer pins + identity/lanes floors),
`test_inline_meta_read_gate.py`, `test_write_surface_placement_guard.py`, `test_mission_runtime_surface.py`.
Floors are **shrink-only**; verify from the primary checkout (markers vacuous under `.worktrees/` — F1);
grep floor constants repo-wide before assuming one gate file owns a pin (F2/F3).
