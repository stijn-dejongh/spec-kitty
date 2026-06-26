---
work_package_id: WP05
title: Verify & close — full-gate dry run, floor, issue-matrix terminal
dependencies:
- WP01
- WP02
- WP03
- WP04
requirement_refs:
- FR-010
- NFR-001
- NFR-003
tracker_refs: []
subtasks:
- T026
- T027
- T028
phase: Phase 4 - Close-out
assignee: ''
agent: claude
history:
- at: '2026-06-26T19:00:00Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: python-pedro
create_intent: []
model: ''
owned_files: []
role: implementer
tags: []
task_type: implement
---

# Work Package Prompt: WP05 – Verify & close

## ⚡ Do This First: Load Agent Profile
Use `/ad-hoc-profile-load` to load `python-pedro` (implementer).

## Objectives & Success Criteria
- Cross-cutting verification: full architectural gate green (incl. the new identity arm) with no un-pinned strangers; floor strictly-below census; zero STATUS legs re-routed; issue-matrix #2185/#2186 reach a terminal verdict.

## Context & Constraints
- Depends on WP01–WP04. Gate-added-in-mission can't catch offenders in its own merge → the dry run (T026) is the backstop.

## Branch Strategy
- **Planning base branch**: `mission/coord-read-residuals-2185-2186`
- **Merge target branch**: `mission/coord-read-residuals-2185-2186`

## Subtasks & Detailed Guidance
### T026 – Full-gate dry run
- Run the full `tests/architectural/` suite (and integration/git CI-only shards locally per post-merge arch-gate discipline). Confirm the new identity arm is green and flags nothing un-pinned; `ruff` + `mypy` clean.
### T027 – Floor + NFR-001 confirm [P]
- Confirm `ROUTED_CANONICALIZER_FLOOR` is strictly-below the live census and that no STATUS-partition read was re-routed to PRIMARY (grep the diff for STATUS legs).
### T028 – Issue-matrix terminal + traces [P]
- Set #2185/#2186 to `fixed` in `issue-matrix.md` with evidence refs; append the implement-phase entries to the three `traces/` files; validate the quickstart scenario.

## Test Strategy
- Whole-suite verification; this WP gates the mission `done`.

## Risks & Mitigations
- A STATUS leg silently re-routed → T027 diff grep + the WP04 integration test's STATUS-from-husk assertions.

## Review Guidance
- `reviewer-renata`: confirm terminal issue-matrix verdicts are evidence-backed, the gate dry run actually ran, traces appended.

## Activity Log
- 2026-06-26T19:00:00Z – system – Prompt created.
