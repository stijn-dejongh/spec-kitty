# Mission Specification: Role-Aware Review-Claim Gate

**Mission Branch**: `fix/review-claim-role-aware-gate`
**Created**: 2026-08-15
**Status**: Draft
**Input**: Fix the self-review-gate false positive on the `for_review → in_review` review-claim so a reviewer running a different agent profile can review another profile's work package.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - A different profile can review another profile's work (Priority: P1)

A work package is implemented by one agent profile (e.g. an implementer) and then a
*different* profile (e.g. a reviewer) is dispatched to review it. The reviewer claims
the work package for review (moving it from the "for review" state to the "in review"
state). Today this is wrongly refused with "WP already claimed for review by
\<implementer\>", because the claim guard compares the identity that last touched the
work package — which at the "for review" state is the *implementer*, not a prior
reviewer. The reviewer must be able to claim and review the work.

**Why this priority**: This blocks the core two-party review loop the product is built
around — independent review of one agent's work by another. It is a live P1 friction
that stops legitimate work from progressing and, inversely, lets a same-identity
self-review through.

**Independent Test**: Seed a work package whose latest event is an implementer-authored
"submitted for review" transition, then claim it for review as a distinct reviewer
identity/profile. The claim succeeds and the work package enters the "in review" state.

**Acceptance Scenarios**:

1. **Given** a work package in "for review" whose last transition was authored by
   profile A (implementer), **When** profile B (reviewer) claims it for review,
   **Then** the claim is allowed and the work package moves to "in review".
2. **Given** the same work package, **When** the *same* identity that implemented it
   claims it for review, **Then** the claim is allowed (independence stays advisory —
   see Edge Cases) and is surfaced as a review-independence advisory, not a hard block.
3. **Given** a work package already actively "in review" by reviewer B, **When** a
   *different* reviewer C attempts to claim the active review, **Then** a genuine
   reviewer-vs-reviewer collision is refused with a clear message.

---

### User Story 2 - Claim identity is read from one canonical source (Priority: P1)

Whoever asks "who currently holds / last acted on this work package, and in what role?"
— the claim guard, the dashboard, the status command, the sync path — must get the same
answer from the same place: the canonical append-only status event log. The role-aware
claim guard must not introduce a second way to read status/identity that could disagree
with the rest of the system (split-brain).

**Why this priority**: A second identity/role reader that drifts from the canonical one
would reintroduce exactly the class of status-authority bug the event-log model exists to
prevent, and would make the guard's verdict inconsistent with what the operator sees on
the board.

**Independent Test**: Exercise the claim guard and the canonical status read over the
same event stream and assert they resolve the same actor and role for a work package;
assert no code path resolves claim identity from work-package file frontmatter.

**Acceptance Scenarios**:

1. **Given** a work package with a resolved reviewer/implementer role recorded in the
   event log, **When** the claim guard evaluates a review claim, **Then** it obtains the
   current actor *and role* from the same reduction of the event log the rest of the
   system uses, not from a separate reader or from file frontmatter.

---

### Edge Cases

- **Same identity self-review**: When the claiming reviewer is the same identity that
  implemented the work package, the claim is **allowed** but flagged by the existing
  advisory review-independence surface (doctor/preflight) and the existing
  self-review-fallback record. This mission does **not** turn self-review into a hard
  block (a configurable-strictness hard block is deferred to a follow-up).
- **Missing / blank actor**: If the recorded current actor is empty or blank, the guard
  must not treat the blank as a colliding reviewer (it must not block on a blank), and
  must not silently trust a blank as a valid identity.
- **Missing role**: If no resolved role is recorded for the current holder, the guard
  must default to allowing the claim (absence of a positive reviewer-role signal means
  "not a reviewer collision"), never to blocking.
- **Compact actor string**: A structured actor carrying `tool:model:profile:role` must
  be interpreted by its resolved role, not by treating the whole string as the tool
  identity (regression guard for the previously-fixed claim-blocking bug).
- **Canonical `review` command path**: The dedicated review action already emits the
  claim correctly; this mission aligns the `move-task` / state-machine path with it so
  both paths agree.

## Requirements *(mandatory)*

### Functional Requirements

