# Tasks: Charter Doctrine Mission-Type Configuration

**Mission**: `charter-doctrine-mission-type-configuration-01KSWJVX`
**Date**: 2026-05-30
**Phase**: Implementation

---

## Work Packages

| WP | Title | Phase | Dependencies | FRs |
|---|---|---|---|---|
| WP01 | Unify MissionStep model + migrate callers | Phase A | — | FR-011 |
| WP02 | Create mission-steps/ directory structure + move command templates | Phase A | WP01 | FR-010, FR-011 |
| WP03 | Create MissionType YAML definitions + MissionTypeRepository | Phase A | WP01, WP02 | FR-004, FR-005, FR-015 |
| WP04 | MissionStepRepository — compound-key resolution | Phase A | WP01, WP02, WP03, WP06 | FR-012 |
| WP05 | Charter API: existing_mission_types() + resolve_action_sequence() + open Literal→str | Phase B | WP03, WP04, WP06 | FR-007, FR-008, FR-009 |
| WP06 | PackContext dataclass + charter wiring | Phase B | WP03 | FR-007 |
| WP07 | Delete frozensets + wire all 4 call sites to charter | Phase C | WP05, WP06 | FR-007, FR-008 |
| WP08 | Rewire template deployment pipeline; update CLAUDE.md | Phase C | WP02, WP07 | FR-010 |
| WP09 | OrgCharterPolicy extends: field + chain resolver + error classes | Phase D | WP06 | FR-001, FR-002, FR-003 |
| WP10 | PackContext wiring into OrgCharterPolicy loader | Phase D | WP09 | FR-001, FR-003 |
| WP11 | Activation-filtered DRG traversal (FR-018) | Phase E | WP03, WP06, WP10 | FR-006, FR-018 |
| WP12 | FR-019 upgrade migration (m_3_2_7) | Phase E | WP11 | FR-019 |
| WP13 | CLI — spec-kitty doctrine mission-type list | Phase F | WP03, WP04 | FR-013, FR-014 |
| WP14 | CLI — charter mission-type list / mission-type list / mission-type show | Phase F | WP05, WP13 | FR-016, FR-017 |
| WP15 | spec-kitty charter activate in-flight warning | Phase G | WP07, WP14 | FR-008 |

---

## Subtask Registry

### WP01 — Unify MissionStep model + migrate callers

| ID | Subtask |
|---|---|
| T001 | Audit existing MissionStep models in doctrine/missions/models.py and doctrine/mission_step_contracts/models.py; document field differences | [D] |
| T002 | Author unified MissionStep Pydantic model with step_type discriminant (agent/human_in_loop/integration) in doctrine/missions/models.py | [D] |
| T003 | Add IDENTIFIER_PATTERN validation for MissionStep.id (C-003) and declare __all__ | [D] |
| T004 | Migrate callers in doctrine/ (artifact_kinds.py, service.py) from mission_step_contracts to unified model; org_pack_loader.py migration deferred to WP11/T066b | [D] |
| T005 | Migrate all callers in specify_cli/ (pack_assembler.py, pack_validator.py, snapshot.py) from mission_step_contracts to the unified model | [D] |
| T006 | Migrate charter/ callers (schemas.py, mission_steps.py, activations.py, context.py, drg.py) to unified model | [D] |
| T007 | Delete doctrine/mission_step_contracts/ subpackage; confirm specify_cli/mission_step_contracts/ is NOT deleted | [D] |
| T008 | Extend tests/architectural/test_layer_rules.py for unified model boundary | [D] |
| T009 | Write unit tests for unified MissionStep model validation (step_type variants, id pattern, field defaults) | [D] |

### WP02 — Create mission-steps/ directory structure + move command templates

| ID | Subtask |
|---|---|
| T010 | Enumerate all existing command-template Markdown files in src/specify_cli/missions/*/command-templates/ | [D] |
| T011 | Create src/doctrine/missions/mission-steps/ with subdirectory structure per mission type and step ID | [D] |
| T012 | Move software-dev command templates verbatim to mission-steps/software-dev/{step_id}/prompt.md | [D] |
| T013 | Move documentation, research, plan command templates verbatim to their respective mission-steps/ subdirectories | [D] |
| T014 | Author step.yaml descriptors for each step (id, display_name, step_type=agent, prompt_template=prompt.md) | [D] |
| T015 | Delete old src/specify_cli/missions/*/command-templates/ directories | [D] |
| T016 | Write tests verifying mission-steps/ directory structure is complete and all step.yaml files are valid | [D] |

### WP03 — Create MissionType YAML definitions + MissionTypeRepository

| ID | Subtask |
|---|---|
| T017 | Author software-dev.yaml in src/doctrine/missions/mission_types/ with action_sequence from _COMPOSED_ACTIONS_BY_MISSION | [D] |
| T018 | Author documentation.yaml, research.yaml, plan.yaml with their respective action sequences | [D] |
| T019 | Implement MissionType Pydantic model (id, display_name, extends, action_sequence, governance_refs, template_set) in doctrine/missions/models.py | [D] |
| T020 | Implement MissionTypeRepository — load all YAML files from mission_types/ directory, validate, index by id | [D] |
| T021 | Add template_set dict[str, str] field evolution (from string to per-artifact dict); update ATDD test suite | [D] |
| T022 | Write unit tests: YAML round-trip, action_sequence non-empty validation, id matches filename stem | [D] |

