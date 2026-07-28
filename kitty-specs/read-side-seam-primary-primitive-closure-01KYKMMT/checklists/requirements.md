# Specification Quality Checklist: Read-Side Seam: Primary-Primitive Closure

**Purpose**: Validate specification completeness and quality before proceeding to planning
**Created**: 2026-07-28
**Feature**: [spec.md](../spec.md)

## Content Quality

- [x] No implementation details (languages, frameworks, APIs) — *see Note 1*
- [x] Focused on user value and business needs
- [x] Written for non-technical stakeholders — *see Note 1*
- [x] All mandatory sections completed

## Requirement Completeness

- [x] No [NEEDS CLARIFICATION] markers remain (zero markers; both open scope questions were resolved by the operator before authoring)
- [x] Requirements are testable and unambiguous
- [x] Requirement types are separated (Functional / Non-Functional / Constraints)
- [x] IDs are unique across FR-###, NFR-###, and C-### entries (FR-001…010, NFR-001…006, C-001…006)
- [x] All requirement rows include a non-empty Status value (all `Open`)
- [x] Non-functional requirements include measurable thresholds (identity-of-result, zero-count, and enumerated bite conditions — see Note 2)
- [x] Success criteria are measurable (SC-001…008 are counts, percentages, or binary gate outcomes)
- [x] Success criteria are technology-agnostic — *see Note 1*
- [x] All acceptance scenarios are defined (4 user stories × 2–4 scenarios each)
- [x] Edge cases are identified (7, including the backfilled composed/bare-handle case that caused a silent wrong answer in the predecessor mission)
- [x] Scope is clearly bounded (explicit Out of Scope section + C-004 scope boundary)
- [x] Dependencies and assumptions identified (Assumptions section, 5 entries, each independently verified or scheduled for re-derivation)

## Feature Readiness

- [x] All functional requirements have clear acceptance criteria (each FR maps to a user story whose Acceptance Scenarios are the criteria)
- [x] User scenarios cover primary flows (silent-wrong-read prevention, enforcement against reintroduction, authority integrity, residual closure)
- [x] Feature meets measurable outcomes defined in Success Criteria
- [x] No implementation details leak into specification — *see Note 1*

## Notes

**Note 1 — "no implementation details" / "non-technical stakeholders" / "technology-agnostic", in context.**
This is an infrastructure mission in a developer-tooling repository: the product
surface *is* code and architectural gates, and the primary actor is a
maintainer/agent, not an end user. The spec therefore names code surfaces
(`primary_feature_dir_for_mission`, `MissionArtifactKind`, the two gate modules)
where they are the *subject* of the requirement, not an implementation choice. It
deliberately does **not** prescribe how to implement any change (no diff shapes, no
control flow, no new APIs). The Context & Motivation and Domain Language sections
carry a plain-language explanation of PRIMARY/COORD partitions and what a
"topology-blind primitive" is, so a stakeholder who has not followed the programme
can read the spec. This matches the established pattern for this repo's
infrastructure missions (e.g. the predecessor read-side migration spec). Treated as
PASS with this rationale recorded rather than silently ticked.

**Note 2 — NFR thresholds are identity/zero-count assertions, not latency numbers.**
This mission changes no performance characteristic, so the meaningful measurable
thresholds are equality and zero-count claims (resolved directory identical in the
healthy case; zero lenient or flat-topology sites begin raising; enumerated
gate-bite conditions all hold; census totals reconcile exactly). Each is
mechanically checkable.

**Note 4 — The spec was RE-FRAMED after a post-spec adversarial squad (2026-07-28).**
The first draft inherited #3014's premise and a two-lens squad (architect +
patterns) returned **10 MAJOR findings** against the live tree, three of which
falsified the premise: (a) `primary_feature_dir_for_mission` is already
census-policed on the anchoring axis by `test_resolution_authority_gates.py`;
(b) its fail-loud surface is **zero** — all 34 in-scope sites read a PRIMARY
artifact off a deliberately PRIMARY anchor, six with comments stating the
topology-routed resolver would be wrong — and migrating them would red two census
floors plus a third module; (c) a **fourth** kind-blind resolver
(`resolve_feature_dir_for_mission`, 8 sites / 7 files) is the genuinely unpoliced
gap. The squad also *executed* the originally-prescribed ledger restructuring and
demonstrated it parses **silently vacuously**, and showed the index grammar cannot
represent a multi-site qualname, and that deleting the `#2214` pin reds a test by
construction. The operator chose the honest-reframe. Every MAJOR is now either a
requirement (FR-004/005 grammar prerequisites, FR-002 paired retirement, FR-011
record correction, FR-012 honest bounds, NFR-004 per-primitive non-vacuity, NFR-007
no floor breakage) or an explicit constraint (C-004 excludes the mis-identified
primitive with rationale). Re-validated against every checklist item after the
rewrite.

**Note 3 — Two facts in the source issues were corrected during authoring.**
(a) #2824's functional defect is already fixed (`6923d1d40`, regression-green,
independently re-verified) and its *suggested* fix would have broken `lanes.json`
placement — recorded as C-001 and C-004 so it cannot be reintroduced. (b) #3014's
census figure (40 sites) is stale; the live count differs and the file set changed,
so FR-004 re-derives it rather than trusting the issue text, and NFR-006/SC-006
require the stale figure in the existing ledger to be corrected.

- Items marked incomplete require spec updates before `/spec-kitty.plan` — none are incomplete.
