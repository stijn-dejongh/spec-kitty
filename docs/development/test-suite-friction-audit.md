# Test-Suite Friction Audit — "Tests as scaffold, not friction"

**Date**: 2026-06-22
**Epic**: [#2071](https://github.com/Priivacy-ai/spec-kitty/issues/2071)
**Method**: four profile-loaded review lenses (debugger-debbie, reviewer-renata, randy-reducer) +
a paula-patterns second-opinion on the randy findings most at risk of being symptomatic.
**Suite scale**: ~1,800 test files, ~500K LOC, 36 conftests.

## Verdict on the theory (honest)

The operator's theory — *the test suite has degraded from scaffold into friction* — is
**confirmed in its core but materially narrower than the alarming headline**. All three
investigation lenses independently tempered it:

- **Not pervasive tautological-green.** The egregious accidental-pass forms came back **clean**:
  `assert result == mock.return_value` → **0 occurrences**; a test mocking the exact SUT it names
  → **0 confirmed**. The high mock density (~4,500 `@patch`) is overwhelmingly CLI-collaborator
  *style*, not false-green.
- **The "same dir asserted twice" memory is mostly a false alarm.** The `read_dir == write_dir`
  and triple-equality assertions the operator remembered are, on inspection, **correct
  convergence/collapse invariants** (`test_execution_context_parity.py`,
  `test_aggregate_surface_resolution.py`, `test_cli_status_mediation.py`) — desired contracts,
  not codified bugs.
- **The suite has gold-standard regions.** `test_execution_context_parity.py` (real subprocess +
  real git worktrees + on-disk event logs, with explicit **anti-vacuity injection proofs**),
  `tests/git/test_protection_preserved.py` (converged ATDD ratchet), auth single-flight, feature
  creation, orchestrator integration — these are models to emulate, not friction.

**Where the theory IS true, it is dense and localized.** The center of gravity is three clusters,
not a pervasive rot:

1. **`file:line`-keyed architectural ratchets** (systemic, cross-confirmed by renata + randy) —
   the real "false-red on a correct change → revert the good change" engine.
2. **Security xfail-masking** (renata, localized but pure) — vulnerabilities codified as
   acceptable; *fixing the bug turns the test red*.
3. **Duplicate-knowledge meta scaffold** (randy, structural) — N hand-rolled schema sources that
   drift on every meta.json change.

Plus a contained band of mock-wiring "assert HOW not WHAT" tests and one weak directory
(`sync/tracker/`).

## Consolidated findings → ticket map

Deduped across lenses; severity and the **structural** fix (with paula's corrections applied to
the randy items, so fixes *drain* debt rather than re-home it).

### CT1 — Re-key `file:line` architectural ratchets to stable anchors **+ drain deferred-defect entries** — HIGH
*Sources: renata F3, randy T3, paula T3 correction (cross-confirmed, the systemic finding).*

- **Evidence**: `tests/architectural/test_single_mission_surface_resolver.py` `_ALLOWLISTED_RAW_JOINS`
  keys entries by raw `surface_resolver.py:472`, `_read_path_resolver.py:885`,
  `mission_creation.py:328`, `cycle.py:185`; in-file comments confess repeated hand-re-keying
  (`:511 → :641 → :737 → :744`; `:518→:472`; `:869→:885`). `test_no_write_side_rederivation.py:84`
  has a raw `("status_transition.py", 336)` tuple **and a private verbatim copy** of
  `_ratchet_keys.code_tokens_by_line`. The drift-proof primitive `_ratchet_keys.composite_key`
  (qualname + normalized token-line) **already exists but is adopted by only one test**
  (`test_no_worktree_name_guess.py`). ~113 baseline/allowlist refs; 8 files carry "re-key/drifted/
  stays green" notes.
- **Failure mode**: a correct, behavior-neutral edit above a pinned line shifts the number and
  turns the architectural gate RED, forcing a manual re-key in the same PR — friction by
  construction; bit this cycle repeatedly.
- **Structural fix (two tracked obligations — do NOT conflate, per paula)**:
  1. **Re-key** all surviving entries onto `_ratchet_keys.composite_key`; delete the private
     `_code_tokens_by_line` copy; converge `test_no_write_side_rederivation.py` onto the shared
     primitive. (Churn fix.)
  2. **Drain with named owners**: classify each entry as **PERMANENT-BY-DESIGN** (the DIAG /
     topology-blind-by-design seam joins — annotate as permanent so they aren't mistaken for debt)
     vs **DEFERRED-DEFECT** (`status_transition.py:336` → the #1716 write-surface-selection ladder;
     the `:295`/C-007 token-copy deferral). Each deferred entry carries its tracker link + a
     **non-vacuous drain condition** — when the fix lands, the entry is *removed*, not re-keyed.
- **⚠ Mission link**: `status_transition.py:336` is the deferred **#1716** write-surface ladder —
  the exact split-brain mission `01KVPR00` (FR-007) closes. See "Mission-impact flags" below.

### CT2 — De-theater the security path-validation tests — HIGH
*Source: renata F1 (the purest instance of the theory).*

- **Evidence**: `tests/adversarial/test_path_validation.py` — every malicious-path test has an
  escape hatch `if is_valid: pytest.xfail("Traversal not blocked in current implementation")`.
  8 traversal/case/symlink/home/absolute/null-byte tests are titled "must be rejected" but
  **green-pass when the path is accepted** (a live security gap); fixing `validate_deliverables_path`
  turns them XPASS — *the suite penalizes the fix*. ~5 sibling tests have **no assertions at all**
  (pure no-ops). This file holds 7 of the suite's 12 total `pytest.xfail` calls.
- **Structural fix**: decide the real `validate_deliverables_path` contract, then either (a) make
  the tests strict failures pinning the desired rejection (RED until fixed, ATDD-style — model:
  `tests/git/test_protection_preserved.py`), or (b) if the validator legitimately delegates
  containment elsewhere, delete these and test the real boundary. Remove the no-op tests.

### CT3 — Meta/mission test factory **delegating to the production `create_mission_core()` seam** — L
*Sources: randy T1 + T2, paula T1 correction.*

- **Evidence**: 329 test files write `meta.json` directly; **53** `_write_meta` + **38**
  `_seed_mission`/`_setup_feature` copies; `tests/_factories/__init__.py` is a 0-byte stub with
  zero importers; the `feature_repo` fixture (conftest.py:696) writes **no meta.json at all** (no
  `mission_id`/`mid8`). 385 hardcoded ULID literals, mostly handcrafted placeholders
  (`01AAA…`×41, `01HXYZ…`×36, `01TEST…`×26) — violating the realistic-test-data rule.
- **Structural fix (paula correction — NOT a parallel hand-roll)**: `tests/_factories.make_mission()`
  must be a **thin wrapper that delegates to `create_mission_core()`** (mission_creation.py:201 —
  the documented programmatic API; the CLI `create()` is a thin wrapper over it), applying
  test-specific `**overrides` on the production-shaped meta. One schema authority; a new required
  field flows to every test automatically. **If `create_mission_core` lacks a clean
  side-effect-free / no-coordination-branch / no-fan-out test entrypoint, *that gap is the real
  finding*** — add the lever, don't fork the schema. Then migrate `_write_meta`×53; the 329 raw
  writers are the long-tail drain. Bundle production-shaped ULID fixtures + ban the placeholder
  patterns.

### CT4 — Re-point mock-wiring "assert HOW not WHAT" tests to observable contracts — M
*Sources: renata F4 (~10), debbie T1 (`sync/tracker/` ~12), debbie T3 (status/merge wiring band).*

- **Evidence**: `test_dashboard/test_api_handler.py::TestDossierEndpointRouting::*` (mock
  `DossierAPIHandler`, assert internal forwarding, never the HTTP response); `agent/glossary/
  test_event_emission.py::*` (assert event class instantiated/forwarded, not persisted);
  `cli/commands/test_charter_lint.py::*` (assert CLI→`LintEngine.run` kwargs, not rendered
  findings); `sync/tracker/test_service.py::*` (patch the backend method they claim to verify);
  `test_origin.py::test_saas_first_ordering_set_origin_ticket_not_called` (assert_not_called on a
  patched name — an inline/renamed write still passes). Redundant status/merge wiring twins
  (`status/test_agent_status_emit_aggregate_wiring.py::test_emit_does_not_call_transactional_emit_directly`,
  `::test_command_module_has_no_direct_transactional_reference` — reads module **source as text**).
- **Structural fix**: re-point each to the observable contract (HTTP status+body; persisted
  event/JSONL; rendered lint output; config persisted to disk). For the status/merge band, keep the
  one real-outcome test per seam (`test_done_events_committed_to_git`, the differential-equivalence
  + JSON-contract tests) and demote/delete the wiring twins.
- **⚠ Mission link**: the status/merge emit-wiring tests wrap the **emit/safe_commit seams FR-007/
  FR-009 rewrite** — they may false-red on a behavior-preserving refactor. See below.

### CT5 — Stale golden-count assertions + fakeable-DoD / dead-assertion tail — S
*Sources: renata F2 + F5, debbie T2.*

- **Evidence**: `status/test_models.py::test_lane_enum_has_nine_values` asserts `len(Lane) == 10`
  (name/docstring drift after `Lane.GENESIS`); 182-wide tail of `assert len(...) == N` golden
  counts where an adjacent set-equality already covers the contract. Vacuous/dead:
  `sync/tracker/test_local_service.py:420` (`"import" not in source or …` is always-true);
  `::test_map_add_and_list_roundtrip` (dead patch, overclaiming name);
  `cross_cutting/test_gitignore_manager_unit.py::test_result_object_structure` (6 `hasattr`, no
  values); `doctrine/test_structure_templates.py::test_structure_templates_exist` (`.exists()`
  only); `release/test_release_payload_draft.py` + `doctrine/test_relationship_fields_rejected.py`
  (hasattr/absence only).
- **Structural fix**: rename the lane test; drop redundant `len()==N` where set-equality exists
  (keep counts only where cardinality is the contract); add a content/behavior assertion next to
  each existence/hasattr check; delete the 2 dead assertions.

### CT6 — (Adjacent, deprecation-hygiene) Re-point 77 `specify_cli.next` shim importers — M
*Source: randy T4. Flagged as ADJACENT to test-friction (it is deprecation-migration), include
only if the epic owner wants it here; otherwise it belongs to the shared-package-boundary cutover.*

- **Evidence**: `src/specify_cli/next/` is a deprecation shim (`__removal_release__ = "3.3.0"`); 77
  test files still import through it (incl. the two largest bridge test files, ~1,727 + ~1,483 LOC).
- **Fix**: mechanical sweep re-pointing importers to `runtime.next` ahead of the 3.3.0 cut.

### CT7 — Test-hygiene directive/styleguide + guard (recurrence prevention) — M
*The epic's "don't recur" obligation, beyond remediation.*

- Codify the anti-patterns as doctrine: no xfail-masking a defect (use ATDD strict-RED); no
  `file:line` ratchets (anchor on symbol/AST/fingerprint via `_ratchet_keys`); test fixtures
  delegate to production seams (single schema authority); assert observable contracts, not wiring;
  production-shaped test data. Pair with a guard/ratchet where mechanizable (e.g. ban
  `pytest.xfail` with a "not blocked/implemented" reason; ban new raw `file.py:NNN` ratchet keys).
  Prior art: the post-merge AST stale-assertion analyzer (mission 068, `src/specify_cli/post_merge/`).

## Where the theory does NOT hold (counterweight — do NOT "fix" these)

- Convergence-invariant assertions (`read_dir == write_dir` for flattened topology, triple-equality
  collapse) — **correct contracts**.
- `test_execution_context_parity.py` — gold-standard ATDD ratchet with anti-vacuity injection proofs.
- `tests/git/test_protection_preserved.py` — the model ATDD ratchet (markers removed on convergence).
- `assert_called*` in `tests/sync/` (non-tracker), `tests/auth/` — **legitimate boundary verification**
  (subprocess, httpx, SaaS sink) paired with observable outcomes.
- ~85 arg-pinned delegation tests (debbie T5) — brittle-but-defensible style; the regression class
  *is* "wrong args forwarded." Leave unless a refactor trips them.
- `_baselines.yaml` **count**-keyed ratchets — semantically meaningful burn-down accounting; churn is
  inherent, not fixable friction.

## Mission-impact flags (for mission `single-planning-surface-authority-01KVPR00`)

Two findings touch surfaces this mission edits and could produce churn / false-red *during* the WP run:

1. **CT1 — the surface-resolver / write-side ratchets** (`test_single_mission_surface_resolver.py`,
   `test_no_write_side_rederivation.py`) are `file:line`-keyed and gate the very files this mission
   edits (`_read_path_resolver.py`, `resolution.py`, `mission_creation.py`, `surface_resolver.py`,
   `status_transition.py`). The mission's FR-004/FR-006/FR-007 edits **will** shift those lines →
   forced re-keys mid-mission; and the `status_transition.py:336` entry is the #1716 ladder FR-007
   *closes* (it should DRAIN, not re-key). **Strong candidate to pull to the FRONT of the mission.**
2. **CT4 — the status/merge emit-wiring tests** wrap the emit/safe_commit seams FR-007/FR-009
   rewrite; the source-as-text test (`test_command_module_has_no_direct_transactional_reference`)
   could false-red on a behavior-preserving emit refactor.

A paula + alphonso assessment determines whether CT1 (and/or CT4) is pulled into the mission's
front so it reduces churn/reverts rather than fighting the implementation.
