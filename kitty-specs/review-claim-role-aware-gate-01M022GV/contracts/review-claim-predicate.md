# Contract: review-claim allow/collision predicate + test surface

Concrete, round-trippable examples the implementation must satisfy verbatim.

## Predicate truth table (`review_claim_decision`)

| current_actor | current_role | requesting_actor | requesting_role | Decision |
|---|---|---|---|---|
| `implementer-ivan` | `implementer` | `reviewer-renata` | `reviewer` | ALLOW (cross-profile) |
| `""` (blank) | `""` | `reviewer-renata` | `reviewer` | ALLOW (blank not trusted, no block) |
| `reviewer-renata` | `reviewer` | `reviewer-renata` | `reviewer` | ALLOW (idempotent same actor) |
| `reviewer-bob` | `reviewer` | `reviewer-renata` | `reviewer` | COLLISION(holder=`reviewer-bob`) |
| `reviewer-renata` (stale after rework) | `reviewer` | `reviewer-cara` | `reviewer` | *at `for_review`*: ALLOW (guard is allow-only; never blocks) |
| `architect-alphonso` | `architect` | `reviewer-renata` | `reviewer` | ALLOW (non-reviewer holder) |

Note: the stale-reviewer row is ALLOW at the `for_review` guard because that guard is
allow-only by construction; the COLLISION path is reachable only at the `in_review` re-claim.

## Two enforcement points

- `for_review → in_review`: never returns a block; on a distinct reviewer it MUST allow (the
  original bug: it returned "WP already claimed for review by <implementer>").
- `in_review` re-claim: returns `WorkPackageClaimConflict(holder=...)` on COLLISION,
  message names the holder.

## #2861 regression (compact actor)

Given a reduced holder actor `{tool: "claude", model: "sonnet", profile: "reviewer-renata", role: "reviewer"}`:
- The predicate's `current_role` is `"reviewer"` from the **reduced slot**.
- `actor["tool"]` MUST equal `"claude"` — never the compound `"claude:sonnet:reviewer-renata:reviewer"`.

## #2960 regression (blank identity)

- Read side: a blank `current_actor` → ALLOW, and blank is not recorded as a colliding holder.
- Write side (FR-008): reducing an annotation with `agent: ""` MUST NOT overwrite a
  previously-recorded non-blank identity/role in the folded snapshot.

## Wrong-model test set to re-point (complete enumeration — NFR-002)

All four locations assert the old role-free distinct-actor block and MUST be re-pointed:

1. `tests/specify_cli/status/test_wp_state.py` — `for_review → in_review` conflict cases (seed `current_actor="reviewer-A"`).
2. `tests/status/test_transitions.py` — the conflict / idempotent / no-prior-actor rows.
3. `tests/status/fsm_parity_baseline.jsonl:1278` — flip reject→allow AND add a role-carrying collision row.
4. `tests/unit/status/test_review_claim_transition.py` — the "rejects steal by second actor" cases.

Plus: a grep/source guard asserting no test re-asserts a role-free distinct-actor block after the fix.

## Architectural guard (NFR-001)

A source-level test over the claim-resolution surface asserts actor/role are resolved only
from the canonical reduction and never from WP-file frontmatter (scoped to actor/role; the
lane genesis fallback via `get_wp_lane` is permitted and out of scope).
