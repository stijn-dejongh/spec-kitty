---
work_package_id: WP03
title: SSOT gate-selection seam (keystone)
dependencies:
- WP01
requirement_refs:
- FR-002
- FR-003
- FR-006
- C-001
- C-005
tracker_refs:
- '2535'
planning_base_branch: design/doctrine-controlled-gates
merge_target_branch: design/doctrine-controlled-gates
branch_strategy: Planning artifacts for this mission were generated on design/doctrine-controlled-gates. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into design/doctrine-controlled-gates unless the human explicitly redirects the landing branch.
subtasks:
- T011
- T012
- T013
- T014
- T015
phase: Lane B - Selection seam
history:
- at: '2026-07-11T00:00:00Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: python-pedro
authoritative_surface: src/specify_cli/review/gates/
execution_mode: code_change
owned_files:
- src/specify_cli/review/gates/resolver.py
- src/specify_cli/review/gates/__init__.py
create_intent:
- src/specify_cli/review/gates/resolver.py
- src/specify_cli/review/gates/__init__.py
role: implementer
tags: []
task_type: implement
---

# Work Package Prompt: WP03 — SSOT gate-selection seam (keystone)

## Objective

Build the **single SSOT gate-*selection* seam** — `resolve_gates(mission_id, transition, activation) -> list[ResolvedGate]` — the one and only place in the codebase that reads step-contract gate bindings and applies charter activation to decide **which** gates fire on a transition. This is the keystone both runtime consumers (the `move-task` pre-review hook and the composed-action guard) depend on for gate *selection*.

**Scope discipline (read this twice):** this WP delivers **selection ONLY**. It does NOT reduce verdicts, does NOT run gates, does NOT fold faults into operator outcomes — that is WP04 (`outcomes.py` / `run_gate`), a per-gate-class reduction boundary that depends on this WP. This WP also does NOT invert either consumer onto the seam — that is Lane E (WP13 move-task hook, WP14 the F(48) guard). Here we **extract-then-inject**: build the seam behind characterization tests, ship a dispatch `Protocol`, and stop. No consumer edits.

## Context

**Mission**: `doctrine-controlled-gates-01KX81KR` · **Epic**: #2535 · **Branch**: `design/doctrine-controlled-gates`

**Why this WP is the keystone.** Today there are **two independent runtime consumers** that each decide "does a check run on this transition," wired completely separately (research §0):

1. **The `move-task` pre-review hook** — `_mt_run_pre_review_gate` in `src/specify_cli/cli/commands/agent/tasks_move_task.py:996`, gated by the literal `if st.target_lane != Lane.FOR_REVIEW: return` at `:1012`, folding faults to `no_coverage` at `:905-909`. It keys on **lane** (`for_review`).
2. **The composed-action post-task guard** — `_check_composed_action_guard` in `src/runtime/next/runtime_bridge.py:1515`, a hardcoded `if/elif` on `(mission, action)` at radon complexity **F(48)** (already `# noqa: C901`). It keys on **action** (`specify`/`plan`/`tasks`/…).

The forensic finding (paula-patterns, research §0): these two files have **never co-changed** and have **independent test harnesses**. If the mission rewires them separately to consult step-contract bindings, the two selectors *will* drift — NFR-005 ("adding a gate is a doctrine-only edit") becomes unprovable. The fix is **one selection authority** both consumers trust: this seam.

**Critical nuance — selection is shared; reduction is NOT.** The two consumers are semantically different gate-classes. The pre-review hook is a fail-**open** test-regression `GateVerdict` gate; the composed-action guard is a fail-**closed** artifact-presence check that returns `list[str]` and hard-blocks on missing spec/plan/tasks. They share **one selection authority** (this seam); each keeps its **own reduction**. Routing the artifact guard through the test-gate "only regression blocks" reducer would silently downgrade its hard-blocks (SC-010). This WP therefore ships selection only and defines — but does not unify — reduction.

**Dependency reality (why Lane A ships first).** `ResolvedGate.binding` is a `GateBinding`, which lives in `src/doctrine` (WP01) and is arch-gated: `src/doctrine` MUST NOT import `specify_cli`. This resolver **imports `GateBinding` from `src/doctrine`** — so Lanes A and B are NOT independent. WP01 ships the `GateBinding` model first; this WP depends on it.

## Branch Strategy

