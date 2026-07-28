# Mission Specification: Read-Side Seam: Honest Census and Kind-Blind Resolver Closure

**Mission Branch**: `fix/read-side-seam-primary-primitive-closure`
**Created**: 2026-07-28 · **Re-framed**: 2026-07-28 after a two-lens post-spec squad falsified the original premise (see Provenance)
**Status**: Draft
**Input**: Close the residuals left by #3013 — #2886 (route `_run_documentation_wiring`, retire the `PINNED: #2214` exception) and the #2824 residual (correct two actively-wrong comments) — and discharge #3014 **honestly**: correct the false and stale claims it rests on, and police the resolver that is genuinely unpoliced (`resolve_feature_dir_for_mission`) instead of the one #3014 mis-identified.

> **Note on the mission slug.** The slug `…-primary-primitive-closure-01KYKMMT` is historical: it was minted before the squad disproved #3014's premise. The mission's actual subject is the **kind-blind** resolver `resolve_feature_dir_for_mission` plus census honesty; `primary_feature_dir_for_mission` is deliberately **out of scope** (C-004). The slug is immutable identity and is not renamed.

## Context & Motivation

Mission artifacts live on one of two partitions: **PRIMARY** (stable planning and
metadata — `meta.json`, `spec.md`, `tasks/`) or **COORD** (lifecycle surfaces on a
coordination branch). The **placement seam** is the single authority that maps a
`MissionArtifactKind` to the right partition and fails loud when a COORD partition
is gone.

PR #3012 routed 72 read sites onto that seam and added an AST census gate
(`tests/architectural/test_no_read_side_bypass.py`) over **two** kind-blind
primitives, backed by a machine-parsed ledger
(`docs/development/read-side-seam-classification.md`). Its landing pass had to
repair two failures that this mission must not repeat: a **vacuous** ledger
reconciliation (two literals compared inside one test file) and **single-axis**
classification that let a silent wrong answer through.

Issue #3014 asserted that a third primitive, `primary_feature_dir_for_mission`, is
"policed by nothing" and needs ~39 sites migrated to fail loud. **A two-lens
post-spec squad disproved that**, and this spec is written to the corrected facts:

1. **It is already policed.** `tests/architectural/test_resolution_authority_gates.py`
   censuses exactly this primitive on the **anchoring axis**
   (`CANONICALIZER_PRIMITIVE`, `CANONICALIZER_FLOOR = 44`,
   `ROUTED_CANONICALIZER_FLOOR = 40`, plus a rationale-bearing allow-list YAML with
   shrink-only and stale-entry tests). Live: 46 scanned / 43 routed / 3 sanctioned.
   A raw-handle call reds today.
2. **Its fail-loud surface is zero.** All 34 in-scope sites read a PRIMARY-partition
   artifact off a deliberately PRIMARY anchor, and six carry explicit comments
   stating that the topology-routed resolver would be *wrong* (it lands on the
   STATUS-only coord husk, which has no `meta.json`). `read_dir()` only raises for a
   COORD kind, so "migrate these to fail loud" is vacuous.
3. **Migrating them would break two gates.** Routing ~30 sites drops the routed
   count 43 → ~13, reding `test_canonicalizer_gate_floor`, `test_routed_count_floor`,
   and the closeout gate's floor-honesty assertion — for no safety gain.
4. **The real gap is a different resolver.** `resolve_feature_dir_for_mission`
   (`src/specify_cli/missions/_read_path_resolver.py:1581`) is the same **kind-blind**
   shape, exported in `__all__`, with **8 live sites / 7 files** — and is covered by
   **no** census gate and **no** ledger row. Because it is kind-blind *and*
   topology-routed, a caller reading a PRIMARY artifact through it can land on the
   coord husk: precisely the failure those six comments describe.

So the honest work is: close the two residuals, **correct the record** (the ledger's
"unpoliced" text, a stale count that appears in two places, and an off-by-one
census), and **police the resolver that nobody polices** — with the ledger
grammar and index grammar fixed first, because the squad demonstrated that the
naive extension parses **silently vacuously**.

