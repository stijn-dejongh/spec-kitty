---
work_package_id: WP08
title: Delete the public wrapper; drain and privatise the canonicalizer
dependencies:
- WP04
- WP05
- WP06
- WP07
requirement_refs:
- FR-006
- FR-022
- FR-024
- NFR-004
- NFR-007
planning_base_branch: fix/read-side-seam-primary-primitive-closure
merge_target_branch: fix/read-side-seam-primary-primitive-closure
branch_strategy: Planning artifacts for this mission were generated on fix/read-side-seam-primary-primitive-closure. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into fix/read-side-seam-primary-primitive-closure unless the human explicitly redirects the landing branch.
subtasks:
- T035
- T036
- T037
- T038
- T039
phase: Phase 4 - Make it structural
history:
- at: '2026-07-28T09:27:08Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: python-pedro
authoritative_surface: src/specify_cli/cli/commands/agent/tasks.py
create_intent: []
execution_mode: code_change
model: claude-sonnet-5
owned_files:
- src/specify_cli/cli/commands/agent/tasks.py
- tests/architectural/surface_resolution_audit/inventory.md
role: implementer
tags: []
task_type: implement
tracker_refs:
- '3011'
---

# Work Package Prompt: WP08 – Delete the public wrapper; drain and privatise the canonicalizer

## ⚡ Do This First: Load Agent Profile
Use `/ad-hoc-profile-load` to load `python-pedro` (implementer, claude).

## Objective

Make the mission's invariant **structural instead of counted**.

Until now, "callers must not decide the partition" has been enforced by two integer floors and a
YAML allow-list. After this WP the **public name ceases to exist** — it cannot be re-imported,
so there is nothing left to police. That is the whole point of the delegate-then-remove
sequence, and this is its final step.

Three things end here: the public wrapper is **deleted**, `_canonicalize_primary_read_handle`
is **drained and privatised**, and the read-side census goes **green** for both callees WP02
added — discharging the largest block of expected reds in the mission.

## ⚠ Prerequisite check — do this before writing any code

All four routing WPs must be **approved**, not merely landed. Confirm:

```bash
spec-kitty agent tasks status --mission read-side-seam-primary-primitive-closure-01KYKMMT
# then re-derive the census yourself — never trust a written count:
```

Run the census recipe in [quickstart.md](../quickstart.md) §1. **Every** consumer site outside
the resolver module and the four named foundation sites must be routed. If any remain, stop:
deleting the wrapper with a live consumer is a broken build, not a migration.

## Context & Constraints

- **C-004 (operator-decided 2026-07-28)** — the terminal `KITTY_SPECS_DIR` **assembler** is
  module-private and **permanent**; the **public wrapper** is a transitional shim and is
  **deleted**. It is *not* merely renamed. A rename would leave a private name needing
  re-blessing in the trio gate and a name that can be re-imported; deletion leaves neither.
- **FR-022** — `_canonicalize_primary_read_handle` is a **peer** of the primitive, not an
  afterthought. The seam canonicalizes **internally**, so every routed site drained it too. It
  must be censused, drained, and privatised in **this** cycle — leaving a public leaf propped up
  by an integer floor is the shape this mission exists to remove.
- **NFR-007** — record the floor→census transfer honestly: before/after integers and the reason.
- **C-006** — do **not** extend the pinned scan-scope prefix set, and do not take on the ~14
  hand-assembled `KITTY_SPECS_DIR` paths outside sanctioned constructors (tracked separately).

**Pre-authorised out-of-map edits** (record a one-line rationale in the commit body; the
no-overlap rule is the real guard — see [tasks.md](../tasks.md) §6):

- `src/specify_cli/missions/_read_path_resolver.py` — WP03's owned file. You delete the wrapper
  and edit `__all__` there. This is the deliberate serial-by-phase handoff (IC-00 extract → IC-04
  wrapper body → IC-05 delete), recorded in plan.md's single-owner table.
- Any `tests/` module that imports a drained name — ~11 test modules plus 43 test files that
  reference the primitive by name. You are the WP whose diff makes those imports invalid.

## Doctrine for this WP

- **`tactic:refactoring-change-function-declaration`** — its **final** step: *"remove the old
  function when no callers remain"*. This WP is that step.
  `Run: spec-kitty charter context --include tactic:refactoring-change-function-declaration`
  **When doing T035**, confirm "no callers remain" by **census**, not by grep and not by this
  prompt's numbers.
- **`tactic:canonical-source-unification`** — step 5: *"do not leave a non-canonical copy as a
  fallback — fallbacks revive the split-brain silently."* This is the doctrinal case for
  **deleting** rather than deprecating.
  `Run: spec-kitty charter context --include tactic:canonical-source-unification`
  **When doing T035/T036**, resist leaving a thin deprecated alias "for safety". That alias *is*
  the fallback, and it will be re-imported.
