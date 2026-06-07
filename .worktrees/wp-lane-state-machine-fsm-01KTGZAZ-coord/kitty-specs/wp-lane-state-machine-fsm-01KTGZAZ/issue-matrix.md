# Issue matrix — wp-lane-state-machine-fsm-01KTGZAZ

Per FR-037 of the spec-kitty-mission-review skill Gate-4. One row per issue referenced in spec.md.

| Issue | Title | Verdict | Evidence ref |
|-------|-------|---------|--------------|
| #1589 | Status model split-brain (finalize clobbers coord event log; unseeded WP defaults to `planned`; dual transition-truth) | deferred-with-followup | WP01 (613a0f4d0) closes the dual-transition-truth half: FSM is now the sole edge+guard+force authority, no production `ALLOWED_TRANSITIONS` gate, genesis `from_lane`-only. Follow-up: #1589 stays open — the finalize/coord-clobber and read-side default-to-genesis halves are tracked by later WPs (Contract 3 / Contract 5, FR-019) and resolved at mission-review. |
| #1666 | Epic: canonical execution-state surface (lane FSM slice) | deferred-with-followup | This mission is an explicit slice of epic #1666 (spec.md §Assumptions). WP01 (613a0f4d0) delivers the FSM single-ownership slice (FR-001/002/003/012/015). Follow-up: #1666 remains the umbrella epic, continued across WP02–WP06 and beyond. |

Valid `Verdict` values: `fixed`, `verified-already-fixed`, `deferred-with-followup`.
