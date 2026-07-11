---
work_package_id: WP14
title: F(48) composed-action guard selection-inversion
dependencies:
- WP03
- WP04
requirement_refs:
- FR-002
- C-002
- FR-013
tracker_refs:
- '2535'
- '2531'
planning_base_branch: design/doctrine-controlled-gates
merge_target_branch: design/doctrine-controlled-gates
branch_strategy: Planning artifacts for this mission were generated on design/doctrine-controlled-gates. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into design/doctrine-controlled-gates unless the human explicitly redirects the landing branch.
subtasks:
- T060
- T061
- T062
- T063
phase: Lane E - Consumer inversions
assignee: ''
agent: ''
history:
- event: created
  at: '2026-07-11T00:00:00Z'
  note: Prompt generated via /spec-kitty.tasks
agent_profile: python-pedro
authoritative_surface: src/runtime/next/runtime_bridge.py
execution_mode: code_change
owned_files:
- src/runtime/next/runtime_bridge.py
create_intent: []
role: implementer
tags: []
task_type: implement
---

# Work Package Prompt: WP14 – F(48) composed-action guard selection-inversion

## Objective

Invert the **selection** side of the composed-action post-task guard
(`_check_composed_action_guard`, `runtime_bridge.py:1515`, radon complexity
**F(48)**) onto the SSOT selection seam `resolve_gates`, so that both runtime
consumers now obtain their gate set from the **one** code path — **while keeping
the guard's own fail-closed reduction unchanged**. A missing spec/plan/tasks
still hard-blocks; it is **not** routed through the FR-014 fail-open reducer
(that would silently downgrade its hard-blocks to warns — SC-010).

Because this is the **final** consumer inversion, this WP also carries the
joint **NFR-005 / SC-004 proof**: adding a gate to a transition is a
doctrine-only edit, and *both* consumers (the WP13 move-task hook and this
guard) select through the single seam.

## Context

**Mission**: `doctrine-controlled-gates-01KX81KR` · **Epic**: #2535 · **Coordinates with #2531**

**The two-consumer problem this WP finishes closing (research §0).** There are
exactly two runtime consumers that decide "does a check run on this transition":
the move-task pre-review hook (inverted in WP13) and this composed-action guard.
The forensic finding (paula-patterns): these two files have **never co-changed**
and have **independent test harnesses**. If they resolve selection separately,
they *will* drift — and **NFR-005 ("adding a gate is a doctrine-only edit") is
unprovable** unless both route *selection* through the same seam. WP13 inverted
the first; this WP inverts the second and lands the joint proof.

**Why selection only, and why fail-closed reduction stays.** The two consumers are
**different gate-classes**:
- The move-task hook is a fail-**open** test-regression `GateVerdict` keyed on the
  lane `for_review` — it uses the FR-014 reducer (`run_gate`).
- This composed-action guard is a fail-**closed** artifact-presence check keyed on
  the **action** (`specify`/`plan`/`tasks`/…). It returns `list[str]` and
  hard-blocks on missing spec/plan/tasks (consumed at `runtime_bridge.py:1783`,
  where a non-empty `failures` list refuses the step).

They **share one selection authority** (`resolve_gates` + the lane↔action adapter)
but keep their **own reduction**. Routing this guard through `run_gate`'s "only
regression blocks" reducer would silently downgrade its hard-blocks to warns —
**SC-010 forbids that**. So this WP shares *selection* only.

**The anti-drift-insurance nature of this inversion (plan Notes item 6).** This
mission binds only the pre-review gate (FR-013). `resolve_gates` therefore returns
`[]` for this guard's `(mission, action)` keys **today** — no gate is bound on
`specify`/`plan`/`tasks` this mission. The inversion is therefore **anti-drift
insurance**, NOT a replacement of the guard's hardcoded missing-artifact check.
The hardcoded artifact-presence check **stays and stays fail-closed**; the seam is
threaded in *alongside* it so that when a future gate *is* bound to one of these
actions, both consumers already select through the one path. SC-010 (fail-closed
hard-blocks preserved) is the acceptance criterion.

