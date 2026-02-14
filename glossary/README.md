# Spec Kitty Living Glossary

Canonical terminology for Spec Kitty. This is a **living artifact** — it evolves with the codebase and domain understanding. All new code, specs, plans, and documentation must use these terms consistently. Terminology decisions are architectural decisions.

**Approaches**: This glossary follows the Living Glossary Practice and Language-First Architecture approaches (`doctrine/approaches/`).

**Status lifecycle**: `candidate` → `canonical` → `deprecated` / `superseded`

---

## Context: Execution (Tools & Invocation)

Terms describing the CLI tooling that executes LLM interactions.

### Tool

| | |
|---|---|
| **Definition** | The CLI application that executes LLM prompts on behalf of the orchestrator. A tool wraps a model provider and exposes it as a command-line interface. |
| **Context** | Execution |
| **Status** | canonical |
| **In code** | `ToolInvoker` (Protocol), `ToolConfig`, `tool_id`, `select_tool()` |
| **Related terms** | [Agent](#agent), [Orchestration Assignment](#orchestration-assignment) |
| **Examples** | Claude Code, OpenCode, GitHub Codex, Cursor, Google Gemini, Windsurf, Qwen Code, Amazon Q, Roo Cline, Kilocode, Augment Code, GitHub Copilot |
| **Decision history** | 2026-02-15: Renamed from "agent" to resolve collision with Doctrine's agent concept. See [naming convention decision](#naming-decision-tool-vs-agent). |

**Fields**:
- `tool_id` — Unique identifier (e.g., `"claude"`, `"opencode"`, `"codex"`)
- `command` — CLI executable name
- `uses_stdin` — Whether the tool reads prompts from stdin

---

### Tool Invoker

| | |
|---|---|
| **Definition** | The Protocol (interface) that defines how a tool is invoked: check installation, build command, parse output. |
| **Context** | Execution |
| **Status** | canonical |
| **In code** | `ToolInvoker` (Protocol, runtime_checkable) |
| **Related terms** | [Tool](#tool) |
| **Legacy name** | `AgentInvoker` |

---

### Invocation Result

| | |
|---|---|
| **Definition** | Structured output of a tool execution — captures success status, stdout/stderr, duration, files modified, commits made, errors, and warnings. |
| **Context** | Execution |
| **Status** | canonical |
| **In code** | `InvocationResult` (dataclass) |
| **Related terms** | [Tool Invoker](#tool-invoker), [Execution Event](#execution-event) |

---

## Context: Identity (Agents & Roles)

Terms describing Doctrine agent identities — *who* performs work and *what rules govern* their behavior.

### Agent

| | |
|---|---|
| **Definition** | A named identity with a role, capabilities, behavioral rules, and handoff patterns. An agent defines *who* performs a task and *what governance applies*. An agent runs on a [tool](#tool). |
| **Context** | Identity |
| **Status** | canonical |
| **In code** | `AgentProfile` (dataclass), `agent_profile_id` |
| **Related terms** | [Agent Profile](#agent-profile), [Role](#role), [Tool](#tool), [Orchestration Assignment](#orchestration-assignment) |
| **Examples** | "Python Pedro" (implementer), "Review Rachel" (reviewer), "Doc Diana" (documenter) |
| **Decision history** | 2026-02-15: Clarified as identity concept, distinct from tool. Existing code's "agent" refers to [Tool](#tool). |

**Fields**:
- `id` — Unique identifier (e.g., `"python-pedro"`)
- `name` — Human-readable name (e.g., `"Python Pedro"`)
- `specialization` — Primary skill area (e.g., `"python"`, `"security"`)
- `capabilities` — What the agent can do (frozenset, e.g., `{"write-code", "write-tests"}`)
- `required_directives` — Directive numbers this agent must follow

---

### Agent Profile

| | |
|---|---|
| **Definition** | The full definition document for an [agent](#agent). A markdown file with YAML front matter stored at `doctrine/agents/*.agent.md`. Contains identity, capabilities, required directives, handoff patterns, and primer matrix. |
| **Context** | Identity |
| **Status** | canonical |
| **In code** | `AgentProfile` (dataclass), `AgentProfile.from_file()` |
| **Related terms** | [Agent](#agent), [Directive](#directive), [Handoff Pattern](#handoff-pattern), [Primer Matrix](#primer-matrix) |

---

### Role

| | |
|---|---|
| **Definition** | The function an agent performs in a workflow phase. Assigned per orchestration step, not permanently — the same agent profile could serve different roles across features or phases. |
| **Context** | Identity |
| **Status** | canonical |
| **In code** | `agent_role` field on `GovernanceContext` |
| **Related terms** | [Agent](#agent), [Phase](#phase), [Orchestration Assignment](#orchestration-assignment) |
| **Values** | `implementer`, `reviewer`, `architect`, `documenter` |

---

### Handoff Pattern

| | |
|---|---|
| **Definition** | A rule in an agent profile defining who receives work next. Specifies direction (e.g., `after_implement`, `on_rejection`) and target agent profile ID. |
| **Context** | Identity |
| **Status** | canonical |
| **Related terms** | [Agent Profile](#agent-profile), [Role](#role) |

---

### Primer Matrix

| | |
|---|---|
| **Definition** | A mapping in an agent profile from task type to required context documents. Defines what context must be loaded before the agent starts a given task type. |
| **Context** | Identity |
| **Status** | canonical |
| **Related terms** | [Agent Profile](#agent-profile) |
| **Example** | `implement: [spec, plan, architecture]`, `fix: [spec, review-comments, test-output]` |

---

## Context: Orchestration (Workflow & Lifecycle)

Terms describing spec-kitty's workflow engine and lifecycle management.

### Orchestration Assignment

| | |
|---|---|
| **Definition** | The complete binding of [agent](#agent), [role](#role), and [tool](#tool) for a single workflow step. The orchestrator constructs an assignment when dispatching work. |
| **Context** | Orchestration |
| **Status** | canonical |
| **Related terms** | [Agent](#agent), [Role](#role), [Tool](#tool) |

> Assign agent profile **"python pedro"**, with role **implementer**, running on tool **claude**.

```
┌─────────────────────────────────────────────┐
│  Orchestration Assignment                   │
│                                             │
│  agent_profile: "python-pedro"              │
│  role: implementer                          │
│  tool: claude                               │
│                                             │
│  ┌──────────────┐    ┌──────────────────┐   │
│  │ Agent        │    │ Tool             │   │
│  │              │    │                  │   │
│  │ name         │    │ tool_id: claude  │   │
│  │ role         │    │ command: claude  │   │
│  │ capabilities │    │ uses_stdin: true │   │
│  │ directives   │    │ is_installed()   │   │
│  │ handoffs     │    │ build_command()  │   │
│  └──────────────┘    └──────────────────┘   │
└─────────────────────────────────────────────┘
```

---

### Feature

| | |
|---|---|
| **Definition** | A bounded unit of product change tracked by spec-kitty. Contains a spec, plan, tasks, and one or more work packages. Goes through the full SDD lifecycle. |
| **Context** | Orchestration |
| **Status** | canonical |
| **In code** | Feature directory at `kitty-specs/<number>-<slug>/` |
| **Related terms** | [Work Package](#work-package), [Phase](#phase), [Spec-Driven Development](#spec-driven-development) |
| **Note** | Specs are change deltas — they describe what to change, not the final state |

---

### Work Package (WP)

| | |
|---|---|
| **Definition** | An independently implementable unit of work within a feature. Each WP gets its own git worktree and branch. Tracked with frontmatter YAML including status lane, dependencies, and assigned tool. |
| **Context** | Orchestration |
| **Status** | canonical |
| **In code** | `work_package_id`, `WPExecution` (dataclass), WP frontmatter in `tasks/*.md` |
| **Related terms** | [Feature](#feature), [Lane](#lane), [Worktree](#worktree), [Dependency Graph](#dependency-graph) |
| **Identifiers** | `WP01`, `WP02`, etc. |

---

### Phase

| | |
|---|---|
| **Definition** | A stage in the spec-driven development lifecycle. Phases are sequential within a feature but WPs within a phase can run in parallel. |
| **Context** | Orchestration |
| **Status** | canonical |
| **Related terms** | [Feature](#feature), [Lane](#lane), [Spec-Driven Development](#spec-driven-development) |
| **Values** | `specify` → `plan` → `tasks` → `implement` → `review` → `accept` → `merge` |

---

### Lane

| | |
|---|---|
| **Definition** | The kanban-style status state of a work package. Lane transitions are the primary events emitted by the EventBridge. |
| **Context** | Orchestration |
| **Status** | canonical |
| **In code** | `lane` field in WP frontmatter |
| **Related terms** | [Work Package](#work-package), [Lane Transition Event](#lane-transition-event) |
| **Values** | `planned` → `doing` → `for_review` → `done` |

---

### Worktree

| | |
|---|---|
| **Definition** | An isolated git working directory created per work package via `git worktree`. Provides isolation between parallel agent work. |
| **Context** | Orchestration |
| **Status** | canonical |
| **In code** | Located at `.worktrees/<feature>-<WP>/` |
| **Related terms** | [Work Package](#work-package) |
| **Synonym** | Run Container (ADR-048) |

---

### Dependency Graph

| | |
|---|---|
| **Definition** | A directed acyclic graph (DAG) of WP dependencies within a feature. Used to enforce ordering and plan parallelization waves. |
| **Context** | Orchestration |
| **Status** | canonical |
| **In code** | `DependencyGraph` class in `src/specify_cli/core/dependency_graph.py` |
| **Related terms** | [Work Package](#work-package) |

---

### Spec-Driven Development (SDD)

| | |
|---|---|
| **Definition** | Spec Kitty's core methodology. The prescribed phase sequence: spec → plan → tasks → implement → review → accept → merge. Code is the source of truth; specs are change requests (deltas). |
| **Context** | Orchestration |
| **Status** | canonical |
| **Related terms** | [Phase](#phase), [Feature](#feature) |
| **Directive** | Directive 034 |

---

### Mission

| | |
|---|---|
| **Definition** | A domain-specific behavioral adapter in Spec Kitty that configures prompts, validation rules, and artifact structures for a particular type of work. |
| **Context** | Orchestration |
| **Status** | canonical |
| **In code** | `src/specify_cli/missions/` — `software-dev`, `research`, `documentation` |
| **Related terms** | [Phase](#phase), [Slash Command](#slash-command) |
| **Distinction** | Missions are domain-scoped; [Directives](#directive) are cross-cutting |

---

### Slash Command

| | |
|---|---|
| **Definition** | An agent-facing shorthand command that triggers a spec-kitty workflow step (e.g., `/spec-kitty.specify`, `/spec-kitty.plan`). Implemented as markdown prompt templates deployed to tool-specific directories. |
| **Context** | Orchestration |
| **Status** | canonical |
| **In code** | Source templates at `src/specify_cli/missions/*/command-templates/*.md` |
| **Related terms** | [Mission](#mission), [Phase](#phase), [Tool](#tool) |
| **Distinction** | Slash commands trigger lifecycle phases; [Tactics](#tactic) provide step-by-step execution within a phase |

---

## Context: Governance

Terms describing behavioral governance — rules, validation, and compliance.

### Doctrine (Agentic Doctrine)

| | |
|---|---|
| **Definition** | Spec Kitty's behavioral governance framework — a stack of Guidelines → Approaches → Directives → Tactics → Templates providing policy enforcement, decision traceability, agent profiles, and precedence-driven constraint systems. Distributed as a git subtree at `doctrine/`. |
| **Context** | Governance |
| **Status** | canonical |
| **Related terms** | [Guideline](#guideline), [Directive](#directive), [Approach](#approach), [Tactic](#tactic), [Constitution](#constitution) |

---

### Guideline

| | |
|---|---|
| **Definition** | A high-level, immutable governance rule from the governance stack. Two levels: **general** (highest precedence, non-negotiable framework values) and **operational** (day-to-day behavioral norms). No project-level override may contradict them. |
| **Context** | Governance |
| **Status** | canonical |
| **Location** | `doctrine/guidelines/general/`, `doctrine/guidelines/operational/` |
| **Related terms** | [Precedence Hierarchy](#precedence-hierarchy), [Directive](#directive), [Constitution](#constitution) |

---

### Directive

| | |
|---|---|
| **Definition** | A numbered, cross-cutting behavioral constraint from the governance stack. Directives have phase tags (indicating when they apply), severity (advisory/required), and structured rules. They can be narrowed by the Constitution but not removed. |
| **Context** | Governance |
| **Status** | canonical |
| **Location** | `doctrine/directives/*.md` (YAML front matter + markdown body) |
| **In code** | `Directive` (dataclass), referenced by integer ID (`directive_refs`) |
| **Related terms** | [Guideline](#guideline), [Precedence Hierarchy](#precedence-hierarchy), [Agent Profile](#agent-profile) |
| **Examples** | Directive 017 (TDD Required), Directive 023 (Conventional Commits), Directive 034 (Spec-Driven Development) |

---

### Approach

| | |
|---|---|
| **Definition** | A mental model and domain-specific philosophical framework within the governance stack. Approaches define *how to think* about a domain or problem type — distinct from step-by-step tactics. |
| **Context** | Governance |
| **Status** | canonical |
| **Location** | `doctrine/approaches/*.md` |
| **Related terms** | [Tactic](#tactic), [Mission](#mission) |
| **Examples** | Living Glossary Practice, Language-First Architecture, Decision-First Development |

---

### Tactic

| | |
|---|---|
| **Definition** | A step-by-step execution pattern within the governance stack — concrete procedures for performing specific activities. Together with Templates, they form the lowest precedence governance layer. |
| **Context** | Governance |
| **Status** | canonical |
| **Location** | `doctrine/tactics/*.tactic.md` |
| **Related terms** | [Approach](#approach), [Template (Doctrine)](#template-doctrine), [Slash Command](#slash-command) |

---

### Template (Doctrine)

| | |
|---|---|
| **Definition** | An output contract and artifact scaffold within the governance stack — the structured format that Tactics produce. Not to be confused with spec-kitty's slash command templates. |
| **Context** | Governance |
| **Status** | canonical |
| **Location** | `doctrine/templates/` |
| **Related terms** | [Tactic](#tactic) |

---

### Constitution

| | |
|---|---|
| **Definition** | A project-level governance document that narrows or extends Doctrine rules for a specific repository. Human-readable markdown created via `/spec-kitty.constitution`. May narrow directive thresholds but must not contradict Guidelines. The `.doctrine-config/` directory is its machine-parseable counterpart. |
| **Context** | Governance |
| **Status** | canonical |
| **Location** | `.kittify/memory/constitution.md` |
| **In code** | Created by constitution command template, parsed by `ConstitutionParser` (Feature 044) |
| **Related terms** | [.doctrine-config/](#doctrine-config), [Guideline](#guideline), [Precedence Hierarchy](#precedence-hierarchy) |
| **Precedence position** | 3 (after General and Operational Guidelines; before Directives) |

---

### `.doctrine-config/`

| | |
|---|---|
| **Definition** | Project-level machine-parseable governance configuration generated from the Constitution via `spec-kitty sync constitution`. Contains `config.yaml` (structured overrides) and `repository-guidelines.md` (narrative). One-way sync: Constitution always wins. |
| **Context** | Governance |
| **Status** | canonical |
| **Related terms** | [Constitution](#constitution) |
| **Key insight** | "Two views of the same governance state — Constitution for humans, `.doctrine-config/` for agents" |

---

### Precedence Hierarchy

| | |
|---|---|
| **Definition** | The conflict resolution order when governance rules disagree. Higher-precedence rules override lower ones. |
| **Context** | Governance |
| **Status** | canonical |
| **In code** | `PrecedenceResolver` (Feature 043) |
| **Related terms** | [Guideline](#guideline), [Constitution](#constitution), [Directive](#directive), [Approach](#approach), [Tactic](#tactic) |

```
General Guidelines > Operational Guidelines > Constitution > Directives > Approaches > Tactics/Templates
```

---

### Governance Plugin

| | |
|---|---|
| **Definition** | An ABC that validates workflow state at lifecycle boundaries. Returns a `ValidationResult` (pass/warn/block) with reasons, directive references, and suggested actions. The `NullGovernancePlugin` is the default no-op implementation. |
| **Context** | Governance |
| **Status** | canonical |
| **In code** | `GovernancePlugin` (ABC), `NullGovernancePlugin`, `DoctrineGovernancePlugin` |
| **Related terms** | [Validation Result](#validation-result), [Governance Context](#governance-context) |

---

### Validation Result

| | |
|---|---|
| **Definition** | Structured output of a governance check. Contains status (pass/warn/block), reasons, directive references, and suggested actions. |
| **Context** | Governance |
| **Status** | canonical |
| **In code** | `ValidationResult` (Pydantic BaseModel, frozen) |
| **Related terms** | [Governance Plugin](#governance-plugin), [Validation Event](#validation-event) |
| **Fields** | `status` (ValidationStatus), `reasons` (list[str]), `directive_refs` (list[int]), `suggested_actions` (list[str]) |

---

### Governance Context

| | |
|---|---|
| **Definition** | The context object passed to governance hooks. Provides the plugin with enough information to make a validation decision without direct file access. |
| **Context** | Governance |
| **Status** | canonical |
| **In code** | `GovernanceContext` (Pydantic BaseModel, frozen) |
| **Related terms** | [Governance Plugin](#governance-plugin), [Tool](#tool), [Agent](#agent), [Role](#role) |

**Fields**:
- `phase` — Current lifecycle phase
- `feature_slug` — Feature identifier
- `work_package_id` — WP being validated
- `tool_id` — Which tool is executing
- `agent_profile_id` — Which Doctrine agent profile applies
- `agent_role` — Role: implementer, reviewer, etc.

---

### Two-Masters Problem

| | |
|---|---|
| **Definition** | The conflict that arises when both [Guidelines](#guideline) and the [Constitution](#constitution) claim top-level behavioral authority over agents. Resolved by the [Precedence Hierarchy](#precedence-hierarchy): Constitution sits at position 3 — it customizes within Guideline bounds, not above them. |
| **Context** | Governance |
| **Status** | canonical |
| **Synonyms** | Dual Authority Problem |
| **Related terms** | [Precedence Hierarchy](#precedence-hierarchy), [Constitution](#constitution), [Guideline](#guideline) |

---

## Context: Events & Telemetry

Terms describing the event emission and telemetry infrastructure.

### EventBridge

| | |
|---|---|
| **Definition** | An ABC for structured event emission at workflow points. All cross-cutting concerns (telemetry, work logs, cost tracking) register as consumers. `NullEventBridge` discards events (default). `CompositeEventBridge` fans out to registered listeners with error isolation. |
| **Context** | Events & Telemetry |
| **Status** | canonical |
| **In code** | `EventBridge` (ABC), `NullEventBridge`, `CompositeEventBridge` |
| **Related terms** | [Lane Transition Event](#lane-transition-event), [Validation Event](#validation-event), [Execution Event](#execution-event) |
| **Architecture** | Unified Event Spine — all lifecycle events flow through a single bridge |

---

### Lane Transition Event

| | |
|---|---|
| **Definition** | Emitted when a work package moves between lanes. The primary unit of progress tracking. |
| **Context** | Events & Telemetry |
| **Status** | canonical |
| **In code** | `LaneTransitionEvent` (Pydantic BaseModel, frozen) |
| **Fields** | `timestamp`, `work_package_id`, `from_lane`, `to_lane`, `agent`, `commit_sha` |
| **Related terms** | [Lane](#lane), [EventBridge](#eventbridge) |

---

### Validation Event

| | |
|---|---|
| **Definition** | Emitted when a governance check runs. Makes governance compliance auditable. |
| **Context** | Events & Telemetry |
| **Status** | canonical |
| **In code** | `ValidationEvent` (Pydantic BaseModel, frozen) |
| **Fields** | `timestamp`, `validation_type`, `status`, `directive_refs`, `duration_ms` |
| **Related terms** | [Validation Result](#validation-result), [EventBridge](#eventbridge) |

---

### Execution Event

| | |
|---|---|
| **Definition** | Emitted when a tool executes work. Captures token usage, cost, duration, and success/failure. |
| **Context** | Events & Telemetry |
| **Status** | canonical |
| **In code** | `ExecutionEvent` (Pydantic BaseModel, frozen) |
| **Fields** | `timestamp`, `work_package_id`, `agent`, `model`, `input_tokens`, `output_tokens`, `cost_usd`, `duration_ms`, `success`, `error` |
| **Related terms** | [EventBridge](#eventbridge), [Invocation Result](#invocation-result) |

---

## Context: Configuration & Project Structure

### `.kittify/`

| | |
|---|---|
| **Definition** | Spec Kitty's project-local configuration directory. Contains `config.yaml` (single source of truth for tool configuration), `merge-state.json` (merge progress), and `memory/constitution.md`. Distinct from `doctrine/` — `.kittify/` is SK-specific; `doctrine/` is the governance framework. |
| **Context** | Configuration |
| **Status** | canonical |

---

### `kitty-specs/`

| | |
|---|---|
| **Definition** | Directory where all feature specifications, plans, tasks, and work package files are stored. Follows naming pattern `<number>-<slug>/`. All planning artifacts are committed to the main branch here before implementation begins. |
| **Context** | Configuration |
| **Status** | canonical |
| **Related terms** | [Feature](#feature) |

---

### `doctrine/`

| | |
|---|---|
| **Definition** | Directory at project root where Doctrine framework artifacts live, distributed as a git subtree. Its root-level placement signals cross-cutting authority. Contains guidelines, directives, approaches, tactics, templates, and agent profiles. |
| **Context** | Configuration |
| **Status** | canonical |
| **Related terms** | [Doctrine](#doctrine-agentic-doctrine) |

---

## Naming Decision: Tool vs Agent

**Date**: 2026-02-15
**Status**: Agreed — apply in Doctrine integration features (040-044+)

**Problem**: Spec-kitty used "agent" to mean the CLI tooling (Claude Code, OpenCode, etc.). Doctrine uses "agent" to mean a role-based identity with capabilities and behavioral rules. Using "agent" for both creates collisions.

**Resolution**: Split into two distinct concepts:
- **Tool** = the CLI executable (claude, opencode, codex)
- **Agent** = the Doctrine identity (Python Pedro, Review Rachel)

**Migration**: New code uses `tool` terminology. Existing code renames in a dedicated refactor WP with backward-compatible aliases during transition.

| Legacy (pre-Doctrine) | Current term |
|----------------------|--------------|
| `AgentInvoker` | `ToolInvoker` |
| `AgentConfig` | `ToolConfig` |
| `agent_id` | `tool_id` |
| `select_agent()` | `select_tool()` |
| `--impl-agent` | `--impl-tool` |
| `--review-agent` | `--review-tool` |
| `agents:` (config) | `tools:` |
| `spec-kitty agent` | `spec-kitty tool` |
| `AGENT_DIRS` | `TOOL_DIRS` |

---

## Historical Terms

Terms from pre-integration origins that may appear in older documentation. Use the canonical terms above in all new work.

| Historical term | Canonical term | Notes |
|---|---|---|
| Iteration (batch execution) | *(no equivalent)* | Spec Kitty uses continuous lane progression per WP, not batch grouping |
| Cycle (TDD RED→GREEN→REFACTOR) | [Phase](#phase) | Related but different granularity |
| Run Container (ADR-048) | [Worktree](#worktree) | Same concept, different name |
| Bootstrap Protocol | *(initialization)* | Handled by `spec-kitty init` |

---

*Last updated: 2026-02-15*
