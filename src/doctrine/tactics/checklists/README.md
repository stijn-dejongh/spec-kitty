# Checklists

Checklists are specialized tactic artifacts that encode step-by-step review
or verification procedures.

## Naming Convention

Files follow the pattern `slug.tactic.yaml` (same suffix as parent tactics):

- `code-review-checklist.tactic.yaml`
- `design-review-checklist.tactic.yaml`
- `architecture-review-checklist.tactic.yaml`

## Purpose

Checklists provide concrete, ordered verification steps for review workflows.
They are referenced by directives and agent profiles as operating procedures.

## Schema

Checklists share the tactic schema: `schemas/tactic.schema.yaml`.
