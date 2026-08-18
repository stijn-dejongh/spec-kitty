# Contract: source_module non-goal invariants (G1–G6)

These guards live in `tests/unit/test_symbol_key.py` and MUST be present and green.
They pin the #3552 non-goals so a future edit cannot silently violate them.

## G6 — keystone: field is non-comparing

```python
import dataclasses
f = {f.name: f for f in dataclasses.fields(SymbolKey)}["source_module"]
assert f.compare is False
```
Fails the instant someone makes the field comparing (closes critical risk R1).

## G1 — equality ignores source_module

Two `SymbolKey`s equal in `(bare_name, body_hash[, module_path])` but differing in
`source_module` (incl. `None` vs set) compare **equal**.

## G2 — hash / frozenset membership ignores source_module

The same two keys hash-equal and are mutual members of a `frozenset`; a resolver-minted
key with `source_module=None` is `in` an allowlist frozenset whose entry carries a
non-None `source_module` (models `final_key in allowlist`).

## G3 — no tier escalation

A content-tier key (`module_path=None`) with `source_module` set is still
`is_content_tier`, and `key_tier(...)` returns it **unescalated** (no `module_path`
minted from provenance). Preserves D-1 relocation-tolerance (non-goal: no content→collision).

## G4 — as_tuple() excludes source_module

`SymbolKey("Foo", "h", source_module="pkg.mod").as_tuple() == ("Foo", "h")`;
collision-tier → `("Foo", "m", "h")`. Provenance never enters the identity tuple.

## G5 — body_hash unaffected; resolver key has no provenance

`body_hash` is identical with or without `source_module`; a resolver-minted key for a
still-dead symbol has `source_module is None`. Adding a provenance peer does not change
any other key's `body_hash`.

## Acceptance anchor (FR-005 / SC-002)

Reproduce the #3560 Finding-1 scenario: two dead symbols sharing `bare_name` + `body_hash`
with distinct `source_module`. A content-tier entry for one resolves via `source_module`
and does **not** emit `NEEDS_MODULE_PATH`, while the other still-dead symbol is never admitted.
