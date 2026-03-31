# Rebase Alignment Outline

> Historical reference. See `docs/development/architecture_recomposition_tracker.md`
> for the active recomposition tracker and current next steps.

## Purpose

This outline condenses the working material in `work/spec-kitty-rebase/` into a
tracked development note for aligning the large feature-extension branch with
the architectural work already landed on `main`.

## Branch intent to preserve

The feature branch contributes governance-heavy capabilities:

- layered `kernel`, `constitution`, and `doctrine` packages
- doctrine asset expansion, agent profiles, and mission step contracts
- mission/template repository work
- terminology movement from `feature` toward `mission`

`main` contributes execution-heavy architecture:

- explicit context resolution and mission context binding
- ownership manifests and execution modes
- event-log-first status handling
- dedicated merge workspace/engine modules
- thin shim generation for CLI-driven commands

The integration goal is not to choose one branch wholesale. It is to keep
`main`'s execution architecture while carrying forward the feature branch's
governance, asset, and terminology work.

## Main conflict zones

### 1. Template canonical location

- Feature branch moves package templates into `src/doctrine/missions/`.
- `main` still reflects package-default resolution around `src/specify_cli/missions/`
  plus shim-driven command handling.
- Alignment target: keep the shim topology from `main`, but make package-default
  mission assets resolve from doctrine.

### 2. Terminology drift

- The branch work trends toward `mission` language.
- `main` still contains many `feature_*` names in code and imports.
- Alignment target: preserve canonical `Mission` language in active/user-facing
  surfaces and apply the rename where it does not fight `main`'s newer
  execution architecture.

### 3. Replaced subsystems

- `main` intentionally replaced older status and merge modules with new
  event-log and workspace-isolated implementations.
- The feature branch modified several of the older files that no longer survive
  on `main`.
- Alignment target: do not resurrect deleted architectures. Reapply only the
  intent that still matters, primarily terminology and doctrine integration.

### 4. Detection versus explicit context

- The feature branch has mission-detection helpers that many files depend on.
- `main` prefers explicit context and opaque tokens for runtime binding.
- Alignment target: allow detection helpers only where they remain necessary,
  without undercutting `main`'s explicit context model.

## Practical rebase approach

1. Start from `main` as the structural base.
2. Reintroduce additive packages and doctrine assets from the feature branch.
3. Keep `main`'s new context, ownership, migration, status, merge, and shim
   modules as the surviving architecture.
4. Route package-default template resolution toward doctrine-backed assets.
5. Apply the terminology cleanup deliberately rather than mechanically.
6. Resolve conflicts file-by-file in the modules where both branches changed
   structure.
7. Verify import chains, template resolution, and targeted tests after each
   integration slice instead of relying on a single bulk merge outcome.

## File-level decision rules

- Main structure wins for `context/`, `ownership/`, `migration/`, and the
  rewritten `status/` and `merge/` surfaces.
- Feature content wins for doctrine-owned assets, profile definitions, and
  mission-oriented content where no newer `main` structure supersedes it.
- Deleted legacy bridge/status/merge modules stay deleted.
- Reintroduced files need a concrete justification, not a blanket
  `--ours`/`--theirs` merge choice.

## Why the prior bulk strategy failed

- A squash-style attempt surfaced heavy content overlap plus imports that still
  pointed at modules `main` had already deleted.
- Bulk mechanical resolution produced trees that were superficially merged but
  architecturally incoherent.
- The branch therefore needs staged integration with explicit decision rules,
  not a one-shot conflict sweep.

## Source material condensed here

- `work/spec-kitty-rebase/REBASE_PLAN.md`
- `work/spec-kitty-rebase/ARCHITECTURAL_REVIEW.md`
- `work/spec-kitty-rebase/EXECUTION_LOG.md`
