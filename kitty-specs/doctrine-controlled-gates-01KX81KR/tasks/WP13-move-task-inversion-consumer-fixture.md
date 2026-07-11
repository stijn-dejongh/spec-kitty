---
work_package_id: WP13
title: Move-task pre-review inversion + consumer fixture
dependencies:
- WP06
- WP08
- WP03
- WP04
requirement_refs:
- FR-002
- FR-011
- FR-008
tracker_refs:
- '2535'
- '2534'
planning_base_branch: design/doctrine-controlled-gates
merge_target_branch: design/doctrine-controlled-gates
branch_strategy: Planning artifacts for this mission were generated on design/doctrine-controlled-gates. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into design/doctrine-controlled-gates unless the human explicitly redirects the landing branch.
subtasks:
- T056
- T057
- T058
- T059
phase: Lane E - Consumer inversions
assignee: ''
agent: ''
history:
- event: created
  at: '2026-07-11T00:00:00Z'
  note: Prompt generated via /spec-kitty.tasks
agent_profile: python-pedro
authoritative_surface: src/specify_cli/cli/commands/agent/pre_review_hook.py
execution_mode: code_change
owned_files:
- src/specify_cli/cli/commands/agent/pre_review_hook.py
- tests/integration/gates/
create_intent:
- src/specify_cli/cli/commands/agent/pre_review_hook.py
- tests/integration/gates/
role: implementer
tags: []
task_type: implement
---

# Work Package Prompt: WP13 – Move-task pre-review inversion + consumer fixture

## Objective

Invert the **move-task pre-review hook** so it obtains its gate set from the
SSOT selection seam (`resolve_gates`) and reduces test-gate outcomes through the
FR-014 reducer (`run_gate`) — instead of calling the hardcoded, spec-kitty-shaped
`pre_review_gate` decision path directly. Then **build the consumer-shaped
regression fixture** that proves a non-spec-kitty repository crosses
`move-task --to for_review` with a calm, non-blocking CALM-NOTICE and **zero**
internal-module leakage (`#2534` closed).

This is the first of the two Lane E consumer inversions. It lands on the clean
surface WP06 opened (the extracted `pre_review_hook.py`) and consumes the seam
WP03 built + the reducer WP04 built + the Path-A handler WP08 migrated.

## Context

**Mission**: `doctrine-controlled-gates-01KX81KR` · **Epic**: #2535 · **Closes (this WP's slice of) #2534**

**Where this sits in the lane graph.** Lane E is the *consumer inversion* lane —
it is where the selection seam actually replaces the hardcoded call sites. There
are exactly two consumers (research §0): the move-task pre-review hook (this WP)
and the composed-action guard (WP14). This WP inverts the first; WP14 inverts the
second and carries the joint NFR-005/SC-004 proof once *both* consumers route
through the one seam.

**Why the ordering of deps matters:**
- **WP06** *extracted* the pre-review hook block out of the 1817-LOC
  `tasks_move_task.py` god-module into a dedicated sibling
  `src/specify_cli/cli/commands/agent/pre_review_hook.py`, **behavior-preserving**.
  WP06 did **not** invert anything — it only relocated the block and re-pointed
  the `tasks.py:427-448` re-export shim. Per plan Notes-for-/tasks item 5, the
  inversion has **exactly one owner: this WP**. Do not let the Path-A lane (WP08)
  or WP06 touch the inversion; WP08 supplied the handler, WP06 supplied the clean
  module, WP13 wires them together at the consumer boundary.
- **WP03** shipped `resolve_gates(mission, transition, activation)` (selection
  only) + the dispatch Protocol; `resolve_gates("…","for_review",…)` returns the
  pre-review exemplar's built-in binding when spec-kitty's own doctrine is active,
  and `[]` (→ CALM_NOTICE) when nothing is declared/active.
- **WP04** shipped `run_gate(resolved, ctx)` (the FR-014 test-gate reducer) — it
  folds every fault class to a non-blocking `OperatorOutcome` and only lets a
  valid `regression(blocking=true)` BLOCK.
- **WP08** shipped the Path-A pre-review handler
  (`review/gates/handlers/pre_review.py`) that reuses `evaluate_with_scope`
  unchanged and is bound in the built-in step contract on `transition: for_review`.

