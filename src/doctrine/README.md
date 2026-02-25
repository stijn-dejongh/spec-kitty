# Doctrine

The **Doctrine Domain** structures reusable governance knowledge in Spec Kitty. It
organizes behavior and constraints into composable artifacts that agents and humans
use across missions and ad-hoc interactions.

## Artifact Taxonomy

| Artifact | Directory | Purpose |
|----------|-----------|---------|
| **Paradigm** | `paradigms/` | Worldview-level framing for how work is approached in a domain |
| **Directive** | `directives/` | Constraint-oriented governance rules (required or advisory) |
| **Tactic** | `tactics/` | Reusable behavioral execution patterns (step-by-step recipes) |
| **Styleguide** | `styleguides/` | Cross-cutting quality and consistency conventions |
| **Toolguide** | `toolguides/` | Tool-specific operational syntax and guidance |
| **Schema** | `schemas/` | Machine-validated contracts for doctrine artifact structure |
| **Template** | `templates/` | Output artifact scaffolds and interaction contracts |
| **Agent Profile** | `agent_profiles/` | Declarative agent identity: role, specialization, collaboration contracts |
| **Import Candidate** | `curation/` | Pull-based intake records for external practices |

## Supporting Directories

| Directory | Purpose |
|-----------|---------|
| `missions/` | Workflow mission definitions (state machines, DAG runtimes, command and content templates) |

## Package

`src/doctrine` is a standalone Python package (`spec-kitty-doctrine`) included in
the wheel distribution. It ships YAML artifacts, JSON schemas, markdown templates,
and the `agent_profiles` Python subpackage. See `pyproject.toml` for package metadata.

## Glossary Alignment

This package implements the **Doctrine Domain** as defined in the
[doctrine glossary context](../../glossary/contexts/doctrine.md). Key naming
distinctions:

- **Agent** = logical collaborator identity (defined here via agent profiles)
- **Tool** = concrete runtime product (Claude Code, Codex, etc.) — managed by `ToolConfig`

See [naming-decision-tool-vs-agent](../../glossary/naming-decision-tool-vs-agent.md)
for the canonical naming decision.
