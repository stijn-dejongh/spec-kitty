"""Tool availability helpers for Spec Kitty."""

from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path
from typing import Dict, Mapping, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from specify_cli.cli import StepTracker

from specify_cli.core.config import AGENT_TOOL_REQUIREMENTS, IDE_AGENTS

CLAUDE_LOCAL_PATH = Path.home() / ".claude" / "local" / "claude"
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


def check_tool_for_tracker(tool: str, tracker: "StepTracker") -> bool:
    args = [tool, tracker]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_check_tool_for_tracker__mutmut_orig, x_check_tool_for_tracker__mutmut_mutants, args, kwargs, None)


def x_check_tool_for_tracker__mutmut_orig(tool: str, tracker: "StepTracker") -> bool:
    """Check if a tool is installed and update the provided StepTracker instance."""
    if shutil.which(tool):
        tracker.complete(tool, "available")
        return True
    tracker.error(tool, "not found")
    return False


def x_check_tool_for_tracker__mutmut_1(tool: str, tracker: "StepTracker") -> bool:
    """Check if a tool is installed and update the provided StepTracker instance."""
    if shutil.which(None):
        tracker.complete(tool, "available")
        return True
    tracker.error(tool, "not found")
    return False


def x_check_tool_for_tracker__mutmut_2(tool: str, tracker: "StepTracker") -> bool:
    """Check if a tool is installed and update the provided StepTracker instance."""
    if shutil.which(tool):
        tracker.complete(None, "available")
        return True
    tracker.error(tool, "not found")
    return False


def x_check_tool_for_tracker__mutmut_3(tool: str, tracker: "StepTracker") -> bool:
    """Check if a tool is installed and update the provided StepTracker instance."""
    if shutil.which(tool):
        tracker.complete(tool, None)
        return True
    tracker.error(tool, "not found")
    return False


def x_check_tool_for_tracker__mutmut_4(tool: str, tracker: "StepTracker") -> bool:
    """Check if a tool is installed and update the provided StepTracker instance."""
    if shutil.which(tool):
        tracker.complete("available")
        return True
    tracker.error(tool, "not found")
    return False


def x_check_tool_for_tracker__mutmut_5(tool: str, tracker: "StepTracker") -> bool:
    """Check if a tool is installed and update the provided StepTracker instance."""
    if shutil.which(tool):
        tracker.complete(tool, )
        return True
    tracker.error(tool, "not found")
    return False


def x_check_tool_for_tracker__mutmut_6(tool: str, tracker: "StepTracker") -> bool:
    """Check if a tool is installed and update the provided StepTracker instance."""
    if shutil.which(tool):
        tracker.complete(tool, "XXavailableXX")
        return True
    tracker.error(tool, "not found")
    return False


def x_check_tool_for_tracker__mutmut_7(tool: str, tracker: "StepTracker") -> bool:
    """Check if a tool is installed and update the provided StepTracker instance."""
    if shutil.which(tool):
        tracker.complete(tool, "AVAILABLE")
        return True
    tracker.error(tool, "not found")
    return False


def x_check_tool_for_tracker__mutmut_8(tool: str, tracker: "StepTracker") -> bool:
    """Check if a tool is installed and update the provided StepTracker instance."""
    if shutil.which(tool):
        tracker.complete(tool, "available")
        return False
    tracker.error(tool, "not found")
    return False


def x_check_tool_for_tracker__mutmut_9(tool: str, tracker: "StepTracker") -> bool:
    """Check if a tool is installed and update the provided StepTracker instance."""
    if shutil.which(tool):
        tracker.complete(tool, "available")
        return True
    tracker.error(None, "not found")
    return False


def x_check_tool_for_tracker__mutmut_10(tool: str, tracker: "StepTracker") -> bool:
    """Check if a tool is installed and update the provided StepTracker instance."""
    if shutil.which(tool):
        tracker.complete(tool, "available")
        return True
    tracker.error(tool, None)
    return False


def x_check_tool_for_tracker__mutmut_11(tool: str, tracker: "StepTracker") -> bool:
    """Check if a tool is installed and update the provided StepTracker instance."""
    if shutil.which(tool):
        tracker.complete(tool, "available")
        return True
    tracker.error("not found")
    return False


def x_check_tool_for_tracker__mutmut_12(tool: str, tracker: "StepTracker") -> bool:
    """Check if a tool is installed and update the provided StepTracker instance."""
    if shutil.which(tool):
        tracker.complete(tool, "available")
        return True
    tracker.error(tool, )
    return False


