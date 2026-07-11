---
work_package_id: WP07
title: ScopeSource abstraction + built-in spec-kitty ScopeSource
dependencies:
- WP03
requirement_refs:
- FR-009
- FR-012
tracker_refs:
- '2535'
planning_base_branch: design/doctrine-controlled-gates
merge_target_branch: design/doctrine-controlled-gates
branch_strategy: Planning artifacts for this mission were generated on design/doctrine-controlled-gates. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into design/doctrine-controlled-gates unless the human explicitly redirects the landing branch.
subtasks:
- T029
- T030
- T031
- T032
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
- src/specify_cli/review/gates/scope_source.py
- src/specify_cli/review/pre_review_gate.py
create_intent:
- src/specify_cli/review/gates/scope_source.py
role: implementer
tags: []
task_type: implement
---

# Work Package Prompt: WP07 – ScopeSource abstraction + built-in spec-kitty ScopeSource

## ⚡ Do This First: Load Agent Profile

Load the **python-pedro** implementer profile via `/ad-hoc-profile-load` before touching
code. This is a `code_change` WP on `src/specify_cli/review/`.

---

## Objectives & Success Criteria

- Make **scope derivation a doctrine-declared strategy** (`ScopeSource`) rather than a
  hardcoded `src/specify_cli/` + `tests.architectural._gate_coverage` assumption baked
  into the decision path (FR-009).
- Move spec-kitty's filter-group / CI-topology census (`_SRC_PACKAGE_PREFIX`,
  `_load_gate_coverage_module`, `_default_filter_groups`, `_default_composite_routing`)
  behind a **built-in** `ScopeSource` that is reached **only when spec-kitty's own
  doctrine is active** (FR-012) — a repo with a different layout supplies its own
  `ScopeSource` or gets the FR-008 CALM-NOTICE.
- **Done when:** `review/gates/scope_source.py` defines the `ScopeSource` protocol whose
  `derive(changed_files) -> Scope` returns the canonical `Scope`/`ScopeResult` type; the
  spec-kitty census is a built-in `ScopeSource` implementation; `derive_test_scope` stays
  **≤ C(15)**; a non-pytest fixture with no declared `ScopeSource` does **not** force-apply
  the built-in (NFR-002 acceptance); ruff + mypy clean.

## Context & Constraints

