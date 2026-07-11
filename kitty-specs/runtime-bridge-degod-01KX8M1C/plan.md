# Implementation Plan: Runtime-Bridge God-Module Decomposition

**Branch**: `design/runtime-bridge-degod` | **Date**: 2026-07-11 | **Spec**: [spec.md](./spec.md)
**Input**: [spec.md](./spec.md) · **Research (FR-002 gate)**: [research.md](./research.md) — seam boundaries, parity contract, fixture matrix, compat strategy are FIXED there.

## Summary

Decompose the 3,813-LOC `src/runtime/next/runtime_bridge.py` into **6 flat
responsibility-named seam modules + a thin residual** (per the #2464 sibling),
via **Ports+cores** (#2173). It is a **behavior-preserving** refactor guarded by
two safety nets built first: a `decide_next()` **parity characterization oracle**
(normalization contract from research §Parity) and a **compat-surface guard** for
the 50-symbol monkeypatch surface (research §Compat). Extraction proceeds in the
coupling-ordered sequence with the hot identity/coord port cut last.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: existing `src/runtime/next/` (`_internal_runtime` engine, `decision.py`); the #2464 `workflow.py` decomposition as the layout/`DecideNextContext`/lazy-accessor template; `pytest` (characterization + compat guards); `ruff --select C901` + radon (complexity gate)
**Storage**: N/A — refactor; `meta.json` / `feature-runs.json` / `tasks.md` are read through the extracted ports, not changed
**Testing**: `pytest` — WP-0 parity oracle (masked, frozen-snapshot), the compat-surface guard (behavioral sentinel + static AST anti-shadowing), per-seam unit tests (pure cores in isolation; ports/adapter against stubs), and the full `runtime/next` suite staying green
**Target Platform**: Linux/macOS CLI library
**Project Type**: single
**Performance Goals**: no measurable `decide_next()` latency regression from added indirection (NFR-006)
**Constraints**: behavior-preserving (C-001); every function ≤15 with zero `# noqa: C901` (NFR-002); no new public surface (NFR-004); preserve the `runtime.next.runtime_bridge` import path + the 50-symbol private patch surface (FR-012); no new import cycle (C-007)
**Scale/Scope**: 9 WPs; one 3,813-LOC module → 6 seam modules (`runtime_bridge_{engine,cores,io,composition,retrospective,identity}.py`) + a thin residual (~35–40% per the #2464 precedent; exact target confirmed in research)

## Charter Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Single canonical authority** ✅ — one engine-adapter owns all `_internal_runtime.engine` private access (FR-013); one Decision-builder collapses the 29 open-coded constructions (FR-011).
- **Architectural alignment** ✅ — Ports+cores per #2173; flat sibling-convention layout per #2464; import path preserved (C-003).
- **DDD + tiered rigour** ✅ — pure cores (tasks.md parse, `evaluate_guards`, Decision-builder) get high rigour + isolation unit tests; ports/adapter contract-tested against stubs.
- **ATDD-first** ✅ — the WP-0 characterization lock (parity oracle + fixture ledger, proven green on unmodified source) precedes every extraction (C-004).
- **Campsite-first** ✅ — this mission *is* the campsite for the repo's largest god-module; no functional work rides along.
- **No legacy fallback** ✅ — behavior-preserving relocation, no compatibility branch on decision logic (C-001).

No violations → Complexity Tracking empty.

## Project Structure

### Documentation (this mission)
```
kitty-specs/runtime-bridge-degod-01KX8M1C/
├── plan.md · spec.md · research.md (FR-002 gate)
├── data-model.md            # new types: ArtifactPresenceSnapshot, DecisionEnvelope, DecideNextContext, port/adapter interfaces
├── contracts/
│   ├── parity-oracle.md      # the characterization safety net (normalization + fixtures + side-effect isolation)
│   └── compat-surface.md     # the 50-symbol monkeypatch preservation + guard test
├── quickstart.md            # maintainer workflow with the decomposed modules
└── tasks.md                 # /spec-kitty.tasks output
```

### Source Code (repository root)
```
src/runtime/next/
├── runtime_bridge.py            # THINNED residual: 4-phase decide_next_via_runtime, query/answer, DecideNextContext,
│                                #   guarded compat re-export block, __all__, #2531 pointer
├── runtime_bridge_engine.py     # NEW (FR-013): sole home of _internal_runtime.engine privates
├── runtime_bridge_cores.py      # NEW (pure): tasks.md parse; ArtifactPresenceSnapshot+evaluate_guards (FR-009); Decision-builder (FR-011)
├── runtime_bridge_io.py         # NEW (ports): feature-runs index, template discovery, run lifecycle, OC, gather_artifact_presence, resolve_commit_target
├── runtime_bridge_composition.py# NEW: dispatch + run-state advance + FR-008 selection seam
├── runtime_bridge_retrospective.py # NEW: learning-capture
├── runtime_bridge_identity.py   # NEW: hot identity/coord port (cut LAST)
└── decision.py                  # unchanged (its :428 lazy edge stays lazy — C-007)

tests/runtime/
├── test_bridge_parity.py        # WP-0 characterization oracle (masked, frozen snapshots)
├── test_bridge_compat_surface.py# WP-0 compat guard (behavioral sentinel + AST anti-shadowing)
└── test_bridge_<seam>.py        # per-seam unit tests
```

**Structure Decision**: Flat responsibility-named modules (not a `ports/`|`cores/` subdir), preserving the `runtime.next.runtime_bridge` import path used by ~13 prod + ~40 test sites.

## Complexity Tracking

*No Charter Check violations — section intentionally empty.*

## Implementation Concern Map

> Concerns follow the research §Seams coupling-ordered extraction sequence. This is a
> single-god-module refactor: nearly every WP edits `runtime_bridge.py` (moving symbols
> out), so the lanes are inherently a **serial spine** — the allocator will collapse
> them on the shared parent file. Value is the decomposition, not parallelism.

### IC-01 — Safety nets (WP-0, BLOCKING) — parity oracle + compat guard
- **Purpose**: Build both safety nets and prove them green on **unmodified** source before any extraction. The parity oracle implements research §Parity (masking contract + frozen-snapshot side-effect isolation + the 22–26 fixture ledger with the every-site/every-guard-branch coverage floor); the compat guard implements research §Compat (behavioral sentinel + static AST anti-shadowing over the 50 symbols).
- **Requirements**: FR-002, C-004; NFR-001; enables all. **Depends-on**: none (first).
- **Risks**: the whole mission's safety depends on this; if the oracle under-covers, extractions can silently drift. Coverage floor is binding.

### IC-02 — Engine-adapter (FR-013)
- **Purpose**: Extract `runtime_bridge_engine.py` as the sole home of the `_internal_runtime.engine` privates (`_read_snapshot`/`_load_frozen_template`/`plan_next`/`_append_event`/`_write_snapshot`; sites `:1840`/`:2606`/`:3261`/`:3416`/`:1800`). `_advance_run_state_after_composition` (duplicates the engine's `next_step` branch) is adapter-owned.
- **Requirements**: FR-013; FR-006. **Depends-on**: IC-01.
- **Risks**: engine-boundary correctness; arch guard that no core reaches engine internals.

### IC-03 — Retrospective seam
- **Purpose**: Extract `runtime_bridge_retrospective.py` (self-contained learning-capture cluster). Low-coupling, front-loads confidence.
- **Requirements**: FR-001, FR-006. **Depends-on**: IC-01.

### IC-04 — Clean I/O ports
- **Purpose**: Extract `runtime_bridge_io.py`: feature-runs index, template/pack discovery, run lifecycle, OC builder, the `gather_artifact_presence` fact-port (feeds FR-009), and the lifted pure `resolve_commit_target` (from `_wrap_with_decision_git_log:226–261`).
- **Requirements**: FR-001, FR-003, FR-006. **Depends-on**: IC-01. (60 lazy imports make these near-mechanical.)

### IC-05 — Pure cores + guard inversion (FR-009)
- **Purpose**: Extract `runtime_bridge_cores.py` pure leaves — tasks.md parse (`:343–473`) and the `ArtifactPresenceSnapshot`+`evaluate_guards(snapshot)` inversion collapsing both C901 guards. **Preserve the fail-closed default** (guard-failure list identical incl. order — SC-007).
- **Requirements**: FR-009, FR-004, NFR-003; SC-007. **Depends-on**: IC-01, IC-04 (the fact-port).
- **Risks**: the fail-closed defaults + `tasks` legacy-union are the highest-risk relocation fixtures.

### IC-06 — Decision-builder (FR-011)
- **Purpose**: `DecisionEnvelope`+`step_or_blocked` core collapsing the 29 open-coded `Decision(...)` sites + the 4× triad. The single highest CC lever.
- **Requirements**: FR-011, FR-004. **Depends-on**: IC-01.

### IC-07 — Composition dispatch + FR-008 selection seam
- **Purpose**: Extract `runtime_bridge_composition.py`: dispatch + run-state advance + the isolated `_should_dispatch_via_composition` **selection** seam (FR-008 — leave it clean for gates #2535 WP14; import no gates code).
- **Requirements**: FR-008, FR-004. **Depends-on**: IC-02 (engine-adapter), IC-06 (Decision-builder).

### IC-08 — `decide_next` phase-split (FR-010)
- **Purpose**: Rewrite the residual `decide_next_via_runtime` as a **bootstrap / dependency-gate / composition-dispatch / decision-materialize** early-return chain over the `DecideNextContext` dataclass; residual ≤15.
- **Requirements**: FR-010, FR-004, FR-005. **Depends-on**: IC-05, IC-06, IC-07.

### IC-09 — Identity/coord port (LAST)
- **Purpose**: Extract `runtime_bridge_identity.py` — the hottest fracture line (scars #2091/#1978/#1918/#1814/#2069; correctness path — malformed coord branch → `git worktree` exit-128). Cut last, behind the fattest golden coverage.
- **Requirements**: FR-001, FR-003. **Depends-on**: IC-01 … IC-08 (last).
- **Risks**: highest-regression seam; identity-trio compat symbols kept-in-place per research §Compat.

## Notes for /tasks

1. **WP-0 is a blocking gate** — no extraction WP starts until the parity oracle + compat guard are green on unmodified source (C-004/SC-008).
2. **Compat preservation is per-WP, not one-shot** — every extraction that moves a patched symbol must add the guarded re-export (and lazy-accessor for sibling-called names) + keep the compat guard green. KEEP-IN-PLACE `_wrap_with_decision_git_log` + `_advance_run_state_after_composition`.
3. **Serial spine** — WPs linearize on `runtime_bridge.py`; expect the allocator to collapse to ~1 lane. Do not fabricate parallelism.
4. Each WP re-runs the parity oracle (must stay green) — it is the extraction's acceptance gate, alongside the seam's own unit tests.
5. NFR-005 residual-LOC target is confirmed in research (~35–40%); assert it at IC-08/IC-09.
