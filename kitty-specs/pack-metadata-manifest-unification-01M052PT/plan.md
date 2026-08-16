# Implementation Plan: Pack-Metadata Manifest Unification

**Branch**: `feat/pack-metadata-manifest-unification` | **Date**: 2026-08-16 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `kitty-specs/pack-metadata-manifest-unification-01M052PT/spec.md`

## Summary

Unify pack metadata onto **one** canonical manifest schema for every pack type (built-in, org, fetched, charter), replacing the two divergent formats that ship today — per-kind `artifact_counts` for org packs (`src/specify_cli/doctrine/snapshot.py:157-212`) and enumerated `artifacts[]` for charter bundles (`src/charter/synthesizer/manifest.py:46-112`). The enumerated shape is promoted to the canonical `constituents[]`; identity/lineage become authored data in a `pack.yaml`/`pack.md` pair, distinct from the generated `pack-manifest.yaml`; lineage resolution delegates to the existing `org_extends` resolver. Ratified by ADR `docs/adr/3.x/2026-08-16-1-pack-metadata-manifest-unification.md`.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: internal only — `specify_cli.doctrine` (snapshot/pack config), `charter.synthesizer.manifest`, `charter.org_extends`, `doctrine.resolver`; `ruamel.yaml` for round-trip YAML; ULID minting reused from the mission-identity model.
**Storage**: YAML files on disk — authored `pack.yaml`/`pack.md` + generated `pack-manifest.yaml` at each pack root; `packs/built-in/` for the reference pack.
**Testing**: `pytest` (unit for schema/derivation/hashing; architectural test for the C-005 no-parallel-resolver ratchet; contract test for the pack-layout no-author-edit rule).
**Target Platform**: Linux/macOS/Windows CLI (DIR-001 cross-platform).
**Project Type**: single (CLI/library).
**Performance Goals**: manifest generation is build/upgrade-time, not hot-path; determinism > speed.
**Constraints**: deterministic/idempotent generation (0-byte re-run diff); 0 new lineage resolvers; 0 counts-consumer regressions; generated file never hand-authored.
**Scale/Scope**: 1 built-in pack (~14 kinds), N org/fetched packs, 1 charter bundle profile; ~2–3 core surfaces + a long non-blocking tail (out of scope, deferred to #2721).

## Charter Check

Gates in scope (software-dev-default, DIR-001…013):
- **DIR-001 cross-platform** — YAML paths POSIX-normalized; no OS-specific manifest paths.
- **DIR-010/011 identifier safety** — `pack_id` is ULID (ASCII); `kind`/`id` in constituents are canonical URNs.
- **Single-canonical-authority** (charter principle) — this mission *is* that principle applied to pack metadata; the C-005 ratchet enforces the "no parallel resolver" half.
- **DIR-018 doctrine versioning** — `schema_version` on the manifest; a version bump gates any future shape change.

No charter violation; the mission removes a canonical-authority violation (two manifests) rather than introducing one.

## Project Structure

### Documentation (this mission)
```
kitty-specs/pack-metadata-manifest-unification-01M052PT/
  spec.md            # done
  plan.md            # this file
  data-model.md      # manifest + descriptor + constituent + lineage-edge entities
  research/          # ADR corroboration is the research (docs/adr/3.x/2026-08-16-1)
  tasks/             # authored at /spec-kitty.tasks
```

### Source Code (repository root)
```
src/specify_cli/doctrine/
  snapshot.py            # retire artifact_counts as stored; write enumerated constituents
  pack_manifest.py       # NEW: the unified schema model + read/derive-counts view
  pack_descriptor.py     # NEW: authored pack.yaml model (pack_id, pack_version, lineage edges)
  builtin_manifest.py    # NEW: generator emitting pack-manifest.yaml from packs/built-in/*.graph.yaml
  org_pack_config.py     # key by pack_id (not just name)
src/charter/
  synthesizer/manifest.py  # becomes the charter profile instance of the unified schema
  org_extends.py           # unchanged authority; parent_pack resolution delegates here
packs/built-in/
  pack.yaml                # NEW authored descriptor (pack_id, version)
  pack-manifest.yaml       # NEW generated manifest (constituents from the *.graph.yaml nodes)
tests/
  doctrine/test_pack_manifest_schema.py, test_builtin_manifest.py, test_counts_derivation.py
  architectural/test_pack_lineage_no_parallel_resolver.py   # C-005 ratchet
  contracts/test_pack_layout_no_author_edit.py
```

## Complexity Tracking

| Concern | Why it exists | Why simpler is insufficient |
|---|---|---|
| A separate `pack.yaml` (authored) vs `pack-manifest.yaml` (generated) | The pack-layout contract forbids authors editing the generated file (`pack-layout.md:104`) | A single fenced-block file requires the generator to preserve authored regions — fragile; two files make the boundary structural. |
| A `charter:` profile block instead of a separate charter schema | Charter bundle carries 3 extra fields | A forked charter schema re-creates the two-format split the mission exists to remove. |

## Implementation Concern Map

### IC-01 — Unified manifest schema + enumerated constituents  *(WP-core → #3500; FR-001, FR-004, FR-009; C-001)*
- **Purpose**: define the single `pack-manifest` schema (`schema_version`, `generated_by/at`, `manifest_hash`, `constituents:[{kind,id,path,content_hash}]`, optional `charter:` profile) and its reader.
- **Affected surfaces**: NEW `doctrine/pack_manifest.py`; adapt `charter/synthesizer/manifest.py` to emit this schema as the charter instance.
- **Sequencing/depends-on**: none (foundation).
- **Risks**: charter profile must remain optional so non-charter packs validate; reuse `manifest_hash` logic from `manifest.py:107` rather than a second hasher.

### IC-02 — Built-in pack manifest generator  *(WP-core → #3500; FR-002; SC-002)*
- **Purpose**: emit `pack-manifest.yaml` for `packs/built-in/` from the per-kind `*.graph.yaml` `nodes:`, wired into the build/upgrade path.
- **Affected surfaces**: NEW `doctrine/builtin_manifest.py`; hook into the build/upgrade step.
- **Sequencing/depends-on**: IC-01.
- **Risks**: determinism — stable ordering of constituents (sort by `kind` then `id`) so re-runs are byte-identical (NFR-003).

### IC-03 — Retire stored `artifact_counts`; derived-count view  *(WP-core → #3500; FR-003; NFR-002; Q1 = compat view)*
- **Purpose**: stop persisting `artifact_counts` (`snapshot.py:195`); expose counts derived from `constituents[]` for existing callers.
- **Affected surfaces**: `snapshot.py`; a `counts_from(constituents)` helper; existing count readers keep their interface via the derived view.
- **Sequencing/depends-on**: IC-01.
- **Risks**: **Q1 boundary** — this mission ships the derived view + keeps stored counts as migration input only; full reader migration is a fast-follow. Enumerate every current `artifact_counts` reader and pin them green (NFR-002).

### IC-04 — Stable `pack_id` identity  *(WP-identity → #3501; FR-005; C-004)*
- **Purpose**: mint a stable, immutable `pack_id` (ULID, mirroring the mission-identity model); key lineage/trust on it, not config `name` (`org_pack_config.py:166`).
- **Affected surfaces**: NEW `doctrine/pack_descriptor.py`; `org_pack_config.py`.
- **Sequencing/depends-on**: IC-01. **Q2 boundary** — built-in pack first; org/fetched backfill as coverage extends.
- **Risks**: immutability — mint once, never regenerate; backfill must be idempotent.

### IC-05 — Lineage edges, delegated resolution  *(WP-lineage → #3502; FR-006, FR-007; NFR-001; C-002)*
- **Purpose**: store `parent_pack` + `accompanies_doctrine_pack` edges on the authored descriptor; resolve order **only** via `org_extends.resolve_extends_order`; `accompanies_doctrine_pack` gives the pack-level charter→doctrine binding missing today (only per-activation `doctrine_pack_id`, `activations.py:241`).
- **Affected surfaces**: `pack_descriptor.py`; a read path that calls `org_extends`; NEW architectural test asserting no second resolver.
- **Sequencing/depends-on**: IC-04.
- **Risks**: the C-005 ratchet — any new traversal fails the arch test; reuse the existing cycle detection.

### IC-06 — Authored/generated two-file split  *(WP-split → #3503; FR-008; NFR-004; C-005)*
- **Purpose**: authored `pack.yaml`(+`pack.md`) holds identity/lineage; generated `pack-manifest.yaml` holds constituents/hashes; regeneration never touches the authored files.
- **Affected surfaces**: `pack_descriptor.py` (authored read); the generators (IC-02/IC-03 write only the generated file); contract test for no-author-edit.
- **Sequencing/depends-on**: IC-01 (schema), IC-04 (descriptor fields).
- **Risks**: ensure every writer targets only `pack-manifest.yaml`; a byte-unchanged assertion on `pack.yaml`/`pack.md` across regeneration (NFR-004).

### Concern dependency graph
```
IC-01 (schema) ── IC-02 (built-in writer)
              ├── IC-03 (counts derive)
              └── IC-04 (pack_id) ── IC-05 (lineage)
                                 └── IC-06 (two-file split)
```
Maps to WPs: **WP-core = IC-01+IC-02+IC-03 (#3500)**; WP-identity = IC-04 (#3501); WP-lineage = IC-05 (#3502); WP-split = IC-06 (#3503). #3501/#3502/#3503 `blocked_by` #3500.

## Risks & Mitigations

- **Counts-reader migration deeper than expected (Q1).** Mitigation: ship the derived view first; enumerate readers in IC-03 and pin them green; defer full reader migration if the set is large (operator-confirmed at this plan).
- **A second lineage walker sneaks in (C-005).** Mitigation: architectural test in IC-05 fails on any new traversal; resolution routes through `org_extends` only.
- **Non-determinism in generation.** Mitigation: stable sort + a 0-byte re-run diff test (NFR-003).
- **ADR/docs not yet on base.** The ratifying ADR lives on PR #3480; if it merges after this mission's base is cut, the reference is by-path and resolves on merge. Non-blocking.
