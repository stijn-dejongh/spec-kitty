---
work_package_id: WP10
title: 'Closeout: delete fallbacks + land invariants'
dependencies:
- WP04
- WP05
- WP06
- WP07
- WP08
- WP09
requirement_refs:
- FR-005
- FR-009
- FR-010
- FR-013
tracker_refs: []
planning_base_branch: mission-prep/2684-wp-runtime-state-eviction
merge_target_branch: mission-prep/2684-wp-runtime-state-eviction
branch_strategy: Planning artifacts for this mission were generated on mission-prep/2684-wp-runtime-state-eviction. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into mission-prep/2684-wp-runtime-state-eviction unless the human explicitly redirects the landing branch.
subtasks:
- T036
- T037
- T038
- T039
- T040
agent: claude
history: []
agent_profile: reviewer-renata
authoritative_surface: tests/architectural/test_2093_authority_invariant.py
create_intent:
- tests/architectural/test_2093_authority_invariant.py
- tests/integration/test_ac5_hash_guard.py
execution_mode: code_change
owned_files:
- src/specify_cli/cli/commands/agent/workflow_cores.py
- src/specify_cli/merge/done_bookkeeping.py
- tests/architectural/test_no_dead_symbols.py
- tests/architectural/test_2093_authority_invariant.py
- tests/integration/test_ac5_hash_guard.py
role: implementer
tags: []
---

# Work Package Prompt: WP10 — Closeout: delete fallbacks + land invariants

## ⚡ Do This First: Load Agent Profile

```
/ad-hoc-profile-load reviewer-renata
```

Load the `reviewer-renata` profile before touching any file. This work package is the mission
**closeout**: it removes the last transitional scaffolding and lands the enforcing invariants. It is
owned by the reviewer profile because its deliverable is proof — proof that no runtime state remains
dual-homed, that no inert fallback lingers, and that the dossier content hash is byte-stable across a
driven lifecycle. Adopt the profile's anti-laziness, testability, and single-authority governance lens
for every decision below. Do **not** advance any mission step until the profile's initialization
declaration is emitted.

## Objective

Land the closeout for the WP-runtime-state eviction: delete the FR-005 frontmatter-fallback flag and
any C-001 dual-write shim (T036); delete the two legacy verdict-field read fallbacks in
`workflow_cores.py:340-348` and `done_bookkeeping.py:104-105` — **only after** the WP03 backfill has
seeded legacy approvals as events (T037); land the AC-5 stable-hash guard as a proof-of-drive full
lifecycle test (T038); land the #2093 refactor-stable architectural test — no consumer reads a dynamic
frontmatter field as authority, and no field appears in both the static authored schema and the
event-sourced slot set — and reconcile the `test_no_dead_symbols.py` allowlist (T039); confirm the
re-pointed force tests (from WP02) and the full suite are green (T040).

This is the terminal WP on the dependency graph: it depends on **every** field vertical (WP04–WP09)
having landed its reader re-point, writer cut, and created-orphan deletes. Nothing here may run before
those are merged — the fallbacks and shims this WP deletes are still load-bearing until then.

## Context

**Design of record**: ADR `2026-07-19-1-wp-runtime-state-event-log-eviction-via-innerstatechanged.md`.
This WP corresponds to plan concern **IC-07 — Delete legacy fallbacks + land invariants (closeout)**.

The mission evicts runtime-mutable WP state (`shell_pid`, subtask completion, `## Activity Log` notes,
`tracker_refs`, `agent`/`assignee`, review-cycle fields) out of `tasks/WP##.md` into the append-only
event log, folded through one generic off-axis `InnerStateChanged` event. The migration runs under the
strict order (contract `migration.md`):

```
backfill → verify(FAIL-CLOSED) → reader cutover → writer cutover → delete fallbacks → land hash guard
```

WP10 owns the last two boxes. The delete-fallbacks step is **gated on backfill** by construction: the
two legacy read fallbacks synthesize done-evidence for un-migrated on-disk WPs, so removing them before
WP03 seeds those approvals as events would strand legacy corpora. Do **not** reorder the delete ahead of
backfill.

