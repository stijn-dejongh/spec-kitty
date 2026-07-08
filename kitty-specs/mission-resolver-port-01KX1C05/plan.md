# Implementation Plan: MissionResolver Port (2173 Phase 2)

**Branch**: `feat/mission-resolver-port-2173` | **Date**: 2026-07-08 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `kitty-specs/mission-resolver-port-01KX1C05/spec.md`

## Summary

Introduce one injectable `MissionResolver` seam (Protocol + `FsMissionResolver` real adapter +
`FakeMissionResolver` stub) in front of the single `kitty-specs/` enumeration walk, injected at the
`mission_runtime/resolution.py` shell — never on the frozen `MissionExecutionContext` — so the
execution-context builder becomes FS-free-testable (the `#1619` unblock). Ship an ADR + a new AST
call-site gate to bind the seam by construction, and finish three same-surface strangler residuals in
sibling slices: the `#2139` `target_branch` reader reconcile, the Clock helper consolidation, and the
InstalledVersion routing + `#2447` doctrine-phantom fix. Technical approach and scope are grounded by a
3-lens pre-spec squad; see `research.md` and the `tracer-*.md` files.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: standard library only (`pathlib`, `dataclasses`, `typing.Protocol`); existing
first-party packages `specify_cli` (owns `context/mission_resolver.py`, the walk) and `mission_runtime`
(owns the resolution shell + frozen context). No new runtime dependencies.
**Storage**: Filesystem — `kitty-specs/<mission>/meta.json` reads. This FS coupling is precisely what the
port abstracts; the `FakeMissionResolver` replaces it in tests.
**Testing**: `pytest`. New **FS-free** builder unit tests via `FakeMissionResolver` (NFR-001); the full
`tests/architectural/` ratchet suite (NFR-002); a byte-identical timestamp characterization test
(NFR-004); structured-error tests for cold-miss/ambiguity (NFR-005). ATDD-first: the FS-free builder
test is written red before the seam exists.
**Target Platform**: Linux / macOS developer + CI runners (the Spec Kitty CLI).
**Project Type**: single (Python CLI + library).
**Performance Goals**: none — Phase-2 ships the walk **uncached** by design (C-005); wall-clock behavior
is unchanged.
**Constraints**: `ruff` + `mypy` zero new issues; cyclomatic complexity ≤ 15 on touched/extracted
functions; no new dependencies; ports on the shell never on the frozen context; no process-level cache;
fail-closed-loud with no legacy `is None`/`or slug` branch (ADR `2026-07-01-1`).
**Scale/Scope**: one new port module (Protocol + 2 adapters) co-located with the existing walk; reroute
~2 shell identity sites + 2 resolve-by-identity consumers; `#2139` = 4 straggler readers; Clock ≈ 16
helpers → 3; 1 migration version read; 1 doctrine row + 1 path-resolution guard; 1 new ADR; 1 new AST
arch-gate.

## Charter Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Charter loaded (`spec-kitty charter context --action plan`; `software-dev-default`, DIR-001…DIR-013).
Relevant governing principles and their disposition:

| Principle / Directive | Disposition |
|---|---|
| **Single canonical authority** | ✅ **This mission embodies it** — one `MissionResolver` becomes the sole sanctioned `kitty-specs/` walker, enforced by a new AST gate (FR-007). |
| **Architectural alignment / adopt-don't-duplicate** | ✅ Reuses `PlacementSeam`, the canonicalizer, `resolve_mid8`, and the shipped `x or Default()` DI idiom (`RuntimeEventEmitter`/`NullEmitter`); no new framework. |
| **DDD + tiered rigour** | ✅ Core seam (resolver + shell) gets full rigour + FS-free unit tests; glue (doc tail) gets proportionate treatment. |
| **ATDD-first / red-first** | ✅ FR-004/NFR-001 FS-free builder test authored red first through the pre-existing builder entry point. |
| **No legacy resolver paths** (ADR `2026-07-01-1`) | ✅ Cold-miss fail-closed-loud → `backfill-identity`; forbidden `is None`/`or slug` branch explicitly barred (FR-005). |
| **Blind-primitive non-fold rule** (ADR `2026-06-26-1`) | ✅ Resolver sits at the shell in front of `primary_feature_dir_for_mission`; canonicalization is not folded into the primitive (C-007). |
| **Terminology canon** | ✅ Mission (not feature) throughout; doc tail touches shipped doctrine → run the terminology guard pre-push. |

