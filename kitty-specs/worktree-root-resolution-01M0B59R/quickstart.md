# Quickstart: Reproducing & Verifying the Invariants

This mission is red-first (NFR-001). Each behavioral invariant has a reproduction that must be **red on `upstream/main`** and **green after the fix**, driven through the real CLI entry point and pinned to its issue with `@pytest.mark.regression`.

## Setup

```bash
# From the primary checkout (NOT a worktree — this mission fixes that footgun):
git rev-parse --show-toplevel        # confirm you are in the intended checkout
pip install -e .                     # ensure spec-kitty shells out to THIS tree (stale-install gotcha)
```

## Reproducing each invariant (red-first)

### SC-001 — No silent re-anchor on write (FR-001…FR-009)

```bash
# Create a standalone clone and a linked worktree of a throwaway mission repo, then:
#   run intake / doctor --fix / migrate backfill-runtime-state / --owned-checkout create
#   from inside each, and assert the write landed in the invoking checkout (or refused, naming the path).
# Red on base: the write silently lands in the primary checkout.
pytest tests/ -k "regression and root_resolution" -n0 -q
```

### SC-002 — No false-green guard (FR-005, FR-006)

```bash
# Run setup-plan / migrate backfill-runtime-state from a worktree whose meta.json names a branch.
# Assert the guard does NOT report branch_matches_target: true from a redirected read.
pytest tests/ -k "regression and (setup_plan_branch or cutover_guard)" -n0 -q
```

### SC-003 — Clone ≠ primary (FR-009)

```bash
# doctor mission-state --fix inside a standalone clone must rewrite the clone (or refuse),
# never an unrelated primary, and the manifest must enumerate every field touched.
pytest tests/ -k "regression and clone_reanchor" -n0 -q
```

### SC-004 — One review-verdict path, both surfaces (FR-010…FR-013)

```bash
# Walk a WP in_progress -> done via `agent status emit` ALONE with a structured verdict:
spec-kitty agent status emit --wp WP01 --to for_review ...
spec-kitty agent status emit --wp WP01 --to in_review ...
spec-kitty agent status emit --wp WP01 --to approved --review-result-json '{"verdict":"approve"}'
# Assert: same for_review gate verdict on both surfaces; topology-aware; --help shows only working paths.
pytest tests/ -k "regression and (verdict_parity or for_review_gate)" -n0 -q
spec-kitty agent status emit --help    # no non-functional in_review example
```

### SC-005 — Snapshots round-trip & audit clean (FR-014…FR-016, FR-018)

```bash
# Replay an event log carrying review_result; assert no snapshot field is missing on replay,
# and the event row audits with 0 UNKNOWN_SHAPE.
pytest tests/ -k "regression and (round_trip or shape_registry)" -n0 -q
```

## Full verification (post-fix)

```bash
PWHEADLESS=1 pytest tests/ -n auto --dist loadfile -p no:cacheprovider          # parallel suite
PWHEADLESS=1 pytest tests/sync/test_orphan_sweep.py -n0 -q                       # serial daemon/port tests
pytest tests/architectural/test_no_legacy_terminology.py                        # terminology gate
ruff check . && mypy src/                                                        # zero issues
spec-kitty analyze --mission worktree-root-resolution-01M0B59R                   # cross-artifact consistency
```

## Baseline-red note

Before treating any failure as yours, classify per the charter's baseline-red gotcha: pre-existing known-P0 reds (leave red), CI-env failures (auth/sync toggles), and stale-install false reds (reinstall). Only failures red on this branch **and** green on `upstream/main` are in scope.
