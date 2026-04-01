"""Deprecated agent_config shim — use specify_cli.core.tool_config instead.

All symbols are re-exported from the canonical ``tool_config`` module.
Importing this module emits a :class:`DeprecationWarning` so that callers
can migrate at their own pace.
"""

from __future__ import annotations

import warnings as _warnings

_warnings.warn(
    "specify_cli.core.agent_config is deprecated; "
    "use specify_cli.core.tool_config instead.",
    DeprecationWarning,
    stacklevel=2,
)

from specify_cli.core.tool_config import (  # noqa: E402, F401
    ToolConfig as AgentConfig,
    ToolConfigError as AgentConfigError,
    ToolSelectionConfig as AgentSelectionConfig,
    get_auto_commit_default,
    get_configured_tools as get_configured_agents,
    load_tool_config as load_agent_config,
    save_tool_config as save_agent_config,
)

__all__ = [
    "AgentConfig",
    "AgentConfigError",
    "AgentSelectionConfig",
    "get_auto_commit_default",
    "get_configured_agents",
    "load_agent_config",
    "save_agent_config",
]
