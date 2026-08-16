---
work_package_id: WP04
title: Authored/generated split + pack_version relocation
dependencies:
- WP01
- WP02
requirement_refs:
- FR-008
planning_base_branch: feat/pack-metadata-manifest-unification
merge_target_branch: feat/pack-metadata-manifest-unification
branch_strategy: Planning artifacts for this mission were generated on feat/pack-metadata-manifest-unification. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/pack-metadata-manifest-unification unless the human explicitly redirects the landing branch.
subtasks:
- T014
- T015
- T016
history:
- at: '2026-08-16'
  note: Authored at /spec-kitty.tasks. Parallel with WP03 after WP02.
agent_profile: python-pedro
authoritative_surface: packs/built-in/
create_intent:
- packs/built-in/pack.yaml
- packs/built-in/pack.md
- tests/architectural/test_pack_manifest_no_author_edit.py
- tests/doctrine/test_pack_version_relocation.py
execution_mode: code_change
owned_files:
- packs/built-in/pack.yaml
- packs/built-in/pack.md
- src/specify_cli/doctrine/pack_assembler.py
- src/specify_cli/cli/commands/doctor.py
- tests/architectural/test_pack_manifest_no_author_edit.py
- tests/doctrine/test_pack_version_relocation.py
role: implementer
tags: []
tracker_refs: []
---

## ⚡ Do This First: Load Agent Profile

Load your assigned profile first: `/ad-hoc-profile-load python-pedro` (or `spec-kitty agent profile show python-pedro` + `spec-kitty charter context --action implement --json`).

## Objective

Complete the two-file split: create the authored `pack.yaml`/`pack.md` for the built-in pack, and **relocate `pack_version`** off the generated file (which the generator no longer emits, per WP01) to the authored descriptor — switching the two consumers to read it there. Pin the no-author-edit contract.

## Context

Design: [plan.md](../plan.md) IC-06 + [data-model.md](../data-model.md). `write_pack_manifest` writes `pack_version` into the **generated** file today (`snapshot.py:172`); consumers read it there: `pack_assembler.py:390`, `doctor.py:1098` (`_resolve_pack_version`). WP01 already reserved the `pack.yaml` path (generator writes only `pack-manifest.yaml`). The pack-layout contract forbids authoring the generated file (`pack-layout.md:104`).

## Subtasks

### T014 — Authored `pack.yaml` / `pack.md` for the built-in pack
Write `packs/built-in/pack.yaml` (authored `PackDescriptor` from WP02's model: `pack_id`, `pack_version`, `parent_pack`, `accompanies_doctrine_pack`, `name`) and `packs/built-in/pack.md` (human-readable pack description). These are the authored half of the split.

### T015 — Relocate `pack_version` to authored; switch consumers
Move `pack_version` to the authored descriptor. Switch `pack_assembler.py:390` and `doctor.py:1098` (`_resolve_pack_version`) to read `pack_version` from the authored `pack.yaml`, **not** the generated manifest. Keep genuine generated provenance (`source_url`/`source_type`/`fetched_at`) on the generated file. Test: `test_pack_version_relocation.py` — consumers resolve the authored value; the generated manifest no longer carries `pack_version`.

### T016 — No-author-edit contract test [P]
Create `tests/architectural/test_pack_manifest_no_author_edit.py`: regenerate the built-in pack's manifest and assert `packs/built-in/pack.yaml` and `pack.md` are **byte-unchanged** (NFR-004); assert the generator writes only `pack-manifest.yaml`.

## Definition of Done
- Authored `pack.yaml`/`pack.md` exist; `pack_version` resolves from the authored descriptor for both consumers; generated file no longer carries it; regen leaves authored files byte-unchanged; `ruff`/`mypy` clean; new branches tested.

## Reviewer guidance
Confirm no consumer still reads `pack_version` from the generated manifest; confirm the byte-unchanged assertion is real (regenerate and diff); confirm generated provenance fields stay put.
