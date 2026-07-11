---
work_package_id: WP04
title: Test-gate reducer + FR-014 outcomes
dependencies:
- WP03
requirement_refs:
- FR-010
- FR-014
- FR-019
- C-002
- FR-008
tracker_refs:
- '2535'
planning_base_branch: design/doctrine-controlled-gates
merge_target_branch: design/doctrine-controlled-gates
branch_strategy: Planning artifacts for this mission were generated on design/doctrine-controlled-gates. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into design/doctrine-controlled-gates unless the human explicitly redirects the landing branch.
subtasks:
- T016
- T017
- T018
- T019
- T020
phase: Lane B - Test-gate reducer
history:
- at: '2026-07-11T00:00:00Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: python-pedro
authoritative_surface: src/specify_cli/review/gates/
execution_mode: code_change
owned_files:
- src/specify_cli/review/gates/outcomes.py
create_intent:
- src/specify_cli/review/gates/outcomes.py
role: implementer
tags: []
task_type: implement
---

# Work Package Prompt: WP04 — Test-gate reducer + FR-014 outcomes

## Objective

Build the **test/verdict-gate reduction boundary** — the fail-open reducer that turns a `GateVerdict` (or a fault, or a trust refusal) into an `OperatorOutcome`, and the seam's `run_gate` that dispatches a resolved gate and **folds every fault class to a non-blocking outcome**. This is the FR-014 canonical mapping made executable. It is the reduction the SSOT seam (WP03) owns for **test/verdict gates only** — the former IC-08, folded into IC-02 because `run_gate` cannot meet its fault-containment / only-regression invariants without it.

**Scope discipline:** this reducer governs **test/verdict gates only**. The artifact-presence composed-action guard (`_check_composed_action_guard`) is NOT routed through this reducer — it keeps its own **fail-closed** reduction (SC-010). Do not generalize this into a universal reducer.

## Context

**Mission**: `doctrine-controlled-gates-01KX81KR` · **Epic**: #2535 · **Branch**: `design/doctrine-controlled-gates`

**Why this exists.** The whole system is **fail-open** (C-002): no gate-infrastructure fault may ever block a transition. Only a real, well-formed regression may block. Today the pre-review hook hand-folds faults to `no_coverage` at `tasks_move_task.py:905-909`; this WP replaces that ad-hoc fold with a single canonical, tested reducer so every test/verdict gate obeys the same mapping.

**The load-bearing invariant (C-002 / spec B5).** BLOCK is reachable **only** from an explicitly emitted, well-formed `GateVerdict(status=regression, blocking=true)`. A crashed, killed, timed-out, or garbled gate is a **fault → FAULT_WARN**, NEVER BLOCK. A gate that mimics a failure by crashing must not be read as a regression. This is the single most important behavioral guarantee in the mission.

**Depends on WP03.** `run_gate` consumes a `ResolvedGate` (from `resolve_gates`) and dispatches through the WP03 handler/asset **Protocol**. The Path-A handler (WP08) and the Path-B asset runner (WP10) *implement* that Protocol — this WP dispatches through it and reduces the result; it does not import those implementations directly (forward-only; dispatch by `binding.mechanism` through the Protocol).

## Branch Strategy

- **Planning base**: `design/doctrine-controlled-gates`.
- **Final merge target**: `design/doctrine-controlled-gates`.
- **Execution worktree**: allocated from `lanes.json` at implement time.

## Ordered Steps

Work in order. T019 (table-driven mapping test) and T020 (fault-injection) are the ATDD acceptance surface — write them **red-first** against the mapping before the reducer body is complete, so the reducer is driven by the FR-014 table, not the other way round.

### T016 — `outcomes.py`: the FR-014 verdict→operator-outcome reducer

**Purpose**: The canonical, pure reduction the whole system obeys for test/verdict gates.

1. Create `src/specify_cli/review/gates/outcomes.py`. Model the `OperatorOutcome` result: one of `BLOCK | FAULT_WARN | CALM_NOTICE | TRUST_REFUSAL | PASS` (data-model.md) plus its operator-facing message and a `blocks: bool` flag.
2. Implement the pure reducer — a function that takes one of: a valid `GateVerdict`, a **fault** (no valid verdict), **no active gate**, or a **trust refusal** — and returns the `OperatorOutcome` per the FR-014 mapping table (`contracts/gate-verdict-and-outcomes.md`):

   | Condition | Outcome | Blocks? |
   |-----------|---------|---------|
   | Valid `status=regression`, `blocking=true` | **BLOCK** | **Yes (only case)** |
   | Valid `status=regression`, `blocking=false` | FAULT_WARN | No |
   | Valid `status=no_new_failures` | PASS | No |
   | Valid `status=no_coverage` | CALM_NOTICE | No |
   | Valid `status=error` | FAULT_WARN | No |
   | No gate declared/active | CALM_NOTICE | No |
   | Fault (resolve fail / crash / non-zero exit / timeout / malformed or absent verdict / missing test command / inactive doctrine) | FAULT_WARN | No |
   | Trust refusal (provenance not allowlisted / opt-in off / unconfinable host) | TRUST_REFUSAL | No |
