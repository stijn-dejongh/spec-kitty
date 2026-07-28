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

*Pending — WP01 is still implementing in lane-a. Its section lands here on completion.*