**The pre-inversion call site (ground truth).** The hook today (pre-WP06, now
relocated into `pre_review_hook.py`) is `_mt_run_pre_review_gate`
(`tasks_move_task.py:996` before extraction) gated by the literal
`if st.target_lane != Lane.FOR_REVIEW: return`, calling `pre_review_gate.evaluate_*`
directly and folding faults to `no_coverage`/empty-scope verdicts via
`_mt_empty_scope_verdict` (`tasks_move_task.py:859`) inside a broad `except`
(`:1035`). That fail-open scaffolding **is the FR-010 contract** — it is
preserved verbatim, not deleted; the inversion changes *where the gate set comes
from* and *how faults are reduced*, not *whether faults block*.

**The #2534 defect this fixture proves closed.** In a consumer repo the current
gate imports `tests.architectural._gate_coverage` and assumes
`_SRC_PACKAGE_PREFIX = "src/specify_cli/"`; it runs inert *and* leaks those
internal names into the operator's face. After the inversion, a consumer repo
resolves `[]` from the seam → CALM_NOTICE with no internal name. The consumer
fixture (T058/T059) is the executable proof — it is currently **unowned** (plan
Notes item 4) and is assigned here.

## Branch Strategy

- **Planning base**: `design/doctrine-controlled-gates`.
- **Final merge target**: `design/doctrine-controlled-gates`.
- **Execution worktree**: allocated from `lanes.json` at implement time. This WP
  depends on WP06/WP08/WP03/WP04, so it is only claimable once those are
  `approved` or `done` (dependency gating).

## Ordered Steps

### T056 — Invert the extracted pre-review hook to resolve through `resolve_gates`

**Purpose**: Make `pre_review_hook.py` the single owner of the inversion: the
hook selects its gate set from the seam and stops reading bindings/enablement
itself.

**Steps**:
1. In `pre_review_hook.py`, replace the direct `pre_review_gate.evaluate_*`
   invocation with a call to `resolve_gates(mission_id, "for_review", activation)`.
   Pass the lane key `for_review` (NOT an action) — the lane↔action adapter in
   `resolve_gates` matches bindings whose declared `binding.transition == "for_review"`.
   Do **not** call `get_by_action(mission, "for_review")` yourself (a lane is not
   an action → `None`); the seam owns that adapter.
2. Preserve the existing lane guard semantics: the hook still only engages on the
   `for_review` transition. The `if st.target_lane != Lane.FOR_REVIEW: return`
   short-circuit stays — it is a cheap pre-filter, not a selection decision.
3. Obtain the `ActivationState` the seam needs from the already-resolved charter
   activation for the mission (do not construct a parallel activation read — C-001,
   single selection authority). Thread it in from the move-task state (`_MoveTaskState`).
4. Do **not** re-implement selection or binding-reads in the hook. The hook's job
   after this WP is: pre-filter on lane → ask the seam for the gate set → dispatch
   each `ResolvedGate` via `run_gate` → render the resulting `OperatorOutcome`.

