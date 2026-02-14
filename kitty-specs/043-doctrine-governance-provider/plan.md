# Implementation Plan: Doctrine Governance Provider

**Branch**: `043-doctrine-governance-provider` | **Date**: 2026-02-15 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `kitty-specs/043-doctrine-governance-provider/spec.md`

## Summary

Implement `DoctrineGovernancePlugin` — a concrete `GovernancePlugin` (Feature 042) that loads Agentic Doctrine artifacts from a `doctrine/` subtree at the project root, evaluates relevant directives against lifecycle state, and resolves precedence between guidelines, constitution, and directives. Supports opt-in blocking mode via `--enforce-governance`. Falls back to `NullGovernancePlugin` when no `doctrine/` directory is present.

## Technical Context

**Language/Version**: Python 3.11+ (existing spec-kitty codebase)
**Primary Dependencies**: pydantic >=2.0, ruamel.yaml (YAML parsing), pathlib, logging, re (markdown parsing)
**Testing**: pytest (existing test infrastructure)
**Performance Goals**: <500ms per governance check; <6K tokens of directive context loaded per phase
**Constraints**: Must implement GovernancePlugin ABC from Feature 042; zero impact when doctrine/ absent
**Scale/Scope**: ~10 new files, ~600-800 lines of production code, ~500-700 lines of test code

## Constitution Check

*Constitution file not present. Skipped.*

## Project Structure

### Source Code (repository root)

```
src/specify_cli/
├── governance/                            # Extends governance/ from Feature 042
│   ├── __init__.py                        # MODIFIED: Export DoctrineGovernancePlugin
│   ├── doctrine/                          # NEW: Doctrine-specific governance
│   │   ├── __init__.py                    # Public API
│   │   ├── plugin.py                      # DoctrineGovernancePlugin implementation
│   │   ├── loader.py                      # DoctrineLoader — reads doctrine/ tree
│   │   ├── evaluator.py                   # DirectiveEvaluator — evaluates directives
│   │   ├── precedence.py                  # PrecedenceResolver — resolves conflicts
│   │   └── models.py                      # Directive, Guideline, DoctrineConfig dataclasses
│   └── factory.py                         # MODIFIED: Wire "doctrine" provider lookup
│
├── cli/commands/
│   └── orchestrate.py                     # MODIFIED: Add --enforce-governance flag

tests/specify_cli/
└── governance/
    └── doctrine/
        ├── test_plugin.py                 # DoctrineGovernancePlugin integration tests
        ├── test_loader.py                 # DoctrineLoader parsing tests
        ├── test_evaluator.py              # DirectiveEvaluator evaluation tests
        ├── test_precedence.py             # PrecedenceResolver conflict tests
        ├── test_agent_profiles.py         # Agent profile loading + capability validation tests
        └── fixtures/                      # Test doctrine/ trees
            ├── minimal/                   # Minimal doctrine with 1 directive
            ├── full/                      # Full doctrine with guidelines + directives + agents
            ├── constitution_override/     # Constitution narrowing a directive
            └── agent_profiles/            # Agent profiles with capability mismatches
```

## Architecture

### Doctrine Directory Structure (Expected Input)

```
doctrine/                            # Git subtree at project root
├── guidelines/
│   ├── general/                     # General Guidelines (highest precedence)
│   │   └── *.md
│   └── operational/                 # Operational Guidelines
│       └── *.md
├── directives/
│   ├── 017-tdd-required.md          # Individual directives with front matter
│   ├── 023-conventional-commits.md
│   └── ...
├── agents/                          # Agent profiles (role identity + capabilities)
│   ├── implementer.agent.md         # Agent profile with front matter
│   ├── reviewer.agent.md
│   └── ...
├── approaches/                      # Tactical approaches (lowest precedence)
│   └── *.md
└── README.md

.doctrine-config/                    # Project-level overrides (Feature 044)
├── config.yaml                      # Structured overrides
└── repository-guidelines.md         # Project-specific narrative

.kittify/memory/constitution.md      # Constitution (narrows directives)
```

### Governance Flow

```
DoctrineGovernancePlugin.validate_pre_implement(context)
    │
    ├── DoctrineLoader.load(phase="implement")
    │       │
    │       ├── Scan doctrine/directives/ for files with phase tag "implement"
    │       ├── Parse front matter: directive_number, title, phase_tags, severity
    │       ├── Lazy: skip directives not tagged for current phase
    │       └── Return list[Directive]
    │
    ├── DoctrineLoader.load_agent_profiles()
    │       │
    │       ├── Scan doctrine/agents/*.agent.md
    │       ├── Parse front matter: id, specialization, capabilities, required_directives
    │       ├── Match assigned agent (from context) to profile by agent key
    │       └── Return AgentProfile | None
    │
    ├── Load overrides
    │       ├── .doctrine-config/config.yaml (structured overrides)
    │       └── .kittify/memory/constitution.md (narrative overrides)
    │
    ├── PrecedenceResolver.resolve(directives, guidelines, constitution)
    │       │
    │       ├── Hierarchy: General Guidelines > Operational > Constitution > Directives
    │       ├── Constitution can narrow directive thresholds (e.g., 80% → 60%)
    │       ├── Detect contradictions: Constitution vs Guidelines → warn
    │       └── Return resolved list[ResolvedDirective]
    │
    ├── Agent profile validation (if profile loaded)
    │       │
    │       ├── Filter resolved directives to profile's required_directives
    │       ├── Check agent capabilities match task requirements
    │       └── Warn if assigned agent lacks required capabilities
    │
    └── DirectiveEvaluator.evaluate(resolved_directives, context, agent_profile)
            │
            ├── For each directive: check rule against context
            ├── If agent profile: also validate capability fit
            ├── Aggregate: any "block" → block, any "warn" → warn, else pass
            └── Return ValidationResult with directive_refs
```

