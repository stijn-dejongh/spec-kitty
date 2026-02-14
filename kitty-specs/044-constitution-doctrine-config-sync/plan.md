# Implementation Plan: Constitution to Doctrine Config Sync

**Branch**: `044-constitution-doctrine-config-sync` | **Date**: 2026-02-15 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `kitty-specs/044-constitution-doctrine-config-sync/spec.md`

## Summary

Implement one-way sync from the Constitution (`.kittify/memory/constitution.md`) to `.doctrine-config/` (machine-parseable YAML + markdown). A `ConstitutionParser` extracts structured rules from the human-written Constitution's sections. A `DoctrineConfigGenerator` produces `.doctrine-config/config.yaml` and `.doctrine-config/repository-guidelines.md`. Sync is re-triggerable and always overwrites `.doctrine-config/` with current Constitution state (one-way, Constitution wins). Backup of existing manual `.doctrine-config/` edits before overwrite.

## Technical Context

**Language/Version**: Python 3.11+ (existing spec-kitty codebase)
**Primary Dependencies**: ruamel.yaml (YAML generation), pydantic >=2.0 (for parsed models), re (markdown parsing), pathlib, shutil (backup), logging
**Testing**: pytest (existing test infrastructure)
**Performance Goals**: Sync completes in <2s for any realistic Constitution
**Constraints**: One-way sync only; Constitution is single source of truth; output must be loadable by DoctrineGovernancePlugin (Feature 043)
**Scale/Scope**: ~6 new files, ~350-500 lines of production code, ~350-500 lines of test code

## Constitution Check

*Constitution file not present. Skipped.*

## Project Structure

### Source Code (repository root)

```
src/specify_cli/
├── governance/
│   └── sync/                              # NEW: Constitution-to-config sync
│       ├── __init__.py                    # Public API
│       ├── parser.py                      # ConstitutionParser — extracts rules from markdown
│       ├── generator.py                   # DoctrineConfigGenerator — produces .doctrine-config/
│       ├── models.py                      # ParsedConstitution, SyncReport dataclasses
│       └── cli.py                         # CLI command registration
│
├── cli/commands/
│   └── sync.py                            # NEW: `spec-kitty sync constitution` command

tests/specify_cli/
└── governance/
    └── sync/
        ├── test_parser.py                 # ConstitutionParser tests (various section formats)
        ├── test_generator.py              # DoctrineConfigGenerator output tests
        ├── test_sync_command.py           # CLI integration tests
        └── fixtures/
            ├── sample_constitution.md     # Realistic constitution input
            ├── minimal_constitution.md    # Constitution with missing sections
            └── expected_config.yaml       # Expected output for comparison
```

## Architecture

### Sync Flow

```
.kittify/memory/constitution.md (human-written)
    │
    ▼
ConstitutionParser.parse(constitution_path)
    │
    ├── Extract section: "Testing Standards"
    │       → { coverage_minimum: 80, tdd_required: true }
    │
    ├── Extract section: "Code Quality"
    │       → { commit_convention: "conventional", linting: "ruff" }
    │
    ├── Extract section: "Branch Strategy"
    │       → { strategy: "trunk-based", feature_branches: true }
    │
    ├── Extract section: "Architecture Constraints"
    │       → { patterns: ["hexagonal"], forbidden: [...] }
    │
    └── Return ParsedConstitution
            │
            ▼
DoctrineConfigGenerator.generate(parsed, output_dir)
    │
    ├── Backup existing .doctrine-config/ (if present)
    │       → .doctrine-config.bak.<timestamp>/
    │
    ├── Write .doctrine-config/config.yaml
    │       ├── precedence declaration
    │       ├── testing section
    │       ├── code_quality section
    │       ├── branch_strategy section
    │       └── architecture section
    │
    ├── Write .doctrine-config/repository-guidelines.md
    │       └── Project-specific narrative (branch strategy, etc.)
    │
    └── Return SyncReport
            ├── files_written: [...]
            ├── files_backed_up: [...]
            └── warnings: [...]
```

### Key Classes

