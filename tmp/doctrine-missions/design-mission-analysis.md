# Design Mission Analysis

> Analysis of how a `design` mission fits into the spec-kitty mission system,
> cross-referenced with Doctrine sources.
>
> Date: 2026-02-15

---

## 1. Mission System Integration

Spec-kitty's mission system is **filesystem-based auto-discovery**. Adding a new mission requires:

| Component | Path | Notes |
|-----------|------|-------|
| Mission directory | `src/specify_cli/missions/design/` | New directory |
| Config | `mission.yaml` | Pydantic-validated `MissionConfig` |
| Command overrides | `command-templates/*.md` | Only commands that differ from `software-dev` |
| Artifact templates | `templates/*.md` | Mission-specific templates |
| Migration | `m_0_X_Y_design_mission.py` | Deploys to existing projects |
| Domain enum | `src/specify_cli/mission.py` line ~114 | Add `"design"` literal to `MissionConfig` |

Template merging is automatic: base templates from `software-dev` are copied first, then `design/command-templates/*.md` files overwrite matching names. Only commands that differ need to be written.

---

## 2. Existing Assets to Leverage

| Asset | Location | Relevance |
|-------|----------|-----------|
| 24 ADRs | `architecture/adrs/` | Design mission would produce these |
| ADR template | `architecture/adr-template.md` | Could become a design mission template |
| `plan.md` template | `software-dev` mission | Design mission would expand the architecture section |
| Research mission | `src/specify_cli/missions/research/` | Design borrows research patterns (evidence gathering, source tracking) |
| Governance glossary | `glossary/README.md` | Already has Decision Boundary, Precedence Hierarchy, Escalation terms |
| Documentation mission | `src/specify_cli/missions/documentation/` | Best reference for adding a new mission (v0.12.0 pattern) |

---

## 3. Cross-Reference: Doctrine Sources → Design Mission

| Doctrine Source | File | Maps To (Design Mission) |
|----------------|------|--------------------------|
| **Traceable Decisions** | `doctrine/approaches/traceable-decisions-detailed-guide.md` | Core workflow: decision markers, ADR creation, forward/backward links, decision debt tracking |
| **Locality of Change** | `doctrine/approaches/locality-of-change.md` | Validation gate: Problem Assessment Protocol (evidence ≥ 3 instances, severity measured, baseline considered, simple alternatives first) |
| **PERSONA template** | `doctrine/templates/architecture/PERSONA.md` | Artifact: Stakeholder personas as design input — who's affected, what they care about |
| **Audience Persona** | `doctrine/templates/documentation/audience-persona-template.md` | Artifact: Detailed persona with motivations, frustrations, behavioral cues |
| **Design Vision** | `doctrine/templates/architecture/design_vision.md` | Artifact: Updated as output — business goals, quality attributes, constraints |
| **Technical Design** | `doctrine/templates/architecture/technical_design.md` | Artifact: Per-feature technical design with acceptance criteria, cross-cutting concerns |
| **Functional Requirements** | `doctrine/templates/architecture/functional_requirements.md` | Artifact: Stakeholder overview table with persona references |
| **ADR template** | `doctrine/templates/architecture/adr.md` | Artifact: The primary design decision record |

---

## 4. Proposed Workflow Phases

```
discover → research → design → validate → document
```

| Phase | Purpose | Doctrine Alignment |
|-------|---------|-------------------|
| **Discover** | Problem framing, stakeholder identification, codebase alignment scan | Locality-of-change §2 (Evidence Collection, Severity Measurement) |
| **Research** | Known patterns/techniques, prior art, existing ADRs, codebase conventions | Traceable Decisions §1 (Pre-Task Decision Check), Research mission patterns |
| **Design** | Alternatives evaluation, trade-off analysis, decision recording | Traceable Decisions §2.2 (Decision Markers), Locality §5 (Cost-Benefit Calibration) |
| **Validate** | Cross-reference with existing ADRs, principle alignment, architecture doc update | Traceable Decisions §6 (Validation Requirements), Locality §3 (Architectural Preservation) |
| **Document** | Update architecture docs, personas, link artifacts, communicate decisions | Traceable Decisions §3 (Linking Conventions), §4 (Decision Debt Tracking) |

### Phase Details

#### Discover
- Collect evidence of the problem (≥ 3 concrete instances per Locality-of-change)
- Measure severity (user impact, frequency, workaround cost)
- Establish "do nothing" baseline
- Identify stakeholders and create persona drafts
- Scan codebase for related patterns, conventions, prior decisions

#### Research
- Search for known patterns/techniques that address the problem
- Review existing ADRs for related decisions
- Check alignment with current codebase architecture
- Evaluate prior art (open source, papers, internal patterns)
- Pre-task decision check: what decisions must be made before designing?

