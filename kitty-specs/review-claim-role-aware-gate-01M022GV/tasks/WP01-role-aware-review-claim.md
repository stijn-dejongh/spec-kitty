---
work_package_id: WP01
title: Role-aware review-claim gate (atomic)
dependencies: []
requirement_refs:
- FR-001
- FR-002
- FR-003
- FR-004
- FR-005
- FR-006
- FR-007
- NFR-001
- NFR-002
- NFR-003
- NFR-004
- NFR-005
planning_base_branch: fix/review-claim-role-aware-gate
merge_target_branch: fix/review-claim-role-aware-gate
branch_strategy: Planning artifacts for this mission were generated on fix/review-claim-role-aware-gate. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into fix/review-claim-role-aware-gate unless the human explicitly redirects the landing branch.
subtasks:
- T001
- T002
- T003
- T004
- T005
- T006
- T007
history:
- at: '2026-08-15T07:20:00+00:00'
  actor: claude
  note: WP created by /spec-kitty.tasks
agent_profile: python-pedro
authoritative_surface: src/specify_cli/status/
create_intent:
- src/specify_cli/status/review_claim_predicate.py
- tests/status/test_review_claim_role_aware.py
- tests/unit/status/test_review_claim_predicate.py
- tests/architectural/test_review_claim_no_frontmatter.py
execution_mode: code_change
owned_files:
- src/specify_cli/status/wp_state.py
- src/specify_cli/status/review_claim_predicate.py
- src/specify_cli/status/work_package_lifecycle.py
- src/specify_cli/status/aggregate.py
- src/specify_cli/coordination/status_transition.py
- src/specify_cli/coordination/status_service.py
- src/specify_cli/coordination/coherence.py
- src/specify_cli/merge/done_bookkeeping.py
- tests/specify_cli/status/test_wp_state.py
- tests/status/test_transitions.py
- tests/status/fsm_parity_baseline.jsonl
- tests/unit/status/test_review_claim_transition.py
- tests/status/test_work_package_lifecycle.py
- tests/status/test_review_claim_role_aware.py
- tests/unit/status/test_review_claim_predicate.py
- tests/architectural/test_review_claim_no_frontmatter.py
role: implementer
tags: []
tracker_refs: []
---

## ⚡ Do This First: Load Agent Profile

Before reading anything else, load your assigned profile:

```
/ad-hoc-profile-load python-pedro
```

Apply its identity, boundaries, directives, and tactics (TDD/red-first, type safety,
idiomatic Python). State which you applied, then proceed.

## Objective

Fix the self-review-gate false positive: a reviewer running a different agent profile than
the implementer must be able to claim a completed WP for review (`for_review → in_review`),
instead of being refused "WP already claimed for review by \<implementer\>". The refusal
manifests where the holder is resolved from the reduction into the guard — the
`MissionStatus.transition` aggregate seam (`aggregate.py:632/683`, driven by
`agent tasks mark-status`), **not** the `move-task` command (which never sets `current_actor`).
Do it without introducing a second identity reader (no split-brain) and without a new hard
self-review block.

**The design (from plan.md + data-model.md + contracts/ — read them first):**
1. `for_review → in_review` guard (`_check_no_review_conflict`) becomes **hard allow-only**.
2. The one genuine reviewer-vs-reviewer collision site (`in_review` re-claim,
   `work_package_lifecycle.py:307`) becomes role-aware via a new **pure predicate**.
3. Role rides **only** the `CurrentWpState` value object on the transaction-resolved read —
   it is **NOT** added to `GuardContext`/`TransitionContext`/`TransitionInputs`.

This whole change is ONE WP because the value-object return type couples the reads and
`work_package_lifecycle.py`, and the test re-point/parity must co-commit to keep the suite
green.

## Context you must load

- `data-model.md` — the `CurrentWpState` value object, the predicate rules, the single
  enforcement point, and the **best-effort** collision note.
- `contracts/review-claim-predicate.md` — the predicate truth table, the complete four-file
  wrong-model enumeration, and the #2861/#2960 contracts.
- Grounding code: `src/specify_cli/status/wp_state.py:597` (`_check_no_review_conflict`),
  `coordination/status_transition.py:975` (`read_current_wp_state_transactional`),
  `coordination/status_service.py:256` (`wp_lane_actor_from_events`),
  `status/work_package_lifecycle.py:88` (`_actors_compatible`), `:180/:210` (implementer
  claims — **do not touch**), `:307` (in_review re-claim — **this** is the collision site),
  `cli/commands/agent/workflow_executor.py:936,1640-1642` (`_REVIEW_CLAIM_ROLE`, the
  conditional role write).

## Subtasks

