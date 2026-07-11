# Feature Specification: Doctrine-Controlled Transition Gates

**Mission**: doctrine-controlled-gates-01KX81KR
**Epic**: #2535 (under #2466 — Doctrine/Charter extensibility & pack ecosystem)
**Closes**: #2534 (fully) · **#2330** (partially — see SC-002/FR-009)
**ADR**: [docs/adr/3.x/2026-07-11-1-doctrine-controlled-transition-gates.md](../../docs/adr/3.x/2026-07-11-1-doctrine-controlled-transition-gates.md)

## Summary

Task-lifecycle transition checks ("gates" — e.g. the pre-review regression gate
that fires on `move-task --to for_review`) are today decided by hardcoded
per-lane logic in `specify_cli`, and the pre-review gate in particular is shaped
to spec-kitty's own repository (it imports a spec-kitty-only test module and
assumes a `src/specify_cli/` + pytest layout). In any consumer repository that
gate runs inert **and** leaks internal module names into the operator's face
(#2534, #2330).

This mission moves the **selection and supply** of transition gates into the
doctrine/charter layer, via **two coexisting mechanisms** (the operator's full
A+B scope):

- **Gate handlers (Path A)** — implementations **shipped inside spec-kitty**,
  selected by doctrine but running with **no opt-in and no doctrine-supplied
  code execution**. spec-kitty's own gates (including the migrated pre-review
  gate) are handlers, so they keep running with unchanged behavior.
- **Gate assets (Path B)** — gate logic **supplied by doctrine/packs as
  executable ASSET-kind helpers**, run only behind a strict trust envelope and a
  default-off opt-in. This lets a consumer (or org pack) ship its own gate.

A mission **step contract** declares which gate(s) fire on which transition; the
**charter** subsystem's activation decides which declared gates are active in a
given repository. A repository therefore runs exactly the gates its active
doctrine declares — a non-spec-kitty repo with nothing declared runs none and
sees a calm, non-blocking **notice**, never a leaked internal module. The whole
system is **fail-open**: no gate-infrastructure fault ever blocks a transition.

## User Scenarios & Testing

