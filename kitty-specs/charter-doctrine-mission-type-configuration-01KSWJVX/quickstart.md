# Quickstart: Charter Doctrine Mission-Type Configuration

**Mission**: `charter-doctrine-mission-type-configuration-01KSWJVX`

---

## Scenario 1 — Add a step to an existing mission type (project layer)

**Goal**: Add a `security-scan` step to `software-dev` in a project without touching built-in code.

**1. Create the step artifact** in `.kittify/overrides/mission-steps/software-dev/security-scan/`:

```bash
mkdir -p .kittify/overrides/mission-steps/software-dev/security-scan
```

```yaml
# .kittify/overrides/mission-steps/software-dev/security-scan/step.yaml
id: security-scan
display_name: "Security Scan"
step_type: agent
prompt_template: prompt.md
agent_profile: security-reviewer
```

```markdown
<!-- .kittify/overrides/mission-steps/software-dev/security-scan/prompt.md -->
# Security Scan Step
Run SAST tooling and review output...
```

**2. Create the mission-type override** at `.kittify/overrides/mission-types/software-dev.yaml`:

```yaml
schema_version: 1
id: software-dev
extends: software-dev
action_sequence:
  - specify
  - plan
  - tasks
  - implement
  - security-scan
  - review
```

**3. Activate the override** in the project charter:

```bash
spec-kitty charter activate mission-type software-dev
```

**4. Verify**:

```bash
spec-kitty mission-type show software-dev
# action_sequence: [specify, plan, tasks, implement, security-scan, review]
# source: project (override)
```

**5. Run a mission** — `spec-kitty next` now dispatches `security-scan` after `implement`.

---

## Scenario 2 — Create a fully custom mission type

**Goal**: Create a `compliance-audit` mission type with its own step sequence.

**1. Define the MissionType** at `.kittify/overrides/mission-types/compliance-audit.yaml`:

```yaml
schema_version: 1
id: compliance-audit
display_name: "Compliance Audit"
action_sequence:
  - scope
  - evidence-gather
  - assess
  - report
governance_refs:
  - DIR-GDPR-001
```

**2. Create step artifacts** for each step in `.kittify/overrides/mission-steps/compliance-audit/`:

```bash
for step in scope evidence-gather assess report; do
  mkdir -p .kittify/overrides/mission-steps/compliance-audit/$step
  echo "id: $step" > .kittify/overrides/mission-steps/compliance-audit/$step/step.yaml
  echo "display_name: $step" >> .kittify/overrides/mission-steps/compliance-audit/$step/step.yaml
  echo "step_type: agent" >> .kittify/overrides/mission-steps/compliance-audit/$step/step.yaml
  echo "prompt_template: prompt.md" >> .kittify/overrides/mission-steps/compliance-audit/$step/step.yaml
  echo "# TODO: fill in prompt" > .kittify/overrides/mission-steps/compliance-audit/$step/prompt.md
done
```

**3. Activate** in the project charter:

```bash
spec-kitty charter activate mission-type compliance-audit
```

**4. Create a mission of the new type**:

```bash
spec-kitty mission create --mission-type compliance-audit --name "Q3 2026 Audit"
```

**5. Confirm type appears in the activated list**:

```bash
spec-kitty mission-type list
# ID                  SOURCE     DISPLAY NAME
# compliance-audit    project    Compliance Audit
# software-dev        built-in   Software Development
# ...
```

---

## Scenario 3 — Extend an org pack using `extends:`

**Goal**: Org pack `team-alpha` adds a directive on top of `corp-baseline`.

**`corp-baseline/org-charter.yaml`**:
```yaml
schema_version: 1
required_directives:
  - SWIFT_CSP
  - GDPR_HANDLING
interview_defaults:
  verbosity: concise
```

**`team-alpha/org-charter.yaml`**:
```yaml
schema_version: 1
extends: corp-baseline
required_directives:
  - DIR-035
interview_defaults:
  verbosity: verbose    # overrides corp-baseline value per-key
```

**Resolved governance for a team-alpha project:**
```
required_directives: [SWIFT_CSP, GDPR_HANDLING, DIR-035]
interview_defaults:   {verbosity: verbose}
```

---

## CLI Reference

```bash
# List all available doctrine mission types (regardless of activation)
spec-kitty doctrine mission-type list

# List only activated mission types for this project
spec-kitty mission-type list
# alias:
spec-kitty charter mission-type list

# Show fully resolved mission-type definition
spec-kitty mission-type show software-dev

# Activate a mission type
spec-kitty charter activate mission-type <id>

# Check what step sequence will be dispatched
spec-kitty mission-type show <id> --field action_sequence
```

---

## Validation

After any change, confirm the state is consistent:

```bash
# Confirm the resolved action sequence
spec-kitty mission-type show software-dev

# Confirm only activated types are visible
spec-kitty mission-type list

# Confirm charter is internally consistent
spec-kitty charter validate
```
