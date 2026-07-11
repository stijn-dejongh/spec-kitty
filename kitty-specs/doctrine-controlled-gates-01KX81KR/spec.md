# Feature Specification: Doctrine-Controlled Transition Gates

**Mission**: doctrine-controlled-gates-01KX81KR
**Epic**: #2535 (under #2466 — Doctrine/Charter extensibility & pack ecosystem)
**Closes by construction**: #2534, #2330
**ADR**: [docs/adr/3.x/2026-07-11-1-doctrine-controlled-transition-gates.md](../../docs/adr/3.x/2026-07-11-1-doctrine-controlled-transition-gates.md)

## Summary

Task-lifecycle transition checks ("gates" — e.g. the pre-review regression gate
that fires on `move-task --to for_review`) are today hardcoded in `specify_cli`
as per-lane `if` branches and are shaped to spec-kitty's own repository (they
import a spec-kitty-only test module and assume a `src/specify_cli/` + pytest
layout). In any consumer repository those gates run inert **and** leak internal
module names into the operator's face (#2534, #2330).

This mission moves the **selection and supply** of transition gates into the
doctrine/charter layer. A mission **step contract** declares which gate(s) fire
on which transition; the gate logic is supplied by an **executable ASSET-kind
helper**; and the **charter** subsystem's activation decides which gates are
active in a given repository. A repository therefore runs exactly the gates its
active doctrine declares — a non-spec-kitty repo runs none by default and sees a
calm, non-blocking notice instead of a leaked internal module. Executing
doctrine-supplied code is confined to a strict trust envelope, and the whole
system is **fail-open**: no gate-infrastructure fault ever blocks a transition.

## User Scenarios & Testing

