# Design Trace — coord-read-residuals-merge-lanes-and-identity-routing-01KW2M8V

**Purpose:** a running log of the design decisions and their rationale — the "what the fix
looks like and why" record. Seeded at spec→plan; **append during implement**; assessed at close.

> Format per entry: `[date] [phase] DECISION — rationale — evidence/constraint`

---

## Seeded during spec → plan (2026-06-26)

1. **[spec] Route by the REAL artifact-kind partition, not the issue labels.** The fix re-points
   each site to `resolve_planning_read_dir(kind=<real kind>)`. The issues mislabel 6 of 10 Lane A
   sites — `merge/resolve.py:98`, `cli/commands/merge.py:269`, `lanes/worktree_allocator.py:360`
   read `meta.json` (PRIMARY_METADATA) not LANE_STATE; `lanes/recovery.py:611` reads `lanes.json`
   (LANE_STATE) not `tasks/`. Evidence: debugger lens verified each against `is_primary_artifact_kind`.

2. **[spec] Per-leg split for mixed PRIMARY+STATUS sites; STATUS stays coord-aware (C-001).**
   `merge/executor.py` (`feature_dir`→`run.feature_dir`→`status_feature_dir` at `:503`/`:560`),
   `merge/done_bookkeeping.py:237` (WP-path leg only; status-transactional legs stay on the
   meta-bearing primary dir), `lanes/recovery.py:356` (lanes/tasks → PRIMARY; events leg coord-aware).
   Rationale: collapsing both legs onto PRIMARY would break status semantics. Constraint: NFR-001.

3. **[spec] Lane B builds a NET-NEW command-layer identity-read scan arm — not a pin drain.**
   The existing scanner matches only `resolver / "tasks"|"lanes.json"|"*.md"` dir-joins and is
   structurally blind to `resolve_mission_identity(dir)` / `get_mission_type(dir)` function-call
   reads. So #2186 has no inherited pin; the detector + remediation co-land here, validated by a
   committed synthetic-AST non-vacuity self-test + a pre-merge full-gate dry run (gate-can't-
   self-validate). Arm scoped to `cli/commands/` to avoid red-CI on out-of-scope strangers
   (~41 identity sites repo-wide; sync/acceptance/policy/orchestrator_api are follow-on).

4. **[spec] Divergent-husk integration fixture (the squad's CRITICAL fix).** `build_coord` as-is
   writes `meta.json` to main before the worktree add → byte-identical husk meta → identity reads
   pass regardless of routing; and it seeds no `lanes.json`/`tasks/` anywhere. FR-009 requires a
   **divergent** husk: sentinel coord `meta.json` (≠ PRIMARY) + PRIMARY-only `lanes.json`/`tasks/`
   seeded post-worktree-add, asserting the husk lacks them — so reverting a routed read to
   coord-aware observably fails. Evidence: reviewer lens, `topology_fixtures.py:199-218`.

5. **[spec] `next_cmd.py:631` is routing, not telemetry.** `get_mission_type` husk-miss returns the
   default `software-dev` (no raise) → `get_or_start_run` starts the wrong run type. Higher impact
   than the `:187`/`:253` silent lifecycle-record drops. Evidence: `mission.py:574-575`.

6. **[spec] Consume the resolver seam, never author it (C-002); guards precede fallback removal
   (C-EXCL-FALLBACK).** Every fix is a call-site swap; `_read_path_resolver` internals are untouched.
   `implement.py:1389` gets its own primary anchor so it survives the eventual removal of the
   `:1018` fallback — but this mission does NOT remove that fallback (separate follow-on).

7. **[plan/brownfield] Deferred the `primary_read_dir` shared seam — consume, don't dedup here.**
   Brownfield scan found the two-call PRIMARY idiom inlined at ~12 sites + 3 duplicate
   `_planning_read_dir` wrappers — a real dedup opportunity. Deferred to a separate follow-on
   (cousin of #2100): it tension-conflicts with C-002 (consume-not-author the resolver), straddles
   the implement-loop sibling's owned `workflow.py`/`implement.py` legs, and is broader than
   #2185/#2186. This mission consumes the existing `resolve_planning_read_dir` seam only.
   But: converge the one in-scope split-brain pair — thread `executor.py:887`'s PRIMARY dir through
   to `:976` instead of recomputing coord-aware. Guardrail: `candidate_feature_dir_for_mission` is
   the C-005 STATUS primitive — never removed/"converged away".

<!-- append during implement: per-site route deltas, the ROUTE/KEEP ownership table outcome,
     any kind re-classification found mid-implementation, floor recompute census. -->
