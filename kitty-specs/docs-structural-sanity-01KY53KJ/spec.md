# Mission Specification: Docs Structural Sanity & Concern Guard

**Mission Branch**: `docs/common-docs-section-audit`
**Created**: 2026-07-22
**Status**: Draft
**Input**: Address all findings of the Common-Docs section audit (`docs/plans/engineering-notes/common-docs-section-audit.md`) and add a durable guard so `docs/` stays structurally sane.

## Context

Issue #2851 hand-cleaned `docs/development/` by concern and, in the same change (PR #2855, commit `758c2bd45`), **retired the anti-sprawl ratchet** (`scripts/docs/anti_sprawl_ratchet.py`) — the only mechanical guard for canonical sections and required indexes. A docs-wide concern audit (this branch's engineering note) then classified every remaining `docs/` section by concern bucket — (a) contributor how-to · (b) reference/policy · (c) point-in-time report · (d) generated/nav/tooling · (e) doctrine artifact — and found the accretion concentrated in `architecture/`, plus a split-brain shadow tree and an incomplete section index. This mission redistributes the misfiled subset to its canonical concern-home **and** replaces the retired ratchet with a live lint that is wired back into the **existing** documentation doctrine — DIRECTIVE_042 "Common Docs Documentation Standard" already binds the single root, 13-section structure, `doc_status` frontmatter, `related:` validity, and the no-shadow-tree red-line, but its `validation_criteria` NOTES the anti-sprawl ratchet was retired and wires **no** replacement gate. This mission **extends** DIRECTIVE_042 and the companion `common-docs` styleguide (it does **not** mint a new `documentation-placement` directive) with the finer concern-bucket→section map + a point-in-time allowlist, reconciles the 4 artifacts that still cite the dead ratchet as a live gate, and lands `scripts/docs/docs_structural_lint.py` as the ratchet's named successor. Parent epic: #2314 (bucket C — content sanitization; bucket E — docs governance as doctrine). Closes #2302.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Point-in-time architecture artifacts reach their concern-home (Priority: P1)

A maintainer opening `docs/architecture/` sees only living design (ADR-adjacent explanation), not dated one-shot mission dossiers and forensic audits. The audit's 9 firm misfiled files (`architecture/883-research-synthesis.md`, `architecture/883-mission-type-authority-brief.md`, and `architecture/audits/*` ×7) move to `docs/plans/engineering-notes/`, each with a redirect stub, fixed relative links, and refreshed `related:` frontmatter.

**Why this priority**: Largest single concentration of misfiling; the most visible inconsistency and the one that most degrades the "living design" section.

**Independent Test**: After this slice, `architecture/` contains no dated/point-in-time dossier; every moved URL resolves via a redirect; `relative_link_fixer --check` is clean. Delivers a coherent `architecture/` regardless of the other slices.

**Acceptance Scenarios**:

1. **Given** `architecture/883-research-synthesis.md` self-declaring "point-in-time … superseded by the ADR and brief", **When** the mission runs, **Then** it lives under `docs/plans/engineering-notes/`, its old path 301s to the new one, and no referrer link is broken.
2. **Given** the 7 `architecture/audits/*` dated forensic files, **When** moved, **Then** each has a redirect-map entry and the page-inventory + `toc.yml` are regenerated to reflect the new home.

---

### User Story 2 - A durable guard replaces the retired ratchet, wired into existing doctrine (Priority: P1)

A contributor adds a new doc; the **extended** DIRECTIVE_042 + `common-docs` styleguide tell them where each concern belongs, and a `scripts/docs/docs_structural_lint.py` lint (wired into CI) rejects a misfiling before it lands — the mechanical successor to the retired anti-sprawl ratchet, catching what it never did. The styleguide carries a machine-parseable config block that the lint LOADS (single source of truth), and the 4 artifacts that still name the dead "WP05 anti-sprawl structure ratchet" as a live gate are reconciled to cite the new lint.

**Why this priority**: Without this, every slice below is a one-time cleanup that re-accretes. This is the keystone that makes "structurally sane" durable; independently testable against a seeded fixture. It also closes the live gap in DIRECTIVE_042 (`validation_criteria` notes the ratchet is retired but wires no replacement) and clears the dangling-ratchet references so no artifact points at a deleted gate.

**Independent Test**: A regression fixture reintroducing each of the 4 audit finding-classes (misfiled point-in-time file, incomplete index for a curated-complete section, shadow-tree content-duplicate basename, missing frontmatter on an in-scope page) fails the lint; the **current** clean tree passes with zero violations. Deliverable on its own.

