# Research — Mission A — P0 Read/Write Consistency

Phase 0 output. Four resolution decisions, each grounded in a live trace against
`main`. A pre-spec research squad (debugger-debbie · reviewer-renata ·
paula-patterns) and a Phase-0 #3334 trace produced the evidence below; contested
findings and their dispositions are recorded per
`contracts/adversarial-evidence-contract.md` conventions in the final section.

Supply-chain note: **this mission adds/updates/removes no dependency** — the
supply-chain-install-safety directive is N/A (no lifecycle-script or registry
surface is introduced).

---

## R-01 — #3320 retrospect `--update` reports/emits the persisted record

- **Decision**: In `create_cmd` (`src/specify_cli/cli/commands/retrospect.py`),
  after `write_gen_record(...)` returns the path, **read the persisted record
  back** via the existing `read_gen_record(record_path)`
  (`src/specify_cli/retrospective/reader.py:329`) and build the JSON `counts`/
  `findings_status` **and** the `emit_captured(...)` payload from that read-back
  record — not from the pre-merge `record`.
- **Rationale**: `write_gen_record(mode="update")` merges with the on-disk record
  and recomputes `findings_status` inside the writer, but returns only a `Path`
  (`writer.py:498`); the CLI reports from the stale pre-merge object
  (`retrospect.py:405`/`423`/`442`). Read-back is a no-op for
  `overwrite`/`error`/backfill (persisted == new) and corrects only the `--update`
  divergence.
- **Alternatives considered**: change `write_gen_record` to return the record
  (Path→record). **Rejected** — wide blast radius: ~4 callers use the `Path`
  (`retrospect.py:733`, `agent_retrospect.py:310`, …) and ~30 test assertions +
  mocks return a `Path`. If enrichment is ever wanted it must be **additive**
  (`(path, record)`), never a replacement (C-002).
- **Guard beyond the repro**: the committed repro asserts JSON only (it patches
  `emit_captured`→None). Add a focused test asserting the **emitted event
  payload** equals the persisted record (FR-002 / NFR-002).

## R-02 — #3231 verdict special-cases only the empty scaffold placeholder

- **Decision**: In `AcceptanceMatrix.overall_verdict`
  (`src/specify_cli/acceptance/matrix.py:249-272`), exempt a criterion from the
  `pending`-dominates rule **iff `description == SCAFFOLD_TODO_MARKER`** (the
  contentless placeholder), and only when at least one non-scaffold criterion
  exists. An all-scaffold matrix stays `pending`.
- **Rationale**: `overall_verdict:263` lets any `pending` row dominate; the empty
  scaffold placeholder (`AC-001`) is a `pending` row. The scaffold builder writes
  the marker into **two** shapes: the empty placeholder with
  `description == SCAFFOLD_TODO_MARKER` (`matrix.py:531`) **and** one row per
  functional requirement with a real `description=f"Verify {req_id}…"` carrying
  the marker only in `notes` (`matrix.py:517-520`). Keying on `description`
  therefore uniquely targets the empty placeholder (CONFIRMED at
  `matrix.py:517` vs `:531`).
- **Alternatives considered**:
  - Key on `notes == SCAFFOLD_TODO_MARKER`. **Rejected — demonstrated
    false-accept**: it also exempts seeded-but-unauthored FR rows, so 9-of-10
    unauthored requirements → verdict `pass` through the accept gate
    (`gates_core.py:525-529`). This is the load-bearing correction (C-003).
  - Fix the merge-driver reconciler to drop the scaffold row.
    **Rejected** — the reconciler is correct (FR-008 row-union); a leftover
    scaffold in a hand-authored/non-merged matrix would still poison. The verdict
    property is the single authority and the right seam.
- **Guard beyond the repro**: partial-authoring (9/10 FR rows `pending` →
  `pending`) and all-scaffold (→ `pending`) tests are mandatory (FR-004 /
  NFR-002); the repro pins only the empty-`AC-001`+all-pass case.

## R-03 — #3334 failed upgrade leaves a recoverable project *(Phase-0 trace)*

- **Decision**: Fix in `MigrationRunner.upgrade()`
  (`src/specify_cli/upgrade/runner.py` ~:148-201) with **restore-on-failure**:
  capture `pre_schema = get_project_schema_version(project_path)` before the
  migration loop; ensure the schema stamp is written **regardless of
  `result.success`** — on success stamp `REQUIRED_SCHEMA_VERSION`, on failure
  restore `pre_schema`. When `pre_schema is None` (genuine pre-3.x), stamp
  nothing → project stays `LEGACY` → still gate-blocked (FR-006 preserved).
  **Do not touch** `compat/planner.py` or `safety.py`.
- **Rationale (traced live)**: the restoring re-stamp (`runner.py:189-190`) is
  gated behind `if not dry_run and result.success:` (`runner.py:181`). On a
  migration failure, `_apply_migration` records the migration `"failed"` →
  `metadata.save()` (`runner.py:487-489`/`288`) → `ProjectMetadata.save()`
  (`metadata.py:188-210`) rebuilds YAML from a fixed 3-key model with no
  `schema_version`, stripping it (the appended `failed` record changes
  `migrations.applied`, so the masked compare-before-write fires a real write).
  The restore is skipped. On re-run, `has_migration()` counts only
  `result == "success"` (`metadata.py:242`), so the migration re-fails and the
  restore is never reached — self-perpetuating. Exit-4 then surfaces two ways:
  the startup gate (`migration/gate.py:146-154`, wired `__init__.py:140`) for
  non-exempt commands, and `upgrade --json --project` (`upgrade.py:688`,
  `1136-1163`) directly.
