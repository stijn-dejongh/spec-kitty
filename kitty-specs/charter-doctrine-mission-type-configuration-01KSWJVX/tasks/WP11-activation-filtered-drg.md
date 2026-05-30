---
work_package_id: WP11
title: Activation-filtered DRG traversal
dependencies:
- WP06
- WP10
requirement_refs:
- FR-006
- FR-018
tracker_refs: []
planning_base_branch: feat/doctrine-mission-type-spec-01KSWJVX
merge_target_branch: feat/doctrine-mission-type-spec-01KSWJVX
branch_strategy: Planning artifacts for this mission were generated on feat/doctrine-mission-type-spec-01KSWJVX. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/doctrine-mission-type-spec-01KSWJVX unless the human explicitly redirects the landing branch.
subtasks:
- T066
- T067
- T068
- T069
- T070
agent: claude
history:
- at: '2026-05-30T17:21:57Z'
  event: created
  note: Initial task breakdown
agent_profile: architect-alphonso
authoritative_surface: src/charter/drg.py
execution_mode: code_change
owned_files:
- src/charter/drg.py
- src/doctrine/drg/
- tests/charter/test_activation_filtered_drg.py
role: implementer
tags: []
---

## ⚡ Do This First: Load Agent Profile

Before reading anything else, load your agent profile:

/ad-hoc-profile-load architect-alphonso

This profile contains the coding standards, testing requirements, and
architectural constraints you must follow throughout this work package.

---

# Work Package Prompt: WP11 — Activation-filtered DRG traversal

## Context

FR-018 specifies that DRG traversal is activation-filtered: only doctrine artifacts that are explicitly activated in the project charter are included in the resolved governance set. "Activated" and "registered" are synonyms — an artifact that is not activated is non-canonical and invisible to charter-mediated resolution.

The `PackContext` (from WP06) carries `activated_kinds` and `activated_mission_types` as frozen sets. The DRG traversal reads these sets from `PackContext` and filters the resolved artifact set accordingly.

Non-activated artifacts remain accessible via the doctrine module API on direct user request — they are not deleted, just invisible to charter-mediated resolution.

## Objective

Add activation-filter logic to the DRG traversal in `src/charter/drg.py` and/or `src/doctrine/drg/`. Apply the filter to all artifact kinds (directives, tactics, mission types, mission steps, agent profiles). Write tests verifying the filter behavior.

## FR-006 Context

FR-006 specifies two-tier directive scope:
1. **Project-scoped**: `org-charter.yaml` `required_directives` apply to all mission types
2. **Mission-type-scoped**: a mission type's `governance_refs` adds directives scoped only to that mission type

The activation filter ensures that mission-type-scoped directives (from `governance_refs`) are only included in governance resolution when that mission type is activated. Software-dev directives do not appear in non-software missions because they are in `software-dev.governance_refs`, which is only included when software-dev is activated.

## Subtasks

### T066 — Add activation filter to DRG traversal

Open `src/charter/drg.py` (and/or `src/doctrine/drg/org_pack_loader.py` if that is where DRG traversal happens).

Before traversal begins, read `PackContext.activated_mission_types`:
- During mission-type artifact resolution: only include mission types whose `id` is in `pack_context.activated_mission_types`
- During mission-step artifact resolution: only include steps belonging to activated mission types

This filter is applied at the start of traversal — activated types are enumerated, then their steps are resolved.

Implementation pattern:
```python
def traverse(
    artifact_kind: str,
    pack_context: PackContext,
    repo_root: Path,
) -> list[ArtifactResult]:
    # Activation filter: skip non-activated mission types
    active_mission_types = pack_context.activated_mission_types
    if artifact_kind in ("mission_type", "mission_step"):
        results = [r for r in raw_results if r.mission_type_id in active_mission_types]
    return results
```

### T067 — Apply filter across all artifact kinds

Extend the activation filter to cover all artifact kinds, not just mission types:
- `directives`: only include if the directive's source pack is activated (or if it is a project-scoped directive)
- `tactics`: same
- `agent_profiles`: only if the profile's owning pack is activated
- `mission_types`: only if `mission_type_id` in `activated_mission_types`
- `mission_steps`: only if owning `mission_type_id` in `activated_mission_types`

Use `PackContext.activated_kinds` for non-mission-type artifact kinds.

### T068 — Implement PackContext.activated_kinds filter

In `PackContext.from_config()` (WP06), ensure `activated_kinds` is populated from the charter's activation configuration. If no explicit activation configuration exists, default to including all built-in kinds (backward compatibility, consistent with FR-019 intent).

Update `PackContext` if any new fields are needed to support the per-kind filter.

### T069 — Non-activated artifacts remain accessible via doctrine API

This is a documentation and test guard, not a code change:

Verify that calling `MissionTypeRepository.get("documentation")` directly (bypassing the charter/DRG path) returns the `documentation` mission type even when `documentation` is not activated in the project charter.

The activation filter applies only to charter-mediated resolution paths. Direct doctrine API calls are exempt.

Add a comment in the DRG traversal code explaining this invariant.

### T070 — Activation filter tests

Write `tests/charter/test_activation_filtered_drg.py`:

Test cases:
- **Activation filter**: project charter activates only `software-dev`; DRG traversal returns only software-dev mission type and its steps
- **Non-activated excluded**: `documentation` not in activated set; DRG traversal does not include documentation mission type or its steps
- **FR-006 directive scope**: software-dev `governance_refs` directives do not appear in governance resolution for a documentation mission (different mission type)
- **Direct doctrine API bypass**: `MissionTypeRepository.get("documentation")` returns the type even when not activated in charter
- **Empty activation set**: DRG traversal with empty `activated_mission_types` returns empty list for mission types

Use `tmp_path` fixtures for PackContext construction with test data.

## Acceptance Criteria

- [ ] DRG traversal only returns artifacts for activated mission types
- [ ] Software-dev `governance_refs` directives do not appear in documentation mission governance
- [ ] Non-activated artifacts are still accessible via direct doctrine API calls
- [ ] `PackContext.activated_kinds` drives the per-kind filter
- [ ] `tests/charter/test_activation_filtered_drg.py` passes
- [ ] `mypy --strict` clean on modified files

## References

- FR-006: Two-tier directive scope
- FR-018: Activation-filtered DRG traversal
- data-model.md §"PackContext" — activated_kinds and activated_mission_types fields
- contracts/activation-filtered-drg-contract.md
