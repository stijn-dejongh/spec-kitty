# Mission Specification: Worktree-Aware Root Resolution & Verdict Parity

**Mission Branch**: `fix/worktree-root-resolution`
**Created**: 2026-08-18
**Status**: Draft
**Mission ID**: `01M0B59R1GMN6N33GSGJFVNBP9`
**Base**: `upstream/main` (tip `31798b6bd9`) · **Topology**: coord
**Input**: Mission brief `.kittify/mission-brief.md` (worktree/clone-aware root resolution + review-verdict CLI parity), operator-ratified scope Tier A+B+C (2026-08-18).

## Overview

A family of root/workspace resolvers answers *"given this working directory, what is the primary checkout?"* by following `.git` file-pointers. Every one of them **treats a standalone clone (a `.git` directory) as its own primary** and **re-anchors a linked-worktree working directory back to the main checkout**. This single seam produces three observable harms across at least a dozen commands: silent cross-checkout writes, false-green guards, and divergent review-verdict behavior between the `agent status emit` and `orchestrator-api transition` surfaces.

This mission fixes that shared root cause (the resolver family) and closes the review-verdict CLI-parity gaps that ride the same seam. It is a concrete fix-slice of the class captured by design spike #3129 and Epic #2624 — not a competing design.

**Grounding note (already-fixed residuals — do not re-implement):** two headline defects the triggering issues described are already fixed on `upstream/main`. The `review_result` reducer projection is fixed (`407ea376c4`, `status/reducer.py:210-215`) and the `doctor mission-state --fix` verdict destruction is fixed (`bec7c25273`, `migration/mission_state.py:1879`). This mission scopes only the *live residuals* around those fixes (see Constraints C-001/C-002).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Honest write target under a worktree or clone (Priority: P1)

A maintainer runs a mission-state-writing command (e.g. `intake`, `doctor … --fix`, `migrate backfill-runtime-state`, `--owned-checkout` mission create) from inside a linked worktree or a standalone clone. Today the resolver silently re-anchors the write to the primary checkout, clobbering a shared slot or mutating the wrong repository while reporting success.

**Why this priority**: This is the root cause. It causes silent data loss / cross-checkout corruption and is the mechanism behind the entire issue cluster. Fixing it is the MVP that delivers the mission's core value.

**Independent Test**: From a linked worktree and from a standalone clone, invoke each in-scope writing command and assert the write lands in the invoking checkout, or the command refuses with a message that names the checkout it would otherwise have written to. No assertion depends on any other user story.

**Acceptance Scenarios**:

1. **Given** a standalone clone (a `.git` directory, not a linked worktree), **When** a mission-state-writing command runs, **Then** the resolver classifies the clone as its own primary is prevented — the command writes into the clone itself and does not re-anchor to an unrelated checkout.
2. **Given** a linked worktree with an untracked shared brief slot, **When** `intake` runs (with or without `--force`), **Then** the brief is written into the invoking checkout, or `intake` refuses and names the exact path it would otherwise have written to; `--force` does not overwrite a shared untracked slot without an identity check.
3. **Given** any in-scope writing command invoked from a worktree, **When** it cannot write into the invoking checkout, **Then** its refusal message names the concrete target checkout path (actionable), rather than a generic error.

---

### User Story 2 - One review-verdict path on both surfaces (Priority: P1)

An agent orchestrator drives a work package from `in_progress` to `done`, including the `in_review` exit, recording a structured review verdict. Today only `orchestrator-api transition` accepts a structured `review_result`; `agent status emit` cannot exit `in_review`, its `--help` documents a non-functional path, and the `for_review` commit-gate is one surface's extra check rather than a shared invariant — and it fails a clone on topology instead of on commits.

**Why this priority**: Without verdict parity the two CLI surfaces disagree on a core lifecycle transition; the `--help` trap actively misleads operators. This is independently valuable and independently testable.

**Independent Test**: Using `agent status emit` alone, walk a WP `in_progress → for_review → in_review → approved → done` with a structured `review_result`, and assert the same `for_review` commit-gate invariant fires identically on both `agent status emit` and `orchestrator-api transition`, and is topology-aware (a clone is not failed on topology).

**Acceptance Scenarios**:

