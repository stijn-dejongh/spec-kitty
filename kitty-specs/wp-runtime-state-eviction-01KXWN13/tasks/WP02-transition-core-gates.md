---
work_package_id: WP02
title: 'Transition-core gates: force-fix + subtask gate re-source'
dependencies:
- WP01
requirement_refs:
- FR-003
- FR-015
tracker_refs: []
planning_base_branch: mission-prep/2684-wp-runtime-state-eviction
merge_target_branch: mission-prep/2684-wp-runtime-state-eviction
branch_strategy: Planning artifacts for this mission were generated on mission-prep/2684-wp-runtime-state-eviction. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into mission-prep/2684-wp-runtime-state-eviction unless the human explicitly redirects the landing branch.
subtasks:
- T007
- T008
- T009
agent: claude
history: []
agent_profile: python-pedro
authoritative_surface: src/specify_cli/cli/commands/agent/
create_intent:
- tests/regression/test_2684_force_provenance.py
execution_mode: code_change
owned_files:
- src/specify_cli/cli/commands/agent/tasks_transition_core.py
- tests/specify_cli/cli/commands/agent/test_tasks_transition_core.py
- tests/specify_cli/cli/commands/agent/test_tasks_backward_emit.py
- tests/regression/test_2684_force_provenance.py
role: implementer
tags: []
---

# WP02 — Transition-core gates: force-fix + subtask gate re-source

## ⚡ Do This First: Load Agent Profile

Before reading further, run `/ad-hoc-profile-load python-pedro` and adopt the profile: its identity
(type-safe Python 3.12+ implementer), its directives (TDD red→green→refactor, type hints on public
APIs, full `pytest`/`ruff`/`mypy` gate before handoff), its tactics, and its **boundaries** — you do
**not** redesign the FSM or the force-provenance policy here. The five exempt edges and the
"ask-the-FSM" mechanism are ratified in the design of record. Implement them faithfully; the moment you
feel tempted to hard-code an edge list, stop — that is the exact anti-pattern this WP exists to remove.

## Objective

Fix the false-force provenance bug and re-source the subtask gate, both of which live in
`tasks_transition_core.py`. First: stop `build_transition_plan` from auto-stamping `force=True` on the
five evidence-gated review-rejection backward edges — decided by **asking the FSM** whether the edge is
legal force-free given the supplied evidence, never by a frozen edge list (so it cannot rot if the
matrix changes). Second: re-source `_guard_subtasks` to read subtask completion from the reduced
snapshot (WP01's `subtasks` slot) instead of `tasks.md` bytes. Land this early — right after WP01 — so
every writer WP rebases onto corrected force/gate logic instead of racing it on shared files. The WP is
proven by a persisted-layer force-provenance regression driven through the **real** move-task path, plus
re-pointed existing plan-level force tests.

## Context

**Design of record**: ADR `docs/adr/3.x/2026-07-19-1-...innerstatechanged.md`. This WP realises
**IC-02** (force-provenance fix, LAND FIRST) and the `_guard_subtasks` half of **IC-04b** from
`plan.md`. Contract of record: `contracts/emit-force.md`.

**Requirements owned here**: FR-015 (ask-the-FSM force suppression; edge-specific evidence; re-point
existing tests; persisted assertion) and FR-003's gate half (`_guard_subtasks` re-source to the reduced
snapshot). Success criterion **SC-007** (persisted `StatusEvent.force` falsy for the five edges + a
genuine-force positive control, via the real move-task entry point) and **NFR-003** (0 false-force
stamps).

**Design-of-record facts you must honour**:

- **Ask the FSM, not a frozen edge list.** The mechanism is: on a backward edge without explicit
  `--force`, query `validate_transition(old, target, ctx_with_evidence)` (force-free) and only promote
  `emit_force` when the FSM genuinely rejects it. The five-edge table in `contracts/emit-force.md` is
  **confirmatory/illustrative — NOT the implementation surface**; encoding it literally would rot when
  the matrix changes (FR-015, close-by-construction).
- **Evidence is edge-specific and not interchangeable.** `reason` for `in_progress→planned`;
  `review_ref` for `approved→*`; a **structured `review_result` object** (reviewer + verdict +
  reference) for the two `in_review→*` edges (a scalar reason is rejected at `wp_state.py:624`). The
  FSM already enforces this via `_check_review_result` (`wp_state.py:612-629`) — you supply the
  evidence into the context, the FSM decides legality.
- **Persisted-force assertion via the real move-task.** SC-007 is the **persisted** `StatusEvent.force`
  read off `status.events.jsonl` after driving the real move-task entry point — **not** the plan
  object. Add the command-layer regression and re-point (delete-the-assertion-not-the-test) the
  enumerated existing plan-level tests.
