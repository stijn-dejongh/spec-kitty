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

### User Story 2 - Contract-conformance tests run for real in CI (Priority: P1)

`test_project_migration_needed_project_dry_run_json_contract` (`tests/specify_cli/cli/commands/test_upgrade_command.py`) is meant to validate real `spec-kitty upgrade --dry-run --json` output against the committed `compat-planner.json` contract — described in that contract's own header as "Stable... Stable across patch releases." Its `_CONTRACT_PATH` resolution walks a hardcoded number of parent directories that only coincidentally resolves inside a specific maintainer worktree layout; in a real CI checkout it does not exist, so the schema-conformance assertion silently no-ops. This is why #2339 (a pattern bug affecting 83 of 89 real migration IDs) was never caught by CI. 13 call sites in this file depend on the broken helper.

**Post-spec squad finding (architect-alphonso, independently confirmed by direct execution during squad review):** the identical defect class exists a second time, independently, in `tests/specify_cli/compat/test_messages.py` — its own `_CONTRACT_PATH` (a *different* hardcoded parent-walk, off by one directory level) resolves to a path that does not exist in **any** checkout, worktree or CI (`.exists()` is `False` unconditionally — confirmed by direct execution, not just static reading). 6 call sites there (`TestRenderJson._get_contract`/`_validate_against_schema`) silently no-op the same way. This file was not in #2419's original report and is not covered by the issue as filed — this spec widens scope to cover it, since leaving it unfixed would mean this mission claims to close the "dead contract-conformance check" defect class while a second, unaddressed instance remains.

**Why this priority**: A documented external contract with zero real enforcement, across two independent test files (19 total silently-dead call sites), is a silent trust gap for anything scripting against `spec-kitty upgrade --json`. Primary instance filed as #2419; the `test_messages.py` instance is newly discovered by this spec's validation squad and is in scope here (file a companion tracker issue for it before/at plan time).

**Independent Test**: Run both files' contract-conformance tests from a fresh, CI-shaped checkout (no `.worktrees/` nesting). Confirm each schema-conformance assertion actually executes (not silently skipped) and genuinely fails against a deliberately-broken contract.

**Acceptance Scenarios**:

1. **Given** a checkout laid out the way CI actually lays it out, **When** either file's contract-conformance test runs, **Then** `jsonschema.validate(...)` (or the equivalent schema check) against `compat-planner.json` actually executes — no silent `None`-guarded skip, in either file.
2. **Given** the tests now run for real, **When** the contract is deliberately violated (e.g. the migration_id pattern reverted), **Then** both files' tests fail loudly, not silently.
3. **Given** the two files currently use two different (both broken) path-resolution approaches, **When** this mission fixes them, **Then** both resolve the contract path the same way — a single canonical resolution helper, not two independently-maintained hacks — so this defect class cannot recur a third time.

---

### User Story 3 - Masked contract violation is fixed (Priority: P3)

Once User Story 2 makes the contract-conformance tests run for real, `m_3_2_0rc35_unified_bundle.py`'s `description` field (283 chars) exceeds the contract's `maxLength: 256` and would fail the now-live check(s).

