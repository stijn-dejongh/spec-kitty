# Expected reds — mission `read-side-seam-primary-primitive-closure-01KYKMMT`

**Authored per WP, append-only.** Each WP owns exactly one `## WPnn` section. Do **not** rewrite
another WP's section — WP01 and WP02 run in parallel lanes, and WP08 reconciles the union of all
sections (its T039 step 6).

> **Why this file lives on the planning branch, not in a lane.** `research/expected-reds.md` sits
> under `kitty-specs/`, and `move-task`'s pre-flight guard blocks `kitty-specs/` changes on a lane
> branch ("planning artifacts must live on `fix/read-side-seam-primary-primitive-closure`") — the
> same rule that makes `finalize-tasks` reject `owned_files` under `kitty-specs/`. The WP prompts
> asked implementers to write here, which is not possible from a lane; **the orchestrator lands
> each section on the planning branch** from the implementer's reported content or by re-deriving
> it from the gate. WP02's implementer correctly refused to `--force` past the guard.

## WP02 — read-side bypass census, terminal shape

**Gate**: `tests/architectural/test_no_read_side_bypass.py::test_no_read_side_bypass_outside_sanctioned_and_allow_listed`
**Status**: **RED by design** (US8 / FR-023). WP02 grew the censused callees 2 → 4 and landed the
end-state sanction set, so the gate now flags every not-yet-routed consumer site. This red is the
mission's acceptance signal; **WP08 T039 greens it.**

**Enumerated finding set — 32 findings** (WP04 4 · WP05 10 · WP06 10 · WP07 8). Re-derived from the gate
itself, not copied. Per-primitive: 31 `primary_feature_dir_for_mission` + 1
`resolve_feature_dir_for_mission`.

**The ratchet each routing WP is held to**: after your WP, this set equals the set below **minus
exactly the sites you routed** — **zero additions**. The node stays red until WP08, so this
per-site diff is the only real signal available to WP04–WP07. A new finding is a regression even
though the node's red/green state did not change.

| Site (`rel_path:line`) | Primitive | Greened by |
|---|---|---|
| `src/runtime/next/runtime_bridge.py:1244` | `primary_feature_dir_for_mission` | WP07 |
| `src/runtime/next/runtime_bridge.py:260` | `primary_feature_dir_for_mission` | WP07 |
| `src/runtime/next/runtime_bridge_identity.py:118` | `primary_feature_dir_for_mission` | WP07 |
| `src/specify_cli/acceptance/__init__.py:860` | `primary_feature_dir_for_mission` | WP05 |
| `src/specify_cli/agent_tasks_ports.py:266` | `primary_feature_dir_for_mission` | WP04 |
| `src/specify_cli/cli/commands/accept.py:270` | `primary_feature_dir_for_mission` | WP06 |
| `src/specify_cli/cli/commands/agent/mission_feature_resolution.py:145` | `primary_feature_dir_for_mission` | WP06 |
| `src/specify_cli/cli/commands/agent/mission_finalize.py:1645` | `primary_feature_dir_for_mission` | WP06 |
| `src/specify_cli/cli/commands/agent/tasks_move_task.py:301` | `primary_feature_dir_for_mission` | WP06 |
| `src/specify_cli/cli/commands/agent/tasks_move_task.py:699` | `primary_feature_dir_for_mission` | WP06 |
| `src/specify_cli/cli/commands/agent/workflow.py:889` | `primary_feature_dir_for_mission` | WP05 |
| `src/specify_cli/cli/commands/agent/workflow.py:897` | `primary_feature_dir_for_mission` | WP05 |
| `src/specify_cli/cli/commands/agent/workflow_executor.py:1986` | `primary_feature_dir_for_mission` | WP05 |
| `src/specify_cli/cli/commands/agent/workflow_executor.py:520` | `primary_feature_dir_for_mission` | WP05 |
| `src/specify_cli/cli/commands/agent/workflow_executor.py:680` | `primary_feature_dir_for_mission` | WP05 |
| `src/specify_cli/cli/commands/implement.py:1449` | `primary_feature_dir_for_mission` | WP05 |
| `src/specify_cli/cli/commands/implement.py:274` | `primary_feature_dir_for_mission` | WP05 |
| `src/specify_cli/cli/commands/implement.py:430` | `primary_feature_dir_for_mission` | WP05 |
| `src/specify_cli/cli/commands/implement.py:603` | `primary_feature_dir_for_mission` | WP05 |
| `src/specify_cli/cli/commands/mission_type.py:1069` | `primary_feature_dir_for_mission` | WP04 |
| `src/specify_cli/cli/commands/mission_type.py:610` | `primary_feature_dir_for_mission` | WP04 |
| `src/specify_cli/cli/commands/next_cmd.py:190` | `primary_feature_dir_for_mission` | WP06 |
| `src/specify_cli/cli/commands/next_cmd.py:269` | `primary_feature_dir_for_mission` | WP06 |
| `src/specify_cli/cli/commands/next_cmd.py:671` | `primary_feature_dir_for_mission` | WP06 |
| `src/specify_cli/coordination/commit_router.py:657` | `primary_feature_dir_for_mission` | WP07 |
| `src/specify_cli/decisions/emit.py:71` | `resolve_feature_dir_for_mission` | WP04 |
| `src/specify_cli/merge/executor.py:1437` | `primary_feature_dir_for_mission` | WP06 |
| `src/specify_cli/retrospective/writer.py:85` | `primary_feature_dir_for_mission` | WP06 |
| `src/specify_cli/status/aggregate.py:499` | `primary_feature_dir_for_mission` | WP07 |
| `src/specify_cli/status/aggregate.py:522` | `primary_feature_dir_for_mission` | WP07 |
| `src/specify_cli/status/aggregate.py:543` | `primary_feature_dir_for_mission` | WP07 |
| `src/specify_cli/status/aggregate.py:791` | `primary_feature_dir_for_mission` | WP07 |

