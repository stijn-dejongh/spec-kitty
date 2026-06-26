---
description: "Work package task list — coord-read-residuals merge/lanes + identity routing (#2185 + #2186)"
---

# Work Packages: Coord-Read Residuals — Merge/Lanes + Identity Routing

**Mission**: `coord-read-residuals-merge-lanes-and-identity-routing-01KW2M8V`
**Branch**: `mission/coord-read-residuals-2185-2186` | **Spec**: [spec.md](./spec.md) | **Plan**: [plan.md](./plan.md) | **Research**: [research.md](./research.md)

Routes the PRIMARY-partition reads that still resolve through coord-aware resolvers (landing on the empty `-coord` husk post-#2106) onto the existing read-path seam. **Lane A (#2185)** = `merge/`/`lanes/`/`core/worktree_topology` reads of `lanes.json`/`tasks/`/`meta.json`. **Lane B (#2186)** = command-layer identity/type reads + a net-new identity-read scan arm.

**Tests**: required (NFR-004 integration-over-stubs; gate self-tests).

## ⚠️ C-SEQ landing precondition (read before implementing)

This mission **lands after** the implement-loop sibling (`implement-loop-coord-authority-completion-01KW2E7A`). Before implementing Lane A:
1. **Rebase** this branch onto post-implement-loop-merge `main`.
2. **Re-resolve every line citation** below against the merged tree (the sibling rewrites functions that contain some Lane B legs; Lane A files are C-009-protected so their lines are stable).
3. **FR-011 preflight** (T009): assert the `_DIR_READ_KNOWN_RESIDUALS` set on the rebased base actually contains the #2185 pins before any Lane A drain — otherwise the drain is a vacuous no-op.

Lane B is **self-contained** (its identity arm is net-new, not inherited) and is not blocked on the sibling except for re-resolving the `workflow.py` citations.

## Ownership / lane note

**WP01 owns `tests/architectural/test_gate_read_literal_ban.py`** (the dir-read ratchet + the new identity arm) and `tests/architectural/test_resolution_authority_gates.py` (the canonicalizer floor). The Lane A routing WPs (**WP02, WP03**) each **remove their own #2185 pins** from that file in the same commit they route (FR-008) — a rationale-backed out-of-map edit — so WP01 → WP02 → WP03 form a **sequential chain (one lane)** to avoid a shared-file race. WP04 (integration proof) depends on the routed code; WP05 is cross-cutting close-out.

**C-009-mirror:** never edit the implement-loop ROUTE surface (`cli/commands/agent/tasks.py`, the `workflow.py` route legs, `tasks_dependency_graph.py`, `workspace/context.py`, …) or the `scripts/tasks/` legacy reader (#2167). Lane B touches only the **owned identity legs** in `workflow.py`/`implement.py`. Never edit `_read_path_resolver` internals (C-002) and never remove `candidate_feature_dir_for_mission` (C-005 STATUS primitive).

## Subtask Index

| ID | Description | WP | Parallel |
|----|-------------|----|----------|
| T001 | Build the `cli/commands/`-scoped identity-read scan arm (flag `resolve_mission_identity`/`get_mission_type` whose dir arg is coord-aware-resolved without a primary fold) | WP01 | |
| T002 | Synthetic-AST non-vacuity self-test for the arm (pre-fix snippet flagged; routed snippet not flagged) | WP01 | [P] |
| T003 | Emit the per-site ROUTE/KEEP/owned-by-implement-loop table (cross-check vs sibling ROUTE+KEEP; re-resolve citations on merged main) | WP01 | |
| T004 | Route `next_cmd.py:187/:253` — primary-anchor the `resolve_mission_identity` reads (lifecycle records) | WP01 | |
| T005 | Route `next_cmd.py:631` — `get_mission_type` primary fold (fixes wrong-run-type routing) | WP01 | |
| T006 | Route `implement.py:1389` (own primary anchor, survives `:1018` fallback removal) + owned `workflow.py` identity legs (`:1274` clean / `:1636` own-anchor shared-var / `:2732` clean) | WP01 | |
| T007 | Recompute `ROUTED_CANONICALIZER_FLOOR` strictly-below the post-fix census (before/after census recorded) | WP01 | |
| T008 | RED-first per-site tests on the divergent coord fixture — identity reads return the PRIMARY id/type, not the sentinel/default | WP01 | |
| T009 | FR-011 preflight (assert #2185 pins present) + FR-006 verify inherited whole-`src` scope covers `merge/`/`lanes/`/`core/` | WP02 | |
| T010 | Route `merge/forecast.py:153` (lanes) + `:159` (review-artifact preflight) | WP02 | |
| T011 | Route `merge/executor.py` — thread the `:887` PRIMARY dir through to `:976`; keep the `status_feature_dir` leg coord-aware | WP02 | |
| T012 | Route `merge/resolve.py:98` (meta); leave `:63` (handle→name canonicalization) on `candidate_` | WP02 | |
| T013 | Route `merge/done_bookkeeping.py:237` WP-path leg (`kind=WORK_PACKAGE_TASK`); remove the misleading comment; keep status-transactional legs on the primary dir | WP02 | |
| T014 | Route `cli/commands/merge.py:269` (meta; verify coord-teardown semantics first) | WP02 | |
| T015 | Remove the merge-cluster #2185 pins (same commit as routing) | WP02 | |
| T016 | RED-first per-site tests (both legs) on the divergent coord fixture | WP02 | |
| T017 | Route `lanes/merge.py:68/:198` (lanes) | WP03 | |
| T018 | Extract `scan_recovery_state` PRIMARY-planning + status-events helpers, drop `# noqa: C901`, route `:356` per-leg + `:611`; focused tests | WP03 | |
| T019 | Route `lanes/worktree_allocator.py:360` (meta; `kind=PRIMARY_METADATA` topology-blind) | WP03 | |
| T020 | Route `core/worktree_topology.py:138` (single swap co-resolves 3 PRIMARY legs) | WP03 | |
| T021 | Remove the lanes/core #2185 pins (same commit) | WP03 | |
| T022 | RED-first per-site tests (both legs) on the divergent coord fixture | WP03 | |
| T023 | Extend `build_coord`: sentinel husk `meta.json` (≠ PRIMARY) + PRIMARY-only `lanes.json`/`tasks/` seeded post-worktree-add; assert husk lacks them | WP04 | |
| T024 | Coord-topology merge/recovery/topology integration test; reverting any routed read to coord-aware FAILS | WP04 | |
| T025 | Flat-topology parity assertions (NFR-003) | WP04 | [P] |
| T026 | Pre-merge full-gate dry run (`tests/architectural/` green incl. the new arm; no un-pinned strangers; `ruff`+`mypy` clean) | WP05 | |
| T027 | Confirm floor recompute + zero STATUS legs re-routed (NFR-001) | WP05 | [P] |
| T028 | Issue-matrix #2185/#2186 → terminal verdict; append traces; validate quickstart | WP05 | [P] |

---

## Work Package WP01: Lane B — Identity arm + identity routing + floor (Priority: P1) 🎯

**Goal**: Build the net-new command-layer identity-read scan arm (with self-test), route the #2186 identity sites onto PRIMARY (arm + remediation co-land), and recompute the canonicalizer floor.
**Independent Test**: On a divergent coord fixture, `next_cmd` lifecycle records carry the PRIMARY `mission_id` and `get_mission_type` returns the PRIMARY type; the arm flags an injected unguarded identity read and passes after routing.
**Prompt**: `/tasks/WP01-lane-b-identity-arm-and-routing.md`
**Requirement Refs**: FR-004, FR-005, FR-007, FR-010, NFR-002

### Included Subtasks
- [ ] T001, T002, T003, T004, T005, T006, T007, T008

### Dependencies
- None (self-contained; net-new arm). Re-resolve `workflow.py` citations after the C-SEQ rebase.

### Risks & Mitigations
- Gate-unmask-cannot-self-validate → arm + routing co-land in this WP, validated by the WP05 full-gate dry run. Arm scope bounded to `cli/commands/` to avoid red-CI on out-of-scope strangers (sync/acceptance/policy).

---

## Work Package WP02: Lane A — Merge cluster routing (Priority: P1)

**Goal**: Route the `merge/` + `cli/commands/merge.py` PRIMARY reads by real kind (per-leg split where mixed) and drain the merge-cluster #2185 pins.
**Independent Test**: Merge/forecast on a divergent coord fixture reads lanes/meta/WP-tasks off PRIMARY; the status leg stays coord-aware; reverting any routed read fails the test.
**Prompt**: `/tasks/WP02-lane-a-merge-cluster.md`
**Requirement Refs**: FR-001, FR-002, FR-003, FR-006, FR-008, FR-011, NFR-001

### Included Subtasks
- [ ] T009, T010, T011, T012, T013, T014, T015, T016

### Dependencies
- Depends on WP01 (owns the gate file — linearize the pin-drain edits). C-SEQ rebase + T009 preflight first.

### Risks & Mitigations
- Over-routing a STATUS leg (NFR-001) → per-leg split, keep `status_feature_dir`/status-transactional legs coord-aware/primary as appropriate. Don't reintroduce #2139's silent `main` fallback.

---

## Work Package WP03: Lane A — Lanes/core cluster routing (Priority: P1)

**Goal**: Route the `lanes/` + `core/worktree_topology` PRIMARY reads; extract helpers out of the over-complex `scan_recovery_state`; drain the lanes/core #2185 pins.
**Independent Test**: Recovery scan + topology materialization read lanes/tasks/meta off PRIMARY on a divergent coord fixture; the events leg stays coord-aware.
**Prompt**: `/tasks/WP03-lane-a-lanes-core-cluster.md`
**Requirement Refs**: FR-001, FR-002, FR-008, NFR-001

### Included Subtasks
- [ ] T017, T018, T019, T020, T021, T022

### Dependencies
- Depends on WP02 (sequential gate-file chain).

### Risks & Mitigations
- A per-leg split inside `scan_recovery_state` (already `# noqa: C901`) worsens complexity → extract named helpers + drop the noqa + add tests, don't add a branch.

---

## Work Package WP04: Lane A — Coord-topology integration proof (Priority: P1)

**Goal**: Extend `build_coord` to a divergent husk and add the real `git worktree` coord-topology integration test that proves the routed reads land on PRIMARY.
**Independent Test**: The integration test is green and fails if any routed Lane A read is reverted to the coord-aware resolver.
**Prompt**: `/tasks/WP04-lane-a-integration-proof.md`
**Requirement Refs**: FR-009, NFR-003, NFR-004, SC-001

### Included Subtasks
- [ ] T023, T024, T025

### Dependencies
- Depends on WP02 + WP03 (routed code under test).

### Risks & Mitigations
- Non-divergent husk = false-green (the squad's CRITICAL finding) → the divergence assertion (husk lacks PRIMARY artifacts; sentinel meta) is the guard.

---

## Work Package WP05: Verify & close (Priority: P2)

**Goal**: Cross-cutting verification and mission close-out.
**Independent Test**: Full `tests/architectural/` green; floor strictly-below census; no STATUS leg re-routed; issue-matrix terminal.
**Prompt**: `/tasks/WP05-verify-and-close.md`
**Requirement Refs**: FR-010, NFR-001, NFR-003, C-SEQ

### Included Subtasks
- [ ] T026, T027, T028

### Dependencies
- Depends on WP01, WP02, WP03, WP04.

### Risks & Mitigations
- Gate-added-in-mission can't catch offenders in its own merge → pre-merge full-gate dry run (T026).

---

## Dependency & Execution Summary

- **Sequence**: WP01 → WP02 → WP03 → WP04 → WP05 (the gate file linearizes WP01→WP02→WP03; WP04 needs routed code; WP05 closes).
- **Parallelization**: WP01 is independent of the implement-loop landing (Lane B); Lane A (WP02–WP04) waits on the C-SEQ rebase. T002/T025/T027/T028 are `[P]` within their WPs.
- **MVP Scope**: WP01 (Lane B identity fix + arm) is independently shippable and not blocked on the sibling.

## Requirements Coverage Summary

| Requirement ID | Covered By Work Package(s) |
|----------------|----------------------------|
| FR-001 | WP02, WP03 |
| FR-002 | WP02, WP03 |
| FR-003 | WP02 |
| FR-004 | WP01 |
| FR-005 | WP01 |
| FR-006 | WP02 |
| FR-007 | WP01 |
| FR-008 | WP02, WP03 |
| FR-009 | WP04 |
| FR-010 | WP01, WP05 |
| FR-011 | WP02 |
| NFR-001 | WP02, WP03, WP05 |
| NFR-002 | WP01 |
| NFR-003 | WP04, WP05 |
| NFR-004 | WP04 |
| C-001 | WP02, WP03 |
| C-002 | WP01, WP02, WP03 |
| C-009-mirror | all |

## Subtask Index (Reference)

| Subtask ID | Summary | Work Package | Priority | Parallel? |
|------------|---------|--------------|----------|-----------|
| T001 | Identity-read scan arm | WP01 | P1 | No |
| T002 | Arm non-vacuity self-test | WP01 | P1 | Yes |
| T003 | ROUTE/KEEP ownership table | WP01 | P1 | No |
| T004 | Route next_cmd :187/:253 | WP01 | P1 | No |
| T005 | Route next_cmd :631 | WP01 | P1 | No |
| T006 | Route implement.py:1389 + owned workflow.py legs | WP01 | P1 | No |
| T007 | Floor recompute | WP01 | P1 | No |
| T008 | RED-first identity tests | WP01 | P1 | No |
| T009 | FR-011 preflight + FR-006 verify | WP02 | P1 | No |
| T010 | Route forecast | WP02 | P1 | No |
| T011 | Route executor (thread :887) | WP02 | P1 | No |
| T012 | Route resolve:98 | WP02 | P1 | No |
| T013 | Route done_bookkeeping:237 | WP02 | P1 | No |
| T014 | Route merge.py:269 | WP02 | P1 | No |
| T015 | Drain merge pins | WP02 | P1 | No |
| T016 | RED-first merge tests | WP02 | P1 | No |
| T017 | Route lanes/merge | WP03 | P1 | No |
| T018 | recovery extraction + route | WP03 | P1 | No |
| T019 | Route worktree_allocator | WP03 | P1 | No |
| T020 | Route worktree_topology | WP03 | P1 | No |
| T021 | Drain lanes/core pins | WP03 | P1 | No |
| T022 | RED-first lanes/core tests | WP03 | P1 | No |
| T023 | Divergent build_coord | WP04 | P1 | No |
| T024 | Coord integration test | WP04 | P1 | No |
| T025 | Flat-topology parity | WP04 | P1 | Yes |
| T026 | Full-gate dry run | WP05 | P2 | No |
| T027 | Floor + NFR-001 confirm | WP05 | P2 | Yes |
| T028 | Issue-matrix terminal + traces | WP05 | P2 | Yes |
