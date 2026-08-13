# Implementation Plan: Upgrade/migration atomicity & recoverability

**Branch**: `spec/upgrade-atomicity-recovery` | **Date**: 2026-08-13 | **Spec**: [spec.md](./spec.md) · [research.md](./research.md)
**Input**: Feature specification from `kitty-specs/upgrade-atomicity-recovery-01KZWSHC/spec.md`

## Summary

Remediate the interlocking upgrade-wedge cluster (epic #3347 + root trigger #3372) so a failed upgrade is **recoverable, atomic, and honestly reported**. Corroboration (`research.md`) corrected three field-report root causes and set the technical approach: the P0 is a `schema_version` **save/stamp ordering** fix plus a diagnostic **SAFE-classification** (not "ungate upgrade"); atomicity leans on **report-on-abort** (the data is already collected) and the canonical **staging-promote ADR**, not corpus rollback; the duplicate-key trigger is **legacy/retired**, so US3 is **guard-hardening + detect/repair**. Delivery is sequenced **recovery → atomicity → prevention → observability → hygiene**, enforced by WP dependency edges (policy, not code-forced).

## Technical Context

**Language/Version**: Python 3.11+ (repo standard; ruff/mypy strict, complexity ≤15)
**Primary Dependencies**: `typer`, `rich`, `ruamel.yaml` (round-trip frontmatter), existing `specify_cli` internals — no new runtime deps
**Storage**: on-disk mission artifacts — `metadata.yaml`, `meta.json`, WP `.md` frontmatter, append-only `status.events.jsonl`; no DB
**Testing**: `pytest` (ATDD-first). P0 (#3334) requires an issue-pinned red-first `@pytest.mark.regression` reproduction (ADR `2026-07-17-1`). New-code coverage on every extracted helper/branch (Sonar gate)
**Target Platform**: local CLI (Linux/macOS), Python 3.11–3.13
**Project Type**: single project (`src/specify_cli/…`, `tests/…`)
**Performance Goals**: N/A (correctness/reliability mission, not throughput)
**Constraints**: zero ruff/mypy suppressions; terminology guard green; conform to ADRs `2026-04-17-2` (staging atomicity) and `2026-05-10-1` (deterministic repair); loopback/localhost rules N/A
**Scale/Scope**: ~7 tracker issues, 12 FR / 5 NFR / 4 C; ~7 source seams across `upgrade/`, `migration/`, `compat/`, `frontmatter.py`, `status/doctor.py`

## Charter Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **ATDD-first / red-first**: PASS — acceptance scenarios per US; NFR-001 mandates a red-first P0 reproduction for #3334.
- **Architectural alignment / canonical sources**: PASS with a binding constraint — US1 **adopts the non-destructive + deterministic principles** of ADR `2026-05-10-1` and **reuses its `migration/mission_state.py` repair machinery** (`repair_repo`/`RepairReport`/`FileChange`/`atomic_write`), not a net-new repair; US2's **FR-004 only** conforms to the staging-promote ADR `2026-04-17-2` (the primary FR-005 path is honest-reporting, no staging). No new shadow paths. See §Post-Plan Adversarial Revisions.
- **Tiered rigour (DDD)**: PASS — reliability-critical seams (migration runner, frontmatter boundary) get tests at the unit + integration tier; hygiene (US5) is lighter.
- **Terminology canon**: PASS — "Mission" not "feature"; run `tests/architectural/test_no_legacy_terminology.py` before push.
- **Quality gates**: PASS — zero suppressions; every new helper/branch carries focused tests (Sonar new-code coverage).
- **Ledger coupling (#2933)**: DEFERRED-with-note — FR-005/NFR-003 reconcile with the migration-ledger intent or explicitly scope-defer (C-004); recorded in Complexity Tracking.

## Project Structure

### Documentation (this mission)

```
kitty-specs/upgrade-atomicity-recovery-01KZWSHC/
├── spec.md              # corroborated requirements
├── research.md          # corroboration record (file:line evidence)
├── plan.md              # this file
└── tasks.md + tasks/    # /spec-kitty.tasks output (next step)
```

### Source Code (repository root)

```
src/specify_cli/
├── upgrade/
│   ├── runner.py                     # IC-01: move _stamp_schema_version out of success-guard (FR-002/012)
│   ├── metadata.py                   # IC-01: schema_version omission on save-rewrite (FR-002)
│   ├── detector.py                   # IC-04: MigrationRegistry.get_applicable (real pending set)
│   └── migrations/
│       ├── base.py                   # IC-02: MigrationResult partial-write channel (FR-005)
│       └── m_zz_runtime_state_backfill.py  # IC-02: report-on-abort / staging (FR-004/005)
├── migration/
│   ├── gate.py                       # IC-01: upgrade/init exemption (context)
│   ├── runtime_state_cutover.py      # IC-02: per-mission cutover write model
│   └── schema_version.py             # IC-01: legacy classification on missing schema
├── compat/
│   ├── safety.py                     # IC-01/04: SAFE registration (FR-003); planner path
│   ├── planner.py                    # IC-04: divergent pending_migrations (FR-009)
│   └── messages.py                   # IC-04: render_json pending set
├── frontmatter.py                    # IC-03: legible duplicate-key guard (FR-007)
├── task_utils/support.py             # IC-03: retire/fail-close set_scalar append-on-miss (FR-006)
├── status/doctor.py                  # IC-03: net-new dup-key scan/repair (FR-008)
└── cli/commands/upgrade.py           # IC-04: dry-run routing (FR-009)

tests/
├── upgrade/ · migration/ · compat/   # unit + integration for the seams above
└── (issue-pinned regression for #3334, @pytest.mark.regression)
```

**Structure Decision**: single-project layout; all changes land under `src/specify_cli/` with mirrored tests under `tests/`. No new packages; reuse existing seams named in `research.md`.

## Complexity Tracking

| Violation / Risk | Why Needed | Simpler Alternative Rejected Because |
|------------------|------------|--------------------------------------|
| FR-004 corpus staging (staging-promote) | True "mutate nothing on abort" for a bulk migration | Corpus rollback rejected by D-03 (no cross-mission transaction); FR-005 report-on-abort is the cheap primary, FR-004 is optional/higher-risk and must reuse ADR `2026-04-17-2` |
| Migration-ledger reconciliation (#2933) | FR-005/NFR-003 need an authoritative "what did the half-run write" | Building a full ledger now is out of scope; deferred with an explicit note + coupling flag rather than silently reinvented |

## Implementation Concern Map

> Concerns are NOT work packages. `/spec-kitty.tasks` translates these into WPs (one IC may become several WPs; small ICs may merge). No WP-style IDs or sequencing verbs here.

### IC-01 — Recovery & non-recurrence (the P0 escape hatch)

- **Purpose**: Make a mid-migration failure survivable — `schema_version` survives, a re-run doesn't re-abort on the same artifact, and the recommended diagnostic is reachable.
- **Relevant requirements**: FR-001, FR-002, FR-003, FR-012; NFR-001 (red-first #3334), NFR-002 (non-destructive, ADR `2026-05-10-1`).
- **Affected surfaces**: `upgrade/runner.py` (re-stamp out of success-guard), `upgrade/metadata.py` (save-rewrite omission), `compat/safety.py` (register `("migrate","backfill-runtime-state")` SAFE via `--dry-run` predicate), `compat/planner.py` / `migration/gate.py` / `migration/schema_version.py` (classification context).
- **Sequencing/depends-on**: none — lands first; **FR-008's repair (from IC-03) ships with this bundle** (heal-before-upgrade).
- **Risks**: FR-001's true blocking point must be pinned before coding (research says the field report mis-located it); re-stamp reorder must be idempotent/re-entrant (FR-012).

### IC-02 — Migration atomicity & honest partial-write reporting

- **Purpose**: A bulk cutover never silently leaves a partial write; the abort enumerates exactly what it wrote.
- **Relevant requirements**: FR-005 (primary), FR-004 (optional, staging ADR), NFR-003, NFR-005 (event-log/reducer integrity).
- **Affected surfaces**: `upgrade/migrations/m_zz_runtime_state_backfill.py` (`apply`/`_cutover_corpus` — stop discarding `results`), `upgrade/migrations/base.py` (`MigrationResult` partial-write channel), `migration/runtime_state_cutover.py` (write model if FR-004 pursued).
- **Sequencing/depends-on**: IC-01 (policy: recovery must exist before atomicity so a mid-run abort can't strand).
- **Risks**: FR-004 contradicts the intentional per-mission design (D-03) — treat as optional/staging-ADR; NFR-005 must guard append-only reducer determinism after recovery.

### IC-03 — Frontmatter guard & legacy-artifact repair

- **Purpose**: Harden against the (retired) duplicate-key trigger and clean existing malformed artifacts.
- **Relevant requirements**: FR-006 (retire `set_scalar` append-on-miss), FR-007 (legible fail-closed guard + pin `allow_duplicate_keys=False`), FR-008 (net-new doctor scan/repair), NFR-004 (repair batch-atomic).
- **Affected surfaces**: `frontmatter.py` (`read`/`validate` legible message), `task_utils/support.py` (`set_scalar`), `status/doctor.py` (new scan/repair over `kitty-specs/**/*.md`).
- **Sequencing/depends-on**: **FR-008 repair ships with IC-01 recovery bundle**; FR-006/FR-007 guard-hardening follows IC-02.
- **Risks**: repair policy (keep-last non-empty) must not discard recorded state; keep the guard centralized in the canonical boundary (C-002).

### IC-04 — Honest dry-run preview

- **Purpose**: `upgrade --dry-run` reports the real pending set by using the same detector the real run uses.
- **Relevant requirements**: FR-009.
- **Affected surfaces**: `cli/commands/upgrade.py` (dry-run routing), `compat/planner.py` (`_pending_migrations_for` divergence), `upgrade/detector.py` (`MigrationRegistry.get_applicable`), `compat/messages.py` (`render_json`).
- **Sequencing/depends-on**: none — independent; parallelizable with IC-05.
- **Risks**: reconcile two computation paths without regressing the block-decision semantics; the `null` framing is stale (fix the divergence, not the serializer).

### IC-05 — Mission-create & remediation-surface hygiene

- **Purpose**: Adjacent rough edges — remediation body survives `--json`; failed mission-create restores checkout.
- **Relevant requirements**: FR-010, FR-011.
- **Affected surfaces**: charter-pack-invalid path in mission-create `--json`; mission-create branch/checkout restore (coordinate with #3328).
- **Sequencing/depends-on**: none — lowest blast radius, parallelizable.
- **Risks**: FR-011 must coordinate with #3328's mission-create git-side-effect rework to avoid double-fixing.

## Post-Plan Adversarial Revisions (binding)

A profile-loaded squad (architect-alphonso, planner-priti, reviewer-renata) stress-tested this plan and verified every load-bearing seam. The following decisions are **binding** and supersede any conflicting IC wording above; the tasks step consumes them directly.

**Correctness fixes (must-do):**
1. **FR-002 = preserve, not re-stamp-to-target.** A literal `try/finally` re-stamp would write `REQUIRED_SCHEMA_VERSION=3` onto a *failed/legacy* project (`_stamp_schema_version` writes the target; `schema_version.py:22-27`), opening the gate on a half-backfilled corpus — the exact dishonest-state bug this mission closes. Capture the pre-run `schema_version` and restore on abort (or stop `save()` from erasing it); stamp target only on success. Invariant: **a failed migration never advances `schema_version`.**
2. **#3334 red-first repro is trigger-agnostic.** Force the mid-loop abort with a **synthetic always-failing migration**, not a real duplicate-key artifact — otherwise the co-shipped FR-008 repair heals the trigger and the P0 test passes for the wrong reason (masking). (reviewer H3 / planner M2)
3. **FR-008 reuses the ADR's repair framework.** Detection = a `check_*` Finding + a small extracted **raw-text duplicate-key detector module** (e.g. `status/dup_key_repair.py`, NOT grown into the `status/doctor.py` god-module, #1623). Repair = extend `migration/mission_state.py` (`repair_repo`/`RepairReport`/`FileChange`/`atomic_write`) surfaced via `cli/commands/_mission_state_doctor.py`, **opt-in `--fix`** (because `doctor` is unconditionally SAFE), non-destructive (NFR-002), batch-atomic (NFR-004). (architect HIGH-2 / reviewer M1)
4. **FR-003 predicate fails closed.** Register `("migrate","backfill-runtime-state")` SAFE **iff** `--dry-run` present; UNSAFE otherwise and on predicate exception.

**Scope / framing fixes:**
5. **FR-001 is a composition WP** (FR-002 + FR-008 + FR-012 wiring → SC-001), depends on FR-002+FR-008 — not a parallel unknown. No net-new command unless proven necessary.
6. **Recovery is roll-forward** (`detect()`-gated re-run), which is *why* ledger #2933 is safely deferred. NFR-003's machine-readable account is scoped to **graceful** abort; durable cross-run/SIGKILL accounting is deferred with #2933.
7. **SIGKILL edge case is FR-004-only.** FR-005 cannot cover a process that never returns; if FR-004 is deferred, the SIGKILL edge case is explicitly out of scope.
8. **NFR-005 gets a concrete test.** Assert `reduce()` over the recovered log == pre-abort log ∪ committed events; mechanism = `detect()`-gating + reducer `event_id` de-dup. Owned as a verification WP depending on the recovery bundle + FR-005.
9. **Staging + append-only tension (if FR-004 ships):** `status.events.jsonl` must be staged/promoted append-preservingly (staged = prior ∪ appended, verified monotonic) so `os.replace` can't violate NFR-005.
10. **ATDD-first applies to every FR**, not only #3334: each acceptance scenario lands as a failing test before its code.
11. **Housekeeping:** migrate `tests/utils.py`'s `set_scalar` callers as part of FR-006 retirement; FR-007 adds an explicit `except DuplicateKeyError` branch naming the key + pins `allow_duplicate_keys=False` on the `YAML()` instance (`frontmatter.py:83`).

**Ordering = priority, not blocking edges.** Recovery-first is a *scheduling* preference; encoding it as `dependencies` frontmatter would gate *claiming* and needlessly serialize disjoint modules. The **only** genuine dependency edges: WP04→{WP01,WP03}; WP06→WP05; WP07→{WP01,WP05}; WP09→WP03. Everything else is claimable in parallel.

**WP-slice sketch (input to `/spec-kitty.tasks`):**
- **WP01** — #3334 red-first (synthetic failing migration) + FR-002/FR-012 preserve-`schema_version` ordering fix. *No deps. P0 core.*
- **WP02** — FR-003 ungate diagnostic (SAFE `--dry-run` predicate). *No deps.*
- **WP03** — raw-text dup-key detector module + FR-008 detect/repair via `mission_state` framework, `--fix`, batch-atomic. *No code deps; riskiest mandatory WP.*
- **WP04** — FR-001 recovery composition + SC-001 zero-git + no-VCS acceptance. *Deps: WP01, WP03.*
- **WP05** — FR-005 report-on-abort (stop discarding `_cutover_corpus` results) + NFR-003. *Parallel.*
- **WP06** *(optional)* — FR-004 corpus staging-promote (ADR `2026-04-17-2`, append-preserving events). *Deps: WP05.*
- **WP07** — NFR-005 reducer-integrity verification. *Deps: WP01, WP05.*
- **WP08** — FR-006 retire/fail-close `set_scalar` (+ migrate test callers). *Independent.*
- **WP09** — FR-007 legible dup-key message + pin `allow_duplicate_keys=False`. *Deps: WP03 (detector).*
- **WP10** — FR-009 unify dry-run through the real detector. *Independent.*
- **WP11** — FR-010 remediation body survives `--json`. *Independent.*
- **WP12** — FR-011 mission-create checkout restore (coordinate #3328). *Independent; external-coordination risk.*
