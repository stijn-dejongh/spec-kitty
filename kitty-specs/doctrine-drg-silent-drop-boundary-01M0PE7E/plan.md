# Implementation Plan: Doctrine DRG Silent-Drop Boundary Fix

**Branch**: `fix/doctrine-drg-silent-drop-boundary` | **Date**: 2026-08-23 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `kitty-specs/doctrine-drg-silent-drop-boundary-01M0PE7E/spec.md`

## Summary

Close four instances of the "declared-but-inert" doctrine/DRG family — where an
artifact is authored, schema-validated, and reported healthy yet silently never
takes effect — by making each declaration→consumption boundary **derived from a
single source, fail-loud, and test-pinned**:

1. **#3608** — derive the resolver's DRG node-kind set from the canonical
   `NodeKind` enum (kill the hand-copy) + a drift-guard test.
2. **#3629 part 1** — remove the redundant/inert `context-sources.*` profile
   surface and consolidate on the canonical top-level `*-references` surface
   (migration + update 25 shipped profiles).
3. **#3629 part 2** — verify the already-landed governance-profile fail-loud guard
   (`d8beee2761`) covers the org tier; close the item.
4. **#3530 + operator direction** — fix the `org_roots=` seam that silently drops
   `drg/fragment.yaml` (executor + `action_doctrine_bundle` callers), then verify
   chain delivery on the real `packs/internal/` (spec-kitty-internal) org pack.

Plus the #3629 part-3 doc-nit. The approach is brownfield-surgical: each concern
is a small, testable change against an existing seam; no new dependencies, no new
shadow paths.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: none new — existing stdlib + pydantic (models/schema), ruamel.yaml (pack/profile YAML), the in-repo `doctrine`/`charter`/`specify_cli` packages. **No dependency added, upgraded, or removed** → supply-chain planning section N/A.
**Storage**: files only — YAML doctrine artifacts under `packs/`, `.kittify/`, and the DRG serialized graphs; no database.
**Testing**: pytest (unit + `tests/integration/`, `tests/doctrine/`, `tests/architectural/`); run targeted, never the full suite in-session (see charter/CLAUDE.md). Terminology guard `tests/architectural/test_no_legacy_terminology.py` before push.
**Target Platform**: cross-platform CLI (Linux/macOS/Windows) — Python library + CLI, no runtime service.
**Project Type**: single project (library + CLI); source under `src/`, tests under `tests/`.
**Performance Goals**: N/A — correctness/fail-loud mission; no latency/throughput target. DRG build stays within current bounds (no new full-corpus scans).
**Constraints**: zero new `# noqa`/`# type: ignore`/per-file ignores (NFR-001); touched functions ≤15 cyclomatic complexity (NFR-004); every new branch/helper gets a focused test in the same WP (NFR-002); no behaviour change to what reaches a dispatched agent today (C-006).
**Scale/Scope**: ~6 code areas, ~25 shipped profile YAMLs migrated, 1 migration, ~5 test modules. Bounded; #3514 and #3511 explicitly out (C-007).

## Constitution Check (Charter)

*GATE: must pass before Phase 0 and re-checked after Phase 1.*

Charter present (`.kittify/charter/charter.md`); `software-dev-default` template, tools git/mypy/pytest/ruff/spec-kitty. Relevant binding items and how the plan complies:

| Charter item | Compliance in this plan |
|---|---|
| Canonical sources / single authority (G2) | Core of the mission: derive `_DRG_NODE_KINDS` from `NodeKind` (IC-1); collapse two profile-reference surfaces to one (IC-2). |
| No new shadow paths | No new resolvers/enumerations; every fix consolidates onto an existing canonical seam. |
| Fail-loud / no silent drop | IC-1 (unknown kind), IC-3 (bad selection), IC-4 (fragment drop + warning suppression) all convert silence to derivation or a loud signal. |
| ATDD-first / red-first | Each WP writes the failing test first (drift-guard, org-tier fail-loud, executor-seam delivery, chain-delivery) before the fix. |
| Terminology canon | Mission-not-Feature; run the terminology guard pre-push (NFR-003). |
| No suppressions to pass gates | NFR-001 binds; fixes are real, not silenced. |
| `__all__` convention (C-007 charter) | Any new public helper added to the module `__all__`. |

No charter violations → Complexity Tracking empty.

## Project Structure

### Documentation (this mission)

```
kitty-specs/doctrine-drg-silent-drop-boundary-01M0PE7E/
├── plan.md              # this file
├── spec.md              # committed
├── research.md          # Phase 0 (this command) — consolidates the squad findings
├── data-model.md        # Phase 1 (this command) — schema/model + DRG-shape changes
├── quickstart.md        # Phase 1 (this command) — how to verify each fix
├── contracts/
│   └── failloud-seams.md # Phase 1 — the behavioural (fail-loud) contracts per seam
├── research/            # pre-plan squad findings (committed)
│   └── context-sources-drg-projection.md
└── tasks.md             # Phase 2 (/spec-kitty.tasks — NOT created here)
```

### Source Code (repository root)

