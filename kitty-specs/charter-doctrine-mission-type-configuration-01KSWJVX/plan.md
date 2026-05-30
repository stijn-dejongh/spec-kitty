# Implementation Plan: Charter Doctrine Mission-Type Configuration

**Branch**: `feat/doctrine-mission-type-spec-01KSWJVX` | **Date**: 2026-05-30 | **Spec**: [spec.md](spec.md)
**Input**: `kitty-specs/charter-doctrine-mission-type-configuration-01KSWJVX/spec.md`

---

## Summary

Replace hardcoded mission-type dispatch (two frozenset tables in `runtime_bridge.py` and
`decision.py`) with a live, charter-mediated resolution chain through
`src/charter/` → `src/doctrine/`. Introduce `MissionType` and unified `MissionStep` as
first-class doctrine artifacts with a directory-per-step on-disk layout. Add `extends:`
to `OrgCharterPolicy` for hierarchical pack composition. Make DRG traversal
activation-filtered. Deliver P1 (core infrastructure) and P2 (CLI enumeration surfaces)
in one sprint.

---

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: Pydantic v2, ruamel.yaml, typer, rich — all existing; no new external packages
**Storage**: Filesystem only — YAML descriptors, Markdown templates, `.kittify/` config and charter files
**Testing**: pytest with mypy --strict; ATDD suite in `tests/`; architectural boundary tests in `tests/architectural/test_layer_rules.py`
**Target Platform**: Cross-platform (Linux, macOS, Windows 10+) — DIR-001
**Project Type**: Single Python package (`src/specify_cli` + `src/charter` + `src/doctrine`)
**Performance Goals**: `spec-kitty next` cold-start overhead ≤100 ms for built-in-only projects (NFR-001)
**Constraints**: No direct `doctrine.*` imports from `specify_cli.*`; charter is the only ACL (C-004); `doctrine.*` must not import `charter.*` or `specify_cli.*`

---

## Charter Check

