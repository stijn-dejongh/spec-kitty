# Tactics

Tactics are actionable procedures that describe *how* to carry out work
governed by directives.

> See `glossary/` for the canonical definition of *tactic*.

## Naming Convention

Files follow the pattern `slug.tactic.yaml`:

- **slug** — kebab-case description of the procedure
- **`.tactic.yaml`** — required suffix

Example: `tdd-red-green-refactor.tactic.yaml`

## Relationship to Directives

Directives define *what* rules apply; tactics define *how* to execute them.
A directive's `tactic_refs` field links to the tactics that implement it.

## Subdirectories

- [`checklists/`](checklists/README.md) — Procedural checklist artifacts
  (code review, design review, architecture review)

## Schema

Tactics are validated against `schemas/tactic.schema.yaml`.
