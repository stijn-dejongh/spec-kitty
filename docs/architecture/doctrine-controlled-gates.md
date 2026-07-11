---
title: Doctrine-Controlled Transition Gates
description: "How Spec Kitty is moving transition pre-gate checks from hardcoded specify_cli branches to doctrine-declared, activation-selected gate bindings — and the trust model for executable ASSET-kind gate helpers."
doc_status: active
updated: '2026-07-11'
related:
- docs/adr/3.x/2026-07-11-1-doctrine-controlled-transition-gates.md
- docs/architecture/kanban-workflow.md
- docs/architecture/mission-system.md
- docs/architecture/doctrine-relationships.md
- docs/architecture/charter-synthesis-drg.md
---
# Doctrine-Controlled Transition Gates

This page explains *why* Spec Kitty is moving transition pre-gate checks out of
hardcoded `specify_cli` branches and into **doctrine-declared, activation-selected
gate bindings**, and how the target data flow works. The authoritative decision —
including the strangler migration, the trust model, and the open spec forks — is
[ADR 2026-07-11-1: Doctrine-Controlled Transition Gates](../adr/3.x/2026-07-11-1-doctrine-controlled-transition-gates.md).
This page narrates and links up to that ADR; it does not restate the decision.

## The problem: gates are hardcoded and spec-kitty-shaped

A **gate** is a check that fires when a work package crosses a lane boundary —
most visibly the **pre-review regression gate** on the `in_progress → for_review`
transition (see [Kanban Workflow](kanban-workflow.md) for the lane model and its
guards). Today every such check is hardcoded in `specify_cli`, keyed on the lane
enum by literal `if target_lane == Lane.X` branches. There is no registry that
maps a transition to the set of checks it should run.

That coupling leaks. The pre-review gate imports a repo-internal test module
(`tests.architectural._gate_coverage`) as its scope authority and assumes a
`src/specify_cli/` package layout, a pytest runner, and JUnit output. In any
consumer repository that module does not exist and those assumptions do not hold,
so the gate silently degrades to a "no coverage" warning — inert everywhere
except spec-kitty itself, while still dragging spec-kitty's CI topology into the
consumer. Those are issues **#2534** (the module leak) and **#2330** (the
pytest-layout assumption).

## The shape of the fix: declare, select, dispatch

The fix inverts control so a repository's **active doctrine declares its own
gates**. Two doctrine surfaces already exist and are simply not wired to gates
yet:

- **Mission step contracts** are machine-loaded, schema-validated, and resolvable
  by `(mission, action)` — they already model the transition step. See
  [The Mission System](mission-system.md) for step contracts and guards.
- **Charter activation** already selects which mission-type step contract applies,
  by filtering the Doctrine Reference Graph (DRG). See
  [Understanding Charter: Synthesis, DRG, and Governed Context](charter-synthesis-drg.md)
  and [Doctrine relationships](doctrine-relationships.md) for the DRG model.

The target design binds a gate to a transition **in the step contract**, selects
it through **existing activation**, and dispatches it through a **shipped handler
registry** — so doctrine *selects and parameterizes* the gate rather than
*supplying its code* (Path A). Executable **ASSET-kind** gate helpers, where
doctrine can ship the gate script itself, are a deliberately later, opt-in tier
(Path B) governed by a mandatory trust model.

## Target data flow

```
move-task --to for_review
  └─ resolve active mission-type + step contract        (PackContext + get_by_action)
       └─ filter_graph_by_activation drops gates not in active doctrine
  └─ read the step's gate bindings → [gate:pre-review-regression, …]
  └─ for each declared gate:
       ├─ GateRegistry.get(id) → shipped handler          (Path A: no doctrine code runs)
       │     └─ (Path B, opt-in) asset-backed handler:
       │          resolve asset:<id> → blob path → sandboxed run
       ├─ handler.resolve_scope(changed_files, ScopeSource)   (portable; no _gate_coverage import)
       ├─ handler.run(scope) → structured verdict
       └─ GateVerdict
  └─ warn / opt-in block / --force ; record on transition policy_metadata   (unchanged tail)
```

The move-task hook, the `policy_metadata` write, and the warn/block/`--force`
policy tail stay where they are; only *scope resolution* and *which gate fires*
move from hardcoded Python to doctrine-declared bindings dispatched through a
port. This keeps the hook a thin orchestrator, aligned with the
infra/logic-separation epic (#2173).

## Why this closes the defect class by construction

A consumer repository runs **only the gates its active doctrine declares**.
Spec-kitty's census gate (the `_gate_coverage` strategy) becomes one pluggable
`ScopeSource` that spec-kitty ships *for itself* — never a default others
inherit. A repo whose active doctrine does not declare that gate never fires it,
so #2534 and #2330 cannot recur. The portable default scope strategies
(`explicit-list`, `changed-dir-glob`, or "run the configured `review.test_command`
whole") make the gate meaningful in non-Python repos without assuming pytest.

## The trust model (executable ASSET helpers)

Path B lets doctrine ship gate code, which is an RCE-equivalent surface. The ADR
makes the trust model a first-class, mandatory pillar rather than an afterthought:

- **Provenance allowlist** — only built-in and governed org-pack assets may be
  executable; never a project-local or mission-authored asset by default.
- **Interpreter allowlist / no shell** — a named interpreter and an argv vector;
  never `shell=True` or a raw command string.
- **Explicit opt-in** — `review.allow_executable_gate_assets`, off by default.
- **Bounded execution** — timeout + environment scrub.
- **Fail-open** — a malformed verdict or any resolution/execution failure
  degrades to a warn; a doctrine misconfiguration must never harden into a block.

Follow-up **#2536** adds an activation-time warning when an org pack ships
executable gate assets — the seed of a future trust-tier / accredited-pack
distribution model.

## Status

This is a **proposed** design (epic #2535) recorded ahead of implementation. The
strangler migration, the six open spec decisions, and the full rationale live in
the [ADR](../adr/3.x/2026-07-11-1-doctrine-controlled-transition-gates.md). Until
the migration lands, transition gates remain hardcoded as described in
[Kanban Workflow](kanban-workflow.md).

## See also

- [Kanban Workflow](kanban-workflow.md) — the lane model and today's transition guards.
- [The Mission System](mission-system.md) — mission types, step contracts, and guards.
- [Doctrine relationships](doctrine-relationships.md) — how the DRG models edges.
- [Understanding Charter: Synthesis, DRG, and Governed Context](charter-synthesis-drg.md) — activation and DRG selection.
