# Contract: write-location accessor

**Operation:** `PlacementSeam.write_dir(self, kind: MissionArtifactKind) -> WriteLocation`
**Home:** `src/mission_runtime/resolution.py`, class `PlacementSeam` (L2261), beside `write_target` (L2304) and `read_dir` (L2318). `WriteLocation` and `Establishment` live in `src/mission_runtime/write_location.py`, which is new.
**Delegate:** for a COORD kind of a coordination-routed Mission, the work is done by `specify_cli.coordination.coord_seed.establish_coord_write_location(repo_root, mission_slug, kind, *, owned) -> WriteLocation` (new). The seam reaches it through a lazy import over the existing `coordination` ledger edge.
**Requirements:** FR-003, FR-003a, FR-004, FR-004a, FR-004b; C-001, C-002, C-008.

## Signature

```python
@dataclass(frozen=True)
class WriteLocation:
    path: Path
    surface: Literal["primary", "coordination"]
    coord_state_before: CoordState | None
    establishment: Establishment          # NONE | MATERIALIZED | SEEDED | RESTORED_FROM_BRANCH
    seed: SeedReport | None = None

class PlacementSeam:
    def write_dir(self, kind: MissionArtifactKind) -> WriteLocation: ...
```

## Preconditions

- The `PlacementSeam` was built with `placement_seam(repo_root, mission_slug, owned=...)` (`resolution.py:2835`). The partition invariant was asserted at construction.
- The Mission resolves: `meta.json` is readable on the PRIMARY partition.

## Postconditions

| Case | Result |
|------|--------|
| `kind` is a PRIMARY-partition kind | `surface="primary"`, `path` = the declared PRIMARY dir (identical to `read_dir(kind)` today), `establishment=NONE`. No side effects. |
| COORD kind, topology `lanes` or `single_branch` | the PRIMARY dir, as today (C-008). No side effects. |
| COORD kind, coordination-routed, state `MATERIALIZED` | the coordination Mission dir. No side effects. |
| COORD kind, coordination-routed, state `UNMATERIALIZED` with a local branch | the worktree is materialized via `CoordinationWorkspace.resolve`; then the `MATERIALIZED` or `EMPTY` row applies |
| COORD kind, coordination-routed, state `EMPTY`, branch lacks the Mission dir | seeded (`contracts/seed.md`); `establishment=SEEDED` |
| COORD kind, coordination-routed, state `EMPTY`, branch carries the Mission dir | loud `WARNING`, the dir is restored from the branch tip, then any root-only records are seeded; `establishment=RESTORED_FROM_BRANCH` |

The following hold in every case:
- `write_dir(kind).surface` matches the partition of `write_target(kind).ref`: the coordination worktree's branch is `write_target(kind).ref`. A property test over every `MissionArtifactKind` pins this.
- The returned `path` exists on return for COORD kinds of a coordination-routed Mission.
- A seed is logged at `WARNING` with its `SeedReport`, so callers that do not render it still surface it.

## Errors (raised; nothing is written)

| Code | When | Exception (existing unless marked) |
|------|------|------------------------------------|
| `COORDINATION_BRANCH_DELETED` | `meta.json` declares a coordination branch that does not exist | `CoordinationBranchDeleted` |
| `COORDINATION_WORKTREE_UNMATERIALIZED` | branch is remote-only (#4970 parity), or materialization failed after one re-probe | `CoordinationWorktreeUnmaterialized` via `_raise_unmaterialized` (`surface_resolver.py:877`) |
| `COORD_SEED_FORK_REFUSED` (new) | seed found a true fork (`contracts/seed.md`) | `CoordSeedForkRefused(ActionContextError)` (new) |
| `STATUS_LOCK_HELD` (new code on an existing exception) | status lock timeout during the seed | `FeatureStatusLockTimeoutError` (`status/locking.py:59`); the `error_code` attribute is added |
| `OWNED_COORDINATION_WORKSPACE_UNAVAILABLE` | owned checkout whose coordination workspace cannot be established | existing `OwnedRefusalCode` |

Every error message names the Mission, the coordination branch, and a recovery command.

## Relationship to existing seams

- **`resolve_placement_only` / `write_target`:** unchanged. They give the commit ref and are materialization-blind. `write_dir` gives the directory.
- **`read_dir`:** unchanged. It keeps the `EMPTY` → PRIMARY read fallback (C-002). It is never a write location for a COORD kind; the FR-014 gate enforces that.
- **`materialize_coord_surface_for_write`** (`surface_resolver.py:903`): becomes step 1 of `establish_coord_write_location`. Its two writer callers (`decisions/service.py:501,696`) switch to `write_dir`. The `doctor coordination` caller (`_coordination_doctor.py:1424`) keeps calling it, because it repairs a worktree and is not a writer.
- **`resolve_status_surface_with_anchor(for_write=True)`:** unchanged, and documented as "commit-ref oriented, not a write location". The read-side `EMPTY` warning goes loud for post-fix Missions in both coordination topologies.
- **`status_transition._coord_feature_dir`** (L400) and `transaction.py:490`'s inline composition: both are replaced by `write_dir(STATUS_STATE).path`. No second composer remains.

## Compatibility

- Additive API. No existing signature changes.
- Writers migrate call by call (IC-04). The FR-014 gate ratchets the migration.
- `lanes` and `single_branch` Missions: byte-identical behaviour (C-008).