- **DIR-005** Tests added for new functionality — resolved: each WP includes test coverage per acceptance criteria.
- **DIR-006** Type annotations (mypy --strict) — resolved: all new models and functions carry full annotations.
- **DIR-007** Docstrings for public APIs — resolved: `__all__` on every new public module (C-007).
- **DIR-010/DIR-011** Identifier sanitisation — resolved: `IDENTIFIER_PATTERN` in `doctrine/missions/models.py` enforces C-003 for mission-type IDs.
- **DIR-012** Tracker assignment — the implementing agent must assign the relevant GitHub issues (#1397, #1333, #682, #883) to the HiC before beginning implementation.
- **C-004** Architectural boundary — enforced by `tests/architectural/test_layer_rules.py`; no new cross-boundary imports may be introduced.
- **C-007** `__all__` convention — all new public modules must declare `__all__`.
- **C-011** ATDD-First Discipline — GWT contracts in `contracts/` serve as the ATDD acceptance surface; tests must be authored before or alongside implementation.

---

## Project Structure

### Documentation (this feature)

```
kitty-specs/charter-doctrine-mission-type-configuration-01KSWJVX/
├── plan.md              ← this file
├── research.md          ← Phase 0 output
├── data-model.md        ← Phase 1 output
├── quickstart.md        ← Phase 1 output
├── contracts/           ← 7 contract files (2 existing + 5 new GWT files)
└── tasks.md             ← Phase 2 output (/spec-kitty.tasks — not created here)
```

### Source Code (repository root)

```
src/
├── doctrine/
│   └── missions/
│       ├── models.py                    ← unified MissionStep Pydantic model (modify)
│       ├── mission-steps/               ← NEW: built-in step artifacts
│       │   ├── software-dev/
│       │   │   ├── specify/
│       │   │   │   ├── step.yaml        ← MissionStep descriptor
│       │   │   │   ├── prompt.md        ← verbatim moved command-template
│       │   │   │   └── guidelines.md    ← optional guidance
│       │   │   ├── plan/ …
│       │   │   ├── tasks/ …
│       │   │   ├── implement/ …
│       │   │   └── review/ …
│       │   ├── documentation/ …
│       │   ├── research/ …
│       │   └── plan/ …
│       └── mission_types/               ← NEW: built-in MissionType YAML definitions
│           ├── software-dev.yaml
│           ├── documentation.yaml
│           ├── research.yaml
│           └── plan.yaml
│   └── drg/
│       └── org_pack_loader.py           ← add extends: chain resolution (modify)
│
├── charter/
│   ├── mission_type_profiles.py         ← open Literal→str; add existing_mission_types(),
│   │                                       resolve_action_sequence() (modify)
│   └── mission_steps.py                 ← wire to new doctrine mission-steps layer (modify)
│
└── specify_cli/
    ├── doctrine/
    │   └── org_charter.py               ← OrgCharterPolicy gets extends: field (modify)
    ├── next/
    │   ├── runtime_bridge.py            ← delete _COMPOSED_ACTIONS_BY_MISSION (modify)
    │   └── decision.py                  ← delete _COMPOSED_ACTIONS_FOR_PROMPT (modify)
    ├── upgrade/migrations/
    │   └── m_<version>_activate_builtin_mission_types.py  ← NEW: FR-019 migration
    └── cli/commands/
        ├── doctrine.py                  ← NEW: spec-kitty doctrine mission-type list
        └── charter_cmd.py               ← EXTEND: spec-kitty charter mission-type list/show

tests/
├── architectural/
│   └── test_layer_rules.py              ← extend with charter→doctrine boundary
├── doctrine/
│   └── missions/
│       └── test_mission_step_resolver.py ← NEW: step shadowing, layer precedence
├── charter/
│   ├── test_mission_type_profiles.py    ← extend: dynamic types, existing_mission_types
│   └── test_action_sequence_dispatch.py ← NEW: dispatch chain contracts
├── specify_cli/
│   └── doctrine/
│       └── test_org_charter.py          ← extend: extends chain, cycle detection
└── upgrade/
    └── test_activate_builtin_types_migration.py ← NEW: FR-019 migration
```

---

## Phase 0: Research

### Research tasks

1. **Frozenset deletion impact analysis** — Trace all callers of `_COMPOSED_ACTIONS_BY_MISSION`
   (in `runtime_bridge.py`) and `_COMPOSED_ACTIONS_FOR_PROMPT` (in `decision.py`) to enumerate
   every call site that must be rewired to `charter.resolve_action_sequence()`. Confirm the
   `_build_prompt_or_error` path in `decision.py` and the `_should_dispatch_via_composition`
   function in `runtime_bridge.py` cover all cases.

2. **MissionTypeProfile.mission_type Literal removal** — The field currently uses
   `Literal["software-dev", "documentation", "research", "plan"]`. Opening to `str` may
   break Pydantic discriminated unions elsewhere. Enumerate all consumers of
   `MissionTypeProfile.mission_type` to assess impact.

3. **`mission_step_contracts` consolidation scope** — `doctrine/mission_step_contracts/models.py`
   and `doctrine/mission_step_contracts/repository.py` are the fragmented classes to be
   superseded. Confirm all callers so the consolidation WP can safely delete them.

4. **Upgrade migration version slot** — Identify the next available migration version number
   in `src/specify_cli/upgrade/migrations/` and confirm the migration registration pattern.

5. **Template deployment pipeline** — `FR-010` requires the upgrade migration pipeline
   (which generates `.claude/commands/`, `.amazonq/prompts/`, etc.) to be rewired to read
   from `src/doctrine/missions/mission-steps/`. Confirm where `get_agent_dirs_for_project()`
   is consumed and which migration/installer writes the deployed copies.

Research findings are captured in [research.md](research.md).

---

## Phase 1: Design

### Data Model

Full entity specifications are in [data-model.md](data-model.md).

**Key entities introduced or modified:**

| Entity | Location | Change |
|---|---|---|
| `MissionType` | `src/doctrine/missions/mission_types/` (new YAML) | New doctrine artifact: `id`, `display_name`, `extends?`, `action_sequence`, `governance_refs?`, `template_set?` |
| `MissionStep` (unified) | `src/doctrine/missions/models.py` | Consolidate two fragmented models; add `step_type`, `display_name`, `delegates_to?`, `guidance?`, `depends_on?` |
| `OrgCharterPolicy` | `src/specify_cli/doctrine/org_charter.py` | Add `schema_version: int`, `extends: str \| None`; chain resolver |
| `PackContext` | `src/charter/` (new dataclass) | Pre-validated pack set passed to doctrine resolver; never reads `config.yaml` directly |
| `MissionTypeProfile` | `src/charter/mission_type_profiles.py` | Open `Literal[…]` → `str`; remove at resolve-time; validated by `charter.existing_mission_types()` |

### Contracts

Contracts in `contracts/` cover all behavioral flows — see [contracts/](contracts/).

### Quickstart

End-to-end walkthrough for adding a custom mission type is in [quickstart.md](quickstart.md).

---

## Implementation Phases

### Phase A — Doctrine foundation (P1 core, no CLI changes yet)

**Prerequisite for all other phases.**

1. **Unify `MissionStep` model** in `src/doctrine/missions/models.py`. Consolidate
   `doctrine.missions.models.MissionStep` and `doctrine.mission_step_contracts.models.MissionStep`
   into a single Pydantic model with `step_type: Literal["agent", "human_in_loop", "integration"]`.
   Delete the `mission_step_contracts` subpackage after migrating all callers.

2. **Create `mission-steps/` directory structure** — Create `step.yaml` descriptors and move
   command-template Markdown files verbatim for all four built-in mission types
   (`software-dev`, `documentation`, `research`, `plan`). Delete old
   `src/specify_cli/missions/*/command-templates/` directories.

3. **Create `MissionType` YAML definitions** — Author `software-dev.yaml`, `documentation.yaml`,
   `research.yaml`, `plan.yaml` in `src/doctrine/missions/mission_types/` capturing the
   current hardcoded `action_sequence` from `_COMPOSED_ACTIONS_BY_MISSION`.

4. **`mission-step` repository** — Add `MissionStepRepository` (or extend
   `src/charter/mission_steps.py`) to resolve a step by compound key
   `(mission_type_id, step_id)` across `built-in → org → project` layers.

### Phase B — Charter API additions

5. **`charter.existing_mission_types(repo_root) → list[str]`** — New public function in
   `src/charter/mission_type_profiles.py`. Reads the project charter's activation set;
   returns only activated mission type IDs.

6. **`charter.resolve_action_sequence(mission_type_id, repo_root) → list[str]`** — New public
   function. Resolves the live action sequence for the given mission type by reading
   the `MissionType` YAML through the `built-in → org → project` DRG chain.

7. **Open `MissionTypeProfile.mission_type`** from `Literal[…]` to `str`; validate against
   `existing_mission_types()` at runtime rather than at model-validation time.

8. **`PackContext` dataclass** — New frozen dataclass in `src/charter/` encapsulating the
   pre-validated pack set. Charter constructs it; doctrine resolver receives it.

### Phase C — Wire dispatch; delete frozensets

9. **Delete `_COMPOSED_ACTIONS_BY_MISSION`** from `src/specify_cli/next/runtime_bridge.py`.
   Replace every call site with `charter.resolve_action_sequence(mission_type, repo_root)`.

10. **Delete `_COMPOSED_ACTIONS_FOR_PROMPT`** from `src/specify_cli/next/decision.py`.
    Wire `_build_prompt_or_error` to resolve the prompt template path from the doctrine
    mission-steps layer via `charter`.

11. **Template deployment migration** — Update the upgrade migration pipeline
    (`get_agent_dirs_for_project()` callers) to read prompt templates from
    `src/doctrine/missions/mission-steps/` instead of `src/specify_cli/missions/*/command-templates/`.
    Update `CLAUDE.md` "Template Source Location" section.

### Phase D — `extends:` for OrgCharterPolicy

12. **`OrgCharterPolicy.extends`** — Add optional `extends: str | None` and `schema_version: int`
    fields to the Pydantic model in `src/specify_cli/doctrine/org_charter.py`.

13. **Chain resolver** — Implement `_resolve_chain(pack_name, pack_set) → list[OrgCharterPolicy]`
    with cycle detection (`OrgCharterCycleError`) and missing-base detection
    (`OrgCharterExtensionError`). Union `required_directives`/`required_toolguides`;
    per-key merge `interview_defaults`. Schema-version mismatch raises structured error.

14. **`PackContext` wiring** — Charter reads `.kittify/config.yaml`, constructs `PackContext`,
    passes it to `load_org_charter_policies` (and `doctrine_resolver`). Resolver never
    reads `config.yaml` directly.

### Phase E — Activation-filtered DRG (FR-018)

15. **Activation filter in DRG traversal** — Before traversal, charter resolves the activation
    set from the project charter and passes it as part of `PackContext`. Doctrine resolver
    applies the filter: only activated artifacts are included in resolution results across
    all artifact kinds.

16. **FR-019 upgrade migration** — New migration activates all built-in mission types
    (`software-dev`, `documentation`, `research`, `plan`) in any existing project charter
    that does not yet have explicit mission-type activation entries.

### Phase F — CLI surfaces (P2)

17. **`spec-kitty doctrine mission-type list`** — New command under `spec-kitty doctrine`
    group. Lists all mission types discoverable in the doctrine layer (built-in + any org/project
    overrides), regardless of activation state. Output: `id`, `source_layer`, `display_name`.

18. **`spec-kitty charter mission-type list`** (alias `spec-kitty mission-type list`) — New
    command under `spec-kitty charter` group. Lists only activated mission types for the
    current project. Output: `id`, `source_layer`, `display_name`, `action_sequence`.

19. **`spec-kitty mission-type show <id>`** — Renders the fully resolved mission-type
    definition (merged across all layers) for the current project: `action_sequence`,
    `governance_refs`, `template_set`, source layer per field.

### Phase G — `spec-kitty charter activate` warning (FR-008 tail)

20. **In-flight lane warning** — When `spec-kitty charter activate` loads an override that
    removes a step ID, check all in-flight missions for any in the corresponding lane. Emit
    a structured warning per affected mission before completing activation.

---

## Complexity Tracking

No Charter Check violations. All phases are additive; the frozenset deletion (Phase C) is
the only breaking change, isolated to two files with a clear call-graph boundary.

---

## Risks

| Risk | Mitigation |
|---|---|
| Frozenset deletion breaks in-flight missions that depend on `_COMPOSED_ACTIONS_BY_MISSION` fast path | Architectural test + ATDD contract B in `action-sequence-dispatch-contract.md` must pass before merge; NFR-002 zero-regression gate |
| `MissionTypeProfile.mission_type` open-`str` change breaks Pydantic discriminated unions | Phase 0 research task #2 enumerates all consumers before the change is made |
| Template deployment pipeline silently stops generating agent commands | NFR-004 gate: deploy test must verify `.claude/commands/specify.md` renders from new doctrine path |
| `extends:` chain resolution is O(n) per resolve call | Depth is bounded in practice (≤3 packs typical); NFR-001 ≤100ms gate covers this |
| `mission_step_contracts` callers missed during consolidation | Phase 0 research task #3 + `rg -r doctrine.mission_step_contracts` over test suite before deletion |