- **Alternatives considered**:
  - Teach `_scan_project` to read `migrations.applied` (the classifier change the
    **committed repro pins**). **Rejected** — treats the symptom, duplicates
    schema truth into a drift-prone heuristic, risks weakening the genuine-pre-3.x
    `LEGACY` guard, trusts spoofable metadata, and still does not let
    `spec-kitty upgrade` complete (the runner keeps exiting without restoring).
  - Make `ProjectMetadata.save()` preserve the on-disk `schema_version` (the
    durable, deeper fix). **Deferred as optional follow-up** — larger blast
    radius (touches every `save()` caller); the runner restore is the minimal,
    correct fix that closes the wedge. Noted for a future campsite/hardening pass.
- **Repro replacement (C-006)**: replace
  `tests/regression/test_issue_3334_failed_upgrade_wedges_repair.py` (which drives
  compat `plan()` with a fabricated UNSAFE command and asserts on `Decision`) with
  a reproduction driving the real `MigrationRunner(project_path).upgrade(target)`
  (or the `upgrade` CLI via `CliRunner`) with a stub failing migration injected
  into `MigrationRegistry`, starting from `schema_version: 3` present + version
  behind + 3.x `success` history. Post-conditions: (1) `get_project_schema_version
  == 3` (not `None`) after the failed upgrade; (2) real gate
  `check_schema_version(project_path, "plan")` does not raise `SystemExit`;
  (3) negative guard — genuine pre-3.x still `LEGACY` and gate raises
  `SystemExit(4)`.

## R-04 — #3311 re-finalize preserves provenance once execution has begun

- **Decision**: Gate the recompute/overwrite in `_compute_and_write_lanes`
  (`src/specify_cli/cli/commands/agent/mission_finalize.py` ~:1205-1252) on an
  **"execution has begun"** signal. When execution has begun, preserve the
  established `planning_commit_sha` (do not re-capture the branch tip), or refuse
  before writing any bytes. When it has not begun, keep today's recompute
  behavior (including re-capture) — the documented idempotent pre-execution
  re-finalize (`mission_finalize.py` docstring ~:326-327).
- **Signal**: the append-only status event log — the sole authority for WP lane
  state (034+/060) — read through the canonical, coord-aware reader
  (`status/reducer.py::materialize` / `status/lane_reader.py`, per the resolved
  status surface). **Execution begun ⟺ any WP's current lane ∉ {`planned`}.**
- **Rationale**: first-time finalize **always** writes `lanes.json` and sets
  `planning_commit_sha` (`runner`/`:1251`), so a trigger keyed on file/SHA
  presence fires on every benign second finalize and would freeze/refuse a
  legitimate pre-implementation re-plan (renata, HIGH). The status event log is
  the correct authority for "has execution started." Respect ADR 2026-07-29-1 /
  FR-009 single-write freeze — no second commit, no re-capture on the
  execution-begun path (C-005).
- **Scope correction**: the "topology collapse / lane renumber" narrative does
  **not** reproduce (debbie — live run shows lanes stable, `collapsed:0`); scope
  the fix to the confirmed `planning_commit_sha` clobber only. Do not promise
  topology preservation without first reproducing it (C-007).
- **Guard beyond the repro**: (a) preservation must hold against a **non-`None`**
  re-captured tip — the repro only covers the `None` (non-git tmp) case, which a
  naive `if sha is not None:` would fake-green; (b) a benign pre-execution
  re-finalize still regenerates and does not refuse (FR-008 / NFR-002).
- **Open sub-question (non-blocking)**: whether re-finalize that adds a **new** WP
  (vs. amending an existing one) is a supported re-plan or a refuse case. Default
  for this mission: the refuse/preserve path triggers only on execution-begun; a
  pre-execution add-WP re-finalize regenerates freely. Revisit only if a WP
  surfaces a concrete need.

---

## Adversarial evidence ledger

Per `contracts/adversarial-evidence-contract.md`. All contested findings were
resolved before plan readiness — none silently dropped.

| Finding (source) | Disposition | Where reflected |
|------------------|-------------|-----------------|
| #3231 `notes`-marker discriminator → false-accept (renata, CRITICAL) | **changed** | R-02, C-003, spec FR-004 |
| #3334 repro pins wrong contract; classifier fix over-corrects (renata, HIGH; #3334 trace) | **changed** | R-03, C-006, IC-03 fix retargeted to `runner.upgrade()` |
| #3311 trigger must be execution-state, not file presence (renata, HIGH) | **changed** | R-04, C-005 |
| #3311 topology-collapse narrative not reproduced (debbie, HIGH) | **changed** | R-04 scope correction, C-007 |
| #3320 writer return-type change has wide blast radius (renata, MED) | **accepted** (steer to read-back) | R-01, C-002 |
| "One shared root cause" framing partially forced; #3231 is the odd member (paula, HIGH) | **accepted** | reframed to per-fix ICs; C-001 no-shared-helper non-goal |
| Green-wash: 3 of 4 repros pin only the positive half (debbie) | **accepted** | NFR-002 mandatory guard tests in every IC |
| #3334 durable `save()`-preserves-schema fix vs minimal runner restore | **deferred_with_rationale** | R-03 (minimal runner restore now; `save()` hardening noted as optional follow-up) |
