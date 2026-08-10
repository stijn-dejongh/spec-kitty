# Mission Specification: Common Docs Convergence

**Mission Branch**: `docs/common-docs-cleanup`
**Created**: 2026-08-10
**Status**: Draft
**Input**: Documentation structural cleanup / Common Docs convergence. Establish audience-metadata grounding first, then rehome, restructure, normalize, and rewrite the docs corpus onto the Common Docs standard. Excludes the `docs/plans/` backlog (follow-on mission).

## Context

Spec Kitty's documentation has grown to ~700 Markdown files across flat mega-directories, plus several stray documentation directories at the repository root (`research/`, `examples/`, `contracts/`, `glossary/`, `media/`) and loose root files. Per-page frontmatter is already clean (the mechanical structural-lint gate is green), but readers on the published DocFX site and contributors cannot reliably find or trust the right page. The activated **Common Docs** doctrine (DIRECTIVE_042, `common-docs` styleguide, `common-docs-*` tactics) defines the target: one `docs/` root of 13 sections (index, context, architecture, adr, plans, api, configuration, integrations, security, guides, operations, migrations, changelog), `doc_status` frontmatter, `related:` cross-refs, ADRs under `adr/<era>/`, delete-stale curation.

This mission converges the corpus onto that standard **and** adds an `audience:` frontmatter dimension (per the activated `047-audience-oriented-writing` directive and `writing-audience-catalog` tactic) so page rewrites are grounded in a named reader. The `docs/plans/` distil-and-retire triage is deliberately **out of scope** — it is a larger, higher-judgment effort spun out as a follow-on mission. All cleanup missions run in sequence on `docs/common-docs-cleanup`; a single upstream pull request is opened only after the sequence completes.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Audience-grounded documentation metadata (Priority: P1)

A writer (human or Comms Cleo) opening any documentation page can see, in the frontmatter, exactly which reader the page is written for, and that declaration resolves to a shared, central audience profile describing that reader's motivations, prior knowledge, and desired tone/depth.

**Why this priority**: This is the foundation the rest of the mission builds on. Grounding every rewrite in a named audience is what makes the subsequent restructuring and rewriting raise scanability and quality rather than just move files. It must land first so later work packages can consume it.

**Independent Test**: Create the central profile set under `docs/context/audiences/`, add the `audience:` field to a sample of pages, and run the new resolution test — it passes when every `audience:` reference resolves and fails when one is dangling. Delivers value on its own: an audience catalog + a governed, tested metadata field.

**Acceptance Scenarios**:

1. **Given** the built-in audience baseline in `packs/built-in/assets/audiences/`, **When** the mission completes WP-0, **Then** an equivalent central profile set exists under `docs/context/audiences/` as Common Docs pages (frontmatter, `doc_status`, kebab-case, an `index.md`).
2. **Given** a documentation page that declares `audience: <path>`, **When** the docs-consistency test runs, **Then** it passes only if `<path>` resolves to an existing profile page, and fails otherwise.
3. **Given** a page with no obvious reader, **When** a writer authors it, **Then** the `audience:` field lets them cite an existing profile rather than write for an undefined reader.

---

### User Story 2 - All documentation lives under one root (Priority: P1)

A contributor looking for a piece of documentation finds it under the single `docs/` root, never scattered at the repository root.

**Why this priority**: The single-root violation is the most disorienting structural defect and is invisible to the docs-rooted lint. Consolidating it delivers immediate discoverability value and is largely low-risk (much of the root clutter has zero inbound links).

**Independent Test**: Enumerate documentation-bearing files outside `docs/`; the story is met when only the sanctioned root allowlist remains, every rehomed page resolves, and the site still builds.

**Acceptance Scenarios**:

1. **Given** the root dirs `research/`, `examples/`, `glossary/` and loose root doc files, **When** the mission completes, **Then** each is either retired (stale, zero-inbound) or rehomed into the correct `docs/` section, with a redirect stub where an inbound link requires one.
2. **Given** `media/` is moved to `docs/assets/`, **When** the README renders on GitHub and PyPI, **Then** the logo still displays (the absolute raw URL is updated in the same change).
3. **Given** `contracts/`, **When** the mission completes, **Then** `batch-api-contract.md` is rehomed to `docs/api/` while `contracts/fixtures/*.json` (test data) is left untouched.

---

### User Story 3 - Only the canonical sections exist (Priority: P2)

A reader browsing the docs sees exactly the 13 canonical Common Docs sections — no non-canonical umbrella directories, no per-version shadow trees, no empty placeholder sections.

