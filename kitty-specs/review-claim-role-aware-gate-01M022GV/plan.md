# Implementation Plan: Role-Aware Review-Claim Gate

**Branch**: `fix/review-claim-role-aware-gate` | **Date**: 2026-08-15 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `kitty-specs/review-claim-role-aware-gate-01M022GV/spec.md`

## Summary

Make the `for_review → in_review` review-claim guard **hard allow-only** (never block on
actor/role) so a distinct agent profile can review another profile's work, and make the one
genuine reviewer-vs-reviewer collision site (`in_review` re-claim, `work_package_lifecycle.py:307`)
role-aware via a pure, unit-tested predicate. Role rides **only** the `CurrentWpState` value
object on the transaction-resolved read (a frozen value object, not a widened tuple) to that
single in-lock collision site — it is NOT threaded onto the guard input contract (dead
plumbing / TOCTOU per the post-plan squad). Fold in the write-side blank-identity fix (#2960,
identity-slot-scoped) and a #2861 compound-actor regression guard. Hardened, red-first, on
the move-task path. Collision detection is best-effort (active only when the holder claimed
with a resolved binding).

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: standard library + existing internal packages (`specify_cli.status`, `specify_cli.coordination`); no new third-party dependency
**Storage**: append-only `status.events.jsonl` (canonical) reduced in-memory; no schema/store change
**Testing**: pytest (unit + integration via Typer `CliRunner`); FSM parity via `tests/status/fsm_parity_baseline.jsonl`; architectural guard test under `tests/architectural/`; `PWHEADLESS=1 pytest -n auto --dist loadfile`
**Target Platform**: cross-platform CLI (Linux/macOS/Windows), Python 3.11+
**Project Type**: single project (CLI + internal packages)
**Performance Goals**: no measurable change — one extra reduced slot carried on a read already performed; zero added reductions (C-002)
**Constraints**: no new third-party dependency; no store/schema change; build only on the current event-log seam (C-001, not the deferred Beads backend #1168); reuse the single in-transaction reduction (C-002); compose with existing advisory independence machinery (C-003)
**Scale/Scope**: source files `status/wp_state.py`, `status/review_claim_predicate.py` (new), `status/work_package_lifecycle.py`, `status/aggregate.py`, `coordination/status_transition.py`, `coordination/status_service.py`, `coordination/coherence.py`, `merge/done_bookkeeping.py` (WP01) + `status/reducer.py` (WP02) + a focused test set. NOT touched: `status/transition_context.py`, `status/models.py` (no `current_role` on the guard contract — post-plan correction). Single P1 bug fix with two high-ROI folds.

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
│   ├── wp_state.py                 # _check_no_review_conflict -> HARD ALLOW-ONLY (actor-presence only, never consults collision). No role on TransitionInputs.
│   ├── reducer.py                  # FR-008: identity-slot fold on truthiness (:261-264 loop scoped to actor/agent/agent_profile/role; + :185 agent fold)
│   ├── work_package_lifecycle.py   # :307 in_review re-claim -> review_claim_decision (role from CurrentWpState.role). :180/:210 _actors_compatible UNCHANGED.
│   └── review_claim_predicate.py   # NEW: pure collision predicate, used at the single collision site only
└── coordination/
    ├── status_transition.py        # read_current_wp_state_transactional -> CurrentWpState(lane, actor, role). NO change to _prepare_event (dead current_actor plumbing).
    └── status_service.py           # wp_lane_actor_from_events -> CurrentWpState (surface reduced role slot)

# CurrentWpState consumers to convert:
#   status/aggregate.py:733 · work_package_lifecycle.py:129/:271 · merge/done_bookkeeping.py:305
#   coordination/coherence.py:260 ([0] -> .lane) · merge/done_bookkeeping.py:598 (wp_lane_actor_from_events direct consumers)
# NOT touched: models.py GuardContext / transition_context.py TransitionContext (no current_role added)

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
(the allow-only guard, the reducer identity-fold, the lifecycle collision call site, the new
predicate) plus the two role-carrying reads in `coordination/`. A new small module
`status/review_claim_predicate.py` holds the pure collision predicate, used at the **single**
collision site (`work_package_lifecycle.py:307`); the `for_review` guard is allow-only and
does not consult it. No `current_role` is added to the guard input contract.

**C-005 posture (downgraded post-plan).** Both co-editor missions
(`review-cycle-verdict-seam-rebuild-01KZ2W7W` → `wp_state.py`;
`verdict-seam-boundary-hardening-01KZG179` → the coordination reads) carry terminal merge/
lane-approved events dated ~a week before this plan and have no local branch/worktree in this
checkout (remote `moes/*review-cycle-read-authority` branches exist). They appear **already
landed**. C-005 is therefore a **pre-implement verification step** ("confirm both are in the
mission base; if so, no hand-coordination"), not a live-conflict budget. Verify before
implement — a stale base resurrects the risk.

## Complexity Tracking

*No Charter Check violations — section intentionally empty.*

## Implementation Concern Map

> Concerns are NOT work packages. `/spec-kitty.tasks` translates these into WPs.

> **Post-plan squad correction (3-way convergence).** Role does NOT belong on the guard
> path. The `for_review` guard is hard allow-only (needs no role); role rides only the
> `CurrentWpState` value object to the single collision site (`work_package_lifecycle.py:307`).
> `current_role` is NOT added to `GuardContext`/`TransitionContext`/`TransitionInputs`, and no
> emit/`_prepare_event`/aggregate guard threading is done. This erases the guard-construction
> census entirely and keeps the single-reduction invariant honest.

### IC-01 — Role on the in-lock re-claim read (value object)

- **Purpose**: Surface the already-reduced `role` slot on the transaction-resolved read so the single collision site can be role-aware — with no second reduction and no guard-path plumbing.
- **Relevant requirements**: FR-004 (revised), FR-005, NFR-001, C-002.
- **Affected surfaces**: `coordination/status_service.py` (`wp_lane_actor_from_events` → return `CurrentWpState` incl. role); `coordination/status_transition.py` (`read_current_wp_state_transactional` → return `CurrentWpState`). Consumers to convert: `status/aggregate.py:733`, `status/work_package_lifecycle.py:129`/`:271`, `merge/done_bookkeeping.py:305` **and** the two direct `wp_lane_actor_from_events` consumers `coordination/coherence.py:260` (`[0]`→`.lane`) and `merge/done_bookkeeping.py:598`.
- **Sequencing/depends-on**: none (foundation for IC-02).
- **Risks**: Return-shape change — a **frozen value object** (`CurrentWpState`) over a 3-tuple; mypy catches the `coherence.py:260` subscript + `done_bookkeeping.py:598` unpack. Do NOT thread role into any GuardContext/TransitionContext/TransitionInputs (dead plumbing / TOCTOU). C-005 (coordination reads) → see Sequencing note.

### IC-02 — Allow-only guard + single role-aware collision predicate

- **Purpose**: Make `_check_no_review_conflict` hard allow-only; make the one genuine collision site role-aware via a pure, unit-tested predicate.
- **Relevant requirements**: FR-001, FR-002, FR-003 (revised), FR-006.
- **Affected surfaces**: `status/wp_state.py` (`_check_no_review_conflict` → **allow-only**, actor-presence only, never consults collision — one function covers the move-task and `emit.py:725/894` sites); NEW `status/review_claim_predicate.py` (pure leaf, `frozenset({"reviewer"})`); `status/work_package_lifecycle.py:307` **only** (in_review re-claim call site → `review_claim_decision`). Do NOT modify `_actors_compatible` (shared with `:180`/`:210` implementer claims).
- **Sequencing/depends-on**: IC-01 (needs role on the value object at `:271`).
- **Risks**: The allow-only property must be **explicit in code** (guard never evaluates a collision), not an emergent "input is never a reviewer-role" — else a stale/future reviewer role re-cements the bug. Collision is **best-effort** (fires only when a resolved binding recorded `role="reviewer"`; binding-less → ALLOW, accepted). Role from the reduced slot only, never by splitting the actor (FR-005/#2861). C-005: `review-cycle-verdict-seam-rebuild-01KZ2W7W` co-edits `wp_state.py` — see Sequencing note.

### IC-03 — Blank-identity write-side safety (folds #2960)

- **Purpose**: The canonical reduction must not let a blank annotation clobber a recorded identity/role.
- **Relevant requirements**: FR-008, NFR-005(c).
- **Affected surfaces**: `status/reducer.py:261-264` (the `_REPLACE_SLOTS` fold loop `if value is not None`) and the separate `agent` fold at `~:185` (PLANNED→CLAIMED exception).
- **Sequencing/depends-on**: none (independent).
- **Risks**: The `_REPLACE_SLOTS` loop folds ~9 slots; a blanket `is not None`→truthiness flip changes fold semantics for **all** (e.g. can't clear `assignee=""`; drops `shell_pid=0`). **Scope the truthiness guard to the identity slots only** (`actor`/`agent`/`agent_profile`/`role`) — split the loop or use a per-slot predicate — leaving the non-identity slots' clearing semantics intact. Add a regression proving `assignee=""` still clears. The `status doctor` empty-slot arm of #2960 stays out of scope.

### IC-04a — Red-first repros + guards (before IC-02)

- **Purpose**: Falsify the bug on the move-task path and lock the invariants before behavior changes.
- **Relevant requirements**: NFR-001, NFR-005, SC-001, SC-003.
- **Affected surfaces**: red-first move-task repro (NEW, exercises `validate_transition`/`move-task`, red on pre-fix); architectural guard test (NFR-001, actor/role never from frontmatter, covers the move-task + emit paths); predicate unit tests; `#2861` compact-actor + `#2960` blank regressions.
- **Sequencing/depends-on**: authored before IC-02 (ATDD red-first).
- **Risks**: The repro MUST exercise the move-task path (the lifecycle path is already green — SC-001). A reviewer-role-at-`for_review` test must still assert ALLOW.

### IC-04b — Wrong-model re-point + parity coverage (atomic with IC-02)

- **Purpose**: Re-point every test encoding the old role-free block and preserve collision coverage.
- **Relevant requirements**: NFR-002, NFR-003, SC-002, SC-004.
- **Affected surfaces**: re-point ALL FOUR wrong-model files (`tests/specify_cli/status/test_wp_state.py`, `tests/status/test_transitions.py`, `tests/status/fsm_parity_baseline.jsonl:1278`, `tests/unit/status/test_review_claim_transition.py`) + a grep/source guard; parity **flip 1278 AND add** a role-carrying collision row; the re-pointed "rejects steal" cases seed `role="reviewer"` via the binding path.
- **Sequencing/depends-on**: co-committed with IC-02 (else the suite is red between WPs).
- **Risks**: A literal 1-for-1 parity flip deletes the only reject-branch coverage — the added role-carrying row is mandatory. Missing the fourth wrong-model file tempts a re-assert of the block.
