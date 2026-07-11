---
work_package_id: WP12
title: Trust/containment tests + audit-harness extension
dependencies:
- WP11
requirement_refs:
- C-007
- FR-015
- FR-019
- NFR-006
tracker_refs:
- '2535'
planning_base_branch: design/doctrine-controlled-gates
merge_target_branch: design/doctrine-controlled-gates
branch_strategy: Planning artifacts for this mission were generated on design/doctrine-controlled-gates. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into design/doctrine-controlled-gates unless the human explicitly redirects the landing branch.
subtasks:
- T052
- T053
- T054
- T055
phase: Lane D - Path B
history:
- at: '2026-07-11T00:00:00Z'
  actor: claude
  action: created
agent_profile: python-pedro
authoritative_surface: tests/
execution_mode: code_change
owned_files:
- tests/doctrine/assets/test_containment.py
- tests/doctrine/assets/test_verdict_channel.py
- tests/architectural/untrusted_path_audit/audit.py
- tests/architectural/untrusted_path_audit/inventory.md
- tests/architectural/untrusted_path_audit/audited-surfaces.md
create_intent:
- tests/doctrine/assets/test_containment.py
- tests/doctrine/assets/test_verdict_channel.py
role: implementer
tags: []
task_type: implement
---

# WP12 — Trust/containment tests + audit-harness extension *(Lane D, Path B, tail)*

## Objective

Prove the WP11 trust envelope actually contains, and extend the static
`untrusted_path_audit` harness to cover the new code-exec sink (C-007). Two
**distinct** obligations that this WP must keep distinct: **runtime containment
tests** (behavioral proof the envelope kills/blocks/refuses) and a **static
audit-harness extension** (a scanner that fails if a new *unaudited* exec path
appears). The audit harness is NOT a substitute for the runtime tests, and the
runtime tests are NOT a substitute for the harness — **both are required**.

This WP is test-authoring but is still an implementer role: the tests here are
the acceptance proof for the whole Lane-D containment story (NFR-006, SC-006/007/
011/012), and the audit-harness edit is production-config code.

## Context

WP11 shipped the envelope; WP10 made a `third_party` provenance tier producible.
This WP is where the security claims become *live evidence* rather than
"code looks fixed". Per the charter's live-evidence discipline, a containment
clause is not proven because the code appears to enforce it — it is proven by a
test that drives the real runner and observes the sentinel absent / the
grandchild reaped / the out-of-tree write blocked / the forged stdout verdict
rejected.

The existing `tests/architectural/untrusted_path_audit/` harness (`audit.py`)
AST-walks **`src/specify_cli`** for untrusted-segment → filesystem-sink flows and
fails closed against a curated `inventory.md` (drift-proof composite row
identity). The new Path-B **code-exec** sink lives under `src/doctrine/assets/`
(runner/entrypoint/trust) — a surface the harness does not currently scan. C-007
requires extending the harness so this exec sink is audited and a *new unaudited
exec path* reddens CI (no stale-green). This is a static scanner extension: it
does not run the asset; it inventories the sink.

## Ordered steps

### T052 — Containment tests: out-of-tree write blocked → FAULT_WARN; unconfinable host → refuse (SC-007)

1. New `tests/doctrine/assets/test_containment.py`. Drive the real WP11 runner +
   envelope (flag on, allowlisted provenance) with realistic gate-asset fixtures.
2. **Out-of-tree write (SC-007):** an asset entrypoint attempting a write to a
   path outside the scratch/working-tree dir — including via a `..` traversal and
   via a **symlink** pointing outside — is blocked by the path-resolved
   confinement; outcome is **FAULT_WARN**; the out-of-tree file is **absent**
   afterward. Cover both the plain `..` and the symlink-escape case (path-resolved
   confinement must catch both).
3. **Unconfinable host (SC-007):** simulate a host whose capability probe reports
   it cannot confine fs/network (inject/monkeypatch the probe to report
   unconfinable). Assert Path-B execution is **REFUSED** (TRUST_REFUSAL), the
   child is never spawned, and an egress-capable asset never runs unconfined.

### T053 — Timeout kills the process group (no orphaned grandchild); rlimit breach terminates (NFR-006)

1. In `test_containment.py` (or a sibling), **process-group kill:** an asset that
   spawns a **grandchild** (e.g. `subprocess`/fork) and then over-runs the
   timeout. Assert: the runner kills the whole process group; after the run,
   **no orphaned grandchild** survives (probe by pgid liveness / a sentinel the
   grandchild would write only if it outlived the kill). Outcome FAULT_WARN.
2. **`setrlimit` breach:** an asset that exceeds a resource cap
   (`RLIMIT_CPU` busy-loop, `RLIMIT_AS` allocation, or `RLIMIT_FSIZE` oversized
   write) is terminated by the cap → FAULT_WARN. One test per clause per NFR-006
   ("Verified by one test per clause").
3. Keep these tests hermetic and bounded (small caps / short timeouts) so they
   run fast and do not leak processes into the suite. Guard POSIX-only clauses
   with a skip on platforms lacking the primitive (and assert those platforms hit
   the T052 refuse path instead).

### T054 — Verdict-channel forgery test: fake stdout verdict → FAULT_WARN (FR-019 / SC-011)

1. New `tests/doctrine/assets/test_verdict_channel.py`. An asset that prints a
   **fake passing/blocking `GateVerdict` to stdout** but emits nothing (or garbage)
   on the dedicated channel → outcome **FAULT_WARN**; the forged verdict is NOT
   read; stdout cannot forge PASS or BLOCK (SC-011).
