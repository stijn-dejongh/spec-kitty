"""Context validation for location-aware commands.

This module provides runtime validation to ensure commands are executed
in the correct location (main repository vs worktree). Prevents common
mistakes like running 'implement' from inside a worktree.

Example:
    from specify_cli.core.context_validation import (
        require_main_repo,
        require_worktree,
        get_current_context,
    )

    @require_main_repo
    def implement(wp_id: str):
        # This function can only run from main repo
        pass

    @require_worktree
    def some_workspace_command():
        # This function can only run from inside a worktree
        pass
"""

from __future__ import annotations

import functools
import os
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Callable, TypeVar

import typer
from rich.console import Console

console = Console()
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


class ExecutionContext(str, Enum):
    """Execution context for a command."""

    MAIN_REPO = "main"  # Command runs in main repository
    WORKTREE = "worktree"  # Command runs inside a worktree
    EITHER = "either"  # Command can run in either location


@dataclass
class CurrentContext:
    """Current execution context information."""

    location: ExecutionContext
    cwd: Path
    repo_root: Path | None
    worktree_name: str | None  # e.g., "010-feature-WP02" if in worktree
    worktree_path: Path | None  # Absolute path to worktree directory


def detect_execution_context(cwd: Path | None = None) -> CurrentContext:
    args = [cwd]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_detect_execution_context__mutmut_orig, x_detect_execution_context__mutmut_mutants, args, kwargs, None)


def x_detect_execution_context__mutmut_orig(cwd: Path | None = None) -> CurrentContext:
    """Detect current execution context.

    Args:
        cwd: Current working directory (defaults to Path.cwd())

    Returns:
        CurrentContext with location, paths, and worktree info

    Example:
        >>> ctx = detect_execution_context()
        >>> if ctx.location == ExecutionContext.WORKTREE:
        ...     print(f"In worktree: {ctx.worktree_name}")
    """
    if cwd is None:
        cwd = Path.cwd().resolve()
    else:
        cwd = cwd.resolve()

    # Check if .worktrees is in path
    if ".worktrees" in cwd.parts:
        # Extract worktree information
        for i, part in enumerate(cwd.parts):
            if part == ".worktrees" and i + 1 < len(cwd.parts):
                candidate_root = Path(*cwd.parts[:i])
                if (candidate_root / ".kittify").exists() or (candidate_root / ".git").exists():
                    worktree_name = cwd.parts[i + 1]
                    worktree_path = Path(*cwd.parts[: i + 2])
                    repo_root = candidate_root

                    return CurrentContext(
                        location=ExecutionContext.WORKTREE,
                        cwd=cwd,
                        repo_root=repo_root,
                        worktree_name=worktree_name,
                        worktree_path=worktree_path,
                    )

    # Not in worktree - assume main repo
    # Try to find repo root (directory containing .kittify or .git)
    repo_root = None
    search_path = cwd
    for _ in range(10):  # Limit depth
        if (search_path / ".kittify").exists() or (search_path / ".git").exists():
            repo_root = search_path
            break
        if search_path.parent == search_path:
            break  # Reached filesystem root
        search_path = search_path.parent

    return CurrentContext(
        location=ExecutionContext.MAIN_REPO,
        cwd=cwd,
        repo_root=repo_root,
        worktree_name=None,
        worktree_path=None,
    )


def x_detect_execution_context__mutmut_1(cwd: Path | None = None) -> CurrentContext:
    """Detect current execution context.

    Args:
        cwd: Current working directory (defaults to Path.cwd())

    Returns:
        CurrentContext with location, paths, and worktree info

    Example:
        >>> ctx = detect_execution_context()
        >>> if ctx.location == ExecutionContext.WORKTREE:
        ...     print(f"In worktree: {ctx.worktree_name}")
    """
    if cwd is not None:
        cwd = Path.cwd().resolve()
    else:
        cwd = cwd.resolve()

    # Check if .worktrees is in path
    if ".worktrees" in cwd.parts:
        # Extract worktree information
        for i, part in enumerate(cwd.parts):
            if part == ".worktrees" and i + 1 < len(cwd.parts):
                candidate_root = Path(*cwd.parts[:i])
                if (candidate_root / ".kittify").exists() or (candidate_root / ".git").exists():
                    worktree_name = cwd.parts[i + 1]
                    worktree_path = Path(*cwd.parts[: i + 2])
                    repo_root = candidate_root

                    return CurrentContext(
                        location=ExecutionContext.WORKTREE,
                        cwd=cwd,
                        repo_root=repo_root,
                        worktree_name=worktree_name,
                        worktree_path=worktree_path,
                    )

    # Not in worktree - assume main repo
    # Try to find repo root (directory containing .kittify or .git)
    repo_root = None
    search_path = cwd
    for _ in range(10):  # Limit depth
        if (search_path / ".kittify").exists() or (search_path / ".git").exists():
            repo_root = search_path
            break
        if search_path.parent == search_path:
            break  # Reached filesystem root
        search_path = search_path.parent

    return CurrentContext(
        location=ExecutionContext.MAIN_REPO,
        cwd=cwd,
        repo_root=repo_root,
        worktree_name=None,
        worktree_path=None,
    )


def x_detect_execution_context__mutmut_2(cwd: Path | None = None) -> CurrentContext:
    """Detect current execution context.

    Args:
        cwd: Current working directory (defaults to Path.cwd())

    Returns:
        CurrentContext with location, paths, and worktree info

    Example:
        >>> ctx = detect_execution_context()
        >>> if ctx.location == ExecutionContext.WORKTREE:
        ...     print(f"In worktree: {ctx.worktree_name}")
    """
    if cwd is None:
        cwd = None
    else:
        cwd = cwd.resolve()

    # Check if .worktrees is in path
    if ".worktrees" in cwd.parts:
        # Extract worktree information
        for i, part in enumerate(cwd.parts):
            if part == ".worktrees" and i + 1 < len(cwd.parts):
                candidate_root = Path(*cwd.parts[:i])
                if (candidate_root / ".kittify").exists() or (candidate_root / ".git").exists():
                    worktree_name = cwd.parts[i + 1]
                    worktree_path = Path(*cwd.parts[: i + 2])
                    repo_root = candidate_root

                    return CurrentContext(
                        location=ExecutionContext.WORKTREE,
                        cwd=cwd,
                        repo_root=repo_root,
                        worktree_name=worktree_name,
                        worktree_path=worktree_path,
                    )

    # Not in worktree - assume main repo
    # Try to find repo root (directory containing .kittify or .git)
    repo_root = None
    search_path = cwd
    for _ in range(10):  # Limit depth
        if (search_path / ".kittify").exists() or (search_path / ".git").exists():
            repo_root = search_path
            break
        if search_path.parent == search_path:
            break  # Reached filesystem root
        search_path = search_path.parent

    return CurrentContext(
        location=ExecutionContext.MAIN_REPO,
        cwd=cwd,
        repo_root=repo_root,
        worktree_name=None,
        worktree_path=None,
    )


def x_detect_execution_context__mutmut_3(cwd: Path | None = None) -> CurrentContext:
    """Detect current execution context.

    Args:
        cwd: Current working directory (defaults to Path.cwd())

    Returns:
        CurrentContext with location, paths, and worktree info

    Example:
        >>> ctx = detect_execution_context()
        >>> if ctx.location == ExecutionContext.WORKTREE:
        ...     print(f"In worktree: {ctx.worktree_name}")
    """
    if cwd is None:
        cwd = Path.cwd().resolve()
    else:
        cwd = None

    # Check if .worktrees is in path
    if ".worktrees" in cwd.parts:
        # Extract worktree information
        for i, part in enumerate(cwd.parts):
            if part == ".worktrees" and i + 1 < len(cwd.parts):
                candidate_root = Path(*cwd.parts[:i])
                if (candidate_root / ".kittify").exists() or (candidate_root / ".git").exists():
                    worktree_name = cwd.parts[i + 1]
                    worktree_path = Path(*cwd.parts[: i + 2])
                    repo_root = candidate_root

                    return CurrentContext(
                        location=ExecutionContext.WORKTREE,
                        cwd=cwd,
                        repo_root=repo_root,
                        worktree_name=worktree_name,
                        worktree_path=worktree_path,
                    )

    # Not in worktree - assume main repo
    # Try to find repo root (directory containing .kittify or .git)
    repo_root = None
    search_path = cwd
    for _ in range(10):  # Limit depth
        if (search_path / ".kittify").exists() or (search_path / ".git").exists():
            repo_root = search_path
            break
        if search_path.parent == search_path:
            break  # Reached filesystem root
        search_path = search_path.parent

    return CurrentContext(
        location=ExecutionContext.MAIN_REPO,
        cwd=cwd,
        repo_root=repo_root,
        worktree_name=None,
        worktree_path=None,
    )


def x_detect_execution_context__mutmut_4(cwd: Path | None = None) -> CurrentContext:
    """Detect current execution context.

    Args:
        cwd: Current working directory (defaults to Path.cwd())

    Returns:
        CurrentContext with location, paths, and worktree info

    Example:
        >>> ctx = detect_execution_context()
        >>> if ctx.location == ExecutionContext.WORKTREE:
        ...     print(f"In worktree: {ctx.worktree_name}")
    """
    if cwd is None:
        cwd = Path.cwd().resolve()
    else:
        cwd = cwd.resolve()

    # Check if .worktrees is in path
    if "XX.worktreesXX" in cwd.parts:
        # Extract worktree information
        for i, part in enumerate(cwd.parts):
            if part == ".worktrees" and i + 1 < len(cwd.parts):
                candidate_root = Path(*cwd.parts[:i])
                if (candidate_root / ".kittify").exists() or (candidate_root / ".git").exists():
                    worktree_name = cwd.parts[i + 1]
                    worktree_path = Path(*cwd.parts[: i + 2])
                    repo_root = candidate_root

                    return CurrentContext(
                        location=ExecutionContext.WORKTREE,
                        cwd=cwd,
                        repo_root=repo_root,
                        worktree_name=worktree_name,
                        worktree_path=worktree_path,
                    )

    # Not in worktree - assume main repo
    # Try to find repo root (directory containing .kittify or .git)
    repo_root = None
    search_path = cwd
    for _ in range(10):  # Limit depth
        if (search_path / ".kittify").exists() or (search_path / ".git").exists():
            repo_root = search_path
            break
        if search_path.parent == search_path:
            break  # Reached filesystem root
        search_path = search_path.parent

    return CurrentContext(
        location=ExecutionContext.MAIN_REPO,
        cwd=cwd,
        repo_root=repo_root,
        worktree_name=None,
        worktree_path=None,
    )


def x_detect_execution_context__mutmut_5(cwd: Path | None = None) -> CurrentContext:
    """Detect current execution context.

    Args:
        cwd: Current working directory (defaults to Path.cwd())

    Returns:
        CurrentContext with location, paths, and worktree info

    Example:
        >>> ctx = detect_execution_context()
        >>> if ctx.location == ExecutionContext.WORKTREE:
        ...     print(f"In worktree: {ctx.worktree_name}")
    """
    if cwd is None:
        cwd = Path.cwd().resolve()
    else:
        cwd = cwd.resolve()

    # Check if .worktrees is in path
    if ".WORKTREES" in cwd.parts:
        # Extract worktree information
        for i, part in enumerate(cwd.parts):
            if part == ".worktrees" and i + 1 < len(cwd.parts):
                candidate_root = Path(*cwd.parts[:i])
                if (candidate_root / ".kittify").exists() or (candidate_root / ".git").exists():
                    worktree_name = cwd.parts[i + 1]
                    worktree_path = Path(*cwd.parts[: i + 2])
                    repo_root = candidate_root

                    return CurrentContext(
                        location=ExecutionContext.WORKTREE,
                        cwd=cwd,
                        repo_root=repo_root,
                        worktree_name=worktree_name,
                        worktree_path=worktree_path,
                    )

    # Not in worktree - assume main repo
    # Try to find repo root (directory containing .kittify or .git)
    repo_root = None
    search_path = cwd
    for _ in range(10):  # Limit depth
        if (search_path / ".kittify").exists() or (search_path / ".git").exists():
            repo_root = search_path
            break
        if search_path.parent == search_path:
            break  # Reached filesystem root
        search_path = search_path.parent

    return CurrentContext(
        location=ExecutionContext.MAIN_REPO,
        cwd=cwd,
        repo_root=repo_root,
        worktree_name=None,
        worktree_path=None,
    )


def x_detect_execution_context__mutmut_6(cwd: Path | None = None) -> CurrentContext:
    """Detect current execution context.

    Args:
        cwd: Current working directory (defaults to Path.cwd())

    Returns:
        CurrentContext with location, paths, and worktree info

    Example:
        >>> ctx = detect_execution_context()
        >>> if ctx.location == ExecutionContext.WORKTREE:
        ...     print(f"In worktree: {ctx.worktree_name}")
    """
    if cwd is None:
        cwd = Path.cwd().resolve()
    else:
        cwd = cwd.resolve()

    # Check if .worktrees is in path
    if ".worktrees" not in cwd.parts:
        # Extract worktree information
        for i, part in enumerate(cwd.parts):
            if part == ".worktrees" and i + 1 < len(cwd.parts):
                candidate_root = Path(*cwd.parts[:i])
                if (candidate_root / ".kittify").exists() or (candidate_root / ".git").exists():
                    worktree_name = cwd.parts[i + 1]
                    worktree_path = Path(*cwd.parts[: i + 2])
                    repo_root = candidate_root

                    return CurrentContext(
                        location=ExecutionContext.WORKTREE,
                        cwd=cwd,
                        repo_root=repo_root,
                        worktree_name=worktree_name,
                        worktree_path=worktree_path,
                    )

    # Not in worktree - assume main repo
    # Try to find repo root (directory containing .kittify or .git)
    repo_root = None
    search_path = cwd
    for _ in range(10):  # Limit depth
        if (search_path / ".kittify").exists() or (search_path / ".git").exists():
            repo_root = search_path
            break
        if search_path.parent == search_path:
            break  # Reached filesystem root
        search_path = search_path.parent

    return CurrentContext(
        location=ExecutionContext.MAIN_REPO,
        cwd=cwd,
        repo_root=repo_root,
        worktree_name=None,
        worktree_path=None,
    )


def x_detect_execution_context__mutmut_7(cwd: Path | None = None) -> CurrentContext:
    """Detect current execution context.

    Args:
        cwd: Current working directory (defaults to Path.cwd())

    Returns:
        CurrentContext with location, paths, and worktree info

    Example:
        >>> ctx = detect_execution_context()
        >>> if ctx.location == ExecutionContext.WORKTREE:
        ...     print(f"In worktree: {ctx.worktree_name}")
    """
    if cwd is None:
        cwd = Path.cwd().resolve()
    else:
        cwd = cwd.resolve()

    # Check if .worktrees is in path
    if ".worktrees" in cwd.parts:
        # Extract worktree information
        for i, part in enumerate(None):
            if part == ".worktrees" and i + 1 < len(cwd.parts):
                candidate_root = Path(*cwd.parts[:i])
                if (candidate_root / ".kittify").exists() or (candidate_root / ".git").exists():
                    worktree_name = cwd.parts[i + 1]
                    worktree_path = Path(*cwd.parts[: i + 2])
                    repo_root = candidate_root

                    return CurrentContext(
                        location=ExecutionContext.WORKTREE,
                        cwd=cwd,
                        repo_root=repo_root,
                        worktree_name=worktree_name,
                        worktree_path=worktree_path,
                    )

    # Not in worktree - assume main repo
    # Try to find repo root (directory containing .kittify or .git)
    repo_root = None
    search_path = cwd
    for _ in range(10):  # Limit depth
        if (search_path / ".kittify").exists() or (search_path / ".git").exists():
            repo_root = search_path
            break
        if search_path.parent == search_path:
            break  # Reached filesystem root
        search_path = search_path.parent

    return CurrentContext(
        location=ExecutionContext.MAIN_REPO,
        cwd=cwd,
        repo_root=repo_root,
        worktree_name=None,
        worktree_path=None,
    )


def x_detect_execution_context__mutmut_8(cwd: Path | None = None) -> CurrentContext:
    """Detect current execution context.

    Args:
        cwd: Current working directory (defaults to Path.cwd())

    Returns:
        CurrentContext with location, paths, and worktree info

    Example:
        >>> ctx = detect_execution_context()
        >>> if ctx.location == ExecutionContext.WORKTREE:
        ...     print(f"In worktree: {ctx.worktree_name}")
    """
    if cwd is None:
        cwd = Path.cwd().resolve()
    else:
        cwd = cwd.resolve()

    # Check if .worktrees is in path
    if ".worktrees" in cwd.parts:
        # Extract worktree information
        for i, part in enumerate(cwd.parts):
            if part == ".worktrees" or i + 1 < len(cwd.parts):
                candidate_root = Path(*cwd.parts[:i])
                if (candidate_root / ".kittify").exists() or (candidate_root / ".git").exists():
                    worktree_name = cwd.parts[i + 1]
                    worktree_path = Path(*cwd.parts[: i + 2])
                    repo_root = candidate_root

                    return CurrentContext(
                        location=ExecutionContext.WORKTREE,
                        cwd=cwd,
                        repo_root=repo_root,
                        worktree_name=worktree_name,
                        worktree_path=worktree_path,
                    )

    # Not in worktree - assume main repo
    # Try to find repo root (directory containing .kittify or .git)
    repo_root = None
    search_path = cwd
    for _ in range(10):  # Limit depth
        if (search_path / ".kittify").exists() or (search_path / ".git").exists():
            repo_root = search_path
            break
        if search_path.parent == search_path:
            break  # Reached filesystem root
        search_path = search_path.parent

    return CurrentContext(
        location=ExecutionContext.MAIN_REPO,
        cwd=cwd,
        repo_root=repo_root,
        worktree_name=None,
        worktree_path=None,
    )


def x_detect_execution_context__mutmut_9(cwd: Path | None = None) -> CurrentContext:
    """Detect current execution context.

    Args:
        cwd: Current working directory (defaults to Path.cwd())

    Returns:
        CurrentContext with location, paths, and worktree info

    Example:
        >>> ctx = detect_execution_context()
        >>> if ctx.location == ExecutionContext.WORKTREE:
        ...     print(f"In worktree: {ctx.worktree_name}")
    """
    if cwd is None:
        cwd = Path.cwd().resolve()
    else:
        cwd = cwd.resolve()

    # Check if .worktrees is in path
    if ".worktrees" in cwd.parts:
        # Extract worktree information
        for i, part in enumerate(cwd.parts):
            if part != ".worktrees" and i + 1 < len(cwd.parts):
                candidate_root = Path(*cwd.parts[:i])
                if (candidate_root / ".kittify").exists() or (candidate_root / ".git").exists():
                    worktree_name = cwd.parts[i + 1]
                    worktree_path = Path(*cwd.parts[: i + 2])
                    repo_root = candidate_root

                    return CurrentContext(
                        location=ExecutionContext.WORKTREE,
                        cwd=cwd,
                        repo_root=repo_root,
                        worktree_name=worktree_name,
                        worktree_path=worktree_path,
                    )

    # Not in worktree - assume main repo
    # Try to find repo root (directory containing .kittify or .git)
    repo_root = None
    search_path = cwd
    for _ in range(10):  # Limit depth
        if (search_path / ".kittify").exists() or (search_path / ".git").exists():
            repo_root = search_path
            break
        if search_path.parent == search_path:
            break  # Reached filesystem root
        search_path = search_path.parent

    return CurrentContext(
        location=ExecutionContext.MAIN_REPO,
        cwd=cwd,
        repo_root=repo_root,
        worktree_name=None,
        worktree_path=None,
    )


def x_detect_execution_context__mutmut_10(cwd: Path | None = None) -> CurrentContext:
    """Detect current execution context.

    Args:
        cwd: Current working directory (defaults to Path.cwd())

    Returns:
        CurrentContext with location, paths, and worktree info

    Example:
        >>> ctx = detect_execution_context()
        >>> if ctx.location == ExecutionContext.WORKTREE:
        ...     print(f"In worktree: {ctx.worktree_name}")
    """
    if cwd is None:
        cwd = Path.cwd().resolve()
    else:
        cwd = cwd.resolve()

    # Check if .worktrees is in path
    if ".worktrees" in cwd.parts:
        # Extract worktree information
        for i, part in enumerate(cwd.parts):
            if part == "XX.worktreesXX" and i + 1 < len(cwd.parts):
                candidate_root = Path(*cwd.parts[:i])
                if (candidate_root / ".kittify").exists() or (candidate_root / ".git").exists():
                    worktree_name = cwd.parts[i + 1]
                    worktree_path = Path(*cwd.parts[: i + 2])
                    repo_root = candidate_root

                    return CurrentContext(
                        location=ExecutionContext.WORKTREE,
                        cwd=cwd,
                        repo_root=repo_root,
                        worktree_name=worktree_name,
                        worktree_path=worktree_path,
                    )

    # Not in worktree - assume main repo
    # Try to find repo root (directory containing .kittify or .git)
    repo_root = None
    search_path = cwd
    for _ in range(10):  # Limit depth
        if (search_path / ".kittify").exists() or (search_path / ".git").exists():
            repo_root = search_path
            break
        if search_path.parent == search_path:
            break  # Reached filesystem root
        search_path = search_path.parent

    return CurrentContext(
        location=ExecutionContext.MAIN_REPO,
        cwd=cwd,
        repo_root=repo_root,
        worktree_name=None,
        worktree_path=None,
    )


def x_detect_execution_context__mutmut_11(cwd: Path | None = None) -> CurrentContext:
    """Detect current execution context.

    Args:
        cwd: Current working directory (defaults to Path.cwd())

    Returns:
        CurrentContext with location, paths, and worktree info

    Example:
        >>> ctx = detect_execution_context()
        >>> if ctx.location == ExecutionContext.WORKTREE:
        ...     print(f"In worktree: {ctx.worktree_name}")
    """
    if cwd is None:
        cwd = Path.cwd().resolve()
    else:
        cwd = cwd.resolve()

    # Check if .worktrees is in path
    if ".worktrees" in cwd.parts:
        # Extract worktree information
        for i, part in enumerate(cwd.parts):
            if part == ".WORKTREES" and i + 1 < len(cwd.parts):
                candidate_root = Path(*cwd.parts[:i])
                if (candidate_root / ".kittify").exists() or (candidate_root / ".git").exists():
                    worktree_name = cwd.parts[i + 1]
                    worktree_path = Path(*cwd.parts[: i + 2])
                    repo_root = candidate_root

                    return CurrentContext(
                        location=ExecutionContext.WORKTREE,
                        cwd=cwd,
                        repo_root=repo_root,
                        worktree_name=worktree_name,
                        worktree_path=worktree_path,
                    )

    # Not in worktree - assume main repo
    # Try to find repo root (directory containing .kittify or .git)
    repo_root = None
    search_path = cwd
    for _ in range(10):  # Limit depth
        if (search_path / ".kittify").exists() or (search_path / ".git").exists():
            repo_root = search_path
            break
        if search_path.parent == search_path:
            break  # Reached filesystem root
        search_path = search_path.parent

    return CurrentContext(
        location=ExecutionContext.MAIN_REPO,
        cwd=cwd,
        repo_root=repo_root,
        worktree_name=None,
        worktree_path=None,
    )


def x_detect_execution_context__mutmut_12(cwd: Path | None = None) -> CurrentContext:
    """Detect current execution context.

    Args:
        cwd: Current working directory (defaults to Path.cwd())

    Returns:
        CurrentContext with location, paths, and worktree info

    Example:
        >>> ctx = detect_execution_context()
        >>> if ctx.location == ExecutionContext.WORKTREE:
        ...     print(f"In worktree: {ctx.worktree_name}")
    """
    if cwd is None:
        cwd = Path.cwd().resolve()
    else:
        cwd = cwd.resolve()

    # Check if .worktrees is in path
    if ".worktrees" in cwd.parts:
        # Extract worktree information
        for i, part in enumerate(cwd.parts):
            if part == ".worktrees" and i - 1 < len(cwd.parts):
                candidate_root = Path(*cwd.parts[:i])
                if (candidate_root / ".kittify").exists() or (candidate_root / ".git").exists():
                    worktree_name = cwd.parts[i + 1]
                    worktree_path = Path(*cwd.parts[: i + 2])
                    repo_root = candidate_root

                    return CurrentContext(
                        location=ExecutionContext.WORKTREE,
                        cwd=cwd,
                        repo_root=repo_root,
                        worktree_name=worktree_name,
                        worktree_path=worktree_path,
                    )

    # Not in worktree - assume main repo
    # Try to find repo root (directory containing .kittify or .git)
    repo_root = None
    search_path = cwd
    for _ in range(10):  # Limit depth
        if (search_path / ".kittify").exists() or (search_path / ".git").exists():
            repo_root = search_path
            break
        if search_path.parent == search_path:
            break  # Reached filesystem root
        search_path = search_path.parent

    return CurrentContext(
        location=ExecutionContext.MAIN_REPO,
        cwd=cwd,
        repo_root=repo_root,
        worktree_name=None,
        worktree_path=None,
    )


def x_detect_execution_context__mutmut_13(cwd: Path | None = None) -> CurrentContext:
    """Detect current execution context.

    Args:
        cwd: Current working directory (defaults to Path.cwd())

    Returns:
        CurrentContext with location, paths, and worktree info

    Example:
        >>> ctx = detect_execution_context()
        >>> if ctx.location == ExecutionContext.WORKTREE:
        ...     print(f"In worktree: {ctx.worktree_name}")
    """
    if cwd is None:
        cwd = Path.cwd().resolve()
    else:
        cwd = cwd.resolve()

    # Check if .worktrees is in path
    if ".worktrees" in cwd.parts:
        # Extract worktree information
        for i, part in enumerate(cwd.parts):
            if part == ".worktrees" and i + 2 < len(cwd.parts):
                candidate_root = Path(*cwd.parts[:i])
                if (candidate_root / ".kittify").exists() or (candidate_root / ".git").exists():
                    worktree_name = cwd.parts[i + 1]
                    worktree_path = Path(*cwd.parts[: i + 2])
                    repo_root = candidate_root

                    return CurrentContext(
                        location=ExecutionContext.WORKTREE,
                        cwd=cwd,
                        repo_root=repo_root,
                        worktree_name=worktree_name,
                        worktree_path=worktree_path,
                    )

    # Not in worktree - assume main repo
    # Try to find repo root (directory containing .kittify or .git)
    repo_root = None
    search_path = cwd
    for _ in range(10):  # Limit depth
        if (search_path / ".kittify").exists() or (search_path / ".git").exists():
            repo_root = search_path
            break
        if search_path.parent == search_path:
            break  # Reached filesystem root
        search_path = search_path.parent

    return CurrentContext(
        location=ExecutionContext.MAIN_REPO,
        cwd=cwd,
        repo_root=repo_root,
        worktree_name=None,
        worktree_path=None,
    )


