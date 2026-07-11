# Issue matrix — runtime-bridge-degod-01KX8M1C

Per FR-037 of the spec-kitty-mission-review skill Gate-4. One row per issue referenced in spec.md.

| Issue | Title | Verdict | Evidence ref |
|-------|-------|---------|--------------|
| #2531 | Decompose `runtime_bridge.py` god-module into ports+cores (behavior-preserving) | in-mission | design/runtime-bridge-degod — WP01 parity oracle (3d83732cc) + WP02 compat guard (72f5d5785) landed as the C-004 blocking safety nets; decomposition lands across WP03–WP10. Terminal `fixed` at mission `done`. |
| #1619 | Epic: runtime/state overhaul | deferred-with-followup | Parent epic. This mission is a scoped slice (`runtime_bridge.py` only); the broader overhaul is explicitly out of scope (spec Non-Goals). Epic remains open and tracks the remaining slices. |
| #2173 | Epic: infra-logic separation (inject infra as ports, keep core pure) | deferred-with-followup | Parent epic. This mission applies the ports+cores treatment (C-002) to one module; the epic remains open for the other god-modules. |
| #2056 | Sibling god-module: `agent/mission.py` | deferred-with-followup | Sibling (different file, same shape). Not a deliverable here; handled by its own mission. Referenced only as a convention template (C-003). |
| #2057 | Sibling god-module: `merge.py` | deferred-with-followup | Sibling. Already landed under its own mission; reused here as the flat-module + `__all__` convention template (C-003). |
| #2059 | Sibling god-module: `doctor.py` | deferred-with-followup | Sibling (different file). Not a deliverable here; handled by its own mission. |
| #2464 | Sibling god-module: `agent/workflow.py` | deferred-with-followup | Sibling. Already landed; reused here as the layout + `DecideNextContext` + lazy-accessor template (spec Assumptions). |
| #2535 | Doctrine-controlled gates mission (WP14 inverts the composition-dispatch selection) | deferred-with-followup | Downstream consumer this mission ENABLES via FR-008 (clean selection seam) WITHOUT coupling to its unlanded `resolve_gates` (C-005). Gates WP14 runs after this mission lands; tracked in mission #2535. |
| #2545 | Sibling: coord-authority trio degod | deferred-with-followup | Coordination sibling on a separate branch; does not touch `runtime_bridge.py` (rewrites `cli/commands/agent/workflow.py`, lists #2531 out of scope). Light rebase only, coordinate not block (C-006). |

Valid `Verdict` values: `fixed`, `verified-already-fixed`, `deferred-with-followup`, `in-mission` (being fixed by a later WP in this mission; must reach a terminal verdict before mission `done`).
