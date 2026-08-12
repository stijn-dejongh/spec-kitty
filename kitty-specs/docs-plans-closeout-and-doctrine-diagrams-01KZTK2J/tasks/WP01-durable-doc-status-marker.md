---
work_package_id: WP01
title: Durable doc_status marker + validator propagation (IC-01 foundation)
dependencies: []
requirement_refs:
- C-004
- FR-002
- NFR-001
planning_base_branch: feat/docs-plans-tier3-closeout
merge_target_branch: feat/docs-plans-tier3-closeout
branch_strategy: Planning artifacts for this mission were generated on feat/docs-plans-tier3-closeout. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/docs-plans-tier3-closeout unless the human explicitly redirects the landing branch.
subtasks:
- T001
- T002
- T003
- T004
- T005
- T006
history:
- at: '2026-08-12'
  note: Authored by /spec-kitty.tasks (post-plan-squad model). IC-01 predecessor of IC-02/IC-03/IC-04.
agent_profile: python-pedro
authoritative_surface: packs/built-in/directives/042-common-docs.directive.yaml
create_intent:
- tests/docs/test_doc_status_durable.py
execution_mode: code_change
owned_files:
- packs/built-in/directives/042-common-docs.directive.yaml
- scripts/docs/frontmatter_backfill.py
- packs/built-in/styleguides/common-docs.styleguide.yaml
- packs/built-in/styleguides/docs-freshness-sla.styleguide.yaml
- tests/docs/test_doc_status_durable.py
role: implementer
tags: []
tracker_refs: []
---

## ⚡ Do This First: Load Agent Profile

Before reading anything else, load your assigned profile:

```
/ad-hoc-profile-load python-pedro
```

Apply its initialization, boundaries, directives, and tactics. Then read this WP, `spec.md` (FR-002, NFR-001, C-004), `plan.md` (IC-01), `research.md` (D1), and `contracts/doc-status-durable.md` (the authority chain).

## Objective

Add `durable` as a **reserved, never-retire** value to the `doc_status` documentation-lifecycle vocabulary, propagated across the full authority chain so a domain-plan throughline marked `doc_status: durable` is accepted at every enumerated validation site and never flagged point-in-time / stale. **This is the foundation WP — IC-02, IC-03, and IC-04 all depend on it** (any doc written with `doc_status: durable` fails validation until this lands).

## Context

- **The `doc_status` vocabulary is prose/enum-declared, not structurally schema-encoded.** There is no closed-set validator that rejects an unlisted value today (the styleguide even notes vocabulary enforcement is deferred). So the executable gates that could *misclassify* `durable` are: (a) the structural lint's `point_in_time_placement` — `durable` must NOT be in `point_in_time_markers`; (b) the structural lint's `frontmatter_contract` — a `durable` page still carries `doc_status` + `updated`; (c) the `DocStatus` StrEnum. `scripts/docs/check_docs_freshness.py` is a **lockfile-drift** gate (regenerate-from-frontmatter), NOT a `doc_status`-threshold gate, so it does not flag durable pages — do not invent a staleness threshold there.
- **Authority order matters (C-004):** directive `042-common-docs` is the authoritative vocabulary; the `DocStatus` enum **mirrors** it. Edit the directive first, then the enum, or you introduce doctrine/code drift.
- **`closeout` is NOT a `doc_status` value** — it is a point-in-time-marker / archive-directory convention that maps to `deprecated`. It already appears in `point_in_time_markers`. Do not touch that; do not add `durable` beside it.
- **ATDD-first (C-011):** the "durable accepted everywhere" test lands **red-first** as a separate first commit, RED on `feat/docs-plans-tier3-closeout` before any propagation edit, GREEN on the final commit.

### Subtask T001 — Red-first ATDD test: `tests/docs/test_doc_status_durable.py`

**Purpose**: Pin the user-observable contract before implementing it. Commit this test FIRST (separate commit); it must be RED on the planning base.

**Steps**:
1. Create `tests/docs/test_doc_status_durable.py` with the neighbour marker convention `pytestmark = pytest.mark.architectural` (matches `tests/docs/test_docs_structural_lint.py`, `test_frontmatter_backfill.py`, `test_related_validator.py`). Reuse their fixture harness: the lint asset is loaded via `importlib` from `packs/built-in/assets/docs_structural_lint.py` and configured with `load_config(STYLEGUIDE_PATH)`; the `_write(...)` helper builds a synthetic page — mirror it rather than re-inventing.
2. Assert the four propagation guarantees (contract §Guarantees):
   - **Directive authority**: parse `packs/built-in/directives/042-common-docs.directive.yaml` and assert its `doc_status` vocabulary line lists `durable`.
   - **Enum mirror**: `from scripts.docs.frontmatter_backfill import DocStatus` and assert `DocStatus.DURABLE.value == "durable"` and `"durable" in {s.value for s in DocStatus}`.
   - **Structural-lint acceptance**: build a synthetic `durable` page (frontmatter `doc_status: durable`, `updated: <date>`) placed OUTSIDE `plans/` (e.g. a temp `docs/architecture/foo.md`-shaped fixture) and run it through the structural lint (`packs/built-in/assets/docs_structural_lint.py` — mirror the fixture harness in `tests/docs/test_docs_structural_lint.py`); assert `point_in_time_placement` does **NOT** flag it and `frontmatter_contract` passes.
   - **Never point-in-time**: assert `durable` is NOT among the styleguide's `structural_lint_config.point_in_time_markers` values.
