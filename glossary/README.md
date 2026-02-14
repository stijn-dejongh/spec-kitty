# Spec Kitty Glossary

Canonical terminology for the Spec Kitty project. All new code, specs, plans, and documentation should use these terms consistently.

---

## Core Concepts

### Tool

The CLI application that provides LLM interactions. A tool wraps a model provider and exposes it as a command-line interface that spec-kitty's orchestrator can invoke.

| Field | Description |
|-------|-------------|
| `tool_id` | Unique identifier (e.g., `"claude"`, `"opencode"`, `"codex"`) |
| `command` | CLI executable name (e.g., `"claude"`, `"opencode"`) |

**Examples**: Claude Code, OpenCode, GitHub Codex, Cursor, Google Gemini, Windsurf, Qwen Code, Amazon Q, Roo Cline, Kilocode, Augment Code, GitHub Copilot.

**In code**: `ToolInvoker` (Protocol), `ToolConfig`, `tool_id`, `select_tool()`.

**Legacy note**: Existing spec-kitty code (pre-Doctrine integration) uses `agent` where `tool` is now correct. See [Migration](#migration-from-legacy-naming) below.

---

### Agent

A Doctrine identity — a named persona with a role, capabilities, behavioral rules, and handoff patterns. An agent defines *who* performs a task and *what rules govern* their behavior. An agent runs on a [tool](#tool).

| Field | Description |
|-------|-------------|
| `id` | Unique identifier (e.g., `"python-pedro"`, `"review-rachel"`) |
| `name` | Human-readable name (e.g., `"Python Pedro"`, `"Review Rachel"`) |
| `specialization` | Primary skill area (e.g., `"python"`, `"security"`, `"docs"`) |
| `capabilities` | What the agent can do (e.g., `{"write-code", "write-tests", "refactor"}`) |
| `required_directives` | Directive numbers this agent must follow |

**In code**: `AgentProfile` (dataclass), `agent_profile_id`, `get_agent_profile_for_tool()`.

---

### Agent Profile

The full definition document for an [agent](#agent), stored as a markdown file with YAML front matter in the Doctrine tree at `doctrine/agents/*.agent.md`.

**Example** (`doctrine/agents/python-pedro.agent.md`):

```yaml
---
id: python-pedro
name: Python Pedro
specialization: python
capabilities:
  - write-code
  - write-tests
  - refactor
  - debug
required_directives: [17, 23, 31]
handoff_patterns:
  after_implement: review-rachel
  on_rejection: python-pedro
primer_matrix:
  implement: [spec, plan, architecture]
  fix: [spec, review-comments, test-output]
---
```

---

### Role

The function an agent performs in a workflow phase. Roles are assigned per orchestration step, not permanently — the same agent profile could serve different roles across features.

| Role | Description |
|------|-------------|
| `implementer` | Writes code for a work package |
| `reviewer` | Reviews implementation output |
| `architect` | Designs plans and architecture |
| `documenter` | Writes documentation |

**In code**: `agent_role` field on `GovernanceContext`.

---

### Orchestration Assignment

The complete binding of agent, role, and tool for a single workflow step. The orchestrator constructs an assignment when dispatching work.

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

**Configuration** (`.doctrine-config/config.yaml`):

```yaml
agent_profiles:
  # tool_id → agent_profile_id
  claude: python-pedro
  opencode: review-rachel
```

---

## Lifecycle & Workflow

### Feature

A unit of product change tracked by spec-kitty. Contains a spec, plan, tasks, and work packages. Stored in `kitty-specs/<number>-<slug>/`.

### Work Package (WP)

An individually implementable unit within a feature. Each WP gets its own worktree and branch. Identified as `WP01`, `WP02`, etc.

### Phase

A stage in the spec-driven development lifecycle.

| Phase | Description |
|-------|-------------|
| `specify` | Define what to build (spec.md) |
| `plan` | Design how to build it (plan.md) |
| `tasks` | Break into work packages (tasks/) |
| `implement` | Write code in a worktree |
| `review` | Cross-review by a different tool/agent |
| `accept` | Final approval |
| `merge` | Merge WP branches to target |

### Lane

The kanban state of a work package: `planned`, `doing`, `for_review`, `done`.

---

## Governance

### Governance Plugin

An ABC (`GovernancePlugin`) that validates workflow state at lifecycle boundaries. Returns `ValidationResult` (pass/warn/block). The `NullGovernancePlugin` is the default no-op implementation.

### Directive

A numbered behavioral rule from the Doctrine tree (`doctrine/directives/*.md`). Directives have phase tags indicating when they apply and severity indicating advisory vs required.

### Guideline

A high-level governance rule from `doctrine/guidelines/`. Two levels: **general** (highest precedence) and **operational**.

### Constitution

A project-level governance document (`.kittify/memory/constitution.md`) that narrows or extends Doctrine rules for a specific project. Created via `/spec-kitty.constitution`.

### Precedence Hierarchy

When governance rules conflict, this hierarchy determines which wins:

```
General Guidelines > Operational Guidelines > Constitution > Directives > Approaches
```

### Governance Context

The context object passed to governance hooks. Contains:

| Field | Description |
|-------|-------------|
| `phase` | Current lifecycle phase |
| `feature_slug` | Feature identifier |
| `work_package_id` | WP being validated (if applicable) |
| `tool_id` | Which tool is executing |
| `agent_profile_id` | Which Doctrine agent profile applies |
| `agent_role` | Role: implementer, reviewer, etc. |

---

## Infrastructure

### EventBridge

An ABC for structured event emission at workflow points. `NullEventBridge` discards events (default). `CompositeEventBridge` fans out to registered listeners.

### Doctrine

The Agentic Doctrine — a behavioral governance framework distributed as a git subtree at `doctrine/`. Contains guidelines, directives, approaches, and agent profiles.

### `.doctrine-config/`

Project-level configuration generated from the Constitution via `spec-kitty sync constitution`. Contains `config.yaml` (structured overrides) and `repository-guidelines.md` (narrative). One-way sync: Constitution always wins.

---

## Migration from Legacy Naming

Existing spec-kitty code (pre-0.16) uses `agent` where `tool` is now the correct term. The table below maps old to new:

| Legacy (pre-Doctrine) | Current term | Notes |
|----------------------|--------------|-------|
| `AgentInvoker` | `ToolInvoker` | Protocol for CLI execution |
| `AgentConfig` | `ToolConfig` | Config for available tools |
| `agent_id` | `tool_id` | Tool identifier |
| `agent_config.py` | `tool_config.py` | Config module |
| `select_agent()` | `select_tool()` | Tool selection |
| `--impl-agent` | `--impl-tool` | CLI flag |
| `--review-agent` | `--review-tool` | CLI flag |
| `agents:` (config.yaml) | `tools:` | Config section |
| `spec-kitty agent` | `spec-kitty tool` | CLI command group |
| `AGENT_DIRS` | `TOOL_DIRS` | Directory mapping |

**Strategy**: New code uses `tool` terminology. Existing code is renamed in a dedicated refactor WP. CLI flags and config keys accept both old and new names during transition.
