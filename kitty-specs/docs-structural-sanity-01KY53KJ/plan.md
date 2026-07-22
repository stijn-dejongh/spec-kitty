# Implementation Plan: Docs Structural Sanity & Concern Guard

**Branch**: `docs/common-docs-section-audit` | **Date**: 2026-07-22 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `kitty-specs/docs-structural-sanity-01KY53KJ/spec.md`

## Summary

Bring the `docs/` tree to a structurally-sane baseline by redistributing the misfiled subset the Common-Docs section audit found (concentrated in `architecture/`, plus a `plans/notes/` split-brain shadow tree and an incomplete section index), and replace the retired anti-sprawl ratchet with a durable guard: a documentation-standard **doctrine artifact** (the authoritative concern-bucket→canonical-section map) plus a `scripts/docs/` structural lint wired into the docs test surface. Every move carries its redirect-map, relative-link, page-inventory, and frontmatter obligations (Common-Docs ADR `2026-06-27-1`); nothing lands in `guides/` (FR-003 boundary). Change mode is `bulk_edit` — an `occurrence_map.yaml` classifies every cross-file referrer so no link is silently missed.

## Technical Context

**Language/Version**: Python 3.11+ (docs lint + doctrine artifact loading; matches repo baseline)
**Primary Dependencies**: existing `scripts/docs/` tooling (`redirect_map.yaml` + `redirect_stub_generator.py`, `relative_link_fixer.py`, `check_docs_freshness.py`, page-inventory lockfile), the doctrine tree (`src/doctrine/`), DocFX docsite (`toc.yml`), `ruamel.yaml`/`pyyaml` for frontmatter/lint parsing
**Storage**: files — Markdown docs, YAML doctrine artifacts, `redirect_map.yaml`, `3-2-page-inventory.yaml`
**Testing**: `pytest tests/docs/` (new lint unit tests + regression fixture), terminology guard (`tests/architectural/test_no_legacy_terminology.py`), `check_docs_freshness --ci`
**Target Platform**: Linux / CI (docs build + gates)
**Project Type**: single
**Performance Goals**: docs structural lint completes in < 5 s locally (NFR-003)
**Constraints**: no content into `docs/guides/` (C-001); path-pinned artifacts regenerated in place, never moved (C-004); redistribution targets limited to `engineering-notes/`, `operations/`, doctrine tree, or in-zone (C-002); doctrine artifact via canonical doctrine tree, not an ad-hoc page (C-005)
**Scale/Scope**: ~11 file moves (9 firm + 2 borderline) + 3 shadow-tree reconcile/deletes + 1 new lint module + 1–2 doctrine artifacts; ~25–30 referrer files to repoint (measured: `audits/`→11, `adr-connector`→6, `feature-detection`→5, `closeout`→4, `883-brief`→2)

## Charter Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.* Charter present (`.kittify/charter/charter.md`), context mode `bootstrap`.

| Principle | Verdict | Note |
|---|---|---|
| Canonical sources, never improvise | PASS | The documentation standard is authored as a doctrine artifact (directive + styleguide) via the doctrine tree — not an ad-hoc page (C-005, FR-006). |
| Unification not parity | PASS | The new lint is a single authoritative structural guard replacing the *retired* anti-sprawl ratchet — it does not resurrect the ratchet or chase a dead quirk. |
| ATDD-first / red-first | PASS | The lint ships with a regression fixture that reintroduces each of the 4 audit finding-classes (red) before the tree is proven green (NFR-003, SC-003). |
| Terminology adherence | PASS | Terminology guard is part of the aggregate gate sweep (NFR-004); prose moves scrub point-in-time residue. |
| Campsite cleaning | PASS | The mission *is* a campsite pass on the docs tree; the guard prevents re-accretion. |
| Tiered rigour (DDD) | PASS | The lint is enforcement tooling (glue-tier) with focused unit tests per check; moves are content ops with gate verification. |

No violations → Complexity Tracking omitted.

## Project Structure

### Documentation (this mission)

```
kitty-specs/docs-structural-sanity-01KY53KJ/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (docs-lint contract, doc-standard schema)
├── occurrence_map.yaml  # Bulk-edit classification (change_mode: bulk_edit)
└── tasks.md             # Phase 2 (/spec-kitty.tasks — NOT created here)
```

### Source Code / docs (repository root)

```
docs/
├── architecture/                  # FR-001/FR-004: point-in-time artifacts leave; index.md refreshed to full membership
│   ├── audits/                    #   → 7 dated forensic files move to plans/engineering-notes/
│   ├── 883-research-synthesis.md  #   → moves (self-declared point-in-time)
│   └── 883-mission-type-authority-brief.md  # → moves
├── plans/
│   ├── notes/                     # FR-003: 1.x shadow tree retired (3 drifted dups reconciled/deleted)
│   └── engineering-notes/         # destination for point-in-time artifacts (+ this mission's audit note)
├── migrations/                    # FR-005: closeout evidence relocates out
└── adr/3.x/2026-06-27-1-common-docs-reconciliation.md   # governing ADR

scripts/docs/
├── <new> docs_structural_lint.py  # FR-007: index-completeness · point-in-time placement · shadow-tree · frontmatter
├── redirect_map.yaml              # FR-009: one entry per moved/removed path
└── redirect_stub_generator.py, relative_link_fixer.py, check_docs_freshness.py  # existing, reused

src/doctrine/                      # FR-006: documentation-standard directive + styleguide (canonical home)

tests/docs/
└── <new> test_docs_structural_lint.py  # regression fixture (4 finding-classes) + clean-tree pass
```

