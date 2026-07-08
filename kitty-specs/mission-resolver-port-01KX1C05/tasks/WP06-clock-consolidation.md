---
work_package_id: WP06
title: Clock consolidation (+ Sonar stamp campsite)
dependencies:
- WP01
requirement_refs:
- FR-009
- NFR-004
tracker_refs: []
planning_base_branch: feat/mission-resolver-port-2173
merge_target_branch: feat/mission-resolver-port-2173
branch_strategy: Planning artifacts for this mission were generated on feat/mission-resolver-port-2173. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/mission-resolver-port-2173 unless the human explicitly redirects the landing branch.
subtasks:
- T024
- T025
- T026
history:
- at: '2026-07-08T18:06:06+00:00'
  actor: planner
  action: created
agent_profile: randy-reducer
authoritative_surface: src/specify_cli/
create_intent:
- src/specify_cli/core/time_utils.py
- tests/specify_cli/test_clock_consolidation.py
execution_mode: code_change
owned_files:
- src/specify_cli/core/time_utils.py
- src/specify_cli/event_journal/journal.py
- src/specify_cli/event_journal/coalesce.py
- src/specify_cli/sync/migrate_journal.py
- src/specify_cli/status/reducer.py
- src/specify_cli/status/emit.py
- src/specify_cli/status/lifecycle_events.py
- src/specify_cli/retrospective/lifecycle_events.py
- src/specify_cli/retrospective/events.py
- src/specify_cli/delivery/ledger.py
- src/specify_cli/delivery/targets.py
- src/specify_cli/delivery/retention.py
- src/specify_cli/dossier/events.py
- src/specify_cli/cli/commands/agent/mission_parsing.py
- tests/specify_cli/test_clock_consolidation.py
role: implementer
tags: []
---

## ⚡ Do This First: Load Agent Profile

Load your agent profile via `/ad-hoc-profile-load` for `randy-reducer` (implementer — behavior-preserving
reduction). Then read `kitty-specs/mission-resolver-port-01KX1C05/spec.md` (FR-009, NFR-004), `plan.md`
(IC-06), and `research.md` (D-04 + census).

## Objective

Collapse the **12 byte-identical** isoformat `_now_utc` copies into **one** canonical helper, while
**preserving** the two distinct-contract helper families (2 `%Y-%m-%dT%H:%M:%SZ` stamp callers, 2
`-> datetime` callers) so on-disk timestamps do not change (NFR-004). Fold one SAFE Sonar campsite item.

## The three families (do NOT merge across them)
- **Isoformat string (12 copies → one)**: `return datetime.now(UTC).isoformat()`.
- **Stamp string (preserve, 2)**: `task_utils/support.py:101`, `cli/commands/agent/mission_parsing.py:257`
  → `%Y-%m-%dT%H:%M:%SZ` (second precision, `Z` suffix). Different serialized output — MUST NOT fold into
  the isoformat helper.
- **`datetime` (preserve, 2)**: `decisions/emit.py:64`, `decisions/service.py:86` return a `datetime`, not
  a string. Out of this WP's owned files — leave them; only note them.

## Subtasks

### T024 — One canonical isoformat helper + migrate the 12 copies
- Add `now_utc_iso() -> str` to a shared home (`src/specify_cli/core/time_utils.py` if none exists; or the
  existing canonical util — check first, do not duplicate). Body: `datetime.now(UTC).isoformat()`.
- Replace the 12 byte-identical copies (owned files list) with imports of the one helper. Delete the local
  `_now_utc`/`_utc_now_iso`/`_now_iso`/`_iso_utc_now` defs.
- The near-identical `skills/command_installer.py:361` (`datetime.now(tz=UTC).isoformat()`) folds into the
  same helper **if** owned; it is NOT in this WP's owned files — note it for a follow-up rather than reaching out.

### T025 — Triage the 2 cross-package copies
- `src/glossary/events.py:215` and `src/runtime/next/_internal_runtime/retrospective_terminus.py:63` are
  byte-identical isoformat copies **across package boundaries**. Do NOT silently stop at 12: either point
  them at the shared helper (if import direction allows) or record them **OUT with a one-line rationale**
  (import-direction). They are not in this WP's owned files — document the decision in the review; do not
  reach out to edit them here.

### T026 — SAFE Sonar campsite + NFR-004 test
- **SAFE fold**: `cli/commands/agent/mission_parsing.py:259` hard-codes `"%Y-%m-%dT%H:%M:%SZ"` — replace
  with the shared stamp constant (`UTC_SECOND_TIMESTAMP_FORMAT`/`TIMESTAMP_FORMAT`). Do NOT change the
  serialized output.
- **ADJACENT (note, don't fold)**: the literal recurs 18× with 4 redundant constant defs
  (`review/cycle.py:23`, `cli/commands/agent/tasks.py:355`, `tasks_materialization.py:43`,
  `task_utils/support.py:22`) — a separate stamp-consolidation cleanup; record it, don't do it here.
- **NFR-004 test**: new `tests/specify_cli/test_clock_consolidation.py` — assert the stamp callers produce
  byte-identical output vs a frozen expected string, and that the one canonical isoformat helper is the
  single definition (grep-style or import assertion).

## Branch Strategy
Planning branch and merge target: `feat/mission-resolver-port-2173`. Lane worktree per `lanes.json`.

## Definition of Done
- One canonical `now_utc_iso()`; the 12 owned copies import it; local dup defs deleted.
- Stamp + datetime families untouched in behavior; NFR-004 byte-identical test green.
- Cross-package copies triaged (routed or OUT-with-rationale, documented).
- `ruff`/`mypy` clean.

## Risks / reviewer guidance
- **NFR-004**: reviewer confirms no serialized timestamp format changed (diff the test's expected strings).
- Confirm the monkeypatch-based determinism tests that patched a folded `_now_utc` still control time
  (update them to patch the canonical helper).
