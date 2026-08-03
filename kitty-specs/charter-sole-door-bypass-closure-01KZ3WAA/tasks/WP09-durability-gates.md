---
work_package_id: WP09
title: Durability gates for all five bypass categories
dependencies:
- WP01
- WP02
- WP03
- WP04
- WP05
- WP06
- WP07
- WP08
requirement_refs:
- FR-007
- NFR-001
- NFR-003
planning_base_branch: feat/charter-sole-door-bypass-closure
merge_target_branch: feat/charter-sole-door-bypass-closure
branch_strategy: Planning artifacts for this mission were generated on feat/charter-sole-door-bypass-closure. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/charter-sole-door-bypass-closure unless the human explicitly redirects the landing branch.
subtasks:
- T037
- T038
- T039
- T040
- T041
phase: Phase 3 - Durability (must run last)
history:
- at: '2026-08-03T14:10:00Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: architect-alphonso
authoritative_surface: tests/architectural/
create_intent:
- tests/architectural/test_charter_sole_door_agent_profile_repository.py
- tests/architectural/test_charter_sole_door_doctrine_service.py
- tests/architectural/test_charter_sole_door_resolver_imports.py
- tests/architectural/test_charter_sole_door_hardcoded_paths.py
- tests/architectural/test_charter_sole_door_inner_reacharound.py
execution_mode: code_change
model: ''
owned_files:
- tests/architectural/test_charter_sole_door_agent_profile_repository.py
- tests/architectural/test_charter_sole_door_doctrine_service.py
- tests/architectural/test_charter_sole_door_resolver_imports.py
- tests/architectural/test_charter_sole_door_hardcoded_paths.py
- tests/architectural/test_charter_sole_door_inner_reacharound.py
role: implementer
tags: []
task_type: implement
tracker_refs: []
---

# Work Package Prompt: WP09 – Durability gates for all five bypass categories

## ⚡ Do This First: Load Agent Profile

Use the `/ad-hoc-profile-load` skill to load `architect-alphonso` (implementer role, claude agent) before
parsing the rest of this prompt — non-vacuous gate construction is a structural-integrity concern, not a
mechanical task.

---

## ⚠️ IMPORTANT: Review Feedback

Check `review_ref` in the event log before starting. Address all feedback; log changes in the Activity Log.

---

## Objectives & Success Criteria

Ship non-vacuous, zero-tolerance architectural gates for all five closed bypass categories, so none of
WP01-08's work can silently regress on a later PR (FR-007). **This WP must run LAST** — a gate written
before the bypasses close is either vacuous (passes despite bypasses existing) or immediately red.

**Success criteria** (NFR-001, NFR-003):
- Each gate resolves the **bound qualname** of the offending construct (via import resolution, not text
  matching) — a text-only grep cannot distinguish `charter.resolver.DoctrineService(inner,
  pack_context=None)` (sanctioned) from a raw `doctrine.service.DoctrineService(...)` (forbidden), since both
  share the literal substring `DoctrineService(`.
- The `.kittify/profiles` exclusions (Gate 1) and `_doctrine_collect.py` unfiltered-mode exclusions (Gate 2)
  are keyed by **composite identity** (file + qualname + line), never a whole-file exclusion — mirroring
  `tests/architectural/test_charter_path_literal_authority.py`'s allowlist shape from the precedent mission.
- Every self-mutation proof injects its violating construct at **function-local or nested (`try`/`except`)
  scope** — matching the actual shape of the real violations found (module-level-only injection does not
  prove non-vacuity; this is the exact WP10 lesson from `doctrine-charter-split-unification-01KZ0SRB`).
- Frozen **zero-tolerance** baselines — no shrink-only allowlist, per the operator's "no exceptions"
  decision (C-002).

## Context & Constraints

- **Depends on WP01-08 — all of them.** Do not start this WP until every bypass-closure WP has landed;
  writing these gates earlier produces either false-green or false-red results.
- Read `tests/architectural/test_charter_no_specify_cli_import.py` (the WP10 precedent from the prior
  mission) for the AST-walk + self-mutation idiom, and `tests/architectural/
  test_charter_path_literal_authority.py` (the WP11 precedent) for the composite-key shrink-only-allowlist
  idiom — **this WP's allowlists are zero-tolerance, not shrink-only, but the composite-key mechanics are
  the same shape to reuse.**
- Extend `tests/architectural/test_org_activation_seam.py` and `tests/architectural/test_layer_rules.py`
  where their existing coverage is adjacent — do not re-assert what they already prove.

## Branch Strategy

- **Strategy**: lane-per-WP (normalized by `finalize-tasks`)
- **Planning base branch**: feat/charter-sole-door-bypass-closure
- **Merge target branch**: feat/charter-sole-door-bypass-closure

## Subtasks & Detailed Guidance

### Subtask T037 – Gate 1: `AgentProfileRepository` zero-tolerance

- **Purpose**: Close FR-001's category durably.
- **Steps**:
  1. AST-walk all of `src/` for `AgentProfileRepository(` construction calls, resolving each to its bound
     import.
  2. Zero-tolerance: fail on any match outside `src/charter/resolver.py`, the unified builder (WP01), and
     the two composite-key-excluded `.kittify/profiles` sites (`registry.py:48`, `profiles_cmd.py:83`) —
     excluded by exact file+line, not by filename alone.
  3. Self-mutation proof: inject a new `AgentProfileRepository(` construction at function-local scope in a
     scratch module; assert the gate fails naming the exact line.
