# Decision Moment `01KSWJWNWDRCFZ18M7E3VAZSTR`

- **Mission:** `charter-doctrine-mission-type-configuration-01KSWJVX`
- **Origin flow:** `specify`
- **Slot key:** `specify.scope.issue-682-depth`
- **Input key:** `issue_682_implementation_depth`
- **Status:** `resolved`
- **Created:** `2026-05-30T13:59:00.749610+00:00`
- **Resolved:** `2026-05-30T13:59:08.165859+00:00`
- **Other answer:** `false`

## Question

How deep should the implementation of #682 (composable workflow sequencing) go?

## Options

- Narrowest slice (integrate action only)
- Full v1 schema (declarative workflow.yaml)
- Via mission-type profile action_sequence (backed by #883 infrastructure)
- Design-only (ADR + contracts)

## Final answer

action_sequence field in mission-type governance profile, backed by #883 infrastructure — no standalone workflow.yaml artifact

## Rationale

_(none)_

## Change log

- `2026-05-30T13:59:00.749610+00:00` — opened
- `2026-05-30T13:59:08.165859+00:00` — resolved (final_answer="action_sequence field in mission-type governance profile, backed by #883 infrastructure — no standalone workflow.yaml artifact")
