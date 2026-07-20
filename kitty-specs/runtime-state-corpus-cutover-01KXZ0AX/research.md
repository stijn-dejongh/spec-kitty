# Phase 0 Research: Runtime-State Corpus Cutover

All spec requirements are grounded in the post-#2817 tree (verified by the pre-planning brownfield
squad — see spec "Pre-planning verification note"). No `[NEEDS CLARIFICATION]` markers remain; the
decisions below are engineering choices resolved from the spec + charter, recorded here as the
authoritative design ground for `/spec-kitty.tasks`.

## D-01 — One shared cutover orchestration helper (not two callers re-implementing verify-then-flip)

- **Decision**: Add `migration/runtime_state_cutover.py` — a single helper implementing
  `backfill → fail-closed verify → atomic per-mission status_phase flip`. Both the operator CLI
  (IC-01) and the upgrade migration (IC-02) call it.
- **Rationale**: The fail-closed atomicity (NFR-001) is the load-bearing invariant; it must live in
  exactly one place. Two callers re-deriving "seed, then verify, then flip only if ok" is precisely the
  logical-duplication trap (one operation across N sites → one canonical seam). The helper wraps the
  existing library's `run_backfill_and_verify` and adds the flip.
- **Alternatives rejected**: (a) put the flip logic in the CLI and have the migration shell out to the
  CLI — brittle, couples migration to CLI parsing; (b) duplicate verify-then-flip in each caller —
  drifts, and a bug fixed in one is missed in the other.

## D-02 — status_phase is the *sole-writer, post-verify migrated-marker*; correctness rests on ordering, not a runtime gate

- **Decision**: The cutover helper is the **only** writer of `meta.json` `status_phase`, and writes it
  **only after** a mission's verify passes (FR-003). After IC-03 deletes the predicate, runtime readers
  are **unconditional** (always the snapshot) and no longer read `status_phase`; the field then serves
  as a durable per-mission "backfilled + verified" audit/idempotency marker.
- **Why this is coherent (the subtle part)**: Once readers are unconditional, an un-backfilled mission
  reads `None` **regardless** of `status_phase`. So end-state correctness for existing deployments does
  **not** come from a runtime gate — it comes from the **upgrade migration running the backfill before
  the upgraded code serves a runtime read** (IC-02). `spec-kitty upgrade` installs new code and runs
  migrations within one command; the only window where new-code-meets-un-backfilled-corpus is *inside*
  that command, closed by the migration itself. This is standard migration sequencing; recorded as a
  precondition (no concurrent spec-kitty runtime command during `upgrade`).
