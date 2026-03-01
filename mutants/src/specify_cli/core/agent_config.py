"""Agent configuration (canonical location in core).

This module manages agent configuration that is set during `spec-kitty init`
and used by commands and migrations to select agents for implementation and review.

The configuration is stored in .kittify/config.yaml under the `agents` key.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from ruamel.yaml import YAML

from specify_cli.core.config import AI_CHOICES

import logging

logger = logging.getLogger(__name__)
from typing import Annotated
from typing import Callable
from typing import ClassVar

MutantDict = Annotated[dict[str, Callable], "Mutant"] # type: ignore


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None): # type: ignore
    """Forward call to original or mutated function, depending on the environment"""
    import os # type: ignore
    mutant_under_test = os.environ['MUTANT_UNDER_TEST'] # type: ignore
    if mutant_under_test == 'fail': # type: ignore
        from mutmut.__main__ import MutmutProgrammaticFailException # type: ignore
        raise MutmutProgrammaticFailException('Failed programmatically')       # type: ignore
    elif mutant_under_test == 'stats': # type: ignore
        from mutmut.__main__ import record_trampoline_hit # type: ignore
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__) # type: ignore
        # (for class methods, orig is bound and thus does not need the explicit self argument)
        result = orig(*call_args, **call_kwargs) # type: ignore
        return result # type: ignore
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_' # type: ignore
    if not mutant_under_test.startswith(prefix): # type: ignore
        result = orig(*call_args, **call_kwargs) # type: ignore
        return result # type: ignore
    mutant_name = mutant_under_test.rpartition('.')[-1] # type: ignore
    if self_arg is not None: # type: ignore
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs) # type: ignore
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs) # type: ignore
    return result # type: ignore


class AgentConfigError(RuntimeError):
    """Raised when .kittify/config.yaml cannot be parsed or validated."""


@dataclass
class AgentSelectionConfig:
    """Configuration for preferred role assignment.

    Attributes:
        preferred_implementer: Agent ID to prefer for implementation tasks.
        preferred_reviewer: Agent ID to prefer for review tasks.
    """

    preferred_implementer: str | None = None
    preferred_reviewer: str | None = None


@dataclass
class AgentConfig:
    """Full agent configuration.

    Attributes:
        available: List of agent IDs that are available for use
        selection: Configuration for how to select agents
    """

    available: list[str] = field(default_factory=list)
    selection: AgentSelectionConfig = field(default_factory=AgentSelectionConfig)

    def select_implementer(self, exclude: str | None = None) -> str | None:
        """Select an agent for implementation.

        Args:
            exclude: Optional agent ID to exclude from selection

        Returns:
            Selected agent ID or None if no agents available
        """
        candidates = [a for a in self.available if a != exclude]
        if not candidates:
            return None

        if self.selection.preferred_implementer in candidates:
            return self.selection.preferred_implementer
        # Fall back to first available
        return candidates[0]

    def select_reviewer(self, implementer: str | None = None) -> str | None:
        """Select an agent for review.

        Prefers a different agent than the implementer for cross-review.

        Args:
            implementer: Agent that did implementation (prefer different agent)

        Returns:
            Selected agent ID or None if no agents available
        """
        # Prefer different agent for cross-review
        candidates = [a for a in self.available if a != implementer]

        # Fall back to same agent if no other available
        if not candidates:
            candidates = self.available.copy()

        if not candidates:
            return None

        if self.selection.preferred_reviewer in candidates:
            return self.selection.preferred_reviewer
        # Fall back to first available that's not the implementer
        return candidates[0]


def load_agent_config(repo_root: Path) -> AgentConfig:
    args = [repo_root]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_load_agent_config__mutmut_orig, x_load_agent_config__mutmut_mutants, args, kwargs, None)


def x_load_agent_config__mutmut_orig(repo_root: Path) -> AgentConfig:
    """Load agent configuration from .kittify/config.yaml.

    Args:
        repo_root: Repository root directory

    Returns:
        AgentConfig instance (defaults if not configured)
    """
    config_file = repo_root / ".kittify" / "config.yaml"

    if not config_file.exists():
        logger.warning(f"Config file not found: {config_file}")
        return AgentConfig()

    yaml = YAML()
    yaml.preserve_quotes = True

    try:
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        raise AgentConfigError(
            f"Invalid YAML in {config_file}: {e}"
        ) from e

    agents_data = data.get("agents", {})
    if not agents_data:
        logger.info("No agents section in config.yaml")
        return AgentConfig()

    # Parse available agents
    available = agents_data.get("available", [])
    if isinstance(available, str):
        available = [available]
    if not isinstance(available, list):
        raise AgentConfigError(
            "Invalid agents.available in config.yaml: expected a list of agent keys"
        )

    invalid_agents = [agent for agent in available if agent not in AI_CHOICES]
    if invalid_agents:
        valid_agents = ", ".join(sorted(AI_CHOICES.keys()))
        unknown = ", ".join(sorted(invalid_agents))
        raise AgentConfigError(
            f"Unknown agent key(s) in config.yaml: {unknown}. "
            f"Valid agents: {valid_agents}"
        )

    # Parse selection config (legacy strategy field ignored)
    selection_data = agents_data.get("selection", {})
    if not isinstance(selection_data, dict):
        selection_data = {}

    selection = AgentSelectionConfig(
        preferred_implementer=selection_data.get("preferred_implementer"),
        preferred_reviewer=selection_data.get("preferred_reviewer"),
    )

    return AgentConfig(available=available, selection=selection)


def x_load_agent_config__mutmut_1(repo_root: Path) -> AgentConfig:
    """Load agent configuration from .kittify/config.yaml.

    Args:
        repo_root: Repository root directory

    Returns:
        AgentConfig instance (defaults if not configured)
    """
    config_file = None

    if not config_file.exists():
        logger.warning(f"Config file not found: {config_file}")
        return AgentConfig()

    yaml = YAML()
    yaml.preserve_quotes = True

    try:
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        raise AgentConfigError(
            f"Invalid YAML in {config_file}: {e}"
        ) from e

    agents_data = data.get("agents", {})
    if not agents_data:
        logger.info("No agents section in config.yaml")
        return AgentConfig()

    # Parse available agents
    available = agents_data.get("available", [])
    if isinstance(available, str):
        available = [available]
    if not isinstance(available, list):
        raise AgentConfigError(
            "Invalid agents.available in config.yaml: expected a list of agent keys"
        )

    invalid_agents = [agent for agent in available if agent not in AI_CHOICES]
    if invalid_agents:
        valid_agents = ", ".join(sorted(AI_CHOICES.keys()))
        unknown = ", ".join(sorted(invalid_agents))
        raise AgentConfigError(
            f"Unknown agent key(s) in config.yaml: {unknown}. "
            f"Valid agents: {valid_agents}"
        )

    # Parse selection config (legacy strategy field ignored)
    selection_data = agents_data.get("selection", {})
    if not isinstance(selection_data, dict):
        selection_data = {}

    selection = AgentSelectionConfig(
        preferred_implementer=selection_data.get("preferred_implementer"),
        preferred_reviewer=selection_data.get("preferred_reviewer"),
    )

    return AgentConfig(available=available, selection=selection)


def x_load_agent_config__mutmut_2(repo_root: Path) -> AgentConfig:
    """Load agent configuration from .kittify/config.yaml.

    Args:
        repo_root: Repository root directory

    Returns:
        AgentConfig instance (defaults if not configured)
    """
    config_file = repo_root / ".kittify" * "config.yaml"

    if not config_file.exists():
        logger.warning(f"Config file not found: {config_file}")
        return AgentConfig()

    yaml = YAML()
    yaml.preserve_quotes = True

    try:
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        raise AgentConfigError(
            f"Invalid YAML in {config_file}: {e}"
        ) from e

    agents_data = data.get("agents", {})
    if not agents_data:
        logger.info("No agents section in config.yaml")
        return AgentConfig()

    # Parse available agents
    available = agents_data.get("available", [])
    if isinstance(available, str):
        available = [available]
    if not isinstance(available, list):
        raise AgentConfigError(
            "Invalid agents.available in config.yaml: expected a list of agent keys"
        )

    invalid_agents = [agent for agent in available if agent not in AI_CHOICES]
    if invalid_agents:
        valid_agents = ", ".join(sorted(AI_CHOICES.keys()))
        unknown = ", ".join(sorted(invalid_agents))
        raise AgentConfigError(
            f"Unknown agent key(s) in config.yaml: {unknown}. "
            f"Valid agents: {valid_agents}"
        )

    # Parse selection config (legacy strategy field ignored)
    selection_data = agents_data.get("selection", {})
    if not isinstance(selection_data, dict):
        selection_data = {}

    selection = AgentSelectionConfig(
        preferred_implementer=selection_data.get("preferred_implementer"),
        preferred_reviewer=selection_data.get("preferred_reviewer"),
    )

    return AgentConfig(available=available, selection=selection)


def x_load_agent_config__mutmut_3(repo_root: Path) -> AgentConfig:
    """Load agent configuration from .kittify/config.yaml.

    Args:
        repo_root: Repository root directory

    Returns:
        AgentConfig instance (defaults if not configured)
    """
    config_file = repo_root * ".kittify" / "config.yaml"

    if not config_file.exists():
        logger.warning(f"Config file not found: {config_file}")
        return AgentConfig()

    yaml = YAML()
    yaml.preserve_quotes = True

    try:
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        raise AgentConfigError(
            f"Invalid YAML in {config_file}: {e}"
        ) from e

    agents_data = data.get("agents", {})
    if not agents_data:
        logger.info("No agents section in config.yaml")
        return AgentConfig()

    # Parse available agents
    available = agents_data.get("available", [])
    if isinstance(available, str):
        available = [available]
    if not isinstance(available, list):
        raise AgentConfigError(
            "Invalid agents.available in config.yaml: expected a list of agent keys"
        )

    invalid_agents = [agent for agent in available if agent not in AI_CHOICES]
    if invalid_agents:
        valid_agents = ", ".join(sorted(AI_CHOICES.keys()))
        unknown = ", ".join(sorted(invalid_agents))
        raise AgentConfigError(
            f"Unknown agent key(s) in config.yaml: {unknown}. "
            f"Valid agents: {valid_agents}"
        )

    # Parse selection config (legacy strategy field ignored)
    selection_data = agents_data.get("selection", {})
    if not isinstance(selection_data, dict):
        selection_data = {}

    selection = AgentSelectionConfig(
        preferred_implementer=selection_data.get("preferred_implementer"),
        preferred_reviewer=selection_data.get("preferred_reviewer"),
    )

    return AgentConfig(available=available, selection=selection)


def x_load_agent_config__mutmut_4(repo_root: Path) -> AgentConfig:
    """Load agent configuration from .kittify/config.yaml.

    Args:
        repo_root: Repository root directory

    Returns:
        AgentConfig instance (defaults if not configured)
    """
    config_file = repo_root / "XX.kittifyXX" / "config.yaml"

    if not config_file.exists():
        logger.warning(f"Config file not found: {config_file}")
        return AgentConfig()

    yaml = YAML()
    yaml.preserve_quotes = True

    try:
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        raise AgentConfigError(
            f"Invalid YAML in {config_file}: {e}"
        ) from e

    agents_data = data.get("agents", {})
    if not agents_data:
        logger.info("No agents section in config.yaml")
        return AgentConfig()

    # Parse available agents
    available = agents_data.get("available", [])
    if isinstance(available, str):
        available = [available]
    if not isinstance(available, list):
        raise AgentConfigError(
            "Invalid agents.available in config.yaml: expected a list of agent keys"
        )

    invalid_agents = [agent for agent in available if agent not in AI_CHOICES]
    if invalid_agents:
        valid_agents = ", ".join(sorted(AI_CHOICES.keys()))
        unknown = ", ".join(sorted(invalid_agents))
        raise AgentConfigError(
            f"Unknown agent key(s) in config.yaml: {unknown}. "
            f"Valid agents: {valid_agents}"
        )

    # Parse selection config (legacy strategy field ignored)
    selection_data = agents_data.get("selection", {})
    if not isinstance(selection_data, dict):
        selection_data = {}

    selection = AgentSelectionConfig(
        preferred_implementer=selection_data.get("preferred_implementer"),
        preferred_reviewer=selection_data.get("preferred_reviewer"),
    )

    return AgentConfig(available=available, selection=selection)


def x_load_agent_config__mutmut_5(repo_root: Path) -> AgentConfig:
    """Load agent configuration from .kittify/config.yaml.

    Args:
        repo_root: Repository root directory

    Returns:
        AgentConfig instance (defaults if not configured)
    """
    config_file = repo_root / ".KITTIFY" / "config.yaml"

    if not config_file.exists():
        logger.warning(f"Config file not found: {config_file}")
        return AgentConfig()

    yaml = YAML()
    yaml.preserve_quotes = True

    try:
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        raise AgentConfigError(
            f"Invalid YAML in {config_file}: {e}"
        ) from e

    agents_data = data.get("agents", {})
    if not agents_data:
        logger.info("No agents section in config.yaml")
        return AgentConfig()

    # Parse available agents
    available = agents_data.get("available", [])
    if isinstance(available, str):
        available = [available]
    if not isinstance(available, list):
        raise AgentConfigError(
            "Invalid agents.available in config.yaml: expected a list of agent keys"
        )

    invalid_agents = [agent for agent in available if agent not in AI_CHOICES]
    if invalid_agents:
        valid_agents = ", ".join(sorted(AI_CHOICES.keys()))
        unknown = ", ".join(sorted(invalid_agents))
        raise AgentConfigError(
            f"Unknown agent key(s) in config.yaml: {unknown}. "
            f"Valid agents: {valid_agents}"
        )

    # Parse selection config (legacy strategy field ignored)
    selection_data = agents_data.get("selection", {})
    if not isinstance(selection_data, dict):
        selection_data = {}

    selection = AgentSelectionConfig(
        preferred_implementer=selection_data.get("preferred_implementer"),
        preferred_reviewer=selection_data.get("preferred_reviewer"),
    )

    return AgentConfig(available=available, selection=selection)


def x_load_agent_config__mutmut_6(repo_root: Path) -> AgentConfig:
    """Load agent configuration from .kittify/config.yaml.

    Args:
        repo_root: Repository root directory

    Returns:
        AgentConfig instance (defaults if not configured)
    """
    config_file = repo_root / ".kittify" / "XXconfig.yamlXX"

    if not config_file.exists():
        logger.warning(f"Config file not found: {config_file}")
        return AgentConfig()

    yaml = YAML()
    yaml.preserve_quotes = True

    try:
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        raise AgentConfigError(
            f"Invalid YAML in {config_file}: {e}"
        ) from e

    agents_data = data.get("agents", {})
    if not agents_data:
        logger.info("No agents section in config.yaml")
        return AgentConfig()

    # Parse available agents
    available = agents_data.get("available", [])
    if isinstance(available, str):
        available = [available]
    if not isinstance(available, list):
        raise AgentConfigError(
            "Invalid agents.available in config.yaml: expected a list of agent keys"
        )

    invalid_agents = [agent for agent in available if agent not in AI_CHOICES]
    if invalid_agents:
        valid_agents = ", ".join(sorted(AI_CHOICES.keys()))
        unknown = ", ".join(sorted(invalid_agents))
        raise AgentConfigError(
            f"Unknown agent key(s) in config.yaml: {unknown}. "
            f"Valid agents: {valid_agents}"
        )

    # Parse selection config (legacy strategy field ignored)
    selection_data = agents_data.get("selection", {})
    if not isinstance(selection_data, dict):
        selection_data = {}

    selection = AgentSelectionConfig(
        preferred_implementer=selection_data.get("preferred_implementer"),
        preferred_reviewer=selection_data.get("preferred_reviewer"),
    )

    return AgentConfig(available=available, selection=selection)


def x_load_agent_config__mutmut_7(repo_root: Path) -> AgentConfig:
    """Load agent configuration from .kittify/config.yaml.

    Args:
        repo_root: Repository root directory

    Returns:
        AgentConfig instance (defaults if not configured)
    """
    config_file = repo_root / ".kittify" / "CONFIG.YAML"

    if not config_file.exists():
        logger.warning(f"Config file not found: {config_file}")
        return AgentConfig()

    yaml = YAML()
    yaml.preserve_quotes = True

    try:
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        raise AgentConfigError(
            f"Invalid YAML in {config_file}: {e}"
        ) from e

    agents_data = data.get("agents", {})
    if not agents_data:
        logger.info("No agents section in config.yaml")
        return AgentConfig()

    # Parse available agents
    available = agents_data.get("available", [])
    if isinstance(available, str):
        available = [available]
    if not isinstance(available, list):
        raise AgentConfigError(
            "Invalid agents.available in config.yaml: expected a list of agent keys"
        )

    invalid_agents = [agent for agent in available if agent not in AI_CHOICES]
    if invalid_agents:
        valid_agents = ", ".join(sorted(AI_CHOICES.keys()))
        unknown = ", ".join(sorted(invalid_agents))
        raise AgentConfigError(
            f"Unknown agent key(s) in config.yaml: {unknown}. "
            f"Valid agents: {valid_agents}"
        )

    # Parse selection config (legacy strategy field ignored)
    selection_data = agents_data.get("selection", {})
    if not isinstance(selection_data, dict):
        selection_data = {}

    selection = AgentSelectionConfig(
        preferred_implementer=selection_data.get("preferred_implementer"),
        preferred_reviewer=selection_data.get("preferred_reviewer"),
    )

    return AgentConfig(available=available, selection=selection)


def x_load_agent_config__mutmut_8(repo_root: Path) -> AgentConfig:
    """Load agent configuration from .kittify/config.yaml.

    Args:
        repo_root: Repository root directory

    Returns:
        AgentConfig instance (defaults if not configured)
    """
    config_file = repo_root / ".kittify" / "config.yaml"

    if config_file.exists():
        logger.warning(f"Config file not found: {config_file}")
        return AgentConfig()

    yaml = YAML()
    yaml.preserve_quotes = True

    try:
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        raise AgentConfigError(
            f"Invalid YAML in {config_file}: {e}"
        ) from e

    agents_data = data.get("agents", {})
    if not agents_data:
        logger.info("No agents section in config.yaml")
        return AgentConfig()

    # Parse available agents
    available = agents_data.get("available", [])
    if isinstance(available, str):
        available = [available]
    if not isinstance(available, list):
        raise AgentConfigError(
            "Invalid agents.available in config.yaml: expected a list of agent keys"
        )

    invalid_agents = [agent for agent in available if agent not in AI_CHOICES]
    if invalid_agents:
        valid_agents = ", ".join(sorted(AI_CHOICES.keys()))
        unknown = ", ".join(sorted(invalid_agents))
        raise AgentConfigError(
            f"Unknown agent key(s) in config.yaml: {unknown}. "
            f"Valid agents: {valid_agents}"
        )

    # Parse selection config (legacy strategy field ignored)
    selection_data = agents_data.get("selection", {})
    if not isinstance(selection_data, dict):
        selection_data = {}

    selection = AgentSelectionConfig(
        preferred_implementer=selection_data.get("preferred_implementer"),
        preferred_reviewer=selection_data.get("preferred_reviewer"),
    )

    return AgentConfig(available=available, selection=selection)


def x_load_agent_config__mutmut_9(repo_root: Path) -> AgentConfig:
    """Load agent configuration from .kittify/config.yaml.

    Args:
        repo_root: Repository root directory

    Returns:
        AgentConfig instance (defaults if not configured)
    """
    config_file = repo_root / ".kittify" / "config.yaml"

    if not config_file.exists():
        logger.warning(None)
        return AgentConfig()

    yaml = YAML()
    yaml.preserve_quotes = True

    try:
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        raise AgentConfigError(
            f"Invalid YAML in {config_file}: {e}"
        ) from e

    agents_data = data.get("agents", {})
    if not agents_data:
        logger.info("No agents section in config.yaml")
        return AgentConfig()

    # Parse available agents
    available = agents_data.get("available", [])
    if isinstance(available, str):
        available = [available]
    if not isinstance(available, list):
        raise AgentConfigError(
            "Invalid agents.available in config.yaml: expected a list of agent keys"
        )

    invalid_agents = [agent for agent in available if agent not in AI_CHOICES]
    if invalid_agents:
        valid_agents = ", ".join(sorted(AI_CHOICES.keys()))
        unknown = ", ".join(sorted(invalid_agents))
        raise AgentConfigError(
            f"Unknown agent key(s) in config.yaml: {unknown}. "
            f"Valid agents: {valid_agents}"
        )

    # Parse selection config (legacy strategy field ignored)
    selection_data = agents_data.get("selection", {})
    if not isinstance(selection_data, dict):
        selection_data = {}

    selection = AgentSelectionConfig(
        preferred_implementer=selection_data.get("preferred_implementer"),
        preferred_reviewer=selection_data.get("preferred_reviewer"),
    )

    return AgentConfig(available=available, selection=selection)


def x_load_agent_config__mutmut_10(repo_root: Path) -> AgentConfig:
    """Load agent configuration from .kittify/config.yaml.

    Args:
        repo_root: Repository root directory

    Returns:
        AgentConfig instance (defaults if not configured)
    """
    config_file = repo_root / ".kittify" / "config.yaml"

    if not config_file.exists():
        logger.warning(f"Config file not found: {config_file}")
        return AgentConfig()

    yaml = None
    yaml.preserve_quotes = True

    try:
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        raise AgentConfigError(
            f"Invalid YAML in {config_file}: {e}"
        ) from e

    agents_data = data.get("agents", {})
    if not agents_data:
        logger.info("No agents section in config.yaml")
        return AgentConfig()

    # Parse available agents
    available = agents_data.get("available", [])
    if isinstance(available, str):
        available = [available]
    if not isinstance(available, list):
        raise AgentConfigError(
            "Invalid agents.available in config.yaml: expected a list of agent keys"
        )

    invalid_agents = [agent for agent in available if agent not in AI_CHOICES]
    if invalid_agents:
        valid_agents = ", ".join(sorted(AI_CHOICES.keys()))
        unknown = ", ".join(sorted(invalid_agents))
        raise AgentConfigError(
            f"Unknown agent key(s) in config.yaml: {unknown}. "
            f"Valid agents: {valid_agents}"
        )

    # Parse selection config (legacy strategy field ignored)
    selection_data = agents_data.get("selection", {})
    if not isinstance(selection_data, dict):
        selection_data = {}

    selection = AgentSelectionConfig(
        preferred_implementer=selection_data.get("preferred_implementer"),
        preferred_reviewer=selection_data.get("preferred_reviewer"),
    )

    return AgentConfig(available=available, selection=selection)


def x_load_agent_config__mutmut_11(repo_root: Path) -> AgentConfig:
    """Load agent configuration from .kittify/config.yaml.

    Args:
        repo_root: Repository root directory

    Returns:
        AgentConfig instance (defaults if not configured)
    """
    config_file = repo_root / ".kittify" / "config.yaml"

    if not config_file.exists():
        logger.warning(f"Config file not found: {config_file}")
        return AgentConfig()

    yaml = YAML()
    yaml.preserve_quotes = None

    try:
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        raise AgentConfigError(
            f"Invalid YAML in {config_file}: {e}"
        ) from e

    agents_data = data.get("agents", {})
    if not agents_data:
        logger.info("No agents section in config.yaml")
        return AgentConfig()

    # Parse available agents
    available = agents_data.get("available", [])
    if isinstance(available, str):
        available = [available]
    if not isinstance(available, list):
        raise AgentConfigError(
            "Invalid agents.available in config.yaml: expected a list of agent keys"
        )

    invalid_agents = [agent for agent in available if agent not in AI_CHOICES]
    if invalid_agents:
        valid_agents = ", ".join(sorted(AI_CHOICES.keys()))
        unknown = ", ".join(sorted(invalid_agents))
        raise AgentConfigError(
            f"Unknown agent key(s) in config.yaml: {unknown}. "
            f"Valid agents: {valid_agents}"
        )

    # Parse selection config (legacy strategy field ignored)
    selection_data = agents_data.get("selection", {})
    if not isinstance(selection_data, dict):
        selection_data = {}

    selection = AgentSelectionConfig(
        preferred_implementer=selection_data.get("preferred_implementer"),
        preferred_reviewer=selection_data.get("preferred_reviewer"),
    )

    return AgentConfig(available=available, selection=selection)


def x_load_agent_config__mutmut_12(repo_root: Path) -> AgentConfig:
    """Load agent configuration from .kittify/config.yaml.

    Args:
        repo_root: Repository root directory

    Returns:
        AgentConfig instance (defaults if not configured)
    """
    config_file = repo_root / ".kittify" / "config.yaml"

    if not config_file.exists():
        logger.warning(f"Config file not found: {config_file}")
        return AgentConfig()

    yaml = YAML()
    yaml.preserve_quotes = False

    try:
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        raise AgentConfigError(
            f"Invalid YAML in {config_file}: {e}"
        ) from e

    agents_data = data.get("agents", {})
    if not agents_data:
        logger.info("No agents section in config.yaml")
        return AgentConfig()

    # Parse available agents
    available = agents_data.get("available", [])
    if isinstance(available, str):
        available = [available]
    if not isinstance(available, list):
        raise AgentConfigError(
            "Invalid agents.available in config.yaml: expected a list of agent keys"
        )

    invalid_agents = [agent for agent in available if agent not in AI_CHOICES]
    if invalid_agents:
        valid_agents = ", ".join(sorted(AI_CHOICES.keys()))
        unknown = ", ".join(sorted(invalid_agents))
        raise AgentConfigError(
            f"Unknown agent key(s) in config.yaml: {unknown}. "
            f"Valid agents: {valid_agents}"
        )

    # Parse selection config (legacy strategy field ignored)
    selection_data = agents_data.get("selection", {})
    if not isinstance(selection_data, dict):
        selection_data = {}

    selection = AgentSelectionConfig(
        preferred_implementer=selection_data.get("preferred_implementer"),
        preferred_reviewer=selection_data.get("preferred_reviewer"),
    )

    return AgentConfig(available=available, selection=selection)


def x_load_agent_config__mutmut_13(repo_root: Path) -> AgentConfig:
    """Load agent configuration from .kittify/config.yaml.

    Args:
        repo_root: Repository root directory

    Returns:
        AgentConfig instance (defaults if not configured)
    """
    config_file = repo_root / ".kittify" / "config.yaml"

    if not config_file.exists():
        logger.warning(f"Config file not found: {config_file}")
        return AgentConfig()

    yaml = YAML()
    yaml.preserve_quotes = True

    try:
        with open(None, "r") as f:
            data = yaml.load(f) or {}
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        raise AgentConfigError(
            f"Invalid YAML in {config_file}: {e}"
        ) from e

    agents_data = data.get("agents", {})
    if not agents_data:
        logger.info("No agents section in config.yaml")
        return AgentConfig()

    # Parse available agents
    available = agents_data.get("available", [])
    if isinstance(available, str):
        available = [available]
    if not isinstance(available, list):
        raise AgentConfigError(
            "Invalid agents.available in config.yaml: expected a list of agent keys"
        )

    invalid_agents = [agent for agent in available if agent not in AI_CHOICES]
    if invalid_agents:
        valid_agents = ", ".join(sorted(AI_CHOICES.keys()))
        unknown = ", ".join(sorted(invalid_agents))
        raise AgentConfigError(
            f"Unknown agent key(s) in config.yaml: {unknown}. "
            f"Valid agents: {valid_agents}"
        )

    # Parse selection config (legacy strategy field ignored)
    selection_data = agents_data.get("selection", {})
    if not isinstance(selection_data, dict):
        selection_data = {}

    selection = AgentSelectionConfig(
        preferred_implementer=selection_data.get("preferred_implementer"),
        preferred_reviewer=selection_data.get("preferred_reviewer"),
    )

    return AgentConfig(available=available, selection=selection)


def x_load_agent_config__mutmut_14(repo_root: Path) -> AgentConfig:
    """Load agent configuration from .kittify/config.yaml.

    Args:
        repo_root: Repository root directory

    Returns:
        AgentConfig instance (defaults if not configured)
    """
    config_file = repo_root / ".kittify" / "config.yaml"

    if not config_file.exists():
        logger.warning(f"Config file not found: {config_file}")
        return AgentConfig()

    yaml = YAML()
    yaml.preserve_quotes = True

    try:
        with open(config_file, None) as f:
            data = yaml.load(f) or {}
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        raise AgentConfigError(
            f"Invalid YAML in {config_file}: {e}"
        ) from e

    agents_data = data.get("agents", {})
    if not agents_data:
        logger.info("No agents section in config.yaml")
        return AgentConfig()

    # Parse available agents
    available = agents_data.get("available", [])
    if isinstance(available, str):
        available = [available]
    if not isinstance(available, list):
        raise AgentConfigError(
            "Invalid agents.available in config.yaml: expected a list of agent keys"
        )

    invalid_agents = [agent for agent in available if agent not in AI_CHOICES]
    if invalid_agents:
        valid_agents = ", ".join(sorted(AI_CHOICES.keys()))
        unknown = ", ".join(sorted(invalid_agents))
        raise AgentConfigError(
            f"Unknown agent key(s) in config.yaml: {unknown}. "
            f"Valid agents: {valid_agents}"
        )

    # Parse selection config (legacy strategy field ignored)
    selection_data = agents_data.get("selection", {})
    if not isinstance(selection_data, dict):
        selection_data = {}

    selection = AgentSelectionConfig(
        preferred_implementer=selection_data.get("preferred_implementer"),
        preferred_reviewer=selection_data.get("preferred_reviewer"),
    )

    return AgentConfig(available=available, selection=selection)


def x_load_agent_config__mutmut_15(repo_root: Path) -> AgentConfig:
    """Load agent configuration from .kittify/config.yaml.

    Args:
        repo_root: Repository root directory

    Returns:
        AgentConfig instance (defaults if not configured)
    """
    config_file = repo_root / ".kittify" / "config.yaml"

    if not config_file.exists():
        logger.warning(f"Config file not found: {config_file}")
        return AgentConfig()

    yaml = YAML()
    yaml.preserve_quotes = True

    try:
        with open("r") as f:
            data = yaml.load(f) or {}
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        raise AgentConfigError(
            f"Invalid YAML in {config_file}: {e}"
        ) from e

    agents_data = data.get("agents", {})
    if not agents_data:
        logger.info("No agents section in config.yaml")
        return AgentConfig()

    # Parse available agents
    available = agents_data.get("available", [])
    if isinstance(available, str):
        available = [available]
    if not isinstance(available, list):
        raise AgentConfigError(
            "Invalid agents.available in config.yaml: expected a list of agent keys"
        )

    invalid_agents = [agent for agent in available if agent not in AI_CHOICES]
    if invalid_agents:
        valid_agents = ", ".join(sorted(AI_CHOICES.keys()))
        unknown = ", ".join(sorted(invalid_agents))
        raise AgentConfigError(
            f"Unknown agent key(s) in config.yaml: {unknown}. "
            f"Valid agents: {valid_agents}"
        )

    # Parse selection config (legacy strategy field ignored)
    selection_data = agents_data.get("selection", {})
    if not isinstance(selection_data, dict):
        selection_data = {}

    selection = AgentSelectionConfig(
        preferred_implementer=selection_data.get("preferred_implementer"),
        preferred_reviewer=selection_data.get("preferred_reviewer"),
    )

    return AgentConfig(available=available, selection=selection)


def x_load_agent_config__mutmut_16(repo_root: Path) -> AgentConfig:
    """Load agent configuration from .kittify/config.yaml.

    Args:
        repo_root: Repository root directory

    Returns:
        AgentConfig instance (defaults if not configured)
    """
    config_file = repo_root / ".kittify" / "config.yaml"

    if not config_file.exists():
        logger.warning(f"Config file not found: {config_file}")
        return AgentConfig()

    yaml = YAML()
    yaml.preserve_quotes = True

    try:
        with open(config_file, ) as f:
            data = yaml.load(f) or {}
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        raise AgentConfigError(
            f"Invalid YAML in {config_file}: {e}"
        ) from e

    agents_data = data.get("agents", {})
    if not agents_data:
        logger.info("No agents section in config.yaml")
        return AgentConfig()

    # Parse available agents
    available = agents_data.get("available", [])
    if isinstance(available, str):
        available = [available]
    if not isinstance(available, list):
        raise AgentConfigError(
            "Invalid agents.available in config.yaml: expected a list of agent keys"
        )

    invalid_agents = [agent for agent in available if agent not in AI_CHOICES]
    if invalid_agents:
        valid_agents = ", ".join(sorted(AI_CHOICES.keys()))
        unknown = ", ".join(sorted(invalid_agents))
        raise AgentConfigError(
            f"Unknown agent key(s) in config.yaml: {unknown}. "
            f"Valid agents: {valid_agents}"
        )

    # Parse selection config (legacy strategy field ignored)
    selection_data = agents_data.get("selection", {})
    if not isinstance(selection_data, dict):
        selection_data = {}

    selection = AgentSelectionConfig(
        preferred_implementer=selection_data.get("preferred_implementer"),
        preferred_reviewer=selection_data.get("preferred_reviewer"),
    )

    return AgentConfig(available=available, selection=selection)


def x_load_agent_config__mutmut_17(repo_root: Path) -> AgentConfig:
    """Load agent configuration from .kittify/config.yaml.

    Args:
        repo_root: Repository root directory

    Returns:
        AgentConfig instance (defaults if not configured)
    """
    config_file = repo_root / ".kittify" / "config.yaml"

    if not config_file.exists():
        logger.warning(f"Config file not found: {config_file}")
        return AgentConfig()

    yaml = YAML()
    yaml.preserve_quotes = True

    try:
        with open(config_file, "XXrXX") as f:
            data = yaml.load(f) or {}
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        raise AgentConfigError(
            f"Invalid YAML in {config_file}: {e}"
        ) from e

    agents_data = data.get("agents", {})
    if not agents_data:
        logger.info("No agents section in config.yaml")
        return AgentConfig()

    # Parse available agents
    available = agents_data.get("available", [])
    if isinstance(available, str):
        available = [available]
    if not isinstance(available, list):
        raise AgentConfigError(
            "Invalid agents.available in config.yaml: expected a list of agent keys"
        )

    invalid_agents = [agent for agent in available if agent not in AI_CHOICES]
    if invalid_agents:
        valid_agents = ", ".join(sorted(AI_CHOICES.keys()))
        unknown = ", ".join(sorted(invalid_agents))
        raise AgentConfigError(
            f"Unknown agent key(s) in config.yaml: {unknown}. "
            f"Valid agents: {valid_agents}"
        )

    # Parse selection config (legacy strategy field ignored)
    selection_data = agents_data.get("selection", {})
    if not isinstance(selection_data, dict):
        selection_data = {}

    selection = AgentSelectionConfig(
        preferred_implementer=selection_data.get("preferred_implementer"),
        preferred_reviewer=selection_data.get("preferred_reviewer"),
    )

    return AgentConfig(available=available, selection=selection)


def x_load_agent_config__mutmut_18(repo_root: Path) -> AgentConfig:
    """Load agent configuration from .kittify/config.yaml.

    Args:
        repo_root: Repository root directory

    Returns:
        AgentConfig instance (defaults if not configured)
    """
    config_file = repo_root / ".kittify" / "config.yaml"

    if not config_file.exists():
        logger.warning(f"Config file not found: {config_file}")
        return AgentConfig()

    yaml = YAML()
    yaml.preserve_quotes = True

    try:
        with open(config_file, "R") as f:
            data = yaml.load(f) or {}
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        raise AgentConfigError(
            f"Invalid YAML in {config_file}: {e}"
        ) from e

    agents_data = data.get("agents", {})
    if not agents_data:
        logger.info("No agents section in config.yaml")
        return AgentConfig()

    # Parse available agents
    available = agents_data.get("available", [])
    if isinstance(available, str):
        available = [available]
    if not isinstance(available, list):
        raise AgentConfigError(
            "Invalid agents.available in config.yaml: expected a list of agent keys"
        )

    invalid_agents = [agent for agent in available if agent not in AI_CHOICES]
    if invalid_agents:
        valid_agents = ", ".join(sorted(AI_CHOICES.keys()))
        unknown = ", ".join(sorted(invalid_agents))
        raise AgentConfigError(
            f"Unknown agent key(s) in config.yaml: {unknown}. "
            f"Valid agents: {valid_agents}"
        )

    # Parse selection config (legacy strategy field ignored)
    selection_data = agents_data.get("selection", {})
    if not isinstance(selection_data, dict):
        selection_data = {}

    selection = AgentSelectionConfig(
        preferred_implementer=selection_data.get("preferred_implementer"),
        preferred_reviewer=selection_data.get("preferred_reviewer"),
    )

    return AgentConfig(available=available, selection=selection)


def x_load_agent_config__mutmut_19(repo_root: Path) -> AgentConfig:
    """Load agent configuration from .kittify/config.yaml.

    Args:
        repo_root: Repository root directory

    Returns:
        AgentConfig instance (defaults if not configured)
    """
    config_file = repo_root / ".kittify" / "config.yaml"

    if not config_file.exists():
        logger.warning(f"Config file not found: {config_file}")
        return AgentConfig()

    yaml = YAML()
    yaml.preserve_quotes = True

    try:
        with open(config_file, "r") as f:
            data = None
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        raise AgentConfigError(
            f"Invalid YAML in {config_file}: {e}"
        ) from e

    agents_data = data.get("agents", {})
    if not agents_data:
        logger.info("No agents section in config.yaml")
        return AgentConfig()

    # Parse available agents
    available = agents_data.get("available", [])
    if isinstance(available, str):
        available = [available]
    if not isinstance(available, list):
        raise AgentConfigError(
            "Invalid agents.available in config.yaml: expected a list of agent keys"
        )

    invalid_agents = [agent for agent in available if agent not in AI_CHOICES]
    if invalid_agents:
        valid_agents = ", ".join(sorted(AI_CHOICES.keys()))
        unknown = ", ".join(sorted(invalid_agents))
        raise AgentConfigError(
            f"Unknown agent key(s) in config.yaml: {unknown}. "
            f"Valid agents: {valid_agents}"
        )

    # Parse selection config (legacy strategy field ignored)
    selection_data = agents_data.get("selection", {})
    if not isinstance(selection_data, dict):
        selection_data = {}

    selection = AgentSelectionConfig(
        preferred_implementer=selection_data.get("preferred_implementer"),
        preferred_reviewer=selection_data.get("preferred_reviewer"),
    )

    return AgentConfig(available=available, selection=selection)


def x_load_agent_config__mutmut_20(repo_root: Path) -> AgentConfig:
    """Load agent configuration from .kittify/config.yaml.

    Args:
        repo_root: Repository root directory

    Returns:
        AgentConfig instance (defaults if not configured)
    """
    config_file = repo_root / ".kittify" / "config.yaml"

    if not config_file.exists():
        logger.warning(f"Config file not found: {config_file}")
        return AgentConfig()

    yaml = YAML()
    yaml.preserve_quotes = True

    try:
        with open(config_file, "r") as f:
            data = yaml.load(f) and {}
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        raise AgentConfigError(
            f"Invalid YAML in {config_file}: {e}"
        ) from e

    agents_data = data.get("agents", {})
    if not agents_data:
        logger.info("No agents section in config.yaml")
        return AgentConfig()

    # Parse available agents
    available = agents_data.get("available", [])
    if isinstance(available, str):
        available = [available]
    if not isinstance(available, list):
        raise AgentConfigError(
            "Invalid agents.available in config.yaml: expected a list of agent keys"
        )

    invalid_agents = [agent for agent in available if agent not in AI_CHOICES]
    if invalid_agents:
        valid_agents = ", ".join(sorted(AI_CHOICES.keys()))
        unknown = ", ".join(sorted(invalid_agents))
        raise AgentConfigError(
            f"Unknown agent key(s) in config.yaml: {unknown}. "
            f"Valid agents: {valid_agents}"
        )

    # Parse selection config (legacy strategy field ignored)
    selection_data = agents_data.get("selection", {})
    if not isinstance(selection_data, dict):
        selection_data = {}

    selection = AgentSelectionConfig(
        preferred_implementer=selection_data.get("preferred_implementer"),
        preferred_reviewer=selection_data.get("preferred_reviewer"),
    )

    return AgentConfig(available=available, selection=selection)


def x_load_agent_config__mutmut_21(repo_root: Path) -> AgentConfig:
    """Load agent configuration from .kittify/config.yaml.

    Args:
        repo_root: Repository root directory

    Returns:
        AgentConfig instance (defaults if not configured)
    """
    config_file = repo_root / ".kittify" / "config.yaml"

    if not config_file.exists():
        logger.warning(f"Config file not found: {config_file}")
        return AgentConfig()

    yaml = YAML()
    yaml.preserve_quotes = True

    try:
        with open(config_file, "r") as f:
            data = yaml.load(None) or {}
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        raise AgentConfigError(
            f"Invalid YAML in {config_file}: {e}"
        ) from e

    agents_data = data.get("agents", {})
    if not agents_data:
        logger.info("No agents section in config.yaml")
        return AgentConfig()

    # Parse available agents
    available = agents_data.get("available", [])
    if isinstance(available, str):
        available = [available]
    if not isinstance(available, list):
        raise AgentConfigError(
            "Invalid agents.available in config.yaml: expected a list of agent keys"
        )

    invalid_agents = [agent for agent in available if agent not in AI_CHOICES]
    if invalid_agents:
        valid_agents = ", ".join(sorted(AI_CHOICES.keys()))
        unknown = ", ".join(sorted(invalid_agents))
        raise AgentConfigError(
            f"Unknown agent key(s) in config.yaml: {unknown}. "
            f"Valid agents: {valid_agents}"
        )

    # Parse selection config (legacy strategy field ignored)
    selection_data = agents_data.get("selection", {})
    if not isinstance(selection_data, dict):
        selection_data = {}

    selection = AgentSelectionConfig(
        preferred_implementer=selection_data.get("preferred_implementer"),
        preferred_reviewer=selection_data.get("preferred_reviewer"),
    )

    return AgentConfig(available=available, selection=selection)


def x_load_agent_config__mutmut_22(repo_root: Path) -> AgentConfig:
    """Load agent configuration from .kittify/config.yaml.

    Args:
        repo_root: Repository root directory

    Returns:
        AgentConfig instance (defaults if not configured)
    """
    config_file = repo_root / ".kittify" / "config.yaml"

    if not config_file.exists():
        logger.warning(f"Config file not found: {config_file}")
        return AgentConfig()

    yaml = YAML()
    yaml.preserve_quotes = True

    try:
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    except Exception as e:
        logger.error(None)
        raise AgentConfigError(
            f"Invalid YAML in {config_file}: {e}"
        ) from e

    agents_data = data.get("agents", {})
    if not agents_data:
        logger.info("No agents section in config.yaml")
        return AgentConfig()

    # Parse available agents
    available = agents_data.get("available", [])
    if isinstance(available, str):
        available = [available]
    if not isinstance(available, list):
        raise AgentConfigError(
            "Invalid agents.available in config.yaml: expected a list of agent keys"
        )

    invalid_agents = [agent for agent in available if agent not in AI_CHOICES]
    if invalid_agents:
        valid_agents = ", ".join(sorted(AI_CHOICES.keys()))
        unknown = ", ".join(sorted(invalid_agents))
        raise AgentConfigError(
            f"Unknown agent key(s) in config.yaml: {unknown}. "
            f"Valid agents: {valid_agents}"
        )

    # Parse selection config (legacy strategy field ignored)
    selection_data = agents_data.get("selection", {})
    if not isinstance(selection_data, dict):
        selection_data = {}

    selection = AgentSelectionConfig(
        preferred_implementer=selection_data.get("preferred_implementer"),
        preferred_reviewer=selection_data.get("preferred_reviewer"),
    )

    return AgentConfig(available=available, selection=selection)


def x_load_agent_config__mutmut_23(repo_root: Path) -> AgentConfig:
    """Load agent configuration from .kittify/config.yaml.

    Args:
        repo_root: Repository root directory

    Returns:
        AgentConfig instance (defaults if not configured)
    """
    config_file = repo_root / ".kittify" / "config.yaml"

    if not config_file.exists():
        logger.warning(f"Config file not found: {config_file}")
        return AgentConfig()

    yaml = YAML()
    yaml.preserve_quotes = True

    try:
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        raise AgentConfigError(
            None
        ) from e

    agents_data = data.get("agents", {})
    if not agents_data:
        logger.info("No agents section in config.yaml")
        return AgentConfig()

    # Parse available agents
    available = agents_data.get("available", [])
    if isinstance(available, str):
        available = [available]
    if not isinstance(available, list):
        raise AgentConfigError(
            "Invalid agents.available in config.yaml: expected a list of agent keys"
        )

    invalid_agents = [agent for agent in available if agent not in AI_CHOICES]
    if invalid_agents:
        valid_agents = ", ".join(sorted(AI_CHOICES.keys()))
        unknown = ", ".join(sorted(invalid_agents))
        raise AgentConfigError(
            f"Unknown agent key(s) in config.yaml: {unknown}. "
            f"Valid agents: {valid_agents}"
        )

    # Parse selection config (legacy strategy field ignored)
    selection_data = agents_data.get("selection", {})
    if not isinstance(selection_data, dict):
        selection_data = {}

    selection = AgentSelectionConfig(
        preferred_implementer=selection_data.get("preferred_implementer"),
        preferred_reviewer=selection_data.get("preferred_reviewer"),
    )

    return AgentConfig(available=available, selection=selection)


def x_load_agent_config__mutmut_24(repo_root: Path) -> AgentConfig:
    """Load agent configuration from .kittify/config.yaml.

    Args:
        repo_root: Repository root directory

    Returns:
        AgentConfig instance (defaults if not configured)
    """
    config_file = repo_root / ".kittify" / "config.yaml"

    if not config_file.exists():
        logger.warning(f"Config file not found: {config_file}")
        return AgentConfig()

    yaml = YAML()
    yaml.preserve_quotes = True

    try:
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        raise AgentConfigError(
            f"Invalid YAML in {config_file}: {e}"
        ) from e

    agents_data = None
    if not agents_data:
        logger.info("No agents section in config.yaml")
        return AgentConfig()

    # Parse available agents
    available = agents_data.get("available", [])
    if isinstance(available, str):
        available = [available]
    if not isinstance(available, list):
        raise AgentConfigError(
            "Invalid agents.available in config.yaml: expected a list of agent keys"
        )

    invalid_agents = [agent for agent in available if agent not in AI_CHOICES]
    if invalid_agents:
        valid_agents = ", ".join(sorted(AI_CHOICES.keys()))
        unknown = ", ".join(sorted(invalid_agents))
        raise AgentConfigError(
            f"Unknown agent key(s) in config.yaml: {unknown}. "
            f"Valid agents: {valid_agents}"
        )

    # Parse selection config (legacy strategy field ignored)
    selection_data = agents_data.get("selection", {})
    if not isinstance(selection_data, dict):
        selection_data = {}

    selection = AgentSelectionConfig(
        preferred_implementer=selection_data.get("preferred_implementer"),
        preferred_reviewer=selection_data.get("preferred_reviewer"),
    )

    return AgentConfig(available=available, selection=selection)


def x_load_agent_config__mutmut_25(repo_root: Path) -> AgentConfig:
    """Load agent configuration from .kittify/config.yaml.

    Args:
        repo_root: Repository root directory

    Returns:
        AgentConfig instance (defaults if not configured)
    """
    config_file = repo_root / ".kittify" / "config.yaml"

    if not config_file.exists():
        logger.warning(f"Config file not found: {config_file}")
        return AgentConfig()

    yaml = YAML()
    yaml.preserve_quotes = True

    try:
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        raise AgentConfigError(
            f"Invalid YAML in {config_file}: {e}"
        ) from e

    agents_data = data.get(None, {})
    if not agents_data:
        logger.info("No agents section in config.yaml")
        return AgentConfig()

    # Parse available agents
    available = agents_data.get("available", [])
    if isinstance(available, str):
        available = [available]
    if not isinstance(available, list):
        raise AgentConfigError(
            "Invalid agents.available in config.yaml: expected a list of agent keys"
        )

    invalid_agents = [agent for agent in available if agent not in AI_CHOICES]
    if invalid_agents:
        valid_agents = ", ".join(sorted(AI_CHOICES.keys()))
        unknown = ", ".join(sorted(invalid_agents))
        raise AgentConfigError(
            f"Unknown agent key(s) in config.yaml: {unknown}. "
            f"Valid agents: {valid_agents}"
        )

    # Parse selection config (legacy strategy field ignored)
    selection_data = agents_data.get("selection", {})
    if not isinstance(selection_data, dict):
        selection_data = {}

    selection = AgentSelectionConfig(
        preferred_implementer=selection_data.get("preferred_implementer"),
        preferred_reviewer=selection_data.get("preferred_reviewer"),
    )

    return AgentConfig(available=available, selection=selection)


def x_load_agent_config__mutmut_26(repo_root: Path) -> AgentConfig:
    """Load agent configuration from .kittify/config.yaml.

    Args:
        repo_root: Repository root directory

    Returns:
        AgentConfig instance (defaults if not configured)
    """
    config_file = repo_root / ".kittify" / "config.yaml"

    if not config_file.exists():
        logger.warning(f"Config file not found: {config_file}")
        return AgentConfig()

    yaml = YAML()
    yaml.preserve_quotes = True

    try:
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        raise AgentConfigError(
            f"Invalid YAML in {config_file}: {e}"
        ) from e

    agents_data = data.get("agents", None)
    if not agents_data:
        logger.info("No agents section in config.yaml")
        return AgentConfig()

    # Parse available agents
    available = agents_data.get("available", [])
    if isinstance(available, str):
        available = [available]
    if not isinstance(available, list):
        raise AgentConfigError(
            "Invalid agents.available in config.yaml: expected a list of agent keys"
        )

    invalid_agents = [agent for agent in available if agent not in AI_CHOICES]
    if invalid_agents:
        valid_agents = ", ".join(sorted(AI_CHOICES.keys()))
        unknown = ", ".join(sorted(invalid_agents))
        raise AgentConfigError(
            f"Unknown agent key(s) in config.yaml: {unknown}. "
            f"Valid agents: {valid_agents}"
        )

    # Parse selection config (legacy strategy field ignored)
    selection_data = agents_data.get("selection", {})
    if not isinstance(selection_data, dict):
        selection_data = {}

    selection = AgentSelectionConfig(
        preferred_implementer=selection_data.get("preferred_implementer"),
        preferred_reviewer=selection_data.get("preferred_reviewer"),
    )

    return AgentConfig(available=available, selection=selection)


def x_load_agent_config__mutmut_27(repo_root: Path) -> AgentConfig:
    """Load agent configuration from .kittify/config.yaml.

    Args:
        repo_root: Repository root directory

    Returns:
        AgentConfig instance (defaults if not configured)
    """
    config_file = repo_root / ".kittify" / "config.yaml"

    if not config_file.exists():
        logger.warning(f"Config file not found: {config_file}")
        return AgentConfig()

    yaml = YAML()
    yaml.preserve_quotes = True

    try:
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        raise AgentConfigError(
            f"Invalid YAML in {config_file}: {e}"
        ) from e

    agents_data = data.get({})
    if not agents_data:
        logger.info("No agents section in config.yaml")
        return AgentConfig()

    # Parse available agents
    available = agents_data.get("available", [])
    if isinstance(available, str):
        available = [available]
    if not isinstance(available, list):
        raise AgentConfigError(
            "Invalid agents.available in config.yaml: expected a list of agent keys"
        )

    invalid_agents = [agent for agent in available if agent not in AI_CHOICES]
    if invalid_agents:
        valid_agents = ", ".join(sorted(AI_CHOICES.keys()))
        unknown = ", ".join(sorted(invalid_agents))
        raise AgentConfigError(
            f"Unknown agent key(s) in config.yaml: {unknown}. "
            f"Valid agents: {valid_agents}"
        )

    # Parse selection config (legacy strategy field ignored)
    selection_data = agents_data.get("selection", {})
    if not isinstance(selection_data, dict):
        selection_data = {}

    selection = AgentSelectionConfig(
        preferred_implementer=selection_data.get("preferred_implementer"),
        preferred_reviewer=selection_data.get("preferred_reviewer"),
    )

    return AgentConfig(available=available, selection=selection)


def x_load_agent_config__mutmut_28(repo_root: Path) -> AgentConfig:
    """Load agent configuration from .kittify/config.yaml.

    Args:
        repo_root: Repository root directory

    Returns:
        AgentConfig instance (defaults if not configured)
    """
    config_file = repo_root / ".kittify" / "config.yaml"

    if not config_file.exists():
        logger.warning(f"Config file not found: {config_file}")
        return AgentConfig()

    yaml = YAML()
    yaml.preserve_quotes = True

    try:
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        raise AgentConfigError(
            f"Invalid YAML in {config_file}: {e}"
        ) from e

    agents_data = data.get("agents", )
    if not agents_data:
        logger.info("No agents section in config.yaml")
        return AgentConfig()

    # Parse available agents
    available = agents_data.get("available", [])
    if isinstance(available, str):
        available = [available]
    if not isinstance(available, list):
        raise AgentConfigError(
            "Invalid agents.available in config.yaml: expected a list of agent keys"
        )

    invalid_agents = [agent for agent in available if agent not in AI_CHOICES]
    if invalid_agents:
        valid_agents = ", ".join(sorted(AI_CHOICES.keys()))
        unknown = ", ".join(sorted(invalid_agents))
        raise AgentConfigError(
            f"Unknown agent key(s) in config.yaml: {unknown}. "
            f"Valid agents: {valid_agents}"
        )

    # Parse selection config (legacy strategy field ignored)
    selection_data = agents_data.get("selection", {})
    if not isinstance(selection_data, dict):
        selection_data = {}

    selection = AgentSelectionConfig(
        preferred_implementer=selection_data.get("preferred_implementer"),
        preferred_reviewer=selection_data.get("preferred_reviewer"),
    )

    return AgentConfig(available=available, selection=selection)


def x_load_agent_config__mutmut_29(repo_root: Path) -> AgentConfig:
    """Load agent configuration from .kittify/config.yaml.

    Args:
        repo_root: Repository root directory

    Returns:
        AgentConfig instance (defaults if not configured)
    """
    config_file = repo_root / ".kittify" / "config.yaml"

    if not config_file.exists():
        logger.warning(f"Config file not found: {config_file}")
        return AgentConfig()

    yaml = YAML()
    yaml.preserve_quotes = True

    try:
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        raise AgentConfigError(
            f"Invalid YAML in {config_file}: {e}"
        ) from e

    agents_data = data.get("XXagentsXX", {})
    if not agents_data:
        logger.info("No agents section in config.yaml")
        return AgentConfig()

    # Parse available agents
    available = agents_data.get("available", [])
    if isinstance(available, str):
        available = [available]
    if not isinstance(available, list):
        raise AgentConfigError(
            "Invalid agents.available in config.yaml: expected a list of agent keys"
        )

    invalid_agents = [agent for agent in available if agent not in AI_CHOICES]
    if invalid_agents:
        valid_agents = ", ".join(sorted(AI_CHOICES.keys()))
        unknown = ", ".join(sorted(invalid_agents))
        raise AgentConfigError(
            f"Unknown agent key(s) in config.yaml: {unknown}. "
            f"Valid agents: {valid_agents}"
        )

    # Parse selection config (legacy strategy field ignored)
    selection_data = agents_data.get("selection", {})
    if not isinstance(selection_data, dict):
        selection_data = {}

    selection = AgentSelectionConfig(
        preferred_implementer=selection_data.get("preferred_implementer"),
        preferred_reviewer=selection_data.get("preferred_reviewer"),
    )

    return AgentConfig(available=available, selection=selection)


def x_load_agent_config__mutmut_30(repo_root: Path) -> AgentConfig:
    """Load agent configuration from .kittify/config.yaml.

    Args:
        repo_root: Repository root directory

    Returns:
        AgentConfig instance (defaults if not configured)
    """
    config_file = repo_root / ".kittify" / "config.yaml"

    if not config_file.exists():
        logger.warning(f"Config file not found: {config_file}")
        return AgentConfig()

    yaml = YAML()
    yaml.preserve_quotes = True

    try:
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        raise AgentConfigError(
            f"Invalid YAML in {config_file}: {e}"
        ) from e

    agents_data = data.get("AGENTS", {})
    if not agents_data:
        logger.info("No agents section in config.yaml")
        return AgentConfig()

    # Parse available agents
    available = agents_data.get("available", [])
    if isinstance(available, str):
        available = [available]
    if not isinstance(available, list):
        raise AgentConfigError(
            "Invalid agents.available in config.yaml: expected a list of agent keys"
        )

    invalid_agents = [agent for agent in available if agent not in AI_CHOICES]
    if invalid_agents:
        valid_agents = ", ".join(sorted(AI_CHOICES.keys()))
        unknown = ", ".join(sorted(invalid_agents))
        raise AgentConfigError(
            f"Unknown agent key(s) in config.yaml: {unknown}. "
            f"Valid agents: {valid_agents}"
        )

    # Parse selection config (legacy strategy field ignored)
    selection_data = agents_data.get("selection", {})
    if not isinstance(selection_data, dict):
        selection_data = {}

    selection = AgentSelectionConfig(
        preferred_implementer=selection_data.get("preferred_implementer"),
        preferred_reviewer=selection_data.get("preferred_reviewer"),
    )

    return AgentConfig(available=available, selection=selection)


def x_load_agent_config__mutmut_31(repo_root: Path) -> AgentConfig:
    """Load agent configuration from .kittify/config.yaml.

    Args:
        repo_root: Repository root directory

    Returns:
        AgentConfig instance (defaults if not configured)
    """
    config_file = repo_root / ".kittify" / "config.yaml"

    if not config_file.exists():
        logger.warning(f"Config file not found: {config_file}")
        return AgentConfig()

    yaml = YAML()
    yaml.preserve_quotes = True

    try:
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        raise AgentConfigError(
            f"Invalid YAML in {config_file}: {e}"
        ) from e

    agents_data = data.get("agents", {})
    if agents_data:
        logger.info("No agents section in config.yaml")
        return AgentConfig()

    # Parse available agents
    available = agents_data.get("available", [])
    if isinstance(available, str):
        available = [available]
    if not isinstance(available, list):
        raise AgentConfigError(
            "Invalid agents.available in config.yaml: expected a list of agent keys"
        )

    invalid_agents = [agent for agent in available if agent not in AI_CHOICES]
    if invalid_agents:
        valid_agents = ", ".join(sorted(AI_CHOICES.keys()))
        unknown = ", ".join(sorted(invalid_agents))
        raise AgentConfigError(
            f"Unknown agent key(s) in config.yaml: {unknown}. "
            f"Valid agents: {valid_agents}"
        )

    # Parse selection config (legacy strategy field ignored)
    selection_data = agents_data.get("selection", {})
    if not isinstance(selection_data, dict):
        selection_data = {}

    selection = AgentSelectionConfig(
        preferred_implementer=selection_data.get("preferred_implementer"),
        preferred_reviewer=selection_data.get("preferred_reviewer"),
    )

    return AgentConfig(available=available, selection=selection)


def x_load_agent_config__mutmut_32(repo_root: Path) -> AgentConfig:
    """Load agent configuration from .kittify/config.yaml.

    Args:
        repo_root: Repository root directory

    Returns:
        AgentConfig instance (defaults if not configured)
    """
    config_file = repo_root / ".kittify" / "config.yaml"

    if not config_file.exists():
        logger.warning(f"Config file not found: {config_file}")
        return AgentConfig()

    yaml = YAML()
    yaml.preserve_quotes = True

    try:
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        raise AgentConfigError(
            f"Invalid YAML in {config_file}: {e}"
        ) from e

    agents_data = data.get("agents", {})
    if not agents_data:
        logger.info(None)
        return AgentConfig()

    # Parse available agents
    available = agents_data.get("available", [])
    if isinstance(available, str):
        available = [available]
    if not isinstance(available, list):
        raise AgentConfigError(
            "Invalid agents.available in config.yaml: expected a list of agent keys"
        )

    invalid_agents = [agent for agent in available if agent not in AI_CHOICES]
    if invalid_agents:
        valid_agents = ", ".join(sorted(AI_CHOICES.keys()))
        unknown = ", ".join(sorted(invalid_agents))
        raise AgentConfigError(
            f"Unknown agent key(s) in config.yaml: {unknown}. "
            f"Valid agents: {valid_agents}"
        )

    # Parse selection config (legacy strategy field ignored)
    selection_data = agents_data.get("selection", {})
    if not isinstance(selection_data, dict):
        selection_data = {}

    selection = AgentSelectionConfig(
        preferred_implementer=selection_data.get("preferred_implementer"),
        preferred_reviewer=selection_data.get("preferred_reviewer"),
    )

    return AgentConfig(available=available, selection=selection)


def x_load_agent_config__mutmut_33(repo_root: Path) -> AgentConfig:
    """Load agent configuration from .kittify/config.yaml.

    Args:
        repo_root: Repository root directory

    Returns:
        AgentConfig instance (defaults if not configured)
    """
    config_file = repo_root / ".kittify" / "config.yaml"

    if not config_file.exists():
        logger.warning(f"Config file not found: {config_file}")
        return AgentConfig()

    yaml = YAML()
    yaml.preserve_quotes = True

    try:
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        raise AgentConfigError(
            f"Invalid YAML in {config_file}: {e}"
        ) from e

    agents_data = data.get("agents", {})
    if not agents_data:
        logger.info("XXNo agents section in config.yamlXX")
        return AgentConfig()

    # Parse available agents
    available = agents_data.get("available", [])
    if isinstance(available, str):
        available = [available]
    if not isinstance(available, list):
        raise AgentConfigError(
            "Invalid agents.available in config.yaml: expected a list of agent keys"
        )

    invalid_agents = [agent for agent in available if agent not in AI_CHOICES]
    if invalid_agents:
        valid_agents = ", ".join(sorted(AI_CHOICES.keys()))
        unknown = ", ".join(sorted(invalid_agents))
        raise AgentConfigError(
            f"Unknown agent key(s) in config.yaml: {unknown}. "
            f"Valid agents: {valid_agents}"
        )

    # Parse selection config (legacy strategy field ignored)
    selection_data = agents_data.get("selection", {})
    if not isinstance(selection_data, dict):
        selection_data = {}

    selection = AgentSelectionConfig(
        preferred_implementer=selection_data.get("preferred_implementer"),
        preferred_reviewer=selection_data.get("preferred_reviewer"),
    )

    return AgentConfig(available=available, selection=selection)


def x_load_agent_config__mutmut_34(repo_root: Path) -> AgentConfig:
    """Load agent configuration from .kittify/config.yaml.

    Args:
        repo_root: Repository root directory

    Returns:
        AgentConfig instance (defaults if not configured)
    """
    config_file = repo_root / ".kittify" / "config.yaml"

    if not config_file.exists():
        logger.warning(f"Config file not found: {config_file}")
        return AgentConfig()

    yaml = YAML()
    yaml.preserve_quotes = True

    try:
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        raise AgentConfigError(
            f"Invalid YAML in {config_file}: {e}"
        ) from e

    agents_data = data.get("agents", {})
    if not agents_data:
        logger.info("no agents section in config.yaml")
        return AgentConfig()

    # Parse available agents
    available = agents_data.get("available", [])
    if isinstance(available, str):
        available = [available]
    if not isinstance(available, list):
        raise AgentConfigError(
            "Invalid agents.available in config.yaml: expected a list of agent keys"
        )

    invalid_agents = [agent for agent in available if agent not in AI_CHOICES]
    if invalid_agents:
        valid_agents = ", ".join(sorted(AI_CHOICES.keys()))
        unknown = ", ".join(sorted(invalid_agents))
        raise AgentConfigError(
            f"Unknown agent key(s) in config.yaml: {unknown}. "
            f"Valid agents: {valid_agents}"
        )

    # Parse selection config (legacy strategy field ignored)
    selection_data = agents_data.get("selection", {})
    if not isinstance(selection_data, dict):
        selection_data = {}

    selection = AgentSelectionConfig(
        preferred_implementer=selection_data.get("preferred_implementer"),
        preferred_reviewer=selection_data.get("preferred_reviewer"),
    )

    return AgentConfig(available=available, selection=selection)


def x_load_agent_config__mutmut_35(repo_root: Path) -> AgentConfig:
    """Load agent configuration from .kittify/config.yaml.

    Args:
        repo_root: Repository root directory

    Returns:
        AgentConfig instance (defaults if not configured)
    """
    config_file = repo_root / ".kittify" / "config.yaml"

    if not config_file.exists():
        logger.warning(f"Config file not found: {config_file}")
        return AgentConfig()

    yaml = YAML()
    yaml.preserve_quotes = True

    try:
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        raise AgentConfigError(
            f"Invalid YAML in {config_file}: {e}"
        ) from e

    agents_data = data.get("agents", {})
    if not agents_data:
        logger.info("NO AGENTS SECTION IN CONFIG.YAML")
        return AgentConfig()

    # Parse available agents
    available = agents_data.get("available", [])
    if isinstance(available, str):
        available = [available]
    if not isinstance(available, list):
        raise AgentConfigError(
            "Invalid agents.available in config.yaml: expected a list of agent keys"
        )

    invalid_agents = [agent for agent in available if agent not in AI_CHOICES]
    if invalid_agents:
        valid_agents = ", ".join(sorted(AI_CHOICES.keys()))
        unknown = ", ".join(sorted(invalid_agents))
        raise AgentConfigError(
            f"Unknown agent key(s) in config.yaml: {unknown}. "
            f"Valid agents: {valid_agents}"
        )

    # Parse selection config (legacy strategy field ignored)
    selection_data = agents_data.get("selection", {})
    if not isinstance(selection_data, dict):
        selection_data = {}

    selection = AgentSelectionConfig(
        preferred_implementer=selection_data.get("preferred_implementer"),
        preferred_reviewer=selection_data.get("preferred_reviewer"),
    )

    return AgentConfig(available=available, selection=selection)


def x_load_agent_config__mutmut_36(repo_root: Path) -> AgentConfig:
    """Load agent configuration from .kittify/config.yaml.

    Args:
        repo_root: Repository root directory

    Returns:
        AgentConfig instance (defaults if not configured)
    """
    config_file = repo_root / ".kittify" / "config.yaml"

    if not config_file.exists():
        logger.warning(f"Config file not found: {config_file}")
        return AgentConfig()

    yaml = YAML()
    yaml.preserve_quotes = True

    try:
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        raise AgentConfigError(
            f"Invalid YAML in {config_file}: {e}"
        ) from e

    agents_data = data.get("agents", {})
    if not agents_data:
        logger.info("No agents section in config.yaml")
        return AgentConfig()

    # Parse available agents
    available = None
    if isinstance(available, str):
        available = [available]
    if not isinstance(available, list):
        raise AgentConfigError(
            "Invalid agents.available in config.yaml: expected a list of agent keys"
        )

    invalid_agents = [agent for agent in available if agent not in AI_CHOICES]
    if invalid_agents:
        valid_agents = ", ".join(sorted(AI_CHOICES.keys()))
        unknown = ", ".join(sorted(invalid_agents))
        raise AgentConfigError(
            f"Unknown agent key(s) in config.yaml: {unknown}. "
            f"Valid agents: {valid_agents}"
        )

    # Parse selection config (legacy strategy field ignored)
    selection_data = agents_data.get("selection", {})
    if not isinstance(selection_data, dict):
        selection_data = {}

    selection = AgentSelectionConfig(
        preferred_implementer=selection_data.get("preferred_implementer"),
        preferred_reviewer=selection_data.get("preferred_reviewer"),
    )

    return AgentConfig(available=available, selection=selection)


def x_load_agent_config__mutmut_37(repo_root: Path) -> AgentConfig:
    """Load agent configuration from .kittify/config.yaml.

    Args:
        repo_root: Repository root directory

    Returns:
        AgentConfig instance (defaults if not configured)
    """
    config_file = repo_root / ".kittify" / "config.yaml"

    if not config_file.exists():
        logger.warning(f"Config file not found: {config_file}")
        return AgentConfig()

    yaml = YAML()
    yaml.preserve_quotes = True

    try:
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        raise AgentConfigError(
            f"Invalid YAML in {config_file}: {e}"
        ) from e

    agents_data = data.get("agents", {})
    if not agents_data:
        logger.info("No agents section in config.yaml")
        return AgentConfig()

    # Parse available agents
    available = agents_data.get(None, [])
    if isinstance(available, str):
        available = [available]
    if not isinstance(available, list):
        raise AgentConfigError(
            "Invalid agents.available in config.yaml: expected a list of agent keys"
        )

    invalid_agents = [agent for agent in available if agent not in AI_CHOICES]
    if invalid_agents:
        valid_agents = ", ".join(sorted(AI_CHOICES.keys()))
        unknown = ", ".join(sorted(invalid_agents))
        raise AgentConfigError(
            f"Unknown agent key(s) in config.yaml: {unknown}. "
            f"Valid agents: {valid_agents}"
        )

    # Parse selection config (legacy strategy field ignored)
    selection_data = agents_data.get("selection", {})
    if not isinstance(selection_data, dict):
        selection_data = {}

    selection = AgentSelectionConfig(
        preferred_implementer=selection_data.get("preferred_implementer"),
        preferred_reviewer=selection_data.get("preferred_reviewer"),
    )

    return AgentConfig(available=available, selection=selection)


def x_load_agent_config__mutmut_38(repo_root: Path) -> AgentConfig:
    """Load agent configuration from .kittify/config.yaml.

    Args:
        repo_root: Repository root directory

    Returns:
        AgentConfig instance (defaults if not configured)
    """
    config_file = repo_root / ".kittify" / "config.yaml"

    if not config_file.exists():
        logger.warning(f"Config file not found: {config_file}")
        return AgentConfig()

    yaml = YAML()
    yaml.preserve_quotes = True

    try:
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        raise AgentConfigError(
            f"Invalid YAML in {config_file}: {e}"
        ) from e

    agents_data = data.get("agents", {})
    if not agents_data:
        logger.info("No agents section in config.yaml")
        return AgentConfig()

    # Parse available agents
    available = agents_data.get("available", None)
    if isinstance(available, str):
        available = [available]
    if not isinstance(available, list):
        raise AgentConfigError(
            "Invalid agents.available in config.yaml: expected a list of agent keys"
        )

    invalid_agents = [agent for agent in available if agent not in AI_CHOICES]
    if invalid_agents:
        valid_agents = ", ".join(sorted(AI_CHOICES.keys()))
        unknown = ", ".join(sorted(invalid_agents))
        raise AgentConfigError(
            f"Unknown agent key(s) in config.yaml: {unknown}. "
            f"Valid agents: {valid_agents}"
        )

    # Parse selection config (legacy strategy field ignored)
    selection_data = agents_data.get("selection", {})
    if not isinstance(selection_data, dict):
        selection_data = {}

    selection = AgentSelectionConfig(
        preferred_implementer=selection_data.get("preferred_implementer"),
        preferred_reviewer=selection_data.get("preferred_reviewer"),
    )

    return AgentConfig(available=available, selection=selection)


def x_load_agent_config__mutmut_39(repo_root: Path) -> AgentConfig:
    """Load agent configuration from .kittify/config.yaml.

    Args:
        repo_root: Repository root directory

    Returns:
        AgentConfig instance (defaults if not configured)
    """
    config_file = repo_root / ".kittify" / "config.yaml"

    if not config_file.exists():
        logger.warning(f"Config file not found: {config_file}")
        return AgentConfig()

    yaml = YAML()
    yaml.preserve_quotes = True

    try:
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        raise AgentConfigError(
            f"Invalid YAML in {config_file}: {e}"
        ) from e

    agents_data = data.get("agents", {})
    if not agents_data:
        logger.info("No agents section in config.yaml")
        return AgentConfig()

    # Parse available agents
    available = agents_data.get([])
    if isinstance(available, str):
        available = [available]
    if not isinstance(available, list):
        raise AgentConfigError(
            "Invalid agents.available in config.yaml: expected a list of agent keys"
        )

    invalid_agents = [agent for agent in available if agent not in AI_CHOICES]
    if invalid_agents:
        valid_agents = ", ".join(sorted(AI_CHOICES.keys()))
        unknown = ", ".join(sorted(invalid_agents))
        raise AgentConfigError(
            f"Unknown agent key(s) in config.yaml: {unknown}. "
            f"Valid agents: {valid_agents}"
        )

    # Parse selection config (legacy strategy field ignored)
    selection_data = agents_data.get("selection", {})
    if not isinstance(selection_data, dict):
        selection_data = {}

    selection = AgentSelectionConfig(
        preferred_implementer=selection_data.get("preferred_implementer"),
        preferred_reviewer=selection_data.get("preferred_reviewer"),
    )

    return AgentConfig(available=available, selection=selection)


def x_load_agent_config__mutmut_40(repo_root: Path) -> AgentConfig:
    """Load agent configuration from .kittify/config.yaml.

    Args:
        repo_root: Repository root directory

    Returns:
        AgentConfig instance (defaults if not configured)
    """
    config_file = repo_root / ".kittify" / "config.yaml"

    if not config_file.exists():
        logger.warning(f"Config file not found: {config_file}")
        return AgentConfig()

    yaml = YAML()
    yaml.preserve_quotes = True

    try:
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        raise AgentConfigError(
            f"Invalid YAML in {config_file}: {e}"
        ) from e

    agents_data = data.get("agents", {})
    if not agents_data:
        logger.info("No agents section in config.yaml")
        return AgentConfig()

    # Parse available agents
    available = agents_data.get("available", )
    if isinstance(available, str):
        available = [available]
    if not isinstance(available, list):
        raise AgentConfigError(
            "Invalid agents.available in config.yaml: expected a list of agent keys"
        )

    invalid_agents = [agent for agent in available if agent not in AI_CHOICES]
    if invalid_agents:
        valid_agents = ", ".join(sorted(AI_CHOICES.keys()))
        unknown = ", ".join(sorted(invalid_agents))
        raise AgentConfigError(
            f"Unknown agent key(s) in config.yaml: {unknown}. "
            f"Valid agents: {valid_agents}"
        )

    # Parse selection config (legacy strategy field ignored)
    selection_data = agents_data.get("selection", {})
    if not isinstance(selection_data, dict):
        selection_data = {}

    selection = AgentSelectionConfig(
        preferred_implementer=selection_data.get("preferred_implementer"),
        preferred_reviewer=selection_data.get("preferred_reviewer"),
    )

    return AgentConfig(available=available, selection=selection)


def x_load_agent_config__mutmut_41(repo_root: Path) -> AgentConfig:
    """Load agent configuration from .kittify/config.yaml.

    Args:
        repo_root: Repository root directory

    Returns:
        AgentConfig instance (defaults if not configured)
    """
    config_file = repo_root / ".kittify" / "config.yaml"

    if not config_file.exists():
        logger.warning(f"Config file not found: {config_file}")
        return AgentConfig()

    yaml = YAML()
    yaml.preserve_quotes = True

    try:
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        raise AgentConfigError(
            f"Invalid YAML in {config_file}: {e}"
        ) from e

    agents_data = data.get("agents", {})
    if not agents_data:
        logger.info("No agents section in config.yaml")
        return AgentConfig()

    # Parse available agents
    available = agents_data.get("XXavailableXX", [])
    if isinstance(available, str):
        available = [available]
    if not isinstance(available, list):
        raise AgentConfigError(
            "Invalid agents.available in config.yaml: expected a list of agent keys"
        )

    invalid_agents = [agent for agent in available if agent not in AI_CHOICES]
    if invalid_agents:
        valid_agents = ", ".join(sorted(AI_CHOICES.keys()))
        unknown = ", ".join(sorted(invalid_agents))
        raise AgentConfigError(
            f"Unknown agent key(s) in config.yaml: {unknown}. "
            f"Valid agents: {valid_agents}"
        )

    # Parse selection config (legacy strategy field ignored)
    selection_data = agents_data.get("selection", {})
    if not isinstance(selection_data, dict):
        selection_data = {}

    selection = AgentSelectionConfig(
        preferred_implementer=selection_data.get("preferred_implementer"),
        preferred_reviewer=selection_data.get("preferred_reviewer"),
    )

    return AgentConfig(available=available, selection=selection)


def x_load_agent_config__mutmut_42(repo_root: Path) -> AgentConfig:
    """Load agent configuration from .kittify/config.yaml.

    Args:
        repo_root: Repository root directory

    Returns:
        AgentConfig instance (defaults if not configured)
    """
    config_file = repo_root / ".kittify" / "config.yaml"

    if not config_file.exists():
        logger.warning(f"Config file not found: {config_file}")
        return AgentConfig()

    yaml = YAML()
    yaml.preserve_quotes = True

    try:
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        raise AgentConfigError(
            f"Invalid YAML in {config_file}: {e}"
        ) from e

    agents_data = data.get("agents", {})
    if not agents_data:
        logger.info("No agents section in config.yaml")
        return AgentConfig()

    # Parse available agents
    available = agents_data.get("AVAILABLE", [])
    if isinstance(available, str):
        available = [available]
    if not isinstance(available, list):
        raise AgentConfigError(
            "Invalid agents.available in config.yaml: expected a list of agent keys"
        )

    invalid_agents = [agent for agent in available if agent not in AI_CHOICES]
    if invalid_agents:
        valid_agents = ", ".join(sorted(AI_CHOICES.keys()))
        unknown = ", ".join(sorted(invalid_agents))
        raise AgentConfigError(
            f"Unknown agent key(s) in config.yaml: {unknown}. "
            f"Valid agents: {valid_agents}"
        )

    # Parse selection config (legacy strategy field ignored)
    selection_data = agents_data.get("selection", {})
    if not isinstance(selection_data, dict):
        selection_data = {}

    selection = AgentSelectionConfig(
        preferred_implementer=selection_data.get("preferred_implementer"),
        preferred_reviewer=selection_data.get("preferred_reviewer"),
    )

    return AgentConfig(available=available, selection=selection)


def x_load_agent_config__mutmut_43(repo_root: Path) -> AgentConfig:
    """Load agent configuration from .kittify/config.yaml.

    Args:
        repo_root: Repository root directory

    Returns:
        AgentConfig instance (defaults if not configured)
    """
    config_file = repo_root / ".kittify" / "config.yaml"

    if not config_file.exists():
        logger.warning(f"Config file not found: {config_file}")
        return AgentConfig()

    yaml = YAML()
    yaml.preserve_quotes = True

    try:
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        raise AgentConfigError(
            f"Invalid YAML in {config_file}: {e}"
        ) from e

    agents_data = data.get("agents", {})
    if not agents_data:
        logger.info("No agents section in config.yaml")
        return AgentConfig()

    # Parse available agents
    available = agents_data.get("available", [])
    if isinstance(available, str):
        available = None
    if not isinstance(available, list):
        raise AgentConfigError(
            "Invalid agents.available in config.yaml: expected a list of agent keys"
        )

    invalid_agents = [agent for agent in available if agent not in AI_CHOICES]
    if invalid_agents:
        valid_agents = ", ".join(sorted(AI_CHOICES.keys()))
        unknown = ", ".join(sorted(invalid_agents))
        raise AgentConfigError(
            f"Unknown agent key(s) in config.yaml: {unknown}. "
            f"Valid agents: {valid_agents}"
        )

    # Parse selection config (legacy strategy field ignored)
    selection_data = agents_data.get("selection", {})
    if not isinstance(selection_data, dict):
        selection_data = {}

    selection = AgentSelectionConfig(
        preferred_implementer=selection_data.get("preferred_implementer"),
        preferred_reviewer=selection_data.get("preferred_reviewer"),
    )

    return AgentConfig(available=available, selection=selection)


def x_load_agent_config__mutmut_44(repo_root: Path) -> AgentConfig:
    """Load agent configuration from .kittify/config.yaml.

    Args:
        repo_root: Repository root directory

    Returns:
        AgentConfig instance (defaults if not configured)
    """
    config_file = repo_root / ".kittify" / "config.yaml"

    if not config_file.exists():
        logger.warning(f"Config file not found: {config_file}")
        return AgentConfig()

    yaml = YAML()
    yaml.preserve_quotes = True

    try:
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        raise AgentConfigError(
            f"Invalid YAML in {config_file}: {e}"
        ) from e

    agents_data = data.get("agents", {})
    if not agents_data:
        logger.info("No agents section in config.yaml")
        return AgentConfig()

    # Parse available agents
    available = agents_data.get("available", [])
    if isinstance(available, str):
        available = [available]
    if isinstance(available, list):
        raise AgentConfigError(
            "Invalid agents.available in config.yaml: expected a list of agent keys"
        )

    invalid_agents = [agent for agent in available if agent not in AI_CHOICES]
    if invalid_agents:
        valid_agents = ", ".join(sorted(AI_CHOICES.keys()))
        unknown = ", ".join(sorted(invalid_agents))
        raise AgentConfigError(
            f"Unknown agent key(s) in config.yaml: {unknown}. "
            f"Valid agents: {valid_agents}"
        )

    # Parse selection config (legacy strategy field ignored)
    selection_data = agents_data.get("selection", {})
    if not isinstance(selection_data, dict):
        selection_data = {}

    selection = AgentSelectionConfig(
        preferred_implementer=selection_data.get("preferred_implementer"),
        preferred_reviewer=selection_data.get("preferred_reviewer"),
    )

    return AgentConfig(available=available, selection=selection)


def x_load_agent_config__mutmut_45(repo_root: Path) -> AgentConfig:
    """Load agent configuration from .kittify/config.yaml.

    Args:
        repo_root: Repository root directory

    Returns:
        AgentConfig instance (defaults if not configured)
    """
    config_file = repo_root / ".kittify" / "config.yaml"

    if not config_file.exists():
        logger.warning(f"Config file not found: {config_file}")
        return AgentConfig()

    yaml = YAML()
    yaml.preserve_quotes = True

    try:
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        raise AgentConfigError(
            f"Invalid YAML in {config_file}: {e}"
        ) from e

    agents_data = data.get("agents", {})
    if not agents_data:
        logger.info("No agents section in config.yaml")
        return AgentConfig()

    # Parse available agents
    available = agents_data.get("available", [])
    if isinstance(available, str):
        available = [available]
    if not isinstance(available, list):
        raise AgentConfigError(
            None
        )

    invalid_agents = [agent for agent in available if agent not in AI_CHOICES]
    if invalid_agents:
        valid_agents = ", ".join(sorted(AI_CHOICES.keys()))
        unknown = ", ".join(sorted(invalid_agents))
        raise AgentConfigError(
            f"Unknown agent key(s) in config.yaml: {unknown}. "
            f"Valid agents: {valid_agents}"
        )

    # Parse selection config (legacy strategy field ignored)
    selection_data = agents_data.get("selection", {})
    if not isinstance(selection_data, dict):
        selection_data = {}

    selection = AgentSelectionConfig(
        preferred_implementer=selection_data.get("preferred_implementer"),
        preferred_reviewer=selection_data.get("preferred_reviewer"),
    )

    return AgentConfig(available=available, selection=selection)


def x_load_agent_config__mutmut_46(repo_root: Path) -> AgentConfig:
    """Load agent configuration from .kittify/config.yaml.

    Args:
        repo_root: Repository root directory

    Returns:
        AgentConfig instance (defaults if not configured)
    """
    config_file = repo_root / ".kittify" / "config.yaml"

    if not config_file.exists():
        logger.warning(f"Config file not found: {config_file}")
        return AgentConfig()

    yaml = YAML()
    yaml.preserve_quotes = True

    try:
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        raise AgentConfigError(
            f"Invalid YAML in {config_file}: {e}"
        ) from e

    agents_data = data.get("agents", {})
    if not agents_data:
        logger.info("No agents section in config.yaml")
        return AgentConfig()

    # Parse available agents
    available = agents_data.get("available", [])
    if isinstance(available, str):
        available = [available]
    if not isinstance(available, list):
        raise AgentConfigError(
            "XXInvalid agents.available in config.yaml: expected a list of agent keysXX"
        )

    invalid_agents = [agent for agent in available if agent not in AI_CHOICES]
    if invalid_agents:
        valid_agents = ", ".join(sorted(AI_CHOICES.keys()))
        unknown = ", ".join(sorted(invalid_agents))
        raise AgentConfigError(
            f"Unknown agent key(s) in config.yaml: {unknown}. "
            f"Valid agents: {valid_agents}"
        )

    # Parse selection config (legacy strategy field ignored)
    selection_data = agents_data.get("selection", {})
    if not isinstance(selection_data, dict):
        selection_data = {}

    selection = AgentSelectionConfig(
        preferred_implementer=selection_data.get("preferred_implementer"),
        preferred_reviewer=selection_data.get("preferred_reviewer"),
    )

    return AgentConfig(available=available, selection=selection)


def x_load_agent_config__mutmut_47(repo_root: Path) -> AgentConfig:
    """Load agent configuration from .kittify/config.yaml.

    Args:
        repo_root: Repository root directory

    Returns:
        AgentConfig instance (defaults if not configured)
    """
    config_file = repo_root / ".kittify" / "config.yaml"

    if not config_file.exists():
        logger.warning(f"Config file not found: {config_file}")
        return AgentConfig()

    yaml = YAML()
    yaml.preserve_quotes = True

    try:
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        raise AgentConfigError(
            f"Invalid YAML in {config_file}: {e}"
        ) from e

    agents_data = data.get("agents", {})
    if not agents_data:
        logger.info("No agents section in config.yaml")
        return AgentConfig()

    # Parse available agents
    available = agents_data.get("available", [])
    if isinstance(available, str):
        available = [available]
    if not isinstance(available, list):
        raise AgentConfigError(
            "invalid agents.available in config.yaml: expected a list of agent keys"
        )

    invalid_agents = [agent for agent in available if agent not in AI_CHOICES]
    if invalid_agents:
        valid_agents = ", ".join(sorted(AI_CHOICES.keys()))
        unknown = ", ".join(sorted(invalid_agents))
        raise AgentConfigError(
            f"Unknown agent key(s) in config.yaml: {unknown}. "
            f"Valid agents: {valid_agents}"
        )

    # Parse selection config (legacy strategy field ignored)
    selection_data = agents_data.get("selection", {})
    if not isinstance(selection_data, dict):
        selection_data = {}

    selection = AgentSelectionConfig(
        preferred_implementer=selection_data.get("preferred_implementer"),
        preferred_reviewer=selection_data.get("preferred_reviewer"),
    )

    return AgentConfig(available=available, selection=selection)


def x_load_agent_config__mutmut_48(repo_root: Path) -> AgentConfig:
    """Load agent configuration from .kittify/config.yaml.

    Args:
        repo_root: Repository root directory

    Returns:
        AgentConfig instance (defaults if not configured)
    """
    config_file = repo_root / ".kittify" / "config.yaml"

    if not config_file.exists():
        logger.warning(f"Config file not found: {config_file}")
        return AgentConfig()

    yaml = YAML()
    yaml.preserve_quotes = True

    try:
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        raise AgentConfigError(
            f"Invalid YAML in {config_file}: {e}"
        ) from e

    agents_data = data.get("agents", {})
    if not agents_data:
        logger.info("No agents section in config.yaml")
        return AgentConfig()

    # Parse available agents
    available = agents_data.get("available", [])
    if isinstance(available, str):
        available = [available]
    if not isinstance(available, list):
        raise AgentConfigError(
            "INVALID AGENTS.AVAILABLE IN CONFIG.YAML: EXPECTED A LIST OF AGENT KEYS"
        )

    invalid_agents = [agent for agent in available if agent not in AI_CHOICES]
    if invalid_agents:
        valid_agents = ", ".join(sorted(AI_CHOICES.keys()))
        unknown = ", ".join(sorted(invalid_agents))
        raise AgentConfigError(
            f"Unknown agent key(s) in config.yaml: {unknown}. "
            f"Valid agents: {valid_agents}"
        )

    # Parse selection config (legacy strategy field ignored)
    selection_data = agents_data.get("selection", {})
    if not isinstance(selection_data, dict):
        selection_data = {}

    selection = AgentSelectionConfig(
        preferred_implementer=selection_data.get("preferred_implementer"),
        preferred_reviewer=selection_data.get("preferred_reviewer"),
    )

    return AgentConfig(available=available, selection=selection)


def x_load_agent_config__mutmut_49(repo_root: Path) -> AgentConfig:
    """Load agent configuration from .kittify/config.yaml.

    Args:
        repo_root: Repository root directory

    Returns:
        AgentConfig instance (defaults if not configured)
    """
    config_file = repo_root / ".kittify" / "config.yaml"

    if not config_file.exists():
        logger.warning(f"Config file not found: {config_file}")
        return AgentConfig()

    yaml = YAML()
    yaml.preserve_quotes = True

    try:
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        raise AgentConfigError(
            f"Invalid YAML in {config_file}: {e}"
        ) from e

    agents_data = data.get("agents", {})
    if not agents_data:
        logger.info("No agents section in config.yaml")
        return AgentConfig()

    # Parse available agents
    available = agents_data.get("available", [])
    if isinstance(available, str):
        available = [available]
    if not isinstance(available, list):
        raise AgentConfigError(
            "Invalid agents.available in config.yaml: expected a list of agent keys"
        )

    invalid_agents = None
    if invalid_agents:
        valid_agents = ", ".join(sorted(AI_CHOICES.keys()))
        unknown = ", ".join(sorted(invalid_agents))
        raise AgentConfigError(
            f"Unknown agent key(s) in config.yaml: {unknown}. "
            f"Valid agents: {valid_agents}"
        )

    # Parse selection config (legacy strategy field ignored)
    selection_data = agents_data.get("selection", {})
    if not isinstance(selection_data, dict):
        selection_data = {}

    selection = AgentSelectionConfig(
        preferred_implementer=selection_data.get("preferred_implementer"),
        preferred_reviewer=selection_data.get("preferred_reviewer"),
    )

    return AgentConfig(available=available, selection=selection)


def x_load_agent_config__mutmut_50(repo_root: Path) -> AgentConfig:
    """Load agent configuration from .kittify/config.yaml.

    Args:
        repo_root: Repository root directory

    Returns:
        AgentConfig instance (defaults if not configured)
    """
    config_file = repo_root / ".kittify" / "config.yaml"

    if not config_file.exists():
        logger.warning(f"Config file not found: {config_file}")
        return AgentConfig()

    yaml = YAML()
    yaml.preserve_quotes = True

    try:
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        raise AgentConfigError(
            f"Invalid YAML in {config_file}: {e}"
        ) from e

    agents_data = data.get("agents", {})
    if not agents_data:
        logger.info("No agents section in config.yaml")
        return AgentConfig()

    # Parse available agents
    available = agents_data.get("available", [])
    if isinstance(available, str):
        available = [available]
    if not isinstance(available, list):
        raise AgentConfigError(
            "Invalid agents.available in config.yaml: expected a list of agent keys"
        )

    invalid_agents = [agent for agent in available if agent in AI_CHOICES]
    if invalid_agents:
        valid_agents = ", ".join(sorted(AI_CHOICES.keys()))
        unknown = ", ".join(sorted(invalid_agents))
        raise AgentConfigError(
            f"Unknown agent key(s) in config.yaml: {unknown}. "
            f"Valid agents: {valid_agents}"
        )

    # Parse selection config (legacy strategy field ignored)
    selection_data = agents_data.get("selection", {})
    if not isinstance(selection_data, dict):
        selection_data = {}

    selection = AgentSelectionConfig(
        preferred_implementer=selection_data.get("preferred_implementer"),
        preferred_reviewer=selection_data.get("preferred_reviewer"),
    )

    return AgentConfig(available=available, selection=selection)


def x_load_agent_config__mutmut_51(repo_root: Path) -> AgentConfig:
    """Load agent configuration from .kittify/config.yaml.

    Args:
        repo_root: Repository root directory

    Returns:
        AgentConfig instance (defaults if not configured)
    """
    config_file = repo_root / ".kittify" / "config.yaml"

    if not config_file.exists():
        logger.warning(f"Config file not found: {config_file}")
        return AgentConfig()

    yaml = YAML()
    yaml.preserve_quotes = True

    try:
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        raise AgentConfigError(
            f"Invalid YAML in {config_file}: {e}"
        ) from e

    agents_data = data.get("agents", {})
    if not agents_data:
        logger.info("No agents section in config.yaml")
        return AgentConfig()

    # Parse available agents
    available = agents_data.get("available", [])
    if isinstance(available, str):
        available = [available]
    if not isinstance(available, list):
        raise AgentConfigError(
            "Invalid agents.available in config.yaml: expected a list of agent keys"
        )

    invalid_agents = [agent for agent in available if agent not in AI_CHOICES]
    if invalid_agents:
        valid_agents = None
        unknown = ", ".join(sorted(invalid_agents))
        raise AgentConfigError(
            f"Unknown agent key(s) in config.yaml: {unknown}. "
            f"Valid agents: {valid_agents}"
        )

    # Parse selection config (legacy strategy field ignored)
    selection_data = agents_data.get("selection", {})
    if not isinstance(selection_data, dict):
        selection_data = {}

    selection = AgentSelectionConfig(
        preferred_implementer=selection_data.get("preferred_implementer"),
        preferred_reviewer=selection_data.get("preferred_reviewer"),
    )

    return AgentConfig(available=available, selection=selection)


def x_load_agent_config__mutmut_52(repo_root: Path) -> AgentConfig:
    """Load agent configuration from .kittify/config.yaml.

    Args:
        repo_root: Repository root directory

    Returns:
        AgentConfig instance (defaults if not configured)
    """
    config_file = repo_root / ".kittify" / "config.yaml"

    if not config_file.exists():
        logger.warning(f"Config file not found: {config_file}")
        return AgentConfig()

    yaml = YAML()
    yaml.preserve_quotes = True

    try:
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        raise AgentConfigError(
            f"Invalid YAML in {config_file}: {e}"
        ) from e

    agents_data = data.get("agents", {})
    if not agents_data:
        logger.info("No agents section in config.yaml")
        return AgentConfig()

    # Parse available agents
    available = agents_data.get("available", [])
    if isinstance(available, str):
        available = [available]
    if not isinstance(available, list):
        raise AgentConfigError(
            "Invalid agents.available in config.yaml: expected a list of agent keys"
        )

    invalid_agents = [agent for agent in available if agent not in AI_CHOICES]
    if invalid_agents:
        valid_agents = ", ".join(None)
        unknown = ", ".join(sorted(invalid_agents))
        raise AgentConfigError(
            f"Unknown agent key(s) in config.yaml: {unknown}. "
            f"Valid agents: {valid_agents}"
        )

    # Parse selection config (legacy strategy field ignored)
    selection_data = agents_data.get("selection", {})
    if not isinstance(selection_data, dict):
        selection_data = {}

    selection = AgentSelectionConfig(
        preferred_implementer=selection_data.get("preferred_implementer"),
        preferred_reviewer=selection_data.get("preferred_reviewer"),
    )

    return AgentConfig(available=available, selection=selection)


def x_load_agent_config__mutmut_53(repo_root: Path) -> AgentConfig:
    """Load agent configuration from .kittify/config.yaml.

    Args:
        repo_root: Repository root directory

    Returns:
        AgentConfig instance (defaults if not configured)
    """
    config_file = repo_root / ".kittify" / "config.yaml"

    if not config_file.exists():
        logger.warning(f"Config file not found: {config_file}")
        return AgentConfig()

    yaml = YAML()
    yaml.preserve_quotes = True

    try:
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        raise AgentConfigError(
            f"Invalid YAML in {config_file}: {e}"
        ) from e

    agents_data = data.get("agents", {})
    if not agents_data:
        logger.info("No agents section in config.yaml")
        return AgentConfig()

    # Parse available agents
    available = agents_data.get("available", [])
    if isinstance(available, str):
        available = [available]
    if not isinstance(available, list):
        raise AgentConfigError(
            "Invalid agents.available in config.yaml: expected a list of agent keys"
        )

    invalid_agents = [agent for agent in available if agent not in AI_CHOICES]
    if invalid_agents:
        valid_agents = "XX, XX".join(sorted(AI_CHOICES.keys()))
        unknown = ", ".join(sorted(invalid_agents))
        raise AgentConfigError(
            f"Unknown agent key(s) in config.yaml: {unknown}. "
            f"Valid agents: {valid_agents}"
        )

    # Parse selection config (legacy strategy field ignored)
    selection_data = agents_data.get("selection", {})
    if not isinstance(selection_data, dict):
        selection_data = {}

    selection = AgentSelectionConfig(
        preferred_implementer=selection_data.get("preferred_implementer"),
        preferred_reviewer=selection_data.get("preferred_reviewer"),
    )

    return AgentConfig(available=available, selection=selection)


def x_load_agent_config__mutmut_54(repo_root: Path) -> AgentConfig:
    """Load agent configuration from .kittify/config.yaml.

    Args:
        repo_root: Repository root directory

    Returns:
        AgentConfig instance (defaults if not configured)
    """
    config_file = repo_root / ".kittify" / "config.yaml"

    if not config_file.exists():
        logger.warning(f"Config file not found: {config_file}")
        return AgentConfig()

    yaml = YAML()
    yaml.preserve_quotes = True

    try:
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        raise AgentConfigError(
            f"Invalid YAML in {config_file}: {e}"
        ) from e

    agents_data = data.get("agents", {})
    if not agents_data:
        logger.info("No agents section in config.yaml")
        return AgentConfig()

    # Parse available agents
    available = agents_data.get("available", [])
    if isinstance(available, str):
        available = [available]
    if not isinstance(available, list):
        raise AgentConfigError(
            "Invalid agents.available in config.yaml: expected a list of agent keys"
        )

    invalid_agents = [agent for agent in available if agent not in AI_CHOICES]
    if invalid_agents:
        valid_agents = ", ".join(sorted(None))
        unknown = ", ".join(sorted(invalid_agents))
        raise AgentConfigError(
            f"Unknown agent key(s) in config.yaml: {unknown}. "
            f"Valid agents: {valid_agents}"
        )

    # Parse selection config (legacy strategy field ignored)
    selection_data = agents_data.get("selection", {})
    if not isinstance(selection_data, dict):
        selection_data = {}

    selection = AgentSelectionConfig(
        preferred_implementer=selection_data.get("preferred_implementer"),
        preferred_reviewer=selection_data.get("preferred_reviewer"),
    )

    return AgentConfig(available=available, selection=selection)


def x_load_agent_config__mutmut_55(repo_root: Path) -> AgentConfig:
    """Load agent configuration from .kittify/config.yaml.

    Args:
        repo_root: Repository root directory

    Returns:
        AgentConfig instance (defaults if not configured)
    """
    config_file = repo_root / ".kittify" / "config.yaml"

    if not config_file.exists():
        logger.warning(f"Config file not found: {config_file}")
        return AgentConfig()

    yaml = YAML()
    yaml.preserve_quotes = True

    try:
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        raise AgentConfigError(
            f"Invalid YAML in {config_file}: {e}"
        ) from e

    agents_data = data.get("agents", {})
    if not agents_data:
        logger.info("No agents section in config.yaml")
        return AgentConfig()

    # Parse available agents
    available = agents_data.get("available", [])
    if isinstance(available, str):
        available = [available]
    if not isinstance(available, list):
        raise AgentConfigError(
            "Invalid agents.available in config.yaml: expected a list of agent keys"
        )

    invalid_agents = [agent for agent in available if agent not in AI_CHOICES]
    if invalid_agents:
        valid_agents = ", ".join(sorted(AI_CHOICES.keys()))
        unknown = None
        raise AgentConfigError(
            f"Unknown agent key(s) in config.yaml: {unknown}. "
            f"Valid agents: {valid_agents}"
        )

    # Parse selection config (legacy strategy field ignored)
    selection_data = agents_data.get("selection", {})
    if not isinstance(selection_data, dict):
        selection_data = {}

    selection = AgentSelectionConfig(
        preferred_implementer=selection_data.get("preferred_implementer"),
        preferred_reviewer=selection_data.get("preferred_reviewer"),
    )

    return AgentConfig(available=available, selection=selection)


def x_load_agent_config__mutmut_56(repo_root: Path) -> AgentConfig:
    """Load agent configuration from .kittify/config.yaml.

    Args:
        repo_root: Repository root directory

    Returns:
        AgentConfig instance (defaults if not configured)
    """
    config_file = repo_root / ".kittify" / "config.yaml"

    if not config_file.exists():
        logger.warning(f"Config file not found: {config_file}")
        return AgentConfig()

    yaml = YAML()
    yaml.preserve_quotes = True

    try:
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        raise AgentConfigError(
            f"Invalid YAML in {config_file}: {e}"
        ) from e

    agents_data = data.get("agents", {})
    if not agents_data:
        logger.info("No agents section in config.yaml")
        return AgentConfig()

    # Parse available agents
    available = agents_data.get("available", [])
    if isinstance(available, str):
        available = [available]
    if not isinstance(available, list):
        raise AgentConfigError(
            "Invalid agents.available in config.yaml: expected a list of agent keys"
        )

    invalid_agents = [agent for agent in available if agent not in AI_CHOICES]
    if invalid_agents:
        valid_agents = ", ".join(sorted(AI_CHOICES.keys()))
        unknown = ", ".join(None)
        raise AgentConfigError(
            f"Unknown agent key(s) in config.yaml: {unknown}. "
            f"Valid agents: {valid_agents}"
        )

    # Parse selection config (legacy strategy field ignored)
    selection_data = agents_data.get("selection", {})
    if not isinstance(selection_data, dict):
        selection_data = {}

    selection = AgentSelectionConfig(
        preferred_implementer=selection_data.get("preferred_implementer"),
        preferred_reviewer=selection_data.get("preferred_reviewer"),
    )

    return AgentConfig(available=available, selection=selection)


def x_load_agent_config__mutmut_57(repo_root: Path) -> AgentConfig:
    """Load agent configuration from .kittify/config.yaml.

    Args:
        repo_root: Repository root directory

    Returns:
        AgentConfig instance (defaults if not configured)
    """
    config_file = repo_root / ".kittify" / "config.yaml"

    if not config_file.exists():
        logger.warning(f"Config file not found: {config_file}")
        return AgentConfig()

    yaml = YAML()
    yaml.preserve_quotes = True

    try:
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        raise AgentConfigError(
            f"Invalid YAML in {config_file}: {e}"
        ) from e

    agents_data = data.get("agents", {})
    if not agents_data:
        logger.info("No agents section in config.yaml")
        return AgentConfig()

    # Parse available agents
    available = agents_data.get("available", [])
    if isinstance(available, str):
        available = [available]
    if not isinstance(available, list):
        raise AgentConfigError(
            "Invalid agents.available in config.yaml: expected a list of agent keys"
        )

    invalid_agents = [agent for agent in available if agent not in AI_CHOICES]
    if invalid_agents:
        valid_agents = ", ".join(sorted(AI_CHOICES.keys()))
        unknown = "XX, XX".join(sorted(invalid_agents))
        raise AgentConfigError(
            f"Unknown agent key(s) in config.yaml: {unknown}. "
            f"Valid agents: {valid_agents}"
        )

    # Parse selection config (legacy strategy field ignored)
    selection_data = agents_data.get("selection", {})
    if not isinstance(selection_data, dict):
        selection_data = {}

    selection = AgentSelectionConfig(
        preferred_implementer=selection_data.get("preferred_implementer"),
        preferred_reviewer=selection_data.get("preferred_reviewer"),
    )

    return AgentConfig(available=available, selection=selection)


def x_load_agent_config__mutmut_58(repo_root: Path) -> AgentConfig:
    """Load agent configuration from .kittify/config.yaml.

    Args:
        repo_root: Repository root directory

    Returns:
        AgentConfig instance (defaults if not configured)
    """
    config_file = repo_root / ".kittify" / "config.yaml"

    if not config_file.exists():
        logger.warning(f"Config file not found: {config_file}")
        return AgentConfig()

    yaml = YAML()
    yaml.preserve_quotes = True

    try:
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        raise AgentConfigError(
            f"Invalid YAML in {config_file}: {e}"
        ) from e

    agents_data = data.get("agents", {})
    if not agents_data:
        logger.info("No agents section in config.yaml")
        return AgentConfig()

    # Parse available agents
    available = agents_data.get("available", [])
    if isinstance(available, str):
        available = [available]
    if not isinstance(available, list):
        raise AgentConfigError(
            "Invalid agents.available in config.yaml: expected a list of agent keys"
        )

    invalid_agents = [agent for agent in available if agent not in AI_CHOICES]
    if invalid_agents:
        valid_agents = ", ".join(sorted(AI_CHOICES.keys()))
        unknown = ", ".join(sorted(None))
        raise AgentConfigError(
            f"Unknown agent key(s) in config.yaml: {unknown}. "
            f"Valid agents: {valid_agents}"
        )

    # Parse selection config (legacy strategy field ignored)
    selection_data = agents_data.get("selection", {})
    if not isinstance(selection_data, dict):
        selection_data = {}

    selection = AgentSelectionConfig(
        preferred_implementer=selection_data.get("preferred_implementer"),
        preferred_reviewer=selection_data.get("preferred_reviewer"),
    )

    return AgentConfig(available=available, selection=selection)


def x_load_agent_config__mutmut_59(repo_root: Path) -> AgentConfig:
    """Load agent configuration from .kittify/config.yaml.

    Args:
        repo_root: Repository root directory

    Returns:
        AgentConfig instance (defaults if not configured)
    """
    config_file = repo_root / ".kittify" / "config.yaml"

    if not config_file.exists():
        logger.warning(f"Config file not found: {config_file}")
        return AgentConfig()

    yaml = YAML()
    yaml.preserve_quotes = True

    try:
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        raise AgentConfigError(
            f"Invalid YAML in {config_file}: {e}"
        ) from e

    agents_data = data.get("agents", {})
    if not agents_data:
        logger.info("No agents section in config.yaml")
        return AgentConfig()

    # Parse available agents
    available = agents_data.get("available", [])
    if isinstance(available, str):
        available = [available]
    if not isinstance(available, list):
        raise AgentConfigError(
            "Invalid agents.available in config.yaml: expected a list of agent keys"
        )

    invalid_agents = [agent for agent in available if agent not in AI_CHOICES]
    if invalid_agents:
        valid_agents = ", ".join(sorted(AI_CHOICES.keys()))
        unknown = ", ".join(sorted(invalid_agents))
        raise AgentConfigError(
            None
        )

    # Parse selection config (legacy strategy field ignored)
    selection_data = agents_data.get("selection", {})
    if not isinstance(selection_data, dict):
        selection_data = {}

    selection = AgentSelectionConfig(
        preferred_implementer=selection_data.get("preferred_implementer"),
        preferred_reviewer=selection_data.get("preferred_reviewer"),
    )

    return AgentConfig(available=available, selection=selection)


def x_load_agent_config__mutmut_60(repo_root: Path) -> AgentConfig:
    """Load agent configuration from .kittify/config.yaml.

    Args:
        repo_root: Repository root directory

    Returns:
        AgentConfig instance (defaults if not configured)
    """
    config_file = repo_root / ".kittify" / "config.yaml"

    if not config_file.exists():
        logger.warning(f"Config file not found: {config_file}")
        return AgentConfig()

    yaml = YAML()
    yaml.preserve_quotes = True

    try:
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        raise AgentConfigError(
            f"Invalid YAML in {config_file}: {e}"
        ) from e

    agents_data = data.get("agents", {})
    if not agents_data:
        logger.info("No agents section in config.yaml")
        return AgentConfig()

    # Parse available agents
    available = agents_data.get("available", [])
    if isinstance(available, str):
        available = [available]
    if not isinstance(available, list):
        raise AgentConfigError(
            "Invalid agents.available in config.yaml: expected a list of agent keys"
        )

    invalid_agents = [agent for agent in available if agent not in AI_CHOICES]
    if invalid_agents:
        valid_agents = ", ".join(sorted(AI_CHOICES.keys()))
        unknown = ", ".join(sorted(invalid_agents))
        raise AgentConfigError(
            f"Unknown agent key(s) in config.yaml: {unknown}. "
            f"Valid agents: {valid_agents}"
        )

    # Parse selection config (legacy strategy field ignored)
    selection_data = None
    if not isinstance(selection_data, dict):
        selection_data = {}

    selection = AgentSelectionConfig(
        preferred_implementer=selection_data.get("preferred_implementer"),
        preferred_reviewer=selection_data.get("preferred_reviewer"),
    )

    return AgentConfig(available=available, selection=selection)


def x_load_agent_config__mutmut_61(repo_root: Path) -> AgentConfig:
    """Load agent configuration from .kittify/config.yaml.

    Args:
        repo_root: Repository root directory

    Returns:
        AgentConfig instance (defaults if not configured)
    """
    config_file = repo_root / ".kittify" / "config.yaml"

    if not config_file.exists():
        logger.warning(f"Config file not found: {config_file}")
        return AgentConfig()

    yaml = YAML()
    yaml.preserve_quotes = True

    try:
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        raise AgentConfigError(
            f"Invalid YAML in {config_file}: {e}"
        ) from e

    agents_data = data.get("agents", {})
    if not agents_data:
        logger.info("No agents section in config.yaml")
        return AgentConfig()

    # Parse available agents
    available = agents_data.get("available", [])
    if isinstance(available, str):
        available = [available]
    if not isinstance(available, list):
        raise AgentConfigError(
            "Invalid agents.available in config.yaml: expected a list of agent keys"
        )

    invalid_agents = [agent for agent in available if agent not in AI_CHOICES]
    if invalid_agents:
        valid_agents = ", ".join(sorted(AI_CHOICES.keys()))
        unknown = ", ".join(sorted(invalid_agents))
        raise AgentConfigError(
            f"Unknown agent key(s) in config.yaml: {unknown}. "
            f"Valid agents: {valid_agents}"
        )

    # Parse selection config (legacy strategy field ignored)
    selection_data = agents_data.get(None, {})
    if not isinstance(selection_data, dict):
        selection_data = {}

    selection = AgentSelectionConfig(
        preferred_implementer=selection_data.get("preferred_implementer"),
        preferred_reviewer=selection_data.get("preferred_reviewer"),
    )

    return AgentConfig(available=available, selection=selection)


def x_load_agent_config__mutmut_62(repo_root: Path) -> AgentConfig:
    """Load agent configuration from .kittify/config.yaml.

    Args:
        repo_root: Repository root directory

    Returns:
        AgentConfig instance (defaults if not configured)
    """
    config_file = repo_root / ".kittify" / "config.yaml"

    if not config_file.exists():
        logger.warning(f"Config file not found: {config_file}")
        return AgentConfig()

    yaml = YAML()
    yaml.preserve_quotes = True

    try:
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        raise AgentConfigError(
            f"Invalid YAML in {config_file}: {e}"
        ) from e

    agents_data = data.get("agents", {})
    if not agents_data:
        logger.info("No agents section in config.yaml")
        return AgentConfig()

    # Parse available agents
    available = agents_data.get("available", [])
    if isinstance(available, str):
        available = [available]
    if not isinstance(available, list):
        raise AgentConfigError(
            "Invalid agents.available in config.yaml: expected a list of agent keys"
        )

    invalid_agents = [agent for agent in available if agent not in AI_CHOICES]
    if invalid_agents:
        valid_agents = ", ".join(sorted(AI_CHOICES.keys()))
        unknown = ", ".join(sorted(invalid_agents))
        raise AgentConfigError(
            f"Unknown agent key(s) in config.yaml: {unknown}. "
            f"Valid agents: {valid_agents}"
        )

    # Parse selection config (legacy strategy field ignored)
    selection_data = agents_data.get("selection", None)
    if not isinstance(selection_data, dict):
        selection_data = {}

    selection = AgentSelectionConfig(
        preferred_implementer=selection_data.get("preferred_implementer"),
        preferred_reviewer=selection_data.get("preferred_reviewer"),
    )

    return AgentConfig(available=available, selection=selection)


def x_load_agent_config__mutmut_63(repo_root: Path) -> AgentConfig:
    """Load agent configuration from .kittify/config.yaml.

    Args:
        repo_root: Repository root directory

    Returns:
        AgentConfig instance (defaults if not configured)
    """
    config_file = repo_root / ".kittify" / "config.yaml"

    if not config_file.exists():
        logger.warning(f"Config file not found: {config_file}")
        return AgentConfig()

    yaml = YAML()
    yaml.preserve_quotes = True

    try:
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        raise AgentConfigError(
            f"Invalid YAML in {config_file}: {e}"
        ) from e

    agents_data = data.get("agents", {})
    if not agents_data:
        logger.info("No agents section in config.yaml")
        return AgentConfig()

    # Parse available agents
    available = agents_data.get("available", [])
    if isinstance(available, str):
        available = [available]
    if not isinstance(available, list):
        raise AgentConfigError(
            "Invalid agents.available in config.yaml: expected a list of agent keys"
        )

    invalid_agents = [agent for agent in available if agent not in AI_CHOICES]
    if invalid_agents:
        valid_agents = ", ".join(sorted(AI_CHOICES.keys()))
        unknown = ", ".join(sorted(invalid_agents))
        raise AgentConfigError(
            f"Unknown agent key(s) in config.yaml: {unknown}. "
            f"Valid agents: {valid_agents}"
        )

    # Parse selection config (legacy strategy field ignored)
    selection_data = agents_data.get({})
    if not isinstance(selection_data, dict):
        selection_data = {}

    selection = AgentSelectionConfig(
        preferred_implementer=selection_data.get("preferred_implementer"),
        preferred_reviewer=selection_data.get("preferred_reviewer"),
    )

    return AgentConfig(available=available, selection=selection)


def x_load_agent_config__mutmut_64(repo_root: Path) -> AgentConfig:
    """Load agent configuration from .kittify/config.yaml.

    Args:
        repo_root: Repository root directory

    Returns:
        AgentConfig instance (defaults if not configured)
    """
    config_file = repo_root / ".kittify" / "config.yaml"

    if not config_file.exists():
        logger.warning(f"Config file not found: {config_file}")
        return AgentConfig()

    yaml = YAML()
    yaml.preserve_quotes = True

    try:
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        raise AgentConfigError(
            f"Invalid YAML in {config_file}: {e}"
        ) from e

    agents_data = data.get("agents", {})
    if not agents_data:
        logger.info("No agents section in config.yaml")
        return AgentConfig()

    # Parse available agents
    available = agents_data.get("available", [])
    if isinstance(available, str):
        available = [available]
    if not isinstance(available, list):
        raise AgentConfigError(
            "Invalid agents.available in config.yaml: expected a list of agent keys"
        )

    invalid_agents = [agent for agent in available if agent not in AI_CHOICES]
    if invalid_agents:
        valid_agents = ", ".join(sorted(AI_CHOICES.keys()))
        unknown = ", ".join(sorted(invalid_agents))
        raise AgentConfigError(
            f"Unknown agent key(s) in config.yaml: {unknown}. "
            f"Valid agents: {valid_agents}"
        )

    # Parse selection config (legacy strategy field ignored)
    selection_data = agents_data.get("selection", )
    if not isinstance(selection_data, dict):
        selection_data = {}

    selection = AgentSelectionConfig(
        preferred_implementer=selection_data.get("preferred_implementer"),
        preferred_reviewer=selection_data.get("preferred_reviewer"),
    )

    return AgentConfig(available=available, selection=selection)


def x_load_agent_config__mutmut_65(repo_root: Path) -> AgentConfig:
    """Load agent configuration from .kittify/config.yaml.

    Args:
        repo_root: Repository root directory

    Returns:
        AgentConfig instance (defaults if not configured)
    """
    config_file = repo_root / ".kittify" / "config.yaml"

    if not config_file.exists():
        logger.warning(f"Config file not found: {config_file}")
        return AgentConfig()

    yaml = YAML()
    yaml.preserve_quotes = True

    try:
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        raise AgentConfigError(
            f"Invalid YAML in {config_file}: {e}"
        ) from e

    agents_data = data.get("agents", {})
    if not agents_data:
        logger.info("No agents section in config.yaml")
        return AgentConfig()

    # Parse available agents
    available = agents_data.get("available", [])
    if isinstance(available, str):
        available = [available]
    if not isinstance(available, list):
        raise AgentConfigError(
            "Invalid agents.available in config.yaml: expected a list of agent keys"
        )

    invalid_agents = [agent for agent in available if agent not in AI_CHOICES]
    if invalid_agents:
        valid_agents = ", ".join(sorted(AI_CHOICES.keys()))
        unknown = ", ".join(sorted(invalid_agents))
        raise AgentConfigError(
            f"Unknown agent key(s) in config.yaml: {unknown}. "
            f"Valid agents: {valid_agents}"
        )

    # Parse selection config (legacy strategy field ignored)
    selection_data = agents_data.get("XXselectionXX", {})
    if not isinstance(selection_data, dict):
        selection_data = {}

    selection = AgentSelectionConfig(
        preferred_implementer=selection_data.get("preferred_implementer"),
        preferred_reviewer=selection_data.get("preferred_reviewer"),
    )

    return AgentConfig(available=available, selection=selection)


def x_load_agent_config__mutmut_66(repo_root: Path) -> AgentConfig:
    """Load agent configuration from .kittify/config.yaml.

    Args:
        repo_root: Repository root directory

    Returns:
        AgentConfig instance (defaults if not configured)
    """
    config_file = repo_root / ".kittify" / "config.yaml"

    if not config_file.exists():
        logger.warning(f"Config file not found: {config_file}")
        return AgentConfig()

    yaml = YAML()
    yaml.preserve_quotes = True

    try:
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        raise AgentConfigError(
            f"Invalid YAML in {config_file}: {e}"
        ) from e

    agents_data = data.get("agents", {})
    if not agents_data:
        logger.info("No agents section in config.yaml")
        return AgentConfig()

    # Parse available agents
    available = agents_data.get("available", [])
    if isinstance(available, str):
        available = [available]
    if not isinstance(available, list):
        raise AgentConfigError(
            "Invalid agents.available in config.yaml: expected a list of agent keys"
        )

    invalid_agents = [agent for agent in available if agent not in AI_CHOICES]
    if invalid_agents:
        valid_agents = ", ".join(sorted(AI_CHOICES.keys()))
        unknown = ", ".join(sorted(invalid_agents))
        raise AgentConfigError(
            f"Unknown agent key(s) in config.yaml: {unknown}. "
            f"Valid agents: {valid_agents}"
        )

    # Parse selection config (legacy strategy field ignored)
    selection_data = agents_data.get("SELECTION", {})
    if not isinstance(selection_data, dict):
        selection_data = {}

    selection = AgentSelectionConfig(
        preferred_implementer=selection_data.get("preferred_implementer"),
        preferred_reviewer=selection_data.get("preferred_reviewer"),
    )

    return AgentConfig(available=available, selection=selection)


def x_load_agent_config__mutmut_67(repo_root: Path) -> AgentConfig:
    """Load agent configuration from .kittify/config.yaml.

    Args:
        repo_root: Repository root directory

    Returns:
        AgentConfig instance (defaults if not configured)
    """
    config_file = repo_root / ".kittify" / "config.yaml"

    if not config_file.exists():
        logger.warning(f"Config file not found: {config_file}")
        return AgentConfig()

    yaml = YAML()
    yaml.preserve_quotes = True

    try:
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        raise AgentConfigError(
            f"Invalid YAML in {config_file}: {e}"
        ) from e

    agents_data = data.get("agents", {})
    if not agents_data:
        logger.info("No agents section in config.yaml")
        return AgentConfig()

    # Parse available agents
    available = agents_data.get("available", [])
    if isinstance(available, str):
        available = [available]
    if not isinstance(available, list):
        raise AgentConfigError(
            "Invalid agents.available in config.yaml: expected a list of agent keys"
        )

    invalid_agents = [agent for agent in available if agent not in AI_CHOICES]
    if invalid_agents:
        valid_agents = ", ".join(sorted(AI_CHOICES.keys()))
        unknown = ", ".join(sorted(invalid_agents))
        raise AgentConfigError(
            f"Unknown agent key(s) in config.yaml: {unknown}. "
            f"Valid agents: {valid_agents}"
        )

    # Parse selection config (legacy strategy field ignored)
    selection_data = agents_data.get("selection", {})
    if isinstance(selection_data, dict):
        selection_data = {}

    selection = AgentSelectionConfig(
        preferred_implementer=selection_data.get("preferred_implementer"),
        preferred_reviewer=selection_data.get("preferred_reviewer"),
    )

    return AgentConfig(available=available, selection=selection)


def x_load_agent_config__mutmut_68(repo_root: Path) -> AgentConfig:
    """Load agent configuration from .kittify/config.yaml.

    Args:
        repo_root: Repository root directory

    Returns:
        AgentConfig instance (defaults if not configured)
    """
    config_file = repo_root / ".kittify" / "config.yaml"

    if not config_file.exists():
        logger.warning(f"Config file not found: {config_file}")
        return AgentConfig()

    yaml = YAML()
    yaml.preserve_quotes = True

    try:
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        raise AgentConfigError(
            f"Invalid YAML in {config_file}: {e}"
        ) from e

    agents_data = data.get("agents", {})
    if not agents_data:
        logger.info("No agents section in config.yaml")
        return AgentConfig()

    # Parse available agents
    available = agents_data.get("available", [])
    if isinstance(available, str):
        available = [available]
    if not isinstance(available, list):
        raise AgentConfigError(
            "Invalid agents.available in config.yaml: expected a list of agent keys"
        )

    invalid_agents = [agent for agent in available if agent not in AI_CHOICES]
    if invalid_agents:
        valid_agents = ", ".join(sorted(AI_CHOICES.keys()))
        unknown = ", ".join(sorted(invalid_agents))
        raise AgentConfigError(
            f"Unknown agent key(s) in config.yaml: {unknown}. "
            f"Valid agents: {valid_agents}"
        )

    # Parse selection config (legacy strategy field ignored)
    selection_data = agents_data.get("selection", {})
    if not isinstance(selection_data, dict):
        selection_data = None

    selection = AgentSelectionConfig(
        preferred_implementer=selection_data.get("preferred_implementer"),
        preferred_reviewer=selection_data.get("preferred_reviewer"),
    )

    return AgentConfig(available=available, selection=selection)


def x_load_agent_config__mutmut_69(repo_root: Path) -> AgentConfig:
    """Load agent configuration from .kittify/config.yaml.

    Args:
        repo_root: Repository root directory

    Returns:
        AgentConfig instance (defaults if not configured)
    """
    config_file = repo_root / ".kittify" / "config.yaml"

    if not config_file.exists():
        logger.warning(f"Config file not found: {config_file}")
        return AgentConfig()

    yaml = YAML()
    yaml.preserve_quotes = True

    try:
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        raise AgentConfigError(
            f"Invalid YAML in {config_file}: {e}"
        ) from e

    agents_data = data.get("agents", {})
    if not agents_data:
        logger.info("No agents section in config.yaml")
        return AgentConfig()

    # Parse available agents
    available = agents_data.get("available", [])
    if isinstance(available, str):
        available = [available]
    if not isinstance(available, list):
        raise AgentConfigError(
            "Invalid agents.available in config.yaml: expected a list of agent keys"
        )

    invalid_agents = [agent for agent in available if agent not in AI_CHOICES]
    if invalid_agents:
        valid_agents = ", ".join(sorted(AI_CHOICES.keys()))
        unknown = ", ".join(sorted(invalid_agents))
        raise AgentConfigError(
            f"Unknown agent key(s) in config.yaml: {unknown}. "
            f"Valid agents: {valid_agents}"
        )

    # Parse selection config (legacy strategy field ignored)
    selection_data = agents_data.get("selection", {})
    if not isinstance(selection_data, dict):
        selection_data = {}

    selection = None

    return AgentConfig(available=available, selection=selection)


def x_load_agent_config__mutmut_70(repo_root: Path) -> AgentConfig:
    """Load agent configuration from .kittify/config.yaml.

    Args:
        repo_root: Repository root directory

    Returns:
        AgentConfig instance (defaults if not configured)
    """
    config_file = repo_root / ".kittify" / "config.yaml"

    if not config_file.exists():
        logger.warning(f"Config file not found: {config_file}")
        return AgentConfig()

    yaml = YAML()
    yaml.preserve_quotes = True

    try:
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        raise AgentConfigError(
            f"Invalid YAML in {config_file}: {e}"
        ) from e

    agents_data = data.get("agents", {})
    if not agents_data:
        logger.info("No agents section in config.yaml")
        return AgentConfig()

    # Parse available agents
    available = agents_data.get("available", [])
    if isinstance(available, str):
        available = [available]
    if not isinstance(available, list):
        raise AgentConfigError(
            "Invalid agents.available in config.yaml: expected a list of agent keys"
        )

    invalid_agents = [agent for agent in available if agent not in AI_CHOICES]
    if invalid_agents:
        valid_agents = ", ".join(sorted(AI_CHOICES.keys()))
        unknown = ", ".join(sorted(invalid_agents))
        raise AgentConfigError(
            f"Unknown agent key(s) in config.yaml: {unknown}. "
            f"Valid agents: {valid_agents}"
        )

    # Parse selection config (legacy strategy field ignored)
    selection_data = agents_data.get("selection", {})
    if not isinstance(selection_data, dict):
        selection_data = {}

    selection = AgentSelectionConfig(
        preferred_implementer=None,
        preferred_reviewer=selection_data.get("preferred_reviewer"),
    )

    return AgentConfig(available=available, selection=selection)


def x_load_agent_config__mutmut_71(repo_root: Path) -> AgentConfig:
    """Load agent configuration from .kittify/config.yaml.

    Args:
        repo_root: Repository root directory

    Returns:
        AgentConfig instance (defaults if not configured)
    """
    config_file = repo_root / ".kittify" / "config.yaml"

    if not config_file.exists():
        logger.warning(f"Config file not found: {config_file}")
        return AgentConfig()

    yaml = YAML()
    yaml.preserve_quotes = True

    try:
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        raise AgentConfigError(
            f"Invalid YAML in {config_file}: {e}"
        ) from e

    agents_data = data.get("agents", {})
    if not agents_data:
        logger.info("No agents section in config.yaml")
        return AgentConfig()

    # Parse available agents
    available = agents_data.get("available", [])
    if isinstance(available, str):
        available = [available]
    if not isinstance(available, list):
        raise AgentConfigError(
            "Invalid agents.available in config.yaml: expected a list of agent keys"
        )

    invalid_agents = [agent for agent in available if agent not in AI_CHOICES]
    if invalid_agents:
        valid_agents = ", ".join(sorted(AI_CHOICES.keys()))
        unknown = ", ".join(sorted(invalid_agents))
        raise AgentConfigError(
            f"Unknown agent key(s) in config.yaml: {unknown}. "
            f"Valid agents: {valid_agents}"
        )

    # Parse selection config (legacy strategy field ignored)
    selection_data = agents_data.get("selection", {})
    if not isinstance(selection_data, dict):
        selection_data = {}

    selection = AgentSelectionConfig(
        preferred_implementer=selection_data.get("preferred_implementer"),
        preferred_reviewer=None,
    )

    return AgentConfig(available=available, selection=selection)


def x_load_agent_config__mutmut_72(repo_root: Path) -> AgentConfig:
    """Load agent configuration from .kittify/config.yaml.

    Args:
        repo_root: Repository root directory

    Returns:
        AgentConfig instance (defaults if not configured)
    """
    config_file = repo_root / ".kittify" / "config.yaml"

    if not config_file.exists():
        logger.warning(f"Config file not found: {config_file}")
        return AgentConfig()

    yaml = YAML()
    yaml.preserve_quotes = True

    try:
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        raise AgentConfigError(
            f"Invalid YAML in {config_file}: {e}"
        ) from e

    agents_data = data.get("agents", {})
    if not agents_data:
        logger.info("No agents section in config.yaml")
        return AgentConfig()

    # Parse available agents
    available = agents_data.get("available", [])
    if isinstance(available, str):
        available = [available]
    if not isinstance(available, list):
        raise AgentConfigError(
            "Invalid agents.available in config.yaml: expected a list of agent keys"
        )

    invalid_agents = [agent for agent in available if agent not in AI_CHOICES]
    if invalid_agents:
        valid_agents = ", ".join(sorted(AI_CHOICES.keys()))
        unknown = ", ".join(sorted(invalid_agents))
        raise AgentConfigError(
            f"Unknown agent key(s) in config.yaml: {unknown}. "
            f"Valid agents: {valid_agents}"
        )

    # Parse selection config (legacy strategy field ignored)
    selection_data = agents_data.get("selection", {})
    if not isinstance(selection_data, dict):
        selection_data = {}

    selection = AgentSelectionConfig(
        preferred_reviewer=selection_data.get("preferred_reviewer"),
    )

    return AgentConfig(available=available, selection=selection)


def x_load_agent_config__mutmut_73(repo_root: Path) -> AgentConfig:
    """Load agent configuration from .kittify/config.yaml.

    Args:
        repo_root: Repository root directory

    Returns:
        AgentConfig instance (defaults if not configured)
    """
    config_file = repo_root / ".kittify" / "config.yaml"

    if not config_file.exists():
        logger.warning(f"Config file not found: {config_file}")
        return AgentConfig()

    yaml = YAML()
    yaml.preserve_quotes = True

    try:
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        raise AgentConfigError(
            f"Invalid YAML in {config_file}: {e}"
        ) from e

    agents_data = data.get("agents", {})
    if not agents_data:
        logger.info("No agents section in config.yaml")
        return AgentConfig()

    # Parse available agents
    available = agents_data.get("available", [])
    if isinstance(available, str):
        available = [available]
    if not isinstance(available, list):
        raise AgentConfigError(
            "Invalid agents.available in config.yaml: expected a list of agent keys"
        )

    invalid_agents = [agent for agent in available if agent not in AI_CHOICES]
    if invalid_agents:
        valid_agents = ", ".join(sorted(AI_CHOICES.keys()))
        unknown = ", ".join(sorted(invalid_agents))
        raise AgentConfigError(
            f"Unknown agent key(s) in config.yaml: {unknown}. "
            f"Valid agents: {valid_agents}"
        )

    # Parse selection config (legacy strategy field ignored)
    selection_data = agents_data.get("selection", {})
    if not isinstance(selection_data, dict):
        selection_data = {}

    selection = AgentSelectionConfig(
        preferred_implementer=selection_data.get("preferred_implementer"),
        )

    return AgentConfig(available=available, selection=selection)


def x_load_agent_config__mutmut_74(repo_root: Path) -> AgentConfig:
    """Load agent configuration from .kittify/config.yaml.

    Args:
        repo_root: Repository root directory

    Returns:
        AgentConfig instance (defaults if not configured)
    """
    config_file = repo_root / ".kittify" / "config.yaml"

    if not config_file.exists():
        logger.warning(f"Config file not found: {config_file}")
        return AgentConfig()

    yaml = YAML()
    yaml.preserve_quotes = True

    try:
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        raise AgentConfigError(
            f"Invalid YAML in {config_file}: {e}"
        ) from e

    agents_data = data.get("agents", {})
    if not agents_data:
        logger.info("No agents section in config.yaml")
        return AgentConfig()

    # Parse available agents
    available = agents_data.get("available", [])
    if isinstance(available, str):
        available = [available]
    if not isinstance(available, list):
        raise AgentConfigError(
            "Invalid agents.available in config.yaml: expected a list of agent keys"
        )

    invalid_agents = [agent for agent in available if agent not in AI_CHOICES]
    if invalid_agents:
        valid_agents = ", ".join(sorted(AI_CHOICES.keys()))
        unknown = ", ".join(sorted(invalid_agents))
        raise AgentConfigError(
            f"Unknown agent key(s) in config.yaml: {unknown}. "
            f"Valid agents: {valid_agents}"
        )

    # Parse selection config (legacy strategy field ignored)
    selection_data = agents_data.get("selection", {})
    if not isinstance(selection_data, dict):
        selection_data = {}

    selection = AgentSelectionConfig(
        preferred_implementer=selection_data.get(None),
        preferred_reviewer=selection_data.get("preferred_reviewer"),
    )

    return AgentConfig(available=available, selection=selection)


def x_load_agent_config__mutmut_75(repo_root: Path) -> AgentConfig:
    """Load agent configuration from .kittify/config.yaml.

    Args:
        repo_root: Repository root directory

    Returns:
        AgentConfig instance (defaults if not configured)
    """
    config_file = repo_root / ".kittify" / "config.yaml"

    if not config_file.exists():
        logger.warning(f"Config file not found: {config_file}")
        return AgentConfig()

    yaml = YAML()
    yaml.preserve_quotes = True

    try:
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        raise AgentConfigError(
            f"Invalid YAML in {config_file}: {e}"
        ) from e

    agents_data = data.get("agents", {})
    if not agents_data:
        logger.info("No agents section in config.yaml")
        return AgentConfig()

    # Parse available agents
    available = agents_data.get("available", [])
    if isinstance(available, str):
        available = [available]
    if not isinstance(available, list):
        raise AgentConfigError(
            "Invalid agents.available in config.yaml: expected a list of agent keys"
        )

    invalid_agents = [agent for agent in available if agent not in AI_CHOICES]
    if invalid_agents:
        valid_agents = ", ".join(sorted(AI_CHOICES.keys()))
        unknown = ", ".join(sorted(invalid_agents))
        raise AgentConfigError(
            f"Unknown agent key(s) in config.yaml: {unknown}. "
            f"Valid agents: {valid_agents}"
        )

    # Parse selection config (legacy strategy field ignored)
    selection_data = agents_data.get("selection", {})
    if not isinstance(selection_data, dict):
        selection_data = {}

    selection = AgentSelectionConfig(
        preferred_implementer=selection_data.get("XXpreferred_implementerXX"),
        preferred_reviewer=selection_data.get("preferred_reviewer"),
    )

    return AgentConfig(available=available, selection=selection)


def x_load_agent_config__mutmut_76(repo_root: Path) -> AgentConfig:
    """Load agent configuration from .kittify/config.yaml.

    Args:
        repo_root: Repository root directory

    Returns:
        AgentConfig instance (defaults if not configured)
    """
    config_file = repo_root / ".kittify" / "config.yaml"

    if not config_file.exists():
        logger.warning(f"Config file not found: {config_file}")
        return AgentConfig()

    yaml = YAML()
    yaml.preserve_quotes = True

    try:
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        raise AgentConfigError(
            f"Invalid YAML in {config_file}: {e}"
        ) from e

    agents_data = data.get("agents", {})
    if not agents_data:
        logger.info("No agents section in config.yaml")
        return AgentConfig()

    # Parse available agents
    available = agents_data.get("available", [])
    if isinstance(available, str):
        available = [available]
    if not isinstance(available, list):
        raise AgentConfigError(
            "Invalid agents.available in config.yaml: expected a list of agent keys"
        )

    invalid_agents = [agent for agent in available if agent not in AI_CHOICES]
    if invalid_agents:
        valid_agents = ", ".join(sorted(AI_CHOICES.keys()))
        unknown = ", ".join(sorted(invalid_agents))
        raise AgentConfigError(
            f"Unknown agent key(s) in config.yaml: {unknown}. "
            f"Valid agents: {valid_agents}"
        )

    # Parse selection config (legacy strategy field ignored)
    selection_data = agents_data.get("selection", {})
    if not isinstance(selection_data, dict):
        selection_data = {}

    selection = AgentSelectionConfig(
        preferred_implementer=selection_data.get("PREFERRED_IMPLEMENTER"),
        preferred_reviewer=selection_data.get("preferred_reviewer"),
    )

    return AgentConfig(available=available, selection=selection)


def x_load_agent_config__mutmut_77(repo_root: Path) -> AgentConfig:
    """Load agent configuration from .kittify/config.yaml.

    Args:
        repo_root: Repository root directory

    Returns:
        AgentConfig instance (defaults if not configured)
    """
    config_file = repo_root / ".kittify" / "config.yaml"

    if not config_file.exists():
        logger.warning(f"Config file not found: {config_file}")
        return AgentConfig()

    yaml = YAML()
    yaml.preserve_quotes = True

    try:
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        raise AgentConfigError(
            f"Invalid YAML in {config_file}: {e}"
        ) from e

    agents_data = data.get("agents", {})
    if not agents_data:
        logger.info("No agents section in config.yaml")
        return AgentConfig()

    # Parse available agents
    available = agents_data.get("available", [])
    if isinstance(available, str):
        available = [available]
    if not isinstance(available, list):
        raise AgentConfigError(
            "Invalid agents.available in config.yaml: expected a list of agent keys"
        )

    invalid_agents = [agent for agent in available if agent not in AI_CHOICES]
    if invalid_agents:
        valid_agents = ", ".join(sorted(AI_CHOICES.keys()))
        unknown = ", ".join(sorted(invalid_agents))
        raise AgentConfigError(
            f"Unknown agent key(s) in config.yaml: {unknown}. "
            f"Valid agents: {valid_agents}"
        )

    # Parse selection config (legacy strategy field ignored)
    selection_data = agents_data.get("selection", {})
    if not isinstance(selection_data, dict):
        selection_data = {}

    selection = AgentSelectionConfig(
        preferred_implementer=selection_data.get("preferred_implementer"),
        preferred_reviewer=selection_data.get(None),
    )

    return AgentConfig(available=available, selection=selection)


def x_load_agent_config__mutmut_78(repo_root: Path) -> AgentConfig:
    """Load agent configuration from .kittify/config.yaml.

    Args:
        repo_root: Repository root directory

    Returns:
        AgentConfig instance (defaults if not configured)
    """
    config_file = repo_root / ".kittify" / "config.yaml"

    if not config_file.exists():
        logger.warning(f"Config file not found: {config_file}")
        return AgentConfig()

    yaml = YAML()
    yaml.preserve_quotes = True

    try:
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        raise AgentConfigError(
            f"Invalid YAML in {config_file}: {e}"
        ) from e

    agents_data = data.get("agents", {})
    if not agents_data:
        logger.info("No agents section in config.yaml")
        return AgentConfig()

    # Parse available agents
    available = agents_data.get("available", [])
    if isinstance(available, str):
        available = [available]
    if not isinstance(available, list):
        raise AgentConfigError(
            "Invalid agents.available in config.yaml: expected a list of agent keys"
        )

    invalid_agents = [agent for agent in available if agent not in AI_CHOICES]
    if invalid_agents:
        valid_agents = ", ".join(sorted(AI_CHOICES.keys()))
        unknown = ", ".join(sorted(invalid_agents))
        raise AgentConfigError(
            f"Unknown agent key(s) in config.yaml: {unknown}. "
            f"Valid agents: {valid_agents}"
        )

    # Parse selection config (legacy strategy field ignored)
    selection_data = agents_data.get("selection", {})
    if not isinstance(selection_data, dict):
        selection_data = {}

    selection = AgentSelectionConfig(
        preferred_implementer=selection_data.get("preferred_implementer"),
        preferred_reviewer=selection_data.get("XXpreferred_reviewerXX"),
    )

    return AgentConfig(available=available, selection=selection)


def x_load_agent_config__mutmut_79(repo_root: Path) -> AgentConfig:
    """Load agent configuration from .kittify/config.yaml.

    Args:
        repo_root: Repository root directory

    Returns:
        AgentConfig instance (defaults if not configured)
    """
    config_file = repo_root / ".kittify" / "config.yaml"

    if not config_file.exists():
        logger.warning(f"Config file not found: {config_file}")
        return AgentConfig()

    yaml = YAML()
    yaml.preserve_quotes = True

    try:
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        raise AgentConfigError(
            f"Invalid YAML in {config_file}: {e}"
        ) from e

    agents_data = data.get("agents", {})
    if not agents_data:
        logger.info("No agents section in config.yaml")
        return AgentConfig()

    # Parse available agents
    available = agents_data.get("available", [])
    if isinstance(available, str):
        available = [available]
    if not isinstance(available, list):
        raise AgentConfigError(
            "Invalid agents.available in config.yaml: expected a list of agent keys"
        )

    invalid_agents = [agent for agent in available if agent not in AI_CHOICES]
    if invalid_agents:
        valid_agents = ", ".join(sorted(AI_CHOICES.keys()))
        unknown = ", ".join(sorted(invalid_agents))
        raise AgentConfigError(
            f"Unknown agent key(s) in config.yaml: {unknown}. "
            f"Valid agents: {valid_agents}"
        )

    # Parse selection config (legacy strategy field ignored)
    selection_data = agents_data.get("selection", {})
    if not isinstance(selection_data, dict):
        selection_data = {}

    selection = AgentSelectionConfig(
        preferred_implementer=selection_data.get("preferred_implementer"),
        preferred_reviewer=selection_data.get("PREFERRED_REVIEWER"),
    )

    return AgentConfig(available=available, selection=selection)


def x_load_agent_config__mutmut_80(repo_root: Path) -> AgentConfig:
    """Load agent configuration from .kittify/config.yaml.

    Args:
        repo_root: Repository root directory

    Returns:
        AgentConfig instance (defaults if not configured)
    """
    config_file = repo_root / ".kittify" / "config.yaml"

    if not config_file.exists():
        logger.warning(f"Config file not found: {config_file}")
        return AgentConfig()

    yaml = YAML()
    yaml.preserve_quotes = True

    try:
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        raise AgentConfigError(
            f"Invalid YAML in {config_file}: {e}"
        ) from e

    agents_data = data.get("agents", {})
    if not agents_data:
        logger.info("No agents section in config.yaml")
        return AgentConfig()

    # Parse available agents
    available = agents_data.get("available", [])
    if isinstance(available, str):
        available = [available]
    if not isinstance(available, list):
        raise AgentConfigError(
            "Invalid agents.available in config.yaml: expected a list of agent keys"
        )

    invalid_agents = [agent for agent in available if agent not in AI_CHOICES]
    if invalid_agents:
        valid_agents = ", ".join(sorted(AI_CHOICES.keys()))
        unknown = ", ".join(sorted(invalid_agents))
        raise AgentConfigError(
            f"Unknown agent key(s) in config.yaml: {unknown}. "
            f"Valid agents: {valid_agents}"
        )

    # Parse selection config (legacy strategy field ignored)
    selection_data = agents_data.get("selection", {})
    if not isinstance(selection_data, dict):
        selection_data = {}

    selection = AgentSelectionConfig(
        preferred_implementer=selection_data.get("preferred_implementer"),
        preferred_reviewer=selection_data.get("preferred_reviewer"),
    )

    return AgentConfig(available=None, selection=selection)


def x_load_agent_config__mutmut_81(repo_root: Path) -> AgentConfig:
    """Load agent configuration from .kittify/config.yaml.

    Args:
        repo_root: Repository root directory

    Returns:
        AgentConfig instance (defaults if not configured)
    """
    config_file = repo_root / ".kittify" / "config.yaml"

    if not config_file.exists():
        logger.warning(f"Config file not found: {config_file}")
        return AgentConfig()

    yaml = YAML()
    yaml.preserve_quotes = True

    try:
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        raise AgentConfigError(
            f"Invalid YAML in {config_file}: {e}"
        ) from e

    agents_data = data.get("agents", {})
    if not agents_data:
        logger.info("No agents section in config.yaml")
        return AgentConfig()

    # Parse available agents
    available = agents_data.get("available", [])
    if isinstance(available, str):
        available = [available]
    if not isinstance(available, list):
        raise AgentConfigError(
            "Invalid agents.available in config.yaml: expected a list of agent keys"
        )

    invalid_agents = [agent for agent in available if agent not in AI_CHOICES]
    if invalid_agents:
        valid_agents = ", ".join(sorted(AI_CHOICES.keys()))
        unknown = ", ".join(sorted(invalid_agents))
        raise AgentConfigError(
            f"Unknown agent key(s) in config.yaml: {unknown}. "
            f"Valid agents: {valid_agents}"
        )

    # Parse selection config (legacy strategy field ignored)
    selection_data = agents_data.get("selection", {})
    if not isinstance(selection_data, dict):
        selection_data = {}

    selection = AgentSelectionConfig(
        preferred_implementer=selection_data.get("preferred_implementer"),
        preferred_reviewer=selection_data.get("preferred_reviewer"),
    )

    return AgentConfig(available=available, selection=None)


def x_load_agent_config__mutmut_82(repo_root: Path) -> AgentConfig:
    """Load agent configuration from .kittify/config.yaml.

    Args:
        repo_root: Repository root directory

    Returns:
        AgentConfig instance (defaults if not configured)
    """
    config_file = repo_root / ".kittify" / "config.yaml"

    if not config_file.exists():
        logger.warning(f"Config file not found: {config_file}")
        return AgentConfig()

    yaml = YAML()
    yaml.preserve_quotes = True

    try:
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        raise AgentConfigError(
            f"Invalid YAML in {config_file}: {e}"
        ) from e

    agents_data = data.get("agents", {})
    if not agents_data:
        logger.info("No agents section in config.yaml")
        return AgentConfig()

    # Parse available agents
    available = agents_data.get("available", [])
    if isinstance(available, str):
        available = [available]
    if not isinstance(available, list):
        raise AgentConfigError(
            "Invalid agents.available in config.yaml: expected a list of agent keys"
        )

    invalid_agents = [agent for agent in available if agent not in AI_CHOICES]
    if invalid_agents:
        valid_agents = ", ".join(sorted(AI_CHOICES.keys()))
        unknown = ", ".join(sorted(invalid_agents))
        raise AgentConfigError(
            f"Unknown agent key(s) in config.yaml: {unknown}. "
            f"Valid agents: {valid_agents}"
        )

    # Parse selection config (legacy strategy field ignored)
    selection_data = agents_data.get("selection", {})
    if not isinstance(selection_data, dict):
        selection_data = {}

    selection = AgentSelectionConfig(
        preferred_implementer=selection_data.get("preferred_implementer"),
        preferred_reviewer=selection_data.get("preferred_reviewer"),
    )

    return AgentConfig(selection=selection)


def x_load_agent_config__mutmut_83(repo_root: Path) -> AgentConfig:
    """Load agent configuration from .kittify/config.yaml.

    Args:
        repo_root: Repository root directory

    Returns:
        AgentConfig instance (defaults if not configured)
    """
    config_file = repo_root / ".kittify" / "config.yaml"

    if not config_file.exists():
        logger.warning(f"Config file not found: {config_file}")
        return AgentConfig()

    yaml = YAML()
    yaml.preserve_quotes = True

    try:
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        raise AgentConfigError(
            f"Invalid YAML in {config_file}: {e}"
        ) from e

    agents_data = data.get("agents", {})
    if not agents_data:
        logger.info("No agents section in config.yaml")
        return AgentConfig()

    # Parse available agents
    available = agents_data.get("available", [])
    if isinstance(available, str):
        available = [available]
    if not isinstance(available, list):
        raise AgentConfigError(
            "Invalid agents.available in config.yaml: expected a list of agent keys"
        )

    invalid_agents = [agent for agent in available if agent not in AI_CHOICES]
    if invalid_agents:
        valid_agents = ", ".join(sorted(AI_CHOICES.keys()))
        unknown = ", ".join(sorted(invalid_agents))
        raise AgentConfigError(
            f"Unknown agent key(s) in config.yaml: {unknown}. "
            f"Valid agents: {valid_agents}"
        )

    # Parse selection config (legacy strategy field ignored)
    selection_data = agents_data.get("selection", {})
    if not isinstance(selection_data, dict):
        selection_data = {}

    selection = AgentSelectionConfig(
        preferred_implementer=selection_data.get("preferred_implementer"),
        preferred_reviewer=selection_data.get("preferred_reviewer"),
    )

    return AgentConfig(available=available, )

x_load_agent_config__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_load_agent_config__mutmut_1': x_load_agent_config__mutmut_1, 
    'x_load_agent_config__mutmut_2': x_load_agent_config__mutmut_2, 
    'x_load_agent_config__mutmut_3': x_load_agent_config__mutmut_3, 
    'x_load_agent_config__mutmut_4': x_load_agent_config__mutmut_4, 
    'x_load_agent_config__mutmut_5': x_load_agent_config__mutmut_5, 
    'x_load_agent_config__mutmut_6': x_load_agent_config__mutmut_6, 
    'x_load_agent_config__mutmut_7': x_load_agent_config__mutmut_7, 
    'x_load_agent_config__mutmut_8': x_load_agent_config__mutmut_8, 
    'x_load_agent_config__mutmut_9': x_load_agent_config__mutmut_9, 
    'x_load_agent_config__mutmut_10': x_load_agent_config__mutmut_10, 
    'x_load_agent_config__mutmut_11': x_load_agent_config__mutmut_11, 
    'x_load_agent_config__mutmut_12': x_load_agent_config__mutmut_12, 
    'x_load_agent_config__mutmut_13': x_load_agent_config__mutmut_13, 
    'x_load_agent_config__mutmut_14': x_load_agent_config__mutmut_14, 
    'x_load_agent_config__mutmut_15': x_load_agent_config__mutmut_15, 
    'x_load_agent_config__mutmut_16': x_load_agent_config__mutmut_16, 
    'x_load_agent_config__mutmut_17': x_load_agent_config__mutmut_17, 
    'x_load_agent_config__mutmut_18': x_load_agent_config__mutmut_18, 
    'x_load_agent_config__mutmut_19': x_load_agent_config__mutmut_19, 
    'x_load_agent_config__mutmut_20': x_load_agent_config__mutmut_20, 
    'x_load_agent_config__mutmut_21': x_load_agent_config__mutmut_21, 
    'x_load_agent_config__mutmut_22': x_load_agent_config__mutmut_22, 
    'x_load_agent_config__mutmut_23': x_load_agent_config__mutmut_23, 
    'x_load_agent_config__mutmut_24': x_load_agent_config__mutmut_24, 
    'x_load_agent_config__mutmut_25': x_load_agent_config__mutmut_25, 
    'x_load_agent_config__mutmut_26': x_load_agent_config__mutmut_26, 
    'x_load_agent_config__mutmut_27': x_load_agent_config__mutmut_27, 
    'x_load_agent_config__mutmut_28': x_load_agent_config__mutmut_28, 
    'x_load_agent_config__mutmut_29': x_load_agent_config__mutmut_29, 
    'x_load_agent_config__mutmut_30': x_load_agent_config__mutmut_30, 
    'x_load_agent_config__mutmut_31': x_load_agent_config__mutmut_31, 
    'x_load_agent_config__mutmut_32': x_load_agent_config__mutmut_32, 
    'x_load_agent_config__mutmut_33': x_load_agent_config__mutmut_33, 
    'x_load_agent_config__mutmut_34': x_load_agent_config__mutmut_34, 
    'x_load_agent_config__mutmut_35': x_load_agent_config__mutmut_35, 
    'x_load_agent_config__mutmut_36': x_load_agent_config__mutmut_36, 
    'x_load_agent_config__mutmut_37': x_load_agent_config__mutmut_37, 
    'x_load_agent_config__mutmut_38': x_load_agent_config__mutmut_38, 
    'x_load_agent_config__mutmut_39': x_load_agent_config__mutmut_39, 
    'x_load_agent_config__mutmut_40': x_load_agent_config__mutmut_40, 
    'x_load_agent_config__mutmut_41': x_load_agent_config__mutmut_41, 
    'x_load_agent_config__mutmut_42': x_load_agent_config__mutmut_42, 
    'x_load_agent_config__mutmut_43': x_load_agent_config__mutmut_43, 
    'x_load_agent_config__mutmut_44': x_load_agent_config__mutmut_44, 
    'x_load_agent_config__mutmut_45': x_load_agent_config__mutmut_45, 
    'x_load_agent_config__mutmut_46': x_load_agent_config__mutmut_46, 
    'x_load_agent_config__mutmut_47': x_load_agent_config__mutmut_47, 
    'x_load_agent_config__mutmut_48': x_load_agent_config__mutmut_48, 
    'x_load_agent_config__mutmut_49': x_load_agent_config__mutmut_49, 
    'x_load_agent_config__mutmut_50': x_load_agent_config__mutmut_50, 
    'x_load_agent_config__mutmut_51': x_load_agent_config__mutmut_51, 
    'x_load_agent_config__mutmut_52': x_load_agent_config__mutmut_52, 
    'x_load_agent_config__mutmut_53': x_load_agent_config__mutmut_53, 
    'x_load_agent_config__mutmut_54': x_load_agent_config__mutmut_54, 
    'x_load_agent_config__mutmut_55': x_load_agent_config__mutmut_55, 
    'x_load_agent_config__mutmut_56': x_load_agent_config__mutmut_56, 
    'x_load_agent_config__mutmut_57': x_load_agent_config__mutmut_57, 
    'x_load_agent_config__mutmut_58': x_load_agent_config__mutmut_58, 
    'x_load_agent_config__mutmut_59': x_load_agent_config__mutmut_59, 
    'x_load_agent_config__mutmut_60': x_load_agent_config__mutmut_60, 
    'x_load_agent_config__mutmut_61': x_load_agent_config__mutmut_61, 
    'x_load_agent_config__mutmut_62': x_load_agent_config__mutmut_62, 
    'x_load_agent_config__mutmut_63': x_load_agent_config__mutmut_63, 
    'x_load_agent_config__mutmut_64': x_load_agent_config__mutmut_64, 
    'x_load_agent_config__mutmut_65': x_load_agent_config__mutmut_65, 
    'x_load_agent_config__mutmut_66': x_load_agent_config__mutmut_66, 
    'x_load_agent_config__mutmut_67': x_load_agent_config__mutmut_67, 
    'x_load_agent_config__mutmut_68': x_load_agent_config__mutmut_68, 
    'x_load_agent_config__mutmut_69': x_load_agent_config__mutmut_69, 
    'x_load_agent_config__mutmut_70': x_load_agent_config__mutmut_70, 
    'x_load_agent_config__mutmut_71': x_load_agent_config__mutmut_71, 
    'x_load_agent_config__mutmut_72': x_load_agent_config__mutmut_72, 
    'x_load_agent_config__mutmut_73': x_load_agent_config__mutmut_73, 
    'x_load_agent_config__mutmut_74': x_load_agent_config__mutmut_74, 
    'x_load_agent_config__mutmut_75': x_load_agent_config__mutmut_75, 
    'x_load_agent_config__mutmut_76': x_load_agent_config__mutmut_76, 
    'x_load_agent_config__mutmut_77': x_load_agent_config__mutmut_77, 
    'x_load_agent_config__mutmut_78': x_load_agent_config__mutmut_78, 
    'x_load_agent_config__mutmut_79': x_load_agent_config__mutmut_79, 
    'x_load_agent_config__mutmut_80': x_load_agent_config__mutmut_80, 
    'x_load_agent_config__mutmut_81': x_load_agent_config__mutmut_81, 
    'x_load_agent_config__mutmut_82': x_load_agent_config__mutmut_82, 
    'x_load_agent_config__mutmut_83': x_load_agent_config__mutmut_83
}
x_load_agent_config__mutmut_orig.__name__ = 'x_load_agent_config'


def save_agent_config(repo_root: Path, config: AgentConfig) -> None:
    args = [repo_root, config]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_save_agent_config__mutmut_orig, x_save_agent_config__mutmut_mutants, args, kwargs, None)


def x_save_agent_config__mutmut_orig(repo_root: Path, config: AgentConfig) -> None:
    """Save agent configuration to .kittify/config.yaml.

    Merges with existing config (preserves other sections like vcs).

    Args:
        repo_root: Repository root directory
        config: AgentConfig to save
    """
    config_dir = repo_root / ".kittify"
    config_file = config_dir / "config.yaml"

    yaml = YAML()
    yaml.preserve_quotes = True

    # Load existing config or create new
    if config_file.exists():
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    else:
        data = {}
        config_dir.mkdir(parents=True, exist_ok=True)

    # Update agents section
    data["agents"] = {
        "available": config.available,
        "selection": {
            "preferred_implementer": config.selection.preferred_implementer,
            "preferred_reviewer": config.selection.preferred_reviewer,
        },
    }

    # Write back
    with open(config_file, "w") as f:
        yaml.dump(data, f)

    logger.info(f"Saved agent config to {config_file}")


def x_save_agent_config__mutmut_1(repo_root: Path, config: AgentConfig) -> None:
    """Save agent configuration to .kittify/config.yaml.

    Merges with existing config (preserves other sections like vcs).

    Args:
        repo_root: Repository root directory
        config: AgentConfig to save
    """
    config_dir = None
    config_file = config_dir / "config.yaml"

    yaml = YAML()
    yaml.preserve_quotes = True

    # Load existing config or create new
    if config_file.exists():
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    else:
        data = {}
        config_dir.mkdir(parents=True, exist_ok=True)

    # Update agents section
    data["agents"] = {
        "available": config.available,
        "selection": {
            "preferred_implementer": config.selection.preferred_implementer,
            "preferred_reviewer": config.selection.preferred_reviewer,
        },
    }

    # Write back
    with open(config_file, "w") as f:
        yaml.dump(data, f)

    logger.info(f"Saved agent config to {config_file}")


def x_save_agent_config__mutmut_2(repo_root: Path, config: AgentConfig) -> None:
    """Save agent configuration to .kittify/config.yaml.

    Merges with existing config (preserves other sections like vcs).

    Args:
        repo_root: Repository root directory
        config: AgentConfig to save
    """
    config_dir = repo_root * ".kittify"
    config_file = config_dir / "config.yaml"

    yaml = YAML()
    yaml.preserve_quotes = True

    # Load existing config or create new
    if config_file.exists():
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    else:
        data = {}
        config_dir.mkdir(parents=True, exist_ok=True)

    # Update agents section
    data["agents"] = {
        "available": config.available,
        "selection": {
            "preferred_implementer": config.selection.preferred_implementer,
            "preferred_reviewer": config.selection.preferred_reviewer,
        },
    }

    # Write back
    with open(config_file, "w") as f:
        yaml.dump(data, f)

    logger.info(f"Saved agent config to {config_file}")


def x_save_agent_config__mutmut_3(repo_root: Path, config: AgentConfig) -> None:
    """Save agent configuration to .kittify/config.yaml.

    Merges with existing config (preserves other sections like vcs).

    Args:
        repo_root: Repository root directory
        config: AgentConfig to save
    """
    config_dir = repo_root / "XX.kittifyXX"
    config_file = config_dir / "config.yaml"

    yaml = YAML()
    yaml.preserve_quotes = True

    # Load existing config or create new
    if config_file.exists():
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    else:
        data = {}
        config_dir.mkdir(parents=True, exist_ok=True)

    # Update agents section
    data["agents"] = {
        "available": config.available,
        "selection": {
            "preferred_implementer": config.selection.preferred_implementer,
            "preferred_reviewer": config.selection.preferred_reviewer,
        },
    }

    # Write back
    with open(config_file, "w") as f:
        yaml.dump(data, f)

    logger.info(f"Saved agent config to {config_file}")


def x_save_agent_config__mutmut_4(repo_root: Path, config: AgentConfig) -> None:
    """Save agent configuration to .kittify/config.yaml.

    Merges with existing config (preserves other sections like vcs).

    Args:
        repo_root: Repository root directory
        config: AgentConfig to save
    """
    config_dir = repo_root / ".KITTIFY"
    config_file = config_dir / "config.yaml"

    yaml = YAML()
    yaml.preserve_quotes = True

    # Load existing config or create new
    if config_file.exists():
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    else:
        data = {}
        config_dir.mkdir(parents=True, exist_ok=True)

    # Update agents section
    data["agents"] = {
        "available": config.available,
        "selection": {
            "preferred_implementer": config.selection.preferred_implementer,
            "preferred_reviewer": config.selection.preferred_reviewer,
        },
    }

    # Write back
    with open(config_file, "w") as f:
        yaml.dump(data, f)

    logger.info(f"Saved agent config to {config_file}")


def x_save_agent_config__mutmut_5(repo_root: Path, config: AgentConfig) -> None:
    """Save agent configuration to .kittify/config.yaml.

    Merges with existing config (preserves other sections like vcs).

    Args:
        repo_root: Repository root directory
        config: AgentConfig to save
    """
    config_dir = repo_root / ".kittify"
    config_file = None

    yaml = YAML()
    yaml.preserve_quotes = True

    # Load existing config or create new
    if config_file.exists():
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    else:
        data = {}
        config_dir.mkdir(parents=True, exist_ok=True)

    # Update agents section
    data["agents"] = {
        "available": config.available,
        "selection": {
            "preferred_implementer": config.selection.preferred_implementer,
            "preferred_reviewer": config.selection.preferred_reviewer,
        },
    }

    # Write back
    with open(config_file, "w") as f:
        yaml.dump(data, f)

    logger.info(f"Saved agent config to {config_file}")


def x_save_agent_config__mutmut_6(repo_root: Path, config: AgentConfig) -> None:
    """Save agent configuration to .kittify/config.yaml.

    Merges with existing config (preserves other sections like vcs).

    Args:
        repo_root: Repository root directory
        config: AgentConfig to save
    """
    config_dir = repo_root / ".kittify"
    config_file = config_dir * "config.yaml"

    yaml = YAML()
    yaml.preserve_quotes = True

    # Load existing config or create new
    if config_file.exists():
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    else:
        data = {}
        config_dir.mkdir(parents=True, exist_ok=True)

    # Update agents section
    data["agents"] = {
        "available": config.available,
        "selection": {
            "preferred_implementer": config.selection.preferred_implementer,
            "preferred_reviewer": config.selection.preferred_reviewer,
        },
    }

    # Write back
    with open(config_file, "w") as f:
        yaml.dump(data, f)

    logger.info(f"Saved agent config to {config_file}")


def x_save_agent_config__mutmut_7(repo_root: Path, config: AgentConfig) -> None:
    """Save agent configuration to .kittify/config.yaml.

    Merges with existing config (preserves other sections like vcs).

    Args:
        repo_root: Repository root directory
        config: AgentConfig to save
    """
    config_dir = repo_root / ".kittify"
    config_file = config_dir / "XXconfig.yamlXX"

    yaml = YAML()
    yaml.preserve_quotes = True

    # Load existing config or create new
    if config_file.exists():
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    else:
        data = {}
        config_dir.mkdir(parents=True, exist_ok=True)

    # Update agents section
    data["agents"] = {
        "available": config.available,
        "selection": {
            "preferred_implementer": config.selection.preferred_implementer,
            "preferred_reviewer": config.selection.preferred_reviewer,
        },
    }

    # Write back
    with open(config_file, "w") as f:
        yaml.dump(data, f)

    logger.info(f"Saved agent config to {config_file}")


def x_save_agent_config__mutmut_8(repo_root: Path, config: AgentConfig) -> None:
    """Save agent configuration to .kittify/config.yaml.

    Merges with existing config (preserves other sections like vcs).

    Args:
        repo_root: Repository root directory
        config: AgentConfig to save
    """
    config_dir = repo_root / ".kittify"
    config_file = config_dir / "CONFIG.YAML"

    yaml = YAML()
    yaml.preserve_quotes = True

    # Load existing config or create new
    if config_file.exists():
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    else:
        data = {}
        config_dir.mkdir(parents=True, exist_ok=True)

    # Update agents section
    data["agents"] = {
        "available": config.available,
        "selection": {
            "preferred_implementer": config.selection.preferred_implementer,
            "preferred_reviewer": config.selection.preferred_reviewer,
        },
    }

    # Write back
    with open(config_file, "w") as f:
        yaml.dump(data, f)

    logger.info(f"Saved agent config to {config_file}")


def x_save_agent_config__mutmut_9(repo_root: Path, config: AgentConfig) -> None:
    """Save agent configuration to .kittify/config.yaml.

    Merges with existing config (preserves other sections like vcs).

    Args:
        repo_root: Repository root directory
        config: AgentConfig to save
    """
    config_dir = repo_root / ".kittify"
    config_file = config_dir / "config.yaml"

    yaml = None
    yaml.preserve_quotes = True

    # Load existing config or create new
    if config_file.exists():
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    else:
        data = {}
        config_dir.mkdir(parents=True, exist_ok=True)

    # Update agents section
    data["agents"] = {
        "available": config.available,
        "selection": {
            "preferred_implementer": config.selection.preferred_implementer,
            "preferred_reviewer": config.selection.preferred_reviewer,
        },
    }

    # Write back
    with open(config_file, "w") as f:
        yaml.dump(data, f)

    logger.info(f"Saved agent config to {config_file}")


def x_save_agent_config__mutmut_10(repo_root: Path, config: AgentConfig) -> None:
    """Save agent configuration to .kittify/config.yaml.

    Merges with existing config (preserves other sections like vcs).

    Args:
        repo_root: Repository root directory
        config: AgentConfig to save
    """
    config_dir = repo_root / ".kittify"
    config_file = config_dir / "config.yaml"

    yaml = YAML()
    yaml.preserve_quotes = None

    # Load existing config or create new
    if config_file.exists():
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    else:
        data = {}
        config_dir.mkdir(parents=True, exist_ok=True)

    # Update agents section
    data["agents"] = {
        "available": config.available,
        "selection": {
            "preferred_implementer": config.selection.preferred_implementer,
            "preferred_reviewer": config.selection.preferred_reviewer,
        },
    }

    # Write back
    with open(config_file, "w") as f:
        yaml.dump(data, f)

    logger.info(f"Saved agent config to {config_file}")


def x_save_agent_config__mutmut_11(repo_root: Path, config: AgentConfig) -> None:
    """Save agent configuration to .kittify/config.yaml.

    Merges with existing config (preserves other sections like vcs).

    Args:
        repo_root: Repository root directory
        config: AgentConfig to save
    """
    config_dir = repo_root / ".kittify"
    config_file = config_dir / "config.yaml"

    yaml = YAML()
    yaml.preserve_quotes = False

    # Load existing config or create new
    if config_file.exists():
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    else:
        data = {}
        config_dir.mkdir(parents=True, exist_ok=True)

    # Update agents section
    data["agents"] = {
        "available": config.available,
        "selection": {
            "preferred_implementer": config.selection.preferred_implementer,
            "preferred_reviewer": config.selection.preferred_reviewer,
        },
    }

    # Write back
    with open(config_file, "w") as f:
        yaml.dump(data, f)

    logger.info(f"Saved agent config to {config_file}")


def x_save_agent_config__mutmut_12(repo_root: Path, config: AgentConfig) -> None:
    """Save agent configuration to .kittify/config.yaml.

    Merges with existing config (preserves other sections like vcs).

    Args:
        repo_root: Repository root directory
        config: AgentConfig to save
    """
    config_dir = repo_root / ".kittify"
    config_file = config_dir / "config.yaml"

    yaml = YAML()
    yaml.preserve_quotes = True

    # Load existing config or create new
    if config_file.exists():
        with open(None, "r") as f:
            data = yaml.load(f) or {}
    else:
        data = {}
        config_dir.mkdir(parents=True, exist_ok=True)

    # Update agents section
    data["agents"] = {
        "available": config.available,
        "selection": {
            "preferred_implementer": config.selection.preferred_implementer,
            "preferred_reviewer": config.selection.preferred_reviewer,
        },
    }

    # Write back
    with open(config_file, "w") as f:
        yaml.dump(data, f)

    logger.info(f"Saved agent config to {config_file}")


def x_save_agent_config__mutmut_13(repo_root: Path, config: AgentConfig) -> None:
    """Save agent configuration to .kittify/config.yaml.

    Merges with existing config (preserves other sections like vcs).

    Args:
        repo_root: Repository root directory
        config: AgentConfig to save
    """
    config_dir = repo_root / ".kittify"
    config_file = config_dir / "config.yaml"

    yaml = YAML()
    yaml.preserve_quotes = True

    # Load existing config or create new
    if config_file.exists():
        with open(config_file, None) as f:
            data = yaml.load(f) or {}
    else:
        data = {}
        config_dir.mkdir(parents=True, exist_ok=True)

    # Update agents section
    data["agents"] = {
        "available": config.available,
        "selection": {
            "preferred_implementer": config.selection.preferred_implementer,
            "preferred_reviewer": config.selection.preferred_reviewer,
        },
    }

    # Write back
    with open(config_file, "w") as f:
        yaml.dump(data, f)

    logger.info(f"Saved agent config to {config_file}")


def x_save_agent_config__mutmut_14(repo_root: Path, config: AgentConfig) -> None:
    """Save agent configuration to .kittify/config.yaml.

    Merges with existing config (preserves other sections like vcs).

    Args:
        repo_root: Repository root directory
        config: AgentConfig to save
    """
    config_dir = repo_root / ".kittify"
    config_file = config_dir / "config.yaml"

    yaml = YAML()
    yaml.preserve_quotes = True

    # Load existing config or create new
    if config_file.exists():
        with open("r") as f:
            data = yaml.load(f) or {}
    else:
        data = {}
        config_dir.mkdir(parents=True, exist_ok=True)

    # Update agents section
    data["agents"] = {
        "available": config.available,
        "selection": {
            "preferred_implementer": config.selection.preferred_implementer,
            "preferred_reviewer": config.selection.preferred_reviewer,
        },
    }

    # Write back
    with open(config_file, "w") as f:
        yaml.dump(data, f)

    logger.info(f"Saved agent config to {config_file}")


def x_save_agent_config__mutmut_15(repo_root: Path, config: AgentConfig) -> None:
    """Save agent configuration to .kittify/config.yaml.

    Merges with existing config (preserves other sections like vcs).

    Args:
        repo_root: Repository root directory
        config: AgentConfig to save
    """
    config_dir = repo_root / ".kittify"
    config_file = config_dir / "config.yaml"

    yaml = YAML()
    yaml.preserve_quotes = True

    # Load existing config or create new
    if config_file.exists():
        with open(config_file, ) as f:
            data = yaml.load(f) or {}
    else:
        data = {}
        config_dir.mkdir(parents=True, exist_ok=True)

    # Update agents section
    data["agents"] = {
        "available": config.available,
        "selection": {
            "preferred_implementer": config.selection.preferred_implementer,
            "preferred_reviewer": config.selection.preferred_reviewer,
        },
    }

    # Write back
    with open(config_file, "w") as f:
        yaml.dump(data, f)

    logger.info(f"Saved agent config to {config_file}")


def x_save_agent_config__mutmut_16(repo_root: Path, config: AgentConfig) -> None:
    """Save agent configuration to .kittify/config.yaml.

    Merges with existing config (preserves other sections like vcs).

    Args:
        repo_root: Repository root directory
        config: AgentConfig to save
    """
    config_dir = repo_root / ".kittify"
    config_file = config_dir / "config.yaml"

    yaml = YAML()
    yaml.preserve_quotes = True

    # Load existing config or create new
    if config_file.exists():
        with open(config_file, "XXrXX") as f:
            data = yaml.load(f) or {}
    else:
        data = {}
        config_dir.mkdir(parents=True, exist_ok=True)

    # Update agents section
    data["agents"] = {
        "available": config.available,
        "selection": {
            "preferred_implementer": config.selection.preferred_implementer,
            "preferred_reviewer": config.selection.preferred_reviewer,
        },
    }

    # Write back
    with open(config_file, "w") as f:
        yaml.dump(data, f)

    logger.info(f"Saved agent config to {config_file}")


def x_save_agent_config__mutmut_17(repo_root: Path, config: AgentConfig) -> None:
    """Save agent configuration to .kittify/config.yaml.

    Merges with existing config (preserves other sections like vcs).

    Args:
        repo_root: Repository root directory
        config: AgentConfig to save
    """
    config_dir = repo_root / ".kittify"
    config_file = config_dir / "config.yaml"

    yaml = YAML()
    yaml.preserve_quotes = True

    # Load existing config or create new
    if config_file.exists():
        with open(config_file, "R") as f:
            data = yaml.load(f) or {}
    else:
        data = {}
        config_dir.mkdir(parents=True, exist_ok=True)

    # Update agents section
    data["agents"] = {
        "available": config.available,
        "selection": {
            "preferred_implementer": config.selection.preferred_implementer,
            "preferred_reviewer": config.selection.preferred_reviewer,
        },
    }

    # Write back
    with open(config_file, "w") as f:
        yaml.dump(data, f)

    logger.info(f"Saved agent config to {config_file}")


def x_save_agent_config__mutmut_18(repo_root: Path, config: AgentConfig) -> None:
    """Save agent configuration to .kittify/config.yaml.

    Merges with existing config (preserves other sections like vcs).

    Args:
        repo_root: Repository root directory
        config: AgentConfig to save
    """
    config_dir = repo_root / ".kittify"
    config_file = config_dir / "config.yaml"

    yaml = YAML()
    yaml.preserve_quotes = True

    # Load existing config or create new
    if config_file.exists():
        with open(config_file, "r") as f:
            data = None
    else:
        data = {}
        config_dir.mkdir(parents=True, exist_ok=True)

    # Update agents section
    data["agents"] = {
        "available": config.available,
        "selection": {
            "preferred_implementer": config.selection.preferred_implementer,
            "preferred_reviewer": config.selection.preferred_reviewer,
        },
    }

    # Write back
    with open(config_file, "w") as f:
        yaml.dump(data, f)

    logger.info(f"Saved agent config to {config_file}")


def x_save_agent_config__mutmut_19(repo_root: Path, config: AgentConfig) -> None:
    """Save agent configuration to .kittify/config.yaml.

    Merges with existing config (preserves other sections like vcs).

    Args:
        repo_root: Repository root directory
        config: AgentConfig to save
    """
    config_dir = repo_root / ".kittify"
    config_file = config_dir / "config.yaml"

    yaml = YAML()
    yaml.preserve_quotes = True

    # Load existing config or create new
    if config_file.exists():
        with open(config_file, "r") as f:
            data = yaml.load(f) and {}
    else:
        data = {}
        config_dir.mkdir(parents=True, exist_ok=True)

    # Update agents section
    data["agents"] = {
        "available": config.available,
        "selection": {
            "preferred_implementer": config.selection.preferred_implementer,
            "preferred_reviewer": config.selection.preferred_reviewer,
        },
    }

    # Write back
    with open(config_file, "w") as f:
        yaml.dump(data, f)

    logger.info(f"Saved agent config to {config_file}")


def x_save_agent_config__mutmut_20(repo_root: Path, config: AgentConfig) -> None:
    """Save agent configuration to .kittify/config.yaml.

    Merges with existing config (preserves other sections like vcs).

    Args:
        repo_root: Repository root directory
        config: AgentConfig to save
    """
    config_dir = repo_root / ".kittify"
    config_file = config_dir / "config.yaml"

    yaml = YAML()
    yaml.preserve_quotes = True

    # Load existing config or create new
    if config_file.exists():
        with open(config_file, "r") as f:
            data = yaml.load(None) or {}
    else:
        data = {}
        config_dir.mkdir(parents=True, exist_ok=True)

    # Update agents section
    data["agents"] = {
        "available": config.available,
        "selection": {
            "preferred_implementer": config.selection.preferred_implementer,
            "preferred_reviewer": config.selection.preferred_reviewer,
        },
    }

    # Write back
    with open(config_file, "w") as f:
        yaml.dump(data, f)

    logger.info(f"Saved agent config to {config_file}")


def x_save_agent_config__mutmut_21(repo_root: Path, config: AgentConfig) -> None:
    """Save agent configuration to .kittify/config.yaml.

    Merges with existing config (preserves other sections like vcs).

    Args:
        repo_root: Repository root directory
        config: AgentConfig to save
    """
    config_dir = repo_root / ".kittify"
    config_file = config_dir / "config.yaml"

    yaml = YAML()
    yaml.preserve_quotes = True

    # Load existing config or create new
    if config_file.exists():
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    else:
        data = None
        config_dir.mkdir(parents=True, exist_ok=True)

    # Update agents section
    data["agents"] = {
        "available": config.available,
        "selection": {
            "preferred_implementer": config.selection.preferred_implementer,
            "preferred_reviewer": config.selection.preferred_reviewer,
        },
    }

    # Write back
    with open(config_file, "w") as f:
        yaml.dump(data, f)

    logger.info(f"Saved agent config to {config_file}")


def x_save_agent_config__mutmut_22(repo_root: Path, config: AgentConfig) -> None:
    """Save agent configuration to .kittify/config.yaml.

    Merges with existing config (preserves other sections like vcs).

    Args:
        repo_root: Repository root directory
        config: AgentConfig to save
    """
    config_dir = repo_root / ".kittify"
    config_file = config_dir / "config.yaml"

    yaml = YAML()
    yaml.preserve_quotes = True

    # Load existing config or create new
    if config_file.exists():
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    else:
        data = {}
        config_dir.mkdir(parents=None, exist_ok=True)

    # Update agents section
    data["agents"] = {
        "available": config.available,
        "selection": {
            "preferred_implementer": config.selection.preferred_implementer,
            "preferred_reviewer": config.selection.preferred_reviewer,
        },
    }

    # Write back
    with open(config_file, "w") as f:
        yaml.dump(data, f)

    logger.info(f"Saved agent config to {config_file}")


def x_save_agent_config__mutmut_23(repo_root: Path, config: AgentConfig) -> None:
    """Save agent configuration to .kittify/config.yaml.

    Merges with existing config (preserves other sections like vcs).

    Args:
        repo_root: Repository root directory
        config: AgentConfig to save
    """
    config_dir = repo_root / ".kittify"
    config_file = config_dir / "config.yaml"

    yaml = YAML()
    yaml.preserve_quotes = True

    # Load existing config or create new
    if config_file.exists():
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    else:
        data = {}
        config_dir.mkdir(parents=True, exist_ok=None)

    # Update agents section
    data["agents"] = {
        "available": config.available,
        "selection": {
            "preferred_implementer": config.selection.preferred_implementer,
            "preferred_reviewer": config.selection.preferred_reviewer,
        },
    }

    # Write back
    with open(config_file, "w") as f:
        yaml.dump(data, f)

    logger.info(f"Saved agent config to {config_file}")


def x_save_agent_config__mutmut_24(repo_root: Path, config: AgentConfig) -> None:
    """Save agent configuration to .kittify/config.yaml.

    Merges with existing config (preserves other sections like vcs).

    Args:
        repo_root: Repository root directory
        config: AgentConfig to save
    """
    config_dir = repo_root / ".kittify"
    config_file = config_dir / "config.yaml"

    yaml = YAML()
    yaml.preserve_quotes = True

    # Load existing config or create new
    if config_file.exists():
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    else:
        data = {}
        config_dir.mkdir(exist_ok=True)

    # Update agents section
    data["agents"] = {
        "available": config.available,
        "selection": {
            "preferred_implementer": config.selection.preferred_implementer,
            "preferred_reviewer": config.selection.preferred_reviewer,
        },
    }

    # Write back
    with open(config_file, "w") as f:
        yaml.dump(data, f)

    logger.info(f"Saved agent config to {config_file}")


def x_save_agent_config__mutmut_25(repo_root: Path, config: AgentConfig) -> None:
    """Save agent configuration to .kittify/config.yaml.

    Merges with existing config (preserves other sections like vcs).

    Args:
        repo_root: Repository root directory
        config: AgentConfig to save
    """
    config_dir = repo_root / ".kittify"
    config_file = config_dir / "config.yaml"

    yaml = YAML()
    yaml.preserve_quotes = True

    # Load existing config or create new
    if config_file.exists():
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    else:
        data = {}
        config_dir.mkdir(parents=True, )

    # Update agents section
    data["agents"] = {
        "available": config.available,
        "selection": {
            "preferred_implementer": config.selection.preferred_implementer,
            "preferred_reviewer": config.selection.preferred_reviewer,
        },
    }

    # Write back
    with open(config_file, "w") as f:
        yaml.dump(data, f)

    logger.info(f"Saved agent config to {config_file}")


def x_save_agent_config__mutmut_26(repo_root: Path, config: AgentConfig) -> None:
    """Save agent configuration to .kittify/config.yaml.

    Merges with existing config (preserves other sections like vcs).

    Args:
        repo_root: Repository root directory
        config: AgentConfig to save
    """
    config_dir = repo_root / ".kittify"
    config_file = config_dir / "config.yaml"

    yaml = YAML()
    yaml.preserve_quotes = True

    # Load existing config or create new
    if config_file.exists():
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    else:
        data = {}
        config_dir.mkdir(parents=False, exist_ok=True)

    # Update agents section
    data["agents"] = {
        "available": config.available,
        "selection": {
            "preferred_implementer": config.selection.preferred_implementer,
            "preferred_reviewer": config.selection.preferred_reviewer,
        },
    }

    # Write back
    with open(config_file, "w") as f:
        yaml.dump(data, f)

    logger.info(f"Saved agent config to {config_file}")


def x_save_agent_config__mutmut_27(repo_root: Path, config: AgentConfig) -> None:
    """Save agent configuration to .kittify/config.yaml.

    Merges with existing config (preserves other sections like vcs).

    Args:
        repo_root: Repository root directory
        config: AgentConfig to save
    """
    config_dir = repo_root / ".kittify"
    config_file = config_dir / "config.yaml"

    yaml = YAML()
    yaml.preserve_quotes = True

    # Load existing config or create new
    if config_file.exists():
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    else:
        data = {}
        config_dir.mkdir(parents=True, exist_ok=False)

    # Update agents section
    data["agents"] = {
        "available": config.available,
        "selection": {
            "preferred_implementer": config.selection.preferred_implementer,
            "preferred_reviewer": config.selection.preferred_reviewer,
        },
    }

    # Write back
    with open(config_file, "w") as f:
        yaml.dump(data, f)

    logger.info(f"Saved agent config to {config_file}")


def x_save_agent_config__mutmut_28(repo_root: Path, config: AgentConfig) -> None:
    """Save agent configuration to .kittify/config.yaml.

    Merges with existing config (preserves other sections like vcs).

    Args:
        repo_root: Repository root directory
        config: AgentConfig to save
    """
    config_dir = repo_root / ".kittify"
    config_file = config_dir / "config.yaml"

    yaml = YAML()
    yaml.preserve_quotes = True

    # Load existing config or create new
    if config_file.exists():
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    else:
        data = {}
        config_dir.mkdir(parents=True, exist_ok=True)

    # Update agents section
    data["agents"] = None

    # Write back
    with open(config_file, "w") as f:
        yaml.dump(data, f)

    logger.info(f"Saved agent config to {config_file}")


def x_save_agent_config__mutmut_29(repo_root: Path, config: AgentConfig) -> None:
    """Save agent configuration to .kittify/config.yaml.

    Merges with existing config (preserves other sections like vcs).

    Args:
        repo_root: Repository root directory
        config: AgentConfig to save
    """
    config_dir = repo_root / ".kittify"
    config_file = config_dir / "config.yaml"

    yaml = YAML()
    yaml.preserve_quotes = True

    # Load existing config or create new
    if config_file.exists():
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    else:
        data = {}
        config_dir.mkdir(parents=True, exist_ok=True)

    # Update agents section
    data["XXagentsXX"] = {
        "available": config.available,
        "selection": {
            "preferred_implementer": config.selection.preferred_implementer,
            "preferred_reviewer": config.selection.preferred_reviewer,
        },
    }

    # Write back
    with open(config_file, "w") as f:
        yaml.dump(data, f)

    logger.info(f"Saved agent config to {config_file}")


def x_save_agent_config__mutmut_30(repo_root: Path, config: AgentConfig) -> None:
    """Save agent configuration to .kittify/config.yaml.

    Merges with existing config (preserves other sections like vcs).

    Args:
        repo_root: Repository root directory
        config: AgentConfig to save
    """
    config_dir = repo_root / ".kittify"
    config_file = config_dir / "config.yaml"

    yaml = YAML()
    yaml.preserve_quotes = True

    # Load existing config or create new
    if config_file.exists():
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    else:
        data = {}
        config_dir.mkdir(parents=True, exist_ok=True)

    # Update agents section
    data["AGENTS"] = {
        "available": config.available,
        "selection": {
            "preferred_implementer": config.selection.preferred_implementer,
            "preferred_reviewer": config.selection.preferred_reviewer,
        },
    }

    # Write back
    with open(config_file, "w") as f:
        yaml.dump(data, f)

    logger.info(f"Saved agent config to {config_file}")


def x_save_agent_config__mutmut_31(repo_root: Path, config: AgentConfig) -> None:
    """Save agent configuration to .kittify/config.yaml.

    Merges with existing config (preserves other sections like vcs).

    Args:
        repo_root: Repository root directory
        config: AgentConfig to save
    """
    config_dir = repo_root / ".kittify"
    config_file = config_dir / "config.yaml"

    yaml = YAML()
    yaml.preserve_quotes = True

    # Load existing config or create new
    if config_file.exists():
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    else:
        data = {}
        config_dir.mkdir(parents=True, exist_ok=True)

    # Update agents section
    data["agents"] = {
        "XXavailableXX": config.available,
        "selection": {
            "preferred_implementer": config.selection.preferred_implementer,
            "preferred_reviewer": config.selection.preferred_reviewer,
        },
    }

    # Write back
    with open(config_file, "w") as f:
        yaml.dump(data, f)

    logger.info(f"Saved agent config to {config_file}")


def x_save_agent_config__mutmut_32(repo_root: Path, config: AgentConfig) -> None:
    """Save agent configuration to .kittify/config.yaml.

    Merges with existing config (preserves other sections like vcs).

    Args:
        repo_root: Repository root directory
        config: AgentConfig to save
    """
    config_dir = repo_root / ".kittify"
    config_file = config_dir / "config.yaml"

    yaml = YAML()
    yaml.preserve_quotes = True

    # Load existing config or create new
    if config_file.exists():
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    else:
        data = {}
        config_dir.mkdir(parents=True, exist_ok=True)

    # Update agents section
    data["agents"] = {
        "AVAILABLE": config.available,
        "selection": {
            "preferred_implementer": config.selection.preferred_implementer,
            "preferred_reviewer": config.selection.preferred_reviewer,
        },
    }

    # Write back
    with open(config_file, "w") as f:
        yaml.dump(data, f)

    logger.info(f"Saved agent config to {config_file}")


def x_save_agent_config__mutmut_33(repo_root: Path, config: AgentConfig) -> None:
    """Save agent configuration to .kittify/config.yaml.

    Merges with existing config (preserves other sections like vcs).

    Args:
        repo_root: Repository root directory
        config: AgentConfig to save
    """
    config_dir = repo_root / ".kittify"
    config_file = config_dir / "config.yaml"

    yaml = YAML()
    yaml.preserve_quotes = True

    # Load existing config or create new
    if config_file.exists():
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    else:
        data = {}
        config_dir.mkdir(parents=True, exist_ok=True)

    # Update agents section
    data["agents"] = {
        "available": config.available,
        "XXselectionXX": {
            "preferred_implementer": config.selection.preferred_implementer,
            "preferred_reviewer": config.selection.preferred_reviewer,
        },
    }

    # Write back
    with open(config_file, "w") as f:
        yaml.dump(data, f)

    logger.info(f"Saved agent config to {config_file}")


def x_save_agent_config__mutmut_34(repo_root: Path, config: AgentConfig) -> None:
    """Save agent configuration to .kittify/config.yaml.

    Merges with existing config (preserves other sections like vcs).

    Args:
        repo_root: Repository root directory
        config: AgentConfig to save
    """
    config_dir = repo_root / ".kittify"
    config_file = config_dir / "config.yaml"

    yaml = YAML()
    yaml.preserve_quotes = True

    # Load existing config or create new
    if config_file.exists():
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    else:
        data = {}
        config_dir.mkdir(parents=True, exist_ok=True)

    # Update agents section
    data["agents"] = {
        "available": config.available,
        "SELECTION": {
            "preferred_implementer": config.selection.preferred_implementer,
            "preferred_reviewer": config.selection.preferred_reviewer,
        },
    }

    # Write back
    with open(config_file, "w") as f:
        yaml.dump(data, f)

    logger.info(f"Saved agent config to {config_file}")


def x_save_agent_config__mutmut_35(repo_root: Path, config: AgentConfig) -> None:
    """Save agent configuration to .kittify/config.yaml.

    Merges with existing config (preserves other sections like vcs).

    Args:
        repo_root: Repository root directory
        config: AgentConfig to save
    """
    config_dir = repo_root / ".kittify"
    config_file = config_dir / "config.yaml"

    yaml = YAML()
    yaml.preserve_quotes = True

    # Load existing config or create new
    if config_file.exists():
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    else:
        data = {}
        config_dir.mkdir(parents=True, exist_ok=True)

    # Update agents section
    data["agents"] = {
        "available": config.available,
        "selection": {
            "XXpreferred_implementerXX": config.selection.preferred_implementer,
            "preferred_reviewer": config.selection.preferred_reviewer,
        },
    }

    # Write back
    with open(config_file, "w") as f:
        yaml.dump(data, f)

    logger.info(f"Saved agent config to {config_file}")


def x_save_agent_config__mutmut_36(repo_root: Path, config: AgentConfig) -> None:
    """Save agent configuration to .kittify/config.yaml.

    Merges with existing config (preserves other sections like vcs).

    Args:
        repo_root: Repository root directory
        config: AgentConfig to save
    """
    config_dir = repo_root / ".kittify"
    config_file = config_dir / "config.yaml"

    yaml = YAML()
    yaml.preserve_quotes = True

    # Load existing config or create new
    if config_file.exists():
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    else:
        data = {}
        config_dir.mkdir(parents=True, exist_ok=True)

    # Update agents section
    data["agents"] = {
        "available": config.available,
        "selection": {
            "PREFERRED_IMPLEMENTER": config.selection.preferred_implementer,
            "preferred_reviewer": config.selection.preferred_reviewer,
        },
    }

    # Write back
    with open(config_file, "w") as f:
        yaml.dump(data, f)

    logger.info(f"Saved agent config to {config_file}")


def x_save_agent_config__mutmut_37(repo_root: Path, config: AgentConfig) -> None:
    """Save agent configuration to .kittify/config.yaml.

    Merges with existing config (preserves other sections like vcs).

    Args:
        repo_root: Repository root directory
        config: AgentConfig to save
    """
    config_dir = repo_root / ".kittify"
    config_file = config_dir / "config.yaml"

    yaml = YAML()
    yaml.preserve_quotes = True

    # Load existing config or create new
    if config_file.exists():
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    else:
        data = {}
        config_dir.mkdir(parents=True, exist_ok=True)

    # Update agents section
    data["agents"] = {
        "available": config.available,
        "selection": {
            "preferred_implementer": config.selection.preferred_implementer,
            "XXpreferred_reviewerXX": config.selection.preferred_reviewer,
        },
    }

    # Write back
    with open(config_file, "w") as f:
        yaml.dump(data, f)

    logger.info(f"Saved agent config to {config_file}")


def x_save_agent_config__mutmut_38(repo_root: Path, config: AgentConfig) -> None:
    """Save agent configuration to .kittify/config.yaml.

    Merges with existing config (preserves other sections like vcs).

    Args:
        repo_root: Repository root directory
        config: AgentConfig to save
    """
    config_dir = repo_root / ".kittify"
    config_file = config_dir / "config.yaml"

    yaml = YAML()
    yaml.preserve_quotes = True

    # Load existing config or create new
    if config_file.exists():
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    else:
        data = {}
        config_dir.mkdir(parents=True, exist_ok=True)

    # Update agents section
    data["agents"] = {
        "available": config.available,
        "selection": {
            "preferred_implementer": config.selection.preferred_implementer,
            "PREFERRED_REVIEWER": config.selection.preferred_reviewer,
        },
    }

    # Write back
    with open(config_file, "w") as f:
        yaml.dump(data, f)

    logger.info(f"Saved agent config to {config_file}")


def x_save_agent_config__mutmut_39(repo_root: Path, config: AgentConfig) -> None:
    """Save agent configuration to .kittify/config.yaml.

    Merges with existing config (preserves other sections like vcs).

    Args:
        repo_root: Repository root directory
        config: AgentConfig to save
    """
    config_dir = repo_root / ".kittify"
    config_file = config_dir / "config.yaml"

    yaml = YAML()
    yaml.preserve_quotes = True

    # Load existing config or create new
    if config_file.exists():
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    else:
        data = {}
        config_dir.mkdir(parents=True, exist_ok=True)

    # Update agents section
    data["agents"] = {
        "available": config.available,
        "selection": {
            "preferred_implementer": config.selection.preferred_implementer,
            "preferred_reviewer": config.selection.preferred_reviewer,
        },
    }

    # Write back
    with open(None, "w") as f:
        yaml.dump(data, f)

    logger.info(f"Saved agent config to {config_file}")


def x_save_agent_config__mutmut_40(repo_root: Path, config: AgentConfig) -> None:
    """Save agent configuration to .kittify/config.yaml.

    Merges with existing config (preserves other sections like vcs).

    Args:
        repo_root: Repository root directory
        config: AgentConfig to save
    """
    config_dir = repo_root / ".kittify"
    config_file = config_dir / "config.yaml"

    yaml = YAML()
    yaml.preserve_quotes = True

    # Load existing config or create new
    if config_file.exists():
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    else:
        data = {}
        config_dir.mkdir(parents=True, exist_ok=True)

    # Update agents section
    data["agents"] = {
        "available": config.available,
        "selection": {
            "preferred_implementer": config.selection.preferred_implementer,
            "preferred_reviewer": config.selection.preferred_reviewer,
        },
    }

    # Write back
    with open(config_file, None) as f:
        yaml.dump(data, f)

    logger.info(f"Saved agent config to {config_file}")


def x_save_agent_config__mutmut_41(repo_root: Path, config: AgentConfig) -> None:
    """Save agent configuration to .kittify/config.yaml.

    Merges with existing config (preserves other sections like vcs).

    Args:
        repo_root: Repository root directory
        config: AgentConfig to save
    """
    config_dir = repo_root / ".kittify"
    config_file = config_dir / "config.yaml"

    yaml = YAML()
    yaml.preserve_quotes = True

    # Load existing config or create new
    if config_file.exists():
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    else:
        data = {}
        config_dir.mkdir(parents=True, exist_ok=True)

    # Update agents section
    data["agents"] = {
        "available": config.available,
        "selection": {
            "preferred_implementer": config.selection.preferred_implementer,
            "preferred_reviewer": config.selection.preferred_reviewer,
        },
    }

    # Write back
    with open("w") as f:
        yaml.dump(data, f)

    logger.info(f"Saved agent config to {config_file}")


def x_save_agent_config__mutmut_42(repo_root: Path, config: AgentConfig) -> None:
    """Save agent configuration to .kittify/config.yaml.

    Merges with existing config (preserves other sections like vcs).

    Args:
        repo_root: Repository root directory
        config: AgentConfig to save
    """
    config_dir = repo_root / ".kittify"
    config_file = config_dir / "config.yaml"

    yaml = YAML()
    yaml.preserve_quotes = True

    # Load existing config or create new
    if config_file.exists():
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    else:
        data = {}
        config_dir.mkdir(parents=True, exist_ok=True)

    # Update agents section
    data["agents"] = {
        "available": config.available,
        "selection": {
            "preferred_implementer": config.selection.preferred_implementer,
            "preferred_reviewer": config.selection.preferred_reviewer,
        },
    }

    # Write back
    with open(config_file, ) as f:
        yaml.dump(data, f)

    logger.info(f"Saved agent config to {config_file}")


def x_save_agent_config__mutmut_43(repo_root: Path, config: AgentConfig) -> None:
    """Save agent configuration to .kittify/config.yaml.

    Merges with existing config (preserves other sections like vcs).

    Args:
        repo_root: Repository root directory
        config: AgentConfig to save
    """
    config_dir = repo_root / ".kittify"
    config_file = config_dir / "config.yaml"

    yaml = YAML()
    yaml.preserve_quotes = True

    # Load existing config or create new
    if config_file.exists():
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    else:
        data = {}
        config_dir.mkdir(parents=True, exist_ok=True)

    # Update agents section
    data["agents"] = {
        "available": config.available,
        "selection": {
            "preferred_implementer": config.selection.preferred_implementer,
            "preferred_reviewer": config.selection.preferred_reviewer,
        },
    }

    # Write back
    with open(config_file, "XXwXX") as f:
        yaml.dump(data, f)

    logger.info(f"Saved agent config to {config_file}")


def x_save_agent_config__mutmut_44(repo_root: Path, config: AgentConfig) -> None:
    """Save agent configuration to .kittify/config.yaml.

    Merges with existing config (preserves other sections like vcs).

    Args:
        repo_root: Repository root directory
        config: AgentConfig to save
    """
    config_dir = repo_root / ".kittify"
    config_file = config_dir / "config.yaml"

    yaml = YAML()
    yaml.preserve_quotes = True

    # Load existing config or create new
    if config_file.exists():
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    else:
        data = {}
        config_dir.mkdir(parents=True, exist_ok=True)

    # Update agents section
    data["agents"] = {
        "available": config.available,
        "selection": {
            "preferred_implementer": config.selection.preferred_implementer,
            "preferred_reviewer": config.selection.preferred_reviewer,
        },
    }

    # Write back
    with open(config_file, "W") as f:
        yaml.dump(data, f)

    logger.info(f"Saved agent config to {config_file}")


def x_save_agent_config__mutmut_45(repo_root: Path, config: AgentConfig) -> None:
    """Save agent configuration to .kittify/config.yaml.

    Merges with existing config (preserves other sections like vcs).

    Args:
        repo_root: Repository root directory
        config: AgentConfig to save
    """
    config_dir = repo_root / ".kittify"
    config_file = config_dir / "config.yaml"

    yaml = YAML()
    yaml.preserve_quotes = True

    # Load existing config or create new
    if config_file.exists():
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    else:
        data = {}
        config_dir.mkdir(parents=True, exist_ok=True)

    # Update agents section
    data["agents"] = {
        "available": config.available,
        "selection": {
            "preferred_implementer": config.selection.preferred_implementer,
            "preferred_reviewer": config.selection.preferred_reviewer,
        },
    }

    # Write back
    with open(config_file, "w") as f:
        yaml.dump(None, f)

    logger.info(f"Saved agent config to {config_file}")


def x_save_agent_config__mutmut_46(repo_root: Path, config: AgentConfig) -> None:
    """Save agent configuration to .kittify/config.yaml.

    Merges with existing config (preserves other sections like vcs).

    Args:
        repo_root: Repository root directory
        config: AgentConfig to save
    """
    config_dir = repo_root / ".kittify"
    config_file = config_dir / "config.yaml"

    yaml = YAML()
    yaml.preserve_quotes = True

    # Load existing config or create new
    if config_file.exists():
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    else:
        data = {}
        config_dir.mkdir(parents=True, exist_ok=True)

    # Update agents section
    data["agents"] = {
        "available": config.available,
        "selection": {
            "preferred_implementer": config.selection.preferred_implementer,
            "preferred_reviewer": config.selection.preferred_reviewer,
        },
    }

    # Write back
    with open(config_file, "w") as f:
        yaml.dump(data, None)

    logger.info(f"Saved agent config to {config_file}")


def x_save_agent_config__mutmut_47(repo_root: Path, config: AgentConfig) -> None:
    """Save agent configuration to .kittify/config.yaml.

    Merges with existing config (preserves other sections like vcs).

    Args:
        repo_root: Repository root directory
        config: AgentConfig to save
    """
    config_dir = repo_root / ".kittify"
    config_file = config_dir / "config.yaml"

    yaml = YAML()
    yaml.preserve_quotes = True

    # Load existing config or create new
    if config_file.exists():
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    else:
        data = {}
        config_dir.mkdir(parents=True, exist_ok=True)

    # Update agents section
    data["agents"] = {
        "available": config.available,
        "selection": {
            "preferred_implementer": config.selection.preferred_implementer,
            "preferred_reviewer": config.selection.preferred_reviewer,
        },
    }

    # Write back
    with open(config_file, "w") as f:
        yaml.dump(f)

    logger.info(f"Saved agent config to {config_file}")


def x_save_agent_config__mutmut_48(repo_root: Path, config: AgentConfig) -> None:
    """Save agent configuration to .kittify/config.yaml.

    Merges with existing config (preserves other sections like vcs).

    Args:
        repo_root: Repository root directory
        config: AgentConfig to save
    """
    config_dir = repo_root / ".kittify"
    config_file = config_dir / "config.yaml"

    yaml = YAML()
    yaml.preserve_quotes = True

    # Load existing config or create new
    if config_file.exists():
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    else:
        data = {}
        config_dir.mkdir(parents=True, exist_ok=True)

    # Update agents section
    data["agents"] = {
        "available": config.available,
        "selection": {
            "preferred_implementer": config.selection.preferred_implementer,
            "preferred_reviewer": config.selection.preferred_reviewer,
        },
    }

    # Write back
    with open(config_file, "w") as f:
        yaml.dump(data, )

    logger.info(f"Saved agent config to {config_file}")


def x_save_agent_config__mutmut_49(repo_root: Path, config: AgentConfig) -> None:
    """Save agent configuration to .kittify/config.yaml.

    Merges with existing config (preserves other sections like vcs).

    Args:
        repo_root: Repository root directory
        config: AgentConfig to save
    """
    config_dir = repo_root / ".kittify"
    config_file = config_dir / "config.yaml"

    yaml = YAML()
    yaml.preserve_quotes = True

    # Load existing config or create new
    if config_file.exists():
        with open(config_file, "r") as f:
            data = yaml.load(f) or {}
    else:
        data = {}
        config_dir.mkdir(parents=True, exist_ok=True)

    # Update agents section
    data["agents"] = {
        "available": config.available,
        "selection": {
            "preferred_implementer": config.selection.preferred_implementer,
            "preferred_reviewer": config.selection.preferred_reviewer,
        },
    }

    # Write back
    with open(config_file, "w") as f:
        yaml.dump(data, f)

    logger.info(None)

x_save_agent_config__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_save_agent_config__mutmut_1': x_save_agent_config__mutmut_1, 
    'x_save_agent_config__mutmut_2': x_save_agent_config__mutmut_2, 
    'x_save_agent_config__mutmut_3': x_save_agent_config__mutmut_3, 
    'x_save_agent_config__mutmut_4': x_save_agent_config__mutmut_4, 
    'x_save_agent_config__mutmut_5': x_save_agent_config__mutmut_5, 
    'x_save_agent_config__mutmut_6': x_save_agent_config__mutmut_6, 
    'x_save_agent_config__mutmut_7': x_save_agent_config__mutmut_7, 
    'x_save_agent_config__mutmut_8': x_save_agent_config__mutmut_8, 
    'x_save_agent_config__mutmut_9': x_save_agent_config__mutmut_9, 
    'x_save_agent_config__mutmut_10': x_save_agent_config__mutmut_10, 
    'x_save_agent_config__mutmut_11': x_save_agent_config__mutmut_11, 
    'x_save_agent_config__mutmut_12': x_save_agent_config__mutmut_12, 
    'x_save_agent_config__mutmut_13': x_save_agent_config__mutmut_13, 
    'x_save_agent_config__mutmut_14': x_save_agent_config__mutmut_14, 
    'x_save_agent_config__mutmut_15': x_save_agent_config__mutmut_15, 
    'x_save_agent_config__mutmut_16': x_save_agent_config__mutmut_16, 
    'x_save_agent_config__mutmut_17': x_save_agent_config__mutmut_17, 
    'x_save_agent_config__mutmut_18': x_save_agent_config__mutmut_18, 
    'x_save_agent_config__mutmut_19': x_save_agent_config__mutmut_19, 
    'x_save_agent_config__mutmut_20': x_save_agent_config__mutmut_20, 
    'x_save_agent_config__mutmut_21': x_save_agent_config__mutmut_21, 
    'x_save_agent_config__mutmut_22': x_save_agent_config__mutmut_22, 
    'x_save_agent_config__mutmut_23': x_save_agent_config__mutmut_23, 
    'x_save_agent_config__mutmut_24': x_save_agent_config__mutmut_24, 
    'x_save_agent_config__mutmut_25': x_save_agent_config__mutmut_25, 
    'x_save_agent_config__mutmut_26': x_save_agent_config__mutmut_26, 
    'x_save_agent_config__mutmut_27': x_save_agent_config__mutmut_27, 
    'x_save_agent_config__mutmut_28': x_save_agent_config__mutmut_28, 
    'x_save_agent_config__mutmut_29': x_save_agent_config__mutmut_29, 
    'x_save_agent_config__mutmut_30': x_save_agent_config__mutmut_30, 
    'x_save_agent_config__mutmut_31': x_save_agent_config__mutmut_31, 
    'x_save_agent_config__mutmut_32': x_save_agent_config__mutmut_32, 
    'x_save_agent_config__mutmut_33': x_save_agent_config__mutmut_33, 
    'x_save_agent_config__mutmut_34': x_save_agent_config__mutmut_34, 
    'x_save_agent_config__mutmut_35': x_save_agent_config__mutmut_35, 
    'x_save_agent_config__mutmut_36': x_save_agent_config__mutmut_36, 
    'x_save_agent_config__mutmut_37': x_save_agent_config__mutmut_37, 
    'x_save_agent_config__mutmut_38': x_save_agent_config__mutmut_38, 
    'x_save_agent_config__mutmut_39': x_save_agent_config__mutmut_39, 
    'x_save_agent_config__mutmut_40': x_save_agent_config__mutmut_40, 
    'x_save_agent_config__mutmut_41': x_save_agent_config__mutmut_41, 
    'x_save_agent_config__mutmut_42': x_save_agent_config__mutmut_42, 
    'x_save_agent_config__mutmut_43': x_save_agent_config__mutmut_43, 
    'x_save_agent_config__mutmut_44': x_save_agent_config__mutmut_44, 
    'x_save_agent_config__mutmut_45': x_save_agent_config__mutmut_45, 
    'x_save_agent_config__mutmut_46': x_save_agent_config__mutmut_46, 
    'x_save_agent_config__mutmut_47': x_save_agent_config__mutmut_47, 
    'x_save_agent_config__mutmut_48': x_save_agent_config__mutmut_48, 
    'x_save_agent_config__mutmut_49': x_save_agent_config__mutmut_49
}
x_save_agent_config__mutmut_orig.__name__ = 'x_save_agent_config'


def get_configured_agents(repo_root: Path) -> list[str]:
    args = [repo_root]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_get_configured_agents__mutmut_orig, x_get_configured_agents__mutmut_mutants, args, kwargs, None)


def x_get_configured_agents__mutmut_orig(repo_root: Path) -> list[str]:
    """Get list of configured agents.

    This is the DEFINITIVE list of available agents, set during init.

    Args:
        repo_root: Repository root directory

    Returns:
        List of agent IDs, empty if not configured
    """
    config = load_agent_config(repo_root)
    return config.available


def x_get_configured_agents__mutmut_1(repo_root: Path) -> list[str]:
    """Get list of configured agents.

    This is the DEFINITIVE list of available agents, set during init.

    Args:
        repo_root: Repository root directory

    Returns:
        List of agent IDs, empty if not configured
    """
    config = None
    return config.available


def x_get_configured_agents__mutmut_2(repo_root: Path) -> list[str]:
    """Get list of configured agents.

    This is the DEFINITIVE list of available agents, set during init.

    Args:
        repo_root: Repository root directory

    Returns:
        List of agent IDs, empty if not configured
    """
    config = load_agent_config(None)
    return config.available

x_get_configured_agents__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_get_configured_agents__mutmut_1': x_get_configured_agents__mutmut_1, 
    'x_get_configured_agents__mutmut_2': x_get_configured_agents__mutmut_2
}
x_get_configured_agents__mutmut_orig.__name__ = 'x_get_configured_agents'


__all__ = [
    "AgentSelectionConfig",
    "AgentConfig",
    "AgentConfigError",
    "load_agent_config",
    "save_agent_config",
    "get_configured_agents",
]
