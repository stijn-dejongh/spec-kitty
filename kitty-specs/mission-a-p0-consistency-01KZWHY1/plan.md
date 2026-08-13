# Implementation Plan: Mission A — P0 Read/Write Consistency

**Branch**: `fix/mission-a-p0-consistency` | **Date**: 2026-08-13 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `kitty-specs/mission-a-p0-consistency-01KZWHY1/spec.md`

## Summary

Remediate four accepted, open P0 defects — #3320, #3231, #3334, #3311 — each with a committed red-first reproduction under `tests/regression/`. Each is a surgically-scoped, module-local fix; there is **no shared helper or shared read-state abstraction** (C-001). The unifying theme (a read/compute/report step trusting the wrong slice of persisted state) is a review lens, not an implementation seam. Delivery sequence P1→P4 lands the lowest-risk fixes first and the highest-blast-radius fix (#3311, provenance-ADR behavior change) last.

## Technical Context

**Language/Version**: Python 3.11+ (project baseline; typed, `from __future__ import annotations`)
**Primary Dependencies**: typer, rich, ruamel.yaml (existing) — **no new dependencies added by this mission**
**Storage**: on-disk mission artifacts under `kitty-specs/<mission>/` (`acceptance-matrix.json`, `status.events.jsonl`, `lanes.json`, retrospective `*.yaml`) and `.kittify/metadata.yaml`
**Testing**: pytest; committed red-first repros under `tests/regression/` (`-m regression`) plus per-fix focused unit tests in each module's functional suite; `PWHEADLESS=1`, `-n auto --dist loadfile` for local parallel runs
**Target Platform**: cross-platform CLI (Linux/macOS/Windows 10+)
**Project Type**: single project (CLI toolkit)
**Performance Goals**: N/A — correctness fixes; no hot-path or latency change
**Constraints**: `ruff` + `mypy` clean on changed code, complexity ≤ 15, no new suppressions (NFR-003); no other CI suite reddened (NFR-004); no dependency changes (supply-chain section N/A)
**Scale/Scope**: 4 defects × (1 product fix + guard tests) across 4 independent modules; no cross-module coupling

