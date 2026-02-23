# Schemas

YAML schema files that provide machine-readable validation for all doctrine
artifact types.

## Available Schemas

| Schema | Validates |
|--------|-----------|
| `directive.schema.yaml` | Governance directives |
| `tactic.schema.yaml` | Tactical procedures |
| `styleguide.schema.yaml` | Style conventions |
| `toolguide.schema.yaml` | Tool-specific guides |
| `mission.schema.yaml` | Mission configurations |
| `agent-profile.schema.yaml` | Agent profile definitions |
| `import-candidate.schema.yaml` | Curation import candidates |

## Validation

Schema validation runs via `tests/doctrine/test_schema_validation.py`.
All doctrine artifacts must conform to their corresponding schema before merge.

## Format

Schemas use JSON Schema draft 2020-12 expressed in YAML.
