---
work_package_id: WP10
title: Asset repository + resolver + runner + provenance fix
dependencies:
- WP03
- WP09
requirement_refs:
- FR-004
- FR-005
- C-008
tracker_refs:
- '2535'
planning_base_branch: design/doctrine-controlled-gates
merge_target_branch: design/doctrine-controlled-gates
branch_strategy: Planning artifacts for this mission were generated on design/doctrine-controlled-gates. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into design/doctrine-controlled-gates unless the human explicitly redirects the landing branch.
subtasks:
- T042
- T043
- T044
- T045
- T046
phase: Lane D - Path B
history:
- at: '2026-07-11T00:00:00Z'
  actor: claude
  action: created
agent_profile: python-pedro
authoritative_surface: src/doctrine/assets/
execution_mode: code_change
owned_files:
- src/doctrine/assets/repository.py
- src/doctrine/assets/resolver.py
- src/doctrine/assets/runner.py
- src/doctrine/assets/entrypoint.py
- src/doctrine/drg/org_pack_loader.py
- tests/doctrine/assets/test_asset_resolver.py
- tests/doctrine/assets/test_asset_runner.py
- tests/doctrine/assets/test_source_kind_provenance.py
create_intent:
- src/doctrine/assets/repository.py
- src/doctrine/assets/resolver.py
- src/doctrine/assets/runner.py
- src/doctrine/assets/entrypoint.py
- tests/doctrine/assets/test_asset_resolver.py
- tests/doctrine/assets/test_asset_runner.py
- tests/doctrine/assets/test_source_kind_provenance.py
role: implementer
tags: []
task_type: implement
---

# WP10 — Asset repository + resolver + runner + provenance fix *(Lane D, Path B)*

## Objective

Build the Path-B **execution substrate** on top of WP09's validated shape: an
asset **repository** (discover gate-asset manifests), a URN→path **resolver**, a
code-asset **entrypoint** contract, and a **runner** that invokes the entrypoint
and returns a structured `GateVerdict` on a dedicated channel — implementing the
WP03 dispatch Protocol. Plus the **provenance fix** in the pack loader so a
genuine `third_party` tier is derivable (C-008), without which WP11/WP12's
trust-refusal tests are untestable.

This WP wires *execution* but **not** the trust envelope. The runner accepts an
injected `TrustEnvelope` (WP09 Protocol; WP11 supplies the concrete policy). Here
the envelope may be a permissive test double so the plumbing is provable; **all
real confinement, allowlists, and refusal are WP11**. Do not smuggle env
scrubbing / `setrlimit` / fs confinement forward into this WP — that split keeps
WP11's containment the single owner of trust.

## Context

Per research §3 the resolver, entrypoint contract, runner, and repository are the
new pieces; the schema (WP09) is an extension of the existing `AssetManifest`.
The runner reuses the **argv-vector / no-shell / timeout** shape of
`run_scoped_tests_at_head` (`pre_review_gate.py:358`) but **must NOT** copy its
`env = dict(os.environ)` full inheritance at `:374` — env handling is WP11's
allowlist. In this WP the runner's env is whatever the injected envelope hands it.

The **provenance fix** is the C-008 keystone for the whole lane. Today the pack
loader unconditionally overwrites the pack's declared `source_kind` with
`"local_path"` (`org_pack_loader.py:403`) because operator-side config is treated
as authoritative over pack-side declarations. Combined with the pack layer only
distinguishing built-in/org/project (`merge.py:20-22` provenance semantics), the
result is that **every configured pack reads as `org`** and a provenance
allowlist would admit everything — so NFR-004a/SC-012 (refuse a genuine
`third_party` asset) cannot be exercised. The fix: stop discarding the
provenance signal so a `third_party` tier is producible/refusable. This must not
break existing pack-load callers (they rely on `pack_name`/`source_ref`/
`layer_index` overrides staying authoritative — only the provenance derivation
changes).

`source_kind` (`local_path|url|package`, `org_pack_loader.py:331`) is the *transport*
kind; the trust **provenance tier** (`built_in|org_pack|third_party`,
data-model `TrustEnvelope`) is derived from preserved pack-load metadata. The
fix preserves the signal the derivation needs; the derivation *policy* itself
(what maps to `third_party`) is applied by WP11's envelope. Keep this WP's job
to "stop discarding the signal + expose it on the resolved asset's provenance
metadata", not "decide the allowlist".

## Ordered steps

### T042 — `assets/repository.py` + `assets/resolver.py`: URN→path resolution

