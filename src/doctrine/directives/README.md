# Directives

Directives are cross-cutting governance rules that define agent behavior
boundaries, escalation triggers, and enforcement levels.

> See `glossary/` for the canonical definition of *directive*.

## Naming Convention

Files follow the pattern `NNN-slug.directive.yaml` where:

- **NNN** — zero-padded sequence number (001–019 currently)
- **slug** — kebab-case short description
- **`.directive.yaml`** — required suffix

Example: `016-acceptance-test-driven-development.directive.yaml`

## Key Fields

Each directive declares at minimum:

| Field | Purpose |
|-------|---------|
| `id` | Unique SCREAMING_SNAKE identifier (e.g. `CLI_SHELL_TOOLING`) |
| `title` | Human-readable name |
| `intent` | What the directive governs |
| `enforcement` | `mandatory` or `advisory` |
| `fetch_policy` | When and how agents should load related artifacts |

## Schema

Directives are validated against `schemas/directive.schema.yaml`.

## Relationships

- Directives may reference **paradigms** (`paradigm_refs`), **tactics** (`tactic_refs`),
  and **toolguides** (`toolguide_refs`).
- Agent profiles list applicable directives in their `directive-references`.
