---
title: 'ADR: Doctrine-Controlled Transition Gates — Declarative Bindings Now, Executable ASSET Helpers as an Opt-In Later Tier'
status: Proposed
date: '2026-07-11'
---

## Context and Problem Statement

Every check that fires on a mission task-lifecycle transition is **hardcoded in
`specify_cli` Python**, keyed on the `Lane.*` enum by literal `if target_lane ==
Lane.X` branches. There are roughly **35 such transition checks** across the
command layer (`tasks_move_task.py`, `implement.py`, `accept.py`,
`policy/merge_gates.py`) and **no data-driven registry anywhere maps a transition
→ the set of checks that should run on it**. Adding a check today means editing
`specify_cli` and wiring a new `if target_lane == …` branch; a consumer repo
inherits spec-kitty's exact gate set whether or not it fits.

Two tiers exist. The **FSM entry-guards** (`status/wp_state.py`) are structural,
per-lane, and repo-agnostic — clean invariants worth keeping. The **command-layer
pre-gates** are the problem surface: imperative `if`-cascades gathered before the
FSM emit, several of which embed spec-kitty-repo-shaped assumptions
(`src/specify_cli/` prefix, a `tests/architectural/_gate_coverage` module, a
pytest/JUnit layout, `.kittify/config.yaml` keys).