### WP04 — MissionStepRepository — compound-key resolution

| ID | Subtask |
|---|---|
| T023 | Design MissionStepRepository class interface: resolve(mission_type_id, step_id, pack_context) -> MissionStep | [D] |
| T024 | Implement built-in layer resolution: find step.yaml at src/doctrine/missions/mission-steps/{mission_type_id}/{step_id}/ | [D] |
| T025 | Implement org-layer shadowing: scan org pack roots for {mission_type_id}/{step_id}/ overrides | [D] |
| T026 | Implement project-layer shadowing: scan .kittify/overrides/mission-steps/{mission_type_id}/{step_id}/ | [D] |
| T027 | Add compound-key collision safety: a software-dev/review shadow does NOT affect documentation/review | [D] |
| T028 | Write layered-resolution tests: built-in only, org shadow, project shadow, compound-key isolation | [D] |

### WP05 — Charter API: existing_mission_types() + resolve_action_sequence() + open Literal→str

| ID | Subtask |
|---|---|
| T029 | Open MissionTypeProfile.mission_type from Literal[...] to str in src/charter/mission_type_profiles.py | [D] |
| T030 | Update UnknownMissionTypeError to include registered_ids list in message (FR-009) | [D] |
| T031 | Implement charter.existing_mission_types(repo_root: Path) -> list[str]: returns activated mission type IDs sorted | [D] |
| T032 | Implement charter.resolve_action_sequence(mission_type_id: str, repo_root: Path) -> list[str]: live DRG lookup | [D] |
| T033 | Update resolve_mission_type_governance() to use charter.existing_mission_types() for validation instead of Literal | [D] |
| T034 | Update ATDD test suite pinning the Literal constraint (test_wp_prompt_governance_contract.py) | [D] |
| T035 | Write tests: existing_mission_types() returns sorted deduplicated IDs; resolve_action_sequence() for built-in types; UnknownMissionTypeError with registered_ids | [D] |

### WP06 — PackContext dataclass + charter wiring

| ID | Subtask |
|---|---|
| T036 | Implement PackContext frozen dataclass in src/charter/ with fields: activated_kinds, activated_mission_types, pack_roots, org_pack_names | [D] |
| T037 | Add __all__ declaration and full type annotations to PackContext module | [D] |
| T038 | Implement charter-side constructor: read .kittify/config.yaml, validate pack set, build PackContext | [D] |
| T039 | Pass PackContext to existing doctrine resolver calls in charter/ — replace any direct config.yaml reads in resolver | [D] |
| T040 | Write unit tests: PackContext construction from config, immutability assertion, empty config fallback | [D] |

### WP07 — Delete frozensets + wire all 4 call sites to charter

| ID | Subtask |
|---|---|
| T041 | Delete _COMPOSED_ACTIONS_BY_MISSION frozenset from runtime_bridge.py (lines 827 region) |
| T042 | Replace runtime_bridge.py line 876 call site with charter.resolve_action_sequence() |
| T043 | Replace runtime_bridge.py line 988 call site with charter.resolve_action_sequence() |
| T044 | Replace runtime_bridge.py line 2090 (_should_dispatch_via_composition) with charter.resolve_action_sequence() |
| T045 | Delete _COMPOSED_ACTIONS_FOR_PROMPT frozenset from decision.py (lines 535 region) |
| T046 | Replace decision.py line 573 call site with charter.resolve_action_sequence() |
| T047 | Write integration tests: all 4 call sites exercise the live charter path; NFR-002 zero-regression verification |

### WP08 — Rewire template deployment pipeline; update CLAUDE.md

| ID | Subtask |
|---|---|
| T048 | Update src/specify_cli/skills/command_renderer.py to read prompt templates from src/doctrine/missions/mission-steps/{mission_type}/{step_id}/prompt.md |
| T049 | Update src/specify_cli/skills/command_installer.py source path references |
| T050 | Update upgrade migration pipeline (caller of get_agent_dirs_for_project()) to use new doctrine source path |
| T051 | Update CLAUDE.md "Template Source Location" section: table row and code example to reflect src/doctrine/missions/mission-steps/ |
| T052 | Write NFR-004 gate test: verify .claude/commands/specify.md renders from new doctrine path |

### WP09 — OrgCharterPolicy extends: field + chain resolver + error classes

