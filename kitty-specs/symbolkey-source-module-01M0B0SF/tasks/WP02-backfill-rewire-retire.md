---
work_package_id: WP02
title: Backfill + helper rewire + parse retirement + completeness/integrity guards (ATOMIC)
dependencies:
- WP01
requirement_refs:
- C-003
- C-004
- FR-002
- FR-003
- FR-004
- FR-005
- FR-006
- FR-007
- NFR-001
- NFR-002
planning_base_branch: remediation/symbolkey-source-module-3552
merge_target_branch: remediation/symbolkey-source-module-3552
branch_strategy: Planning artifacts for this mission were generated on remediation/symbolkey-source-module-3552. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into remediation/symbolkey-source-module-3552 unless the human explicitly redirects the landing branch.
subtasks:
- T007
- T008
- T009
- T010
- T011
- T012
- T013
- T014
history:
- at: '2026-08-18T18:20:00+00:00'
  actor: claude
  note: WP created by /spec-kitty.tasks
agent_profile: python-pedro
authoritative_surface: tests/architectural/test_no_dead_symbols.py
create_intent: []
execution_mode: code_change
owned_files:
- tests/architectural/test_no_dead_symbols.py
- tests/architectural/_refresh_dead_symbol_hashes.py
- tests/architectural/test_refresh_dead_symbol_hashes.py
role: implementer
tags: []
tracker_refs: []
---

## ⚡ Do This First: Load Agent Profile

Load your profile: `/ad-hoc-profile-load python-pedro` (or `spec-kitty agent profile show python-pedro` + `spec-kitty charter context --action implement --json`). ATDD; `mypy --strict` + zero new suppressions; complexity ≤ 15; realistic test data; never green-wash a red.

## Objective

Make `source_module` the single canonical provenance source: backfill it onto every content-tier
allowlist entry, rewire the refresh helper to read it, delete the machine comment-parse surfaces,
and add the completeness + integrity guards that replace what the deletion removes — **all in one
commit**. This is the heart of #3552.

## ⚠️ ATOMICITY (C-004) — this is ONE WP on ONE lane

`ruff` line-length is **164** (`pyproject.toml`). Many content-tier allowlist lines already sit at
164; appending `source_module="…"` overflows → E501. Forcing an entry multi-line shifts its
`Call.lineno`, which reds the still-live `test_every_content_tier_entry_has_parseable_provenance_comment`
(it matches the comment at `lineno`/`lineno-1`). Therefore the reflow (T007) and that test's deletion
(T009) **must land in the same commit**. Do not split this WP across lanes or commits in a way that
leaves the suite red mid-way. `decide()` and the `NEEDS_MODULE_PATH` outcome are **unchanged** — this
mission is provenance-only; a live collision still correctly escalates (confirm, do not rewrite).

## Context

- Allowlist source: `tests/architectural/test_no_dead_symbols.py` — content-tier entries are
  `SymbolKey("Name","hash")` (no `module_path=`) with a `# module::Name` provenance comment
  (2 formats today: trailing 192, preceding 146). Collision-tier entries already carry `module_path=`.
- Helper: `tests/architectural/_refresh_dead_symbol_hashes.py` — `AllowlistEntry.module_path`
  currently recovers from the comment via `_recover_provenance` (~L237) / `_comments_by_row` (~L183).
  `parse_allowlist_entries` calls `_recover_provenance` (~L276). `Outcome.UNRECOVERABLE` (~L88) is the
  generic fail-closed branch.
- Parse surfaces to delete (paula's verified list): `_PROVENANCE_COMMENT_RE` (`test_no_dead_symbols.py:1435`),
  `_content_tier_entry_lines`/`_comments_by_line` (`:1440-1481`), `test_every_content_tier_entry_has_parseable_provenance_comment` (`:1484-1513`),
  `_comments_by_row` (`_refresh_dead_symbol_hashes.py:183-194`), `_recover_provenance` + its call (`:237-251`, `:276`),
  `AllowlistEntry.module_path` comment branch (`:132-141`).
- Blast radius: `test_refresh_dead_symbol_hashes.py` builds `AllowlistEntry` via a local `_entry()`
  helper passing `provenance_module=`/`kwarg_module_path=`, and asserts on `Outcome.UNRECOVERABLE`.
  Its two #3560 tests (`test_decide_escalates_content_tier_entry_needing_collision_tier`,
  `..._escalates_end_to_end`) assert `NEEDS_MODULE_PATH` is correct — they MUST stay green.

## Subtasks

