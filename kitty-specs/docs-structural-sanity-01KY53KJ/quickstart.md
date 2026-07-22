# Quickstart — Docs Structural Sanity & Concern Guard

How to execute and verify this mission's work. All commands run from the repository root checkout.

## Apply one move (the per-file loop)

```bash
git mv docs/architecture/2026-05-spec-kitty-caacs.md \
       docs/plans/engineering-notes/architecture-audits/2026-05-spec-kitty-caacs.md
# 1. redirect entry (1:1 — NFR-002)
python -m scripts.docs.redirect_stub_generator --add \
  --old architecture/audits/2026-05-spec-kitty-caacs.html \
  --new plans/engineering-notes/architecture-audits/2026-05-spec-kitty-caacs.html
# 2. repoint in-repo relative links
python -m scripts.docs.relative_link_fixer --write
# 3. regenerate nav + inventory in place (path pinned — C-004)
python -m scripts.docs.check_docs_freshness --write-inventory
# 4. update related: frontmatter edges on the moved file + referrers
```

The authoritative move list + per-path rationale is `occurrence_map.yaml` (`moves:` block).

## Run the new guard

```bash
python -m scripts.docs.docs_structural_lint            # exit 0 = clean
python -m scripts.docs.docs_structural_lint --json     # machine-readable violations
```

## Verify the aggregate (mission Definition of Done)

```bash
python -m scripts.docs.relative_link_fixer --check     # NFR-001: 0 broken links
python -m scripts.docs.check_docs_freshness --ci       # NFR-004: inventory/toc fresh
pytest tests/docs/ -q                                  # incl. docs_structural_lint regression fixture (SC-003)
pytest tests/architectural/test_no_legacy_terminology.py -q   # NFR-004: terminology guard (CI-only gate)
python -m scripts.docs.docs_structural_lint            # SC-003/004/005: clean tree, 0 shadow basenames, full index
```

## Success signals

- `architecture/` holds no dated dossier; `architecture/index.md` enumerates every page (SC-005).
- `docs/plans/notes/` no longer shadows any canonical basename (SC-004).
- Every moved URL resolves via a redirect; `relative_link_fixer --check` is clean (SC-002).
- The documentation-standard doctrine artifact loads; `#2302` is closable (SC-006).
- Reintroducing any of the 4 finding-classes fails `docs_structural_lint` (SC-003).
