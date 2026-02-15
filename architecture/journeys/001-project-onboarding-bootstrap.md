# User Journey: Project Onboarding & Bootstrap

**Status**: DRAFT
**Date**: 2026-02-15
**Primary Contexts**: Project Initialization, Governance
**Supporting Contexts**: Mission Selection, Feature Specification
**Related Spec**: N/A (proposed new feature — would become kitty-specs/04X-bootstrap-command)

---

## Scenario

A developer starts a new project with spec-kitty. They need to go from an empty
directory (or existing repo) to a fully contextualized project where AI agents
understand the project's purpose, technical constraints, and governance rules —
and where the first feature can be specified with full project context.

The current flow (`init` → optional `constitution` → `specify`) leaves a gap:
project-level intent ("what are we building and why?") is never captured. The
proposed `/spec-kitty.bootstrap` command fills this gap by wrapping vision capture
and constitution into a single guided onboarding, replacing the standalone
`/spec-kitty.constitution` command.

---

## Actors

| # | Actor | Type | Persona | Role in Journey |
|---|-------|------|---------|-----------------|
| 1 | Project Owner | `human` | — | Answers vision and governance questions; makes scope decisions |
| 2 | AI Agent | `llm` | — | Conducts discovery interview; generates vision.md and constitution.md |
| 3 | Spec-Kitty CLI | `system` | — | Scaffolds project structure; validates prerequisites; stores artifacts |

---

## Preconditions

1. Developer has spec-kitty CLI installed and available on PATH.
2. A target directory exists (empty or existing repo).
3. At least one supported AI agent is configured (e.g., Claude Code, Copilot, Gemini).
4. Git is available (optional but recommended).

---

## Journey Map

| Phase | Actor(s) | System | Key Events |
|-------|----------|--------|------------|
| 1. Init | Project Owner | CLI scaffolds `.kittify/`, agent dirs, git repo, context files | `ProjectInitialized`, `AgentConfigured` |
| 2. Vision Discovery | Project Owner ↔ AI Agent | AI conducts interview: purpose, outcomes, scope, stakeholders | `VisionInterviewStarted`, `VisionCaptured` |
| 3. Technical Standards | Project Owner ↔ AI Agent | AI asks about languages, testing, performance, deployment | `ConstitutionPhaseCompleted` |
| 4. Code Quality (optional) | Project Owner ↔ AI Agent | AI asks about PR requirements, review gates, documentation standards | `ConstitutionPhaseCompleted` |
| 5. Tribal Knowledge (optional) | Project Owner ↔ AI Agent | AI asks about team conventions, lessons learned, known pitfalls | `ConstitutionPhaseCompleted` |
| 6. Governance (optional) | Project Owner ↔ AI Agent | AI asks about amendment process, compliance, escalation rules | `ConstitutionPhaseCompleted` |
| 7. Bootstrap Complete | — | CLI commits vision.md + constitution.md; displays next steps | `BootstrapCompleted` |
| 8. First Feature | Project Owner | Owner runs `/spec-kitty.specify` — discovery interview now has vision.md context | `FeatureSpecificationStarted` |

---

## Coordination Rules

**Default posture**: Gated (each phase requires human answers before proceeding)

