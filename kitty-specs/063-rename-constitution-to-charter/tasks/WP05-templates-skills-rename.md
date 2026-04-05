---
work_package_id: WP05
title: Templates and Skills Rename
dependencies: [WP04]
requirement_refs:
- FR-007
- FR-008
planning_base_branch: 063-rename-constitution-to-charter
merge_target_branch: 063-rename-constitution-to-charter
branch_strategy: Planning artifacts for this feature were generated on 063-rename-constitution-to-charter. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into 063-rename-constitution-to-charter unless the human explicitly redirects the landing branch.
subtasks:
- T029
- T030
- T031
- T032
- T033
- T034
- T035
phase: Phase 3 - Surface Rename
assignee: ''
agent: ''
shell_pid: ''
history:
- at: '2026-04-05T05:50:00Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: python-implementer
authoritative_surface: src/specify_cli/missions
execution_mode: code_change
lane: planned
owned_files:
- src/doctrine/skills/spec-kitty-charter-doctrine/**
- src/specify_cli/missions/**/command-templates/charter.md
- src/specify_cli/missions/**/templates/*.md
task_type: implement
---

# Work Package Prompt: WP05 – Templates and Skills Rename

## Objectives & Success Criteria

- Rename command template `constitution.md` → `charter.md` and update content
- Update all 7 other template files that reference constitution
- Rename skill directory `spec-kitty-constitution-doctrine/` → `spec-kitty-charter-doctrine/`
- Update skill content (SKILL.md, reference files)
- Template cleanliness tests pass

## Context & Constraints

- **Spec**: `kitty-specs/063-rename-constitution-to-charter/spec.md` — User Story 4
- **Plan**: Stage 5 of 8. Depends on WP04 (CLI commands renamed).
- **Constraint C-005**: Legacy agent config copies (`.cursor/`, `.codex/`, etc.) must NOT be modified — they're updated via `spec-kitty upgrade`.
- **Tactic**: Change Function Declaration (simple mechanics) for filename + content renames.

## Branch Strategy

- **Strategy**: Feature branch
- **Planning base branch**: main
- **Merge target branch**: main

**Implementation command**: `spec-kitty implement WP05 --base WP04`

## Subtasks & Detailed Guidance

### Subtask T029 – git mv constitution.md → charter.md (template)

- **Purpose**: Rename the primary command template.
- **Steps**:
  1. `git mv src/specify_cli/missions/software-dev/command-templates/constitution.md src/specify_cli/missions/software-dev/command-templates/charter.md`
  2. Update content inside `charter.md`:
     - Replace all `constitution` → `charter` in command names, paths, descriptions
     - Update `.kittify/constitution/` → `.kittify/charter/` path references
     - Update `spec-kitty constitution` → `spec-kitty charter` CLI references
- **Files**: `src/specify_cli/missions/software-dev/command-templates/charter.md`
- **Parallel?**: Yes (parallel with T031).

### Subtask T030 – Update 7 other template files

- **Purpose**: Fix constitution references in templates that reference the constitution workflow.
- **Steps**:
  1. Update each file, replacing `constitution` → `charter` in:
     - `src/specify_cli/missions/software-dev/command-templates/specify.md` — constitution context bootstrap section
     - `src/specify_cli/missions/software-dev/command-templates/plan.md` — constitution context bootstrap + Constitution Check heading
     - `src/specify_cli/missions/software-dev/command-templates/analyze.md` — constitution references
     - `src/specify_cli/missions/software-dev/templates/plan-template.md` — "Constitution Check" section heading
     - `src/specify_cli/missions/software-dev/templates/task-prompt-template.md` — constitution.md reference
     - `src/specify_cli/missions/documentation/templates/task-prompt-template.md` — constitution references
     - `src/specify_cli/missions/research/templates/task-prompt-template.md` — constitution references
  2. Be careful with section headings that other tools may parse (e.g., "Constitution Check" → "Charter Check")
- **Files**: 7 template/markdown files
- **Parallel?**: Yes (each file is independent).
- **Notes**: The plan-template.md `## Constitution Check` heading may be parsed by automation — verify no hardcoded references exist in Python code.

### Subtask T031 – git mv skill directory

- **Purpose**: Rename the skill from constitution to charter.
- **Steps**:
  1. `git mv src/doctrine/skills/spec-kitty-constitution-doctrine/ src/doctrine/skills/spec-kitty-charter-doctrine/`
  2. Verify directory exists at new location
- **Files**: `src/doctrine/skills/spec-kitty-charter-doctrine/`
- **Parallel?**: Yes (parallel with T029).

### Subtask T032 – Update skill content

- **Purpose**: Replace all constitution references in skill files.
- **Steps**:
  1. In `src/doctrine/skills/spec-kitty-charter-doctrine/SKILL.md` (~600 lines):
     - Replace skill name references: `spec-kitty-constitution-doctrine` → `spec-kitty-charter-doctrine`
     - Replace CLI command references: `spec-kitty constitution` → `spec-kitty charter`
     - Replace path references: `.kittify/constitution/` → `.kittify/charter/`
     - Replace conceptual references: "constitution" → "charter" in descriptions
  2. In `references/constitution-command-map.md`:
     - Rename file to `charter-command-map.md` (via `git mv`)
     - Update all content references
  3. In `references/doctrine-artifact-structure.md`:
     - Update constitution references
- **Files**: 3 files in `src/doctrine/skills/spec-kitty-charter-doctrine/`
- **Parallel?**: Yes (after T031).

### Subtask T033 – Update template registry/migration refs

- **Purpose**: Ensure any code that references the old template/skill names is updated.
- **Steps**:
  1. Search for `"constitution.md"` or `"spec-kitty-constitution"` in Python source:
     `grep -rn "constitution.md\|spec-kitty-constitution" src/ --include="*.py" | grep -v upgrade/migrations | grep -v __pycache__`
  2. Update any template registry entries, skill loading code, or migration references
  3. Check `src/specify_cli/missions/*/mission.yaml` for template filename references
- **Files**: As found by grep
- **Parallel?**: No.

### Subtask T034 – Verify templates + skills

- **Purpose**: Confirm all renames are clean.
- **Steps**:
  1. Run template cleanliness tests: `pytest tests/specify_cli/test_command_template_cleanliness.py`
  2. Run skill-related tests if they exist
  3. `grep -rn "constitution" src/specify_cli/missions/ src/doctrine/skills/ --include="*.md" | grep -v _reference` — zero hits
- **Parallel?**: No.

### Subtask T035 – Commit stage 5

- **Purpose**: Standalone commit.
- **Steps**: `git commit --no-gpg-sign -m "refactor: rename templates + skills constitution → charter (stage 5/8)"`
- **Parallel?**: No.

## Risks & Mitigations

- **Template parsing**: Some automation may parse section headings like "Constitution Check" — grep for hardcoded heading strings in Python code before renaming.
- **Skill loading**: The skill name change may require updating skill registry or discovery code.

## Review Guidance

- Verify no legacy agent copies (`.claude/`, `.codex/`, etc.) were modified (C-005).
- Spot-check SKILL.md for completeness — it's a large file (~600 lines).
- Verify the `charter-command-map.md` rename happened (not just content update).

## Activity Log

- 2026-04-05T05:50:00Z – system – Prompt created.