- **Files**: `tests/architectural/test_charter_sole_door_agent_profile_repository.py` (new).
- **Parallel?**: Yes, alongside T038-T041 — each gate is independent of the others.

### Subtask T038 – Gate 2: `DoctrineService` zero-tolerance, qualname-resolving

- **Purpose**: Close FR-002/FR-008's category durably, correctly distinguishing the two classes.
- **Steps**:
  1. AST-walk all of `src/` for `DoctrineService(` construction calls; resolve each to its bound import
     (`doctrine.service.DoctrineService` vs `charter.resolver.DoctrineService`).
  2. Zero-tolerance on raw `doctrine.service.DoctrineService(` outside `src/charter/resolver.py` and the
     unified builder.
  3. The 4 `_doctrine_collect.py` unfiltered-mode sites (`charter.resolver.DoctrineService(inner,
     pack_context=None)`) are sanctioned — exclude by composite key (file+qualname+line), confirming each
     genuinely uses `pack_context=None` (not merely present in an excluded file).
  4. Self-mutation proof: inject a raw `doctrine.service.DoctrineService(` construction at function-local
     scope; assert the gate fails.
- **Files**: `tests/architectural/test_charter_sole_door_doctrine_service.py` (new).
- **Parallel?**: Yes.

### Subtask T039 – Gate 3: `doctrine.resolver` direct-import zero-tolerance

- **Purpose**: Close FR-003's category durably.
- **Steps**:
  1. Scan `src/` for `from doctrine.resolver import ...` / `import doctrine.resolver` outside
     `src/charter/**` and `src/doctrine/**`.
  2. Zero-tolerance — no exclusions expected (WP05 closed the one real consumer).
  3. Self-mutation proof: inject a direct import at function-local scope in a scratch module outside
     `src/charter/**`; assert the gate fails.
- **Files**: `tests/architectural/test_charter_sole_door_resolver_imports.py` (new).
- **Parallel?**: Yes.

### Subtask T040 – Gate 4: hardcoded missions-root path-literal zero-tolerance

- **Purpose**: Close FR-004's category durably.
- **Steps**:
  1. Scan `src/` for `Path(__file__)`-relative constructions of a missions-root-shaped path (e.g. containing
     `"doctrine"` and `"missions"` as adjacent path components) outside
     `src/doctrine/missions/repository.py` (the one promoted authority).
  2. Zero-tolerance.
  3. Self-mutation proof: inject such a literal at function-local scope; assert the gate fails.
- **Files**: `tests/architectural/test_charter_sole_door_hardcoded_paths.py` (new).
- **Parallel?**: Yes.

### Subtask T041 – Gate 5: `._inner` attribute-access zero-tolerance

- **Purpose**: Close FR-010's category durably — the escape hatch that would otherwise defeat every other
  gate in this WP.
- **Steps**:
  1. AST-walk `src/` for `._inner` attribute access on any expression, outside `src/charter/**`.
  2. Zero-tolerance.
  3. Self-mutation proof: inject `._inner` access at function-local scope in a scratch module outside
     `src/charter/**`; assert the gate fails.
  4. This gate can build on/extend WP04's narrower `test_no_inner_reacharound.py` — do not duplicate; either
     absorb that test's logic into this broader gate or have this gate import/reuse its AST-scan helper.
- **Files**: `tests/architectural/test_charter_sole_door_inner_reacharound.py` (new).
- **Parallel?**: Yes.

## Test Strategy

- `pytest tests/architectural/ -k "charter_sole_door" -v` — all 5 new gates.
- Run the FULL `tests/architectural/` suite once after all 5 land, to confirm no interaction with existing
  gates (`test_layer_rules.py`, `test_org_activation_seam.py`, `test_no_dead_doctrine_paths.py`).
- Confirm each gate's self-mutation proof actually fails when run against the mutated scratch module (not
  just "the test file exists").

## Risks & Mitigations

- **Writing a gate that only scans module-level imports/constructs** (the exact WP10 lesson). Mitigation:
  every self-mutation proof MUST inject at function-local/nested scope, and reviewers must confirm the proof
  actually reds when run, not just that a self-mutation test file exists.
- **Whole-file exclusions instead of composite-key.** Mitigation: Gates 1 and 2's exclusion lists must name
  exact (file, line) or (file, qualname) pairs — a reviewer should try adding a fake new bypass to an
  excluded file at a DIFFERENT line and confirm the gate still catches it.
- **Starting this WP before WP01-08 land.** Mitigation: check `spec-kitty agent tasks status` for WP01-08's
  completion before claiming this WP.

## Review Guidance

- Confirm every self-mutation proof was actually run and observed failing (not just written).
- Confirm no gate uses a bare text `grep`/string-match — all must resolve qualnames via AST/import
  resolution.
- Confirm the exclusion lists are composite-key, and try to defeat one by adding a fake bypass to an
  excluded file at a different line.

## Activity Log

- 2026-08-03T14:10:00Z – system – Prompt created.
