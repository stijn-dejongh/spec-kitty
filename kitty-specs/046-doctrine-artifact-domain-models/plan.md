# Implementation Plan: Doctrine Artifact Domain Models

**Branch**: `feature/agent-profile-implementation` | **Date**: 2026-02-25 | **Updated**: 2026-02-27 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `kitty-specs/046-doctrine-artifact-domain-models/spec.md`

## Summary

Create Pydantic domain models and repository services for 5 doctrine artifact types (directives, tactics, styleguides, toolguides, paradigms) following the established `agent_profiles` pattern, plus a `DoctrineService` aggregation point. Enrich all 19 existing shipped directives and create new directives from the `doctrine_ref` reference corpus. All implementation WPs follow ATDD/TDD methodology.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: pydantic>=2.0, ruamel.yaml>=0.18.0, jsonschema>=4.0 (existing doctrine package deps)
**Storage**: Filesystem (YAML files in `src/doctrine/` subpackages)
**Testing**: pytest with ATDD/TDD — acceptance tests first, then unit tests
**Target Platform**: Cross-platform (Linux, macOS, Windows 10+)
**Project Type**: Single Python package (`spec-kitty-doctrine`)
**Constraints**: All models must use kebab-case YAML aliases; backward-compatible schema evolution; no new external dependencies

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Gate | Status | Notes |
|------|--------|-------|
| Python 3.11+ | Pass | Existing requirement; no change |
| Testing (pytest, 90%+ coverage) | Pass | ATDD/TDD enforced per all WPs |
| mypy --strict | Pass | Pydantic models support strict typing |
| Cross-platform | Pass | Pure Python, filesystem-only |
| No new dependencies | Pass | Using existing pydantic, ruamel.yaml, jsonschema |

No constitution violations.

## Project Structure

### Documentation (this feature)

```
kitty-specs/046-doctrine-artifact-domain-models/
├── plan.md              # This file
├── spec.md              # Feature specification
├── meta.json            # Feature metadata
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
└── checklists/
    └── requirements.md  # Spec quality checklist
```

### Source Code (repository root)

```
src/doctrine/
├── __init__.py              # Package root (currently empty)
├── service.py               # NEW: DoctrineService aggregation point
├── agent_profiles/          # EXISTING: No changes to public API
│   ├── __init__.py
│   ├── profile.py
│   ├── repository.py
│   ├── validation.py
│   ├── capabilities.py
│   └── shipped/             # 7 shipped agent profiles
├── directives/              # NEW: Subpackage (currently just YAML files)
│   ├── __init__.py          # NEW: Exports Directive, DirectiveRepository
│   ├── models.py            # NEW: Directive Pydantic model (includes enrichment fields)
│   ├── repository.py        # NEW: DirectiveRepository
│   ├── validation.py        # NEW: Schema validation utility
│   └── shipped/             # MOVED+ENRICHED: directive YAML files
├── tactics/                 # NEW: Subpackage (currently just YAML files)
│   ├── __init__.py          # NEW: Exports Tactic, TacticRepository
│   ├── models.py            # NEW: Tactic, TacticStep models
│   ├── repository.py        # NEW: TacticRepository
│   ├── validation.py        # NEW: Schema validation utility
│   └── shipped/             # MOVED: tactic YAML files
├── styleguides/             # NEW: Subpackage (currently just YAML files + README)
│   ├── __init__.py          # NEW: Exports Styleguide, StyleguideRepository
│   ├── models.py            # NEW: Styleguide, AntiPattern models
│   ├── repository.py        # NEW: StyleguideRepository
│   ├── validation.py        # NEW: Schema validation utility
│   └── shipped/             # MOVED: styleguide YAML files (including writing/)
├── toolguides/              # NEW: Subpackage (currently just YAML + MD files)
│   ├── __init__.py          # NEW: Exports Toolguide, ToolguideRepository
│   ├── models.py            # NEW: Toolguide model
│   ├── repository.py        # NEW: ToolguideRepository
│   ├── validation.py        # NEW: Schema validation utility
│   └── shipped/             # MOVED: toolguide YAML files + companion MD
├── paradigms/               # NEW: Subpackage (currently just YAML files)
│   ├── __init__.py          # NEW: Exports Paradigm, ParadigmRepository
│   ├── models.py            # NEW: Paradigm model
│   ├── repository.py        # NEW: ParadigmRepository
│   ├── validation.py        # NEW: Schema validation utility
│   └── shipped/             # MOVED: paradigm YAML files
├── schemas/                 # EXISTING: Extended
│   ├── directive.schema.yaml  # UPDATED: New optional fields, additionalProperties removed
│   ├── paradigm.schema.yaml   # NEW: Formal schema for paradigms
│   └── ...                    # Existing schemas unchanged
├── curation/                # EXISTING: No changes
├── missions/                # EXISTING: No changes
└── templates/               # EXISTING: No changes

tests/doctrine/
├── directives/
│   ├── test_models.py       # NEW: Directive model tests (minimal + enriched)
│   ├── test_repository.py   # NEW: DirectiveRepository tests
│   └── test_validation.py   # NEW: Schema validation tests (backward compat + enriched)
├── tactics/
│   ├── test_models.py       # NEW
│   └── test_repository.py   # NEW
├── styleguides/
│   ├── test_models.py       # NEW
│   └── test_repository.py   # NEW
├── toolguides/
│   ├── test_models.py       # NEW
│   └── test_repository.py   # NEW
├── paradigms/
│   ├── test_models.py       # NEW
│   └── test_repository.py   # NEW
├── test_service.py              # NEW: DoctrineService tests
├── test_directive_consistency.py  # UPDATED: Extended with tactic_ref resolution tests
└── test_enriched_directives.py    # NEW: Enriched directive content tests
```

