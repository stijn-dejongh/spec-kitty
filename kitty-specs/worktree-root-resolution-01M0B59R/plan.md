# Implementation Plan: Worktree-Aware Root Resolution & Verdict Parity

**Branch**: `fix/worktree-root-resolution` | **Date**: 2026-08-18 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `kitty-specs/worktree-root-resolution-01M0B59R/spec.md`
**Mission ID**: `01M0B59R1GMN6N33GSGJFVNBP9` · **Base**: `upstream/main` (`31798b6bd9`) · **Topology**: coord

## Summary

Fix the shared root-resolution seam so that no mission-state-writing command silently re-anchors its write, guard check, or review verdict from a linked worktree or standalone clone to an unrelated primary checkout, and unify the review-verdict CLI path so `agent status emit` and `orchestrator-api transition` enforce one topology-aware invariant.

**Technical approach**: Introduce a single **checkout-kind classifier** that the resolver family (`find_repo_root`, `resolve_canonical_root`, `predict_lane_worktree`, `locate_project_root`, `_get_main_repo_root`) consults, distinguishing *primary checkout* / *linked worktree* / *standalone clone*. Writing commands consume a **write-target resolver** that either writes into the invoking checkout or refuses with a path-naming message (mirroring the existing `is_worktree_context` guard that `specify` already uses). On the verdict side, hoist `_parse_review_result_json` and the `for_review` commit-gate into a shared, topology-aware surface consumed by both CLI entry points, and add `--review-result-json` to `agent status emit`. Finish the audit/round-trip residuals (register `review_result` in the shape registry, de-tautologize the drift test, add the round-trip property test) and migrate the coordination-key writer as a separately-sized WP. Every release-blocking slice lands with an issue-pinned red-first regression through the real CLI.

The `review_result` reducer projection (`407ea376c4`) and the `doctor mission-state --fix` verdict preservation (`bec7c25273`) are **already fixed on base** and are explicitly out of the change surface (spec C-001/C-002) — this plan builds on them, it does not re-open them.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: typer, rich, ruamel.yaml (existing); `spec_kitty_events` / `spec_kitty_tracker` public imports only (no vendored copies); no new third-party dependency is introduced by this mission.
**Storage**: filesystem — git checkouts/worktrees, `.kittify/` state, append-only `status.events.jsonl` event log, `meta.json` mission identity. No database.
**Testing**: pytest (`-n auto --dist loadfile` parallel; real-port/daemon tests serial with `-n0`); `@pytest.mark.regression` for issue-pinned red-first reproductions; `tests/architectural/` gates (terminology + shared-package boundary).
**Target Platform**: Linux/macOS developer CLI (Spec Kitty CLI); no runtime service.
**Project Type**: single project (Python CLI package under `src/specify_cli/` + `src/doctrine/` + `src/runtime/`).
**Performance Goals**: No regression to CLI command latency; resolver classification adds only bounded filesystem stat/`.git` reads already performed today (no new process spawns on the hot path).
**Constraints**: New/changed code passes `ruff` + `mypy` with zero issues and zero warnings; complexity ceiling ≤15 (C901/S3776); no new blanket suppressions; canonical terminology (`Mission`, not `feature`); no direct pushes to origin/main; base is `upstream/main` (`31798b6bd9`).
**Scale/Scope**: ~12 CLI commands touched across the resolver seam; ~18 FRs; the change concentrates on one new classifier module + call-site migrations, plus the verdict-parity seam.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Charter present at `.kittify/charter/charter.md`. Governing-principle gates:

