---
work_package_id: WP04
title: Close the ._inner reach-around
dependencies: []
requirement_refs:
- FR-010
planning_base_branch: feat/charter-sole-door-bypass-closure
merge_target_branch: feat/charter-sole-door-bypass-closure
branch_strategy: Planning artifacts for this mission were generated on feat/charter-sole-door-bypass-closure. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/charter-sole-door-bypass-closure unless the human explicitly redirects the landing branch.
subtasks:
- T015
- T016
- T017
phase: Phase 2 - Bypass closure
history:
- at: '2026-08-03T14:10:00Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: python-pedro
authoritative_surface: src/specify_cli/invocation/
create_intent:
- tests/specify_cli/invocation/test_no_inner_reacharound.py
execution_mode: code_change
model: ''
owned_files:
- src/specify_cli/invocation/registry.py
- src/specify_cli/invocation/org_profiles.py
- tests/specify_cli/invocation/test_no_inner_reacharound.py
role: implementer
tags: []
task_type: implement
tracker_refs: []
---

# Work Package Prompt: WP04 – Close the `._inner` reach-around

## ⚡ Do This First: Load Agent Profile

Use the `/ad-hoc-profile-load` skill to load `python-pedro` (implementer role, claude agent) before parsing
the rest of this prompt.

---

## ⚠️ IMPORTANT: Review Feedback

Check `review_ref` in the event log before starting. Address all feedback; log changes in the Activity Log.

---

## Objectives & Success Criteria

Close the escape hatch a post-plan squad delegate found: `service._inner.agent_profiles` reads the raw,
unfiltered repository directly, bypassing every gate WP01-03/WP07-09 add. Left open, this WP means the
mission's "sole door" claim is hollow — a genuinely gated 9-of-10 factory with a `._inner` side door is not
a sole door (FR-010).

**Success criteria**: zero `._inner` attribute access on a `charter.resolver.DoctrineService` instance
outside `src/charter/**`, proven by a test, not a one-time grep.

## Context & Constraints

- **Depends on WP01** — both sites need the new lineage/mutation accessor, not a re-derived reach-around
  workaround.
- These two sites exist specifically because the filtered `agent_profiles` property doesn't expose mutation
  (`register_overlay`) or raw lineage access — the same gap WP02's `projection.py`/`runtime_bridge_io.py`
  sites had. Use the *same* accessor, don't invent a second one.

## Branch Strategy

- **Strategy**: lane-per-WP (normalized by `finalize-tasks`)
- **Planning base branch**: feat/charter-sole-door-bypass-closure
- **Merge target branch**: feat/charter-sole-door-bypass-closure

## Subtasks & Detailed Guidance

### Subtask T015 – Migrate `registry.py:64`

- **Purpose**: `inner_repo = service._inner.agent_profiles` reaches past the gate for overlay
  registration/lineage purposes identical to WP02's `projection.py` need.
- **Steps**: Replace `service._inner.agent_profiles` with WP01's new public accessor. Confirm this site's
  existing doctrine-layer factory call (already correct, per FR-001's C-006 finding) is untouched — only the
  `._inner` reach is being closed, not the whole function rewritten.
- **Files**: `src/specify_cli/invocation/registry.py`.
- **Parallel?**: Yes.

### Subtask T016 – Migrate `org_profiles.py:117`

- **Purpose**: Same reach-around shape as T015, different call site.
- **Steps**: Replace `inner_repository = service._inner.agent_profiles` with WP01's accessor.
- **Files**: `src/specify_cli/invocation/org_profiles.py`.
- **Parallel?**: Yes.

### Subtask T017 – ATDD test: zero `._inner` access remains

- **Purpose**: Non-fakeable, red-first proof this closure holds.
- **Steps**: Write a test (RED first, against the pre-migration code) that AST-scans both files for
  `._inner` attribute access and asserts zero matches; run it, confirm it fails against the unmigrated code,
  then implement T015-T016 and confirm it passes.
- **Files**: `tests/specify_cli/invocation/test_no_inner_reacharound.py` (new).
- **Parallel?**: No — depends on T015-T016.
- **Notes**: This test is the seed for WP09's Gate 5 (the broader `._inner` architectural gate covering all
  of `src/`) — keep its AST-scan logic reusable/extractable if practical, but do not skip writing this
  narrower version now waiting for WP09.

## Test Strategy

- `pytest tests/specify_cli/invocation/ -v`.
- `mypy --strict src/specify_cli/invocation/registry.py src/specify_cli/invocation/org_profiles.py`.

## Risks & Mitigations

- **Reinventing a second accessor instead of reusing WP01's.** Mitigation: if WP01's accessor doesn't fit
  cleanly, that's a finding to report against WP01, not grounds for a parallel mechanism (C-001).

## Review Guidance

- Confirm both sites use the exact same accessor WP02 uses — not a lookalike.
- Confirm T017's test actually AST-scans (or otherwise non-fakeably proves absence), not a text grep on a
  known-good state.

## Activity Log

- 2026-08-03T14:10:00Z – system – Prompt created.
