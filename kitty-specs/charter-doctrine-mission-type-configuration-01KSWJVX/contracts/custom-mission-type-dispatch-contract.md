# Contract: Custom Mission Type Creation and `spec-kitty next` Dispatch

**Mission**: `charter-doctrine-mission-type-configuration-01KSWJVX`
**Addresses**: FR-009, FR-007
**Status**: Proposed

---

## Activation Model

A custom mission type is a `MissionType` artifact with an `id` not present in the built-in
set. It must be declared in the project's `.kittify/` layer (or an org pack) and explicitly
activated in the project charter before it is usable.

**Registered = Activated.** A mission type is registered if and only if it appears in the
project charter's activation list. Non-activated types are invisible to all
charter-mediated resolution and do not appear in `charter.existing_mission_types(repo_root)`.

---

## Invariants

1. `spec-kitty mission create --mission-type <id>` validates the type ID against the set
   returned by `charter.existing_mission_types(repo_root)` at create time.
2. An unregistered type ID raises `UnknownMissionTypeError` with the queried ID and the
   list of registered IDs. The mission is not created.
3. After a custom type is activated, `spec-kitty next` dispatches its `action_sequence`
   using the same call chain as built-in types:
   `specify_cli.next → charter.resolve_action_sequence(mission_type_id, repo_root)
   → doctrine_resolver.resolve_action_sequence(mission_type_id, layer_context)`
4. `specify_cli.next` never imports from `doctrine.*` directly (C-004).

---

## Behavioral Contracts (Given/When/Then)

### Contract A — Activated custom type accepted at mission create

```
Given: a custom mission type "compliance-audit" defined in
         .kittify/mission-types/compliance-audit.yaml
         with action_sequence: [scope, evidence-gather, assess, report]
  and: "compliance-audit" is activated in the project charter
When:  spec-kitty mission create --mission-type compliance-audit --name "Q3 Audit"
Then:  the mission is created with mission_type=compliance-audit in meta.json
  and: no error is raised
```

### Contract B — Unregistered type ID raises UnknownMissionTypeError

```
Given: "compliance-audit" is defined in .kittify/ but NOT activated in the charter
  and: charter.existing_mission_types(repo_root) returns ["software-dev", "research"]
When:  spec-kitty mission create --mission-type compliance-audit --name "Q3 Audit"
Then:  UnknownMissionTypeError is raised with:
         queried_id: "compliance-audit"
         registered_ids: ["software-dev", "research"]
  and: no mission is created
```

### Contract C — spec-kitty next dispatches custom action_sequence

```
Given: mission "mission-q3-audit" with mission_type=compliance-audit in meta.json
  and: "compliance-audit" activated with
         action_sequence: [scope, evidence-gather, assess, report]
  and: the mission's current lane is "scope" (first step)
When:  spec-kitty next --mission mission-q3-audit is run
Then:  the dispatch resolves via charter.resolve_action_sequence("compliance-audit", repo_root)
  and: the next step returned is "evidence-gather"
  and: no frozenset lookup occurs in specify_cli.next
  and: no direct doctrine.* import is used by specify_cli.next
```

### Contract D — charter.existing_mission_types returns only activated types

```
Given: built-in types "software-dev", "documentation", "research", "plan" — all activated
  and: "compliance-audit" defined in .kittify/ but NOT activated
When:  charter.existing_mission_types(repo_root) is called
Then:  the returned list is ["software-dev", "documentation", "research", "plan"]
       "compliance-audit" is absent
```
