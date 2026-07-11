# Contract: decide_next() Parity Oracle (the characterization safety net)

The load-bearing safety net for the whole behavior-preserving refactor. Built in WP-0, proven green on **unmodified** source, then re-run as the acceptance gate of every extraction WP. Full derivation: research.md §Parity.

## Equality contract — `canonical(decision, repo_root)`
Over `Decision.to_dict()` (`decision.py:82-166`):
- **MASK** (drop before compare, but keep None-vs-present so a kind-shape change isn't blinded): `timestamp` (`bridge:2542`), `run_id`, `decision_id` (ULIDs).
- **PATH-NORMALIZE** (relativize to `repo_root`): `workspace_path`, `prompt_file`, **`reason`** (non-obvious carrier — embeds `feature_dir`/`exc` paths), `origin.mission_path` (`bridge:2575`). NB `origin.mission_tier` stays STABLE.
- **STABLE** (compare as-is): everything else — `kind`, `agent`, mission identity, `state`, `action`, `wp_id`, `step_id`, `guard_failures` (content **and order**), `progress`, `question`/`options`, `is_query`, …

`assert_parity(before, after, repo_root)` = `canonical(before, root) == canonical(after, root)`.

## Side-effect isolation
Each fixture runs **once** against a fresh `copytree` of a frozen repo snapshot with a fixed `repo_root`:
- Run create/advance (`get_or_start_run`) runs **REAL** on the throwaway copy (its ULID is masked).
- **STUB** (optionally CAPTURE for secondary asserts): the sync emitter (`bridge:2556`), the coord-branch `DecisionGitLog` commit (`bridge:2563`), the retrospective `Confirm.ask` gate.
- The runtime planner (`next_step`) is **never** stubbed — it is the logic under test.

## Fixture matrix + coverage floor (binding)
- **29 `Decision(...)` sites** (19 blocked / 4 step / 4 query / 1 terminal / 1 decision_required) across 7 orchestrator phases.
- Both guards fully branched: `_check_cli_guards` (`:1057`, ~10 branches incl. requirement-ref cross-check) and `_check_composed_action_guard` (`:1515`) across **3 mission families** (software-dev / research / documentation), including **both fail-closed defaults** and the 4-way `tasks` `legacy_step_id` union.
- **Coverage floor: every Decision site ≥1× AND every guard branch ≥1×.** Ledger ≈ 22–26 fixtures.
- **Named highest-risk fixtures**: the two fail-closed defaults + the `tasks` legacy-union — each asserts identical `guard_failures` content **and order** before/after.

## Gate semantics
- WP-0 done ⇔ oracle green on unmodified source at full coverage-floor.
- Every subsequent extraction WP: oracle stays green (its acceptance gate). A parity break = the extraction changed behavior = reject.
