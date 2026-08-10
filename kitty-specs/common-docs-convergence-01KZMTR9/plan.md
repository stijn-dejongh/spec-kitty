# Implementation Plan: Common Docs Convergence

**Branch**: `docs/common-docs-cleanup` | **Date**: 2026-08-10 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `kitty-specs/common-docs-convergence-01KZMTR9/spec.md`

## Summary

Converge Spec Kitty's ~700-file docs corpus onto the repository's sanctioned Common Docs section set, driven by a bulk-edit move spine and the canonical `scripts/docs/` tooling, with audience metadata formalized first to ground rewrites. The work is decomposed so that two foundations (audience formalization; the occurrence-map/redirect tooling) land before any file moves; all shared manifests and `docs/plans/**` link-fixes are single-threaded through one nav/redirect-reconcile owner; content rewrites are bounded, fact-guarded, and split from mechanical moves; and new pre-merge gates (DocFX build, extended structural-lint, non-vacuous audience/link resolvers, occurrence-map grep gate) make the acceptance criteria verifiable on PR rather than at deploy.

## Technical Context

**Language/Version**: Python 3.11+ (gates/tests/tooling); Markdown + YAML (docs content); DocFX (published site)
**Primary Dependencies**: Existing only — `docfx`, `ruamel.yaml`, `pytest`, and the `scripts/docs/` tooling (`redirect_stub_generator.py`, `relative_link_fixer.py`, `related_validator.py`, `inventory_lockfile.py`, `_guards.py`, `build_cli_reference.py`). **No new runtime dependencies.**
**Storage**: N/A (filesystem; docs + committed manifests)
**Testing**: `pytest` (`tests/docs/`, `tests/architectural/`) + new gates: audience resolver (non-vacuous), extended structural-lint, occurrence-map⊆redirect-map + stale-path grep gate, charter authority-path resolution test; new **pre-merge DocFX build job** (GitHub Actions `pull_request`).
**Target Platform**: repository docs tree + published DocFX site (docs.spec-kitty.ai) + CI (GitHub Actions)
**Project Type**: single (repo tooling + docs content)
**Performance Goals**: structural-lint completes < 5s over the corpus (asset NFR-003 contract); PR gate set stays within existing docs-freshness budget
**Constraints**: DocFX build zero-error/zero-warning on PR; 0 dangling `related:`/`audience:` refs; all mission gates non-vacuous; shared manifests single-threaded; no new deps; charter authority paths preserved or updated in-commit
**Scale/Scope**: ~700 docs pages; ~149 redirect entries (cumulative spine); 5 root dirs + ~8 loose root files to retire/rehome; `development/` (22) + `guides/` (59) subdivision; 13 free-text `audience:` values to migrate; 3 dead authority paths to repair

## Charter Check

*GATE: charter present and activated. Re-checked after Phase 1.*

- **DIRECTIVE_042 Common Docs** — the mission's governing standard. ✅ aligned (this is convergence work).
- **DIRECTIVE_044 Canonical sources & unification** — FR-021 routes all moves through canonical `scripts/docs/` tooling; no improvised redirects. ✅
- **DIRECTIVE_035 Bulk-edit occurrence classification** — `change_mode: bulk_edit`; this mission authors its own `occurrence_map.yaml` (C-007). ✅
- **publication-authority styleguide (code is source of truth)** — FR-014/NFR-009 keep rewrites prose-only and fact-verified; behavior-doc pages regenerated from source. ✅
- **047-audience-oriented-writing** — US1 formalizes the audience field against the existing catalog. ✅
- **037 living-documentation-sync / delete-stale** — FR-024 migrations curation; retire-stale in FR-006. ✅
- **no-legacy-terminology** — NFR-004; reconcile the stale `plans/notes/` exemption before touching plans links. ✅
- **025 Boy-Scout / 024 locality-of-change** — bounded per-WP scope; shared surfaces single-threaded (C-011). ✅

No charter violations. Complexity Tracking not required.

