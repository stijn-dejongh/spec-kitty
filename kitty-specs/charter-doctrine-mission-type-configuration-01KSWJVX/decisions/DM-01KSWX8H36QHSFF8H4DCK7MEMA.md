# Decision Moment `01KSWX8H36QHSFF8H4DCK7MEMA`

- **Mission:** `charter-doctrine-mission-type-configuration-01KSWJVX`
- **Origin flow:** `plan`
- **Slot key:** `plan.architecture.mission-step-on-disk-format`
- **Input key:** `mission_step_disk_format`
- **Status:** `resolved`
- **Created:** `2026-05-30T17:00:14.822871+00:00`
- **Resolved:** `2026-05-30T17:03:02.066089+00:00`
- **Other answer:** `false`

## Question

What is the on-disk format for MissionStep artifacts under src/doctrine/missions/mission-steps/{mission_type_id}/? The current command-templates are pure Markdown. Should each step be: (A) a single YAML file ({step_id}.yaml) with the prompt content embedded as a YAML field, or (B) a YAML descriptor ({step_id}.yaml) with a prompt_template path pointing to an adjacent Markdown file ({step_id}.md)?

## Options

- A — single YAML file, prompt embedded
- B — YAML descriptor + adjacent .md file

## Final answer

B — YAML descriptor + adjacent Markdown files, using directory-per-step layout following the existing actions/{id}/ pattern: mission-steps/{mission_type_id}/{step_id}/step.yaml (descriptor), {step_id}/prompt.md (verbatim command template), {step_id}/guidelines.md (optional). Shadowing key is the compound path {mission_type_id}/{step_id}/ (directory).

## Rationale

_(none)_

## Change log

- `2026-05-30T17:00:14.822871+00:00` — opened
- `2026-05-30T17:03:02.066089+00:00` — resolved (final_answer="B — YAML descriptor + adjacent Markdown files, using directory-per-step layout following the existing actions/{id}/ pattern: mission-steps/{mission_type_id}/{step_id}/step.yaml (descriptor), {step_id}/prompt.md (verbatim command template), {step_id}/guidelines.md (optional). Shadowing key is the compound path {mission_type_id}/{step_id}/ (directory).")
