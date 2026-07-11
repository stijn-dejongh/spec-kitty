# Tasks: Doctrine-Controlled Transition Gates

**Mission**: doctrine-controlled-gates-01KX81KR · **Epic**: #2535 · **Branch**: `design/doctrine-controlled-gates`
**Inputs**: [spec.md](./spec.md) · [plan.md](./plan.md) (9-IC map + lane sketch) · [research.md](./research.md) (§0 SSOT selection seam) · [contracts/](./contracts/)

14 work packages across 5 dependency-ordered lanes. The SSOT **selection** seam (WP03) is the keystone both consumers depend on; reduction stays per gate-class. Path-B (WP09-12) ships **refuse-unconfinable v1** containment (RD-006). Only the pre-review **test-gate** is migrated (exemplar, FR-013).

## Lane / dependency overview

- **A — charter spine (serial, migration-first)**: WP01 → WP02
- **B — selection seam + reducer**: WP03 → WP04, WP05
- **C — Path-A (serial)**: WP06 → ; WP07 → WP08
- **D — Path-B**: WP09 → WP10 → WP11 → WP12
- **E — consumer inversions**: WP13 (needs WP06/WP08/WP03/WP04), WP14 (needs WP03/WP04; **coord #2531**)

Cross-lane deps: WP01→{WP03,WP09,WP02}; WP03→{WP04,WP05,WP07,WP10,WP13,WP14}; WP02→WP08; WP07→WP08; WP06→WP13; WP08→WP13; WP04→{WP13,WP14}; WP09→WP10→WP11→WP12. DAG is acyclic.

## Subtask Index

| ID | Description | WP | Parallel |
|----|-------------|----|----------|
| T001 | Add `GateBinding` model (`transition`, `gate_ref`, `mechanism: handler\|asset`, `on_unrunnable`) in `src/doctrine` | WP01 | — |
| T002 | Add optional `gate` binding field to `MissionStepContractStep` + unified `MissionStep` (versioned; `extra="forbid"` backward-compatible) | WP01 | — |
| T003 | Red-first: a pre-mission built-in step contract (no `gate`) still loads (FR-016/SC-009) | WP01 | — |
| T004 | Red-first: new `gate` field validates + round-trips | WP01 | — |
| T005 | Confirm `src/doctrine` has zero `specify_cli` imports (arch gate stays green) | WP01 | — |
| T006 | Extend `_SINGULAR_TO_PLURAL` (`src/charter/drg.py:187`) so step-contract-node activation is not a silent default-allow (FR-006) | WP02 | — |
| T007 | Add the `gate` binding to the pre-review built-in step contract (`transition: for_review`) | WP02 | — |
| T008 | Regenerate DRG (`graph.yaml`/`references.yaml`); freshness + `test_activation_parity_guard` green | WP02 | — |
| T009 | Migrate gate-declaring built-in `*.step-contract.yaml` (only those, not all 17) | WP02 | — |
| T010 | Red-first: activation on a step-contract node gates its bound gate (inactive doctrine → not selected) | WP02 | — |
| T011 | New `review/gates/resolver.py`: `resolve_gates(mission, transition, activation)` reading bindings by `binding.transition` (lane→transition adapter; NOT `get_by_action("for_review")`) | WP03 | — |
| T012 | Apply charter activation on the owning step-contract node; return ordered `ResolvedGate{binding,declaring_doctrine,dispatch,activation_state}` | WP03 | — |
| T013 | Define the handler/asset **dispatch Protocol** (implemented later by WP08/WP10) | WP03 | — |
| T014 | Characterization tests on the current `(mission, action)` selection matrix (extract-then-inject baseline) | WP03 | — |
| T015 | Contract tests: determinism; `[]`→CALM_NOTICE (empty≠clean); single selection call site | WP03 | — |
| T016 | New `review/gates/outcomes.py`: FR-014 verdict→operator-outcome reducer (test/verdict gates) | WP04 | — |
| T017 | `run_gate` folds every fault class → non-blocking outcome; only valid `regression(blocking)` BLOCKs | WP04 | — |
| T018 | Dedicated size-capped schema-validated verdict read (stray stdout can't forge — FR-019) | WP04 | — |
| T019 | Table-driven test over the full FR-014 mapping | WP04 | — |
| T020 | Fault-injection tests: crash/non-zero/timeout/malformed/absent verdict → FAULT_WARN (SC-005) | WP04 | — |
| T021 | New `review/gates/observe.py`: which gates active for a transition, declaring doctrine, why ran/didn't | WP05 | ∥ WP04 |
| T022 | Expose via a read-only surface (no heavy new CLI; reads the resolver) | WP05 | ∥ WP04 |
| T023 | Test SC-008 (observability answers active/inactive/refused/faulted) | WP05 | ∥ WP04 |
| T024 | Extract the pre-review hook block (`tasks_move_task.py:690-1051` + `_PRE_REVIEW_*`/`_mt_pre_review_*`) → new `pre_review_hook.py` (behavior-preserving) | WP06 | — |
| T025 | Preserve fail-open scaffolding VERBATIM (`_mt_empty_scope_verdict`, broad `except`, `_mt` catch) — it IS the FR-010 contract | WP06 | — |
| T026 | Re-point the `tasks.py:427-448` re-export shim | WP06 | — |
| T027 | Golden characterization tests prove move-task behavior unchanged by the extraction | WP06 | — |
| T028 | ruff/mypy clean on the extracted module (no new complexity over 15) | WP06 | — |
| T029 | New `review/gates/scope_source.py`: `ScopeSource` protocol (`derive(changed_files)->Scope`) | WP07 | — |
| T030 | Move `_SRC_PACKAGE_PREFIX`/`_gate_coverage` census into a **built-in** ScopeSource (active only when spec-kitty doctrine active — FR-012) | WP07 | — |
| T031 | `derive_test_scope` extraction stays ≤ C(15) | WP07 | — |
| T032 | Test: non-pytest fixture with no declared ScopeSource → the built-in is not force-applied (FR-009) | WP07 | — |
| T033 | New `review/gates/handlers/pre_review.py`: Path-A handler implementing the dispatch Protocol (no opt-in, no doctrine code) | WP08 | — |
| T034 | Reuse `evaluate_with_scope` (`pre_review_gate.py:451-511`) unchanged; preserve `review.fail_on_pre_review_regression`/`review.test_command` semantics (FR-017) | WP08 | — |
| T035 | Register the Path-A handler under the binding's `gate_ref` in the handler registry (the `transition: for_review` binding yaml is authored by WP02·T007 — no yaml edit here); **remove** the hardcoded spec-kitty-shaped decision path (C-004, no fallback tail) | WP08 | — |
| T036 | Red-first parity: migrated handler == prior hardcoded verdict on the same change set (NFR-001/SC-003) | WP08 | — |
| T037 | ruff/mypy clean; no `# noqa`/`# type: ignore` added | WP08 | — |
| T038 | Extend `AssetManifest` (`assets/models.py`) with the executable gate-asset shape (`entrypoint`, `interpreter`, `verdict_channel`) + `TrustEnvelope` protocol | WP09 | — |
| T039 | `pack_validator._validate_asset_manifests`: gate-asset-shape detection that keys code-exec (non-gate assets stay inert — C-003) | WP09 | — |
| T040 | Red-first: a plain `*.asset.yaml` is NOT treated as executable | WP09 | — |
| T041 | Red-first: an executable gate-asset shape validates | WP09 | — |
| T042 | New `assets/repository.py` + `assets/resolver.py`: URN→path resolution for a gate asset | WP10 | — |
| T043 | New `assets/runner.py`: invoke the entrypoint, implement the dispatch Protocol, return a `GateVerdict` | WP10 | — |
| T044 | **Provenance fix**: stop the loader overwriting `source_kind` (`org_pack_loader.py:403`) so `built_in\|org_pack\|third_party` is derivable/refusable (C-008) | WP10 | — |
| T045 | Red-first: a resolved gate asset runs and returns a structured verdict on the dedicated channel | WP10 | — |
| T046 | Red-first: a genuine `third_party`-provenance asset is now producible (feeds WP12 refusal test) | WP10 | — |
| T047 | New `assets/trust.py` (RD-006 v1): **env allowlist** (never `dict(os.environ)`); interpreter allowlist/no-shell | WP11 | — |
| T048 | **Process-group kill** on timeout (grandchildren) + `setrlimit` CPU/mem/output caps | WP11 | — |
| T049 | **Path-resolved (symlink-safe) fs write confinement**; **capability probe** → REFUSE (never run unconfined) | WP11 | — |
| T050 | Opt-in flag `review.allow_executable_gate_assets` (default off); wire the envelope into the runner | WP11 | — |
| T051 | Red-first: flag off / non-allowlisted provenance → TRUST_REFUSAL, not executed (NFR-004a/b) | WP11 | — |
| T052 | Containment tests: out-of-tree write blocked → FAULT_WARN; unconfinable host → refuse (SC-007) | WP12 | — |
| T053 | Timeout kills the process group (no orphaned grandchild); rlimit breach terminates (NFR-006) | WP12 | — |
| T054 | Verdict-channel forgery test: fake stdout verdict → FAULT_WARN (FR-019/SC-011) | WP12 | — |
| T055 | **Extend `tests/architectural/untrusted_path_audit/`** to cover the new code-exec sink (C-007; fails if a new unaudited exec path appears) | WP12 | — |
| T056 | Invert the extracted pre-review hook to resolve through `resolve_gates` (single owner of the inversion) | WP13 | — |
| T057 | Wire Path-A handler dispatch + FR-014 reducer at the move-task boundary; preserve fail-open | WP13 | — |
| T058 | Build the **consumer-shaped fixture** (non-pytest, no `_gate_coverage.py`) — SC-001/SC-002/NFR-002 | WP13 | — |
| T059 | Red-first: consumer fixture crossing `for_review` → CALM_NOTICE, zero internal-module leakage (#2534 closed) | WP13 | — |
| T060 | Invert `_check_composed_action_guard` **selection** onto `resolve_gates` (OWN WP; `runtime_bridge.py` exclusive; **coord #2531**) | WP14 | — |
| T061 | Keep its **fail-closed** reduction — missing spec/plan/tasks still hard-blocks (NOT routed through FR-014 — SC-010) | WP14 | — |
| T062 | Characterization tests on the `(mission, action)` guard matrix before inversion; behavior unchanged after | WP14 | — |
| T063 | NFR-005/SC-004 proof: adding a gate is a doctrine-only edit; **both** consumers now select through the one seam | WP14 | — |

## Work Packages

### WP01 — Gate-binding model + step-contract schema *(Lane A, foundational)*
- **owned_files**: `src/doctrine/missions/step_contracts.py`, `src/doctrine/missions/models.py`
- **dependencies**: none · **requirement_refs**: FR-001, FR-016, C-006 · **acceptance**: SC-009
- **safeguards**: `src/doctrine` MUST NOT import `specify_cli`; `extra="forbid"` backward compatibility (old contracts load).
- [ ] T001 · [ ] T002 · [ ] T003 · [ ] T004 · [ ] T005

### WP02 — Kind-map + DRG regen + built-in migration *(Lane A)*
- **owned_files**: `src/charter/drg.py`, the gate-declaring built-in `*.step-contract.yaml`, generated `graph.yaml`/`references.yaml`, migration module
- **dependencies**: WP01 · **requirement_refs**: FR-006, FR-016 · **acceptance**: SC-009
- **safeguards**: migration-first within the charter spine (one lane, no parallel); a skipped DRG regen fails the freshness/parity gate.
- [ ] T006 · [ ] T007 · [ ] T008 · [ ] T009 · [ ] T010

### WP03 — SSOT gate-*selection* seam (keystone) *(Lane B)*
- **owned_files**: `src/specify_cli/review/gates/resolver.py`, `src/specify_cli/review/gates/__init__.py`
- **dependencies**: WP01 · **requirement_refs**: FR-002, FR-003, FR-006, C-001, C-005 · **acceptance**: NFR-005 (proven in WP14)
- **safeguards**: selection ONLY (reduction is WP04 / per gate-class); the resolver imports `GateBinding` from `src/doctrine`; extract-then-inject (characterization first).
- [ ] T011 · [ ] T012 · [ ] T013 · [ ] T014 · [ ] T015

### WP04 — Test-gate reducer + FR-014 outcomes *(Lane B; IC-08 folded)*
- **owned_files**: `src/specify_cli/review/gates/outcomes.py`
- **dependencies**: WP03 · **requirement_refs**: FR-010, FR-014, FR-019, C-002 · **acceptance**: SC-005, SC-011
- **safeguards**: only a valid `regression(blocking)` may BLOCK; a crashed/timed-out/malformed gate is FAULT_WARN, never BLOCK.
- [ ] T016 · [ ] T017 · [ ] T018 · [ ] T019 · [ ] T020

### WP05 — Observability surface *(Lane B tail)*
- **owned_files**: `src/specify_cli/review/gates/observe.py`, `src/specify_cli/cli/commands/agent/gates_status.py`
- **dependencies**: WP03 · **requirement_refs**: FR-018 · **acceptance**: SC-008
- **safeguards**: read-only over the resolver; no heavy new CLI; loopback/local only.
- [ ] T021 · [ ] T022 · [ ] T023

### WP06 — Tidy-first: extract the pre-review hook *(Lane C, first)*
- **owned_files**: `src/specify_cli/cli/commands/agent/pre_review_hook.py`, `src/specify_cli/cli/commands/agent/tasks_move_task.py`, `src/specify_cli/cli/commands/agent/tasks.py`
- **dependencies**: none · **requirement_refs**: FR-010 (preserve) · **acceptance**: behavior-preserving (golden)
- **safeguards**: preserve fail-open scaffolding VERBATIM; broader `tasks_move_task` degod is OUT (#2116-closed → #2531); do NOT invert onto the seam here (that is WP13).
- [ ] T024 · [ ] T025 · [ ] T026 · [ ] T027 · [ ] T028

### WP07 — ScopeSource abstraction + built-in spec-kitty ScopeSource *(Lane C)*
- **owned_files**: `src/specify_cli/review/gates/scope_source.py`, `src/specify_cli/review/pre_review_gate.py`
- **dependencies**: WP03 · **requirement_refs**: FR-009, FR-012 · **acceptance**: NFR-002
- **safeguards**: `derive_test_scope` stays ≤ C(15); the spec-kitty census is a built-in ScopeSource active only under spec-kitty's own doctrine.
- [ ] T029 · [ ] T030 · [ ] T031 · [ ] T032

### WP08 — Pre-review Path-A handler (exemplar migration) *(Lane C)*
- **owned_files**: `src/specify_cli/review/gates/handlers/pre_review.py`, `src/specify_cli/review/pre_review_gate.py` *(the `transition: for_review` binding yaml is owned by WP02·T007 — WP08 is code-only)*
- **dependencies**: WP03, WP02, WP07 · **requirement_refs**: FR-011, FR-017 · **acceptance**: NFR-001, SC-003
- **safeguards**: no opt-in / no doctrine code (Path A); **remove** the hardcoded decision path (C-004 — no legacy fallback); reuse `evaluate_with_scope` unchanged.
- [ ] T033 · [ ] T034 · [ ] T035 · [ ] T036 · [ ] T037

### WP09 — Executable ASSET schema + validator *(Lane D)*
- **owned_files**: `src/doctrine/assets/models.py`, `src/specify_cli/doctrine/pack_validator.py`
- **dependencies**: WP01 · **requirement_refs**: FR-004, FR-005, C-003 · **acceptance**: (feeds SC-006/007)
- **safeguards**: EXTEND the existing manifest (not greenfield); code-exec keyed on the gate-asset shape — plain assets stay inert.
- [ ] T038 · [ ] T039 · [ ] T040 · [ ] T041

### WP10 — Asset repository + resolver + runner + provenance fix *(Lane D)*
- **owned_files**: `src/doctrine/assets/repository.py`, `src/doctrine/assets/resolver.py`, `src/doctrine/assets/runner.py`, `src/doctrine/assets/entrypoint.py`, `src/doctrine/drg/org_pack_loader.py`
- **dependencies**: WP03, WP09 · **requirement_refs**: FR-004, FR-005, C-008 · **acceptance**: SC-012
- **safeguards**: runner implements the WP03 dispatch Protocol; the `source_kind` fix must not break existing pack-load callers.
- [ ] T042 · [ ] T043 · [ ] T044 · [ ] T045 · [ ] T046

### WP11 — Trust envelope v1 (refuse-unconfinable) *(Lane D)*
- **owned_files**: `src/doctrine/assets/trust.py`, `.kittify/config.yaml` schema (opt-in flag surface)
- **dependencies**: WP10 · **requirement_refs**: FR-007, FR-015, FR-019, RD-006 · **acceptance**: NFR-004a/b
- **safeguards**: never `dict(os.environ)`; refuse-if-unconfinable (never run unconfined); NO new sandbox dependency; deeper OS isolation deferred (#2541).
- [ ] T047 · [ ] T048 · [ ] T049 · [ ] T050 · [ ] T051

### WP12 — Trust/containment tests + audit-harness extension *(Lane D)*
- **owned_files**: `tests/doctrine/assets/` (trust tests), `tests/architectural/untrusted_path_audit/`
- **dependencies**: WP11 · **requirement_refs**: C-007 · **acceptance**: NFR-006, SC-006, SC-007, SC-011, SC-012
- **safeguards**: the audit harness is a static scanner — do NOT conflate it with runtime containment proof; both are required.
- [ ] T052 · [ ] T053 · [ ] T054 · [ ] T055

### WP13 — Move-task pre-review inversion + consumer fixture *(Lane E)*
- **owned_files**: `src/specify_cli/cli/commands/agent/pre_review_hook.py`, `tests/integration/gates/` (consumer fixture)
- **dependencies**: WP06, WP08, WP03, WP04 · **requirement_refs**: FR-002, FR-011 · **acceptance**: SC-001, SC-002, NFR-002
- **safeguards**: SOLE owner of the hook inversion (WP06 only extracts); preserve fail-open.
- [ ] T056 · [ ] T057 · [ ] T058 · [ ] T059

### WP14 — F(48) composed-action guard selection-inversion *(Lane E; coord #2531)*
- **owned_files**: `src/runtime/next/runtime_bridge.py`
- **dependencies**: WP03, WP04 · **requirement_refs**: FR-002, C-002 · **acceptance**: NFR-005, SC-004, SC-010
- **safeguards**: `runtime_bridge.py` EXCLUSIVE — **coordinate with #2531** (concurrent decomposition); keep the guard **fail-closed** (selection-only inversion; do NOT route through the FR-014 reducer — SC-010); characterization tests before + after.
- [ ] T060 · [ ] T061 · [ ] T062 · [ ] T063
