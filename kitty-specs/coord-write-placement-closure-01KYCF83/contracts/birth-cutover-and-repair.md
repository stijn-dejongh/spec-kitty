# Contract — Birth-Cutover, Acceptance Lock, and Repair

## Event-sourced authoring (FR-008)
- **Scope**: exactly two paths — claim (`shell_pid`/`agent`) and subtask-completion (`tasks.md` checkboxes), per #2684.
- **Given** a WP is claimed or a subtask completed, **when** the write occurs, **then** it is recorded as an event (not authored to frontmatter/`tasks.md`), so no un-seeded runtime accrues.
- **Bound**: no other authoring path changes (C-002).

## Birth-cutover (FR-009, NFR-003, C-004)
- **Given** a mission is merged and the target commit is durable, **when** the `_bake_mission_number` hook runs, **then** `cutover_mission` reconciles residual runtime and stamps `status_phase`, with `meta.json`/`status_phase` routed to PRIMARY and seed events to COORD via the placement port (FR-002).
- **Idempotent**: a re-run (merge `--resume`, or the one-time migration) seeds 0 events and leaves `status_phase` + the event log byte-identical.
- **Safety**: fires only after the target commit is durable — a merge-abort never leaves a flipped-but-unmerged mission.
- **Sole writer**: reuses `cutover_mission` / `_flip_phase` (no parallel `status_phase` writer).

## Acceptance lock (FR-010, NFR-006, C-003)
- **Given** a mission whose **event log** carries runtime (excluding the self-referential cutover mission), **when** `test_dogfood_corpus_backfilled` runs, **then** it requires `status_phase>=1` + a non-empty snapshot, and preserves the `verify_backfill` parity assertion (no green-wash).
- **Durable**: the lock stays green after ≥3 subsequent mission merges with no manual backfill (SC-001).
- **Migration coexistence**: a regression proves the one-time `migrate backfill-runtime-state` path still cuts over a legacy corpus after FR-008.

## `agent mission repair` (FR-005, NFR-005)
- **Given** a mission with pre-existing content divergence across partitions:
  - **strict-ancestor + clean worktree** → forward-only (fast-forward), zero data loss;
  - **non-ancestor divergence** → **refuse**, emit a unified diff, zero mutation.
- **Bound**: distinct command; `doctor coordination --fix` stays minimized (C-002/C-003).
