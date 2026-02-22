# Paradigms

Paradigms define high-level execution models that shape how work is approached
across the project.

> See `glossary/` for the canonical definition of *paradigm*.

## Naming Convention

Files follow the pattern `slug.paradigm.yaml`:

- **slug** — kebab-case name of the paradigm
- **`.paradigm.yaml`** — required suffix

Example: `spec-driven-development.paradigm.yaml`

## Key Fields

| Field | Purpose |
|-------|---------|
| `id` | Unique kebab-case identifier |
| `name` | Human-readable name |
| `summary` | One-line description of the paradigm |
| `principles` | Ordered list of guiding principles |

## Relationships

Directives reference paradigms via their `paradigm_refs` field to declare
which execution model governs the directive's scope.
