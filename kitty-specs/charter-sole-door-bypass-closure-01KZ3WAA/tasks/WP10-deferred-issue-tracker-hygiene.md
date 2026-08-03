---
work_package_id: WP10
title: Deferred-issue tracker hygiene + CHANGELOG entry
dependencies: []
requirement_refs:
- FR-011
- NFR-004
planning_base_branch: feat/charter-sole-door-bypass-closure
merge_target_branch: feat/charter-sole-door-bypass-closure
branch_strategy: Planning artifacts for this mission were generated on feat/charter-sole-door-bypass-closure. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/charter-sole-door-bypass-closure unless the human explicitly redirects the landing branch.
subtasks:
- T042
- T043
- T044
phase: Phase 3 - Durability
history:
- at: '2026-08-03T14:10:00Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
- at: '2026-08-03T15:30:00Z'
  actor: system
  action: /spec-kitty.analyze finding E1 - added T044 (CHANGELOG entry) since NFR-004 had zero task coverage across all 9 WPs
agent_profile: planner-priti
authoritative_surface: docs/plans/charter-sole-door-deferred-issues.md
create_intent:
- docs/plans/charter-sole-door-deferred-issues.md
execution_mode: planning_artifact
model: ''
owned_files:
- docs/plans/charter-sole-door-deferred-issues.md
- CHANGELOG.md
role: implementer
tags: []
task_type: implement
tracker_refs: []
---

# Work Package Prompt: WP10 – Deferred-issue tracker hygiene

## ⚡ Do This First: Load Agent Profile

Use the `/ad-hoc-profile-load` skill to load `planner-priti` (implementer role, claude agent) before parsing
the rest of this prompt — this WP is tracker/planning administration, not code.

---

## ⚠️ IMPORTANT: Review Feedback

Check `review_ref` in the event log before starting. Address all feedback; log changes in the Activity Log.

---

## Objectives & Success Criteria