**Guardrails**: This is a **selection** inversion for the hook plus a **reduction**
delegation to `run_gate` (the pre-review gate is a test/verdict gate, so it *does*
route through the FR-014 reducer — unlike WP14's artifact guard). Single owner:
no other WP edits this inversion.

### T057 — Wire Path-A handler dispatch + FR-014 reducer at the move-task boundary; preserve fail-open

**Purpose**: For each selected `ResolvedGate`, dispatch the WP08 Path-A handler
through the WP03 dispatch Protocol and fold the verdict/faults through the WP04
reducer — while keeping the FR-010 fail-open scaffolding intact.

**Steps**:
1. For each `ResolvedGate` returned by `resolve_gates`, call
   `run_gate(resolved, ctx)` (WP04). `run_gate` dispatches the Path-A handler
   (WP08), reuses `evaluate_with_scope`, and returns an `OperatorOutcome`. It
   **never raises** — every fault class is already folded inside it (WP04
   invariant 4).
2. Map the returned `OperatorOutcome` onto the move-task result surface:
   - `BLOCK` (only a valid `regression(blocking=true)`) → the transition is
     refused, exactly as the prior hardcoded `would_block` path did.
   - `FAULT_WARN` / `CALM_NOTICE` / `TRUST_REFUSAL` / `PASS` → the transition
     **proceeds**; render the calm operator message.
3. **Preserve fail-open verbatim.** Keep `_mt_empty_scope_verdict`
   (`tasks_move_task.py:859`) and the broad `except` fold (`:1035`) as the
   outermost belt-and-braces around the whole hook: even if the seam/reducer
   wiring itself throws (it should not — `run_gate` contains faults), the hook
   degrades to a non-blocking outcome. Do **not** narrow or remove this scaffold —
   it *is* the FR-010 contract (research §1). Deleting it is a regression even if
   `run_gate` currently makes it dead-looking; it is the last line of defense.
4. Preserve the `review.fail_on_pre_review_regression` / `review.test_command`
   config semantics — these belong to the WP08 handler now (FR-017), so the hook
   must simply pass the transition context through; do not re-read or re-interpret
   them at the hook layer.

**Guardrails**: The only thing that may BLOCK is a real emitted
`regression(blocking=true)` (C-002/FR-014). A crash, timeout, non-zero exit,
malformed/absent verdict, missing test command, inactive/absent doctrine, or
trust refusal **must** proceed. This is verified end-to-end via the fixture in
T059 and the fault-injection tests owned by WP04 (do not duplicate WP04's
table-driven fault matrix here — assert the consumer-boundary behavior instead).

### T058 — Build the consumer-shaped fixture (non-pytest, no `_gate_coverage.py`)

**Purpose**: Own the SC-001/SC-002/NFR-002 fixture repo — the executable proof
that a repository *without* spec-kitty's test layout crosses `for_review`
cleanly. Currently unowned (plan Notes item 4); assigned here.

**Steps**:
1. Create the fixture under `tests/integration/gates/` (this WP owns the whole
   directory). Build a **real** consumer-shaped repository fixture, NOT a
   monkeypatch of spec-kitty's own tree:
   - **No** `tests/architectural/_gate_coverage.py` module.
   - **Not** a `src/specify_cli/` layout — use a plausible foreign layout
     (e.g. `app/`, `lib/`, or a non-Python project shape). Use realistic,
     production-shaped file names and paths (not `foo/bar.py` placeholders) so the
     fixture exercises real path/scope derivation, not a degenerate stub.
   - **Non-pytest**: the fixture repo declares no pytest layout and no
     `ScopeSource`, so the built-in spec-kitty census ScopeSource (WP07, FR-012)
     is **not** force-applied (FR-009).
2. Give the fixture a mission with a WP in a lane that can cross into `for_review`,
   so the move-task hook actually engages on the transition.
3. Ensure the fixture's active doctrine declares **no** gate on `for_review`
   (nothing charter-active) → `resolve_gates` returns `[]`.
4. Keep the fixture self-contained and hermetic (per-worker HOME isolation
   applies; do not touch the real `~/.spec-kitty`).

**Guardrails**: The fixture must be genuinely consumer-shaped. If it inherits any
spec-kitty-internal module or the `src/specify_cli/` prefix, it does not prove
#2534 closed. This is the load-bearing artifact for NFR-002 — treat its realism as
a correctness requirement, not decoration.

### T059 — Red-first: consumer fixture crossing `for_review` → CALM_NOTICE, zero internal leakage

**Purpose**: The acceptance test. Written **red-first** through the pre-existing
move-task entry point, proving the leak/inert behavior before the inversion and
the CALM_NOTICE after.

**Steps**:
1. Write the test to drive the fixture across `move-task --to for_review` through
   the **real** move-task entry point (the same path an operator hits) — do not
   call `resolve_gates`/`run_gate` directly; the point is the end-to-end consumer
   experience.
2. Assert the transition **proceeds** (non-blocking).
3. Assert the operator output is a single clearly-labelled **CALM_NOTICE**
   ("automated pre-review scope not configured for this repository" per FR-008) —
   `resolve_gates` → `[]` → CALM_NOTICE, and `[]` is NEVER rendered as
   `PASS`/`no_new_failures` (seam invariant 3).
4. Assert **zero** occurrences of `tests.architectural._gate_coverage` or
   `src/specify_cli/` anywhere in the operator-visible output (SC-001/NFR-002,
   seam invariant 6).
5. Red-first discipline: confirm the assertion is genuinely red against pre-WP13
   code (the leak / inert behavior reproduces through the pre-existing entry
   point), then green after the inversion — prove the red, do not assume it.

**Guardrails**: This test closes #2534 for the selection path. It must exercise
the real entry point (not a shortcut), and the leakage assertion is a hard
invariant — a substring match on the internal names, asserted absent.

## Acceptance

- **SC-001**: a consumer repo (no spec-kitty test layout) crossing
  `move-task --to for_review` sees a calm CALM-NOTICE and **zero** occurrences of
  `tests.architectural._gate_coverage` or `src/specify_cli/` in the output
  (#2534 fully closed). *(T058/T059)*
- **SC-002**: the hardcoded pytest assumption is removed from the selection path —
  selection is now doctrine-driven through the seam; the fixture demonstrates a
  non-pytest repo does not get the built-in census force-applied. *(T056/T058)*
- **NFR-002**: consumer-repo portability — the consumer-shaped fixture crossing
  `for_review` produces the FR-008 CALM-NOTICE with none of the internal
  module/path strings. *(T059)*
- **FR-002/FR-011**: the move-task pre-review hook obtains its gate set from the
  single `resolve_gates` seam and the pre-review gate runs as the WP08 Path-A
  handler through it (no direct hardcoded `pre_review_gate` decision call in the
  hook). *(T056/T057)*
- All new/changed code is `ruff` and `mypy` clean with zero suppressions added;
  the extracted hook stays ≤ C(15).

## Safeguards

- **SOLE owner of the hook inversion.** WP06 only *extracted*
  `pre_review_hook.py` (behavior-preserving) and WP08 only *supplied* the handler.
  The inversion — replacing the hardcoded decision call with seam-selection +
  `run_gate` reduction — happens **only here** (plan Notes item 5). Do not edit
  the inversion in WP06/WP08; do not let this WP re-do WP06's extraction.
- **Preserve fail-open (FR-010) verbatim.** Keep `_mt_empty_scope_verdict`
  (`:859`) and the broad outer `except` fold (`:1035`) as the last-resort
  non-blocking degrade. Even though `run_gate` contains faults, this scaffold is
  the FR-010 contract and stays. Only a valid `regression(blocking=true)` may
  BLOCK (C-002).
- **Selection through the one seam only.** Do not re-read step-contract bindings
  or re-apply charter activation in the hook — that is the seam's job (C-001/C-005,
  seam invariant 1). The hook keeps its own *reduction* via `run_gate` (the
  pre-review gate is a test gate, so it *does* use the FR-014 reducer — this is
  the contrast with WP14's fail-closed artifact guard).
- **Consumer fixture must be genuinely foreign.** Non-pytest, no
  `_gate_coverage.py`, no `src/specify_cli/` prefix, realistic paths. The fixture
  is the NFR-002 proof — its realism is load-bearing.
- **Red-first.** T059 must be shown red through the pre-existing entry point
  before the inversion, green after — do not assert green without proving the red.
- **No branch switching / hermetic tests.** Respect per-worker HOME isolation;
  never touch the real `~/.spec-kitty`.

## References

- `src/specify_cli/cli/commands/agent/pre_review_hook.py` — the extracted hook
  (WP06 output; this WP owns and inverts it).
- `src/specify_cli/cli/commands/agent/tasks_move_task.py:996` —
  `_mt_run_pre_review_gate` (pre-extraction locus of the hook / the inverted call
  site's origin).
- `src/specify_cli/cli/commands/agent/tasks_move_task.py:859` —
  `_mt_empty_scope_verdict` (fail-open scaffold to preserve).
- `src/specify_cli/cli/commands/agent/tasks_move_task.py:1035` — broad `except`
  fold (FR-010 contract, preserve verbatim).
- `src/specify_cli/review/gates/resolver.py` — `resolve_gates` (WP03 seam; select
  only, key `for_review`).
- `src/specify_cli/review/gates/outcomes.py` — `run_gate` / FR-014 reducer (WP04).
- `src/specify_cli/review/gates/handlers/pre_review.py` — Path-A handler (WP08).
- `contracts/gate-resolution-seam.md` — the seam contract (lane↔action adapter,
  invariants 3/6).
- `spec.md` FR-002, FR-008, FR-011, NFR-002; SC-001, SC-002.
- `research.md` §0 (the SSOT selection seam), §1 (fail-open scaffolding to
  preserve verbatim).

## Activity Log

- (append implement/review events here)
