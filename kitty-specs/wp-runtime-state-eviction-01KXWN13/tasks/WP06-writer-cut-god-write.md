---
work_package_id: WP06
title: 'Writer cut: move-task god-write (+ #2647 invariant)'
dependencies:
- WP01
- WP02
- WP03
- WP04
requirement_refs:
- FR-006
- FR-007
- FR-008
- FR-012
tracker_refs: []
planning_base_branch: mission-prep/2684-wp-runtime-state-eviction
merge_target_branch: mission-prep/2684-wp-runtime-state-eviction
branch_strategy: Planning artifacts for this mission were generated on mission-prep/2684-wp-runtime-state-eviction. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into mission-prep/2684-wp-runtime-state-eviction unless the human explicitly redirects the landing branch.
subtasks:
- T022
- T023
- T024
- T025
agent: claude
history: []
agent_profile: python-pedro
authoritative_surface: src/specify_cli/cli/commands/agent/tasks_move_task.py
create_intent:
- tests/integration/test_wp_file_hash_stability.py
execution_mode: code_change
owned_files:
- src/specify_cli/cli/commands/agent/tasks_move_task.py
- tests/integration/test_wp_file_hash_stability.py
role: implementer
tags: []
---

# Work Package Prompt: WP06 – Writer cut: move-task god-write (+ #2647 invariant)

## ⚡ Do This First: Load Agent Profile

Run `/ad-hoc-profile-load python-pedro` and adopt that profile before touching any
code. You are Python Pedro: TDD, type hints on every public API, and the full quality
gate (`pytest`, `ruff`, `mypy`) before handoff. The `InnerStateChanged` event, the
`emit_inner_state_changed` API, the reducer fold, and the snapshot slots are delivered
by WP01; the FR-015 force fix + `_guard_subtasks` re-source by WP02; the migration /
backfill / verify + FR-005 flag by WP03; the `mark-status` subtask emit + reader
delegate by WP04. This WP is the **god-write hub** — it consumes those and removes the
last WP-file runtime writer on the `move-task` path. Do not redesign their contracts.

## Objective

