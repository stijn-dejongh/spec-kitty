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

**Consumers to convert (complete census — post-plan).** `read_current_wp_state_transactional`
unpack sites: `aggregate.py:733`, `work_package_lifecycle.py:129`/`:271`,
`merge/done_bookkeeping.py:305`. Its delegate `wp_lane_actor_from_events`
(`coordination/status_service.py:256`) also widens and has two *direct* consumers that must
convert or they break: `coordination/coherence.py:260` (uses positional `[...]​[0]` → becomes
`.lane`) and `merge/done_bookkeeping.py:598` (2-tuple unpack). A frozen value object is
non-subscriptable/non-iterable, so mypy catches both — but they must be in IC-01's scope.

## Guard input contract — NO role field (post-plan simplification)

The FSM guard input carriers (`GuardContext`, `TransitionContext`, `TransitionInputs`) are
**not** extended with `current_role`. The post-plan squad (architect + pedro + paula)
established that role does not belong on the guard path at all:

- The `for_review → in_review` FSM guard (`_check_no_review_conflict`) is made **hard
  allow-only** — it consults actor-presence only and never evaluates a collision, so it
  needs no role. Both move-task guard-construction sites call this one function, so the one
  change covers them; the `emit.py:725/894` sites (coord-less topologies) call it too.
- `request.current_actor` on `_prepare_event` is structurally always `None` (dead plumbing);
  threading role there would encode a pre-lock TOCTOU, not a single in-transaction read.

Role therefore rides **only** the `CurrentWpState` value object to the single collision
site (below). This keeps the "one reduction, no split-brain" invariant honest — it holds at
the in-lock re-claim read (`work_package_lifecycle.py:271`), which is the only role consumer.

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

Single enforcement point (the predicate is used at exactly ONE site):
- `in_review` re-claim — the call site `work_package_lifecycle.py:307` switches from
  `_actors_compatible` to `review_claim_decision`; its COLLISION path is the genuine
  reviewer-vs-reviewer gate → `WorkPackageClaimConflict`. `current_role` comes from
  `CurrentWpState.role` (the in-lock read at `:271`). **Do NOT** change `_actors_compatible`
  itself — it is shared with the implementer-claim sites `:180`/`:210`
  (`allow_generic_existing=True`), which are out of scope.
- `for_review → in_review` (`_check_no_review_conflict`): **hard allow-only** — returns
  ALLOW on actor-presence only and MUST NOT invoke the collision arm or consult a COLLISION
  verdict. It does not import or evaluate the predicate. This is the safe resolution of the
  stale-role hazard: even a stale `reviewer` role can never produce a block here because the
  guard never looks at role.

**Best-effort collision (design note).** The reduced `role` slot is populated at review-claim
only when a resolved binding exists (`workflow_executor.py:1640-1642`, `role="reviewer"`
written `if resolved_binding is not None`). A binding-less claim (bare `--agent claude`)
leaves `current_role=None`, so rule 2 fires → ALLOW. Collision detection is therefore
**best-effort**: it fires only when the holder claimed with a resolved binding. This is
accepted — it degrades toward ALLOW, matching the mission's primary goal (never false-block
cross-profile review). Re-pointed "rejects steal" tests MUST seed `role="reviewer"` via the
binding path, or they will (correctly) assert ALLOW.

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
