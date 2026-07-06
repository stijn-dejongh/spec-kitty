# Contract — Backlog Slice Ticket Shape

> Mission: `ci-hygiene-and-sonar-debt-remediation-01KWV531`
> Closes: FR-008, FR-009, C-003, C-004, NFR-004
> Data model: [../data-model.md §4-5](../data-model.md#4-backlogsliceticket-github-issue-shape-fr-008)

## Contract

Every GitHub issue filed by IC-07 (backlog slicing) MUST satisfy:

1. **Live data only (C-003)**: `body.rule_ids`, `body.live_issue_count` are
   pulled from a live SonarCloud API query (via the promoted
   `scripts/ci/sonarcloud_branch_review.sh`, IC-06) at filing time — never a
   placeholder or extrapolated estimate. The issue body must show the exact
   API query used, so the count is independently reproducible.
2. **Labels (C-004)**: exactly `tech-debt` + `quality` + `devex` — the
   latter two created ahead of filing, following this repo's existing label
   naming/coloring conventions (verified via `gh label list` before
   creation, not invented ad hoc).
3. **Milestone**: `3.2.x`.
4. **Parent**: filed as a native GitHub sub-issue of **#1928** (verified live
   during spec validation as the correct existing epic — do not re-derive
   this at implementation time, do not parent elsewhere without recording
   why).
5. **Effort/impact buckets**: `effort_bucket` and `impact_bucket` are always
   populated; a slice whose effort is genuinely unknown until investigated
   uses `effort_bucket: needs-triage`, never a forced guess.
6. **Completeness (NFR-004)**: after all slices are filed,
   `sum(live_issue_count)` across every filed ticket must equal the live
   SonarCloud open-issue count queried at the *start* of slicing (a single
   snapshot, not a moving target re-queried per ticket) — this equality is
   the mechanical verification for SC-005, not a manual eyeball check.

## Roadmap-aligned slice marking

Any ticket covering a module inside the Wave 2 degod trio
(`workflow.py`/`implement.py`/`acceptance/__init__.py`) or a live #1868/#2173
sub-issue's file scope gets an explicit note in its body identifying it as
"roadmap-aligned — fixed in mission `ci-hygiene-and-sonar-debt-remediation-01KWV531`"
(for the ones FR-010 actually fixes) or "roadmap-aligned but excluded — see
`RoadmapSliceExclusion`" (for the ones the C-001 triage rule excludes, per
[data-model.md §5](../data-model.md#5-roadmapsliceexclusion-tracking-record-c-001fr-010-triage-rule)).
This is the mechanism that makes SC-006's "reduced to zero, excluding
recorded exclusions" claim auditable after the fact.

## Verification

- Before closing this mission: re-query the live SonarCloud backlog count
  and confirm it equals the sum of all filed-ticket `live_issue_count`
  values plus the count of issues fixed directly (not re-ticketed) by IC-08
  — i.e., no issue is double-counted or dropped between "ticketed" and
  "fixed".