1. Vision phase (Phase 2) is **required** — bootstrap cannot be skipped entirely.
2. Technical Standards (Phase 3) is **recommended** — skippable with confirmation.
3. Phases 4-6 are **optional** — each can be skipped independently.
4. AI Agent proposes answers based on repo analysis; Project Owner confirms or corrects.
5. If `constitution.md` already exists, bootstrap enters **update mode** (merge, don't overwrite).
6. If `vision.md` already exists, bootstrap asks whether to revise or skip Phase 2.

---

## Responsibilities

### Spec-Kitty CLI (Local Runtime)

1. Validate prerequisites (`spec-kitty check`-equivalent before bootstrap).
2. Detect existing artifacts (vision.md, constitution.md) and offer update vs. create.
3. Store outputs in `.kittify/memory/` (vision.md, constitution.md).
4. Commit artifacts to the current branch.
5. Display post-bootstrap guidance (next command: `/spec-kitty.specify`).

### AI Agent (LLM Context)

1. Conduct phase-by-phase discovery interview with skip options.
2. Analyze existing repo structure for context (if bootstrapping an existing project).
3. Generate vision.md from interview answers using Doctrine VISION.md structure.
4. Generate or update constitution.md from interview answers using existing template.
5. Propose sensible defaults where Project Owner skips questions.

---

## Scope: MVP (Phase 1)

### In Scope

1. **Vision capture**:
   - Purpose statement ("What is the purpose of this repository?")
   - Problem statement (optional follow-up — only when purpose implies solving something)
   - Desired outcomes, scope boundaries
   - Lightweight stakeholder identification (names and roles, not full personas)
   - Role of AI agents in this project

2. **Constitution** (existing functionality, repackaged):
   - Technical standards (languages, testing, deployment)
   - Code quality gates (optional)
   - Tribal knowledge (optional)
   - Governance rules (optional)

3. **Artifact generation**:
   - `.kittify/memory/vision.md` (new)
   - `.kittify/memory/constitution.md` (existing format)

### Out of Scope (Deferred)

- Full stakeholder personas (use design mission for deep profiles)
- Architecture decision records (captured per-feature, not at bootstrap)
- CI/CD pipeline generation (use `init` flags or manual setup)
- Multi-repo or monorepo orchestration
- Team/organization-level governance (bootstrap is per-project)

---

## Required Event Set

| # | Event | Emitted By | Phase |
|---|-------|-----------|-------|
| 1 | `ProjectInitialized` | CLI | 1 |
| 2 | `AgentConfigured` | CLI | 1 |
| 3 | `VisionInterviewStarted` | AI Agent | 2 |
| 4 | `VisionCaptured` | AI Agent | 2 |
| 5 | `ConstitutionPhaseCompleted` | AI Agent | 3-6 |
| 6 | `BootstrapCompleted` | CLI | 7 |
| 7 | `FeatureSpecificationStarted` | AI Agent | 8 |

---

## Acceptance Scenarios

1. **Fresh project bootstrap**
   Given an empty directory and spec-kitty installed,
   when the user runs `spec-kitty init` followed by `/spec-kitty.bootstrap`,
   then `.kittify/memory/vision.md` and `.kittify/memory/constitution.md` are created
   and committed to the current branch.

2. **Vision informs feature specification**
   Given a bootstrapped project with `vision.md` containing "CLI tool for X",
   when the user runs `/spec-kitty.specify "add Y feature"`,
   then the discovery interview references the project vision for context alignment.

3. **Minimal bootstrap (skip optional phases)**
   Given a user who wants to start quickly,
   when they complete Phase 2 (Vision) and skip Phases 3-6,
   then `vision.md` is created and `constitution.md` contains sensible defaults
   with a note that phases were skipped.

4. **Existing project bootstrap (update mode)**
   Given an existing project with a `constitution.md`,
   when the user runs `/spec-kitty.bootstrap`,
   then bootstrap detects the existing constitution and offers to update rather than overwrite,
   and creates `vision.md` without affecting constitution content.

5. **Constitution deprecated gracefully**
   Given a user who runs `/spec-kitty.constitution` after bootstrap exists,
   then the command displays guidance to use `/spec-kitty.bootstrap` instead
   and offers to redirect.

---

## Design Decisions

| Decision | Rationale | ADR |
|----------|-----------|-----|
| Vision is a separate file from constitution | Vision captures *what/why*, constitution captures *how* — different lifecycles and audiences | pending |
| Bootstrap runs after init, not merged into init | Init is non-interactive scaffolding; bootstrap is interactive discovery — different concerns | pending |
| Constitution command deprecated, not removed | Backward compatibility; existing projects may have workflows depending on it | pending |
| Phase 2 (Vision) is required, Phases 3-6 optional | A project without stated intent is more harmful than a project without governance rules | pending |
| Events emitted via EventBridge (Feature 040) | Bootstrap is a lane transition-equivalent lifecycle event; use existing infrastructure | pending |
| Opening question is purpose-first, not problem-first | "What is the purpose of this repository?" accommodates non-solution repos (creative writing, exploration, research, worldbuilding) — problem statement is a conditional follow-up only when purpose implies solving something | pending |
| Vision questions are mission-agnostic | Bootstrap must not assume software development — future missions include creative writing, exploration, design, and other non-engineering endeavours | pending |

---

## Product Alignment

1. **Every spec-kitty command leads with discovery** — bootstrap continues this pattern at the project level.
2. **Constitution is governance, not vision** — separating them clarifies the purpose of each artifact.
3. **Agents need project context** — vision.md gives every subsequent agent interaction a "north star" reference.
