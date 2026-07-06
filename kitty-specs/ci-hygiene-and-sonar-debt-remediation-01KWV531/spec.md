# Mission Specification: CI Hygiene & Sonar Debt Remediation

**Mission Branch**: `design/pr-landing-followups-and-sonar-remediation`
**Created**: 2026-07-06
**Status**: Draft
**Input**: User description: "Follow-up mission covering issues discovered during today's PR #2414 landing pass (LOC-census test brittleness #2416, dead-in-CI contract-conformance test #2419, masked description-length contract violation #2420) plus SonarCloud quality-gate remediation (#825 umbrella: stale backlog, missing sonar.projectVersion tracking #2421, coverage-scope mismatch between Sonar and internal diff-coverage #2422)"

## Purpose

Today's maintainer PR-landing pass on #2414 surfaced two independent classes of quality-gate debt that both erode confidence in CI signal:

- **CI-infra friction (Concern A).** The CI-topology census gate reds on any unrelated LOC change to a tracked directory (hit 3 times in one landing pass); a contract-conformance test that names itself after enforcing a "stable" external JSON contract has been silently dead in CI since introduction (a path-resolution bug that only coincidentally works from a specific maintainer worktree layout); and that dead check masked a second, real contract violation.
- **SonarCloud quality-gate debt (Concern B).** SonarCloud has never tracked a code version for this project (`sonar.projectVersion` is never set), so its new-code baseline has been frozen since 2026-03-21 instead of resetting per release — the gate measures four months of undifferentiated drift, not a release's worth of change. Separately, SonarCloud's whole-repo coverage metric and the project's own internal diff-coverage gate measure different scopes entirely, making the reported coverage numbers look alarmingly low without being a like-for-like comparison. The live backlog (~900 open issues) has never been triaged into scoped, actionable work.

This mission fixes both structural classes, then treats the live Sonar backlog as real, addressable work rather than inventory: slice it by module/effort/impact into tracked tickets (so nothing is lost), then select and actually fix the slice that intersects the project's current active roadmap surface (the Wave 2 degod trio — `workflow.py`, `implement.py`, `acceptance/__init__.py` — and any #1868/#2173 seam-binding touchpoints), rather than deferring everything to a ratchet/baseline mechanism.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - CI-topology census gate stops reding on unrelated changes (Priority: P1)

A contributor or maintainer opens a PR that adds or removes a modest amount of code in any `src/specify_cli/<dir>` tracked by the CI-topology worklist, with zero intent to touch CI routing. Today this reliably reds `test_census_worklist_matches_live_derivation` and requires a maintainer to notice, diagnose, and manually regenerate a committed LOC snapshot before the PR can merge — three times in a single landing pass on 2026-07-06.

**Why this priority**: Highest-frequency friction of the three CI-infra findings — it fires on essentially any moderately-sized diff, not an edge case. Filed as #2416.

**Independent Test**: Open a PR that adds ~20 lines to a tracked worklist directory with no other CI-relevant change. CI passes without a manual census-regeneration commit.

**Acceptance Scenarios**:

1. **Given** a PR that changes only the line count of a tracked worklist directory, **When** CI runs `test_census_worklist_matches_live_derivation` (or its replacement), **Then** the check does not fail solely because of that LOC change.
2. **Given** a PR that actually breaks CI-routing completeness (a directory becomes unmapped, a test becomes orphaned), **When** the same gate runs, **Then** it still fails — the fix must not weaken genuine routing-completeness enforcement.

---

### User Story 2 - Contract-conformance test runs for real in CI (Priority: P1)

`test_project_migration_needed_project_dry_run_json_contract` is meant to validate real `spec-kitty upgrade --dry-run --json` output against the committed `compat-planner.json` contract — described in that contract's own header as "Stable... Stable across patch releases." Its `_CONTRACT_PATH` resolution walks a hardcoded number of parent directories that only coincidentally resolves inside a specific maintainer worktree layout; in a real CI checkout it does not exist, so the schema-conformance assertion silently no-ops. This is why #2339 (a pattern bug affecting 83 of 89 real migration IDs) was never caught by CI.

**Why this priority**: A documented external contract with zero real enforcement is a silent trust gap for anything scripting against `spec-kitty upgrade --json`. Filed as #2419.

