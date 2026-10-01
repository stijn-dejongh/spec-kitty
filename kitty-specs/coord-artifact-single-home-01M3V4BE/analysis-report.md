---
schema_version: 1
artifact_type: spec-kitty.analysis-report
command: /spec-kitty.analyze
mission_slug: coord-artifact-single-home-01M3V4BE
mission_id: 01M3V4BEWYPR3TP9N6A95A44KN
generated_at: '2026-10-01T09:29:37.580795+00:00'
analyzer_agent: unknown
input_artifacts:
  spec.md:
    path: kitty-specs/coord-artifact-single-home-01M3V4BE/spec.md
    sha256: a949c969dd2855525607128d5675f092e8124aa5dc8010dc90490cfa0629c5bd
  plan.md:
    path: kitty-specs/coord-artifact-single-home-01M3V4BE/plan.md
    sha256: a16264fab8fac96ab8be867406518fa12a05d296f22825e1fba49e9b47ee22bd
  tasks.md:
    path: kitty-specs/coord-artifact-single-home-01M3V4BE/tasks.md
    sha256: a9d500bc6162087ff883d4a5baa21ad3fd0bcfd8840b631659cbfd498b729e1d
  charter:
    path: .kittify/charter/charter.yaml
    sha256: 69c63e91ae27a02b0c07b48939f72198b0d2654ed5bee42e3d6bc1d5d4e71a6e
verdict: blocked
issue_counts:
  medium: 6
  low: 11
  high: 2
  critical: 0
  info: 0
findings:
- id: C1
  severity: high
  category: charter
  summary: NFR-001 lets coordination create take up to about 3.65 s with no absolute bound, which conflicts with the charter's 'CLI operations must complete in < 2 seconds'. plan.md's Charter Check omits the performance rule and says 'No violation needs justifying'.
- id: G1
  severity: high
  category: coverage
  summary: FR-009b names setup-plan and finalize-tasks as decision-ledger committers. Neither commits decisions/ today and no code WP changes that, yet WP21 T119 asserts it and routes a failure to an owner that does not exist.
- id: I1
  severity: medium
  category: inconsistency
  summary: 'Post-tasks squad folds were not carried into the design artifacts: WriteLocation.checkout_root, coordination/event_prefix.py and union_decision_index are missing from the contracts, data-model.md and plan.md. The traces put the seed in surface_resolver.py; the plan puts it in coord_seed.py.'
- id: I2
  severity: medium
  category: inconsistency
  summary: FR-006/US3.1 list exactly four named refusal reasons for COORD records. WP05 T029 also refuses with remote-only (COORDINATION_WORKTREE_UNMATERIALIZED) and COORD_SEED_FORK_REFUSED, which are not in the spec or in the commit-outcome contract's reason table.
- id: U1
  severity: medium
  category: underspecification
  summary: contracts/seed.md lets a refused seed commit (protected coordination ref) leave the seed uncommitted while the write proceeds. Spec FR-004 says the seed commits once before the triggering write proceeds and asserts one seed commit. The refusal path is not specified.
- id: C2
  severity: medium
  category: charter
  summary: tasks.md says every code WP is RED on its base, which does not fit WP01, WP02, WP20 or WP21. WP21's Review Guidance makes the charter-required RED check on planning_base_branch optional.
- id: C3
  severity: medium
  category: charter
  summary: No task covers CHANGELOG, migration-guide or user-docs updates for the operator-visible behaviour changes (charter Code Review Checklist and Documentation Standards; DIRECTIVE_037). WP22 covers only the ADRs and the seam doc.
- id: C4
  severity: medium
  category: charter
  summary: 'The WP prompts omit two implement-time charter duties: appending to the Mission tracer files (Standing Order 3) and the Pre-existing Failure Reporting Rule (MUST open a GitHub issue). They only say to classify a baseline red.'
- id: A1
  severity: low
  category: ambiguity
  summary: Spec US1 presents `--pr-bound --start-branch` from the primary branch as a coordination-routed create path without noting it requires a protected primary branch. WP21 found it defaults to `lanes` on an unprotected primary.
- id: A2
  severity: low
  category: ambiguity
  summary: "'Loud' and 'loudly' (US2.7, FR-003a) are not defined in the spec; only the contract makes them concrete (a WARNING log)."
