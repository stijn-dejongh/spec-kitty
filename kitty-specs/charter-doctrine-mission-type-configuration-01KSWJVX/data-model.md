# Data Model: Charter Doctrine Mission-Type Configuration

**Mission**: `charter-doctrine-mission-type-configuration-01KSWJVX`
**Date**: 2026-05-30

---

## Entities

### MissionType

**Location**: `src/doctrine/missions/mission_types/{id}.yaml` (built-in),
`<pack-root>/mission-types/{id}.yaml` (org), `.kittify/overrides/mission-types/{id}.yaml` (project)

**Aggregate root** in the Doctrine bounded context.

```yaml
# Example: src/doctrine/missions/mission_types/software-dev.yaml
schema_version: 1
id: software-dev
display_name: "Software Development"
action_sequence:
  - specify
  - plan
  - tasks
  - implement
  - review
governance_refs:
  - DIR-010
  - DIR-011
template_set:
  spec: spec-template.md
  plan: plan-template.md
```

| Field | Type | Required | Notes |
|---|---|---|---|
| `schema_version` | `int` | yes | Monotonically increasing integer; baseline = 1 |
| `id` | `str` | yes | ASCII kebab-case slug; enforced by `IDENTIFIER_PATTERN` (C-003) |
| `display_name` | `str` | yes | Human-readable name |
| `extends` | `str \| None` | no | ID of the base mission type at the same layer |
| `action_sequence` | `list[str]` | yes | Ordered step IDs; must be non-empty and unique |
| `governance_refs` | `list[str]` | no | Directive/tactic IDs scoped to this mission type only |
| `template_set` | `dict[str, str] \| None` | no | Per-artifact-type template mapping `{artifact_type: template_id}` |

**Invariants**:
- `action_sequence` must be non-empty (validated at activate time).
- All step IDs in `action_sequence` must be unique within that list.
- `id` must match the filename stem (e.g., `software-dev.yaml` → `id: software-dev`).
- Built-in definitions are immutable at runtime (C-006); org/project layers shadow only.
- `ResolvedMissionType` is the pure-function output of the resolver: identical inputs always produce identical output.

---

### MissionStep (unified)

**Location**: `src/doctrine/missions/mission-steps/{mission_type_id}/{step_id}/`

**Entity owned by `MissionType`.** Identity is `(mission_type_id, step_id)` — two steps with the same `step_id` in different mission types are independent entities.

```
src/doctrine/missions/mission-steps/
└── software-dev/
    └── specify/
        ├── step.yaml       ← descriptor
        ├── prompt.md       ← command template (verbatim from old command-templates/)
        └── guidelines.md   ← optional guidance document
```

**`step.yaml` schema:**

```yaml
# Example: mission-steps/software-dev/specify/step.yaml
id: specify
display_name: "Specification"
step_type: agent            # agent | human_in_loop | integration
prompt_template: prompt.md  # relative path within this step directory
agent_profile: architect-alphonso   # optional
guidance: null              # optional short guidance string
delegates_to: []            # optional doctrine artifact refs
depends_on: []              # optional step IDs within same mission type
```

| Field | Type | Required | Notes |
|---|---|---|---|
| `id` | `str` | yes | Step ID; unique within the owning `MissionType` |
| `display_name` | `str` | yes | Human-readable step name |
| `step_type` | `"agent" \| "human_in_loop" \| "integration"` | yes | Executor discriminant |
| `prompt_template` | `str` | yes | Relative path to the Markdown prompt file |
| `agent_profile` | `str \| None` | no | Doctrine agent profile ID |
| `guidance` | `str \| None` | no | Short inline guidance for operators |
| `delegates_to` | `list[str]` | no | Doctrine artifact refs for governance concretisation |
| `depends_on` | `list[str]` | no | Step IDs that must complete before this step |

**`step_type` → `Decision.kind` mapping** (used by `spec-kitty next`):

| `step_type` | `Decision.kind` | Behaviour |
|---|---|---|
| `agent` | `step` | Prompt dispatched to LLM |
| `human_in_loop` | `decision_required` | Operator must act before next can proceed |
| `integration` | `blocked` | Structured advisory; no providers in this release |

**Shadowing key**: compound path `{mission_type_id}/{step_id}` (directory). A `software-dev/review/` shadow overrides only the `review` step of `software-dev`.

**Resolution order**: `built-in → org → project` (project shadow wins).

---

### OrgCharterPolicy (extended)

**Location**: `src/specify_cli/doctrine/org_charter.py`

Extends the existing Pydantic model with `schema_version` and `extends`.