| ID | Subtask |
|---|---|
| T053 | Add schema_version: int field to OrgCharterPolicy (with backward-compat str coercion validator if field already exists as str) | [D] |
| T054 | Add extends: str | None optional field to OrgCharterPolicy | [D] |
| T055 | Implement _resolve_chain(pack_name, pack_set) -> list[OrgCharterPolicy] with depth-first traversal | [D] |
| T056 | Add cycle detection: OrgCharterCycleError raised with full cycle path when extends: creates a loop | [D] |
| T057 | Add missing-base detection: OrgCharterExtensionError raised when named base pack not found | [D] |
| T058 | Implement merge logic: union required_directives and required_toolguides; per-key replace interview_defaults | [D] |
| T059 | Implement schema_version mismatch error: structured error with both version values | [D] |
| T060 | Write tests: simple extends chain; depth-2 chain; union semantics; cycle detection; missing base; version mismatch | [D] |
| T061-sig | Update load_org_charter_policies() signature to accept optional PackContext parameter | [D] |
| T062-chain | Wire _resolve_chain to use PackContext.pack_roots; add _build_pack_set() helper | [D] |

### WP10 — PackContext wiring into OrgCharterPolicy loader

| ID | Subtask |
|---|---|
| T063 | Audit and confirm no config.yaml reads remain in resolver path when PackContext is provided | [D] |
| T064 | Update charter callers (src/charter/drg.py, src/charter/context.py) to pass PackContext to load_org_charter_policies() | [D] |
| T065 | Write integration tests: full chain resolution through PackContext; backward compat for packs without extends: | [D] |

### WP11 — Activation-filtered DRG traversal

| ID | Subtask |
|---|---|
| T066b | Migrate org_pack_loader.py _ORG_DRG_CANONICAL_KINDS alias and imports (deferred from WP01/T004) | [D] |
| T066 | Add activation filter logic to DRG traversal: only include artifacts with IDs present in PackContext.activated_mission_types | [D] |
| T067 | Apply filter across all artifact kinds (directives, tactics, mission types, mission steps, agent profiles) | [D] |
| T068 | Verify PackContext.activated_kinds is populated correctly by WP06 (do NOT modify pack_context.py) | [D] |
| T069 | Non-activated artifacts remain accessible via doctrine module API on explicit request (not through charter) | [D] |
| T070 | Write tests: activation-filtered traversal includes only activated types; non-activated excluded from charter resolution; direct doctrine API still accessible | [D] |

### WP12 — FR-019 upgrade migration (m_3_2_7)

| ID | Subtask |
|---|---|
| T071 | Create src/specify_cli/upgrade/migrations/m_3_2_7_activate_builtin_mission_types.py following m_3_2_6 pattern |
| T072 | Migration logic: detect .kittify/config.yaml; if no explicit mission-type activation entries, add full built-in set (software-dev, documentation, research, plan) |
| T073 | Preserve any existing charter configuration; only add missing activation entries |
| T074 | Use get_agent_dirs_for_project() from m_0_9_1_complete_lane_migration for config-aware agent directory handling |
| T075 | Register migration in the upgrade migration registry |
| T076 | Write tests: migration on project without mission-type entries adds all four built-ins; migration on project with existing entries is idempotent; dry-run mode |

### WP13 — CLI: spec-kitty doctrine mission-type list

| ID | Subtask |
|---|---|
| T077 | Add mission-type sub-group (or command) under spec-kitty doctrine CLI group in src/specify_cli/cli/commands/doctrine.py | [D] |
| T078 | Implement list sub-command: enumerate all mission types in doctrine layer (built-in + org + project overrides) regardless of activation | [D] |
| T079 | Output columns: id, source_layer, display_name; support --json flag | [D] |
| T080 | Wire to MissionTypeRepository for layer-aware enumeration | [D] |
| T081 | Write tests: list returns built-in types; list includes org/project overrides when present; --json output schema | [D] |

### WP14 — CLI: charter mission-type list / mission-type list alias / mission-type show

| ID | Subtask |
|---|---|
| T082 | Add spec-kitty charter mission-type list command: activated-only types for current project; output includes action_sequence |
| T083 | Add spec-kitty mission-type list as alias for charter mission-type list |
| T084 | Implement spec-kitty mission-type show <id>: render fully resolved MissionType (merged across all layers) with action_sequence, governance_refs, template_set, source layer per field |
| T085 | Wire mission-type show to resolve_action_sequence() and MissionTypeRepository for full resolution |
| T086 | Write tests: charter list returns only activated types; show renders resolved definition; show raises UnknownMissionTypeError for unknown ID; alias behaves identically to charter list |

### WP15 — spec-kitty charter activate in-flight warning

| ID | Subtask |
|---|---|
| T087 | Hook into spec-kitty charter activate execution path to inspect mission-type overrides being activated |
| T088 | Compare incoming action_sequence against current activated action_sequence; identify removed step IDs |
| T089 | For each removed step ID, query in-flight missions (status.events.jsonl) for any WPs in the corresponding lane |
| T090 | Emit structured warning per affected mission (mission_slug, wp_id, removed_step) before completing activation |
| T091 | Warning is non-blocking: activation completes after warning is emitted |
| T092 | Write tests: warning emitted when removed step has in-flight WPs; no warning when no in-flight WPs; activation completes in both cases |
