---
affected_files: []
cycle_number: 2
mission_slug: charter-doctrine-mission-type-configuration-01KSWJVX
reproduction_command:
reviewed_at: '2026-05-30T19:15:19Z'
reviewer_agent: unknown
verdict: rejected
wp_id: WP01
---

# WP01 Review Cycle 1 — REJECTED

**Reviewer**: reviewer-renata (claude:opus)
**Date**: 2026-05-30
**Verdict**: REJECT — stale documentation paths must be updated before approval.

## Summary

The core code migration is correct and complete:

- Unified `MissionStep` model in `src/doctrine/missions/models.py` (with `IDENTIFIER_PATTERN`, `step_type` Literal discriminant, `__all__`, all required fields).
- Legacy `src/doctrine/mission_step_contracts/` subpackage deleted.
- `src/specify_cli/mission_step_contracts/` correctly preserved.
- `src/doctrine/drg/org_pack_loader.py` correctly untouched (deferred to WP11).
- Built-in step-contract YAMLs relocated cleanly to `src/doctrine/missions/built_in_step_contracts/` via git rename.
- Legacy contract types (MissionStepContract, DelegatesTo, MissionStepContractRepository) relocated to `src/doctrine/missions/step_contracts.py` as compatibility surface.
- All callers migrated.
- Architectural test extended.
- 135 targeted tests pass (`tests/doctrine/missions/` + `tests/architectural/test_layer_rules.py`).

However, **8 source-tree documentation references still point to paths that no longer exist after this WP's migration**. Per the project owner's explicit directive, documentation containing incorrect file paths is a BLOCKING finding, not a nit. These must be fixed before WP01 can be approved.

## Blocking Defects

All 8 references point to `src/doctrine/mission_step_contracts/` — a directory deleted by this WP. The correct current location is `src/doctrine/missions/built_in_step_contracts/`.

### Issue 1 — Stale YAML comment in software-dev mission-runtime (doctrine layer)

**File**: `src/doctrine/missions/software-dev/mission-runtime.yaml`
**Lines**: 4, 26

```
# under src/doctrine/mission_step_contracts/built-in/ via
...
# src/doctrine/mission_step_contracts/built-in/tasks.step-contract.yaml.
```

**Fix**: replace `src/doctrine/mission_step_contracts/built-in/` with `src/doctrine/missions/built_in_step_contracts/` on both lines.

### Issue 2 — Stale YAML comment in documentation mission-runtime (doctrine layer)

**File**: `src/doctrine/missions/documentation/mission-runtime.yaml`
**Line**: 12

```
# src/doctrine/mission_step_contracts/built-in/documentation-*.step-contract.yaml
```

**Fix**: replace `src/doctrine/mission_step_contracts/built-in/` with `src/doctrine/missions/built_in_step_contracts/`.

### Issue 3 — Stale YAML comment in research mission-runtime (doctrine layer)

**File**: `src/doctrine/missions/research/mission-runtime.yaml`
**Line**: 12

```
# src/doctrine/mission_step_contracts/built-in/research-*.step-contract.yaml
```

**Fix**: replace `src/doctrine/mission_step_contracts/built-in/` with `src/doctrine/missions/built_in_step_contracts/`.

### Issue 4 — Stale YAML comment in documentation mission-runtime (specify_cli copy)

**File**: `src/specify_cli/missions/documentation/mission-runtime.yaml`
**Line**: 12

```
# src/doctrine/mission_step_contracts/built-in/documentation-*.step-contract.yaml
```

**Fix**: replace `src/doctrine/mission_step_contracts/built-in/` with `src/doctrine/missions/built_in_step_contracts/`.

### Issue 5 — Stale YAML comment in software-dev mission-runtime (specify_cli copy)

**File**: `src/specify_cli/missions/software-dev/mission-runtime.yaml`
**Line**: 18

```
# src/doctrine/mission_step_contracts/built-in/tasks.step-contract.yaml.
```

**Fix**: replace `src/doctrine/mission_step_contracts/built-in/` with `src/doctrine/missions/built_in_step_contracts/`.

### Issue 6 — Stale YAML comment in research mission-runtime (specify_cli copy)

**File**: `src/specify_cli/missions/research/mission-runtime.yaml`
**Line**: 12

```
# src/doctrine/mission_step_contracts/built-in/research-*.step-contract.yaml
```

**Fix**: replace `src/doctrine/mission_step_contracts/built-in/` with `src/doctrine/missions/built_in_step_contracts/`.

### Issue 7 — Stale prose path reference in research output guidelines

**File**: `src/doctrine/missions/research/actions/output/guidelines.md`
**Line**: 9

```
... enforced by `src/doctrine/mission_step_contracts/shipped/research-output.step-contract.yaml`, ...
```

**Fix**: replace `src/doctrine/mission_step_contracts/shipped/research-output.step-contract.yaml` with `src/doctrine/missions/built_in_step_contracts/research-output.step-contract.yaml`. Note this one also uses the older `shipped/` segment, not `built-in/`; both forms are wrong post-WP01.

## Notes for Implementer

- The references in `kitty-specs/**`, `CHANGELOG.md`, `architecture/**/initiatives/**`, and `docs/development/pr305-review-resolution-plan.md` are historical mission artifacts / changelog entries / archival material. Those are explicitly out of scope — do NOT rewrite history.
- The two references inside `src/doctrine/missions/step_contracts.py` (`line 4` and `line 109`) are intentional:
  - Line 4 describes the historical relocation in the module docstring.
  - Line 109 references `<repo_root>/.kittify/doctrine/mission_step_contracts/`, which is the **project-layer** operator path, intentionally preserved for UX continuity per the docstring.
  Leave both untouched.
- The reference at `src/specify_cli/mission_loader/command.py:214` and the path construction at line 233 are the same project-layer operator path. Leave untouched.

## Other Acceptance Criteria — All Met

| Criterion | Status |
|---|---|
| `doctrine/mission_step_contracts/` deleted | PASS |
| `specify_cli/mission_step_contracts/` preserved | PASS |
| `grep -r "from doctrine.mission_step_contracts" src/` returns no results | PASS (verified) |
| Unified `MissionStep` model present with required fields | PASS |
| `__all__` declared in `doctrine/missions/models.py` | PASS |
| `tests/doctrine/missions/test_models.py` passes | PASS (31 passed) |
| `tests/architectural/test_layer_rules.py` passes | PASS (11 passed) |
| `src/doctrine/drg/org_pack_loader.py` untouched (WP11) | PASS |

## Re-review Checklist

After the implementer fixes the 7 files above, the next reviewer should:

1. Re-run `grep -rn "doctrine/mission_step_contracts/shipped\|doctrine/mission_step_contracts/built" src/ --include="*.md" --include="*.yaml" --include="*.yml"` — must return zero hits except the two intentional `step_contracts.py` references (which are not under `--include="*.yaml"` anyway).
2. Re-run `cd src && pytest tests/doctrine/missions/ tests/architectural/test_layer_rules.py -x -q` — must still pass.
3. Approve.