### T001 — `CurrentWpState` value object + convert consumers
- Add a frozen `CurrentWpState(lane: Lane, actor: str | None, role: str | None)` (module TBD in `status/`; import-cycle-safe).
- `wp_lane_actor_from_events` (`status_service.py:256`) returns `CurrentWpState`, reading `role` from `reduce(...).work_packages[wp_id].get("role")` in the SAME reduction (no second reduce — C-002). Genesis fallback → `CurrentWpState(GENESIS, None, None)`.
- `read_current_wp_state_transactional` (`status_transition.py:975`) returns `CurrentWpState`.
- Convert every consumer (mypy will flag them): `aggregate.py:733`, `work_package_lifecycle.py:129`/`:271`, `merge/done_bookkeeping.py:305`, plus the direct `wp_lane_actor_from_events` consumers `coordination/coherence.py:260` (`...[0]` → `.lane`) and `merge/done_bookkeeping.py:598`.
- **Do NOT** add `current_role` to `GuardContext`/`TransitionContext`/`TransitionInputs` or thread role through `_prepare_event`/emit/aggregate guard construction (dead plumbing / TOCTOU).

### T002 [P] — Pure `review_claim_predicate` module + unit tests
- New `src/specify_cli/status/review_claim_predicate.py`: `review_claim_decision(current_actor, current_role, requesting_actor, requesting_role) -> ReviewClaimDecision` (ALLOW | COLLISION(holder)). Reviewer-role token set = a local `frozenset({"reviewer"})` (confirm the token against `_REVIEW_CLAIM_ROLE`). Pure leaf, no imports from `wp_state`/`work_package_lifecycle`.
- Rules (data-model.md): (1) blank/None current_actor → ALLOW; (2) current_role not a reviewer-role → ALLOW; (3) same actor → ALLOW (idempotent); (4) reviewer-role holder AND actors differ → COLLISION(holder).
- `tests/unit/status/test_review_claim_predicate.py` — one test per truth-table row (contracts/).

### T003 — `_check_no_review_conflict` → hard allow-only
- Rewrite so it returns ALLOW on actor-identity presence only. It MUST NOT import or evaluate the collision predicate and MUST NOT block on actor or role. Make the allow-only property **explicit** (e.g. no collision branch at all) — do not rely on "input is never a reviewer-role". A stale reviewer role at `for_review` must still ALLOW.
- This one function covers both move-task guard sites and the `emit.py:725/894` sites (they call it).

### T004 — Switch the single collision site to the predicate
- `work_package_lifecycle.py:307` (in_review re-claim): replace the `_actors_compatible(current_actor, actor)` call with `review_claim_decision(...)`, taking `current_role` from the `CurrentWpState.role` read at `:271` (in-lock — the split-brain-free seam). On COLLISION raise `WorkPackageClaimConflict(holder=...)`.
- **Do NOT** modify `_actors_compatible` itself — it is shared with the implementer claims at `:180`/`:210` (`allow_generic_existing=True`), which are out of scope.

### T005 — Red-first acceptance repro (aggregate seam, NOT the move-task command)
- **Surface correction (debbie):** the `agent tasks move-task` command NEVER populates `current_actor` (grep `tasks_move_task.py` — no `current_actor`), so `_check_no_review_conflict` sees `None` → ALLOW even pre-fix; a `move-task --to in_review` integration is GREEN pre-fix (vacuous). The block manifests ONLY where the holder is resolved from the reduction into the guard: **`MissionStatus.transition`** (`aggregate.py:632/683`, driven by `agent tasks mark-status`, `cli/commands/agent/status.py:317`).
- `tests/status/test_review_claim_role_aware.py`: red-first via BOTH — (a) **`MissionStatus.transition`** seeded with a real event stream at `for_review` whose latest event is implementer-authored, a distinct reviewer claiming `in_review` (this reads the reduction → resolves `current_actor` → the guard; genuinely red-pre / green-post); and (b) a unit companion `validate_transition('for_review','in_review', GuardContext(actor=<reviewer>, current_actor=<implementer>))`. **Do NOT** use the `move-task` command as the repro.
- **Capture the pre-fix RED** (the "WP already claimed for review by \<implementer\>" refusal) as evidence in the WP history.
- Add: a reviewer-role (even stale, via a rework cycle) at `for_review` still ALLOWs; and (NFR-004/FR-007) a **same-identity self-review** claim is ALLOWED with **no new hard refusal** — the existing advisory/self-review-fallback surface remains the only independence signal.

