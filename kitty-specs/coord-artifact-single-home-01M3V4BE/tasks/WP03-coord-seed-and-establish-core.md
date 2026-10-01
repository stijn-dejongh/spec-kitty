---
work_package_id: WP03
title: 'Coordination write-location core: establish, seed, refuse (IC-03 part 1)'
dependencies:
- WP02
requirement_refs:
- FR-003a
- FR-004
- FR-004a
- FR-004b
- C-001
- C-003
- C-004
- NFR-002
planning_base_branch: issue-5440-coord-artifact-single-home
merge_target_branch: issue-5440-coord-artifact-single-home
branch_strategy: Planning artifacts for this mission were generated on issue-5440-coord-artifact-single-home. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into issue-5440-coord-artifact-single-home unless the human explicitly redirects the landing branch.
subtasks:
- T012
- T013
- T014
- T015
- T016
- T017
phase: Phase 1 - Write-location accessor
history:
- at: '2026-10-01T08:36:27Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: python-pedro
agent: claude
authoritative_surface: src/specify_cli/coordination/coord_seed.py
create_intent:
- src/mission_runtime/write_location.py
- src/specify_cli/coordination/coord_seed.py
- tests/coordination/test_coord_seed.py
- tests/mission_runtime/test_write_location.py
- src/specify_cli/coordination/event_prefix.py
- tests/coordination/test_event_prefix.py
execution_mode: code_change
model: claude-sonnet-5
owned_files:
- src/mission_runtime/write_location.py
- src/specify_cli/coordination/coord_seed.py
- src/specify_cli/status/locking.py
- tests/coordination/test_coord_seed.py
- tests/mission_runtime/test_write_location.py
- src/specify_cli/coordination/event_prefix.py
- tests/coordination/test_event_prefix.py
role: implementer
tags: []
task_type: implement
tracker_refs: []
---

# Work Package Prompt: WP03 – Coordination write-location core: establish, seed, refuse (IC-03 part 1)

## ⚡ Do This First: Load Agent Profile

Use the `/ad-hoc-profile-load` skill to load the agent profile specified in the frontmatter (or any user-defined profile), and behave according to its guidance before parsing the rest of this prompt.

- **Profile**: `python-pedro`
- **Role**: `implementer`
- **Agent/tool**: `claude`

If no profile is specified, run `spec-kitty agent profile list` and select the best match for this work package's `task_type` and `authoritative_surface`.

---

## ⚠️ IMPORTANT: Review Feedback

**Read this first if you are implementing this task!**

- **Has review feedback?**: Check the `review_ref` field in the event log (via `spec-kitty agent tasks status` or the Activity Log below).
- **You must address all feedback** before your work is complete. Feedback items are your implementation TODO list.
- **Report progress**: As you address each feedback item, update the Activity Log explaining what you changed.

## Review Feedback

*[If this WP was returned from review, the reviewer feedback reference appears in the Activity Log below or in the status event log.]*

---

## Markdown Formatting

Wrap HTML/XML tags in backticks: `` `<div>` ``, `` `<script>` ``
Use language identifiers in code blocks: ````python`, ````bash`

---

## Objectives & Success Criteria

Build the **core of the one write-location accessor**: the function that, for a COORD-partition record of a coordination-routed Mission, returns the coordination Mission dir. It returns that in every coordination-worktree state, or refuses loudly. Specifically:

- **Value objects** in a new `src/mission_runtime/write_location.py`: `WriteLocation`, `Establishment`, `SeedReport`.
- **`establish_coord_write_location(...)`** in a new `src/specify_cli/coordination/coord_seed.py`. It does all of the following:
  - materializes an UNMATERIALIZED surface whose branch is local;
  - refuses a remote-only or deleted branch;
  - seeds a pre-fix EMPTY surface;
  - restores a post-fix EMPTY surface from the branch tip, with a loud warning.
