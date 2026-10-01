# Design decisions: coord-artifact-single-home-01M3V4BE

Running log of design choices and their rationale. One entry per decision, 1-3 sentences, dated. The full rationale is in `research.md`.

## Decisions already made (spec and plan, 2026-10-01)

- **Decision ledger partition.** The ledger (`DM-*.md`, `index.json`) is PRIMARY-partition; decision events stay COORD (decision `specify.scope.decision-ledger-partition`).
- **Forked logs.** Detect and guide only, with no automatic merge or re-sequencing (decision `specify.scope.forked-log-recovery`, C-003).
- **Seed mechanism.** Eager materialization at create, committing through the existing coordination commit path. A direct ref commit was rejected (decision `specify.design.seed-mechanism`).
- **Fork check.** Runs at seed time only. Carry over when one event-id sequence is a prefix of the other, and refuse on a true fork. There is no lockout for already-materialized forked Missions (decision `specify.design.fork-check`).
- **Pre-fix coordination-only ledger.** Fixed forward via `doctor decisions --repair`, with no read fallback. Teardown refuses until the repair has run (decision `specify.scope.legacy-ledger`).
- **`planning_commit_sha`.** `finalize-tasks` refreshes it automatically; the opt-in flag's behaviour becomes the default (decision `specify.scope.planning-commit-refresh`).
- **Plan: the accessor is a method on the existing seam.** It is `PlacementSeam.write_dir(kind)`, not a new module or class. The seed body lives in the new `coordination/coord_seed.py`, which calls `materialize_coord_surface_for_write` (`surface_resolver.py`) as its first step; the pure prefix classifier lives in `coordination/event_prefix.py`. (Corrected 2026-10-01: an earlier wording placed the seed in `surface_resolver.py`.) The seam reaches it through a lazy import over the `coordination` edge that `_MISSION_RUNTIME_ALLOWED_SPECIFY_CLI` already lists, so the ledger does not grow (research D1).
- **Plan: seed under the status lock.** The seed runs under the existing per-Mission status lock, which both surfaces already share because it is keyed on the Mission directory name. It runs before the write reduces the log (research D2).

## Entries

- 2026-10-01 (operator rulings on the plan's open questions; recorded as plan Decision Moments):
  - **Q1.** Keep the #4970 refusal for a remote-only coordination branch, with a recovery hint. Materialize-then-write applies only when the local branch exists.
  - **Q2.** NFR-001 is "at most +1.0 s over the measured base median" (about 2.64 s), with no absolute bound.
  - **Q3.** On a post-fix EMPTY surface: restore the Mission dir from the coordination branch tip, warn loudly, then write.
  - **Q4.** The consolidation executor (`executor.py:825`, `:4183`) and `materialize` writers migrate to `write_dir` in this Mission (new IC-18). The FR-014 gate allowlist starts empty.
  - **Q5.** The pre-fix seed commits once on the coordination branch before the triggering write.
  - **Q6.** A refused automatic `planning_commit_sha` refresh warns and continues, keeping the old pin.
- 2026-10-01: Q4 made two existing pins deliberate behaviour changes, not stale tests. Consolidation on an UNMATERIALIZED surface with a local branch now materializes instead of aborting, which re-pins `test_merge_status_commit.py:271` (R23). The completed-Mission `--resume` PRIMARY answer at `executor.py:825` is preserved and pinned by characterization test R1d.
- 2026-10-01 (analyze folds plus brownfield-scout decisions):
  - **C1.** NFR-001 is recorded as an accepted charter deviation (Decision Moment `plan.nfr.create-latency`).
  - **G1.** The ledger committers are narrowed to spec-commit and accept (`plan.scope.ledger-committers`).
  - **#4827.** The orphan fail-closed is kept. The automatic `planning_commit_sha` refresh rides the no-flag preserve-decision path, and Q6's warn-and-continue covers only non-orphan cases.
  - **C-008.** ~~Topology-less residue readers keep today's `decisions/` answer through a shrink-only compatibility set.~~ Superseded 2026-10-01 (round 4) by `plan.design.topology-less-callers`; see the entry below.
  - **Merge drivers.** Paths covered by a merge driver are skipped by planning recency.
  - **Merge-class guard.** ~~`decisions` moves into its divergent set~~ Superseded 2026-10-01 (round 4) by `plan.design.merge-class-guard-set`; see the entry below.
  - **Single write authority.** `write_dir` absorbs `assert_coord_write_materialized` (D22).
  - **PUBLISHED kinds.** They follow the existing E2 resolution (D23).
  - **Post-fix discriminator.** It is a `Spec-Kitty-Coordination-Seed` commit trailer (the branch-tree test over-matched), and the restore copies COORD-kind paths only.
  - **Seed lock.** It uses the owned root, the `coord_mission_dir_name` key and a bounded timeout.
  - **Create rollback.** It tears down the create-owned worktree and branch despite the dirty-worktree refusal.
  - **Imports.** `coord_seed.py` imports `mission_runtime` from the root only.
  - **Matrix writes.** `write_dir` is resolved before the lock.
  - **Review cycle.** `_review_cycle_wp_dir` defaults to `REVIEW_CYCLE`, so readers and writers move together.
  - **Ledger ADR.** The ledger reversal gets its own 4.x ADR.
- 2026-10-01 (analyze re-run folds, round 4; recorded as plan Decision Moments):
  - **I7, `plan.design.merge-class-guard-set`.** `decisions` stays in `_NON_DIVERGENT_COORD_RESIDUE_DIRS`, because the guard hard-asserts the divergent set is `{traces}`. The ruling text is amended, and an assertion requires the `decisions/index.json` driver pattern to be registered.
  - **I8, `plan.design.topology-less-callers`.** The fix lives at one point: `coherence.py` resolves the stored topology from the slug when `topology is None`.
    - `lanes`/`single_branch` keep today's verdict (C-008).
    - Coordination Missions get the PRIMARY ledger rule at every caller.
    - The compatibility set is dropped.
    - Coordination-Mission tests are added at move-task, implement and auto-rebase.
  - **U3, `plan.design.seed-trailer-ownership`.** One constant, `COORD_SEED_TRAILER`, is owned by `coord_seed.py` (WP03) and written by the seed commit (WP03 T015) and create's commit (WP06 T031). A refused seed commit is retried with the trailer by the next seed attempt; there is no router change. The tree-content alternative is removed.
  - **I12.** mark-status is not a commit-outcome consumer; its live write path commits nothing. The tracer-append CLI is.
  - **I13.** FR-017's anchors include the new 4.x ledger ADR.
  - **I9.** If FR-013 touches the `lanes`/`single_branch` receipt, the change is output-only and additive (spec edge case).
