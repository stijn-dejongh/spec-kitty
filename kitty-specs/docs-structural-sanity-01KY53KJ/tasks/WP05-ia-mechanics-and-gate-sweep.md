---
work_package_id: WP05
title: IA-mechanics, tooling un-pin & aggregate gate sweep
dependencies:
- WP02
- WP03
- WP04
requirement_refs:
- C-006
- C-007
- FR-009
- FR-010
- NFR-001
- NFR-002
- NFR-004
planning_base_branch: docs/common-docs-section-audit
merge_target_branch: docs/common-docs-section-audit
branch_strategy: Planning artifacts for this mission were generated on docs/common-docs-section-audit. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into docs/common-docs-section-audit unless the human explicitly redirects the landing branch.
created_at: '2026-07-22T16:30:00+00:00'
subtasks:
- T022
- T023
- T024
- T025
- T026
history:
- timestamp: '2026-07-22T16:30:00Z'
  agent: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: python-pedro
authoritative_surface: scripts/docs/
create_intent: []
execution_mode: code_change
model: sonnet
owned_files:
- scripts/docs/redirect_stub_generator.py
- scripts/docs/bulk_ref_rewrite.py
- scripts/docs/redirect_map.yaml
- docs/development/3-2-page-inventory.yaml
role: implementer
tags: []
tracker_refs: []
---

# Work Package Prompt: WP05 – IA-mechanics, tooling un-pin & aggregate gate sweep

## ⚡ Do This First: Load Agent Profile

**Before reading any further**, load the `python-pedro` implementer profile via the `/ad-hoc-profile-load`
skill. Adopt its identity, governance scope, boundaries, and the initialization declaration it prints.
Everything below is authored for that profile: type-safe Python, canonical-tooling discipline, real CLIs
(never fabricated flags), gate-verified done-ness, no suppressions. Do not begin editing until the profile is
loaded and its init declaration is on the record.

- **Profile**: `python-pedro`
- **Role**: `implementer`
- **Agent/tool**: `claude`

---

## Sanctioned tool-driven leeway (read first — ownership note)

This WP runs `relative_link_fixer` (writes across `docs/**` referrers) + `toc.yml` regeneration across
referrer files that are NOT in any WP's `owned_files`. This is **sanctioned tool-driven leeway**: the
referrers are touched by a canonical tool sweep, not hand-edited feature work, and **no other WP claims those
referrer files** (WP03/WP04 explicitly deferred referrer repointing to this WP), so the no-overlap ownership
guard holds. The rationale is recorded here per the ownership-map-leeway discipline. Do NOT expand beyond the
tool-driven referrer rewrites + the derived artifacts in `owned_files`.

## Objectives & Success Criteria

