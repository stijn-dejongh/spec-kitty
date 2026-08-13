---
description: "Work packages for Upgrade/migration atomicity & recoverability"
---

# Work Packages: Upgrade/migration atomicity & recoverability

**Inputs**: `kitty-specs/upgrade-atomicity-recovery-01KZWSHC/` — spec.md, plan.md (§Post-Plan Adversarial Revisions is binding), research.md
**Prerequisites**: plan.md (required), spec.md (user stories), research.md (file:line seams)

**Tests**: ATDD-first for **every** WP — each acceptance scenario lands as a failing test before its code (not only #3334).

**Organization**: Subtasks (`Txxx`) roll into work packages (`WPxx`). Each WP is independently deliverable/testable. Ordering is **priority, not blocking edges** — only the genuine dependency edges below gate claiming; everything else is claimable in parallel.

## Path Conventions

Single project: `src/specify_cli/…`, tests under `tests/…`.

---

## Work Package WP01: Recovery core — preserve `schema_version` + resumable re-run (Priority: P0) 🎯 MVP

**Goal**: A failed migration never advances `schema_version`; a re-run is a safe no-op — closing the #3334 P0.
**Independent Test**: A red-first `@pytest.mark.regression` repro (synthetic always-failing migration) is red pre-fix, green post-fix; legacy/None and `<REQUIRED` projects never get the target schema stamped; FR-012 re-run applies zero migrations.
**Prompt**: `/tasks/WP01-recovery-core-preserve-schema-version.md`
**Requirement Refs**: FR-002, FR-012, NFR-001, NFR-002

### Included Subtasks
- [ ] T001 Author the #3334 red-first regression (`@pytest.mark.regression`, synthetic failing migration; trigger-agnostic) in `tests/upgrade/`
- [ ] T002 Preserve/restore pre-run `schema_version` on the abort path in `src/specify_cli/upgrade/runner.py` (do NOT blanket-`finally`-stamp target)
- [ ] T003 Ensure `ProjectMetadata.save()` no longer erases `schema_version` on the failure path (`src/specify_cli/upgrade/metadata.py`)
- [ ] T004 [P] Assert FR-012 resumable no-op (re-run applies zero migrations)

### Dependencies
- None (P0 core; starting package).

### Risks & Mitigations
- Load-bearing coupling: `_stamp_schema_version` writes the **target** schema — restore the captured value, never the target, on failure. Regression pins the legacy/None case.

---

## Work Package WP02: Ungate the recommended diagnostic (Priority: P0)

**Goal**: `migrate backfill-runtime-state --dry-run` is reachable on a wedged project (fixes the #3338 circularity).
**Independent Test**: On a LEGACY/blocked project, the `--dry-run` diagnostic runs; the mutating form stays blocked.
**Prompt**: `/tasks/WP02-ungate-diagnostic.md`
**Requirement Refs**: FR-003

### Included Subtasks
- [ ] T005 Register `("migrate","backfill-runtime-state")` SAFE via a fail-closed `--dry-run` predicate in `src/specify_cli/compat/safety.py`
- [ ] T006 [P] Test: predicate returns SAFE iff `--dry-run`; UNSAFE otherwise and on predicate exception

### Dependencies
- None.

### Risks & Mitigations
- Predicate must fail closed — the mutating `migrate backfill-runtime-state` (no `--dry-run`) must remain UNSAFE.

---

## Work Package WP03: Duplicate-key detect + repair (Priority: P1) 🎯 recovery bundle

**Goal**: Heal legacy dual-key `review_feedback` artifacts before upgrade trips over them.
**Independent Test**: Doctor scan lists malformed artifacts; opt-in `--fix` repairs them batch-atomically to valid YAML without discarding recorded state.
**Prompt**: `/tasks/WP03-dup-key-detect-repair.md`
**Requirement Refs**: FR-008, NFR-002, NFR-004, C-004

### Included Subtasks
- [ ] T007 New small module `src/specify_cli/status/dup_key_repair.py` — raw-text duplicate-key **detector** (not via `read_frontmatter`, which fails closed)
- [ ] T008 Surface detection as a `check_*` Finding in `status/doctor.py` (thin delegation; keep god-module #1623 from growing)
- [ ] T009 Implement **repair** by extending `src/specify_cli/migration/mission_state.py` (`repair_repo`/`RepairReport`/`FileChange`/`atomic_write`); keep-last-non-empty policy
- [ ] T010 Wire opt-in `--fix` through `cli/commands/_mission_state_doctor.py`
- [ ] T011 [P] Unit tests: detector, batch-atomic repair, non-destructive invariant

### Dependencies
- None (code); ships with the recovery bundle for heal-before-upgrade.

### Risks & Mitigations
- Riskiest **mandatory** WP: repair must be non-destructive (NFR-002) and batch-atomic (NFR-004). Reuse the ADR `2026-05-10-1` machinery — do not reinvent.

---

## Work Package WP04: Recovery composition — end-to-end, zero-git (Priority: P1) 🎯 MVP

**Goal**: Compose FR-002 + FR-008 + FR-012 so a wedged project self-recovers (SC-001), including a no-VCS project.
**Independent Test**: A wedged project (incl. one not under version control) recovers to an upgradable state with zero manual git steps.
**Prompt**: `/tasks/WP04-recovery-composition.md`
**Requirement Refs**: FR-001, NFR-002

### Included Subtasks
- [ ] T012 Wire the recovery flow (no new command unless proven necessary); adopt ADR `2026-05-10-1` principles
- [ ] T013 [P] Acceptance: SC-001 zero-git recovery
- [ ] T014 [P] Acceptance: no-VCS wedged-project recovery (on-disk, no git checkpoint)

### Dependencies
- Depends on WP01, WP03.

### Risks & Mitigations
- Pin FR-001 scope: composition/wiring, not a parallel unknown.

---

## Work Package WP05: Report-on-abort for the bulk cutover (Priority: P1)

**Goal**: A non-atomic abort enumerates every mission/file already written (no silent partial write).
**Independent Test**: Backfill over a fixture where mission K fails → abort output lists every mission/file already written.
**Prompt**: `/tasks/WP05-report-on-abort.md`
**Requirement Refs**: FR-005, NFR-003

### Included Subtasks
- [ ] T015 Stop discarding `_cutover_corpus` `results` on abort in `src/specify_cli/upgrade/migrations/m_zz_runtime_state_backfill.py::apply`
- [ ] T016 Add a machine-readable partial-write account (extend `MigrationResult`, `upgrade/migrations/base.py`)
- [ ] T017 [P] Test: graceful-abort enumeration matches what was written

### Dependencies
- None (claimable in parallel; recovery-first is priority, not an edge).

### Risks & Mitigations
- Scope to **graceful** abort; SIGKILL/durable accounting is WP06/#2933 territory.

---

## Work Package WP06: Corpus staging-promote (Priority: P2, OPTIONAL)

**Goal**: True "mutate nothing on abort" + SIGKILL crash-atomicity via the staging-promote pattern.
**Independent Test**: Abort/SIGKILL mid-run leaves zero missions mutated; `status.events.jsonl` promotion is append-preserving.
**Prompt**: `/tasks/WP06-corpus-staging-promote.md`
**Requirement Refs**: FR-004, C-004

### Included Subtasks
- [ ] T018 Stage → validate → `os.replace` promote per ADR `2026-04-17-2`
- [ ] T019 Append-preserving event-log staging (staged = prior ∪ appended, verified monotonic) to protect NFR-005
- [ ] T020 [P] Test: SIGKILL mid-commit recoverable

### Dependencies
- Depends on WP05. **Deferrable** — dropping it removes SIGKILL-edge coverage (documented).

### Risks & Mitigations
- Contradicts the intentional per-mission design (D-03) — justify via ADR; higher-risk, isolate from WP05.

---

## Work Package WP07: Event-log / reducer integrity after recovery (Priority: P1)

**Goal**: Recovery never breaks reducer determinism or append-only integrity.
**Independent Test**: `reduce()` over the recovered log == pre-abort log ∪ committed events; re-run appends no duplicate transitions.
**Prompt**: `/tasks/WP07-event-log-integrity.md`
**Requirement Refs**: NFR-005

### Included Subtasks
- [ ] T021 Half-applied-backfill fixture builder in `tests/`
- [ ] T022 Assert reducer-determinism invariant + `event_id` de-dup + `detect()`-gating idempotency

### Dependencies
- Depends on WP01, WP05.

### Risks & Mitigations
- Verification WP — no product code beyond fixtures/asserts; guards the recovery/atomicity WPs.

---

## Work Package WP08: Retire the append-on-miss frontmatter writer (Priority: P2)

**Goal**: The latent `set_scalar` append-on-miss path can never re-introduce a dual-key.
**Independent Test**: No code path appends an inline `review_feedback` key; `set_scalar` is retired/fail-closed and its test callers migrated.
**Prompt**: `/tasks/WP08-retire-set-scalar.md`
**Requirement Refs**: FR-006

### Included Subtasks
- [ ] T023 Retire or fail-close `set_scalar` in `src/specify_cli/task_utils/support.py`
- [ ] T024 [P] Migrate `tests/utils.py` `set_scalar` callers to a supported writer

### Dependencies
- None.

### Risks & Mitigations
- Zero production callers today; the only red is the test helper (migrate it in the same WP).

---

## Work Package WP09: Legible duplicate-key guard (Priority: P2)

**Goal**: The already-fail-closed frontmatter boundary raises a legible error naming the duplicate key(s).
**Independent Test**: A dual-key artifact raises an error naming the key; `allow_duplicate_keys=False` is pinned by regression.
**Prompt**: `/tasks/WP09-legible-dup-key-guard.md`
**Requirement Refs**: FR-007, C-002

### Included Subtasks
- [ ] T025 Explicit `except DuplicateKeyError` branch naming the key(s) before the generic handler in `src/specify_cli/frontmatter.py:122-127`
- [ ] T026 Pin `allow_duplicate_keys=False` on the `YAML()` instance (`frontmatter.py:83`) under regression; consume WP03's raw-text detector to enumerate all duplicates

### Dependencies
- Depends on WP03 (shared detector).

### Risks & Mitigations
- Keep the guard centralized in the canonical boundary (C-002).

---

## Work Package WP10: Honest dry-run preview (Priority: P2)

**Goal**: `upgrade --dry-run` reports the real pending set (drive the preview through the real detector).
**Independent Test**: On a project with M pending migrations, `--dry-run` reports exactly those M.
**Prompt**: `/tasks/WP10-honest-dry-run.md`
**Requirement Refs**: FR-009

### Included Subtasks
- [ ] T027 Route the dry-run/`--json` preview through `MigrationRegistry.get_applicable` (`upgrade/detector.py`) instead of the divergent planner path (`compat/planner.py:1027`)
- [ ] T028 [P] Test: preview pending set == real applied set

### Dependencies
- None (independent).

### Risks & Mitigations
- Preserve block-decision semantics while unifying the computation; the `null` framing is stale — fix the divergence.

---

## Work Package WP11: Remediation body survives `--json` (Priority: P3)

**Goal**: The `CHARTER_PACK_CONFIG_INVALID` remediation body is present in `agent mission create --json`.
**Independent Test**: Invalid charter pack → `--json` failure envelope carries the remediation body.
**Prompt**: `/tasks/WP11-remediation-body-json.md`
**Requirement Refs**: FR-010

### Included Subtasks
- [ ] T029 Carry the remediation body on the mission-create `--json` envelope
- [ ] T030 [P] Test: remediation body present in `--json`

### Dependencies
- None (independent).

### Risks & Mitigations
- Good-first-issue scope (#3337); keep narrow.

---

## Work Package WP12: Mission-create checkout restore (Priority: P3)

**Goal**: A failed mission-create restores the operator's branch/checkout and leaves no orphan branch.
**Independent Test**: A mission-create that fails after creating a branch restores the original checkout with no orphan branch.
**Prompt**: `/tasks/WP12-mission-create-checkout-restore.md`
**Requirement Refs**: FR-011

### Included Subtasks
- [ ] T031 Restore branch/checkout on mission-create failure
- [ ] T032 [P] Test: failed create → original branch, no orphan

### Dependencies
- None (independent); coordinate with #3328 to avoid double-fixing.

### Risks & Mitigations
- External-coordination risk (#3328 mission-create git-side-effect rework).

---

## Dependency & Execution Summary

- **Genuine edges (gate claiming)**: WP04→{WP01,WP03}; WP06→WP05; WP07→{WP01,WP05}; WP09→WP03. **All other WPs are claimable in parallel.**
- **Priority (scheduling, not edges)**: Recovery (WP01–WP04) → Atomicity (WP05–WP07) → Prevention (WP08–WP09) → Observability (WP10) → Hygiene (WP11–WP12).
- **MVP**: WP01 (closes #3334) is the minimal P0 increment; WP01+WP02+WP03+WP04 is the full recovery MVP (closes #3334/#3338 + heals the trigger).
- **Optional**: WP06 (droppable; dropping it removes SIGKILL-edge coverage).

---

## Requirements Coverage Summary

| Requirement ID | Covered By Work Package(s) |
|----------------|----------------------------|
| FR-001 | WP04 |
| FR-002 | WP01 |
| FR-003 | WP02 |
| FR-004 | WP06 (optional) |
| FR-005 | WP05 |
| FR-006 | WP08 |
| FR-007 | WP09 |
| FR-008 | WP03 |
| FR-009 | WP10 |
| FR-010 | WP11 |
| FR-011 | WP12 |
| FR-012 | WP01 |
| NFR-001 | WP01 |
| NFR-002 | WP01, WP03, WP04 |
| NFR-003 | WP05 |
| NFR-004 | WP03 |
| NFR-005 | WP07 |
| C-001 | all (sequencing) |
| C-002 | WP09 |
| C-003 | all (quality gates) |
| C-004 | WP03, WP04, WP06 |

---

## Subtask Index (Reference)

| Subtask ID | Summary | Work Package | Priority | Parallel? |
|------------|---------|--------------|----------|-----------|
| T001 | #3334 red-first regression | WP01 | P0 | No |
| T002 | Preserve schema_version on abort | WP01 | P0 | No |
| T005 | SAFE `--dry-run` predicate | WP02 | P0 | No |
| T007 | Raw-text dup-key detector module | WP03 | P1 | No |
| T009 | Repair via mission_state framework | WP03 | P1 | No |
| T012 | Recovery composition wiring | WP04 | P1 | No |
| T015 | Report-on-abort (keep results) | WP05 | P1 | No |
| T018 | Corpus staging-promote | WP06 | P2 | No |
| T021 | Reducer-integrity fixture+assert | WP07 | P1 | No |
| T023 | Retire `set_scalar` | WP08 | P2 | No |
| T025 | Legible DuplicateKeyError | WP09 | P2 | No |
| T027 | Unify dry-run detector | WP10 | P2 | No |
| T029 | Remediation body in `--json` | WP11 | P3 | Yes |
| T031 | Mission-create checkout restore | WP12 | P3 | Yes |
