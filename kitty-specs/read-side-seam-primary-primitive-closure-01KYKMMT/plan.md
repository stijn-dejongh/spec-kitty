# Implementation Plan: Read-Side Seam: Placement-Authority Closure

**Branch**: `fix/read-side-seam-primary-primitive-closure` | **Date**: 2026-07-28 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `kitty-specs/read-side-seam-primary-primitive-closure-01KYKMMT/spec.md`

**Branch contract**: current branch at plan start `fix/read-side-seam-primary-primitive-closure`; planning/base branch `fix/read-side-seam-primary-primitive-closure`; final merge target `fix/read-side-seam-primary-primitive-closure`; `branch_matches_target = true`.

## Summary

Move the "which surface does this artifact live on?" decision out of 34 call sites and
into the one resolver that owns it, using a **delegate-then-remove** refactor; police the
one kind-blind resolver that no gate covers; close two coord-awareness residuals; and
write the layering down once in `docs/architecture/` so the next mission cites a design
document instead of repeating a multi-round audit.

Two prerequisites gate everything else: the ledger's parse grammar and its per-site index
must be fixed **before** any classification row is written (a naive multi-primitive
restructuring was demonstrated to parse silently-empty), and the delegation must land and
be verified **before** any call site is rewritten (it is the step that surfaces hidden
behaviour with the existing suite as harness, at one file's cost).

## Technical Context

**Language/Version**: Python 3.11+ (repository standard; `pyproject.toml` `requires-python`)
**Primary Dependencies**: no new runtime dependencies. Internal surfaces only — `mission_runtime` (placement seam: `resolution.py`, `artifacts.py`, `context.py`), `specify_cli.missions._read_path_resolver` (path constructors), and the architectural gate suite under `tests/architectural/`
**Storage**: filesystem + git only (mission artifacts under `kitty-specs/<mission>/`; no database)
**Testing**: `pytest` with targeted node-ids (C-008 — the exhaustive `tests/architectural/` sweep is CI's responsibility, never local); `uv run pytest` / `uv run mypy` inside lane worktrees; AST-based architectural gates as the enforcement mechanism; red-first evidence per behavioural change (NFR-003)
**Target Platform**: Linux/macOS developer machines and CI (the `spec-kitty` CLI)
**Project Type**: single project — library + CLI, existing `src/` layout
**Performance Goals**: none — no performance characteristic changes. The operative goals are correctness and enforceability
**Constraints**: behaviour-preserving except one named delta (NFR-001); no new raises where leniency is the contract (NFR-002); no resolution cycle (NFR-009); no floor relaxed without recorded before/after (NFR-007); frozen stores untouched — `BOUNDARY_SANCTIONED_PREFIXES`, the doctrine glossary pack and its seed (C-005, FR-019)
**Scale/Scope**: 34 in-scope call sites for the primary primitive (33 semi-compliant + 1 non-compliant) across ~19 files; 8 sites for the unpoliced resolver across 7 files; 2 architectural gates extended, 2 census floors retired or re-pinned, 3 gate allow-sets widened; 1 new architecture page + 1 narrowed page + 1 glossary entry + 1 Terminology Canon line

## Charter Check

Charter present at `.kittify/charter/charter.md`; context loaded for the `plan` action
(`mode: compact`, template set `software-dev-default`, directives DIR-001…013).

| Principle | Status | Note |
|---|---|---|
| Single canonical authority | **Advanced by this mission** | The mission's thesis *is* this principle: one resolver decides placement. FR-020 additionally retires a competing documentation authority. |
| Architectural alignment | **Pass** | Aligns to ADR `2026-06-24-1` (kind-and-topology-aware placement) and ADR `2026-07-23-1` (`TopologySurface` vocabulary, forbidden-conditioning rule). No new architectural decision is introduced; FR-018 documents what those ADRs already decided. |
| DDD + tiered rigour | **Pass** | Core placement logic is treated as core-tier (red-first, typed errors, gate-enforced); documentation and glossary work is glue-tier. |
| ATDD-first / red-first | **Pass** | NFR-003 requires a demonstrably-failing test per behavioural change, verified by reverting the product file. |
| Terminology adherence | **Pass, and extended** | FR-019 extends the canonical glossary rather than inventing vocabulary; NFR-011 forbids new synonyms and applies the rule inward (Domain Language pins the three `Disposition` values). |
| Campsite cleaning | **Pass** | FR-001 fixes two pre-existing gate holes found in the audit; FR-016 corrects stale records. |
| Canonical sources | **Pass** | The classification ledger is extended, not duplicated (C-002); the frozen glossary stores are explicitly excluded (FR-019). |
| Architectural gate discipline | **Pass** | Every gate touched is tightened or has its guarantee transferred, never relaxed: allow-lists shrink, floors move only with recorded before/after (NFR-007), and green-by-omission is forbidden (NFR-005). |

No violations requiring justification → **Complexity Tracking is intentionally empty.**

## Project Structure

### Documentation (this mission)

```text
kitty-specs/read-side-seam-primary-primitive-closure-01KYKMMT/
├── spec.md                # 20 FR / 11 NFR / 9 C / 17 SC / 7 user stories
├── plan.md                # this file
├── research.md            # Phase 0 — decisions already established by the audits
├── data-model.md          # Phase 1 — the layer model + ledger row schema
├── quickstart.md          # Phase 1 — how to verify the mission locally
├── contracts/
│   ├── placement-layering.md      # the layer→owner contract the new page must state
│   ├── ledger-grammar.md          # parse constraints + index discriminator
│   └── gate-extension.md          # census, sanctions, allow-list, floor transfer
└── checklists/requirements.md
```

### Source Code (repository root)

```text
src/mission_runtime/
├── resolution.py          # decision + translation layers; both composition roots
├── artifacts.py           # kind→partition classification (L1)
└── context.py             # routes_through_coordination

src/specify_cli/
├── missions/_read_path_resolver.py   # path constructors (L3); the primitive to privatise
├── status/aggregate.py               # the non-compliant site + the multi-site qualname case
├── cli/commands/agent/mission_setup_plan.py  # the #2886 residual (two reads)
├── acceptance/__init__.py            # the two misleading comments
└── core/paths.py, core/git_ops.py, coordination/surface_resolver.py  # foundation sites (NOT routed)

tests/architectural/
├── test_no_read_side_bypass.py           # read-side census: gains a callee + honest bounds
├── test_resolution_authority_gates.py    # the two use-count floors (retire/re-pin)
├── test_gate_read_literal_ban.py         # three allow-sets to widen (no green-by-omission)
├── test_coord_read_residuals_closeout.py # the #2214 pin + its pin-existence test
└── test_trio_seam_only.py                # blessed-name allow-list shrinks

docs/
├── architecture/artifact-placement-seam.md   # NEW (FR-018)
├── architecture/branch-target-routing.md     # NARROWED to the branch sense (FR-020)
├── architecture/index.md                     # registration (NFR-010)
├── context/orchestration.md                  # Routing disambiguation (FR-019)
├── development/read-side-seam-classification.md  # the machine-parsed ledger
└── development/3-2-page-inventory.yaml, 3-2-docs-retrieval-index.yaml  # regenerated
```

**Structure Decision**: single project, existing layout. No new packages, modules, or
directories beyond one documentation page. All work lands in the surfaces enumerated
above.

## Complexity Tracking

*No Charter Check violations — intentionally empty.*

## Implementation Concern Map

> **Note**: Implementation concerns are NOT work packages and are NOT executable units.
> `/spec-kitty.tasks` translates these into executable WPs — one concern may become
> multiple WPs; multiple small concerns may merge into one WP.

### IC-01 — Close the gate holes before anything moves

- **Purpose**: Make the gates capable of noticing the migration, so nothing later passes by omission.
- **Relevant requirements**: FR-001, NFR-005, SC-004
- **Affected surfaces**: `tests/architectural/test_gate_read_literal_ban.py` (three allow/flag sets: sanctioned read-seam funcs, primary-fold call shapes, the write-side primary anchor); `src/specify_cli/status/aggregate.py:522` (handle from a canonicalizer the fold set does not recognise) or the gate's fold set
- **Sequencing/depends-on**: none — must precede IC-04/IC-05
- **Risks**: Widening a blessing set is a *loosening* unless paired with the bite test that proves it still flags a bad read; the one non-compliant site can be discharged either by routing it or by teaching the gate its canonicalizer — the choice must be recorded, not implicit.

### IC-02 — Ledger parse grammar and per-site index

- **Purpose**: Make the ledger able to carry more than one primitive without parsing silently-empty, and able to address several censused sites inside one function.
- **Relevant requirements**: FR-008, FR-009, NFR-004, SC-006, SC-015, C-009
- **Affected surfaces**: `docs/development/read-side-seam-classification.md` (Summary + stay-lenient index sections); `tests/architectural/test_no_read_side_bypass.py` (the markdown-table reader, the summary-count parser, the index builder and its uniqueness assertion)
- **Sequencing/depends-on**: none — **hard gate before IC-03 and IC-06** (C-009)
- **Risks**: The parse is positional and heading-exact: a sub-table under a parsed heading is silently dropped, a mid-inserted column silently skips rows, and a duplicated verdict key silently overwrites. The prerequisite tests (parsed-row-count equals summed census; per-primitive mutation reds) are what convert this from hope to enforcement. The known four-site qualname is the acceptance fixture.

### IC-03 — Census and classify the unpoliced resolver

- **Purpose**: Establish, per site, what `resolve_feature_dir_for_mission` is doing and which sites are genuinely reading a PRIMARY artifact through a topology-routed resolver.
- **Relevant requirements**: FR-010, FR-011 (classification half), SC-001, SC-016
- **Affected surfaces**: AST census over `src/`; ledger rows; the 8 known sites across 7 files (agent ports, decision CLI, mission-type CLI ×2, context resolver, decisions emit, lanes recovery, widen state)
- **Sequencing/depends-on**: IC-02
- **Risks**: **Vacuity risk** — a zero-fail-loud outcome must be an explicit recorded finding with per-disposition counts, not a silently satisfied requirement (this is how the first spec draft died). Several sites carry production comments asserting the topology-routed answer is required; those become the rationale of record, not a reason to skip classification. Both axes (raise-or-degrade **and** anchoring root) must be recorded — single-axis classification is what let a silent wrong answer through last time.

### IC-04 — Delegate the primary primitive to the seam (Step 1)

- **Purpose**: Prove equivalence in production and surface the one hidden behavioural delta at a single file's cost, with the existing suite as the harness.
- **Relevant requirements**: FR-002, FR-003, NFR-001, NFR-002, NFR-003, SC-003
- **Affected surfaces**: `src/specify_cli/missions/_read_path_resolver.py` (the primitive's body only)
- **Sequencing/depends-on**: IC-01; **hard gate before IC-05** (C-005)
- **Risks**: Call sites are untouched, so the two census floors must **not** move here — if they do, something else changed. Every divergence must be attributed (anchoring / backfill recovery / husk / raising); the accepted one is the seam's bare-slug backfill recovery, which must be pinned rather than absorbed. A latent shape exists at the `.name`-derived site where the recovered answer differs.

### IC-05 — Push the kind to callers and privatise the primitive (Step 2)

- **Purpose**: Move the placement decision into the resolver for every consumer, then make the invariant structural rather than counted.
- **Relevant requirements**: FR-004, FR-005, FR-006, FR-011 (routing half), FR-012, NFR-009, SC-001, SC-002, SC-005, SC-014
- **Affected surfaces**: ~33 consumer sites across ~19 files; `_read_path_resolver.py` (`__all__`, rename to module-private); the named foundation sites (`core/paths.py` ×2, `core/git_ops.py`, `coordination/surface_resolver.py`) which are **recorded, not routed**; `test_no_read_side_bypass.py` (censused callee + per-primitive sanctions)
- **Sequencing/depends-on**: IC-03, IC-04
- **Risks**: Each site needs an individual kind decision — this is the expensive part and the reason C-007 treats it as semantic, not mechanical. Routing a foundation site risks a resolution cycle (`core/paths.py` feeds the write-side composition root). The seam-internal sites under the pinned scan-scope prefix cannot be brought into scope; accountability there is a per-file rationale plus a per-primitive non-vacuity assertion.

### IC-06 — Retire the use-count floors and transfer the guarantee

- **Purpose**: Stop a gate from obliging the primitive to remain in use, and move its teeth to the bypass census where they belong.
- **Relevant requirements**: FR-007, NFR-004, NFR-007, SC-010
- **Affected surfaces**: `tests/architectural/test_resolution_authority_gates.py` (both floors + the allow-list YAML's canonicalizer block); `tests/architectural/test_coord_read_residuals_closeout.py` (the floor-honesty assertions that import them); `tests/architectural/test_trio_seam_only.py` (blessed-name allow-list shrinks); `test_no_read_side_bypass.py` (receives the guarantee)
- **Sequencing/depends-on**: IC-05
- **Risks**: The floors are counted in two files as bare literals, so any move must be edited in both. The doctrine is to record the honest before/after — a shrink driven by routing is precedented (five prior shrinks, one for this exact move) but must be labelled as such, never as a relaxation. Retirement is preferred to re-pinning because after Step 2 the remaining population is resolver-internal, where a raw handle is correct by contract.

### IC-07 — The two coord-awareness residuals

- **Purpose**: Route the documentation-wiring reads and retire the pinned exception honestly.
- **Relevant requirements**: FR-013, FR-014, SC-007
- **Affected surfaces**: `src/specify_cli/cli/commands/agent/mission_setup_plan.py` (**both** reads, plus the audit-metadata write that follows); `tests/architectural/test_coord_read_residuals_closeout.py` (the `#2214` allow-list entry **and** the test asserting that entry exists)
- **Sequencing/depends-on**: none (independent of the migration)
- **Risks**: Routing only one of the two reads clears the pin while leaving the defect — a green-gate honesty hole. Deleting the pin without retiring its pin-existence assertion reds by construction. One downstream write (`gap-analysis.md`) has no artifact kind; it anchors on the resolved directory and is recorded as an honest bound rather than given a kind (adding one is out of scope).

### IC-08 — Correct the record

- **Purpose**: Remove the false and stale claims that manufactured a wrong follow-up issue.
- **Relevant requirements**: FR-015, FR-016, FR-017, SC-008, SC-009
- **Affected surfaces**: `src/specify_cli/acceptance/__init__.py` (two misleading comments); the six husk-conflating comments (`workflow_executor.py` ×3, `next_cmd.py`, `runtime_bridge.py`, `runtime_bridge_identity.py`); `docs/development/read-side-seam-classification.md` (Known-gap text, stale count, drifted line reference); `tests/architectural/test_no_read_side_bypass.py` (docstring count + the "not covered here" claim); `test_coord_read_residuals_closeout.py` (off-by-one recorded census)
- **Sequencing/depends-on**: IC-03 (the bounds enumeration needs the census result)
- **Risks**: The six comments are correct *about a different resolver*; the correction must preserve their true warning (the kind-blind resolver does select the husk) while removing the false implication about the seam. Enumerating bounds requires stating what is **not** covered — silence is the failure mode being fixed.

### IC-09 — Document the seam and disambiguate "routing"

- **Purpose**: Write the layering down once, in the canonical vocabulary, so the next mission cites a design document instead of re-running discovery.
- **Relevant requirements**: FR-018, FR-019, FR-020, NFR-010, NFR-011, SC-012, SC-013, SC-017
- **Affected surfaces**: `docs/architecture/artifact-placement-seam.md` (new); `docs/architecture/branch-target-routing.md` (narrowed to the branch sense); `docs/architecture/index.md`; `docs/context/orchestration.md` (Routing disambiguation extending the existing partition/surface entries); `CLAUDE.md` (Terminology Canon line); `docs/development/3-2-page-inventory.yaml` + `3-2-docs-retrieval-index.yaml` (regenerated)
- **Sequencing/depends-on**: IC-03 and IC-05 — the page must document the layering **as landed**, not as intended
- **Risks**: This concern's failure mode is becoming the fifth authority it exists to replace. Mitigations are in the requirements: the page is explanatory and links to the two ADRs for normative rules; every code-shape claim carries a `module:symbol` citation; the competing page is narrowed in the same slice; the byte-frozen glossary pack and seed are excluded (parity + SHA pins); existing glossary headings that ADRs deep-link must not be reworded. The layer model must be the **verified** one — an earlier draft misdescribed it in two load-bearing ways, and publishing that would have taught the very misappropriation the page prevents.

### Sequencing summary

```text
IC-01 ─┐
       ├─→ IC-04 ─→ IC-05 ─→ IC-06
IC-02 ─┴─→ IC-03 ─┘        └─→ IC-08 ─┐
IC-07 (independent)                   ├─→ IC-09
                            IC-05 ────┘
```

Two hard gates: **IC-02 before any ledger row** (C-009) and **IC-04 before any call-site
rewrite** (C-005).
