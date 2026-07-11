---
work_package_id: WP02
title: Kind-map + DRG regen + built-in migration
dependencies:
- WP01
requirement_refs:
- FR-006
- FR-016
tracker_refs:
- '2535'
planning_base_branch: design/doctrine-controlled-gates
merge_target_branch: design/doctrine-controlled-gates
branch_strategy: Planning artifacts for this mission were generated on design/doctrine-controlled-gates. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into design/doctrine-controlled-gates unless the human explicitly redirects the landing branch.
subtasks:
- T006
- T007
- T008
- T009
- T010
phase: Lane A - Charter spine
history:
- at: '2026-07-11T00:00:00Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: python-pedro
authoritative_surface: src/charter/
execution_mode: code_change
owned_files:
- src/charter/drg.py
- src/doctrine/missions/built_in_step_contracts/implement.step-contract.yaml
- src/doctrine/graph.yaml
- src/specify_cli/upgrade/migrations/
create_intent: []
role: implementer
tags: []
task_type: implement
---

# WP02 — Kind-map + DRG regen + built-in migration *(Lane A)*

## Context

WP02 makes the WP01 binding **charter-activatable** and wires the first built-in
gate binding into the shipped doctrine — the second (serial) step of Lane A. It
depends on WP01 (the `GateBinding` model + optional `gate` field must exist first).

The core insight (FR-006, `research.md §0`): a gate's `gate_ref` is a
`urn:gate-handler:<id>` or `urn:asset:<id>`. Those URN kinds — `gate-handler` and
`asset` — are **absent** from the DRG singular↔plural kind maps
(`_SINGULAR_TO_PLURAL`, `src/charter/drg.py:187`), so `filter_graph_by_activation`
would **default-allow** them (they can't be gated directly). The activatable unit
is therefore the **owning step-contract node**, not the gate URN. A gate is active
**iff** its declaring step contract is charter-active. WP02 ensures step-contract-node
activation actually gates the bound gate, then regenerates the DRG so the shipped
`graph.yaml` reflects the schema/binding change and stays freshness/parity-green.

**Important verified state — read before you edit `drg.py`:** `_SINGULAR_TO_PLURAL`
at `src/charter/drg.py:187` **already contains** `"mission_step_contract":
"mission_step_contracts"`, and `_MISSION_STEP_SINGULAR_KINDS` (`:217`) already
routes that kind through `activated_mission_types` via `_owning_mission_type`.
So the *step-contract node is already activatable*. T006 is therefore **not** a
blind "add a dict key" — it is: (a) confirm the owning step-contract node gates
its bound gate; (b) ensure `gate-handler`/`asset` gate-ref URNs are **not** added
as directly-activatable kinds (they must keep default-allow and be gated only via
their owning node); (c) add whatever minimal wiring is needed so a binding's
`gate_ref` inherits its node's activation state. Let the **red-first T010** define
the required behavior and make the smallest `drg.py` change that turns it green —
do not expand the kind map speculatively.

**What WP02 delivers:**
1. DRG kind-map / activation wiring so step-contract-node activation gates the
   bound gate, and inactive doctrine → gate not selected (T006, T010, FR-006).
2. The first real gate binding on the built-in **implement** step contract's
   `status_transition` step — `transition: for_review`,
   `urn:gate-handler:<pre-review>` (T007).
3. A regenerated, committed DRG (`graph.yaml` + `references.yaml`) that passes the
   freshness and activation-parity gates (T008).
4. The versioned migration for the gate-declaring built-in contract(s) — only
   those, not all 17 (T009, FR-016).

## Ordered steps

Lane A is **serial and migration-first** (C-006): land the schema-support edit,
then the built-in binding, then regenerate the DRG, then prove activation gating.
Do **not** parallelize the charter spine (`step_contracts → models → drg → DRG
regen → pack_validator → merge` co-change tightly).

### T007 — Add the `gate` binding to the pre-review built-in step contract
*(do this early so T008's DRG regen and T010's test have a real binding to act on)*
- Edit `src/doctrine/missions/built_in_step_contracts/implement.step-contract.yaml`.
  The pre-review regression gate fires on `move-task --to for_review`, which is the
  **`status_transition`** step of the `implement` contract (its `command:` is
  `spec-kitty agent tasks move-task {wp_id} --to for_review`). Add a `gate:`
  binding to that step:
  ```yaml
  - id: status_transition
    description: Move WP to for_review
    command: "spec-kitty agent tasks move-task {wp_id} --to for_review"
    gate:
      transition: for_review
      gate_ref: "urn:gate-handler:pre-review-regression"   # confirm the canonical id
      mechanism: handler
      on_unrunnable: warn
  ```
- Confirm the exact `gate_ref` URN id against the Path-A handler WP08 will bind
  (the pre-review handler). Use one canonical id; WP08 and WP03's dispatch must
  resolve the *same* URN. If WP08's handler id is not yet pinned, use the
  descriptive `pre-review-regression` slug and note it in the PR so WP08 aligns.
- This is the **only** built-in contract that declares a gate in this mission
  (FR-013 — only the pre-review gate is migrated). Do not add bindings to the
  other 16 built-in contracts.
- Confirm the file still loads through `MissionStepContractRepository` after the
  edit (it uses the WP01 optional `gate` field).

### T006 — Ensure step-contract-node activation gates the bound gate (not default-allow)
- **First read** `src/charter/drg.py:187` (`_SINGULAR_TO_PLURAL`), `:202`
  (`_SINGULAR_TO_PER_KIND_FIELD`), `:217` (`_MISSION_STEP_SINGULAR_KINDS`), and the
  `_owning_mission_type` helper (`:233`) and the activation filter body. Establish
  what already works: `mission_step_contract` is present and routes through
  `activated_mission_types`.
- Make the **minimal** change so that the `gate` binding declared on a
  step-contract node inherits that node's activation decision — i.e. when the
  owning step contract's mission type is **not** activated, the bound gate is
  **not** selected; when it is, the gate is selected. If the existing node-level
  filter already achieves this transitively (because the binding is data *on* the
  node), the `drg.py` change may be limited to a comment/assertion plus the T010
  regression test — that is an acceptable outcome; do not manufacture churn.
- **Do NOT** add `gate-handler` or `asset` to `_SINGULAR_TO_PLURAL` /
  `_SINGULAR_TO_PER_KIND_FIELD` to try to gate the gate-ref URN directly (FR-006
  says those URNs are intentionally default-allow; the *node* is the activatable
  unit). Adding them would also risk the `test_kind_mapping_totality.py` /
  `test_activation_parity_guard.py` guards and create a second, drifting selection
  authority (violates C-001).
- If you touch any module-level dict keyed by a kind enum, re-run
  `tests/doctrine/drg/test_kind_mapping_totality.py` — it enforces totality /
  explicit-partial exemptions for those tables.

### T010 — Red-first: activation on a step-contract node gates its bound gate
- Write the failing test **first**. Construct (or use a fixture with) a mission
  whose `implement` step contract carries the `for_review` gate binding, and:
  - with the owning step contract **charter-active**, assert the bound gate is
    present in the activation-filtered/resolved set;
  - with it **inactive** (mission type not activated), assert the bound gate is
    **absent** (not default-allowed) → this is the FR-006 proof.
- Because the WP03 `resolve_gates` seam does not exist yet, drive this at the
  **DRG/activation layer** (`filter_graph_by_activation` / the charter activation
  surface `drg.py` exposes) — assert on whether the gate binding's owning node
  survives activation filtering, not on `resolve_gates` output. WP03/WP14 prove
  the end-to-end selection; T010 proves the *activation gating* invariant here.
- Prove the test was **red** before T006's wiring (or, if node-level filtering
  already gates it, prove the *default-allow-a-bare-gate-URN* mistake is caught —
  add the negative assertion that a `gate-handler`/`asset` URN is not itself an
  independently-activatable node).

