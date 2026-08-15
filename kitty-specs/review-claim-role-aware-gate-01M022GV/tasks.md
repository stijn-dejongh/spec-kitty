# Tasks: Role-Aware Review-Claim Gate

**Mission**: review-claim-role-aware-gate-01M022GV
**Branch**: `fix/review-claim-role-aware-gate` | **Merge target**: `main`
**Plan**: [plan.md](./plan.md) · **Spec**: [spec.md](./spec.md) · **Data model**: [data-model.md](./data-model.md) · **Contract**: [contracts/review-claim-predicate.md](./contracts/review-claim-predicate.md)

Two work packages. They are **independent** (different files) and run in parallel lanes.
WP01 is the atomic role-aware change (the value object, allow-only guard, predicate, the one
collision-site switch, and all test re-point/parity — kept in one WP because they share
`work_package_lifecycle.py` and must co-commit to keep the suite green). WP02 is the
independent reducer blank-identity fold (#2960 write side).

## Subtask Index

| ID | Description | WP | Parallel |
|----|-------------|----|----------|
| T001 | `CurrentWpState` value object on the transactional reads; convert all consumers | WP01 | |
| T002 | New pure `review_claim_predicate` module + unit tests | WP01 | [P] |
| T003 | `_check_no_review_conflict` → hard allow-only | WP01 | |
| T004 | Switch `work_package_lifecycle.py:307` to the predicate (leave `_actors_compatible` :180/:210) | WP01 | |
| T005 | Red-first move-task acceptance repro + reviewer-role-at-for_review-ALLOW test | WP01 | |
| T006 | Re-point all four wrong-model files; parity flip 1278 AND add a role-carrying collision row; grep guard | WP01 | |
| T007 | #2861 compact-actor regression + NFR-001 architectural guard test | WP01 | [P] |
| T008 | Identity-slot-scoped reducer truthiness fold (`:261-264` + `:185`) | WP02 | |
| T009 | #2960 write-side regression: blank annotation does not clobber recorded identity/role | WP02 | |
| T010 | Non-identity fold semantics preserved (`assignee=""` clears; `shell_pid=0`) | WP02 | [P] |

Completion is event-sourced: `spec-kitty agent tasks mark-status T001 --status done`.

## Work Packages

### WP01 — Role-aware review-claim gate (atomic)

- **Goal**: A distinct agent profile can claim/review another profile's work; the
  `for_review → in_review` guard is hard allow-only; the one genuine collision site
  (`in_review` re-claim) is role-aware via a pure predicate. Role rides only the
  `CurrentWpState` value object (no guard-contract plumbing).
- **Priority**: P1 · **Requirements**: FR-001..FR-007, NFR-001, NFR-002, NFR-003, NFR-005(a,b), SC-001..SC-004
- **Independent test**: red-first move-task repro — a distinct reviewer claims a WP whose
  holder is the implementer → refused pre-fix, allowed post-fix.
- **Subtasks**: T001, T002, T003, T004, T005, T006, T007
- **Depends on**: none
- **Prompt**: [tasks/WP01-role-aware-review-claim.md](./tasks/WP01-role-aware-review-claim.md) (~450 lines)
- **Risks**: return-shape change across 6 consumers (mypy catches); the allow-only property
  must be explicit in code; collision is best-effort (role only present with a resolved
  binding); parity must ADD a collision row, not just flip; all four wrong-model files.

### WP02 — Reducer blank-identity fold (#2960 write side)

- **Goal**: A blank annotation never clobbers a recorded identity/role in the canonical
  reduction — the write-side twin of WP01's read-side blank safety.
- **Priority**: P2 · **Requirements**: FR-008, NFR-005(c)
- **Independent test**: reduce a stream where a later annotation carries `agent:""` → the
  prior recorded identity/role survives; `assignee=""` still clears.
- **Subtasks**: T008, T009, T010
- **Depends on**: none (parallel with WP01)
- **Prompt**: [tasks/WP02-reducer-blank-identity-fold.md](./tasks/WP02-reducer-blank-identity-fold.md) (~220 lines)
- **Risks**: the `_REPLACE_SLOTS` loop folds ~9 slots — scope the truthiness change to
  identity slots only, or a blanket flip breaks `assignee=""`/`shell_pid=0`.

## Pre-implement verification (C-005, from the plan)

Before implementing WP01, confirm `review-cycle-verdict-seam-rebuild-01KZ2W7W` (co-edits
`wp_state.py`) and `verdict-seam-boundary-hardening-01KZG179` (co-edits the coordination
reads) are landed in the mission base. Both appear already-merged (terminal events ~a week
pre-plan, no local branch/worktree); verify, don't budget for concurrency.
