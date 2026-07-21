# Decision Moment `01KY1XHCKPP44C33P5BJ7QJBPV`

- **Mission:** `doctrine-tension-edges-01KY1WPC`
- **Origin flow:** `specify`
- **Slot key:** `specify.migration.downstream-opposed-by-compat`
- **Input key:** `downstream_opposed_by_compat`
- **Status:** `deferred`
- **Created:** `2026-07-21T08:44:04.598646+00:00`
- **Resolved:** `2026-07-21T08:47:48.006653+00:00`
- **Opened by:** `cli`
- **Other answer:** `false`

## Question

Removing opposed_by from additionalProperties:false schemas hard-breaks any downstream/org-pack YAML that authored it. Accept the hard break (opposed_by was built-in-only, undocumented as a pack-author surface) or add a deprecation/migration path?

## Options

- accept-hard-break-and-record
- add-consumer-migration-or-deprecation-window

## Final answer

_(none)_

## Rationale

Escalated to operator: downstream/org-pack opposed_by compat policy (hard break vs deprecation) — product/compat decision.

## Change log

- `2026-07-21T08:44:04.598646+00:00` — opened
- `2026-07-21T08:47:48.006653+00:00` — deferred
