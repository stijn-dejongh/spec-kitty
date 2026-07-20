# Mission Specification: Runtime-State Corpus Cutover

**Mission Branch**: `feat/runtime-state-corpus-cutover`
**Created**: 2026-07-20
**Status**: Draft
**Input**: Follow-up to #2684 / PR #2817 — issue #2816. Complete the deferred runtime-state
corpus cutover: make event-log authority unconditional and retire the phase-1 dual-write toggle,
per the strict migration contract `backfill → verify(FAIL-CLOSED) → flip reader+writer → delete
fallbacks → reduce`.

## Context *(why this mission exists)*

Mission #2684 evicted runtime-mutable work-package state (`shell_pid`, subtask completion,
activity-log notes, `tracker_refs`, `agent`/`assignee`, review-cycle fields) into one off-axis
`InnerStateChanged` event and read it back from the reduced status snapshot — **but shipped it as
dual-write behind an off-by-default flag** (`_phase1_snapshot_authority_active`, keyed on
`meta.json` `status_phase`). With the flag OFF (the production default), the legacy WP-file
frontmatter / `tasks.md` checkboxes remain the live authority and every runtime write hits **both**
surfaces. The corpus was never migrated and the flag was never flipped. Until that lands, #2684's
headline outcome — *stop writing WP-file runtime state* — holds only at `status_phase:1`.

This mission runs the deferred cutover as a **real production-default migration** (staged
backfill + fail-closed verify + an upgrade path for existing deployments), not a code tidy. The
governing contract is `kitty-specs/wp-runtime-state-eviction-01KXWN13/contracts/migration.md`; the
ADR of record is `docs/adr/3.x/2026-07-19-1-wp-runtime-state-event-log-eviction-via-innerstatechanged.md`.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Operator runs a safe, fail-closed corpus cutover (Priority: P1)

An operator (or the upgrade path acting on their behalf) needs to migrate every mission's
frontmatter/checkbox runtime state into the event log and only then switch that mission to
snapshot-authority. The migration must be observable (dry-run first), must prove parity before it
flips anything, and must **refuse to flip** any mission whose backfill/verify has not passed.

**Why this priority**: This is the load-bearing safety mechanism. Flipping a mission to
snapshot-authority before its legacy state is seeded as events means a WP with frontmatter-only
runtime state reduces to `{}` → `None` = **silent data loss**. Everything else depends on this
gate existing and being fail-closed.

**Independent Test**: On a corpus with legacy frontmatter runtime state, run the cutover CLI in
dry-run (reports would-seed counts, writes nothing), then for real: it seeds events, verifies
count+value parity against the old reader, and only flips missions that passed. Inject a corrupt
seed → the command aborts before any flip and leaves `status_phase` unchanged.

**Acceptance Scenarios**:

1. **Given** a mission carrying `shell_pid`/`agent`/`tracker_refs`/subtask completion only in the
   WP files, **When** the operator runs `spec-kitty migrate backfill-runtime-state --dry-run`,
   **Then** the command reports the seed counts per mission and writes nothing (no events, no flip).
2. **Given** the same corpus, **When** the operator runs the cutover for real, **Then** the reduced
   snapshot for every WP equals the old frontmatter/checkbox reader by count and value, and only
   then is `status_phase` set to the snapshot-authority value.
3. **Given** a mission whose backfill would produce a snapshot that diverges from the old reader
   (fault-injected corrupt/conflicting seed), **When** the cutover runs, **Then** it aborts
   fail-closed **before** flipping that mission and reports the mismatch; `status_phase` is untouched.
4. **Given** a mission already migrated, **When** the cutover is re-run, **Then** it seeds nothing
   (idempotent) and the flip is a no-op.

---

### User Story 2 - Event log is the unconditional authority (Priority: P1)

After cutover the reduced snapshot is the authority for WP runtime state everywhere — the phase-1
flag and its flag-OFF (dual-write / frontmatter-authority) branch no longer exist. A runtime
transition writes to the event log only; it never mutates `tasks/WP##.md`.

**Why this priority**: This is the mission's headline outcome and the reason #2684 was undertaken.
While the flag exists, the production default is still the legacy path, so the eviction is not
actually in effect.

**Independent Test**: Grep proves `_phase1_snapshot_authority_active` and its facade export are
gone. Drive a runtime transition (claim / move-task / mark-status) and assert the WP file is
byte-identical before and after, while the event log gains the event and the snapshot reflects it.

**Acceptance Scenarios**:

1. **Given** the cutover is complete, **When** any of the ~10 read/write sites resolves WP runtime
   state, **Then** it reads the snapshot / writes an event only — there is no flag branch to select
   the legacy path.
