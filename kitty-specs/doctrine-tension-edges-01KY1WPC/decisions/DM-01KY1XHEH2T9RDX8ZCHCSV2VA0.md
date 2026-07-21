# Decision Moment `01KY1XHEH2T9RDX8ZCHCSV2VA0`

- **Mission:** `doctrine-tension-edges-01KY1WPC`
- **Origin flow:** `specify`
- **Slot key:** `specify.check.tension-under-all-active`
- **Input key:** `tension_under_all_active`
- **Status:** `deferred`
- **Created:** `2026-07-21T08:44:06.562757+00:00`
- **Resolved:** `2026-07-21T08:47:49.975243+00:00`
- **Opened by:** `cli`
- **Other answer:** `false`

## Question

consistency-check short-circuits to coherent=true when there is no explicit activation list (backward-compat all-active). Should the tension check run under implicit all-active too (making FR-011 reconciliation artefact load-bearing and SC-002 a live assertion), or only under explicit activation?

## Options

- run-under-all-active-too
- only-under-explicit-activation

## Final answer

_(none)_

## Rationale

Escalated to operator: tension check semantics under implicit all-active activation — determines FR-011 load-bearing-ness.

## Change log

- `2026-07-21T08:44:06.562757+00:00` — opened
- `2026-07-21T08:47:49.975243+00:00` — deferred