def x_check_tool_for_tracker__mutmut_13(tool: str, tracker: "StepTracker") -> bool:
    """Check if a tool is installed and update the provided StepTracker instance."""
    if shutil.which(tool):
        tracker.complete(tool, "available")
        return True
    tracker.error(tool, "XXnot foundXX")
    return False


def x_check_tool_for_tracker__mutmut_14(tool: str, tracker: "StepTracker") -> bool:
    """Check if a tool is installed and update the provided StepTracker instance."""
    if shutil.which(tool):
        tracker.complete(tool, "available")
        return True
    tracker.error(tool, "NOT FOUND")
    return False


def x_check_tool_for_tracker__mutmut_15(tool: str, tracker: "StepTracker") -> bool:
    """Check if a tool is installed and update the provided StepTracker instance."""
    if shutil.which(tool):
        tracker.complete(tool, "available")
        return True
    tracker.error(tool, "not found")
    return True

x_check_tool_for_tracker__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_check_tool_for_tracker__mutmut_1': x_check_tool_for_tracker__mutmut_1, 
    'x_check_tool_for_tracker__mutmut_2': x_check_tool_for_tracker__mutmut_2, 
    'x_check_tool_for_tracker__mutmut_3': x_check_tool_for_tracker__mutmut_3, 
    'x_check_tool_for_tracker__mutmut_4': x_check_tool_for_tracker__mutmut_4, 
    'x_check_tool_for_tracker__mutmut_5': x_check_tool_for_tracker__mutmut_5, 
    'x_check_tool_for_tracker__mutmut_6': x_check_tool_for_tracker__mutmut_6, 
    'x_check_tool_for_tracker__mutmut_7': x_check_tool_for_tracker__mutmut_7, 
    'x_check_tool_for_tracker__mutmut_8': x_check_tool_for_tracker__mutmut_8, 
    'x_check_tool_for_tracker__mutmut_9': x_check_tool_for_tracker__mutmut_9, 
    'x_check_tool_for_tracker__mutmut_10': x_check_tool_for_tracker__mutmut_10, 
    'x_check_tool_for_tracker__mutmut_11': x_check_tool_for_tracker__mutmut_11, 
    'x_check_tool_for_tracker__mutmut_12': x_check_tool_for_tracker__mutmut_12, 
    'x_check_tool_for_tracker__mutmut_13': x_check_tool_for_tracker__mutmut_13, 
    'x_check_tool_for_tracker__mutmut_14': x_check_tool_for_tracker__mutmut_14, 
    'x_check_tool_for_tracker__mutmut_15': x_check_tool_for_tracker__mutmut_15
}
x_check_tool_for_tracker__mutmut_orig.__name__ = 'x_check_tool_for_tracker'


def check_tool(tool: str, install_hint: str, agent_name: str | None = None) -> bool:
    args = [tool, install_hint, agent_name]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_check_tool__mutmut_orig, x_check_tool__mutmut_mutants, args, kwargs, None)


def x_check_tool__mutmut_orig(tool: str, install_hint: str, agent_name: str | None = None) -> bool:
    """Return True when the tool is available on PATH (with Claude CLI override and IDE agent bypass).

    IDE-integrated agents (cursor, windsurf, copilot, kilocode) don't require CLI
    installation, so we skip the availability check for them.
    """
    # Skip CLI checks for IDE agents - they run within the IDE, not as CLI tools
    if agent_name and agent_name in IDE_AGENTS:
        return True

    # Special case: Claude local installation
    if tool == "claude" and CLAUDE_LOCAL_PATH.exists() and CLAUDE_LOCAL_PATH.is_file():
        return True

    return shutil.which(tool) is not None


def x_check_tool__mutmut_1(tool: str, install_hint: str, agent_name: str | None = None) -> bool:
    """Return True when the tool is available on PATH (with Claude CLI override and IDE agent bypass).

    IDE-integrated agents (cursor, windsurf, copilot, kilocode) don't require CLI
    installation, so we skip the availability check for them.
    """
    # Skip CLI checks for IDE agents - they run within the IDE, not as CLI tools
    if agent_name or agent_name in IDE_AGENTS:
        return True

    # Special case: Claude local installation
    if tool == "claude" and CLAUDE_LOCAL_PATH.exists() and CLAUDE_LOCAL_PATH.is_file():
        return True

    return shutil.which(tool) is not None


def x_check_tool__mutmut_2(tool: str, install_hint: str, agent_name: str | None = None) -> bool:
    """Return True when the tool is available on PATH (with Claude CLI override and IDE agent bypass).

    IDE-integrated agents (cursor, windsurf, copilot, kilocode) don't require CLI
    installation, so we skip the availability check for them.
    """
    # Skip CLI checks for IDE agents - they run within the IDE, not as CLI tools
    if agent_name and agent_name not in IDE_AGENTS:
        return True

    # Special case: Claude local installation
    if tool == "claude" and CLAUDE_LOCAL_PATH.exists() and CLAUDE_LOCAL_PATH.is_file():
        return True

    return shutil.which(tool) is not None