**Structure Decision**: Uniform subpackage per artifact type. Each gets `__init__.py`, `models.py`, `repository.py`, `validation.py` mirroring `agent_profiles/`. Shipped YAML files move into `shipped/` subdirectories within each subpackage (currently they sit loose in the type directories). The `DoctrineService` lives at `src/doctrine/service.py` as it orchestrates across subpackages.

## Key Design Decisions

### DD-001: YAML Files Move into `shipped/` Subdirectories

Currently, directive YAML files sit directly in `src/doctrine/directives/`. When converting to a Python subpackage (adding `__init__.py`, `models.py`, etc.), the YAML files move into `shipped/` — matching the `agent_profiles/shipped/` pattern. This separates package code from data files.

**Each WP that moves files is responsible for updating any existing tests that reference the old paths.** This ensures every WP stays independently green — no dangling test failures between phases.

### DD-002: Pure YAML with Multiline Strings for Enriched Directives

Enriched directives use pure YAML with multiline string fields (`|` block scalar) for sections like `scope`, `procedures`, `integrity_rules`, and `validation_criteria`. No markdown body or companion files. This keeps everything model-parseable while allowing rich prose content.

Example enriched directive structure:
```yaml
schema_version: "1.0"
id: DIRECTIVE_004
title: Test-Driven Implementation Standard
intent: |
  Ensure all code changes are accompanied by tests that verify the intended
  behavior. Tests serve as executable specification and living documentation.
enforcement: required
scope: |
  Applies to all features, bug fixes, and refactors that alter externally
  observable behavior. Exception: trivial one-off scripts (document exception
  rationale in work log per Directive 014).
tactic_refs:
  - acceptance-test-first
  - tdd-red-green-refactor
  - zombies-tdd
procedures:
  - Capture behavior as an acceptance test before coding
  - Reference scenario ID inside test metadata
  - Keep acceptance tests close to real workflows
  - Delegate detailed work to TDD cycles once acceptance tests fail
integrity_rules:
  - Failing acceptance test must exist before implementation begins
  - Acceptance tests must include clear Arrange/Act/Assert narrative
validation_criteria:
  - All new code has corresponding test coverage
  - Tests pass in CI before merge
  - Test names describe the behavior being verified
```

