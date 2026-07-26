---
work_package_id: WP01
title: Zero-producer lint
dependencies: []
requirement_refs:
- FR-001
- NFR-001
- C-001
planning_base_branch: remediation/doctrine-silence-guards
merge_target_branch: remediation/doctrine-silence-guards
branch_strategy: Planning artifacts for this mission were generated on remediation/doctrine-silence-guards. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into remediation/doctrine-silence-guards unless the human explicitly redirects the landing branch.
base_branch: kitty/mission-doctrine-silence-guards-01KYFV7Q
base_commit: 28784aa4ef1a692118ca16f29b40356371dfd76e
created_at: '2026-07-26T20:33:34.662287+00:00'
subtasks:
- T001
- T002
- T003
- T004
- T005
phase: Phase 1 - Guards
history:
- at: '2026-07-26T19:45:15Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: python-pedro
authoritative_surface: tests/architectural/
create_intent:
- tests/architectural/test_no_inert_schema_slots.py
execution_mode: code_change
model: ''
owned_files:
- tests/architectural/test_no_inert_schema_slots.py
role: implementer
tags: []
task_type: implement
tracker_refs: []
---

# Work Package Prompt: WP01 – Zero-producer lint

## ⚡ Do This First: Load Agent Profile

Load the `python-pedro` profile via `/ad-hoc-profile-load` and behave according to its guidance before parsing the rest of this prompt.

---

## Objectives & Success Criteria

- A schema slot with no producer fails a test, naming the slot and the model that declares it.
- The lint passes on the shipped tree with a **zero-entry allowlist**.
- The lint is itself non-vacuous: a planted producerless slot makes it RED.

**Requirement refs**: FR-001, NFR-001, C-001, SC-001

## Context & Constraints

**Rank 1** in the sequencing authority and the first package in this mission: it is what proves every gate the later WPs add is not itself inert.

Governing precedent: **a schema slot without a producer and a coverage gate in the same commit goes silently inert — 3 for 3 in this repo, one of them for 162 days behind green tests.**

It directly guards mission B1's `impacts` / `is_symmetric` and mission B2's `aliases`.

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

### Subtask T001 – Define "slot" and "producer", in the module docstring.

**The earlier definition was self-annihilating and is withdrawn.** It read: *"a slot is both a
Pydantic model field and a JSON-Schema property; a producer is any writer under `src/` or the
generated schemas."* Since slots are a subset of schema properties and producers included the
generated schemas, **every slot had a producer by construction** — the lint would return the empty
set on any tree and its zero-entry allowlist would pass vacuously. The gate meant to prevent a
fourth inert mechanism would have been the fourth inert mechanism.

**Adopted definition.** A **slot** is a declared field — a Pydantic model field or a JSON-Schema
property. A **producer** is *a code path under `src/` that assigns the field on an object which is
subsequently serialised*. **The generated schemas are explicitly NOT producers**; they are the thing
being checked. The docstring must state the negative case — what a producerless slot looks like —
before implementation begins.

**Two live calibration anchors, both found in this mission and both must be adjudicated in the
docstring** (they pull in opposite directions, which is what makes them useful):
- `point_in_time_marker` — in `styleguide.schema.yaml` but declared in **no model** (WP05/T025). Under a model∩schema definition it is not a slot at all, so the lint cannot see the mission's only genuine specimen.
- `structural_lint_config` — declared in `styleguides/models.py` and present in the schema, but its only code contact is a **reader** (`assets/built-in/docs_structural_lint.py`). Under a strict writer-only reading the lint **flags it** — while WP05/T024 is simultaneously defending it as valid.

WP01 and WP05 must not land contradictory verdicts on the same field. Calibrate against the three known-inert historical cases rather than invented fixtures — a definition too narrow passes everything, too broad false-reds on legitimately read-only fields. Record the definition and its calibration in the docstring so a later reader can challenge it.

### Subtask T002 – Failing-first test.

Plant a producerless slot in a temp tree and assert the lint reports it. **This RED is the deliverable** — it is the proof the silence exists. Commit it before any implementation.

### Subtask T003 – Implement the lint.

New module under `tests/architectural/`. Walk model fields and schema properties; resolve producers; report unmatched slots with slot name + declaring model.

### Subtask T004 – Self-mutation test (NFR-001).

The lint's own gate must reject a planted violation. A gate-unmask cannot self-validate.

### Subtask T005 – Green on the shipped tree.

Allowlist must have exactly 0 entries. If the shipped tree genuinely has an inert slot, that is a finding to report — not an allowlist entry.

## Test Strategy

- `PYTHONPATH=src python -m pytest tests/architectural/test_no_inert_schema_slots.py -q`
- Never run the full `tests/architectural/` directory (C-003).

## Risks & Mitigations

- **A lint with the wrong definition is worse than none, because it looks like coverage.** Calibrate against real historical inert slots.
- If the definition proves unworkable, say so and re-scope — do not ship a lint that passes vacuously.

## Review Guidance

- Verify red→green: the WP's first commit was RED on `remediation/doctrine-silence-guards` and is GREEN at the final commit.
- Verify every gate added is **non-vacuous**: it must reject a planted violation, and its allowlist must be empty.
- Verify the graph invariant where the WP claims it (311 nodes / 774 edges).

## Activity Log

> **CRITICAL**: entries in chronological order, oldest first. **Append** new entries at the END.

- 2026-07-26T19:45:15Z – system – Prompt created.
