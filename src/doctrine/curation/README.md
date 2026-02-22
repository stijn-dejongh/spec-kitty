# Governance Curation

This directory is the pull-based curation entry point for external practices.

## Intent

Capture useful external approaches, tactics, and related doctrine ideas, then
adapt and integrate them into Spec Kitty doctrine so agentic workflows can use
validated, project-aligned guidance.

## Process

1. Capture source provenance as an import candidate.
2. Classify the candidate to target doctrine concepts.
3. Record adaptation notes for Spec Kitty terminology and constraints.
4. Move status through review to adoption.
5. Link adopted candidates to resulting doctrine artifacts.

## Agent-Profile Adaptation Mapping

When an import candidate targets `agent-profile`, use this field mapping to
translate `.agent.md` source files into `.agent.yaml` doctrine artifacts.

| `.agent.md` source | `.agent.yaml` target |
|---|---|
| YAML frontmatter | Top-level profile fields |
| `## 1. Context Sources` | `context-sources:` |
| `## Directive References` table | `directive-references:` list |
| `## 2. Purpose` | `purpose:` scalar |
| `## 3. Specialization` | `specialization:` object |
| `## 4. Collaboration Contract` | `collaboration:` object |
| `## 5. Mode Defaults` table | `mode-defaults:` list |
| `## 6. Initialization Declaration` | `initialization-declaration:` scalar |

Validate the resulting `.agent.yaml` with:

```bash
python -c "
from doctrine.agent_profiles.validation import validate_agent_profile_yaml
from ruamel.yaml import YAML
yaml = YAML(typ='safe')
with open('path/to/profile.agent.yaml') as f:
    data = yaml.load(f)
errors = validate_agent_profile_yaml(data)
print('Valid' if not errors else errors)
"
```

## Example Journey: ZOMBIES TDD

A lead developer reads about ZOMBIES TDD and wants implementation agents to use
it by default.

1. Add a candidate under `imports/<source>/candidates/`.
2. Classify to one or more doctrine concepts (for example `tactic`).
3. Add adaptation notes (terminology + constraints).
4. Mark candidate `adopted` after review.
5. Add resulting artifact links (for example `src/doctrine/tactics/...`).

Adoption without resulting artifact links is invalid.