### Key Classes

```python
# --- models.py ---

@dataclass
class Directive:
    """A single parsed directive from doctrine/directives/."""
    number: int
    title: str
    content: str
    phase_tags: list[str]          # ["plan", "implement", "review"]
    severity: str                   # "advisory" | "required"
    rules: dict[str, Any]          # Structured rules extracted from content
    source_path: Path

@dataclass
class Guideline:
    """A parsed guideline from doctrine/guidelines/."""
    title: str
    content: str
    level: str                      # "general" | "operational"
    rules: dict[str, Any]
    source_path: Path

@dataclass
class AgentProfile:
    """A parsed agent profile from doctrine/agents/."""
    id: str                             # e.g., "implementer", "reviewer"
    name: str                           # Human-readable name
    specialization: str                 # e.g., "architect", "implementer", "reviewer"
    capabilities: frozenset[str]        # e.g., {"write-tests", "design-apis", "refactor"}
    required_directives: list[int]      # Directive numbers this agent must follow
    handoff_patterns: dict[str, str]    # Direction → target agent (loaded for future routing)
    primer_matrix: dict[str, list[str]] # Task type → required context primers
    source_path: Path

@dataclass
class ResolvedDirective:
    """A directive with overrides applied via precedence resolution."""
    directive: Directive
    effective_rules: dict[str, Any]   # After constitution/guideline overrides
    override_source: str | None       # "constitution" | "guideline" | None
    warnings: list[str]               # Contradiction warnings
```

```python
# --- loader.py ---

class DoctrineLoader:
    """Reads doctrine/ tree and returns structured artifacts."""

    def __init__(self, repo_root: Path):
        self.doctrine_path = repo_root / "doctrine"
        self.config_path = repo_root / ".doctrine-config"
        self.constitution_path = repo_root / ".kittify" / "memory" / "constitution.md"

    def is_available(self) -> bool:
        """Check if doctrine/ directory exists."""
        return self.doctrine_path.is_dir()

    def load_directives(self, phase: str) -> list[Directive]:
        """Load only directives tagged for the given phase (lazy loading)."""
        ...

    def load_guidelines(self) -> tuple[list[Guideline], list[Guideline]]:
        """Load general and operational guidelines."""
        ...

    def load_constitution_overrides(self) -> dict[str, Any]:
        """Parse constitution.md for structured overrides."""
        ...

    def load_doctrine_config(self) -> dict[str, Any]:
        """Load .doctrine-config/config.yaml overrides."""
        ...

    def load_agent_profiles(self) -> list[AgentProfile]:
        """Load all agent profiles from doctrine/agents/*.agent.md."""
        ...

    def get_agent_profile(self, agent_key: str) -> AgentProfile | None:
        """Find the agent profile matching a spec-kitty agent key.

        Maps SK agent keys (e.g., "claude") to doctrine profile IDs
        (e.g., "implementer") via specialization or explicit mapping
        in .doctrine-config/config.yaml.
        """
        ...
```

```python
# --- plugin.py ---

class DoctrineGovernancePlugin(GovernancePlugin):
    """Concrete governance plugin backed by Agentic Doctrine artifacts."""

    def __init__(self, repo_root: Path):
        self.loader = DoctrineLoader(repo_root)
        self.resolver = PrecedenceResolver()
        self.evaluator = DirectiveEvaluator()

        if not self.loader.is_available():
            # Degrade to NullGovernancePlugin behavior
            self._null_mode = True
        else:
            self._null_mode = False

    def validate_pre_implement(self, context: GovernanceContext) -> ValidationResult:
        if self._null_mode:
            return ValidationResult(status=ValidationStatus.PASS)

        directives = self.loader.load_directives(phase="implement")
        guidelines = self.loader.load_guidelines()
        overrides = self.loader.load_constitution_overrides()

        # Load agent profile for the assigned agent (if available)
        agent_profile = None
        if context.agent_key:
            agent_profile = self.loader.get_agent_profile(context.agent_key)

        resolved = self.resolver.resolve(directives, guidelines, overrides)

        # If agent profile loaded, filter to profile's required_directives
        if agent_profile:
            resolved = [
                r for r in resolved
                if r.directive.number in agent_profile.required_directives
            ] or resolved  # Fall back to all if profile has no directive filter

        return self.evaluator.evaluate(resolved, context, agent_profile)

    # Similar pattern for validate_pre_plan, validate_pre_review, validate_pre_accept
```