### T006 — Re-point wrong-model tests + re-home reject coverage
- **Surface fact (debbie):** post-fix, `_check_no_review_conflict` is allow-only and the collision predicate is wired ONLY at `work_package_lifecycle.py:307`. `GuardContext` / `validate_transition` / the parity baseline carry **no role** and never invoke the predicate — so **no role-carrying reject can be expressed there**. ⚠️ Do NOT add a role field to `GuardContext` or a role check to `_check_no_review_conflict` to make a parity/guard test go green — that **reintroduces the bug**.
- Re-point the FOUR guard/FSM wrong-model files to assert **ALLOW** post-fix (role seeding is inert on these surfaces — they carry no role): `tests/specify_cli/status/test_wp_state.py` (for_review→in_review conflict cases), `tests/status/test_transitions.py`, `tests/unit/status/test_review_claim_transition.py` (the "rejects steal" cases), and `tests/status/fsm_parity_baseline.jsonl:1278` — **flip conflict→allow ONLY** (do not add a role row).
- Add the **FIFTH** file — the one place the genuine reject lives: `tests/status/test_work_package_lifecycle.py::test_start_review_rejects_second_reviewer` (:532) and `test_start_review_noops_same_reviewer`. Re-point so the holder's `role="reviewer"` is seeded via the annotation/binding delta → it still asserts `WorkPackageClaimConflict` at `:307`. Add a companion: a **binding-less** holder (`role=None`) now ALLOWs (records the accepted best-effort degradation).
- Reject-branch coverage lives at the `:307` lifecycle test + T002 predicate row 4 — NOT parity/`validate_transition`.
- Add a grep/source guard: (a) no test re-asserts a role-free distinct-actor block, AND (b) `_check_no_review_conflict`'s body contains no reject / `return False` branch (a dormant branch is invisible to behavioral tests when `current_actor` is None).

### T007 [P] — #2861 (derivation) + NFR-001 (negative control)
- **#2861 must exercise the DERIVATION, not the pure predicate** (the predicate takes role as a separate arg, so a compound string can never reach it — a predicate-only test stays green through a real regression). Seed a compact reduced actor `{tool,model,profile,role}`; run `wp_lane_actor_from_events`; assert the resulting `CurrentWpState.role` comes from the reduced slot and `.actor` == the bare `tool` (never the compound `tool:model:profile:role`).
- NFR-001 architectural test `tests/architectural/test_review_claim_no_frontmatter.py`: assert actor/role in the claim-resolution surface come only from the canonical reduction, never frontmatter (scoped to actor/role; `get_wp_lane` lane genesis fallback permitted). MUST include a **negative control** — a planted frontmatter-read pattern the test demonstrably FIRES on — so it is a real gate, not a tautology. Cover the aggregate + lifecycle paths.

## Branch Strategy

Planning/base branch: `main`. Final merge target: `main`. Execution worktrees are allocated
per computed lane from `lanes.json` after finalize — do not hand-create a worktree; run
`spec-kitty agent action implement WP01 --agent <name>`.

## Definition of Done

- **C-005 pre-commit check**: confirm `review-cycle-verdict-seam-rebuild-01KZ2W7W` (co-edits `wp_state.py`) and `verdict-seam-boundary-hardening-01KZG179` (co-edits the coordination reads) are in the mission base (they appear already-landed; verify).
- Cross-profile review claim works on the **aggregate (`MissionStatus.transition`) seam** (T005 red→green, pre-fix red captured). The `move-task` command is NOT the repro (it never sets `current_actor`).
- `_check_no_review_conflict` is allow-only with **no reject branch in its body**; the collision predicate is wired ONLY at `work_package_lifecycle.py:307`.
- Role rides only `CurrentWpState`; **no `current_role`** on `GuardContext`/`TransitionContext`/`TransitionInputs` (and none was added to make a parity/guard test pass).
- All FIVE wrong-model files handled: the four guard/FSM files assert ALLOW; `fsm_parity_baseline.jsonl:1278` flipped to allow (flip-only); `test_work_package_lifecycle.py:532` re-pointed to assert reject with `role="reviewer"` seeded via binding + a binding-less-ALLOW companion. Grep guard present (no role-free block; no reject branch).
- #2861 exercises the `CurrentWpState` derivation; NFR-001 has a negative control; predicate unit tests (all four rows incl. COLLISION) green; NFR-004 same-identity-advisory test green.
- `_actors_compatible` (:180/:210) untouched.
- `ruff check` + `mypy` clean on all owned source; full status suite green:
  `PWHEADLESS=1 .venv/bin/python -m pytest tests/specify_cli/status tests/status tests/unit/status tests/architectural -k "review_claim or frontmatter or transitions or wp_state or work_package_lifecycle" -p no:cacheprovider -q`

## Reviewer guidance

- Verify the `for_review` guard body has **no** collision / `return False` branch (allow-only in code, not by input shape).
- Verify the reject branch is covered at `work_package_lifecycle.py:307` (the re-pointed `:532` test with role seeded via binding), NOT at parity — and that parity row 1278 was flip-only.
- Verify #2861 tests the derivation (`wp_lane_actor_from_events`), and NFR-001 has a firing negative control.
- Verify collision is best-effort (binding-less → ALLOW companion exists) and no `current_role` leaked onto any guard carrier.
- Verify `_actors_compatible` and the `:180/:210` implementer claims are unchanged.
