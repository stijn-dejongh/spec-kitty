# Implementation Plan — Charter UX & Org-Pack Vocabulary

**Branch**: `main` → `main` (planning/base = merge target)
**Date**: 2026-05-23
**Mission slug**: `charter-ux-and-org-pack-vocabulary-01KSAF14`
**Mission ID**: `01KSAF14K8FZ56MHYT45EGWHHC`
**Spec**: [spec.md](./spec.md)
**Research brief**: [research/mission-brief.md](./research/mission-brief.md)
**Linked issues**: #1099, #1100, #1101, #1104, #1291 (parent epic #1111)

## Summary

Bundle epic #1111 Slice A (charter freshness UX) and Slice F (pack-authoring vocabulary) into a single mission with a cross-cutting `shipped → built-in` rename. The work splits along the same two code surfaces (charter CLI + doctrine schema/validator pipeline), so a single mission with carefully sequenced waves avoids the merge conflicts that would arise from parallel missions.

Technical approach:
1. Instrument `charter status`/`lint`/`synthesize` with explicit graph-state and freshness reporting (Wave 1).
2. Add a new `charter preflight` command and a callable session-start hook (Wave 2).
3. Add `overrides` and `enhances` as first-class declarative fields across five doctrine artifact kinds; extend the `Relation` enum; reconcile the pack-validator advisory wording with the field-merge ADR (Wave 3).
4. Cutover vocabulary `shipped → built-in` across code, tests, JSON, docs (Wave 4 — last, because it touches the broadest surface).

## Technical Context

**Language/Version**: Python 3.11+ (existing spec-kitty toolchain)
**Primary Dependencies**: typer (CLI), ruamel.yaml (YAML), pydantic (schema models), rich (console rendering); existing `doctrine.drg` and `charter.synthesizer` packages
**Storage**: Filesystem only — `kitty-specs/<mission>/`, `.kittify/charter/*`, `.kittify/doctrine/graph.yaml`, `src/doctrine/*/built-in/*.yaml`
**Testing**: pytest (unit + integration + architectural); existing test patterns under `tests/specify_cli/charter_lint/`, `tests/specify_cli/doctrine/`, `tests/integration/test_charter_*`, `tests/architectural/`
**Target Platform**: Linux/macOS/Windows 10+ (DIR-001 cross-platform)
**Project Type**: single (Python CLI tool with library packages); follows existing `src/` layout
**Performance Goals**: Charter preflight <300 ms warm / <1.0 s cold (NFR-001); lint/status response unchanged for repos with existing DRG
**Constraints**: `mypy --strict` passes; `ruff check` passes; no regression in existing test suite (NFR-003); no fixture YAML must fail to load after the new `overrides`/`enhances` fields land (NFR-004); ASCII-only identifiers (DIR-010 / DIR-011); HiC must be assigned to each linked GitHub issue when a WP for that issue begins implementing (DIR-012)
**Scale/Scope**: ~63 Python files touch `shipped` vocabulary; ~459 source-line occurrences; ~90 test files; ~48 docs/YAML files. 8 issues closed by this mission (5 primary + 3 derived from epic body)

## Charter Check

The project charter `.kittify/charter/charter.md` is present, SYNCED, and synthesized. Action-scoped context for `plan` was loaded via `spec-kitty charter context --action plan --json`. Relevant gates applied to this plan:

| Charter rule | Compliance plan |
|---|---|
| **DIR-001** Cross-platform (Linux/macOS/Windows) | All new code is pure Python; no shell-specific dependencies. Preflight command uses `pathlib` and `subprocess` portably. |
| **DIR-005 / DIR-006 / DIR-007** Tests, types, docstrings | Every new function lands with pytest coverage, mypy-strict annotations, docstrings for public APIs. |
| **DIR-008** No security issues | No credential/secret handling in new code; preflight does not touch git remotes. |
| **DIR-009** Breaking changes documented | FR-017 requires a CHANGELOG entry for the `shipped → built-in` JSON rename. |
| **DIR-010 / DIR-011** ASCII identifier safety | New URN strings for `Relation.ENHANCES`, `Relation.OVERRIDES` are ASCII-only. |
| **DIR-012** HiC issue assignment | First WP for each linked issue assigns the GitHub issue to the HiC before implementation begins. |
| **DIR-013** Pre-existing failure reporting | If implementation surfaces pre-existing pytest failures, open a GitHub issue per the directive before proceeding. |
| **ADR `2026-05-16-1-doctrine-layer-merge-semantics.md`** | Field-merge behaviour is locked (Constraint C-001). New fields are declarative only; they do not change merge code paths. |
| **`__all__` convention** (binding C-007) | New public symbols added to package `__init__.py` exports. |
| **ATDD-First** (binding C-011) | Tests for FR-001..FR-017 written before or alongside production code (matched by WP structure). |

