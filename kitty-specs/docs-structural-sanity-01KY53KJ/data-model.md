# Phase 1 Data Model — Docs Structural Sanity & Concern Guard

This mission's "entities" are documentation-governance concepts and the lint's data shapes, not persistent domain objects.

## Concern bucket

The classification the audit assigns each doc.

- **Values**: `how_to` (a) · `reference_policy` (b) · `point_in_time` (c) · `generated_nav` (d) · `doctrine_artifact` (e)
- **Maps to** → a canonical section (see below). Invariant: every doc resolves to exactly one bucket.

## Canonical section (bucket → home)

| Bucket | Canonical home |
|---|---|
| how_to (contributor) | `docs/development/` — **never** `docs/guides/` (C-001) |
| reference_policy | `docs/development/` (or the domain section) |
| point_in_time | `docs/plans/engineering-notes/` (D7) |
| ops runbook | `docs/operations/` |
| generated_nav | stays at pinned path (`3-2-page-inventory.yaml`, `toc.yml`) — C-004 |
| doctrine_artifact | `src/doctrine/` |

## Redirect-map entry

- **Fields**: `old_path` (e.g. `architecture/audits/2026-05-spec-kitty-caacs.html`), `new_path` (e.g. `plans/engineering-notes/architecture-audits/2026-05-spec-kitty-caacs.html`)
- **Rule**: exactly one entry per moved/removed path (NFR-002 1:1); no orphan entries.

## Documentation-standard directive (FR-006)

- **Kind**: doctrine `directive` + companion `styleguide`.
- **Carries**: the bucket→section map, the frontmatter contract (`type`, `doc_status`, `updated`), the point-in-time allowlist, and the `guides/` boundary rule.
- **Invariant**: loadable via the doctrine loader; the lint cites it as its source of truth.

## Docs structural lint — rule & violation

- **Rule** (4): `index_completeness`, `point_in_time_placement`, `shadow_tree_basename`, `frontmatter_contract`.
- **Violation**: `{ rule_id, path, message }`; nonzero process exit when any violation is present.
- **Config input**: the section list, the point-in-time filename patterns + allowlist, the frontmatter-required fields (sourced from the directive/styleguide).

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
