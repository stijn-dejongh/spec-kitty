---
work_package_id: WP01
title: Unify construction paths + lineage/mutation accessor
dependencies: []
requirement_refs:
- C-001
- FR-001
- FR-008
- FR-010
planning_base_branch: feat/charter-sole-door-bypass-closure
merge_target_branch: feat/charter-sole-door-bypass-closure
branch_strategy: Planning artifacts for this mission were generated on feat/charter-sole-door-bypass-closure. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/charter-sole-door-bypass-closure unless the human explicitly redirects the landing branch.
subtasks:
- T001
- T002
- T003
- T004
- T005
phase: Phase 1 - Foundation (construction unification)
history:
- at: '2026-08-03T14:10:00Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: python-pedro
authoritative_surface: src/charter/resolver.py
create_intent:
- tests/charter/test_doctrine_service_builder_unification.py
- tests/charter/test_doctrine_service_lineage_accessor.py
execution_mode: code_change
model: ''
owned_files:
- src/charter/resolver.py
- src/charter/doctrine_service_builder.py
- src/specify_cli/doctrine_service_factory.py
- src/specify_cli/charter_runtime/lint/checks/org_layer.py
- src/specify_cli/cli/commands/charter/generate.py
- tests/charter/test_doctrine_service_builder_unification.py
- tests/charter/test_doctrine_service_lineage_accessor.py
role: implementer
tags: []
task_type: implement
tracker_refs: []
---

# Work Package Prompt: WP01 – Unify construction paths + lineage/mutation accessor

## ⚡ Do This First: Load Agent Profile

Use the `/ad-hoc-profile-load` skill to load the agent profile specified in the frontmatter, and behave
according to its guidance before parsing the rest of this prompt.

- **Profile**: `python-pedro`
- **Role**: `implementer`
- **Agent/tool**: `claude`

If no profile is specified, run `spec-kitty agent profile list` and select the best match for this work
package's `task_type` and `authoritative_surface`.

---

## ⚠️ IMPORTANT: Review Feedback

**Read this first if you are implementing this task!**

- **Has review feedback?**: Check the `review_ref` field in the event log (via `spec-kitty agent status` or
  the Activity Log below).
- **You must address all feedback** before your work is complete.
- **Report progress**: As you address each feedback item, update the Activity Log explaining what you changed.

---

## Objectives & Success Criteria

This WP is the **foundation** every other WP in this mission builds on. Two things must exist before any
call site can be migrated:

1. **One unified builder function** — `specify_cli.doctrine_service_factory.build_activation_aware_doctrine_service`,
   `charter.doctrine_service_builder._build_activation_aware_doctrine_service`, and the inline "build raw,
   conditionally wrap" pattern repeated in `org_layer.py:244,275` and `generate.py:56` collapse onto one
   function.
2. **A new public accessor** on `charter.resolver.DoctrineService` for lineage/mutation-capable
   `AgentProfileRepository` access (`register_overlay()`, `get_ancestors()`, `resolve_profile()`) — the
   filtered `agent_profiles` property cannot support these; four call sites across WP01-04 need it.

**Success criteria** (FR-008, C-001, contracts/charter-doctrine-service-contract.md):
- Exactly one function builds an activation-aware `DoctrineService`; `org_layer.py`/`generate.py` call it
  instead of reimplementing the pattern inline.
- `org_layer.py:252-253`'s `except ImportError: pass` no longer silently returns an unwrapped service.
- The new accessor's two semantics (below) are implemented exactly as pinned — not re-derived.
- A regression test proves the unified builder returns identical output for both former call sites' inputs.

## Context & Constraints

- Read `research.md`'s "D3" and "R5" sections and `contracts/charter-doctrine-service-contract.md`'s
  "Lineage/mutation accessor semantics" section (pinned by the post-plan squad) — **do not re-derive these
  semantics**, implement against the text.
- Read `contracts/mission-type-and-builder-contracts.md`'s "Unified builder contract" section for the exact
  `active_languages`/`org_roots` resolution rule.
- Single canonical authority (charter governing principle): do not invent a second factory or a second
  builder — extend `charter.resolver.DoctrineService` and unify onto one builder function.
