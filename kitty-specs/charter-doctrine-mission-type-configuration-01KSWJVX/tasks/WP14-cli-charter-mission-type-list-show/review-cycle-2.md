---
affected_files: []
cycle_number: 2
mission_slug: charter-doctrine-mission-type-configuration-01KSWJVX
reproduction_command:
reviewed_at: '2026-05-30T20:52:32Z'
reviewer_agent: unknown
verdict: rejected
wp_id: WP14
review_artifact_override_at: "2026-05-30T21:10:38Z"
review_artifact_override_actor: "operator"
review_artifact_override_wp_id: "WP14"
review_artifact_override_reason: "Review passed (reviewer-renata, cycle 2): Both blocking issues resolved — docs/reference/cli-commands.md now contains all three missing entries (charter mission-type, doctrine mission-type, mission-type show); module-level doctrine.* import in doctrine.py moved to lazy inside _collect_built_in_mission_types(). All 3 architectural tests pass, all 25 CLI tests pass, 91 total related tests pass. FR-016 and FR-017 fully covered. No dead code, no --feature regressions, no frozen file violations, mypy clean on WP14 files, C-004 charter boundary respected."
---

# Review Cycle 1 — WP14 CLI: charter mission-type list / mission-type show

**Reviewer:** reviewer-renata  
**Date:** 2026-05-30  
**Result:** CHANGES REQUESTED — 2 blocking issues

---

## Summary

The core implementation is solid: all 25 tests in `tests/cli/test_charter_mission_type_commands.py` pass, the `charter.existing_mission_types()` and `charter.resolve_action_sequence()` APIs are correctly used, and `mypy --strict` is clean on the new files. The layer boundary concern from the acceptance criteria (C-004) is correctly addressed in WP14's own code — lazy function-level imports are used for `doctrine.*` in WP14's files and are not counted by the ratchet test.

Two architectural tests fail, blocking approval.

---

## Issue 1 (BLOCKING): CLI reference docs not updated

**Test:** `tests/architectural/test_docs_cli_reference_parity.py::test_visible_paths_match_reference`

**Failure:**
```
Visible command paths missing from the reference docs:
  - spec-kitty charter mission-type
  - spec-kitty charter mission-type list
  - spec-kitty mission-type show
```

WP14 adds three new visible CLI commands but does not update `docs/reference/cli-commands.md`. The parity ratchet test detects this and fails.

**Fix:** Update `docs/reference/cli-commands.md` to include the three new command paths. The format follows the existing pattern in that file (markdown `##` headers and usage blocks). You can use `scripts/docs/build_cli_reference.py` (if available) to regenerate the reference, or add the entries manually matching the style of nearby sections such as `## spec-kitty charter bundle`.

The entries needed are:
- `## spec-kitty charter mission-type` — the sub-group help
- `## spec-kitty charter mission-type list` — the list command
- `## spec-kitty mission-type show` — the show command

Note: `spec-kitty mission-type list` may also need an entry if it is not already covered by the pre-existing `spec-kitty mission-type` section.

---

## Issue 2 (BLOCKING, inherited from WP13): Architectural boundary ratchet failure

**Test:** `tests/architectural/test_runtime_charter_doctrine_boundary.py::test_runtime_has_no_new_direct_doctrine_imports`

**Failure:**
```
Runtime → Charter → Doctrine boundary violation. The following
files under src/specify_cli/ introduce a direct
`from doctrine.*` / `import doctrine` import outside the
allowlist and outside the src/specify_cli/doctrine/ pack-management
subpackage:
  - src/specify_cli/cli/commands/doctrine.py
```

The violation is in `src/specify_cli/cli/commands/doctrine.py` at line 44:
```python
from doctrine.missions.mission_type_repository import MissionTypeRepository
```
This was introduced by WP13's commits (`feat(WP13)` and `fix(WP13)`), which were merged into this lane. WP14 does NOT own this file or modify it, but the architectural ratchet test runs on the full branch state and will fail until this is fixed.

**Fix:** This requires coordination with the WP13 implementer. The `from doctrine.missions.mission_type_repository import MissionTypeRepository` import in `doctrine.py` must be moved inside the `mission_type_list()` function as a lazy import (matching the pattern already used in WP14's own `charter/mission_type.py` and `mission_type.py` files):

```python
# In doctrine.py, change the top-level import:
# FROM:
from doctrine.missions.mission_type_repository import MissionTypeRepository

# TO: (lazy import inside the function body)
def mission_type_list(...) -> None:
    from doctrine.missions.mission_type_repository import MissionTypeRepository  # noqa: PLC0415
    ...
```

And remove the `_collect_built_in_mission_types()` helper (which relies on the module-level import) or move the import inside it as well.

Once the WP13 violation is resolved (either in a WP13 fix commit, or by the WP14 implementer applying the fix in this lane as a tidy-up), this ratchet test will pass.

**Note to implementer:** The WP14 docs fix (Issue 1) is entirely within WP14's scope. The doctrine.py fix (Issue 2) may require touching `doctrine.py` which is WP13's owned file — coordinate with the WP13 owner or apply the minimal fix here since it is already merged into lane-n.

---

## Passing items

- All 25 unit tests in `tests/cli/test_charter_mission_type_commands.py`: PASS
- `mypy --strict` on new files (`charter/mission_type.py`, `mission_type.py` additions): PASS
- Layer boundary (C-004) in WP14-owned files: PASS (lazy function-level imports)
- `charter.existing_mission_types()` and `charter.resolve_action_sequence()` used correctly: PASS
- `UnknownMissionTypeError` raised with registered IDs for unknown type: PASS
- `--json` output is valid JSON with required keys: PASS
- Alias (`mission-type list`) delegates to `charter_mission_type_list()`: PASS
- No `--feature` flags introduced (charter terminology canon): PASS
- `__all__` declared in new modules (C-007): PASS
