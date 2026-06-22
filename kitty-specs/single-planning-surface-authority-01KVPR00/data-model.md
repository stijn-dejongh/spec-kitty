# Data Model: Single planning-surface authority + worktree repair

This is a refactor/convergence mission — no new persistent schema. The "entities" are the
existing surface-resolution concepts whose handling is converged.

## Surface authority
- **`resolve_placement_only(repo_root, mission_slug)`** (`mission_runtime/resolution.py:761`)
  — the single write-destination decision: returns the placement (COORDINATION vs FLATTENED
  → ref/branch) byte-identical to the full resolver. **Invariant (FR-001)**: every planning
  write resolves here; no command derives a write target from `HEAD`.

## Planning surface (where an artifact lives)
- **PRIMARY checkout** — `kitty-specs/<slug>-<mid8>/` — authoritative for planning INPUT
  artifacts (`spec.md`, `plan.md`, `tasks/`, `meta.json`) and for flattened/no-coord missions.
- **COORDINATION worktree** — `.worktrees/<slug>-<mid8>-coord/kitty-specs/<slug>-<mid8>/` —
  the commit surface for coord-topology missions (staged at commit-time).
- **Invariant (FR-003)**: `map-requirements` writes and `finalize-tasks --validate-only`
  reads WP `requirement_refs` on the SAME surface.

## Coordination worktree state (the `CoordState` enum + the declared-coord signal)
| State | On disk | Primary meta declares `coordination_branch`? | Read resolution |
|-------|---------|----------------------------------------------|-----------------|
| MATERIALIZED | coord mission dir present | yes | COORD |
| EMPTY | coord root present, mission dir absent | yes | PRIMARY (loud, Option B) |
| UNMATERIALIZED | coord root absent | yes | PRIMARY (create-window, #1718) |
| DELETED | coord branch gone from git | yes | hard-fail `CoordinationBranchDeleted` (#1848) |
| **flattened-stale-coord** (NEW gate) | coord dir present (orphan) | **no** | **PRIMARY** (FR-004) — the bug: read-path leg currently returns COORD |
- **Invariant (FR-004)**: `MATERIALIZED` is necessary-but-not-sufficient; coord-preference
  requires `declares_coordination == True`.

## Repair verb (recreate-or-prune)
- **`agent worktree repair --mission <slug>`** (NEW, FR-007):
  - *missing* coord worktree (declared, UNMATERIALIZED) → **recreate** via
    `CoordinationWorkspace.resolve()`.
  - *orphaned* coord worktree (flattened, dir on disk) → **prune**.
  - no coordination topology → benign no-op with a clear message.

## Status-event write surface
- **`emit_status_transition(feature_dir=…)`** (`status/emit.py:399`) — **Invariant (FR-006)**:
  `feature_dir` is resolved by the single write authority at every call site, not passed
  ad-hoc, so dep-gate/kanban/review-claim reads and `move-task` writes converge.