def x_check_tool__mutmut_3(tool: str, install_hint: str, agent_name: str | None = None) -> bool:
    """Return True when the tool is available on PATH (with Claude CLI override and IDE agent bypass).

    IDE-integrated agents (cursor, windsurf, copilot, kilocode) don't require CLI
    installation, so we skip the availability check for them.
    """
    # Skip CLI checks for IDE agents - they run within the IDE, not as CLI tools
    if agent_name and agent_name in IDE_AGENTS:
        return False

    # Special case: Claude local installation
    if tool == "claude" and CLAUDE_LOCAL_PATH.exists() and CLAUDE_LOCAL_PATH.is_file():
        return True

    return shutil.which(tool) is not None


def x_check_tool__mutmut_4(tool: str, install_hint: str, agent_name: str | None = None) -> bool:
    """Return True when the tool is available on PATH (with Claude CLI override and IDE agent bypass).

    IDE-integrated agents (cursor, windsurf, copilot, kilocode) don't require CLI
    installation, so we skip the availability check for them.
    """
    # Skip CLI checks for IDE agents - they run within the IDE, not as CLI tools
    if agent_name and agent_name in IDE_AGENTS:
        return True

    # Special case: Claude local installation
    if tool == "claude" and CLAUDE_LOCAL_PATH.exists() or CLAUDE_LOCAL_PATH.is_file():
        return True

    return shutil.which(tool) is not None


def x_check_tool__mutmut_5(tool: str, install_hint: str, agent_name: str | None = None) -> bool:
    """Return True when the tool is available on PATH (with Claude CLI override and IDE agent bypass).

    IDE-integrated agents (cursor, windsurf, copilot, kilocode) don't require CLI
    installation, so we skip the availability check for them.
    """
    # Skip CLI checks for IDE agents - they run within the IDE, not as CLI tools
    if agent_name and agent_name in IDE_AGENTS:
        return True

    # Special case: Claude local installation
    if tool == "claude" or CLAUDE_LOCAL_PATH.exists() and CLAUDE_LOCAL_PATH.is_file():
        return True

    return shutil.which(tool) is not None


def x_check_tool__mutmut_6(tool: str, install_hint: str, agent_name: str | None = None) -> bool:
    """Return True when the tool is available on PATH (with Claude CLI override and IDE agent bypass).

    IDE-integrated agents (cursor, windsurf, copilot, kilocode) don't require CLI
    installation, so we skip the availability check for them.
    """
    # Skip CLI checks for IDE agents - they run within the IDE, not as CLI tools
    if agent_name and agent_name in IDE_AGENTS:
        return True

    # Special case: Claude local installation
    if tool != "claude" and CLAUDE_LOCAL_PATH.exists() and CLAUDE_LOCAL_PATH.is_file():
        return True

    return shutil.which(tool) is not None


def x_check_tool__mutmut_7(tool: str, install_hint: str, agent_name: str | None = None) -> bool:
    """Return True when the tool is available on PATH (with Claude CLI override and IDE agent bypass).

    IDE-integrated agents (cursor, windsurf, copilot, kilocode) don't require CLI
    installation, so we skip the availability check for them.
    """
    # Skip CLI checks for IDE agents - they run within the IDE, not as CLI tools
    if agent_name and agent_name in IDE_AGENTS:
        return True

    # Special case: Claude local installation
    if tool == "XXclaudeXX" and CLAUDE_LOCAL_PATH.exists() and CLAUDE_LOCAL_PATH.is_file():
        return True

    return shutil.which(tool) is not None


def x_check_tool__mutmut_8(tool: str, install_hint: str, agent_name: str | None = None) -> bool:
    """Return True when the tool is available on PATH (with Claude CLI override and IDE agent bypass).

    IDE-integrated agents (cursor, windsurf, copilot, kilocode) don't require CLI
    installation, so we skip the availability check for them.
    """
    # Skip CLI checks for IDE agents - they run within the IDE, not as CLI tools
    if agent_name and agent_name in IDE_AGENTS:
        return True

    # Special case: Claude local installation
    if tool == "CLAUDE" and CLAUDE_LOCAL_PATH.exists() and CLAUDE_LOCAL_PATH.is_file():
        return True

    return shutil.which(tool) is not None


