# Research: Doctrine-Controlled Transition Gates

**Mission**: doctrine-controlled-gates-01KX81KR · **Epic**: #2535
**Sources**: grounding research squad (Op 01KX7YCK) + post-spec adversarial squad (Op 01KX8271).
Full lens reports in scratchpad: `research-{SYNTHESIS,A,B,C,D}-*.md`, `postspec-{1..4,SYNTHESIS}.md`.

---

## 0. The keystone: the SSOT gate-resolution seam (single entry point)

**This is the most important design constraint in the mission — the contract must be built around it.**

Today there are **two independent runtime consumers** that decide "does a check run on this transition," and they are wired completely separately:

1. **The `move-task` pre-review hook** — `_mt_run_pre_review_gate` in
   `src/specify_cli/cli/commands/agent/tasks_move_task.py:996`, gated by the
   literal `if st.target_lane != Lane.FOR_REVIEW: return` at `:1012`, calling
   `pre_review_gate.evaluate_*` and folding faults to `no_coverage` at `:905-909`.
2. **The composed-action post-task guard** — `_check_composed_action_guard` in
   `src/runtime/next/runtime_bridge.py:1515` — a hardcoded `if/elif` on
   `(mission, action)` at **radon complexity F(48)** (already `# noqa: C901`).

**Forensic finding (paula-patterns):** these two files have **never co-changed**
in history and have **independent test harnesses**. If the mission rewires them
separately to consult step-contract bindings, the two resolvers *will* drift —
one gets migrated, the other left hardcoded, or they diverge in fault handling.
**NFR-005 ("adding a gate is a doctrine-only edit") is unprovable** unless both
consumers resolve through the *same* code path.

**Design mandate → a single SSOT resolver seam (one injected port).** Introduce
**one** binding-resolution entry point — a `GatePorts`-style port — that:
- takes `(mission, transition/action, active-doctrine)` and returns the ordered
  set of active gate bindings for that transition (handler or asset targets);
- is the **only** place that reads step-contract bindings + applies charter
  activation (`filter_graph_by_activation`, `src/charter/drg.py:319`,
  predicate `:293-316`);
- both consumers above depend on it by injection — neither re-implements
  selection.

**Contract-design implications (for `contracts/` at plan):**
- The seam's **input contract** is `(mission_id, transition, activation_state)`;
  its **output contract** is a deterministic, ordered `list[ResolvedGate]` where
  each carries `{binding, mechanism: handler|asset, on_unrunnable_policy}`.
- The seam owns the **fail-open reduction boundary**: faults never escape as
  exceptions to the consumers; they are folded to the FR-014 outcome inside the
  seam (or a thin verdict-reducer it delegates to), so both consumers get
  identical fault semantics for free.
- The seam is **extract-then-inject**, never edit-in-place: extract the current
  selection logic behind the port with **characterization tests on the current
  `(mission, action)` matrix first**, then invert both consumers onto it. This
  de-risks the F(48) `runtime_bridge` edit (the single highest-regression site).
- The seam is its **own work package**, sequenced before either consumer's
  inversion — it is the contract both halves (Path-A handler dispatch, Path-B
  asset dispatch) plug into.

This single-entry-point seam is what makes the whole "doctrine-controlled"
claim *true and testable* rather than aspirational: one place selects, one place
reduces faults, one place both consumers trust.

---

## 1. Current gate substrate (grounding lens A — verified in post-spec)

- ~35 command-layer transition checks; **~a dozen** are literal `target_lane ==`
  compares, the rest are `policy.require_X` / composed-action `(mission, action)`
  guards. No data-driven registry maps transition → check-set. FSM entry-guards
  (`status/wp_state.py`) are separate, repo-agnostic, and out of scope.
- **#2534 locus** (verified): `review/pre_review_gate.py`
  `_SRC_PACKAGE_PREFIX="src/specify_cli/"` (:98), `_GATE_COVERAGE_MODULE_NAME=
  "tests.architectural._gate_coverage"` (:100), `GateAuthoritiesUnavailable`/
  `_load_gate_coverage_module` refuse-outside-repo_root (:112, :131-159), fold to
  `no_coverage` at `tasks_move_task.py:905-909`.
- **#2330 locus** (verified): hardcoded pytest/`--junitxml` runner
  `run_scoped_tests_at_head` (`pre_review_gate.py:358-423`, argv `:379-386`).
- **Reuse anchor**: `evaluate_with_scope` (`pre_review_gate.py:451-511`) is the
  already-extracted, tested verdict tail — the strangler reuses it (FR-011).
  `derive_test_scope` sits at the C(15) complexity ceiling — extraction behind a
  `ScopeSource` port must not push it over.
- **Fail-open scaffolding to preserve VERBATIM** (it *is* the FR-010 contract,
  not debt): `_mt_empty_scope_verdict` (`tasks_move_task.py:859`), the broad
  `except` at `:1035`, catch at `:905-909`.

## 2. Step-contract consultation model (grounding lens B — verified)

