# Contract: Generalized review-cycle writer

No external/REST/GraphQL contract applies to this mission — it is entirely internal Python behavior.
This document is the internal function-contract equivalent, per this repo's own convention of using
`contracts/` for behavioral contracts on internal seams (cf. `specify-plan-commit-boundary.md`).

## `create_rejected_review_cycle` → generalized writer (name unchanged; behavior extended)

**Before this mission**: writes only `verdict="rejected"` artifacts; validates `feedback_source` only
for existence/is-file/non-empty.

**After this mission**:

```
def create_rejected_review_cycle(
    *,
    main_repo_root: Path,
    mission_slug: str,
    wp_id: str,
    wp_slug: str,
    feedback_source: Path,
    reviewer_agent: str = "unknown",
    affected_files: list[dict[str, str]] | None = None,
    verdict: Literal["approved", "rejected"] = "rejected",   # NEW — default preserves every existing call site
) -> CreatedRejectedReviewCycle:
```

**Contract**:

- **Backward compatibility**: every existing call site (currently one: `_mt_finalize_plan`'s rejection
  path) continues to work unchanged — `verdict` defaults to `"rejected"`.
- **New behavior (`verdict="approved"`)**: writes a new highest-numbered `review-cycle-(N+1).md` with
  `verdict: "approved"`, the caller-supplied `reviewer_agent` (must be real — the caller, not this
  function, is responsible for never passing the literal placeholder for a genuine approval), through
  the same `_review_cycle_wp_dir` seam unchanged.
- **New provenance guard (both verdicts)**: raises `ReviewCycleError` before writing if `feedback_source`
  is, by path or by content, a prior cycle's own artifact for this WP (see `data-model.md`'s Feedback-
  source acceptance transition). Applies uniformly — an `approved` write also goes through this guard,
  since a caller could in principle mis-supply a stale file for either verdict.
- **Unchanged**: cycle-number assignment (`ReviewCycleArtifact.next_cycle_number`), the write target
  (`_review_cycle_wp_dir`, PRIMARY-partition, `WORK_PACKAGE_TASK` kind), and `validate_review_artifact`'s
  role as a post-construction sanity check (loosened per `research.md` R4 to accept both verdicts, not
  removed).

## `validate_review_artifact`

**Before**: `if artifact.verdict != "rejected": raise ReviewCycleError(...)`.
**After**: `if artifact.verdict not in REVIEW_ARTIFACT_VERDICTS: raise ReviewCycleError(...)` — matches
the schema-level `REVIEW_ARTIFACT_VERDICTS` frozenset already in `review/artifacts.py`, no new
vocabulary introduced (C-002).

## `_get_wp_review_verdict` (agent_utils/status.py)

**Before**: `wp_dir.glob("review-cycle-*.md")`, parse latest, return `verdict` field. `wp_dir` is always
computed under a PRIMARY-only `tasks_dir`.

**After**: resolve the WP's event-sourced review state first via `resolve_snapshot_review(feature_dir,
wp_id)` (topology-appropriate `feature_dir` — coord for `lanes_with_coord` missions, matching the
resolution `_mt_resolve_targets` already uses for status events); fall back to the existing file-glob
read only when no snapshot entry exists. Return type and call-site signature for existing callers of
`_get_wp_review_verdict` remain unchanged (`str | None`).
