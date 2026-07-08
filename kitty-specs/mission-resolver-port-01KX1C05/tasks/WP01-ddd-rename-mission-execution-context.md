---
work_package_id: WP01
title: DDD rename ExecutionContext → MissionExecutionContext
dependencies: []
requirement_refs:
- FR-012
tracker_refs: []
planning_base_branch: feat/mission-resolver-port-2173
merge_target_branch: feat/mission-resolver-port-2173
branch_strategy: Planning artifacts for this mission were generated on feat/mission-resolver-port-2173. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/mission-resolver-port-2173 unless the human explicitly redirects the landing branch.
subtasks:
- T001
- T002
- T003
- T004
- T005
history:
- at: '2026-07-08T18:06:06+00:00'
  actor: planner
  action: created
agent_profile: python-pedro
authoritative_surface: src/mission_runtime/context.py
create_intent: []
execution_mode: code_change
owned_files:
- src/mission_runtime/context.py
- docs/adr/3.x/2026-06-22-1-mission-topology-ssot.md
- docs/adr/3.x/2026-06-03-1-execution-state-domain-model.md
role: implementer
tags: []
---

## ⚡ Do This First: Load Agent Profile

Before reading anything else, load your agent profile via `/ad-hoc-profile-load` for
`python-pedro` (implementer). Adopt its identity, governance scope, and boundaries. Then read
`kitty-specs/mission-resolver-port-01KX1C05/spec.md` (FR-012), `plan.md` (IC-00), and
`research.md` (D-10).

## Objective

Rename the frozen composite class `ExecutionContext` → `MissionExecutionContext` in
`src/mission_runtime/context.py` and everywhere it is used, so the code name matches the ubiquitous
language already used in its docstring, the `#1619` epic, and the parity test. This **also removes a
name collision** with the unrelated `class ExecutionContext(StrEnum)` in
`src/specify_cli/core/context_validation.py`. This is a **scoped bulk rename** and lands FIRST so every
downstream WP uses the corrected name.

## Hard exclusion (the whack-a-symbol trap)

**Do NOT rename `src/specify_cli/core/context_validation.py:41 class ExecutionContext(StrEnum)`** — it is a
different type. Rename ONLY the `mission_runtime.context` composite and references that resolve to it.
Verify by import origin, not by bare token match.

## Occurrence classification (scoped — apply the bulk-edit discipline)

| Category | Action |
|----------|--------|
| code_symbols | rename the composite class `ExecutionContext` → `MissionExecutionContext` |
| import_paths | update the ~12 `from mission_runtime.context import ExecutionContext` sites |
| tests_fixtures | update test references + the parity-test assertion string |
| user_facing_strings / docs | update the class docstring + the 2 ADR prose refs |
| filesystem_paths / serialized_keys / cli_commands / logs_telemetry | none |

## Subtasks

### T001 — Rename the class + docstring in `context.py`
- `src/mission_runtime/context.py:262` `class ExecutionContext:` → `class MissionExecutionContext:`.
- Update the module docstring (`:1`, `:11` already say `MissionExecutionContext` — leave those; they are now correct).
- Keep the frozen/`@dataclass(frozen=True)` semantics unchanged.

### T002 — Update the `ActionContext` alias
- `context.py:349` `ActionContext = ExecutionContext` → `ActionContext = MissionExecutionContext` (keep the transitional alias pointing at the new name; do not delete it — its own retirement is a separate track).

### T003 — Mechanical rename across importers + usages (documented out-of-map)
- Update every `from mission_runtime.context import ExecutionContext` and usage that resolves to the
  composite. Known sites (~12 imports across 20 files): `mission_runtime/resolution.py`,
  `runtime/next/runtime_bridge.py`, and the tests listed by
  `grep -rEn "\bExecutionContext\b" src tests | grep -v StrEnum`.
- **These files are owned by other WPs; this is an out-of-map mechanical rename** — record the one-line
  rationale ("WP01 codebase-wide rename FR-012") in the review notes. Because WP01 lands first and all
  other WPs depend on it (directly or via WP02), there is no parallel collision.
- Method: resolve each hit's import origin; rename only composite-typed references; leave the StrEnum.

### T004 — Update ADR prose
- `docs/adr/3.x/2026-06-22-1-mission-topology-ssot.md` and `docs/adr/3.x/2026-06-03-1-execution-state-domain-model.md`
  reference `ExecutionContext` as a canonical seam — update to `MissionExecutionContext` where they mean
  the composite (leave any reference that means the StrEnum / a different `ExecutionContext`).

### T005 — Verify (the collision is the risk)
- `grep -rn "class ExecutionContext" src` → exactly one hit remains: `core/context_validation.py` (StrEnum).
- `grep -rEn "\bExecutionContext\b" src tests | grep -v context_validation | grep -v "StrEnum"` → only the
  StrEnum's own local uses remain; no composite reference survives.
- Run the FULL `tests/architectural/` suite + `tests/architectural/test_execution_context_parity.py` +
  `tests/architectural/test_mission_runtime_surface.py` and confirm green. Run `ruff` + `mypy` clean.

## Branch Strategy

Planning happened on `feat/mission-resolver-port-2173`; that is also the merge target. The execution
worktree for this WP is allocated per computed lane from `lanes.json` at `/spec-kitty.implement`. Do not
push to `origin`.

## Definition of Done
- The composite class is `MissionExecutionContext` everywhere; the `ActionContext` alias points to it.
- The `ExecutionContext(StrEnum)` is untouched.
- Full `tests/architectural/` + parity + surface gates green; `ruff`/`mypy` clean.
- ADR prose updated.

## Risks / reviewer guidance
- **Collision**: reviewer greps `class ExecutionContext` (must be 1, the StrEnum) and spot-checks that no
  StrEnum reference was renamed.
- **Out-of-map touches**: expected and documented (FR-012 codebase rename); confirm they are pure symbol
  renames, no behavior change.
- Sonar campsite (operator standing instruction): census the touched files; fold SAFE trivia, note ADJACENT.