The sharpest edge is the **pre-review regression gate** (issue #2534). It is
doubly bound to spec-kitty's own repository shape, and that binding is exactly
what leaks into consumers:

- The engine imports a **repo-internal, un-packaged test module** as its scope
  authority: `review/pre_review_gate.py:100` sets
  `_GATE_COVERAGE_MODULE_NAME = "tests.architectural._gate_coverage"`;
  `_load_gate_coverage_module` (`pre_review_gate.py:131-159`) does
  `importlib.import_module(...)` under `repo_root` and, at `:153-158`, **refuses
  any module resolving outside `repo_root`** (`GateAuthoritiesUnavailable`). The
  `tests/` tree is excluded from the wheel/sdist, so a consumer never has this
  module.
- The scope model itself encodes spec-kitty's CI topology, not the consumer's:
  hardcoded `_SRC_PACKAGE_PREFIX = "src/specify_cli/"` (`pre_review_gate.py:98`),
  a `_WHOLE_SRC_TREE_GLOB`, dorny filter-groups parsed from named GitHub
  workflow YAMLs, and a frozen `_COMPOSITE_ROUTING` table of spec-kitty directory
  names (`tests/architectural/_gate_coverage.py:72-89,792-860`).
- **Net effect in any non-spec-kitty repo:** every `move-task --to for_review`
  hits `GateAuthoritiesUnavailable` → `_mt_empty_scope_verdict("gate authorities
  unavailable…")` (`tasks_move_task.py:905-909`) → a silent `NO_COVERAGE` warn.
  The gate is **inert for every consumer** while still dragging spec-kitty's
  internal assumptions into a surface deployed to those consumers.

Issue **#2330** is the same coupling one layer down: `run_scoped_tests_at_head`
(`pre_review_gate.py:358-423`) hardcodes the runner as `[sys.executable, "-m",
"pytest", *targets, "--junitxml=…", "-q"]` and parses JUnit XML — baking in that
the project is Python, the runner is pytest, tests are path-addressable, and the
output is JUnit-shaped. A JS/Go/Rust consumer cannot use the gate at all.

Two facts make this tractable rather than a rewrite:

1. **The gate is invoked from exactly one additive seam.**
   `_mt_run_pre_review_gate` (`tasks_move_task.py:996`) fires after all
   pre-existing guards clear, on `for_review` moves only — its binding to that
   lane is a literal early return, `if st.target_lane != Lane.FOR_REVIEW: return`
   (`:1012`), not a lookup. Its warn/block/`--force`/`policy_metadata` policy
   tail is already extracted into a shared, tested body
   (`pre_review_gate.evaluate_with_scope`, `:451-511`). Only *scope + which-gate-
   fires* is spec-kitty-shaped; the verdict plumbing is already clean.

2. **Doctrine already has a declaration surface and an activation selector — they
   are just not wired to gates.** Mission **step contracts** are machine-loaded,
   schema-validated, and DRG-resolved (`MissionStepContractRepository.get_by_action`,
   `step_contracts.py:159-170`), and the transition itself literally lives there
   (`implement.step-contract.yaml` declares a `status_transition` step whose
   command is `move-task --to for_review`). But `StepContractExecutor` is *"a
   composer, not a command runner"* (`executor.py:2-4`) — declared commands are
   rendered as LLM text with an explicit *"declared only; the host/operator owns
   execution"* disclaimer (`:369-370`) and **never executed**. The real gates are
   a separate hardcoded system that never reads the contract. Likewise the
   post-action guard `_check_composed_action_guard` (`runtime_bridge.py:1515`) is
   a hardcoded `if/elif` chain on `(mission, action)`, not contract-driven.
   Meanwhile the activation machinery that already gates mission-type → step-
   contract selection (`filter_graph_by_activation`, `charter/drg.py:293-334`) is
   a ready-made "active doctrine selects which artifact applies" mechanism.

The ASSET kind is *named* as if it could carry executable helpers, but is **inert
by construction**: an asset is a validated sidecar reference
(`AssetManifest{id, mime, path}`) that mints an **identity-only** DRG node — the
extractor discards `path`/`mime` — with **no loader, no URN→path resolver, and no
invocation path**, and assets are **non-activatable** by design
(`_NON_AUGMENTATION_ELIGIBLE_KINDS = {TEMPLATE, ASSET}`, `artifact_kinds.py:178-180`,
which also removes them from `CHARTER_KIND_TOKENS`). Using assets as executable
gate helpers is a **new subsystem**, not a wiring exercise, and it crosses the
code-execution trust boundary the loose contract was written to stay behind.

**Framed as an architecture problem (Directive-043, close defect classes by
construction):** the fix is not "make `_gate_coverage` importable in consumers."
It is to **invert control so a repo's active doctrine declares its own gates and
its own scope source.** Then a non-spec-kitty repo gets exactly the gates its
doctrine declares — spec-kitty's census gate simply is not in its active set, so
#2534/#2330 cannot recur.

## Decision Drivers

- **Close the defect class by construction (D-043).** A gate substrate that
  requires "remember to keep `_gate_coverage` out of consumers" is structurally
  incomplete. The gate set a repo runs must be a function of that repo's active
  doctrine, not of spec-kitty's hardcoded Python.
- **Single canonical authority (D-044).** "Which checks fire on transition Y"
  must live in one declared place (the step contract, activation-filtered),
  not be smeared across early-returns, per-guard lane re-tests, and merge-gate
  `if policy.require_X` branches.
- **Ride the substrate that already exists, don't invent a fourth.** Config-key
  activation → `PackContext` → `ActivationDoctrineService` →
  `filter_graph_by_activation` is the tested precedent for "active doctrine
  selects which contract applies." A doctrine-controlled gate should be selected
  by exactly this machinery.
- **Preserve the fail-open invariant.** Every degradation today is a warn, never
  a block (`GateAuthoritiesUnavailable`, unresolved workspace, malformed JUnit
  all fold to `NO_COVERAGE`). The gate closes a defect class; it must not *open*
  a new "cannot move task because doctrine is misconfigured" class.
- **Keep the trust model a first-class pillar, not an afterthought.** The moment
  doctrine can *supply* gate code (Path B), we have an RCE-equivalent surface.
  The trust contract must be designed into the schema up front, even if Path B
  ships later.
- **Align with the infra-logic-separation epic (#2173).** The hook must stay in
  move-task (that is where transitions execute and `policy_metadata` is written),
  but doctrine resolution + gate dispatch should be an injected port so move-task
  stays a thin, testable orchestrator.

## Considered Options

1. **Keep everything hardcoded** (status quo) — extend the `if target_lane == …`
   cascades in `specify_cli` for each new gate.
2. **Tactical message fix** (the cancelled option) — make the pre-review gate's
   "gate authorities unavailable" path clearer / gate the `_gate_coverage`
   import so it does not appear to run in consumers, without changing where the
   gate set is decided.
3. **Path A only — declarative bindings + shipped handler registry**, no
   executable-asset tier, ever.
4. **Path B only — ASSET-as-executable** from the start: doctrine ships the gate
   script, runtime resolves + runs it.
5. **Phased hybrid — Path A now, Path B as an explicit opt-in later tier, with a
   mandatory trust model authored up front** — **chosen**.

## Decision Outcome

**Chosen option:** "Phased hybrid (A now, B as an opt-in later tier)" (Option 5).

Make transition pre-gate checks **doctrine-controlled and configured** instead of
hardcoded in `specify_cli`, in two paths delivered in sequence, behind one
schema authored to support both.

### Decisions recorded

- **A — Declarative bindings (the spine, delivered first).** Mission **step
  contracts** declare which gate(s) fire on which transition; the repo's **active
  doctrine** (charter activation via `filter_graph_by_activation`) selects the
  gate set. The load-bearing change is **rewiring the consumers**: the move-task
  pre-review hook (`tasks_move_task.py:996`) and the post-action guard
  (`_check_composed_action_guard`, `runtime_bridge.py:1515`) stop deciding by
  `if target_lane == X` / `if (mission, action) == …` and instead consult
  `MissionStepContractRepository.get_by_action(mission, action)` for the declared
  gate bindings. Gate logic **ships in spec-kitty as named handlers behind a
  `GateHandler` port + registry**; doctrine *selects and parameterizes*, it does
  not *supply code*. The existing `evaluate_pre_review_gate` becomes the first
  registered handler. Scope stops importing `tests.architectural._gate_coverage`
  and is chosen through a `ScopeSource` strategy (explicit-list / changed-dir-
  glob / "run the configured `review.test_command` whole"); the census/dorny
  strategy becomes one pluggable option that spec-kitty ships for *itself*, never
  a default others inherit.

- **B — Executable ASSET-kind helpers (greenfield, delivered as an opt-in later
  tier).** A gate helper *is* an ASSET blob (a script) referenced from an
  activatable step contract. This requires a **new subsystem**: an asset
  repository + a URN→path resolver (today the manifest `path` is validated then
  discarded), a code-asset **entrypoint contract** (argv/stdin = changed-files +
  baseline; stdout = schema-validated verdict JSON; declared interpreter +
  timeout), a **sandboxed runner**, and asset **activation** (assets are
  non-activatable today). B is designed as an *additive `GateHandler` kind*
  (`asset-backed`), so the Path-A registry and the binding schema accommodate it
  without re-opening either.

- **Mandatory trust model (a first-class pillar because doctrine-supplied code now
  executes).** Every executable-asset gate is subject to, at minimum:
  - **Provenance allowlist** — only *built-in* and *governed org-pack* assets may
    be executable; **never** a project-local or mission-authored asset by
    default.
  - **Interpreter allowlist / no shell** — the execution contract names an
    interpreter from an allowlist and passes an **argv vector**; never
    `shell=True`, never a raw command string.
  - **Explicit opt-in flag** — `review.allow_executable_gate_assets: true` in
    config, **off by default**. A repo that never opts in can never be made to
    run a doctrine script.
  - **Bounded execution** — timeout + env scrub, mirroring the existing
    subprocess-timeout discipline in `run_scoped_tests_at_head`.
  - **Fail-OPEN, structured-verdict-or-warn** — a malformed verdict, a resolution
    failure, or a missing runner degrades to a `NO_COVERAGE` warn and the
    transition proceeds; a doctrine/asset misconfiguration must **never** harden
    into a block.

- **Consequence by construction:** consumer repos receive **only the gates their
  active doctrine declares**. Spec-kitty's census gate is a spec-kitty-repo-only
  strategy, not a shipped default, so **#2534 (the `tests.architectural._gate_coverage`
  leak) and #2330 (the pytest-layout assumption) are closed by construction**,
  not by a discipline reminder.

### Corollaries (scope boundaries)

- **FSM entry-guards stay put.** The `status/wp_state.py` guards (A1–A12 in the
  inventory) are already clean, repo-agnostic invariants. This decision does
  **not** move them into doctrine; it targets the command-layer pre-gates only.
  They may later be *promoted* to doctrine as declared invariants, but that is
  out of scope here.
- **The hook stays in move-task; the authority is injected.** Transitions and
  `policy_metadata` writes remain in `tasks_move_task.py`. Doctrine resolution +
  gate dispatch are injected as a port (a `GatePorts`/`GateRegistry` façade) so
  the strangler lands on the target seam, not a temporary one (#2173).
- **The binding schema is a versioned evolution, not a free extension.**
  `MissionStep` and `MissionStepContractStep` are `extra="forbid"`. Adding a gate-
  binding field is a deliberate schema-version bump with generator + migration
  for existing built-in contracts.
- **Fail-open is load-bearing for *all* handler kinds**, including Path B. Restated
  because it is the invariant most easily lost when execution is added.

### Strangler migration path

The extracted `evaluate_with_scope` tail makes this incremental and low-risk;
each step is independently shippable and green-testable:

1. **Extract the scope authority behind a `ScopeSource` port.** Keep the current
   census impl as one strategy (`ci-dorny-census`); add a portable default
   (`explicit-list` / `changed-dir-glob`). `pre_review_gate` stops hardcoding
   `tests.architectural._gate_coverage`. **This step alone de-fangs #2330** and
   makes the gate meaningful in a consumer via explicit-list. Boy-scout, no
   behavior change for spec-kitty itself.
2. **Register the existing engine as the first handler.** Wrap
   `evaluate_pre_review_gate` as `GateHandler("pre-review-regression")` in a
   registry; `_mt_run_pre_review_gate` calls the registry, not the module.
   Behaviorally identical; pins parity with the existing move-task harness tests.
3. **Add the declarative binding schema** (versioned — `MissionStep` /
   `MissionStepContractStep` are `extra="forbid"`), with the schema-version bump,
   generator update, and a migration for the built-in step contracts. Ship the
   binding on spec-kitty's own `for_review` step in the default pack only.
4. **Invert control in the hook** — resolve active gate bindings for the
   transition via `get_by_action` + `PackContext`, dispatch each through the
   registry, keep the warn/block/`--force`/`policy_metadata` tail verbatim.
   **At this point #2534 is closed:** a consumer without the census binding in
   its active doctrine fires no census gate.
5. **(Opt-in, later) Add the Tier-1 `asset-backed` handler** + the trust
   contract, behind `review.allow_executable_gate_assets`. Requires the asset-
   resolution + (referenced-not-activated) selection work. This is Path B as a
   named later increment.

### Open decisions the spec must make

Carried forward from the target-architecture research; each is a real fork the
mission spec must resolve:

1. **Binding-schema location** — a new `gates` field on `MissionStep`, vs. reuse
   `MissionOrchestration.guards`/`required_artifacts` (opaque string lists) with
   a `gate:<id>` URN convention, vs. a field on the legacy
   `MissionStepContractStep`. Flag the versioned-migration cost either way.
2. **New kind or not** — is a gate a new activatable `ArtifactKind.GATE`, or is it
   bound through the already-activatable `mission_step_contract`/mission-type, or
   is it just a handler-id string? *Recommendation:* bind through step contracts
   to reuse `filter_graph_by_activation` for free; a new kind means touching the
   enum + `YAML_KEY_MAP` + `PackContext` + validators + migrations.
3. **Portable default scope for non-pytest repos** — a doctrine gate that still
   assumes pytest just relocates #2330. Decide the default strategy for a generic
   (Go/JS/Rust) repo: `explicit-list`, `changed-dir-glob`, or "run the configured
   test command whole" — **never** the census.
4. **Baseline coupling** — the block is inert without a captured baseline
   (`review.test_command`). Decide whether activating a *blocking* gate without a
   baseline becomes a hard config error rather than silent inertness.
5. **Execution-trust boundary** — in-scope (Path B) or explicitly out (Path A
   only) for this mission. If in: provenance allowlist, opt-in flag, interpreter
   allowlist/no-shell, timeout, structured-verdict-or-warn, fail-open — as
   recorded above.
6. **Fail-open invariant preserved for all handler kinds** — confirm every
   handler, including `asset-backed`, degrades to warn on resolution/execution
   failure.

## Consequences

### Positive

- **#2534 and #2330 are closed by construction**, not by convention: a consumer
  runs only the gates its active doctrine declares, and the census gate is a
  spec-kitty-only strategy that is never in a consumer's active set.
- **One canonical authority** for "which checks fire on which transition" (the
  activation-filtered step contract), replacing ~35 smeared `if target_lane ==`
  branches — D-044 satisfied.
- **Reuses existing machinery** (activation, `get_by_action`, the extracted
  verdict tail) for a small, centralized change surface; steps 1–2 are pure
  refactors, step 4 is the semantic pivot.
- **Aligns with #2173**: the gate becomes an injected port and move-task stays a
  thin orchestrator.
- **Opens a real doctrine-extensibility path** (Path B): an org can ship a
  bespoke gate without a spec-kitty release — the 3.3.x pack-ecosystem vision —
  without forcing the trust problem into the first increment.

### Negative

- **Under Path A, a new gate needs a spec-kitty release** (handlers are shipped
  code); orgs cannot ship a bespoke gate without upstreaming a handler until
  Path B lands.
- **A versioned strict-schema evolution** (`extra="forbid"`) is required to add
  the binding field — a deliberate bump with generator + migration cost.
- **Path B opens an RCE-equivalent trust surface.** Executing doctrine-supplied
  code is a hard, security-sensitive problem; the trust model is mandatory
  precisely because the failure mode is severe. This is why B is gated behind an
  off-by-default opt-in and a provenance allowlist.
- **Portability of the *script itself* (Path B) is unsolved by execution alone**:
  a doctrine script that assumes pytest is as brittle as today's `_gate_coverage`,
  only relocated. The `ScopeSource` abstraction (Path A) is what actually makes a
  gate portable; Path B inherits that, it does not replace it.

### Neutral

- The FSM entry-guards (`wp_state.py`) are untouched by this decision.
- **Follow-up #2536** — *pack activation must warn on code-asset packs.* Activating
  an org pack that ships executable gate assets must surface a clear warning at
  activation time, seeding a future **trust-tier / SK-accredited-certified-pack
  distribution model** (the 3.3.x vision). This is tracked as its own issue, not
  folded into this design.
- **Groundwork already landed:** the ASSET kind (#2469), step-contracts-as-kinds
  (#2468), and first-class TEMPLATE (#2495) provide the doctrine substrate this
  design builds on.

### Confirmation

The decision is confirmed when: (1) `_mt_run_pre_review_gate` resolves its gate
set from `get_by_action` + active-doctrine filtering rather than a
`target_lane == FOR_REVIEW` early return; (2) a fresh `spec-kitty init` consumer
repo performs a `move-task --to for_review` with **no** `GateAuthoritiesUnavailable`
path reached and **no** `tests.architectural._gate_coverage` import attempted;
(3) the scope authority is selected through `ScopeSource`, and a non-Python
consumer can run a meaningful gate via `explicit-list`/`review.test_command`;
(4) every degradation (unresolved binding, missing baseline, malformed verdict,
Path-B runner failure) yields a `NO_COVERAGE` warn, never a block; and (5) the
full `tests/architectural/` suite stays green, proving no regression against the
existing structural gates.

## Pros and Cons of the Options

### Option 1 — Keep everything hardcoded

**Pros:** zero new infrastructure.

**Cons:** leaves #2534/#2330 open; every new gate requires editing `specify_cli`
and a new `if target_lane == …` branch; consumers keep inheriting spec-kitty's
gate set. Structurally incomplete under D-043.

### Option 2 — Tactical message fix (cancelled)

**Pros:** smallest possible diff; makes the "gate authorities unavailable" path
look intentional.

**Cons:** cosmetic. The gate stays inert in every consumer, the gate set is still
decided by hardcoded Python, and the defect class is not closed — a next consumer
repo hits the same silent no-op. Rejected as treating a symptom.

### Option 3 — Path A only (no executable tier, ever)

**Pros:** trust-safe (no doctrine code runs); closes #2534/#2330; small change
surface.

**Cons:** forecloses the doctrine-extensibility vision (3.3.x pack ecosystem):
orgs can never ship a bespoke gate without upstreaming a handler and cutting a
spec-kitty release. Rejected in favor of designing the schema to *accommodate* B
even though A ships first.

### Option 4 — Path B only (ASSET-as-executable from the start)

**Pros:** maximal extensibility; directly realizes the "ASSET-kind helper"
vision; org/project-authored gates without a release.

**Cons:** largest greenfield (asset repo + resolver + entrypoint contract +
sandboxed runner + activation) and it opens the code-execution trust surface *in
the same mission that must also close #2534/#2330*. Highest blast radius, highest
risk, and it does not deliver the structural fix any sooner. Rejected as v1.

### Option 5 — Phased hybrid (CHOSEN)

**Pros:** delivers the structural win (doctrine-controlled, configured gates that
fix #2534/#2330 by construction) on the existing activation substrate, trust-safe,
with a small centralized change surface — while keeping the executable-asset
vision as a named, schema-compatible Phase 2 behind an off-by-default opt-in and a
mandatory trust model.

**Cons:** a new gate needs a spec-kitty release until Path B lands; requires a
versioned schema evolution; Path B, when it lands, still carries the trust burden
(mitigated, not eliminated, by the allowlist + opt-in + fail-open contract).

## More Information

- Predecessor substrate: [2026-05-16-1 — Doctrine layer merge semantics](2026-05-16-1-doctrine-layer-merge-semantics.md);
  [2026-05-24-2 — Pack augmentation vocabulary (`overrides`/`enhances`)](2026-05-24-2-pack-augmentation-vocabulary.md).
- Control-inversion precedent: [2026-06-26-1 — Single-authority seam + call-site gate](2026-06-26-1-single-authority-seam-and-call-site-gate.md);
  [2026-07-08-1 — MissionResolver Port (shell-side DI, injected port)](2026-07-08-1-mission-resolver-port.md).
- Narrative (living explanation): [`docs/architecture/doctrine-controlled-gates.md`](../../architecture/doctrine-controlled-gates.md).
- Load-bearing citations — #2534/#2330 locus: `src/specify_cli/review/pre_review_gate.py:85,98,100,131-159,358-423,451-511`;
  hook + policy tail: `src/specify_cli/cli/commands/agent/tasks_move_task.py:905-909,996,1012`;
  composer-only executor: `src/specify_cli/mission_step_contracts/executor.py:2-4,369-370`;
  contract lookup: `src/doctrine/missions/step_contracts.py:159-170`;
  hardcoded post-action guard: `src/runtime/next/runtime_bridge.py:1515`;
  activation selector: `src/specify_cli/charter/drg.py:293-334`;
  inert ASSET kind: `src/doctrine/assets/models.py:27-53`, `src/doctrine/artifact_kinds.py:178-190`;
  census authority: `tests/architectural/_gate_coverage.py:72-89,792-860`.
- Cross-references: epic [#2535](https://github.com/Priivacy-ai/spec-kitty/issues/2535) (this design),
  follow-up [#2536](https://github.com/Priivacy-ai/spec-kitty/issues/2536) (pack activation warns on code-asset packs; trust-tier seed),
  [#2534](https://github.com/Priivacy-ai/spec-kitty/issues/2534) (gate-coverage leak),
  [#2330](https://github.com/Priivacy-ai/spec-kitty/issues/2330) (pytest-layout assumption),
  [#2466](https://github.com/Priivacy-ai/spec-kitty/issues/2466);
  groundwork [#2469](https://github.com/Priivacy-ai/spec-kitty/issues/2469) (ASSET kind),
  [#2468](https://github.com/Priivacy-ai/spec-kitty/issues/2468) (step-contracts as kinds),
  [#2495](https://github.com/Priivacy-ai/spec-kitty/issues/2495) (TEMPLATE).
