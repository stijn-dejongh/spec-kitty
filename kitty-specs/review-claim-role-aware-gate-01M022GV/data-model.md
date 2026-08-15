# Data Model: Role-Aware Review-Claim Gate

No persistent schema changes. The event wire and `status.events.jsonl` are unchanged; `role`
is already a reduced slot. This documents the in-memory shapes the fix adds/extends.

## Value object (new): current WP state from the transactional read

`CurrentWpState` (frozen) — returned by `read_current_wp_state_transactional` and derived by
`wp_lane_actor_from_events` from the single in-transaction reduction.

| Field | Type | Source | Notes |
|-------|------|--------|-------|
| `lane` | `Lane` | reduced `state["lane"]` | unchanged semantics |
| `actor` | `str \| None` | `actor_identity_str(reduced actor)` | tool identity; unchanged |
| `role` | `str \| None` | reduced `state["role"]` | **new** — carried, not re-derived; may be blank/None |

Genesis fallback (unseeded WP) yields `CurrentWpState(GENESIS, None, None)`.

## Guard input contract extension

Add `current_role: str | None = None` to each carrier (default keeps all existing
constructors valid):

- `GuardContext` (`status/models.py`)
- `TransitionContext` (`status/transition_context.py`)
- `TransitionInputs` protocol (`status/wp_state.py`)

Populated at **every** guard-construction site from `CurrentWpState.role`:
- `aggregate.py` move-task construction (`~:669`)
- `_prepare_event` (`coordination/status_transition.py:~872`) — today builds from
  `request.current_actor`; must also carry role or the second evaluation loses it.

## Predicate (new): `review_claim_decision`

Pure function in `status/review_claim_predicate.py`:

```
review_claim_decision(
    current_actor: str | None,
    current_role: str | None,
    requesting_actor: str | None,
    requesting_role: str | None,
) -> ReviewClaimDecision   # ALLOW | COLLISION(holder=<actor>)
```

Rules:
1. Blank/None `current_actor` → **ALLOW** (no positive collision signal; never trust blank).
2. `current_role` is not a reviewer-role → **ALLOW** (implementer/other holder; covers the
   stale-role rework case — the `for_review` guard passes `current_role` but treats
   non-reviewer/blank as allow).
3. `current_actor == requesting_actor` → **ALLOW** (idempotent same-actor re-claim).
4. `current_role` is a reviewer-role AND `current_actor != requesting_actor` → **COLLISION**
   naming the holder.

Enforcement points:
- `for_review → in_review` (`_check_no_review_conflict`): allow-only — it may call the
  predicate but by construction `current_role` there is never a reviewer-role (or is stale),
  so the outcome is always ALLOW. It MUST NOT block.
- `in_review` re-claim (`work_package_lifecycle.py`): the predicate's COLLISION path is the
  genuine reviewer-vs-reviewer gate → `WorkPackageClaimConflict`.

## Reviewer-role vocabulary

"Reviewer-role" is the resolved-binding role token used at review-claim (e.g. `reviewer`).
Sourced from the reduced `role` slot only (never by splitting the actor string — #2861).
Exact token set confirmed against `build_resolved_actor` / the review-claim binding during
implementation.

## State transitions (unchanged FSM; guard semantics only)

```
for_review --claim--> in_review   : ALLOW (never blocks on actor/role)   [was: blocked cross-profile]
in_review  --re-claim-> (conflict) : ALLOW if same actor / non-reviewer holder; COLLISION otherwise
```