| Charter principle | Compliance in this plan |
|-------------------|--------------------------|
| **Single canonical authority** | One checkout-kind classifier owns the primary/worktree/clone distinction; one shared `_parse_review_result_json` + one `for_review` gate own verdict validation. No parallel/duplicate resolvers introduced — existing ones are migrated to consult the single classifier. |
| **Architectural alignment** | Respects the shared-package boundary (consume `spec_kitty_events`/`spec_kitty_tracker` via public imports only). No new cross-boundary reach. |
| **DDD + tiered rigour** | The resolver family is the bounded seam; the classifier is a small pure value-producing unit with focused unit tests. Writing commands depend on the write-target resolver, not on raw `.git` walking. |
| **ATDD-first** | Each behavioral invariant (SC-001…SC-006) is driven outside-in from an acceptance scenario; red-first regression per release-blocking slice (NFR-001). |
| **Terminology adherence** | `Mission`/`primary`/`worktree`/`clone` used per glossary; `primary` sense disambiguated (repository-root checkout vs Primary Branch). Run `tests/architectural/test_no_legacy_terminology.py` pre-push. |
| **Locality of change + smallest viable diff** | The classifier is additive; call sites migrate to it one command at a time. Out-of-scope campsite folds (#3323, #3548) only when already editing that file. |

**No unjustified violations.** Complexity Tracking is empty.

## Project Structure

### Documentation (this mission)

```
kitty-specs/worktree-root-resolution-01M0B59R/
├── plan.md              # This file
├── research.md          # Phase 0 output — root-cause decisions + already-fixed grounding
├── data-model.md        # Phase 1 output — CheckoutKind, WriteTarget, ReviewResult, gate entities
├── quickstart.md        # Phase 1 output — how to reproduce each invariant red-first
├── contracts/           # Phase 1 output — resolver + verdict-CLI + audit contracts
└── tasks.md             # Phase 2 output (/spec-kitty.tasks — NOT created here)
```

### Source Code (repository root)

```
src/specify_cli/
├── core/
│   ├── paths.py                     # resolve_canonical_root — migrate to classifier (FR-001)
│   ├── mission_creation.py          # is_worktree_context (the good guard) — generalize/reuse (FR-002,007)
│   └── checkout_kind.py             # NEW: single checkout-kind classifier + write-target resolver (FR-001)
├── task_utils/
│   └── support.py                   # find_repo_root — migrate to classifier (FR-001)
├── lanes/
│   └── worktree_allocator.py        # predict_lane_worktree — topology-aware, clone-safe (FR-001,011)
├── orchestrator_api/
│   └── commands.py                  # _get_main_repo_root, _parse_review_result_json,
│                                    #   _enforce_for_review_commit_gate — hoist to shared seam (FR-010,011)
├── cli/commands/
│   ├── agent/status.py              # emit: add --review-result-json, fix --help (FR-010,012,013)
│   ├── intake.py                    # _resolve_repo_root — worktree/clone-aware write target (FR-002)
│   └── doctor/…                     # tool-surfaces --fix, mission-state --fix (FR-003,004,009)
├── migrate/… (backfill-runtime-state)  # write into linked worktree + honest cutover guard (FR-005)
├── status/
│   ├── reducer.py                   # projection ALREADY fixed (C-001) — untouched
│   └── audit/shape_registry.py      # register review_result + coordination-key; de-tautologize drift (FR-014,016,018)
├── migration/
│   ├── mission_state.py             # _build_canonical_row preserved (C-002); manifest honesty + _anchor_repair_root (FR-009)
│   └── review/cycle.py              # write-side kind-flip + resolve_review_verdict_facts (FR-017)
└── (setup-plan branch resolver)     # resolve from invoking checkout / meta.json (FR-006)

tests/
├── specify_cli/…                    # unit coverage for classifier + each migrated call site
├── architectural/                   # terminology + shared-package gates (must stay green)
└── <issue-pinned regression tests>  # @pytest.mark.regression red-first per invariant (NFR-001)
```

**Structure Decision**: Single-project Python CLI. The one net-new module is `src/specify_cli/core/checkout_kind.py` (classifier + write-target resolver); everything else is a call-site migration onto it plus the verdict-seam hoist. Exact module boundary (new file vs. extending `core/paths.py`) is confirmed in `research.md` after the code-anchor verification.

## Parallel Work Analysis

### Dependency Graph

```
Foundation (WP-A: checkout-kind classifier + write-target resolver + its unit tests)
    │
    ├── Wave 1 (parallel, each migrates one command family onto the classifier, red-first):
    │     WP-B intake write target (#3540)
    │     WP-C doctor tool-surfaces --fix (#2613)
    │     WP-D doctor mission-state --fix + manifest honesty + clone re-anchor (#3051,#3541)
    │     WP-E migrate backfill-runtime-state + honest cutover guard (#3049)
    │     WP-F setup-plan branch resolution / no false-green (#3124)
    │     WP-G --owned-checkout reachability + .kittify containment boundary (#3449,#2610)
    │
    ├── Wave 1' (parallel, verdict seam — independent of resolver foundation):
    │     WP-H shared _parse_review_result_json + for_review gate hoist, topology-aware (#3547,#1734)
    │     WP-I agent status emit --review-result-json + --help fix + in_review→approved path (#3547,#1734)
    │     WP-J shape_registry: register review_result + round-trip property test + de-tautologize drift (#3543,#3461-registry)
    │     WP-K review/cycle write-side kind-flip + resolve_review_verdict_facts (#3563)
    │
    └── Wave 2 (depends on WP-J): WP-L coordination-key writer migration (#3461-writer, sized separately per C-004)

Integration: full-suite parallel run + architectural gates + spk-analyze cross-artifact check.
```

WP-H gates WP-I (I consumes the hoisted parser/gate). WP-J gates WP-L (writer migration depends on the registered shape). All WP-B…WP-G depend on WP-A. WP-H/…/WP-K are independent of WP-A and can start immediately.

### Work Distribution

- **Sequential (foundation first)**: WP-A must land before the resolver-consumer WPs (B–G).
- **Parallel streams**: resolver-consumer WPs (B–G) are file-disjoint; verdict-seam WPs (H–K) run in a separate stream; WP-L trails WP-J.
- **Agent assignments**: one lane per WP (coord topology); file ownership is disjoint by command module to avoid worktree conflicts.

### Coordination Points

- **Sync**: rebase each lane onto the coord branch after WP-A lands; re-run the architectural terminology gate before each push.
- **Integration tests**: the six SC invariants each have a regression test; the full `spec-kitty analyze` cross-artifact consistency pass runs before consolidation.

## Complexity Tracking

*No Constitution Check violations — table intentionally empty.*
