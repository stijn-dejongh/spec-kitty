# Mission Specification: Sync CLI Degod — Wave 4

**Mission Branch**: `refactor/wave4-sync-degod`
**Created**: 2026-08-18
**Status**: Draft
**Input**: Wave-4 (CLI-split half) of the degod/unshim program. Decompose `cli/commands/sync.py` (6,332 LOC) into ports + pure cores + thin command shells and tidy `calibration/walker.py`, retiring the three `# noqa: C901` and clearing walker's `S1192` cluster — **with zero behavior change**, under the program's architectural invariants. Grounding: `scratchpad/mission-brief-wave4-sync-degod.md`. Tracked as a #1797 child. PR to upstream/main; coord topology.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Decompose the sync god-module behind a frozen CLI contract (Priority: P1)

A maintainer needs `cli/commands/sync.py` — the single largest, worst-rated source file in the repository — to become a set of small, focused, individually-testable modules (ports + pure decision cores + thin Typer command shells), so future sync work is reviewable and the pure cores are stub-testable. Before touching structure, they freeze the observable behavior of all 22 `spec-kitty sync` subcommands with a golden-CLI-characterization test; every extraction is then a refactor that keeps that characterization green.

**Why this priority**: This is the mission. The file blocks reviewability and carries three complexity suppressions the charter says to retire. The golden test is the safety net that makes the decomposition safe; without it, extraction risks silent behavior drift.