## Project Structure

### Documentation (this mission)

```
kitty-specs/common-docs-convergence-01KZMTR9/
├── plan.md              # this file
├── spec.md              # revised post-squad
├── research.md          # Phase 0 — decisions (tooling model, audience, gates, supply-chain)
├── data-model.md        # Phase 1 — frontmatter schema, occurrence-map schema, sanctioned sets
├── quickstart.md        # Phase 1 — how to run the mission's gates locally
├── contracts/           # Phase 1 — audience-resolution, redirect-tooling, pre-merge-build, adversarial-evidence
├── occurrence_map.yaml  # bulk-edit spine (C-007) — drives the redirect/link tooling
├── reviews/             # post-spec-squad.md (+ post-plan-squad.md)
├── traces/              # tracer files (tooling-friction, approach, design-decisions)
└── tasks.md             # Phase 2 (/spec-kitty.tasks — NOT created here)
```

### Source Code (repository root)

```
docs/                         # the single documentation root (target of convergence)
├── index/ context/ architecture/ adr/ plans/ api/ configuration/
├── integrations/ security/ guides/ operations/ migrations/ changelog/   # 13 canonical
├── development/              # sanctioned content section (config how_to/reference_policy home)
├── assets/  templates/spec-kitty/                                        # sanctioned non-content
└── context/audience/{internal,external}/                                # persona catalog (SSOT)

scripts/docs/                 # canonical move/gate tooling (extended, not replaced)
├── redirect_stub_generator.py  relative_link_fixer.py  related_validator.py
├── inventory_lockfile.py  _guards.py  redirect_map.yaml  redirect_baseline_urls.json
├── build_cli_reference.py
└── (new) audience_resolver.py  # or extend related_validator; non-vacuous

packs/built-in/
├── styleguides/common-docs.styleguide.yaml   # structural_lint_config (extended: FR-023, FR-009 routing)
├── directives/042-common-docs.directive.yaml # canonize audience: (FR-002)
└── assets/docs_structural_lint.py            # extended checks (FR-023)

tests/docs/                   # audience resolver, extended lint, authority-path, grep-gate tests
.github/workflows/            # docs-freshness.yml (add audience --strict); NEW pre-merge docfx build job
```

**Structure Decision**: single-project repo. Docs content under `docs/`; gate/tooling code under `scripts/docs/` + `packs/built-in/` (doctrine); tests under `tests/docs/`; CI under `.github/workflows/`. No new top-level trees.

## Implementation Concern Map

> Concerns, not work packages. `/spec-kitty.tasks` translates these into WPs. The dependency
> notes below ARE load-bearing: they encode the post-spec architect lens's DAG (two foundations
> before any move; a single-threaded reconcile owner; rewrites split from moves; ADR polish as the
> only fully-parallel leaf).

### IC-01 — Audience metadata formalization *(foundation; gates rewrites)*
- **Purpose**: Make `audience:` a resolvable, canonized, tested link into the existing `docs/context/audience/` catalog.
- **Relevant requirements**: FR-001, FR-002, FR-003, FR-004; C-012; NFR-002(audience half), NFR-008.
- **Affected surfaces**: `docs/context/audience/**`, `packs/built-in/directives/042-common-docs.directive.yaml`, `packs/built-in/styleguides/common-docs.styleguide.yaml`, `packs/built-in/directives/047-audience-oriented-writing.directive.yaml`, new `tests/docs/test_audience_resolves.py` + resolver in `scripts/docs/`, the 13 pages with free-text `audience:`.
- **Sequencing/depends-on**: none. **Must precede IC-06 and IC-08.**
- **Risks**: audience resolver must be non-vacuous (`assert_examined_floor`); must NOT enter `frontmatter_required_fields`; coordinate #3024 (singular `audience/` ownership).

