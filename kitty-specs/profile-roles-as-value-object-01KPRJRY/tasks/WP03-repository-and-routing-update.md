---
work_package_id: WP03
title: Repository and Routing Update
dependencies:
- WP01
requirement_refs:
- FR-007
- FR-008
- FR-010
planning_base_branch: doctrine/profile_reinforcement
merge_target_branch: doctrine/profile_reinforcement
branch_strategy: Execute in worktree branched from the WP01 lane (WP03 depends on WP01, parallelizes with WP02). Merge back to doctrine/profile_reinforcement when done.
subtasks:
- T016
- T017
- T018
- T019
- T020
history:
- at: '2026-04-21T18:24:37Z'
  event: created
authoritative_surface: src/doctrine/agent_profiles/repository.py
execution_mode: code_change
mission_slug: profile-roles-as-value-object-01KPRJRY
owned_files:
- src/doctrine/agent_profiles/repository.py
- tests/doctrine/test_profile_repository.py
tags: []
---

# WP03 — Repository and Routing Update

## Objective

Update `repository.py` so all role-based filtering, scoring, and lookup use
`profile.roles` (a list). Remove dead `isinstance(p.role, ...)` branches that
relied on the old `StrEnum | str` union. Write new tests for secondary-role
inclusion, primary scoring (1.0), and secondary scoring (0.5).

This WP can run in parallel with WP02 once WP01 is merged.

## Implementation Command

```bash
spec-kitty agent action implement WP03 --agent python-pedro
```

## Branch Strategy

- **Plan base**: `doctrine/profile_reinforcement`
- **Depends on**: WP01 lane — do not start until WP01 is merged
- **Parallelizes with**: WP02 (different files)
- **Merge target**: `doctrine/profile_reinforcement`

---

## Context

### Current `repository.py` (key functions)

```python
def _filter_candidates_by_role(
    candidates: list[AgentProfile], required_role: str
) -> list[AgentProfile]:
    role_str = required_role.lower()
    return [
        p for p in candidates
        if (isinstance(p.role, Role) and p.role.value == role_str)
        or (isinstance(p.role, str) and p.role.lower() == role_str)
        or p.profile_id == required_role
    ]


def _exact_id_signal(
    context: TaskContext, profile: AgentProfile
) -> float:
    req = context.required_role
    if req is None:
        return 0.0
    role_val = profile.role.value if isinstance(profile.role, Role) else str(profile.role).lower()
    return 1.0 if (req == profile.profile_id or req == role_val) else 0.0


def find_by_role(self, role: str | Role) -> list[AgentProfile]:
    role_lower = role.value.lower() if isinstance(role, Role) else role.lower()
    return [
        p for p in self._profiles.values()
        if (isinstance(p.role, Role) and p.role.value == role_lower)
        or (isinstance(p.role, str) and p.role.lower() == role_lower)
    ]
```

### After this WP

- `profile.role` is a `@property` returning `profile.roles[0]` — always a `Role` instance
- `profile.roles` is `list[Role]` — indexable, iterable
- No more `isinstance(p.role, Role)` / `isinstance(p.role, str)` branches

---

## Subtask Guidance

### T016 — Rewrite `_filter_candidates_by_role`

**File**: `src/doctrine/agent_profiles/repository.py`

Replace the existing function:

```python
def _filter_candidates_by_role(
    candidates: list[AgentProfile], required_role: str
) -> list[AgentProfile]:
    return [
        p for p in candidates
        if required_role in p.roles or p.profile_id == required_role
    ]
```

`required_role in p.roles` uses `str.__eq__` (since `Role` is a `str` subclass), so
string comparison with `Role` instances is seamless. Case sensitivity follows whatever
the caller passes; callers should already lower-case `required_role` before calling this
function. Check call sites and document the expectation with a brief inline note if the
old code was doing `.lower()` normalization.

---

### T017 — Rewrite `_exact_id_signal` with primary/secondary scoring

**File**: `src/doctrine/agent_profiles/repository.py`

```python
def _exact_id_signal(
    context: TaskContext, profile: AgentProfile
) -> float:
    req = context.required_role
    if req is None:
        return 0.0
    if req == profile.profile_id or req == profile.roles[0]:
        return 1.0
    if req in profile.roles[1:]:
        return 0.5
    return 0.0
```

**Scoring rules** (from data-model.md):
| Condition | Score |
|-----------|-------|
| `req` matches `profile.profile_id` | 1.0 |
| `req` matches `profile.roles[0]` (primary) | 1.0 |
| `req` is in `profile.roles[1:]` (secondary) | 0.5 |
| no match | 0.0 |

The `required_role` on `TaskContext` is now `Role | None` (after WP01 T008); `req == profile.roles[0]`
uses `str.__eq__` and handles both `Role` and plain `str` correctly.

---

### T018 — Rewrite `find_by_role`

