---
work_package_id: WP09
title: '`applies` retype and relation gate'
dependencies:
- WP08
requirement_refs:
- FR-012
- NFR-002
planning_base_branch: remediation/doctrine-silence-guards
merge_target_branch: remediation/doctrine-silence-guards
branch_strategy: Planning artifacts for this mission were generated on remediation/doctrine-silence-guards. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into remediation/doctrine-silence-guards unless the human explicitly redirects the landing branch.
subtasks:
- T046
- T047
- T048
- T049
phase: Phase 3 - Guidance
history:
- at: '2026-07-26T19:45:15Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: doctrine-daphne
authoritative_surface: src/doctrine/agent_profiles/built-in/doctrine-daphne.agent.yaml
create_intent:
- tests/architectural/test_no_authored_applies_edge.py
execution_mode: code_change
model: ''
owned_files:
- src/doctrine/agent_profiles/built-in/doctrine-daphne.agent.yaml
- src/doctrine/agent_profile.graph.yaml
- tests/architectural/test_no_authored_applies_edge.py
role: implementer
tags: []
task_type: implement
tracker_refs: []
---

# Work Package Prompt: WP09 – `applies` retype and relation gate

## ⚡ Do This First: Load Agent Profile

Load the `doctrine-daphne` profile via `/ad-hoc-profile-load` and behave according to its guidance before parsing the rest of this prompt.

---

## Objectives & Success Criteria

- `procedure:onboard-external-agent-to-pack` has a traversable inbound edge.
- A newly-authored `applies` edge fails a gate.

**Requirement refs**: FR-012, NFR-002, SC-010

## Context & Constraints

Exactly one `applies` edge exists: `agent_profile:doctrine-daphne --applies--> procedure:onboard-external-agent-to-pack`. It is that procedure's **only** inbound edge, which makes daphne's own operating procedure unreachable.

This is the **one** WP in the mission that changes a graph relation — the single ledgered exception to NFR-004.

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

### Subtask T046 – Failing-first test.

The procedure is currently unreachable. Prove it.

### Subtask T047 – Retype the edge.

To a relation traversal actually reads.

### Subtask T048 – Gate the relation.

No newly-authored `applies` edge. **Build it on measurement, not on the wrong comment at `drg/merge.py:97-98`.**

### Subtask T049 – Ledger the change.

Golden counts: cardinality unchanged, relation changed. Record the entry.

## Test Strategy

- `PYTHONPATH=src python -m pytest tests/architectural/test_no_authored_applies_edge.py -q`
- Graph check: 311 nodes / 774 edges, with the relation histogram change ledgered.

## Risks & Mitigations

- Retyping changes a live traversal result — that is the point, but it must be ledgered, not slipped in.
- The `applies` relation is still produced by `project_drg.py`; the gate targets **newly-authored** edges, not the relation's existence.

## Review Guidance

- Verify red→green: the WP's first commit was RED on `remediation/doctrine-silence-guards` and is GREEN at the final commit.
- Verify every gate added is **non-vacuous**: it must reject a planted violation, and its allowlist must be empty.
- Verify the graph invariant where the WP claims it (311 nodes / 774 edges).

## Activity Log

> **CRITICAL**: entries in chronological order, oldest first. **Append** new entries at the END.

- 2026-07-26T19:45:15Z – system – Prompt created.
