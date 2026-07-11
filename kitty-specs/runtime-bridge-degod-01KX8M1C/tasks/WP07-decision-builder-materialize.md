---
work_package_id: WP07
title: Decision-builder + query/answer materialize (FR-011)
dependencies: [WP06]
requirement_refs:
- FR-011
- FR-004
tracker_refs:
- '2531'
planning_base_branch: design/runtime-bridge-degod
merge_target_branch: design/runtime-bridge-degod
branch_strategy: Planning artifacts for this mission were generated on design/runtime-bridge-degod. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into design/runtime-bridge-degod unless the human explicitly redirects the landing branch.
subtasks:
- T025
- T026
- T027
phase: Extraction spine
history:
- at: '2026-07-11T00:00:00Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: python-pedro
authoritative_surface: src/runtime/next/
create_intent:
- src/runtime/next/runtime_bridge_cores.py
- tests/runtime/test_bridge_decision_builder.py
execution_mode: code_change
owned_files:
- src/runtime/next/runtime_bridge_cores.py
- src/runtime/next/runtime_bridge.py
- tests/runtime/test_bridge_decision_builder.py
role: implementer
tags: []
task_type: implement
---

# Work Package Prompt: WP07 – Decision-builder + query/answer materialize (FR-011)

## Context

This WP lands the **single highest complexity lever** in the mission: a canonical
Decision-builder core that collapses the **29 open-coded `Decision(...)` constructions**
(confirmed count in the source) and the 4× `_state_to_action → _build_prompt_or_error →
step-or-blocked` triad, then uses it to drive the decision-materialize offenders on the
query and answer paths under the complexity ceiling. Behavior-preserving (C-001).

It shares `runtime_bridge_cores.py` with WP06 (**serial** — `dependencies: […, WP06]`; both
list the file in `create_intent`). WP06 lands the parse family + `evaluate_guards` and leaves
the module structured for WP07 to append the Decision-builder without churn. It also depends
on **WP01/WP02** — the parity oracle and compat guard are the blocking acceptance gate
(C-004), and this WP is precisely where under-coverage would bite: the oracle MUST exercise
the **14 query/answer-only sites** (incl. the CC≈33 `_map_runtime_decision` cluster), which
driving `decide_next` alone never reaches (contracts/parity-oracle.md §Scope).

### What this WP owns (research.md §Seams / plan.md IC-06)

1. **`DecisionEnvelope` + `step_or_blocked` core (FR-011)** — the normalized inputs a
   `Decision` is built from + the materializer. **blocked / query / terminal branches are
   PURE; the step branch is PORT-INJECTED.** `Decision.__post_init__` (`decision.py:129`) runs
   `Path(prompt).is_file()` for `kind="step"`, so constructing a step Decision is intrinsically
   I/O-bearing. The builder therefore takes a `prompt_exists: Callable[[str], bool]` predicate
   (real `Path.is_file` in production; an in-memory stub in the pure unit test) — the step
   branch is port-injected, not filesystem-pure (data-model.md §DecisionEnvelope). All
   non-deterministic fields (`timestamp` `bridge:2542`, ULIDs) are stamped by the caller/residual,
   **not** the builder.
2. **The query/answer materialize offenders** reduced ≤15 by routing through the builder:
   - `_map_runtime_decision:3555` (CC≈33; 10 sites on the answer path, `answer_decision_via_runtime`).
   - `query_current_state:3199` (CC≈16).
   - the 4 `_build_*_query_decision` builders reached **exclusively** via `query_current_state`:
     `_build_finalized_override_query_decision:3059`, `_build_initial_query_decision:3111`,
     `_build_decision_required_query:3136`, `_build_runtime_query_decision:3166`.

## Ordered Steps

### T025 — `DecisionEnvelope` + `step_or_blocked`; collapse the 29 `Decision(` sites