2. **Given** a claimed WP, **When** its `shell_pid`/`agent`/`assignee`/`tracker_refs`/subtask/review
   state changes, **Then** `tasks/WP##.md` is byte-stable and the change is visible only via the
   snapshot.
3. **Given** the codebase after this mission, **When** the predicate `_phase1_snapshot_authority_active`
   is searched for (source and status facade `__all__`), **Then** there are zero occurrences.

---

### User Story 3 - Existing deployments migrate safely on upgrade (Priority: P2)

A user upgrading an existing Spec Kitty project must have their corpus backfilled+verified as part
of `spec-kitty upgrade`, so the unconditional cutover does not strand their un-migrated on-disk WP
state. A fresh install with no corpus is a no-op.

**Why this priority**: A big-bang production-default flip without an upgrade migration would break
every existing deployment on the first runtime read after upgrade. This makes the cutover shippable.

**Independent Test**: On a fixture project with legacy runtime state, run the upgrade sequence and
confirm the corpus is backfilled + verified idempotently. On a fresh project (no `kitty-specs/` or
no legacy state), confirm the migration is a no-op. On a corpus that fails verify, confirm the
upgrade migration aborts with an actionable operator message and does not leave a partial flip.

**Acceptance Scenarios**:

1. **Given** a legacy deployment, **When** `spec-kitty upgrade` runs, **Then** the runtime-state
   backfill+verify migration runs (sequenced like the charter.yaml fold) and the corpus is migrated.
2. **Given** a fresh install, **When** `spec-kitty upgrade` runs, **Then** the runtime-state
   migration detects no corpus / no legacy state and no-ops.
3. **Given** an upgrade run whose verify fails for some mission, **When** the migration executes,
   **Then** it aborts that step fail-closed with a message naming the mismatch and does not flip.

---

### User Story 4 - Single-authority invariant is enforced with no exceptions (Priority: P2)

The `#2093` authority invariant test must forbid **any** frontmatter authority read for runtime
state, with an **empty** tolerated-gate set (the flag it tolerated is gone). The two remaining
ungated bypass readers documented in #2817's allow-list are routed onto the snapshot seam so no
split-brain reader survives.

**Why this priority**: The whole point of a single canonical authority is defeated if a stray
reader still resolves frontmatter after the flip. This closes the #2093 debt and prevents
regression.

**Independent Test**: `tests/architectural/test_2093_authority_invariant.py` passes with an empty
tolerated set. The two bypass readers (`tasks_move_task.py` ownership read; `workflow_cores.py`
review-status read) resolve via the snapshot accessor; a reintroduced frontmatter authority read
trips the invariant red.

**Acceptance Scenarios**:

1. **Given** the cutover is complete, **When** the #2093 invariant runs, **Then** the
   tolerated-fallback set is empty and the test passes.
2. **Given** `tasks_move_task.py` and `workflow_cores.py`, **When** they read `current_agent`/
   `shell_pid`/`review_status`/`review_feedback`, **Then** they resolve from the snapshot seam,
   not `extract_scalar(front, ...)`.
3. **Given** a hypothetical new frontmatter authority read, **When** the invariant runs, **Then**
   it fails (the guard is non-vacuous).

---

### User Story 5 - Post-cutover reduction of inert fields (Priority: P3, optional)

After the flip, the `wp_metadata` fields that fed the retired legacy path and the cosmetic
`WP_FIELD_ORDER` slots are inert. Reducing them (IC-08) is a bounded cleanup that is safe only
post-cutover and is not a gate on mission completion.

**Why this priority**: Pure hygiene with no behavioural consequence. Explicitly deferrable to a
follow-up so it never blocks the load-bearing cutover.

**Independent Test**: With the reduction applied, the inert fields are gone and no reader
references them; the full suite stays green. If deferred, the mission still completes on US1–US4.

**Acceptance Scenarios**:

1. **Given** the cutover is complete, **When** the inert `wp_metadata` fields / `WP_FIELD_ORDER`
   slots are removed, **Then** no live reader references them and the suite is green.

---

### Edge Cases

- **A WP that was never claimed** carries no claim anchor; its runtime seeds are skipped (a
  never-claimed WP cannot honestly carry completed subtasks). Backfill must warn, not fail.
- **A mission with no `kitty-specs/` or no `tasks/` directory** (fresh install) → backfill skips
  cleanly; upgrade migration no-ops.
- **`status_phase` hand-flipped to the authority value before backfill runs** — there is no
  production writer for `status_phase` today; the cutover CLI must be the only path that flips it,
  and must refuse to flip a mission whose verify has not passed (no hand-flip footgun).