- **`seed_coord_surface(...)`**: the one-time carry-over (contracts/seed.md):
  - prefix rule on event-id sequences;
  - fork refusal `COORD_SEED_FORK_REFUSED`;
  - atomic temp-dir + `os.rename` visibility;
  - one seed commit on the coordination branch;
  - root-checkout restoration;
  - idempotent; runs under the status lock.
- **`FeatureStatusLockTimeoutError.error_code = "STATUS_LOCK_HELD"`**.
- A test matrix over every state row, the prefix and fork cases, idempotence, atomicity, root restoration, lock reentrancy and the NFR-002 fixtures.

`PlacementSeam.write_dir(kind)`, the seam method writers call, is **WP04**. This WP exposes `establish_coord_write_location` for WP04 to delegate to.

## Context & Constraints

- **Load the charter**: `.kittify/charter/charter.md` and `spec-kitty charter context --action implement --json`.
- **Spec**:
  - FR-003a (establish or refuse; post-fix EMPTY warns and restores);
  - FR-004, FR-004a, FR-004b (seed exactly once, atomic, fork refusal);
  - US2.3-US2.8;
  - C-001 (one sanctioned seam extension; no new commit mechanism; the seed commits through the existing `commit_for_mission`);
  - C-003 (no automatic log merge);
  - C-004 (fix forward);
  - NFR-002 (zero loss).
- **Plan**: IC-03, including its risks: lock ordering; the owned-checkout arm; remote-only refusal (ruling Q1); post-fix restore (ruling Q3); pre-fix seed commit (ruling Q5).
- **Research**: D1 (accessor shape), D2 (lock ordering, atomicity), D3 (prefix rule, fork refusal), D4 (post-fix vs pre-fix discriminator: no meta flag, the coordination branch tree is the fact), D5 (seed commits on the coordination branch), D20 (remote-only refusal).
- **Contracts**: `contracts/seed.md` (procedure steps 1-11, errors) and `contracts/write-location-accessor.md` (states, errors).
- **Data model**: §2 (WriteLocation, CoordState handling table), §3 (SeedRequest/SeedReport, invariants I-SEED-1..9, outcomes), §7 (atomicity boundaries).
- **Code anchors** (verified at `ecb5dd914a`):
  - `ActionContextError`: `src/mission_runtime/resolution.py:126`.
  - `FeatureStatusLockTimeoutError`: `src/specify_cli/status/locking.py:59`. `feature_status_lock(repo_root, lock_key, *, timeout=-1)` at L278 is keyed on the git common dir plus the Mission dir name (path helper L147) and is reentrant (`machine_file_lock(..., reentrant=True)`, L255).
  - `CoordState`: `missions/_read_path_resolver.py:250-275`; `probe_coord_state` is just below it.
  - `materialize_coord_surface_for_write`: `coordination/surface_resolver.py:903`. It no-ops unless UNMATERIALIZED, raises via `_raise_unmaterialized` (L877) for a remote-only branch, and calls `CoordinationWorkspace.resolve` (`workspace.py:297`) otherwise.
  - `CoordinationBranchDeleted`: `surface_resolver.py:191`; `CoordinationWorktreeUnmaterialized`: `surface_resolver.py:292`.
  - `commit_for_mission(repo_root, mission_slug, files, message, policy, *, kind, ...)`: `coordination/commit_router.py:218`. Coordination-worktree paths commit in place (the `is_under_worktrees_segment` branch, ≈L1026).
  - `kind_for_mission_file`: `mission_runtime/artifacts.py:415`.
- **Layering**: `mission_runtime` must not import `specify_cli` at module level. `write_location.py` therefore holds only types and a stdlib/mission_runtime import set. `SeedReport` lives there because `WriteLocation.seed` references it. Run `tests/architectural/test_layer_rules.py`.
- **Do not edit `surface_resolver.py`** (owned by WP01/WP04). Call its public and private functions as needed; if you must use a private one, note it.
- **Model discipline**: implement = sonnet (`claude-sonnet-5`); review = opus.
- **Terminology**: Mission, never feature. Name the sense: "repository root checkout" (where pre-fix records sit), "target branch", "coordination branch/surface".
- **No heavy suites** (C-006).