Cut the `move-task` god-write. `_mt_persist_wp_file` (`tasks_move_task.py:1751`) is the
single hub that stamps runtime state — `agent`/`assignee`/`shell_pid` frontmatter, an
Activity-Log history line, `tracker_refs`, and (on rollback) the claim-marker clear and
subtask uncheck — into the WP file on every transition. Replace those **field writes**
with `InnerStateChanged` emits (T022), **delete** the orphaned tails the cut creates —
`_mt_persist_tracker_refs`, the `_mt_*uncheck*` trio, and `_mt_clear_rollback_claim_
markers` (T023) — and make **every** emit site resolve `destination_ref` from stored
topology, **never** `Path.cwd()` (T024, SC-008 / #2647). Prove it with a proof-of-drive
lifecycle hash test: no WP-file write across a full driven lifecycle (T025, SC-001 /
SC-005 / AC-5 / US2).

## Context

- **Design of record**: ADR 2026-07-19-1.
- **FR-008**: no `move-task` action writes `tasks/WP##.md` or the `tasks.md` subtask
  surface — cut the god-write `_mt_persist_wp_file` and the `shell_pid` writer at
  `tasks_move_task.py:1770`; delete the `_mt_*uncheck*` trio (`:1793-1920`).
- **FR-006**: `tracker_refs` is evicted (union delta from `move-task`,
  `tasks_move_task.py:1721`); delete the dead tail `_mt_persist_tracker_refs`
  (`:1707-1727`). *(The `WP_FIELD_ORDER` strike is WP07's IC-04c concern, not here.)*
- **FR-007**: `## Activity Log` notes become `InnerStateChanged` `note` appends — the
  `append_activity_log(updated_body, history_entry)` write inside `_mt_persist_wp_file`
  (`:1773-1774`) becomes an emit.
- **FR-012 / C-003 / SC-008 (#2647 invariant)**: every new off-axis emit site resolves
  its write target from stored topology / target branch, **never** `Path.cwd()`. An
  emit run from a cwd different from the mission root must land at the stored-topology
  target, not a cwd-derived location.
- **NFR-001 / SC-005 (AC-5)**: across a full lifecycle (claim → subtask-done → review →
  history) the raw-byte content hash of `tasks/WP##.md` (and the `tasks.md` WP section)
  changes **0 times**.
- **Key facts (god-write hub)**: `_mt_persist_wp_file` is called from `_mt_execute`
  (`:1970`); `_mt_reset_for_planned_rollback` (`:1972`) drives the uncheck tail. Cut the
  field writes, delete the tails including `_mt_clear_rollback_claim_markers`
  (`:1730`, moved here from IC-08 per plan — its sole caller is the god-write). Every
  emit site resolves `destination_ref` from stored topology, **never** `Path.cwd()`
  (SC-008 / #2647). Land the proof-of-drive hash test.

### Subtask T022 — Cut `_mt_persist_wp_file` field writes → emit `InnerStateChanged`

**Purpose**: Turn the god-write from a WP-file mutator into an emitter — the WP file
stops carrying runtime state; the log carries it.

**Steps** (file:line-grounded in `tasks_move_task.py`, `_mt_persist_wp_file` `:1751`):
1. The body (`:1751-1787`) currently: reads the WP file (`:1755`), splits frontmatter
   (`:1756`); on `PLANNED` rollback clears claim markers (`:1758-1759`); sets `assignee`
   (`:1760-1761`), `agent` (`:1762-1763`), `shell_pid` via `write_shell_pid_claim`
   (`:1764-1771`); builds a history line and `append_activity_log` (`:1772-1774`);
   `build_document` (`:1775`) and commits/writes the WP file
   (`_mt_commit_wp_file`/`write_text_within_directory`, `:1778-1785`); then
   `_mt_persist_tracker_refs` (`:1787`).
2. **Replace the frontmatter field writes** (`assignee`, `agent`, `shell_pid`) with an
   `InnerStateChanged` `WPInnerStateDelta` carrying `agent`/`assignee`/`shell_pid`(+
   `shell_pid_created_at`) — emitted through the WP01 API. Per data-model, the claim
   `(shell_pid, shell_pid_created_at, agent)` on the real `planned→claimed` transition
   rides the existing `policy_metadata` sidecar (FR-004) — reuse that path for the claim
   case; a `move-task`-driven reassignment/refresh outside the claim transition is an
   `InnerStateChanged` delta.
3. **Replace the Activity-Log write** (`:1772-1774`) with an `InnerStateChanged` `note`
   append (FR-007). Do not write the history line into `updated_body`.
4. **Remove the WP-file write/commit** for runtime state: `_mt_persist_wp_file` must no
   longer produce an `updated_doc` that mutates `tasks/WP##.md` for runtime fields. The
   static WP file is not rewritten on a runtime transition (that is the whole AC-5 win).
   If any *static* re-materialization remains legitimately needed, keep only that; the
   runtime field writes go.
5. Update `_mt_execute` (`:1953-1972`) so the god-write call (`:1970`) invokes the new
   emit path; `_mt_reset_for_planned_rollback` (`:1972`) is handled in T023.

**Files**: `src/specify_cli/cli/commands/agent/tasks_move_task.py`.

**Validation**: after `move-task WP01 --to claimed --shell-pid <pid> --agent claude`,
the reduced snapshot carries `shell_pid`/`agent`; `tasks/WP01.md` bytes are unchanged;
a persisted `annotation` (or claim-transition `policy_metadata`) event exists. `ruff` /
`mypy` clean.

**Edge cases**: the claim path vs the reassignment path resolve to different carriers
(transition `policy_metadata` vs `InnerStateChanged`) — do not conflate. The
`skip_target_commit`/coord-topology branches (`:1776-1785`) must not resurrect a WP-file
write. `--no-auto-commit` must not write runtime state to the WP file either.

### Subtask T023 — Delete the orphaned tails (`_mt_persist_tracker_refs`, `_mt_*uncheck*` trio, `_mt_clear_rollback_claim_markers`)

**Purpose**: Extreme campsiting — the field-write cut orphans these helpers; delete
them so no dead WP-file writer survives (randy: no half-owned dead writer).

**Steps** (file:line-grounded in `tasks_move_task.py`):
1. `_mt_persist_tracker_refs` (`:1707-1727`) writes `tracker_refs` into frontmatter via
   `write_frontmatter`. **Delete it** and its call at `:1787`. `tracker_refs` becomes an
   `InnerStateChanged` **union** delta emitted from the `move-task` path (FR-006) — emit
   the union delta where the tracker-ref values are known (`st.tracker_ref_values`),
   resolving the target from stored topology (T024). *(Striking `tracker_refs` from
   `WP_FIELD_ORDER`/static schema is WP07 IC-04c — not owned here; do not edit
   `frontmatter.py`.)*
2. `_mt_clear_rollback_claim_markers` (`:1730-1749`) `delete_scalar`s `agent`/`shell_
   pid` from frontmatter on a `PLANNED` rollback. Its sole caller is the god-write
   (`:1758-1759`). With runtime state evicted from the frontmatter, clearing frontmatter
   markers is meaningless — **delete the function** and the call. The rollback's release
   semantics are now expressed as an `InnerStateChanged` delta clearing the snapshot
   `shell_pid`/`agent` (a claim release), if the FSM/policy requires an explicit release
   record; otherwise the `planned` transition itself is the release.
3. The `_mt_*uncheck*` trio — `_mt_attempt_uncheck_write` (`:1793-1825`),
   `_mt_commit_uncheck_tasks_md` (`:1827-1855`), `_mt_uncheck_rollback_subtasks`
   (`:1857-1897`) — unchecks `- [x]` rows in `tasks.md` on rollback to `planned`. With
   subtask completion event-sourced (WP04), unchecking the byte surface is obsolete:
   rollback to `planned` is expressed as an `InnerStateChanged` `subtasks` delta
   resetting the WP's subtasks (so the gate re-blocks, #2513 intent preserved via the
   log, not the checkbox). **Delete all three** and their wiring; simplify
   `_mt_reset_for_planned_rollback` (`:1899-1920`) accordingly — or remove it if it
   becomes a pass-through (mind `_mt_execute:1972`). Also drop the now-unused
   `st.rollback_uncheck_error` field (`:207-210`) and the `write_shell_pid_claim` import
   (`:95`) if no longer referenced.
4. Run `ruff --select F401,F811` and the dead-symbol check to confirm no orphan import
   or symbol remains in this file (`test_no_dead_symbols` reconciliation is WP10, but
   your file must be clean).

**Files**: `src/specify_cli/cli/commands/agent/tasks_move_task.py`.

**Validation**: the three named functions and `_mt_clear_rollback_claim_markers` no
longer exist; rollback-to-`planned` still re-blocks the review gate (via a `subtasks`
reset delta, verified through `_check_unchecked_subtasks`); `tasks.md` bytes unchanged
on rollback. `#2513` regression (a rolled-back WP cannot re-pass the gate with no work)
still holds — now proven via the snapshot, not the checkbox.

**Edge cases**: the two former uncheck failure-handlers were deliberately separate
(C-001) — deleting both is fine since the write no longer happens, but ensure
`_mt_release_review_lock` (`:1925+`) still runs on the rollback path (the D2 ordering
the uncheck was carefully sequenced around). Preserve that ordering.

### Subtask T024 — Emit sites resolve `destination_ref` from stored topology (never `Path.cwd()`)

**Purpose**: Close #2647 by construction — a new off-axis emit must land at the
stored-topology target regardless of the caller's cwd (SC-008).

**Steps** (file:line-grounded in `tasks_move_task.py`):
1. This file already resolves the target the safe way: `_mt_resolve_targets`
   (`:240-260`) sets `st.target_branch` via `_ensure_target_branch_checked_out`, and
   the coord path resolves through `_coord_status_events_path` (`:2183+`) /
   `resolve_topology` (`:2175`) / `resolve_transaction_mid8`. **Every** new emit from
   T022/T023 MUST derive its `destination_ref` from `st.target_branch` / the resolved
   coord status ref — **not** from `Path.cwd()`.
2. Audit for cwd leaks: `_mt_warn_worktree_kitty_specs` uses `Path.cwd()` (`:223`) for a
   *warning* and `_mt_resolve_feedback` uses `Path.cwd()` (`:330`) for a *feedback-file*
   path — those are pre-existing, non-emit uses; do **not** route any *emit target*
   through them. No emit `destination_ref` may be assembled from `Path.cwd()`.
3. Reuse the same target-resolution the existing `_mt_emit_transitions` (`:1381`) /
   `emit_status_transition` chain uses (it already threads `target_branch` /
   `skip_target_branch_commit`, `:365-366`, `:620`). The new `InnerStateChanged` emits
   ride the identical resolution.

**Files**: `src/specify_cli/cli/commands/agent/tasks_move_task.py`.

**Validation**: covered by T025's SC-008 arm — an emit driven from a foreign cwd lands
at the stored-topology target. Static check: `grep -n "Path.cwd()"` shows no occurrence
on any emit-target derivation path.

**Edge cases**: coord topology vs flat/legacy — the stored-topology resolver returns ""
mid8 for a flattened mission (`_coord_status_events_path` `:2178-2181`) and the flat
target is canonical on primary; both must land correctly without a cwd fallback.

### Subtask T025 — Proof-of-drive lifecycle hash test (no WP-file write across lifecycle)

**Purpose**: Prove "unchanged" means "the actions fired AND the file bytes never moved"
— the AC-5 headline, with a proof-of-drive so it can't mean "untouched" (SC-001/005).

**Steps**:
1. Create `tests/integration/test_wp_file_hash_stability.py` (new; `@pytest.mark.
   integration`, likely `@pytest.mark.git_repo`). Build a real lanes mission fixture
   with a claimed WP.
2. Drive the **mandatory action set** through the real `move-task` / `mark-status`
   entry points: `claim → mark-subtask-done → add note → tracker_ref append →
   review-reject → review-approve → history append`.
3. **Proof-of-drive**: assert a persisted event exists in `status.events.jsonl` for
   **each** action (the action fired).
4. **Hash stability**: assert the raw-byte content hash of `tasks/WP##.md` (and the
   WP's `tasks.md` section) is **byte-identical** from `claimed` to `done` (NFR-001:
   changes 0 times). `mtime` is informational only — hash the bytes, not the stat.
5. **SC-008 arm**: run at least one off-axis `InnerStateChanged` emit from a cwd
   **different** from the mission root (`monkeypatch.chdir(tmp_path)`), and assert the
   write landed at the stored-topology target branch — never a `Path.cwd()`-derived
   location.

**Files**: `tests/integration/test_wp_file_hash_stability.py` (create — in owned_files).

**Validation**: the test is green with T022–T024 landed; it is red if any runtime write
leaks back into the WP file (positive control: temporarily restore one field write and
watch the hash assertion fail).

**Edge cases**: idempotent no-op writes bump `mtime` but not the hash — the test must
key on the hash, not `mtime` (spec: "mtime is informational, not gated"). Cover both
coord-topology and flat missions if the fixture allows; at minimum the topology the
mission uses.

## Branch Strategy

`lane-per-wp`. Planning base and merge target are both
`mission-prep/2684-wp-runtime-state-eviction`. This WP depends on WP01+WP02+WP03+WP04
and is the deepest writer cut on `tasks_move_task.py`; WP02 lands **before** the writer
WPs specifically to avoid `tasks_transition_core.py` / `tasks_move_task.py` / `emit.py`
merge races. **PR #2766 has no inbound gate — it rebases onto this writer cutover, not
the reverse (C-006).** Carry that rebase note.

## Definition of Done

- T022: `_mt_persist_wp_file` no longer writes `agent`/`assignee`/`shell_pid` or the
  Activity-Log line into the WP file; those become `InnerStateChanged` emits (claim
  rides `policy_metadata`); no runtime WP-file write remains on the transition path.
- T023: `_mt_persist_tracker_refs`, `_mt_clear_rollback_claim_markers`, and the
  `_mt_*uncheck*` trio are deleted; rollback re-blocks the gate via a `subtasks` reset
  delta; no orphan import/symbol left in the file.
- T024: every emit resolves `destination_ref` from stored topology / `st.target_branch`;
  zero `Path.cwd()` on any emit-target path.
- T025: `tests/integration/test_wp_file_hash_stability.py` lands and is green —
  proof-of-drive (event per action) + byte-stable WP-file hash across the lifecycle +
  the SC-008 foreign-cwd arm.
- `pytest` (touched paths + new test), `ruff`, `mypy` all clean.

## Risks

- **The god-write hub**: `_mt_persist_wp_file` fans into claim, reassignment, notes,
  tracker_refs, rollback-clear, and uncheck — cutting one leg while another still writes
  the file defeats AC-5. Cut them together; the hash test is the guard.
- **`destination_ref` must never be `Path.cwd()`** (#2647/SC-008): a single leaked cwd
  emit-target silently reopens the bug. Route every emit through stored topology.
- **Rollback semantics regression (#2513)**: deleting the uncheck trio without a
  `subtasks` reset delta lets a rolled-back WP re-pass the gate with no work. Preserve
  the intent through the log.
- **Ordering around `_mt_release_review_lock`**: the deleted uncheck was sequenced
  out-of-lock before the review-lock release (D2). Keep that release running on rollback.
- **Merge race**: land after WP02; do not touch `tasks_transition_core.py`/`emit.py`
  here (not owned).

## Reviewer guidance

- Hash the `tasks/WP##.md` bytes before and after the full driven lifecycle — assert 0
  changes — and confirm a persisted event exists for each action (proof-of-drive, not
  "untouched").
- `grep -n "Path.cwd()"` the file and confirm no occurrence feeds an emit
  `destination_ref` (the two surviving uses are a warning and a feedback-file path).
- Confirm `_mt_persist_tracker_refs`, `_mt_clear_rollback_claim_markers`,
  `_mt_attempt_uncheck_write`, `_mt_commit_uncheck_tasks_md`,
  `_mt_uncheck_rollback_subtasks` are all gone and no dead import (e.g.
  `write_shell_pid_claim`) remains.
- Confirm rollback-to-`planned` still re-blocks the review gate via the snapshot
  `subtasks` slot (drive it, don't assume).
- Confirm the SC-008 arm actually chdir's away from the mission root before emitting.
