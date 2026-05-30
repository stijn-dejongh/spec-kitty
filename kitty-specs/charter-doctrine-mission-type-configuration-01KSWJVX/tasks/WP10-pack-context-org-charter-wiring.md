---
work_package_id: WP10
title: PackContext wiring into OrgCharterPolicy loader
dependencies:
- WP09
requirement_refs:
- FR-001
- FR-003
tracker_refs: []
planning_base_branch: feat/doctrine-mission-type-spec-01KSWJVX
merge_target_branch: feat/doctrine-mission-type-spec-01KSWJVX
branch_strategy: feature-branch
subtasks:
- T061
- T062
- T063
- T064
- T065
agent: claude
history:
- at: '2026-05-30T17:21:57Z'
  event: created
  note: Initial task breakdown
agent_profile: python-pedro
authoritative_surface: src/specify_cli/doctrine/org_charter.py
execution_mode: code_change
owned_files:
- src/specify_cli/doctrine/org_charter.py
- src/charter/pack_context.py
- tests/specify_cli/doctrine/test_org_charter_pack_context.py
role: implementer
tags: []
---

## ⚡ Do This First: Load Agent Profile

Before reading anything else, load your agent profile:

/ad-hoc-profile-load python-pedro

This profile contains the coding standards, testing requirements, and
architectural constraints you must follow throughout this work package.

---

# Work Package Prompt: WP10 — PackContext wiring into OrgCharterPolicy loader

## Context

WP09 implemented the `extends:` chain resolver in isolation. This WP wires it into the actual loader: `load_org_charter_policies()` receives a `PackContext` (from WP06), uses it to locate org packs, and runs each pack through `_resolve_chain()` before merging. The resolver never reads `.kittify/config.yaml` directly — all data flows through `PackContext`.

## Objective

Update `load_org_charter_policies()` signature to accept `PackContext`. Wire `_resolve_chain()` to use `PackContext.pack_roots` for pack location lookup. Update all callers. Write integration tests covering full chain resolution and backward compatibility.

## Subtasks

### T061 — Update load_org_charter_policies() signature

In `src/specify_cli/doctrine/org_charter.py`:

Before:
```python
def load_org_charter_policies(repo_root: Path) -> list[OrgCharterPolicy]:
```

After:
```python
def load_org_charter_policies(
    repo_root: Path,
    pack_context: PackContext | None = None,
) -> list[OrgCharterPolicy]:
```

The `PackContext | None` default maintains backward compatibility: if `None`, fall back to reading `.kittify/config.yaml` directly (existing behavior). This allows callers to be migrated incrementally.

Import `PackContext` from `charter.pack_context`. Do not import from `specify_cli.*` (C-004 direction is `charter → doctrine`, not the reverse — `org_charter.py` is in `specify_cli.doctrine`, which may import from `charter.*`).

Wait — check the import direction. `specify_cli.doctrine.org_charter` importing from `charter.*` is fine per C-004 (the boundary prohibits `specify_cli.*` → `doctrine.*`, not the other way). Confirm this before importing.

Actually, re-read C-004: "specify_cli.* modules must not import from doctrine.* directly". This says `charter.*` may import from `doctrine.*`, and `specify_cli.*` is allowed to import from `charter.*`. So `specify_cli.doctrine.org_charter` can import `PackContext` from `charter.pack_context`.

### T062 — Wire _resolve_chain to use PackContext.pack_roots

In `_resolve_chain()` (from WP09), the function needs to locate packs by name. Currently it receives `pack_set: dict[str, OrgCharterPolicy]`.

When `PackContext` is available, load each pack from its root path in `PackContext.pack_roots` rather than from a pre-loaded dict. Update the internal `pack_set` construction to scan `PackContext.pack_roots` for `org-charter.yaml` files:

```python
def _build_pack_set(pack_context: PackContext) -> dict[str, OrgCharterPolicy]:
    """Build a dict[pack_name, policy] by scanning pack_roots."""
    pack_set: dict[str, OrgCharterPolicy] = {}
    for pack_root in pack_context.pack_roots:
        charter_file = pack_root / "org-charter.yaml"
        if charter_file.exists():
            policy = OrgCharterPolicy.model_validate(yaml.safe_load(charter_file.read_text()))
            pack_set[policy.org_name] = policy
    return pack_set
```

(Adjust field names to match the actual `OrgCharterPolicy` model.)

### T063 — Ensure resolver never reads config.yaml directly

Audit `load_org_charter_policies()` and all functions it calls. Replace any `Path(".kittify/config.yaml").read_text()` or similar with the data already present in `PackContext` (e.g., `pack_context.org_pack_names`).

The only permitted direct config.yaml read is in `PackContext.from_config()` itself (charter module, not doctrine module).

### T064 — Update all callers of load_org_charter_policies()

Find all call sites in the codebase that call `load_org_charter_policies(repo_root)`. Update them to pass a `PackContext` when one is available. For callers that don't yet have a `PackContext`, leave them using the `None` fallback and add a `# TODO: pass PackContext` comment.

Priority callers to update:
- `src/charter/drg.py` (if it calls the loader)
- `src/charter/context.py` (if it calls the loader)
- CLI entry points that trigger charter loading

### T065 — Integration tests

Write `tests/specify_cli/doctrine/test_org_charter_pack_context.py`:

Test cases:
- **Full chain resolution**: Two org packs where B extends A; `load_org_charter_policies` with a `PackContext` containing both pack roots returns the merged policy with unioned directives
- **PackContext pack_roots ordering**: org packs are processed in `pack_roots` order
- **Backward compatibility**: `load_org_charter_policies(repo_root, pack_context=None)` still works for projects without a PackContext
- **No config.yaml read in resolver**: mock or monkeypatch the config.yaml file; resolution works entirely from PackContext without reading config.yaml

## Acceptance Criteria

- [ ] `load_org_charter_policies()` accepts optional `PackContext` parameter
- [ ] `_resolve_chain()` uses `PackContext.pack_roots` to locate pack files
- [ ] No config.yaml reads inside `_resolve_chain()` or `_merge_chain()`
- [ ] All updated callers pass (no breakage in existing tests)
- [ ] Integration tests for full chain resolution via PackContext pass
- [ ] `mypy --strict` clean on modified files

## References

- FR-001: extends: chain resolution
- C-005: PackContext isolation — resolver never reads config.yaml
- WP06: PackContext implementation
- WP09: _resolve_chain() implementation