**Charter-Check verdict**: PASS. No violations require justification; the Complexity Tracking table at the end of this plan is empty.

## Project Structure

### Documentation (this mission)

```
kitty-specs/charter-ux-and-org-pack-vocabulary-01KSAF14/
├── spec.md                  # /spec-kitty.specify output (committed)
├── plan.md                  # this file (/spec-kitty.plan output)
├── research.md              # Phase 0 — consolidated decisions
├── data-model.md            # Phase 1 — new model fields & freshness state object
├── quickstart.md            # Phase 1 — operator-facing smoke flow
├── contracts/
│   ├── charter-status-json.md       # JSON contract for `charter status --json`
│   ├── charter-lint-json.md         # JSON contract for `charter lint --json`
│   ├── charter-preflight-json.md    # JSON contract for new `charter preflight`
│   └── pack-validator-advisory.md   # Validator wording / suppression rules
├── occurrence_map.yaml      # bulk-edit gate (shipped → built-in)
├── research/
│   └── mission-brief.md     # Researcher Robbie pre-research (already committed)
├── checklists/
│   └── requirements.md      # Spec quality checklist
├── tasks/                   # /spec-kitty.tasks output (not yet)
└── meta.json                # mission identity (change_mode: bulk_edit)
```

### Source code (repository root)

The mission touches these existing trees and adds a new `charter_preflight` package:

```
src/
├── charter/
│   ├── drg.py                       # Wave 3 — `_warn_project_override` vocabulary; new `enhances`/`overrides` edge handling
│   ├── synthesizer/
│   │   └── project_drg.py           # Wave 1 — synthesize bootstrap post-condition (FR-009)
│   └── … (other charter modules unchanged)
├── doctrine/
│   ├── schemas/
│   │   ├── tactic.schema.yaml       # Wave 3 — add `overrides` / `enhances`
│   │   ├── styleguide.schema.yaml   #     ditto
│   │   ├── paradigm.schema.yaml     #     ditto
│   │   ├── procedure.schema.yaml    #     ditto
│   │   └── agent-profile.schema.yaml #    ditto
│   ├── tactics/models.py            # Wave 3 — Pydantic model fields + cross-field validator
│   ├── styleguides/models.py        #     ditto
│   ├── paradigms/models.py          #     ditto
│   ├── procedures/models.py         #     ditto
│   ├── agent_profiles/profile.py    #     ditto
│   ├── drg/
│   │   ├── models.py                # Wave 3 — extend `Relation` enum
│   │   └── org_pack_loader.py       # Wave 3 — auto-emit ENHANCES / OVERRIDES edges
│   └── base.py                      # Wave 4 — rename `shipped` identifiers / comments
└── specify_cli/
    ├── charter_lint/
    │   ├── _drg.py                  # Wave 1 — built-in fallback loader
    │   ├── engine.py                # Wave 1 — `DecayReport.graph_state` field
    │   └── findings.py              # Wave 1 — extend DecayReport schema
    ├── charter_preflight/           # NEW package (Wave 2)
    │   ├── __init__.py
    │   ├── runner.py                # `run_charter_preflight(...)`
    │   ├── result.py                # `CharterPreflightResult` dataclass
    │   └── cli.py                   # `spec-kitty charter preflight` command surface
    ├── cli/commands/
    │   ├── charter.py               # Wave 1 + 2 — wire preflight, freshness, graph-state
    │   └── profiles_cmd.py          # Wave 4 — rename "shipped" → "built-in" in JSON
    └── doctrine/
        └── pack_validator.py        # Wave 3 — branch advisory on enhances/overrides

tests/
├── specify_cli/charter_lint/
│   └── test_engine.py               # FR-001..FR-004 coverage
├── specify_cli/doctrine/
│   └── test_pack_validator.py       # FR-013 coverage
├── specify_cli/charter_preflight/   # NEW
│   ├── test_runner.py               # FR-006..FR-008 coverage
│   └── test_cli.py
├── integration/
│   ├── test_charter_lint_lints_all_layers.py   # extend for FR-002
│   ├── test_charter_status_reports_three_layers.py # extend for FR-005
│   └── test_charter_synthesize_fresh.py        # extend for FR-009
└── architectural/
    └── test_no_shipped_layer_label.py # NEW — FR-016 surface scan

architecture/3.x/adr/
├── 2026-05-DD-1-charter-freshness-ux-contract.md         # Wave 1+2 ADR
├── 2026-05-DD-2-pack-augmentation-vocabulary.md          # Wave 3 ADR
└── 2026-05-DD-3-shipped-to-built-in-cutover.md           # Wave 4 ADR (follow-up to 2026-05-16-1)
```

