---
work_package_id: WP06
title: Route the agent-CLI and lifecycle shells
dependencies:
- WP03
requirement_refs:
- FR-004
- FR-015
- FR-024
- NFR-001
- NFR-002
planning_base_branch: fix/read-side-seam-primary-primitive-closure
merge_target_branch: fix/read-side-seam-primary-primitive-closure
branch_strategy: Planning artifacts for this mission were generated on fix/read-side-seam-primary-primitive-closure. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into fix/read-side-seam-primary-primitive-closure unless the human explicitly redirects the landing branch.
subtasks:
- T029
- T030
- T031
phase: Phase 3 - Route
history:
- at: '2026-07-28T09:27:08Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: python-pedro
authoritative_surface: src/specify_cli/cli/commands/
create_intent:
- tests/specify_cli/cli/commands/test_lifecycle_read_seam_migration.py
execution_mode: code_change
model: claude-sonnet-5
owned_files:
- src/specify_cli/cli/commands/agent/mission_feature_resolution.py
- src/specify_cli/cli/commands/agent/mission_finalize.py
- src/specify_cli/cli/commands/agent/tasks_move_task.py
- src/specify_cli/cli/commands/accept.py
- src/specify_cli/cli/commands/next_cmd.py
- src/specify_cli/merge/executor.py
- src/specify_cli/retrospective/writer.py
- tests/specify_cli/cli/commands/test_lifecycle_read_seam_migration.py
role: implementer
tags: []
task_type: implement
tracker_refs: []
---

# Work Package Prompt: WP06 – Route the agent-CLI and lifecycle shells

## ⚡ Do This First: Load Agent Profile
Use `/ad-hoc-profile-load` to load `python-pedro` (implementer, claude).

## Objective

Route the **10** `primary_feature_dir_for_mission` sites across the agent-CLI and
lifecycle-shell cluster, and correct the one husk comment in `next_cmd.py`.

This is the most mechanical of the routing WPs — no gate coupling, no foundation sites, no
non-compliant site. It runs fully in parallel with WP05 and WP07 (disjoint files).

## Context & Constraints

Follow **the shared migration procedure** in [tasks.md](../tasks.md) — read it before starting.

**Site distribution** (census on this base — re-derive before starting):

| File | Sites | Notes |
|---|---|---|
| `cli/commands/agent/mission_feature_resolution.py` | 1 | |
| `cli/commands/agent/mission_finalize.py` | 1 | |
| `cli/commands/agent/tasks_move_task.py` | 2 | |
| `cli/commands/accept.py` | 1 | |
| `cli/commands/next_cmd.py` | 3 | **+ 1 husk comment** |
| `merge/executor.py` | 1 | |
| `retrospective/writer.py` | 1 | has a dedicated home resolver — see T029 |

- **The ledger is the authority** (`docs/development/read-side-seam-classification.md`, terminal
  shape from WP02). Apply verdicts; do not re-derive them.
- **NFR-001** — identical resolved directory for a materialized, non-backfilled mission; the only
  permitted delta is the seam's bare-`<slug>` backfill recovery.
- **NFR-002** — no new raises where leniency is the contract. A PRIMARY kind must not begin
  raising on husk / empty / deleted-coord.
- **C-007** — not a bulk edit. Each site gets an individual kind decision.
- **Do not edit any file under `tests/architectural/`.** Those gates belong to WP01 and WP02.

## Doctrine for this WP

- **`tactic:refactoring-strangler-fig`** — reroute cadence only: one caller at a time, **verify
  after each**, delete the legacy path last (WP08 does the deletion).
  `Run: spec-kitty charter context --include tactic:refactoring-strangler-fig`
  **When doing T029**, `next_cmd.py` has 3 sites and `tasks_move_task.py` 2 — verify per site.
  Ten sites batched into one test run makes a divergence unattributable, which is the only thing
  this cadence buys and the only reason it is prescribed.
- **`tactic:change-apply-smallest-viable-diff`** — route the read; leave the surrounding function
  alone. `Run: spec-kitty charter context --include tactic:change-apply-smallest-viable-diff`
- **`DIRECTIVE_041`** — classify every red **STALE / PATCHWORK / VALID**; never retry-to-green.
  Check WP01's `.expected-reds.md` first — a red may be expected-by-design and owned elsewhere.
  `Run: spec-kitty charter context --include directive:DIRECTIVE_041`
- **`tactic:canonical-source-unification`** — reuse the module's existing seam import; do not add
  a per-module read helper.
  `Run: spec-kitty charter context --include tactic:canonical-source-unification`
  **When doing T029** for `retrospective/writer.py` specifically — see the note below.

## Subtasks

### T029 — Route the 10 sites per ledger verdict (FR-004)

Apply the shared procedure per site, verifying after each.