- id: A3
  severity: low
  category: ambiguity
  summary: FR-003 says the write location is the coordination surface 'in every coordination-worktree state', but FR-003a requires refusals for the remote-only and missing-branch states.
- id: I3
  severity: low
  category: inconsistency
  summary: "plan.md carries stale counts: gate floor >= 18 in the Charter Check vs >= 22 in IC-15, D18 and WP20; R1-R21 and '21 reproductions' vs R1-R24 plus R1d; D1-D20 vs D1-D21."
- id: I4
  severity: low
  category: inconsistency
  summary: tasks.md and WP02 still call WP19 a parallel root that runs 'from the start', although WP19 depends on WP02 (P-m6). The Sequence line is ambiguous.
- id: I5
  severity: low
  category: inconsistency
  summary: "WP05 says 'Plan order: IC-10 -> IC-07 core -> IC-06', but the plan.md shared-file map says 10 -> 06 -> 07, and IC-07 depends on IC-06."
- id: I6
  severity: low
  category: inconsistency
  summary: The research.md red-first note and plan.md Project Structure name the standalone adopted repro files as their permanent homes, while R-M8 folds them into the owning module test files and deletes the standalone files.
- id: G2
  severity: low
  category: coverage
  summary: FR-017 is mapped only to WP22, yet WP12 T065 (stale residue comments) and WP04 T022 (seam docstrings, CoordState.EMPTY text) deliver parts of FR-017 without listing it.
