# Engineering Notes: Open Review Findings

**Mission**: `charter-doctrine-mission-type-configuration-01KSWJVX`
**Source**: Adversarial spec review (Opus + Sonnet, 2026-05-30)
**Status**: Captured for planning — not yet resolved in spec

These findings emerged from the interactive review session. Blockers (B-1 through B-6)
and M-1 through M-3 are resolved in the spec. The items below are paused for planning input.

---

## ~~M-3~~ — RESOLVED

- Step removal is permitted in overrides.
- `action_sequence` must be non-empty, unique step IDs.
- `action_sequence` resolves live at each `spec-kitty next` invocation.
- `spec-kitty charter activate` warns when the activated override removes a step
  for which in-flight missions are currently in the corresponding lane.
- Applied to FR-008.

---

## ~~M-4~~ — RESOLVED

`step_type` is the executor discriminant — who is responsible for execution:
- `agent` → LLM system → `kind=step`
- `human_in_loop` → human operator / HiC → `kind=decision_required`
- `integration` → external system call → `kind=blocked` (no providers this release)
Applied to FR-011.

---

## ~~M-5~~ — RESOLVED (via M-3)

`action_sequence` resolves live at each `spec-kitty next` invocation. Applied to FR-008.

---

## ~~M-6~~ — RESOLVED

"Registered" and "activated" are synonyms in charter behaviour. A mission type is
registered if and only if it is activated in the project charter. Non-activated
artifacts are non-canonical and invisible to charter-mediated resolution; doctrine
module API is the explicit escape hatch. Applied to FR-009, FR-018, and Domain Language.

---

## ~~M-7~~ — RESOLVED

`MissionStep` identity is `(mission_type_id, step_id)` — steps are entities owned
by `MissionType`, not independent aggregate roots. Two steps with the same `id`
in different mission types are independent entities. Shadowing key for step overrides
is the compound path `{mission_type_id}/{step_id}.yaml`. Applied to Key Entities,
FR-012, and the MissionStep assumption.

---

## ~~M-8~~ — RESOLVED

C-005 updated: charter module reads `.kittify/config.yaml`, validates the pack set, and
constructs a `PackContext` object. This `PackContext` is passed to the doctrine resolver;
the resolver never reads `config.yaml` directly. ACL direction is preserved: `charter →
doctrine`, not `doctrine → specify_cli`.

---

## ~~M-9~~ — RESOLVED

C-002 updated: directives and toolguides follow union-only semantics; `interview_defaults`
is explicitly exempted and follows per-key replacement semantics (overlay value wins per
key). Rationale: `interview_defaults` are behavioural preferences, not governance rules.

---

## ~~M-10~~ — RESOLVED

Five GWT contract files authored in `contracts/`:

- `org-charter-extends-union-contract.md` — FR-001 (5 contracts: union, missing base, cycle, flat-union compat, schema mismatch)
- `mission-type-override-contract.md` — FR-008 Scenario 1 (5 contracts: add step, remove step clean, remove step with in-flight warning, full replace, empty sequence error)
- `custom-mission-type-dispatch-contract.md` — FR-009 + FR-007 (4 contracts: activated type accepted, unregistered raises error, next dispatches custom sequence, existing_mission_types filters)
- `mission-step-shadowing-contract.md` — FR-012 (4 contracts: compound key scope, layer precedence, step identity independence, fallthrough)
- `activation-filtered-drg-contract.md` — FR-018 (5 contracts: non-activated type invisible, non-activated directive excluded, activation makes visible, non-activated org pack excluded, post-upgrade migration)

---

## Minor findings — ALL RESOLVED

| # | Finding | Resolution |
|---|---------|------------|
| m-1 | P2 CLI commands lack `--json`/output format | Deferred to P2 planning (no spec change needed now) |
| m-2 | "restrict" in C-002 contradicts "union only" | Resolved via M-9: C-002 reworded to "add only (never remove)" |
| m-3 | `template_set` precedence vs. project-layer DRG override unspecified | FR-015 updated: project-layer DRG shadow wins over mission-type-level `template_set` |
| m-4 | Scenario 2 removes `review` step; may break in-flight missions | Resolved by M-3 decision |
| m-5 | NFR-001 label collision with `charter_runtime/preflight` | NFR-001 qualified with `(doctrine/mission-type scope)` prefix |
| m-6 | `schema_version` absent from `OrgCharterExtension` | Added `schema_version: int` (monotonically increasing integer, baseline=1) to entity table |
| m-7 | C-003 enforcement mechanism unspecified | C-003 updated to reference `IDENTIFIER_PATTERN` in `doctrine/missions/models.py` |
| m-8 | `ResolvedMissionType` lacks referential-transparency contract | Entity table updated: "pure function of inputs; identical inputs → identical output" |
