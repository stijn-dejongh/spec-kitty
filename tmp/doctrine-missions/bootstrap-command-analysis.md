# Bootstrap Command Analysis

> Analysis of how `/spec-kitty.bootstrap` would subsume Bootstrap Bill's role
> and wrap constitution into a unified onboarding flow.
>
> Date: 2026-02-15

---

## 1. What Bootstrap Bill Does (That Spec-Kitty Doesn't)

| Bootstrap Bill Responsibility | Spec-Kitty Equivalent | Gap? |
|---|---|---|
| Repo topology mapping (REPO_MAP, SURFACES) | `spec-kitty init` creates `.kittify/` structure | ✅ Covered (different format) |
| Vision capture ("What is this project?") | **Nothing** | ❌ Gap |
| Directory scaffolding (work/, docs/, specs/) | `spec-kitty init` (creates .kittify/, agent dirs) | ✅ Covered (different layout) |
| Doctrine config (.doctrine-config/config.yaml) | `.kittify/config.yaml` (agent config) | ✅ Covered (different schema) |
| Context files for sibling agents (REPO_MAP, SURFACES, WORKFLOWS) | `CLAUDE.md`, `AGENTS.md`, `.cursorrules` | ⚠️ Partially covered |
| Constitution / governance | `/spec-kitty.constitution` (optional, post-init) | ⚠️ Exists but disconnected |
| Tooling detection (CI, linters, test runners) | `spec-kitty check` (validates tools) | ✅ Covered |

## 2. The Core Insight

Bootstrap Bill's value is **the opening question**: "What is the purpose of this repository?"

Spec-kitty currently skips straight from scaffolding (`init`) to optional governance (`constitution`)
to per-feature work (`specify`). The project-level *why* is never explicitly captured.

This means:
- Each `/spec-kitty.specify` discovery interview lacks project context
- The constitution captures *how we build* but not *what we're building or for whom*
- Agents entering a project have no single artifact explaining purpose and scope

### Future Mission Horizons

The purpose-first framing is deliberate — spec-kitty's mission system should expand beyond
engineering. Anticipated future missions include:

| Mission | Domain | Example Projects |
|---------|--------|-----------------|
| `software-dev` | Engineering | APIs, CLIs, web apps |
| `research` | Investigation | Feasibility studies, literature reviews |
| `documentation` | Knowledge capture | User guides, API docs, tutorials |
| `design` | Architecture | ADRs, trade-off analysis, system design |
| `creative-writing` | Creative | Fiction, poetry, worldbuilding, scripts |
| `exploration` | Discovery | Prototyping, spikes, concept validation |

Bootstrap must not assume any particular mission — `vision.md` captures intent that is
mission-agnostic. The mission is selected later, per-feature, during `/spec-kitty.specify`.

## 3. Proposed `/spec-kitty.bootstrap` Flow

```
/spec-kitty.bootstrap
  │
  ├── Phase 1: Vision (NEW — from Bootstrap Bill)
  │   ├── "What is the purpose of this repository?"
  │   ├── "What problem does it address?" (optional — only if purpose implies solving something)
  │   ├── "What does success look like?"
  │   ├── "What's in scope / out of scope?"
  │   ├── "Who are the stakeholders?" (lightweight — not full personas)
  │   └── → .kittify/memory/vision.md
  │
  ├── Phase 2: Agent Customization (NEW)
  │   ├── Present available approaches from doctrine/approaches/
  │   ├── Three paths: accept defaults / pick-and-choose / define custom
  │   ├── Example: "Use TDD" → agents follow RED-GREEN-REFACTOR cycle
  │   ├── Example: "Use test-first bug fixing" → agents write failing test before fixing
  │   ├── Selected approaches recorded in constitution.md "Agent Practices" section
  │   └── → .kittify/memory/constitution.md (agent practices section)
  │
  ├── Phase 3: Technical Standards (from constitution Phase 1)
  │   ├── Languages, frameworks, testing requirements
  │   ├── Performance targets, deployment constraints
  │   └── → .kittify/memory/constitution.md (technical section)
  │
  ├── Phase 3: Code Quality (from constitution Phase 2, optional)
  │   ├── PR requirements, review checklist, quality gates
  │   └── → .kittify/memory/constitution.md (quality section)
  │
  ├── Phase 4: Tribal Knowledge (from constitution Phase 3, optional)
  │   ├── Team conventions, lessons learned
  │   └── → .kittify/memory/constitution.md (tribal section)
  │
  └── Phase 5: Governance (from constitution Phase 4, optional)
      ├── Amendment process, compliance, escalation
      └── → .kittify/memory/constitution.md (governance section)
```

## 4. Key Design Choices

1. **Vision first, standards second** — you need to know *what* before *how*
2. **Constitution folded in** — no longer a separate step; phases 2-5 of bootstrap
3. **Same skip mechanics** — each phase after Vision remains optional (minimal/comprehensive)
4. **Bootstrap Bill eliminated as agent** — his workflow becomes a spec-kitty command
5. **`vision.md` becomes first-class** — referenced by `specify` during feature discovery
6. **Existing `init` untouched** — `bootstrap` runs *after* `init`

## 5. Updated Onboarding Sequence

### Before (current)
```
spec-kitty init          → Scaffolding
/spec-kitty.constitution → Governance (optional, often skipped)
/spec-kitty.specify      → First feature (no project context)
```

### After (proposed)
```
spec-kitty init          → Scaffolding (unchanged)
/spec-kitty.bootstrap    → Vision + Constitution (replaces /spec-kitty.constitution)
/spec-kitty.specify      → First feature (now has vision.md as context)
```

## 6. Artifacts

| Artifact | Source | Created By |
|----------|--------|------------|
| `.kittify/memory/vision.md` | NEW — Doctrine VISION.md adapted | Bootstrap Phase 1 |
| `.kittify/memory/constitution.md` | EXISTING — unchanged format | Bootstrap Phases 2-5 |

## 7. Impact on Existing Commands

| Command | Change |
|---------|--------|
| `/spec-kitty.constitution` | **Deprecated** — folded into `/spec-kitty.bootstrap` phases 2-5 |
| `/spec-kitty.specify` | **Enhanced** — reads `vision.md` during discovery interview for project context |
| `spec-kitty init` | **Unchanged** — bootstrap runs after init |
| `spec-kitty check` | **Minor** — could validate `vision.md` exists |

## 8. Doctrine Source Cross-Reference

| Doctrine Source | Used In Bootstrap |
|----------------|-------------------|
| `agents/bootstrap-bill.agent.md` | Overall workflow model (topology → vision → scaffolding) |
| `guidelines/bootstrap.md` | Phase sequencing (context loading → first small step → summarize) |
| `shorthands/bootstrap-repo.md` | Required input: VISION summary as opening parameter |
| `templates/project/VISION.md` | Template for `vision.md` output (Problem, Outcomes, Scope, Role of Agents) |
| `tactics/repository-initialization.tactic.md` | Checklist structure (directory → config → docs → tooling → commit) |