**Cross-check on the corrected arithmetic (A3)**: 34 in-scope sites − 3 in-scope FR-005 foundation
sites (`core/paths.py` ×2, `core/git_ops.py`), now carried by WP02's foundation-sanction seed =
**31 routable**, which is exactly the primary-primitive finding count above. The fourth FR-005
foundation site (`coordination/surface_resolver.py:739`) is the separately-counted sanctioned
single-authority site and was never inside the 34.

### Foreign honest-red P0s — NOT this mission's business (C-010)

| Test | Issue | Why it is red | Rule |
|---|---|---|---|
| `tests/sync/test_sync_consent_default_deny.py` (5 failing) | **#3031** | Red **by design** — honest-red P0 pin per ADR `2026-07-17-1`. Marked `fast`, so it appears in every lane. Surface is `sync/routing.py` / `is_sync_enabled_for_checkout` — the **sync fan-out** sense of "routing", zero overlap with placement. | **Do not touch. Do not green-wash.** Its own docstring flags further #3031 work as not yet pinned, so more may land mid-mission. |

Classification is **by surface, not by timing**: a red is this mission's business only if it touches
a placement/read-path surface the mission owns, or is a demonstrable regression from this mission's
diff.

## WP01 — architectural gate expectations

**Scope**: T001–T007 (`test_resolution_authority_gates.py`,
`resolution_gate_allowlist.yaml`, `test_gate_read_literal_ban.py`,
`test_trio_seam_only.py`, `test_coord_read_residuals_closeout.py`,
`_gate_coverage_baseline.json`, `_golden_count_baseline.json`). **Zero
changes under `src/`.**

**Reconciled against a live run of all six C-008 gates** (`PWHEADLESS=1
SPEC_KITTY_SYNC_MINIMAL_IMPORT=1 uv run pytest test_no_read_side_bypass.py
test_resolution_authority_gates.py test_gate_read_literal_ban.py
test_coord_read_residuals_closeout.py test_trio_seam_only.py
test_no_write_side_rederivation.py -q`, lane-a): **168 passed / 3 failed / 0
collection errors** — the 3 failures are exactly the 3 nodes below, no
unpredicted red.

