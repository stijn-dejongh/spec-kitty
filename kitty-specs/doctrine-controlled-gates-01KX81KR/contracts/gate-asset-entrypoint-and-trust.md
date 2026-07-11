# Contract: Path-B Gate-Asset Entrypoint + Trust Envelope

Governs executing doctrine-supplied gate code. Default-off; contained; fail-open. (FR-004/005/007/015; NFR-004a/b/006; C-003/C-007.)

## Entrypoint contract
A gate asset (`*.asset.yaml` with the executable gate shape) declares:
- `entrypoint` — a module:function or script path *inside the asset*.
- `interpreter` — from the interpreter allowlist (no shell; argv-vector invocation only).
- Runtime input: a structured `TransitionContext` (mission, transition, changed files, scope) passed via a controlled channel (argv/stdin/env — never shell-interpolated).
- Runtime output: a single well-formed `GateVerdict` on a structured channel. Anything else (no output, malformed, extra output over the size limit) = fault → FAULT_WARN.

Non-gate assets remain inert: the runner activates **only** on the executable gate-asset shape; a plain `*.asset.yaml` is never executed (C-003).

## Trust envelope (ALL must hold or the asset is NOT executed → TRUST_REFUSAL)
1. **Derived provenance allowlist** — provenance ∈ {built_in, org_pack} by default; **derived from pack-load metadata, never self-declared by the asset**. third_party is refused unless an org explicitly widens (out of scope here; see #2536).
2. **Opt-in** — `review.allow_executable_gate_assets` is `true` (default **false**).
3. **Interpreter allowlist / no shell** — interpreter ∈ allowlist; argv-vector; env scrubbed (reuse the `run_scoped_tests_at_head` precedent, `pre_review_gate.py:358`).
4. **Timeout** — enforced; over-run → terminate → FAULT_WARN.
5. **Filesystem confinement** — writes limited to a scratch/working-tree dir; no out-of-tree writes.
6. **No network egress.**
7. **Resource limits** — memory / CPU / output-size caps.
8. **Refuse-if-unconfinable** — if the host lacks a required containment primitive, **refuse** (TRUST_REFUSAL); NEVER run unconfined.

## Tests (acceptance)
- **NFR-004a** provenance refusal: non-allowlisted-provenance asset whose entrypoint would drop a sentinel side effect → after transition the sentinel is ABSENT.
- **NFR-004b** opt-in refusal: allowlisted asset, flag off → sentinel absent + TRUST_REFUSAL.
- **SC-007** containment: asset attempting network egress or out-of-tree write → contained/terminated → FAULT_WARN (does not succeed).
- **NFR-006** timeout: over-running asset terminated → FAULT_WARN.
- **C-007** the `tests/architectural/untrusted_path_audit/` harness is EXTENDED to include this code-exec sink (fails if a new unaudited exec path is added).