```python
# --- models.py ---

@dataclass
class ParsedConstitution:
    """Structured rules extracted from Constitution markdown."""
    testing: dict[str, Any] | None = None
    code_quality: dict[str, Any] | None = None
    branch_strategy: dict[str, Any] | None = None
    architecture: dict[str, Any] | None = None
    governance: dict[str, Any] | None = None
    raw_sections: dict[str, str] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)

@dataclass
class SyncReport:
    """Summary of sync operation."""
    files_written: list[str]
    files_backed_up: list[str]
    warnings: list[str]
    overwritten_manual_edits: bool
```

```python
# --- parser.py ---

class ConstitutionParser:
    """Extracts structured governance rules from Constitution markdown.

    Parses sections by heading (## Testing, ## Code Quality, etc.).
    Extracts key-value pairs from bullet points and prose.
    """

    KNOWN_SECTIONS = {
        "testing": ["testing", "testing standards", "test requirements"],
        "code_quality": ["code quality", "coding standards", "style"],
        "branch_strategy": ["branch strategy", "branching", "git workflow"],
        "architecture": ["architecture", "architecture constraints", "design"],
        "governance": ["governance", "governance process", "compliance"],
    }

    def parse(self, constitution_path: Path) -> ParsedConstitution:
        """Parse constitution markdown into structured rules."""
        if not constitution_path.exists():
            raise ConstitutionNotFoundError(
                f"Constitution not found at {constitution_path}. "
                "Create one with: /spec-kitty.constitution"
            )

        content = constitution_path.read_text(encoding="utf-8")
        sections = self._split_sections(content)
        result = ParsedConstitution()

        for heading, body in sections.items():
            category = self._classify_section(heading)
            if category:
                rules = self._extract_rules(body, category)
                setattr(result, category, rules)
                result.raw_sections[category] = body
            else:
                result.warnings.append(
                    f"Unrecognized section '{heading}' — skipped. "
                    "Consider using standard headings: Testing, Code Quality, Branch Strategy, Architecture."
                )

        return result

    def _split_sections(self, content: str) -> dict[str, str]:
        """Split markdown by ## headings."""
        ...

    def _classify_section(self, heading: str) -> str | None:
        """Map heading text to a known section category."""
        heading_lower = heading.strip().lower()
        for category, aliases in self.KNOWN_SECTIONS.items():
            if any(alias in heading_lower for alias in aliases):
                return category
        return None

    def _extract_rules(self, body: str, category: str) -> dict[str, Any]:
        """Extract key-value rules from section body.

        Uses heuristics:
        - "minimum X%" → coverage_minimum: X
        - "TDD required" → tdd_required: true
        - "conventional commits" → commit_convention: "conventional"
        - Ambiguous values → reasonable default + warning
        """
        ...
```

```python
# --- generator.py ---

class DoctrineConfigGenerator:
    """Produces .doctrine-config/ directory from parsed Constitution."""

    def generate(
        self,
        parsed: ParsedConstitution,
        output_dir: Path,
        repo_root: Path,
    ) -> SyncReport:
        """Generate .doctrine-config/ from parsed constitution.

        Backs up existing directory before overwriting.
        """
        report = SyncReport(
            files_written=[], files_backed_up=[], warnings=[], overwritten_manual_edits=False
        )

        # Backup existing
        if output_dir.exists():
            self._backup(output_dir, report)

        output_dir.mkdir(parents=True, exist_ok=True)

        # Generate config.yaml
        config = self._build_config(parsed)
        config_path = output_dir / "config.yaml"
        yaml = YAML()
        yaml.default_flow_style = False
        with open(config_path, "w", encoding="utf-8") as f:
            yaml.dump(config, f)
        report.files_written.append(str(config_path))

        # Generate repository-guidelines.md
        guidelines_path = output_dir / "repository-guidelines.md"
        guidelines_content = self._build_guidelines(parsed)
        guidelines_path.write_text(guidelines_content, encoding="utf-8")
        report.files_written.append(str(guidelines_path))

        report.warnings.extend(parsed.warnings)
        return report
```

### CLI Command

New command: `spec-kitty sync constitution`