| Field | Type | Required | Change |
|---|---|---|---|
| `schema_version` | `int` | yes | **New** — baseline = 1 |
| `extends` | `str \| None` | no | **New** — names the base pack to extend |
| `required_directives` | `list[str]` | no | Existing — union semantics |
| `required_toolguides` | `list[str]` | no | Existing — union semantics |
| `interview_defaults` | `dict[str, str \| bool]` | no | Existing — per-key replacement (C-002 exemption) |

**Resolution semantics**:
- `required_directives`, `required_toolguides`: union across chain (overlay adds, never removes).
- `interview_defaults`: per-key replacement (overlay key wins, unmentioned keys inherit from base).
- `schema_version`: must match between base and overlay; mismatch raises a structured error.
- Cycle in `extends:` chain: raises `OrgCharterCycleError` with the full cycle path.
- Missing base: raises `OrgCharterExtensionError` with the chain that led to the failure.

---

### PackContext

**Location**: `src/charter/` (new frozen dataclass)

Encapsulates the pre-validated pack set constructed by the charter module. Passed to the doctrine resolver; the resolver never reads `.kittify/config.yaml` directly (C-005).

```python
@dataclass(frozen=True)
class PackContext:
    activated_kinds: frozenset[str]           # artifact kinds activated in project charter
    activated_mission_types: frozenset[str]   # mission type IDs activated in project charter
    pack_roots: tuple[Path, ...]              # ordered pack root paths (built-in first)
    org_pack_names: tuple[str, ...]           # org pack names present in config.yaml
```

**Invariants**:
- Constructed by the charter module only; the doctrine resolver never constructs it.
- Immutable after construction (frozen dataclass).
- `activated_mission_types` is the filter applied during DRG traversal (FR-018).

---

### MissionTypeProfile (modified)

**Location**: `src/charter/mission_type_profiles.py`

| Field | Change |
|---|---|
| `mission_type: Literal[…]` | **Open** to `str`; runtime validation via `charter.existing_mission_types()` |
| `template_set: str \| None` | **Evolve** to `dict[str, str] \| None` (per-artifact dict) in Phase F; string form deprecated |

---

## New Public APIs

### `charter.existing_mission_types(repo_root: Path) → list[str]`

Returns the list of activated mission type IDs for the project at `repo_root`.
An ID appears in this list if and only if the mission type is explicitly activated in the project charter. Non-activated types are excluded regardless of their presence in the doctrine layer.

### `charter.resolve_action_sequence(mission_type_id: str, repo_root: Path) → list[str]`

Returns the live action sequence for `mission_type_id` by resolving the `MissionType` YAML
through the `built-in → org → project` DRG chain. Called fresh at each `spec-kitty next`
invocation (not cached across calls). Pure function of inputs.

---

## Error Types

| Error class | Location | Trigger |
|---|---|---|
| `UnknownMissionTypeError` | `src/charter/mission_type_profiles.py` | `--mission-type <id>` not in `existing_mission_types()` |
| `OrgCharterExtensionError` | `src/specify_cli/doctrine/org_charter.py` | Base pack named in `extends:` not found in loaded pack set |
| `OrgCharterCycleError` | `src/specify_cli/doctrine/org_charter.py` | Cycle detected in `extends:` chain |

Both `OrgCharterExtensionError` and `OrgCharterCycleError` include the chain that led to the failure in their message.

---

## On-Disk Directory Layout Summary

```
src/
├── doctrine/
│   └── missions/
│       ├── models.py                           ← unified MissionStep Pydantic model
│       ├── mission_types/                      ← NEW: MissionType YAML definitions
│       │   ├── software-dev.yaml
│       │   ├── documentation.yaml
│       │   ├── research.yaml
│       │   └── plan.yaml
│       └── mission-steps/                      ← NEW: step artifacts
│           ├── software-dev/
│           │   ├── specify/
│           │   │   ├── step.yaml
│           │   │   ├── prompt.md
│           │   │   └── guidelines.md
│           │   ├── plan/ …
│           │   ├── tasks/ …
│           │   ├── implement/ …
│           │   └── review/ …
│           ├── documentation/ …
│           ├── research/ …
│           └── plan/ …
│
└── charter/
    └── (new: PackContext dataclass, existing_mission_types(), resolve_action_sequence())

.kittify/overrides/mission-types/        ← project-layer MissionType overrides
.kittify/overrides/mission-steps/        ← project-layer MissionStep overrides
<org-pack-root>/mission-types/           ← org-layer MissionType overrides
<org-pack-root>/mission-steps/           ← org-layer MissionStep overrides
```
