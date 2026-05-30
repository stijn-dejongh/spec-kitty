# Research: Charter Doctrine Mission-Type Configuration

**Mission**: `charter-doctrine-mission-type-configuration-01KSWJVX`
**Date**: 2026-05-30
**Phase**: Plan research

---

## Research Task 1 — Frozenset deletion impact analysis

### Decision
All frozenset call sites can be deleted and replaced by a single `charter.resolve_action_sequence(mission_type, repo_root)` call. No callers outside `runtime_bridge.py` and `decision.py` need individual updating.

### Findings

**`_COMPOSED_ACTIONS_BY_MISSION`** (in `src/specify_cli/next/runtime_bridge.py`) has three call sites:

| Line | Context | Replacement |
|---|---|---|
| 876 | `_should_dispatch_via_composition()` — checks if `(mission, step_id)` routes through composition | Check against `charter.resolve_action_sequence(mission, repo_root)` |
| 988 | Inline check: `if action in _COMPOSED_ACTIONS_BY_MISSION.get(mission, frozenset())` | Same live lookup |
| 2090 | `_should_dispatch_via_composition()` called from dispatch hot path | Covered by replacing the function |

**`_COMPOSED_ACTIONS_FOR_PROMPT`** (in `src/specify_cli/next/decision.py`) has one call site:

| Line | Context | Replacement |
|---|---|---|
| 573 | `if wp_id is None and action in _COMPOSED_ACTIONS_FOR_PROMPT.get(mission_type, frozenset())` | Check against `charter.resolve_action_sequence(mission_type, repo_root)` |

Both tables share identical content by design ("must stay in sync" per the comment at line 532). After deletion, `charter.resolve_action_sequence()` is the single source of truth.

**Note on `_should_dispatch_via_composition`**: This function currently uses `_COMPOSED_ACTIONS_BY_MISSION` as a fast path (avoids loading the frozen template). After the change, the fast path becomes a `charter.resolve_action_sequence()` call that reads from the doctrine layer (disk-backed). The NFR-001 ≤100ms budget must be verified in the ATDD suite; caching at the charter layer is the mitigation if cold-start regresses.

### Rationale
Keeping two separate frozensets in sync was the original technical debt. The live lookup is the correct design; performance risk is bounded and measurable.

---

## Research Task 2 — `MissionTypeProfile.mission_type` Literal removal

### Decision
Open `mission_type` from `Literal["software-dev", "documentation", "research", "plan"]` to `str`. Validation against the activation list moves to call-time (`charter.existing_mission_types()`), not model-construction time.

### Findings

Consumers of `MissionTypeProfile.mission_type` found in `src/charter/mission_type_profiles.py`:
- `load_profile(mission_type)` — used for directory routing to `src/doctrine/missions/<mission_type>/`. This function becomes data-driven: the directory must exist, not be in a hard-coded set.
- `resolve_mission_type_governance(repo_root, feature_dir)` — calls `load_profile()`, then raises `UnknownMissionTypeError` when profile is None. After the change, `None` means "not in doctrine layer at all", which is a genuine error; the check becomes: if `mission_type not in charter.existing_mission_types(repo_root)`.
- `GovernancePayload.mission_type: str` — already `str`, no change needed.
- `UnknownMissionTypeError` — already exists with the right semantics; just needs the `registered_ids` list added to its message (FR-009).

**No discriminated unions found** using `MissionTypeProfile.mission_type` as discriminator. The `Literal` field was purely defensive; removing it is safe.

### Rationale
Opening to `str` defers validation to the charter's activation list, which is the correct authority per FR-009 and C-004.

---

## Research Task 3 — `mission_step_contracts` consolidation scope

### Decision
`doctrine/mission_step_contracts/` is the fragmented subpackage to supersede. After consolidation, all callers route through the unified `MissionStep` model in `doctrine/missions/models.py`. The `specify_cli/mission_step_contracts/` subpackage is a separate, execution-layer package and is **not** in scope for deletion in this mission.

### Findings