**Independent Test**: Run the test from a fresh, CI-shaped checkout (no `.worktrees/` nesting). Confirm the schema-conformance assertion actually executes (not silently skipped) and genuinely fails against a deliberately-broken contract.

**Acceptance Scenarios**:

1. **Given** a checkout laid out the way CI actually lays it out, **When** the contract-conformance test runs, **Then** `jsonschema.validate(...)` against `compat-planner.json` actually executes — no silent `None`-guarded skip.
2. **Given** the test now runs for real, **When** the contract is deliberately violated (e.g. the migration_id pattern reverted), **Then** the test fails loudly, not silently.

---

### User Story 3 - Masked contract violation is fixed (Priority: P2)

Once User Story 2 makes the contract-conformance test run for real, `m_3_2_0rc35_unified_bundle.py`'s `description` field (283 chars) exceeds the contract's `maxLength: 256` and would fail the now-live check.

**Why this priority**: Currently invisible (masked by #2419); becomes a real, immediate CI blocker the moment #2419 is fixed, so it must land in the same mission. Filed as #2420.

**Independent Test**: With #2419's fix in place, run the contract-conformance test — it passes.

**Acceptance Scenarios**:

1. **Given** the contract-conformance test now runs for real, **When** it validates `m_3_2_0rc35_unified_bundle.py`'s migration description, **Then** the description is ≤256 characters and the test passes.

---

### User Story 4 - SonarCloud tracks a real code version (Priority: P1)

SonarCloud analysis for this project never sets `sonar.projectVersion` (or any version-identifying parameter). Every analysis reports `"projectVersion": "not provided"`, and the new-code baseline (`previous_version`) has been frozen at 2026-03-21 for four months — every subsequent PR's "new code" gate measures against an ever-growing, undifferentiated window instead of the most recent release.

**Why this priority**: Root cause of why the quality gate has stayed red/uninterpretable despite remediation work landing — confirmed live via SonarCloud's own analysis-history API. Filed as #2421, parented under #825.

**Independent Test**: Trigger a SonarCloud analysis after the fix. The analysis reports a real `projectVersion` (e.g. the CLI's `pyproject.toml` version or the release tag), and the new-code baseline period reflects a release boundary, not a fixed 2026-03-21 anchor.

**Acceptance Scenarios**:

1. **Given** a CI run on `main` after this fix, **When** the `sonarcloud` job submits its analysis, **Then** the analysis is tagged with a real, non-placeholder version identifier.
2. **Given** a subsequent release, **When** the next analysis runs, **Then** the new-code baseline advances rather than staying pinned to 2026-03-21.

---

### User Story 5 - Sonar and internal coverage numbers are reconcilable (Priority: P2)

SonarCloud's project-wide `coverage`/`new_coverage` metrics and the project's own internal `diff-coverage` PR gate (90% threshold, critical-path-only, per-PR-diff scoped) measure fundamentally different things, making Sonar's reported coverage look alarmingly low by comparison without being a fair comparison.

**Why this priority**: Currently causes confusion/false alarm about coverage regressions that aren't real regressions — a reporting-clarity problem, not (as far as this mission can verify without file-level Sonar API access) a missing-instrumentation bug. Filed as #2422, parented under #825.

**Independent Test**: A documented explanation (in the Sonar dashboard project description, a repo doc, or both) states what each coverage number actually measures and why they differ, OR the scopes are aligned so the numbers are directly comparable — whichever this mission's investigation determines is correct.

**Acceptance Scenarios**:

1. **Given** someone compares SonarCloud's coverage number to the internal diff-coverage gate's result on the same PR, **When** they read the documented explanation, **Then** they can correctly interpret whether an apparent discrepancy is a real regression or an expected scope difference.

---

### User Story 6 - Sonar backlog is sliced into tracked work, and the roadmap-aligned slice is fixed (Priority: P1)

The live SonarCloud backlog (~900 open issues, confirmed via live API query) has never been triaged into scoped, ownable work. Per operator direction: this mission slices the backlog by module, effort, and impact into tracked GitHub issues (milestone `3.2.x`, labels `tech-debt` + new `quality` + new `devex`), then selects and actually fixes the slice(s) that intersect the project's current active roadmap surface — explicitly rejecting a ratchet/baseline-suppression mechanism as the primary strategy, since that trades real fixes for recurring inventory overhead.

**Why this priority**: The core deliverable of the Sonar-remediation half of this mission — without it, #2421/#2422 only fix how the gate measures, not what it measures.

**Independent Test**: Query the tracker after this mission: every SonarCloud backlog item is covered by exactly one filed, correctly labeled/milestoned issue (no orphaned/unticketed backlog items), and the roadmap-aligned slice's issue count is measurably lower than at mission start.

**Acceptance Scenarios**:

1. **Given** the live SonarCloud backlog at mission start, **When** slicing is complete, **Then** every issue is covered by a filed GitHub issue grouped by module/effort/impact, milestoned `3.2.x`, labeled `tech-debt` + `quality` + `devex`.
2. **Given** the sliced backlog, **When** the roadmap-aligned slice (Wave 2 degod trio files + #1868/#2173 seam-binding touchpoints) is identified, **Then** those specific issues are fixed within this mission, not merely ticketed.
3. **Given** the non-selected slices, **When** the mission concludes, **Then** they remain open, real, unsuppressed tracked issues — no ratchet baseline, allowlist, or suppression file is introduced to make them invisible to the gate.

### Edge Cases

- What happens when a future PR touches a tracked worklist directory AND the census-gate fix itself? The fix must not just move the brittleness elsewhere (e.g., a tolerance band with a threshold that's itself another brittle constant needing periodic re-pins).
- How does the contract-conformance test behave in a checkout layout neither its old path resolution NOR a naive fix anticipates (e.g., a shallow CI clone with an unusual working-directory depth)? The fix must be genuinely checkout-shape-agnostic, not just fixed for the currently-known CI layout.
- What happens if a Sonar backlog item spans multiple modules, or its "effort" is genuinely unknown until investigated? The slicing scheme must have an explicit answer (e.g., a "needs-triage" bucket) rather than forcing a premature categorization.
- What happens if the roadmap-aligned slice (Wave 2 degod trio) turns out to have zero or very few live Sonar issues once actually queried? The mission's success does not depend on that slice being large — User Story 6's acceptance scenario 2 is satisfied by fixing whatever is genuinely found there, even if small.

## Requirements *(mandatory)*

### Functional Requirements

| ID | Title | User Story | Priority | Status |
|----|-------|------------|----------|--------|
| FR-001 | Census gate does not fail on unrelated LOC changes | As a contributor, I want an unrelated small diff to not trip the CI-topology census gate, so that I am not blocked by CI-infra bookkeeping unrelated to my change. | High | Open |
| FR-002 | Census gate still catches genuine routing regressions | As a maintainer, I want the census gate to still fail when CI-routing completeness genuinely regresses, so that the fix for FR-001 doesn't silently weaken coverage enforcement. | High | Open |
| FR-003 | Contract-conformance test resolves its contract path in any real checkout layout | As a maintainer, I want `test_project_migration_needed_project_dry_run_json_contract` to find `compat-planner.json` correctly from a CI-shaped checkout, so that the contract is actually enforced, not silently skipped. | High | Open |
| FR-004 | Contract-conformance test fails loudly, never silently, on a missing/unreadable contract file | As a maintainer, I want a broken path resolution to be a visible test failure, not a silent no-op, so that a future regression of this kind is caught immediately. | Medium | Open |
| FR-005 | `m_3_2_0rc35_unified_bundle.py` description fits the contract's maxLength | As a maintainer, I want every migration's description to satisfy the compat-planner.json contract, so that the now-live conformance check passes. | Medium | Open |
| FR-006 | SonarCloud analysis reports a real project version | As a maintainer, I want each SonarCloud analysis to carry a real version identifier, so that the new-code baseline resets per release instead of freezing indefinitely. | High | Open |
| FR-007 | Sonar vs. internal coverage scope is reconciled or documented | As anyone reviewing a PR's coverage signal, I want to know whether SonarCloud's coverage number and the internal diff-coverage gate are comparable, so that I don't mistake an expected scope difference for a regression. | Medium | Open |
| FR-008 | Live Sonar backlog is sliced into tracked tickets by module/effort/impact | As a maintainer, I want the ~900-issue Sonar backlog turned into scoped, ownable GitHub issues, so that debt is trackable work instead of an opaque count. | High | Open |
| FR-009 | Tracker labels `quality` and `devex` exist and are applied consistently | As a maintainer, I want the new backlog-slice tickets labeled consistently, so that they're filterable/reportable alongside `tech-debt`. | Low | Open |
| FR-010 | Roadmap-aligned Sonar slice is identified and fixed | As a maintainer, I want the Sonar issues living in the current roadmap's active surface (Wave 2 degod trio, #1868/#2173 touchpoints) fixed in this mission, so that the highest-leverage debt doesn't wait for a future mission. | High | Open |
| FR-011 | Non-selected backlog slices remain real, unsuppressed, tracked issues | As a maintainer, I want the un-remediated backlog to stay visible and real (no ratchet/allowlist/suppression mechanism), so that future missions inherit honest debt, not hidden debt. | High | Open |

### Non-Functional Requirements

| ID | Title | Requirement | Category | Priority | Status |
|----|-------|-------------|----------|----------|--------|
| NFR-001 | Census-gate fix preserves routing-completeness coverage | The fixed gate must continue to detect every routing-completeness regression the current `tests/architectural/test_ci_topology_worklist.py` suite detects today — zero dropped invariants, verified by running the existing suite's own test cases against the new implementation. | Reliability | High | Open |
| NFR-002 | Contract-conformance fix verified in real CI, not just locally | The fix for FR-003/FR-004 must be demonstrated passing on an actual GitHub Actions CI run (not only a local repro), since the original defect was specifically "works locally, silently no-ops in CI." | Reliability | High | Open |
| NFR-003 | Sonar quality-gate results are independently interpretable post-mission | After FR-006/FR-007 land, a maintainer with no prior context can read the SonarCloud dashboard and the internal coverage report and correctly state whether the project's quality gate is passing, and why, within 5 minutes. | Usability | Medium | Open |
| NFR-004 | Backlog slicing has 100% coverage of the live backlog | Every issue present in the live SonarCloud backlog at the time of slicing (FR-008) is covered by exactly one filed tracked issue — zero unticketed items, verified by comparing the live API issue count against the sum of ticketed-issue counts across all filed slices. | Completeness | High | Open |

### Constraints

| ID | Title | Constraint | Category | Priority | Status |
|----|-------|------------|----------|----------|--------|
| C-001 | No Wave 2 degod trio body-thinning refactor in this mission | This mission fixes Sonar issues found within `workflow.py`/`implement.py`/`acceptance/__init__.py`; it does not perform the pure-core/port extraction refactor itself — that is a separate future mission per the 3.2.x roadmap. | Technical | High | Open |
| C-002 | No ratchet-baseline or suppression mechanism for un-remediated backlog | Per explicit operator direction, this mission must not introduce a shrink-only ratchet baseline, ignore-list, or suppression file to make the Sonar gate pass for backlog items outside the selected roadmap-aligned slice. | Business | High | Open |
| C-003 | Backlog-slice tickets must cite live data, not estimates | Every filed backlog-slice issue must reference real SonarCloud data at filing time (rule, file/module, live issue count) — not a placeholder or extrapolated estimate. | Technical | Medium | Open |
| C-004 | New tracker labels reuse existing vocabulary conventions | The new `quality` and `devex` labels must be created following this repo's existing label naming/coloring conventions (verified against `gh label list` before creation), not invented ad hoc. | Technical | Low | Open |

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A PR that adds/removes code in a tracked CI-topology worklist directory, with no CI-routing-relevant change, passes CI without requiring a manual census-regeneration commit.
- **SC-002**: `test_project_migration_needed_project_dry_run_json_contract`'s schema-conformance assertion is confirmed executing (not silently skipped) on an actual CI run, and fails when the contract is deliberately violated.
- **SC-003**: The full `tests/architectural/` suite passes with the FR-001–FR-005 fixes in place, with zero net reduction in the number of distinct invariants enforced.
- **SC-004**: The next SonarCloud analysis after this mission reports a non-placeholder `projectVersion` and a new-code baseline that is not frozen at 2026-03-21.
- **SC-005**: 100% of the live SonarCloud backlog (issue-for-issue, verified by count) is covered by a filed, milestoned, labeled tracker issue.
- **SC-006**: The roadmap-aligned slice (Wave 2 degod trio + #1868/#2173 touchpoints) shows its SonarCloud issue count reduced to zero for the issues identified and selected at mission start, with zero regression injected (verified by re-running the affected file's test suite and the full `tests/architectural/` suite).
- **SC-007**: Zero ratchet-baseline, allowlist, or suppression-file entries are introduced anywhere in the codebase as part of this mission's Sonar-remediation work.