- **Re-source the gate, do not delete it.** `_guard_subtasks` still refuses genuinely-incomplete WPs;
  it just reads the reduced snapshot instead of `tasks.md` bytes. The refusal branch stays.

Point to `contracts/emit-force.md` for the exact FSM-query shape and the SC-007 assertion surface.

### Current wiring (grounded)

- `build_transition_plan` is defined at `tasks_transition_core.py:173` (keyword-only signature:
  `old_lane, target_lane, force, review_feedback_pointer, arb_review_ref, note_text`).
- `tasks_transition_core.py:210` — `emit_force = force` (baseline mirrors the `--force` flag).
- `tasks_transition_core.py:218-219` — the bug: `if not force and _is_backward_transition(old_lane,
  canonical_lane): emit_force = True`. Lines 220-230 then synthesise the `"backward rewind: <old> ->
  <new>"` reason.
- `_is_backward_transition` is **imported at `tasks_transition_core.py:57`** from
  `tasks_finalize_validation` (it is NOT defined locally; the spec's "line 384" for it is stale).
- `_guard_subtasks` is defined at `tasks_transition_core.py:384`. It does **not** call
  `tasks_shared._check_unchecked_subtasks` directly — it reads the precomputed
  `req.unchecked_subtasks` tuple (a `MoveTaskRequest` field declared at
  `tasks_transition_core.py:114`). It short-circuits when `req.target_lane not in _REVIEW_GATE_LANES or
  req.force` (`:385`), returns `None` on an empty tuple (`:387`), else builds the refusal
  (`:389-395`).
- The tuple is populated **upstream** in `tasks_move_task.py:505-508` via
  `_tasks._check_unchecked_subtasks(st.repo_root, st.mission_slug, st.task_id, st.force)` and passed
  into the request at `tasks_move_task.py:539`. That reader (`tasks_shared.py:412`) reads `tasks.md`
  text (`tasks_shared.py:445`). **Note:** `tasks_move_task.py` and `tasks_shared.py` are NOT owned by
  this WP — WP04/WP06 own the upstream reader re-point. Your job is the `_guard_subtasks` consumer side.
- `validate_transition` is at `transitions.py:68`, signature `(from_lane, to_lane, ctx: GuardContext |
  None = None) -> tuple[bool, str | None]` — no `force` param; force-free legality is expressed
  structurally by the state object's `transition_to`. `ctx` defaults to `GuardContext()` (`:80`).

### Subtask T007: `build_transition_plan` ask-the-FSM force suppression (FR-015)

**Purpose**: Replace the blunt backward-edge auto-force-promotion with an FSM legality query so
evidence-gated review-rejection edges persist an honest, force-free transition.

**Steps**:
1. In `src/specify_cli/cli/commands/agent/tasks_transition_core.py`, locate the auto-promotion at
   `tasks_transition_core.py:218-219`. Replace the unconditional `emit_force = True` with the FSM query
   from `contracts/emit-force.md`:
   ```
   if not force and _is_backward_transition(old_lane, canonical_lane):
       legal_force_free, _ = validate_transition(old_lane, canonical_lane, ctx_with_evidence)
       emit_force = not legal_force_free
   ```
   where `ctx_with_evidence` is a `GuardContext` (`transitions.py:80`) populated with the edge-specific
   evidence already available to `build_transition_plan`: the `reason`/`review_feedback_pointer`
   (`in_progress→planned`), `arb_review_ref` (`approved→*`), and the structured `review_result` (the
   `in_review→*` edges). Import `validate_transition` from `status.transitions`.
2. Preserve the reason synthesis at `tasks_transition_core.py:220-230` — an honest force-free backward
   transition still carries its `"backward rewind: ..."` reason and any feedback pointer / user note.
   Only the `force` bit changes, not the audit narrative.
3. Preserve the target expansion at `tasks_transition_core.py:232-234`: `transition_targets =
   [canonical_lane]`, expanded via `_lane_targets_for_emit` only `when not emit_force`. Confirm the new
   force-free backward edges do **not** accidentally trigger forward multi-hop expansion (a backward
   edge stays single-hop; add a guard/test if the expansion path is now reachable).
4. Keep genuine-force promotion intact: edges the FSM rejects force-free (leaving terminal
   `done`/`canceled`, and all `for_review→*`/`claimed→*` rewinds per `contracts/emit-force.md`) must
   still set `emit_force = True`.

**Files**: `src/specify_cli/cli/commands/agent/tasks_transition_core.py`.

**Validation checklist**:
- [ ] The five evidence-gated edges resolve `emit_force == False` **at the plan layer** when supplied
      their edge-specific evidence.
- [ ] A genuine-force edge (e.g. leaving `done`) still resolves `emit_force == True`.
- [ ] No hard-coded five-edge tuple/set/list appears anywhere (grep the diff).
- [ ] The `"backward rewind: ..."` reason is unchanged for the force-free edges.

**Edge cases**: an `in_review→planned` supplied only a **scalar** `reason` (no structured
`review_result`) is FSM-rejected force-free (`wp_state.py:624`) → `emit_force` stays `True` (honest —
the caller did not supply valid evidence); explicit `--force=True` short-circuits at
`tasks_transition_core.py:210` before the query (unchanged); a forward edge never enters the branch.

### Subtask T008: `_guard_subtasks` re-source to the reduced snapshot (FR-003)

**Purpose**: Make the review-gate refusal decide from the event-sourced `subtasks` slot, not
`tasks.md` bytes — the consumer half of the subtask eviction.

**Steps**:
1. In `tasks_transition_core.py`, `_guard_subtasks` (`:384`) currently reads
   `req.unchecked_subtasks` (`MoveTaskRequest` field, `:114`), which upstream is populated from
   `tasks.md` text. Re-source the guard's notion of "unchecked" to the WP01 reduced-snapshot
   `subtasks` slot: materialise the snapshot for `req.task_id` and compute the incomplete set from the
   slot (a subtask id whose status is not the done-equivalent).
2. Keep the short-circuit at `:385` (`req.target_lane not in _REVIEW_GATE_LANES or req.force`) and the
   empty→`None` pass at `:387`. Keep the refusal string construction (`:389-395`) — only its **source**
   of unchecked ids changes.
3. Do **not** edit `tasks_move_task.py:505-508/539` or `tasks_shared.py:412` — those upstream readers
   are owned by WP04/WP06. If the request object still needs to carry the tuple during the migration
   window, read the snapshot inside the guard and treat `req.unchecked_subtasks` as a fallback behind
   the FR-005 flag (C-001 symmetric-window: a snapshot-first reader never strands a fresh write). Prefer
   snapshot-authoritative; document the fallback lifetime (removed in WP10).

**Files**: `src/specify_cli/cli/commands/agent/tasks_transition_core.py`.

**Validation checklist**:
- [ ] With completion recorded in the snapshot and `tasks.md` checkboxes still unchecked, the guard
      passes (returns `None`) — the SC-003 mechanism.
- [ ] With genuinely-incomplete subtasks (nothing recorded), the guard still refuses with the
      `:389-395` message.
- [ ] The resolution source is the snapshot `subtasks` slot, not a `tasks.md` read (assert via a
      patched/absent `tasks.md`).

**Edge cases**: a WP with zero subtasks in the snapshot → guard passes (nothing to refuse); a target
lane outside `_REVIEW_GATE_LANES` → short-circuit unchanged; `req.force` true → short-circuit unchanged.

### Subtask T009: Re-point plan-level force tests + persisted-force command-layer regression

**Purpose**: Reconcile the existing tests that assert the old false-force behaviour, and add the SC-007
persisted-layer regression through the real move-task entry point.

**Steps**:
1. Re-point (delete-the-assertion-not-the-test) the enumerated plan-level assertions in
   `tests/specify_cli/cli/commands/agent/test_tasks_transition_core.py`:
   - `:542` — `assert plan.emit_force is True` in `test_non_force_backward_is_rewound_and_forced`
     (`approved→in_progress`, `force=False` auto-promoted). Flip to `emit_force is False` given
     supplied `review_ref` evidence; keep the `"backward rewind: approved -> in_progress"` reason
     assertion (`:544`). Rename the test to reflect force-free provenance.
   - `:527-528` — `test_for_review_to_in_progress_force_sets_force_override_ref` is an **explicit
     `force=True`** case; it should stay `emit_force is True` (genuine force). Confirm it is not
     collateral-damaged by the T007 change (it short-circuits at `:210`). Leave as a positive control.
   - Leave the already-`False` asserts (`:110`, `:596`, `:711`) as-is or strengthen to cover the new
     force-free backward edges.
2. Re-point `tests/specify_cli/cli/commands/agent/test_tasks_backward_emit.py` (end-to-end via Typer
   `CliRunner`, reading emitted `StatusEvent.force` off `status.events.jsonl`). The backward-rewind
   assertions currently expect `force is True` (`:348,:395,:445,:529,:556`); flip the **evidence-gated
   review-rejection** edges to `force is False`, keep the genuine-force edges (`:205` and the explicit
   `--force` `"Force move to ..."` path at `:351-361`) truthy as positive controls.
3. Create `tests/regression/test_2684_force_provenance.py` (SC-007): drive each of the five
   evidence-gated edges through the **real move-task entry point** (Typer `CliRunner`, not the plan
   object), read the **persisted** `StatusEvent.force` off `status.events.jsonl`, assert falsy for all
   five with correct edge-specific evidence, and assert a retained genuine-force edge (e.g. leaving
   `done`) persists `force` truthy (positive control). Register the `regression` marker per `pytest.ini`.

**Files**: `tests/specify_cli/cli/commands/agent/test_tasks_transition_core.py` (re-point),
`tests/specify_cli/cli/commands/agent/test_tasks_backward_emit.py` (re-point),
`tests/regression/test_2684_force_provenance.py` (new).

**Validation checklist**:
- [ ] No re-pointed test was **deleted** — only its expected value corrected (the tests still exist and
      still assert force provenance).
- [ ] The new regression reads persisted force from the jsonl, not from the plan object.
- [ ] Each of the five edges is supplied its correct evidence type; a scalar-reason `in_review→*` case
      is included as a truthful-force control.

**Edge cases**: an edge that is force-free-legal but where the caller omits evidence → persisted `force`
truthy (honest); the genuine-force positive control must fail loudly if T007 over-suppresses.

## Branch Strategy

- **Planning base branch**: `mission-prep/2684-wp-runtime-state-eviction`.
- **Final merge target**: `mission-prep/2684-wp-runtime-state-eviction`.
- **Strategy**: `lane-per-wp`. Execution worktrees allocated per computed lane from `lanes.json`.
  **Land order**: WP02 depends on WP01 and MUST land before the writer WPs (WP04/WP06/WP07/WP08/WP09) so
  they rebase onto corrected `tasks_transition_core.py` force/gate logic instead of racing it (plan
  "Land order note" — avoid `tasks_transition_core.py`/`tasks_move_task.py`/`emit.py` merge races).

## Definition of Done

- [ ] `build_transition_plan` suppresses `emit_force` on FSM-legal-force-free backward edges via the
      `validate_transition` query, with **no** hard-coded edge list (FR-015, T007).
- [ ] Edge-specific evidence flows into the FSM context; genuine-force edges stay truthy (T007).
- [ ] `_guard_subtasks` decides from the reduced-snapshot `subtasks` slot and still refuses
      genuinely-incomplete WPs (FR-003, T008).
- [ ] The enumerated plan-level force tests are **re-pointed, not deleted** (SC-007, T009).
- [ ] `tests/regression/test_2684_force_provenance.py` asserts persisted `StatusEvent.force` falsy for
      all five edges + a genuine-force positive control, via the real move-task path (SC-007/NFR-003).
- [ ] `pytest tests/specify_cli/cli/commands/agent/test_tasks_transition_core.py
      tests/specify_cli/cli/commands/agent/test_tasks_backward_emit.py
      tests/regression/test_2684_force_provenance.py`, `ruff check`, and `mypy` on the module are green.
- [ ] No changes outside `owned_files` (in particular: no edits to `tasks_move_task.py`,
      `tasks_shared.py`, or `transitions.py`).

## Risks

- **Hard-coding the five edges.** The single biggest anti-pattern here; the design explicitly forbids it
  because the matrix can change. Ask the FSM.
- **Over-suppression.** If `ctx_with_evidence` is under-populated, a genuinely-force edge could go
  force-free (silent provenance loss the other way). The genuine-force positive control guards this —
  keep it.
- **Evidence type confusion.** `in_review→*` needs a structured `review_result`, not a scalar reason
  (`wp_state.py:624`). Supplying the wrong type makes the FSM reject force-free → force stays truthy,
  which is *correct* but easy to misread as a bug. Test both.
- **Cross-file bleed.** The subtask reader lives upstream in files this WP does not own. Re-source the
  **consumer** (`_guard_subtasks`) only; do not touch `tasks_move_task.py`/`tasks_shared.py`.

## Reviewer guidance

- Grep the diff for any literal set/list of the five lane pairs — its presence is an automatic reject.
- Confirm the persisted-force regression reads `status.events.jsonl`, not `plan.emit_force`.
- Confirm the re-pointed tests still assert provenance (they were corrected, not gutted) — count
  assertions before/after.
- Confirm `_guard_subtasks` reads the snapshot with `tasks.md` absent/patched and still refuses a
  genuinely-incomplete WP.
- Confirm no edits leaked into `tasks_move_task.py`, `tasks_shared.py`, or `transitions.py`.
- Confirm the genuine-force positive control fails if force is over-suppressed (non-vacuous).