### IC-02 — Move spine & redirect tooling *(foundation; gates all moves)*
- **Purpose**: Author this mission's `occurrence_map.yaml` (cumulative spine) and wire the canonical tooling to it.
- **Relevant requirements**: FR-021, C-007, C-010; NFR-010.
- **Affected surfaces**: `kitty-specs/common-docs-convergence-01KZMTR9/occurrence_map.yaml`, `scripts/docs/redirect_stub_generator.py` (parameterize off the hardcoded closed-mission slug or pass `--occurrence-map`), `relative_link_fixer.py`, `redirect_map.yaml` (derived), `redirect_baseline_urls.json` (immutable input).
- **Sequencing/depends-on**: none. **Must precede IC-04, IC-05, IC-06, IC-07.**
- **Risks**: naive regen drops the prior closed mission's 149 entries → coverage regression (NFR-010); cross-mission single-writer ownership (#2358) must be reconciled; baseline is immutable.

### IC-03 — Verification gates *(enables safe movement)*
- **Purpose**: Make acceptance verifiable on PR: pre-merge DocFX build + redirect-coverage + seo_verify; extend structural-lint to mission invariants; occurrence-map⊆redirect-map + stale-path grep gate; authority-path resolution test.
- **Relevant requirements**: FR-017, FR-018, FR-023; NFR-001, NFR-003, NFR-005, NFR-010; FR-019(test half).
- **Affected surfaces**: `.github/workflows/` (new PR job), `packs/built-in/assets/docs_structural_lint.py` + `structural_lint_config`, `tests/docs/*`, `scripts/docs/`.
- **Sequencing/depends-on**: IC-01 (audience test), IC-02 (occurrence-map). Gates should exist before mass movement lands.
- **Risks**: extended lint must keep the current tree green (NFR-003 scoping); pre-merge build folds a slice of #3265 (advisory not blocking beyond build correctness).

### IC-04 — Single-root consolidation
- **Purpose**: Retire/rehome all documentation outside `docs/` to the sanctioned set.
- **Relevant requirements**: FR-005, FR-006; NFR-006; SC-002. Closes root `research/ examples/ contracts/*.md glossary/ media/` + loose files.
- **Affected surfaces**: repo root dirs/files; `docs/{context,integrations,api,assets}/`; `README.md` logo URL; `contracts/` split (fixtures stay).
- **Sequencing/depends-on**: IC-02, IC-03. Feeds IC-11 for manifest regen. **IC-04 rehome of `examples/`→guides precedes IC-06.**
- **Risks**: README absolute media URL; `contracts/fixtures/` is test data (C-002); research survivors NOT into `plans/` (C-001).

