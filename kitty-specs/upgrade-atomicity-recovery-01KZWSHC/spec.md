# Mission Specification: Upgrade/migration atomicity & recoverability

**Mission Branch**: `spec/upgrade-atomicity-recovery`
**Mission ID**: `01KZWSHCEEBBEXZNYGXBB1QFQF` (`upgrade-atomicity-recovery-01KZWSHC`)
**Created**: 2026-08-13
**Status**: Draft
**Tracker**: Epic [#3347](https://github.com/Priivacy-ai/spec-kitty/issues/3347) (Upgrade/migration atomicity & recoverability) · root trigger [#3372](https://github.com/Priivacy-ai/spec-kitty/issues/3372) (under epic [#3044](https://github.com/Priivacy-ai/spec-kitty/issues/3044), review-artifact integrity)
**Milestone**: 3.2.x

## Debrief — why this mission exists

The cluster is dangerous because the bugs **interlock into a trap** with no self-service escape:

1. A **legacy** write-path (now retired) once wrote the `review_feedback` key into an artifact's YAML frontmatter **twice** — first `''`, then a real path — producing a **duplicate-key, invalid-YAML** artifact that still exists on disk in affected projects (**#3372**, root trigger — see correction C below).
2. `spec-kitty upgrade` fails to parse that artifact; `runtime_state_backfill` aborts **mid-migration**, having already mutated missions one-by-one (field report: 22 `meta.json` + 16 `status.events.jsonl`), and **says nothing** about the partial write (**#3335**, non-atomic + silent).
3. On that failure `schema_version` is **not restored** (it is omitted on save-rewrite and only re-stamped on success), so a re-run re-detects the project as legacy and **re-hits the same failing migration** on the still-invalid artifact (**#3334**, P0 release-blocker — see correction A).
4. The **diagnostic** the failure recommends (`spec-kitty migrate backfill-runtime-state --dry-run`) is **itself gated behind the failed migration** (hard block, exit 4) — the true "gated behind destroyed state" bug (**#3338**, circular).

The governing principle is **"make failures survivable before you make them rare."** Restore the escape hatch first (recovery), then stop making it worse (atomicity), then harden against the trigger (prevention), then restore trust in the preview (observability). Fixing atomicity or the guard *first* leaves any already-wedged project stranded.

> ✅ **Corroborated 2026-08-13** — a post-spec research squad grounded every claim in current source (see `research.md`). It **corrected three field-report root causes**; those corrections are folded in below:
> - **(A) `upgrade` is NOT schema-gated.** It is exempt in the CLI gate / classified SAFE. FR-001 targets *restoration + non-recurrence*, not "ungate upgrade." The `schema_version` loss is a save/stamp **ordering** bug (`upgrade/runner.py:181-190`), not a `del`.
> - **(B) The dry-run `null` is not reproducible on current source** (it serializes `[]`). The real FR-009 defect is **two divergent pending-set computations** (preview planner vs real `MigrationRegistry.get_applicable`).
> - **(C) The inline dual-write is legacy/unreachable.** The canonical path writes a `review-cycle://` pointer, not an inline key, and the frontmatter read boundary **already fails closed** on duplicate keys. US3 is therefore **guard-hardening + detect/repair of legacy artifacts**, not a live-writer fix.
> Two user stories must **conform to existing ADRs**: US2 → `2026-04-17-2` (staging-promote atomicity); US1 → `2026-05-10-1` (deterministic non-destructive repair). Ledger epic **#2933** is the missing recovery substrate (FR-005/NFR-003 coupling). Ordering (C-001) is a **policy** constraint enforced by WP dependency edges, not code-forced.

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Restore the escape hatch: a wedged project can recover (Priority: P1)

An operator whose `upgrade` already failed part-way — `schema_version` unrestored, migration half-applied — must be able to **run a command that repairs the project**, and the diagnostic that explains the failure must be **reachable without first completing the migration that failed**. Corrected root cause (per `research.md`): `upgrade` itself already runs on legacy projects; the wedge is that (a) `schema_version` is not re-stamped on the failure path so a re-run re-detects legacy and **re-hits the same failing migration**, and (b) the recommended **diagnostic** is hard-blocked (exit 4) because its subcommand path is not classified SAFE. Recovery must conform to the deterministic non-destructive repair ADR (`2026-05-10-1`).

**Why this priority**: This is the release-blocker (#3334 is P0, expected to red mainline per ADR 2026-07-17-1). Until recovery exists, no other fix helps a project that is *already* wedged. Ship first.

**Independent Test**: Construct a project in the wedged state (missing/damaged `schema_version` + half-applied migration), run the repair command, and assert the project returns to a consistent, upgradable state — and that the recommended diagnostic runs against the wedged project and reports the real cause.

**Acceptance Scenarios**:
1. **Given** a project whose `upgrade` aborted and deleted `schema_version`, **When** the operator invokes the repair path, **Then** the project is restored to a consistent schema state and a subsequent `upgrade` proceeds — with no manual `git` intervention required.
2. **Given** a failed migration whose error recommends a diagnostic, **When** the operator runs that diagnostic, **Then** it executes and reports the cause **without** being gated behind the migration that failed.
3. **Given** the fix, **When** the #3334 issue-pinned red-first reproduction test runs on the pre-fix tree, **Then** it fails (honest red); **When** it runs post-fix, **Then** it passes. The reproduction MUST force the mid-loop abort via a **synthetic always-failing migration** (independent of the duplicate-key trigger and of FR-008 repair), so the P0 proof isolates the save/stamp ordering defect and cannot be masked by artifact healing.
4. **Given** a **legacy / lower-schema** project (`schema_version` absent or `< REQUIRED`), **When** its migration aborts, **Then** the on-disk `schema_version` is NOT advanced to the target (invariant: a failed migration never advances schema).
5. **Given** a wedged project **not under version control**, **When** the recovery path runs, **Then** it repairs on-disk without requiring a git checkpoint and returns the project to an upgradable state.
6. **Given** `schema_version` restored, **When** `upgrade` is re-run (FR-012), **Then** it applies **zero** migrations (safe no-op/resume), not a redundant re-application.

---

### User Story 2 — Atomic, honestly-reported migration (Priority: P1)

`runtime_state_backfill` (and any comparable bulk-cutover migration) must never silently leave a partial write. Corrected framing (per `research.md`): the migration is **intentionally per-mission atomic** (research D-03: no cross-mission transaction primitive), so full corpus rollback (FR-004) would *undo a documented design decision* and is the higher-risk path. The **primary** requirement is **report-on-abort** (FR-005): the abort must enumerate every mission/file it wrote — the data is already collected and merely discarded today. Where true staging is pursued, it must **reuse the canonical staging-promote atomicity pattern** (ADR `2026-04-17-2`: stage → validate → `os.replace` promote → preserve `.failed/cause.yaml`), whose `cause.yaml` *is* the machine-readable partial-write account.

**Why this priority**: Stops the migration from creating the half-migrated, *silent* state that makes the wedge (US1) so costly. Meaningful only *after* US1 recovery exists, so a mid-run abort no longer strands.

**Independent Test**: Run the backfill over a fixture set where one mission fails verification; assert the abort output **enumerates every mission/file already written** and is rollback-recoverable (FR-005). If corpus staging is implemented, additionally assert **zero** missions remain mutated after abort (FR-004).

**Acceptance Scenarios**:
1. **Given** N missions where mission K fails verification, **When** the backfill runs, **Then** the abort output enumerates every mission/file already written (FR-005), **or** (if FR-004 staging ships) no `meta.json`/`status.events.jsonl` is left mutated (atomic).
2. **Given** a successful run, **When** it completes, **Then** all N missions are cut over and the result is reported truthfully (count matches reality).
3. **(NFR-005)** **Given** a half-applied backfill that was then recovered, **When** `reduce()` runs over the recovered `status.events.jsonl`, **Then** it yields the same snapshot as (pre-abort log ∪ committed cutover events) — no reducer divergence. Idempotency is guaranteed by `detect()`/`_mission_needs_cutover` skipping already-cut-over missions plus reducer `event_id` de-duplication; the #3334 regression additionally asserts a re-run appends **no** duplicate transitions.
4. **(SIGKILL — FR-004-only)** **Given** the backfill is killed mid-commit, **When** the process restarts, **Then** the corpus is recoverable. NOTE: this edge case is satisfied **only if FR-004 staging-promote ships**; FR-005 report-on-abort cannot cover a process that never returns. If FR-004 is deferred, durable cross-run/SIGKILL accounting is explicitly out of scope (deferred with ledger #2933). Recovery is **roll-forward** (a `detect()`-gated re-run completes remaining missions), not roll-back — which is why the #2933 ledger can be deferred.

---

### User Story 3 — Kill the trigger: no duplicate-key artifacts (Priority: P1)

Corrected framing (per `research.md`): the inline dual-write is **legacy and already retired** — the canonical path writes a `review-cycle://` pointer, not an inline key, and the frontmatter read boundary **already fails closed** on duplicate keys (ruamel raises `DuplicateKeyError`). So US3 is **guard-hardening + detect/repair of legacy artifacts on disk**, not a live-writer fix. Three parts: (FR-006) retire/fail-close the latent append-on-miss writer (`task_utils/support.py::set_scalar`, currently zero production callers) so the bug can't be reintroduced; (FR-007) make the existing fail-closed guard **legible** (name the duplicate key), pin `allow_duplicate_keys=False` under a regression test, and add a raw-text pre-parse scan feeding detect; (FR-008) build a **net-new** doctor scan/repair over `kitty-specs/**/*.md` that heals dual-key artifacts (keep-last non-empty policy) so a project can be repaired *before* upgrade trips over it.

**Why this priority**: Hardens against the root cause and cleans existing damage. The detect/repair half (FR-008) directly serves US1 (heal-before-upgrade) and should ship *with* the recovery bundle; the guard hardening (FR-006/007) lands after recovery + atomicity.

**Independent Test**: Assert no code path writes an inline `review_feedback` frontmatter key and `set_scalar` cannot append it; feed a duplicate-key artifact through `read_frontmatter`/`validate_frontmatter` and assert a legible error that names the key; run the doctor scan over a fixture of malformed artifacts and assert detection + safe, batch-atomic repair to valid YAML.

**Acceptance Scenarios**:
1. **Given** the current code, **When** any review cycle persists feedback, **Then** no inline `review_feedback` frontmatter key is produced (pointer-based), and the latent `set_scalar` append-on-miss path is retired or fails closed.
2. **Given** an artifact with a duplicate `review_feedback` key, **When** it passes through `read_frontmatter`/`validate_frontmatter`, **Then** it raises/reports a **legible** error naming the duplicate key (not a generic "invalid YAML"), and `allow_duplicate_keys=False` is pinned by a regression test.
3. **Given** a project containing malformed artifacts, **When** the doctor scan runs, **Then** it lists them and offers a safe, batch-atomic repair that yields valid YAML without discarding recorded state.

---

### User Story 4 — Honest upgrade preview (Priority: P2)

`spec-kitty upgrade --dry-run` must report the **real** pending set. Corrected root cause (per `research.md`): the reported `null` is not reproducible on current source (it serializes `[]`); the true defect is **two divergent computations** — the preview uses the compat-planner's `_pending_migrations_for` (gated on `BLOCK_PROJECT_MIGRATION`) while the real run selects via `MigrationRegistry.get_applicable`, and `_provision_missing_mission_type_activations` never runs in dry-run. So the preview can report `[]` while the real run applies migrations. The fix is to **drive the preview through the same planning path the real run uses**, not to patch the serializer.

**Why this priority**: Not on the wedge path, but it is what lets an operator *trust the preview* after US1–US3. Restores confidence in the safe inspection step.

**Independent Test**: On a project with known-pending migrations, run `--dry-run` and assert the reported pending set equals what a real run applies.

**Acceptance Scenarios**:
1. **Given** a project with M pending migrations, **When** `upgrade --dry-run` runs, **Then** it reports exactly those M (the preview path consults the same detector the real run uses; never empty when work is pending).

---

### User Story 5 — Mission-create & remediation-surface hygiene (Priority: P2)

Adjacent upgrade/mission-create rough edges that share the incident's surface: the `CHARTER_PACK_CONFIG_INVALID` remediation body must survive `--json` on `agent mission create` (#3337), and a failed mission-create must restore the operator's branch/checkout instead of stranding a half-created branch (#3339, coordinate with #3328).

**Why this priority**: Real but lower blast-radius; parallelizable and not on the critical recovery path.

**Independent Test**: Trigger each failure mode and assert the remediation body is present in `--json` output (#3337) and that a failed mission-create leaves the operator on their original branch with no orphan branch (#3339).

**Acceptance Scenarios**:
1. **Given** an invalid charter pack config, **When** `agent mission create --json` fails, **Then** the JSON envelope carries the remediation body.
2. **Given** a mission-create that fails after creating a branch, **When** it aborts, **Then** the operator's checkout and branch state are restored.

### Edge Cases

- A project **not** under version control reaches the wedged state (no `git` workaround) — US1 must still recover it.
- A duplicate key exists on an artifact the current writer no longer produces (legacy/interrupted path) — US3 detect/repair must still catch it.
- The backfill is interrupted by SIGKILL/power-loss mid-commit — US2 atomicity boundary must degrade to a recoverable, reported state.
- Multiple missions carry malformed artifacts — repair must be batch-safe and not itself partial (don't reintroduce the US2 anti-pattern in the repair tool).

## Requirements *(mandatory)*

### Functional Requirements

| ID | Title | User Story | Priority | Status |
|----|-------|------------|----------|--------|
| FR-001 | Non-recurring, self-recoverable upgrade *(composition)* | As an operator, I want end-to-end recovery — no new command unless proven necessary; recovery = FR-002 preservation + FR-008 artifact repair + FR-012 resumable re-run, wired so SC-001 holds with zero manual git. Adopts the non-destructive + deterministic **principles** of ADR `2026-05-10-1` and reuses its `migration/mission_state.py` repair machinery. Depends on FR-002 + FR-008. | High | Open |
| FR-002 | **Preserve** `schema_version` on failure | As an operator, I want `schema_version` on disk to **always reflect the schema the project actually satisfies** — a failed migration must NEVER advance it. Capture the pre-run value and restore it on abort (or prevent `_record_migration_result`→`save()` from erasing it); stamp `REQUIRED_SCHEMA_VERSION` only on success. **Do not** blanket-`finally`-stamp the target schema onto a failed/legacy project. Seam: `upgrade/runner.py:181-190,489`, `upgrade/metadata.py:188-210`. | High | Open |
| FR-003 | Ungate the recommended diagnostic | As an operator, I want `migrate backfill-runtime-state --dry-run` reachable when blocked. (Seam: register the subcommand path SAFE via a `--dry-run` predicate, `compat/safety.py`.) | High | Open |
| FR-005 | Honest partial-write reporting *(primary)* | As an operator, I want any non-atomic abort to enumerate every mission/file it wrote. (Data already collected in `_cutover_corpus` results, discarded at `apply():284-286`.) | High | Open |
| FR-004 | Corpus-atomic cutover *(higher-risk, optional)* | As an operator, I want `runtime_state_backfill` to mutate nothing on abort — via the staging-promote pattern (ADR `2026-04-17-2`), not corpus rollback. `[NEEDS CORROBORATION]` vs the intentional per-mission design (D-03). | Medium | Open |
| FR-006 | Retire the latent append-on-miss writer | As the toolkit, I want `set_scalar` (zero prod callers) retired or fail-closed so no path can re-append an inline `review_feedback` key. | High | Open |
| FR-007 | Legible duplicate-key guard | As the toolkit, I want the (already fail-closed) frontmatter read boundary to raise a **legible** error naming the duplicate key, with `allow_duplicate_keys=False` pinned by a regression test. | High | Open |
| FR-008 | Detect & repair malformed artifacts | As an operator, I want a net-new doctor-surfaced scan that finds and safely (batch-atomically) repairs duplicate-key artifacts before upgrade. Ships with the US1 recovery bundle. | High | Open |
| FR-009 | Truthful `--dry-run` | As an operator, I want `upgrade --dry-run` to report the real pending set by driving the preview through the same detector the real run uses (`MigrationRegistry.get_applicable`), not the divergent planner path. | Medium | Open |
| FR-010 | Remediation body survives `--json` | As an agent, I want the charter-pack-invalid remediation body present in mission-create `--json` output. | Medium | Open |
| FR-011 | Mission-create failure restores checkout | As an operator, I want a failed mission-create to restore my branch/checkout and leave no orphan branch. | Medium | Open |
| FR-012 | Resumable-upgrade idempotency | As an operator, I want a re-run of `upgrade` after `schema_version` restoration to be a safe no-op/resume, not a redundant re-application. | High | Open |

### Non-Functional Requirements

| ID | Title | Requirement | Category | Priority | Status |
|----|-------|-------------|----------|----------|--------|
| NFR-001 | P0 red-first proof | #3334 lands with an issue-pinned `@pytest.mark.regression` reproduction that is red pre-fix, green post-fix (ADR 2026-07-17-1). | Reliability | High | Open |
| NFR-002 | No data loss in recovery | The repair path must never discard recorded mission results/events; recovery is non-destructive. | Reliability | High | Open |
| NFR-003 | Atomicity is observable | Every migration abort emits a truthful, machine-readable account of what was/wasn't written. | Reliability | High | Open |
| NFR-004 | Repair is itself atomic | The detect/repair tool must not partially repair (no recursion of the US2 anti-pattern). | Reliability | Medium | Open |
| NFR-005 | Event-log integrity after recovery | After any recovery/repair, `status.events.jsonl` remains append-only and reducer-deterministic (no reducer divergence from a half-applied backfill). | Reliability | High | Open |

### Constraints

| ID | Title | Constraint | Category | Priority | Status |
|----|-------|------------|----------|----------|--------|
| C-001 | Ship recovery before prevention | Phase order US1(+FR-008) → US2 → US3 → US4 → US5. This is a **policy** constraint (modules are disjoint / not code-forced) enforced by explicit WP dependency edges at finalize-tasks. | Technical | High | Open |
| C-002 | Canonical frontmatter boundary | The duplicate-key guard lives in the canonical `src/specify_cli/frontmatter.py` boundary, not ad-hoc per-caller checks. | Technical | High | Open |
| C-003 | No new legacy terminology / suppressions | New code passes ruff+mypy with zero suppressions; terminology guard green. | Technical | Medium | Open |
| C-004 | Conform to atomicity & repair ADRs | US2 reuses the staging-promote pattern (ADR `2026-04-17-2`); US1 conforms to deterministic non-destructive repair (ADR `2026-05-10-1`); FR-005/NFR-003 reconcile with the migration-ledger intent (epic #2933) or explicitly scope-defer it. | Technical | High | Open |

### Key Entities

- **`schema_version`**: the marker `upgrade` reads to decide applicability; destroying it wedges recovery (FR-002).
- **`review_feedback` frontmatter key**: the field whose duplicate write produces invalid YAML (FR-006/007).
- **`runtime_state_backfill` migration**: the bulk cutover that must become atomic (FR-004/005).
- **Mission artifact (`meta.json` / `status.events.jsonl` / WP `.md`)**: the files mutated by backfill and corrupted by the trigger.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A project in the wedged state (missing `schema_version` + half-applied migration) is recovered to an upgradable state by a documented command with **zero** manual git steps.
- **SC-002**: `runtime_state_backfill` over a fixture with one failing mission leaves **0** files mutated on abort (or reports 100% of the files it wrote).
- **SC-003**: Two consecutive review cycles on one WP yield **exactly one** `review_feedback` key; a duplicate-key artifact fails closed at the frontmatter boundary in 100% of read/write paths.
- **SC-004**: `upgrade --dry-run` reported pending set equals the real applied set in 100% of tested projects.
- **SC-005**: The #3334 red-first regression is red on the pre-fix tree and green post-fix, and the full cluster (#3334/#3335/#3336/#3337/#3338/#3339/#3372) is closed against evidence.
