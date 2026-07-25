---
work_package_id: WP06
title: Whole-tree write-placement enforcement gate + shared scanner
dependencies:
- WP02
- WP03
- WP04
requirement_refs:
- FR-001
- NFR-001
- NFR-004
planning_base_branch: feat/coord-write-placement-closure
merge_target_branch: feat/coord-write-placement-closure
branch_strategy: Planning artifacts for this mission were generated on feat/coord-write-placement-closure. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/coord-write-placement-closure unless the human explicitly redirects the landing branch.
created_at: '2026-07-25T12:00:00+00:00'
subtasks:
- T025
- T026
- T027
- T028
- T029
- T030
phase: Phase 3 - Whole-tree enforcement
history:
- at: '2026-07-25T12:00:00Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: python-pedro
authoritative_surface: tests/architectural/test_no_write_side_rederivation.py
create_intent:
- tests/architectural/_placement_whole_tree_scan.py
execution_mode: code_change
owned_files:
- tests/architectural/test_no_write_side_rederivation.py
- tests/architectural/test_safe_commit_import_boundary.py
- tests/architectural/_placement_whole_tree_scan.py
role: implementer
tags: []
task_type: implement
tracker_refs: []
---

# Work Package Prompt: WP06 – Whole-tree write-placement enforcement gate + shared scanner

## ⚡ Do This First: Load Agent Profile

Use the `/ad-hoc-profile-load` skill to load the agent profile in the frontmatter and behave per its guidance before parsing the rest of this prompt.

- **Profile**: `python-pedro`
- **Role**: `implementer`
- **Agent/tool**: `claude`

---

## Markdown Formatting

Wrap HTML/XML tags in backticks. Use language identifiers in code blocks.

---

## Objective

Replace the 17-module `_CHECKOUT_GRAMMAR_MODULES` allowlist with a **whole-tree AST gate** so a non-seam-derived mission-artifact write anywhere in `src/` reds. Build the **shared whole-tree scan helper** that IC-05's read gate (WP07) will also consume. This WP depends on WP02/WP03/WP04 so all writers are already routed — the gate lands green.

- **FR-001 / NFR-001**: scan 100% of `src/` Python modules; no module allowlist; a synthetic bypass in any module reds the gate.
- **NFR-004**: the existing write-side gates (`test_no_write_side_rederivation`, `test_safe_commit_import_boundary`, `test_write_surface_placement_guard`) stay green.

**Done** = the allowlist is replaced by a whole-tree scan with a per-file, individually-justified sanctioned-primitive exclusion set (reusing the existing `_BOUNDARY_SANCTIONED_MODULES`); `test_safe_commit_import_boundary` asserts `target=CommitTarget(...)` is seam-derived; a synthetic bypass reds; the shared scanner is a reusable module.

## Context & Constraints

- Spec: [spec.md](../spec.md) US3 AS1, FR-001, NFR-001, NFR-004, SC-002. Plan: [plan.md](../plan.md) IC-02. Contract: [contracts/placement-enforcement.md](../contracts/placement-enforcement.md) "Write". Research D-01.
- **Reuse, do not add** (folded squad finding): reuse the **existing** `_BOUNDARY_SANCTIONED_MODULES:486` — do NOT add a new collection. **Forbid dir-prefix exclusions** (`_BOUNDARY_SANCTIONED_PREFIXES` is how an allowlist creeps back). Keep exclusions **per-file** with an inline rationale enforced by the meta-test at `:746`.
- **def-vs-call discrimination**: ~15 modules newly enter scope, including **definition sites** (`commit_helpers.safe_commit`, `mission_metadata.write_meta`, `merge/baseline.py`, `acceptance/__init__.py`, `doc_state.py`, …). The gate must discriminate a *definition* of `safe_commit`/`write_meta`/`CommitTarget` from a *call* — or it false-reds the def sites. Budget each newly-scanned module as route (already done in WP02-04) vs sanctioned.
- **Proxy honesty**: the gate proves **syntactic** provenance (the arg is a `resolve_placement_only`/`placement_seam.write_target` call), not value-flow. State this in the gate docstring; do not over-promise semantic proof.
- **Baseline-red gotcha**: after widening, any newly-red module is either a real un-routed writer (fix belongs to WP02-04 — coordinate) or a sanctioned primitive (add per-file with rationale). Do NOT green-wash by broadening exclusions.

## Branch Strategy

- **Strategy**: generated on `feat/coord-write-placement-closure`; changes merge back into `feat/coord-write-placement-closure`.
- **Planning base branch**: `feat/coord-write-placement-closure`
- **Merge target branch**: `feat/coord-write-placement-closure`

## Subtasks & Detailed Guidance

### Subtask T025 – Extract the shared whole-tree scan helper