**Acceptance Scenarios**:

1. **Given** a dated `report-2026-05.md` placed outside `plans/**`, **When** the docs lint runs, **Then** it fails naming the canonical home; **and given** the current era-dated files under `adr/**` and `plans/{research,investigations}/**`, the lint passes them clean (allowlisted).
2. **Given** a section declared "curated-complete" in the styleguide config (initially `architecture/` only) whose `index.md` omits a sibling page, **When** the lint runs, **Then** it fails the index-completeness check; **and** a landing-page index for a non-curated section does not fail.
3. **Given** two files sharing a NON-NAV content basename across two section subtrees, **When** the lint runs, **Then** it fails the shadow-tree check; **and** shared nav basenames (`index.md`, `README.md`, `toc.yml`) and sanctioned era files (`README-N.x.md`, `00-SYNTHESIS.md`) do not.
4. **Given** the concern taxonomy + allowlist + frontmatter contract, **When** encoded by extending DIRECTIVE_042 and the `common-docs` styleguide config block (not an ad-hoc page, not a new directive), **Then** it loads through the canonical doctrine tree, the lint reads that config, and #2302 is satisfied.
5. **Given** the 4 artifacts that cite the retired ratchet (042 directive `validation_criteria`; styleguide `tooling`/`quality_test`; `common-docs-curation` + `common-docs-scaffold` tactics), **When** reconciled, **Then** each names `scripts/docs/docs_structural_lint.py` as the live successor gate and none references the deleted ratchet.

---

### User Story 3 - The split-brain shadow tree is retired (Priority: P2)

A maintainer editing connector/feature-detection docs has one canonical copy, not two drifted ones. The 3 `plans/notes/` files that are drifted near-duplicates of canonical copies in `architecture/`/`adr/3.x/` are reconciled, the stale shadows deleted, referrers repointed, and the `notes/` README corrected.

**Why this priority**: Correctness/safety — split-brain duplicates silently serve stale content; higher than cosmetic index work but smaller blast radius than US1.

**Independent Test**: After this slice, no basename is shared across doc roots (`plans/notes/` no longer shadows canonical copies); every referrer points at the surviving canonical file.

**Acceptance Scenarios**:

1. **Given** `plans/notes/feature-detection.md` (396 lines) drifted from the canonical `architecture/` copy (388 lines), **When** reconciled, **Then** one canonical file remains, the shadow is redirected/removed, and referrers resolve to the survivor.

---

### User Story 4 - The architecture section index is complete (Priority: P2)

A reader of `architecture/index.md` sees every page in the section, not 4 of ~60. The index is regenerated to enumerate the whole section (post-US1 membership).

**Why this priority**: Navigation completeness; depends on US1's final membership, so it sequences after the moves.

**Independent Test**: `architecture/index.md` lists 100% of the section's files; the new index-completeness lint passes for that section.

**Acceptance Scenarios**:

1. **Given** an `architecture/` file absent from `index.md`, **When** the index is refreshed, **Then** it appears, and the completeness lint is green.

---

### User Story 5 - Mission-closeout evidence leaves the runbook zone (Priority: P3)

An operator browsing `docs/migrations/` finds reusable runbooks, not a dated one-mission closeout record. `migrations/teamspace-mission-state-920-closeout.md` moves to the engineering-notes/mission-archive home, point-in-time residue scrubbed, redirect + links updated.

**Why this priority**: Smallest, most contained; low reader impact, so last.

**Independent Test**: `migrations/` contains only reusable runbooks; the closeout resolves at its new home via redirect.

**Acceptance Scenarios**:

1. **Given** the dated closeout in `migrations/`, **When** relocated, **Then** its old URL redirects and `migrations/` holds no point-in-time closeout.

### Edge Cases

- A flagged file is referenced by an *end-user* (`guides/`) page — the move must not create a contributor-only page reachable from end-user nav (guides-zone boundary); if such a referrer exists, the link is repointed to a redirect stub, never by moving content into `guides/`.
- A `plans/notes/` shadow has *diverged* from its canonical twin (not a pure duplicate) — reconciliation must preserve any unique content into the canonical copy before deleting the shadow, not blind-delete.
- A generated/path-pinned artifact (`3-2-page-inventory.yaml`, `toc.yml`) is touched by a move — regenerate its contents in place; never relocate the pinned file (`test_inventory_path_stable.py`).
- A moved file's new home collides with the in-flight `docs-ia-onboarding-overhaul` mission or #2227's architecture-residual scope — coordinate/defer rather than double-move.
- The docs lint would flag a legitimately-dated file that must stay put (e.g. an ADR named by date) — the standard must carve an explicit allowlist/pattern so the guard does not force churn on correctly-placed dated artifacts.

