---
title: 'ADR: Doctrine-Controlled Transition Gates — Declarative Bindings and Executable ASSET Helpers, Both In Scope This Mission'
status: Proposed
date: '2026-07-11'
---

## Context and Problem Statement

Every check that fires on a mission task-lifecycle transition is **hardcoded in
`specify_cli` Python**. There are roughly **35 such command-layer transition
checks** across the command layer (`tasks_move_task.py`, `implement.py`,
`accept.py`, `policy/merge_gates.py`), and **no data-driven registry anywhere maps
a transition → the set of checks that should run on it**. The applicability
mechanism is not uniform: only about a dozen sites are literal `if target_lane ==
Lane.X` compares (the pre-review hook's early return being the clearest); the rest
decide through `if policy.require_X` merge-gate flags and composed-action
`(mission, action)` guard dispatch. Whatever the spelling, the binding is
imperative and inline — adding a check today means editing `specify_cli` and
wiring a new conditional, and a consumer repo inherits spec-kitty's exact gate set
whether or not it fits.

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
   execution"* disclaimer (`executor.py:372`) and **never executed**. The real
   gates are a separate hardcoded system that never reads the contract. Likewise
   the post-action guard `_check_composed_action_guard` (`runtime_bridge.py:1515`)
   is a hardcoded `if/elif` chain on `(mission, action)`, not contract-driven.
   Meanwhile the activation machinery that already gates mission-type → step-
   contract selection (`filter_graph_by_activation`, `src/charter/drg.py:319`,
   predicate `:293-316`) is a ready-made "active doctrine selects which artifact
   applies" mechanism.

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

1. **Keep everything hardcoded** (status quo) — extend the inline `if target_lane
   == …` / `if policy.require_X` / `(mission, action)` guard cascades in
   `specify_cli` for each new gate.
2. **Tactical message fix** (the cancelled option) — make the pre-review gate's
   "gate authorities unavailable" path clearer / gate the `_gate_coverage`
   import so it does not appear to run in consumers, without changing where the
   gate set is decided.
3. **Path A only — declarative bindings + shipped handler registry**, no
   executable-asset tier, ever.
4. **Path B only — ASSET-as-executable** from the start: doctrine ships the gate
   script, runtime resolves + runs it.
5. **Phased hybrid — Path A now, Path B as an explicit opt-in *later* tier, with a
   mandatory trust model authored up front.** This was the ADR's *initial*
   recommendation; it was **superseded by RD-005** (see Decision Outcome) and is
   retained here as the rejected-in-favour-of-full-scope alternative.
6. **Full A+B in this mission — both mechanisms in scope now**: Path-A handlers
   (spec-kitty-shipped, no opt-in) *and* Path-B executable gate assets
   (doctrine-supplied, default-off opt-in behind a real containment envelope),
   on one coherent schema authored to carry both — **chosen (RD-005)**.

## Decision Outcome

**Chosen option:** "Full A+B in this mission" (Option 6).

> **RD-005 (operator, 2026-07-11).** The ADR's initial draft recommended the
> phased hybrid (Option 5): Path A now, Path B as a later opt-in tier. The
> operator superseded that with **full A+B in this mission** — both mechanisms are
> in scope now. Rationale: (a) **safety-first for a new product gap** — the
> executable-gate-asset trust model is easier to get right when designed and
> shipped *with* its consumers than retrofitted onto a Path-A-only base whose
> schema and handler registry have already frozen around the no-code-execution
> assumption; (b) **a single coherent schema** — authoring the binding + handler
> contract once, with Path B's execution/trust fields present from day one, avoids
> a second schema-version bump and migration when the executable tier lands. Path
> B remains gated by its trust envelope (default-off opt-in + containment); "in
> scope now" changes *when*, not *whether*, that envelope is mandatory.

> **RD-006 (operator, 2026-07-11) — containment primitives, refuse-unconfinable
> v1.** The v1 containment envelope for `asset-backed` gates is built from
> **in-process, dependency-free primitives — no new sandbox dependency**:
> (a) an **environment allowlist** passed to the child — an explicit minimal env,
> **never `dict(os.environ)`** (which would leak tokens/keys);
> (b) **process-group kill + `setrlimit`** for the wall-clock/memory/CPU/output
> limits; (c) **path-resolved filesystem confinement** (writes only to a dedicated
> scratch dir, checked after symlink resolution);
> (d) a **dedicated, size-capped, schema-validated verdict channel** distinct from
> stdout, so stray script output cannot forge a verdict (SC-011);
> (e) **derived provenance** — the loader **must stop overwriting `source_kind`**
> so a `third_party` provenance is actually *producible* (and therefore
> *refusable*); provenance is read from load metadata, never self-declared;
> (f) a **capability probe that refuses** to run where these cannot be
> established, rather than degrading to an unconfined run. Active network-egress
> blocking and OS-level isolation (namespaces / Landlock / seccomp) are
> **deferred** — v1 safety comes from *refusing*, not from *sandboxing*.

Make transition pre-gate checks **doctrine-controlled and configured** instead of
hardcoded in `specify_cli`, delivering **both** the declarative-binding spine
(Path A) and the executable-ASSET-helper tier (Path B) in this mission, on one
schema authored to support both. Path B ships behind a default-off opt-in and the
containment envelope recorded below; it is not a deferred increment.

### Decisions recorded

- **A — Declarative bindings (the spine, delivered first).** Mission **step
  contracts** declare which gate(s) fire on which transition; the repo's **active
  doctrine** (charter activation via `filter_graph_by_activation`) selects the
  gate set. The load-bearing change is **rewiring the consumers' *selection*
  only** — this is the seam both consumers share, and *only* selection is shared.
  The move-task pre-review hook (`tasks_move_task.py:996`) and the post-action
  guard (`_check_composed_action_guard`, `runtime_bridge.py:1515`) stop hardcoding
  *which* gate fires (`if target_lane == X` / `if (mission, action) == …`) and
  instead resolve their declared gate bindings through one **selection** surface
  (`resolve_gates`, backed by `MissionStepContractRepository.get_by_action` with a
  small lane↔action adapter so the lane-keyed hook and the action-keyed guard
  share the same lookup). **Reduction stays per gate-class — it is NOT unified.**
  The artifact-presence guard keeps its own **fail-closed** reduction (missing
  `spec.md`/`plan.md`/`tasks.md` is a hard block) and is **never** routed through
  the regression gate's "only a new failure blocks, everything else warns"
  reducer; doing so would silently downgrade its hard-blocks (SC-010). The two
  consumers converge on *selection*; each keeps its own verdict semantics. Gate
  logic **ships in spec-kitty as named handlers behind a `GateHandler` port +
  registry**; doctrine *selects and parameterizes*, it does not *supply code*. The
  existing `evaluate_pre_review_gate` becomes the first registered handler. Scope
  stops importing `tests.architectural._gate_coverage` and is chosen through a
  `ScopeSource` strategy (explicit-list / changed-dir-glob / "run the configured
  `review.test_command` whole"); the census/dorny strategy becomes one pluggable
  option that spec-kitty ships for *itself*, never a default others inherit.

- **B — Executable ASSET-kind helpers (extends the existing ASSET substrate, in
  scope this mission behind the containment envelope).** A gate helper *is* an
  ASSET blob (a script) referenced from an activatable step contract. This is a
  **new execution subsystem built by extending the existing ASSET kind, not a
  greenfield one**: the manifest model (`assets/models.py`) and `pack_validator`
  already exist — the mission adds an asset repository + a URN→path resolver (today
  the manifest `path` is validated then discarded), a code-asset **entrypoint
  contract** (argv/stdin = changed-files + baseline; the verdict is returned on a
  **dedicated, size-capped, schema-validated channel — never stdout** (see FR-019
  / SC-011: stray stdout must not be able to forge a verdict); declared interpreter
  + resource limits), a **contained runner** (see the trust model below —
  interpreter-allowlist alone is not a sandbox), and asset **activation** (assets
  are non-activatable today). B is an *additive `GateHandler` kind* (`asset-backed`)
  on the same schema and registry as Path A, so both are authored once. Per RD-005
  it ships in this mission, gated by the default-off opt-in and the containment
  envelope — not as a deferred increment.

- **Mandatory trust model — real containment, not just an interpreter allowlist
  (a first-class pillar because doctrine-supplied code now executes).**
  Interpreter-allowlist + no-shell + timeout is an *input-shaping* discipline, not
  a sandbox: a script invoked with an allowlisted interpreter can still read the
  developer's SSH keys, exfiltrate the tree over the network, or fork-bomb the
  host. Every executable-asset gate is therefore subject to, at minimum:
  - **Derived provenance allowlist** — only *built-in* and *governed org-pack*
    assets may be executable; **never** a project-local or mission-authored asset.
    Provenance is **derived from pack-load metadata** (which layer/pack the asset
    was loaded from), **never self-declared** by the asset or its manifest — a
    project-tier asset cannot claim built-in provenance to earn execution.
  - **Interpreter allowlist / no shell** — the execution contract names an
    interpreter from an allowlist and passes an **argv vector**; never
    `shell=True`, never a raw command string.
  - **Explicit opt-in flag** — `review.allow_executable_gate_assets: true` in
    config, **off by default**. A repo that never opts in can never be made to
    run a doctrine script.
  - **Filesystem confinement** — the runner may **read** the mission tree +
    declared inputs but must **not write outside a dedicated scratch dir**;
    enforced by path-resolved confinement (no writes to the repo tree, `$HOME`, or
    system paths).
  - **Refuse-unconfinable v1, no active no-egress guarantee (RD-006).** v1 does
    **not** actively block outbound network with an OS sandbox. Instead a
    **capability probe refuses to run** the asset where filesystem (and network)
    confinement cannot be established on the host — the gate is skipped with a
    warn rather than executed unconfined. Deeper OS isolation (Linux namespaces /
    Landlock / seccomp for a hard no-egress boundary) is **deferred**; v1 buys
    safety by refusing, not by sandboxing.
  - **Resource limits** — bounded **wall-clock timeout, memory, CPU, and
    output size** via process-group kill + `setrlimit`; an over-limit process is
    killed and its gate degrades to warn (fail-open, below).
  - **Refuse rather than run unconfined** — if a required containment primitive is
    unavailable on the host (the capability probe cannot establish fs/resource
    confinement), the asset gate is **refused** (skipped with a warn), **never
    executed unconfined**. Containment is a precondition of execution, not
    best-effort.
  - **Fail-OPEN, structured-verdict-or-warn** — a malformed verdict, a resolution
    failure, a missing/refused runner, or a limit kill degrades to a `NO_COVERAGE`
    warn and the transition proceeds; a doctrine/asset misconfiguration must
    **never** harden into a block.
  - **Cryptographic/signature provenance is deferred** to #2536 (the trust-tier /
    accredited-pack model); v1 provenance is layer-derived, not signature-verified.

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
5. **Add the `asset-backed` handler + the containment envelope (in scope this
   mission, RD-005)**, behind the default-off `review.allow_executable_gate_assets`
   opt-in. Requires the asset-resolution + (referenced-not-activated) selection
   work and the contained runner (path-resolved fs confinement, `setrlimit` +
   process-group resource limits, dedicated verdict channel, capability-probe
   refuse-if-unconfinable — no active no-egress guarantee in v1, RD-006).
   Sequenced last so it lands on the frozen Path-A
   registry + schema, but delivered in **this** mission, not deferred.

### Resolved decisions

- **Execution-trust boundary — RESOLVED in scope (RD-005).** Path B (executable
  ASSET gate helpers) is **in scope this mission**, not deferred and not out. The
  binding terms are the containment envelope in the trust-model bullet above and
  the RD-006 primitives: derived-provenance allowlist (built-in/org-pack only),
  default-off opt-in (`review.allow_executable_gate_assets`),
  interpreter-allowlist/no-shell, path-resolved filesystem confinement,
  `setrlimit`/process-group memory/CPU/output-size limits, a dedicated verdict
  channel, and a **capability-probe that refuses to run when confinement can't be
  established (no active no-egress guarantee in v1)** — all fail-open.
  Signature-based provenance and active OS-level egress isolation are deferred to
  #2536. (This was open-decision #5 in the initial draft.)

### Open decisions the spec must make

Carried forward from the target-architecture research; each is a real fork the
mission spec must resolve:

1. **Binding-schema location** — a new `gates` field on `MissionStep`, vs. reuse
   `MissionOrchestration.guards`/`required_artifacts` (opaque string lists) with
   a `gate:<id>` URN convention, vs. a field on the legacy
   `MissionStepContractStep`. The single-schema-for-both mandate (RD-005) raises
   the bar: the chosen location must carry Path B's execution/trust fields from
   day one. Flag the versioned-migration cost either way.
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
5. **Fail-open invariant preserved for all handler kinds** — confirm every
   handler, including `asset-backed`, degrades to warn on resolution/execution
   failure.
6. **Containment mechanism per host** — RD-006 fixes the v1 primitives (env
   allowlist, `setrlimit` + process-group kill, path-resolved fs confinement,
   dedicated verdict channel, capability-probe→refuse). The spec must still pin
   **what the capability probe concretely detects** per supported platform, and
   **when** the deferred active-egress/OS-isolation tier (namespaces / Landlock /
   seccomp) is scheduled.

## Consequences

### Positive

- **#2534 and #2330 are closed by construction**, not by convention: a consumer
  runs only the gates its active doctrine declares, and the census gate is a
  spec-kitty-only strategy that is never in a consumer's active set.
- **One canonical authority** for "which checks fire on which transition" (the
  activation-filtered step contract), replacing ~35 smeared command-layer
  conditionals (a mix of literal `target_lane ==` compares, `policy.require_X`
  flags, and `(mission, action)` guard dispatch) — D-044 satisfied.
- **Reuses existing machinery** (activation, `get_by_action`, the extracted
  verdict tail) for a small, centralized change surface; steps 1–2 are pure
  refactors, step 4 is the semantic pivot.
- **Aligns with #2173**: the gate becomes an injected port and move-task stays a
  thin orchestrator.
- **Delivers doctrine-extensibility now** (Path B, RD-005): an org can ship a
  bespoke gate without a spec-kitty release — the 3.3.x pack-ecosystem vision —
  in this mission, gated by the containment envelope rather than deferred behind a
  second schema bump.

### Negative

- **Built-in (Path-A) handlers still need a spec-kitty release** — a *first-party*
  gate ships as handler code. But per RD-005 orgs are **not** blocked on that:
  Path B lets a governed org pack ship a bespoke executable gate this mission,
  behind the opt-in + containment envelope.
- **A versioned strict-schema evolution** (`extra="forbid"`) is required to add
  the binding field. RD-005's single-schema-for-both mandate makes this a *larger*
  one-time design (Path B's execution/trust fields present from day one) in
  exchange for avoiding a second bump + migration later.
- **Path B opens an RCE-equivalent trust surface, delivered now.** Executing
  doctrine-supplied code is a hard, security-sensitive problem; bringing it into
  this mission is why the trust model is a *real containment envelope*
  (path-resolved fs confinement, `setrlimit`/process-group resource limits,
  dedicated verdict channel, derived provenance, capability-probe refuse-if-
  unconfinable), not merely an interpreter allowlist. v1 buys safety by
  *refusing* where it can't confine rather than by actively sandboxing egress
  (RD-006) — active OS isolation is deferred. Getting the confinement + refuse
  logic right is the dominant risk this mission carries.
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
and wiring a new inline conditional (a `target_lane ==` compare, a
`policy.require_X` flag, or a `(mission, action)` guard); consumers keep
inheriting spec-kitty's gate set. Structurally incomplete under D-043.

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
spec-kitty release. Rejected in favour of full A+B this mission (Option 6): the
executable tier is a product gap worth closing now, on one coherent schema.

### Option 4 — Path B only (ASSET-as-executable from the start)

**Pros:** maximal extensibility; directly realizes the "ASSET-kind helper"
vision; org/project-authored gates without a release.

**Cons:** largest build (asset repo + resolver + entrypoint contract + contained
runner + activation — extending the existing ASSET kind, not greenfield) and it
opens the code-execution trust surface *in the same mission that must also close
#2534/#2330*. Highest blast radius, highest risk, and it does not deliver the
structural fix any sooner. Rejected as v1.

### Option 5 — Phased hybrid (initial recommendation, SUPERSEDED by RD-005)

**Pros:** delivers the structural win (doctrine-controlled, configured gates that
fix #2534/#2330 by construction) on the existing activation substrate first,
trust-safe in its first increment, with a small centralized change surface — while
keeping the executable-asset tier as a named, schema-compatible later phase behind
an off-by-default opt-in and a mandatory trust model.

**Cons:** defers the executable-gate product gap; and freezing the Path-A schema +
handler registry around the no-code-execution assumption risks a **second** schema
bump + migration when Path B is retrofitted, and a trust envelope designed after
the fact rather than with its consumers. **Superseded** by the operator's RD-005
decision to take full A+B in one mission for exactly these reasons.

### Option 6 — Full A+B in this mission (CHOSEN, RD-005)

**Pros:** delivers the structural fix (#2534/#2330 closed by construction) *and*
the executable-gate product gap in one mission, on a single coherent schema whose
execution/trust fields exist from day one — no second bump, no retrofitted trust
model. The containment envelope is designed together with the handler registry it
guards.

**Cons:** the largest single design (Path-A binding + registry + Path-B asset
resolution + activation + a real containment runner) in one mission; and it takes
on the code-execution trust surface now rather than later — the containment
envelope (path-resolved fs confinement, `setrlimit`/process-group resource limits,
dedicated verdict channel, derived provenance, capability-probe refuse-if-
unconfinable, fail-open; active egress isolation deferred, RD-006) must be right on
first delivery. Mitigated by sequencing Path B last in the strangler so it lands
on the frozen Path-A spine.

## More Information

- Predecessor substrate: [2026-05-16-1 — Doctrine layer merge semantics](2026-05-16-1-doctrine-layer-merge-semantics.md);
  [2026-05-24-2 — Pack augmentation vocabulary (`overrides`/`enhances`)](2026-05-24-2-pack-augmentation-vocabulary.md).
- Control-inversion precedent: [2026-06-26-1 — Single-authority seam + call-site gate](2026-06-26-1-single-authority-seam-and-call-site-gate.md);
  [2026-07-08-1 — MissionResolver Port (shell-side DI, injected port)](2026-07-08-1-mission-resolver-port.md).
- Narrative (living explanation): [`docs/architecture/doctrine-controlled-gates.md`](../../architecture/doctrine-controlled-gates.md).
- Load-bearing citations — #2534/#2330 locus: `src/specify_cli/review/pre_review_gate.py:85,98,100,131-159,358-423,451-511`;
  hook + policy tail: `src/specify_cli/cli/commands/agent/tasks_move_task.py:905-909,996,1012`;
  composer-only executor: `src/specify_cli/mission_step_contracts/executor.py:2-4,372`;
  contract lookup: `src/doctrine/missions/step_contracts.py:159-170`;
  hardcoded post-action guard: `src/runtime/next/runtime_bridge.py:1515`;
  activation selector: `src/charter/drg.py:319` (`filter_graph_by_activation`, predicate `:293-316`);
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
