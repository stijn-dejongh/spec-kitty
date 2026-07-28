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

**Three** prerequisites gate everything else. (1) The terminal path assembler must be
extracted and the seam's own PRIMARY leg re-pointed at it — the seam *calls* the primitive
through that leg, so delegating without the extraction is an infinite recursion, not a
refactor. (2) The ledger's parse grammar and per-site index must be fixed before any
classification row is written (a naive multi-primitive restructuring was demonstrated to
parse silently-empty). (3) The delegation must land and be verified before any call site is
rewritten — it is the step that surfaces hidden behaviour with the existing suite as
harness, at one file's cost.

The end state is stronger than a rename: the **public wrapper is deleted**, the private
assembler survives, and `_canonicalize_primary_read_handle` — co-drained because the seam
canonicalizes internally — is drained and privatised in the same cycle.

## ⚠ Expected-Red Ledger — the existing suite enforces the structure being removed

Several architectural gates **prescribe** the shape this mission retires: two floors
*count uses of the primitive*, one gate blesses it as the sanctioned read anchor and tells
contributors to route *through* it, one asserts a pin **exists**, and one requires blessed
names to be **currently used**. Their reds are **expected consequences of a correct
migration, not regressions.**

**The single most dangerous failure mode in this mission is an implementer "fixing" the
product to keep a defunct gate green.** Judge every red against the failing-test
remediation framework — *stale → re-pin/retire · scaffold → delete · genuinely valid → fix
the product* — and record which of the three it was (SC-019). **Never retry-to-green.**

26 friction points across **14** files were censused. The nine that change the plan:

| # | Node | Enforces today | On landing | Disposition | Owner |
|---|---|---|---|---|---|
| M1 | `test_resolution_authority_gates.py::test_routed_count_floor` | ≥40 **routed uses of the primitive**, strict `>` | flips at ~the 5th routed site, mid-drain | **STALE → RETIRE** | IC-06 |
| M2 | same `::test_canonicalizer_gate_floor` (44) | ≥44 total uses | drains → fails | **STALE → RETIRE** | IC-06 |
| M3 | `test_coord_read_residuals_closeout.py` floor **import** + two `==` pins | hard equality on both floors | deleting the constants → **`ImportError` at collection → the whole ~780-line module errors (~20 tests)** | **STALE → retire with M1/M2** | IC-06 |
| M4 | `test_single_mission_surface_resolver.py` import-time `ContentDescriptor` | the primitive's body still holds that exact raw join under that exact qualname | **collection ERROR for ~30 tests**, twice (body change **and** rename) | **STALE → re-author the descriptor onto the new leaf** | IC-00/IC-05 |
| M5 | `test_trio_seam_only.py::test_allowed_read_path_resolver_names_are_currently_used` | the primitive **and** `_canonicalize_primary_read_handle` are *currently imported* by a trio file | both go unused → fails, with the fix in its own message | **STALE → shrink the blessed set (both names)** | IC-05 (trio WP) |
| M6 | same file, after the shrink | — | set reduces to one name which a later line **subtracts** → the gate goes **vacuously green** | **VALID → FIX THE GATE** (positive assertion) | IC-06 |
| M7 | `test_gate_read_literal_ban.py::_PRIMARY_FOLD_CALLSHAPE_FUNCS` | the fold names are the sanctioned first-arg source | widening it by **callee name** is kind-blind → sanctions `STATUS_STATE` reads too, and propagates cross-file into the closeout's NFR-001 check as a **false regression** | **VALID → FIX THE GATE: discriminate on the `kind` argument** | IC-01 |
| M8 | same file `::test_write_arm_resolvers_anchor_meta_on_primary` | *claims* meta must anchor on the primitive — but **discards `reads_via_primary`** and only asserts the negative | routing stays green **by omission**; the rename also makes the anchor literal match nothing | **VALID → FIX THE GATE: assert the positive** | IC-01 |
| M16 | *product, not test:* `read_dir → resolve_artifact_surface → resolve_planning_read_dir →` the primitive | the seam's PRIMARY leg **calls** the primitive | delegating without extracting first is an **infinite recursion** | **PLAN CHANGE → IC-00** | IC-00 |

