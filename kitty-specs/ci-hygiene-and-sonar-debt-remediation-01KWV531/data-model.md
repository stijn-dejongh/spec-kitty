# Phase 1 Data Model: CI Hygiene & Sonar Debt Remediation

This mission has no application data model (no database, no runtime domain
objects). The entities below are the structural shapes of the config/tracker
artifacts this mission creates or restructures.

## 1. `WorklistCensusEntry` (structural-only, post-IC-01)

Represents one tracked CI-topology worklist directory in
`tests/architectural/ci_topology_census.json`, after LOC is split out.

| Field | Type | Notes |
|---|---|---|
| `dir` | string | Directory name under `src/specify_cli/` |
| `cone_roots` | list[string] | Test root(s) covering this dir |
| `target_group` | string | Named `dorny/paths-filter` composite group |
| `target_shard` | string | Focused integration shard this dir routes to |

**Invariant**: exact-equality against `live_derived_worklist()` for these four
fields only — this is what NFR-001 requires the fix to keep enforcing.
`loc` is **removed** from this structure's equality check (moved to §2).

## 2. `LocRatchetBaseline` (new, in `_baselines.yaml`)

One entry per tracked worklist directory, under a new top-level
`test_ci_topology_worklist` key, following the existing `BaselinesFile`
pydantic-validated schema (`{module_name: {baseline_key: int}}`).

| Field (YAML key shape) | Type | Notes |
|---|---|---|
| `<dir>_loc` | int | Committed LOC baseline for that directory |

**Invariant**: growth above baseline fails `test_growth_fails_shrinkage_warns`
(the existing shared ratchet meta-test); shrinkage warns only, never fails —
identical semantics to the other 7 gated modules already in this file.

## 3. `ContractPathResolution` (new shared test fixture, IC-02)

Not a persisted entity — the *contract* of the new canonical helper.

| Aspect | Value |
|---|---|
| Input | none (resolves relative to its own `__file__` and the discovered repo root) |
| Output | `Path` to `compat-planner.json`, guaranteed to exist |
| Error behavior | raises (e.g. `FileNotFoundError` with a clear message) if the contract file cannot be located after walking to the repo root — never returns `None` and never silently skips a caller's assertion |
| Consumers | `tests/specify_cli/cli/commands/test_upgrade_command.py` (13 call sites), `tests/specify_cli/compat/test_messages.py` (6 call sites) |

## 4. `BacklogSliceTicket` (GitHub Issue shape, FR-008)

The shape every filed backlog-slice issue must have, per C-003/C-004/NFR-004.

| Field | Type | Notes |
|---|---|---|
| `title` | string | Names the module + rule class, not a generic "Sonar issues" title |
| `body.module` | string | The `src/specify_cli/<dir>` (or equivalent) the slice covers |
| `body.rule_ids` | list[string] | SonarCloud rule keys covered by this slice (live data, per C-003) |
| `body.live_issue_count` | int | Count at filing time, from the live API — never an estimate |
| `body.effort_bucket` | enum | `small` / `medium` / `large` / `needs-triage` (per spec Edge Cases — multi-module or unknown-effort items get `needs-triage`, never forced into a wrong bucket) |
| `body.impact_bucket` | enum | `low` / `medium` / `high` — reliability/security-hotspot-bearing slices bias toward `high` |
| `labels` | list[string] | `tech-debt` + `quality` + `devex` (all three, always) |
| `milestone` | string | `3.2.x` |
| `parent` | issue ref | Native GitHub sub-issue of **#1928** |
| `roadmap_aligned` | bool (implicit via a label or note, TBD at task time) | Marks the slice(s) selected for FR-010's in-mission fix, distinguishing "ticketed" from "ticketed AND fixed now" |

**Invariant** (NFR-004): `sum(live_issue_count across all filed BacklogSliceTicket rows) == live SonarCloud open-issue count at slicing time` — the completeness check this mission's own success criteria demand must be mechanically computable from this shape, not eyeballed.

## 5. `RoadmapSliceExclusion` (tracking record, C-001/FR-010 triage rule)

Not a new artifact type — a required annotation on any `BacklogSliceTicket`
(§4) that would otherwise qualify as "roadmap-aligned" (module ∈ Wave 2 degod
trio or #1868/#2173 touchpoints) but is excluded from FR-010's in-mission fix
because its only correct remediation requires the C-001-forbidden refactor.

| Field | Type | Notes |
|---|---|---|
| `excluded_reason` | string | Must explicitly state "requires pure-core/port extraction (C-001)" or equivalent — a generic "too hard" is not sufficient per the spec's Edge Cases resolution |

This keeps SC-006's "reduced to zero" claim honest: it excludes exactly the
issues recorded here, not an unstated/undocumented subset.
