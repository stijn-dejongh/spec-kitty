---
work_package_id: WP08
title: org→DRG bridge integrity
dependencies:
- WP04
requirement_refs:
- FR-010
- FR-011
planning_base_branch: remediation/doctrine-silence-guards
merge_target_branch: remediation/doctrine-silence-guards
branch_strategy: Planning artifacts for this mission were generated on remediation/doctrine-silence-guards. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into remediation/doctrine-silence-guards unless the human explicitly redirects the landing branch.
subtasks:
- T041
- T042
- T043
- T044
- T045
phase: Phase 2 - Boundaries
history:
- at: '2026-07-26T19:45:15Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: architect-alphonso
authoritative_surface: src/doctrine/drg/merge.py
create_intent:
- tests/doctrine/drg/test_org_drg_bridge.py
execution_mode: code_change
model: ''
owned_files:
- src/doctrine/drg/merge.py
- src/doctrine/drg/org_pack_loader.py
- CLAUDE.md
- tests/doctrine/drg/test_org_drg_bridge.py
role: implementer
tags: []
task_type: implement
tracker_refs: []
---

# Work Package Prompt: WP08 – org→DRG bridge integrity

## ⚡ Do This First: Load Agent Profile

Load the `architect-alphonso` profile via `/ad-hoc-profile-load` and behave according to its guidance before parsing the rest of this prompt.

---

## Objectives & Success Criteria

- An unresolvable cross-layer edge fails loudly with a conflict record, never `None`-with-silence.
- The documented `specializes_from` snippet produces an edge.

**Requirement refs**: FR-010, FR-011, SC-009

## Context & Constraints

ADR `2026-07-26-3` is explicit: **the bridge fix must land before or with the `Relation.IMPACTS` migration**, or the new relation inherits a silent-drop path.

Three measured defects: a built-in-source → pack-target edge returns `None` with no warning and no conflict record; a bare built-in target id is blindly re-kinded to a node that may not exist; a URN-shaped target dies with a raw pydantic error instead of a typed pack error.

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

### Subtask T041 – Failing-first test.

A built-in-source → pack-target edge currently returns `None` silently. Prove it.

### Subtask T042 – Emit a conflict record.

Instead of `None`. The pack author must see the drop.

### Subtask T043 – Stop blind re-kinding.

A bare built-in target id must not be re-kinded to a node that may not exist.

### Subtask T044 – Typed pack error on URN-shaped targets.

Not raw pydantic.

### Subtask T045 – Fix the documented example (FR-011).

The `urn:profile:` `specializes_from` snippet in `CLAUDE.md` is silently dropped today — documentation that yields an inert declaration.

## Test Strategy

- `PYTHONPATH=src python -m pytest tests/doctrine/drg/ -q`

## Risks & Mitigations

- **`applies` is not a dead sink** — the comment at `drg/merge.py:97-98` is **wrong**. `charter_runtime/lint/checks/orphan.py` reads it and `charter/synthesizer/project_drg.py` produces it. Do not build anything on that comment (WP09 depends on this).
- Making previously-silent drops loud may surface existing broken pack edges. Each is a finding, not a reason to soften the error.

## Review Guidance

- Verify red→green: the WP's first commit was RED on `remediation/doctrine-silence-guards` and is GREEN at the final commit.
- Verify every gate added is **non-vacuous**: it must reject a planted violation, and its allowlist must be empty.
- Verify the graph invariant where the WP claims it (311 nodes / 774 edges).

## Activity Log

> **CRITICAL**: entries in chronological order, oldest first. **Append** new entries at the END.

- 2026-07-26T19:45:15Z – system – Prompt created.