**No charter violations.** Complexity Tracking table below is empty.

## Project Structure

### Documentation (this mission)

```
kitty-specs/mission-resolver-port-01KX1C05/
├── plan.md              # This file
├── research.md          # Phase 0 output — squad grounding + Q1/Q2 resolutions
├── data-model.md        # Phase 1 output — port interface + value objects
├── quickstart.md        # Phase 1 output — how to use FakeMissionResolver in a builder test
├── contracts/           # Phase 1 output — MissionResolver Protocol contract
├── tracer-approach.md           # WP sketch + adopt-don't-duplicate map
├── tracer-design-decisions.md   # D1–D8 + Q1/Q2 resolutions
└── tracer-tooling-friction.md   # F1–F7 friction watch-list
```

### Source Code (repository root)

```
src/specify_cli/context/
└── mission_resolver.py          # HOME of the port: resolve_mission, ResolvedMission, _build_index
                                 #   ADD: MissionResolver (Protocol), FsMissionResolver, FakeMissionResolver

src/mission_runtime/
└── resolution.py                # SHELL: _assemble_core_fragments / _resolve_mission_id (:913) /
                                 #   _resolve_mission_slug (:303) — inject resolver=None here

src/specify_cli/                 # sibling-slice touch points:
├── core/paths.py                # read_target_branch_from_meta (the #2139 authority) — unchanged
├── context/resolver.py          # #2139 straggler :82
├── retrospective/generator.py   # #2139 straggler :1263
├── cli/commands/agent/mission_branch_context.py  # #2139 straggler :63
├── missions/_resolve_planning_branch.py          # #2139 straggler :80
├── <12 modules>                 # Clock: 12 isoformat _now_utc copies → one canonical helper
├── task_utils/support.py, cli/commands/agent/mission_parsing.py  # Clock: preserve 2 stamp callers
├── decisions/emit.py, decisions/service.py        # Clock: preserve 2 ->datetime callers
├── upgrade/migrations/m_2_1_4_enforce_command_file_state.py  # InstalledVersion → _CliStatusLike
└── doctrine_synthesizer/apply.py, core/vcs/detection.py       # adopt 2 resolve-by-identity consumers

docs/adr/3.x/
└── 2026-07-08-*-mission-resolver-port.md   # NEW ADR (FR-006)

tests/architectural/
└── test_mission_resolver_walker_gate.py    # NEW AST call-site gate (FR-007)

src/doctrine/skills/spec-kitty-git-workflow/references/
└── git-operations-matrix.md                # #2447 phantom row repoint + path-resolution guard
```

**Structure Decision**: Single Python project. The port lands in
`src/specify_cli/context/mission_resolver.py` co-located with the existing walk / `ResolvedMission` /
error taxonomy (**Q2 resolved**, see research.md); the `mission_runtime` shell imports it (the
`mission_runtime → specify_cli` direction is already established at `resolution.py:327/344/…`). This
avoids fragmenting the seam and sidesteps the `mission_runtime` external-import gate for the Fake, which
tests and CLI code must import freely.

## Complexity Tracking

*No Charter Check violations — table intentionally empty.*

## Implementation Concern Map

> Implementation concerns are NOT work packages. `/spec-kitty.tasks` translates these into executable
> WPs (one IC may become several WPs; small ICs may merge).

