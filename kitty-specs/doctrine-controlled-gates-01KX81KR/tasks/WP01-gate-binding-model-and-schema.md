---
work_package_id: WP01
title: Gate-binding model + step-contract schema
dependencies: []
requirement_refs:
- FR-001
- FR-016
- C-006
tracker_refs:
- '2535'
planning_base_branch: design/doctrine-controlled-gates
merge_target_branch: design/doctrine-controlled-gates
branch_strategy: Planning artifacts for this mission were generated on design/doctrine-controlled-gates. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into design/doctrine-controlled-gates unless the human explicitly redirects the landing branch.
subtasks:
- T001
- T002
- T003
- T004
- T005
phase: Lane A - Charter spine
history:
- at: '2026-07-11T00:00:00Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: python-pedro
authoritative_surface: src/doctrine/missions/
execution_mode: code_change
owned_files:
- src/doctrine/missions/step_contracts.py
- src/doctrine/missions/models.py
create_intent: []
role: implementer
tags: []
task_type: implement
---

# WP01 — Gate-binding model + step-contract schema *(Lane A, foundational)*

## Context

This is the **foundational sub-WP of Lane A (the charter spine)** and the keystone
that everything downstream imports. It adds the declarative data type that lets a
mission **step contract** bind a gate to a transition — the concept the whole
mission is built on (FR-001). Nothing runs it here; WP01 only lands the *shape*.

Per the **plan's Notes-for-/tasks #1** and `research.md §0`: the SSOT selection
seam (WP03, `src/specify_cli/review/gates/resolver.py`) **imports `GateBinding`
from `src/doctrine`**, and the architectural layer rule forbids `src/doctrine`
from importing `specify_cli` (verified by
`tests/architectural/test_layer_rules.py::test_doctrine_does_not_import_specify_cli`,
around line 244). That is exactly why the binding model must live in
`src/doctrine` and ship **first** — Lanes A and B are *not* independent, and WP03
depends on this WP. Keep the type pure doctrine data: no `specify_cli` import, no
runtime/dispatch logic.

**What WP01 delivers:**
1. A frozen `GateBinding` pydantic model in `src/doctrine/missions/` carrying the
   canonical shape from `data-model.md` — `transition`, `gate_ref`, `mechanism`
   (`handler|asset`), `on_unrunnable` (T001).
2. An **optional** `gate` binding field added to both the legacy
   `MissionStepContractStep` (`step_contracts.py:65`) and the unified
   `MissionStep` (`models.py:87`) — a **versioned schema evolution** on
   `extra="forbid"` models, so old contracts still load (T002, FR-016, C-006).
3. Red-first tests proving both the **backward-compatible load** (SC-009) and the
   **new-field validation + round-trip** (T003, T004).
4. A confirmation that the arch layer rule stays green — `src/doctrine` still has
   zero `specify_cli` imports (T005).

### Canonical `GateBinding` shape (from `data-model.md`, do not invent fields)

| Field | Type | Notes |
|-------|------|-------|
| `transition` | `str` | the lane/action the gate fires on (e.g. `for_review`) |
| `gate_ref` | `str` (URN) | `urn:gate-handler:<id>` (Path A) or `urn:asset:<id>` (Path B) |
| `mechanism` | enum `handler` \| `asset` | which dispatch path |
| `on_unrunnable` | enum `warn` (default) | reserved; fail-open is the only value this mission ships |

`mechanism` and `on_unrunnable` live **inside** `binding` (per `research.md §0`);
the runtime `ResolvedGate` wrapper (WP03) adds `declaring_doctrine` and
`activation_state` around it — **do not** add those to `GateBinding` here.

## Ordered steps

Follow ATDD: for T003 and T004 write the **failing test first**, watch it go red
against the current models, then make it green with the schema change (T001/T002).

