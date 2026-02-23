# Doctrine Framework

The `src/doctrine/` directory contains the governance artifacts that guide agent
behavior, quality constraints, and operational procedures in Spec Kitty projects.

> **Conceptual definitions** for doctrine terms (directive, tactic, paradigm, etc.)
> are maintained in `glossary/` and the compiled `project.glossary.yml`.
> The glossary is the single source of truth for terminology — this README is
> a navigational index only.

## Directory Map

| Directory | Contents |
|-----------|----------|
| [`agent_profiles/`](agent_profiles/) | Agent profile domain models, shipped profiles, and validation logic |
| [`curation/`](curation/) | Pull-based curation workflow for importing external practices (see [curation README](curation/README.md)) |
| [`directives/`](directives/) | Cross-cutting governance rules and escalation behavior (see [directives README](directives/README.md)) |
| [`missions/`](missions/) | Mission configurations and command templates for each workflow type |
| [`paradigms/`](paradigms/) | High-level execution model definitions (see [paradigms README](paradigms/README.md)) |
| [`schemas/`](schemas/) | YAML schema files used for machine validation (see [schemas README](schemas/README.md)) |
| [`styleguides/`](styleguides/) | Coding and documentation style conventions (see [styleguides README](styleguides/README.md)) |
| [`tactics/`](tactics/) | Actionable procedures and checklists (see [tactics README](tactics/README.md)) |
| [`templates/`](templates/) | Artifact structure templates (spec, plan, task prompts, agent files) |
| [`toolguides/`](toolguides/) | Tool-specific operational conventions (see [toolguides README](toolguides/README.md)) |

## Read Order

When executing or reviewing work, process doctrine in this order:

1. **Directives** — cross-cutting rules and escalation behavior
2. **Paradigms** and **Tactics** — execution model and procedures
3. **Styleguides** and **Toolguides** — quality and tool conventions
4. **Templates** — artifact structure contracts

## Contribution Flow

1. Register external sources via the [curation workflow](curation/README.md).
2. Validate new artifacts against their [schema](schemas/).
3. Run `pytest tests/doctrine/ -v` to confirm integrity.

## Validation Entrypoints

- **Schema validation**: `tests/doctrine/test_schema_validation.py`
- **Profile integrity**: `tests/doctrine/test_shipped_profiles.py`
- **Glossary alignment**: `tests/doctrine/test_profile_glossary_alignment.py`
- **Directive entrypoints**: `tests/doctrine/test_directive_entrypoints.py`

---

## Future Work

- **T068 — Doctrine catalog generation**: Build a machine-readable catalog
  (id, title, path, type) from all doctrine artifacts for tooling integration
  and automated cross-referencing.
- **T069 — Orphan artifact detection**: Add a CI check that detects doctrine
  files not referenced by any directive, profile, or mission configuration.
