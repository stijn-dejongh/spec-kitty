# Implementation Plan: Evict WP runtime state into the event log

**Branch**: `mission-prep/2684-wp-runtime-state-eviction` | **Date**: 2026-07-19 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `kitty-specs/wp-runtime-state-eviction-01KXWN13/spec.md`

## Summary

Evict all runtime-mutable WP state (`shell_pid`(+baseline), subtask completion, `## Activity Log`
notes, `tracker_refs`, `agent`/`assignee`, review-cycle fields) out of `tasks/WP##.md` and the
`tasks.md` subtask surface into the canonical append-only event log, via **one generic
`InnerStateChanged` off-axis event** folded into the reduced snapshot (design of record:
[ADR 2026-07-19-1](../../docs/adr/3.x/2026-07-19-1-wp-runtime-state-event-log-eviction-via-innerstatechanged.md)).
The WP files become static design-intent only, which stabilises the dossier content hash (AC-5), makes
subtask completion event-sourced (the merged P0 red test flips green), and lets claim-liveness resolve
from the snapshot. Additionally fixes the false-force provenance bug (FR-015). Executed as a
**brownfield migration** under the strict `backfill → verify → reader cutover → writer cutover → delete
fallbacks` ordering, with **extreme-campsiting** removal of the dead tails the eviction creates.

## Technical Context

