# Quickstart: validating the convergence (live-evidence recipes)

These are the repro-backed acceptance recipes the implement loop MUST run (NFR-001 — no
close-on-static; #2062 carries C-002). Each is a throwaway tmp git repo.

## R1 — Flattened-stale-coord resolves PRIMARY on all legs × all handles (FR-004/FR-005, #2062)

```python
# Build: primary meta with NO coordination_branch + a stale -coord worktree on disk.
#   kitty-specs/<slug>-<mid8>/meta.json            -> {"mission_id": ...}  (NO coordination_branch)
#   kitty-specs/<slug>-<mid8>/status.events.jsonl  -> canonical = approved
#   .worktrees/<slug>-<mid8>-coord/kitty-specs/<slug>-<mid8>/status.events.jsonl -> stale = planned
from specify_cli.coordination.surface_resolver import resolve_status_surface_with_anchor
from specify_cli.missions._read_path_resolver import resolve_handle_to_read_path
from specify_cli.status.aggregate import MissionStatus
# For handle in {<slug>-<mid8>, bare-mid8, full-ULID, bare-human-slug}:
#   surface  leg -> PRIMARY
#   read_path leg (require_exists=True) -> PRIMARY   # currently STALE-COORD: the bug
#   aggregate leg -> PRIMARY
```
**Pass**: all three legs return the PRIMARY dir for every handle form. **Today**: the
read-path leg returns the stale `-coord` dir for composed/bare-mid8/ULID — that is the fix
target. This must be a new strict row in `tests/missions/test_surface_resolution_equivalence.py`.

## R2 — spec.md visible to /tasks + finalize from one surface (FR-001/FR-002, #2063)

```bash
# Coord-topology mission. Commit spec.md via the mission-aware path.
spec-kitty spec-commit --mission <slug> --message "..." <feature_dir>/spec.md
# finalize-tasks and the /tasks read path must resolve spec.md from the SAME surface:
spec-kitty agent mission finalize-tasks --validate-only --mission <slug> --json   # no "spec.md not found"
```
**Pass**: no "spec.md not found" / "Tasks directory not found" divergence between the
commands.

## R3 — map-requirements full coverage == finalize zero-unmapped (FR-003/FR-013, #2064)

```bash
spec-kitty agent tasks map-requirements --mission <slug> --wp WP01 --refs FR-001   # reports 1/1 mapped
spec-kitty agent mission finalize-tasks --validate-only --mission <slug> --json    # unmapped_functional_requirements == []
```
**Pass**: after map-requirements reports full coverage, finalize `--validate-only` reports
ZERO `unmapped_functional_requirements`.

## R4 — worktree repair recreates + prunes (FR-007, #1890)

```bash
spec-kitty agent worktree repair --mission <slug>   # registered command (not "No such command")
# missing coord worktree -> recreated;  orphaned coord worktree -> pruned;  no coord topology -> benign no-op
```
**Pass**: the command is registered and performs the right action per state; every recovery
hint elsewhere (doctor / surface_resolver / ADR) names a registered command.

## R5 — command-reference guard fails on a planted phantom (FR-008/NFR-003)

```bash
# Plant a bogus `spec-kitty agent nonesuch` in a Python literal; the guard MUST go RED.
PWHEADLESS=1 pytest tests/architectural/<new-command-reference-guard> -q
```
**Pass**: green on the clean tree; RED when a phantom Python-literal invocation is planted
(self-test). Run the full architectural sweep as the gate-unmask dry-run before relying on it.
