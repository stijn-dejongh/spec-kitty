# Research: Profile Roles as Value Object

**Mission**: profile-roles-as-value-object-01KPRJRY
**Status**: Complete — all decisions resolved during planning interrogation

---

## Decision 1 — `Role` value object pattern

**Decision**: Option A — `str` subclass with class-level constants.

**Rationale**:
- `Role("my-custom")` produces a `Role` instance, not a bare `str`; type annotations
  (`list[Role]`) are truthful everywhere
- Pydantic serialises a `str` subclass as a plain string; no custom serialiser needed
- `role == "implementer"` continues to work via `str.__eq__`
- Future extension paths are open without code changes:
  - Add a `description: str = ""` field to `Role.__init__` to document what a role means
  - Load well-known roles from a shipped YAML registry at import time
  - Expose `Role.known_roles()` as a class method returning the pre-defined set

**Alternatives considered**:
- *Keep `StrEnum` + `Role | str` union at field level* — already the current approach;
  inconsistent: `type(custom_role) is str` while `type(Role.IMPLEMENTER) is Role`
- *Metaclass registry with `__getattr__`* — most ergonomic but complex to type-check;
  deferred to a potential future YAML-loading extension

---

## Decision 2 — Backward compatibility for `role:` scalar

**Decision**: Option B — transparent coercion with `DeprecationWarning`.

- Scalar `role: implementer` → promoted to `roles: [Role("implementer")]` on load
- `DeprecationWarning` names the `profile-id` and gives the exact replacement syntax
- Coercion lives in a Pydantic `model_validator(mode="before")` on `AgentProfile`
- Shipped profiles are fully migrated; coercion is a permanent compatibility shim for
  user-authored profiles

---

## Decision 3 — Routing behaviour for secondary roles

**Decision**: primary role (index 0) scores 1.0 in `_exact_id_signal`; any secondary role
(index 1+) scores 0.5.

**Rationale**: A profile that lists `[architect, researcher]` should rank first for an
architect slot but still appear as a candidate for a researcher slot at reduced priority.
The 0.5 weight keeps secondary-role candidates visible in ranked lists without displacing
true-primary matches.

---

## Decision 4 — Computed `role` property

**Decision**: Retain `AgentProfile.role` as a `@property` returning `roles[0]`.

Callers throughout the codebase (`wp_metadata.py`, `scanner.py`) read `.role` as a string.
Keeping a computed property avoids a wide mechanical refactor outside this mission's scope.
The property emits no warning — it is a supported read accessor, not a deprecated field.

---

## Decision 5 — Character names for shipped profiles

All shipped profiles already carry character names in their `name` field. Only two require
a `name` update (the `profile-id` rename is the primary change for the others):

| profile-id → new ID | name update |
|---------------------|-------------|
| `planner` → `planner-priti` | "Planner Petra" → "Planner Priti" |
| `researcher` → `researcher-robbie` | "Researcher Rosa" → "Researcher Robbie" |

`generic-agent` and `human-in-charge` are structural profiles exempt from FR-012.
`implementer` base profile is also exempt (specialised by `implementer-ivan`).

---

## Decision 6 — `avatar_image` field

**Decision**: Add `avatar_image: str | None = None` with YAML alias `avatar-image`.
No path validation at load time (deferred to issue #647). Field is optional;
absent YAML key → `None` with no warning.
