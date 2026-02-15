---
work_package_id: WP04
title: Documentation
lane: "done"
dependencies:
- WP01
subtasks:
- T018
- T019
phase: Phase 3 - Polish
assignee: ''
agent: ''
shell_pid: ''
review_status: "approved"
reviewed_by: "Stijn Dejongh"
history:
- timestamp: '2026-02-15T00:24:27Z'
  lane: planned
  agent: system
  shell_pid: ''
  action: Prompt generated via /spec-kitty.tasks
---

# Work Package Prompt: WP04 – Documentation

## ⚠️ IMPORTANT: Review Feedback Status

**Read this first if you are implementing this task!**

- **Has review feedback?**: Check the `review_status` field above. If it says `has_feedback`, scroll to the **Review Feedback** section immediately.
- **You must address all feedback** before your work is complete.
- **Mark as acknowledged**: When you understand the feedback, update `review_status: acknowledged`.

---

## Review Feedback

> **Populated by `/spec-kitty.review`** – Reviewers add detailed feedback here when work needs changes.

*[This section is empty initially.]*

---

## Objectives & Success Criteria

- Glossary entries for all new event system types exist with correct `In code` references.
- CLAUDE.md project structure section includes `core/events/` and `telemetry/` packages.
- All entries follow existing glossary format and style.

## Context & Constraints

- **Glossary format**: Follow the table-based format in `glossary/README.md` (Definition, Context, Status, In code, Related terms).
- **Context**: "Events & Telemetry" (matches existing section in glossary).
- **Status**: "canonical" for all new entries.
- **Glossary already has event entries**: The glossary already contains EventBridge, LaneTransitionEvent, ValidationEvent, ExecutionEvent entries in the "Events & Telemetry" section. **Verify and update** these entries to match the actual implementation — don't duplicate.

## Implementation Command

```bash
spec-kitty implement WP04 --base WP02
```

Can run in parallel with WP03.

## Subtasks & Detailed Guidance

### Subtask T018 — Update Glossary

**Purpose**: Ensure glossary entries for event system types reference the correct code locations from WP01/WP02 implementation.

**Steps**:
1. Open `glossary/README.md`
2. Find the "Context: Events & Telemetry" section
3. **Verify existing entries** — the glossary already has entries for EventBridge, NullEventBridge, CompositeEventBridge, LaneTransitionEvent, ValidationEvent, ExecutionEvent. Update `In code` references to match actual file paths:
   - EventBridge: `EventBridge` (ABC) in `src/specify_cli/core/events/bridge.py`
   - NullEventBridge: `NullEventBridge` in `src/specify_cli/core/events/bridge.py`
   - CompositeEventBridge: `CompositeEventBridge` in `src/specify_cli/core/events/bridge.py`
   - LaneTransitionEvent: `LaneTransitionEvent` (Pydantic BaseModel, frozen) in `src/specify_cli/core/events/models.py`
   - ValidationEvent: `ValidationEvent` (Pydantic BaseModel, frozen) in `src/specify_cli/core/events/models.py`
   - ExecutionEvent: `ExecutionEvent` (Pydantic BaseModel, frozen) in `src/specify_cli/core/events/models.py`
4. **Add missing entry** for JsonlEventWriter if not present:

```markdown
### JsonlEventWriter

| | |
|---|---|
| **Definition** | JSONL file appender that serializes Pydantic event models as one JSON object per line. Handles write failures gracefully (logs warning, does not crash workflow). |
| **Context** | Events & Telemetry |
| **Status** | canonical |
| **In code** | `JsonlEventWriter` in `src/specify_cli/telemetry/jsonl_writer.py` |
| **Related terms** | [EventBridge](#eventbridge), [CompositeEventBridge](#compositeventbridge) |
```

5. **Add missing entry** for `load_event_bridge` factory if not present:

```markdown
### Event Bridge Factory

| | |
|---|---|
| **Definition** | Factory function `load_event_bridge(repo_root)` that reads `.kittify/config.yaml` telemetry settings and returns the appropriate EventBridge. Returns NullEventBridge when telemetry is disabled or config is missing/malformed. |
| **Context** | Events & Telemetry |
| **Status** | canonical |
| **In code** | `load_event_bridge()` in `src/specify_cli/core/events/factory.py` |
| **Related terms** | [EventBridge](#eventbridge), [NullEventBridge](#nulleventbridge), [JsonlEventWriter](#jsonleventwriter) |
```

**Files**:
- `glossary/README.md` (modified)

---

### Subtask T019 — Update CLAUDE.md

**Purpose**: Add new packages to CLAUDE.md project structure.

**Steps**:
1. Open `CLAUDE.md`
2. Find the project structure section
3. Add entries for the new packages:
   - `src/specify_cli/core/events/` — Event ABCs, Pydantic models, factory
   - `src/specify_cli/telemetry/` — JSONL event writer
4. Keep additions minimal — match existing style.

**Files**:
- `CLAUDE.md` (modified — 2-3 lines added)

---

## Risks & Mitigations

- **Documentation drift**: Keep entries focused on "what" and "where", not implementation details.
- **Glossary duplicates**: Check for existing entries before adding — update rather than duplicate.

## Review Guidance

- Verify `In code` references match actual file paths from WP01/WP02.
- Verify no duplicate glossary entries.
- Verify CLAUDE.md additions are minimal and match existing style.

## Activity Log

- 2026-02-15T00:24:27Z – system – lane=planned – Prompt created.
- 2026-02-15T01:03:14Z – unknown – lane=done – Moved to done