## Branch Strategy

- **Strategy**: Planning artifacts were generated on issue-5440-coord-artifact-single-home; completed changes must merge back into issue-5440-coord-artifact-single-home.
- **Planning base branch**: `issue-5440-coord-artifact-single-home`
- **Merge target branch**: `issue-5440-coord-artifact-single-home`
- `finalize-tasks` allocates execution worktrees per computed lane from `lanes.json`.
- Start with `spec-kitty agent action implement WP03 --agent claude` and use the printed workspace path; never reconstruct it.
- **Lane-relevant shared files**: none. This WP runs in its own lane, after WP02 (fixtures). WP04 (lane A) depends on it.

## Subtasks & Detailed Guidance

### Subtask T012 – Red-first tests, value objects, error codes

- **Purpose**: Pin the observable contract before implementing (charter ATDD-First Discipline C-011), and introduce the typed results every writer receives.
- **Steps**:
  1. **Red-first commit (separate, first)**: `tests/coordination/test_coord_seed.py` with WP02 builders:
     - **Through the pre-existing entry point**: on `make_prefix_coord_mission(worktree="empty")`, the existing read resolver `placement_seam(repo_root, slug).read_dir(MissionArtifactKind.STATUS_STATE)` returns the **repository root checkout** dir. That is today's EMPTY fallback, so any writer using it forks the log. Write the test asserting the **write side** instead: `establish_coord_write_location(repo_root, slug, STATUS_STATE, owned=None).path` is the coordination Mission dir and holds the carried log. It fails at the base, because the function and module do not exist.
     - Assert in the same test that `read_dir` still returns the root dir. This is C-002, the kept read fallback, and stays green.
     - Add one failing test per state row (they become green in T016).
  2. `src/mission_runtime/write_location.py` (new):
     ```python
     class Establishment(enum.Enum):
         NONE = "none"; MATERIALIZED = "materialized"; SEEDED = "seeded"; RESTORED_FROM_BRANCH = "restored_from_branch"

     @dataclass(frozen=True)
     class SeedReport:
         carried: tuple[str, ...] = ()
         restored_root: tuple[str, ...] = ()
         restored_from_branch: tuple[str, ...] = ()
         coord_commit: str | None = None
         warnings: tuple[str, ...] = ()

     @dataclass(frozen=True)
     class WriteLocation:
         path: Path
         surface: Literal["primary", "coordination"]
         coord_state_before: CoordState | None
         establishment: Establishment
         seed: SeedReport | None = None
     ```
     `CoordState` lives in `specify_cli.missions._read_path_resolver`. Do not import it at module level from mission_runtime: use `TYPE_CHECKING` plus a string annotation, or type `coord_state_before` as `str | None` holding the enum value. Pick whichever passes `test_layer_rules.py` and `mypy --strict`, and document the choice. Declare `__all__`.
  3. **Error type**: `CoordSeedForkRefused(ActionContextError)`. Place it in `coord_seed.py` (specify_cli may import `mission_runtime.resolution`). Putting it in `write_location.py` would make that module import `resolution.py`, and `resolution.py` will import `write_location.py` in WP04: a cycle. Give it `error_code = "COORD_SEED_FORK_REFUSED"` and structured attributes: `root_path`, `coord_path`, `coord_ref`, `first_divergence_root`, `first_divergence_coord`, `reconcile_steps`.
  4. `status/locking.py:59`: add the class attribute `error_code: str = "STATUS_LOCK_HELD"` to `FeatureStatusLockTimeoutError`. Additive; the message is unchanged.
