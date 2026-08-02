# Phase 0 Research & Decisions — Doctrine-Charter Split Single-Path Authority

Consolidated from the pre-spec (planner-priti / paula-patterns / architect-alphonso) and post-plan
(paula-patterns / planner-priti / python-pedro) adversarial squads. Every anchor below is verified against
live code on `feat/doctrine-charter-split-unification` (base `8466727eb`).

## D1 — Charter path/read authority already has its home; FR-001 is near-empty

`charter/bundle.py` already defines **and exports** `CHARTER_YAML` (`:35`) and `CHARTER_MD` (`:48`) in
`__all__` (`:467`), and `charter/context.py` already imports them (pre-deduped by #3146). **Decision:** FR-001
does **not** get its own lane — it folds into the first IC-01 WP as a confirm/guard; the four surface repoints
(FR-002/003/004/006) start in parallel immediately (file-disjoint, no shared new symbol to wait on). The
durability comes from the FR-016 gate (D6), not from a front-loaded constant WP.

## D2 — No genuine write-scope collisions (file granularity)

`lanes.json write_scope` is an **explicit per-file path list**, not a directory glob → lanes collide only on
the *same path*. Verified false alarms: (a) the IC-02 emitter is `charter/compiler.py:441`
(`write_compiled_charter`), **not** `synthesize_pipeline.py` — so IC-02 (emitter) and IC-04 (FR-008 edge in
`synthesize_pipeline.py:68`) are **distinct files**; (b) FR-016/FR-008 gates are **new test files**;
(c) `src/charter/**` and `src/specify_cli/retrospective/**` call `load_meta` **zero** times, so IC-03 is fully
file-disjoint from IC-01/IC-02/IC-04. **Decision:** the per-file "fold the repoint into the surface WP"
discipline holds; cross-IC lanes parallelize safely.

## D3 — FR-005 (retrospective → charter.yaml governance): no layer inversion; one omit-mechanism fix

`GovernanceConfig` (`charter/schemas.py:135`) composes nested pydantic sub-models and imports peers **within**
the charter layer. **Decision:** re-author a pure-data `RetrospectiveGovernance` sub-model **into**
`charter/schemas.py` (bool / `Literal` / nested permissions — zero `specify_cli` import; the existing
`specify_cli.retrospective.policy.RetrospectivePolicy` is **not** imported upward). Emitter (FR-005b) stays
in-layer via `charter.sync.load_governance_config` (`sync.py:233`) feeding `write_compiled_charter`
(`compiler.py:441`/`:601`). Resolver (FR-005c) is a **downward** import: `specify_cli/retrospective/{policy,mode,gate}.py`
imports `charter.charter_yaml_io.load_charter_yaml` + `charter.bundle`, reads `governance.retrospective` as a
dict, and feeds it as highest-precedence through the existing `_apply_block_to_policy` (`policy.py:381`).
**Refinement (must fold):** the omit-when-empty pruner `_prune_optional_empties` (`schemas.py:346`) is
**list-only** (`isinstance(value, list) and not value`) — it will **not** omit an empty `retrospective`
dict/None, leaking a default block into every `charter.yaml` and breaking NFR-005 byte-stability. Extend the
pruner to drop an allowlisted key whose value is `None`/empty-dict (or model the field `| None` with a
None-drop branch). Ship a byte-stability regression test.

## D4 — FR-007 (meta.json fail-closed): reuse core/paths; keep the import function-local

`core/paths.py` already owns `MissionMetaReadError` (`:506`) and `_load_meta_fail_closed` (`:638`, which lazily
imports `load_meta` inside the function at `:655` to break the pre-existing `core/paths ↔ mission_metadata`
cycle). **Decision:** promote `_load_meta_fail_closed` to a public `load_meta_fail_closed` in `core/paths`
(or have `mission_metadata` delegate to it) — **one home, no second authority**. **Guard:** the `load_meta`
import MUST stay function-local during promotion, or the cycle re-forms.

**Two `load_meta` definitions hazard:** there are **two** distinct functions — `mission_metadata.py:275`
(`load_meta(feature_dir)`) and `task_utils/support.py:599` (`load_meta(meta_path: Path)`), different
signatures. The FR-007 **caller census** (110 `load_meta(` sites across ~55 files) MUST disambiguate which
function each site targets, or routing mis-wires the `task_utils` callers. This is a census acceptance
criterion.

## D5 — IC-03 sub-slicing (census + reader-publish + parallel routing lanes)

Routing ~dozens of files in one lane is an unreviewable diff. **Decision:** (1) census artifact (D4, gating),
(2) publish the public reader in `core/paths`+`mission_metadata`, then (3) parallel routing lanes sub-sliced by
subsystem (coordination+migration / merge+status+dashboard+cli / mission_runtime+runtime). The
`mission_runtime+runtime` lane turns the two red `test_mission_status_aggregate::TestLoadCoordUnavailableFailsClosed`
tests green via `lifecycle_phase.py` (C-004 owns these reds). Preserve deliberately-silent callers
(`load_meta_or_empty`, `on_malformed="none"`).

## D6 — FR-016 anti-regression gate: AST census + understated allowlist + doctrine-scope decision

**Decision:** detection is **AST path-construction literals** (a `.kittify/charter/charter.{yaml,md}` string
inside a `Path(...)` construction / const assignment), **not** raw text grep (else it floods on ~161
docstring/prose mentions). The frozen **shrink-only allowlist** is the right mechanism (a hard zero is
unshippable). The plan's stated allowlist (`upgrade/migrations/**` + C-003 prose readers) is **understated** —
real path-builders also live at `invocation/empty_charter.py:60` (`_CHARTER_BUNDLE_PATH`),
`charter_runtime/lint/checks/org_layer.py:291`, `doctrine/versioning.py:190,451`,
`doctrine/spdd_reasons/activation.py:49`. **Open decision the WP must make:** does the gate police
`src/doctrine/**` (then allowlist `versioning.py`/`activation.py`) or scope to `charter/`+`specify_cli/`?
The WP runs a full AST census to seed the allowlist so FR-016 lands green, and lands **after** IC-01 repoints
+ FR-005c resolver (sink ordering).

## D7 — FR-010 packs out-of-tree mechanism: hatchling build hook; the spike MUST run

`packs/` is a repo-root `doctrine`-sibling; a naive `force-include ../../packs` escapes the project root and
hatchling refuses it. `_resolve_built_in` (`pack_paths.py:195`, step 3) expects `files("doctrine").parent /
"packs" / "built-in"` (a site-packages sibling — the monorepo wheel already achieves this via root
`force-include`). The doctrine wheel's `kernel` dependency is a **real import-closure need** (`resolver.py:32`,
`missions/primitives.py`, `shared/schema_utils.py` all `from kernel...`). **Decision:** use a hatchling custom
build hook (`hatch_build.py` implementing `BuildHookInterface.initialize`, injecting a computed absolute
`force_include` for the sibling `packs/`). **Guard (must fold):** the FR-010 closure test proves manifest
**shape** only (C-002 forbids CI building the nested wheel), so WP acceptance MUST include an **actually
executed** `hatch build` of the nested doctrine wheel with the built wheel showing `packs/built-in/` as a
`doctrine` sibling — recorded here — else the groundwork is inert.

