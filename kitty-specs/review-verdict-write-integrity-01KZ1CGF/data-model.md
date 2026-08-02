# Phase 1 Data Model: Review Verdict Write Integrity

No new persistent entity is introduced. This mission changes the **behavior** of existing entities'
writers/readers; the shapes below are the existing schema, annotated with what changes.

## ReviewCycleArtifact

The durable, per-WP, per-cycle record of a review decision (`review-cycle-N.md`).

| Field | Type | Change this mission |
|---|---|---|
| `cycle_number` | `int` | unchanged — `ReviewCycleArtifact.next_cycle_number` (glob-count + 1) unchanged |
| `wp_id` | `str` | unchanged |
| `mission_slug` | `str` | unchanged |
| `reviewer_agent` | `str` | unchanged — must be a real value, never the literal `"unknown"`, on both verdict paths |
| `verdict` | `Literal["approved", "rejected", "changes_requested"]` | **schema already allows `"approved"`; FR-001 is the first writer that produces it** |
| `reviewed_at` | `str` (UTC timestamp) | unchanged |
| `affected_files` | `list[AffectedFile]` | unchanged |
| `body` | `str` | **FR-002 adds a provenance guard before this is populated from `feedback_source`** — see State Transitions below |

**Invariant (unchanged)**: the highest-numbered `review-cycle-N.md` for a WP is the one every terminal
gate (`move-task --to approved/--to done`, `spec-kitty merge`) treats as authoritative.

**New invariant (FR-002)**: `body` may never be populated from a `feedback_source` that is — by path
identity or by content identity (post-frontmatter-strip, whitespace-normalized) — a prior cycle's own
artifact for the same WP.

## ReviewOverride (existing, consumed not created by this mission)

Event-sourced record of an operator/arbiter override, resolved via `resolve_snapshot_review(feature_dir,
wp_id)` from the reduced status snapshot. FR-003 reuses this exact mechanism (already proven for the
override-honoring case) to resolve the WP's authoritative review state for the stale-verdict scan,
instead of that scan's current bare file-glob.

| Field | Type | Role |
|---|---|---|
| `override_actor` | `str \| None` | who authorized the override |
| `override_reason` | `str \| None` | why |
| `complete` | `bool` (property) | both actor and reason present and non-empty |

## State Transitions

### WP review-verdict lifecycle (extended by FR-001)

```
[no artifact] --reject--> review-cycle-1.md (verdict=rejected)
review-cycle-N.md (verdict=rejected) --approve (normal path, NEW)--> review-cycle-(N+1).md (verdict=approved)
review-cycle-N.md (verdict=rejected) --approve (genuine arbiter override, UNCHANGED)--> review_artifact_override_* stamped on cycle N, honored via ReviewOverride snapshot
```

The "approve (normal path, NEW)" edge is FR-001 — it does not exist in the codebase today (confirmed:
zero call sites for any approved-verdict writer). The override edge is unchanged, pre-existing, already
correct (fixed by #1924) — genuinely separate machinery, not touched by this mission.

### Feedback-source acceptance (FR-002, new guard on the rejection edge)

```
feedback_source provided
  → resolve path
  → [NEW] path ∈ {this WP's own review-cycle-*.md}? → reject (ReviewCycleError)
  → [NEW] body(feedback_source) content-matches any existing cycle's body? → reject (ReviewCycleError)
  → read body, proceed as today
```

### Stale-verdict scan resolution (FR-003, new precedence)

```
_get_wp_review_verdict(wp_id)
  → [NEW] resolve_snapshot_review(coord-or-primary feature_dir per topology, wp_id) → ReviewOverride/verdict present? use it
  → [fallback, unchanged] file-glob review-cycle-*.md in the topology-appropriate authoritative dir → parse verdict
```

## Key Entities (from spec.md, restated with implementation shape)

- **Work Package (WP)**: unit under review; owns a directory of `review-cycle-N.md` files under its
  mission's `tasks/<wp-slug>/` (PRIMARY-partition, `MissionArtifactKind.WORK_PACKAGE_TASK`, unchanged).
- **Terminal gate**: `move-task --to approved/--to done` and `spec-kitty merge`'s
  `REJECTED_REVIEW_ARTIFACT_CONFLICT` invariant — both read the highest-numbered artifact; FR-001
  changes what that artifact *is* (a real approved record) on the normal path, not how it's read.
