---
work_package_id: WP02
title: 'Aggregator decision script: quality-gate verdict logic, extracted + fixture-tested'
dependencies: []
requirement_refs:
- FR-011
tracker_refs: []
planning_base_branch: tidy/ci-suite-map-2034
merge_target_branch: tidy/ci-suite-map-2034
branch_strategy: Planning artifacts for this mission were generated on tidy/ci-suite-map-2034. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into tidy/ci-suite-map-2034 unless the human explicitly redirects the landing branch.
subtasks:
- T004
- T005
- T006
phase: Phase 1 - Substrate
assignee: ''
agent: ''
history:
- at: '2026-07-04T05:27:33Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: python-pedro
authoritative_surface: scripts/ci/
create_intent:
- scripts/ci/quality_gate_decision.py
- tests/scripts/test_quality_gate_decision.py
- tests/scripts/__init__.py
execution_mode: code_change
model: ''
owned_files:
- scripts/ci/quality_gate_decision.py
- tests/scripts/test_quality_gate_decision.py
- tests/scripts/__init__.py
role: implementer
tags: []
task_type: implement
---

# Work Package Prompt: WP02 – Aggregator decision script

## ⚡ Do This First: Load Agent Profile

Use the `/ad-hoc-profile-load` skill to load the agent profile specified in the frontmatter (or any user-defined profile), and behave according to its guidance before parsing the rest of this prompt.

- **Profile**: `python-pedro`
- **Role**: `implementer`

---

## ⚠️ IMPORTANT: Review Feedback

Check the `review_ref` field in the event log before starting; address all feedback.

---

## Objectives & Success Criteria

FR-011's decision logic as a standalone, hermetically-testable script — so WP03's `ci-quality.yml` wiring is a thin invocation, and the riskiest semantics in the mission (the aggregator guards every merge) are pinned by fixtures BEFORE they go live. IC-07's "extract the decision into a testable script" made concrete.

## Subtasks & Detailed Guidance

### Subtask T004 – The decision script
`scripts/ci/quality_gate_decision.py` (stdlib-only; invoked by the workflow with JSON on stdin or via files):

**Inputs**: (a) the `needs` context (job → result) as JSON; (b) the `changes` job outputs (group → 'true'/'false') as JSON; (c) a job→groups mapping (which filter outputs gate each job) as JSON — WP03 generates this mapping IN the workflow from the same source the `if:` expressions use; WP04's invariant asserts it ≡ the parsed `if:` gating (Decision 8: derived, never hand-maintained); (d) flags: `run_all`, `catchall_unmatched`, `pr_is_draft`, plus the draft-gated job set.

**Decision table (paula, spec FR-011 — encode EXACTLY)**:
- `full_run = run_all OR catchall_unmatched`
- per blocking job: `filter_true = any(outputs[g] == 'true' for g in job_groups)`; `job_skipped = needs[job].result == 'skipped'`
- `draft_exempt = job in draft_gated_jobs AND pr_is_draft` (safe per FR-013 + GitHub's native draft-merge block)
- **FAIL** iff `filter_true AND job_skipped AND NOT full_run AND NOT draft_exempt` (improperly skipped)
- existing semantics preserved: `failure`/`cancelled` still FAIL; legitimately-skipped (filter false) still OK.

**Scope guard (C-005)**: the script evaluates ONLY the jobs it is given; WP03 passes the blocking `needs:` set — `quarantine-visibility` must never enter it. Assert defensively: if a job named `quarantine-visibility` appears in the input set, exit with a loud error (the C-005 tripwire).

**Outputs**: exit code + a Markdown run/skipped table on stdout for `$GITHUB_STEP_SUMMARY` (job | filter state | result | verdict), naming any improperly-skipped suite.

### Subtask T005 – Fixture tests
`tests/scripts/test_quality_gate_decision.py` (marked `pytest.mark.fast` — CI-selected, NFR-005). Cases, minimum:
- happy path all-success; legitimately-skipped (filter false) → OK;
- improperly-skipped (filter true, skipped, no full_run, not draft) → FAIL naming the job;
- full-run supersede (same state + `catchall_unmatched=true`) → OK;
- draft-exempt (draft-gated job, draft PR) → OK; same job on NON-draft PR skipped → FAIL;
- failure/cancelled → FAIL (existing semantics preserved);
- quarantine-visibility in input → loud error (C-005 tripwire);
- table snapshot: the summary output includes every job with its verdict.
Realistic test data ([[testing doctrine]]): real job names from ci-quality.yml, real group names.

### Subtask T006 – Gates
- `PWHEADLESS=1 pytest tests/scripts/ -q` green; verify the file is CI-selected (`fast` marker → fast-tests-core-misc catch-all path; confirm `tests/scripts/` isn't in the catch-all `--ignore` lists — if it is, note it for WP03).
- Diff-scoped `ruff check` exit 0; mypy clean on the new files.

## Definition of Done
- Script encodes the exact table; every fixture case above green; C-005 tripwire proven by test.
- Zero workflow edits (WP03 wires it).

## Risks / Reviewer Guidance
- The job→groups mapping input is DATA here; its truthfulness is WP03/WP04's contract (Decision 8). Reject any hardcoded job→group table inside the script.
- Reject clever GitHub-expression parsing in the script — it consumes plain JSON the workflow assembles.

## Activity Log

> Append at the END, chronological. Format: `- YYYY-MM-DDTHH:MM:SSZ – agent_id – <action>`

- 2026-07-04T05:27:33Z – system – Prompt created.
- 2026-07-04T09:05:00Z – wp02-implementer – Loaded python-pedro profile; recon: real job/group names + draft-gated set (`integration-tests-core-misc`, `e2e-cross-cutting`) + release-required arm read from ci-quality.yml quality-gate (:2915); confirmed `tests/scripts` absent from every catch-all `--ignore` list (grep over .github/workflows/*.yml → no hits), so a `fast`-marked test there is CI-routed via fast-tests-core-misc — nothing to flag for WP03.
- 2026-07-04T09:12:00Z – wp02-implementer – ATDD RED: authored tests/scripts/test_quality_gate_decision.py (17 cases: happy path, legitimate skip, improperly-skipped, full-run supersede ×2, draft-exempt + non-draft FAIL, failure/cancelled ×2, C-005 tripwire ×4 injection points, table snapshot, release-required slot ×2, GitHub-native needs shape, contract errors ×3, Decision-8 no-hardcoded-table structural guard). Red run: `PWHEADLESS=1 uv run pytest tests/scripts/ -q` → `FileNotFoundError: .../scripts/ci/quality_gate_decision.py` — 1 error (collection), script absent as expected.
