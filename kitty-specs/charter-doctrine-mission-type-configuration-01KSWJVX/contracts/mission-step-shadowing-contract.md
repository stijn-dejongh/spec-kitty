# Contract: MissionStep Override Shadowing

**Mission**: `charter-doctrine-mission-type-configuration-01KSWJVX`
**Addresses**: FR-012
**Status**: Proposed

---

## Shadowing Model

Individual `MissionStep` definitions can be overridden at the org or project layer.
The shadowing key is the **compound path** `{mission_type_id}/{step_id}`.

On-disk locations by layer:

| Layer | Path |
|---|---|
| Built-in | `src/doctrine/missions/mission-steps/{mission_type_id}/{step_id}.yaml` |
| Org pack | `<pack-root>/mission-steps/{mission_type_id}/{step_id}.yaml` |
| Project | `.kittify/overrides/mission-steps/{mission_type_id}/{step_id}.yaml` |

Resolution follows the standard `built-in → org → project` precedence: project shadow
wins over org shadow, which wins over built-in.

---

## Invariants

1. Shadowing is **scoped by compound key**. A `software-dev/review.yaml` override shadows
   only the `review` step of `software-dev`. The `review` step of any other mission type
   (e.g., `documentation/review.yaml`) is unaffected.
2. Two `MissionStep` instances with the same `step_id` in different mission types are
   **independent entities** with independent content and independent shadowing keys.
3. A project-layer shadow takes precedence over an org-layer shadow for the same compound
   key; the built-in definition is never mutated (C-006).
4. The `MissionStep` entity has no globally unique identity on `step_id` alone — its
   identity is always `(mission_type_id, step_id)`.

---

## Behavioral Contracts (Given/When/Then)

### Contract A — Project step override shadows built-in for the correct mission type only

```
Given: built-in step "software-dev/review.yaml" with
         prompt_template: src/doctrine/missions/mission-steps/software-dev/review.yaml
  and: built-in step "documentation/review.yaml" with a different prompt_template
  and: project override at
         .kittify/overrides/mission-steps/software-dev/review.yaml
         with a custom prompt_template
  and: both "software-dev" and "documentation" are activated
When:  doctrine_resolver resolves the "review" step for a software-dev mission
Then:  the project override prompt_template is returned (project wins over built-in)
  and: the "review" step for a documentation mission returns the built-in
         documentation/review.yaml template (unaffected by the software-dev shadow)
```

### Contract B — Org-layer shadow wins over built-in; project shadow wins over org

```
Given: built-in  "software-dev/specify.yaml"  with guidance: "Built-in guidance"
  and: org shadow "software-dev/specify.yaml"  with guidance: "Org guidance"
  and: project shadow absent for "software-dev/specify"
When:  doctrine_resolver resolves the "specify" step for a software-dev mission
Then:  guidance = "Org guidance"  (org wins over built-in)

Given: additionally, project shadow "software-dev/specify.yaml" with guidance: "Project guidance"
When:  doctrine_resolver resolves the "specify" step for a software-dev mission
Then:  guidance = "Project guidance"  (project wins over org and built-in)
```

### Contract C — Step identity is compound; same step_id in different types are independent

```
Given: "software-dev/review.yaml" has step_type: human_in_loop
  and: "documentation/review.yaml" has step_type: agent
When:  spec-kitty next resolves the "review" step for a software-dev mission
Then:  kind = decision_required  (human_in_loop mapping)

When:  spec-kitty next resolves the "review" step for a documentation mission
Then:  kind = step               (agent mapping)
       (the two "review" steps are independent entities)
```

### Contract D — Override file absent at a layer falls through to next layer

```
Given: built-in "software-dev/plan.yaml" exists
  and: no org-layer shadow for "software-dev/plan"
  and: no project-layer shadow for "software-dev/plan"
When:  doctrine_resolver resolves the "plan" step for a software-dev mission
Then:  the built-in "software-dev/plan.yaml" is returned
       no error is raised
```