### DD-003: Paradigm Schema Created

No `paradigm.schema.yaml` currently exists. A minimal schema is created to formalize the existing structure (`schema_version`, `id`, `name`, `summary`) and enable validation.

### DD-004: Repository Base Pattern

All 5 new repositories share the same structural pattern from `AgentProfileRepository`:
- `__init__(shipped_dir, project_dir)` with `importlib.resources` default
- `_load()` scans `*.{type}.yaml` with warning on malformed files
- `list_all()`, `get(id)`, `save(model)` public API
- Field-level merge for project overrides

Domain-specific methods (hierarchy traversal, weighted matching) are NOT added to the new repositories — those are agent-profile-specific concerns.

### DD-005: DoctrineService as Lazy Aggregation Point

`DoctrineService` instantiates repositories lazily (on first attribute access) to avoid loading all artifact types when only one is needed. This supports the on-demand loading principle.

### DD-006: Directive ID Lookup Normalization

Directive IDs use `SCREAMING_SNAKE_CASE` (e.g., `DIRECTIVE_004`), but consumers may look up by numeric shorthand (e.g., `"004"`). The `DirectiveRepository.get()` method accepts both forms and normalizes internally.

### DD-007: New Directives from doctrine_ref

New shipped directives are created for `doctrine_ref` concepts not yet represented. The numbering continues from 020 onward. Each new directive uses the enriched format from the start. The `doctrine_ref` content is adapted to fit the YAML schema structure, not copied verbatim.

### DD-008: Directive Schema Extension is Atomic with Model Creation

The directive schema's `additionalProperties: false` blocks enrichment fields. Rather than treating schema extension as a separate work package with a dependency on WP01, the schema update, model creation (including enrichment fields), and file move are done together in WP01. This eliminates the gap where enriched directives cannot validate and ensures the directive subpackage is fully ready for enrichment work from the start.

### DD-009: Existing Tests Updated Per-WP (No Red-Between-Phases)

Each WP that moves YAML files into `shipped/` is responsible for updating any existing tests that reference the old paths. Affected test files:
- `test_directive_consistency.py` — references `src/doctrine/directives/*.directive.yaml` (updated in WP01)
- `test_tactic_compliance.py` — references `src/doctrine/tactics/*.tactic.yaml` (updated in WP02)
- `test_artifact_compliance.py` — references directive, styleguide, toolguide, tactic paths (updated in WP01-WP04 respectively; each WP updates only its own artifact type's path entries)

This ensures the test suite stays green after every WP merge, not just after a cleanup phase.

## Existing Test Files Affected by File Relocation

The following existing test files reference doctrine artifact paths that will change when YAML files move into `shipped/` subdirectories. Each WP must update the paths for its own artifact type:

| Test File | Current Path Pattern | Affected Artifact Types |
|-----------|---------------------|------------------------|
| `tests/doctrine/test_directive_consistency.py` | `DOCTRINE_DIR / "directives"` + `*.directive.yaml` | Directives (WP01) |
| `tests/doctrine/test_tactic_compliance.py` | `TACTICS_DIR` + `*.tactic.yaml`, also `ARTIFACT_DIRS` dict | Tactics, plus cross-refs to directives/styleguides/toolguides (WP02, update `ARTIFACT_DIRS` for all moved types) |
| `tests/doctrine/test_artifact_compliance.py` | `DOCTRINE_DIR / "directives"`, `"tactics"`, `"styleguides"`, `"toolguides"` | All four types (each WP updates its own entries) |

**Strategy for `test_tactic_compliance.py`**: This file has an `ARTIFACT_DIRS` dict mapping artifact types to `(directory, glob)` tuples. As each WP moves files, it updates the corresponding entry. WP01 updates the `"directive"` entry, WP02 updates `"tactic"`, WP03 updates `"styleguide"`, WP04 updates `"toolguide"`.

## Complexity Tracking

No constitution violations — no entries needed.