def x_detect_execution_context__mutmut_14(cwd: Path | None = None) -> CurrentContext:
    """Detect current execution context.

    Args:
        cwd: Current working directory (defaults to Path.cwd())

    Returns:
        CurrentContext with location, paths, and worktree info

    Example:
        >>> ctx = detect_execution_context()
        >>> if ctx.location == ExecutionContext.WORKTREE:
        ...     print(f"In worktree: {ctx.worktree_name}")
    """
    if cwd is None:
        cwd = Path.cwd().resolve()
    else:
        cwd = cwd.resolve()

    # Check if .worktrees is in path
    if ".worktrees" in cwd.parts:
        # Extract worktree information
        for i, part in enumerate(cwd.parts):
            if part == ".worktrees" and i + 1 <= len(cwd.parts):
                candidate_root = Path(*cwd.parts[:i])
                if (candidate_root / ".kittify").exists() or (candidate_root / ".git").exists():
                    worktree_name = cwd.parts[i + 1]
                    worktree_path = Path(*cwd.parts[: i + 2])
                    repo_root = candidate_root

                    return CurrentContext(
                        location=ExecutionContext.WORKTREE,
                        cwd=cwd,
                        repo_root=repo_root,
                        worktree_name=worktree_name,
                        worktree_path=worktree_path,
                    )

    # Not in worktree - assume main repo
    # Try to find repo root (directory containing .kittify or .git)
    repo_root = None
    search_path = cwd
    for _ in range(10):  # Limit depth
        if (search_path / ".kittify").exists() or (search_path / ".git").exists():
            repo_root = search_path
            break
        if search_path.parent == search_path:
            break  # Reached filesystem root
        search_path = search_path.parent

    return CurrentContext(
        location=ExecutionContext.MAIN_REPO,
        cwd=cwd,
        repo_root=repo_root,
        worktree_name=None,
        worktree_path=None,
    )


def x_detect_execution_context__mutmut_15(cwd: Path | None = None) -> CurrentContext:
    """Detect current execution context.

    Args:
        cwd: Current working directory (defaults to Path.cwd())

    Returns:
        CurrentContext with location, paths, and worktree info

    Example:
        >>> ctx = detect_execution_context()
        >>> if ctx.location == ExecutionContext.WORKTREE:
        ...     print(f"In worktree: {ctx.worktree_name}")
    """
    if cwd is None:
        cwd = Path.cwd().resolve()
    else:
        cwd = cwd.resolve()

    # Check if .worktrees is in path
    if ".worktrees" in cwd.parts:
        # Extract worktree information
        for i, part in enumerate(cwd.parts):
            if part == ".worktrees" and i + 1 < len(cwd.parts):
                candidate_root = None
                if (candidate_root / ".kittify").exists() or (candidate_root / ".git").exists():
                    worktree_name = cwd.parts[i + 1]
                    worktree_path = Path(*cwd.parts[: i + 2])
                    repo_root = candidate_root

                    return CurrentContext(
                        location=ExecutionContext.WORKTREE,
                        cwd=cwd,
                        repo_root=repo_root,
                        worktree_name=worktree_name,
                        worktree_path=worktree_path,
                    )

    # Not in worktree - assume main repo
    # Try to find repo root (directory containing .kittify or .git)
    repo_root = None
    search_path = cwd
    for _ in range(10):  # Limit depth
        if (search_path / ".kittify").exists() or (search_path / ".git").exists():
            repo_root = search_path
            break
        if search_path.parent == search_path:
            break  # Reached filesystem root
        search_path = search_path.parent

    return CurrentContext(
        location=ExecutionContext.MAIN_REPO,
        cwd=cwd,
        repo_root=repo_root,
        worktree_name=None,
        worktree_path=None,
    )


def x_detect_execution_context__mutmut_16(cwd: Path | None = None) -> CurrentContext:
    """Detect current execution context.

    Args:
        cwd: Current working directory (defaults to Path.cwd())

    Returns:
        CurrentContext with location, paths, and worktree info

    Example:
        >>> ctx = detect_execution_context()
        >>> if ctx.location == ExecutionContext.WORKTREE:
        ...     print(f"In worktree: {ctx.worktree_name}")
    """
    if cwd is None:
        cwd = Path.cwd().resolve()
    else:
        cwd = cwd.resolve()

    # Check if .worktrees is in path
    if ".worktrees" in cwd.parts:
        # Extract worktree information
        for i, part in enumerate(cwd.parts):
            if part == ".worktrees" and i + 1 < len(cwd.parts):
                candidate_root = Path(*cwd.parts[:i])
                if (candidate_root / ".kittify").exists() and (candidate_root / ".git").exists():
                    worktree_name = cwd.parts[i + 1]
                    worktree_path = Path(*cwd.parts[: i + 2])
                    repo_root = candidate_root

                    return CurrentContext(
                        location=ExecutionContext.WORKTREE,
                        cwd=cwd,
                        repo_root=repo_root,
                        worktree_name=worktree_name,
                        worktree_path=worktree_path,
                    )

    # Not in worktree - assume main repo
    # Try to find repo root (directory containing .kittify or .git)
    repo_root = None
    search_path = cwd
    for _ in range(10):  # Limit depth
        if (search_path / ".kittify").exists() or (search_path / ".git").exists():
            repo_root = search_path
            break
        if search_path.parent == search_path:
            break  # Reached filesystem root
        search_path = search_path.parent

    return CurrentContext(
        location=ExecutionContext.MAIN_REPO,
        cwd=cwd,
        repo_root=repo_root,
        worktree_name=None,
        worktree_path=None,
    )


def x_detect_execution_context__mutmut_17(cwd: Path | None = None) -> CurrentContext:
    """Detect current execution context.

    Args:
        cwd: Current working directory (defaults to Path.cwd())

    Returns:
        CurrentContext with location, paths, and worktree info

    Example:
        >>> ctx = detect_execution_context()
        >>> if ctx.location == ExecutionContext.WORKTREE:
        ...     print(f"In worktree: {ctx.worktree_name}")
    """
    if cwd is None:
        cwd = Path.cwd().resolve()
    else:
        cwd = cwd.resolve()

    # Check if .worktrees is in path
    if ".worktrees" in cwd.parts:
        # Extract worktree information
        for i, part in enumerate(cwd.parts):
            if part == ".worktrees" and i + 1 < len(cwd.parts):
                candidate_root = Path(*cwd.parts[:i])
                if (candidate_root * ".kittify").exists() or (candidate_root / ".git").exists():
                    worktree_name = cwd.parts[i + 1]
                    worktree_path = Path(*cwd.parts[: i + 2])
                    repo_root = candidate_root

                    return CurrentContext(
                        location=ExecutionContext.WORKTREE,
                        cwd=cwd,
                        repo_root=repo_root,
                        worktree_name=worktree_name,
                        worktree_path=worktree_path,
                    )

    # Not in worktree - assume main repo
    # Try to find repo root (directory containing .kittify or .git)
    repo_root = None
    search_path = cwd
    for _ in range(10):  # Limit depth
        if (search_path / ".kittify").exists() or (search_path / ".git").exists():
            repo_root = search_path
            break
        if search_path.parent == search_path:
            break  # Reached filesystem root
        search_path = search_path.parent

    return CurrentContext(
        location=ExecutionContext.MAIN_REPO,
        cwd=cwd,
        repo_root=repo_root,
        worktree_name=None,
        worktree_path=None,
    )


def x_detect_execution_context__mutmut_18(cwd: Path | None = None) -> CurrentContext:
    """Detect current execution context.

    Args:
        cwd: Current working directory (defaults to Path.cwd())

    Returns:
        CurrentContext with location, paths, and worktree info

    Example:
        >>> ctx = detect_execution_context()
        >>> if ctx.location == ExecutionContext.WORKTREE:
        ...     print(f"In worktree: {ctx.worktree_name}")
    """
    if cwd is None:
        cwd = Path.cwd().resolve()
    else:
        cwd = cwd.resolve()

    # Check if .worktrees is in path
    if ".worktrees" in cwd.parts:
        # Extract worktree information
        for i, part in enumerate(cwd.parts):
            if part == ".worktrees" and i + 1 < len(cwd.parts):
                candidate_root = Path(*cwd.parts[:i])
                if (candidate_root / "XX.kittifyXX").exists() or (candidate_root / ".git").exists():
                    worktree_name = cwd.parts[i + 1]
                    worktree_path = Path(*cwd.parts[: i + 2])
                    repo_root = candidate_root

                    return CurrentContext(
                        location=ExecutionContext.WORKTREE,
                        cwd=cwd,
                        repo_root=repo_root,
                        worktree_name=worktree_name,
                        worktree_path=worktree_path,
                    )

    # Not in worktree - assume main repo
    # Try to find repo root (directory containing .kittify or .git)
    repo_root = None
    search_path = cwd
    for _ in range(10):  # Limit depth
        if (search_path / ".kittify").exists() or (search_path / ".git").exists():
            repo_root = search_path
            break
        if search_path.parent == search_path:
            break  # Reached filesystem root
        search_path = search_path.parent

    return CurrentContext(
        location=ExecutionContext.MAIN_REPO,
        cwd=cwd,
        repo_root=repo_root,
        worktree_name=None,
        worktree_path=None,
    )


def x_detect_execution_context__mutmut_19(cwd: Path | None = None) -> CurrentContext:
    """Detect current execution context.

    Args:
        cwd: Current working directory (defaults to Path.cwd())

    Returns:
        CurrentContext with location, paths, and worktree info

    Example:
        >>> ctx = detect_execution_context()
        >>> if ctx.location == ExecutionContext.WORKTREE:
        ...     print(f"In worktree: {ctx.worktree_name}")
    """
    if cwd is None:
        cwd = Path.cwd().resolve()
    else:
        cwd = cwd.resolve()

    # Check if .worktrees is in path
    if ".worktrees" in cwd.parts:
        # Extract worktree information
        for i, part in enumerate(cwd.parts):
            if part == ".worktrees" and i + 1 < len(cwd.parts):
                candidate_root = Path(*cwd.parts[:i])
                if (candidate_root / ".KITTIFY").exists() or (candidate_root / ".git").exists():
                    worktree_name = cwd.parts[i + 1]
                    worktree_path = Path(*cwd.parts[: i + 2])
                    repo_root = candidate_root

                    return CurrentContext(
                        location=ExecutionContext.WORKTREE,
                        cwd=cwd,
                        repo_root=repo_root,
                        worktree_name=worktree_name,
                        worktree_path=worktree_path,
                    )

    # Not in worktree - assume main repo
    # Try to find repo root (directory containing .kittify or .git)
    repo_root = None
    search_path = cwd
    for _ in range(10):  # Limit depth
        if (search_path / ".kittify").exists() or (search_path / ".git").exists():
            repo_root = search_path
            break
        if search_path.parent == search_path:
            break  # Reached filesystem root
        search_path = search_path.parent

    return CurrentContext(
        location=ExecutionContext.MAIN_REPO,
        cwd=cwd,
        repo_root=repo_root,
        worktree_name=None,
        worktree_path=None,
    )


def x_detect_execution_context__mutmut_20(cwd: Path | None = None) -> CurrentContext:
    """Detect current execution context.

    Args:
        cwd: Current working directory (defaults to Path.cwd())

    Returns:
        CurrentContext with location, paths, and worktree info

    Example:
        >>> ctx = detect_execution_context()
        >>> if ctx.location == ExecutionContext.WORKTREE:
        ...     print(f"In worktree: {ctx.worktree_name}")
    """
    if cwd is None:
        cwd = Path.cwd().resolve()
    else:
        cwd = cwd.resolve()

    # Check if .worktrees is in path
    if ".worktrees" in cwd.parts:
        # Extract worktree information
        for i, part in enumerate(cwd.parts):
            if part == ".worktrees" and i + 1 < len(cwd.parts):
                candidate_root = Path(*cwd.parts[:i])
                if (candidate_root / ".kittify").exists() or (candidate_root * ".git").exists():
                    worktree_name = cwd.parts[i + 1]
                    worktree_path = Path(*cwd.parts[: i + 2])
                    repo_root = candidate_root

                    return CurrentContext(
                        location=ExecutionContext.WORKTREE,
                        cwd=cwd,
                        repo_root=repo_root,
                        worktree_name=worktree_name,
                        worktree_path=worktree_path,
                    )

    # Not in worktree - assume main repo
    # Try to find repo root (directory containing .kittify or .git)
    repo_root = None
    search_path = cwd
    for _ in range(10):  # Limit depth
        if (search_path / ".kittify").exists() or (search_path / ".git").exists():
            repo_root = search_path
            break
        if search_path.parent == search_path:
            break  # Reached filesystem root
        search_path = search_path.parent

    return CurrentContext(
        location=ExecutionContext.MAIN_REPO,
        cwd=cwd,
        repo_root=repo_root,
        worktree_name=None,
        worktree_path=None,
    )


def x_detect_execution_context__mutmut_21(cwd: Path | None = None) -> CurrentContext:
    """Detect current execution context.

    Args:
        cwd: Current working directory (defaults to Path.cwd())

    Returns:
        CurrentContext with location, paths, and worktree info

    Example:
        >>> ctx = detect_execution_context()
        >>> if ctx.location == ExecutionContext.WORKTREE:
        ...     print(f"In worktree: {ctx.worktree_name}")
    """
    if cwd is None:
        cwd = Path.cwd().resolve()
    else:
        cwd = cwd.resolve()

    # Check if .worktrees is in path
    if ".worktrees" in cwd.parts:
        # Extract worktree information
        for i, part in enumerate(cwd.parts):
            if part == ".worktrees" and i + 1 < len(cwd.parts):
                candidate_root = Path(*cwd.parts[:i])
                if (candidate_root / ".kittify").exists() or (candidate_root / "XX.gitXX").exists():
                    worktree_name = cwd.parts[i + 1]
                    worktree_path = Path(*cwd.parts[: i + 2])
                    repo_root = candidate_root

                    return CurrentContext(
                        location=ExecutionContext.WORKTREE,
                        cwd=cwd,
                        repo_root=repo_root,
                        worktree_name=worktree_name,
                        worktree_path=worktree_path,
                    )

    # Not in worktree - assume main repo
    # Try to find repo root (directory containing .kittify or .git)
    repo_root = None
    search_path = cwd
    for _ in range(10):  # Limit depth
        if (search_path / ".kittify").exists() or (search_path / ".git").exists():
            repo_root = search_path
            break
        if search_path.parent == search_path:
            break  # Reached filesystem root
        search_path = search_path.parent

    return CurrentContext(
        location=ExecutionContext.MAIN_REPO,
        cwd=cwd,
        repo_root=repo_root,
        worktree_name=None,
        worktree_path=None,
    )


def x_detect_execution_context__mutmut_22(cwd: Path | None = None) -> CurrentContext:
    """Detect current execution context.

    Args:
        cwd: Current working directory (defaults to Path.cwd())

    Returns:
        CurrentContext with location, paths, and worktree info

    Example:
        >>> ctx = detect_execution_context()
        >>> if ctx.location == ExecutionContext.WORKTREE:
        ...     print(f"In worktree: {ctx.worktree_name}")
    """
    if cwd is None:
        cwd = Path.cwd().resolve()
    else:
        cwd = cwd.resolve()

    # Check if .worktrees is in path
    if ".worktrees" in cwd.parts:
        # Extract worktree information
        for i, part in enumerate(cwd.parts):
            if part == ".worktrees" and i + 1 < len(cwd.parts):
                candidate_root = Path(*cwd.parts[:i])
                if (candidate_root / ".kittify").exists() or (candidate_root / ".GIT").exists():
                    worktree_name = cwd.parts[i + 1]
                    worktree_path = Path(*cwd.parts[: i + 2])
                    repo_root = candidate_root

                    return CurrentContext(
                        location=ExecutionContext.WORKTREE,
                        cwd=cwd,
                        repo_root=repo_root,
                        worktree_name=worktree_name,
                        worktree_path=worktree_path,
                    )

    # Not in worktree - assume main repo
    # Try to find repo root (directory containing .kittify or .git)
    repo_root = None
    search_path = cwd
    for _ in range(10):  # Limit depth
        if (search_path / ".kittify").exists() or (search_path / ".git").exists():
            repo_root = search_path
            break
        if search_path.parent == search_path:
            break  # Reached filesystem root
        search_path = search_path.parent

    return CurrentContext(
        location=ExecutionContext.MAIN_REPO,
        cwd=cwd,
        repo_root=repo_root,
        worktree_name=None,
        worktree_path=None,
    )


def x_detect_execution_context__mutmut_23(cwd: Path | None = None) -> CurrentContext:
    """Detect current execution context.

    Args:
        cwd: Current working directory (defaults to Path.cwd())

    Returns:
        CurrentContext with location, paths, and worktree info

    Example:
        >>> ctx = detect_execution_context()
        >>> if ctx.location == ExecutionContext.WORKTREE:
        ...     print(f"In worktree: {ctx.worktree_name}")
    """
    if cwd is None:
        cwd = Path.cwd().resolve()
    else:
        cwd = cwd.resolve()

    # Check if .worktrees is in path
    if ".worktrees" in cwd.parts:
        # Extract worktree information
        for i, part in enumerate(cwd.parts):
            if part == ".worktrees" and i + 1 < len(cwd.parts):
                candidate_root = Path(*cwd.parts[:i])
                if (candidate_root / ".kittify").exists() or (candidate_root / ".git").exists():
                    worktree_name = None
                    worktree_path = Path(*cwd.parts[: i + 2])
                    repo_root = candidate_root

                    return CurrentContext(
                        location=ExecutionContext.WORKTREE,
                        cwd=cwd,
                        repo_root=repo_root,
                        worktree_name=worktree_name,
                        worktree_path=worktree_path,
                    )

    # Not in worktree - assume main repo
    # Try to find repo root (directory containing .kittify or .git)
    repo_root = None
    search_path = cwd
    for _ in range(10):  # Limit depth
        if (search_path / ".kittify").exists() or (search_path / ".git").exists():
            repo_root = search_path
            break
        if search_path.parent == search_path:
            break  # Reached filesystem root
        search_path = search_path.parent

    return CurrentContext(
        location=ExecutionContext.MAIN_REPO,
        cwd=cwd,
        repo_root=repo_root,
        worktree_name=None,
        worktree_path=None,
    )


def x_detect_execution_context__mutmut_24(cwd: Path | None = None) -> CurrentContext:
    """Detect current execution context.

    Args:
        cwd: Current working directory (defaults to Path.cwd())

    Returns:
        CurrentContext with location, paths, and worktree info

    Example:
        >>> ctx = detect_execution_context()
        >>> if ctx.location == ExecutionContext.WORKTREE:
        ...     print(f"In worktree: {ctx.worktree_name}")
    """
    if cwd is None:
        cwd = Path.cwd().resolve()
    else:
        cwd = cwd.resolve()

    # Check if .worktrees is in path
    if ".worktrees" in cwd.parts:
        # Extract worktree information
        for i, part in enumerate(cwd.parts):
            if part == ".worktrees" and i + 1 < len(cwd.parts):
                candidate_root = Path(*cwd.parts[:i])
                if (candidate_root / ".kittify").exists() or (candidate_root / ".git").exists():
                    worktree_name = cwd.parts[i - 1]
                    worktree_path = Path(*cwd.parts[: i + 2])
                    repo_root = candidate_root

                    return CurrentContext(
                        location=ExecutionContext.WORKTREE,
                        cwd=cwd,
                        repo_root=repo_root,
                        worktree_name=worktree_name,
                        worktree_path=worktree_path,
                    )

    # Not in worktree - assume main repo
    # Try to find repo root (directory containing .kittify or .git)
    repo_root = None
    search_path = cwd
    for _ in range(10):  # Limit depth
        if (search_path / ".kittify").exists() or (search_path / ".git").exists():
            repo_root = search_path
            break
        if search_path.parent == search_path:
            break  # Reached filesystem root
        search_path = search_path.parent

    return CurrentContext(
        location=ExecutionContext.MAIN_REPO,
        cwd=cwd,
        repo_root=repo_root,
        worktree_name=None,
        worktree_path=None,
    )


def x_detect_execution_context__mutmut_25(cwd: Path | None = None) -> CurrentContext:
    """Detect current execution context.

    Args:
        cwd: Current working directory (defaults to Path.cwd())

    Returns:
        CurrentContext with location, paths, and worktree info

    Example:
        >>> ctx = detect_execution_context()
        >>> if ctx.location == ExecutionContext.WORKTREE:
        ...     print(f"In worktree: {ctx.worktree_name}")
    """
    if cwd is None:
        cwd = Path.cwd().resolve()
    else:
        cwd = cwd.resolve()

    # Check if .worktrees is in path
    if ".worktrees" in cwd.parts:
        # Extract worktree information
        for i, part in enumerate(cwd.parts):
            if part == ".worktrees" and i + 1 < len(cwd.parts):
                candidate_root = Path(*cwd.parts[:i])
                if (candidate_root / ".kittify").exists() or (candidate_root / ".git").exists():
                    worktree_name = cwd.parts[i + 2]
                    worktree_path = Path(*cwd.parts[: i + 2])
                    repo_root = candidate_root

                    return CurrentContext(
                        location=ExecutionContext.WORKTREE,
                        cwd=cwd,
                        repo_root=repo_root,
                        worktree_name=worktree_name,
                        worktree_path=worktree_path,
                    )

    # Not in worktree - assume main repo
    # Try to find repo root (directory containing .kittify or .git)
    repo_root = None
    search_path = cwd
    for _ in range(10):  # Limit depth
        if (search_path / ".kittify").exists() or (search_path / ".git").exists():
            repo_root = search_path
            break
        if search_path.parent == search_path:
            break  # Reached filesystem root
        search_path = search_path.parent

    return CurrentContext(
        location=ExecutionContext.MAIN_REPO,
        cwd=cwd,
        repo_root=repo_root,
        worktree_name=None,
        worktree_path=None,
    )


def x_detect_execution_context__mutmut_26(cwd: Path | None = None) -> CurrentContext:
    """Detect current execution context.

    Args:
        cwd: Current working directory (defaults to Path.cwd())

    Returns:
        CurrentContext with location, paths, and worktree info

    Example:
        >>> ctx = detect_execution_context()
        >>> if ctx.location == ExecutionContext.WORKTREE:
        ...     print(f"In worktree: {ctx.worktree_name}")
    """
    if cwd is None:
        cwd = Path.cwd().resolve()
    else:
        cwd = cwd.resolve()

    # Check if .worktrees is in path
    if ".worktrees" in cwd.parts:
        # Extract worktree information
        for i, part in enumerate(cwd.parts):
            if part == ".worktrees" and i + 1 < len(cwd.parts):
                candidate_root = Path(*cwd.parts[:i])
                if (candidate_root / ".kittify").exists() or (candidate_root / ".git").exists():
                    worktree_name = cwd.parts[i + 1]
                    worktree_path = None
                    repo_root = candidate_root

                    return CurrentContext(
                        location=ExecutionContext.WORKTREE,
                        cwd=cwd,
                        repo_root=repo_root,
                        worktree_name=worktree_name,
                        worktree_path=worktree_path,
                    )

    # Not in worktree - assume main repo
    # Try to find repo root (directory containing .kittify or .git)
    repo_root = None
    search_path = cwd
    for _ in range(10):  # Limit depth
        if (search_path / ".kittify").exists() or (search_path / ".git").exists():
            repo_root = search_path
            break
        if search_path.parent == search_path:
            break  # Reached filesystem root
        search_path = search_path.parent

    return CurrentContext(
        location=ExecutionContext.MAIN_REPO,
        cwd=cwd,
        repo_root=repo_root,
        worktree_name=None,
        worktree_path=None,
    )


def x_detect_execution_context__mutmut_27(cwd: Path | None = None) -> CurrentContext:
    """Detect current execution context.

    Args:
        cwd: Current working directory (defaults to Path.cwd())

    Returns:
        CurrentContext with location, paths, and worktree info

    Example:
        >>> ctx = detect_execution_context()
        >>> if ctx.location == ExecutionContext.WORKTREE:
        ...     print(f"In worktree: {ctx.worktree_name}")
    """
    if cwd is None:
        cwd = Path.cwd().resolve()
    else:
        cwd = cwd.resolve()

    # Check if .worktrees is in path
    if ".worktrees" in cwd.parts:
        # Extract worktree information
        for i, part in enumerate(cwd.parts):
            if part == ".worktrees" and i + 1 < len(cwd.parts):
                candidate_root = Path(*cwd.parts[:i])
                if (candidate_root / ".kittify").exists() or (candidate_root / ".git").exists():
                    worktree_name = cwd.parts[i + 1]
                    worktree_path = Path(*cwd.parts[: i - 2])
                    repo_root = candidate_root

                    return CurrentContext(
                        location=ExecutionContext.WORKTREE,
                        cwd=cwd,
                        repo_root=repo_root,
                        worktree_name=worktree_name,
                        worktree_path=worktree_path,
                    )

    # Not in worktree - assume main repo
    # Try to find repo root (directory containing .kittify or .git)
    repo_root = None
    search_path = cwd
    for _ in range(10):  # Limit depth
        if (search_path / ".kittify").exists() or (search_path / ".git").exists():
            repo_root = search_path
            break
        if search_path.parent == search_path:
            break  # Reached filesystem root
        search_path = search_path.parent

    return CurrentContext(
        location=ExecutionContext.MAIN_REPO,
        cwd=cwd,
        repo_root=repo_root,
        worktree_name=None,
        worktree_path=None,
    )