Give the five confirmed-deferred issues (#2986, #3036, #3039, #3091, #3022) a durable tracker trace, per
Standing Order #8 — not just PR-description prose (FR-011). A post-plan squad delegate found the precedent
mission (`doctrine-charter-split-unification-01KZ0SRB`) already carries `issue-matrix.json` rows with
`verdict: "deferred-with-followup"` for two of these exact issues — this WP matches that established
practice for all five.

**Success criteria**: each of the 5 issues has an `issue-matrix.json` row in this mission naming the
one-line reason it's out of scope, AND an actual GitHub comment on the issue naming this mission. **Also
covers NFR-004** (`/spec-kitty.analyze` finding E1 — zero task coverage for the CHANGELOG requirement in
the original task breakdown): a `CHANGELOG.md` entry documenting the three intentional-scope items DIR-009
requires.

## Context & Constraints

- **Fully independent of code** — this WP has no dependency on WP01-09 and can run at any point, including
  in parallel with everything else.
- Read spec.md's C-003 for the exact one-line reason per issue (already researched, do not re-derive):
  - #2986 — runtime→doctrine import-ratchet's own function-local-import blind spot, 61 sites/30 files,
    different pair.
  - #3036 — doctrine-content-shippability gate contradiction, different domain.
  - #3039 — test-file reorganisation unrelated to access-path enforcement.
  - #3091 — relocate `src/doctrine/missions/` to `packs/built-in`, packaging track.
  - #3022 — extract built-in packs into `spec-kitty-packs-open`, packaging/distribution track.
- Use `gh issue comment <N> --body "..."` per the repo's GitHub tracker toolguide.

## Branch Strategy

- **Strategy**: lane-per-WP (normalized by `finalize-tasks`)
- **Planning base branch**: feat/charter-sole-door-bypass-closure
- **Merge target branch**: feat/charter-sole-door-bypass-closure

## Subtasks & Detailed Guidance

### Subtask T042 – Add `issue-matrix.json` rows + a citable docs record

- **Purpose**: A durable record of the deferral decision, both in the mission's own coordination artifact
  and in a citable docs location (this WP's declared, owned surface).
- **Steps**:
  1. For each of the 5 issues, add a row to `kitty-specs/charter-sole-door-bypass-closure-01KZ3WAA/
     issue-matrix.json` with `verdict: "deferred-with-followup"`, the issue number, and the one-line reason
     from the Context section above, matching the precedent mission's row shape exactly (read
     `kitty-specs/doctrine-charter-split-unification-01KZ0SRB/issue-matrix.json` for the exact schema before
     writing). This is a coordination-branch write, not a declared `owned_files` entry for this WP.
  2. Create `docs/plans/charter-sole-door-deferred-issues.md` — a short, citable record listing all 5 issues,
     their one-line out-of-scope reason, and a link back to this mission's spec.md §C-003 for full context.
- **Files**: `kitty-specs/charter-sole-door-bypass-closure-01KZ3WAA/issue-matrix.json` (coordination write),
  `docs/plans/charter-sole-door-deferred-issues.md` (new, this WP's owned surface).
- **Parallel?**: Yes, alongside T043.

### Subtask T043 – Post tracker comments

- **Purpose**: Make the deferral discoverable by opening the issue itself, not only by reading this
  mission's PR.
- **Steps**: For each of the 5 issues, run
  `gh issue comment <N> --repo Priivacy-ai/spec-kitty --body "..."` naming this mission
  (`charter-sole-door-bypass-closure-01KZ3WAA`) and the one-line reason it stays out of scope. Confirm the
  Tracker Ticket Assignment Rule (charter, DIR-012) does NOT apply here — these issues are not being
  implemented by this mission, only referenced, so no assignment action is needed.
  **Non-fakeable evidence requirement** (post-tasks squad correction — "a live GitHub comment" is otherwise
  unverifiable to a reviewer with no gh-cli access): paste the output of `gh issue view <N> --comments` for
  each of the 5 issues into this WP's Activity Log, showing the posted comment, before marking this WP
  complete.
- **Files**: none (GitHub API side effect only).
- **Parallel?**: Yes, alongside T042.

### Subtask T044 – Add the NFR-004 CHANGELOG entry

- **Purpose**: DIR-009 requires breaking/behaviour changes documented in `CHANGELOG.md`; NFR-004 names three
  specific items this mission must not slip past silently.
- **Steps**: Add one `CHANGELOG.md` entry (under `[Unreleased]` or the current in-progress version, matching
  the file's existing convention) stating explicitly:
  1. `charter.resolver.DoctrineService` now activation-gates all 9 charter-activatable `ArtifactKind`
     members (up from 3) plus the `mission-type` token via `resolve_mission_type_context()` — a project
     that activates a subset of a newly-gated kind's packs will see a narrower result than before this
     mission.
  2. `src/specify_cli/invocation/registry.py:48` and `src/specify_cli/cli/commands/profiles_cmd.py:83`'s
     `.kittify/profiles` construction is explicitly excluded from this mission's factory-routing work — not
     silently missed.
  3. The missions-root path consolidation (FR-004) does not claim convergence with
     `doctrine.pack_paths.built_in_dir` — that remains `#3091`'s to deliver.
- **Files**: `CHANGELOG.md`.
- **Parallel?**: Yes, alongside T042-T043.

## Test Strategy

- No automated test — this is tracker administration. Verify via the Activity Log: `gh issue view <N>
  --comments` output for each of the 5 issues must be pasted there (T043's non-fakeable evidence
  requirement), not just asserted as done. Verify T044 by reading the committed `CHANGELOG.md` entry against
  the three required items above.

## Risks & Mitigations

- **Posting a comment without a matching `issue-matrix.json` row (or vice versa).** Mitigation: do both for
  all 5 issues in the same WP pass — do not partially complete this WP.

## Review Guidance

- Confirm all 5 issues have both an `issue-matrix.json` row and a live GitHub comment.
- Confirm the one-line reasons match spec.md's C-003 exactly (no drift in the stated rationale).
- Confirm `CHANGELOG.md` names all three NFR-004 items, not a partial subset.

## Activity Log

- 2026-08-03T14:10:00Z – system – Prompt created.
