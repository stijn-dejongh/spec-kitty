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

## M-5 — Live vs. frozen `action_sequence` for in-flight missions

If `action_sequence` resolves fresh on each `spec-kitty next` call, a mid-flight
org-pack update can silently change the sequence of a running mission. If frozen
at create time, the spec must say where the snapshot lives.

**Decision needed**: Is `action_sequence` frozen in `meta.json` at mission create
time, or re-resolved live at each `spec-kitty next` invocation?

---

## M-6 — Mission-type registry: what constitutes "registration"

FR-009 requires `charter.existing_mission_types(repo_root)` to enumerate registered
types. But the spec doesn't define what makes a type "registered" in the DRG
inventory — is it any YAML file present in any layer's `mission-types/` directory,
or does it require an explicit activation entry in the charter?

**Decision needed**: Is presence in a `mission-types/` directory sufficient for
registration, or does activation (FR-018) also gate registration?

---

## M-7 — `DoctrineTemplate.id` matching key for shadowing

FR-014 says org/project layers shadow a built-in template "by providing a file with
the same `id`." Template IDs are untyped strings — not URNs, not file paths.
The resolution matching key is unspecified.

**Decision needed**: Is shadowing keyed by filename stem (consistent with the
filesystem-based DRG pattern) or by an explicit `id` field in template frontmatter?

---

## M-8 — C-005 inverts ACL dependency direction

C-005 requires all packs in an `extends:` chain to be listed in `.kittify/config.yaml`.
This makes the Doctrine resolver depend on a `specify_cli` runtime config artifact,
inverting the ACL direction declared in C-004.

**Decision needed**: Does the pack registry live in the Doctrine BC (self-contained),
or does the charter module receive a pre-loaded pack set from the runtime (keeping
dependency direction correct)? The latter aligns with how `LayerContext` is constructed
in the dispatch contract.

---

## M-9 — `interview_defaults` per-key override vs. C-002 "add only"

FR-001 says `interview_defaults` resolve "per-key, overlay key wins" (replacement
semantics). C-002 says overlay can only "add, never remove." Per-key replacement is
neither add nor remove — it is overwrite. The two clauses are in tension.

**Decision needed**: Is `interview_defaults` explicitly exempted from C-002's union
rule (overlay replacement is intentional for defaults), and should C-002 be clarified
to say "directives and toolguides union only; interview_defaults override per-key"?

---

## M-10 — BDD behavioral contracts absent (active tactic mandate)

The architect-alphonso profile mandates Given/When/Then contracts before implementation.
The spec has narrative scenarios and success criteria but no GWT contracts beyond
those in `contracts/action-sequence-dispatch-contract.md` and
`contracts/directive-scope-contract.md`.

**Needed before planning**:
- GWT for org-charter `extends:` union resolution (FR-001)
- GWT for mission-type override extending built-in type (FR-008, Scenario 1)
- GWT for custom mission type creation and `spec-kitty next` dispatch (FR-009)
- GWT for `MissionStep` override shadowing (FR-012)
- GWT for activation-filtered DRG traversal (FR-018)

These can be authored as additional contract files or added to existing contracts.

---

## Minor findings (deferred)

| # | Finding | Suggested action |
|---|---------|-----------------|
| m-1 | P2 CLI commands (`template list`, `mission-type list`, `mission-type show`) lack `--json`, output format, command group | Add interface sketch when P2 work is planned |
| m-2 | "restrict" in C-002 contradicts "union only" in FR-001 | Reword C-002: "add only (never remove)" |
| m-3 | `template_set` precedence vs. project-layer DRG override unspecified | State: project-layer DRG shadow wins over mission-type-level `template_set` |
| m-4 | Scenario 2 removes `review` step; may break in-flight missions mid-flight | Resolved by M-3 decision |
| m-5 | NFR-001 label collision: `charter_runtime/preflight` uses NFR-001 for a different budget | Renumber new latency NFR or qualify with module scope |
| m-6 | `schema_version` not in any entity table; no version policy defined | Add `schema_version` to `OrgCharterExtension` entity; specify integer or semver |
| m-7 | C-003 enforcement mechanism unspecified | Reference `IDENTIFIER_PATTERN` in `doctrine/missions/models.py` |
| m-8 | `ResolvedMissionType` has no equality or referential-transparency contract | Add: "pure function of inputs; identical inputs → identical output" |
