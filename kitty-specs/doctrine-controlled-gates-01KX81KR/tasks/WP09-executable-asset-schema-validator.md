---
work_package_id: WP09
title: Executable ASSET schema + validator
dependencies:
- WP01
requirement_refs:
- FR-004
- FR-005
- C-003
tracker_refs:
- '2535'
planning_base_branch: design/doctrine-controlled-gates
merge_target_branch: design/doctrine-controlled-gates
branch_strategy: Planning artifacts for this mission were generated on design/doctrine-controlled-gates. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into design/doctrine-controlled-gates unless the human explicitly redirects the landing branch.
subtasks:
- T038
- T039
- T040
- T041
phase: Lane D - Path B
history:
- at: '2026-07-11T00:00:00Z'
  actor: claude
  action: created
agent_profile: python-pedro
authoritative_surface: src/doctrine/assets/
execution_mode: code_change
owned_files:
- src/doctrine/assets/models.py
- src/specify_cli/doctrine/pack_validator.py
- tests/doctrine/assets/test_gate_asset_schema.py
create_intent:
- tests/doctrine/assets/test_gate_asset_schema.py
role: implementer
tags: []
task_type: implement
---

# WP09 — Executable ASSET schema + validator *(Lane D, Path B, foundational)*

## Objective

Extend the **existing** `AssetManifest` domain model and the pack validator with
the *executable gate-asset shape* — the schema half of Path-B. This is the first
WP of Lane D: it introduces the shape that keys code execution (WP10 runs it,
WP11 confines it), while keeping **every non-gate asset inert** (C-003). No code
is executed in this WP; it is schema + static validation only.

## Context

Path-B (doctrine-supplied executable gate assets) has **no substrate today**.
The ASSET kind is deliberately inert: `AssetManifest` carries only an
identity/well-formedness contract (`id`, `mime`, `path`, optional `title`;
`src/doctrine/assets/models.py:27-53`) and the two teeth of the loose contract —
path containment + mime consistency — live in the pack validator
(`pack_validator._validate_asset_manifests`), not on the model. ASSET is
non-activatable by construction (`artifact_kinds.py` `_NON_AUGMENTATION_ELIGIBLE_KINDS = {TEMPLATE, ASSET}`).

Per research §3, Path-B is **EXTEND, not greenfield**: the schema and validation
are *extensions* of that existing surface. The design mandate (C-003) is that
code execution is a **new, distinct capability keyed on the gate-asset shape** —
NOT a generalization of asset loading. A plain `*.asset.yaml` (an image, a font,
a fixture) must remain a passive blob descriptor forever; only the specific
executable shape (an `entrypoint` + allowlisted `interpreter` + dedicated
`verdict_channel`) tells the downstream runner "this asset may run". If shape
detection is loose, an ordinary asset could be coaxed into execution — that is
the C-003 regression this WP exists to prevent.

Because `AssetManifest` is `extra="forbid"` and frozen, adding fields is a
**versioned schema evolution** (mirrors FR-016/SC-009 for assets): existing
plain manifests without the new fields MUST still load unchanged. The new fields
are therefore all optional, and "is this a gate asset?" is a derived predicate
over their presence/coherence — not a required discriminator that would break
old manifests.

This WP feeds WP10 (repository/resolver/runner consume the validated shape) and
ultimately SC-006/SC-007 (only a well-formed executable gate asset can ever be a
candidate for execution).

## Ordered steps

### T038 — Extend `AssetManifest` with the executable gate-asset shape + `TrustEnvelope` protocol

1. In `src/doctrine/assets/models.py`, add the three optional fields to
   `AssetManifest` (keep `model_config = ConfigDict(frozen=True, extra="forbid")`):
   - `entrypoint: str | None = None` — a `module:function` reference or a script
     path *inside the asset* (relative to `path`). Never shell-interpolated.
   - `interpreter: str | None = None` — a member of the interpreter allowlist
     (e.g. `"python"`); shape only here, allowlist *membership* is enforced by
     the trust envelope (WP11), not this model.
   - `verdict_channel: str | None = None` — a `const`-style marker declaring the
     asset emits its `GateVerdict` on the dedicated, size-capped, schema-validated
     channel (FR-019), NOT shared stdout. Accept a single canonical literal
     (e.g. `"fd3"` / `"verdict-file"`; pick one and pin it) and reject anything
     else at validate time (T039), not here.