### T008 — Regenerate the DRG; freshness + parity gates green
- After the schema (WP01), kind-map (T006), and built-in binding (T007) changes
  land, **regenerate** the shipped DRG deterministically:
  ```bash
  spec-kitty doctrine regenerate-graph          # writes src/doctrine/graph.yaml
  spec-kitty doctrine regenerate-graph --check   # freshness gate: exits non-zero if stale
  ```
  Commit the regenerated `src/doctrine/graph.yaml`. If the change affects
  synthesized references, regenerate/refresh `references.yaml`
  (`.kittify/charter/references.yaml`) via the charter synthesize/resynthesize
  path so the config↔references parity guard stays green.
- Run the gates and confirm green:
  - `tests/specify_cli/cli/commands/test_doctrine_regenerate_graph.py` (freshness /
    deterministic-regen gate);
  - `tests/doctrine/test_activation_parity_guard.py` (`run_consistency_check` /
    `src/charter/consistency_check.py` — config↔DRG + config↔references parity,
    **fail-closed**).
- **A skipped DRG regen fails the freshness/parity gate** — this step is not
  optional. If the parity guard bites, it means the config/DRG/references are out
  of sync; regenerate rather than suppressing the finding.

### T009 — Migrate the gate-declaring built-in contract(s) (versioned, FR-016)
- The built-in contracts ship inside the package, so the T007 edit **is** the
  built-in migration. Ensure FR-016 is satisfied end-to-end:
  - old built-in/project contracts **without** a `gate` still load (covered by
    WP01 T003, re-assert at the repository level here if not already);
  - the migrated `implement` contract now carries the binding and loads.
