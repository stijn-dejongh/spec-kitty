---
schema_version: 1
artifact_type: spec-kitty.analysis-report
command: /spec-kitty.analyze
mission_slug: coord-artifact-single-home-01M3V4BE
mission_id: 01M3V4BEWYPR3TP9N6A95A44KN
generated_at: '2026-10-01T09:56:11.629431+00:00'
analyzer_agent: unknown
input_artifacts:
  spec.md:
    path: kitty-specs/coord-artifact-single-home-01M3V4BE/spec.md
    sha256: 2d63d0ea68076f51227df92cbaed46872301386ebd18956639d139c2b936ee8e
  plan.md:
    path: kitty-specs/coord-artifact-single-home-01M3V4BE/plan.md
    sha256: da19c321ba05724abeeeb84fa7e5f2733f8b9afc54a3cde28aea4030ed33d0d0
  tasks.md:
    path: kitty-specs/coord-artifact-single-home-01M3V4BE/tasks.md
    sha256: 40e074a41a517dd2e3d715a3852a0e8e91dc63d5daaf9f5584b9b3f5a5bcaa2b
  charter:
    path: .kittify/charter/charter.yaml
    sha256: 69c63e91ae27a02b0c07b48939f72198b0d2654ed5bee42e3d6bc1d5d4e71a6e
verdict: ready
issue_counts:
  critical: 0
  low: 10
  high: 0
  medium: 3
  info: 0
findings:
- id: I7
  severity: medium
  category: inconsistency
  summary: 'Merge-class guard: plan IC-11, research D13 and traces/design-decisions move `decisions` into the divergent set ({traces, decisions}); WP12 Binding / OD-WP12 keeps it in _NON_DIVERGENT_COORD_RESIDUE_DIRS. No Decision Moment records the interpretation.'
- id: I8
  severity: medium
  category: inconsistency
  summary: 'Topology-less residue callers: plan IC-11, research D12, data-model L28 and plan Project Structure keep the legacy COORD answer via _TOPOLOGY_LESS_LEGACY_RESIDUE_KINDS; WP12 Binding resolves the stored topology at the coherence.py predicate, which widens coordination-Mission behaviour, and its red-first test covers only lanes/single_branch.'
- id: U3
  severity: medium
  category: underspecification
  summary: The D4 post-fix discriminator (Spec-Kitty-Coordination-Seed trailer) has no owning subtask. WP06 never writes it on the create commit; WP03 T015 does not require it, and WP03 Binding offers a tree-content discriminator that D4 rejected. No WP adds it after a refused seed commit.
- id: C3
  severity: low
  category: charter
  summary: WP17's operator-visible changes (fork report, repair exit 1, verify exit 1 on a fork, teardown/discard refusal) have no help-text or reference-delta line, and WP22's delta list omits them.
- id: I3
  severity: low
  category: inconsistency
  summary: plan.md Charter Check still says the gate floor is >= 18 writer functions; IC-15, D18 and WP20 say >= 22.
- id: I4
  severity: low
  category: inconsistency
  summary: tasks.md L115 and L712 still call WP19 a root that runs from the start.
- id: I9
  severity: low
  category: inconsistency
  summary: WP19's conditional fallback (fix the lanes/single_branch sha=None receipt) would change lanes/single_branch output against C-008 with no recorded exception, and leave FR-013/US6 without a red on a coordination Mission.
- id: I10
  severity: low
  category: inconsistency
  summary: 'Stale cross-references: tasks.md header says spec rev 3 and research D1-D21; WP01 says D1-D21; no WP prompt cites D22/D23, although the WP03/WP04 Bindings implement them.'
- id: I11
  severity: low
  category: inconsistency
  summary: Text superseded by the Binding corrections is left unstruck in WP21, WP06, plan IC-01/IC-02 and tasks.md T033/WP01/WP14.
- id: I12
  severity: low
  category: inconsistency
  summary: mark-status is still listed as a commit-outcome consumer in spec FR-007, plan IC-07, research D8 and tasks.md T046, though the shim is dead; plan IC-04 names the wrong mark-status write site.
- id: I13
  severity: low
  category: inconsistency
  summary: Spec FR-017's anchor list omits the new 4.x ADR (2026-10-01-2) that carries the ledger reversal.
- id: I14
  severity: low
  category: inconsistency
  summary: tasks.md calls WP01 a concurrent root, but lanes.json puts it in lane-a, which depends on lane-c (WP03); the prose lane names also differ from the lanes.json ids.
- id: G4
  severity: low
  category: coverage
  summary: WP16 T087 delivers the accept leg of FR-009b without FR-009b in its requirement_refs.
---

## Specification Analysis Report

**Mission:** `coord-artifact-single-home-01M3V4BE`. This is a re-run after the analyze plus brownfield-scout fold (round 3).

**Result:** the verdict is **READY**. Both previous HIGH findings (C1, G1) are resolved. Of the 19 previous findings, 15 are resolved and 3 are partial (C3, I3, I4); C3 drops to low.

The three new MEDIUM findings come from parallel fold edits that drifted apart: the design docs and the binding WP text no longer agree. Resolve I7 and I8 before WP12, and U3 before WP03.

