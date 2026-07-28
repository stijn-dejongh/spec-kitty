# Mission Specification: Read-Side Seam: Primary-Primitive Closure

**Mission Branch**: `fix/read-side-seam-primary-primitive-closure`
**Created**: 2026-07-28
**Status**: Draft
**Input**: Close the read-side placement-seam's third topology-blind primitive — police and route `primary_feature_dir_for_mission` (#3014, the tracked follow-up PR #3012 promised) — plus route `mission_setup_plan::_run_documentation_wiring` through the coord-aware resolver and retire the stale `PINNED: #2214` allow-list entry (#2886), plus correct the actively-wrong T028 comment at `acceptance/__init__.py:1021-1023` (#2824 residual; its functional fix already landed in `6923d1d40`).

## Context & Motivation

Mission artifacts live on one of two partitions: **PRIMARY** (stable planning and
metadata) or **COORD** (lifecycle surfaces on a coordination branch). The
**placement seam** is the single authority that answers "where does this artifact
live?" for a given `MissionArtifactKind`, and it fails loud when the partition it
needs is gone.

PR #3012 routed 72 read call sites onto that seam and added a whole-tree AST gate
(`tests/architectural/test_no_read_side_bypass.py`) so a new kind-blind read cannot
be introduced silently. That gate's census covers **two** topology-blind
primitives: `candidate_feature_dir_for_mission` and `resolve_planning_read_dir`.

A **third sibling primitive** — `primary_feature_dir_for_mission`
(`src/specify_cli/missions/_read_path_resolver.py`) — is equally topology-blind and
policed by **nothing**: no gate, no allow-list, no per-site classification. PR
#3012's own ledger and gate docstring name this as tracked follow-up work; #3014 is
that tracking. A caller on a COORD-topology mission gets back a plausible-looking
PRIMARY-checkout directory with **no exception and no loud failure** — a silently
wrong read, which is worse than a crash because callers build on it believing they
succeeded.

Two smaller residuals in the same thesis are folded here because they are the same
bug class (a read that should be coord-aware but is not) and each is far below
mission size on its own:

- **#2886** — `_run_documentation_wiring` receives a coord-aware directory as a
  parameter but performs PRIMARY-kind reads against it; the closeout gate carries
  it as a deliberate `PINNED: #2214` exception that is self-describing about
  needing removal.
- **#2824 residual** — the functional defect (the acceptance-matrix gate reading
  from the wrong partition) **was already fixed** by `6923d1d40` and is
  regression-covered; what remains is an inline comment that actively misdescribes
  the code and would mislead the next reader.

### Two-axis classification *(load-bearing — learned from #3012's landing pass)*

PR #3012's classification assessed only the **exception axis** ("can this kind
raise on a deleted partition?") and never the **anchoring axis** ("which root does
this resolve against?"). That blind spot let a silent wrong answer through: for a
backfilled mission (bare `<slug>` PRIMARY dir, composed `<slug>-<mid8>` COORD dir)
a composed handle resolved to a nonexistent PRIMARY path — the seam was not
idempotent under its own output. This mission's classification **must record both
axes per site**.

### Gate honesty *(load-bearing — learned from #3012's landing pass)*

#3012's capstone gate initially did not enforce what it advertised: its
ledger-reconciliation test compared two literals inside the same file rather than
parsing the ledger, and an import alias walked past the AST scanner. Both were
repaired during landing (the ledger is now the machine-parsed authority and alias
resolution exists). Extending that gate to a third primitive must **preserve those
properties**, not regress them.

## Domain Language *(load-bearing)*

| Term | Canonical sense in this mission | Do NOT confuse with |
|------|--------------------------------|---------------------|
| **PRIMARY partition** | Stable planning/metadata home for a mission's artifacts. | The Primary Branch (`main`). A PRIMARY-partition verdict is not a "write to main" instruction. |
| **COORD partition** | Lifecycle surfaces routed via the coordination branch. | The PRIMARY partition. |
| **Topology-blind primitive** | A resolver that maps (repo root, handle) → directory with **no** partition awareness: `candidate_feature_dir_for_mission`, `resolve_planning_read_dir`, and — the subject of this mission — `primary_feature_dir_for_mission`. | The kind-aware seam (`placement_seam(...).read_dir(kind)` / `resolve_artifact_surface`), which *is* partition-aware. |
| **Exception axis** | Whether a resolution can raise when the partition is absent/deleted. | The anchoring axis. |
| **Anchoring axis** | Which root the resolution is computed against (repo root vs main-repo root vs coord worktree), and whether the result is idempotent under a composed vs bare handle. | The exception axis. Assessing only one axis is what let a silent wrong answer through in #3012. |
| **sanction-infra** | A call site inside the seam's own internals, legitimately calling the low-level primitive; asserted-sanctioned by the gate, never silently skipped. | An allow-listed lenient site (a *consumer* that stays lenient by design). |
| **Census** | The AST-derived set of real `ast.Call` sites of a named primitive (aliases resolved), which the gate enforces against the ledger. | A grep count. Grep over-counts comments/docstrings and misses aliases. |