- Supporting docs: `.kittify/charter/charter.md`, `kitty-specs/charter-sole-door-bypass-closure-01KZ3WAA/{plan.md,research.md,data-model.md,contracts/}`.

## Branch Strategy

- **Strategy**: lane-per-WP (normalized by `finalize-tasks`)
- **Planning base branch**: feat/charter-sole-door-bypass-closure
- **Merge target branch**: feat/charter-sole-door-bypass-closure

> These fields are populated automatically by `spec-kitty agent mission tasks`. Do NOT change them manually
> unless you are certain the branch topology has changed.

## Subtasks & Detailed Guidance

### Subtask T001 – Pin and implement the lineage/mutation accessor

- **Purpose**: Give `projection.py:84`, `runtime_bridge_io.py:576`, `registry.py:64`, and
  `org_profiles.py:117` (WP02/WP04) one shared, public way to reach mutation/lineage operations without
  reaching into `._inner`.
- **Steps**:
  1. Add a public method/property to `charter.resolver.DoctrineService` (e.g. `agent_profile_repository`)
     that returns the raw, lineage-capable `AgentProfileRepository` instance.
  2. Implement per the two pinned semantics in `contracts/charter-doctrine-service-contract.md`:
     - `register_overlay()` mutates the underlying repository's lineage graph; it does **not** create a way
       to read an unfiltered profile through the gated `agent_profiles` property afterward — the property's
       three-state filter still applies on every read.
     - `resolve_profile()`'s `specializes_from` lineage traversal reads through the **raw** repository (not
       re-wrapped) — matching the existing precedent at `resolver.py:402-413`'s
       `resolve_governance_for_profile`.
  3. The accessor returns the raw repository object directly; it is a second, explicitly-named entry point,
     not a widening of `agent_profiles`'s return type.
- **Files**: `src/charter/resolver.py`.
- **Parallel?**: No — T002-T003 depend on this landing in the same module first.
- **Notes**: This is the trickiest subtask in the WP because the two semantics have no default — they were
  pinned specifically because an implementer guessing wrong here breaks WP02/WP04's migrations silently.

### Subtask T002 – Unify the two named builder functions

- **Purpose**: Close the C-001 violation: two "canonical" builders with silently different output.
- **Steps**:
  1. Read both `specify_cli.doctrine_service_factory.build_activation_aware_doctrine_service` and
     `charter.doctrine_service_builder._build_activation_aware_doctrine_service` in full.
  2. Pick the *fuller* behaviour on each axis, per `contracts/mission-type-and-builder-contracts.md`:
     - Always compute `active_languages=infer_repo_languages(repo_root)` and pass it to the inner
       `DoctrineService` construction (the `charter` builder's behaviour — the `specify_cli` builder
       currently omits this).
     - Always self-resolve `org_roots` via `resolve_org_roots` (the `specify_cli` builder's behaviour — the
       `charter` builder currently defaults to no org layer when the caller omits the argument).
  3. Collapse to one function; make the other either delete-and-repoint-callers or a thin re-export of the
     first — never two independent implementations.
- **Files**: `src/charter/doctrine_service_builder.py`, `src/specify_cli/doctrine_service_factory.py`.
- **Parallel?**: No — depends on T001 only in that both touch the factory module; can be done in the same
  commit.
- **Notes**: Do not guess at the "right" behaviour on either axis — the contract file states which side wins
  and why. Grep for all existing callers of both functions before changing signatures.

### Subtask T003 – Retarget the inline construction sites; fix the fail-open bug

- **Purpose**: Close the 3 additional construction sites the post-plan squad found, and their fail-open bug.
- **Steps**:
  1. `org_layer.py:244-253` and `:275` (`_build_org_aware_service`, `_build_built_in_only_service`): replace
     the inline `inner = DoctrineService(...)` + `try: ... except ImportError: pass` + `return inner` pattern
     with a call to the unified builder from T002.
  2. The unified builder must **fail closed** on any construction error — no branch of this WP may return a
     silently-unwrapped raw `DoctrineService` when `pack_context is not None` was requested. Raise or
     propagate the error instead of the current `pass`.
  3. `generate.py:56`: replace the inline construction + wrap with a call to the unified builder.
