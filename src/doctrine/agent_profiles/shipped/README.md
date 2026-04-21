# Shipped Agent Profiles

Reference agent profiles included in the `doctrine` package distribution. These
define the core roles with their specialization, collaboration contracts, directive
references, and initialization declarations. Language-specialist profiles (prefixed
with the language name) extend the base `implementer` role for polyglot projects.

| File | Profile ID | Role |
|------|------------|------|
| `architect.agent.yaml` | `architect` | architect |
| `curator.agent.yaml` | `curator` | curator |
| `designer.agent.yaml` | `designer` | designer |
| `implementer.agent.yaml` | `implementer` | implementer |
| `java-implementer.agent.yaml` | `java-implementer` | implementer (Java specialist) |
| `planner.agent.yaml` | `planner` | planner |
| `python-implementer.agent.yaml` | `python-implementer` | implementer (Python specialist) |
| `researcher.agent.yaml` | `researcher` | researcher |
| `reviewer.agent.yaml` | `reviewer` | reviewer |

Shipped profiles are read-only at the package level. Project-level overrides in
`.kittify/charter/agents/` can customize any profile by matching `profile-id`.
