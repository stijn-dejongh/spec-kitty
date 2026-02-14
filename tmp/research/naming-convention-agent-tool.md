# Naming Convention: Agent vs Tool

**Decision date**: 2026-02-15
**Status**: Agreed — apply in Doctrine integration features (040-044+)

## The Problem

Spec-kitty currently uses "agent" to mean the CLI tooling that provides LLM interactions (Claude Code, OpenCode, Codex, Cursor, etc.). The Doctrine integration introduces a second concept — role-based identities with capabilities and behavioral rules — which is also naturally called "agent."

Using "agent" for both creates naming collisions and conceptual confusion.

## The Resolution

| Concept | Term | Definition | Examples |
|---------|------|-----------|----------|
| **Tool** | `tool` | The CLI/vendor that executes LLM prompts | `claude`, `opencode`, `codex`, `cursor`, `gemini` |
| **Agent** | `agent` | A Doctrine identity with name, role, capabilities, and rules | `"python pedro"`, `"doc diana"` |
| **Agent profile** | `agent_profile` | The full definition document for an agent | `doctrine/agents/python-pedro.agent.md` |
| **Role** | `role` | The function an agent performs in a workflow | `implementer`, `reviewer`, `architect` |

### The Assignment Model

An orchestration assignment combines all three:

> Assign agent profile **"python pedro"**, with role **implementer**, running on tool **claude**.

```
┌─────────────────────────────────────────────┐
│  Orchestration Assignment                   │
│                                             │
│  agent_profile: "python pedro"              │
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

## Mapping to Existing Code

### Current names → New names (in new code)

| Current (spec-kitty) | New term | Notes |
|----------------------|----------|-------|
| `AgentInvoker` | `ToolInvoker` | The Protocol that wraps CLI execution |
| `AgentConfig` | `ToolConfig` | Config for available tools |
| `agent_id` | `tool_id` | Identifier for a tool (e.g., "claude") |
| `agent_config.py` | `tool_config.py` | Config loading module |
| `select_agent()` | `select_tool()` | Tool selection logic |
| `--impl-agent` | `--impl-tool` | CLI flag |
| `--review-agent` | `--review-tool` | CLI flag |
| `agents:` (config.yaml) | `tools:` | Config section |
| `spec-kitty agent` | `spec-kitty tool` | CLI command group |
| `AGENT_DIRS` | `TOOL_DIRS` | Directory mapping for tool file deployment |

### Renaming strategy

**New code** (features 040-044+): Use `tool` terminology from the start.

**Existing code**: Rename as part of a dedicated migration/refactor WP within the Doctrine integration. This keeps the Doctrine features clean and avoids mixing old/new terminology in the same codebase.

**Backward compatibility**: CLI flags (`--impl-agent`) should alias to new names during transition. Config file (`agents:` section) should accept both keys temporarily.

## Impact on Feature Specs

### GovernanceContext (042)

```python
class GovernanceContext(BaseModel):
    phase: str
    feature_slug: str
    work_package_id: str | None = None
    tool_id: str | None = None           # Was: agent_key — which tool is assigned
    agent_profile_id: str | None = None  # Doctrine agent profile ID
    agent_role: str | None = None        # Role: implementer, reviewer, etc.
    ...
```

### DoctrineLoader (043)

```python
def get_agent_profile(self, tool_id: str) -> AgentProfile | None:
    """Find the agent profile mapped to a tool.

    Looks up tool_id in .doctrine-config/config.yaml agent_profiles
    mapping to find which doctrine agent profile applies.
    """
```

### Config (043)

```yaml
# .doctrine-config/config.yaml
agent_profiles:
  # tool_id → agent_profile_id
  claude: python-pedro
  opencode: review-rachel
```

### Orchestrator integration

```python
# Before:
impl_agent = select_agent(config, "implementation")

# After:
impl_tool = select_tool(config, "implementation")
agent_profile = get_agent_profile_for_tool(impl_tool.tool_id)

gov_context = GovernanceContext(
    phase="implement",
    feature_slug=state.feature_slug,
    work_package_id=wp_id,
    tool_id=impl_tool.tool_id,
    agent_profile_id=agent_profile.id if agent_profile else None,
    agent_role="implementer",
)
```

## Summary

- **Tool** = the executable (claude, opencode, codex)
- **Agent** = the Doctrine identity (python pedro, doc diana)
- **Role** = the function (implementer, reviewer)
- An agent runs on a tool. A role is assigned to an agent. The orchestrator assigns all three.
