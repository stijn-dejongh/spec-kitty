# Post-tasks adversarial squad: findings and dispositions

- **Procedure:** `adversarial-squad-deployment`, point-cut **post-tasks**.
- **Squad:** two profile-loaded lenses, read-only, against `tasks.md` and the 22 WP prompts, as written before this fold.
  - **reviewer-renata** (fidelity: does the decomposition deliver every FR, US and scenario): verdict **READY-WITH-FOLDS**.
  - **paula-patterns** (sequencing, ownership, boundary leaks): verdict **READY-WITH-FOLDS**.
- **Blockers:** none.
- **Outcome:** every finding was folded into `tasks.md` and the WP prompts; none was deferred.
- **Validation:** after the folds, `spec-kitty agent mission finalize-tasks --validate-only` passes with 18 lanes, no lane cycle and no ownership warnings. `map-requirements` reports 28/28 functional requirements mapped.

## Structural deltas (summary)

| Change | Why |
|---|---|
| T002/T003/T004 moved WP01 → WP13/WP14/WP15 (each WP's tidy-first first commit). WP01 keeps T001/T005/T006/T007 | P-m7: frees WP13/14/15 from lane A. Lanes went from 16 to 18 with no cycle |
| New dependencies: WP08 → WP19, WP09 → WP07, WP17 → WP09, WP19 → WP02 | R-M3, P-M1, P-M4, P-m6 |
| New subtask T119 (WP21) | R-M1 |
| New owned files: WP03 `coordination/event_prefix.py` (+ test); WP07 `test_coord_read_seam_callers.py`; WP08 `workflow.py`, `workflow_cores.py`, `workflow_executor.py`, `test_analysis_report_rehome.py`, a new reject→fix-mode test; WP09 six `DecisionGitLog` caller test files; WP10 `tracer_append.py` (+ test); WP12 `test_artifact_partition_mapping.py`, `test_coherence_integrity.py`; WP15 `test_finalize_extracted_helpers.py` | R-M2, R-M3, P-M1, P-M6, P-m3, R-m5, P-m7 |
| Named post-consolidation fold recorded in `tasks.md`: retire the router's legacy root-staging copy | P-M2 (it cannot be a WP without a lane cycle) |

## reviewer-renata (fidelity)

| ID | Severity | Finding (short) | Disposition | Where |
|----|----------|-----------------|-------------|-------|
| R-M1 | MAJOR | US4.8 / FR-009b fresh-clone durability is not delivered by any WP | accepted. New subtask T119: a post-fix Mission opens a decision, commits it via spec-commit/setup-plan, then `git clone`; `decision verify` and `doctor decisions` must find every decision id. An extra assertion checks that setup-plan or finalize commits an uncommitted ledger on the target. FR-009b mapped to WP21 | WP21 T119, DoD; tasks.md WP21 |
| R-M2 | MAJOR | `tracer_append.py:135-163` hand-renders caller-surface fields (masking) | accepted. WP10 owns it and renders through `commit_outcome_payload` / `render_commit_outcome`, with a new test. WP20 adds it to the consumer-pin floor. "Report rather than edit" removed | WP10 T055, surface; WP20 T110, DoD |
| R-M3 | MAJOR | WP08 reject→fix-mode readers are only "verified or reported" | changed. A CLI-level reject-then-fix-mode test is now a **blocking** DoD item. WP08 owns `workflow.py`, `workflow_cores.py` and `workflow_executor.py`, so it fixes readers there. `workflow.py` is shared with WP19, so WP08 depends on WP19 and runs in its lane | WP08 T044 step 6, DoD, surface; frontmatter |
| R-M4 | MAJOR | The WP13/14/15 red-first fixture premise is false at their lane base (create does not seed yet) | accepted. WP02 gains `make_coord_mission(..., materialized=True)`, built explicitly with git and asserting MATERIALIZED through the production probe (WP02 cannot depend on WP04, which would be a cycle). WP13/14/15 assert their preconditions before invoking the CLI. No WP13 → WP06 edge was added | WP02 T009; WP13 T069, WP14 T074, WP15 T079 |
| R-M5 | MAJOR | No integrated re-run of the Mission's new tests on the post-WP06 tree | accepted. WP20 runs every new test file by name (35 files, plus the two fold destinations), with counts recorded | WP20 surface, DoD |
| R-M6 | MAJOR | WP16 red reasons are not derived from its real lane base | accepted. Per-path red reasons are re-derived on the WP01–05, WP11, WP12 base and recorded first. R9 now targets paths that still disagree on that base (for example `traces/*`), because `decisions/*` already agree after WP12 | WP16 T085 |
| R-M7 | MAJOR | `ensure_coordination_branch` is not driven by any test | accepted. Two tests: an expected-divergence existing branch is returned without raising, and a genuinely diverged branch still raises | WP06 T034, DoD |
| R-M8 | MAJOR | FR-016 relocation of the adopted reproductions is missing | accepted. After GREEN, R2/R2b fold into `tests/coordination/test_commit_router.py` and R1/R1b into `tests/core/test_mission_creation_decomposition.py`. The adopted standalone files and their "stays red on main" markers are removed | WP05 DoD, WP06 DoD, WP20 surface note |
| R-m1 | MINOR | WP17 R14 uses one fork fixture | accepted. Parametrized over fork fixtures (a), (b) and (c) | WP17 T090 |
| R-m2 | MINOR | WP16 does not prove each leg is load-bearing | accepted. A one-time local revert of each half (raw commit makes R7 red; the L425 root-join makes R8 red) is recorded in the activity log | WP16 T086 |
| R-m3 | MINOR | The WP07 move-task matrix lacks a post-fix EMPTY row | accepted. New row: remove the coordination Mission dir, run move-task, assert the warning, the restore from the branch tip and no root write | WP07 T037 |
| R-m4 | MINOR | The real default path (protected primary, `--pr-bound`, no `--topology`) is not exercised | accepted. Added as a parametrization asserting `meta.topology == coord` plus US1.1/US1.4 | WP06 T030 |
| R-m5 | MINOR | The legacy `DecisionGitLog` composer is kept as an optional fallback | changed. `mission_dir` is required, the legacy composer is deleted, and the six test callers are migrated (now owned by WP09) | WP09 T051; frontmatter |
| R-m6 | MINOR | SC-001 history probe could be vacuous | accepted. A planted COORD-path commit on the target in a throwaway run must turn the probe red; recorded | WP21 T114 |
| R-m7 | MINOR | T004 wording omits `_commit_planning_pin_refresh_locked`; `_print_acceptance_result` (C901 13) is unwatched | accepted. T004 wording fixed (now in WP15). WP16 quality gates watch `_print_acceptance_result` | tasks.md T004; WP16 quality gates |
| R-m8 | MINOR | R12 could pass vacuously | accepted. Precondition: a base-shaped advance does move the target (clean checkout, target an ancestor of the coordination tip) | WP05 T023 |

## paula-patterns (sequencing)

| ID | Severity | Finding (short) | Disposition | Where |
|----|----------|-----------------|-------------|-------|
| P-M1 | MAJOR | `test_coord_read_seam_callers.py` is flipped concurrently by WP07 and WP09; `test_commit_router.py` imports `_coord_feature_dir`, which WP07 deletes | accepted. WP07 owns and re-pins the file, and WP09 depends on WP07 (no lane cycle). WP09 also runs `test_decision_fresh_coord_5113.py` by name. WP07 declares the out-of-map edit to `test_commit_router.py` (≈L953, ≈L1012) after WP05, with rationale | WP07 T038, surface; WP09 context, surface; tasks.md lane notes |
| P-M2 | MAJOR | Owning-surface judgement only covers STATUS_STATE/DECISION_LOG; the legacy `shutil.copy2` root-staging copy has no retirement | accepted. The judgement extends to all COORD kinds, including the `COORD_RECORD_IN_ROOT_CHECKOUT` skip, with a test per kind. Retiring the legacy copy is recorded in tasks.md as a named post-consolidation fold, because as a WP it would create a lane cycle. WP20's gate module carries a pointer | WP05 T027, T028; tasks.md; WP20 T110 |
| P-M3 | MAJOR | Consumers derive the checkout root by guessing (`.path.parent.parent`) | accepted. `WriteLocation.checkout_root` added (WP03 defines and populates it, WP04 populates PRIMARY). WP07, WP09, WP16 and WP18 consume it. `test_no_worktree_name_guess.py` becomes a named gate for WP03, WP07, WP09 and WP17 | WP03 T012, surface; WP04 T018; WP07 T038; WP09 T051; WP16 T089; WP18 T099; WP17 T091 |
| P-M4 | MAJOR | `decisions.events.jsonl` dir-name mismatch (`<slug>` vs `coord_mission_dir_name`) | accepted. WP09 either proves no reachable shape differs (pinned test) or folds the legacy stream once under the seed lock with the WP03 classifier. WP17 depends on WP09 and composes names only via `lanes.branch_naming` | WP09 T051; WP17 T091; frontmatter |
| P-M5 | MAJOR | WP16 T088 risks a new `_is_coordination_owned()` classifier | accepted. WP05 exports the router's per-path partition predicate as a public helper, and WP16's gate calls it | WP05 T025, DoD; WP16 T088 |
| P-M6 | MAJOR | WP17 could re-implement the prefix/fork classifier and the index union | accepted. WP03 puts the pure classifier in `coordination/event_prefix.py` (owned, tested), and WP17 must reuse it. WP11 exposes a pure `union_decision_index(ours, theirs)` that the merge driver and WP17's repair both use | WP03 T013; WP11 T060; WP17 T091, T094 |
| P-m1 | MINOR | The WP17 targeted surface misses the consolidation guards; T096 touches unowned callers | accepted. WP18's T102 guard list is copied into WP17's surface. Caller rendering in `consolidate.py`/`mission_type.py` is limited to verification and reporting | WP17 surface, T096 |
| P-m2 | MINOR | The WP05 risk text inverts the I-SEED-2 lock order | accepted. Now reads: status → workspace is permitted; workspace → status is forbidden | WP05 risks |
| P-m3 | MINOR | WP12/WP08 re-pins not declared in owned_files; wrong `test_coherence.py` name | accepted. `test_artifact_partition_mapping.py` and `test_coherence_integrity.py` added to WP12 (the name is fixed), and `test_analysis_report_rehome.py` added to WP08 | WP12 T066, frontmatter; WP08 frontmatter, DoD |
| P-m5 | MINOR | Cross-lane fixture semantics are unstated | accepted. One line in each writer and consumer WP (WP02, WP07–WP10, WP13–WP16, WP18): pre-fix assertions use `make_prefix_coord_mission`, and `make_coord_mission` only for shape-agnostic invariants or `materialized=True` | those WPs' Context & Constraints |
| P-m6 | MINOR | WP19 hand-rolls its fixture | accepted. WP19 depends on WP02 and uses the factory | WP19 T103; frontmatter; tasks.md |
| P-m7 | MINOR | Lane A serializes WP13/14/15 because of WP01's extractions | accepted (condition met). T002/T003/T004 moved to WP13/WP14/WP15 as tidy-first first commits. validate-only shows no new cycle and clean ownership; lanes went from 16 to 18. Subtask ids keep their global numbers, so T002–T004 appear out of numeric order in those WPs, which avoids a global renumber that would risk corrupting quoted foreign T-ids | WP01, WP13, WP14, WP15; tasks.md |

## Tooling friction noted

- `spec-kitty agent tasks map-requirements` rewrites the WP frontmatter and drops the `agent`, `assignee` and `shell_pid` keys. They were restored after this fold. The mutating `finalize-tasks` may drop them again, so re-check `agent: claude` per canonical step 8a after it runs.