**The #2531 coordination hazard (critical).** `runtime_bridge.py` is a 3813-LOC
god-module with 30 historical bug-fixes, and `_check_composed_action_guard` is the
exact F(48) function that **#2531** (concurrent `runtime_bridge` decomposition,
superseding the closed #2116) is also decomposing. This is an **owned-file
collision on the same function**. Before landing:
- Do a `git fetch` + `git rev-parse` / `git log <base>..origin/<their-branch>`
  check to see whether #2531 has moved `_check_composed_action_guard` (renamed,
  extracted, relocated). A stale-lane-base merge here can clobber their rebased
  file (memory: gate-substrate mission — stale-lane-base merge clobbers rebased
  files).
- Rebase onto the current tip before final push; if a `(stale info)`
  force-with-lease rejection appears, fetch and inspect `mybase..origin/branch`,
  cherry-pick unseen commits, then push (memory: force-with-lease rejection).
- Keep the diff **surgical**: touch only the selection-read inside
  `_check_composed_action_guard` and its immediate wiring. Do **not** attempt the
  broader degod — that is #2531's scope (spec.md Out of Scope). Minimizing the
  diff is the primary collision-avoidance tactic.

## Branch Strategy

- **Planning base**: `design/doctrine-controlled-gates`.
- **Final merge target**: `design/doctrine-controlled-gates`.
- **Execution worktree**: allocated from `lanes.json` at implement time. Depends
  on WP03 + WP04 (claimable once both are `approved`/`done`).
- **Co-ownership**: `runtime_bridge.py` is exclusive to this WP *within this
  mission*, but concurrently edited by #2531 in another stream — rebase/rev-parse
  check before landing (see Context).

## Ordered Steps

### T060 — Invert `_check_composed_action_guard` selection onto `resolve_gates`

**Purpose**: Make the guard obtain its gate *selection* from the seam instead of
(only) its internal hardcoded `(mission, action)` `if/elif`, without changing what
it blocks on.

**Steps**:
1. **Extract-then-inject, never edit-in-place** (research §0/§5, contract Migration
   discipline). Do the characterization capture in T062 **first**; only then thread
   the seam in.
2. Inside `_check_composed_action_guard` (`runtime_bridge.py:1515`), add a call to
   `resolve_gates(mission, action, activation)` using the **action** key (this
   consumer keys on action, per the lane↔action adapter table in
   `contracts/gate-resolution-seam.md`). The seam matches bindings whose
   `binding.transition == action`.
3. This mission binds no gate to these actions (FR-013) → `resolve_gates` returns
   `[]`. Handle `[]` as "no doctrine-selected gate for this action" — which does
   **not** clear the existing hardcoded artifact-presence check; the two are
   additive. The hardcoded check continues to run and continues to return its
   `list[str]` of missing-artifact failures.
4. Obtain the `ActivationState` from the mission's already-resolved charter
   activation — do **not** build a parallel activation read (C-001, single
   selection authority).
5. Keep the function's signature and return type `list[str]` unchanged (consumed
   at `:1783`).

**Guardrails**: **Selection only.** You are threading in the shared selection
read; you are **not** replacing or weakening the artifact-presence check. If a
future gate is bound to `specify`/`plan`/`tasks`, this seam read is where it will
be picked up — but that reduction path (for any doctrine-selected *test/verdict*
gate on these actions) is out of scope for this mission and must not alter the
artifact guard's fail-closed behavior.

### T061 — Keep its fail-closed reduction — missing spec/plan/tasks still hard-blocks

**Purpose**: Guarantee SC-010 — the guard's fail-closed hard-blocks survive the
inversion.