2. **Oversized / malformed / absent** on the dedicated channel each → FAULT_WARN
   (size cap + schema validation, FR-019). A well-formed verdict on the dedicated
   channel → read correctly (positive control).
3. Assert the read path is exclusively the dedicated channel — stdout is inert.

### T055 — Extend `untrusted_path_audit/` to cover the new code-exec sink (C-007)

1. Extend `tests/architectural/untrusted_path_audit/audit.py` so its AST walk
   **also covers `src/doctrine/assets/`** (today it walks only `src/specify_cli`).
   Add the new code-exec sink shape to the sink recognition: the `subprocess`
   exec of an asset-supplied `entrypoint`/`interpreter` (argv built from
   asset-controlled values) is an untrusted-input → **code-exec** sink, analogous
   to the existing FS sinks. Keep the drift-proof composite row identity
   (`rel_path, enclosing_qualname, token`).
2. Add the new sink(s) to `inventory.md` with an explicit human **disposition**
   citing the WP11 trust envelope (provenance allowlist + opt-in + interpreter
   allowlist/no-shell + env allowlist + pg-kill/rlimit + path-resolved fs
   confinement + capability-probe refusal) as the guarding seam. Update
   `audited-surfaces.md` to record `src/doctrine/assets/` as an audited surface.
3. Prove the tripwire **both directions**: the audit is GREEN with the code-exec
   sink documented, and RED if a new *unaudited* exec path is introduced
   (undercount) or a documented sink is deleted (overcount/ghost). Add a focused
   test (or extend `test_untrusted_path_containment.py`) that drives the extended
   audit over a fixture introducing an unaudited exec path and asserts it fails
   closed.
4. `ruff`/`mypy` clean on the audit module edit; no new suppressions.

## Acceptance

- **SC-007**: out-of-tree write (incl. symlink escape) blocked → FAULT_WARN,
  file absent; unconfinable host → TRUST_REFUSAL, never run unconfined (T052).
- **NFR-006**: timeout kills the process group with no orphaned grandchild; an
  `setrlimit` breach terminates the child — one test per clause (T053).
- **SC-011 / FR-019**: a fake stdout verdict yields FAULT_WARN; the verdict is
  read only from the dedicated size-capped schema-validated channel (T054).
- **SC-006 / SC-012** (envelope decisions from WP11, exercised end-to-end here):
  non-allowlisted / opt-in-off assets refused (sentinel absent); a genuine
  `third_party`-provenance asset (WP10-producible) refused by default.
- **C-007**: the `untrusted_path_audit` harness now audits the `src/doctrine/assets/`
  code-exec sink and fails closed if a new unaudited exec path appears (T055) —
  no stale-green.
- **Both obligations satisfied and kept distinct**: runtime containment tests AND
  the static audit-harness extension are present; neither is used as a stand-in
  for the other.

## Safeguards

- **The audit harness is a STATIC scanner — not a substitute for runtime
  containment tests.** T055 proves *a sink is audited*; T052-T054 prove *the
  envelope actually contains*. Do not let a green audit be cited as containment
  proof, and do not skip the audit extension because runtime tests pass.
- **Live evidence, not "looks fixed."** Every containment clause is proven by
  driving the real runner and observing the effect (sentinel absent, grandchild
  reaped, write blocked, forged verdict rejected) — not by asserting the code
  path exists.
- **Fail-open outcomes only.** Every containment/forgery/refusal case resolves to
  a non-blocking outcome (FAULT_WARN / TRUST_REFUSAL); none blocks the transition
  (C-002). A crashed/timed-out/refused asset is never read as `regression`.
- **Hermetic, process-leak-free tests.** Small rlimit caps / short timeouts;
  reap children; assert no orphaned grandchild survives. Serial-safe (these spawn
  real processes — do not rely on per-worker HOME isolation for process/pgid
  global state; mark for serial run if needed).
- **Realistic fixtures** — production-shaped asset manifests and provenance tiers,
  not placeholders, so the containment behavior is genuinely exercised.
- **No new sandbox dependency** is introduced by the tests either (RD-006).

## References

- `tests/architectural/untrusted_path_audit/audit.py` — AST walk (currently
  `src/specify_cli` only) + drift-proof composite row identity `(rel_path,
  enclosing_qualname, token)`; `check_undercount`/`check_overcount` tripwires
  (extend to `src/doctrine/assets/`).
- `tests/architectural/untrusted_path_audit/inventory.md`,
  `audited-surfaces.md`, `RULESET.md` — the curated dispositions + canonical
  seam table (add the code-exec sink + WP11 envelope disposition).
- `tests/architectural/test_untrusted_path_containment.py` — the pytest driver
  over the audit (extend for the code-exec tripwire).
- `src/doctrine/assets/runner.py` / `trust.py` (WP10/WP11) — the runner + envelope
  under test.
- data-model.md → `TrustEnvelope` (each clause = a test), `OperatorOutcome`
  (`FAULT_WARN`/`TRUST_REFUSAL`).
- contracts/gate-asset-entrypoint-and-trust.md → "Tests (acceptance)" — the
  authoritative NFR-004a/SC-012/SC-007/NFR-006/FR-019/SC-011/C-007 test list.
- spec.md → NFR-006, SC-006, SC-007, SC-011, SC-012; C-007.
