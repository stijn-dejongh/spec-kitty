---
work_package_id: WP05
title: Observability surface
dependencies:
- WP03
requirement_refs:
- FR-018
tracker_refs:
- '2535'
planning_base_branch: design/doctrine-controlled-gates
merge_target_branch: design/doctrine-controlled-gates
branch_strategy: Planning artifacts for this mission were generated on design/doctrine-controlled-gates. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into design/doctrine-controlled-gates unless the human explicitly redirects the landing branch.
subtasks:
- T021
- T022
- T023
phase: Lane B - Observability
history:
- at: '2026-07-11T00:00:00Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: python-pedro
authoritative_surface: src/specify_cli/review/gates/
execution_mode: code_change
owned_files:
- src/specify_cli/review/gates/observe.py
- src/specify_cli/cli/commands/agent/gates_status.py
create_intent:
- src/specify_cli/review/gates/observe.py
- src/specify_cli/cli/commands/agent/gates_status.py
role: implementer
tags: []
task_type: implement
---

# Work Package Prompt: WP05 — Observability surface

## Objective

Give operators a **read-only** way to answer, for a given transition: **which gates are active, from which declaring doctrine, and why each did or did not run** (active / inactive / refused / faulted) — without reading `specify_cli` source. This is a thin observability layer **over the SSOT selection seam** (WP03), plus a light read-only CLI surface. No heavy new CLI, no new decision logic.

## Context

**Mission**: `doctrine-controlled-gates-01KX81KR` · **Epic**: #2535 · **Branch**: `design/doctrine-controlled-gates`

**Why this exists (FR-018/SC-008).** With gate selection moved into doctrine + charter activation, an operator can no longer read the hardcoded `if/elif` to see what fires. They need a first-class answer to "what gates apply to `for_review` here, and why did/didn't each one run?" — active, inactive, refused, or faulted — expressed in operator terms, naming **no** spec-kitty-internal module. This closes the observability gap the strangler opens.

**This is glue, not core (tiered rigour).** It reads the resolver; it derives nothing new. The `ResolvedGate` shape already carries exactly what FR-018 needs: `declaring_doctrine` (which doctrine) and `activation_state` (`active | inactive | refused`). The "faulted" dimension is the outcome the WP04 reducer produces at run time — observability reports the *last/expected* disposition per gate, sourced from selection state, not by re-running gates.

**Depends on WP03 only** (parallel with WP04, per the subtask index: T021-T023 run ∥ WP04). It reads `resolve_gates` / `ResolvedGate`; it does NOT depend on the reducer for its selection view.

## Branch Strategy

- **Planning base**: `design/doctrine-controlled-gates`.
- **Final merge target**: `design/doctrine-controlled-gates`.
- **Execution worktree**: allocated from `lanes.json` at implement time.

## Ordered Steps

### T021 — `observe.py`: which gates active for a transition, declaring doctrine, why ran/didn't

**Purpose**: The read model over the resolver.

