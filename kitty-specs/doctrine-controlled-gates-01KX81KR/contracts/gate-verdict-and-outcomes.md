# Contract: Gate Verdict → Operator Outcome (FR-014)

The single canonical mapping the whole system obeys. The reducer that implements
it (`review/gates/outcomes.py`) is the fail-open boundary owned by the resolution seam.

## Inputs
- A `GateVerdict` (from a handler/asset), OR a **fault** (no valid verdict), OR
  **no active gate**, OR a **trust refusal**.

## Mapping

| Condition | Operator Outcome | Blocks transition? |
|-----------|------------------|--------------------|
| Valid verdict `status=regression`, `blocking=true` | **BLOCK** | **Yes** (only case) |
| Valid verdict `status=regression`, `blocking=false` | FAULT_WARN | No |
| Valid verdict `status ∈ {no_new_failures}` | PASS | No |
| Valid verdict `status=no_coverage` | CALM_NOTICE | No |
| Valid verdict `status=error` | FAULT_WARN | No |
| No gate declared/active for the transition | CALM_NOTICE | No |
| Fault: asset resolve fail / runner crash / non-zero exit / timeout / malformed or absent verdict / missing test command / inactive doctrine | FAULT_WARN | No |
| Trust: provenance not allowlisted / opt-in off / unconfinable host | TRUST_REFUSAL | No |

## Rules
- **BLOCK is reachable only from an explicitly emitted, well-formed `regression(blocking=true)` verdict.** A crashed/killed/garbled gate is a fault → FAULT_WARN, NEVER BLOCK. (C-002 / spec B5.)
- **`notice` vs `warn` are distinct** and must not be conflated: CALM_NOTICE = "nothing to run here, all good"; FAULT_WARN = "something meant to run couldn't". TRUST_REFUSAL = "we chose not to execute this".
- Every message is operator-facing and MUST NOT name spec-kitty-internal modules/paths.

## Tests
- One table-driven test enumerating every row → asserts outcome + blocks-flag.
- Fault-injection tests feeding malformed/absent/crash verdicts assert FAULT_WARN + non-blocking (SC-005).