Also unowned before this revision, now assigned: `resolve_feature_dir_for_mission` in
`__all__` goes dead once its 5 importers route (M14 → IC-05); the `agent/tasks.py`
re-export that exists **only** to serve a test patch seam (M15 → **SCAFFOLD, delete it**,
do not preserve it to keep tests green); the second census under
`tests/architectural/surface_resolution_audit/` (N17/N18 → IC-05, hand-edit only — the
rekey script is not round-trip-safe, #3011); gate-coverage baselines when node-ids are
deleted (N25 → IC-06).

### Patch-seam exposure — 20 in-scope seams / 13 files (2.5× the predecessor's 8)

- **Class A — module-local bindings** (6 seams / 5 files): die with `AttributeError` the moment a consumer stops importing the name. Includes the `agent/tasks.py` seam and a test whose entire subject is the old shape → **delete, don't repair**.
- **Class B — resolver-module bindings** (10 seams / 7 files): die on the rename/delete.
- **Class C — the dangerous one**: a module-wide fixture stubs four resolver names *because* the PRIMARY leg calls them internally. IC-00's extraction makes those stubs **unreached** → the convergence harness may go **vacuously green**. Hand-verify it as part of IC-00/IC-04's attribution list.
- 43 test files reference the primitive by name (imports, calls, assertions); the rename touches every one.

### Load-bearing vs bookkeeping — nothing on the right justifies a product change

| **LOAD-BEARING — you broke something** | **BOOKKEEPING — the gate encoded the old shape** |
|---|---|
| a resolved directory changed for a materialized, non-backfilled mission (NFR-001) | M1/M2/M3 floors and their equality pins |
| a PRIMARY kind **raising** on husk / empty / deleted coord (NFR-002) | M4 descriptor collection error |
| the husk-proof and no-STATUS-reroute nodes — **unless** the red is M7's false positive | M5 blessed-name staleness |
| a newly censused offender that is genuinely an unrouted read | M9 the `#2214` pin / pin-existence pair |
| ledger parse reds (the ledger really is mis-parsing) | M14 `__all__` membership |
| an allow-list entry failing for a site you did **not** touch | stale inventory rows, stale counts, baselines |
| **`RecursionError` after delegation** — real, highest-priority stop | Class A/B patch-seam `AttributeError`s |
| **M6/M8 going *green* while covering nothing** (silent) | — |

Two traps to spell out to implementers: a red in the no-STATUS-reroute check may be a
**gate** defect (M7), not an NFR-001 regression — check whether the offending dir came from
a STATUS-kind read before touching product; and M6/M8 are reds that *never fire* — they
need positive assertions, not a fix-until-green loop.


## Technical Context

**Language/Version**: Python 3.11+ (repository standard; `pyproject.toml` `requires-python`)
**Primary Dependencies**: no new runtime dependencies. Internal surfaces only — `mission_runtime` (placement seam: `resolution.py`, `artifacts.py`, `context.py`), `specify_cli.missions._read_path_resolver` (path constructors), and the architectural gate suite under `tests/architectural/`
**Storage**: filesystem + git only (mission artifacts under `kitty-specs/<mission>/`; no database)
**Testing**: `pytest` with targeted node-ids (C-008 — the exhaustive `tests/architectural/` sweep is CI's responsibility, never local); `uv run pytest` / `uv run mypy` inside lane worktrees; AST-based architectural gates as the enforcement mechanism; red-first evidence per behavioural change (NFR-003). **Four gates prescribe the retired shape — see the Expected-Red Ledger. Two failures present as module-level *collection errors*, not assertion failures** (an import-time content descriptor, and a floor import), so they read as collateral damage unless anticipated
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

### IC-00 — Extract the terminal assembler (tidy-first; makes delegation possible)

- **Purpose**: Split the pure `KITTY_SPECS_DIR` assembly out of the primitive into a module-private leaf and re-point the seam's own PRIMARY leg plus the resolver-internal callers at it, so the primitive can later delegate without recursing.
- **Relevant requirements**: FR-021, NFR-001, NFR-009, SC-018
- **Affected surfaces**: `src/specify_cli/missions/_read_path_resolver.py` (extract + repoint its internal callers), `src/mission_runtime/resolution.py` (4 internal callers + the PRIMARY leg), `tests/architectural/test_single_mission_surface_resolver.py` (the import-time content descriptor must be re-authored onto the new leaf **in the same commit**, or ~30 tests fail at collection), `tests/specify_cli/missions/test_read_path_resolver_validation.py`
- **Sequencing/depends-on**: none — **hard gate before IC-04** (C-005 Step 0)
- **Risks**: Behaviour must be identical with **zero** call-site changes. The Class-C patch fixture stubs four resolver names *because* the PRIMARY leg calls them internally; re-pointing that leg makes the stubs unreached, so the fixture may go red **or vacuously green** — hand-verify it here rather than discovering it later. A negative patch elsewhere asserts a specific kind never routes through the planning resolver; confirm the extraction does not trip it.

### IC-01 — Close the gate holes before anything moves

- **Purpose**: Make the gates capable of noticing the migration, so nothing later passes by omission.
- **Relevant requirements**: FR-001, NFR-005, SC-004
- **Affected surfaces**: `tests/architectural/test_gate_read_literal_ban.py` (three allow/flag sets: sanctioned read-seam funcs, primary-fold call shapes, the write-side primary anchor); `src/specify_cli/status/aggregate.py:522` (handle from a canonicalizer the fold set does not recognise) or the gate's fold set
- **Sequencing/depends-on**: none — **must precede IC-04, IC-05 and IC-07**
- **Two gate defects to fix here, not merely widen** (Expected-Red Ledger M7/M8):
  - the fold-set widening MUST **discriminate on the `kind` argument** (PRIMARY kinds only). Widening by callee name would sanction `STATUS_STATE` reads through the same seam call — a genuine loosening — and propagates cross-file into the closeout module's no-STATUS-reroute check, producing a **false NFR-001 regression** that invites an implementer to "fix" a correct STATUS leg.
  - the write-arm node **discards its positive signal** and asserts only the negative, so a routed site passes **by omission**; it must assert the positive (or its seam equivalent) and track the post-migration spelling.
- **Risks**: Widening a blessing set is a *loosening* unless paired with a bite test proving it still flags a bad read (NFR-005). The one non-compliant production site is discharged in the WP that routes its module (its three sibling sites live in the same function), while the gate-side fold-set recognition stays here. **Downstream consumers of this IC's constants live in the closeout module** — that is why IC-07 depends on this IC, not only IC-05.

### IC-02 — Ledger parse grammar and per-site index

- **Purpose**: Make the ledger able to carry more than one primitive without parsing silently-empty, and able to address several censused sites inside one function.
- **Relevant requirements**: FR-008, FR-009, NFR-004, SC-006, SC-015, C-009
- **Affected surfaces**: `docs/development/read-side-seam-classification.md` (Summary + stay-lenient index sections); `tests/architectural/test_no_read_side_bypass.py` (the markdown-table reader, the summary-count parser, the index builder and its uniqueness assertion)
- **Sequencing/depends-on**: none — **hard gate before IC-03, IC-05 and IC-06** (C-009). This IC's WP is the **sole owner** of both the ledger and the read-side gate module for the whole mission, and should land their **terminal** shape up front (grammar + index + the full censused-callee set + sanctions + honest bounds) so later WPs only *satisfy* those gates and never edit them.
- **Provision for four callees, not two**: the censused set grows from 2 to **4** (the newly policed kind-blind resolver, plus the primary primitive receiving the retired floors' transferred guarantee). A grammar built for two or three under-provisions.
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
- **Affected surfaces**: `src/specify_cli/missions/_read_path_resolver.py` (the **public wrapper's** body only — the assembler extracted in IC-00 stays untouched), plus the Class-C patch fixture and the equivalence/behavioural suites named in IC-00
- **Sequencing/depends-on**: **IC-00** (without the extraction this recurses) and IC-01; **hard gate before IC-05** (C-005 Step 1)
- **Risks**: Call sites are untouched, so the two census floors must **not** move here — if they do, something else changed. Every divergence must be attributed (anchoring / backfill recovery / husk / raising); the accepted one is the seam's bare-slug backfill recovery, which must be pinned rather than absorbed. A latent shape exists at the `.name`-derived site where the recovered answer differs.

### IC-05 — Push the kind to callers and privatise the primitive (Step 2)

- **Purpose**: Move the placement decision into the resolver for every consumer, then make the invariant structural rather than counted.
- **Relevant requirements**: FR-004, FR-005, FR-006, FR-011 (routing half), FR-012, NFR-009, SC-001, SC-002, SC-005, SC-014
- **Affected surfaces**: ~30 routable consumer sites; `_read_path_resolver.py` (**delete the public wrapper** + drop both drained names from `__all__`); `_canonicalize_primary_read_handle` (co-drained — 86 references / 22 files — drained and privatised in this cycle per FR-022); the named foundation sites (`core/paths.py` ×2, `core/git_ops.py`, `coordination/surface_resolver.py`) **recorded, not routed**; the `agent/tasks.py` re-export that exists **only** to serve a test patch seam (**delete it and rewrite the two tests against the real seam** — do not preserve it to keep tests green); `tests/architectural/surface_resolution_audit/` (second census — **hand-edit `inventory.md`; do NOT run the rekey script, it is not round-trip-safe, #3011**); the ~11 test modules importing the drained names
- **Slicing axis (non-negotiable)**: **trio-membership first, then directory.** The trio gate asserts its blessed names are *currently used* by 8 specific files, 4 of which are rewrite targets — a directory split scatters them across three WPs and the blessed-name shrink would only be safe after the third lands. One WP must own all 8 trio files **and** the trio gate. Recommended: trio (10 sites) · agent-CLI non-trio (5) · CLI-commands + core/misc (15).
- **Sequencing/depends-on**: IC-03, IC-04
- **Risks**: Each site needs an individual kind decision — this is the expensive part and the reason C-007 treats it as semantic, not mechanical. Routing a foundation site risks a resolution cycle (`core/paths.py` feeds the write-side composition root). The seam-internal sites under the pinned scan-scope prefix cannot be brought into scope; accountability there is a per-file rationale plus a per-primitive non-vacuity assertion.

### IC-06 — Retire the use-count floors and transfer the guarantee

- **Purpose**: Stop a gate from obliging the primitive to remain in use, and move its teeth to the bypass census where they belong.
- **Relevant requirements**: FR-007, NFR-004, NFR-007, SC-010
- **Affected surfaces**: `tests/architectural/test_resolution_authority_gates.py` (both floors + the allow-list YAML's canonicalizer block); `tests/architectural/test_coord_read_residuals_closeout.py` (the floor-honesty assertions that import them); `tests/architectural/test_trio_seam_only.py` (blessed-name allow-list shrinks); `test_no_read_side_bypass.py` (receives the guarantee)
- **Sequencing/depends-on**: IC-02 (grammar) and IC-07 (the closeout file's pin must already be gone — this IC is that file's **sole owner**). ⚠ **The floor retirement itself must land at the START of the call-site migration, not after it**: the routed-count bound is strict, so it breaks around the fifth routed site while the census is still moving.
- **Also fix here, do not merely shrink** (Ledger M6): after the blessed-set shrink the trio gate reduces to a single name that a later line **subtracts**, leaving it **vacuously green**. Replace the exemption with a positive assertion so the gate the mission tightens does not silently die.
- **Risks**: The floor values are an **import plus two equality pins** across two modules — not "bare literals". Deleting the constants without retiring their consumer produces an `ImportError` at collection that errors ~20 tests, which reads as collateral damage. Retiring node-ids also drifts the gate-coverage baselines, which must be refrozen with provenance. The doctrine is to record the honest before/after — a shrink driven by routing is precedented (five prior shrinks, one for this exact move) but must be labelled as such, never as a relaxation. Retirement is preferred to re-pinning because after Step 2 the remaining population is resolver-internal, where a raw handle is correct by contract.

### IC-07 — The two coord-awareness residuals

- **Purpose**: Route the documentation-wiring reads and retire the pinned exception honestly.
- **Relevant requirements**: FR-013, FR-014, SC-007
- **Affected surfaces**: `src/specify_cli/cli/commands/agent/mission_setup_plan.py` (**both** reads, plus the audit-metadata write that follows); `tests/architectural/test_coord_read_residuals_closeout.py` (the `#2214` allow-list entry **and** the test asserting that entry exists)
- **Sequencing/depends-on**: **IC-01** — this IC is *not* independent: the closeout module scans call shapes live against IC-01's sanctioned set, so routing these reads before that set knows the seam idiom flags the newly-routed site. Sequenced **before** IC-06, which owns the closeout file.
- **Ownership note**: this IC does **not** edit the closeout module. Its pin removal is an inbound line item on IC-06's WP (single-owner rule).
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
IC-00 (extract) ──┐
IC-01 (gates)  ───┼──> IC-04 (delegate) ──> IC-05 (route · trio-first · delete wrapper) ──┐
IC-02 (grammar) ──┴──> IC-03 (classify) ──────────────────────────────────────────────────┤
IC-01 ──> IC-07 (residuals) ──> IC-06 (floors retired at START of IC-05; owns closeout) ───┤
                                                                     IC-08 (record) ──────┼──> IC-09 (docs)
```

**Three hard gates**: IC-00 before IC-04 (else recursion), IC-02 before any ledger row
(C-009), IC-04 before any call-site rewrite (C-005).

### Single-owner assignments (cross-WP coordination debt is the predecessor's known failure)

| File touched by several ICs | Sole owner | Inbound edits from |
|---|---|---|
| `docs/development/read-side-seam-classification.md` | IC-02's WP | IC-03 rows, IC-08 prose |
| `tests/architectural/test_no_read_side_bypass.py` | IC-02's WP | IC-05/IC-06 censused-callee + sanctions, IC-08 docstring count |
| `tests/architectural/test_coord_read_residuals_closeout.py` | IC-06's WP | IC-07 pin removal, IC-08 recorded census |
| `src/specify_cli/missions/_read_path_resolver.py` | serial, by phase | IC-00 extract → IC-04 wrapper body → IC-05 delete + `__all__` |
| `tests/architectural/test_trio_seam_only.py` | the trio WP of IC-05 | — |

**Rule for `/spec-kitty.tasks`**: an enforcement retirement is owned by the WP whose diff
makes it defunct — never by a downstream "bookkeeping" WP. **Per-WP acceptance = the full
C-008 local gate list** (read-side census, closeout, anchoring floors, fold-prescription,
trio-seam, write-side), not just the WP's own suites — that is how the trio and closeout
reds would otherwise escape to the aggregate.

### Tracker rows for the issue matrix

| Issue | Action |
|---|---|
| #2886 | **Closes** — the residuals IC |
| #3014 | **Close with the corrected finding** (the issue that manufactured this mission; assign an owner — the record-correction IC) |
| #2465 | **Partial** — no closing keyword; comment progress, or scope-check whether the trio WP can consolidate all four resolvers in that file |
| #2707 | **Verify first** — may already be fixed and stale; if live it is one more read in the residuals IC's own file |
| #3011 | Reference as a hazard (do not run the rekey script) |
| #2653 | Cross-reference only — shares the Terminology Canon surface with IC-09 |
