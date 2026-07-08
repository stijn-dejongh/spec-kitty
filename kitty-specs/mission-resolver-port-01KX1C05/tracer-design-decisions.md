# Tracer — Design Decisions

Mission: `mission-resolver-port-01KX1C05` · #2173 Phase-2 MissionResolver port.
Seeded at planning from the 3-lens pre-spec squad (architect-alphonso, paula-patterns, researcher-robbie).
**Append a dated entry whenever a material decision is made or revised during implement; assess at close.**

## Decisions carried in from the pre-spec squad (2026-07-08)

- **D1 — Seam on the shell, never the frozen context.** The `resolver=None` default-param is injected at
  `_assemble_core_fragments` (the FS shell), **not** on `build_execution_context` (the pure projection
  door) and **never** on the frozen `MissionExecutionContext`. Rationale: a frozen value object carrying
  a mutable I/O collaborator breaks the immutability invariant — the synthesis records the "context is a
  proto-DI container" framing as a category error (ADR `2026-06-26-1`).
- **D2 — "6 walkers → 1" is overstated; honest deliverable is Protocol+Fake on the existing single walk.**
  The canonicalizer already *delegates* to `resolve_mission` (`_read_path_resolver.py:503`); it is not a
  rival walk. Phase-2 puts a port face on the one `_build_index` walk (+ adopts 2 missed identity
  consumers: `doctrine_synthesizer/apply.py:602/788`, `vcs/detection.py:169`). We do NOT oversell a
  six-way collapse.
- **D3 — #2139 is a reconcile-first SIBLING WP, not a resolver method.** `read_target_branch_from_meta`
  already exists as the authority; making `target_branch` a resolver method conflates mission-selection
  with field-extraction (widens the port past its concern). Work = route 4 stragglers + delete divergent
  `"main"`/`""`/`KeyError` defaults.
- **D4 — No cache in Phase-2.** Request-scoped resolver only; module/process-level `@lru_cache` is a
  correctness trap because `merge/ordering.py` mutates the scanned surface under the merge lock and the
  dashboard daemon is long-lived. The Phase-2 win is the seam (Fake → FS-free builder test), not perf.
- **D5 — Clock is 3 helpers, not 1.** Collapse the 12 byte-identical isoformat copies; preserve the 2
  `%Y-%m-%dT%H:%M:%SZ` stamp callers (`task_utils/support.py:101`, `mission_parsing.py:257`) and the 2
  `-> datetime` callers (`decisions/emit.py:64`, `decisions/service.py:86`) as distinct helpers. Folding
  them would change on-disk timestamp serialization (NFR-004).
- **D6 — Fail-closed-loud, no legacy branch.** Cold-miss → structured not-found → `backfill-identity`;
  ambiguity → `MissionSelectorAmbiguous`. Forbidden shape: `if <canonical> is None: <fallback>` /
  `mission_id or slug` (ADR `2026-07-01-1`; motivating incident PR #2277 — the real root was stale
  non-canonical fixtures, not a missing fallback). Fake fixtures must be canonical-shaped.
- **D7 — Scope to MissionResolver only.** The `#2173` epic title still lists 5 ports; the synthesis
  rejected 4 (GitOps=consolidation-not-absence; ProcessEnv/Clock=monkeypatch suffices; SaaSQueue=already
  seamed). Spec states this explicitly (C-008) so the title cannot pull scope back in.
- **D8 — Bind by construction.** Ship an ADR + a new AST call-site gate (`FsMissionResolver` = single
  sanctioned walker) together, copying the `test_protection_resolver_call_sites.py` precedent — otherwise
  the invariant is reviewer-vigilance, not structural, and walker #7 reappears.

## Open questions — RESOLVED at /plan (2026-07-08, by code analysis)
- **Q1 → context/mission_resolver.py::resolve_mission.** `runtime/resolver.py` has NO `resolve_mission`
  — it resolves template/config *paths* (`resolve_command_template_path`, …), a different concern; not a
  rival. The canonicalizer already delegates to the context resolver (`_read_path_resolver.py:503`),
  confirming it is the single identity walk. See research.md D-Q1.
- **Q2 → co-locate the port in `src/specify_cli/context/mission_resolver.py`** (not `mission_runtime`).
  The walk + `ResolvedMission` + errors already live there; `mission_runtime` submodules are
  external-import-forbidden (MR gate) but tests/CLI must import the Fake; and `mission_runtime → specify_cli`
  is already an established direction (`resolution.py:327/344/394…`). See research.md D-Q2.

## Decisions made during implement
_(append here)_
