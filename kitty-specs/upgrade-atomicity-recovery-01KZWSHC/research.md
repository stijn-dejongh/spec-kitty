# Research & Corroboration — Upgrade/migration atomicity & recoverability

**Mission**: `upgrade-atomicity-recovery-01KZWSHC` · **Date**: 2026-08-13
**Method**: post-spec corroboration squad (3× researcher-robbie code-grounding + 1× architect-alphonso architectural grounding), read-only, evidence cited to file:line against the current tree. Field-report claims on issues #3334–#3372 were verified against source; where the tree has drifted from the `3.2.6` builds the issues were filed on, the drift is flagged.

**Headline**: the *problem* is real and the phasing is sound, but three field-report root causes are **inaccurate against current source** and must be reworded before planning. Two user stories should **conform to existing ADRs** rather than invent patterns.

---

## US1 — recovery (#3334 / #3338), FR-001/002/003

- **`upgrade` is NOT gated behind `schema_version`** (field report's stated root cause is REFUTED). It is exempt in the CLI gate (`migration/gate.py:86,119`), classified SAFE (`compat/safety.py:85`), and its own too-new guard returns early on legacy (`cli/commands/upgrade.py:518-519`). → **Reword FR-001** away from "let upgrade run when schema_version missing" (already true) toward **restoration + non-recurrence**.
- **The real `upgrade` wedge**: on any migration failure, `schema_version` is not restored, so a re-run re-detects LEGACY, recomputes the full migration set, and **re-hits the same failing migration** on the still-invalid artifact (`has_migration` counts only `result=="success"`, `upgrade/metadata.py:242`).
- **`schema_version` "deletion" is a save/stamp ordering bug, not a `del`.** `ProjectMetadata.save()` rewrites `metadata.yaml` from a fixed dict that omits `schema_version` (`upgrade/metadata.py:188-210,32-35`); the compensating `_stamp_schema_version` runs **only on success** (`upgrade/runner.py:181-190`), skipped on the mid-loop `break` (`:172-178`). → **FR-002 smallest seam**: move the re-stamp out of the `result.success` guard (try/finally around the loop). **Add** a resumable-upgrade idempotency requirement (re-run after preservation is a safe no-op).
- **#3338 diagnostic gating is CORROBORATED (hard block, exit 4).** The failed migration recommends `spec-kitty migrate backfill-runtime-state --dry-run` (`migrations/m_zz_runtime_state_backfill.py:114-116`), but only the bare `("migrate",)` path is registered SAFE (`compat/safety.py:86`) and `classify()` fails closed on the missing subcommand (`:145-147`) → `BLOCK_PROJECT_MIGRATION` (`compat/planner.py:369-370`). This — not `upgrade` — is the command "gated behind the destroyed state." → **FR-003 smallest seam**: register `("migrate","backfill-runtime-state")` SAFE via a `--dry-run` predicate (mechanism exists, `safety.py:113-134`).
- **Conform to** ADR `docs/adr/3.x/2026-05-10-1-deterministic-historical-mission-state-repair.md` (non-destructive, git-safe, deterministic repair) for the FR-001 recovery command + NFR-002.

## US2 — atomicity (#3335), FR-004/005

- **Non-atomic + silent = CORROBORATED**, but the per-mission model is **intentional and documented** (`m_zz_runtime_state_backfill.py:14-17`, research D-03: "per-mission atomicity … no cross-mission transaction primitive to roll back with"). → **FR-004's corpus-rollback contradicts shipped design.** Lean primary on **FR-005 (report-on-abort)**: `_cutover_corpus` already returns the full `results` list and `apply()` **discards it** on abort (`:284-286`) — enumerating the written set is a localized change. Mark full corpus-atomicity (FR-004) as higher-risk / `[NEEDS CORROBORATION]`.
- **Conform to** ADR `docs/adr/3.x/2026-04-17-2-charter-synthesizer-atomicity.md` (stage under `.staging/<runid>/` → validate → `os.replace` promote → preserve `.failed/cause.yaml`). Its `cause.yaml` **is** NFR-003's machine-readable partial-write account. Reuse, don't reinvent.
- Field counts "22 meta.json + 16 status.events.jsonl" are field-observed (mechanistically consistent), not code-derived — keep attributed as such.

## US3 — the trigger (#3372), FR-006/007/008

- **The inline `review_feedback` dual-write is NOT reachable in current code** (REFUTED as live; CORROBORATED as legacy). The canonical path writes a **`review-cycle://` pointer + a separate `review-cycle-N.md` artifact**, never an inline key (`tasks_materialization.py:201-226`; `WP_FIELD_ORDER` excludes it, `frontmatter.py:50-79`; `strip_frontmatter.py:46-65` removes it). The legacy origin: `task_utils/support.py::set_scalar` **append-on-miss** (`:196-204`) + templates seeding `review_feedback: ''`; retired by commit `b13c47f9a`. `set_scalar` now has **zero production callers**.
- **The frontmatter read boundary ALREADY fails closed**: ruamel round-trip (`frontmatter.py:83`) raises `DuplicateKeyError` → `FrontmatterError` (`:122-127`); `write()` takes a dict and structurally can't emit a dup key. So the issue's "silently takes last value" is REFUTED. This is *why* the migration aborts loudly (the US2 problem), not silently corrupts downstream.
- **Reframe US3**: FR-006 → retire/fail-close the latent `set_scalar` footgun and reword AC1 away from "exactly one inline key" toward "no inline key ever + no re-append path". FR-007 → **legible** `DuplicateKeyError` message + pin `allow_duplicate_keys=False` (regression test) + raw-text pre-parse scan in `validate_frontmatter` feeding detect. FR-008 → **net-new** doctor scan/repair over `kitty-specs/**/*.md` (no existing artifact dup-key scan; seam `status/doctor.py`), atomic per NFR-004, keep-last (non-empty) repair policy. "Kill the trigger" is mostly already killed → this is guard + repair.

## US4 — honest preview (#3336), FR-009

- **`null` serialization is REFUTED against current source** — it serializes as `[]`/dicts (`compat/messages.py:147-159`); `null` may have been true on the reporter's `SHA ada9b45c2` build only. **Overclaim → reword.**
- **Real defect = two divergent pending-set computations**: preview uses compat-planner `_pending_migrations_for` gated on `BLOCK_PROJECT_MIGRATION` (`planner.py:1027`) while the real run uses `MigrationRegistry.get_applicable` (`upgrade.py:751`); plus `_provision_missing_mission_type_activations` never runs in dry-run (`upgrade.py:446,480-481`). → **FR-009 fix = unify the preview through the real detector**, not patch the serializer.

## Cross-cutting gaps (architect)

- **G4 — migration ledger (#2933) is the missing substrate.** There is no `spec-kitty doctor migrations`; `applied_migrations` is a side-record, not execution authority. US1 recovery/FR-005 has no authoritative "what did the half-run write." Reconcile FR-005/NFR-003 with #2933's ledger intent or explicitly scope-defer + note the coupling.
- **G6 — event-log integrity unguarded after partial write.** `status.events.jsonl` is the append-only sole authority; a half-applied backfill threatens reducer determinism. **Add NFR** for reducer-consistency/append-only integrity after recovery.
- **Ordering (C-001) is policy, not code-forced.** US1/US2/US3 touch disjoint modules and build independently. Enforce "recovery before prevention" via **explicit WP dependency edges at finalize-tasks**, not assumption. **Pull FR-008 (detect/repair) forward into the US1 recovery bundle** — it serves heal-before-upgrade.

## Net planning directives

1. Reword FR-001 (restoration+non-recurrence), FR-009 (unify preview path), US2 (report-on-abort primary + staging ADR), US3 (guard+repair, legacy writer retired).
2. Add: FR-012 resumable-upgrade idempotency; NFR-005 event-log/reducer integrity after recovery.
3. Conform to ADRs `2026-04-17-2` (US2) and `2026-05-10-1` (US1); reconcile epic #2933 (ledger).
4. Sequence WPs: US1 + FR-008 (recovery bundle) → US2 → US3 (FR-006/007) → US4 → US5, as finalize-tasks dependency edges.

## Evidence index (primary seams)
`upgrade/runner.py` (save/stamp ordering) · `upgrade/metadata.py` (schema_version omission) · `migration/gate.py` + `compat/safety.py` + `compat/planner.py` (FR-001/003) · `migrations/m_zz_runtime_state_backfill.py` + `migration/runtime_state_cutover.py` (US2) · `frontmatter.py` + `task_utils/support.py` + `review/cycle.py` (US3) · `upgrade/detector.py` + `compat/messages.py` (FR-009) · `status/doctor.py` (FR-008). ADRs: `2026-04-17-2`, `2026-05-10-1`. Epic: #2933.