| # | Node id | Finding (rel_path :: qualname) | FR | Greened by | Why expected |
|---|---|---|---|---|---|
| 1 | `test_coord_read_residuals_closeout.py::test_fr007_arm_live_identity_scan_is_clean` | `src/specify_cli/cli/commands/agent/mission_setup_plan.py::_run_documentation_wiring` (flag: `get_mission_type(feature_dir)`) | FR-014 | WP04 | T005 retired the `#2214` allow-list pin (`_IDENTITY_CALLSHAPE_KNOWN_RESIDUALS`) that tolerated this one-hop residual, together with the test asserting the pin exists. The live arm still (correctly) flags the site — it is not yet routed. |
| 2 | `test_trio_seam_only.py::test_trio_imports_route_only_through_seam_wrappers` | 7 sites still import `_canonicalize_primary_read_handle` / `primary_feature_dir_for_mission` from `_read_path_resolver`: `workflow.py::<module>`, `workflow_executor.py::<module>`, `acceptance/__init__.py::<module>` (top-level imports), `implement.py::find_wp_file`, `implement.py::_load_primary_anchored_mission_meta`, `implement.py::_planning_artifact_source_dir`, `implement.py::_build_implement_json_payload` | FR-004/FR-005 | WP05 | T006 shrank `_SEAM_ALLOWED_READ_PATH_RESOLVER_NAMES` to `{resolve_handle_to_read_path}` (a tightening, Ledger M5). This is a **pre-existing** gate (zero code change to itself) that now structurally enforces the shrink. |
| 3 | `test_trio_seam_only.py::test_allowed_read_path_resolver_names_are_currently_used` | same reacquisition set as #2 | FR-004/FR-012 | WP05 | T006's replacement for the self-nullifying exemption (Ledger M6 — the retired `blessed - used - {"resolve_handle_to_read_path"}` shape was the empty set by construction once `blessed` shrank to one name, vacuously green regardless of what the trio imported). The new positive assertion reds on the identical still-imported leaf primitives until WP05 routes all four trio rewrite targets. |

**T001/T002 gate-defect fixes (not widenings)**: `_PRIMARY_FOLD_CALLSHAPE_FUNCS`'s
two consumption sites (`callshape_violations` here; `test_no_status_leg_rerouted_to_primary`
above) now UNION a kind-discriminated helper (`_names_bound_from_primary_read_dir`, via
`mission_runtime.is_primary_artifact_kind` — never a hardcoded kind list) instead of widening
the frozenset by callee name (Ledger M7 — a callee-name widening would have sanctioned
`STATUS_STATE` reads through the same seam call, producing a false positive on
`test_no_status_leg_rerouted_to_primary`; verified that node does **not** acquire a new failure
from this change). `test_write_arm_resolvers_anchor_meta_on_primary` now asserts the positive
`reads_via_primary` signal it used to discard (Ledger M8); making it positive against the REAL
write-arm surfaces (`core/paths.py::get_feature_target_branch`,
`core/git_ops.py::resolve_target_branch`, `mission_finalize.py::finalize_tasks`) surfaced a
genuine pre-existing detection gap — all three are thin adapters over
`read_target_branch_from_meta` and never match the literal `anchor(...) / "meta.json"` BinOp
shape.

**Review-cycle-1 (B1) found that gap only HALF-closed.** The initial fix (`_anchor_invoked_in`)
recognised the thin-adapter shape only when anchored on the exact **deleted** wrapper name
`primary_feature_dir_for_mission`, while its docstring claimed the seam branch was "the
surviving spelling after WP08". That branch requires a literal `/ "meta.json"` join no real
surface has, so it could never match its own subjects: the moment WP08 deletes the wrapper the
positive assertion would have gone **unrecorded-red** — in WP06 (`mission_finalize.py:1645`
sits inside `finalize_tasks`, a WP06 routing target) and again in WP08 (`core/paths.py` ×2 and
`core/git_ops.py` forced off the name) — emitting a message instructing the implementer to
"POSITIVELY anchor on `primary_feature_dir_for_mission`". That is a gate **obliging a deleted
primitive to keep being used**: the very inversion T003 retires on the read arm, rebuilt on the
write arm.