def x_detect_execution_context__mutmut_28(cwd: Path | None = None) -> CurrentContext:
    """Detect current execution context.

    Args:
        cwd: Current working directory (defaults to Path.cwd())

    Returns:
        CurrentContext with location, paths, and worktree info

    Example:
        >>> ctx = detect_execution_context()
        >>> if ctx.location == ExecutionContext.WORKTREE:
        ...     print(f"In worktree: {ctx.worktree_name}")
    """
    if cwd is None:
        cwd = Path.cwd().resolve()
    else:
        cwd = cwd.resolve()

    # Check if .worktrees is in path
    if ".worktrees" in cwd.parts:
        # Extract worktree information
        for i, part in enumerate(cwd.parts):
            if part == ".worktrees" and i + 1 < len(cwd.parts):
                candidate_root = Path(*cwd.parts[:i])
                if (candidate_root / ".kittify").exists() or (candidate_root / ".git").exists():
                    worktree_name = cwd.parts[i + 1]
                    worktree_path = Path(*cwd.parts[: i + 3])
                    repo_root = candidate_root

                    return CurrentContext(
                        location=ExecutionContext.WORKTREE,
                        cwd=cwd,
                        repo_root=repo_root,
                        worktree_name=worktree_name,
                        worktree_path=worktree_path,
                    )

    # Not in worktree - assume main repo
    # Try to find repo root (directory containing .kittify or .git)
    repo_root = None
    search_path = cwd
    for _ in range(10):  # Limit depth
        if (search_path / ".kittify").exists() or (search_path / ".git").exists():
            repo_root = search_path
            break
        if search_path.parent == search_path:
            break  # Reached filesystem root
        search_path = search_path.parent

    return CurrentContext(
        location=ExecutionContext.MAIN_REPO,
        cwd=cwd,
        repo_root=repo_root,
        worktree_name=None,
        worktree_path=None,
    )


def x_detect_execution_context__mutmut_29(cwd: Path | None = None) -> CurrentContext:
    """Detect current execution context.

    Args:
        cwd: Current working directory (defaults to Path.cwd())

    Returns:
        CurrentContext with location, paths, and worktree info

    Example:
        >>> ctx = detect_execution_context()
        >>> if ctx.location == ExecutionContext.WORKTREE:
        ...     print(f"In worktree: {ctx.worktree_name}")
    """
    if cwd is None:
        cwd = Path.cwd().resolve()
    else:
        cwd = cwd.resolve()

    # Check if .worktrees is in path
    if ".worktrees" in cwd.parts:
        # Extract worktree information
        for i, part in enumerate(cwd.parts):
            if part == ".worktrees" and i + 1 < len(cwd.parts):
                candidate_root = Path(*cwd.parts[:i])
                if (candidate_root / ".kittify").exists() or (candidate_root / ".git").exists():
                    worktree_name = cwd.parts[i + 1]
                    worktree_path = Path(*cwd.parts[: i + 2])
                    repo_root = None

                    return CurrentContext(
                        location=ExecutionContext.WORKTREE,
                        cwd=cwd,
                        repo_root=repo_root,
                        worktree_name=worktree_name,
                        worktree_path=worktree_path,
                    )

    # Not in worktree - assume main repo
    # Try to find repo root (directory containing .kittify or .git)
    repo_root = None
    search_path = cwd
    for _ in range(10):  # Limit depth
        if (search_path / ".kittify").exists() or (search_path / ".git").exists():
            repo_root = search_path
            break
        if search_path.parent == search_path:
            break  # Reached filesystem root
        search_path = search_path.parent

    return CurrentContext(
        location=ExecutionContext.MAIN_REPO,
        cwd=cwd,
        repo_root=repo_root,
        worktree_name=None,
        worktree_path=None,
    )


def x_detect_execution_context__mutmut_30(cwd: Path | None = None) -> CurrentContext:
    """Detect current execution context.

    Args:
        cwd: Current working directory (defaults to Path.cwd())

    Returns:
        CurrentContext with location, paths, and worktree info

    Example:
        >>> ctx = detect_execution_context()
        >>> if ctx.location == ExecutionContext.WORKTREE:
        ...     print(f"In worktree: {ctx.worktree_name}")
    """
    if cwd is None:
        cwd = Path.cwd().resolve()
    else:
        cwd = cwd.resolve()

    # Check if .worktrees is in path
    if ".worktrees" in cwd.parts:
        # Extract worktree information
        for i, part in enumerate(cwd.parts):
            if part == ".worktrees" and i + 1 < len(cwd.parts):
                candidate_root = Path(*cwd.parts[:i])
                if (candidate_root / ".kittify").exists() or (candidate_root / ".git").exists():
                    worktree_name = cwd.parts[i + 1]
                    worktree_path = Path(*cwd.parts[: i + 2])
                    repo_root = candidate_root

                    return CurrentContext(
                        location=None,
                        cwd=cwd,
                        repo_root=repo_root,
                        worktree_name=worktree_name,
                        worktree_path=worktree_path,
                    )

    # Not in worktree - assume main repo
    # Try to find repo root (directory containing .kittify or .git)
    repo_root = None
    search_path = cwd
    for _ in range(10):  # Limit depth
        if (search_path / ".kittify").exists() or (search_path / ".git").exists():
            repo_root = search_path
            break
        if search_path.parent == search_path:
            break  # Reached filesystem root
        search_path = search_path.parent

    return CurrentContext(
        location=ExecutionContext.MAIN_REPO,
        cwd=cwd,
        repo_root=repo_root,
        worktree_name=None,
        worktree_path=None,
    )


def x_detect_execution_context__mutmut_31(cwd: Path | None = None) -> CurrentContext:
    """Detect current execution context.

    Args:
        cwd: Current working directory (defaults to Path.cwd())

    Returns:
        CurrentContext with location, paths, and worktree info

    Example:
        >>> ctx = detect_execution_context()
        >>> if ctx.location == ExecutionContext.WORKTREE:
        ...     print(f"In worktree: {ctx.worktree_name}")
    """
    if cwd is None:
        cwd = Path.cwd().resolve()
    else:
        cwd = cwd.resolve()

    # Check if .worktrees is in path
    if ".worktrees" in cwd.parts:
        # Extract worktree information
        for i, part in enumerate(cwd.parts):
            if part == ".worktrees" and i + 1 < len(cwd.parts):
                candidate_root = Path(*cwd.parts[:i])
                if (candidate_root / ".kittify").exists() or (candidate_root / ".git").exists():
                    worktree_name = cwd.parts[i + 1]
                    worktree_path = Path(*cwd.parts[: i + 2])
                    repo_root = candidate_root

                    return CurrentContext(
                        location=ExecutionContext.WORKTREE,
                        cwd=None,
                        repo_root=repo_root,
                        worktree_name=worktree_name,
                        worktree_path=worktree_path,
                    )

    # Not in worktree - assume main repo
    # Try to find repo root (directory containing .kittify or .git)
    repo_root = None
    search_path = cwd
    for _ in range(10):  # Limit depth
        if (search_path / ".kittify").exists() or (search_path / ".git").exists():
            repo_root = search_path
            break
        if search_path.parent == search_path:
            break  # Reached filesystem root
        search_path = search_path.parent

    return CurrentContext(
        location=ExecutionContext.MAIN_REPO,
        cwd=cwd,
        repo_root=repo_root,
        worktree_name=None,
        worktree_path=None,
    )


def x_detect_execution_context__mutmut_32(cwd: Path | None = None) -> CurrentContext:
    """Detect current execution context.

    Args:
        cwd: Current working directory (defaults to Path.cwd())

    Returns:
        CurrentContext with location, paths, and worktree info

    Example:
        >>> ctx = detect_execution_context()
        >>> if ctx.location == ExecutionContext.WORKTREE:
        ...     print(f"In worktree: {ctx.worktree_name}")
    """
    if cwd is None:
        cwd = Path.cwd().resolve()
    else:
        cwd = cwd.resolve()

    # Check if .worktrees is in path
    if ".worktrees" in cwd.parts:
        # Extract worktree information
        for i, part in enumerate(cwd.parts):
            if part == ".worktrees" and i + 1 < len(cwd.parts):
                candidate_root = Path(*cwd.parts[:i])
                if (candidate_root / ".kittify").exists() or (candidate_root / ".git").exists():
                    worktree_name = cwd.parts[i + 1]
                    worktree_path = Path(*cwd.parts[: i + 2])
                    repo_root = candidate_root

                    return CurrentContext(
                        location=ExecutionContext.WORKTREE,
                        cwd=cwd,
                        repo_root=None,
                        worktree_name=worktree_name,
                        worktree_path=worktree_path,
                    )

    # Not in worktree - assume main repo
    # Try to find repo root (directory containing .kittify or .git)
    repo_root = None
    search_path = cwd
    for _ in range(10):  # Limit depth
        if (search_path / ".kittify").exists() or (search_path / ".git").exists():
            repo_root = search_path
            break
        if search_path.parent == search_path:
            break  # Reached filesystem root
        search_path = search_path.parent

    return CurrentContext(
        location=ExecutionContext.MAIN_REPO,
        cwd=cwd,
        repo_root=repo_root,
        worktree_name=None,
        worktree_path=None,
    )


def x_detect_execution_context__mutmut_33(cwd: Path | None = None) -> CurrentContext:
    """Detect current execution context.

    Args:
        cwd: Current working directory (defaults to Path.cwd())

    Returns:
        CurrentContext with location, paths, and worktree info

    Example:
        >>> ctx = detect_execution_context()
        >>> if ctx.location == ExecutionContext.WORKTREE:
        ...     print(f"In worktree: {ctx.worktree_name}")
    """
    if cwd is None:
        cwd = Path.cwd().resolve()
    else:
        cwd = cwd.resolve()

    # Check if .worktrees is in path
    if ".worktrees" in cwd.parts:
        # Extract worktree information
        for i, part in enumerate(cwd.parts):
            if part == ".worktrees" and i + 1 < len(cwd.parts):
                candidate_root = Path(*cwd.parts[:i])
                if (candidate_root / ".kittify").exists() or (candidate_root / ".git").exists():
                    worktree_name = cwd.parts[i + 1]
                    worktree_path = Path(*cwd.parts[: i + 2])
                    repo_root = candidate_root

                    return CurrentContext(
                        location=ExecutionContext.WORKTREE,
                        cwd=cwd,
                        repo_root=repo_root,
                        worktree_name=None,
                        worktree_path=worktree_path,
                    )

    # Not in worktree - assume main repo
    # Try to find repo root (directory containing .kittify or .git)
    repo_root = None
    search_path = cwd
    for _ in range(10):  # Limit depth
        if (search_path / ".kittify").exists() or (search_path / ".git").exists():
            repo_root = search_path
            break
        if search_path.parent == search_path:
            break  # Reached filesystem root
        search_path = search_path.parent

    return CurrentContext(
        location=ExecutionContext.MAIN_REPO,
        cwd=cwd,
        repo_root=repo_root,
        worktree_name=None,
        worktree_path=None,
    )


def x_detect_execution_context__mutmut_34(cwd: Path | None = None) -> CurrentContext:
    """Detect current execution context.

    Args:
        cwd: Current working directory (defaults to Path.cwd())

    Returns:
        CurrentContext with location, paths, and worktree info

    Example:
        >>> ctx = detect_execution_context()
        >>> if ctx.location == ExecutionContext.WORKTREE:
        ...     print(f"In worktree: {ctx.worktree_name}")
    """
    if cwd is None:
        cwd = Path.cwd().resolve()
    else:
        cwd = cwd.resolve()

    # Check if .worktrees is in path
    if ".worktrees" in cwd.parts:
        # Extract worktree information
        for i, part in enumerate(cwd.parts):
            if part == ".worktrees" and i + 1 < len(cwd.parts):
                candidate_root = Path(*cwd.parts[:i])
                if (candidate_root / ".kittify").exists() or (candidate_root / ".git").exists():
                    worktree_name = cwd.parts[i + 1]
                    worktree_path = Path(*cwd.parts[: i + 2])
                    repo_root = candidate_root

                    return CurrentContext(
                        location=ExecutionContext.WORKTREE,
                        cwd=cwd,
                        repo_root=repo_root,
                        worktree_name=worktree_name,
                        worktree_path=None,
                    )

    # Not in worktree - assume main repo
    # Try to find repo root (directory containing .kittify or .git)
    repo_root = None
    search_path = cwd
    for _ in range(10):  # Limit depth
        if (search_path / ".kittify").exists() or (search_path / ".git").exists():
            repo_root = search_path
            break
        if search_path.parent == search_path:
            break  # Reached filesystem root
        search_path = search_path.parent

    return CurrentContext(
        location=ExecutionContext.MAIN_REPO,
        cwd=cwd,
        repo_root=repo_root,
        worktree_name=None,
        worktree_path=None,
    )


def x_detect_execution_context__mutmut_35(cwd: Path | None = None) -> CurrentContext:
    """Detect current execution context.

    Args:
        cwd: Current working directory (defaults to Path.cwd())

    Returns:
        CurrentContext with location, paths, and worktree info

    Example:
        >>> ctx = detect_execution_context()
        >>> if ctx.location == ExecutionContext.WORKTREE:
        ...     print(f"In worktree: {ctx.worktree_name}")
    """
    if cwd is None:
        cwd = Path.cwd().resolve()
    else:
        cwd = cwd.resolve()

    # Check if .worktrees is in path
    if ".worktrees" in cwd.parts:
        # Extract worktree information
        for i, part in enumerate(cwd.parts):
            if part == ".worktrees" and i + 1 < len(cwd.parts):
                candidate_root = Path(*cwd.parts[:i])
                if (candidate_root / ".kittify").exists() or (candidate_root / ".git").exists():
                    worktree_name = cwd.parts[i + 1]
                    worktree_path = Path(*cwd.parts[: i + 2])
                    repo_root = candidate_root

                    return CurrentContext(
                        cwd=cwd,
                        repo_root=repo_root,
                        worktree_name=worktree_name,
                        worktree_path=worktree_path,
                    )

    # Not in worktree - assume main repo
    # Try to find repo root (directory containing .kittify or .git)
    repo_root = None
    search_path = cwd
    for _ in range(10):  # Limit depth
        if (search_path / ".kittify").exists() or (search_path / ".git").exists():
            repo_root = search_path
            break
        if search_path.parent == search_path:
            break  # Reached filesystem root
        search_path = search_path.parent

    return CurrentContext(
        location=ExecutionContext.MAIN_REPO,
        cwd=cwd,
        repo_root=repo_root,
        worktree_name=None,
        worktree_path=None,
    )


def x_detect_execution_context__mutmut_36(cwd: Path | None = None) -> CurrentContext:
    """Detect current execution context.

    Args:
        cwd: Current working directory (defaults to Path.cwd())

    Returns:
        CurrentContext with location, paths, and worktree info

    Example:
        >>> ctx = detect_execution_context()
        >>> if ctx.location == ExecutionContext.WORKTREE:
        ...     print(f"In worktree: {ctx.worktree_name}")
    """
    if cwd is None:
        cwd = Path.cwd().resolve()
    else:
        cwd = cwd.resolve()

    # Check if .worktrees is in path
    if ".worktrees" in cwd.parts:
        # Extract worktree information
        for i, part in enumerate(cwd.parts):
            if part == ".worktrees" and i + 1 < len(cwd.parts):
                candidate_root = Path(*cwd.parts[:i])
                if (candidate_root / ".kittify").exists() or (candidate_root / ".git").exists():
                    worktree_name = cwd.parts[i + 1]
                    worktree_path = Path(*cwd.parts[: i + 2])
                    repo_root = candidate_root

                    return CurrentContext(
                        location=ExecutionContext.WORKTREE,
                        repo_root=repo_root,
                        worktree_name=worktree_name,
                        worktree_path=worktree_path,
                    )

    # Not in worktree - assume main repo
    # Try to find repo root (directory containing .kittify or .git)
    repo_root = None
    search_path = cwd
    for _ in range(10):  # Limit depth
        if (search_path / ".kittify").exists() or (search_path / ".git").exists():
            repo_root = search_path
            break
        if search_path.parent == search_path:
            break  # Reached filesystem root
        search_path = search_path.parent

    return CurrentContext(
        location=ExecutionContext.MAIN_REPO,
        cwd=cwd,
        repo_root=repo_root,
        worktree_name=None,
        worktree_path=None,
    )


def x_detect_execution_context__mutmut_37(cwd: Path | None = None) -> CurrentContext:
    """Detect current execution context.

    Args:
        cwd: Current working directory (defaults to Path.cwd())

    Returns:
        CurrentContext with location, paths, and worktree info

    Example:
        >>> ctx = detect_execution_context()
        >>> if ctx.location == ExecutionContext.WORKTREE:
        ...     print(f"In worktree: {ctx.worktree_name}")
    """
    if cwd is None:
        cwd = Path.cwd().resolve()
    else:
        cwd = cwd.resolve()

    # Check if .worktrees is in path
    if ".worktrees" in cwd.parts:
        # Extract worktree information
        for i, part in enumerate(cwd.parts):
            if part == ".worktrees" and i + 1 < len(cwd.parts):
                candidate_root = Path(*cwd.parts[:i])
                if (candidate_root / ".kittify").exists() or (candidate_root / ".git").exists():
                    worktree_name = cwd.parts[i + 1]
                    worktree_path = Path(*cwd.parts[: i + 2])
                    repo_root = candidate_root

                    return CurrentContext(
                        location=ExecutionContext.WORKTREE,
                        cwd=cwd,
                        worktree_name=worktree_name,
                        worktree_path=worktree_path,
                    )

    # Not in worktree - assume main repo
    # Try to find repo root (directory containing .kittify or .git)
    repo_root = None
    search_path = cwd
    for _ in range(10):  # Limit depth
        if (search_path / ".kittify").exists() or (search_path / ".git").exists():
            repo_root = search_path
            break
        if search_path.parent == search_path:
            break  # Reached filesystem root
        search_path = search_path.parent

    return CurrentContext(
        location=ExecutionContext.MAIN_REPO,
        cwd=cwd,
        repo_root=repo_root,
        worktree_name=None,
        worktree_path=None,
    )


def x_detect_execution_context__mutmut_38(cwd: Path | None = None) -> CurrentContext:
    """Detect current execution context.

    Args:
        cwd: Current working directory (defaults to Path.cwd())

    Returns:
        CurrentContext with location, paths, and worktree info

    Example:
        >>> ctx = detect_execution_context()
        >>> if ctx.location == ExecutionContext.WORKTREE:
        ...     print(f"In worktree: {ctx.worktree_name}")
    """
    if cwd is None:
        cwd = Path.cwd().resolve()
    else:
        cwd = cwd.resolve()

    # Check if .worktrees is in path
    if ".worktrees" in cwd.parts:
        # Extract worktree information
        for i, part in enumerate(cwd.parts):
            if part == ".worktrees" and i + 1 < len(cwd.parts):
                candidate_root = Path(*cwd.parts[:i])
                if (candidate_root / ".kittify").exists() or (candidate_root / ".git").exists():
                    worktree_name = cwd.parts[i + 1]
                    worktree_path = Path(*cwd.parts[: i + 2])
                    repo_root = candidate_root

                    return CurrentContext(
                        location=ExecutionContext.WORKTREE,
                        cwd=cwd,
                        repo_root=repo_root,
                        worktree_path=worktree_path,
                    )

    # Not in worktree - assume main repo
    # Try to find repo root (directory containing .kittify or .git)
    repo_root = None
    search_path = cwd
    for _ in range(10):  # Limit depth
        if (search_path / ".kittify").exists() or (search_path / ".git").exists():
            repo_root = search_path
            break
        if search_path.parent == search_path:
            break  # Reached filesystem root
        search_path = search_path.parent

    return CurrentContext(
        location=ExecutionContext.MAIN_REPO,
        cwd=cwd,
        repo_root=repo_root,
        worktree_name=None,
        worktree_path=None,
    )


def x_detect_execution_context__mutmut_39(cwd: Path | None = None) -> CurrentContext:
    """Detect current execution context.

    Args:
        cwd: Current working directory (defaults to Path.cwd())

    Returns:
        CurrentContext with location, paths, and worktree info

    Example:
        >>> ctx = detect_execution_context()
        >>> if ctx.location == ExecutionContext.WORKTREE:
        ...     print(f"In worktree: {ctx.worktree_name}")
    """
    if cwd is None:
        cwd = Path.cwd().resolve()
    else:
        cwd = cwd.resolve()

    # Check if .worktrees is in path
    if ".worktrees" in cwd.parts:
        # Extract worktree information
        for i, part in enumerate(cwd.parts):
            if part == ".worktrees" and i + 1 < len(cwd.parts):
                candidate_root = Path(*cwd.parts[:i])
                if (candidate_root / ".kittify").exists() or (candidate_root / ".git").exists():
                    worktree_name = cwd.parts[i + 1]
                    worktree_path = Path(*cwd.parts[: i + 2])
                    repo_root = candidate_root

                    return CurrentContext(
                        location=ExecutionContext.WORKTREE,
                        cwd=cwd,
                        repo_root=repo_root,
                        worktree_name=worktree_name,
                        )

    # Not in worktree - assume main repo
    # Try to find repo root (directory containing .kittify or .git)
    repo_root = None
    search_path = cwd
    for _ in range(10):  # Limit depth
        if (search_path / ".kittify").exists() or (search_path / ".git").exists():
            repo_root = search_path
            break
        if search_path.parent == search_path:
            break  # Reached filesystem root
        search_path = search_path.parent

    return CurrentContext(
        location=ExecutionContext.MAIN_REPO,
        cwd=cwd,
        repo_root=repo_root,
        worktree_name=None,
        worktree_path=None,
    )


def x_detect_execution_context__mutmut_40(cwd: Path | None = None) -> CurrentContext:
    """Detect current execution context.

    Args:
        cwd: Current working directory (defaults to Path.cwd())

    Returns:
        CurrentContext with location, paths, and worktree info

    Example:
        >>> ctx = detect_execution_context()
        >>> if ctx.location == ExecutionContext.WORKTREE:
        ...     print(f"In worktree: {ctx.worktree_name}")
    """
    if cwd is None:
        cwd = Path.cwd().resolve()
    else:
        cwd = cwd.resolve()

    # Check if .worktrees is in path
    if ".worktrees" in cwd.parts:
        # Extract worktree information
        for i, part in enumerate(cwd.parts):
            if part == ".worktrees" and i + 1 < len(cwd.parts):
                candidate_root = Path(*cwd.parts[:i])
                if (candidate_root / ".kittify").exists() or (candidate_root / ".git").exists():
                    worktree_name = cwd.parts[i + 1]
                    worktree_path = Path(*cwd.parts[: i + 2])
                    repo_root = candidate_root

                    return CurrentContext(
                        location=ExecutionContext.WORKTREE,
                        cwd=cwd,
                        repo_root=repo_root,
                        worktree_name=worktree_name,
                        worktree_path=worktree_path,
                    )

    # Not in worktree - assume main repo
    # Try to find repo root (directory containing .kittify or .git)
    repo_root = ""
    search_path = cwd
    for _ in range(10):  # Limit depth
        if (search_path / ".kittify").exists() or (search_path / ".git").exists():
            repo_root = search_path
            break
        if search_path.parent == search_path:
            break  # Reached filesystem root
        search_path = search_path.parent

    return CurrentContext(
        location=ExecutionContext.MAIN_REPO,
        cwd=cwd,
        repo_root=repo_root,
        worktree_name=None,
        worktree_path=None,
    )


def x_detect_execution_context__mutmut_41(cwd: Path | None = None) -> CurrentContext:
    """Detect current execution context.

    Args:
        cwd: Current working directory (defaults to Path.cwd())

    Returns:
        CurrentContext with location, paths, and worktree info

    Example:
        >>> ctx = detect_execution_context()
        >>> if ctx.location == ExecutionContext.WORKTREE:
        ...     print(f"In worktree: {ctx.worktree_name}")
    """
    if cwd is None:
        cwd = Path.cwd().resolve()
    else:
        cwd = cwd.resolve()

    # Check if .worktrees is in path
    if ".worktrees" in cwd.parts:
        # Extract worktree information
        for i, part in enumerate(cwd.parts):
            if part == ".worktrees" and i + 1 < len(cwd.parts):
                candidate_root = Path(*cwd.parts[:i])
                if (candidate_root / ".kittify").exists() or (candidate_root / ".git").exists():
                    worktree_name = cwd.parts[i + 1]
                    worktree_path = Path(*cwd.parts[: i + 2])
                    repo_root = candidate_root

                    return CurrentContext(
                        location=ExecutionContext.WORKTREE,
                        cwd=cwd,
                        repo_root=repo_root,
                        worktree_name=worktree_name,
                        worktree_path=worktree_path,
                    )

    # Not in worktree - assume main repo
    # Try to find repo root (directory containing .kittify or .git)
    repo_root = None
    search_path = None
    for _ in range(10):  # Limit depth
        if (search_path / ".kittify").exists() or (search_path / ".git").exists():
            repo_root = search_path
            break
        if search_path.parent == search_path:
            break  # Reached filesystem root
        search_path = search_path.parent

    return CurrentContext(
        location=ExecutionContext.MAIN_REPO,
        cwd=cwd,
        repo_root=repo_root,
        worktree_name=None,
        worktree_path=None,
    )


def x_detect_execution_context__mutmut_42(cwd: Path | None = None) -> CurrentContext:
    """Detect current execution context.

    Args:
        cwd: Current working directory (defaults to Path.cwd())

    Returns:
        CurrentContext with location, paths, and worktree info

    Example:
        >>> ctx = detect_execution_context()
        >>> if ctx.location == ExecutionContext.WORKTREE:
        ...     print(f"In worktree: {ctx.worktree_name}")
    """
    if cwd is None:
        cwd = Path.cwd().resolve()
    else:
        cwd = cwd.resolve()

    # Check if .worktrees is in path
    if ".worktrees" in cwd.parts:
        # Extract worktree information
        for i, part in enumerate(cwd.parts):
            if part == ".worktrees" and i + 1 < len(cwd.parts):
                candidate_root = Path(*cwd.parts[:i])
                if (candidate_root / ".kittify").exists() or (candidate_root / ".git").exists():
                    worktree_name = cwd.parts[i + 1]
                    worktree_path = Path(*cwd.parts[: i + 2])
                    repo_root = candidate_root

                    return CurrentContext(
                        location=ExecutionContext.WORKTREE,
                        cwd=cwd,
                        repo_root=repo_root,
                        worktree_name=worktree_name,
                        worktree_path=worktree_path,
                    )

    # Not in worktree - assume main repo
    # Try to find repo root (directory containing .kittify or .git)
    repo_root = None
    search_path = cwd
    for _ in range(None):  # Limit depth
        if (search_path / ".kittify").exists() or (search_path / ".git").exists():
            repo_root = search_path
            break
        if search_path.parent == search_path:
            break  # Reached filesystem root
        search_path = search_path.parent

    return CurrentContext(
        location=ExecutionContext.MAIN_REPO,
        cwd=cwd,
        repo_root=repo_root,
        worktree_name=None,
        worktree_path=None,
    )


