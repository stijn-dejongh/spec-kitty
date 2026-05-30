# Decision Moment `01KSWWZYGZ79D518YS9PDVVBGB`

- **Mission:** `charter-doctrine-mission-type-configuration-01KSWJVX`
- **Origin flow:** `plan`
- **Slot key:** `plan.scope.p1-vs-p2-delivery`
- **Input key:** `delivery_scope`
- **Status:** `resolved`
- **Created:** `2026-05-30T16:55:33.664056+00:00`
- **Resolved:** `2026-05-30T16:59:34.817482+00:00`
- **Other answer:** `false`

## Question

Should this plan target P1 requirements only (core doctrine layer, action sequence dispatch, step migration, activation filter, upgrade migration), or also include P2 (template list CLI, mission-type list/show CLI, template_set dict evolution, template DRG)?

## Options

- P1 only (P2 in separate mission)
- P1 + P2 together

## Final answer

P1 + P2 together. CLI surfaces clarified: 'spec-kitty doctrine mission-type list' enumerates all available doctrine mission types (regardless of activation); 'spec-kitty charter mission-type list' (alias 'spec-kitty mission-type list') shows only activated types.

## Rationale

_(none)_

## Change log

- `2026-05-30T16:55:33.664056+00:00` — opened
- `2026-05-30T16:59:34.817482+00:00` — resolved (final_answer="P1 + P2 together. CLI surfaces clarified: 'spec-kitty doctrine mission-type list' enumerates all available doctrine mission types (regardless of activation); 'spec-kitty charter mission-type list' (alias 'spec-kitty mission-type list') shows only activated types.")