### D7 spike result

- Status: **PENDING** — to be executed and recorded by the owning WP (WP15). Expected mechanism: build hook as
  above. If the hook approach fails the real build, fall back options: (i) a thin `MANIFEST`/data-dir copy at
  build time, (ii) declare the mechanism and defer the *functional* packs-carry to the cutover follow-on while
  still shipping the kernel-dep closure now (narrower groundwork). The WP records the chosen, build-verified
  mechanism here.

## D8 — Sequencing (dependency DAG, no cycles)

`FR-005a→FR-005b→FR-005c`; `FR-007 census→publish reader→{routing lanes}`; `packs-spike→FR-010`;
`{IC-01 repoints, FR-005c}→FR-016 (sink)`; `FR-012→FR-014 (#3102 closeout)`. Free parallel first-wave:
the 4 IC-01 repoints, FR-008, FR-009 kernel pyproject, FR-012/FR-013 CI hygiene, FR-011 ADR (soft-after
FR-008). Critical path (depth): the IC-02 chain. Width long-pole: IC-03 routing. FR-015 is a **timeboxed
investigation with a deferred issue-matrix verdict**, not a code WP (default defer-with-reason).

## D9 — Tracker hygiene (DIR-012 + coord issue-matrix)

Each folded issue (#3150, #3140, #3149, #3107, #3102) gets an issue-matrix row (coord worktree) **and** a
DIR-012 HiC assignment + mission-naming tracker comment when its owning WP starts. Memory: WP approval
hard-fails until each row's verdict is filled in the coord worktree — `tasks-finalize` seeds the rows.
