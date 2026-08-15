# Mission Specification: Role-Aware Review-Claim Gate

**Mission Branch**: `fix/review-claim-role-aware-gate`
**Created**: 2026-08-15
**Status**: Draft (revised after post-spec adversarial squad)
**Input**: Fix the self-review-gate false positive on `for_review → in_review` so a reviewer running a different agent profile can review another profile's work package.

> **Post-spec squad note (2026-08-15).** A four-lens adversarial squad (architect / reviewer / debugger / planner) found that the original draft mis-located the "reviewer-vs-reviewer collision" onto an FSM edge that can never observe it, under-specified the role plumbing, and had a test strategy an implementer could satisfy without fixing the bug. This revision reframes the work as **one shared allow/collision predicate with two enforcement points**, threads `role` end-to-end, hardens the test strategy against the exact false-positive on the *move-task path*, and folds in the high-ROI write-side twin of the blank-actor fix (#2960).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - A different profile can review another profile's work (Priority: P1)

A work package is implemented by one agent profile and then a *different* profile is
dispatched to review it. The reviewer claims it for review (`for_review → in_review`).
Today, on the **state-machine / move-task path**, this is wrongly refused with "WP
already claimed for review by \<implementer\>", because the claim guard compares the
identity that last touched the work package — which at "for review" is the *implementer*.
(The dedicated `review` action path already allows it, because it does not feed a current
actor into the guard — so the bug is path-specific.)

**Why this priority**: This blocks the core two-party review loop and, inversely, lets a
same-identity self-review through the guard.

**Independent Test (must be red-first on the move-task path)**: Evaluate the review-claim
decision on the **state-machine path** (`validate_transition('for_review','in_review', …)`
with the current holder resolved as the implementer, and/or a `move-task WP## --to in_review`
integration) where a *distinct* reviewer identity/profile claims the work. On the pre-fix
commit this MUST fail (refused); after the fix it MUST pass. A test that only exercises the
dedicated `review`-action path does NOT satisfy this story (it is already green on main).

**Acceptance Scenarios**:

1. **Given** a work package in "for review" whose last transition was authored by an
   implementer identity/role, **When** a distinct reviewer identity/profile claims it for
   review on the move-task path, **Then** the claim is allowed and the WP moves to "in review".
2. **Given** a holder whose recorded role is a **non-reviewer** role (implementer,
   architect, custom), **When** any distinct actor claims the WP for review, **Then** the
   claim is allowed (the `for_review` guard never blocks on role).
3. **Given** a reject→rework→re-review cycle (`in_review → in_progress → for_review`) that
   leaves a **stale** reviewer role on the reduced state, **When** a distinct reviewer
   re-claims the resubmitted WP for review, **Then** the claim is still allowed (stale role
   must not resurrect the false-block).
4. **Given** a work package already actively "in review" held by reviewer B, **When** a
   *different* reviewer C claims it, **Then** the claim is refused as a genuine
   reviewer-vs-reviewer collision naming the holder — enforced at the `in_review` re-claim
   surface (see FR-003), not the `for_review` guard.
5. **Given** a reviewer who already holds an active review, **When** the *same* reviewer
   identity re-issues the claim, **Then** it is allowed (idempotent re-claim, not a collision).

---

### User Story 2 - Claim identity and role come from one canonical source (Priority: P1)

Whoever asks "who currently holds / last acted on this work package, and in what role?" —
the claim guard, the dashboard, the status command, the sync path — must get the same
answer from the same canonical reduction of the append-only status event log. The fix must
not introduce a second identity/role reader that could disagree with the rest of the system.

**Why this priority**: A second reader that drifts reintroduces the split-brain class the
event-log model exists to prevent and makes the guard's verdict inconsistent with the board.

**Independent Test**: A source-level (architectural) guard test asserts that the review-claim
decision path resolves current **actor and role** only from the canonical reduction the
guard already consumes, and that no code path in the claim-resolution surface reads actor or
role from work-package file frontmatter.

**Acceptance Scenarios**:

1. **Given** a work package with a resolved role recorded in the event log, **When** the
   claim decision runs on the move-task path, **Then** current actor and role are read from
   the **single event list already read inside the transaction**, at every guard-construction
   site, not from a second reduction, a different reader, or file frontmatter.

---

### Edge Cases

- **Same-identity self-review**: allowed but flagged by the existing **post-hoc** advisory
  independence surface (doctor/preflight) and the `--self-review-fallback` record. This
  mission does not add a claim-time hard block (deferred: #3445). NFR-004 governs.
- **Stale reviewer role (rework cycle)**: after `in_review(reviewer) → in_progress →
  for_review`, the reduced `role` slot can remain `reviewer` (carry-forward). The `for_review`
  guard must not treat that stale role as a collision — it never blocks on role.
- **Non-reviewer role holder**: a holder with a non-reviewer role → claim allowed.
- **Blank / missing actor or role**: a blank current actor/role must neither block the claim
  (false positive) nor be trusted as a valid identity or recorded as a colliding holder.
- **Compact actor string**: a structured actor `tool:model:profile:role` must be interpreted
  by its **reduced `role` slot**, never by string-splitting the actor into the guard
  (regression of the previously-closed #2861 claim-blocking leak).
- **Two claim paths**: the dedicated `review` action already allows the first claim; this
  mission aligns the move-task path with it and makes the collision gate role-aware via a
  shared predicate (FR-003) so the two cannot diverge again.

## Requirements *(mandatory)*

### Functional Requirements

| ID | Title | User Story | Priority | Status |
|----|-------|------------|----------|--------|
| FR-001 | `for_review → in_review` is allow-only | As a reviewer of a different profile, I want the first review claim to never be refused on the basis of who holds/last-touched the WP, so independent review can proceed. The guard never blocks on actor or role at this edge. | High | Open |
| FR-002 | Genuine collision refused at the in_review re-claim | As a maintainer, I want a second reviewer claiming an already-active review (`in_review` re-claim) refused with a message naming the holder, so real reviewer-vs-reviewer collisions are still caught — enforced on the lifecycle re-claim surface, not the `for_review` guard. | High | Open |
| FR-003 | Single collision predicate; `for_review` guard allow-only | As a maintainer, I want the reviewer-vs-reviewer collision decided by one pure predicate used at the single collision site (the `in_review` re-claim), while the `for_review → in_review` guard is hard allow-only and never consults collision — so there is exactly one collision implementation and the two claim edges cannot drift. | High | Open |
| FR-004 | Carry role on the transaction-resolved read value object | As a maintainer, I want `role` carried from the reduced status slot on the transaction-resolved read (a frozen value object, not a positional tuple) to the in-lock collision site, so the collision reads role from the single in-transaction reduction. Role is NOT added to the guard input contract (`GuardContext`/`TransitionContext`/`TransitionInputs`) — the `for_review` guard is allow-only and needs no role; that plumbing would be dead/TOCTOU-prone. Convert all value-object consumers (incl. the `wp_lane_actor_from_events` direct consumers). | High | Open |
| FR-005 | Resolve role from the reduced slot, never parse the actor | As a maintainer, I want role read from the reduced `role` slot only, never by string-splitting the actor identity, so the #2861 compound-actor leak is not reintroduced. | High | Open |
| FR-006 | Blank/ambiguous actor is claim-safe | As a maintainer, I want a blank current actor/role to neither block the claim nor be trusted as a colliding holder, so attribution gaps cause neither false blocks nor silent passes. | Medium | Open |
| FR-007 | Keep self-review advisory | As a maintainer, I want a same-identity self-review claim to remain allowed-but-advisory (existing post-hoc independence surface + self-review-fallback record), so this fix does not silently change independence policy. | Medium | Open |
| FR-008 | Blank annotation must not clobber recorded identity (folds #2960) | As a maintainer, I want the canonical reduction to fold actor/agent identity on **truthiness**, not `is not None`, so a blank annotation (`agent:""`) never overwrites a previously-recorded identity/role — the write-side twin of FR-006's read-side safety. | Medium | Open |

### Non-Functional Requirements

| ID | Title | Requirement | Category | Priority | Status |
|----|-------|-------------|----------|----------|--------|
| NFR-001 | Single-source identity, guarded architecturally | A source-level architectural test asserts the claim-resolution path resolves **actor and role** only from the canonical reduction and never from frontmatter (scoped to actor/role — the lane genesis fallback is out of scope). Fails if a frontmatter/actor-split read reappears in the claim path. | Reliability | High | Open |
| NFR-002 | Complete wrong-model re-point, no silent re-cement | 100% of existing review-cycle/verdict/status-transition suites pass. The complete set of tests encoding the old role-free block is enumerated and re-pointed: `tests/specify_cli/status/test_wp_state.py` (for_review→in_review conflict cases), `tests/status/test_transitions.py` (the conflict/idempotent rows), `tests/status/fsm_parity_baseline.jsonl:1278`, and `tests/unit/status/test_review_claim_transition.py` (the second-actor "steal" cases). A grep/source guard asserts no test re-asserts a role-free distinct-actor block after the fix. | Reliability | High | Open |
| NFR-003 | Parity coverage preserved, not just flipped | The parity baseline change (a) flips row 1278 from reject to allow (role-free / non-reviewer holder), AND (b) **adds a new role-carrying context + baseline row** exercising the genuine reviewer-vs-reviewer reject branch, so collision coverage is preserved rather than deleted. Both the exact old value and the exact new/added rows are named in the plan. Review-gated (PR diff audit), not test-gated. | Maintainability | High | Open |
| NFR-004 | No new hard gate | Reviewer independence stays advisory: no state transition is newly refused for same-identity self-review. Verified by a test asserting the same-identity claim is allowed and the existing advisory surface is (still) the only signal. | Compatibility | Medium | Open |
| NFR-005 | Regression forcing tests for #2861 and #2960 | Named regression tests: (a) a holder whose actor is the compact `tool:model:profile:role` form with a reduced `role` slot — the guard's role comes from the slot and `actor["tool"]` never carries the compound string (#2861); (b) a blank current actor — claim allowed and blank not recorded as a colliding holder (#2960 read side); (c) a blank annotation does not clobber a prior identity in the reduction (#2960 write side / FR-008). | Reliability | High | Open |

### Constraints

| ID | Title | Constraint | Category | Priority | Status |
|----|-------|------------|----------|----------|--------|
| C-001 | Current event-log seam only | Build on the current canonical event-log status seam. Do NOT couple to or wait on the deferred Beads-backed state backend (#1168); it is a later release. | Technical | High | Open |
| C-002 | One reduction of one already-read event list | Resolve lane, actor, and role from the **single `events` list already read inside the transaction** (the transaction-target-resolved read). Do NOT call a second reader (e.g. the typed view reader) or perform a second reduction inside the guard — even the same reader on the same dir would be a second read that can diverge mid-transaction (coord worktree ahead of the committed ref). | Technical | High | Open |
| C-003 | Compose with independence machinery | Integrate with, not duplicate, the existing advisory independence surface and the self-review-fallback record; do not depend on the `force_count` accounting known to be currently inverted (#3010). | Technical | High | Open |
| C-004 | Inherit resolved-actor parsing (#2861) | Read role from the structured/reduced actor role; do not reintroduce leaking a compound `tool:model:profile:role` string into the tool identity. Forced by NFR-005(a). | Technical | High | Open |
| C-005 | Sequence around co-editing seam missions | Before implement, resolve the merge state of the two collision-watch missions on this fix's real edit surface: `review-cycle-verdict-seam-rebuild-01KZ2W7W` (sole other co-editor of `wp_state.py`) AND `verdict-seam-boundary-hardening-01KZG179` (co-editor of `coordination/status_transition.py` + `status_service.py`, which the FR-004 role-thread widens). Land them first or hand-coordinate the specific hunks; do not reopen `reducer.py` for role (already reduced — except the FR-008 truthiness arm). | Process | High | Open |

### Key Entities *(include if feature involves data)*

- **Status event**: the append-only record of a lane transition, carrying the
  resolved-binding actor (tool, profile, role). Canonical authority for current lane, actor,
  and role.
- **Resolved role**: the reviewer/implementer/profile role of the latest reduced transition
  for a WP — a first-class reduced slot (latest-wins, carry-forward), not currently on the
  transactional read path or the guard input contract.
- **Allow/collision predicate (new)**: a single pure function deciding allow vs genuine
  reviewer collision from (current actor+role, requesting actor+role). Two enforcement
  points: the `for_review → in_review` guard (allow-only) and the `in_review` re-claim check.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: On the move-task path, a reviewer of a different profile than the implementer
  can claim and enter review in 100% of cases where no other reviewer holds an active review
  (0% false-block for cross-profile review); demonstrated by a repro that is red on the
  pre-fix commit and green after.
- **SC-002**: A genuine reviewer-vs-reviewer collision (a second reviewer claiming an
  actively-held `in_review`) is refused in 100% of cases with a message naming the holder —
  asserted on the lifecycle re-claim surface — and this reject branch retains dedicated
  parity/unit coverage (a role-carrying baseline row) after the change.
- **SC-003**: Claim actor and role resolve identically between the guard and the canonical
  status reduction for the same WP in 100% of tested cases; 0 code paths in the claim
  resolution read actor/role from frontmatter (architectural test).
- **SC-004**: The full existing review-cycle / verdict / status-transition suites pass, with
  every enumerated wrong-model encoding re-pointed and no test re-asserting a role-free
  distinct-actor block; the parity baseline preserves collision coverage.
- **SC-005**: A blank annotation never clobbers a previously recorded identity/role in the
  reduction (#2960), and a compact-actor holder resolves its role from the reduced slot
  without leaking the compound string (#2861) — both pinned by regression tests.