Cycle-1 closed it by adding `_primary_partition_seam_invoked_in` — the seam-idiom counterpart
of `_anchor_invoked_in`, **kind**-discriminated (via `_is_primary_partition_read_dir_call`)
rather than **name**-discriminated, recognising a PRIMARY-partition `<seam>.read_dir(kind)`
call anywhere in the function, which is the actual post-WP08 shape. Verified by AST mutation
against the live tree on all three surfaces:

| Mutant | Required | Result (all 3 surfaces) |
|---|---|---|
| baseline | green | `(False, True)` ✓ |
| → candidate resolver | bites | `(False, False)` ✓ |
| → unrelated third resolver (M8 case) | bites | `(False, False)` ✓ |
| **→ post-migration seam idiom** | **GREEN** | **`(False, True)`** ✓ *(was `(False, False)` — the B1 defect)* |
| → `read_dir(STATUS_STATE)`, same shape | bites | `(False, False)` ✓ *(kind discipline holds)* |

Locked in by two new self-tests
(`test_write_arm_recognises_primary_seam_thin_adapter_post_migration_shape`,
`test_write_arm_primary_seam_thin_adapter_kind_discipline_holds`). Both the pre-migration and
post-migration thin-adapter shapes are now covered — **fixed, not carried as a red.**

**T003/T004 floor retirement (FR-007, DIRECTIVE_043 required)**: retired
`CANONICALIZER_FLOOR` (was 44) and `ROUTED_CANONICALIZER_FLOOR` /
`_MARGIN` (were 40 / 4) together with `test_canonicalizer_gate_floor` /
`test_routed_count_floor`. Live re-derived census at retirement
(quickstart.md §1 recipe, re-run fresh): **46 total canonicalizer call sites,
43 routed** (both figures had already drifted from the stale 44/40 recorded
in-tree — unrelated `src/` growth between missions). This is a **retirement**,
not a re-pin: after Step 2 the floors' only remaining subject population is
resolver-internal + named-sanctioned code, where a raw handle is correct by
contract, so a floor obliging continued use would invert its own purpose.
**DIRECTIVE_043 adjudication**: non-vacuity is preserved by **transfer**, not
abandoned — `tactic:architectural-gate-non-vacuity`'s routed-count-floor
element moves to WP02's read-side bypass census above (its own concrete
floor, per-primitive non-vacuity, alias resistance, shrink-only allow-list).
`test_coord_read_residuals_closeout.py`'s floor **import** + both equality
pins + the two bound checks (the whole `test_routed_canonicalizer_floor_
matches_recorded_census` test — zero coverage beyond the retired floor's own
derivation) retired in the **same commit** — otherwise `ImportError` at
collection, ~20 tests (DIRECTIVE_034). Also corrected the module's
off-by-one identity read-site census in the same pass (FR-016): **24** live,
not the recorded 22 (re-derived via the module's own
`_count_read_call_sites`; unrelated drift since that figure was written).

**T007 baselines**: `_gate_coverage_baseline.json` (orphan baseline,
`--update-baseline`) refrozen — `total_tests` 32346 → 33948, `duplicate_
test_count` 924 → 1046 (repo-wide drift unrelated to this WP's ~10-test net
delta; `orphan_test_count`/`orphan_files` unchanged at 0/`[]`).
`_golden_count_baseline.json` (selection baseline) needed **no change** —
none of this WP's additions introduce a new `len(x) == n` golden-count shape
(the retired floor tests used `>=`/`>`/`<=`, never `==`).

**Contradictions with the WP prompt** (reported, not silently resolved):
(1) T003's "corresponding block in `resolution_gate_allowlist.yaml`" does not
exist — that YAML's `canonicalizer:` allow-list (3 permanent entries) is a
separate, still-live def-use correctness gate, untouched; (2) T005's
"off-by-one" was actually **+2** (22 → 24), not literally one — same drift
class as the canonicalizer census above; (3) `tests/architectural/
test_inline_meta_read_gate.py` (not owned by WP01) carries a stale docstring
precedent-citation to `ROUTED_CANONICALIZER_FLOOR` — a comment-only mention,
left untouched (out of WP01's `owned_files` and task list), flagged here for
a future cleanup pass.