- **Files**: `src/mission_runtime/write_location.py`, `src/specify_cli/status/locking.py`, `tests/coordination/test_coord_seed.py`, `tests/mission_runtime/test_write_location.py`.
- **Validation**: the red commit fails for the right reason (missing behaviour, not a fixture error); `tests/mission_runtime/test_write_location.py` covers frozen-ness and defaults; the existing locking tests stay green (`grep -rl FeatureStatusLockTimeoutError tests/`).
- **Edge cases**: `error_code` must not clash with an existing attribute name on the exception. Check how other spec-kitty errors expose codes (for example `StructuredError`) and match that convention.
- **`checkout_root` (post-tasks squad P-M3)**: `WriteLocation` gains `checkout_root: Path`. It is the root of the checkout that holds `path`: the coordination worktree root for `surface="coordination"`, and the repository root checkout for `surface="primary"`. `establish_coord_write_location` populates it, and WP04 populates it for PRIMARY results. WP05, WP07, WP09, WP16 and WP18 consume it instead of deriving `.path.parent.parent`. Add a value-object test.

### Subtask T013 – Prefix rule as pure functions

- **Purpose**: The heart of "carry exactly once, refuse a fork" (I-SEED-4, I-SEED-6; research D3). Keep it pure, so it is exhaustively testable.
- **Steps**:
  1. In `coord_seed.py`:
     - `def read_event_ids(lines: Iterable[str]) -> tuple[str, ...]`: parse JSONL; skip blank lines; a malformed line raises a typed error and never silently skips (zero-loss rule).
     - `@dataclass(frozen=True) class PrefixVerdict`, with `kind: Literal["carry_tail", "nothing", "fork"]`, `tail_start: int` and `first_divergence: tuple[str | None, str | None]`.
     - `def classify_prefix(root_ids, coord_ids) -> PrefixVerdict`:
       - `C` empty → carry_tail(0);
       - `C` a proper prefix of `R` → carry_tail(len(C));
       - `R` a prefix of `C`, or equal → nothing;
       - otherwise fork, recording the first index where they differ.
     - `def merged_log_bytes(root_lines, coord_lines, verdict) -> bytes`: `C` plus the root lines from `tail_start` onward, **byte-faithful** (take the original root lines; never re-serialize).
  2. The streams are `status.events.jsonl` and `decisions.events.jsonl`. Apply the rule per stream; both must pass for the seed to proceed.
- **Files**: `src/specify_cli/coordination/coord_seed.py`; tests in `tests/coordination/test_coord_seed.py`.
- **Validation**:
  - A table-driven matrix: empty/empty, empty/R, C⊂R, R⊂C, equal, diverge at 0, diverge mid, diverge at last.
  - If `hypothesis` is already a dev dependency (check `pyproject.toml`), add a property test: for any `R` and a prefix `C`, `merged == R` and there are no duplicate ids. Otherwise use a seeded random generator.
- **Edge cases**:
  - Duplicate ids inside one input log: refuse (fork-like) rather than "fix" it, and name the duplicate. NFR-002 says no id twice; do not create or propagate duplicates.
  - Trailing newline handling must be byte-faithful.
- **Neutral home, mandatory reuse (post-tasks squad P-M6)**: put the pure prefix/fork classifier in `src/specify_cli/coordination/event_prefix.py` (owned here; tests in `tests/coordination/test_event_prefix.py`). It is pure, takes event-id sequences, and has no git or lock imports. `coord_seed.py` imports it, and WP17's fork detector **must** reuse it (no second classifier). Export a small, typed public API (e.g. `event_ids_of(lines)`, `classify_prefix(root_ids, coord_ids) -> PrefixVerdict`).

### Subtask T014 – `seed_coord_surface`: lock, re-probe, collect, build, rename