**Steps**:
1. The artifact-presence reduction stays **inside** `_check_composed_action_guard`
   and stays fail-closed: a missing spec/plan/tasks still appends to `failures`
   and the caller at `:1783` still refuses the step on a non-empty list.
2. Do **NOT** route this guard through `run_gate` / the FR-014 reducer
   (`review/gates/outcomes.py`). That reducer is for **test/verdict** gates and
   only lets `regression(blocking=true)` block — passing an artifact-presence
   failure through it would downgrade a hard-block to a FAULT_WARN, violating
   SC-010. The guard shares *selection* only (contract §Reduction, seam invariant
   5 exception).
3. Any doctrine-selected gate that `resolve_gates` *would* return for an action
   (none this mission) is additive to — never a substitute for — the artifact
   check. The artifact check is not gated behind the seam returning something.

**Guardrails**: The FR-014 reducer must not appear anywhere in this guard's code
path. SC-010 is the acceptance test: a missing-artifact case still blocks, not
downgraded to a warn.

### T062 — Characterization tests on the `(mission, action)` guard matrix before + after

**Purpose**: Prove behavior is unchanged by the inversion — the F(48) god-function
is the single highest-regression site in the mission (research §5).

**Steps**:
1. **Before** touching `_check_composed_action_guard`, write characterization
   tests that pin its current behavior across the live `(mission, action)` matrix:
   for each `(mission, action)` combination the guard handles, capture whether it
   returns failures and which. Use realistic mission/action inputs and real
   artifact-presence states (present vs missing spec/plan/tasks) — not degenerate
   stubs.
2. Run them green against the **pre-inversion** code (they characterize current
   behavior).
3. Perform the T060/T061 inversion.
4. Run the **same** characterization tests — they must stay green (behavior
   unchanged). Any diff in the `(mission, action)` → `failures` mapping is a
   regression to fix, not to re-baseline.

**Guardrails**: These tests are the safety net for the F(48) edit. Pin
**behavioral** invariants (the `(mission, action)` → block/allow matrix), not the
literal `if/elif` shape (memory: refactor-stable arch tests) — #2531 will
restructure the internals and these tests must survive its decomposition too.

### T063 — NFR-005 / SC-004 proof: adding a gate is doctrine-only; both consumers select through the one seam

**Purpose**: Land the joint proof that lives in the final consumer-inversion WP
(plan Notes item 3) — provable only after **both** consumers route selection
through the seam (WP13 done + this WP).

**Steps**:
1. Write a test that adds a gate to a transition using **doctrine artifacts only**
   — a step-contract binding + a handler/asset — and observes it fire through the
   `resolve_gates` shared seam, with **no** edit to `specify_cli`/`runtime`
   gate-decision control flow (NFR-005).
2. Assert both consumers now select through the one seam: the move-task hook
   (WP13) and this guard both obtain their gate set from `resolve_gates` — there is
   no second binding-read + activation path for gate *selection* (seam invariant 1).
   A structural assertion (single selection call site) plus the behavioral
   doctrine-only-extension test together discharge SC-004.
3. SC-004: adding a new gate to a transition requires only doctrine edits (binding
   + handler/asset); no `specify_cli` gate-decision code changes via the shared
   seam. Demonstrate via the doctrine-only fixture from step 1.

**Guardrails**: This proof is **unprovable** until both consumers are inverted, so
it belongs here (the final inversion), not in WP03. Do not attempt it before WP13
is `approved`/`done`.

## Acceptance

- **NFR-005**: doctrine-only extensibility — a gate added to a transition via
  doctrine artifacts only fires through the shared `resolve_gates` seam, with no
  edit to gate-decision control flow. *(T063)*
- **SC-004**: adding a new gate to a transition requires only doctrine edits; no
  `specify_cli` gate-decision code changes (via the FR-002 shared seam). *(T063)*
- **SC-010**: the composed-action artifact-presence guard's fail-closed
  hard-blocks (e.g. missing spec/plan/tasks) are **preserved** after it adopts
  shared selection — a missing-artifact case still blocks, not downgraded to a
  warn. *(T061/T062)*