- **`DIRECTIVE_041`** — for T037 specifically: *a green test that would stay green if the code
  regressed provides no coverage*, and the disposition taxonomy **STALE / PATCHWORK / VALID**.
  `Run: spec-kitty charter context --include directive:DIRECTIVE_041`
  **When doing T037**, the `agent/tasks.py` re-export exists **only** to serve a test patch seam.
  That is textbook PATCHWORK: **delete it and rewrite the tests against the real seam.**
  Preserving production code to keep a test green is the exact inversion this directive names.
- **`DIRECTIVE_044` (canonical sources / unification)** — `required`. Unification, not parity with
  a dead quirk; never drop a load-bearing invariant without a migration path proven safe by tests.
  `Run: spec-kitty charter context --include directive:DIRECTIVE_044`
  **When doing T039**, the migration path *is* the census — prove the transfer, do not assert it.
- **`tactic:frozen-baseline-shrink-only-ratchet`** — for T039's recorded transfer.
  `Run: spec-kitty charter context --include tactic:frozen-baseline-shrink-only-ratchet`

## Subtasks

### T035 — Delete the public wrapper and drop it from `__all__` (FR-006, SC-001)

**Steps**:
1. Re-derive the census. Confirm zero consumer sites outside the resolver module and the four
   named foundation sites.
2. **Delete** the public `primary_feature_dir_for_mission`. Do **not** rename it, do **not** leave
   a deprecated alias, do **not** leave a `__getattr__` shim.
3. Drop it from `_read_path_resolver.py`'s `__all__`. Also drop `resolve_feature_dir_for_mission`
   from `__all__` — it goes dead once its 5 importers route (Ledger M14).
4. The **private assembler stays** (C-004): it is the terminal `KITTY_SPECS_DIR` constructor the
   resolver's own PRIMARY leg is built on, and the sanctioned owner of that assembly under a
   separate gate.
5. Fix the ~11 test modules that import the deleted name. Judge each with `DIRECTIVE_041`: a test
   whose entire subject is the old shape is **PATCHWORK → delete**; a test that merely imports it
   incidentally is **STALE → re-point**.

**Validation**: `from specify_cli.missions._read_path_resolver import
primary_feature_dir_for_mission` **raises `ImportError`**. Add that as an assertion — it is the
structural claim of the whole mission.

### T036 — Drain and privatise `_canonicalize_primary_read_handle` (FR-022, SC-001)

**Steps**:
1. Census it. On this base it shows **38 sites / 22 files** — **re-derive**, since the routing WPs
   have since drained most of them (the seam canonicalizes internally, so a routed site no longer
   needs it).
2. Route or remove any residual consumer sites. Do not leave one propped up by an exemption.
3. Privatise it: no external importers, absent from `__all__`. If, after draining, it has only
   in-module callers, that is the end state — self-policing rather than floor-policed.
4. Update the ~11 test modules and the trio gate expectations accordingly. **Do not edit
   `test_trio_seam_only.py`** — WP01 owns it and already shrank the blessed set; if its positive
   assertion now fails, that is a real signal, not bookkeeping.

**Validation**: no module outside `_read_path_resolver.py` imports the name; the census confirms
it.

### T037 — Delete the `agent/tasks.py` re-export and rewrite its two tests (Ledger M15)

**Purpose**: this re-export exists **only** to serve a test patch seam. It is production code
kept alive by tests — the inversion `DIRECTIVE_041` names.

**Steps**:
1. Delete the re-export from `src/specify_cli/cli/commands/agent/tasks.py`.
2. **Rewrite the two tests against the real seam.** Do **not** preserve the re-export to keep
   them green, and do **not** delete the tests to avoid rewriting them — the second is the
   "never delete a test to fix it" failure.
3. This is one of 6 Class-A module-local patch seams (5 files) that die with `AttributeError` the
   moment a consumer stops importing the name. Expect more of them; handle each with the same
   taxonomy. One test whose **entire subject** is the old shape is **delete, don't repair**.

**Validation**: the two rewritten tests exercise the real seam and fail if the seam regresses
(mutate the seam and confirm).

### T038 — Hand-edit the second census inventory (do NOT run the rekey script)

`tests/architectural/surface_resolution_audit/inventory.md` is a **second** census that must be
kept consistent.

