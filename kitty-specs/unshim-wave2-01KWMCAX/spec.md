# Mission Specification: Unshim Wave 2 — registered-shim removals + charter deprecation-cycle closure

**Mission Branch**: `tidy/unshim-wave2`
**Created**: 2026-07-03
**Status**: Draft
**Input**: Operator directive "spec: wave 2 + fold-ins" — execute #2291 (`specify_cli.next` #612 + `specify_cli.glossary` #613 registered removals; HiC comment rescinded the 3.3.0 deferral → current cycle) and #2290 (charter deprecation-cycle closure) as **full deletion**, plus fold-ins: #2326 (dead `frontmatter::update_field` wrapper) and the WS1 `mission_runtime` layer-rule bind. Pre-planning 3-lens squad (debugger-debbie, planner-priti, architect-alphonso; 2026-07-03, verified on main @ 47fed302d) findings are folded below as binding facts; squad-corrected facts override the issue bodies.

## Adjudicated Decisions (binding; divergences resolved from source)

1. **Charter shims: FULL DELETE, not register-and-defer.** Alphonso recommended register-only (cheaper); overruled by the operator's standing anti-deferral ruling — registering `charter_*` shims at a `removal_target_release` would recreate exactly the version-boundary deferral the HiC rescinded on #2291. Deletion is sized honestly below (it is ~4× the issue's framing).
2. **WS1 layer rule is NOT a prerequisite** (roadmap claim falsified: `src/mission_runtime/` — 4 files — imports neither `specify_cli.next` nor `runtime.next`; no edge exists). It folds in as an independent probe/bind WP because it is cheap, roadmap-committed, and un-tracked (dedicated sub-issue filed at spec time, parent #1868). If the bind surfaces a hidden lazy edge, it becomes load-bearing and sequences before the next-shim deletion; otherwise it is parallel.
3. **No sanctioned-surface prerequisite.** `runtime.next.*` is already the canonical import surface; the shared-package-boundary gates forbid only the retired `spec_kitty_runtime` package; `_internal_runtime` imports are un-gated (convention, not boundary).
4. **`_CATEGORY_6_FROZEN_RUNTIME_REEXPORTS` (3 rows) is OUT of scope** — falsified claim; those are canonical `runtime.next._internal_runtime.*` modules that survive.
5. **#612/#613 are CLOSED antecedents** (extraction tickets, closed 2026-06-01, parent #391) — referenced, never re-closed.
6. **#2072 Obligation B (~10 resolver-site drain) stays OUT** (different surface, not in any Wave 2 target; roadmap assigns category_b burn-down #2293 to a later wave). Recorded as an open operator question on #2293's prerequisite semantics.

## Squad-Verified Census (binding facts, override stale issue-body claims)

### Stream A — `specify_cli.next` (#2291, registered removal #612)

- Shim: `src/specify_cli/next/__init__.py` (75 LOC, pure re-export via `sys.modules` aliasing — same object identity as canonical; carries `__deprecated__`/`__canonical_import__="runtime.next"`). Canonical `src/runtime/next/` fully live; re-point is 1:1.
- **Src callers (3, line-exact)**: `cli/commands/implement.py:1285` and `cli/commands/agent/workflow.py:1518` (plain `from specify_cli.next.runtime_bridge import build_operational_context_for_claim` → `runtime.next.runtime_bridge`); `cli/commands/next_cmd.py:52-58` — **a monkeypatch injection seam**, `sys.modules.get("specify_cli.next.runtime_bridge") or importlib.import_module("runtime.next.runtime_bridge")`, with 2 injector tests (`test_selector_resolution.py:502,548`) using `patch.dict(sys.modules, ...)` on the legacy key. Seam + injectors move together to the `runtime.next.runtime_bridge` key — else the injection **silently no-ops after deletion** (vacuous-pass class). `next_cmd.py:557`/`schema.py:22` are comments, not callers.
- **Test surface (DRIFTED UP from the issue's 49): 77 files / ~480 refs** = ~417 plain import lines (mechanical, loud-on-error) + **80 `patch()`/`patch.dict(sys.modules,...)` string targets** (the silent-no-op class Wave 1 proved real — per-line verification required, blind sed is a review reject). Dominant modules: `runtime_bridge` (186), `decision` (54), `_internal_runtime.{schema,engine}` (23 each).
- This is **bulk-edit territory**: the plan phase MUST produce an occurrence-map classification for the `specify_cli.next` → `runtime.next` rename (all 8 categories with explicit actions).

### Stream B — `specify_cli.glossary` (#2291, registered removal #613)

- Shim: `src/specify_cli/glossary/__init__.py` (55 LOC husk, full `__deprecated__` metadata, aliases 21 submodules). Canonical `src/glossary/` (22 modules) live with its own layer gate (untouched).
- **Zero src callers** (issue's "verify count" → resolved). Test surface: 2 files — `tests/glossary/test_legacy_import_shim.py` (tests the shim itself → deletes with it) + `tests/architectural/test_shim_registry_schema.py:45` (asserts the registry row → edit in the same commit).

### Stream C — charter deprecation-cycle closure (#2290, ~4× the issue's framing)

- **Three legacy shim packages** `charter_lint/`, `charter_freshness/`, `charter_preflight/` re-export `specify_cli.charter_runtime.{lint,freshness,preflight}`; **no `__deprecated__` markers, absent from shim-registry** → invisible to the scanner (the C-008 governance hole; any "N shims remaining" metric undercounts by ≥3).
- **Non-test callers to re-point: 4, not 2** — `cli/commands/charter/lint.py:45,93`, `cli/commands/charter/status.py:55`, and the squad-found defect **`charter_runtime/preflight/runner.py:36`: the canonical package imports its own legacy shim** (canonical→legacy→canonical cycle) → `from specify_cli.charter_runtime.freshness import compute_freshness`.
- **Test surface: ~19-20 files** importing legacy paths (charter_lint ~13 files incl. 10 patch-strings; charter_preflight ~6 incl. `test_next_no_implicit_success` patching `charter_preflight.hook`; charter_freshness ~3) → all re-point to `charter_runtime.*`.
- **Lock-gate retirement**: `tests/architectural/test_charter_runtime_shim_paths.py` (5 tests) explicitly pins the legacy paths importable + module-identity for patching. Full deletion retires this gate **with surviving-coverage proof** (the re-pointed suites ARE the surviving coverage) per the refactor-stable convert-or-delete doctrine — this is precisely the "transitional shape-guard needing a retirement path" class.
- **4th unmarked shim (fold-in): `charter_activate.py`** — live caller `cli/commands/charter/activate.py:141`, no marker, outside #2290's named list. Disposition in-mission: re-point callers to its canonical home and delete if zero-caller after re-point; if inspection shows it is canonical itself (not a shim), document-and-exclude with evidence. Adjacent category_b rows `charter_activate::{AffectedMission,StepRemovalWarning}` (:517-518) — drain only what deletion makes dead.

### Stream D — #2326 fold (dead wrapper)

- `frontmatter.py:318-320` module wrapper `update_field` (+ `__all__` entry :373) — zero callers (Wave 1 deleted the sole one). Also the now-orphaned instance method `FrontmatterManager.update_field` (:142, called only by the wrapper) — delete both. Drain `test_no_dead_symbols.py:235` row + `_baselines.yaml category_b_grandfathered_legacy: 216 → 215` (shrink-only).

### Stream E — WS1 probe/bind (fold-in; dedicated sub-issue at spec time, parent #1868)

- `mission_runtime` is a **defined layer with no LayerRule** (`tests/architectural/conftest.py:108`; every sibling layer has a `should_not().access_layers_that()` rule in `test_layer_rules.py`). Bind a non-vacuous outbound rule (allowed set adjudicated at plan time from the actual import graph) + record the layer decision. The bind doubles as the probe proving no hidden lazy edge to the next-shim.

### Spine — co-tenant governance surfaces (forced sequencing point)

`docs/migrations/shim-registry.yaml` (2 rows out: next, glossary; 0 charter rows needed under full-delete), `tests/architectural/test_shim_registry_schema.py:44-45` (hard-asserts BOTH rows present — **breaks on row removal**; edit in the same commit), `tests/architectural/test_unregistered_shim_scanner.py` (passes once shims are gone), `_baselines.yaml` (D's 216→215 + any deletion-made-dead rows). Per the Wave 1 pattern: atomic delete+drain per WP (C-005); a standalone gate-drain WP is forbidden.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - One runtime surface, no legacy import path (Priority: P1)

As a Spec Kitty contributor, `runtime.next.*` and `glossary.*` are the only import paths for their domains — `import specify_cli.next` and `import specify_cli.glossary` raise `ModuleNotFoundError`, and every test exercises the canonical namespace so mocks provably intercept.

**Why this priority**: the registered removals are the cluster's core debt; every day the aliases exist, new code and new `patch()` strings can re-couple to them.

**Independent Test**: both shims gone; `spec-kitty next --help` exit 0 (clean-install CI lane green); the 2 injector tests inject at the `runtime.next.runtime_bridge` key and still intercept; full suite green.

**Acceptance Scenarios**:

1. **Given** the shims deleted, **When** `python -c "import specify_cli.next"` / `"import specify_cli.glossary"` run, **Then** both raise `ModuleNotFoundError`, and `spec-kitty next` still resolves the runtime bridge via the canonical import.
2. **Given** the re-pointed 80 patch-strings, **When** each rewritten site executes, **Then** it provably intercepts: per site EITHER an existing/added call assertion OR a recorded red-first bogus-target flip (Wave 1 protocol; bulk sed = review reject).
3. **Given** the `next_cmd.py` seam re-pointed, **When** `test_selector_resolution.py`'s injector tests run, **Then** the injected fake is actually consumed (assert on the fake's usage, not just green).

---

### User Story 2 - Charter deprecation cycle closed by deletion (Priority: P2)

As the operator, the three charter legacy shims (+ the `charter_activate` straggler) are deleted with all callers re-pointed to `charter_runtime.*`, the canonical→legacy defect in `runner.py` fixed, and the legacy-path lock-gate retired with surviving-coverage proof — no shim is left invisible to governance.

**Why this priority**: C-008 hole — unmarked shims make the scanner's health signal silently wrong; full deletion (not registration) per the anti-deferral ruling.

**Independent Test**: `charter_lint/`, `charter_freshness/`, `charter_preflight/` gone; `test_charter_runtime_shim_paths.py` retired with the surviving-coverage proof recorded; `test_unregistered_shim_scanner` green; all ~20 re-pointed test files green.

**Acceptance Scenarios**:

1. **Given** the deletions, **When** an import-scoped grep for `specify_cli.charter_(lint|freshness|preflight)` runs over src/ and tests/, **Then** zero import/patch references remain (prose/archives excluded).
2. **Given** the retired lock-gate, **When** the mission diff is reviewed, **Then** it carries the surviving-coverage proof: the re-pointed suites cover every behavior the 5 retired tests pinned (per-test disposition, judge-the-test framework).
3. **Given** `runner.py:36` re-pointed, **When** the preflight suite runs, **Then** green with the canonical import (defect fix is import-path-only).

---

### User Story 3 - Governance surfaces stay coherent (Priority: P3)

As a future planner, the shim registry, scanner, layer rules, and baselines reflect the post-wave reality: registry drained of executed rows, WS1 layer rule bound and non-vacuous, category_b at the honest count.

**Independent Test**: `test_shim_registry_schema.py` green with its presence-assertions updated; the new `mission_runtime` LayerRule exists and fails on a synthetic violation (non-vacuity theater); `_baselines.yaml` category_b 215 (or lower if deletions dead more rows — honest live count, Wave 1 precedent).

**Acceptance Scenarios**:

1. **Given** the merged wave, **When** `pytest tests/architectural/ -q` runs, **Then** green with zero staleness reds and all baseline changes shrink-only.
2. **Given** the WS1 bind, **When** a synthetic `mission_runtime → specify_cli` import is exercised in theater, **Then** the new LayerRule reds (non-vacuity proof).

### Edge Cases

- A patch-string re-pointed to a plausible-but-wrong `runtime.next` namespace passes while the shim lives (shared object identity) and only no-ops after deletion → interception proofs must hold against the canonical key directly (or run post-deletion in the WP order).
- The `sys.modules` injection seam: production re-pointed but injector tests left on the legacy key → tests pass vacuously; the seam + both injectors move in one change (FR-001).
- `test_shim_registry_schema.py` asserts row PRESENCE → registry row removal without the same-commit test edit reds; the owning WP carries both (C-005).
- `charter_activate.py` may prove canonical-not-shim on inspection → document-and-exclude with evidence rather than force-fit deletion (FR-007).
- The bulk `specify_cli.next→runtime.next` rename hits doc prose and archived kitty-specs → occurrence-map classifies archives as leave-as-is vs live docs as update (C-004).

## Requirements *(mandatory)*

### Functional Requirements

| ID | Title | User Story | Priority | Status |
|----|-------|------------|----------|--------|
| FR-001 | Re-point specify_cli.next src callers + seam | As a contributor, I want the 2 plain imports re-pointed to `runtime.next.runtime_bridge` and the `next_cmd.py:52-58` monkeypatch seam + its 2 injector tests moved to the canonical key in one change, so no vacuous injection survives. | High | Open |
| FR-002 | Re-point the 77-file next test surface | As a contributor, I want all ~417 plain import lines re-pointed mechanically and each of the 80 patch-strings re-pointed with a per-site interception proof (Wave 1 protocol), classified via the plan-phase occurrence-map. | High | Open |
| FR-003 | Delete specify_cli.next + drain registry | As a maintainer, I want `src/specify_cli/next/` deleted with the shim-registry row removed and `test_shim_registry_schema.py`'s presence-assertion updated in the same commit. | High | Open |
| FR-004 | Delete specify_cli.glossary + drain registry | As a maintainer, I want the glossary husk deleted, `test_legacy_import_shim.py` deleted with it, and the registry row + schema-test assertion drained atomically. | High | Open |
| FR-005 | Charter callers re-pointed incl. the canonical→legacy defect | As a contributor, I want the 4 non-test callers (lint.py:45,93; status.py:55; runner.py:36) re-pointed to `charter_runtime.*` — runner.py:36 is a defect fix (canonical importing its own legacy shim). | High | Open |
| FR-006 | Charter shims deleted + lock-gate retired | As the operator, I want `charter_lint/`, `charter_freshness/`, `charter_preflight/` deleted after the ~20 legacy-import test files re-point to `charter_runtime.*`, and `test_charter_runtime_shim_paths.py` retired with a per-test surviving-coverage proof. | High | Open |
| FR-007 | charter_activate disposition | As the operator, I want `charter_activate.py` adjudicated in-mission: re-point its live callers and delete if it is a shim with a canonical home; document-and-exclude with evidence if inspection shows it is canonical itself. Drain only deletion-made-dead category_b rows. | Medium | Open |
| FR-008 | #2326 dead-wrapper prune | As a maintainer, I want the `update_field` module wrapper + `__all__` entry + orphaned instance method deleted with the category_b row drained and baseline 216→215. | Medium | Open |
| FR-009 | WS1 layer-rule bind | As an architect, I want a non-vacuous `mission_runtime` outbound LayerRule bound in `test_layer_rules.py` (allowed set adjudicated at plan time from the actual import graph), with theater proving it reds on a synthetic violation, and the layer decision recorded. | Medium | Open |
| FR-010 | Tracker closeout | As the operator, I want #2291/#2290/#2326 closed by the PR, the WS1 sub-issue filed (parent #1868) and progressed, a #1797 progress comment, #612/#613 referenced as closed antecedents, an operator-facing note on #2293's prerequisite semantics, and the issue-matrix at terminal verdicts. | Medium | Open |

### Non-Functional Requirements

| ID | Title | Requirement | Category | Priority | Status |
|----|-------|-------------|----------|----------|--------|
| NFR-001 | Full-suite green | `PWHEADLESS=1 pytest tests/ -n auto --dist loadfile` green on the merged branch; full `tests/architectural/` sweep green with zero staleness reds; clean-install-verification lane green (post-repoint `spec-kitty next` works in a fresh venv). | Reliability | High | Open |
| NFR-002 | Zero legacy-path residue at merge | Import-scoped grep for `specify_cli.(next|glossary|charter_lint|charter_freshness|charter_preflight)` across src/ and tests/ returns empty (pinned pattern in quickstart at plan time; prose/archives excluded). | Correctness | High | Open |
| NFR-003 | Static gates stay clean | Whole-tree mypy 0; ruff clean on the diff; zero new suppressions. | Maintainability | High | Open |
| NFR-004 | Shrink-only ratchets + honest counts | Every baseline/allowlist/registry change is a removal or decrease; post-wave counts are live-derived (Wave 1 honest-216 precedent), never spec-derived. | Governance | Medium | Open |
| NFR-005 | CI-visible new tests | Any new/relocated test carries markers the CI suite-map actually selects (#2034 is live — invisible-marker tests are a known hole); verify per new test file. | Process | Medium | Open |

### Constraints

| ID | Title | Constraint | Category | Priority | Status |
|----|-------|------------|----------|----------|--------|
| C-001 | Re-point before delete | No shim file is deleted while any src or test reference resolves through it; per-stream ordering is re-point → prove → delete (the #2159/uv_receipt lesson). | Technical | High | Open |
| C-002 | Behavior-neutral migration | Re-points are import-path changes only; zero behavior changes to canonical modules (the runner.py:36 fix is import-path-only). New code limited to the WS1 LayerRule + theater. | Technical | High | Open |
| C-003 | Canonical surfaces are fixed | Re-point targets: `runtime.next.*`, `glossary.*`, `specify_cli.charter_runtime.*` — no new surface, no `_internal_runtime` privatization work (out of scope; un-gated per adjudicated decision 3). | Scope | High | Open |
| C-004 | Bulk-edit governance | The `specify_cli.next` rename goes through the plan-phase occurrence-map (8 categories, explicit actions); ad-hoc repo-wide sed is forbidden. | Process | High | Open |
| C-005 | Atomic delete+drain per WP | Registry rows, schema-test assertions, baselines, and category rows drain in the same WP as the deletion they correspond to; no standalone gate-drain WP. | Technical | High | Open |
| C-006 | Refactor-stable self-conformance | Retired tests (lock-gate, shim self-tests) follow convert-or-delete with surviving-coverage proof; no re-pins; the WS1 rule ships with non-vacuity theater. | Doctrine | Medium | Open |
| C-007 | Census authority | Re-point site counts and paths come from this spec's squad-verified census; the #2291/#2290 issue bodies are stale (49 vs 77 files; 2 vs 4 callers). | Process | Medium | Open |

### Key Entities

- **Registered shim**: a `__deprecated__=True` module with a shim-registry row; removal = re-point all callers → delete file → drain row + schema-test assertion atomically.
- **Unregistered legacy shim** (the #2290 class): re-export package invisible to the scanner; closure here = deletion (registration would re-defer).
- **Interception proof**: per rewritten patch-string, evidence the mock still intercepts (call assertion or red-first flip) — Wave 1 protocol, now standing.
- **Lock-gate**: an arch test pinning legacy paths importable; retirement requires per-test surviving-coverage proof.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 5+ shim surfaces deleted (`specify_cli/next/`, `specify_cli/glossary/`, 3 charter packages, + `charter_activate.py` per FR-007 disposition, + the #2326 wrapper); shim-registry drained to zero legacy rows; no unregistered `__deprecated__` module remains in src/.
- **SC-002**: ~500 re-point sites executed (≈417+80 next, ~25 charter test-file sites, 4 charter src callers) with all patch-strings carrying interception proofs; zero legacy-path imports at merge (NFR-002 grep empty).
- **SC-003**: `test_charter_runtime_shim_paths.py` and `test_legacy_import_shim.py` retired with recorded surviving-coverage proofs; the new WS1 LayerRule exists, is non-vacuous (theater red on synthetic violation), and its decision is recorded.
- **SC-004**: #2291, #2290, #2326 closed via the PR; WS1 sub-issue filed and progressed; #1797 progress comment posted; category_b baseline at the honest live count (≤215); all gates green with zero retries and zero new suppressions.