**Why this priority**: Non-canonical and umbrella sections (`reference/`, `doctrine/`, `core-concepts/`, `updates/`, `output/`, `release-goals/`) and the `architecture/` version shadow (`README-1.x/2.x/3.x`) fragment discoverability. High value, but riskier than US2 because it moves link-heavy, nav-registered content.

**Independent Test**: Enumerate top-level `docs/` section directories; the story is met when only the 13 canonical sections (plus sanctioned nav/theme assets) remain and no content basename is duplicated across section subtrees.

**Acceptance Scenarios**:

1. **Given** `reference/` duplicates `api/`, **When** the mission completes, **Then** its real content (`skills/`, `agent_profiles/`) is folded under `api/` and "Reference" survives only as a navigation zone.
2. **Given** `architecture/README-1.x/2.x/3.x.md`, **When** the mission completes, **Then** version history is distilled into `adr/<era>/` and `architecture/` presents a single living design, with the shipped `src/doctrine` diagram links repointed first.
3. **Given** index-only or empty placeholder sections, **When** the mission completes, **Then** they are dissolved into navigation zones or retired, and the DocFX nav is updated in lockstep.

---

### User Story 4 - Each guide declares and fits one Divio type (Priority: P2)

A reader in `guides/` can tell a learning tutorial from a task how-to by where it lives, and every guide page declares its Divio type.

**Why this priority**: `guides/` (the largest how-to surface) mixes tutorials and how-tos flat behind multiple index files, with a third of pages untyped. Clarifying it materially improves the most-used reader surface.

**Independent Test**: Check that every `guides/**` page carries a `type:`; tutorials live under a tutorials location and how-tos under a how-to location; a single index per grouping.

**Acceptance Scenarios**:

1. **Given** tutorials intermixed with how-tos, **When** the mission completes, **Then** tutorials are separated from how-tos and the three competing index files are collapsed into one per grouping.
2. **Given** guide pages lacking a Divio `type:`, **When** the mission completes, **Then** every in-scope guide page declares exactly one Divio type.

---

### User Story 5 - Pages are consistently named, indexed, and rewritten for scanability (Priority: P2)

A reader lands on any section or content subdirectory and finds a single landing page, consistent kebab-case names, and page bodies written to be scanned — grounded in the page's declared audience.

**Why this priority**: Naming inconsistency (README-vs-index ambiguity, non-kebab names) and dense prose reduce scanability across the corpus. The rewrite dimension is where the Common Docs quality goal is actually realized, page by page, for the pages this mission touches.

**Independent Test**: Every in-scope section/subdirectory has exactly one `index.md`; in-scope names are lowercase kebab-case; touched pages carry a resolvable `audience:` and a scanability pass (headings, lead summary, tables/lists over walls of prose).

**Acceptance Scenarios**:

1. **Given** directories that use `README.md` as a landing page or lack any index, **When** the mission completes, **Then** each in-scope directory presents a single `index.md` landing page.
2. **Given** non-kebab-case file and directory names in scope, **When** the mission completes, **Then** they are renamed to lowercase kebab-case and every reference to them is updated in the same change.
3. **Given** a page this mission moves or restructures, **When** it is finalized, **Then** its body is rewritten for scanability grounded in its declared `audience:`, without changing the underlying facts.

---

### User Story 6 - ADR corpus polished (Priority: P3)

A reader of the (already largely compliant) ADR corpus sees consistent era filing, dated filenames, and no redundant lifecycle keys.

**Why this priority**: The ADR corpus is essentially compliant; this is low-value polish, sequenced last and independent.

**Independent Test**: The handful of flagged ADRs carry dated filename prefixes, use only MADR `status` (no redundant `doc_status`), and era indexes use `index.md`.

**Acceptance Scenarios**:

1. **Given** two 3.x ADRs with non-dated filenames and redundant `doc_status`, **When** the mission completes, **Then** they carry dated prefixes and only the MADR `status` key.
2. **Given** ADR era directories using `README.md`, **When** the mission completes, **Then** they use `index.md` (with references updated).

---

### Edge Cases

- A file that looks like documentation but is read by code, tests, or CI (e.g. `contracts/fixtures/*.json`, the generated page-inventory/retrieval-index rollups, charter authority-path targets) — it must be preserved in place or repointed in the same change, never blindly moved.
- An inbound `related:` link that lives in an out-of-scope area (`docs/plans/**`) but points at a page this mission moves — the link target must still be fixed even though the plans page is otherwise untouched.
- A page whose only reasonable audience is not in the baseline catalog — a new profile is authored from the persona template, or an existing profile is cited; the page is never left with an undefined reader.
- A redirect stub is required when an external or shipped link cannot be updated (e.g. absolute or third-party references) — leave a stub rather than break the link.
- The DocFX theme (`templates/spec-kitty/`) resembles a docs directory but is site machinery — it must not be treated as content.

