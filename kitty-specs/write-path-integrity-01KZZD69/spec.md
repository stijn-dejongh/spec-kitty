# Mission Specification: Mission-Artifact Write-Path Integrity

**Mission Branch**: `mission/write-path-integrity`
**Created**: 2026-08-14
**Status**: Draft
**Input**: Fold #3371 (P0), #3372 (P1), #3373 (P2), and #3128 (structural boundary) into one write-path-integrity mission; prefer structural, design-aligned fixes over duct tape.

## Summary & Framing

Four tracker items share **one disease class**: *a write path emits a latent-malformed mission
artifact that a later bulk consumer detonates on.* The corpus already names this the
"ambient-location / write-path topology" cluster (#3129, 14 issues) and prescribes how fixes here
must land (`docs/plans/investigations/write-path-topology-root-cause.md`).

| Issue | Latent-malformed artifact | Detonates in | Roadmap home |
|-------|---------------------------|--------------|--------------|
| #3371 (P0) | PRIMARY `lanes.json` committed to the **coord** branch | lane allocator `git merge` → add/add | #2160 coord-artifact-authority |
| #3128 (structural) | *(the enabling gap)* no invariant compares invoking checkout vs declared workspace | any ambient-location write | #1878 / #3128 Option A |
| #3372 (P1) | duplicate-key YAML in a WP frontmatter (legacy corpora) | `spec-kitty upgrade` → uncaught `LegacyRuntimeReadError` | #3044 / #3347 |
| #3373 (P2) | *(no artifact yet)* triplicated topology/checkout primitives that **will** drift | a future one-copy correctness fix | #2624 (foundation for #3128) |

**Confirmed root cause of #3371** (git-proven): `implement.py::_commit_planning_artifacts_transaction`
(`src/specify_cli/cli/commands/implement.py:890-902`, the `placement_ref is not None` arm) commits the
whole planning batch **verbatim to `placement_ref.ref`**, which under coord topology is the coordination
branch — so a dirty PRIMARY `lanes.json` lands on coord (commit `c3d92a364` on
`kitty/mission-mission-a-p0-consistency-01KZWHY1` carries `implement.py:701`'s exact message and adds
only `lanes.json`). The partition helper that would prevent it (`_partition_files_for_commit`,
`implement.py:714`) is **dead on this path** — wired only into the legacy `else` branch. The lane then
branches from coord and merges the recorded `planning_commit_sha` (on `target_branch`, also carrying
`lanes.json`), and because `lanes.json` is absent at the merge-base, the merge is a guaranteed add/add
→ `PlanningCommitMergeConflictError` (`worktree_allocator.py:339-356`). This directly violates ADR
`2026-07-29-1` §3's disjointness assumption; the ADR itself flagged the upstream cause and deferred it
to #2160. A **second door** exists: finalize's `_stage_artifacts_in_coord_worktree`
(`commit_router.py:715-727`) still stages `tasks.md`/`lanes.json` into the coord worktree (test-pinned).

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Coord-topology missions can seed lanes without a manual reconcile (Priority: P1) — #3371

An operator creates a mission with coordination topology and a PR-bound `--start-branch`, runs
specify → plan → tasks → finalize, then `implement WP01`. Today lane allocation fails with an add/add
`lanes.json` conflict and requires an operator-granted manual coord←primary merge to recover. After
this mission, lane allocation succeeds because **no PRIMARY-partition artifact is ever committed to the
coordination branch** — restoring the disjointness invariant ADR `2026-07-29-1`'s allocator merge
already assumes.

**Why this priority**: P0 in the tracker — it blocks *all* implementation on any coord + pr-bound
mission and recovery is not self-service.

**Independent Test**: Reproduce mission `mission-a-p0-consistency`'s shape (coord topology, PR-bound
`--start-branch`), drive finalize + `implement WP01`, assert allocation succeeds and the coordination
branch tree contains zero PRIMARY-partition files.

**Acceptance Scenarios**:

1. **Given** a coord-topology mission on a PR-bound `--start-branch` whose planning artifacts (incl.
   `lanes.json`) are committed to `target_branch`, **When** `spec-kitty agent action implement WP01`
   allocates the lane worktree, **Then** the recorded-planning-commit merge is conflict-free and the
   lane worktree is created (no `PlanningCommitMergeConflictError`).