1. In `runtime_bridge_cores.py` (appending to WP06's structure), add:
   - `DecisionEnvelope` — a value object carrying the normalized inputs (kind, agent, mission
     identity, state, action, wp_id, step_id, guard_failures, progress, question/options, …;
     data-model.md §DecisionEnvelope).
   - `step_or_blocked(envelope, guard_failures, *, prompt_exists) -> Decision` — pure for the
     blocked/query/terminal branches; the step branch calls the injected `prompt_exists`
     predicate instead of touching disk.
2. Replace the **29 open-coded `Decision(...)` constructions** and the 4× triad across
   `runtime_bridge.py` with calls into `step_or_blocked` / the builder. The caller supplies the
   non-deterministic fields (timestamp/ULIDs) so the core stays deterministic (NFR-003).
3. Keep the import DAG acyclic — `cores` imports only stdlib / `Lane` / decision types; no
   `decision → runtime_bridge_*` top-level edge (C-007). The `decision.py:428` lazy edge stays
   lazy.

### T026 — Own the query/answer materialize; reduce the offenders ≤15

1. **`_map_runtime_decision:3555` (CC≈33)** — route its 10 answer-path `Decision(...)` sites
   through the builder; extract the residual branch logic into small named helpers so the
   function lands **≤15**.
2. **The 4 `_build_*_query_decision` builders** (`:3059`/`:3111`/`:3136`/`:3166`) — re-express
   each as a thin envelope-populate + `step_or_blocked` call. These are reached only via
   `query_current_state`, so their sentinel/oracle coverage runs through the **query** entry.
3. **`query_current_state:3199` (CC≈16)** — collapsing the 4 builders into the shared
   materializer is what drives this ≤15. Extract any remaining branching into helpers.
4. Remove any `# noqa: C901` touched — do not relocate (FR-004/NFR-002). `ruff --select C901`
   reports zero offenders on the touched functions; radon confirms.
5. Guarded re-export: every relocated-but-patched symbol stays reachable at
   `runtime_bridge.<name>` (FR-012). `_state_to_action`, `_build_prompt_or_error` are
   SPLIT-flag symbols (patchable via the residual path, dead via the render-seam path —
   research.md §Compat) — keep the residual path the live one so the compat sentinel fires.

### T027 — Pure unit tests; re-export; oracle + compat green (esp. the 14 query/answer sites)

1. Create `tests/runtime/test_bridge_decision_builder.py`:
   - Direct in-memory tests of `step_or_blocked` for **blocked / query / terminal** branches
     (no I/O), plus the **step** branch with an in-memory `prompt_exists` stub for both
     True/False (NFR-003/SC-004) — assert the constructed `Decision` fields.
   - Assert the builder never stamps timestamp/ULIDs itself (they are threaded by the caller).
   - A regression asserting all 29 former open-coded sites now route through the builder (e.g. a
     count/AST check, or coverage that each collapsed site produces the expected envelope).
2. Confirm re-export identity (`runtime_bridge.x is runtime_bridge_cores.x`) for relocated
   patched symbols.
3. Re-run the acceptance gate (below), with explicit attention to the oracle's **query and
   answer sub-ledgers** — the 14 query/answer-only sites incl. `_map_runtime_decision`.

## Acceptance

- 29 open-coded `Decision(...)` sites + the 4× triad collapsed into one `DecisionEnvelope` +
  `step_or_blocked` core (FR-011); step branch port-injected via `prompt_exists`.
- `_map_runtime_decision`, `query_current_state`, and the 4 `_build_*_query_decision` builders
  are each **≤15**; no `# noqa: C901` remains on any touched function (FR-004).
- Direct in-memory unit tests cover blocked/query/terminal (pure) + step (stubbed predicate)
  branches (NFR-003/SC-004).
- **Acceptance gate:** WP01 parity oracle green on **all 3 entries** — specifically green on
  the **14 query/answer sites** (the false-green minefield this WP most risks); WP02 compat
  guard green with each relocated symbol's sentinel firing through its reaching entry
  (`_map_runtime_decision` via `answer_decision_via_runtime`; the `_build_*_query_decision`
  family via `query_current_state`).

## Safeguards

- **Do not make the step branch pure.** `Decision.__post_init__` stats disk at `decision.py:129`
  — a "pure" step builder would either lie or crash. Inject `prompt_exists`; production passes
  `Path.is_file`, the unit test passes a stub.
- The builder must **not** stamp `timestamp`/`run_id`/`decision_id` — the caller/residual does
  (the oracle masks these; a builder that stamped them could hide a real field change).
- Serial co-ownership with WP06: append to `runtime_bridge_cores.py`, do not rewrite WP06's
  parse family / `evaluate_guards` blocks.
- Per-entry reach mapping is binding for the compat sentinel — a query/answer-only symbol driven
  through `decide_next` is a vacuous pass (contracts/compat-surface.md).
- Never stub `next_step` in the oracle — it is the logic under test.

## References

- `src/runtime/next/runtime_bridge.py:3555` — `_map_runtime_decision` (CC≈33, 10 answer-path sites).
- `src/runtime/next/runtime_bridge.py:3199` — `query_current_state` (CC≈16).
- `src/runtime/next/runtime_bridge.py:3059`/`:3111`/`:3136`/`:3166` — the 4 `_build_*_query_decision` builders (query-only).
- `src/runtime/next/runtime_bridge.py:3355` — `answer_decision_via_runtime` (owning entry for the map-decision cluster).
- `src/runtime/next/decision.py:129` — `Path(prompt).is_file()` in `__post_init__` (why the step branch is port-injected).
- `kitty-specs/runtime-bridge-degod-01KX8M1C/data-model.md` §DecisionEnvelope + step_or_blocked.
- `kitty-specs/runtime-bridge-degod-01KX8M1C/contracts/parity-oracle.md` §Scope — the query/answer sub-ledgers.
- `kitty-specs/runtime-bridge-degod-01KX8M1C/contracts/compat-surface.md` — per-entry reach mapping.
- `kitty-specs/runtime-bridge-degod-01KX8M1C/spec.md` — FR-011, FR-004, NFR-001, SC-006.
