# Tasks: Docs Structural Sanity & Concern Guard (#2302, epic #2314)

**Mission**: `docs-structural-sanity-01KY53KJ` | **Branch**: `docs/common-docs-section-audit` (coord topology)
**Spec**: `spec.md` | **Plan**: `plan.md` | **Research**: `research.md` | **Contract**: `contracts/docs-structural-lint.md` | **Map**: `occurrence_map.yaml`

Two independent tracks that converge at the aggregate sweep:

- **Doctrine + guard** (the durable keystone): **WP01 → WP02** — extend DIRECTIVE_042 + the `common-docs`
  styleguide config block (SSOT), then land the config-driven `docs_structural_lint.py` + CI wiring.
- **Content redistribution** (parallel, disjoint file sets): **WP03** (point-in-time moves + architecture
  index) ∥ **WP04** (shadow-tree fold-then-delete). Both feed the final IA-mechanics sweep.
- **IA mechanics & aggregate gate**: **WP05** — un-pins the foreign-pinned redirect tooling, regenerates
  the derived redirect-map / page-inventory / toc, repoints every referrer, and runs the aggregate gate
  (incl. the new lint) over the whole diff.

WP01, WP03, WP04 are parallel-startable (disjoint surfaces). WP02 needs WP01's config block; WP05 needs
the final move set (WP03+WP04) and the lint (WP02).

## Subtask Index

