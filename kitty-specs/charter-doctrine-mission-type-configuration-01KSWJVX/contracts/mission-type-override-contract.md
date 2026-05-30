# Contract: Mission-Type Override Extending a Built-In Type

**Mission**: `charter-doctrine-mission-type-configuration-01KSWJVX`
**Addresses**: FR-008 (Scenario 1 — project override extends built-in)
**Status**: Proposed

---

## Override Model

A project or org layer can define a mission-type override in two modes:

| Mode | Marker | Semantics |
|---|---|---|
| **Extend** | `extends: <built-in-id>` present | Base `action_sequence` is inherited; overlay may add, remove, or reorder steps |
| **Replace** | No `extends:` | Override supplies the complete `action_sequence`; built-in definition is ignored |

`action_sequence` is resolved **live** at each `spec-kitty next` invocation. It is never
frozen at mission create time.

---

## Invariants

1. `action_sequence` in the resolved mission type must be non-empty.
2. All step IDs in `action_sequence` must be unique within that sequence.
3. Step removal is explicitly permitted in an override.
4. When an override that removes a step is activated via `spec-kitty charter activate`,
   and at least one in-flight mission is currently in the lane corresponding to the
   removed step, a structured warning is emitted identifying the affected missions and
   the removed step. Activation completes regardless.
5. Built-in mission-type definitions are immutable at runtime (C-006). Overrides shadow;
   they never mutate the built-in artifact on disk.

---

## Behavioral Contracts (Given/When/Then)

### Contract A — Project override adds a step to built-in software-dev

```
Given: built-in "software-dev" with
         action_sequence: [discovery, specify, plan, implement, review, done]
  and: project override at .kittify/overrides/mission-types/software-dev.yaml with
         extends: software-dev
         action_sequence: [discovery, specify, plan, implement, security-scan, review, done]
  and: the "software-dev" mission type is activated in the project charter
When:  spec-kitty next resolves the action sequence for an active software-dev mission
Then:  the resolved sequence is
         [discovery, specify, plan, implement, security-scan, review, done]
       the built-in definition on disk is unchanged
```

### Contract B — Project override removes a step, no in-flight missions affected

```
Given: built-in "software-dev" with
         action_sequence: [discovery, specify, plan, implement, review, done]
  and: project override with
         extends: software-dev
         action_sequence: [discovery, specify, plan, implement, done]
         (review step removed)
  and: no missions are currently in the "review" lane
When:  spec-kitty charter activate is run with the override
Then:  activation completes with no warning
  and: spec-kitty next resolves action_sequence as
         [discovery, specify, plan, implement, done]
```

### Contract C — Override activated with in-flight missions in removed step's lane

```
Given: built-in "software-dev" with action_sequence including "review"
  and: a project override that removes "review" from action_sequence
  and: mission "mission-abc" is currently in the "review" lane
When:  spec-kitty charter activate is run with the override
Then:  a structured warning is emitted:
         "Override removes step 'review'; mission 'mission-abc' is currently in that lane."
  and: activation completes (warning does not block)
  and: spec-kitty next for "mission-abc" resolves the new sequence (review absent)
```

### Contract D — Full replacement override (no extends)

```
Given: built-in "software-dev" with action_sequence: [discovery, specify, plan, implement, review, done]
  and: project override with NO extends: key and
         action_sequence: [intake, build, ship]
  and: the "software-dev" mission type is activated in the project charter
When:  spec-kitty next resolves the action sequence for an active software-dev mission
Then:  the resolved sequence is [intake, build, ship]
       the built-in sequence is entirely ignored (full replacement semantics)
```

### Contract E — action_sequence must be non-empty

```
Given: a project override for "software-dev" with
         extends: software-dev
         action_sequence: []
When:  charter validates the override at activate time
Then:  a structured validation error is raised:
         "action_sequence must be non-empty"
       activation is rejected; the previous charter state is preserved
```