- **Planning base**: `design/doctrine-controlled-gates`.
- **Final merge target**: `design/doctrine-controlled-gates`.
- **Execution worktree**: allocated from `lanes.json` at implement time.

## Ordered Steps

Work the subtasks in order. T014 (characterization) is **red-first** and lands **before** T011's production logic settles — it is the safety net that proves the extraction preserves the live `(mission, action)` selection matrix.

### T014 (red-first, do FIRST) — Characterization tests on the current `(mission, action)` selection matrix

**Purpose**: Pin the *current* selection behavior of both consumers before any code moves. This is the extract-then-inject baseline: prove what selection produces today, so the seam can be shown to reproduce it.

1. Enumerate the live matrix the two consumers select over:
   - The move-task pre-review hook: the only transition that selects a check today is lane `for_review` (`tasks_move_task.py:1012` literal `target_lane != Lane.FOR_REVIEW: return`). Every other lane selects nothing.
   - The composed-action guard: the `(mission, action)` pairs enumerated in `_check_composed_action_guard` (`runtime_bridge.py:1515`) — the `specify`/`plan`/`tasks` artifact-presence checks. Characterize which `(mission, action)` pairs trigger a guard today (do NOT change behavior — this is a read-only census of the current branch matrix).
2. Write characterization tests that assert, per matrix cell, the **current** selection result (fires / does not fire). These tests describe the *pre-seam* world; they are the golden baseline the new seam must reproduce for the pre-review exemplar and must return `[]` (no binding this mission) for the composed-action action keys.
3. These tests live under the seam's test surface (e.g. `tests/contract/gates/` or `tests/unit/review/gates/`). They MUST fail-to-green only once `resolve_gates` reproduces the pre-review lane-`for_review` selection; the composed-action action keys are expected to resolve to `[]` (anti-drift insurance — FR-013 binds only the pre-review gate this mission).

**Red-first proof**: run the characterization tests against the branch tip BEFORE writing `resolve_gates` and confirm they encode current behavior (the `resolve_gates`-driven assertions are red because the function does not exist yet).

### T011 — `resolver.py`: `resolve_gates(mission, transition, activation)` with the lane↔action adapter

**Purpose**: The single selection call site.

1. Create `src/specify_cli/review/gates/resolver.py`. Define:
   ```
   def resolve_gates(mission_id: str, transition: str, activation: ActivationState) -> list[ResolvedGate]
   ```
