---
work_package_id: WP06
title: Glossary, Architecture Docs, and User Docs
dependencies: [WP05]
requirement_refs:
- FR-009
- FR-010
- NFR-002
planning_base_branch: 063-rename-constitution-to-charter
merge_target_branch: 063-rename-constitution-to-charter
branch_strategy: Planning artifacts for this feature were generated on 063-rename-constitution-to-charter. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into 063-rename-constitution-to-charter unless the human explicitly redirects the landing branch.
subtasks:
- T036
- T037
- T038
- T039
- T040
- T041
phase: Phase 3 - Surface Rename
assignee: ''
agent: ''
shell_pid: ''
history:
- at: '2026-04-05T05:50:00Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: curator
authoritative_surface: docs
execution_mode: code_change
lane: planned
owned_files:
- architecture/**/*.md
- docs/**/*.md
- src/specify_cli/.contextive/governance.yml
task_type: implement
---

# Work Package Prompt: WP06 – Glossary, Architecture Docs, and User Docs

## Objectives & Success Criteria

- Update 3 glossary entries to use "charter" terminology
- Update ~25 architecture files and ~23 user documentation files
- Zero stale "constitution" references in active docs (NFR-002)
- Historical context preserved where appropriate

## Context & Constraints

- **Spec**: `kitty-specs/063-rename-constitution-to-charter/spec.md` — User Story 5
- **Plan**: Stage 6 of 8. Depends on WP05 (templates already renamed).
- **Constraint C-004**: Changelog entries must NOT be changed (historical record)
- **Directive DIRECTIVE_031**: This rename is a ubiquitous language alignment — the glossary must reflect the canonical term change.
- **Agent Profile**: Curator Carla — knowledge organization and terminology specialist

## Branch Strategy

- **Strategy**: Feature branch
- **Planning base branch**: main
- **Merge target branch**: main

**Implementation command**: `spec-kitty implement WP06 --base WP05`

## Subtasks & Detailed Guidance

### Subtask T036 – Update 3 glossary entries

- **Purpose**: Update the canonical glossary to use "charter" as the authoritative term.
- **Steps**:
  1. Open `src/specify_cli/.contextive/governance.yml`
  2. Rename entries:
     - "Constitution Compiler" → "Charter Compiler" (update name and description)
     - "Constitution Interview" → "Charter Interview" (update name and description)
     - "Constitution Validation" → "Charter Validation" (update name and description)
  3. Update descriptions to reference "charter" instead of "constitution"
  4. Preserve YAML structure and formatting
- **Files**: `src/specify_cli/.contextive/governance.yml`
- **Parallel?**: No.
- **Notes**: Use careful YAML editing — `governance.yml` is structured with specific formatting. Do not alter other entries.

### Subtask T037 – Update ~25 architecture files

- **Purpose**: Align architecture documentation with new terminology.
- **Steps**:
  1. `grep -rln "constitution" architecture/ --include="*.md"` — get list of files
  2. For each file, context-aware replacement:
     - Replace `constitution` → `charter` in active descriptions, component names, path references
     - In ADRs that describe historical decisions: update terminology but preserve the decision context (e.g., "This ADR introduced the charter system, originally named constitution")
     - Key files to focus on:
       - `architecture/2.x/user_journey/005-governance-mission-constitution-operations.md` — may need filename rename too
       - `architecture/2.x/user_journey/init-doctrine-flow.md`
       - `architecture/2.x/03_components/README.md`
       - `architecture/2.x/00_landscape/README.md`
  3. Consider renaming files with "constitution" in the filename (e.g., `005-governance-mission-constitution-operations.md` → `005-governance-mission-charter-operations.md`)
- **Files**: ~25 files in `architecture/`
- **Parallel?**: Yes (parallel with T038).
- **Notes**: Architecture docs may reference "constitution" in quotes or historical context — use judgment on whether to replace.

### Subtask T038 – Update ~23 docs files

- **Purpose**: Align user-facing documentation with new terminology.
- **Steps**:
  1. `grep -rln "constitution" docs/ --include="*.md"` — get list of files
  2. For each file, replace:
     - CLI command references: `spec-kitty constitution` → `spec-kitty charter`
     - Path references: `.kittify/constitution/` → `.kittify/charter/`
     - Conceptual references: "constitution" → "charter"
     - Key files:
       - `docs/2x/doctrine-and-constitution.md` — may need filename rename to `doctrine-and-charter.md`
       - `docs/how-to/setup-governance.md`
       - `docs/reference/cli-commands.md`
       - `docs/reference/file-structure.md`
  3. Consider renaming files with "constitution" in the filename
- **Files**: ~23 files in `docs/`
- **Parallel?**: Yes (parallel with T037).

### Subtask T039 – Update plan template section headings

- **Purpose**: The plan template has a "Constitution Check" section — update if it appears generically.
- **Steps**:
  1. Check if the "Constitution Check" heading in `plan-template.md` was already updated in WP05
  2. If not, update "Constitution Check" → "Charter Check"
  3. Search for any other generic template references to "constitution" that weren't caught in WP05
- **Files**: As needed
- **Parallel?**: No.

### Subtask T040 – Verification grep for stale references

- **Purpose**: Confirm zero remaining constitution references in active documentation.
- **Steps**:
  1. `grep -ri "constitution" docs/ architecture/ --include="*.md" | grep -v _reference | grep -v curation | grep -v CHANGELOG`
  2. Review any remaining hits — they should only be in excluded contexts
  3. `grep -ri "constitution" src/specify_cli/.contextive/ --include="*.yml"` — zero hits
- **Parallel?**: No.

### Subtask T041 – Commit stage 6

- **Purpose**: Standalone commit.
- **Steps**: `git commit --no-gpg-sign -m "docs: rename constitution → charter in glossary, architecture, and user docs (stage 6/8)"`
- **Parallel?**: No.

## Risks & Mitigations

- **Over-zealous replacement**: Historical ADRs may lose context if "constitution" is replaced everywhere — preserve historical notes about the rename.
- **YAML formatting**: `governance.yml` has specific formatting — test that contextive tools still parse it correctly after edits.
- **File renames in docs**: Renaming doc files may break cross-references and links — check for relative links between docs.

## Review Guidance

- Verify changelog was NOT modified (C-004).
- Spot-check architecture ADRs for preserved historical context.
- Verify glossary entries parse correctly (YAML validation).
- Check cross-links between docs still resolve after any file renames.

## Activity Log

- 2026-04-05T05:50:00Z – system – Prompt created.