| ID | Description | WP | Parallel |
|----|-------------|----|----------|
| T001 | Extend DIRECTIVE_042 `validation_criteria` to cite `scripts/docs/docs_structural_lint.py` as the live successor gate | WP01 | [P] |
| T002 | Add the FR-011 machine-parseable **config block** (SSOT) to `common-docs.styleguide.yaml` | WP01 | |
| T003 | Rewrite the styleguide `tooling:` / `quality_test` rows: name the lint, retire the ratchet | WP01 | |
| T004 | Reconcile `common-docs-curation` + `common-docs-scaffold` tactics — ratchet steps → lint | WP01 | |
| T005 | Run the DRG/doctrine freshness gate; record the IC-02→IC-01 reverse-edge follow-up | WP01 | |
| T006 | Implement the 4 scoped checks in `docs_structural_lint.py` (index/point-in-time/shadow/frontmatter) | WP02 | |
| T007 | LOAD policy from the WP01 styleguide config block (FR-011) — no hard-coded divergent policy | WP02 | |
| T008 | Red-first regression fixture: one instance of each of the 4 finding-classes | WP02 | |
| T009 | Clean-tree assertions (adr/**, plans/{research,investigations}/**, 38 index/README nav basenames, 3 ADR READMEs) | WP02 | |
| T010 | Config-SSOT agreement test (lint runtime behaviour == styleguide config) | WP02 | |
| T011 | Wire the lint into `.github/workflows/docs-freshness.yml`; verify < 5 s | WP02 | |
| T012 | `git mv` `883-research-synthesis.md` → `engineering-notes/` | WP03 | [P] |
| T013 | `git mv` `883-mission-type-authority-brief.md` → `engineering-notes/` | WP03 | [P] |
| T014 | `git mv` `architecture/audits/` (7 files) → `engineering-notes/architecture-audits/` | WP03 | [P] |
| T015 | FR-002 verify the crime-scene assessment (DEFAULT STAYS; move only if verified point-in-time) | WP03 | |
| T016 | FR-002 verify the migrations `…-920-closeout.md` (DEFAULT STAYS; move only if verified) | WP03 | |
| T017 | Refresh `architecture/index.md` to full post-move section membership (FR-004) | WP03 | |
| T018 | Fold-then-delete `plans/notes/feature-detection.md` → canonical `architecture/` twin | WP04 | [P] |
| T019 | Fold-then-delete `plans/notes/gap-analysis-connector-installation-model.md` → canonical | WP04 | [P] |
| T020 | Fold-then-delete `plans/notes/adr-connector-auth-binding-separation.md` → canonical `adr/3.x/` (flag #2227) | WP04 | [P] |
| T021 | Correct/remove `plans/notes/README.md` for the emptied shadow dir | WP04 | |
| T022 | FR-010 un-pin: `redirect_stub_generator` `MISSION_SLUG` + `bulk_ref_rewrite` `01KW3SBK` default | WP05 | |
| T023 | Regenerate `redirect_map.yaml` via `regenerate-map --occurrence-map $MAP` (relocations + 3 folds) | WP05 | |
| T024 | `relative_link_fixer` over docs/** + `bulk_ref_rewrite` for the non-docs paradigm referrer | WP05 | |
| T025 | Regenerate page-inventory (`check_docs_freshness --inventory`) + `toc.yml` in place | WP05 | |
| T026 | Aggregate gate sweep (link-check, freshness, terminology, `tests/docs/`, lint clean) | WP05 | |

---

## Work Packages

### WP01 — Extend the Common-Docs doctrine standard (IC-01) · Track: Doctrine · Priority P1

- **Goal**: EXTEND the existing DIRECTIVE_042 + `common-docs` styleguide in place — cite the lint as the
  successor gate, add the FR-011 machine-parseable config block (SSOT), and reconcile the 4 dangling-ratchet
  artifacts to name `docs_structural_lint.py`. No new directive is minted (C-005).
- **Independent test**: `spec-kitty doctor doctrine --json` loads clean; a grep proves no artifact still
  names the retired "WP05 anti-sprawl structure ratchet"; the styleguide config block parses.
- **Dependencies**: none (Track root). **Prompt**: `tasks/WP01-extend-common-docs-doctrine.md`
- **Subtasks**: T001, T002, T003, T004, T005
- [ ] T001 Extend DIRECTIVE_042 `validation_criteria` to cite `scripts/docs/docs_structural_lint.py` (WP01)
- [ ] T002 Add the FR-011 machine-parseable config block (SSOT) to `common-docs.styleguide.yaml` (WP01)
- [ ] T003 Rewrite the styleguide `tooling:` / `quality_test` rows: name the lint, retire the ratchet (WP01)
- [ ] T004 Reconcile `common-docs-curation` + `common-docs-scaffold` tactics — ratchet steps → lint (WP01)
- [ ] T005 Run the DRG/doctrine freshness gate; record the IC-02→IC-01 reverse-edge follow-up (WP01)

### WP02 — Structural docs lint + config-SSOT + CI wiring (IC-02) · Track: Doctrine · Priority P1

- **Goal**: Land `scripts/docs/docs_structural_lint.py` — the durable successor to the retired ratchet —
  with 4 checks scoped so the current clean tree passes (NFR-003), LOADING the WP01 styleguide config as
  its single source of truth (FR-011), plus a red-first regression fixture and CI wiring (FR-008).
- **Independent test**: `pytest tests/docs/test_docs_structural_lint.py -q` — the 4-class fixture is RED
  before the checks land / GREEN after; the current tree passes with zero violations in < 5 s.
- **Dependencies**: WP01 (consumes its config block — may start against a stub, finalize after WP01).
  **Prompt**: `tasks/WP02-docs-structural-lint-and-ci.md`
- **Subtasks**: T006, T007, T008, T009, T010, T011
- [ ] T006 Implement the 4 scoped checks (index/point-in-time/shadow/frontmatter) (WP02)
- [ ] T007 LOAD policy from the WP01 styleguide config block (FR-011) — no hard-coded divergent policy (WP02)
- [ ] T008 Red-first regression fixture: one instance of each of the 4 finding-classes (WP02)
- [ ] T009 Clean-tree assertions (adr/**, plans/{research,investigations}/**, nav basenames, 3 ADR READMEs) (WP02)
- [ ] T010 Config-SSOT agreement test (lint runtime behaviour == styleguide config) (WP02)
- [ ] T011 Wire the lint into `.github/workflows/docs-freshness.yml`; verify < 5 s (WP02)

### WP03 — Point-in-time redistribution + architecture index (IC-03 + IC-05) · Track: Content · Priority P1/P3

- **Goal**: Relocate the 9 firm point-in-time architecture artifacts to `engineering-notes/`, adjudicate the
  2 FR-002 borderlines (default STAYS unless verified point-in-time), and refresh `architecture/index.md`
  to full post-move membership. Redirect/link mechanics are WP05's sweep — this WP does the moves + index only.
- **Independent test**: `architecture/` holds no dated dossier; `architecture/index.md` enumerates every
  remaining page; the moved files exist under `engineering-notes/`; each borderline carries a one-line verdict.
- **Dependencies**: none (Track root). **Prompt**: `tasks/WP03-point-in-time-redistribution.md`
- **Subtasks**: T012, T013, T014, T015, T016, T017
- [ ] T012 `git mv` `883-research-synthesis.md` → `engineering-notes/` (WP03)
- [ ] T013 `git mv` `883-mission-type-authority-brief.md` → `engineering-notes/` (WP03)
- [ ] T014 `git mv` `architecture/audits/` (7 files) → `engineering-notes/architecture-audits/` (WP03)
- [ ] T015 FR-002 verify the crime-scene assessment (DEFAULT STAYS; move only if verified) (WP03)
- [ ] T016 FR-002 verify the migrations `…-920-closeout.md` (DEFAULT STAYS; move only if verified) (WP03)
- [ ] T017 Refresh `architecture/index.md` to full post-move section membership (FR-004) (WP03)

### WP04 — Shadow-tree fold-then-delete (IC-04) · Track: Content · Priority P2

- **Goal**: Retire the `plans/notes/` split-brain shadow tree — for each of the 3 drifted twins, port the
  unique content INTO the EXISTING canonical copy, then `git rm` the shadow (NEVER `git mv` — it clobbers
  the canonical). Referrer repointing + old-shadow→canonical redirects are WP05's sweep.
- **Independent test**: `plans/notes/` no longer shadows any canonical basename; each canonical twin carries
  the reconciled content; the emptied shadow dir's README is corrected/removed.
- **Dependencies**: none (Track root). **Prompt**: `tasks/WP04-shadow-tree-fold-then-delete.md`
- **Subtasks**: T018, T019, T020, T021
- [ ] T018 Fold-then-delete `plans/notes/feature-detection.md` → canonical `architecture/` twin (WP04)
- [ ] T019 Fold-then-delete `plans/notes/gap-analysis-connector-installation-model.md` → canonical (WP04)
- [ ] T020 Fold-then-delete `plans/notes/adr-connector-auth-binding-separation.md` → canonical `adr/3.x/` (flag #2227) (WP04)
- [ ] T021 Correct/remove `plans/notes/README.md` for the emptied shadow dir (WP04)

### WP05 — IA-mechanics, tooling un-pin & aggregate gate sweep (IC-06) · Track: Convergence · Priority P1

- **Goal**: Un-pin the foreign-pinned redirect/link tooling (FR-010/C-007), regenerate the derived
  redirect-map / page-inventory / toc against THIS mission's map, repoint every referrer (docs/** + the
  one non-docs paradigm ref), and run the aggregate gate — the mission's Definition of Done.
- **Independent test**: `relative_link_fixer --check` clean (NFR-001); `check_docs_freshness --ci` green
  (NFR-004); `redirect_stub_generator check-map` reports 1:1 coverage (NFR-002); `docs_structural_lint`
  exits 0 (SC-003/004/005); `pytest tests/docs/` + terminology guard green.
- **Dependencies**: WP02 (the lint), WP03, WP04 (the final move set). **Prompt**: `tasks/WP05-ia-mechanics-and-gate-sweep.md`
- **Subtasks**: T022, T023, T024, T025, T026
- [ ] T022 FR-010 un-pin: `redirect_stub_generator` `MISSION_SLUG` + `bulk_ref_rewrite` `01KW3SBK` default (WP05)
- [ ] T023 Regenerate `redirect_map.yaml` via `regenerate-map --occurrence-map $MAP` (relocations + 3 folds) (WP05)
- [ ] T024 `relative_link_fixer` over docs/** + `bulk_ref_rewrite` for the non-docs paradigm referrer (WP05)
- [ ] T025 Regenerate page-inventory (`check_docs_freshness --inventory`) + `toc.yml` in place (WP05)
- [ ] T026 Aggregate gate sweep (link-check, freshness, terminology, `tests/docs/`, lint clean) (WP05)

---

## Dependencies & Lanes

```
Doctrine:  WP01 ───── WP02 ──┐
Content:   WP03 ─────────────┼── WP05
           WP04 ─────────────┘
```

- **Parallel-startable**: WP01, WP03, WP04 (disjoint surfaces — `src/doctrine/`, `docs/architecture/` moves,
  `docs/plans/notes/` folds — no path collision).
- **WP02 → WP01**: the lint LOADS WP01's styleguide config block (FR-011). Start against a stub if needed;
  the config is authoritative before merge. **Reverse edge (IC-02→IC-01)**: the lint's module path is written
  back into WP01's 4 artifacts — WP01 T005 records this so it is not lost.
- **WP05 → WP02, WP03, WP04**: the redirect-map regeneration + aggregate sweep need the final move set AND
  the lint. WP05 also carries the **sanctioned tool-driven leeway** to `relative_link_fixer --write` /
  `toc.yml` regen across referrer files outside any WP's `owned_files` (no other WP claims those referrers —
  the no-overlap guard holds).
- **MVP**: WP01→WP02 (the durable guard) is the keystone; without it every content move re-accretes. WP03 is
  the largest single content win.
- Coord topology; `finalize-tasks` computes `lanes.json` from these dependencies.

## Requirement coverage (each FR → exactly one primary WP)

| Requirement | Primary WP | Notes |
|---|---|---|
| FR-001 (relocate 9 firm point-in-time) | WP03 | |
| FR-002 (adjudicate 2 borderlines, default stays) | WP03 | |
| FR-003 (retire shadow tree) | WP04 | |
| FR-004 (architecture index completeness) | WP03 | |
| FR-005 (migrations closeout relocation) | WP03 | borderline — default stays unless verified |
| FR-006 (extend doctrine + reconcile ratchet refs) | WP01 | |
| FR-007 (lint, 4 checks) | WP02 | |
| FR-008 (CI wiring) | WP02 | |
| FR-009 (redirect-map/inventory/toc, 1:1 coverage) | WP05 | |
| FR-010 (un-pin foreign-pinned tooling) | WP05 | |
| FR-011 (styleguide config SSOT) | WP01 (author) | WP02 consumes/asserts agreement |
| NFR-001 (link integrity) | WP05 | |
| NFR-002 (redirect coverage) | WP05 | |
| NFR-003 (guard efficacy + clean-tree + speed) | WP02 | |
| NFR-004 (no suite regressions) | WP05 | aggregate sweep |
| NFR-005 (zero split-brain) | WP04 (produce) / WP02 (verify) | shadow-tree check |
| NFR-006 (frontmatter completeness) | WP02 | frontmatter check |
| C-001 (guides-zone boundary) | WP03/WP04 | no content into guides/ |
| C-002 (canonical homes + ADR) | WP03 | |
| C-005 (extend, don't mint) | WP01 | |
| C-006 (bulk-edit fidelity) | WP05 | occurrence_map is the checklist |
| C-007 (tooling not foreign-pinned) | WP05 | |

## Risks

- **Foreign-pinned tooling silently consumed** (C-007): every redirect/link command MUST pass
  `--occurrence-map $MAP`; WP05 T022 un-pins the default so an omission cannot bind the foreign mission.
- **Fold-then-delete clobber** (WP04): a mechanical `git mv shadow canonical` destroys the canonical twin —
  the 3 shadow entries are reconcile-into-canonical + `git rm`, per occurrence_map fold notes / quickstart B.
- **Config/lint drift** (FR-011): the styleguide config and the lint must agree — WP02 T010's config-SSOT
  test is the guard; WP01 must not encode policy the lint cannot read.
- **Borderline force-move** (FR-002): the assessment + closeout DEFAULT to stays; WP03 moves one only on a
  recorded point-in-time verdict, never by assumption.
</content>
</invoke>