## Charter Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **ATDD-first / red-first discipline (C-011):** PASS — every fix already has a committed red-first reproduction; guard tests are specified per fix (NFR-002). #3334's mis-targeted repro is replaced, not weakened (C-006), consistent with the `tests/regression/` exit rule.
- **Single canonical authority / no legacy resolver paths:** PASS — each fix routes reads through the canonical authority (verdict property, `read_gen_record`, resolved status surface, metadata reader); no no-canonical-field fallback branches introduced.
- **Terminology Canon (Mission not feature):** PASS — no user-facing identifier renames; not a bulk edit.
- **Regression Vigilance / no collateral:** PASS by design — no shared helper (C-001); each fix is module-local; NFR-004 gates collateral.
- **Shared Package Boundary:** N/A for Mission A (that boundary governs #3307 / Mission B). No `spec_kitty_events`/`spec_kitty_tracker` internals touched.
- **Provenance ADR 2026-07-29-1 / FR-009:** BINDING on #3311 — the single-write provenance freeze must be preserved; the fix must not introduce a second commit or re-capture on an execution-begun re-run (C-005).

No charter violations requiring Complexity Tracking.

## Project Structure

### Documentation (this mission)

```
kitty-specs/mission-a-p0-consistency-01KZWHY1/
├── plan.md              # This file
├── research.md          # Phase 0 — four resolution decisions + #3334 trace
├── data-model.md        # Phase 1 — the four state authorities + their invariants
├── quickstart.md        # Phase 1 — how to run each repro + guard test
└── contracts/           # Phase 1 — the four observable behavioral contracts
```

### Source Code (repository root)

```
src/specify_cli/
├── acceptance/matrix.py                          # #3231 — overall_verdict discriminator
├── cli/commands/retrospect.py                    # #3320 — read-back before report/emit
├── retrospective/reader.py                       # #3320 — read_gen_record (reused, unchanged)
├── compat/            (planner.py, safety.py)     # #3334 — messaging-only, keep UNSAFE blocked
├── upgrade/           (runner.py, detector.py, metadata write path)  # #3334 — write-once-and-restore (primary fix site, pending Phase-0 trace)
├── cli/commands/agent/mission_finalize.py         # #3311 — execution-begun guard on _compute_and_write_lanes
└── status/            (reducer.py, lane_reader.py) # #3311 — resolved status surface reader (reused)

tests/
├── regression/        # existing repros; #3334 repro replaced (C-006), others exit on green
├── acceptance/ · cli/commands/ · specify_cli/compat/ · specify_cli/cli/commands/agent/  # per-fix guard tests
```

**Structure Decision**: single project; each fix stays within its existing module and its sibling test suite. No new packages, no new shared module.

## Implementation Concern Map

> Concerns are not work packages. `/spec-kitty.tasks` translates these into WPs. The 1:1 concern→WP mapping here is intentional (C-001 non-goal: four independent fixes) — do not merge them.

### IC-01 — Retrospect reports/emits the persisted record (#3320)

- **Purpose**: `retrospect create --update` must report counts/`findings_status` and emit the lifecycle event from the merged on-disk record, not the pre-merge generated one.
- **Relevant requirements**: FR-001, FR-002; C-002; SC-002.
- **Affected surfaces**: `src/specify_cli/cli/commands/retrospect.py` (`create_cmd` — build `counts`/JSON/`emit_captured` from a read-back record); reuse `src/specify_cli/retrospective/reader.py::read_gen_record` (unchanged). **Do not** change `write_gen_record`'s `Path` return type.
- **Sequencing/depends-on**: none (land first — lowest risk).
- **Risks**: `emit_captured` currently fed the pre-merge record — the event payload must be re-pointed too, not just the JSON. Guard test asserts the emitted payload (repro covers JSON only).

### IC-02 — Verdict special-cases only the empty scaffold placeholder (#3231)

- **Purpose**: `AcceptanceMatrix.overall_verdict` must not let the contentless `AC-001` scaffold placeholder dominate a matrix whose real criteria pass — while seeded-but-unauthored FR rows and all-scaffold matrices still stay `pending`.
- **Relevant requirements**: FR-003, FR-004; C-003; SC-001.
- **Affected surfaces**: `src/specify_cli/acceptance/matrix.py` (`overall_verdict`, ~:263). Discriminator = `description == SCAFFOLD_TODO_MARKER` — CONFIRMED unique to the empty placeholder (matrix.py:531); seeded FR rows carry the marker only in `notes` with a real `description` (matrix.py:517-520).
- **Sequencing/depends-on**: none.
- **Risks**: symmetric false-accept if the discriminator is too broad — guard tests (partial-authoring → pending; all-scaffold → pending) are mandatory. No other `overall_verdict` caller relies on the empty placeholder dominating (verify the accept/done gates in `gates_core.py` treat seeded-pending FR rows unchanged).

### IC-03 — Failed upgrade leaves a recoverable project (#3334)  *(fix site finalized by Phase-0 trace — see research.md R-03)*

- **Purpose**: a project whose `schema_version` was stripped by a failed `upgrade` must remain repairable via the normal route; a genuine pre-3.x project must stay blocked from unsafe mutating commands.
- **Relevant requirements**: FR-005, FR-006; C-004, C-006; SC-003.
- **Root cause (traced live)**: `MigrationRunner.upgrade()` gates the restoring re-stamp `_stamp_schema_version(..., REQUIRED_SCHEMA_VERSION)` (`runner.py:189-190`) behind `if not dry_run and result.success:` (`runner.py:181`). On a migration failure, `_apply_migration` records the migration `"failed"` → `metadata.save()` (`runner.py:487-489`/`288`) → `ProjectMetadata.save()` (`metadata.py:188-210`) rebuilds the YAML from a fixed 3-key model with **no** `schema_version`, stripping it; the failed record changes `migrations.applied` so the masked compare-before-write fires a real write. The restore is skipped (`result.success=False`). On re-run, `has_migration()` ignores `failed` records (`metadata.py:242`) → the migration re-fails → restore never reached: self-perpetuating. Exit-4 then surfaces via the startup gate (`migration/gate.py:146-154`, wired `__init__.py:140`) for non-exempt commands **and** via `upgrade --json --project` (`upgrade.py:688`,`1136-1163`).
- **Fix site**: `src/specify_cli/upgrade/runner.py::MigrationRunner.upgrade()` (~:148-201) — **restore-on-failure**: capture `pre_schema` before the loop; write the stamp regardless of `result.success` (on success → `REQUIRED_SCHEMA_VERSION`; on failure → restore `pre_schema`; `pre_schema is None` → stamp nothing, project stays `LEGACY`-blocked, preserving FR-006). **No classifier change** — `compat/planner.py` and `safety.py` are untouched (the classifier is a faithful reader; changing it is the wrong site, C-004 satisfied trivially). Optional durable follow-up (larger, out of minimal scope): make `ProjectMetadata.save()` preserve the on-disk `schema_version` so no caller can strip it.
- **Repro replacement (C-006)**: drive the real `MigrationRunner(project_path).upgrade(target)` (or `upgrade` via `CliRunner`) with a stub failing migration injected into `MigrationRegistry`; fixture starts with `schema_version: 3` present + version behind + 3.x `success` history. Assert (1) post-failure `get_project_schema_version == 3` (not `None`); (2) real gate `check_schema_version(project_path, "plan")` does not raise `SystemExit`; (3) negative guard — genuine pre-3.x (no schema_version, no 3.x history) still classifies `LEGACY` and the gate raises `SystemExit(4)`.
- **Sequencing/depends-on**: none (independent module).
- **Risks**: none of the over-correction hazards apply now — the fix does not touch `decide`/`safety`, so the UNSAFE-blocking guard and the genuine-LEGACY path are preserved unchanged.

### IC-04 — Re-finalize after execution preserves provenance (#3311)

- **Purpose**: a `finalize-tasks` re-run after execution has begun must preserve `planning_commit_sha` (or refuse before writing), never clobber it on an ownership-only amendment; a pre-execution re-finalize still regenerates freely.
- **Relevant requirements**: FR-007, FR-008; C-005, C-007; SC-004.
- **Affected surfaces**: `src/specify_cli/cli/commands/agent/mission_finalize.py::_compute_and_write_lanes` (~:1251) — gate the recompute/re-capture on an "execution has begun" signal. Signal = the resolved status surface (034+ append-only event log, coord-aware) via the canonical reader (`status/reducer.py::materialize` / `status/lane_reader.py`): execution begun ⟺ any WP's current lane ∉ {`planned`}. Respect ADR 2026-07-29-1/FR-009 single-write freeze.
- **Sequencing/depends-on**: LAST (highest blast radius; behavior change). Does not block IC-01–IC-03.
- **Risks**: a presence-based trigger (`lanes.json`/`planning_commit_sha` set) would break the documented idempotent pre-execution re-finalize (`mission_finalize.py` docstring ~:326) — the trigger MUST be execution-state-based. Scope strictly to the confirmed provenance-clobber; do not promise topology preservation (unreproduced).