### --enforce-governance Flag

Added to `orchestrate.py` alongside the existing `--skip-governance` from Feature 042:

```python
enforce_governance: bool = typer.Option(
    False,
    "--enforce-governance",
    help="Make 'block' governance results halt the workflow with non-zero exit",
),
```

**Enforcement logic** — modify `GovernanceRunner.run_check()` (from 042):

```python
def run_check(self, phase: str, context: GovernanceContext, enforce: bool = False) -> ValidationResult:
    ...
    result = hook(context)

    # In enforce mode, "block" results raise
    if enforce and result.status == ValidationStatus.BLOCK:
        self._display_result(phase, result, blocking=True)
        raise GovernanceBlockError(
            f"Governance blocked {phase}: {'; '.join(result.reasons)}"
        )

    # Otherwise advisory
    self._display_result(phase, result)
    return result
```

The orchestrator catches `GovernanceBlockError` and exits with non-zero status.

**Precedence**: `--skip-governance` beats `--enforce-governance` (skip wins).

### Directive Front Matter Format

Directives in `doctrine/directives/` are expected to have YAML front matter:

```markdown
---
directive_number: 17
title: TDD Required
phase_tags: [implement, review]
severity: required
rules:
  test_coverage_minimum: 80
  tdd_approach: true
---

# Directive 017: TDD Required

All implementation work packages must include tests...
```

### Agent Profile Front Matter Format

Agent profiles in `doctrine/agents/` have YAML front matter defining role identity:

```markdown
---
id: implementer
name: Implementation Specialist
specialization: implementer
capabilities:
  - write-code
  - write-tests
  - refactor
  - debug
required_directives: [17, 23, 31]
handoff_patterns:
  after_implement: reviewer
  on_rejection: implementer
primer_matrix:
  implement: [spec, plan, architecture]
  fix: [spec, review-comments, test-output]
---

# Implementation Specialist

This agent handles all code implementation tasks...
```

**Agent key mapping**: SK uses flat keys like `"claude"`, `"opencode"`. The mapping from SK key to doctrine profile is configured in `.doctrine-config/config.yaml`:

```yaml
agent_profiles:
  claude: implementer       # claude uses the "implementer" profile
  opencode: reviewer        # opencode uses the "reviewer" profile
```

If no explicit mapping exists, the loader attempts to match by checking if the SK agent key appears in the profile's `id` or `name` field. If no profile matches, governance proceeds without profile-specific filtering (all directives apply).

### Lazy Loading Strategy

Only directives tagged for the current phase are loaded. For a typical Doctrine tree with 20 directives:

| Phase | Typical tags | Loaded count |
|-------|-------------|-------------|
| plan | plan | 3-5 directives |
| implement | implement | 5-8 directives |
| review | review | 4-6 directives |
| accept | accept | 2-3 directives |

This keeps context overhead under 6K tokens per phase (SC-003).

### Config Schema Extension

Extension to `.kittify/config.yaml` (builds on 042's `governance:` section):

```yaml
governance:
  provider: doctrine          # Activates DoctrineGovernancePlugin
  enforce: false              # Default: advisory. Set to true for blocking mode.
  doctrine_path: doctrine/    # Override doctrine subtree location (rare)
```

### Integration Points (Modified Files)

**`src/specify_cli/governance/factory.py`** — Wire doctrine provider:
```python
if provider == "doctrine":
    from specify_cli.governance.doctrine import DoctrineGovernancePlugin
    return DoctrineGovernancePlugin(repo_root)
```

**`src/specify_cli/cli/commands/orchestrate.py`** — Add `--enforce-governance` flag. Thread `enforce` bool to `GovernanceRunner`.

**`src/specify_cli/governance/runner.py`** — Add `enforce` parameter to `run_check()`. Raise `GovernanceBlockError` on block+enforce.

## Risk Mitigation

| Risk | Mitigation |
|------|-----------|
| Malformed directive files | Skip with warning, continue with remaining directives |
| Missing doctrine/ directory | _null_mode flag degrades to NullGovernancePlugin |
| Constitution contradicts guidelines | PrecedenceResolver detects and emits warnings |
| Directive evaluation is ambiguous | Default to "pass" — governance should not block on uncertainty |
| Performance: loading too many directives | Lazy loading by phase tags; target <6K tokens |
| doctrine/ subtree out of date | Informational version check only; do not block on old versions |

## Dependency Chain

```
Feature 040 (EventBridge) ← Feature 042 (GovernancePlugin ABC) ← Feature 043 (this)
                                                                 ↙
Feature 044 (Constitution sync) ← generates .doctrine-config/ used here
```

043 can be implemented before 044 — it loads `.doctrine-config/` if present but works without it.

## Complexity Tracking

The PrecedenceResolver is the most complex component. It follows a clear hierarchy rule (General > Operational > Constitution > Directives) and should not attempt deep semantic analysis — it compares structured `rules` dicts by key overlap. Ambiguity → pass.
