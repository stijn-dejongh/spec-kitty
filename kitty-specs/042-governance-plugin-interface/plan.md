# Implementation Plan: Governance Plugin Interface

**Branch**: `042-governance-plugin-interface` | **Date**: 2026-02-15 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `kitty-specs/042-governance-plugin-interface/spec.md`

## Summary

Add a `GovernancePlugin` ABC with lifecycle hooks (`validate_pre_plan`, `validate_pre_implement`, `validate_pre_review`, `validate_pre_accept`) that return structured `ValidationResult` objects. A `NullGovernancePlugin` ensures zero overhead by default. Governance checks are advisory-only in this feature — results are displayed but never block workflow progression. A `--skip-governance` flag allows bypassing checks entirely. Governance results emit `ValidationEvent`s to the EventBridge (Feature 040).

## Technical Context

**Language/Version**: Python 3.11+ (existing spec-kitty codebase)
**Primary Dependencies**: pydantic >=2.0 (for ValidationResult), abc (for GovernancePlugin ABC), typing, dataclasses, logging
**Testing**: pytest (existing test infrastructure)
**Performance Goals**: <1ms for NullGovernancePlugin; <100ms added overhead for governance hook dispatch
**Constraints**: Zero behavioral change when no plugin configured; advisory-only (no blocking)
**Scale/Scope**: ~8 new files, ~400-500 lines of production code, ~400-500 lines of test code

## Constitution Check

*Constitution file not present. Skipped.*

## Project Structure

### Source Code (repository root)

```
src/specify_cli/
├── governance/                       # NEW: Governance plugin system
│   ├── __init__.py                   # Public API: GovernancePlugin, ValidationResult, etc.
│   ├── plugin.py                     # GovernancePlugin ABC, NullGovernancePlugin
│   ├── models.py                     # ValidationResult, ValidationStatus, GovernanceContext
│   ├── runner.py                     # GovernanceRunner — calls hooks, catches errors, emits events
│   └── factory.py                    # load_governance_plugin(repo_root) → GovernancePlugin
│
├── orchestrator/
│   └── integration.py                # MODIFIED: Insert governance hooks in process_wp()
│
└── cli/commands/
    └── orchestrate.py                # MODIFIED: Add --skip-governance flag

tests/specify_cli/
└── governance/
    ├── test_plugin.py                # GovernancePlugin ABC + NullGovernancePlugin tests
    ├── test_models.py                # ValidationResult serialization + display tests
    ├── test_runner.py                # GovernanceRunner: hook dispatch, error isolation, event emission
    └── test_factory.py               # Factory loading: config-present, absent, invalid
```

## Architecture

### Governance Flow

```
Lifecycle boundary (e.g., before implementation starts)
    │
    ▼
GovernanceRunner.run_check(phase, context)
    │
    ├── --skip-governance? → return (no-op)
    │
    ├── GovernancePlugin.validate_pre_implement(context)
    │       │
    │       ├── NullGovernancePlugin: return ValidationResult(status=pass)
    │       └── [Future: DoctrineGovernancePlugin]
    │
    ├── Catch plugin exceptions → log warning, treat as "pass"
    │
    ├── Display result (advisory only)
    │       ├── pass → silent (no output)
    │       ├── warn → console warning with reasons + suggested actions
    │       └── block → console warning (treated as warn in 042)
    │
    └── Emit ValidationEvent to EventBridge
```

### GovernancePlugin ABC

```python
from abc import ABC, abstractmethod

class GovernancePlugin(ABC):
    """Abstract base class for governance validation plugins."""

    @abstractmethod
    def validate_pre_plan(self, context: GovernanceContext) -> ValidationResult:
        """Validate before planning phase begins."""
        ...

    @abstractmethod
    def validate_pre_implement(self, context: GovernanceContext) -> ValidationResult:
        """Validate before implementation phase begins."""
        ...

    @abstractmethod
    def validate_pre_review(self, context: GovernanceContext) -> ValidationResult:
        """Validate before review phase begins."""
        ...

    @abstractmethod
    def validate_pre_accept(self, context: GovernanceContext) -> ValidationResult:
        """Validate before acceptance phase begins."""
        ...


class NullGovernancePlugin(GovernancePlugin):
    """Default: passes all checks with zero overhead."""

    def validate_pre_plan(self, context):
        return ValidationResult(status=ValidationStatus.PASS)

    def validate_pre_implement(self, context):
        return ValidationResult(status=ValidationStatus.PASS)

    def validate_pre_review(self, context):
        return ValidationResult(status=ValidationStatus.PASS)

    def validate_pre_accept(self, context):
        return ValidationResult(status=ValidationStatus.PASS)
```

### Models

```python
from enum import Enum
from pydantic import BaseModel, ConfigDict

class ValidationStatus(str, Enum):
    PASS = "pass"
    WARN = "warn"
    BLOCK = "block"

class ValidationResult(BaseModel):
    model_config = ConfigDict(frozen=True)

    status: ValidationStatus = ValidationStatus.PASS
    reasons: list[str] = []
    directive_refs: list[int] = []
    suggested_actions: list[str] = []

class GovernanceContext(BaseModel):
    """Context passed to governance hooks.

    Provides the plugin with enough information to make a validation decision
    without needing to read files itself.
    """
    model_config = ConfigDict(frozen=True)

    phase: str                              # plan | implement | review | accept
    feature_slug: str
    work_package_id: str | None = None      # None for pre_plan (feature-level)
    tool_id: str | None = None              # Which tool runs this (e.g., "claude", "opencode")
    agent_profile_id: str | None = None     # Doctrine agent profile (e.g., "python-pedro")
    agent_role: str | None = None           # Role: "implementer", "reviewer", etc.
    spec_content: str | None = None         # Spec markdown (for pre_plan)
    task_content: str | None = None         # WP markdown (for pre_implement)
    review_comments: str | None = None      # Review output (for pre_accept)
    constitution_path: Path | None = None   # Path to constitution.md if present
    repo_root: Path | None = None           # Repo root for plugin file access
```