| ID | Title | User Story | Priority | Status |
|----|-------|------------|----------|--------|
| FR-001 | Allow cross-profile review claim | As a reviewer running a different profile than the implementer, I want to claim a completed work package for review so that independent review can proceed. | High | Open |
| FR-002 | Role-aware collision only | As a maintainer, I want a review claim refused only on a genuine reviewer-vs-reviewer collision (an active review already held by a different reviewer) so that legitimate cross-profile review is never blocked. | High | Open |
| FR-003 | Resolve claim role from the canonical event-log seam | As a maintainer, I want the claim guard to obtain the current holder's actor *and role* from the same canonical status reduction the rest of the system uses so that no second identity reader is introduced. | High | Open |
| FR-004 | Surface role on the transactional read path | As a maintainer, I want the transaction-resolved status read (the one the claim guard uses) to carry the already-reduced role slot so the guard reads lane, actor, and role from one reduction over one resolved surface. | High | Open |
| FR-005 | Keep self-review advisory | As a maintainer, I want a same-identity self-review claim to remain allowed-but-advisory (existing independence warning + self-review-fallback record) so this fix does not silently change independence policy. | Medium | Open |
| FR-006 | Align move-task and dedicated-review paths | As a maintainer, I want the state-machine/move-task claim path to agree with the dedicated review action on review-claim semantics so the two cannot diverge. | Medium | Open |
| FR-007 | Reject blank/ambiguous actor safely | As a maintainer, I want the guard to refuse to treat a blank recorded actor as a colliding reviewer and to not trust a blank as a valid identity so attribution gaps cannot cause false blocks or silent passes. | Medium | Open |

### Non-Functional Requirements

| ID | Title | Requirement | Category | Priority | Status |
|----|-------|-------------|----------|----------|--------|
| NFR-001 | Single-source identity (no split-brain) | The claim guard resolves current actor and role from exactly one reduction of the canonical status event log; zero code paths resolve review-claim identity from work-package frontmatter. Verified by test. | Reliability | High | Open |
| NFR-002 | No regression of shipped review flows | 100% of the existing review-cycle, verdict, and status-transition regression suites pass unchanged except the conflict tests deliberately re-pointed by this mission. | Reliability | High | Open |
| NFR-003 | Parity baseline honesty | The state-machine parity baseline is updated by a documented 1-for-1 change reflecting the new cross-review-allowed semantics — no silent baseline regeneration. | Maintainability | High | Open |
| NFR-004 | No new hard gate | Reviewer independence remains advisory: no new state transition is refused for same-identity self-review. Verified by an allowed-self-review-with-advisory test. | Compatibility | Medium | Open |

### Constraints

| ID | Title | Constraint | Category | Priority | Status |
|----|-------|------------|----------|----------|--------|
| C-001 | Current event-log seam only | Build on the current canonical event-log status seam. Do NOT couple to or wait on the deferred state-backend repoint (the Beads-backed backend), which is out of scope and a later release. | Technical | High | Open |
| C-002 | Reuse the canonical reader | Surface role by widening the existing transaction-resolved read that the guard already uses — do NOT call a different status reader (e.g. the typed view reader) inside the guard, which would read a different resolved surface than the adjacent lane/actor check. | Technical | High | Open |
| C-003 | Compose with independence machinery | Integrate with, not duplicate, the existing review-independence advisory surface and the self-review-fallback record and its accounting; do not depend on any accounting field known to be currently inverted. | Technical | High | Open |
| C-004 | Inherit resolved-actor parsing | Read the resolved role from the structured actor; do not reintroduce leaking a compound tool:model:profile:role string into the tool identity (regression of a previously-closed claim-blocking bug). | Technical | High | Open |
| C-005 | Sequence around in-flight seam work | Before implementation, confirm the merge state of in-flight verdict/status-write seam missions and sequence to avoid colliding edits to the same status/guard surfaces. | Process | Medium | Open |

### Key Entities *(include if feature involves data)*

- **Status event**: The append-only record of a work-package lane transition, carrying
  the resolved-binding actor (tool, profile, role) that authored it. The canonical
  authority for current lane, current actor, and current role.
- **Resolved role**: The reviewer/implementer (or profile) role associated with the
  actor of the latest reduced transition for a work package — already a first-class
  reduced slot, but not currently surfaced on the transactional read path the guard uses.
- **Review-claim guard**: The rule evaluated on the `for review → in review` transition
  that decides whether a claim is allowed or is a genuine reviewer collision.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A reviewer running a different profile than the implementer can claim and
  enter review on a completed work package in 100% of cases where no other reviewer holds
  an active review (0% false-block rate for cross-profile review).
- **SC-002**: A genuine reviewer-vs-reviewer collision (a second reviewer claiming an
  actively-held review) is still refused in 100% of cases, with a message naming the
  holding reviewer.
- **SC-003**: Claim identity and role resolve identically between the guard and the
  canonical status read for the same work package in 100% of tested cases; 0 code paths
  read review-claim identity from frontmatter.
- **SC-004**: The full existing review-cycle / verdict / status-transition regression
  suites pass, with only the deliberately re-pointed conflict tests and parity-baseline
  row changed and documented.
