# Mission Specification: Review Verdict Write Integrity

**Mission Branch**: `research/3044-review-artifact-topology-seam`
**Created**: 2026-08-02
**Status**: Draft
**Input**: GitHub issue #3044 ("Epic: review-artifact integrity — approval must write a real verdict, and no cycle may fabricate one"), scoped by the pre-spec research at `docs/plans/investigations/review-artifact-write-integrity-3044.md` and revised by a post-spec adversarial squad. Corroborated scope: add a missing approved-verdict writer (closes #2275's residual gap + #2996(a)); harden the rejected-verdict writer's feedback-source provenance validation against both fabrication and content-wrapping (closes #2996(b) and #990 — folded in after the squad found both are the identical mechanism); fix the independent coord-topology review-artifact write/read authority split (#2646, #2697). #1817 was verified and closed as a stale duplicate of the already-fixed #1924 directly on the tracker — it is not mission scope.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - A rejected work package reaches a durable approval (Priority: P1)

A work package (WP) is rejected on review cycle N. The implementer fixes it, and a reviewer re-reviews and approves it. Today, `move-task --to approved` accepts the transition and advances the WP's status, but persists no artifact recording that decision — cycle N's `rejected` verdict remains the highest-numbered, authoritative artifact. Every downstream terminal gate (`move-task --to done`, `spec-kitty merge`) reads that stale artifact and refuses, forcing the reviewer or operator to reach for `--skip-review-artifact-check` — a flag intended for genuine arbiter overrides — just to get an ordinary approval to stick.

**Why this priority**: This is the mission's P0-rated core defect (#2275's residual gap, #2996(a)). Without it, no other requirement in this mission matters — the escape hatch remains mandatory for the normal path, and every terminal gate keeps trusting evidence no reviewer actually wrote.

**Independent Test**: Reject a WP (cycle 1, `rejected`), then approve it via the normal `move-task --to approved` path with no override flag. Confirm a new highest-numbered `review-cycle-(N+1).md` exists with `verdict: approved`, a real `reviewer_agent`, and that `spec-kitty merge --dry-run` no longer blocks on `REJECTED_REVIEW_ARTIFACT_CONFLICT` for that WP.

**Acceptance Scenarios**:

1. **Given** a WP whose highest-numbered review-cycle artifact has `verdict: rejected`, **When** a reviewer transitions it to `approved` through the normal review path, **Then** a new review-cycle artifact is persisted with `verdict: approved`, a real (non-`unknown`) `reviewer_agent`, and the next sequential cycle number.
2. **Given** that newly-approved artifact exists, **When** `spec-kitty merge --dry-run` runs, **Then** it reports no conflict for that WP and no `--skip-review-artifact-check` override is needed.
3. **Given** a WP approved directly to `--to done` (skipping an intermediate `approved` lane) from a rejected-latest state, **When** the transition completes, **Then** the same approved-artifact persistence occurs — the write is not conditional on which terminal lane is the target.

---

### User Story 2 - A rejection cycle cannot be filed as someone else's fabricated or wrapped review (Priority: P1)

Creating a rejection artifact accepts any file as the "feedback source" without checking what it actually is. If that source is itself a prior cycle's own review artifact for the same WP — whether by tooling error, manual mistake, or a renamed/copied variant of that prior artifact's content — the new cycle is filed as a duplicate of the old one, with fresh (often synthetic `reviewer_agent: unknown`) frontmatter wrapped around it. The artifact reads as though a second, independent review happened when none did.

**Why this priority**: This is #2996(b) and #990 — the fabrication and content-wrapping halves of the P0 epic, confirmed by a post-spec code trace to be the **identical mechanism** in the identical function (`create_rejected_review_cycle`'s unvalidated `feedback_source` read), not two separate defects. Both are reproducible today: `tests/review/test_cycle.py::test_self_referential_feedback_source_is_rejected` and `::test_new_cycle_body_never_duplicates_a_prior_cycle_file` are currently RED on `main`.