**File**: `src/doctrine/agent_profiles/repository.py`

```python
def find_by_role(self, role: str | Role) -> list[AgentProfile]:
    return [
        p for p in self._profiles.values()
        if role in p.roles
    ]
```

`role in p.roles` iterates the list and uses `str.__eq__` for each comparison.

---

### T019 — Remove dead `isinstance` branches

**File**: `src/doctrine/agent_profiles/repository.py`

After T016–T018, search for any remaining `isinstance(p.role, Role)` or
`isinstance(p.role, str)` patterns:

```bash
rg "isinstance.*\.role" src/doctrine/agent_profiles/repository.py
```

Delete any dead branches. If there are guard checks like:
```python
if isinstance(p.role, Role):
    role_val = p.role.value
else:
    role_val = str(p.role)
```
these can be replaced with simply `role_val = p.role` (the property always returns a `Role`
instance, which is already a `str`).

Also remove the `from enum import StrEnum` import if `StrEnum` is no longer referenced
in `repository.py`.

---

### T020 — Write new routing tests

**File**: `tests/doctrine/test_profile_repository.py`

Add a new test class (do not remove existing tests):

```python
class TestMultiRoleRouting:
    """Tests for profiles that carry multiple roles."""

    def _make_profile(self, profile_id: str, roles: list[str]) -> AgentProfile:
        return AgentProfile(**{
            "profile-id": profile_id,
            "name": f"Test {profile_id}",
            "version": "1.0",
            "roles": roles,
        })

    def test_secondary_role_included_in_filter(self):
        """A profile with secondary role still passes the role filter."""
        p = self._make_profile("arch-alex", ["architect", "researcher"])
        result = _filter_candidates_by_role([p], "researcher")
        assert p in result

    def test_primary_role_included_in_filter(self):
        p = self._make_profile("arch-alex", ["architect", "researcher"])
        result = _filter_candidates_by_role([p], "architect")
        assert p in result

    def test_unrelated_role_excluded_from_filter(self):
        p = self._make_profile("arch-alex", ["architect", "researcher"])
        result = _filter_candidates_by_role([p], "implementer")
        assert p not in result

    def test_primary_role_signal_is_1_0(self):
        p = self._make_profile("arch-alex", ["architect", "researcher"])
        ctx = TaskContext(required_role=Role("architect"))
        assert _exact_id_signal(ctx, p) == 1.0

    def test_secondary_role_signal_is_0_5(self):
        p = self._make_profile("arch-alex", ["architect", "researcher"])
        ctx = TaskContext(required_role=Role("researcher"))
        assert _exact_id_signal(ctx, p) == 0.5

    def test_no_match_signal_is_0_0(self):
        p = self._make_profile("arch-alex", ["architect", "researcher"])
        ctx = TaskContext(required_role=Role("implementer"))
        assert _exact_id_signal(ctx, p) == 0.0

    def test_profile_id_match_signal_is_1_0(self):
        p = self._make_profile("arch-alex", ["architect"])
        ctx = TaskContext(required_role=Role("arch-alex"))
        assert _exact_id_signal(ctx, p) == 1.0

    def test_find_by_role_returns_secondary_role_profiles(self):
        """find_by_role checks all roles, not just the primary."""
        from doctrine.agent_profiles.repository import AgentProfileRepository
        repo = AgentProfileRepository.__new__(AgentProfileRepository)
        primary  = self._make_profile("arch-alex", ["architect"])
        secondary = self._make_profile("arch-bob",  ["implementer", "architect"])
        repo._profiles = {"arch-alex": primary, "arch-bob": secondary}

        result = repo.find_by_role("architect")
        assert primary  in result
        assert secondary in result
```

Adjust imports and `TaskContext` construction to match actual module paths. Run
`pytest tests/doctrine/test_profile_repository.py -v` to confirm all pass.

---

## Definition of Done

- [ ] `_filter_candidates_by_role` checks `required_role in profile.roles` (any position)
- [ ] `_exact_id_signal` returns 1.0 for primary match, 0.5 for secondary, 0.0 for none
- [ ] `find_by_role` checks `role in profile.roles`
- [ ] No `isinstance(p.role, Role)` or `isinstance(p.role, str)` branches remain
- [ ] `pytest tests/doctrine/test_profile_repository.py -v` passes (old + new tests)

## Risks

- **Case sensitivity**: Old code called `.lower()` on role strings before comparison. The
  new `Role("implementer")` is already lowercase (by convention). Verify call sites pass
  normalized values; add a `req = str(req).lower()` normalization inside the functions if
  the broader codebase passes un-normalized strings.
- **`profile_id` matching**: `p.profile_id == required_role` is a string equality check.
  Profile IDs are like `"implementer-ivan"`. If callers pass `Role("implementer-ivan")`,
  this works via `str.__eq__`. Confirm with a test.
