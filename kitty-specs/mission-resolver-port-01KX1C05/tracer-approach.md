# Tracer — Approach

Mission: `mission-resolver-port-01KX1C05` · #2173 Phase-2 MissionResolver port.
Seeded at planning. **Append as the approach is refined/validated during implement; assess at close.**

## Intended WP shape (pre-plan sketch — /plan and /tasks own the final slicing)

- **WP-A — Resolver seam + builder unblock (core).** Define `MissionResolver` Protocol +
  `FsMissionResolver` (real, owns the `_build_index` walk) + `FakeMissionResolver` (in-memory). Thread
  `resolver=None` into `_assemble_core_fragments`. Adopt `doctrine_synthesizer/apply.py:602/788` and
  `vcs/detection.py:169`. Deliver NFR-001: an FS-free builder unit test via the Fake. Fail-closed-loud
  cold-miss/ambiguity (FR-005/NFR-005).
- **WP-B — ADR + AST call-site gate (bind-by-construction).** Write the ADR (D1/D4/D6/D7). Add the new
  gate naming `FsMissionResolver` as sole sanctioned walker (token-keyed allowlist), copying
  `test_protection_resolver_call_sites.py`.
- **WP-C — #2139 target_branch reconcile (sibling).** Route the 4 stragglers onto
  `read_target_branch_from_meta`; delete `"main"`/`""`/`KeyError` defaults; characterization test on the
  unified missing-value behavior.
- **WP-D — Clock consolidation.** 12 isoformat copies → one; preserve the 2 stamp + 2 datetime helpers
  (NFR-004 byte-identical test). Inject Clock port only at determinism-tested sites.
- **WP-E — InstalledVersion routing + #2447 doc tail.** Route the migration reader through
  `_CliStatusLike`; repoint/remove the phantom doctrine row + add the path-resolution guard.

Dependency hint: WP-A precedes WP-B (gate needs the blessed owner to exist). WP-C/D/E are independent
sibling slices and can parallelize. Final ordering/lanes are decided at finalize-tasks.

## Adopt-don't-duplicate SSOTs (must reuse, verified in scout)
- `PlacementSeam` (`mission_runtime/resolution.py:1266`) — the resolver yields dirs *through* this seam's grammar; do not compose paths (the `test_no_raw_mission_spec_paths.py` gate bites otherwise).
- `_canonicalize_primary_read_handle` (`_read_path_resolver.py:1243`) — handle-form canonicalization delegates here; the port does identity→dir only.
- `resolve_mid8` / `mission_dir_name` (`lanes/branch_naming.py`) — the mid8 SSOT.

## Existing DI precedent to copy (not reinvent)
- `RuntimeEventEmitter` Protocol + `NullEmitter` (`runtime/next/_internal_runtime/events.py:67/95`); wiring `emitter or NullEmitter()` (`engine.py:191`). This is the exact `x or Default()` idiom.

## Verification approach
- Per drained site: full `tests/architectural/` run + repo-wide floor-constant grep, from the **primary checkout** (marker gates are vacuous under `.worktrees/` — NFR-002).
- Floors are shrink-only; a genuine drain lowers a floor, never raises it.

## Refinements during implement
_(append here)_