### Primary scenario (consumer repo, no gate declared)
A consumer-repo operator runs `spec-kitty agent tasks move-task WP01 --to for_review`.
No gate doctrine is charter-active in their repo. The transition proceeds and
surfaces a single clearly-labelled non-blocking notice: automated pre-review
regression scoping is not configured for this repository. No `src/specify_cli/`
path, no `tests.architectural._gate_coverage`, no spec-kitty-internal name
appears. (This is the #2534 defect, resolved.)

### Consumer declares its own gate (non-pytest repo)
A consumer maintainer authors, in their org pack, a gate asset plus a
`ScopeSource` and binds it to the `for_review` transition in a step contract,
then charter-activates it. Now `move-task --to for_review` runs *their* gate and
returns a real verdict — with no change to any `specify_cli` code. (This is the
#2330 defect, resolved.)

### spec-kitty's own repo (migration parity)
In the spec-kitty source repo the pre-review regression gate is now a built-in
gate asset bound through a built-in step contract. On the same changed-file set
it produces the **same** verdict (block / warn / no_coverage) as the prior
hardcoded gate — no observable behavior change for spec-kitty itself.

### Exception path (gate declared but unrunnable)
A gate is charter-active but cannot run — the gate asset fails to resolve, the
runner errors or times out, or a blocking test-run gate has no configured test
command. The transition **still proceeds**, emitting a calm non-blocking warn
that names the misconfiguration in operator terms (never an internal module).

### Trust path (untrusted / opt-out)
A gate asset whose provenance is outside the allowlist (e.g. an unverified
third-party pack), or any executable gate asset while the opt-in flag is off, is
**never executed**. The operator sees an explicit "not executed — provenance /
opt-in" notice; the transition proceeds fail-open.

## Domain Language

| Term | Meaning | Avoid |
|------|---------|-------|
| **Gate** | A check bound to a task-lifecycle transition (e.g. pre-review regression). | "hook" (overloaded) |
| **Gate binding** | The declarative `transition → gate` association carried on a mission step contract. | "wiring" |
| **Gate asset** | An executable ASSET-kind doctrine helper that supplies a gate's logic and returns a structured verdict. | "plugin", "script" (unqualified) |
| **ScopeSource** | A doctrine-declared strategy that derives the affected test/verification scope for a change (portable; not pytest-bound). | "filter group" (that is spec-kitty's internal shape) |
| **Active doctrine** | The set the **charter** subsystem has activated for the repository — the sole gate-selection authority. | "installed doctrine" |
| **Fail-open** | Any gate-infrastructure fault degrades to a non-blocking warn; only a real computed regression may block. | "fail-safe" (ambiguous) |
| **Trust envelope** | Provenance allowlist + opt-in flag + interpreter allowlist / no-shell + timeout that confine gate-asset execution. | "sandbox" (alone) |

## Functional Requirements

| ID | Requirement | Status |
|----|-------------|--------|
| FR-001 | A mission **step contract** can declaratively bind one or more gates to a named transition (e.g. `for_review`). The binding is data on the existing activatable step-contract surface — not a hardcoded per-lane branch in `specify_cli`. | Proposed |
| FR-002 | The runtime gate consumers (the `move-task` pre-review hook and the composed-action post-task guard) resolve the **active gate set for a transition from the step-contract bindings**, replacing the hardcoded `if target_lane == Lane.X` decision of which check runs. | Proposed |
| FR-003 | The **charter** subsystem is the single selection authority: only gates whose declaring doctrine is charter-active fire. A repository with no active gate doctrine runs no gate. Selection reuses the existing activation/DRG machinery (`filter_graph_by_activation`) — no parallel gate-enablement registry. | Proposed |
| FR-004 | Gate logic is supplied by an **executable ASSET-kind helper**: a gate asset declares a code entrypoint that the runtime resolves (URN → path) and invokes to produce a structured gate **verdict** (`no_new_failures` / `regression` / `no_coverage` / `error`, with a `blocking` flag and an operator-facing message). | Proposed |
| FR-005 | Build the ASSET **execution substrate** that does not exist today: an asset repository, a URN→path resolver, a code-asset **entrypoint contract**, and a **runner**. Non-gate assets remain inert by default — code execution is a new, distinct capability, not a generalization of asset loading. | Proposed |
| FR-006 | Gate assets and/or their bindings participate in **charter activation** so the active doctrine selects them (binding through activatable step contracts per FR-001 is the chosen vehicle; assets are non-activatable today). | Proposed |
| FR-007 | Executing a gate asset is confined to a **trust envelope**: provenance allowlist (built-in and org-pack only by default; never arbitrary third-party), an explicit opt-in flag (`review.allow_executable_gate_assets`, default off), an interpreter allowlist with no shell interpolation, and an enforced timeout. A gate asset failing any of these is not executed. | Proposed |
| FR-008 | When no gate/ScopeSource is charter-active for a transition, the transition emits a **calm, clearly-labelled, non-blocking notice** ("automated pre-review scope not configured for this repository") that names **no** spec-kitty-internal module or layout. | Proposed |
| FR-009 | Scope derivation is a **doctrine-declared `ScopeSource` strategy**, not a hardcoded pytest / `src/specify_cli/` / `tests.architectural._gate_coverage` assumption. A non-pytest repo is served by its own declared `ScopeSource` or by the FR-008 calm default. | Proposed |
| FR-010 | **Fail-open**: any unrunnable, misconfigured, or unresolvable gate (asset resolve failure, runner error, timeout, missing test command, inactive/absent doctrine) degrades to a non-blocking warn. Only a real computed regression may block, and only when that gate is configured to block. | Proposed |
| FR-011 | **Strangler migration**: the existing pre-review regression gate is re-expressed as the first built-in gate asset bound through a built-in step contract, and the hardcoded `pre_review_gate` invocation is inverted to resolve through the binding. The extracted verdict tail (`evaluate_with_scope`) is reused. | Proposed |
| FR-012 | The consumer-facing gate path **must not import** `tests.architectural._gate_coverage` nor assume `_SRC_PACKAGE_PREFIX = "src/specify_cli/"`; those spec-kitty-shaped authorities become a built-in `ScopeSource` used only when spec-kitty's own doctrine is active. | Proposed |
| FR-013 | Operators can observe, for a given transition, **which gates are active and why** (their declaring doctrine + activation state), so a "why did/didn't a gate run" question is answerable without reading `specify_cli` source. | Proposed |

## Non-Functional Requirements

| ID | Requirement | Threshold / Measure | Status |
|----|-------------|---------------------|--------|
| NFR-001 | Behavior parity for spec-kitty's own repo: the migrated built-in gate yields the same verdict as the prior hardcoded gate on the same inputs. | 100% of existing `pre_review_gate` verdict tests pass unchanged (or with only binding-indirection edits); zero new failures attributable to the migration. | Proposed |
| NFR-002 | Consumer-repo portability: no transition in a repo lacking spec-kitty's test layout surfaces any spec-kitty-internal module/path. | A consumer-shaped fixture (no `tests/architectural/_gate_coverage.py`, non-pytest) crossing `for_review` produces the FR-008 notice and its output contains none of `tests.architectural._gate_coverage`, `src/specify_cli/`. | Proposed |
| NFR-003 | Fail-open holds for every handler kind and every fault. | Fault-injection tests (missing asset, runner exception, timeout, no test command, inactive doctrine) each yield a non-blocking warn; zero of them block the transition. | Proposed |
| NFR-004 | Trust envelope is enforced. | A gate asset with non-allowlisted provenance, and any executable gate asset while the opt-in flag is off, is never executed (asserted by a test that would observe a side effect if it ran). | Proposed |
| NFR-005 | Doctrine-only extensibility: adding/removing a gate for a transition changes no `specify_cli` control flow. | A test adds a gate to a transition via doctrine artifacts only (step-contract binding + gate asset) and observes it fire, with no edit to `specify_cli` gate-decision code. | Proposed |
| NFR-006 | Bounded execution. | Every gate-asset run is subject to an enforced timeout (default mirrors the current baseline run timeout); an over-running gate is terminated and folds to a fail-open warn. | Proposed |

## Constraints

| ID | Constraint | Status |
|----|------------|--------|
| C-001 | The **charter** subsystem is the single gate-selection authority (operator 2026-07-11). No parallel enablement registry; reuse `filter_graph_by_activation`. | Active |
| C-002 | Fail-open is load-bearing: never introduce a "cannot move task because doctrine is misconfigured" hard block for gate-infrastructure faults. | Active |
| C-003 | Executable gate assets run **only** behind the trust envelope; the loose-contract ASSET kind's inert-by-default posture is preserved for all non-gate assets. Code execution is opt-in, not a generalization of asset loading. | Active |
| C-004 | Unification not parity: the hardcoded spec-kitty-shaped `pre_review_gate` path is **removed** (folded into a built-in `ScopeSource`), not preserved as a compatibility fallback. | Active |
| C-005 | Reuse existing substrate: the activation/DRG machinery and the extracted `evaluate_with_scope` verdict tail. No parallel resolver; the gate-decision **binding** is the new seam, not a new read path. | Active |
| C-006 | The binding field lands on `extra="forbid"` step-contract/MissionStep models, so it requires a **versioned schema evolution** plus a migration for built-in step contracts — not a silent field add. | Active |
| C-007 | Planning on a coord-topology mission whose `target_branch` is a feature branch (`design/doctrine-controlled-gates`) — status stays on the coordination branch; planning artifacts follow the repo's current write-surface authority. | Active |

## Key Entities

- **Gate binding** — declarative `transition → gate URN` association on a mission step contract; the unit charter activation selects.
- **Gate asset** — executable ASSET-kind helper (URN + code entrypoint) that returns a structured verdict.
- **ScopeSource** — doctrine-declared scope-derivation strategy; spec-kitty's filter-group/census model becomes one built-in implementation.
- **Gate verdict** — `{ status, blocking, message }` returned by a gate; the fail-open reducer maps faults to non-blocking warns.
- **Trust envelope** — provenance allowlist + `review.allow_executable_gate_assets` opt-in + interpreter allowlist/no-shell + timeout.
- **Charter activation** — the selection authority that turns declared gates into active gates for a repository.

## Success Criteria

| ID | Criterion |
|----|-----------|
| SC-001 | A consumer repo (no spec-kitty test layout) crossing `move-task --to for_review` sees a calm non-blocking notice and **zero** occurrences of `tests.architectural._gate_coverage` or `src/specify_cli/` in the output. (#2534 closed) |
| SC-002 | A non-pytest consumer repo declares a gate + `ScopeSource` in its doctrine, charter-activates it, and it runs on `for_review` with a real verdict — with **no** change to `specify_cli` code. (#2330 closed) |
| SC-003 | In spec-kitty's own repo the migrated built-in gate produces the **identical** pre-review verdict to the prior hardcoded gate on the same change set. |
| SC-004 | Adding a new gate to a transition requires **only** doctrine edits (step-contract binding + gate asset); no `specify_cli` gate-decision code changes. |
| SC-005 | **Every** injected gate-infrastructure fault (missing asset, runner error, timeout, no test command, inactive doctrine) yields a non-blocking warn; none blocks the transition. |
| SC-006 | A gate asset from non-allowlisted provenance, or any executable gate asset while `review.allow_executable_gate_assets` is off, is **refused execution** and the transition proceeds fail-open. |

## Resolved Decisions

| ID | Decision | Source |
|----|----------|--------|
| RD-001 | Gates bind via **activatable step contracts** (reuse charter activation), not a new first-class `gate` DRG kind. | operator 2026-07-11 |
| RD-002 | "Active doctrine" = the **charter-activated** set; the charter subsystem is the selection authority. | operator 2026-07-11 |
| RD-003 | Portable default when nothing is declared = a **calm non-blocking notice**, not a heuristic scope and not a hard opt-in error. | operator 2026-07-11 |
| RD-004 | An unrunnable/misconfigured gate is a **fail-open non-blocking warn**. | operator 2026-07-11 |
| RD-005 | **Full scope A+B** in one mission: declarative bindings + the executable ASSET subsystem + the trust model. | operator 2026-07-11 |

## Assumptions

- The activation machinery (`filter_graph_by_activation`) and the extracted verdict tail (`evaluate_with_scope`) are reused rather than reinvented.
- The binding schema evolves the existing step-contract / `MissionStep` models via a versioned bump plus a built-in-contract migration (C-006).
- Baseline coupling: a blocking test-run gate remains inert without a configured test command; per RD-004 that is a fail-open warn, not an error.
- Provenance tiers (built-in / org-pack / third-party) are derivable from existing pack-load provenance; cryptographic verification is not required for this mission.

## Out of Scope

- **Pack-activation warning** when a pack ships executable code assets — tracked as **#2536** (follow-up).
- **Trust tiers / `verified` status / SK-accredited certified-pack distribution** and signature/provenance cryptography — 3.3.x vision, seeded by #2536.
- Migrating **all ~35** non-review transition gates at once — this mission delivers the substrate and migrates the pre-review regression gate as the exemplar; the rest is incremental follow-on.
- Any change to the FSM entry-guards in `status/wp_state.py` (already repo-agnostic; not part of the leak).
