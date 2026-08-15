---
work_package_id: WP08
title: Tracker toolguide + review-discipline tactic enrichments
dependencies: []
requirement_refs:
- FR-006
- FR-009
- NFR-004
- NFR-005
planning_base_branch: kitty/mission-workflow-self-doc
merge_target_branch: kitty/mission-workflow-self-doc
branch_strategy: Planning artifacts for this mission were generated on kitty/mission-workflow-self-doc. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into kitty/mission-workflow-self-doc unless the human explicitly redirects the landing branch.
subtasks:
- T017
- T018
- T019
history: []
authoritative_surface: packs/built-in/
create_intent: []
execution_mode: code_change
owned_files:
- packs/built-in/toolguides/GITHUB_TRACKER.md
- packs/built-in/toolguides/github-tracker.toolguide.yaml
- packs/built-in/tactics/architectural-gate-non-vacuity.tactic.yaml
- packs/built-in/tactics/reviewer-implementer-role-separation.tactic.yaml
- packs/built-in/tactics/canonical-source-unification.tactic.yaml
tags: []
tracker_refs: []
---

## Objective
Doctrine enrichment (standalone `packs/**` lane): the `gh` closing-keyword pitfall + three review-discipline heuristics into the tactics that own them. Keep enrichments as step/failure-mode additions (NO new `references:` → no graph regen).

## Subtasks
- **T017** `GITHUB_TRACKER.md`: a closing-keyword section + pitfall-table row — `gh`/GitHub "Closes #A,#B" links only #A; use one keyword per issue. Keep `github-tracker.toolguide.yaml` consistent; do NOT change the node `title` (a body-only edit keeps `toolguide.graph.yaml` byte-identical → no regen).
- **T018** Tactic enrichments (single `.tactic.yaml` each; heuristics as `steps`/`failure_modes`):
  - `architectural-gate-non-vacuity.tactic.yaml` += authority-parse vacuity: prove the gate READS its authority at runtime (mutate the authority in a scratch copy → gate must red; an alias/re-export defeats a census gate) — a NEW element that CROSS-REFERENCES the existing self-mutation step (don't restate), framed as distinct from the four structural elements.
  - `reviewer-implementer-role-separation.tactic.yaml` += the two-party-review-integrity rationale: never manufacture/self-certify an `approved` artifact (trips the self-approval classifier); recover by fresh independent review. Doctrine RATIONALE only — the CLI mechanics live in WP01.
  - `canonical-source-unification.tactic.yaml` += "a 'can't reuse the seam' comment is a red flag — verify the seam's real signature; parameterize the seam, don't allow-list a duplicate", LINKED to the existing Parity/Fallback failure modes.
- **T019** Gates: `.venv/bin/python -m pytest tests/architectural/test_no_dead_doctrine_paths.py -q` (new links resolve); `spec-kitty doctrine regenerate-graph --check` (byte-identical — no title change); `spec-kitty doctor doctrine --json` clean; terminology guard. If an enrichment genuinely needs a new `references:` edge, add `packs/built-in/tactic.graph.yaml` to scope + regen it — otherwise leave graphs untouched.

## Rules
Read an existing `.tactic.yaml` for the schema first. `.venv/bin/python`, never bare `uv run`.

## Done
Closing-keyword pitfall home; three tactics enriched (cross-ref, not restate); doctrine gates green.
