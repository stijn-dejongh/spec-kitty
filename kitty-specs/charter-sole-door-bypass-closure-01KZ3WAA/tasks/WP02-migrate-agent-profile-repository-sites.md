---
work_package_id: WP02
title: Migrate AgentProfileRepository sites + NFR-005 measurement
dependencies: []
requirement_refs:
- FR-001
- NFR-005
planning_base_branch: feat/charter-sole-door-bypass-closure
merge_target_branch: feat/charter-sole-door-bypass-closure
branch_strategy: Planning artifacts for this mission were generated on feat/charter-sole-door-bypass-closure. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/charter-sole-door-bypass-closure unless the human explicitly redirects the landing branch.
subtasks:
- T006
- T007
- T008
- T009
- T010
phase: Phase 2 - Bypass closure
history:
- at: '2026-08-03T14:10:00Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: python-pedro
authoritative_surface: src/specify_cli/cli/commands/agent/tasks_status_cmd.py
create_intent:
- tests/perf/test_tasks_status_baseline.py
execution_mode: code_change
model: ''
owned_files:
- src/runtime/next/runtime_bridge_io.py
- src/specify_cli/tool_surface/profiles/projection.py
- src/specify_cli/cli/commands/agent/tasks_status_cmd.py
- src/charter/profile_resolution.py
- tests/perf/test_tasks_status_baseline.py
role: implementer
tags: []
task_type: implement
tracker_refs: []
---

# Work Package Prompt: WP02 – Migrate AgentProfileRepository sites + NFR-005 measurement

## ⚡ Do This First: Load Agent Profile

Use the `/ad-hoc-profile-load` skill to load `python-pedro` (implementer role, claude agent) before parsing
the rest of this prompt.

---

## ⚠️ IMPORTANT: Review Feedback

Check `review_ref` in the event log before starting. Address all feedback; log changes in the Activity Log.

---

## Objectives & Success Criteria

Close the 5 in-scope direct `AgentProfileRepository` construction sites (FR-001), and prove no perf
regression on the two sites whose removed "boundary ratchet" comment named a construction-cost concern
(NFR-005).

**Success criteria**:
- `runtime_bridge_io.py:576`, `projection.py:84`, `tasks_status_cmd.py:712`, `tasks_status_cmd.py:823`,
  `charter/profile_resolution.py:81` all route through `charter.resolver.DoctrineService` (or WP01's new
  accessor where lineage/mutation is needed) instead of constructing `AgentProfileRepository` directly.
- A pre-mission p95 latency baseline for `spec-kitty agent tasks status` is captured and recorded BEFORE
  `tasks_status_cmd.py` is touched; a post-migration measurement is within 10% of it.

## Context & Constraints

- **Depends on WP01** — the unified builder and the new lineage/mutation accessor must exist first.
- Read `research.md`'s R3 and R5 sections: the "boundary ratchet" comment is confirmed a red herring against
  the existing import-scanning gate; the real, unmeasured risk is construction cost — that is what T009
  measures.
- Two of these five sites need the accessor (lineage/mutation), not the plain gated property — check
  `research.md`'s per-site verdict table before writing each migration:
  - `runtime_bridge_io.py:576` needs `resolve_profile()` (lineage composition) → use the accessor.
  - `projection.py:84` needs `register_overlay()`/`get_ancestors()` (mutation + lineage) → use the accessor.
  - `tasks_status_cmd.py:712,823` and `profile_resolution.py:81` only need the gated `agent_profiles`
    property — no accessor needed.

## Branch Strategy

- **Strategy**: lane-per-WP (normalized by `finalize-tasks`)
- **Planning base branch**: feat/charter-sole-door-bypass-closure
- **Merge target branch**: feat/charter-sole-door-bypass-closure

## Subtasks & Detailed Guidance

### Subtask T006 – Capture the pre-mission p95 baseline

- **Purpose**: Make NFR-005's "within 10% of baseline" falsifiable — this MUST run before T007-T009 touch
  any of the migrated sites.
