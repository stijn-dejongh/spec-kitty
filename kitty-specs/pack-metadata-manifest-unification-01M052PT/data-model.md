# Data Model: Pack-Metadata Manifest Unification

Entities and their fields for the unified pack-metadata design (ADR 2026-08-16-1).
Two files per pack: an **authored** descriptor and a **generated** manifest.

## PackDescriptor  *(authored — `pack.yaml`; never machine-rewritten)*

| Field | Type | Notes |
|---|---|---|
| `pack_id` | ULID (26 chars) | Stable, **immutable** identity. Minted once (mirrors `mission_id`). |
| `pack_version` | semver string | Author-managed pack version. |
| `parent_pack` | ULID \| null | Edge only → parent `pack_id`. Resolved by `org_extends`. |
| `accompanies_doctrine_pack` | ULID \| null | Charter-pack → doctrine-pack pack-level binding (was per-activation `doctrine_pack_id`). |
| `name` | string | Human handle (retained; no longer the identity key). |

Invariants: `pack_id` immutable once set; `parent_pack`/`accompanies_doctrine_pack` are **edges**, not resolved orders — a cycle is caught by `org_extends`, not a new walker.

## PackManifest  *(generated — `pack-manifest.yaml`; never hand-authored, NFR-004)*

| Field | Type | Notes |
|---|---|---|
| `schema_version` | string | Version-gates any shape change (DIR-018). |
| `generated_by` / `generated_at` | string | Provenance of the generation run. |
| `manifest_hash` | sha256 | Self-integrity over the manifest (reuse `manifest.py:107`). |
| `constituents` | list[Constituent] | The canonical enumerated inventory. |
| `charter` | CharterProfile \| absent | Optional profile block for charter packs only. |

Derived (not stored): `artifact_counts` — computed from `constituents` for legacy callers (Q1 compat view).
Invariant: regeneration for an unchanged pack is byte-identical (NFR-003) — constituents sorted by `(kind, id)`.

## Constituent  *(element of `PackManifest.constituents`)*

| Field | Type | Notes |
|---|---|---|
| `kind` | ArtifactKind | e.g. `directive`, `tactic`, `agent_profile`. |
| `id` | string (URN or bare id) | Canonical artifact id within its kind. |
| `path` | string (POSIX) | Repo-relative path to the artifact source. |
| `content_hash` | sha256 | Per-artifact tamper-evidence (trust substrate, #2539). |

## CharterProfile  *(optional block on a charter pack's manifest)*

| Field | Type | Notes |
|---|---|---|
| `mission_id` | ULID | From the synthesizing mission. |
| `bundle_content_hash` | sha256 | Existing charter bundle hash. |
| `synthesizer_version` | string | Existing synthesizer provenance. |

These are today's `synthesis-manifest.yaml` fields (`manifest.py:46-112`), relocated onto the unified schema as a profile so the charter pack stops being a forked format.

## Relationships

```
PackDescriptor(pack_id) ──parent_pack──▶ PackDescriptor(pack_id)      [resolved by org_extends]
PackDescriptor(charter) ──accompanies_doctrine_pack──▶ PackDescriptor(doctrine pack)
PackDescriptor 1───1 PackManifest        (same pack root; authored vs generated)
PackManifest 1───N Constituent
PackManifest 0/1─── CharterProfile       (charter packs only)
```

## Migration inputs (read-only, not re-emitted)

- Legacy org `pack-manifest.yaml` `artifact_counts` (`snapshot.py:195`) → superseded by the derived view.
- Legacy `synthesis-manifest.yaml` (`manifest.py`) → becomes the charter pack's `pack-manifest.yaml` instance.
- Packs keyed by config `name` (`org_pack_config.py:166`) → gain a `pack_id` (built-in first; Q2).
