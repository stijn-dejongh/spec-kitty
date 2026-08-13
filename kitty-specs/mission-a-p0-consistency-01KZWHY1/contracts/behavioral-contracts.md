# Behavioral Contracts — Mission A

Four observable contracts. Each is pinned by a red-first reproduction (existing or
replaced) plus the mandatory green-wash guard tests. These are behavior contracts,
not HTTP APIs — the mission adds no endpoints.

## C#3320 — Retrospect `--update` agrees with disk

- **Given** an on-disk retrospective record `has_findings` with 1 gap, **when**
  `retrospect create --update --json` runs with a generator yielding
  `ran_no_findings`, **then** reported `findings_status == "has_findings"` and
  `counts.gaps == 1`, **and** the emitted `RetrospectiveCaptured` event carries
  the same merged record.
- **Invariant**: report ≡ event ≡ persisted file, for `--update`. `--overwrite`/
  `error`/backfill unchanged. `write_gen_record` return type unchanged.
- **Tests**: `tests/regression/test_issue_3320_*` (JSON) → on green, relocate to
  `tests/cli/commands/`; **+ new**: emitted-event-payload equals persisted record.

## C#3231 — A scaffold placeholder cannot flip acceptance

- **Given** a matrix whose real criteria are all `pass` plus the empty `AC-001`
  placeholder (`description == SCAFFOLD_TODO_MARKER`), **when** `overall_verdict`
  is computed, **then** it is not `pending`.
- **Given** a matrix with a seeded FR row still `pending` (marker in `notes`,
  real `description`), **or** an all-scaffold matrix, **then** `overall_verdict`
  is `pending`.
- **Invariant**: only the contentless empty placeholder is verdict-exempt; a
  seeded-but-unauthored requirement always blocks; an un-authored matrix never
  reads `pass`.
- **Tests**: `tests/regression/test_issue_3231_*` (empty-placeholder+all-pass) →
  on green relocate to `tests/acceptance/`; **+ new**: partial-authoring→pending,
  all-scaffold→pending.

## C#3334 — A failed upgrade leaves a recoverable project

- **Given** a healthy schema-3 project (`schema_version: 3`, version behind, 3.x
  `success` history), **when** `MigrationRunner.upgrade(target)` hits a failing
  migration, **then** `get_project_schema_version() == 3` afterward (not `None`),
  **and** the real startup gate `check_schema_version(project_root, "plan")` does
  not raise `SystemExit`.
- **Given** a genuinely pre-3.x project (`schema_version` absent, no 3.x `success`
  history), **when** the gate runs for an unsafe command, **then** it classifies
  `LEGACY` and raises `SystemExit(4)`.
- **Invariant**: a failed upgrade is non-destructive to the schema stamp; the
  genuine-pre-3.x `LEGACY` guard is unchanged; the classifier (`planner.py`,
  `safety.py`) is untouched.
- **Tests**: **replace** `tests/regression/test_issue_3334_*` — drive real
  `MigrationRunner.upgrade()` (stub failing migration via `MigrationRegistry`);
  assert the three post-conditions above.

## C#3311 — Re-finalize after execution preserves provenance

- **Given** a mission with materialized lanes, a recorded `planning_commit_sha`,
  and ≥1 WP past `planned` in the status event log, **when** `finalize-tasks`
  re-runs after an ownership-only `owned_files` amendment, **then**
  `planning_commit_sha` is preserved (or the run refuses before writing) — even
  when the current branch tip differs (non-`None`).
- **Given** a mission with all WPs at `planned` (no execution begun), **when**
  `finalize-tasks` re-runs, **then** lanes regenerate and the run does not refuse.
- **Invariant**: preserve/refuse triggers on execution-state (status log), never
  on `lanes.json`/`planning_commit_sha` presence; single-write provenance freeze
  (ADR 2026-07-29-1/FR-009) preserved.
- **Tests**: `tests/regression/test_issue_3311_*` (None-tip) → on green relocate
  to `tests/specify_cli/cli/commands/agent/`; **+ new**: non-`None`-tip
  preservation, benign pre-execution re-finalize regenerates.