- **Purpose**: contracts/seed.md steps 1-8. Readers must never see a partial seed (I-SEED-3), and PRIMARY files are never copied (I-SEED-9).
- **Steps**:
  1. Signature: `seed_coord_surface(request: SeedRequest) -> SeedReport`. `SeedRequest` is a frozen dataclass in `coord_seed.py` with: `repo_root`, `mission_slug`, `mission_dir_name`, `mid8`, `coordination_branch`, `coord_worktree`, `root_mission_dir`, `post_fix: bool`.
  2. **Lock**: `with feature_status_lock(repo_root, mission_dir_name):`. This is reentrant, so a caller already holding it (`BookkeepingTransaction`) does not deadlock. Map `FeatureStatusLockTimeoutError` by letting it propagate (it now carries `STATUS_LOCK_HELD`).
  3. **Re-probe**: `probe_coord_state(...)`. If it is MATERIALIZED, return `SeedReport()` (another writer won; idempotent, I-SEED-6).
  4. **Cleanup**: remove stale `<coord_wt>/kitty-specs/.<dir>.seed-*` dirs (crash leftovers).
  5. **Collect**: walk `root_mission_dir`. Keep a file iff `kind_for_mission_file(<mission-relative path>)` is a COORD-partition kind; use the taxonomy's partition predicate (`artifact_home_for` / the `_PLACEMENT_ARTIFACT_KINDS` membership exposed by `mission_runtime.artifacts`), not a hand list. Expected: `status.events.jsonl`, `status.json`, `decisions.events.jsonl`, `traces/*.md`, `tasks/*/review-cycle-*.md`, `issue-matrix.*`, `acceptance-matrix.json`. **Never** `meta.json`, `spec.md` or other PRIMARY files.
     - Note: WP12 later moves `DECISION_LEDGER` (`decisions/DM-*.md`, `index.json`) to PRIMARY. Rely on the taxonomy, not a list, so the seed follows automatically.
  6. **Coordination side**: when `post_fix` is set, the coordination-side content is the branch tip blobs (`git show <coord>:kitty-specs/<dir>/<file>`; list them with `git ls-tree -r --name-only <coord> -- kitty-specs/<dir>/`). Otherwise it is empty.
  7. **Logs**: `classify_prefix` per stream. A fork raises `CoordSeedForkRefused` **before writing anything** (state unchanged). The message names both paths, both refs, the first diverging ids, and the reconcile steps from contracts/seed.md errors table:
     - inspect with `spec-kitty doctor decisions`;
     - keep the coordination log;
     - re-open any root-only decisions with `spec-kitty agent decision open ...`;
     - then remove the root copy.
  8. **Non-log records** (I-SEED-5): coordination copy if present, else root copy. When both exist and differ, add a warning; the root is untouched.
  9. **Build**: write the full output tree into `<coord_wt>/kitty-specs/.<dir>.seed-<pid>-<ulid>/`, then `os.rename(temp, <coord_wt>/kitty-specs/<dir>)`. Ensure `<coord_wt>/kitty-specs/` exists first. If the target appears between re-probe and rename, the lock makes that impossible for cooperating writers. Still handle `FileExistsError`/`OSError` by removing the temp dir and re-probing once.
- **Files**: `src/specify_cli/coordination/coord_seed.py`.
- **Validation**: unit tests in T017. Keep each step a separate private function, so every function stays C901 ≤ 15.
- **Edge cases**:
  - **Create-time seed**: nothing to collect, so an empty Mission dir is created. WP06 relies on this; the report has empty `carried`.
  - **Windows**: `os.rename` onto an existing dir fails, which is acceptable because the target must be absent.

### Subtask T015 – Seed commit and repository-root restoration

