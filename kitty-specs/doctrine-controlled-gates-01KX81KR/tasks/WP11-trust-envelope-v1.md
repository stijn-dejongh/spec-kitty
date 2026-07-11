---
work_package_id: WP11
title: Trust envelope v1 (refuse-unconfinable)
dependencies:
- WP10
requirement_refs:
- FR-007
- FR-015
- FR-019
tracker_refs:
- '2535'
planning_base_branch: design/doctrine-controlled-gates
merge_target_branch: design/doctrine-controlled-gates
branch_strategy: Planning artifacts for this mission were generated on design/doctrine-controlled-gates. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into design/doctrine-controlled-gates unless the human explicitly redirects the landing branch.
subtasks:
- T047
- T048
- T049
- T050
- T051
phase: Lane D - Path B
history:
- at: '2026-07-11T00:00:00Z'
  actor: claude
  action: created
agent_profile: python-pedro
authoritative_surface: src/doctrine/assets/
execution_mode: code_change
owned_files:
- src/doctrine/assets/trust.py
- src/doctrine/assets/runner.py
- .kittify/config.yaml
- tests/doctrine/assets/test_trust_envelope.py
create_intent:
- src/doctrine/assets/trust.py
- src/doctrine/assets/runner.py
- tests/doctrine/assets/test_trust_envelope.py
role: implementer
tags: []
task_type: implement
---

# WP11 — Trust envelope v1 (refuse-unconfinable) *(Lane D, Path B)*

## Objective

Ship the **refuse-unconfinable v1** containment envelope (RD-006) that confines
Path-B gate-asset execution and **refuses to run where it cannot confine** —
using stdlib-only, cheap-real primitives with **no new sandbox dependency**.
This is the security-load-bearing WP of the lane: every safeguard below is a
requirement clause, not an optimisation. When the envelope cannot guarantee a
clause, the outcome is **TRUST_REFUSAL — never unconfined execution**.

## Context

WP10 built the runner with the env / timeout / fs-confinement points **delegated
to an injected `TrustEnvelope`** and exercised with a permissive test double.
This WP replaces that double with the real policy object (`assets/trust.py`) and
wires it into the runner, so production Path-B execution is confined or refused.

The threat model is RCE-adjacent: doctrine/packs can supply executable code. The
envelope's job is to make sure that code (a) only runs when explicitly opted-in
and from allowlisted provenance, (b) cannot read ambient credentials, (c) cannot
escape the working tree on the filesystem, (d) cannot exhaust the host or orphan
grandchild processes, and (e) is **refused** rather than run on a host that
cannot actually confine fs/network. Deeper OS isolation (namespaces / landlock /
seccomp / a sandbox dependency) is explicitly deferred to **#2541** — do not add
one here.

The `run_scoped_tests_at_head` precedent (`pre_review_gate.py:358`) is the reuse
anchor for argv/no-shell/timeout — but its `env = dict(os.environ)` at `:374` is
**the exact anti-pattern this WP exists to reject**. Path-B constructs an
explicit env allowlist instead. The provenance tier this envelope keys its
allowlist on is produced by WP10's `source_kind` fix (C-008); without it the
allowlist would admit everything.

## Ordered steps

### T047 — `assets/trust.py`: env allowlist + interpreter allowlist / no-shell

1. New `src/doctrine/assets/trust.py`: a concrete `TrustEnvelope` implementing
   the WP09 Protocol. Pure `doctrine` layer (no `specify_cli` import).