def x_detect_execution_context__mutmut_43(cwd: Path | None = None) -> CurrentContext:
    """Detect current execution context.

    Args:
        cwd: Current working directory (defaults to Path.cwd())

    Returns:
        CurrentContext with location, paths, and worktree info

    Example:
        >>> ctx = detect_execution_context()
        >>> if ctx.location == ExecutionContext.WORKTREE:
        ...     print(f"In worktree: {ctx.worktree_name}")
    """
    if cwd is None:
        cwd = Path.cwd().resolve()
    else:
        cwd = cwd.resolve()

    # Check if .worktrees is in path
    if ".worktrees" in cwd.parts:
        # Extract worktree information
        for i, part in enumerate(cwd.parts):
            if part == ".worktrees" and i + 1 < len(cwd.parts):
                candidate_root = Path(*cwd.parts[:i])
                if (candidate_root / ".kittify").exists() or (candidate_root / ".git").exists():
                    worktree_name = cwd.parts[i + 1]
                    worktree_path = Path(*cwd.parts[: i + 2])
                    repo_root = candidate_root

                    return CurrentContext(
                        location=ExecutionContext.WORKTREE,
                        cwd=cwd,
                        repo_root=repo_root,
                        worktree_name=worktree_name,
                        worktree_path=worktree_path,
                    )

    # Not in worktree - assume main repo
    # Try to find repo root (directory containing .kittify or .git)
    repo_root = None
    search_path = cwd
    for _ in range(11):  # Limit depth
        if (search_path / ".kittify").exists() or (search_path / ".git").exists():
            repo_root = search_path
            break
        if search_path.parent == search_path:
            break  # Reached filesystem root
        search_path = search_path.parent

    return CurrentContext(
        location=ExecutionContext.MAIN_REPO,
        cwd=cwd,
        repo_root=repo_root,
        worktree_name=None,
        worktree_path=None,
    )


def x_detect_execution_context__mutmut_44(cwd: Path | None = None) -> CurrentContext:
    """Detect current execution context.

    Args:
        cwd: Current working directory (defaults to Path.cwd())

    Returns:
        CurrentContext with location, paths, and worktree info

    Example:
        >>> ctx = detect_execution_context()
        >>> if ctx.location == ExecutionContext.WORKTREE:
        ...     print(f"In worktree: {ctx.worktree_name}")
    """
    if cwd is None:
        cwd = Path.cwd().resolve()
    else:
        cwd = cwd.resolve()

    # Check if .worktrees is in path
    if ".worktrees" in cwd.parts:
        # Extract worktree information
        for i, part in enumerate(cwd.parts):
            if part == ".worktrees" and i + 1 < len(cwd.parts):
                candidate_root = Path(*cwd.parts[:i])
                if (candidate_root / ".kittify").exists() or (candidate_root / ".git").exists():
                    worktree_name = cwd.parts[i + 1]
                    worktree_path = Path(*cwd.parts[: i + 2])
                    repo_root = candidate_root

                    return CurrentContext(
                        location=ExecutionContext.WORKTREE,
                        cwd=cwd,
                        repo_root=repo_root,
                        worktree_name=worktree_name,
                        worktree_path=worktree_path,
                    )

    # Not in worktree - assume main repo
    # Try to find repo root (directory containing .kittify or .git)
    repo_root = None
    search_path = cwd
    for _ in range(10):  # Limit depth
        if (search_path / ".kittify").exists() and (search_path / ".git").exists():
            repo_root = search_path
            break
        if search_path.parent == search_path:
            break  # Reached filesystem root
        search_path = search_path.parent

    return CurrentContext(
        location=ExecutionContext.MAIN_REPO,
        cwd=cwd,
        repo_root=repo_root,
        worktree_name=None,
        worktree_path=None,
    )


def x_detect_execution_context__mutmut_45(cwd: Path | None = None) -> CurrentContext:
    """Detect current execution context.

    Args:
        cwd: Current working directory (defaults to Path.cwd())

    Returns:
        CurrentContext with location, paths, and worktree info

    Example:
        >>> ctx = detect_execution_context()
        >>> if ctx.location == ExecutionContext.WORKTREE:
        ...     print(f"In worktree: {ctx.worktree_name}")
    """
    if cwd is None:
        cwd = Path.cwd().resolve()
    else:
        cwd = cwd.resolve()

    # Check if .worktrees is in path
    if ".worktrees" in cwd.parts:
        # Extract worktree information
        for i, part in enumerate(cwd.parts):
            if part == ".worktrees" and i + 1 < len(cwd.parts):
                candidate_root = Path(*cwd.parts[:i])
                if (candidate_root / ".kittify").exists() or (candidate_root / ".git").exists():
                    worktree_name = cwd.parts[i + 1]
                    worktree_path = Path(*cwd.parts[: i + 2])
                    repo_root = candidate_root

                    return CurrentContext(
                        location=ExecutionContext.WORKTREE,
                        cwd=cwd,
                        repo_root=repo_root,
                        worktree_name=worktree_name,
                        worktree_path=worktree_path,
                    )

    # Not in worktree - assume main repo
    # Try to find repo root (directory containing .kittify or .git)
    repo_root = None
    search_path = cwd
    for _ in range(10):  # Limit depth
        if (search_path * ".kittify").exists() or (search_path / ".git").exists():
            repo_root = search_path
            break
        if search_path.parent == search_path:
            break  # Reached filesystem root
        search_path = search_path.parent

    return CurrentContext(
        location=ExecutionContext.MAIN_REPO,
        cwd=cwd,
        repo_root=repo_root,
        worktree_name=None,
        worktree_path=None,
    )


def x_detect_execution_context__mutmut_46(cwd: Path | None = None) -> CurrentContext:
    """Detect current execution context.

    Args:
        cwd: Current working directory (defaults to Path.cwd())

    Returns:
        CurrentContext with location, paths, and worktree info

    Example:
        >>> ctx = detect_execution_context()
        >>> if ctx.location == ExecutionContext.WORKTREE:
        ...     print(f"In worktree: {ctx.worktree_name}")
    """
    if cwd is None:
        cwd = Path.cwd().resolve()
    else:
        cwd = cwd.resolve()

    # Check if .worktrees is in path
    if ".worktrees" in cwd.parts:
        # Extract worktree information
        for i, part in enumerate(cwd.parts):
            if part == ".worktrees" and i + 1 < len(cwd.parts):
                candidate_root = Path(*cwd.parts[:i])
                if (candidate_root / ".kittify").exists() or (candidate_root / ".git").exists():
                    worktree_name = cwd.parts[i + 1]
                    worktree_path = Path(*cwd.parts[: i + 2])
                    repo_root = candidate_root

                    return CurrentContext(
                        location=ExecutionContext.WORKTREE,
                        cwd=cwd,
                        repo_root=repo_root,
                        worktree_name=worktree_name,
                        worktree_path=worktree_path,
                    )

    # Not in worktree - assume main repo
    # Try to find repo root (directory containing .kittify or .git)
    repo_root = None
    search_path = cwd
    for _ in range(10):  # Limit depth
        if (search_path / "XX.kittifyXX").exists() or (search_path / ".git").exists():
            repo_root = search_path
            break
        if search_path.parent == search_path:
            break  # Reached filesystem root
        search_path = search_path.parent

    return CurrentContext(
        location=ExecutionContext.MAIN_REPO,
        cwd=cwd,
        repo_root=repo_root,
        worktree_name=None,
        worktree_path=None,
    )


def x_detect_execution_context__mutmut_47(cwd: Path | None = None) -> CurrentContext:
    """Detect current execution context.

    Args:
        cwd: Current working directory (defaults to Path.cwd())

    Returns:
        CurrentContext with location, paths, and worktree info

    Example:
        >>> ctx = detect_execution_context()
        >>> if ctx.location == ExecutionContext.WORKTREE:
        ...     print(f"In worktree: {ctx.worktree_name}")
    """
    if cwd is None:
        cwd = Path.cwd().resolve()
    else:
        cwd = cwd.resolve()

    # Check if .worktrees is in path
    if ".worktrees" in cwd.parts:
        # Extract worktree information
        for i, part in enumerate(cwd.parts):
            if part == ".worktrees" and i + 1 < len(cwd.parts):
                candidate_root = Path(*cwd.parts[:i])
                if (candidate_root / ".kittify").exists() or (candidate_root / ".git").exists():
                    worktree_name = cwd.parts[i + 1]
                    worktree_path = Path(*cwd.parts[: i + 2])
                    repo_root = candidate_root

                    return CurrentContext(
                        location=ExecutionContext.WORKTREE,
                        cwd=cwd,
                        repo_root=repo_root,
                        worktree_name=worktree_name,
                        worktree_path=worktree_path,
                    )

    # Not in worktree - assume main repo
    # Try to find repo root (directory containing .kittify or .git)
    repo_root = None
    search_path = cwd
    for _ in range(10):  # Limit depth
        if (search_path / ".KITTIFY").exists() or (search_path / ".git").exists():
            repo_root = search_path
            break
        if search_path.parent == search_path:
            break  # Reached filesystem root
        search_path = search_path.parent

    return CurrentContext(
        location=ExecutionContext.MAIN_REPO,
        cwd=cwd,
        repo_root=repo_root,
        worktree_name=None,
        worktree_path=None,
    )


def x_detect_execution_context__mutmut_48(cwd: Path | None = None) -> CurrentContext:
    """Detect current execution context.

    Args:
        cwd: Current working directory (defaults to Path.cwd())

    Returns:
        CurrentContext with location, paths, and worktree info

    Example:
        >>> ctx = detect_execution_context()
        >>> if ctx.location == ExecutionContext.WORKTREE:
        ...     print(f"In worktree: {ctx.worktree_name}")
    """
    if cwd is None:
        cwd = Path.cwd().resolve()
    else:
        cwd = cwd.resolve()

    # Check if .worktrees is in path
    if ".worktrees" in cwd.parts:
        # Extract worktree information
        for i, part in enumerate(cwd.parts):
            if part == ".worktrees" and i + 1 < len(cwd.parts):
                candidate_root = Path(*cwd.parts[:i])
                if (candidate_root / ".kittify").exists() or (candidate_root / ".git").exists():
                    worktree_name = cwd.parts[i + 1]
                    worktree_path = Path(*cwd.parts[: i + 2])
                    repo_root = candidate_root

                    return CurrentContext(
                        location=ExecutionContext.WORKTREE,
                        cwd=cwd,
                        repo_root=repo_root,
                        worktree_name=worktree_name,
                        worktree_path=worktree_path,
                    )

    # Not in worktree - assume main repo
    # Try to find repo root (directory containing .kittify or .git)
    repo_root = None
    search_path = cwd
    for _ in range(10):  # Limit depth
        if (search_path / ".kittify").exists() or (search_path * ".git").exists():
            repo_root = search_path
            break
        if search_path.parent == search_path:
            break  # Reached filesystem root
        search_path = search_path.parent

    return CurrentContext(
        location=ExecutionContext.MAIN_REPO,
        cwd=cwd,
        repo_root=repo_root,
        worktree_name=None,
        worktree_path=None,
    )


def x_detect_execution_context__mutmut_49(cwd: Path | None = None) -> CurrentContext:
    """Detect current execution context.

    Args:
        cwd: Current working directory (defaults to Path.cwd())

    Returns:
        CurrentContext with location, paths, and worktree info

    Example:
        >>> ctx = detect_execution_context()
        >>> if ctx.location == ExecutionContext.WORKTREE:
        ...     print(f"In worktree: {ctx.worktree_name}")
    """
    if cwd is None:
        cwd = Path.cwd().resolve()
    else:
        cwd = cwd.resolve()

    # Check if .worktrees is in path
    if ".worktrees" in cwd.parts:
        # Extract worktree information
        for i, part in enumerate(cwd.parts):
            if part == ".worktrees" and i + 1 < len(cwd.parts):
                candidate_root = Path(*cwd.parts[:i])
                if (candidate_root / ".kittify").exists() or (candidate_root / ".git").exists():
                    worktree_name = cwd.parts[i + 1]
                    worktree_path = Path(*cwd.parts[: i + 2])
                    repo_root = candidate_root

                    return CurrentContext(
                        location=ExecutionContext.WORKTREE,
                        cwd=cwd,
                        repo_root=repo_root,
                        worktree_name=worktree_name,
                        worktree_path=worktree_path,
                    )

    # Not in worktree - assume main repo
    # Try to find repo root (directory containing .kittify or .git)
    repo_root = None
    search_path = cwd
    for _ in range(10):  # Limit depth
        if (search_path / ".kittify").exists() or (search_path / "XX.gitXX").exists():
            repo_root = search_path
            break
        if search_path.parent == search_path:
            break  # Reached filesystem root
        search_path = search_path.parent

    return CurrentContext(
        location=ExecutionContext.MAIN_REPO,
        cwd=cwd,
        repo_root=repo_root,
        worktree_name=None,
        worktree_path=None,
    )


def x_detect_execution_context__mutmut_50(cwd: Path | None = None) -> CurrentContext:
    """Detect current execution context.

    Args:
        cwd: Current working directory (defaults to Path.cwd())

    Returns:
        CurrentContext with location, paths, and worktree info

    Example:
        >>> ctx = detect_execution_context()
        >>> if ctx.location == ExecutionContext.WORKTREE:
        ...     print(f"In worktree: {ctx.worktree_name}")
    """
    if cwd is None:
        cwd = Path.cwd().resolve()
    else:
        cwd = cwd.resolve()

    # Check if .worktrees is in path
    if ".worktrees" in cwd.parts:
        # Extract worktree information
        for i, part in enumerate(cwd.parts):
            if part == ".worktrees" and i + 1 < len(cwd.parts):
                candidate_root = Path(*cwd.parts[:i])
                if (candidate_root / ".kittify").exists() or (candidate_root / ".git").exists():
                    worktree_name = cwd.parts[i + 1]
                    worktree_path = Path(*cwd.parts[: i + 2])
                    repo_root = candidate_root

                    return CurrentContext(
                        location=ExecutionContext.WORKTREE,
                        cwd=cwd,
                        repo_root=repo_root,
                        worktree_name=worktree_name,
                        worktree_path=worktree_path,
                    )

    # Not in worktree - assume main repo
    # Try to find repo root (directory containing .kittify or .git)
    repo_root = None
    search_path = cwd
    for _ in range(10):  # Limit depth
        if (search_path / ".kittify").exists() or (search_path / ".GIT").exists():
            repo_root = search_path
            break
        if search_path.parent == search_path:
            break  # Reached filesystem root
        search_path = search_path.parent

    return CurrentContext(
        location=ExecutionContext.MAIN_REPO,
        cwd=cwd,
        repo_root=repo_root,
        worktree_name=None,
        worktree_path=None,
    )


def x_detect_execution_context__mutmut_51(cwd: Path | None = None) -> CurrentContext:
    """Detect current execution context.

    Args:
        cwd: Current working directory (defaults to Path.cwd())

    Returns:
        CurrentContext with location, paths, and worktree info

    Example:
        >>> ctx = detect_execution_context()
        >>> if ctx.location == ExecutionContext.WORKTREE:
        ...     print(f"In worktree: {ctx.worktree_name}")
    """
    if cwd is None:
        cwd = Path.cwd().resolve()
    else:
        cwd = cwd.resolve()

    # Check if .worktrees is in path
    if ".worktrees" in cwd.parts:
        # Extract worktree information
        for i, part in enumerate(cwd.parts):
            if part == ".worktrees" and i + 1 < len(cwd.parts):
                candidate_root = Path(*cwd.parts[:i])
                if (candidate_root / ".kittify").exists() or (candidate_root / ".git").exists():
                    worktree_name = cwd.parts[i + 1]
                    worktree_path = Path(*cwd.parts[: i + 2])
                    repo_root = candidate_root

                    return CurrentContext(
                        location=ExecutionContext.WORKTREE,
                        cwd=cwd,
                        repo_root=repo_root,
                        worktree_name=worktree_name,
                        worktree_path=worktree_path,
                    )

    # Not in worktree - assume main repo
    # Try to find repo root (directory containing .kittify or .git)
    repo_root = None
    search_path = cwd
    for _ in range(10):  # Limit depth
        if (search_path / ".kittify").exists() or (search_path / ".git").exists():
            repo_root = None
            break
        if search_path.parent == search_path:
            break  # Reached filesystem root
        search_path = search_path.parent

    return CurrentContext(
        location=ExecutionContext.MAIN_REPO,
        cwd=cwd,
        repo_root=repo_root,
        worktree_name=None,
        worktree_path=None,
    )


def x_detect_execution_context__mutmut_52(cwd: Path | None = None) -> CurrentContext:
    """Detect current execution context.

    Args:
        cwd: Current working directory (defaults to Path.cwd())

    Returns:
        CurrentContext with location, paths, and worktree info

    Example:
        >>> ctx = detect_execution_context()
        >>> if ctx.location == ExecutionContext.WORKTREE:
        ...     print(f"In worktree: {ctx.worktree_name}")
    """
    if cwd is None:
        cwd = Path.cwd().resolve()
    else:
        cwd = cwd.resolve()

    # Check if .worktrees is in path
    if ".worktrees" in cwd.parts:
        # Extract worktree information
        for i, part in enumerate(cwd.parts):
            if part == ".worktrees" and i + 1 < len(cwd.parts):
                candidate_root = Path(*cwd.parts[:i])
                if (candidate_root / ".kittify").exists() or (candidate_root / ".git").exists():
                    worktree_name = cwd.parts[i + 1]
                    worktree_path = Path(*cwd.parts[: i + 2])
                    repo_root = candidate_root

                    return CurrentContext(
                        location=ExecutionContext.WORKTREE,
                        cwd=cwd,
                        repo_root=repo_root,
                        worktree_name=worktree_name,
                        worktree_path=worktree_path,
                    )

    # Not in worktree - assume main repo
    # Try to find repo root (directory containing .kittify or .git)
    repo_root = None
    search_path = cwd
    for _ in range(10):  # Limit depth
        if (search_path / ".kittify").exists() or (search_path / ".git").exists():
            repo_root = search_path
            return
        if search_path.parent == search_path:
            break  # Reached filesystem root
        search_path = search_path.parent

    return CurrentContext(
        location=ExecutionContext.MAIN_REPO,
        cwd=cwd,
        repo_root=repo_root,
        worktree_name=None,
        worktree_path=None,
    )


def x_detect_execution_context__mutmut_53(cwd: Path | None = None) -> CurrentContext:
    """Detect current execution context.

    Args:
        cwd: Current working directory (defaults to Path.cwd())

    Returns:
        CurrentContext with location, paths, and worktree info

    Example:
        >>> ctx = detect_execution_context()
        >>> if ctx.location == ExecutionContext.WORKTREE:
        ...     print(f"In worktree: {ctx.worktree_name}")
    """
    if cwd is None:
        cwd = Path.cwd().resolve()
    else:
        cwd = cwd.resolve()

    # Check if .worktrees is in path
    if ".worktrees" in cwd.parts:
        # Extract worktree information
        for i, part in enumerate(cwd.parts):
            if part == ".worktrees" and i + 1 < len(cwd.parts):
                candidate_root = Path(*cwd.parts[:i])
                if (candidate_root / ".kittify").exists() or (candidate_root / ".git").exists():
                    worktree_name = cwd.parts[i + 1]
                    worktree_path = Path(*cwd.parts[: i + 2])
                    repo_root = candidate_root

                    return CurrentContext(
                        location=ExecutionContext.WORKTREE,
                        cwd=cwd,
                        repo_root=repo_root,
                        worktree_name=worktree_name,
                        worktree_path=worktree_path,
                    )

    # Not in worktree - assume main repo
    # Try to find repo root (directory containing .kittify or .git)
    repo_root = None
    search_path = cwd
    for _ in range(10):  # Limit depth
        if (search_path / ".kittify").exists() or (search_path / ".git").exists():
            repo_root = search_path
            break
        if search_path.parent != search_path:
            break  # Reached filesystem root
        search_path = search_path.parent

    return CurrentContext(
        location=ExecutionContext.MAIN_REPO,
        cwd=cwd,
        repo_root=repo_root,
        worktree_name=None,
        worktree_path=None,
    )


def x_detect_execution_context__mutmut_54(cwd: Path | None = None) -> CurrentContext:
    """Detect current execution context.

    Args:
        cwd: Current working directory (defaults to Path.cwd())

    Returns:
        CurrentContext with location, paths, and worktree info

    Example:
        >>> ctx = detect_execution_context()
        >>> if ctx.location == ExecutionContext.WORKTREE:
        ...     print(f"In worktree: {ctx.worktree_name}")
    """
    if cwd is None:
        cwd = Path.cwd().resolve()
    else:
        cwd = cwd.resolve()

    # Check if .worktrees is in path
    if ".worktrees" in cwd.parts:
        # Extract worktree information
        for i, part in enumerate(cwd.parts):
            if part == ".worktrees" and i + 1 < len(cwd.parts):
                candidate_root = Path(*cwd.parts[:i])
                if (candidate_root / ".kittify").exists() or (candidate_root / ".git").exists():
                    worktree_name = cwd.parts[i + 1]
                    worktree_path = Path(*cwd.parts[: i + 2])
                    repo_root = candidate_root

                    return CurrentContext(
                        location=ExecutionContext.WORKTREE,
                        cwd=cwd,
                        repo_root=repo_root,
                        worktree_name=worktree_name,
                        worktree_path=worktree_path,
                    )

    # Not in worktree - assume main repo
    # Try to find repo root (directory containing .kittify or .git)
    repo_root = None
    search_path = cwd
    for _ in range(10):  # Limit depth
        if (search_path / ".kittify").exists() or (search_path / ".git").exists():
            repo_root = search_path
            break
        if search_path.parent == search_path:
            return  # Reached filesystem root
        search_path = search_path.parent

    return CurrentContext(
        location=ExecutionContext.MAIN_REPO,
        cwd=cwd,
        repo_root=repo_root,
        worktree_name=None,
        worktree_path=None,
    )


def x_detect_execution_context__mutmut_55(cwd: Path | None = None) -> CurrentContext:
    """Detect current execution context.

    Args:
        cwd: Current working directory (defaults to Path.cwd())

    Returns:
        CurrentContext with location, paths, and worktree info

    Example:
        >>> ctx = detect_execution_context()
        >>> if ctx.location == ExecutionContext.WORKTREE:
        ...     print(f"In worktree: {ctx.worktree_name}")
    """
    if cwd is None:
        cwd = Path.cwd().resolve()
    else:
        cwd = cwd.resolve()

    # Check if .worktrees is in path
    if ".worktrees" in cwd.parts:
        # Extract worktree information
        for i, part in enumerate(cwd.parts):
            if part == ".worktrees" and i + 1 < len(cwd.parts):
                candidate_root = Path(*cwd.parts[:i])
                if (candidate_root / ".kittify").exists() or (candidate_root / ".git").exists():
                    worktree_name = cwd.parts[i + 1]
                    worktree_path = Path(*cwd.parts[: i + 2])
                    repo_root = candidate_root

                    return CurrentContext(
                        location=ExecutionContext.WORKTREE,
                        cwd=cwd,
                        repo_root=repo_root,
                        worktree_name=worktree_name,
                        worktree_path=worktree_path,
                    )

    # Not in worktree - assume main repo
    # Try to find repo root (directory containing .kittify or .git)
    repo_root = None
    search_path = cwd
    for _ in range(10):  # Limit depth
        if (search_path / ".kittify").exists() or (search_path / ".git").exists():
            repo_root = search_path
            break
        if search_path.parent == search_path:
            break  # Reached filesystem root
        search_path = None

    return CurrentContext(
        location=ExecutionContext.MAIN_REPO,
        cwd=cwd,
        repo_root=repo_root,
        worktree_name=None,
        worktree_path=None,
    )


def x_detect_execution_context__mutmut_56(cwd: Path | None = None) -> CurrentContext:
    """Detect current execution context.

    Args:
        cwd: Current working directory (defaults to Path.cwd())

    Returns:
        CurrentContext with location, paths, and worktree info

    Example:
        >>> ctx = detect_execution_context()
        >>> if ctx.location == ExecutionContext.WORKTREE:
        ...     print(f"In worktree: {ctx.worktree_name}")
    """
    if cwd is None:
        cwd = Path.cwd().resolve()
    else:
        cwd = cwd.resolve()

    # Check if .worktrees is in path
    if ".worktrees" in cwd.parts:
        # Extract worktree information
        for i, part in enumerate(cwd.parts):
            if part == ".worktrees" and i + 1 < len(cwd.parts):
                candidate_root = Path(*cwd.parts[:i])
                if (candidate_root / ".kittify").exists() or (candidate_root / ".git").exists():
                    worktree_name = cwd.parts[i + 1]
                    worktree_path = Path(*cwd.parts[: i + 2])
                    repo_root = candidate_root

                    return CurrentContext(
                        location=ExecutionContext.WORKTREE,
                        cwd=cwd,
                        repo_root=repo_root,
                        worktree_name=worktree_name,
                        worktree_path=worktree_path,
                    )

    # Not in worktree - assume main repo
    # Try to find repo root (directory containing .kittify or .git)
    repo_root = None
    search_path = cwd
    for _ in range(10):  # Limit depth
        if (search_path / ".kittify").exists() or (search_path / ".git").exists():
            repo_root = search_path
            break
        if search_path.parent == search_path:
            break  # Reached filesystem root
        search_path = search_path.parent

    return CurrentContext(
        location=None,
        cwd=cwd,
        repo_root=repo_root,
        worktree_name=None,
        worktree_path=None,
    )