1. New `src/doctrine/assets/repository.py`: an `AssetRepository` that, given a
   pack's resolved root, discovers `*.asset.yaml` manifests and exposes lookup by
   asset id / URN (`urn:asset:<id>`). Reuse the existing manifest-collection
   surface where the pack validator already gathers the `"assets"` plural — do
   not re-implement YAML discovery from scratch; thread the same
   `{id: (raw_data, source_file)}` slice.
2. New `src/doctrine/assets/resolver.py`: `resolve_gate_asset(urn, ...) ->
   ResolvedGateAsset` that (a) looks the manifest up via the repository, (b)
   asserts `is_executable_gate_asset` (WP09 predicate) — a plain asset URN
   resolves to a *non-runnable* result, never an executable one (C-003), (c)
   resolves `entrypoint`+`path` to a concrete on-disk target under the asset root
   (symlink-safe containment via `resolve_relative_path_within_root`), and (d)
   attaches the **derived provenance tier** (from T044's preserved metadata) so
   the runner/envelope can refuse by provenance.
3. Both modules stay pure `doctrine`-layer (no `specify_cli` import).

### T043 — `assets/runner.py` + `assets/entrypoint.py`: invoke, implement dispatch Protocol, return `GateVerdict`

1. New `src/doctrine/assets/entrypoint.py`: the code-asset **entrypoint contract**
   — how a `module:function` or script is located and how the `TransitionContext`
   (data-model: `mission_id`, `transition`, `changed_files`, `scope`) is handed in
   via a controlled channel (argv/stdin/**allowlisted env**, never
   shell-interpolated), and how the `GateVerdict` comes back on the **dedicated
   size-capped schema-validated verdict channel** (FR-019) — NOT shared stdout.
   Define the channel here (e.g. a private fd or a runner-owned temp file the
   child writes and the parent reads); the *size cap + schema validation* on read
   is enforced in the runner.
2. New `src/doctrine/assets/runner.py`: `run_gate_asset(resolved, ctx, envelope)
   -> GateVerdict` that:
   - Reuses the `run_scoped_tests_at_head` **argv/no-shell/timeout** shape
     (`pre_review_gate.py:358`) — argv vector, `shell=False`, an enforced
     `timeout`. **Do NOT** replicate its `env = dict(os.environ)` (`:374`); take
     the child env from `envelope` (in this WP, whatever the injected double
     provides — WP11 makes it an allowlist).
   - Implements the **WP03 handler/asset dispatch Protocol** so the seam's
     `run_gate` can dispatch to it identically to a Path-A handler.
   - Reads the verdict **only** from the dedicated channel; parses + schema-
     validates it into a `GateVerdict`. Absent / malformed / oversized output =
     a fault → returns an `error`-status verdict (the FR-014 reducer in WP04 folds
     it to FAULT_WARN; the runner never raises across the seam boundary).
3. Leave the timeout/process-group-kill/`setrlimit`/fs-confinement **hooks**
   present but delegated to the envelope — WP11 fills them. Mark the delegation
   points explicitly (a `TrustEnvelope` method call), do not stub silent no-ops
   that would look "contained" while running unconfined.

### T044 — Provenance fix: stop the loader overwriting `source_kind` (C-008)

1. In `src/doctrine/drg/org_pack_loader.py` around `:403`, stop unconditionally
   assigning `fragment_data["source_kind"] = "local_path"`. Preserve the
   pack-declared / derivable provenance signal so the trust tier
   (`built_in|org_pack|third_party`) is derivable from preserved pack-load
   metadata (C-008).
2. **Do not break existing callers.** The neighboring operator-authoritative
   overrides (`pack_name`, `source_ref`, `layer_index` — set for the documented
   rename/relocate reason) stay authoritative. Only the `source_kind`/provenance
   discarding changes. If a caller genuinely needs the old transport value,
   surface it distinctly (transport `source_kind` vs derived provenance tier);
   do not conflate them.
3. Expose the preserved signal on the resolved-asset provenance metadata (T042)
   so WP11's envelope can key its allowlist on a real tier. This WP does **not**
   decide the allowlist — it only makes the tier producible.

### T045 — Red-first: a resolved gate asset runs and returns a structured verdict on the dedicated channel

1. `tests/doctrine/assets/test_asset_runner.py`, red-first. Build a realistic
   gate-asset fixture whose entrypoint writes a valid `GateVerdict`
   (`status: no_new_failures`, `blocking: false`, operator message) to the
   dedicated channel. Inject a **permissive test-double envelope** (real
   confinement is WP11).
2. Assert: `run_gate_asset` returns a `GateVerdict` matching the emitted one;
   the verdict came from the dedicated channel (prove it by having the entrypoint
   *also* print a different verdict to stdout — the runner must ignore stdout;
   this pre-stages SC-011, whose full forgery test is WP12).
3. Assert the runner dispatches through the WP03 Protocol type (structural
   conformance).

### T046 — Red-first: a genuine `third_party`-provenance asset is now producible

1. `tests/doctrine/assets/test_source_kind_provenance.py`, red-first against
   pre-fix `org_pack_loader` (today it always reads back `local_path`/`org`).
2. Load a pack whose metadata yields a `third_party` tier; assert the resolved
   asset's derived provenance tier is `third_party` (not collapsed to `org_pack`).
   This is the producible tier WP12's SC-012 refusal test consumes.
3. Add a regression test proving the operator-authoritative overrides
   (`pack_name`/`source_ref`/`layer_index`) are unchanged by the fix — existing
   pack-load callers keep their behavior.
4. `ruff`/`mypy` clean across all owned source files; no new suppressions.

## Acceptance

- **SC-012 producible**: a gate asset resolved through a `third_party`-provenance
  pack is now derivable as `third_party` (T046) — the tier WP12 asserts is
  refused by default. Without T044 this criterion is untestable.
- **FR-004/FR-005 substrate**: repository + URN→path resolver + entrypoint
  contract + runner exist and a resolved executable gate asset runs and returns a
  structured `GateVerdict` on the dedicated channel (T045); the runner implements
  the WP03 dispatch Protocol.
- **C-003 held**: the resolver asserts the WP09 executable shape; a plain asset
  URN never resolves to a runnable target.
- **No trust logic here**: env is taken from the injected envelope (never
  `dict(os.environ)`); containment hooks delegate to the envelope. Real
  allowlists/confinement/refusal are WP11.
- **No caller breakage**: existing `org_pack_loader` consumers unaffected except
  the provenance derivation (T046 regression test).

## Safeguards

- **The runner reuses argv/no-shell/timeout ONLY** from `run_scoped_tests_at_head`
  — never its `env = dict(os.environ)` (`pre_review_gate.py:374`). In this WP the
  env comes from the envelope; in production (WP11) it is an allowlist.
- **Verdict from the dedicated channel only** (FR-019). stdout can never forge a
  verdict — the runner reads/validates the private channel and ignores stdout.
  Absent/malformed/oversized = fault verdict, never a crash across the seam.
- **The `source_kind` fix must not regress pack-load callers.** Keep
  `pack_name`/`source_ref`/`layer_index` operator-authoritative; only stop
  discarding the provenance signal. Transport `source_kind` and derived
  provenance tier are distinct concepts — don't conflate.
- **Fail-open at the boundary**: the runner returns an `error`-status verdict on
  any fault; it never raises through the dispatch Protocol (WP04's reducer folds
  faults to FAULT_WARN). A crashed/timed-out run is never a `regression`.
- **Containment hooks are delegated, not faked.** Leave explicit envelope calls
  where WP11 will confine; do not insert silent no-op "containment" that would
  run unconfined while looking safe.
- **Pure doctrine layer** — `src/doctrine/assets/*` must not import `specify_cli`.

## References

- `src/doctrine/assets/models.py` — WP09 `AssetManifest` extension +
  `is_executable_gate_asset` predicate + `TrustEnvelope` Protocol (consumed here).
- `src/specify_cli/review/pre_review_gate.py:358` — `run_scoped_tests_at_head`
  (reuse argv/no-shell/timeout shape); `:374` — `env = dict(os.environ)` (do NOT
  copy).
- `src/doctrine/drg/org_pack_loader.py:403` — `fragment_data["source_kind"] = "local_path"`
  (the overwrite to fix); `:331` — `source_kind: Literal["local_path","url","package"]`
  (transport kind, distinct from the provenance tier); `:395-406` — the
  operator-authoritative override block (must stay authoritative except provenance).
- `src/doctrine/drg/merge.py:20-22` — provenance semantics (`built-in`/`org:<pack>`/
  `project`) the pack layer distinguishes today; the tier derivation extends this.
- data-model.md → `TransitionContext`, `GateVerdict`, `GateAsset`, `TrustEnvelope`
  (`provenance` derived, never self-declared).
- contracts/gate-asset-entrypoint-and-trust.md → "Entrypoint contract" + trust
  clause 1 (the `source_kind`/`merge.py` provenance fix rationale) + clause 3
  (env allowlist) + FR-019 verdict channel.
- research.md §3 — EXTEND-not-greenfield; reuse argv/no-shell/timeout but NOT env.