**Why this priority**: Currently invisible (masked by #2419); becomes a real, immediate CI blocker the moment #2419 is fixed, so it must land in the same mission. Filed as #2420 (`priority:P3`, matching this story's priority — corrected from an earlier draft mismatch).

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

The live SonarCloud backlog (~900 open issues — independently re-confirmed at 903 via a live, unauthenticated SonarCloud API query during this spec's validation squad) has never been triaged into scoped, ownable work. Per operator direction: this mission slices the backlog by module, effort, and impact into tracked GitHub issues (milestone `3.2.x`, labels `tech-debt` + new `quality` + new `devex`), then selects and actually fixes the slice(s) that intersect the project's current active roadmap surface — explicitly rejecting a ratchet/baseline-suppression mechanism as the primary strategy, since that trades real fixes for recurring inventory overhead.

**Post-spec squad finding (planner-priti, independently confirmed):** epic **#1928** ("EPIC: Reduce ruff / mypy --strict / SonarCloud debt as a 3.2.x goal") already owns this exact mandate — milestoned `3.2.x`, with #825 already a confirmed sub-issue, and a named DRI. This spec's FR-008 backlog-slice tickets must be filed as children of #1928, not left unparented, to avoid creating a second, disconnected decomposition of work #1928 already charters. Note the reconciliation: #1928's own stated general approach favors an "explicit-baseline-shrink discipline" (matching the charter's binding Burn-down Policy pattern used elsewhere in this repo, e.g. Cat-7 shim shrink-to-0-by-4.0) — this is **not** a contradiction with C-002's no-ratchet constraint below; #1928 is a broad epic that may reasonably use different remediation strategies per sub-scope, and the operator has explicitly directed that *this mission's* live-backlog sub-scope use real fixes rather than a ratchet. Separately, #2416 and #2419 (User Stories 1-2) are already tracked as members of epic **#1931** ("EPIC: Test quality & suite hygiene") — closing them should be reflected there.

**Post-spec squad finding (paula-patterns, independently confirmed):** `work/snippets/sonarcloud_branch_review.sh` already implements the SonarCloud REST API interactions this story needs repeatedly (quality-gate status, coverage metrics, per-file uncovered lines, open-issues-by-severity/rule/file) — it is currently gitignored/untracked. Promote it into a tracked location (e.g. `scripts/ci/`) with a smoke test as part of this story's work, so the backlog-slicing sweep, the roadmap-slice fix verification, and SC-006's re-check all route through one canonical, testable script instead of each reinventing the API calls.

**Why this priority**: The core deliverable of the Sonar-remediation half of this mission — without it, #2421/#2422 only fix how the gate measures, not what it measures.

**Independent Test**: Query the tracker after this mission: every SonarCloud backlog item is covered by exactly one filed, correctly labeled/milestoned issue (no orphaned/unticketed backlog items), and the roadmap-aligned slice's issue count is measurably lower than at mission start.

**Acceptance Scenarios**:

1. **Given** the live SonarCloud backlog at mission start, **When** slicing is complete, **Then** every issue is covered by a filed GitHub issue grouped by module/effort/impact, milestoned `3.2.x`, labeled `tech-debt` + `quality` + `devex`.
2. **Given** the sliced backlog, **When** the roadmap-aligned slice (Wave 2 degod trio files + #1868/#2173 seam-binding touchpoints) is identified, **Then** those specific issues are fixed within this mission, not merely ticketed.
3. **Given** the non-selected slices, **When** the mission concludes, **Then** they remain open, real, unsuppressed tracked issues — no ratchet baseline, allowlist, or suppression file is introduced to make them invisible to the gate.

### Edge Cases

- What happens when a future PR touches a tracked worklist directory AND the census-gate fix itself? The fix must not just move the brittleness elsewhere (e.g., a tolerance band with a threshold that's itself another brittle constant needing periodic re-pins). **Post-spec squad finding (paula-patterns, independently confirmed):** this repo already has a proven, in-family answer — `tests/architectural/test_gate_coverage.py`/`_gate_coverage_baseline.json` and the broader `test_ratchet_baselines.py`/`_baselines.yaml` convention (used by 7 other gated modules) implement exactly "growth fails, shrinkage warns" instead of exact equality. FR-001's fix should reuse this established pattern — pin structural/routing facts and treat raw LOC as a floor check (as `test_every_worklist_dir_meets_loc_floor` already does), not invent a new tolerance mechanism.
- How do the contract-conformance tests (both files, per the widened User Story 2) behave in a checkout layout neither their old path resolutions NOR a naive fix anticipates (e.g., a shallow CI clone with an unusual working-directory depth)? The fix must be genuinely checkout-shape-agnostic, not just fixed for the currently-known CI layout — and both files must resolve the contract path through the same canonical helper (see User Story 2, Acceptance Scenario 3) so this can't recur a third time.
- What happens if a Sonar backlog item spans multiple modules, or its "effort" is genuinely unknown until investigated? The slicing scheme must have an explicit answer (e.g., a "needs-triage" bucket) rather than forcing a premature categorization.
- What happens if the roadmap-aligned slice (Wave 2 degod trio) turns out to have zero or very few live Sonar issues once actually queried? The mission's success does not depend on that slice being large — User Story 6's acceptance scenario 2 is satisfied by fixing whatever is genuinely found there, even if small.
- **What happens if a roadmap-aligned Sonar issue (FR-010) can only be correctly fixed via the pure-core/port extraction refactor that C-001 explicitly excludes from this mission?** (Post-spec squad finding, architect-alphonso — real tension identified between C-001 and FR-010/SC-006 as originally drafted.) Resolution: any such issue is out of scope for FR-010/SC-006 in this mission. It gets ticketed under FR-008/FR-011 instead (i.e., folded into the general backlog-slice tracking, explicitly noting the extraction dependency in the ticket), and does **not** count against SC-006's "reduced to zero" claim for the selected slice. An implementer must not violate C-001 to force SC-006, nor silently narrow "the slice" without recording which issues were excluded and why.

## Requirements *(mandatory)*

### Functional Requirements

| ID | Title | User Story | Priority | Status |
|----|-------|------------|----------|--------|
| FR-001 | Census gate does not fail on unrelated LOC changes | As a contributor, I want an unrelated small diff to not trip the CI-topology census gate, so that I am not blocked by CI-infra bookkeeping unrelated to my change. Fix reuses the existing growth-only-ratchet pattern already proven in the same module family (`_gate_coverage_baseline.json`/`_baselines.yaml`), not a novel tolerance mechanism. | High | Open |
| FR-002 | Census gate still catches genuine routing regressions | As a maintainer, I want the census gate to still fail when CI-routing completeness genuinely regresses, so that the fix for FR-001 doesn't silently weaken coverage enforcement. | High | Open |
| FR-003 | Both contract-conformance tests resolve their contract path in any real checkout layout | As a maintainer, I want `test_project_migration_needed_project_dry_run_json_contract` (`test_upgrade_command.py`) **and** the equivalent checks in `test_messages.py` (`TestRenderJson`) to find `compat-planner.json` correctly, through one shared canonical path-resolution helper, from any CI-shaped checkout, so that the contract is actually enforced everywhere it's supposed to be, not silently skipped in either file. | High | Open |
| FR-004 | Contract-conformance tests fail loudly, never silently, on a missing/unreadable contract file | As a maintainer, I want a broken path resolution to be a visible test failure in both files, not a silent no-op, so that a future regression of this kind is caught immediately regardless of which file it recurs in. | Medium | Open |
| FR-005 | `m_3_2_0rc35_unified_bundle.py` description fits the contract's maxLength | As a maintainer, I want every migration's description to satisfy the compat-planner.json contract, so that the now-live conformance checks pass in both files. | Medium | Open |
| FR-006 | SonarCloud analysis reports a real project version | As a maintainer, I want each SonarCloud analysis to carry a real version identifier, so that the new-code baseline resets per release instead of freezing indefinitely. | High | Open |
| FR-007 | Sonar vs. internal coverage scope is reconciled or documented | As anyone reviewing a PR's coverage signal, I want to know whether SonarCloud's coverage number and the internal diff-coverage gate are comparable, so that I don't mistake an expected scope difference for a regression. | Medium | Open |
| FR-008 | Live Sonar backlog is sliced into tracked tickets by module/effort/impact, parented under the correct existing epic | As a maintainer, I want the ~900-issue Sonar backlog turned into scoped, ownable GitHub issues filed as children of epic #1928 (which already charters this exact mandate), so that debt is trackable work instead of an opaque count, and doesn't create a second disconnected decomposition. | High | Open |
| FR-009 | Tracker labels `quality` and `devex` exist and are applied consistently | As a maintainer, I want the new backlog-slice tickets labeled consistently, so that they're filterable/reportable alongside `tech-debt`. | Low | Open |
| FR-010 | Roadmap-aligned Sonar slice is identified and fixed, except where only fixable via the C-001-forbidden refactor | As a maintainer, I want the Sonar issues living in the current roadmap's active surface (Wave 2 degod trio, #1868/#2173 touchpoints) fixed in this mission, so that the highest-leverage debt doesn't wait for a future mission — any issue whose only correct fix requires the C-001-forbidden extraction is excluded here and ticketed under FR-008/FR-011 instead. | High | Open |
| FR-011 | Non-selected backlog slices remain real, unsuppressed, tracked issues | As a maintainer, I want the un-remediated backlog to stay visible and real (no ratchet/allowlist/suppression mechanism), so that future missions inherit honest debt, not hidden debt. | High | Open |
| FR-012 | `sonarcloud_branch_review.sh` is promoted into a tracked, tested script | As a maintainer, I want the existing (currently gitignored) SonarCloud REST-API script promoted into a tracked location with a smoke test, so that FR-008's slicing sweep and FR-010's fix-verification route through one canonical tool instead of ad hoc API calls. | Medium | Open |

### Non-Functional Requirements

| ID | Title | Requirement | Category | Priority | Status |
|----|-------|-------------|----------|----------|--------|
| NFR-001 | Census-gate fix preserves routing-completeness coverage | The fixed gate must continue to detect every routing-completeness regression the current `tests/architectural/test_ci_topology_worklist.py` suite detects today — zero dropped invariants, verified by running the existing suite's own test cases against the new implementation. | Reliability | High | Open |
| NFR-002 | Contract-conformance fix verified in real CI, not just locally | The fix for FR-003/FR-004, in both `test_upgrade_command.py` and `test_messages.py`, must be demonstrated passing on an actual GitHub Actions CI run (not only a local repro) — the `test_messages.py` instance is broken in every checkout including local, so its fix additionally needs a local-repro-then-CI-confirm pair, not just a CI-only check. | Reliability | High | Open |
| NFR-003 | Sonar quality-gate results are independently interpretable post-mission | After FR-006/FR-007 land, a maintainer with no prior context can read the SonarCloud dashboard and the internal coverage report and correctly state whether the project's quality gate is passing, and why, within 5 minutes. | Usability | Medium | Open |
| NFR-004 | Backlog slicing has 100% coverage of the live backlog | Every issue present in the live SonarCloud backlog at the time of slicing (FR-008) is covered by exactly one filed tracked issue — zero unticketed items, verified by comparing the live API issue count against the sum of ticketed-issue counts across all filed slices. | Completeness | High | Open |

### Constraints

| ID | Title | Constraint | Category | Priority | Status |
|----|-------|------------|----------|----------|--------|
| C-001 | No Wave 2 degod trio body-thinning refactor in this mission | This mission fixes Sonar issues found within `workflow.py`/`implement.py`/`acceptance/__init__.py`; it does not perform the pure-core/port extraction refactor itself — that is a separate future mission per the 3.2.x roadmap. Any specific Sonar issue whose only correct fix requires that extraction is excluded from FR-010 and ticketed under FR-008/FR-011 instead (see Edge Cases). | Technical | High | Open |
| C-002 | No ratchet-baseline or suppression mechanism for un-remediated backlog | Per explicit operator direction, this mission must not introduce a shrink-only ratchet baseline, ignore-list, or suppression file to make the Sonar gate pass for backlog items outside the selected roadmap-aligned slice. | Business | High | Open |
| C-003 | Backlog-slice tickets must cite live data, not estimates | Every filed backlog-slice issue must reference real SonarCloud data at filing time (rule, file/module, live issue count) — not a placeholder or extrapolated estimate. | Technical | Medium | Open |
| C-004 | New tracker labels reuse existing vocabulary conventions | The new `quality` and `devex` labels must be created following this repo's existing label naming/coloring conventions (verified against `gh label list` before creation), not invented ad hoc. | Technical | Low | Open |

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A PR that adds/removes code in a tracked CI-topology worklist directory, with no CI-routing-relevant change, passes CI without requiring a manual census-regeneration commit.
- **SC-002**: Both `test_project_migration_needed_project_dry_run_json_contract` (`test_upgrade_command.py`) and the equivalent `TestRenderJson` schema-conformance checks (`test_messages.py`) are confirmed executing (not silently skipped) — the latter on a local run at minimum, since it was never conditional on CI layout — and both fail when the contract is deliberately violated.
- **SC-003**: The full `tests/architectural/` suite passes with the FR-001–FR-005 fixes in place, with zero net reduction in the number of distinct invariants enforced.
- **SC-004**: The next SonarCloud analysis after this mission (the `sonarcloud` job runs nightly on schedule, not on push/PR — no manual `workflow_dispatch` trigger is required for this to be observed within ~24h) reports a non-placeholder `projectVersion` and a new-code baseline that is not frozen at 2026-03-21.
- **SC-005**: 100% of the live SonarCloud backlog (issue-for-issue, verified by count) is covered by a filed, milestoned, labeled tracker issue, correctly parented as children of epic #1928.
- **SC-006**: The roadmap-aligned slice (Wave 2 degod trio + #1868/#2173 touchpoints), excluding any issue explicitly recorded as C-001-blocked per the Edge Cases resolution, shows its SonarCloud issue count reduced to zero for the issues identified and selected at mission start, with zero regression injected (verified by re-running the affected file's test suite and the full `tests/architectural/` suite).
- **SC-007**: Zero ratchet-baseline, allowlist, or suppression-file entries are introduced anywhere in the codebase as part of this mission's Sonar-remediation work.
- **SC-008**: `work/snippets/sonarcloud_branch_review.sh` is promoted into a tracked location with a passing smoke test, and is the sole SonarCloud-API-calling code path this mission's WPs use.