2. Add a `TrustEnvelope` **Protocol** (typing-only structural contract) to a new
   `src/doctrine/assets/models.py` protocol block *or* re-declare it where the
   runner (WP10) and trust module (WP11) can both import it without a cycle.
   Keep it a `Protocol` — the concrete policy object lands in WP11
   (`assets/trust.py`). The protocol pins the surface WP10's runner will depend
   on: `provenance`, `allow_flag`, `interpreter_allowlist`, `env_allowlist`,
   `timeout_s`, `process_group_kill`, `rlimits`, `fs_confinement`,
   `capability_probe` (see data-model `TrustEnvelope`). Do **not** implement it.
3. Keep `src/doctrine/assets/` free of any `specify_cli` import (arch gate) — the
   model and protocol are pure `doctrine`-layer types.
4. Add a module-level helper predicate `is_executable_gate_asset(manifest) -> bool`
   that returns `True` iff **all three** new fields are present and non-empty.
   This is the single canonical shape test both the validator (T039) and WP10's
   resolver reuse — do not duplicate the predicate at call sites.

### T039 — Gate-asset-shape detection in `_validate_asset_manifests` (keys code-exec)

1. In `src/specify_cli/doctrine/pack_validator.py`, extend
   `_validate_asset_manifests` (currently: path-containment + mime consistency
   only). After the existing containment/mime checks for each manifest, branch on
   the gate-asset shape:
   - If **none** of `entrypoint`/`interpreter`/`verdict_channel` are present →
     plain asset → run the existing checks only, emit nothing new (inert; C-003).
   - If **all three** are present → executable gate-asset shape → run the
     additional gate-asset validations below.
   - If **some but not all** are present → this is a *malformed* gate asset →
     emit an `error` `ValidationIssue` (category e.g. `gate_asset_shape_incomplete`)
     naming the missing field(s). Partial shape must never silently degrade to
     either "plain asset" (would hide author intent) or "executable" (would run an
     under-specified asset). This is the load-bearing C-003 boundary.
2. Gate-asset validations (all as `ValidationIssue`s, mirroring the existing
   `_check_asset_*` helper style — one small helper per check, ≤ C(15)):
   - `interpreter` ∈ the interpreter allowlist constant (define the allowlist as
     a module constant, e.g. `_GATE_ASSET_INTERPRETER_ALLOWLIST = frozenset({"python"})`).
   - `verdict_channel` == the single canonical literal.
   - `entrypoint` shape: either `module:function` (both sides non-empty) or a
     relative script path that stays under the asset's own directory (reuse the
     existing containment primitive `resolve_relative_path_within_root` against
     the asset's resolved root — do NOT hand-roll a sixth resolve/`relative_to`).
3. Hoist any string/message/category that appears ≥3 times to a named module
   constant (Sonar S1192). Keep each new helper's complexity ≤ 15.
4. Do **not** wire any execution here — this function only *classifies and
   validates*. Detection keys code-exec downstream (WP10 asks
   `is_executable_gate_asset`), it does not perform it.

### T040 — Red-first: a plain `*.asset.yaml` is NOT treated as executable

1. Add `tests/doctrine/assets/test_gate_asset_schema.py`. Write this test
   **first** and watch it fail against pre-WP code (the fields/predicate don't
   exist yet), then make it pass.
2. Build a realistic plain asset manifest fixture (e.g. an `image/png` logo:
   `id`, `mime`, `path`, `title` — production-shaped, not `foo`/`bar`). Assert:
   - `AssetManifest(**data)` loads unchanged (schema evolution back-compat,
     FR-016 mirror).
   - `is_executable_gate_asset(manifest)` is `False`.
   - `_validate_asset_manifests` emits **no** new gate-asset issue for it (only
     the pre-existing containment/mime behavior).