```python
# src/specify_cli/cli/commands/sync.py

app = typer.Typer(name="sync", help="Sync governance artifacts")

@app.command("constitution")
def sync_constitution() -> None:
    """Sync Constitution to .doctrine-config/ (one-way)."""
    repo_root = get_project_root_or_exit()
    constitution_path = repo_root / ".kittify" / "memory" / "constitution.md"

    parser = ConstitutionParser()
    try:
        parsed = parser.parse(constitution_path)
    except ConstitutionNotFoundError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)

    generator = DoctrineConfigGenerator()
    output_dir = repo_root / ".doctrine-config"
    report = generator.generate(parsed, output_dir, repo_root)

    # Display report
    console.print(Panel(
        f"Files written: {len(report.files_written)}\n"
        + "\n".join(f"  • {f}" for f in report.files_written)
        + (f"\n\nBackups: {len(report.files_backed_up)}" if report.files_backed_up else "")
        + (f"\n\nWarnings:\n" + "\n".join(f"  ⚠ {w}" for w in report.warnings) if report.warnings else ""),
        title="Constitution Sync Complete",
        border_style="green",
    ))
```

### Generated Config Format

The output `.doctrine-config/config.yaml` must be loadable by `DoctrineGovernancePlugin` (Feature 043):

```yaml
# Generated by spec-kitty sync constitution
# Source: .kittify/memory/constitution.md
# Do not edit — re-run `spec-kitty sync constitution` after amending Constitution.

precedence:
  source: constitution
  hierarchy: "General Guidelines > Operational Guidelines > Constitution > Directives"

testing:
  coverage_minimum: 80
  tdd_required: true

code_quality:
  commit_convention: conventional
  linting: ruff

branch_strategy:
  strategy: trunk-based
  feature_branches: true

architecture:
  patterns:
    - hexagonal
```

### Auto-trigger on Constitution Amendment (FR-008)

After the `/spec-kitty.constitution` command completes, the sync should run automatically. This is best implemented as a post-command hook in the constitution template:

Add to `src/specify_cli/missions/software-dev/command-templates/constitution.md`:
```markdown
## Post-completion Step

After writing the Constitution to `.kittify/memory/constitution.md`, run:
```
spec-kitty sync constitution
```
to regenerate `.doctrine-config/` from the updated Constitution.
```

This is a template-level hint, not a programmatic hook. A proper post-command hook can be added in a future iteration.

### Integration with Feature 043

The `DoctrineLoader` (Feature 043) reads `.doctrine-config/config.yaml`:

```python
# In DoctrineLoader.load_doctrine_config()
def load_doctrine_config(self) -> dict[str, Any]:
    config_path = self.config_path / "config.yaml"
    if not config_path.exists():
        return {}
    yaml = YAML()
    return dict(yaml.load(config_path))
```

The sync ensures this file is always valid YAML matching the expected schema.

## Risk Mitigation

| Risk | Mitigation |
|------|-----------|
| Constitution has non-standard sections | Best-effort parsing with warnings for unrecognized sections |
| Ambiguous values ("high coverage") | Map to reasonable defaults + warning suggesting explicit values |
| Manual .doctrine-config/ edits lost | Backup before overwrite with timestamped directory |
| Parser too brittle for free-form markdown | Focus on known section headings + bullet point extraction; log unknowns |
| Invalid YAML output | Test round-trip: generate → load with DoctrineGovernancePlugin |

## Dependency Chain

```
Feature 042 (GovernancePlugin ABC)
    ↓
Feature 043 (DoctrineGovernancePlugin) ← loads .doctrine-config/ output
    ↑
Feature 044 (this) ← generates .doctrine-config/ from Constitution
```

044 can be implemented in parallel with 043. Both consume/produce `.doctrine-config/` but neither depends on the other at build time — only at runtime.

## Complexity Tracking

The `ConstitutionParser._extract_rules()` method is the highest-risk component. It parses free-form markdown into structured rules. Keep it simple: match known patterns (percentages, "required"/"optional" keywords, tool names), emit warnings for anything ambiguous.