def x_detect_execution_context__mutmut_57(cwd: Path | None = None) -> CurrentContext:
    """Detect current execution context.

    Args:
        cwd: Current working directory (defaults to Path.cwd())

    Returns:
        CurrentContext with location, paths, and worktree info

    Example:
        >>> ctx = detect_execution_context()
        >>> if ctx.location == ExecutionContext.WORKTREE:
        ...     print(f"In worktree: {ctx.worktree_name}")
    """
    if cwd is None:
        cwd = Path.cwd().resolve()
    else:
        cwd = cwd.resolve()

    # Check if .worktrees is in path
    if ".worktrees" in cwd.parts:
        # Extract worktree information
        for i, part in enumerate(cwd.parts):
            if part == ".worktrees" and i + 1 < len(cwd.parts):
                candidate_root = Path(*cwd.parts[:i])
                if (candidate_root / ".kittify").exists() or (candidate_root / ".git").exists():
                    worktree_name = cwd.parts[i + 1]
                    worktree_path = Path(*cwd.parts[: i + 2])
                    repo_root = candidate_root

                    return CurrentContext(
                        location=ExecutionContext.WORKTREE,
                        cwd=cwd,
                        repo_root=repo_root,
                        worktree_name=worktree_name,
                        worktree_path=worktree_path,
                    )

    # Not in worktree - assume main repo
    # Try to find repo root (directory containing .kittify or .git)
    repo_root = None
    search_path = cwd
    for _ in range(10):  # Limit depth
        if (search_path / ".kittify").exists() or (search_path / ".git").exists():
            repo_root = search_path
            break
        if search_path.parent == search_path:
            break  # Reached filesystem root
        search_path = search_path.parent

    return CurrentContext(
        location=ExecutionContext.MAIN_REPO,
        cwd=None,
        repo_root=repo_root,
        worktree_name=None,
        worktree_path=None,
    )


def x_detect_execution_context__mutmut_58(cwd: Path | None = None) -> CurrentContext:
    """Detect current execution context.

    Args:
        cwd: Current working directory (defaults to Path.cwd())

    Returns:
        CurrentContext with location, paths, and worktree info

    Example:
        >>> ctx = detect_execution_context()
        >>> if ctx.location == ExecutionContext.WORKTREE:
        ...     print(f"In worktree: {ctx.worktree_name}")
    """
    if cwd is None:
        cwd = Path.cwd().resolve()
    else:
        cwd = cwd.resolve()

    # Check if .worktrees is in path
    if ".worktrees" in cwd.parts:
        # Extract worktree information
        for i, part in enumerate(cwd.parts):
            if part == ".worktrees" and i + 1 < len(cwd.parts):
                candidate_root = Path(*cwd.parts[:i])
                if (candidate_root / ".kittify").exists() or (candidate_root / ".git").exists():
                    worktree_name = cwd.parts[i + 1]
                    worktree_path = Path(*cwd.parts[: i + 2])
                    repo_root = candidate_root

                    return CurrentContext(
                        location=ExecutionContext.WORKTREE,
                        cwd=cwd,
                        repo_root=repo_root,
                        worktree_name=worktree_name,
                        worktree_path=worktree_path,
                    )

    # Not in worktree - assume main repo
    # Try to find repo root (directory containing .kittify or .git)
    repo_root = None
    search_path = cwd
    for _ in range(10):  # Limit depth
        if (search_path / ".kittify").exists() or (search_path / ".git").exists():
            repo_root = search_path
            break
        if search_path.parent == search_path:
            break  # Reached filesystem root
        search_path = search_path.parent

    return CurrentContext(
        location=ExecutionContext.MAIN_REPO,
        cwd=cwd,
        repo_root=None,
        worktree_name=None,
        worktree_path=None,
    )


def x_detect_execution_context__mutmut_59(cwd: Path | None = None) -> CurrentContext:
    """Detect current execution context.

    Args:
        cwd: Current working directory (defaults to Path.cwd())

    Returns:
        CurrentContext with location, paths, and worktree info

    Example:
        >>> ctx = detect_execution_context()
        >>> if ctx.location == ExecutionContext.WORKTREE:
        ...     print(f"In worktree: {ctx.worktree_name}")
    """
    if cwd is None:
        cwd = Path.cwd().resolve()
    else:
        cwd = cwd.resolve()

    # Check if .worktrees is in path
    if ".worktrees" in cwd.parts:
        # Extract worktree information
        for i, part in enumerate(cwd.parts):
            if part == ".worktrees" and i + 1 < len(cwd.parts):
                candidate_root = Path(*cwd.parts[:i])
                if (candidate_root / ".kittify").exists() or (candidate_root / ".git").exists():
                    worktree_name = cwd.parts[i + 1]
                    worktree_path = Path(*cwd.parts[: i + 2])
                    repo_root = candidate_root

                    return CurrentContext(
                        location=ExecutionContext.WORKTREE,
                        cwd=cwd,
                        repo_root=repo_root,
                        worktree_name=worktree_name,
                        worktree_path=worktree_path,
                    )

    # Not in worktree - assume main repo
    # Try to find repo root (directory containing .kittify or .git)
    repo_root = None
    search_path = cwd
    for _ in range(10):  # Limit depth
        if (search_path / ".kittify").exists() or (search_path / ".git").exists():
            repo_root = search_path
            break
        if search_path.parent == search_path:
            break  # Reached filesystem root
        search_path = search_path.parent

    return CurrentContext(
        cwd=cwd,
        repo_root=repo_root,
        worktree_name=None,
        worktree_path=None,
    )


def x_detect_execution_context__mutmut_60(cwd: Path | None = None) -> CurrentContext:
    """Detect current execution context.

    Args:
        cwd: Current working directory (defaults to Path.cwd())

    Returns:
        CurrentContext with location, paths, and worktree info

    Example:
        >>> ctx = detect_execution_context()
        >>> if ctx.location == ExecutionContext.WORKTREE:
        ...     print(f"In worktree: {ctx.worktree_name}")
    """
    if cwd is None:
        cwd = Path.cwd().resolve()
    else:
        cwd = cwd.resolve()

    # Check if .worktrees is in path
    if ".worktrees" in cwd.parts:
        # Extract worktree information
        for i, part in enumerate(cwd.parts):
            if part == ".worktrees" and i + 1 < len(cwd.parts):
                candidate_root = Path(*cwd.parts[:i])
                if (candidate_root / ".kittify").exists() or (candidate_root / ".git").exists():
                    worktree_name = cwd.parts[i + 1]
                    worktree_path = Path(*cwd.parts[: i + 2])
                    repo_root = candidate_root

                    return CurrentContext(
                        location=ExecutionContext.WORKTREE,
                        cwd=cwd,
                        repo_root=repo_root,
                        worktree_name=worktree_name,
                        worktree_path=worktree_path,
                    )

    # Not in worktree - assume main repo
    # Try to find repo root (directory containing .kittify or .git)
    repo_root = None
    search_path = cwd
    for _ in range(10):  # Limit depth
        if (search_path / ".kittify").exists() or (search_path / ".git").exists():
            repo_root = search_path
            break
        if search_path.parent == search_path:
            break  # Reached filesystem root
        search_path = search_path.parent

    return CurrentContext(
        location=ExecutionContext.MAIN_REPO,
        repo_root=repo_root,
        worktree_name=None,
        worktree_path=None,
    )


def x_detect_execution_context__mutmut_61(cwd: Path | None = None) -> CurrentContext:
    """Detect current execution context.

    Args:
        cwd: Current working directory (defaults to Path.cwd())

    Returns:
        CurrentContext with location, paths, and worktree info

    Example:
        >>> ctx = detect_execution_context()
        >>> if ctx.location == ExecutionContext.WORKTREE:
        ...     print(f"In worktree: {ctx.worktree_name}")
    """
    if cwd is None:
        cwd = Path.cwd().resolve()
    else:
        cwd = cwd.resolve()

    # Check if .worktrees is in path
    if ".worktrees" in cwd.parts:
        # Extract worktree information
        for i, part in enumerate(cwd.parts):
            if part == ".worktrees" and i + 1 < len(cwd.parts):
                candidate_root = Path(*cwd.parts[:i])
                if (candidate_root / ".kittify").exists() or (candidate_root / ".git").exists():
                    worktree_name = cwd.parts[i + 1]
                    worktree_path = Path(*cwd.parts[: i + 2])
                    repo_root = candidate_root

                    return CurrentContext(
                        location=ExecutionContext.WORKTREE,
                        cwd=cwd,
                        repo_root=repo_root,
                        worktree_name=worktree_name,
                        worktree_path=worktree_path,
                    )

    # Not in worktree - assume main repo
    # Try to find repo root (directory containing .kittify or .git)
    repo_root = None
    search_path = cwd
    for _ in range(10):  # Limit depth
        if (search_path / ".kittify").exists() or (search_path / ".git").exists():
            repo_root = search_path
            break
        if search_path.parent == search_path:
            break  # Reached filesystem root
        search_path = search_path.parent

    return CurrentContext(
        location=ExecutionContext.MAIN_REPO,
        cwd=cwd,
        worktree_name=None,
        worktree_path=None,
    )


def x_detect_execution_context__mutmut_62(cwd: Path | None = None) -> CurrentContext:
    """Detect current execution context.

    Args:
        cwd: Current working directory (defaults to Path.cwd())

    Returns:
        CurrentContext with location, paths, and worktree info

    Example:
        >>> ctx = detect_execution_context()
        >>> if ctx.location == ExecutionContext.WORKTREE:
        ...     print(f"In worktree: {ctx.worktree_name}")
    """
    if cwd is None:
        cwd = Path.cwd().resolve()
    else:
        cwd = cwd.resolve()

    # Check if .worktrees is in path
    if ".worktrees" in cwd.parts:
        # Extract worktree information
        for i, part in enumerate(cwd.parts):
            if part == ".worktrees" and i + 1 < len(cwd.parts):
                candidate_root = Path(*cwd.parts[:i])
                if (candidate_root / ".kittify").exists() or (candidate_root / ".git").exists():
                    worktree_name = cwd.parts[i + 1]
                    worktree_path = Path(*cwd.parts[: i + 2])
                    repo_root = candidate_root

                    return CurrentContext(
                        location=ExecutionContext.WORKTREE,
                        cwd=cwd,
                        repo_root=repo_root,
                        worktree_name=worktree_name,
                        worktree_path=worktree_path,
                    )

    # Not in worktree - assume main repo
    # Try to find repo root (directory containing .kittify or .git)
    repo_root = None
    search_path = cwd
    for _ in range(10):  # Limit depth
        if (search_path / ".kittify").exists() or (search_path / ".git").exists():
            repo_root = search_path
            break
        if search_path.parent == search_path:
            break  # Reached filesystem root
        search_path = search_path.parent

    return CurrentContext(
        location=ExecutionContext.MAIN_REPO,
        cwd=cwd,
        repo_root=repo_root,
        worktree_path=None,
    )


def x_detect_execution_context__mutmut_63(cwd: Path | None = None) -> CurrentContext:
    """Detect current execution context.

    Args:
        cwd: Current working directory (defaults to Path.cwd())

    Returns:
        CurrentContext with location, paths, and worktree info

    Example:
        >>> ctx = detect_execution_context()
        >>> if ctx.location == ExecutionContext.WORKTREE:
        ...     print(f"In worktree: {ctx.worktree_name}")
    """
    if cwd is None:
        cwd = Path.cwd().resolve()
    else:
        cwd = cwd.resolve()

    # Check if .worktrees is in path
    if ".worktrees" in cwd.parts:
        # Extract worktree information
        for i, part in enumerate(cwd.parts):
            if part == ".worktrees" and i + 1 < len(cwd.parts):
                candidate_root = Path(*cwd.parts[:i])
                if (candidate_root / ".kittify").exists() or (candidate_root / ".git").exists():
                    worktree_name = cwd.parts[i + 1]
                    worktree_path = Path(*cwd.parts[: i + 2])
                    repo_root = candidate_root

                    return CurrentContext(
                        location=ExecutionContext.WORKTREE,
                        cwd=cwd,
                        repo_root=repo_root,
                        worktree_name=worktree_name,
                        worktree_path=worktree_path,
                    )

    # Not in worktree - assume main repo
    # Try to find repo root (directory containing .kittify or .git)
    repo_root = None
    search_path = cwd
    for _ in range(10):  # Limit depth
        if (search_path / ".kittify").exists() or (search_path / ".git").exists():
            repo_root = search_path
            break
        if search_path.parent == search_path:
            break  # Reached filesystem root
        search_path = search_path.parent

    return CurrentContext(
        location=ExecutionContext.MAIN_REPO,
        cwd=cwd,
        repo_root=repo_root,
        worktree_name=None,
        )

x_detect_execution_context__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_detect_execution_context__mutmut_1': x_detect_execution_context__mutmut_1, 
    'x_detect_execution_context__mutmut_2': x_detect_execution_context__mutmut_2, 
    'x_detect_execution_context__mutmut_3': x_detect_execution_context__mutmut_3, 
    'x_detect_execution_context__mutmut_4': x_detect_execution_context__mutmut_4, 
    'x_detect_execution_context__mutmut_5': x_detect_execution_context__mutmut_5, 
    'x_detect_execution_context__mutmut_6': x_detect_execution_context__mutmut_6, 
    'x_detect_execution_context__mutmut_7': x_detect_execution_context__mutmut_7, 
    'x_detect_execution_context__mutmut_8': x_detect_execution_context__mutmut_8, 
    'x_detect_execution_context__mutmut_9': x_detect_execution_context__mutmut_9, 
    'x_detect_execution_context__mutmut_10': x_detect_execution_context__mutmut_10, 
    'x_detect_execution_context__mutmut_11': x_detect_execution_context__mutmut_11, 
    'x_detect_execution_context__mutmut_12': x_detect_execution_context__mutmut_12, 
    'x_detect_execution_context__mutmut_13': x_detect_execution_context__mutmut_13, 
    'x_detect_execution_context__mutmut_14': x_detect_execution_context__mutmut_14, 
    'x_detect_execution_context__mutmut_15': x_detect_execution_context__mutmut_15, 
    'x_detect_execution_context__mutmut_16': x_detect_execution_context__mutmut_16, 
    'x_detect_execution_context__mutmut_17': x_detect_execution_context__mutmut_17, 
    'x_detect_execution_context__mutmut_18': x_detect_execution_context__mutmut_18, 
    'x_detect_execution_context__mutmut_19': x_detect_execution_context__mutmut_19, 
    'x_detect_execution_context__mutmut_20': x_detect_execution_context__mutmut_20, 
    'x_detect_execution_context__mutmut_21': x_detect_execution_context__mutmut_21, 
    'x_detect_execution_context__mutmut_22': x_detect_execution_context__mutmut_22, 
    'x_detect_execution_context__mutmut_23': x_detect_execution_context__mutmut_23, 
    'x_detect_execution_context__mutmut_24': x_detect_execution_context__mutmut_24, 
    'x_detect_execution_context__mutmut_25': x_detect_execution_context__mutmut_25, 
    'x_detect_execution_context__mutmut_26': x_detect_execution_context__mutmut_26, 
    'x_detect_execution_context__mutmut_27': x_detect_execution_context__mutmut_27, 
    'x_detect_execution_context__mutmut_28': x_detect_execution_context__mutmut_28, 
    'x_detect_execution_context__mutmut_29': x_detect_execution_context__mutmut_29, 
    'x_detect_execution_context__mutmut_30': x_detect_execution_context__mutmut_30, 
    'x_detect_execution_context__mutmut_31': x_detect_execution_context__mutmut_31, 
    'x_detect_execution_context__mutmut_32': x_detect_execution_context__mutmut_32, 
    'x_detect_execution_context__mutmut_33': x_detect_execution_context__mutmut_33, 
    'x_detect_execution_context__mutmut_34': x_detect_execution_context__mutmut_34, 
    'x_detect_execution_context__mutmut_35': x_detect_execution_context__mutmut_35, 
    'x_detect_execution_context__mutmut_36': x_detect_execution_context__mutmut_36, 
    'x_detect_execution_context__mutmut_37': x_detect_execution_context__mutmut_37, 
    'x_detect_execution_context__mutmut_38': x_detect_execution_context__mutmut_38, 
    'x_detect_execution_context__mutmut_39': x_detect_execution_context__mutmut_39, 
    'x_detect_execution_context__mutmut_40': x_detect_execution_context__mutmut_40, 
    'x_detect_execution_context__mutmut_41': x_detect_execution_context__mutmut_41, 
    'x_detect_execution_context__mutmut_42': x_detect_execution_context__mutmut_42, 
    'x_detect_execution_context__mutmut_43': x_detect_execution_context__mutmut_43, 
    'x_detect_execution_context__mutmut_44': x_detect_execution_context__mutmut_44, 
    'x_detect_execution_context__mutmut_45': x_detect_execution_context__mutmut_45, 
    'x_detect_execution_context__mutmut_46': x_detect_execution_context__mutmut_46, 
    'x_detect_execution_context__mutmut_47': x_detect_execution_context__mutmut_47, 
    'x_detect_execution_context__mutmut_48': x_detect_execution_context__mutmut_48, 
    'x_detect_execution_context__mutmut_49': x_detect_execution_context__mutmut_49, 
    'x_detect_execution_context__mutmut_50': x_detect_execution_context__mutmut_50, 
    'x_detect_execution_context__mutmut_51': x_detect_execution_context__mutmut_51, 
    'x_detect_execution_context__mutmut_52': x_detect_execution_context__mutmut_52, 
    'x_detect_execution_context__mutmut_53': x_detect_execution_context__mutmut_53, 
    'x_detect_execution_context__mutmut_54': x_detect_execution_context__mutmut_54, 
    'x_detect_execution_context__mutmut_55': x_detect_execution_context__mutmut_55, 
    'x_detect_execution_context__mutmut_56': x_detect_execution_context__mutmut_56, 
    'x_detect_execution_context__mutmut_57': x_detect_execution_context__mutmut_57, 
    'x_detect_execution_context__mutmut_58': x_detect_execution_context__mutmut_58, 
    'x_detect_execution_context__mutmut_59': x_detect_execution_context__mutmut_59, 
    'x_detect_execution_context__mutmut_60': x_detect_execution_context__mutmut_60, 
    'x_detect_execution_context__mutmut_61': x_detect_execution_context__mutmut_61, 
    'x_detect_execution_context__mutmut_62': x_detect_execution_context__mutmut_62, 
    'x_detect_execution_context__mutmut_63': x_detect_execution_context__mutmut_63
}
x_detect_execution_context__mutmut_orig.__name__ = 'x_detect_execution_context'


def get_current_context() -> CurrentContext:
    """Get current execution context.

    Convenience function that detects context from current working directory.

    Returns:
        CurrentContext with location and path information
    """
    return detect_execution_context()


def format_location_error(
    required: ExecutionContext,
    actual: ExecutionContext,
    command_name: str,
    current_ctx: CurrentContext,
) -> str:
    args = [required, actual, command_name, current_ctx]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_format_location_error__mutmut_orig, x_format_location_error__mutmut_mutants, args, kwargs, None)


def x_format_location_error__mutmut_orig(
    required: ExecutionContext,
    actual: ExecutionContext,
    command_name: str,
    current_ctx: CurrentContext,
) -> str:
    """Format a clear error message for location mismatch.

    Args:
        required: Required execution context
        actual: Actual execution context
        command_name: Name of command being run
        current_ctx: Current context information

    Returns:
        Formatted error message with actionable instructions
    """
    if required == ExecutionContext.MAIN_REPO and actual == ExecutionContext.WORKTREE:
        # Command needs main repo, but in worktree
        if current_ctx.repo_root:
            return (
                f"[bold red]Error:[/bold red] '{command_name}' must run from the main repository\n\n"
                f"[yellow]Current location:[/yellow] Inside worktree [cyan]{current_ctx.worktree_name}[/cyan]\n"
                f"[yellow]Required location:[/yellow] Main repository\n\n"
                f"[bold]Change to main repository:[/bold]\n"
                f"  cd {current_ctx.repo_root}\n\n"
                f"[dim]This command creates/manages worktrees and must run from the main repository.\n"
                f"Running from inside a worktree would create nested worktrees, corrupting git state.[/dim]"
            )
        else:
            return (
                f"[bold red]Error:[/bold red] '{command_name}' must run from the main repository\n\n"
                f"[yellow]Current location:[/yellow] Inside worktree [cyan]{current_ctx.worktree_name}[/cyan]\n"
                f"[yellow]Required location:[/yellow] Main repository\n\n"
                f"[bold]Change to main repository:[/bold]\n"
                f"  cd ../..  # Navigate up from worktree\n\n"
                f"[dim]This command must run from the main repository.[/dim]"
            )

    elif required == ExecutionContext.WORKTREE and actual == ExecutionContext.MAIN_REPO:
        # Command needs worktree, but in main repo
        return (
            f"[bold red]Error:[/bold red] '{command_name}' must run from inside a worktree\n\n"
            f"[yellow]Current location:[/yellow] Main repository\n"
            f"[yellow]Required location:[/yellow] Inside a worktree\n\n"
            f"[bold]Change to a worktree:[/bold]\n"
            f"  cd .worktrees/###-feature-WP##/\n\n"
            f"[dim]This command operates on workspace files and must run from inside a worktree.[/dim]"
        )

    else:
        # Generic error
        return (
            f"[bold red]Error:[/bold red] '{command_name}' cannot run in current location\n\n"
            f"[yellow]Current location:[/yellow] {actual.value}\n"
            f"[yellow]Required location:[/yellow] {required.value}\n"
        )


def x_format_location_error__mutmut_1(
    required: ExecutionContext,
    actual: ExecutionContext,
    command_name: str,
    current_ctx: CurrentContext,
) -> str:
    """Format a clear error message for location mismatch.

    Args:
        required: Required execution context
        actual: Actual execution context
        command_name: Name of command being run
        current_ctx: Current context information

    Returns:
        Formatted error message with actionable instructions
    """
    if required == ExecutionContext.MAIN_REPO or actual == ExecutionContext.WORKTREE:
        # Command needs main repo, but in worktree
        if current_ctx.repo_root:
            return (
                f"[bold red]Error:[/bold red] '{command_name}' must run from the main repository\n\n"
                f"[yellow]Current location:[/yellow] Inside worktree [cyan]{current_ctx.worktree_name}[/cyan]\n"
                f"[yellow]Required location:[/yellow] Main repository\n\n"
                f"[bold]Change to main repository:[/bold]\n"
                f"  cd {current_ctx.repo_root}\n\n"
                f"[dim]This command creates/manages worktrees and must run from the main repository.\n"
                f"Running from inside a worktree would create nested worktrees, corrupting git state.[/dim]"
            )
        else:
            return (
                f"[bold red]Error:[/bold red] '{command_name}' must run from the main repository\n\n"
                f"[yellow]Current location:[/yellow] Inside worktree [cyan]{current_ctx.worktree_name}[/cyan]\n"
                f"[yellow]Required location:[/yellow] Main repository\n\n"
                f"[bold]Change to main repository:[/bold]\n"
                f"  cd ../..  # Navigate up from worktree\n\n"
                f"[dim]This command must run from the main repository.[/dim]"
            )

    elif required == ExecutionContext.WORKTREE and actual == ExecutionContext.MAIN_REPO:
        # Command needs worktree, but in main repo
        return (
            f"[bold red]Error:[/bold red] '{command_name}' must run from inside a worktree\n\n"
            f"[yellow]Current location:[/yellow] Main repository\n"
            f"[yellow]Required location:[/yellow] Inside a worktree\n\n"
            f"[bold]Change to a worktree:[/bold]\n"
            f"  cd .worktrees/###-feature-WP##/\n\n"
            f"[dim]This command operates on workspace files and must run from inside a worktree.[/dim]"
        )

    else:
        # Generic error
        return (
            f"[bold red]Error:[/bold red] '{command_name}' cannot run in current location\n\n"
            f"[yellow]Current location:[/yellow] {actual.value}\n"
            f"[yellow]Required location:[/yellow] {required.value}\n"
        )


def x_format_location_error__mutmut_2(
    required: ExecutionContext,
    actual: ExecutionContext,
    command_name: str,
    current_ctx: CurrentContext,
) -> str:
    """Format a clear error message for location mismatch.

    Args:
        required: Required execution context
        actual: Actual execution context
        command_name: Name of command being run
        current_ctx: Current context information

    Returns:
        Formatted error message with actionable instructions
    """
    if required != ExecutionContext.MAIN_REPO and actual == ExecutionContext.WORKTREE:
        # Command needs main repo, but in worktree
        if current_ctx.repo_root:
            return (
                f"[bold red]Error:[/bold red] '{command_name}' must run from the main repository\n\n"
                f"[yellow]Current location:[/yellow] Inside worktree [cyan]{current_ctx.worktree_name}[/cyan]\n"
                f"[yellow]Required location:[/yellow] Main repository\n\n"
                f"[bold]Change to main repository:[/bold]\n"
                f"  cd {current_ctx.repo_root}\n\n"
                f"[dim]This command creates/manages worktrees and must run from the main repository.\n"
                f"Running from inside a worktree would create nested worktrees, corrupting git state.[/dim]"
            )
        else:
            return (
                f"[bold red]Error:[/bold red] '{command_name}' must run from the main repository\n\n"
                f"[yellow]Current location:[/yellow] Inside worktree [cyan]{current_ctx.worktree_name}[/cyan]\n"
                f"[yellow]Required location:[/yellow] Main repository\n\n"
                f"[bold]Change to main repository:[/bold]\n"
                f"  cd ../..  # Navigate up from worktree\n\n"
                f"[dim]This command must run from the main repository.[/dim]"
            )

    elif required == ExecutionContext.WORKTREE and actual == ExecutionContext.MAIN_REPO:
        # Command needs worktree, but in main repo
        return (
            f"[bold red]Error:[/bold red] '{command_name}' must run from inside a worktree\n\n"
            f"[yellow]Current location:[/yellow] Main repository\n"
            f"[yellow]Required location:[/yellow] Inside a worktree\n\n"
            f"[bold]Change to a worktree:[/bold]\n"
            f"  cd .worktrees/###-feature-WP##/\n\n"
            f"[dim]This command operates on workspace files and must run from inside a worktree.[/dim]"
        )

    else:
        # Generic error
        return (
            f"[bold red]Error:[/bold red] '{command_name}' cannot run in current location\n\n"
            f"[yellow]Current location:[/yellow] {actual.value}\n"
            f"[yellow]Required location:[/yellow] {required.value}\n"
        )