- **Strip-before-verify** — verify against the *un-stripped* frontmatter; if the frontmatter key a
  snapshot slot depends on has already been stripped, fail closed (`MigrationOrderingError`).
- **Tampered same-slot seed annotation** masked by ULID tiebreak — the raw-stream conflict scan
  aborts fail-closed regardless of fold order.
- **A partially-migrated corpus** (some missions flipped, some not) must be a valid intermediate
  state: unflipped missions still read correctly (they simply have not been cut over yet), and the
  migration is resumable/idempotent.

## Requirements *(mandatory)*

### Functional Requirements

| ID | Title | User Story | Priority | Status |
|----|-------|------------|----------|--------|
| FR-001 | Backfill CLI entry point | As an operator, I want an invocable `migrate backfill-runtime-state` command with a `--dry-run` mode so that I can seed the corpus and preview counts before writing. | High | Open |
| FR-002 | Fail-closed verify | As an operator, I want the command to verify count+value parity of the reduced snapshot against the old frontmatter/checkbox reader and abort on any mismatch so that no mission is flipped on divergent state. | High | Open |
| FR-003 | Atomic verify-then-flip | As an operator, I want the command to flip `status_phase` to snapshot-authority **only** for missions whose backfill+verify passed, refusing to flip otherwise, so that there is no hand-flip data-loss footgun. | High | Open |
| FR-004 | Unconditional reader/writer cutover | As a maintainer, I want the flag-OFF (legacy/dual-write) branch removed across the ~10 read/write sites so that the reduced snapshot is always the authority and runtime writes are event-only. | High | Open |
| FR-005 | Delete the phase-1 predicate | As a maintainer, I want `_phase1_snapshot_authority_active` and its status-facade export deleted so that no runtime flag remains. | High | Open |
| FR-006 | Delete T037 legacy fallbacks | As a maintainer, I want the legacy fallbacks removed (`workflow_cores.py` verdict-field read fallback; `done_bookkeeping.py` done-evidence synthesis) now that backfill seeds those approvals as events. | High | Open |
| FR-007 | Route bypass readers onto the snapshot seam | As a maintainer, I want the two remaining ungated bypass readers (`tasks_move_task.py` ownership read; `workflow_cores.py` review-status read) resolved via the snapshot accessor so no split-brain reader survives. | High | Open |
| FR-008 | Harden the #2093 invariant | As a maintainer, I want `test_2093_authority_invariant.py` to run with an empty tolerated-gate set, forbidding any frontmatter authority read, so the single-authority guarantee is permanent. | High | Open |
| FR-009 | Reconcile the split test suite | As a maintainer, I want the flag-ON/flag-OFF split test suite reconciled — flag-OFF dual-write tests deleted or re-pointed, flag-ON assertions made unconditional — so the suite reflects the single end-state. | High | Open |
| FR-010 | Upgrade-path migration | As an upgrading user, I want the runtime-state backfill+verify to run as a sequenced `spec-kitty upgrade` migration (idempotent; no-op on fresh installs; fail-closed on verify failure) so my corpus migrates safely. | High | Open |
| FR-011 | IC-08 inert-field reduction | As a maintainer, I want the now-inert `wp_metadata` fields and cosmetic `WP_FIELD_ORDER` slots reduced, safe only post-cutover, so the model carries no dead runtime slots. | Low (optional/deferrable) | Open |

### Non-Functional Requirements

