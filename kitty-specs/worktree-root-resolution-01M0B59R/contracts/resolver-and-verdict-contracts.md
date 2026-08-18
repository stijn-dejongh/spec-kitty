# Contracts: Resolver Seam & Verdict-CLI Parity

This is a CLI + internal-resolver mission; contracts are **behavioral interface contracts**, not HTTP schemas. Each contract is testable and pinned to its FR(s). "MUST" is a normative requirement.

## C-1 — Checkout-kind classifier (FR-001)

**Interface**: a pure classifier `classify_checkout(cwd) -> CheckoutKind`.

- MUST return `PRIMARY` when `cwd`'s `.git` is a directory AND the checkout is not a secondary clone of another in-scope primary.
- MUST return `STANDALONE_CLONE` when `.git` is a directory but the checkout is an independent clone (its own primary) — and MUST set `primary_root = checkout_root` (never an unrelated path).
- MUST return `LINKED_WORKTREE` when `.git` is a file whose `gitdir:` pointer has `.git/worktrees/<name>` topology (not submodule `.git/modules/*`, not separate-git-dir).
- MUST NOT re-anchor: for `LINKED_WORKTREE`, `checkout_root` is the worktree; `primary_root` is the main checkout, and write-target resolution defaults to `checkout_root`.
- The four resolver functions (`find_repo_root`, `resolve_canonical_root`, `predict_lane_worktree`, `locate_project_root`/`_get_main_repo_root`) MUST consult this classifier rather than re-deriving `.git` classification.

**Contract test**: given fixtures {primary, linked-worktree, standalone-clone, submodule, separate-git-dir}, assert the returned `kind` and that no clone's `primary_root` points outside itself.

## C-2 — Write-target resolution & refusal (FR-002…FR-009, NFR-003)

**Interface**: `resolve_write_target(command, cwd) -> WriteTarget`.

- MUST return `WRITE_INVOKING` with `target_root == checkout_root` for a `PRIMARY` or `STANDALONE_CLONE` invocation.
- For a `LINKED_WORKTREE`, MUST either return `WRITE_INVOKING` targeting the worktree, or `REFUSE` — never silently target `primary_root`.
- On `REFUSE`, the emitted CLI message MUST contain the concrete `refusal_path` verbatim (the checkout it would otherwise have written to). No generic-only refusal.
- `intake --force` MUST NOT overwrite a shared untracked slot owned by a different mission/worktree without an identity check.

**Consumers bound by this contract**: `intake` (FR-002), `doctor tool-surfaces --fix` (FR-003), `doctor mission-state --fix` (FR-004, FR-009), `migrate backfill-runtime-state` (FR-005), `--owned-checkout` mission create (FR-007).

**Contract test**: from a linked worktree and a standalone clone, each consumer either writes into the invoking checkout or refuses with a message asserting the exact `refusal_path`.

## C-3 — No false-green guard (FR-005, FR-006)

- `setup-plan` MUST resolve the branch from the invoking checkout / mission `meta.json`, and MUST NOT report `branch_matches_target: true` when the value was read from a redirected (re-anchored) path.
- `migrate backfill-runtime-state` MUST write into the linked worktree and its cutover guard MUST read the same path it wrote.

**Contract test**: run from a worktree whose `meta.json` names branch X while primary is on branch Y; assert the guard reflects X (or reports honest disagreement), never a false `true` from Y.

## C-4 — `.kittify` containment boundary (FR-008)

- cwd-ancestor `.kittify` discovery MUST stop at an explicit containment boundary and MUST NOT cross it to a parent checkout.

**Contract test**: nested checkout with an inner `.kittify`; assert discovery resolves to the inner boundary, not the outer.

## C-5 — Unified review-verdict CLI path (FR-010, FR-012, FR-013)

- `agent status emit` MUST accept `--review-result-json <json>`, validated by the **same** `_parse_review_result_json` used by `orchestrator-api transition`.
- The parsed `review_result` MUST be threaded into the `TransitionRequest`.
- A WP MUST be walkable `in_progress → for_review → in_review → approved → done` via `agent status emit` alone.
- `agent status emit --help` MUST document only functional paths; the misleading `in_review`/`--evidence-json` verdict example MUST be corrected.
- The `in_review → approved` guard MUST admit the `ReviewResult` path on both surfaces.

**Contract test**: identical verdict JSON produces identical validation outcome on both surfaces; a full emit-only lifecycle walk reaches `done`; `--help` snapshot contains no non-functional example.

## C-6 — Shared, topology-aware `for_review` commit-gate (FR-011)

- The `for_review` commit-gate MUST be one shared implementation enforced on both `agent status emit` and `orchestrator-api transition`.
- It MUST be topology-aware: a standalone clone is evaluated on **commit state**, not failed on topology.

**Contract test**: the gate yields the same verdict for the same repo state on both surfaces across the topology matrix {primary, worktree, clone}; a clone with satisfied commits passes.

## C-7 — Snapshot round-trip & audit registration (FR-014, FR-015, FR-016, FR-018)

- Replaying any persisted snapshot's event log MUST reproduce every field present in the snapshot (round-trip property; includes `review_result`).
- A review-carrying event row MUST audit clean — `review_result` registered in `status_event_row`; 0 `UNKNOWN_SHAPE`.
- The shape-registry drift test MUST fail when a persisted shape is unregistered (real assertion, not a subset tautology).
- After the writer migration, persisted coordination-key rows MUST carry the registered shape.

**Contract test**: property test over generated event logs asserting snapshot⊆replay; audit a `review_result` row and assert no `UNKNOWN_SHAPE`; add a deliberately-unregistered shape and assert the drift test goes red.

## C-8 — Review-cycle write-side kind (FR-017)

- `review/cycle.py` write-side MUST emit the correct artifact kind (not `WORK_PACKAGE_TASK`).
- `resolve_review_verdict_facts` (`tasks_verdict_persistence.py:404`) MUST be migrated to the new kind and `test_analysis_report_rehome` re-verified green.

**Contract test**: a review-cycle write lands under the review-cycle kind; verdict-facts resolution reads it; the rehome test passes.

## Cross-cutting: red-first (NFR-001)

Every contract above whose FR is release-blocking MUST ship with a `@pytest.mark.regression` test, pinned to its issue, that is **red on `upstream/main`** and green after the fix, exercised through the real CLI entry point.