- id: C5
  severity: low
  category: charter
  summary: The decision-ledger partition reversal (#3928) is recorded only as a subsection of ADR 2026-06-19-1 (empty-surface fallback). The charter wants major changes in an ADR, and new ADRs belong in docs/adr/4.x.
- id: U2
  severity: low
  category: underspecification
  summary: The named post-consolidation fold (retire the router's root-staging shutil.copy2) has no tracker reference; the charter requires deferred work to be tracked.
- id: G3
  severity: low
  category: coverage
  summary: "The spec Assumption says the issue matrix records #2533's claim-leg verdict, but no WP or subtask owns that, and the issue-matrix.json rows are still placeholders."
---

## Specification Analysis Report

**Mission:** `coord-artifact-single-home-01M3V4BE`.

**Artifacts analysed:**
- spec.md (revision 3), plan.md, tasks.md;
- WP01–WP22 (frontmatter, objectives, subtasks, DoD);
- research.md, data-model.md, contracts/*;
- squad-post-spec.md, squad-post-tasks.md, traces/design-decisions.md, issue-matrix.json;
- the charter (v1.4.0).

**Verdict: BLOCKED.** There are 2 HIGH findings. Both are document fixes; neither needs a redesign.

Findings the squads already dispositioned were not re-raised, unless the fold is missing from an artifact (I1, I4, I6, U2).

| ID | Category | Severity | Location(s) | Summary | Recommendation |
|----|----------|----------|-------------|---------|----------------|
| C1 | Charter | HIGH | spec.md NFR-001; plan.md Charter Check, Technical Context; charter §Performance and Scale; research.md NFR-001 baseline | NFR-001 allows create up to about 3.64 s ("There is no absolute bound"). The charter says "CLI operations must complete in < 2 seconds". The base already measures 2.64 s, and the operator ruled Q2 knowing this. Even so, the Charter Check never lists the performance rule and claims "No violation needs justifying". | Add a Charter Check row: *Performance and Scale: DEVIATION (accepted)*, citing ruling Q2 and noting the base already exceeds 2 s. Record it under Complexity Tracking. |
| G1 | Coverage | HIGH | spec.md FR-009b; WP21 T119 step 2; WP14, WP15; `mission_finalize.py:274-356` | FR-009b names spec-commit, setup-plan, finalize-tasks and accept as ledger committers. At base, finalize-tasks does not collect `decisions/`, and setup-plan commits only plan artefacts; no code WP changes either. WP21 T119 asserts that "setup-plan or finalize-tasks" commits an uncommitted ledger, and routes a failure to an owning WP that does not exist. | Pick one. (a) Narrow FR-009b's committer list to spec-commit and accept (WP12/WP16) and narrow T119 to match. (b) Add ledger candidates plus red-first tests to WP14/WP15. Either way, remove the "or" in T119. |
| I1 | Inconsistency | MEDIUM | contracts/write-location-accessor.md; data-model.md; plan.md Project Structure; contracts/seed.md; traces/design-decisions.md | Fold results missing from the design docs: `WriteLocation.checkout_root` (P-M3), `coordination/event_prefix.py` and `union_decision_index` (P-M6). The seed location also differs between the traces and the plan. | Update the contracts, data-model and plan Project Structure to match the WPs. |
| I2 | Inconsistency | MEDIUM | spec.md FR-006, US3.1; WP05 T029; contracts/commit-outcome.md | The remote-only and seed-fork refusals reach the commit result but are not in the spec's closed reason list or the contract table. | Add both to FR-006/US3.1 and the contract reason table. |
| U1 | Underspecification | MEDIUM | contracts/seed.md errors; spec.md FR-004, US2.4; WP03 T015 | The refused seed commit (protected coordination ref) path is not in the spec. | Add an edge case: what the operator sees, and that the next coordination commit carries the seed. Test it in WP03. |
| C2 | Charter | MEDIUM | tasks.md; charter §ATDD-First; WP21 Review Guidance; WP01, WP02, WP20 | The red-on-base rule as stated does not fit WP01, WP02, WP20 or WP21. WP21 makes the check optional. | State each WP's red evidence: WP01/WP02 exempt as tidy-first and harness; WP20 red at `ecb5dd914a` plus mutation; WP21 red on planning_base_branch, required. |
| C3 | Charter | MEDIUM | charter Code Review Checklist, Documentation Standards; DIRECTIVE_037 | No CHANGELOG or CLI-docs task covers the operator-visible changes: the finalize pin refresh, the accept ledger commit, the consolidation dirty gate, consolidation materializing (R23), `spec-commit success=false`, `materialize` creating worktrees, and the merge-driver migration. | Add CHANGELOG and help/reference subtasks. |
| C4 | Charter | MEDIUM | Standing Order 3; Implement governance; Pre-existing Failure Reporting Rule | The WP prompts omit the tracer-append duty and the duty to file an issue for a pre-existing failure. | Add one line to each WP's quality gates. |
| A1 | Ambiguity | LOW | spec.md US1 | The protected-primary precondition for the default coordination create path is unstated. | Add the precondition. |
| A2 | Ambiguity | LOW | spec.md US2.7, FR-003a | "Loud" is undefined. | Define it as a WARNING-level log line naming the Mission, the state and the action. |
| A3 | Ambiguity | LOW | spec.md FR-003 vs FR-003a | "Every coordination-worktree state" contradicts the required refusals. | Reword: "...or a named refusal (FR-003a); never the repository root checkout". |
| I3 | Inconsistency | LOW | plan.md | Stale counts (gate floor 18/22, R1-R21/R24, D1-D20/21). | Align them. |
| I4 | Inconsistency | LOW | tasks.md; WP02 | WP19 is still described as a root. | Correct the prose. |
| I5 | Inconsistency | LOW | tasks.md WP05 goal; plan.md | The WP05 order is credited to the plan, which says otherwise. | Reword as a stated deviation. |
| I6 | Inconsistency | LOW | research.md; plan.md | The standalone repro files are named as permanent homes. | Update to the R-M8 fold-in homes. |
| G2 | Coverage | LOW | tasks.md coverage table; WP12 T065; WP04 T022 | Parts of FR-017 are delivered but not mapped. | Add FR-017 to WP04/WP12 refs. |
| C5 | Charter | LOW | WP22 T116; charter Amendment Process | The ledger reversal ADR is placed under an unrelated 3.x ADR. | Write a short dedicated 4.x ADR, or record why. |
| U2 | Underspecification | LOW | tasks.md named fold; squad-post-tasks.md | The deferred legacy-copy retirement has no tracker issue. | File a follow-up issue and cite it. |
| G3 | Coverage | LOW | spec.md Assumptions; issue-matrix.json | No step owns filling the issue-matrix verdicts (#2533 split verdict). | Name the accept/closeout step. |

### Coverage Summary Table

| Requirement Key | Has Task? | Task/WP IDs | Notes |
|-----------------|-----------|-------------|-------|
| FR-001 | Yes | WP06 | |
| FR-002 | Yes | WP06 | |
| FR-002a | Yes | WP06 | |
| FR-002b | Yes | WP06 | |
| FR-003 | Yes | WP04, WP07–WP10, WP14–WP16, WP18 | |
| FR-003a | Yes | WP03, WP04, WP07, WP09 | A3 |
| FR-004 | Yes | WP03 | U1 |
| FR-004a | Yes | WP03 | |
| FR-004b | Yes | WP03 | |
| FR-005 | Yes | WP16 | |
| FR-006 | Yes | WP05 | I2 |
| FR-007 | Yes | WP05, WP07, WP08, WP10, WP13–WP16, WP20 | |
| FR-007a | Yes | WP13 (+ WP12 T064) | |
| FR-007b | Yes | WP15 | |
| FR-008 | Yes | WP05 | |
| FR-009 | Yes | WP12, WP16 | |
| FR-009a | Yes | WP12 | |
| FR-009b | Partial | WP11, WP12, WP21 | G1 |
| FR-009c | Yes | WP17 | |
| FR-010 | Yes | WP17 | |
| FR-010a | Yes | WP17 | |
| FR-011 | Yes | WP17 | |
| FR-012 | Yes | WP15 | |
| FR-013 | Yes | WP19 | |
| FR-014 | Yes | WP20, WP18 | |
| FR-015 | Yes | WP21 | |
| FR-016 | Yes | WP02, WP05, WP06, WP09, WP13–WP15, WP17, WP18 | |
| FR-017 | Yes | WP22 | G2 |
| NFR-001 | Yes | WP06 | C1 |
| NFR-002 | Yes | WP02, WP03, WP17, WP18, WP21 | |
| NFR-003 | Yes | all WPs | |
| NFR-004 | Yes | WP01, WP13–WP15, all | |
| NFR-005 | Yes | all WPs | |
| C-001 | Yes | WP03, WP04 | |
| C-002 | Yes | WP04 | |
| C-003 | Yes | WP03, WP17 | |
| C-004 | Yes | WP03 | |
| C-005 | Yes | WP02 + per WP | C2 |
| C-006 | Policy | all WPs | process |
| C-007 | Policy | all WPs | process |
| C-008 | Yes | WP04, WP06, WP07, WP18 | |
| SC-001 | Yes | WP21 | |
| SC-002 | Yes | WP09, WP21 | |
| SC-003 | Yes | WP05, WP08, WP10, WP13–WP16 | |
| SC-004 | Yes | WP17 | |
| SC-005 | Yes | WP20 | |

All 38 acceptance scenarios (US1.1–US6.2) trace to at least one WP.

### Charter Alignment Issues

- C1 (HIGH): the performance deviation is not recorded.
- C2, C3, C4 (MEDIUM): the red-evidence statement, the docs/CHANGELOG task, and the tracer and failure-issue duties.
- C5 (LOW): ADR placement.
- Compliant: single canonical authority, the non-vacuous gate, NO_FULL_HEAVY_SUITES_IN_MISSION, the terminology canon, campsite-clean first, the C901/mypy/ruff/coverage gates.

### Unmapped Tasks

None. All 119 subtasks belong to a WP, and every WP's requirement_refs resolve to spec IDs.

### Metrics

| Metric | Value |
|--------|-------|
| Total requirements | 46 (28 FR, 5 NFR, 8 C, 5 SC) |
| Total WPs / subtasks | 22 / 119 |
| Coverage | 44/46 = 95.7% (C-006 and C-007 are process constraints; 100% of FR/NFR/SC are mapped) |
| Partially delivered | 1 (FR-009b) |
| Ambiguity | 3 |
| Duplication | 0 |
| Critical | 0 |
| High / Medium / Low | 2 / 6 / 11 |

### Next Actions

1. Resolve C1 and G1 before `/spec-kitty.implement`.
2. Fold the MEDIUM findings (I1, I2, U1, C2, C3, C4). These are document edits.
3. Fold the LOW findings where the artifacts are touched.
4. Re-run `/spec-kitty.analyze`.
