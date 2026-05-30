# Contract: Action Sequence Dispatch via Charter

**Mission**: `charter-doctrine-mission-type-configuration-01KSWJVX`
**Addresses**: FR-007, B-1 (adversarial review finding)
**Status**: Proposed

---

## Problem

`spec-kitty next` currently determines which action to dispatch via two mirrored
hardcoded `frozenset` tables:

- `_COMPOSED_ACTIONS_BY_MISSION` in `src/specify_cli/next/runtime_bridge.py`
- `_COMPOSED_ACTIONS_FOR_PROMPT` in `src/specify_cli/next/decision.py`

These tables embed the action sequences for all built-in mission types (`software-dev`,
`documentation`, `research`, `plan`) as static data. FR-007 requires that this dispatch
is never hardcoded; the action sequence must come from the resolved mission-type profile.

---

## Required Code Path

The replacement call chain is:

```
spec-kitty next
  └─ decide_next_via_runtime(agent, mission_slug, result, repo_root)
       └─ charter.resolve_action_sequence(mission_type_id, repo_root)
            └─ doctrine_resolver.resolve_action_sequence(mission_type_id, layer_context)
                 └─ MissionType.action_sequence  (from built-in → org → project DRG)
```

### Layer 1 — `specify_cli.next` (runtime entry point)

`decide_next_via_runtime` must not call `_COMPOSED_ACTIONS_BY_MISSION` or any
static table. Instead it calls:

```python
from charter.mission_type_profiles import resolve_action_sequence

action_sequence = resolve_action_sequence(mission_type_id, repo_root)
```

`_COMPOSED_ACTIONS_BY_MISSION` and `_COMPOSED_ACTIONS_FOR_PROMPT` are removed. The
tables are not refactored into a new location — they are deleted. Their content
becomes the built-in `action_sequence` field in the built-in `MissionType` definitions
under `src/doctrine/missions/mission-types/`.

### Layer 2 — `charter.resolve_action_sequence` (source of truth for behavioral findings)

Charter is the authoritative source for behavioral outcomes. The charter module
exposes:

```python
# src/charter/mission_type_profiles.py
def resolve_action_sequence(
    mission_type_id: str,
    repo_root: Path,
) -> list[str]:
    """
    Returns the fully resolved action_sequence for the given mission type.

    Resolution order: built-in → org → project (standard DRG precedence).

    Raises:
        UnknownMissionTypeError: if mission_type_id is not registered in any layer.
        MissionTypeCycleError: if the extends: chain contains a cycle.
        MissionTypeStepResolutionError: if action_sequence references a step ID
            that has no corresponding MissionStep definition in the resolved layer set.
    """
```

This function is the single integration seam between `specify_cli.next` and the
doctrine layer. `specify_cli.next` must not import from `src/doctrine/` directly.

### Layer 3 — `doctrine_resolver.resolve_action_sequence` (DRG resolution)

Charter delegates to the doctrine resolver for the DRG traversal:

```python
# src/doctrine/resolvers/mission_type_resolver.py
def resolve_action_sequence(
    mission_type_id: str,
    layer_context: LayerContext,
) -> list[str]:
    """
    Resolves MissionType from the DRG chain and returns its action_sequence.

    LayerContext encapsulates: built-in layer root, org pack paths, project .kittify/ root.
    The charter module constructs LayerContext from repo_root; specify_cli never
    constructs it directly (ACL boundary).
    """
```

`LayerContext` is constructed by the charter module from `repo_root`. `specify_cli.next`
never constructs `LayerContext` directly; this preserves the ACL declared in C-004.

---

## Invariants

1. `_COMPOSED_ACTIONS_BY_MISSION` and `_COMPOSED_ACTIONS_FOR_PROMPT` do not exist
   after this mission is implemented. Any grep for these identifiers in the non-test
   source tree must return zero results.

2. `specify_cli.next` imports only from `charter.*`, never from `doctrine.*` directly.
   The existing `test_layer_rules.py` architectural test must remain green.

3. `resolve_action_sequence` is a pure function of its inputs. Given identical
   `(mission_type_id, layer_context)`, it always returns the same sequence.
   It performs no I/O beyond reading YAML from the resolved layer paths.

4. If `mission_type_id` is not found in any layer, `UnknownMissionTypeError` is raised
   with the queried ID and the list of registered IDs from all active layers.

5. If a referenced step ID in `action_sequence` has no corresponding `MissionStep`
   definition in the resolved layer set, `MissionTypeStepResolutionError` is raised
   with the missing step ID and the mission type ID, before any dispatch occurs.

---

## Behavioral Contracts (Given/When/Then)

### Contract A — Built-in mission type, no overrides

```
Given: a software-dev mission with no org or project overrides active
When:  spec-kitty next --agent X --mission <slug> is invoked
Then:  charter.resolve_action_sequence("software-dev", repo_root)
       returns ["specify", "plan", "tasks", "implement", "review", "merge"]
       and decide_next_via_runtime dispatches the correct step
       and _COMPOSED_ACTIONS_BY_MISSION is not consulted
```

### Contract B — Project override adds a step

```
Given: a project-level override at .kittify/overrides/mission-types/software-dev.yaml
       that extends: software-dev and appends "executive-summary" to action_sequence
When:  spec-kitty next is invoked after "merge" completes
Then:  charter.resolve_action_sequence("software-dev", repo_root)
       returns ["specify", "plan", "tasks", "implement", "review", "merge", "executive-summary"]
       and spec-kitty next dispatches "executive-summary"
```

### Contract C — Unknown step ID in action_sequence

```
Given: a mission-type override whose action_sequence contains "nonexistent-step"
       and no MissionStep definition for "nonexistent-step" exists in any layer
When:  charter.resolve_action_sequence is called
Then:  MissionTypeStepResolutionError is raised with step_id="nonexistent-step"
       before any dispatch occurs
       and spec-kitty next exits non-zero with a structured error JSON payload
```

---

## Migration Note

The content of the existing `_COMPOSED_ACTIONS_BY_MISSION` tables becomes the
`action_sequence` field in the built-in `MissionType` definition files:

| Current table entry | Shipped file target |
|---------------------|---------------------|
| `"software-dev": frozenset({...})` | `src/doctrine/missions/mission-types/software-dev.yaml` |
| `"documentation": frozenset({...})` | `src/doctrine/missions/mission-types/documentation.yaml` |
| `"research": frozenset({...})` | `src/doctrine/missions/mission-types/research.yaml` |
| `"plan": frozenset({...})` | `src/doctrine/missions/mission-types/plan.yaml` |

The migration must preserve the frozenset members verbatim as the initial
`action_sequence` values, ensuring NFR-002 (zero regression for existing missions).
