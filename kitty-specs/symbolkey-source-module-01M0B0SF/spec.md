# Mission Specification: SymbolKey source_module provenance field

**Mission Branch**: `remediation/symbolkey-source-module-3552`
**Created**: 2026-08-18
**Status**: Draft
**Input**: Root-cause follow-up to #2853 (frozen-baseline toll reduction); closes #3552; parented under EPIC #1931. Scope locked by a four-lens research squad (design / invariants / code-state / related-work).

## User Scenarios & Testing *(mandatory)*

The actor throughout is a **repo developer/maintainer** working in the architectural
test suite. "The gate" means the dead-symbol architectural gate
(`tests/architectural/test_no_dead_symbols.py`) and its #2853 refresh helper
(`tests/architectural/_refresh_dead_symbol_hashes.py`).

### User Story 1 - Refresh a still-dead allowlisted symbol without touching a comment (Priority: P1)

A developer edits the body of a still-dead allowlisted symbol. The refresh helper
must recover which module that symbol came from to refresh its `body_hash` safely.
Today it can only do so by parsing a free-form provenance comment, failing closed
when the comment is missing or ambiguous — so a load-bearing safety property depends
on comment hygiene.

**Why this priority**: This is the root cause #3552 exists to remove. Machine-readable
provenance is what lets the helper work without comment-parsing.

**Independent Test**: With `source_module` populated, the helper resolves provenance
from the field alone; deleting/garbling the provenance comment does not change the
refresh decision.

**Acceptance Scenarios**:

1. **Given** an allowlist entry carrying `source_module=`, **When** the refresh helper decides its fate, **Then** it uses `source_module` (not the comment) to recover the module, and the decision is unchanged if the comment text is altered or removed.
2. **Given** the machine comment-parsing path has been retired, **When** the gate and helper run, **Then** no code reads the provenance comment for machine decisions.

---

### User Story 2 - Disambiguate a same-name/same-body collision cleanly (Priority: P1)

