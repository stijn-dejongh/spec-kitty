"""
Stale Work Package Detection
============================

Detects work packages that are in "doing" lane but have no recent VCS activity,
indicating the agent may have stopped without transitioning the WP.

Uses git/jj commit timestamps as a "heartbeat" - if no commits for a threshold
period, the WP is considered stale.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from specify_cli.core.vcs import get_vcs, VCSError
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


@dataclass
class StaleCheckResult:
    """Result of checking a work package for staleness."""

    wp_id: str
    is_stale: bool
    last_commit_time: datetime | None
    minutes_since_commit: float | None
    worktree_exists: bool
    error: str | None = None


def get_default_branch(repo_path: Path) -> str:
    args = [repo_path]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_get_default_branch__mutmut_orig, x_get_default_branch__mutmut_mutants, args, kwargs, None)


def x_get_default_branch__mutmut_orig(repo_path: Path) -> str:
    """
    Get the default/base branch name for the repository (for stale detection).

    This is used to find the branch that feature branches diverged FROM.
    Unlike resolve_primary_branch() in git_ops, this does NOT use the current
    branch because stale detection always runs from worktrees where the current
    branch is always the feature branch, never the base branch.

    Tries multiple methods to detect the default branch:
    1. Check origin's HEAD symbolic ref
    2. Check which common branch exists (main, master, develop)
    3. Fallback to "main"

    Args:
        repo_path: Path to the repository

    Returns:
        Default branch name (e.g., "main", "master", "develop")
    """
    import subprocess

    # Method 1: Get from origin's HEAD
    result = subprocess.run(
        ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
        cwd=repo_path,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=5,
    )

    if result.returncode == 0:
        # Output: "refs/remotes/origin/main" → extract "main"
        ref = result.stdout.strip()
        return ref.split("/")[-1]

    # Method 2: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        result = subprocess.run(
            ["git", "rev-parse", "--verify", branch],
            cwd=repo_path,
            capture_output=True,
            timeout=5,
        )
        if result.returncode == 0:
            return branch

    # Method 3: Fallback
    return "main"


def x_get_default_branch__mutmut_1(repo_path: Path) -> str:
    """
    Get the default/base branch name for the repository (for stale detection).

    This is used to find the branch that feature branches diverged FROM.
    Unlike resolve_primary_branch() in git_ops, this does NOT use the current
    branch because stale detection always runs from worktrees where the current
    branch is always the feature branch, never the base branch.

    Tries multiple methods to detect the default branch:
    1. Check origin's HEAD symbolic ref
    2. Check which common branch exists (main, master, develop)
    3. Fallback to "main"

    Args:
        repo_path: Path to the repository

    Returns:
        Default branch name (e.g., "main", "master", "develop")
    """
    import subprocess

    # Method 1: Get from origin's HEAD
    result = None

    if result.returncode == 0:
        # Output: "refs/remotes/origin/main" → extract "main"
        ref = result.stdout.strip()
        return ref.split("/")[-1]

    # Method 2: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        result = subprocess.run(
            ["git", "rev-parse", "--verify", branch],
            cwd=repo_path,
            capture_output=True,
            timeout=5,
        )
        if result.returncode == 0:
            return branch

    # Method 3: Fallback
    return "main"


def x_get_default_branch__mutmut_2(repo_path: Path) -> str:
    """
    Get the default/base branch name for the repository (for stale detection).

    This is used to find the branch that feature branches diverged FROM.
    Unlike resolve_primary_branch() in git_ops, this does NOT use the current
    branch because stale detection always runs from worktrees where the current
    branch is always the feature branch, never the base branch.

    Tries multiple methods to detect the default branch:
    1. Check origin's HEAD symbolic ref
    2. Check which common branch exists (main, master, develop)
    3. Fallback to "main"

    Args:
        repo_path: Path to the repository

    Returns:
        Default branch name (e.g., "main", "master", "develop")
    """
    import subprocess

    # Method 1: Get from origin's HEAD
    result = subprocess.run(
        None,
        cwd=repo_path,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=5,
    )

    if result.returncode == 0:
        # Output: "refs/remotes/origin/main" → extract "main"
        ref = result.stdout.strip()
        return ref.split("/")[-1]

    # Method 2: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        result = subprocess.run(
            ["git", "rev-parse", "--verify", branch],
            cwd=repo_path,
            capture_output=True,
            timeout=5,
        )
        if result.returncode == 0:
            return branch

    # Method 3: Fallback
    return "main"


def x_get_default_branch__mutmut_3(repo_path: Path) -> str:
    """
    Get the default/base branch name for the repository (for stale detection).

    This is used to find the branch that feature branches diverged FROM.
    Unlike resolve_primary_branch() in git_ops, this does NOT use the current
    branch because stale detection always runs from worktrees where the current
    branch is always the feature branch, never the base branch.

    Tries multiple methods to detect the default branch:
    1. Check origin's HEAD symbolic ref
    2. Check which common branch exists (main, master, develop)
    3. Fallback to "main"

    Args:
        repo_path: Path to the repository

    Returns:
        Default branch name (e.g., "main", "master", "develop")
    """
    import subprocess

    # Method 1: Get from origin's HEAD
    result = subprocess.run(
        ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
        cwd=None,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=5,
    )

    if result.returncode == 0:
        # Output: "refs/remotes/origin/main" → extract "main"
        ref = result.stdout.strip()
        return ref.split("/")[-1]

    # Method 2: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        result = subprocess.run(
            ["git", "rev-parse", "--verify", branch],
            cwd=repo_path,
            capture_output=True,
            timeout=5,
        )
        if result.returncode == 0:
            return branch

    # Method 3: Fallback
    return "main"


def x_get_default_branch__mutmut_4(repo_path: Path) -> str:
    """
    Get the default/base branch name for the repository (for stale detection).

    This is used to find the branch that feature branches diverged FROM.
    Unlike resolve_primary_branch() in git_ops, this does NOT use the current
    branch because stale detection always runs from worktrees where the current
    branch is always the feature branch, never the base branch.

    Tries multiple methods to detect the default branch:
    1. Check origin's HEAD symbolic ref
    2. Check which common branch exists (main, master, develop)
    3. Fallback to "main"

    Args:
        repo_path: Path to the repository

    Returns:
        Default branch name (e.g., "main", "master", "develop")
    """
    import subprocess

    # Method 1: Get from origin's HEAD
    result = subprocess.run(
        ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
        cwd=repo_path,
        capture_output=None,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=5,
    )

    if result.returncode == 0:
        # Output: "refs/remotes/origin/main" → extract "main"
        ref = result.stdout.strip()
        return ref.split("/")[-1]

    # Method 2: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        result = subprocess.run(
            ["git", "rev-parse", "--verify", branch],
            cwd=repo_path,
            capture_output=True,
            timeout=5,
        )
        if result.returncode == 0:
            return branch

    # Method 3: Fallback
    return "main"


def x_get_default_branch__mutmut_5(repo_path: Path) -> str:
    """
    Get the default/base branch name for the repository (for stale detection).

    This is used to find the branch that feature branches diverged FROM.
    Unlike resolve_primary_branch() in git_ops, this does NOT use the current
    branch because stale detection always runs from worktrees where the current
    branch is always the feature branch, never the base branch.

    Tries multiple methods to detect the default branch:
    1. Check origin's HEAD symbolic ref
    2. Check which common branch exists (main, master, develop)
    3. Fallback to "main"

    Args:
        repo_path: Path to the repository

    Returns:
        Default branch name (e.g., "main", "master", "develop")
    """
    import subprocess

    # Method 1: Get from origin's HEAD
    result = subprocess.run(
        ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
        cwd=repo_path,
        capture_output=True,
        text=None,
        encoding="utf-8",
        errors="replace",
        timeout=5,
    )

    if result.returncode == 0:
        # Output: "refs/remotes/origin/main" → extract "main"
        ref = result.stdout.strip()
        return ref.split("/")[-1]

    # Method 2: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        result = subprocess.run(
            ["git", "rev-parse", "--verify", branch],
            cwd=repo_path,
            capture_output=True,
            timeout=5,
        )
        if result.returncode == 0:
            return branch

    # Method 3: Fallback
    return "main"


def x_get_default_branch__mutmut_6(repo_path: Path) -> str:
    """
    Get the default/base branch name for the repository (for stale detection).

    This is used to find the branch that feature branches diverged FROM.
    Unlike resolve_primary_branch() in git_ops, this does NOT use the current
    branch because stale detection always runs from worktrees where the current
    branch is always the feature branch, never the base branch.

    Tries multiple methods to detect the default branch:
    1. Check origin's HEAD symbolic ref
    2. Check which common branch exists (main, master, develop)
    3. Fallback to "main"

    Args:
        repo_path: Path to the repository

    Returns:
        Default branch name (e.g., "main", "master", "develop")
    """
    import subprocess

    # Method 1: Get from origin's HEAD
    result = subprocess.run(
        ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
        cwd=repo_path,
        capture_output=True,
        text=True,
        encoding=None,
        errors="replace",
        timeout=5,
    )

    if result.returncode == 0:
        # Output: "refs/remotes/origin/main" → extract "main"
        ref = result.stdout.strip()
        return ref.split("/")[-1]

    # Method 2: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        result = subprocess.run(
            ["git", "rev-parse", "--verify", branch],
            cwd=repo_path,
            capture_output=True,
            timeout=5,
        )
        if result.returncode == 0:
            return branch

    # Method 3: Fallback
    return "main"


def x_get_default_branch__mutmut_7(repo_path: Path) -> str:
    """
    Get the default/base branch name for the repository (for stale detection).

    This is used to find the branch that feature branches diverged FROM.
    Unlike resolve_primary_branch() in git_ops, this does NOT use the current
    branch because stale detection always runs from worktrees where the current
    branch is always the feature branch, never the base branch.

    Tries multiple methods to detect the default branch:
    1. Check origin's HEAD symbolic ref
    2. Check which common branch exists (main, master, develop)
    3. Fallback to "main"

    Args:
        repo_path: Path to the repository

    Returns:
        Default branch name (e.g., "main", "master", "develop")
    """
    import subprocess

    # Method 1: Get from origin's HEAD
    result = subprocess.run(
        ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
        cwd=repo_path,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors=None,
        timeout=5,
    )

    if result.returncode == 0:
        # Output: "refs/remotes/origin/main" → extract "main"
        ref = result.stdout.strip()
        return ref.split("/")[-1]

    # Method 2: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        result = subprocess.run(
            ["git", "rev-parse", "--verify", branch],
            cwd=repo_path,
            capture_output=True,
            timeout=5,
        )
        if result.returncode == 0:
            return branch

    # Method 3: Fallback
    return "main"


def x_get_default_branch__mutmut_8(repo_path: Path) -> str:
    """
    Get the default/base branch name for the repository (for stale detection).

    This is used to find the branch that feature branches diverged FROM.
    Unlike resolve_primary_branch() in git_ops, this does NOT use the current
    branch because stale detection always runs from worktrees where the current
    branch is always the feature branch, never the base branch.

    Tries multiple methods to detect the default branch:
    1. Check origin's HEAD symbolic ref
    2. Check which common branch exists (main, master, develop)
    3. Fallback to "main"

    Args:
        repo_path: Path to the repository

    Returns:
        Default branch name (e.g., "main", "master", "develop")
    """
    import subprocess

    # Method 1: Get from origin's HEAD
    result = subprocess.run(
        ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
        cwd=repo_path,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=None,
    )

    if result.returncode == 0:
        # Output: "refs/remotes/origin/main" → extract "main"
        ref = result.stdout.strip()
        return ref.split("/")[-1]

    # Method 2: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        result = subprocess.run(
            ["git", "rev-parse", "--verify", branch],
            cwd=repo_path,
            capture_output=True,
            timeout=5,
        )
        if result.returncode == 0:
            return branch

    # Method 3: Fallback
    return "main"


def x_get_default_branch__mutmut_9(repo_path: Path) -> str:
    """
    Get the default/base branch name for the repository (for stale detection).

    This is used to find the branch that feature branches diverged FROM.
    Unlike resolve_primary_branch() in git_ops, this does NOT use the current
    branch because stale detection always runs from worktrees where the current
    branch is always the feature branch, never the base branch.

    Tries multiple methods to detect the default branch:
    1. Check origin's HEAD symbolic ref
    2. Check which common branch exists (main, master, develop)
    3. Fallback to "main"

    Args:
        repo_path: Path to the repository

    Returns:
        Default branch name (e.g., "main", "master", "develop")
    """
    import subprocess

    # Method 1: Get from origin's HEAD
    result = subprocess.run(
        cwd=repo_path,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=5,
    )

    if result.returncode == 0:
        # Output: "refs/remotes/origin/main" → extract "main"
        ref = result.stdout.strip()
        return ref.split("/")[-1]

    # Method 2: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        result = subprocess.run(
            ["git", "rev-parse", "--verify", branch],
            cwd=repo_path,
            capture_output=True,
            timeout=5,
        )
        if result.returncode == 0:
            return branch

    # Method 3: Fallback
    return "main"


def x_get_default_branch__mutmut_10(repo_path: Path) -> str:
    """
    Get the default/base branch name for the repository (for stale detection).

    This is used to find the branch that feature branches diverged FROM.
    Unlike resolve_primary_branch() in git_ops, this does NOT use the current
    branch because stale detection always runs from worktrees where the current
    branch is always the feature branch, never the base branch.

    Tries multiple methods to detect the default branch:
    1. Check origin's HEAD symbolic ref
    2. Check which common branch exists (main, master, develop)
    3. Fallback to "main"

    Args:
        repo_path: Path to the repository

    Returns:
        Default branch name (e.g., "main", "master", "develop")
    """
    import subprocess

    # Method 1: Get from origin's HEAD
    result = subprocess.run(
        ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=5,
    )

    if result.returncode == 0:
        # Output: "refs/remotes/origin/main" → extract "main"
        ref = result.stdout.strip()
        return ref.split("/")[-1]

    # Method 2: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        result = subprocess.run(
            ["git", "rev-parse", "--verify", branch],
            cwd=repo_path,
            capture_output=True,
            timeout=5,
        )
        if result.returncode == 0:
            return branch

    # Method 3: Fallback
    return "main"


def x_get_default_branch__mutmut_11(repo_path: Path) -> str:
    """
    Get the default/base branch name for the repository (for stale detection).

    This is used to find the branch that feature branches diverged FROM.
    Unlike resolve_primary_branch() in git_ops, this does NOT use the current
    branch because stale detection always runs from worktrees where the current
    branch is always the feature branch, never the base branch.

    Tries multiple methods to detect the default branch:
    1. Check origin's HEAD symbolic ref
    2. Check which common branch exists (main, master, develop)
    3. Fallback to "main"

    Args:
        repo_path: Path to the repository

    Returns:
        Default branch name (e.g., "main", "master", "develop")
    """
    import subprocess

    # Method 1: Get from origin's HEAD
    result = subprocess.run(
        ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
        cwd=repo_path,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=5,
    )

    if result.returncode == 0:
        # Output: "refs/remotes/origin/main" → extract "main"
        ref = result.stdout.strip()
        return ref.split("/")[-1]

    # Method 2: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        result = subprocess.run(
            ["git", "rev-parse", "--verify", branch],
            cwd=repo_path,
            capture_output=True,
            timeout=5,
        )
        if result.returncode == 0:
            return branch

    # Method 3: Fallback
    return "main"


def x_get_default_branch__mutmut_12(repo_path: Path) -> str:
    """
    Get the default/base branch name for the repository (for stale detection).

    This is used to find the branch that feature branches diverged FROM.
    Unlike resolve_primary_branch() in git_ops, this does NOT use the current
    branch because stale detection always runs from worktrees where the current
    branch is always the feature branch, never the base branch.

    Tries multiple methods to detect the default branch:
    1. Check origin's HEAD symbolic ref
    2. Check which common branch exists (main, master, develop)
    3. Fallback to "main"

    Args:
        repo_path: Path to the repository

    Returns:
        Default branch name (e.g., "main", "master", "develop")
    """
    import subprocess

    # Method 1: Get from origin's HEAD
    result = subprocess.run(
        ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
        cwd=repo_path,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        timeout=5,
    )

    if result.returncode == 0:
        # Output: "refs/remotes/origin/main" → extract "main"
        ref = result.stdout.strip()
        return ref.split("/")[-1]

    # Method 2: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        result = subprocess.run(
            ["git", "rev-parse", "--verify", branch],
            cwd=repo_path,
            capture_output=True,
            timeout=5,
        )
        if result.returncode == 0:
            return branch

    # Method 3: Fallback
    return "main"


def x_get_default_branch__mutmut_13(repo_path: Path) -> str:
    """
    Get the default/base branch name for the repository (for stale detection).

    This is used to find the branch that feature branches diverged FROM.
    Unlike resolve_primary_branch() in git_ops, this does NOT use the current
    branch because stale detection always runs from worktrees where the current
    branch is always the feature branch, never the base branch.

    Tries multiple methods to detect the default branch:
    1. Check origin's HEAD symbolic ref
    2. Check which common branch exists (main, master, develop)
    3. Fallback to "main"

    Args:
        repo_path: Path to the repository

    Returns:
        Default branch name (e.g., "main", "master", "develop")
    """
    import subprocess

    # Method 1: Get from origin's HEAD
    result = subprocess.run(
        ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
        cwd=repo_path,
        capture_output=True,
        text=True,
        errors="replace",
        timeout=5,
    )

    if result.returncode == 0:
        # Output: "refs/remotes/origin/main" → extract "main"
        ref = result.stdout.strip()
        return ref.split("/")[-1]

    # Method 2: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        result = subprocess.run(
            ["git", "rev-parse", "--verify", branch],
            cwd=repo_path,
            capture_output=True,
            timeout=5,
        )
        if result.returncode == 0:
            return branch

    # Method 3: Fallback
    return "main"


def x_get_default_branch__mutmut_14(repo_path: Path) -> str:
    """
    Get the default/base branch name for the repository (for stale detection).

    This is used to find the branch that feature branches diverged FROM.
    Unlike resolve_primary_branch() in git_ops, this does NOT use the current
    branch because stale detection always runs from worktrees where the current
    branch is always the feature branch, never the base branch.

    Tries multiple methods to detect the default branch:
    1. Check origin's HEAD symbolic ref
    2. Check which common branch exists (main, master, develop)
    3. Fallback to "main"

    Args:
        repo_path: Path to the repository

    Returns:
        Default branch name (e.g., "main", "master", "develop")
    """
    import subprocess

    # Method 1: Get from origin's HEAD
    result = subprocess.run(
        ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
        cwd=repo_path,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=5,
    )

    if result.returncode == 0:
        # Output: "refs/remotes/origin/main" → extract "main"
        ref = result.stdout.strip()
        return ref.split("/")[-1]

    # Method 2: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        result = subprocess.run(
            ["git", "rev-parse", "--verify", branch],
            cwd=repo_path,
            capture_output=True,
            timeout=5,
        )
        if result.returncode == 0:
            return branch

    # Method 3: Fallback
    return "main"


def x_get_default_branch__mutmut_15(repo_path: Path) -> str:
    """
    Get the default/base branch name for the repository (for stale detection).

    This is used to find the branch that feature branches diverged FROM.
    Unlike resolve_primary_branch() in git_ops, this does NOT use the current
    branch because stale detection always runs from worktrees where the current
    branch is always the feature branch, never the base branch.

    Tries multiple methods to detect the default branch:
    1. Check origin's HEAD symbolic ref
    2. Check which common branch exists (main, master, develop)
    3. Fallback to "main"

    Args:
        repo_path: Path to the repository

    Returns:
        Default branch name (e.g., "main", "master", "develop")
    """
    import subprocess

    # Method 1: Get from origin's HEAD
    result = subprocess.run(
        ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
        cwd=repo_path,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        )

    if result.returncode == 0:
        # Output: "refs/remotes/origin/main" → extract "main"
        ref = result.stdout.strip()
        return ref.split("/")[-1]

    # Method 2: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        result = subprocess.run(
            ["git", "rev-parse", "--verify", branch],
            cwd=repo_path,
            capture_output=True,
            timeout=5,
        )
        if result.returncode == 0:
            return branch

    # Method 3: Fallback
    return "main"


def x_get_default_branch__mutmut_16(repo_path: Path) -> str:
    """
    Get the default/base branch name for the repository (for stale detection).

    This is used to find the branch that feature branches diverged FROM.
    Unlike resolve_primary_branch() in git_ops, this does NOT use the current
    branch because stale detection always runs from worktrees where the current
    branch is always the feature branch, never the base branch.

    Tries multiple methods to detect the default branch:
    1. Check origin's HEAD symbolic ref
    2. Check which common branch exists (main, master, develop)
    3. Fallback to "main"

    Args:
        repo_path: Path to the repository

    Returns:
        Default branch name (e.g., "main", "master", "develop")
    """
    import subprocess

    # Method 1: Get from origin's HEAD
    result = subprocess.run(
        ["XXgitXX", "symbolic-ref", "refs/remotes/origin/HEAD"],
        cwd=repo_path,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=5,
    )

    if result.returncode == 0:
        # Output: "refs/remotes/origin/main" → extract "main"
        ref = result.stdout.strip()
        return ref.split("/")[-1]

    # Method 2: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        result = subprocess.run(
            ["git", "rev-parse", "--verify", branch],
            cwd=repo_path,
            capture_output=True,
            timeout=5,
        )
        if result.returncode == 0:
            return branch

    # Method 3: Fallback
    return "main"


def x_get_default_branch__mutmut_17(repo_path: Path) -> str:
    """
    Get the default/base branch name for the repository (for stale detection).

    This is used to find the branch that feature branches diverged FROM.
    Unlike resolve_primary_branch() in git_ops, this does NOT use the current
    branch because stale detection always runs from worktrees where the current
    branch is always the feature branch, never the base branch.

    Tries multiple methods to detect the default branch:
    1. Check origin's HEAD symbolic ref
    2. Check which common branch exists (main, master, develop)
    3. Fallback to "main"

    Args:
        repo_path: Path to the repository

    Returns:
        Default branch name (e.g., "main", "master", "develop")
    """
    import subprocess

    # Method 1: Get from origin's HEAD
    result = subprocess.run(
        ["GIT", "symbolic-ref", "refs/remotes/origin/HEAD"],
        cwd=repo_path,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=5,
    )

    if result.returncode == 0:
        # Output: "refs/remotes/origin/main" → extract "main"
        ref = result.stdout.strip()
        return ref.split("/")[-1]

    # Method 2: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        result = subprocess.run(
            ["git", "rev-parse", "--verify", branch],
            cwd=repo_path,
            capture_output=True,
            timeout=5,
        )
        if result.returncode == 0:
            return branch

    # Method 3: Fallback
    return "main"


def x_get_default_branch__mutmut_18(repo_path: Path) -> str:
    """
    Get the default/base branch name for the repository (for stale detection).

    This is used to find the branch that feature branches diverged FROM.
    Unlike resolve_primary_branch() in git_ops, this does NOT use the current
    branch because stale detection always runs from worktrees where the current
    branch is always the feature branch, never the base branch.

    Tries multiple methods to detect the default branch:
    1. Check origin's HEAD symbolic ref
    2. Check which common branch exists (main, master, develop)
    3. Fallback to "main"

    Args:
        repo_path: Path to the repository

    Returns:
        Default branch name (e.g., "main", "master", "develop")
    """
    import subprocess

    # Method 1: Get from origin's HEAD
    result = subprocess.run(
        ["git", "XXsymbolic-refXX", "refs/remotes/origin/HEAD"],
        cwd=repo_path,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=5,
    )

    if result.returncode == 0:
        # Output: "refs/remotes/origin/main" → extract "main"
        ref = result.stdout.strip()
        return ref.split("/")[-1]

    # Method 2: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        result = subprocess.run(
            ["git", "rev-parse", "--verify", branch],
            cwd=repo_path,
            capture_output=True,
            timeout=5,
        )
        if result.returncode == 0:
            return branch

    # Method 3: Fallback
    return "main"


def x_get_default_branch__mutmut_19(repo_path: Path) -> str:
    """
    Get the default/base branch name for the repository (for stale detection).

    This is used to find the branch that feature branches diverged FROM.
    Unlike resolve_primary_branch() in git_ops, this does NOT use the current
    branch because stale detection always runs from worktrees where the current
    branch is always the feature branch, never the base branch.

    Tries multiple methods to detect the default branch:
    1. Check origin's HEAD symbolic ref
    2. Check which common branch exists (main, master, develop)
    3. Fallback to "main"

    Args:
        repo_path: Path to the repository

    Returns:
        Default branch name (e.g., "main", "master", "develop")
    """
    import subprocess

    # Method 1: Get from origin's HEAD
    result = subprocess.run(
        ["git", "SYMBOLIC-REF", "refs/remotes/origin/HEAD"],
        cwd=repo_path,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=5,
    )

    if result.returncode == 0:
        # Output: "refs/remotes/origin/main" → extract "main"
        ref = result.stdout.strip()
        return ref.split("/")[-1]

    # Method 2: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        result = subprocess.run(
            ["git", "rev-parse", "--verify", branch],
            cwd=repo_path,
            capture_output=True,
            timeout=5,
        )
        if result.returncode == 0:
            return branch

    # Method 3: Fallback
    return "main"


def x_get_default_branch__mutmut_20(repo_path: Path) -> str:
    """
    Get the default/base branch name for the repository (for stale detection).

    This is used to find the branch that feature branches diverged FROM.
    Unlike resolve_primary_branch() in git_ops, this does NOT use the current
    branch because stale detection always runs from worktrees where the current
    branch is always the feature branch, never the base branch.

    Tries multiple methods to detect the default branch:
    1. Check origin's HEAD symbolic ref
    2. Check which common branch exists (main, master, develop)
    3. Fallback to "main"

    Args:
        repo_path: Path to the repository

    Returns:
        Default branch name (e.g., "main", "master", "develop")
    """
    import subprocess

    # Method 1: Get from origin's HEAD
    result = subprocess.run(
        ["git", "symbolic-ref", "XXrefs/remotes/origin/HEADXX"],
        cwd=repo_path,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=5,
    )

    if result.returncode == 0:
        # Output: "refs/remotes/origin/main" → extract "main"
        ref = result.stdout.strip()
        return ref.split("/")[-1]

    # Method 2: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        result = subprocess.run(
            ["git", "rev-parse", "--verify", branch],
            cwd=repo_path,
            capture_output=True,
            timeout=5,
        )
        if result.returncode == 0:
            return branch

    # Method 3: Fallback
    return "main"


def x_get_default_branch__mutmut_21(repo_path: Path) -> str:
    """
    Get the default/base branch name for the repository (for stale detection).

    This is used to find the branch that feature branches diverged FROM.
    Unlike resolve_primary_branch() in git_ops, this does NOT use the current
    branch because stale detection always runs from worktrees where the current
    branch is always the feature branch, never the base branch.

    Tries multiple methods to detect the default branch:
    1. Check origin's HEAD symbolic ref
    2. Check which common branch exists (main, master, develop)
    3. Fallback to "main"

    Args:
        repo_path: Path to the repository

    Returns:
        Default branch name (e.g., "main", "master", "develop")
    """
    import subprocess

    # Method 1: Get from origin's HEAD
    result = subprocess.run(
        ["git", "symbolic-ref", "refs/remotes/origin/head"],
        cwd=repo_path,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=5,
    )

    if result.returncode == 0:
        # Output: "refs/remotes/origin/main" → extract "main"
        ref = result.stdout.strip()
        return ref.split("/")[-1]

    # Method 2: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        result = subprocess.run(
            ["git", "rev-parse", "--verify", branch],
            cwd=repo_path,
            capture_output=True,
            timeout=5,
        )
        if result.returncode == 0:
            return branch

    # Method 3: Fallback
    return "main"


def x_get_default_branch__mutmut_22(repo_path: Path) -> str:
    """
    Get the default/base branch name for the repository (for stale detection).

    This is used to find the branch that feature branches diverged FROM.
    Unlike resolve_primary_branch() in git_ops, this does NOT use the current
    branch because stale detection always runs from worktrees where the current
    branch is always the feature branch, never the base branch.

    Tries multiple methods to detect the default branch:
    1. Check origin's HEAD symbolic ref
    2. Check which common branch exists (main, master, develop)
    3. Fallback to "main"

    Args:
        repo_path: Path to the repository

    Returns:
        Default branch name (e.g., "main", "master", "develop")
    """
    import subprocess

    # Method 1: Get from origin's HEAD
    result = subprocess.run(
        ["git", "symbolic-ref", "REFS/REMOTES/ORIGIN/HEAD"],
        cwd=repo_path,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=5,
    )

    if result.returncode == 0:
        # Output: "refs/remotes/origin/main" → extract "main"
        ref = result.stdout.strip()
        return ref.split("/")[-1]

    # Method 2: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        result = subprocess.run(
            ["git", "rev-parse", "--verify", branch],
            cwd=repo_path,
            capture_output=True,
            timeout=5,
        )
        if result.returncode == 0:
            return branch

    # Method 3: Fallback
    return "main"


def x_get_default_branch__mutmut_23(repo_path: Path) -> str:
    """
    Get the default/base branch name for the repository (for stale detection).

    This is used to find the branch that feature branches diverged FROM.
    Unlike resolve_primary_branch() in git_ops, this does NOT use the current
    branch because stale detection always runs from worktrees where the current
    branch is always the feature branch, never the base branch.

    Tries multiple methods to detect the default branch:
    1. Check origin's HEAD symbolic ref
    2. Check which common branch exists (main, master, develop)
    3. Fallback to "main"

    Args:
        repo_path: Path to the repository

    Returns:
        Default branch name (e.g., "main", "master", "develop")
    """
    import subprocess

    # Method 1: Get from origin's HEAD
    result = subprocess.run(
        ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
        cwd=repo_path,
        capture_output=False,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=5,
    )

    if result.returncode == 0:
        # Output: "refs/remotes/origin/main" → extract "main"
        ref = result.stdout.strip()
        return ref.split("/")[-1]

    # Method 2: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        result = subprocess.run(
            ["git", "rev-parse", "--verify", branch],
            cwd=repo_path,
            capture_output=True,
            timeout=5,
        )
        if result.returncode == 0:
            return branch

    # Method 3: Fallback
    return "main"


def x_get_default_branch__mutmut_24(repo_path: Path) -> str:
    """
    Get the default/base branch name for the repository (for stale detection).

    This is used to find the branch that feature branches diverged FROM.
    Unlike resolve_primary_branch() in git_ops, this does NOT use the current
    branch because stale detection always runs from worktrees where the current
    branch is always the feature branch, never the base branch.

    Tries multiple methods to detect the default branch:
    1. Check origin's HEAD symbolic ref
    2. Check which common branch exists (main, master, develop)
    3. Fallback to "main"

    Args:
        repo_path: Path to the repository

    Returns:
        Default branch name (e.g., "main", "master", "develop")
    """
    import subprocess

    # Method 1: Get from origin's HEAD
    result = subprocess.run(
        ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
        cwd=repo_path,
        capture_output=True,
        text=False,
        encoding="utf-8",
        errors="replace",
        timeout=5,
    )

    if result.returncode == 0:
        # Output: "refs/remotes/origin/main" → extract "main"
        ref = result.stdout.strip()
        return ref.split("/")[-1]

    # Method 2: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        result = subprocess.run(
            ["git", "rev-parse", "--verify", branch],
            cwd=repo_path,
            capture_output=True,
            timeout=5,
        )
        if result.returncode == 0:
            return branch

    # Method 3: Fallback
    return "main"


def x_get_default_branch__mutmut_25(repo_path: Path) -> str:
    """
    Get the default/base branch name for the repository (for stale detection).

    This is used to find the branch that feature branches diverged FROM.
    Unlike resolve_primary_branch() in git_ops, this does NOT use the current
    branch because stale detection always runs from worktrees where the current
    branch is always the feature branch, never the base branch.

    Tries multiple methods to detect the default branch:
    1. Check origin's HEAD symbolic ref
    2. Check which common branch exists (main, master, develop)
    3. Fallback to "main"

    Args:
        repo_path: Path to the repository

    Returns:
        Default branch name (e.g., "main", "master", "develop")
    """
    import subprocess

    # Method 1: Get from origin's HEAD
    result = subprocess.run(
        ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
        cwd=repo_path,
        capture_output=True,
        text=True,
        encoding="XXutf-8XX",
        errors="replace",
        timeout=5,
    )

    if result.returncode == 0:
        # Output: "refs/remotes/origin/main" → extract "main"
        ref = result.stdout.strip()
        return ref.split("/")[-1]

    # Method 2: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        result = subprocess.run(
            ["git", "rev-parse", "--verify", branch],
            cwd=repo_path,
            capture_output=True,
            timeout=5,
        )
        if result.returncode == 0:
            return branch

    # Method 3: Fallback
    return "main"


def x_get_default_branch__mutmut_26(repo_path: Path) -> str:
    """
    Get the default/base branch name for the repository (for stale detection).

    This is used to find the branch that feature branches diverged FROM.
    Unlike resolve_primary_branch() in git_ops, this does NOT use the current
    branch because stale detection always runs from worktrees where the current
    branch is always the feature branch, never the base branch.

    Tries multiple methods to detect the default branch:
    1. Check origin's HEAD symbolic ref
    2. Check which common branch exists (main, master, develop)
    3. Fallback to "main"

    Args:
        repo_path: Path to the repository

    Returns:
        Default branch name (e.g., "main", "master", "develop")
    """
    import subprocess

    # Method 1: Get from origin's HEAD
    result = subprocess.run(
        ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
        cwd=repo_path,
        capture_output=True,
        text=True,
        encoding="UTF-8",
        errors="replace",
        timeout=5,
    )

    if result.returncode == 0:
        # Output: "refs/remotes/origin/main" → extract "main"
        ref = result.stdout.strip()
        return ref.split("/")[-1]

    # Method 2: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        result = subprocess.run(
            ["git", "rev-parse", "--verify", branch],
            cwd=repo_path,
            capture_output=True,
            timeout=5,
        )
        if result.returncode == 0:
            return branch

    # Method 3: Fallback
    return "main"


def x_get_default_branch__mutmut_27(repo_path: Path) -> str:
    """
    Get the default/base branch name for the repository (for stale detection).

    This is used to find the branch that feature branches diverged FROM.
    Unlike resolve_primary_branch() in git_ops, this does NOT use the current
    branch because stale detection always runs from worktrees where the current
    branch is always the feature branch, never the base branch.

    Tries multiple methods to detect the default branch:
    1. Check origin's HEAD symbolic ref
    2. Check which common branch exists (main, master, develop)
    3. Fallback to "main"

    Args:
        repo_path: Path to the repository

    Returns:
        Default branch name (e.g., "main", "master", "develop")
    """
    import subprocess

    # Method 1: Get from origin's HEAD
    result = subprocess.run(
        ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
        cwd=repo_path,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="XXreplaceXX",
        timeout=5,
    )

    if result.returncode == 0:
        # Output: "refs/remotes/origin/main" → extract "main"
        ref = result.stdout.strip()
        return ref.split("/")[-1]

    # Method 2: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        result = subprocess.run(
            ["git", "rev-parse", "--verify", branch],
            cwd=repo_path,
            capture_output=True,
            timeout=5,
        )
        if result.returncode == 0:
            return branch

    # Method 3: Fallback
    return "main"


def x_get_default_branch__mutmut_28(repo_path: Path) -> str:
    """
    Get the default/base branch name for the repository (for stale detection).

    This is used to find the branch that feature branches diverged FROM.
    Unlike resolve_primary_branch() in git_ops, this does NOT use the current
    branch because stale detection always runs from worktrees where the current
    branch is always the feature branch, never the base branch.

    Tries multiple methods to detect the default branch:
    1. Check origin's HEAD symbolic ref
    2. Check which common branch exists (main, master, develop)
    3. Fallback to "main"

    Args:
        repo_path: Path to the repository

    Returns:
        Default branch name (e.g., "main", "master", "develop")
    """
    import subprocess

    # Method 1: Get from origin's HEAD
    result = subprocess.run(
        ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
        cwd=repo_path,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="REPLACE",
        timeout=5,
    )

    if result.returncode == 0:
        # Output: "refs/remotes/origin/main" → extract "main"
        ref = result.stdout.strip()
        return ref.split("/")[-1]

    # Method 2: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        result = subprocess.run(
            ["git", "rev-parse", "--verify", branch],
            cwd=repo_path,
            capture_output=True,
            timeout=5,
        )
        if result.returncode == 0:
            return branch

    # Method 3: Fallback
    return "main"


def x_get_default_branch__mutmut_29(repo_path: Path) -> str:
    """
    Get the default/base branch name for the repository (for stale detection).

    This is used to find the branch that feature branches diverged FROM.
    Unlike resolve_primary_branch() in git_ops, this does NOT use the current
    branch because stale detection always runs from worktrees where the current
    branch is always the feature branch, never the base branch.

    Tries multiple methods to detect the default branch:
    1. Check origin's HEAD symbolic ref
    2. Check which common branch exists (main, master, develop)
    3. Fallback to "main"

    Args:
        repo_path: Path to the repository

    Returns:
        Default branch name (e.g., "main", "master", "develop")
    """
    import subprocess

    # Method 1: Get from origin's HEAD
    result = subprocess.run(
        ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
        cwd=repo_path,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=6,
    )

    if result.returncode == 0:
        # Output: "refs/remotes/origin/main" → extract "main"
        ref = result.stdout.strip()
        return ref.split("/")[-1]

    # Method 2: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        result = subprocess.run(
            ["git", "rev-parse", "--verify", branch],
            cwd=repo_path,
            capture_output=True,
            timeout=5,
        )
        if result.returncode == 0:
            return branch

    # Method 3: Fallback
    return "main"


def x_get_default_branch__mutmut_30(repo_path: Path) -> str:
    """
    Get the default/base branch name for the repository (for stale detection).

    This is used to find the branch that feature branches diverged FROM.
    Unlike resolve_primary_branch() in git_ops, this does NOT use the current
    branch because stale detection always runs from worktrees where the current
    branch is always the feature branch, never the base branch.

    Tries multiple methods to detect the default branch:
    1. Check origin's HEAD symbolic ref
    2. Check which common branch exists (main, master, develop)
    3. Fallback to "main"

    Args:
        repo_path: Path to the repository

    Returns:
        Default branch name (e.g., "main", "master", "develop")
    """
    import subprocess

    # Method 1: Get from origin's HEAD
    result = subprocess.run(
        ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
        cwd=repo_path,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=5,
    )

    if result.returncode != 0:
        # Output: "refs/remotes/origin/main" → extract "main"
        ref = result.stdout.strip()
        return ref.split("/")[-1]

    # Method 2: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        result = subprocess.run(
            ["git", "rev-parse", "--verify", branch],
            cwd=repo_path,
            capture_output=True,
            timeout=5,
        )
        if result.returncode == 0:
            return branch

    # Method 3: Fallback
    return "main"


def x_get_default_branch__mutmut_31(repo_path: Path) -> str:
    """
    Get the default/base branch name for the repository (for stale detection).

    This is used to find the branch that feature branches diverged FROM.
    Unlike resolve_primary_branch() in git_ops, this does NOT use the current
    branch because stale detection always runs from worktrees where the current
    branch is always the feature branch, never the base branch.

    Tries multiple methods to detect the default branch:
    1. Check origin's HEAD symbolic ref
    2. Check which common branch exists (main, master, develop)
    3. Fallback to "main"

    Args:
        repo_path: Path to the repository

    Returns:
        Default branch name (e.g., "main", "master", "develop")
    """
    import subprocess

    # Method 1: Get from origin's HEAD
    result = subprocess.run(
        ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
        cwd=repo_path,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=5,
    )

    if result.returncode == 1:
        # Output: "refs/remotes/origin/main" → extract "main"
        ref = result.stdout.strip()
        return ref.split("/")[-1]

    # Method 2: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        result = subprocess.run(
            ["git", "rev-parse", "--verify", branch],
            cwd=repo_path,
            capture_output=True,
            timeout=5,
        )
        if result.returncode == 0:
            return branch

    # Method 3: Fallback
    return "main"


def x_get_default_branch__mutmut_32(repo_path: Path) -> str:
    """
    Get the default/base branch name for the repository (for stale detection).

    This is used to find the branch that feature branches diverged FROM.
    Unlike resolve_primary_branch() in git_ops, this does NOT use the current
    branch because stale detection always runs from worktrees where the current
    branch is always the feature branch, never the base branch.

    Tries multiple methods to detect the default branch:
    1. Check origin's HEAD symbolic ref
    2. Check which common branch exists (main, master, develop)
    3. Fallback to "main"

    Args:
        repo_path: Path to the repository

    Returns:
        Default branch name (e.g., "main", "master", "develop")
    """
    import subprocess

    # Method 1: Get from origin's HEAD
    result = subprocess.run(
        ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
        cwd=repo_path,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=5,
    )

    if result.returncode == 0:
        # Output: "refs/remotes/origin/main" → extract "main"
        ref = None
        return ref.split("/")[-1]

    # Method 2: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        result = subprocess.run(
            ["git", "rev-parse", "--verify", branch],
            cwd=repo_path,
            capture_output=True,
            timeout=5,
        )
        if result.returncode == 0:
            return branch

    # Method 3: Fallback
    return "main"


def x_get_default_branch__mutmut_33(repo_path: Path) -> str:
    """
    Get the default/base branch name for the repository (for stale detection).

    This is used to find the branch that feature branches diverged FROM.
    Unlike resolve_primary_branch() in git_ops, this does NOT use the current
    branch because stale detection always runs from worktrees where the current
    branch is always the feature branch, never the base branch.

    Tries multiple methods to detect the default branch:
    1. Check origin's HEAD symbolic ref
    2. Check which common branch exists (main, master, develop)
    3. Fallback to "main"

    Args:
        repo_path: Path to the repository

    Returns:
        Default branch name (e.g., "main", "master", "develop")
    """
    import subprocess

    # Method 1: Get from origin's HEAD
    result = subprocess.run(
        ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
        cwd=repo_path,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=5,
    )

    if result.returncode == 0:
        # Output: "refs/remotes/origin/main" → extract "main"
        ref = result.stdout.strip()
        return ref.split(None)[-1]

    # Method 2: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        result = subprocess.run(
            ["git", "rev-parse", "--verify", branch],
            cwd=repo_path,
            capture_output=True,
            timeout=5,
        )
        if result.returncode == 0:
            return branch

    # Method 3: Fallback
    return "main"


def x_get_default_branch__mutmut_34(repo_path: Path) -> str:
    """
    Get the default/base branch name for the repository (for stale detection).

    This is used to find the branch that feature branches diverged FROM.
    Unlike resolve_primary_branch() in git_ops, this does NOT use the current
    branch because stale detection always runs from worktrees where the current
    branch is always the feature branch, never the base branch.

    Tries multiple methods to detect the default branch:
    1. Check origin's HEAD symbolic ref
    2. Check which common branch exists (main, master, develop)
    3. Fallback to "main"

    Args:
        repo_path: Path to the repository

    Returns:
        Default branch name (e.g., "main", "master", "develop")
    """
    import subprocess

    # Method 1: Get from origin's HEAD
    result = subprocess.run(
        ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
        cwd=repo_path,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=5,
    )

    if result.returncode == 0:
        # Output: "refs/remotes/origin/main" → extract "main"
        ref = result.stdout.strip()
        return ref.split("XX/XX")[-1]

    # Method 2: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        result = subprocess.run(
            ["git", "rev-parse", "--verify", branch],
            cwd=repo_path,
            capture_output=True,
            timeout=5,
        )
        if result.returncode == 0:
            return branch

    # Method 3: Fallback
    return "main"


def x_get_default_branch__mutmut_35(repo_path: Path) -> str:
    """
    Get the default/base branch name for the repository (for stale detection).

    This is used to find the branch that feature branches diverged FROM.
    Unlike resolve_primary_branch() in git_ops, this does NOT use the current
    branch because stale detection always runs from worktrees where the current
    branch is always the feature branch, never the base branch.

    Tries multiple methods to detect the default branch:
    1. Check origin's HEAD symbolic ref
    2. Check which common branch exists (main, master, develop)
    3. Fallback to "main"

    Args:
        repo_path: Path to the repository

    Returns:
        Default branch name (e.g., "main", "master", "develop")
    """
    import subprocess

    # Method 1: Get from origin's HEAD
    result = subprocess.run(
        ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
        cwd=repo_path,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=5,
    )

    if result.returncode == 0:
        # Output: "refs/remotes/origin/main" → extract "main"
        ref = result.stdout.strip()
        return ref.split("/")[+1]

    # Method 2: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        result = subprocess.run(
            ["git", "rev-parse", "--verify", branch],
            cwd=repo_path,
            capture_output=True,
            timeout=5,
        )
        if result.returncode == 0:
            return branch

    # Method 3: Fallback
    return "main"


def x_get_default_branch__mutmut_36(repo_path: Path) -> str:
    """
    Get the default/base branch name for the repository (for stale detection).

    This is used to find the branch that feature branches diverged FROM.
    Unlike resolve_primary_branch() in git_ops, this does NOT use the current
    branch because stale detection always runs from worktrees where the current
    branch is always the feature branch, never the base branch.

    Tries multiple methods to detect the default branch:
    1. Check origin's HEAD symbolic ref
    2. Check which common branch exists (main, master, develop)
    3. Fallback to "main"

    Args:
        repo_path: Path to the repository

    Returns:
        Default branch name (e.g., "main", "master", "develop")
    """
    import subprocess

    # Method 1: Get from origin's HEAD
    result = subprocess.run(
        ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
        cwd=repo_path,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=5,
    )

    if result.returncode == 0:
        # Output: "refs/remotes/origin/main" → extract "main"
        ref = result.stdout.strip()
        return ref.split("/")[-2]

    # Method 2: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        result = subprocess.run(
            ["git", "rev-parse", "--verify", branch],
            cwd=repo_path,
            capture_output=True,
            timeout=5,
        )
        if result.returncode == 0:
            return branch

    # Method 3: Fallback
    return "main"


def x_get_default_branch__mutmut_37(repo_path: Path) -> str:
    """
    Get the default/base branch name for the repository (for stale detection).

    This is used to find the branch that feature branches diverged FROM.
    Unlike resolve_primary_branch() in git_ops, this does NOT use the current
    branch because stale detection always runs from worktrees where the current
    branch is always the feature branch, never the base branch.

    Tries multiple methods to detect the default branch:
    1. Check origin's HEAD symbolic ref
    2. Check which common branch exists (main, master, develop)
    3. Fallback to "main"

    Args:
        repo_path: Path to the repository

    Returns:
        Default branch name (e.g., "main", "master", "develop")
    """
    import subprocess

    # Method 1: Get from origin's HEAD
    result = subprocess.run(
        ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
        cwd=repo_path,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=5,
    )

    if result.returncode == 0:
        # Output: "refs/remotes/origin/main" → extract "main"
        ref = result.stdout.strip()
        return ref.split("/")[-1]

    # Method 2: Check which common branch exists
    for branch in ["XXmainXX", "master", "develop"]:
        result = subprocess.run(
            ["git", "rev-parse", "--verify", branch],
            cwd=repo_path,
            capture_output=True,
            timeout=5,
        )
        if result.returncode == 0:
            return branch

    # Method 3: Fallback
    return "main"


def x_get_default_branch__mutmut_38(repo_path: Path) -> str:
    """
    Get the default/base branch name for the repository (for stale detection).

    This is used to find the branch that feature branches diverged FROM.
    Unlike resolve_primary_branch() in git_ops, this does NOT use the current
    branch because stale detection always runs from worktrees where the current
    branch is always the feature branch, never the base branch.

    Tries multiple methods to detect the default branch:
    1. Check origin's HEAD symbolic ref
    2. Check which common branch exists (main, master, develop)
    3. Fallback to "main"

    Args:
        repo_path: Path to the repository

    Returns:
        Default branch name (e.g., "main", "master", "develop")
    """
    import subprocess

    # Method 1: Get from origin's HEAD
    result = subprocess.run(
        ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
        cwd=repo_path,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=5,
    )

    if result.returncode == 0:
        # Output: "refs/remotes/origin/main" → extract "main"
        ref = result.stdout.strip()
        return ref.split("/")[-1]

    # Method 2: Check which common branch exists
    for branch in ["MAIN", "master", "develop"]:
        result = subprocess.run(
            ["git", "rev-parse", "--verify", branch],
            cwd=repo_path,
            capture_output=True,
            timeout=5,
        )
        if result.returncode == 0:
            return branch

    # Method 3: Fallback
    return "main"


def x_get_default_branch__mutmut_39(repo_path: Path) -> str:
    """
    Get the default/base branch name for the repository (for stale detection).

    This is used to find the branch that feature branches diverged FROM.
    Unlike resolve_primary_branch() in git_ops, this does NOT use the current
    branch because stale detection always runs from worktrees where the current
    branch is always the feature branch, never the base branch.

    Tries multiple methods to detect the default branch:
    1. Check origin's HEAD symbolic ref
    2. Check which common branch exists (main, master, develop)
    3. Fallback to "main"

    Args:
        repo_path: Path to the repository

    Returns:
        Default branch name (e.g., "main", "master", "develop")
    """
    import subprocess

    # Method 1: Get from origin's HEAD
    result = subprocess.run(
        ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
        cwd=repo_path,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=5,
    )

    if result.returncode == 0:
        # Output: "refs/remotes/origin/main" → extract "main"
        ref = result.stdout.strip()
        return ref.split("/")[-1]

    # Method 2: Check which common branch exists
    for branch in ["main", "XXmasterXX", "develop"]:
        result = subprocess.run(
            ["git", "rev-parse", "--verify", branch],
            cwd=repo_path,
            capture_output=True,
            timeout=5,
        )
        if result.returncode == 0:
            return branch

    # Method 3: Fallback
    return "main"


def x_get_default_branch__mutmut_40(repo_path: Path) -> str:
    """
    Get the default/base branch name for the repository (for stale detection).

    This is used to find the branch that feature branches diverged FROM.
    Unlike resolve_primary_branch() in git_ops, this does NOT use the current
    branch because stale detection always runs from worktrees where the current
    branch is always the feature branch, never the base branch.

    Tries multiple methods to detect the default branch:
    1. Check origin's HEAD symbolic ref
    2. Check which common branch exists (main, master, develop)
    3. Fallback to "main"

    Args:
        repo_path: Path to the repository

    Returns:
        Default branch name (e.g., "main", "master", "develop")
    """
    import subprocess

    # Method 1: Get from origin's HEAD
    result = subprocess.run(
        ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
        cwd=repo_path,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=5,
    )

    if result.returncode == 0:
        # Output: "refs/remotes/origin/main" → extract "main"
        ref = result.stdout.strip()
        return ref.split("/")[-1]

    # Method 2: Check which common branch exists
    for branch in ["main", "MASTER", "develop"]:
        result = subprocess.run(
            ["git", "rev-parse", "--verify", branch],
            cwd=repo_path,
            capture_output=True,
            timeout=5,
        )
        if result.returncode == 0:
            return branch

    # Method 3: Fallback
    return "main"


def x_get_default_branch__mutmut_41(repo_path: Path) -> str:
    """
    Get the default/base branch name for the repository (for stale detection).

    This is used to find the branch that feature branches diverged FROM.
    Unlike resolve_primary_branch() in git_ops, this does NOT use the current
    branch because stale detection always runs from worktrees where the current
    branch is always the feature branch, never the base branch.

    Tries multiple methods to detect the default branch:
    1. Check origin's HEAD symbolic ref
    2. Check which common branch exists (main, master, develop)
    3. Fallback to "main"

    Args:
        repo_path: Path to the repository

    Returns:
        Default branch name (e.g., "main", "master", "develop")
    """
    import subprocess

    # Method 1: Get from origin's HEAD
    result = subprocess.run(
        ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
        cwd=repo_path,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=5,
    )

    if result.returncode == 0:
        # Output: "refs/remotes/origin/main" → extract "main"
        ref = result.stdout.strip()
        return ref.split("/")[-1]

    # Method 2: Check which common branch exists
    for branch in ["main", "master", "XXdevelopXX"]:
        result = subprocess.run(
            ["git", "rev-parse", "--verify", branch],
            cwd=repo_path,
            capture_output=True,
            timeout=5,
        )
        if result.returncode == 0:
            return branch

    # Method 3: Fallback
    return "main"


def x_get_default_branch__mutmut_42(repo_path: Path) -> str:
    """
    Get the default/base branch name for the repository (for stale detection).

    This is used to find the branch that feature branches diverged FROM.
    Unlike resolve_primary_branch() in git_ops, this does NOT use the current
    branch because stale detection always runs from worktrees where the current
    branch is always the feature branch, never the base branch.

    Tries multiple methods to detect the default branch:
    1. Check origin's HEAD symbolic ref
    2. Check which common branch exists (main, master, develop)
    3. Fallback to "main"

    Args:
        repo_path: Path to the repository

    Returns:
        Default branch name (e.g., "main", "master", "develop")
    """
    import subprocess

    # Method 1: Get from origin's HEAD
    result = subprocess.run(
        ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
        cwd=repo_path,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=5,
    )

    if result.returncode == 0:
        # Output: "refs/remotes/origin/main" → extract "main"
        ref = result.stdout.strip()
        return ref.split("/")[-1]

    # Method 2: Check which common branch exists
    for branch in ["main", "master", "DEVELOP"]:
        result = subprocess.run(
            ["git", "rev-parse", "--verify", branch],
            cwd=repo_path,
            capture_output=True,
            timeout=5,
        )
        if result.returncode == 0:
            return branch

    # Method 3: Fallback
    return "main"


def x_get_default_branch__mutmut_43(repo_path: Path) -> str:
    """
    Get the default/base branch name for the repository (for stale detection).

    This is used to find the branch that feature branches diverged FROM.
    Unlike resolve_primary_branch() in git_ops, this does NOT use the current
    branch because stale detection always runs from worktrees where the current
    branch is always the feature branch, never the base branch.

    Tries multiple methods to detect the default branch:
    1. Check origin's HEAD symbolic ref
    2. Check which common branch exists (main, master, develop)
    3. Fallback to "main"

    Args:
        repo_path: Path to the repository

    Returns:
        Default branch name (e.g., "main", "master", "develop")
    """
    import subprocess

    # Method 1: Get from origin's HEAD
    result = subprocess.run(
        ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
        cwd=repo_path,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=5,
    )

    if result.returncode == 0:
        # Output: "refs/remotes/origin/main" → extract "main"
        ref = result.stdout.strip()
        return ref.split("/")[-1]

    # Method 2: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        result = None
        if result.returncode == 0:
            return branch

    # Method 3: Fallback
    return "main"


def x_get_default_branch__mutmut_44(repo_path: Path) -> str:
    """
    Get the default/base branch name for the repository (for stale detection).

    This is used to find the branch that feature branches diverged FROM.
    Unlike resolve_primary_branch() in git_ops, this does NOT use the current
    branch because stale detection always runs from worktrees where the current
    branch is always the feature branch, never the base branch.

    Tries multiple methods to detect the default branch:
    1. Check origin's HEAD symbolic ref
    2. Check which common branch exists (main, master, develop)
    3. Fallback to "main"

    Args:
        repo_path: Path to the repository

    Returns:
        Default branch name (e.g., "main", "master", "develop")
    """
    import subprocess

    # Method 1: Get from origin's HEAD
    result = subprocess.run(
        ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
        cwd=repo_path,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=5,
    )

    if result.returncode == 0:
        # Output: "refs/remotes/origin/main" → extract "main"
        ref = result.stdout.strip()
        return ref.split("/")[-1]

    # Method 2: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        result = subprocess.run(
            None,
            cwd=repo_path,
            capture_output=True,
            timeout=5,
        )
        if result.returncode == 0:
            return branch

    # Method 3: Fallback
    return "main"


def x_get_default_branch__mutmut_45(repo_path: Path) -> str:
    """
    Get the default/base branch name for the repository (for stale detection).

    This is used to find the branch that feature branches diverged FROM.
    Unlike resolve_primary_branch() in git_ops, this does NOT use the current
    branch because stale detection always runs from worktrees where the current
    branch is always the feature branch, never the base branch.

    Tries multiple methods to detect the default branch:
    1. Check origin's HEAD symbolic ref
    2. Check which common branch exists (main, master, develop)
    3. Fallback to "main"

    Args:
        repo_path: Path to the repository

    Returns:
        Default branch name (e.g., "main", "master", "develop")
    """
    import subprocess

    # Method 1: Get from origin's HEAD
    result = subprocess.run(
        ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
        cwd=repo_path,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=5,
    )

    if result.returncode == 0:
        # Output: "refs/remotes/origin/main" → extract "main"
        ref = result.stdout.strip()
        return ref.split("/")[-1]

    # Method 2: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        result = subprocess.run(
            ["git", "rev-parse", "--verify", branch],
            cwd=None,
            capture_output=True,
            timeout=5,
        )
        if result.returncode == 0:
            return branch

    # Method 3: Fallback
    return "main"


def x_get_default_branch__mutmut_46(repo_path: Path) -> str:
    """
    Get the default/base branch name for the repository (for stale detection).

    This is used to find the branch that feature branches diverged FROM.
    Unlike resolve_primary_branch() in git_ops, this does NOT use the current
    branch because stale detection always runs from worktrees where the current
    branch is always the feature branch, never the base branch.

    Tries multiple methods to detect the default branch:
    1. Check origin's HEAD symbolic ref
    2. Check which common branch exists (main, master, develop)
    3. Fallback to "main"

    Args:
        repo_path: Path to the repository

    Returns:
        Default branch name (e.g., "main", "master", "develop")
    """
    import subprocess

    # Method 1: Get from origin's HEAD
    result = subprocess.run(
        ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
        cwd=repo_path,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=5,
    )

    if result.returncode == 0:
        # Output: "refs/remotes/origin/main" → extract "main"
        ref = result.stdout.strip()
        return ref.split("/")[-1]

    # Method 2: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        result = subprocess.run(
            ["git", "rev-parse", "--verify", branch],
            cwd=repo_path,
            capture_output=None,
            timeout=5,
        )
        if result.returncode == 0:
            return branch

    # Method 3: Fallback
    return "main"


def x_get_default_branch__mutmut_47(repo_path: Path) -> str:
    """
    Get the default/base branch name for the repository (for stale detection).

    This is used to find the branch that feature branches diverged FROM.
    Unlike resolve_primary_branch() in git_ops, this does NOT use the current
    branch because stale detection always runs from worktrees where the current
    branch is always the feature branch, never the base branch.

    Tries multiple methods to detect the default branch:
    1. Check origin's HEAD symbolic ref
    2. Check which common branch exists (main, master, develop)
    3. Fallback to "main"

    Args:
        repo_path: Path to the repository

    Returns:
        Default branch name (e.g., "main", "master", "develop")
    """
    import subprocess

    # Method 1: Get from origin's HEAD
    result = subprocess.run(
        ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
        cwd=repo_path,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=5,
    )

    if result.returncode == 0:
        # Output: "refs/remotes/origin/main" → extract "main"
        ref = result.stdout.strip()
        return ref.split("/")[-1]

    # Method 2: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        result = subprocess.run(
            ["git", "rev-parse", "--verify", branch],
            cwd=repo_path,
            capture_output=True,
            timeout=None,
        )
        if result.returncode == 0:
            return branch

    # Method 3: Fallback
    return "main"


def x_get_default_branch__mutmut_48(repo_path: Path) -> str:
    """
    Get the default/base branch name for the repository (for stale detection).

    This is used to find the branch that feature branches diverged FROM.
    Unlike resolve_primary_branch() in git_ops, this does NOT use the current
    branch because stale detection always runs from worktrees where the current
    branch is always the feature branch, never the base branch.

    Tries multiple methods to detect the default branch:
    1. Check origin's HEAD symbolic ref
    2. Check which common branch exists (main, master, develop)
    3. Fallback to "main"

    Args:
        repo_path: Path to the repository

    Returns:
        Default branch name (e.g., "main", "master", "develop")
    """
    import subprocess

    # Method 1: Get from origin's HEAD
    result = subprocess.run(
        ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
        cwd=repo_path,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=5,
    )

    if result.returncode == 0:
        # Output: "refs/remotes/origin/main" → extract "main"
        ref = result.stdout.strip()
        return ref.split("/")[-1]

    # Method 2: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        result = subprocess.run(
            cwd=repo_path,
            capture_output=True,
            timeout=5,
        )
        if result.returncode == 0:
            return branch

    # Method 3: Fallback
    return "main"


def x_get_default_branch__mutmut_49(repo_path: Path) -> str:
    """
    Get the default/base branch name for the repository (for stale detection).

    This is used to find the branch that feature branches diverged FROM.
    Unlike resolve_primary_branch() in git_ops, this does NOT use the current
    branch because stale detection always runs from worktrees where the current
    branch is always the feature branch, never the base branch.

    Tries multiple methods to detect the default branch:
    1. Check origin's HEAD symbolic ref
    2. Check which common branch exists (main, master, develop)
    3. Fallback to "main"

    Args:
        repo_path: Path to the repository

    Returns:
        Default branch name (e.g., "main", "master", "develop")
    """
    import subprocess

    # Method 1: Get from origin's HEAD
    result = subprocess.run(
        ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
        cwd=repo_path,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=5,
    )

    if result.returncode == 0:
        # Output: "refs/remotes/origin/main" → extract "main"
        ref = result.stdout.strip()
        return ref.split("/")[-1]

    # Method 2: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        result = subprocess.run(
            ["git", "rev-parse", "--verify", branch],
            capture_output=True,
            timeout=5,
        )
        if result.returncode == 0:
            return branch

    # Method 3: Fallback
    return "main"


def x_get_default_branch__mutmut_50(repo_path: Path) -> str:
    """
    Get the default/base branch name for the repository (for stale detection).

    This is used to find the branch that feature branches diverged FROM.
    Unlike resolve_primary_branch() in git_ops, this does NOT use the current
    branch because stale detection always runs from worktrees where the current
    branch is always the feature branch, never the base branch.

    Tries multiple methods to detect the default branch:
    1. Check origin's HEAD symbolic ref
    2. Check which common branch exists (main, master, develop)
    3. Fallback to "main"

    Args:
        repo_path: Path to the repository

    Returns:
        Default branch name (e.g., "main", "master", "develop")
    """
    import subprocess

    # Method 1: Get from origin's HEAD
    result = subprocess.run(
        ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
        cwd=repo_path,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=5,
    )

    if result.returncode == 0:
        # Output: "refs/remotes/origin/main" → extract "main"
        ref = result.stdout.strip()
        return ref.split("/")[-1]

    # Method 2: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        result = subprocess.run(
            ["git", "rev-parse", "--verify", branch],
            cwd=repo_path,
            timeout=5,
        )
        if result.returncode == 0:
            return branch

    # Method 3: Fallback
    return "main"


def x_get_default_branch__mutmut_51(repo_path: Path) -> str:
    """
    Get the default/base branch name for the repository (for stale detection).

    This is used to find the branch that feature branches diverged FROM.
    Unlike resolve_primary_branch() in git_ops, this does NOT use the current
    branch because stale detection always runs from worktrees where the current
    branch is always the feature branch, never the base branch.

    Tries multiple methods to detect the default branch:
    1. Check origin's HEAD symbolic ref
    2. Check which common branch exists (main, master, develop)
    3. Fallback to "main"

    Args:
        repo_path: Path to the repository

    Returns:
        Default branch name (e.g., "main", "master", "develop")
    """
    import subprocess

    # Method 1: Get from origin's HEAD
    result = subprocess.run(
        ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
        cwd=repo_path,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=5,
    )

    if result.returncode == 0:
        # Output: "refs/remotes/origin/main" → extract "main"
        ref = result.stdout.strip()
        return ref.split("/")[-1]

    # Method 2: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        result = subprocess.run(
            ["git", "rev-parse", "--verify", branch],
            cwd=repo_path,
            capture_output=True,
            )
        if result.returncode == 0:
            return branch

    # Method 3: Fallback
    return "main"


def x_get_default_branch__mutmut_52(repo_path: Path) -> str:
    """
    Get the default/base branch name for the repository (for stale detection).

    This is used to find the branch that feature branches diverged FROM.
    Unlike resolve_primary_branch() in git_ops, this does NOT use the current
    branch because stale detection always runs from worktrees where the current
    branch is always the feature branch, never the base branch.

    Tries multiple methods to detect the default branch:
    1. Check origin's HEAD symbolic ref
    2. Check which common branch exists (main, master, develop)
    3. Fallback to "main"

    Args:
        repo_path: Path to the repository

    Returns:
        Default branch name (e.g., "main", "master", "develop")
    """
    import subprocess

    # Method 1: Get from origin's HEAD
    result = subprocess.run(
        ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
        cwd=repo_path,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=5,
    )

    if result.returncode == 0:
        # Output: "refs/remotes/origin/main" → extract "main"
        ref = result.stdout.strip()
        return ref.split("/")[-1]

    # Method 2: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        result = subprocess.run(
            ["XXgitXX", "rev-parse", "--verify", branch],
            cwd=repo_path,
            capture_output=True,
            timeout=5,
        )
        if result.returncode == 0:
            return branch

    # Method 3: Fallback
    return "main"


def x_get_default_branch__mutmut_53(repo_path: Path) -> str:
    """
    Get the default/base branch name for the repository (for stale detection).

    This is used to find the branch that feature branches diverged FROM.
    Unlike resolve_primary_branch() in git_ops, this does NOT use the current
    branch because stale detection always runs from worktrees where the current
    branch is always the feature branch, never the base branch.

    Tries multiple methods to detect the default branch:
    1. Check origin's HEAD symbolic ref
    2. Check which common branch exists (main, master, develop)
    3. Fallback to "main"

    Args:
        repo_path: Path to the repository

    Returns:
        Default branch name (e.g., "main", "master", "develop")
    """
    import subprocess

    # Method 1: Get from origin's HEAD
    result = subprocess.run(
        ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
        cwd=repo_path,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=5,
    )

    if result.returncode == 0:
        # Output: "refs/remotes/origin/main" → extract "main"
        ref = result.stdout.strip()
        return ref.split("/")[-1]

    # Method 2: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        result = subprocess.run(
            ["GIT", "rev-parse", "--verify", branch],
            cwd=repo_path,
            capture_output=True,
            timeout=5,
        )
        if result.returncode == 0:
            return branch

    # Method 3: Fallback
    return "main"


def x_get_default_branch__mutmut_54(repo_path: Path) -> str:
    """
    Get the default/base branch name for the repository (for stale detection).

    This is used to find the branch that feature branches diverged FROM.
    Unlike resolve_primary_branch() in git_ops, this does NOT use the current
    branch because stale detection always runs from worktrees where the current
    branch is always the feature branch, never the base branch.

    Tries multiple methods to detect the default branch:
    1. Check origin's HEAD symbolic ref
    2. Check which common branch exists (main, master, develop)
    3. Fallback to "main"

    Args:
        repo_path: Path to the repository

    Returns:
        Default branch name (e.g., "main", "master", "develop")
    """
    import subprocess

    # Method 1: Get from origin's HEAD
    result = subprocess.run(
        ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
        cwd=repo_path,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=5,
    )

    if result.returncode == 0:
        # Output: "refs/remotes/origin/main" → extract "main"
        ref = result.stdout.strip()
        return ref.split("/")[-1]

    # Method 2: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        result = subprocess.run(
            ["git", "XXrev-parseXX", "--verify", branch],
            cwd=repo_path,
            capture_output=True,
            timeout=5,
        )
        if result.returncode == 0:
            return branch

    # Method 3: Fallback
    return "main"


def x_get_default_branch__mutmut_55(repo_path: Path) -> str:
    """
    Get the default/base branch name for the repository (for stale detection).

    This is used to find the branch that feature branches diverged FROM.
    Unlike resolve_primary_branch() in git_ops, this does NOT use the current
    branch because stale detection always runs from worktrees where the current
    branch is always the feature branch, never the base branch.

    Tries multiple methods to detect the default branch:
    1. Check origin's HEAD symbolic ref
    2. Check which common branch exists (main, master, develop)
    3. Fallback to "main"

    Args:
        repo_path: Path to the repository

    Returns:
        Default branch name (e.g., "main", "master", "develop")
    """
    import subprocess

    # Method 1: Get from origin's HEAD
    result = subprocess.run(
        ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
        cwd=repo_path,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=5,
    )

    if result.returncode == 0:
        # Output: "refs/remotes/origin/main" → extract "main"
        ref = result.stdout.strip()
        return ref.split("/")[-1]

    # Method 2: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        result = subprocess.run(
            ["git", "REV-PARSE", "--verify", branch],
            cwd=repo_path,
            capture_output=True,
            timeout=5,
        )
        if result.returncode == 0:
            return branch

    # Method 3: Fallback
    return "main"


def x_get_default_branch__mutmut_56(repo_path: Path) -> str:
    """
    Get the default/base branch name for the repository (for stale detection).

    This is used to find the branch that feature branches diverged FROM.
    Unlike resolve_primary_branch() in git_ops, this does NOT use the current
    branch because stale detection always runs from worktrees where the current
    branch is always the feature branch, never the base branch.

    Tries multiple methods to detect the default branch:
    1. Check origin's HEAD symbolic ref
    2. Check which common branch exists (main, master, develop)
    3. Fallback to "main"

    Args:
        repo_path: Path to the repository

    Returns:
        Default branch name (e.g., "main", "master", "develop")
    """
    import subprocess

    # Method 1: Get from origin's HEAD
    result = subprocess.run(
        ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
        cwd=repo_path,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=5,
    )

    if result.returncode == 0:
        # Output: "refs/remotes/origin/main" → extract "main"
        ref = result.stdout.strip()
        return ref.split("/")[-1]

    # Method 2: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        result = subprocess.run(
            ["git", "rev-parse", "XX--verifyXX", branch],
            cwd=repo_path,
            capture_output=True,
            timeout=5,
        )
        if result.returncode == 0:
            return branch

    # Method 3: Fallback
    return "main"


def x_get_default_branch__mutmut_57(repo_path: Path) -> str:
    """
    Get the default/base branch name for the repository (for stale detection).

    This is used to find the branch that feature branches diverged FROM.
    Unlike resolve_primary_branch() in git_ops, this does NOT use the current
    branch because stale detection always runs from worktrees where the current
    branch is always the feature branch, never the base branch.

    Tries multiple methods to detect the default branch:
    1. Check origin's HEAD symbolic ref
    2. Check which common branch exists (main, master, develop)
    3. Fallback to "main"

    Args:
        repo_path: Path to the repository

    Returns:
        Default branch name (e.g., "main", "master", "develop")
    """
    import subprocess

    # Method 1: Get from origin's HEAD
    result = subprocess.run(
        ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
        cwd=repo_path,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=5,
    )

    if result.returncode == 0:
        # Output: "refs/remotes/origin/main" → extract "main"
        ref = result.stdout.strip()
        return ref.split("/")[-1]

    # Method 2: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        result = subprocess.run(
            ["git", "rev-parse", "--VERIFY", branch],
            cwd=repo_path,
            capture_output=True,
            timeout=5,
        )
        if result.returncode == 0:
            return branch

    # Method 3: Fallback
    return "main"


def x_get_default_branch__mutmut_58(repo_path: Path) -> str:
    """
    Get the default/base branch name for the repository (for stale detection).

    This is used to find the branch that feature branches diverged FROM.
    Unlike resolve_primary_branch() in git_ops, this does NOT use the current
    branch because stale detection always runs from worktrees where the current
    branch is always the feature branch, never the base branch.

    Tries multiple methods to detect the default branch:
    1. Check origin's HEAD symbolic ref
    2. Check which common branch exists (main, master, develop)
    3. Fallback to "main"

    Args:
        repo_path: Path to the repository

    Returns:
        Default branch name (e.g., "main", "master", "develop")
    """
    import subprocess

    # Method 1: Get from origin's HEAD
    result = subprocess.run(
        ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
        cwd=repo_path,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=5,
    )

    if result.returncode == 0:
        # Output: "refs/remotes/origin/main" → extract "main"
        ref = result.stdout.strip()
        return ref.split("/")[-1]

    # Method 2: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        result = subprocess.run(
            ["git", "rev-parse", "--verify", branch],
            cwd=repo_path,
            capture_output=False,
            timeout=5,
        )
        if result.returncode == 0:
            return branch

    # Method 3: Fallback
    return "main"


def x_get_default_branch__mutmut_59(repo_path: Path) -> str:
    """
    Get the default/base branch name for the repository (for stale detection).

    This is used to find the branch that feature branches diverged FROM.
    Unlike resolve_primary_branch() in git_ops, this does NOT use the current
    branch because stale detection always runs from worktrees where the current
    branch is always the feature branch, never the base branch.

    Tries multiple methods to detect the default branch:
    1. Check origin's HEAD symbolic ref
    2. Check which common branch exists (main, master, develop)
    3. Fallback to "main"

    Args:
        repo_path: Path to the repository

    Returns:
        Default branch name (e.g., "main", "master", "develop")
    """
    import subprocess

    # Method 1: Get from origin's HEAD
    result = subprocess.run(
        ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
        cwd=repo_path,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=5,
    )

    if result.returncode == 0:
        # Output: "refs/remotes/origin/main" → extract "main"
        ref = result.stdout.strip()
        return ref.split("/")[-1]

    # Method 2: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        result = subprocess.run(
            ["git", "rev-parse", "--verify", branch],
            cwd=repo_path,
            capture_output=True,
            timeout=6,
        )
        if result.returncode == 0:
            return branch

    # Method 3: Fallback
    return "main"


def x_get_default_branch__mutmut_60(repo_path: Path) -> str:
    """
    Get the default/base branch name for the repository (for stale detection).

    This is used to find the branch that feature branches diverged FROM.
    Unlike resolve_primary_branch() in git_ops, this does NOT use the current
    branch because stale detection always runs from worktrees where the current
    branch is always the feature branch, never the base branch.

    Tries multiple methods to detect the default branch:
    1. Check origin's HEAD symbolic ref
    2. Check which common branch exists (main, master, develop)
    3. Fallback to "main"

    Args:
        repo_path: Path to the repository

    Returns:
        Default branch name (e.g., "main", "master", "develop")
    """
    import subprocess

    # Method 1: Get from origin's HEAD
    result = subprocess.run(
        ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
        cwd=repo_path,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=5,
    )

    if result.returncode == 0:
        # Output: "refs/remotes/origin/main" → extract "main"
        ref = result.stdout.strip()
        return ref.split("/")[-1]

    # Method 2: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        result = subprocess.run(
            ["git", "rev-parse", "--verify", branch],
            cwd=repo_path,
            capture_output=True,
            timeout=5,
        )
        if result.returncode != 0:
            return branch

    # Method 3: Fallback
    return "main"


def x_get_default_branch__mutmut_61(repo_path: Path) -> str:
    """
    Get the default/base branch name for the repository (for stale detection).

    This is used to find the branch that feature branches diverged FROM.
    Unlike resolve_primary_branch() in git_ops, this does NOT use the current
    branch because stale detection always runs from worktrees where the current
    branch is always the feature branch, never the base branch.

    Tries multiple methods to detect the default branch:
    1. Check origin's HEAD symbolic ref
    2. Check which common branch exists (main, master, develop)
    3. Fallback to "main"

    Args:
        repo_path: Path to the repository

    Returns:
        Default branch name (e.g., "main", "master", "develop")
    """
    import subprocess

    # Method 1: Get from origin's HEAD
    result = subprocess.run(
        ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
        cwd=repo_path,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=5,
    )

    if result.returncode == 0:
        # Output: "refs/remotes/origin/main" → extract "main"
        ref = result.stdout.strip()
        return ref.split("/")[-1]

    # Method 2: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        result = subprocess.run(
            ["git", "rev-parse", "--verify", branch],
            cwd=repo_path,
            capture_output=True,
            timeout=5,
        )
        if result.returncode == 1:
            return branch

    # Method 3: Fallback
    return "main"


def x_get_default_branch__mutmut_62(repo_path: Path) -> str:
    """
    Get the default/base branch name for the repository (for stale detection).

    This is used to find the branch that feature branches diverged FROM.
    Unlike resolve_primary_branch() in git_ops, this does NOT use the current
    branch because stale detection always runs from worktrees where the current
    branch is always the feature branch, never the base branch.

    Tries multiple methods to detect the default branch:
    1. Check origin's HEAD symbolic ref
    2. Check which common branch exists (main, master, develop)
    3. Fallback to "main"

    Args:
        repo_path: Path to the repository

    Returns:
        Default branch name (e.g., "main", "master", "develop")
    """
    import subprocess

    # Method 1: Get from origin's HEAD
    result = subprocess.run(
        ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
        cwd=repo_path,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=5,
    )

    if result.returncode == 0:
        # Output: "refs/remotes/origin/main" → extract "main"
        ref = result.stdout.strip()
        return ref.split("/")[-1]

    # Method 2: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        result = subprocess.run(
            ["git", "rev-parse", "--verify", branch],
            cwd=repo_path,
            capture_output=True,
            timeout=5,
        )
        if result.returncode == 0:
            return branch

    # Method 3: Fallback
    return "XXmainXX"


def x_get_default_branch__mutmut_63(repo_path: Path) -> str:
    """
    Get the default/base branch name for the repository (for stale detection).

    This is used to find the branch that feature branches diverged FROM.
    Unlike resolve_primary_branch() in git_ops, this does NOT use the current
    branch because stale detection always runs from worktrees where the current
    branch is always the feature branch, never the base branch.

    Tries multiple methods to detect the default branch:
    1. Check origin's HEAD symbolic ref
    2. Check which common branch exists (main, master, develop)
    3. Fallback to "main"

    Args:
        repo_path: Path to the repository

    Returns:
        Default branch name (e.g., "main", "master", "develop")
    """
    import subprocess

    # Method 1: Get from origin's HEAD
    result = subprocess.run(
        ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
        cwd=repo_path,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=5,
    )

    if result.returncode == 0:
        # Output: "refs/remotes/origin/main" → extract "main"
        ref = result.stdout.strip()
        return ref.split("/")[-1]

    # Method 2: Check which common branch exists
    for branch in ["main", "master", "develop"]:
        result = subprocess.run(
            ["git", "rev-parse", "--verify", branch],
            cwd=repo_path,
            capture_output=True,
            timeout=5,
        )
        if result.returncode == 0:
            return branch

    # Method 3: Fallback
    return "MAIN"

x_get_default_branch__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_get_default_branch__mutmut_1': x_get_default_branch__mutmut_1, 
    'x_get_default_branch__mutmut_2': x_get_default_branch__mutmut_2, 
    'x_get_default_branch__mutmut_3': x_get_default_branch__mutmut_3, 
    'x_get_default_branch__mutmut_4': x_get_default_branch__mutmut_4, 
    'x_get_default_branch__mutmut_5': x_get_default_branch__mutmut_5, 
    'x_get_default_branch__mutmut_6': x_get_default_branch__mutmut_6, 
    'x_get_default_branch__mutmut_7': x_get_default_branch__mutmut_7, 
    'x_get_default_branch__mutmut_8': x_get_default_branch__mutmut_8, 
    'x_get_default_branch__mutmut_9': x_get_default_branch__mutmut_9, 
    'x_get_default_branch__mutmut_10': x_get_default_branch__mutmut_10, 
    'x_get_default_branch__mutmut_11': x_get_default_branch__mutmut_11, 
    'x_get_default_branch__mutmut_12': x_get_default_branch__mutmut_12, 
    'x_get_default_branch__mutmut_13': x_get_default_branch__mutmut_13, 
    'x_get_default_branch__mutmut_14': x_get_default_branch__mutmut_14, 
    'x_get_default_branch__mutmut_15': x_get_default_branch__mutmut_15, 
    'x_get_default_branch__mutmut_16': x_get_default_branch__mutmut_16, 
    'x_get_default_branch__mutmut_17': x_get_default_branch__mutmut_17, 
    'x_get_default_branch__mutmut_18': x_get_default_branch__mutmut_18, 
    'x_get_default_branch__mutmut_19': x_get_default_branch__mutmut_19, 
    'x_get_default_branch__mutmut_20': x_get_default_branch__mutmut_20, 
    'x_get_default_branch__mutmut_21': x_get_default_branch__mutmut_21, 
    'x_get_default_branch__mutmut_22': x_get_default_branch__mutmut_22, 
    'x_get_default_branch__mutmut_23': x_get_default_branch__mutmut_23, 
    'x_get_default_branch__mutmut_24': x_get_default_branch__mutmut_24, 
    'x_get_default_branch__mutmut_25': x_get_default_branch__mutmut_25, 
    'x_get_default_branch__mutmut_26': x_get_default_branch__mutmut_26, 
    'x_get_default_branch__mutmut_27': x_get_default_branch__mutmut_27, 
    'x_get_default_branch__mutmut_28': x_get_default_branch__mutmut_28, 
    'x_get_default_branch__mutmut_29': x_get_default_branch__mutmut_29, 
    'x_get_default_branch__mutmut_30': x_get_default_branch__mutmut_30, 
    'x_get_default_branch__mutmut_31': x_get_default_branch__mutmut_31, 
    'x_get_default_branch__mutmut_32': x_get_default_branch__mutmut_32, 
    'x_get_default_branch__mutmut_33': x_get_default_branch__mutmut_33, 
    'x_get_default_branch__mutmut_34': x_get_default_branch__mutmut_34, 
    'x_get_default_branch__mutmut_35': x_get_default_branch__mutmut_35, 
    'x_get_default_branch__mutmut_36': x_get_default_branch__mutmut_36, 
    'x_get_default_branch__mutmut_37': x_get_default_branch__mutmut_37, 
    'x_get_default_branch__mutmut_38': x_get_default_branch__mutmut_38, 
    'x_get_default_branch__mutmut_39': x_get_default_branch__mutmut_39, 
    'x_get_default_branch__mutmut_40': x_get_default_branch__mutmut_40, 
    'x_get_default_branch__mutmut_41': x_get_default_branch__mutmut_41, 
    'x_get_default_branch__mutmut_42': x_get_default_branch__mutmut_42, 
    'x_get_default_branch__mutmut_43': x_get_default_branch__mutmut_43, 
    'x_get_default_branch__mutmut_44': x_get_default_branch__mutmut_44, 
    'x_get_default_branch__mutmut_45': x_get_default_branch__mutmut_45, 
    'x_get_default_branch__mutmut_46': x_get_default_branch__mutmut_46, 
    'x_get_default_branch__mutmut_47': x_get_default_branch__mutmut_47, 
    'x_get_default_branch__mutmut_48': x_get_default_branch__mutmut_48, 
    'x_get_default_branch__mutmut_49': x_get_default_branch__mutmut_49, 
    'x_get_default_branch__mutmut_50': x_get_default_branch__mutmut_50, 
    'x_get_default_branch__mutmut_51': x_get_default_branch__mutmut_51, 
    'x_get_default_branch__mutmut_52': x_get_default_branch__mutmut_52, 
    'x_get_default_branch__mutmut_53': x_get_default_branch__mutmut_53, 
    'x_get_default_branch__mutmut_54': x_get_default_branch__mutmut_54, 
    'x_get_default_branch__mutmut_55': x_get_default_branch__mutmut_55, 
    'x_get_default_branch__mutmut_56': x_get_default_branch__mutmut_56, 
    'x_get_default_branch__mutmut_57': x_get_default_branch__mutmut_57, 
    'x_get_default_branch__mutmut_58': x_get_default_branch__mutmut_58, 
    'x_get_default_branch__mutmut_59': x_get_default_branch__mutmut_59, 
    'x_get_default_branch__mutmut_60': x_get_default_branch__mutmut_60, 
    'x_get_default_branch__mutmut_61': x_get_default_branch__mutmut_61, 
    'x_get_default_branch__mutmut_62': x_get_default_branch__mutmut_62, 
    'x_get_default_branch__mutmut_63': x_get_default_branch__mutmut_63
}
x_get_default_branch__mutmut_orig.__name__ = 'x_get_default_branch'


def get_last_meaningful_commit_time(worktree_path: Path) -> tuple[datetime | None, bool]:
    args = [worktree_path]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_get_last_meaningful_commit_time__mutmut_orig, x_get_last_meaningful_commit_time__mutmut_mutants, args, kwargs, None)


def x_get_last_meaningful_commit_time__mutmut_orig(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_1(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_2(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, True

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_3(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = None

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_4(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(None)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_5(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = None

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_6(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            None,
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_7(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=None,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_8(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=None,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_9(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=None,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_10(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding=None,
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_11(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors=None,
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_12(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=None,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_13(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_14(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_15(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_16(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_17(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_18(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_19(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_20(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["XXgitXX", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_21(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["GIT", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_22(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "XXmerge-baseXX", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_23(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "MERGE-BASE", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_24(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "XXHEADXX", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_25(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "head", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_26(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=False,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_27(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=False,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_28(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="XXutf-8XX",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_29(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="UTF-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_30(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="XXreplaceXX",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_31(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="REPLACE",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_32(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=11,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_33(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode == 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_34(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 1:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_35(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, True

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_36(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = None

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_37(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = None

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_38(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            None,
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_39(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=None,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_40(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=None,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_41(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=None,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_42(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding=None,
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_43(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors=None,
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_44(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=None,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_45(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_46(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_47(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_48(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_49(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_50(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_51(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_52(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["XXgitXX", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_53(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["GIT", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_54(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "XXrev-listXX", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_55(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "REV-LIST", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_56(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "XX--countXX", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_57(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--COUNT", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_58(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=False,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_59(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=False,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_60(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="XXutf-8XX",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_61(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="UTF-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_62(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="XXreplaceXX",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_63(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="REPLACE",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_64(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=11,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_65(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode != 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_66(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 1:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_67(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = None
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_68(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(None)
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_69(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count != 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_70(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 1:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_71(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, True

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_72(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = None

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_73(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            None,
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_74(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=None,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_75(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=None,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_76(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=None,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_77(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding=None,
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_78(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors=None,
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_79(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=None,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_80(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_81(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_82(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_83(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_84(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_85(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_86(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_87(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["XXgitXX", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_88(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["GIT", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_89(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "XXlogXX", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_90(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "LOG", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_91(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "XX-1XX", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_92(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "XX--format=%cIXX"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_93(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%ci"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_94(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--FORMAT=%CI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_95(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=False,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_96(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=False,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_97(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="XXutf-8XX",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_98(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="UTF-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_99(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="XXreplaceXX",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_100(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="REPLACE",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_101(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=11,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_102(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 and not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_103(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode == 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_104(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 1 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_105(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_106(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, True

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_107(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = None
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_108(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(None), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_109(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), False

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_110(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, True
    except Exception:
        return None, False


def x_get_last_meaningful_commit_time__mutmut_111(worktree_path: Path) -> tuple[datetime | None, bool]:
    """
    Get the timestamp of the most recent meaningful commit in a worktree.

    A "meaningful" commit is one made ON THIS BRANCH since it diverged from main.
    This prevents false staleness when a worktree is just created but no commits
    have been made yet (HEAD points to parent branch's old commit).

    For worktrees, we always use git to check the branch-specific history,
    even in jj colocated repos. This is because:
    - jj's shared history includes commits from ALL workspaces
    - jj continuously auto-snapshots the working copy
    - We need the last commit on THIS worktree's branch, not the shared history

    Args:
        worktree_path: Path to the worktree

    Returns:
        Tuple of (datetime of last commit on this branch, has_own_commits).
        has_own_commits is False if the branch has no commits since diverging from main.
    """
    import subprocess

    if not worktree_path.exists():
        return None, False

    try:
        # Detect the actual default branch name (main, master, develop, etc.)
        default_branch = get_default_branch(worktree_path)

        # First, check if this branch has any commits since diverging from the default branch
        # This prevents false staleness when worktree was just created
        merge_base_result = subprocess.run(
            ["git", "merge-base", "HEAD", default_branch],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if merge_base_result.returncode != 0:
            # Merge-base failed - branch might not exist, detached HEAD, etc.
            # Return None to avoid using wrong commit timestamp from parent branch
            return None, False

        merge_base = merge_base_result.stdout.strip()

        # Count commits on this branch since the merge base
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{merge_base}..HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if count_result.returncode == 0:
            commit_count = int(count_result.stdout.strip())
            if commit_count == 0:
                # No commits on this branch yet - worktree just created
                # Don't flag as stale since agent just started
                return None, False

        # Get the last commit time on this branch
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None, False

        # Parse ISO format timestamp
        timestamp_str = result.stdout.strip()
        return datetime.fromisoformat(timestamp_str), True

    except subprocess.TimeoutExpired:
        return None, False
    except Exception:
        return None, True

x_get_last_meaningful_commit_time__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_get_last_meaningful_commit_time__mutmut_1': x_get_last_meaningful_commit_time__mutmut_1, 
    'x_get_last_meaningful_commit_time__mutmut_2': x_get_last_meaningful_commit_time__mutmut_2, 
    'x_get_last_meaningful_commit_time__mutmut_3': x_get_last_meaningful_commit_time__mutmut_3, 
    'x_get_last_meaningful_commit_time__mutmut_4': x_get_last_meaningful_commit_time__mutmut_4, 
    'x_get_last_meaningful_commit_time__mutmut_5': x_get_last_meaningful_commit_time__mutmut_5, 
    'x_get_last_meaningful_commit_time__mutmut_6': x_get_last_meaningful_commit_time__mutmut_6, 
    'x_get_last_meaningful_commit_time__mutmut_7': x_get_last_meaningful_commit_time__mutmut_7, 
    'x_get_last_meaningful_commit_time__mutmut_8': x_get_last_meaningful_commit_time__mutmut_8, 
    'x_get_last_meaningful_commit_time__mutmut_9': x_get_last_meaningful_commit_time__mutmut_9, 
    'x_get_last_meaningful_commit_time__mutmut_10': x_get_last_meaningful_commit_time__mutmut_10, 
    'x_get_last_meaningful_commit_time__mutmut_11': x_get_last_meaningful_commit_time__mutmut_11, 
    'x_get_last_meaningful_commit_time__mutmut_12': x_get_last_meaningful_commit_time__mutmut_12, 
    'x_get_last_meaningful_commit_time__mutmut_13': x_get_last_meaningful_commit_time__mutmut_13, 
    'x_get_last_meaningful_commit_time__mutmut_14': x_get_last_meaningful_commit_time__mutmut_14, 
    'x_get_last_meaningful_commit_time__mutmut_15': x_get_last_meaningful_commit_time__mutmut_15, 
    'x_get_last_meaningful_commit_time__mutmut_16': x_get_last_meaningful_commit_time__mutmut_16, 
    'x_get_last_meaningful_commit_time__mutmut_17': x_get_last_meaningful_commit_time__mutmut_17, 
    'x_get_last_meaningful_commit_time__mutmut_18': x_get_last_meaningful_commit_time__mutmut_18, 
    'x_get_last_meaningful_commit_time__mutmut_19': x_get_last_meaningful_commit_time__mutmut_19, 
    'x_get_last_meaningful_commit_time__mutmut_20': x_get_last_meaningful_commit_time__mutmut_20, 
    'x_get_last_meaningful_commit_time__mutmut_21': x_get_last_meaningful_commit_time__mutmut_21, 
    'x_get_last_meaningful_commit_time__mutmut_22': x_get_last_meaningful_commit_time__mutmut_22, 
    'x_get_last_meaningful_commit_time__mutmut_23': x_get_last_meaningful_commit_time__mutmut_23, 
    'x_get_last_meaningful_commit_time__mutmut_24': x_get_last_meaningful_commit_time__mutmut_24, 
    'x_get_last_meaningful_commit_time__mutmut_25': x_get_last_meaningful_commit_time__mutmut_25, 
    'x_get_last_meaningful_commit_time__mutmut_26': x_get_last_meaningful_commit_time__mutmut_26, 
    'x_get_last_meaningful_commit_time__mutmut_27': x_get_last_meaningful_commit_time__mutmut_27, 
    'x_get_last_meaningful_commit_time__mutmut_28': x_get_last_meaningful_commit_time__mutmut_28, 
    'x_get_last_meaningful_commit_time__mutmut_29': x_get_last_meaningful_commit_time__mutmut_29, 
    'x_get_last_meaningful_commit_time__mutmut_30': x_get_last_meaningful_commit_time__mutmut_30, 
    'x_get_last_meaningful_commit_time__mutmut_31': x_get_last_meaningful_commit_time__mutmut_31, 
    'x_get_last_meaningful_commit_time__mutmut_32': x_get_last_meaningful_commit_time__mutmut_32, 
    'x_get_last_meaningful_commit_time__mutmut_33': x_get_last_meaningful_commit_time__mutmut_33, 
    'x_get_last_meaningful_commit_time__mutmut_34': x_get_last_meaningful_commit_time__mutmut_34, 
    'x_get_last_meaningful_commit_time__mutmut_35': x_get_last_meaningful_commit_time__mutmut_35, 
    'x_get_last_meaningful_commit_time__mutmut_36': x_get_last_meaningful_commit_time__mutmut_36, 
    'x_get_last_meaningful_commit_time__mutmut_37': x_get_last_meaningful_commit_time__mutmut_37, 
    'x_get_last_meaningful_commit_time__mutmut_38': x_get_last_meaningful_commit_time__mutmut_38, 
    'x_get_last_meaningful_commit_time__mutmut_39': x_get_last_meaningful_commit_time__mutmut_39, 
    'x_get_last_meaningful_commit_time__mutmut_40': x_get_last_meaningful_commit_time__mutmut_40, 
    'x_get_last_meaningful_commit_time__mutmut_41': x_get_last_meaningful_commit_time__mutmut_41, 
    'x_get_last_meaningful_commit_time__mutmut_42': x_get_last_meaningful_commit_time__mutmut_42, 
    'x_get_last_meaningful_commit_time__mutmut_43': x_get_last_meaningful_commit_time__mutmut_43, 
    'x_get_last_meaningful_commit_time__mutmut_44': x_get_last_meaningful_commit_time__mutmut_44, 
    'x_get_last_meaningful_commit_time__mutmut_45': x_get_last_meaningful_commit_time__mutmut_45, 
    'x_get_last_meaningful_commit_time__mutmut_46': x_get_last_meaningful_commit_time__mutmut_46, 
    'x_get_last_meaningful_commit_time__mutmut_47': x_get_last_meaningful_commit_time__mutmut_47, 
    'x_get_last_meaningful_commit_time__mutmut_48': x_get_last_meaningful_commit_time__mutmut_48, 
    'x_get_last_meaningful_commit_time__mutmut_49': x_get_last_meaningful_commit_time__mutmut_49, 
    'x_get_last_meaningful_commit_time__mutmut_50': x_get_last_meaningful_commit_time__mutmut_50, 
    'x_get_last_meaningful_commit_time__mutmut_51': x_get_last_meaningful_commit_time__mutmut_51, 
    'x_get_last_meaningful_commit_time__mutmut_52': x_get_last_meaningful_commit_time__mutmut_52, 
    'x_get_last_meaningful_commit_time__mutmut_53': x_get_last_meaningful_commit_time__mutmut_53, 
    'x_get_last_meaningful_commit_time__mutmut_54': x_get_last_meaningful_commit_time__mutmut_54, 
    'x_get_last_meaningful_commit_time__mutmut_55': x_get_last_meaningful_commit_time__mutmut_55, 
    'x_get_last_meaningful_commit_time__mutmut_56': x_get_last_meaningful_commit_time__mutmut_56, 
    'x_get_last_meaningful_commit_time__mutmut_57': x_get_last_meaningful_commit_time__mutmut_57, 
    'x_get_last_meaningful_commit_time__mutmut_58': x_get_last_meaningful_commit_time__mutmut_58, 
    'x_get_last_meaningful_commit_time__mutmut_59': x_get_last_meaningful_commit_time__mutmut_59, 
    'x_get_last_meaningful_commit_time__mutmut_60': x_get_last_meaningful_commit_time__mutmut_60, 
    'x_get_last_meaningful_commit_time__mutmut_61': x_get_last_meaningful_commit_time__mutmut_61, 
    'x_get_last_meaningful_commit_time__mutmut_62': x_get_last_meaningful_commit_time__mutmut_62, 
    'x_get_last_meaningful_commit_time__mutmut_63': x_get_last_meaningful_commit_time__mutmut_63, 
    'x_get_last_meaningful_commit_time__mutmut_64': x_get_last_meaningful_commit_time__mutmut_64, 
    'x_get_last_meaningful_commit_time__mutmut_65': x_get_last_meaningful_commit_time__mutmut_65, 
    'x_get_last_meaningful_commit_time__mutmut_66': x_get_last_meaningful_commit_time__mutmut_66, 
    'x_get_last_meaningful_commit_time__mutmut_67': x_get_last_meaningful_commit_time__mutmut_67, 
    'x_get_last_meaningful_commit_time__mutmut_68': x_get_last_meaningful_commit_time__mutmut_68, 
    'x_get_last_meaningful_commit_time__mutmut_69': x_get_last_meaningful_commit_time__mutmut_69, 
    'x_get_last_meaningful_commit_time__mutmut_70': x_get_last_meaningful_commit_time__mutmut_70, 
    'x_get_last_meaningful_commit_time__mutmut_71': x_get_last_meaningful_commit_time__mutmut_71, 
    'x_get_last_meaningful_commit_time__mutmut_72': x_get_last_meaningful_commit_time__mutmut_72, 
    'x_get_last_meaningful_commit_time__mutmut_73': x_get_last_meaningful_commit_time__mutmut_73, 
    'x_get_last_meaningful_commit_time__mutmut_74': x_get_last_meaningful_commit_time__mutmut_74, 
    'x_get_last_meaningful_commit_time__mutmut_75': x_get_last_meaningful_commit_time__mutmut_75, 
    'x_get_last_meaningful_commit_time__mutmut_76': x_get_last_meaningful_commit_time__mutmut_76, 
    'x_get_last_meaningful_commit_time__mutmut_77': x_get_last_meaningful_commit_time__mutmut_77, 
    'x_get_last_meaningful_commit_time__mutmut_78': x_get_last_meaningful_commit_time__mutmut_78, 
    'x_get_last_meaningful_commit_time__mutmut_79': x_get_last_meaningful_commit_time__mutmut_79, 
    'x_get_last_meaningful_commit_time__mutmut_80': x_get_last_meaningful_commit_time__mutmut_80, 
    'x_get_last_meaningful_commit_time__mutmut_81': x_get_last_meaningful_commit_time__mutmut_81, 
    'x_get_last_meaningful_commit_time__mutmut_82': x_get_last_meaningful_commit_time__mutmut_82, 
    'x_get_last_meaningful_commit_time__mutmut_83': x_get_last_meaningful_commit_time__mutmut_83, 
    'x_get_last_meaningful_commit_time__mutmut_84': x_get_last_meaningful_commit_time__mutmut_84, 
    'x_get_last_meaningful_commit_time__mutmut_85': x_get_last_meaningful_commit_time__mutmut_85, 
    'x_get_last_meaningful_commit_time__mutmut_86': x_get_last_meaningful_commit_time__mutmut_86, 
    'x_get_last_meaningful_commit_time__mutmut_87': x_get_last_meaningful_commit_time__mutmut_87, 
    'x_get_last_meaningful_commit_time__mutmut_88': x_get_last_meaningful_commit_time__mutmut_88, 
    'x_get_last_meaningful_commit_time__mutmut_89': x_get_last_meaningful_commit_time__mutmut_89, 
    'x_get_last_meaningful_commit_time__mutmut_90': x_get_last_meaningful_commit_time__mutmut_90, 
    'x_get_last_meaningful_commit_time__mutmut_91': x_get_last_meaningful_commit_time__mutmut_91, 
    'x_get_last_meaningful_commit_time__mutmut_92': x_get_last_meaningful_commit_time__mutmut_92, 
    'x_get_last_meaningful_commit_time__mutmut_93': x_get_last_meaningful_commit_time__mutmut_93, 
    'x_get_last_meaningful_commit_time__mutmut_94': x_get_last_meaningful_commit_time__mutmut_94, 
    'x_get_last_meaningful_commit_time__mutmut_95': x_get_last_meaningful_commit_time__mutmut_95, 
    'x_get_last_meaningful_commit_time__mutmut_96': x_get_last_meaningful_commit_time__mutmut_96, 
    'x_get_last_meaningful_commit_time__mutmut_97': x_get_last_meaningful_commit_time__mutmut_97, 
    'x_get_last_meaningful_commit_time__mutmut_98': x_get_last_meaningful_commit_time__mutmut_98, 
    'x_get_last_meaningful_commit_time__mutmut_99': x_get_last_meaningful_commit_time__mutmut_99, 
    'x_get_last_meaningful_commit_time__mutmut_100': x_get_last_meaningful_commit_time__mutmut_100, 
    'x_get_last_meaningful_commit_time__mutmut_101': x_get_last_meaningful_commit_time__mutmut_101, 
    'x_get_last_meaningful_commit_time__mutmut_102': x_get_last_meaningful_commit_time__mutmut_102, 
    'x_get_last_meaningful_commit_time__mutmut_103': x_get_last_meaningful_commit_time__mutmut_103, 
    'x_get_last_meaningful_commit_time__mutmut_104': x_get_last_meaningful_commit_time__mutmut_104, 
    'x_get_last_meaningful_commit_time__mutmut_105': x_get_last_meaningful_commit_time__mutmut_105, 
    'x_get_last_meaningful_commit_time__mutmut_106': x_get_last_meaningful_commit_time__mutmut_106, 
    'x_get_last_meaningful_commit_time__mutmut_107': x_get_last_meaningful_commit_time__mutmut_107, 
    'x_get_last_meaningful_commit_time__mutmut_108': x_get_last_meaningful_commit_time__mutmut_108, 
    'x_get_last_meaningful_commit_time__mutmut_109': x_get_last_meaningful_commit_time__mutmut_109, 
    'x_get_last_meaningful_commit_time__mutmut_110': x_get_last_meaningful_commit_time__mutmut_110, 
    'x_get_last_meaningful_commit_time__mutmut_111': x_get_last_meaningful_commit_time__mutmut_111
}
x_get_last_meaningful_commit_time__mutmut_orig.__name__ = 'x_get_last_meaningful_commit_time'


def check_wp_staleness(
    wp_id: str,
    worktree_path: Path,
    threshold_minutes: int = 10,
) -> StaleCheckResult:
    args = [wp_id, worktree_path, threshold_minutes]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_check_wp_staleness__mutmut_orig, x_check_wp_staleness__mutmut_mutants, args, kwargs, None)


def x_check_wp_staleness__mutmut_orig(
    wp_id: str,
    worktree_path: Path,
    threshold_minutes: int = 10,
) -> StaleCheckResult:
    """
    Check if a work package is stale based on VCS activity.

    A WP is considered stale if:
    - Its worktree exists
    - The branch has commits since diverging from main (agent has done work)
    - The last commit is older than threshold_minutes

    A WP with a worktree but NO commits since diverging is NOT stale - the agent
    just started and hasn't committed yet.

    Args:
        wp_id: Work package ID (e.g., "WP01")
        worktree_path: Path to the WP's worktree
        threshold_minutes: Minutes of inactivity before considered stale

    Returns:
        StaleCheckResult with staleness status
    """
    if not worktree_path.exists():
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=False,
        )

    try:
        last_commit, has_own_commits = get_last_meaningful_commit_time(worktree_path)

        if last_commit is None:
            # Can't determine commit time, or no commits on this branch yet
            # If no commits yet (has_own_commits=False), agent just started - not stale
            return StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=True,
                error=None if not has_own_commits else "Could not determine last commit time",
            )

        now = datetime.now(timezone.utc)
        # Ensure last_commit is timezone-aware
        if last_commit.tzinfo is None:
            last_commit = last_commit.replace(tzinfo=timezone.utc)

        delta = now - last_commit
        minutes_since = delta.total_seconds() / 60

        is_stale = minutes_since > threshold_minutes

        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=is_stale,
            last_commit_time=last_commit,
            minutes_since_commit=round(minutes_since, 1),
            worktree_exists=True,
        )

    except Exception as e:
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=True,
            error=str(e),
        )


def x_check_wp_staleness__mutmut_1(
    wp_id: str,
    worktree_path: Path,
    threshold_minutes: int = 11,
) -> StaleCheckResult:
    """
    Check if a work package is stale based on VCS activity.

    A WP is considered stale if:
    - Its worktree exists
    - The branch has commits since diverging from main (agent has done work)
    - The last commit is older than threshold_minutes

    A WP with a worktree but NO commits since diverging is NOT stale - the agent
    just started and hasn't committed yet.

    Args:
        wp_id: Work package ID (e.g., "WP01")
        worktree_path: Path to the WP's worktree
        threshold_minutes: Minutes of inactivity before considered stale

    Returns:
        StaleCheckResult with staleness status
    """
    if not worktree_path.exists():
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=False,
        )

    try:
        last_commit, has_own_commits = get_last_meaningful_commit_time(worktree_path)

        if last_commit is None:
            # Can't determine commit time, or no commits on this branch yet
            # If no commits yet (has_own_commits=False), agent just started - not stale
            return StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=True,
                error=None if not has_own_commits else "Could not determine last commit time",
            )

        now = datetime.now(timezone.utc)
        # Ensure last_commit is timezone-aware
        if last_commit.tzinfo is None:
            last_commit = last_commit.replace(tzinfo=timezone.utc)

        delta = now - last_commit
        minutes_since = delta.total_seconds() / 60

        is_stale = minutes_since > threshold_minutes

        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=is_stale,
            last_commit_time=last_commit,
            minutes_since_commit=round(minutes_since, 1),
            worktree_exists=True,
        )

    except Exception as e:
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=True,
            error=str(e),
        )


def x_check_wp_staleness__mutmut_2(
    wp_id: str,
    worktree_path: Path,
    threshold_minutes: int = 10,
) -> StaleCheckResult:
    """
    Check if a work package is stale based on VCS activity.

    A WP is considered stale if:
    - Its worktree exists
    - The branch has commits since diverging from main (agent has done work)
    - The last commit is older than threshold_minutes

    A WP with a worktree but NO commits since diverging is NOT stale - the agent
    just started and hasn't committed yet.

    Args:
        wp_id: Work package ID (e.g., "WP01")
        worktree_path: Path to the WP's worktree
        threshold_minutes: Minutes of inactivity before considered stale

    Returns:
        StaleCheckResult with staleness status
    """
    if worktree_path.exists():
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=False,
        )

    try:
        last_commit, has_own_commits = get_last_meaningful_commit_time(worktree_path)

        if last_commit is None:
            # Can't determine commit time, or no commits on this branch yet
            # If no commits yet (has_own_commits=False), agent just started - not stale
            return StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=True,
                error=None if not has_own_commits else "Could not determine last commit time",
            )

        now = datetime.now(timezone.utc)
        # Ensure last_commit is timezone-aware
        if last_commit.tzinfo is None:
            last_commit = last_commit.replace(tzinfo=timezone.utc)

        delta = now - last_commit
        minutes_since = delta.total_seconds() / 60

        is_stale = minutes_since > threshold_minutes

        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=is_stale,
            last_commit_time=last_commit,
            minutes_since_commit=round(minutes_since, 1),
            worktree_exists=True,
        )

    except Exception as e:
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=True,
            error=str(e),
        )


def x_check_wp_staleness__mutmut_3(
    wp_id: str,
    worktree_path: Path,
    threshold_minutes: int = 10,
) -> StaleCheckResult:
    """
    Check if a work package is stale based on VCS activity.

    A WP is considered stale if:
    - Its worktree exists
    - The branch has commits since diverging from main (agent has done work)
    - The last commit is older than threshold_minutes

    A WP with a worktree but NO commits since diverging is NOT stale - the agent
    just started and hasn't committed yet.

    Args:
        wp_id: Work package ID (e.g., "WP01")
        worktree_path: Path to the WP's worktree
        threshold_minutes: Minutes of inactivity before considered stale

    Returns:
        StaleCheckResult with staleness status
    """
    if not worktree_path.exists():
        return StaleCheckResult(
            wp_id=None,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=False,
        )

    try:
        last_commit, has_own_commits = get_last_meaningful_commit_time(worktree_path)

        if last_commit is None:
            # Can't determine commit time, or no commits on this branch yet
            # If no commits yet (has_own_commits=False), agent just started - not stale
            return StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=True,
                error=None if not has_own_commits else "Could not determine last commit time",
            )

        now = datetime.now(timezone.utc)
        # Ensure last_commit is timezone-aware
        if last_commit.tzinfo is None:
            last_commit = last_commit.replace(tzinfo=timezone.utc)

        delta = now - last_commit
        minutes_since = delta.total_seconds() / 60

        is_stale = minutes_since > threshold_minutes

        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=is_stale,
            last_commit_time=last_commit,
            minutes_since_commit=round(minutes_since, 1),
            worktree_exists=True,
        )

    except Exception as e:
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=True,
            error=str(e),
        )


def x_check_wp_staleness__mutmut_4(
    wp_id: str,
    worktree_path: Path,
    threshold_minutes: int = 10,
) -> StaleCheckResult:
    """
    Check if a work package is stale based on VCS activity.

    A WP is considered stale if:
    - Its worktree exists
    - The branch has commits since diverging from main (agent has done work)
    - The last commit is older than threshold_minutes

    A WP with a worktree but NO commits since diverging is NOT stale - the agent
    just started and hasn't committed yet.

    Args:
        wp_id: Work package ID (e.g., "WP01")
        worktree_path: Path to the WP's worktree
        threshold_minutes: Minutes of inactivity before considered stale

    Returns:
        StaleCheckResult with staleness status
    """
    if not worktree_path.exists():
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=None,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=False,
        )

    try:
        last_commit, has_own_commits = get_last_meaningful_commit_time(worktree_path)

        if last_commit is None:
            # Can't determine commit time, or no commits on this branch yet
            # If no commits yet (has_own_commits=False), agent just started - not stale
            return StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=True,
                error=None if not has_own_commits else "Could not determine last commit time",
            )

        now = datetime.now(timezone.utc)
        # Ensure last_commit is timezone-aware
        if last_commit.tzinfo is None:
            last_commit = last_commit.replace(tzinfo=timezone.utc)

        delta = now - last_commit
        minutes_since = delta.total_seconds() / 60

        is_stale = minutes_since > threshold_minutes

        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=is_stale,
            last_commit_time=last_commit,
            minutes_since_commit=round(minutes_since, 1),
            worktree_exists=True,
        )

    except Exception as e:
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=True,
            error=str(e),
        )


def x_check_wp_staleness__mutmut_5(
    wp_id: str,
    worktree_path: Path,
    threshold_minutes: int = 10,
) -> StaleCheckResult:
    """
    Check if a work package is stale based on VCS activity.

    A WP is considered stale if:
    - Its worktree exists
    - The branch has commits since diverging from main (agent has done work)
    - The last commit is older than threshold_minutes

    A WP with a worktree but NO commits since diverging is NOT stale - the agent
    just started and hasn't committed yet.

    Args:
        wp_id: Work package ID (e.g., "WP01")
        worktree_path: Path to the WP's worktree
        threshold_minutes: Minutes of inactivity before considered stale

    Returns:
        StaleCheckResult with staleness status
    """
    if not worktree_path.exists():
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=None,
        )

    try:
        last_commit, has_own_commits = get_last_meaningful_commit_time(worktree_path)

        if last_commit is None:
            # Can't determine commit time, or no commits on this branch yet
            # If no commits yet (has_own_commits=False), agent just started - not stale
            return StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=True,
                error=None if not has_own_commits else "Could not determine last commit time",
            )

        now = datetime.now(timezone.utc)
        # Ensure last_commit is timezone-aware
        if last_commit.tzinfo is None:
            last_commit = last_commit.replace(tzinfo=timezone.utc)

        delta = now - last_commit
        minutes_since = delta.total_seconds() / 60

        is_stale = minutes_since > threshold_minutes

        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=is_stale,
            last_commit_time=last_commit,
            minutes_since_commit=round(minutes_since, 1),
            worktree_exists=True,
        )

    except Exception as e:
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=True,
            error=str(e),
        )


def x_check_wp_staleness__mutmut_6(
    wp_id: str,
    worktree_path: Path,
    threshold_minutes: int = 10,
) -> StaleCheckResult:
    """
    Check if a work package is stale based on VCS activity.

    A WP is considered stale if:
    - Its worktree exists
    - The branch has commits since diverging from main (agent has done work)
    - The last commit is older than threshold_minutes

    A WP with a worktree but NO commits since diverging is NOT stale - the agent
    just started and hasn't committed yet.

    Args:
        wp_id: Work package ID (e.g., "WP01")
        worktree_path: Path to the WP's worktree
        threshold_minutes: Minutes of inactivity before considered stale

    Returns:
        StaleCheckResult with staleness status
    """
    if not worktree_path.exists():
        return StaleCheckResult(
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=False,
        )

    try:
        last_commit, has_own_commits = get_last_meaningful_commit_time(worktree_path)

        if last_commit is None:
            # Can't determine commit time, or no commits on this branch yet
            # If no commits yet (has_own_commits=False), agent just started - not stale
            return StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=True,
                error=None if not has_own_commits else "Could not determine last commit time",
            )

        now = datetime.now(timezone.utc)
        # Ensure last_commit is timezone-aware
        if last_commit.tzinfo is None:
            last_commit = last_commit.replace(tzinfo=timezone.utc)

        delta = now - last_commit
        minutes_since = delta.total_seconds() / 60

        is_stale = minutes_since > threshold_minutes

        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=is_stale,
            last_commit_time=last_commit,
            minutes_since_commit=round(minutes_since, 1),
            worktree_exists=True,
        )

    except Exception as e:
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=True,
            error=str(e),
        )


def x_check_wp_staleness__mutmut_7(
    wp_id: str,
    worktree_path: Path,
    threshold_minutes: int = 10,
) -> StaleCheckResult:
    """
    Check if a work package is stale based on VCS activity.

    A WP is considered stale if:
    - Its worktree exists
    - The branch has commits since diverging from main (agent has done work)
    - The last commit is older than threshold_minutes

    A WP with a worktree but NO commits since diverging is NOT stale - the agent
    just started and hasn't committed yet.

    Args:
        wp_id: Work package ID (e.g., "WP01")
        worktree_path: Path to the WP's worktree
        threshold_minutes: Minutes of inactivity before considered stale

    Returns:
        StaleCheckResult with staleness status
    """
    if not worktree_path.exists():
        return StaleCheckResult(
            wp_id=wp_id,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=False,
        )

    try:
        last_commit, has_own_commits = get_last_meaningful_commit_time(worktree_path)

        if last_commit is None:
            # Can't determine commit time, or no commits on this branch yet
            # If no commits yet (has_own_commits=False), agent just started - not stale
            return StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=True,
                error=None if not has_own_commits else "Could not determine last commit time",
            )

        now = datetime.now(timezone.utc)
        # Ensure last_commit is timezone-aware
        if last_commit.tzinfo is None:
            last_commit = last_commit.replace(tzinfo=timezone.utc)

        delta = now - last_commit
        minutes_since = delta.total_seconds() / 60

        is_stale = minutes_since > threshold_minutes

        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=is_stale,
            last_commit_time=last_commit,
            minutes_since_commit=round(minutes_since, 1),
            worktree_exists=True,
        )

    except Exception as e:
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=True,
            error=str(e),
        )


def x_check_wp_staleness__mutmut_8(
    wp_id: str,
    worktree_path: Path,
    threshold_minutes: int = 10,
) -> StaleCheckResult:
    """
    Check if a work package is stale based on VCS activity.

    A WP is considered stale if:
    - Its worktree exists
    - The branch has commits since diverging from main (agent has done work)
    - The last commit is older than threshold_minutes

    A WP with a worktree but NO commits since diverging is NOT stale - the agent
    just started and hasn't committed yet.

    Args:
        wp_id: Work package ID (e.g., "WP01")
        worktree_path: Path to the WP's worktree
        threshold_minutes: Minutes of inactivity before considered stale

    Returns:
        StaleCheckResult with staleness status
    """
    if not worktree_path.exists():
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            minutes_since_commit=None,
            worktree_exists=False,
        )

    try:
        last_commit, has_own_commits = get_last_meaningful_commit_time(worktree_path)

        if last_commit is None:
            # Can't determine commit time, or no commits on this branch yet
            # If no commits yet (has_own_commits=False), agent just started - not stale
            return StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=True,
                error=None if not has_own_commits else "Could not determine last commit time",
            )

        now = datetime.now(timezone.utc)
        # Ensure last_commit is timezone-aware
        if last_commit.tzinfo is None:
            last_commit = last_commit.replace(tzinfo=timezone.utc)

        delta = now - last_commit
        minutes_since = delta.total_seconds() / 60

        is_stale = minutes_since > threshold_minutes

        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=is_stale,
            last_commit_time=last_commit,
            minutes_since_commit=round(minutes_since, 1),
            worktree_exists=True,
        )

    except Exception as e:
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=True,
            error=str(e),
        )


def x_check_wp_staleness__mutmut_9(
    wp_id: str,
    worktree_path: Path,
    threshold_minutes: int = 10,
) -> StaleCheckResult:
    """
    Check if a work package is stale based on VCS activity.

    A WP is considered stale if:
    - Its worktree exists
    - The branch has commits since diverging from main (agent has done work)
    - The last commit is older than threshold_minutes

    A WP with a worktree but NO commits since diverging is NOT stale - the agent
    just started and hasn't committed yet.

    Args:
        wp_id: Work package ID (e.g., "WP01")
        worktree_path: Path to the WP's worktree
        threshold_minutes: Minutes of inactivity before considered stale

    Returns:
        StaleCheckResult with staleness status
    """
    if not worktree_path.exists():
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            worktree_exists=False,
        )

    try:
        last_commit, has_own_commits = get_last_meaningful_commit_time(worktree_path)

        if last_commit is None:
            # Can't determine commit time, or no commits on this branch yet
            # If no commits yet (has_own_commits=False), agent just started - not stale
            return StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=True,
                error=None if not has_own_commits else "Could not determine last commit time",
            )

        now = datetime.now(timezone.utc)
        # Ensure last_commit is timezone-aware
        if last_commit.tzinfo is None:
            last_commit = last_commit.replace(tzinfo=timezone.utc)

        delta = now - last_commit
        minutes_since = delta.total_seconds() / 60

        is_stale = minutes_since > threshold_minutes

        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=is_stale,
            last_commit_time=last_commit,
            minutes_since_commit=round(minutes_since, 1),
            worktree_exists=True,
        )

    except Exception as e:
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=True,
            error=str(e),
        )


def x_check_wp_staleness__mutmut_10(
    wp_id: str,
    worktree_path: Path,
    threshold_minutes: int = 10,
) -> StaleCheckResult:
    """
    Check if a work package is stale based on VCS activity.

    A WP is considered stale if:
    - Its worktree exists
    - The branch has commits since diverging from main (agent has done work)
    - The last commit is older than threshold_minutes

    A WP with a worktree but NO commits since diverging is NOT stale - the agent
    just started and hasn't committed yet.

    Args:
        wp_id: Work package ID (e.g., "WP01")
        worktree_path: Path to the WP's worktree
        threshold_minutes: Minutes of inactivity before considered stale

    Returns:
        StaleCheckResult with staleness status
    """
    if not worktree_path.exists():
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            )

    try:
        last_commit, has_own_commits = get_last_meaningful_commit_time(worktree_path)

        if last_commit is None:
            # Can't determine commit time, or no commits on this branch yet
            # If no commits yet (has_own_commits=False), agent just started - not stale
            return StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=True,
                error=None if not has_own_commits else "Could not determine last commit time",
            )

        now = datetime.now(timezone.utc)
        # Ensure last_commit is timezone-aware
        if last_commit.tzinfo is None:
            last_commit = last_commit.replace(tzinfo=timezone.utc)

        delta = now - last_commit
        minutes_since = delta.total_seconds() / 60

        is_stale = minutes_since > threshold_minutes

        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=is_stale,
            last_commit_time=last_commit,
            minutes_since_commit=round(minutes_since, 1),
            worktree_exists=True,
        )

    except Exception as e:
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=True,
            error=str(e),
        )


def x_check_wp_staleness__mutmut_11(
    wp_id: str,
    worktree_path: Path,
    threshold_minutes: int = 10,
) -> StaleCheckResult:
    """
    Check if a work package is stale based on VCS activity.

    A WP is considered stale if:
    - Its worktree exists
    - The branch has commits since diverging from main (agent has done work)
    - The last commit is older than threshold_minutes

    A WP with a worktree but NO commits since diverging is NOT stale - the agent
    just started and hasn't committed yet.

    Args:
        wp_id: Work package ID (e.g., "WP01")
        worktree_path: Path to the WP's worktree
        threshold_minutes: Minutes of inactivity before considered stale

    Returns:
        StaleCheckResult with staleness status
    """
    if not worktree_path.exists():
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=True,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=False,
        )

    try:
        last_commit, has_own_commits = get_last_meaningful_commit_time(worktree_path)

        if last_commit is None:
            # Can't determine commit time, or no commits on this branch yet
            # If no commits yet (has_own_commits=False), agent just started - not stale
            return StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=True,
                error=None if not has_own_commits else "Could not determine last commit time",
            )

        now = datetime.now(timezone.utc)
        # Ensure last_commit is timezone-aware
        if last_commit.tzinfo is None:
            last_commit = last_commit.replace(tzinfo=timezone.utc)

        delta = now - last_commit
        minutes_since = delta.total_seconds() / 60

        is_stale = minutes_since > threshold_minutes

        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=is_stale,
            last_commit_time=last_commit,
            minutes_since_commit=round(minutes_since, 1),
            worktree_exists=True,
        )

    except Exception as e:
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=True,
            error=str(e),
        )


def x_check_wp_staleness__mutmut_12(
    wp_id: str,
    worktree_path: Path,
    threshold_minutes: int = 10,
) -> StaleCheckResult:
    """
    Check if a work package is stale based on VCS activity.

    A WP is considered stale if:
    - Its worktree exists
    - The branch has commits since diverging from main (agent has done work)
    - The last commit is older than threshold_minutes

    A WP with a worktree but NO commits since diverging is NOT stale - the agent
    just started and hasn't committed yet.

    Args:
        wp_id: Work package ID (e.g., "WP01")
        worktree_path: Path to the WP's worktree
        threshold_minutes: Minutes of inactivity before considered stale

    Returns:
        StaleCheckResult with staleness status
    """
    if not worktree_path.exists():
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=True,
        )

    try:
        last_commit, has_own_commits = get_last_meaningful_commit_time(worktree_path)

        if last_commit is None:
            # Can't determine commit time, or no commits on this branch yet
            # If no commits yet (has_own_commits=False), agent just started - not stale
            return StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=True,
                error=None if not has_own_commits else "Could not determine last commit time",
            )

        now = datetime.now(timezone.utc)
        # Ensure last_commit is timezone-aware
        if last_commit.tzinfo is None:
            last_commit = last_commit.replace(tzinfo=timezone.utc)

        delta = now - last_commit
        minutes_since = delta.total_seconds() / 60

        is_stale = minutes_since > threshold_minutes

        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=is_stale,
            last_commit_time=last_commit,
            minutes_since_commit=round(minutes_since, 1),
            worktree_exists=True,
        )

    except Exception as e:
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=True,
            error=str(e),
        )


def x_check_wp_staleness__mutmut_13(
    wp_id: str,
    worktree_path: Path,
    threshold_minutes: int = 10,
) -> StaleCheckResult:
    """
    Check if a work package is stale based on VCS activity.

    A WP is considered stale if:
    - Its worktree exists
    - The branch has commits since diverging from main (agent has done work)
    - The last commit is older than threshold_minutes

    A WP with a worktree but NO commits since diverging is NOT stale - the agent
    just started and hasn't committed yet.

    Args:
        wp_id: Work package ID (e.g., "WP01")
        worktree_path: Path to the WP's worktree
        threshold_minutes: Minutes of inactivity before considered stale

    Returns:
        StaleCheckResult with staleness status
    """
    if not worktree_path.exists():
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=False,
        )

    try:
        last_commit, has_own_commits = None

        if last_commit is None:
            # Can't determine commit time, or no commits on this branch yet
            # If no commits yet (has_own_commits=False), agent just started - not stale
            return StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=True,
                error=None if not has_own_commits else "Could not determine last commit time",
            )

        now = datetime.now(timezone.utc)
        # Ensure last_commit is timezone-aware
        if last_commit.tzinfo is None:
            last_commit = last_commit.replace(tzinfo=timezone.utc)

        delta = now - last_commit
        minutes_since = delta.total_seconds() / 60

        is_stale = minutes_since > threshold_minutes

        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=is_stale,
            last_commit_time=last_commit,
            minutes_since_commit=round(minutes_since, 1),
            worktree_exists=True,
        )

    except Exception as e:
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=True,
            error=str(e),
        )


def x_check_wp_staleness__mutmut_14(
    wp_id: str,
    worktree_path: Path,
    threshold_minutes: int = 10,
) -> StaleCheckResult:
    """
    Check if a work package is stale based on VCS activity.

    A WP is considered stale if:
    - Its worktree exists
    - The branch has commits since diverging from main (agent has done work)
    - The last commit is older than threshold_minutes

    A WP with a worktree but NO commits since diverging is NOT stale - the agent
    just started and hasn't committed yet.

    Args:
        wp_id: Work package ID (e.g., "WP01")
        worktree_path: Path to the WP's worktree
        threshold_minutes: Minutes of inactivity before considered stale

    Returns:
        StaleCheckResult with staleness status
    """
    if not worktree_path.exists():
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=False,
        )

    try:
        last_commit, has_own_commits = get_last_meaningful_commit_time(None)

        if last_commit is None:
            # Can't determine commit time, or no commits on this branch yet
            # If no commits yet (has_own_commits=False), agent just started - not stale
            return StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=True,
                error=None if not has_own_commits else "Could not determine last commit time",
            )

        now = datetime.now(timezone.utc)
        # Ensure last_commit is timezone-aware
        if last_commit.tzinfo is None:
            last_commit = last_commit.replace(tzinfo=timezone.utc)

        delta = now - last_commit
        minutes_since = delta.total_seconds() / 60

        is_stale = minutes_since > threshold_minutes

        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=is_stale,
            last_commit_time=last_commit,
            minutes_since_commit=round(minutes_since, 1),
            worktree_exists=True,
        )

    except Exception as e:
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=True,
            error=str(e),
        )


def x_check_wp_staleness__mutmut_15(
    wp_id: str,
    worktree_path: Path,
    threshold_minutes: int = 10,
) -> StaleCheckResult:
    """
    Check if a work package is stale based on VCS activity.

    A WP is considered stale if:
    - Its worktree exists
    - The branch has commits since diverging from main (agent has done work)
    - The last commit is older than threshold_minutes

    A WP with a worktree but NO commits since diverging is NOT stale - the agent
    just started and hasn't committed yet.

    Args:
        wp_id: Work package ID (e.g., "WP01")
        worktree_path: Path to the WP's worktree
        threshold_minutes: Minutes of inactivity before considered stale

    Returns:
        StaleCheckResult with staleness status
    """
    if not worktree_path.exists():
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=False,
        )

    try:
        last_commit, has_own_commits = get_last_meaningful_commit_time(worktree_path)

        if last_commit is not None:
            # Can't determine commit time, or no commits on this branch yet
            # If no commits yet (has_own_commits=False), agent just started - not stale
            return StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=True,
                error=None if not has_own_commits else "Could not determine last commit time",
            )

        now = datetime.now(timezone.utc)
        # Ensure last_commit is timezone-aware
        if last_commit.tzinfo is None:
            last_commit = last_commit.replace(tzinfo=timezone.utc)

        delta = now - last_commit
        minutes_since = delta.total_seconds() / 60

        is_stale = minutes_since > threshold_minutes

        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=is_stale,
            last_commit_time=last_commit,
            minutes_since_commit=round(minutes_since, 1),
            worktree_exists=True,
        )

    except Exception as e:
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=True,
            error=str(e),
        )


def x_check_wp_staleness__mutmut_16(
    wp_id: str,
    worktree_path: Path,
    threshold_minutes: int = 10,
) -> StaleCheckResult:
    """
    Check if a work package is stale based on VCS activity.

    A WP is considered stale if:
    - Its worktree exists
    - The branch has commits since diverging from main (agent has done work)
    - The last commit is older than threshold_minutes

    A WP with a worktree but NO commits since diverging is NOT stale - the agent
    just started and hasn't committed yet.

    Args:
        wp_id: Work package ID (e.g., "WP01")
        worktree_path: Path to the WP's worktree
        threshold_minutes: Minutes of inactivity before considered stale

    Returns:
        StaleCheckResult with staleness status
    """
    if not worktree_path.exists():
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=False,
        )

    try:
        last_commit, has_own_commits = get_last_meaningful_commit_time(worktree_path)

        if last_commit is None:
            # Can't determine commit time, or no commits on this branch yet
            # If no commits yet (has_own_commits=False), agent just started - not stale
            return StaleCheckResult(
                wp_id=None,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=True,
                error=None if not has_own_commits else "Could not determine last commit time",
            )

        now = datetime.now(timezone.utc)
        # Ensure last_commit is timezone-aware
        if last_commit.tzinfo is None:
            last_commit = last_commit.replace(tzinfo=timezone.utc)

        delta = now - last_commit
        minutes_since = delta.total_seconds() / 60

        is_stale = minutes_since > threshold_minutes

        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=is_stale,
            last_commit_time=last_commit,
            minutes_since_commit=round(minutes_since, 1),
            worktree_exists=True,
        )

    except Exception as e:
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=True,
            error=str(e),
        )


def x_check_wp_staleness__mutmut_17(
    wp_id: str,
    worktree_path: Path,
    threshold_minutes: int = 10,
) -> StaleCheckResult:
    """
    Check if a work package is stale based on VCS activity.

    A WP is considered stale if:
    - Its worktree exists
    - The branch has commits since diverging from main (agent has done work)
    - The last commit is older than threshold_minutes

    A WP with a worktree but NO commits since diverging is NOT stale - the agent
    just started and hasn't committed yet.

    Args:
        wp_id: Work package ID (e.g., "WP01")
        worktree_path: Path to the WP's worktree
        threshold_minutes: Minutes of inactivity before considered stale

    Returns:
        StaleCheckResult with staleness status
    """
    if not worktree_path.exists():
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=False,
        )

    try:
        last_commit, has_own_commits = get_last_meaningful_commit_time(worktree_path)

        if last_commit is None:
            # Can't determine commit time, or no commits on this branch yet
            # If no commits yet (has_own_commits=False), agent just started - not stale
            return StaleCheckResult(
                wp_id=wp_id,
                is_stale=None,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=True,
                error=None if not has_own_commits else "Could not determine last commit time",
            )

        now = datetime.now(timezone.utc)
        # Ensure last_commit is timezone-aware
        if last_commit.tzinfo is None:
            last_commit = last_commit.replace(tzinfo=timezone.utc)

        delta = now - last_commit
        minutes_since = delta.total_seconds() / 60

        is_stale = minutes_since > threshold_minutes

        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=is_stale,
            last_commit_time=last_commit,
            minutes_since_commit=round(minutes_since, 1),
            worktree_exists=True,
        )

    except Exception as e:
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=True,
            error=str(e),
        )


def x_check_wp_staleness__mutmut_18(
    wp_id: str,
    worktree_path: Path,
    threshold_minutes: int = 10,
) -> StaleCheckResult:
    """
    Check if a work package is stale based on VCS activity.

    A WP is considered stale if:
    - Its worktree exists
    - The branch has commits since diverging from main (agent has done work)
    - The last commit is older than threshold_minutes

    A WP with a worktree but NO commits since diverging is NOT stale - the agent
    just started and hasn't committed yet.

    Args:
        wp_id: Work package ID (e.g., "WP01")
        worktree_path: Path to the WP's worktree
        threshold_minutes: Minutes of inactivity before considered stale

    Returns:
        StaleCheckResult with staleness status
    """
    if not worktree_path.exists():
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=False,
        )

    try:
        last_commit, has_own_commits = get_last_meaningful_commit_time(worktree_path)

        if last_commit is None:
            # Can't determine commit time, or no commits on this branch yet
            # If no commits yet (has_own_commits=False), agent just started - not stale
            return StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=None,
                error=None if not has_own_commits else "Could not determine last commit time",
            )

        now = datetime.now(timezone.utc)
        # Ensure last_commit is timezone-aware
        if last_commit.tzinfo is None:
            last_commit = last_commit.replace(tzinfo=timezone.utc)

        delta = now - last_commit
        minutes_since = delta.total_seconds() / 60

        is_stale = minutes_since > threshold_minutes

        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=is_stale,
            last_commit_time=last_commit,
            minutes_since_commit=round(minutes_since, 1),
            worktree_exists=True,
        )

    except Exception as e:
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=True,
            error=str(e),
        )


def x_check_wp_staleness__mutmut_19(
    wp_id: str,
    worktree_path: Path,
    threshold_minutes: int = 10,
) -> StaleCheckResult:
    """
    Check if a work package is stale based on VCS activity.

    A WP is considered stale if:
    - Its worktree exists
    - The branch has commits since diverging from main (agent has done work)
    - The last commit is older than threshold_minutes

    A WP with a worktree but NO commits since diverging is NOT stale - the agent
    just started and hasn't committed yet.

    Args:
        wp_id: Work package ID (e.g., "WP01")
        worktree_path: Path to the WP's worktree
        threshold_minutes: Minutes of inactivity before considered stale

    Returns:
        StaleCheckResult with staleness status
    """
    if not worktree_path.exists():
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=False,
        )

    try:
        last_commit, has_own_commits = get_last_meaningful_commit_time(worktree_path)

        if last_commit is None:
            # Can't determine commit time, or no commits on this branch yet
            # If no commits yet (has_own_commits=False), agent just started - not stale
            return StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=True,
                error=None,
            )

        now = datetime.now(timezone.utc)
        # Ensure last_commit is timezone-aware
        if last_commit.tzinfo is None:
            last_commit = last_commit.replace(tzinfo=timezone.utc)

        delta = now - last_commit
        minutes_since = delta.total_seconds() / 60

        is_stale = minutes_since > threshold_minutes

        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=is_stale,
            last_commit_time=last_commit,
            minutes_since_commit=round(minutes_since, 1),
            worktree_exists=True,
        )

    except Exception as e:
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=True,
            error=str(e),
        )


def x_check_wp_staleness__mutmut_20(
    wp_id: str,
    worktree_path: Path,
    threshold_minutes: int = 10,
) -> StaleCheckResult:
    """
    Check if a work package is stale based on VCS activity.

    A WP is considered stale if:
    - Its worktree exists
    - The branch has commits since diverging from main (agent has done work)
    - The last commit is older than threshold_minutes

    A WP with a worktree but NO commits since diverging is NOT stale - the agent
    just started and hasn't committed yet.

    Args:
        wp_id: Work package ID (e.g., "WP01")
        worktree_path: Path to the WP's worktree
        threshold_minutes: Minutes of inactivity before considered stale

    Returns:
        StaleCheckResult with staleness status
    """
    if not worktree_path.exists():
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=False,
        )

    try:
        last_commit, has_own_commits = get_last_meaningful_commit_time(worktree_path)

        if last_commit is None:
            # Can't determine commit time, or no commits on this branch yet
            # If no commits yet (has_own_commits=False), agent just started - not stale
            return StaleCheckResult(
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=True,
                error=None if not has_own_commits else "Could not determine last commit time",
            )

        now = datetime.now(timezone.utc)
        # Ensure last_commit is timezone-aware
        if last_commit.tzinfo is None:
            last_commit = last_commit.replace(tzinfo=timezone.utc)

        delta = now - last_commit
        minutes_since = delta.total_seconds() / 60

        is_stale = minutes_since > threshold_minutes

        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=is_stale,
            last_commit_time=last_commit,
            minutes_since_commit=round(minutes_since, 1),
            worktree_exists=True,
        )

    except Exception as e:
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=True,
            error=str(e),
        )


def x_check_wp_staleness__mutmut_21(
    wp_id: str,
    worktree_path: Path,
    threshold_minutes: int = 10,
) -> StaleCheckResult:
    """
    Check if a work package is stale based on VCS activity.

    A WP is considered stale if:
    - Its worktree exists
    - The branch has commits since diverging from main (agent has done work)
    - The last commit is older than threshold_minutes

    A WP with a worktree but NO commits since diverging is NOT stale - the agent
    just started and hasn't committed yet.

    Args:
        wp_id: Work package ID (e.g., "WP01")
        worktree_path: Path to the WP's worktree
        threshold_minutes: Minutes of inactivity before considered stale

    Returns:
        StaleCheckResult with staleness status
    """
    if not worktree_path.exists():
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=False,
        )

    try:
        last_commit, has_own_commits = get_last_meaningful_commit_time(worktree_path)

        if last_commit is None:
            # Can't determine commit time, or no commits on this branch yet
            # If no commits yet (has_own_commits=False), agent just started - not stale
            return StaleCheckResult(
                wp_id=wp_id,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=True,
                error=None if not has_own_commits else "Could not determine last commit time",
            )

        now = datetime.now(timezone.utc)
        # Ensure last_commit is timezone-aware
        if last_commit.tzinfo is None:
            last_commit = last_commit.replace(tzinfo=timezone.utc)

        delta = now - last_commit
        minutes_since = delta.total_seconds() / 60

        is_stale = minutes_since > threshold_minutes

        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=is_stale,
            last_commit_time=last_commit,
            minutes_since_commit=round(minutes_since, 1),
            worktree_exists=True,
        )

    except Exception as e:
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=True,
            error=str(e),
        )


def x_check_wp_staleness__mutmut_22(
    wp_id: str,
    worktree_path: Path,
    threshold_minutes: int = 10,
) -> StaleCheckResult:
    """
    Check if a work package is stale based on VCS activity.

    A WP is considered stale if:
    - Its worktree exists
    - The branch has commits since diverging from main (agent has done work)
    - The last commit is older than threshold_minutes

    A WP with a worktree but NO commits since diverging is NOT stale - the agent
    just started and hasn't committed yet.

    Args:
        wp_id: Work package ID (e.g., "WP01")
        worktree_path: Path to the WP's worktree
        threshold_minutes: Minutes of inactivity before considered stale

    Returns:
        StaleCheckResult with staleness status
    """
    if not worktree_path.exists():
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=False,
        )

    try:
        last_commit, has_own_commits = get_last_meaningful_commit_time(worktree_path)

        if last_commit is None:
            # Can't determine commit time, or no commits on this branch yet
            # If no commits yet (has_own_commits=False), agent just started - not stale
            return StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                minutes_since_commit=None,
                worktree_exists=True,
                error=None if not has_own_commits else "Could not determine last commit time",
            )

        now = datetime.now(timezone.utc)
        # Ensure last_commit is timezone-aware
        if last_commit.tzinfo is None:
            last_commit = last_commit.replace(tzinfo=timezone.utc)

        delta = now - last_commit
        minutes_since = delta.total_seconds() / 60

        is_stale = minutes_since > threshold_minutes

        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=is_stale,
            last_commit_time=last_commit,
            minutes_since_commit=round(minutes_since, 1),
            worktree_exists=True,
        )

    except Exception as e:
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=True,
            error=str(e),
        )


def x_check_wp_staleness__mutmut_23(
    wp_id: str,
    worktree_path: Path,
    threshold_minutes: int = 10,
) -> StaleCheckResult:
    """
    Check if a work package is stale based on VCS activity.

    A WP is considered stale if:
    - Its worktree exists
    - The branch has commits since diverging from main (agent has done work)
    - The last commit is older than threshold_minutes

    A WP with a worktree but NO commits since diverging is NOT stale - the agent
    just started and hasn't committed yet.

    Args:
        wp_id: Work package ID (e.g., "WP01")
        worktree_path: Path to the WP's worktree
        threshold_minutes: Minutes of inactivity before considered stale

    Returns:
        StaleCheckResult with staleness status
    """
    if not worktree_path.exists():
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=False,
        )

    try:
        last_commit, has_own_commits = get_last_meaningful_commit_time(worktree_path)

        if last_commit is None:
            # Can't determine commit time, or no commits on this branch yet
            # If no commits yet (has_own_commits=False), agent just started - not stale
            return StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                worktree_exists=True,
                error=None if not has_own_commits else "Could not determine last commit time",
            )

        now = datetime.now(timezone.utc)
        # Ensure last_commit is timezone-aware
        if last_commit.tzinfo is None:
            last_commit = last_commit.replace(tzinfo=timezone.utc)

        delta = now - last_commit
        minutes_since = delta.total_seconds() / 60

        is_stale = minutes_since > threshold_minutes

        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=is_stale,
            last_commit_time=last_commit,
            minutes_since_commit=round(minutes_since, 1),
            worktree_exists=True,
        )

    except Exception as e:
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=True,
            error=str(e),
        )


def x_check_wp_staleness__mutmut_24(
    wp_id: str,
    worktree_path: Path,
    threshold_minutes: int = 10,
) -> StaleCheckResult:
    """
    Check if a work package is stale based on VCS activity.

    A WP is considered stale if:
    - Its worktree exists
    - The branch has commits since diverging from main (agent has done work)
    - The last commit is older than threshold_minutes

    A WP with a worktree but NO commits since diverging is NOT stale - the agent
    just started and hasn't committed yet.

    Args:
        wp_id: Work package ID (e.g., "WP01")
        worktree_path: Path to the WP's worktree
        threshold_minutes: Minutes of inactivity before considered stale

    Returns:
        StaleCheckResult with staleness status
    """
    if not worktree_path.exists():
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=False,
        )

    try:
        last_commit, has_own_commits = get_last_meaningful_commit_time(worktree_path)

        if last_commit is None:
            # Can't determine commit time, or no commits on this branch yet
            # If no commits yet (has_own_commits=False), agent just started - not stale
            return StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                error=None if not has_own_commits else "Could not determine last commit time",
            )

        now = datetime.now(timezone.utc)
        # Ensure last_commit is timezone-aware
        if last_commit.tzinfo is None:
            last_commit = last_commit.replace(tzinfo=timezone.utc)

        delta = now - last_commit
        minutes_since = delta.total_seconds() / 60

        is_stale = minutes_since > threshold_minutes

        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=is_stale,
            last_commit_time=last_commit,
            minutes_since_commit=round(minutes_since, 1),
            worktree_exists=True,
        )

    except Exception as e:
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=True,
            error=str(e),
        )


def x_check_wp_staleness__mutmut_25(
    wp_id: str,
    worktree_path: Path,
    threshold_minutes: int = 10,
) -> StaleCheckResult:
    """
    Check if a work package is stale based on VCS activity.

    A WP is considered stale if:
    - Its worktree exists
    - The branch has commits since diverging from main (agent has done work)
    - The last commit is older than threshold_minutes

    A WP with a worktree but NO commits since diverging is NOT stale - the agent
    just started and hasn't committed yet.

    Args:
        wp_id: Work package ID (e.g., "WP01")
        worktree_path: Path to the WP's worktree
        threshold_minutes: Minutes of inactivity before considered stale

    Returns:
        StaleCheckResult with staleness status
    """
    if not worktree_path.exists():
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=False,
        )

    try:
        last_commit, has_own_commits = get_last_meaningful_commit_time(worktree_path)

        if last_commit is None:
            # Can't determine commit time, or no commits on this branch yet
            # If no commits yet (has_own_commits=False), agent just started - not stale
            return StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=True,
                )

        now = datetime.now(timezone.utc)
        # Ensure last_commit is timezone-aware
        if last_commit.tzinfo is None:
            last_commit = last_commit.replace(tzinfo=timezone.utc)

        delta = now - last_commit
        minutes_since = delta.total_seconds() / 60

        is_stale = minutes_since > threshold_minutes

        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=is_stale,
            last_commit_time=last_commit,
            minutes_since_commit=round(minutes_since, 1),
            worktree_exists=True,
        )

    except Exception as e:
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=True,
            error=str(e),
        )


def x_check_wp_staleness__mutmut_26(
    wp_id: str,
    worktree_path: Path,
    threshold_minutes: int = 10,
) -> StaleCheckResult:
    """
    Check if a work package is stale based on VCS activity.

    A WP is considered stale if:
    - Its worktree exists
    - The branch has commits since diverging from main (agent has done work)
    - The last commit is older than threshold_minutes

    A WP with a worktree but NO commits since diverging is NOT stale - the agent
    just started and hasn't committed yet.

    Args:
        wp_id: Work package ID (e.g., "WP01")
        worktree_path: Path to the WP's worktree
        threshold_minutes: Minutes of inactivity before considered stale

    Returns:
        StaleCheckResult with staleness status
    """
    if not worktree_path.exists():
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=False,
        )

    try:
        last_commit, has_own_commits = get_last_meaningful_commit_time(worktree_path)

        if last_commit is None:
            # Can't determine commit time, or no commits on this branch yet
            # If no commits yet (has_own_commits=False), agent just started - not stale
            return StaleCheckResult(
                wp_id=wp_id,
                is_stale=True,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=True,
                error=None if not has_own_commits else "Could not determine last commit time",
            )

        now = datetime.now(timezone.utc)
        # Ensure last_commit is timezone-aware
        if last_commit.tzinfo is None:
            last_commit = last_commit.replace(tzinfo=timezone.utc)

        delta = now - last_commit
        minutes_since = delta.total_seconds() / 60

        is_stale = minutes_since > threshold_minutes

        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=is_stale,
            last_commit_time=last_commit,
            minutes_since_commit=round(minutes_since, 1),
            worktree_exists=True,
        )

    except Exception as e:
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=True,
            error=str(e),
        )


def x_check_wp_staleness__mutmut_27(
    wp_id: str,
    worktree_path: Path,
    threshold_minutes: int = 10,
) -> StaleCheckResult:
    """
    Check if a work package is stale based on VCS activity.

    A WP is considered stale if:
    - Its worktree exists
    - The branch has commits since diverging from main (agent has done work)
    - The last commit is older than threshold_minutes

    A WP with a worktree but NO commits since diverging is NOT stale - the agent
    just started and hasn't committed yet.

    Args:
        wp_id: Work package ID (e.g., "WP01")
        worktree_path: Path to the WP's worktree
        threshold_minutes: Minutes of inactivity before considered stale

    Returns:
        StaleCheckResult with staleness status
    """
    if not worktree_path.exists():
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=False,
        )

    try:
        last_commit, has_own_commits = get_last_meaningful_commit_time(worktree_path)

        if last_commit is None:
            # Can't determine commit time, or no commits on this branch yet
            # If no commits yet (has_own_commits=False), agent just started - not stale
            return StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=False,
                error=None if not has_own_commits else "Could not determine last commit time",
            )

        now = datetime.now(timezone.utc)
        # Ensure last_commit is timezone-aware
        if last_commit.tzinfo is None:
            last_commit = last_commit.replace(tzinfo=timezone.utc)

        delta = now - last_commit
        minutes_since = delta.total_seconds() / 60

        is_stale = minutes_since > threshold_minutes

        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=is_stale,
            last_commit_time=last_commit,
            minutes_since_commit=round(minutes_since, 1),
            worktree_exists=True,
        )

    except Exception as e:
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=True,
            error=str(e),
        )


def x_check_wp_staleness__mutmut_28(
    wp_id: str,
    worktree_path: Path,
    threshold_minutes: int = 10,
) -> StaleCheckResult:
    """
    Check if a work package is stale based on VCS activity.

    A WP is considered stale if:
    - Its worktree exists
    - The branch has commits since diverging from main (agent has done work)
    - The last commit is older than threshold_minutes

    A WP with a worktree but NO commits since diverging is NOT stale - the agent
    just started and hasn't committed yet.

    Args:
        wp_id: Work package ID (e.g., "WP01")
        worktree_path: Path to the WP's worktree
        threshold_minutes: Minutes of inactivity before considered stale

    Returns:
        StaleCheckResult with staleness status
    """
    if not worktree_path.exists():
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=False,
        )

    try:
        last_commit, has_own_commits = get_last_meaningful_commit_time(worktree_path)

        if last_commit is None:
            # Can't determine commit time, or no commits on this branch yet
            # If no commits yet (has_own_commits=False), agent just started - not stale
            return StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=True,
                error=None if has_own_commits else "Could not determine last commit time",
            )

        now = datetime.now(timezone.utc)
        # Ensure last_commit is timezone-aware
        if last_commit.tzinfo is None:
            last_commit = last_commit.replace(tzinfo=timezone.utc)

        delta = now - last_commit
        minutes_since = delta.total_seconds() / 60

        is_stale = minutes_since > threshold_minutes

        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=is_stale,
            last_commit_time=last_commit,
            minutes_since_commit=round(minutes_since, 1),
            worktree_exists=True,
        )

    except Exception as e:
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=True,
            error=str(e),
        )


def x_check_wp_staleness__mutmut_29(
    wp_id: str,
    worktree_path: Path,
    threshold_minutes: int = 10,
) -> StaleCheckResult:
    """
    Check if a work package is stale based on VCS activity.

    A WP is considered stale if:
    - Its worktree exists
    - The branch has commits since diverging from main (agent has done work)
    - The last commit is older than threshold_minutes

    A WP with a worktree but NO commits since diverging is NOT stale - the agent
    just started and hasn't committed yet.

    Args:
        wp_id: Work package ID (e.g., "WP01")
        worktree_path: Path to the WP's worktree
        threshold_minutes: Minutes of inactivity before considered stale

    Returns:
        StaleCheckResult with staleness status
    """
    if not worktree_path.exists():
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=False,
        )

    try:
        last_commit, has_own_commits = get_last_meaningful_commit_time(worktree_path)

        if last_commit is None:
            # Can't determine commit time, or no commits on this branch yet
            # If no commits yet (has_own_commits=False), agent just started - not stale
            return StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=True,
                error=None if not has_own_commits else "XXCould not determine last commit timeXX",
            )

        now = datetime.now(timezone.utc)
        # Ensure last_commit is timezone-aware
        if last_commit.tzinfo is None:
            last_commit = last_commit.replace(tzinfo=timezone.utc)

        delta = now - last_commit
        minutes_since = delta.total_seconds() / 60

        is_stale = minutes_since > threshold_minutes

        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=is_stale,
            last_commit_time=last_commit,
            minutes_since_commit=round(minutes_since, 1),
            worktree_exists=True,
        )

    except Exception as e:
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=True,
            error=str(e),
        )


def x_check_wp_staleness__mutmut_30(
    wp_id: str,
    worktree_path: Path,
    threshold_minutes: int = 10,
) -> StaleCheckResult:
    """
    Check if a work package is stale based on VCS activity.

    A WP is considered stale if:
    - Its worktree exists
    - The branch has commits since diverging from main (agent has done work)
    - The last commit is older than threshold_minutes

    A WP with a worktree but NO commits since diverging is NOT stale - the agent
    just started and hasn't committed yet.

    Args:
        wp_id: Work package ID (e.g., "WP01")
        worktree_path: Path to the WP's worktree
        threshold_minutes: Minutes of inactivity before considered stale

    Returns:
        StaleCheckResult with staleness status
    """
    if not worktree_path.exists():
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=False,
        )

    try:
        last_commit, has_own_commits = get_last_meaningful_commit_time(worktree_path)

        if last_commit is None:
            # Can't determine commit time, or no commits on this branch yet
            # If no commits yet (has_own_commits=False), agent just started - not stale
            return StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=True,
                error=None if not has_own_commits else "could not determine last commit time",
            )

        now = datetime.now(timezone.utc)
        # Ensure last_commit is timezone-aware
        if last_commit.tzinfo is None:
            last_commit = last_commit.replace(tzinfo=timezone.utc)

        delta = now - last_commit
        minutes_since = delta.total_seconds() / 60

        is_stale = minutes_since > threshold_minutes

        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=is_stale,
            last_commit_time=last_commit,
            minutes_since_commit=round(minutes_since, 1),
            worktree_exists=True,
        )

    except Exception as e:
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=True,
            error=str(e),
        )


def x_check_wp_staleness__mutmut_31(
    wp_id: str,
    worktree_path: Path,
    threshold_minutes: int = 10,
) -> StaleCheckResult:
    """
    Check if a work package is stale based on VCS activity.

    A WP is considered stale if:
    - Its worktree exists
    - The branch has commits since diverging from main (agent has done work)
    - The last commit is older than threshold_minutes

    A WP with a worktree but NO commits since diverging is NOT stale - the agent
    just started and hasn't committed yet.

    Args:
        wp_id: Work package ID (e.g., "WP01")
        worktree_path: Path to the WP's worktree
        threshold_minutes: Minutes of inactivity before considered stale

    Returns:
        StaleCheckResult with staleness status
    """
    if not worktree_path.exists():
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=False,
        )

    try:
        last_commit, has_own_commits = get_last_meaningful_commit_time(worktree_path)

        if last_commit is None:
            # Can't determine commit time, or no commits on this branch yet
            # If no commits yet (has_own_commits=False), agent just started - not stale
            return StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=True,
                error=None if not has_own_commits else "COULD NOT DETERMINE LAST COMMIT TIME",
            )

        now = datetime.now(timezone.utc)
        # Ensure last_commit is timezone-aware
        if last_commit.tzinfo is None:
            last_commit = last_commit.replace(tzinfo=timezone.utc)

        delta = now - last_commit
        minutes_since = delta.total_seconds() / 60

        is_stale = minutes_since > threshold_minutes

        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=is_stale,
            last_commit_time=last_commit,
            minutes_since_commit=round(minutes_since, 1),
            worktree_exists=True,
        )

    except Exception as e:
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=True,
            error=str(e),
        )


def x_check_wp_staleness__mutmut_32(
    wp_id: str,
    worktree_path: Path,
    threshold_minutes: int = 10,
) -> StaleCheckResult:
    """
    Check if a work package is stale based on VCS activity.

    A WP is considered stale if:
    - Its worktree exists
    - The branch has commits since diverging from main (agent has done work)
    - The last commit is older than threshold_minutes

    A WP with a worktree but NO commits since diverging is NOT stale - the agent
    just started and hasn't committed yet.

    Args:
        wp_id: Work package ID (e.g., "WP01")
        worktree_path: Path to the WP's worktree
        threshold_minutes: Minutes of inactivity before considered stale

    Returns:
        StaleCheckResult with staleness status
    """
    if not worktree_path.exists():
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=False,
        )

    try:
        last_commit, has_own_commits = get_last_meaningful_commit_time(worktree_path)

        if last_commit is None:
            # Can't determine commit time, or no commits on this branch yet
            # If no commits yet (has_own_commits=False), agent just started - not stale
            return StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=True,
                error=None if not has_own_commits else "Could not determine last commit time",
            )

        now = None
        # Ensure last_commit is timezone-aware
        if last_commit.tzinfo is None:
            last_commit = last_commit.replace(tzinfo=timezone.utc)

        delta = now - last_commit
        minutes_since = delta.total_seconds() / 60

        is_stale = minutes_since > threshold_minutes

        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=is_stale,
            last_commit_time=last_commit,
            minutes_since_commit=round(minutes_since, 1),
            worktree_exists=True,
        )

    except Exception as e:
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=True,
            error=str(e),
        )


def x_check_wp_staleness__mutmut_33(
    wp_id: str,
    worktree_path: Path,
    threshold_minutes: int = 10,
) -> StaleCheckResult:
    """
    Check if a work package is stale based on VCS activity.

    A WP is considered stale if:
    - Its worktree exists
    - The branch has commits since diverging from main (agent has done work)
    - The last commit is older than threshold_minutes

    A WP with a worktree but NO commits since diverging is NOT stale - the agent
    just started and hasn't committed yet.

    Args:
        wp_id: Work package ID (e.g., "WP01")
        worktree_path: Path to the WP's worktree
        threshold_minutes: Minutes of inactivity before considered stale

    Returns:
        StaleCheckResult with staleness status
    """
    if not worktree_path.exists():
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=False,
        )

    try:
        last_commit, has_own_commits = get_last_meaningful_commit_time(worktree_path)

        if last_commit is None:
            # Can't determine commit time, or no commits on this branch yet
            # If no commits yet (has_own_commits=False), agent just started - not stale
            return StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=True,
                error=None if not has_own_commits else "Could not determine last commit time",
            )

        now = datetime.now(None)
        # Ensure last_commit is timezone-aware
        if last_commit.tzinfo is None:
            last_commit = last_commit.replace(tzinfo=timezone.utc)

        delta = now - last_commit
        minutes_since = delta.total_seconds() / 60

        is_stale = minutes_since > threshold_minutes

        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=is_stale,
            last_commit_time=last_commit,
            minutes_since_commit=round(minutes_since, 1),
            worktree_exists=True,
        )

    except Exception as e:
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=True,
            error=str(e),
        )


def x_check_wp_staleness__mutmut_34(
    wp_id: str,
    worktree_path: Path,
    threshold_minutes: int = 10,
) -> StaleCheckResult:
    """
    Check if a work package is stale based on VCS activity.

    A WP is considered stale if:
    - Its worktree exists
    - The branch has commits since diverging from main (agent has done work)
    - The last commit is older than threshold_minutes

    A WP with a worktree but NO commits since diverging is NOT stale - the agent
    just started and hasn't committed yet.

    Args:
        wp_id: Work package ID (e.g., "WP01")
        worktree_path: Path to the WP's worktree
        threshold_minutes: Minutes of inactivity before considered stale

    Returns:
        StaleCheckResult with staleness status
    """
    if not worktree_path.exists():
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=False,
        )

    try:
        last_commit, has_own_commits = get_last_meaningful_commit_time(worktree_path)

        if last_commit is None:
            # Can't determine commit time, or no commits on this branch yet
            # If no commits yet (has_own_commits=False), agent just started - not stale
            return StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=True,
                error=None if not has_own_commits else "Could not determine last commit time",
            )

        now = datetime.now(timezone.utc)
        # Ensure last_commit is timezone-aware
        if last_commit.tzinfo is not None:
            last_commit = last_commit.replace(tzinfo=timezone.utc)

        delta = now - last_commit
        minutes_since = delta.total_seconds() / 60

        is_stale = minutes_since > threshold_minutes

        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=is_stale,
            last_commit_time=last_commit,
            minutes_since_commit=round(minutes_since, 1),
            worktree_exists=True,
        )

    except Exception as e:
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=True,
            error=str(e),
        )


def x_check_wp_staleness__mutmut_35(
    wp_id: str,
    worktree_path: Path,
    threshold_minutes: int = 10,
) -> StaleCheckResult:
    """
    Check if a work package is stale based on VCS activity.

    A WP is considered stale if:
    - Its worktree exists
    - The branch has commits since diverging from main (agent has done work)
    - The last commit is older than threshold_minutes

    A WP with a worktree but NO commits since diverging is NOT stale - the agent
    just started and hasn't committed yet.

    Args:
        wp_id: Work package ID (e.g., "WP01")
        worktree_path: Path to the WP's worktree
        threshold_minutes: Minutes of inactivity before considered stale

    Returns:
        StaleCheckResult with staleness status
    """
    if not worktree_path.exists():
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=False,
        )

    try:
        last_commit, has_own_commits = get_last_meaningful_commit_time(worktree_path)

        if last_commit is None:
            # Can't determine commit time, or no commits on this branch yet
            # If no commits yet (has_own_commits=False), agent just started - not stale
            return StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=True,
                error=None if not has_own_commits else "Could not determine last commit time",
            )

        now = datetime.now(timezone.utc)
        # Ensure last_commit is timezone-aware
        if last_commit.tzinfo is None:
            last_commit = None

        delta = now - last_commit
        minutes_since = delta.total_seconds() / 60

        is_stale = minutes_since > threshold_minutes

        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=is_stale,
            last_commit_time=last_commit,
            minutes_since_commit=round(minutes_since, 1),
            worktree_exists=True,
        )

    except Exception as e:
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=True,
            error=str(e),
        )


def x_check_wp_staleness__mutmut_36(
    wp_id: str,
    worktree_path: Path,
    threshold_minutes: int = 10,
) -> StaleCheckResult:
    """
    Check if a work package is stale based on VCS activity.

    A WP is considered stale if:
    - Its worktree exists
    - The branch has commits since diverging from main (agent has done work)
    - The last commit is older than threshold_minutes

    A WP with a worktree but NO commits since diverging is NOT stale - the agent
    just started and hasn't committed yet.

    Args:
        wp_id: Work package ID (e.g., "WP01")
        worktree_path: Path to the WP's worktree
        threshold_minutes: Minutes of inactivity before considered stale

    Returns:
        StaleCheckResult with staleness status
    """
    if not worktree_path.exists():
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=False,
        )

    try:
        last_commit, has_own_commits = get_last_meaningful_commit_time(worktree_path)

        if last_commit is None:
            # Can't determine commit time, or no commits on this branch yet
            # If no commits yet (has_own_commits=False), agent just started - not stale
            return StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=True,
                error=None if not has_own_commits else "Could not determine last commit time",
            )

        now = datetime.now(timezone.utc)
        # Ensure last_commit is timezone-aware
        if last_commit.tzinfo is None:
            last_commit = last_commit.replace(tzinfo=None)

        delta = now - last_commit
        minutes_since = delta.total_seconds() / 60

        is_stale = minutes_since > threshold_minutes

        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=is_stale,
            last_commit_time=last_commit,
            minutes_since_commit=round(minutes_since, 1),
            worktree_exists=True,
        )

    except Exception as e:
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=True,
            error=str(e),
        )


def x_check_wp_staleness__mutmut_37(
    wp_id: str,
    worktree_path: Path,
    threshold_minutes: int = 10,
) -> StaleCheckResult:
    """
    Check if a work package is stale based on VCS activity.

    A WP is considered stale if:
    - Its worktree exists
    - The branch has commits since diverging from main (agent has done work)
    - The last commit is older than threshold_minutes

    A WP with a worktree but NO commits since diverging is NOT stale - the agent
    just started and hasn't committed yet.

    Args:
        wp_id: Work package ID (e.g., "WP01")
        worktree_path: Path to the WP's worktree
        threshold_minutes: Minutes of inactivity before considered stale

    Returns:
        StaleCheckResult with staleness status
    """
    if not worktree_path.exists():
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=False,
        )

    try:
        last_commit, has_own_commits = get_last_meaningful_commit_time(worktree_path)

        if last_commit is None:
            # Can't determine commit time, or no commits on this branch yet
            # If no commits yet (has_own_commits=False), agent just started - not stale
            return StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=True,
                error=None if not has_own_commits else "Could not determine last commit time",
            )

        now = datetime.now(timezone.utc)
        # Ensure last_commit is timezone-aware
        if last_commit.tzinfo is None:
            last_commit = last_commit.replace(tzinfo=timezone.utc)

        delta = None
        minutes_since = delta.total_seconds() / 60

        is_stale = minutes_since > threshold_minutes

        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=is_stale,
            last_commit_time=last_commit,
            minutes_since_commit=round(minutes_since, 1),
            worktree_exists=True,
        )

    except Exception as e:
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=True,
            error=str(e),
        )


def x_check_wp_staleness__mutmut_38(
    wp_id: str,
    worktree_path: Path,
    threshold_minutes: int = 10,
) -> StaleCheckResult:
    """
    Check if a work package is stale based on VCS activity.

    A WP is considered stale if:
    - Its worktree exists
    - The branch has commits since diverging from main (agent has done work)
    - The last commit is older than threshold_minutes

    A WP with a worktree but NO commits since diverging is NOT stale - the agent
    just started and hasn't committed yet.

    Args:
        wp_id: Work package ID (e.g., "WP01")
        worktree_path: Path to the WP's worktree
        threshold_minutes: Minutes of inactivity before considered stale

    Returns:
        StaleCheckResult with staleness status
    """
    if not worktree_path.exists():
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=False,
        )

    try:
        last_commit, has_own_commits = get_last_meaningful_commit_time(worktree_path)

        if last_commit is None:
            # Can't determine commit time, or no commits on this branch yet
            # If no commits yet (has_own_commits=False), agent just started - not stale
            return StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=True,
                error=None if not has_own_commits else "Could not determine last commit time",
            )

        now = datetime.now(timezone.utc)
        # Ensure last_commit is timezone-aware
        if last_commit.tzinfo is None:
            last_commit = last_commit.replace(tzinfo=timezone.utc)

        delta = now + last_commit
        minutes_since = delta.total_seconds() / 60

        is_stale = minutes_since > threshold_minutes

        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=is_stale,
            last_commit_time=last_commit,
            minutes_since_commit=round(minutes_since, 1),
            worktree_exists=True,
        )

    except Exception as e:
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=True,
            error=str(e),
        )


def x_check_wp_staleness__mutmut_39(
    wp_id: str,
    worktree_path: Path,
    threshold_minutes: int = 10,
) -> StaleCheckResult:
    """
    Check if a work package is stale based on VCS activity.

    A WP is considered stale if:
    - Its worktree exists
    - The branch has commits since diverging from main (agent has done work)
    - The last commit is older than threshold_minutes

    A WP with a worktree but NO commits since diverging is NOT stale - the agent
    just started and hasn't committed yet.

    Args:
        wp_id: Work package ID (e.g., "WP01")
        worktree_path: Path to the WP's worktree
        threshold_minutes: Minutes of inactivity before considered stale

    Returns:
        StaleCheckResult with staleness status
    """
    if not worktree_path.exists():
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=False,
        )

    try:
        last_commit, has_own_commits = get_last_meaningful_commit_time(worktree_path)

        if last_commit is None:
            # Can't determine commit time, or no commits on this branch yet
            # If no commits yet (has_own_commits=False), agent just started - not stale
            return StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=True,
                error=None if not has_own_commits else "Could not determine last commit time",
            )

        now = datetime.now(timezone.utc)
        # Ensure last_commit is timezone-aware
        if last_commit.tzinfo is None:
            last_commit = last_commit.replace(tzinfo=timezone.utc)

        delta = now - last_commit
        minutes_since = None

        is_stale = minutes_since > threshold_minutes

        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=is_stale,
            last_commit_time=last_commit,
            minutes_since_commit=round(minutes_since, 1),
            worktree_exists=True,
        )

    except Exception as e:
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=True,
            error=str(e),
        )


def x_check_wp_staleness__mutmut_40(
    wp_id: str,
    worktree_path: Path,
    threshold_minutes: int = 10,
) -> StaleCheckResult:
    """
    Check if a work package is stale based on VCS activity.

    A WP is considered stale if:
    - Its worktree exists
    - The branch has commits since diverging from main (agent has done work)
    - The last commit is older than threshold_minutes

    A WP with a worktree but NO commits since diverging is NOT stale - the agent
    just started and hasn't committed yet.

    Args:
        wp_id: Work package ID (e.g., "WP01")
        worktree_path: Path to the WP's worktree
        threshold_minutes: Minutes of inactivity before considered stale

    Returns:
        StaleCheckResult with staleness status
    """
    if not worktree_path.exists():
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=False,
        )

    try:
        last_commit, has_own_commits = get_last_meaningful_commit_time(worktree_path)

        if last_commit is None:
            # Can't determine commit time, or no commits on this branch yet
            # If no commits yet (has_own_commits=False), agent just started - not stale
            return StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=True,
                error=None if not has_own_commits else "Could not determine last commit time",
            )

        now = datetime.now(timezone.utc)
        # Ensure last_commit is timezone-aware
        if last_commit.tzinfo is None:
            last_commit = last_commit.replace(tzinfo=timezone.utc)

        delta = now - last_commit
        minutes_since = delta.total_seconds() * 60

        is_stale = minutes_since > threshold_minutes

        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=is_stale,
            last_commit_time=last_commit,
            minutes_since_commit=round(minutes_since, 1),
            worktree_exists=True,
        )

    except Exception as e:
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=True,
            error=str(e),
        )


def x_check_wp_staleness__mutmut_41(
    wp_id: str,
    worktree_path: Path,
    threshold_minutes: int = 10,
) -> StaleCheckResult:
    """
    Check if a work package is stale based on VCS activity.

    A WP is considered stale if:
    - Its worktree exists
    - The branch has commits since diverging from main (agent has done work)
    - The last commit is older than threshold_minutes

    A WP with a worktree but NO commits since diverging is NOT stale - the agent
    just started and hasn't committed yet.

    Args:
        wp_id: Work package ID (e.g., "WP01")
        worktree_path: Path to the WP's worktree
        threshold_minutes: Minutes of inactivity before considered stale

    Returns:
        StaleCheckResult with staleness status
    """
    if not worktree_path.exists():
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=False,
        )

    try:
        last_commit, has_own_commits = get_last_meaningful_commit_time(worktree_path)

        if last_commit is None:
            # Can't determine commit time, or no commits on this branch yet
            # If no commits yet (has_own_commits=False), agent just started - not stale
            return StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=True,
                error=None if not has_own_commits else "Could not determine last commit time",
            )

        now = datetime.now(timezone.utc)
        # Ensure last_commit is timezone-aware
        if last_commit.tzinfo is None:
            last_commit = last_commit.replace(tzinfo=timezone.utc)

        delta = now - last_commit
        minutes_since = delta.total_seconds() / 61

        is_stale = minutes_since > threshold_minutes

        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=is_stale,
            last_commit_time=last_commit,
            minutes_since_commit=round(minutes_since, 1),
            worktree_exists=True,
        )

    except Exception as e:
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=True,
            error=str(e),
        )


def x_check_wp_staleness__mutmut_42(
    wp_id: str,
    worktree_path: Path,
    threshold_minutes: int = 10,
) -> StaleCheckResult:
    """
    Check if a work package is stale based on VCS activity.

    A WP is considered stale if:
    - Its worktree exists
    - The branch has commits since diverging from main (agent has done work)
    - The last commit is older than threshold_minutes

    A WP with a worktree but NO commits since diverging is NOT stale - the agent
    just started and hasn't committed yet.

    Args:
        wp_id: Work package ID (e.g., "WP01")
        worktree_path: Path to the WP's worktree
        threshold_minutes: Minutes of inactivity before considered stale

    Returns:
        StaleCheckResult with staleness status
    """
    if not worktree_path.exists():
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=False,
        )

    try:
        last_commit, has_own_commits = get_last_meaningful_commit_time(worktree_path)

        if last_commit is None:
            # Can't determine commit time, or no commits on this branch yet
            # If no commits yet (has_own_commits=False), agent just started - not stale
            return StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=True,
                error=None if not has_own_commits else "Could not determine last commit time",
            )

        now = datetime.now(timezone.utc)
        # Ensure last_commit is timezone-aware
        if last_commit.tzinfo is None:
            last_commit = last_commit.replace(tzinfo=timezone.utc)

        delta = now - last_commit
        minutes_since = delta.total_seconds() / 60

        is_stale = None

        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=is_stale,
            last_commit_time=last_commit,
            minutes_since_commit=round(minutes_since, 1),
            worktree_exists=True,
        )

    except Exception as e:
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=True,
            error=str(e),
        )


def x_check_wp_staleness__mutmut_43(
    wp_id: str,
    worktree_path: Path,
    threshold_minutes: int = 10,
) -> StaleCheckResult:
    """
    Check if a work package is stale based on VCS activity.

    A WP is considered stale if:
    - Its worktree exists
    - The branch has commits since diverging from main (agent has done work)
    - The last commit is older than threshold_minutes

    A WP with a worktree but NO commits since diverging is NOT stale - the agent
    just started and hasn't committed yet.

    Args:
        wp_id: Work package ID (e.g., "WP01")
        worktree_path: Path to the WP's worktree
        threshold_minutes: Minutes of inactivity before considered stale

    Returns:
        StaleCheckResult with staleness status
    """
    if not worktree_path.exists():
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=False,
        )

    try:
        last_commit, has_own_commits = get_last_meaningful_commit_time(worktree_path)

        if last_commit is None:
            # Can't determine commit time, or no commits on this branch yet
            # If no commits yet (has_own_commits=False), agent just started - not stale
            return StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=True,
                error=None if not has_own_commits else "Could not determine last commit time",
            )

        now = datetime.now(timezone.utc)
        # Ensure last_commit is timezone-aware
        if last_commit.tzinfo is None:
            last_commit = last_commit.replace(tzinfo=timezone.utc)

        delta = now - last_commit
        minutes_since = delta.total_seconds() / 60

        is_stale = minutes_since >= threshold_minutes

        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=is_stale,
            last_commit_time=last_commit,
            minutes_since_commit=round(minutes_since, 1),
            worktree_exists=True,
        )

    except Exception as e:
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=True,
            error=str(e),
        )


def x_check_wp_staleness__mutmut_44(
    wp_id: str,
    worktree_path: Path,
    threshold_minutes: int = 10,
) -> StaleCheckResult:
    """
    Check if a work package is stale based on VCS activity.

    A WP is considered stale if:
    - Its worktree exists
    - The branch has commits since diverging from main (agent has done work)
    - The last commit is older than threshold_minutes

    A WP with a worktree but NO commits since diverging is NOT stale - the agent
    just started and hasn't committed yet.

    Args:
        wp_id: Work package ID (e.g., "WP01")
        worktree_path: Path to the WP's worktree
        threshold_minutes: Minutes of inactivity before considered stale

    Returns:
        StaleCheckResult with staleness status
    """
    if not worktree_path.exists():
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=False,
        )

    try:
        last_commit, has_own_commits = get_last_meaningful_commit_time(worktree_path)

        if last_commit is None:
            # Can't determine commit time, or no commits on this branch yet
            # If no commits yet (has_own_commits=False), agent just started - not stale
            return StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=True,
                error=None if not has_own_commits else "Could not determine last commit time",
            )

        now = datetime.now(timezone.utc)
        # Ensure last_commit is timezone-aware
        if last_commit.tzinfo is None:
            last_commit = last_commit.replace(tzinfo=timezone.utc)

        delta = now - last_commit
        minutes_since = delta.total_seconds() / 60

        is_stale = minutes_since > threshold_minutes

        return StaleCheckResult(
            wp_id=None,
            is_stale=is_stale,
            last_commit_time=last_commit,
            minutes_since_commit=round(minutes_since, 1),
            worktree_exists=True,
        )

    except Exception as e:
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=True,
            error=str(e),
        )


def x_check_wp_staleness__mutmut_45(
    wp_id: str,
    worktree_path: Path,
    threshold_minutes: int = 10,
) -> StaleCheckResult:
    """
    Check if a work package is stale based on VCS activity.

    A WP is considered stale if:
    - Its worktree exists
    - The branch has commits since diverging from main (agent has done work)
    - The last commit is older than threshold_minutes

    A WP with a worktree but NO commits since diverging is NOT stale - the agent
    just started and hasn't committed yet.

    Args:
        wp_id: Work package ID (e.g., "WP01")
        worktree_path: Path to the WP's worktree
        threshold_minutes: Minutes of inactivity before considered stale

    Returns:
        StaleCheckResult with staleness status
    """
    if not worktree_path.exists():
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=False,
        )

    try:
        last_commit, has_own_commits = get_last_meaningful_commit_time(worktree_path)

        if last_commit is None:
            # Can't determine commit time, or no commits on this branch yet
            # If no commits yet (has_own_commits=False), agent just started - not stale
            return StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=True,
                error=None if not has_own_commits else "Could not determine last commit time",
            )

        now = datetime.now(timezone.utc)
        # Ensure last_commit is timezone-aware
        if last_commit.tzinfo is None:
            last_commit = last_commit.replace(tzinfo=timezone.utc)

        delta = now - last_commit
        minutes_since = delta.total_seconds() / 60

        is_stale = minutes_since > threshold_minutes

        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=None,
            last_commit_time=last_commit,
            minutes_since_commit=round(minutes_since, 1),
            worktree_exists=True,
        )

    except Exception as e:
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=True,
            error=str(e),
        )


def x_check_wp_staleness__mutmut_46(
    wp_id: str,
    worktree_path: Path,
    threshold_minutes: int = 10,
) -> StaleCheckResult:
    """
    Check if a work package is stale based on VCS activity.

    A WP is considered stale if:
    - Its worktree exists
    - The branch has commits since diverging from main (agent has done work)
    - The last commit is older than threshold_minutes

    A WP with a worktree but NO commits since diverging is NOT stale - the agent
    just started and hasn't committed yet.

    Args:
        wp_id: Work package ID (e.g., "WP01")
        worktree_path: Path to the WP's worktree
        threshold_minutes: Minutes of inactivity before considered stale

    Returns:
        StaleCheckResult with staleness status
    """
    if not worktree_path.exists():
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=False,
        )

    try:
        last_commit, has_own_commits = get_last_meaningful_commit_time(worktree_path)

        if last_commit is None:
            # Can't determine commit time, or no commits on this branch yet
            # If no commits yet (has_own_commits=False), agent just started - not stale
            return StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=True,
                error=None if not has_own_commits else "Could not determine last commit time",
            )

        now = datetime.now(timezone.utc)
        # Ensure last_commit is timezone-aware
        if last_commit.tzinfo is None:
            last_commit = last_commit.replace(tzinfo=timezone.utc)

        delta = now - last_commit
        minutes_since = delta.total_seconds() / 60

        is_stale = minutes_since > threshold_minutes

        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=is_stale,
            last_commit_time=None,
            minutes_since_commit=round(minutes_since, 1),
            worktree_exists=True,
        )

    except Exception as e:
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=True,
            error=str(e),
        )


def x_check_wp_staleness__mutmut_47(
    wp_id: str,
    worktree_path: Path,
    threshold_minutes: int = 10,
) -> StaleCheckResult:
    """
    Check if a work package is stale based on VCS activity.

    A WP is considered stale if:
    - Its worktree exists
    - The branch has commits since diverging from main (agent has done work)
    - The last commit is older than threshold_minutes

    A WP with a worktree but NO commits since diverging is NOT stale - the agent
    just started and hasn't committed yet.

    Args:
        wp_id: Work package ID (e.g., "WP01")
        worktree_path: Path to the WP's worktree
        threshold_minutes: Minutes of inactivity before considered stale

    Returns:
        StaleCheckResult with staleness status
    """
    if not worktree_path.exists():
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=False,
        )

    try:
        last_commit, has_own_commits = get_last_meaningful_commit_time(worktree_path)

        if last_commit is None:
            # Can't determine commit time, or no commits on this branch yet
            # If no commits yet (has_own_commits=False), agent just started - not stale
            return StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=True,
                error=None if not has_own_commits else "Could not determine last commit time",
            )

        now = datetime.now(timezone.utc)
        # Ensure last_commit is timezone-aware
        if last_commit.tzinfo is None:
            last_commit = last_commit.replace(tzinfo=timezone.utc)

        delta = now - last_commit
        minutes_since = delta.total_seconds() / 60

        is_stale = minutes_since > threshold_minutes

        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=is_stale,
            last_commit_time=last_commit,
            minutes_since_commit=None,
            worktree_exists=True,
        )

    except Exception as e:
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=True,
            error=str(e),
        )


def x_check_wp_staleness__mutmut_48(
    wp_id: str,
    worktree_path: Path,
    threshold_minutes: int = 10,
) -> StaleCheckResult:
    """
    Check if a work package is stale based on VCS activity.

    A WP is considered stale if:
    - Its worktree exists
    - The branch has commits since diverging from main (agent has done work)
    - The last commit is older than threshold_minutes

    A WP with a worktree but NO commits since diverging is NOT stale - the agent
    just started and hasn't committed yet.

    Args:
        wp_id: Work package ID (e.g., "WP01")
        worktree_path: Path to the WP's worktree
        threshold_minutes: Minutes of inactivity before considered stale

    Returns:
        StaleCheckResult with staleness status
    """
    if not worktree_path.exists():
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=False,
        )

    try:
        last_commit, has_own_commits = get_last_meaningful_commit_time(worktree_path)

        if last_commit is None:
            # Can't determine commit time, or no commits on this branch yet
            # If no commits yet (has_own_commits=False), agent just started - not stale
            return StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=True,
                error=None if not has_own_commits else "Could not determine last commit time",
            )

        now = datetime.now(timezone.utc)
        # Ensure last_commit is timezone-aware
        if last_commit.tzinfo is None:
            last_commit = last_commit.replace(tzinfo=timezone.utc)

        delta = now - last_commit
        minutes_since = delta.total_seconds() / 60

        is_stale = minutes_since > threshold_minutes

        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=is_stale,
            last_commit_time=last_commit,
            minutes_since_commit=round(minutes_since, 1),
            worktree_exists=None,
        )

    except Exception as e:
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=True,
            error=str(e),
        )


def x_check_wp_staleness__mutmut_49(
    wp_id: str,
    worktree_path: Path,
    threshold_minutes: int = 10,
) -> StaleCheckResult:
    """
    Check if a work package is stale based on VCS activity.

    A WP is considered stale if:
    - Its worktree exists
    - The branch has commits since diverging from main (agent has done work)
    - The last commit is older than threshold_minutes

    A WP with a worktree but NO commits since diverging is NOT stale - the agent
    just started and hasn't committed yet.

    Args:
        wp_id: Work package ID (e.g., "WP01")
        worktree_path: Path to the WP's worktree
        threshold_minutes: Minutes of inactivity before considered stale

    Returns:
        StaleCheckResult with staleness status
    """
    if not worktree_path.exists():
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=False,
        )

    try:
        last_commit, has_own_commits = get_last_meaningful_commit_time(worktree_path)

        if last_commit is None:
            # Can't determine commit time, or no commits on this branch yet
            # If no commits yet (has_own_commits=False), agent just started - not stale
            return StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=True,
                error=None if not has_own_commits else "Could not determine last commit time",
            )

        now = datetime.now(timezone.utc)
        # Ensure last_commit is timezone-aware
        if last_commit.tzinfo is None:
            last_commit = last_commit.replace(tzinfo=timezone.utc)

        delta = now - last_commit
        minutes_since = delta.total_seconds() / 60

        is_stale = minutes_since > threshold_minutes

        return StaleCheckResult(
            is_stale=is_stale,
            last_commit_time=last_commit,
            minutes_since_commit=round(minutes_since, 1),
            worktree_exists=True,
        )

    except Exception as e:
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=True,
            error=str(e),
        )


def x_check_wp_staleness__mutmut_50(
    wp_id: str,
    worktree_path: Path,
    threshold_minutes: int = 10,
) -> StaleCheckResult:
    """
    Check if a work package is stale based on VCS activity.

    A WP is considered stale if:
    - Its worktree exists
    - The branch has commits since diverging from main (agent has done work)
    - The last commit is older than threshold_minutes

    A WP with a worktree but NO commits since diverging is NOT stale - the agent
    just started and hasn't committed yet.

    Args:
        wp_id: Work package ID (e.g., "WP01")
        worktree_path: Path to the WP's worktree
        threshold_minutes: Minutes of inactivity before considered stale

    Returns:
        StaleCheckResult with staleness status
    """
    if not worktree_path.exists():
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=False,
        )

    try:
        last_commit, has_own_commits = get_last_meaningful_commit_time(worktree_path)

        if last_commit is None:
            # Can't determine commit time, or no commits on this branch yet
            # If no commits yet (has_own_commits=False), agent just started - not stale
            return StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=True,
                error=None if not has_own_commits else "Could not determine last commit time",
            )

        now = datetime.now(timezone.utc)
        # Ensure last_commit is timezone-aware
        if last_commit.tzinfo is None:
            last_commit = last_commit.replace(tzinfo=timezone.utc)

        delta = now - last_commit
        minutes_since = delta.total_seconds() / 60

        is_stale = minutes_since > threshold_minutes

        return StaleCheckResult(
            wp_id=wp_id,
            last_commit_time=last_commit,
            minutes_since_commit=round(minutes_since, 1),
            worktree_exists=True,
        )

    except Exception as e:
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=True,
            error=str(e),
        )


def x_check_wp_staleness__mutmut_51(
    wp_id: str,
    worktree_path: Path,
    threshold_minutes: int = 10,
) -> StaleCheckResult:
    """
    Check if a work package is stale based on VCS activity.

    A WP is considered stale if:
    - Its worktree exists
    - The branch has commits since diverging from main (agent has done work)
    - The last commit is older than threshold_minutes

    A WP with a worktree but NO commits since diverging is NOT stale - the agent
    just started and hasn't committed yet.

    Args:
        wp_id: Work package ID (e.g., "WP01")
        worktree_path: Path to the WP's worktree
        threshold_minutes: Minutes of inactivity before considered stale

    Returns:
        StaleCheckResult with staleness status
    """
    if not worktree_path.exists():
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=False,
        )

    try:
        last_commit, has_own_commits = get_last_meaningful_commit_time(worktree_path)

        if last_commit is None:
            # Can't determine commit time, or no commits on this branch yet
            # If no commits yet (has_own_commits=False), agent just started - not stale
            return StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=True,
                error=None if not has_own_commits else "Could not determine last commit time",
            )

        now = datetime.now(timezone.utc)
        # Ensure last_commit is timezone-aware
        if last_commit.tzinfo is None:
            last_commit = last_commit.replace(tzinfo=timezone.utc)

        delta = now - last_commit
        minutes_since = delta.total_seconds() / 60

        is_stale = minutes_since > threshold_minutes

        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=is_stale,
            minutes_since_commit=round(minutes_since, 1),
            worktree_exists=True,
        )

    except Exception as e:
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=True,
            error=str(e),
        )


def x_check_wp_staleness__mutmut_52(
    wp_id: str,
    worktree_path: Path,
    threshold_minutes: int = 10,
) -> StaleCheckResult:
    """
    Check if a work package is stale based on VCS activity.

    A WP is considered stale if:
    - Its worktree exists
    - The branch has commits since diverging from main (agent has done work)
    - The last commit is older than threshold_minutes

    A WP with a worktree but NO commits since diverging is NOT stale - the agent
    just started and hasn't committed yet.

    Args:
        wp_id: Work package ID (e.g., "WP01")
        worktree_path: Path to the WP's worktree
        threshold_minutes: Minutes of inactivity before considered stale

    Returns:
        StaleCheckResult with staleness status
    """
    if not worktree_path.exists():
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=False,
        )

    try:
        last_commit, has_own_commits = get_last_meaningful_commit_time(worktree_path)

        if last_commit is None:
            # Can't determine commit time, or no commits on this branch yet
            # If no commits yet (has_own_commits=False), agent just started - not stale
            return StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=True,
                error=None if not has_own_commits else "Could not determine last commit time",
            )

        now = datetime.now(timezone.utc)
        # Ensure last_commit is timezone-aware
        if last_commit.tzinfo is None:
            last_commit = last_commit.replace(tzinfo=timezone.utc)

        delta = now - last_commit
        minutes_since = delta.total_seconds() / 60

        is_stale = minutes_since > threshold_minutes

        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=is_stale,
            last_commit_time=last_commit,
            worktree_exists=True,
        )

    except Exception as e:
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=True,
            error=str(e),
        )


def x_check_wp_staleness__mutmut_53(
    wp_id: str,
    worktree_path: Path,
    threshold_minutes: int = 10,
) -> StaleCheckResult:
    """
    Check if a work package is stale based on VCS activity.

    A WP is considered stale if:
    - Its worktree exists
    - The branch has commits since diverging from main (agent has done work)
    - The last commit is older than threshold_minutes

    A WP with a worktree but NO commits since diverging is NOT stale - the agent
    just started and hasn't committed yet.

    Args:
        wp_id: Work package ID (e.g., "WP01")
        worktree_path: Path to the WP's worktree
        threshold_minutes: Minutes of inactivity before considered stale

    Returns:
        StaleCheckResult with staleness status
    """
    if not worktree_path.exists():
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=False,
        )

    try:
        last_commit, has_own_commits = get_last_meaningful_commit_time(worktree_path)

        if last_commit is None:
            # Can't determine commit time, or no commits on this branch yet
            # If no commits yet (has_own_commits=False), agent just started - not stale
            return StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=True,
                error=None if not has_own_commits else "Could not determine last commit time",
            )

        now = datetime.now(timezone.utc)
        # Ensure last_commit is timezone-aware
        if last_commit.tzinfo is None:
            last_commit = last_commit.replace(tzinfo=timezone.utc)

        delta = now - last_commit
        minutes_since = delta.total_seconds() / 60

        is_stale = minutes_since > threshold_minutes

        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=is_stale,
            last_commit_time=last_commit,
            minutes_since_commit=round(minutes_since, 1),
            )

    except Exception as e:
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=True,
            error=str(e),
        )


def x_check_wp_staleness__mutmut_54(
    wp_id: str,
    worktree_path: Path,
    threshold_minutes: int = 10,
) -> StaleCheckResult:
    """
    Check if a work package is stale based on VCS activity.

    A WP is considered stale if:
    - Its worktree exists
    - The branch has commits since diverging from main (agent has done work)
    - The last commit is older than threshold_minutes

    A WP with a worktree but NO commits since diverging is NOT stale - the agent
    just started and hasn't committed yet.

    Args:
        wp_id: Work package ID (e.g., "WP01")
        worktree_path: Path to the WP's worktree
        threshold_minutes: Minutes of inactivity before considered stale

    Returns:
        StaleCheckResult with staleness status
    """
    if not worktree_path.exists():
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=False,
        )

    try:
        last_commit, has_own_commits = get_last_meaningful_commit_time(worktree_path)

        if last_commit is None:
            # Can't determine commit time, or no commits on this branch yet
            # If no commits yet (has_own_commits=False), agent just started - not stale
            return StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=True,
                error=None if not has_own_commits else "Could not determine last commit time",
            )

        now = datetime.now(timezone.utc)
        # Ensure last_commit is timezone-aware
        if last_commit.tzinfo is None:
            last_commit = last_commit.replace(tzinfo=timezone.utc)

        delta = now - last_commit
        minutes_since = delta.total_seconds() / 60

        is_stale = minutes_since > threshold_minutes

        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=is_stale,
            last_commit_time=last_commit,
            minutes_since_commit=round(None, 1),
            worktree_exists=True,
        )

    except Exception as e:
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=True,
            error=str(e),
        )


def x_check_wp_staleness__mutmut_55(
    wp_id: str,
    worktree_path: Path,
    threshold_minutes: int = 10,
) -> StaleCheckResult:
    """
    Check if a work package is stale based on VCS activity.

    A WP is considered stale if:
    - Its worktree exists
    - The branch has commits since diverging from main (agent has done work)
    - The last commit is older than threshold_minutes

    A WP with a worktree but NO commits since diverging is NOT stale - the agent
    just started and hasn't committed yet.

    Args:
        wp_id: Work package ID (e.g., "WP01")
        worktree_path: Path to the WP's worktree
        threshold_minutes: Minutes of inactivity before considered stale

    Returns:
        StaleCheckResult with staleness status
    """
    if not worktree_path.exists():
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=False,
        )

    try:
        last_commit, has_own_commits = get_last_meaningful_commit_time(worktree_path)

        if last_commit is None:
            # Can't determine commit time, or no commits on this branch yet
            # If no commits yet (has_own_commits=False), agent just started - not stale
            return StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=True,
                error=None if not has_own_commits else "Could not determine last commit time",
            )

        now = datetime.now(timezone.utc)
        # Ensure last_commit is timezone-aware
        if last_commit.tzinfo is None:
            last_commit = last_commit.replace(tzinfo=timezone.utc)

        delta = now - last_commit
        minutes_since = delta.total_seconds() / 60

        is_stale = minutes_since > threshold_minutes

        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=is_stale,
            last_commit_time=last_commit,
            minutes_since_commit=round(minutes_since, None),
            worktree_exists=True,
        )

    except Exception as e:
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=True,
            error=str(e),
        )


def x_check_wp_staleness__mutmut_56(
    wp_id: str,
    worktree_path: Path,
    threshold_minutes: int = 10,
) -> StaleCheckResult:
    """
    Check if a work package is stale based on VCS activity.

    A WP is considered stale if:
    - Its worktree exists
    - The branch has commits since diverging from main (agent has done work)
    - The last commit is older than threshold_minutes

    A WP with a worktree but NO commits since diverging is NOT stale - the agent
    just started and hasn't committed yet.

    Args:
        wp_id: Work package ID (e.g., "WP01")
        worktree_path: Path to the WP's worktree
        threshold_minutes: Minutes of inactivity before considered stale

    Returns:
        StaleCheckResult with staleness status
    """
    if not worktree_path.exists():
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=False,
        )

    try:
        last_commit, has_own_commits = get_last_meaningful_commit_time(worktree_path)

        if last_commit is None:
            # Can't determine commit time, or no commits on this branch yet
            # If no commits yet (has_own_commits=False), agent just started - not stale
            return StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=True,
                error=None if not has_own_commits else "Could not determine last commit time",
            )

        now = datetime.now(timezone.utc)
        # Ensure last_commit is timezone-aware
        if last_commit.tzinfo is None:
            last_commit = last_commit.replace(tzinfo=timezone.utc)

        delta = now - last_commit
        minutes_since = delta.total_seconds() / 60

        is_stale = minutes_since > threshold_minutes

        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=is_stale,
            last_commit_time=last_commit,
            minutes_since_commit=round(1),
            worktree_exists=True,
        )

    except Exception as e:
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=True,
            error=str(e),
        )


def x_check_wp_staleness__mutmut_57(
    wp_id: str,
    worktree_path: Path,
    threshold_minutes: int = 10,
) -> StaleCheckResult:
    """
    Check if a work package is stale based on VCS activity.

    A WP is considered stale if:
    - Its worktree exists
    - The branch has commits since diverging from main (agent has done work)
    - The last commit is older than threshold_minutes

    A WP with a worktree but NO commits since diverging is NOT stale - the agent
    just started and hasn't committed yet.

    Args:
        wp_id: Work package ID (e.g., "WP01")
        worktree_path: Path to the WP's worktree
        threshold_minutes: Minutes of inactivity before considered stale

    Returns:
        StaleCheckResult with staleness status
    """
    if not worktree_path.exists():
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=False,
        )

    try:
        last_commit, has_own_commits = get_last_meaningful_commit_time(worktree_path)

        if last_commit is None:
            # Can't determine commit time, or no commits on this branch yet
            # If no commits yet (has_own_commits=False), agent just started - not stale
            return StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=True,
                error=None if not has_own_commits else "Could not determine last commit time",
            )

        now = datetime.now(timezone.utc)
        # Ensure last_commit is timezone-aware
        if last_commit.tzinfo is None:
            last_commit = last_commit.replace(tzinfo=timezone.utc)

        delta = now - last_commit
        minutes_since = delta.total_seconds() / 60

        is_stale = minutes_since > threshold_minutes

        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=is_stale,
            last_commit_time=last_commit,
            minutes_since_commit=round(minutes_since, ),
            worktree_exists=True,
        )

    except Exception as e:
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=True,
            error=str(e),
        )


def x_check_wp_staleness__mutmut_58(
    wp_id: str,
    worktree_path: Path,
    threshold_minutes: int = 10,
) -> StaleCheckResult:
    """
    Check if a work package is stale based on VCS activity.

    A WP is considered stale if:
    - Its worktree exists
    - The branch has commits since diverging from main (agent has done work)
    - The last commit is older than threshold_minutes

    A WP with a worktree but NO commits since diverging is NOT stale - the agent
    just started and hasn't committed yet.

    Args:
        wp_id: Work package ID (e.g., "WP01")
        worktree_path: Path to the WP's worktree
        threshold_minutes: Minutes of inactivity before considered stale

    Returns:
        StaleCheckResult with staleness status
    """
    if not worktree_path.exists():
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=False,
        )

    try:
        last_commit, has_own_commits = get_last_meaningful_commit_time(worktree_path)

        if last_commit is None:
            # Can't determine commit time, or no commits on this branch yet
            # If no commits yet (has_own_commits=False), agent just started - not stale
            return StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=True,
                error=None if not has_own_commits else "Could not determine last commit time",
            )

        now = datetime.now(timezone.utc)
        # Ensure last_commit is timezone-aware
        if last_commit.tzinfo is None:
            last_commit = last_commit.replace(tzinfo=timezone.utc)

        delta = now - last_commit
        minutes_since = delta.total_seconds() / 60

        is_stale = minutes_since > threshold_minutes

        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=is_stale,
            last_commit_time=last_commit,
            minutes_since_commit=round(minutes_since, 2),
            worktree_exists=True,
        )

    except Exception as e:
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=True,
            error=str(e),
        )


def x_check_wp_staleness__mutmut_59(
    wp_id: str,
    worktree_path: Path,
    threshold_minutes: int = 10,
) -> StaleCheckResult:
    """
    Check if a work package is stale based on VCS activity.

    A WP is considered stale if:
    - Its worktree exists
    - The branch has commits since diverging from main (agent has done work)
    - The last commit is older than threshold_minutes

    A WP with a worktree but NO commits since diverging is NOT stale - the agent
    just started and hasn't committed yet.

    Args:
        wp_id: Work package ID (e.g., "WP01")
        worktree_path: Path to the WP's worktree
        threshold_minutes: Minutes of inactivity before considered stale

    Returns:
        StaleCheckResult with staleness status
    """
    if not worktree_path.exists():
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=False,
        )

    try:
        last_commit, has_own_commits = get_last_meaningful_commit_time(worktree_path)

        if last_commit is None:
            # Can't determine commit time, or no commits on this branch yet
            # If no commits yet (has_own_commits=False), agent just started - not stale
            return StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=True,
                error=None if not has_own_commits else "Could not determine last commit time",
            )

        now = datetime.now(timezone.utc)
        # Ensure last_commit is timezone-aware
        if last_commit.tzinfo is None:
            last_commit = last_commit.replace(tzinfo=timezone.utc)

        delta = now - last_commit
        minutes_since = delta.total_seconds() / 60

        is_stale = minutes_since > threshold_minutes

        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=is_stale,
            last_commit_time=last_commit,
            minutes_since_commit=round(minutes_since, 1),
            worktree_exists=False,
        )

    except Exception as e:
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=True,
            error=str(e),
        )


def x_check_wp_staleness__mutmut_60(
    wp_id: str,
    worktree_path: Path,
    threshold_minutes: int = 10,
) -> StaleCheckResult:
    """
    Check if a work package is stale based on VCS activity.

    A WP is considered stale if:
    - Its worktree exists
    - The branch has commits since diverging from main (agent has done work)
    - The last commit is older than threshold_minutes

    A WP with a worktree but NO commits since diverging is NOT stale - the agent
    just started and hasn't committed yet.

    Args:
        wp_id: Work package ID (e.g., "WP01")
        worktree_path: Path to the WP's worktree
        threshold_minutes: Minutes of inactivity before considered stale

    Returns:
        StaleCheckResult with staleness status
    """
    if not worktree_path.exists():
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=False,
        )

    try:
        last_commit, has_own_commits = get_last_meaningful_commit_time(worktree_path)

        if last_commit is None:
            # Can't determine commit time, or no commits on this branch yet
            # If no commits yet (has_own_commits=False), agent just started - not stale
            return StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=True,
                error=None if not has_own_commits else "Could not determine last commit time",
            )

        now = datetime.now(timezone.utc)
        # Ensure last_commit is timezone-aware
        if last_commit.tzinfo is None:
            last_commit = last_commit.replace(tzinfo=timezone.utc)

        delta = now - last_commit
        minutes_since = delta.total_seconds() / 60

        is_stale = minutes_since > threshold_minutes

        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=is_stale,
            last_commit_time=last_commit,
            minutes_since_commit=round(minutes_since, 1),
            worktree_exists=True,
        )

    except Exception as e:
        return StaleCheckResult(
            wp_id=None,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=True,
            error=str(e),
        )


def x_check_wp_staleness__mutmut_61(
    wp_id: str,
    worktree_path: Path,
    threshold_minutes: int = 10,
) -> StaleCheckResult:
    """
    Check if a work package is stale based on VCS activity.

    A WP is considered stale if:
    - Its worktree exists
    - The branch has commits since diverging from main (agent has done work)
    - The last commit is older than threshold_minutes

    A WP with a worktree but NO commits since diverging is NOT stale - the agent
    just started and hasn't committed yet.

    Args:
        wp_id: Work package ID (e.g., "WP01")
        worktree_path: Path to the WP's worktree
        threshold_minutes: Minutes of inactivity before considered stale

    Returns:
        StaleCheckResult with staleness status
    """
    if not worktree_path.exists():
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=False,
        )

    try:
        last_commit, has_own_commits = get_last_meaningful_commit_time(worktree_path)

        if last_commit is None:
            # Can't determine commit time, or no commits on this branch yet
            # If no commits yet (has_own_commits=False), agent just started - not stale
            return StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=True,
                error=None if not has_own_commits else "Could not determine last commit time",
            )

        now = datetime.now(timezone.utc)
        # Ensure last_commit is timezone-aware
        if last_commit.tzinfo is None:
            last_commit = last_commit.replace(tzinfo=timezone.utc)

        delta = now - last_commit
        minutes_since = delta.total_seconds() / 60

        is_stale = minutes_since > threshold_minutes

        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=is_stale,
            last_commit_time=last_commit,
            minutes_since_commit=round(minutes_since, 1),
            worktree_exists=True,
        )

    except Exception as e:
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=None,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=True,
            error=str(e),
        )


def x_check_wp_staleness__mutmut_62(
    wp_id: str,
    worktree_path: Path,
    threshold_minutes: int = 10,
) -> StaleCheckResult:
    """
    Check if a work package is stale based on VCS activity.

    A WP is considered stale if:
    - Its worktree exists
    - The branch has commits since diverging from main (agent has done work)
    - The last commit is older than threshold_minutes

    A WP with a worktree but NO commits since diverging is NOT stale - the agent
    just started and hasn't committed yet.

    Args:
        wp_id: Work package ID (e.g., "WP01")
        worktree_path: Path to the WP's worktree
        threshold_minutes: Minutes of inactivity before considered stale

    Returns:
        StaleCheckResult with staleness status
    """
    if not worktree_path.exists():
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=False,
        )

    try:
        last_commit, has_own_commits = get_last_meaningful_commit_time(worktree_path)

        if last_commit is None:
            # Can't determine commit time, or no commits on this branch yet
            # If no commits yet (has_own_commits=False), agent just started - not stale
            return StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=True,
                error=None if not has_own_commits else "Could not determine last commit time",
            )

        now = datetime.now(timezone.utc)
        # Ensure last_commit is timezone-aware
        if last_commit.tzinfo is None:
            last_commit = last_commit.replace(tzinfo=timezone.utc)

        delta = now - last_commit
        minutes_since = delta.total_seconds() / 60

        is_stale = minutes_since > threshold_minutes

        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=is_stale,
            last_commit_time=last_commit,
            minutes_since_commit=round(minutes_since, 1),
            worktree_exists=True,
        )

    except Exception as e:
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=None,
            error=str(e),
        )


def x_check_wp_staleness__mutmut_63(
    wp_id: str,
    worktree_path: Path,
    threshold_minutes: int = 10,
) -> StaleCheckResult:
    """
    Check if a work package is stale based on VCS activity.

    A WP is considered stale if:
    - Its worktree exists
    - The branch has commits since diverging from main (agent has done work)
    - The last commit is older than threshold_minutes

    A WP with a worktree but NO commits since diverging is NOT stale - the agent
    just started and hasn't committed yet.

    Args:
        wp_id: Work package ID (e.g., "WP01")
        worktree_path: Path to the WP's worktree
        threshold_minutes: Minutes of inactivity before considered stale

    Returns:
        StaleCheckResult with staleness status
    """
    if not worktree_path.exists():
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=False,
        )

    try:
        last_commit, has_own_commits = get_last_meaningful_commit_time(worktree_path)

        if last_commit is None:
            # Can't determine commit time, or no commits on this branch yet
            # If no commits yet (has_own_commits=False), agent just started - not stale
            return StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=True,
                error=None if not has_own_commits else "Could not determine last commit time",
            )

        now = datetime.now(timezone.utc)
        # Ensure last_commit is timezone-aware
        if last_commit.tzinfo is None:
            last_commit = last_commit.replace(tzinfo=timezone.utc)

        delta = now - last_commit
        minutes_since = delta.total_seconds() / 60

        is_stale = minutes_since > threshold_minutes

        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=is_stale,
            last_commit_time=last_commit,
            minutes_since_commit=round(minutes_since, 1),
            worktree_exists=True,
        )

    except Exception as e:
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=True,
            error=None,
        )


def x_check_wp_staleness__mutmut_64(
    wp_id: str,
    worktree_path: Path,
    threshold_minutes: int = 10,
) -> StaleCheckResult:
    """
    Check if a work package is stale based on VCS activity.

    A WP is considered stale if:
    - Its worktree exists
    - The branch has commits since diverging from main (agent has done work)
    - The last commit is older than threshold_minutes

    A WP with a worktree but NO commits since diverging is NOT stale - the agent
    just started and hasn't committed yet.

    Args:
        wp_id: Work package ID (e.g., "WP01")
        worktree_path: Path to the WP's worktree
        threshold_minutes: Minutes of inactivity before considered stale

    Returns:
        StaleCheckResult with staleness status
    """
    if not worktree_path.exists():
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=False,
        )

    try:
        last_commit, has_own_commits = get_last_meaningful_commit_time(worktree_path)

        if last_commit is None:
            # Can't determine commit time, or no commits on this branch yet
            # If no commits yet (has_own_commits=False), agent just started - not stale
            return StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=True,
                error=None if not has_own_commits else "Could not determine last commit time",
            )

        now = datetime.now(timezone.utc)
        # Ensure last_commit is timezone-aware
        if last_commit.tzinfo is None:
            last_commit = last_commit.replace(tzinfo=timezone.utc)

        delta = now - last_commit
        minutes_since = delta.total_seconds() / 60

        is_stale = minutes_since > threshold_minutes

        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=is_stale,
            last_commit_time=last_commit,
            minutes_since_commit=round(minutes_since, 1),
            worktree_exists=True,
        )

    except Exception as e:
        return StaleCheckResult(
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=True,
            error=str(e),
        )


def x_check_wp_staleness__mutmut_65(
    wp_id: str,
    worktree_path: Path,
    threshold_minutes: int = 10,
) -> StaleCheckResult:
    """
    Check if a work package is stale based on VCS activity.

    A WP is considered stale if:
    - Its worktree exists
    - The branch has commits since diverging from main (agent has done work)
    - The last commit is older than threshold_minutes

    A WP with a worktree but NO commits since diverging is NOT stale - the agent
    just started and hasn't committed yet.

    Args:
        wp_id: Work package ID (e.g., "WP01")
        worktree_path: Path to the WP's worktree
        threshold_minutes: Minutes of inactivity before considered stale

    Returns:
        StaleCheckResult with staleness status
    """
    if not worktree_path.exists():
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=False,
        )

    try:
        last_commit, has_own_commits = get_last_meaningful_commit_time(worktree_path)

        if last_commit is None:
            # Can't determine commit time, or no commits on this branch yet
            # If no commits yet (has_own_commits=False), agent just started - not stale
            return StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=True,
                error=None if not has_own_commits else "Could not determine last commit time",
            )

        now = datetime.now(timezone.utc)
        # Ensure last_commit is timezone-aware
        if last_commit.tzinfo is None:
            last_commit = last_commit.replace(tzinfo=timezone.utc)

        delta = now - last_commit
        minutes_since = delta.total_seconds() / 60

        is_stale = minutes_since > threshold_minutes

        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=is_stale,
            last_commit_time=last_commit,
            minutes_since_commit=round(minutes_since, 1),
            worktree_exists=True,
        )

    except Exception as e:
        return StaleCheckResult(
            wp_id=wp_id,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=True,
            error=str(e),
        )


def x_check_wp_staleness__mutmut_66(
    wp_id: str,
    worktree_path: Path,
    threshold_minutes: int = 10,
) -> StaleCheckResult:
    """
    Check if a work package is stale based on VCS activity.

    A WP is considered stale if:
    - Its worktree exists
    - The branch has commits since diverging from main (agent has done work)
    - The last commit is older than threshold_minutes

    A WP with a worktree but NO commits since diverging is NOT stale - the agent
    just started and hasn't committed yet.

    Args:
        wp_id: Work package ID (e.g., "WP01")
        worktree_path: Path to the WP's worktree
        threshold_minutes: Minutes of inactivity before considered stale

    Returns:
        StaleCheckResult with staleness status
    """
    if not worktree_path.exists():
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=False,
        )

    try:
        last_commit, has_own_commits = get_last_meaningful_commit_time(worktree_path)

        if last_commit is None:
            # Can't determine commit time, or no commits on this branch yet
            # If no commits yet (has_own_commits=False), agent just started - not stale
            return StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=True,
                error=None if not has_own_commits else "Could not determine last commit time",
            )

        now = datetime.now(timezone.utc)
        # Ensure last_commit is timezone-aware
        if last_commit.tzinfo is None:
            last_commit = last_commit.replace(tzinfo=timezone.utc)

        delta = now - last_commit
        minutes_since = delta.total_seconds() / 60

        is_stale = minutes_since > threshold_minutes

        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=is_stale,
            last_commit_time=last_commit,
            minutes_since_commit=round(minutes_since, 1),
            worktree_exists=True,
        )

    except Exception as e:
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            minutes_since_commit=None,
            worktree_exists=True,
            error=str(e),
        )


def x_check_wp_staleness__mutmut_67(
    wp_id: str,
    worktree_path: Path,
    threshold_minutes: int = 10,
) -> StaleCheckResult:
    """
    Check if a work package is stale based on VCS activity.

    A WP is considered stale if:
    - Its worktree exists
    - The branch has commits since diverging from main (agent has done work)
    - The last commit is older than threshold_minutes

    A WP with a worktree but NO commits since diverging is NOT stale - the agent
    just started and hasn't committed yet.

    Args:
        wp_id: Work package ID (e.g., "WP01")
        worktree_path: Path to the WP's worktree
        threshold_minutes: Minutes of inactivity before considered stale

    Returns:
        StaleCheckResult with staleness status
    """
    if not worktree_path.exists():
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=False,
        )

    try:
        last_commit, has_own_commits = get_last_meaningful_commit_time(worktree_path)

        if last_commit is None:
            # Can't determine commit time, or no commits on this branch yet
            # If no commits yet (has_own_commits=False), agent just started - not stale
            return StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=True,
                error=None if not has_own_commits else "Could not determine last commit time",
            )

        now = datetime.now(timezone.utc)
        # Ensure last_commit is timezone-aware
        if last_commit.tzinfo is None:
            last_commit = last_commit.replace(tzinfo=timezone.utc)

        delta = now - last_commit
        minutes_since = delta.total_seconds() / 60

        is_stale = minutes_since > threshold_minutes

        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=is_stale,
            last_commit_time=last_commit,
            minutes_since_commit=round(minutes_since, 1),
            worktree_exists=True,
        )

    except Exception as e:
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            worktree_exists=True,
            error=str(e),
        )


def x_check_wp_staleness__mutmut_68(
    wp_id: str,
    worktree_path: Path,
    threshold_minutes: int = 10,
) -> StaleCheckResult:
    """
    Check if a work package is stale based on VCS activity.

    A WP is considered stale if:
    - Its worktree exists
    - The branch has commits since diverging from main (agent has done work)
    - The last commit is older than threshold_minutes

    A WP with a worktree but NO commits since diverging is NOT stale - the agent
    just started and hasn't committed yet.

    Args:
        wp_id: Work package ID (e.g., "WP01")
        worktree_path: Path to the WP's worktree
        threshold_minutes: Minutes of inactivity before considered stale

    Returns:
        StaleCheckResult with staleness status
    """
    if not worktree_path.exists():
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=False,
        )

    try:
        last_commit, has_own_commits = get_last_meaningful_commit_time(worktree_path)

        if last_commit is None:
            # Can't determine commit time, or no commits on this branch yet
            # If no commits yet (has_own_commits=False), agent just started - not stale
            return StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=True,
                error=None if not has_own_commits else "Could not determine last commit time",
            )

        now = datetime.now(timezone.utc)
        # Ensure last_commit is timezone-aware
        if last_commit.tzinfo is None:
            last_commit = last_commit.replace(tzinfo=timezone.utc)

        delta = now - last_commit
        minutes_since = delta.total_seconds() / 60

        is_stale = minutes_since > threshold_minutes

        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=is_stale,
            last_commit_time=last_commit,
            minutes_since_commit=round(minutes_since, 1),
            worktree_exists=True,
        )

    except Exception as e:
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            error=str(e),
        )


def x_check_wp_staleness__mutmut_69(
    wp_id: str,
    worktree_path: Path,
    threshold_minutes: int = 10,
) -> StaleCheckResult:
    """
    Check if a work package is stale based on VCS activity.

    A WP is considered stale if:
    - Its worktree exists
    - The branch has commits since diverging from main (agent has done work)
    - The last commit is older than threshold_minutes

    A WP with a worktree but NO commits since diverging is NOT stale - the agent
    just started and hasn't committed yet.

    Args:
        wp_id: Work package ID (e.g., "WP01")
        worktree_path: Path to the WP's worktree
        threshold_minutes: Minutes of inactivity before considered stale

    Returns:
        StaleCheckResult with staleness status
    """
    if not worktree_path.exists():
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=False,
        )

    try:
        last_commit, has_own_commits = get_last_meaningful_commit_time(worktree_path)

        if last_commit is None:
            # Can't determine commit time, or no commits on this branch yet
            # If no commits yet (has_own_commits=False), agent just started - not stale
            return StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=True,
                error=None if not has_own_commits else "Could not determine last commit time",
            )

        now = datetime.now(timezone.utc)
        # Ensure last_commit is timezone-aware
        if last_commit.tzinfo is None:
            last_commit = last_commit.replace(tzinfo=timezone.utc)

        delta = now - last_commit
        minutes_since = delta.total_seconds() / 60

        is_stale = minutes_since > threshold_minutes

        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=is_stale,
            last_commit_time=last_commit,
            minutes_since_commit=round(minutes_since, 1),
            worktree_exists=True,
        )

    except Exception as e:
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=True,
            )


def x_check_wp_staleness__mutmut_70(
    wp_id: str,
    worktree_path: Path,
    threshold_minutes: int = 10,
) -> StaleCheckResult:
    """
    Check if a work package is stale based on VCS activity.

    A WP is considered stale if:
    - Its worktree exists
    - The branch has commits since diverging from main (agent has done work)
    - The last commit is older than threshold_minutes

    A WP with a worktree but NO commits since diverging is NOT stale - the agent
    just started and hasn't committed yet.

    Args:
        wp_id: Work package ID (e.g., "WP01")
        worktree_path: Path to the WP's worktree
        threshold_minutes: Minutes of inactivity before considered stale

    Returns:
        StaleCheckResult with staleness status
    """
    if not worktree_path.exists():
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=False,
        )

    try:
        last_commit, has_own_commits = get_last_meaningful_commit_time(worktree_path)

        if last_commit is None:
            # Can't determine commit time, or no commits on this branch yet
            # If no commits yet (has_own_commits=False), agent just started - not stale
            return StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=True,
                error=None if not has_own_commits else "Could not determine last commit time",
            )

        now = datetime.now(timezone.utc)
        # Ensure last_commit is timezone-aware
        if last_commit.tzinfo is None:
            last_commit = last_commit.replace(tzinfo=timezone.utc)

        delta = now - last_commit
        minutes_since = delta.total_seconds() / 60

        is_stale = minutes_since > threshold_minutes

        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=is_stale,
            last_commit_time=last_commit,
            minutes_since_commit=round(minutes_since, 1),
            worktree_exists=True,
        )

    except Exception as e:
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=True,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=True,
            error=str(e),
        )


def x_check_wp_staleness__mutmut_71(
    wp_id: str,
    worktree_path: Path,
    threshold_minutes: int = 10,
) -> StaleCheckResult:
    """
    Check if a work package is stale based on VCS activity.

    A WP is considered stale if:
    - Its worktree exists
    - The branch has commits since diverging from main (agent has done work)
    - The last commit is older than threshold_minutes

    A WP with a worktree but NO commits since diverging is NOT stale - the agent
    just started and hasn't committed yet.

    Args:
        wp_id: Work package ID (e.g., "WP01")
        worktree_path: Path to the WP's worktree
        threshold_minutes: Minutes of inactivity before considered stale

    Returns:
        StaleCheckResult with staleness status
    """
    if not worktree_path.exists():
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=False,
        )

    try:
        last_commit, has_own_commits = get_last_meaningful_commit_time(worktree_path)

        if last_commit is None:
            # Can't determine commit time, or no commits on this branch yet
            # If no commits yet (has_own_commits=False), agent just started - not stale
            return StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=True,
                error=None if not has_own_commits else "Could not determine last commit time",
            )

        now = datetime.now(timezone.utc)
        # Ensure last_commit is timezone-aware
        if last_commit.tzinfo is None:
            last_commit = last_commit.replace(tzinfo=timezone.utc)

        delta = now - last_commit
        minutes_since = delta.total_seconds() / 60

        is_stale = minutes_since > threshold_minutes

        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=is_stale,
            last_commit_time=last_commit,
            minutes_since_commit=round(minutes_since, 1),
            worktree_exists=True,
        )

    except Exception as e:
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=False,
            error=str(e),
        )


def x_check_wp_staleness__mutmut_72(
    wp_id: str,
    worktree_path: Path,
    threshold_minutes: int = 10,
) -> StaleCheckResult:
    """
    Check if a work package is stale based on VCS activity.

    A WP is considered stale if:
    - Its worktree exists
    - The branch has commits since diverging from main (agent has done work)
    - The last commit is older than threshold_minutes

    A WP with a worktree but NO commits since diverging is NOT stale - the agent
    just started and hasn't committed yet.

    Args:
        wp_id: Work package ID (e.g., "WP01")
        worktree_path: Path to the WP's worktree
        threshold_minutes: Minutes of inactivity before considered stale

    Returns:
        StaleCheckResult with staleness status
    """
    if not worktree_path.exists():
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=False,
        )

    try:
        last_commit, has_own_commits = get_last_meaningful_commit_time(worktree_path)

        if last_commit is None:
            # Can't determine commit time, or no commits on this branch yet
            # If no commits yet (has_own_commits=False), agent just started - not stale
            return StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=True,
                error=None if not has_own_commits else "Could not determine last commit time",
            )

        now = datetime.now(timezone.utc)
        # Ensure last_commit is timezone-aware
        if last_commit.tzinfo is None:
            last_commit = last_commit.replace(tzinfo=timezone.utc)

        delta = now - last_commit
        minutes_since = delta.total_seconds() / 60

        is_stale = minutes_since > threshold_minutes

        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=is_stale,
            last_commit_time=last_commit,
            minutes_since_commit=round(minutes_since, 1),
            worktree_exists=True,
        )

    except Exception as e:
        return StaleCheckResult(
            wp_id=wp_id,
            is_stale=False,
            last_commit_time=None,
            minutes_since_commit=None,
            worktree_exists=True,
            error=str(None),
        )

x_check_wp_staleness__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_check_wp_staleness__mutmut_1': x_check_wp_staleness__mutmut_1, 
    'x_check_wp_staleness__mutmut_2': x_check_wp_staleness__mutmut_2, 
    'x_check_wp_staleness__mutmut_3': x_check_wp_staleness__mutmut_3, 
    'x_check_wp_staleness__mutmut_4': x_check_wp_staleness__mutmut_4, 
    'x_check_wp_staleness__mutmut_5': x_check_wp_staleness__mutmut_5, 
    'x_check_wp_staleness__mutmut_6': x_check_wp_staleness__mutmut_6, 
    'x_check_wp_staleness__mutmut_7': x_check_wp_staleness__mutmut_7, 
    'x_check_wp_staleness__mutmut_8': x_check_wp_staleness__mutmut_8, 
    'x_check_wp_staleness__mutmut_9': x_check_wp_staleness__mutmut_9, 
    'x_check_wp_staleness__mutmut_10': x_check_wp_staleness__mutmut_10, 
    'x_check_wp_staleness__mutmut_11': x_check_wp_staleness__mutmut_11, 
    'x_check_wp_staleness__mutmut_12': x_check_wp_staleness__mutmut_12, 
    'x_check_wp_staleness__mutmut_13': x_check_wp_staleness__mutmut_13, 
    'x_check_wp_staleness__mutmut_14': x_check_wp_staleness__mutmut_14, 
    'x_check_wp_staleness__mutmut_15': x_check_wp_staleness__mutmut_15, 
    'x_check_wp_staleness__mutmut_16': x_check_wp_staleness__mutmut_16, 
    'x_check_wp_staleness__mutmut_17': x_check_wp_staleness__mutmut_17, 
    'x_check_wp_staleness__mutmut_18': x_check_wp_staleness__mutmut_18, 
    'x_check_wp_staleness__mutmut_19': x_check_wp_staleness__mutmut_19, 
    'x_check_wp_staleness__mutmut_20': x_check_wp_staleness__mutmut_20, 
    'x_check_wp_staleness__mutmut_21': x_check_wp_staleness__mutmut_21, 
    'x_check_wp_staleness__mutmut_22': x_check_wp_staleness__mutmut_22, 
    'x_check_wp_staleness__mutmut_23': x_check_wp_staleness__mutmut_23, 
    'x_check_wp_staleness__mutmut_24': x_check_wp_staleness__mutmut_24, 
    'x_check_wp_staleness__mutmut_25': x_check_wp_staleness__mutmut_25, 
    'x_check_wp_staleness__mutmut_26': x_check_wp_staleness__mutmut_26, 
    'x_check_wp_staleness__mutmut_27': x_check_wp_staleness__mutmut_27, 
    'x_check_wp_staleness__mutmut_28': x_check_wp_staleness__mutmut_28, 
    'x_check_wp_staleness__mutmut_29': x_check_wp_staleness__mutmut_29, 
    'x_check_wp_staleness__mutmut_30': x_check_wp_staleness__mutmut_30, 
    'x_check_wp_staleness__mutmut_31': x_check_wp_staleness__mutmut_31, 
    'x_check_wp_staleness__mutmut_32': x_check_wp_staleness__mutmut_32, 
    'x_check_wp_staleness__mutmut_33': x_check_wp_staleness__mutmut_33, 
    'x_check_wp_staleness__mutmut_34': x_check_wp_staleness__mutmut_34, 
    'x_check_wp_staleness__mutmut_35': x_check_wp_staleness__mutmut_35, 
    'x_check_wp_staleness__mutmut_36': x_check_wp_staleness__mutmut_36, 
    'x_check_wp_staleness__mutmut_37': x_check_wp_staleness__mutmut_37, 
    'x_check_wp_staleness__mutmut_38': x_check_wp_staleness__mutmut_38, 
    'x_check_wp_staleness__mutmut_39': x_check_wp_staleness__mutmut_39, 
    'x_check_wp_staleness__mutmut_40': x_check_wp_staleness__mutmut_40, 
    'x_check_wp_staleness__mutmut_41': x_check_wp_staleness__mutmut_41, 
    'x_check_wp_staleness__mutmut_42': x_check_wp_staleness__mutmut_42, 
    'x_check_wp_staleness__mutmut_43': x_check_wp_staleness__mutmut_43, 
    'x_check_wp_staleness__mutmut_44': x_check_wp_staleness__mutmut_44, 
    'x_check_wp_staleness__mutmut_45': x_check_wp_staleness__mutmut_45, 
    'x_check_wp_staleness__mutmut_46': x_check_wp_staleness__mutmut_46, 
    'x_check_wp_staleness__mutmut_47': x_check_wp_staleness__mutmut_47, 
    'x_check_wp_staleness__mutmut_48': x_check_wp_staleness__mutmut_48, 
    'x_check_wp_staleness__mutmut_49': x_check_wp_staleness__mutmut_49, 
    'x_check_wp_staleness__mutmut_50': x_check_wp_staleness__mutmut_50, 
    'x_check_wp_staleness__mutmut_51': x_check_wp_staleness__mutmut_51, 
    'x_check_wp_staleness__mutmut_52': x_check_wp_staleness__mutmut_52, 
    'x_check_wp_staleness__mutmut_53': x_check_wp_staleness__mutmut_53, 
    'x_check_wp_staleness__mutmut_54': x_check_wp_staleness__mutmut_54, 
    'x_check_wp_staleness__mutmut_55': x_check_wp_staleness__mutmut_55, 
    'x_check_wp_staleness__mutmut_56': x_check_wp_staleness__mutmut_56, 
    'x_check_wp_staleness__mutmut_57': x_check_wp_staleness__mutmut_57, 
    'x_check_wp_staleness__mutmut_58': x_check_wp_staleness__mutmut_58, 
    'x_check_wp_staleness__mutmut_59': x_check_wp_staleness__mutmut_59, 
    'x_check_wp_staleness__mutmut_60': x_check_wp_staleness__mutmut_60, 
    'x_check_wp_staleness__mutmut_61': x_check_wp_staleness__mutmut_61, 
    'x_check_wp_staleness__mutmut_62': x_check_wp_staleness__mutmut_62, 
    'x_check_wp_staleness__mutmut_63': x_check_wp_staleness__mutmut_63, 
    'x_check_wp_staleness__mutmut_64': x_check_wp_staleness__mutmut_64, 
    'x_check_wp_staleness__mutmut_65': x_check_wp_staleness__mutmut_65, 
    'x_check_wp_staleness__mutmut_66': x_check_wp_staleness__mutmut_66, 
    'x_check_wp_staleness__mutmut_67': x_check_wp_staleness__mutmut_67, 
    'x_check_wp_staleness__mutmut_68': x_check_wp_staleness__mutmut_68, 
    'x_check_wp_staleness__mutmut_69': x_check_wp_staleness__mutmut_69, 
    'x_check_wp_staleness__mutmut_70': x_check_wp_staleness__mutmut_70, 
    'x_check_wp_staleness__mutmut_71': x_check_wp_staleness__mutmut_71, 
    'x_check_wp_staleness__mutmut_72': x_check_wp_staleness__mutmut_72
}
x_check_wp_staleness__mutmut_orig.__name__ = 'x_check_wp_staleness'


def find_worktree_for_wp(
    main_repo_root: Path,
    feature_slug: str,
    wp_id: str,
) -> Path | None:
    args = [main_repo_root, feature_slug, wp_id]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_find_worktree_for_wp__mutmut_orig, x_find_worktree_for_wp__mutmut_mutants, args, kwargs, None)


def x_find_worktree_for_wp__mutmut_orig(
    main_repo_root: Path,
    feature_slug: str,
    wp_id: str,
) -> Path | None:
    """
    Find the worktree path for a given work package.

    Args:
        main_repo_root: Root of the main repository
        feature_slug: Feature slug (e.g., "001-my-feature")
        wp_id: Work package ID (e.g., "WP01")

    Returns:
        Path to worktree if found, None otherwise
    """
    worktrees_dir = main_repo_root / ".worktrees"
    if not worktrees_dir.exists():
        return None

    # Expected pattern: feature_slug-WP01
    expected_name = f"{feature_slug}-{wp_id}"
    worktree_path = worktrees_dir / expected_name

    if worktree_path.exists():
        return worktree_path

    # Try case-insensitive search
    for item in worktrees_dir.iterdir():
        if item.is_dir() and item.name.lower() == expected_name.lower():
            return item

    return None


def x_find_worktree_for_wp__mutmut_1(
    main_repo_root: Path,
    feature_slug: str,
    wp_id: str,
) -> Path | None:
    """
    Find the worktree path for a given work package.

    Args:
        main_repo_root: Root of the main repository
        feature_slug: Feature slug (e.g., "001-my-feature")
        wp_id: Work package ID (e.g., "WP01")

    Returns:
        Path to worktree if found, None otherwise
    """
    worktrees_dir = None
    if not worktrees_dir.exists():
        return None

    # Expected pattern: feature_slug-WP01
    expected_name = f"{feature_slug}-{wp_id}"
    worktree_path = worktrees_dir / expected_name

    if worktree_path.exists():
        return worktree_path

    # Try case-insensitive search
    for item in worktrees_dir.iterdir():
        if item.is_dir() and item.name.lower() == expected_name.lower():
            return item

    return None


def x_find_worktree_for_wp__mutmut_2(
    main_repo_root: Path,
    feature_slug: str,
    wp_id: str,
) -> Path | None:
    """
    Find the worktree path for a given work package.

    Args:
        main_repo_root: Root of the main repository
        feature_slug: Feature slug (e.g., "001-my-feature")
        wp_id: Work package ID (e.g., "WP01")

    Returns:
        Path to worktree if found, None otherwise
    """
    worktrees_dir = main_repo_root * ".worktrees"
    if not worktrees_dir.exists():
        return None

    # Expected pattern: feature_slug-WP01
    expected_name = f"{feature_slug}-{wp_id}"
    worktree_path = worktrees_dir / expected_name

    if worktree_path.exists():
        return worktree_path

    # Try case-insensitive search
    for item in worktrees_dir.iterdir():
        if item.is_dir() and item.name.lower() == expected_name.lower():
            return item

    return None


def x_find_worktree_for_wp__mutmut_3(
    main_repo_root: Path,
    feature_slug: str,
    wp_id: str,
) -> Path | None:
    """
    Find the worktree path for a given work package.

    Args:
        main_repo_root: Root of the main repository
        feature_slug: Feature slug (e.g., "001-my-feature")
        wp_id: Work package ID (e.g., "WP01")

    Returns:
        Path to worktree if found, None otherwise
    """
    worktrees_dir = main_repo_root / "XX.worktreesXX"
    if not worktrees_dir.exists():
        return None

    # Expected pattern: feature_slug-WP01
    expected_name = f"{feature_slug}-{wp_id}"
    worktree_path = worktrees_dir / expected_name

    if worktree_path.exists():
        return worktree_path

    # Try case-insensitive search
    for item in worktrees_dir.iterdir():
        if item.is_dir() and item.name.lower() == expected_name.lower():
            return item

    return None


def x_find_worktree_for_wp__mutmut_4(
    main_repo_root: Path,
    feature_slug: str,
    wp_id: str,
) -> Path | None:
    """
    Find the worktree path for a given work package.

    Args:
        main_repo_root: Root of the main repository
        feature_slug: Feature slug (e.g., "001-my-feature")
        wp_id: Work package ID (e.g., "WP01")

    Returns:
        Path to worktree if found, None otherwise
    """
    worktrees_dir = main_repo_root / ".WORKTREES"
    if not worktrees_dir.exists():
        return None

    # Expected pattern: feature_slug-WP01
    expected_name = f"{feature_slug}-{wp_id}"
    worktree_path = worktrees_dir / expected_name

    if worktree_path.exists():
        return worktree_path

    # Try case-insensitive search
    for item in worktrees_dir.iterdir():
        if item.is_dir() and item.name.lower() == expected_name.lower():
            return item

    return None


def x_find_worktree_for_wp__mutmut_5(
    main_repo_root: Path,
    feature_slug: str,
    wp_id: str,
) -> Path | None:
    """
    Find the worktree path for a given work package.

    Args:
        main_repo_root: Root of the main repository
        feature_slug: Feature slug (e.g., "001-my-feature")
        wp_id: Work package ID (e.g., "WP01")

    Returns:
        Path to worktree if found, None otherwise
    """
    worktrees_dir = main_repo_root / ".worktrees"
    if worktrees_dir.exists():
        return None

    # Expected pattern: feature_slug-WP01
    expected_name = f"{feature_slug}-{wp_id}"
    worktree_path = worktrees_dir / expected_name

    if worktree_path.exists():
        return worktree_path

    # Try case-insensitive search
    for item in worktrees_dir.iterdir():
        if item.is_dir() and item.name.lower() == expected_name.lower():
            return item

    return None


def x_find_worktree_for_wp__mutmut_6(
    main_repo_root: Path,
    feature_slug: str,
    wp_id: str,
) -> Path | None:
    """
    Find the worktree path for a given work package.

    Args:
        main_repo_root: Root of the main repository
        feature_slug: Feature slug (e.g., "001-my-feature")
        wp_id: Work package ID (e.g., "WP01")

    Returns:
        Path to worktree if found, None otherwise
    """
    worktrees_dir = main_repo_root / ".worktrees"
    if not worktrees_dir.exists():
        return None

    # Expected pattern: feature_slug-WP01
    expected_name = None
    worktree_path = worktrees_dir / expected_name

    if worktree_path.exists():
        return worktree_path

    # Try case-insensitive search
    for item in worktrees_dir.iterdir():
        if item.is_dir() and item.name.lower() == expected_name.lower():
            return item

    return None


def x_find_worktree_for_wp__mutmut_7(
    main_repo_root: Path,
    feature_slug: str,
    wp_id: str,
) -> Path | None:
    """
    Find the worktree path for a given work package.

    Args:
        main_repo_root: Root of the main repository
        feature_slug: Feature slug (e.g., "001-my-feature")
        wp_id: Work package ID (e.g., "WP01")

    Returns:
        Path to worktree if found, None otherwise
    """
    worktrees_dir = main_repo_root / ".worktrees"
    if not worktrees_dir.exists():
        return None

    # Expected pattern: feature_slug-WP01
    expected_name = f"{feature_slug}-{wp_id}"
    worktree_path = None

    if worktree_path.exists():
        return worktree_path

    # Try case-insensitive search
    for item in worktrees_dir.iterdir():
        if item.is_dir() and item.name.lower() == expected_name.lower():
            return item

    return None


def x_find_worktree_for_wp__mutmut_8(
    main_repo_root: Path,
    feature_slug: str,
    wp_id: str,
) -> Path | None:
    """
    Find the worktree path for a given work package.

    Args:
        main_repo_root: Root of the main repository
        feature_slug: Feature slug (e.g., "001-my-feature")
        wp_id: Work package ID (e.g., "WP01")

    Returns:
        Path to worktree if found, None otherwise
    """
    worktrees_dir = main_repo_root / ".worktrees"
    if not worktrees_dir.exists():
        return None

    # Expected pattern: feature_slug-WP01
    expected_name = f"{feature_slug}-{wp_id}"
    worktree_path = worktrees_dir * expected_name

    if worktree_path.exists():
        return worktree_path

    # Try case-insensitive search
    for item in worktrees_dir.iterdir():
        if item.is_dir() and item.name.lower() == expected_name.lower():
            return item

    return None


def x_find_worktree_for_wp__mutmut_9(
    main_repo_root: Path,
    feature_slug: str,
    wp_id: str,
) -> Path | None:
    """
    Find the worktree path for a given work package.

    Args:
        main_repo_root: Root of the main repository
        feature_slug: Feature slug (e.g., "001-my-feature")
        wp_id: Work package ID (e.g., "WP01")

    Returns:
        Path to worktree if found, None otherwise
    """
    worktrees_dir = main_repo_root / ".worktrees"
    if not worktrees_dir.exists():
        return None

    # Expected pattern: feature_slug-WP01
    expected_name = f"{feature_slug}-{wp_id}"
    worktree_path = worktrees_dir / expected_name

    if worktree_path.exists():
        return worktree_path

    # Try case-insensitive search
    for item in worktrees_dir.iterdir():
        if item.is_dir() or item.name.lower() == expected_name.lower():
            return item

    return None


def x_find_worktree_for_wp__mutmut_10(
    main_repo_root: Path,
    feature_slug: str,
    wp_id: str,
) -> Path | None:
    """
    Find the worktree path for a given work package.

    Args:
        main_repo_root: Root of the main repository
        feature_slug: Feature slug (e.g., "001-my-feature")
        wp_id: Work package ID (e.g., "WP01")

    Returns:
        Path to worktree if found, None otherwise
    """
    worktrees_dir = main_repo_root / ".worktrees"
    if not worktrees_dir.exists():
        return None

    # Expected pattern: feature_slug-WP01
    expected_name = f"{feature_slug}-{wp_id}"
    worktree_path = worktrees_dir / expected_name

    if worktree_path.exists():
        return worktree_path

    # Try case-insensitive search
    for item in worktrees_dir.iterdir():
        if item.is_dir() and item.name.upper() == expected_name.lower():
            return item

    return None


def x_find_worktree_for_wp__mutmut_11(
    main_repo_root: Path,
    feature_slug: str,
    wp_id: str,
) -> Path | None:
    """
    Find the worktree path for a given work package.

    Args:
        main_repo_root: Root of the main repository
        feature_slug: Feature slug (e.g., "001-my-feature")
        wp_id: Work package ID (e.g., "WP01")

    Returns:
        Path to worktree if found, None otherwise
    """
    worktrees_dir = main_repo_root / ".worktrees"
    if not worktrees_dir.exists():
        return None

    # Expected pattern: feature_slug-WP01
    expected_name = f"{feature_slug}-{wp_id}"
    worktree_path = worktrees_dir / expected_name

    if worktree_path.exists():
        return worktree_path

    # Try case-insensitive search
    for item in worktrees_dir.iterdir():
        if item.is_dir() and item.name.lower() != expected_name.lower():
            return item

    return None


def x_find_worktree_for_wp__mutmut_12(
    main_repo_root: Path,
    feature_slug: str,
    wp_id: str,
) -> Path | None:
    """
    Find the worktree path for a given work package.

    Args:
        main_repo_root: Root of the main repository
        feature_slug: Feature slug (e.g., "001-my-feature")
        wp_id: Work package ID (e.g., "WP01")

    Returns:
        Path to worktree if found, None otherwise
    """
    worktrees_dir = main_repo_root / ".worktrees"
    if not worktrees_dir.exists():
        return None

    # Expected pattern: feature_slug-WP01
    expected_name = f"{feature_slug}-{wp_id}"
    worktree_path = worktrees_dir / expected_name

    if worktree_path.exists():
        return worktree_path

    # Try case-insensitive search
    for item in worktrees_dir.iterdir():
        if item.is_dir() and item.name.lower() == expected_name.upper():
            return item

    return None

x_find_worktree_for_wp__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_find_worktree_for_wp__mutmut_1': x_find_worktree_for_wp__mutmut_1, 
    'x_find_worktree_for_wp__mutmut_2': x_find_worktree_for_wp__mutmut_2, 
    'x_find_worktree_for_wp__mutmut_3': x_find_worktree_for_wp__mutmut_3, 
    'x_find_worktree_for_wp__mutmut_4': x_find_worktree_for_wp__mutmut_4, 
    'x_find_worktree_for_wp__mutmut_5': x_find_worktree_for_wp__mutmut_5, 
    'x_find_worktree_for_wp__mutmut_6': x_find_worktree_for_wp__mutmut_6, 
    'x_find_worktree_for_wp__mutmut_7': x_find_worktree_for_wp__mutmut_7, 
    'x_find_worktree_for_wp__mutmut_8': x_find_worktree_for_wp__mutmut_8, 
    'x_find_worktree_for_wp__mutmut_9': x_find_worktree_for_wp__mutmut_9, 
    'x_find_worktree_for_wp__mutmut_10': x_find_worktree_for_wp__mutmut_10, 
    'x_find_worktree_for_wp__mutmut_11': x_find_worktree_for_wp__mutmut_11, 
    'x_find_worktree_for_wp__mutmut_12': x_find_worktree_for_wp__mutmut_12
}
x_find_worktree_for_wp__mutmut_orig.__name__ = 'x_find_worktree_for_wp'


def check_doing_wps_for_staleness(
    main_repo_root: Path,
    feature_slug: str,
    doing_wps: list[dict],
    threshold_minutes: int = 10,
) -> dict[str, StaleCheckResult]:
    args = [main_repo_root, feature_slug, doing_wps, threshold_minutes]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_check_doing_wps_for_staleness__mutmut_orig, x_check_doing_wps_for_staleness__mutmut_mutants, args, kwargs, None)


def x_check_doing_wps_for_staleness__mutmut_orig(
    main_repo_root: Path,
    feature_slug: str,
    doing_wps: list[dict],
    threshold_minutes: int = 10,
) -> dict[str, StaleCheckResult]:
    """
    Check all WPs in "doing" lane for staleness.

    Args:
        main_repo_root: Root of the main repository
        feature_slug: Feature slug
        doing_wps: List of WP dicts with at least 'id' key
        threshold_minutes: Minutes of inactivity threshold

    Returns:
        Dict mapping WP ID to StaleCheckResult
    """
    results = {}

    for wp in doing_wps:
        wp_id = wp.get("id") or wp.get("work_package_id")
        if not wp_id:
            continue

        worktree_path = find_worktree_for_wp(main_repo_root, feature_slug, wp_id)

        if worktree_path:
            result = check_wp_staleness(wp_id, worktree_path, threshold_minutes)
        else:
            result = StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=False,
            )

        results[wp_id] = result

    return results


def x_check_doing_wps_for_staleness__mutmut_1(
    main_repo_root: Path,
    feature_slug: str,
    doing_wps: list[dict],
    threshold_minutes: int = 11,
) -> dict[str, StaleCheckResult]:
    """
    Check all WPs in "doing" lane for staleness.

    Args:
        main_repo_root: Root of the main repository
        feature_slug: Feature slug
        doing_wps: List of WP dicts with at least 'id' key
        threshold_minutes: Minutes of inactivity threshold

    Returns:
        Dict mapping WP ID to StaleCheckResult
    """
    results = {}

    for wp in doing_wps:
        wp_id = wp.get("id") or wp.get("work_package_id")
        if not wp_id:
            continue

        worktree_path = find_worktree_for_wp(main_repo_root, feature_slug, wp_id)

        if worktree_path:
            result = check_wp_staleness(wp_id, worktree_path, threshold_minutes)
        else:
            result = StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=False,
            )

        results[wp_id] = result

    return results


def x_check_doing_wps_for_staleness__mutmut_2(
    main_repo_root: Path,
    feature_slug: str,
    doing_wps: list[dict],
    threshold_minutes: int = 10,
) -> dict[str, StaleCheckResult]:
    """
    Check all WPs in "doing" lane for staleness.

    Args:
        main_repo_root: Root of the main repository
        feature_slug: Feature slug
        doing_wps: List of WP dicts with at least 'id' key
        threshold_minutes: Minutes of inactivity threshold

    Returns:
        Dict mapping WP ID to StaleCheckResult
    """
    results = None

    for wp in doing_wps:
        wp_id = wp.get("id") or wp.get("work_package_id")
        if not wp_id:
            continue

        worktree_path = find_worktree_for_wp(main_repo_root, feature_slug, wp_id)

        if worktree_path:
            result = check_wp_staleness(wp_id, worktree_path, threshold_minutes)
        else:
            result = StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=False,
            )

        results[wp_id] = result

    return results


def x_check_doing_wps_for_staleness__mutmut_3(
    main_repo_root: Path,
    feature_slug: str,
    doing_wps: list[dict],
    threshold_minutes: int = 10,
) -> dict[str, StaleCheckResult]:
    """
    Check all WPs in "doing" lane for staleness.

    Args:
        main_repo_root: Root of the main repository
        feature_slug: Feature slug
        doing_wps: List of WP dicts with at least 'id' key
        threshold_minutes: Minutes of inactivity threshold

    Returns:
        Dict mapping WP ID to StaleCheckResult
    """
    results = {}

    for wp in doing_wps:
        wp_id = None
        if not wp_id:
            continue

        worktree_path = find_worktree_for_wp(main_repo_root, feature_slug, wp_id)

        if worktree_path:
            result = check_wp_staleness(wp_id, worktree_path, threshold_minutes)
        else:
            result = StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=False,
            )

        results[wp_id] = result

    return results


def x_check_doing_wps_for_staleness__mutmut_4(
    main_repo_root: Path,
    feature_slug: str,
    doing_wps: list[dict],
    threshold_minutes: int = 10,
) -> dict[str, StaleCheckResult]:
    """
    Check all WPs in "doing" lane for staleness.

    Args:
        main_repo_root: Root of the main repository
        feature_slug: Feature slug
        doing_wps: List of WP dicts with at least 'id' key
        threshold_minutes: Minutes of inactivity threshold

    Returns:
        Dict mapping WP ID to StaleCheckResult
    """
    results = {}

    for wp in doing_wps:
        wp_id = wp.get("id") and wp.get("work_package_id")
        if not wp_id:
            continue

        worktree_path = find_worktree_for_wp(main_repo_root, feature_slug, wp_id)

        if worktree_path:
            result = check_wp_staleness(wp_id, worktree_path, threshold_minutes)
        else:
            result = StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=False,
            )

        results[wp_id] = result

    return results


def x_check_doing_wps_for_staleness__mutmut_5(
    main_repo_root: Path,
    feature_slug: str,
    doing_wps: list[dict],
    threshold_minutes: int = 10,
) -> dict[str, StaleCheckResult]:
    """
    Check all WPs in "doing" lane for staleness.

    Args:
        main_repo_root: Root of the main repository
        feature_slug: Feature slug
        doing_wps: List of WP dicts with at least 'id' key
        threshold_minutes: Minutes of inactivity threshold

    Returns:
        Dict mapping WP ID to StaleCheckResult
    """
    results = {}

    for wp in doing_wps:
        wp_id = wp.get(None) or wp.get("work_package_id")
        if not wp_id:
            continue

        worktree_path = find_worktree_for_wp(main_repo_root, feature_slug, wp_id)

        if worktree_path:
            result = check_wp_staleness(wp_id, worktree_path, threshold_minutes)
        else:
            result = StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=False,
            )

        results[wp_id] = result

    return results


def x_check_doing_wps_for_staleness__mutmut_6(
    main_repo_root: Path,
    feature_slug: str,
    doing_wps: list[dict],
    threshold_minutes: int = 10,
) -> dict[str, StaleCheckResult]:
    """
    Check all WPs in "doing" lane for staleness.

    Args:
        main_repo_root: Root of the main repository
        feature_slug: Feature slug
        doing_wps: List of WP dicts with at least 'id' key
        threshold_minutes: Minutes of inactivity threshold

    Returns:
        Dict mapping WP ID to StaleCheckResult
    """
    results = {}

    for wp in doing_wps:
        wp_id = wp.get("XXidXX") or wp.get("work_package_id")
        if not wp_id:
            continue

        worktree_path = find_worktree_for_wp(main_repo_root, feature_slug, wp_id)

        if worktree_path:
            result = check_wp_staleness(wp_id, worktree_path, threshold_minutes)
        else:
            result = StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=False,
            )

        results[wp_id] = result

    return results


def x_check_doing_wps_for_staleness__mutmut_7(
    main_repo_root: Path,
    feature_slug: str,
    doing_wps: list[dict],
    threshold_minutes: int = 10,
) -> dict[str, StaleCheckResult]:
    """
    Check all WPs in "doing" lane for staleness.

    Args:
        main_repo_root: Root of the main repository
        feature_slug: Feature slug
        doing_wps: List of WP dicts with at least 'id' key
        threshold_minutes: Minutes of inactivity threshold

    Returns:
        Dict mapping WP ID to StaleCheckResult
    """
    results = {}

    for wp in doing_wps:
        wp_id = wp.get("ID") or wp.get("work_package_id")
        if not wp_id:
            continue

        worktree_path = find_worktree_for_wp(main_repo_root, feature_slug, wp_id)

        if worktree_path:
            result = check_wp_staleness(wp_id, worktree_path, threshold_minutes)
        else:
            result = StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=False,
            )

        results[wp_id] = result

    return results


def x_check_doing_wps_for_staleness__mutmut_8(
    main_repo_root: Path,
    feature_slug: str,
    doing_wps: list[dict],
    threshold_minutes: int = 10,
) -> dict[str, StaleCheckResult]:
    """
    Check all WPs in "doing" lane for staleness.

    Args:
        main_repo_root: Root of the main repository
        feature_slug: Feature slug
        doing_wps: List of WP dicts with at least 'id' key
        threshold_minutes: Minutes of inactivity threshold

    Returns:
        Dict mapping WP ID to StaleCheckResult
    """
    results = {}

    for wp in doing_wps:
        wp_id = wp.get("id") or wp.get(None)
        if not wp_id:
            continue

        worktree_path = find_worktree_for_wp(main_repo_root, feature_slug, wp_id)

        if worktree_path:
            result = check_wp_staleness(wp_id, worktree_path, threshold_minutes)
        else:
            result = StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=False,
            )

        results[wp_id] = result

    return results


def x_check_doing_wps_for_staleness__mutmut_9(
    main_repo_root: Path,
    feature_slug: str,
    doing_wps: list[dict],
    threshold_minutes: int = 10,
) -> dict[str, StaleCheckResult]:
    """
    Check all WPs in "doing" lane for staleness.

    Args:
        main_repo_root: Root of the main repository
        feature_slug: Feature slug
        doing_wps: List of WP dicts with at least 'id' key
        threshold_minutes: Minutes of inactivity threshold

    Returns:
        Dict mapping WP ID to StaleCheckResult
    """
    results = {}

    for wp in doing_wps:
        wp_id = wp.get("id") or wp.get("XXwork_package_idXX")
        if not wp_id:
            continue

        worktree_path = find_worktree_for_wp(main_repo_root, feature_slug, wp_id)

        if worktree_path:
            result = check_wp_staleness(wp_id, worktree_path, threshold_minutes)
        else:
            result = StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=False,
            )

        results[wp_id] = result

    return results


def x_check_doing_wps_for_staleness__mutmut_10(
    main_repo_root: Path,
    feature_slug: str,
    doing_wps: list[dict],
    threshold_minutes: int = 10,
) -> dict[str, StaleCheckResult]:
    """
    Check all WPs in "doing" lane for staleness.

    Args:
        main_repo_root: Root of the main repository
        feature_slug: Feature slug
        doing_wps: List of WP dicts with at least 'id' key
        threshold_minutes: Minutes of inactivity threshold

    Returns:
        Dict mapping WP ID to StaleCheckResult
    """
    results = {}

    for wp in doing_wps:
        wp_id = wp.get("id") or wp.get("WORK_PACKAGE_ID")
        if not wp_id:
            continue

        worktree_path = find_worktree_for_wp(main_repo_root, feature_slug, wp_id)

        if worktree_path:
            result = check_wp_staleness(wp_id, worktree_path, threshold_minutes)
        else:
            result = StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=False,
            )

        results[wp_id] = result

    return results


def x_check_doing_wps_for_staleness__mutmut_11(
    main_repo_root: Path,
    feature_slug: str,
    doing_wps: list[dict],
    threshold_minutes: int = 10,
) -> dict[str, StaleCheckResult]:
    """
    Check all WPs in "doing" lane for staleness.

    Args:
        main_repo_root: Root of the main repository
        feature_slug: Feature slug
        doing_wps: List of WP dicts with at least 'id' key
        threshold_minutes: Minutes of inactivity threshold

    Returns:
        Dict mapping WP ID to StaleCheckResult
    """
    results = {}

    for wp in doing_wps:
        wp_id = wp.get("id") or wp.get("work_package_id")
        if wp_id:
            continue

        worktree_path = find_worktree_for_wp(main_repo_root, feature_slug, wp_id)

        if worktree_path:
            result = check_wp_staleness(wp_id, worktree_path, threshold_minutes)
        else:
            result = StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=False,
            )

        results[wp_id] = result

    return results


def x_check_doing_wps_for_staleness__mutmut_12(
    main_repo_root: Path,
    feature_slug: str,
    doing_wps: list[dict],
    threshold_minutes: int = 10,
) -> dict[str, StaleCheckResult]:
    """
    Check all WPs in "doing" lane for staleness.

    Args:
        main_repo_root: Root of the main repository
        feature_slug: Feature slug
        doing_wps: List of WP dicts with at least 'id' key
        threshold_minutes: Minutes of inactivity threshold

    Returns:
        Dict mapping WP ID to StaleCheckResult
    """
    results = {}

    for wp in doing_wps:
        wp_id = wp.get("id") or wp.get("work_package_id")
        if not wp_id:
            break

        worktree_path = find_worktree_for_wp(main_repo_root, feature_slug, wp_id)

        if worktree_path:
            result = check_wp_staleness(wp_id, worktree_path, threshold_minutes)
        else:
            result = StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=False,
            )

        results[wp_id] = result

    return results


def x_check_doing_wps_for_staleness__mutmut_13(
    main_repo_root: Path,
    feature_slug: str,
    doing_wps: list[dict],
    threshold_minutes: int = 10,
) -> dict[str, StaleCheckResult]:
    """
    Check all WPs in "doing" lane for staleness.

    Args:
        main_repo_root: Root of the main repository
        feature_slug: Feature slug
        doing_wps: List of WP dicts with at least 'id' key
        threshold_minutes: Minutes of inactivity threshold

    Returns:
        Dict mapping WP ID to StaleCheckResult
    """
    results = {}

    for wp in doing_wps:
        wp_id = wp.get("id") or wp.get("work_package_id")
        if not wp_id:
            continue

        worktree_path = None

        if worktree_path:
            result = check_wp_staleness(wp_id, worktree_path, threshold_minutes)
        else:
            result = StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=False,
            )

        results[wp_id] = result

    return results


def x_check_doing_wps_for_staleness__mutmut_14(
    main_repo_root: Path,
    feature_slug: str,
    doing_wps: list[dict],
    threshold_minutes: int = 10,
) -> dict[str, StaleCheckResult]:
    """
    Check all WPs in "doing" lane for staleness.

    Args:
        main_repo_root: Root of the main repository
        feature_slug: Feature slug
        doing_wps: List of WP dicts with at least 'id' key
        threshold_minutes: Minutes of inactivity threshold

    Returns:
        Dict mapping WP ID to StaleCheckResult
    """
    results = {}

    for wp in doing_wps:
        wp_id = wp.get("id") or wp.get("work_package_id")
        if not wp_id:
            continue

        worktree_path = find_worktree_for_wp(None, feature_slug, wp_id)

        if worktree_path:
            result = check_wp_staleness(wp_id, worktree_path, threshold_minutes)
        else:
            result = StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=False,
            )

        results[wp_id] = result

    return results


def x_check_doing_wps_for_staleness__mutmut_15(
    main_repo_root: Path,
    feature_slug: str,
    doing_wps: list[dict],
    threshold_minutes: int = 10,
) -> dict[str, StaleCheckResult]:
    """
    Check all WPs in "doing" lane for staleness.

    Args:
        main_repo_root: Root of the main repository
        feature_slug: Feature slug
        doing_wps: List of WP dicts with at least 'id' key
        threshold_minutes: Minutes of inactivity threshold

    Returns:
        Dict mapping WP ID to StaleCheckResult
    """
    results = {}

    for wp in doing_wps:
        wp_id = wp.get("id") or wp.get("work_package_id")
        if not wp_id:
            continue

        worktree_path = find_worktree_for_wp(main_repo_root, None, wp_id)

        if worktree_path:
            result = check_wp_staleness(wp_id, worktree_path, threshold_minutes)
        else:
            result = StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=False,
            )

        results[wp_id] = result

    return results


def x_check_doing_wps_for_staleness__mutmut_16(
    main_repo_root: Path,
    feature_slug: str,
    doing_wps: list[dict],
    threshold_minutes: int = 10,
) -> dict[str, StaleCheckResult]:
    """
    Check all WPs in "doing" lane for staleness.

    Args:
        main_repo_root: Root of the main repository
        feature_slug: Feature slug
        doing_wps: List of WP dicts with at least 'id' key
        threshold_minutes: Minutes of inactivity threshold

    Returns:
        Dict mapping WP ID to StaleCheckResult
    """
    results = {}

    for wp in doing_wps:
        wp_id = wp.get("id") or wp.get("work_package_id")
        if not wp_id:
            continue

        worktree_path = find_worktree_for_wp(main_repo_root, feature_slug, None)

        if worktree_path:
            result = check_wp_staleness(wp_id, worktree_path, threshold_minutes)
        else:
            result = StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=False,
            )

        results[wp_id] = result

    return results


def x_check_doing_wps_for_staleness__mutmut_17(
    main_repo_root: Path,
    feature_slug: str,
    doing_wps: list[dict],
    threshold_minutes: int = 10,
) -> dict[str, StaleCheckResult]:
    """
    Check all WPs in "doing" lane for staleness.

    Args:
        main_repo_root: Root of the main repository
        feature_slug: Feature slug
        doing_wps: List of WP dicts with at least 'id' key
        threshold_minutes: Minutes of inactivity threshold

    Returns:
        Dict mapping WP ID to StaleCheckResult
    """
    results = {}

    for wp in doing_wps:
        wp_id = wp.get("id") or wp.get("work_package_id")
        if not wp_id:
            continue

        worktree_path = find_worktree_for_wp(feature_slug, wp_id)

        if worktree_path:
            result = check_wp_staleness(wp_id, worktree_path, threshold_minutes)
        else:
            result = StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=False,
            )

        results[wp_id] = result

    return results


def x_check_doing_wps_for_staleness__mutmut_18(
    main_repo_root: Path,
    feature_slug: str,
    doing_wps: list[dict],
    threshold_minutes: int = 10,
) -> dict[str, StaleCheckResult]:
    """
    Check all WPs in "doing" lane for staleness.

    Args:
        main_repo_root: Root of the main repository
        feature_slug: Feature slug
        doing_wps: List of WP dicts with at least 'id' key
        threshold_minutes: Minutes of inactivity threshold

    Returns:
        Dict mapping WP ID to StaleCheckResult
    """
    results = {}

    for wp in doing_wps:
        wp_id = wp.get("id") or wp.get("work_package_id")
        if not wp_id:
            continue

        worktree_path = find_worktree_for_wp(main_repo_root, wp_id)

        if worktree_path:
            result = check_wp_staleness(wp_id, worktree_path, threshold_minutes)
        else:
            result = StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=False,
            )

        results[wp_id] = result

    return results


def x_check_doing_wps_for_staleness__mutmut_19(
    main_repo_root: Path,
    feature_slug: str,
    doing_wps: list[dict],
    threshold_minutes: int = 10,
) -> dict[str, StaleCheckResult]:
    """
    Check all WPs in "doing" lane for staleness.

    Args:
        main_repo_root: Root of the main repository
        feature_slug: Feature slug
        doing_wps: List of WP dicts with at least 'id' key
        threshold_minutes: Minutes of inactivity threshold

    Returns:
        Dict mapping WP ID to StaleCheckResult
    """
    results = {}

    for wp in doing_wps:
        wp_id = wp.get("id") or wp.get("work_package_id")
        if not wp_id:
            continue

        worktree_path = find_worktree_for_wp(main_repo_root, feature_slug, )

        if worktree_path:
            result = check_wp_staleness(wp_id, worktree_path, threshold_minutes)
        else:
            result = StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=False,
            )

        results[wp_id] = result

    return results


def x_check_doing_wps_for_staleness__mutmut_20(
    main_repo_root: Path,
    feature_slug: str,
    doing_wps: list[dict],
    threshold_minutes: int = 10,
) -> dict[str, StaleCheckResult]:
    """
    Check all WPs in "doing" lane for staleness.

    Args:
        main_repo_root: Root of the main repository
        feature_slug: Feature slug
        doing_wps: List of WP dicts with at least 'id' key
        threshold_minutes: Minutes of inactivity threshold

    Returns:
        Dict mapping WP ID to StaleCheckResult
    """
    results = {}

    for wp in doing_wps:
        wp_id = wp.get("id") or wp.get("work_package_id")
        if not wp_id:
            continue

        worktree_path = find_worktree_for_wp(main_repo_root, feature_slug, wp_id)

        if worktree_path:
            result = None
        else:
            result = StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=False,
            )

        results[wp_id] = result

    return results


def x_check_doing_wps_for_staleness__mutmut_21(
    main_repo_root: Path,
    feature_slug: str,
    doing_wps: list[dict],
    threshold_minutes: int = 10,
) -> dict[str, StaleCheckResult]:
    """
    Check all WPs in "doing" lane for staleness.

    Args:
        main_repo_root: Root of the main repository
        feature_slug: Feature slug
        doing_wps: List of WP dicts with at least 'id' key
        threshold_minutes: Minutes of inactivity threshold

    Returns:
        Dict mapping WP ID to StaleCheckResult
    """
    results = {}

    for wp in doing_wps:
        wp_id = wp.get("id") or wp.get("work_package_id")
        if not wp_id:
            continue

        worktree_path = find_worktree_for_wp(main_repo_root, feature_slug, wp_id)

        if worktree_path:
            result = check_wp_staleness(None, worktree_path, threshold_minutes)
        else:
            result = StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=False,
            )

        results[wp_id] = result

    return results


def x_check_doing_wps_for_staleness__mutmut_22(
    main_repo_root: Path,
    feature_slug: str,
    doing_wps: list[dict],
    threshold_minutes: int = 10,
) -> dict[str, StaleCheckResult]:
    """
    Check all WPs in "doing" lane for staleness.

    Args:
        main_repo_root: Root of the main repository
        feature_slug: Feature slug
        doing_wps: List of WP dicts with at least 'id' key
        threshold_minutes: Minutes of inactivity threshold

    Returns:
        Dict mapping WP ID to StaleCheckResult
    """
    results = {}

    for wp in doing_wps:
        wp_id = wp.get("id") or wp.get("work_package_id")
        if not wp_id:
            continue

        worktree_path = find_worktree_for_wp(main_repo_root, feature_slug, wp_id)

        if worktree_path:
            result = check_wp_staleness(wp_id, None, threshold_minutes)
        else:
            result = StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=False,
            )

        results[wp_id] = result

    return results


def x_check_doing_wps_for_staleness__mutmut_23(
    main_repo_root: Path,
    feature_slug: str,
    doing_wps: list[dict],
    threshold_minutes: int = 10,
) -> dict[str, StaleCheckResult]:
    """
    Check all WPs in "doing" lane for staleness.

    Args:
        main_repo_root: Root of the main repository
        feature_slug: Feature slug
        doing_wps: List of WP dicts with at least 'id' key
        threshold_minutes: Minutes of inactivity threshold

    Returns:
        Dict mapping WP ID to StaleCheckResult
    """
    results = {}

    for wp in doing_wps:
        wp_id = wp.get("id") or wp.get("work_package_id")
        if not wp_id:
            continue

        worktree_path = find_worktree_for_wp(main_repo_root, feature_slug, wp_id)

        if worktree_path:
            result = check_wp_staleness(wp_id, worktree_path, None)
        else:
            result = StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=False,
            )

        results[wp_id] = result

    return results


def x_check_doing_wps_for_staleness__mutmut_24(
    main_repo_root: Path,
    feature_slug: str,
    doing_wps: list[dict],
    threshold_minutes: int = 10,
) -> dict[str, StaleCheckResult]:
    """
    Check all WPs in "doing" lane for staleness.

    Args:
        main_repo_root: Root of the main repository
        feature_slug: Feature slug
        doing_wps: List of WP dicts with at least 'id' key
        threshold_minutes: Minutes of inactivity threshold

    Returns:
        Dict mapping WP ID to StaleCheckResult
    """
    results = {}

    for wp in doing_wps:
        wp_id = wp.get("id") or wp.get("work_package_id")
        if not wp_id:
            continue

        worktree_path = find_worktree_for_wp(main_repo_root, feature_slug, wp_id)

        if worktree_path:
            result = check_wp_staleness(worktree_path, threshold_minutes)
        else:
            result = StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=False,
            )

        results[wp_id] = result

    return results


def x_check_doing_wps_for_staleness__mutmut_25(
    main_repo_root: Path,
    feature_slug: str,
    doing_wps: list[dict],
    threshold_minutes: int = 10,
) -> dict[str, StaleCheckResult]:
    """
    Check all WPs in "doing" lane for staleness.

    Args:
        main_repo_root: Root of the main repository
        feature_slug: Feature slug
        doing_wps: List of WP dicts with at least 'id' key
        threshold_minutes: Minutes of inactivity threshold

    Returns:
        Dict mapping WP ID to StaleCheckResult
    """
    results = {}

    for wp in doing_wps:
        wp_id = wp.get("id") or wp.get("work_package_id")
        if not wp_id:
            continue

        worktree_path = find_worktree_for_wp(main_repo_root, feature_slug, wp_id)

        if worktree_path:
            result = check_wp_staleness(wp_id, threshold_minutes)
        else:
            result = StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=False,
            )

        results[wp_id] = result

    return results


def x_check_doing_wps_for_staleness__mutmut_26(
    main_repo_root: Path,
    feature_slug: str,
    doing_wps: list[dict],
    threshold_minutes: int = 10,
) -> dict[str, StaleCheckResult]:
    """
    Check all WPs in "doing" lane for staleness.

    Args:
        main_repo_root: Root of the main repository
        feature_slug: Feature slug
        doing_wps: List of WP dicts with at least 'id' key
        threshold_minutes: Minutes of inactivity threshold

    Returns:
        Dict mapping WP ID to StaleCheckResult
    """
    results = {}

    for wp in doing_wps:
        wp_id = wp.get("id") or wp.get("work_package_id")
        if not wp_id:
            continue

        worktree_path = find_worktree_for_wp(main_repo_root, feature_slug, wp_id)

        if worktree_path:
            result = check_wp_staleness(wp_id, worktree_path, )
        else:
            result = StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=False,
            )

        results[wp_id] = result

    return results


def x_check_doing_wps_for_staleness__mutmut_27(
    main_repo_root: Path,
    feature_slug: str,
    doing_wps: list[dict],
    threshold_minutes: int = 10,
) -> dict[str, StaleCheckResult]:
    """
    Check all WPs in "doing" lane for staleness.

    Args:
        main_repo_root: Root of the main repository
        feature_slug: Feature slug
        doing_wps: List of WP dicts with at least 'id' key
        threshold_minutes: Minutes of inactivity threshold

    Returns:
        Dict mapping WP ID to StaleCheckResult
    """
    results = {}

    for wp in doing_wps:
        wp_id = wp.get("id") or wp.get("work_package_id")
        if not wp_id:
            continue

        worktree_path = find_worktree_for_wp(main_repo_root, feature_slug, wp_id)

        if worktree_path:
            result = check_wp_staleness(wp_id, worktree_path, threshold_minutes)
        else:
            result = None

        results[wp_id] = result

    return results


def x_check_doing_wps_for_staleness__mutmut_28(
    main_repo_root: Path,
    feature_slug: str,
    doing_wps: list[dict],
    threshold_minutes: int = 10,
) -> dict[str, StaleCheckResult]:
    """
    Check all WPs in "doing" lane for staleness.

    Args:
        main_repo_root: Root of the main repository
        feature_slug: Feature slug
        doing_wps: List of WP dicts with at least 'id' key
        threshold_minutes: Minutes of inactivity threshold

    Returns:
        Dict mapping WP ID to StaleCheckResult
    """
    results = {}

    for wp in doing_wps:
        wp_id = wp.get("id") or wp.get("work_package_id")
        if not wp_id:
            continue

        worktree_path = find_worktree_for_wp(main_repo_root, feature_slug, wp_id)

        if worktree_path:
            result = check_wp_staleness(wp_id, worktree_path, threshold_minutes)
        else:
            result = StaleCheckResult(
                wp_id=None,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=False,
            )

        results[wp_id] = result

    return results


def x_check_doing_wps_for_staleness__mutmut_29(
    main_repo_root: Path,
    feature_slug: str,
    doing_wps: list[dict],
    threshold_minutes: int = 10,
) -> dict[str, StaleCheckResult]:
    """
    Check all WPs in "doing" lane for staleness.

    Args:
        main_repo_root: Root of the main repository
        feature_slug: Feature slug
        doing_wps: List of WP dicts with at least 'id' key
        threshold_minutes: Minutes of inactivity threshold

    Returns:
        Dict mapping WP ID to StaleCheckResult
    """
    results = {}

    for wp in doing_wps:
        wp_id = wp.get("id") or wp.get("work_package_id")
        if not wp_id:
            continue

        worktree_path = find_worktree_for_wp(main_repo_root, feature_slug, wp_id)

        if worktree_path:
            result = check_wp_staleness(wp_id, worktree_path, threshold_minutes)
        else:
            result = StaleCheckResult(
                wp_id=wp_id,
                is_stale=None,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=False,
            )

        results[wp_id] = result

    return results


def x_check_doing_wps_for_staleness__mutmut_30(
    main_repo_root: Path,
    feature_slug: str,
    doing_wps: list[dict],
    threshold_minutes: int = 10,
) -> dict[str, StaleCheckResult]:
    """
    Check all WPs in "doing" lane for staleness.

    Args:
        main_repo_root: Root of the main repository
        feature_slug: Feature slug
        doing_wps: List of WP dicts with at least 'id' key
        threshold_minutes: Minutes of inactivity threshold

    Returns:
        Dict mapping WP ID to StaleCheckResult
    """
    results = {}

    for wp in doing_wps:
        wp_id = wp.get("id") or wp.get("work_package_id")
        if not wp_id:
            continue

        worktree_path = find_worktree_for_wp(main_repo_root, feature_slug, wp_id)

        if worktree_path:
            result = check_wp_staleness(wp_id, worktree_path, threshold_minutes)
        else:
            result = StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=None,
            )

        results[wp_id] = result

    return results


def x_check_doing_wps_for_staleness__mutmut_31(
    main_repo_root: Path,
    feature_slug: str,
    doing_wps: list[dict],
    threshold_minutes: int = 10,
) -> dict[str, StaleCheckResult]:
    """
    Check all WPs in "doing" lane for staleness.

    Args:
        main_repo_root: Root of the main repository
        feature_slug: Feature slug
        doing_wps: List of WP dicts with at least 'id' key
        threshold_minutes: Minutes of inactivity threshold

    Returns:
        Dict mapping WP ID to StaleCheckResult
    """
    results = {}

    for wp in doing_wps:
        wp_id = wp.get("id") or wp.get("work_package_id")
        if not wp_id:
            continue

        worktree_path = find_worktree_for_wp(main_repo_root, feature_slug, wp_id)

        if worktree_path:
            result = check_wp_staleness(wp_id, worktree_path, threshold_minutes)
        else:
            result = StaleCheckResult(
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=False,
            )

        results[wp_id] = result

    return results


def x_check_doing_wps_for_staleness__mutmut_32(
    main_repo_root: Path,
    feature_slug: str,
    doing_wps: list[dict],
    threshold_minutes: int = 10,
) -> dict[str, StaleCheckResult]:
    """
    Check all WPs in "doing" lane for staleness.

    Args:
        main_repo_root: Root of the main repository
        feature_slug: Feature slug
        doing_wps: List of WP dicts with at least 'id' key
        threshold_minutes: Minutes of inactivity threshold

    Returns:
        Dict mapping WP ID to StaleCheckResult
    """
    results = {}

    for wp in doing_wps:
        wp_id = wp.get("id") or wp.get("work_package_id")
        if not wp_id:
            continue

        worktree_path = find_worktree_for_wp(main_repo_root, feature_slug, wp_id)

        if worktree_path:
            result = check_wp_staleness(wp_id, worktree_path, threshold_minutes)
        else:
            result = StaleCheckResult(
                wp_id=wp_id,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=False,
            )

        results[wp_id] = result

    return results


def x_check_doing_wps_for_staleness__mutmut_33(
    main_repo_root: Path,
    feature_slug: str,
    doing_wps: list[dict],
    threshold_minutes: int = 10,
) -> dict[str, StaleCheckResult]:
    """
    Check all WPs in "doing" lane for staleness.

    Args:
        main_repo_root: Root of the main repository
        feature_slug: Feature slug
        doing_wps: List of WP dicts with at least 'id' key
        threshold_minutes: Minutes of inactivity threshold

    Returns:
        Dict mapping WP ID to StaleCheckResult
    """
    results = {}

    for wp in doing_wps:
        wp_id = wp.get("id") or wp.get("work_package_id")
        if not wp_id:
            continue

        worktree_path = find_worktree_for_wp(main_repo_root, feature_slug, wp_id)

        if worktree_path:
            result = check_wp_staleness(wp_id, worktree_path, threshold_minutes)
        else:
            result = StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                minutes_since_commit=None,
                worktree_exists=False,
            )

        results[wp_id] = result

    return results


def x_check_doing_wps_for_staleness__mutmut_34(
    main_repo_root: Path,
    feature_slug: str,
    doing_wps: list[dict],
    threshold_minutes: int = 10,
) -> dict[str, StaleCheckResult]:
    """
    Check all WPs in "doing" lane for staleness.

    Args:
        main_repo_root: Root of the main repository
        feature_slug: Feature slug
        doing_wps: List of WP dicts with at least 'id' key
        threshold_minutes: Minutes of inactivity threshold

    Returns:
        Dict mapping WP ID to StaleCheckResult
    """
    results = {}

    for wp in doing_wps:
        wp_id = wp.get("id") or wp.get("work_package_id")
        if not wp_id:
            continue

        worktree_path = find_worktree_for_wp(main_repo_root, feature_slug, wp_id)

        if worktree_path:
            result = check_wp_staleness(wp_id, worktree_path, threshold_minutes)
        else:
            result = StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                worktree_exists=False,
            )

        results[wp_id] = result

    return results


def x_check_doing_wps_for_staleness__mutmut_35(
    main_repo_root: Path,
    feature_slug: str,
    doing_wps: list[dict],
    threshold_minutes: int = 10,
) -> dict[str, StaleCheckResult]:
    """
    Check all WPs in "doing" lane for staleness.

    Args:
        main_repo_root: Root of the main repository
        feature_slug: Feature slug
        doing_wps: List of WP dicts with at least 'id' key
        threshold_minutes: Minutes of inactivity threshold

    Returns:
        Dict mapping WP ID to StaleCheckResult
    """
    results = {}

    for wp in doing_wps:
        wp_id = wp.get("id") or wp.get("work_package_id")
        if not wp_id:
            continue

        worktree_path = find_worktree_for_wp(main_repo_root, feature_slug, wp_id)

        if worktree_path:
            result = check_wp_staleness(wp_id, worktree_path, threshold_minutes)
        else:
            result = StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                )

        results[wp_id] = result

    return results


def x_check_doing_wps_for_staleness__mutmut_36(
    main_repo_root: Path,
    feature_slug: str,
    doing_wps: list[dict],
    threshold_minutes: int = 10,
) -> dict[str, StaleCheckResult]:
    """
    Check all WPs in "doing" lane for staleness.

    Args:
        main_repo_root: Root of the main repository
        feature_slug: Feature slug
        doing_wps: List of WP dicts with at least 'id' key
        threshold_minutes: Minutes of inactivity threshold

    Returns:
        Dict mapping WP ID to StaleCheckResult
    """
    results = {}

    for wp in doing_wps:
        wp_id = wp.get("id") or wp.get("work_package_id")
        if not wp_id:
            continue

        worktree_path = find_worktree_for_wp(main_repo_root, feature_slug, wp_id)

        if worktree_path:
            result = check_wp_staleness(wp_id, worktree_path, threshold_minutes)
        else:
            result = StaleCheckResult(
                wp_id=wp_id,
                is_stale=True,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=False,
            )

        results[wp_id] = result

    return results


def x_check_doing_wps_for_staleness__mutmut_37(
    main_repo_root: Path,
    feature_slug: str,
    doing_wps: list[dict],
    threshold_minutes: int = 10,
) -> dict[str, StaleCheckResult]:
    """
    Check all WPs in "doing" lane for staleness.

    Args:
        main_repo_root: Root of the main repository
        feature_slug: Feature slug
        doing_wps: List of WP dicts with at least 'id' key
        threshold_minutes: Minutes of inactivity threshold

    Returns:
        Dict mapping WP ID to StaleCheckResult
    """
    results = {}

    for wp in doing_wps:
        wp_id = wp.get("id") or wp.get("work_package_id")
        if not wp_id:
            continue

        worktree_path = find_worktree_for_wp(main_repo_root, feature_slug, wp_id)

        if worktree_path:
            result = check_wp_staleness(wp_id, worktree_path, threshold_minutes)
        else:
            result = StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=True,
            )

        results[wp_id] = result

    return results


def x_check_doing_wps_for_staleness__mutmut_38(
    main_repo_root: Path,
    feature_slug: str,
    doing_wps: list[dict],
    threshold_minutes: int = 10,
) -> dict[str, StaleCheckResult]:
    """
    Check all WPs in "doing" lane for staleness.

    Args:
        main_repo_root: Root of the main repository
        feature_slug: Feature slug
        doing_wps: List of WP dicts with at least 'id' key
        threshold_minutes: Minutes of inactivity threshold

    Returns:
        Dict mapping WP ID to StaleCheckResult
    """
    results = {}

    for wp in doing_wps:
        wp_id = wp.get("id") or wp.get("work_package_id")
        if not wp_id:
            continue

        worktree_path = find_worktree_for_wp(main_repo_root, feature_slug, wp_id)

        if worktree_path:
            result = check_wp_staleness(wp_id, worktree_path, threshold_minutes)
        else:
            result = StaleCheckResult(
                wp_id=wp_id,
                is_stale=False,
                last_commit_time=None,
                minutes_since_commit=None,
                worktree_exists=False,
            )

        results[wp_id] = None

    return results

x_check_doing_wps_for_staleness__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_check_doing_wps_for_staleness__mutmut_1': x_check_doing_wps_for_staleness__mutmut_1, 
    'x_check_doing_wps_for_staleness__mutmut_2': x_check_doing_wps_for_staleness__mutmut_2, 
    'x_check_doing_wps_for_staleness__mutmut_3': x_check_doing_wps_for_staleness__mutmut_3, 
    'x_check_doing_wps_for_staleness__mutmut_4': x_check_doing_wps_for_staleness__mutmut_4, 
    'x_check_doing_wps_for_staleness__mutmut_5': x_check_doing_wps_for_staleness__mutmut_5, 
    'x_check_doing_wps_for_staleness__mutmut_6': x_check_doing_wps_for_staleness__mutmut_6, 
    'x_check_doing_wps_for_staleness__mutmut_7': x_check_doing_wps_for_staleness__mutmut_7, 
    'x_check_doing_wps_for_staleness__mutmut_8': x_check_doing_wps_for_staleness__mutmut_8, 
    'x_check_doing_wps_for_staleness__mutmut_9': x_check_doing_wps_for_staleness__mutmut_9, 
    'x_check_doing_wps_for_staleness__mutmut_10': x_check_doing_wps_for_staleness__mutmut_10, 
    'x_check_doing_wps_for_staleness__mutmut_11': x_check_doing_wps_for_staleness__mutmut_11, 
    'x_check_doing_wps_for_staleness__mutmut_12': x_check_doing_wps_for_staleness__mutmut_12, 
    'x_check_doing_wps_for_staleness__mutmut_13': x_check_doing_wps_for_staleness__mutmut_13, 
    'x_check_doing_wps_for_staleness__mutmut_14': x_check_doing_wps_for_staleness__mutmut_14, 
    'x_check_doing_wps_for_staleness__mutmut_15': x_check_doing_wps_for_staleness__mutmut_15, 
    'x_check_doing_wps_for_staleness__mutmut_16': x_check_doing_wps_for_staleness__mutmut_16, 
    'x_check_doing_wps_for_staleness__mutmut_17': x_check_doing_wps_for_staleness__mutmut_17, 
    'x_check_doing_wps_for_staleness__mutmut_18': x_check_doing_wps_for_staleness__mutmut_18, 
    'x_check_doing_wps_for_staleness__mutmut_19': x_check_doing_wps_for_staleness__mutmut_19, 
    'x_check_doing_wps_for_staleness__mutmut_20': x_check_doing_wps_for_staleness__mutmut_20, 
    'x_check_doing_wps_for_staleness__mutmut_21': x_check_doing_wps_for_staleness__mutmut_21, 
    'x_check_doing_wps_for_staleness__mutmut_22': x_check_doing_wps_for_staleness__mutmut_22, 
    'x_check_doing_wps_for_staleness__mutmut_23': x_check_doing_wps_for_staleness__mutmut_23, 
    'x_check_doing_wps_for_staleness__mutmut_24': x_check_doing_wps_for_staleness__mutmut_24, 
    'x_check_doing_wps_for_staleness__mutmut_25': x_check_doing_wps_for_staleness__mutmut_25, 
    'x_check_doing_wps_for_staleness__mutmut_26': x_check_doing_wps_for_staleness__mutmut_26, 
    'x_check_doing_wps_for_staleness__mutmut_27': x_check_doing_wps_for_staleness__mutmut_27, 
    'x_check_doing_wps_for_staleness__mutmut_28': x_check_doing_wps_for_staleness__mutmut_28, 
    'x_check_doing_wps_for_staleness__mutmut_29': x_check_doing_wps_for_staleness__mutmut_29, 
    'x_check_doing_wps_for_staleness__mutmut_30': x_check_doing_wps_for_staleness__mutmut_30, 
    'x_check_doing_wps_for_staleness__mutmut_31': x_check_doing_wps_for_staleness__mutmut_31, 
    'x_check_doing_wps_for_staleness__mutmut_32': x_check_doing_wps_for_staleness__mutmut_32, 
    'x_check_doing_wps_for_staleness__mutmut_33': x_check_doing_wps_for_staleness__mutmut_33, 
    'x_check_doing_wps_for_staleness__mutmut_34': x_check_doing_wps_for_staleness__mutmut_34, 
    'x_check_doing_wps_for_staleness__mutmut_35': x_check_doing_wps_for_staleness__mutmut_35, 
    'x_check_doing_wps_for_staleness__mutmut_36': x_check_doing_wps_for_staleness__mutmut_36, 
    'x_check_doing_wps_for_staleness__mutmut_37': x_check_doing_wps_for_staleness__mutmut_37, 
    'x_check_doing_wps_for_staleness__mutmut_38': x_check_doing_wps_for_staleness__mutmut_38
}
x_check_doing_wps_for_staleness__mutmut_orig.__name__ = 'x_check_doing_wps_for_staleness'