def x_check_tool__mutmut_9(tool: str, install_hint: str, agent_name: str | None = None) -> bool:
    """Return True when the tool is available on PATH (with Claude CLI override and IDE agent bypass).

    IDE-integrated agents (cursor, windsurf, copilot, kilocode) don't require CLI
    installation, so we skip the availability check for them.
    """
    # Skip CLI checks for IDE agents - they run within the IDE, not as CLI tools
    if agent_name and agent_name in IDE_AGENTS:
        return True

    # Special case: Claude local installation
    if tool == "claude" and CLAUDE_LOCAL_PATH.exists() and CLAUDE_LOCAL_PATH.is_file():
        return False

    return shutil.which(tool) is not None


def x_check_tool__mutmut_10(tool: str, install_hint: str, agent_name: str | None = None) -> bool:
    """Return True when the tool is available on PATH (with Claude CLI override and IDE agent bypass).

    IDE-integrated agents (cursor, windsurf, copilot, kilocode) don't require CLI
    installation, so we skip the availability check for them.
    """
    # Skip CLI checks for IDE agents - they run within the IDE, not as CLI tools
    if agent_name and agent_name in IDE_AGENTS:
        return True

    # Special case: Claude local installation
    if tool == "claude" and CLAUDE_LOCAL_PATH.exists() and CLAUDE_LOCAL_PATH.is_file():
        return True

    return shutil.which(None) is not None


def x_check_tool__mutmut_11(tool: str, install_hint: str, agent_name: str | None = None) -> bool:
    """Return True when the tool is available on PATH (with Claude CLI override and IDE agent bypass).

    IDE-integrated agents (cursor, windsurf, copilot, kilocode) don't require CLI
    installation, so we skip the availability check for them.
    """
    # Skip CLI checks for IDE agents - they run within the IDE, not as CLI tools
    if agent_name and agent_name in IDE_AGENTS:
        return True

    # Special case: Claude local installation
    if tool == "claude" and CLAUDE_LOCAL_PATH.exists() and CLAUDE_LOCAL_PATH.is_file():
        return True

    return shutil.which(tool) is None

x_check_tool__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_check_tool__mutmut_1': x_check_tool__mutmut_1, 
    'x_check_tool__mutmut_2': x_check_tool__mutmut_2, 
    'x_check_tool__mutmut_3': x_check_tool__mutmut_3, 
    'x_check_tool__mutmut_4': x_check_tool__mutmut_4, 
    'x_check_tool__mutmut_5': x_check_tool__mutmut_5, 
    'x_check_tool__mutmut_6': x_check_tool__mutmut_6, 
    'x_check_tool__mutmut_7': x_check_tool__mutmut_7, 
    'x_check_tool__mutmut_8': x_check_tool__mutmut_8, 
    'x_check_tool__mutmut_9': x_check_tool__mutmut_9, 
    'x_check_tool__mutmut_10': x_check_tool__mutmut_10, 
    'x_check_tool__mutmut_11': x_check_tool__mutmut_11
}
x_check_tool__mutmut_orig.__name__ = 'x_check_tool'


def get_tool_version(command: str) -> str | None:
    args = [command]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_get_tool_version__mutmut_orig, x_get_tool_version__mutmut_mutants, args, kwargs, None)


