# Phase 1 Data Model — Docs Structural Sanity & Concern Guard

This mission's "entities" are documentation-governance concepts and the lint's data shapes, not persistent domain objects.

## Concern bucket

The classification the audit assigns each doc.

- **Values**: `how_to` (a) · `reference_policy` (b) · `point_in_time` (c) · `generated_nav` (d) · `doctrine_artifact` (e)
- **Maps to** → a canonical section (see below). Invariant: every doc resolves to exactly one bucket.

## Canonical section (bucket → home)

| Bucket | Canonical relocation home | Lint allow-zone (`point_in_time_placement`) |
|---|---|---|
| how_to (contributor) | `docs/development/` — **never** `docs/guides/` (C-001) | n/a |
| reference_policy | `docs/development/` (or the domain section) | n/a |
| point_in_time | `docs/plans/engineering-notes/` (D7) | `plans/**` **broadly** + allowlist `adr/**`, `plans/research/**`, `plans/investigations/**` |
| ops runbook | `docs/operations/` | n/a |
| generated_nav | stays at pinned path (`3-2-page-inventory.yaml`, `toc.yml`) — C-004 | nav basenames exempt from `shadow_tree_basename` |
| doctrine_artifact | `src/doctrine/` | n/a |

Relocations land specifically in `engineering-notes/` (D7), but the lint's ALLOW zone is `plans/**` broadly so the STAY subtrees `plans/{research,investigations}/**` and era-dated `adr/**` pass without churn (NFR-003).

## Redirect-map entry

- **Fields**: `old_path` (e.g. `architecture/audits/2026-05-spec-kitty-caacs.html`), `new_path` (e.g. `plans/engineering-notes/architecture-audits/2026-05-spec-kitty-caacs.html`)
- **Rule**: exactly one entry per moved/removed path (NFR-002 1:1); no orphan entries.

## Extended documentation doctrine (FR-006, FR-011) — NOT a new directive

- **Kind**: the EXISTING `DIRECTIVE_042` (`042-common-docs.directive.yaml`) + the companion `common-docs` styleguide, extended in place. No new `documentation-placement` directive is minted (highest existing directive number is 046).
- **042 extension**: `validation_criteria` cites `scripts/docs/docs_structural_lint.py` as the live successor gate (currently it notes the ratchet retired and wires none).
- **Styleguide extension — config block (SSOT, FR-011)**: a machine-parseable block carrying the section list + the "curated-complete" set, the dated-filename patterns, the point-in-time allowlist (`adr/**`, `plans/research/**`, `plans/investigations/**`), the required frontmatter fields + in-scope exclusions (section READMEs), and the `guides/` boundary rule.
- **Dangling-ratchet reconciliation**: the styleguide `tooling`/`quality_test` rows and the `common-docs-curation` + `common-docs-scaffold` tactics stop naming the retired "WP05 anti-sprawl structure ratchet" and name the lint.
- **Invariant**: loadable via the doctrine loader; the lint LOADS the styleguide config block as its single source of truth (a `tests/docs/` test asserts lint behaviour == config).

## Docs structural lint — rule & violation

- **Rule** (4, each scoped so the clean tree passes): `index_completeness` (curated-complete sections only), `point_in_time_placement` (`plans/**` + allowlist), `shadow_tree_basename` (non-nav content basenames), `frontmatter_contract` (in-scope pages, section READMEs excluded).
- **Violation**: `{ rule_id, path, message }`; nonzero process exit when any violation is present.
- **Config input (SSOT)**: the section/curated-complete list, the point-in-time filename patterns + allowlist, the frontmatter-required fields + exclusions — **loaded from** the extended `common-docs` styleguide config block (FR-011), not hard-coded.

## Page-inventory lockfile / toc

- **Generated** from frontmatter; **path-pinned** (`test_inventory_path_stable.py`). Regenerated in place per move; never relocated (C-004).

## State transition (per moved file)

```
placed(old) --git mv--> placed(new)
             --redirect entry--> redirect_covered
             --relative_link_fixer--> referrers_repointed
             --inventory+toc regen--> nav_consistent
             --lint green--> compliant
```
Terminal: `compliant` (all gates green). A move is "done" only at `compliant`.

**Fold-then-delete variant** (the 3 shadow entries — canonical twin EXISTS): the first transition is `reconcile-into-canonical --git rm shadow-->` (NOT `git mv`, which would clobber the canonical), then the same redirect / link-fix / regen / lint path. See `occurrence_map.yaml` fold entries and quickstart Recipe B.