def x_format_location_error__mutmut_3(
    required: ExecutionContext,
    actual: ExecutionContext,
    command_name: str,
    current_ctx: CurrentContext,
) -> str:
    """Format a clear error message for location mismatch.

    Args:
        required: Required execution context
        actual: Actual execution context
        command_name: Name of command being run
        current_ctx: Current context information

    Returns:
        Formatted error message with actionable instructions
    """
    if required == ExecutionContext.MAIN_REPO and actual != ExecutionContext.WORKTREE:
        # Command needs main repo, but in worktree
        if current_ctx.repo_root:
            return (
                f"[bold red]Error:[/bold red] '{command_name}' must run from the main repository\n\n"
                f"[yellow]Current location:[/yellow] Inside worktree [cyan]{current_ctx.worktree_name}[/cyan]\n"
                f"[yellow]Required location:[/yellow] Main repository\n\n"
                f"[bold]Change to main repository:[/bold]\n"
                f"  cd {current_ctx.repo_root}\n\n"
                f"[dim]This command creates/manages worktrees and must run from the main repository.\n"
                f"Running from inside a worktree would create nested worktrees, corrupting git state.[/dim]"
            )
        else:
            return (
                f"[bold red]Error:[/bold red] '{command_name}' must run from the main repository\n\n"
                f"[yellow]Current location:[/yellow] Inside worktree [cyan]{current_ctx.worktree_name}[/cyan]\n"
                f"[yellow]Required location:[/yellow] Main repository\n\n"
                f"[bold]Change to main repository:[/bold]\n"
                f"  cd ../..  # Navigate up from worktree\n\n"
                f"[dim]This command must run from the main repository.[/dim]"
            )

    elif required == ExecutionContext.WORKTREE and actual == ExecutionContext.MAIN_REPO:
        # Command needs worktree, but in main repo
        return (
            f"[bold red]Error:[/bold red] '{command_name}' must run from inside a worktree\n\n"
            f"[yellow]Current location:[/yellow] Main repository\n"
            f"[yellow]Required location:[/yellow] Inside a worktree\n\n"
            f"[bold]Change to a worktree:[/bold]\n"
            f"  cd .worktrees/###-feature-WP##/\n\n"
            f"[dim]This command operates on workspace files and must run from inside a worktree.[/dim]"
        )

    else:
        # Generic error
        return (
            f"[bold red]Error:[/bold red] '{command_name}' cannot run in current location\n\n"
            f"[yellow]Current location:[/yellow] {actual.value}\n"
            f"[yellow]Required location:[/yellow] {required.value}\n"
        )


def x_format_location_error__mutmut_4(
    required: ExecutionContext,
    actual: ExecutionContext,
    command_name: str,
    current_ctx: CurrentContext,
) -> str:
    """Format a clear error message for location mismatch.

    Args:
        required: Required execution context
        actual: Actual execution context
        command_name: Name of command being run
        current_ctx: Current context information

    Returns:
        Formatted error message with actionable instructions
    """
    if required == ExecutionContext.MAIN_REPO and actual == ExecutionContext.WORKTREE:
        # Command needs main repo, but in worktree
        if current_ctx.repo_root:
            return (
                f"[bold red]Error:[/bold red] '{command_name}' must run from the main repository\n\n"
                f"[yellow]Current location:[/yellow] Inside worktree [cyan]{current_ctx.worktree_name}[/cyan]\n"
                f"[yellow]Required location:[/yellow] Main repository\n\n"
                f"[bold]Change to main repository:[/bold]\n"
                f"  cd {current_ctx.repo_root}\n\n"
                f"[dim]This command creates/manages worktrees and must run from the main repository.\n"
                f"Running from inside a worktree would create nested worktrees, corrupting git state.[/dim]"
            )
        else:
            return (
                f"[bold red]Error:[/bold red] '{command_name}' must run from the main repository\n\n"
                f"[yellow]Current location:[/yellow] Inside worktree [cyan]{current_ctx.worktree_name}[/cyan]\n"
                f"[yellow]Required location:[/yellow] Main repository\n\n"
                f"[bold]Change to main repository:[/bold]\n"
                f"  cd ../..  # Navigate up from worktree\n\n"
                f"[dim]This command must run from the main repository.[/dim]"
            )

    elif required == ExecutionContext.WORKTREE or actual == ExecutionContext.MAIN_REPO:
        # Command needs worktree, but in main repo
        return (
            f"[bold red]Error:[/bold red] '{command_name}' must run from inside a worktree\n\n"
            f"[yellow]Current location:[/yellow] Main repository\n"
            f"[yellow]Required location:[/yellow] Inside a worktree\n\n"
            f"[bold]Change to a worktree:[/bold]\n"
            f"  cd .worktrees/###-feature-WP##/\n\n"
            f"[dim]This command operates on workspace files and must run from inside a worktree.[/dim]"
        )

    else:
        # Generic error
        return (
            f"[bold red]Error:[/bold red] '{command_name}' cannot run in current location\n\n"
            f"[yellow]Current location:[/yellow] {actual.value}\n"
            f"[yellow]Required location:[/yellow] {required.value}\n"
        )


def x_format_location_error__mutmut_5(
    required: ExecutionContext,
    actual: ExecutionContext,
    command_name: str,
    current_ctx: CurrentContext,
) -> str:
    """Format a clear error message for location mismatch.

    Args:
        required: Required execution context
        actual: Actual execution context
        command_name: Name of command being run
        current_ctx: Current context information

    Returns:
        Formatted error message with actionable instructions
    """
    if required == ExecutionContext.MAIN_REPO and actual == ExecutionContext.WORKTREE:
        # Command needs main repo, but in worktree
        if current_ctx.repo_root:
            return (
                f"[bold red]Error:[/bold red] '{command_name}' must run from the main repository\n\n"
                f"[yellow]Current location:[/yellow] Inside worktree [cyan]{current_ctx.worktree_name}[/cyan]\n"
                f"[yellow]Required location:[/yellow] Main repository\n\n"
                f"[bold]Change to main repository:[/bold]\n"
                f"  cd {current_ctx.repo_root}\n\n"
                f"[dim]This command creates/manages worktrees and must run from the main repository.\n"
                f"Running from inside a worktree would create nested worktrees, corrupting git state.[/dim]"
            )
        else:
            return (
                f"[bold red]Error:[/bold red] '{command_name}' must run from the main repository\n\n"
                f"[yellow]Current location:[/yellow] Inside worktree [cyan]{current_ctx.worktree_name}[/cyan]\n"
                f"[yellow]Required location:[/yellow] Main repository\n\n"
                f"[bold]Change to main repository:[/bold]\n"
                f"  cd ../..  # Navigate up from worktree\n\n"
                f"[dim]This command must run from the main repository.[/dim]"
            )

    elif required != ExecutionContext.WORKTREE and actual == ExecutionContext.MAIN_REPO:
        # Command needs worktree, but in main repo
        return (
            f"[bold red]Error:[/bold red] '{command_name}' must run from inside a worktree\n\n"
            f"[yellow]Current location:[/yellow] Main repository\n"
            f"[yellow]Required location:[/yellow] Inside a worktree\n\n"
            f"[bold]Change to a worktree:[/bold]\n"
            f"  cd .worktrees/###-feature-WP##/\n\n"
            f"[dim]This command operates on workspace files and must run from inside a worktree.[/dim]"
        )

    else:
        # Generic error
        return (
            f"[bold red]Error:[/bold red] '{command_name}' cannot run in current location\n\n"
            f"[yellow]Current location:[/yellow] {actual.value}\n"
            f"[yellow]Required location:[/yellow] {required.value}\n"
        )


def x_format_location_error__mutmut_6(
    required: ExecutionContext,
    actual: ExecutionContext,
    command_name: str,
    current_ctx: CurrentContext,
) -> str:
    """Format a clear error message for location mismatch.

    Args:
        required: Required execution context
        actual: Actual execution context
        command_name: Name of command being run
        current_ctx: Current context information

    Returns:
        Formatted error message with actionable instructions
    """
    if required == ExecutionContext.MAIN_REPO and actual == ExecutionContext.WORKTREE:
        # Command needs main repo, but in worktree
        if current_ctx.repo_root:
            return (
                f"[bold red]Error:[/bold red] '{command_name}' must run from the main repository\n\n"
                f"[yellow]Current location:[/yellow] Inside worktree [cyan]{current_ctx.worktree_name}[/cyan]\n"
                f"[yellow]Required location:[/yellow] Main repository\n\n"
                f"[bold]Change to main repository:[/bold]\n"
                f"  cd {current_ctx.repo_root}\n\n"
                f"[dim]This command creates/manages worktrees and must run from the main repository.\n"
                f"Running from inside a worktree would create nested worktrees, corrupting git state.[/dim]"
            )
        else:
            return (
                f"[bold red]Error:[/bold red] '{command_name}' must run from the main repository\n\n"
                f"[yellow]Current location:[/yellow] Inside worktree [cyan]{current_ctx.worktree_name}[/cyan]\n"
                f"[yellow]Required location:[/yellow] Main repository\n\n"
                f"[bold]Change to main repository:[/bold]\n"
                f"  cd ../..  # Navigate up from worktree\n\n"
                f"[dim]This command must run from the main repository.[/dim]"
            )

    elif required == ExecutionContext.WORKTREE and actual != ExecutionContext.MAIN_REPO:
        # Command needs worktree, but in main repo
        return (
            f"[bold red]Error:[/bold red] '{command_name}' must run from inside a worktree\n\n"
            f"[yellow]Current location:[/yellow] Main repository\n"
            f"[yellow]Required location:[/yellow] Inside a worktree\n\n"
            f"[bold]Change to a worktree:[/bold]\n"
            f"  cd .worktrees/###-feature-WP##/\n\n"
            f"[dim]This command operates on workspace files and must run from inside a worktree.[/dim]"
        )

    else:
        # Generic error
        return (
            f"[bold red]Error:[/bold red] '{command_name}' cannot run in current location\n\n"
            f"[yellow]Current location:[/yellow] {actual.value}\n"
            f"[yellow]Required location:[/yellow] {required.value}\n"
        )

x_format_location_error__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_format_location_error__mutmut_1': x_format_location_error__mutmut_1, 
    'x_format_location_error__mutmut_2': x_format_location_error__mutmut_2, 
    'x_format_location_error__mutmut_3': x_format_location_error__mutmut_3, 
    'x_format_location_error__mutmut_4': x_format_location_error__mutmut_4, 
    'x_format_location_error__mutmut_5': x_format_location_error__mutmut_5, 
    'x_format_location_error__mutmut_6': x_format_location_error__mutmut_6
}
x_format_location_error__mutmut_orig.__name__ = 'x_format_location_error'


# Type variable for function decoration
F = TypeVar("F", bound=Callable)


def require_main_repo(func: F) -> F:
    """Decorator to require command runs from main repository.

    Prevents commands from running inside worktrees, which could cause
    nested worktrees or other git corruption.

    Example:
        @require_main_repo
        def implement(wp_id: str):
            # Can only run from main repo
            create_worktree(...)

    Args:
        func: Function to decorate

    Returns:
        Decorated function that validates location before executing
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        ctx = get_current_context()

        if ctx.location == ExecutionContext.WORKTREE:
            error_msg = format_location_error(
                required=ExecutionContext.MAIN_REPO,
                actual=ctx.location,
                command_name=func.__name__,
                current_ctx=ctx,
            )
            console.print(error_msg)
            raise typer.Exit(1)

        return func(*args, **kwargs)

    return wrapper  # type: ignore


def require_worktree(func: F) -> F:
    """Decorator to require command runs from inside a worktree.

    Prevents commands from running in main repo when they need workspace context.

    Example:
        @require_worktree
        def workspace_status():
            # Can only run from inside worktree
            show_workspace_info(...)

    Args:
        func: Function to decorate

    Returns:
        Decorated function that validates location before executing
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        ctx = get_current_context()

        if ctx.location == ExecutionContext.MAIN_REPO:
            error_msg = format_location_error(
                required=ExecutionContext.WORKTREE,
                actual=ctx.location,
                command_name=func.__name__,
                current_ctx=ctx,
            )
            console.print(error_msg)
            raise typer.Exit(1)

        return func(*args, **kwargs)

    return wrapper  # type: ignore


def require_either(func: F) -> F:
    """Decorator for commands that can run in either location.

    This is primarily for documentation - the decorator doesn't enforce
    anything, just marks the function as location-agnostic.

    Example:
        @require_either
        def status():
            # Can run from main repo or worktree
            ctx = get_current_context()
            if ctx.location == ExecutionContext.WORKTREE:
                show_worktree_status()
            else:
                show_main_repo_status()

    Args:
        func: Function to decorate

    Returns:
        Original function (no validation added)
    """
    return func


def set_context_env_vars(ctx: CurrentContext) -> None:
    args = [ctx]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_set_context_env_vars__mutmut_orig, x_set_context_env_vars__mutmut_mutants, args, kwargs, None)


def x_set_context_env_vars__mutmut_orig(ctx: CurrentContext) -> None:
    """Set environment variables for current context.

    Makes context information available to subprocesses and scripts.

    Environment variables set:
        SPEC_KITTY_CONTEXT: "main" or "worktree"
        SPEC_KITTY_CWD: Current working directory
        SPEC_KITTY_REPO_ROOT: Repository root (if detected)
        SPEC_KITTY_WORKTREE_NAME: Worktree name (if in worktree)
        SPEC_KITTY_WORKTREE_PATH: Worktree path (if in worktree)

    Args:
        ctx: Current context information

    Example:
        >>> ctx = get_current_context()
        >>> set_context_env_vars(ctx)
        >>> print(os.environ.get("SPEC_KITTY_CONTEXT"))
        "main"
    """
    os.environ["SPEC_KITTY_CONTEXT"] = ctx.location.value
    os.environ["SPEC_KITTY_CWD"] = str(ctx.cwd)

    if ctx.repo_root:
        os.environ["SPEC_KITTY_REPO_ROOT"] = str(ctx.repo_root)
    else:
        os.environ.pop("SPEC_KITTY_REPO_ROOT", None)

    if ctx.worktree_name:
        os.environ["SPEC_KITTY_WORKTREE_NAME"] = ctx.worktree_name
    else:
        os.environ.pop("SPEC_KITTY_WORKTREE_NAME", None)

    if ctx.worktree_path:
        os.environ["SPEC_KITTY_WORKTREE_PATH"] = str(ctx.worktree_path)
    else:
        os.environ.pop("SPEC_KITTY_WORKTREE_PATH", None)


def x_set_context_env_vars__mutmut_1(ctx: CurrentContext) -> None:
    """Set environment variables for current context.

    Makes context information available to subprocesses and scripts.

    Environment variables set:
        SPEC_KITTY_CONTEXT: "main" or "worktree"
        SPEC_KITTY_CWD: Current working directory
        SPEC_KITTY_REPO_ROOT: Repository root (if detected)
        SPEC_KITTY_WORKTREE_NAME: Worktree name (if in worktree)
        SPEC_KITTY_WORKTREE_PATH: Worktree path (if in worktree)

    Args:
        ctx: Current context information

    Example:
        >>> ctx = get_current_context()
        >>> set_context_env_vars(ctx)
        >>> print(os.environ.get("SPEC_KITTY_CONTEXT"))
        "main"
    """
    os.environ["SPEC_KITTY_CONTEXT"] = None
    os.environ["SPEC_KITTY_CWD"] = str(ctx.cwd)

    if ctx.repo_root:
        os.environ["SPEC_KITTY_REPO_ROOT"] = str(ctx.repo_root)
    else:
        os.environ.pop("SPEC_KITTY_REPO_ROOT", None)

    if ctx.worktree_name:
        os.environ["SPEC_KITTY_WORKTREE_NAME"] = ctx.worktree_name
    else:
        os.environ.pop("SPEC_KITTY_WORKTREE_NAME", None)

    if ctx.worktree_path:
        os.environ["SPEC_KITTY_WORKTREE_PATH"] = str(ctx.worktree_path)
    else:
        os.environ.pop("SPEC_KITTY_WORKTREE_PATH", None)


def x_set_context_env_vars__mutmut_2(ctx: CurrentContext) -> None:
    """Set environment variables for current context.

    Makes context information available to subprocesses and scripts.

    Environment variables set:
        SPEC_KITTY_CONTEXT: "main" or "worktree"
        SPEC_KITTY_CWD: Current working directory
        SPEC_KITTY_REPO_ROOT: Repository root (if detected)
        SPEC_KITTY_WORKTREE_NAME: Worktree name (if in worktree)
        SPEC_KITTY_WORKTREE_PATH: Worktree path (if in worktree)

    Args:
        ctx: Current context information

    Example:
        >>> ctx = get_current_context()
        >>> set_context_env_vars(ctx)
        >>> print(os.environ.get("SPEC_KITTY_CONTEXT"))
        "main"
    """
    os.environ["XXSPEC_KITTY_CONTEXTXX"] = ctx.location.value
    os.environ["SPEC_KITTY_CWD"] = str(ctx.cwd)

    if ctx.repo_root:
        os.environ["SPEC_KITTY_REPO_ROOT"] = str(ctx.repo_root)
    else:
        os.environ.pop("SPEC_KITTY_REPO_ROOT", None)

    if ctx.worktree_name:
        os.environ["SPEC_KITTY_WORKTREE_NAME"] = ctx.worktree_name
    else:
        os.environ.pop("SPEC_KITTY_WORKTREE_NAME", None)

    if ctx.worktree_path:
        os.environ["SPEC_KITTY_WORKTREE_PATH"] = str(ctx.worktree_path)
    else:
        os.environ.pop("SPEC_KITTY_WORKTREE_PATH", None)


def x_set_context_env_vars__mutmut_3(ctx: CurrentContext) -> None:
    """Set environment variables for current context.

    Makes context information available to subprocesses and scripts.

    Environment variables set:
        SPEC_KITTY_CONTEXT: "main" or "worktree"
        SPEC_KITTY_CWD: Current working directory
        SPEC_KITTY_REPO_ROOT: Repository root (if detected)
        SPEC_KITTY_WORKTREE_NAME: Worktree name (if in worktree)
        SPEC_KITTY_WORKTREE_PATH: Worktree path (if in worktree)

    Args:
        ctx: Current context information

    Example:
        >>> ctx = get_current_context()
        >>> set_context_env_vars(ctx)
        >>> print(os.environ.get("SPEC_KITTY_CONTEXT"))
        "main"
    """
    os.environ["spec_kitty_context"] = ctx.location.value
    os.environ["SPEC_KITTY_CWD"] = str(ctx.cwd)

    if ctx.repo_root:
        os.environ["SPEC_KITTY_REPO_ROOT"] = str(ctx.repo_root)
    else:
        os.environ.pop("SPEC_KITTY_REPO_ROOT", None)

    if ctx.worktree_name:
        os.environ["SPEC_KITTY_WORKTREE_NAME"] = ctx.worktree_name
    else:
        os.environ.pop("SPEC_KITTY_WORKTREE_NAME", None)

    if ctx.worktree_path:
        os.environ["SPEC_KITTY_WORKTREE_PATH"] = str(ctx.worktree_path)
    else:
        os.environ.pop("SPEC_KITTY_WORKTREE_PATH", None)


def x_set_context_env_vars__mutmut_4(ctx: CurrentContext) -> None:
    """Set environment variables for current context.

    Makes context information available to subprocesses and scripts.

    Environment variables set:
        SPEC_KITTY_CONTEXT: "main" or "worktree"
        SPEC_KITTY_CWD: Current working directory
        SPEC_KITTY_REPO_ROOT: Repository root (if detected)
        SPEC_KITTY_WORKTREE_NAME: Worktree name (if in worktree)
        SPEC_KITTY_WORKTREE_PATH: Worktree path (if in worktree)

    Args:
        ctx: Current context information

    Example:
        >>> ctx = get_current_context()
        >>> set_context_env_vars(ctx)
        >>> print(os.environ.get("SPEC_KITTY_CONTEXT"))
        "main"
    """
    os.environ["SPEC_KITTY_CONTEXT"] = ctx.location.value
    os.environ["SPEC_KITTY_CWD"] = None

    if ctx.repo_root:
        os.environ["SPEC_KITTY_REPO_ROOT"] = str(ctx.repo_root)
    else:
        os.environ.pop("SPEC_KITTY_REPO_ROOT", None)

    if ctx.worktree_name:
        os.environ["SPEC_KITTY_WORKTREE_NAME"] = ctx.worktree_name
    else:
        os.environ.pop("SPEC_KITTY_WORKTREE_NAME", None)

    if ctx.worktree_path:
        os.environ["SPEC_KITTY_WORKTREE_PATH"] = str(ctx.worktree_path)
    else:
        os.environ.pop("SPEC_KITTY_WORKTREE_PATH", None)


def x_set_context_env_vars__mutmut_5(ctx: CurrentContext) -> None:
    """Set environment variables for current context.

    Makes context information available to subprocesses and scripts.

    Environment variables set:
        SPEC_KITTY_CONTEXT: "main" or "worktree"
        SPEC_KITTY_CWD: Current working directory
        SPEC_KITTY_REPO_ROOT: Repository root (if detected)
        SPEC_KITTY_WORKTREE_NAME: Worktree name (if in worktree)
        SPEC_KITTY_WORKTREE_PATH: Worktree path (if in worktree)

    Args:
        ctx: Current context information

    Example:
        >>> ctx = get_current_context()
        >>> set_context_env_vars(ctx)
        >>> print(os.environ.get("SPEC_KITTY_CONTEXT"))
        "main"
    """
    os.environ["SPEC_KITTY_CONTEXT"] = ctx.location.value
    os.environ["XXSPEC_KITTY_CWDXX"] = str(ctx.cwd)

    if ctx.repo_root:
        os.environ["SPEC_KITTY_REPO_ROOT"] = str(ctx.repo_root)
    else:
        os.environ.pop("SPEC_KITTY_REPO_ROOT", None)

    if ctx.worktree_name:
        os.environ["SPEC_KITTY_WORKTREE_NAME"] = ctx.worktree_name
    else:
        os.environ.pop("SPEC_KITTY_WORKTREE_NAME", None)

    if ctx.worktree_path:
        os.environ["SPEC_KITTY_WORKTREE_PATH"] = str(ctx.worktree_path)
    else:
        os.environ.pop("SPEC_KITTY_WORKTREE_PATH", None)


def x_set_context_env_vars__mutmut_6(ctx: CurrentContext) -> None:
    """Set environment variables for current context.

    Makes context information available to subprocesses and scripts.

    Environment variables set:
        SPEC_KITTY_CONTEXT: "main" or "worktree"
        SPEC_KITTY_CWD: Current working directory
        SPEC_KITTY_REPO_ROOT: Repository root (if detected)
        SPEC_KITTY_WORKTREE_NAME: Worktree name (if in worktree)
        SPEC_KITTY_WORKTREE_PATH: Worktree path (if in worktree)

    Args:
        ctx: Current context information

    Example:
        >>> ctx = get_current_context()
        >>> set_context_env_vars(ctx)
        >>> print(os.environ.get("SPEC_KITTY_CONTEXT"))
        "main"
    """
    os.environ["SPEC_KITTY_CONTEXT"] = ctx.location.value
    os.environ["spec_kitty_cwd"] = str(ctx.cwd)

    if ctx.repo_root:
        os.environ["SPEC_KITTY_REPO_ROOT"] = str(ctx.repo_root)
    else:
        os.environ.pop("SPEC_KITTY_REPO_ROOT", None)

    if ctx.worktree_name:
        os.environ["SPEC_KITTY_WORKTREE_NAME"] = ctx.worktree_name
    else:
        os.environ.pop("SPEC_KITTY_WORKTREE_NAME", None)

    if ctx.worktree_path:
        os.environ["SPEC_KITTY_WORKTREE_PATH"] = str(ctx.worktree_path)
    else:
        os.environ.pop("SPEC_KITTY_WORKTREE_PATH", None)


def x_set_context_env_vars__mutmut_7(ctx: CurrentContext) -> None:
    """Set environment variables for current context.

    Makes context information available to subprocesses and scripts.

    Environment variables set:
        SPEC_KITTY_CONTEXT: "main" or "worktree"
        SPEC_KITTY_CWD: Current working directory
        SPEC_KITTY_REPO_ROOT: Repository root (if detected)
        SPEC_KITTY_WORKTREE_NAME: Worktree name (if in worktree)
        SPEC_KITTY_WORKTREE_PATH: Worktree path (if in worktree)

    Args:
        ctx: Current context information

    Example:
        >>> ctx = get_current_context()
        >>> set_context_env_vars(ctx)
        >>> print(os.environ.get("SPEC_KITTY_CONTEXT"))
        "main"
    """
    os.environ["SPEC_KITTY_CONTEXT"] = ctx.location.value
    os.environ["SPEC_KITTY_CWD"] = str(None)

    if ctx.repo_root:
        os.environ["SPEC_KITTY_REPO_ROOT"] = str(ctx.repo_root)
    else:
        os.environ.pop("SPEC_KITTY_REPO_ROOT", None)

    if ctx.worktree_name:
        os.environ["SPEC_KITTY_WORKTREE_NAME"] = ctx.worktree_name
    else:
        os.environ.pop("SPEC_KITTY_WORKTREE_NAME", None)

    if ctx.worktree_path:
        os.environ["SPEC_KITTY_WORKTREE_PATH"] = str(ctx.worktree_path)
    else:
        os.environ.pop("SPEC_KITTY_WORKTREE_PATH", None)


def x_set_context_env_vars__mutmut_8(ctx: CurrentContext) -> None:
    """Set environment variables for current context.

    Makes context information available to subprocesses and scripts.

    Environment variables set:
        SPEC_KITTY_CONTEXT: "main" or "worktree"
        SPEC_KITTY_CWD: Current working directory
        SPEC_KITTY_REPO_ROOT: Repository root (if detected)
        SPEC_KITTY_WORKTREE_NAME: Worktree name (if in worktree)
        SPEC_KITTY_WORKTREE_PATH: Worktree path (if in worktree)

    Args:
        ctx: Current context information

    Example:
        >>> ctx = get_current_context()
        >>> set_context_env_vars(ctx)
        >>> print(os.environ.get("SPEC_KITTY_CONTEXT"))
        "main"
    """
    os.environ["SPEC_KITTY_CONTEXT"] = ctx.location.value
    os.environ["SPEC_KITTY_CWD"] = str(ctx.cwd)

    if ctx.repo_root:
        os.environ["SPEC_KITTY_REPO_ROOT"] = None
    else:
        os.environ.pop("SPEC_KITTY_REPO_ROOT", None)

    if ctx.worktree_name:
        os.environ["SPEC_KITTY_WORKTREE_NAME"] = ctx.worktree_name
    else:
        os.environ.pop("SPEC_KITTY_WORKTREE_NAME", None)

    if ctx.worktree_path:
        os.environ["SPEC_KITTY_WORKTREE_PATH"] = str(ctx.worktree_path)
    else:
        os.environ.pop("SPEC_KITTY_WORKTREE_PATH", None)