### IC-01 — Resolver seam + builder unblock

- **Purpose**: Put a `Protocol` + `FsMissionResolver` + `FakeMissionResolver` on the single walk and inject it at the shell so the execution-context builder is FS-free-testable.
- **Relevant requirements**: FR-001, FR-002, FR-003, FR-004, FR-005; NFR-001, NFR-005.
- **Affected surfaces**: `context/mission_resolver.py` (add port + adapters), `mission_runtime/resolution.py` (`_resolve_mission_id` :913, `_resolve_mission_slug` :303, `_assemble_core_fragments`), plus the 2 adopted consumers `doctrine_synthesizer/apply.py:602/788`, `core/vcs/detection.py:169`.
- **Sequencing/depends-on**: none (foundational).
- **Risks**: must not touch `build_execution_context` (pure door) or the frozen context (C-006); resolver stays request-scoped, no cache (C-005); cold-miss fail-closed (FR-005). Anti-fold surfaces (`identity_audit.py`, `merge/ordering.py`, `core/paths.py:816/835`) must be left alone (C-001..C-003).

### IC-02 — ADR + AST call-site gate (bind by construction)

- **Purpose**: Record the seam decision and make "one sanctioned walker" structural, not reviewer-enforced.
- **Relevant requirements**: FR-006, FR-007; NFR-002.
- **Affected surfaces**: `docs/adr/3.x/…`, `tests/architectural/test_mission_resolver_walker_gate.py` (token-keyed allowlist for legacy walkers strangled incrementally).
- **Sequencing/depends-on**: follows IC-01 (the blessed owner must exist before the gate names it).
- **Risks**: allowlist must be token-keyed not line-numbered (F5); the gate must derive its scan scope from `src/` so it can't drift blind.

### IC-03 — `#2139` target_branch reconcile (sibling)

- **Purpose**: Route 4 straggler readers onto `read_target_branch_from_meta`; delete divergent `"main"`/`""`/`KeyError` defaults so all readers share one fail-closed behavior.
- **Relevant requirements**: FR-008.
- **Affected surfaces**: `context/resolver.py:82`, `retrospective/generator.py:1263`, `mission_branch_context.py:63`, `missions/_resolve_planning_branch.py:80`.
- **Sequencing/depends-on**: independent of IC-01 (reuses an existing authority; NOT a resolver method).
- **Risks**: reconcile 3 different absent-value contracts before routing — whack-a-field regression if done piecemeal.

### IC-04 — Clock consolidation

- **Purpose**: Collapse the 12 byte-identical isoformat `_now_utc` copies into one helper; preserve the 2 `%Y-%m-%dT%H:%M:%SZ` stamp callers and the 2 `-> datetime` callers as distinct helpers.
- **Relevant requirements**: FR-009; NFR-004.
- **Affected surfaces**: ~12 modules (isoformat copies) + `task_utils/support.py:101`, `mission_parsing.py:257` (stamp) + `decisions/emit.py:64`, `decisions/service.py:86` (datetime).
- **Sequencing/depends-on**: independent.
- **Risks**: folding the stamp/datetime callers would change on-disk serialization (NFR-004) — must stay 3 helpers; inject a Clock port only at determinism-tested sites (no broad injection).

### IC-05 — InstalledVersion routing + `#2447` doc tail

- **Purpose**: Route the migration version read through the existing `_CliStatusLike` Protocol; repoint/remove the phantom doctrine row and add a path-resolution guard.
- **Relevant requirements**: FR-010, FR-011.
- **Affected surfaces**: `upgrade/migrations/m_2_1_4_enforce_command_file_state.py:55`; `git-operations-matrix.md:28` + a new guard that every `src/…` path in the matrix resolves on disk.
- **Sequencing/depends-on**: independent.
- **Risks**: doctrine is a shipped artifact — run the terminology guard + `tests/architectural/` locally before push (F7).
