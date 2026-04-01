## Context: Governance

Terms describing rule ownership, precedence, and policy controls in Spec Kitty.

### Constitution

| | |
|---|---|
| **Definition** | Project-level policy document that captures the HiC's operating constraints, quality rules, and doctrine selections for a repository. Compiled from interview answers and doctrine catalog choices. |
| **Context** | Governance |
| **Status** | canonical |
| **Applicable to** | `1.x`, `2.x` |
| **Related terms** | [Project Constitution](./configuration-project-structure.md#project-constitution), [Constitution Interview](#constitution-interview), [Constitution Compiler](#constitution-compiler), [Human-in-Charge (HiC)](./identity.md#human-in-charge-hic) |

---

### ADR (Architectural Decision Record)

| | |
|---|---|
| **Definition** | Immutable record of a significant technical/domain decision, with context and consequences. |
| **Context** | Governance |
| **Status** | canonical |
| **Applicable to** | `1.x`, `2.x` |
| **Location** | `architecture/1.x/adr/` and `architecture/2.x/adr/` |

---

### Glossary Strictness Policy

| | |
|---|---|
| **Definition** | Governance rule for how semantic conflicts are treated (`warn` vs `block`) under each strictness mode. |
| **Context** | Governance |
| **Status** | canonical |
| **Applicable to** | `1.x`, `2.x` |
| **Default** | `medium` |

---

### Clarification Burst Policy

| | |
|---|---|
| **Definition** | Rule that limits clarification interruption by prioritizing highest-impact conflicts first and capping prompt count per burst. |
| **Context** | Governance |
| **Status** | canonical |
| **Applicable to** | `1.x`, `2.x` |
| **Cap** | 3 prompts per burst |

---

### Precedence Rule

| | |
|---|---|
| **Definition** | Ordering used when policy settings conflict. |
| **Context** | Governance |
| **Status** | canonical |
| **Applicable to** | `1.x`, `2.x` |
| **Operational order (strictness)** | CLI override > step metadata > mission config > global default |

---

### Constitution Interview

| | |
|---|---|
| **Definition** | A guided question-and-answer process that walks the HiC through their project's preferences, constraints, and doctrine selections. Answers are saved to `answers.yaml` and used to compile the constitution. |
| **Context** | Governance |
| **Status** | canonical |
| **Applicable to** | `1.x`, `2.x` |
| **Related terms** | [Constitution](#constitution), [Constitution Compiler](#constitution-compiler), [Human-in-Charge (HiC)](./identity.md#human-in-charge-hic) |

---

### Constitution Compiler

| | |
|---|---|
| **Definition** | The processor that takes the HiC's interview answers and their selected doctrine artifacts, and combines them into a finalized constitution document and supporting governance files. |
| **Context** | Governance |
| **Status** | canonical |
| **Applicable to** | `1.x`, `2.x` |
| **Related terms** | [Constitution](#constitution), [Constitution Interview](#constitution-interview), [Doctrine Catalog](./doctrine.md#doctrine-catalog) |

---

### Governance Resolution

| | |
|---|---|
| **Definition** | The result of checking the HiC's constitution selections against available doctrine catalogs — confirming that the referenced paradigms, directives, and tools actually exist and are compatible with each other. |
| **Context** | Governance |
| **Status** | canonical |
| **Applicable to** | `1.x`, `2.x` |
| **Related terms** | [Constitution Compiler](#constitution-compiler), [Doctrine Catalog](./doctrine.md#doctrine-catalog) |

---

### Trade-off Assessment

| | |
|---|---|
| **Definition** | A required governance process (DIRECTIVE_007) that mandates explicit identification of quality attributes at stake, assessment of their impact on a proposed design, and documentation of accepted trade-offs before an architectural decision is finalised. Assessments must be proportionate to the decision's risk profile. |
| **Context** | Governance |
| **Status** | canonical |
| **Applicable to** | `2.x` |
| **Related terms** | [ADR (Architectural Decision Record)](#adr-architectural-decision-record), [Prestudy Requirement](#prestudy-requirement), [Directive](./doctrine.md#directive) |

---

### Glossary Integrity

| | |
|---|---|
| **Definition** | A governance standard (DIRECTIVE_017) requiring every domain term used in specifications, code, documentation, or agent instructions to have a single canonical definition in the project glossary. Guards against semantic drift — terms silently meaning different things to different actors. |
| **Context** | Governance |
| **Status** | canonical |
| **Applicable to** | `2.x` |
| **Related terms** | [Glossary Strictness Policy](#glossary-strictness-policy), [Constitution](#constitution), [Directive](./doctrine.md#directive) |

---

### Prestudy Requirement

| | |
|---|---|
| **Definition** | A governance gate (DIRECTIVE_035) mandating that significant architectural decisions and initiatives are preceded by a documented situational assessment (System Context Canvas and Lightweight Prestudy) before solution design begins. Prevents technically correct but contextually wrong solutions. |
| **Context** | Governance |
| **Status** | canonical |
| **Applicable to** | `2.x` |
| **Related terms** | [Trade-off Assessment](#trade-off-assessment), [ADR (Architectural Decision Record)](#adr-architectural-decision-record), [Traceable Decisions](#traceable-decisions) |

---

### Traceable Decisions

| | |
|---|---|
| **Definition** | A governance principle (part of DIRECTIVE_035) requiring that every decision is recorded at a consistent level of abstraction and links upward to the constraint or goal that motivated it and downward to the artifacts that implement it. Prevents reasoning from mixing organisational, architectural, design, and code-level concerns within a single rationale. |
| **Context** | Governance |
| **Status** | canonical |
| **Applicable to** | `2.x` |
| **Related terms** | [Prestudy Requirement](#prestudy-requirement), [Drill-Down Documentation](#drill-down-documentation), [ADR (Architectural Decision Record)](#adr-architectural-decision-record) |

---

### Drill-Down Documentation

| | |
|---|---|
| **Definition** | A governance procedure that ensures decisions, documentation, and architecture descriptions are captured at a consistent level of abstraction and scope. Each layer (organisational/strategic, architecture, design, code) addresses a distinct audience. Prevents convoluting reasoning with detail from the wrong abstraction level. |
| **Context** | Governance |
| **Status** | canonical |
| **Applicable to** | `2.x` |
| **Related terms** | [Traceable Decisions](#traceable-decisions), [Prestudy Requirement](#prestudy-requirement), [Procedure](./doctrine.md#procedure) |
