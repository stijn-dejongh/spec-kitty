# Feature Specification: Runtime-Bridge God-Module Decomposition

**Mission**: runtime-bridge-degod-01KX8M1C
**Closes**: #2531 · **Epics**: #1619 (runtime/state overhaul), #2173 (infra-logic separation)
**Siblings** (same shape): #2056 `agent/mission.py`, #2057 `merge.py`, #2059 `doctor.py`, #2464 `agent/workflow.py`

## Summary

`src/runtime/next/runtime_bridge.py` is the single largest module in the repo —
**3,813 LOC** (+49% since the 2026-05 CaaCS audit), carrying two
`# noqa: C901`-suppressed guard functions (`_check_cli_guards:1057`,
`_check_composed_action_guard:1515`) and a ~535-line `decide_next_via_runtime`
orchestrator, all far past the complexity ceiling of 15. Docstringed as a
"bridge" between the CLI's `decide_next()` and the internal `_internal_runtime`
DAG engine, at ~4k lines it is a hub, not a bridge.

This mission gives it the **Ports+cores** treatment per #2173: inject the
I/O-bearing seams (identity/coordination resolution, `feature-runs.json` index,
template/pack discovery, run lifecycle) behind **narrow ports**, and extract the
parsing/mapping/gating logic (tasks.md parsing, decision mapping, guard
predicates) as **pure, directly unit-testable cores** — leaving `runtime_bridge.py`
a thin orchestration surface that composes them. It is a **behavior-preserving
structural refactor**: the `spec-kitty next` / `decide_next()` CLI contract does
not change.

## User Scenarios & Testing

### Primary scenario (maintainer changes composition-dispatch logic)
A maintainer needs to change how a composed action dispatches. Today that logic
is buried in the ~570-LOC composition-dispatch cluster and the F-complexity
`_check_composed_action_guard`. After this mission it lives in a focused,
named, directly unit-testable core — the maintainer edits it and runs its own
fast test module, without spinning the whole runtime.

### Behavioral-parity scenario (the load-bearing guarantee)
`spec-kitty next` (→ `decide_next()`) produces the **identical** decision, for
every fixture in the characterization matrix, before and after the refactor. No
operator or agent observes any change.

### Pure-core scenario
The tasks.md-parsing and decision-mapping cores are imported and unit-tested in
isolation with plain in-memory inputs — no filesystem, no `meta.json`, no git.

## Functional Requirements

| ID | Requirement | Status |
|----|-------------|--------|
| FR-001 | Extract `runtime_bridge.py`'s cohesive seams: **I/O-bearing** seams as narrow **ports** (identity/coordination resolution incl. `meta.json` + coord-branch naming; `feature-runs.json` compat-index; template/pack discovery; run lifecycle start/lookup), and **parsing/mapping/gating** logic as pure **cores** (tasks.md parsing; query-decision building + `NextDecision`→`Decision` mapping; guard predicates; composition-dispatch adapter; retrospective/learning-capture orchestration; operational-context building). | Proposed |
| FR-002 | A **research pass confirms/refines** the final module boundaries + naming **before extraction begins**, recorded in `research.md` (the seam list below is the starting hypothesis, not the frozen answer). | Proposed |
| FR-003 | Ports inject I/O so the pure cores take plain data and are unit-testable **without** filesystem/git/`meta.json` access; the split follows #2173 (inject infra as ports, keep the core pure). | Proposed |
| FR-004 | The two `# noqa: C901` functions (`_check_cli_guards`, `_check_composed_action_guard`) **and** the ~535-line `decide_next_via_runtime` orchestrator are reduced to **≤ complexity 15**, with the `# noqa: C901` suppressions **removed** (not relocated). | Proposed |
| FR-005 | `runtime_bridge.py` becomes a **thin orchestration/composition surface** that composes the extracted ports+cores. | Proposed |
| FR-006 | **Each extracted seam carries focused tests**: pure cores unit-tested in isolation; ports contract-tested against stubs. | Proposed |
| FR-007 | A **top-of-file decomposition pointer** is added to `runtime_bridge.py` referencing #2531, matching the sibling-god-module convention (#2056/#2057/#2059/#2464). | Proposed |
| FR-008 | The composition-dispatch seam **isolates `_check_composed_action_guard`'s selection decision as a clean, testable core** — leaving a seam a future consumer can route through **without** this mission coupling to it. (Coordination note: unblocks the later gates mission #2535 WP14; do not import or depend on that mission's code here.) | Proposed |

## Non-Functional Requirements