Two dead symbols share a `bare_name` and `body_hash`. Today the helper fail-closes to
a `NEEDS_MODULE_PATH` escalation (the #3560 Finding-1 case), because content-tier keys
carry no machine identity to tell the two apart without forcing a collision-tier key.

**Why this priority**: This is the concrete acceptance anchor carried over from the
already-closed #3560; it proves `source_module` actually disambiguates.

**Independent Test**: Reproduce the #3560 Finding-1 scenario; with `source_module`
present it resolves cleanly instead of escalating.

**Acceptance Scenarios**:

1. **Given** two dead symbols with the same `bare_name` and `body_hash` and distinct `source_module`, **When** the helper decides a content-tier entry for one of them, **Then** it disambiguates via `source_module` and does **not** emit `NEEDS_MODULE_PATH`, while still never admitting the other (still-dead) symbol.

---

### User Story 3 - One canonical provenance source (Priority: P2)

Provenance is split today: structured `module_path=` for the 25 collision-tier entries,
free-form comment for the 338 content-tier entries — the same fact (origin module) split
along a tier boundary. The developer should have a single canonical machine source.

**Why this priority**: SSOT hygiene; closes the whack-a-field trap of leaving two
provenance representations alive.

**Independent Test**: Every content-tier allowlist entry carries `source_module`; the
comment-parsing surfaces no longer exist in the codebase.

**Acceptance Scenarios**:

1. **Given** the mission is complete, **When** the content-tier entries are inspected, **Then** all 338 carry `source_module=`, and the `# module::Name` comment remains as human audit only.

### Edge Cases

- What happens when `source_module` differs between two entries that are otherwise identical (`bare_name`, `body_hash`, `module_path`)? They must not silently collapse in a frozenset — an authoring-time no-collision guard should catch it.
- What happens if a future edit makes the field *comparing*? Every provenance-bearing entry would stop matching its resolver-minted key and the whole allowlist would false-red — a keystone guard must fail the instant `compare` is flipped.
- What happens if the backfill runs but the parse-path deletion does not (or vice-versa)? A half-retired state; the two must move atomically.

## Requirements *(mandatory)*

### Functional Requirements

| ID | Title | User Story | Priority | Status |
|----|-------|------------|----------|--------|
| FR-001 | Non-hashing `source_module` field on `SymbolKey` | As a maintainer, I want `SymbolKey` to carry an optional `source_module` that is excluded from equality, hash, `body_hash`, `key_tier`, and `as_tuple()`, so provenance is machine-readable without affecting identity. | High | Open |
| FR-002 | Helper consumes `source_module` | As a maintainer, I want the refresh helper to recover a symbol's module from `source_module` (preferred over the comment), so refresh no longer depends on comment hygiene. | High | Open |
| FR-003 | Backfill all content-tier entries | As a maintainer, I want all 338 content-tier allowlist entries to carry `source_module`, applied by a scripted AST rewrite (not hand-edited), so provenance is complete and uniform. | High | Open |
| FR-004 | Retire the machine comment-parsing path | As a maintainer, I want the machine comment-parsing surfaces removed (regex, comment readers, the parseable-comment test, `_recover_provenance`), keeping the comment text as human audit, so there is one canonical provenance source. | High | Open |
| FR-005 | Collision disambiguation | As a maintainer, I want a same-name/same-body collision to resolve via `source_module` instead of fail-closing to `NEEDS_MODULE_PATH`, so the #3560 Finding-1 case is fixed at the root. | High | Open |

### Non-Functional Requirements

| ID | Title | Requirement | Category | Priority | Status |
|----|-------|-------------|----------|----------|--------|
| NFR-001 | Identity invariance | Guard tests (G1–G6) prove `source_module` is excluded from `__eq__`/`__hash__`/`body_hash`/`key_tier`/`as_tuple()`; SymbolKey allowlist cardinality is unchanged (363 total: 338 content-tier + 25 collision-tier). Measured: all guard tests present and green. | Correctness | High | Open |
| NFR-002 | No gate regression | The full `tests/architectural/test_no_dead_symbols.py` suite and the #2853 refresh-helper suite pass; `tests/architectural/test_ratchet_baselines.py` baselines are unchanged (no ratchet key added or moved). Measured: 0 failures, 0 baseline deltas. | Reliability | High | Open |
| NFR-003 | Lint/type/version hygiene | `ruff check` and `mypy --strict` are clean on every touched file; no `pyproject.toml` version bump (test-infra only, no `src/` change); a CHANGELOG entry is added. Measured: ruff 0, mypy 0, no version diff. | Maintainability | Medium | Open |

### Constraints

| ID | Title | Constraint | Category | Priority | Status |
|----|-------|------------|----------|----------|--------|
| C-001 | Field never enters hash/tier | `source_module` MUST NOT participate in `body_hash` or `key_tier`. | Technical | High | Open |
| C-002 | No tier escalation | The field MUST NOT escalate content-tier entries to collision-tier; relocation-tolerance (D-1) is preserved (content-tier keys stay location-free for equality/hash). | Technical | High | Open |
| C-003 | No ratchet key | MUST NOT add any `_baselines.yaml` / `test_ratchet_baselines.py` key for `test_no_dead_symbols`; re-adding one REDs by design (`test_readding_inert_dead_symbols_key_is_now_rejected`). | Technical | High | Open |
| C-004 | Atomic retirement | The backfill (FR-003) and the parse-path deletion (FR-004) MUST land as one coherent change set — no half-retired state where the field is populated but comment-parsing is still live, or vice-versa. | Technical | High | Open |

### Key Entities

- **SymbolKey**: the dead-symbol identity (`tests/architectural/_symbol_key.py`). Content-tier = `(bare_name, body_hash)`; collision-tier adds `module_path`. Gains `source_module` as a non-comparing provenance attribute.
- **Allowlist entry**: a `SymbolKey(...)` call in `test_no_dead_symbols.py` with an accompanying `# module::Name` provenance comment. 338 content-tier + 25 collision-tier.
- **Refresh helper**: `_refresh_dead_symbol_hashes.py` — consumes provenance to refresh `body_hash`; today parses the comment, will read `source_module`.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of the 338 content-tier allowlist entries carry `source_module` after the mission (0 depend on comment-parsing for machine decisions).
- **SC-002**: The #3560 Finding-1 same-name/same-body collision resolves via `source_module` with **no** `NEEDS_MODULE_PATH` escalation, and no still-dead symbol is admitted.
- **SC-003**: All non-goal guard tests (G1–G6, incl. the keystone `compare is False` guard) are present and green; the SymbolKey allowlist cardinality is unchanged (363).
- **SC-004**: Zero machine comment-parsing call-sites remain — the seven identified parse surfaces are removed; the comment text is retained as human audit.
