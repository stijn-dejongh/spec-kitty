# Implementation Plan: Doctrine-Controlled Transition Gates

**Branch**: `design/doctrine-controlled-gates` | **Date**: 2026-07-11 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `kitty-specs/doctrine-controlled-gates-01KX81KR/spec.md`
**Research**: [research.md](./research.md) · **ADR**: [docs/adr/3.x/2026-07-11-1-doctrine-controlled-transition-gates.md](../../docs/adr/3.x/2026-07-11-1-doctrine-controlled-transition-gates.md)

## Summary

Move the *selection and supply* of task-transition gates out of hardcoded
`specify_cli` logic into the doctrine/charter layer. Two coexisting mechanisms
(RD-005): **Path-A handlers** (spec-kitty-shipped, no opt-in) and **Path-B
executable gate assets** (doctrine-supplied, opt-in + real containment). A
mission **step contract** declares `transition → gate` bindings; the **charter**
subsystem's activation selects which are active. Both runtime consumers obtain
their gate set through **one SSOT *selection* seam** (`resolve_gates` + a
lane↔action adapter; research §0) — **reduction stays per gate-class**:
test/verdict gates use the FR-014 fail-open reducer (folded into the seam, IC-02);
the artifact-presence composed-action guard keeps its existing **fail-closed**
reduction and shares *selection* only. The pre-review regression **test-gate** is
migrated as the Path-A exemplar, closing #2534 fully and #2330 for the selection path.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: pydantic (frozen models, `extra="forbid"`), ruamel.yaml (doctrine YAML), the existing charter/DRG subsystem (`src/charter/`, `filter_graph_by_activation`), `review/baseline.py` + `review/pre_review_gate.evaluate_with_scope` (reused verdict tail), `subprocess` + stdlib primitives only for the Path-B runner (`os.setsid`/process-group kill, `resource.setrlimit`, path-resolved fs confinement, env allowlist) — **no new sandbox dependency** (RD-006)
**Storage**: doctrine YAML (`*.step-contract.yaml`, `*.asset.yaml`), generated DRG (`graph.yaml`/`references.yaml`), `.kittify/config.yaml` (opt-in flag), gate assets on disk (resolved via URN→path)
**Testing**: pytest — characterization/golden tests (behavior-preserving extractions), contract tests (the SSOT seam), fault-injection tests (fail-open), trust/containment tests, and an extension of `tests/architectural/untrusted_path_audit/`
**Target Platform**: Linux/macOS CLI (cross-platform; refuse-unconfinable v1 — a capability probe refuses where fs/network can't be confined, never run unconfined)
**Project Type**: single (CLI + library)
**Performance Goals**: gate execution bounded by an enforced timeout (default mirrors the baseline ~300 s); resolution seam is O(active bindings) — negligible
**Constraints**: fail-open invariant (only a valid emitted `regression(blocking)` may block); cognitive-complexity ceiling 15 (S3776/C901); no new public CLI surface beyond the observability query + the opt-in flag; `extra="forbid"` models → versioned schema evolution + migration; no doctrine code executes on Path A
**Scale/Scope**: ~12–14 WPs (see the lane sketch under the IC map); surfaces: `src/specify_cli/review/`, `src/specify_cli/cli/commands/agent/tasks_move_task.py`, `src/runtime/next/runtime_bridge.py`, `src/charter/` (`drg.py` kind-map), `src/doctrine/missions/step_contracts.py`, `src/doctrine/assets/models.py`, `src/specify_cli/doctrine/pack_validator.py`, DRG `graph.yaml`/`references.yaml` regeneration

## Charter Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Single canonical authority** ✅ — charter activation is the sole gate-selection authority (C-001); exactly **one** SSOT resolution seam both consumers depend on (research §0). No parallel registry/resolver.
- **Architectural alignment** ✅ — reuse `filter_graph_by_activation` + `evaluate_with_scope`; the binding + seam is the only new decision surface (C-005). No legacy fallback (C-004, unification-not-parity).
- **DDD + tiered rigour** ✅ — core (resolution seam, runner, trust envelope, fault reducer) = high rigour + contract tests; glue (observability query, doc/yaml wiring) = standard rigour.
- **ATDD-first** ✅ — contract tests for the seam + fault-injection acceptance tests precede implementation; characterization tests precede every extraction.
- **Campsite-first** ✅ — IC-01 tidy-first hook extraction opens the surface before the functional change; broader `runtime_bridge` degod stays tracked at **#2531** (#2116 is closed) — **coordinate** the F(48) inversion with it.
- **Trust/safety** ✅ — executing doctrine code (Path B) is gated by the refuse-unconfinable v1 containment envelope + default-off opt-in + derived provenance; the untrusted-input audit harness is extended (C-007).
- **Anti-fallback (C-004)** ✅ — the strangler **removes** the hardcoded spec-kitty-shaped `pre_review_gate` decision path; there is **no** "doctrine-inactive → run the old gate" compatibility tail. Inactive/undeclared → CALM-NOTICE, not a legacy fallback.

No violations → Complexity Tracking empty.

## Project Structure

### Documentation (this mission)

```
kitty-specs/doctrine-controlled-gates-01KX81KR/
├── plan.md              # This file
├── research.md          # Grounding + post-spec squad (SSOT seam = §0)
├── data-model.md        # Entities: binding, resolved-gate, verdict, handler/asset, scope-source, trust-envelope
├── quickstart.md        # How a doctrine author declares a gate; how a consumer ships one
├── contracts/
│   ├── gate-resolution-seam.md      # THE keystone: the single entry point
│   ├── gate-verdict-and-outcomes.md # FR-014 verdict→operator-outcome mapping
│   └── gate-asset-entrypoint-and-trust.md  # Path-B entrypoint + containment contract
└── tasks.md             # /spec-kitty.tasks output (NOT created here)
```

### Source Code (repository root)

```
src/
├── specify_cli/
│   ├── review/
│   │   ├── pre_review_gate.py          # split: verdict tail (reuse) vs spec-kitty ScopeSource (move) vs decision path (remove)
│   │   └── gates/                       # NEW: SSOT *selection* seam + per-class reduction, handler registry
│   │       ├── resolver.py              # resolve_gates (selection) + lane↔action adapter; run_gate (test-gate reduction) folds outcomes
│   │       ├── outcomes.py              # FR-014 reducer (test-gate fail-open boundary; owned by resolver — IC-08 folded into IC-02)
│   │       ├── handlers/                # Path-A handlers (pre-review exemplar)
│   │       └── scope_source.py          # ScopeSource protocol + built-in spec-kitty impl
│   ├── doctrine/pack_validator.py       # EXTEND _validate_asset_manifests: gate-asset-shape detection (keys code-exec)
│   └── cli/commands/agent/
│       ├── tasks_move_task.py           # invert the pre-review hook onto the seam
│       └── pre_review_hook.py           # NEW (IC-01): extracted hook block, behavior-preserving
├── runtime/next/runtime_bridge.py       # share SELECTION only for _check_composed_action_guard; keep its fail-closed reduction (coord #2531)
├── charter/drg.py                       # EXTEND _SINGULAR_TO_PLURAL so step-contract-based gate activation isn't a no-op
└── doctrine/
    ├── missions/step_contracts.py       # + versioned gate-binding field on MissionStepContractStep:65 (migration)
    ├── assets/models.py                 # EXTEND AssetManifest (extra="forbid") with executable gate-asset shape (Path-B substrate: repository/resolver/runner/entrypoint alongside)
    ├── missions/models.py               # + gate-binding on unified MissionStep (migration)
    └── graph.yaml / references.yaml     # REGENERATE (generated + freshness/parity-gated) after the schema/kind-map change

tests/
├── contract/            # seam I/O + verdict→outcome contract tests
├── integration/         # consumer-repo fixture, non-pytest gate, migration round-trip
├── unit/                # reducer, scope-source, trust-envelope, runner
└── architectural/untrusted_path_audit/  # EXTENDED to cover the code-exec sink
```

**Structure Decision**: Single project. The functional core lands in a new
`src/specify_cli/review/gates/` package (the seam, reducer, handler registry,
scope-source) plus a new Path-B substrate under `src/doctrine/assets/`. The two
runtime consumers (`tasks_move_task.py`, `runtime_bridge.py`) are *inverted* onto
the seam, never re-implementing selection.

## Complexity Tracking

*No Charter Check violations — section intentionally empty.*

## Implementation Concern Map

> Concerns are NOT work packages. `/spec-kitty.tasks` translates these into WPs.
> Ordering below reflects dependency + the CaaCS forensic risk sequencing from research §5.

### IC-01 — Tidy-first: extract the pre-review hook (enabler)
- **Purpose**: Relocate the pre-review hook block out of the 1817-LOC `tasks_move_task.py` god-module into a dedicated sibling, behavior-preserving, so the seam + handler dispatch land on a clean surface.
- **Relevant requirements**: enables FR-002/FR-011; preserves FR-010.
- **Affected surfaces**: `tasks_move_task.py:690-1051` (`_PRE_REVIEW_*` consts + `_mt_pre_review_*` helpers + `_pre_review_gate_*` seams), `tasks.py:427-448` re-export shim.
- **Sequencing/depends-on**: none (first).
- **Risks**: must preserve fail-open scaffolding (`_mt_empty_scope_verdict:859`, broad `except:1035`) **verbatim** — it IS the FR-010 contract. Golden-guard with existing move-task characterization tests before moving.

### IC-02 — SSOT gate-*selection* seam + test-gate reducer (the keystone; IC-08 folded in)
- **Purpose**: One injected `resolve_gates(mission, transition, activation)` → ordered `ResolvedGate` list (with a **lane↔action adapter**: `resolve_gates` selects bindings whose declared `binding.transition` equals the requested key — it does NOT call `get_by_action("for_review")` (a lane is not an action → None). Lane keys (`for_review`) and action keys (`implement`…) share one `transition` namespace on the binding; the pre-review exemplar's built-in binding declares `transition: for_review`. Adapter table in `contracts/gate-resolution-seam.md`); the ONLY place that reads bindings + applies charter activation. **Selection only** — both consumers share it. **Reduction is per gate-class**: the seam's `run_gate` folds test/verdict-gate faults via the FR-014 reducer (the former IC-08 — folded in here because `run_gate` cannot meet its fault-containment/only-regression invariants without it); the artifact-presence guard keeps its own **fail-closed** reduction (shares selection only, NOT routed through `run_gate` — else SC-010 hard-blocks downgrade to warns).
- **Relevant requirements**: FR-002, FR-003, FR-006, FR-010, FR-014; C-001, C-002, C-005; SC-010.
- **Affected surfaces**: new `review/gates/resolver.py` + `review/gates/outcomes.py`; `runtime_bridge._check_composed_action_guard` (F48, selection only) and the extracted pre-review hook both inverted onto it.
- **Sequencing/depends-on**: IC-01 **and IC-03's `GateBinding` model** — the resolver imports `GateBinding` from `src/doctrine` (arch-gated: `src/doctrine` must not import `specify_cli`), so lanes A/B are **not** independent. Carve `GateBinding` as a foundational sub-WP that charter-spine lane A ships first; IC-02 depends on it. (IC-08 no longer standalone — folded here.)
- **Risks**: highest-regression edit (F48 god-module). **Extract-then-inject**: characterization tests on the current `(mission, action)` matrix FIRST; never edit-in-place. Isolate the F(48) inversion in its **own** WP and **coordinate with #2531** (concurrent decomposition of the same file). If both consumers don't route selection through it, NFR-005 is unprovable.

### IC-03 — Gate-binding schema + kind-map + DRG regen + migration (charter spine)
- **Purpose**: Add the declarative `transition → gate` binding to `MissionStepContractStep` and unified `MissionStep`; **extend `_SINGULAR_TO_PLURAL`** (`src/charter/drg.py:187`) so step-contract-based gate activation is not a silent no-op (the owning step-contract node is the activatable unit); **regenerate the DRG** (`graph.yaml`/`references.yaml` are generated + freshness/parity-gated); migrate the gate-declaring built-in step contracts.
- **Relevant requirements**: FR-001, FR-006, FR-016; C-006.
- **Affected surfaces**: `src/doctrine/missions/step_contracts.py:65` (NOT `src/charter/step_contracts.py` — corrected), `src/doctrine/missions/models.py:87`, `src/charter/drg.py:187` (kind-map), the DRG regeneration (`graph.yaml`/`references.yaml`; freshness gate `consistency_check.py`, `test_activation_parity_guard`), and **only the gate-declaring built-in `*.step-contract.yaml`** (not all 17), a migration.
- **Sequencing/depends-on**: none for schema; **migration-first within the charter-spine lane** (step_contracts→executor→drg→pack_validator→merge co-change tightly — one lane, no parallel). DRG regen runs after the schema + kind-map change lands, before the freshness gate.
- **Risks**: `extra="forbid"` → old contracts must still load (FR-016/SC-009). Coupled spine ripple. A skipped DRG regen fails the freshness/parity gate.

### IC-04 — ScopeSource abstraction + built-in spec-kitty ScopeSource
- **Purpose**: Make scope derivation a doctrine-declared strategy; move `_SRC_PACKAGE_PREFIX` / `_gate_coverage` census into a built-in ScopeSource used only when spec-kitty's own doctrine is active.
- **Relevant requirements**: FR-009, FR-012; NFR-002.
- **Affected surfaces**: `pre_review_gate.py` (`derive_test_scope`, `_load_gate_coverage_module`, `_default_filter_groups/_default_composite_routing`).
- **Sequencing/depends-on**: IC-02 (verdict interface).
- **Risks**: `derive_test_scope` at the C(15) ceiling — extraction must not exceed it.

### IC-05 — Pre-review handler (Path-A exemplar migration)
- **Purpose**: Re-express the pre-review **test-gate** as a built-in **handler** bound via a built-in step contract; invert the hardcoded invocation through the IC-02 seam; reuse `evaluate_with_scope`; preserve existing config semantics. This is the **only** gate migrated (FR-013); the composed-action artifact guard shares *selection* only and keeps its fail-closed reduction (not migrated here).
- **Relevant requirements**: FR-011, FR-013, FR-017; NFR-001; SC-003.
- **Affected surfaces**: `review/gates/handlers/`, a built-in step contract, `pre_review_gate.py` (decision path **removed** — no compat fallback, C-004).
- **Sequencing/depends-on**: IC-02, IC-03, IC-04.
- **Risks**: verdict parity on spec-kitty's own repo (no opt-in). C-004: remove the hardcoded decision path, do not grow a "doctrine-inactive → old gate" tail.

### IC-06 — Executable ASSET substrate (Path-B) — EXTEND existing, not greenfield
- **Purpose**: **Extend** the existing `AssetManifest` (`src/doctrine/assets/models.py`, `extra="forbid"`) with the executable gate-asset shape and **extend** `pack_validator._validate_asset_manifests` (`:604`) with **gate-asset-shape detection that keys code-exec** (non-gate assets stay inert — C-003); add the URN→path resolver + code-asset entrypoint contract + runner returning a structured verdict on a dedicated capped channel (FR-019). Fix the **`source_kind` provenance derivation** (loader stops overwriting it, `org_pack_loader.py:403`) so a `third_party` tier is producible/refusable (C-008) — else NFR-004a/SC-012 are untestable.
- **Relevant requirements**: FR-004, FR-005, FR-019; C-003, C-008.
- **Affected surfaces**: EXTEND `src/doctrine/assets/models.py` + `src/specify_cli/doctrine/pack_validator.py:604`; new `doctrine/assets/{repository,resolver,runner,entrypoint}.py`; loader `source_kind` fix.
- **Sequencing/depends-on**: IC-02 (verdict interface), IC-03 (binding names asset).
- **Risks**: schema evolution on an `extra="forbid"` model (old assets must still load, mirror FR-016/SC-009 for assets); must not generalize asset loading into code-exec.

### IC-07 — Trust envelope + containment (refuse-unconfinable v1, RD-006)
- **Purpose**: Confine Path-B execution with **stdlib-only, cheap-real** primitives and **refuse where it cannot confine** — **no new sandbox dependency**: derived provenance allowlist (needs the IC-06 `source_kind` fix), `review.allow_executable_gate_assets` opt-in (default off), interpreter allowlist/no-shell/argv, **environment allowlist (never `dict(os.environ)`)**, **process-group kill on timeout** (grandchildren), **`setrlimit` CPU/mem/output caps**, **path-resolved (symlink-safe) fs write confinement**, a **capability probe → refuse (TRUST_REFUSAL)** where fs/network can't be confined, and a **dedicated size-capped schema-validated verdict channel** (FR-019, not stdout). Deeper OS sandbox (namespaces/landlock/seccomp) explicitly **deferred**.
- **Relevant requirements**: FR-007, FR-015, FR-019; NFR-004a/b, NFR-006; C-007, C-008; RD-006; SC-007/011/012.
- **Affected surfaces**: the IC-06 runner, config (`review.allow_executable_gate_assets`), `tests/architectural/untrusted_path_audit/` (extended).
- **Sequencing/depends-on**: IC-06.
- **Risks**: RCE-adjacent — extend the audit harness (static) or it goes stale-green. **Do NOT reuse the `run_scoped_tests_at_head` env behavior** — it does `env = dict(os.environ)` (`pre_review_gate.py:374`, full inheritance); reuse only its argv/no-shell/timeout shape and construct an env allowlist instead.

### IC-08 — Fault→outcome reducer + fail-open enforcement (FOLDED INTO IC-02)
- **Folded into IC-02.** The FR-014 test-gate reducer (`review/gates/outcomes.py`) is the reduction boundary the seam's `run_gate` owns and cannot satisfy its fault-containment / only-regression invariants without — so it is delivered *with* IC-02, not as a separable downstream concern. Kept as a numbered concern for FR traceability (FR-010, FR-014; NFR-003; C-002; SC-005) only.
- **Scope reminder**: this reducer governs **test/verdict gates only**; the artifact-presence composed-action guard keeps its own fail-closed reduction (SC-010).

### IC-09 — Observability + operator surface
- **Purpose**: Answer "which gates are active for this transition, from which doctrine, and why did/didn't each run".
- **Relevant requirements**: FR-018; SC-008.
- **Affected surfaces**: a read-only query over the IC-02 selection seam (CLI subcommand or `agent tasks status` extension).
- **Sequencing/depends-on**: IC-02.
- **Risks**: keep loopback/read-only; no new heavy CLI surface.

## WP sizing + lane sketch (~12–14 WPs)

Undersized ~8–10 → **~12–14 WPs**. IC-07≈2–3 (env-allowlist+process-group/rlimit; path-resolved fs + capability-probe/refuse; verdict channel), IC-06≈2 (schema+validator+shape-detection; resolver+runner+`source_kind` fix), IC-03≈2 (schema+kind-map; DRG regen+migration), consumer-inversions≈2 (move-task hook; **F(48) guard alone, coord #2531**).

Lanes (dependency-ordered):
- **A — charter spine** (IC-03, serial, **migration-first**, single lane: step_contracts→models→drg kind-map→DRG regen→pack_validator→merge).
- **B — selection seam + test-gate reducer** (IC-02 with folded IC-08; + IC-09 read-only tail).
- **C — Path-A** (serial IC-01 → IC-04 → IC-05), depends B (+A for the binding).
- **D — Path-B** (IC-06 → IC-07), depends B (+A for the binding).
- **E — consumer inversions**: move-task pre-review hook onto the seam; the **F(48) `_check_composed_action_guard` selection inversion in its OWN WP, coordinated with #2531** (owned-file collision).

## Notes for /tasks (pre-tasks squad, Op 01KX8DTJ)

The WP graph must encode these (not plan defects — decomposition constraints):

1. **Foundational `GateBinding` sub-WP first.** `GateBinding` lives in `src/doctrine` (IC-03) and IC-02's resolver imports it → lanes A and B are NOT independent; ship the binding model as the first sub-WP of lane A, and make IC-02 depend on it.
2. **IC-02 ships a dispatch `Protocol` only; IC-07 implements the Path-B arm (forward-only).** `run_gate`'s Path-B branch back-depends on the IC-06/IC-07 runner+envelope, which don't exist at IC-02 time — else `run_gate`'s DoD is circular. IC-02 defines the handler/asset dispatch Protocol; Path-A handler (IC-05) and Path-B runner (IC-07) implement it.
3. **NFR-005 / SC-004 proof lives in the FINAL consumer-inversion WP**, not IC-02 — it is provable only after BOTH consumers (move-task hook AND the F(48) guard) route selection through the seam.
4. **Own the consumer-shaped fixture.** SC-001/SC-002/NFR-002 need a non-pytest, no-`_gate_coverage.py` fixture repo — assign it to exactly one WP (it is currently unowned).
5. **`pre_review_hook.py` inversion has exactly ONE owner** — do not let both the Path-A lane (IC-05) and the consumer-inversion lane (E) claim it.
6. **Artifact-guard watch-item:** the composed-action guard shares *selection* only; `resolve_gates` returns `[]` for its `(mission, action)` keys today (this mission binds only the pre-review gate, FR-013), so its selection-inversion WP is anti-drift insurance, NOT a replacement of its hardcoded missing-artifact check — SC-010 (fail-closed hard-blocks preserved) is its acceptance criterion.
7. **`ScopeSource` `derive` output type is `Scope`** (see data-model `TransitionContext.scope`) — thread one `Scope`/`ScopeResult` type through handler + asset, don't fork it.
