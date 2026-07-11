---
work_package_id: WP06
title: "Tidy-first: extract the pre-review hook (Lane C enabler)"
dependencies: []
requirement_refs:
- FR-010
tracker_refs:
- "2535"
planning_base_branch: design/doctrine-controlled-gates
merge_target_branch: design/doctrine-controlled-gates
branch_strategy: Planning artifacts for this mission were generated on design/doctrine-controlled-gates. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into design/doctrine-controlled-gates unless the human explicitly redirects the landing branch.
subtasks:
- T024
- T025
- T026
- T027
- T028
phase: "Lane C - Path A"
assignee: ''
agent: ''
shell_pid: ''
history:
- at: '2026-07-11T00:00:00Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: python-pedro
authoritative_surface: src/specify_cli/cli/commands/agent/
execution_mode: code_change
model: ''
owned_files:
- src/specify_cli/cli/commands/agent/pre_review_hook.py
- src/specify_cli/cli/commands/agent/tasks_move_task.py
- src/specify_cli/cli/commands/agent/tasks.py
create_intent:
- src/specify_cli/cli/commands/agent/pre_review_hook.py
role: implementer
tags: []
task_type: implement
---

# Work Package Prompt: WP06 – Tidy-first: extract the pre-review hook

## ⚡ Do This First: Load Agent Profile

Load the **python-pedro** implementer profile via `/ad-hoc-profile-load` before touching
code. This is a `code_change` WP on `src/specify_cli/cli/commands/agent/`.

---

## Objectives & Success Criteria

- **Relocate** the pre-review regression-gate hook block out of the 1817-LOC
  `tasks_move_task.py` god-module into a dedicated sibling module
  `src/specify_cli/cli/commands/agent/pre_review_hook.py` — a **behavior-preserving
  move only** (IC-01, the Lane C tidy-first enabler).
- This clean isolated surface is what the seam (WP03) + the Path-A handler dispatch
  (WP08) land on later. The **inversion onto the seam is NOT this WP** — WP06 only
  moves code; WP13 owns the inversion.
- **Done when:** the `_PRE_REVIEW_*` constants + the `_mt_pre_review_*` helper family
  + the `_pre_review_gate_*` seams live in `pre_review_hook.py`; `tasks_move_task.py`
  imports them (or re-exports through them) with identical call sites; the
  `tasks.py:427-448` re-export shim resolves to the new home; existing move-task
  characterization / golden tests are green **unchanged**; ruff + mypy clean.

## Context & Constraints

The pre-review gate hook was added by mission `review-regression-gate-01KWX6DF` (WP02).
It is phase **C.5** of `_do_move_task`: after every pre-existing guard clears and before
the transition is emitted/committed. See the block comment at
`tasks_move_task.py:689-708`.

- **This is a pure extraction.** No logic changes, no signature changes, no
  fault-handling changes. The golden move-task tests must pass **without edits**.
- **Broader `tasks_move_task` / `runtime_bridge` degod is OUT of scope** — that is
  tracked at **#2531** (#2116 is closed, superseded). Move only the pre-review hook
  family; do not opportunistically relocate unrelated move-task helpers.
- **Do NOT invert onto the seam here.** WP06 does not import `resolve_gates` / the
  `review/gates/` package and does not change what the hook decides. Inversion is
  **WP13's** sole responsibility (Note-for-tasks #5: the hook inversion has exactly
  one owner). Introducing seam calls here is a scope violation.
- Design refs: `plan.md` IC-01; `research.md` §1 (fail-open scaffolding to preserve
  VERBATIM) and §5 (Campsite — Tidy-First enabler, sequence FIRST); `spec.md` FR-010.

## Branch Strategy
- **Planning base / merge target**: `design/doctrine-controlled-gates`. Populated by
  finalize-tasks. This WP has **no dependencies** and may start immediately.

## Subtasks & Detailed Guidance

### T024 — Extract the pre-review hook block into `pre_review_hook.py`
Move the following from `tasks_move_task.py` (`:690-1051`) into a new sibling module
`src/specify_cli/cli/commands/agent/pre_review_hook.py`:

- The `_PRE_REVIEW_*` constants: `_PRE_REVIEW_CONFIG_KEY_BLOCK`,
  `_PRE_REVIEW_CONFIG_KEY_TEST_COMMAND`, `_PRE_REVIEW_FRONTMATTER_KEY`
  (`tasks_move_task.py:711-713`).
- The `_pre_review_gate_*` test seams: `_pre_review_gate_filter_groups` (`:716`),
  `_pre_review_gate_composite_routing` (`:733`).
