---
work_package_id: WP08
title: Pre-review Path-A handler (exemplar migration)
dependencies:
- WP03
- WP02
- WP07
requirement_refs:
- FR-011
- FR-017
- FR-013
tracker_refs:
- '2535'
- "2330"
planning_base_branch: design/doctrine-controlled-gates
merge_target_branch: design/doctrine-controlled-gates
branch_strategy: Planning artifacts for this mission were generated on design/doctrine-controlled-gates. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into design/doctrine-controlled-gates unless the human explicitly redirects the landing branch.
subtasks:
- T033
- T034
- T035
- T036
- T037
phase: Lane C - Path A
assignee: ''
agent: ''
history:
- at: '2026-07-11T00:00:00Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: python-pedro
authoritative_surface: src/specify_cli/review/
execution_mode: code_change
model: ''
owned_files:
- src/specify_cli/review/gates/handlers/pre_review.py
- src/specify_cli/review/pre_review_gate.py
create_intent:
- src/specify_cli/review/gates/handlers/pre_review.py
role: implementer
tags: []
task_type: implement
---

# Work Package Prompt: WP08 – Pre-review Path-A handler (exemplar migration)

## ⚡ Do This First: Load Agent Profile

Load the **python-pedro** implementer profile via `/ad-hoc-profile-load` before touching
code. This is a `code_change` WP on `src/specify_cli/review/`.

---

## Objectives & Success Criteria

- Re-express the pre-review regression **test-gate** as the first built-in **Path-A
  handler** (FR-011) — implementing the WP03 dispatch Protocol, bound via a built-in step
  contract (`transition: for_review`), with **no opt-in and no doctrine-supplied code
  execution** (it is spec-kitty-shipped).
- **Reuse `evaluate_with_scope` unchanged** as the verdict tail; the handler derives scope
  through the WP07 built-in `ScopeSource`, then calls `evaluate_with_scope` — exactly the
  behavior the hardcoded gate had.
- **Remove** the hardcoded spec-kitty-shaped decision path from `pre_review_gate.py`
  (C-004, unification-not-parity): there is **no** "doctrine-inactive → run the old gate"
  compatibility tail. Inactive/undeclared → CALM-NOTICE (rendered downstream), not a
  legacy fallback.
- **Preserve existing config semantics** (FR-017): `review.fail_on_pre_review_regression`
  (opt-in block) and `review.test_command` — same defaults, same behavior, moved onto the
  handler's configuration.
- **Done when:** the handler produces the **identical** verdict to the prior hardcoded gate
  on the same change set with no opt-in (NFR-001 / SC-003 parity); the hardcoded decision
  path is gone (no fallback tail); ruff + mypy clean with **no** `# noqa` / `# type: ignore`
  added.

## Context & Constraints

- **Depends on WP03** (the `resolve_gates` seam + the handler/asset **dispatch Protocol** —
  IC-02 ships the Protocol only; this WP implements the Path-A arm), **WP02** (the built-in
  step contract has the `gate` binding on `transition: for_review` + DRG regen), and
  **WP07** (the built-in `ScopeSource` + the single `Scope` type).
- This is a **Path-A handler**: shipped inside spec-kitty, selected by doctrine, run with
  **no opt-in and no doctrine code executed**. It is the **only** gate migrated in this
  mission (FR-013) — do not touch the other transition checks; the composed-action artifact
  guard shares *selection* only (WP14) and is not migrated here.
- **C-004 is the sharp edge**: the hardcoded spec-kitty-shaped decision path in
  `pre_review_gate.py` is **removed**, not preserved as a compatibility fallback. Do NOT
  grow a "if doctrine inactive → old gate" tail. The census authorities themselves live
  behind WP07's built-in `ScopeSource` (still reachable when spec-kitty doctrine is active);
  what is removed here is the *decision/invocation path* that hard-wired the gate
  independent of charter activation.