- **Steps**:
  1. Confirm or build a fixture project with 100+ work packages (check `tests/fixtures/` for an existing
     large-mission fixture before creating a new one).
  2. On the merge-base commit (before this WP's changes), run `spec-kitty agent tasks status --feature
     <fixture>` repeatedly (e.g. 10 runs) and record p95 wall-clock latency.
  3. Record the number in the mission's tracer file (`tooling-friction.md` or equivalent, per Standing
     Order #3) and in a new lightweight regression harness `tests/perf/test_tasks_status_baseline.py` that
     stores the baseline as a committed constant for T009 to compare against.
- **Files**: `tests/perf/test_tasks_status_baseline.py` (new).
- **Parallel?**: No — must run first, before T007-T009.
- **Notes**: This is measurement, not a code change to the production surfaces. Do not skip it — it is the
  only thing that makes T009's comparison meaningful.

### Subtask T007 – Migrate `runtime_bridge_io.py:576`

- **Purpose**: `_resolve_tech_stack_for_profile` needs `resolve_profile()` (lineage-composed), not the plain
  filtered dict.
- **Steps**: Replace the direct `AgentProfileRepository(...)` construction with WP01's new accessor on a
  `charter.resolver.DoctrineService` instance (built via the unified builder, `repo_root` already available
  as a function parameter). Call `.resolve_profile(profile_id)` on the accessor's returned repository, per
  the pattern already proven at `resolver.py:402-413`'s `resolve_governance_for_profile`.
- **Files**: `src/runtime/next/runtime_bridge_io.py`.
- **Parallel?**: Yes — different file from T008-T010.

### Subtask T008 – Migrate `projection.py:84`

- **Purpose**: `default_profile_repository` needs `register_overlay()`/`get_ancestors()` (mutation +
  lineage).
- **Steps**: Replace the direct construction with WP01's accessor. Confirm `register_overlay()` calls still
  mutate the correct underlying repository object and that subsequent `get_ancestors()` calls still resolve
  lineage correctly post-mutation.
- **Files**: `src/specify_cli/tool_surface/profiles/projection.py`.
- **Parallel?**: Yes.

### Subtask T009 – Migrate `tasks_status_cmd.py:712,823`; re-measure and compare

- **Purpose**: Close the two sites whose comment cited the (now-confirmed-non-blocking) boundary ratchet;
  prove NFR-005 holds.
- **Steps**:
  1. Replace both direct `AgentProfileRepository(...)` constructions with the gated `agent_profiles`
     property on a factory instance (no accessor needed — dashboard icon rendering only reads).
  2. Remove the "boundary ratchet" comment; replace with a one-line note citing why it was a false concern
     (function-local imports aren't scanned by the existing gate — cite `research.md` R3) — do not just
     delete the comment silently.
  3. Re-run the same p95 measurement from T006 against the migrated code, on the same fixture. If it
     regresses beyond 10%, do NOT accept it — add caching or lazy construction to close the gap (NFR-005 is
     explicit that the fix must be architectural, not accepted).
- **Files**: `src/specify_cli/cli/commands/agent/tasks_status_cmd.py`.
- **Parallel?**: No — must run after T006.

### Subtask T010 – Migrate `charter/profile_resolution.py:81`

- **Purpose**: `_default_agent_profile_repository`'s org-packs branch already has an activation-aware branch
  elsewhere in the module — this is the one remaining raw construction to close.
- **Steps**: Replace with the gated `agent_profiles` property. **Leave the `repo_root is None` branch
  untouched** — that is the legitimate bootstrap edge case named in spec.md's Edge Cases section (R7), not a
  site to migrate.
- **Files**: `src/charter/profile_resolution.py`.
- **Parallel?**: Yes.

## Test Strategy

- `pytest tests/runtime/ tests/specify_cli/tool_surface/ tests/specify_cli/cli/commands/agent/
  tests/charter/ -v` — targeted surfaces for the 4 modified modules.
- `pytest tests/perf/test_tasks_status_baseline.py -v` — the NFR-005 gate.
- `mypy --strict` on all 4 changed modules.

## Risks & Mitigations

- **Measuring the baseline after the change, not before.** Mitigation: T006's ordering is load-bearing —
  reviewers should check the tracer file's timestamp precedes T009's commit.
- **Using the plain gated property where the accessor was actually needed (or vice versa).** Mitigation:
  re-check each site's need against `research.md`'s per-site verdict table before writing the migration.

## Review Guidance

- Confirm the baseline was captured on the merge-base, not after any of this WP's changes.
- Confirm `runtime_bridge_io.py` and `projection.py` use the accessor, not the plain gated property.
- Confirm the removed "boundary ratchet" comment is replaced with an accurate one, not silently deleted.

## Activity Log

- 2026-08-03T14:10:00Z – system – Prompt created.