3. Run it and confirm RED (imports/values missing). Commit as the first WP commit.

**Files**: `tests/docs/test_doc_status_durable.py` (new, ~90 lines).

### Subtask T002 — Edit the AUTHORITY: directive 042 vocabulary

**Purpose**: Add `durable` to the authoritative closed vocabulary FIRST.

**Steps**:
1. In `packs/built-in/directives/042-common-docs.directive.yaml`, the doc_status vocabulary is stated at the `doc_status` bullet (currently `draft / active / deprecated / superseded`). Add `durable` to that vocabulary list, with a short reserved-never-retire gloss.
2. **Do NOT** touch the MADR `status` lines (Proposed / Accepted / Deprecated / Superseded) — those are the ADR decision-status exception, a different vocabulary.
3. If the directive restates the vocabulary elsewhere (integrity_rules / validation_criteria), keep them consistent — grep for `draft / active` to find every restatement.

**Files**: `packs/built-in/directives/042-common-docs.directive.yaml`.

### Subtask T003 — Mirror in the `DocStatus` enum

**Purpose**: Keep the code enum in lockstep with the directive.

**Steps**:
1. In `scripts/docs/frontmatter_backfill.py`, add `DURABLE = "durable"` to `class DocStatus(StrEnum)` (after `SUPERSEDED`), with a one-line docstring/comment noting it is the reserved never-retire member mirroring directive 042.
2. Do NOT add `durable` to `TAG_DOC_STATUS` or `derive_doc_status` — no version tag derives to durable; it is authored by hand on throughlines only.

**Files**: `scripts/docs/frontmatter_backfill.py`.

### Subtask T004 — Styleguide vocabulary prose + `durable ∉ point_in_time_markers`

**Purpose**: Reconcile the styleguide's prose vocabulary and prove durable is never point-in-time.

**Steps**:
1. In `packs/built-in/styleguides/common-docs.styleguide.yaml`, update the controlled-vocabulary prose (the `doc_status` line currently reading `draft | active | deprecated | superseded`) to include `durable` with the reserved-never-retire gloss.
2. **Leave `structural_lint_config.point_in_time_markers` unchanged** — it must continue to list only `point_in_time` and `closeout`. `durable` must NOT appear there (it is the semantic opposite). The T001 test asserts this.

**Files**: `packs/built-in/styleguides/common-docs.styleguide.yaml`.

### Subtask T005 — Freshness-SLA styleguide: durable is never-stale

**Purpose**: Record the durable-is-never-stale policy in the freshness doctrine.

**Steps**:
1. In `packs/built-in/styleguides/docs-freshness-sla.styleguide.yaml`, add a prose rule (near the deprecation/retirement rule) stating that `doc_status: durable` pages are throughlines exempt from the staleness sweep — they are re-verified on domain change, not aged out.
2. This is a **prose/policy** edit (there is no executable staleness-threshold gate keyed on doc_status today); do not fabricate one.

**Files**: `packs/built-in/styleguides/docs-freshness-sla.styleguide.yaml`.

### Subtask T006 — Turn the suite green + confirm no regressions

**Purpose**: Prove red→green and zero collateral breakage.

**Steps**:
1. Run `PWHEADLESS=1 python -m pytest tests/docs/ tests/doctrine/test_schema_generation_integrity.py -q` — the new durable test is GREEN; `test_docs_structural_lint.py` (esp. the `point_in_time_markers` round-trip assertion) and `test_frontmatter_backfill.py` still pass.
2. Run `pytest tests/architectural/test_no_legacy_terminology.py -q` and `python scripts/docs/check_docs_freshness.py` (0 errors).
3. Record the red→green evidence (base SHA red, final SHA green) in the activity log.

**Files**: none beyond the above.

## Branch Strategy

Planning/base branch: `feat/docs-plans-tier3-closeout`. Final merge target: `feat/docs-plans-tier3-closeout`. Execution worktrees are allocated per computed lane from `lanes.json`.

## Definition of Done

- `tests/docs/test_doc_status_durable.py` was RED on the planning base and is GREEN on the final commit (red→green evidence recorded).
- `durable` is present in: directive 042 vocabulary, `DocStatus` enum, common-docs styleguide vocabulary prose, docs-freshness-sla prose.
- `durable` is **absent** from `point_in_time_markers`; `closeout` is **not** added to the enum.
- `tests/docs/` + `tests/doctrine/test_schema_generation_integrity.py` + `tests/architectural/test_no_legacy_terminology.py` green; `check_docs_freshness.py` 0 errors.
- ruff + mypy clean on `scripts/docs/frontmatter_backfill.py` and the new test (zero suppressions).

## Reviewer guidance

- Verify the directive was edited **before/with** the enum (authority-first) and the two agree (SC-004).
- Verify the ATDD test genuinely exercises the structural lint (not a tautology asserting a constant) and was red on the base.
- Confirm no MADR `status` line was altered and `closeout` was not added to the enum.
- Confirm `point_in_time_markers` is byte-for-byte unchanged.
