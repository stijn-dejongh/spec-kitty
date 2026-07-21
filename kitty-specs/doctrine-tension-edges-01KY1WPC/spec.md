# Mission Specification: Doctrine Tension as First-Class DRG Edges

**Mission Branch**: `doctrine/drg-missing-links-analysis`
**Created**: 2026-07-21
**Status**: Draft
**Input**: Model doctrine tension as first-class DRG edges, retiring the legacy `opposed_by` field. Anchored on Accepted ADR `docs/adr/3.x/2026-07-21-1-in-tension-with-drg-edge.md`. Anchor ticket #2537 under epic #2466; folds #2737. Out of scope: cascade-all-kinds (#2829), `delegates_to` swarm (#2827).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Operator sees co-activated tension and how to resolve it (Priority: P1)

An operator activates a doctrine artefact (or runs a consistency check) on a pack in which two artefacts that are *in tension* — e.g. "Locality of Change" (DIRECTIVE_024) and "Boy Scout Rule" (DIRECTIVE_025) — are both active. Instead of the competition being invisible (so an agent silently picks a winner), the tooling surfaces an advisory finding that names both artefacts and states the two ways to resolve it.

**Why this priority**: This is the mission's reason to exist — making silent doctrine competition visible with a concrete resolution path. Everything else is enabling machinery.

**Independent Test**: On a pack with two co-activated in-tension artefacts and no reconciliation, `charter consistency-check` and `charter activate` both emit a `tension_unreconciled` finding naming both artefacts and the two resolution paths; the run is advisory (does not hard-fail).

**Acceptance Scenarios**:

1. **Given** two artefacts declared `in_tension_with` each other, both in the active set, and no active reconciler, **When** the operator runs `charter consistency-check`, **Then** a `tension_unreconciled` finding lists the pair and both resolution paths, and the overall result stays coherent (advisory).
2. **Given** the same pair, **When** the operator activates one of them via `charter activate`, **Then** a warning surfaces the tension alongside the existing warnings.
3. **Given** an in-tension pair where only one side is in the active set, **When** consistency-check runs, **Then** no tension finding is raised.

---

### User Story 2 - Tension is resolved by a reconciliation artefact (Priority: P1)

The operator (or a pack author) resolves a flagged tension not by dropping a rule, but by activating a reconciliation artefact whose body explains how to weigh the two rules and which links to both via `reconciles_tension`.

**Why this priority**: The resolution path is half the value; a warning with no structured way to clear it is noise. The built-in default pack ships 024+025 both active, so it must carry such an artefact to stay coherent.

**Independent Test**: Adding an active artefact with `reconciles_tension` edges to both sides of a flagged pair clears the finding; removing either edge (or deactivating the artefact) re-raises it.

**Acceptance Scenarios**:

1. **Given** a flagged in-tension pair `(A, B)`, **When** an active artefact `R` has `reconciles_tension` edges to both `A` and `B`, **Then** the pair is treated as resolved and no finding is raised.
2. **Given** the same `R` but with only one `reconciles_tension` edge (to `A` only), **When** consistency-check runs, **Then** the pair remains flagged.
3. **Given** the built-in default pack, **When** consistency-check runs out of the box, **Then** the 024/025 tension is already reconciled by a shipped built-in reconciliation artefact and no finding is raised.

---

### User Story 3 - `opposed_by` is retired in favour of composable edges (Priority: P2)

A doctrine maintainer removes the legacy `opposed_by` field entirely. Genuine tensions become `in_tension_with` edges; rejections of anti-patterns become `rejects` edges pointing at first-class, marked anti-pattern/smell nodes. No surface anywhere still reads `opposed_by`.

**Why this priority**: `opposed_by` is mis-encoded (extractor maps it to `replaces`, producing a nonsensical mutual 024↔025 cycle), inconsistently consumed (dead for tactics), and fights the field→edge migration. It must go, but the mission delivers value even before this cleanup lands.

**Independent Test**: `grep -rn "opposed_by" src/` returns zero hits; the `Contradiction` model is gone (dead-symbol gate passes); the 024↔025 `replaces` cycle is replaced by a single `in_tension_with` edge; the three paradigm anti-pattern usages are `rejects` edges to marked nodes.

