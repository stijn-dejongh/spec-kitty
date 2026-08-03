---
work_package_id: WP07
title: Extend factory activation-gating to 6 mechanical kinds
dependencies:
- WP01
- WP05
requirement_refs:
- FR-005
- FR-008
planning_base_branch: feat/charter-sole-door-bypass-closure
merge_target_branch: feat/charter-sole-door-bypass-closure
branch_strategy: Planning artifacts for this mission were generated on feat/charter-sole-door-bypass-closure. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/charter-sole-door-bypass-closure unless the human explicitly redirects the landing branch.
subtasks:
- T026
- T027
- T028
- T029
- T030
- T031
- T032
- T033
phase: Phase 2 - Bypass closure
history:
- at: '2026-08-03T14:10:00Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: python-pedro
authoritative_surface: tests/charter/test_resolver_activation_gating.py
create_intent:
- tests/charter/test_resolver_activation_gating.py
execution_mode: code_change
model: ''
owned_files:
- tests/charter/test_resolver_activation_gating.py
role: implementer
tags: []
task_type: implement
tracker_refs: []
---

# Work Package Prompt: WP07 – Extend factory activation-gating to 6 mechanical kinds

## ⚡ Do This First: Load Agent Profile

Use the `/ad-hoc-profile-load` skill to load `python-pedro` (implementer role, claude agent) before parsing
the rest of this prompt.

---

## ⚠️ IMPORTANT: Review Feedback

Check `review_ref` in the event log before starting. Address all feedback; log changes in the Activity Log.

---

## Objectives & Success Criteria

Extend `charter.resolver.DoctrineService` to activation-gate 6 more of the 10 doctrine-artifact kinds:
`directive`, `tactic`, `styleguide`, `toolguide`, `mission_step_contract`, `glossary_pack` (FR-005). This is
confirmed **mechanical** — `PackContext` already has a matching three-state `activated_<kind>` field for
each, and `doctrine.service.DoctrineService` already exposes a matching raw property. Copy the existing
`paradigms` property pattern 6 times.

**Success criteria**:
- All 6 kinds gated with the identical three-state semantics (`None`=catalog default /
  `frozenset()`=explicit empty opt-out / `{ids}`=filtered) already proven for `paradigms`/`procedures`/
  `agent_profiles`.
- A bare-project regression test per kind proves **equality** against the raw unwrapped service — not an
  existence check.
- WP01's builder-unification test (`test_doctrine_service_builder_unification.py`, T004) is extended to
  assert identical output across all 9 gated properties (not just the original 3).

## Context & Constraints

- Read `research.md`'s R2 finding: field names and line numbers for all 6 `PackContext.activated_<kind>`
  fields and all 6 matching `doctrine.service.DoctrineService` raw properties — use these directly, this is
  not a discovery task.
- **Depends on WP01 and WP05** (declared in frontmatter). `src/charter/resolver.py` is owned by WP01 (its
  sole declared owner, to avoid a real ownership overlap between WP01/WP05/WP07 all touching the same
  class) — T026-T031's property additions there are a small, explicitly sequenced out-of-map edit, safe
  because the dependency chain (WP01 → WP05 → WP07) guarantees this WP never runs in parallel with either.
  T033 similarly edits WP01's test file (`tests/charter/test_doctrine_service_builder_unification.py`) as a
  sequenced out-of-map extension, not a declared ownership.
- Read `contracts/charter-doctrine-service-contract.md`'s "Gated properties" and "Non-regression
  obligations" sections for the exact equality-assertion shape required.

## Branch Strategy

- **Strategy**: lane-per-WP (normalized by `finalize-tasks`)
- **Planning base branch**: feat/charter-sole-door-bypass-closure
- **Merge target branch**: feat/charter-sole-door-bypass-closure

## Subtasks & Detailed Guidance

### Subtasks T026-T031 – Add the 6 mechanical properties

For each of `directives` (T026), `tactics` (T027), `styleguides` (T028), `toolguides` (T029),
`mission_step_contracts` (T030), `glossary_packs` (T031):

- **Purpose**: Mechanical copy of the existing `paradigms` property pattern (`src/charter/resolver.py:96`).
- **Steps**:
  1. Read the exact `paradigms` property implementation (getter logic, which `PackContext.activated_*`
     field it reads, how it applies the three-state filter to `self._inner.paradigms.list_all()`).
  2. Add a new `@property` with the same structure, swapping `paradigms`/`activated_paradigms` for the
     target kind's name and `PackContext` field (e.g. `directives`/`activated_directives`).
  3. Remove the kind from the `__getattr__` unfiltered passthrough path (it should now resolve via the new
     property, not fall through).
- **Files**: `src/charter/resolver.py`.
- **Parallel?**: Yes — all 6 are independent property additions in the same file; write them together in one
  pass rather than 6 separate diffs.

### Subtask T032 – Bare-project equality regression test, all 6 kinds

- **Purpose**: Non-fakeable proof — an existence check (`assert svc.directives`) passes even if some
  directives silently leaked away; this must be equality.
- **Steps**: For a bare `PackContext` (no activated packs), assert
  `wrapped.<prop> == unwrapped_inner.<prop>` for each of the 6 new properties, per the exact shape pinned in
  `contracts/charter-doctrine-service-contract.md`'s "Non-regression obligations" section.
- **Files**: `tests/charter/test_resolver_activation_gating.py` (new).
- **Parallel?**: No — depends on T026-T031.
- **Notes**: Write this RED first (against the pre-T026-T031 code, where these properties don't exist or
  fall through unfiltered) as the ATDD contract for FR-005.

### Subtask T033 – Extend WP01's builder-unification proof to all 9 kinds

- **Purpose**: WP01's T004 deliberately scoped its proof to 3 kinds because these 6 didn't exist yet — now
  they do.
- **Steps**: Edit `tests/charter/test_doctrine_service_builder_unification.py` (from WP01) to add assertions
  for the 6 new properties alongside the original 3, completing the full 9-property identical-output proof.
- **Files**: `tests/charter/test_doctrine_service_builder_unification.py`.
- **Parallel?**: No — depends on T026-T031 (needs the 6 properties to exist) and on WP01 having landed
  first.

## Test Strategy

- `pytest tests/charter/ -v`.
- `mypy --strict src/charter/resolver.py`.

## Risks & Mitigations

- **T032 written as an existence check instead of equality.** Mitigation: re-read the pinned contract
  language; a reviewer should reject any bare-project test that doesn't assert `==` against the unwrapped
  service.
- **Forgetting T033 because it touches a file outside this WP's primary surface.** Mitigation: it's listed
  explicitly in the Subtask Index and owned_files — do not skip it because it feels like "someone else's
  test file."

## Review Guidance

- Confirm all 6 properties follow the identical structural pattern as `paradigms` — no kind gets a
  "simplified" or divergent implementation.
- Confirm T032's assertions are equality-based for every kind, not a sample.
- Confirm T033 actually extends the existing test file rather than duplicating it.

## Activity Log

- 2026-08-03T14:10:00Z – system – Prompt created.
