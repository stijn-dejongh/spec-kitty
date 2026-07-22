# Contract — `scripts/docs/docs_structural_lint.py` (FR-007, FR-008)

The durable successor to the retired anti-sprawl ratchet. Contract-level behaviour the implementation and its tests must satisfy.

## Invocation

```
python -m scripts.docs.docs_structural_lint [--json] [--fix-hints] [DOCS_ROOT=docs]
```

- Exit `0` when no violations; exit non-zero when any violation exists (CI gate role, FR-008).
- `--json` emits `{"violations": [{rule_id, path, message}], "checked": <int>}`.
- Completes in **< 5 s** on the current tree (NFR-003).

## Checks (each independently testable — SC-003)

| rule_id | Fails when | Message names |
|---|---|---|
| `index_completeness` | a non-index page in a section is absent from that section's `index.md` | the missing page + its section index |
| `point_in_time_placement` | a file whose name matches a dated pattern (`^\d{4}-\d{2}`) or self-declares point-in-time/closeout lives outside `plans/engineering-notes/` and is not allowlisted | the file + its canonical home |
| `shadow_tree_basename` | the same basename exists under two distinct doc roots | both paths |
| `frontmatter_contract` | an in-scope page lacks `type`, `doc_status`, or `updated` | the file + missing field(s) |

## Configuration source of truth

The section list, dated-filename patterns, the **allowlist** (ADR-by-date, `CHANGELOG`, `changelog/`), and required frontmatter fields are read from the documentation-standard doctrine artifact (FR-006) — the lint does not hard-code policy divergent from the directive (C-005).

## Regression fixture (ATDD — Charter Check)

A `tests/docs/test_docs_structural_lint.py` fixture reintroduces one instance of **each** of the 4 rule classes and asserts each is caught (100% detection, SC-003); a clean-tree assertion proves no false positive on the post-mission tree.

## Non-goals

- Does not move files or rewrite links (that is the mission's content work + `relative_link_fixer`).
- Does not resurrect the retired ratchet's `CANONICAL_SECTIONS`/`section_missing_index` behaviour verbatim — index *completeness* replaces index *existence*.