def x_set_context_env_vars__mutmut_9(ctx: CurrentContext) -> None:
    """Set environment variables for current context.

    Makes context information available to subprocesses and scripts.

    Environment variables set:
        SPEC_KITTY_CONTEXT: "main" or "worktree"
        SPEC_KITTY_CWD: Current working directory
        SPEC_KITTY_REPO_ROOT: Repository root (if detected)
        SPEC_KITTY_WORKTREE_NAME: Worktree name (if in worktree)
        SPEC_KITTY_WORKTREE_PATH: Worktree path (if in worktree)

    Args:
        ctx: Current context information

    Example:
        >>> ctx = get_current_context()
        >>> set_context_env_vars(ctx)
        >>> print(os.environ.get("SPEC_KITTY_CONTEXT"))
        "main"
    """
    os.environ["SPEC_KITTY_CONTEXT"] = ctx.location.value
    os.environ["SPEC_KITTY_CWD"] = str(ctx.cwd)

    if ctx.repo_root:
        os.environ["XXSPEC_KITTY_REPO_ROOTXX"] = str(ctx.repo_root)
    else:
        os.environ.pop("SPEC_KITTY_REPO_ROOT", None)

    if ctx.worktree_name:
        os.environ["SPEC_KITTY_WORKTREE_NAME"] = ctx.worktree_name
    else:
        os.environ.pop("SPEC_KITTY_WORKTREE_NAME", None)

    if ctx.worktree_path:
        os.environ["SPEC_KITTY_WORKTREE_PATH"] = str(ctx.worktree_path)
    else:
        os.environ.pop("SPEC_KITTY_WORKTREE_PATH", None)


def x_set_context_env_vars__mutmut_10(ctx: CurrentContext) -> None:
    """Set environment variables for current context.

    Makes context information available to subprocesses and scripts.

    Environment variables set:
        SPEC_KITTY_CONTEXT: "main" or "worktree"
        SPEC_KITTY_CWD: Current working directory
        SPEC_KITTY_REPO_ROOT: Repository root (if detected)
        SPEC_KITTY_WORKTREE_NAME: Worktree name (if in worktree)
        SPEC_KITTY_WORKTREE_PATH: Worktree path (if in worktree)

    Args:
        ctx: Current context information

    Example:
        >>> ctx = get_current_context()
        >>> set_context_env_vars(ctx)
        >>> print(os.environ.get("SPEC_KITTY_CONTEXT"))
        "main"
    """
    os.environ["SPEC_KITTY_CONTEXT"] = ctx.location.value
    os.environ["SPEC_KITTY_CWD"] = str(ctx.cwd)

    if ctx.repo_root:
        os.environ["spec_kitty_repo_root"] = str(ctx.repo_root)
    else:
        os.environ.pop("SPEC_KITTY_REPO_ROOT", None)

    if ctx.worktree_name:
        os.environ["SPEC_KITTY_WORKTREE_NAME"] = ctx.worktree_name
    else:
        os.environ.pop("SPEC_KITTY_WORKTREE_NAME", None)

    if ctx.worktree_path:
        os.environ["SPEC_KITTY_WORKTREE_PATH"] = str(ctx.worktree_path)
    else:
        os.environ.pop("SPEC_KITTY_WORKTREE_PATH", None)


def x_set_context_env_vars__mutmut_11(ctx: CurrentContext) -> None:
    """Set environment variables for current context.

    Makes context information available to subprocesses and scripts.

    Environment variables set:
        SPEC_KITTY_CONTEXT: "main" or "worktree"
        SPEC_KITTY_CWD: Current working directory
        SPEC_KITTY_REPO_ROOT: Repository root (if detected)
        SPEC_KITTY_WORKTREE_NAME: Worktree name (if in worktree)
        SPEC_KITTY_WORKTREE_PATH: Worktree path (if in worktree)

    Args:
        ctx: Current context information

    Example:
        >>> ctx = get_current_context()
        >>> set_context_env_vars(ctx)
        >>> print(os.environ.get("SPEC_KITTY_CONTEXT"))
        "main"
    """
    os.environ["SPEC_KITTY_CONTEXT"] = ctx.location.value
    os.environ["SPEC_KITTY_CWD"] = str(ctx.cwd)

    if ctx.repo_root:
        os.environ["SPEC_KITTY_REPO_ROOT"] = str(None)
    else:
        os.environ.pop("SPEC_KITTY_REPO_ROOT", None)

    if ctx.worktree_name:
        os.environ["SPEC_KITTY_WORKTREE_NAME"] = ctx.worktree_name
    else:
        os.environ.pop("SPEC_KITTY_WORKTREE_NAME", None)

    if ctx.worktree_path:
        os.environ["SPEC_KITTY_WORKTREE_PATH"] = str(ctx.worktree_path)
    else:
        os.environ.pop("SPEC_KITTY_WORKTREE_PATH", None)


def x_set_context_env_vars__mutmut_12(ctx: CurrentContext) -> None:
    """Set environment variables for current context.

    Makes context information available to subprocesses and scripts.

    Environment variables set:
        SPEC_KITTY_CONTEXT: "main" or "worktree"
        SPEC_KITTY_CWD: Current working directory
        SPEC_KITTY_REPO_ROOT: Repository root (if detected)
        SPEC_KITTY_WORKTREE_NAME: Worktree name (if in worktree)
        SPEC_KITTY_WORKTREE_PATH: Worktree path (if in worktree)

    Args:
        ctx: Current context information

    Example:
        >>> ctx = get_current_context()
        >>> set_context_env_vars(ctx)
        >>> print(os.environ.get("SPEC_KITTY_CONTEXT"))
        "main"
    """
    os.environ["SPEC_KITTY_CONTEXT"] = ctx.location.value
    os.environ["SPEC_KITTY_CWD"] = str(ctx.cwd)

    if ctx.repo_root:
        os.environ["SPEC_KITTY_REPO_ROOT"] = str(ctx.repo_root)
    else:
        os.environ.pop(None, None)

    if ctx.worktree_name:
        os.environ["SPEC_KITTY_WORKTREE_NAME"] = ctx.worktree_name
    else:
        os.environ.pop("SPEC_KITTY_WORKTREE_NAME", None)

    if ctx.worktree_path:
        os.environ["SPEC_KITTY_WORKTREE_PATH"] = str(ctx.worktree_path)
    else:
        os.environ.pop("SPEC_KITTY_WORKTREE_PATH", None)


def x_set_context_env_vars__mutmut_13(ctx: CurrentContext) -> None:
    """Set environment variables for current context.

    Makes context information available to subprocesses and scripts.

    Environment variables set:
        SPEC_KITTY_CONTEXT: "main" or "worktree"
        SPEC_KITTY_CWD: Current working directory
        SPEC_KITTY_REPO_ROOT: Repository root (if detected)
        SPEC_KITTY_WORKTREE_NAME: Worktree name (if in worktree)
        SPEC_KITTY_WORKTREE_PATH: Worktree path (if in worktree)

    Args:
        ctx: Current context information

    Example:
        >>> ctx = get_current_context()
        >>> set_context_env_vars(ctx)
        >>> print(os.environ.get("SPEC_KITTY_CONTEXT"))
        "main"
    """
    os.environ["SPEC_KITTY_CONTEXT"] = ctx.location.value
    os.environ["SPEC_KITTY_CWD"] = str(ctx.cwd)

    if ctx.repo_root:
        os.environ["SPEC_KITTY_REPO_ROOT"] = str(ctx.repo_root)
    else:
        os.environ.pop(None)

    if ctx.worktree_name:
        os.environ["SPEC_KITTY_WORKTREE_NAME"] = ctx.worktree_name
    else:
        os.environ.pop("SPEC_KITTY_WORKTREE_NAME", None)

    if ctx.worktree_path:
        os.environ["SPEC_KITTY_WORKTREE_PATH"] = str(ctx.worktree_path)
    else:
        os.environ.pop("SPEC_KITTY_WORKTREE_PATH", None)


def x_set_context_env_vars__mutmut_14(ctx: CurrentContext) -> None:
    """Set environment variables for current context.

    Makes context information available to subprocesses and scripts.

    Environment variables set:
        SPEC_KITTY_CONTEXT: "main" or "worktree"
        SPEC_KITTY_CWD: Current working directory
        SPEC_KITTY_REPO_ROOT: Repository root (if detected)
        SPEC_KITTY_WORKTREE_NAME: Worktree name (if in worktree)
        SPEC_KITTY_WORKTREE_PATH: Worktree path (if in worktree)

    Args:
        ctx: Current context information

    Example:
        >>> ctx = get_current_context()
        >>> set_context_env_vars(ctx)
        >>> print(os.environ.get("SPEC_KITTY_CONTEXT"))
        "main"
    """
    os.environ["SPEC_KITTY_CONTEXT"] = ctx.location.value
    os.environ["SPEC_KITTY_CWD"] = str(ctx.cwd)

    if ctx.repo_root:
        os.environ["SPEC_KITTY_REPO_ROOT"] = str(ctx.repo_root)
    else:
        os.environ.pop("SPEC_KITTY_REPO_ROOT", )

    if ctx.worktree_name:
        os.environ["SPEC_KITTY_WORKTREE_NAME"] = ctx.worktree_name
    else:
        os.environ.pop("SPEC_KITTY_WORKTREE_NAME", None)

    if ctx.worktree_path:
        os.environ["SPEC_KITTY_WORKTREE_PATH"] = str(ctx.worktree_path)
    else:
        os.environ.pop("SPEC_KITTY_WORKTREE_PATH", None)


def x_set_context_env_vars__mutmut_15(ctx: CurrentContext) -> None:
    """Set environment variables for current context.

    Makes context information available to subprocesses and scripts.

    Environment variables set:
        SPEC_KITTY_CONTEXT: "main" or "worktree"
        SPEC_KITTY_CWD: Current working directory
        SPEC_KITTY_REPO_ROOT: Repository root (if detected)
        SPEC_KITTY_WORKTREE_NAME: Worktree name (if in worktree)
        SPEC_KITTY_WORKTREE_PATH: Worktree path (if in worktree)

    Args:
        ctx: Current context information

    Example:
        >>> ctx = get_current_context()
        >>> set_context_env_vars(ctx)
        >>> print(os.environ.get("SPEC_KITTY_CONTEXT"))
        "main"
    """
    os.environ["SPEC_KITTY_CONTEXT"] = ctx.location.value
    os.environ["SPEC_KITTY_CWD"] = str(ctx.cwd)

    if ctx.repo_root:
        os.environ["SPEC_KITTY_REPO_ROOT"] = str(ctx.repo_root)
    else:
        os.environ.pop("XXSPEC_KITTY_REPO_ROOTXX", None)

    if ctx.worktree_name:
        os.environ["SPEC_KITTY_WORKTREE_NAME"] = ctx.worktree_name
    else:
        os.environ.pop("SPEC_KITTY_WORKTREE_NAME", None)

    if ctx.worktree_path:
        os.environ["SPEC_KITTY_WORKTREE_PATH"] = str(ctx.worktree_path)
    else:
        os.environ.pop("SPEC_KITTY_WORKTREE_PATH", None)


def x_set_context_env_vars__mutmut_16(ctx: CurrentContext) -> None:
    """Set environment variables for current context.

    Makes context information available to subprocesses and scripts.

    Environment variables set:
        SPEC_KITTY_CONTEXT: "main" or "worktree"
        SPEC_KITTY_CWD: Current working directory
        SPEC_KITTY_REPO_ROOT: Repository root (if detected)
        SPEC_KITTY_WORKTREE_NAME: Worktree name (if in worktree)
        SPEC_KITTY_WORKTREE_PATH: Worktree path (if in worktree)

    Args:
        ctx: Current context information

    Example:
        >>> ctx = get_current_context()
        >>> set_context_env_vars(ctx)
        >>> print(os.environ.get("SPEC_KITTY_CONTEXT"))
        "main"
    """
    os.environ["SPEC_KITTY_CONTEXT"] = ctx.location.value
    os.environ["SPEC_KITTY_CWD"] = str(ctx.cwd)

    if ctx.repo_root:
        os.environ["SPEC_KITTY_REPO_ROOT"] = str(ctx.repo_root)
    else:
        os.environ.pop("spec_kitty_repo_root", None)

    if ctx.worktree_name:
        os.environ["SPEC_KITTY_WORKTREE_NAME"] = ctx.worktree_name
    else:
        os.environ.pop("SPEC_KITTY_WORKTREE_NAME", None)

    if ctx.worktree_path:
        os.environ["SPEC_KITTY_WORKTREE_PATH"] = str(ctx.worktree_path)
    else:
        os.environ.pop("SPEC_KITTY_WORKTREE_PATH", None)


def x_set_context_env_vars__mutmut_17(ctx: CurrentContext) -> None:
    """Set environment variables for current context.

    Makes context information available to subprocesses and scripts.

    Environment variables set:
        SPEC_KITTY_CONTEXT: "main" or "worktree"
        SPEC_KITTY_CWD: Current working directory
        SPEC_KITTY_REPO_ROOT: Repository root (if detected)
        SPEC_KITTY_WORKTREE_NAME: Worktree name (if in worktree)
        SPEC_KITTY_WORKTREE_PATH: Worktree path (if in worktree)

    Args:
        ctx: Current context information

    Example:
        >>> ctx = get_current_context()
        >>> set_context_env_vars(ctx)
        >>> print(os.environ.get("SPEC_KITTY_CONTEXT"))
        "main"
    """
    os.environ["SPEC_KITTY_CONTEXT"] = ctx.location.value
    os.environ["SPEC_KITTY_CWD"] = str(ctx.cwd)

    if ctx.repo_root:
        os.environ["SPEC_KITTY_REPO_ROOT"] = str(ctx.repo_root)
    else:
        os.environ.pop("SPEC_KITTY_REPO_ROOT", None)

    if ctx.worktree_name:
        os.environ["SPEC_KITTY_WORKTREE_NAME"] = None
    else:
        os.environ.pop("SPEC_KITTY_WORKTREE_NAME", None)

    if ctx.worktree_path:
        os.environ["SPEC_KITTY_WORKTREE_PATH"] = str(ctx.worktree_path)
    else:
        os.environ.pop("SPEC_KITTY_WORKTREE_PATH", None)


def x_set_context_env_vars__mutmut_18(ctx: CurrentContext) -> None:
    """Set environment variables for current context.

    Makes context information available to subprocesses and scripts.

    Environment variables set:
        SPEC_KITTY_CONTEXT: "main" or "worktree"
        SPEC_KITTY_CWD: Current working directory
        SPEC_KITTY_REPO_ROOT: Repository root (if detected)
        SPEC_KITTY_WORKTREE_NAME: Worktree name (if in worktree)
        SPEC_KITTY_WORKTREE_PATH: Worktree path (if in worktree)

    Args:
        ctx: Current context information

    Example:
        >>> ctx = get_current_context()
        >>> set_context_env_vars(ctx)
        >>> print(os.environ.get("SPEC_KITTY_CONTEXT"))
        "main"
    """
    os.environ["SPEC_KITTY_CONTEXT"] = ctx.location.value
    os.environ["SPEC_KITTY_CWD"] = str(ctx.cwd)

    if ctx.repo_root:
        os.environ["SPEC_KITTY_REPO_ROOT"] = str(ctx.repo_root)
    else:
        os.environ.pop("SPEC_KITTY_REPO_ROOT", None)

    if ctx.worktree_name:
        os.environ["XXSPEC_KITTY_WORKTREE_NAMEXX"] = ctx.worktree_name
    else:
        os.environ.pop("SPEC_KITTY_WORKTREE_NAME", None)

    if ctx.worktree_path:
        os.environ["SPEC_KITTY_WORKTREE_PATH"] = str(ctx.worktree_path)
    else:
        os.environ.pop("SPEC_KITTY_WORKTREE_PATH", None)


def x_set_context_env_vars__mutmut_19(ctx: CurrentContext) -> None:
    """Set environment variables for current context.

    Makes context information available to subprocesses and scripts.

    Environment variables set:
        SPEC_KITTY_CONTEXT: "main" or "worktree"
        SPEC_KITTY_CWD: Current working directory
        SPEC_KITTY_REPO_ROOT: Repository root (if detected)
        SPEC_KITTY_WORKTREE_NAME: Worktree name (if in worktree)
        SPEC_KITTY_WORKTREE_PATH: Worktree path (if in worktree)

    Args:
        ctx: Current context information

    Example:
        >>> ctx = get_current_context()
        >>> set_context_env_vars(ctx)
        >>> print(os.environ.get("SPEC_KITTY_CONTEXT"))
        "main"
    """
    os.environ["SPEC_KITTY_CONTEXT"] = ctx.location.value
    os.environ["SPEC_KITTY_CWD"] = str(ctx.cwd)

    if ctx.repo_root:
        os.environ["SPEC_KITTY_REPO_ROOT"] = str(ctx.repo_root)
    else:
        os.environ.pop("SPEC_KITTY_REPO_ROOT", None)

    if ctx.worktree_name:
        os.environ["spec_kitty_worktree_name"] = ctx.worktree_name
    else:
        os.environ.pop("SPEC_KITTY_WORKTREE_NAME", None)

    if ctx.worktree_path:
        os.environ["SPEC_KITTY_WORKTREE_PATH"] = str(ctx.worktree_path)
    else:
        os.environ.pop("SPEC_KITTY_WORKTREE_PATH", None)


def x_set_context_env_vars__mutmut_20(ctx: CurrentContext) -> None:
    """Set environment variables for current context.

    Makes context information available to subprocesses and scripts.

    Environment variables set:
        SPEC_KITTY_CONTEXT: "main" or "worktree"
        SPEC_KITTY_CWD: Current working directory
        SPEC_KITTY_REPO_ROOT: Repository root (if detected)
        SPEC_KITTY_WORKTREE_NAME: Worktree name (if in worktree)
        SPEC_KITTY_WORKTREE_PATH: Worktree path (if in worktree)

    Args:
        ctx: Current context information

    Example:
        >>> ctx = get_current_context()
        >>> set_context_env_vars(ctx)
        >>> print(os.environ.get("SPEC_KITTY_CONTEXT"))
        "main"
    """
    os.environ["SPEC_KITTY_CONTEXT"] = ctx.location.value
    os.environ["SPEC_KITTY_CWD"] = str(ctx.cwd)

    if ctx.repo_root:
        os.environ["SPEC_KITTY_REPO_ROOT"] = str(ctx.repo_root)
    else:
        os.environ.pop("SPEC_KITTY_REPO_ROOT", None)

    if ctx.worktree_name:
        os.environ["SPEC_KITTY_WORKTREE_NAME"] = ctx.worktree_name
    else:
        os.environ.pop(None, None)

    if ctx.worktree_path:
        os.environ["SPEC_KITTY_WORKTREE_PATH"] = str(ctx.worktree_path)
    else:
        os.environ.pop("SPEC_KITTY_WORKTREE_PATH", None)


def x_set_context_env_vars__mutmut_21(ctx: CurrentContext) -> None:
    """Set environment variables for current context.

    Makes context information available to subprocesses and scripts.

    Environment variables set:
        SPEC_KITTY_CONTEXT: "main" or "worktree"
        SPEC_KITTY_CWD: Current working directory
        SPEC_KITTY_REPO_ROOT: Repository root (if detected)
        SPEC_KITTY_WORKTREE_NAME: Worktree name (if in worktree)
        SPEC_KITTY_WORKTREE_PATH: Worktree path (if in worktree)

    Args:
        ctx: Current context information

    Example:
        >>> ctx = get_current_context()
        >>> set_context_env_vars(ctx)
        >>> print(os.environ.get("SPEC_KITTY_CONTEXT"))
        "main"
    """
    os.environ["SPEC_KITTY_CONTEXT"] = ctx.location.value
    os.environ["SPEC_KITTY_CWD"] = str(ctx.cwd)

    if ctx.repo_root:
        os.environ["SPEC_KITTY_REPO_ROOT"] = str(ctx.repo_root)
    else:
        os.environ.pop("SPEC_KITTY_REPO_ROOT", None)

    if ctx.worktree_name:
        os.environ["SPEC_KITTY_WORKTREE_NAME"] = ctx.worktree_name
    else:
        os.environ.pop(None)

    if ctx.worktree_path:
        os.environ["SPEC_KITTY_WORKTREE_PATH"] = str(ctx.worktree_path)
    else:
        os.environ.pop("SPEC_KITTY_WORKTREE_PATH", None)


def x_set_context_env_vars__mutmut_22(ctx: CurrentContext) -> None:
    """Set environment variables for current context.

    Makes context information available to subprocesses and scripts.

    Environment variables set:
        SPEC_KITTY_CONTEXT: "main" or "worktree"
        SPEC_KITTY_CWD: Current working directory
        SPEC_KITTY_REPO_ROOT: Repository root (if detected)
        SPEC_KITTY_WORKTREE_NAME: Worktree name (if in worktree)
        SPEC_KITTY_WORKTREE_PATH: Worktree path (if in worktree)

    Args:
        ctx: Current context information

    Example:
        >>> ctx = get_current_context()
        >>> set_context_env_vars(ctx)
        >>> print(os.environ.get("SPEC_KITTY_CONTEXT"))
        "main"
    """
    os.environ["SPEC_KITTY_CONTEXT"] = ctx.location.value
    os.environ["SPEC_KITTY_CWD"] = str(ctx.cwd)

    if ctx.repo_root:
        os.environ["SPEC_KITTY_REPO_ROOT"] = str(ctx.repo_root)
    else:
        os.environ.pop("SPEC_KITTY_REPO_ROOT", None)

    if ctx.worktree_name:
        os.environ["SPEC_KITTY_WORKTREE_NAME"] = ctx.worktree_name
    else:
        os.environ.pop("SPEC_KITTY_WORKTREE_NAME", )

    if ctx.worktree_path:
        os.environ["SPEC_KITTY_WORKTREE_PATH"] = str(ctx.worktree_path)
    else:
        os.environ.pop("SPEC_KITTY_WORKTREE_PATH", None)


def x_set_context_env_vars__mutmut_23(ctx: CurrentContext) -> None:
    """Set environment variables for current context.

    Makes context information available to subprocesses and scripts.

    Environment variables set:
        SPEC_KITTY_CONTEXT: "main" or "worktree"
        SPEC_KITTY_CWD: Current working directory
        SPEC_KITTY_REPO_ROOT: Repository root (if detected)
        SPEC_KITTY_WORKTREE_NAME: Worktree name (if in worktree)
        SPEC_KITTY_WORKTREE_PATH: Worktree path (if in worktree)

    Args:
        ctx: Current context information

    Example:
        >>> ctx = get_current_context()
        >>> set_context_env_vars(ctx)
        >>> print(os.environ.get("SPEC_KITTY_CONTEXT"))
        "main"
    """
    os.environ["SPEC_KITTY_CONTEXT"] = ctx.location.value
    os.environ["SPEC_KITTY_CWD"] = str(ctx.cwd)

    if ctx.repo_root:
        os.environ["SPEC_KITTY_REPO_ROOT"] = str(ctx.repo_root)
    else:
        os.environ.pop("SPEC_KITTY_REPO_ROOT", None)

    if ctx.worktree_name:
        os.environ["SPEC_KITTY_WORKTREE_NAME"] = ctx.worktree_name
    else:
        os.environ.pop("XXSPEC_KITTY_WORKTREE_NAMEXX", None)

    if ctx.worktree_path:
        os.environ["SPEC_KITTY_WORKTREE_PATH"] = str(ctx.worktree_path)
    else:
        os.environ.pop("SPEC_KITTY_WORKTREE_PATH", None)


def x_set_context_env_vars__mutmut_24(ctx: CurrentContext) -> None:
    """Set environment variables for current context.

    Makes context information available to subprocesses and scripts.

    Environment variables set:
        SPEC_KITTY_CONTEXT: "main" or "worktree"
        SPEC_KITTY_CWD: Current working directory
        SPEC_KITTY_REPO_ROOT: Repository root (if detected)
        SPEC_KITTY_WORKTREE_NAME: Worktree name (if in worktree)
        SPEC_KITTY_WORKTREE_PATH: Worktree path (if in worktree)

    Args:
        ctx: Current context information

    Example:
        >>> ctx = get_current_context()
        >>> set_context_env_vars(ctx)
        >>> print(os.environ.get("SPEC_KITTY_CONTEXT"))
        "main"
    """
    os.environ["SPEC_KITTY_CONTEXT"] = ctx.location.value
    os.environ["SPEC_KITTY_CWD"] = str(ctx.cwd)

    if ctx.repo_root:
        os.environ["SPEC_KITTY_REPO_ROOT"] = str(ctx.repo_root)
    else:
        os.environ.pop("SPEC_KITTY_REPO_ROOT", None)

    if ctx.worktree_name:
        os.environ["SPEC_KITTY_WORKTREE_NAME"] = ctx.worktree_name
    else:
        os.environ.pop("spec_kitty_worktree_name", None)

    if ctx.worktree_path:
        os.environ["SPEC_KITTY_WORKTREE_PATH"] = str(ctx.worktree_path)
    else:
        os.environ.pop("SPEC_KITTY_WORKTREE_PATH", None)


def x_set_context_env_vars__mutmut_25(ctx: CurrentContext) -> None:
    """Set environment variables for current context.

    Makes context information available to subprocesses and scripts.

    Environment variables set:
        SPEC_KITTY_CONTEXT: "main" or "worktree"
        SPEC_KITTY_CWD: Current working directory
        SPEC_KITTY_REPO_ROOT: Repository root (if detected)
        SPEC_KITTY_WORKTREE_NAME: Worktree name (if in worktree)
        SPEC_KITTY_WORKTREE_PATH: Worktree path (if in worktree)

    Args:
        ctx: Current context information

    Example:
        >>> ctx = get_current_context()
        >>> set_context_env_vars(ctx)
        >>> print(os.environ.get("SPEC_KITTY_CONTEXT"))
        "main"
    """
    os.environ["SPEC_KITTY_CONTEXT"] = ctx.location.value
    os.environ["SPEC_KITTY_CWD"] = str(ctx.cwd)

    if ctx.repo_root:
        os.environ["SPEC_KITTY_REPO_ROOT"] = str(ctx.repo_root)
    else:
        os.environ.pop("SPEC_KITTY_REPO_ROOT", None)

    if ctx.worktree_name:
        os.environ["SPEC_KITTY_WORKTREE_NAME"] = ctx.worktree_name
    else:
        os.environ.pop("SPEC_KITTY_WORKTREE_NAME", None)

    if ctx.worktree_path:
        os.environ["SPEC_KITTY_WORKTREE_PATH"] = None
    else:
        os.environ.pop("SPEC_KITTY_WORKTREE_PATH", None)


