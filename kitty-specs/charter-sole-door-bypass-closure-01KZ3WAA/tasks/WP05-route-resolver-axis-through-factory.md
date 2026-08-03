---
work_package_id: WP05
title: Route the template/command resolver axis through the factory
dependencies:
- WP01
requirement_refs:
- FR-003
planning_base_branch: feat/charter-sole-door-bypass-closure
merge_target_branch: feat/charter-sole-door-bypass-closure
branch_strategy: Planning artifacts for this mission were generated on feat/charter-sole-door-bypass-closure. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/charter-sole-door-bypass-closure unless the human explicitly redirects the landing branch.
subtasks:
- T018
- T019
- T020
- T021
phase: Phase 2 - Bypass closure
history:
- at: '2026-08-03T14:10:00Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: architect-alphonso
authoritative_surface: src/charter/template_resolver.py
create_intent:
- tests/charter/test_resolver_tier_axis_via_factory.py
execution_mode: code_change
model: ''
owned_files:
- src/charter/template_resolver.py
- src/specify_cli/runtime/resolver.py
- tests/charter/test_resolver_tier_axis_via_factory.py
role: implementer
tags: []
task_type: implement
tracker_refs: []
---

# Work Package Prompt: WP05 – Route the template/command resolver axis through the factory

## ⚡ Do This First: Load Agent Profile

Use the `/ad-hoc-profile-load` skill to load `architect-alphonso` (implementer role, claude agent) before
parsing the rest of this prompt — this WP is a structural seam change, not a mechanical swap.

---

## ⚠️ IMPORTANT: Review Feedback

Check `review_ref` in the event log before starting. Address all feedback; log changes in the Activity Log.

---

## Objectives & Success Criteria

`CharterTemplateResolver`'s one real caller (`specify_cli/runtime/resolver.py`'s tier-5 routing) currently
imports `doctrine.resolver` directly. Give `charter.resolver.DoctrineService` resolution methods so no
consumer outside `src/charter/**` needs that import (FR-003).

**This WP's scope was corrected by the post-plan squad — read this before starting:**
- `src/charter/resolution.py` and `src/charter/context_renderers/template_include.py` are **NOT** in scope —
  both import only the `ResolutionResult`/`ResolutionTier` *types*, sanctioned by an existing facade
  contract, not resolution calls. Do not touch them.
- `doctrine.template_catalog.resolve_template_by_id` (5 importers) and `specify_cli/runtime/resolver.py`'s
  tier-1-4 reimplementation are explicitly **deferred debt**, named but out of this WP's blast radius. Do
  not fold them in.
- `doctrine/resolver.py`'s tier functions (`_resolve_asset`, `resolve_mission`) **stay where they are** —
  moving them fights the module's own documented rationale (`charter → doctrine` is the sanctioned import
  direction). Only the entry point moves.

## Context & Constraints