#### Design
- Enumerate alternatives (minimum 3 per Traceable Decisions)
- Evaluate trade-offs (pros/cons matrix)
- Apply simple-alternatives-first principle (Locality §4)
- Record decision markers (full or minimal format)
- Draft ADR with context, decision, consequences

#### Validate
- Cross-reference against existing ADRs for contradictions
- Check architectural principle alignment
- Verify locality-of-change discipline (not over-engineering)
- Update architecture docs (design_vision.md, technical_design.md)
- Peer review gate

#### Document
- Finalize ADR and promote to `architecture/adrs/`
- Update stakeholder personas if new insights emerged
- Link artifacts (spec → ADR → code → tests)
- Track decision debt (markers not yet promoted to ADRs)
- Communicate decisions to affected stakeholders

---

## 5. Proposed Artifacts

| Artifact | Template Source | Required/Optional | Produced In Phase |
|----------|----------------|-------------------|-------------------|
| `spec.md` | Custom design-spec template | Required | Discover |
| `plan.md` | Custom design-plan template | Required | Research + Design |
| `tasks.md` | Reuse base | Required | Design |
| `stakeholders/` | Doctrine `PERSONA.md` + `audience-persona-template.md` | Optional | Discover |
| `alternatives.md` | Derived from Traceable Decisions §2.2 | Optional | Design |
| `adr-draft.md` | Doctrine `adr.md` template | Optional | Design |
| `design-vision.md` | Doctrine `design_vision.md` | Optional | Validate |
| `technical-design.md` | Doctrine `technical_design.md` | Optional | Validate |
| `research.md` | Reuse from research mission | Optional | Research |
| `trade-off-matrix.md` | New template | Optional | Design |
| `codebase-alignment.md` | New template | Optional | Research |

---

## 6. How It Differs From Software-Dev

The `software-dev` mission's `plan.md` already has design elements, but the **design mission** differs in these ways:

| Dimension | Software-Dev | Design Mission |
|-----------|-------------|----------------|
| **Research** | Minimal — jump to planning | Front-loaded — pattern/technique discovery before committing |
| **Evidence** | Not required | Required — Locality-of-change Problem Assessment Protocol as gate |
| **Outputs** | Code, tests, docs | ADRs, architecture updates, personas, trade-off analyses |
| **Stakeholders** | Implicit | Explicit — persona artifacts capture who's affected |
| **Architecture** | Plan has architecture section | Living architecture docs updated as outputs |
| **Decision tracking** | Informal | Formal — decision markers, ADR linkage, decision debt registry |
| **Alternatives** | Optional | Required — minimum 3 alternatives evaluated |
| **Validation** | Tests pass | Principle alignment, ADR consistency, locality discipline |

---

## 7. Implementation Estimate

| Item | Count | Notes |
|------|-------|-------|
| `mission.yaml` | 1 | ~80 lines, 5 phases, 8-10 artifacts, 5-6 commands |
| Command template overrides | 3-4 | `specify.md`, `plan.md`, `implement.md`, `review.md` |
| Artifact templates | 5-6 | spec, plan, persona, alternatives, ADR draft, technical design |
| Migration file | 1 | ~150 lines, following `m_0_12_0_documentation_mission.py` pattern |
| `mission.py` change | 1 line | Add `"design"` to domain `Literal` |
| Tests | ~5-8 | Mission loading, template merging, migration |
| `pyproject.toml` | version bump | Required per AGENTS.md |
| `CHANGELOG.md` | entry | Required per AGENTS.md |

**Comparable effort**: Similar to the documentation mission (Feature 012).

---

## 8. Open Questions

1. **Should this become a kitty-specs feature?** (e.g., 046-design-mission) — recommended for dogfooding
2. **Should the design mission reuse spec-kitty's own ADR infrastructure** (`architecture/adrs/`) or create parallel artifacts in `kitty-specs/###-feature/`?
3. **Stakeholder personas**: Per-feature in `kitty-specs/###/stakeholders/` or project-wide in `architecture/personas/`?
4. **Codebase alignment scan**: Manual (agent reads codebase) or automated (tooling to detect patterns)?
5. **Decision debt tracking**: Simple list in `architecture/decision-debt.md` or structured YAML?

---

## 9. Doctrine Principle Alignment Summary

| Doctrine Principle | How Design Mission Honors It |
|-------------------|------------------------------|
| **Human In Charge** | Validate phase requires human review gate; personas center human stakeholders |
| **Locality of Change** | Discover phase enforces evidence collection and "do nothing" baseline |
| **Traceable Decisions** | ADR artifacts with forward/backward links; decision markers in commits |
| **Flow State Awareness** | Design phase captures minimal decision markers during flow, promotes later |
| **Stopping Condition** | Research phase has explicit "enough evidence" criteria |
| **Escalation** | Design decisions that cross decision boundaries trigger escalation |
| **Decision Boundary** | Each phase has clear authority levels (agent-autonomous vs. human-required) |
