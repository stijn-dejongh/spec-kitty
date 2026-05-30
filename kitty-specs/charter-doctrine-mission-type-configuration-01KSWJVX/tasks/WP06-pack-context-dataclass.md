---
work_package_id: WP06
title: PackContext dataclass + charter wiring
dependencies:
- WP05
requirement_refs:
- FR-007
tracker_refs: []
planning_base_branch: feat/doctrine-mission-type-spec-01KSWJVX
merge_target_branch: feat/doctrine-mission-type-spec-01KSWJVX
branch_strategy: feature-branch
subtasks:
- T036
- T037
- T038
- T039
- T040
agent: claude
history:
- at: '2026-05-30T17:21:57Z'
  event: created
  note: Initial task breakdown
agent_profile: architect-alphonso
authoritative_surface: src/charter/pack_context.py
execution_mode: code_change
owned_files:
- src/charter/pack_context.py
- src/charter/__init__.py
- tests/charter/test_pack_context.py
role: implementer
tags: []
---

## ⚡ Do This First: Load Agent Profile

Before reading anything else, load your agent profile:

/ad-hoc-profile-load architect-alphonso

This profile contains the coding standards, testing requirements, and
architectural constraints you must follow throughout this work package.

---

# Work Package Prompt: WP06 — PackContext dataclass + charter wiring

## Context

C-005 requires that the doctrine resolver never reads `.kittify/config.yaml` directly. Instead, the charter module constructs a `PackContext` object from the validated pack set and passes it to the doctrine resolver. The resolver uses `PackContext` as its sole source of truth for pack locations and activation state.

`PackContext` is a frozen dataclass — immutable after construction. It is the "pre-validation token" that proves the charter has already validated the pack set before doctrine sees it.

## Objective

Implement `PackContext` as a frozen dataclass in `src/charter/pack_context.py`, implement the charter-side constructor that builds it from `.kittify/config.yaml`, wire it into existing doctrine resolver calls in `charter/`, and replace any direct `config.yaml` reads inside the resolver.

## PackContext Specification

```python
# src/charter/pack_context.py
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class PackContext:
    """Pre-validated pack set constructed by the charter module.

    The doctrine resolver receives this; it never reads .kittify/config.yaml directly.
    Invariant: constructed by charter module only (C-005).
    """
    activated_kinds: frozenset[str]
    """Artifact kinds explicitly activated in the project charter."""

    activated_mission_types: frozenset[str]
    """Mission type IDs activated in the project charter."""

    pack_roots: tuple[Path, ...]
    """Ordered pack root paths: built-in first, then org packs in config order."""

    org_pack_names: tuple[str, ...]
    """Org pack names as declared in config.yaml."""

    repo_root: Path
    """Repository root path (for resolving project-layer overrides)."""


__all__ = ["PackContext"]
```

## Subtasks

### T036 — Implement PackContext frozen dataclass

Create `src/charter/pack_context.py` with the `PackContext` dataclass exactly as specified above.

All fields must have type annotations. The dataclass must be `frozen=True` (immutable). No mutable defaults (use `frozenset` and `tuple`, not `set` and `list`).

### T037 — Add __all__ and type annotations

Verify all fields are fully type-annotated (mypy --strict will check).

Add `__all__ = ["PackContext"]` at the module level.

Export `PackContext` from `src/charter/__init__.py` so it is accessible as `charter.PackContext`.

### T038 — Implement charter-side constructor

Add a factory function or classmethod `PackContext.from_config(repo_root: Path) -> PackContext`:

```python
@classmethod
def from_config(cls, repo_root: Path) -> "PackContext":
    """Construct a PackContext from .kittify/config.yaml.

    Reads the project charter activation state and pack roots.
    Raises if config.yaml references pack names that cannot be resolved.
    """
    ...
```

Implementation:
1. Read `.kittify/config.yaml` to get the list of configured org pack names and activated artifact kinds
2. Resolve `pack_roots` in order: `[builtin_doctrine_root, ...org_pack_roots...]`
3. Determine `activated_mission_types` from the charter's activation section (if present; default to all built-ins if absent — consistent with FR-019 intent)
4. Construct and return the frozen dataclass

The built-in doctrine root is `Path(__file__).parent.parent.parent / "doctrine"` (relative to `src/charter/`).

### T039 — Wire PackContext into existing charter resolver calls

Find all places in `src/charter/` where `.kittify/config.yaml` is read directly inside what will become the doctrine resolver path.

Replace those reads with `PackContext.from_config(repo_root)` calls that feed the `PackContext` to the resolver. Specifically:

- `src/charter/drg.py` — if it reads config.yaml for pack locations, replace with PackContext
- `src/charter/activations.py` — if it reads config.yaml for activation state, replace with PackContext
- Any other charter module that reads config.yaml inside a doctrine resolution path

Ensure no doctrine-layer code receives or reads `config.yaml` directly after this change.

### T040 — Unit tests for PackContext

Write `tests/charter/test_pack_context.py`:

Test cases:
- `PackContext.from_config(repo_root)` with a minimal config.yaml produces correct `activated_mission_types`
- `PackContext.from_config(repo_root)` with no config.yaml returns fallback PackContext with all built-in mission types
- `PackContext` is immutable: attempting to set a field raises `FrozenInstanceError`
- `pack_roots` is a `tuple` (not list), ensuring immutability
- `activated_kinds` is a `frozenset`
- `PackContext` can be used as a dict key (frozen dataclasses are hashable)

## Acceptance Criteria

- [ ] `PackContext` dataclass exists in `src/charter/pack_context.py` and is exported from `src/charter/__init__.py`
- [ ] All fields are immutable types (`frozenset`, `tuple`)
- [ ] `PackContext.from_config()` builds a correct context from `.kittify/config.yaml`
- [ ] No doctrine-layer module reads `.kittify/config.yaml` directly after this WP
- [ ] `tests/charter/test_pack_context.py` passes
- [ ] `mypy --strict` clean

## References

- FR-007: Charter as source of truth for dispatch
- C-005: PackContext isolation constraint
- data-model.md §"PackContext"