- **Files**: `src/specify_cli/charter_runtime/lint/checks/org_layer.py`,
  `src/specify_cli/cli/commands/charter/generate.py`.
- **Parallel?**: Yes, alongside T001 (different files) once T002's builder signature is settled.
- **Notes**: `org_layer.py`'s two functions have subtly different signatures (`org_roots` param present in
  one, absent in the other) — read both before assuming they retarget identically.

### Subtask T004 – Regression test: unified builder identical output (scoped to today's 3 kinds)

- **Purpose**: Prove T002's unification actually closed the divergence — non-fakeable per NFR (equality, not
  "some result returned").
- **Steps**:
  1. Construct the unified builder with the same `repo_root`, once exercising each former call site's
     original argument shape (with/without explicit `org_roots`; with/without a language-diverse project
     fixture for `active_languages`).
  2. Assert identical output for `paradigms`, `procedures`, `agent_profiles` (the 3 kinds gated today) AND
     the builder's `active_languages`/`org_roots` resolution.
  3. **Do NOT** write this assertion against all 9 gated properties — 6 of them don't exist until WP07
     (FR-005) lands. WP07's T033 extends this exact test file to the full 9-property surface later; this
     subtask's job is the 3-kind baseline proof only.
- **Files**: `tests/charter/test_doctrine_service_builder_unification.py` (new).
- **Parallel?**: No — depends on T002/T003.
- **Notes**: This is the ATDD red-first test for FR-008 — write it failing (against the pre-unification two
  builders) before implementing T002, then watch it go green.

### Subtask T005 – ATDD test: accessor semantics

- **Purpose**: Prove T001's two pinned semantics hold, not just that the accessor exists.
- **Steps**:
  1. Test 1 (mutation does not leak through filter): call `register_overlay()` with a non-activated profile
     via the accessor; assert the gated `agent_profiles` property still excludes it.
  2. Test 2 (lineage traversal reads raw): construct a profile with `specializes_from` pointing at a
     deactivated parent; call `resolve_profile()` via the accessor; assert it successfully composes lineage
     from the deactivated parent (matching `resolve_governance_for_profile`'s existing precedent behaviour).
- **Files**: `tests/charter/test_doctrine_service_lineage_accessor.py` (new).
- **Parallel?**: No — depends on T001.
- **Notes**: Write both tests RED first (they should fail against a `charter.resolver.DoctrineService`
  without the accessor), then implement T001 to make them pass — this is the ATDD contract (charter C-011).

## Test Strategy

- Run `pytest tests/charter/ -v` after each subtask; this WP's owned test files are new, so there's no
  pre-existing suite to regress against within `tests/charter/`.
- Run `mypy --strict src/charter/resolver.py src/charter/doctrine_service_builder.py
  src/specify_cli/doctrine_service_factory.py` — zero new issues (NFR-002).
- Do NOT run the full `pytest tests/` suite for this WP — targeted surfaces only, per charter testing
  guidance.

## Risks & Mitigations

- **Guessing the accessor semantics instead of reading the pinned contract.** Mitigation: the contract file
  is the source of truth; if it seems ambiguous, that is itself a finding to report, not a decision to make
  silently.
- **Retargeting `org_layer.py`'s two functions identically when their signatures differ.** Mitigation: read
  both call sites in full before writing the retarget; write T003's fix as two separate, reviewed diffs if
  the signatures genuinely diverge.
- **Writing T004 against all 9 properties instead of 3.** Mitigation: re-read this prompt's T004 section —
  the scoping is deliberate and matches the plan's IC-01/IC-04 sequencing fix.

## Review Guidance

- Confirm T004's test asserts equality (`==`), not existence, across the 3 kinds AND the builder kwargs.
- Confirm zero remaining direct constructions of the raw `DoctrineService` at `org_layer.py`/`generate.py`
  (grep for `doctrine.service.DoctrineService(` in both files — should be gone).
- Confirm the `except ImportError: pass` shape no longer exists in `org_layer.py`.
- Confirm the accessor's two semantics are tested as written in T005, not simplified.

## Activity Log

> **CRITICAL**: Activity log entries MUST be in chronological order (oldest first, newest last).

- 2026-08-03T14:10:00Z – system – Prompt created.
