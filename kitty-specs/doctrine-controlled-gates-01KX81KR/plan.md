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
subsystem's activation selects which are active. Both runtime consumers resolve
through **one SSOT gate-resolution seam** (see research §0) that also owns
fail-open reduction. The pre-review regression gate is migrated as the Path-A
exemplar, closing #2534 fully and #2330 for the selection path.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: pydantic (frozen models, `extra="forbid"`), ruamel.yaml (doctrine YAML), the existing charter/DRG subsystem (`src/charter/`, `filter_graph_by_activation`), `review/baseline.py` + `review/pre_review_gate.evaluate_with_scope` (reused verdict tail), `subprocess` + host OS isolation primitives (Path-B runner)
**Storage**: doctrine YAML (`*.step-contract.yaml`, `*.asset.yaml`), generated DRG (`graph.yaml`/`references.yaml`), `.kittify/config.yaml` (opt-in flag), gate assets on disk (resolved via URN→path)
**Testing**: pytest — characterization/golden tests (behavior-preserving extractions), contract tests (the SSOT seam), fault-injection tests (fail-open), trust/containment tests, and an extension of `tests/architectural/untrusted_path_audit/`
**Target Platform**: Linux/macOS CLI (cross-platform; containment primitives are host-dependent → refuse-if-unconfinable, never run unconfined)
**Project Type**: single (CLI + library)
**Performance Goals**: gate execution bounded by an enforced timeout (default mirrors the baseline ~300 s); resolution seam is O(active bindings) — negligible
**Constraints**: fail-open invariant (only a valid emitted `regression(blocking)` may block); cognitive-complexity ceiling 15 (S3776/C901); no new public CLI surface beyond the observability query + the opt-in flag; `extra="forbid"` models → versioned schema evolution + migration; no doctrine code executes on Path A
**Scale/Scope**: ~8–10 WPs; surfaces: `src/specify_cli/review/`, `src/specify_cli/cli/commands/agent/tasks_move_task.py`, `src/runtime/next/runtime_bridge.py`, `src/charter/`, `src/doctrine/assets/`, `src/doctrine/missions/`