- **FR-002 / C-002**: the guard shares *selection* only through the one seam and
  keeps its fail-closed reduction; fail-open is not imposed on it, and its
  hard-block is not weakened. *(T060/T061)*
- Characterization matrix green before **and** after (T062).
- `runtime_bridge.py` diff is surgical (selection read + wiring only), rebased onto
  the current tip with a #2531 rev-parse check; `ruff`/`mypy` clean with zero new
  suppressions; complexity does not grow (the `# noqa: C901` at `:1515` must not
  become a larger F-number — prefer a small extracted helper for the seam read).

## Safeguards

- **`runtime_bridge.py` is EXCLUSIVE to this WP within the mission — but co-edited
  by #2531.** Do a `git fetch` + `git rev-parse` / `git log <base>..origin/<#2531-branch>`
  check before landing; rebase onto the current tip; keep the diff surgical. A
  stale-lane-base merge can clobber #2531's rebased file. On a force-with-lease
  `(stale info)` rejection: fetch, inspect `mybase..origin/branch`, cherry-pick
  unseen commits, then push.
- **Selection-only inversion.** Thread `resolve_gates` in for *selection*; do
  **not** route the guard through the FR-014 reducer (`run_gate`). SC-010 depends
  on this — the artifact-presence hard-block must not become a warn.
- **Fail-closed reduction stays.** Missing spec/plan/tasks still hard-blocks
  (`list[str]` → refused at `:1783`). This guard is a different gate-class from the
  fail-open pre-review hook; do not "unify" their reductions (contract Non-goals).
- **Anti-drift insurance, not a replacement.** `resolve_gates` returns `[]` for
  these actions this mission (FR-013); the hardcoded artifact check is untouched.
  Do not delete or weaken it on the theory that the seam "handles it now" — it does
  not this mission (plan Notes item 6).
- **Extract-then-inject, characterization first.** Never edit the F(48) function
  in place without the T062 before-capture. Pin behavioral invariants, not the
  literal `if/elif` shape, so the tests survive #2531's decomposition.
- **Final-inversion proof.** NFR-005/SC-004 lives here because it is only provable
  once both consumers select through the seam — do not push it upstream to WP03.
- **No branch-switch during background test runs**; respect per-worker HOME
  isolation.

## References

- `src/runtime/next/runtime_bridge.py:1515` — `_check_composed_action_guard`
  (F(48), `# noqa: C901`) — the selection-inversion target.
- `src/runtime/next/runtime_bridge.py:1783` — the consumption site where a
  non-empty `failures` list hard-blocks the step (fail-closed reduction to
  preserve).
- `src/specify_cli/cli/commands/agent/tasks_move_task.py:996` —
  `_mt_run_pre_review_gate`, the *other* consumer (inverted in WP13) — reference
  for the two-consumer NFR-005 proof.
- `src/specify_cli/review/gates/resolver.py` — `resolve_gates` (WP03 seam; key on
  **action** here, returns `[]` this mission).
- `src/specify_cli/review/gates/outcomes.py` — `run_gate` / FR-014 reducer (WP04)
  — **explicitly NOT used by this guard** (SC-010).
- `contracts/gate-resolution-seam.md` — lane↔action adapter table (composed-action
  guard row), §Reduction (fail-closed exception), invariants 1 & 5, Migration
  discipline (coordinate with #2531).
- `spec.md` FR-002; C-002; SC-004, SC-010; NFR-005; Out of Scope (#2531 degod
  boundary).
- `research.md` §0 (two-consumer drift / single selection authority), §5 item 1
  (runtime_bridge F(48) highest regression risk; coordinate #2531).
- `plan.md` Notes-for-/tasks items 3 (proof lives in final inversion) & 6
  (artifact-guard anti-drift watch-item).

## Activity Log

- (append implement/review events here)