| ID | Requirement | Threshold / Measure | Status |
|----|-------------|---------------------|--------|
| NFR-001 | Behavioral parity — no change to the `spec-kitty next` / `decide_next()` CLI contract. | A before/after **characterization suite** over `decide_next()` produces byte-identical decisions on a fixture matrix; all existing `runtime/next` tests stay green (zero new failures attributable to the refactor). | Proposed |
| NFR-002 | Complexity — every extracted core and the residual orchestrator is at or below the ceiling. | `ruff --select C901` reports **zero** functions >15 in `runtime_bridge.py` and the new seam modules; **zero** `# noqa: C901` remain. | Proposed |
| NFR-003 | Pure-core testability. | Each pure core has ≥1 direct unit test that exercises it with in-memory inputs and **no** I/O (importable + tested standalone). | Proposed |
| NFR-004 | No new public surface. | No new CLI command/flag and no new public API; internal seam modules only. | Proposed |
| NFR-005 | Size reduction of the god-module itself. | `runtime_bridge.py` drops from 3,813 LOC to a thin surface (target ≤ ~40% of current; exact figure set by the FR-002 research once seam boundaries are fixed). | Proposed |

## Constraints

| ID | Constraint | Status |
|----|------------|--------|
| C-001 | **Behavior-preserving** — this is a pure structural refactor; decision logic is not changed, only relocated. | Active |
| C-002 | **Ports+cores per #2173** — inject I/O as ports, keep decision/parsing/mapping cores pure. Do not invent a different structure. | Active |
| C-003 | Follow the **sibling-god-module decompose convention** (#2056/#2057/#2059/#2464) — matching module layout + top-of-file decomposition pointer. | Active |
| C-004 | **Characterization-first** (extract-then-inject) — golden characterization tests over `decide_next()` land **before** any extraction; the C901 functions + orchestrator are never edited in place without a green golden guard. | Active |
| C-005 | Do **not** adopt or depend on the gates mission (#2535) `resolve_gates` seam — it is unlanded. Only leave `_check_composed_action_guard` a clean seam (FR-008). | Active |
| C-006 | **Sequencing** — per the roadmap + #2531 body, this mission is Wave-4-ish, following the Wave-2 coord-authority trio degod (#2160 / PR #2545) and the Wave-3 `orchestrator_api` degod. It shares the `runtime/next/` surface with those, so coordinate/rebase against them; it does not jump the queue. | Active |

## Key Entities (starting seam hypothesis — FR-002 confirms)

- **Ports (I/O)**: identity/coordination resolution (`meta.json` + coord-branch naming); `feature-runs.json` compat-index; template/pack discovery; run lifecycle (start/lookup).
- **Pure cores**: tasks.md parsing; query-decision building + `NextDecision`→`Decision` mapping; CLI guard predicates; composition-dispatch adapter (incl. the `_check_composed_action_guard` selection decision); retrospective/learning-capture orchestration; operational-context building.
- **Thin residual**: `decide_next_via_runtime` orchestrator composing the above (phase-split — dependency-gate / composition-dispatch / decision-materialize — mirroring #2464's `implement`/`review` precedent).

## Success Criteria

| ID | Criterion |
|----|-----------|
| SC-001 | `runtime_bridge.py` is reduced from 3,813 LOC to a thin orchestration surface (per the NFR-005 target set by research). |
| SC-002 | **Zero** `# noqa: C901` remain in `runtime_bridge.py`; `_check_cli_guards`, `_check_composed_action_guard`, and `decide_next_via_runtime` are each ≤ 15. |
| SC-003 | `spec-kitty next` / `decide_next()` produces **identical** decisions before and after, across the characterization fixture matrix (NFR-001). |
| SC-004 | Every extracted pure core passes a direct unit test run in isolation (no I/O). |
| SC-005 | The decomposition pointer is present and the seam modules follow the #2173 ports+cores + sibling-convention layout. |

## Assumptions

- The FR-002 research pass fixes the final seam boundaries/naming; the seam list here is the informed starting hypothesis from #2531's structural skim.
- Sibling decomposes (#2056/#2057/#2059/#2464) are the layout template.
- The mission is sequenced after the trio degod and the `orchestrator_api` degod (Wave 4); it will rebase against whatever they land in `runtime/next/`.

## Out of Scope

- Any **behavioral/functional change** to decision logic — pure structural refactor only.
- Adopting the gates-mission (#2535) `resolve_gates` seam — that inversion is gates WP14, sequenced after this mission (FR-008 only leaves the seam clean).
- The broader runtime/state overhaul beyond `runtime_bridge.py` (root epic #1619) and the `orchestrator_api` degod (its own Wave-3 slice).
