# Contract: SSOT Gate-*Selection* Seam (the single selection entry point)

**Keystone of the mission — SELECTION, not reduction.** Both runtime consumers —
the `move-task` pre-review hook and `runtime_bridge._check_composed_action_guard`
— obtain their gate set from this one seam. No second resolver, no re-implemented
selection. **Reduction is per gate-class and stays with each consumer** (see
below). (research §0; FR-002/FR-003/FR-006; C-001/C-005; NFR-005.)

## Interface

### Selection (the SSOT — both consumers share this)
```
resolve_gates(mission_id: str, transition: str, activation: ActivationState) -> list[ResolvedGate]
```
- **Deterministic + ordered.** Same inputs → same ordered list (stable across processes).
- Reads step-contract bindings (`MissionStepContractRepository.get_by_action`) and applies charter activation. Activation is evaluated on the **owning step-contract node** (the activatable unit) — NOT the asset/handler URN, which is absent from the DRG singular↔plural kind maps (`asset`/`gate-handler` not in `_SINGULAR_TO_PLURAL`, `src/charter/drg.py:187`) and would therefore default-allow. This is the **only** gate-selection call site.
- **Lane↔action adapter.** The move-task side keys on a lane (`for_review`); `get_by_action` keys on a mission action (`specify`/`plan`/`tasks`/…) — `get_by_action(mission, "for_review")` is `None` today. The seam owns a small adapter that maps the consumer's key (lane or action) to the contract's action key, so both consumers resolve through one path.
- Returns `[]` when nothing is declared/active → the caller renders `CALM_NOTICE` (FR-008). `[]` is NEVER "verified clean".

### Reduction (per gate-class — NOT unified)
```
run_gate(resolved: ResolvedGate, ctx: TransitionContext) -> OperatorOutcome   # TEST/verdict gates only
```
- Dispatches a Path-A handler or a Path-B asset (behind the trust envelope) for **test/verdict** gates and folds every fault via the FR-014 fail-open reducer (owned here). No exception escapes to the consumer. (C-002/FR-010.)
- The **artifact-presence** guard (`_check_composed_action_guard`) is NOT routed through `run_gate`: it keeps its existing **fail-closed** reduction (returns `list[str]`, hard-blocks on missing spec/plan/tasks, consumed at `runtime_bridge.py:1783`). Routing it through the "only regression blocks" reducer would silently downgrade its hard-blocks to warns (SC-010). It shares *selection* only.

## Invariants (contract tests MUST assert)
1. **Single selection authority.** Both consumers obtain their gate set from `resolve_gates`; neither re-implements binding-read + activation for gate *selection*. Each consumer keeps its own *reduction*. (Guards NFR-005 + prevents selection drift — research §0.)
2. **Determinism.** Repeated `resolve_gates` on a fixed fixture returns byte-identical ordered results.
3. **Empty ≠ clean.** `resolve_gates` returning `[]` maps to `CALM_NOTICE`, never `PASS`/`no_new_failures`.
4. **Fault containment (test gates).** For every fault class (asset resolve error, runner crash, non-zero exit, timeout, malformed/absent verdict, missing test command, trust refusal, inactive doctrine) `run_gate` returns a non-blocking `OperatorOutcome` — it never raises. Scoped to test/verdict gates. (Fault-injection acceptance test — SC-005.)
5. **Only regression blocks (test gates).** `run_gate` returns `BLOCK` **iff** the gate emitted a valid `GateVerdict(status=regression, blocking=true)`. Any other input (including a crash mimicking a failure) is non-blocking. (C-002/B5.) The artifact-presence guard's fail-closed blocks are governed by its own reduction, not this invariant (SC-010).
6. **No internal leakage.** No `OperatorOutcome.message` for a consumer-shaped fixture contains `tests.architectural._gate_coverage` or `src/specify_cli/`. (SC-001/NFR-002.)

## Migration discipline (research §0/§5)
- **Extract-then-inject.** Extract current selection behind the seam with characterization tests on the live `(mission, action)` matrix BEFORE inverting either consumer. Never edit the F(48) `_check_composed_action_guard` in place.
- The seam is its own work package, sequenced before both consumer inversions (IC-02 before the consumer wiring).
- The F(48) `_check_composed_action_guard` inversion is isolated in its **own** WP and **coordinated with #2531** (concurrent `runtime_bridge` decomposition — owned-file collision on the same F(48) file).

## Non-goals
- The seam does not run tests or derive scope itself — it dispatches to handler/asset which use a `ScopeSource`. It does not know about pytest.
- The seam does not unify reduction — artifact-presence guards keep fail-closed semantics (FR-002).
