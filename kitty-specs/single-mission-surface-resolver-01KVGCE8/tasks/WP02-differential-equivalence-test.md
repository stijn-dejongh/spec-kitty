---
work_package_id: WP02
title: Differential equivalence test (the deletion safety gate)
dependencies: []
requirement_refs:
- FR-002
tracker_refs: []
planning_base_branch: feat/single-mission-surface-resolver
merge_target_branch: feat/single-mission-surface-resolver
branch_strategy: Planning artifacts for this mission were generated on feat/single-mission-surface-resolver. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/single-mission-surface-resolver unless the human explicitly redirects the landing branch.
subtasks:
- T005
- T006
- T007
- T008
agent: claude
history:
- at: '2026-06-19T17:06:54Z'
  actor: claude
  note: WP authored from plan IC-05 (FR-002, the C-004 deletion gate).
agent_profile: python-pedro
authoritative_surface: tests/missions/
create_intent:
- tests/missions/test_surface_resolution_equivalence.py
execution_mode: code_change
model: claude-opus-4-8
owned_files:
- tests/missions/test_surface_resolution_equivalence.py
role: implementer
tags: []
---

## ⚡ Do This First: Load Agent Profile

Load `python-pedro` (`src/doctrine/agent_profiles/built-in/python-pedro.agent.yaml`); acknowledge its initialization declaration.

## Objective

Build the **differential equivalence test** that feeds the same `(slug, mid8, topology)` matrix to every mission-surface resolution entry point and asserts each returns an **identical directory OR identical typed error**. This is the C-004 **deletion safety gate**: no duplicate resolver may be deleted (WP06/WP07) until the relevant cells are green. (IC-05; FR-002, NFR-003)

## Context

- Entry points to compare: `_read_path_resolver.resolve_mission_read_path` + `primary_feature_dir_for_mission`, `coordination/surface_resolver.resolve_status_surface_with_anchor`, `status/aggregate.MissionStatus.load`/`_resolve_read_dir`, `mission_runtime/resolution` boundary.
- The test goes **RED initially** on the known divergences (that's the point — it documents them); WP03/WP04/WP05/WP06 fixes flip cells green. Mark the known-RED cells with the FR/WP that closes each (xfail-with-reason or a documented expected-divergence list — NOT a silent skip).

## Subtasks

### T005 — Matrix fixtures
- Build fixtures for the topology states (per data-model.md): `no-coord`, `coord-fresh`, `coord-behind`, `coord-empty` (materialized-but-empty), `coord-deleted`; × handle classes `bare-slug`, `<slug>-<mid8>`, `ambiguous-mid8`. Use realistic on-disk shapes (real worktree/registry layout — no toy slugs).

### T006 — Differential assertion (spelled-out shapes — NO truthiness)
- For each (topology, handle) cell, call every entry point; assert agreement with these EXACT shapes (a too-lenient assertion voids the whole gate):
  - dirs: `resolved_a.resolve() == resolved_b.resolve()` (path equality, NOT "both non-None").
  - errors: `type(exc_a) is type(exc_b) and exc_a.error_code == exc_b.error_code` (same class AND same code, NOT "both raise something").
- A disagreement is a recorded divergence (the gate). **Forbidden**: `assert a and b`, `is not None`-only checks, `pytest.skip(...)` anywhere in the module (a skip hides a divergence). Use `xfail` only.

### T007 — Cover all input classes
- MUST include `coord-empty` (→ expected `STATUS_READ_PATH_NOT_FOUND` post-FR-006), `coord-deleted` (→ `COORDINATION_BRANCH_DELETED`), `ambiguous-mid8` (→ `MISSION_AMBIGUOUS_SELECTOR` post-FR-008), the `<slug>-<mid8>` handle class (the FR-009/T1 divergence class — a missing column would hide T1's false-green), AND the **no-coord create→first-write** window (→ PRIMARY, NOT a hard-fail; distinct from coord-empty — this is the WP04 T016 contract).

### T008 — Mark initially-RED cells with `xfail(strict=True)`
- Cells that diverge today (e.g. ambiguous-mid8: aggregate silent-picks vs resolver raises; mid8-handle divergence) → `@pytest.mark.xfail(strict=True, reason="closed by WP04/FR-008")`. `strict=True` is mandatory: an xfail cell that *unexpectedly passes* then FAILS the suite, catching a premature green / a delete-before-equivalence. As each fix lands, the closing WP removes its xfail. Document the expected-green-by-WP map in the test module docstring. (WP06's DoD asserts **zero `xfail` markers remain** before the collapse — that is the gate's CI teeth.)

## Branch Strategy
Planning/base + merge target: `feat/single-mission-surface-resolver`. Worktree per lane.

## Definition of Done
- [ ] Differential test covers the full (topology × handle) matrix incl. coord-empty, coord-deleted, ambiguous-mid8, `<slug>-<mid8>`, AND no-coord create→first-write (→ primary).
- [ ] Assertions use the exact shapes: `dir.resolve() == dir.resolve()` / `type is type and error_code == error_code` (NOT truthiness). No `pytest.skip` in the module.
- [ ] Initially-RED cells are `xfail(strict=True)`-with-WP-reason (no silent skips); the docstring maps cell→closing WP.
- [ ] ruff + mypy clean; the test runs (green on the cells already equivalent, strict-xfail on the rest).

## Risks / Reviewer guidance
- **Risk**: a too-lenient assertion (truthiness / "both non-None") or a `skip` that passes under divergence — the entire C-004 deletion gate is then worthless. The reviewer must confirm the exact assertion shapes and `strict=True`.
- **Reviewer**: grep the module for `assert .* and `, `is not None`, `skip(`, and `xfail(` without `strict` — any hit blocks approval. Confirm the matrix has the `<slug>-<mid8>` column (else FR-009 can false-green later); confirm coord-empty expects the hard-fail while no-coord create→first-write expects primary.
