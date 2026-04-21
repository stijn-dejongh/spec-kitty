---
work_package_id: WP05
title: Test Suite Alignment
dependencies:
- WP01
- WP02
- WP03
- WP04
agent_profile: "python-pedro"
role: "implementer"
agent: "claude"
model: "claude-sonnet-4-6"
requirement_refs:
- NFR-003
planning_base_branch: doctrine/profile_reinforcement
merge_target_branch: doctrine/profile_reinforcement
branch_strategy: Planning artifacts for this feature were generated on doctrine/profile_reinforcement. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into doctrine/profile_reinforcement unless the human explicitly redirects the landing branch.
subtasks:
- T029
- T030
- T031
- T032
- T033
history:
- at: '2026-04-21T18:24:37Z'
  event: created
authoritative_surface: tests/
execution_mode: code_change
mission_slug: profile-roles-as-value-object-01KPRJRY
owned_files:
- tests/doctrine/test_service.py
- tests/charter/test_catalog.py
- tests/specify_cli/status/test_wp_metadata.py
tags: []
---

# WP05 — Test Suite Alignment

## ⚡ Do This First: Load Agent Profile

Use the `/ad-hoc-profile-load` skill to load the agent profile specified in the frontmatter, and behave according to its guidance before parsing the rest of this prompt.

- **Profile**: `python-pedro`
- **Role**: `implementer`
- **Agent/tool**: `claude`

If no profile is specified, run `spec-kitty agent profile list` and select the best match for this work package's `task_type` and `authoritative_surface`.

---

## Objective

Fix all test files outside `test_shipped_profiles.py` that reference old profile IDs,
old `Role(StrEnum)` imports, or old scalar `role:` fixture keys. Verify the full test
suite passes with zero failures and zero mypy errors in `src/doctrine/agent_profiles/`.

This is the final integration gate — all other WPs must be merged before starting WP05.

## Implementation Command

```bash
spec-kitty agent action implement WP05 --agent python-pedro
```

## Branch Strategy

- **Plan base**: `doctrine/profile_reinforcement`
- **Depends on**: WP01 + WP02 + WP03 + WP04 (all merged first)
- **Parallelizes with**: nothing
- **Merge target**: `doctrine/profile_reinforcement`

---

## Context

Three test files were updated in an earlier session (profile rename propagation) but
may still contain patterns that break after the `Role(StrEnum)` → `Role(str)` change.
The key breakage patterns to fix:

1. **`.role.value` pattern**: `StrEnum` exposes `.value`; the new `str` subclass does not.
   `profile.role` is now a `str` directly — use it as a string.
2. **`from enum import Role` / `from ...profile import Role` with StrEnum assumption**:
   Imports are likely fine but check for usage of `.value`, `list(Role)`, or iteration
   over `Role` as an enum.
3. **Fixture dicts with `"role": ...` scalar**: These will trigger `DeprecationWarning`
   on model construction. Either update to `"roles": [...]` or leave intentionally and
   add a `warnings.catch_warnings` block with a comment explaining the deprecation path
   is being intentionally exercised.

---

## Subtask Guidance

### T029 — Fix `tests/doctrine/test_service.py`

**File**: `tests/doctrine/test_service.py`

Audit all fixture dicts and assertions:

1. Find all occurrences of `"role":` in fixture dicts:
   ```bash
   rg '"role":' tests/doctrine/test_service.py
   ```
   Update to `"roles": [<value>]` unless the test is explicitly testing the deprecation
   coercion path (in which case, add a comment and a `warnings.catch_warnings` block).

2. Find `.role.value` patterns:
   ```bash
   rg '\.role\.value' tests/doctrine/test_service.py
   ```
   Replace `profile.role.value` with `profile.role` (which is already a `str`).

3. Find `isinstance(x, Role)` — these remain valid since `Role` is still a class;
   no change needed unless the test was checking `StrEnum`-specific behavior.

4. Verify `AgentProfile` constructor calls use `roles=` or `"roles":` keys.

Run `pytest tests/doctrine/test_service.py -v` and fix any remaining failures.

