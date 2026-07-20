# Phase 1 Data Model: Runtime-State Corpus Cutover

This mission adds no new persistent entity. It changes **which existing store is authoritative** and
adds one bookkeeping marker. The entities below are the ones the cutover reads, writes, and reasons
about.

## Authority entities (existing — reused, not redefined)

### Reduced status snapshot (authority after cutover)
- **What**: the deterministic projection of `status.events.jsonl` (`reduce()` / `materialize_snapshot()`).
- **Runtime slots per WP**: `shell_pid`, `shell_pid_created_at`, `agent`, `assignee`, `tracker_refs`,
  `subtasks` (id → status), `review` (ReviewOverride).
- **Role change**: becomes the **sole** authority for these slots once the predicate is deleted (IC-03).
- **Access seam**: the `wp_snapshot_state` accessor (shipped #2817) — bypass readers reroute onto it.

### `InnerStateChanged` seed events + seed `planned→claimed` transition
- **What**: the events the backfill emits to reconstruct pre-eviction frontmatter/checkbox state.
- **Identity**: deterministic content-namespaced ULID (`mission_id|wp_id|field`) → idempotent re-runs.
- **Fold**: ordinary WP01 events; the reducer folds them into the snapshot with no special-casing.
- **Honesty bound (C-005)**: subtask-completion `at` is clamped (fictional); seed ULIDs are
  content-namespaced (not chronological). Valid only because no consumer reads subtask-completion time
  or relies on seed-ULID order.

### `LegacyWPRuntime` (old reader — verify ground truth)
- **What**: the pre-eviction frontmatter/checkbox per-WP view (`read_legacy_runtime`).
- **Role**: the value `verify_backfill` compares the snapshot against by **count + value** parity.
- **Lifecycle**: read-only; deleted from the code path once the fallbacks (IC-04) are gone.

## Cutover marker (the one stateful addition)

### `meta.json` `status_phase`
- **Type**: string/int; `>= 1` historically meant "snapshot authority active" (predicate `status_phase >= 1`).
- **Writer**: the cutover orchestration helper — **sole writer**, writes only **after** a passing verify
  (FR-003). No other production writer exists (confirmed by squad).
- **Readers**: `_phase1_snapshot_authority_active` (runtime-slot authority) — **deleted in IC-03**. BUT
  `_legacy_lane_mirror_enabled` (kept by C-004) — **still reads `status_phase`**. So after IC-03 the
  field remains a **live runtime gate for the lane mirror**, not an inert marker (corrected post-planning;
  see research D-02). Flipping `0 → 1` therefore also **activates the lane mirror** for that mission.
- **State transition**: `absent | null | "0"`  →(backfill+verify passes)→  `"1"`. No reverse transition
  in this mission. **IC-06 must NOT retire this field** (would disable the lane mirror corpus-wide).
- **Today's corpus state**: all 299 dogfood missions are `status_phase=0` → lane mirror OFF, runtime
  slots read from frontmatter. IC-01b flips this repo's corpus; IC-02 flips consumers' on upgrade.

## Deleted / inert model surfaces (end-state)

| Surface | Fate | Concern |
|---------|------|---------|
| `_phase1_snapshot_authority_active` (predicate) | **deleted** + facade alias/`__all__` dropped | IC-03 |
| `_legacy_lane_mirror_enabled` | **kept** (`lane` still frontmatter-authored) | C-004 (out of scope) |
| `workflow_cores.resolve_review_feedback_context` frontmatter fallback | **deleted** (one block w/ bypass reader) | IC-04 |
| `merge/done_bookkeeping._extract_done_evidence` frontmatter synthesis | **deleted** (after event-sourced replacement confirmed) | IC-04 |
| `tasks_move_task` `agent` ownership frontmatter read | **rerouted** to snapshot accessor | IC-04 |
| `_CATEGORY_C_DEFERRED_RUNTIME_STATE_BACKFILL_CUTOVER` (15 dead-symbol pins) | **removed** (library now has callers) | IC-01 |
| `_SANCTIONED_READER_MODULES` (#2093 tolerated set) | → `frozenset()` | IC-05 |
| inert `wp_metadata` fields + `WP_FIELD_ORDER` slots | **removed** (optional) | IC-06 |

## Invariants (acceptance-shaping)

- **INV-1 (fail-closed)**: `status_phase` is `"1"` for a mission **iff** that mission's backfill+verify
  passed. No mission is flipped on a mismatch. (SC-001, NFR-001)
- **INV-2 (single authority)**: after cutover, no code path reads WP runtime slots from frontmatter;
  every read resolves the snapshot. (FR-008, SC-003)
- **INV-3 (byte-stability)**: a runtime-state transition writes 0 bytes to `tasks/WP##.md`. (NFR-003, SC-004)
- **INV-4 (idempotency)**: re-running backfill (CLI or upgrade) seeds nothing and does not re-flip.
  (NFR-002)
- **INV-5 (no repo-root write)**: all event writes resolve via `canonicalize_feature_dir`; nothing lands
  at repo root. (C-003, #2815)
