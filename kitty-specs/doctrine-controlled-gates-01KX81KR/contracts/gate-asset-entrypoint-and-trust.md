# Contract: Path-B Gate-Asset Entrypoint + Trust Envelope (refuse-unconfinable v1, RD-006)

Governs executing doctrine-supplied gate code. Default-off; contained by cheap-real
primitives; **refuse where it cannot be confined**; fail-open. **No new sandbox
dependency** — deeper OS sandboxing is deferred. (FR-004/005/007/015/019; NFR-004a/b/006; C-003/C-007/C-008; RD-006.)

## Entrypoint contract
A gate asset (`*.asset.yaml` with the executable gate shape) declares:
- `entrypoint` — a module:function or script path *inside the asset*.
- `interpreter` — from the interpreter allowlist (no shell; argv-vector invocation only).
- Runtime input: a structured `TransitionContext` (mission, transition, changed files, scope) passed via a controlled channel (argv/stdin/**allowlisted env** — never shell-interpolated).
- Runtime output (FR-019): a single well-formed `GateVerdict` on a **dedicated, size-capped, schema-validated verdict channel** — NOT shared stdout. No output / malformed / oversized / absent = fault → FAULT_WARN. Stray stdout can never forge a passing or blocking verdict.

Non-gate assets remain inert: the runner activates **only** on the executable gate-asset shape; a plain `*.asset.yaml` is never executed (C-003).

## Trust envelope (ALL must hold or the asset is NOT executed → TRUST_REFUSAL)
1. **Derived provenance allowlist** — provenance ∈ {built_in, org_pack} by default; **derived from pack-load metadata, never self-declared by the asset**. **Required fix (C-008):** the loader currently overwrites `source_kind` (`org_pack_loader.py:403`) and the pack layer only distinguishes built-in/org/project (`merge.py:20-22`), so today every configured pack reads as `org` and the allowlist admits everything — NFR-004a/SC-012 are untestable until a genuine `third_party` tier is producible/refusable. The loader MUST stop overwriting `source_kind` so provenance is derivable.
2. **Opt-in** — `review.allow_executable_gate_assets` is `true` (default **false**).
3. **Interpreter allowlist / no shell / environment allowlist** — interpreter ∈ allowlist; argv-vector; the child gets an **explicitly constructed env, never `dict(os.environ)` inheritance**. (The `run_scoped_tests_at_head` precedent, `pre_review_gate.py:358`, is reused only for argv/no-shell/timeout — it does `env = dict(os.environ)` at `:374` (full inheritance), which Path-B must NOT copy or ambient `GITHUB_TOKEN`/cloud creds reach the asset. C-007/C-008.)
4. **Timeout with process-group kill** — enforced timeout; the runner kills the whole **process group** (grandchildren included), not just the direct child. Over-run → terminate → FAULT_WARN.
5. **Path-resolved filesystem confinement** — writes limited to a scratch/working-tree dir, enforced on the **symlink-resolved real path** (no `..`/symlink escape); no out-of-tree writes.
6. **Resource limits via `setrlimit`** — CPU / memory / output-size caps applied to the child before exec.
7. **Capability probe → refuse-if-unconfinable** — the runner probes whether the host can actually confine filesystem + network; if it **cannot**, the asset is **refused** (TRUST_REFUSAL), **never run unconfined**. No network-namespace dependency is added in v1; where true fs/network isolation is unavailable, refusal — not unconfined execution — is the outcome.
8. **Deferred (RD-006):** deeper OS-level sandboxing (namespaces / landlock / seccomp / a sandbox system dependency) and per-gate network-egress *permitting*. v1 refuses rather than runs where it cannot confine.

## Tests (acceptance)
- **NFR-004a / SC-012** provenance refusal: a `third_party`-provenance asset (derivation preserved, C-008) whose entrypoint would drop a sentinel side effect → after transition the sentinel is ABSENT.
- **NFR-004b** opt-in refusal: allowlisted asset, flag off → sentinel absent + TRUST_REFUSAL.
- **SC-007** containment: asset attempting an out-of-tree write → blocked by path-resolved confinement → FAULT_WARN; and a host whose capability probe reports it cannot confine fs/network → Path-B execution REFUSED (never run unconfined).
- **NFR-006** timeout: over-running asset terminated at the **process group** (no orphaned grandchild) → FAULT_WARN; an `setrlimit` cap breach → terminated.
- **FR-019 / SC-011** verdict channel: an asset printing a fake verdict to stdout yields FAULT_WARN — the verdict is read only from the dedicated size-capped channel.
- **C-007** the `tests/architectural/untrusted_path_audit/` harness is EXTENDED to include this code-exec sink (fails if a new unaudited exec path is added).