**Kind selection matters.** ~24 of the mission's sites have an unambiguous kind:
`PRIMARY_METADATA`, plus `WORK_PACKAGE_TASK` and `ANALYSIS_REPORT` where the site names those
artifacts. `mission_finalize.py` and `tasks_move_task.py` touch work-package tasks;
`accept.py` touches analysis reports. Pick the kind from **what the site actually reads
downstream**, not from what is least effort. A wrong `kind` argument is **census-invisible by
construction** — no gate catches it.

**`retrospective/writer.py` — check before routing.** The predecessor mission introduced a
dedicated home resolver for retrospective artifacts (`resolve_retrospective_home`). If that is
the idiom for this surface, route through it rather than a bare `read_dir` — adding a second
authority for the same question is the split-brain shape `tactic:canonical-source-unification`
forbids. Confirm against the ledger verdict and say which you used.

**Watch for**: `next_cmd.py`'s sites sit near the husk comment you correct in T030 — handle them
together.

### T030 — Correct the `next_cmd.py` husk comment (FR-015)

One of the six husk-conflating comments lives here. It argues against routing by naming the
**coord-aware / topology-aware** resolver's failure mode — which is true of the *kind-blind*
`resolve_feature_dir_for_mission` and **false** of the kind-aware seam: for a PRIMARY-partition
kind the decision layer short-circuits to PRIMARY *before any coord probe*.

Preserve the **true** warning (the kind-blind resolver does select the husk); remove the
**false** implication about the seam. Correct it in the **same commit** as the call site it
annotates.

### T031 — Behaviour-preservation evidence for the cluster (NFR-001, NFR-002, NFR-003)

Write `tests/specify_cli/cli/commands/test_lifecycle_read_seam_migration.py`:

1. For **representative** migrated sites (at least one per file), a materialized mission
   resolves an **identical** directory pre/post migration.
2. A PRIMARY-kind read on a **husk** mission resolves the primary anchor and does **not** raise;
   same for an empty coord worktree and a deleted coord branch (NFR-002).
3. Red-first (NFR-003): verify by reverting one routed site and observing the failure.
4. Build fixtures under the **session scratchpad**, not a bare `/tmp` path; remove any throwaway
   worktree afterwards.

Do **not** duplicate WP04's husk pin for the other resolver — this is about *your* cluster's
sites.

## Branch Strategy

- Planning/base branch: **`fix/read-side-seam-primary-primitive-closure`**
- Final merge target: **`fix/read-side-seam-primary-primitive-closure`**
- Worktree allocated **per computed lane** from `lanes.json` by `spec-kitty implement WP06`.
  Never hand-construct it; never `git stash` inside a lane worktree.

## Test strategy

```bash
PWHEADLESS=1 SPEC_KITTY_SYNC_MINIMAL_IMPORT=1 uv run pytest \
  tests/specify_cli/cli/commands/ tests/merge/ -q
```

Plus the six C-008 gates (tasks.md §5), `uv run ruff check <changed>`, and project-mode
`uv run python -m mypy --strict src/specify_cli src/charter src/doctrine`.

## Definition of Done

- All 10 sites routed per ledger verdict, each with a kind chosen from what it actually reads,
  verified per site (T029).
- `retrospective/writer.py` routed through the correct authority, with the choice stated.
- The `next_cmd.py` husk comment corrected in the same commit as its call site (T030).
- Behaviour preservation pinned red-first: identical directories for materialized missions; no
  new raises on husk / empty / deleted-coord (T031).
- No edits under `tests/architectural/`.
- `ruff` and project-mode `mypy` clean.
- Finish: commit, `mark-status T029 T030 T031 --status done`, then `move-task WP06 --to
  for_review` and **wait** for the synchronous pre-review gate.

## Risks

- **Wrong `kind` is the invisible error.** No gate catches it; only review does. Trace what each
  site reads downstream before choosing.
- **`retrospective/writer.py`** may need its dedicated home resolver rather than `read_dir` —
  check, do not default.
- A red in the fold-prescription gate on a newly-routed site means WP01's kind-discriminated
  widening did not cover your call shape. Report it as a WP01 gap; do **not** add a local
  exemption.
- Foreign honest-red P0s will appear in your lane (`tests/sync/test_sync_consent_default_deny.py`,
  #3031, marked `fast`). Not yours. Do not touch (C-010).

## Reviewer guidance

1. For each of the 10 sites: does the declared **kind** match what the site actually reads?
2. Was `retrospective/writer.py` routed through the dedicated home resolver where that is the
   surface's idiom, rather than a second authority?
3. Is the behaviour-preservation test **red-first**? Revert a routed site and confirm.
4. Were sites verified **individually**, or batched and tested once at the end?
5. Does the corrected `next_cmd.py` comment keep the true kind-blind warning?