- Contracts **are** machine-loaded + DRG-resolved:
  `MissionStepContractRepository.get_by_action` (`charter/step_contracts.py:159-170`);
  the transition literally lives in `implement.step-contract.yaml:56-58`
  (`status_transition → move-task --to for_review`).
- BUT `StepContractExecutor` is **a composer, not a runner** — declared commands
  are rendered as LLM text ("declared only; the host/operator owns execution",
  `executor.py:372`) and never executed. `executor.py` is a **defect-magnet**
  (16/18 commits are fixes) → build a **new runner subsystem**, do not mutate the
  composer.
- **Seam**: add the gate-binding field to `MissionStepContractStep`
  (`step_contracts.py:65`) **and** the unified `doctrine.missions.models.MissionStep`;
  both are `extra="forbid"` → **versioned schema evolution + migration** (FR-016,
  C-006). The coupled charter spine (step_contracts→executor→drg→pack_validator→
  merge) co-changes tightly → **migration-first, one lane, no parallel**.

## 3. ASSET kind mechanics (grounding lens C — verified)

- ASSET is **inert today**: `AssetManifest{id, mime, path}` (identity-only,
  `src/doctrine/assets/models.py:27-53`); no loader, no resolver, no runner.
  Non-activatable by construction (`artifact_kinds.py:178-180`,
  `_NON_AUGMENTATION_ELIGIBLE_KINDS = {TEMPLATE, ASSET}`).
- Path B is therefore **greenfield**: asset repository + URN→path resolver +
  code-asset entrypoint contract + contained runner. Keep code execution keyed on
  the **gate-asset shape** so non-gate assets stay inert (C-003).
- **Reuse, don't reinvent, the safety precedents**: `run_scoped_tests_at_head`
  already does argv-vector / no-shell / timeout / env-scrub
  (`pre_review_gate.py:358`); `pack_validator._check_asset_path_containment` /
  `_check_asset_mime` (`:604-733`) + the `path_escape_pack` / `bad_mime_pack`
  fixtures; and the `tests/architectural/untrusted_path_audit/` harness —
  **which MUST be extended to cover the new code-exec sink or it goes stale-green**
  (C-007).

## 4. Target architecture + trust (grounding lens D + post-spec B1/B3)

- **Two mechanisms coexist (RD-005 full A+B):** Path-A **handlers** (spec-kitty-
  shipped, selected by doctrine, no opt-in, no doctrine code executed) AND Path-B
  **executable gate assets** (doctrine-supplied, default-off opt-in + containment).
  The exemplar pre-review migration is a **Path-A handler** so it runs on
  spec-kitty's own repo with no opt-in (parity, SC-003).
- **Trust envelope = real containment, not just an allowlist** (post-spec B3):
  interpreter allowlist + no-shell + timeout **plus** filesystem confinement (no
  out-of-tree writes), no network egress, memory/CPU/output-size limits;
  provenance **derived** from pack-load metadata (never self-declared); refuse
  (TRUST-REFUSAL) rather than run unconfined. Cryptographic/signature provenance
  deferred to #2536.
- **Canonical verdict→operator-outcome mapping** (post-spec B4, FR-014): BLOCK
  only on a valid emitted `regression(blocking=true)`; FAULT-WARN for any fault;
  CALM-NOTICE when nothing active; TRUST-REFUSAL when execution is refused; PASS
  otherwise. A crashed/timed-out/malformed-verdict gate is FAULT-WARN, **never**
  BLOCK (post-spec B5, C-002).

## 5. Sequencing evidence (CaaCS forensic — for WP decomposition)

Risk-ranked target surfaces and the couplings that constrain order:
1. **`runtime_bridge.py`** (3813 LOC, 30 bug-fixes) — `_check_composed_action_guard`
   F(48): highest regression risk → extract-then-inject via the §0 seam,
   characterization tests first.
2. **Charter spine** (step_contracts→executor→drg→pack_validator→merge) — C-006
   schema bump ripples across all five → migration-first, single lane.
3. **`executor.py`** defect-magnet → new runner, don't mutate the composer.
4. **ASSET runner + trust envelope** — greenfield + RCE-adjacent → extend
   `untrusted_path_audit`; reuse the argv/no-shell/timeout/env-scrub precedent.
5. **`pre_review_gate.py`** `derive_test_scope` at C(15) — ScopeSource extraction
   must not exceed the ceiling; well-covered for NFR-001 parity.

**Campsite (Tidy-First enabler, sequence FIRST):** extract the pre-review hook
block (`tasks_move_task.py:690-1051` — `_PRE_REVIEW_*` constants + ~15
`_mt_pre_review_*` helpers + the `_pre_review_gate_*` seams, and re-point the
`tasks.py:427-448` re-export shim) into a dedicated sibling module as a
behavior-preserving move, preserving the fail-open scaffolding verbatim. This
gives the §0 seam + handler/asset dispatch a clean isolated surface. Domain-
matched to #2116 (`WP-move_task-relocate`); golden-guarded by existing move-task
characterization tests. Broader `tasks_move_task` / `runtime_bridge` degod stays
OUT → #2116.
