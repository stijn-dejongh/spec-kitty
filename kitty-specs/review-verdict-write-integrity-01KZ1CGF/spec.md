# Mission Specification: Review Verdict Write Integrity

**Mission Branch**: `research/3044-review-artifact-topology-seam`
**Created**: 2026-08-02
**Status**: Draft
**Input**: GitHub issue #3044 ("Epic: review-artifact integrity — approval must write a real verdict, and no cycle may fabricate one"), scoped by the pre-spec research at `docs/plans/investigations/review-artifact-write-integrity-3044.md`. Corroborated scope: add a missing approved-verdict writer (closes #2275's residual gap + #2996(a)); harden the rejected-verdict writer's feedback-source provenance validation (closes #2996(b)); verify #1817, #2646, and #2697 against fixes/seams already proven to close this defect shape.

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

### User Story 2 - A rejection cycle cannot be filed as someone else's fabricated review (Priority: P1)

Creating a rejection artifact accepts any file as the "feedback source" without checking what it actually is. If that source is itself a prior cycle's own review artifact for the same WP — whether by tooling error or manual mistake — the new cycle is filed as a byte-identical duplicate of the old one, with fresh (often synthetic `reviewer_agent: unknown`) frontmatter. The artifact reads as though a second, independent review happened when none did.

**Why this priority**: This is #2996(b) — the fabrication half of the P0 epic. It corrupts the audit trail the same way the missing-writer gap does, by a different mechanism, and is independently reproducible.

**Independent Test**: Attempt to create a rejection review-cycle artifact whose `feedback_source` is a prior `review-cycle-N.md` for the same WP. Confirm the operation is refused (or the duplication is otherwise detected and rejected) rather than silently writing a duplicate artifact under synthetic frontmatter.

**Acceptance Scenarios**:

1. **Given** WP02 already has `review-cycle-1.md`, **When** a rejection is filed with `--review-feedback-file` pointing at that same `review-cycle-1.md`, **Then** the operation fails with a clear error instead of writing a `review-cycle-2.md` that duplicates cycle 1's body under synthetic frontmatter.
2. **Given** a genuine, distinct feedback file, **When** a rejection is filed normally, **Then** the artifact is created exactly as before — the new validation does not reject legitimate rejections.

---

### User Story 3 - Adjacent, already-fixed-looking issues are verified and closed, not left stale (Priority: P2)