**Structure decision**: Single-project layout. New `charter_preflight` package follows the existing pattern of `charter_lint` (sibling package with `engine.py` / `result.py` / `cli.py` triad). Vocabulary rename touches existing modules in place; no new top-level packages introduced for the rename.

## Phase 0 — Research findings

See `research.md` for the full version. Summary of decisions:

| Decision | Choice | Rationale |
|---|---|---|
| Field name | `enhances` (not `augments`) | Matches canonical text in issue #1291; consistent with future-glossary entry. |
| `Relation` enum policy | Add `ENHANCES = "enhances"` and `OVERRIDES = "overrides"` as new values; **keep** `REPLACES = "replaces"` for backward compatibility | Zero migration cost for existing DRG fragments; explicit alias on `OVERRIDES` is unnecessary because the new declarative field is what drives auto-emit. |
| Vocabulary cutover style | Straight cutover with CHANGELOG breaking-change note | Pre-3.2.0 stable; deprecation window adds maintenance overhead without consumer benefit. |
| Preflight invocation scope | Manual `spec-kitty charter preflight` command + opt-in hook from `next`, `implement`, dashboard launch | Avoids overhead on every CLI invocation while still catching the launch-blocker scenarios. |
| Bulk-edit gate format | Standard `occurrence_map.yaml` with all 8 categories | The skill is binding for `change_mode: bulk_edit`. |

## Phase 1 — Design outputs

See:
- `data-model.md` for new model fields, freshness state shape, and DRG enum extension.
- `contracts/charter-status-json.md`, `contracts/charter-lint-json.md`, `contracts/charter-preflight-json.md`, `contracts/pack-validator-advisory.md`.
- `quickstart.md` for the operator-facing smoke flow.
- `occurrence_map.yaml` for the `shipped → built-in` rename classification.

## Implementation waves (dependency-ordered)

These waves map to dependency clusters in the work-package graph. Tasks within a wave can be parallelised; waves themselves are sequential because of shared file ownership.

### Wave 1 — Charter freshness instrumentation (FR-001..FR-005, FR-009)
Shared file: `src/specify_cli/cli/commands/charter.py`, `src/specify_cli/charter_lint/`.
Outputs: `DecayReport.graph_state`, `built_in_only` synthesizer marker, status freshness payload.

### Wave 2 — Preflight (FR-006..FR-008)
Adds new `src/specify_cli/charter_preflight/` package; consumes Wave 1 freshness payload. Wires hooks into `next`/`implement`/dashboard entry points.

### Wave 3 — Pack-authoring vocabulary (FR-010..FR-014)
Schema additions across 5 artifact kinds; Pydantic model changes + cross-field validator; `Relation` enum extension; pack validator advisory branch logic; DRG auto-emit. Shares the `doctrine` package — no overlap with Wave 1/2 file set, so can begin in parallel with Wave 2 once Wave 1 lands.

### Wave 4 — Vocabulary cutover (FR-015..FR-017)
Last wave because it touches the broadest file set. Driven by `occurrence_map.yaml` from Phase 1. Includes the architectural regression test FR-016 and the CHANGELOG entry FR-017. Sequencing after Wave 3 ensures the validator advisory text changes from Wave 3 land in the new vocabulary.

### Cross-cutting (every wave)
- ADR landed alongside the wave's first WP (Phase 1 lists 3 ADRs).
- HiC issue assignment on first WP touching each linked GitHub issue (DIR-012).
- Bulk-edit gate active throughout Wave 4 — every commit in Wave 4 must trace to a row in `occurrence_map.yaml`.

## Complexity Tracking

*No charter violations require justification.* The Complexity Tracking table is intentionally empty.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|

## Branch contract (final restatement)

- **Current branch at plan time**: `main`
- **Planning / base branch**: `main`
- **Final merge target**: `main`
- `branch_matches_target`: **true**

This mission lands on `main`. There is no intermediate integration branch.

## Next step

Run `/spec-kitty.tasks` to decompose this plan into work packages.

⚠️ DO NOT proceed to tasks generation inside this command. The user invokes `/spec-kitty.tasks` separately.
