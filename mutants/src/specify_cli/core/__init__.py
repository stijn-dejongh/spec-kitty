"""Core utilities and configuration exports."""

from .config import (
    AGENT_COMMAND_CONFIG,
    AGENT_TOOL_REQUIREMENTS,
    AI_CHOICES,
    BANNER,
    DEFAULT_MISSION_KEY,
    DEFAULT_TEMPLATE_REPO,
    MISSION_CHOICES,
    SCRIPT_TYPE_CHOICES,
)
from .utils import format_path, ensure_directory, safe_remove, get_platform
from .git_ops import run_command, is_git_repo, init_git_repo, get_current_branch, resolve_primary_branch
from .project_resolver import (
    locate_project_root,
    resolve_template_path,
    resolve_worktree_aware_feature_dir,
    get_active_mission_key,
)
from .tool_checker import (
    check_tool,
    check_tool_for_tracker,
    check_all_tools,
    get_tool_version,
)

__all__ = [
    "AGENT_COMMAND_CONFIG",
    "AGENT_TOOL_REQUIREMENTS",
    "AI_CHOICES",
    "BANNER",
    "DEFAULT_MISSION_KEY",
    "DEFAULT_TEMPLATE_REPO",
    "MISSION_CHOICES",
    "SCRIPT_TYPE_CHOICES",
    "format_path",
    "ensure_directory",
    "safe_remove",
    "get_platform",
    "run_command",
    "is_git_repo",
    "init_git_repo",
    "get_current_branch",
    "resolve_primary_branch",
    "locate_project_root",
    "resolve_template_path",
    "resolve_worktree_aware_feature_dir",
    "get_active_mission_key",
    "check_tool",
    "check_tool_for_tracker",
    "check_all_tools",
    "get_tool_version",
]
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
