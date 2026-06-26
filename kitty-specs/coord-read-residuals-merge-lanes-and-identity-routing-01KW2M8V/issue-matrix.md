# Issue matrix — coord-read-residuals-merge-lanes-and-identity-routing-01KW2M8V

Per FR-037 of the spec-kitty-mission-review skill Gate-4. One row per issue referenced in spec.md.

**Addressed by this Mission:** #2185 (Lane A) and #2186 (Lane B). The rest are context/boundary and are not closed here.

| Issue | Title | Verdict | Evidence ref |
|-------|-------|---------|--------------|
| #2185 | Coord-authority: route merge/+lanes/ PRIMARY reads off coord-aware resolvers | in-mission | Lane A — `<fill at WP time>` |
| #2186 | Coord-authority: route/guard meta.json identity reads (next_cmd telemetry drop) | in-mission | Lane B — `<fill at WP time>` |
| #2106 | Kind-aware write-surface placement (the cause) | verified-already-fixed | merged 2026-06-24; this Mission consumes its read-side seam |
| #2115 | Implement/review/merge reads WP `tasks/` off coord (originating) | deferred-with-followup | owned by sibling `implement-loop-coord-authority-completion-01KW2E7A`; not closed here |
| #2167 | Retire pre-3.0 `scripts/tasks/` legacy reader | deferred-with-followup | explicitly excluded (C-EXCL-2167) — pin-and-cite only, separate ticket |
| #2160 | Coord topology: unify artifact authority (epic) | deferred-with-followup | epic parent — reference-only (never claimed/closed by a child Mission) |

Valid `Verdict` values: `fixed`, `verified-already-fixed`, `deferred-with-followup`, `in-mission` (being fixed by a later WP in this Mission; must reach a terminal verdict before Mission `done`).

**Claim:** #2185 + #2186 assigned to the operator and a mission-naming comment posted on each (ticket-based mission hygiene). #2160 epic is operator-owned and reference-only — never re-claimed by this child.