**Acceptance Scenarios**:

1. **Given** the migrated codebase, **When** `opposed_by` is searched across `src/`, **Then** there are zero occurrences (field, schema, model, extractor, YAML).
2. **Given** a `rejects` edge, **When** its target node is inspected, **Then** the target is a first-class node marked as an anti-pattern/smell (not an extractor-invented phantom).
3. **Given** the migration, **When** the built-in DRG is loaded, **Then** every previously-canonical `replaces` edge that was NOT derived from `opposed_by` is still present and unchanged.

---

### User Story 4 - Directives stop being falsely flagged as orphaned (Priority: P2)

A pack author running `charter lint` no longer sees all built-in directives flagged `orphaned_directive`. The phantom `governs` (directive) and `supersedes` (adr) orphan-lint branches — neither of which is a real relation the model can author — are removed. Only genuinely-disconnected directives surface.

**Why this priority**: Persistent false-positive noise on every otherwise-green run for every consumer (#2737). Directly folded into this mission because it is the same relation-vocabulary hygiene.

**Independent Test**: `charter lint` on the built-in layer drops `orphaned_directive` from 25 findings to at most the genuinely-disconnected directives (DIRECTIVE_035, DIRECTIVE_039), with zero false positives on directives already referenced via `scope`/`requires`/`suggests`.

**Acceptance Scenarios**:

1. **Given** the built-in layer, **When** `charter lint` runs after the fix, **Then** directives referenced by any real relation are not flagged, and the finding count for `orphaned_directive` is ≤ 2.
2. **Given** the orphan rule set, **When** it is inspected, **Then** neither `governs` nor `supersedes` appears (they are not `Relation` enum members).

---

### User Story 5 - Every relation is self-describing with glossary parity (Priority: P3)

Anyone reading the code or the glossary finds the same human-readable definition for every DRG relation. The three new relations (`in_tension_with`, `reconciles_tension`, `rejects`) are defined once, identically, in both places.

**Why this priority**: Single canonical authority (charter principle) — relation semantics must not drift between code and docs. Lower priority because it does not change runtime behaviour, but it is a binding quality bar for the new vocabulary.

**Independent Test**: Each new `Relation` member carries a description at its definition point; the glossary holds matching text; the glossary-integrity pipeline reports zero drift.

**Acceptance Scenarios**:

1. **Given** the three new relations, **When** the enum and the glossary are compared, **Then** each relation's description matches verbatim.
2. **Given** the glossary-integrity check, **When** it runs, **Then** it passes with no term-drift findings for the new relations.

### Edge Cases

- **Symmetric authoring drift**: a tension authored in both directions (`A→B` and `B→A`) with divergent reasons — resolved by storing one canonical edge (lexicographically-smaller URN as source) queried both ways; two-direction authoring must not be required or duplicated.
- **Non-transitivity**: `A in_tension_with B` and `B in_tension_with C` must NOT synthesize `A in_tension_with C`; the checker inspects only declared pairs and computes no closure.
- **Half-reconciled pair**: a reconciler with only one of the two `reconciles_tension` edges does not resolve the pair.
- **`rejects` at an unmarked node**: a `rejects` edge whose target is not marked as an anti-pattern/smell is a validation error.
- **Cascade must not manufacture conflict**: activating one side of a tension must not auto-activate the other; activating a reconciler must not drag in the pair (the three new relations are excluded from cascade).
- **Partial migration**: a surface updated on the write side but not the read/checkup side (e.g. an edge authored but a query still assuming direction) — must be prevented; see the Change Surface Map.

## Doctrine Schema & Model Change Surface *(mandatory — read / write / checkup)*

The mission changes the doctrine **schema** and **code models**, and those changes MUST propagate consistently across three surfaces. A change that lands on one surface but not the others is a defect. This map is the acceptance backbone for FR-014/NFR-002.

**Schema changes** (`src/doctrine/schemas/`):
- Remove the `opposed_by` property and the `contradiction` definition from `directive.schema.yaml`, `tactic.schema.yaml`, `paradigm.schema.yaml`.
- Add an anti-pattern/smell node marker (`tags`/`labels`) to the node schema so `rejects` targets are first-class and validatable.

**Code-model changes** (`src/doctrine/drg/models.py` + kind models):
- Add `IN_TENSION_WITH`, `RECONCILES_TENSION`, `REJECTS` to the `Relation` enum, each with a description.
- Remove the `opposed_by` field from `directives/models.py`, `tactics/models.py`, `paradigms/models.py`, and the now-dead `Contradiction` model from `shared/models.py`.

**Propagation across surfaces** (each must be verified independently):

| Surface | What must change | Verification |
|---------|------------------|--------------|
| **Write** (authoring / emission) | Extractor stops minting `replaces` from `opposed_by`; built-in YAML drops `opposed_by`; graph fragments author `in_tension_with` / `reconciles_tension` / `rejects` edges and marked anti-pattern nodes. | No field-authored relationships remain (`test_relationship_migration.py`); `opposed_by` absent from all YAML; extractor blocks removed. |
| **Read** (query / load / render) | DRG queries treat `in_tension_with` symmetrically (union of both directions off one canonical edge); loaders/models expose the new relations; agent-facing context can render "these compete; here is the reconciliation". | Symmetric-query test returns the pair from either endpoint; no consumer assumes a single direction for `in_tension_with`. |
| **Checkup** (validation / lint / gates) | `charter consistency-check` gains the advisory `tension_unreconciled` finding; `charter activate` warns; orphan lint drops the phantom `governs`/`supersedes` branches; glossary-integrity enforces relation-description parity; dead-symbol gate enforces `Contradiction` removal. | The scenarios in US1/US2/US4/US5; grep-zero for `opposed_by`; glossary parity check green. |

## Requirements *(mandatory)*

### Functional Requirements

| ID | Title | User Story | Priority | Status |
|----|-------|------------|----------|--------|
| FR-001 | `in_tension_with` relation | As a doctrine author, I want a symmetric, non-transitive `in_tension_with` relation stored as one canonical edge so competing co-valid artefacts are queryable structure. | High | Open |
| FR-002 | `reconciles_tension` relation | As an operator, I want a `reconciles_tension` relation so an active reconciliation artefact that bridges both sides of a tension resolves it. | High | Open |
| FR-003 | `rejects` relation | As a doctrine author, I want a directional `rejects` relation to express rejection of a named anti-pattern (distinct from tension and from supersession). | High | Open |
| FR-004 | Anti-pattern/smell node marker | As a maintainer, I want anti-pattern/smell targets to be first-class marked nodes so every `rejects` edge terminates at a validatable node, not a phantom. | High | Open |
| FR-005 | Remove `opposed_by` + `Contradiction` | As a maintainer, I want `opposed_by` and the `Contradiction` model removed from every schema and model so there is a single edge-based representation. | High | Open |
| FR-006 | Migrate genuine tensions | As a maintainer, I want 024↔025 and smallest-viable-diff↔025 migrated to single `in_tension_with` edges, replacing the mis-minted `replaces` cycle. | High | Open |
| FR-007 | Migrate anti-pattern rejections | As a maintainer, I want the three paradigm `opposed_by` anti-pattern usages migrated to `rejects` edges pointing at marked nodes. | Medium | Open |
| FR-008 | Remove phantom orphan-lint branches | As a pack author, I want the `governs`/`supersedes` orphan-lint branches removed (or re-pointed at real relations) so directives are not falsely flagged (closes #2737). | High | Open |
| FR-009 | Advisory `tension_unreconciled` finding | As an operator, I want `charter consistency-check` to emit an advisory finding for co-activated unreconciled tension over the activation-filtered graph. | High | Open |
| FR-010 | Activate-time tension warning | As an operator, I want `charter activate` to surface the tension as a warning alongside existing warnings. | Medium | Open |
| FR-011 | Built-in reconciliation artefact | As an operator, I want a shipped built-in reconciliation artefact for 024/025 (and smallest-diff/025) so the default pack is coherent out of the box. | High | Open |
| FR-012 | Relation self-description + glossary parity | As a reader, I want every `Relation` member to carry a description matched verbatim in the glossary. | Medium | Open |
| FR-013 | Cascade exclusion | As a system, I want `in_tension_with`/`reconciles_tension`/`rejects` excluded from cascade so opponents/reconcilers are never auto-activated. | High | Open |
| FR-014 | Consistent surface propagation | As a maintainer, I want schema/model changes to propagate consistently across write, read, and checkup surfaces (see Change Surface Map), with each surface independently verified. | High | Open |

### Non-Functional Requirements

| ID | Title | Requirement | Category | Priority | Status |
|----|-------|-------------|----------|----------|--------|
| NFR-001 | Advisory, never hard-block | The tension check MUST NOT fail coherence by default; the built-in default pack's `consistency-check` returns `coherent = true` with 0 unreconciled-tension findings. | Reliability | High | Open |
| NFR-002 | Migration completeness | `grep -rn "opposed_by" src/` returns 0 hits; `Contradiction` model removed; dead-symbol gate passes; `test_relationship_migration.py` "no field-authored relationships" invariant holds. | Correctness | High | Open |
| NFR-003 | Zero false-positive directives | After the orphan-lint fix, `orphaned_directive` findings ≤ 2 (only genuinely-disconnected directives) with 0 false positives on referenced directives. | Correctness | High | Open |
| NFR-004 | Glossary parity | Each new relation's enum description equals its glossary definition; glossary-integrity pipeline reports 0 drift for the new relations. | Maintainability | Medium | Open |
| NFR-005 | Quality gates | New/changed code passes `ruff` and `mypy` with zero issues; every new branch/helper has focused tests in the same PR. | Maintainability | High | Open |

### Constraints

| ID | Title | Constraint | Category | Priority | Status |
|----|-------|------------|----------|----------|--------|
| C-001 | `replaces` stays canonical | `replaces` and the pack-augmentation family (`enhances`/`overrides`/`specializes_from`) are canonical (multi-tier pack composition, not self-hosted in SK). Do NOT remove them; only `opposed_by`-derived `replaces` edges are touched. | Technical | High | Open |
| C-002 | Symmetric single-edge storage | `in_tension_with` is stored as ONE canonical edge (lexicographically-smaller URN as source), queried both directions; no transitive closure is computed. | Technical | High | Open |
| C-003 | Cascade contract preserved | The three new relations are excluded from cascade `REFERENCE_RELATIONS`; the cascade engine keeps its pure-reachability, no-per-kind-logic contract. | Technical | High | Open |
| C-004 | Out-of-scope items | Cascade-all-kinds (#2829) and `delegates_to` runtime swarm (#2827) are explicitly out of scope. | Business | High | Open |
| C-005 | Edge-authored, not field-derived | Relationships are authored as DRG edges, consistent with extractor retirement (ADR 2026-07-18-1); no new field-form relationship is introduced. | Technical | High | Open |

### Key Entities

- **Relation**: the DRG edge vocabulary; gains `in_tension_with`, `reconciles_tension`, `rejects`, each self-describing.
- **`in_tension_with` edge**: symmetric, non-transitive link between two co-valid, co-activatable artefacts.
- **`reconciles_tension` edge**: link from an active reconciliation artefact to each side of a tension pair.
- **`rejects` edge**: directional link from a good artefact to a marked anti-pattern/smell node.
- **Anti-pattern/smell node marker**: node attribute making rejection targets first-class and validatable.
- **Reconciliation artefact**: a doctrine artefact whose body carries the guidance for weighing a tension pair.
- **`tension_unreconciled` finding**: the advisory consistency-check/activate output for a co-activated, unreconciled tension pair.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: An operator co-activating two in-tension artefacts sees, in both `charter activate` and `charter consistency-check`, a finding naming both artefacts and stating both resolution paths (deactivate one side, or activate a reconciler).
- **SC-002**: The built-in default pack reports `coherent = true` with 0 unreconciled-tension findings out of the box, because 024/025 ship with a reconciliation artefact.
- **SC-003**: `charter lint` `orphaned_directive` findings drop from 25 to ≤ 2 (only genuinely-disconnected directives), with 0 false positives — #2737 closed.
- **SC-004**: `opposed_by` no longer exists anywhere in the codebase (schema, model, YAML, extractor); the mis-encoded 024↔025 `replaces` cycle is gone; all other `replaces` edges are unchanged.
- **SC-005**: Every DRG relation the system defines has a human-readable definition discoverable identically in code and glossary (0 drift for the new relations).
