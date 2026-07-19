# Mission Specification: Evict WP runtime state into the event log

**Mission Branch**: `mission-prep/2684-wp-runtime-state-eviction`
**Created**: 2026-07-19
**Status**: Draft
**Input**: #2684 (P0) — "Evict runtime-mutable WP state (shell_pid, history, subtask-checkbox, review-cycle, activity-log) from tasks/WP##.md into the event log", the execution vehicle for the #2093 authority ruling. Design of record: `docs/adr/3.x/2026-07-19-1-wp-runtime-state-event-log-eviction-via-innerstatechanged.md`. Full grounding + seven ratified decisions: `docs/plans/investigations/2684-task-move-cluster-scoping.md` (§0). Additionally accommodates a confirmed force-provenance bug found during #2736 / PR #2810 (see FR-015 / US5).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Hand a completed WP to review without hand-ticking checkboxes (Priority: P1)

An operator/agent finishes a WP's work and moves it to `for_review`. Completion recorded through the
canonical path is honored by the review gate — no manual `mark-status` per subtask.

**Why this priority**: This is the P0 operator friction (mission #2736 catfooding) and the invariant
the already-merged red test pins.

**Independent Test**: On a lanes mission, complete WP01's subtasks via the canonical path and run
`move-task WP01 --to for_review` — it succeeds without editing `tasks.md` checkboxes
(`tests/regression/test_issue_2684_subtask_completion_event_sourced.py` flips green).

**Acceptance Scenarios**:
1. **Given** WP01 `in_progress` with subtasks recorded complete in the reduced snapshot **and**
   `tasks.md` checkboxes not hand-edited, **When** `move-task WP01 --to for_review`, **Then** it
   succeeds and the WP is `for_review`.
2. **Given** WP01 with genuinely-incomplete subtasks (no completion recorded), **When**
   `move-task WP01 --to for_review`, **Then** it is correctly refused.

### User Story 2 - No false drift across a WP lifecycle (Priority: P1)

The content hash of `tasks/WP##.md` and the WP's `tasks.md` section stays stable across
claim → subtask-done → review → history, because no runtime state is written into those files.

**Why this priority**: AC-5 — the headline proof of the mission and the long-homeless dossier churn fix.

**Independent Test**: Run a WP through a full lifecycle; assert the raw-byte content hash of its files
is unchanged from `claimed` to `done`.

**Acceptance Scenarios**:
1. **Given** a WP taken through claim, subtask completion, review, and history, **When** the dossier
   parity hash is computed at each step, **Then** the WP's file hashes are identical throughout.

### User Story 3 - Claim-liveness and resume resolve from the log (Priority: P2)

Claim-liveness reads the reduced snapshot. A claimed WP with no frontmatter `shell_pid` is still
detected live; a resumed `in_progress` WP refreshes its PID via an off-axis event and is not falsely
flagged stale.

**Why this priority**: AC-2; closes the resume false-stale window by construction.

**Independent Test**: Claim a WP (empty frontmatter), assert liveness = live from the snapshot; resume
it, assert the PID refresh is an `InnerStateChanged` event and liveness stays live.

**Acceptance Scenarios**:
1. **Given** a claimed WP with no frontmatter `shell_pid`, **When** liveness is evaluated, **Then** it
   resolves live from the reduced snapshot.
2. **Given** a resumed `in_progress` WP, **When** its shell PID refreshes, **Then** an
   `InnerStateChanged` delta records it with a truthful timestamp, no lane transition, and no
   `force_count` increment.

### User Story 4 - Activity Log / History / review render from events (Priority: P2)

The `## Activity Log`, `## History`, and review sections render from the event log with no content
loss, now that they are no longer written into the WP file.

**Why this priority**: AC-4; guards the M7 data-loss risk during eviction.

**Independent Test**: Drive a WP through notes + a review cycle; assert the rendered content matches,
sourced from events.

### User Story 5 - Rejecting a WP to review does not stamp a false force override (Priority: P2)

A reviewer rejects a WP back to an earlier lane (e.g. `in_review → planned`) with evidence. The
persisted event records an honest, force-free transition — it does **not** claim a guard-bypass that
never happened, so audit provenance stays truthful.

**Why this priority**: A confirmed provenance-corruption bug (found during #2736 / PR #2810) in the
exact transition-emit path this mission rewrites; it is the missing caller-side half of FR-007 from
#2736.

**Independent Test**: Reject a WP across each of the five evidence-gated backward edges through the
real `move-task` entry point; assert the persisted `StatusEvent.force` is falsy for all five.

**Acceptance Scenarios**:
1. **Given** an `in_review` WP with review evidence (reason / review_ref / review_result), **When**
   `move-task --to planned` (or `in_progress`) is run without `--force`, **Then** the transition
   succeeds and the persisted `StatusEvent.force` is falsy.
2. **Given** a genuinely force-requiring backward edge (e.g. leaving a terminal `done`/`canceled`
   state), **When** it is emitted, **Then** `force` remains truthfully set.

### User Story 6 - Existing missions migrate idempotently (Priority: P3)

A migration backfills existing missions' frontmatter/checkbox runtime state into seed events, safe to
re-run.

**Why this priority**: AC-6; makes the cutover safe for the live corpus.

**Independent Test**: Run the migration twice; assert the reduced snapshot equals pre-migration state
by count+value and that re-running seeds nothing new.

### Edge Cases

- Subtask checkboxes carry **no timestamp** → the backfilled mark is clamped to the WP's `claimed`
  timestamp; "no data loss" is asserted against count+value parity, not literal temporal fidelity.
- A new off-axis emit site resolving its write target from `Path.cwd()` silently reopens #2647 —
  targets MUST come from stored topology/target branch.
- `history[]` frontmatter is dead **and** mis-filed in `STATIC_FIELDS` — delete outright, no migration.
- `progress` is dead — retire explicitly, don't silently drop.
- The external writer `orchestrator_api/commands.py:1563` (Activity Log) must migrate too.
- Many existing backward-transition tests assert `emit_force=True`; they must be reconciled when the
  false-force promotion is removed (FR-015).

## Requirements *(mandatory)*

### Functional Requirements

| ID | Requirement | Priority | Status |
|----|-------------|----------|--------|
| FR-001 | Introduce one generic non-transition event `InnerStateChanged` carrying a **typed** partial `WPInnerStateDelta` (optional typed fields, not a free dict); no `from_lane`/`to_lane`; bypasses `validate_transition`; reducer-folded. | High | Accepted |
| FR-002 | The reducer folds `InnerStateChanged` deltas onto the reduced snapshot with per-field merge — **replace** for `shell_pid`/`shell_pid_created_at`/per-subtask status, **union** for `tracker_refs`, **append** for `notes` — after transition folds, last-writer-wins, and **never** increments `force_count`. Snapshot gains typed slots: `shell_pid`, `shell_pid_created_at`, `subtasks`, `notes`, `tracker_refs`. | High | Accepted |
| FR-003 | Subtask completion is recorded as an `InnerStateChanged` `subtasks` delta (single or batch). `_guard_subtasks` (`tasks_transition_core.py:384` via `tasks_shared.py:412`) and done-inference `_infer_subtasks_complete` (`status/emit.py:279`) resolve from the reduced snapshot, not `tasks.md` bytes. | High | Accepted |
| FR-004 | Claim `(shell_pid, shell_pid_created_at)` rides the real `planned→claimed` transition via the existing `policy_metadata` sidecar (no wire-schema change); a **resume** refresh of an already-`in_progress` WP is recorded as an `InnerStateChanged` delta. | High | Accepted |
| FR-005 | Claim-liveness (`stale_detection.py:402-403`) and model readers `WorkPackage.{shell_pid,agent,assignee}` (`task_utils/support.py:287-296`) + `WPMetadata` coercion resolve from the reduced snapshot; the frontmatter fallback is retained behind a flag until backfill is verified, then removed. | High | Accepted |
| FR-006 | `tracker_refs` is evicted (runtime, event-sourced): `map-requirements` (`tasks_map_requirements.py:428`) and `move-task` (`tasks_move_task.py:1721`) emit an `InnerStateChanged` `tracker_refs` union delta; FR-011 runtime append preserved; removed as a WP-file write. | Medium | Accepted |
| FR-007 | `## Activity Log` notes are recorded as `InnerStateChanged` `note` appends from all six writers, including the external `orchestrator_api/commands.py:1563`; the section renders from events. | Medium | Accepted |
| FR-008 | No `implement`/`mark-status`/`move-task`/review action writes `tasks/WP##.md` or the `tasks.md` subtask surface. Cut the four `shell_pid` writers (`implement.py:1730`, `workflow_executor.py:695` & `:1370`, `tasks_move_task.py:1770`), the `agent`/`assignee` writers, the subtask checkbox write/uncheck, and the move-task god-write `_mt_persist_wp_file`. | High | Accepted |
| FR-009 | Evict all review-cycle state: **delete** the dead verdict-field read fallbacks `workflow_cores.py:340-341` and `done_bookkeeping.py:104-105` (guaranteeing canonical done-evidence), **and** evict the actively-written `review_artifact_override_*` (`tasks_materialization.py:58-61,125-128`). | High | Accepted |
| FR-010 | Extend the canonical `migration/strip_frontmatter.py:MUTABLE_FIELDS` (do not fork): add `shell_pid_created_at`, `review_artifact_override_*`, `reviewer_shell_pid`; move `history` out of `STATIC_FIELDS`. Retire `progress` (remove from set/schema; document). Delete `history[]` outright (dead). | Medium | Accepted |
| FR-011 | Migration order: **backfill → verify → reader cutover → writer cutover → delete fallbacks + land AC-5 hash guard**. Seed transition + `InnerStateChanged` events with deterministic namespaced ULID ids (`mission_id + wp_id + field`); idempotent; verify snapshot == pre-migration by count+value. | High | Accepted |
| FR-012 | Every new off-axis emit site resolves its write target from stored topology/target branch, never `Path.cwd()` (do not reopen #2647). | High | Accepted |
| FR-013 | A refactor-stable architectural test asserts no consumer reads a dynamic frontmatter field as authority (the #2093 invariant). | Medium | Accepted |
| FR-014 | This mission **owns** the `implement.py:1730` shell_pid-writer restructuring; the former #2160 co-sequence is retired (#2160's writer work is `pr:deferred` and yields), so the writer cutover proceeds without an external `blocks/blocked_by` gate. | High | Accepted |
| FR-015 | Fix the false-force provenance bug: exempt the five evidence-gated review-rejection backward edges (`in_progress→planned`, `approved→in_progress`, `approved→planned`, `in_review→in_progress`, `in_review→planned`) from auto-force-promotion in `build_transition_plan` (`tasks_transition_core.py:218-219`). When the edge is FSM-legal force-free given supplied evidence (reason / review_ref / review_result), do **not** set `emit_force`. Keep force auto-promotion only for backward edges that genuinely require it (e.g. leaving terminal `done`/`canceled`). Add a command-layer emit-force test asserting the persisted `StatusEvent.force` is falsy for these five edges (the missing caller-side half of FR-007 from #2736), and reconcile existing backward-transition tests that assert `emit_force=True`. CLI-side; distinct from `spec-kitty-saas#509`. | High | Accepted |

### Non-Functional Requirements

| ID | Requirement (measurable threshold) | Category | Priority | Status |
|----|-----------------------------------|----------|----------|--------|
| NFR-001 | Across a full WP lifecycle (claim → subtask-done → review → history), the raw-byte content hash of `tasks/WP##.md` and the WP's `tasks.md` section changes **0 times**. | Reliability / Integrity | High | Accepted |
| NFR-002 | The migration is idempotent: a second run seeds **0** new events; the reduced snapshot equals pre-migration state by **100%** count+value parity. | Data Integrity | High | Accepted |
| NFR-003 | The persisted `StatusEvent.force` is falsy for **all five** evidence-gated review-rejection edges (0 false-force stamps); `force` remains truthful only where a genuine guard-bypass occurred. | Auditability / Provenance | High | Accepted |
| NFR-004 | A resumed `in_progress` WP is **never** falsely flagged stale due to a missing frontmatter `shell_pid` (0 false-stale on resume within the configured staleness threshold). | Reliability | Medium | Accepted |
| NFR-005 | The added reducer fold introduces no more than a negligible (**<5%**) increase in `reduce()` wall-time on a representative 500-event mission snapshot. | Performance | Medium | Accepted |

### Constraints

| ID | Constraint | Category | Priority | Status |
|----|------------|----------|----------|--------|
| C-001 | Migration MUST follow `backfill → verify → reader cutover → writer cutover` ordering; writer-first is prohibited (the B3 clobber window). | Technical | High | Accepted |
| C-002 | `WPInnerStateDelta` MUST be a typed partial (typed optional fields), never a free `dict[str, Any]` — no re-introduced split-brain. | Technical | High | Accepted |
| C-003 | Every new emit site MUST resolve `destination_ref` from stored topology/target branch; never `Path.cwd()` (the #2647 invariant). | Technical | High | Accepted |
| C-004 | The 9-lane FSM transition matrix (27 pairs) MUST NOT be modified; `InnerStateChanged` bypasses `validate_transition` via a sanctioned non-transition path — it does not add lane self-edges to the matrix. | Technical | High | Accepted |
| C-005 | Out of scope: the static-model authority election (deferred, gated on this landing / #1619); the 3.3.x YAML-authoritative WP-prompt flip (requires #2400-owner re-ratification); the semantic-only content-hash slice (#2686 follow-up). | Scope | High | Accepted |
| C-006 | #2684 is authoritative over the WP-metadata surface; deferred PRs (#2641, #2766, #2612, and #2160's writer work) yield to and rebase onto this mission. | Governance | Medium | Accepted |

### Key Entities

- **`InnerStateChanged`** — the single generic off-axis event; no lane transition; carries a typed
  `WPInnerStateDelta`; reducer-folded; never bumps `force_count`.
- **`WPInnerStateDelta`** — typed partial: `shell_pid?`, `shell_pid_created_at?`,
  `subtasks?: Mapping[str, Status]`, `note?`, `tracker_refs?`.
- **Reduced snapshot (per WP)** — gains typed runtime slots; the single read path for runtime state
  (liveness, done-inference, gates).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001 (AC-1)**: A full WP lifecycle leaves `tasks/WP##.md` bytes and mtime unchanged.
- **SC-002 (AC-2)**: A claimed WP with empty frontmatter resolves live from the snapshot; resume never
  falsely flags stale.
- **SC-003 (AC-3)**: `move-task --to for_review` succeeds on log-recorded subtask completion with
  unchecked `tasks.md`; genuinely-incomplete WPs are refused — the merged red test flips green.
- **SC-004 (AC-4)**: Activity Log / History / review render from events with no content loss.
- **SC-005 (AC-5)**: The dossier content hash of the WP files is stable across the full lifecycle.
- **SC-006 (AC-6)**: Migration is idempotent on the live corpus; snapshot == pre-migration by
  count+value.
- **SC-007 (provenance)**: 0 false-force stamps across the five evidence-gated review-rejection edges;
  the new command-layer emit-force test passes and the existing backward-transition tests are
  reconciled.

## Domain Language *(canonical terms)*

- **Static design-intent** — WP fields authored once at plan/tasks time; stay frontmatter-canonical.
- **Runtime-mutable state** — state written during execution; evicted to the event log (the SSOT).
- **Off-axis / annotation event** — an `InnerStateChanged` record with no lane change; distinct from a
  lane **transition** (a `StatusEvent` with `from_lane`/`to_lane`).
- **Eviction** — moving a runtime field's authority out of the WP file into the event log; the WP file
  is not "derived" (that is the deferred 3.3.x flip), only reduced to static intent.
- **False force** — a persisted `force=True` on an edge that was legal force-free; a provenance
  corruption (FR-015).

## Assumptions

- The seven design decisions (brief §0 / ADR 2026-07-19-1) are settled and not re-litigated here.
- No cluster-touching work is pending; the adjacent PRs are `pr:deferred` and yield to this mission,
  which owns the `implement.py:1730` restructuring (FR-014).
- `lanes` topology is used for parallel execution across the WP-A…WP-F decomposition (brief §10).
