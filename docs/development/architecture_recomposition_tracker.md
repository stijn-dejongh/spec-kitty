# Architecture Recomposition Tracker

## Purpose

This is the primary development entrypoint for the ongoing recomposition of the
feature-extension branch onto the newer `main` architecture. It collects the
live follow-up actions that were previously scattered across development notes.

Historical background is preserved in:

- `docs/development/references/effort-recap-2026-03.md`
- `docs/development/references/rebase-alignment-outline.md`

## Current focus

The branch direction remains:

- keep `main`'s execution architecture (`context/`, `ownership/`, event-log
  status, merge engine, shims)
- preserve the governance-heavy additions from the feature branch
  (`kernel`, `constitution`, `doctrine`, agent profiles, mission/template
  repository work)
- continue converging on canonical Mission terminology without reintroducing
  deleted pre-rebase subsystems

## Open recomposition tasks

### 1. Constitution-led path centralization

Status: open

Concrete next steps:

1. Add constitution path routing for `.kittify/constitution/` artifacts such as
   `constitution.md`, `references.yaml`, and `context-state.json`.
2. Centralize `kitty-specs/<mission-slug>/` path construction behind typed path
   services.
3. Unify global runtime path handling for `~/.kittify/`.
4. Reroute remaining hardcoded `.kittify/missions/` sites in migrations,
   runtime bootstrap, and resolver paths.
5. Evaluate whether project config should eventually support path overrides.

### 2. Doctrine migration architecture cleanup

Status: open until explicitly confirmed in architecture docs

Concrete next steps:

1. Confirm `architecture/2.x/04_implementation_mapping/README.md` fully
   reflects doctrine as the canonical package-default asset source.
2. Ensure Loop B / connector-path references no longer point at pre-migration
   `specify_cli/missions/*` asset paths.
3. Ensure the Agent Tool Connectors row no longer describes legacy asset
   fallback as current architecture.
4. Keep `expected-artifacts.yaml` documented as a doctrine-owned artifact
   surface.
5. Keep the 5-tier resolver chain documented and aligned with the runtime.

### 3. `next` mission compatibility gaps

Status: open

Known accepted gaps:

- `plan` mission
- `documentation` mission

Closure criteria for each:

1. `spec-kitty next` returns a real step path rather than blocking early.
2. State-to-action mapping is explicit and deterministic.
3. Required command templates resolve successfully.
4. The current strict `xfail` coverage is replaced by passing tests.

### 4. Verification debt still relevant to merge readiness

Status: open

Known unresolved items worth carrying forward:

1. Wheel packaging verification for doctrine-backed distribution.
2. Glossary pipeline / production-path integration failures previously called
   out during PR #305 verification.
3. Higher-severity type/export/error-handling debt from the March 25 code
   review that still matters after the rebase.

## Operational runbooks moved out of development notes

The CI deploy-key setup guidance now lives at:

- `docs/how-to/runbooks/ssh-deploy-keys.md`

## Working rule

Use this tracker for active next steps. Use the files in
`docs/development/references/` for historical rationale, prior review context,
and rebase background.