3. **`notice` vs `warn` vs `refusal` are distinct — never conflate them.** CALM_NOTICE = "nothing to run here, all good"; FAULT_WARN = "something meant to run couldn't"; TRUST_REFUSAL = "we chose not to execute this". Model them as distinct outcomes with distinct operator wording.
4. **No internal leakage.** Every `OperatorOutcome.message` is operator-facing and MUST NOT name a spec-kitty-internal module/path (no `tests.architectural._gate_coverage`, no `src/specify_cli/`). This is the FR-008/NFR-002 contract at the message boundary.
5. Keep the reducer **pure** (verdict/fault-descriptor in → outcome out) so it is trivially table-testable and stays ≤ C(15). Push any I/O (running the gate, reading the channel) into `run_gate`.

### T017 — `run_gate`: fold every fault class to a non-blocking outcome; only valid `regression(blocking)` BLOCKs

**Purpose**: The seam's execution+reduction boundary for test/verdict gates. **No exception escapes to the consumer** (C-002/FR-010).

1. Implement `run_gate(resolved: ResolvedGate, ctx: TransitionContext) -> OperatorOutcome` (the interface from `contracts/gate-resolution-seam.md`). It:
   - dispatches the resolved gate via the WP03 Protocol, selecting the arm by `resolved.binding.mechanism` (`handler` → Path-A handler dispatch, WP08; `asset` → Path-B runner behind the trust envelope, WP10);
   - wraps **all** dispatch in fault containment: any exception, non-zero exit, timeout, crash, malformed/absent verdict, missing test command, inactive doctrine, or trust refusal is caught and folded via the T016 reducer to a non-blocking `OperatorOutcome`. `run_gate` **never raises**.
