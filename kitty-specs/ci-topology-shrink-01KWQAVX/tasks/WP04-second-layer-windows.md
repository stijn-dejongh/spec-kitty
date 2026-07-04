---
work_package_id: WP04
title: 'Second-layer Windows surface: ci-windows.yml static windows_critical list propagation (FR-008)'
dependencies:
- WP03
requirement_refs:
- FR-008
tracker_refs: []
planning_base_branch: tidy/ci-topology-shrink
merge_target_branch: tidy/ci-topology-shrink
branch_strategy: Planning artifacts for this mission were generated on tidy/ci-topology-shrink. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into tidy/ci-topology-shrink unless the human explicitly redirects the landing branch.
base_branch: kitty/mission-ci-topology-shrink-01KWQAVX
base_commit: aa998ede7e31927286e78e7819757e03c2f2c604
created_at: '2026-07-04T21:00:00+00:00'
subtasks:
- T012
phase: Phase 4 - Second-layer surfaces
assignee: ''
agent: ''
shell_pid: ''
history:
- at: '2026-07-04T21:00:00Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: python-pedro
authoritative_surface: .github/workflows/ci-windows.yml
create_intent: []
execution_mode: code_change
model: ''
owned_files:
- .github/workflows/ci-windows.yml
role: implementer
tags: []
task_type: implement
---

# Work Package Prompt: WP04 – Second-layer Windows surface

## ⚡ Do This First: Load Agent Profile

Use the `/ad-hoc-profile-load` skill to load the agent profile specified in the frontmatter (or any user-defined profile), and behave according to its guidance before parsing the rest of this prompt.

- **Profile**: `python-pedro`
- **Role**: `implementer`

---

## ⚠️ IMPORTANT: Review Feedback

Check the `review_ref` field in the event log before starting; address all feedback.

---

## Objectives & Success Criteria

Propagate any **windows-marked** test file that WP03's shard carve relocated into `ci-windows.yml`'s static `windows_critical` list (`:24-42`) — the **only** real second-layer surface per the corrected FR-008. This closes the Windows split-brain edge case: a carved test file also listed in `windows_critical` must be updated in lockstep or FR-003c reds.

**FR-008 correction (do NOT edit these)**: `scripts/ci/quality_gate_decision.py` holds no job→group data; `drift-detector.yml` and `release.yml` carry no shard/ignore/job names. Editing any of them is out-of-scope drift.

## Subtasks & Detailed Guidance

### Subtask T012 – Static `windows_critical` list propagation
- Diff WP03's carve against the current `ci-windows.yml:24-42` static list. For each windows-marked test file whose path moved (or whose owning root was carved into a new shard), update the static list entry so it still points at a live test file.
- Assert `test_every_filter_glob_is_live` (FR-003c — covers all 4 workflows incl. `ci-windows.yml`) stays green: no dead `windows_critical` glob, no split-brain (C-002).
- If WP03 relocated NO windows-marked files, this is a verified no-op: record the justification AND the green glob-live invariant (the invariant proves the list is coherent — the DoD stays non-fakeable).

## Campsite cleaning (standing rule; ride the WP's normal review)

YAML file — keep it coherent, no dead anchors. Do NOT touch `ci-quality.yml` (WP03), `quality_gate_decision.py`, `drift-detector.yml`, or `release.yml`.

## Definition of Done (non-fakeable — every anchor is a green test)

- **`test_every_filter_glob_is_live` GREEN** over `ci-windows.yml` (every `windows_critical` entry maps to a live file; no dead glob) — recorded run output.
- Every windows-marked file relocated by WP03 is present in the static list (or a recorded no-op justification if none moved), with C-002 no-split-brain preserved.

## Risks / Reviewer Guidance

- A relocated windows file dropped from the static list → the glob-live/coherence invariant reds; update in the same landing.
- Reviewer confirms scope stayed on `ci-windows.yml` — the FR-008 correction rules out the other three files.

## Activity Log

> Append at the END, chronological. Format: `- YYYY-MM-DDTHH:MM:SSZ – agent_id – <action>`

- 2026-07-04T21:00:00Z – system – Prompt created.
