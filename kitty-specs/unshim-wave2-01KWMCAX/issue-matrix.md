# Issue Matrix — unshim-wave2-01KWMCAX

<!-- Schema: issue | title (optional) | verdict | evidence ref (mandatory) -->
<!-- Valid verdicts: fixed | verified-already-fixed | deferred-with-followup | in-mission -->

| Issue | Title | Verdict | Evidence ref |
|---|---|---|---|
| #2291 | closes: execute registered removals (specify_cli.next + glossary) | in-mission | FR-001..FR-004: re-point 3 src callers + seam + 77-file test surface (squad census supersedes the body's 49), delete both shims, drain registry rows + schema-test assertions. |
| #2290 | closes: charter deprecation-cycle closure | in-mission | FR-005..FR-007 as FULL DELETE (adjudicated decision 1 — registering would recreate the rescinded version-boundary deferral): 4 src callers incl. the runner.py:36 canonical→legacy defect, ~20 test files, lock-gate (6 tests) retired with per-test disposition table, charter_activate settled CANONICAL (documented-excluded, no deletion). |
| #2326 | closes: dead frontmatter::update_field wrapper | in-mission | FR-008: wrapper + __all__ + orphaned instance method deleted; category_b row drained; baseline 216→215. |
| #1868 | partial: WS1 mission_runtime layer-rule bind | in-mission | FR-009: dedicated sub-issue filed at spec time (parent #1868); non-vacuous LayerRule + theater; WS2–WS6 remain open. |
| #2327 | closes: WS1 mission_runtime layer-rule bind (sub-issue of #1868) | in-mission | FR-009 / WP08: outbound LayerRule bound with the named allowed-exception ledger + committed CI-selected negative test; closeout posts the evidence comment. |
| #1797 | parent epic (unshim cluster) | deferred-with-followup | Epic stays OPEN — Wave 2 is one slice; follow-up is #1797 itself (Wave 3+: #2293 burn-down, remaining shim families). Progress comment at merge: registry drained to zero legacy rows, 5+ shim surfaces deleted, honest baseline counts. |
| #612 | closed antecedent (next-extraction ticket, parent #391) | verified-already-fixed | CLOSED 2026-06-01; Wave 2 completes the deletion it registered. PR body references, never re-closes. |
| #613 | closed antecedent (glossary-extraction ticket, parent #391) | verified-already-fixed | CLOSED 2026-06-01; Wave 2 completes the deletion it registered. PR body references, never re-closes. |
| #391 | debt epic (parent of #612/#613) | deferred-with-followup | Referenced lineage only — remainder of the extraction-debt epic continues under #391; nothing in Wave 2 closes it. |
| #2072 | Obligation B boundary | deferred-with-followup | Obligation B (~10 resolver sites) is NOT in any Wave 2 surface (verified); stays open under #2072; operator note on #2293's prerequisite semantics posted at closeout (FR-010). |
| #2293 | boundary: category_b burn-down (later wave) | deferred-with-followup | Stays OPEN as the follow-up wave; needs #2072 formal closure or operator prerequisite confirmation; Wave 2 hands it honest baselines (WP07). |
| #2034 | CI marker-gate hole | deferred-with-followup | Follow-up: #2034 stays OPEN upstream; honored in-mission as the NFR-005 obligation (new/relocated tests carry CI-selected markers — proven for WP08's three new tests). |
| #2159 | reference: uv_receipt trap (closed) | verified-already-fixed | Lesson encoded as C-001 (re-point before delete); no structural constraint. |
