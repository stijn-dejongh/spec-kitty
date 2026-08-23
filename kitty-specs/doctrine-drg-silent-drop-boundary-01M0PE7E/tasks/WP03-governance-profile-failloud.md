---
work_package_id: WP03
title: 'Governance-profile fail-loud: built-in e2e + org-tier implement (#3629 p2)'
dependencies: []
requirement_refs:
- FR-008
planning_base_branch: fix/doctrine-drg-silent-drop-boundary
merge_target_branch: fix/doctrine-drg-silent-drop-boundary
branch_strategy: Planning artifacts for this mission were generated on fix/doctrine-drg-silent-drop-boundary. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into fix/doctrine-drg-silent-drop-boundary unless the human explicitly redirects the landing branch.
subtasks:
- T013
- T014
- T015
- T016
history:
- at: '2026-08-23T00:00:00Z'
  actor: tasks
  note: WP created
agent_profile: python-pedro
authoritative_surface: src/doctrine/drg/org_pack_loader.py
create_intent:
- src/doctrine/drg/org_governance.py
- tests/doctrine/drg/migration/test_governance_scope_e2e.py
- tests/doctrine/drg/test_org_governance_failloud.py
execution_mode: code_change
owned_files:
- src/doctrine/drg/org_pack_loader.py
- src/doctrine/drg/org_governance.py
- tests/doctrine/drg/migration/test_governance_scope_e2e.py
- tests/doctrine/drg/test_org_governance_failloud.py
role: implementer
tags: []
tracker_refs: []
---

## ⚡ Do This First: Load Agent Profile

`/ad-hoc-profile-load python-pedro` (+ `spec-kitty charter context --action
implement --json`). Apply + state what you applied. Shadow venv:
`export PATH="$PWD/.venv/bin:$PATH"`.

## Objective

Make a nonexistent governance-profile `selected_*` selection fail loud on **both**
tiers. The built-in guard already exists but is only unit-tested with synthetic
edges — add an end-to-end test. The org tier has **no scope path at all** today —
implement it. This is #3629 part 2 (built-in verify-and-close + org-tier build).

## Context (from squad findings F8, F9)

- Built-in: `assert_governance_scope_edges_resolve` (`extractor.py:1406`) is wired
  into `generate_graph` (`:1574`) and raises on unresolved `selected_*` targets.
  Its tests (`test_extractor.py:1608-1653`) call it with **synthetic** edges — they
  never drive `generate_graph`. The commit message for `d8beee2761` admits this.
- Org tier: `extract_governance_profile_scope_edges` (`extractor.py:1336`) reads
  **only** built-in missions (`_missions_root`). `org_pack_loader.py` has **no**
  governance/`selected_*` handling — an org-tier typo is unread AND unguarded (a
  total no-op, not even a silent prune).

**Ownership note**: WP02 owns `extractor.py`. Keep this WP's org-tier code in
`org_pack_loader.py` (or a new `src/doctrine/drg/org_governance.py`) and NEW test
files; do not edit `extractor.py`. If the built-in guard genuinely must be touched,
coordinate/sequence after WP02.

## Subtasks

### T013 — Built-in end-to-end `generate_graph` fail-loud test  [P]
- New `tests/doctrine/drg/migration/test_governance_scope_e2e.py`.
- Build a temp doctrine root whose built-in `governance-profile.yaml` has a
  fictional `selected_*` id; assert `generate_graph(...)` raises `ValueError`
  naming `mission_type:field=id` (pins the `:1574` wiring, not just the pure
  extractor). Valid selections → no raise.

### T014 — Implement org-tier governance-profile scope extraction
- In `org_pack_loader.py` (or `org_governance.py`), read each org pack's
  governance-profile selections (mirror `_GOVERNANCE_PROFILE_SCOPE_FIELDS`) and
  mint the org-tier `scope` edges (or equivalent) so org-tier selections enter the
  merged DRG rather than being unread.
- Wire it into the org load/merge path (`load_org_pack` / `merge_three_layers`
  consumer) so org governance-profiles are actually processed.

### T015 — Org-tier fail-loud guard
- Add the org-tier analogue of `assert_governance_scope_edges_resolve`: any
  org-tier `selected_*` target that does not resolve to a minted node raises a
  triage-required error naming `mission_type:field=id`. Mirror the built-in guard's
  message shape.

### T016 — Org-tier fail-loud tests
- New `tests/doctrine/drg/test_org_governance_failloud.py`: red-first — an org pack
  whose governance-profile names a nonexistent `selected_*` id fails loud; a valid
  org-tier selection resolves and mints its scope edge with no false positive.

## Branch Strategy

Planning base + merge target: `fix/doctrine-drg-silent-drop-boundary`. Worktrees
per computed lane from `lanes.json` at implement time.

## Definition of Done

- Built-in e2e `generate_graph` raise test passes (closes #3629 p2 built-in).
- Org-tier governance-profile scope extraction implemented + wired; org-tier
  selections reach the DRG.
- Org-tier fail-loud guard raises on nonexistent selection naming the id; valid
  selections pass (no false positive). Red-first tests demonstrate both.
- `ruff` + `mypy` clean; no new suppressions. No edits to `extractor.py`.
- Targeted greens: `pytest tests/doctrine/drg/migration/test_governance_scope_e2e.py tests/doctrine/drg/test_org_governance_failloud.py -q`.

## Risks / reviewer guidance

- Scope creep: org-tier extraction is net-new; keep it minimal (parity with the
  built-in selectors), do not redesign governance-profiles.
- Reviewer: reject any "document the gap" close for the org tier — FR-008 requires
  a passing org-tier fail-loud test (C-002). Confirm no `extractor.py` edit
  (ownership vs WP02).