## User Scenarios & Testing *(mandatory)*

Primary actor throughout: the **maintainer/agent** running mission lifecycle
commands (`accept`, `merge`, `setup-plan`, status/dashboard reads), plus **future
contributors** who add new read call sites. The value is safety: a read either
returns the right partition's data or fails loudly, and the guarantee is enforced
mechanically rather than by reviewer vigilance.

### User Story 1 - A coord-topology read cannot silently return a PRIMARY path (Priority: P1)

A maintainer runs a lifecycle command against a mission whose authoritative
artifact lives on the COORD partition, in a repository where that coordination
branch has been consolidated away. Today a caller that reaches
`primary_feature_dir_for_mission` receives a plausible PRIMARY-checkout directory
and proceeds on wrong data. After this mission, every such site that *should* be
partition-aware resolves through the seam and fails loud instead.

**Why this priority**: This is the bug class the whole placement-seam programme
exists to remove, on the one primitive #3012 did not reach. A silent wrong answer
is the most expensive failure mode: no stack trace, no signal, downstream work
built on bad data.

**Independent Test**: Drive a migrated call site on a mission whose COORD branch is
deleted; assert it raises the seam's typed error rather than returning a PRIMARY
directory. Assert the healthy (materialized) case resolves to the identical
directory it resolved to before the change.

**Acceptance Scenarios**:

1. **Given** a coord-topology mission with its coordination branch deleted, **When** a migrated (fail-loud-classified) site reads its artifact, **Then** it raises the seam's typed partition error and returns no directory.
2. **Given** the same mission fully materialized, **When** the same site reads, **Then** the resolved directory is byte-identical to the pre-migration result.
3. **Given** a mission whose PRIMARY dir is the bare `<slug>` form while its COORD dir is the composed `<slug>-<mid8>` form (a backfilled mission), **When** a migrated site resolves using either handle form, **Then** the result is correct and idempotent under the seam's own output — no nonexistent path is returned.

---

### User Story 2 - A new topology-blind read cannot be introduced silently (Priority: P1)

A future contributor adds a call to `primary_feature_dir_for_mission` in a module
that should be partition-aware. Today nothing objects. After this mission the
architectural gate reds on it, naming the site, and the contributor must either
route it through the seam or record it as a justified, individually-rationalised
exception.

**Why this priority**: Without enforcement the migration decays — this is the same
"unbounded, one-caller-at-a-time" trap that made #3012 necessary. Enforcement is
what converts a one-time cleanup into a durable invariant.

**Independent Test**: Plant a synthetic `primary_feature_dir_for_mission(...)` call
in a non-sanctioned module and confirm the gate reds; confirm a prose/docstring
mention stays green; confirm an **aliased** import of the primitive also reds.

**Acceptance Scenarios**:

1. **Given** a planted direct call in a non-sanctioned `src/` module, **When** the read-side gate runs, **Then** it fails and names the offending file and symbol.
2. **Given** the same primitive imported under an alias and called, **When** the gate runs, **Then** it still fails (alias resolution is not defeatable).
3. **Given** only a comment or docstring mentioning the primitive, **When** the gate runs, **Then** it passes.
4. **Given** an allow-list entry whose underlying site has since been routed or deleted, **When** the gate runs, **Then** the staleness twin-guard reds until that entry is removed (shrink-only).

---

### User Story 3 - The classification is a machine-checked authority, not prose (Priority: P2)

A maintainer reviewing this mission (or a future one) needs to know that "the
allow-list matches the ledger" is a *fact*, not a claim. The ledger is parsed by
the gate at runtime, and its census numbers reconcile against the live tree.

