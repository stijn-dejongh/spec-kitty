# Phase 1 — Data Model

Mission `mission-resolver-port-01KX1C05` · #2173 Phase-2. No persistent data model changes — this is a
DI seam over existing reads. The "entities" here are the port interface and the value objects it moves.

## Value objects (existing, reused unchanged)

### `ResolvedMission` (`context/mission_resolver.py:51`, frozen)
| Field | Type | Meaning |
|-------|------|---------|
| `mission_id` | `str` | 26-char ULID from `meta.json` |
| `mission_slug` | `str` | `kitty-specs/` directory name |
| `feature_dir` | `Path` | absolute mission directory |
| `mid8` | `str` | first 8 chars of `mission_id` |

### `MissionExecutionContext` (`mission_runtime/context.py:11`, frozen)
The pure composite the builder mints. **Invariant: never carries an adapter** (C-006). Unchanged by this
mission except that its builder becomes injectable at the shell.

## New port interface

### `MissionResolver` (Protocol) — handle→mission resolution only
```python
class MissionResolver(Protocol):
    def resolve(self, handle: str) -> ResolvedMission: ...
    def all_missions(self) -> list[ResolvedMission]: ...
```
- `resolve(handle)` — the identity resolution currently in `resolve_mission`; **fail-closed-loud**:
  ambiguity → `AmbiguousHandleError`/`MissionSelectorAmbiguous`, cold-miss → `MissionNotFoundError`
  naming `spec-kitty migrate backfill-identity`. **No** `is None`/`or slug` fallback (D-05).
- `all_missions()` — the enumeration currently in `_build_index`, for the resolve-by-identity consumers
  (`doctrine_synthesizer/apply.py`, `vcs/detection.py`) that scan for a matching `mission_id`.
- Bound to a `repo_root` at construction (adapter concern), so callers pass only the handle.

### `FsMissionResolver` — real adapter
- Wraps the existing `_build_index(repo_root)` walk + the `resolve_mission` priority ladder.
- **Request-scoped**; instance-lifetime memoization only, **no** module/process cache (C-005).
- Silently skips `mission_id`-less / non-dict-meta missions exactly as `_build_index` does today (so the
  anti-fold `identity_audit.py` consumer keeps its own walk — C-001).

### `FakeMissionResolver` — stub adapter
- Constructed from an in-memory `list[ResolvedMission]` (canonical-shaped fixtures — D-05).
- Zero filesystem access → enables the FS-free builder test (NFR-001).
- Same fail-closed contract: unknown handle → `MissionNotFoundError`; ambiguous → `AmbiguousHandleError`.

## Injection seam

```python
# mission_runtime/resolution.py  (the imperative shell)
def _assemble_core_fragments(repo_root, *, resolver: MissionResolver | None = None, ...):
    resolver = resolver or FsMissionResolver(repo_root)
    # ... identity/dir reads (_resolve_mission_id :913, _resolve_mission_slug :303) consume `resolver`
# build_execution_context(...) stays FS-free and takes NO resolver.
```

## Out-of-model (anti-fold — NOT routed through the port)
- `status/identity_audit.py` — needs to *see* `mission_id`-less missions the resolver skips (C-001).
- `merge/ordering.py` — `max(mission_number)` aggregate over a caller-supplied non-primary scan root under the merge lock (C-002).
- `core/paths.py:816/835` — best-effort swallow-and-degrade error listing (C-003).
- migration-time walks (C-004).