- The `_mt_pre_review_*` helper family (~15 helpers), including
  `_mt_pre_review_gate_with_override_scope`, `_mt_empty_scope_verdict` (`:859`),
  `_mt_pre_review_gate_verdict`, `_mt_pre_review_gate_metadata`,
  `_mt_pre_review_block_enabled`, `_mt_pre_review_changed_files`,
  `_mt_pre_review_scope_override`, `_mt_pre_review_gate_console_warning`,
  `_mt_pre_review_gate_block_message`, `_mt_resolve_pre_review_workspace`,
  `_mt_review_config_section`, and the orchestrating `_mt_run_pre_review_gate` (`:996`).

Guidance on the mechanics of the move:
- Prefer **module-to-module import** over copy: `tasks_move_task._do_move_task` continues
  to call `_mt_run_pre_review_gate`; make `tasks_move_task` import it from
  `pre_review_hook` (or keep a thin re-export in `tasks_move_task` if that minimizes
  churn on the phase-C.5 call site). The `_MoveTaskState` type is threaded through — keep
  the parameter shape (`st: _MoveTaskState`) intact; import `_MoveTaskState` into the new
  module rather than duplicating it.
- Watch the cross-module coupling: the hook reads `st.target_lane`, `Lane.FOR_REVIEW`,
  `st.wp`, `st.main_repo_root`, `st.feature_dir`, `st.force`, `st.json_output`, and
  writes `st.pre_review_gate_metadata`. Import the same symbols (`Lane`, `pre_review_gate`,
  `BaselineTestResult`, `typer`, `_resolve_wp_slug`) into `pre_review_hook.py`.
- The lazy `from specify_cli.cli.commands.agent import tasks as _tasks` inside
  `_mt_run_pre_review_gate` (used for `_tasks.console` / `_tasks._output_error`) must be
  preserved as-is — it exists to dodge an import cycle; do not hoist it to module top.

### T025 — Preserve the fail-open scaffolding VERBATIM
The three fail-open elements **ARE the FR-010 contract**, not debt — copy them
character-for-character, do not "clean them up", do not invert them onto any seam:

1. `_mt_empty_scope_verdict` (`tasks_move_task.py:859`) — builds a `NO_COVERAGE`
   verdict without deriving/running anything. Keep its exact `ScopeResult` shape and its
   `excluded_scope_files` kwarg.
2. The **broad `except Exception as exc:`** in `_mt_run_pre_review_gate` (the internal-
   failure catch, `tasks_move_task.py:1035`) — folds ANY internal gate failure to
   `_mt_empty_scope_verdict(f"pre-review gate evaluation failed — unverified: {exc}")`.
   The comment `# An internal gate failure must never break move-task (FR-003 spirit).`
   moves with it verbatim.
3. The `except pre_review_gate.GateAuthoritiesUnavailable as exc:` catch
   (`tasks_move_task.py:905-909`) in `_mt_pre_review_gate_verdict` — folds unavailable
   authorities into the SAME `no_coverage` shape. Keep it and its `excluded_scope_files`
   argument intact.

The only non-local exit the hook may take remains the deliberate opt-in
`raise typer.Exit(1)` block at the tail of `_mt_run_pre_review_gate` — do not add,
remove, or reshape any exit path.

### T026 — Re-point the `tasks.py:427-448` re-export shim
`tasks.py` re-exports the whole `_mt_*` / `_pre_review_gate_*` family for backward
compatibility (`tasks.py:420-451`, an `import ... as ...` block). After the move, these
names live in `pre_review_hook`. Update the shim so every relocated symbol re-exports
from its new home:

- `_mt_pre_review_block_enabled`, `_mt_pre_review_changed_files`,
  `_mt_pre_review_gate_block_message`, `_mt_pre_review_gate_console_warning`,
  `_mt_pre_review_gate_metadata`, `_mt_pre_review_gate_verdict`,
  `_mt_pre_review_gate_with_override_scope`, `_mt_pre_review_scope_override`,
  `_mt_resolve_pre_review_workspace`, `_mt_review_config_section`,
  `_mt_run_pre_review_gate`, `_pre_review_gate_composite_routing`,
  `_pre_review_gate_filter_groups`.
- Keep the non-pre-review `_mt_*` re-exports pointing at `tasks_move_task` unchanged —
  only the pre-review family moves.
- The public import surface (`from specify_cli.cli.commands.agent.tasks import <name>`)
  must remain byte-for-byte identical for every relocated symbol, because integration
  tests monkeypatch `_pre_review_gate_filter_groups` / `_pre_review_gate_composite_routing`
  through this path. Verify the monkeypatch target still resolves.