| ID | Category | Severity | Location(s) | Summary | Recommendation |
|----|----------|----------|-------------|---------|----------------|
| I7 | Inconsistency | MEDIUM | plan IC-11; research D13; traces; WP12 Binding | The design docs and WP12 disagree on which merge-class guard set holds `decisions`. | Decide (Decision Moment) and fold everywhere. |
| I8 | Inconsistency | MEDIUM | research D12; plan IC-11; data-model L28; WP12 Binding | Two designs for topology-less callers: a legacy set, or the single predicate resolving the stored topology. | Pick one; if the single predicate wins, add coordination-Mission tests at move-task, implement and auto-rebase. |
| U3 | Underspecification | MEDIUM | research D4; contracts/seed.md; WP03 T015; WP06 T031 | Nothing owns writing the seed trailer discriminator. | Bind the trailer in WP03 and WP06 through a shared constant; drop the tree-content alternative; decide who writes it after a refused seed commit. |
| C3 | Charter | LOW | WP17; WP22 | WP17's docs and help-text deltas are missing. | Add a C3 line and the WP22 deltas. |
| I3 | Inconsistency | LOW | plan.md L46 | Stale gate floor. | Change to ≥ 22. |
| I4 | Inconsistency | LOW | tasks.md L115, L712 | WP19 is still called a root. | Fix both lines. |
| I9 | Inconsistency | LOW | WP19 Binding; spec C-008/FR-013/US6 | The fallback could change lanes/single_branch output. | Record a C-008 exception if the fallback triggers. |
| I10 | Inconsistency | LOW | tasks.md L8; WP01 L107 | Stale rev/D-range references; D22/D23 not cited. | Update them. |
| I11 | Inconsistency | LOW | WP21, WP06, plan IC-01/IC-02, tasks.md | Superseded text is not struck. | Strike it inline and align plan/tasks. |
| I12 | Inconsistency | LOW | spec FR-007; plan IC-07, IC-04; research D8; tasks.md T046 | mark-status is listed as a consumer. | Remove it or qualify it; fix the IC-04 site. |
| I13 | Inconsistency | LOW | spec FR-017 | The 4.x ADR is missing from the anchors. | Add it. |
| I14 | Inconsistency | LOW | tasks.md; lanes.json | WP01 parallelism claim and lane-name prose are wrong. | Align with lanes.json. |
| G4 | Coverage | LOW | WP16 frontmatter | FR-009b is missing from WP16's refs. | Add it. |

### Coverage Summary Table

| Requirement | Has task? | WP(s) |
|-------------|-----------|-------|
| FR-001 | Yes | WP06 |
| FR-002 | Yes | WP06 |
| FR-002a | Yes | WP06 |
| FR-002b | Yes | WP06 |
| FR-003 | Yes | WP04, WP07–WP10, WP14–WP16, WP18 |
| FR-003a | Yes | WP03, WP04, WP07, WP09 |
| FR-004 | Yes | WP03 |
| FR-004a | Yes | WP03 |
| FR-004b | Yes | WP03 |
| FR-005 | Yes | WP16 |
| FR-006 | Yes | WP05 |
| FR-007 | Yes | WP05, WP07, WP08, WP10, WP13–WP16, WP20 |
| FR-007a | Yes | WP13 |
| FR-007b | Yes | WP15 |
| FR-008 | Yes | WP05 |
| FR-009 | Yes | WP12, WP16 |
| FR-009a | Yes | WP12 |
| FR-009b | Yes | WP11, WP12, WP21 (+ WP16) |
| FR-009c | Yes | WP17 |
| FR-010 | Yes | WP17 |
| FR-010a | Yes | WP17 |
| FR-011 | Yes | WP17 |
| FR-012 | Yes | WP15 |
| FR-013 | Yes | WP19 |
| FR-014 | Yes | WP18, WP20 |
| FR-015 | Yes | WP21 |
| FR-016 | Yes | WP02, WP05, WP06, WP09, WP13–WP15, WP17, WP18 |
| FR-017 | Yes | WP04, WP12, WP22 |
| NFR-001 | Yes | WP06 (accepted deviation recorded) |
| NFR-002 | Yes | WP02, WP03, WP17, WP18, WP21 |
| NFR-003 | Yes | all WPs |
| NFR-004 | Yes | all WPs |
| NFR-005 | Yes | all WPs |
| C-001 | Yes | WP03, WP04 |
| C-002 | Yes | WP04 |
| C-003 | Yes | WP03, WP17 |
| C-004 | Yes | WP03 |
| C-005 | Yes | all code WPs |
| C-006 | Policy | all WPs |
| C-007 | Policy | all WPs |
| C-008 | Yes | WP04, WP06, WP07, WP12, WP18 |
| SC-001 | Yes | WP21 |
| SC-002 | Yes | WP09, WP21 |
| SC-003 | Yes | WP05, WP08, WP10, WP13–WP16 |
| SC-004 | Yes | WP17 |
| SC-005 | Yes | WP20 |

All 38 acceptance scenarios still trace to at least one WP.

### Charter Alignment Issues

- No CRITICAL or HIGH charter issue.
- Performance: an accepted deviation is recorded (operator ruling).
- ATDD-First: the red-evidence table states the exemptions.
- Tracer and pre-existing-failure duties: present in every WP.
- C3 is LOW (WP17 only).
- C5 is resolved by the planned 4.x ADR.

### Unmapped Tasks

None. All 119 subtasks belong to a WP; one delivered requirement is unmapped (G4).

### Metrics

| Metric | Value |
|--------|-------|
| Total requirements | 46 |
| Total WPs / subtasks / lanes | 22 / 119 / 16 |
| Coverage | 95.7% (100% of FR/NFR/SC; C-006 and C-007 are process constraints) |
| Previous findings | 19: 15 resolved, 3 partial |
| New findings | 10 |
| Critical / High / Medium / Low | 0 / 0 / 3 / 10 |

### Next Actions

1. No blocker for implement. Resolve I7 and I8 before WP12, and U3 before WP03.
2. Fold the LOW findings when the artifacts are next touched.
