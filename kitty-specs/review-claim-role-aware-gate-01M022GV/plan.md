# Implementation Plan: Role-Aware Review-Claim Gate

**Branch**: `fix/review-claim-role-aware-gate` | **Date**: 2026-08-15 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `kitty-specs/review-claim-role-aware-gate-01M022GV/spec.md`

## Summary

Make the `for_review → in_review` review-claim allow-only (never block on actor/role) so a
distinct agent profile can review another profile's work, and move the genuine
reviewer-vs-reviewer collision to the `in_review` re-claim surface behind **one shared pure
predicate** used by both the state-machine guard and the dedicated-review check. Thread the
already-reduced `role` slot through the transaction-resolved read (as a small value object,
not a widened positional tuple) to every guard-construction site, so the guard reads
lane+actor+role from a single in-transaction reduction (no split-brain). Fold in the
write-side blank-identity fix (#2960) and a #2861 compound-actor regression guard. Hardened,
red-first, on the move-task path.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: standard library + existing internal packages (`specify_cli.status`, `specify_cli.coordination`); no new third-party dependency
**Storage**: append-only `status.events.jsonl` (canonical) reduced in-memory; no schema/store change
**Testing**: pytest (unit + integration via Typer `CliRunner`); FSM parity via `tests/status/fsm_parity_baseline.jsonl`; architectural guard test under `tests/architectural/`; `PWHEADLESS=1 pytest -n auto --dist loadfile`
**Target Platform**: cross-platform CLI (Linux/macOS/Windows), Python 3.11+
**Project Type**: single project (CLI + internal packages)
**Performance Goals**: no measurable change — one extra reduced slot carried on a read already performed; zero added reductions (C-002)
**Constraints**: no new third-party dependency; no store/schema change; build only on the current event-log seam (C-001, not the deferred Beads backend #1168); reuse the single in-transaction reduction (C-002); compose with existing advisory independence machinery (C-003)
**Scale/Scope**: ~5 source files (`status/wp_state.py`, `status/transition_context.py`, `status/models.py`, `status/reducer.py`, `coordination/status_transition.py`, `coordination/status_service.py`, `status/work_package_lifecycle.py`) + ~4 unpack call sites + a focused test set; single P1 bug fix with two high-ROI folds

## Charter Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **ATDD-First (C-011) / DIR-005 — tests with new behavior**: PASS by design. Every FR/NFR is
  pinned by an executable test; the P1 repro is red-first on the move-task path (SC-001), and
  NFR-005 forces the #2861/#2960 regression tests. No behavior lands without a failing-first test.
- **Terminology Canon (Mission, not Feature)**: PASS — artifacts use "mission"/"work package".
- **Regression Vigilance / Pre-existing Failure Reporting**: PASS — NFR-002 enumerates the
  complete wrong-model test set and forbids re-cementing the role-free block; baseline changes
  are review-gated (NFR-003).
- **No suppression / complexity ceiling**: the shared predicate is a small pure function
  (well under the complexity ceiling); no `# noqa`/`# type: ignore` introduced.
- **Single canonical authority**: PASS — role resolved from the one canonical reduction (C-002),
  no second reader (NFR-001). Charter present; no violations to justify in Complexity Tracking.

## Project Structure

### Documentation (this mission)

```
kitty-specs/review-claim-role-aware-gate-01M022GV/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (predicate + wrong-model-test contracts)
└── tasks.md             # Phase 2 (/spec-kitty.tasks — NOT created here)
```

### Source Code (repository root)

```
src/specify_cli/
├── status/
│   ├── wp_state.py                 # TransitionInputs protocol (+current_role); ForReviewState guard -> allow-only; shared predicate call
│   ├── transition_context.py       # TransitionContext (+current_role field)
│   ├── models.py                   # GuardContext (+current_role); actor_identity_str (unchanged; role stays a separate slot)
│   ├── reducer.py                  # FR-008: fold identity on truthiness, not `is not None` (blank never clobbers)
│   ├── work_package_lifecycle.py   # in_review re-claim uses the shared predicate (role-aware); start_review_status first-claim stays allow
│   └── review_claim_predicate.py   # NEW: the single pure allow/collision predicate (both paths import it)
└── coordination/
    ├── status_transition.py        # read_current_wp_state_transactional -> return value object w/ role; _prepare_event guard-construction carries role
    └── status_service.py           # wp_lane_actor_from_events -> surface the reduced role slot

# consumers to update (unpack sites):
#   status/aggregate.py (:733, move-task guard construction :669 carries role)
#   status/work_package_lifecycle.py (:129, :271)
#   merge/done_bookkeeping.py (:305)

tests/
├── specify_cli/status/test_wp_state.py            # re-point for_review->in_review conflict cases
├── status/test_transitions.py                      # re-point conflict/idempotent rows
├── status/fsm_parity_baseline.jsonl                # flip row 1278 + ADD role-carrying collision row
├── unit/status/test_review_claim_transition.py     # re-point the "steal by second actor" cases
├── status/test_work_package_lifecycle.py           # collision now role-aware on in_review re-claim
├── architectural/                                  # NFR-001 guard test (no frontmatter actor/role read)
└── <new>                                           # move-task red-first repro; #2861 + #2960 regressions; predicate unit tests
```

**Structure Decision**: Single project. The change concentrates in the `status/` package
(guard, contexts, reducer, lifecycle, new predicate) plus the two role-dropping reads in
`coordination/`. A new small module `status/review_claim_predicate.py` holds the shared pure
predicate so both enforcement points import one implementation (FR-003).

## Complexity Tracking

*No Charter Check violations — section intentionally empty.*

## Implementation Concern Map

> Concerns are NOT work packages. `/spec-kitty.tasks` translates these into WPs.

### IC-01 — Role on the canonical read path (plumbing)

- **Purpose**: Carry the already-reduced `role` slot from the single in-transaction reduction to every guard-construction site, so the guard can be role-aware without a second read.
- **Relevant requirements**: FR-004, FR-005, NFR-001, C-002.
- **Affected surfaces**: `coordination/status_service.py` (`wp_lane_actor_from_events`), `coordination/status_transition.py` (`read_current_wp_state_transactional` return + `_prepare_event`), `status/models.py` (`GuardContext`), `status/transition_context.py` (`TransitionContext`), `status/wp_state.py` (`TransitionInputs` protocol); consumers `status/aggregate.py`, `status/work_package_lifecycle.py`, `merge/done_bookkeeping.py`.
- **Sequencing/depends-on**: none (foundation for IC-02).
- **Risks**: Return-shape change — prefer a small **frozen value object** over a 3-tuple to avoid positional fragility across ~4 unpack sites. **Two** guard-construction sites (`aggregate.py` move-task and `_prepare_event`); role must reach both or the second silently loses it. **C-005**: `verdict-seam-boundary-hardening-01KZG179` co-edits these coordination reads — confirm its merge state first.

### IC-02 — Shared allow/collision predicate + two enforcement points

- **Purpose**: One pure predicate decides allow vs genuine reviewer collision; the `for_review→in_review` guard becomes allow-only; the `in_review` re-claim becomes role-aware via the same predicate.
- **Relevant requirements**: FR-001, FR-002, FR-003, FR-006.
- **Affected surfaces**: NEW `status/review_claim_predicate.py`; `status/wp_state.py` (`_check_no_review_conflict` → allow-only + predicate); `status/work_package_lifecycle.py` (`_actors_compatible`/in_review re-claim → predicate).
- **Sequencing/depends-on**: IC-01 (needs `current_role` available).
- **Risks**: The `for_review` guard must **never** block on role (also neutralizes the stale-role hazard). Predicate must be blank-safe (FR-006) and read role from the reduced slot, never by splitting the actor (FR-005/#2861). **C-005**: `review-cycle-verdict-seam-rebuild-01KZ2W7W` is the sole other co-editor of `wp_state.py` — confirm merge state / hand-coordinate the guard hunk.

### IC-03 — Blank-identity write-side safety (folds #2960)

- **Purpose**: The canonical reduction must not let a blank annotation clobber a recorded identity/role.
- **Relevant requirements**: FR-008, NFR-005(c).
- **Affected surfaces**: `status/reducer.py` (fold actor/agent identity on truthiness, not `is not None`).
- **Sequencing/depends-on**: none (independent; the read-side twin FR-006 lives in IC-02).
- **Risks**: Scope discipline — only the reducer truthiness arm; the `status doctor` empty-slot arm of #2960 is explicitly out of scope. Do not otherwise reopen `reducer.py` for role (already reduced).

### IC-04 — Test hardening + wrong-model re-point + parity coverage

- **Purpose**: Make the fix falsifiable and prevent silent re-cementing of the bug or the named regressions.
- **Relevant requirements**: NFR-001, NFR-002, NFR-003, NFR-005, SC-001..SC-005.
- **Affected surfaces**: red-first move-task repro (NEW); re-point all four wrong-model encodings (`test_wp_state.py`, `test_transitions.py`, `fsm_parity_baseline.jsonl:1278`, `test_review_claim_transition.py`) + a grep/source guard; parity **flip 1278 AND add** a role-carrying collision row; `#2861` compound-actor + `#2960` blank-actor regressions; architectural guard test (NFR-001); predicate unit tests.
- **Sequencing/depends-on**: repros/guards authored red-first before IC-02; re-point lands with IC-02.
- **Risks**: A literal 1-for-1 parity flip deletes the only reject-branch coverage — the added role-carrying row is mandatory. Missing the fourth wrong-model file (`test_review_claim_transition.py`) tempts a re-assert of the block.
