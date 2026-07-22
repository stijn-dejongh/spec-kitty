# Quickstart — Docs Structural Sanity & Concern Guard

How to execute and verify this mission's work. All commands run from the repository-root checkout. **All redirect/link tooling is driven against THIS mission's `occurrence_map.yaml` via `--occurrence-map`** — its built-in default is pinned to a foreign mission (`common-docs-structural-move-01KW3SBK`); never rely on that default (FR-010/C-007).

```bash
MAP=kitty-specs/docs-structural-sanity-01KY53KJ/occurrence_map.yaml
```

## Recipe A — relocate a point-in-time file (target does NOT yet exist)

```bash
git mv docs/architecture/audits/2026-05-spec-kitty-caacs.md \
       docs/plans/engineering-notes/architecture-audits/2026-05-spec-kitty-caacs.md
# 1. redirect_map is single-writer + DERIVED — REGENERATE it from this mission's moves: spine
python -m scripts.docs.redirect_stub_generator regenerate-map --occurrence-map "$MAP"
python -m scripts.docs.redirect_stub_generator check-map      --occurrence-map "$MAP"   # 1:1 coverage (NFR-002)
# 2. repoint in-repo relative links (docs/** ONLY — writes by default; NO --write flag)
python -m scripts.docs.relative_link_fixer
# 3. rewrite NON-docs/ prefix referrers (src/, scripts/) the relative fixer never walks
python -m scripts.docs.bulk_ref_rewrite --occurrence-map "$MAP"
# 4. regenerate the page-inventory lockfile in place (path pinned — C-004)
python -m scripts.docs.check_docs_freshness --inventory docs/development/3-2-page-inventory.yaml
# 5. update related: frontmatter edges on the moved file + referrers
```

## Recipe B — fold-then-delete a shadow (canonical twin ALREADY EXISTS)

The 3 `plans/notes/` shadows have canonical twins that STAY — do **NOT** `git mv` (it clobbers the canonical).

```bash
# 1. reconcile: port any UNIQUE content from the shadow INTO the existing canonical twin
diff docs/plans/notes/feature-detection.md docs/architecture/feature-detection.md
#    (merge divergent content into docs/architecture/feature-detection.md by hand)
# 2. delete the shadow
git rm docs/plans/notes/feature-detection.md
# 3. redirect the old-shadow URL -> the EXISTING canonical .html (derived from the fold note in the map)
python -m scripts.docs.redirect_stub_generator regenerate-map --occurrence-map "$MAP"
# 4. repoint referrers to the canonical path
python -m scripts.docs.relative_link_fixer
python -m scripts.docs.bulk_ref_rewrite --occurrence-map "$MAP"
# 5. correct docs/plans/notes/README.md; regenerate inventory
```

The authoritative relocation list is `occurrence_map.yaml` (`moves:` block); the 3 folds are carried in its clearly-marked fold-then-delete note, not as `moves:` relocations.

## Run the new guard

```bash
python -m scripts.docs.docs_structural_lint            # exit 0 = clean
python -m scripts.docs.docs_structural_lint --json     # machine-readable violations
```

## Verify the aggregate (mission Definition of Done)

```bash
python -m scripts.docs.relative_link_fixer --check     # NFR-001: 0 broken relative links
python -m scripts.docs.check_docs_freshness --ci       # NFR-004: inventory/toc fresh, no baseline 404s
pytest tests/docs/ -q                                  # docs_structural_lint regression fixture + config-SSOT assert (SC-003, FR-011)
pytest tests/architectural/test_no_legacy_terminology.py -q   # NFR-004: terminology guard (CI-only gate)
python -m scripts.docs.docs_structural_lint            # SC-003/004/005: clean tree, 0 shadow basenames, full architecture/ index
```

## Success signals

- `architecture/` holds no dated dossier; `architecture/index.md` enumerates every page (SC-005).
- `docs/plans/notes/` no longer shadows any canonical basename (SC-004).
- Every moved URL resolves via a redirect; `relative_link_fixer --check` is clean (SC-002).
- DIRECTIVE_042 + the `common-docs` styleguide are extended in place, the lint loads the styleguide config, the 4 dangling-ratchet references are reconciled, and `#2302` is closable (SC-006).
- Reintroducing any of the 4 finding-classes fails `docs_structural_lint` (SC-003).