### GovernanceRunner

The `GovernanceRunner` orchestrates hook dispatch with error isolation and event emission:

```python
class GovernanceRunner:
    """Executes governance checks with error isolation and telemetry."""

    def __init__(
        self,
        plugin: GovernancePlugin,
        event_bridge: EventBridge | None = None,
        console: Console | None = None,
    ):
        self.plugin = plugin
        self.event_bridge = event_bridge or NullEventBridge()
        self.console = console or Console()

    def run_check(self, phase: str, context: GovernanceContext) -> ValidationResult:
        """Run a governance check for the given phase.

        Catches plugin exceptions, logs warnings, emits events.
        Returns ValidationResult (never raises).
        """
        hook = getattr(self.plugin, f"validate_pre_{phase}", None)
        if hook is None:
            return ValidationResult(status=ValidationStatus.PASS)

        try:
            result = hook(context)
        except Exception as e:
            logger.warning(f"Governance plugin error during pre_{phase}: {e}")
            result = ValidationResult(status=ValidationStatus.PASS)

        # Display advisory result
        self._display_result(phase, result)

        # Emit event
        self.event_bridge.emit_validation_event(ValidationEvent(
            timestamp=datetime.now(timezone.utc),
            validation_type=f"pre_{phase}",
            status=result.status.value,
            directive_refs=result.directive_refs,
            duration_ms=0,  # Simple timing can be added later
        ))

        return result

    def _display_result(self, phase: str, result: ValidationResult) -> None:
        if result.status == ValidationStatus.PASS:
            return  # Silent pass
        label = "[yellow]Advisory[/yellow]" if result.status == ValidationStatus.WARN else "[red]Advisory (block deferred)[/red]"
        self.console.print(f"\n{label} — governance check for [bold]{phase}[/bold]:")
        for reason in result.reasons:
            self.console.print(f"  • {reason}")
        for action in result.suggested_actions:
            self.console.print(f"  → {action}")
```

### Factory

```python
def load_governance_plugin(repo_root: Path) -> GovernancePlugin:
    """Load governance plugin from .kittify/config.yaml.

    Returns NullGovernancePlugin if not configured or on any error.
    """
    config_path = repo_root / ".kittify" / "config.yaml"
    if not config_path.exists():
        return NullGovernancePlugin()

    yaml = YAML()
    try:
        data = yaml.load(config_path)
        governance = data.get("governance", {})
        provider = governance.get("provider")
    except Exception:
        logger.warning("Failed to load governance config, using NullGovernancePlugin")
        return NullGovernancePlugin()

    if provider == "doctrine":
        # Feature 043 will register this
        try:
            from specify_cli.governance.doctrine import DoctrineGovernancePlugin
            return DoctrineGovernancePlugin(repo_root)
        except ImportError:
            logger.warning("Doctrine governance provider not available")
            return NullGovernancePlugin()

    return NullGovernancePlugin()
```

### Config Schema Extension

Addition to `.kittify/config.yaml`:

```yaml
governance:
  provider: null       # null (default) | "doctrine" (Feature 043)
  skip: false          # Equivalent to --skip-governance on every command
```

### Integration Points (Modified Files)

**`src/specify_cli/orchestrator/integration.py`** — `process_wp()`:

Insert governance hooks at two natural boundaries in `process_wp()` (line 806 and 849):

```python
# Before implementation (line ~806, after tool selection, before throttle):
if governance_runner:
    gov_context = GovernanceContext(
        phase="implement",
        feature_slug=state.feature_slug,
        work_package_id=wp_id,
        tool_id=impl_tool,           # Which tool is assigned (e.g., "claude")
        agent_role="implementer",
    )
    governance_runner.run_check("implement", gov_context)

# Before review (line ~849, before review tool selection):
if governance_runner:
    gov_context = GovernanceContext(
        phase="review",
        feature_slug=state.feature_slug,
        work_package_id=wp_id,
        tool_id=review_tool,         # Which tool is assigned
        agent_role="reviewer",
    )
    governance_runner.run_check("review", gov_context)
```

Thread `governance_runner: GovernanceRunner | None = None` through `run_orchestration_loop()` → `process_wp()`.

**`src/specify_cli/cli/commands/orchestrate.py`** — `orchestrate()` callback:

Add `--skip-governance` option:
```python
skip_governance: bool = typer.Option(
    False,
    "--skip-governance",
    help="Skip all governance checks",
),
```

In `start_orchestration_async()`, after config loading:
```python
if not skip_governance:
    plugin = load_governance_plugin(repo_root)
    governance_runner = GovernanceRunner(plugin, event_bridge, console)
else:
    governance_runner = None
```

Pass `governance_runner` to `run_orchestration_loop()`.

## Risk Mitigation

| Risk | Mitigation |
|------|-----------|
| Plugin exception crashes orchestrator | GovernanceRunner catches all exceptions, logs warning, returns "pass" |
| Governance slows down orchestration | NullGovernancePlugin is a no-op; real plugins run once per phase boundary |
| Breaking existing tests | NullGovernancePlugin is default; no governance code runs unless configured |
| GovernanceContext too coupled to internals | Context is a Pydantic model with simple fields, not raw internal objects |
| "block" results confuse users in advisory mode | Display clearly labels as "Advisory (block deferred)" |

## Complexity Tracking

No unnecessary complexity. The runner pattern cleanly separates concerns: the plugin decides, the runner dispatches, the orchestrator calls at boundaries.
