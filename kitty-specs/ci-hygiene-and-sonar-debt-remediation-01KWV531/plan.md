# Implementation Plan: CI Hygiene & Sonar Debt Remediation

**Branch**: `design/pr-landing-followups-and-sonar-remediation` | **Date**: 2026-07-06 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `kitty-specs/ci-hygiene-and-sonar-debt-remediation-01KWV531/spec.md`

## Summary

Fix two independent classes of CI/quality-gate debt surfaced during today's PR #2414 landing pass, then treat the live SonarCloud backlog as real, addressable work. **Concern A (CI-infra)**: migrate the CI-topology census gate's LOC tracking off exact-equality onto the repo's existing growth-only-ratchet convention (`_baselines.yaml`); unify two independently-broken contract-conformance path-resolution hacks (`test_upgrade_command.py`, `test_messages.py`) onto one canonical helper; fix the description-length violation the dead check was masking. **Concern B (Sonar)**: wire `sonar.projectVersion` from `pyproject.toml` into the CI scanner config so the new-code baseline resets per dev cycle instead of freezing indefinitely; document/reconcile the Sonar-vs-internal coverage-scope mismatch; promote the existing (gitignored) `sonarcloud_branch_review.sh` into a tracked, idempotent, re-runnable tool; use it to slice the ~900-issue live backlog into tracked GitHub issues (parented under epic #1928, milestoned `3.2.x`, labeled `tech-debt`+`quality`+`devex`); then identify and actually fix the slice that intersects the current roadmap's active surface (the Wave 2 degod trio files), explicitly excluding any issue whose only correct fix requires the refactor that mission is separately chartered to do.

## Technical Context

**Language/Version**: Python 3.11+ (existing `spec-kitty-cli` monorepo stack; no new language/runtime)
**Primary Dependencies**: `pytest` (existing marker-based CI-gate conventions: `fast`/`architectural`/`unit`), `jsonschema` (contract validation), `ruamel.yaml`/`PyYAML` (for `_baselines.yaml` and `ci_topology_census.json` edits), `gh` CLI (issue filing/parenting via `sub_issues` API), `curl`/SonarCloud public REST API (already used by `sonarcloud_branch_review.sh`), GitHub Actions (`.github/workflows/ci-quality.yml`)
**Storage**: N/A — flat committed config files (JSON/YAML: `ci_topology_census.json`, `_baselines.yaml`, `sonar-project.properties`) plus GitHub Issues as the backlog-slice record; no database
**Testing**: `pytest` via this repo's existing marker/gate conventions (`tests/architectural/` for the CI-topology and contract-conformance fixes; a new smoke test for the promoted Sonar script per FR-012); red-first verification for every bug fix per DIRECTIVE_034
**Target Platform**: GitHub Actions Linux runners (CI) + local dev (macOS/Linux) — no new deployment target
**Project Type**: single (existing monorepo; no new service/app boundary)
**Performance Goals**: N/A for runtime — this is CI-infra/tracker-hygiene work. Constraint instead: no new or modified job may push the `arch-adversarial`/`fast-tests-core-misc` critical path past the existing NFR-001 ceiling established by the `ci-topology-shrink` mission (~13.6 min)
**Constraints**: C-001 (no Wave 2 degod-trio body-thinning refactor in this mission), C-002 (no ratchet/suppression mechanism for un-remediated backlog items), NFR-001 (census-gate fix must not drop any routing-completeness invariant the current suite enforces)
**Scale/Scope**: ~900 live SonarCloud issues to slice (903 confirmed live); 2 test files with 19 total silently-dead contract-conformance call sites (13 + 6); 3 Wave-2-trio files (~6,145 combined LOC: `workflow.py` 2830, `acceptance/__init__.py` 1733, `implement.py` 1582) for the roadmap-aligned fix slice

### Confirmed planning decisions (Decision Moment Protocol)