2. **Only regression blocks.** `run_gate` returns an outcome with `blocks=true` **iff** the dispatched gate produced a valid `GateVerdict(status=regression, blocking=true)`. Every other path — including a crash that mimics a failure — is non-blocking. Encode this as the single BLOCK gate in the fold, not as scattered conditionals.
3. **Trust refusal is not a fault, it's a distinct outcome.** A `refused` activation_state / trust-envelope refusal (Path B, populated by WP10/WP11) reduces to TRUST_REFUSAL (non-blocking), not FAULT_WARN. Route it distinctly.
4. **Forward-only on the arms.** Dispatch through the Protocol; do not hard-import `handlers/pre_review.py` (WP08) or `assets/runner.py` (WP10). At this WP's time the arms may be stubbed via the Protocol for testing — the fault-injection tests (T020) feed synthetic verdicts/faults through a fake Protocol impl.
5. Export `run_gate` + `OperatorOutcome` + the reducer from the package (extend `review/gates/__init__.py`'s public surface established in WP03 — reduction is exported here, selection was exported in WP03).

### T018 — Dedicated size-capped schema-validated verdict read (stray stdout can't forge — FR-019)

**Purpose**: A Path-B asset emits its `GateVerdict` on a **dedicated, size-capped, schema-validated channel** — not shared stdout. Stray stdout must never forge a passing or blocking verdict.

1. Implement the verdict **read** side: parse a `GateVerdict` only from the dedicated channel (e.g. a fixed fd / a temp verdict file the runner controls — the exact transport is finalized with the WP10 runner; this WP owns the *read + validation* contract). Enforce:
   - a **size cap** — oversized output is a fault (FAULT_WARN), not a truncated-but-accepted verdict;
   - **schema validation** — the payload must validate against the `GateVerdict` schema (`status ∈ {no_new_failures, regression, no_coverage, error}`, `blocking: bool`, `message: str`); malformed → fault;
   - **absent** verdict (channel empty / no emission) → fault.
2. **stdout is not a verdict source.** Anything printed to the asset's stdout/stderr is diagnostic noise, never parsed as a verdict. A test where the asset prints a fake `regression(blocking=true)` to stdout MUST yield FAULT_WARN (absent-on-dedicated-channel), NOT BLOCK. This is SC-011.
3. Wire the read into `run_gate`'s Path-B fold: a malformed/oversized/absent verdict on the dedicated channel is one of the fault classes → FAULT_WARN.

### T019 — Table-driven test over the full FR-014 mapping

**Purpose**: Enumerate every mapping row and assert outcome + blocks-flag (the ATDD acceptance for the mapping).

1. One table-driven test that enumerates **every** row of the FR-014 table (T016 step 2). Each case asserts both the `OperatorOutcome` and its `blocks` flag.
2. Include the two `regression` rows explicitly (`blocking=true` → BLOCK; `blocking=false` → FAULT_WARN) — the blocking flag, not the status alone, decides.
3. Assert no message in any row leaks a spec-kitty-internal module/path (guards FR-008/NFR-002 at the reducer).

### T020 (red-first) — Fault-injection tests: crash/non-zero/timeout/malformed/absent → FAULT_WARN (SC-005)

**Purpose**: Prove fail-open for every fault class — the SC-005 acceptance.

1. Fault-injection tests feeding `run_gate` (through a fake Protocol impl / synthetic `ResolvedGate`) each fault class:
   - runner **crash** (raises);
   - **non-zero exit**;
   - **timeout**;
   - **malformed** verdict (schema-invalid on the dedicated channel);
   - **absent** verdict (nothing emitted);
   - **missing test command** (handler has no configured `review.test_command`);
   - **inactive doctrine** (no active gate — CALM_NOTICE, distinct from fault);
   - **trust refusal** (→ TRUST_REFUSAL, distinct from fault).
2. Assert each yields the correct **non-blocking** outcome per FR-014, and that **none** blocks the transition. Explicitly assert a **crash mimicking a failure is FAULT_WARN, never BLOCK / never read as `regression`** (C-002 / spec B5).
3. Write these red-first: they should fail against an empty `run_gate` and drive the fold to green.

## Acceptance

- **SC-005**: every injected FR-010 fault class yields the correct non-blocking outcome per the FR-014 table; **none** blocks the transition; a crashed/timed-out/malformed gate is **never** read as `regression`.
- **SC-011**: a Path-B asset that prints a fake verdict to stdout yields FAULT_WARN — the verdict is read only from the dedicated, size-capped, schema-validated channel (FR-019); stray stdout cannot forge a passing or blocking verdict.
- **Only regression blocks** (C-002): `run_gate` returns a blocking outcome **iff** the gate emitted a valid `GateVerdict(status=regression, blocking=true)`. Every other input — including a crash — is non-blocking.
- **`run_gate` never raises**: all fault classes are contained inside the seam; no exception escapes to the consumer.
- **CALM_NOTICE ≠ PASS ≠ FAULT_WARN ≠ TRUST_REFUSAL**: the four non-block outcomes are distinct with distinct operator wording; no conflation.
- **No internal leakage**: no `OperatorOutcome.message` names a spec-kitty-internal module/path.
- **Test/verdict scope only**: the reducer is not wired to the artifact-presence guard (that keeps fail-closed — SC-010, WP14's concern).
- `ruff`/`mypy` clean on `outcomes.py`; reducer ≤ C(15); no `# noqa`/`# type: ignore` added; the table-driven + fault-injection tests give the new branches focused coverage (Sonar new-code).

## Safeguards

- **Only a valid `regression(blocking=true)` may BLOCK.** A crashed / timed-out / non-zero-exit / malformed-verdict / absent-verdict gate is FAULT_WARN, **never** BLOCK. This is the C-002 fail-open invariant — the whole WP exists to guarantee it. Do not add any other BLOCK path.
- **Verdict is read from the dedicated channel, NOT stdout.** Stray stdout can't forge a verdict (FR-019/SC-011). Size-cap + schema-validate the dedicated channel; absent/oversized/malformed → FAULT_WARN.
- **Test/verdict gates only.** Do NOT route the artifact-presence guard through this reducer — that would silently downgrade its fail-closed hard-blocks to warns (SC-010). This reducer's home is test/verdict gates; the artifact guard keeps its own reduction (WP14).
- **Fold, don't scatter.** One reduction table (T016) and one BLOCK gate in `run_gate`. Do not re-derive the mapping at call sites.
- **Forward-only on dispatch arms.** Dispatch via the WP03 Protocol by `binding.mechanism`; do not import the WP08 handler or WP10 runner implementations — a fake Protocol impl drives the tests.
- **Preserve the FR-010 fail-open scaffolding semantics.** This reducer *replaces* the ad-hoc fold at `tasks_move_task.py:905-909` in intent — but the actual consumer inversion (pointing the move-task hook at `run_gate`) is WP13, not this WP. Here, ship the reducer + tests; do not edit the move-task hook.

## References

- **Verdict/outcome contract**: `contracts/gate-verdict-and-outcomes.md` (the FR-014 mapping table + rules) — the authority for this WP.
- **Seam contract**: `contracts/gate-resolution-seam.md` §Reduction (`run_gate` signature; per-gate-class reduction; invariants 4 & 5 — fault containment + only-regression-blocks).
- **Data model**: `data-model.md` — `GateVerdict` (`status`/`blocking`/`message`/`scope_evidence`), `OperatorOutcome`, `TransitionContext`, `ResolvedGate`.
- **Research §0**: the seam owns the test-gate fail-open reduction boundary (per gate-class; artifact guard NOT routed through `run_gate`).
- **Current ad-hoc fold (replaced in intent; do NOT edit here)**: `tasks_move_task.py:905-909` (folds faults to `no_coverage`).
- **Verdict tail (produces the `GateVerdict` this reducer consumes; reused by WP08)**: `evaluate_with_scope` `src/specify_cli/review/pre_review_gate.py:451-511`.
- **WP03 Protocol/`ResolvedGate`**: `src/specify_cli/review/gates/resolver.py` + `__init__.py`.