- **Purpose**: one module walker + sanctioned-set resolver consumed by both this gate and WP07's read gate.
- **Steps**: Create `tests/architectural/_placement_whole_tree_scan.py` exposing (a) a `src/` module walker yielding parsed AST per module, and (b) the sanctioned-set accessor that reads the **existing** `_BOUNDARY_SANCTIONED_MODULES`. Keep it a pure helper (no gate assertions) so WP07 can import it.
- **Files**: `tests/architectural/_placement_whole_tree_scan.py` (new).
- **Validation**: importable; walks all `src/` modules; returns the existing sanctioned set unchanged.

### Subtask T026 – Replace the allowlist with a whole-tree scan

- **Purpose**: FR-001 — remove `_CHECKOUT_GRAMMAR_MODULES:471-476`; scan all of `src/`.
- **Steps**: In `test_no_write_side_rederivation.py`, replace the 17-module allowlist iteration with the shared whole-tree walker. Every module is in scope unless per-file sanctioned.
- **Files**: `tests/architectural/test_no_write_side_rederivation.py`.
- **Validation**: the gate iterates 100% of `src/` modules.

### Subtask T027 – def-vs-call discrimination for newly-scanned modules

- **Purpose**: NFR-001 without false-reds on definition sites.
- **Steps**: Add AST logic that treats a `def safe_commit`/`def write_meta` / `class CommitTarget` **definition** as out-of-scope and only flags **calls** whose `target=`/`ref=` arg is not a seam-derivation call. Walk the ~15 newly-entered modules; classify each as routed (should pass) or sanctioned (per-file rationale).
- **Files**: `tests/architectural/test_no_write_side_rederivation.py` (+ helper if needed in the scanner).
- **Validation**: the def sites (`commit_helpers`, `mission_metadata`, …) pass without exclusion; only true bypass calls red.

### Subtask T028 – Extend `test_safe_commit_import_boundary` for `target=` seam-derivation

- **Purpose**: FR-001 — assert `target=CommitTarget(...)` is seam-derived.
- **Steps**: Extend `test_safe_commit_import_boundary.py` to assert every `safe_commit(target=…)` / `CommitTarget(ref=…)` call site derives the target from `resolve_placement_only`/`placement_seam.write_target`. Reuse the shared scanner.
- **Files**: `tests/architectural/test_safe_commit_import_boundary.py`.
- **Validation**: a non-seam-derived `target=` reds.

### Subtask T029 – Per-file sanctioned exclusions + meta-test rationale

- **Purpose**: NFR-001 — sanctioned primitives carry inline rationale; no dir-prefix creep.
- **Steps**: For each genuinely-sanctioned primitive (e.g. lane-deliverable commit, invocation/upgrade commits), add a per-file entry to the **existing** `_BOUNDARY_SANCTIONED_MODULES` with an inline rationale. Extend the meta-test at `:746` to REQUIRE a rationale per entry. Confirm no `_BOUNDARY_SANCTIONED_PREFIXES`-style dir exclusion is introduced.
- **Files**: `tests/architectural/test_no_write_side_rederivation.py`.
- **Validation**: the meta-test reds if any sanctioned entry lacks a rationale.

### Subtask T030 – Synthetic-bypass proof + non-regression

- **Purpose**: SC-002 / NFR-004.
- **Steps**: Add a test that injects a synthetic non-seam-derived write into a scratch module path and asserts the gate reds and **names the offending site**. Run the three existing write-side gates — they must stay green.
- **Files**: `tests/architectural/test_no_write_side_rederivation.py`.
- **Validation**: synthetic bypass reds with the site named; existing gates green.

## Test Strategy

- New: `tests/architectural/_placement_whole_tree_scan.py` (shared helper).
- Run: `PWHEADLESS=1 uv run --extra test pytest tests/architectural/test_no_write_side_rederivation.py tests/architectural/test_safe_commit_import_boundary.py -q` plus the full `tests/architectural/` suite for non-regression.

## Definition of Done

- Allowlist replaced by whole-tree scan; shared scanner reusable by WP07.
- def-vs-call discrimination; no dir-prefix exclusions; per-file rationale via meta-test.
- `target=CommitTarget(...)` seam-derivation asserted.
- Synthetic bypass reds and names the site; existing gates green; `ruff` + `mypy` clean.

## Risks & Mitigations

- **Exclusion list balloons into an inverted allowlist** → forbid dir-prefix exclusions; per-file + rationale meta-test.
- **Def sites false-red** → T027 def-vs-call discrimination.
- **A real un-routed writer surfaces** → coordinate the fix back to WP02-04 (its owner); do NOT sanction it away.

## Review Guidance

- Verify NO new collection was added — the existing `_BOUNDARY_SANCTIONED_MODULES` is reused.
- Verify each sanctioned entry has an inline rationale enforced by the meta-test.
- Verify the gate docstring states the syntactic-proxy limitation honestly.

## Activity Log

- 2026-07-25T12:00:00Z – system – Prompt created.