- **`sonar.projectVersion` source** (`DM-01KWV7EJRDAG6MHJ8CK5513KY8`): derives from `pyproject.toml`'s current version. Updates on every version-bump commit (dev-cycle-open and release), so the new-code baseline resets promptly each cycle rather than staying frozen. Accepted tradeoff: briefly reports an unreleased version number mid-cycle — acceptable since SonarCloud only uses this as a baseline-reset signal, not a release-authority claim.
- **Census-gate fix mechanism** (`DM-01KWV7EKTEP05FJQC2W65GWJ3H`): split the LOC field out of `ci_topology_census.json`'s exact-equality assertion entirely; route LOC tracking through the existing `_baselines.yaml` growth-only-ratchet system (the same mechanism 7 other gated modules already use). `ci_topology_census.json` becomes purely structural/routing (which dirs route to which shard/group), independent of the LOC-ratchet concern.
- **Backlog-slicing tooling reusability** (`DM-01KWV7EMW7V24156HB72M39Z87`): build the promoted `sonarcloud_branch_review.sh` + slicing/filing logic as a re-runnable, idempotent tool (skip-if-already-filed per rule+file), not a one-shot script — future backlog-triage passes (there will be more, per C-002's explicit no-ratchet stance) reuse it instead of starting from scratch.

## Charter Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Charter loaded (compact mode). Relevant directives and how this mission satisfies them:

- **DIRECTIVE_024 (Locality of Change)** — satisfied by construction: C-001 explicitly excludes the Wave 2 degod-trio refactor from this mission's own scope, preventing exactly the drive-by-refactor risk this directive warns against.
- **DIRECTIVE_043 (Close Defect Classes by Construction)** — the core shape of ICs 01 and 02 below: both fix a *class* of defect (brittle exact-equality snapshots; ad hoc contract-path resolution) via a structural gate/shared-helper change, not a one-off patch.
- **DIRECTIVE_044 (Canonical Sources and Unification)** — directly implemented by IC-02 (one canonical path-resolution helper replacing two independent hacks) and IC-06 (promoting the existing `sonarcloud_branch_review.sh` instead of each WP reinventing SonarCloud API calls).
- **DIRECTIVE_034 (Test-First Development)** — every IC below that fixes a bug reproduces it red-first through the pre-existing test entry point before applying the fix (per this mission's own spec User Stories, which already document the red-first reproduction for #2416/#2419/#2420).
- **DIRECTIVE_030 (Test and Typecheck Quality Gate)** — `ruff`/`mypy --strict` clean on every touched Python file; the full `tests/architectural/` suite must stay green (NFR-001's explicit requirement).

No charter conflicts identified. **Gate: PASS.**

## Project Structure

### Documentation (this mission)

```
kitty-specs/ci-hygiene-and-sonar-debt-remediation-01KWV531/
├── spec.md              # Committed (feature spec + post-spec squad folds)
├── plan.md              # This file
├── research.md          # Phase 0 output (below)
├── data-model.md        # Phase 1 output (below)
├── contracts/           # Phase 1 output (below)
├── quickstart.md        # Phase 1 output (below)
└── tasks.md             # Phase 2 output (/spec-kitty.tasks — NOT created here)
```

### Source Code (repository root)

Single project (existing monorepo). No new top-level directories — this mission touches existing surfaces:

```
tests/architectural/
├── test_ci_topology_worklist.py     # FR-001/002: census-gate assertion migrates off exact-LOC-equality
├── ci_topology_census.json          # FR-001: LOC field removed/reduced to structural-only fields
├── _baselines.yaml                  # FR-001: new per-dir LOC ratchet entries added
├── test_ratchet_baselines.py        # FR-001: existing ratchet-check meta-test now also covers the new entries
└── _gate_coverage.py                # FR-001: live_derived_worklist() no longer emits LOC into the equality-checked shape

tests/specify_cli/cli/commands/
└── test_upgrade_command.py          # FR-003/004: repoint at canonical contract-path helper (13 call sites)

tests/specify_cli/compat/
└── test_messages.py                 # FR-003/004: repoint at the same canonical helper (6 call sites)

tests/<new shared location, e.g. tests/_contract_paths.py or tests/conftest.py fixture>
                                      # FR-003: new canonical compat-planner.json path-resolution helper

src/specify_cli/upgrade/migrations/
└── m_3_2_0rc35_unified_bundle.py    # FR-005: trim description to <=256 chars

.github/workflows/
└── ci-quality.yml                   # FR-006: sonarcloud job passes -Dsonar.projectVersion from pyproject.toml

sonar-project.properties             # FR-006: no version key needed here if wired via CI step args (confirm in research.md)

scripts/ci/ (new tracked location, promoted from work/snippets/)
└── sonarcloud_branch_review.sh      # FR-012: promoted, made idempotent, gains a smoke test

docs/ or a mission-local doc         # FR-007: Sonar-vs-internal coverage-scope reconciliation note

<Wave 2 degod trio files, fix-only, no refactor>
├── src/specify_cli/cli/commands/agent/workflow.py
├── src/specify_cli/cli/commands/implement.py
└── src/specify_cli/acceptance/__init__.py
```

**Structure Decision**: Single project, no new source directories. This mission's deliverables are: (1) targeted fixes/migrations of existing test-infra files, (2) one new canonical shared test helper, (3) one promoted-and-hardened script, (4) N new GitHub issues (not source files), and (5) fixes to specific pre-existing Sonar findings inside three already-large files — no new architectural surface.

## Complexity Tracking

*No Charter Check violations requiring justification — table omitted.*

## Implementation Concern Map

> Implementation concerns are NOT work packages. `/spec-kitty.tasks` translates these into executable WPs — one concern may become multiple WPs; multiple small concerns may merge into one WP.

### IC-01 — Census-gate LOC-ratchet migration

- **Purpose**: Stop `test_census_worklist_matches_live_derivation` from reding on unrelated LOC changes, by moving LOC tracking off exact-equality onto the repo's proven growth-only-ratchet convention, while preserving 100% of existing routing-completeness enforcement.
- **Relevant requirements**: FR-001, FR-002, NFR-001, SC-001, SC-003.
- **Affected surfaces**: `tests/architectural/test_ci_topology_worklist.py`, `tests/architectural/ci_topology_census.json`, `tests/architectural/_baselines.yaml`, `tests/architectural/_gate_coverage.py`, `tests/architectural/test_ratchet_baselines.py`.
- **Sequencing/depends-on**: none — independent of every other IC.
- **Risks**: `live_derived_worklist()` is consumed by more than just this one test (confirmed during spec validation it's also read by `test_census_mapped_dirs_matches_live_derivation` and `test_census_arch_blind_groups_matches_live_derivation`, which stay exact-equality since they're structural, not LOC-based — do not accidentally change their behavior while touching the same module).

### IC-02 — Canonical contract-path-resolution helper (both files)

- **Purpose**: Replace two independently-broken hardcoded parent-walk hacks with one canonical, checkout-shape-agnostic helper that resolves `compat-planner.json`'s path correctly from any real checkout (CI, worktree, or plain clone), and fails loudly (never silently no-ops) if it still can't be found.
- **Relevant requirements**: FR-003, FR-004, NFR-002, SC-002, SC-003.
- **Affected surfaces**: `tests/specify_cli/cli/commands/test_upgrade_command.py` (13 call sites), `tests/specify_cli/compat/test_messages.py` (6 call sites), one new shared helper location (research.md to confirm exact placement — `tests/conftest.py` fixture vs. a small `tests/_contract_paths.py`-style module).
- **Sequencing/depends-on**: none — independent, but IC-03 depends on this landing first (its check can't run for real until this IC lands).
- **Risks**: the new helper must resolve correctly in a CI runner, a plain single-checkout clone, AND a maintainer's `.worktrees/<name>` layout — three distinct directory-depth shapes to prove, not just the two currently known-broken ones.

### IC-03 — Fix the masked migration-description length violation

- **Purpose**: Trim `m_3_2_0rc35_unified_bundle.py`'s migration description to ≤256 chars so it passes the contract-conformance check the moment IC-02 makes that check run for real.
- **Relevant requirements**: FR-005, SC-002 (partial).
- **Affected surfaces**: `src/specify_cli/upgrade/migrations/m_3_2_0rc35_unified_bundle.py`.
- **Sequencing/depends-on**: IC-02 (this violation is only observable/verifiable once the dead check is fixed).
- **Risks**: trimming must preserve the description's meaning for anyone reading `spec-kitty upgrade --dry-run` output — not just mechanically truncate.

### IC-04 — Wire `sonar.projectVersion` from `pyproject.toml`

- **Purpose**: Give every SonarCloud analysis a real, non-placeholder version identifier so the new-code baseline resets per dev cycle instead of freezing indefinitely (frozen since 2026-03-21 today).
- **Relevant requirements**: FR-006, SC-004.
- **Affected surfaces**: `.github/workflows/ci-quality.yml` (the `sonarcloud` job's "Materialize effective Sonar config" step and scanner-action `args`), possibly `sonar-project.properties`.
- **Sequencing/depends-on**: none.
- **Risks**: the `sonarcloud` job only runs on `schedule`/`workflow_dispatch` (confirmed during spec validation), so this fix can only be observed end-to-end via the nightly cron or a manual dispatch — plan verification accordingly, don't assume a push/PR will show it.

### IC-05 — Reconcile/document the Sonar-vs-internal coverage-scope mismatch

- **Purpose**: Make it possible for anyone comparing SonarCloud's whole-repo coverage number to the internal `diff-coverage` PR gate's result to correctly interpret whether a discrepancy is a real regression or an expected scope difference.
- **Relevant requirements**: FR-007, NFR-003, SC-... (documentation-quality outcome, not a numbered SC on its own — covered by NFR-003's "5 minutes" interpretability bar).
- **Affected surfaces**: research/investigation-heavy; likely output is a short doc (SonarCloud project description field, and/or a repo doc) plus, if the investigation finds a genuine scope-alignment fix is feasible, a small CI-config change.
- **Sequencing/depends-on**: none — can run in parallel with everything else. Genuinely research-first: the spec explicitly could not verify file-level Sonar coverage gaps without `SONAR_TOKEN` access, so this IC's first task is determining whether a real instrumentation gap exists at all, or whether it's purely a reporting-clarity problem.
- **Risks**: low — worst case this IC produces documentation only, no code risk.

### IC-06 — Promote `sonarcloud_branch_review.sh` into a tracked, idempotent tool

- **Purpose**: Give this mission (and future ones) one canonical, tested SonarCloud-API tool instead of ad hoc API calls per WP.
- **Relevant requirements**: FR-012, SC-008.
- **Affected surfaces**: new tracked location (e.g. `scripts/ci/sonarcloud_branch_review.sh`, promoted from `work/snippets/`), a new smoke test for it, `.gitignore` (remove the now-tracked path from the `work` ignore rule's effective scope if needed).
- **Sequencing/depends-on**: none — but IC-07 and IC-08 both consume its output, so it should land first in implementation order even though it has no hard blocking dependency.
- **Risks**: the script currently works standalone; hardening it for idempotent, tracked, tested use may surface auth/rate-limit handling gaps not exercised in its ad hoc usage to date.

### IC-07 — Slice the live Sonar backlog into tracked, parented GitHub issues

- **Purpose**: Turn the ~900-issue live backlog into scoped, ownable, correctly-parented tracker work — nothing lost, nothing orphaned.
- **Relevant requirements**: FR-008, FR-009, C-003, C-004, NFR-004, SC-005.
- **Affected surfaces**: GitHub issues (new, via `gh`/API) parented under epic #1928; new `quality`/`devex` labels (created following existing label conventions).
- **Sequencing/depends-on**: IC-06 (needs the promoted tool's output to slice from).
- **Risks**: the "needs-triage" bucket (per spec Edge Cases) must have an explicit home so multi-module or effort-unknown issues aren't dropped or forced into a wrong bucket; NFR-004's 100%-coverage claim must be independently verifiable (live API count vs. sum of filed-issue counts), not eyeballed.

### IC-08 — Identify and fix the roadmap-aligned Sonar slice

- **Purpose**: Deliver the mission's highest-leverage outcome — actually fix (not just ticket) the Sonar issues living in the Wave 2 degod trio files and any #1868/#2173 seam-binding touchpoints, respecting the C-001 refactor exclusion.
- **Relevant requirements**: FR-010, FR-011, C-001, C-002, SC-006, SC-007.
- **Affected surfaces**: `src/specify_cli/cli/commands/agent/workflow.py`, `src/specify_cli/cli/commands/implement.py`, `src/specify_cli/acceptance/__init__.py` — fixes only, per-issue, no structural extraction.
- **Sequencing/depends-on**: IC-07 (needs the slice identified and sliced first) and, transitively, IC-06.
- **Risks**: the C-001/FR-010 triage rule (any issue only fixable via the forbidden refactor is excluded and re-ticketed under FR-008/FR-011, not force-fixed and not silently dropped) must be applied consistently and the exclusions recorded — this is the one place in the mission where scope discipline is easiest to accidentally violate under time pressure.
