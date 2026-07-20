# Implementation Plan: Runtime-State Corpus Cutover

**Branch**: `feat/runtime-state-corpus-cutover` | **Date**: 2026-07-20 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `kitty-specs/runtime-state-corpus-cutover-01KXZ0AX/spec.md`

## Summary

Complete the deferred #2684 corpus cutover: make the reduced event-log snapshot the **unconditional**
authority for work-package runtime state and remove the phase-1 dual-write toggle, following the strict
migration contract `backfill → verify(FAIL-CLOSED) → flip reader+writer → delete fallbacks → reduce`.

Technical approach: the WP03 backfill library (`specify_cli.migration.backfill_runtime_state`) already
implements seed backfill + a fail-closed count+value verify (hardened in #2817). This mission **wires**
that library into two callers — an operator CLI (`spec-kitty migrate backfill-runtime-state`) and an
auto-discovered upgrade migration — through **one shared cutover orchestration helper** (backfill →
verify → atomic per-mission `status_phase` flip), then removes the flag branch across all 12 call
sites, deletes the predicate and the T037 fallbacks, routes the two remaining bypass readers onto the
snapshot seam, and hardens the #2093 invariant to forbid any frontmatter authority read. IC-08 field
reduction is an optional post-cutover tail.

The load-bearing invariant is **fail-closed atomicity**: a mission's `status_phase` is flipped **only**
after its backfill+verify passes; a verify failure aborts before any flip and leaves the deployment on
a consistent, non-partially-flipped state.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: `typer` (CLI surface); existing `specify_cli.status` (reducer/emit/store facade),
`specify_cli.migration.backfill_runtime_state` (backfill + fail-closed verify), `specify_cli.upgrade`
(auto-discovered migration registry); `pytest` / `mypy` / `ruff`
**Storage**: append-only event log (`status.events.jsonl`) as authority; `meta.json` `status_phase` as the
per-mission cutover marker. No database; no network I/O.
**Testing**: `pytest` — unit (CLI + orchestration helper), fault-injection (verify abort paths),
architectural (`test_2093_authority_invariant`, `test_no_dead_symbols`), and the `status` suite. Run
architectural tests **per-file with a timeout**, never the whole directory (it hangs). Use
`uv run --extra test python -m pytest -p no:cacheprovider <FILE>` (bare `python` resolves a sibling
checkout → false greens).
**Target Platform**: Linux / macOS / Windows CLI (developer tool)
**Project Type**: single project (Python CLI package under `src/specify_cli/`)
**Performance Goals**: backfill+verify is linear in mission count, a few seconds per mission on the
dogfood corpus; no network calls; idempotent re-runs seed nothing.
**Constraints**: fail-closed with **zero** tolerated parity mismatches; WP-file byte-stability after
cutover; `ruff` + `mypy` clean with **no** new `# noqa` / `# type: ignore` / per-file ignores; all
event-writing paths resolve via `canonicalize_feature_dir` (never `Path.cwd()`; #2815/#2647 class).
**Scale/Scope**: remove the flag branch at **12 call sites across 11 files**; delete 1 predicate + its
facade alias/`__all__` entry; delete 2 legacy fallback blocks (1 shared with a bypass reader); route 2
bypass readers; empty 1 arch-test tolerated set + rewrite 1 vacuous test arm; un-pin a 15-symbol
dead-symbol frozenset; add 1 CLI command + 1 upgrade migration. Six implementation concerns.

## Charter Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Charter present (`software-dev-default`, DIR-001..013). Relevant gates and this plan's posture:

- **Single canonical authority** (governing principle) — this mission *is* the enforcement: one
  authority (the reduced snapshot), predicate deleted, invariant hardened to forbid any frontmatter
  authority read. ✅ aligned (the whole point).
- **DIR-005 tests for new functionality / ATDD-first (C-011)** — every new branch/helper (CLI command,
  orchestration helper, upgrade migration, bypass-reader reroute) gets focused tests in the same WP,
  including fault-injection for the verify-abort and flip-refusal paths. ✅
- **DIR-006 mypy --strict / Code Quality (no suppression)** — no new blanket ignores; complexity ≤15;
  repeated literals hoisted (Sonar S1192). ✅ (planned as a code-shaping constraint, not cleanup).
- **Git workflow — no direct pushes to origin/main** — mission lands on `feat/runtime-state-corpus-cutover`,
  PR-bound; local `spec-kitty merge` only; operator publishes. ✅
- **Regression Vigilance / Pre-existing Failure Reporting** — the known-P0 reds and the phantom
  `SYNC_DISABLE_ENV_VARS` arch-adversarial red (pre-existing on main, CI-runner artifact) are NOT this
  mission's to fix; attribute before folding. ✅ (recorded in research.md risks).
- **Canonical sources (no improvise)** — reuse the WP03 library and the auto-discovery migration
  registry; do not hand-roll a parallel backfill or a manual migration sequence. ✅

No charter violations requiring Complexity Tracking.

## Project Structure

### Documentation (this mission)

```
kitty-specs/runtime-state-corpus-cutover-01KXZ0AX/
├── plan.md              # This file
├── research.md          # Phase 0 — design decisions + risks
├── data-model.md        # Phase 1 — entities/state (event, snapshot, status_phase marker)
├── quickstart.md        # Phase 1 — operator + upgrade runbook
├── contracts/
│   └── cutover-cli.md    # Phase 1 — CLI + upgrade-migration behavioural contract
└── tasks.md             # Phase 2 (/spec-kitty.tasks — NOT created here)
```

### Source Code (repository root)

```
src/specify_cli/
├── migration/
│   ├── backfill_runtime_state.py       # WP03 library (exists) — backfill + fail-closed verify
│   └── runtime_state_cutover.py        # NEW — shared orchestration: backfill→verify→atomic flip
├── cli/commands/
│   ├── migrate_cmd.py                  # EDIT — add `@app.command("backfill-runtime-state")`
│   ├── implement.py                    # EDIT — remove flag branch (1 site)
│   └── agent/
│       ├── tasks_transition_core.py    # EDIT — remove flag branch
│       ├── tasks_shared.py             # EDIT — remove flag branch
│       ├── tasks_move_task.py          # EDIT — remove flag branch + route ownership bypass reader
│       ├── tasks_mark_status.py        # EDIT — remove flag branch
│       ├── tasks_status_cmd.py         # EDIT — remove flag branch (missed by the brief)
│       ├── workflow_executor.py        # EDIT — remove flag branch
│       └── workflow_cores.py           # EDIT — delete verdict fallback + route review bypass reader (ONE block)
├── status/
│   ├── emit.py                         # EDIT — delete `_phase1_snapshot_authority_active`; keep `_legacy_lane_mirror_enabled`; remove 1 flag branch
│   ├── __init__.py                     # EDIT — drop facade alias + `__all__` entry
│   └── wp_metadata.py                  # EDIT — remove flag branch; (IC-08) reduce inert fields
├── core/
│   └── stale_detection.py              # EDIT — remove flag branch
├── task_utils/
│   └── support.py                      # EDIT — remove flag branch (TWO sites)
├── merge/
│   └── done_bookkeeping.py             # EDIT — delete `_extract_done_evidence` frontmatter synthesis
└── upgrade/migrations/
    └── m_<version>_runtime_state_backfill.py   # NEW — auto-discovered fail-closed upgrade migration

tests/
├── architectural/
│   ├── test_2093_authority_invariant.py   # EDIT — `_SANCTIONED_READER_MODULES` → frozenset(); rewrite vacuous gate-identity arm
│   └── test_no_dead_symbols.py            # EDIT — remove 15-symbol `_CATEGORY_C_DEFERRED_RUNTIME_STATE_BACKFILL_CUTOVER`
├── (status suite)                          # EDIT — reconcile flag-ON/flag-OFF split; delete/re-point dual-write tests
└── (new)                                   # NEW — CLI command, orchestration helper, upgrade migration, #2815 repo-root-write guard
```

**Structure Decision**: Single-project Python CLI. The one net-new module is
`migration/runtime_state_cutover.py` — a thin **shared orchestration seam** (backfill → fail-closed
verify → atomic per-mission `status_phase` flip) consumed by *both* the operator CLI and the upgrade
migration, so the fail-closed atomicity lives in exactly one place (avoids the logical-duplication
trap of two callers re-implementing verify-then-flip). Everything else is edits to existing surfaces.

## Complexity Tracking

*No Charter Check violations — section intentionally empty.*

## Implementation Concern Map

> Concerns are NOT work packages. `/spec-kitty.tasks` translates these into WPs. The **contract order**
> (C-001) is the hard sequencing spine: IC-01 (backfill+verify+flip wiring) must precede IC-03
> (unconditional flip), which must precede IC-04 (delete fallbacks). IC-05 hardens the end-state; IC-06
> is an optional tail.

### IC-01 — Cutover orchestration + operator CLI (backfill → verify → atomic flip)

- **Purpose**: Give the corpus cutover an invocable, fail-closed entry point that seeds runtime state
  as events, verifies count+value parity against the old reader, and flips `status_phase` **only** for
  missions that pass — the load-bearing safety mechanism.
- **Relevant requirements**: FR-001 (dry-run CLI), FR-002 (wire the library's fail-closed verify),
  FR-003 (atomic verify-then-flip; sole `status_phase` writer), NFR-001, NFR-002, NFR-006, C-003.
- **Affected surfaces**: NEW `migration/runtime_state_cutover.py` (orchestration helper);
  `cli/commands/migrate_cmd.py` (new `backfill-runtime-state` command with `--dry-run`,
  `--mission`, whole-corpus default); consumes `backfill_runtime_state_repo` / `run_backfill_and_verify`.
  **Removes** the 15-symbol `_CATEGORY_C_DEFERRED_RUNTIME_STATE_BACKFILL_CUTOVER` frozenset from
  `tests/architectural/test_no_dead_symbols.py` (this WP is the first real caller — un-pin is mandatory
  here or the ratchet trips).
- **Sequencing/depends-on**: none (library exists). This is the spine's first step.
- **Risks**: `status_phase` has no existing writer — this helper is the *only* writer; guard against a
  hand-flip of an unverified mission (refuse-to-flip on non-`ok` verify). Dead-symbol un-pin must land
  in the same WP that adds the caller. `#2815` class: write target via `canonicalize_feature_dir` only.

### IC-02 — Upgrade-path migration (existing deployments)

- **Purpose**: Ensure existing deployments migrate their corpus on `spec-kitty upgrade` so the
  unconditional cutover does not strand un-migrated on-disk WP state; fresh installs no-op.
- **Relevant requirements**: FR-010, NFR-002 (idempotent), NFR-005 (abort safety), C-003.
- **Affected surfaces**: NEW `upgrade/migrations/m_<version>_runtime_state_backfill.py` (self-registers
  via `@MigrationRegistry.register`; version-key ordered to sort **after** the charter folds); reuses
  the IC-01 orchestration helper. NEW `#2815` regression test (no `status.events.jsonl` at repo root).
- **Sequencing/depends-on**: IC-01 (reuses the shared orchestration helper; do not fork verify-then-flip).
- **Risks**: a verify failure must abort the migration step with an operator-actionable message and
  leave no partial flip (NFR-005). Auto-discovery ordering is name-encoded — pick a version prefix that
  sorts after the charter-fold migrations.

### IC-03 — Unconditional reader/writer cutover (flip the flag, delete the predicate)

- **Purpose**: Make the snapshot the authority everywhere by removing the flag-OFF branch and deleting
  the predicate, so runtime writes are event-only and WP files are byte-stable.
- **Relevant requirements**: FR-004 (12 sites / 11 files), FR-005 (delete predicate + facade export),
  NFR-003 (WP-file byte-stability), C-002 (predicate deleted, not defaulted), C-004 (keep
  `_legacy_lane_mirror_enabled`).
- **Affected surfaces**: the 12 call sites in 11 files (see Project Structure); `status/emit.py` (delete
  `_phase1_snapshot_authority_active`, keep `_legacy_lane_mirror_enabled`); `status/__init__.py` (drop
  alias + `__all__`); remove each paired local `from specify_cli.status import …` import.
- **Sequencing/depends-on**: IC-01 (C-001: backfill+verify must be wired+passing before the flip is safe).
- **Risks**: undersizing — the brief said "~10"; the real surface is 12/11 incl. `tasks_status_cmd.py`
  and the double site in `support.py`. Each site collapses *differently* (not a mechanical rename → not
  a bulk edit). Must NOT touch `_legacy_lane_mirror_enabled`.

### IC-04 — Delete T037 legacy fallbacks + route bypass readers onto the snapshot seam

- **Purpose**: Remove the frontmatter fallbacks that synthesised done-evidence / verdict for un-migrated
  WPs (safe only post-backfill) and eliminate the two remaining split-brain bypass readers.
- **Relevant requirements**: FR-006 (delete fallbacks), FR-007 (route bypass readers), C-001 (order).
- **Affected surfaces**: `cli/commands/agent/workflow_cores.py` — `resolve_review_feedback_context`: the
  verdict fallback (FR-006a) and the `review_status`/`review_feedback` bypass reader (FR-007) are the
  **same block** → ONE edit that deletes the fallback and resolves via the snapshot; `merge/done_bookkeeping.py`
  — delete `_extract_done_evidence` frontmatter synthesis (verify the event-sourced done-evidence
  replacement exists first); `cli/commands/agent/tasks_move_task.py` — route the `agent`/`current_agent`
  ownership read onto the snapshot accessor.
- **Sequencing/depends-on**: IC-03 (fallbacks are only safe to delete after the flip; C-001 order) and
  IC-01 (backfill has seeded the approvals as events).
- **Risks**: `done_bookkeeping` feeds the **merge** done path — deleting the synthesis without an
  event-sourced replacement would break merge; verify before delete. FR-006a and FR-007-workflow_cores
  are one block — do not decompose into two edits to the same lines.

### IC-05 — Authority-invariant hardening (#2093) + test-suite reconciliation

- **Purpose**: Lock the single-authority end-state so no frontmatter authority read can regress, and
  reconcile the flag-ON/flag-OFF split test suite to the single end-state.
- **Relevant requirements**: FR-008 (empty tolerated set + rewrite vacuous arm), FR-009 (reconcile
  split suite), C-006 (arch-gate updated not suppressed), SC-003, SC-004, SC-006.
- **Affected surfaces**: `tests/architectural/test_2093_authority_invariant.py` — `_SANCTIONED_READER_MODULES`
  → `frozenset()`, and rewrite the now-vacuous canonical-gate-identity arm (it imports the deleted
  predicate) into a "zero frontmatter-authority reads" assertion; the `status`-suite dual-write
  (flag-OFF) tests — delete or re-point (the flag-ON assertions become unconditional). Add the NFR-003
  byte-stability regression and the #2815 repo-root-write guard if not already added in IC-01/IC-02.
- **Sequencing/depends-on**: IC-03 and IC-04 (the invariant/tests must reflect the end-state).
- **Risks**: the arm rewrite is more than a set edit — the test currently asserts the *identity* of the
  canonical gate symbol, which no longer exists. Keep the guard **non-vacuous** (a reintroduced
  frontmatter read must still fail it).

### IC-06 — IC-08 inert-field reduction (optional tail; the deferred #2684 IC-08)

- **Purpose**: Remove the now-inert `wp_metadata` fields and cosmetic `WP_FIELD_ORDER` slots that fed
  the retired legacy path — pure hygiene, safe only post-cutover.
- **Relevant requirements**: FR-011 (Low / optional / deferrable).
- **Affected surfaces**: `status/wp_metadata.py` (inert field definitions), `WP_FIELD_ORDER` slots; the
  `wp_snapshot_state` accessor dedup already shipped in #2817 so this is field/slot removal only.
- **Sequencing/depends-on**: IC-03 (post-cutover). **Deferrable** — does not gate mission DoD; may split
  to a fresh follow-up issue (then the PR uses `Contributes to #2816`, not `Closes`).
- **Risks**: none behavioural; keep the full suite green; confirm zero live readers before removal
  (the library's `assert_zero_readers` proof).
