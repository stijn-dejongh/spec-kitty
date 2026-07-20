# Handover — Mission #2816 · Runtime-State Corpus Cutover

*Paste-ready pickup prompt for a co-maintainer. All paths are repo-relative. Spec/plan are complete
through `/spec-kitty.plan`; **implementation has not started**.*

---

You are picking up a governed spec-kitty mission that is fully **SPECCED + PLANNED** and ready for
`/spec-kitty.tasks`. Do not re-plan from scratch — the artifacts below are the source of truth; refine
only where you find a genuine gap.

## Where it lives
- **Mission**: `runtime-state-corpus-cutover-01KXZ0AX` (mid8 `01KXZ0AX`), type `software-dev`,
  topology **`coord`**.
- **Branch**: `feat/runtime-state-corpus-cutover` (+ coordination branch
  `kitty/mission-runtime-state-corpus-cutover-01KXZ0AX`). Both pushed to the **fork** remote
  (`github.com/stijn-dejongh/spec-kitty`), branched off upstream `main` (which contains the merged #2817).
- **Artifacts** (`kitty-specs/runtime-state-corpus-cutover-01KXZ0AX/`): `spec.md` (16 FRs, 11 constraints,
  US1–US6), `plan.md` (11 implementation concerns + the IC-08a ADR), `research.md` (D-01…D-14 decisions),
  `data-model.md`, `contracts/cutover-cli.md`, `contracts/resolved-binding.md`, `checklists/requirements.md`.

## Mission intent
Complete the deferred #2684 cutover: make the reduced **event-log snapshot the unconditional authority**
for WP runtime state and **delete the phase-1 dual-write toggle**, per the strict contract
`backfill → verify(FAIL-CLOSED) → flip reader+writer → delete fallbacks → reduce`. Then (operator scope
generalization) make the WP/dashboard reader **reconstruct a WP's resolved final-state from the event
log**, and event-source the WP's runtime **identity** — the *actual* `role`/`agent_profile`/`model` that
take a WP (distinct from the frontmatter *authored* recommendation), because the actual identity shifts
across the lifecycle (implementer→reviewer, model swaps) so a static value is wrong mid-cycle. This
implements #2093's resolved-binding "record + reconstruct" half and the WP-metadata slice of #2400; the
full fail-closed enforcement (#2399) stays out of scope.

## Status
- Driven through **spec → plan** with four review squads (pre-planning brownfield ×2, post-planning
  architect, dashboard/events boundary, a consistency-QA pass, and a grounding/campsite/adversarial pass).
  All findings folded.
- Tracker refreshed: comments posted on #2093, #2400, #2399.
- **Next step: `/spec-kitty.tasks`** on this mission, then implement-review with per-WP model discipline
  (Opus for backfill/verify/flip/linkage WPs and all reviews; a mid tier for mechanical test re-points).
- Not started: any source edit. The WP03 backfill **library** exists; nothing is wired yet.

## The 11 concerns (contract-order spine; see plan.md for the full map)
`IC-01` wire cutover helper+CLI → **`IC-01b` RUN the backfill on this repo's corpus + commit seeds** →
`IC-03` flip flag unconditional + delete predicate → `IC-04` build snapshot done-evidence then delete
fallbacks + route bypass readers → `IC-05` harden #2093 invariant + reconcile ~33 test files → `IC-06`
(optional) inert-field reduction. Then the resolved-binding slice: `IC-07` canonical `reconstruct_wp_view`
(collapse 3 hand-rolled gates → 1) → `IC-08` resolved-binding vocabulary + **dispatch→claim linkage**
(+`IC-08a` field-authority ADR) → `IC-09` SaaS fan-out → `IC-10` subtasks event-sourced + markdown
checkboxes removed. `IC-02` (upgrade migration) rides the shared cutover helper.

## ⚠️ EXTREME campsite-cleaning directive (binding for this mission)
Every surface you touch must be left **materially cleaner** — this is not optional polish:
- **Two functions breach the complexity ceiling (15) as a direct result of the functional edits** — you
  MUST tidy-first extract them in the same WP, not leave them at 16+: `status/reducer.py::_apply_annotation_delta`
  (data-drive the replace-slot table before IC-08 adds slots) and `dashboard/scanner.py::_process_wp_file`
  (extract a runtime-view helper on the IC-04/07 reroute). `tasks_move_task.py::_mt_emit_runtime_state` is
  already at 15 — extract the ownership read, don't inline.
- Hoist repeated literals to constants (Sonar S1192): `status_phase`, command names, messages.
- Delete orphan flag-wrapper functions + dead docstring refs at each of the 12 flag sites (don't leave
  wrappers). Narrow the broad `except Exception:` in `workflow_cores.py`. Delete the dead
  `frontmatter-migration:` synth branch in `merge/done_bookkeeping.py`.
- Consolidate logical duplication: 3 (→4, incl. `tasks_status_cmd.py`) hand-rolled snapshot gates → one
  `reconstruct_wp_view`; a shared review-slot reader across `merge/done_bookkeeping.py` +
  `cli/commands/agent/workflow_cores.py`.
- **God-modules are surgical-ONLY** (degod is a tracked follow-up, not this mission):
  `cli/commands/implement.py`, `cli/commands/agent/workflow_executor.py`, `status/emit.py`,
  `cli/commands/agent/tasks_move_task.py`, `migration/mission_state.py`. Do NOT inflate the tracked
  `# NOSONAR` on `emit.py::emit_status_transition` — thread new actor logic via a helper.

## Standing orders (charter + project memory — all binding)
- **Git**: no direct pushes to origin/main; PR-bound. `spec-kitty merge` is local-main only; the
  **operator merges to origin** and opens the PR. Work on the mission branch.
- **Contract order (C-001)** is the hard spine: never delete a fallback before backfill is wired+verified.
- **Fail-closed (NFR-001)**: never flip a mission whose verify didn't pass; zero tolerated parity mismatches.
- **Tests**: run via `uv run --extra test python -m pytest -p no:cacheprovider <FILE>` — bare `python`
  resolves a sibling checkout and gives false greens. **Never run the whole `tests/architectural/`
  directory** (it hangs) — per-file with a timeout only.
- **No suppression** to pass gates: no new blanket `# noqa` / `# type: ignore` / per-file ignores; keep
  complexity ≤15; `ruff` + `mypy` clean. Every new branch/helper gets a focused test in the same WP (ATDD).
- **Canonical sources**: use the doctrine templates/CLI/library; don't improvise or copy older missions.
  Edit SOURCE doctrine templates (`src/doctrine/missions/mission-steps/…`), never the generated agent copies.
- **Pre-push**: run the terminology guard + docs-freshness when touching `src/doctrine/` or prose.
- **Pre-existing reds are NOT yours**: the `arch-adversarial (arch_shard_1)` `SYNC_DISABLE_ENV_VARS` red is
  a CI-runner phantom on `main`; the ADR-2026-07-17-1 known-P0s (#2736/#2772/#1834) stay red. Confirm on
  the merge-base before attributing any red to your diff.

## Gotchas that will bite (heed these before coding)
1. **IC-01b is a BLOCKER, not a tool**: all ~299 dogfood missions are `status_phase=0` and write runtime
   state to frontmatter only (no events). The moment IC-03 makes readers unconditional on local main, every
   mission reads an empty snapshot → red. IC-01b (run the backfill on THIS repo + commit the seed events)
   MUST land in the **same merge unit** as IC-03/IC-04, edges `IC-01 → IC-01b → {IC-03, IC-04}`. This is the
   exact contract-step-ownership gap the mission's own field report documents.
2. **Re-seed namespace (C-011)**: IC-08's resolved-binding re-seed MUST use a NEW
   `_seed_id(…, "resolved_binding")` — reusing the committed `"claim"` seed id makes the idempotent re-run
   silently skip, leaving resolved slots empty corpus-wide. Add an acceptance test that the extended
   backfill returns `"wrote"`, not `"skip"`.
3. **Checkbox removal ordering (C-010)**: remove the `- [ ] T###` markdown checkboxes only AFTER the
   backfill has seeded historical subtask completion from them (they are the legacy source). Reroute the
   lane-transition guard (`core/subtask_rows.py`) onto the snapshot `subtasks` slot; it is behaviour-sensitive.
4. **Dispatch→claim linkage (IC-08)**: the claim seam has only the bare `--agent` string; the genuine model
   is resolved only in the invocation layer (keyed by `invocation_id`). Recording the frontmatter value is
   forbidden (C-007). You must thread the resolved model+profile from the Op record into the implement/review
   commands. Where a genuine model is unavailable, record it **explicitly absent** — never fabricated.
5. **Local `actor` is `str`-typed end-to-end** (`StatusEvent.actor`, `build_status_event`, `from_dict` does
   `str(...)`). The SaaS fan-out (FR-015) is "zero *shared-package* change" (6.1.0 already accepts a dict
   actor) but requires **non-trivial local plumbing** to widen `actor` to `str | dict` and guard the
   round-trip coercions. Size IC-09 accordingly.
6. **#2093 invariant coverage hole**: its detector only matches `extract_scalar(...)`; it is blind to
   attribute-access reads (`read_wp_frontmatter().agent`). Emptying the tolerated set is a false green until
   IC-05 EXTENDS the detector to the attribute-read class (prove it flags the dashboard scanner red first).
7. **ADR before vocabulary**: the IC-08a field-authority ADR (resolved role/profile/model → dynamic;
   authored → static) must land before the IC-08 vocabulary change (C-009).
8. **`status_phase` stays live** for the kept `_legacy_lane_mirror_enabled` (C-004) — do NOT retire the
   field in IC-06; flipping it activates the lane mirror (add a regression that lane behaviour is unchanged).
9. **`migration/mission_state.py`** is named in the original brief but NOT in the plan's edit map — verify
   at `/tasks` whether it's actually touched; drop from the surface list if not (else surgical-only).
10. **Dead-symbol re-pin**: the 15-symbol `_CATEGORY_C_DEFERRED_RUNTIME_STATE_BACKFILL_CUTOVER` frozenset
    in `tests/architectural/test_no_dead_symbols.py` MUST be removed in the WP that first wires a caller
    (IC-01), or the ratchet trips. That gate pins by content hash.

## Open coordination
- The **SaaS team is aware** of the new resolved-binding event; coordinate the final `actor`/event contract
  with them (FR-015 / IC-09).
- Follow-ups to file if deferred: the `_legacy_lane_mirror_enabled`/`lane` eviction (C-004); IC-06 if split;
  a `WPResolvedBindingChanged` shared event only if the off-transition fan-out path is chosen.
