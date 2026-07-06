# Decision Moment `01KWV7EKTEP05FJQC2W65GWJ3H`

- **Mission:** `ci-hygiene-and-sonar-debt-remediation-01KWV531`
- **Origin flow:** `plan`
- **Slot key:** `plan.census-gate.fix-mechanism`
- **Input key:** `census_gate_fix_mechanism`
- **Status:** `resolved`
- **Created:** `2026-07-06T08:06:56.590063+00:00`
- **Resolved:** `2026-07-06T08:10:57.804312+00:00`
- **Opened by:** `cli`
- **Other answer:** `false`

## Question

FR-001's census-gate fix: (a) move the LOC field out of the exact-equality census entirely into the existing _baselines.yaml growth-only-ratchet system, treating routing-structure and LOC-ratchet as independent concerns, or (b) keep census as one file but change its own assertion from equality to a floor+ratchet check inline?

## Options

- (a) split into _baselines.yaml ratchet
- (b) inline floor+ratchet on census itself
- Other

## Final answer

(a) split into _baselines.yaml ratchet

## Rationale

_(none)_

## Change log

- `2026-07-06T08:06:56.590063+00:00` — opened
- `2026-07-06T08:10:57.804312+00:00` — resolved (final_answer="(a) split into _baselines.yaml ratchet")