**Why this priority**: #3012's first attempt at exactly this reconciliation
compared two literals inside the same test file — green, and meaningless. The
authority must be read, not restated.

**Independent Test**: Mutate the ledger in a scratch copy (add/remove a row) and
confirm the gate reds; confirm the ledger's per-primitive census counts match a
fresh AST census of the live tree.

**Acceptance Scenarios**:

1. **Given** a ledger row that disagrees with the gate's allow-list, **When** the gate runs, **Then** it fails (the ledger is parsed, not mirrored).
2. **Given** the ledger's stated per-primitive census totals, **When** compared against a fresh AST census of `src/`, **Then** they agree exactly.

---

### User Story 4 - The two coord-awareness residuals are closed and their exceptions retired (Priority: P2)

`_run_documentation_wiring` performs its metadata reads (and the writes that follow
from them) against the coord-aware directory it is handed, so the closeout gate's
`PINNED: #2214` exception can be deleted and the gate enforces with no exceptions.
Separately, the misleading T028 comment no longer tells a reader that
`read_feature_dir` is coord-resolved or that `lanes.json` should come from COORD.

**Why this priority**: Both are small and bounded, but each is a live trap: the pin
hides a real unrouted site behind a green gate, and the comment would lead the next
maintainer to "fix" `lanes.json` onto the wrong partition.

**Independent Test**: Delete the `PINNED: #2214` entry and confirm the closeout gate
stays green (proving the site is genuinely routed). Read the corrected comment and
confirm it describes what the code does.

**Acceptance Scenarios**:

1. **Given** `_run_documentation_wiring` routed in production, **When** the `PINNED: #2214` allow-list entry is removed, **Then** `test_coord_read_residuals_closeout.py` remains green.
2. **Given** the documentation-wiring path writes audit metadata after its read, **When** it runs, **Then** the write lands on the same partition the read resolved (read and write placement stay coherent).
3. **Given** the corrected comment at the `_check_lane_gates` call site, **When** a reader follows it, **Then** it accurately states that `lanes.json` is a PRIMARY artifact and that only the matrix read is placement-resolved.

---

### Edge Cases

