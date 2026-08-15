---
work_package_id: WP02
title: Reducer blank-identity fold (#2960 write side)
dependencies: []
requirement_refs:
- FR-008
- NFR-005
planning_base_branch: fix/review-claim-role-aware-gate
merge_target_branch: fix/review-claim-role-aware-gate
branch_strategy: Planning artifacts for this mission were generated on fix/review-claim-role-aware-gate. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into fix/review-claim-role-aware-gate unless the human explicitly redirects the landing branch.
subtasks:
- T008
- T009
- T010
history:
- at: '2026-08-15T07:20:00+00:00'
  actor: claude
  note: WP created by /spec-kitty.tasks
agent_profile: python-pedro
authoritative_surface: src/specify_cli/status/reducer.py
create_intent:
- tests/status/test_reducer_blank_identity.py
execution_mode: code_change
owned_files:
- src/specify_cli/status/reducer.py
- tests/status/test_reducer_blank_identity.py
role: implementer
tags: []
tracker_refs: []
---

## ⚡ Do This First: Load Agent Profile

Before reading anything else, load your assigned profile:

```
/ad-hoc-profile-load python-pedro
```

Apply its identity, boundaries, directives, and tactics (TDD/red-first, type safety). State
which you applied, then proceed.

## Objective

Fold #2960's write-side arm: the canonical reduction must not let a **blank** annotation
clobber a previously-recorded identity/role. This is the write-side twin of WP01's read-side
blank safety (FR-006). Independent of WP01 (different file) — runs in parallel.

## Context you must load

- `spec.md` FR-008 / NFR-005(c); `plan.md` IC-03; `contracts/review-claim-predicate.md`
  (#2960 write-side contract).
- Grounding: `src/specify_cli/status/reducer.py:261-264` — the `_REPLACE_SLOTS` fold loop
  `for name in _REPLACE_SLOTS: value = getattr(delta, name); if value is not None: state[name] = value`;
  and the separate `agent` fold at `~:185` (the PLANNED→CLAIMED claim exception).
  `_REPLACE_SLOTS` (lines ~73-83) has ~9 slots: `role`, `agent`, `agent_profile`, `model`,
  `provider`, `assignee`, `shell_pid`, ... — a blanket `is not None`→truthiness flip changes
  fold semantics for ALL of them.

## Subtasks

### T008 — Identity-slot-scoped truthiness fold
- **Slot census (debbie/renata):** `_REPLACE_SLOTS` has **no `actor` member** — actor rides
  the event, not the delta. The identity slots to guard are `agent`, `agent_profile`, `role`
  (confirm against `_REPLACE_SLOTS` lines ~73-83; `model`/`provider`/`agent_profile_version`
  are identity-ish but left under the existing `is not None` unless a test demands otherwise).
- Change the blank-clobber behavior so a blank/empty value on the identity slots
  (`agent`, `agent_profile`, `role`) never overwrites a recorded one — at the `:261-264`
  fold loop AND the separate `agent` fold at `~:185` (PLANNED→CLAIMED claim exception).
- **Do NOT** blanket-flip the whole `_REPLACE_SLOTS` loop: `assignee=""` must still clear
  (deliberate), `shell_pid=0` must not be dropped. Split the loop / per-slot predicate /
  guard only the identity subset — keep non-identity clearing semantics intact.
- Keep the change minimal and idiomatic; `ruff`/`mypy` clean.

### T009 — #2960 write-side regression
- `tests/status/test_reducer_blank_identity.py`: reduce a stream where a later annotation
  carries `agent: ""` after a non-blank identity was recorded; assert the prior identity
  **survives** (not clobbered to blank).
- **Explicitly** assert a blank `role: ""` (and `agent_profile: ""`) does NOT clobber a
  recorded `role="reviewer"` — this is exactly the slot WP01's best-effort collision reads, so
  a blank clobber would silently degrade every collision to ALLOW.
- Cover the `~:185` fold: a `CLAIMED` claim event carrying `agent: ""` after a recorded agent
  must not blank the recorded agent.

### T010 [P] — Non-identity fold semantics preserved
- Assert `assignee=""` still clears a previously-set assignee (non-identity slot semantics
  unchanged), and add a `shell_pid=0` case proving integer-zero is not dropped by the new
  identity-scoped guard. This is the guard against an over-broad truthiness flip.

## Branch Strategy

Planning/base branch: `main`. Final merge target: `main`. Execution worktrees are allocated
per computed lane from `lanes.json` after finalize — run
`spec-kitty agent action implement WP02 --agent <name>`.

## Definition of Done

- Blank identity annotation never clobbers a recorded identity/role (T009 green).
- `assignee=""` still clears; `shell_pid=0` preserved (T010 green) — the truthiness change is
  scoped to identity slots only.
- The `status doctor` empty-slot arm of #2960 is **out of scope** (separate `doctor.py`).
- `ruff check` + `mypy` clean; `PWHEADLESS=1 .venv/bin/python -m pytest tests/status/test_reducer_blank_identity.py tests/status -k reducer -p no:cacheprovider -q` green.

## Reviewer guidance

- Verify the truthiness change is scoped to identity slots — confirm `assignee=""`/`shell_pid=0`
  regressions exist and pass.
- Verify no behavior change to the review-claim guard (that is WP01's surface).