Close the mission: un-pin the foreign-pinned redirect/link tooling (FR-010/C-007), regenerate the DERIVED
redirect-map / page-inventory / `toc.yml` against THIS mission's `occurrence_map.yaml`, repoint every referrer
(docs/** via `relative_link_fixer` + the one non-docs paradigm ref via `bulk_ref_rewrite`/manual), and run the
aggregate gate — the mission's Definition of Done.

```bash
MAP=kitty-specs/docs-structural-sanity-01KY53KJ/occurrence_map.yaml
```

**Success criteria (SC-002/003/004/005/006; NFR-001/002/004)**:
- `relative_link_fixer --check` → 0 broken relative links, 0 baseline-URL 404s (NFR-001).
- `redirect_stub_generator check-map --occurrence-map $MAP` → 1:1 coverage, no orphan (NFR-002).
- `check_docs_freshness --ci` → inventory/toc fresh, no baseline 404 (NFR-004).
- `docs_structural_lint` → exit 0 (SC-003/004/005: clean tree, 0 shadow basenames, full architecture/ index).
- `pytest tests/docs/` + the terminology guard green (NFR-004).
- Neither tool silently consumes the foreign `01KW3SBK` default (C-007).

## Context & Constraints

- **Charter**: `.kittify/charter/charter.md` — canonical sources (never fabricate flags), campsite cleaning,
  missing/broken canonical surface → trace + file upstream gap (C-007), no suppressions.
- **Read before editing**: `quickstart.md` (the VERIFIED real CLIs — Recipe A/B + the aggregate verify block;
  an earlier draft fabricated flags — obey quickstart exactly), `research.md` (D5 — the real subcommands/flags
  + the foreign-pinning facts), `plan.md` (IC-06), `spec.md` (FR-009/010; NFR-001/002/004; C-006/007),
  `occurrence_map.yaml` (the `moves:` spine + 3 fold entries + the `exceptions` incl. the non-docs paradigm
  referrer + the baseline-URL manifest note), `data-model.md` (redirect-map entry + state transition).
- **VERIFIED real CLIs (research.md D5 / quickstart — do NOT fabricate)**:
  - `redirect_stub_generator.py` subcommands: `regenerate-map | check-map | generate | coverage`. There is
    **NO** `--add/--old/--new`. `redirect_map.yaml` is **single-writer + DERIVED** ("do not hand-edit") —
    REGENERATED from the baseline manifest + this mission's `occurrence_map.yaml` `moves:` spine.
  - `relative_link_fixer.py` **writes by default** (flags `--dry-run` / `--check` / `--no-exclude`; there is
    **NO** `--write`) and walks **`docs/**` ONLY**.
  - `check_docs_freshness.py` uses `--inventory` (NOT `--write-inventory`) and `--ci`.
  - `bulk_ref_rewrite.py` is the prefix-anchored complement for non-`docs/` (`src/`, `scripts/`) referrers;
    accepts `--occurrence-map`.
- **C-007 (binding)**: EVERY redirect/link command passes `--occurrence-map "$MAP"`. Never rely on the built-in
  default (pinned to the foreign `common-docs-structural-move-01KW3SBK`).
- **C-004**: `3-2-page-inventory.yaml` + `toc.yml` are path-pinned (`test_inventory_path_stable.py`) —
  regenerate CONTENTS in place, NEVER relocate.
- **Prereqs**: WP03 (final move set) + WP04 (folds) must be landed; WP02's lint must exist. Read WP03's and
  WP04's Activity Logs for the referrer lists + the non-docs paradigm referrer hand-off + any borderline that
  moved (assessment/closeout) — the redirect-map regen must cover exactly the ACTUAL move set.
- **Stale-install note**: `redirect_stub_generator`/`bulk_ref_rewrite` behaviour reflects the installed CLI —
  if you edit them (T022) and behaviour seems unchanged, `pip install -e .` may be stale; run via
  `python -m scripts.docs.<tool>` from the repo root (which uses the working tree) to be sure.

## Branch Strategy

- **Strategy**: coord topology; execution worktree allocated per computed lane from `lanes.json`.
- **Planning base branch**: `docs/common-docs-section-audit`
- **Merge target branch**: `docs/common-docs-section-audit`

> Populated by `spec-kitty agent mission tasks` / `finalize-tasks`. Do not change manually.

## Subtasks & Detailed Guidance

### Subtask T022 — FR-010 un-pin the foreign-pinned tooling

- **Purpose**: FR-010/C-007 — neither tool may silently bind the foreign mission's occurrence map.
- **Steps**:
  1. `redirect_stub_generator.py`: find `MISSION_SLUG = "common-docs-structural-move-01KW3SBK"` (its DEFAULT
     occurrence-map source). Un-pin it — make the occurrence-map path a REQUIRED `--occurrence-map` argument
     (no foreign default) OR parametrize `MISSION_SLUG` so the default is not a specific foreign mission. If
     a clean un-pin is not feasible without broader refactor, **file an upstream gap** (charter: missing/broken
     canonical surface → trace + file) and drive strictly via `--occurrence-map` — record the gap issue in the
     Activity Log.
  2. `bulk_ref_rewrite.py`: find the hardcoded `.../common-docs-structural-move-01KW3SBK/occurrence_map.yaml`
     DEFAULT; un-pin identically (require `--occurrence-map` or parametrize) or file the same gap.
  3. Add/adjust a focused test if these tools have unit tests (`tests/docs/test_bulk_ref_rewrite.py` exists) —
     assert the default no longer resolves to the foreign slug (or that omitting `--occurrence-map` errors
     clearly rather than silently consuming a foreign map).
- **Files**: `scripts/docs/redirect_stub_generator.py`, `scripts/docs/bulk_ref_rewrite.py`.
- **Validation**: grep both for `01KW3SBK` → no live default binding; ruff/mypy clean; the existing
  `tests/docs/test_bulk_ref_rewrite.py` still green (adjust if it asserted the old default).
- **Edge cases**: if you file a gap instead of a full un-pin, the mission still proceeds via `--occurrence-map`
  — but the grep-for-`01KW3SBK`-default must show it is no longer SILENTLY consumed.

### Subtask T023 — Regenerate `redirect_map.yaml` against this mission's map

- **Purpose**: FR-009/NFR-002 — one redirect entry per moved/removed path (relocations + the 3 fold
  old-shadow→existing-canonical redirects).
- **Steps**:
  1. `python -m scripts.docs.redirect_stub_generator regenerate-map --occurrence-map "$MAP"` — regenerates the
     DERIVED `redirect_map.yaml` from the baseline manifest + this map's `moves:` spine (incl. the fold from→to
     pairs, which derive old-shadow.html → EXISTING canonical.html).
  2. `python -m scripts.docs.redirect_stub_generator check-map --occurrence-map "$MAP"` — assert 1:1 coverage
     (NFR-002): no moved/removed path lacks an entry, no orphan entry.
  3. If a borderline MOVED in WP03 (assessment/closeout verified point-in-time), ensure the map's `moves:`
     spine includes it before regenerating — the redirect must cover the ACTUAL move set. (If a borderline
     STAYED, it must NOT have a redirect entry.)
- **Files**: `scripts/docs/redirect_map.yaml` (DERIVED — regenerated, never hand-edited).
- **Validation**: `check-map` passes 1:1; `redirect_baseline_urls.json` closeout URL stays green (verify no
  baseline 404 after any closeout move).
- **Edge cases**: NEVER hand-edit `redirect_map.yaml` — if `check-map` fails, fix the `occurrence_map.yaml`
  `moves:` spine or the tooling, then regenerate.

### Subtask T024 — Repoint referrers (docs/** + the non-docs paradigm ref)

- **Purpose**: FR-009/NFR-001/C-006 — every in-repo referrer resolves to the new path.
- **Steps**:
  1. `python -m scripts.docs.relative_link_fixer` (writes by default; `docs/**` ONLY) — repoints relative
     links across the ~25–30 docs referrers to the moved/folded paths.
  2. `python -m scripts.docs.bulk_ref_rewrite --occurrence-map "$MAP"` — the prefix-anchored complement that
     rewrites NON-`docs/` referrers (`src/`, `scripts/`). This MUST catch
     `src/doctrine/paradigms/built-in/brownfield-onboarding.paradigm.yaml:50` (the moved audit path
     `docs/architecture/audits/2026-05-spec-kitty-caacs.md` → `…/plans/engineering-notes/architecture-audits/…`)
     — `relative_link_fixer` never walks it (occurrence_map `manual_review` exception). If `bulk_ref_rewrite`
     does not rewrite it, hand-edit the one line and record why.
  3. Cross-check against WP03/WP04's Activity-Log referrer lists (audits→11, adr-connector→6,
     feature-detection→5, 883-brief→2, gap-analysis→1, + any borderline) — confirm each is repointed.
- **Files**: docs/** referrers (tool-driven leeway) + `src/doctrine/paradigms/built-in/brownfield-onboarding.paradigm.yaml`.
- **Validation**: `relative_link_fixer --check` clean (T026); grep the paradigm.yaml for the old audit path →
  gone.
- **Edge cases**: the non-docs referrer is the classic gap (`docs/**`-only walk) — do NOT declare done until it
  is confirmed rewritten.

### Subtask T025 — Regenerate page-inventory + toc in place

- **Purpose**: FR-009/C-004 — the pinned generated nav artifacts reflect the new tree.
- **Steps**:
  1. `python -m scripts.docs.check_docs_freshness --inventory docs/development/3-2-page-inventory.yaml` —
     regenerate the page-inventory lockfile CONTENTS in place (path pinned by `test_inventory_path_stable.py`).
  2. Regenerate any `docs/**/toc.yml` the moves affected (per the freshness tooling / DocFX nav) — contents in
     place, never relocated.
- **Files**: `docs/development/3-2-page-inventory.yaml` (+ affected `toc.yml` files — tool-driven, in place).
- **Validation**: `check_docs_freshness --ci` green (T026); the inventory path is unchanged (still at the
  pinned location).
- **Edge cases**: never move the pinned inventory/`toc.yml` — regenerate contents only (C-004).

### Subtask T026 — Aggregate gate sweep (mission Definition of Done)

- **Purpose**: NFR-001/002/004 + SC verification — prove the whole diff is green.
- **Steps** (run from repo root; obey quickstart's verify block):
  1. `python -m scripts.docs.relative_link_fixer --check` — NFR-001: 0 broken relative links + 0 baseline 404s.
  2. `python -m scripts.docs.redirect_stub_generator check-map --occurrence-map "$MAP"` — NFR-002: 1:1 coverage.
  3. `python -m scripts.docs.check_docs_freshness --ci` — NFR-004: inventory/toc fresh, no baseline 404.
  4. `python -m scripts.docs.docs_structural_lint` — SC-003/004/005: exit 0 (clean tree, 0 shadow basenames,
     full architecture/ index — proves WP03's index + WP04's folds are complete and the lint is satisfied).
  5. `pytest tests/docs/ -q` — the lint regression fixture + config-SSOT assert + `test_bulk_ref_rewrite` +
     `test_inventory_path_stable` all green.
  6. `pytest tests/architectural/test_no_legacy_terminology.py -q` — NFR-004 terminology guard (CI-only gate).
  7. ruff/mypy clean on the touched `scripts/docs/` modules.
- **Files**: none new (verification).
- **Validation**: every command green; record the results in the Activity Log as the DoD evidence. If the lint
  flags something, it is a REAL structural gap (missing index entry, an un-folded shadow, a mis-placed move) —
  fix the underlying content/move (coordinate with WP03/WP04 owners), do not weaken the lint.
- **Edge cases**: a red terminology guard on doctrine/prose is CI-only — run it locally before declaring done.
  If `check_docs_freshness --ci` fails on baseline 404, a redirect entry is missing — re-run T023's `check-map`.

## Test Strategy

- Verification-driven (this WP's product is a green aggregate). Mandatory green:
  `relative_link_fixer --check`, `redirect_stub_generator check-map`, `check_docs_freshness --ci`,
  `docs_structural_lint` (exit 0), `pytest tests/docs/`, the terminology guard.
- If T022 changes tool defaults, `tests/docs/test_bulk_ref_rewrite.py` must stay green (update it to assert the
  new non-foreign default).

## Risks & Mitigations

- **Silent foreign-default consumption** (C-007): mitigate by ALWAYS passing `--occurrence-map "$MAP"` + the
  T022 un-pin (grep-for-`01KW3SBK` proves it is gone).
- **Hand-editing the derived redirect-map** (D5): forbidden — always `regenerate-map`; `check-map` is the gate.
- **Missed non-docs referrer** (R6): `relative_link_fixer` won't see `paradigm.yaml` — T024 explicitly drives
  `bulk_ref_rewrite` + a grep confirmation.
- **Moving a pinned artifact** (C-004): regenerate `3-2-page-inventory.yaml`/`toc.yml` contents in place only.
- **Stale editable install**: run tools via `python -m scripts.docs.<tool>` from the repo root so working-tree
  edits take effect.

## Review Guidance (reviewer-renata / opus)

Verify: no live default binds `01KW3SBK` (grep both tools); every redirect/link invocation passed
`--occurrence-map "$MAP"`; `redirect_map.yaml` was REGENERATED (not hand-edited) and `check-map` is 1:1;
`relative_link_fixer --check` clean incl. the non-docs `paradigm.yaml` rewrite (grep the old audit path →
gone); `check_docs_freshness --ci` green; `docs_structural_lint` exits 0 (full architecture/ index, 0 shadow
basenames); pinned inventory/`toc.yml` regenerated in place (path unchanged); `pytest tests/docs/` + terminology
guard green; the tool-driven referrer leeway is within sanctioned scope (no hand-edited feature work outside
owned_files beyond the recorded paradigm.yaml line).

## Activity Log

> **CRITICAL**: entries in chronological order (oldest first, newest last). Append at the END.

- 2026-07-22T16:30:00Z – system – Prompt created.
</content>
