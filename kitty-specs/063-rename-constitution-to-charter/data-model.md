# Data Model: Rename Mapping

## Directory Renames

| Current Path | New Path | File Count |
|-------------|----------|------------|
| `src/doctrine/constitution/` | `src/doctrine/charter/` | 1 |
| `src/constitution/` | `src/charter/` | 15 |
| `src/specify_cli/constitution/` | `src/specify_cli/charter/` | 12 |
| `src/specify_cli/dashboard/constitution_path.py` | `src/specify_cli/dashboard/charter_path.py` | 1 |
| `src/specify_cli/cli/commands/constitution.py` | `src/specify_cli/cli/commands/charter.py` | 1 |
| `src/doctrine/skills/spec-kitty-constitution-doctrine/` | `src/doctrine/skills/spec-kitty-charter-doctrine/` | 3 |
| `src/specify_cli/missions/software-dev/command-templates/constitution.md` | `…/charter.md` | 1 |
| `tests/constitution/` | `tests/charter/` | 14 |

## Class/Type Renames

| Current Name | New Name | File(s) |
|-------------|----------|---------|
| `CompiledConstitution` | `CompiledCharter` | `src/constitution/compiler.py`, `src/specify_cli/constitution/compiler.py` |
| `ConstitutionReference` | `CharterReference` | `src/constitution/compiler.py`, `src/specify_cli/constitution/compiler.py` |
| `ConstitutionContextResult` | `CharterContextResult` | `src/constitution/context.py`, `src/specify_cli/constitution/context.py` |
| `ConstitutionDraft` | `CharterDraft` | `src/constitution/generator.py`, `src/specify_cli/constitution/generator.py` |
| `ConstitutionInterview` | `CharterInterview` | `src/constitution/interview.py`, `src/specify_cli/constitution/interview.py` |
| `ConstitutionSection` | `CharterSection` | `src/constitution/parser.py`, `src/specify_cli/constitution/parser.py` |
| `ConstitutionParser` | `CharterParser` | `src/constitution/parser.py`, `src/specify_cli/constitution/parser.py` |
| `ConstitutionTestingConfig` | `CharterTestingConfig` | `src/constitution/schemas.py`, `src/specify_cli/constitution/schemas.py` |
| `ConstitutionTemplateResolver` | `CharterTemplateResolver` | `src/constitution/template_resolver.py` |

## Function Renames

| Current Name | New Name | File |
|-------------|----------|------|
| `resolve_project_constitution_path()` | `resolve_project_charter_path()` | `src/specify_cli/dashboard/constitution_path.py` |
| `_resolve_constitution_path()` | `_resolve_charter_path()` | `src/specify_cli/cli/commands/constitution.py` |
| `_render_constitution_context()` | `_render_charter_context()` | `src/specify_cli/cli/commands/agent/workflow.py` |
| `build_constitution_context()` | `build_charter_context()` | `src/constitution/context.py` |
| `build_constitution_draft()` | `build_charter_draft()` | `src/constitution/generator.py` |
| `write_constitution()` | `write_charter()` | `src/constitution/generator.py` |
| `sync_constitution()` | `sync_charter()` | `src/constitution/sync.py` |

## CLI Command Renames

| Current Command | New Command | Deprecation |
|----------------|-------------|-------------|
| `spec-kitty constitution` | `spec-kitty charter` | Alias with warning |
| `spec-kitty constitution interview` | `spec-kitty charter interview` | Via parent alias |
| `spec-kitty constitution generate` | `spec-kitty charter generate` | Via parent alias |
| `spec-kitty constitution context` | `spec-kitty charter context` | Via parent alias |
| `spec-kitty constitution sync` | `spec-kitty charter sync` | Via parent alias |
| `spec-kitty constitution status` | `spec-kitty charter status` | Via parent alias |
| `spec-kitty agent mission create-feature` | `spec-kitty agent mission create-mission` | No alias |

## Glossary Term Renames

| Current Term | New Term | File |
|-------------|----------|------|
| Constitution Compiler | Charter Compiler | `src/specify_cli/.contextive/governance.yml` |
| Constitution Interview | Charter Interview | `src/specify_cli/.contextive/governance.yml` |
| Constitution Validation | Charter Validation | `src/specify_cli/.contextive/governance.yml` |

## Filesystem Path Renames (User Projects)

| Current Path | New Path | Migration |
|-------------|----------|-----------|
| `.kittify/constitution/` | `.kittify/charter/` | New upgrade migration |
| `.kittify/constitution/constitution.md` | `.kittify/charter/charter.md` | Part of directory rename |
| `.kittify/constitution/interview/answers.yaml` | `.kittify/charter/interview/answers.yaml` | Part of directory rename |
| `.kittify/memory/constitution.md` | N/A | Legacy path, already handled by existing migration |

## File Relocations (Non-Rename)

| Current Path | New Path | Reason |
|-------------|----------|--------|
| `src/doctrine/paradigms/test-first.paradigm.yaml` | `src/doctrine/paradigms/shipped/test-first.paradigm.yaml` | Misplaced — not discoverable by paradigm repository |

## Exclusions (Must NOT Rename)

| Path Pattern | Reason |
|-------------|--------|
| `src/specify_cli/upgrade/migrations/m_*_constitution_*.py` | Historical migration files |
| `tests/**/test_migration_*.py` referencing constitution migrations | Test migration behavior |
| `kitty-specs/*/` (all existing features) | Historical archives |
| `CHANGELOG.md` | Historical record |
| `.cursor/`, `.codex/`, `.amazonq/`, etc. | Legacy agent config copies |