- **Do NOT invert the move-task hook onto the seam here.** That inversion (wiring the
  extracted `pre_review_hook` through `resolve_gates` + the FR-014 reducer at the move-task
  boundary) is **WP13** (Note-for-tasks #5: exactly one owner). WP08 delivers the *handler*
  + its *binding* + the decision-path *removal*; WP13 wires the consumer.
- The verdict tail `evaluate_with_scope` (`pre_review_gate.py:451-511`) is **reused
  unchanged** — do not edit it. The handler orchestrates: resolve `ScopeSource` → `derive`
  → `evaluate_with_scope`, mirroring `_mt_pre_review_gate_verdict`'s precedence but reached
  through the seam.
- Design refs: `plan.md` IC-05; `research.md` §1 (reuse anchor `evaluate_with_scope`;
  #2330 hardcoded runner locus) and §4 (Path-A handler, no opt-in, parity); `spec.md`
  FR-011 / FR-013 / FR-017, NFR-001, SC-003.

## Branch Strategy
- **Planning base / merge target**: `design/doctrine-controlled-gates`. This WP branches
  atop **WP03 + WP02 + WP07** (all three must be present for the seam, the binding, and the
  `ScopeSource`).

## Subtasks & Detailed Guidance

### T033 — Path-A handler implementing the WP03 dispatch Protocol
In `src/specify_cli/review/gates/handlers/pre_review.py` implement the handler:

- Implement the **dispatch Protocol** defined by WP03 (`run`/`dispatch` returning a
  `GateVerdict`, per `contracts/gate-resolution-seam.md` — the handler/asset dispatch arm
  the seam's `run_gate` folds via FR-014).
- **No opt-in, no doctrine code**: the handler is instantiated by spec-kitty when its
  built-in binding is charter-active. It never executes doctrine-supplied code (that is
  Path-B / WP10-12).
- The handler's `derive`-then-evaluate body:
  1. Obtain the built-in spec-kitty `ScopeSource` (WP07) for the transition context.
  2. `scope = source.derive(changed_files)`.
  3. `verdict = pre_review_gate.evaluate_with_scope(scope, repo_root=..., baseline=...)`
     — **unchanged** tail.
  4. Return the `GateVerdict`; **do not** fold faults here — fault-folding to the operator
     outcome is the seam's `run_gate` (WP04 FR-014 reducer). The handler may still surface
     the `NO_COVERAGE` / `UNVERIFIED_BASELINE` / `NEW_FAILURES` verdict shapes exactly as
     today; the reducer maps them.
- Preserve the FR-004 override-scope precedence tier that `_mt_pre_review_gate_verdict`
  carried (explicit `pre_review_test_scope` frontmatter override → manual `ScopeResult` →
  `evaluate_with_scope`) so parity holds for WPs that pin an override scope.

### T034 — Reuse `evaluate_with_scope`; preserve config semantics (FR-017)
- **Reuse `evaluate_with_scope` (`pre_review_gate.py:451-511`) unchanged.** Do not
  reimplement the head-run → `diff_baseline` tail. The empty-scope `NO_COVERAGE`, the
  `UNVERIFIED_BASELINE` (baseline uncomputable), the `NEW_FAILURES`, and the
  `NO_NEW_FAILURES` branches all stay in that one tested body.
- **Preserve `review.fail_on_pre_review_regression`** (opt-in block) and
  **`review.test_command`** semantics — same defaults, same meaning — as the handler's
  configuration. The block precedence (`block_enabled` + `NEW_FAILURES` + `--force`
  bypass) that lived in `_mt_run_pre_review_gate` is preserved: whether it lives on the
  handler or is applied by the reducer/consumer is a WP03/WP04 boundary decision — carry
  the config read (`_mt_review_config_section` / `_mt_pre_review_block_enabled` shapes)
  into the handler's config surface without changing operator-observable behavior.
- Do NOT silently change any default: `fail_on_pre_review_regression` defaults off
  (warn-by-default, NFR-001); `--force` still bypasses the opt-in block and is recorded on
  the transition's `policy_metadata`.

### T035 — Bind the handler; remove the hardcoded decision path (C-004)
- **Bind** the handler in the built-in step contract on `transition: for_review` — the
  binding field WP02 added (`gate` binding, `mechanism: handler`). Confirm the binding
  names this handler and that WP03's `resolve_gates(mission, "for_review", activation)`
  selects it when spec-kitty doctrine is active.
- **Remove** the hardcoded spec-kitty-shaped **decision/invocation path** from
  `pre_review_gate.py` — the `#2330` hardcoded pytest/`--junitxml` invocation path that
  decided the gate independent of charter activation (`run_scoped_tests_at_head` argv
  `:379-386` stays as the *runner primitive* reused by the tail, but the *decision path*
  that unconditionally wired it is removed). **No fallback tail** — there is no
  "doctrine-inactive → old gate" branch. Undeclared/inactive → the seam returns `[]` →
  CALM-NOTICE (WP13 renders it).
- Keep `evaluate_with_scope`, `run_scoped_tests_at_head`, `derive_test_scope`, and the
  WP07 built-in `ScopeSource` — those are reused substrate. What is deleted is the
  hardcoded *selection/decision* wiring that made the gate spec-kitty-shaped regardless of
  doctrine (C-004). If a symbol becomes dead only because of the removal, delete it in this
  WP (campsite), noting it in the handoff.

### T036 — Red-first parity: migrated handler == prior hardcoded verdict (NFR-001/SC-003)
Write the parity test **red-first**, before the removal lands:

- On spec-kitty's **own** repo layout (pytest, `src/specify_cli/`), for a fixed change set
  the migrated handler (selected via the built-in binding, no opt-in) produces the
  **identical** `GateVerdict` (outcome + new/pre-existing failures + scope) as the prior
  hardcoded gate on the same inputs.
- Cover the key verdict shapes: `NO_COVERAGE` (empty scope), `UNVERIFIED_BASELINE`
  (baseline uncomputable), `NEW_FAILURES` (regression) with block-off (warn) and block-on
  (would-block) + `--force` bypass, and `NO_NEW_FAILURES`.
- **100% of existing `pre_review_gate` verdict tests must pass** with only binding-
  indirection edits; zero new failures attributable to the migration (NFR-001). If an
  existing verdict test fails, suspect the migration wiring, not the test.

### T037 — ruff / mypy clean; no suppressions added
- `ruff check` + `mypy` zero-issue on `handlers/pre_review.py` and the trimmed
  `pre_review_gate.py`.
- **Do NOT add** any `# noqa` or `# type: ignore` to make the handler or the removal pass.
  Fix the code (extract helpers, keep functions ≤ C(15)). Any pre-existing suppression you
  touch must be justified or removed, not propagated.

## Test Strategy
- **Red-first** parity test (T036) — the primary evidence for NFR-001 / SC-003.
- Existing `pre_review_gate` verdict suite green with only binding-indirection edits.
- Config-semantics test: `fail_on_pre_review_regression` off = warn, on = would-block,
  `--force` bypasses and records `policy_metadata` (FR-017).
- Selection test: `resolve_gates(mission, "for_review", active)` returns the handler when
  spec-kitty doctrine is active; `[]` when inactive (no fallback → CALM-NOTICE downstream).
- `ruff` + `mypy` zero-issue, no new suppressions.

## Risks & Mitigations
- **C-004 fallback creep** — the strong temptation is a "doctrine-inactive → old gate"
  safety branch. That is explicitly forbidden; inactive → `[]` → CALM-NOTICE. Review the
  removal for any residual unconditional invocation.
- **Verdict drift** — reuse `evaluate_with_scope` unchanged; any diff to that tail is a
  parity risk. Do not edit it.
- **Config regression** — a silently changed default breaks operators relying on
  `fail_on_pre_review_regression` / `test_command` (FR-017). Assert defaults explicitly.
- **Boundary overreach** — do not wire the move-task consumer (WP13) or migrate other
  gates (FR-013). Handler + binding + decision-path removal only.

## Safeguards / MUST NOT touch
- **MUST NOT** add any opt-in or execute doctrine-supplied code — this is a Path-A handler.
- **MUST NOT** keep a hardcoded decision fallback (C-004) — no "inactive → old gate" tail.
- **MUST NOT** edit `evaluate_with_scope` (`pre_review_gate.py:451-511`) — reuse unchanged.
- **MUST NOT** invert the move-task hook onto the seam (WP13) nor migrate any other gate
  (FR-013); do not touch `tasks_move_task.py` / `pre_review_hook.py` / `runtime_bridge.py`.
- **MUST NOT** change `review.fail_on_pre_review_regression` / `review.test_command`
  semantics or defaults (FR-017).
- **MUST NOT** add `# noqa` / `# type: ignore` to pass ruff/mypy.

## References (file:line, from research §1/§4)
- `pre_review_gate.py:451-511` — `evaluate_with_scope` (**reuse anchor, unchanged**).
- `pre_review_gate.py:358-423` — `run_scoped_tests_at_head` (runner primitive; argv
  `:379-386`) — kept as the reused runner, its *decision wiring* removed (#2330 locus).
- `pre_review_gate.py:374` — `env = dict(os.environ)` (Path-A inherits as today; only
  Path-B/WP11 must NOT copy this — noted for cross-WP awareness, not changed here).
- `pre_review_gate.py:278-341` — `derive_test_scope` (reached via WP07 `ScopeSource`).
- `tasks_move_task.py:996` / `:1035` / `:905-909` — the prior hardcoded hook + fail-open
  folds (the parity oracle for T036; **owned by WP06/WP13**, read-only reference here).
- `contracts/gate-resolution-seam.md` — the dispatch Protocol this handler implements +
  the `run_gate` FR-014 reducer that folds its verdict (WP04).
- Built-in step contract (`transition: for_review`) — WP02's `gate` binding target that
  T035 binds this handler to.

## Review Guidance
- Recommended sign-off: **reviewer-renata** (+ architect lens on the C-004 removal).
- Confirm: no fallback tail (grep the removal for any unconditional gate invocation);
  `evaluate_with_scope` untouched; config defaults preserved; T036 parity red-first then
  green; selection returns `[]` when doctrine inactive; ruff/mypy clean with no new
  suppressions.

## Activity Log
- 2026-07-11T00:00:00Z – system – Prompt created.