2. **Given** a coord-topology mission with a *dirty* uncommitted `lanes.json` at implement time,
   **When** `_ensure_planning_artifacts_committed_git` auto-commits it, **Then** the PRIMARY
   `lanes.json` is committed to the mission `target_branch`, and **never** to `placement_ref.ref`/the
   coordination branch.
3. **Given** finalize-tasks running under coord topology, **When** it commits its artifact batch,
   **Then** `tasks.md`/`lanes.json` (PRIMARY) are committed only to `target_branch` and are **not**
   staged into the coordination worktree.
4. **Given** any code path attempting to commit a PRIMARY-partition kind onto a coordination write
   surface, **When** the commit is attempted, **Then** it fails loud with a `PrimaryKindReachedCoord…`
   error rather than silently succeeding.

---

### User Story 2 — Mission-mutating commands refuse to write into a checkout the mission does not own (Priority: P1) — #3128

An agent (e.g. a compacted/resumed session) invokes a mission-mutating command from the wrong
checkout. Today nothing compares the invoking checkout against the mission's declared workspace, so the
write silently lands in the ambient location (the 2026-07-31 `spec-kitty-saas` incident). After this
mission, such a command **fails closed** with an actionable message.

**Why this priority**: This is the structural gap under the entire #3129 class — the sanctioned
near-term remedy (Option A / #3128). Closing it makes #3371's class of defect *detectable* even where
partition routing is not the vector.

**Independent Test**: Invoke a mission-mutating command from a foreign checkout (one the mission does
not own); assert it refuses (exit ≠ 0, legible error) instead of writing.

**Acceptance Scenarios**:

1. **Given** a mission whose declared workspace is checkout A, **When** a mission-mutating command is
   invoked from unrelated checkout B, **Then** the command refuses with an actionable error naming the
   expected vs actual checkout, and performs no write.
2. **Given** the mission's own legitimate lane/coord worktrees (owned by the mission), **When** the
   same command is invoked from them, **Then** it proceeds normally (no false refusal).
3. **Given** the comparison data, **When** the check runs, **Then** it compares against
   already-computed mission/lane metadata (no new bookkeeping, no live re-derivation) and adds no
   protected-branch-independent git calls beyond the consolidated topology primitive.

---

### User Story 3 — `spec-kitty upgrade` survives (and heals) malformed-frontmatter corpora (Priority: P1) — #3372

A project carries a legacy WP artifact with a duplicate `review_feedback` key (invalid YAML). Today the
first `spec-kitty upgrade` crashes uncaught mid-`runtime_state_backfill` and strands the project — the
repair command is gated behind the state the crash destroyed. After this mission, upgrade degrades
gracefully and a doctor check detects/repairs the artifact, and git can no longer *compose* such a
duplicate.

**Why this priority**: P1 (operator-flagged possible P0) — it produces on-disk corruption that later
manifests as "core workflow broken with no self-service recovery" (root trigger of #3334/#3335/#3338).

**Independent Test**: Feed a hand-crafted duplicate-key WP file to the backfill migration; assert it
returns `MigrationResult(success=False)` with a per-file diagnostic instead of raising; run
`doctor frontmatter-integrity` and assert detect + safe repair.

**Acceptance Scenarios**:

1. **Given** ≥1 malformed-frontmatter artifact anywhere under `kitty-specs/`, **When**
   `spec-kitty upgrade` / `runtime_state_backfill` runs, **Then** it does not raise uncaught; it
   reports the offending file(s) and returns a structured failure the operator can act on, leaving the
   project recoverable.
2. **Given** a corpus with duplicate-key frontmatter, **When** `spec-kitty doctor frontmatter-integrity`
   runs, **Then** it detects the malformed files with a tolerant reader and (report-only by default)
   offers a safe repair to valid YAML.
3. **Given** two lane/coord branches independently editing a WP frontmatter, **When** they are merged,
   **Then** the YAML-aware merge driver prevents composing a duplicate mapping key (no silent
   dual-key artifact).
4. **Given** the frontmatter read boundary, **When** a duplicate mapping key is present, **Then** the
   canonical reader fails closed with a legible error, and a tolerant repair path is available to
   consumers that must survive legacy corpora.

---

### User Story 4 — Topology / checkout-identity primitives live in exactly one place (Priority: P2) — #3373

A maintainer applying a correctness fix (symlink canonicalization, `.git`-interior detection, stderr
classification) to the git-common-dir / toplevel probe should touch one implementation, not four.
Today the probe is re-implemented in `checkout_ownership.py`, `commit_helpers.py`, `workspace/context.py`,
and `charter/resolution.py` (only the last caches + classifies "not a repo"), and the
`effective_root`-read-path fork recurs ~12× inside the coord/topology resolvers.

**Why this priority**: P2 tech-debt, but it is the **foundation** the #3128 checkout-identity check
stands on — consolidating it first prevents the check from becoming a fifth copy.

**Independent Test**: The four probe implementations reduce to one shared primitive; the existing suite
(charter caching, not-a-repo classification, NESTED refusal) stays green with no behavioral change.

**Acceptance Scenarios**:

1. **Given** the git-common-dir / toplevel probe, **When** consolidated, **Then** exactly one
   `git_common_dir()`/`git_toplevel()` primitive exists, preserving the richest contract (caching +
   not-a-repo classification + `.git`-interior detection); the other 3 copies are removed.
2. **Given** the `effective_root is None ? legacy : compose_meta_json_path(...)` fork, **When**
   consolidated, **Then** a single `read_dir_for(...)` helper is consumed by every coord/topology
   resolver with no per-site copy.
3. **Given** the nested/toplevel-mismatch classifier, **When** consolidated, **Then** one authority
   feeds both the fast `is_worktree_of` gate and the comparator classification, preserving the NESTED
   refusal (proven by an existing-behavior test).

---

### Edge Cases

- **Moving-tip**: a coord mission whose `target_branch` advances (for unrelated reasons) between
  finalize and implement — lane allocation must still succeed (recorded `planning_commit_sha` frozen;
  no live re-derivation).
- **Legacy mission** (no `coordination_branch`): the partition-aware commit path must no-op to
  `target_branch` exactly as today (no behavior change for SINGLE_BRANCH / LANES).
- **Non-`review_feedback` duplicate key**: the frontmatter guard/repair must handle *any* duplicate
  mapping key, not just `review_feedback`.
- **Legitimate linked worktrees**: the #3128 check must PASS for the mission's own lane/coord
  worktrees and only refuse foreign checkouts (no false positives).
- **Nested worktree path** and **not-a-git-repo path**: the consolidated primitive must classify these
  exactly as `charter/resolution.py` does today.

## Requirements *(mandatory)*

### Functional Requirements

| ID | Title | User Story | Priority | Status |
|----|-------|------------|----------|--------|
| FR-001 | Partition-aware planning-artifact auto-commit | US1 | High | Open |
| FR-002 | PRIMARY-on-coord commit fails loud everywhere | US1 | High | Open |
| FR-003 | Retire finalize `tasks.md`/`lanes.json` → coord staging (door #2) | US1 | High | Open |
| FR-004 | Coord + PR-bound lane allocation succeeds end-to-end | US1 | High | Open |
| FR-005 | Fail-closed checkout-identity comparison-and-refuse | US2 | High | Open |
| FR-006 | `upgrade`/backfill degrades (no uncaught crash) on malformed frontmatter | US3 | High | Open |
| FR-007 | `doctor frontmatter-integrity` detect + safe repair | US3 | High | Open |
| FR-008 | YAML-aware merge driver for `tasks/WP*.md` frontmatter | US3 | Medium | Open |
| FR-009 | Frontmatter boundary fail-closed on duplicate key + tolerant repair path | US3 | Medium | Open |
| FR-010 | Single `git_common_dir()`/`git_toplevel()` primitive (richest contract) | US4 | Medium | Open |
| FR-011 | Centralized `read_dir_for(...)` effective-root helper | US4 | Medium | Open |
| FR-012 | Single nested/toplevel-mismatch classifier authority | US4 | Medium | Open |

**FR detail:**

- **FR-001** — `implement.py::_commit_planning_artifacts_transaction` MUST partition `files_to_commit` by
  kind on the `placement_ref is not None` path (not only the legacy branch): PRIMARY kinds commit to the
  mission `target_branch`; COORD-residue to the coordination branch. Route through the canonical
  partition seam (`_group_files_by_partition` / `placement_seam().write_target(kind)`) rather than a
  new per-caller conditional. Preserve `BookkeepingTransaction` atomicity (FR-020/FR-027).
- **FR-002** — The `PrimaryKindReachedCoordStagingError` guard MUST cover every coord write entry point
  — including the `BookkeepingTransaction` commit path implement.py uses — so no PRIMARY artifact can
  reach a coordination write surface silently.
- **FR-003** — finalize-tasks MUST NOT stage PRIMARY planning artifacts into the coordination worktree;
  the pinned `test_finalize_coord_staging.py` / `test_finalize_clobber_e2e.py` contracts are updated to
  assert the disjoint behavior.
- **FR-004** — A coord-topology + PR-bound `--start-branch` mission MUST reach `implement WP01+` lane
  allocation without a `PlanningCommitMergeConflictError` and without a manual reconcile.
- **FR-005** — A mission-mutating command invoked from a checkout the mission does not own MUST fail
  closed with an actionable error, comparing the invoking checkout against already-computed mission/lane
  workspace metadata. It MUST NOT refuse the mission's own owned worktrees.
- **FR-006** — `runtime_state_backfill` / the upgrade runner MUST catch the malformed-artifact read
  failure and degrade to a structured `MigrationResult(success=False)` with a per-file diagnostic; it
  MUST NOT propagate an uncaught `LegacyRuntimeReadError` that aborts the whole `upgrade`.
- **FR-007** — A `doctor frontmatter-integrity` subcommand MUST scan `kitty-specs/*` for
  duplicate-key/malformed frontmatter using a tolerant reader and offer a safe repair (report-only by
  default), following the `_review_cycle_reconcile_doctor.py` per-subcommand-module precedent.
- **FR-008** — A YAML-aware merge driver MUST cover `tasks/WP*.md` (and any frontmatter-bearing mission
  artifact not already covered) so concurrent lane/coord merges cannot compose a duplicate mapping key.
- **FR-009** — The canonical frontmatter reader MUST fail closed on a duplicate mapping key with a
  legible error; a tolerant repair path (last-value-wins or report-both) MUST be available for
  consumers (migrations, doctor) that must survive legacy corpora.
- **FR-010** — One `git_common_dir()`/`git_toplevel()` primitive MUST replace the four
  re-implementations, preserving caching + not-a-repo classification + `.git`-interior detection; the
  other callers adapt to consume it.
- **FR-011** — The `effective_root is None ? legacy : compose_meta_json_path(...)` derivation MUST be
  centralized in one `read_dir_for(...)` helper consumed by all coord/topology resolvers.
- **FR-012** — Nested/toplevel-mismatch detection MUST consolidate to one authority feeding both the
  fast gate and the comparator classifier, preserving the NESTED refusal.

### Non-Functional Requirements

| ID | Title | Requirement | Category | Priority | Status |
|----|-------|-------------|----------|----------|--------|
| NFR-001 | Coord-branch purity | Zero PRIMARY-partition files present on any coordination branch across a full mission lifecycle (automated repo scan) | Reliability | High | Open |
| NFR-002 | Upgrade survivability | `upgrade` completes without data loss and remains self-service-recoverable with ≥1 malformed artifact present | Reliability | High | Open |
| NFR-003 | No architectural regression | All `tests/architectural/` gates stay green; ADRs `2026-07-29-1`, `2026-06-24-1/2`, `2026-06-22-1` invariants preserved | Compatibility | High | Open |
| NFR-004 | Checkout-check overhead | The #3128 check is a single comparison against already-computed metadata; adds no extra git subprocess calls beyond the consolidated primitive | Performance | Medium | Open |

### Constraints

| ID | Title | Constraint | Category | Priority | Status |
|----|-------|------------|----------|----------|--------|
| C-001 | Kind-partition, not topology switch | Placement changes expressed as kind-partition routing through the canonical seam (frozensets / `commit_for_mission` / `placement_seam`), never per-caller topology `if` or a parallel write-only resolver (ADR 2026-06-24-1 C-006) | Technical | High | Open |
| C-002 | Preserve coord parentage | Keep the coordination-worktree mechanism (C-004) and lane coord-descent (Assert A'); do NOT re-parent lanes off `target_branch` or change the create-time coord base | Technical | High | Open |
| C-003 | No topology redesign | #3128 is additive comparison-and-refuse only; no shadow-workspace / topology redesign (#1878 on-record non-goal) — reversing that non-goal is an operator call, not an in-mission decision | Technical | High | Open |
| C-004 | Route through the seam | Route through `placement_seam().write_target(kind)` / `commit_for_mission` and fail loud on an unresolved surface; do NOT re-add surface selection at the call site (the "semi-compliance" anti-pattern) | Technical | High | Open |
| C-005 | Read-from-stored, no live re-derivation | Topology read from stored `meta.json`, never re-inferred from worktree existence; `planning_commit_sha` never re-derived live; `meta.json`/`target_branch` read from the repository-root checkout | Technical | High | Open |
| C-006 | Project quality bars | Terminology canon (Mission not feature*); new code passes ruff + mypy with zero issues; every new branch/helper covered by focused tests in the same PR | Technical | Medium | Open |

### Key Entities *(include if mission involves data)*

- **Placement partition** — the two frozensets (`_PRIMARY_ARTIFACT_KINDS` / `_PLACEMENT_ARTIFACT_KINDS`
  in `mission_runtime/artifacts.py`); the single "swappable locus" deciding PRIMARY vs COORD.
- **CommitTarget / `placement_ref`** — the resolved write surface; today conflated ("one ref for
  everything") under coord topology, which is the #3371 vector.
- **Coordination branch / worktree** — COORD-partition write surface; must carry only status/matrix/
  tracer artifacts, never PRIMARY planning artifacts.
- **Mission workspace identity** — the declared workspace vs the invoking checkout (the #3128
  comparison).
- **WP frontmatter artifact** (`tasks/WP*.md`) — YAML-frontmatter mission artifact; must never carry a
  duplicate mapping key.
- **Git-topology primitive** — `git_common_dir()`/`git_toplevel()` + nested-classifier (the #3373
  consolidation target).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A coord-topology + PR-bound `--start-branch` mission completes specify → `implement WP01`
  with **zero** manual coord←primary reconciles (the `mission-a-p0-consistency` reproduction passes as
  an automated regression).
- **SC-002**: Automated scan finds **zero** PRIMARY-partition files on any coordination branch across a
  full mission lifecycle (NFR-001).
- **SC-003**: `spec-kitty upgrade` over a corpus containing ≥1 duplicate-key WP frontmatter completes
  **without crashing**, reports the offending file(s), and `doctor frontmatter-integrity` repairs it to
  valid YAML.
- **SC-004**: A mission-mutating command invoked from a foreign checkout refuses (exit ≠ 0, actionable
  message) in **100%** of attempts; the 2026-07-31 incident shape is caught; the mission's own worktrees
  are never falsely refused.
- **SC-005**: The git-topology/effective-root probe exists in **exactly one** place; the four prior
  copies are removed; the full existing suite stays green (no behavioral regression).

## Traceability

- **Issues**: #3371 (P0), #3128 (folded structural boundary), #3372 (P1), #3373 (P2). Class umbrella
  #3129; coord-authority #2160; #1878.
- **ADRs**: `2026-07-29-1` (lane base merges recorded planning commit — disjointness invariant),
  `2026-06-24-1` (kind- and topology-aware placement — C-006), `2026-06-24-2` (write-branch primary
  anchor), `2026-06-22-1` (topology SSOT).
- **Investigation**: `docs/plans/investigations/write-path-topology-root-cause.md` (Option A / #3128).
- **Reproduction evidence**: coord branch `kitty/mission-mission-a-p0-consistency-01KZWHY1`, commit
  `c3d92a364` (PRIMARY `lanes.json` on coord).
- **Canonical seams**: `implement.py::_commit_planning_artifacts_transaction`,
  `coordination/commit_router.py` (`_group_files_by_partition`, `_stage_artifacts_in_coord_worktree`,
  `PrimaryKindReachedCoordStagingError`), `lanes/worktree_allocator.py::_merge_recorded_planning_commit`,
  `migration/backfill_runtime_state.py::read_legacy_runtime`, `frontmatter.py`, `lanes/merge.py`
  (`_MERGE_DRIVERS`), `core/checkout_ownership.py` / `git/commit_helpers.py` / `workspace/context.py` /
  `charter/resolution.py`, `mission_runtime/resolution.py`.
