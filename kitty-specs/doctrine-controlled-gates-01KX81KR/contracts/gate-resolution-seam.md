# Contract: SSOT Gate-Resolution Seam (the single entry point)

**Keystone of the mission.** Both runtime consumers — the `move-task` pre-review
hook and `runtime_bridge._check_composed_action_guard` — MUST resolve gates
through this one seam. No second resolver, no re-implemented selection. (research §0; FR-002/FR-003; C-001/C-005; NFR-005.)

## Interface

```
resolve_gates(mission_id: str, transition: str, activation: ActivationState) -> list[ResolvedGate]
```
- **Deterministic + ordered.** Same inputs → same ordered list (stable across processes).
- Reads step-contract bindings (`MissionStepContractRepository.get_by_action`) and applies charter activation (`filter_graph_by_activation`, `src/charter/drg.py:319`) — this is the **only** call site of that selection for gates.
- Returns `[]` when nothing is declared/active → the caller renders `CALM_NOTICE` (FR-008). `[]` is NEVER "verified clean".

```
run_gate(resolved: ResolvedGate, ctx: TransitionContext) -> OperatorOutcome
```
- Dispatches Path-A handler or Path-B asset (behind the trust envelope).
- **Owns the fail-open reduction boundary**: catches every fault and folds it via the FR-014 reducer. No exception escapes to the consumer. (C-002/FR-010.)

## Invariants (contract tests MUST assert)
1. **Single call site.** A test asserts both consumers import/inject this seam and neither calls `filter_graph_by_activation` / `get_by_action` directly for gate decisions. (Guards NFR-005 + prevents resolver drift — research §0.)
2. **Determinism.** Repeated `resolve_gates` on a fixed fixture returns byte-identical ordered results.
3. **Empty ≠ clean.** `resolve_gates` returning `[]` maps to `CALM_NOTICE`, never `PASS`/`no_new_failures`.
4. **Fault containment.** For every fault class (asset resolve error, runner crash, non-zero exit, timeout, malformed/absent verdict, missing test command, trust refusal, inactive doctrine) `run_gate` returns a non-blocking `OperatorOutcome` — the seam never raises. (Fault-injection acceptance test — SC-005.)
5. **Only regression blocks.** `run_gate` returns `BLOCK` **iff** the gate emitted a valid `GateVerdict(status=regression, blocking=true)`. Any other input (including a crash mimicking a failure) is non-blocking. (C-002/B5.)
6. **No internal leakage.** No `OperatorOutcome.message` for a consumer-shaped fixture contains `tests.architectural._gate_coverage` or `src/specify_cli/`. (SC-001/NFR-002.)

## Migration discipline (research §0/§5)
- **Extract-then-inject.** Extract current selection behind the seam with characterization tests on the live `(mission, action)` matrix BEFORE inverting either consumer. Never edit the F(48) `_check_composed_action_guard` in place.
- The seam is its own work package, sequenced before both consumer inversions (IC-02 before IC-05/IC-08 wiring).

## Non-goals
- The seam does not run tests or derive scope itself — it dispatches to handler/asset which use a `ScopeSource`. It does not know about pytest.