1. Create `src/specify_cli/review/gates/observe.py`. Implement a pure read function, e.g.:
   ```
   def describe_gates(mission_id: str, transition: str, activation: ActivationState) -> GateObservation
   ```
   that calls `resolve_gates` (WP03) and projects each `ResolvedGate` into an operator-facing observation row:
   - **which gate** (the binding's gate ref / mechanism `handler|asset`, in operator terms — not the raw internal URN dump);
   - **declaring doctrine** (`ResolvedGate.declaring_doctrine` — FR-018 "from which doctrine");
   - **why it will/won't run** (`ResolvedGate.activation_state`: `active` / `inactive` / `refused`), plus the "faulted" disposition where a run-time fault applies. Map the four operator-visible reasons: **active** (declared + charter-active → will run), **inactive** (declared but doctrine not charter-active → won't run), **refused** (trust envelope refuses Path-B execution → won't run), **faulted** (ran but hit an FR-010 fault → ran non-blocking).
2. Also handle the **empty** case explicitly: when `resolve_gates` returns `[]`, the observation states "no gate declared/active for this transition" (the CALM_NOTICE story — FR-008), naming **no** internal module/layout. `[]` here is "nothing configured", never "verified clean".
3. Keep `observe.py` a pure projection — it reads the seam and formats; it does not read bindings itself (single selection authority — WP03) and does not run gates. Operator-facing strings MUST NOT leak `tests.architectural._gate_coverage` / `src/specify_cli/` (SC-001/NFR-002 discipline extends to the observability surface).

### T022 — Expose via a read-only surface (no heavy new CLI; reads the resolver)

**Purpose**: A minimal operator entry point — loopback/local, read-only.

1. Create `src/specify_cli/cli/commands/agent/gates_status.py` — a **read-only** command surface that calls `observe.describe_gates` and renders the observation (e.g. a small table: gate / mechanism / declaring doctrine / disposition). Follow the existing `agent tasks status` command conventions (thin CLI wrapper delegating to the read model). Keep it lightweight — this is a status query, not a new subsystem.
2. **No new decision logic, no mutation, no heavy CLI.** It only reads the seam and prints. No flags that change gate behavior; no execution. Loopback/local only (per WP05 safeguards). Prefer extending the existing `agent tasks status` surface / registering a small sibling command over inventing a broad new CLI group.
3. Resolve the `(mission, transition, activation)` inputs from the current mission context the same way the existing status commands do — do not reconstruct paths the resolver/context should provide.

### T023 — Test SC-008: observability answers active / inactive / refused / faulted

**Purpose**: Prove the four dispositions are answerable without reading source.

1. Tests over `describe_gates` (and a thin smoke test of the CLI surface) asserting each disposition is reported correctly:
   - **active**: a charter-active declared gate (the pre-review exemplar bound at `for_review`) → reported active, with its declaring doctrine.
   - **inactive**: a declared gate whose doctrine is not charter-active → reported inactive (won't run).
   - **refused**: a Path-B gate the trust envelope refuses → reported refused. (Where the full Path-B stack isn't available at this WP's time, drive this via a `ResolvedGate` with `activation_state=refused` — the read model must render it; the end-to-end refusal is exercised in Lane D.)
   - **faulted**: a gate that ran but hit an FR-010 fault → reported faulted (ran non-blocking).
2. Assert the **empty/CALM_NOTICE** case: no declared gate → "not configured", naming no internal module.
3. Assert **no internal leakage**: no observation string contains `tests.architectural._gate_coverage` or `src/specify_cli/`.

## Acceptance

- **SC-008**: an operator can query which gates are active for `for_review`, their declaring doctrine, and why each did/didn't run (active / inactive / refused / faulted) — **without reading source**. Verified by T023 + the read-only CLI surface.
- **Reads the seam, derives nothing**: `observe.py` obtains its gate set only from `resolve_gates` (single selection authority — WP03); it does not re-read bindings or apply activation itself.
- **Read-only, loopback/local**: `gates_status.py` mutates nothing, runs no gate, adds no heavy CLI surface.
- **No internal leakage**: no operator-facing observation string names a spec-kitty-internal module/path.
- **Empty ≠ clean**: the no-gate case reports "not configured" (CALM_NOTICE story), never "verified clean".
- `ruff`/`mypy` clean on `observe.py` + `gates_status.py`; no `# noqa`/`# type: ignore` added; T023 gives the new projection branches focused coverage (Sonar new-code).

## Safeguards

- **Read-only over the resolver.** `observe.py` reads `resolve_gates`; it never re-implements binding-read + activation (that would create a second selection authority — the exact drift WP03 exists to prevent). No mutation, no gate execution anywhere in this WP.
- **No heavy new CLI.** Extend/mirror the existing `agent tasks status` conventions; do not stand up a broad new CLI group or public surface. Loopback/local only.
- **No internal leakage in operator strings.** Observability is a #2534-adjacent surface — the whole point of the mission is that operators never see `tests.architectural._gate_coverage` / `src/specify_cli/`. Hold that line in the projection and the CLI output.
- **Report `refused` without owning the trust logic.** The trust-envelope decision is Lane D (WP11); this WP renders the `refused` disposition, it does not compute it.
- **Depends on WP03 only.** Do not couple observability to the WP04 reducer for its selection view — it runs ∥ WP04.

## References

- **Requirement**: FR-018 (observe which gates active, from which doctrine, why ran/didn't) · **Acceptance**: SC-008.
- **Seam contract**: `contracts/gate-resolution-seam.md` — `resolve_gates` output (`declaring_doctrine` + `activation_state` are "exactly what FR-018/SC-008 observability reads", research §0).
- **Data model**: `data-model.md` — `ResolvedGate` (`declaring_doctrine`, `activation_state ∈ {active,inactive,refused}`), `OperatorOutcome` (the `faulted` disposition source).
- **WP03 read source**: `src/specify_cli/review/gates/resolver.py` + `__init__.py` (`resolve_gates`, `ResolvedGate`).
- **CLI convention to follow**: existing `agent tasks status` surface under `src/specify_cli/cli/commands/agent/` (thin wrapper → read model).
- **No-leakage acceptance lineage**: SC-001 / NFR-002 (#2534 — no `tests.architectural._gate_coverage` / `src/specify_cli/` in operator output).
