# Research: Agent Profile Domain Model

**Feature**: 047-agent-profile-domain-model
**Date**: 2026-02-21 (revised from 2026-02-16)

## Decision 1 (REVISED): Modeling Approach — Pydantic

**Decision**: Use Pydantic `BaseModel` for `AgentProfile` and all value objects in `src/doctrine/model/profile.py`.

**Rationale**: The existing `AgentProfile` in `specify_cli.constitution.schemas` already uses Pydantic. The rich model benefits from Pydantic's built-in validation, serialization, JSON Schema generation, and YAML round-trip support. Manual `to_dict()`/`from_dict()` boilerplate is eliminated. The `doctrine` package's zero-import constraint on `specify_cli` is unaffected — Pydantic is an independent dependency.

**Alternatives considered**:

- Frozen dataclasses with manual serialization — original decision; consistent with status model but adds boilerplate and loses validation
- Hybrid (Pydantic for complex types, dataclasses for simple) — creates confusion about which pattern to use

**Migration path**: The shallow `AgentProfile` in `src/specify_cli/constitution/schemas.py` is removed. The rich model in `src/doctrine/model/profile.py` becomes the single definition. `specify_cli.constitution.resolver` imports from `doctrine.model`.

## Decision 2: Package Distribution — Single Distribution

**Decision**: `src/doctrine/` is a subpackage within the `spec-kitty-cli` PyPI distribution. Add `"src/doctrine"` to `pyproject.toml` `[tool.hatch.build.targets.wheel] packages` list.

**Rationale**: Simplest distribution model during alpha. The zero-import boundary between `doctrine` and `specify_cli` is enforced by a CI test (AST-level import scan), not by package isolation. This provides the architectural benefit (loose coupling) without the operational cost (separate PyPI package, separate versioning, dependency edge).

**Alternatives considered**:

- Separate PyPI package `spec-kitty-doctrine` — true isolation but adds release complexity; no external consumers justify the overhead yet
- Namespace package within `specify_cli` (e.g., `specify_cli.doctrine`) — violates the conceptual separation; doctrine should not be "under" the CLI

**Implementation note**: `pyproject.toml` change:

```toml
[tool.hatch.build.targets.wheel]
packages = ["src/specify_cli", "src/doctrine"]
```

## Decision 3: ToolConfig Rename Strategy — Alias-First

**Decision**: Create `tool_config.py` with new names, replace `agent_config.py` with a deprecated alias module, then iteratively update all importing files with tests passing at each step.

**Rationale**: Alias-first approach ensures backward compatibility at every step. No single commit breaks imports. The alias module can be removed in a future version.

**Files requiring import updates** (verify against current codebase before implementation):

1. `src/specify_cli/agent_utils/directories.py`
2. `src/specify_cli/orchestrator/scheduler.py`
3. `src/specify_cli/upgrade/migrations/m_0_14_0_centralized_feature_detection.py`
4. `src/specify_cli/cli/commands/init.py`
5. `src/specify_cli/cli/commands/agent/config.py`
6. `src/specify_cli/orchestrator/monitor.py`
7. `src/specify_cli/orchestrator/config.py`

## Decision 4: Shipped Profile Format — Pure YAML

**Decision**: Shipped profiles use `.agent.yaml` format (pure structured YAML), stored in `src/doctrine/agent-profiles/`.

**Rationale**: Machine-parseable structured data for the repository loader, hierarchy builder, and schema validator. YAML avoids Markdown frontmatter parsing complexity.

**Curation source format**: External profiles in `.agent.md` format (like Python Pedro) enter through the curation pipeline and are adapted to `.agent.yaml` during the import flow. The `.agent.md` is the curation input; `.agent.yaml` is the doctrine output.

## Decision 5: `importlib.resources` for Shipped Profiles

**Decision**: Use `importlib.resources` (Python 3.11+) to locate shipped profile YAML files within the installed package.

**Implementation pattern**:

```python
from importlib.resources import files

def _shipped_profiles_dir() -> Path:
    return files("doctrine.agent_profiles") / "shipped"
```

## Decision 6: Custom Role Support

**Decision**: The `role` field accepts both `Role` enum values and arbitrary strings. The enum provides the controlled vocabulary; custom strings allow extension.

**Implementation approach**: Pydantic validator parses the role field. If it matches a known `Role` enum value, convert it. Otherwise, keep as string. Validation warns on unknown roles but does not reject them.

## Decision 7: Curation Flow as Acceptance Path

**Decision**: New agent profiles enter the system through the curation pipeline (`src/doctrine/curation/`). The `agent-profile` is a valid `target_type` for `ImportCandidate`.

**Rationale**: The curation flow is the governed path for adding new doctrine artifacts. Making agent profiles a first-class curation target validates that the pipeline is lean, efficient, and extensible. The manual acceptance test (importing Python Pedro via curation) validates the full end-to-end flow without shipping an incomplete profile as a reference default.

**Process**: Candidate creation → classification (`target_type: agent-profile`) → adaptation (`.agent.md` to `.agent.yaml`) → schema validation → adoption → `resulting_artifacts` linkage.

## Decision 8: Code Style

**Decision**: All Python code follows `src/doctrine/styleguides/python-implementation.styleguide.yaml`.

**Key principles**:
- Explicit typing for public functions
- Focused functions with minimal side effects
- Clear names over abbreviated names