### T007 — Backfill script (reuse the verified reader; handle E501) and run it
Write a one-shot script (ephemeral — do NOT commit it; keep it in scratch). It MUST:
1. Import and call the existing `_content_tier_entry_lines`/`_comments_by_line` reader **before it is deleted** to source each content-tier entry's module (do not hand-roll a second comment parser — that risks missing the `preceding` format for 146 entries).
2. For each content-tier `SymbolKey(...)` call in the allowlist frozensets, insert `source_module="<module>"` as a kwarg. If the resulting line exceeds 164, reflow the call to a canonical multi-line form.
3. **Assert** the reader's own allowlist-scoped count equals the number of entries backfilled — abort on mismatch (this makes SC-001 a mechanical gate; never hardcode 338).
4. Run it; then eyeball `git diff` for sanity (correct module per symbol, no collision-tier entries touched).

### T008 — Rewire the helper
`AllowlistEntry.module_path` returns `self.source_module` (parsed from the `source_module=` kwarg via the AST) instead of the recovered comment. Delete `_recover_provenance` and its call in `parse_allowlist_entries`, and delete `_comments_by_row`. Add `source_module` parsing to `parse_allowlist_entries` (read the kwarg from the `SymbolKey(...)` call).

### T009 — Delete the test-side parse surfaces (same commit as T007 reflow)
Delete `_PROVENANCE_COMMENT_RE`, `_content_tier_entry_lines`/`_comments_by_line`, and `test_every_content_tier_entry_has_parseable_provenance_comment` from `test_no_dead_symbols.py`. Keep the `# module::Name` comment TEXT on the entries (human audit).

### T010 — Reword `Outcome.UNRECOVERABLE` (keep the branch)
Its `decide()` branch is the generic fail-closed backstop for any entry missing provenance — **keep it**. Only update the comment-specific docstring wording (it no longer "could not be recovered from the comment"; it's "no `source_module` recovered").

### T011 — Completeness + integrity guards (FR-006 / FR-007)
- `test_every_content_tier_entry_has_source_module`: fails if any allowlist-scoped content-tier `SymbolKey(...)` lacks a `source_module=` kwarg (replaces the deleted parseable-comment gate; keeps SSOT as the corpus grows).
- Integrity guard: every entry's `source_module` matches its retained `# module::Name` audit comment (and/or is a known corpus module) — replaces `_recover_provenance`'s `Name == bare_name` cross-check so drift can't move onto the field.

### T012 — Comment-independent recovery test (FR-005 / SC-002)
Red-first: with `source_module` set, garble/delete the entry's provenance comment and assert the helper's recovered module + refresh decision are unchanged. Show it fails against the pre-rewire (comment-parsing) code and passes after.

### T013 — Fix the blast-radius suite
Update `test_refresh_dead_symbol_hashes.py`'s `_entry()` fixtures / `UNRECOVERABLE` assertions to the new `source_module` model. **Confirm** the two #3560 Finding-1 tests still pass asserting `NEEDS_MODULE_PATH` (do not touch their intent).

### T014 — Verify
```bash
uv run ruff check tests/architectural/test_no_dead_symbols.py tests/architectural/_refresh_dead_symbol_hashes.py tests/architectural/test_refresh_dead_symbol_hashes.py
uv run mypy --strict tests/architectural/_refresh_dead_symbol_hashes.py tests/architectural/test_refresh_dead_symbol_hashes.py
PWHEADLESS=1 uv run pytest tests/architectural/test_no_dead_symbols.py tests/architectural/test_refresh_dead_symbol_hashes.py tests/architectural/test_ratchet_baselines.py -q
# SC-004: no machine parse surface remains
grep -nE "_recover_provenance|_PROVENANCE_COMMENT_RE|_comments_by_row|test_every_content_tier_entry_has_parseable_provenance_comment" tests/architectural/ -r || echo "parse surfaces retired"
```
All green; ratchet baselines unchanged; allowlist cardinality equal pre/post.

## Branch Strategy

Planning base and merge target are both `remediation/symbolkey-source-module-3552`. This WP depends on WP01 and branches from WP01's completed base; execution worktree per `lanes.json`. All three owned files are in this one lane (no cross-lane split).

## Definition of Done

- Every content-tier entry carries `source_module=` (FR-003; mechanically asserted, FR-006).
- Helper reads `source_module`; the 6 machine parse surfaces are gone; comment text kept (FR-002/FR-004/SC-004).
- `Outcome.UNRECOVERABLE` branch retained (docstring reworded).
- FR-005 comment-independent test + FR-007 integrity guard green; #3560 tests green.
- ruff + mypy --strict clean; full suites green; ratchet baselines + cardinality unchanged. **No `_baselines.yaml`/ratchet key added (C-003).**

## Reviewer guidance

Verify atomicity (single commit; no red intermediate), that the backfill reused the verified reader (not a re-implemented parser), that `source_module` values are correct per symbol (spot-check the `preceding`-format entries), that `decide()`/`NEEDS_MODULE_PATH` logic is untouched, and that no ratchet baseline moved.