- **Backfilled missions (composed vs bare handle).** A mission whose PRIMARY dir is `<slug>` while its COORD dir is `<slug>-<mid8>`: resolution must be idempotent under the seam's own output. This is the exact shape that produced a silent wrong answer in #3012.
- **Seam internals.** Call sites inside `mission_runtime/resolution.py` (and any sibling infra module) legitimately use the low-level primitive; they must be *asserted-sanctioned*, not silently excluded, or the gate becomes vacuous for the modules that matter most.
- **Flat / coord-less missions.** `SINGLE_BRANCH` / `LANES` topologies route everything to PRIMARY; a migrated site must behave identically there (no new raise).
- **Diagnostic and reporting readers.** Any site whose contract is "never crash" (audit, dashboard, SaaS-facing) must stay lenient and be recorded as such — routing it fail-loud would be a regression, not a fix.
- **Alias / re-export imports.** `from ... import primary_feature_dir_for_mission as X` must not defeat the census.
- **A wrong-`kind` argument.** Passing the wrong `MissionArtifactKind` to an already-seam-routed `read_dir()` call is invisible to any callee-name census (this was #2824's actual defect). It must be named as an honest bound of the gate and covered behaviourally instead of being implied as covered.
- **Census drift during the mission.** `main` moves; the census must be re-derived on the mission's own base rather than trusted from the issue text (which is already stale: 39 sites, not 40, with a changed file set).

## Requirements *(mandatory)*

### Functional Requirements

| ID | Title | User Story | Priority | Status |
|----|-------|------------|----------|--------|
| FR-001 | Route `_run_documentation_wiring` coord-aware | As a maintainer, I want `_run_documentation_wiring`'s metadata read (and the audit-metadata write that follows it) to resolve through the coord-aware authority, so the documentation-wiring path stops reading PRIMARY kinds off a coord-bound directory. | High | Open |
| FR-002 | Retire the `PINNED: #2214` exception | As a maintainer, I want the `PINNED: #2214` allow-list entry deleted from the closeout gate so the invariant is enforced with no exceptions and the tracker no longer hides a live residual behind a green test. | High | Open |
| FR-003 | Correct the misleading T028 comment | As a maintainer, I want the inline comment at the `_check_lane_gates` call site to state what the code actually does — `lanes.json` is a PRIMARY artifact; only the acceptance-matrix read is placement-resolved — so no future reader "fixes" `lanes.json` onto COORD. | Medium | Open |
| FR-004 | Re-census the third primitive | As a maintainer, I want an AST-derived census of `primary_feature_dir_for_mission` call sites on this mission's own base (aliases resolved, definition module excluded), so migration decisions rest on the live tree rather than the issue's stale count. | High | Open |
| FR-005 | Classify every site on both axes | As a maintainer, I want each censused site classified as migrate-fail-loud / stay-lenient / sanction-infra **and** annotated with its target `MissionArtifactKind`, its raise-or-degrade behaviour, and its anchoring root, so no site is migrated on a one-axis assessment. | High | Open |
| FR-006 | Extend the ledger as the single authority | As a maintainer, I want the classification to land as a per-primitive extension of `docs/development/read-side-seam-classification.md` (restructuring its Summary and Coverage blocks into per-primitive sub-tables) rather than a second document, so one machine-parsed authority covers all three primitives. | High | Open |
| FR-007 | Migrate the fail-loud sites | As a maintainer, I want every site classified migrate-fail-loud routed through `placement_seam(...).read_dir(<kind>)` with its ledger-prescribed kind, so coord-partition reads fail loud instead of silently substituting PRIMARY. | High | Open |
| FR-008 | Preserve the lenient sites | As a maintainer, I want every site classified stay-lenient left on its lenient path with its existing degrade behaviour and recorded as a justified allow-list entry, so audit/reporting/SaaS surfaces do not start raising. | High | Open |
| FR-009 | Police the third primitive in the gate | As a maintainer, I want `primary_feature_dir_for_mission` added to the read-side gate's censused callee set, with its sanctions asserted and its lenient residuals allow-listed shrink-only under the staleness twin-guard, so a new bypass reds in CI. | High | Open |
| FR-010 | Keep the gate's advertised bounds honest | As a maintainer, I want the gate to parse the ledger at runtime, resist aliased imports, and state its residual bounds explicitly (including that a wrong-`kind` argument is not census-detectable), so the gate never advertises more coverage than it enforces. | High | Open |

### Non-Functional Requirements

| ID | Title | Requirement | Category | Priority | Status |
|----|-------|-------------|----------|----------|--------|
| NFR-001 | Behaviour-preserving healthy case | For every migrated site, the resolved directory in the healthy (materialized) case is identical to the pre-migration result; any intended behaviour change is named per site in the ledger and pinned by a test. | Reliability | High | Open |
| NFR-002 | No new raises on lenient/flat paths | Zero sites classified stay-lenient, and zero flat/coord-less (`SINGLE_BRANCH`/`LANES`) executions, begin raising as a result of this mission. | Reliability | High | Open |
| NFR-003 | Red-first evidence per behavioural fix | Every behavioural change ships a test demonstrably failing before the fix and passing after (verified by reverting the product file), including the deleted-coord raise and the backfilled composed/bare handle case. | Safety | High | Open |
| NFR-004 | Gate bite, non-vacuity, and authority-parse | The extended gate: reds on a planted direct call **and** on an aliased call; stays green on a prose mention; reds when the parsed ledger disagrees with its allow-list; reds on a stale allow-list entry; and proves each sanctioned module carries a real finding that would otherwise red. | Safety | High | Open |
| NFR-005 | Single scanner authority | The read-side gate continues to consume the shared whole-tree scan scope (no forked tree walk), and the write-side gate remains green after the extension. | Maintainability | High | Open |
| NFR-006 | Census reconciliation | The ledger's per-primitive census totals reconcile exactly against a fresh AST census of `src/` for all three primitives, and the stale "40 sites" figure in the existing Known-gap section is corrected. | Maintainability | Medium | Open |

### Constraints

| ID | Title | Constraint | Category | Priority | Status |
|----|-------|------------|----------|----------|--------|
| C-001 | `LANE_STATE` stays PRIMARY | `lanes.json` is a PRIMARY artifact (`LANE_STATE` ∈ the primary-kinds set). No change may move it to COORD, and no "covers both lanes.json and acceptance-matrix" kind may be introduced — that would break lane-manifest resolution. | Technical | High | Open |
| C-002 | Ledger extended, not duplicated | The classification must extend the existing `read-side-seam-classification.md` (which the gate machine-parses) rather than introducing a second authority document. | Technical | High | Open |
| C-003 | No file-scoped blanket exemptions | Allow-list entries are content descriptors with individual rationale; path-scoped blanket skips are not permitted. | Technical | High | Open |
| C-004 | Scope boundary | Out of scope: the #2966 remainder (parts 2/3/4), the #2964 `feature*`→`mission*` terminology migration, and re-fixing #2824's already-landed functional defect (only its stale comment is in scope). | Technical | High | Open |
| C-005 | Not a bulk edit | Each site requires an individual semantic decision (kind + disposition), so this is not a mechanical same-string replacement; the machine-parsed classification ledger is the guardrail of record instead of an `occurrence_map.yaml`. Operator-confirmed 2026-07-28. | Technical | Medium | Open |
| C-006 | No full architectural suite locally | Verification uses targeted gates and mission suites; the exhaustive `tests/architectural/` sweep is CI's responsibility. | Technical | Medium | Open |

### Key Entities

- **Classification ledger** (`docs/development/read-side-seam-classification.md`) — the machine-parsed authority: one row per call site with primitive, target kind, disposition, raise/degrade behaviour, anchoring root, cluster, and rationale; plus per-primitive census/summary tables the gate reconciles.
- **Read-side gate** (`tests/architectural/test_no_read_side_bypass.py`) — the AST census of topology-blind primitives, its sanctioned-module assertions, and its shrink-only allow-list with staleness twin-guard.
- **Coord-read closeout gate** (`tests/architectural/test_coord_read_residuals_closeout.py`) — the one-hop call-shape gate carrying the `PINNED: #2214` exception this mission retires. A *different* gate with a different grammar from the read-side gate.
- **Topology-blind primitives** — `primary_feature_dir_for_mission` (this mission's subject) alongside the two already censused.
- **`MissionArtifactKind`** — the partition-routing vocabulary the seam consumes.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Every censused `primary_feature_dir_for_mission` site in `src/` is accounted for in the ledger as exactly one of migrate-fail-loud, stay-lenient, or sanction-infra — zero unclassified sites.
- **SC-002**: A synthetic direct call to the primitive added to any non-sanctioned `src/` module reds the read-side gate; the same call written through an aliased import also reds; a prose-only mention does not.
- **SC-003**: Reading a coord-partition artifact on a mission whose coordination branch is deleted fails loud at 100% of migrated sites — zero silent PRIMARY substitutions.
- **SC-004**: Zero stay-lenient sites and zero flat-topology executions change from non-raising to raising.
- **SC-005**: The `PINNED: #2214` entry is absent from the closeout gate and that gate is green.
- **SC-006**: The ledger's per-primitive census totals equal a fresh AST census of the live tree for all three primitives, and no stale count remains in the Known-gap section.
- **SC-007**: A mutated ledger row (added or removed in a scratch copy) reds the gate — proving the authority is parsed, not mirrored.
- **SC-008**: Targeted gates and mission suites are green on the mission's rebased tip; `ruff` and project-mode `mypy` report zero new findings.

## Assumptions

- The functional part of #2824 is already fixed and regression-covered (`6923d1d40`; `tests/integration/test_accept_matrix_coord_partition.py` green) — independently verified on `e97fc6ab9`. Only the comment is in scope.
- The census on this mission's base is ~39 sites / 21 files, of which roughly four are seam internals (sanction-infra), leaving a migration surface near 30. Exact numbers are re-derived in FR-004 rather than assumed.
- `_run_documentation_wiring`'s fix pattern already exists in the same module (a sibling function re-points its planning reads for the same reason), so FR-001 follows established local precedent.
- The read-side gate currently parses the ledger and resolves aliases (repaired during #3012's landing pass); this mission preserves those properties rather than re-establishing them.
- PR #3007 is clear of every surface this mission touches, so no sequencing constraint applies.

## Out of Scope

- The #2966 remainder (parts 2/3/4) — write-target / read-leg consolidation.
- The #2964 `feature*` → `mission*` terminology migration.
- Re-fixing #2824's functional defect (already landed) or altering `lanes.json`'s PRIMARY placement.
- Any change to the write-side gate's own censused grammar beyond keeping it green.
- Broadening the seam's public contract or adding new `MissionArtifactKind` members.
