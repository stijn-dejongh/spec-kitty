---
work_package_id: "WP15"
subtasks:
  - "T030"
  - "T031"
  - "T032"
  - "T033"
  - "T034"
title: "Profile Inheritance Resolution and Matching Integration"
phase: "Phase 2 - Foundation Wave"
lane: "planned"
dependencies:
  - "WP05"
assignee: ""
agent: ""
shell_pid: ""
review_status: ""
reviewed_by: ""
history:
  - timestamp: "2026-02-23T20:24:30Z"
    lane: "planned"
    agent: "system"
    shell_pid: ""
    action: "Prompt generated via /spec-kitty.tasks"
---

# Work Package Prompt: WP15 - Profile Inheritance Resolution and Matching Integration

## Objectives & Success Criteria
- Implement deterministic `resolve_profile()` inheritance traversal.
- Enforce shallow merge semantics from spec clarifications.
- Use resolved profiles in weighted matching.

## Context & Constraints
- Must support multi-level chains and existing hierarchy validation behavior.
- For orphan parent references, warn and return child-as-is fallback.

## Implementation Command
- `spec-kitty implement WP15 --base WP05`

## Subtasks & Detailed Guidance

### Subtask T030 - Implement ancestor traversal and resolution workflow
- **Purpose**: Create the core resolution path.
- **Steps**:
  1. Add `resolve_profile(profile_id)` API to repository.
  2. Traverse specialization chain in deterministic order.
  3. Reuse cycle detection safeguards.
- **Files**:
  - `src/doctrine/agent_profiles/repository.py`
- **Parallel?**: No.
- **Notes**: Keep error/warning behavior explicit and testable.

### Subtask T031 - Implement shallow merge semantics
- **Purpose**: Match required field-level inheritance behavior.
- **Steps**:
  1. Define merge helper for section dictionaries.
  2. Child keys override parent keys one level deep.
  3. Preserve parent keys absent from child.
- **Files**:
  - repository merge helper(s)
- **Parallel?**: No.
- **Notes**: Avoid deep recursive merge drift.

### Subtask T032 - Orphan handling and diagnostics
- **Purpose**: Handle missing parent references safely.
- **Steps**:
  1. Detect unresolved `specializes-from` links.
  2. Emit warning message with profile IDs.
  3. Return unmerged child profile as fallback.
- **Files**:
  - `src/doctrine/agent_profiles/repository.py`
- **Parallel?**: No.
- **Notes**: Ensure warnings are stable for test assertions.

### Subtask T033 - Matching integration uses resolved profiles
- **Purpose**: Include inherited specialization fields in scoring.
- **Steps**:
  1. Update matching path to resolve profiles before scoring.
  2. Keep existing weighting behavior unchanged.
  3. Confirm performance remains acceptable.
- **Files**:
  - repository matching methods
- **Parallel?**: No.
- **Notes**: Preserve ranking determinism for tied scores.

### Subtask T034 - Inheritance and matching test matrix
- **Purpose**: Verify all required edge cases.
- **Steps**:
  1. Add single-level and multi-level inheritance tests.
  2. Add shallow-merge override/preserve tests.
  3. Add orphan and cycle behavior tests.
  4. Add matching tests proving inherited fields affect scoring.
- **Files**:
  - `tests/doctrine/test_profile_inheritance.py`
  - related repository tests
- **Parallel?**: Yes.
- **Notes**: Keep fixtures readable and scenario-specific.

## Test Strategy
- Write failing inheritance tests first.
- Implement traversal + merge + matching updates until matrix passes.

## Risks & Mitigations
- Merge ambiguity: define explicit fixture expectations for each section.

## Review Guidance
- Reviewers should validate shallow merge semantics against clarification examples in spec.

## Activity Log
- 2026-02-23T20:24:30Z - system - lane=planned - Prompt created.
