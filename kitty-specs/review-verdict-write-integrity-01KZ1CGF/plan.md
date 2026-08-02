# Implementation Plan: Review Verdict Write Integrity

**Branch**: `research/3044-review-artifact-topology-seam` | **Date**: 2026-08-02 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `kitty-specs/review-verdict-write-integrity-01KZ1CGF/spec.md`

**Note**: This template is filled in by the `/spec-kitty.plan` command. See `src/doctrine/missions/software-dev/command-templates/plan.md` for the execution workflow.

## Summary

Approving a previously-rejected work package (WP) does not persist any artifact today — the stale `rejected` verdict remains authoritative for every terminal gate, forcing an operator override on the ordinary path. This mission generalizes the existing rejected-verdict writer (`create_rejected_review_cycle`) into a single verdict-aware writer that also handles `approved`, adds a feedback-source provenance guard that closes both the fabrication (#2996(b)) and content-wrapping (#990) defects in that same function, and fixes an independent coord-topology authority split (#2646/#2697) where a review-cycle write and at least one of its readers disagree about which worktree is canonical.

## Technical Context

**Language/Version**: Python 3.11+ (repository standard; no new language/runtime requirement)
**Primary Dependencies**: None new. Uses existing internals: `mission_runtime.placement_seam`/`MissionArtifactKind`, `specify_cli.review.cycle`, `specify_cli.review.artifacts`, `specify_cli.status` (`ReviewResult`).
**Storage**: Filesystem — git-tracked Markdown artifacts (`review-cycle-N.md` with YAML frontmatter). No database involved.
**Testing**: pytest, targeted packages (`tests/review/`, `tests/post_merge/`, `tests/agent/`, `tests/regression/`) per this repo's scoped-change testing convention — not the full suite, per Testing Requirements.
**Target Platform**: Cross-platform CLI (Linux/macOS/Windows via WSL) — unchanged from the project as a whole.
**Project Type**: Single project (this mission modifies the `spec-kitty` CLI package itself).
**Performance Goals**: No new performance target beyond NFR-003 (≤5% wall-clock regression on `move-task --to approved` / `spec-kitty merge --dry-run` versus pre-mission baseline).
**Constraints**: NFR-001 (zero regression in `tests/review/`, `tests/post_merge/`); C-001–C-004 from spec.md (no topology-seam re-architecture beyond FR-003's narrow scope, no verdict-vocabulary/cycle-numbering change, no coord/primary partition relitigation).
**Scale/Scope**: Touches 3–4 production modules (`review/cycle.py`, `review/artifacts.py`, `cli/commands/agent/tasks_move_task.py`, `agent_utils/status.py`) plus their test siblings. No new modules.

## Charter Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Assessed against `.kittify/charter/charter.md`'s Code Quality / Quality Gates sections:

- **Required pytest surface**: `tests/review/`, `tests/post_merge/`, `tests/agent/`, `tests/regression/` (scoped — not the full suite, per this repo's own scoped-change testing convention).
- **Type checking**: `mypy --strict` must pass on every touched module (`review/cycle.py`, `review/artifacts.py`, `tasks_move_task.py`, `agent_utils/status.py`).
- **Docstrings**: the generalized writer's new `verdict` parameter and any new public/module-level function need docstrings per the Code Review Checklist.
- **No regressions**: NFR-001 restates this explicitly as a spec-level requirement, not just a charter formality.
- **CHANGELOG**: this is a bug fix to internal review-cycle behavior, not a breaking public-API/CLI-surface change (existing callers of `create_rejected_review_cycle` keep working via a `verdict="rejected"` default) — a CHANGELOG entry is still warranted (user-visible behavior change: approvals now persist; `--skip-review-artifact-check` no longer needed on the ordinary path) even though it isn't a breaking change requiring a migration note.
- **PR requirements** (linear history, independent review): applies at merge time, not plan time — noted here so `/spec-kitty.tasks` and the eventual PR reflect it; an adversarial squad (as already run post-spec) is this mission's sanctioned independent-review mechanism.

No charter violations identified. Complexity Tracking table below is empty — no exceptions to justify.

## Project Structure

### Documentation (this mission)

```
kitty-specs/review-verdict-write-integrity-01KZ1CGF/
├── plan.md              # This file (/spec-kitty.plan command output)
├── research.md          # Phase 0 output (/spec-kitty.plan command)
├── data-model.md        # Phase 1 output (/spec-kitty.plan command)
├── quickstart.md        # Phase 1 output (/spec-kitty.plan command)
├── contracts/           # Phase 1 output (/spec-kitty.plan command) — not applicable, no new external contract
└── tasks.md             # Phase 2 output (/spec-kitty.tasks command - NOT created by /spec-kitty.plan)
```

### Source Code (repository root)

```
src/specify_cli/review/
├── cycle.py              # create_rejected_review_cycle generalized to a verdict-aware writer (FR-001);
│                          # feedback-source provenance guard added here (FR-002, closes #2996(b) + #990)
└── artifacts.py           # validate_review_artifact's hardcoded rejected-only check loosened to accept
                            # "approved" (C-002)

src/specify_cli/cli/commands/agent/
└── tasks_move_task.py      # _mt_finalize_plan / _mt_plan_review_result wired to call the generalized
                             # writer on the approve/done transition when the latest artifact is rejected (FR-001)

src/specify_cli/agent_utils/
└── status.py               # _get_wp_review_verdict / stale-verdict scan re-pointed at the same
                             # coord-authority the write lands on, for coord-topology missions (FR-003)

tests/
├── review/test_cycle.py                    # FR-001/FR-002 unit coverage; turns the two pre-existing
│                                            # red tests green (test_self_referential_feedback_source_is_rejected,
│                                            # test_new_cycle_body_never_duplicates_a_prior_cycle_file)
├── post_merge/                              # FR-001 merge-gate integration coverage (review_artifact_consistency)
└── regression/                              # new coord-topology regression for FR-003 (#2646/#2697),
                                              # mirroring test_2684_review_override_recognition.py's shape
```

**Structure Decision**: Single project (Option 1). This mission is entirely internal to the existing `spec-kitty` CLI package — no new top-level directories, no frontend/backend split, no new service boundary.

## Complexity Tracking

*No Charter Check violations identified — table intentionally empty.*

## Implementation Concern Map

> **Note**: Implementation concerns are NOT work packages and are NOT executable units.
> `/spec-kitty.tasks` translates these into executable WPs — one concern may become
> multiple WPs; multiple small concerns may merge into one WP.

### IC-01 — Approved-verdict writer and validator loosening

- **Purpose**: Generalize `create_rejected_review_cycle` into a single verdict-aware writer (operator-confirmed shape: generalize, not a new sibling function), loosen `validate_review_artifact`'s hardcoded rejected-only check to accept `approved`, and wire `move-task --to approved`/`--to done` to call the writer whenever the WP's latest artifact is `rejected`.
- **Relevant requirements**: FR-001, C-002, NFR-001, NFR-002, NFR-003
- **Affected surfaces**: `src/specify_cli/review/cycle.py`, `src/specify_cli/review/artifacts.py`, `src/specify_cli/cli/commands/agent/tasks_move_task.py`
- **Sequencing/depends-on**: none — foundational; IC-02 and IC-03 both build on the generalized writer this concern produces.
- **Risks**: Existing callers of `create_rejected_review_cycle` must keep working unchanged — a `verdict="rejected"` default parameter preserves current call sites. The commit-target-resolution path this writer runs under (`_mt_resolve_targets` / `_ensure_target_branch_checked_out` in `tasks_move_task.py`/`tasks_shared.py`) does not check out a target branch today ("respects user's current branch" per its own docstring) — Phase 0 research must determine whether this is a pre-existing latent gap the new writer simply inherits (same as the existing rejected-writer) or something that needs hardening before FR-001 ships, and whether IC-03 needs the identical fix.

### IC-02 — Feedback-source provenance guard

- **Purpose**: Refuse creating a review-cycle artifact whose feedback source is itself — by exact path or by duplicated content (e.g., a renamed copy) — a prior cycle's own artifact for the same WP. Closes #2996(b) and #990 as the identical mechanism in the same function.
- **Relevant requirements**: FR-002, NFR-001, NFR-002
- **Affected surfaces**: `src/specify_cli/review/cycle.py` (same function IC-01 generalizes)
- **Sequencing/depends-on**: IC-01 — shares the same function post-generalization; implement together or immediately after so the guard protects both verdict paths from the start.
- **Risks**: Content-based (not just path-based) duplicate detection must not false-positive on legitimately similar feedback text between independent reviews — the guard's detection boundary (exact/near-exact prior-cycle content vs. merely similar prose) needs an explicit, testable rule, not a fuzzy heuristic.

### IC-03 — Coord-topology review-artifact authority fix

- **Purpose**: Make the `agent tasks status` stale-verdict scan (`_get_wp_review_verdict`) and the rejection-transition's write agree on one canonical authority per topology, closing #2646 (stale-read) and #2697 (write duplication/split lifecycle mutation) for real.
- **Relevant requirements**: FR-003, C-001, C-003, NFR-001
- **Affected surfaces**: `src/specify_cli/agent_utils/status.py`, and whatever coord-commit path in `tasks_move_task.py`/`tasks_shared.py` currently lets a canonical write land on the coordination authority while the PRIMARY-only scan never sees it
- **Sequencing/depends-on**: IC-01 — both concerns touch commit-target/branch-authority resolution for coord-topology missions; Phase 0 research must determine whether one shared fix serves both or whether they need independently-implemented-but-coordinated fixes, per spec.md's flagged architectural dependency.
- **Risks**: Highest architectural uncertainty of the three concerns — coord-topology-specific behavior must not regress flat/single-branch missions (spec.md User Story 3, Acceptance Scenario 3). Flagged for a dedicated Phase 0 research task rather than assumed straightforward.
