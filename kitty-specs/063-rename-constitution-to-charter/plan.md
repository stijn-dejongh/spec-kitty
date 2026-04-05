# Implementation Plan: Rename Constitution to Charter

**Branch**: `063-rename-constitution-to-charter` | **Date**: 2026-04-05 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `kitty-specs/063-rename-constitution-to-charter/spec.md`
**Issue**: [Priivacy-ai/spec-kitty#379](https://github.com/Priivacy-ai/spec-kitty/issues/379) | **Epic**: #364

## Summary

Rename all active `constitution` references to `charter` across ~60 source files, ~49 test files, ~48 documentation files, and 3 skill files. The rename is staged: doctrine layer → core library → specify_cli module → CLI + shim → templates + skills → glossary + docs → migration + cleanup. Each stage is a standalone commit with tests green before proceeding. A CLI deprecation alias preserves backward compatibility. A user-project migration renames `.kittify/constitution/` → `.kittify/charter/`.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: typer, rich, ruamel.yaml, pathlib
**Storage**: Filesystem only (YAML, Markdown, JSONL)
**Testing**: pytest (with rtk filtering), ruff, mypy
**Target Platform**: Cross-platform CLI
**Project Type**: Single Python package (`src/specify_cli/`, `src/constitution/`, `src/doctrine/`, `src/kernel/`)
**Constraints**: Migration files, migration tests, kitty-specs archives, changelog, and legacy agent configs must NOT be renamed (C-001 through C-005)

## Constitution Check

Constitution file not present (`.kittify/constitution/constitution.md` missing). Governance context loaded from doctrine directives. Relevant directives acknowledged in spec Operational Guidelines section. No gate violations.

## Project Structure

### Documentation (this mission)

```
kitty-specs/063-rename-constitution-to-charter/
├── spec.md              # Mission specification
├── plan.md              # This file
├── research.md          # Phase 0 — codebase inventory
├── data-model.md        # Phase 1 — rename mapping
├── checklists/
│   └── requirements.md  # Spec quality checklist
└── tasks.md             # Phase 2 output (created by /spec-kitty.tasks)
```

### Source Code (affected areas)

```
src/
├── constitution/                    # → src/charter/ (14 Python files, 3,253 lines)
│   ├── __init__.py
│   ├── catalog.py
│   ├── compiler.py
│   ├── context.py
│   ├── extractor.py
│   ├── generator.py
│   ├── hasher.py
│   ├── interview.py
│   ├── parser.py
│   ├── reference_resolver.py
│   ├── resolver.py
│   ├── schemas.py
│   ├── sync.py
│   └── template_resolver.py
├── specify_cli/
│   ├── constitution/                # → specify_cli/charter/ (12 Python files, 2,928 lines)
│   ├── cli/commands/
│   │   ├── __init__.py              # CLI registration: constitution → charter
│   │   ├── constitution.py          # → charter.py (5 subcommands)
│   │   ├── shim.py                  # Shim dispatch: constitution entry
│   │   └── agent/
│   │       ├── feature.py           # create-feature → create-mission
│   │       └── workflow.py          # _render_constitution_context()
│   ├─�� dashboard/
│   │   └── constitution_path.py     # → charter_path.py
│   └── missions/
│       ├── software-dev/command-templates/constitution.md  # → charter.md
│       ├── software-dev/command-templates/{specify,plan,analyze}.md  # references
│       ├── software-dev/templates/{plan-template,task-prompt-template}.md  # references
│       ├── documentation/templates/task-prompt-template.md  # references
│       └── research/templates/task-prompt-template.md  # references
├── doctrine/
│   ├── constitution/                # → doctrine/charter/ (defaults.yaml)
│   ├── paradigms/
│   │   └── test-first.paradigm.yaml # → paradigms/shipped/ (misplaced)
│   └── skills/
│       └── spec-kitty-constitution-doctrine/  # → spec-kitty-charter-doctrine/
├── kernel/
│   └── paths.py                     # No constitution-specific functions (confirmed)
└── specify_cli/.contextive/
    └── governance.yml               # 3 glossary entries to rename

tests/
├── constitution/                    # 14 test files — rename imports + references
├── agent/
│   ├── test_workflow_constitution_context.py
│   └── cli/commands/test_constitution_cli.py
├── specify_cli/cli/commands/test_constitution_cli.py
├── test_dashboard/test_api_constitution.py
├── init/test_constitution_runtime_integration.py
├── merge/test_profile_constitution_e2e.py
└── (30+ files with scattered constitution references)

architecture/                        # 25 files referencing constitution
docs/                                # 23 files referencing constitution
```

**Structure Decision**: Existing single-package structure preserved. The rename is mechanical — no new modules, no structural changes beyond directory renames.

## Staged Rename Strategy

The rename follows the dependency graph bottom-up. Each stage is independently committable and testable.

```
Stage 1: src/doctrine/constitution/ → src/doctrine/charter/
    ↓
Stage 2: src/constitution/ → src/charter/  (core library)
    ↓
Stage 3: src/specify_cli/constitution/ → src/specify_cli/charter/  (CLI wrapper)
    ↓
Stage 4: CLI command registration + deprecation alias + shim + dashboard
    ↓
Stage 5: Templates + skills rename
    ↓
Stage 6: Glossary + architecture docs + user docs
    ↓
Stage 7: User-project migration (.kittify/constitution/ → .kittify/charter/)
    ↓
Stage 8: Cleanup — paradigm file relocation, create-feature → create-mission, test rename
```

### Stage 1 — Doctrine Layer

**Scope**: `src/doctrine/constitution/` → `src/doctrine/charter/`
**Files**: 1 (defaults.yaml)
**Tactic**: Move Field — relocate directory, update any imports referencing `doctrine.constitution`
**Verification**: `ruff check src/doctrine/` + relevant tests

### Stage 2 — Core Library

**Scope**: `src/constitution/` → `src/charter/`
**Files**: 14 Python files + README.md
**Classes to rename**: ConstitutionReference, CompiledConstitution, ConstitutionContextResult, ConstitutionDraft, ConstitutionInterview, ConstitutionSection, ConstitutionParser, ConstitutionTestingConfig, ConstitutionTemplateResolver
**Functions to rename**: build_constitution_context(), build_constitution_draft(), write_constitution(), etc.
**Tactic**: Change Function Declaration (simple mechanics — internal API, rename in place + update all call sites)
**Verification**: `pytest tests/constitution/` (after updating test imports) + `ruff check src/charter/`

### Stage 3 — Specify CLI Module

**Scope**: `src/specify_cli/constitution/` → `src/specify_cli/charter/`
**Files**: 12 Python files
**Classes to rename**: Mirror of Stage 2 classes in CLI wrapper layer
**Tactic**: Change Function Declaration (simple mechanics)
**Verification**: `pytest tests/specify_cli/` + `ruff check src/specify_cli/charter/`

### Stage 4 — CLI Registration + Deprecation Alias

**Scope**: CLI command group, shim, dashboard path resolver, agent workflow
**Files**:
- `src/specify_cli/cli/commands/constitution.py` → `charter.py`
- `src/specify_cli/cli/commands/__init__.py` — registration line
- `src/specify_cli/cli/commands/shim.py` — shim dispatch
- `src/specify_cli/dashboard/constitution_path.py` → `charter_path.py`
- `src/specify_cli/cli/commands/agent/workflow.py` — `_render_constitution_context()`
**Tactic**: Strangler Fig — register `charter` as primary, add `constitution` as deprecated alias that emits warning then delegates
**Deprecation pattern**:
```python
import warnings
@app.callback(invoke_without_command=True)
def constitution_compat():
    warnings.warn(
        "'spec-kitty constitution' is deprecated, use 'spec-kitty charter' instead.",
        DeprecationWarning, stacklevel=2
    )
```
**Verification**: `spec-kitty charter --help` works, `spec-kitty constitution --help` works + emits warning

### Stage 5 — Templates + Skills

**Scope**: Command templates, skill directory, skill content
**Files**:
- `src/specify_cli/missions/software-dev/command-templates/constitution.md` → `charter.md`
- 7 other template files with constitution references in content
- `src/doctrine/skills/spec-kitty-constitution-doctrine/` → `spec-kitty-charter-doctrine/`
- 3 skill files (SKILL.md + 2 references)
**Tactic**: Change Function Declaration (simple mechanics — rename + update references)
**Verification**: Template cleanliness tests + skill loading

### Stage 6 — Glossary + Documentation

**Scope**: Glossary entries, architecture docs, user docs
**Files**:
- `src/specify_cli/.contextive/governance.yml` — 3 glossary terms
- ~25 architecture files
- ~23 documentation files
**Tactic**: Smallest Viable Diff — text replacement in docs, no structural changes
**Verification**: Grep for stale references (NFR-001, NFR-002)

### Stage 7 — User-Project Migration

**Scope**: New upgrade migration for user projects
**Files**: 1 new migration file + 1 test file
**Behavior**: Renames `.kittify/constitution/` → `.kittify/charter/` during `spec-kitty upgrade`
**Edge case**: If both directories exist, warn and skip (don't overwrite)
**Verification**: Migration unit tests

### Stage 8 — Cleanup

**Scope**: Doctrine paradigm relocation, CLI subcommand rename, final test sweep
**Files**:
- `src/doctrine/paradigms/test-first.paradigm.yaml` → `src/doctrine/paradigms/shipped/test-first.paradigm.yaml`
- `src/specify_cli/cli/commands/agent/feature.py` — `create-feature` → `create-mission`
- Test files: rename `tests/constitution/` → `tests/charter/`, update scattered references
**Tactic**: Move Field (paradigm), Change Function Declaration (CLI subcommand)
**Verification**: Full test suite green, paradigm repository discovers test-first, `spec-kitty agent mission create-mission` works

## Parallel Work Analysis

### Dependency Graph

```
Stage 1 (doctrine) ──→ Stage 2 (core lib) ──→ Stage 3 (specify_cli) ──→ Stage 4 (CLI)
                                                                            ↓
                                                                    Stage 5 (templates/skills)
                                                                            ↓
                                                                    Stage 6 (docs)
                                                                            ↓
                                                                    Stage 7 (migration)
                                                                            ↓
                                                                    Stage 8 (cleanup)
```

Stages 1-4 are strictly sequential (import dependency chain). Stages 5-6 could theoretically parallel but the diff is cleaner sequential. Stage 7 is independent of docs but depends on Stage 4 (CLI registration). Stage 8 is final sweep.

### Work Distribution

- **Sequential core**: Stages 1–4 (must be done in order — each stage's imports depend on the previous)
- **Sequential follow-up**: Stages 5–8 (lower risk, can be reviewed independently)
- **Single agent**: This is a mechanical rename best done by one agent to avoid merge conflicts across the rename boundary

### Coordination Points

- **After Stage 4**: Full test suite must be green. This is the critical gate — if CLI works with new naming, the rest is text replacement.
- **After Stage 8**: Final acceptance grep (NFR-001, NFR-002) to confirm zero stale references.

## Complexity Tracking

No constitution check violations to justify. The rename is mechanical and does not introduce new abstractions, patterns, or architectural changes.

## Inventory Summary

| Category | Count |
|----------|-------|
| Directories to rename | 4 (+ 1 skill dir) |
| Python source files (non-test, non-migration) | ~46 |
| Test files (non-migration) | ~49 |
| Classes/types to rename | 17+ |
| CLI subcommands affected | 5 + shim + 1 agent command |
| Template files | 8 |
| Skill files | 3 |
| Glossary entries | 3 |
| Architecture docs | ~25 |
| User docs | ~23 |
| New files (migration) | 2 (migration + test) |