- **Consequence / refuse-to-flip footgun**: because `status_phase` has no other writer, the guard
  "refuse to flip a mission whose verify hasn't passed" is enforced by making the helper the sole path
  that ever writes it — there is no hand-flip surface to abuse (the brief's explicit concern).
- **Idempotency source of truth**: the **backfill seeds** (deterministic content-namespaced ULIDs),
  not `status_phase`. A re-run seeds nothing because the ids already exist; `status_phase` is a fast
  skip-hint, not the correctness anchor.
- **Open refinement (→ IC-06 candidate, non-blocking)**: once readers are unconditional, `status_phase`
  is inert at runtime. Retiring the meta field itself could fold into the IC-08 reduction — but only
  after confirming zero readers. Kept OUT of the critical path; FR-003 as specified stands.
- **Alternatives rejected**: drop `status_phase` entirely and rely only on backfill idempotency — loses
  the audit marker and contradicts FR-003's explicit "sole writer" requirement; keep `status_phase` as a
  live runtime gate — contradicts C-002 (unconditional; predicate deleted).

## D-03 — CLI = per-mission best-effort; upgrade migration = fail-closed abort on any failure

- **Decision**: `spec-kitty migrate backfill-runtime-state` flips each mission independently: it seeds +
  verifies + flips every mission that passes, records failures, and exits non-zero if any mission
  failed (never flips an unverified mission). The **upgrade migration** is stricter: **any** mission's
  verify failure aborts the whole migration step with an operator-actionable message (NFR-005), leaving
  no mission half-flipped.
- **Rationale**: The CLI is an operator tool — reporting per-mission results and letting the operator
  triage is more useful than all-or-nothing. The upgrade path is unattended and must not leave a
  deployment in a mixed/ambiguous state without the operator knowing, so it fails the upgrade step
  loudly. Both honour "refuse to flip unverified" (NFR-001); they differ only in blast-radius on failure.
- **"Non-partially-flipped" clarified (NFR-005)**: a mission is never left *half*-flipped (flipped
  without a passing verify). Across the corpus, each mission is independently consistent — either
  flipped-and-verified or not-flipped-and-legacy. NFR-005's guarantee is *per-mission* atomicity, not
  corpus all-or-nothing.
- **Alternatives rejected**: corpus-wide all-or-nothing transaction for the CLI — no cross-mission
  atomicity primitive exists (each mission is an independent event log), and it would block the whole
  corpus on one bad mission.

## D-04 — Upgrade migration is a new auto-discovered module, ordered after the charter folds

- **Decision**: Add `upgrade/migrations/m_<version>_runtime_state_backfill.py` self-registering via
  `@MigrationRegistry.register`; no central sequence-list edit (`auto_discover_migrations()` walks
  `m_*.py`). Choose a version-key prefix that sorts **after** the charter-fold migrations.
- **Rationale**: Matches the canonical upgrade-migration pattern (the charter.yaml fold the brief cites);
  hand-rolling a sequence entry would drift from the registry mechanism.
- **Alternatives rejected**: a manual runner hook — not the sanctioned surface.

## D-05 — Fallback deletion order: verify the event-sourced replacement exists first (merge path)

- **Decision**: Before deleting `merge/done_bookkeeping.py::_extract_done_evidence` (frontmatter
  done-evidence synthesis, FR-006b), confirm the merge done path already reads done-evidence from the
  event log for backfilled missions. The verdict fallback in `workflow_cores.py` (FR-006a) is the
  **same block** as the FR-007 review bypass reader → deleted-and-rerouted as one edit.
- **Rationale**: `done_bookkeeping` feeds the **merge** gate; deleting synthesis without an event-sourced
  replacement would break merge for any mission. C-001 order (delete fallbacks only after backfill has
  seeded the approvals as events) makes this safe, but the replacement read must be exercised by a test.
- **Alternatives rejected**: delete first and fix merge later — violates C-001 and risks a red merge gate.

## D-06 — Not a DIRECTIVE_035 bulk edit

- **Decision**: No `occurrence_map.yaml`. The 12-site flag removal is a **heterogeneous per-site
  refactor** — each call site collapses its `if predicate: … else: …` differently (some keep the
  snapshot branch, some are early-returns, `support.py` has two distinct sites). It is not a mechanical
  same-string replacement.
- **Re-verify trigger**: if, during implementation, the collapse proves mechanically uniform across
  sites, revisit and add the map. Current evidence (squad) says heterogeneous.

## Risks & pre-existing-red discipline (charter: Pre-existing Failure Reporting)

- **Phantom `SYNC_DISABLE_ENV_VARS`** `arch-adversarial (arch_shard_1)` red is **pre-existing on main**
  (CI-runner artifact, exists nowhere in source) — NOT this mission's; do not "fix".
- **Known-P0 reds** (ADR 2026-07-17-1: #2736, #2772, #1834) stay red; confirm on merge-base before
  attributing any red to this diff (test-run baseline-red gotcha).
- **`uv run` discipline**: run tests via `uv run --extra test python -m pytest -p no:cacheprovider <FILE>`
  — bare `python` resolves a sibling checkout and yields false greens.
- **Never run the whole `tests/architectural/` dir** — it hangs; per-file with a timeout only.
- **Dead-symbol re-pin coupling**: the 15-symbol frozenset un-pin MUST land in the WP that first wires a
  caller (IC-01), or `test_no_dead_symbols` / `test_auto_exempt_disjoint_from_hand_allowlist` trips.
- **`done_bookkeeping` under `merge/`** — a merge-path change; exercise the event-sourced done-evidence
  read before deleting the synthesis.

## Best practices applied

- ATDD-first (C-011): each new branch/helper (orchestration helper, CLI command, upgrade migration,
  bypass-reader reroute, fail-closed abort) gets a focused test in the same WP, incl. fault-injection
  for verify-abort and flip-refusal.
- Sonar: complexity ≤15 (extract the orchestration into small phases: seed / verify / flip); hoist
  repeated literals (command names, `status_phase` key, messages) to constants; no suppression.
