---
work_package_id: WP01
title: Unify MissionStep model + migrate callers
dependencies: []
requirement_refs:
- FR-011
tracker_refs: []
planning_base_branch: feat/doctrine-mission-type-spec-01KSWJVX
merge_target_branch: feat/doctrine-mission-type-spec-01KSWJVX
branch_strategy: feature-branch
subtasks:
- T001
- T002
- T003
- T004
- T005
- T006
- T007
- T008
- T009
agent: claude
history:
- at: '2026-05-30T17:21:57Z'
  event: created
  note: Initial task breakdown
agent_profile: python-pedro
authoritative_surface: src/doctrine/missions/models.py
execution_mode: code_change
owned_files:
- src/doctrine/missions/models.py
- src/doctrine/mission_step_contracts/
- src/doctrine/artifact_kinds.py
- src/doctrine/service.py
- src/doctrine/drg/org_pack_loader.py
- src/specify_cli/doctrine/pack_assembler.py
- src/specify_cli/doctrine/pack_validator.py
- src/specify_cli/doctrine/snapshot.py
- src/charter/schemas.py
- src/charter/mission_steps.py
- src/charter/activations.py
- src/charter/context.py
- src/charter/drg.py
- tests/doctrine/missions/test_models.py
- tests/architectural/test_layer_rules.py
role: implementer
tags: []
---

## ⚡ Do This First: Load Agent Profile

Before reading anything else, load your agent profile:

/ad-hoc-profile-load python-pedro

This profile contains the coding standards, testing requirements, and
architectural constraints you must follow throughout this work package.

---

# Work Package Prompt: WP01 — Unify MissionStep model + migrate callers

## Context

The codebase currently has two Pydantic classes both named `MissionStep` in separate doctrine subpackages:

- `doctrine.missions.models.MissionStep` — schema-validation shape for `mission.yaml`
- `doctrine.mission_step_contracts.models.MissionStep` — governance-delegation shape for step contracts

These are fragmented manifestations of a single concept, split by evolutionary accident. This WP consolidates them into one canonical `MissionStep` model — an entity owned by `MissionType`, globally identified by `(mission_type_id, step_id)`. All callers of either legacy class are migrated; the `doctrine/mission_step_contracts/` subpackage is then deleted.

**Critical boundary**: `specify_cli/mission_step_contracts/` is a separate execution-layer package — do NOT delete it.

## Objective

Produce a single, unified `MissionStep` Pydantic model in `src/doctrine/missions/models.py` with the `step_type` discriminant field, migrate all callers, delete the fragmented `doctrine/mission_step_contracts/` subpackage, and extend the architectural boundary test.

## Subtasks

### T001 — Audit existing MissionStep models

Read both files:
- `src/doctrine/missions/models.py` — find the existing `MissionStep` class definition; document all fields
- `src/doctrine/mission_step_contracts/models.py` — find the duplicate `MissionStep` class; document all fields

Also read `src/doctrine/mission_step_contracts/repository.py` to understand `MissionStepContractRepository`.

Produce a field-diff table (fields unique to each, fields shared). This drives the unified model design.

### T002 — Author unified MissionStep Pydantic model

In `src/doctrine/missions/models.py`, consolidate into a single `MissionStep` class with ALL of these fields:

```python
class MissionStep(BaseModel):
    id: str                              # validated by IDENTIFIER_PATTERN
    display_name: str
    step_type: Literal["agent", "human_in_loop", "integration"]
    prompt_template: str                 # relative path to Markdown file
    agent_profile: str | None = None
    guidance: str | None = None
    delegates_to: list[str] = Field(default_factory=list)
    depends_on: list[str] = Field(default_factory=list)
```

`step_type` is the executor discriminant:
- `agent` → `Decision.kind = step` (prompt dispatched to LLM)
- `human_in_loop` → `Decision.kind = decision_required`
- `integration` → `Decision.kind = blocked` (reserved; no providers in this release)

The unified model supersedes BOTH legacy classes. All fields from both legacy models must be preserved or intentionally deprecated with rationale.

### T003 — Add IDENTIFIER_PATTERN and __all__

`MissionStep.id` must be validated by `IDENTIFIER_PATTERN` (ASCII kebab-case, per C-003). Reuse or define the pattern at the module level.

Add `__all__` declaration listing all public symbols (C-007).

### T004 — Migrate doctrine/ callers

Migrate these files to import from `doctrine.missions.models.MissionStep` instead of `doctrine.mission_step_contracts.*`:
- `src/doctrine/artifact_kinds.py` — update `mission_step_contracts` artifact kind reference
- `src/doctrine/service.py` — update DRG loading call
- `src/doctrine/drg/org_pack_loader.py` — update `_ORG_DRG_CANONICAL_KINDS`; keep `mission_step_contracts` as alias for one release (do NOT rename outright)

### T005 — Migrate specify_cli/ callers

Migrate these files to the unified model:
- `src/specify_cli/doctrine/pack_assembler.py`
- `src/specify_cli/doctrine/pack_validator.py`
- `src/specify_cli/doctrine/snapshot.py`

Do not change any functionality — only update the import paths and model references.

### T006 — Migrate charter/ callers

Migrate these charter-layer files to the unified model:
- `src/charter/schemas.py`
- `src/charter/mission_steps.py`
- `src/charter/activations.py`
- `src/charter/context.py`
- `src/charter/drg.py`

Respect C-004: `charter.*` may import from `doctrine.*`; confirm you are not adding `specify_cli.*` → `doctrine.*` imports.

### T007 — Delete doctrine/mission_step_contracts/ subpackage

After all callers are migrated:
1. Verify zero references remain to `doctrine.mission_step_contracts` (use `grep -r` or equivalent)
2. Delete `src/doctrine/mission_step_contracts/` directory entirely
3. **DO NOT touch** `src/specify_cli/mission_step_contracts/` — this is a separate execution-layer package

### T008 — Extend architectural boundary test

In `tests/architectural/test_layer_rules.py`, add or update the test that verifies:
- `specify_cli.*` does not import from `doctrine.*` directly (C-004)
- `doctrine.*` does not import from `charter.*` or `specify_cli.*`

The test should fail if any new cross-boundary import is introduced.

### T009 — Unit tests for unified MissionStep model

Write tests in `tests/doctrine/missions/test_models.py` covering:
- Valid `step_type` values: `agent`, `human_in_loop`, `integration`
- Invalid `step_type` raises `ValidationError`
- `id` rejected when it does not match `IDENTIFIER_PATTERN` (e.g., spaces, capitals)
- Valid `id` accepted (e.g., `specify`, `plan-tasks`, `exec-summary`)
- Default field values (`delegates_to`, `depends_on` default to empty lists)
- Optional fields can be `None`

## Acceptance Criteria

- [ ] `doctrine/mission_step_contracts/` directory is gone; `specify_cli/mission_step_contracts/` is untouched
- [ ] `grep -r "from doctrine.mission_step_contracts" src/` returns no results
- [ ] Unified `MissionStep` model in `doctrine/missions/models.py` has all required fields
- [ ] `__all__` declared in `doctrine/missions/models.py`
- [ ] All doctests + unit tests pass: `cd src && pytest tests/doctrine/missions/test_models.py`
- [ ] `tests/architectural/test_layer_rules.py` passes with the new boundary assertions
- [ ] `mypy --strict src/doctrine/missions/models.py` clean

## References

- FR-011: Unified MissionStep model specification
- spec.md §"Assumptions" — fragmentation background
- data-model.md §"MissionStep (unified)" — field specification
- `tests/architectural/test_layer_rules.py` — boundary enforcement pattern
