# Doctrine Reference

The doctrine framework provides machine-readable governance artifacts that
control agent behavior, quality standards, and operational procedures.

## Artifact Categories

| Category | Directory | Schema | Description |
|----------|-----------|--------|-------------|
| Directives | `src/doctrine/directives/` | `directive.schema.yaml` | Cross-cutting rules, enforcement levels, escalation behavior |
| Tactics | `src/doctrine/tactics/` | `tactic.schema.yaml` | Actionable procedures implementing directive intent |
| Paradigms | `src/doctrine/paradigms/` | — | High-level execution models (e.g. Spec-Driven Development) |
| Styleguides | `src/doctrine/styleguides/` | `styleguide.schema.yaml` | Coding and documentation conventions |
| Toolguides | `src/doctrine/toolguides/` | `toolguide.schema.yaml` | Tool-specific operational syntax and patterns |
| Agent Profiles | `src/doctrine/agent_profiles/` | `agent-profile.schema.yaml` | Role-specific agent configurations |
| Missions | `src/doctrine/missions/` | `mission.schema.yaml` | Workflow type configurations and command templates |

## Relationship to Constitution

The constitution (`.kittify/constitution/constitution.md`) captures project-specific
principles and standards. Doctrine artifacts provide the reusable, validated
framework that agents follow *within* constitutional boundaries.

Constitution selection determines which doctrine subsets are active for a project.
Doctrine artifacts are the implementation layer; the constitution is the policy layer.

## Curation and Provenance

External practices enter doctrine through the
[curation workflow](../../src/doctrine/curation/README.md):

1. **Import** — Register source and create candidate files with provenance metadata.
2. **Classify** — Map candidates to doctrine artifact types (tactic, directive, etc.).
3. **Adapt** — Translate source concepts into Spec Kitty terminology.
4. **Validate** — Confirm artifacts pass schema validation and reference integrity.
5. **Adopt** — Mark candidates as adopted with links to resulting artifacts.

All imported artifacts carry traceable `source_references` for attribution.

## Terminology

Canonical definitions for all doctrine terms (directive, tactic, paradigm,
styleguide, toolguide, etc.) are maintained in the project glossary:

- **Glossary source**: `glossary/` directory
- **Compiled artifact**: `project.glossary.yml`

The glossary is the single source of truth for terminology.

## Validation Tests

| Test | Purpose |
|------|---------|
| `tests/doctrine/test_schema_validation.py` | All artifacts conform to their YAML schema |
| `tests/doctrine/test_shipped_profiles.py` | Shipped agent profiles pass integrity checks |
| `tests/doctrine/test_profile_glossary_alignment.py` | Profile terms align with glossary |
| `tests/doctrine/test_directive_entrypoints.py` | Directive references resolve correctly |
| `tests/doctrine/test_curation_agent_profile.py` | Curation pipeline for agent profiles |

## Further Reading

- [Doctrine directory index](../../src/doctrine/README.md)
- [Curation workflow](../../src/doctrine/curation/README.md)
- [Glossary README](../../glossary/README.md)
