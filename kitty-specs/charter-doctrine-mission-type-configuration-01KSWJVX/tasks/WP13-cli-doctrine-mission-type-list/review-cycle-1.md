# WP13 Review — Cycle 1 (Reviewer: reviewer-renata)

**Verdict:** REJECTED — blocking defect: defensive `try/except ImportError` fallback for `MissionTypeRepository` in production code.

**Date:** 2026-05-30
**Reviewer:** reviewer-renata (Claude / opus)
**Lane:** lane-m
**Branch:** `kitty/mission-charter-doctrine-mission-type-configuration-01KSWJVX-lane-m`
**HEAD commit:** `27ae8cbf2 feat(WP13): add spec-kitty doctrine mission-type list command`

---

## Summary of findings

The functional surface of WP13 actually works when exercised against the lane's source:

- `spec-kitty doctrine mission-type list` returns the 4 expected built-in types (`documentation`, `plan`, `research`, `software-dev`) with `source_layer: built-in`.
- `--json` returns a valid JSON array with the required `id`, `source_layer`, `display_name` keys.
- Pytest: `tests/cli/test_doctrine_commands.py` — 10/10 pass.
- `spec-kitty doctrine --help` regression guard for PR #1352: the `doctrine` group is still registered (the `mission-type` sub-app is added at module import time alongside the existing `pack` / `org` sub-apps).
- mypy --strict on `src/specify_cli/cli/commands/doctrine.py`: no errors attributable to this WP's changes (the 7 errors reported are all pre-existing `[import-untyped]` issues for `jsonschema` stubs and for the WP03 module which doesn't exist in this lane — both are environmental, not introduced by WP13).

However, **the implementation violates the explicit human-mandated rule** in the review prompt:

> "If production code has `try: from doctrine.missions.mission_type_repository import MissionTypeRepository except ImportError: <fallback>` — this is a **blocking defect**. Production code must import directly without fallback; the lane merge will resolve the dependency."

The implementer's commit message and the in-code comment acknowledge this is intentional WP03-unavailable workaround logic that has been placed in production code rather than confined to tests.

## Blocking issues (must fix before re-review)

### B1 — Defensive `try/except ImportError` fallback for `MissionTypeRepository` in production code

**File:** `src/specify_cli/cli/commands/doctrine.py`
**Lines:** 791–806 (primary defect) and 810–815 (secondary fallback to `MissionTemplateRepository`)
**Severity:** BLOCKING (per human-mandated rule in the review prompt)

The function `_collect_built_in_mission_types()` is structured as:

```python
def _collect_built_in_mission_types() -> list[_MissionTypeRow]:
    rows: list[_MissionTypeRow] = []

    # Attempt WP03 MissionTypeRepository (available post-merge of lane-c).
    try:
        from doctrine.missions.mission_type_repository import MissionTypeRepository  # noqa: PLC0415

        repo = MissionTypeRepository.default()
        for mt in repo.load_all():
            rows.append(
                _MissionTypeRow(
                    id=mt.id,
                    source_layer="built-in",
                    display_name=mt.display_name,
                )
            )
        return rows
    except (ImportError, ModuleNotFoundError, AttributeError):
        pass  # WP03 not yet available — use fallback

    # Fallback: scan doctrine/missions/ for directories with governance-profile.yaml.
    try:
        from doctrine.missions.repository import MissionTemplateRepository  # noqa: PLC0415

        missions_root = MissionTemplateRepository.default_missions_root()
    except (ImportError, ModuleNotFoundError, AttributeError):
        return rows

    # … directory scan, derive display name from a private override dict …
```

This is exactly the pattern the review prompt called out as a blocking defect. The contract is:

- Production code imports `MissionTypeRepository` directly at the top of the module (or inside the function, but **without** `try/except`).
- The lane merge order (WP03 merging before WP13) is what resolves the runtime dependency.
- Defensive scaffolding to make WP13 runnable in isolation belongs in tests (e.g., monkeypatching the import) — not in shipped code paths.

**Why this matters beyond the mandated rule:**