- **Purpose**: contracts/seed.md steps 9-11; I-SEED-7 (durable), I-SEED-8 (root restoration); research D5 (ruling Q5: one commit on the coordination branch before the triggering write proceeds).
- **Steps**:
  1. After the rename, if anything was carried, call:
     ```python
     result = commit_for_mission(
         repo_root, mission_slug,
         files=tuple(<coord worktree absolute paths of carried files>),
         message=f"chore({mission_slug}): seed coordination surface",
         policy=ProtectionPolicy.resolve(repo_root),
         kind=MissionArtifactKind.STATUS_STATE,
     )
     ```
     The paths are under `.worktrees/`, so the router commits them in place.
  2. `committed` → `coord_commit = result.commit_hash`. Anything else (protected coordination ref, etc.) → **do not roll back the dir** (records are not lost); append a warning naming the reason. The next coordination commit carries them (data-model §7).
  3. **Root restoration**, per carried root file:
     - tracked and dirty → `git checkout -- <path>`;
     - untracked → unlink;
     - tracked and clean → untouched (pre-fix history stays: C-004).

     Use `git status --porcelain=v1 -z -- <path>` for the decision. Record `restored_root` (repository-relative paths).
  4. Log the whole `SeedReport` at `WARNING` (contract: callers that do not render it still surface it).
- **Files**: `src/specify_cli/coordination/coord_seed.py`.
- **Validation**: tests assert:
  - exactly one new commit on the coordination branch, whose tree carries the log;
  - the target branch did not move;
  - the root copy is back to `HEAD` (dirty case) or gone (untracked case);
  - `restored_root` lists them.
- **Edge cases**:
  - The commit runs inside the status lock, and `commit_for_mission` takes coordination status locks itself (`_coord_status_locks`, ≈L586). The lock is reentrant on the same key; add a test that proves no deadlock.
  - If WP05 has not landed yet in your lane, the router still commits in-place coordination paths today. Do not depend on WP05 behaviour.

### Subtask T016 – `establish_coord_write_location`: the state machine