**Structure Decision**: Single project. Content moves within `docs/`; the guard lives in `scripts/docs/` (its natural home, where the retired ratchet lived) with tests in `tests/docs/`; the standard is a doctrine artifact under `src/doctrine/`.

## Implementation Concern Map

> Concerns are NOT work packages. `/spec-kitty.tasks` translates these into WPs.

### IC-01 — Documentation standard as doctrine

- **Purpose**: Encode the concern-bucket→canonical-section map + frontmatter contract as an authoritative doctrine artifact, so placement is defined by doctrine rather than a retired CI ratchet. Satisfies #2302.
- **Relevant requirements**: FR-006; C-005.
- **Affected surfaces**: `src/doctrine/` (a `documentation-standard` directive + a concern-taxonomy styleguide); referenced from `docs/development/index.md`.
- **Sequencing/depends-on**: none (defines the model the other concerns conform to).
- **Risks**: choosing the right doctrine kinds (directive vs styleguide) and not duplicating existing doc-governance doctrine; must load cleanly via the doctrine loader.

### IC-02 — Structural docs lint + CI wiring

- **Purpose**: Mechanically enforce the standard — index completeness, no dated filenames outside `engineering-notes/` (with allowlist), no shared basename across roots, frontmatter contract — the durable successor to the retired ratchet.
- **Relevant requirements**: FR-007, FR-008; NFR-003, NFR-005, NFR-006.
- **Affected surfaces**: `scripts/docs/docs_structural_lint.py`, `tests/docs/test_docs_structural_lint.py`, docs CI job (assuming the anti-sprawl ratchet's vacated gate role).
- **Sequencing/depends-on**: consumes IC-01's taxonomy (can start against a stub, finalize after IC-01).
- **Risks**: false positives on legitimately-dated files (ADR-by-date) → needs an explicit allowlist; must not reintroduce the ratchet's over-strict behavior.

### IC-03 — Architecture point-in-time redistribution + index completeness

- **Purpose**: Move the 9 firm + 2 borderline point-in-time artifacts to `engineering-notes/` and refresh `architecture/index.md` to full membership.
- **Relevant requirements**: FR-001, FR-002, FR-004; SC-001, SC-005.
- **Affected surfaces**: `docs/architecture/{883-*.md, audits/*, assessments/*}`, `docs/architecture/index.md`, `docs/plans/engineering-notes/`, ~13+ referrers.
- **Sequencing/depends-on**: index refresh (FR-004) follows the moves; verified by IC-02's completeness check.
- **Risks**: referrers in end-user-reachable pages (repoint via redirect, never move to guides/); page-inventory/toc regeneration.

### IC-04 — Shadow-tree retirement

- **Purpose**: Reconcile the 3 `plans/notes/` drifted duplicates against their canonical twins (`architecture/`, `adr/3.x/`), preserve unique content, delete the shadows, repoint referrers, fix the `notes/` README.
- **Relevant requirements**: FR-003; NFR-005; SC-004.
- **Affected surfaces**: `docs/plans/notes/{feature-detection,gap-analysis-connector-installation-model,adr-connector-auth-binding-separation}.md` + README; canonical twins; ~12 referrers.
- **Sequencing/depends-on**: none; verified by IC-02's shadow-tree check.
- **Risks**: divergence (not pure duplication) — must merge unique content into the canonical copy before deleting, not blind-delete.

### IC-05 — Migrations closeout relocation

- **Purpose**: Move the dated mission-closeout evidence out of the operator-runbook zone to `engineering-notes/`, scrubbing point-in-time residue.
- **Relevant requirements**: FR-005; SC-001.
- **Affected surfaces**: `docs/migrations/teamspace-mission-state-920-closeout.md` → `engineering-notes/`; 4 referrers.
- **Sequencing/depends-on**: none.
- **Risks**: minimal; standard move + redirect.

### IC-06 — IA-mechanics & aggregate gate sweep

- **Purpose**: Cross-cutting: one redirect-map entry per moved/removed path, relative-link fix, page-inventory + `toc.yml` regeneration, and the aggregate gate verification (link integrity, freshness, terminology, tests/docs).
- **Relevant requirements**: FR-009; NFR-001, NFR-002, NFR-004.
- **Affected surfaces**: `scripts/docs/redirect_map.yaml`, `3-2-page-inventory.yaml`, `docs/**/toc.yml`, `redirect_baseline_urls.json`.
- **Sequencing/depends-on**: follows IC-03/IC-04/IC-05 (needs the final move set); the lint (IC-02) runs as part of the sweep.
- **Risks**: missing a redirect entry (NFR-002 1:1) — the `occurrence_map` is the checklist that prevents it.