1. **Silent shadowing.** `except (ImportError, ModuleNotFoundError, AttributeError)` is overly broad. An `AttributeError` raised *inside* `MissionTypeRepository.default()` or `repo.load_all()` (e.g., a future refactor that renames `.id` or `.display_name`) would silently fall through to a directory-scan fallback with manually-overridden display names, instead of failing loudly. This is a future regression vector.
2. **Display-name drift.** The fallback path resolves `display_name` from a private `_DISPLAY_NAME_OVERRIDES` dict on lines 837–842 of the same file. Once WP03 lands, the canonical `MissionType.display_name` from `governance-profile.yaml` becomes the source of truth, but the fallback's hard-coded values can drift from the YAML. There is no test that fails if they diverge.
3. **Dead code on merge.** After WP03 merges, the fallback branch and the entire `_DISPLAY_NAME_OVERRIDES` map become unreachable code that future maintainers will not know to delete.

### Required remediation

1. Replace the contents of `_collect_built_in_mission_types()` with a direct, top-level-import implementation:
   ```python
   from doctrine.missions.mission_type_repository import MissionTypeRepository

   def _collect_built_in_mission_types() -> list[_MissionTypeRow]:
       repo = MissionTypeRepository.default()
       return [
           _MissionTypeRow(
               id=mt.id,
               source_layer="built-in",
               display_name=mt.display_name,
           )
           for mt in repo.load_all()
       ]
   ```
2. Delete the `try/except` block (lines 791–806), the secondary fallback (lines 808–831), the `_DISPLAY_NAME_OVERRIDES` dict (lines 836–842), and the `_derive_display_name()` helper (lines 845–853). They are all coverage for the absent-WP03 case and become dead code once the lane merges.
3. If WP13 must pass tests *in this lane in isolation* (i.e., before lane-c merges), the only acceptable workaround is in test code: e.g., a conftest fixture that monkeypatches the import or vendors a minimal stub `MissionTypeRepository`. Document that pattern in the test file rather than in production.
4. Update the module docstring on line 23 to remove the `[--json]` note about the fallback path being a transitional state.

### Suggested workflow

- Coordinate with the lane-c implementer so WP03 is rebased into a state where its `MissionTypeRepository` can be cherry-picked or otherwise made available to lane-m during the rebase before re-review.
- Alternatively, if WP03 is genuinely blocked, mark WP13 as `blocked` on the WP03 dependency (already declared in the WP13 metadata `dependencies: [WP03, WP04]`) rather than ship a workaround.

## Non-blocking observations (FYI — not required to fix)

- N1 (style) — Line 766: `class _MissionTypeRow:` is "Dataclass-free" per its own comment. Once the fallback is removed, this can be replaced with a `dataclasses.dataclass(frozen=True, slots=True)` for less ceremony. Optional.
- N2 (test coverage) — `tests/cli/test_doctrine_commands.py` does not currently assert that **all four** canonical mission types (`documentation`, `plan`, `research`, `software-dev`) appear. After the fix lands, please add a test that pins this set (FR-013 acceptance).
- N3 (docstring) — Lines 780–787 describe the "Prefers MissionTypeRepository … Falls back to …" behavior. After the fix this docstring should be tightened to describe only the canonical path.

## Evidence captured

- Diff stat: `7 files changed, 353 insertions(+), 407 deletions(-)` (most of the deletions are obsolete task spec files for completed WPs in this lane's recent history; the WP13 surface area is just `src/specify_cli/cli/commands/doctrine.py` + `tests/cli/test_doctrine_commands.py`).
- Lane execution shows the fallback path is the one currently active (because `doctrine.missions.mission_type_repository` truly doesn't exist in lane-m yet — confirmed via `python -c "from doctrine.missions.mission_type_repository import MissionTypeRepository"` → `ModuleNotFoundError`). This means the WP is currently "passing" through scaffolding, not through the contract it is supposed to implement.

## What's good

- Command surface, flag shape, JSON schema, and table layout match the WP13 spec.
- Tests are clean and run fast.
- `doctrine --help` regression guard for PR #1352 is intact — the `mission-type` sub-app is registered at import time.
- No `--feature` flag introduced; terminology canon respected.
- mypy --strict reports no WP13-introduced errors.

## Action requested

Move WP13 back to `planned`, fix B1 by removing the production-side fallback and importing `MissionTypeRepository` directly, then re-request review. Notify the WP14 owner (declared dependency on WP13) that the rebase will move.