- **Purpose**: The single answer to "where does a COORD write go" (data-model §2 table; contracts/write-location-accessor.md).
- **Steps**:
  1. Signature: `establish_coord_write_location(repo_root: Path, mission_slug: str, kind: MissionArtifactKind, *, owned: OwnedCheckout | None) -> WriteLocation`.
  2. Read `meta.json` from the PRIMARY partition (`read_primary_meta`, as `materialize_coord_surface_for_write` does). Resolve `mid8` and `coordination_branch`. No coordination branch → `WriteLocation(path=<primary dir>, surface="primary", coord_state_before=None, establishment=NONE)`.
  3. `state = probe_coord_state(...)`, then dispatch to one small handler per state:
     - **MATERIALIZED**: return the coordination Mission dir, establishment `NONE`. No side effects.
     - **UNMATERIALIZED**: call `materialize_coord_surface_for_write(repo_root, mission_slug)`. It raises `CoordinationWorktreeUnmaterialized` for a remote-only branch (#4970 parity, ruling Q1); let that propagate, because nothing has been written. Re-probe, then continue with the MATERIALIZED or EMPTY handler. Establishment is `MATERIALIZED` unless a seed follows.
     - **DELETED**: raise `CoordinationBranchDeleted`, with the recovery hint the existing exception carries.
     - **EMPTY, branch tree lacks the Mission dir** (`git ls-tree <coord> -- kitty-specs/<dir>` empty; pre-fix): `seed_coord_surface(post_fix=False)` → `SEEDED`.
     - **EMPTY, branch tree carries the Mission dir** (post-fix regression, D4, ruling Q3):
       1. `logger.warning` loudly (Mission, branch, "coordination Mission dir missing from worktree; restoring from branch tip");
       2. `git -C <coord_wt> checkout HEAD -- kitty-specs/<dir>`, which restores only committed content;
       3. if root-only COORD records exist, `seed_coord_surface(post_fix=True)` for them;
       4. return `RESTORED_FROM_BRANCH` with `restored_from_branch` filled.
  4. **Lock order** (I-SEED-2): materialization takes the workspace lock and releases it **before** the seed takes the status lock. Never acquire the status lock and then call `CoordinationWorkspace.resolve` from inside this function, **except** when the caller already holds the status lock. That nesting is the existing `BookkeepingTransaction.acquire` order (`transaction.py:292` then `:465`), and `workspace.py` never takes the status lock.
  5. **Owned checkout** (`owned is not None`): resolve the owned coordination workspace (the owned variant `runtime_bridge.py:363` uses). On failure raise `OWNED_COORDINATION_WORKSPACE_UNAVAILABLE` (existing `OwnedRefusalCode`).
  6. Every error message names the Mission, the coordination branch and a recovery command.
- **Files**: `src/specify_cli/coordination/coord_seed.py`.
- **Validation**: T017 matrix.
- **Edge cases**:
  - The path of a COORD kind must **exist** on return (contract postcondition).
  - PRIMARY-partition kinds are handled by WP04 before delegating. Still, defensively return the primary location for a PRIMARY kind (establishment NONE), and test it.

### Subtask T017 – Test matrix completion

- **Purpose**: Prove every row and invariant (NFR-002, SC-002 groundwork).
- **Steps**: in `tests/coordination/test_coord_seed.py`, using `tests._factories.coord_mission`:
  1. **State rows** (both `coord` and `lanes_with_coord`):
     - MATERIALIZED returns with no git change (`git rev-parse` of every ref unchanged; no new files);
     - UNMATERIALIZED-local → materialized, and the worktree exists;
     - remote-only → `CoordinationWorktreeUnmaterialized`, nothing written;
     - DELETED → `CoordinationBranchDeleted`;
     - pre-fix EMPTY → SEEDED;
     - post-fix EMPTY (delete the dir in the worktree after a seed) → loud warning (`caplog`) and RESTORED_FROM_BRANCH.
  2. **Prefix and fork**: `make_fork_fixture("root_uncommitted_coord_untracked")` → refused; both files are byte-identical before and after; the error carries both paths and the ids.
  3. **Idempotence**: a second call → no new commit, `carried` empty, no event id twice (`event_ids` helper).
  4. **Atomicity**: monkeypatch `os.rename` to raise once. Only `.seed-*` remains and the state is still EMPTY; the next call cleans it and seeds.
  5. **Root restoration**: dirty-tracked and untracked variants.
  6. **Lock reentrancy**: call `establish_coord_write_location` inside `with feature_status_lock(repo_root, dir_name):`. It completes, with no deadlock (use a timeout guard).
  7. **NFR-002**: across fixtures (a)-(d), the count of status events and decision index entries is never reduced by any call.
  8. **C-008 controls**: `lanes` and `single_branch` Missions → primary location, establishment NONE, no side effects.
- **Files**: `tests/coordination/test_coord_seed.py`, `tests/mission_runtime/test_write_location.py`.
- **Validation**: all green; diff coverage ≥ 90% on `coord_seed.py` and `write_location.py`.
- **Edge cases**: tests must not depend on create's current status-log placement. Use the explicit pre-fix builder.

## Targeted test surface

- Baseline: `make test-fast`.
- This WP:
  ```bash
  uv run --frozen pytest tests/coordination/test_coord_seed.py tests/mission_runtime/test_write_location.py -q
  uv run --frozen pytest tests/coordination/test_materialize_coord_surface.py tests/coordination/test_unmaterialized_remedy_text.py tests/specify_cli/coordination/test_coord_topology_states.py tests/specify_cli/coordination/test_coord_branch_remote_probe_4979.py -q
  uv run --frozen pytest $(grep -rl "FeatureStatusLockTimeoutError\|feature_status_lock" tests --include="test_*.py" | grep -v architectural) -q
  ```
- Named architectural gate files: `tests/architectural/test_layer_rules.py` (mission_runtime must not grow its outbound ledger), `tests/architectural/test_no_dead_symbols.py` (new public symbols must have callers; WP04 adds the caller, so declare `__all__` and keep public names minimal).
- Never run the bare `tests/architectural/`, any e2e/integration directory, performance/stress suites or `make test-full` (NO_FULL_HEAVY_SUITES_IN_MISSION, C-006).
- Record commands and counts in the Activity Log. Classify unrelated reds with the CLAUDE.md baseline-red gotcha.
- Named architectural gate (post-tasks squad P-M3): `uv run --frozen pytest tests/architectural/test_no_worktree_name_guess.py -q`.
- New file: `uv run --frozen pytest tests/coordination/test_event_prefix.py -q`.

## Quality gates

- C901 ≤ 15 per function (NFR-004). One handler per state; the seed steps are separate helpers.
- `ruff check`, `ruff format --check` and `mypy --strict` are clean on changed files (NFR-005), with no new suppressions.
- ≥ 90% coverage of new lines, and a focused test for every branch, including error branches (NFR-003).
- New public symbols: `tests/architectural/test_no_dead_symbols.py`. If it flags `establish_coord_write_location` as callerless until WP04, record that in the Activity Log and coordinate (WP04 is the immediate dependent); do not add a fake caller.

## Issues

Issues: #5519 #2533

## Definition of Done

- `write_location.py` (types) and `coord_seed.py` (prefix rule, seed, establish) exist, are typed and are documented.
- `FeatureStatusLockTimeoutError.error_code == "STATUS_LOCK_HELD"`.
- The red-first commit precedes the implementation commits. Every state row, prefix/fork, idempotence, atomicity, restoration, reentrancy, NFR-002 and C-008 test is green.
- No PRIMARY file is ever written to the coordination Mission dir. A fork leaves both surfaces untouched.
- Static gates are clean; layer rules are green.

## Risks & Mitigations

- **Deadlock between the status lock and the workspace lock.** Mitigation: the I-SEED-2 order, plus an explicit reentrancy test with a timeout.
- **Partial seed visible to readers.** Mitigation: temp dir plus a single rename, and a crash-simulation test.
- **Silent data loss on a malformed log line.** Mitigation: parse errors refuse; nothing is skipped.
- **Import cycle mission_runtime ↔ specify_cli.** Mitigation: types-only `write_location.py`, the error class in `coord_seed.py`, and a lazy import in WP04.
- **Seed commit refused** (protected coordination ref). Mitigation: the dir stays and a warning is reported (data-model §7); a test covers it.

## Review Guidance

- Reviewer: opus, distinct from the implementer.
- Verify red→green: the red-first tests (T012) are RED on the WP's base (lane base before the fix commits: missing module/behaviour, and the write-side assertion fails) and GREEN on the final commit.
- Check specifically:
  - fork refusal writes nothing;
  - the prefix rule is byte-faithful;
  - lock order;
  - `read_dir` still falls back for reads (C-002);
  - the seed commit lands on the coordination branch only, and the target ref is unchanged;
  - root restoration never rewrites committed history (C-004).

## Activity Log

> **CRITICAL**: Activity log entries MUST be in chronological order (oldest first, newest last).

### How to Add Activity Log Entries

**When adding an entry**:

1. Scroll to the bottom of this Activity Log section
2. **APPEND the new entry at the END** (do NOT prepend or insert in middle)
3. Use exact format: `- YYYY-MM-DDTHH:MM:SSZ – agent_id – <action>`
4. Timestamp MUST be current time in UTC (check with `date -u "+%Y-%m-%dT%H:%M:%SZ"`)
5. Agent ID should identify who made the change (claude-sonnet-4-5, codex, etc.)

**Format**:

```
- YYYY-MM-DDTHH:MM:SSZ – <agent_id> – <brief action description>
```

**Common mistakes (DO NOT DO THIS)**:

- Adding new entry at the top (breaks chronological order)
- Using future timestamps (causes acceptance validation to fail)
- Inserting in middle instead of appending to end

**Why this matters**: The acceptance system reads the LAST activity log entry as the current state. If entries are out of order, acceptance will fail even when the work is complete.

**Initial entry**:

- 2026-10-01T08:36:27Z – system – Prompt created.

---

### Updating Status

Status is managed via `status.events.jsonl`. Use `spec-kitty agent tasks move-task <WPID> --to <status>` to change WP status.
