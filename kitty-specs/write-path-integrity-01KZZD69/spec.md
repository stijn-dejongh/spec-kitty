# Mission Specification: Mission-Artifact Write-Path Integrity

**Mission Branch**: `mission/write-path-integrity`
**Created**: 2026-08-14
**Status**: Draft (post-research + post-design-squad; structural spine adopted)
**Input**: Treat the #3371 P0 as a *symptom of a structural problem*. Fold the write-path cluster
siblings (#3371, #2549, #2702, #3128, #3372, #3373) into one mission with a **by-construction**
fix, not another round of whack-a-field. Prefer design-aligned solutions that complete the #1878
strangler and close epic #2160.

## Summary & Framing

The tracker's "ambient-location / write-path topology" cluster (#3129, 14 issues) keeps re-spawning
because **no single seam enforces two invariants every mission-mutating write depends on**: (1) the
write originates from the checkout the mission *declares*, and (2) each artifact lands on the partition
its *kind* dictates. Today both facts are *computed* but nothing *refuses* on them, so each new command
that forgets to route correctly becomes a new field-level bug.

**This mission relocates the fix to the one mandatory construction door and makes it fail closed —
so the failure class becomes unrepresentable rather than patched command-by-command.**

### The disease, one table

| Issue | Latent-malformed write | Detonates in | Class |
|-------|------------------------|--------------|-------|
| #3371 (P0) | PRIMARY `lanes.json` committed to the **coord** ref | lane allocator `git merge` → add/add | #2160 partition |
| #2549 | COORD `status.*` committed to the **lane** ref (`move-task --force`) | tool's own later `--to approved` rejects it | #2160 partition (the mirror of #3371) |
| #2702 | `record-analysis` commits the coord copy, reports the primary path | untracked residue on primary | #2160 partition |
| #3128 | *(enabling gap)* nothing compares invoking checkout vs declared workspace | any ambient-location write (2026-07-31 incident) | #1878 checkout-identity |
| #3372 (P1) | duplicate-key YAML in a legacy WP frontmatter | `spec-kitty upgrade` → uncaught `LegacyRuntimeReadError` | #3044 / #3347 |
| #3373 (P2) | *(no artifact yet)* triplicated topology/checkout primitives that will drift | a future one-copy correctness fix | #2624 (substrate for #3128) |

### The structural spine (adopted)

`build_execution_context()` (`src/mission_runtime/resolution.py:217`) is the **sole**
`MissionExecutionContext(` construction door in production code. It already assembles, on every build,
both `artifact_placement`/`branch_ref` (the partition surface) and `workspace`
(`primary_root`/`current_cwd`/`allowed_command_cwd`, the checkout identity). **Nothing currently
refuses on either.**

> **Spine:** make `build_execution_context()` a **fail-closed smart constructor**. For a *mutating*
> action it refuses to produce a context when **(i)** `current_cwd` is not the mission's *declared*
> workspace (checkout-identity, #3128), or **(ii)** the requested placement would route a PRIMARY kind
> to a coord ref / a COORD kind to a lane ref (partition, #3371/#2549/#2702). Read-only actions keep
> serving from anywhere.

This defeats the "comparison-and-refuse is bug #16 in the same disease class" objection *by
construction*: a command cannot skip a door it must pass through to obtain the context it needs to
write. `PrimaryKindReachedCoordStagingError` (`commit_router.py:615`) is the codebase's own existence
proof that a defect class can be made impossible with a typed refusal at one seam — this mission gives
that guard teeth on the actual write path and generalizes it to checkout identity. Both legs are on
#1878's **sanctioned deferred list** (item 1 "migrate remaining direct-placement call sites … residual
scope is the `implement.py` C-004 fallback"; item 4 "is-a-worktree type invariant"). **No topology /
shadow-workspace redesign** — the mission *completes the strangler #1878 already defines*.

### Confirmed P0 root cause (git-proven)

`implement.py::_commit_planning_artifacts_transaction` (`implement.py:890-902`, the
`placement_ref is not None` arm) commits the whole planning batch **verbatim to `placement_ref.ref`**,
which under coord topology is the coordination branch — so a dirty PRIMARY `lanes.json` lands on coord
(commit `c3d92a364` on `kitty/mission-mission-a-p0-consistency-01KZWHY1` carries `implement.py:701`'s
exact message, adds only `lanes.json`). The partition helper that would prevent it
(`_partition_files_for_commit`, `implement.py:714`) is **dead on this path** — wired only into the
legacy `else` branch. This arm is a *deliberate, pinned* C-004/#2160 deferral
(`test_effective_destination_ref_is_placement_ref_verbatim`); **this mission sanctions reversing it.**
The lane then branches from coord and merges the recorded `planning_commit_sha` (on `target_branch`,
also carrying `lanes.json`); with `lanes.json` absent at the merge-base the merge is a guaranteed
add/add → `PlanningCommitMergeConflictError` (`worktree_allocator.py:339-356`), violating ADR
`2026-07-29-1` §3's disjointness assumption (which the ADR itself deferred to #2160).

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Partition-correct commits: no artifact ever lands on the wrong branch (Priority: P1) — #3371 + #2549 + #2702 (closes #2160)

Three commands today commit an artifact to the wrong partition surface: `implement`'s planning
auto-commit (PRIMARY→coord, the P0), `move-task --force` (COORD→lane), and `record-analysis`
(write/report-surface disagreement). After this mission, every mission-mutating commit routes each file
to the partition its *kind* dictates, and a mis-route **fails loud** instead of silently corrupting a
branch. This closes epic #2160.

**Why this priority**: The P0 blocks all implementation on coord + PR-bound missions; #2549 is its
exact mirror; fixing one direction alone leaves the other live (whack-a-field).

**Independent Test**: Reproduce `mission-a-p0-consistency`'s shape (coord topology, PR-bound
`--start-branch`), drive finalize + `implement WP01`; assert allocation succeeds and no PRIMARY file
sits on coord. Separately assert `move-task --force` from a lane commits `status.*` to the coord ref,
and `record-analysis` writes and reports the same seam-resolved ref.

**Acceptance Scenarios**:

1. **Given** a coord-topology mission with a dirty uncommitted `lanes.json` at implement time, **When**
   `_ensure_planning_artifacts_committed_git` auto-commits, **Then** the PRIMARY `lanes.json` commits to
   `target_branch` and the coord-residue (if any) to the coord ref — never a mixed batch to one ref.
2. **Given** the coord-topology + PR-bound `--start-branch` reproduction, **When** `implement WP01`
   allocates the lane, **Then** the recorded-planning-commit merge is conflict-free (no
   `PlanningCommitMergeConflictError`) with no manual reconcile.
3. **Given** `move-task --force` invoked from a lane (#2549), **When** it commits status, **Then**
   `status.*` (COORD) lands on the coord ref, never the lane ref.
4. **Given** `record-analysis` (#2702), **When** it commits the analysis artifact, **Then** the write
   surface and the reported path are the same seam-resolved ref (no untracked primary residue).
5. **Given** any attempt to commit a PRIMARY kind to a coord surface (or COORD kind to a lane surface),
   **When** the commit is attempted at the planning-commit entry, **Then** it fails loud with a
   partition-guard error — excluding legitimate self-bookkeeping churn (`meta.json`) that co-travels
   coord writes.

---

### User Story 2 — Mission-mutating commands refuse to run from a checkout the mission does not own (Priority: P1) — #3128 (via the factory spine)

An agent (e.g. a compacted/resumed session) invokes a mission-mutating command from the wrong checkout.
Today nothing compares the invoking checkout against the mission's *declared* workspace, so the write
silently lands in the ambient location (the 2026-07-31 `spec-kitty-saas` incident). After this mission,
`build_execution_context()` refuses to produce a mutating context on that mismatch.

**Why this priority**: The structural gap under the entire #3129 class; the sanctioned near-term remedy.
Wiring it into the mandatory factory (not opt-in per-call flags) is what makes it actually fire.

**Independent Test**: From a checkout that is *not* the mission's declared workspace (including another
mission's lane in the same repo/registry), invoke a mission-mutating command; assert it refuses (exit ≠
0, actionable error). From the mission's own declared lane/coord worktree, assert it proceeds.

**Acceptance Scenarios**:

1. **Given** mission A whose declared workspace is lane A, **When** a mission-A-mutating command is
   invoked from mission B's lane (same worktree registry), **Then** it refuses — the comparison is
   against the mission's *declared* lane/`meta.json`, not mere repo-membership.
2. **Given** the mission's own owned lane/coord worktree, **When** the same command runs there, **Then**
   it proceeds (no false refusal).
3. **Given** a read-only command (`status`, `doctor --audit`), **When** invoked from anywhere, **Then**
   it still serves (reads are not gated by the identity refusal).
4. **Given** the comparison, **When** it runs, **Then** it uses already-computed mission/lane metadata
   (no live re-derivation) and adds no git subprocess calls beyond the consolidated topology primitive.

---

### User Story 3 — `spec-kitty upgrade` survives (and heals) malformed-frontmatter corpora (Priority: P1) — #3372

A project carries a legacy WP artifact with a duplicate `review_feedback` key (invalid YAML). Today the
first `spec-kitty upgrade` crashes uncaught mid-`runtime_state_backfill` and strands the project. After
this mission, upgrade degrades gracefully and a doctor check detects/repairs the artifact.

**Why this priority**: P1 (operator-flagged possible P0) — the root trigger of #3334/#3335/#3338; it
produces corruption that later manifests as "core workflow broken with no self-service recovery."

**Independent Test**: Feed a hand-crafted duplicate-key WP file to the backfill migration; assert it
returns `MigrationResult(success=False)` with a per-file diagnostic instead of raising. Run
`doctor frontmatter-integrity`; assert detect + safe repair.

**Acceptance Scenarios**:

1. **Given** ≥1 malformed-frontmatter artifact anywhere under `kitty-specs/`, **When** `upgrade` /
   `runtime_state_backfill` runs, **Then** it does not raise uncaught; it catches the read failure,
   reports the offending file(s), and returns a structured failure that leaves the project recoverable.
2. **Given** a corpus with duplicate-key frontmatter, **When** `spec-kitty doctor frontmatter-integrity`
   runs, **Then** it detects the malformed files with a tolerant reader and (report-only by default)
   offers a safe repair to valid YAML.
3. **Given** the canonical frontmatter reader, **When** a duplicate mapping key is present, **Then** it
   *continues* to fail closed (it already raises `DuplicateKeyError` → `FrontmatterError`); this
   behavior is **not relaxed** — only migration/doctor call sites wrap it in a tolerant repair path.

---

### User Story 4 — Topology / checkout-identity primitives live in exactly one place (Priority: P2, lands first) — #3373

A maintainer applying a correctness fix (symlink canonicalization, `.git`-interior detection, stderr
classification) should touch one implementation, not four. The probe is re-implemented in
`checkout_ownership.py`, `commit_helpers.py`, `workspace/context.py`, and `charter/resolution.py` (only
the last caches + classifies "not a repo"); the `effective_root`-read fork recurs ~12× inside the
coord/topology resolvers.

**Why this priority**: P2 tech-debt, but it is the **substrate the factory spine stands on** — a
constructor invariant built on a probe with three drifting copies is untrustworthy, and un-canonicalized
symlinks would make the #3128 identity check false-refuse the mission's own worktrees. **It lands
first.**

**Independent Test**: The four probe implementations reduce to one shared, symlink-canonicalizing
primitive; the existing suite (charter caching, not-a-repo classification, NESTED refusal) stays green
with no behavioral change.

**Acceptance Scenarios**:

1. **Given** the git-common-dir / toplevel probe, **When** consolidated, **Then** exactly one
   `git_common_dir()`/`git_toplevel()` primitive exists (caching + not-a-repo classification +
   `.git`-interior detection + symlink canonicalization); the other 3 copies are removed.
2. **Given** the `effective_root is None ? legacy : compose_meta_json_path(...)` fork, **When**
   consolidated, **Then** one `read_dir_for(...)` helper is consumed by every coord/topology resolver.
3. **Given** the nested/toplevel-mismatch classifier, **When** consolidated, **Then** one authority
   feeds both the fast `is_worktree_of` gate and the comparator classification, preserving the NESTED
   refusal (proven by an existing-behavior test).

---

### Edge Cases

- **Moving-tip**: a coord mission whose `target_branch` advances between finalize and implement — lane
  allocation still succeeds (`planning_commit_sha` frozen; no live re-derivation).
- **Legacy mission** (no `coordination_branch`): the partition-aware commit path no-ops to
  `target_branch` exactly as today (no behavior change for SINGLE_BRANCH / LANES).
- **Empty partition group**: one partition clean at commit time must not hard-fail the claim (use
  `commit_idempotent`; per-partition atomicity, not implied end-to-end atomicity).
- **`meta.json` co-travel**: `meta.json` is PRIMARY per the residue predicate yet legitimately
  accompanies coord writes — the partition guard must exclude self-bookkeeping churn.
- **Non-`review_feedback` duplicate key**: the degrade/repair path handles *any* duplicate mapping key.
- **Symlinked components** (`/var`→`/private/var`): the identity check must not false-refuse an owned
  worktree — hence #3373 lands first.
- **Same worktree registry, different mission**: the identity check refuses a foreign mission's lane
  (repo-membership alone would classify it OWNED).

## Requirements *(mandatory)*

### Functional Requirements

| ID | Title | User Story | Priority | Status |
|----|-------|------------|----------|--------|
| FR-001 | Partition-aware planning-artifact auto-commit (retire the verbatim arm) | US1 | High | Open |
| FR-002 | Partition guard bites at the planning-commit entry (excl. self-bookkeeping) | US1 | High | Open |
| FR-003 | Fold #2549 (`move-task`) + #2702 (`record-analysis`) through the seam | US1 | High | Open |
| FR-004 | Coord + PR-bound lane allocation succeeds end-to-end | US1 | High | Open |
| FR-005 | Fail-closed **mission-identity** checkout refusal in `build_execution_context` | US2 | High | Open |
| FR-006 | `upgrade`/backfill degrades (no uncaught crash) on malformed frontmatter | US3 | High | Open |
| FR-007 | `doctor frontmatter-integrity` detect + safe repair (tolerant reader) | US3 | High | Open |
| FR-008 | Single `git_common_dir()`/`git_toplevel()` primitive + symlink canonicalization | US4 | High | Open |
| FR-009 | Centralized `read_dir_for(...)` effective-root helper | US4 | Medium | Open |
| FR-010 | Single nested/toplevel-mismatch classifier authority | US4 | Medium | Open |
| FR-011 | Arch gate for Axis-B (mixed-partition-batch-to-single-ref) | US1 | Medium | Open |

**FR detail:**

- **FR-001** — Replace `implement.py`'s verbatim `placement_ref` arm with
  `_partition_files_for_commit` + **two partition-scoped `BookkeepingTransaction` commits** using
  `commit_idempotent` (PRIMARY → `target_branch`; COORD-residue → coord ref). Preserve
  `BookkeepingTransaction` atomicity *per partition*. This **explicitly reverses** the pinned C-004/D11
  verbatim deferral (`test_effective_destination_ref_is_placement_ref_verbatim` is rewritten to assert
  the partition split); the reversal is sanctioned by this mission (closing #2160).
- **FR-002** — The partition/`PrimaryKindReachedCoordStaging` guard MUST bite at the planning-commit
  entry (`_run_planning_artifact_commit`), classifying staged paths by kind, and MUST exclude
  self-bookkeeping churn (`meta.json`) that legitimately co-travels coord writes — so PRIMARY→coord and
  COORD→lane both fail loud without refusing legitimate coord commits.
- **FR-003** — Route `move-task --force` (#2549) and `record-analysis` (#2702) through the same
  partition seam so their commits resolve per-kind refs; a mis-route fails loud. **Respect the withdrawn
  Trigger A**: status→coord *under coord topology* is correct by design and MUST NOT be "fixed."
- **FR-004** — A coord-topology + PR-bound `--start-branch` mission MUST reach `implement WP01+` lane
  allocation without a `PlanningCommitMergeConflictError` and without a manual reconcile (regression pin).
- **FR-005** — `build_execution_context()` MUST refuse to produce a *mutating* context when the invoking
  checkout is not the mission's **declared** workspace (compared against `meta.json`/lane metadata, not
  mere repo-membership), with an actionable error. Read-only actions are exempt. It MUST NOT refuse the
  mission's own owned lane/coord worktrees, and MUST NOT re-derive metadata live.
- **FR-006** — `runtime_state_backfill` / the upgrade runner MUST catch the malformed-artifact read
  failure (`LegacyRuntimeReadError` at `backfill_runtime_state.py:581-585`) and degrade to a structured
  `MigrationResult(success=False)` with a per-file diagnostic; it MUST NOT propagate an uncaught error
  that aborts the whole `upgrade`.
- **FR-007** — A `doctor frontmatter-integrity` subcommand MUST scan `kitty-specs/*` for
  duplicate-key/malformed frontmatter using a *tolerant* reader and offer a safe repair (report-only by
  default), following the `_review_cycle_reconcile_doctor.py` per-subcommand-module precedent. It MUST
  NOT relax the canonical `FrontmatterManager.read()` (which already fails closed).
- **FR-008** — One `git_common_dir()`/`git_toplevel()` primitive MUST replace the four
  re-implementations, preserving caching + not-a-repo classification + `.git`-interior detection and
  adding **symlink canonicalization**; the other callers adapt to consume it.
- **FR-009** — The `effective_root is None ? legacy : compose_meta_json_path(...)` derivation MUST be
  centralized in one `read_dir_for(...)` helper consumed by all coord/topology resolvers.
- **FR-010** — Nested/toplevel-mismatch detection MUST consolidate to one authority feeding both the
  fast gate and the comparator classifier, preserving the NESTED refusal.
- **FR-011** — An architectural gate MUST catch mixed-partition-batch-to-single-ref commits (the P0's
  "Axis B" — neither existing arch gate detects it today), so a future regression fails CI.

### Non-Functional Requirements

| ID | Title | Requirement | Category | Priority | Status |
|----|-------|-------------|----------|----------|--------|
| NFR-001 | Coord-branch purity | Zero PRIMARY-partition files on any coordination branch, and zero COORD-partition files on any lane branch, across a full mission lifecycle (automated repo scan) | Reliability | High | Open |
| NFR-002 | Upgrade survivability | `upgrade` completes without data loss and remains self-service-recoverable with ≥1 malformed artifact present | Reliability | High | Open |
| NFR-003 | No architectural regression | All `tests/architectural/` gates green; ADR `2026-07-29-1` (Assert A'/coord-descent), `2026-06-24-1/2`, `2026-06-22-1` invariants preserved; #1878 no-topology-redesign non-goal upheld | Compatibility | High | Open |
| NFR-004 | Refusal overhead | The factory refusal is a comparison against already-computed metadata; no extra git subprocess calls beyond the consolidated primitive | Performance | Medium | Open |

### Constraints

| ID | Title | Constraint | Category | Priority | Status |
|----|-------|------------|----------|----------|--------|
| C-001 | By-construction, one door | The two invariants (checkout-identity, partition) are enforced in the mandatory `build_execution_context()` factory, NOT re-added as per-call-site checks or a parallel resolver (ADR 2026-06-24-1 C-006; defeats the "bug #16" pattern) | Technical | High | Open |
| C-002 | Preserve coord parentage | Keep the coordination-worktree mechanism (C-004) and lane coord-descent (Assert A'); do NOT re-parent lanes off `target_branch` or change the create-time coord base | Technical | High | Open |
| C-003 | No topology redesign | No shadow-workspace / topology-model change (#1878 on-record non-goal); the mission completes the strangler #1878 defines. Reversing that non-goal is an operator call, not an in-mission decision | Technical | High | Open |
| C-004 | Sanctioned C-004/D11 reversal | Reversing the pinned `placement_ref`-verbatim deferral (FR-001) is explicitly sanctioned by this mission because it closes #2160; the pinned test is rewritten, not deleted silently | Technical | High | Open |
| C-005 | Read-from-stored, no live re-derivation | Topology read from stored `meta.json`, never re-inferred; `planning_commit_sha` never re-derived live; `meta.json`/`target_branch` read from the repository-root checkout | Technical | High | Open |
| C-006 | Per-partition atomicity | Split commits use `commit_idempotent`; an empty partition group MUST NOT hard-fail the claim; atomicity is per-partition, not implied end-to-end | Technical | High | Open |
| C-007 | Project quality bars | Terminology canon (Mission not feature*); new code passes ruff + mypy with zero issues; every new branch/helper covered by focused tests in the same PR | Technical | Medium | Open |

### Non-Goals (explicit)

- **No WP-frontmatter merge driver** (former FR-008). WP task files are deliberately single-writer
  (`lanes/merge.py:112-120`; `owned_files` partitions lanes); a union driver would *manufacture* the
  dual-key artifact #3372 is about. #3372 is covered by FR-006 (degrade) + FR-007 (repair).
- **No relaxing the canonical frontmatter reader** — it already fails closed; only migration/doctor
  wrap it in a tolerant path.
- **No read-side lookup rewrite.** The read/lookup halves of #3124/#3051/#3049/#2613 are *de-risked but
  not closed* (their mutating halves are refused by FR-005; their read halves serve from anywhere by
  design). Full closure needs "resolve reads from the mission's declaration, not ambient location"
  (`locate_project_root`/`canonicalize_feature_dir`, #2624) — out of scope; doubles the mission.
- **Candidates #3131/#3133** stay candidates (same meta-shape, no shared implementation).

### Key Entities

- **`MissionExecutionContext` + `build_execution_context()`** — the sole construction door; becomes the
  fail-closed enforcement seam for both invariants.
- **Placement partition** — `_PRIMARY_ARTIFACT_KINDS` / `_PLACEMENT_ARTIFACT_KINDS`
  (`mission_runtime/artifacts.py`); the swappable locus deciding PRIMARY vs COORD.
- **CommitTarget / `placement_ref`** — the resolved write surface; conflated ("one ref for everything")
  in the verbatim arm — the #3371 vector.
- **Coordination branch / worktree** — COORD write surface; must carry only status/matrix/tracer, never
  PRIMARY planning artifacts.
- **Mission workspace identity** — the *declared* lane/workspace vs the invoking checkout (FR-005).
- **Git-topology primitive** — `git_common_dir()`/`git_toplevel()` + nested classifier (the #3373
  substrate).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A coord-topology + PR-bound `--start-branch` mission completes specify → `implement WP01`
  with **zero** manual coord←primary reconciles (the `mission-a-p0-consistency` reproduction is an
  automated regression).
- **SC-002**: Automated scan finds **zero** cross-partition artifacts — no PRIMARY file on any coord
  branch and no COORD file on any lane branch — across a full mission lifecycle (NFR-001), covering
  `implement`, `move-task --force`, and `record-analysis`.
- **SC-003**: `spec-kitty upgrade` over a corpus containing ≥1 duplicate-key WP frontmatter completes
  **without crashing**, reports the offending file(s), and `doctor frontmatter-integrity` repairs it to
  valid YAML.
- **SC-004**: A mission-mutating command invoked from a foreign checkout — *including another mission's
  lane in the same registry* — refuses (exit ≠ 0, actionable message) in **100%** of attempts; the
  mission's own worktrees and all read-only commands are never falsely refused; the 2026-07-31 incident
  shape is caught.
- **SC-005**: The git-topology/effective-root probe exists in **exactly one** place; the four prior
  copies are removed; the full existing suite stays green (no behavioral regression).
- **SC-006**: A new architectural gate fails CI on any mixed-partition-batch-to-single-ref commit
  (FR-011), so the P0's Axis-B cannot silently regress.

## Traceability

- **Issues**: #3371 (P0), #2549, #2702, #3128, #3372 (P1), #3373 (P2). Closes epic **#2160**; completes
  strangler **#1878**. Class umbrella #3129.
- **De-risked, not closed** (left under #2624/#1878): #3124, #3051, #3049, #2613 (read-side halves).
- **ADRs**: `2026-07-29-1` (disjointness invariant), `2026-06-24-1` (kind-partition placement, C-006),
  `2026-06-24-2` (write-branch primary anchor), `2026-06-22-1` (topology SSOT),
  `2026-06-03-2` (ExecutionContext owner + CommitTarget).
- **Investigation**: `docs/plans/investigations/write-path-topology-root-cause.md` (Option A / #3128).
- **Reproduction evidence**: coord branch `kitty/mission-mission-a-p0-consistency-01KZWHY1`, commit
  `c3d92a364` (PRIMARY `lanes.json` on coord).
- **Canonical seams**: `mission_runtime/resolution.py::build_execution_context` (spine),
  `implement.py::_commit_planning_artifacts_transaction` / `_partition_files_for_commit`,
  `coordination/commit_router.py` (`_group_files_by_partition`, `PrimaryKindReachedCoordStagingError`),
  `coordination/transaction.py` (`commit_idempotent`), `lanes/worktree_allocator.py`,
  `core/checkout_ownership.py::resolve_ownership_claim`,
  `migration/backfill_runtime_state.py::read_legacy_runtime`, `frontmatter.py`,
  `git/commit_helpers.py` / `workspace/context.py` / `charter/resolution.py`.