## Requirements *(mandatory)*

### Functional Requirements

| ID | Title | User Story | Priority | Status |
|----|-------|------------|----------|--------|
| FR-001 | Redistribute the 9 firm point-in-time `architecture/` artifacts (audits×7 + 883 research/brief) to `docs/plans/engineering-notes/`, with a redirect entry, fixed relative links, and refreshed `related:` frontmatter per file. | As a maintainer, I want living-design sections free of dated dossiers so `architecture/` reads as current design. | High | Open |
| FR-002 | Adjudicate the 2 borderline artifacts (`migrations/…-920-closeout.md`, `architecture/assessments/code-as-a-crime-scene-overview.md`): record a per-borderline verification result and **DEFAULT to "stays"** per the audit unless a file is verified point-in-time — only a verified point-in-time file moves (with the full move contract). Each decision is recorded (assessment + closeout note). | As a maintainer, I want borderline files decided by recorded evidence, defaulting to stays, not force-moved. | Medium | Open |
| FR-003 | Retire the `plans/notes/` 1.x shadow tree: reconcile the 3 drifted duplicates against their canonical copies (`architecture/` + `adr/3.x/`), preserve unique content, delete the shadows, repoint referrers, correct the `notes/` README. | As a maintainer, I want one canonical copy per doc so no stale shadow is served. | High | Open |
| FR-004 | Refresh `architecture/index.md` to enumerate every file in the section (completeness), matching the section-index convention. | As a reader, I want the section index to list every page. | Medium | Open |
| FR-005 | Relocate the `migrations/` mission-closeout evidence out of the runbook zone (to engineering-notes/mission-archive), scrubbing point-in-time residue, with redirect + links. | As an operator, I want `migrations/` to hold only reusable runbooks. | Low | Open |
| FR-006 | **Extend the existing documentation doctrine** — DIRECTIVE_042 "Common Docs Documentation Standard" + the companion `common-docs` styleguide — with the finer concern-bucket→canonical-section map, the point-in-time allowlist, and a machine-parseable config block (see FR-011). Do **not** mint a new `documentation-placement` directive. Additionally **reconcile the 4 dangling-ratchet artifacts** (042 directive `validation_criteria`; styleguide `tooling`+`quality_test`; the `common-docs-curation` + `common-docs-scaffold` tactics) so each cites `scripts/docs/docs_structural_lint.py` as the live successor gate, not the deleted "WP05 anti-sprawl structure ratchet". Satisfies #2302. | As a contributor, I want the authoritative standard extended in place so placement is doctrine-defined and no artifact points at a deleted gate. | High | Open |
| FR-007 | Implement a `scripts/docs/docs_structural_lint.py` structural lint with 4 checks scoped so the **current clean tree passes** (NFR-003): (a) `index_completeness` — only for sections the styleguide config declares "curated-complete" (start with `architecture/` only; other section indexes are landing pages, exempt); (b) `point_in_time_placement` — dated/point-in-time files live under `plans/**` broadly, with an allowlist covering `adr/**` (era-dated ADRs) and the audit's STAY subtrees `plans/research/**` + `plans/investigations/**`; (c) `shadow_tree_basename` — no shared NON-NAV content-duplicate basename across section subtrees (nav basenames `index.md`/`README.md`/`toc.yml` and era files `README-N.x.md`/`00-SYNTHESIS.md` exempt); (d) `frontmatter_contract` — every in-scope page carries the required frontmatter, where "in-scope" excludes section `README.md` landing pages (the 3 frontmatter-less ADR READMEs are deferred to #2227). | As a maintainer, I want a mechanical guard that catches drift the retired ratchet never did and is green on the real tree. | High | Open |
| FR-008 | Wire the new lint into the docs test/CI surface (target: `.github/workflows/docs-freshness.yml`) so it runs on every change, assuming the gate role the retired anti-sprawl ratchet vacated. | As a maintainer, I want structural drift blocked at CI, not discovered later. | High | Open |
| FR-009 | For every moved/removed path, add exactly one redirect-map entry, verify no baseline-URL 404s, regenerate the page-inventory and `toc.yml`, and keep `check_docs_freshness --ci` green. | As a docsite operator, I want zero dead URLs across the moves. | High | Open |
| FR-010 | The redirect/link tooling is currently **pinned to a different mission** (`redirect_stub_generator.py` `MISSION_SLUG = "common-docs-structural-move-01KW3SBK"`; `bulk_ref_rewrite.py` hardcodes `.../common-docs-structural-move-01KW3SBK/occurrence_map.yaml` as its DEFAULT). This mission must drive both against **this** mission's `occurrence_map.yaml` via the existing `--occurrence-map` (and `--redirect-map` where applicable) overrides; and either un-pin/parametrize the DEFAULT `MISSION_SLUG`/occurrence-map path so it is not silently bound to a foreign mission, OR (charter: missing/broken canonical surface → trace + file the gap) file an upstream gap for the pinned default. FR-009/NFR-002 must not ride on tooling silently bound to another mission. | As a docsite operator, I want the redirect tooling driven by this mission's map, not a foreign default. | High | Open |
| FR-011 | The extended `common-docs` styleguide gains a **machine-parseable config block** (SSOT) holding: the section list + which sections are "curated-complete"; the dated-filename patterns; the point-in-time allowlist; and the required frontmatter fields + in-scope exclusions. `docs_structural_lint.py` LOADS this config rather than hard-coding policy, and a test asserts the lint's behaviour matches the config (single source of truth, C-005). | As a maintainer, I want lint policy and doctrine to share one source so they cannot drift. | High | Open |

