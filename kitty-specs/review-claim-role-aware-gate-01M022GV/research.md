# Research: Role-Aware Review-Claim Gate

Phase 0. Decisions that resolve the plan's design unknowns. No third-party dependency is
added, so the supply-chain planning gate is **N/A** (recorded per the plan template's
supply-chain section).

## D1 — Carry role via a frozen value object, not a widened tuple

- **Decision**: `read_current_wp_state_transactional` returns a small frozen dataclass
  (e.g. `CurrentWpState(lane, actor, role)`) instead of widening the `(Lane, str|None)`
  positional tuple to a 3-tuple.
- **Rationale**: Four unpack sites consume the current tuple (`aggregate.py:733`,
  `work_package_lifecycle.py:129`/`:271`, `merge/done_bookkeeping.py:305`). A positional
  3-tuple is fragile (silent mis-unpack); a named value object makes the new `role` field
  explicit and lets consumers that don't need role ignore it by attribute.
- **Alternatives**: 3-tuple (rejected — positional fragility, adversarial-flagged);
  a parallel second reader for role (rejected — violates C-002 single-reduction rule).

## D2 — One shared pure predicate in a new module

- **Decision**: A new `status/review_claim_predicate.py` holds `review_claim_decision(current_actor, current_role, requesting_actor, requesting_role) -> Allow | Collision`, imported by both `_check_no_review_conflict` (FSM guard) and the `in_review` re-claim check in `work_package_lifecycle.py`.
- **Rationale**: FR-003 requires the two enforcement points to share the *logic*, not a call
  site (the FSM has no `in_review→in_review` edge, so a single guard site is impossible). A
  pure, separately-unit-tested predicate is the convergence mechanism and keeps each guard
  small (complexity ceiling).
- **Alternatives**: duplicate the role logic in both places (rejected — this is exactly the
  FR-006-original drift the squad flagged).

## D3 — `for_review → in_review` is allow-only

- **Decision**: The `for_review` guard never blocks on actor or role; it only enforces
  actor-identity presence (unchanged). Collision detection lives solely at the `in_review`
  re-claim.
- **Rationale**: At `for_review` the reduced holder is structurally the implementer (and can
  be a *stale* reviewer after a rework cycle). Any block-on-role there is either the original
  false-positive or the stale-role false-positive. Both squad HIGH/MED findings converge here.
- **Alternatives**: role-aware block at `for_review` (rejected — cannot observe a real
  collision, and re-opens the stale-role false-block).

## D4 — Role resolved from the reduced slot; blank-safe both sides

- **Decision**: Role comes from the reducer's per-WP `role` slot (already latest-wins), surfaced
  through the transactional read. The predicate treats blank actor/role as "no positive
  collision signal" (allow) and never trusts a blank as identity. Reduction folds identity on
  truthiness (FR-008) so a blank annotation never clobbers a recorded value.
- **Rationale**: Reading role by splitting the actor string re-opens #2861; trusting a blank
  re-opens #2960. Both are pinned by NFR-005 regressions.
- **Alternatives**: string-split the compact actor (rejected — #2861); `is not None` fold
  (rejected — #2960 write-side bug being folded in).

## D5 — Parity coverage is preserved, not just flipped

- **Decision**: `fsm_parity_baseline.jsonl:1278` flips reject→allow (role-free / non-reviewer
  holder), AND a new role-carrying context + row is added asserting the genuine
  reviewer-vs-reviewer reject branch.
- **Rationale**: Row 1278 is the only reject-branch coverage; a literal 1-for-1 flip erases it.
- **Alternatives**: flip-only (rejected — silent coverage loss, debugger HIGH).

## Adversarial evidence disposition (post-spec squad)

Per `contracts/adversarial-evidence-contract.md`: the four-lens post-spec squad's contested
findings are all **accepted** and folded into spec v2 + this plan — collision reframe (D3),
role-thread value object (D1), shared predicate (D2), blank-safety (D4), parity preservation
(D5), and the C-005 sequencing risk (plan IC-01/IC-02 Risks). None deferred, none dropped.

## Post-plan squad disposition (accepted)

A three-lens post-plan squad (python-pedro / paula-patterns / architect-alphonso) converged
on a simplification, all **accepted**: the `for_review` guard is hard allow-only and needs no
role, so `current_role` is dropped from the guard input contract (D1 value object rides only
to the single in-lock collision site `work_package_lifecycle.py:307`). Also accepted:
enroll `coherence.py:260` + `done_bookkeeping.py:598` as value-object consumers; only
`:307` switches to the predicate (`:180`/`:210` unchanged); IC-03 fold is `reducer.py:261-264`
(+`:185`), scoped to identity slots only (don't break `assignee=""`/`shell_pid=0`); collision
is best-effort (role present only with a resolved binding — graceful ALLOW accepted); IC-04
split into red-first (before) + re-point/parity (atomic with IC-02); C-005 downgraded to a
verification step. None deferred, none dropped.

## C-005 sequencing (open risk, resolve before implement)

Two missions co-edit this fix's surface: `review-cycle-verdict-seam-rebuild-01KZ2W7W`
(`wp_state.py`) and `verdict-seam-boundary-hardening-01KZG179` (the coordination reads).
Their merge state is ambiguous in this checkout (status.json all-done but no code branch /
no ULID-bearing commit on main). **Action**: confirm merge state at implement time; land them
first or hand-coordinate the specific hunks. Upstream/main moved 18 commits during planning
but did **not** touch this mission's edit surface (verified).