---

### T030 — Fix `tests/charter/test_catalog.py`

**File**: `tests/charter/test_catalog.py`

Apply the same audit as T029:

1. `rg '"role":' tests/charter/test_catalog.py` — update to `"roles": [...]`
2. `rg '\.role\.value' tests/charter/test_catalog.py` — remove `.value`
3. Verify profile IDs in fixture dicts match the new character IDs if relevant
   (e.g., if the test references `"python-pedro"` as a profile ID — that's already correct
   from the earlier rename propagation session).

Run `pytest tests/charter/test_catalog.py -v`.

---

### T031 — Fix `tests/specify_cli/status/test_wp_metadata.py`

**File**: `tests/specify_cli/status/test_wp_metadata.py`

1. `rg '"role":' tests/specify_cli/status/test_wp_metadata.py` — update to `"roles": [...]`
2. `rg '\.role\.value' tests/specify_cli/status/test_wp_metadata.py` — remove `.value`
3. Profile IDs in `agent_profile=` kwargs should already be `"python-pedro"` (updated in
   the earlier session). Verify no stale `"python-implementer"` references remain.

Run `pytest tests/specify_cli/status/test_wp_metadata.py -v`.

---

### T032 — Run full test suite; fix any remaining failures

```bash
pytest tests/doctrine/ tests/charter/ tests/specify_cli/ -x --tb=short 2>&1 | head -80
```

Triage and fix any failures not already addressed in T029–T031. Common patterns:

- `AttributeError: 'Role' object has no attribute 'value'` → remove `.value`
- `DeprecationWarning treated as error` → update fixture to use `roles:` list, or
  suppress the warning intentionally with `warnings.filterwarnings("ignore", category=DeprecationWarning)`
  in the test if the deprecation path is being exercised
- `ValidationError: roles field required` → fixture dict is missing `roles` key entirely

Run the full suite until `pytest ... -x` exits green (no failures).

---

### T033 — Run `mypy`; fix any type annotation issues

```bash
mypy src/doctrine/agent_profiles/ --ignore-missing-imports 2>&1 | head -60
```

Common issues to expect:

- `Role` used where `str` is expected: should be fine since `Role` is a `str` subclass
- `@property role` return type vs field type mismatch: annotate the property explicitly
  as `-> Role`
- `list[Role]` vs `list[str]` narrowing: Pydantic models may report type warnings on
  the `roles` field if the annotation is not fully resolved; ignore with `# type: ignore`
  only if the runtime behavior is correct and the warning is a Pydantic/mypy integration
  limitation
- `ClassVar` usage for constants in `Role`: mypy may complain about assigning after class
  body; suppress with `# type: ignore[assignment]` on the post-body constant assignments

Fix real type errors; suppress false positives with targeted `# type: ignore[...]`.
Goal: `mypy` exits 0 on `src/doctrine/agent_profiles/`.

---

## Definition of Done

- [ ] `tests/doctrine/test_service.py`: no `"role":` scalar fixtures (or intentional with comment); no `.role.value`
- [ ] `tests/charter/test_catalog.py`: same audit applied
- [ ] `tests/specify_cli/status/test_wp_metadata.py`: same audit applied
- [ ] `pytest tests/doctrine/ tests/charter/ tests/specify_cli/ -x` passes with zero failures
- [ ] `mypy src/doctrine/agent_profiles/` exits 0 (or only known false-positive suppressions)

## Risks

- **`DeprecationWarning` as error**: If the pytest config (`pyproject.toml` / `pytest.ini`)
  has `filterwarnings = error::DeprecationWarning`, fixture dicts using the old `"role":`
  scalar will cause test failures even for tests not specifically testing that path.
  Check `pyproject.toml` for this setting and update fixtures proactively.
- **Implicit `role` usage in other test files**: The three files listed are the known
  consumers. Run a broad search after T031:
  ```bash
  rg '"role":' tests/ --include="*.py"
  rg '\.role\.value' tests/ --include="*.py"
  ```
  Fix any additional occurrences found.