## Requirements *(mandatory)*

### Functional Requirements

| ID | Title | User Story | Priority | Status |
|----|-------|------------|----------|--------|
| FR-001 | Central audience profile set | As a writer, I want a central set of audience/stakeholder profiles under `docs/context/audiences/` (copied from the built-in baseline, one page per persona plus an index) so that pages can cite a shared reader definition. | High | Open |
| FR-002 | `audience:` frontmatter field | As a writer, I want an `audience:` frontmatter field expressed as resolvable repo-relative `.md` path(s) (same convention as `related:`) so a page names its intended reader, documented in the Common Docs convention. | High | Open |
| FR-003 | Audience-resolution test | As a maintainer, I want a docs-consistency test that fails when any `audience:` reference does not resolve to an existing profile page, so the field cannot silently rot. | High | Open |
| FR-004 | Single documentation root | As a contributor, I want no documentation files outside `docs/` except a named sanctioned root allowlist, so all docs are discoverable in one place. | High | Open |
| FR-005 | Rehome/retire root clutter | As a contributor, I want the root `research/`, `examples/`, `contracts/*.md`, `glossary/`, `media/`, and loose root doc files rehomed into the correct `docs/` section or retired per the delete-stale policy. | High | Open |
| FR-006 | Canonical sections only | As a reader, I want only the 13 canonical sections under `docs/` — non-canonical umbrella and empty placeholder sections dissolved or folded. | Medium | Open |
| FR-007 | Single living architecture | As a reader, I want `architecture/` to hold one unversioned living design with version history moved to `adr/<era>/`, eliminating the per-version README shadow tree. | Medium | Open |
| FR-008 | Divio-typed guides | As a reader, I want every `guides/` page to declare exactly one Divio type, with tutorials separated from how-tos and one index per grouping. | Medium | Open |
| FR-009 | One landing page per directory | As a reader, I want each in-scope section and content subdirectory to present a single `index.md` landing page (no README/index ambiguity). | Medium | Open |
| FR-010 | Kebab-case naming | As a contributor, I want in-scope documentation file and directory names in lowercase kebab-case (one concern per file), with references updated in the same change. | Medium | Open |
| FR-011 | Audience-grounded rewrites | As a reader, I want pages this mission moves or restructures rewritten for scanability, grounded in the page's declared `audience:`, without altering the underlying facts. | Medium | Open |
| FR-012 | ADR polish | As a reader, I want the flagged ADRs to use dated filenames and only the MADR `status` key, and era indexes to use `index.md`. | Low | Open |
| FR-013 | Cross-reference integrity | As a reader, I want every `related:` and `audience:` cross-reference to resolve after restructuring, with link targets updated in the same change as each move. | High | Open |
| FR-014 | Navigation lockstep | As a site visitor, I want the DocFX navigation (`toc.yml`, `docfx.json`, `llms.txt`, per-section toc) updated in lockstep with every move so the published site does not break. | High | Open |
| FR-015 | Code/test/CI reference updates | As a maintainer, I want every code, test, and CI reference to a moved documentation path updated in the same change, so nothing that reads a doc path breaks. | High | Open |
| FR-016 | Governance path integrity | As a governance owner, I want charter authority paths preserved, or updated in the same change, and the dead `glossary/contexts/` authority path repaired. | High | Open |
| FR-017 | Regenerate rollups | As a maintainer, I want the page-inventory and docs-retrieval-index rollups regenerated from frontmatter after changes, kept in place (not relocated). | Medium | Open |

### Non-Functional Requirements

| ID | Title | Requirement | Category | Priority | Status |
|----|-------|-------------|----------|----------|--------|
| NFR-001 | Site builds clean | The published documentation site builds with zero errors after the mission (DocFX build gate green). | Reliability | High | Open |
| NFR-002 | Zero dangling references | 100% of `related:` and `audience:` references resolve to existing files; 0 dangling links across `docs/`. | Correctness | High | Open |
| NFR-003 | Structural lint green | The `common-docs-structural-lint` asset reports 0 violations with `checked` equal to the in-tree page count after the mission. | Correctness | High | Open |
| NFR-004 | Terminology guard green | The terminology-guard suite reports 0 forbidden-term regressions introduced by the mission. | Correctness | High | Open |
| NFR-005 | Touched references green | Every test that exercises a moved/renamed documentation path passes; 0 failures attributable to the mission's changes. | Reliability | High | Open |
| NFR-006 | Single-root measurable | 0 documentation files reside outside `docs/` except the enumerated sanctioned root allowlist. | Maintainability | High | Open |
| NFR-007 | Canonical section count | The top level of `docs/` contains only the 13 canonical section directories plus sanctioned nav/theme asset directories; 0 non-canonical content sections remain. | Maintainability | Medium | Open |
| NFR-008 | Frontmatter completeness | 100% of in-scope content pages carry the required Common Docs frontmatter, including a resolvable `audience:` on every page this mission touches. | Correctness | Medium | Open |

