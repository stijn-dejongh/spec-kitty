# Tasks: Single planning-surface authority + worktree repair

**Mission**: `single-planning-surface-authority-01KVPR00` · branch `feat/single-planning-surface-authority`
**Driver**: #1890 + #1716 · folds #2062/#2063/#2064 · campsite #1970 (ACTIVE every WP)

10 WPs / 44 subtasks. Linearized anchor chain (read-path safety-net → write-authority →
`is_committed` collapse last) + disjoint lanes B/D/E. **#1970 is active in every WP:
remediate adjacent debt in the touched surface in-slice.**

## Subtask Index

| ID | Description | WP | Parallel |
| --- | --- | --- | --- |
| T001 | Gate `_resolve_existing_for_slug` coord-preference on declared coordination (FR-004) | WP01 | |
| T002 | Unify `probe_coord_state` branch-signal threading + fix stale `:263` comment (FR-012) | WP01 | |
| T003 | Zero-mock unit: flattened-stale-coord → PRIMARY on read-path leg, all handles | WP01 | |
| T004 | FR-017 gated: retire `mission_read_path` shim if zero external consumers | WP01 | |
| T005 | Campsite #1970 in `_read_path_resolver.py` | WP01 | |
| T006 | Add `flattened-stale-coord` topology to `_build_topology` (FR-005) | WP02 | |
| T007 | Add topology × all-handle rows asserting all 3 legs → PRIMARY (assertion unweakened) | WP02 | |
| T008 | Live flattened-mid-flight repro (quickstart R1, NFR-001) | WP02 | |
| T009 | Campsite: de-stale the equivalence-gate module docstring | WP02 | |
| T010 | `safe-commit` mission-aware path → `resolve_placement_only`; separate from generic (FR-001/FR-002/NFR-002) | WP03 | |
| T011 | `spec-commit` routes the same authority; consolidate duplicate placement logic | WP03 | |
| T012 | Tests: mission commit lands on authority surface; generic operator-file path preserved | WP03 | |
| T013 | Campsite in safe/spec-commit (note NOT-DUE `--to-branch` v3.3 deprecation, leave) | WP03 | |
| T014 | `emit_status_transition` write `feature_dir` resolved by the single authority (FR-006) | WP04 | |
| T015 | Tests: dep-gate/kanban/review-claim read surface converges with `move-task` write | WP04 | |
| T016 | Campsite in `status/emit.py` (20-param hub out of scope — pointer only) | WP04 | |
| T017 | `setup_plan` write path → `resolve_placement_only` (FR-001) | WP05 | |
| T018 | `finalize-tasks` read region → single WP-frontmatter surface (FR-003 finalize half) | WP05 | |
| T019 | FR-019: extract touched placement/commit helpers → `coordination/commit_router.py` (#2056) | WP05 | |
| T020 | FR-015: `setup-plan`/`finalize-tasks` `--json` single clean document | WP05 | |
| T021 | FR-016: harden `mission.py:312` untrusted-path sink + negative test | WP05 | |
| T022 | Campsite + complexity ≤15 on touched `mission.py` functions | WP05 | |
| T023 | `map-requirements` writes WP refs on the SAME surface finalize reads (FR-003 map half) | WP06 | |
| T024 | FR-013: consolidate the WP-frontmatter READ surface (not `compute_coverage`) | WP06 | |
| T025 | FR-014: emit parsed FR-ID set on coverage mismatch in `--json` (#2066) | WP06 | |
| T026 | FR-016: harden `tasks.py:1911` untrusted-path sink + negative test | WP06 | |
| T027 | FR-010 de-pin: re-point `test_map_requirements_coord/spec_path` to cross-command coherence | WP06 | |
| T028 | Campsite in the map-requirements region | WP06 | |
| T029 | FR-009: hoist 5× doctor recovery hint to ≤2 named constants per failure class | WP07 | |
| T030 | FR-018: extract doctor coord-recovery cluster `:3092-3225` → `_coord_recovery.py` (#2059) | WP07 | |
| T031 | FR-007: register `agent worktree repair --mission` (recreate / prune / benign no-op) | WP07 | |
| T032 | Repoint recovery hints (doctor + surface_resolver strings) + amend ADR 2026-06-19-1 | WP07 | |
| T033 | FR-010 de-pin: re-point the phantom-string tests to the real command | WP07 | |
| T034 | Campsite + tests for the new verb (recreate/prune/no-op) | WP07 | |
| T035 | FR-008: command-reference guard (Python literals + ADRs vs registered Typer commands) | WP08 | |
| T036 | NFR-003: planted-phantom self-test + full-suite dry-run note | WP08 | |
| T037 | FR-016: harden `merge.py:1055` untrusted-path sink + negative test | WP08 | |
| T038 | Campsite | WP08 | |
| T039 | FR-011: collapse `_substantive.is_committed` 3-leg OR → single-surface check | WP09 | |
| T040 | Prove against all topologies — gated on WP02 live repro green | WP09 | |
| T041 | Campsite | WP09 | |
| T042 | FR-002 doctrine: migrate `charter/prompt.md` off `safe-commit` → `spec-commit` | WP10 | |
| T043 | Run terminology guard + full `tests/architectural/` sweep pre-push | WP10 | |
| T044 | Campsite | WP10 | |

## Work Packages

### WP01 — Read-path flattened-stale-coord gate (SAFETY NET, first)
**Goal**: a flattened mission never reads an orphaned coord worktree (read-path leg). **FRs**: FR-004, FR-012, FR-017. **Independent test**: `pytest tests/missions/test_coord_feature_dir_helpers.py` + a zero-mock flattened-stale-coord unit. **Deps**: none. **Prompt**: tasks/WP01-read-path-flattened-coord-gate.md
- [ ] T001 Gate `_resolve_existing_for_slug` coord-preference on declared coordination (WP01)
- [ ] T002 Unify `probe_coord_state` branch-signal threading + fix stale `:263` comment (WP01)
- [ ] T003 Zero-mock unit: flattened-stale-coord → PRIMARY on read-path leg, all handles (WP01)
- [ ] T004 FR-017 gated: retire `mission_read_path` shim if zero external consumers (WP01)
- [ ] T005 Campsite #1970 in `_read_path_resolver.py` (WP01)

### WP02 — Differential gate: flattened-stale-coord cell + live repro
**Goal**: the convergence safety net feeds the broken topology. **FRs**: FR-005 (NFR-001). **Independent test**: the gate reads N passed / 0 xfailed incl. the new rows. **Deps**: WP01. **Prompt**: tasks/WP02-differential-gate-flattened-coord-cell.md
- [ ] T006 Add `flattened-stale-coord` topology to `_build_topology` (WP02)
- [ ] T007 Add topology × all-handle rows asserting all 3 legs → PRIMARY (WP02)
- [ ] T008 Live flattened-mid-flight repro (quickstart R1, NFR-001) (WP02)
- [ ] T009 Campsite: de-stale the equivalence-gate module docstring (WP02)

### WP03 — Commit-path write-authority adoption
**Goal**: `safe-commit`/`spec-commit` route through the single write authority; generic use preserved. **FRs**: FR-001, FR-002 (NFR-002). **Deps**: WP02. **Prompt**: tasks/WP03-commit-path-write-authority.md
- [ ] T010 `safe-commit` mission-aware path → `resolve_placement_only`; separate from generic (WP03)
- [ ] T011 `spec-commit` routes the same authority; consolidate duplicate placement logic (WP03)
- [ ] T012 Tests: mission commit lands on authority surface; generic preserved (WP03)
- [ ] T013 Campsite in safe/spec-commit (WP03)

### WP04 — Status-event emission write-surface
**Goal**: event emission resolves its write surface from the single authority. **FRs**: FR-006. **Deps**: WP03. **Prompt**: tasks/WP04-status-emit-write-surface.md
- [ ] T014 `emit_status_transition` write `feature_dir` resolved by the single authority (WP04)
- [ ] T015 Tests: read surface converges with `move-task` write (WP04)
- [ ] T016 Campsite in `status/emit.py` (WP04)

### WP05 — mission.py anchor: setup_plan/finalize routing + de-godding (FR-019)
**Goal**: the god-module's planning write/read routes through the authority; touched helpers extracted. **FRs**: FR-001, FR-003, FR-015, FR-016, FR-019 (NFR-004). **Deps**: WP03, WP04. **Prompt**: tasks/WP05-mission-py-anchor-routing-degod.md
- [ ] T017 `setup_plan` write path → `resolve_placement_only` (WP05)
- [ ] T018 `finalize-tasks` read region → single WP-frontmatter surface (WP05)
- [ ] T019 FR-019: extract touched placement/commit helpers → `coordination/commit_router.py` (WP05)
- [ ] T020 FR-015: `setup-plan`/`finalize-tasks` `--json` single clean document (WP05)
- [ ] T021 FR-016: harden `mission.py:312` untrusted-path sink + negative test (WP05)
- [ ] T022 Campsite + complexity ≤15 on touched functions (WP05)

### WP06 — map-requirements one-surface + diagnostics
**Goal**: map-requirements and finalize read/write WP frontmatter on ONE surface. **FRs**: FR-003, FR-013, FR-014, FR-016 (FR-010). **Deps**: WP05. **Prompt**: tasks/WP06-map-requirements-one-surface.md
- [ ] T023 `map-requirements` writes refs on the SAME surface finalize reads (WP06)
- [ ] T024 FR-013: consolidate the WP-frontmatter READ surface (WP06)
- [ ] T025 FR-014: emit parsed FR-ID set on coverage mismatch in `--json` (WP06)
- [ ] T026 FR-016: harden `tasks.py:1911` untrusted-path sink + negative test (WP06)
- [ ] T027 FR-010 de-pin: re-point map_requirements tests to cross-command coherence (WP06)
- [ ] T028 Campsite in the map-requirements region (WP06)

### WP07 — Worktree-repair verb + recovery repoint + doctor de-godding
**Goal**: a real recreate-or-prune verb; recovery hints name registered commands; doctor cluster extracted. **FRs**: FR-007, FR-009, FR-018 (FR-010). **Internal order**: T029 hoist → T030 extract → T031 verb → T032 repoint. **Deps**: none. **Prompt**: tasks/WP07-worktree-repair-verb-degod.md
- [ ] T029 FR-009: hoist 5× doctor recovery hint to ≤2 named constants (WP07)
- [ ] T030 FR-018: extract doctor coord-recovery cluster → `_coord_recovery.py` (WP07)
- [ ] T031 FR-007: register `agent worktree repair --mission` (recreate / prune / no-op) (WP07)
- [ ] T032 Repoint recovery hints + amend ADR 2026-06-19-1 (WP07)
- [ ] T033 FR-010 de-pin: re-point the phantom-string tests to the real command (WP07)
- [ ] T034 Campsite + tests for the new verb (WP07)

### WP08 — Command-reference guard + merge.py sink
**Goal**: no shipped string names an unregistered command; the guard self-validates. **FRs**: FR-008, FR-016 (NFR-003). **Deps**: WP07. **Prompt**: tasks/WP08-command-reference-guard.md
- [ ] T035 FR-008: command-reference guard (Python literals + ADRs vs registered commands) (WP08)
- [ ] T036 NFR-003: planted-phantom self-test + full-suite dry-run note (WP08)
- [ ] T037 FR-016: harden `merge.py:1055` untrusted-path sink + negative test (WP08)
- [ ] T038 Campsite (WP08)

### WP09 — Collapse is_committed 3-leg OR (LAST, gated)
**Goal**: reduce the load-bearing workaround once write-authority is singular + the safety net proven. **FRs**: FR-011. **Deps**: WP05, WP02. **Prompt**: tasks/WP09-is-committed-collapse.md
- [ ] T039 FR-011: collapse `_substantive.is_committed` 3-leg OR → single-surface check (WP09)
- [ ] T040 Prove against all topologies — gated on WP02 live repro green (WP09)
- [ ] T041 Campsite (WP09)

### WP10 — Doctrine charter prompt off safe-commit
**Goal**: planning prompts use mission-aware `spec-commit`. **FRs**: FR-002 (doctrine half). **Deps**: WP03. **Prompt**: tasks/WP10-doctrine-charter-prompt.md
- [ ] T042 FR-002 doctrine: migrate `charter/prompt.md` off `safe-commit` (WP10)
- [ ] T043 Run terminology guard + full `tests/architectural/` sweep pre-push (WP10)
- [ ] T044 Campsite (WP10)

## Dependency graph
- WP01 → WP02 → WP03 → WP04 → WP05 → WP09 (linearized anchor chain; WP09 last, also deps WP02)
- WP05 → WP06 (Lane B, after the mission.py anchor)
- WP03 → WP10 (Lane E)
- WP07 → WP08 (Lane D, independent of the anchor chain)

## Risks
- **Dogfooding hazard (LIVE):** the mission was flattened during planning to escape the
  coord/primary split it fixes (create→primary tasks/, spec-commit→coord, finalize→primary).
  The implement loop will hit the same friction — drive status from the authoritative
  (primary) surface; re-flatten if a lane wedges.
- **Load-bearing-workaround collapse:** WP09 is gated on WP02's live repro + write-authority
  adoption — never collapse `is_committed` before convergence is proven (NFR-001).
- **God-module brush-by:** keep touched `mission.py`/`tasks.py`/`doctor.py` functions ≤15;
  extract only the touched seam (FR-018/FR-019), not the whole module.