- **Depends on WP03** — the seam/dispatch protocol. Thread the **one** `Scope` /
  `ScopeResult` type that the seam's `TransitionContext.scope` uses through the
  `ScopeSource` output; **do NOT fork a second scope type** (plan Note-for-tasks #7).
  `pre_review_gate.ScopeResult` is the existing shape — reuse it as the canonical `Scope`
  unless WP03/data-model names a distinct `Scope`, in which case adapt to that one type.
- The `ScopeSource` protocol lives in `review/gates/scope_source.py` (a new module in the
  WP03 gate package). The **built-in spec-kitty implementation** wraps the census that
  currently lives in `pre_review_gate.py` — this WP relocates/adapts that census so the
  consumer-facing decision path no longer hard-references the spec-kitty layout.
- FR-012 is the load-bearing constraint: after this WP, the **consumer-facing gate path
  must not import** `tests.architectural._gate_coverage` nor assume
  `_SRC_PACKAGE_PREFIX = "src/specify_cli/"`. Those authorities are reachable **only**
  through the built-in `ScopeSource`, which is selected only when spec-kitty's own
  doctrine is charter-active.
- This WP is **selection-of-strategy**, not the handler wiring. The Path-A handler that
  calls a resolved `ScopeSource` and reuses `evaluate_with_scope` is **WP08**. Here you
  define the strategy seam + the built-in impl; you do not remove the hardcoded decision
  tail (that removal is WP08, C-004).
- Design refs: `plan.md` IC-04; `research.md` §1 (`derive_test_scope` at the C(15)
  ceiling; `_load_gate_coverage_module` refuse-outside-repo_root) and §0 (the seam
  dispatches to a handler/asset which uses a `ScopeSource` — the seam itself knows nothing
  about pytest); `spec.md` FR-009 / FR-012, SC-002, NFR-002.

## Branch Strategy
- **Planning base / merge target**: `design/doctrine-controlled-gates`. This WP branches
  atop **WP03** (the gate package + `Scope` type must exist first).

## Subtasks & Detailed Guidance

### T029 — Define the `ScopeSource` protocol
In `src/specify_cli/review/gates/scope_source.py` define:

```python
class ScopeSource(Protocol):
    def derive(self, changed_files: Sequence[str]) -> Scope: ...
```

- `Scope` is the **single** canonical scope type threaded from WP03
  (`TransitionContext.scope`). If WP03's data-model uses `ScopeResult` from
  `pre_review_gate`, alias/re-export it here so downstream (WP08 handler, Path-B) import
  one type. Do not introduce a parallel dataclass.
- Keep the protocol minimal — `derive` only. Repo-root / config are constructor-injected
  into concrete implementations, not protocol parameters, so a consumer `ScopeSource` has
  no obligation to spec-kitty's `repo_root` census contract.
- The protocol must be portable: nothing pytest-specific in its signature (per the Domain
  Language table — a `ScopeSource` is "not intrinsically pytest-bound").

### T030 — Move the spec-kitty census into a built-in `ScopeSource`
Wrap the existing spec-kitty CI-topology census as a **built-in** `ScopeSource`
(e.g. `SpecKittyCensusScopeSource`) whose `derive` calls `derive_test_scope`:

- The census authorities stay in `pre_review_gate.py` but become reachable **only**
  through this built-in `ScopeSource`: `_SRC_PACKAGE_PREFIX` (`:98`),
  `_GATE_COVERAGE_MODULE_NAME` (`:100`), `_load_gate_coverage_module` (`:131`),
  `_default_filter_groups` (`:162`), `_default_composite_routing` (`:170`),
  `derive_test_scope` (`:278`).
- The built-in `ScopeSource` is **active only when spec-kitty's own doctrine is active**
  (FR-012). It is a doctrine-selected strategy — WP08 binds it via the built-in step
  contract; here you make it *a* `ScopeSource`, you do not force-apply it. Ensure the
  built-in carries whatever identity WP03/WP08 needs to select it (URN / name) but the
  selection logic itself is WP08's binding + WP03's resolver.
- Preserve `GateAuthoritiesUnavailable` (`pre_review_gate.py:110`) semantics: the built-in
  `ScopeSource.derive` may raise it (unavailable/outside-repo authority) exactly as
  `derive_test_scope`'s caller expects — the fail-open fold is the consumer's (WP08/WP13),
  not swallowed here.

### T031 — `derive_test_scope` extraction stays ≤ C(15)
`derive_test_scope` (`pre_review_gate.py:278-341`) currently sits **at** the C(15)
cognitive-complexity ceiling.

- Any refactor to route it under the `ScopeSource` port must keep it **≤ 15** (ruff C901 /
  Sonar S3776 aligned). Prefer extracting the per-file inner loop body
  (`focused_group_names` matching + composite-dir routing, `:307-337`) into a small pure
  helper rather than adding branches.
- **Do NOT** add a `# noqa: C901`. If the wrapping pushes it over, decompose it — the
  spec explicitly names this as the risk (research §5.5).
- The `filter_groups` / `composite_routing` override seam on `derive_test_scope` is used
  by unit tests (`test_pre_review_scope_singlesource.py`) — keep that override seam intact.

### T032 — Test: undeclared consumer fixture does not force-apply the built-in
Add a focused test proving FR-009 / NFR-002:

- A **non-pytest** fixture (no `tests/architectural/_gate_coverage.py`, no
  `src/specify_cli/` layout) with **no declared `ScopeSource`** must **not** silently get
  the spec-kitty built-in `ScopeSource` applied. The built-in is doctrine-selected, not a
  default.
- Assert the output path contains **none** of `tests.architectural._gate_coverage` or
  `src/specify_cli/` — the built-in census must not leak when it is not selected (this is
  the WP-level unit proof; the full consumer-fixture CALM-NOTICE acceptance is WP13).
- Add a positive counterpart: when the built-in `ScopeSource` **is** selected (spec-kitty
  doctrine active), `derive` reproduces `derive_test_scope`'s scope for a known changed-file
  set (parity anchor for WP08's NFR-001).

## Test Strategy
- `ScopeSource` protocol conformance test (the built-in satisfies it; a trivial fake
  satisfies it).
- `derive_test_scope` complexity guard: confirm ruff C901 clean (no new suppression).
- FR-009/NFR-002 non-force-apply test (T032) + built-in parity test.
- Existing `test_pre_review_scope_singlesource.py` and `pre_review_gate` unit suite green.

## Risks & Mitigations
- **Complexity ceiling breach** on `derive_test_scope` → extract the inner loop body to a
  pure helper; test the helper directly (Sonar rewards testable extraction).
- **Scope-type fork** → reuse the WP03 `Scope`/`ScopeResult`; do not define a second
  dataclass (Note-for-tasks #7).
- **Premature removal of the decision tail** → do NOT delete the hardcoded decision path
  here; that is WP08 (C-004). This WP adds the strategy seam and moves the census behind
  it, leaving the current caller intact until WP08 inverts it.

## Safeguards / MUST NOT touch
- **MUST NOT** fork a second scope type — thread the one `Scope`/`ScopeResult` from WP03.
- **MUST NOT** add `# noqa: C901` / `# type: ignore` to `derive_test_scope`; keep it ≤ 15
  by decomposition.
- **MUST NOT** force-apply the built-in `ScopeSource` as a default — it is doctrine-
  selected (FR-012); a consumer with no declared source gets the FR-008 notice (WP13).
- **MUST NOT** remove the hardcoded `pre_review_gate` decision path (that is WP08, C-004),
  nor touch `handlers/pre_review.py`, `resolver.py`, `outcomes.py`, `tasks_move_task.py`,
  or `pre_review_hook.py`.
- **MUST** keep `GateAuthoritiesUnavailable` raise semantics so the consumer's fail-open
  fold still fires.

## References (file:line, from research §1)
- `pre_review_gate.py:98` — `_SRC_PACKAGE_PREFIX = "src/specify_cli/"` (moves behind the
  built-in `ScopeSource`; FR-012).
- `pre_review_gate.py:100` — `_GATE_COVERAGE_MODULE_NAME = "tests.architectural._gate_coverage"`.
- `pre_review_gate.py:110` — `GateAuthoritiesUnavailable` (preserve raise semantics).
- `pre_review_gate.py:131` — `_load_gate_coverage_module` (refuse-outside-repo_root).
- `pre_review_gate.py:162` / `:170` — `_default_filter_groups` / `_default_composite_routing`.
- `pre_review_gate.py:219-221` — `_SRC_PACKAGE_PREFIX` prefix strip in `_src_dir_segment`.
- `pre_review_gate.py:278-341` — `derive_test_scope` (keep ≤ C(15); override seam intact).
- `pre_review_gate.py:451-511` — `evaluate_with_scope` (the reuse anchor consumed by WP08,
  **not** modified here).

## Review Guidance
- Recommended sign-off: **reviewer-renata** (+ architect lens on the `ScopeSource`
  protocol shape if available).
- Confirm: one `Scope` type (no fork); `derive_test_scope` ≤ 15 with no new suppression;
  the consumer-facing path no longer hard-imports `_gate_coverage` / `_SRC_PACKAGE_PREFIX`;
  T032 proves the built-in is not force-applied.

## Activity Log
- 2026-07-11T00:00:00Z – system – Prompt created.