**`doctrine/mission_step_contracts/`** (doctrine domain, in scope):
- `models.py` — duplicate `MissionStep` Pydantic model; superseded by the unified model.
- `repository.py` — `MissionStepContractRepository`; callers:
  - `src/doctrine/artifact_kinds.py` — references `mission_step_contracts` as an artifact kind
  - `src/doctrine/service.py` — loads `mission_step_contracts` via DRG
  - `src/doctrine/drg/org_pack_loader.py` — `_ORG_DRG_CANONICAL_KINDS` includes `mission_step_contracts`
  - `src/specify_cli/doctrine/pack_assembler.py`, `pack_validator.py`, `snapshot.py` — pack assembly
  - `src/charter/schemas.py`, `mission_steps.py`, `activations.py`, `context.py`, `drg.py` — charter consumers

**`specify_cli/mission_step_contracts/`** (execution layer, NOT in scope):
- This is a distinct execution-layer concept (`MissionStepContractExecutor`, etc.) unrelated to the doctrine artifact model. Do not delete.

**Consolidation approach**: The unified `MissionStep` model replaces `doctrine.mission_step_contracts.models.MissionStep`. The `doctrine/mission_step_contracts/repository.py` is migrated to read from the new `mission-steps/` directory structure. The kind key `mission_step_contracts` in `_ORG_DRG_CANONICAL_KINDS` may be renamed to `mission_steps` (breaking change — defer to plan note; keep old key as alias for one release).

### Rationale
The dual-model fragmentation was introduced by separate mission slices. Consolidation is the stated goal in FR-011.

---

## Research Task 4 — Upgrade migration version slot

### Decision
The new migration is named `m_3_2_7_activate_builtin_mission_types.py`, following the `m_3_2_6_charter_bundle_v2.py` pattern.

### Findings

Latest migrations in `src/specify_cli/upgrade/migrations/`:
- `m_3_2_4_repository_root_checkout_terminology.py`
- `m_3_2_5_fix_prompt_file_workaround.py`
- `m_3_2_6_charter_bundle_v2.py`

Next slot: `m_3_2_7`. Migration must use `get_agent_dirs_for_project()` from `m_0_9_1_complete_lane_migration.py` for config-aware agent directory handling, per CLAUDE.md.

### Rationale
Monotonic migration numbering is the established convention.

---

## Research Task 5 — Template deployment pipeline

### Decision
The deployment pipeline reads prompt templates from a **configurable source path** inside the migration. After FR-010, the source is `src/doctrine/missions/mission-steps/{mission_type}/{step_id}/prompt.md`. The installer logic in `src/specify_cli/skills/command_installer.py` (mission 083) and the migration `m_3_2_5_fix_prompt_file_workaround.py` are the relevant callers.

### Findings

Agent command files are generated by:
1. `src/specify_cli/skills/command_renderer.py` — renders source templates into agent-skills format
2. `src/specify_cli/skills/command_installer.py` — installs/removes skill packages
3. Upgrade migrations that call `get_agent_dirs_for_project()` and write to agent directories

The `src/specify_cli/missions/software-dev/command-templates/` path is the current source. After FR-010:
- The new source is `src/doctrine/missions/mission-steps/<mission_type>/<step_id>/prompt.md`
- `command_renderer.py` must be updated to read from the new path
- The template deployment migration (`m_3_2_7`) must copy from the new path
- `CLAUDE.md`'s "Template Source Location" table row must be updated

### Rationale
The deployment pipeline is already abstracted behind `command_renderer.py`; the path change is localized.

---

## Alternatives considered

| Decision | Alternative | Rejected because |
|---|---|---|
| Single YAML descriptor + adjacent Markdown (B) for MissionStep on-disk | Single YAML with embedded Markdown content (A) | Large Markdown blobs buried in YAML degrade diff readability and IDE navigation; the existing `actions/{id}/guidelines.md` pattern proves the split is practical |
| Directory-per-step (`{step_id}/step.yaml + prompt.md`) | Flat `{step_id}.yaml` only | User preference: "easier to find related artefacts"; consistent with `actions/` convention already in `src/doctrine/missions/software-dev/actions/` |
| P1 + P2 in one mission | P1 only, P2 follow-on | User chose combined delivery; P2 CLI surfaces are thin wrappers over the P1 resolver, not additional risk |