**Independent Test**: Attempt to create a rejection review-cycle artifact whose `feedback_source` is a prior `review-cycle-N.md` for the same WP (exact path, or a renamed/copied file carrying that prior cycle's content). Confirm the operation is refused rather than silently writing a duplicate/wrapped artifact under synthetic frontmatter.

**Acceptance Scenarios**:

1. **Given** WP02 already has `review-cycle-1.md`, **When** a rejection is filed with `--review-feedback-file` pointing at that same `review-cycle-1.md`, **Then** the operation fails with a clear error instead of writing a `review-cycle-2.md` that duplicates cycle 1's body under synthetic frontmatter.
2. **Given** a feedback source whose *content* (not just its path) is a copy of a prior cycle's frontmatter+body — e.g. a renamed duplicate of `review-cycle-1.md` — **When** a rejection is filed against it, **Then** the operation is refused on the same grounds as scenario 1; detection is not defeated by a simple rename.
3. **Given** a genuine, distinct feedback file, **When** a rejection is filed normally, **Then** the artifact is created exactly as before — the new validation does not reject legitimate rejections.

---

### User Story 3 - A coord-topology review decision is visible to every consumer, not split across surfaces (Priority: P2)

In `lanes_with_coord` missions, a review-cycle artifact's canonical write can land on the coordination authority while at least one consumer (the `agent tasks status` stale-verdict scan) reads a different, PRIMARY-only surface — and a rejection transition can duplicate the artifact and split its accompanying task/status mutations across both surfaces instead of writing and committing one canonical record. An approved WP can therefore continue to display a stale rejection warning, and a rejection can leave no single authoritative committed record.

**Why this priority**: #2646 and #2697 are independent, differently-shaped defects from #2275/#2996/#990 — a genuine coord/primary write-and-read authority split for coord-topology missions, not a missing writer or a content-provenance gap. The operator chose to fix these for real in this mission rather than split them into a fast-follow.

**Independent Test**: Reproduce #2646 (cycle 1 rejected, cycle 2 approved and committed on the coord authority for a `lanes_with_coord` mission) and confirm `agent tasks status` reports the WP approved with no stale-verdict warning. Reproduce #2697 (a rejection transition in a coord-topology mission) and confirm exactly one canonical review artifact is written and committed, with lifecycle mutations routed transactionally rather than split across primary and coordination surfaces.

**Acceptance Scenarios**:

1. **Given** a `lanes_with_coord` mission where a WP's cycle 2 approval is committed on the coordination authority, **When** `agent tasks status` runs its stale-verdict scan, **Then** it reads from the same authority the write landed on and reports no stale rejection for that WP.
2. **Given** a coord-topology mission, **When** a WP is rejected via `move-task --to planned --review-feedback-file <feedback>`, **Then** exactly one canonical `review-cycle-N.md` is written and committed — no duplicate across primary and coordination surfaces — and the transition returns its authoritative path/commit.
3. **Given** a flat/single-branch mission, **When** the same transitions run, **Then** behavior is unchanged from today — this fix does not alter non-coord topology.

### Edge Cases

- What happens when a WP has gone through many rejection cycles (cycle N is large) before finally being approved? The approved artifact must still land at the correct next sequential cycle number, not collide with or skip any prior cycle.
- How does the system handle a genuine arbiter/operator override (`--skip-review-artifact-check`) after User Story 1 ships, for a case where an actual code concern is being knowingly waived rather than worked around? The override mechanism itself is out of this mission's rebuild scope (already fixed per #1924, confirmed live in code) — it must continue to work unchanged for genuine override use, now simply no longer *needed* for the ordinary reject→fix→approve path.
- What happens if User Story 3's fix requires touching the same commit-target resolution machinery FR-001's new approved-writer depends on (`_mt_resolve_targets`/branch-checkout assumptions in `tasks_move_task.py`/`tasks_shared.py`)? Treat that overlap as a real architectural dependency to sequence explicitly during planning, not a coincidence to ignore — a plan-phase note, not a spec blocker.
- #1817 is not an edge case of this mission: it was verified as a stale duplicate of #1924 and closed directly on the tracker before planning began.

## Domain Language

- **Review-cycle artifact**: the durable, per-WP, per-cycle record of a review decision (`review-cycle-N.md`: cycle number, verdict, reviewer, affected files, body). The highest-numbered artifact for a WP is the one every terminal gate treats as authoritative.
- **Verdict**: the recorded outcome of a review cycle — `approved`, `rejected`, or `changes_requested`. Avoid "status" as a synonym; status/lane refers to the WP's separate lifecycle-lane state.
- **Override annotation**: an operator/arbiter-authored addendum (`review_artifact_override_*` frontmatter) recording a deliberate decision to treat a rejected-verdict artifact as the approval record. Distinct from an ordinary review decision — reserved for genuine arbitration, not a workaround for a missing writer.
- **Terminal gate**: a transition or merge-time check (`move-task --to approved/--to done`, `spec-kitty merge`'s `REJECTED_REVIEW_ARTIFACT_CONFLICT` invariant) that reads the highest-numbered review-cycle artifact as ground truth.
- **Coordination authority**: for `lanes_with_coord` missions, the coordination branch/worktree that is canonical for lifecycle events; distinct from the PRIMARY partition some artifact kinds resolve to unconditionally.

## Requirements *(mandatory)*

### Functional Requirements

| ID | Title | User Story | Priority | Status |
|----|-------|------------|----------|--------|
| FR-001 | Persist a real approved-verdict artifact on approval | As a reviewer/operator, I want approving a previously-rejected WP to durably persist a new highest-numbered review-cycle artifact with `verdict: approved` and a real `reviewer_agent`, so that terminal gates see an honest recorded decision instead of a stale rejection. | High | Open |
| FR-002 | Refuse rejection artifacts fabricated or wrapped from prior-cycle content | As a reviewer, I want the system to refuse creating a rejection artifact whose feedback source is itself (by path or by content) a prior cycle's own artifact for the same WP, so that a cycle number never implies an independent review that didn't happen and no cycle ever wraps another cycle's material. | High | Open |
| FR-003 | Fix the coord-topology review-artifact write/read authority split | As a maintainer, I want #2646's stale-verdict-scan authority split and #2697's cross-surface duplication fixed for real — the canonical write and every reader agreeing on one authority per topology — not merely verified against an assumption that turned out to be wrong. | Medium | Open |
| FR-004 | Annotate #2275 with its corrected residual scope | As a maintainer, I want #2275 commented on to record that its read-side split is already fixed in code and that this mission closes its remaining write-side gap, so future readers aren't misled by the issue's original wording. *(Completed pre-plan: comment posted, see Assumptions.)* | Low | Done |

### Non-Functional Requirements

| ID | Title | Requirement | Category | Priority | Status |
|----|-------|-------------|----------|----------|--------|
| NFR-001 | No regression to existing review/merge-gate behavior | 100% of pre-existing tests under `tests/review/` and `tests/post_merge/` pass unchanged after this mission's changes. | Reliability | High | Open |
| NFR-002 | Red-then-green coverage for every new behavior | Each of FR-001 through FR-003 has at least one regression test that fails without its fix and passes with it. FR-002's coverage includes the two pre-existing tests already RED on `main` (`test_self_referential_feedback_source_is_rejected`, `test_new_cycle_body_never_duplicates_a_prior_cycle_file`). | Reliability | High | Open |
| NFR-003 | No meaningful performance regression on the approval/merge path | `move-task --to approved` and `spec-kitty merge --dry-run` show no more than 5% wall-clock regression versus pre-mission baseline on a representative multi-WP mission. | Performance | Medium | Open |

### Constraints

| ID | Title | Constraint | Category | Priority | Status |
|----|-------|------------|----------|----------|--------|
| C-001 | No general topology-seam re-architecture | This mission does not re-architect the `PlacementSeam` program itself. #2275/#2996's residual gap needs no topology-seam change — its placement routing is already correct. FR-003's #2646/#2697 fix is scoped narrowly to routing the review-cycle write (and the stale-verdict read) to the same coord-authority already established for other artifact kinds — not a general re-architecture of the seam. | Technical | High | Open |
| C-002 | Verdict vocabulary and cycle numbering unchanged; verdict validator scope is explicit | The set of valid verdicts (`approved`/`rejected`/`changes_requested`) and the sequential review-cycle numbering scheme are unchanged. `validate_review_artifact` currently hardcodes a rejected-only check (`src/specify_cli/review/cycle.py:184-188`) and must be loosened as part of FR-001 — this is in-scope schema-validation work, not a vocabulary change. | Technical | High | Open |
| C-003 | No relitigating the coord/primary partition | Consistent with #3044's own non-goal: nothing in this mission is an argument to change the coordination-branch/worktree topology itself, including FR-003's fix — it routes to the existing coord authority, it does not redesign it. | Technical | Medium | Open |
| C-004 | This mission closes all of #3044's children, but not #1817/#2646/#2697 as epic members | With #990 folded into FR-002, this mission's completion closes all three of #3044's native children (#2275, #2996, #990). #1817 (already closed, duplicate-of-#1924) and #2646/#2697 (fixed by FR-003) are independent issues, not #3044 children — their resolution is bundled into this mission for efficiency, not because they are epic scope. | Process | Medium | Open |

### Key Entities

- **Review-Cycle Artifact**: the durable per-WP, per-cycle record of a review decision (cycle number, verdict, reviewer, affected files, body). The highest-numbered one is authoritative for terminal gates.
- **Work Package (WP)**: the unit under review; owns a directory of review-cycle artifacts under its mission.
- **Override Annotation**: an operator/arbiter-authored addendum recording a deliberate decision to treat a rejected-verdict artifact as the approval record, distinct from an ordinary review decision.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Every WP that moves from a rejected-latest state to `approved`/`done` has a highest-numbered review-cycle artifact whose verdict is `approved` before any merge is attempted — zero false-positive `REJECTED_REVIEW_ARTIFACT_CONFLICT` blocks on the ordinary reject→fix→approve path.
- **SC-002**: In this mission's regression suite, no test exercising the ordinary reject→fix→re-review→approve path passes by invoking `--skip-review-artifact-check` — the flag appears only in tests that explicitly construct a genuine arbiter-override scenario.
- **SC-003**: #2646 and #2697 are closed with a passing regression test each; #2275 carries its clarifying comment (posted); #1817 is closed as a duplicate (done, pre-plan).
- **SC-004**: `test_self_referential_feedback_source_is_rejected` and `test_new_cycle_body_never_duplicates_a_prior_cycle_file` (currently RED, reproducing #2996(b) and #990's identical mechanism) both turn green with no new test needed for #990 specifically.

## Assumptions

- #1817 was verified against current `main`, confirmed to be a stale, never-cross-referenced duplicate of the already-fixed-and-closed #1924, and closed directly on the tracker (comment + close) before this mission's planning began. It carries no FR and no mission scope.
- #2275 was verified, confirmed to have its read-side split already fixed in code, and commented on directly (see FR-004, status Done) — the comment is complete; FR-001 in this mission closes its residual write-side gap.
- #990 is folded into FR-002 rather than kept as a separate fast-follow: a post-spec code trace found it and #2996(b) are the identical mechanism in the identical function, with existing regression tests already reproducing both as RED.
- #2646/#2697 were reassessed after a post-spec code trace corrected the original assumption that they were "already closed by the same seam-routing fix that closed #2275's read-side split" — they are not; they are an independent, still-open coord-topology write/read authority split, now real mission scope (FR-003) per operator decision rather than the initially-assumed lightweight verification.
- FR-003's implementation may share commit-target-resolution surface with FR-001 (both touch how a review-cycle write's target branch/worktree is resolved in coord-topology missions) — flagged for explicit sequencing during `/spec-kitty.plan`, not assumed independent.
