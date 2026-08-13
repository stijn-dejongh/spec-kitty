# Mission Specification: Upgrade/migration atomicity & recoverability

**Mission Branch**: `spec/upgrade-atomicity-recovery`
**Mission ID**: `01KZWSHCEEBBEXZNYGXBB1QFQF` (`upgrade-atomicity-recovery-01KZWSHC`)
**Created**: 2026-08-13
**Status**: Draft
**Tracker**: Epic [#3347](https://github.com/Priivacy-ai/spec-kitty/issues/3347) (Upgrade/migration atomicity & recoverability) · root trigger [#3372](https://github.com/Priivacy-ai/spec-kitty/issues/3372) (under epic [#3044](https://github.com/Priivacy-ai/spec-kitty/issues/3044), review-artifact integrity)
**Milestone**: 3.2.x

## Debrief — why this mission exists

The cluster is dangerous because four bugs **interlock into a trap** with no self-service escape:

1. A review cycle writes the `review_feedback` key into an artifact's YAML frontmatter **twice** — first `''`, then a real path — producing a **duplicate-key, invalid-YAML** artifact (**#3372**, root trigger).
2. `spec-kitty upgrade` later fails to parse that artifact; `runtime_state_backfill` aborts **mid-migration**, having already mutated 22 `meta.json` + 16 `status.events.jsonl`, and **says nothing** about the partial write (**#3335**, non-atomic + silent).
3. The failed upgrade **deletes `schema_version`**, and `upgrade` — the *only* repair command — is **gated behind exactly the `schema_version` its own failure destroyed** (**#3334**, P0 release-blocker).
4. The diagnostic the failure recommends is **itself gated behind the failed migration** (**#3338**, circular).

The governing principle is **"make failures survivable before you make them rare."** Restore the escape hatch first (recovery), then stop making it worse (atomicity), then kill the trigger (prevention), then restore trust in the preview (observability). Fixing the trigger or atomicity *first* leaves any already-wedged project stranded.

> ⚠️ Several code-grounded claims below (exact write-path, `schema_version` gating, dry-run serialization) are drawn from field reports on the linked issues and a first-pass code scan. A **post-spec research & corroboration squad** grounds each in the current source and architecture before planning; findings feed `research.md` and may adjust requirement wording. Requirements carrying residual uncertainty are marked `[NEEDS CORROBORATION]`.

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Restore the escape hatch: a wedged project can recover (Priority: P1)

An operator whose `upgrade` already failed part-way — `schema_version` gone, migration half-applied — must be able to **run a command that repairs the project**, and the diagnostic that explains the failure must be **reachable without first completing the migration that failed**. Today both the repair and the diagnostic are gated behind the destroyed/failed state, so a non-VCS or fresh-clone project has no forward path.

**Why this priority**: This is the release-blocker (#3334 is P0, expected to red mainline per ADR 2026-07-17-1). Until recovery exists, no other fix helps a project that is *already* wedged. Ship first.

**Independent Test**: Construct a project in the wedged state (missing/damaged `schema_version` + half-applied migration), run the repair command, and assert the project returns to a consistent, upgradable state — and that the recommended diagnostic runs against the wedged project and reports the real cause.

**Acceptance Scenarios**:
1. **Given** a project whose `upgrade` aborted and deleted `schema_version`, **When** the operator invokes the repair path, **Then** the project is restored to a consistent schema state and a subsequent `upgrade` proceeds — with no manual `git` intervention required.
2. **Given** a failed migration whose error recommends a diagnostic, **When** the operator runs that diagnostic, **Then** it executes and reports the cause **without** being gated behind the migration that failed.
3. **Given** the fix, **When** the #3334 issue-pinned red-first reproduction test runs on the pre-fix tree, **Then** it fails (honest red); **When** it runs post-fix, **Then** it passes.

---

### User Story 2 — Atomic, honestly-reported migration (Priority: P1)

`runtime_state_backfill` (and any comparable bulk-cutover migration) must be **all-or-nothing**: either every mission verifies and the cutover commits once, or nothing is mutated and the abort **explicitly reports** the set it would have touched. An operator who trusts the step's stated atomicity must never be silently left with a partial write.

**Why this priority**: Stops the migration from creating the half-migrated, silent state that makes the wedge (US1) so costly. Only fully safe *after* US1 exists, so a mid-run abort can no longer strand.

**Independent Test**: Run the backfill over a fixture set where one mission fails verification; assert **zero** missions were mutated (staged-and-committed-once), or — if the design chooses report-on-abort — that the partial set is named explicitly in output and is rollback-recoverable.

**Acceptance Scenarios**:
1. **Given** N missions where mission K fails verification, **When** the backfill runs, **Then** no `meta.json`/`status.events.jsonl` is left mutated by the aborted run (atomic), **or** the abort output enumerates every file it wrote.
2. **Given** a successful run, **When** it completes, **Then** all N missions are cut over and the result is reported truthfully (count matches reality).

---

### User Story 3 — Kill the trigger: no duplicate-key artifacts (Priority: P1)

A review cycle must write `review_feedback` **idempotently** (set, never append), the frontmatter boundary must **fail closed** on a duplicate mapping key rather than silently taking the last value, and the toolkit must be able to **detect and repair** artifacts already carrying the malformed dual key — so a project can be healed *before* an upgrade trips over it.

**Why this priority**: Eliminates the root cause. The detect/repair half also directly serves US1 (heal-before-upgrade). Prevention lands after recovery + atomicity so it never masks an unrecovered project.

**Independent Test**: Run two review cycles on the same WP and assert exactly one `review_feedback` key; feed a duplicate-key artifact to the frontmatter reader/writer and assert a legible fail-closed error; run the doctor scan over a fixture with malformed artifacts and assert detection + safe repair.

**Acceptance Scenarios**:
1. **Given** a WP that already has `review_feedback`, **When** a second review cycle writes feedback, **Then** the key is updated in place (exactly one key remains).
2. **Given** an artifact with a duplicate `review_feedback` key, **When** it passes through `write_frontmatter`/`read_frontmatter`/`validate_frontmatter`, **Then** the operation refuses/raises with a legible message rather than persisting or silently coercing.
3. **Given** a project containing malformed artifacts, **When** the doctor scan runs, **Then** it lists them and offers a safe repair that yields valid YAML.

---

### User Story 4 — Honest upgrade preview (Priority: P2)

`spec-kitty upgrade --dry-run` must report the **real** pending set. Today it can report nothing pending while the real run applies 19 migrations (`pending_migrations` serializing as `null`), so an operator cannot see blast radius before committing.

**Why this priority**: Not on the wedge path, but it is what lets an operator *trust the preview* after US1–US3. Restores confidence in the safe inspection step.

**Independent Test**: On a project with known-pending migrations, run `--dry-run` and assert the reported pending set equals what a real run applies.

**Acceptance Scenarios**:
1. **Given** a project with M pending migrations, **When** `upgrade --dry-run` runs, **Then** it reports exactly those M (never `null`/empty when work is pending).

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
| FR-001 | Self-recoverable upgrade | As an operator, I want `upgrade` (or a repair path) to run even when `schema_version` is missing/damaged so that a failed upgrade is recoverable without manual git. `[NEEDS CORROBORATION]` exact gating point. | High | Open |
| FR-002 | Preserve `schema_version` on failure | As an operator, I want a failed upgrade to **not** delete `schema_version` so that the repair command is never gated behind destroyed state. | High | Open |
| FR-003 | Ungate the recommended diagnostic | As an operator, I want the failure-recommended diagnostic reachable without completing the failed migration. | High | Open |
| FR-004 | Atomic bulk cutover | As an operator, I want `runtime_state_backfill` to commit once all missions verify, or mutate nothing on abort. | High | Open |
| FR-005 | Honest partial-write reporting | As an operator, I want any non-atomic abort to enumerate every file it wrote. | High | Open |
| FR-006 | Idempotent `review_feedback` write | As a reviewer, I want feedback writes to update the key in place so no duplicate key is ever produced. | High | Open |
| FR-007 | Fail-closed duplicate-key guard | As the toolkit, I want the frontmatter boundary to reject/raise on duplicate mapping keys rather than silently coerce. | High | Open |
| FR-008 | Detect & repair malformed artifacts | As an operator, I want a doctor-surfaced scan that finds and safely repairs duplicate-key artifacts before upgrade. | High | Open |
| FR-009 | Truthful `--dry-run` | As an operator, I want `upgrade --dry-run` to report the real pending migration set. | Medium | Open |
| FR-010 | Remediation body survives `--json` | As an agent, I want the charter-pack-invalid remediation body present in mission-create `--json` output. | Medium | Open |
| FR-011 | Mission-create failure restores checkout | As an operator, I want a failed mission-create to restore my branch/checkout and leave no orphan branch. | Medium | Open |

### Non-Functional Requirements

| ID | Title | Requirement | Category | Priority | Status |
|----|-------|-------------|----------|----------|--------|
| NFR-001 | P0 red-first proof | #3334 lands with an issue-pinned `@pytest.mark.regression` reproduction that is red pre-fix, green post-fix (ADR 2026-07-17-1). | Reliability | High | Open |
| NFR-002 | No data loss in recovery | The repair path must never discard recorded mission results/events; recovery is non-destructive. | Reliability | High | Open |
| NFR-003 | Atomicity is observable | Every migration abort emits a truthful, machine-readable account of what was/wasn't written. | Reliability | High | Open |
| NFR-004 | Repair is itself atomic | The detect/repair tool must not partially repair (no recursion of the US2 anti-pattern). | Reliability | Medium | Open |

### Constraints

| ID | Title | Constraint | Category | Priority | Status |
|----|-------|------------|----------|----------|--------|
| C-001 | Ship recovery before prevention | Remediation lands in phase order US1 → US2 → US3 → US4 → US5; prevention must not precede recovery. | Technical | High | Open |
| C-002 | Canonical frontmatter boundary | The duplicate-key guard lives in the canonical `src/specify_cli/frontmatter.py` boundary, not ad-hoc per-caller checks. | Technical | High | Open |
| C-003 | No new legacy terminology / suppressions | New code passes ruff+mypy with zero suppressions; terminology guard green. | Technical | Medium | Open |

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