2. **Environment allowlist — never `dict(os.environ)`.** Construct the child env
   *explicitly* from a small allowlist constant (e.g. `PATH`, `HOME`, `LANG`,
   `PWHEADLESS`, plus the controlled `TransitionContext` channel vars) — an
   explicit, deny-by-default `dict`, built key by key. Ambient credentials
   (`GITHUB_TOKEN`, cloud creds, `AWS_*`, etc.) MUST NOT reach the child. Add a
   guard/assertion that the constructed env is *not* derived from `os.environ`
   wholesale (construct-from-allowlist, then optionally copy only allowlisted
   keys' values).
3. **Interpreter allowlist / no shell / argv-vector.** Validate the asset's
   declared `interpreter` ∈ the allowlist (reuse/import the WP09 allowlist
   constant — single source). Invocation is argv-vector, `shell=False`, no
   string interpolation of any asset-controlled value.

### T048 — Process-group kill on timeout + `setrlimit` CPU/mem/output caps

1. **Process-group kill.** Launch the child in its **own process group**
   (`start_new_session=True` / `os.setsid` via `preexec_fn`), so a timeout can
   `os.killpg(pgid, SIGKILL)` the **whole group** — grandchildren included, no
   orphans. On `TimeoutExpired`, kill the group, reap, and return a fault
   (→ FAULT_WARN via WP04). Never leave a detached grandchild running.
2. **`setrlimit` caps applied in the child before exec** (in the `preexec_fn`,
   before the process group leader execs the interpreter): `RLIMIT_CPU`,
   `RLIMIT_AS` (address space / memory), `RLIMIT_FSIZE` (output/file-size). A
   breach terminates the child → fault → FAULT_WARN. Choose conservative defaults
   as module constants; the enforced wall-clock `timeout` (default mirrors the
   ~300 s baseline) is separate from `RLIMIT_CPU`.
3. Keep the `preexec_fn` POSIX-guarded; on a platform where these primitives are
   unavailable this feeds the capability probe (T049) → REFUSE, not a silent
   skip.

### T049 — Path-resolved (symlink-safe) fs write confinement + capability probe → REFUSE

1. **Path-resolved filesystem write confinement.** Writes are limited to a
   scratch/working-tree dir; enforcement is on the **symlink-resolved real path**
   (`Path.resolve(strict=False)` / `os.path.realpath`), rejecting any `..` or
   symlink escape — reuse the `resolve_relative_path_within_root` containment
   discipline. An out-of-tree write attempt is blocked → FAULT_WARN (SC-007). Do
   not confine via string-prefix on the un-resolved path (symlink bypass).
2. **Capability probe → refuse-if-unconfinable.** Before running, probe whether
   the host can actually confine filesystem + network for this execution. If it
   **cannot** (e.g. the process-group/rlimit/fs-confinement primitives or a
   required isolation capability are unavailable), the asset is **REFUSED**
   (TRUST_REFUSAL) and **never run unconfined**. No network-namespace dependency
   is added in v1; where true fs/network isolation is unavailable, refusal is the
   outcome — not degraded/unconfined execution.
3. **Dedicated size-capped verdict channel enforcement** (FR-019): the runner
   reads the `GateVerdict` only from WP10's dedicated channel, with the envelope
   enforcing the **size cap** and schema validation on read. Oversized / malformed
   / absent = fault → FAULT_WARN. stdout can never forge a verdict.

### T050 — Opt-in flag `review.allow_executable_gate_assets` (default off) + wire into runner

1. Add `review.allow_executable_gate_assets` to the `.kittify/config.yaml` schema
   surface, **default `false`**. Document it as the Path-B opt-in.
2. Wire the concrete `TrustEnvelope` into `src/doctrine/assets/runner.py`,
   replacing the WP10 injected double at the production call site. The runner now
   consults the envelope for: opt-in flag, provenance allowlist (keyed on WP10's
   derived tier), interpreter allowlist, env allowlist, timeout+pg-kill, rlimits,
   fs confinement, capability probe.
3. **Refusal ordering (all-or-refuse):** evaluate every trust clause up front;
   if *any* fails (flag off, non-allowlisted provenance, bad interpreter,
   unconfinable host), the runner returns **TRUST_REFUSAL and does not exec** —
   the child process is never spawned. Only when *all* clauses hold does exec
   happen inside the confinement.

### T051 — Red-first: flag off / non-allowlisted provenance → TRUST_REFUSAL, not executed

1. `tests/doctrine/assets/test_trust_envelope.py`, red-first (the concrete
   envelope + wiring don't exist yet).
2. **NFR-004b (opt-in refusal):** allowlisted-provenance asset whose entrypoint
   would drop a sentinel side effect, but `review.allow_executable_gate_assets`
   **off** → after the transition the sentinel is **absent**; outcome is
   TRUST_REFUSAL; the child was never spawned.
3. **NFR-004a (provenance refusal):** flag **on** but a `third_party`-provenance
   asset (produced via WP10's fix) with a sentinel entrypoint → sentinel
   **absent**; TRUST_REFUSAL. (SC-012's full genuinely-producible-tier assertion
   is exercised in WP12; this pins the envelope's decision.)
4. **Env isolation:** an asset entrypoint that tries to read `GITHUB_TOKEN` /
   an ambient credential env var sees it **absent** — the constructed env is the
   allowlist, not `os.environ`.
5. `ruff`/`mypy` clean on `trust.py` + `runner.py`; no new `# noqa`/`# type: ignore`.

## Acceptance

- **NFR-004a / NFR-004b**: a non-allowlisted-provenance asset, and any executable
  gate asset while the opt-in is off, are **never executed** — sentinel side
  effect absent, TRUST_REFUSAL surfaced, child never spawned (T051).
- **NFR-006 (verified fully in WP12, enforced here)**: timeout kills the whole
  **process group** (no orphaned grandchild); an `setrlimit` breach terminates
  the child; a host whose capability probe reports it cannot confine fs/network
  → execution **refused**, not run.
- **Env isolation**: the child env is an explicit allowlist; ambient credentials
  never reach the asset (never `dict(os.environ)`).
- **FR-019**: the verdict is read only from the dedicated size-capped
  schema-validated channel; stdout cannot forge a verdict.
- **RD-006 v1**: containment is stdlib-only; **no new sandbox dependency** added;
  deeper OS isolation left to #2541.
- `ruff`/`mypy` clean; every trust clause has a focused test.

## Safeguards (load-bearing — each maps to a requirement clause)

- **Env allowlist, never `dict(os.environ)`** (FR-007d / C-008). Build the child
  env key-by-key from an allowlist; assert it is not `os.environ`-derived
  wholesale. Ambient `GITHUB_TOKEN` / cloud creds must be absent in the child.
- **Process-group kill + `setrlimit`** (FR-015 / NFR-006). Own process group
  (`start_new_session`/`setsid`); timeout → `killpg` the whole group; `RLIMIT_CPU`
  /`RLIMIT_AS`/`RLIMIT_FSIZE` applied in `preexec_fn` before exec. No orphaned
  grandchildren.
- **Path-resolved (symlink-safe) fs confinement** (FR-015). Confine on the
  realpath, reject `..`/symlink escape; out-of-tree write → FAULT_WARN. Never
  string-prefix an un-resolved path.
- **Capability probe → REFUSE, never run unconfined** (FR-015 / SC-007). If the
  host can't confine fs/network, the asset is refused (TRUST_REFUSAL). Refusal is
  the *only* fallback — no degraded/unconfined path exists.
- **Dedicated size-capped verdict channel, not stdout** (FR-019). Verdict read +
  size-cap + schema-validate off the private channel; stdout ignored.
- **All-or-refuse ordering.** Evaluate every clause before spawning; any failure
  → TRUST_REFUSAL with **no child process spawned** — not "spawn then police".
- **NO new sandbox dependency.** stdlib primitives only; deeper OS isolation
  (namespaces/landlock/seccomp) is deferred to **#2541** — do not import or add
  one.
- **Fail-open, never fail-closed on infra.** Every refusal/fault is a
  non-blocking outcome (TRUST_REFUSAL / FAULT_WARN); no trust failure ever
  hard-blocks a transition (C-002). Only a valid `regression(blocking)` blocks —
  and that comes from the verdict, never from the envelope.
- **Pure doctrine layer** — `trust.py`/`runner.py` must not import `specify_cli`.

## References

- `src/doctrine/assets/runner.py` — WP10 runner with delegated envelope hooks
  (wire the concrete envelope here).
- `src/doctrine/assets/models.py` — WP09 `TrustEnvelope` Protocol + interpreter
  allowlist constant (single source; reuse, don't fork).
- `src/specify_cli/review/pre_review_gate.py:358` — `run_scoped_tests_at_head`
  (reuse argv/no-shell/timeout); `:374` — `env = dict(os.environ)` (the
  anti-pattern this WP rejects).
- `src/doctrine/drg/org_pack_loader.py:403` — the WP10 `source_kind` fix that
  makes the provenance tier this envelope allowlists on producible (C-008).
- data-model.md → `TrustEnvelope` (every field is a clause here) + `OperatorOutcome`
  (`TRUST_REFUSAL`/`FAULT_WARN`).
- contracts/gate-asset-entrypoint-and-trust.md → "Trust envelope (ALL must hold
  or … TRUST_REFUSAL)" clauses 1-8 (this WP implements 1-7; 8 is deferred).
- spec.md → FR-007, FR-015, FR-019; NFR-004a/b, NFR-006; RD-006; SC-006/007.
- research.md §4 — "real containment, not just an allowlist"; §3 — env anti-pattern.