### T027 — Golden characterization tests prove move-task behavior unchanged
Do **not** rewrite the existing move-task tests to point at the new module. The whole
point of an extraction is that the **existing** golden/characterization suite passes
unchanged (it exercises the public `move-task` command, not the private helper location):

- Run the move-task + pre-review-gate suites (e.g. the tests owned by
  `review-regression-gate-01KWX6DF` and the `tasks_move_task` characterization tests) and
  confirm green with **zero** edits.
- If any test imports a relocated private symbol directly, the T026 re-export shim should
  keep it resolving; if a test hard-codes `tasks_move_task._mt_...`, prefer fixing the
  re-export (not the test) so the symbol resolves from both old and new module paths, and
  note the residual in the review handoff.
- Add a thin **golden guard** only if the existing suite does not already assert the
  three outcome shapes for: (a) `for_review` with no changed files → `NO_COVERAGE`;
  (b) internal exception → fail-open `NO_COVERAGE` warn (T025 broad catch);
  (c) `GateAuthoritiesUnavailable` → fail-open `NO_COVERAGE`. Assert message-shape and
  non-block, not internal call counts.

### T028 — ruff / mypy clean; no new complexity over 15
- `ruff check` and `mypy` must be **zero issues, zero warnings** on both the new
  `pre_review_hook.py` and the trimmed `tasks_move_task.py` / `tasks.py`.
- **Do NOT add** `# noqa`, `# type: ignore`, or per-file ignores to make the split pass.
  If `_mt_run_pre_review_gate` carried a `# noqa: C901`, the extraction should not raise
  any function above C(15); do not introduce a new complexity suppression.
- The extraction must not fuse helpers — keep the small-composition-helper structure so
  each function stays well under the ceiling.

## Test Strategy
- Existing move-task / pre-review golden suite green **unchanged** (primary evidence of
  behavior preservation).
- `ruff` + `mypy` zero-issue on all three owned files.
- Import-surface probe: every symbol in the `tasks.py` re-export block still importable
  from `specify_cli.cli.commands.agent.tasks` and resolving to the relocated definition.

## Risks & Mitigations
- **Import cycle** between `tasks_move_task` ⇄ `pre_review_hook` ⇄ `tasks` → keep the
  lazy `import tasks as _tasks` inside `_mt_run_pre_review_gate`; import `_MoveTaskState`
  and `Lane` from their canonical homes, not via `tasks`.
- **Silent monkeypatch breakage** — the `_pre_review_gate_filter_groups` seam is patched
  by integration tests through `tasks.py`; verify the re-export target resolves to the new
  module before declaring done.
- **Accidental behavior drift** — any diff to the fault-folding branches is a defect; if a
  golden test needs a change to pass, suspect the extraction, not the test.

## Safeguards / MUST NOT touch
- **MUST NOT** change any hook logic, signature, precedence tier, or fault-fold. Pure move.
- **MUST NOT** invert the hook onto `resolve_gates` / the `review/gates/` seam — that is
  **WP13**. No import of `review.gates` in this WP.
- **MUST NOT** touch `pre_review_gate.py` (that surface is WP07/WP08), `runtime_bridge.py`,
  or any non-pre-review move-task helper.
- **MUST NOT** widen scope into a `tasks_move_task` decomposition — degod is **#2531**.
- **MUST** preserve `_mt_empty_scope_verdict` (`:859`), the broad `except` (`:1035`), and
  the `GateAuthoritiesUnavailable` catch (`:905-909`) **verbatim** — they are the FR-010
  fail-open contract.

## References (file:line, from research §1/§5)
- `tasks_move_task.py:689-708` — phase C.5 block comment (extraction origin).
- `tasks_move_task.py:711-713` — `_PRE_REVIEW_*` constants.
- `tasks_move_task.py:716,733` — `_pre_review_gate_filter_groups` / `_composite_routing`
  test seams (monkeypatch targets).
- `tasks_move_task.py:859` — `_mt_empty_scope_verdict` (fail-open, VERBATIM).
- `tasks_move_task.py:905-909` — `GateAuthoritiesUnavailable` fold (VERBATIM).
- `tasks_move_task.py:996` — `_mt_run_pre_review_gate` (orchestrator; `:1012` lane guard).
- `tasks_move_task.py:1035` — broad `except Exception` internal-failure fold (VERBATIM).
- `tasks.py:420-451` — the re-export shim block to re-point (T026).

## Review Guidance
- Recommended sign-off: **reviewer-renata**.
- Confirm the diff is a **move**, not a rewrite: the three fail-open elements are
  byte-identical; no `review.gates` import; golden suite green with zero test edits;
  ruff/mypy clean with no new suppressions.

## Activity Log
- 2026-07-11T00:00:00Z – system – Prompt created.