### IC-05 — Section canon & architecture collapse
- **Purpose**: Dissolve non-canonical/umbrella/placeholder sections; collapse the `architecture/` version shadow to one living design (closes #2215).
- **Relevant requirements**: FR-007, FR-008; NFR-007; SC-003. Folds #2215, partial #2227.
- **Affected surfaces**: `docs/{reference,doctrine,core-concepts,updates,output,release-goals,archive}/`, `docs/architecture/README-*.x.md`, `src/doctrine/templates/diagrams/README.md` (repoint anchors FIRST).
- **Sequencing/depends-on**: IC-02, IC-03. Feeds IC-09 (authority paths) + IC-11.
- **Risks**: shipped src/doctrine links to `README-2.x.md` anchors; charter authority paths reference `architecture/` (see IC-09).

### IC-06 — How-to audience routing, Divio typing & subdivision
- **Purpose**: Route how-tos by audience (contributor→`development/`, user→`guides/`), type every page, subdivide the flat sections (folds #3273 residual).
- **Relevant requirements**: FR-009, FR-010, FR-011; SC-007, SC-009.
- **Affected surfaces**: `docs/guides/**`, `docs/development/**`, `structural_lint_config.concern_bucket_to_section`/`guides_boundary`.
- **Sequencing/depends-on**: IC-01 (audience routing), IC-02, IC-04 (examples rehomed first). Feeds IC-11.
- **Risks**: double-move if Divio-split and subdivision aren't done as one pass; `CLAUDE.md`/`AGENTS.md` refs + `CONTRIBUTING.md` symlink target under `development/`.

### IC-07 — Naming & index normalization
- **Purpose**: One `index.md` per in-scope directory; kebab-case names.
- **Relevant requirements**: FR-012, FR-013; SC-004.
- **Affected surfaces**: corpus-wide in-scope dirs/files (incl. snake_case persona files being formalized).
- **Sequencing/depends-on**: IC-04, IC-05, IC-06 (run after structure settles, else renames get redone). Feeds IC-11.
- **Risks**: rename churn; must route through occurrence-map (IC-02) so links/redirects stay covered.

### IC-08 — Bounded, fact-safe content rewrites
- **Purpose**: Prose-only scanability rewrites on an enumerated per-WP page list, grounded by `audience:`.
- **Relevant requirements**: FR-014; NFR-009; SC-001(rewrite half). Behavior-doc pages regenerated from source.
- **Affected surfaces**: enumerated pages within IC-04..07's touched set; `scripts/docs/build_cli_reference.py` for regenerated pages.
- **Sequencing/depends-on**: IC-01 (audience) + the page's structural move complete. **Separate reviewable WPs from the mechanical moves.**
- **Risks**: fact drift (NFR-009 reviewer must cite code/test backing); unbounded scope (enumerated lists + per-WP ceiling).

### IC-09 — Governance paths & generated rollups
- **Purpose**: Repair all 3 dead charter authority paths; regenerate rollups in place.
- **Relevant requirements**: FR-019, FR-020; NFR-004; C-003, C-005.
- **Affected surfaces**: `.kittify/charter/{charter,governance}.yaml`, `docs/development/3-2-*.yaml` rollups (via `inventory_lockfile.py`), terminology-guard exemption list.
- **Sequencing/depends-on**: IC-05 (architecture moves change authority paths). Sequence rollup regen against the ~10 live missions that own them.
- **Risks**: cross-mission `owned_files` on the rollups (C-005); authority-path test must assert all paths resolve.

### IC-10 — ADR polish & migrations curation *(parallel-safe leaf)*
- **Purpose**: #2887 date-sequence + non-dated/redundant-`doc_status` ADR fixes; migrations delete-stale.
- **Relevant requirements**: FR-015, FR-024; closes #2887, reconcile #2227/#3227.
- **Affected surfaces**: `docs/adr/**`, `docs/migrations/**`.
- **Sequencing/depends-on**: none (independent). Safe to run in parallel with IC-01/IC-02.
- **Risks**: era `README.md`→`index.md` overlaps #2227 lint exclusion — reconcile or exclude.

### IC-11 — Nav/redirect reconcile owner *(single-threaded integration)*
- **Purpose**: The single owner of shared manifests and `docs/plans/**` link-fixes; regenerates the derived map + nav after each mover lands.
- **Relevant requirements**: FR-016, FR-020; C-011, C-009; NFR-010; SC-005, SC-010.
- **Affected surfaces**: `redirect_map.yaml`, `redirect_baseline_urls.json`(read-only), `docs/toc.yml`, `docs/docfx.json`, `docs/llms.txt`, per-section `toc.yml`, inventory lockfiles, inbound `related:` links under `docs/plans/**`.
- **Sequencing/depends-on**: consumes the occurrence-map intent from IC-04..07; runs as the serialization point (no two movers edit these concurrently).
- **Risks**: this is the contention chokepoint — `/spec-kitty.tasks` must assign these files to exactly one writer at a time.

**DAG summary**: `IC-01, IC-02, IC-10` start in parallel → `IC-03` (needs 01+02) → `IC-04` → `IC-05`, `IC-06` (06 needs 01+04) → `IC-07` → `IC-08` (per-page, needs 01 + that page moved) → `IC-09` (needs 05); **`IC-11` is the single-threaded serialization point every mover (04–07,09) feeds.** Only `IC-10` is a fully parallel leaf.
