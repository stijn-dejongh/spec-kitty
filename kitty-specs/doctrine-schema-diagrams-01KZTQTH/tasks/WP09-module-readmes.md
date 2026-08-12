---
work_package_id: WP09
title: Per-module pointer-only READMEs + structural lint (LAST, abandonable)
dependencies:
- WP05
- WP06
- WP07
requirement_refs:
- C-005
- FR-005
planning_base_branch: feat/doctrine-schema-diagrams-impl
merge_target_branch: feat/doctrine-schema-diagrams-impl
branch_strategy: Planning artifacts for this mission were generated on feat/doctrine-schema-diagrams-impl. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/doctrine-schema-diagrams-impl unless the human explicitly redirects the landing branch.
subtasks:
- T031
- T032
- T033
- T034
phase: Phase 5 - Legibility
history:
- at: '2026-08-12T16:41:10Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: scribe-sally
authoritative_surface: src/doctrine/
create_intent:
- tests/docs/test_module_readme_lint.py
execution_mode: code_change
model: ''
owned_files:
- src/doctrine/**/README.md
- tests/docs/test_module_readme_lint.py
role: documentarian
tags: []
task_type: implement
tracker_refs: []
---

# Work Package Prompt: WP09 – Per-module pointer-only READMEs + lint

## ⚡ Do This First: Load Agent Profile

Use `/ad-hoc-profile-load` to load `scribe-sally` (documentarian) and behave per its guidance first.

---

## Objectives & Success Criteria

Bridge each doctrine source module to its canonical docs with a **pointer-only** `README.md` — no copied
schema/field content. **This is the LAST, decoupled, abandonable WP** — it must never block mission merge.

**Definition of Done:**

1. Each covered `src/doctrine/**` module has a `README.md` with: a one-line description + resolving links
   to (a) its **doctrine-kinds entry**, (b) its **schema diagram** (WP05–WP07 — in-mission targets that
   always resolve), and (c) opportunistically the **owning domain plan** (doctrine-charter is on `main`;
   others may not exist yet — link only if the target resolves).
2. Existing READMEs (~17) are **extended, not clobbered**.
3. A structural lint (`tests/docs/test_module_readme_lint.py`) enforces pointer-only by machine: a length
   cap + forbid field-table markers (e.g. schema/field pipe-tables) — so no README recreates the drift
   surface C-005 forbids.
4. All README links resolve **in-mission** (no dependence on an external merge); lint green.

## Context & Constraints

- **Source of truth**: spec FR-005 / C-005, [research.md](../research.md) (D5), [plan.md](../plan.md) IC-05.
- **Independently landable**: fallback links point at in-mission targets (the doctrine-kinds entry + the
  schema diagram) so FR-005's link check never reds on an external merge. The "owning domain plan" link
  is **opportunistic** — include only if the target resolves now.
- **Depends on WP05–WP07** for the link targets (the diagrams + kinds entries must exist).
- **~17 modules already have READMEs** → EXTEND-heavy. Read each before editing; preserve existing content.
- Charter: pointers not copies; docs mirror shipped behaviour; audience-oriented (agent + maintainer).

## Subtasks & Detailed Guidance

### Subtask T031 – Inventory + mapping

- **Steps**: enumerate `src/doctrine/**` modules (and domain-relevant ones). For each, determine its
  doctrine-kinds entry anchor + the schema diagram it maps to (WP05 overview / WP06 DRG / WP07
  mission-type / per-kind), and whether an owning domain plan exists yet. Produce the module→target map.
- **Files**: (working note; the map drives T032). ~17 existing READMEs are the baseline.

### Subtask T032 – Extend/create pointer-only READMEs

- **Steps**: for each module, create or **extend** `README.md` with: one-line purpose; a "Canonical docs"
  link list (doctrine-kinds entry + schema diagram, both in-mission); optional owning-plan link. **No
  field tables, no copied schema.** Keep each README short (well under the lint cap).
- **Files**: `src/doctrine/**/README.md`.

### Subtask T033 – Structural pointer-only lint

- **Steps**: `tests/docs/test_module_readme_lint.py` walks the covered READMEs and asserts: (a) length ≤
  cap (e.g. ≤ 40 lines / ≤ 2 KB — pick a defensible cap and justify it); (b) NO field-table markers (a
  markdown pipe-table whose header looks like a schema/field listing); (c) required links present and
  in-mission-resolvable. ATDD RED-first for the lint rules.
- **Files**: `tests/docs/test_module_readme_lint.py`.

### Subtask T034 – Green + link resolution

- **Steps**: run the lint; fix READMEs until green; confirm every link resolves against the in-mission
  tree (no external-merge dependency).

## Branch Strategy

- **Strategy**: merge back into `feat/doctrine-schema-diagrams-impl`.
- **Planning base branch**: `feat/doctrine-schema-diagrams-impl`
- **Merge target branch**: `feat/doctrine-schema-diagrams-impl`

## Test Strategy

- `python3 -m pytest tests/docs/test_module_readme_lint.py -q`.
- Link-resolution check runs against in-mission targets only.

## Risks & Mitigations

- **Clobbering existing READMEs** → data loss. Mitigation: read + extend; diff-review each.
- **Linking a not-yet-existing plan** → link red. Mitigation: opportunistic only; fallback to in-mission
  targets that always resolve.
- **Copying schema into a README** → new drift surface (C-005). Mitigation: the lint forbids field-tables.
- **Scope creep across 17+ modules** → this WP is abandonable; if time-boxed, land the lint + a covered
  subset and record the remainder as a tracked follow-up (never block merge on it).

## Review Guidance

- Confirm READMEs are pointer-only (lint enforces); no copied schema/field content.
- Confirm existing READMEs were extended, not overwritten.
- Confirm all links resolve in-mission.
- Reviewer ≠ implementer.

## Activity Log

> Append newest entries at the END, chronological.
