---
work_package_id: WP02
title: Lane A — Merge cluster routing + pin drain
dependencies:
- WP01
requirement_refs:
- FR-001
- FR-002
- FR-003
- FR-006
- FR-008
- FR-011
- NFR-001
tracker_refs: []
subtasks:
- T009
- T010
- T011
- T012
- T013
- T014
- T015
- T016
phase: Phase 2 - Lane A (post C-SEQ rebase)
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

# Work Package Prompt: WP02 – Lane A — Merge cluster routing + pin drain

## ⚡ Do This First: Load Agent Profile

Use `/ad-hoc-profile-load` to load `python-pedro` (implementer).

## Objectives & Success Criteria

- Route the `merge/` + `cli/commands/merge.py` PRIMARY reads by their real kind; per-leg split where a single resolved dir feeds both PRIMARY and STATUS legs; drain the merge-cluster #2185 pins in the same commit.

## Context & Constraints

- **C-SEQ FIRST**: rebase onto post-implement-loop-merge `main`; re-resolve all line citations; run T009 preflight before any pin drain.
- **C-001**: STATUS legs stay coord-aware. **C-002**: consume the resolver; never edit its internals or remove `candidate_feature_dir_for_mission`.
- **C-009-mirror**: `merge.py` line ranges differ from the sibling's `_mark_wp_merged_done`; drain only the #2185 pins.

## Branch Strategy
- **Planning base branch**: `mission/coord-read-residuals-2185-2186`
- **Merge target branch**: `mission/coord-read-residuals-2185-2186`

## Subtasks & Detailed Guidance

### T009 – Preflight + scope verify
- Assert `_DIR_READ_KNOWN_RESIDUALS` on the rebased base contains the #2185 pins (FR-011); confirm the sibling's whole-`src` scan covers `merge/`/`lanes/`/`core/` (FR-006). If a pin is absent → STOP (the sibling hasn't landed).
### T010 – `merge/forecast.py:153`+`:159`
- Route the `require_lanes_json` read (LANE_STATE) and the review-artifact preflight (WORK_PACKAGE_TASK) onto `resolve_planning_read_dir`.
### T011 – `merge/executor.py`
- **Thread the existing `:887` PRIMARY `target_feature_dir` through to `:976`** instead of recomputing the coord-aware `feature_dir`. Keep `status_feature_dir` (run.feature_dir at `:503`/`:560`) coord-aware.
### T012 – `merge/resolve.py:98`
- Route the `resolve_mission_identity` (meta) read; **leave `:63`** (handle→name canonicalization at the no-silent-fallback boundary) on `candidate_`.
### T013 – `merge/done_bookkeeping.py:237`
- Route the WP-path leg via `kind=WORK_PACKAGE_TASK`; **remove the misleading "do not use the read-path resolver" comment**; keep the status-transactional legs (`:248-249`) on the meta-bearing primary dir.
### T014 – `cli/commands/merge.py:269`
- Verify the `--abort` coord-teardown semantics, then route the `_load_meta` (PRIMARY_METADATA) read.
### T015 – Drain merge pins
- Remove the merge-cluster #2185 pins from `_DIR_READ_KNOWN_RESIDUALS` in the same commit (FR-008).
### T016 – RED-first tests
- Per-site tests (both legs) on the divergent coord fixture; revert → fail.

## Test Strategy
- RED-first per-site; the WP04 integration test is the cross-cutting proof. `ruff`+`mypy` clean; complexity ≤ 15.

## Risks & Mitigations
- Over-routing a STATUS leg (NFR-001) → split per-leg. Don't reintroduce #2139's silent `main` fallback in this neighborhood.

## Review Guidance
- `reviewer-renata`: confirm STATUS legs untouched, pins drained == sites routed, executor threads the existing primary dir.

## Activity Log
- 2026-06-26T19:00:00Z – system – Prompt created.