### Non-Functional Requirements

| ID | Title | Requirement | Category | Priority | Status |
|----|-------|-------------|----------|----------|--------|
| NFR-001 | Link integrity | After all moves, `relative_link_fixer --check` reports 0 broken relative links and 0 baseline-URL 404s against `redirect_baseline_urls.json`. | Reliability | High | Open |
| NFR-002 | Redirect coverage | 100% of moved/removed paths have exactly one corresponding redirect-map entry (1:1; no path without an entry, no orphan entry). | Reliability | High | Open |
| NFR-003 | Guard efficacy, clean-tree pass & speed | The docs lint flags each of the 4 audit finding-classes on a seeded regression fixture (100% detection) **and passes with zero violations on the current clean tree** (the 38 `index.md`, 38 `README.md`, 132 dated files under `adr/`, and the borderline STAY subtrees `plans/{research,investigations}/**` must all pass — they are allowlisted/exempt, not violations), completing in under 5 seconds locally. | Performance | High | Open |
| NFR-004 | No suite regressions | `tests/docs/`, the terminology guard (`test_no_legacy_terminology.py`), and `check_docs_freshness --ci` are all green on the aggregate diff. | Reliability | High | Open |
| NFR-005 | Zero split-brain | After FR-003, **0 shared NON-NAV content-duplicate basenames** across distinct section subtrees, and **0 basenames in the named shadow set** (`plans/notes/` twins of `architecture/`+`adr/3.x/`) — verified by the `shadow_tree_basename` check. Nav basenames (`index.md`, `README.md`, `toc.yml`) and sanctioned era files are exempt; this is not an absolute basename-uniqueness count. | Reliability | High | Open |
| NFR-006 | Frontmatter completeness | 100% of **in-scope** docs carry the required frontmatter (`doc_status`/`updated`; `type` where applicable), where "in-scope" **excludes section `README.md` landing pages**. The 3 frontmatter-less files (`docs/adr/{1.x,2.x,3.x}/README.md`) are allowlisted and deferred to #2227 — the audit confirms `adr/` is otherwise structurally clean. | Maintainability | Medium | Open |

### Constraints

