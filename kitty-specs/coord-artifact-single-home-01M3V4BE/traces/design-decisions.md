# Design decisions: coord-artifact-single-home-01M3V4BE

Running log of design choices and their rationale. One entry per decision, 1-3 sentences, dated. The full rationale is in `research.md`.

## Decisions already made (spec and plan, 2026-10-01)

- **Decision ledger partition.** The ledger (`DM-*.md`, `index.json`) is PRIMARY-partition; decision events stay COORD (decision `specify.scope.decision-ledger-partition`).
- **Forked logs.** Detect and guide only, with no automatic merge or re-sequencing (decision `specify.scope.forked-log-recovery`, C-003).
- **Seed mechanism.** Eager materialization at create, committing through the existing coordination commit path. A direct ref commit was rejected (decision `specify.design.seed-mechanism`).
- **Fork check.** Runs at seed time only. Carry over when one event-id sequence is a prefix of the other, and refuse on a true fork. There is no lockout for already-materialized forked Missions (decision `specify.design.fork-check`).
- **Pre-fix coordination-only ledger.** Fixed forward via `doctor decisions --repair`, with no read fallback. Teardown refuses until the repair has run (decision `specify.scope.legacy-ledger`).
- **`planning_commit_sha`.** `finalize-tasks` refreshes it automatically; the opt-in flag's behaviour becomes the default (decision `specify.scope.planning-commit-refresh`).
- **Plan: the accessor is a method on the existing seam.** It is `PlacementSeam.write_dir(kind)`, not a new module or class. The seed body lives beside `materialize_coord_surface_for_write` in `coordination/surface_resolver.py`. The seam reaches it through a lazy import over the `coordination` edge that `_MISSION_RUNTIME_ALLOWED_SPECIFY_CLI` already lists, so the ledger does not grow (research D1).
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
