# Issue matrix — mission-lifecycle-dispatch-drg-closeout-01KV0S99

One row per issue this mission addresses. `in-mission` = being driven to closure by this mission
(non-terminal; must reach `fixed` / `verified-already-fixed` / `deferred-with-followup` before mission `done`).

| Issue | Title | Verdict | Evidence ref |
|-------|-------|---------|--------------|
| #1802 | Epic: Pre- and post-mission lifecycle support | in-mission | FR-001/FR-002/FR-003 — deliver post-merge follow-up + mission re-open surface (pre-mission half already shipped via #687/#1220); SC-3 |
| #1804 | Epic: Ops execution layer (ask/advise/do) | in-mission | FR-007 — closes once child #1810 lands; ops layer otherwise substantially delivered; SC-2 |
| #1810 | refactor: collapse do/ask/advise to dispatch | in-mission | FR-004/FR-005/FR-006 — single dispatch mechanism + retained UX aliases + 19-agent propagation; SC-1 |
| #1863 | DRG extractor orphans: styleguide/toolguide references | in-mission | FR-008/FR-009 — fix java-implementer stale ref + mechanical orphans; deterministic regen; documented residual; SC-4 |

Valid `Verdict` values: `fixed`, `verified-already-fixed`, `deferred-with-followup`, `in-mission`.

Context (not addressed here — already delivered, listed for lineage): #687, #1220 (pre-mission ingestion half of #1802, closed).
