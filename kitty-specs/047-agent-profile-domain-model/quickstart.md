# Quickstart: Agent Profile Domain Model

**Feature**: 047-agent-profile-domain-model

## Key Concepts

- **AgentProfile** — behavioral identity (who an agent IS): purpose, specialization, collaboration
- **ToolConfig** — tool stack availability (which IDE/CLI): claude, copilot, cursor
- These are orthogonal: a tool (claude) can operate as any agent profile (architect, implementer)

## Package Layout

```
src/doctrine/                        # Doctrine package (zero imports from specify_cli)
  agent-profiles/                    # Agent profile subpackage
    __init__.py                      # Public API exports
    profile.py                       # AgentProfile Pydantic model, value objects
    capabilities.py                  # RoleCapabilities, canonical verbs
    repository.py                    # AgentProfileRepository (loading, hierarchy, matching)
    shipped/                         # Shipped reference profiles (.agent.yaml)
      architect.agent.yaml
      designer.agent.yaml
      implementer.agent.yaml
      reviewer.agent.yaml
      planner.agent.yaml
      researcher.agent.yaml
      curator.agent.yaml
  schemas/
    agent-profile.schema.yaml        # YAML schema for validation

src/specify_cli/
  constitution/
    schemas.py                       # AgentProfile removed, imports from doctrine
    resolver.py                      # Uses rich AgentProfile from doctrine
  orchestrator/
    tool_config.py                   # Renamed from agent_config.py
    agent_config.py                  # Deprecated alias → tool_config.py
  cli/commands/agents/
    profile.py                       # CLI: spec-kitty agents profile ...
```

## Common Operations

### Load profiles programmatically

```python
from doctrine.agent_profiles.repository import AgentProfileRepository
from pathlib import Path

repo = AgentProfileRepository(
    shipped_dir=None,  # auto-detects from package
    project_dir=Path(".kittify/constitution/agents"),
)

# List all
profiles = repo.list_all()

# Get by ID
architect = repo.get("architect")

# Find by role
implementers = repo.find_by_role("implementer")

# Find best match for task context
from doctrine.agent_profiles.profile import TaskContext
context = TaskContext(language="python", framework="fastapi")
best = repo.find_best_match(context)
```

### CLI commands

```bash
# List all profiles (shipped + custom)
spec-kitty agents profile list

# Show full profile details
spec-kitty agents profile show architect

# Create custom profile from template
spec-kitty agents profile create --from-template implementer

# Show hierarchy tree
spec-kitty agents profile hierarchy
```

### Profile YAML format

```yaml
# .kittify/constitution/agents/my-specialist.agent.yaml
schema_version: "1.0"
profile_id: my-specialist
name: "My Specialist"
role: implementer
capabilities: [read, write, edit, bash]
specializes_from: implementer
routing_priority: 75
max_concurrent_tasks: 5

specialization_context:
  languages: [python]
  frameworks: [django]
  file_patterns: ["**/models.py", "**/views.py"]

purpose: >
  Implement Django-specific features with deep knowledge of
  the Django ORM, middleware, and template system.

specialization:
  primary_focus: "Django web application development"
  avoidance_boundary: "Frontend JavaScript, infrastructure"

collaboration:
  canonical_verbs: [generate, refine]
  output_artifacts: [code, migration, test]
```

### Import a new profile via curation

```bash
# 1. Create an import candidate
cp src/doctrine/curation/import-candidate.template.yaml \
   src/doctrine/curation/imports/<source>/candidates/my-profile.import.yaml

# 2. Fill in: source provenance, target_type: agent-profile, adaptation notes

# 3. Create the .agent.yaml in src/doctrine/agent-profiles/shipped/
#    (adapted from the source .agent.md)

# 4. Update candidate: status → adopted, resulting_artifacts → path to .agent.yaml

# 5. Validate
pytest tests/doctrine/test_curation_agent_profile.py -v
```

## Testing

```bash
# Run doctrine agent-profiles tests
pytest tests/doctrine/ -v

# Run ToolConfig rename tests
pytest tests/unit/specify_cli/orchestrator/test_tool_config.py -v

# Run CLI profile tests
pytest tests/unit/specify_cli/cli/commands/agents/test_profile_cli.py -v

# Full suite with coverage
pytest -v --cov=src/doctrine --cov-report=term-missing
```

## Files Modified by This Feature

### New files (`src/doctrine/agent-profiles/`)

- `src/doctrine/agent-profiles/__init__.py`
- `src/doctrine/agent-profiles/profile.py`
- `src/doctrine/agent-profiles/capabilities.py`
- `src/doctrine/agent-profiles/repository.py`
- `src/doctrine/agent-profiles/shipped/*.agent.yaml` (7 reference profiles)

### New files (`src/specify_cli/`)

- `src/specify_cli/orchestrator/tool_config.py`
- `src/specify_cli/cli/commands/agents/profile.py`

### Modified files

- `pyproject.toml` — ensure `src/doctrine` in packages list
- `src/doctrine/schemas/agent-profile.schema.yaml` — expanded for 6-section model
- `src/specify_cli/constitution/schemas.py` — AgentProfile removed, imports from doctrine
- `src/specify_cli/constitution/resolver.py` — uses rich AgentProfile from doctrine
- `src/specify_cli/orchestrator/agent_config.py` — replaced with deprecation alias
- `src/specify_cli/cli/commands/agents/__init__.py` — register profile subcommand
- `src/specify_cli/agent_utils/directories.py` — update import
- `src/specify_cli/orchestrator/scheduler.py` — update import
- `src/specify_cli/orchestrator/monitor.py` — update import
- `src/specify_cli/orchestrator/config.py` — update import
- `src/specify_cli/orchestrator/__init__.py` — update re-exports
- `src/specify_cli/cli/commands/init.py` — update import
- `src/specify_cli/cli/commands/agent/config.py` — update import