### Constraints

| ID | Title | Constraint | Category | Priority | Status |
|----|-------|------------|----------|----------|--------|
| C-001 | Plans backlog out of scope | No distil/retire/restructure of `docs/plans/**` content; only mechanical link-target fixes required by moves elsewhere are permitted there. | Scope | High | Open |
| C-002 | Test data is not docs | `contracts/fixtures/*.json` is test data read by the suite and MUST NOT be moved into `docs/`. | Technical | High | Open |
| C-003 | Authority paths protected | `docs/context/` and `docs/adr/3.x/` are charter authority paths; do not relocate them unless charter and governance config are updated in the same change. | Governance | High | Open |
| C-004 | Preserve DocFX theme | `docs/templates/spec-kitty/` is the site theme, not content, and MUST be preserved. | Technical | High | Open |
| C-005 | Rollups regenerate in place | The page-inventory and retrieval-index rollups are owned by live missions; regenerate them in place, do not relocate. | Technical | Medium | Open |
| C-006 | Common Docs canon | Exactly one `docs/` root and only the 13 canonical sections; a 14th section or a second documentation root is a red-line violation. | Governance | High | Open |
| C-007 | Bulk-edit discipline | Same-path/link renames across files follow DIRECTIVE_035 occurrence-classification (an `occurrence_map.yaml` is produced at plan time). | Process | High | Open |
| C-008 | No version numbers | No release/version numbers are assigned by this mission; the release boundary belongs to the product owner. | Business | Medium | Open |
| C-009 | Sequenced, single PR | All cleanup missions run in sequence on `docs/common-docs-cleanup`; a single upstream pull request is opened only after the sequence completes. | Process | Medium | Open |

### Key Entities

- **Documentation page**: a Markdown file under `docs/` with Common Docs frontmatter (`title`, `doc_status`, `updated`, `description`, `type`, `related`, and the new `audience`).
- **Audience/stakeholder profile**: a persona page under `docs/context/audiences/` describing a reader's motivations, prior knowledge, and desired tone/depth; the resolution target of the `audience:` field.
- **Common Docs section**: one of the 13 canonical top-level directories, each with an `index.md`.
- **ADR**: an era-filed decision record under `adr/<era>/` using the MADR `status` key.
- **Navigation manifest**: the DocFX surface (`toc.yml`, `docfx.json`, `llms.txt`, per-section toc) that enumerates and orders pages for the published site.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of pages this mission touches declare a resolvable `audience:`, and the central audience profile set resolves without dangling references.
- **SC-002**: 0 documentation files live outside the single `docs/` root except the named sanctioned root allowlist.
- **SC-003**: The `docs/` tree contains only the 13 canonical sections; 0 non-canonical, umbrella, empty-placeholder, or shadow sections remain.
- **SC-004**: Every in-scope section and content subdirectory presents exactly one `index.md` landing page.
- **SC-005**: 0 broken internal documentation links after restructuring (all `related:`/`audience:` references resolve).
- **SC-006**: The published documentation site builds successfully and all pre-existing docs gates (structural-lint, freshness, terminology guard) remain green.
- **SC-007**: Every in-scope `guides/` page is exactly one Divio type, and a reader can distinguish tutorials from how-tos by location.
- **SC-008**: `docs/plans/` content is unchanged except for link-target fixes required by moves elsewhere (scope boundary respected).

## Assumptions

- The built-in audience baseline (`packs/built-in/assets/audiences/`, 5 personas) and `src/doctrine/templates/architecture/stakeholder-persona-template.md` are the copy-source for the central profile set; org-specific persona content is not required for this mission.
- The Common Docs doctrine is already activated in the charter (verified); no charter activation work is required, only same-change updates to authority-path targets if any protected path is touched.
- "Sanctioned root allowlist" covers at least: `README.md`, `LICENSE`, `CHANGELOG.md` (symlink), `CONTRIBUTING.md` (symlink), `CLAUDE.md`/`AGENTS.md`, `CODE_OF_CONDUCT.md`, `SECURITY-POSITION.md`, `CONTRIBUTORS.md`, `RELEASE_CHECKLIST.md`; the exact list is finalized at plan time.
- The follow-on `docs/plans/` triage mission and any full-corpus `audience:` backfill beyond touched pages are separate missions.
