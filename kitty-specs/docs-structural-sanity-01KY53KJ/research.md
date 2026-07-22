# Phase 0 Research — Docs Structural Sanity & Concern Guard

The finding set is settled by the Common-Docs section audit (`docs/plans/engineering-notes/common-docs-section-audit.md`, this branch); research here resolves the *how*, not the *what*.

## D1 — Documentation-standard as doctrine (FR-006, C-005)

- **Decision**: Author the standard as **two doctrine artifacts** in `src/doctrine/`: a **directive** (`documentation-placement`) carrying the authoritative rule ("every doc lives in the canonical section for its concern bucket; point-in-time → engineering-notes; ops-runbook → operations; contributor how-to → development, never guides; doctrine YAML → src/doctrine") and a **styleguide** carrying the concern-bucket→section table + the frontmatter contract (`type`/`doc_status`/`updated`).
- **Rationale**: The retired ratchet encoded structure as a CI script with no authoritative source; a directive is the canonical, loadable, activation-aware home (charter: canonical sources). Splitting the *rule* (directive) from the *reference table* (styleguide) matches existing doctrine kind usage and lets the lint cite the directive.
- **Alternatives**: (a) a single `docs/` page — rejected, not canonical/loadable (C-005); (b) reviving the ratchet's inline constants — rejected, that is the drift being retired (unification not parity).

## D2 — Docs structural lint (FR-007)

- **Decision**: A `scripts/docs/docs_structural_lint.py` module with four independent checks, each emitting structured violations and a nonzero exit on failure: (1) **index completeness** — every non-index file in a section is enumerated in that section's `index.md`; (2) **point-in-time placement** — filenames matching a dated pattern (`^\d{4}-\d{2}` etc.) or self-declaring "point-in-time"/"closeout" live only under `engineering-notes/`, honoring an explicit allowlist (ADR-by-date, changelog); (3) **shadow-tree** — no basename is shared across distinct doc roots; (4) **frontmatter contract** — every in-scope page carries `type`/`doc_status`/`updated`.
- **Rationale**: These four are exactly the finding-classes the audit surfaced and the ratchet never caught (it checked index *existence*, not completeness; nothing checked shadowing). Independent checks keep each testable in isolation (SC-003).
- **Alternatives**: extend the retired ratchet — rejected (it is being removed by PR #2855); a monolithic check — rejected (harder to test per-class).
- **Allowlist**: the point-in-time check needs an explicit allowlist so correctly-placed dated artifacts (ADRs named by date, `CHANGELOG`) don't force churn (spec edge case).

## D3 — Redistribution homes (FR-001/002/005, C-002)

- **Decision**: Per the audit + Common-Docs ADR (`2026-06-27-1`, D7 distil-then-retire → engineering-notes): the 9 firm architecture artifacts + the borderline assessment + the migrations closeout all go to `docs/plans/engineering-notes/` (the audits as a `architecture-audits/` subfolder). `operations/` receives nothing (it already absorbed #2851's runbooks).
- **Rationale**: engineering-notes is the canonical home for point-in-time/report content (D7); keeping the 7 audits grouped preserves their provenance.
- **Alternatives**: a mission-archive under `plans/` — rejected, engineering-notes is the established home and already indexes such content.

## D4 — Shadow-tree reconciliation (FR-003)

- **Decision**: **Fold-then-delete**: diff each `plans/notes/` shadow against its canonical twin, port any unique content into the canonical copy, then delete the shadow and repoint referrers to the canonical path (with a redirect stub for external URLs). Twins confirmed: `feature-detection.md`↔`architecture/`, `gap-analysis-connector-installation-model.md`↔`architecture/`, `adr-connector-auth-binding-separation.md`↔`adr/3.x/`.
- **Rationale**: blind-delete would lose the shadow's divergent content (spec edge case); the canonical twins are the ones referrers *should* resolve to.
- **Alternatives**: keep both + cross-link — rejected, that is the split-brain being eliminated (NFR-005).

## D5 — Move mechanics & gate obligations (FR-009, NFR-001/002/004)

- **Decision**: For every move: (1) `git mv`; (2) add one `redirect_map.yaml` entry (`old_path.html → new_path.html`) via `redirect_stub_generator`; (3) `relative_link_fixer` over referrers; (4) regenerate the page-inventory lockfile + `toc.yml` in place; (5) update `related:` frontmatter edges. Verify aggregate with `relative_link_fixer --check`, `check_docs_freshness --ci`, the terminology guard, and `tests/docs/`.
- **Rationale**: this is the canonical Common-Docs move contract (D4 redirects); the `occurrence_map` is the 1:1 checklist guaranteeing no path lacks a redirect (NFR-002).
- **Alternatives**: rely on redirects without rewriting in-repo links — rejected, in-repo relative links must resolve directly (NFR-001).
