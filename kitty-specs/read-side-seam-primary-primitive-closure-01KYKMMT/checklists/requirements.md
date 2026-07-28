# Specification Quality Checklist: Read-Side Seam: Placement-Authority Closure

**Purpose**: Validate specification completeness and quality before proceeding to planning
**Created**: 2026-07-28 · **Revalidated**: 2026-07-28 after two scope revisions (see Provenance note)
**Feature**: [spec.md](../spec.md)

## Content Quality

- [x] No implementation details (languages, frameworks, APIs) — *see Note 1*
- [x] Focused on user value and business needs
- [x] Written for non-technical stakeholders — *see Note 1*
- [x] All mandatory sections completed

## Requirement Completeness

- [x] No [NEEDS CLARIFICATION] markers remain (zero markers; every open scope question was resolved by an explicit operator decision before authoring)
- [x] Requirements are testable and unambiguous
- [x] Requirement types are separated (Functional / Non-Functional / Constraints)
- [x] IDs are unique across FR-###, NFR-###, and C-### entries (FR-001…017, NFR-001…009, C-001…008)
- [x] All requirement rows include a non-empty Status value (all `Open`)
- [x] Non-functional requirements include measurable thresholds — *see Note 2*
- [x] Success criteria are measurable (SC-001…011 are counts, identity assertions, or binary gate outcomes)
- [x] Success criteria are technology-agnostic — *see Note 1*
- [x] All acceptance scenarios are defined (6 user stories × 3–4 scenarios each)
- [x] Edge cases are identified (10, including the backfilled composed-handle divergence and the foundation-site recursion hazard)
- [x] Scope is clearly bounded (explicit Out of Scope section + C-006 scope boundary + C-004/FR-005 naming what is deliberately *not* touched)
- [x] Dependencies and assumptions identified (Assumptions section, 5 entries, each either independently verified or explicitly scheduled for re-derivation)

## Feature Readiness

- [x] All functional requirements have clear acceptance criteria (each FR maps to a user story whose Acceptance Scenarios are the criteria)
- [x] User scenarios cover primary flows (single placement authority, delegation-surfaces-the-delta, no-green-by-omission, husk protection, ledger integrity, residual + record closure)
- [x] Feature meets measurable outcomes defined in Success Criteria
- [x] No implementation details leak into specification — *see Note 1*

## Notes

**Note 1 — "no implementation details" / "non-technical stakeholders" / "technology-agnostic", in context.**
This is an infrastructure mission in a developer-tooling repository: the product
surface *is* code and architectural gates, and the primary actor is a
maintainer/agent, not an end user. The spec names code surfaces where they are the
*subject* of a requirement, not as an implementation choice, and it does not prescribe
diff shapes, control flow, or new APIs. Context & Motivation and Domain Language carry
a plain-language account of PRIMARY/COORD partitions, "semi-compliance", and the
husk, so a stakeholder who has not followed the programme can read it. `meta.json`'s
`purpose_tldr` / `purpose_context` are written for that reader. Matches the
established pattern for this repo's infrastructure missions. PASS with rationale
recorded rather than silently ticked.

**Note 2 — NFR thresholds are identity / zero-count / enumerated-condition assertions.**
The mission changes no performance characteristic, so the meaningful thresholds are
equality and zero-count claims: identical resolved directory for materialized
missions (NFR-001), zero new raises (NFR-002), enumerated gate-bite conditions
(NFR-004), no site passing by omission (NFR-005), recorded before/after integers for
any floor that moves (NFR-007), and no cycle in the resolver call graph (NFR-009).
Each is mechanically checkable.

**Note 3 — Provenance: two scope revisions, both evidence-driven.**

*Draft 1* inherited #3014's premise. A two-lens post-spec squad (architect + patterns)
returned **10 MAJOR findings** against the live tree, three falsifying that premise:
`primary_feature_dir_for_mission` is already censused (on the *anchoring* axis) by
`test_resolution_authority_gates.py`; its **fail-loud** surface is zero; and a
*fourth* kind-blind resolver (`resolve_feature_dir_for_mission`, 8 sites / 7 files) is
the genuinely unpoliced gap. The squad also **executed** the prescribed ledger
restructuring and showed it parses *silently vacuously*, showed the stay-lenient index
cannot represent a multi-site qualname, and showed that deleting the `#2214` pin reds a
test by construction.

*Draft 2* (honest-reframe, operator-chosen) dropped the vacuous fail-loud migration and
kept record-correction + policing the real gap.

*Draft 3* (this one) followed the operator's question — do the "already policed" sites
route through the seam, or are they semi-compliance with a hardcoded target? A
placement-authority audit established: the 34 sites pass a canonical *handle* (all the
floors check) while **hardcoding the partition at the call site**;
`read_dir(<PRIMARY kind>)` is answer-equivalent across eight real-repo fixtures and
**strictly better** on a backfilled mission (the blind composition returns a
non-existent path); the 33 compositions are hand-inlined resolver internals
(`resolve_planning_read_dir`'s PRIMARY leg *is* that composition); the six "lands on the
husk" comments argue against a *different* resolver and do not survive as an argument;
and the floor collision is bookkeeping with five recorded in-tree shrinks, one for this
exact routing move. The operator prescribed **delegate-then-remove** and chose to carry
both steps here. Two live gate holes were found and folded in as FR-001 (a canonicalizer
the fold set does not recognise, and allow-sets that would let migrated sites go
green-by-omission).

Every MAJOR is now a requirement or a constraint: FR-008/009 (grammar and index
prerequisites, before any rows), FR-014 (paired pin + pin-existence-test retirement),
FR-016 (record correction), FR-017 (honest bounds), FR-005 + NFR-009 (foundation sites
stay out; no resolution cycle), NFR-004 (per-primitive non-vacuity), NFR-005
(no green-by-omission), NFR-007 (honest floor accounting), C-004 (privatise, never
delete), C-005 (delegation is a hard sequencing gate). Note that C-004's meaning is
**reversed** from draft 2, where it excluded the primitive from scope.

**Note 4 — Two facts in the source issues were corrected, not inherited.**
(a) #2824's functional defect was already fixed (`6923d1d40`, regression-green,
independently re-verified) and its *suggested* fix would have broken `lanes.json`
placement — recorded as C-001. The issue was closed with that evidence; only its
comments remain in scope (FR-015). (b) #3014's census figure (40) is stale in both the
ledger and the gate docstring; FR-010/FR-016 re-derive and correct it rather than
trusting the issue text. The corrected findings were posted to #3014.

**Note 5 — Size and sequencing.**
17 FR / 9 NFR / 8 C / 11 SC across six user stories is larger than a typical mission
here. The tasks phase should expect roughly 8–10 work packages, with two hard
sequencing gates: the grammar/index prerequisites (FR-008/009) before any ledger rows,
and the delegation (FR-002/003) before any call-site rewrite (C-005). The floors move
only in Step 2, deliberately (NFR-007).

- Items marked incomplete require spec updates before `/spec-kitty.plan` — none are incomplete.
