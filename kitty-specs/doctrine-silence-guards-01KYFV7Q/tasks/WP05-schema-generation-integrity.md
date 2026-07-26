---
work_package_id: WP05
title: Schema-generation integrity
dependencies:
- WP01
requirement_refs:
- FR-005
planning_base_branch: remediation/doctrine-silence-guards
merge_target_branch: remediation/doctrine-silence-guards
branch_strategy: Planning artifacts for this mission were generated on remediation/doctrine-silence-guards. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into remediation/doctrine-silence-guards unless the human explicitly redirects the landing branch.
subtasks:
- T023
- T024
- T025
- T026
- T027
phase: Phase 1 - Guards
history:
- at: '2026-07-26T19:45:15Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: python-pedro
authoritative_surface: scripts/generate_schemas.py
create_intent:
- tests/doctrine/test_schema_generation_integrity.py
execution_mode: code_change
model: ''
owned_files:
- scripts/generate_schemas.py
- src/doctrine/schemas/paradigm.schema.yaml
- src/doctrine/schemas/tactic.schema.yaml
- src/doctrine/schemas/directive.schema.yaml
- src/doctrine/schemas/procedure.schema.yaml
- src/doctrine/schemas/styleguide.schema.yaml
- src/doctrine/schemas/toolguide.schema.yaml
- src/doctrine/schemas/mission.schema.yaml
- tests/doctrine/test_schema_generation_integrity.py
role: implementer
tags: []
task_type: implement
tracker_refs: []
---

# Work Package Prompt: WP05 – Schema-generation integrity

## ⚡ Do This First: Load Agent Profile

Load the `python-pedro` profile via `/ad-hoc-profile-load` and behave according to its guidance before parsing the rest of this prompt.

---

## Objectives & Success Criteria

- `scripts/generate_schemas.py --check` **exits 0** on the reconciled tree.
- `structural_lint_config` is emitted by the generator; `point_in_time_marker` has a recorded adjudication.

**Requirement refs**: FR-005, SC-004

## Context & Constraints

Measured: `--check` **exits 1 today with 7 stale schemas**. Three divergence classes, **only one safe to accept**.

| Divergence | Disposition |
|---|---|
| `enhances`/`overrides` removed | **Safe** — finishes a half-done excision |
| `structural_lint_config` removed | **Generator bug — fix the generator.** It is a real declared field (`styleguides/models.py:92`) the generator fails to emit; accepting the deletion invalidates `common-docs.styleguide.yaml` |
| `point_in_time_marker` removed | Declared in **no model**, used by a shipped artefact — **adjudicate** |

**Binding, every WP in this mission:**

- **Never run the full `tests/architectural/` directory** (C-003) — a known harness issue kills the session. Targeted single-file runs only.
- The 6 inherited `arch-adversarial` reds stay red (C-004). No greenwashing, no retry-to-green.
- **ATDD (C-006)**: the failing test is the **first commit** of this WP, RED on the planning base and GREEN at the final commit.
- New code passes `ruff` and `mypy --strict` with zero issues. No `# noqa` / `# type: ignore` to get there.
- Charter: `.kittify/charter/charter.md`. Spec: `../spec.md`. Plan: `../plan.md`. Manifest: `../tasks.md`.

## Branch Strategy

- **Planning base branch**: `remediation/doctrine-silence-guards`
- **Merge target branch**: `remediation/doctrine-silence-guards` → draft PR to `main`; the operator merges.

## Subtasks & Detailed Guidance

### Subtask T023 – Failing-first test.

`--check` exits 1 with 7 stale schemas. Pin it.

### Subtask T024 – Fix the generator.

Emit `structural_lint_config`. **Do not accept its deletion** — that would invalidate a shipped artefact.

### Subtask T025 – Adjudicate `point_in_time_marker`.

Declared in no model, used by a shipped artefact — silently ignored today because the models lack `extra="forbid"`. Either add it to the model or remove it from the artefact. **Decide and record; do not regenerate blindly.**

### Subtask T026 – Verify the `paradigm_reference` rename.

A definition rename `reference` → `paradigm_reference`; confirm every `$ref` target resolves. `mission_step_template_ref` is newly emitted.

### Subtask T027 – Regenerate.

The 7 stale schemas, after T024–T026 — not before.

## Test Strategy

- `PYTHONPATH=src python scripts/generate_schemas.py --check` → must exit 0
- `PYTHONPATH=src python -m pytest tests/doctrine/ -q`

## Risks & Mitigations

- **Wiring the gate before this reconciliation puts a red gate on the branch** and invites someone to 'fix' it by accepting a regeneration that deletes valid schema. That is why WP10 does the wiring, after this lands.
- T025 is a judgement call — record the reasoning, do not silently pick.

## Review Guidance

- Verify red→green: the WP's first commit was RED on `remediation/doctrine-silence-guards` and is GREEN at the final commit.
- Verify every gate added is **non-vacuous**: it must reject a planted violation, and its allowlist must be empty.
- Verify the graph invariant where the WP claims it (311 nodes / 774 edges).

## Activity Log

> **CRITICAL**: entries in chronological order, oldest first. **Append** new entries at the END.

- 2026-07-26T19:45:15Z – system – Prompt created.