- Read `research.md`'s R6 finding in full — it names the exact precedent
  (`specify_cli/runtime/resolver.py`'s existing tier-5 routing pattern) to extend, and the exact things to
  leave alone.
- **Real design work required**: `CharterTemplateResolver`'s one real caller currently uses a cached
  (`lru_cache`), `missions_root`-keyed construction (`from_missions_root(...)`); the factory is built from
  `repo_root` via the unified builder (WP01). T019 resolves this mismatch explicitly — do not improvise a fix
  mid-implementation without documenting the chosen mapping.
- **Depends on WP01** (declared in frontmatter) — not just for the unified builder, but because T018 adds
  methods to `src/charter/resolver.py`, which WP01 already owns and edits first. `src/charter/resolver.py`
  is **not** in this WP's `owned_files` (WP01 is its sole declared owner, to avoid a real ownership overlap)
  — T018's edit there is a small, explicitly sequenced out-of-map addition, permitted because the
  dependency on WP01 guarantees it runs after WP01's lane, never in parallel with it.

## Branch Strategy

- **Strategy**: lane-per-WP (normalized by `finalize-tasks`)
- **Planning base branch**: feat/charter-sole-door-bypass-closure
- **Merge target branch**: feat/charter-sole-door-bypass-closure

## Subtasks & Detailed Guidance

### Subtask T018 – Add resolution methods to `charter.resolver.DoctrineService`

- **Purpose**: Give the factory a public surface for the 5-tier axis, mirroring `CharterTemplateResolver`'s
  current public methods.
- **Steps**:
  1. Read `doctrine/resolver.py::_resolve_asset` (5 tiers) and `resolve_mission` (4 duplicated tiers) and
     `CharterTemplateResolver`'s current method signatures.
  2. Add matching methods to `charter.resolver.DoctrineService` (e.g. `resolve_command_template`,
     `resolve_content_template`, `resolve_mission_config` — name them to match `CharterTemplateResolver`'s
     existing API so the retarget in T020 is close to 1:1) that call into `doctrine.resolver`'s functions
     internally.
  3. These new methods are explicitly **ungated** by design (the 5-tier axis has no activation concept
     today, per spec.md) — do not attempt to add activation filtering here; that would conflate FR-003 with
     FR-005's separate scope. Note this explicitly in a docstring/comment on the new methods.
- **Files**: `src/charter/resolver.py`.
- **Parallel?**: No — T020 depends on this.

### Subtask T019 – Resolve the construction-contract mismatch

- **Purpose**: `_charter_template_resolver_for()` in `runtime/resolver.py` is `lru_cache`d and keyed on a
  `missions_root` string; `charter.resolver.DoctrineService` needs a `repo_root`. Design the mapping now.
- **Steps**: Either (a) resolve `repo_root` at the same call site `missions_root` is currently resolved from
  (check what upstream context is available there), or (b) add a `repo_root`-equivalent construction path.
  Document the chosen mapping in a comment at the call site — this is a real design decision, not a detail
  to leave implicit.
- **Files**: `src/specify_cli/runtime/resolver.py`.
- **Parallel?**: No — depends on T018's method shapes being settled.

### Subtask T020 – Retarget `CharterTemplateResolver`

- **Purpose**: Make the one real caller stop importing `doctrine.resolver` directly.
- **Steps**: Either turn `CharterTemplateResolver` into a thin delegating shim to T018's new factory methods,
  or retire it and have `_charter_template_resolver_for()` construct `charter.resolver.DoctrineService`
  directly (per T019's resolved mapping) and call the new methods. Pick whichever is the smaller diff given
  T019's actual design; state which you picked and why in the Activity Log.
- **Files**: `src/charter/template_resolver.py`, `src/specify_cli/runtime/resolver.py`.
- **Parallel?**: No — depends on T018, T019.

### Subtask T021 – Regression test: tier resolution unchanged

- **Purpose**: Prove the retarget didn't change resolution behaviour.
- **Steps**: For each of the 5 tiers (OVERRIDE, LEGACY, GLOBAL_MISSION, GLOBAL, PACKAGE_DEFAULT), assert the
  factory-routed resolution returns the identical result the old direct `doctrine.resolver` call would have,
  on the same fixture project.
- **Files**: `tests/charter/test_resolver_tier_axis_via_factory.py` (new).
- **Parallel?**: No — depends on T020.

## Test Strategy

- `pytest tests/charter/ tests/specify_cli/runtime/ -v`.
- `mypy --strict src/charter/resolver.py src/charter/template_resolver.py src/specify_cli/runtime/resolver.py`.

## Risks & Mitigations

- **Moving `doctrine/resolver.py`'s tier functions instead of adding an entry point.** Mitigation: re-read
  this prompt's Objectives section — this is explicitly forbidden; the tier functions stay put.
- **Silently pulling in `template_catalog` or `runtime/resolver.py`'s tier-1-4 reimplementation.** Mitigation:
  if fixing T019/T020 seems to require touching either, stop and report — that's scope creep beyond this
  WP's boundary, not a natural extension.

## Review Guidance

- Confirm no import of `doctrine.resolver` remains outside `src/charter/**` after this WP (excluding the
  explicitly-out-of-scope `template_catalog` axis).
- Confirm `doctrine/resolver.py` itself is untouched (diff should show zero changes to that file).
- Confirm T019's chosen mapping is documented, not silently invented.

## Activity Log

- 2026-08-03T14:10:00Z – system – Prompt created.