- If a **project-layer** data migration is warranted (to add the binding to
  consumer-side copies), place it under `src/specify_cli/upgrade/migrations/`
  following the naming pattern (`m_<version>_<slug>.py`, e.g.
  `m_unify_charter_activation.py`) and the **config-aware** helper
  `get_agent_dirs_for_project(project_path)` — never `mkdir` missing dirs, respect
  deletions (per CLAUDE.md "Writing Migrations"). If no project-layer migration is
  needed (optional field → old contracts just keep loading), state that
  explicitly in the PR rather than adding an empty migration.
- **Only** the gate-declaring built-in contract is migrated (not all 17) — FR-013.

## Acceptance criteria

- **SC-009 / FR-016**: a pre-mission built-in contract still loads; the migration
  adds the binding to the gate-declaring built-in contract; both covered by tests.
- **FR-006**: a gate is active **iff** its declaring step contract is charter-active.
  Proven by T010: node inactive → bound gate absent (no default-allow); node active
  → bound gate present. `gate-handler`/`asset` URNs are **not** independently
  activatable.
- **DRG freshness gate green**: `spec-kitty doctrine regenerate-graph --check`
  exits 0; `test_doctrine_regenerate_graph.py` passes; the committed
  `src/doctrine/graph.yaml` is up to date.
- **Activation-parity gate green (fail-closed)**:
  `tests/doctrine/test_activation_parity_guard.py` passes; no config↔DRG or
  config↔references dangler introduced.
- ruff + mypy clean on `drg.py` (and any migration module); no new `# noqa` /
  `# type: ignore`; no function over cognitive-complexity 15.

## Safeguards / MUST NOT touch

- **Migration-first, single lane, no parallel** (C-006): the charter spine
  (`step_contracts → models → drg → DRG regen → pack_validator → merge`) co-changes
  tightly. Do not interleave WP02 with parallel edits to these surfaces.
- **A skipped DRG regen reds the freshness/parity gate.** You MUST run
  `regenerate-graph` and commit `graph.yaml` after the kind-map/binding change.
  Do not hand-edit `graph.yaml` (it is generated) and do not suppress a parity
  finding — resync instead.
- **Do NOT create a second selection authority** (C-001). Activation stays on the
  owning step-contract node via the existing `filter_graph_by_activation`
  machinery; do not add a parallel gate-enablement registry or make
  `gate-handler`/`asset` URNs directly activatable.
- **Do NOT touch the WP01 owned files** (`step_contracts.py`, `models.py`) beyond
  what WP01 shipped — the schema is WP01's. WP02 consumes it.
- **FR-013 boundary**: bind the gate on **only** the pre-review (`implement`
  `status_transition`) contract; do not add bindings to the other built-in
  contracts.
- If you edit any kind-keyed dict, keep `test_kind_mapping_totality.py` green
  (totality or explicit `.get`-defaulted-partial exemption) — do not silently
  create a partial table.
- `src/doctrine` still must not import `specify_cli` if you touch anything under
  it (`test_layer_rules.py:244`).

## References (file:line anchors — verified in this repo)

- `src/charter/drg.py:187` — `_SINGULAR_TO_PLURAL` (**already** contains
  `mission_step_contract`); `:202` `_SINGULAR_TO_PER_KIND_FIELD`; `:217`
  `_MISSION_STEP_SINGULAR_KINDS`; `:233` `_owning_mission_type`.
- `src/doctrine/missions/built_in_step_contracts/implement.step-contract.yaml` —
  `status_transition` step (`command: spec-kitty agent tasks move-task {wp_id}
  --to for_review`) is where the `for_review` gate binds.
- `src/specify_cli/cli/commands/doctrine.py:200` — `regenerate-graph` command
  (`--check` = freshness gate, FR-009); writes `src/doctrine/graph.yaml`.
- `tests/specify_cli/cli/commands/test_doctrine_regenerate_graph.py` — the
  deterministic-regen / freshness gate test.
- `tests/doctrine/test_activation_parity_guard.py` +
  `src/charter/consistency_check.py` — fail-closed config↔DRG / config↔references
  parity guard (`run_consistency_check`).
- `tests/doctrine/drg/test_kind_mapping_totality.py` — totality guard for
  kind-keyed module dicts (bites if you add/omit a kind-map entry incorrectly).
- `.kittify/charter/references.yaml` — synthesized references (regen via charter
  synthesize if the change touches resolved references).
- `src/specify_cli/upgrade/migrations/` (`m_unify_charter_activation.py` naming
  pattern) — where a project-layer migration lands if one is warranted; use the
  config-aware `get_agent_dirs_for_project` helper.
- `research.md §0` / `§2` and `spec.md` FR-006 / FR-016 / C-006 — the activatable
  unit is the owning step-contract node; `gate-handler`/`asset` URNs default-allow.