| ID | Title | Constraint | Category | Priority | Status |
|----|-------|------------|----------|----------|--------|
| C-001 | Guides-zone boundary | No contributor/internal/point-in-time page may move into `docs/guides/`; nothing may become reachable from end-user navigation (the docs' own FR-003). Redistribution is to `engineering-notes/`, `operations/`, the doctrine tree, or intra-zone regroup only. | Technical | High | Open |
| C-002 | Canonical homes & ADR compliance | Targets and mechanics follow the Common-Docs reconciliation ADR (`docs/adr/3.x/2026-06-27-1`): canonical sections (D3), redirect stubs (D4), distil-then-retire → engineering-notes (D7). | Technical | High | Open |
| C-003 | Coordinate with in-flight work | Do not conflict with the `docs-ia-onboarding-overhaul` mission (owns `guides/`) or PR #2855 (folds #2851, retires ratchet); coordinate architecture-residual overlap with #2227; defer era-suffixed READMEs to #2215. | Business | High | Open |
| C-004 | Path-pinned artifacts stay put | Generated/pinned files (`3-2-page-inventory.yaml`, `toc.yml`) are regenerated in place, never relocated (`test_inventory_path_stable.py`). | Technical | Medium | Open |
| C-005 | Extend existing doctrine, don't mint | The standard is delivered by **extending** DIRECTIVE_042 + the `common-docs` styleguide (adding the concern-bucket→section map, allowlist, and machine-parseable config block) — NOT by authoring a new `documentation-placement` directive or an improvised `docs/` page. The lint reads the styleguide config as its single source of truth. | Technical | High | Open |
| C-006 | Bulk-edit fidelity | Moving files while repointing cross-file referrers is a bulk edit — a plan-phase `occurrence_map.yaml` classifies every referenced path so no referrer is silently missed (DIRECTIVE_035). | Technical | High | Open |
| C-007 | Redirect tooling not foreign-pinned | `redirect_stub_generator.py` and `bulk_ref_rewrite.py` default to a foreign mission's occurrence map (`common-docs-structural-move-01KW3SBK`). This mission MUST drive them against its own `occurrence_map.yaml` via the `--occurrence-map`/`--redirect-map` overrides, and un-pin the default or file an upstream gap (charter: missing/broken canonical surface → trace + file). No mission step may implicitly consume the foreign default. | Technical | High | Open |

### Key Entities

- **Concern bucket**: the (a–e) classification the audit assigns each file (how-to / reference / point-in-time / generated / doctrine).
- **Canonical section**: the target home a bucket maps to (`engineering-notes/`, `operations/`, doctrine tree, or in-zone).
- **Redirect-map entry**: `old_path → new_path` record generated before a move is complete.
- **Extended DIRECTIVE_042 + `common-docs` styleguide**: the EXISTING doctrine artifacts (FR-006) extended in place with the bucket→section map, the point-in-time allowlist, and the machine-parseable config block — not a new directive.
- **Styleguide config block (SSOT)**: the machine-parseable section list / curated-complete set / dated-filename patterns / allowlist / required-frontmatter block (FR-011) the lint LOADS.
- **Dangling-ratchet artifacts**: the 4 files (042 directive `validation_criteria`; styleguide `tooling`+`quality_test`; `common-docs-curation` + `common-docs-scaffold` tactics) still naming the retired "WP05 anti-sprawl structure ratchet", reconciled to cite the new lint.
- **Docs structural lint**: the `scripts/docs/docs_structural_lint.py` guard (FR-007) — index completeness (curated-complete sections), point-in-time placement (`plans/**` + allowlist), shadow-tree (non-nav basenames), frontmatter (in-scope pages).
- **Page-inventory / toc**: generated, path-pinned nav artifacts regenerated per move.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of the audit's 9 firm files end in a canonical concern-home; both borderlines (assessment + closeout) carry a recorded verification result and default to "stays" unless verified point-in-time (FR-002).
- **SC-002**: 0 broken internal links and 0 baseline-URL 404s across `docs/` after the mission.
- **SC-003**: The durable guard detects 100% of the 4 audit finding-classes on a regression fixture **and passes with zero violations on the current clean tree** — a reintroduced misfiling fails CI.
- **SC-004**: 0 shared non-nav content-duplicate basenames across section subtrees and 0 in the named `plans/notes/` shadow set (NFR-005).
- **SC-005**: The `architecture/` section index enumerates 100% of its files (baseline: ~4 of ~60); growing index-completeness to all 13 sections is explicitly out of scope.
- **SC-006**: DIRECTIVE_042 + the `common-docs` styleguide are extended in place, the lint loads the styleguide config, the 4 dangling-ratchet references are reconciled, and #2302 is closed — no new directive is minted.

## Assumptions

- The audit note (`docs/plans/engineering-notes/common-docs-section-audit.md`, this branch) is the authoritative finding set; its per-section disposition tables are the work list.
- PR #2855 (which retires the ratchet and folds #2851) lands before or independently of this mission; this mission does not reintroduce the ratchet.
- `operations/` already received #2851's runbooks and needs no inbound moves here.
- Era-suffixed architecture READMEs are out of scope (owned by #2215); the ~25 historical architecture residuals coordinate with #2227.
- **Deliberately out of scope**: the wider `migrations/` dated-residue sweep (beyond the single named closeout) is NOT part of this mission; the audit confirms `adr/` is structurally clean apart from the 3 frontmatter-less READMEs deferred to #2227.
- Both `redirect_stub_generator.py` and `bulk_ref_rewrite.py` already accept `--occurrence-map` overrides; only their DEFAULT is foreign-pinned (`01KW3SBK`), so this mission can proceed via overrides while it un-pins the default or files the gap (FR-010/C-007).