### Primary scenario (consumer repo, nothing declared)
A consumer-repo operator runs `spec-kitty agent tasks move-task WP01 --to for_review`.
No gate is charter-active in their repo. The transition proceeds and surfaces a
single clearly-labelled non-blocking **notice**: automated pre-review regression
scoping is not configured for this repository. No `src/specify_cli/` path, no
`tests.architectural._gate_coverage`, no spec-kitty-internal name appears. (#2534 resolved.)

### Consumer ships its own gate (Path B, non-pytest repo)
A consumer maintainer authors, in their org pack, an executable **gate asset**
plus a `ScopeSource`, binds it to the `for_review` transition in a step
contract, charter-activates it, and turns on `review.allow_executable_gate_assets`.
Now `move-task --to for_review` runs *their* gate behind the trust envelope and
returns a real verdict — with no change to any `specify_cli` code.

### spec-kitty's own repo (Path A handler, migration parity)
In the spec-kitty source repo the pre-review regression gate is now a built-in
**handler** bound through a built-in step contract. It runs with **no opt-in**
and produces the **same** verdict as the prior hardcoded gate on the same change
set — no observable behavior change for spec-kitty itself.

### Exception path (gate active but unrunnable)
A gate is charter-active but cannot run — a Path-B asset fails to resolve, the
runner errors/crashes/times out (non-zero exit or no verdict emitted), or a
test-run handler has no configured test command. The transition **still
proceeds**, emitting a calm non-blocking **fault-warn** that names the
misconfiguration in operator terms. A crashed/timed-out gate is **never** read
as a regression.

### Trust path (untrusted / opt-out)
A gate asset whose derived provenance is outside the allowlist (e.g. an
unverified third-party pack), or any executable gate asset while
`review.allow_executable_gate_assets` is off, is **never executed** — a
**trust-refusal** notice is shown and the transition proceeds fail-open.

## Domain Language

| Term | Meaning | Avoid |
|------|---------|-------|
| **Gate** | A check bound to a task-lifecycle transition. | "hook" |
| **Gate binding** | The declarative `transition → gate` association carried on a mission step contract. | "wiring" |
| **Gate handler (Path A)** | A gate implementation shipped **inside spec-kitty**, selected by doctrine, run with no opt-in and no doctrine code execution. | "plugin" |
| **Gate asset (Path B)** | A doctrine/pack-**supplied executable** ASSET-kind helper; runs only behind the trust envelope + opt-in. | "script" (unqualified) |
| **ScopeSource** | A doctrine-declared strategy that derives the affected verification scope for a change (portable; not intrinsically pytest-bound). | "filter group" |
| **Active doctrine** | The set the **charter** subsystem has activated for the repository — the sole gate-selection authority. | "installed doctrine" |
| **Gate verdict** | The structured result a gate emits: `status ∈ {no_new_failures, regression, no_coverage, error}` + `blocking: bool` + operator message. | — |
| **Operator outcome** | What the operator sees/experiences: BLOCK / FAULT-WARN / CALM-NOTICE / TRUST-REFUSAL / PASS (see FR-014). | conflating "notice" & "warn" |
| **Fail-open** | Any gate-infrastructure fault degrades to a non-blocking outcome; only a real regression may block. | "fail-safe" |
| **Trust envelope** | Provenance allowlist + opt-in + interpreter allowlist/no-shell + timeout **+ filesystem/network/resource containment** confining gate-asset execution. | "sandbox" (alone) |

## Functional Requirements

| ID | Requirement | Status |
|----|-------------|--------|
| FR-001 | A mission **step contract** can declaratively bind one or more gates to a named transition (e.g. `for_review`). The binding is data on the existing activatable step-contract surface — not a hardcoded per-lane branch. | Proposed |
| FR-002 | Gate **selection** is a single SSOT seam — `resolve_gates(mission, transition, activation)` with a **lane↔action adapter** — the one place that reads step-contract bindings + applies charter activation. Both consumers (the `move-task` pre-review hook and the composed-action guard `_check_composed_action_guard`) obtain their gate set from it (no parallel resolver). **Reduction stays per gate-class**: test/verdict gates use the FR-014 fail-open mapping; the **artifact-presence** composed-action guard keeps its existing **fail-closed** semantics (it is NOT routed through FR-014). This mission migrates the pre-review **test-gate** as the exemplar; the artifact guard adopts shared *selection* only. | Proposed |
| FR-003 | The **charter** subsystem is the single selection authority: only gates whose declaring doctrine is charter-active fire. A repository with no active gate doctrine runs no gate. Selection reuses the existing activation/DRG machinery (`filter_graph_by_activation`) — no parallel gate-enablement registry. | Proposed |
| FR-004 | A gate's logic is supplied by **one of two mechanisms** behind a common verdict interface: (a) a **gate handler** shipped inside spec-kitty (Path A) — always available when its doctrine is active, no opt-in, no doctrine-supplied code executed; or (b) an **executable gate asset** (Path B) supplied by doctrine/packs. The binding names which. | Proposed |
| FR-005 | Build the ASSET **execution substrate** that does not exist today (Path B): an asset repository, a URN→path resolver, a code-asset **entrypoint contract**, and a **runner** that returns a structured verdict. Non-gate assets remain inert by default — code execution is a new, distinct capability keyed on the gate-asset shape, not a generalization of asset loading (preserves C-003). | Proposed |
| FR-006 | Gate activation is decided on the **owning step-contract node** (the activatable unit) — not the asset/handler URN, which is not activation-filterable today (`asset`/`gate-handler` are absent from the DRG singular↔plural kind maps, so `filter_graph_by_activation` would default-allow them). A gate is active iff its declaring step contract is charter-active. | Proposed |
| FR-007 | Executing a **Path-B gate asset** is confined to a **trust envelope**: (a) provenance allowlist — built-in and org-pack only by default; provenance **derived from pack-load metadata (the loader must stop discarding `source_kind`) so a genuine `third_party` tier is producible and refusable** — never self-declared; (b) opt-in flag `review.allow_executable_gate_assets` (default **off**); (c) interpreter allowlist, no shell interpolation, argv-vector only; (d) an **environment allowlist** — never `dict(os.environ)` inheritance, so no ambient credentials (`GITHUB_TOKEN`, cloud creds) reach the asset; (e) an enforced timeout. A gate asset failing any check is **not executed** (TRUST-REFUSAL). | Proposed |
| FR-008 | When no gate/ScopeSource is charter-active for a transition, the transition emits a **calm, non-blocking CALM-NOTICE** ("automated pre-review scope not configured for this repository") naming **no** spec-kitty-internal module or layout. | Proposed |
| FR-009 | Scope derivation is a **doctrine-declared `ScopeSource` strategy**, not a hardcoded `src/specify_cli/` / `tests.architectural._gate_coverage` assumption in the *decision path*. spec-kitty's filter-group/census model becomes a built-in `ScopeSource` used only when spec-kitty's own doctrine is active; a repo with a different layout supplies its own `ScopeSource` or gets the FR-008 notice. | Proposed |
| FR-010 | **Fail-open**: every unrunnable/misconfigured/unresolvable gate condition — asset resolve failure, runner error/crash, non-zero exit, timeout, **malformed or absent verdict**, missing test command, inactive/absent doctrine, trust refusal — degrades to a non-blocking outcome (FAULT-WARN or TRUST-REFUSAL per FR-014). | Proposed |
| FR-011 | **Strangler migration**: the existing pre-review regression gate is re-expressed as the first built-in **handler** (Path A) bound through a built-in step contract, and the hardcoded `pre_review_gate` invocation is inverted to resolve through the FR-002 seam. The extracted verdict tail (`evaluate_with_scope`) is reused. Because it is a Path-A handler, it runs on spec-kitty's own repo **with no opt-in** (preserving SC-003 parity). | Proposed |
| FR-012 | The consumer-facing gate path **must not import** `tests.architectural._gate_coverage` nor assume `_SRC_PACKAGE_PREFIX = "src/specify_cli/"`; those spec-kitty-shaped authorities move inside the built-in `ScopeSource`, reached only when spec-kitty's own doctrine is active. | Proposed |
| FR-013 | **Only** the pre-review regression gate is migrated in this mission (the exemplar). The other transition checks stay as-is until incremental follow-on; the substrate must support them but this mission does not rewire them. This boundary is explicit, not accidental. | Proposed |
| FR-014 | Define a **canonical verdict→operator-outcome mapping** for **test/verdict gates**: **BLOCK** only when a gate emits a valid `regression` verdict with `blocking=true`; **FAULT-WARN** for any FR-010 fault; **CALM-NOTICE** when nothing is declared/active (FR-008); **TRUST-REFUSAL** when FR-007/FR-015 refuses execution; **PASS** on a valid non-regression verdict. No other input may block a transition. (Artifact-presence guards keep their own fail-closed reduction per FR-002 — they are not governed by this mapping.) | Proposed |
| FR-015 | Path-B execution ships **refuse-unconfinable v1** containment (RD-006): a **process-group kill** on timeout (grandchildren included) + **`setrlimit`** CPU/memory/output-size caps + **path-resolved (symlink-safe) filesystem write confinement** to a scratch/working-tree dir. A **capability probe** determines whether the host can actually confine filesystem + network; if it cannot, the asset is **refused** (TRUST-REFUSAL), **never run unconfined**. Deeper OS-level sandboxing (namespaces/landlock/seccomp, a sandbox dependency) is explicitly deferred (Out of Scope). | Proposed |
| FR-016 | The binding field is a **versioned schema evolution** of the step-contract / `MissionStep` models (they are `extra="forbid"`): existing built-in step contracts without a binding continue to load, and a migration adds the binding to built-in contracts. Both old-load and new-field-validation are covered by tests. | Proposed |
| FR-017 | Existing pre-review config (`review.fail_on_pre_review_regression`, `review.test_command`) is preserved as the built-in pre-review handler's configuration — same semantics, same defaults; no silent behavior change to operators relying on them. | Proposed |
| FR-018 | Operators can observe, for a given transition, **which gates are active, from which declaring doctrine, and why one did or did not run** (active / inactive / refused / faulted), without reading `specify_cli` source. | Proposed |
| FR-019 | A Path-B asset emits its `GateVerdict` on a **dedicated, size-capped, schema-validated channel** (not shared stdout). Malformed / oversized / absent output is a fault (FAULT-WARN); stray stdout cannot forge a passing or blocking verdict. | Proposed |

## Non-Functional Requirements

| ID | Requirement | Threshold / Measure | Status |
|----|-------------|---------------------|--------|
| NFR-001 | Behavior parity for spec-kitty's own repo: the migrated built-in **handler** yields the same verdict as the prior hardcoded gate on the same inputs, running with no opt-in. | 100% of existing `pre_review_gate` verdict tests pass (with only binding-indirection edits); zero new failures attributable to the migration. | Proposed |
| NFR-002 | Consumer-repo portability: no transition in a repo lacking spec-kitty's test layout surfaces any spec-kitty-internal module/path. | A consumer-shaped fixture (no `tests/architectural/_gate_coverage.py`, non-pytest) crossing `for_review` produces the FR-008 CALM-NOTICE; output contains none of `tests.architectural._gate_coverage`, `src/specify_cli/`. | Proposed |
| NFR-003 | Fail-open holds for every fault class in FR-010 and every mechanism. | Fault-injection tests (missing asset, runner crash, non-zero exit, timeout, malformed verdict, absent verdict, no test command, inactive doctrine) each yield a non-blocking outcome per FR-014; zero block the transition. | Proposed |
| NFR-004a | Provenance refusal: a gate asset whose derived provenance is outside the allowlist is never executed. | A test binds a non-allowlisted-provenance asset whose entrypoint would create a sentinel side effect; after the transition the sentinel is absent. | Proposed |
| NFR-004b | Opt-in refusal: with `review.allow_executable_gate_assets` off, no executable gate asset runs. | Same sentinel probe with an allowlisted asset but flag off; sentinel absent; TRUST-REFUSAL surfaced. | Proposed |
| NFR-005 | Doctrine-only extensibility: adding/removing a gate for a transition changes no `specify_cli` control flow. | A test adds a gate to a transition via doctrine artifacts only (step-contract binding + handler/asset) and observes it fire through the FR-002 shared seam, with no edit to `specify_cli` gate-decision code. | Proposed |
| NFR-006 | Bounded, contained execution (Path B, refuse-unconfinable v1). | A run exceeding the timeout is killed at the **process group** (no orphaned grandchild); a run exceeding an `setrlimit` cap is terminated; on a host whose **capability probe** reports it cannot confine fs/network, execution is **refused** (not run). Verified by one test per clause. | Proposed |

## Constraints

| ID | Constraint | Status |
|----|------------|--------|
| C-001 | The **charter** subsystem is the single gate-selection authority (operator 2026-07-11). No parallel enablement registry; reuse `filter_graph_by_activation` unchanged. | Active |
| C-002 | Fail-open is load-bearing: never introduce a "cannot move task because doctrine is misconfigured" hard block for gate-infrastructure faults. Only a valid emitted `regression(blocking)` may block. | Active |
| C-003 | Executable **assets** run only behind the FR-007/FR-015 trust envelope; the loose-contract ASSET kind's inert-by-default posture is preserved for all non-gate assets. Code execution is opt-in, keyed on the gate-asset shape — not a generalization of asset loading. | Active |
| C-004 | Unification not parity: the hardcoded spec-kitty-shaped `pre_review_gate` decision path is **removed** (folded into a built-in `ScopeSource`/handler), not preserved as a compatibility fallback. | Active |
| C-005 | Reuse existing substrate: the activation/DRG machinery and the extracted `evaluate_with_scope` verdict tail. The gate-decision **binding + shared resolver seam** is the new surface; no parallel read resolver. | Active |
| C-006 | The binding field lands on `extra="forbid"` models → versioned schema evolution + built-in-contract migration (FR-016), not a silent field add. Migration-first; the coupled charter spine (step_contracts→executor→drg→pack_validator→merge) is sequenced in one lane, not parallelized. | Active |
| C-007 | The new executable-asset runner is an untrusted-input sink: the existing `tests/architectural/untrusted_path_audit/` harness must be extended to cover it (no stale-green). NOTE: reuse the `run_scoped_tests_at_head` **argv/no-shell/timeout** precedent only — that function does **`env = dict(os.environ)` (full inheritance)**, which Path-B must NOT copy (see C-008). | Active |
| C-008 | Path-B execution uses an **environment allowlist** (never `dict(os.environ)`), and the pack loader **must stop overwriting `source_kind`** so the provenance tier (built_in / org_pack / third_party) is derivable from preserved pack-load metadata. Without both, FR-007's env isolation and provenance refusal (NFR-004a) are untestable. | Active |

## Key Entities

- **Gate binding** — declarative `transition → gate` association on a mission step contract; the unit charter activation selects; names handler-vs-asset.
- **Gate handler (Path A)** — spec-kitty-shipped gate implementation; no opt-in, no doctrine code.
- **Gate asset (Path B)** — doctrine-supplied executable helper; runs only behind the trust envelope.
- **ScopeSource** — doctrine-declared scope-derivation strategy; spec-kitty's filter-group/census model is one built-in implementation.
- **Gate verdict** — `{status, blocking, message}`; the FR-014 mapping turns verdicts + faults into operator outcomes.
- **Trust envelope** — provenance allowlist (derived) + opt-in + interpreter allowlist/no-shell + timeout + FR-015 containment.
- **Charter activation** — the selection authority that turns declared gates into active gates.

## Success Criteria

| ID | Criterion |
|----|-----------|
| SC-001 | A consumer repo (no spec-kitty test layout) crossing `move-task --to for_review` sees a calm CALM-NOTICE and **zero** occurrences of `tests.architectural._gate_coverage` or `src/specify_cli/` in the output. (#2534 fully closed) |
| SC-002 | A non-pytest consumer repo declares a **gate + ScopeSource** in its doctrine, activates it (+opt-in for a Path-B asset), and it runs on `for_review` with a real verdict — with **no** change to `specify_cli`. This removes the hardcoded pytest assumption from the *decision/selection* path; the built-in test-run ScopeSource itself stays pytest-shaped but is now doctrine-selected (so #2330 is closed for selection, not for the built-in runner's internals). |
| SC-003 | In spec-kitty's own repo the migrated built-in **handler** produces the **identical** pre-review verdict to the prior hardcoded gate on the same change set, running with no opt-in. |
| SC-004 | Adding a new gate to a transition requires **only** doctrine edits (binding + handler/asset); no `specify_cli` gate-decision code changes (via the FR-002 shared seam). |
| SC-005 | **Every** injected fault in FR-010 yields the correct non-blocking outcome per the FR-014 table; none blocks the transition; a crashed/timed-out gate is never read as `regression`. |
| SC-006 | A gate asset from non-allowlisted (derived) provenance, or any executable gate asset while the opt-in is off, is **refused execution** (sentinel side effect absent) and the transition proceeds fail-open. |
| SC-007 | A Path-B gate asset attempting an out-of-tree write is blocked by path-resolved confinement → FAULT-WARN; and on a host whose capability probe reports it cannot confine fs/network, Path-B execution is **refused** (TRUST-REFUSAL) — an egress-capable asset never runs unconfined. |
| SC-008 | An operator can query which gates are active for `for_review`, their declaring doctrine, and why each did/didn't run (FR-018), without reading source. |
| SC-009 | A built-in step contract authored before this mission (no binding field) still loads, and the migration adds the binding; both are covered by tests (FR-016). |
| SC-010 | The composed-action **artifact-presence** guard's fail-closed hard-blocks (e.g. missing spec/plan/tasks) are **preserved** after it adopts shared selection — a missing-artifact case still blocks, not downgraded to a warn. |
| SC-011 | A Path-B asset cannot forge a passing or blocking verdict via stray stdout — the verdict is read only from the dedicated size-capped schema-validated channel (FR-019); an asset that prints a fake verdict to stdout yields FAULT-WARN. |
| SC-012 | A gate asset resolved through a `third_party`-provenance pack (derivation preserved) is refused execution by default (NFR-004a is exercised against a genuinely producible tier). |

## Resolved Decisions

| ID | Decision | Source |
|----|----------|--------|
| RD-001 | Gates bind via **activatable step contracts** (reuse charter activation), not a new first-class `gate` DRG kind. | operator 2026-07-11 |
| RD-002 | "Active doctrine" = the **charter-activated** set; the charter subsystem is the selection authority. | operator 2026-07-11 |
| RD-003 | Portable default when nothing is declared = a **calm non-blocking CALM-NOTICE**, not a heuristic scope and not a hard opt-in error. | operator 2026-07-11 |
| RD-004 | An unrunnable/misconfigured gate is a **fail-open non-blocking outcome**. | operator 2026-07-11 |
| RD-005 | **Full scope A+B**: BOTH mechanisms coexist — Path-A handlers (spec-kitty-shipped, no opt-in) AND Path-B executable assets (doctrine-supplied, opt-in + trust envelope). "A+B" does not mean "everything is B." | operator 2026-07-11 |
| RD-006 | Path-B containment = **refuse-unconfinable v1**: cheap-real primitives (env allowlist, process-group kill + `setrlimit`, dedicated size-capped verdict channel, derived provenance) and **refuse** where fs/network can't be confined. **No new sandbox dependency**; deeper OS sandbox (namespaces/landlock/seccomp) deferred. | operator 2026-07-11 |

## Assumptions

- The activation machinery (`filter_graph_by_activation`) and the extracted verdict tail (`evaluate_with_scope`) are reused rather than reinvented.
- Provenance tiers (built-in / org-pack / third-party) are derivable from existing pack-load provenance; cryptographic signature verification is **not** in scope (seeded to #2536).
- FR-015 containment uses host-available OS primitives; where a primitive is unavailable, execution is refused (never run unconfined) — the depth of containment vs. its own follow-up slice is a plan-time sizing question.

## Out of Scope

- **Pack-activation warning** when a pack ships executable code assets — tracked as **#2536**.
- **Trust tiers / `verified` status / SK-accredited certified-pack distribution** and cryptographic provenance — 3.3.x vision, seeded by #2536.
- Migrating the **other** transition gates — this mission delivers the substrate + migrates the pre-review regression gate as the exemplar (FR-013); the rest is incremental follow-on.
- Splitting the `tasks_move_task.py` / `runtime_bridge.py` god-modules beyond the pre-review-hook extraction this mission needs — broader `runtime_bridge` degod is **#2531** (concurrent; **coordinate** to avoid double-editing the F(48) `_check_composed_action_guard`). (#2116 is closed — superseded by #2531.)
- **Deeper OS-level Path-B sandboxing** (namespaces / landlock / seccomp / a sandbox system dependency) — v1 ships refuse-unconfinable containment (RD-006); OS-sandbox depth and per-pack/per-gate opt-in granularity are follow-ups (seeded to #2536).
- Any change to the FSM entry-guards in `status/wp_state.py` (already repo-agnostic).