def x_get_tool_version__mutmut_orig(command: str) -> str | None:
    """Return the version string for a tool if the convention '<tool> --version' succeeds."""
    try:
        result = subprocess.run(
            [command, "--version"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        return None

    output = (result.stdout or result.stderr or "").strip()
    return output or None


def x_get_tool_version__mutmut_1(command: str) -> str | None:
    """Return the version string for a tool if the convention '<tool> --version' succeeds."""
    try:
        result = None
    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        return None

    output = (result.stdout or result.stderr or "").strip()
    return output or None


def x_get_tool_version__mutmut_2(command: str) -> str | None:
    """Return the version string for a tool if the convention '<tool> --version' succeeds."""
    try:
        result = subprocess.run(
            None,
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        return None

    output = (result.stdout or result.stderr or "").strip()
    return output or None


def x_get_tool_version__mutmut_3(command: str) -> str | None:
    """Return the version string for a tool if the convention '<tool> --version' succeeds."""
    try:
        result = subprocess.run(
            [command, "--version"],
            check=None,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        return None

    output = (result.stdout or result.stderr or "").strip()
    return output or None


def x_get_tool_version__mutmut_4(command: str) -> str | None:
    """Return the version string for a tool if the convention '<tool> --version' succeeds."""
    try:
        result = subprocess.run(
            [command, "--version"],
            check=True,
            capture_output=None,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        return None

    output = (result.stdout or result.stderr or "").strip()
    return output or None


def x_get_tool_version__mutmut_5(command: str) -> str | None:
    """Return the version string for a tool if the convention '<tool> --version' succeeds."""
    try:
        result = subprocess.run(
            [command, "--version"],
            check=True,
            capture_output=True,
            text=None,
            encoding="utf-8",
            errors="replace",
        )
    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        return None

    output = (result.stdout or result.stderr or "").strip()
    return output or None


def x_get_tool_version__mutmut_6(command: str) -> str | None:
    """Return the version string for a tool if the convention '<tool> --version' succeeds."""
    try:
        result = subprocess.run(
            [command, "--version"],
            check=True,
            capture_output=True,
            text=True,
            encoding=None,
            errors="replace",
        )
    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        return None

    output = (result.stdout or result.stderr or "").strip()
    return output or None


def x_get_tool_version__mutmut_7(command: str) -> str | None:
    """Return the version string for a tool if the convention '<tool> --version' succeeds."""
    try:
        result = subprocess.run(
            [command, "--version"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors=None,
        )
    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        return None

    output = (result.stdout or result.stderr or "").strip()
    return output or None


def x_get_tool_version__mutmut_8(command: str) -> str | None:
    """Return the version string for a tool if the convention '<tool> --version' succeeds."""
    try:
        result = subprocess.run(
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        return None

    output = (result.stdout or result.stderr or "").strip()
    return output or None


def x_get_tool_version__mutmut_9(command: str) -> str | None:
    """Return the version string for a tool if the convention '<tool> --version' succeeds."""
    try:
        result = subprocess.run(
            [command, "--version"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        return None

    output = (result.stdout or result.stderr or "").strip()
    return output or None


def x_get_tool_version__mutmut_10(command: str) -> str | None:
    """Return the version string for a tool if the convention '<tool> --version' succeeds."""
    try:
        result = subprocess.run(
            [command, "--version"],
            check=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        return None

    output = (result.stdout or result.stderr or "").strip()
    return output or None


def x_get_tool_version__mutmut_11(command: str) -> str | None:
    """Return the version string for a tool if the convention '<tool> --version' succeeds."""
    try:
        result = subprocess.run(
            [command, "--version"],
            check=True,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
        )
    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        return None

    output = (result.stdout or result.stderr or "").strip()
    return output or None


def x_get_tool_version__mutmut_12(command: str) -> str | None:
    """Return the version string for a tool if the convention '<tool> --version' succeeds."""
    try:
        result = subprocess.run(
            [command, "--version"],
            check=True,
            capture_output=True,
            text=True,
            errors="replace",
        )
    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        return None

    output = (result.stdout or result.stderr or "").strip()
    return output or None


def x_get_tool_version__mutmut_13(command: str) -> str | None:
    """Return the version string for a tool if the convention '<tool> --version' succeeds."""
    try:
        result = subprocess.run(
            [command, "--version"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            )
    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        return None

    output = (result.stdout or result.stderr or "").strip()
    return output or None


def x_get_tool_version__mutmut_14(command: str) -> str | None:
    """Return the version string for a tool if the convention '<tool> --version' succeeds."""
    try:
        result = subprocess.run(
            [command, "XX--versionXX"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        return None

    output = (result.stdout or result.stderr or "").strip()
    return output or None


def x_get_tool_version__mutmut_15(command: str) -> str | None:
    """Return the version string for a tool if the convention '<tool> --version' succeeds."""
    try:
        result = subprocess.run(
            [command, "--VERSION"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        return None

    output = (result.stdout or result.stderr or "").strip()
    return output or None


def x_get_tool_version__mutmut_16(command: str) -> str | None:
    """Return the version string for a tool if the convention '<tool> --version' succeeds."""
    try:
        result = subprocess.run(
            [command, "--version"],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        return None

    output = (result.stdout or result.stderr or "").strip()
    return output or None


def x_get_tool_version__mutmut_17(command: str) -> str | None:
    """Return the version string for a tool if the convention '<tool> --version' succeeds."""
    try:
        result = subprocess.run(
            [command, "--version"],
            check=True,
            capture_output=False,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        return None

    output = (result.stdout or result.stderr or "").strip()
    return output or None


def x_get_tool_version__mutmut_18(command: str) -> str | None:
    """Return the version string for a tool if the convention '<tool> --version' succeeds."""
    try:
        result = subprocess.run(
            [command, "--version"],
            check=True,
            capture_output=True,
            text=False,
            encoding="utf-8",
            errors="replace",
        )
    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        return None

    output = (result.stdout or result.stderr or "").strip()
    return output or None


def x_get_tool_version__mutmut_19(command: str) -> str | None:
    """Return the version string for a tool if the convention '<tool> --version' succeeds."""
    try:
        result = subprocess.run(
            [command, "--version"],
            check=True,
            capture_output=True,
            text=True,
            encoding="XXutf-8XX",
            errors="replace",
        )
    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        return None

    output = (result.stdout or result.stderr or "").strip()
    return output or None


def x_get_tool_version__mutmut_20(command: str) -> str | None:
    """Return the version string for a tool if the convention '<tool> --version' succeeds."""
    try:
        result = subprocess.run(
            [command, "--version"],
            check=True,
            capture_output=True,
            text=True,
            encoding="UTF-8",
            errors="replace",
        )
    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        return None

    output = (result.stdout or result.stderr or "").strip()
    return output or None


def x_get_tool_version__mutmut_21(command: str) -> str | None:
    """Return the version string for a tool if the convention '<tool> --version' succeeds."""
    try:
        result = subprocess.run(
            [command, "--version"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="XXreplaceXX",
        )
    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        return None

    output = (result.stdout or result.stderr or "").strip()
    return output or None


def x_get_tool_version__mutmut_22(command: str) -> str | None:
    """Return the version string for a tool if the convention '<tool> --version' succeeds."""
    try:
        result = subprocess.run(
            [command, "--version"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="REPLACE",
        )
    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        return None

    output = (result.stdout or result.stderr or "").strip()
    return output or None


def x_get_tool_version__mutmut_23(command: str) -> str | None:
    """Return the version string for a tool if the convention '<tool> --version' succeeds."""
    try:
        result = subprocess.run(
            [command, "--version"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        return None

    output = None
    return output or None


def x_get_tool_version__mutmut_24(command: str) -> str | None:
    """Return the version string for a tool if the convention '<tool> --version' succeeds."""
    try:
        result = subprocess.run(
            [command, "--version"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        return None

    output = (result.stdout or result.stderr and "").strip()
    return output or None


def x_get_tool_version__mutmut_25(command: str) -> str | None:
    """Return the version string for a tool if the convention '<tool> --version' succeeds."""
    try:
        result = subprocess.run(
            [command, "--version"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        return None

    output = (result.stdout and result.stderr or "").strip()
    return output or None


def x_get_tool_version__mutmut_26(command: str) -> str | None:
    """Return the version string for a tool if the convention '<tool> --version' succeeds."""
    try:
        result = subprocess.run(
            [command, "--version"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        return None

    output = (result.stdout or result.stderr or "XXXX").strip()
    return output or None


def x_get_tool_version__mutmut_27(command: str) -> str | None:
    """Return the version string for a tool if the convention '<tool> --version' succeeds."""
    try:
        result = subprocess.run(
            [command, "--version"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        return None

    output = (result.stdout or result.stderr or "").strip()
    return output and None

x_get_tool_version__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_get_tool_version__mutmut_1': x_get_tool_version__mutmut_1, 
    'x_get_tool_version__mutmut_2': x_get_tool_version__mutmut_2, 
    'x_get_tool_version__mutmut_3': x_get_tool_version__mutmut_3, 
    'x_get_tool_version__mutmut_4': x_get_tool_version__mutmut_4, 
    'x_get_tool_version__mutmut_5': x_get_tool_version__mutmut_5, 
    'x_get_tool_version__mutmut_6': x_get_tool_version__mutmut_6, 
    'x_get_tool_version__mutmut_7': x_get_tool_version__mutmut_7, 
    'x_get_tool_version__mutmut_8': x_get_tool_version__mutmut_8, 
    'x_get_tool_version__mutmut_9': x_get_tool_version__mutmut_9, 
    'x_get_tool_version__mutmut_10': x_get_tool_version__mutmut_10, 
    'x_get_tool_version__mutmut_11': x_get_tool_version__mutmut_11, 
    'x_get_tool_version__mutmut_12': x_get_tool_version__mutmut_12, 
    'x_get_tool_version__mutmut_13': x_get_tool_version__mutmut_13, 
    'x_get_tool_version__mutmut_14': x_get_tool_version__mutmut_14, 
    'x_get_tool_version__mutmut_15': x_get_tool_version__mutmut_15, 
    'x_get_tool_version__mutmut_16': x_get_tool_version__mutmut_16, 
    'x_get_tool_version__mutmut_17': x_get_tool_version__mutmut_17, 
    'x_get_tool_version__mutmut_18': x_get_tool_version__mutmut_18, 
    'x_get_tool_version__mutmut_19': x_get_tool_version__mutmut_19, 
    'x_get_tool_version__mutmut_20': x_get_tool_version__mutmut_20, 
    'x_get_tool_version__mutmut_21': x_get_tool_version__mutmut_21, 
    'x_get_tool_version__mutmut_22': x_get_tool_version__mutmut_22, 
    'x_get_tool_version__mutmut_23': x_get_tool_version__mutmut_23, 
    'x_get_tool_version__mutmut_24': x_get_tool_version__mutmut_24, 
    'x_get_tool_version__mutmut_25': x_get_tool_version__mutmut_25, 
    'x_get_tool_version__mutmut_26': x_get_tool_version__mutmut_26, 
    'x_get_tool_version__mutmut_27': x_get_tool_version__mutmut_27
}
x_get_tool_version__mutmut_orig.__name__ = 'x_get_tool_version'


def check_all_tools(
    requirements: Mapping[str, Tuple[str, str]] | None = None,
) -> Dict[str, Tuple[bool, str]]:
    args = [requirements]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_check_all_tools__mutmut_orig, x_check_all_tools__mutmut_mutants, args, kwargs, None)


def x_check_all_tools__mutmut_orig(
    requirements: Mapping[str, Tuple[str, str]] | None = None,
) -> Dict[str, Tuple[bool, str]]:
    """Check tool availability for all known agents, returning {agent: (ok, detail)}."""
    results: Dict[str, Tuple[bool, str]] = {}
    entries = requirements or AGENT_TOOL_REQUIREMENTS
    for agent, (tool, url) in entries.items():
        ok = check_tool(tool, url)
        detail = get_tool_version(tool) if ok else url
        results[agent] = (ok, detail or url)
    return results


def x_check_all_tools__mutmut_1(
    requirements: Mapping[str, Tuple[str, str]] | None = None,
) -> Dict[str, Tuple[bool, str]]:
    """Check tool availability for all known agents, returning {agent: (ok, detail)}."""
    results: Dict[str, Tuple[bool, str]] = None
    entries = requirements or AGENT_TOOL_REQUIREMENTS
    for agent, (tool, url) in entries.items():
        ok = check_tool(tool, url)
        detail = get_tool_version(tool) if ok else url
        results[agent] = (ok, detail or url)
    return results


def x_check_all_tools__mutmut_2(
    requirements: Mapping[str, Tuple[str, str]] | None = None,
) -> Dict[str, Tuple[bool, str]]:
    """Check tool availability for all known agents, returning {agent: (ok, detail)}."""
    results: Dict[str, Tuple[bool, str]] = {}
    entries = None
    for agent, (tool, url) in entries.items():
        ok = check_tool(tool, url)
        detail = get_tool_version(tool) if ok else url
        results[agent] = (ok, detail or url)
    return results


def x_check_all_tools__mutmut_3(
    requirements: Mapping[str, Tuple[str, str]] | None = None,
) -> Dict[str, Tuple[bool, str]]:
    """Check tool availability for all known agents, returning {agent: (ok, detail)}."""
    results: Dict[str, Tuple[bool, str]] = {}
    entries = requirements and AGENT_TOOL_REQUIREMENTS
    for agent, (tool, url) in entries.items():
        ok = check_tool(tool, url)
        detail = get_tool_version(tool) if ok else url
        results[agent] = (ok, detail or url)
    return results


def x_check_all_tools__mutmut_4(
    requirements: Mapping[str, Tuple[str, str]] | None = None,
) -> Dict[str, Tuple[bool, str]]:
    """Check tool availability for all known agents, returning {agent: (ok, detail)}."""
    results: Dict[str, Tuple[bool, str]] = {}
    entries = requirements or AGENT_TOOL_REQUIREMENTS
    for agent, (tool, url) in entries.items():
        ok = None
        detail = get_tool_version(tool) if ok else url
        results[agent] = (ok, detail or url)
    return results


def x_check_all_tools__mutmut_5(
    requirements: Mapping[str, Tuple[str, str]] | None = None,
) -> Dict[str, Tuple[bool, str]]:
    """Check tool availability for all known agents, returning {agent: (ok, detail)}."""
    results: Dict[str, Tuple[bool, str]] = {}
    entries = requirements or AGENT_TOOL_REQUIREMENTS
    for agent, (tool, url) in entries.items():
        ok = check_tool(None, url)
        detail = get_tool_version(tool) if ok else url
        results[agent] = (ok, detail or url)
    return results


def x_check_all_tools__mutmut_6(
    requirements: Mapping[str, Tuple[str, str]] | None = None,
) -> Dict[str, Tuple[bool, str]]:
    """Check tool availability for all known agents, returning {agent: (ok, detail)}."""
    results: Dict[str, Tuple[bool, str]] = {}
    entries = requirements or AGENT_TOOL_REQUIREMENTS
    for agent, (tool, url) in entries.items():
        ok = check_tool(tool, None)
        detail = get_tool_version(tool) if ok else url
        results[agent] = (ok, detail or url)
    return results


def x_check_all_tools__mutmut_7(
    requirements: Mapping[str, Tuple[str, str]] | None = None,
) -> Dict[str, Tuple[bool, str]]:
    """Check tool availability for all known agents, returning {agent: (ok, detail)}."""
    results: Dict[str, Tuple[bool, str]] = {}
    entries = requirements or AGENT_TOOL_REQUIREMENTS
    for agent, (tool, url) in entries.items():
        ok = check_tool(url)
        detail = get_tool_version(tool) if ok else url
        results[agent] = (ok, detail or url)
    return results


def x_check_all_tools__mutmut_8(
    requirements: Mapping[str, Tuple[str, str]] | None = None,
) -> Dict[str, Tuple[bool, str]]:
    """Check tool availability for all known agents, returning {agent: (ok, detail)}."""
    results: Dict[str, Tuple[bool, str]] = {}
    entries = requirements or AGENT_TOOL_REQUIREMENTS
    for agent, (tool, url) in entries.items():
        ok = check_tool(tool, )
        detail = get_tool_version(tool) if ok else url
        results[agent] = (ok, detail or url)
    return results


def x_check_all_tools__mutmut_9(
    requirements: Mapping[str, Tuple[str, str]] | None = None,
) -> Dict[str, Tuple[bool, str]]:
    """Check tool availability for all known agents, returning {agent: (ok, detail)}."""
    results: Dict[str, Tuple[bool, str]] = {}
    entries = requirements or AGENT_TOOL_REQUIREMENTS
    for agent, (tool, url) in entries.items():
        ok = check_tool(tool, url)
        detail = None
        results[agent] = (ok, detail or url)
    return results


def x_check_all_tools__mutmut_10(
    requirements: Mapping[str, Tuple[str, str]] | None = None,
) -> Dict[str, Tuple[bool, str]]:
    """Check tool availability for all known agents, returning {agent: (ok, detail)}."""
    results: Dict[str, Tuple[bool, str]] = {}
    entries = requirements or AGENT_TOOL_REQUIREMENTS
    for agent, (tool, url) in entries.items():
        ok = check_tool(tool, url)
        detail = get_tool_version(None) if ok else url
        results[agent] = (ok, detail or url)
    return results


def x_check_all_tools__mutmut_11(
    requirements: Mapping[str, Tuple[str, str]] | None = None,
) -> Dict[str, Tuple[bool, str]]:
    """Check tool availability for all known agents, returning {agent: (ok, detail)}."""
    results: Dict[str, Tuple[bool, str]] = {}
    entries = requirements or AGENT_TOOL_REQUIREMENTS
    for agent, (tool, url) in entries.items():
        ok = check_tool(tool, url)
        detail = get_tool_version(tool) if ok else url
        results[agent] = None
    return results


def x_check_all_tools__mutmut_12(
    requirements: Mapping[str, Tuple[str, str]] | None = None,
) -> Dict[str, Tuple[bool, str]]:
    """Check tool availability for all known agents, returning {agent: (ok, detail)}."""
    results: Dict[str, Tuple[bool, str]] = {}
    entries = requirements or AGENT_TOOL_REQUIREMENTS
    for agent, (tool, url) in entries.items():
        ok = check_tool(tool, url)
        detail = get_tool_version(tool) if ok else url
        results[agent] = (ok, detail and url)
    return results

x_check_all_tools__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_check_all_tools__mutmut_1': x_check_all_tools__mutmut_1, 
    'x_check_all_tools__mutmut_2': x_check_all_tools__mutmut_2, 
    'x_check_all_tools__mutmut_3': x_check_all_tools__mutmut_3, 
    'x_check_all_tools__mutmut_4': x_check_all_tools__mutmut_4, 
    'x_check_all_tools__mutmut_5': x_check_all_tools__mutmut_5, 
    'x_check_all_tools__mutmut_6': x_check_all_tools__mutmut_6, 
    'x_check_all_tools__mutmut_7': x_check_all_tools__mutmut_7, 
    'x_check_all_tools__mutmut_8': x_check_all_tools__mutmut_8, 
    'x_check_all_tools__mutmut_9': x_check_all_tools__mutmut_9, 
    'x_check_all_tools__mutmut_10': x_check_all_tools__mutmut_10, 
    'x_check_all_tools__mutmut_11': x_check_all_tools__mutmut_11, 
    'x_check_all_tools__mutmut_12': x_check_all_tools__mutmut_12
}
x_check_all_tools__mutmut_orig.__name__ = 'x_check_all_tools'


__all__ = [
    "check_all_tools",
    "check_tool",
    "check_tool_for_tracker",
    "get_tool_version",
]