1. **Given** a WP in `in_review`, **When** `agent status emit --review-result-json '<verdict>'` is invoked, **Then** the verdict is validated by the same parser both surfaces use, threaded into the transition, and the WP advances toward `approved`/`done`.
2. **Given** either CLI surface, **When** the `for_review` commit-gate is evaluated, **Then** it enforces the same invariant, is topology-aware, and does not fail a clone on topology instead of on commit state.
3. **Given** `agent status emit --help`, **When** an operator reads it, **Then** every documented example describes a path that actually works (the misleading `in_review` example is corrected).

---

### User Story 3 - Snapshots round-trip and audit clean (Priority: P2)

An operator audits the status event log. Today a review-carrying event row emits `UNKNOWN_SHAPE` audit noise because `review_result` is not registered in the shape registry, and there is no guarantee that every field in a persisted snapshot survives a replay of its log.

**Why this priority**: Integrity/observability hardening. The projection is already correct; this closes the audit-registration and round-trip-guarantee gaps and de-tautologizes the drift test.

**Independent Test**: Replay an event log that carries a `review_result` and assert (a) no field present in the resulting snapshot is absent from the replay, and (b) the event row audits clean with no `UNKNOWN_SHAPE`.

**Acceptance Scenarios**:

1. **Given** a status event carrying `review_result`, **When** the audit shape registry validates the row, **Then** it recognizes `review_result` and emits no `UNKNOWN_SHAPE`.
2. **Given** any persisted snapshot, **When** its event log is replayed, **Then** no field present in the snapshot is missing from the replay (round-trip property holds).
3. **Given** the shape-registry drift test, **When** it runs, **Then** it makes a real assertion (not a tautology) and fails if a persisted shape is unregistered.

---

### User Story 4 - No false-green guard (Priority: P2)

An operator relies on a cutover/branch guard to confirm an artifact is in the expected place. Today a guard can read a redirected (re-anchored) path and report agreement (`branch_matches_target: true`, or a cutover "pass") even though the artifact it validated is not where it actually read it.

**Why this priority**: A false-green guard is worse than a red one — it launders a re-anchor into a success signal. Depends conceptually on US1's resolver fix but is separately testable at the guard boundary.

**Independent Test**: Run `setup-plan` and `migrate backfill-runtime-state` from a linked worktree and assert the guard reports agreement only when the validated artifact lives where it was read — no pass produced from a redirected path.

**Acceptance Scenarios**:

1. **Given** `setup-plan` invoked from a worktree whose mission `meta.json` names a branch, **When** the guard evaluates, **Then** it resolves branch from the invoking checkout / `meta.json`, not the primary, and does not report `branch_matches_target: true` from a redirected read.
2. **Given** `migrate backfill-runtime-state`, **When** it writes runtime state, **Then** it writes into the linked worktree and its cutover guard reads the same path it wrote (no false pass).

### Edge Cases