**⚠ The rekey script is not round-trip-safe (#3011).** Running it will corrupt entries. **Hand-edit
`inventory.md`.** If the hand edit is large enough that scripting is tempting, that is a signal to
report the #3011 hazard again, not to run it.

**Validation**: the audit suite passes; entries for routed sites are gone, entries for the four
foundation sites remain with their rationale.

### T039 — Green the read-side census; record the floor→census transfer (NFR-004, NFR-007)

**Purpose**: discharge the mission's largest block of expected reds and close the loop WP01 opened.

**Steps**:
1. Run `uv run pytest tests/architectural/test_no_read_side_bypass.py -q`. It must go **green**
   for **both** callees WP02 added — this is the red→green transition WP02 recorded.
2. Confirm **per-primitive non-vacuity** still holds: each sanctioned module carries a real
   finding **for each** censused primitive, not merely for a previously-censused one.
3. Confirm the **staleness twin-guard** bites: an allow-list entry whose site was routed or
   removed must **red** until deleted. Delete the stale ones.
4. Record the transfer in the commit body: WP01 retired floors *X → retired*, and the guarantee
   now lives in the read-side census with its own concrete floor of *N*. Cite `DIRECTIVE_043` and
   `tactic:architectural-gate-non-vacuity`. This is the closing half of WP01's adjudication —
   without it the retirement reads as an unguarded relaxation.
5. Reconcile against WP01's `.expected-reds.md`: every entry this WP was expected to green **is**
   green, and **nothing previously green went red** (SC-020 scenario 2).

**Validation**: all six C-008 gates green except any entry still legitimately owned by WP09.

## Branch Strategy

- Planning/base branch: **`fix/read-side-seam-primary-primitive-closure`**
- Final merge target: **`fix/read-side-seam-primary-primitive-closure`**
- Worktree allocated **per computed lane** from `lanes.json` by `spec-kitty implement WP08`.
  Never hand-construct it; never `git stash` inside a lane worktree.

## Test strategy

```bash
# the structural claim
uv run python -c "
from specify_cli.missions import _read_path_resolver as m
assert not hasattr(m, 'primary_feature_dir_for_mission'), 'public wrapper still present'
print('wrapper gone')
"
PWHEADLESS=1 SPEC_KITTY_SYNC_MINIMAL_IMPORT=1 uv run pytest \
  tests/specify_cli/ tests/architectural/surface_resolution_audit/ -q
```

Plus the six C-008 gates (tasks.md §5), `uv run ruff check <changed>`, and project-mode
`uv run python -m mypy --strict src/specify_cli src/charter src/doctrine`.

## Definition of Done

- The public wrapper **does not exist**; importing it raises `ImportError`, asserted by a test
  (T035, SC-001).
- Both drained names are absent from `__all__`; no deprecated alias or `__getattr__` shim remains.
- The **private assembler survives** with only in-module and named-sanctioned callers (C-004).
- `_canonicalize_primary_read_handle` drained and non-public, confirmed by census (T036).
- The `agent/tasks.py` re-export **deleted** and its two tests **rewritten against the real
  seam** — neither preserved nor deleted (T037).
- `inventory.md` hand-edited; the rekey script **not run** (T038, #3011).
- The read-side census **green for both new callees**, with per-primitive non-vacuity intact and
  the staleness twin-guard biting (T039).
- The floor→census transfer recorded with before/after integers, the reason, and the
  `DIRECTIVE_043` citation (T039, NFR-007).
- `.expected-reds.md` reconciled: expected greens are green; nothing previously green went red.
- `ruff` and project-mode `mypy` clean.
- Finish: commit, `mark-status T035 T036 T037 T038 T039 --status done`, then `move-task WP08 --to
  for_review` and **wait** for the synchronous pre-review gate.

## Risks

- **Deleting with a live consumer is a broken build.** Re-derive the census; do not trust counts.
- **A "safety" alias defeats the entire mission.** The public name must be gone, not deprecated.
- **Preserving the `agent/tasks.py` re-export to keep two tests green** is the single clearest
  instance of tests-as-friction in this mission. Delete it; rewrite them.
- **Never delete a test to avoid rewriting it.** If a test's subject is genuinely the old shape,
  say so explicitly and delete it as PATCHWORK with the rationale recorded — that is a different
  act from deleting it because it is inconvenient.
- **Do not run the rekey script** (#3011, not round-trip-safe).
- **Do not edit `test_trio_seam_only.py` or `test_no_read_side_bypass.py`** — WP01 and WP02 own
  them. If their assertions fail after your change, that is signal.

## Reviewer guidance

1. Try the import yourself. Does `primary_feature_dir_for_mission` raise `ImportError`? Is there
   a shim, alias, or `__getattr__` anywhere?
2. Re-run the census. Is `_canonicalize_primary_read_handle` genuinely drained, or merely
   exempted?
3. `agent/tasks.py`: was the re-export **deleted** and the tests **rewritten against the real
   seam** — or were the tests deleted, or the re-export kept?
4. Does per-primitive non-vacuity still hold for **each** censused primitive independently?
5. Does the commit body carry the floor→census transfer with before/after integers and the
   `DIRECTIVE_043` citation? WP01's retirement is only honest once this is recorded.
6. Reconcile `.expected-reds.md`: did anything **previously green** go red?
