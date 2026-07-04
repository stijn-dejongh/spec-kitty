---
work_package_id: WP01
title: 'Substrate: workflow-scope preflight + gate-coverage parse-model extension'
dependencies: []
requirement_refs:
- FR-003
- FR-008
tracker_refs: []
planning_base_branch: tidy/ci-suite-map-2034
merge_target_branch: tidy/ci-suite-map-2034
branch_strategy: Planning artifacts for this mission were generated on tidy/ci-suite-map-2034. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into tidy/ci-suite-map-2034 unless the human explicitly redirects the landing branch.
base_branch: kitty/mission-ci-suite-map-bind-01KWNPMP
base_commit: f58bcec37663fae6a642815b229307ba2cab1791
created_at: '2026-07-04T08:52:53.610639+00:00'
subtasks:
- T001
- T002
- T003
phase: Phase 1 - Substrate
assignee: ''
agent: ''
shell_pid: '3796249'
history:
- at: '2026-07-04T05:27:33Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: python-pedro
authoritative_surface: tests/architectural/
create_intent: []
execution_mode: code_change
model: ''
owned_files:
- tests/architectural/_gate_coverage.py
role: implementer
tags: []
task_type: implement
---

# Work Package Prompt: WP01 – Substrate: preflight + parse-model extension

## ⚡ Do This First: Load Agent Profile

Use the `/ad-hoc-profile-load` skill to load the agent profile specified in the frontmatter (or any user-defined profile), and behave according to its guidance before parsing the rest of this prompt.

- **Profile**: `python-pedro`
- **Role**: `implementer`

---

## ⚠️ IMPORTANT: Review Feedback

Check the `review_ref` field in the event log before starting; address all feedback.

---

## Objectives & Success Criteria

Two enablers everything else stacks on:
1. **C-004 preflight**: prove `.github/workflows/` edits can be pushed from this checkout (the `workflow` OAuth scope gate #2296 warns about). If the push fails, STOP the mission and report — nothing downstream is implementable.
2. **IC-02**: extend `tests/architectural/_gate_coverage.py` ADDITIVELY with every parsed relation the WP03/WP04 consumers need. This file is a single-owner spine: after this WP it is READ-ONLY for the rest of the mission (Wave-2 spine lesson).

## Subtasks & Detailed Guidance

### Subtask T001 – Workflow-scope preflight probe
- From the repo root: create a throwaway branch, append a trailing newline to `.github/workflows/ci-quality.yml`, commit, `unset GITHUB_TOKEN && git push origin probe/workflow-scope`. Paste the push output (success or the OAuth error) into the Activity Log. On success: delete the probe branch (remote + local) and revert nothing (the probe never merges). On failure: STOP, move this WP to blocked with the error verbatim.

### Subtask T002 – Parse-model extensions (additive only)
Read `_gate_coverage.py` end-to-end first. Extend the module (new functions/dataclass fields; do NOT change existing behavior — every existing consumer test must pass untouched) to expose:
- **Positive-marker tokens per gate**: a negation-aware walk of each gate's `-m` expression via `_pytest.mark.expression.Expression` returning the positively-referenced marker names (`not windows_ci` = negative; `windows_ci` in ci-windows = positive). This is FR-001's state-(i) primitive. Expected live result: exactly `{fast, integration, git_repo, architectural, slow, timing, quarantine, windows_ci}` (8) — re-derive, record.
- **`needs:` lists per job** and **`needs.<job>.result` references** inside run scripts (FR-003a).
- **Dorny filter groups**: group name → glob list, plus which job `if:` expressions consume which group outputs (the job→group gating map — FR-011's mapping invariant reads this).
- **Diff-cover critical-path entries** and **`--cov=` emitters per job** (FR-005).
- **The pytest-invoking workflow set** discovered from `.github/workflows/*.yml` by content probe (FR-008) — compared against the module's `WORKFLOW_FILES` allowlist.
- **Quality-gate result-loop membership** (which jobs the aggregator reads) (FR-003d).
- **`on: pull_request` trigger types + outer `paths:` lists** (FR-013 / FR-012 two-layer reads).
- Registered-marker list parsed from `pytest.ini`'s `markers =` block (reuse `test_marker_registry_single_source.py`'s approach if importable; else a small parser).

Keep it pure parsing — NO assertions in this module (the invariants live in WP04's test files). Docstring each new surface with the FR it serves.

### Subtask T003 – Gates
- `PWHEADLESS=1 pytest tests/architectural/test_gate_coverage.py tests/architectural/test_ci_quality_path_filters.py tests/architectural/test_marker_registry_single_source.py -q` — all existing consumers green, untouched.
- A quick self-check script exercising each new parse surface against the LIVE workflows; paste the outputs (the 8-token set, the needs map size, the group count = re-derived gate/group numbers) into the Activity Log — these are WP03/WP04's ground truth.
- Diff-scoped `ruff check` exit 0; `python -m mypy src/ 2>&1 | tail -2` stays Success (this file is under tests/, but if mypy covers it, clean).

## Campsite cleaning (standing rule [[feedback-sonar-attack-vector-campsite]]; ride the WP's normal review)

Sonar: zero open issues in the target files (verified). Local ruff --select ALL census (randy, 2026-07-04) — clean while you're there; auto-fixables in one `ruff check --fix` pass where possible:

- `_gate_coverage.py:40` isort (I001) · `:48` Sequence → TYPE_CHECKING (TC003) · `:53` `from pytest import ExitCode` → `import pytest` (PT013) · `:234` `import yaml` → top-level (PLC0415) · `:240` `includes or [None]` (FURB110) · `:341` hoist `_DUPLICATE_GATE_THRESHOLD = 2` (PLR2004) · `:372` explicit `check=False` on subprocess.run (PLW1510) · trailing commas `:89,:256,:403,:438` (COM812)
- `test_gate_coverage.py`: **highest-leverage** — make the five parse helpers PUBLIC in `_gate_coverage.py` (`_parse_pytest_invocation`, `_path_matches`, `_substitute_matrix`, `_join_continuations`, `_strip_to_command` — the module itself is private, so the underscore adds nothing) clearing 9 SLF001 sites at `:195-341`; docstrings `:64,:368` (D103) + D205 blanks `:129,:155,:192,:239`; `:351/:353` add `# noqa: PLC0415  # intentional: exercises import surface`; `:359` `name == "a"` (FURB171); trailing commas ×8 (COM812)
- Adjudicated OUT (leave): `:145` PERF401 (readability), `:394` TRY003 (load-bearing message), `:445-473` T201 (intentional CLI prints), test `:272` PLR2004 (synthetic-universe size).

## Definition of Done
- Preflight evidence recorded (push success verbatim, probe branch cleaned).
- Every listed parse surface exists, additively, with the live self-check outputs recorded. These recorded counts are WP03/WP04's ground truth: any downstream discrepancy is WP01 feedback (re-open), not a downstream workaround — the cross-check is explicit, not implicit.
- Existing gate-coverage/path-filter/marker-registry tests green with zero edits to them.

## Risks / Reviewer Guidance
- The private `_pytest.mark.expression` API: pin its import with a loud failure message (existing precedent in the module) — reviewer should verify the loud-fail is TESTED behavior via the WP04 fixtures, but for this WP a try/except-raise with a clear message suffices.
- Reject any change to existing parse behavior (this is additive-only by contract).

## Activity Log

> Append at the END, chronological. Format: `- YYYY-MM-DDTHH:MM:SSZ – agent_id – <action>`

- 2026-07-04T05:27:33Z – system – Prompt created.
