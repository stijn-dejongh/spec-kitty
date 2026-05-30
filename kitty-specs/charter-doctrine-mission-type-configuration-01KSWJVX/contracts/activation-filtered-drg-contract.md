# Contract: Activation-Filtered DRG Traversal

**Mission**: `charter-doctrine-mission-type-configuration-01KSWJVX`
**Addresses**: FR-018
**Status**: Proposed

---

## Activation Filter Model

DRG traversal is activation-filtered. Before the resolver begins traversing the
`built-in → org → project` chain, the charter module resolves the activation set from the
project charter and passes it to the resolver as a filter (part of `PackContext`).

Only artifacts that are **explicitly activated** in the project charter are included in the
resolved governance set. "Activated" and "registered" are synonyms.

This applies to **all artifact kinds**: directives, tactics, mission types, mission steps,
agent profiles, toolguides, and templates.

Non-activated artifacts are non-canonical: they are invisible to all charter-mediated
resolution and will not be returned by any charter public API. They can only be loaded
explicitly via the doctrine module API on direct user request.

---

## Invariants

1. The charter module resolves the activation set **before** DRG traversal begins.
2. An artifact present in a built-in pack but not activated in the project charter is
   excluded from all charter-mediated resolution results.
3. The activation filter is passed to the doctrine resolver as part of `PackContext`; the
   resolver itself does not read the project charter (C-004, C-005).
4. FR-019's upgrade migration ensures existing pre-upgrade projects activate all built-in
   mission types so they are not silently excluded after upgrade.
5. A project that has activated zero mission types produces an empty
   `charter.existing_mission_types(repo_root)` result — this is valid and not an error.

---

## Behavioral Contracts (Given/When/Then)

### Contract A — Non-activated built-in mission type is invisible to charter resolution

```
Given: built-in mission types: [software-dev, documentation, research, plan]
  and: project charter activates only: [software-dev, research]
When:  charter.existing_mission_types(repo_root) is called
Then:  the returned list is ["software-dev", "research"]
       "documentation" and "plan" are absent
  and: spec-kitty mission create --mission-type documentation raises UnknownMissionTypeError
```

### Contract B — Non-activated built-in agent profile directive is excluded

```
Given: built-in agent profile "architect-alphonso" declares directive DIR-ALPHONSO
  and: "architect-alphonso" is NOT activated in the project charter
  and: the active mission is "software-dev"
When:  charter resolves the governance context for the software-dev mission
Then:  DIR-ALPHONSO does NOT appear in the resolved directive set
       it is excluded because architect-alphonso is not activated
```

### Contract C — Activation of an artifact makes it visible immediately

```
Given: "documentation" mission type is NOT activated in the project charter
  and: spec-kitty mission create --mission-type documentation raises UnknownMissionTypeError
When:  the user activates "documentation" in the project charter
  and: charter.existing_mission_types(repo_root) is called again
Then:  "documentation" now appears in the returned list
  and: spec-kitty mission create --mission-type documentation succeeds
```

### Contract D — Non-activated org-pack directive is excluded from governance

```
Given: org pack "enterprise-pack" declares required_directives: [ENT-001, ENT-002]
  and: "enterprise-pack" is NOT activated in the project charter
When:  charter resolves the governance context for any mission
Then:  ENT-001 and ENT-002 do NOT appear in the resolved directive set
       the org pack is ignored entirely because it is not activated
```

### Contract E — Post-upgrade migration: built-in types activated for existing projects

```
Given: a project created before this mission that has no mission-type activation entries
         in its charter (pre-upgrade state)
When:  spec-kitty upgrade runs the FR-019 migration
Then:  the project charter is updated to activate
         [software-dev, documentation, research, plan]
  and: all other existing charter configuration is preserved unchanged
  and: charter.existing_mission_types(repo_root) returns
         ["software-dev", "documentation", "research", "plan"]
```