- A standalone clone whose `.git` is a directory (not a worktree pointer file) must be classified as its own primary, never re-anchored.
- A linked worktree whose ancestor chain contains an explicit containment boundary (`.kittify`) must not have discovery cross that boundary (#2610).
- `intake --force` against a shared untracked slot already written by a *different* mission/worktree must not clobber without an identity check.
- A WP already in a terminal or non-`in_review` lane receiving `--review-result-json` must be rejected consistently on both surfaces.
- A review-cycle write emitting the wrong artifact kind (`WORK_PACKAGE_TASK`) must be corrected on the write side so downstream fact resolution and rehome tests stay consistent (#3563).

## Requirements *(mandatory)*

### Functional Requirements

| ID | Requirement (testable) | Related Issues | Priority | Status |
|----|------------------------|----------------|----------|--------|
| FR-001 | The root-resolution family (`find_repo_root`, `resolve_canonical_root`, `predict_lane_worktree`, `locate_project_root`, `_get_main_repo_root`) MUST distinguish a standalone clone (a `.git` directory) from a genuine primary checkout, and MUST NOT re-anchor a worktree/clone working directory to a different primary when resolving a write target. | root cause / #3129 | High | Open |
| FR-002 | `intake` MUST write the brief slot into the invoking checkout, or refuse and name the target path it would otherwise write to (mirroring `is_worktree_context`); `--force` MUST NOT overwrite a shared untracked slot without an identity check. | #3540 | High | Open |
| FR-003 | `doctor tool-surfaces --fix` MUST be worktree/clone-aware and MUST NOT silently mutate the primary checkout. | #2613 | High | Open |
| FR-004 | `doctor mission-state --audit`/`--fix` MUST be worktree/clone-aware (same `locate_project_root`/`resolve_canonical_root` mechanism). | #3051 | High | Open |
| FR-005 | `migrate backfill-runtime-state` MUST write runtime state into the linked worktree, and its cutover guard MUST read the same path it wrote (no false pass). | #3049 | High | Open |
| FR-006 | `setup-plan` MUST resolve branch from the invoking checkout / mission `meta.json` (not the primary) and MUST NOT report `branch_matches_target: true` from a redirected read. | #3124 | High | Open |
| FR-007 | `--owned-checkout` mission create MUST be reachable — its reads MUST NOT re-anchor to the primary via `.git` follow. | #3449 | Medium | Open |
| FR-008 | cwd-ancestor `.kittify` discovery MUST NOT cross an explicit containment boundary. | #2610 | Medium | Open |
| FR-009 | `doctor mission-state --fix` invoked in a clone MUST NOT silently rewrite the clone and report success (clone re-anchor); the repair manifest MUST enumerate every field it touches, including removed fields. | #3541 | High | Open |
| FR-010 | `agent status emit` MUST accept `--review-result-json`, validated by the same `_parse_review_result_json` both surfaces use, with `review_result` threaded into the `TransitionRequest`; a WP MUST be walkable `in_progress → done` (including the `in_review` exit) through `agent status emit` alone. | #3547, #1734 | High | Open |
| FR-011 | The `for_review` commit-gate MUST be one shared, topology-aware invariant enforced on both `agent status emit` and `orchestrator-api transition`, and MUST NOT fail a clone on topology instead of on commit state. | #3547 | High | Open |
| FR-012 | `agent status emit --help` MUST document only paths that work; the misleading `in_review` example MUST be corrected. | #3547 | Medium | Open |
| FR-013 | The `in_review → approved` guard MUST admit a `ReviewResult` path on both `agent status emit` and `orchestrator-api transition`. | #1734 | High | Open |
| FR-014 | `review_result` MUST be registered in `audit/shape_registry.py` `status_event_row` so a review-carrying event row audits clean (no `UNKNOWN_SHAPE`). | #3543, #3461 | High | Open |
| FR-015 | A round-trip property MUST hold and be tested: no field present in a persisted snapshot is absent from a replay of its event log. | #3543 | High | Open |
| FR-016 | The `shape_registry` drift test MUST be de-tautologized (a real assertion that fails on an unregistered persisted shape), and the coordination-key `UNKNOWN_SHAPE` MUST be addressed on the registry side. | #3461 (registry half) | Medium | Open |
| FR-017 | `review/cycle.py` write-side MUST emit the correct artifact kind (not `WORK_PACKAGE_TASK`); `resolve_review_verdict_facts` MUST be migrated and `test_analysis_report_rehome` re-verified. | #3563 | Medium | Open |
| FR-018 | The coordination-key writer MUST be migrated so persisted coordination-key rows carry the registered shape (no coordination-key `UNKNOWN_SHAPE`), delivered as its own work package sized separately from the registry/drift-test half. | #3461 (writer half) | Medium | Open |

### Non-Functional Requirements

| ID | Title | Requirement (measurable) | Category | Priority | Status |
|----|-------|--------------------------|----------|----------|--------|
| NFR-001 | Red-first regressions | Each release-blocking slice lands with an issue-pinned `@pytest.mark.regression` reproduction that drives the real CLI entry point and is red on `upstream/main`, green after the fix. At least one such test per behavioral invariant (see Success Criteria SC-001…SC-006). | Reliability | High | Open |
| NFR-002 | Zero-issue static gates | All new/changed code passes `ruff` and `mypy` with zero issues and zero warnings; `tests/architectural/` (incl. legacy-terminology guard) is green; no new blanket suppressions. | Quality | High | Open |
| NFR-003 | Actionable refusals | 100% of write-refusal paths name the concrete checkout path they would otherwise have written to; no generic-only refusal message. | Usability | Medium | Open |

### Constraints

| ID | Title | Constraint | Category | Priority | Status |
|----|-------|------------|----------|----------|--------|
| C-001 | Projection already fixed | Do NOT re-implement the `review_result` reducer projection — already fixed by `407ea376c4` (`status/reducer.py:210-215`). Scope only the shape-registry registration + round-trip test. | Technical | High | Open |
| C-002 | Destruction already fixed | Do NOT re-add a verdict-destruction refuse/quarantine fix — already fixed by `bec7c25273` (`migration/mission_state.py:1879`). Scope only manifest honesty + the clone re-anchor. | Technical | High | Open |
| C-003 | #3540 reframed | The `intake` fix targets the shared untracked-slot clobber after a worktree→primary re-anchor, NOT a tracked-file/branch-diff hazard — the brief slots are gitignored (`.gitignore:204-205`). | Technical | High | Open |
| C-004 | Writer migration is its own WP | The #3461 coordination-key writer migration (FR-018) is delivered in this mission as its own work package, sized separately from the registry/drift-test half (FR-016) because it is a write-path migration with a distinct blast radius. | Technical | Medium | Open |
| C-005 | Base & topology | Work is based on `upstream/main` (tip `31798b6bd9`), uses coord topology, and lands on `fix/worktree-root-resolution`. | Technical | High | Open |
| C-006 | Out of scope | Keep separate (distinct mechanism): #3531 (schema-version refuse/teach), #3307/#3451/#3010, #3043/#3065/#3462 (read-seam consolidation), #2626/#2947/#3536 (lane-worktree lifecycle), #2815 (candidate regression coverage only); #3323 folds ONLY if it traces to the same resolver; #3548 is campsite-fold-only when already editing that file. | Business | Medium | Open |

### Key Entities *(include if feature involves data)*

- **Root resolver family**: The set of functions that answer "given this CWD, what is the primary checkout?" (`find_repo_root`, `resolve_canonical_root`, `predict_lane_worktree`, `locate_project_root`, `_get_main_repo_root`). The shared subject of the fix.
- **Checkout kinds**: *Primary checkout* (the canonical main working tree), *linked worktree* (a `.git` pointer file into a primary), *standalone clone* (an independent `.git` directory that is its own primary). The mission's core distinction is clone ≠ (someone else's) primary.
- **`review_result`**: The structured review verdict carried on a status transition event and persisted in the snapshot; must survive replay and audit registration.
- **`for_review` commit-gate**: The invariant guarding the `for_review` transition; must be one shared, topology-aware check across both CLI surfaces.
- **Shape registry row**: The audit descriptor for a status event row; must recognize `review_result` and coordination-key shapes.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: For every in-scope writing command, invocation from a linked worktree or standalone clone either writes into the invoking checkout or refuses naming the target path — 0 silent re-anchored writes across the command set (covers FR-001…FR-009).
- **SC-002**: 0 false-green guards — no `branch_matches_target: true` or cutover "pass" is produced by reading a redirected path (covers FR-005, FR-006).
- **SC-003**: A repair invoked in a standalone clone rewrites the clone itself (or refuses), never an unrelated primary, in 100% of tested clone scenarios (covers FR-009).
- **SC-004**: A WP can be walked `in_progress → done` (including the `in_review` exit) with a structured verdict through `agent status emit` alone; the `for_review` commit-gate produces identical verdicts on both surfaces across the topology matrix; `--help` contains 0 non-functional example paths (covers FR-010…FR-013).
- **SC-005**: A review-carrying event row audits clean (0 `UNKNOWN_SHAPE`), and the snapshot round-trip property holds for 100% of replayed snapshots (covers FR-014…FR-016, FR-018).
- **SC-006**: Each release-blocking slice ships with an issue-pinned red-first regression test that is red on `upstream/main` and green after the fix (covers NFR-001).

## Assumptions

- "Mission type: fix" maps to the canonical `software-dev` mission type carried on the `fix/` branch prefix; there is no separate `fix` mission-type key.
- The coordination-key writer migration (FR-018) is in-mission but delivered as a separately sized WP (operator-confirmed, 2026-08-18).
- `#3323` (repo event-log write) and `#3548` (`_fail()` message drop) are folded only opportunistically per C-006; absent same-resolver tracing they remain out of scope.
- Base tip `31798b6bd9` reflects the already-fixed projection and destruction residuals; re-verify at implement time before writing any regression.

## Lineage / References

- Umbrella design spike: **#3129** ("scoped shadow workspaces"). Parent epics: **#2624** (root & worktree-path detection spine), **#3549** (event-log integrity — #3541/#3543), **#3044** (review-artifact integrity — #3547).
- Already-fixed antecedents: `407ea376c4` (WP07 verdict projection, from mission `review-cycle-verdict-seam-rebuild-01KZ2W7W`, ADR `2026-08-03-1`), `bec7c25273` (corpus-repair allowlist fix).
- Red-main / red-first discipline: ADR `2026-07-17-1`.
- Operator ratified decisions (2026-08-18): Tier A+B+C scope, priority NOT P0 (P1/P2), tracker hygiene done; #3563 filed under #3044.