## Charter Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Single canonical authority** ✅ — charter activation is the sole gate-selection authority (C-001); exactly **one** SSOT resolution seam both consumers depend on (research §0). No parallel registry/resolver.
- **Architectural alignment** ✅ — reuse `filter_graph_by_activation` + `evaluate_with_scope`; the binding + seam is the only new decision surface (C-005). No legacy fallback (C-004, unification-not-parity).
- **DDD + tiered rigour** ✅ — core (resolution seam, runner, trust envelope, fault reducer) = high rigour + contract tests; glue (observability query, doc/yaml wiring) = standard rigour.
- **ATDD-first** ✅ — contract tests for the seam + fault-injection acceptance tests precede implementation; characterization tests precede every extraction.
- **Campsite-first** ✅ — IC-01 tidy-first hook extraction opens the surface before the functional change; broader god-module debt stays tracked (#2116).
- **Trust/safety** ✅ — executing doctrine code (Path B) is gated by a real containment envelope + default-off opt-in + derived provenance; the untrusted-input audit harness is extended (C-007).

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
│   │   └── gates/                       # NEW: SSOT resolution seam, verdict→outcome reducer, handler registry
│   │       ├── resolver.py              # the single GatePorts entry point
│   │       ├── outcomes.py              # FR-014 reducer (fail-open boundary)
│   │       ├── handlers/                # Path-A handlers (pre-review exemplar)
│   │       └── scope_source.py          # ScopeSource protocol + built-in spec-kitty impl
│   └── cli/commands/agent/
│       ├── tasks_move_task.py           # invert the pre-review hook onto the seam
│       └── pre_review_hook.py           # NEW (IC-01): extracted hook block, behavior-preserving
├── runtime/next/runtime_bridge.py       # invert _check_composed_action_guard onto the SAME seam
├── charter/
│   └── step_contracts.py                # + versioned gate-binding field (migration)
└── doctrine/
    ├── assets/                          # NEW Path-B substrate: repository.py, resolver.py, runner.py, entrypoint.py
    └── missions/models.py               # + gate-binding on unified MissionStep (migration)

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

### IC-02 — SSOT gate-resolution seam (the keystone)
- **Purpose**: One injected entry point mapping `(mission, transition, activation)` → ordered `ResolvedGate` list; the ONLY place that reads bindings + applies charter activation; owns the fail-open reduction boundary. Both consumers depend on it.
- **Relevant requirements**: FR-002, FR-003, FR-006; C-001, C-005.
- **Affected surfaces**: new `review/gates/resolver.py`; `runtime_bridge._check_composed_action_guard` (F48) and the extracted pre-review hook both inverted onto it.
- **Sequencing/depends-on**: IC-01.
- **Risks**: highest-regression edit (F48 god-module). **Extract-then-inject**: characterization tests on the current `(mission, action)` matrix FIRST; never edit-in-place. If both consumers don't route through it, NFR-005 is unprovable.

### IC-03 — Gate-binding schema + migration (charter spine)
- **Purpose**: Add the declarative `transition → gate` binding to `MissionStepContractStep` and unified `MissionStep`; migrate built-in step contracts.
- **Relevant requirements**: FR-001, FR-006, FR-016; C-006.
- **Affected surfaces**: `charter/step_contracts.py:65`, `doctrine/missions/models.py:87`, built-in `*.step-contract.yaml`, a migration.
- **Sequencing/depends-on**: none for schema; **migration-first within the charter-spine lane** (step_contracts→executor→drg→pack_validator→merge co-change tightly — one lane, no parallel).
- **Risks**: `extra="forbid"` → old contracts must still load (FR-016/SC-009). Coupled spine ripple.

### IC-04 — ScopeSource abstraction + built-in spec-kitty ScopeSource
- **Purpose**: Make scope derivation a doctrine-declared strategy; move `_SRC_PACKAGE_PREFIX` / `_gate_coverage` census into a built-in ScopeSource used only when spec-kitty's own doctrine is active.
- **Relevant requirements**: FR-009, FR-012; NFR-002.
- **Affected surfaces**: `pre_review_gate.py` (`derive_test_scope`, `_load_gate_coverage_module`, `_default_filter_groups/_default_composite_routing`).
- **Sequencing/depends-on**: IC-02 (verdict interface).
- **Risks**: `derive_test_scope` at the C(15) ceiling — extraction must not exceed it.

### IC-05 — Pre-review handler (Path-A exemplar migration)
- **Purpose**: Re-express the pre-review gate as a built-in **handler** bound via a built-in step contract; invert the hardcoded invocation through the IC-02 seam; reuse `evaluate_with_scope`; preserve existing config semantics.
- **Relevant requirements**: FR-011, FR-017; NFR-001; SC-003.
- **Affected surfaces**: `review/gates/handlers/`, a built-in step contract, `pre_review_gate.py` (decision path removed).
- **Sequencing/depends-on**: IC-02, IC-03, IC-04.
- **Risks**: verdict parity on spec-kitty's own repo (no opt-in).

### IC-06 — Executable ASSET substrate (Path-B)
- **Purpose**: Greenfield asset repository + URN→path resolver + code-asset entrypoint contract + runner returning a structured verdict; code-exec keyed on the gate-asset shape (non-gate assets stay inert).
- **Relevant requirements**: FR-004, FR-005; C-003.
- **Affected surfaces**: new `doctrine/assets/{repository,resolver,runner,entrypoint}.py`.
- **Sequencing/depends-on**: IC-02 (verdict interface), IC-03 (binding names asset).
- **Risks**: new subsystem; must not generalize asset loading into code-exec.

### IC-07 — Trust envelope + containment
- **Purpose**: Confine Path-B execution: derived provenance allowlist, `review.allow_executable_gate_assets` opt-in (default off), interpreter allowlist/no-shell, timeout, filesystem confinement, no network egress, resource limits, refuse-if-unconfinable.
- **Relevant requirements**: FR-007, FR-015; NFR-004a/b, NFR-006; C-007.
- **Affected surfaces**: the IC-06 runner, config, `tests/architectural/untrusted_path_audit/` (extended).
- **Sequencing/depends-on**: IC-06.
- **Risks**: RCE-adjacent — extend the audit harness or it goes stale-green; reuse the `run_scoped_tests_at_head` argv/no-shell/timeout/env-scrub precedent.

### IC-08 — Fault→outcome reducer + fail-open enforcement
- **Purpose**: Implement the FR-014 canonical mapping; only a valid emitted `regression(blocking)` blocks; every fault → FAULT-WARN / TRUST-REFUSAL / CALM-NOTICE.
- **Relevant requirements**: FR-010, FR-014; NFR-003; C-002; SC-005.
- **Affected surfaces**: `review/gates/outcomes.py` (the reduction boundary owned by IC-02's seam).
- **Sequencing/depends-on**: IC-02.
- **Risks**: the load-bearing invariant; a crashed/timed-out/malformed gate must never read as regression.

### IC-09 — Observability + operator surface
- **Purpose**: Answer "which gates are active for this transition, from which doctrine, and why did/didn't each run".
- **Relevant requirements**: FR-018; SC-008.
- **Affected surfaces**: a read-only query over the IC-02 seam (CLI subcommand or `agent tasks status` extension).
- **Sequencing/depends-on**: IC-02.
- **Risks**: keep loopback/read-only; no new heavy CLI surface.
