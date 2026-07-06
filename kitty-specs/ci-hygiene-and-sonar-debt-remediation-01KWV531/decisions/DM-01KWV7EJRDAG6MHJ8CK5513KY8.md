# Decision Moment `01KWV7EJRDAG6MHJ8CK5513KY8`

- **Mission:** `ci-hygiene-and-sonar-debt-remediation-01KWV531`
- **Origin flow:** `plan`
- **Slot key:** `plan.sonar.project-version-source`
- **Input key:** `project_version_source`
- **Status:** `resolved`
- **Created:** `2026-07-06T08:06:55.501210+00:00`
- **Resolved:** `2026-07-06T08:10:56.726556+00:00`
- **Opened by:** `cli`
- **Other answer:** `false`

## Question

sonar.projectVersion should derive from pyproject.toml's current version (updates every dev-cycle-open, mid-cycle reads the next unreleased version) or the most recent git tag (only updates at actual release)?

## Options

- pyproject.toml current version
- most recent git tag
- Other

## Final answer

pyproject.toml current version

## Rationale

_(none)_

## Change log

- `2026-07-06T08:06:55.501210+00:00` — opened
- `2026-07-06T08:10:56.726556+00:00` — resolved (final_answer="pyproject.toml current version")