2. **Read bindings — enumerate steps, match by `binding.transition`.** Use `MissionStepContractRepository` (`src/doctrine/missions/step_contracts.py:159-170`) to enumerate the mission's step-contract steps. Then select bindings whose declared `binding.transition == transition`.
   - **DO NOT call `get_by_action(mission, "for_review")`.** A lane (`for_review`) is not an action — `get_by_action` matches `contract.action`, so `get_by_action(mission, "for_review")` returns `None`. `get_by_action` is used only to *enumerate* a mission's step-contract steps; bindings are then matched by their declared `transition` field. This is the lane↔action adapter: lane keys (`for_review`) and action keys (`implement`/`specify`/…) share one `transition` namespace on the binding.
   - Adapter table (from `contracts/gate-resolution-seam.md`):

     | Consumer | `transition` key passed | resolves to |
     |----------|-------------------------|-------------|
     | move-task pre-review hook | lane `for_review` | bindings with `transition: for_review` (the pre-review exemplar's built-in binding, added in WP02) |
     | composed-action guard | action (`specify`/`plan`/`tasks`/…) | bindings with `transition: <that action>` (none bound this mission — FR-013; returns `[]`) |
3. **Deterministic + ordered.** Same inputs → the same ordered list, stable across processes. Sort by a stable key (e.g. declaring step-contract node id, then binding index) — never rely on dict/set iteration order.
4. **Empty is a real answer, never "clean".** Return `[]` when nothing is declared/active. `[]` means "nothing to select here" → the caller (WP04/consumers) renders `CALM_NOTICE`. `[]` is NEVER `PASS`/`no_new_failures`. Document this on the function.

### T012 — Apply charter activation on the owning step-contract node; return ordered `ResolvedGate`

**Purpose**: Only gates whose declaring doctrine is charter-active fire (FR-003/FR-006/C-001).

1. Apply charter activation via the existing machinery — `filter_graph_by_activation` (`src/charter/drg.py:319`) — **on the owning step-contract node**, the activatable unit. Activation is evaluated on the step-contract node, NOT on the asset/handler URN: `asset`/`gate-handler` are absent from the DRG singular↔plural kind maps (`_SINGULAR_TO_PLURAL`, `src/charter/drg.py:187`), so filtering on those URNs would **default-allow** (see `drg.py:313` — malformed/absent → bypass). A gate is active iff its declaring step contract is charter-active. This is the FR-006 correction.
2. For each surviving binding, build a `ResolvedGate` (data-model.md):
   - `binding`: the source `GateBinding` (imported from `src/doctrine`) — `mechanism` (`handler|asset`) and `on_unrunnable` live inside it.
   - `declaring_doctrine`: the doctrine node id — exactly what FR-018/SC-008 observability (WP05) reads.
   - `dispatch`: the resolved target (`HandlerRef | AssetRef`) — resolution of the URN to a dispatchable target. The actual handler/asset *implementations* land in WP08/WP10; here `dispatch` carries the ref + mechanism so a later `run_gate` can pick the arm.
   - `activation_state`: `active | inactive | refused`. This WP sets `active` for surviving bindings; `inactive`/`refused` states are populated as observability needs them (WP05 reads them; trust `refused` is set by the Path-B runner in Lane D). Model the enum fully now.
3. Return the ordered `list[ResolvedGate]`.

### T013 — Define the handler/asset dispatch **Protocol** (implemented later by WP08/WP10)

**Purpose**: The seam is the contract both dispatch arms plug into; it must define the Protocol without importing either implementation (forward-only — Notes-for-/tasks #2).

1. Define a `typing.Protocol` (structural) for gate dispatch — the shape a Path-A handler (`run(ctx: TransitionContext) -> GateVerdict`, WP08) and a Path-B asset runner (WP10) both satisfy. Ground the `TransitionContext` / `GateVerdict` shapes in data-model.md (one `TransitionContext`, one `GateVerdict`; both dispatch paths share them).
2. This Protocol is **declaration only** in this WP. `run_gate` (WP04) selects the arm by `binding.mechanism` and dispatches through the Protocol. Do NOT import `handlers/pre_review.py` (WP08) or `assets/runner.py` (WP10) — they do not exist at this WP's time; importing them would make `run_gate`'s DoD circular. The Protocol is the seam; the arms implement it forward.
3. Keep the Protocol minimal and stable — it is a published contract surface both later WPs code against.

### T015 — Contract tests: determinism, empty≠clean, single selection call site

**Purpose**: Assert the seam's invariants (from `contracts/gate-resolution-seam.md` §Invariants).

1. **Determinism** (Invariant 2): repeated `resolve_gates` on a fixed fixture returns a byte-identical ordered result. Assert list equality across repeated calls (and, if practical, across a re-import to catch iteration-order leakage).
2. **Empty ≠ clean** (Invariant 3): `resolve_gates` returning `[]` is the CALM_NOTICE signal, never `PASS`. Assert the empty result is distinguishable from a "verified clean" result (there is no PASS at selection time — PASS is a reduction outcome owned by WP04).
3. **Single selection authority** (Invariant 1): assert that the pre-review lane selection and the composed-action action selection both flow through `resolve_gates` — i.e. there is exactly one function that reads bindings + applies activation for *selection*. (The consumer inversions that make this literally true land in WP13/WP14; here assert the seam is the sole binding-read+activation path in `review/gates/`, with a test that would fail if a second selection function were introduced.)
4. Package init: create `src/specify_cli/review/gates/__init__.py` exporting `resolve_gates`, `ResolvedGate`, and the dispatch `Protocol` as the package's public selection surface. Keep the export list tight — the reducer (`run_gate`/`outcomes`) is exported by WP04, not here.

## Acceptance

This WP is done when the following contract invariants hold (grounded in `contracts/gate-resolution-seam.md` and data-model.md). Its NFR-005 *proof* is deferred to WP14 (provable only once BOTH consumers route selection through the seam) — do not claim NFR-005 here.

- **Determinism**: `resolve_gates` on a fixed fixture is byte-identical and ordered across repeated calls and processes.
- **`[]` → CALM_NOTICE, empty ≠ clean**: an empty selection is never `PASS`/`no_new_failures`; it is the "nothing declared/active" signal the caller renders as CALM_NOTICE.
- **Single selection call site**: `resolve_gates` is the only place in `review/gates/` that reads step-contract bindings and applies charter activation for selection. No parallel selector.
- **Lane↔action adapter is correct**: selection matches `binding.transition == key`; the code never calls `get_by_action(mission, "for_review")` (a lane is not an action → `None`). `get_by_action` is used only to enumerate steps.
- **Activation on the owning step-contract node**: uses `filter_graph_by_activation` on the step-contract node (the activatable unit), NOT the `asset`/`gate-handler` URN (which default-allows — FR-006).
- **Selection ONLY**: no verdict reduction, no gate execution, no fault-folding in this WP. The dispatch `Protocol` is declared but no arm is imported/implemented here.
- **Characterization baseline green**: the T014 characterization matrix (pre-review `for_review` fires; composed-action action keys resolve to `[]`) passes through the new seam.
- `ruff`/`mypy` clean on `resolver.py` + `__init__.py`; no `# noqa`/`# type: ignore` added; every new branch/helper has a focused test in this PR (Sonar new-code coverage).

## Safeguards

- **Selection ONLY — reduction is WP04.** Do not fold faults, do not run gates, do not build the FR-014 mapping here. `run_gate`/`outcomes.py` is WP04's owned surface and depends on this WP.
- **The lane↔action adapter reads by `binding.transition`, NOT `get_by_action("for_review")`.** A lane is not an action; `get_by_action(mission, "for_review")` returns `None`. Use `get_by_action` only to enumerate a mission's step-contract steps, then match bindings by their declared `transition`.
- **Activation on the step-contract node, not the URN.** `asset`/`gate-handler` URNs are absent from `_SINGULAR_TO_PLURAL` (`drg.py:187`) and default-allow — gating on them is a silent no-op. Filter on the owning step-contract node (FR-006). WP02 extends the kind-map + regenerates the DRG so this activation is real; this WP consumes it.
- **Extract-then-inject, never edit-in-place.** Characterization tests (T014) on the current `(mission, action)` matrix come FIRST. Do NOT edit `_check_composed_action_guard` (F(48), `runtime_bridge.py:1515`) or the move-task hook in this WP — that inversion is WP14/WP13. Editing F(48) in place is explicitly the wrong move (highest-regression site, coord #2531).
- **Import `GateBinding` from `src/doctrine`.** Do NOT redefine it in `specify_cli`. The `src/doctrine` → no-`specify_cli`-import arch gate stays green because the dependency direction is `specify_cli` → `doctrine`, never the reverse.
- **Dispatch Protocol is forward-only.** Declare it; do not import WP08/WP10 implementations (they don't exist yet — circular DoD otherwise).
- **Do NOT unify reduction.** The artifact-presence guard keeps fail-closed semantics (FR-002/SC-010); this seam gives it *selection* only.

## References

- **Seam contract**: `contracts/gate-resolution-seam.md` (interface, adapter table, invariants) — the keystone spec for this WP.
- **Verdict/outcome contract**: `contracts/gate-verdict-and-outcomes.md` (for the `GateVerdict`/`TransitionContext` shapes the Protocol references; reduction itself is WP04).
- **Data model**: `data-model.md` — `GateBinding`, `ResolvedGate`, `TransitionContext`, `GateVerdict`, `OperatorOutcome`.
- **Research §0**: the SSOT selection-seam mandate (why one selection authority; extract-then-inject; own WP before consumer inversions).
- **Move-task consumer (do NOT edit here)**: `_mt_run_pre_review_gate` `tasks_move_task.py:996`; lane gate `:1012`; fault-fold `:905-909`.
- **Composed-action consumer (do NOT edit here)**: `_check_composed_action_guard` `runtime_bridge.py:1515` (F(48); coord #2531).
- **Activation machinery (reuse unchanged)**: `filter_graph_by_activation` `src/charter/drg.py:319`; kind-map `_SINGULAR_TO_PLURAL` `drg.py:187` (WP02 extends it).
- **Binding read**: `MissionStepContractRepository.get_by_action` `src/doctrine/missions/step_contracts.py:159-170` (enumerate steps; match by `binding.transition`).
- **Verdict tail (reused later by WP08, referenced for the Protocol shape)**: `evaluate_with_scope` `src/specify_cli/review/pre_review_gate.py:451-511`.
