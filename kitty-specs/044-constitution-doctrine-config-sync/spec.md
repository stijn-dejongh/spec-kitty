# Feature Specification: Constitution to Doctrine Config Sync

**Feature Branch**: `044-constitution-doctrine-config-sync`
**Created**: 2026-02-14
**Status**: Draft
**Input**: One-way sync from Constitution (human narrative) to .doctrine-config/ (machine config). Re-sync on amendment.

## User Scenarios & Testing

### User Story 1 - Generate Doctrine Config from Constitution (Priority: P1)

As a project owner, after creating or updating my Constitution via `/spec-kitty.constitution`, the system generates a `.doctrine-config/` directory with machine-parseable YAML that reflects my Constitution's rules.

**Why this priority**: This is the core sync mechanism. Without it, Constitution and .doctrine-config/ are disconnected.

**Independent Test**: Create a Constitution with testing standards ("minimum 80% coverage"), code quality rules ("conventional commits"), and branch strategy. Run sync. Verify .doctrine-config/config.yaml contains corresponding structured entries.

**Acceptance Scenarios**:

1. **Given** a Constitution with "Testing: minimum 80% coverage, TDD required", **When** sync runs, **Then** `.doctrine-config/config.yaml` contains `testing: { coverage_minimum: 80, tdd_required: true }`.
2. **Given** a Constitution with custom branch strategy, **When** sync runs, **Then** `.doctrine-config/repository-guidelines.md` reflects the branch strategy.
3. **Given** no Constitution file exists, **When** sync is attempted, **Then** a clear error message indicates the Constitution must be created first.

---

### User Story 2 - Re-sync on Constitution Amendment (Priority: P1)

As a project owner, when I amend my Constitution (via `/spec-kitty.constitution` or manual edit), the sync runs again and updates .doctrine-config/ to reflect the changes.

**Why this priority**: Governance drift between Constitution and config is the "two-masters" risk. Re-sync on amendment prevents it.

**Independent Test**: Generate initial config. Modify the Constitution to change coverage from 80% to 60%. Run sync. Verify config.yaml is updated to 60%.

**Acceptance Scenarios**:

1. **Given** an existing .doctrine-config/ generated from Constitution v1, **When** the Constitution is amended (v2) and sync runs, **Then** .doctrine-config/ reflects v2.
2. **Given** a Constitution amendment that removes a section, **When** sync runs, **Then** the corresponding config entry is removed.
3. **Given** manual edits to .doctrine-config/ that conflict with Constitution, **When** sync runs, **Then** Constitution wins (one-way sync) and a warning notes the overwritten manual changes.

---

### User Story 3 - Sync Produces Valid Doctrine Config (Priority: P2)

As the DoctrineGovernancePlugin (Feature 043), when I load .doctrine-config/, the generated files are valid and parseable, so governance checks work correctly.

**Why this priority**: The sync output must be consumable by the governance provider. Invalid output breaks the chain.

**Independent Test**: Generate .doctrine-config/ from a realistic Constitution. Load it with the DoctrineGovernancePlugin. Verify no parse errors.

**Acceptance Scenarios**:

1. **Given** a generated .doctrine-config/config.yaml, **When** parsed by the DoctrineGovernancePlugin loader, **Then** all fields are valid and correctly typed.
2. **Given** a Constitution with all supported sections filled, **When** synced, **Then** the generated config covers: testing standards, code quality, commit conventions, architecture constraints, and relevant directives.

---

### Edge Cases

- What happens when the Constitution uses non-standard section headings? Best-effort parsing with warnings for unrecognized sections.
- What happens when the Constitution contains ambiguous values (e.g., "high test coverage")? Map to reasonable defaults with a warning suggesting explicit values.
- What happens when .doctrine-config/ already exists from manual creation? Overwrite with sync output (one-way sync), but backup the existing files first.

## Requirements

### Functional Requirements

- **FR-001**: System MUST parse the Constitution markdown and extract structured governance rules (testing standards, code quality, commit conventions, branch strategy, architecture constraints).
- **FR-002**: System MUST generate `.doctrine-config/config.yaml` from extracted rules.
- **FR-003**: System MUST generate `.doctrine-config/repository-guidelines.md` with project-specific narrative sections.
- **FR-004**: System MUST include a precedence declaration in generated config referencing the Doctrine hierarchy.
- **FR-005**: Sync MUST be re-triggerable — running it again overwrites .doctrine-config/ with current Constitution state.
- **FR-006**: System MUST warn when overwriting manual .doctrine-config/ edits (backup before overwrite).
- **FR-007**: System MUST provide a CLI command (`spec-kitty sync constitution`) to trigger the sync.
- **FR-008**: System SHOULD auto-trigger sync when `/spec-kitty.constitution` completes (hook or post-command step).
- **FR-009**: Generated config MUST be valid and loadable by the DoctrineGovernancePlugin (Feature 043).
- **FR-010**: System MUST handle Constitutions with missing sections gracefully (omit corresponding config entries).

### Key Entities

- **ConstitutionParser**: Extracts structured rules from Constitution markdown sections.
- **DoctrineConfigGenerator**: Produces .doctrine-config/ directory contents from parsed rules.
- **SyncReport**: Summary of what was generated, what was overwritten, and any warnings.

## Success Criteria

### Measurable Outcomes

- **SC-001**: Sync produces valid .doctrine-config/ that passes DoctrineGovernancePlugin loading without errors.
- **SC-002**: Round-trip: Constitution -> sync -> governance check works end-to-end.
- **SC-003**: Re-sync after amendment correctly reflects all changes.
- **SC-004**: Manual .doctrine-config/ edits are backed up before overwrite.
- **SC-005**: New code achieves at least 90% test coverage.

## Assumptions

- Depends on Feature 043 (DoctrineGovernancePlugin that consumes .doctrine-config/).
- The Constitution format follows spec-kitty's existing template (sections for Testing, Code Quality, Branch Strategy, etc.).
- Sync is one-way only: Constitution -> .doctrine-config/. Changes to .doctrine-config/ are overwritten on next sync.
- The generated .doctrine-config/ structure follows the Doctrine convention.