### T001 — Add the `GateBinding` model (`src/doctrine`)
- Add a `GateBinding` pydantic `BaseModel` to `src/doctrine/missions/`. The two
  owned files are `step_contracts.py` and `models.py`; place `GateBinding` where
  both can import it without a cycle. `step_contracts.py` already imports from
  `doctrine.artifact_kinds` and `doctrine.base`; `models.py` is the unified-model
  home. Prefer defining `GateBinding` **once** (e.g. in `models.py`, which
  `step_contracts.py` may import — confirm no import cycle) and reusing it from
  both step models, rather than two divergent copies. One canonical definition
  (charter: single canonical authority).
- Use `model_config = ConfigDict(extra="forbid", frozen=True)` to match every
  sibling model in these files (`MissionStepInput:58`, `MissionStepContractStep:75`,
  `DelegatesTo:49`).
- Model the four fields exactly as the table above. Use `Literal["handler",
  "asset"]` for `mechanism` and `Literal["warn"]` (default `"warn"`) for
  `on_unrunnable` — the reserved single-value enum is intentional (fail-open is
  the only shipped value; keeping it an enum makes the future widening a
  non-breaking schema evolution).
- Add `GateBinding` to the module `__all__`.
- **MUST NOT** import anything from `specify_cli`, add dispatch/runtime behavior,
  or reference handler/asset *implementations* — this is pure declarative data.

### T002 — Add the optional `gate` field to both step models
- On `MissionStepContractStep` (`step_contracts.py:65`) add
  `gate: GateBinding | None = None`. Because the model is `extra="forbid"`, the
  field being **optional with a `None` default** is what preserves backward
  compatibility — a pre-mission `*.step-contract.yaml` with no `gate:` key still
  validates (FR-016).
- On the unified `MissionStep` (`models.py:87`) add the same
  `gate: GateBinding | None = None`. Keep it consistent with that model's
  `populate_by_name=True` config; only add an alias if the on-disk key differs
  from the field name (it should be `gate`, so no alias is needed).
- This is a **versioned schema evolution**, not a silent field add (C-006): note
  the addition in the model docstring(s) tying it to FR-001/FR-016. If these
  models carry a `schema_version` surface (`MissionStepContract.schema_version`
  at `step_contracts.py:98`), keep the existing `"1.0"` contracts loading — the
  optional field means no version bump is *required* for old files to load, which
  is the FR-016 guarantee. Do not tighten `schema_version` validation such that
  old contracts stop loading.
- **MUST NOT** make the field required, and **MUST NOT** relax `extra="forbid"`.

### T003 — Red-first: a pre-mission built-in contract (no `gate`) still loads (SC-009/FR-016)
- Write the failing test **first** (it will pass trivially once the field is
  optional, so assert it *concretely*): load a representative built-in contract
  that has **no** `gate` binding — e.g. round-trip
  `src/doctrine/missions/built_in_step_contracts/specify.step-contract.yaml` (or
  `plan`/`tasks`) through `MissionStepContractRepository` / the model — and assert
  it loads with every `step.gate is None`.
- Add a parallel case for the unified `MissionStep`: a step dict without a `gate`
  key validates and yields `gate is None`.
- This is the SC-009 "authored-before-this-mission contract still loads" proof.
  Place it near the existing step-contract model tests
  (`tests/doctrine/` — locate the current `MissionStepContractStep` /
  `MissionStep` tests and co-locate).

### T004 — Red-first: the new `gate` field validates + round-trips
- Write the failing test **first** against the current (pre-T001/T002) models to
  prove the field does not yet exist (constructing a step with `gate=...` raises
  under `extra="forbid"`, or the model has no such field). Then implement to green.
- Assert a valid `GateBinding` (`transition="for_review"`,
  `gate_ref="urn:gate-handler:pre-review-regression"`, `mechanism="handler"`,
  `on_unrunnable="warn"`) attaches to a `MissionStepContractStep` and to a
  `MissionStep`, survives a YAML/dict round-trip, and is frozen.
- Assert invalid inputs are rejected: an unknown `mechanism` value, and (because
  the parent is `extra="forbid"`) an unknown extra key inside the binding.
- Use realistic, production-shaped URNs and transition names (not `"foo"`/`"bar"`).

