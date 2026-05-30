# Charter Doctrine Mission-Type Configuration

**Mission ID**: `01KSWJVX564N81MXT8VJFRQ7AB`
**Mission slug**: `charter-doctrine-mission-type-configuration-01KSWJVX`
**Target branch**: `feat/pre-doctrine-stabilization-remediation`
**GitHub issues addressed**: #1397, #883, #682, #1333

---

## Purpose

Spec Kitty's doctrine layer is composable for directives, tactics, and agent profiles — but the mission workflow sequence and the step prompts that drive agents are still hardcoded in the CLI. Teams whose real process differs from the built-in `specify → plan → tasks → implement → review → merge` sequence, or whose organisation requires custom governance layers, currently have no extension point short of forking the codebase.

This mission opens three extension seams and migrates all hardcoded step prompts into the doctrine resolution chain:

1. **org-charter `extends:`** — org packs can additively layer directives without duplicating base policy (#1397)
2. **Mission-type governance profiles** — each mission type is a first-class governed artifact; workflow sequence and step prompts are its properties (#883, #682)
3. **Templates DRG layer** — built-in doctrine templates are enumerable and overridable via the standard resolution chain (#1333)

---

## Actors

| Actor | Role |
|---|---|
| Team/Enterprise operator | Configures `.kittify/config.yaml` with org packs and project overrides |
| Mission author | Creates and runs missions; relies on `spec-kitty next` to dispatch the correct step |
| Org pack author | Writes `org-charter.yaml`, mission-type overrides, and step prompt templates for an org pack |
| Spec Kitty contributor | Maintains built-in doctrine artifacts in `src/doctrine/` |

---

## User Scenarios

### Scenario 1 — Add a step to a built-in workflow

A team wants a post-merge "Executive Summary" step in software-dev missions that writes a summary to their knowledge base. They add a project-level override:

```yaml
# .kittify/overrides/mission-types/software-dev.yaml
extends: software-dev
action_sequence:
  - specify
  - plan
  - tasks
  - implement
  - review
  - merge
  - executive-summary   # ← new step
```

They define the step:
```yaml
# .kittify/overrides/mission-steps/executive-summary.yaml
id: executive-summary
display_name: Write Executive Summary
step_type: agent
prompt_template: executive-summary.md
```

When they run `spec-kitty next` after merge, the executive-summary step is dispatched.

### Scenario 2 — Override an existing built-in mission type

A team replaces the software-dev mission type entirely with a shorter internal flow (no separate review WP — reviewers are embedded in the implement loop):

```yaml
# .kittify/overrides/mission-types/software-dev.yaml
extends: software-dev
action_sequence:
  - specify
  - plan
  - tasks
  - implement          # review is a built-in sub-loop here
  - merge
  - accept
```

`spec-kitty next` for any software-dev mission uses this sequence.

### Scenario 3 — Create a custom mission type

An operator creates a `compliance-audit` mission type with entirely different steps:

```yaml
# .kittify/overrides/mission-types/compliance-audit.yaml
id: compliance-audit
display_name: Compliance Audit
action_sequence:
  - scope
  - evidence-gather
  - review
  - report
  - sign-off
```

They start a mission with `spec-kitty mission create "q2-audit" --mission-type compliance-audit`.

### Scenario 4 — Org pack with additive directives

An enterprise `regnology-banking` org pack extends the `regnology-default` base pack — adding SWIFT_CSP and GDPR_HANDLING directives without duplicating the base set:

```yaml
# regnology-banking/org-charter.yaml
org_name: regnology-banking
extends: regnology-default
required_directives:
  - SWIFT_CSP
  - GDPR_HANDLING
```

The resolved set is the union of `regnology-default`'s directives plus the two banking-specific ones.

---

## Functional Requirements

| ID | Requirement | Priority | Status |
|---|---|---|---|
| FR-001 | `org-charter.yaml` supports an optional `extends: <pack-name>` key. `extends:` makes the existing flat-union behavior explicit and named: without it, all listed packs are merged as before (backward-compatible); with it, the union relationship is declared hierarchically between a named base pack and the overlay. `required_directives` and `required_toolguides` are resolved as the **union** of base and overlay (overlay can add, never remove). `interview_defaults` are resolved per-key (overlay key wins, unmentioned keys inherit from base). The existing `OrgCharterPolicy` Pydantic model gains an optional `extends` field; the loader's flat-union behavior is preserved for packs without `extends:`. | P1 | Proposed |
| FR-002 | Resolution raises `OrgCharterExtensionError` when the named base pack is not present in the loaded pack set, and `OrgCharterCycleError` when an `extends:` chain contains a cycle. Both errors include the chain that led to the failure. | P1 | Proposed |
| FR-003 | `schema_version` must match between base and overlay; a mismatch raises a structured error with both version values. | P1 | Proposed |
| FR-004 | Each mission type (`software-dev`, `documentation`, `research`, `plan`) is a first-class governed artifact in the doctrine layer, resolved via the `built-in → org → project` chain. Governance is keyed from `mission_type` in `meta.json`, not from `template_set`. | P1 | Proposed |
| FR-005 | A mission-type definition includes: `id`, optional `extends`, `display_name`, `action_sequence` (ordered list of step IDs), and optional `governance_refs` (directive/tactic IDs scoped to this mission type). | P1 | Proposed |
| FR-006 | Directive scope is two-tier: (1) **project-scoped** — org-charter `required_directives` apply to all mission types in the project; (2) **mission-type-scoped** — a mission type's `governance_refs` adds directives that apply only to that mission type. The resolved governance for a mission is the union of both tiers. Software-dev directives do not appear in non-software missions because they live in `governance_refs` on the `software-dev` mission-type definition, not in the org-charter. No directive cross-injection occurs across mission types. | P1 | Proposed |
| FR-007 | `spec-kitty next` reads `action_sequence` from the resolved mission-type profile for the active mission and dispatches accordingly. The sequence is never hardcoded in the runtime. The existing `_COMPOSED_ACTIONS_BY_MISSION` (in `runtime_bridge.py`) and `_COMPOSED_ACTIONS_FOR_PROMPT` (in `decision.py`) frozenset tables are removed; the dispatch call chain is `specify_cli.next → charter.resolve_action_sequence(mission_type_id, repo_root) → doctrine_resolver.resolve_action_sequence(mission_type_id, layer_context)`. Charter is the source of truth for behavioral dispatch; `specify_cli.next` never imports from `doctrine.*` directly. See [`contracts/action-sequence-dispatch-contract.md`](contracts/action-sequence-dispatch-contract.md). | P1 | Proposed |
| FR-008 | A project-level or org-level `mission-type` override can **extend** a built-in type (adding or reordering steps) or **replace** it entirely (no `extends:` key → full replacement). | P1 | Proposed |
| FR-009 | A user can create a **custom mission type** with a unique `id` not present in the built-in set. `spec-kitty mission create` accepts `--mission-type <id>` for any registered type. "Registered" means present in the set returned by `charter.existing_mission_types(repo_root)`, which enumerates all mission-type IDs visible in the active `built-in → org → project` DRG inventory. Validation occurs at `mission create` time; an unknown `--mission-type` raises `UnknownMissionTypeError` with the queried ID and the list of registered IDs before the mission is created. | P1 | Proposed |
| FR-010 | All step prompt templates that are currently hardcoded in `src/specify_cli/missions/*/command-templates/` become doctrine `mission-step` artifacts under `src/doctrine/missions/mission-steps/`. The built-in set encodes the current prompts verbatim as the migration baseline. | P1 | Proposed |
| FR-011 | The canonical `MissionStep` aggregate root defines: `id`, `display_name`, `step_type` (`agent` \| `human_in_loop` \| `integration`), `prompt_template` (path to a Markdown template within the same resolution layer), and optionally `delegates_to` (doctrine artifact refs for governance concretization), `guidance`, `depends_on` (step IDs), and `agent_profile`. This is the single unified model superseding `doctrine.missions.models.MissionStep` and `doctrine.mission_step_contracts.models.MissionStep`. | P1 | Proposed |
| FR-012 | Org and project layers can override `mission-step` prompt templates by providing a file at the corresponding path in their pack or `.kittify/overrides/` directory. Resolution follows the standard `built-in → org → project` precedence. | P1 | Proposed |
| FR-013 | `spec-kitty template list [--kind <mission\|diagram\|checklist\|…>]` enumerates built-in doctrine templates by category. Output includes name, kind, source layer, and resolution path. | P2 | Proposed |
| FR-014 | The template DRG layer follows `built-in → org → project` resolution. An org or project layer can shadow a built-in template by providing a file with the same `id` in their pack. | P2 | Proposed |
| FR-015 | A mission-type definition may optionally pin a preferred template variant for a given artifact type (e.g., `plan_template: org-custom-plan.md`). When pinned, the pinned template is resolved from the active layer chain. | P2 | Proposed |
| FR-016 | `spec-kitty mission-type list` enumerates all registered mission types (built-in + org overrides + project overrides) with their source layer and action sequence. | P2 | Proposed |
| FR-017 | `spec-kitty mission-type show <id>` renders the fully resolved mission-type definition (merged across all layers) for the current project. | P2 | Proposed |
| FR-018 | DRG traversal is activation-filtered: only doctrine artifacts that are explicitly activated in the project charter are included in the resolved governance set. Artifacts present in a layer (built-in, org, or project) but not activated are silently ignored during resolution. For example, a built-in agent profile may reference directives that are not activated in the charter; those directives do not appear in the resolved directive set for any mission type. Activation state is resolved by the charter module before DRG traversal begins and passed to the resolver as a filter. | P1 | Proposed |

---

## Non-Functional Requirements

| ID | Requirement | Threshold | Status |
|---|---|---|---|
| NFR-001 | `spec-kitty next` cold-start latency with the resolved mission-type chain must not exceed the pre-mission baseline by more than 100 ms for projects with no org or project overrides (common path). | ≤100 ms overhead | Proposed |
| NFR-002 | Zero migration required for existing software-dev missions. The built-in `software-dev` mission-type definition encodes the current action sequence; `spec-kitty next` behaviour is identical before and after the change. | 0 breaking changes | Proposed |
| NFR-003 | Mission-type and mission-step resolution must be covered by tests at the built-in-only, org-override, and project-override layers. Extends chains of depth ≥ 2 must be tested. | 100% path coverage | Proposed |
| NFR-004 | All existing agent command files deployed to `.claude/`, `.amazonq/`, etc. remain functional after the prompt migration. A migration that updates deployed copies from the new doctrine source is required. | Zero regression in deployed agent commands | Proposed |

---

## Constraints

| ID | Constraint | Status |
|---|---|---|
| C-001 | Project charter remains the top-level authority. Mission-type governance is additive scoping, not a competing charter source. | Binding |
| C-002 | Org overlay `extends:` can only restrict or add (union). Removing a base-pack directive from an overlay is not permitted (raises a structured error). | Binding |
| C-003 | Mission-type identifiers must be ASCII-only kebab-case slugs (enforced by the same sanitiser as DIR-010/DIR-011). | Binding |
| C-004 | DDD boundary: the Doctrine bounded context (`src/doctrine/`) owns all mission-type definitions and step templates. The `src/charter/` module is the anti-corruption layer: it is the **only** permitted entry point through which `specify_cli` accesses doctrine-owned data. `specify_cli.*` modules must not import from `doctrine.*` directly. `src/charter/` may import from `doctrine.*`; `doctrine.*` must not import from `charter.*` or `specify_cli.*`. This boundary is enforced by `tests/architectural/test_layer_rules.py`. `spec-kitty next` must not read charter YAML or mission-type YAML directly. | Binding |
| C-005 | The `extends:` chain for both org-charter and mission-type must be resolved before the active governance is applied. All packs in a chain must be listed in `.kittify/config.yaml`. Cross-repo extends is not supported in this release. | Binding |
| C-006 | Shipped mission-type definitions are immutable at runtime. Org and project overrides shadow; they do not mutate the built-in artifacts. | Binding |
| C-007 | All new public modules must declare `__all__` (per charter C-007 convention). | Binding |

---

## Domain Language

| Canonical Term | Definition | Avoid |
|---|---|---|
| **Mission type** | A first-class governed artifact that defines the `action_sequence` and governance scope for a class of missions | "template set", "mission template", "project type" |
| **Mission step** | A named, ordered action within a mission type's `action_sequence`, with a prompt template and step type | "command", "phase", "workflow step" |
| **Action sequence** | The ordered list of mission-step IDs that `spec-kitty next` dispatches for a given mission type | "workflow", "pipeline" |
| **Step prompt template** | The Markdown artifact that instructs an agent how to execute a mission step | "command template", "slash command", "hardcoded prompt" |
| **Built-in layer** | The layer of doctrine artifacts that ships with spec-kitty itself, under `src/doctrine/` | "shipped", "default", "base layer" |
| **Mission-type resolution chain** | The `built-in → org → project` precedence chain for resolving the active mission-type definition | "override chain", "lookup order", "shipped → org → project" |
| **org-charter extends** | The additive inheritance mechanism for `org-charter.yaml` | "merge", "inherit", "import" |
| **Doctrine bounded context** | The `src/doctrine/` package; owns governed artifacts and their resolution | "doctrine module", "doctrine layer" |
| **Anti-corruption layer** | The resolver interface through which `specify_cli` runtime consumes doctrine artifacts without coupling to doctrine internals | "adapter", "facade" |

---

## Key Entities

| Entity | Properties | Notes |
|---|---|---|
| `MissionType` | `id`, `display_name`, `extends?`, `action_sequence: [StepRef]`, `governance_refs?: [str]`, `template_pins?: {artifact_type: template_id}` | Aggregate root in Doctrine BC |
| `MissionStep` | `id`, `display_name`, `step_type: agent\|human_in_loop\|integration`, `prompt_template: path`, `delegates_to?: [ArtifactRef]`, `guidance?: str`, `depends_on?: [StepRef]`, `agent_profile?: str` | Aggregate root in Doctrine BC. Canonical consolidation of the currently fragmented `doctrine.missions.models.MissionStep` (schema-validation shape) and `doctrine.mission_step_contracts.models.MissionStep` (governance-delegation shape) — both are manifestations of the same concept. This mission establishes the single unified model; existing fragmented classes are superseded. |
| `OrgCharterExtension` | `extends: pack_name`, `required_directives: [str]`, `required_toolguides: [str]`, `interview_defaults: {str: any}` | Value object; merged at resolution time |
| `ResolvedMissionType` | Fully merged MissionType after applying all override layers | Output of the resolver; immutable |
| `DoctrineTemplate` | `id`, `kind`, `source_layer`, `path` | Enumerable via `template list` |

---

## Success Criteria

1. A team can add a custom step to the software-dev workflow in their project `.kittify/` without touching built-in code, and `spec-kitty next` dispatches that step after merge.
2. A team can create a fully custom mission type and start missions of that type; `spec-kitty next` uses the custom action sequence exclusively.
3. An enterprise org pack can layer additional directives on top of a base pack using `extends:` without duplicating the base pack's policy.
4. A non-software-dev mission (documentation, research) receives only its own mission-type governance — no software-dev directives appear in its governed context.
5. Existing software-dev missions run identically before and after this change (zero regression).
6. All built-in step prompt templates are resolvable through the doctrine layer; org and project overrides can shadow individual step prompts.
7. `spec-kitty template list` returns at least the built-in templates with correct kind and source-layer metadata.

---

## Assumptions

- The `src/doctrine/` package structure and the `built-in → org → project` DRG resolution pattern established by #832 are the baseline; this mission extends them to `mission-types` and `mission-steps`.
- The `spec-kitty next` command's existing dispatch logic is the authoritative entry point to refactor; no other runtime commands hardcode the action sequence.
- `spec-kitty mission create --mission-type <id>` already accepts a `mission_type` argument at the CLI level; if not, that CLI surface is part of FR-009's scope.
- Step prompt templates that are currently deployed to agent directories (`.claude/commands/`, etc.) will be regenerated from the new doctrine source during the next `spec-kitty upgrade` invocation in each project.
- The existing `OrgCharterPolicy` Pydantic model in `src/specify_cli/doctrine/` currently has no `extends:` field; the existing `load_org_charter_policies` loader performs a flat multi-pack union with no chain traversal. Adding `extends:` is a backward-compatible schema extension: packs without the field continue to union as before. `OrgCharterExtensionError` and `OrgCharterCycleError` are net-new error classes; the existing flat-union test suite requires no changes for packs that do not use `extends:`, but tests covering the new chain-traversal and cycle-detection paths must be added.
- The codebase currently has two classes named `MissionStep` in separate `doctrine` subpackages: `doctrine.missions.models.MissionStep` (schema-validation shape for `mission.yaml`) and `doctrine.mission_step_contracts.models.MissionStep` (governance-delegation shape for step contracts). These are fragmented manifestations of a single aggregate root concept, split by evolutionary accident. This mission consolidates them into one canonical `MissionStep` model. Existing callers of either class are migrated to the unified model as part of implementation; the two legacy classes are removed.
- `MissionTypeProfile.mission_type` in `src/charter/mission_type_profiles.py` is currently typed as `Literal["software-dev", "documentation", "research", "plan"]`, enforced by a Pydantic field validator and `UnknownMissionTypeError`. This mission widens the field to an open `str`; Pydantic parse-time validation is removed. `UnknownMissionTypeError` is preserved as a **runtime** gate, raised by `charter.resolve_action_sequence` and `charter.existing_mission_types` when the queried ID is absent from the DRG inventory. The ATDD test suite pinning the `Literal` constraint must be updated as part of this mission's implementation.
- `charter.existing_mission_types(repo_root: Path) -> list[str]` is a new public entrypoint added to `src/charter/mission_type_profiles.py`. It returns the deduplicated, sorted list of mission-type IDs registered across all active DRG layers (built-in + org + project). It is the single source of truth for "what mission types exist" at CLI validation time.

---

## Out of Scope

- Integration provider bindings in mission steps (GitLab MR, Jira close-on-merge — from #682's strawman). The `integration` step_type is reserved in the schema but no provider implementations ship in this release.
- ADRs as first-class primitives (#1040).
- AGT policy compilation (#1041).
- Dashboard glossary fix (#1098) — tracked separately.
- Cross-repo `extends:` chains (single-repo only in this release).
- Model selection per step (#531).