### T041 — Red-first: an executable gate-asset shape validates

1. In the same test module, add the executable-shape case. Red-first: assert the
   validated executable manifest is *recognized* before the detection branch
   exists.
2. Fixtures + assertions:
   - A well-formed gate asset (`entrypoint: "gate:evaluate"`, `interpreter: "python"`,
     `verdict_channel: <canonical literal>`, valid `path`/`mime`) → loads,
     `is_executable_gate_asset` is `True`, `_validate_asset_manifests` emits **no**
     error for it.
   - A malformed gate asset (only `entrypoint` present) → `_validate_asset_manifests`
     emits exactly one `gate_asset_shape_incomplete` error naming the missing
     fields; `is_executable_gate_asset` is `False`.
   - Bad `interpreter` (e.g. `"bash"`) with the rest present → one
     `error`-severity issue; not admitted as runnable.
   - Bad `verdict_channel` literal → one `error`-severity issue.
3. Run `ruff check` + `mypy` on the two owned source files; zero issues, no new
   `# noqa`/`# type: ignore`.

## Acceptance

- **Schema evolution / back-compat**: every pre-WP plain `*.asset.yaml` still
  loads and validates with no new issues (T040) — the `extra="forbid"` model
  gains only optional fields.
- **C-003 preserved**: `is_executable_gate_asset` is the single canonical shape
  predicate; a plain asset is `False` and emits no gate-asset validation; a
  *partial* shape is a hard validation `error`, never silently "plain" or
  "executable" (T039/T041). Feeds SC-006 (only a genuine gate asset is even a
  candidate for the WP11 trust checks).
- **No execution introduced**: this WP performs zero `subprocess`/`exec`; it only
  classifies and statically validates. (Runner is WP10; confinement is WP11.)
- `ruff`/`mypy` clean on `src/doctrine/assets/models.py` and
  `src/specify_cli/doctrine/pack_validator.py`; every new branch/helper has a
  focused test in `tests/doctrine/assets/test_gate_asset_schema.py`.

## Safeguards

- **EXTEND, never greenfield.** Add fields/branches to the existing
  `AssetManifest` + `_validate_asset_manifests`; do not stand up a parallel
  gate-asset model or a second validator. The loose-contract ASSET posture is
  canonical — you are widening it by exactly one keyed shape.
- **C-003 is the whole point.** Code-exec is keyed strictly on the *complete*
  executable shape. Never let presence of a single field, or a permissive
  default, flip a plain asset into "runnable". Partial shape → validation error.
- **No `specify_cli` import from `src/doctrine`** — the model + `TrustEnvelope`
  Protocol are pure doctrine-layer types (arch gate: `src/doctrine` must not
  import `specify_cli`).
- **The Protocol is a contract, not an implementation.** `TrustEnvelope` here is
  typing-only; the concrete envelope + all real containment is WP11. Do not leak
  any `os.environ`, `subprocess`, `setrlimit`, or path-confinement logic into
  this WP.
- **Realistic fixtures** — production-shaped ids/paths/mimes, not placeholders,
  so the tests exercise real detection behavior.

## References

- `src/doctrine/assets/models.py:27-53` — `AssetManifest` (the model to EXTEND;
  `frozen=True, extra="forbid"`).
- `src/specify_cli/doctrine/pack_validator.py` — `_validate_asset_manifests`
  (≈`:604`) + `_check_asset_path_containment` / `_check_asset_mime` (the helper
  style to mirror; reuse `resolve_relative_path_within_root`).
- `doctrine.drg.org_pack_config.resolve_relative_path_within_root` — the shared
  containment primitive (do not hand-roll a new resolve/`relative_to`).
- data-model.md → `GateAsset` (new schema; extends `AssetManifest`) and
  `TrustEnvelope` (the Protocol surface WP10/WP11 depend on).
- contracts/gate-asset-entrypoint-and-trust.md → "Entrypoint contract" +
  "Non-gate assets remain inert" (C-003).
- research.md §3 — "ASSET is inert today … EXTEND … keys code-exec so non-gate
  assets stay inert (C-003)".