### T005 — Confirm zero `specify_cli` imports from `src/doctrine` (arch gate stays green)
- Run `tests/architectural/test_layer_rules.py::test_doctrine_does_not_import_specify_cli`
  (and the surrounding `Invariant 2` class) and confirm it is green after your
  change. If you accidentally reached for a `specify_cli` type (e.g. a URN helper),
  move the dependency down into `src/doctrine`/`kernel` or inline it — never import
  upward.
- Do **not** add a new suppression to make this pass; the invariant is the point.

## Acceptance criteria

- **SC-009** (primary): a built-in step contract authored before this mission (no
  `gate` field) still loads, **and** the new `gate` binding validates + round-trips
  — both covered by tests (T003, T004). Concretely testable: the two tests above
  are green, and T004 demonstrably failed against the pre-change models.
- **FR-001**: a step contract can carry one or more gate bindings on its
  activatable step surface as *data* (the `gate` field), not a hardcoded branch.
- **FR-016 / C-006**: the field is a versioned evolution of `extra="forbid"`
  models; old-load and new-field-validation are both tested; no silent field add.
- **T005**: `test_doctrine_does_not_import_specify_cli` green.
- ruff + mypy clean on both owned files with **zero** new `# noqa` / `# type:
  ignore`; no function pushed over cognitive-complexity 15.

## Safeguards / MUST NOT touch

- **`src/doctrine` MUST NOT import `specify_cli`** (arch layer rule,
  `test_layer_rules.py:244`). `GateBinding` is pure doctrine data. This is the
  reason the model lives here and not in `review/gates/`.
- **Backward compatibility is load-bearing**: the models are `extra="forbid"`.
  The `gate` field MUST be optional with a `None` default. Do **not** make it
  required, do **not** remove or weaken `extra="forbid"`, and do **not** change
  `MissionStepContract.validate_unique_step_ids` semantics.
- **No dispatch/runtime logic here.** No handler registry, no resolver, no
  activation reads — those are WP02 (activation) and WP03 (the seam). WP01 ships
  the *shape* only. Do not import or reference `filter_graph_by_activation`,
  `MissionStepContractRepository.get_by_action` dispatch, or any gate runner.
- **Do not** edit the built-in `*.step-contract.yaml` files here — adding the
  `gate:` binding to the built-in `implement` contract is **WP02's** T007. WP01
  must not create a merge collision on those files.
- Keep `GateBinding` defined **once** (single canonical authority); do not fork a
  second copy between `step_contracts.py` and `models.py`.

## References (file:line anchors — verified in this repo)

- `src/doctrine/missions/step_contracts.py:65` — `MissionStepContractStep`
  (`extra="forbid", frozen=True`; fields `id/description/command/inputs/
  delegates_to/guidance`); `__all__` at `:31`; `MissionStepContract` at `:85` with
  `schema_version` at `:98` and `validate_unique_step_ids` at `:103`.
- `src/doctrine/missions/models.py:87` — unified `MissionStep`
  (`frozen=True, extra="forbid", populate_by_name=True`); `__all__` at `:45`.
- `tests/architectural/test_layer_rules.py:244` —
  `test_doctrine_does_not_import_specify_cli` (Invariant 2 class, "doctrine must
  not import from specify_cli or charter").
- `kitty-specs/doctrine-controlled-gates-01KX81KR/data-model.md` — `GateBinding`
  and `ResolvedGate` field tables (the canonical shape; do not invent fields).
- `kitty-specs/doctrine-controlled-gates-01KX81KR/contracts/gate-resolution-seam.md`
  — confirms `mechanism`/`on_unrunnable` live inside `binding`, and that WP03's
  resolver imports `GateBinding` from `src/doctrine`.
- `research.md §2` — step-contract consultation model; both step models are
  `extra="forbid"` → versioned schema evolution + migration (FR-016, C-006).
- `plan.md` Notes-for-/tasks **#1** — the foundational `GateBinding` sub-WP ships
  first in Lane A; WP03 depends on it (lanes A and B are not independent).