**Key spec references**:
- **FR-009** — Evict all review-cycle state. Delete the dead verdict-field read fallbacks
  `workflow_cores.py:340-348` (whole branch) and `done_bookkeeping.py:104-105` — but only after the
  FR-011 backfill seeds legacy approvals as events.
- **FR-013** — A refactor-stable architectural test asserts no consumer reads a dynamic frontmatter
  field as authority (the #2093 invariant), distinguishing an authority-read from a tolerated
  migration-window fallback-read, and additionally asserts no field appears in both the static authored
  schema and the event-sourced slot set (catches the FR-006 `tracker_refs` dual-home).
- **NFR-001** — Across a full WP lifecycle (claim → subtask-done → review → history), the raw-byte
  content hash of `tasks/WP##.md` and the WP's `tasks.md` section changes **0 times**.
- **AC-5 / SC-005** — The WP-file content hash is byte-stable across the full **driven** lifecycle
  (same proof-of-drive as SC-001: a persisted event must exist for each action, so "unchanged" can
  never mean "untouched").

**Key planning references**:
- `contracts/migration.md` — the strict order and the "delete fallbacks only now" rationale.
- `data-model.md` — the post-mission field-authority table ("No field appears in both columns of
  authority — enforced by the FR-013 architectural test") and the event-sourced slot set
  `{shell_pid, shell_pid_created_at, subtasks, notes, tracker_refs, agent, assignee, review}`.
- `quickstart.md` — SC-001/SC-005 proof-of-drive and the FR-013 architectural-invariant list.

**Owned-file boundary (read before you start)**: WP10 owns exactly the five files in the frontmatter
`owned_files`. The FR-005 fallback flag and the phase-1 dual-write shim have definitions that live in
files owned by earlier verticals (`core/stale_detection.py` FR-005 baseline gate — WP05;
`status/emit.py::_phase1_dual_write_enabled`/`_mirror_phase1_frontmatter_lane` shim — WP01). WP10 does
**not** edit non-owned files. Where a residual shim survives outside the owned surface, T036's job is to
**detect and escalate**, and the FR-013 arch test (T039) is the enforcing net. See Reviewer guidance.

---

### Subtask T036 — Delete FR-005 fallback flag + any dual-write shim

**Purpose**: Now that all field verticals (WP04–WP09) have switched their reader authority to the
reduced snapshot atomically-per-field (C-001), the transitional scaffolding is inert and must be torn
down so no second authority path survives the mission. FR-005 retained the frontmatter fallback "behind
a flag until backfill is verified, then removed"; C-001 permitted a bounded dual-write shim "only where
a field cannot switch atomically … explicitly bounded and torn down in IC-07". This is that teardown.

**Steps**:
1. Audit the codebase for the FR-005 fallback flag and any C-001 dual-write shim that is now inert:
   - The FR-005 baseline/flag gate lives in `core/stale_detection.py:230-235,395-403`
     (`shell_pid_baseline` presence-gated fallback to the timestamp heuristic) — **WP05-owned**.
   - The phase-1 dual-write shim lives in `status/emit.py:310` (`_phase1_dual_write_enabled`) and
     `:345` (`_mirror_phase1_frontmatter_lane`) — **WP01-owned**.
2. Within WP10's **owned files**, delete any inert flag/shim that appears there. (After the WP04–WP09
   cuts land, confirm none does — the flag/shim definitions are in non-owned modules.)
3. For a residual flag/shim in a non-owned file: do **not** edit it. Record it as a closeout finding
   and escalate to the owning vertical (WP05 / WP01) so the teardown lands in the correct lane, or
   confirm the owning WP already removed it as part of its atomic per-field switch. The FR-013 arch
   test (T039) is the mechanical proof that no dual-home / inert authority path survives — treat a
   surviving shim as a T039 failure, not a WP10 owned-file edit.

**Files**: (owned) `src/specify_cli/cli/commands/agent/workflow_cores.py`,
`src/specify_cli/merge/done_bookkeeping.py` — only if an inert flag/shim is found in them.

**Validation**: `rg -n "phase1_dual_write|status_phase|_mirror_phase1|shell_pid_baseline.*fallback"`
over `src/` returns no *inert* survivor; the FR-013 arch test (T039) passes with no dual-home finding.

**Edge cases**: Deleting a shim before its paired reader/writer switched atomically reopens the C-001
symmetric split-brain (a fresh runtime write becomes invisible to a snapshot-first reader) — this is why
T036 runs only after WP04–WP09. A flag left inert but undeleted is a latent second authority path (the
#2093 violation the mission exists to close); it must fail T039, not pass silently.

---

### Subtask T037 — Delete legacy verdict-field read fallbacks (post-backfill)

**Purpose**: Remove the two dead frontmatter-sourced done-evidence fallbacks that synthesized approval
evidence for un-migrated on-disk WPs. They are only safe to delete **after** the WP03 backfill seeds
legacy approvals as `InnerStateChanged`/transition events (FR-009 / FR-011 order); the review-cycle
authority is now the reduced snapshot.

**Steps**:
1. In `workflow_cores.py::resolve_review_feedback_context`, delete the frontmatter fallback branch at
   lines **340-348** — the `fm_review_status = extract_scalar(wp_frontmatter, "review_status")` /
   `fm_review_feedback = ...` read and the `if fm_review_status ... == "has_feedback": … return True,
   ref, path, "frontmatter"` branch. The canonical path above it (`latest_review_feedback_reference`
   → `return True, …, "canonical"`) is now the sole resolution; the function returns
   `(False, None, None, None)` when no canonical artifact exists.
2. Confirm the `"frontmatter"` provenance tag has no remaining consumer (it was the fallback's marker);
   if a caller branches on it, the branch is now dead — remove it or verify it is out of WP10's owned
   surface and flag it.
3. In `done_bookkeeping.py::_extract_done_evidence`, delete lines **104-105**
   (`reviewed_by = meta.reviewed_by` and the `if meta.review_status == "approved" and reviewed_by …`
   guard) together with the `DoneEvidence(review=ReviewApproval(..., reference=f"frontmatter-migration:
   {wp}"))` synthesis they gate. After deletion the function resolves done-evidence from the
   event-sourced review slot only; a WP with no seeded/event approval yields `None` (fail-closed — do
   not fabricate approval from frontmatter).
4. Re-point or delete the now-orphaned `WPMetadata` frontmatter reads (`meta.reviewed_by`,
   `meta.review_status`) **only if** they live in owned files; otherwise flag to WP05/WP09.

**Files**: `src/specify_cli/cli/commands/agent/workflow_cores.py` (lines 340-348),
`src/specify_cli/merge/done_bookkeeping.py` (lines 104-105 + gated synthesis).

**Validation**: full merge-gate + review-cycle tests green (WP09 landed both halves); a fixture WP
approved via events resolves done-evidence; a legacy on-disk WP that was backfilled (WP03) still
resolves — proving the delete is post-backfill-safe. `rg -n "frontmatter-migration" src/` returns
nothing.

**Edge cases**: Deleting these **before** backfill strands legacy corpora — assert WP03's backfill has
merged and its fail-closed verify passed before this subtask. A silent behavior change is the danger:
the merge gate must not start falsely blocking merges because override/approval recognition regressed;
lean on WP09's both-halves override migration and the merge-gate override-recognition tests.

---

### Subtask T038 — Land AC-5 stable-hash guard (proof-of-drive lifecycle)

**Purpose**: Prove NFR-001 / SC-005 by construction: across a full **driven** WP lifecycle, the raw-byte
content hash of `tasks/WP##.md` and the WP's `tasks.md` section changes 0 times, and a persisted event
exists for each driven action so "unchanged" can never mean "untouched".

**Steps**:
1. Create `tests/integration/test_ac5_hash_guard.py` (new). Mark it `integration` and `git_repo` per
   the plan's marker registry.
2. On a real lanes-topology WP fixture, drive the mandatory action set through the canonical entry
   points (not by hand-editing files): `claim → mark-subtask-done → add note → tracker_ref append →
   review-reject → review-approve → history append` (quickstart SC-001/SC-005).
3. Capture the raw-byte content hash of `tasks/WP##.md` and the WP's `tasks.md` section at `claimed`
   and after each subsequent action through `done`. Assert every hash equals the `claimed` hash
   (0 changes).
4. **Proof-of-drive**: for each action, assert a corresponding persisted event exists on
   `status.events.jsonl` (an `InnerStateChanged` annotation or a transition, as appropriate). A green
   test with no events would mean the actions never fired — assert both halves.
5. mtime is informational only (idempotent no-op writes bump it); do **not** gate on mtime.

**Files**: `tests/integration/test_ac5_hash_guard.py` (create).

**Validation**: `pytest tests/integration/test_ac5_hash_guard.py -q` passes; deliberately re-introducing
any WP-file runtime write (e.g. reverting a WP06 writer cut) turns it red — confirm the guard bites.

**Edge cases**: An emit site resolving its target from `Path.cwd()` instead of stored topology reopens
#2647 and can write to the wrong file, leaving the fixture hash falsely stable — pair the drive with a
cwd different from the mission root where practical (SC-008 is WP08's dedicated test, but keep the
lifecycle drive honest). Ensure the review-reject/approve steps use the FR-015 evidence-gated,
force-free path so the drive matches production behavior.

---

### Subtask T039 — #2093 refactor-stable arch test + reconcile `test_no_dead_symbols`

**Purpose**: Land the enforcing FR-013 invariant so the single-authority guarantee cannot silently rot
under future refactors, and reconcile the dead-symbol allowlist now that the eviction deleted its
orphaned writers.

**Steps**:
1. Create `tests/architectural/test_2093_authority_invariant.py` (new; marker `architectural`). Assert
   **two** invariants:
   - **No dynamic-authority frontmatter read**: no consumer reads a dynamic frontmatter field
     (`shell_pid`, `shell_pid_created_at`, subtask completion, `agent`, `assignee`, `tracker_refs`,
     review-cycle fields) as **authority**. Define the detection mechanism explicitly — an
     import/call-graph (AST) over the authority read path — and distinguish an authority-read from a
     **tolerated migration-window fallback-read**. Since T036/T037 removed the last fallbacks, the
     tolerated set should now be empty; encode that so a re-introduced fallback fails.
   - **No dual-home**: no field name appears in **both** the static authored schema
     (`WP_FIELD_ORDER` / frontmatter schema) **and** the event-sourced slot set
     `{shell_pid, shell_pid_created_at, subtasks, notes, tracker_refs, agent, assignee, review}`.
     This catches the FR-006 `tracker_refs` dual-home directly (WP07 struck it from `WP_FIELD_ORDER`).
2. Make the test **refactor-stable**: key on symbol identity / slot membership, not line numbers, so a
   later relocation does not produce a false green or a brittle red.
3. Reconcile `tests/architectural/test_no_dead_symbols.py`: the `add_history_entry` allowlist
   `SymbolKey` entry (around **line 282**, commented `specify_cli.frontmatter::add_history_entry`) was
   tolerated while the symbol was live-but-uncalled. WP03/IC-06 deleted `add_history_entry` and its
   `__all__` export, so the allowlist entry is now stale — **remove it** (leaving it masks the next
   dead symbol). Verify no other WP10-adjacent deletion (the FR-009 fallbacks) leaves a symbol that now
   needs an allowlist entry; prefer deleting the symbol over allowlisting it.

**Files**: `tests/architectural/test_2093_authority_invariant.py` (create),
`tests/architectural/test_no_dead_symbols.py` (remove the stale `add_history_entry` allowlist entry).

**Validation**: `pytest tests/architectural -q` green; deliberately re-adding a frontmatter authority
read (or re-listing `tracker_refs` in `WP_FIELD_ORDER`) turns `test_2093_authority_invariant.py` red;
`test_no_dead_symbols.py` passes without the removed allowlist entry.

**Edge cases**: The hard part is distinguishing an **authority-read** from a **tolerated fallback-read** —
misclassifying either produces a false green (an undetected dual-home) or a false red (a legitimate
render-only read). Ground the classifier on the field-authority table in `data-model.md`. Removing the
allowlist entry while the symbol is somehow still live would break `test_no_dead_symbols.py` — confirm
the WP03/IC-06 deletion of `add_history_entry` has merged first.

---

### Subtask T040 — Full-suite green; re-pointed force tests reconciled

**Purpose**: Terminal acceptance — confirm the entire mission lands green, including the WP02 force
tests that were **re-pointed** (not deleted) to the correct FR-015 expected values (SC-007), and the
already-merged red regression that this mission flips green.

**Steps**:
1. Run the full suite: `pytest -q` (or the project's canonical gate). Confirm 0 failures.
2. Confirm the re-pointed force-provenance tests assert the **corrected** values: the persisted
   `StatusEvent.force` is falsy for the five evidence-gated review-rejection edges and truthy for the
   retained genuine-force positive control. These tests are **WP02-owned** — WP10 does not edit them; it
   confirms the whole suite (including them) is green. If any is red, the failure belongs to the owning
   lane (WP02) — record it and escalate, do not edit a non-owned test to force green.
3. Confirm `tests/regression/test_issue_2684_subtask_completion_event_sourced.py` (merged, red today)
   is now **green for the right mechanism** — the resolution source is the reduced-snapshot `subtasks`
   slot (WP04), not a `HistoryAdded` read.
4. Confirm the WP10-owned new tests (`test_ac5_hash_guard.py`, `test_2093_authority_invariant.py`) and
   the reconciled `test_no_dead_symbols.py` are green.

**Files**: none edited (verification subtask); reference the enumerated re-pointed tests
(`test_tasks_transition_core.py`, `test_tasks_backward_emit.py`, `test_status_e2e_integration.py`,
`test_status_cli.py`) as green-confirmation targets only.

**Validation**: full `pytest` green; `ruff` and `mypy` clean on the owned files; the mission's headline
outcomes (P0 red test green, AC-5 hash stable, honest force provenance) all pass.

**Edge cases**: A flaky or environment-dependent failure in a non-owned lane is not a WP10 defect —
attribute it correctly. Do **not** delete or weaken an assertion to reach green (SC-007 is explicit:
"delete-the-assertion-not-the-test" was already done as a *re-point* in WP02; WP10 must not re-delete).

---

## Branch Strategy

- **Strategy**: `lane-per-wp`. This WP executes in its own worktree/lane allocated by `finalize-tasks`.
- **Planning base / merge target**: `mission-prep/2684-wp-runtime-state-eviction`.
- WP10 is the terminal node on the dependency graph; it depends on WP04, WP05, WP06, WP07, WP08, and
  WP09. Rebase onto the integration of those lanes before starting — the fallbacks and shims this WP
  deletes are load-bearing until every field vertical has cut over.
- Completed changes merge back into `mission-prep/2684-wp-runtime-state-eviction`. Do not retarget the
  landing branch unless a human explicitly redirects it.
- Per C-006, PR #2766 has no inbound gate — it rebases onto this mission's writer cutover, not the
  reverse. WP10 does not wait on it.

## Definition of Done

- [ ] T036: no inert FR-005 fallback flag or C-001 dual-write shim survives; any residual in a
      non-owned file is escalated to its owning lane and proven gone by the T039 arch test.
- [ ] T037: `workflow_cores.py:340-348` and `done_bookkeeping.py:104-105` legacy verdict-field
      fallbacks deleted; done-evidence and review-feedback resolve from events only; verified
      post-backfill (WP03 merged, fail-closed verify passed).
- [ ] T038: `tests/integration/test_ac5_hash_guard.py` created and green — 0 hash changes across the
      driven lifecycle **with** a persisted event per action (proof-of-drive).
- [ ] T039: `tests/architectural/test_2093_authority_invariant.py` created and green (no
      dynamic-authority frontmatter read; no field dual-homed static+dynamic); `test_no_dead_symbols.py`
      `add_history_entry` allowlist entry removed and the gate still green.
- [ ] T040: full `pytest` suite green, including the WP02 re-pointed force tests (SC-007) and the
      flipped `test_issue_2684_subtask_completion_event_sourced.py`.
- [ ] `ruff` and `mypy` clean on all owned files; no owned-file edit exceeds the `owned_files` list.
- [ ] Reviewer initialization declaration emitted; findings for any non-owned residual recorded.

## Risks

- **Deleting a fallback before backfill** (FR-009 / migration.md): the two legacy read fallbacks
  synthesize done-evidence for un-migrated on-disk WPs. Removing them ahead of the WP03 backfill strands
  legacy corpora. **Mitigation**: gate T037 on confirmed WP03 merge + passed fail-closed verify.
- **Surviving inert flag/shim = latent second authority path** (#2093): an undeleted flag is exactly the
  split-brain the mission closes. **Mitigation**: T039 arch test fails on any dual-home; treat a survivor
  as a red test, not a tolerated leftover.
- **Owned-file boundary tension**: the FR-005 flag (`stale_detection.py`, WP05) and phase-1 dual-write
  shim (`emit.py`, WP01) live outside WP10's owned surface. **Mitigation**: WP10 detects and escalates;
  it does not edit non-owned files; the arch test is the enforcing net.
- **False-green hash guard**: an emit site writing via `Path.cwd()` (#2647) can leave the fixture hash
  falsely stable. **Mitigation**: drive from a non-mission-root cwd where practical; rely on WP08's
  SC-008 test for the dedicated invariant.
- **Authority-read vs fallback-read misclassification** (T039): the classifier is the subtle part;
  misgrouping yields a false green (missed dual-home) or false red. **Mitigation**: ground on the
  `data-model.md` field-authority table; assert the tolerated-fallback set is empty post-T036/T037.
- **Editing a non-owned red test to force green** (T040): forbidden — SC-007 already re-pointed those in
  WP02. **Mitigation**: escalate cross-lane failures to the owning WP.

## Reviewer guidance

This WP is authored for `reviewer-renata`; apply the profile end to end.

- **Anti-laziness / proof-of-drive**: every "unchanged"/"green" claim must carry a positive control. The
  AC-5 guard (T038) asserts a persisted event per action; the arch test (T039) must bite when a
  frontmatter authority read or a `WP_FIELD_ORDER` dual-home is re-introduced. Reject any test that
  passes vacuously.
- **Single canonical authority (charter)**: the closeout's whole purpose is one-authority-per-field.
  After WP10, runtime state has exactly one authority (the event log) and static intent one authority
  (frontmatter). Verify the field-authority table in `data-model.md` holds with no field in both
  columns.
- **Ordering discipline**: confirm the migration order (`backfill → verify → reader → writer → delete
  fallbacks → hash guard`) was honored — T037 deletions are post-backfill, T036 teardown is
  post-writer-cut. A reordering is a correctness defect even if the suite is green on a fresh corpus.
- **Scope discipline**: WP10 edits only its five owned files. Record every residual shim/flag/dead
  symbol found in a non-owned file as a closeout finding and route it to the owning lane (WP01/WP05/WP09)
  rather than editing out of scope. Escalate cross-lane test failures; never weaken an assertion to
  reach green.
- **Deferred (not this WP)**: IC-08 post-cutover reduction (inert `wp_metadata` fields,
  `WP_FIELD_ORDER` cosmetic slots) is a separate bounded reduction after this mission merges — do not
  pull it forward into the clobber window.