| ID | Title | Requirement | Category | Priority | Status |
|----|-------|-------------|----------|----------|--------|
| NFR-001 | Zero silent data loss | Any count or value parity mismatch (including a fault-injected corrupt/conflicting seed) aborts before the flip; **zero** tolerated mismatches; `status_phase` never changes on a failed verify. | Reliability | High | Open |
| NFR-002 | Idempotency | Re-running backfill mints byte-identical seed ids and seeds nothing on a second run; the upgrade migration is a no-op when the corpus is already migrated. | Reliability | High | Open |
| NFR-003 | WP-file byte-stability | After cutover, a runtime-state transition writes zero bytes to `tasks/WP##.md`; the file is byte-identical before and after (the #2684 AC-5 outcome, now unconditional). | Correctness | High | Open |
| NFR-004 | Suite green with no suppression | The full `tests/architectural/` suite (run per-file) and the `status` test suite pass on the branch; `ruff` and `mypy` report zero issues with no new blanket `# noqa` / `# type: ignore` / per-file ignores. | Quality | High | Open |
| NFR-005 | Upgrade abort safety | An upgrade whose verify fails for any mission aborts that migration step with an operator-actionable message naming the mismatch and leaves the deployment on a consistent (non-partially-flipped) state. | Reliability | High | Open |
| NFR-006 | Backfill performance | Corpus backfill+verify is linear in the number of missions and completes within a few seconds per mission on the dogfood corpus; it performs no network I/O. | Performance | Medium | Open |

### Constraints

| ID | Title | Constraint | Category | Priority | Status |
|----|-------|------------|----------|----------|--------|
| C-001 | Strict contract order | The migration MUST follow `backfill → verify(FAIL-CLOSED) → flip reader+writer → delete fallbacks → reduce`; no step may precede its predecessor (deleting a fallback before backfill is wired+verified strands legacy corpora). | Technical | High | Open |
| C-002 | Big-bang production default | The end-state is a genuine unconditional flip: the predicate is **deleted**, not merely defaulted ON; no residual runtime toggle remains. | Technical | High | Open |
| C-003 | Canonical write target | Backfill resolves its write target via `canonicalize_feature_dir`, never `Path.cwd()` (C-003 / #2647). | Technical | High | Open |
| C-004 | Lane-mirror out of scope | `_legacy_lane_mirror_enabled` is retained — the `lane` field is still frontmatter-authored, so evicting it is a separate concern deferred to its own follow-up. | Technical | Medium | Open |
| C-005 | Honesty bound (no-data-loss) | "No data loss" is asserted against count+value parity of the reduced snapshot, not temporal fidelity: backfilled subtask timestamps are clamped and seed ULIDs are content-namespaced. Holds only because no consumer reads subtask-completion time or relies on seed-ULID chronological order — asserted as a precondition. | Technical | Medium | Open |
| C-006 | No dead-symbol / arch-gate drift | Symbol-allowlist and arch-count gates (`test_no_dead_symbols.py` content-hash pins; `test_2093` reader-module set) must be updated in-mission to the post-cutover form, not suppressed. | Technical | Medium | Open |

### Key Entities

- **Reduced status snapshot**: the deterministic event→snapshot projection; the sole authority for
  WP runtime state after cutover.
- **`InnerStateChanged` seed events**: deterministic, content-namespaced-ULID seed annotations (+ a
  seed `planned→claimed` transition for claim state) reconstructing pre-eviction frontmatter/checkbox
  state.
- **`LegacyWPRuntime` (old reader)**: the pre-eviction frontmatter/checkbox per-WP view — the ground
  truth verify compares the snapshot against.
- **Phase-1 predicate (`_phase1_snapshot_authority_active`)**: the dual-write flag, keyed on
  `meta.json` `status_phase`; to be deleted.
- **`status_phase` (meta.json)**: the per-mission cutover marker the CLI flips atomically after a
  passing verify (the only writer of this field).
- **Bypass readers (`tasks_move_task.py`, `workflow_cores.py`)**: the two ungated frontmatter
  authority reads (#2093 debt) to be routed onto the snapshot seam.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of corpus missions are backfilled + verified with **zero** parity mismatches
  before any `status_phase` flip; a fault-injected corrupt seed aborts the run before any flip.
- **SC-002**: `_phase1_snapshot_authority_active` and its facade export have **zero** occurrences in
  the source tree after this mission.
- **SC-003**: `tests/architectural/test_2093_authority_invariant.py` passes with an **empty**
  tolerated-gate set and fails if a frontmatter authority read is reintroduced.
- **SC-004**: A runtime-state transition writes **0 bytes** to `tasks/WP##.md` (byte-identical
  before/after) with the flag removed.
- **SC-005**: `spec-kitty upgrade` migrates a legacy corpus idempotently (second run seeds nothing)
  and no-ops on a fresh install; a verify failure aborts the step with an actionable message.
- **SC-006**: The full `tests/architectural/` suite (per-file) and the `status` suite are green on
  the branch; `ruff` + `mypy` clean with no new suppressions.

## Assumptions

- **IC-08 (FR-011) is optional/deferrable** — the mission's Definition of Done rests on US1–US4
  (FR-001–FR-010); IC-08 may split to a follow-up if it grows.
- **`_legacy_lane_mirror_enabled` is kept** (C-004); evicting the frontmatter-authored `lane` field
  is a separate follow-up, out of scope here.
- **The upgrade migration auto-runs** backfill+verify (fail-closed) as a sequenced upgrade step,
  mirroring the charter.yaml fold; it does not require a separate operator opt-in.
- **Not a DIRECTIVE_035 bulk edit** — collapsing the flag branches is a heterogeneous per-site
  refactor (each call site collapses differently), not a mechanical token rename, so no
  `occurrence_map.yaml` is required. (Re-evaluated at plan if the flip proves mechanically uniform.)
- **The WP03 backfill library is complete and correct** (seed backfill + fail-closed verify that
  catches value tampering regardless of ULID fold order); this mission wires + invokes it, and does
  not re-derive it.