**Independent Test**: Land the golden-CLI-characterization test (all 22 subcommands' flags/exit-codes/`--json`); confirm it passes on the pre-decomposition code, then passes unchanged after each extraction — the observable CLI contract is byte-stable.

**Acceptance Scenarios**:

1. **Given** the pre-decomposition `sync.py`, **When** the golden-CLI-characterization test runs, **Then** it passes and records the exact flags, exit codes, and `--json` envelopes for all 22 subcommands (including the coord exit-0 silent-skip arm and `status --check` exit-2).
2. **Given** any extraction commit (a port, a pure core, a command-shell move), **When** the golden test re-runs, **Then** it passes **unchanged** — no observable CLI behavior differs.
3. **Given** the completed decomposition, **When** `ruff`/Sonar complexity is measured, **Then** `sync_workspace`, `status`, and `doctor` no longer carry `# noqa: C901` and each function is at or below the complexity ceiling.

---

### User Story 2 - Preserve the architectural invariants during the split (Priority: P1)

A reviewer needs assurance the decomposition honors the degod program's non-negotiable invariants and the repository's architectural gates — a careless split (e.g. unifying the read/write authority, placing cores in the wrong layer, mutating a positional-anchor ratchet) is a regression even if the CLI still works.

**Why this priority**: The operator's explicit constraint is architectural-design compatibility. These invariants are what separate a safe degod from a structural regression; they are as load-bearing as behavior preservation.

**Independent Test**: Run the architectural-gate suite (layer rules, shared-package boundary, dead-symbol/module baselines, ratchet + positional-anchor + golden-count guards, sync-writer census, terminology) after the decomposition and confirm all remain green with no ratchet allowlist growth used to accommodate the refactor.

**Acceptance Scenarios**:

1. **Given** the extracted cores and ports, **When** the layer-rule and shared-package-boundary gates run, **Then** every new module lives under `specify_cli.sync.*`/`cli.commands.*` (never `runtime` or a new top-level package) and introduces no cross-boundary or SDK-internal import.
2. **Given** the sync authority logic, **When** it is split, **Then** the read authority and the write authority remain two separate ports/adapters (never unified).
3. **Given** the golden test, **When** it is added, **Then** it does not rely on mutating the DIR-041 positional-anchor ratchet allowlists.

---

### User Story 3 - Clear the mechanical smell debt (Priority: P2)

A maintainer completes the two behavior-preserving mechanical sweeps that ride alongside the degod: `calibration/walker.py`'s duplicated-URN-literal cluster and `sync.py`'s Tier-1 smells (nested ternaries, re-inlined literals, malformed suppression comments).

**Why this priority**: High signal-to-risk, independently landable, and it clears the litter on the surfaces the degod touches. `walker.py` is a distinct file with its own regression guard.

**Independent Test**: `walker.py`'s `S1192` count goes to zero by completing its named-constant set, with the calibration suite (frozenset-equality) proving byte-identical behavior; `sync.py` Tier-1 findings are resolved and re-verified against a fresh Sonar run.

**Acceptance Scenarios**:

1. **Given** `walker.py`, **When** the named-constant set is completed and raw URN literals are replaced, **Then** the calibration inequality tests pass unchanged (frozensets resolve identically) and the `S1192` smells are cleared.
2. **Given** `sync.py` Tier-1 findings, **When** the nested ternaries are extracted, literals hoisted, and malformed suppressions fixed, **Then** behavior is unchanged and the smell count drops.

### Edge Cases

- **Monkeypatch seams**: many `sync.py` `_*` privates are monkeypatched by existing tests. The husk (`__init__.py` re-export block) must keep `sync.<private>` patch targets resolvable after relocation, or those tests break.
- **The coord exit-0 silent-skip arm** (SaaS-disabled guard) is a *documented behavior to freeze*, not an ambiguity swallow — it must be preserved exactly, not "cleaned up" into an error.
- **Golden-test coverage gaps**: `workspace` (no CLI golden today), `status` full human-render (the cc-90 path), `doctor` non-json render + each `--json` branch, and `diagnose --json` are under-characterized and must be frozen *before* their extraction.
- **Deferred behavior**: daemon reuse/kill/lifecycle semantics and env-var deletion are explicitly frozen/deferred; a change to either is out of scope and would be a scope breach.
- **Baseline drift**: arch-gate count baselines must be re-pinned against `upstream/main` (the true merge-base), not the stale fork `origin/main`.

## Requirements *(mandatory)*

### Functional Requirements

| ID | Title | User Story | Priority | Status |
|----|-------|------------|----------|--------|
| FR-001 | Golden CLI contract frozen first | As a maintainer, I want a golden-CLI-characterization test freezing all 22 `spec-kitty sync` subcommands' flags/exit-codes/`--json` landed before any extraction, so the decomposition is provably behavior-preserving. | High | Draft |
| FR-002 | Decompose sync.py into ports + cores + shells | As a maintainer, I want `cli/commands/sync.py` split into injectable ports, pure decision cores, and thin command shells, so the god-module becomes small, focused, reviewable modules. | High | Draft |
| FR-003 | Retire the three C901 suppressions | As a maintainer, I want `sync_workspace`, `status`, and `doctor` decomposed so their `# noqa: C901` come off and each function is within the complexity ceiling. | High | Draft |
| FR-004 | Preserve the read/write authority split | As a reviewer, I want the sync read authority and write authority kept as two separate ports/adapters (never unified), so the #2160-class invariant is not regressed. | High | Draft |
| FR-005 | Complete walker.py's constant set | As a maintainer, I want `calibration/walker.py`'s duplicated URN literals replaced by a completed named-constant set, so its `S1192` cluster is cleared with byte-identical behavior. | Medium | Draft |
| FR-006 | Clean sync.py Tier-1 smells | As a maintainer, I want `sync.py`'s Tier-1 mechanical smells (nested ternaries, re-inlined literals, malformed suppressions) cleaned, behavior-preserving. | Medium | Draft |
| FR-007 | Produce an env-var census (inventory only) | As a maintainer, I want a `SPEC_KITTY_*` env-var census/inventory for the sync surface, so retirement candidates are documented — without deleting any var (deletion defers to WS6). | Low | Draft |

### Non-Functional Requirements

| ID | Title | Requirement | Category | Priority | Status |
|----|-------|-------------|----------|----------|--------|
| NFR-001 | No behavioral regression | The pre-existing sync + calibration test suites (`tests/sync/`, `tests/cli/commands/test_sync_*`, `tests/calibration/`) pass at 100% after the mission; the golden-CLI-characterization test passes identically pre- and post-extraction. | Reliability | High | Draft |
| NFR-002 | Complexity ceiling met, no new suppressions | The three `# noqa: C901` are removed; every extracted/changed function passes `ruff` C901 / Sonar S3776 at ≤ 15; no new blanket suppressions are added; `ruff` + `mypy --strict` clean on changed files. | Maintainability | High | Draft |
| NFR-003 | Smell reduction | `walker.py` `S1192` count → 0; `sync.py` Tier-1 smell count strictly decreases (re-verified against a fresh Sonar run, since the file has drifted from the 2026-08-12 snapshot). | Maintainability | Medium | Draft |
| NFR-004 | Arch-gates stay green | The architectural-gate suite (layer rules, shared-package boundary, dead-symbol/module baselines, ratchet + positional-anchor + golden-count guards, sync-writer census, no-legacy-terminology) remains green, with count baselines re-pinned against `upstream/main`. | Reliability | High | Draft |

### Constraints

| ID | Title | Constraint | Category | Priority | Status |
|----|-------|------------|----------|----------|--------|
| C-001 | Layer + boundary placement | New cores/ports live under `specify_cli.sync.*` / `cli.commands.*` — never `runtime`, never a new top-level `src/` package; zero `runtime`/`spec_kitty_runtime` import; events/tracker consumed only via the existing public adapter seam (no `_internal`, no SDK re-export). | Technical | High | Draft |
| C-002 | Port discipline | Ports are injected on the command shell (default-param), not the frozen `MissionExecutionContext`; exactly one adapter per port; extracted consent/grant writers stay within the sync-writer-census roots. | Technical | High | Draft |
| C-003 | Golden-test-first, no ratchet mutation | The golden-CLI-characterization test lands before any extraction and must not be satisfied by mutating the DIR-041 positional-anchor ratchet allowlists. | Technical | High | Draft |
| C-004 | Deferred scope frozen | Daemon reuse/kill/lifecycle semantics are frozen (deferred to WS4); env-var deletion is deferred to WS6 (census only). The `emitter`/`transport_attempts`/`queue`/`daemon` adapter-consolidation is out of scope (sequenced follow-on). | Business | High | Draft |
| C-005 | Import/monkeypatch compat | The husk keeps `sync.<private>` monkeypatch/import seams resolvable via a guarded re-export block (the `runtime_bridge` #2531 pattern), so external import paths and existing test patches keep working. | Technical | High | Draft |

### Key Entities *(include if feature involves data)*

- **`spec-kitty sync` subcommands (22)**: the Typer command surface whose observable contract (flags, exit codes, `--json` envelopes) is the thing being frozen and preserved.
- **Ports**: injectable adapter interfaces — `Render`, `GitOps`, `Clock`, `FsReader` (reused), plus sync-specific `DeliveryQueue` and a two-part `AuthorityGate` (read vs write).
- **Pure cores**: stub-testable decision logic with no I/O — status row/coherence build, doctor report build, dispatch/exit-code decisions, purge census differentials, per-project-store summaries.
- **Golden-CLI-characterization contract**: the frozen behavior spec (extends `kitty-specs/mvp-cli-sync-boundary-completion-01KRX11M/contracts/sync-status-output.md`).
- **`_REQUIRED_SCOPE` calibration table**: the `walker.py` lookup whose raw URN literals become named constants.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: `cli/commands/sync.py` is reduced to a thin shell plus a set of focused modules each well under the god-module threshold, and the **three `# noqa: C901` are gone** (`sync_workspace`, `status`, `doctor` each ≤ 15 complexity).
- **SC-002**: **100%** of the pre-existing sync + calibration suites remain green, and the golden-CLI-characterization test freezes all **22** subcommands' contract and passes identically before and after every extraction.
- **SC-003**: `walker.py`'s `S1192` count reaches **0**; the net Sonar smell count on the two target files strictly decreases and is reported.
- **SC-004**: **Zero** behavior change — no env var deleted, no daemon-lifecycle semantics changed, the CoordRead≠CoordWrite split preserved — verifiable from the diff and the green golden test.

## Assumptions

- The decomposition follows the established degod template — `runtime_bridge` (#2531) six-seam split (closest analogue) and the coord-authority trio (#2464/#2465/#2508) shell+core+executor pattern, reusing the `agent_tasks_ports.py` port set.
- `sync.py` currently imports no `runtime`/`spec_kitty_runtime` and does not reach `primary_feature_dir_for_mission`; the decomposition keeps both true.
- The 2026-08-12 Sonar line numbers have drifted; the exact Tier-1 findings are re-verified against a fresh run at implementation time.

## Out of Scope

- The `emitter`/`transport_attempts`/`queue`/`daemon` **adapter-consolidation** (a different refactor shape gated on #2173 Phase-2 / WS4 / WS6) — a sequenced Wave-4 follow-on.
- **Deleting** any `SPEC_KITTY_*` env var (defers to the WS6 versioned-contract policy ADR) — this mission produces the census only.
- Any **behavioral** change to daemon reuse/kill/lifecycle (defers to WS4 daemon-identity).