**Language/Version**: Python 3.12
**Primary Dependencies**: `typer` (CLI), `pydantic` (models), internal `specify_cli.status` (event
log / reducer / FSM), `specify_cli.coordination` (transactional writes), `specify_cli.migration`
(frontmatter stripper), `specify_cli.doctrine`
**Storage**: append-only `status.events.jsonl` (SSOT for runtime state) + the reduced snapshot;
git-backed WP markdown carries **static design-intent only** after cutover
**Testing**: `pytest` (`pytest.ini` marker registry). New coverage: an architectural invariant test
(#2093), a proof-of-drive lifecycle hash test (AC-5), a persisted-force command-layer test (FR-015)
plus re-pointed existing force tests, a migration idempotency + fail-closed-verify test, and the
already-merged regression `test_issue_2684_subtask_completion_event_sourced.py`. Markers:
`regression`, `integration`, `git_repo`, `architectural`, `unit`
**Target Platform**: Linux/macOS CLI (`spec-kitty-cli`)
**Project Type**: single (Python CLI library under `src/specify_cli/`)
**Performance Goals**: the reducer fold is **O(events) with no additional re-reduction pass**
(NFR-005 — asserted structurally, not by wall-clock)
**Constraints**: strict migration ordering incl. the symmetric-window closure (C-001); typed
`WPInnerStateDelta`, never a free dict (C-002); every emit site resolves `destination_ref` from stored
topology, never `Path.cwd()` (C-003 / #2647); the 9-lane FSM 27-pair matrix is not modified — the
annotation uses a sanctioned non-transition path (C-004); no field is dual-homed static+dynamic (#2093)
**Scale/Scope**: ~12 source modules across `status/`, `cli/commands/agent/`, `migration/`, `review/`,
`merge/`, `frontmatter.py`, plus a backfill migration over the live mission corpus

## Charter Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Charter policy summary headline: **"Single canonical authority — every rule, surface, and identity has
exactly one source."** This mission is a *direct expression* of that policy: it removes the WP-metadata
split-brain so runtime state has one authority (the event log) and static intent has one authority (the
frontmatter). **PASS** — no violation; the mission strengthens the invariant. The refactor-stable
architectural test (FR-013) is the enforcing artifact. Re-checked post-design (Phase 1): the typed
delta (C-002) + no-dual-home assertion (FR-013) keep the single-authority guarantee by construction; no
new canonical-source conflict introduced. **PASS.**

## Project Structure

### Documentation (this mission)

```
kitty-specs/wp-runtime-state-eviction-01KXWN13/
├── plan.md              # This file
├── research.md          # Phase 0 — decisions + squad convergent evidence
├── data-model.md        # Phase 1 — InnerStateChanged / WPInnerStateDelta / snapshot slots / authority table
├── quickstart.md        # Phase 1 — how to verify each AC/SC
├── contracts/           # Phase 1 — event, reducer-fold, emit-force, migration contracts
└── tasks.md             # Phase 2 (/spec-kitty.tasks — NOT created here)
```

### Source Code (repository root)

```
src/specify_cli/
├── status/
│   ├── models.py            # StatusEvent + policy_metadata; NEW InnerStateChanged + WPInnerStateDelta
│   ├── store.py             # read_events / is_non_lane_event / from_dict — surface annotations to reduce()
│   ├── reducer.py           # branch on event kind; preserve runtime slots; event-kind-partition fold
│   ├── wp_state.py          # sanctioned non-transition annotate() path (no matrix change)
│   ├── transitions.py       # validate_transition (unchanged matrix)
│   └── emit.py              # _infer_subtasks_complete → snapshot; emit sites resolve topology target
├── cli/commands/agent/
│   ├── tasks_transition_core.py   # _guard_subtasks → snapshot (FR-003); build_transition_plan force fix (FR-015)
│   ├── tasks_shared.py            # _check_unchecked_subtasks (reader cutover)
│   ├── tasks_move_task.py         # cut god-write + tails (_mt_persist_tracker_refs, _mt_*uncheck*)
│   ├── tasks_mark_status.py       # emit subtask InnerStateChanged (stop writing tasks.md checkbox)
│   ├── tasks_materialization.py   # review_artifact_override_* write half + coord mirror collapse
│   ├── implement.py               # :1730 shell_pid writer (this mission OWNS the restructuring, FR-014)
│   └── workflow_executor.py       # :695,:1370 shell_pid writers
├── migration/strip_frontmatter.py # MUTABLE_FIELDS extend + backfill engine
├── review/artifacts.py            # review_artifact_override_* READ half (FR-009 both-halves)
├── merge/done_bookkeeping.py      # legacy done-evidence fallback (delete after backfill)
├── frontmatter.py                 # write_shell_pid_claim* (delete tail); add_history_entry (delete)
├── task_utils/support.py          # WorkPackage.{shell_pid,agent,assignee} reader cutover
├── status/wp_metadata.py          # WPMetadata coercion cutover; inert-field cleanup (deferred)
└── orchestrator_api/commands.py   # :1563 external Activity-Log writer (must migrate too)

tests/
├── regression/     # test_issue_2684_* (merged); force-provenance persisted test
├── architectural/  # #2093 no-dynamic-frontmatter-authority invariant; no-dead-symbols reconcile
├── integration/    # proof-of-drive lifecycle hash; migration idempotency + fail-closed verify
└── unit/           # reducer fold ordering/preserve; delta merge rules
```

**Structure Decision**: Single Python CLI project; all changes are in-place edits to `src/specify_cli/`
modules above plus a net-new backfill migration and the test surfaces listed. No new top-level package.

## Complexity Tracking

*No Charter Check violations — the mission reduces complexity (removes a split-brain). Table omitted.*

## Implementation Concern Map

> Concerns are architectural areas, **not** work packages. `/spec-kitty.tasks` translates these into
> WPs (one concern may split into several WPs; small concerns may merge). No WP IDs / sequencing verbs
> here. Sequencing is expressed as concern dependencies to honour the brownfield migration contract.

### IC-01 — Off-axis event class + reducer fold foundation

- **Purpose**: Introduce the single generic `InnerStateChanged` event with a typed `WPInnerStateDelta`,
  make it visible to and correctly folded by the reducer without touching the FSM matrix.
- **Relevant requirements**: FR-001, FR-002, C-002, C-004; NFR-005.
- **Affected surfaces**: `status/models.py`, `status/store.py` (`read_events`/`is_non_lane_event`/
  `from_dict`), `status/reducer.py` (`_wp_state_from_event`), `status/wp_state.py` (annotate path).
- **Sequencing/depends-on**: none (foundation).
- **Risks**: the reducer today **rebuilds** the per-WP dict on every transition (erases runtime slots) —
  must preserve untouched slots per-field; the wire discriminator must not collide with the existing
  `event_type` skip rule; fold ordering is an **event-kind partition**, not `at`-interleave; an
  annotation must never be reducible as a lane transition (architectural test).

### IC-02 — Reader cutover + subtask/liveness gate re-sourcing

- **Purpose**: Re-point every runtime-state reader at the reduced snapshot, behind a fallback flag until
  backfill verifies; this is what turns the merged red test green.
- **Relevant requirements**: FR-003, FR-005, FR-013; SC-002, SC-003.
- **Affected surfaces**: `tasks_transition_core.py` (`_guard_subtasks`), `tasks_shared.py`
  (`_check_unchecked_subtasks`), `status/emit.py` (`_infer_subtasks_complete`), `stale_detection.py`,
  `task_utils/support.py` (`WorkPackage.{shell_pid,agent,assignee}`), `status/wp_metadata.py` coercion.
- **Sequencing/depends-on**: IC-01.
- **Risks**: the second-polarity split-brain (C-001) — a snapshot-first reader must not ignore a fresh
  frontmatter write in the reader-before-writer window; define the authority-read vs fallback-read
  distinction (FR-013).

### IC-03 — Migration: backfill + fail-closed verify

- **Purpose**: Seed existing missions' frontmatter/checkbox runtime state into the log idempotently, and
  gate cutover on verified parity.
- **Relevant requirements**: FR-010, FR-011; SC-006, NFR-002.
- **Affected surfaces**: `migration/strip_frontmatter.py` (extend `MUTABLE_FIELDS`, move `history` out of
  `STATIC_FIELDS`, retire `progress`), a net-new backfill/seed-event module, read-back verify.
- **Sequencing/depends-on**: IC-01.
- **Risks**: deterministic namespaced ULIDs that order **after** the annotated transition at equal `at`;
  fail-closed verify aborts before reader cutover on mismatch; honest timestamp-clamp bound; zero-reader
  verification for `history[]`/`progress` before deletion.

### IC-04 — Writer cutover + created-orphan campsiting

- **Purpose**: Cut every runtime writer off the WP file and delete the dead tails the cut creates.
- **Relevant requirements**: FR-004, FR-006, FR-007, FR-008, FR-014; SC-001, SC-005, SC-008.
- **Affected surfaces**: `implement.py:1730` (**this mission owns the restructuring**),
  `workflow_executor.py:695,:1370`, `tasks_move_task.py` (god-write + `_mt_persist_tracker_refs` +
  `_mt_*uncheck*` trio), `tasks_mark_status.py`, `frontmatter.py` (`write_shell_pid_claim*`),
  `orchestrator_api/commands.py:1563`, `task_metadata_validation.py:146-165` (divergent activity_log
  frontmatter seam — reconcile), strike `tracker_refs` from `WP_FIELD_ORDER`.
- **Sequencing/depends-on**: IC-03 (verified) + IC-02.
- **Risks**: every new emit site resolves `destination_ref` from stored topology, never `Path.cwd()`
  (#2647 / SC-008); atomic switch with the reader per C-001; carries a **rebase note vs PR #2766**
  (C-006, shared `workflow_executor` writers).

### IC-05 — Review-cycle eviction (both halves)

- **Purpose**: Event-source `review_artifact_override_*` as a matched write+read pair and delete the
  dead verdict-field fallbacks, without breaking the merge gate.
- **Relevant requirements**: FR-009.
- **Affected surfaces**: `tasks_materialization.py` (write + `_persist_review_artifact_override_in_coord`
  mirror collapse), `review/artifacts.py` (read half), the merge-gate override recognition,
  `workflow_cores.py:340-348` + `done_bookkeeping.py:104-105` (delete **after** IC-03 backfill).
- **Sequencing/depends-on**: IC-03.
- **Risks**: migrating only the write silently breaks override recognition → false merge blocks
  (blocker finding); the fallback deletes must not be reordered ahead of backfill (legacy on-disk WPs).

### IC-06 — Force-provenance fix (FR-015)

- **Purpose**: Stop stamping a false `force` on evidence-gated review-rejection backward edges; pin the
  contract at the persisted-event layer.
- **Relevant requirements**: FR-015; SC-007.
- **Affected surfaces**: `tasks_transition_core.py:218-219` (`build_transition_plan`),
  `tasks_move_task.py::_mt_emit_transitions`, `status/emit.py`.
- **Sequencing/depends-on**: none (independent; shares `tasks_transition_core.py` with IC-02 — coordinate
  the lane).
- **Risks**: implement by asking the FSM (`validate_transition` legal force-free), not a frozen five-edge
  list; **re-point** the enumerated existing plan-level tests (not delete); assert the **persisted**
  `StatusEvent.force` via the real move-task path with a genuine-force positive control.

### IC-07 — Delete legacy fallbacks + land invariants (closeout)

- **Purpose**: Once backfill+cutover verify, remove the frontmatter fallbacks and land the enforcing
  guards so nothing regresses.
- **Relevant requirements**: FR-009 (deletes), FR-013; NFR-001, AC-5.
- **Affected surfaces**: the FR-005 fallback flag removal, `workflow_cores.py`/`done_bookkeeping.py`
  fallback deletion, the AC-5 stable-hash guard (wired once, no mixed parity pool), the #2093
  refactor-stable architectural test.
- **Sequencing/depends-on**: IC-02 + IC-03 + IC-04 (+ IC-05).
- **Risks**: no inert fallback left behind (charter/no-inert-fallback ADR); hash guard must cover the
  full driven lifecycle (proof-of-drive).

### IC-08 — Deferred post-cutover reduction (campsiting follow-up)

- **Purpose**: Remove code that is only *inert after* the corpus migration completes — bounded, not to
  balloon this mission.
- **Relevant requirements**: (campsiting, no new FR) — recorded in spec "Deferred to the plan/tasks phase".
- **Affected surfaces**: `_mt_clear_rollback_claim_markers`, `WPMetadata` inert fields + `coerce_shell_pid`
  + `reviewer_shell_pid`, `WP_FIELD_ORDER` cosmetic slots.
- **Sequencing/depends-on**: IC-07 (migration complete).
- **Risks**: only safe once no legacy on-disk WP carries these — do NOT reorder ahead of backfill; if it
  grows, split into a separate post-cutover reduction mission rather than expanding this one.