### Two-axis classification *(load-bearing)*

#3012's ledger assessed only the **exception axis** ("can this kind raise?") and
never the **anchoring axis** ("which root does it resolve against, and is the result
idempotent under a composed vs bare handle?"). That blind spot produced a silent
wrong answer on a backfilled mission. Every site classified here records both.

### Gate honesty *(load-bearing)*

A gate must enforce what it advertises. The squad **executed** the extension shape
this spec originally prescribed and showed the reconciliation stays *green and
meaningless*; and it found the index grammar cannot even represent a module with
several censused sites in one function. Both are fixed before any site is
classified.

## Domain Language *(load-bearing)*

| Term | Canonical sense in this mission | Do NOT confuse with |
|------|--------------------------------|---------------------|
| **PRIMARY partition** | Stable planning/metadata home (`meta.json`, `spec.md`, `tasks/`). | The Primary Branch (`main`). |
| **COORD partition** | Lifecycle surfaces routed via the coordination branch. A coord worktree may be a **husk**: present but carrying no `meta.json`. | The PRIMARY partition. |
| **Kind-blind resolver** | Maps (root, handle) → directory with **no** `MissionArtifactKind`, so it cannot distinguish per-artifact partitions: `candidate_feature_dir_for_mission`, `resolve_planning_read_dir`, and — this mission's subject — `resolve_feature_dir_for_mission`. | "Topology-blind". The two are different axes: `resolve_feature_dir_for_mission` is kind-blind but topology-**routed**, which is exactly why it can land on the husk. |
| **Partition-aware authority** | `placement_seam(...).read_dir(kind)` / `resolve_artifact_surface`. | "Coord-aware". For a `meta.json` read the correct target is the **PRIMARY** anchor; the authority is partition-aware, not coord-preferring. |
| **Anchoring axis** | Which root the resolution is computed against, and whether the answer is idempotent under composed (`<slug>-<mid8>`) vs bare (`<slug>`) handles. | The exception axis (can it raise). |
| **Census** | AST-derived `ast.Call` sites of a named callee, aliases resolved. | A grep count (over-counts prose, misses aliases and wrapper laundering). |
| **Honest bound** | A named, sized limit of what a gate enforces, recorded where the gate advertises itself. | Silence. Silence is what made #3014 wrong. |

## User Scenarios & Testing *(mandatory)*

Primary actor: the **maintainer/agent** running mission lifecycle commands, plus
**future contributors** adding read sites and **future planners** reading the
tracker and the ledger to decide what is already done.

### User Story 1 - A PRIMARY artifact is never read off the coord husk (Priority: P1)

A maintainer runs a lifecycle command on a coord-topology mission whose coordination
worktree exists but is a husk (no `meta.json`). A caller that reaches
`resolve_feature_dir_for_mission` — kind-blind but topology-routed — can be handed
that husk and read a PRIMARY artifact from it, getting a wrong or missing answer with
no partition error. After this mission, every such site that genuinely reads a
PRIMARY artifact resolves through the partition-aware authority instead, and the
sites that deliberately want the topology-routed answer are recorded as such.

**Why this priority**: This is a live silent-wrong-read path in a resolver no gate
covers — the same bug class the programme exists to remove, on the primitive that
was actually missed.

**Independent Test**: Drive a site classified fail-loud on a mission whose coord
worktree is a materialized husk; assert it resolves the PRIMARY anchor (or raises)
rather than silently returning the husk. Assert a site classified deliberate-routed
is unchanged.

**Acceptance Scenarios**:

1. **Given** a coord-topology mission whose coord worktree is a husk with no `meta.json`, **When** a fail-loud-classified site reads its PRIMARY artifact, **Then** it resolves the PRIMARY anchor and does not return the husk.
2. **Given** a site whose production comment documents that the topology-routed answer is required, **When** the mission completes, **Then** its behaviour is unchanged and its rationale is recorded in the ledger.
3. **Given** a mission whose PRIMARY dir is the bare `<slug>` form while its COORD dir is composed `<slug>-<mid8>`, **When** a migrated site resolves either handle form, **Then** the answer is correct and idempotent under the seam's own output.
4. **Given** a flat / coord-less (`SINGLE_BRANCH` / `LANES`) mission, **When** any migrated site runs, **Then** behaviour is identical to before (no new raise).

---

### User Story 2 - A new kind-blind read cannot be introduced silently (Priority: P1)

A future contributor adds a call to `resolve_feature_dir_for_mission`. Today nothing
objects. After this mission the read-side gate reds, names the site, and forces
either routing or an individually-rationalised allow-list entry.

**Why this priority**: Enforcement is what converts a cleanup into a durable
invariant; without it the resolver family decays one caller at a time, which is why
#3012 was needed.

**Independent Test**: Plant a direct call in a non-sanctioned module → gate reds;
plant it via an **aliased** import → still reds; a prose mention → green; stale
allow-list entry → reds until deleted.

**Acceptance Scenarios**:

1. **Given** a planted direct call in a non-sanctioned `src/` module, **When** the read-side gate runs, **Then** it fails naming file and symbol.
2. **Given** the primitive imported under an alias and called, **When** the gate runs, **Then** it still fails.
3. **Given** only a comment or docstring mention, **When** the gate runs, **Then** it passes.
4. **Given** an allow-list entry whose site has been routed or deleted, **When** the gate runs, **Then** the staleness twin-guard reds until the entry is removed.
5. **Given** a sanctioned module, **When** the non-vacuity meta-test runs, **Then** it proves that module carries a real finding **for this primitive specifically** (not merely for a previously-censused one).

---

### User Story 3 - The ledger is a machine-checked authority that cannot go vacuous (Priority: P1)

A maintainer must be able to trust "the allow-list matches the ledger" as a fact.
The gate parses the ledger, and the parse cannot silently drop a primitive's rows.

**Why this priority**: The squad executed the originally-specified extension and
showed the second primitive's rows vanish while the reconciliation stays green — the
exact vacuity #3012's landing pass had to repair. Fixing the grammar is a
prerequisite for classifying anything, not a finishing touch.

**Independent Test**: Mutate a row belonging to **each** primitive in a scratch copy → the gate must red for each. Assert the parsed row count equals the sum of the per-primitive censuses.

**Acceptance Scenarios**:

1. **Given** a ledger row mutated for primitive *N*, **When** the gate runs, **Then** it reds — for every *N*, not just the first.
2. **Given** the ledger's machine-parsed sections, **When** the gate parses them, **Then** the parsed row count equals the summed per-primitive census; a dropped table or column-shift reds loudly rather than parsing empty.
3. **Given** a module with several censused sites inside one function, **When** its rows are recorded, **Then** the index grammar addresses each site distinctly and the uniqueness assertion holds.

---

### User Story 4 - The two coord-awareness residuals are closed and their exceptions retired (Priority: P2)

`_run_documentation_wiring`'s metadata reads — **both** of them — resolve through the
partition-aware authority, its subsequent audit-metadata write stays coherent, and
the `PINNED: #2214` exception plus the test that asserts that pin exists are retired
together. The two misleading comments in `acceptance/__init__.py` are corrected.

**Why this priority**: Each is small but each is a live trap: routing only one of the
two reads clears the pin while leaving the bug (a green-gate honesty hole), and the
comments would lead a maintainer to move `lanes.json` onto the wrong partition.

**Independent Test**: Route both reads; delete the pin **and** retire the
pin-existence assertion; confirm the closeout gate's clean-scan stays green and its
site floor still provides non-vacuity.

**Acceptance Scenarios**:

1. **Given** both reads in `_run_documentation_wiring` routed, **When** the `PINNED: #2214` entry and the pin-existence test are removed together, **Then** the closeout gate's unexpected/stale-pin scan is green and non-vacuity rests on the documented site floor.
2. **Given** the audit-metadata write that follows the read, **When** it runs, **Then** the `meta.json` write resolves through the same PRIMARY authority as the read; the `gap-analysis.md` write (which has **no** `MissionArtifactKind`) anchors on that same resolved directory and is recorded as an honest bound rather than a kind claim.
3. **Given** the corrected comments, **When** a maintainer reads them, **Then** they state that `lanes.json` is a PRIMARY artifact, that only the acceptance-matrix read is placement-resolved, and they no longer claim the shared variable is coord-resolved.

---

### User Story 5 - The record no longer misleads a planner (Priority: P2)

A planner reading the ledger, the gate docstring, or the tracker gets facts: which
primitives are policed by which gate and on which axis, the real site counts, and a
complete, sized list of what remains uncovered.

**Why this priority**: #3014 was filed *because* the record said "tracked follow-up"
without saying by whom or on what axis — and it then asserted "policed by nothing",
which was false. A wrong record manufactures wrong missions.

**Independent Test**: Read the corrected ledger + gate docstring; every count matches
a fresh census, every "unpoliced" claim names the gate that does cover it, and every
residual gap is named with its size.

**Acceptance Scenarios**:

1. **Given** the ledger's Known-gap section, **When** read after this mission, **Then** it states that `primary_feature_dir_for_mission` is censused on the anchoring axis by `test_resolution_authority_gates.py`, that its fail-loud surface is zero, and why read-gate inclusion is deliberately declined.
2. **Given** any site count in the ledger or the gate docstring, **When** compared to a fresh census, **Then** they agree (the stale "40" is corrected in **both** places, and the closeout gate's off-by-one recorded census is corrected).
3. **Given** the enumerated honest bounds, **When** compared to the live tree, **Then** they include the wrong-`kind` class, wrapper laundering, the zero-site latent sibling, the blanket-excluded seam-internal sites, and `resolve_feature_dir_for_slug` — with sizes.

---

### Edge Cases

- **Coord husk** (worktree present, `meta.json` absent) — the shape six production comments already warn about; the primary failure mode for a kind-blind topology-routed read.
- **Backfilled missions** (bare `<slug>` PRIMARY vs composed `<slug>-<mid8>` COORD) — resolution must be idempotent under the seam's own output.
- **Multiple censused sites in one function** — e.g. `status/aggregate.py::MissionStatus._find_meta_path` carries four; the ledger index must address each.
- **Wrapper laundering** — `resolve_subtasks_gate_dir` wraps a censused primitive with a pinned kind; its callers are invisible to a callee-name census.
- **Aliased / re-exported imports** — must not defeat the census.
- **Wrong-`kind` argument** to an already-routed `read_dir()` — census-invisible by construction (this was #2824's actual defect); must be named as a bound, not implied covered.
- **Blanket-excluded seam internals** — sites under the pinned scan-scope prefix cannot be brought into scope; accountability is a per-file rationale entry plus a per-primitive non-vacuity assertion.
- **Artifacts with no kind** — `gap-analysis.md` has no `MissionArtifactKind`; the seam cannot route it, and adding a kind is out of scope.
- **Flat / coord-less topologies** — must see no behaviour change.
- **Census drift** — counts are re-derived on this mission's base, never trusted from issue text.

## Requirements *(mandatory)*

### Functional Requirements

| ID | Title | User Story | Priority | Status |
|----|-------|------------|----------|--------|
| FR-001 | Route both `_run_documentation_wiring` reads | As a maintainer, I want **both** metadata reads in `_run_documentation_wiring` (the mission-type read and the `meta.json` path it derives) resolved through the partition-aware PRIMARY authority, so routing one does not leave the other reading off a coord-bound directory. | High | Open |
| FR-002 | Retire the `#2214` pin and its pin-existence test together | As a maintainer, I want the `PINNED: #2214` allow-list entry **and** the named test asserting that pin exists retired in the same change, so the gate does not red by construction and non-vacuity falls back to its documented site floor. | High | Open |
| FR-003 | Correct both misleading comments | As a maintainer, I want both stale comments in `acceptance/__init__.py` corrected — the T028 comment and the earlier claim that the shared read directory is coord-resolved — so no reader concludes `lanes.json` should move to COORD. | Medium | Open |
| FR-004 | Fix the ledger's machine-parse grammar first | As a maintainer, I want the ledger's parsed sections constrained (exactly one table per parsed heading, verbatim headings, verdict/path/qualname at fixed leading column positions, any primitive discriminator appended as a trailing column) **before** any rows are added, so a multi-primitive ledger cannot parse silently-empty. | High | Open |
| FR-005 | Give the index grammar a per-site discriminator | As a maintainer, I want the stay-lenient index able to address several censused sites inside one qualname (discriminator column or composite key) with its uniqueness assertion updated in the same change, so a module like `status/aggregate.py::_find_meta_path` is representable. | High | Open |
| FR-006 | Census the genuinely unpoliced resolver | As a maintainer, I want an AST census (aliases resolved, definition module excluded) of `resolve_feature_dir_for_mission` on this mission's base, so its sites are known rather than estimated. | High | Open |
| FR-007 | Classify each site on both axes | As a maintainer, I want every censused site classified with its disposition **and** both axes recorded — raise-or-degrade, anchoring root (verbatim root argument plus its semantic class with a provenance citation), handle form, target kind, and idempotence under the seam's output — so no site is migrated on a one-axis assessment. | High | Open |
| FR-008 | Route the genuinely PRIMARY-artifact reads | As a maintainer, I want each site that reads a PRIMARY artifact through the topology-routed resolver routed onto the partition-aware authority with the correct kind, so it can no longer be handed a coord husk. | High | Open |
| FR-009 | Preserve and justify the deliberate sites | As a maintainer, I want each site that genuinely requires the topology-routed answer left unchanged and recorded as a rationale-bearing allow-list entry (reusing its existing production comment as the rationale of record), so intent is captured rather than re-derived. | High | Open |
| FR-010 | Police the resolver in the read-side gate | As a maintainer, I want `resolve_feature_dir_for_mission` added to the read-side gate's censused callees, with its sanctioned modules asserted **per primitive** and its residuals allow-listed shrink-only under the staleness twin-guard. | High | Open |
| FR-011 | Correct the false and stale record | As a maintainer, I want the ledger's Known-gap text to name `test_resolution_authority_gates.py` as the anchoring-axis authority for `primary_feature_dir_for_mission` (replacing the "policed by nothing" framing), the stale site count corrected in **both** the ledger and the gate docstring, the closeout gate's off-by-one recorded census fixed, and the ledger's drifted definition line reference updated. | High | Open |
| FR-012 | Enumerate the honest bounds | As a maintainer, I want the gate's advertised bounds to name, with sizes, everything it does **not** cover: the wrong-`kind` class, wrapper laundering, the zero-site latent sibling resolver, the blanket-excluded seam-internal sites, and the deliberate exclusion of `primary_feature_dir_for_mission` with its rationale — so no future planner repeats #3014. | High | Open |

### Non-Functional Requirements

| ID | Title | Requirement | Category | Priority | Status |
|----|-------|-------------|----------|----------|--------|
| NFR-001 | Behaviour-preserving except one named delta | For every routed site the resolved directory in the materialized, non-backfilled case is identical to the pre-change result. The **one** permitted delta is the seam's bare-`<slug>` backfill recovery; it is named per site in the ledger and pinned by a test. | Reliability | High | Open |
| NFR-002 | No new raises where leniency is the contract | Zero sites classified deliberate/lenient, and zero flat or coord-less executions, begin raising as a result of this mission. | Reliability | High | Open |
| NFR-003 | Red-first evidence per behavioural change | Every behavioural change ships a test demonstrably failing before and passing after (verified by reverting the product file), including the coord-husk case and the composed-vs-bare handle case. | Safety | High | Open |
| NFR-004 | Gate bite, per-primitive non-vacuity, authority parse | The extended gate reds on a planted direct call and on an aliased call; stays green on prose; reds when a parsed ledger row disagrees **for each primitive independently**; reds on a stale allow-list entry; proves each sanctioned module carries a real finding **for this primitive**; and asserts parsed row count equals the summed per-primitive census. | Safety | High | Open |
| NFR-005 | Single scanner authority | The read-side gate keeps consuming the shared whole-tree scan scope (no forked walk); the write-side gate stays green. | Maintainability | High | Open |
| NFR-006 | Census reconciliation, correctly scoped | Reconciliation covers the **live residual/lenient** totals per primitive (the figures the gate parses), not the historical pre-migration totals, which are preserved as an audit record and labelled as such. Every count that is claimed is re-derived on this base. | Maintainability | High | Open |
| NFR-007 | No collateral floor breakage | The mission introduces no change that reds `test_resolution_authority_gates.py` or the closeout gate's floor-honesty assertions; if any floor is touched, the before/after integers are recorded honestly rather than relaxed. | Reliability | High | Open |

### Constraints

| ID | Title | Constraint | Category | Priority | Status |
|----|-------|------------|----------|----------|--------|
| C-001 | `LANE_STATE` stays PRIMARY | `lanes.json` is a PRIMARY artifact and `acceptance-matrix.json` is placement-resolved; the partition sets are disjoint and exhaustive, so no "covers both" kind is structurally possible. No change may move `lanes.json` to COORD. | Technical | High | Open |
| C-002 | One ledger, extended | The classification extends the existing machine-parsed ledger; no second authority document. | Technical | High | Open |
| C-003 | No file-scoped blanket exemptions | Allow-list entries are per-site descriptors with individual rationale. | Technical | High | Open |
| C-004 | `primary_feature_dir_for_mission` is OUT of scope | It is already censused on the anchoring axis by a dedicated gate; its fail-loud surface is zero (every live site is PRIMARY-by-design, several documented as requiring the blind anchor); and read-gate inclusion would red ~34 sites and collide with two census floors for no safety gain. This mission does **not** add it to the read-side census, does **not** migrate its ~33 duplicated compositions, and therefore does **not** re-pin the canonicalizer floors. The decision and its rationale are recorded (FR-011/FR-012). | Technical | High | Open |
| C-005 | Scope boundary | Out of scope: the #2966 remainder, the #2964 terminology migration, re-fixing #2824's already-landed functional defect, adding any new `MissionArtifactKind`, and extending the pinned scan-scope prefix set. | Technical | High | Open |
| C-006 | Not a bulk edit | Each site requires an individual semantic decision (kind + disposition + anchoring class); the machine-parsed ledger is the guardrail of record instead of an occurrence map. Operator-confirmed 2026-07-28. | Technical | Medium | Open |
| C-007 | Targeted verification only | The exhaustive architectural sweep is CI's responsibility; local verification names its gates explicitly, including the read-side gate, the closeout gate, `test_resolution_authority_gates.py`, `test_gate_read_literal_ban.py`, and the write-side gate. | Technical | Medium | Open |

### Key Entities

- **Classification ledger** (`docs/development/read-side-seam-classification.md`) — the machine-parsed authority; gains a constrained multi-primitive grammar, per-site rows for the newly censused resolver, and a corrected Known-gap section.
- **Read-side census gate** (`tests/architectural/test_no_read_side_bypass.py`) — AST census, sanctioned-module assertions, shrink-only allow-list, staleness twin-guard; gains a third censused callee, per-primitive non-vacuity, and honest bounds.
- **Anchoring-axis gate** (`tests/architectural/test_resolution_authority_gates.py`) — the pre-existing authority over `primary_feature_dir_for_mission` (floors + allow-list YAML). Named, not modified.
- **Coord-read closeout gate** (`tests/architectural/test_coord_read_residuals_closeout.py`) — one-hop call-shape grammar; loses the `#2214` pin and its pin-existence test, keeps its site floor.
- **Fold-prescription gate** (`tests/architectural/test_gate_read_literal_ban.py`) — blesses the primary-fold call shape; the reason C-004 matters (it *prescribes* the call another gate would forbid).
- **Kind-blind resolvers** — `resolve_feature_dir_for_mission` (subject), the two already censused, and `resolve_feature_dir_for_slug` (zero live sites, latent).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Every censused `resolve_feature_dir_for_mission` site is recorded in the ledger with a disposition and both axes — zero unclassified sites.
- **SC-002**: A planted direct call in a non-sanctioned module reds the read-side gate; the same call via an aliased import also reds; a prose-only mention does not.
- **SC-003**: For every site classified fail-loud, reading its PRIMARY artifact on a mission whose coord worktree is a husk resolves the PRIMARY anchor rather than the husk — zero husk substitutions.
- **SC-004**: Zero deliberate/lenient sites and zero flat-topology executions change from non-raising to raising.
- **SC-005**: The `#2214` pin and its pin-existence test are both absent, both reads in `_run_documentation_wiring` are routed, and the closeout gate is green with non-vacuity provided by its site floor.
- **SC-006**: Mutating a ledger row for **each** primitive independently reds the gate, and parsed row count equals the summed per-primitive census.
- **SC-007**: Every site count claimed in the ledger and the gate docstring matches a fresh census on this base; the previously stale count is corrected in both places and the closeout gate's recorded census is exact.
- **SC-008**: The enumerated honest bounds match the live tree, each with a size, and include the deliberate exclusion of `primary_feature_dir_for_mission` with its rationale.
- **SC-009**: The named targeted gates (read-side, closeout, anchoring-axis, fold-prescription, write-side) are green on the mission's rebased tip; `ruff` and project-mode `mypy` report zero new findings.

## Assumptions

- The squad's corrected numbers hold and are re-derived rather than trusted: `primary_feature_dir_for_mission` = 39 consumer sites / 21 files (ledger and gate docstring both say 40 — stale by one); `resolve_feature_dir_for_mission` = 8 sites / 7 files; live routed canonicalizer count = 43 against a recorded 44.
- #2824's functional defect is already fixed and regression-covered (independently verified); only its comments are in scope.
- The read-side gate currently parses the ledger and resolves aliases; this mission preserves those properties.
- `gap-analysis.md` has no `MissionArtifactKind`, and adding one is out of scope, so its write is anchored without a kind claim and recorded as a bound.
- PR #3007 is clear of every surface this mission touches (verified at spec time by file-list comparison).

## Provenance

Re-framed on 2026-07-28 after a two-lens post-spec adversarial squad
(architect + patterns) reviewed the first draft against the live tree and returned
**10 MAJOR findings**. The disproofs that changed the mission: `primary_feature_dir_for_mission`
is already census-policed on the anchoring axis; its fail-loud surface is zero and
its migration would red two floors; the prescribed per-primitive ledger tables parse
**silently vacuously** (demonstrated by execution); the index grammar cannot
represent a multi-site qualname; deleting the `#2214` pin reds a test by
construction; and a **fourth** kind-blind resolver — unpoliced, un-ledgered — is the
real gap. Issue #3014's premise ("policed by nothing", "~39 sites to migrate to fail
loud") is superseded by this specification; the corrected findings are to be posted
to #3014.

## Out of Scope

- Adding `primary_feature_dir_for_mission` to the read-side census, migrating its ~33 duplicated compositions, or re-pinning the canonicalizer floors (C-004).
- The #2966 remainder, the #2964 terminology migration, and re-fixing #2824's landed defect.
- New `MissionArtifactKind` members; extending the pinned scan-scope prefix set.
- Consolidating the resolver primitives into one parameterized authority (assessed as disproportionate for this mission).