Three open GitHub issues (#1817, #2646, #2697) describe defects that code-level evidence suggests are already fixed by prior, unrelated work — but none has been checked against the current codebase or closed with evidence. Leaving them open risks future contributors re-investigating or re-fixing already-resolved ground.

**Why this priority**: Tracker hygiene that prevents wasted future effort, explicitly requested alongside the code fixes above; it does not block User Stories 1–2 and can be verified independently.

**Independent Test**: For each of #1817, #2646, #2697: reproduce the issue's exact reported scenario against the current codebase. If the existing fix covers it, close the issue with a comment citing the covering fix/test. If a residual gap is found, fix it and add a regression test before closing.

**Acceptance Scenarios**:

1. **Given** #1817's exact reproduction steps (rejected-then-`--skip-review-artifact-check`-approved WP, then `spec-kitty merge --dry-run`), **When** run against current `main`, **Then** either the merge gate correctly honors the override (issue closed with evidence citing `tests/regression/test_2684_review_override_recognition.py` or equivalent) or a residual gap is found and fixed.
2. **Given** #2646 and #2697's reported scenarios, **When** re-run against current `main`, **Then** each is closed with evidence or its residual gap is fixed within this mission.
3. **Given** #2275's own issue text still describes its now-fixed read-side split, **When** this mission's work lands, **Then** a comment is posted on #2275 clarifying that the read-side split is already resolved (citing `review/cycle.py`'s `_review_cycle_wp_dir`) and that the residual, now-closed gap was the missing approved-verdict writer.

### Edge Cases

- What happens when a WP has gone through many rejection cycles (cycle N is large) before finally being approved? The approved artifact must still land at the correct next sequential cycle number, not collide with or skip any prior cycle.
- How does the system handle a genuine arbiter/operator override (`--skip-review-artifact-check`) after User Story 1 ships, for a case where an actual code concern is being knowingly waived rather than worked around? The override mechanism itself is out of this mission's rebuild scope (already fixed per #1924) — it must continue to work unchanged for genuine override use, now simply no longer *needed* for the ordinary reject→fix→approve path.
- What happens if #1817/#2646/#2697 verification (User Story 3) finds a real residual gap rather than a stale duplicate? That WP's scope grows to include the fix and a regression test; it is not closed on the strength of "probably already fixed."
- What happens to #990 (review-cycle content wrapping/contamination)? It is explicitly out of this mission's committed scope — see Constraints — pending a dedicated post-spec research squad to trace its mechanism.

## Domain Language

- **Review-cycle artifact**: the durable, per-WP, per-cycle record of a review decision (`review-cycle-N.md`: cycle number, verdict, reviewer, affected files, body). The highest-numbered artifact for a WP is the one every terminal gate treats as authoritative.
- **Verdict**: the recorded outcome of a review cycle — `approved`, `rejected`, or `changes_requested`. Avoid "status" as a synonym; status/lane refers to the WP's separate lifecycle-lane state.
- **Override annotation**: an operator/arbiter-authored addendum (`review_artifact_override_*` frontmatter) recording a deliberate decision to treat a rejected-verdict artifact as the approval record. Distinct from an ordinary review decision — reserved for genuine arbitration, not a workaround for a missing writer.
- **Terminal gate**: a transition or merge-time check (`move-task --to approved/--to done`, `spec-kitty merge`'s `REJECTED_REVIEW_ARTIFACT_CONFLICT` invariant) that reads the highest-numbered review-cycle artifact as ground truth.

## Requirements *(mandatory)*

### Functional Requirements

| ID | Title | User Story | Priority | Status |
|----|-------|------------|----------|--------|
| FR-001 | Persist a real approved-verdict artifact on approval | As a reviewer/operator, I want approving a previously-rejected WP to durably persist a new highest-numbered review-cycle artifact with `verdict: approved` and a real `reviewer_agent`, so that terminal gates see an honest recorded decision instead of a stale rejection. | High | Open |
| FR-002 | Refuse rejection artifacts fabricated from prior-cycle content | As a reviewer, I want the system to refuse creating a rejection artifact whose feedback source is itself a prior cycle's own artifact for the same WP, so that a cycle number never implies an independent review that didn't happen. | High | Open |
| FR-003 | Verify and close #1817 against the existing override fix | As a maintainer, I want #1817 reproduced against current `main`, closed with evidence if already covered, or fixed if a residual gap surfaces, so a duplicate report doesn't stay open indefinitely. | Medium | Open |
| FR-004 | Verify #2646 and #2697 for the same residual gap #2275 had | As a maintainer, I want #2646 and #2697 checked for the missing-approved-writer gap #2275 had, with any residual gap fixed and each issue closed or documented with evidence. | Medium | Open |
| FR-005 | Annotate #2275 with its corrected residual scope | As a maintainer, I want #2275 commented on to record that its read-side split is already fixed in code and that this mission closes its remaining write-side gap, so future readers aren't misled by the issue's original wording. | Low | Open |

### Non-Functional Requirements

| ID | Title | Requirement | Category | Priority | Status |
|----|-------|-------------|----------|----------|--------|
| NFR-001 | No regression to existing review/merge-gate behavior | 100% of pre-existing tests under `tests/review/` and `tests/post_merge/` pass unchanged after this mission's changes. | Reliability | High | Open |
| NFR-002 | Red-then-green coverage for every new behavior | Each of FR-001 through FR-004 has at least one regression test that fails without its fix and passes with it. | Reliability | High | Open |
| NFR-003 | No meaningful performance regression on the approval/merge path | `move-task --to approved` and `spec-kitty merge --dry-run` show no more than 5% wall-clock regression versus pre-mission baseline on a representative multi-WP mission. | Performance | Medium | Open |

### Constraints

| ID | Title | Constraint | Category | Priority | Status |
|----|-------|------------|----------|----------|--------|
| C-001 | No topology-seam program extension | This mission must not extend or modify the `PlacementSeam`/read-side topology-seam program — review-cycle artifact placement routing is already correct (verified in `docs/plans/investigations/review-artifact-write-integrity-3044.md`) and is out of scope to re-architect. | Technical | High | Open |
| C-002 | No change to verdict vocabulary or cycle numbering | The set of valid verdicts and the sequential review-cycle numbering scheme are unchanged; this mission adds a writer for an already-valid verdict, not a new one. | Technical | High | Open |
| C-003 | #990 excluded from committed scope | Issue #990 (review-cycle content wrapping/contamination) is explicitly out of this mission's committed scope. A dedicated post-spec research squad traces its mechanism first; the operator decides afterward whether it folds into this mission's tasks or ships as a separate fast-follow. | Process | High | Open |
| C-004 | No relitigating the coord/primary partition | Consistent with #3044's own non-goal: nothing in this mission is an argument to change the coordination-branch/worktree topology itself. | Technical | Medium | Open |

### Key Entities

- **Review-Cycle Artifact**: the durable per-WP, per-cycle record of a review decision (cycle number, verdict, reviewer, affected files, body). The highest-numbered one is authoritative for terminal gates.
- **Work Package (WP)**: the unit under review; owns a directory of review-cycle artifacts under its mission.
- **Override Annotation**: an operator/arbiter-authored addendum recording a deliberate decision to treat a rejected-verdict artifact as the approval record, distinct from an ordinary review decision.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Every WP that moves from a rejected-latest state to `approved`/`done` has a highest-numbered review-cycle artifact whose verdict is `approved` before any merge is attempted — zero false-positive `REJECTED_REVIEW_ARTIFACT_CONFLICT` blocks on the ordinary reject→fix→approve path.
- **SC-002**: Zero missions need `--skip-review-artifact-check` for an ordinary (non-arbiter-override) reject→fix→re-review→approve cycle after this mission ships.
- **SC-003**: #1817 is closed with recorded evidence; #2646 and #2697 are each closed or documented with evidence of no residual gap; #2275 carries a clarifying comment.
- **SC-004**: A fabricated/duplicate review-cycle artifact (byte-identical body to a prior cycle under synthetic frontmatter) cannot be produced via the normal rejection path — demonstrated by a regression test reproducing #2996(b)'s exact mechanism turning from red to green.

## Assumptions

- #990 is deliberately excluded from this spec's committed scope (C-003); a post-spec research squad will trace its mechanism, and the operator will decide whether it folds into this mission or ships separately.
- The override-annotation mechanism itself (honored by the merge gate per the already-closed #1924) is not being rebuilt; FR-003's verification may find #1817 already resolved, in which case its "fix" is closing the issue with evidence, not new code.
- #2646 and #2697 are assumed, pending FR-004's verification, to be genuinely closed by the same seam-routing fix that closed #2275's read-side split — this assumption is exactly what FR-004 tests.