def x_set_context_env_vars__mutmut_26(ctx: CurrentContext) -> None:
    """Set environment variables for current context.

    Makes context information available to subprocesses and scripts.

    Environment variables set:
        SPEC_KITTY_CONTEXT: "main" or "worktree"
        SPEC_KITTY_CWD: Current working directory
        SPEC_KITTY_REPO_ROOT: Repository root (if detected)
        SPEC_KITTY_WORKTREE_NAME: Worktree name (if in worktree)
        SPEC_KITTY_WORKTREE_PATH: Worktree path (if in worktree)

    Args:
        ctx: Current context information

    Example:
        >>> ctx = get_current_context()
        >>> set_context_env_vars(ctx)
        >>> print(os.environ.get("SPEC_KITTY_CONTEXT"))
        "main"
    """
    os.environ["SPEC_KITTY_CONTEXT"] = ctx.location.value
    os.environ["SPEC_KITTY_CWD"] = str(ctx.cwd)

    if ctx.repo_root:
        os.environ["SPEC_KITTY_REPO_ROOT"] = str(ctx.repo_root)
    else:
        os.environ.pop("SPEC_KITTY_REPO_ROOT", None)

    if ctx.worktree_name:
        os.environ["SPEC_KITTY_WORKTREE_NAME"] = ctx.worktree_name
    else:
        os.environ.pop("SPEC_KITTY_WORKTREE_NAME", None)

    if ctx.worktree_path:
        os.environ["XXSPEC_KITTY_WORKTREE_PATHXX"] = str(ctx.worktree_path)
    else:
        os.environ.pop("SPEC_KITTY_WORKTREE_PATH", None)


def x_set_context_env_vars__mutmut_27(ctx: CurrentContext) -> None:
    """Set environment variables for current context.

    Makes context information available to subprocesses and scripts.

    Environment variables set:
        SPEC_KITTY_CONTEXT: "main" or "worktree"
        SPEC_KITTY_CWD: Current working directory
        SPEC_KITTY_REPO_ROOT: Repository root (if detected)
        SPEC_KITTY_WORKTREE_NAME: Worktree name (if in worktree)
        SPEC_KITTY_WORKTREE_PATH: Worktree path (if in worktree)

    Args:
        ctx: Current context information

    Example:
        >>> ctx = get_current_context()
        >>> set_context_env_vars(ctx)
        >>> print(os.environ.get("SPEC_KITTY_CONTEXT"))
        "main"
    """
    os.environ["SPEC_KITTY_CONTEXT"] = ctx.location.value
    os.environ["SPEC_KITTY_CWD"] = str(ctx.cwd)

    if ctx.repo_root:
        os.environ["SPEC_KITTY_REPO_ROOT"] = str(ctx.repo_root)
    else:
        os.environ.pop("SPEC_KITTY_REPO_ROOT", None)

    if ctx.worktree_name:
        os.environ["SPEC_KITTY_WORKTREE_NAME"] = ctx.worktree_name
    else:
        os.environ.pop("SPEC_KITTY_WORKTREE_NAME", None)

    if ctx.worktree_path:
        os.environ["spec_kitty_worktree_path"] = str(ctx.worktree_path)
    else:
        os.environ.pop("SPEC_KITTY_WORKTREE_PATH", None)


def x_set_context_env_vars__mutmut_28(ctx: CurrentContext) -> None:
    """Set environment variables for current context.

    Makes context information available to subprocesses and scripts.

    Environment variables set:
        SPEC_KITTY_CONTEXT: "main" or "worktree"
        SPEC_KITTY_CWD: Current working directory
        SPEC_KITTY_REPO_ROOT: Repository root (if detected)
        SPEC_KITTY_WORKTREE_NAME: Worktree name (if in worktree)
        SPEC_KITTY_WORKTREE_PATH: Worktree path (if in worktree)

    Args:
        ctx: Current context information

    Example:
        >>> ctx = get_current_context()
        >>> set_context_env_vars(ctx)
        >>> print(os.environ.get("SPEC_KITTY_CONTEXT"))
        "main"
    """
    os.environ["SPEC_KITTY_CONTEXT"] = ctx.location.value
    os.environ["SPEC_KITTY_CWD"] = str(ctx.cwd)

    if ctx.repo_root:
        os.environ["SPEC_KITTY_REPO_ROOT"] = str(ctx.repo_root)
    else:
        os.environ.pop("SPEC_KITTY_REPO_ROOT", None)

    if ctx.worktree_name:
        os.environ["SPEC_KITTY_WORKTREE_NAME"] = ctx.worktree_name
    else:
        os.environ.pop("SPEC_KITTY_WORKTREE_NAME", None)

    if ctx.worktree_path:
        os.environ["SPEC_KITTY_WORKTREE_PATH"] = str(None)
    else:
        os.environ.pop("SPEC_KITTY_WORKTREE_PATH", None)


def x_set_context_env_vars__mutmut_29(ctx: CurrentContext) -> None:
    """Set environment variables for current context.

    Makes context information available to subprocesses and scripts.

    Environment variables set:
        SPEC_KITTY_CONTEXT: "main" or "worktree"
        SPEC_KITTY_CWD: Current working directory
        SPEC_KITTY_REPO_ROOT: Repository root (if detected)
        SPEC_KITTY_WORKTREE_NAME: Worktree name (if in worktree)
        SPEC_KITTY_WORKTREE_PATH: Worktree path (if in worktree)

    Args:
        ctx: Current context information

    Example:
        >>> ctx = get_current_context()
        >>> set_context_env_vars(ctx)
        >>> print(os.environ.get("SPEC_KITTY_CONTEXT"))
        "main"
    """
    os.environ["SPEC_KITTY_CONTEXT"] = ctx.location.value
    os.environ["SPEC_KITTY_CWD"] = str(ctx.cwd)

    if ctx.repo_root:
        os.environ["SPEC_KITTY_REPO_ROOT"] = str(ctx.repo_root)
    else:
        os.environ.pop("SPEC_KITTY_REPO_ROOT", None)

    if ctx.worktree_name:
        os.environ["SPEC_KITTY_WORKTREE_NAME"] = ctx.worktree_name
    else:
        os.environ.pop("SPEC_KITTY_WORKTREE_NAME", None)

    if ctx.worktree_path:
        os.environ["SPEC_KITTY_WORKTREE_PATH"] = str(ctx.worktree_path)
    else:
        os.environ.pop(None, None)


def x_set_context_env_vars__mutmut_30(ctx: CurrentContext) -> None:
    """Set environment variables for current context.

    Makes context information available to subprocesses and scripts.

    Environment variables set:
        SPEC_KITTY_CONTEXT: "main" or "worktree"
        SPEC_KITTY_CWD: Current working directory
        SPEC_KITTY_REPO_ROOT: Repository root (if detected)
        SPEC_KITTY_WORKTREE_NAME: Worktree name (if in worktree)
        SPEC_KITTY_WORKTREE_PATH: Worktree path (if in worktree)

    Args:
        ctx: Current context information

    Example:
        >>> ctx = get_current_context()
        >>> set_context_env_vars(ctx)
        >>> print(os.environ.get("SPEC_KITTY_CONTEXT"))
        "main"
    """
    os.environ["SPEC_KITTY_CONTEXT"] = ctx.location.value
    os.environ["SPEC_KITTY_CWD"] = str(ctx.cwd)

    if ctx.repo_root:
        os.environ["SPEC_KITTY_REPO_ROOT"] = str(ctx.repo_root)
    else:
        os.environ.pop("SPEC_KITTY_REPO_ROOT", None)

    if ctx.worktree_name:
        os.environ["SPEC_KITTY_WORKTREE_NAME"] = ctx.worktree_name
    else:
        os.environ.pop("SPEC_KITTY_WORKTREE_NAME", None)

    if ctx.worktree_path:
        os.environ["SPEC_KITTY_WORKTREE_PATH"] = str(ctx.worktree_path)
    else:
        os.environ.pop(None)


def x_set_context_env_vars__mutmut_31(ctx: CurrentContext) -> None:
    """Set environment variables for current context.

    Makes context information available to subprocesses and scripts.

    Environment variables set:
        SPEC_KITTY_CONTEXT: "main" or "worktree"
        SPEC_KITTY_CWD: Current working directory
        SPEC_KITTY_REPO_ROOT: Repository root (if detected)
        SPEC_KITTY_WORKTREE_NAME: Worktree name (if in worktree)
        SPEC_KITTY_WORKTREE_PATH: Worktree path (if in worktree)

    Args:
        ctx: Current context information

    Example:
        >>> ctx = get_current_context()
        >>> set_context_env_vars(ctx)
        >>> print(os.environ.get("SPEC_KITTY_CONTEXT"))
        "main"
    """
    os.environ["SPEC_KITTY_CONTEXT"] = ctx.location.value
    os.environ["SPEC_KITTY_CWD"] = str(ctx.cwd)

    if ctx.repo_root:
        os.environ["SPEC_KITTY_REPO_ROOT"] = str(ctx.repo_root)
    else:
        os.environ.pop("SPEC_KITTY_REPO_ROOT", None)

    if ctx.worktree_name:
        os.environ["SPEC_KITTY_WORKTREE_NAME"] = ctx.worktree_name
    else:
        os.environ.pop("SPEC_KITTY_WORKTREE_NAME", None)

    if ctx.worktree_path:
        os.environ["SPEC_KITTY_WORKTREE_PATH"] = str(ctx.worktree_path)
    else:
        os.environ.pop("SPEC_KITTY_WORKTREE_PATH", )


def x_set_context_env_vars__mutmut_32(ctx: CurrentContext) -> None:
    """Set environment variables for current context.

    Makes context information available to subprocesses and scripts.

    Environment variables set:
        SPEC_KITTY_CONTEXT: "main" or "worktree"
        SPEC_KITTY_CWD: Current working directory
        SPEC_KITTY_REPO_ROOT: Repository root (if detected)
        SPEC_KITTY_WORKTREE_NAME: Worktree name (if in worktree)
        SPEC_KITTY_WORKTREE_PATH: Worktree path (if in worktree)

    Args:
        ctx: Current context information

    Example:
        >>> ctx = get_current_context()
        >>> set_context_env_vars(ctx)
        >>> print(os.environ.get("SPEC_KITTY_CONTEXT"))
        "main"
    """
    os.environ["SPEC_KITTY_CONTEXT"] = ctx.location.value
    os.environ["SPEC_KITTY_CWD"] = str(ctx.cwd)

    if ctx.repo_root:
        os.environ["SPEC_KITTY_REPO_ROOT"] = str(ctx.repo_root)
    else:
        os.environ.pop("SPEC_KITTY_REPO_ROOT", None)

    if ctx.worktree_name:
        os.environ["SPEC_KITTY_WORKTREE_NAME"] = ctx.worktree_name
    else:
        os.environ.pop("SPEC_KITTY_WORKTREE_NAME", None)

    if ctx.worktree_path:
        os.environ["SPEC_KITTY_WORKTREE_PATH"] = str(ctx.worktree_path)
    else:
        os.environ.pop("XXSPEC_KITTY_WORKTREE_PATHXX", None)


def x_set_context_env_vars__mutmut_33(ctx: CurrentContext) -> None:
    """Set environment variables for current context.

    Makes context information available to subprocesses and scripts.

    Environment variables set:
        SPEC_KITTY_CONTEXT: "main" or "worktree"
        SPEC_KITTY_CWD: Current working directory
        SPEC_KITTY_REPO_ROOT: Repository root (if detected)
        SPEC_KITTY_WORKTREE_NAME: Worktree name (if in worktree)
        SPEC_KITTY_WORKTREE_PATH: Worktree path (if in worktree)

    Args:
        ctx: Current context information

    Example:
        >>> ctx = get_current_context()
        >>> set_context_env_vars(ctx)
        >>> print(os.environ.get("SPEC_KITTY_CONTEXT"))
        "main"
    """
    os.environ["SPEC_KITTY_CONTEXT"] = ctx.location.value
    os.environ["SPEC_KITTY_CWD"] = str(ctx.cwd)

    if ctx.repo_root:
        os.environ["SPEC_KITTY_REPO_ROOT"] = str(ctx.repo_root)
    else:
        os.environ.pop("SPEC_KITTY_REPO_ROOT", None)

    if ctx.worktree_name:
        os.environ["SPEC_KITTY_WORKTREE_NAME"] = ctx.worktree_name
    else:
        os.environ.pop("SPEC_KITTY_WORKTREE_NAME", None)

    if ctx.worktree_path:
        os.environ["SPEC_KITTY_WORKTREE_PATH"] = str(ctx.worktree_path)
    else:
        os.environ.pop("spec_kitty_worktree_path", None)

x_set_context_env_vars__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_set_context_env_vars__mutmut_1': x_set_context_env_vars__mutmut_1, 
    'x_set_context_env_vars__mutmut_2': x_set_context_env_vars__mutmut_2, 
    'x_set_context_env_vars__mutmut_3': x_set_context_env_vars__mutmut_3, 
    'x_set_context_env_vars__mutmut_4': x_set_context_env_vars__mutmut_4, 
    'x_set_context_env_vars__mutmut_5': x_set_context_env_vars__mutmut_5, 
    'x_set_context_env_vars__mutmut_6': x_set_context_env_vars__mutmut_6, 
    'x_set_context_env_vars__mutmut_7': x_set_context_env_vars__mutmut_7, 
    'x_set_context_env_vars__mutmut_8': x_set_context_env_vars__mutmut_8, 
    'x_set_context_env_vars__mutmut_9': x_set_context_env_vars__mutmut_9, 
    'x_set_context_env_vars__mutmut_10': x_set_context_env_vars__mutmut_10, 
    'x_set_context_env_vars__mutmut_11': x_set_context_env_vars__mutmut_11, 
    'x_set_context_env_vars__mutmut_12': x_set_context_env_vars__mutmut_12, 
    'x_set_context_env_vars__mutmut_13': x_set_context_env_vars__mutmut_13, 
    'x_set_context_env_vars__mutmut_14': x_set_context_env_vars__mutmut_14, 
    'x_set_context_env_vars__mutmut_15': x_set_context_env_vars__mutmut_15, 
    'x_set_context_env_vars__mutmut_16': x_set_context_env_vars__mutmut_16, 
    'x_set_context_env_vars__mutmut_17': x_set_context_env_vars__mutmut_17, 
    'x_set_context_env_vars__mutmut_18': x_set_context_env_vars__mutmut_18, 
    'x_set_context_env_vars__mutmut_19': x_set_context_env_vars__mutmut_19, 
    'x_set_context_env_vars__mutmut_20': x_set_context_env_vars__mutmut_20, 
    'x_set_context_env_vars__mutmut_21': x_set_context_env_vars__mutmut_21, 
    'x_set_context_env_vars__mutmut_22': x_set_context_env_vars__mutmut_22, 
    'x_set_context_env_vars__mutmut_23': x_set_context_env_vars__mutmut_23, 
    'x_set_context_env_vars__mutmut_24': x_set_context_env_vars__mutmut_24, 
    'x_set_context_env_vars__mutmut_25': x_set_context_env_vars__mutmut_25, 
    'x_set_context_env_vars__mutmut_26': x_set_context_env_vars__mutmut_26, 
    'x_set_context_env_vars__mutmut_27': x_set_context_env_vars__mutmut_27, 
    'x_set_context_env_vars__mutmut_28': x_set_context_env_vars__mutmut_28, 
    'x_set_context_env_vars__mutmut_29': x_set_context_env_vars__mutmut_29, 
    'x_set_context_env_vars__mutmut_30': x_set_context_env_vars__mutmut_30, 
    'x_set_context_env_vars__mutmut_31': x_set_context_env_vars__mutmut_31, 
    'x_set_context_env_vars__mutmut_32': x_set_context_env_vars__mutmut_32, 
    'x_set_context_env_vars__mutmut_33': x_set_context_env_vars__mutmut_33
}
x_set_context_env_vars__mutmut_orig.__name__ = 'x_set_context_env_vars'


def get_context_env_vars() -> dict[str, str]:
    args = []# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_get_context_env_vars__mutmut_orig, x_get_context_env_vars__mutmut_mutants, args, kwargs, None)


def x_get_context_env_vars__mutmut_orig() -> dict[str, str]:
    """Get current context environment variables.

    Returns:
        Dictionary of context environment variables
    """
    env_vars = {}

    for key in [
        "SPEC_KITTY_CONTEXT",
        "SPEC_KITTY_CWD",
        "SPEC_KITTY_REPO_ROOT",
        "SPEC_KITTY_WORKTREE_NAME",
        "SPEC_KITTY_WORKTREE_PATH",
    ]:
        value = os.environ.get(key)
        if value:
            env_vars[key] = value

    return env_vars


def x_get_context_env_vars__mutmut_1() -> dict[str, str]:
    """Get current context environment variables.

    Returns:
        Dictionary of context environment variables
    """
    env_vars = None

    for key in [
        "SPEC_KITTY_CONTEXT",
        "SPEC_KITTY_CWD",
        "SPEC_KITTY_REPO_ROOT",
        "SPEC_KITTY_WORKTREE_NAME",
        "SPEC_KITTY_WORKTREE_PATH",
    ]:
        value = os.environ.get(key)
        if value:
            env_vars[key] = value

    return env_vars


def x_get_context_env_vars__mutmut_2() -> dict[str, str]:
    """Get current context environment variables.

    Returns:
        Dictionary of context environment variables
    """
    env_vars = {}

    for key in [
        "XXSPEC_KITTY_CONTEXTXX",
        "SPEC_KITTY_CWD",
        "SPEC_KITTY_REPO_ROOT",
        "SPEC_KITTY_WORKTREE_NAME",
        "SPEC_KITTY_WORKTREE_PATH",
    ]:
        value = os.environ.get(key)
        if value:
            env_vars[key] = value

    return env_vars


def x_get_context_env_vars__mutmut_3() -> dict[str, str]:
    """Get current context environment variables.

    Returns:
        Dictionary of context environment variables
    """
    env_vars = {}

    for key in [
        "spec_kitty_context",
        "SPEC_KITTY_CWD",
        "SPEC_KITTY_REPO_ROOT",
        "SPEC_KITTY_WORKTREE_NAME",
        "SPEC_KITTY_WORKTREE_PATH",
    ]:
        value = os.environ.get(key)
        if value:
            env_vars[key] = value

    return env_vars


def x_get_context_env_vars__mutmut_4() -> dict[str, str]:
    """Get current context environment variables.

    Returns:
        Dictionary of context environment variables
    """
    env_vars = {}

    for key in [
        "SPEC_KITTY_CONTEXT",
        "XXSPEC_KITTY_CWDXX",
        "SPEC_KITTY_REPO_ROOT",
        "SPEC_KITTY_WORKTREE_NAME",
        "SPEC_KITTY_WORKTREE_PATH",
    ]:
        value = os.environ.get(key)
        if value:
            env_vars[key] = value

    return env_vars


def x_get_context_env_vars__mutmut_5() -> dict[str, str]:
    """Get current context environment variables.

    Returns:
        Dictionary of context environment variables
    """
    env_vars = {}

    for key in [
        "SPEC_KITTY_CONTEXT",
        "spec_kitty_cwd",
        "SPEC_KITTY_REPO_ROOT",
        "SPEC_KITTY_WORKTREE_NAME",
        "SPEC_KITTY_WORKTREE_PATH",
    ]:
        value = os.environ.get(key)
        if value:
            env_vars[key] = value

    return env_vars


def x_get_context_env_vars__mutmut_6() -> dict[str, str]:
    """Get current context environment variables.

    Returns:
        Dictionary of context environment variables
    """
    env_vars = {}

    for key in [
        "SPEC_KITTY_CONTEXT",
        "SPEC_KITTY_CWD",
        "XXSPEC_KITTY_REPO_ROOTXX",
        "SPEC_KITTY_WORKTREE_NAME",
        "SPEC_KITTY_WORKTREE_PATH",
    ]:
        value = os.environ.get(key)
        if value:
            env_vars[key] = value

    return env_vars


def x_get_context_env_vars__mutmut_7() -> dict[str, str]:
    """Get current context environment variables.

    Returns:
        Dictionary of context environment variables
    """
    env_vars = {}

    for key in [
        "SPEC_KITTY_CONTEXT",
        "SPEC_KITTY_CWD",
        "spec_kitty_repo_root",
        "SPEC_KITTY_WORKTREE_NAME",
        "SPEC_KITTY_WORKTREE_PATH",
    ]:
        value = os.environ.get(key)
        if value:
            env_vars[key] = value

    return env_vars


def x_get_context_env_vars__mutmut_8() -> dict[str, str]:
    """Get current context environment variables.

    Returns:
        Dictionary of context environment variables
    """
    env_vars = {}

    for key in [
        "SPEC_KITTY_CONTEXT",
        "SPEC_KITTY_CWD",
        "SPEC_KITTY_REPO_ROOT",
        "XXSPEC_KITTY_WORKTREE_NAMEXX",
        "SPEC_KITTY_WORKTREE_PATH",
    ]:
        value = os.environ.get(key)
        if value:
            env_vars[key] = value

    return env_vars


def x_get_context_env_vars__mutmut_9() -> dict[str, str]:
    """Get current context environment variables.

    Returns:
        Dictionary of context environment variables
    """
    env_vars = {}

    for key in [
        "SPEC_KITTY_CONTEXT",
        "SPEC_KITTY_CWD",
        "SPEC_KITTY_REPO_ROOT",
        "spec_kitty_worktree_name",
        "SPEC_KITTY_WORKTREE_PATH",
    ]:
        value = os.environ.get(key)
        if value:
            env_vars[key] = value

    return env_vars


def x_get_context_env_vars__mutmut_10() -> dict[str, str]:
    """Get current context environment variables.

    Returns:
        Dictionary of context environment variables
    """
    env_vars = {}

    for key in [
        "SPEC_KITTY_CONTEXT",
        "SPEC_KITTY_CWD",
        "SPEC_KITTY_REPO_ROOT",
        "SPEC_KITTY_WORKTREE_NAME",
        "XXSPEC_KITTY_WORKTREE_PATHXX",
    ]:
        value = os.environ.get(key)
        if value:
            env_vars[key] = value

    return env_vars


def x_get_context_env_vars__mutmut_11() -> dict[str, str]:
    """Get current context environment variables.

    Returns:
        Dictionary of context environment variables
    """
    env_vars = {}

    for key in [
        "SPEC_KITTY_CONTEXT",
        "SPEC_KITTY_CWD",
        "SPEC_KITTY_REPO_ROOT",
        "SPEC_KITTY_WORKTREE_NAME",
        "spec_kitty_worktree_path",
    ]:
        value = os.environ.get(key)
        if value:
            env_vars[key] = value

    return env_vars


def x_get_context_env_vars__mutmut_12() -> dict[str, str]:
    """Get current context environment variables.

    Returns:
        Dictionary of context environment variables
    """
    env_vars = {}

    for key in [
        "SPEC_KITTY_CONTEXT",
        "SPEC_KITTY_CWD",
        "SPEC_KITTY_REPO_ROOT",
        "SPEC_KITTY_WORKTREE_NAME",
        "SPEC_KITTY_WORKTREE_PATH",
    ]:
        value = None
        if value:
            env_vars[key] = value

    return env_vars


def x_get_context_env_vars__mutmut_13() -> dict[str, str]:
    """Get current context environment variables.

    Returns:
        Dictionary of context environment variables
    """
    env_vars = {}

    for key in [
        "SPEC_KITTY_CONTEXT",
        "SPEC_KITTY_CWD",
        "SPEC_KITTY_REPO_ROOT",
        "SPEC_KITTY_WORKTREE_NAME",
        "SPEC_KITTY_WORKTREE_PATH",
    ]:
        value = os.environ.get(None)
        if value:
            env_vars[key] = value

    return env_vars


def x_get_context_env_vars__mutmut_14() -> dict[str, str]:
    """Get current context environment variables.

    Returns:
        Dictionary of context environment variables
    """
    env_vars = {}

    for key in [
        "SPEC_KITTY_CONTEXT",
        "SPEC_KITTY_CWD",
        "SPEC_KITTY_REPO_ROOT",
        "SPEC_KITTY_WORKTREE_NAME",
        "SPEC_KITTY_WORKTREE_PATH",
    ]:
        value = os.environ.get(key)
        if value:
            env_vars[key] = None

    return env_vars

x_get_context_env_vars__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_get_context_env_vars__mutmut_1': x_get_context_env_vars__mutmut_1, 
    'x_get_context_env_vars__mutmut_2': x_get_context_env_vars__mutmut_2, 
    'x_get_context_env_vars__mutmut_3': x_get_context_env_vars__mutmut_3, 
    'x_get_context_env_vars__mutmut_4': x_get_context_env_vars__mutmut_4, 
    'x_get_context_env_vars__mutmut_5': x_get_context_env_vars__mutmut_5, 
    'x_get_context_env_vars__mutmut_6': x_get_context_env_vars__mutmut_6, 
    'x_get_context_env_vars__mutmut_7': x_get_context_env_vars__mutmut_7, 
    'x_get_context_env_vars__mutmut_8': x_get_context_env_vars__mutmut_8, 
    'x_get_context_env_vars__mutmut_9': x_get_context_env_vars__mutmut_9, 
    'x_get_context_env_vars__mutmut_10': x_get_context_env_vars__mutmut_10, 
    'x_get_context_env_vars__mutmut_11': x_get_context_env_vars__mutmut_11, 
    'x_get_context_env_vars__mutmut_12': x_get_context_env_vars__mutmut_12, 
    'x_get_context_env_vars__mutmut_13': x_get_context_env_vars__mutmut_13, 
    'x_get_context_env_vars__mutmut_14': x_get_context_env_vars__mutmut_14
}
x_get_context_env_vars__mutmut_orig.__name__ = 'x_get_context_env_vars'


__all__ = [
    "ExecutionContext",
    "CurrentContext",
    "detect_execution_context",
    "get_current_context",
    "require_main_repo",
    "require_worktree",
    "require_either",
    "set_context_env_vars",
    "get_context_env_vars",
]
