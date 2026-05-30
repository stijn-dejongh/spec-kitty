# Contract: Directive Scope Resolution

**Mission**: `charter-doctrine-mission-type-configuration-01KSWJVX`
**Addresses**: FR-006, B-6 (adversarial review finding)
**Status**: Proposed

---

## Directive Scope Model

Directive scope is two-tier:

| Tier | Source | Scope |
|---|---|---|
| Project-scoped | `org-charter.yaml` → `required_directives` | All mission types in the project |
| Mission-type-scoped | `MissionType.governance_refs` | Only the mission type that declares them |

The resolved directive set for a given mission is:

```
resolved_directives(mission) =
    project_directives(org_charter)          # tier 1
    ∪ mission_type_directives(mission_type)  # tier 2
```

---

## Invariants

1. Org-charter `required_directives` are **always** project-scoped. They apply to every
   mission type in the project regardless of which mission type is active.

2. Software-dev-specific directives live in the `software-dev` mission-type's
   `governance_refs`. They do not appear in the resolved governance of
   `documentation`, `research`, `plan`, or any custom mission type unless that
   mission type's own `governance_refs` explicitly references them.

3. There is no implicit cross-injection: activating a `software-dev` mission does
   not add software-dev directives to a concurrently active `documentation` mission.

4. Directive removal is not permitted at any tier (C-002). Adding a directive in
   `governance_refs` never removes a project-scoped directive.

---

## Behavioral Contracts (Given/When/Then)

### Contract A — Org directive applies to all mission types

```
Given: an org pack with required_directives: [SWIFT_CSP, GDPR_HANDLING]
  and: an active compliance-audit mission (custom type)
  and: the compliance-audit MissionType.governance_refs does not reference SWIFT_CSP
When:  charter resolves the governance context for the compliance-audit mission
Then:  SWIFT_CSP and GDPR_HANDLING appear in the resolved directive set
       because they are project-scoped via org-charter
```

### Contract B — Software-dev directive does not leak to documentation

```
Given: a software-dev MissionType with governance_refs: [DIR-010, DIR-035]
  and: an active documentation mission
When:  charter resolves the governance context for the documentation mission
Then:  DIR-010 and DIR-035 do NOT appear in the resolved directive set
       because they are mission-type-scoped to software-dev
```

### Contract C — Mission-type-scoped directive stacks on project-scoped

```
Given: an org pack with required_directives: [SWIFT_CSP]
  and: a compliance-audit MissionType with governance_refs: [GDPR_HANDLING]
  and: an active compliance-audit mission
When:  charter resolves the governance context for the compliance-audit mission
Then:  resolved directives = {SWIFT_CSP, GDPR_HANDLING}
       SWIFT_CSP from tier 1 (project-scoped)
       GDPR_HANDLING from tier 2 (mission-type-scoped)
```