```
src/
├── charter/
│   ├── synthesizer/topic_resolver.py        # IC-1: _DRG_NODE_KINDS derive-from-enum
│   ├── _drg_helpers.py                       # IC-4: org_roots seam folds drg/fragment.yaml; warning honesty
│   ├── action_doctrine_bundle.py            # IC-4: caller wiring (org_fragments)
│   └── context_renderers/profile_sections.py # IC-2: reads *-references (delivery, unchanged behaviour)
├── doctrine/
│   ├── drg/models.py                         # IC-1: canonical NodeKind (source of truth; not edited)
│   ├── drg/migration/extractor.py            # IC-2 (project from *-references), IC-3 (verify guard), IC-6 (doc-nit :557)
│   ├── agent_profiles/profile.py             # IC-2: remove ContextSources.* fields
│   └── agent_profiles/schema_models.py       # IC-2: remove AgentContextSources.* fields
├── doctrine/schemas/agent-profile.schema.yaml# IC-2: drop context-sources block
├── specify_cli/
│   ├── mission_step_contracts/executor.py    # IC-4: caller wiring (org_fragments)
│   └── upgrade/migrations/                    # IC-2: profile context-sources→*-references migration
packs/
├── built-in/agent_profiles/*.agent.yaml      # IC-2: 25 profiles migrated to *-references
└── internal/                                 # IC-4: README refresh; #3530 fixture
tests/
├── architectural/                            # IC-1 drift-guard
├── doctrine/drg/migration/                   # IC-2 projection, IC-3 fail-loud
├── charter/ or specify_cli/                  # IC-4 executor/action-bundle seam
└── integration/                              # IC-5 chain-delivery on built-in+internal
```

**Structure Decision**: Single-project library layout (existing). Changes are
localized to the doctrine/charter seams listed; no new packages or top-level
dirs. Tests live beside the existing suites for each touched module.

## Implementation Concern Map

*The `/spec-kitty.tasks` command translates these concerns into work packages.
Each concern is independently testable (red-first) and small.*

| IC | Concern | Issue | Key files | Depends on | Risk |
|----|---------|-------|-----------|------------|------|
| **IC-1** | Derive `_DRG_NODE_KINDS` from `NodeKind`; drift-guard test; confirm dropped URN kinds resolve | #3608 | `topic_resolver.py`; new `tests/architectural/` (or `tests/charter/`) drift-guard | — | Low — SSOT swap; watch URN prefix vs value (edge case) |
| **IC-2** | Remove `context-sources.*`; consolidate on `*-references`; extractor projects from `*-references`; migrate 25 profiles; upgrade migration | #3629 p1 | `profile.py`, `schema_models.py`, `agent-profile.schema.yaml`, `extractor.py`, `packs/built-in/agent_profiles/*.agent.yaml`, migration + tests | — | **High** — blast radius (25 profiles + schema + migration); must not change delivered content (C-006) |
| **IC-3** | Verify governance-profile fail-loud guard (built-in) and cover org tier; close #3629 p2 | #3629 p2 | `extractor.py`/org loaders; `tests/doctrine/drg/migration/` | — | Low — mostly verify; org-tier may need a small guard |
| **IC-4** | Fix `org_roots=` seam to fold `drg/fragment.yaml` + stop false warning-suppression; wire executor + `action_doctrine_bundle`; refresh `packs/internal` README | #3530 / operator | `_drg_helpers.py`, `executor.py`, `action_doctrine_bundle.py`, `packs/internal/README.md` + tests | — | Medium — shared seam; guard against double-fold with `org_fragments` callers |
| **IC-5** | Chain-delivery verification on built-in + spec-kitty-internal via the executor/action-bundle seam; misconfigured-variant fails loud; close #3530 | #3530 | `tests/integration/` | IC-4 | Medium — build a real chain fixture; possibly a 2nd minimal org fixture |
| **IC-6** | Golden re-ledger doc-nit | #3629 p3 | `extractor.py:557` docstring | — | Trivial — fold into IC-3 |

## Parallel Work Analysis

### Dependency Graph

```
IC-1 (SSOT + drift-guard) ─┐
IC-2 (profile consolidation)┤ independent, parallel
IC-3 (+IC-6) (fail-loud verify + doc-nit) ┤
IC-4 (org_roots seam fix) ─┘
                            │
                            └─► IC-5 (chain-delivery verification)  [needs IC-4]
```

- **Sequential**: IC-5 depends on IC-4 (the seam must fold fragments before the
  chain test can assert delivery).
- **Parallel streams**: IC-1, IC-2, IC-3(+IC-6), IC-4 touch disjoint files and
  can proceed concurrently.
- **File-conflict avoidance**: only IC-2, IC-3, IC-6 all touch `extractor.py`.
  Sequence within that file: IC-2 (add `*-references` projection loops) → IC-3
  (guard verify, mostly reads) → IC-6 (docstring). If run as parallel WPs,
  serialize the `extractor.py` edits or assign IC-2/IC-3/IC-6 to one lane.

### Coordination Points

- After IC-4 lands, IC-5 builds the chain fixture and asserts delivery + fail-loud.
- Integration check: full targeted runs of `tests/doctrine/`, `tests/integration/`
  (org-pack + three-layer), `tests/architectural/` (drift-guard + terminology)
  before hand-off. Never the full suite in-session.

## Complexity Tracking

*No charter violations — none.*

## Engineering Alignment (confirmed assumptions)

- Tech stack fixed; no new dependencies; no user planning decisions outstanding.
- IC-4 fix approach: **fix at the `org_roots=` seam** (`_drg_helpers.py`) so all
  `org_roots` callers benefit from one change, AND stop the false warning
  suppression; thread `org_fragments` at the two callers only if the seam fix is
  insufficient. (Recorded as the default; final call at implement time with tests.)
- IC-2 removal relies on pydantic `extra="forbid"` already rejecting unknown keys,
  so post-removal a profile authoring `context-sources` fails loud at load — the
  desired boundary. The migration preserves authored artefact refs by moving them
  onto `*-references`; `additional`/`doctrine-layers` (no edge shape) are dropped.
- #3530 chain: built-in + internal is the ≥2-layer chain; a second minimal org
  fixture is added only if the strict multi-org-pack merge path must be exercised
  (decided in IC-5).
