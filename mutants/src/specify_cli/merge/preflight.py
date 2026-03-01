"""Pre-flight validation for merge operations.

Implements FR-001 through FR-004: checking worktree status and target branch
divergence before any merge operation begins.
"""

from __future__ import annotations

import logging
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
import re

from rich.console import Console
from rich.table import Table

from specify_cli.core.constants import KITTY_SPECS_DIR, WORKTREES_DIR
from specify_cli.core.dependency_graph import build_dependency_graph

logger = logging.getLogger(__name__)

__all__ = [
    "WPStatus",
    "PreflightResult",
    "check_worktree_status",
    "check_target_divergence",
    "run_preflight",
    "display_preflight_result",
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


@dataclass
class WPStatus:
    """Status of a single WP worktree during pre-flight."""

    wp_id: str
    worktree_path: Path
    branch_name: str
    is_clean: bool
    error: str | None = None


@dataclass
class PreflightResult:
    """Result of pre-merge validation checks."""

    passed: bool
    wp_statuses: list[WPStatus] = field(default_factory=list)
    target_diverged: bool = False
    target_divergence_msg: str | None = None
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


def check_worktree_status(worktree_path: Path, wp_id: str, branch_name: str) -> WPStatus:
    args = [worktree_path, wp_id, branch_name]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_check_worktree_status__mutmut_orig, x_check_worktree_status__mutmut_mutants, args, kwargs, None)


def x_check_worktree_status__mutmut_orig(worktree_path: Path, wp_id: str, branch_name: str) -> WPStatus:
    """Check if a worktree has uncommitted changes.

    Args:
        worktree_path: Path to the worktree directory
        wp_id: Work package ID (e.g., "WP01")
        branch_name: Name of the branch

    Returns:
        WPStatus with is_clean=True if no uncommitted changes
    """
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=str(worktree_path),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        is_clean = not result.stdout.strip()
        error = None if is_clean else f"Uncommitted changes in {worktree_path.name}"
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=is_clean,
            error=error,
        )
    except (OSError, subprocess.SubprocessError) as e:
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=False,
            error=str(e),
        )


def x_check_worktree_status__mutmut_1(worktree_path: Path, wp_id: str, branch_name: str) -> WPStatus:
    """Check if a worktree has uncommitted changes.

    Args:
        worktree_path: Path to the worktree directory
        wp_id: Work package ID (e.g., "WP01")
        branch_name: Name of the branch

    Returns:
        WPStatus with is_clean=True if no uncommitted changes
    """
    try:
        result = None
        is_clean = not result.stdout.strip()
        error = None if is_clean else f"Uncommitted changes in {worktree_path.name}"
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=is_clean,
            error=error,
        )
    except (OSError, subprocess.SubprocessError) as e:
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=False,
            error=str(e),
        )


def x_check_worktree_status__mutmut_2(worktree_path: Path, wp_id: str, branch_name: str) -> WPStatus:
    """Check if a worktree has uncommitted changes.

    Args:
        worktree_path: Path to the worktree directory
        wp_id: Work package ID (e.g., "WP01")
        branch_name: Name of the branch

    Returns:
        WPStatus with is_clean=True if no uncommitted changes
    """
    try:
        result = subprocess.run(
            None,
            cwd=str(worktree_path),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        is_clean = not result.stdout.strip()
        error = None if is_clean else f"Uncommitted changes in {worktree_path.name}"
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=is_clean,
            error=error,
        )
    except (OSError, subprocess.SubprocessError) as e:
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=False,
            error=str(e),
        )


def x_check_worktree_status__mutmut_3(worktree_path: Path, wp_id: str, branch_name: str) -> WPStatus:
    """Check if a worktree has uncommitted changes.

    Args:
        worktree_path: Path to the worktree directory
        wp_id: Work package ID (e.g., "WP01")
        branch_name: Name of the branch

    Returns:
        WPStatus with is_clean=True if no uncommitted changes
    """
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=None,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        is_clean = not result.stdout.strip()
        error = None if is_clean else f"Uncommitted changes in {worktree_path.name}"
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=is_clean,
            error=error,
        )
    except (OSError, subprocess.SubprocessError) as e:
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=False,
            error=str(e),
        )


def x_check_worktree_status__mutmut_4(worktree_path: Path, wp_id: str, branch_name: str) -> WPStatus:
    """Check if a worktree has uncommitted changes.

    Args:
        worktree_path: Path to the worktree directory
        wp_id: Work package ID (e.g., "WP01")
        branch_name: Name of the branch

    Returns:
        WPStatus with is_clean=True if no uncommitted changes
    """
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=str(worktree_path),
            capture_output=None,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        is_clean = not result.stdout.strip()
        error = None if is_clean else f"Uncommitted changes in {worktree_path.name}"
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=is_clean,
            error=error,
        )
    except (OSError, subprocess.SubprocessError) as e:
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=False,
            error=str(e),
        )


def x_check_worktree_status__mutmut_5(worktree_path: Path, wp_id: str, branch_name: str) -> WPStatus:
    """Check if a worktree has uncommitted changes.

    Args:
        worktree_path: Path to the worktree directory
        wp_id: Work package ID (e.g., "WP01")
        branch_name: Name of the branch

    Returns:
        WPStatus with is_clean=True if no uncommitted changes
    """
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=str(worktree_path),
            capture_output=True,
            text=None,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        is_clean = not result.stdout.strip()
        error = None if is_clean else f"Uncommitted changes in {worktree_path.name}"
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=is_clean,
            error=error,
        )
    except (OSError, subprocess.SubprocessError) as e:
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=False,
            error=str(e),
        )


def x_check_worktree_status__mutmut_6(worktree_path: Path, wp_id: str, branch_name: str) -> WPStatus:
    """Check if a worktree has uncommitted changes.

    Args:
        worktree_path: Path to the worktree directory
        wp_id: Work package ID (e.g., "WP01")
        branch_name: Name of the branch

    Returns:
        WPStatus with is_clean=True if no uncommitted changes
    """
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=str(worktree_path),
            capture_output=True,
            text=True,
            encoding=None,
            errors="replace",
            check=False,
        )
        is_clean = not result.stdout.strip()
        error = None if is_clean else f"Uncommitted changes in {worktree_path.name}"
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=is_clean,
            error=error,
        )
    except (OSError, subprocess.SubprocessError) as e:
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=False,
            error=str(e),
        )


def x_check_worktree_status__mutmut_7(worktree_path: Path, wp_id: str, branch_name: str) -> WPStatus:
    """Check if a worktree has uncommitted changes.

    Args:
        worktree_path: Path to the worktree directory
        wp_id: Work package ID (e.g., "WP01")
        branch_name: Name of the branch

    Returns:
        WPStatus with is_clean=True if no uncommitted changes
    """
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=str(worktree_path),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors=None,
            check=False,
        )
        is_clean = not result.stdout.strip()
        error = None if is_clean else f"Uncommitted changes in {worktree_path.name}"
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=is_clean,
            error=error,
        )
    except (OSError, subprocess.SubprocessError) as e:
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=False,
            error=str(e),
        )


def x_check_worktree_status__mutmut_8(worktree_path: Path, wp_id: str, branch_name: str) -> WPStatus:
    """Check if a worktree has uncommitted changes.

    Args:
        worktree_path: Path to the worktree directory
        wp_id: Work package ID (e.g., "WP01")
        branch_name: Name of the branch

    Returns:
        WPStatus with is_clean=True if no uncommitted changes
    """
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=str(worktree_path),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=None,
        )
        is_clean = not result.stdout.strip()
        error = None if is_clean else f"Uncommitted changes in {worktree_path.name}"
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=is_clean,
            error=error,
        )
    except (OSError, subprocess.SubprocessError) as e:
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=False,
            error=str(e),
        )


def x_check_worktree_status__mutmut_9(worktree_path: Path, wp_id: str, branch_name: str) -> WPStatus:
    """Check if a worktree has uncommitted changes.

    Args:
        worktree_path: Path to the worktree directory
        wp_id: Work package ID (e.g., "WP01")
        branch_name: Name of the branch

    Returns:
        WPStatus with is_clean=True if no uncommitted changes
    """
    try:
        result = subprocess.run(
            cwd=str(worktree_path),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        is_clean = not result.stdout.strip()
        error = None if is_clean else f"Uncommitted changes in {worktree_path.name}"
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=is_clean,
            error=error,
        )
    except (OSError, subprocess.SubprocessError) as e:
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=False,
            error=str(e),
        )


def x_check_worktree_status__mutmut_10(worktree_path: Path, wp_id: str, branch_name: str) -> WPStatus:
    """Check if a worktree has uncommitted changes.

    Args:
        worktree_path: Path to the worktree directory
        wp_id: Work package ID (e.g., "WP01")
        branch_name: Name of the branch

    Returns:
        WPStatus with is_clean=True if no uncommitted changes
    """
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        is_clean = not result.stdout.strip()
        error = None if is_clean else f"Uncommitted changes in {worktree_path.name}"
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=is_clean,
            error=error,
        )
    except (OSError, subprocess.SubprocessError) as e:
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=False,
            error=str(e),
        )


def x_check_worktree_status__mutmut_11(worktree_path: Path, wp_id: str, branch_name: str) -> WPStatus:
    """Check if a worktree has uncommitted changes.

    Args:
        worktree_path: Path to the worktree directory
        wp_id: Work package ID (e.g., "WP01")
        branch_name: Name of the branch

    Returns:
        WPStatus with is_clean=True if no uncommitted changes
    """
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=str(worktree_path),
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        is_clean = not result.stdout.strip()
        error = None if is_clean else f"Uncommitted changes in {worktree_path.name}"
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=is_clean,
            error=error,
        )
    except (OSError, subprocess.SubprocessError) as e:
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=False,
            error=str(e),
        )


def x_check_worktree_status__mutmut_12(worktree_path: Path, wp_id: str, branch_name: str) -> WPStatus:
    """Check if a worktree has uncommitted changes.

    Args:
        worktree_path: Path to the worktree directory
        wp_id: Work package ID (e.g., "WP01")
        branch_name: Name of the branch

    Returns:
        WPStatus with is_clean=True if no uncommitted changes
    """
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=str(worktree_path),
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        is_clean = not result.stdout.strip()
        error = None if is_clean else f"Uncommitted changes in {worktree_path.name}"
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=is_clean,
            error=error,
        )
    except (OSError, subprocess.SubprocessError) as e:
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=False,
            error=str(e),
        )


def x_check_worktree_status__mutmut_13(worktree_path: Path, wp_id: str, branch_name: str) -> WPStatus:
    """Check if a worktree has uncommitted changes.

    Args:
        worktree_path: Path to the worktree directory
        wp_id: Work package ID (e.g., "WP01")
        branch_name: Name of the branch

    Returns:
        WPStatus with is_clean=True if no uncommitted changes
    """
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=str(worktree_path),
            capture_output=True,
            text=True,
            errors="replace",
            check=False,
        )
        is_clean = not result.stdout.strip()
        error = None if is_clean else f"Uncommitted changes in {worktree_path.name}"
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=is_clean,
            error=error,
        )
    except (OSError, subprocess.SubprocessError) as e:
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=False,
            error=str(e),
        )


def x_check_worktree_status__mutmut_14(worktree_path: Path, wp_id: str, branch_name: str) -> WPStatus:
    """Check if a worktree has uncommitted changes.

    Args:
        worktree_path: Path to the worktree directory
        wp_id: Work package ID (e.g., "WP01")
        branch_name: Name of the branch

    Returns:
        WPStatus with is_clean=True if no uncommitted changes
    """
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=str(worktree_path),
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
        )
        is_clean = not result.stdout.strip()
        error = None if is_clean else f"Uncommitted changes in {worktree_path.name}"
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=is_clean,
            error=error,
        )
    except (OSError, subprocess.SubprocessError) as e:
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=False,
            error=str(e),
        )


def x_check_worktree_status__mutmut_15(worktree_path: Path, wp_id: str, branch_name: str) -> WPStatus:
    """Check if a worktree has uncommitted changes.

    Args:
        worktree_path: Path to the worktree directory
        wp_id: Work package ID (e.g., "WP01")
        branch_name: Name of the branch

    Returns:
        WPStatus with is_clean=True if no uncommitted changes
    """
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=str(worktree_path),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            )
        is_clean = not result.stdout.strip()
        error = None if is_clean else f"Uncommitted changes in {worktree_path.name}"
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=is_clean,
            error=error,
        )
    except (OSError, subprocess.SubprocessError) as e:
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=False,
            error=str(e),
        )


def x_check_worktree_status__mutmut_16(worktree_path: Path, wp_id: str, branch_name: str) -> WPStatus:
    """Check if a worktree has uncommitted changes.

    Args:
        worktree_path: Path to the worktree directory
        wp_id: Work package ID (e.g., "WP01")
        branch_name: Name of the branch

    Returns:
        WPStatus with is_clean=True if no uncommitted changes
    """
    try:
        result = subprocess.run(
            ["XXgitXX", "status", "--porcelain"],
            cwd=str(worktree_path),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        is_clean = not result.stdout.strip()
        error = None if is_clean else f"Uncommitted changes in {worktree_path.name}"
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=is_clean,
            error=error,
        )
    except (OSError, subprocess.SubprocessError) as e:
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=False,
            error=str(e),
        )


def x_check_worktree_status__mutmut_17(worktree_path: Path, wp_id: str, branch_name: str) -> WPStatus:
    """Check if a worktree has uncommitted changes.

    Args:
        worktree_path: Path to the worktree directory
        wp_id: Work package ID (e.g., "WP01")
        branch_name: Name of the branch

    Returns:
        WPStatus with is_clean=True if no uncommitted changes
    """
    try:
        result = subprocess.run(
            ["GIT", "status", "--porcelain"],
            cwd=str(worktree_path),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        is_clean = not result.stdout.strip()
        error = None if is_clean else f"Uncommitted changes in {worktree_path.name}"
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=is_clean,
            error=error,
        )
    except (OSError, subprocess.SubprocessError) as e:
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=False,
            error=str(e),
        )


def x_check_worktree_status__mutmut_18(worktree_path: Path, wp_id: str, branch_name: str) -> WPStatus:
    """Check if a worktree has uncommitted changes.

    Args:
        worktree_path: Path to the worktree directory
        wp_id: Work package ID (e.g., "WP01")
        branch_name: Name of the branch

    Returns:
        WPStatus with is_clean=True if no uncommitted changes
    """
    try:
        result = subprocess.run(
            ["git", "XXstatusXX", "--porcelain"],
            cwd=str(worktree_path),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        is_clean = not result.stdout.strip()
        error = None if is_clean else f"Uncommitted changes in {worktree_path.name}"
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=is_clean,
            error=error,
        )
    except (OSError, subprocess.SubprocessError) as e:
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=False,
            error=str(e),
        )


def x_check_worktree_status__mutmut_19(worktree_path: Path, wp_id: str, branch_name: str) -> WPStatus:
    """Check if a worktree has uncommitted changes.

    Args:
        worktree_path: Path to the worktree directory
        wp_id: Work package ID (e.g., "WP01")
        branch_name: Name of the branch

    Returns:
        WPStatus with is_clean=True if no uncommitted changes
    """
    try:
        result = subprocess.run(
            ["git", "STATUS", "--porcelain"],
            cwd=str(worktree_path),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        is_clean = not result.stdout.strip()
        error = None if is_clean else f"Uncommitted changes in {worktree_path.name}"
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=is_clean,
            error=error,
        )
    except (OSError, subprocess.SubprocessError) as e:
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=False,
            error=str(e),
        )


def x_check_worktree_status__mutmut_20(worktree_path: Path, wp_id: str, branch_name: str) -> WPStatus:
    """Check if a worktree has uncommitted changes.

    Args:
        worktree_path: Path to the worktree directory
        wp_id: Work package ID (e.g., "WP01")
        branch_name: Name of the branch

    Returns:
        WPStatus with is_clean=True if no uncommitted changes
    """
    try:
        result = subprocess.run(
            ["git", "status", "XX--porcelainXX"],
            cwd=str(worktree_path),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        is_clean = not result.stdout.strip()
        error = None if is_clean else f"Uncommitted changes in {worktree_path.name}"
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=is_clean,
            error=error,
        )
    except (OSError, subprocess.SubprocessError) as e:
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=False,
            error=str(e),
        )


def x_check_worktree_status__mutmut_21(worktree_path: Path, wp_id: str, branch_name: str) -> WPStatus:
    """Check if a worktree has uncommitted changes.

    Args:
        worktree_path: Path to the worktree directory
        wp_id: Work package ID (e.g., "WP01")
        branch_name: Name of the branch

    Returns:
        WPStatus with is_clean=True if no uncommitted changes
    """
    try:
        result = subprocess.run(
            ["git", "status", "--PORCELAIN"],
            cwd=str(worktree_path),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        is_clean = not result.stdout.strip()
        error = None if is_clean else f"Uncommitted changes in {worktree_path.name}"
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=is_clean,
            error=error,
        )
    except (OSError, subprocess.SubprocessError) as e:
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=False,
            error=str(e),
        )


def x_check_worktree_status__mutmut_22(worktree_path: Path, wp_id: str, branch_name: str) -> WPStatus:
    """Check if a worktree has uncommitted changes.

    Args:
        worktree_path: Path to the worktree directory
        wp_id: Work package ID (e.g., "WP01")
        branch_name: Name of the branch

    Returns:
        WPStatus with is_clean=True if no uncommitted changes
    """
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=str(None),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        is_clean = not result.stdout.strip()
        error = None if is_clean else f"Uncommitted changes in {worktree_path.name}"
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=is_clean,
            error=error,
        )
    except (OSError, subprocess.SubprocessError) as e:
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=False,
            error=str(e),
        )


def x_check_worktree_status__mutmut_23(worktree_path: Path, wp_id: str, branch_name: str) -> WPStatus:
    """Check if a worktree has uncommitted changes.

    Args:
        worktree_path: Path to the worktree directory
        wp_id: Work package ID (e.g., "WP01")
        branch_name: Name of the branch

    Returns:
        WPStatus with is_clean=True if no uncommitted changes
    """
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=str(worktree_path),
            capture_output=False,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        is_clean = not result.stdout.strip()
        error = None if is_clean else f"Uncommitted changes in {worktree_path.name}"
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=is_clean,
            error=error,
        )
    except (OSError, subprocess.SubprocessError) as e:
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=False,
            error=str(e),
        )


def x_check_worktree_status__mutmut_24(worktree_path: Path, wp_id: str, branch_name: str) -> WPStatus:
    """Check if a worktree has uncommitted changes.

    Args:
        worktree_path: Path to the worktree directory
        wp_id: Work package ID (e.g., "WP01")
        branch_name: Name of the branch

    Returns:
        WPStatus with is_clean=True if no uncommitted changes
    """
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=str(worktree_path),
            capture_output=True,
            text=False,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        is_clean = not result.stdout.strip()
        error = None if is_clean else f"Uncommitted changes in {worktree_path.name}"
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=is_clean,
            error=error,
        )
    except (OSError, subprocess.SubprocessError) as e:
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=False,
            error=str(e),
        )


def x_check_worktree_status__mutmut_25(worktree_path: Path, wp_id: str, branch_name: str) -> WPStatus:
    """Check if a worktree has uncommitted changes.

    Args:
        worktree_path: Path to the worktree directory
        wp_id: Work package ID (e.g., "WP01")
        branch_name: Name of the branch

    Returns:
        WPStatus with is_clean=True if no uncommitted changes
    """
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=str(worktree_path),
            capture_output=True,
            text=True,
            encoding="XXutf-8XX",
            errors="replace",
            check=False,
        )
        is_clean = not result.stdout.strip()
        error = None if is_clean else f"Uncommitted changes in {worktree_path.name}"
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=is_clean,
            error=error,
        )
    except (OSError, subprocess.SubprocessError) as e:
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=False,
            error=str(e),
        )


def x_check_worktree_status__mutmut_26(worktree_path: Path, wp_id: str, branch_name: str) -> WPStatus:
    """Check if a worktree has uncommitted changes.

    Args:
        worktree_path: Path to the worktree directory
        wp_id: Work package ID (e.g., "WP01")
        branch_name: Name of the branch

    Returns:
        WPStatus with is_clean=True if no uncommitted changes
    """
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=str(worktree_path),
            capture_output=True,
            text=True,
            encoding="UTF-8",
            errors="replace",
            check=False,
        )
        is_clean = not result.stdout.strip()
        error = None if is_clean else f"Uncommitted changes in {worktree_path.name}"
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=is_clean,
            error=error,
        )
    except (OSError, subprocess.SubprocessError) as e:
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=False,
            error=str(e),
        )


def x_check_worktree_status__mutmut_27(worktree_path: Path, wp_id: str, branch_name: str) -> WPStatus:
    """Check if a worktree has uncommitted changes.

    Args:
        worktree_path: Path to the worktree directory
        wp_id: Work package ID (e.g., "WP01")
        branch_name: Name of the branch

    Returns:
        WPStatus with is_clean=True if no uncommitted changes
    """
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=str(worktree_path),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="XXreplaceXX",
            check=False,
        )
        is_clean = not result.stdout.strip()
        error = None if is_clean else f"Uncommitted changes in {worktree_path.name}"
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=is_clean,
            error=error,
        )
    except (OSError, subprocess.SubprocessError) as e:
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=False,
            error=str(e),
        )


def x_check_worktree_status__mutmut_28(worktree_path: Path, wp_id: str, branch_name: str) -> WPStatus:
    """Check if a worktree has uncommitted changes.

    Args:
        worktree_path: Path to the worktree directory
        wp_id: Work package ID (e.g., "WP01")
        branch_name: Name of the branch

    Returns:
        WPStatus with is_clean=True if no uncommitted changes
    """
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=str(worktree_path),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="REPLACE",
            check=False,
        )
        is_clean = not result.stdout.strip()
        error = None if is_clean else f"Uncommitted changes in {worktree_path.name}"
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=is_clean,
            error=error,
        )
    except (OSError, subprocess.SubprocessError) as e:
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=False,
            error=str(e),
        )


def x_check_worktree_status__mutmut_29(worktree_path: Path, wp_id: str, branch_name: str) -> WPStatus:
    """Check if a worktree has uncommitted changes.

    Args:
        worktree_path: Path to the worktree directory
        wp_id: Work package ID (e.g., "WP01")
        branch_name: Name of the branch

    Returns:
        WPStatus with is_clean=True if no uncommitted changes
    """
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=str(worktree_path),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=True,
        )
        is_clean = not result.stdout.strip()
        error = None if is_clean else f"Uncommitted changes in {worktree_path.name}"
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=is_clean,
            error=error,
        )
    except (OSError, subprocess.SubprocessError) as e:
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=False,
            error=str(e),
        )


def x_check_worktree_status__mutmut_30(worktree_path: Path, wp_id: str, branch_name: str) -> WPStatus:
    """Check if a worktree has uncommitted changes.

    Args:
        worktree_path: Path to the worktree directory
        wp_id: Work package ID (e.g., "WP01")
        branch_name: Name of the branch

    Returns:
        WPStatus with is_clean=True if no uncommitted changes
    """
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=str(worktree_path),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        is_clean = None
        error = None if is_clean else f"Uncommitted changes in {worktree_path.name}"
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=is_clean,
            error=error,
        )
    except (OSError, subprocess.SubprocessError) as e:
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=False,
            error=str(e),
        )


def x_check_worktree_status__mutmut_31(worktree_path: Path, wp_id: str, branch_name: str) -> WPStatus:
    """Check if a worktree has uncommitted changes.

    Args:
        worktree_path: Path to the worktree directory
        wp_id: Work package ID (e.g., "WP01")
        branch_name: Name of the branch

    Returns:
        WPStatus with is_clean=True if no uncommitted changes
    """
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=str(worktree_path),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        is_clean = result.stdout.strip()
        error = None if is_clean else f"Uncommitted changes in {worktree_path.name}"
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=is_clean,
            error=error,
        )
    except (OSError, subprocess.SubprocessError) as e:
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=False,
            error=str(e),
        )


def x_check_worktree_status__mutmut_32(worktree_path: Path, wp_id: str, branch_name: str) -> WPStatus:
    """Check if a worktree has uncommitted changes.

    Args:
        worktree_path: Path to the worktree directory
        wp_id: Work package ID (e.g., "WP01")
        branch_name: Name of the branch

    Returns:
        WPStatus with is_clean=True if no uncommitted changes
    """
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=str(worktree_path),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        is_clean = not result.stdout.strip()
        error = None
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=is_clean,
            error=error,
        )
    except (OSError, subprocess.SubprocessError) as e:
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=False,
            error=str(e),
        )


def x_check_worktree_status__mutmut_33(worktree_path: Path, wp_id: str, branch_name: str) -> WPStatus:
    """Check if a worktree has uncommitted changes.

    Args:
        worktree_path: Path to the worktree directory
        wp_id: Work package ID (e.g., "WP01")
        branch_name: Name of the branch

    Returns:
        WPStatus with is_clean=True if no uncommitted changes
    """
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=str(worktree_path),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        is_clean = not result.stdout.strip()
        error = None if is_clean else f"Uncommitted changes in {worktree_path.name}"
        return WPStatus(
            wp_id=None,
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=is_clean,
            error=error,
        )
    except (OSError, subprocess.SubprocessError) as e:
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=False,
            error=str(e),
        )


def x_check_worktree_status__mutmut_34(worktree_path: Path, wp_id: str, branch_name: str) -> WPStatus:
    """Check if a worktree has uncommitted changes.

    Args:
        worktree_path: Path to the worktree directory
        wp_id: Work package ID (e.g., "WP01")
        branch_name: Name of the branch

    Returns:
        WPStatus with is_clean=True if no uncommitted changes
    """
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=str(worktree_path),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        is_clean = not result.stdout.strip()
        error = None if is_clean else f"Uncommitted changes in {worktree_path.name}"
        return WPStatus(
            wp_id=wp_id,
            worktree_path=None,
            branch_name=branch_name,
            is_clean=is_clean,
            error=error,
        )
    except (OSError, subprocess.SubprocessError) as e:
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=False,
            error=str(e),
        )


def x_check_worktree_status__mutmut_35(worktree_path: Path, wp_id: str, branch_name: str) -> WPStatus:
    """Check if a worktree has uncommitted changes.

    Args:
        worktree_path: Path to the worktree directory
        wp_id: Work package ID (e.g., "WP01")
        branch_name: Name of the branch

    Returns:
        WPStatus with is_clean=True if no uncommitted changes
    """
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=str(worktree_path),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        is_clean = not result.stdout.strip()
        error = None if is_clean else f"Uncommitted changes in {worktree_path.name}"
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=None,
            is_clean=is_clean,
            error=error,
        )
    except (OSError, subprocess.SubprocessError) as e:
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=False,
            error=str(e),
        )


def x_check_worktree_status__mutmut_36(worktree_path: Path, wp_id: str, branch_name: str) -> WPStatus:
    """Check if a worktree has uncommitted changes.

    Args:
        worktree_path: Path to the worktree directory
        wp_id: Work package ID (e.g., "WP01")
        branch_name: Name of the branch

    Returns:
        WPStatus with is_clean=True if no uncommitted changes
    """
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=str(worktree_path),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        is_clean = not result.stdout.strip()
        error = None if is_clean else f"Uncommitted changes in {worktree_path.name}"
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=None,
            error=error,
        )
    except (OSError, subprocess.SubprocessError) as e:
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=False,
            error=str(e),
        )


def x_check_worktree_status__mutmut_37(worktree_path: Path, wp_id: str, branch_name: str) -> WPStatus:
    """Check if a worktree has uncommitted changes.

    Args:
        worktree_path: Path to the worktree directory
        wp_id: Work package ID (e.g., "WP01")
        branch_name: Name of the branch

    Returns:
        WPStatus with is_clean=True if no uncommitted changes
    """
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=str(worktree_path),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        is_clean = not result.stdout.strip()
        error = None if is_clean else f"Uncommitted changes in {worktree_path.name}"
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=is_clean,
            error=None,
        )
    except (OSError, subprocess.SubprocessError) as e:
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=False,
            error=str(e),
        )


def x_check_worktree_status__mutmut_38(worktree_path: Path, wp_id: str, branch_name: str) -> WPStatus:
    """Check if a worktree has uncommitted changes.

    Args:
        worktree_path: Path to the worktree directory
        wp_id: Work package ID (e.g., "WP01")
        branch_name: Name of the branch

    Returns:
        WPStatus with is_clean=True if no uncommitted changes
    """
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=str(worktree_path),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        is_clean = not result.stdout.strip()
        error = None if is_clean else f"Uncommitted changes in {worktree_path.name}"
        return WPStatus(
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=is_clean,
            error=error,
        )
    except (OSError, subprocess.SubprocessError) as e:
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=False,
            error=str(e),
        )


def x_check_worktree_status__mutmut_39(worktree_path: Path, wp_id: str, branch_name: str) -> WPStatus:
    """Check if a worktree has uncommitted changes.

    Args:
        worktree_path: Path to the worktree directory
        wp_id: Work package ID (e.g., "WP01")
        branch_name: Name of the branch

    Returns:
        WPStatus with is_clean=True if no uncommitted changes
    """
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=str(worktree_path),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        is_clean = not result.stdout.strip()
        error = None if is_clean else f"Uncommitted changes in {worktree_path.name}"
        return WPStatus(
            wp_id=wp_id,
            branch_name=branch_name,
            is_clean=is_clean,
            error=error,
        )
    except (OSError, subprocess.SubprocessError) as e:
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=False,
            error=str(e),
        )


def x_check_worktree_status__mutmut_40(worktree_path: Path, wp_id: str, branch_name: str) -> WPStatus:
    """Check if a worktree has uncommitted changes.

    Args:
        worktree_path: Path to the worktree directory
        wp_id: Work package ID (e.g., "WP01")
        branch_name: Name of the branch

    Returns:
        WPStatus with is_clean=True if no uncommitted changes
    """
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=str(worktree_path),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        is_clean = not result.stdout.strip()
        error = None if is_clean else f"Uncommitted changes in {worktree_path.name}"
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            is_clean=is_clean,
            error=error,
        )
    except (OSError, subprocess.SubprocessError) as e:
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=False,
            error=str(e),
        )


def x_check_worktree_status__mutmut_41(worktree_path: Path, wp_id: str, branch_name: str) -> WPStatus:
    """Check if a worktree has uncommitted changes.

    Args:
        worktree_path: Path to the worktree directory
        wp_id: Work package ID (e.g., "WP01")
        branch_name: Name of the branch

    Returns:
        WPStatus with is_clean=True if no uncommitted changes
    """
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=str(worktree_path),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        is_clean = not result.stdout.strip()
        error = None if is_clean else f"Uncommitted changes in {worktree_path.name}"
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=branch_name,
            error=error,
        )
    except (OSError, subprocess.SubprocessError) as e:
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=False,
            error=str(e),
        )


def x_check_worktree_status__mutmut_42(worktree_path: Path, wp_id: str, branch_name: str) -> WPStatus:
    """Check if a worktree has uncommitted changes.

    Args:
        worktree_path: Path to the worktree directory
        wp_id: Work package ID (e.g., "WP01")
        branch_name: Name of the branch

    Returns:
        WPStatus with is_clean=True if no uncommitted changes
    """
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=str(worktree_path),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        is_clean = not result.stdout.strip()
        error = None if is_clean else f"Uncommitted changes in {worktree_path.name}"
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=is_clean,
            )
    except (OSError, subprocess.SubprocessError) as e:
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=False,
            error=str(e),
        )


def x_check_worktree_status__mutmut_43(worktree_path: Path, wp_id: str, branch_name: str) -> WPStatus:
    """Check if a worktree has uncommitted changes.

    Args:
        worktree_path: Path to the worktree directory
        wp_id: Work package ID (e.g., "WP01")
        branch_name: Name of the branch

    Returns:
        WPStatus with is_clean=True if no uncommitted changes
    """
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=str(worktree_path),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        is_clean = not result.stdout.strip()
        error = None if is_clean else f"Uncommitted changes in {worktree_path.name}"
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=is_clean,
            error=error,
        )
    except (OSError, subprocess.SubprocessError) as e:
        return WPStatus(
            wp_id=None,
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=False,
            error=str(e),
        )


def x_check_worktree_status__mutmut_44(worktree_path: Path, wp_id: str, branch_name: str) -> WPStatus:
    """Check if a worktree has uncommitted changes.

    Args:
        worktree_path: Path to the worktree directory
        wp_id: Work package ID (e.g., "WP01")
        branch_name: Name of the branch

    Returns:
        WPStatus with is_clean=True if no uncommitted changes
    """
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=str(worktree_path),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        is_clean = not result.stdout.strip()
        error = None if is_clean else f"Uncommitted changes in {worktree_path.name}"
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=is_clean,
            error=error,
        )
    except (OSError, subprocess.SubprocessError) as e:
        return WPStatus(
            wp_id=wp_id,
            worktree_path=None,
            branch_name=branch_name,
            is_clean=False,
            error=str(e),
        )


def x_check_worktree_status__mutmut_45(worktree_path: Path, wp_id: str, branch_name: str) -> WPStatus:
    """Check if a worktree has uncommitted changes.

    Args:
        worktree_path: Path to the worktree directory
        wp_id: Work package ID (e.g., "WP01")
        branch_name: Name of the branch

    Returns:
        WPStatus with is_clean=True if no uncommitted changes
    """
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=str(worktree_path),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        is_clean = not result.stdout.strip()
        error = None if is_clean else f"Uncommitted changes in {worktree_path.name}"
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=is_clean,
            error=error,
        )
    except (OSError, subprocess.SubprocessError) as e:
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=None,
            is_clean=False,
            error=str(e),
        )


def x_check_worktree_status__mutmut_46(worktree_path: Path, wp_id: str, branch_name: str) -> WPStatus:
    """Check if a worktree has uncommitted changes.

    Args:
        worktree_path: Path to the worktree directory
        wp_id: Work package ID (e.g., "WP01")
        branch_name: Name of the branch

    Returns:
        WPStatus with is_clean=True if no uncommitted changes
    """
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=str(worktree_path),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        is_clean = not result.stdout.strip()
        error = None if is_clean else f"Uncommitted changes in {worktree_path.name}"
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=is_clean,
            error=error,
        )
    except (OSError, subprocess.SubprocessError) as e:
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=None,
            error=str(e),
        )


def x_check_worktree_status__mutmut_47(worktree_path: Path, wp_id: str, branch_name: str) -> WPStatus:
    """Check if a worktree has uncommitted changes.

    Args:
        worktree_path: Path to the worktree directory
        wp_id: Work package ID (e.g., "WP01")
        branch_name: Name of the branch

    Returns:
        WPStatus with is_clean=True if no uncommitted changes
    """
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=str(worktree_path),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        is_clean = not result.stdout.strip()
        error = None if is_clean else f"Uncommitted changes in {worktree_path.name}"
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=is_clean,
            error=error,
        )
    except (OSError, subprocess.SubprocessError) as e:
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=False,
            error=None,
        )


def x_check_worktree_status__mutmut_48(worktree_path: Path, wp_id: str, branch_name: str) -> WPStatus:
    """Check if a worktree has uncommitted changes.

    Args:
        worktree_path: Path to the worktree directory
        wp_id: Work package ID (e.g., "WP01")
        branch_name: Name of the branch

    Returns:
        WPStatus with is_clean=True if no uncommitted changes
    """
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=str(worktree_path),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        is_clean = not result.stdout.strip()
        error = None if is_clean else f"Uncommitted changes in {worktree_path.name}"
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=is_clean,
            error=error,
        )
    except (OSError, subprocess.SubprocessError) as e:
        return WPStatus(
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=False,
            error=str(e),
        )


def x_check_worktree_status__mutmut_49(worktree_path: Path, wp_id: str, branch_name: str) -> WPStatus:
    """Check if a worktree has uncommitted changes.

    Args:
        worktree_path: Path to the worktree directory
        wp_id: Work package ID (e.g., "WP01")
        branch_name: Name of the branch

    Returns:
        WPStatus with is_clean=True if no uncommitted changes
    """
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=str(worktree_path),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        is_clean = not result.stdout.strip()
        error = None if is_clean else f"Uncommitted changes in {worktree_path.name}"
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=is_clean,
            error=error,
        )
    except (OSError, subprocess.SubprocessError) as e:
        return WPStatus(
            wp_id=wp_id,
            branch_name=branch_name,
            is_clean=False,
            error=str(e),
        )


def x_check_worktree_status__mutmut_50(worktree_path: Path, wp_id: str, branch_name: str) -> WPStatus:
    """Check if a worktree has uncommitted changes.

    Args:
        worktree_path: Path to the worktree directory
        wp_id: Work package ID (e.g., "WP01")
        branch_name: Name of the branch

    Returns:
        WPStatus with is_clean=True if no uncommitted changes
    """
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=str(worktree_path),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        is_clean = not result.stdout.strip()
        error = None if is_clean else f"Uncommitted changes in {worktree_path.name}"
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=is_clean,
            error=error,
        )
    except (OSError, subprocess.SubprocessError) as e:
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            is_clean=False,
            error=str(e),
        )


def x_check_worktree_status__mutmut_51(worktree_path: Path, wp_id: str, branch_name: str) -> WPStatus:
    """Check if a worktree has uncommitted changes.

    Args:
        worktree_path: Path to the worktree directory
        wp_id: Work package ID (e.g., "WP01")
        branch_name: Name of the branch

    Returns:
        WPStatus with is_clean=True if no uncommitted changes
    """
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=str(worktree_path),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        is_clean = not result.stdout.strip()
        error = None if is_clean else f"Uncommitted changes in {worktree_path.name}"
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=is_clean,
            error=error,
        )
    except (OSError, subprocess.SubprocessError) as e:
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=branch_name,
            error=str(e),
        )


def x_check_worktree_status__mutmut_52(worktree_path: Path, wp_id: str, branch_name: str) -> WPStatus:
    """Check if a worktree has uncommitted changes.

    Args:
        worktree_path: Path to the worktree directory
        wp_id: Work package ID (e.g., "WP01")
        branch_name: Name of the branch

    Returns:
        WPStatus with is_clean=True if no uncommitted changes
    """
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=str(worktree_path),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        is_clean = not result.stdout.strip()
        error = None if is_clean else f"Uncommitted changes in {worktree_path.name}"
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=is_clean,
            error=error,
        )
    except (OSError, subprocess.SubprocessError) as e:
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=False,
            )


def x_check_worktree_status__mutmut_53(worktree_path: Path, wp_id: str, branch_name: str) -> WPStatus:
    """Check if a worktree has uncommitted changes.

    Args:
        worktree_path: Path to the worktree directory
        wp_id: Work package ID (e.g., "WP01")
        branch_name: Name of the branch

    Returns:
        WPStatus with is_clean=True if no uncommitted changes
    """
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=str(worktree_path),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        is_clean = not result.stdout.strip()
        error = None if is_clean else f"Uncommitted changes in {worktree_path.name}"
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=is_clean,
            error=error,
        )
    except (OSError, subprocess.SubprocessError) as e:
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=True,
            error=str(e),
        )


def x_check_worktree_status__mutmut_54(worktree_path: Path, wp_id: str, branch_name: str) -> WPStatus:
    """Check if a worktree has uncommitted changes.

    Args:
        worktree_path: Path to the worktree directory
        wp_id: Work package ID (e.g., "WP01")
        branch_name: Name of the branch

    Returns:
        WPStatus with is_clean=True if no uncommitted changes
    """
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=str(worktree_path),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        is_clean = not result.stdout.strip()
        error = None if is_clean else f"Uncommitted changes in {worktree_path.name}"
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=is_clean,
            error=error,
        )
    except (OSError, subprocess.SubprocessError) as e:
        return WPStatus(
            wp_id=wp_id,
            worktree_path=worktree_path,
            branch_name=branch_name,
            is_clean=False,
            error=str(None),
        )

x_check_worktree_status__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_check_worktree_status__mutmut_1': x_check_worktree_status__mutmut_1, 
    'x_check_worktree_status__mutmut_2': x_check_worktree_status__mutmut_2, 
    'x_check_worktree_status__mutmut_3': x_check_worktree_status__mutmut_3, 
    'x_check_worktree_status__mutmut_4': x_check_worktree_status__mutmut_4, 
    'x_check_worktree_status__mutmut_5': x_check_worktree_status__mutmut_5, 
    'x_check_worktree_status__mutmut_6': x_check_worktree_status__mutmut_6, 
    'x_check_worktree_status__mutmut_7': x_check_worktree_status__mutmut_7, 
    'x_check_worktree_status__mutmut_8': x_check_worktree_status__mutmut_8, 
    'x_check_worktree_status__mutmut_9': x_check_worktree_status__mutmut_9, 
    'x_check_worktree_status__mutmut_10': x_check_worktree_status__mutmut_10, 
    'x_check_worktree_status__mutmut_11': x_check_worktree_status__mutmut_11, 
    'x_check_worktree_status__mutmut_12': x_check_worktree_status__mutmut_12, 
    'x_check_worktree_status__mutmut_13': x_check_worktree_status__mutmut_13, 
    'x_check_worktree_status__mutmut_14': x_check_worktree_status__mutmut_14, 
    'x_check_worktree_status__mutmut_15': x_check_worktree_status__mutmut_15, 
    'x_check_worktree_status__mutmut_16': x_check_worktree_status__mutmut_16, 
    'x_check_worktree_status__mutmut_17': x_check_worktree_status__mutmut_17, 
    'x_check_worktree_status__mutmut_18': x_check_worktree_status__mutmut_18, 
    'x_check_worktree_status__mutmut_19': x_check_worktree_status__mutmut_19, 
    'x_check_worktree_status__mutmut_20': x_check_worktree_status__mutmut_20, 
    'x_check_worktree_status__mutmut_21': x_check_worktree_status__mutmut_21, 
    'x_check_worktree_status__mutmut_22': x_check_worktree_status__mutmut_22, 
    'x_check_worktree_status__mutmut_23': x_check_worktree_status__mutmut_23, 
    'x_check_worktree_status__mutmut_24': x_check_worktree_status__mutmut_24, 
    'x_check_worktree_status__mutmut_25': x_check_worktree_status__mutmut_25, 
    'x_check_worktree_status__mutmut_26': x_check_worktree_status__mutmut_26, 
    'x_check_worktree_status__mutmut_27': x_check_worktree_status__mutmut_27, 
    'x_check_worktree_status__mutmut_28': x_check_worktree_status__mutmut_28, 
    'x_check_worktree_status__mutmut_29': x_check_worktree_status__mutmut_29, 
    'x_check_worktree_status__mutmut_30': x_check_worktree_status__mutmut_30, 
    'x_check_worktree_status__mutmut_31': x_check_worktree_status__mutmut_31, 
    'x_check_worktree_status__mutmut_32': x_check_worktree_status__mutmut_32, 
    'x_check_worktree_status__mutmut_33': x_check_worktree_status__mutmut_33, 
    'x_check_worktree_status__mutmut_34': x_check_worktree_status__mutmut_34, 
    'x_check_worktree_status__mutmut_35': x_check_worktree_status__mutmut_35, 
    'x_check_worktree_status__mutmut_36': x_check_worktree_status__mutmut_36, 
    'x_check_worktree_status__mutmut_37': x_check_worktree_status__mutmut_37, 
    'x_check_worktree_status__mutmut_38': x_check_worktree_status__mutmut_38, 
    'x_check_worktree_status__mutmut_39': x_check_worktree_status__mutmut_39, 
    'x_check_worktree_status__mutmut_40': x_check_worktree_status__mutmut_40, 
    'x_check_worktree_status__mutmut_41': x_check_worktree_status__mutmut_41, 
    'x_check_worktree_status__mutmut_42': x_check_worktree_status__mutmut_42, 
    'x_check_worktree_status__mutmut_43': x_check_worktree_status__mutmut_43, 
    'x_check_worktree_status__mutmut_44': x_check_worktree_status__mutmut_44, 
    'x_check_worktree_status__mutmut_45': x_check_worktree_status__mutmut_45, 
    'x_check_worktree_status__mutmut_46': x_check_worktree_status__mutmut_46, 
    'x_check_worktree_status__mutmut_47': x_check_worktree_status__mutmut_47, 
    'x_check_worktree_status__mutmut_48': x_check_worktree_status__mutmut_48, 
    'x_check_worktree_status__mutmut_49': x_check_worktree_status__mutmut_49, 
    'x_check_worktree_status__mutmut_50': x_check_worktree_status__mutmut_50, 
    'x_check_worktree_status__mutmut_51': x_check_worktree_status__mutmut_51, 
    'x_check_worktree_status__mutmut_52': x_check_worktree_status__mutmut_52, 
    'x_check_worktree_status__mutmut_53': x_check_worktree_status__mutmut_53, 
    'x_check_worktree_status__mutmut_54': x_check_worktree_status__mutmut_54
}
x_check_worktree_status__mutmut_orig.__name__ = 'x_check_worktree_status'


def check_target_divergence(target_branch: str, repo_root: Path) -> tuple[bool, str | None]:
    args = [target_branch, repo_root]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_check_target_divergence__mutmut_orig, x_check_target_divergence__mutmut_mutants, args, kwargs, None)


def x_check_target_divergence__mutmut_orig(target_branch: str, repo_root: Path) -> tuple[bool, str | None]:
    """Check if target branch has diverged from origin.

    Args:
        target_branch: Name of the target branch (e.g., "main")
        repo_root: Path to the repository root

    Returns:
        Tuple of (has_diverged, remediation_message)
        - has_diverged: True if local branch is behind origin
        - remediation_message: Instructions for fixing divergence
    """
    try:
        # Fetch latest refs (optional, may fail if offline)
        subprocess.run(
            ["git", "fetch", "origin", target_branch],
            cwd=str(repo_root),
            capture_output=True,
            check=False,
        )

        # Count commits ahead/behind
        result = subprocess.run(
            ["git", "rev-list", "--left-right", "--count", f"{target_branch}...origin/{target_branch}"],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )

        if result.returncode != 0:
            return False, None  # No remote tracking, assume OK

        parts = result.stdout.strip().split()
        if len(parts) != 2:
            return False, None  # Unexpected output, assume OK

        ahead, behind = map(int, parts)

        if behind > 0:
            return True, f"{target_branch} is {behind} commit(s) behind origin. Run: git checkout {target_branch} && git pull"

        return False, None

    except (OSError, subprocess.SubprocessError, ValueError) as exc:
        logger.warning(
            "Target divergence check failed for %s: %s",
            target_branch,
            exc,
        )
        return False, None  # Non-fatal: preserve merge UX if remote checks fail


def x_check_target_divergence__mutmut_1(target_branch: str, repo_root: Path) -> tuple[bool, str | None]:
    """Check if target branch has diverged from origin.

    Args:
        target_branch: Name of the target branch (e.g., "main")
        repo_root: Path to the repository root

    Returns:
        Tuple of (has_diverged, remediation_message)
        - has_diverged: True if local branch is behind origin
        - remediation_message: Instructions for fixing divergence
    """
    try:
        # Fetch latest refs (optional, may fail if offline)
        subprocess.run(
            None,
            cwd=str(repo_root),
            capture_output=True,
            check=False,
        )

        # Count commits ahead/behind
        result = subprocess.run(
            ["git", "rev-list", "--left-right", "--count", f"{target_branch}...origin/{target_branch}"],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )

        if result.returncode != 0:
            return False, None  # No remote tracking, assume OK

        parts = result.stdout.strip().split()
        if len(parts) != 2:
            return False, None  # Unexpected output, assume OK

        ahead, behind = map(int, parts)

        if behind > 0:
            return True, f"{target_branch} is {behind} commit(s) behind origin. Run: git checkout {target_branch} && git pull"

        return False, None

    except (OSError, subprocess.SubprocessError, ValueError) as exc:
        logger.warning(
            "Target divergence check failed for %s: %s",
            target_branch,
            exc,
        )
        return False, None  # Non-fatal: preserve merge UX if remote checks fail


def x_check_target_divergence__mutmut_2(target_branch: str, repo_root: Path) -> tuple[bool, str | None]:
    """Check if target branch has diverged from origin.

    Args:
        target_branch: Name of the target branch (e.g., "main")
        repo_root: Path to the repository root

    Returns:
        Tuple of (has_diverged, remediation_message)
        - has_diverged: True if local branch is behind origin
        - remediation_message: Instructions for fixing divergence
    """
    try:
        # Fetch latest refs (optional, may fail if offline)
        subprocess.run(
            ["git", "fetch", "origin", target_branch],
            cwd=None,
            capture_output=True,
            check=False,
        )

        # Count commits ahead/behind
        result = subprocess.run(
            ["git", "rev-list", "--left-right", "--count", f"{target_branch}...origin/{target_branch}"],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )

        if result.returncode != 0:
            return False, None  # No remote tracking, assume OK

        parts = result.stdout.strip().split()
        if len(parts) != 2:
            return False, None  # Unexpected output, assume OK

        ahead, behind = map(int, parts)

        if behind > 0:
            return True, f"{target_branch} is {behind} commit(s) behind origin. Run: git checkout {target_branch} && git pull"

        return False, None

    except (OSError, subprocess.SubprocessError, ValueError) as exc:
        logger.warning(
            "Target divergence check failed for %s: %s",
            target_branch,
            exc,
        )
        return False, None  # Non-fatal: preserve merge UX if remote checks fail


def x_check_target_divergence__mutmut_3(target_branch: str, repo_root: Path) -> tuple[bool, str | None]:
    """Check if target branch has diverged from origin.

    Args:
        target_branch: Name of the target branch (e.g., "main")
        repo_root: Path to the repository root

    Returns:
        Tuple of (has_diverged, remediation_message)
        - has_diverged: True if local branch is behind origin
        - remediation_message: Instructions for fixing divergence
    """
    try:
        # Fetch latest refs (optional, may fail if offline)
        subprocess.run(
            ["git", "fetch", "origin", target_branch],
            cwd=str(repo_root),
            capture_output=None,
            check=False,
        )

        # Count commits ahead/behind
        result = subprocess.run(
            ["git", "rev-list", "--left-right", "--count", f"{target_branch}...origin/{target_branch}"],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )

        if result.returncode != 0:
            return False, None  # No remote tracking, assume OK

        parts = result.stdout.strip().split()
        if len(parts) != 2:
            return False, None  # Unexpected output, assume OK

        ahead, behind = map(int, parts)

        if behind > 0:
            return True, f"{target_branch} is {behind} commit(s) behind origin. Run: git checkout {target_branch} && git pull"

        return False, None

    except (OSError, subprocess.SubprocessError, ValueError) as exc:
        logger.warning(
            "Target divergence check failed for %s: %s",
            target_branch,
            exc,
        )
        return False, None  # Non-fatal: preserve merge UX if remote checks fail


def x_check_target_divergence__mutmut_4(target_branch: str, repo_root: Path) -> tuple[bool, str | None]:
    """Check if target branch has diverged from origin.

    Args:
        target_branch: Name of the target branch (e.g., "main")
        repo_root: Path to the repository root

    Returns:
        Tuple of (has_diverged, remediation_message)
        - has_diverged: True if local branch is behind origin
        - remediation_message: Instructions for fixing divergence
    """
    try:
        # Fetch latest refs (optional, may fail if offline)
        subprocess.run(
            ["git", "fetch", "origin", target_branch],
            cwd=str(repo_root),
            capture_output=True,
            check=None,
        )

        # Count commits ahead/behind
        result = subprocess.run(
            ["git", "rev-list", "--left-right", "--count", f"{target_branch}...origin/{target_branch}"],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )

        if result.returncode != 0:
            return False, None  # No remote tracking, assume OK

        parts = result.stdout.strip().split()
        if len(parts) != 2:
            return False, None  # Unexpected output, assume OK

        ahead, behind = map(int, parts)

        if behind > 0:
            return True, f"{target_branch} is {behind} commit(s) behind origin. Run: git checkout {target_branch} && git pull"

        return False, None

    except (OSError, subprocess.SubprocessError, ValueError) as exc:
        logger.warning(
            "Target divergence check failed for %s: %s",
            target_branch,
            exc,
        )
        return False, None  # Non-fatal: preserve merge UX if remote checks fail


def x_check_target_divergence__mutmut_5(target_branch: str, repo_root: Path) -> tuple[bool, str | None]:
    """Check if target branch has diverged from origin.

    Args:
        target_branch: Name of the target branch (e.g., "main")
        repo_root: Path to the repository root

    Returns:
        Tuple of (has_diverged, remediation_message)
        - has_diverged: True if local branch is behind origin
        - remediation_message: Instructions for fixing divergence
    """
    try:
        # Fetch latest refs (optional, may fail if offline)
        subprocess.run(
            cwd=str(repo_root),
            capture_output=True,
            check=False,
        )

        # Count commits ahead/behind
        result = subprocess.run(
            ["git", "rev-list", "--left-right", "--count", f"{target_branch}...origin/{target_branch}"],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )

        if result.returncode != 0:
            return False, None  # No remote tracking, assume OK

        parts = result.stdout.strip().split()
        if len(parts) != 2:
            return False, None  # Unexpected output, assume OK

        ahead, behind = map(int, parts)

        if behind > 0:
            return True, f"{target_branch} is {behind} commit(s) behind origin. Run: git checkout {target_branch} && git pull"

        return False, None

    except (OSError, subprocess.SubprocessError, ValueError) as exc:
        logger.warning(
            "Target divergence check failed for %s: %s",
            target_branch,
            exc,
        )
        return False, None  # Non-fatal: preserve merge UX if remote checks fail


def x_check_target_divergence__mutmut_6(target_branch: str, repo_root: Path) -> tuple[bool, str | None]:
    """Check if target branch has diverged from origin.

    Args:
        target_branch: Name of the target branch (e.g., "main")
        repo_root: Path to the repository root

    Returns:
        Tuple of (has_diverged, remediation_message)
        - has_diverged: True if local branch is behind origin
        - remediation_message: Instructions for fixing divergence
    """
    try:
        # Fetch latest refs (optional, may fail if offline)
        subprocess.run(
            ["git", "fetch", "origin", target_branch],
            capture_output=True,
            check=False,
        )

        # Count commits ahead/behind
        result = subprocess.run(
            ["git", "rev-list", "--left-right", "--count", f"{target_branch}...origin/{target_branch}"],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )

        if result.returncode != 0:
            return False, None  # No remote tracking, assume OK

        parts = result.stdout.strip().split()
        if len(parts) != 2:
            return False, None  # Unexpected output, assume OK

        ahead, behind = map(int, parts)

        if behind > 0:
            return True, f"{target_branch} is {behind} commit(s) behind origin. Run: git checkout {target_branch} && git pull"

        return False, None

    except (OSError, subprocess.SubprocessError, ValueError) as exc:
        logger.warning(
            "Target divergence check failed for %s: %s",
            target_branch,
            exc,
        )
        return False, None  # Non-fatal: preserve merge UX if remote checks fail


def x_check_target_divergence__mutmut_7(target_branch: str, repo_root: Path) -> tuple[bool, str | None]:
    """Check if target branch has diverged from origin.

    Args:
        target_branch: Name of the target branch (e.g., "main")
        repo_root: Path to the repository root

    Returns:
        Tuple of (has_diverged, remediation_message)
        - has_diverged: True if local branch is behind origin
        - remediation_message: Instructions for fixing divergence
    """
    try:
        # Fetch latest refs (optional, may fail if offline)
        subprocess.run(
            ["git", "fetch", "origin", target_branch],
            cwd=str(repo_root),
            check=False,
        )

        # Count commits ahead/behind
        result = subprocess.run(
            ["git", "rev-list", "--left-right", "--count", f"{target_branch}...origin/{target_branch}"],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )

        if result.returncode != 0:
            return False, None  # No remote tracking, assume OK

        parts = result.stdout.strip().split()
        if len(parts) != 2:
            return False, None  # Unexpected output, assume OK

        ahead, behind = map(int, parts)

        if behind > 0:
            return True, f"{target_branch} is {behind} commit(s) behind origin. Run: git checkout {target_branch} && git pull"

        return False, None

    except (OSError, subprocess.SubprocessError, ValueError) as exc:
        logger.warning(
            "Target divergence check failed for %s: %s",
            target_branch,
            exc,
        )
        return False, None  # Non-fatal: preserve merge UX if remote checks fail


def x_check_target_divergence__mutmut_8(target_branch: str, repo_root: Path) -> tuple[bool, str | None]:
    """Check if target branch has diverged from origin.

    Args:
        target_branch: Name of the target branch (e.g., "main")
        repo_root: Path to the repository root

    Returns:
        Tuple of (has_diverged, remediation_message)
        - has_diverged: True if local branch is behind origin
        - remediation_message: Instructions for fixing divergence
    """
    try:
        # Fetch latest refs (optional, may fail if offline)
        subprocess.run(
            ["git", "fetch", "origin", target_branch],
            cwd=str(repo_root),
            capture_output=True,
            )

        # Count commits ahead/behind
        result = subprocess.run(
            ["git", "rev-list", "--left-right", "--count", f"{target_branch}...origin/{target_branch}"],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )

        if result.returncode != 0:
            return False, None  # No remote tracking, assume OK

        parts = result.stdout.strip().split()
        if len(parts) != 2:
            return False, None  # Unexpected output, assume OK

        ahead, behind = map(int, parts)

        if behind > 0:
            return True, f"{target_branch} is {behind} commit(s) behind origin. Run: git checkout {target_branch} && git pull"

        return False, None

    except (OSError, subprocess.SubprocessError, ValueError) as exc:
        logger.warning(
            "Target divergence check failed for %s: %s",
            target_branch,
            exc,
        )
        return False, None  # Non-fatal: preserve merge UX if remote checks fail


def x_check_target_divergence__mutmut_9(target_branch: str, repo_root: Path) -> tuple[bool, str | None]:
    """Check if target branch has diverged from origin.

    Args:
        target_branch: Name of the target branch (e.g., "main")
        repo_root: Path to the repository root

    Returns:
        Tuple of (has_diverged, remediation_message)
        - has_diverged: True if local branch is behind origin
        - remediation_message: Instructions for fixing divergence
    """
    try:
        # Fetch latest refs (optional, may fail if offline)
        subprocess.run(
            ["XXgitXX", "fetch", "origin", target_branch],
            cwd=str(repo_root),
            capture_output=True,
            check=False,
        )

        # Count commits ahead/behind
        result = subprocess.run(
            ["git", "rev-list", "--left-right", "--count", f"{target_branch}...origin/{target_branch}"],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )

        if result.returncode != 0:
            return False, None  # No remote tracking, assume OK

        parts = result.stdout.strip().split()
        if len(parts) != 2:
            return False, None  # Unexpected output, assume OK

        ahead, behind = map(int, parts)

        if behind > 0:
            return True, f"{target_branch} is {behind} commit(s) behind origin. Run: git checkout {target_branch} && git pull"

        return False, None

    except (OSError, subprocess.SubprocessError, ValueError) as exc:
        logger.warning(
            "Target divergence check failed for %s: %s",
            target_branch,
            exc,
        )
        return False, None  # Non-fatal: preserve merge UX if remote checks fail


def x_check_target_divergence__mutmut_10(target_branch: str, repo_root: Path) -> tuple[bool, str | None]:
    """Check if target branch has diverged from origin.

    Args:
        target_branch: Name of the target branch (e.g., "main")
        repo_root: Path to the repository root

    Returns:
        Tuple of (has_diverged, remediation_message)
        - has_diverged: True if local branch is behind origin
        - remediation_message: Instructions for fixing divergence
    """
    try:
        # Fetch latest refs (optional, may fail if offline)
        subprocess.run(
            ["GIT", "fetch", "origin", target_branch],
            cwd=str(repo_root),
            capture_output=True,
            check=False,
        )

        # Count commits ahead/behind
        result = subprocess.run(
            ["git", "rev-list", "--left-right", "--count", f"{target_branch}...origin/{target_branch}"],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )

        if result.returncode != 0:
            return False, None  # No remote tracking, assume OK

        parts = result.stdout.strip().split()
        if len(parts) != 2:
            return False, None  # Unexpected output, assume OK

        ahead, behind = map(int, parts)

        if behind > 0:
            return True, f"{target_branch} is {behind} commit(s) behind origin. Run: git checkout {target_branch} && git pull"

        return False, None

    except (OSError, subprocess.SubprocessError, ValueError) as exc:
        logger.warning(
            "Target divergence check failed for %s: %s",
            target_branch,
            exc,
        )
        return False, None  # Non-fatal: preserve merge UX if remote checks fail


def x_check_target_divergence__mutmut_11(target_branch: str, repo_root: Path) -> tuple[bool, str | None]:
    """Check if target branch has diverged from origin.

    Args:
        target_branch: Name of the target branch (e.g., "main")
        repo_root: Path to the repository root

    Returns:
        Tuple of (has_diverged, remediation_message)
        - has_diverged: True if local branch is behind origin
        - remediation_message: Instructions for fixing divergence
    """
    try:
        # Fetch latest refs (optional, may fail if offline)
        subprocess.run(
            ["git", "XXfetchXX", "origin", target_branch],
            cwd=str(repo_root),
            capture_output=True,
            check=False,
        )

        # Count commits ahead/behind
        result = subprocess.run(
            ["git", "rev-list", "--left-right", "--count", f"{target_branch}...origin/{target_branch}"],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )

        if result.returncode != 0:
            return False, None  # No remote tracking, assume OK

        parts = result.stdout.strip().split()
        if len(parts) != 2:
            return False, None  # Unexpected output, assume OK

        ahead, behind = map(int, parts)

        if behind > 0:
            return True, f"{target_branch} is {behind} commit(s) behind origin. Run: git checkout {target_branch} && git pull"

        return False, None

    except (OSError, subprocess.SubprocessError, ValueError) as exc:
        logger.warning(
            "Target divergence check failed for %s: %s",
            target_branch,
            exc,
        )
        return False, None  # Non-fatal: preserve merge UX if remote checks fail


def x_check_target_divergence__mutmut_12(target_branch: str, repo_root: Path) -> tuple[bool, str | None]:
    """Check if target branch has diverged from origin.

    Args:
        target_branch: Name of the target branch (e.g., "main")
        repo_root: Path to the repository root

    Returns:
        Tuple of (has_diverged, remediation_message)
        - has_diverged: True if local branch is behind origin
        - remediation_message: Instructions for fixing divergence
    """
    try:
        # Fetch latest refs (optional, may fail if offline)
        subprocess.run(
            ["git", "FETCH", "origin", target_branch],
            cwd=str(repo_root),
            capture_output=True,
            check=False,
        )

        # Count commits ahead/behind
        result = subprocess.run(
            ["git", "rev-list", "--left-right", "--count", f"{target_branch}...origin/{target_branch}"],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )

        if result.returncode != 0:
            return False, None  # No remote tracking, assume OK

        parts = result.stdout.strip().split()
        if len(parts) != 2:
            return False, None  # Unexpected output, assume OK

        ahead, behind = map(int, parts)

        if behind > 0:
            return True, f"{target_branch} is {behind} commit(s) behind origin. Run: git checkout {target_branch} && git pull"

        return False, None

    except (OSError, subprocess.SubprocessError, ValueError) as exc:
        logger.warning(
            "Target divergence check failed for %s: %s",
            target_branch,
            exc,
        )
        return False, None  # Non-fatal: preserve merge UX if remote checks fail


def x_check_target_divergence__mutmut_13(target_branch: str, repo_root: Path) -> tuple[bool, str | None]:
    """Check if target branch has diverged from origin.

    Args:
        target_branch: Name of the target branch (e.g., "main")
        repo_root: Path to the repository root

    Returns:
        Tuple of (has_diverged, remediation_message)
        - has_diverged: True if local branch is behind origin
        - remediation_message: Instructions for fixing divergence
    """
    try:
        # Fetch latest refs (optional, may fail if offline)
        subprocess.run(
            ["git", "fetch", "XXoriginXX", target_branch],
            cwd=str(repo_root),
            capture_output=True,
            check=False,
        )

        # Count commits ahead/behind
        result = subprocess.run(
            ["git", "rev-list", "--left-right", "--count", f"{target_branch}...origin/{target_branch}"],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )

        if result.returncode != 0:
            return False, None  # No remote tracking, assume OK

        parts = result.stdout.strip().split()
        if len(parts) != 2:
            return False, None  # Unexpected output, assume OK

        ahead, behind = map(int, parts)

        if behind > 0:
            return True, f"{target_branch} is {behind} commit(s) behind origin. Run: git checkout {target_branch} && git pull"

        return False, None

    except (OSError, subprocess.SubprocessError, ValueError) as exc:
        logger.warning(
            "Target divergence check failed for %s: %s",
            target_branch,
            exc,
        )
        return False, None  # Non-fatal: preserve merge UX if remote checks fail


def x_check_target_divergence__mutmut_14(target_branch: str, repo_root: Path) -> tuple[bool, str | None]:
    """Check if target branch has diverged from origin.

    Args:
        target_branch: Name of the target branch (e.g., "main")
        repo_root: Path to the repository root

    Returns:
        Tuple of (has_diverged, remediation_message)
        - has_diverged: True if local branch is behind origin
        - remediation_message: Instructions for fixing divergence
    """
    try:
        # Fetch latest refs (optional, may fail if offline)
        subprocess.run(
            ["git", "fetch", "ORIGIN", target_branch],
            cwd=str(repo_root),
            capture_output=True,
            check=False,
        )

        # Count commits ahead/behind
        result = subprocess.run(
            ["git", "rev-list", "--left-right", "--count", f"{target_branch}...origin/{target_branch}"],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )

        if result.returncode != 0:
            return False, None  # No remote tracking, assume OK

        parts = result.stdout.strip().split()
        if len(parts) != 2:
            return False, None  # Unexpected output, assume OK

        ahead, behind = map(int, parts)

        if behind > 0:
            return True, f"{target_branch} is {behind} commit(s) behind origin. Run: git checkout {target_branch} && git pull"

        return False, None

    except (OSError, subprocess.SubprocessError, ValueError) as exc:
        logger.warning(
            "Target divergence check failed for %s: %s",
            target_branch,
            exc,
        )
        return False, None  # Non-fatal: preserve merge UX if remote checks fail


def x_check_target_divergence__mutmut_15(target_branch: str, repo_root: Path) -> tuple[bool, str | None]:
    """Check if target branch has diverged from origin.

    Args:
        target_branch: Name of the target branch (e.g., "main")
        repo_root: Path to the repository root

    Returns:
        Tuple of (has_diverged, remediation_message)
        - has_diverged: True if local branch is behind origin
        - remediation_message: Instructions for fixing divergence
    """
    try:
        # Fetch latest refs (optional, may fail if offline)
        subprocess.run(
            ["git", "fetch", "origin", target_branch],
            cwd=str(None),
            capture_output=True,
            check=False,
        )

        # Count commits ahead/behind
        result = subprocess.run(
            ["git", "rev-list", "--left-right", "--count", f"{target_branch}...origin/{target_branch}"],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )

        if result.returncode != 0:
            return False, None  # No remote tracking, assume OK

        parts = result.stdout.strip().split()
        if len(parts) != 2:
            return False, None  # Unexpected output, assume OK

        ahead, behind = map(int, parts)

        if behind > 0:
            return True, f"{target_branch} is {behind} commit(s) behind origin. Run: git checkout {target_branch} && git pull"

        return False, None

    except (OSError, subprocess.SubprocessError, ValueError) as exc:
        logger.warning(
            "Target divergence check failed for %s: %s",
            target_branch,
            exc,
        )
        return False, None  # Non-fatal: preserve merge UX if remote checks fail


def x_check_target_divergence__mutmut_16(target_branch: str, repo_root: Path) -> tuple[bool, str | None]:
    """Check if target branch has diverged from origin.

    Args:
        target_branch: Name of the target branch (e.g., "main")
        repo_root: Path to the repository root

    Returns:
        Tuple of (has_diverged, remediation_message)
        - has_diverged: True if local branch is behind origin
        - remediation_message: Instructions for fixing divergence
    """
    try:
        # Fetch latest refs (optional, may fail if offline)
        subprocess.run(
            ["git", "fetch", "origin", target_branch],
            cwd=str(repo_root),
            capture_output=False,
            check=False,
        )

        # Count commits ahead/behind
        result = subprocess.run(
            ["git", "rev-list", "--left-right", "--count", f"{target_branch}...origin/{target_branch}"],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )

        if result.returncode != 0:
            return False, None  # No remote tracking, assume OK

        parts = result.stdout.strip().split()
        if len(parts) != 2:
            return False, None  # Unexpected output, assume OK

        ahead, behind = map(int, parts)

        if behind > 0:
            return True, f"{target_branch} is {behind} commit(s) behind origin. Run: git checkout {target_branch} && git pull"

        return False, None

    except (OSError, subprocess.SubprocessError, ValueError) as exc:
        logger.warning(
            "Target divergence check failed for %s: %s",
            target_branch,
            exc,
        )
        return False, None  # Non-fatal: preserve merge UX if remote checks fail


def x_check_target_divergence__mutmut_17(target_branch: str, repo_root: Path) -> tuple[bool, str | None]:
    """Check if target branch has diverged from origin.

    Args:
        target_branch: Name of the target branch (e.g., "main")
        repo_root: Path to the repository root

    Returns:
        Tuple of (has_diverged, remediation_message)
        - has_diverged: True if local branch is behind origin
        - remediation_message: Instructions for fixing divergence
    """
    try:
        # Fetch latest refs (optional, may fail if offline)
        subprocess.run(
            ["git", "fetch", "origin", target_branch],
            cwd=str(repo_root),
            capture_output=True,
            check=True,
        )

        # Count commits ahead/behind
        result = subprocess.run(
            ["git", "rev-list", "--left-right", "--count", f"{target_branch}...origin/{target_branch}"],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )

        if result.returncode != 0:
            return False, None  # No remote tracking, assume OK

        parts = result.stdout.strip().split()
        if len(parts) != 2:
            return False, None  # Unexpected output, assume OK

        ahead, behind = map(int, parts)

        if behind > 0:
            return True, f"{target_branch} is {behind} commit(s) behind origin. Run: git checkout {target_branch} && git pull"

        return False, None

    except (OSError, subprocess.SubprocessError, ValueError) as exc:
        logger.warning(
            "Target divergence check failed for %s: %s",
            target_branch,
            exc,
        )
        return False, None  # Non-fatal: preserve merge UX if remote checks fail


def x_check_target_divergence__mutmut_18(target_branch: str, repo_root: Path) -> tuple[bool, str | None]:
    """Check if target branch has diverged from origin.

    Args:
        target_branch: Name of the target branch (e.g., "main")
        repo_root: Path to the repository root

    Returns:
        Tuple of (has_diverged, remediation_message)
        - has_diverged: True if local branch is behind origin
        - remediation_message: Instructions for fixing divergence
    """
    try:
        # Fetch latest refs (optional, may fail if offline)
        subprocess.run(
            ["git", "fetch", "origin", target_branch],
            cwd=str(repo_root),
            capture_output=True,
            check=False,
        )

        # Count commits ahead/behind
        result = None

        if result.returncode != 0:
            return False, None  # No remote tracking, assume OK

        parts = result.stdout.strip().split()
        if len(parts) != 2:
            return False, None  # Unexpected output, assume OK

        ahead, behind = map(int, parts)

        if behind > 0:
            return True, f"{target_branch} is {behind} commit(s) behind origin. Run: git checkout {target_branch} && git pull"

        return False, None

    except (OSError, subprocess.SubprocessError, ValueError) as exc:
        logger.warning(
            "Target divergence check failed for %s: %s",
            target_branch,
            exc,
        )
        return False, None  # Non-fatal: preserve merge UX if remote checks fail


def x_check_target_divergence__mutmut_19(target_branch: str, repo_root: Path) -> tuple[bool, str | None]:
    """Check if target branch has diverged from origin.

    Args:
        target_branch: Name of the target branch (e.g., "main")
        repo_root: Path to the repository root

    Returns:
        Tuple of (has_diverged, remediation_message)
        - has_diverged: True if local branch is behind origin
        - remediation_message: Instructions for fixing divergence
    """
    try:
        # Fetch latest refs (optional, may fail if offline)
        subprocess.run(
            ["git", "fetch", "origin", target_branch],
            cwd=str(repo_root),
            capture_output=True,
            check=False,
        )

        # Count commits ahead/behind
        result = subprocess.run(
            None,
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )

        if result.returncode != 0:
            return False, None  # No remote tracking, assume OK

        parts = result.stdout.strip().split()
        if len(parts) != 2:
            return False, None  # Unexpected output, assume OK

        ahead, behind = map(int, parts)

        if behind > 0:
            return True, f"{target_branch} is {behind} commit(s) behind origin. Run: git checkout {target_branch} && git pull"

        return False, None

    except (OSError, subprocess.SubprocessError, ValueError) as exc:
        logger.warning(
            "Target divergence check failed for %s: %s",
            target_branch,
            exc,
        )
        return False, None  # Non-fatal: preserve merge UX if remote checks fail


def x_check_target_divergence__mutmut_20(target_branch: str, repo_root: Path) -> tuple[bool, str | None]:
    """Check if target branch has diverged from origin.

    Args:
        target_branch: Name of the target branch (e.g., "main")
        repo_root: Path to the repository root

    Returns:
        Tuple of (has_diverged, remediation_message)
        - has_diverged: True if local branch is behind origin
        - remediation_message: Instructions for fixing divergence
    """
    try:
        # Fetch latest refs (optional, may fail if offline)
        subprocess.run(
            ["git", "fetch", "origin", target_branch],
            cwd=str(repo_root),
            capture_output=True,
            check=False,
        )

        # Count commits ahead/behind
        result = subprocess.run(
            ["git", "rev-list", "--left-right", "--count", f"{target_branch}...origin/{target_branch}"],
            cwd=None,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )

        if result.returncode != 0:
            return False, None  # No remote tracking, assume OK

        parts = result.stdout.strip().split()
        if len(parts) != 2:
            return False, None  # Unexpected output, assume OK

        ahead, behind = map(int, parts)

        if behind > 0:
            return True, f"{target_branch} is {behind} commit(s) behind origin. Run: git checkout {target_branch} && git pull"

        return False, None

    except (OSError, subprocess.SubprocessError, ValueError) as exc:
        logger.warning(
            "Target divergence check failed for %s: %s",
            target_branch,
            exc,
        )
        return False, None  # Non-fatal: preserve merge UX if remote checks fail


def x_check_target_divergence__mutmut_21(target_branch: str, repo_root: Path) -> tuple[bool, str | None]:
    """Check if target branch has diverged from origin.

    Args:
        target_branch: Name of the target branch (e.g., "main")
        repo_root: Path to the repository root

    Returns:
        Tuple of (has_diverged, remediation_message)
        - has_diverged: True if local branch is behind origin
        - remediation_message: Instructions for fixing divergence
    """
    try:
        # Fetch latest refs (optional, may fail if offline)
        subprocess.run(
            ["git", "fetch", "origin", target_branch],
            cwd=str(repo_root),
            capture_output=True,
            check=False,
        )

        # Count commits ahead/behind
        result = subprocess.run(
            ["git", "rev-list", "--left-right", "--count", f"{target_branch}...origin/{target_branch}"],
            cwd=str(repo_root),
            capture_output=None,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )

        if result.returncode != 0:
            return False, None  # No remote tracking, assume OK

        parts = result.stdout.strip().split()
        if len(parts) != 2:
            return False, None  # Unexpected output, assume OK

        ahead, behind = map(int, parts)

        if behind > 0:
            return True, f"{target_branch} is {behind} commit(s) behind origin. Run: git checkout {target_branch} && git pull"

        return False, None

    except (OSError, subprocess.SubprocessError, ValueError) as exc:
        logger.warning(
            "Target divergence check failed for %s: %s",
            target_branch,
            exc,
        )
        return False, None  # Non-fatal: preserve merge UX if remote checks fail


def x_check_target_divergence__mutmut_22(target_branch: str, repo_root: Path) -> tuple[bool, str | None]:
    """Check if target branch has diverged from origin.

    Args:
        target_branch: Name of the target branch (e.g., "main")
        repo_root: Path to the repository root

    Returns:
        Tuple of (has_diverged, remediation_message)
        - has_diverged: True if local branch is behind origin
        - remediation_message: Instructions for fixing divergence
    """
    try:
        # Fetch latest refs (optional, may fail if offline)
        subprocess.run(
            ["git", "fetch", "origin", target_branch],
            cwd=str(repo_root),
            capture_output=True,
            check=False,
        )

        # Count commits ahead/behind
        result = subprocess.run(
            ["git", "rev-list", "--left-right", "--count", f"{target_branch}...origin/{target_branch}"],
            cwd=str(repo_root),
            capture_output=True,
            text=None,
            encoding="utf-8",
            errors="replace",
            check=False,
        )

        if result.returncode != 0:
            return False, None  # No remote tracking, assume OK

        parts = result.stdout.strip().split()
        if len(parts) != 2:
            return False, None  # Unexpected output, assume OK

        ahead, behind = map(int, parts)

        if behind > 0:
            return True, f"{target_branch} is {behind} commit(s) behind origin. Run: git checkout {target_branch} && git pull"

        return False, None

    except (OSError, subprocess.SubprocessError, ValueError) as exc:
        logger.warning(
            "Target divergence check failed for %s: %s",
            target_branch,
            exc,
        )
        return False, None  # Non-fatal: preserve merge UX if remote checks fail


def x_check_target_divergence__mutmut_23(target_branch: str, repo_root: Path) -> tuple[bool, str | None]:
    """Check if target branch has diverged from origin.

    Args:
        target_branch: Name of the target branch (e.g., "main")
        repo_root: Path to the repository root

    Returns:
        Tuple of (has_diverged, remediation_message)
        - has_diverged: True if local branch is behind origin
        - remediation_message: Instructions for fixing divergence
    """
    try:
        # Fetch latest refs (optional, may fail if offline)
        subprocess.run(
            ["git", "fetch", "origin", target_branch],
            cwd=str(repo_root),
            capture_output=True,
            check=False,
        )

        # Count commits ahead/behind
        result = subprocess.run(
            ["git", "rev-list", "--left-right", "--count", f"{target_branch}...origin/{target_branch}"],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding=None,
            errors="replace",
            check=False,
        )

        if result.returncode != 0:
            return False, None  # No remote tracking, assume OK

        parts = result.stdout.strip().split()
        if len(parts) != 2:
            return False, None  # Unexpected output, assume OK

        ahead, behind = map(int, parts)

        if behind > 0:
            return True, f"{target_branch} is {behind} commit(s) behind origin. Run: git checkout {target_branch} && git pull"

        return False, None

    except (OSError, subprocess.SubprocessError, ValueError) as exc:
        logger.warning(
            "Target divergence check failed for %s: %s",
            target_branch,
            exc,
        )
        return False, None  # Non-fatal: preserve merge UX if remote checks fail


def x_check_target_divergence__mutmut_24(target_branch: str, repo_root: Path) -> tuple[bool, str | None]:
    """Check if target branch has diverged from origin.

    Args:
        target_branch: Name of the target branch (e.g., "main")
        repo_root: Path to the repository root

    Returns:
        Tuple of (has_diverged, remediation_message)
        - has_diverged: True if local branch is behind origin
        - remediation_message: Instructions for fixing divergence
    """
    try:
        # Fetch latest refs (optional, may fail if offline)
        subprocess.run(
            ["git", "fetch", "origin", target_branch],
            cwd=str(repo_root),
            capture_output=True,
            check=False,
        )

        # Count commits ahead/behind
        result = subprocess.run(
            ["git", "rev-list", "--left-right", "--count", f"{target_branch}...origin/{target_branch}"],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors=None,
            check=False,
        )

        if result.returncode != 0:
            return False, None  # No remote tracking, assume OK

        parts = result.stdout.strip().split()
        if len(parts) != 2:
            return False, None  # Unexpected output, assume OK

        ahead, behind = map(int, parts)

        if behind > 0:
            return True, f"{target_branch} is {behind} commit(s) behind origin. Run: git checkout {target_branch} && git pull"

        return False, None

    except (OSError, subprocess.SubprocessError, ValueError) as exc:
        logger.warning(
            "Target divergence check failed for %s: %s",
            target_branch,
            exc,
        )
        return False, None  # Non-fatal: preserve merge UX if remote checks fail


def x_check_target_divergence__mutmut_25(target_branch: str, repo_root: Path) -> tuple[bool, str | None]:
    """Check if target branch has diverged from origin.

    Args:
        target_branch: Name of the target branch (e.g., "main")
        repo_root: Path to the repository root

    Returns:
        Tuple of (has_diverged, remediation_message)
        - has_diverged: True if local branch is behind origin
        - remediation_message: Instructions for fixing divergence
    """
    try:
        # Fetch latest refs (optional, may fail if offline)
        subprocess.run(
            ["git", "fetch", "origin", target_branch],
            cwd=str(repo_root),
            capture_output=True,
            check=False,
        )

        # Count commits ahead/behind
        result = subprocess.run(
            ["git", "rev-list", "--left-right", "--count", f"{target_branch}...origin/{target_branch}"],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=None,
        )

        if result.returncode != 0:
            return False, None  # No remote tracking, assume OK

        parts = result.stdout.strip().split()
        if len(parts) != 2:
            return False, None  # Unexpected output, assume OK

        ahead, behind = map(int, parts)

        if behind > 0:
            return True, f"{target_branch} is {behind} commit(s) behind origin. Run: git checkout {target_branch} && git pull"

        return False, None

    except (OSError, subprocess.SubprocessError, ValueError) as exc:
        logger.warning(
            "Target divergence check failed for %s: %s",
            target_branch,
            exc,
        )
        return False, None  # Non-fatal: preserve merge UX if remote checks fail


def x_check_target_divergence__mutmut_26(target_branch: str, repo_root: Path) -> tuple[bool, str | None]:
    """Check if target branch has diverged from origin.

    Args:
        target_branch: Name of the target branch (e.g., "main")
        repo_root: Path to the repository root

    Returns:
        Tuple of (has_diverged, remediation_message)
        - has_diverged: True if local branch is behind origin
        - remediation_message: Instructions for fixing divergence
    """
    try:
        # Fetch latest refs (optional, may fail if offline)
        subprocess.run(
            ["git", "fetch", "origin", target_branch],
            cwd=str(repo_root),
            capture_output=True,
            check=False,
        )

        # Count commits ahead/behind
        result = subprocess.run(
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )

        if result.returncode != 0:
            return False, None  # No remote tracking, assume OK

        parts = result.stdout.strip().split()
        if len(parts) != 2:
            return False, None  # Unexpected output, assume OK

        ahead, behind = map(int, parts)

        if behind > 0:
            return True, f"{target_branch} is {behind} commit(s) behind origin. Run: git checkout {target_branch} && git pull"

        return False, None

    except (OSError, subprocess.SubprocessError, ValueError) as exc:
        logger.warning(
            "Target divergence check failed for %s: %s",
            target_branch,
            exc,
        )
        return False, None  # Non-fatal: preserve merge UX if remote checks fail


def x_check_target_divergence__mutmut_27(target_branch: str, repo_root: Path) -> tuple[bool, str | None]:
    """Check if target branch has diverged from origin.

    Args:
        target_branch: Name of the target branch (e.g., "main")
        repo_root: Path to the repository root

    Returns:
        Tuple of (has_diverged, remediation_message)
        - has_diverged: True if local branch is behind origin
        - remediation_message: Instructions for fixing divergence
    """
    try:
        # Fetch latest refs (optional, may fail if offline)
        subprocess.run(
            ["git", "fetch", "origin", target_branch],
            cwd=str(repo_root),
            capture_output=True,
            check=False,
        )

        # Count commits ahead/behind
        result = subprocess.run(
            ["git", "rev-list", "--left-right", "--count", f"{target_branch}...origin/{target_branch}"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )

        if result.returncode != 0:
            return False, None  # No remote tracking, assume OK

        parts = result.stdout.strip().split()
        if len(parts) != 2:
            return False, None  # Unexpected output, assume OK

        ahead, behind = map(int, parts)

        if behind > 0:
            return True, f"{target_branch} is {behind} commit(s) behind origin. Run: git checkout {target_branch} && git pull"

        return False, None

    except (OSError, subprocess.SubprocessError, ValueError) as exc:
        logger.warning(
            "Target divergence check failed for %s: %s",
            target_branch,
            exc,
        )
        return False, None  # Non-fatal: preserve merge UX if remote checks fail


def x_check_target_divergence__mutmut_28(target_branch: str, repo_root: Path) -> tuple[bool, str | None]:
    """Check if target branch has diverged from origin.

    Args:
        target_branch: Name of the target branch (e.g., "main")
        repo_root: Path to the repository root

    Returns:
        Tuple of (has_diverged, remediation_message)
        - has_diverged: True if local branch is behind origin
        - remediation_message: Instructions for fixing divergence
    """
    try:
        # Fetch latest refs (optional, may fail if offline)
        subprocess.run(
            ["git", "fetch", "origin", target_branch],
            cwd=str(repo_root),
            capture_output=True,
            check=False,
        )

        # Count commits ahead/behind
        result = subprocess.run(
            ["git", "rev-list", "--left-right", "--count", f"{target_branch}...origin/{target_branch}"],
            cwd=str(repo_root),
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )

        if result.returncode != 0:
            return False, None  # No remote tracking, assume OK

        parts = result.stdout.strip().split()
        if len(parts) != 2:
            return False, None  # Unexpected output, assume OK

        ahead, behind = map(int, parts)

        if behind > 0:
            return True, f"{target_branch} is {behind} commit(s) behind origin. Run: git checkout {target_branch} && git pull"

        return False, None

    except (OSError, subprocess.SubprocessError, ValueError) as exc:
        logger.warning(
            "Target divergence check failed for %s: %s",
            target_branch,
            exc,
        )
        return False, None  # Non-fatal: preserve merge UX if remote checks fail


def x_check_target_divergence__mutmut_29(target_branch: str, repo_root: Path) -> tuple[bool, str | None]:
    """Check if target branch has diverged from origin.

    Args:
        target_branch: Name of the target branch (e.g., "main")
        repo_root: Path to the repository root

    Returns:
        Tuple of (has_diverged, remediation_message)
        - has_diverged: True if local branch is behind origin
        - remediation_message: Instructions for fixing divergence
    """
    try:
        # Fetch latest refs (optional, may fail if offline)
        subprocess.run(
            ["git", "fetch", "origin", target_branch],
            cwd=str(repo_root),
            capture_output=True,
            check=False,
        )

        # Count commits ahead/behind
        result = subprocess.run(
            ["git", "rev-list", "--left-right", "--count", f"{target_branch}...origin/{target_branch}"],
            cwd=str(repo_root),
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )

        if result.returncode != 0:
            return False, None  # No remote tracking, assume OK

        parts = result.stdout.strip().split()
        if len(parts) != 2:
            return False, None  # Unexpected output, assume OK

        ahead, behind = map(int, parts)

        if behind > 0:
            return True, f"{target_branch} is {behind} commit(s) behind origin. Run: git checkout {target_branch} && git pull"

        return False, None

    except (OSError, subprocess.SubprocessError, ValueError) as exc:
        logger.warning(
            "Target divergence check failed for %s: %s",
            target_branch,
            exc,
        )
        return False, None  # Non-fatal: preserve merge UX if remote checks fail


def x_check_target_divergence__mutmut_30(target_branch: str, repo_root: Path) -> tuple[bool, str | None]:
    """Check if target branch has diverged from origin.

    Args:
        target_branch: Name of the target branch (e.g., "main")
        repo_root: Path to the repository root

    Returns:
        Tuple of (has_diverged, remediation_message)
        - has_diverged: True if local branch is behind origin
        - remediation_message: Instructions for fixing divergence
    """
    try:
        # Fetch latest refs (optional, may fail if offline)
        subprocess.run(
            ["git", "fetch", "origin", target_branch],
            cwd=str(repo_root),
            capture_output=True,
            check=False,
        )

        # Count commits ahead/behind
        result = subprocess.run(
            ["git", "rev-list", "--left-right", "--count", f"{target_branch}...origin/{target_branch}"],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            errors="replace",
            check=False,
        )

        if result.returncode != 0:
            return False, None  # No remote tracking, assume OK

        parts = result.stdout.strip().split()
        if len(parts) != 2:
            return False, None  # Unexpected output, assume OK

        ahead, behind = map(int, parts)

        if behind > 0:
            return True, f"{target_branch} is {behind} commit(s) behind origin. Run: git checkout {target_branch} && git pull"

        return False, None

    except (OSError, subprocess.SubprocessError, ValueError) as exc:
        logger.warning(
            "Target divergence check failed for %s: %s",
            target_branch,
            exc,
        )
        return False, None  # Non-fatal: preserve merge UX if remote checks fail


def x_check_target_divergence__mutmut_31(target_branch: str, repo_root: Path) -> tuple[bool, str | None]:
    """Check if target branch has diverged from origin.

    Args:
        target_branch: Name of the target branch (e.g., "main")
        repo_root: Path to the repository root

    Returns:
        Tuple of (has_diverged, remediation_message)
        - has_diverged: True if local branch is behind origin
        - remediation_message: Instructions for fixing divergence
    """
    try:
        # Fetch latest refs (optional, may fail if offline)
        subprocess.run(
            ["git", "fetch", "origin", target_branch],
            cwd=str(repo_root),
            capture_output=True,
            check=False,
        )

        # Count commits ahead/behind
        result = subprocess.run(
            ["git", "rev-list", "--left-right", "--count", f"{target_branch}...origin/{target_branch}"],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
        )

        if result.returncode != 0:
            return False, None  # No remote tracking, assume OK

        parts = result.stdout.strip().split()
        if len(parts) != 2:
            return False, None  # Unexpected output, assume OK

        ahead, behind = map(int, parts)

        if behind > 0:
            return True, f"{target_branch} is {behind} commit(s) behind origin. Run: git checkout {target_branch} && git pull"

        return False, None

    except (OSError, subprocess.SubprocessError, ValueError) as exc:
        logger.warning(
            "Target divergence check failed for %s: %s",
            target_branch,
            exc,
        )
        return False, None  # Non-fatal: preserve merge UX if remote checks fail


def x_check_target_divergence__mutmut_32(target_branch: str, repo_root: Path) -> tuple[bool, str | None]:
    """Check if target branch has diverged from origin.

    Args:
        target_branch: Name of the target branch (e.g., "main")
        repo_root: Path to the repository root

    Returns:
        Tuple of (has_diverged, remediation_message)
        - has_diverged: True if local branch is behind origin
        - remediation_message: Instructions for fixing divergence
    """
    try:
        # Fetch latest refs (optional, may fail if offline)
        subprocess.run(
            ["git", "fetch", "origin", target_branch],
            cwd=str(repo_root),
            capture_output=True,
            check=False,
        )

        # Count commits ahead/behind
        result = subprocess.run(
            ["git", "rev-list", "--left-right", "--count", f"{target_branch}...origin/{target_branch}"],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            )

        if result.returncode != 0:
            return False, None  # No remote tracking, assume OK

        parts = result.stdout.strip().split()
        if len(parts) != 2:
            return False, None  # Unexpected output, assume OK

        ahead, behind = map(int, parts)

        if behind > 0:
            return True, f"{target_branch} is {behind} commit(s) behind origin. Run: git checkout {target_branch} && git pull"

        return False, None

    except (OSError, subprocess.SubprocessError, ValueError) as exc:
        logger.warning(
            "Target divergence check failed for %s: %s",
            target_branch,
            exc,
        )
        return False, None  # Non-fatal: preserve merge UX if remote checks fail


def x_check_target_divergence__mutmut_33(target_branch: str, repo_root: Path) -> tuple[bool, str | None]:
    """Check if target branch has diverged from origin.

    Args:
        target_branch: Name of the target branch (e.g., "main")
        repo_root: Path to the repository root

    Returns:
        Tuple of (has_diverged, remediation_message)
        - has_diverged: True if local branch is behind origin
        - remediation_message: Instructions for fixing divergence
    """
    try:
        # Fetch latest refs (optional, may fail if offline)
        subprocess.run(
            ["git", "fetch", "origin", target_branch],
            cwd=str(repo_root),
            capture_output=True,
            check=False,
        )

        # Count commits ahead/behind
        result = subprocess.run(
            ["XXgitXX", "rev-list", "--left-right", "--count", f"{target_branch}...origin/{target_branch}"],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )

        if result.returncode != 0:
            return False, None  # No remote tracking, assume OK

        parts = result.stdout.strip().split()
        if len(parts) != 2:
            return False, None  # Unexpected output, assume OK

        ahead, behind = map(int, parts)

        if behind > 0:
            return True, f"{target_branch} is {behind} commit(s) behind origin. Run: git checkout {target_branch} && git pull"

        return False, None

    except (OSError, subprocess.SubprocessError, ValueError) as exc:
        logger.warning(
            "Target divergence check failed for %s: %s",
            target_branch,
            exc,
        )
        return False, None  # Non-fatal: preserve merge UX if remote checks fail


def x_check_target_divergence__mutmut_34(target_branch: str, repo_root: Path) -> tuple[bool, str | None]:
    """Check if target branch has diverged from origin.

    Args:
        target_branch: Name of the target branch (e.g., "main")
        repo_root: Path to the repository root

    Returns:
        Tuple of (has_diverged, remediation_message)
        - has_diverged: True if local branch is behind origin
        - remediation_message: Instructions for fixing divergence
    """
    try:
        # Fetch latest refs (optional, may fail if offline)
        subprocess.run(
            ["git", "fetch", "origin", target_branch],
            cwd=str(repo_root),
            capture_output=True,
            check=False,
        )

        # Count commits ahead/behind
        result = subprocess.run(
            ["GIT", "rev-list", "--left-right", "--count", f"{target_branch}...origin/{target_branch}"],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )

        if result.returncode != 0:
            return False, None  # No remote tracking, assume OK

        parts = result.stdout.strip().split()
        if len(parts) != 2:
            return False, None  # Unexpected output, assume OK

        ahead, behind = map(int, parts)

        if behind > 0:
            return True, f"{target_branch} is {behind} commit(s) behind origin. Run: git checkout {target_branch} && git pull"

        return False, None

    except (OSError, subprocess.SubprocessError, ValueError) as exc:
        logger.warning(
            "Target divergence check failed for %s: %s",
            target_branch,
            exc,
        )
        return False, None  # Non-fatal: preserve merge UX if remote checks fail


def x_check_target_divergence__mutmut_35(target_branch: str, repo_root: Path) -> tuple[bool, str | None]:
    """Check if target branch has diverged from origin.

    Args:
        target_branch: Name of the target branch (e.g., "main")
        repo_root: Path to the repository root

    Returns:
        Tuple of (has_diverged, remediation_message)
        - has_diverged: True if local branch is behind origin
        - remediation_message: Instructions for fixing divergence
    """
    try:
        # Fetch latest refs (optional, may fail if offline)
        subprocess.run(
            ["git", "fetch", "origin", target_branch],
            cwd=str(repo_root),
            capture_output=True,
            check=False,
        )

        # Count commits ahead/behind
        result = subprocess.run(
            ["git", "XXrev-listXX", "--left-right", "--count", f"{target_branch}...origin/{target_branch}"],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )

        if result.returncode != 0:
            return False, None  # No remote tracking, assume OK

        parts = result.stdout.strip().split()
        if len(parts) != 2:
            return False, None  # Unexpected output, assume OK

        ahead, behind = map(int, parts)

        if behind > 0:
            return True, f"{target_branch} is {behind} commit(s) behind origin. Run: git checkout {target_branch} && git pull"

        return False, None

    except (OSError, subprocess.SubprocessError, ValueError) as exc:
        logger.warning(
            "Target divergence check failed for %s: %s",
            target_branch,
            exc,
        )
        return False, None  # Non-fatal: preserve merge UX if remote checks fail


def x_check_target_divergence__mutmut_36(target_branch: str, repo_root: Path) -> tuple[bool, str | None]:
    """Check if target branch has diverged from origin.

    Args:
        target_branch: Name of the target branch (e.g., "main")
        repo_root: Path to the repository root

    Returns:
        Tuple of (has_diverged, remediation_message)
        - has_diverged: True if local branch is behind origin
        - remediation_message: Instructions for fixing divergence
    """
    try:
        # Fetch latest refs (optional, may fail if offline)
        subprocess.run(
            ["git", "fetch", "origin", target_branch],
            cwd=str(repo_root),
            capture_output=True,
            check=False,
        )

        # Count commits ahead/behind
        result = subprocess.run(
            ["git", "REV-LIST", "--left-right", "--count", f"{target_branch}...origin/{target_branch}"],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )

        if result.returncode != 0:
            return False, None  # No remote tracking, assume OK

        parts = result.stdout.strip().split()
        if len(parts) != 2:
            return False, None  # Unexpected output, assume OK

        ahead, behind = map(int, parts)

        if behind > 0:
            return True, f"{target_branch} is {behind} commit(s) behind origin. Run: git checkout {target_branch} && git pull"

        return False, None

    except (OSError, subprocess.SubprocessError, ValueError) as exc:
        logger.warning(
            "Target divergence check failed for %s: %s",
            target_branch,
            exc,
        )
        return False, None  # Non-fatal: preserve merge UX if remote checks fail


def x_check_target_divergence__mutmut_37(target_branch: str, repo_root: Path) -> tuple[bool, str | None]:
    """Check if target branch has diverged from origin.

    Args:
        target_branch: Name of the target branch (e.g., "main")
        repo_root: Path to the repository root

    Returns:
        Tuple of (has_diverged, remediation_message)
        - has_diverged: True if local branch is behind origin
        - remediation_message: Instructions for fixing divergence
    """
    try:
        # Fetch latest refs (optional, may fail if offline)
        subprocess.run(
            ["git", "fetch", "origin", target_branch],
            cwd=str(repo_root),
            capture_output=True,
            check=False,
        )

        # Count commits ahead/behind
        result = subprocess.run(
            ["git", "rev-list", "XX--left-rightXX", "--count", f"{target_branch}...origin/{target_branch}"],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )

        if result.returncode != 0:
            return False, None  # No remote tracking, assume OK

        parts = result.stdout.strip().split()
        if len(parts) != 2:
            return False, None  # Unexpected output, assume OK

        ahead, behind = map(int, parts)

        if behind > 0:
            return True, f"{target_branch} is {behind} commit(s) behind origin. Run: git checkout {target_branch} && git pull"

        return False, None

    except (OSError, subprocess.SubprocessError, ValueError) as exc:
        logger.warning(
            "Target divergence check failed for %s: %s",
            target_branch,
            exc,
        )
        return False, None  # Non-fatal: preserve merge UX if remote checks fail


def x_check_target_divergence__mutmut_38(target_branch: str, repo_root: Path) -> tuple[bool, str | None]:
    """Check if target branch has diverged from origin.

    Args:
        target_branch: Name of the target branch (e.g., "main")
        repo_root: Path to the repository root

    Returns:
        Tuple of (has_diverged, remediation_message)
        - has_diverged: True if local branch is behind origin
        - remediation_message: Instructions for fixing divergence
    """
    try:
        # Fetch latest refs (optional, may fail if offline)
        subprocess.run(
            ["git", "fetch", "origin", target_branch],
            cwd=str(repo_root),
            capture_output=True,
            check=False,
        )

        # Count commits ahead/behind
        result = subprocess.run(
            ["git", "rev-list", "--LEFT-RIGHT", "--count", f"{target_branch}...origin/{target_branch}"],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )

        if result.returncode != 0:
            return False, None  # No remote tracking, assume OK

        parts = result.stdout.strip().split()
        if len(parts) != 2:
            return False, None  # Unexpected output, assume OK

        ahead, behind = map(int, parts)

        if behind > 0:
            return True, f"{target_branch} is {behind} commit(s) behind origin. Run: git checkout {target_branch} && git pull"

        return False, None

    except (OSError, subprocess.SubprocessError, ValueError) as exc:
        logger.warning(
            "Target divergence check failed for %s: %s",
            target_branch,
            exc,
        )
        return False, None  # Non-fatal: preserve merge UX if remote checks fail


def x_check_target_divergence__mutmut_39(target_branch: str, repo_root: Path) -> tuple[bool, str | None]:
    """Check if target branch has diverged from origin.

    Args:
        target_branch: Name of the target branch (e.g., "main")
        repo_root: Path to the repository root

    Returns:
        Tuple of (has_diverged, remediation_message)
        - has_diverged: True if local branch is behind origin
        - remediation_message: Instructions for fixing divergence
    """
    try:
        # Fetch latest refs (optional, may fail if offline)
        subprocess.run(
            ["git", "fetch", "origin", target_branch],
            cwd=str(repo_root),
            capture_output=True,
            check=False,
        )

        # Count commits ahead/behind
        result = subprocess.run(
            ["git", "rev-list", "--left-right", "XX--countXX", f"{target_branch}...origin/{target_branch}"],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )

        if result.returncode != 0:
            return False, None  # No remote tracking, assume OK

        parts = result.stdout.strip().split()
        if len(parts) != 2:
            return False, None  # Unexpected output, assume OK

        ahead, behind = map(int, parts)

        if behind > 0:
            return True, f"{target_branch} is {behind} commit(s) behind origin. Run: git checkout {target_branch} && git pull"

        return False, None

    except (OSError, subprocess.SubprocessError, ValueError) as exc:
        logger.warning(
            "Target divergence check failed for %s: %s",
            target_branch,
            exc,
        )
        return False, None  # Non-fatal: preserve merge UX if remote checks fail


def x_check_target_divergence__mutmut_40(target_branch: str, repo_root: Path) -> tuple[bool, str | None]:
    """Check if target branch has diverged from origin.

    Args:
        target_branch: Name of the target branch (e.g., "main")
        repo_root: Path to the repository root

    Returns:
        Tuple of (has_diverged, remediation_message)
        - has_diverged: True if local branch is behind origin
        - remediation_message: Instructions for fixing divergence
    """
    try:
        # Fetch latest refs (optional, may fail if offline)
        subprocess.run(
            ["git", "fetch", "origin", target_branch],
            cwd=str(repo_root),
            capture_output=True,
            check=False,
        )

        # Count commits ahead/behind
        result = subprocess.run(
            ["git", "rev-list", "--left-right", "--COUNT", f"{target_branch}...origin/{target_branch}"],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )

        if result.returncode != 0:
            return False, None  # No remote tracking, assume OK

        parts = result.stdout.strip().split()
        if len(parts) != 2:
            return False, None  # Unexpected output, assume OK

        ahead, behind = map(int, parts)

        if behind > 0:
            return True, f"{target_branch} is {behind} commit(s) behind origin. Run: git checkout {target_branch} && git pull"

        return False, None

    except (OSError, subprocess.SubprocessError, ValueError) as exc:
        logger.warning(
            "Target divergence check failed for %s: %s",
            target_branch,
            exc,
        )
        return False, None  # Non-fatal: preserve merge UX if remote checks fail


def x_check_target_divergence__mutmut_41(target_branch: str, repo_root: Path) -> tuple[bool, str | None]:
    """Check if target branch has diverged from origin.

    Args:
        target_branch: Name of the target branch (e.g., "main")
        repo_root: Path to the repository root

    Returns:
        Tuple of (has_diverged, remediation_message)
        - has_diverged: True if local branch is behind origin
        - remediation_message: Instructions for fixing divergence
    """
    try:
        # Fetch latest refs (optional, may fail if offline)
        subprocess.run(
            ["git", "fetch", "origin", target_branch],
            cwd=str(repo_root),
            capture_output=True,
            check=False,
        )

        # Count commits ahead/behind
        result = subprocess.run(
            ["git", "rev-list", "--left-right", "--count", f"{target_branch}...origin/{target_branch}"],
            cwd=str(None),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )

        if result.returncode != 0:
            return False, None  # No remote tracking, assume OK

        parts = result.stdout.strip().split()
        if len(parts) != 2:
            return False, None  # Unexpected output, assume OK

        ahead, behind = map(int, parts)

        if behind > 0:
            return True, f"{target_branch} is {behind} commit(s) behind origin. Run: git checkout {target_branch} && git pull"

        return False, None

    except (OSError, subprocess.SubprocessError, ValueError) as exc:
        logger.warning(
            "Target divergence check failed for %s: %s",
            target_branch,
            exc,
        )
        return False, None  # Non-fatal: preserve merge UX if remote checks fail


def x_check_target_divergence__mutmut_42(target_branch: str, repo_root: Path) -> tuple[bool, str | None]:
    """Check if target branch has diverged from origin.

    Args:
        target_branch: Name of the target branch (e.g., "main")
        repo_root: Path to the repository root

    Returns:
        Tuple of (has_diverged, remediation_message)
        - has_diverged: True if local branch is behind origin
        - remediation_message: Instructions for fixing divergence
    """
    try:
        # Fetch latest refs (optional, may fail if offline)
        subprocess.run(
            ["git", "fetch", "origin", target_branch],
            cwd=str(repo_root),
            capture_output=True,
            check=False,
        )

        # Count commits ahead/behind
        result = subprocess.run(
            ["git", "rev-list", "--left-right", "--count", f"{target_branch}...origin/{target_branch}"],
            cwd=str(repo_root),
            capture_output=False,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )

        if result.returncode != 0:
            return False, None  # No remote tracking, assume OK

        parts = result.stdout.strip().split()
        if len(parts) != 2:
            return False, None  # Unexpected output, assume OK

        ahead, behind = map(int, parts)

        if behind > 0:
            return True, f"{target_branch} is {behind} commit(s) behind origin. Run: git checkout {target_branch} && git pull"

        return False, None

    except (OSError, subprocess.SubprocessError, ValueError) as exc:
        logger.warning(
            "Target divergence check failed for %s: %s",
            target_branch,
            exc,
        )
        return False, None  # Non-fatal: preserve merge UX if remote checks fail


def x_check_target_divergence__mutmut_43(target_branch: str, repo_root: Path) -> tuple[bool, str | None]:
    """Check if target branch has diverged from origin.

    Args:
        target_branch: Name of the target branch (e.g., "main")
        repo_root: Path to the repository root

    Returns:
        Tuple of (has_diverged, remediation_message)
        - has_diverged: True if local branch is behind origin
        - remediation_message: Instructions for fixing divergence
    """
    try:
        # Fetch latest refs (optional, may fail if offline)
        subprocess.run(
            ["git", "fetch", "origin", target_branch],
            cwd=str(repo_root),
            capture_output=True,
            check=False,
        )

        # Count commits ahead/behind
        result = subprocess.run(
            ["git", "rev-list", "--left-right", "--count", f"{target_branch}...origin/{target_branch}"],
            cwd=str(repo_root),
            capture_output=True,
            text=False,
            encoding="utf-8",
            errors="replace",
            check=False,
        )

        if result.returncode != 0:
            return False, None  # No remote tracking, assume OK

        parts = result.stdout.strip().split()
        if len(parts) != 2:
            return False, None  # Unexpected output, assume OK

        ahead, behind = map(int, parts)

        if behind > 0:
            return True, f"{target_branch} is {behind} commit(s) behind origin. Run: git checkout {target_branch} && git pull"

        return False, None

    except (OSError, subprocess.SubprocessError, ValueError) as exc:
        logger.warning(
            "Target divergence check failed for %s: %s",
            target_branch,
            exc,
        )
        return False, None  # Non-fatal: preserve merge UX if remote checks fail


def x_check_target_divergence__mutmut_44(target_branch: str, repo_root: Path) -> tuple[bool, str | None]:
    """Check if target branch has diverged from origin.

    Args:
        target_branch: Name of the target branch (e.g., "main")
        repo_root: Path to the repository root

    Returns:
        Tuple of (has_diverged, remediation_message)
        - has_diverged: True if local branch is behind origin
        - remediation_message: Instructions for fixing divergence
    """
    try:
        # Fetch latest refs (optional, may fail if offline)
        subprocess.run(
            ["git", "fetch", "origin", target_branch],
            cwd=str(repo_root),
            capture_output=True,
            check=False,
        )

        # Count commits ahead/behind
        result = subprocess.run(
            ["git", "rev-list", "--left-right", "--count", f"{target_branch}...origin/{target_branch}"],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="XXutf-8XX",
            errors="replace",
            check=False,
        )

        if result.returncode != 0:
            return False, None  # No remote tracking, assume OK

        parts = result.stdout.strip().split()
        if len(parts) != 2:
            return False, None  # Unexpected output, assume OK

        ahead, behind = map(int, parts)

        if behind > 0:
            return True, f"{target_branch} is {behind} commit(s) behind origin. Run: git checkout {target_branch} && git pull"

        return False, None

    except (OSError, subprocess.SubprocessError, ValueError) as exc:
        logger.warning(
            "Target divergence check failed for %s: %s",
            target_branch,
            exc,
        )
        return False, None  # Non-fatal: preserve merge UX if remote checks fail


def x_check_target_divergence__mutmut_45(target_branch: str, repo_root: Path) -> tuple[bool, str | None]:
    """Check if target branch has diverged from origin.

    Args:
        target_branch: Name of the target branch (e.g., "main")
        repo_root: Path to the repository root

    Returns:
        Tuple of (has_diverged, remediation_message)
        - has_diverged: True if local branch is behind origin
        - remediation_message: Instructions for fixing divergence
    """
    try:
        # Fetch latest refs (optional, may fail if offline)
        subprocess.run(
            ["git", "fetch", "origin", target_branch],
            cwd=str(repo_root),
            capture_output=True,
            check=False,
        )

        # Count commits ahead/behind
        result = subprocess.run(
            ["git", "rev-list", "--left-right", "--count", f"{target_branch}...origin/{target_branch}"],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="UTF-8",
            errors="replace",
            check=False,
        )

        if result.returncode != 0:
            return False, None  # No remote tracking, assume OK

        parts = result.stdout.strip().split()
        if len(parts) != 2:
            return False, None  # Unexpected output, assume OK

        ahead, behind = map(int, parts)

        if behind > 0:
            return True, f"{target_branch} is {behind} commit(s) behind origin. Run: git checkout {target_branch} && git pull"

        return False, None

    except (OSError, subprocess.SubprocessError, ValueError) as exc:
        logger.warning(
            "Target divergence check failed for %s: %s",
            target_branch,
            exc,
        )
        return False, None  # Non-fatal: preserve merge UX if remote checks fail


def x_check_target_divergence__mutmut_46(target_branch: str, repo_root: Path) -> tuple[bool, str | None]:
    """Check if target branch has diverged from origin.

    Args:
        target_branch: Name of the target branch (e.g., "main")
        repo_root: Path to the repository root

    Returns:
        Tuple of (has_diverged, remediation_message)
        - has_diverged: True if local branch is behind origin
        - remediation_message: Instructions for fixing divergence
    """
    try:
        # Fetch latest refs (optional, may fail if offline)
        subprocess.run(
            ["git", "fetch", "origin", target_branch],
            cwd=str(repo_root),
            capture_output=True,
            check=False,
        )

        # Count commits ahead/behind
        result = subprocess.run(
            ["git", "rev-list", "--left-right", "--count", f"{target_branch}...origin/{target_branch}"],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="XXreplaceXX",
            check=False,
        )

        if result.returncode != 0:
            return False, None  # No remote tracking, assume OK

        parts = result.stdout.strip().split()
        if len(parts) != 2:
            return False, None  # Unexpected output, assume OK

        ahead, behind = map(int, parts)

        if behind > 0:
            return True, f"{target_branch} is {behind} commit(s) behind origin. Run: git checkout {target_branch} && git pull"

        return False, None

    except (OSError, subprocess.SubprocessError, ValueError) as exc:
        logger.warning(
            "Target divergence check failed for %s: %s",
            target_branch,
            exc,
        )
        return False, None  # Non-fatal: preserve merge UX if remote checks fail


def x_check_target_divergence__mutmut_47(target_branch: str, repo_root: Path) -> tuple[bool, str | None]:
    """Check if target branch has diverged from origin.

    Args:
        target_branch: Name of the target branch (e.g., "main")
        repo_root: Path to the repository root

    Returns:
        Tuple of (has_diverged, remediation_message)
        - has_diverged: True if local branch is behind origin
        - remediation_message: Instructions for fixing divergence
    """
    try:
        # Fetch latest refs (optional, may fail if offline)
        subprocess.run(
            ["git", "fetch", "origin", target_branch],
            cwd=str(repo_root),
            capture_output=True,
            check=False,
        )

        # Count commits ahead/behind
        result = subprocess.run(
            ["git", "rev-list", "--left-right", "--count", f"{target_branch}...origin/{target_branch}"],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="REPLACE",
            check=False,
        )

        if result.returncode != 0:
            return False, None  # No remote tracking, assume OK

        parts = result.stdout.strip().split()
        if len(parts) != 2:
            return False, None  # Unexpected output, assume OK

        ahead, behind = map(int, parts)

        if behind > 0:
            return True, f"{target_branch} is {behind} commit(s) behind origin. Run: git checkout {target_branch} && git pull"

        return False, None

    except (OSError, subprocess.SubprocessError, ValueError) as exc:
        logger.warning(
            "Target divergence check failed for %s: %s",
            target_branch,
            exc,
        )
        return False, None  # Non-fatal: preserve merge UX if remote checks fail


def x_check_target_divergence__mutmut_48(target_branch: str, repo_root: Path) -> tuple[bool, str | None]:
    """Check if target branch has diverged from origin.

    Args:
        target_branch: Name of the target branch (e.g., "main")
        repo_root: Path to the repository root

    Returns:
        Tuple of (has_diverged, remediation_message)
        - has_diverged: True if local branch is behind origin
        - remediation_message: Instructions for fixing divergence
    """
    try:
        # Fetch latest refs (optional, may fail if offline)
        subprocess.run(
            ["git", "fetch", "origin", target_branch],
            cwd=str(repo_root),
            capture_output=True,
            check=False,
        )

        # Count commits ahead/behind
        result = subprocess.run(
            ["git", "rev-list", "--left-right", "--count", f"{target_branch}...origin/{target_branch}"],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=True,
        )

        if result.returncode != 0:
            return False, None  # No remote tracking, assume OK

        parts = result.stdout.strip().split()
        if len(parts) != 2:
            return False, None  # Unexpected output, assume OK

        ahead, behind = map(int, parts)

        if behind > 0:
            return True, f"{target_branch} is {behind} commit(s) behind origin. Run: git checkout {target_branch} && git pull"

        return False, None

    except (OSError, subprocess.SubprocessError, ValueError) as exc:
        logger.warning(
            "Target divergence check failed for %s: %s",
            target_branch,
            exc,
        )
        return False, None  # Non-fatal: preserve merge UX if remote checks fail


def x_check_target_divergence__mutmut_49(target_branch: str, repo_root: Path) -> tuple[bool, str | None]:
    """Check if target branch has diverged from origin.

    Args:
        target_branch: Name of the target branch (e.g., "main")
        repo_root: Path to the repository root

    Returns:
        Tuple of (has_diverged, remediation_message)
        - has_diverged: True if local branch is behind origin
        - remediation_message: Instructions for fixing divergence
    """
    try:
        # Fetch latest refs (optional, may fail if offline)
        subprocess.run(
            ["git", "fetch", "origin", target_branch],
            cwd=str(repo_root),
            capture_output=True,
            check=False,
        )

        # Count commits ahead/behind
        result = subprocess.run(
            ["git", "rev-list", "--left-right", "--count", f"{target_branch}...origin/{target_branch}"],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )

        if result.returncode == 0:
            return False, None  # No remote tracking, assume OK

        parts = result.stdout.strip().split()
        if len(parts) != 2:
            return False, None  # Unexpected output, assume OK

        ahead, behind = map(int, parts)

        if behind > 0:
            return True, f"{target_branch} is {behind} commit(s) behind origin. Run: git checkout {target_branch} && git pull"

        return False, None

    except (OSError, subprocess.SubprocessError, ValueError) as exc:
        logger.warning(
            "Target divergence check failed for %s: %s",
            target_branch,
            exc,
        )
        return False, None  # Non-fatal: preserve merge UX if remote checks fail


def x_check_target_divergence__mutmut_50(target_branch: str, repo_root: Path) -> tuple[bool, str | None]:
    """Check if target branch has diverged from origin.

    Args:
        target_branch: Name of the target branch (e.g., "main")
        repo_root: Path to the repository root

    Returns:
        Tuple of (has_diverged, remediation_message)
        - has_diverged: True if local branch is behind origin
        - remediation_message: Instructions for fixing divergence
    """
    try:
        # Fetch latest refs (optional, may fail if offline)
        subprocess.run(
            ["git", "fetch", "origin", target_branch],
            cwd=str(repo_root),
            capture_output=True,
            check=False,
        )

        # Count commits ahead/behind
        result = subprocess.run(
            ["git", "rev-list", "--left-right", "--count", f"{target_branch}...origin/{target_branch}"],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )

        if result.returncode != 1:
            return False, None  # No remote tracking, assume OK

        parts = result.stdout.strip().split()
        if len(parts) != 2:
            return False, None  # Unexpected output, assume OK

        ahead, behind = map(int, parts)

        if behind > 0:
            return True, f"{target_branch} is {behind} commit(s) behind origin. Run: git checkout {target_branch} && git pull"

        return False, None

    except (OSError, subprocess.SubprocessError, ValueError) as exc:
        logger.warning(
            "Target divergence check failed for %s: %s",
            target_branch,
            exc,
        )
        return False, None  # Non-fatal: preserve merge UX if remote checks fail


def x_check_target_divergence__mutmut_51(target_branch: str, repo_root: Path) -> tuple[bool, str | None]:
    """Check if target branch has diverged from origin.

    Args:
        target_branch: Name of the target branch (e.g., "main")
        repo_root: Path to the repository root

    Returns:
        Tuple of (has_diverged, remediation_message)
        - has_diverged: True if local branch is behind origin
        - remediation_message: Instructions for fixing divergence
    """
    try:
        # Fetch latest refs (optional, may fail if offline)
        subprocess.run(
            ["git", "fetch", "origin", target_branch],
            cwd=str(repo_root),
            capture_output=True,
            check=False,
        )

        # Count commits ahead/behind
        result = subprocess.run(
            ["git", "rev-list", "--left-right", "--count", f"{target_branch}...origin/{target_branch}"],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )

        if result.returncode != 0:
            return True, None  # No remote tracking, assume OK

        parts = result.stdout.strip().split()
        if len(parts) != 2:
            return False, None  # Unexpected output, assume OK

        ahead, behind = map(int, parts)

        if behind > 0:
            return True, f"{target_branch} is {behind} commit(s) behind origin. Run: git checkout {target_branch} && git pull"

        return False, None

    except (OSError, subprocess.SubprocessError, ValueError) as exc:
        logger.warning(
            "Target divergence check failed for %s: %s",
            target_branch,
            exc,
        )
        return False, None  # Non-fatal: preserve merge UX if remote checks fail


def x_check_target_divergence__mutmut_52(target_branch: str, repo_root: Path) -> tuple[bool, str | None]:
    """Check if target branch has diverged from origin.

    Args:
        target_branch: Name of the target branch (e.g., "main")
        repo_root: Path to the repository root

    Returns:
        Tuple of (has_diverged, remediation_message)
        - has_diverged: True if local branch is behind origin
        - remediation_message: Instructions for fixing divergence
    """
    try:
        # Fetch latest refs (optional, may fail if offline)
        subprocess.run(
            ["git", "fetch", "origin", target_branch],
            cwd=str(repo_root),
            capture_output=True,
            check=False,
        )

        # Count commits ahead/behind
        result = subprocess.run(
            ["git", "rev-list", "--left-right", "--count", f"{target_branch}...origin/{target_branch}"],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )

        if result.returncode != 0:
            return False, None  # No remote tracking, assume OK

        parts = None
        if len(parts) != 2:
            return False, None  # Unexpected output, assume OK

        ahead, behind = map(int, parts)

        if behind > 0:
            return True, f"{target_branch} is {behind} commit(s) behind origin. Run: git checkout {target_branch} && git pull"

        return False, None

    except (OSError, subprocess.SubprocessError, ValueError) as exc:
        logger.warning(
            "Target divergence check failed for %s: %s",
            target_branch,
            exc,
        )
        return False, None  # Non-fatal: preserve merge UX if remote checks fail


def x_check_target_divergence__mutmut_53(target_branch: str, repo_root: Path) -> tuple[bool, str | None]:
    """Check if target branch has diverged from origin.

    Args:
        target_branch: Name of the target branch (e.g., "main")
        repo_root: Path to the repository root

    Returns:
        Tuple of (has_diverged, remediation_message)
        - has_diverged: True if local branch is behind origin
        - remediation_message: Instructions for fixing divergence
    """
    try:
        # Fetch latest refs (optional, may fail if offline)
        subprocess.run(
            ["git", "fetch", "origin", target_branch],
            cwd=str(repo_root),
            capture_output=True,
            check=False,
        )

        # Count commits ahead/behind
        result = subprocess.run(
            ["git", "rev-list", "--left-right", "--count", f"{target_branch}...origin/{target_branch}"],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )

        if result.returncode != 0:
            return False, None  # No remote tracking, assume OK

        parts = result.stdout.strip().split()
        if len(parts) == 2:
            return False, None  # Unexpected output, assume OK

        ahead, behind = map(int, parts)

        if behind > 0:
            return True, f"{target_branch} is {behind} commit(s) behind origin. Run: git checkout {target_branch} && git pull"

        return False, None

    except (OSError, subprocess.SubprocessError, ValueError) as exc:
        logger.warning(
            "Target divergence check failed for %s: %s",
            target_branch,
            exc,
        )
        return False, None  # Non-fatal: preserve merge UX if remote checks fail


def x_check_target_divergence__mutmut_54(target_branch: str, repo_root: Path) -> tuple[bool, str | None]:
    """Check if target branch has diverged from origin.

    Args:
        target_branch: Name of the target branch (e.g., "main")
        repo_root: Path to the repository root

    Returns:
        Tuple of (has_diverged, remediation_message)
        - has_diverged: True if local branch is behind origin
        - remediation_message: Instructions for fixing divergence
    """
    try:
        # Fetch latest refs (optional, may fail if offline)
        subprocess.run(
            ["git", "fetch", "origin", target_branch],
            cwd=str(repo_root),
            capture_output=True,
            check=False,
        )

        # Count commits ahead/behind
        result = subprocess.run(
            ["git", "rev-list", "--left-right", "--count", f"{target_branch}...origin/{target_branch}"],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )

        if result.returncode != 0:
            return False, None  # No remote tracking, assume OK

        parts = result.stdout.strip().split()
        if len(parts) != 3:
            return False, None  # Unexpected output, assume OK

        ahead, behind = map(int, parts)

        if behind > 0:
            return True, f"{target_branch} is {behind} commit(s) behind origin. Run: git checkout {target_branch} && git pull"

        return False, None

    except (OSError, subprocess.SubprocessError, ValueError) as exc:
        logger.warning(
            "Target divergence check failed for %s: %s",
            target_branch,
            exc,
        )
        return False, None  # Non-fatal: preserve merge UX if remote checks fail


def x_check_target_divergence__mutmut_55(target_branch: str, repo_root: Path) -> tuple[bool, str | None]:
    """Check if target branch has diverged from origin.

    Args:
        target_branch: Name of the target branch (e.g., "main")
        repo_root: Path to the repository root

    Returns:
        Tuple of (has_diverged, remediation_message)
        - has_diverged: True if local branch is behind origin
        - remediation_message: Instructions for fixing divergence
    """
    try:
        # Fetch latest refs (optional, may fail if offline)
        subprocess.run(
            ["git", "fetch", "origin", target_branch],
            cwd=str(repo_root),
            capture_output=True,
            check=False,
        )

        # Count commits ahead/behind
        result = subprocess.run(
            ["git", "rev-list", "--left-right", "--count", f"{target_branch}...origin/{target_branch}"],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )

        if result.returncode != 0:
            return False, None  # No remote tracking, assume OK

        parts = result.stdout.strip().split()
        if len(parts) != 2:
            return True, None  # Unexpected output, assume OK

        ahead, behind = map(int, parts)

        if behind > 0:
            return True, f"{target_branch} is {behind} commit(s) behind origin. Run: git checkout {target_branch} && git pull"

        return False, None

    except (OSError, subprocess.SubprocessError, ValueError) as exc:
        logger.warning(
            "Target divergence check failed for %s: %s",
            target_branch,
            exc,
        )
        return False, None  # Non-fatal: preserve merge UX if remote checks fail


def x_check_target_divergence__mutmut_56(target_branch: str, repo_root: Path) -> tuple[bool, str | None]:
    """Check if target branch has diverged from origin.

    Args:
        target_branch: Name of the target branch (e.g., "main")
        repo_root: Path to the repository root

    Returns:
        Tuple of (has_diverged, remediation_message)
        - has_diverged: True if local branch is behind origin
        - remediation_message: Instructions for fixing divergence
    """
    try:
        # Fetch latest refs (optional, may fail if offline)
        subprocess.run(
            ["git", "fetch", "origin", target_branch],
            cwd=str(repo_root),
            capture_output=True,
            check=False,
        )

        # Count commits ahead/behind
        result = subprocess.run(
            ["git", "rev-list", "--left-right", "--count", f"{target_branch}...origin/{target_branch}"],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )

        if result.returncode != 0:
            return False, None  # No remote tracking, assume OK

        parts = result.stdout.strip().split()
        if len(parts) != 2:
            return False, None  # Unexpected output, assume OK

        ahead, behind = None

        if behind > 0:
            return True, f"{target_branch} is {behind} commit(s) behind origin. Run: git checkout {target_branch} && git pull"

        return False, None

    except (OSError, subprocess.SubprocessError, ValueError) as exc:
        logger.warning(
            "Target divergence check failed for %s: %s",
            target_branch,
            exc,
        )
        return False, None  # Non-fatal: preserve merge UX if remote checks fail


def x_check_target_divergence__mutmut_57(target_branch: str, repo_root: Path) -> tuple[bool, str | None]:
    """Check if target branch has diverged from origin.

    Args:
        target_branch: Name of the target branch (e.g., "main")
        repo_root: Path to the repository root

    Returns:
        Tuple of (has_diverged, remediation_message)
        - has_diverged: True if local branch is behind origin
        - remediation_message: Instructions for fixing divergence
    """
    try:
        # Fetch latest refs (optional, may fail if offline)
        subprocess.run(
            ["git", "fetch", "origin", target_branch],
            cwd=str(repo_root),
            capture_output=True,
            check=False,
        )

        # Count commits ahead/behind
        result = subprocess.run(
            ["git", "rev-list", "--left-right", "--count", f"{target_branch}...origin/{target_branch}"],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )

        if result.returncode != 0:
            return False, None  # No remote tracking, assume OK

        parts = result.stdout.strip().split()
        if len(parts) != 2:
            return False, None  # Unexpected output, assume OK

        ahead, behind = map(None, parts)

        if behind > 0:
            return True, f"{target_branch} is {behind} commit(s) behind origin. Run: git checkout {target_branch} && git pull"

        return False, None

    except (OSError, subprocess.SubprocessError, ValueError) as exc:
        logger.warning(
            "Target divergence check failed for %s: %s",
            target_branch,
            exc,
        )
        return False, None  # Non-fatal: preserve merge UX if remote checks fail


def x_check_target_divergence__mutmut_58(target_branch: str, repo_root: Path) -> tuple[bool, str | None]:
    """Check if target branch has diverged from origin.

    Args:
        target_branch: Name of the target branch (e.g., "main")
        repo_root: Path to the repository root

    Returns:
        Tuple of (has_diverged, remediation_message)
        - has_diverged: True if local branch is behind origin
        - remediation_message: Instructions for fixing divergence
    """
    try:
        # Fetch latest refs (optional, may fail if offline)
        subprocess.run(
            ["git", "fetch", "origin", target_branch],
            cwd=str(repo_root),
            capture_output=True,
            check=False,
        )

        # Count commits ahead/behind
        result = subprocess.run(
            ["git", "rev-list", "--left-right", "--count", f"{target_branch}...origin/{target_branch}"],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )

        if result.returncode != 0:
            return False, None  # No remote tracking, assume OK

        parts = result.stdout.strip().split()
        if len(parts) != 2:
            return False, None  # Unexpected output, assume OK

        ahead, behind = map(int, None)

        if behind > 0:
            return True, f"{target_branch} is {behind} commit(s) behind origin. Run: git checkout {target_branch} && git pull"

        return False, None

    except (OSError, subprocess.SubprocessError, ValueError) as exc:
        logger.warning(
            "Target divergence check failed for %s: %s",
            target_branch,
            exc,
        )
        return False, None  # Non-fatal: preserve merge UX if remote checks fail


def x_check_target_divergence__mutmut_59(target_branch: str, repo_root: Path) -> tuple[bool, str | None]:
    """Check if target branch has diverged from origin.

    Args:
        target_branch: Name of the target branch (e.g., "main")
        repo_root: Path to the repository root

    Returns:
        Tuple of (has_diverged, remediation_message)
        - has_diverged: True if local branch is behind origin
        - remediation_message: Instructions for fixing divergence
    """
    try:
        # Fetch latest refs (optional, may fail if offline)
        subprocess.run(
            ["git", "fetch", "origin", target_branch],
            cwd=str(repo_root),
            capture_output=True,
            check=False,
        )

        # Count commits ahead/behind
        result = subprocess.run(
            ["git", "rev-list", "--left-right", "--count", f"{target_branch}...origin/{target_branch}"],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )

        if result.returncode != 0:
            return False, None  # No remote tracking, assume OK

        parts = result.stdout.strip().split()
        if len(parts) != 2:
            return False, None  # Unexpected output, assume OK

        ahead, behind = map(parts)

        if behind > 0:
            return True, f"{target_branch} is {behind} commit(s) behind origin. Run: git checkout {target_branch} && git pull"

        return False, None

    except (OSError, subprocess.SubprocessError, ValueError) as exc:
        logger.warning(
            "Target divergence check failed for %s: %s",
            target_branch,
            exc,
        )
        return False, None  # Non-fatal: preserve merge UX if remote checks fail


def x_check_target_divergence__mutmut_60(target_branch: str, repo_root: Path) -> tuple[bool, str | None]:
    """Check if target branch has diverged from origin.

    Args:
        target_branch: Name of the target branch (e.g., "main")
        repo_root: Path to the repository root

    Returns:
        Tuple of (has_diverged, remediation_message)
        - has_diverged: True if local branch is behind origin
        - remediation_message: Instructions for fixing divergence
    """
    try:
        # Fetch latest refs (optional, may fail if offline)
        subprocess.run(
            ["git", "fetch", "origin", target_branch],
            cwd=str(repo_root),
            capture_output=True,
            check=False,
        )

        # Count commits ahead/behind
        result = subprocess.run(
            ["git", "rev-list", "--left-right", "--count", f"{target_branch}...origin/{target_branch}"],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )

        if result.returncode != 0:
            return False, None  # No remote tracking, assume OK

        parts = result.stdout.strip().split()
        if len(parts) != 2:
            return False, None  # Unexpected output, assume OK

        ahead, behind = map(int, )

        if behind > 0:
            return True, f"{target_branch} is {behind} commit(s) behind origin. Run: git checkout {target_branch} && git pull"

        return False, None

    except (OSError, subprocess.SubprocessError, ValueError) as exc:
        logger.warning(
            "Target divergence check failed for %s: %s",
            target_branch,
            exc,
        )
        return False, None  # Non-fatal: preserve merge UX if remote checks fail


def x_check_target_divergence__mutmut_61(target_branch: str, repo_root: Path) -> tuple[bool, str | None]:
    """Check if target branch has diverged from origin.

    Args:
        target_branch: Name of the target branch (e.g., "main")
        repo_root: Path to the repository root

    Returns:
        Tuple of (has_diverged, remediation_message)
        - has_diverged: True if local branch is behind origin
        - remediation_message: Instructions for fixing divergence
    """
    try:
        # Fetch latest refs (optional, may fail if offline)
        subprocess.run(
            ["git", "fetch", "origin", target_branch],
            cwd=str(repo_root),
            capture_output=True,
            check=False,
        )

        # Count commits ahead/behind
        result = subprocess.run(
            ["git", "rev-list", "--left-right", "--count", f"{target_branch}...origin/{target_branch}"],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )

        if result.returncode != 0:
            return False, None  # No remote tracking, assume OK

        parts = result.stdout.strip().split()
        if len(parts) != 2:
            return False, None  # Unexpected output, assume OK

        ahead, behind = map(int, parts)

        if behind >= 0:
            return True, f"{target_branch} is {behind} commit(s) behind origin. Run: git checkout {target_branch} && git pull"

        return False, None

    except (OSError, subprocess.SubprocessError, ValueError) as exc:
        logger.warning(
            "Target divergence check failed for %s: %s",
            target_branch,
            exc,
        )
        return False, None  # Non-fatal: preserve merge UX if remote checks fail


def x_check_target_divergence__mutmut_62(target_branch: str, repo_root: Path) -> tuple[bool, str | None]:
    """Check if target branch has diverged from origin.

    Args:
        target_branch: Name of the target branch (e.g., "main")
        repo_root: Path to the repository root

    Returns:
        Tuple of (has_diverged, remediation_message)
        - has_diverged: True if local branch is behind origin
        - remediation_message: Instructions for fixing divergence
    """
    try:
        # Fetch latest refs (optional, may fail if offline)
        subprocess.run(
            ["git", "fetch", "origin", target_branch],
            cwd=str(repo_root),
            capture_output=True,
            check=False,
        )

        # Count commits ahead/behind
        result = subprocess.run(
            ["git", "rev-list", "--left-right", "--count", f"{target_branch}...origin/{target_branch}"],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )

        if result.returncode != 0:
            return False, None  # No remote tracking, assume OK

        parts = result.stdout.strip().split()
        if len(parts) != 2:
            return False, None  # Unexpected output, assume OK

        ahead, behind = map(int, parts)

        if behind > 1:
            return True, f"{target_branch} is {behind} commit(s) behind origin. Run: git checkout {target_branch} && git pull"

        return False, None

    except (OSError, subprocess.SubprocessError, ValueError) as exc:
        logger.warning(
            "Target divergence check failed for %s: %s",
            target_branch,
            exc,
        )
        return False, None  # Non-fatal: preserve merge UX if remote checks fail


def x_check_target_divergence__mutmut_63(target_branch: str, repo_root: Path) -> tuple[bool, str | None]:
    """Check if target branch has diverged from origin.

    Args:
        target_branch: Name of the target branch (e.g., "main")
        repo_root: Path to the repository root

    Returns:
        Tuple of (has_diverged, remediation_message)
        - has_diverged: True if local branch is behind origin
        - remediation_message: Instructions for fixing divergence
    """
    try:
        # Fetch latest refs (optional, may fail if offline)
        subprocess.run(
            ["git", "fetch", "origin", target_branch],
            cwd=str(repo_root),
            capture_output=True,
            check=False,
        )

        # Count commits ahead/behind
        result = subprocess.run(
            ["git", "rev-list", "--left-right", "--count", f"{target_branch}...origin/{target_branch}"],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )

        if result.returncode != 0:
            return False, None  # No remote tracking, assume OK

        parts = result.stdout.strip().split()
        if len(parts) != 2:
            return False, None  # Unexpected output, assume OK

        ahead, behind = map(int, parts)

        if behind > 0:
            return False, f"{target_branch} is {behind} commit(s) behind origin. Run: git checkout {target_branch} && git pull"

        return False, None

    except (OSError, subprocess.SubprocessError, ValueError) as exc:
        logger.warning(
            "Target divergence check failed for %s: %s",
            target_branch,
            exc,
        )
        return False, None  # Non-fatal: preserve merge UX if remote checks fail


def x_check_target_divergence__mutmut_64(target_branch: str, repo_root: Path) -> tuple[bool, str | None]:
    """Check if target branch has diverged from origin.

    Args:
        target_branch: Name of the target branch (e.g., "main")
        repo_root: Path to the repository root

    Returns:
        Tuple of (has_diverged, remediation_message)
        - has_diverged: True if local branch is behind origin
        - remediation_message: Instructions for fixing divergence
    """
    try:
        # Fetch latest refs (optional, may fail if offline)
        subprocess.run(
            ["git", "fetch", "origin", target_branch],
            cwd=str(repo_root),
            capture_output=True,
            check=False,
        )

        # Count commits ahead/behind
        result = subprocess.run(
            ["git", "rev-list", "--left-right", "--count", f"{target_branch}...origin/{target_branch}"],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )

        if result.returncode != 0:
            return False, None  # No remote tracking, assume OK

        parts = result.stdout.strip().split()
        if len(parts) != 2:
            return False, None  # Unexpected output, assume OK

        ahead, behind = map(int, parts)

        if behind > 0:
            return True, f"{target_branch} is {behind} commit(s) behind origin. Run: git checkout {target_branch} && git pull"

        return True, None

    except (OSError, subprocess.SubprocessError, ValueError) as exc:
        logger.warning(
            "Target divergence check failed for %s: %s",
            target_branch,
            exc,
        )
        return False, None  # Non-fatal: preserve merge UX if remote checks fail


def x_check_target_divergence__mutmut_65(target_branch: str, repo_root: Path) -> tuple[bool, str | None]:
    """Check if target branch has diverged from origin.

    Args:
        target_branch: Name of the target branch (e.g., "main")
        repo_root: Path to the repository root

    Returns:
        Tuple of (has_diverged, remediation_message)
        - has_diverged: True if local branch is behind origin
        - remediation_message: Instructions for fixing divergence
    """
    try:
        # Fetch latest refs (optional, may fail if offline)
        subprocess.run(
            ["git", "fetch", "origin", target_branch],
            cwd=str(repo_root),
            capture_output=True,
            check=False,
        )

        # Count commits ahead/behind
        result = subprocess.run(
            ["git", "rev-list", "--left-right", "--count", f"{target_branch}...origin/{target_branch}"],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )

        if result.returncode != 0:
            return False, None  # No remote tracking, assume OK

        parts = result.stdout.strip().split()
        if len(parts) != 2:
            return False, None  # Unexpected output, assume OK

        ahead, behind = map(int, parts)

        if behind > 0:
            return True, f"{target_branch} is {behind} commit(s) behind origin. Run: git checkout {target_branch} && git pull"

        return False, None

    except (OSError, subprocess.SubprocessError, ValueError) as exc:
        logger.warning(
            None,
            target_branch,
            exc,
        )
        return False, None  # Non-fatal: preserve merge UX if remote checks fail


def x_check_target_divergence__mutmut_66(target_branch: str, repo_root: Path) -> tuple[bool, str | None]:
    """Check if target branch has diverged from origin.

    Args:
        target_branch: Name of the target branch (e.g., "main")
        repo_root: Path to the repository root

    Returns:
        Tuple of (has_diverged, remediation_message)
        - has_diverged: True if local branch is behind origin
        - remediation_message: Instructions for fixing divergence
    """
    try:
        # Fetch latest refs (optional, may fail if offline)
        subprocess.run(
            ["git", "fetch", "origin", target_branch],
            cwd=str(repo_root),
            capture_output=True,
            check=False,
        )

        # Count commits ahead/behind
        result = subprocess.run(
            ["git", "rev-list", "--left-right", "--count", f"{target_branch}...origin/{target_branch}"],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )

        if result.returncode != 0:
            return False, None  # No remote tracking, assume OK

        parts = result.stdout.strip().split()
        if len(parts) != 2:
            return False, None  # Unexpected output, assume OK

        ahead, behind = map(int, parts)

        if behind > 0:
            return True, f"{target_branch} is {behind} commit(s) behind origin. Run: git checkout {target_branch} && git pull"

        return False, None

    except (OSError, subprocess.SubprocessError, ValueError) as exc:
        logger.warning(
            "Target divergence check failed for %s: %s",
            None,
            exc,
        )
        return False, None  # Non-fatal: preserve merge UX if remote checks fail


def x_check_target_divergence__mutmut_67(target_branch: str, repo_root: Path) -> tuple[bool, str | None]:
    """Check if target branch has diverged from origin.

    Args:
        target_branch: Name of the target branch (e.g., "main")
        repo_root: Path to the repository root

    Returns:
        Tuple of (has_diverged, remediation_message)
        - has_diverged: True if local branch is behind origin
        - remediation_message: Instructions for fixing divergence
    """
    try:
        # Fetch latest refs (optional, may fail if offline)
        subprocess.run(
            ["git", "fetch", "origin", target_branch],
            cwd=str(repo_root),
            capture_output=True,
            check=False,
        )

        # Count commits ahead/behind
        result = subprocess.run(
            ["git", "rev-list", "--left-right", "--count", f"{target_branch}...origin/{target_branch}"],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )

        if result.returncode != 0:
            return False, None  # No remote tracking, assume OK

        parts = result.stdout.strip().split()
        if len(parts) != 2:
            return False, None  # Unexpected output, assume OK

        ahead, behind = map(int, parts)

        if behind > 0:
            return True, f"{target_branch} is {behind} commit(s) behind origin. Run: git checkout {target_branch} && git pull"

        return False, None

    except (OSError, subprocess.SubprocessError, ValueError) as exc:
        logger.warning(
            "Target divergence check failed for %s: %s",
            target_branch,
            None,
        )
        return False, None  # Non-fatal: preserve merge UX if remote checks fail


def x_check_target_divergence__mutmut_68(target_branch: str, repo_root: Path) -> tuple[bool, str | None]:
    """Check if target branch has diverged from origin.

    Args:
        target_branch: Name of the target branch (e.g., "main")
        repo_root: Path to the repository root

    Returns:
        Tuple of (has_diverged, remediation_message)
        - has_diverged: True if local branch is behind origin
        - remediation_message: Instructions for fixing divergence
    """
    try:
        # Fetch latest refs (optional, may fail if offline)
        subprocess.run(
            ["git", "fetch", "origin", target_branch],
            cwd=str(repo_root),
            capture_output=True,
            check=False,
        )

        # Count commits ahead/behind
        result = subprocess.run(
            ["git", "rev-list", "--left-right", "--count", f"{target_branch}...origin/{target_branch}"],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )

        if result.returncode != 0:
            return False, None  # No remote tracking, assume OK

        parts = result.stdout.strip().split()
        if len(parts) != 2:
            return False, None  # Unexpected output, assume OK

        ahead, behind = map(int, parts)

        if behind > 0:
            return True, f"{target_branch} is {behind} commit(s) behind origin. Run: git checkout {target_branch} && git pull"

        return False, None

    except (OSError, subprocess.SubprocessError, ValueError) as exc:
        logger.warning(
            target_branch,
            exc,
        )
        return False, None  # Non-fatal: preserve merge UX if remote checks fail


def x_check_target_divergence__mutmut_69(target_branch: str, repo_root: Path) -> tuple[bool, str | None]:
    """Check if target branch has diverged from origin.

    Args:
        target_branch: Name of the target branch (e.g., "main")
        repo_root: Path to the repository root

    Returns:
        Tuple of (has_diverged, remediation_message)
        - has_diverged: True if local branch is behind origin
        - remediation_message: Instructions for fixing divergence
    """
    try:
        # Fetch latest refs (optional, may fail if offline)
        subprocess.run(
            ["git", "fetch", "origin", target_branch],
            cwd=str(repo_root),
            capture_output=True,
            check=False,
        )

        # Count commits ahead/behind
        result = subprocess.run(
            ["git", "rev-list", "--left-right", "--count", f"{target_branch}...origin/{target_branch}"],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )

        if result.returncode != 0:
            return False, None  # No remote tracking, assume OK

        parts = result.stdout.strip().split()
        if len(parts) != 2:
            return False, None  # Unexpected output, assume OK

        ahead, behind = map(int, parts)

        if behind > 0:
            return True, f"{target_branch} is {behind} commit(s) behind origin. Run: git checkout {target_branch} && git pull"

        return False, None

    except (OSError, subprocess.SubprocessError, ValueError) as exc:
        logger.warning(
            "Target divergence check failed for %s: %s",
            exc,
        )
        return False, None  # Non-fatal: preserve merge UX if remote checks fail


def x_check_target_divergence__mutmut_70(target_branch: str, repo_root: Path) -> tuple[bool, str | None]:
    """Check if target branch has diverged from origin.

    Args:
        target_branch: Name of the target branch (e.g., "main")
        repo_root: Path to the repository root

    Returns:
        Tuple of (has_diverged, remediation_message)
        - has_diverged: True if local branch is behind origin
        - remediation_message: Instructions for fixing divergence
    """
    try:
        # Fetch latest refs (optional, may fail if offline)
        subprocess.run(
            ["git", "fetch", "origin", target_branch],
            cwd=str(repo_root),
            capture_output=True,
            check=False,
        )

        # Count commits ahead/behind
        result = subprocess.run(
            ["git", "rev-list", "--left-right", "--count", f"{target_branch}...origin/{target_branch}"],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )

        if result.returncode != 0:
            return False, None  # No remote tracking, assume OK

        parts = result.stdout.strip().split()
        if len(parts) != 2:
            return False, None  # Unexpected output, assume OK

        ahead, behind = map(int, parts)

        if behind > 0:
            return True, f"{target_branch} is {behind} commit(s) behind origin. Run: git checkout {target_branch} && git pull"

        return False, None

    except (OSError, subprocess.SubprocessError, ValueError) as exc:
        logger.warning(
            "Target divergence check failed for %s: %s",
            target_branch,
            )
        return False, None  # Non-fatal: preserve merge UX if remote checks fail


def x_check_target_divergence__mutmut_71(target_branch: str, repo_root: Path) -> tuple[bool, str | None]:
    """Check if target branch has diverged from origin.

    Args:
        target_branch: Name of the target branch (e.g., "main")
        repo_root: Path to the repository root

    Returns:
        Tuple of (has_diverged, remediation_message)
        - has_diverged: True if local branch is behind origin
        - remediation_message: Instructions for fixing divergence
    """
    try:
        # Fetch latest refs (optional, may fail if offline)
        subprocess.run(
            ["git", "fetch", "origin", target_branch],
            cwd=str(repo_root),
            capture_output=True,
            check=False,
        )

        # Count commits ahead/behind
        result = subprocess.run(
            ["git", "rev-list", "--left-right", "--count", f"{target_branch}...origin/{target_branch}"],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )

        if result.returncode != 0:
            return False, None  # No remote tracking, assume OK

        parts = result.stdout.strip().split()
        if len(parts) != 2:
            return False, None  # Unexpected output, assume OK

        ahead, behind = map(int, parts)

        if behind > 0:
            return True, f"{target_branch} is {behind} commit(s) behind origin. Run: git checkout {target_branch} && git pull"

        return False, None

    except (OSError, subprocess.SubprocessError, ValueError) as exc:
        logger.warning(
            "XXTarget divergence check failed for %s: %sXX",
            target_branch,
            exc,
        )
        return False, None  # Non-fatal: preserve merge UX if remote checks fail


def x_check_target_divergence__mutmut_72(target_branch: str, repo_root: Path) -> tuple[bool, str | None]:
    """Check if target branch has diverged from origin.

    Args:
        target_branch: Name of the target branch (e.g., "main")
        repo_root: Path to the repository root

    Returns:
        Tuple of (has_diverged, remediation_message)
        - has_diverged: True if local branch is behind origin
        - remediation_message: Instructions for fixing divergence
    """
    try:
        # Fetch latest refs (optional, may fail if offline)
        subprocess.run(
            ["git", "fetch", "origin", target_branch],
            cwd=str(repo_root),
            capture_output=True,
            check=False,
        )

        # Count commits ahead/behind
        result = subprocess.run(
            ["git", "rev-list", "--left-right", "--count", f"{target_branch}...origin/{target_branch}"],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )

        if result.returncode != 0:
            return False, None  # No remote tracking, assume OK

        parts = result.stdout.strip().split()
        if len(parts) != 2:
            return False, None  # Unexpected output, assume OK

        ahead, behind = map(int, parts)

        if behind > 0:
            return True, f"{target_branch} is {behind} commit(s) behind origin. Run: git checkout {target_branch} && git pull"

        return False, None

    except (OSError, subprocess.SubprocessError, ValueError) as exc:
        logger.warning(
            "target divergence check failed for %s: %s",
            target_branch,
            exc,
        )
        return False, None  # Non-fatal: preserve merge UX if remote checks fail


def x_check_target_divergence__mutmut_73(target_branch: str, repo_root: Path) -> tuple[bool, str | None]:
    """Check if target branch has diverged from origin.

    Args:
        target_branch: Name of the target branch (e.g., "main")
        repo_root: Path to the repository root

    Returns:
        Tuple of (has_diverged, remediation_message)
        - has_diverged: True if local branch is behind origin
        - remediation_message: Instructions for fixing divergence
    """
    try:
        # Fetch latest refs (optional, may fail if offline)
        subprocess.run(
            ["git", "fetch", "origin", target_branch],
            cwd=str(repo_root),
            capture_output=True,
            check=False,
        )

        # Count commits ahead/behind
        result = subprocess.run(
            ["git", "rev-list", "--left-right", "--count", f"{target_branch}...origin/{target_branch}"],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )

        if result.returncode != 0:
            return False, None  # No remote tracking, assume OK

        parts = result.stdout.strip().split()
        if len(parts) != 2:
            return False, None  # Unexpected output, assume OK

        ahead, behind = map(int, parts)

        if behind > 0:
            return True, f"{target_branch} is {behind} commit(s) behind origin. Run: git checkout {target_branch} && git pull"

        return False, None

    except (OSError, subprocess.SubprocessError, ValueError) as exc:
        logger.warning(
            "TARGET DIVERGENCE CHECK FAILED FOR %S: %S",
            target_branch,
            exc,
        )
        return False, None  # Non-fatal: preserve merge UX if remote checks fail


def x_check_target_divergence__mutmut_74(target_branch: str, repo_root: Path) -> tuple[bool, str | None]:
    """Check if target branch has diverged from origin.

    Args:
        target_branch: Name of the target branch (e.g., "main")
        repo_root: Path to the repository root

    Returns:
        Tuple of (has_diverged, remediation_message)
        - has_diverged: True if local branch is behind origin
        - remediation_message: Instructions for fixing divergence
    """
    try:
        # Fetch latest refs (optional, may fail if offline)
        subprocess.run(
            ["git", "fetch", "origin", target_branch],
            cwd=str(repo_root),
            capture_output=True,
            check=False,
        )

        # Count commits ahead/behind
        result = subprocess.run(
            ["git", "rev-list", "--left-right", "--count", f"{target_branch}...origin/{target_branch}"],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )

        if result.returncode != 0:
            return False, None  # No remote tracking, assume OK

        parts = result.stdout.strip().split()
        if len(parts) != 2:
            return False, None  # Unexpected output, assume OK

        ahead, behind = map(int, parts)

        if behind > 0:
            return True, f"{target_branch} is {behind} commit(s) behind origin. Run: git checkout {target_branch} && git pull"

        return False, None

    except (OSError, subprocess.SubprocessError, ValueError) as exc:
        logger.warning(
            "Target divergence check failed for %s: %s",
            target_branch,
            exc,
        )
        return True, None  # Non-fatal: preserve merge UX if remote checks fail

x_check_target_divergence__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_check_target_divergence__mutmut_1': x_check_target_divergence__mutmut_1, 
    'x_check_target_divergence__mutmut_2': x_check_target_divergence__mutmut_2, 
    'x_check_target_divergence__mutmut_3': x_check_target_divergence__mutmut_3, 
    'x_check_target_divergence__mutmut_4': x_check_target_divergence__mutmut_4, 
    'x_check_target_divergence__mutmut_5': x_check_target_divergence__mutmut_5, 
    'x_check_target_divergence__mutmut_6': x_check_target_divergence__mutmut_6, 
    'x_check_target_divergence__mutmut_7': x_check_target_divergence__mutmut_7, 
    'x_check_target_divergence__mutmut_8': x_check_target_divergence__mutmut_8, 
    'x_check_target_divergence__mutmut_9': x_check_target_divergence__mutmut_9, 
    'x_check_target_divergence__mutmut_10': x_check_target_divergence__mutmut_10, 
    'x_check_target_divergence__mutmut_11': x_check_target_divergence__mutmut_11, 
    'x_check_target_divergence__mutmut_12': x_check_target_divergence__mutmut_12, 
    'x_check_target_divergence__mutmut_13': x_check_target_divergence__mutmut_13, 
    'x_check_target_divergence__mutmut_14': x_check_target_divergence__mutmut_14, 
    'x_check_target_divergence__mutmut_15': x_check_target_divergence__mutmut_15, 
    'x_check_target_divergence__mutmut_16': x_check_target_divergence__mutmut_16, 
    'x_check_target_divergence__mutmut_17': x_check_target_divergence__mutmut_17, 
    'x_check_target_divergence__mutmut_18': x_check_target_divergence__mutmut_18, 
    'x_check_target_divergence__mutmut_19': x_check_target_divergence__mutmut_19, 
    'x_check_target_divergence__mutmut_20': x_check_target_divergence__mutmut_20, 
    'x_check_target_divergence__mutmut_21': x_check_target_divergence__mutmut_21, 
    'x_check_target_divergence__mutmut_22': x_check_target_divergence__mutmut_22, 
    'x_check_target_divergence__mutmut_23': x_check_target_divergence__mutmut_23, 
    'x_check_target_divergence__mutmut_24': x_check_target_divergence__mutmut_24, 
    'x_check_target_divergence__mutmut_25': x_check_target_divergence__mutmut_25, 
    'x_check_target_divergence__mutmut_26': x_check_target_divergence__mutmut_26, 
    'x_check_target_divergence__mutmut_27': x_check_target_divergence__mutmut_27, 
    'x_check_target_divergence__mutmut_28': x_check_target_divergence__mutmut_28, 
    'x_check_target_divergence__mutmut_29': x_check_target_divergence__mutmut_29, 
    'x_check_target_divergence__mutmut_30': x_check_target_divergence__mutmut_30, 
    'x_check_target_divergence__mutmut_31': x_check_target_divergence__mutmut_31, 
    'x_check_target_divergence__mutmut_32': x_check_target_divergence__mutmut_32, 
    'x_check_target_divergence__mutmut_33': x_check_target_divergence__mutmut_33, 
    'x_check_target_divergence__mutmut_34': x_check_target_divergence__mutmut_34, 
    'x_check_target_divergence__mutmut_35': x_check_target_divergence__mutmut_35, 
    'x_check_target_divergence__mutmut_36': x_check_target_divergence__mutmut_36, 
    'x_check_target_divergence__mutmut_37': x_check_target_divergence__mutmut_37, 
    'x_check_target_divergence__mutmut_38': x_check_target_divergence__mutmut_38, 
    'x_check_target_divergence__mutmut_39': x_check_target_divergence__mutmut_39, 
    'x_check_target_divergence__mutmut_40': x_check_target_divergence__mutmut_40, 
    'x_check_target_divergence__mutmut_41': x_check_target_divergence__mutmut_41, 
    'x_check_target_divergence__mutmut_42': x_check_target_divergence__mutmut_42, 
    'x_check_target_divergence__mutmut_43': x_check_target_divergence__mutmut_43, 
    'x_check_target_divergence__mutmut_44': x_check_target_divergence__mutmut_44, 
    'x_check_target_divergence__mutmut_45': x_check_target_divergence__mutmut_45, 
    'x_check_target_divergence__mutmut_46': x_check_target_divergence__mutmut_46, 
    'x_check_target_divergence__mutmut_47': x_check_target_divergence__mutmut_47, 
    'x_check_target_divergence__mutmut_48': x_check_target_divergence__mutmut_48, 
    'x_check_target_divergence__mutmut_49': x_check_target_divergence__mutmut_49, 
    'x_check_target_divergence__mutmut_50': x_check_target_divergence__mutmut_50, 
    'x_check_target_divergence__mutmut_51': x_check_target_divergence__mutmut_51, 
    'x_check_target_divergence__mutmut_52': x_check_target_divergence__mutmut_52, 
    'x_check_target_divergence__mutmut_53': x_check_target_divergence__mutmut_53, 
    'x_check_target_divergence__mutmut_54': x_check_target_divergence__mutmut_54, 
    'x_check_target_divergence__mutmut_55': x_check_target_divergence__mutmut_55, 
    'x_check_target_divergence__mutmut_56': x_check_target_divergence__mutmut_56, 
    'x_check_target_divergence__mutmut_57': x_check_target_divergence__mutmut_57, 
    'x_check_target_divergence__mutmut_58': x_check_target_divergence__mutmut_58, 
    'x_check_target_divergence__mutmut_59': x_check_target_divergence__mutmut_59, 
    'x_check_target_divergence__mutmut_60': x_check_target_divergence__mutmut_60, 
    'x_check_target_divergence__mutmut_61': x_check_target_divergence__mutmut_61, 
    'x_check_target_divergence__mutmut_62': x_check_target_divergence__mutmut_62, 
    'x_check_target_divergence__mutmut_63': x_check_target_divergence__mutmut_63, 
    'x_check_target_divergence__mutmut_64': x_check_target_divergence__mutmut_64, 
    'x_check_target_divergence__mutmut_65': x_check_target_divergence__mutmut_65, 
    'x_check_target_divergence__mutmut_66': x_check_target_divergence__mutmut_66, 
    'x_check_target_divergence__mutmut_67': x_check_target_divergence__mutmut_67, 
    'x_check_target_divergence__mutmut_68': x_check_target_divergence__mutmut_68, 
    'x_check_target_divergence__mutmut_69': x_check_target_divergence__mutmut_69, 
    'x_check_target_divergence__mutmut_70': x_check_target_divergence__mutmut_70, 
    'x_check_target_divergence__mutmut_71': x_check_target_divergence__mutmut_71, 
    'x_check_target_divergence__mutmut_72': x_check_target_divergence__mutmut_72, 
    'x_check_target_divergence__mutmut_73': x_check_target_divergence__mutmut_73, 
    'x_check_target_divergence__mutmut_74': x_check_target_divergence__mutmut_74
}
x_check_target_divergence__mutmut_orig.__name__ = 'x_check_target_divergence'


def _wp_lane_from_feature(repo_root: Path, feature_slug: str, wp_id: str) -> str | None:
    args = [repo_root, feature_slug, wp_id]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x__wp_lane_from_feature__mutmut_orig, x__wp_lane_from_feature__mutmut_mutants, args, kwargs, None)


def x__wp_lane_from_feature__mutmut_orig(repo_root: Path, feature_slug: str, wp_id: str) -> str | None:
    """Read lane value for a WP prompt file from kitty-specs."""
    tasks_dir = repo_root / KITTY_SPECS_DIR / feature_slug / "tasks"
    if not tasks_dir.exists():
        return None

    candidates = sorted(tasks_dir.glob(f"{wp_id}*.md"))
    if not candidates:
        return None

    content = candidates[0].read_text(encoding="utf-8", errors="replace")
    if not content.startswith("---"):
        return None

    match = re.search(r"^lane:\s*['\"]?([^'\"\n]+)['\"]?\s*$", content, re.MULTILINE)
    if not match:
        return None
    return match.group(1).strip().lower()


def x__wp_lane_from_feature__mutmut_1(repo_root: Path, feature_slug: str, wp_id: str) -> str | None:
    """Read lane value for a WP prompt file from kitty-specs."""
    tasks_dir = None
    if not tasks_dir.exists():
        return None

    candidates = sorted(tasks_dir.glob(f"{wp_id}*.md"))
    if not candidates:
        return None

    content = candidates[0].read_text(encoding="utf-8", errors="replace")
    if not content.startswith("---"):
        return None

    match = re.search(r"^lane:\s*['\"]?([^'\"\n]+)['\"]?\s*$", content, re.MULTILINE)
    if not match:
        return None
    return match.group(1).strip().lower()


def x__wp_lane_from_feature__mutmut_2(repo_root: Path, feature_slug: str, wp_id: str) -> str | None:
    """Read lane value for a WP prompt file from kitty-specs."""
    tasks_dir = repo_root / KITTY_SPECS_DIR / feature_slug * "tasks"
    if not tasks_dir.exists():
        return None

    candidates = sorted(tasks_dir.glob(f"{wp_id}*.md"))
    if not candidates:
        return None

    content = candidates[0].read_text(encoding="utf-8", errors="replace")
    if not content.startswith("---"):
        return None

    match = re.search(r"^lane:\s*['\"]?([^'\"\n]+)['\"]?\s*$", content, re.MULTILINE)
    if not match:
        return None
    return match.group(1).strip().lower()


def x__wp_lane_from_feature__mutmut_3(repo_root: Path, feature_slug: str, wp_id: str) -> str | None:
    """Read lane value for a WP prompt file from kitty-specs."""
    tasks_dir = repo_root / KITTY_SPECS_DIR * feature_slug / "tasks"
    if not tasks_dir.exists():
        return None

    candidates = sorted(tasks_dir.glob(f"{wp_id}*.md"))
    if not candidates:
        return None

    content = candidates[0].read_text(encoding="utf-8", errors="replace")
    if not content.startswith("---"):
        return None

    match = re.search(r"^lane:\s*['\"]?([^'\"\n]+)['\"]?\s*$", content, re.MULTILINE)
    if not match:
        return None
    return match.group(1).strip().lower()


def x__wp_lane_from_feature__mutmut_4(repo_root: Path, feature_slug: str, wp_id: str) -> str | None:
    """Read lane value for a WP prompt file from kitty-specs."""
    tasks_dir = repo_root * KITTY_SPECS_DIR / feature_slug / "tasks"
    if not tasks_dir.exists():
        return None

    candidates = sorted(tasks_dir.glob(f"{wp_id}*.md"))
    if not candidates:
        return None

    content = candidates[0].read_text(encoding="utf-8", errors="replace")
    if not content.startswith("---"):
        return None

    match = re.search(r"^lane:\s*['\"]?([^'\"\n]+)['\"]?\s*$", content, re.MULTILINE)
    if not match:
        return None
    return match.group(1).strip().lower()


def x__wp_lane_from_feature__mutmut_5(repo_root: Path, feature_slug: str, wp_id: str) -> str | None:
    """Read lane value for a WP prompt file from kitty-specs."""
    tasks_dir = repo_root / KITTY_SPECS_DIR / feature_slug / "XXtasksXX"
    if not tasks_dir.exists():
        return None

    candidates = sorted(tasks_dir.glob(f"{wp_id}*.md"))
    if not candidates:
        return None

    content = candidates[0].read_text(encoding="utf-8", errors="replace")
    if not content.startswith("---"):
        return None

    match = re.search(r"^lane:\s*['\"]?([^'\"\n]+)['\"]?\s*$", content, re.MULTILINE)
    if not match:
        return None
    return match.group(1).strip().lower()


def x__wp_lane_from_feature__mutmut_6(repo_root: Path, feature_slug: str, wp_id: str) -> str | None:
    """Read lane value for a WP prompt file from kitty-specs."""
    tasks_dir = repo_root / KITTY_SPECS_DIR / feature_slug / "TASKS"
    if not tasks_dir.exists():
        return None

    candidates = sorted(tasks_dir.glob(f"{wp_id}*.md"))
    if not candidates:
        return None

    content = candidates[0].read_text(encoding="utf-8", errors="replace")
    if not content.startswith("---"):
        return None

    match = re.search(r"^lane:\s*['\"]?([^'\"\n]+)['\"]?\s*$", content, re.MULTILINE)
    if not match:
        return None
    return match.group(1).strip().lower()


def x__wp_lane_from_feature__mutmut_7(repo_root: Path, feature_slug: str, wp_id: str) -> str | None:
    """Read lane value for a WP prompt file from kitty-specs."""
    tasks_dir = repo_root / KITTY_SPECS_DIR / feature_slug / "tasks"
    if tasks_dir.exists():
        return None

    candidates = sorted(tasks_dir.glob(f"{wp_id}*.md"))
    if not candidates:
        return None

    content = candidates[0].read_text(encoding="utf-8", errors="replace")
    if not content.startswith("---"):
        return None

    match = re.search(r"^lane:\s*['\"]?([^'\"\n]+)['\"]?\s*$", content, re.MULTILINE)
    if not match:
        return None
    return match.group(1).strip().lower()


def x__wp_lane_from_feature__mutmut_8(repo_root: Path, feature_slug: str, wp_id: str) -> str | None:
    """Read lane value for a WP prompt file from kitty-specs."""
    tasks_dir = repo_root / KITTY_SPECS_DIR / feature_slug / "tasks"
    if not tasks_dir.exists():
        return None

    candidates = None
    if not candidates:
        return None

    content = candidates[0].read_text(encoding="utf-8", errors="replace")
    if not content.startswith("---"):
        return None

    match = re.search(r"^lane:\s*['\"]?([^'\"\n]+)['\"]?\s*$", content, re.MULTILINE)
    if not match:
        return None
    return match.group(1).strip().lower()


def x__wp_lane_from_feature__mutmut_9(repo_root: Path, feature_slug: str, wp_id: str) -> str | None:
    """Read lane value for a WP prompt file from kitty-specs."""
    tasks_dir = repo_root / KITTY_SPECS_DIR / feature_slug / "tasks"
    if not tasks_dir.exists():
        return None

    candidates = sorted(None)
    if not candidates:
        return None

    content = candidates[0].read_text(encoding="utf-8", errors="replace")
    if not content.startswith("---"):
        return None

    match = re.search(r"^lane:\s*['\"]?([^'\"\n]+)['\"]?\s*$", content, re.MULTILINE)
    if not match:
        return None
    return match.group(1).strip().lower()


def x__wp_lane_from_feature__mutmut_10(repo_root: Path, feature_slug: str, wp_id: str) -> str | None:
    """Read lane value for a WP prompt file from kitty-specs."""
    tasks_dir = repo_root / KITTY_SPECS_DIR / feature_slug / "tasks"
    if not tasks_dir.exists():
        return None

    candidates = sorted(tasks_dir.glob(None))
    if not candidates:
        return None

    content = candidates[0].read_text(encoding="utf-8", errors="replace")
    if not content.startswith("---"):
        return None

    match = re.search(r"^lane:\s*['\"]?([^'\"\n]+)['\"]?\s*$", content, re.MULTILINE)
    if not match:
        return None
    return match.group(1).strip().lower()


def x__wp_lane_from_feature__mutmut_11(repo_root: Path, feature_slug: str, wp_id: str) -> str | None:
    """Read lane value for a WP prompt file from kitty-specs."""
    tasks_dir = repo_root / KITTY_SPECS_DIR / feature_slug / "tasks"
    if not tasks_dir.exists():
        return None

    candidates = sorted(tasks_dir.glob(f"{wp_id}*.md"))
    if candidates:
        return None

    content = candidates[0].read_text(encoding="utf-8", errors="replace")
    if not content.startswith("---"):
        return None

    match = re.search(r"^lane:\s*['\"]?([^'\"\n]+)['\"]?\s*$", content, re.MULTILINE)
    if not match:
        return None
    return match.group(1).strip().lower()


def x__wp_lane_from_feature__mutmut_12(repo_root: Path, feature_slug: str, wp_id: str) -> str | None:
    """Read lane value for a WP prompt file from kitty-specs."""
    tasks_dir = repo_root / KITTY_SPECS_DIR / feature_slug / "tasks"
    if not tasks_dir.exists():
        return None

    candidates = sorted(tasks_dir.glob(f"{wp_id}*.md"))
    if not candidates:
        return None

    content = None
    if not content.startswith("---"):
        return None

    match = re.search(r"^lane:\s*['\"]?([^'\"\n]+)['\"]?\s*$", content, re.MULTILINE)
    if not match:
        return None
    return match.group(1).strip().lower()


def x__wp_lane_from_feature__mutmut_13(repo_root: Path, feature_slug: str, wp_id: str) -> str | None:
    """Read lane value for a WP prompt file from kitty-specs."""
    tasks_dir = repo_root / KITTY_SPECS_DIR / feature_slug / "tasks"
    if not tasks_dir.exists():
        return None

    candidates = sorted(tasks_dir.glob(f"{wp_id}*.md"))
    if not candidates:
        return None

    content = candidates[0].read_text(encoding=None, errors="replace")
    if not content.startswith("---"):
        return None

    match = re.search(r"^lane:\s*['\"]?([^'\"\n]+)['\"]?\s*$", content, re.MULTILINE)
    if not match:
        return None
    return match.group(1).strip().lower()


def x__wp_lane_from_feature__mutmut_14(repo_root: Path, feature_slug: str, wp_id: str) -> str | None:
    """Read lane value for a WP prompt file from kitty-specs."""
    tasks_dir = repo_root / KITTY_SPECS_DIR / feature_slug / "tasks"
    if not tasks_dir.exists():
        return None

    candidates = sorted(tasks_dir.glob(f"{wp_id}*.md"))
    if not candidates:
        return None

    content = candidates[0].read_text(encoding="utf-8", errors=None)
    if not content.startswith("---"):
        return None

    match = re.search(r"^lane:\s*['\"]?([^'\"\n]+)['\"]?\s*$", content, re.MULTILINE)
    if not match:
        return None
    return match.group(1).strip().lower()


def x__wp_lane_from_feature__mutmut_15(repo_root: Path, feature_slug: str, wp_id: str) -> str | None:
    """Read lane value for a WP prompt file from kitty-specs."""
    tasks_dir = repo_root / KITTY_SPECS_DIR / feature_slug / "tasks"
    if not tasks_dir.exists():
        return None

    candidates = sorted(tasks_dir.glob(f"{wp_id}*.md"))
    if not candidates:
        return None

    content = candidates[0].read_text(errors="replace")
    if not content.startswith("---"):
        return None

    match = re.search(r"^lane:\s*['\"]?([^'\"\n]+)['\"]?\s*$", content, re.MULTILINE)
    if not match:
        return None
    return match.group(1).strip().lower()


def x__wp_lane_from_feature__mutmut_16(repo_root: Path, feature_slug: str, wp_id: str) -> str | None:
    """Read lane value for a WP prompt file from kitty-specs."""
    tasks_dir = repo_root / KITTY_SPECS_DIR / feature_slug / "tasks"
    if not tasks_dir.exists():
        return None

    candidates = sorted(tasks_dir.glob(f"{wp_id}*.md"))
    if not candidates:
        return None

    content = candidates[0].read_text(encoding="utf-8", )
    if not content.startswith("---"):
        return None

    match = re.search(r"^lane:\s*['\"]?([^'\"\n]+)['\"]?\s*$", content, re.MULTILINE)
    if not match:
        return None
    return match.group(1).strip().lower()


def x__wp_lane_from_feature__mutmut_17(repo_root: Path, feature_slug: str, wp_id: str) -> str | None:
    """Read lane value for a WP prompt file from kitty-specs."""
    tasks_dir = repo_root / KITTY_SPECS_DIR / feature_slug / "tasks"
    if not tasks_dir.exists():
        return None

    candidates = sorted(tasks_dir.glob(f"{wp_id}*.md"))
    if not candidates:
        return None

    content = candidates[1].read_text(encoding="utf-8", errors="replace")
    if not content.startswith("---"):
        return None

    match = re.search(r"^lane:\s*['\"]?([^'\"\n]+)['\"]?\s*$", content, re.MULTILINE)
    if not match:
        return None
    return match.group(1).strip().lower()


def x__wp_lane_from_feature__mutmut_18(repo_root: Path, feature_slug: str, wp_id: str) -> str | None:
    """Read lane value for a WP prompt file from kitty-specs."""
    tasks_dir = repo_root / KITTY_SPECS_DIR / feature_slug / "tasks"
    if not tasks_dir.exists():
        return None

    candidates = sorted(tasks_dir.glob(f"{wp_id}*.md"))
    if not candidates:
        return None

    content = candidates[0].read_text(encoding="XXutf-8XX", errors="replace")
    if not content.startswith("---"):
        return None

    match = re.search(r"^lane:\s*['\"]?([^'\"\n]+)['\"]?\s*$", content, re.MULTILINE)
    if not match:
        return None
    return match.group(1).strip().lower()


def x__wp_lane_from_feature__mutmut_19(repo_root: Path, feature_slug: str, wp_id: str) -> str | None:
    """Read lane value for a WP prompt file from kitty-specs."""
    tasks_dir = repo_root / KITTY_SPECS_DIR / feature_slug / "tasks"
    if not tasks_dir.exists():
        return None

    candidates = sorted(tasks_dir.glob(f"{wp_id}*.md"))
    if not candidates:
        return None

    content = candidates[0].read_text(encoding="UTF-8", errors="replace")
    if not content.startswith("---"):
        return None

    match = re.search(r"^lane:\s*['\"]?([^'\"\n]+)['\"]?\s*$", content, re.MULTILINE)
    if not match:
        return None
    return match.group(1).strip().lower()


def x__wp_lane_from_feature__mutmut_20(repo_root: Path, feature_slug: str, wp_id: str) -> str | None:
    """Read lane value for a WP prompt file from kitty-specs."""
    tasks_dir = repo_root / KITTY_SPECS_DIR / feature_slug / "tasks"
    if not tasks_dir.exists():
        return None

    candidates = sorted(tasks_dir.glob(f"{wp_id}*.md"))
    if not candidates:
        return None

    content = candidates[0].read_text(encoding="utf-8", errors="XXreplaceXX")
    if not content.startswith("---"):
        return None

    match = re.search(r"^lane:\s*['\"]?([^'\"\n]+)['\"]?\s*$", content, re.MULTILINE)
    if not match:
        return None
    return match.group(1).strip().lower()


def x__wp_lane_from_feature__mutmut_21(repo_root: Path, feature_slug: str, wp_id: str) -> str | None:
    """Read lane value for a WP prompt file from kitty-specs."""
    tasks_dir = repo_root / KITTY_SPECS_DIR / feature_slug / "tasks"
    if not tasks_dir.exists():
        return None

    candidates = sorted(tasks_dir.glob(f"{wp_id}*.md"))
    if not candidates:
        return None

    content = candidates[0].read_text(encoding="utf-8", errors="REPLACE")
    if not content.startswith("---"):
        return None

    match = re.search(r"^lane:\s*['\"]?([^'\"\n]+)['\"]?\s*$", content, re.MULTILINE)
    if not match:
        return None
    return match.group(1).strip().lower()


def x__wp_lane_from_feature__mutmut_22(repo_root: Path, feature_slug: str, wp_id: str) -> str | None:
    """Read lane value for a WP prompt file from kitty-specs."""
    tasks_dir = repo_root / KITTY_SPECS_DIR / feature_slug / "tasks"
    if not tasks_dir.exists():
        return None

    candidates = sorted(tasks_dir.glob(f"{wp_id}*.md"))
    if not candidates:
        return None

    content = candidates[0].read_text(encoding="utf-8", errors="replace")
    if content.startswith("---"):
        return None

    match = re.search(r"^lane:\s*['\"]?([^'\"\n]+)['\"]?\s*$", content, re.MULTILINE)
    if not match:
        return None
    return match.group(1).strip().lower()


def x__wp_lane_from_feature__mutmut_23(repo_root: Path, feature_slug: str, wp_id: str) -> str | None:
    """Read lane value for a WP prompt file from kitty-specs."""
    tasks_dir = repo_root / KITTY_SPECS_DIR / feature_slug / "tasks"
    if not tasks_dir.exists():
        return None

    candidates = sorted(tasks_dir.glob(f"{wp_id}*.md"))
    if not candidates:
        return None

    content = candidates[0].read_text(encoding="utf-8", errors="replace")
    if not content.startswith(None):
        return None

    match = re.search(r"^lane:\s*['\"]?([^'\"\n]+)['\"]?\s*$", content, re.MULTILINE)
    if not match:
        return None
    return match.group(1).strip().lower()


def x__wp_lane_from_feature__mutmut_24(repo_root: Path, feature_slug: str, wp_id: str) -> str | None:
    """Read lane value for a WP prompt file from kitty-specs."""
    tasks_dir = repo_root / KITTY_SPECS_DIR / feature_slug / "tasks"
    if not tasks_dir.exists():
        return None

    candidates = sorted(tasks_dir.glob(f"{wp_id}*.md"))
    if not candidates:
        return None

    content = candidates[0].read_text(encoding="utf-8", errors="replace")
    if not content.startswith("XX---XX"):
        return None

    match = re.search(r"^lane:\s*['\"]?([^'\"\n]+)['\"]?\s*$", content, re.MULTILINE)
    if not match:
        return None
    return match.group(1).strip().lower()


def x__wp_lane_from_feature__mutmut_25(repo_root: Path, feature_slug: str, wp_id: str) -> str | None:
    """Read lane value for a WP prompt file from kitty-specs."""
    tasks_dir = repo_root / KITTY_SPECS_DIR / feature_slug / "tasks"
    if not tasks_dir.exists():
        return None

    candidates = sorted(tasks_dir.glob(f"{wp_id}*.md"))
    if not candidates:
        return None

    content = candidates[0].read_text(encoding="utf-8", errors="replace")
    if not content.startswith("---"):
        return None

    match = None
    if not match:
        return None
    return match.group(1).strip().lower()


def x__wp_lane_from_feature__mutmut_26(repo_root: Path, feature_slug: str, wp_id: str) -> str | None:
    """Read lane value for a WP prompt file from kitty-specs."""
    tasks_dir = repo_root / KITTY_SPECS_DIR / feature_slug / "tasks"
    if not tasks_dir.exists():
        return None

    candidates = sorted(tasks_dir.glob(f"{wp_id}*.md"))
    if not candidates:
        return None

    content = candidates[0].read_text(encoding="utf-8", errors="replace")
    if not content.startswith("---"):
        return None

    match = re.search(None, content, re.MULTILINE)
    if not match:
        return None
    return match.group(1).strip().lower()


def x__wp_lane_from_feature__mutmut_27(repo_root: Path, feature_slug: str, wp_id: str) -> str | None:
    """Read lane value for a WP prompt file from kitty-specs."""
    tasks_dir = repo_root / KITTY_SPECS_DIR / feature_slug / "tasks"
    if not tasks_dir.exists():
        return None

    candidates = sorted(tasks_dir.glob(f"{wp_id}*.md"))
    if not candidates:
        return None

    content = candidates[0].read_text(encoding="utf-8", errors="replace")
    if not content.startswith("---"):
        return None

    match = re.search(r"^lane:\s*['\"]?([^'\"\n]+)['\"]?\s*$", None, re.MULTILINE)
    if not match:
        return None
    return match.group(1).strip().lower()


def x__wp_lane_from_feature__mutmut_28(repo_root: Path, feature_slug: str, wp_id: str) -> str | None:
    """Read lane value for a WP prompt file from kitty-specs."""
    tasks_dir = repo_root / KITTY_SPECS_DIR / feature_slug / "tasks"
    if not tasks_dir.exists():
        return None

    candidates = sorted(tasks_dir.glob(f"{wp_id}*.md"))
    if not candidates:
        return None

    content = candidates[0].read_text(encoding="utf-8", errors="replace")
    if not content.startswith("---"):
        return None

    match = re.search(r"^lane:\s*['\"]?([^'\"\n]+)['\"]?\s*$", content, None)
    if not match:
        return None
    return match.group(1).strip().lower()


def x__wp_lane_from_feature__mutmut_29(repo_root: Path, feature_slug: str, wp_id: str) -> str | None:
    """Read lane value for a WP prompt file from kitty-specs."""
    tasks_dir = repo_root / KITTY_SPECS_DIR / feature_slug / "tasks"
    if not tasks_dir.exists():
        return None

    candidates = sorted(tasks_dir.glob(f"{wp_id}*.md"))
    if not candidates:
        return None

    content = candidates[0].read_text(encoding="utf-8", errors="replace")
    if not content.startswith("---"):
        return None

    match = re.search(content, re.MULTILINE)
    if not match:
        return None
    return match.group(1).strip().lower()


def x__wp_lane_from_feature__mutmut_30(repo_root: Path, feature_slug: str, wp_id: str) -> str | None:
    """Read lane value for a WP prompt file from kitty-specs."""
    tasks_dir = repo_root / KITTY_SPECS_DIR / feature_slug / "tasks"
    if not tasks_dir.exists():
        return None

    candidates = sorted(tasks_dir.glob(f"{wp_id}*.md"))
    if not candidates:
        return None

    content = candidates[0].read_text(encoding="utf-8", errors="replace")
    if not content.startswith("---"):
        return None

    match = re.search(r"^lane:\s*['\"]?([^'\"\n]+)['\"]?\s*$", re.MULTILINE)
    if not match:
        return None
    return match.group(1).strip().lower()


def x__wp_lane_from_feature__mutmut_31(repo_root: Path, feature_slug: str, wp_id: str) -> str | None:
    """Read lane value for a WP prompt file from kitty-specs."""
    tasks_dir = repo_root / KITTY_SPECS_DIR / feature_slug / "tasks"
    if not tasks_dir.exists():
        return None

    candidates = sorted(tasks_dir.glob(f"{wp_id}*.md"))
    if not candidates:
        return None

    content = candidates[0].read_text(encoding="utf-8", errors="replace")
    if not content.startswith("---"):
        return None

    match = re.search(r"^lane:\s*['\"]?([^'\"\n]+)['\"]?\s*$", content, )
    if not match:
        return None
    return match.group(1).strip().lower()


def x__wp_lane_from_feature__mutmut_32(repo_root: Path, feature_slug: str, wp_id: str) -> str | None:
    """Read lane value for a WP prompt file from kitty-specs."""
    tasks_dir = repo_root / KITTY_SPECS_DIR / feature_slug / "tasks"
    if not tasks_dir.exists():
        return None

    candidates = sorted(tasks_dir.glob(f"{wp_id}*.md"))
    if not candidates:
        return None

    content = candidates[0].read_text(encoding="utf-8", errors="replace")
    if not content.startswith("---"):
        return None

    match = re.search(r"XX^lane:\s*['\"]?([^'\"\n]+)['\"]?\s*$XX", content, re.MULTILINE)
    if not match:
        return None
    return match.group(1).strip().lower()


def x__wp_lane_from_feature__mutmut_33(repo_root: Path, feature_slug: str, wp_id: str) -> str | None:
    """Read lane value for a WP prompt file from kitty-specs."""
    tasks_dir = repo_root / KITTY_SPECS_DIR / feature_slug / "tasks"
    if not tasks_dir.exists():
        return None

    candidates = sorted(tasks_dir.glob(f"{wp_id}*.md"))
    if not candidates:
        return None

    content = candidates[0].read_text(encoding="utf-8", errors="replace")
    if not content.startswith("---"):
        return None

    match = re.search(r"^LANE:\s*['\"]?([^'\"\n]+)['\"]?\s*$", content, re.MULTILINE)
    if not match:
        return None
    return match.group(1).strip().lower()


def x__wp_lane_from_feature__mutmut_34(repo_root: Path, feature_slug: str, wp_id: str) -> str | None:
    """Read lane value for a WP prompt file from kitty-specs."""
    tasks_dir = repo_root / KITTY_SPECS_DIR / feature_slug / "tasks"
    if not tasks_dir.exists():
        return None

    candidates = sorted(tasks_dir.glob(f"{wp_id}*.md"))
    if not candidates:
        return None

    content = candidates[0].read_text(encoding="utf-8", errors="replace")
    if not content.startswith("---"):
        return None

    match = re.search(r"^lane:\s*['\"]?([^'\"\n]+)['\"]?\s*$", content, re.MULTILINE)
    if match:
        return None
    return match.group(1).strip().lower()


def x__wp_lane_from_feature__mutmut_35(repo_root: Path, feature_slug: str, wp_id: str) -> str | None:
    """Read lane value for a WP prompt file from kitty-specs."""
    tasks_dir = repo_root / KITTY_SPECS_DIR / feature_slug / "tasks"
    if not tasks_dir.exists():
        return None

    candidates = sorted(tasks_dir.glob(f"{wp_id}*.md"))
    if not candidates:
        return None

    content = candidates[0].read_text(encoding="utf-8", errors="replace")
    if not content.startswith("---"):
        return None

    match = re.search(r"^lane:\s*['\"]?([^'\"\n]+)['\"]?\s*$", content, re.MULTILINE)
    if not match:
        return None
    return match.group(1).strip().upper()


def x__wp_lane_from_feature__mutmut_36(repo_root: Path, feature_slug: str, wp_id: str) -> str | None:
    """Read lane value for a WP prompt file from kitty-specs."""
    tasks_dir = repo_root / KITTY_SPECS_DIR / feature_slug / "tasks"
    if not tasks_dir.exists():
        return None

    candidates = sorted(tasks_dir.glob(f"{wp_id}*.md"))
    if not candidates:
        return None

    content = candidates[0].read_text(encoding="utf-8", errors="replace")
    if not content.startswith("---"):
        return None

    match = re.search(r"^lane:\s*['\"]?([^'\"\n]+)['\"]?\s*$", content, re.MULTILINE)
    if not match:
        return None
    return match.group(None).strip().lower()


def x__wp_lane_from_feature__mutmut_37(repo_root: Path, feature_slug: str, wp_id: str) -> str | None:
    """Read lane value for a WP prompt file from kitty-specs."""
    tasks_dir = repo_root / KITTY_SPECS_DIR / feature_slug / "tasks"
    if not tasks_dir.exists():
        return None

    candidates = sorted(tasks_dir.glob(f"{wp_id}*.md"))
    if not candidates:
        return None

    content = candidates[0].read_text(encoding="utf-8", errors="replace")
    if not content.startswith("---"):
        return None

    match = re.search(r"^lane:\s*['\"]?([^'\"\n]+)['\"]?\s*$", content, re.MULTILINE)
    if not match:
        return None
    return match.group(2).strip().lower()

x__wp_lane_from_feature__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x__wp_lane_from_feature__mutmut_1': x__wp_lane_from_feature__mutmut_1, 
    'x__wp_lane_from_feature__mutmut_2': x__wp_lane_from_feature__mutmut_2, 
    'x__wp_lane_from_feature__mutmut_3': x__wp_lane_from_feature__mutmut_3, 
    'x__wp_lane_from_feature__mutmut_4': x__wp_lane_from_feature__mutmut_4, 
    'x__wp_lane_from_feature__mutmut_5': x__wp_lane_from_feature__mutmut_5, 
    'x__wp_lane_from_feature__mutmut_6': x__wp_lane_from_feature__mutmut_6, 
    'x__wp_lane_from_feature__mutmut_7': x__wp_lane_from_feature__mutmut_7, 
    'x__wp_lane_from_feature__mutmut_8': x__wp_lane_from_feature__mutmut_8, 
    'x__wp_lane_from_feature__mutmut_9': x__wp_lane_from_feature__mutmut_9, 
    'x__wp_lane_from_feature__mutmut_10': x__wp_lane_from_feature__mutmut_10, 
    'x__wp_lane_from_feature__mutmut_11': x__wp_lane_from_feature__mutmut_11, 
    'x__wp_lane_from_feature__mutmut_12': x__wp_lane_from_feature__mutmut_12, 
    'x__wp_lane_from_feature__mutmut_13': x__wp_lane_from_feature__mutmut_13, 
    'x__wp_lane_from_feature__mutmut_14': x__wp_lane_from_feature__mutmut_14, 
    'x__wp_lane_from_feature__mutmut_15': x__wp_lane_from_feature__mutmut_15, 
    'x__wp_lane_from_feature__mutmut_16': x__wp_lane_from_feature__mutmut_16, 
    'x__wp_lane_from_feature__mutmut_17': x__wp_lane_from_feature__mutmut_17, 
    'x__wp_lane_from_feature__mutmut_18': x__wp_lane_from_feature__mutmut_18, 
    'x__wp_lane_from_feature__mutmut_19': x__wp_lane_from_feature__mutmut_19, 
    'x__wp_lane_from_feature__mutmut_20': x__wp_lane_from_feature__mutmut_20, 
    'x__wp_lane_from_feature__mutmut_21': x__wp_lane_from_feature__mutmut_21, 
    'x__wp_lane_from_feature__mutmut_22': x__wp_lane_from_feature__mutmut_22, 
    'x__wp_lane_from_feature__mutmut_23': x__wp_lane_from_feature__mutmut_23, 
    'x__wp_lane_from_feature__mutmut_24': x__wp_lane_from_feature__mutmut_24, 
    'x__wp_lane_from_feature__mutmut_25': x__wp_lane_from_feature__mutmut_25, 
    'x__wp_lane_from_feature__mutmut_26': x__wp_lane_from_feature__mutmut_26, 
    'x__wp_lane_from_feature__mutmut_27': x__wp_lane_from_feature__mutmut_27, 
    'x__wp_lane_from_feature__mutmut_28': x__wp_lane_from_feature__mutmut_28, 
    'x__wp_lane_from_feature__mutmut_29': x__wp_lane_from_feature__mutmut_29, 
    'x__wp_lane_from_feature__mutmut_30': x__wp_lane_from_feature__mutmut_30, 
    'x__wp_lane_from_feature__mutmut_31': x__wp_lane_from_feature__mutmut_31, 
    'x__wp_lane_from_feature__mutmut_32': x__wp_lane_from_feature__mutmut_32, 
    'x__wp_lane_from_feature__mutmut_33': x__wp_lane_from_feature__mutmut_33, 
    'x__wp_lane_from_feature__mutmut_34': x__wp_lane_from_feature__mutmut_34, 
    'x__wp_lane_from_feature__mutmut_35': x__wp_lane_from_feature__mutmut_35, 
    'x__wp_lane_from_feature__mutmut_36': x__wp_lane_from_feature__mutmut_36, 
    'x__wp_lane_from_feature__mutmut_37': x__wp_lane_from_feature__mutmut_37
}
x__wp_lane_from_feature__mutmut_orig.__name__ = 'x__wp_lane_from_feature'


def run_preflight(
    feature_slug: str,
    target_branch: str,
    repo_root: Path,
    wp_workspaces: list[tuple[Path, str, str]],
) -> PreflightResult:
    args = [feature_slug, target_branch, repo_root, wp_workspaces]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_run_preflight__mutmut_orig, x_run_preflight__mutmut_mutants, args, kwargs, None)


def x_run_preflight__mutmut_orig(
    feature_slug: str,
    target_branch: str,
    repo_root: Path,
    wp_workspaces: list[tuple[Path, str, str]],
) -> PreflightResult:
    """Run all pre-flight checks before merge.

    Args:
        feature_slug: Feature identifier (e.g., "017-smarter-feature-merge")
        target_branch: Branch to merge into (e.g., "main")
        repo_root: Repository root path
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples

    Returns:
        PreflightResult with all check outcomes
    """
    result = PreflightResult(passed=True)

    # Check for missing worktrees based on tasks in kitty-specs
    expected_graph = build_dependency_graph(repo_root / KITTY_SPECS_DIR / feature_slug)
    expected_wps = set(expected_graph.keys())
    discovered_wps = {wp_id for _, wp_id, _ in wp_workspaces}
    missing_wps = sorted(expected_wps - discovered_wps)
    if missing_wps:
        for wp_id in missing_wps:
            lane = _wp_lane_from_feature(repo_root, feature_slug, wp_id)
            if lane == "done":
                result.warnings.append(
                    f"Skipping missing worktree check for {wp_id} (lane=done)."
                )
                continue

            result.passed = False
            expected_path = repo_root / WORKTREES_DIR / f"{feature_slug}-{wp_id}"
            error = f"Missing worktree for {wp_id}. Expected at {expected_path.name}. Run: spec-kitty agent workflow implement {wp_id}"
            result.wp_statuses.append(
                WPStatus(
                    wp_id=wp_id,
                    worktree_path=expected_path,
                    branch_name=f"{feature_slug}-{wp_id}",
                    is_clean=False,
                    error=error,
                )
            )
            result.errors.append(error)

    # Check all worktrees
    for wt_path, wp_id, branch in wp_workspaces:
        status = check_worktree_status(wt_path, wp_id, branch)
        result.wp_statuses.append(status)
        if not status.is_clean:
            result.passed = False
            result.errors.append(status.error or f"{wp_id} has uncommitted changes")

    # Check target divergence
    diverged, msg = check_target_divergence(target_branch, repo_root)
    result.target_diverged = diverged
    result.target_divergence_msg = msg
    if diverged:
        result.passed = False
        result.errors.append(msg or f"{target_branch} has diverged from origin")

    return result


def x_run_preflight__mutmut_1(
    feature_slug: str,
    target_branch: str,
    repo_root: Path,
    wp_workspaces: list[tuple[Path, str, str]],
) -> PreflightResult:
    """Run all pre-flight checks before merge.

    Args:
        feature_slug: Feature identifier (e.g., "017-smarter-feature-merge")
        target_branch: Branch to merge into (e.g., "main")
        repo_root: Repository root path
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples

    Returns:
        PreflightResult with all check outcomes
    """
    result = None

    # Check for missing worktrees based on tasks in kitty-specs
    expected_graph = build_dependency_graph(repo_root / KITTY_SPECS_DIR / feature_slug)
    expected_wps = set(expected_graph.keys())
    discovered_wps = {wp_id for _, wp_id, _ in wp_workspaces}
    missing_wps = sorted(expected_wps - discovered_wps)
    if missing_wps:
        for wp_id in missing_wps:
            lane = _wp_lane_from_feature(repo_root, feature_slug, wp_id)
            if lane == "done":
                result.warnings.append(
                    f"Skipping missing worktree check for {wp_id} (lane=done)."
                )
                continue

            result.passed = False
            expected_path = repo_root / WORKTREES_DIR / f"{feature_slug}-{wp_id}"
            error = f"Missing worktree for {wp_id}. Expected at {expected_path.name}. Run: spec-kitty agent workflow implement {wp_id}"
            result.wp_statuses.append(
                WPStatus(
                    wp_id=wp_id,
                    worktree_path=expected_path,
                    branch_name=f"{feature_slug}-{wp_id}",
                    is_clean=False,
                    error=error,
                )
            )
            result.errors.append(error)

    # Check all worktrees
    for wt_path, wp_id, branch in wp_workspaces:
        status = check_worktree_status(wt_path, wp_id, branch)
        result.wp_statuses.append(status)
        if not status.is_clean:
            result.passed = False
            result.errors.append(status.error or f"{wp_id} has uncommitted changes")

    # Check target divergence
    diverged, msg = check_target_divergence(target_branch, repo_root)
    result.target_diverged = diverged
    result.target_divergence_msg = msg
    if diverged:
        result.passed = False
        result.errors.append(msg or f"{target_branch} has diverged from origin")

    return result


def x_run_preflight__mutmut_2(
    feature_slug: str,
    target_branch: str,
    repo_root: Path,
    wp_workspaces: list[tuple[Path, str, str]],
) -> PreflightResult:
    """Run all pre-flight checks before merge.

    Args:
        feature_slug: Feature identifier (e.g., "017-smarter-feature-merge")
        target_branch: Branch to merge into (e.g., "main")
        repo_root: Repository root path
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples

    Returns:
        PreflightResult with all check outcomes
    """
    result = PreflightResult(passed=None)

    # Check for missing worktrees based on tasks in kitty-specs
    expected_graph = build_dependency_graph(repo_root / KITTY_SPECS_DIR / feature_slug)
    expected_wps = set(expected_graph.keys())
    discovered_wps = {wp_id for _, wp_id, _ in wp_workspaces}
    missing_wps = sorted(expected_wps - discovered_wps)
    if missing_wps:
        for wp_id in missing_wps:
            lane = _wp_lane_from_feature(repo_root, feature_slug, wp_id)
            if lane == "done":
                result.warnings.append(
                    f"Skipping missing worktree check for {wp_id} (lane=done)."
                )
                continue

            result.passed = False
            expected_path = repo_root / WORKTREES_DIR / f"{feature_slug}-{wp_id}"
            error = f"Missing worktree for {wp_id}. Expected at {expected_path.name}. Run: spec-kitty agent workflow implement {wp_id}"
            result.wp_statuses.append(
                WPStatus(
                    wp_id=wp_id,
                    worktree_path=expected_path,
                    branch_name=f"{feature_slug}-{wp_id}",
                    is_clean=False,
                    error=error,
                )
            )
            result.errors.append(error)

    # Check all worktrees
    for wt_path, wp_id, branch in wp_workspaces:
        status = check_worktree_status(wt_path, wp_id, branch)
        result.wp_statuses.append(status)
        if not status.is_clean:
            result.passed = False
            result.errors.append(status.error or f"{wp_id} has uncommitted changes")

    # Check target divergence
    diverged, msg = check_target_divergence(target_branch, repo_root)
    result.target_diverged = diverged
    result.target_divergence_msg = msg
    if diverged:
        result.passed = False
        result.errors.append(msg or f"{target_branch} has diverged from origin")

    return result


def x_run_preflight__mutmut_3(
    feature_slug: str,
    target_branch: str,
    repo_root: Path,
    wp_workspaces: list[tuple[Path, str, str]],
) -> PreflightResult:
    """Run all pre-flight checks before merge.

    Args:
        feature_slug: Feature identifier (e.g., "017-smarter-feature-merge")
        target_branch: Branch to merge into (e.g., "main")
        repo_root: Repository root path
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples

    Returns:
        PreflightResult with all check outcomes
    """
    result = PreflightResult(passed=False)

    # Check for missing worktrees based on tasks in kitty-specs
    expected_graph = build_dependency_graph(repo_root / KITTY_SPECS_DIR / feature_slug)
    expected_wps = set(expected_graph.keys())
    discovered_wps = {wp_id for _, wp_id, _ in wp_workspaces}
    missing_wps = sorted(expected_wps - discovered_wps)
    if missing_wps:
        for wp_id in missing_wps:
            lane = _wp_lane_from_feature(repo_root, feature_slug, wp_id)
            if lane == "done":
                result.warnings.append(
                    f"Skipping missing worktree check for {wp_id} (lane=done)."
                )
                continue

            result.passed = False
            expected_path = repo_root / WORKTREES_DIR / f"{feature_slug}-{wp_id}"
            error = f"Missing worktree for {wp_id}. Expected at {expected_path.name}. Run: spec-kitty agent workflow implement {wp_id}"
            result.wp_statuses.append(
                WPStatus(
                    wp_id=wp_id,
                    worktree_path=expected_path,
                    branch_name=f"{feature_slug}-{wp_id}",
                    is_clean=False,
                    error=error,
                )
            )
            result.errors.append(error)

    # Check all worktrees
    for wt_path, wp_id, branch in wp_workspaces:
        status = check_worktree_status(wt_path, wp_id, branch)
        result.wp_statuses.append(status)
        if not status.is_clean:
            result.passed = False
            result.errors.append(status.error or f"{wp_id} has uncommitted changes")

    # Check target divergence
    diverged, msg = check_target_divergence(target_branch, repo_root)
    result.target_diverged = diverged
    result.target_divergence_msg = msg
    if diverged:
        result.passed = False
        result.errors.append(msg or f"{target_branch} has diverged from origin")

    return result


def x_run_preflight__mutmut_4(
    feature_slug: str,
    target_branch: str,
    repo_root: Path,
    wp_workspaces: list[tuple[Path, str, str]],
) -> PreflightResult:
    """Run all pre-flight checks before merge.

    Args:
        feature_slug: Feature identifier (e.g., "017-smarter-feature-merge")
        target_branch: Branch to merge into (e.g., "main")
        repo_root: Repository root path
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples

    Returns:
        PreflightResult with all check outcomes
    """
    result = PreflightResult(passed=True)

    # Check for missing worktrees based on tasks in kitty-specs
    expected_graph = None
    expected_wps = set(expected_graph.keys())
    discovered_wps = {wp_id for _, wp_id, _ in wp_workspaces}
    missing_wps = sorted(expected_wps - discovered_wps)
    if missing_wps:
        for wp_id in missing_wps:
            lane = _wp_lane_from_feature(repo_root, feature_slug, wp_id)
            if lane == "done":
                result.warnings.append(
                    f"Skipping missing worktree check for {wp_id} (lane=done)."
                )
                continue

            result.passed = False
            expected_path = repo_root / WORKTREES_DIR / f"{feature_slug}-{wp_id}"
            error = f"Missing worktree for {wp_id}. Expected at {expected_path.name}. Run: spec-kitty agent workflow implement {wp_id}"
            result.wp_statuses.append(
                WPStatus(
                    wp_id=wp_id,
                    worktree_path=expected_path,
                    branch_name=f"{feature_slug}-{wp_id}",
                    is_clean=False,
                    error=error,
                )
            )
            result.errors.append(error)

    # Check all worktrees
    for wt_path, wp_id, branch in wp_workspaces:
        status = check_worktree_status(wt_path, wp_id, branch)
        result.wp_statuses.append(status)
        if not status.is_clean:
            result.passed = False
            result.errors.append(status.error or f"{wp_id} has uncommitted changes")

    # Check target divergence
    diverged, msg = check_target_divergence(target_branch, repo_root)
    result.target_diverged = diverged
    result.target_divergence_msg = msg
    if diverged:
        result.passed = False
        result.errors.append(msg or f"{target_branch} has diverged from origin")

    return result


def x_run_preflight__mutmut_5(
    feature_slug: str,
    target_branch: str,
    repo_root: Path,
    wp_workspaces: list[tuple[Path, str, str]],
) -> PreflightResult:
    """Run all pre-flight checks before merge.

    Args:
        feature_slug: Feature identifier (e.g., "017-smarter-feature-merge")
        target_branch: Branch to merge into (e.g., "main")
        repo_root: Repository root path
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples

    Returns:
        PreflightResult with all check outcomes
    """
    result = PreflightResult(passed=True)

    # Check for missing worktrees based on tasks in kitty-specs
    expected_graph = build_dependency_graph(None)
    expected_wps = set(expected_graph.keys())
    discovered_wps = {wp_id for _, wp_id, _ in wp_workspaces}
    missing_wps = sorted(expected_wps - discovered_wps)
    if missing_wps:
        for wp_id in missing_wps:
            lane = _wp_lane_from_feature(repo_root, feature_slug, wp_id)
            if lane == "done":
                result.warnings.append(
                    f"Skipping missing worktree check for {wp_id} (lane=done)."
                )
                continue

            result.passed = False
            expected_path = repo_root / WORKTREES_DIR / f"{feature_slug}-{wp_id}"
            error = f"Missing worktree for {wp_id}. Expected at {expected_path.name}. Run: spec-kitty agent workflow implement {wp_id}"
            result.wp_statuses.append(
                WPStatus(
                    wp_id=wp_id,
                    worktree_path=expected_path,
                    branch_name=f"{feature_slug}-{wp_id}",
                    is_clean=False,
                    error=error,
                )
            )
            result.errors.append(error)

    # Check all worktrees
    for wt_path, wp_id, branch in wp_workspaces:
        status = check_worktree_status(wt_path, wp_id, branch)
        result.wp_statuses.append(status)
        if not status.is_clean:
            result.passed = False
            result.errors.append(status.error or f"{wp_id} has uncommitted changes")

    # Check target divergence
    diverged, msg = check_target_divergence(target_branch, repo_root)
    result.target_diverged = diverged
    result.target_divergence_msg = msg
    if diverged:
        result.passed = False
        result.errors.append(msg or f"{target_branch} has diverged from origin")

    return result


def x_run_preflight__mutmut_6(
    feature_slug: str,
    target_branch: str,
    repo_root: Path,
    wp_workspaces: list[tuple[Path, str, str]],
) -> PreflightResult:
    """Run all pre-flight checks before merge.

    Args:
        feature_slug: Feature identifier (e.g., "017-smarter-feature-merge")
        target_branch: Branch to merge into (e.g., "main")
        repo_root: Repository root path
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples

    Returns:
        PreflightResult with all check outcomes
    """
    result = PreflightResult(passed=True)

    # Check for missing worktrees based on tasks in kitty-specs
    expected_graph = build_dependency_graph(repo_root / KITTY_SPECS_DIR * feature_slug)
    expected_wps = set(expected_graph.keys())
    discovered_wps = {wp_id for _, wp_id, _ in wp_workspaces}
    missing_wps = sorted(expected_wps - discovered_wps)
    if missing_wps:
        for wp_id in missing_wps:
            lane = _wp_lane_from_feature(repo_root, feature_slug, wp_id)
            if lane == "done":
                result.warnings.append(
                    f"Skipping missing worktree check for {wp_id} (lane=done)."
                )
                continue

            result.passed = False
            expected_path = repo_root / WORKTREES_DIR / f"{feature_slug}-{wp_id}"
            error = f"Missing worktree for {wp_id}. Expected at {expected_path.name}. Run: spec-kitty agent workflow implement {wp_id}"
            result.wp_statuses.append(
                WPStatus(
                    wp_id=wp_id,
                    worktree_path=expected_path,
                    branch_name=f"{feature_slug}-{wp_id}",
                    is_clean=False,
                    error=error,
                )
            )
            result.errors.append(error)

    # Check all worktrees
    for wt_path, wp_id, branch in wp_workspaces:
        status = check_worktree_status(wt_path, wp_id, branch)
        result.wp_statuses.append(status)
        if not status.is_clean:
            result.passed = False
            result.errors.append(status.error or f"{wp_id} has uncommitted changes")

    # Check target divergence
    diverged, msg = check_target_divergence(target_branch, repo_root)
    result.target_diverged = diverged
    result.target_divergence_msg = msg
    if diverged:
        result.passed = False
        result.errors.append(msg or f"{target_branch} has diverged from origin")

    return result


def x_run_preflight__mutmut_7(
    feature_slug: str,
    target_branch: str,
    repo_root: Path,
    wp_workspaces: list[tuple[Path, str, str]],
) -> PreflightResult:
    """Run all pre-flight checks before merge.

    Args:
        feature_slug: Feature identifier (e.g., "017-smarter-feature-merge")
        target_branch: Branch to merge into (e.g., "main")
        repo_root: Repository root path
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples

    Returns:
        PreflightResult with all check outcomes
    """
    result = PreflightResult(passed=True)

    # Check for missing worktrees based on tasks in kitty-specs
    expected_graph = build_dependency_graph(repo_root * KITTY_SPECS_DIR / feature_slug)
    expected_wps = set(expected_graph.keys())
    discovered_wps = {wp_id for _, wp_id, _ in wp_workspaces}
    missing_wps = sorted(expected_wps - discovered_wps)
    if missing_wps:
        for wp_id in missing_wps:
            lane = _wp_lane_from_feature(repo_root, feature_slug, wp_id)
            if lane == "done":
                result.warnings.append(
                    f"Skipping missing worktree check for {wp_id} (lane=done)."
                )
                continue

            result.passed = False
            expected_path = repo_root / WORKTREES_DIR / f"{feature_slug}-{wp_id}"
            error = f"Missing worktree for {wp_id}. Expected at {expected_path.name}. Run: spec-kitty agent workflow implement {wp_id}"
            result.wp_statuses.append(
                WPStatus(
                    wp_id=wp_id,
                    worktree_path=expected_path,
                    branch_name=f"{feature_slug}-{wp_id}",
                    is_clean=False,
                    error=error,
                )
            )
            result.errors.append(error)

    # Check all worktrees
    for wt_path, wp_id, branch in wp_workspaces:
        status = check_worktree_status(wt_path, wp_id, branch)
        result.wp_statuses.append(status)
        if not status.is_clean:
            result.passed = False
            result.errors.append(status.error or f"{wp_id} has uncommitted changes")

    # Check target divergence
    diverged, msg = check_target_divergence(target_branch, repo_root)
    result.target_diverged = diverged
    result.target_divergence_msg = msg
    if diverged:
        result.passed = False
        result.errors.append(msg or f"{target_branch} has diverged from origin")

    return result


def x_run_preflight__mutmut_8(
    feature_slug: str,
    target_branch: str,
    repo_root: Path,
    wp_workspaces: list[tuple[Path, str, str]],
) -> PreflightResult:
    """Run all pre-flight checks before merge.

    Args:
        feature_slug: Feature identifier (e.g., "017-smarter-feature-merge")
        target_branch: Branch to merge into (e.g., "main")
        repo_root: Repository root path
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples

    Returns:
        PreflightResult with all check outcomes
    """
    result = PreflightResult(passed=True)

    # Check for missing worktrees based on tasks in kitty-specs
    expected_graph = build_dependency_graph(repo_root / KITTY_SPECS_DIR / feature_slug)
    expected_wps = None
    discovered_wps = {wp_id for _, wp_id, _ in wp_workspaces}
    missing_wps = sorted(expected_wps - discovered_wps)
    if missing_wps:
        for wp_id in missing_wps:
            lane = _wp_lane_from_feature(repo_root, feature_slug, wp_id)
            if lane == "done":
                result.warnings.append(
                    f"Skipping missing worktree check for {wp_id} (lane=done)."
                )
                continue

            result.passed = False
            expected_path = repo_root / WORKTREES_DIR / f"{feature_slug}-{wp_id}"
            error = f"Missing worktree for {wp_id}. Expected at {expected_path.name}. Run: spec-kitty agent workflow implement {wp_id}"
            result.wp_statuses.append(
                WPStatus(
                    wp_id=wp_id,
                    worktree_path=expected_path,
                    branch_name=f"{feature_slug}-{wp_id}",
                    is_clean=False,
                    error=error,
                )
            )
            result.errors.append(error)

    # Check all worktrees
    for wt_path, wp_id, branch in wp_workspaces:
        status = check_worktree_status(wt_path, wp_id, branch)
        result.wp_statuses.append(status)
        if not status.is_clean:
            result.passed = False
            result.errors.append(status.error or f"{wp_id} has uncommitted changes")

    # Check target divergence
    diverged, msg = check_target_divergence(target_branch, repo_root)
    result.target_diverged = diverged
    result.target_divergence_msg = msg
    if diverged:
        result.passed = False
        result.errors.append(msg or f"{target_branch} has diverged from origin")

    return result


def x_run_preflight__mutmut_9(
    feature_slug: str,
    target_branch: str,
    repo_root: Path,
    wp_workspaces: list[tuple[Path, str, str]],
) -> PreflightResult:
    """Run all pre-flight checks before merge.

    Args:
        feature_slug: Feature identifier (e.g., "017-smarter-feature-merge")
        target_branch: Branch to merge into (e.g., "main")
        repo_root: Repository root path
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples

    Returns:
        PreflightResult with all check outcomes
    """
    result = PreflightResult(passed=True)

    # Check for missing worktrees based on tasks in kitty-specs
    expected_graph = build_dependency_graph(repo_root / KITTY_SPECS_DIR / feature_slug)
    expected_wps = set(None)
    discovered_wps = {wp_id for _, wp_id, _ in wp_workspaces}
    missing_wps = sorted(expected_wps - discovered_wps)
    if missing_wps:
        for wp_id in missing_wps:
            lane = _wp_lane_from_feature(repo_root, feature_slug, wp_id)
            if lane == "done":
                result.warnings.append(
                    f"Skipping missing worktree check for {wp_id} (lane=done)."
                )
                continue

            result.passed = False
            expected_path = repo_root / WORKTREES_DIR / f"{feature_slug}-{wp_id}"
            error = f"Missing worktree for {wp_id}. Expected at {expected_path.name}. Run: spec-kitty agent workflow implement {wp_id}"
            result.wp_statuses.append(
                WPStatus(
                    wp_id=wp_id,
                    worktree_path=expected_path,
                    branch_name=f"{feature_slug}-{wp_id}",
                    is_clean=False,
                    error=error,
                )
            )
            result.errors.append(error)

    # Check all worktrees
    for wt_path, wp_id, branch in wp_workspaces:
        status = check_worktree_status(wt_path, wp_id, branch)
        result.wp_statuses.append(status)
        if not status.is_clean:
            result.passed = False
            result.errors.append(status.error or f"{wp_id} has uncommitted changes")

    # Check target divergence
    diverged, msg = check_target_divergence(target_branch, repo_root)
    result.target_diverged = diverged
    result.target_divergence_msg = msg
    if diverged:
        result.passed = False
        result.errors.append(msg or f"{target_branch} has diverged from origin")

    return result


def x_run_preflight__mutmut_10(
    feature_slug: str,
    target_branch: str,
    repo_root: Path,
    wp_workspaces: list[tuple[Path, str, str]],
) -> PreflightResult:
    """Run all pre-flight checks before merge.

    Args:
        feature_slug: Feature identifier (e.g., "017-smarter-feature-merge")
        target_branch: Branch to merge into (e.g., "main")
        repo_root: Repository root path
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples

    Returns:
        PreflightResult with all check outcomes
    """
    result = PreflightResult(passed=True)

    # Check for missing worktrees based on tasks in kitty-specs
    expected_graph = build_dependency_graph(repo_root / KITTY_SPECS_DIR / feature_slug)
    expected_wps = set(expected_graph.keys())
    discovered_wps = None
    missing_wps = sorted(expected_wps - discovered_wps)
    if missing_wps:
        for wp_id in missing_wps:
            lane = _wp_lane_from_feature(repo_root, feature_slug, wp_id)
            if lane == "done":
                result.warnings.append(
                    f"Skipping missing worktree check for {wp_id} (lane=done)."
                )
                continue

            result.passed = False
            expected_path = repo_root / WORKTREES_DIR / f"{feature_slug}-{wp_id}"
            error = f"Missing worktree for {wp_id}. Expected at {expected_path.name}. Run: spec-kitty agent workflow implement {wp_id}"
            result.wp_statuses.append(
                WPStatus(
                    wp_id=wp_id,
                    worktree_path=expected_path,
                    branch_name=f"{feature_slug}-{wp_id}",
                    is_clean=False,
                    error=error,
                )
            )
            result.errors.append(error)

    # Check all worktrees
    for wt_path, wp_id, branch in wp_workspaces:
        status = check_worktree_status(wt_path, wp_id, branch)
        result.wp_statuses.append(status)
        if not status.is_clean:
            result.passed = False
            result.errors.append(status.error or f"{wp_id} has uncommitted changes")

    # Check target divergence
    diverged, msg = check_target_divergence(target_branch, repo_root)
    result.target_diverged = diverged
    result.target_divergence_msg = msg
    if diverged:
        result.passed = False
        result.errors.append(msg or f"{target_branch} has diverged from origin")

    return result


def x_run_preflight__mutmut_11(
    feature_slug: str,
    target_branch: str,
    repo_root: Path,
    wp_workspaces: list[tuple[Path, str, str]],
) -> PreflightResult:
    """Run all pre-flight checks before merge.

    Args:
        feature_slug: Feature identifier (e.g., "017-smarter-feature-merge")
        target_branch: Branch to merge into (e.g., "main")
        repo_root: Repository root path
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples

    Returns:
        PreflightResult with all check outcomes
    """
    result = PreflightResult(passed=True)

    # Check for missing worktrees based on tasks in kitty-specs
    expected_graph = build_dependency_graph(repo_root / KITTY_SPECS_DIR / feature_slug)
    expected_wps = set(expected_graph.keys())
    discovered_wps = {wp_id for _, wp_id, _ in wp_workspaces}
    missing_wps = None
    if missing_wps:
        for wp_id in missing_wps:
            lane = _wp_lane_from_feature(repo_root, feature_slug, wp_id)
            if lane == "done":
                result.warnings.append(
                    f"Skipping missing worktree check for {wp_id} (lane=done)."
                )
                continue

            result.passed = False
            expected_path = repo_root / WORKTREES_DIR / f"{feature_slug}-{wp_id}"
            error = f"Missing worktree for {wp_id}. Expected at {expected_path.name}. Run: spec-kitty agent workflow implement {wp_id}"
            result.wp_statuses.append(
                WPStatus(
                    wp_id=wp_id,
                    worktree_path=expected_path,
                    branch_name=f"{feature_slug}-{wp_id}",
                    is_clean=False,
                    error=error,
                )
            )
            result.errors.append(error)

    # Check all worktrees
    for wt_path, wp_id, branch in wp_workspaces:
        status = check_worktree_status(wt_path, wp_id, branch)
        result.wp_statuses.append(status)
        if not status.is_clean:
            result.passed = False
            result.errors.append(status.error or f"{wp_id} has uncommitted changes")

    # Check target divergence
    diverged, msg = check_target_divergence(target_branch, repo_root)
    result.target_diverged = diverged
    result.target_divergence_msg = msg
    if diverged:
        result.passed = False
        result.errors.append(msg or f"{target_branch} has diverged from origin")

    return result


def x_run_preflight__mutmut_12(
    feature_slug: str,
    target_branch: str,
    repo_root: Path,
    wp_workspaces: list[tuple[Path, str, str]],
) -> PreflightResult:
    """Run all pre-flight checks before merge.

    Args:
        feature_slug: Feature identifier (e.g., "017-smarter-feature-merge")
        target_branch: Branch to merge into (e.g., "main")
        repo_root: Repository root path
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples

    Returns:
        PreflightResult with all check outcomes
    """
    result = PreflightResult(passed=True)

    # Check for missing worktrees based on tasks in kitty-specs
    expected_graph = build_dependency_graph(repo_root / KITTY_SPECS_DIR / feature_slug)
    expected_wps = set(expected_graph.keys())
    discovered_wps = {wp_id for _, wp_id, _ in wp_workspaces}
    missing_wps = sorted(None)
    if missing_wps:
        for wp_id in missing_wps:
            lane = _wp_lane_from_feature(repo_root, feature_slug, wp_id)
            if lane == "done":
                result.warnings.append(
                    f"Skipping missing worktree check for {wp_id} (lane=done)."
                )
                continue

            result.passed = False
            expected_path = repo_root / WORKTREES_DIR / f"{feature_slug}-{wp_id}"
            error = f"Missing worktree for {wp_id}. Expected at {expected_path.name}. Run: spec-kitty agent workflow implement {wp_id}"
            result.wp_statuses.append(
                WPStatus(
                    wp_id=wp_id,
                    worktree_path=expected_path,
                    branch_name=f"{feature_slug}-{wp_id}",
                    is_clean=False,
                    error=error,
                )
            )
            result.errors.append(error)

    # Check all worktrees
    for wt_path, wp_id, branch in wp_workspaces:
        status = check_worktree_status(wt_path, wp_id, branch)
        result.wp_statuses.append(status)
        if not status.is_clean:
            result.passed = False
            result.errors.append(status.error or f"{wp_id} has uncommitted changes")

    # Check target divergence
    diverged, msg = check_target_divergence(target_branch, repo_root)
    result.target_diverged = diverged
    result.target_divergence_msg = msg
    if diverged:
        result.passed = False
        result.errors.append(msg or f"{target_branch} has diverged from origin")

    return result


def x_run_preflight__mutmut_13(
    feature_slug: str,
    target_branch: str,
    repo_root: Path,
    wp_workspaces: list[tuple[Path, str, str]],
) -> PreflightResult:
    """Run all pre-flight checks before merge.

    Args:
        feature_slug: Feature identifier (e.g., "017-smarter-feature-merge")
        target_branch: Branch to merge into (e.g., "main")
        repo_root: Repository root path
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples

    Returns:
        PreflightResult with all check outcomes
    """
    result = PreflightResult(passed=True)

    # Check for missing worktrees based on tasks in kitty-specs
    expected_graph = build_dependency_graph(repo_root / KITTY_SPECS_DIR / feature_slug)
    expected_wps = set(expected_graph.keys())
    discovered_wps = {wp_id for _, wp_id, _ in wp_workspaces}
    missing_wps = sorted(expected_wps + discovered_wps)
    if missing_wps:
        for wp_id in missing_wps:
            lane = _wp_lane_from_feature(repo_root, feature_slug, wp_id)
            if lane == "done":
                result.warnings.append(
                    f"Skipping missing worktree check for {wp_id} (lane=done)."
                )
                continue

            result.passed = False
            expected_path = repo_root / WORKTREES_DIR / f"{feature_slug}-{wp_id}"
            error = f"Missing worktree for {wp_id}. Expected at {expected_path.name}. Run: spec-kitty agent workflow implement {wp_id}"
            result.wp_statuses.append(
                WPStatus(
                    wp_id=wp_id,
                    worktree_path=expected_path,
                    branch_name=f"{feature_slug}-{wp_id}",
                    is_clean=False,
                    error=error,
                )
            )
            result.errors.append(error)

    # Check all worktrees
    for wt_path, wp_id, branch in wp_workspaces:
        status = check_worktree_status(wt_path, wp_id, branch)
        result.wp_statuses.append(status)
        if not status.is_clean:
            result.passed = False
            result.errors.append(status.error or f"{wp_id} has uncommitted changes")

    # Check target divergence
    diverged, msg = check_target_divergence(target_branch, repo_root)
    result.target_diverged = diverged
    result.target_divergence_msg = msg
    if diverged:
        result.passed = False
        result.errors.append(msg or f"{target_branch} has diverged from origin")

    return result


def x_run_preflight__mutmut_14(
    feature_slug: str,
    target_branch: str,
    repo_root: Path,
    wp_workspaces: list[tuple[Path, str, str]],
) -> PreflightResult:
    """Run all pre-flight checks before merge.

    Args:
        feature_slug: Feature identifier (e.g., "017-smarter-feature-merge")
        target_branch: Branch to merge into (e.g., "main")
        repo_root: Repository root path
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples

    Returns:
        PreflightResult with all check outcomes
    """
    result = PreflightResult(passed=True)

    # Check for missing worktrees based on tasks in kitty-specs
    expected_graph = build_dependency_graph(repo_root / KITTY_SPECS_DIR / feature_slug)
    expected_wps = set(expected_graph.keys())
    discovered_wps = {wp_id for _, wp_id, _ in wp_workspaces}
    missing_wps = sorted(expected_wps - discovered_wps)
    if missing_wps:
        for wp_id in missing_wps:
            lane = None
            if lane == "done":
                result.warnings.append(
                    f"Skipping missing worktree check for {wp_id} (lane=done)."
                )
                continue

            result.passed = False
            expected_path = repo_root / WORKTREES_DIR / f"{feature_slug}-{wp_id}"
            error = f"Missing worktree for {wp_id}. Expected at {expected_path.name}. Run: spec-kitty agent workflow implement {wp_id}"
            result.wp_statuses.append(
                WPStatus(
                    wp_id=wp_id,
                    worktree_path=expected_path,
                    branch_name=f"{feature_slug}-{wp_id}",
                    is_clean=False,
                    error=error,
                )
            )
            result.errors.append(error)

    # Check all worktrees
    for wt_path, wp_id, branch in wp_workspaces:
        status = check_worktree_status(wt_path, wp_id, branch)
        result.wp_statuses.append(status)
        if not status.is_clean:
            result.passed = False
            result.errors.append(status.error or f"{wp_id} has uncommitted changes")

    # Check target divergence
    diverged, msg = check_target_divergence(target_branch, repo_root)
    result.target_diverged = diverged
    result.target_divergence_msg = msg
    if diverged:
        result.passed = False
        result.errors.append(msg or f"{target_branch} has diverged from origin")

    return result


def x_run_preflight__mutmut_15(
    feature_slug: str,
    target_branch: str,
    repo_root: Path,
    wp_workspaces: list[tuple[Path, str, str]],
) -> PreflightResult:
    """Run all pre-flight checks before merge.

    Args:
        feature_slug: Feature identifier (e.g., "017-smarter-feature-merge")
        target_branch: Branch to merge into (e.g., "main")
        repo_root: Repository root path
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples

    Returns:
        PreflightResult with all check outcomes
    """
    result = PreflightResult(passed=True)

    # Check for missing worktrees based on tasks in kitty-specs
    expected_graph = build_dependency_graph(repo_root / KITTY_SPECS_DIR / feature_slug)
    expected_wps = set(expected_graph.keys())
    discovered_wps = {wp_id for _, wp_id, _ in wp_workspaces}
    missing_wps = sorted(expected_wps - discovered_wps)
    if missing_wps:
        for wp_id in missing_wps:
            lane = _wp_lane_from_feature(None, feature_slug, wp_id)
            if lane == "done":
                result.warnings.append(
                    f"Skipping missing worktree check for {wp_id} (lane=done)."
                )
                continue

            result.passed = False
            expected_path = repo_root / WORKTREES_DIR / f"{feature_slug}-{wp_id}"
            error = f"Missing worktree for {wp_id}. Expected at {expected_path.name}. Run: spec-kitty agent workflow implement {wp_id}"
            result.wp_statuses.append(
                WPStatus(
                    wp_id=wp_id,
                    worktree_path=expected_path,
                    branch_name=f"{feature_slug}-{wp_id}",
                    is_clean=False,
                    error=error,
                )
            )
            result.errors.append(error)

    # Check all worktrees
    for wt_path, wp_id, branch in wp_workspaces:
        status = check_worktree_status(wt_path, wp_id, branch)
        result.wp_statuses.append(status)
        if not status.is_clean:
            result.passed = False
            result.errors.append(status.error or f"{wp_id} has uncommitted changes")

    # Check target divergence
    diverged, msg = check_target_divergence(target_branch, repo_root)
    result.target_diverged = diverged
    result.target_divergence_msg = msg
    if diverged:
        result.passed = False
        result.errors.append(msg or f"{target_branch} has diverged from origin")

    return result


def x_run_preflight__mutmut_16(
    feature_slug: str,
    target_branch: str,
    repo_root: Path,
    wp_workspaces: list[tuple[Path, str, str]],
) -> PreflightResult:
    """Run all pre-flight checks before merge.

    Args:
        feature_slug: Feature identifier (e.g., "017-smarter-feature-merge")
        target_branch: Branch to merge into (e.g., "main")
        repo_root: Repository root path
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples

    Returns:
        PreflightResult with all check outcomes
    """
    result = PreflightResult(passed=True)

    # Check for missing worktrees based on tasks in kitty-specs
    expected_graph = build_dependency_graph(repo_root / KITTY_SPECS_DIR / feature_slug)
    expected_wps = set(expected_graph.keys())
    discovered_wps = {wp_id for _, wp_id, _ in wp_workspaces}
    missing_wps = sorted(expected_wps - discovered_wps)
    if missing_wps:
        for wp_id in missing_wps:
            lane = _wp_lane_from_feature(repo_root, None, wp_id)
            if lane == "done":
                result.warnings.append(
                    f"Skipping missing worktree check for {wp_id} (lane=done)."
                )
                continue

            result.passed = False
            expected_path = repo_root / WORKTREES_DIR / f"{feature_slug}-{wp_id}"
            error = f"Missing worktree for {wp_id}. Expected at {expected_path.name}. Run: spec-kitty agent workflow implement {wp_id}"
            result.wp_statuses.append(
                WPStatus(
                    wp_id=wp_id,
                    worktree_path=expected_path,
                    branch_name=f"{feature_slug}-{wp_id}",
                    is_clean=False,
                    error=error,
                )
            )
            result.errors.append(error)

    # Check all worktrees
    for wt_path, wp_id, branch in wp_workspaces:
        status = check_worktree_status(wt_path, wp_id, branch)
        result.wp_statuses.append(status)
        if not status.is_clean:
            result.passed = False
            result.errors.append(status.error or f"{wp_id} has uncommitted changes")

    # Check target divergence
    diverged, msg = check_target_divergence(target_branch, repo_root)
    result.target_diverged = diverged
    result.target_divergence_msg = msg
    if diverged:
        result.passed = False
        result.errors.append(msg or f"{target_branch} has diverged from origin")

    return result


def x_run_preflight__mutmut_17(
    feature_slug: str,
    target_branch: str,
    repo_root: Path,
    wp_workspaces: list[tuple[Path, str, str]],
) -> PreflightResult:
    """Run all pre-flight checks before merge.

    Args:
        feature_slug: Feature identifier (e.g., "017-smarter-feature-merge")
        target_branch: Branch to merge into (e.g., "main")
        repo_root: Repository root path
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples

    Returns:
        PreflightResult with all check outcomes
    """
    result = PreflightResult(passed=True)

    # Check for missing worktrees based on tasks in kitty-specs
    expected_graph = build_dependency_graph(repo_root / KITTY_SPECS_DIR / feature_slug)
    expected_wps = set(expected_graph.keys())
    discovered_wps = {wp_id for _, wp_id, _ in wp_workspaces}
    missing_wps = sorted(expected_wps - discovered_wps)
    if missing_wps:
        for wp_id in missing_wps:
            lane = _wp_lane_from_feature(repo_root, feature_slug, None)
            if lane == "done":
                result.warnings.append(
                    f"Skipping missing worktree check for {wp_id} (lane=done)."
                )
                continue

            result.passed = False
            expected_path = repo_root / WORKTREES_DIR / f"{feature_slug}-{wp_id}"
            error = f"Missing worktree for {wp_id}. Expected at {expected_path.name}. Run: spec-kitty agent workflow implement {wp_id}"
            result.wp_statuses.append(
                WPStatus(
                    wp_id=wp_id,
                    worktree_path=expected_path,
                    branch_name=f"{feature_slug}-{wp_id}",
                    is_clean=False,
                    error=error,
                )
            )
            result.errors.append(error)

    # Check all worktrees
    for wt_path, wp_id, branch in wp_workspaces:
        status = check_worktree_status(wt_path, wp_id, branch)
        result.wp_statuses.append(status)
        if not status.is_clean:
            result.passed = False
            result.errors.append(status.error or f"{wp_id} has uncommitted changes")

    # Check target divergence
    diverged, msg = check_target_divergence(target_branch, repo_root)
    result.target_diverged = diverged
    result.target_divergence_msg = msg
    if diverged:
        result.passed = False
        result.errors.append(msg or f"{target_branch} has diverged from origin")

    return result


def x_run_preflight__mutmut_18(
    feature_slug: str,
    target_branch: str,
    repo_root: Path,
    wp_workspaces: list[tuple[Path, str, str]],
) -> PreflightResult:
    """Run all pre-flight checks before merge.

    Args:
        feature_slug: Feature identifier (e.g., "017-smarter-feature-merge")
        target_branch: Branch to merge into (e.g., "main")
        repo_root: Repository root path
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples

    Returns:
        PreflightResult with all check outcomes
    """
    result = PreflightResult(passed=True)

    # Check for missing worktrees based on tasks in kitty-specs
    expected_graph = build_dependency_graph(repo_root / KITTY_SPECS_DIR / feature_slug)
    expected_wps = set(expected_graph.keys())
    discovered_wps = {wp_id for _, wp_id, _ in wp_workspaces}
    missing_wps = sorted(expected_wps - discovered_wps)
    if missing_wps:
        for wp_id in missing_wps:
            lane = _wp_lane_from_feature(feature_slug, wp_id)
            if lane == "done":
                result.warnings.append(
                    f"Skipping missing worktree check for {wp_id} (lane=done)."
                )
                continue

            result.passed = False
            expected_path = repo_root / WORKTREES_DIR / f"{feature_slug}-{wp_id}"
            error = f"Missing worktree for {wp_id}. Expected at {expected_path.name}. Run: spec-kitty agent workflow implement {wp_id}"
            result.wp_statuses.append(
                WPStatus(
                    wp_id=wp_id,
                    worktree_path=expected_path,
                    branch_name=f"{feature_slug}-{wp_id}",
                    is_clean=False,
                    error=error,
                )
            )
            result.errors.append(error)

    # Check all worktrees
    for wt_path, wp_id, branch in wp_workspaces:
        status = check_worktree_status(wt_path, wp_id, branch)
        result.wp_statuses.append(status)
        if not status.is_clean:
            result.passed = False
            result.errors.append(status.error or f"{wp_id} has uncommitted changes")

    # Check target divergence
    diverged, msg = check_target_divergence(target_branch, repo_root)
    result.target_diverged = diverged
    result.target_divergence_msg = msg
    if diverged:
        result.passed = False
        result.errors.append(msg or f"{target_branch} has diverged from origin")

    return result


def x_run_preflight__mutmut_19(
    feature_slug: str,
    target_branch: str,
    repo_root: Path,
    wp_workspaces: list[tuple[Path, str, str]],
) -> PreflightResult:
    """Run all pre-flight checks before merge.

    Args:
        feature_slug: Feature identifier (e.g., "017-smarter-feature-merge")
        target_branch: Branch to merge into (e.g., "main")
        repo_root: Repository root path
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples

    Returns:
        PreflightResult with all check outcomes
    """
    result = PreflightResult(passed=True)

    # Check for missing worktrees based on tasks in kitty-specs
    expected_graph = build_dependency_graph(repo_root / KITTY_SPECS_DIR / feature_slug)
    expected_wps = set(expected_graph.keys())
    discovered_wps = {wp_id for _, wp_id, _ in wp_workspaces}
    missing_wps = sorted(expected_wps - discovered_wps)
    if missing_wps:
        for wp_id in missing_wps:
            lane = _wp_lane_from_feature(repo_root, wp_id)
            if lane == "done":
                result.warnings.append(
                    f"Skipping missing worktree check for {wp_id} (lane=done)."
                )
                continue

            result.passed = False
            expected_path = repo_root / WORKTREES_DIR / f"{feature_slug}-{wp_id}"
            error = f"Missing worktree for {wp_id}. Expected at {expected_path.name}. Run: spec-kitty agent workflow implement {wp_id}"
            result.wp_statuses.append(
                WPStatus(
                    wp_id=wp_id,
                    worktree_path=expected_path,
                    branch_name=f"{feature_slug}-{wp_id}",
                    is_clean=False,
                    error=error,
                )
            )
            result.errors.append(error)

    # Check all worktrees
    for wt_path, wp_id, branch in wp_workspaces:
        status = check_worktree_status(wt_path, wp_id, branch)
        result.wp_statuses.append(status)
        if not status.is_clean:
            result.passed = False
            result.errors.append(status.error or f"{wp_id} has uncommitted changes")

    # Check target divergence
    diverged, msg = check_target_divergence(target_branch, repo_root)
    result.target_diverged = diverged
    result.target_divergence_msg = msg
    if diverged:
        result.passed = False
        result.errors.append(msg or f"{target_branch} has diverged from origin")

    return result


def x_run_preflight__mutmut_20(
    feature_slug: str,
    target_branch: str,
    repo_root: Path,
    wp_workspaces: list[tuple[Path, str, str]],
) -> PreflightResult:
    """Run all pre-flight checks before merge.

    Args:
        feature_slug: Feature identifier (e.g., "017-smarter-feature-merge")
        target_branch: Branch to merge into (e.g., "main")
        repo_root: Repository root path
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples

    Returns:
        PreflightResult with all check outcomes
    """
    result = PreflightResult(passed=True)

    # Check for missing worktrees based on tasks in kitty-specs
    expected_graph = build_dependency_graph(repo_root / KITTY_SPECS_DIR / feature_slug)
    expected_wps = set(expected_graph.keys())
    discovered_wps = {wp_id for _, wp_id, _ in wp_workspaces}
    missing_wps = sorted(expected_wps - discovered_wps)
    if missing_wps:
        for wp_id in missing_wps:
            lane = _wp_lane_from_feature(repo_root, feature_slug, )
            if lane == "done":
                result.warnings.append(
                    f"Skipping missing worktree check for {wp_id} (lane=done)."
                )
                continue

            result.passed = False
            expected_path = repo_root / WORKTREES_DIR / f"{feature_slug}-{wp_id}"
            error = f"Missing worktree for {wp_id}. Expected at {expected_path.name}. Run: spec-kitty agent workflow implement {wp_id}"
            result.wp_statuses.append(
                WPStatus(
                    wp_id=wp_id,
                    worktree_path=expected_path,
                    branch_name=f"{feature_slug}-{wp_id}",
                    is_clean=False,
                    error=error,
                )
            )
            result.errors.append(error)

    # Check all worktrees
    for wt_path, wp_id, branch in wp_workspaces:
        status = check_worktree_status(wt_path, wp_id, branch)
        result.wp_statuses.append(status)
        if not status.is_clean:
            result.passed = False
            result.errors.append(status.error or f"{wp_id} has uncommitted changes")

    # Check target divergence
    diverged, msg = check_target_divergence(target_branch, repo_root)
    result.target_diverged = diverged
    result.target_divergence_msg = msg
    if diverged:
        result.passed = False
        result.errors.append(msg or f"{target_branch} has diverged from origin")

    return result


def x_run_preflight__mutmut_21(
    feature_slug: str,
    target_branch: str,
    repo_root: Path,
    wp_workspaces: list[tuple[Path, str, str]],
) -> PreflightResult:
    """Run all pre-flight checks before merge.

    Args:
        feature_slug: Feature identifier (e.g., "017-smarter-feature-merge")
        target_branch: Branch to merge into (e.g., "main")
        repo_root: Repository root path
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples

    Returns:
        PreflightResult with all check outcomes
    """
    result = PreflightResult(passed=True)

    # Check for missing worktrees based on tasks in kitty-specs
    expected_graph = build_dependency_graph(repo_root / KITTY_SPECS_DIR / feature_slug)
    expected_wps = set(expected_graph.keys())
    discovered_wps = {wp_id for _, wp_id, _ in wp_workspaces}
    missing_wps = sorted(expected_wps - discovered_wps)
    if missing_wps:
        for wp_id in missing_wps:
            lane = _wp_lane_from_feature(repo_root, feature_slug, wp_id)
            if lane != "done":
                result.warnings.append(
                    f"Skipping missing worktree check for {wp_id} (lane=done)."
                )
                continue

            result.passed = False
            expected_path = repo_root / WORKTREES_DIR / f"{feature_slug}-{wp_id}"
            error = f"Missing worktree for {wp_id}. Expected at {expected_path.name}. Run: spec-kitty agent workflow implement {wp_id}"
            result.wp_statuses.append(
                WPStatus(
                    wp_id=wp_id,
                    worktree_path=expected_path,
                    branch_name=f"{feature_slug}-{wp_id}",
                    is_clean=False,
                    error=error,
                )
            )
            result.errors.append(error)

    # Check all worktrees
    for wt_path, wp_id, branch in wp_workspaces:
        status = check_worktree_status(wt_path, wp_id, branch)
        result.wp_statuses.append(status)
        if not status.is_clean:
            result.passed = False
            result.errors.append(status.error or f"{wp_id} has uncommitted changes")

    # Check target divergence
    diverged, msg = check_target_divergence(target_branch, repo_root)
    result.target_diverged = diverged
    result.target_divergence_msg = msg
    if diverged:
        result.passed = False
        result.errors.append(msg or f"{target_branch} has diverged from origin")

    return result


def x_run_preflight__mutmut_22(
    feature_slug: str,
    target_branch: str,
    repo_root: Path,
    wp_workspaces: list[tuple[Path, str, str]],
) -> PreflightResult:
    """Run all pre-flight checks before merge.

    Args:
        feature_slug: Feature identifier (e.g., "017-smarter-feature-merge")
        target_branch: Branch to merge into (e.g., "main")
        repo_root: Repository root path
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples

    Returns:
        PreflightResult with all check outcomes
    """
    result = PreflightResult(passed=True)

    # Check for missing worktrees based on tasks in kitty-specs
    expected_graph = build_dependency_graph(repo_root / KITTY_SPECS_DIR / feature_slug)
    expected_wps = set(expected_graph.keys())
    discovered_wps = {wp_id for _, wp_id, _ in wp_workspaces}
    missing_wps = sorted(expected_wps - discovered_wps)
    if missing_wps:
        for wp_id in missing_wps:
            lane = _wp_lane_from_feature(repo_root, feature_slug, wp_id)
            if lane == "XXdoneXX":
                result.warnings.append(
                    f"Skipping missing worktree check for {wp_id} (lane=done)."
                )
                continue

            result.passed = False
            expected_path = repo_root / WORKTREES_DIR / f"{feature_slug}-{wp_id}"
            error = f"Missing worktree for {wp_id}. Expected at {expected_path.name}. Run: spec-kitty agent workflow implement {wp_id}"
            result.wp_statuses.append(
                WPStatus(
                    wp_id=wp_id,
                    worktree_path=expected_path,
                    branch_name=f"{feature_slug}-{wp_id}",
                    is_clean=False,
                    error=error,
                )
            )
            result.errors.append(error)

    # Check all worktrees
    for wt_path, wp_id, branch in wp_workspaces:
        status = check_worktree_status(wt_path, wp_id, branch)
        result.wp_statuses.append(status)
        if not status.is_clean:
            result.passed = False
            result.errors.append(status.error or f"{wp_id} has uncommitted changes")

    # Check target divergence
    diverged, msg = check_target_divergence(target_branch, repo_root)
    result.target_diverged = diverged
    result.target_divergence_msg = msg
    if diverged:
        result.passed = False
        result.errors.append(msg or f"{target_branch} has diverged from origin")

    return result


def x_run_preflight__mutmut_23(
    feature_slug: str,
    target_branch: str,
    repo_root: Path,
    wp_workspaces: list[tuple[Path, str, str]],
) -> PreflightResult:
    """Run all pre-flight checks before merge.

    Args:
        feature_slug: Feature identifier (e.g., "017-smarter-feature-merge")
        target_branch: Branch to merge into (e.g., "main")
        repo_root: Repository root path
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples

    Returns:
        PreflightResult with all check outcomes
    """
    result = PreflightResult(passed=True)

    # Check for missing worktrees based on tasks in kitty-specs
    expected_graph = build_dependency_graph(repo_root / KITTY_SPECS_DIR / feature_slug)
    expected_wps = set(expected_graph.keys())
    discovered_wps = {wp_id for _, wp_id, _ in wp_workspaces}
    missing_wps = sorted(expected_wps - discovered_wps)
    if missing_wps:
        for wp_id in missing_wps:
            lane = _wp_lane_from_feature(repo_root, feature_slug, wp_id)
            if lane == "DONE":
                result.warnings.append(
                    f"Skipping missing worktree check for {wp_id} (lane=done)."
                )
                continue

            result.passed = False
            expected_path = repo_root / WORKTREES_DIR / f"{feature_slug}-{wp_id}"
            error = f"Missing worktree for {wp_id}. Expected at {expected_path.name}. Run: spec-kitty agent workflow implement {wp_id}"
            result.wp_statuses.append(
                WPStatus(
                    wp_id=wp_id,
                    worktree_path=expected_path,
                    branch_name=f"{feature_slug}-{wp_id}",
                    is_clean=False,
                    error=error,
                )
            )
            result.errors.append(error)

    # Check all worktrees
    for wt_path, wp_id, branch in wp_workspaces:
        status = check_worktree_status(wt_path, wp_id, branch)
        result.wp_statuses.append(status)
        if not status.is_clean:
            result.passed = False
            result.errors.append(status.error or f"{wp_id} has uncommitted changes")

    # Check target divergence
    diverged, msg = check_target_divergence(target_branch, repo_root)
    result.target_diverged = diverged
    result.target_divergence_msg = msg
    if diverged:
        result.passed = False
        result.errors.append(msg or f"{target_branch} has diverged from origin")

    return result


def x_run_preflight__mutmut_24(
    feature_slug: str,
    target_branch: str,
    repo_root: Path,
    wp_workspaces: list[tuple[Path, str, str]],
) -> PreflightResult:
    """Run all pre-flight checks before merge.

    Args:
        feature_slug: Feature identifier (e.g., "017-smarter-feature-merge")
        target_branch: Branch to merge into (e.g., "main")
        repo_root: Repository root path
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples

    Returns:
        PreflightResult with all check outcomes
    """
    result = PreflightResult(passed=True)

    # Check for missing worktrees based on tasks in kitty-specs
    expected_graph = build_dependency_graph(repo_root / KITTY_SPECS_DIR / feature_slug)
    expected_wps = set(expected_graph.keys())
    discovered_wps = {wp_id for _, wp_id, _ in wp_workspaces}
    missing_wps = sorted(expected_wps - discovered_wps)
    if missing_wps:
        for wp_id in missing_wps:
            lane = _wp_lane_from_feature(repo_root, feature_slug, wp_id)
            if lane == "done":
                result.warnings.append(
                    None
                )
                continue

            result.passed = False
            expected_path = repo_root / WORKTREES_DIR / f"{feature_slug}-{wp_id}"
            error = f"Missing worktree for {wp_id}. Expected at {expected_path.name}. Run: spec-kitty agent workflow implement {wp_id}"
            result.wp_statuses.append(
                WPStatus(
                    wp_id=wp_id,
                    worktree_path=expected_path,
                    branch_name=f"{feature_slug}-{wp_id}",
                    is_clean=False,
                    error=error,
                )
            )
            result.errors.append(error)

    # Check all worktrees
    for wt_path, wp_id, branch in wp_workspaces:
        status = check_worktree_status(wt_path, wp_id, branch)
        result.wp_statuses.append(status)
        if not status.is_clean:
            result.passed = False
            result.errors.append(status.error or f"{wp_id} has uncommitted changes")

    # Check target divergence
    diverged, msg = check_target_divergence(target_branch, repo_root)
    result.target_diverged = diverged
    result.target_divergence_msg = msg
    if diverged:
        result.passed = False
        result.errors.append(msg or f"{target_branch} has diverged from origin")

    return result


def x_run_preflight__mutmut_25(
    feature_slug: str,
    target_branch: str,
    repo_root: Path,
    wp_workspaces: list[tuple[Path, str, str]],
) -> PreflightResult:
    """Run all pre-flight checks before merge.

    Args:
        feature_slug: Feature identifier (e.g., "017-smarter-feature-merge")
        target_branch: Branch to merge into (e.g., "main")
        repo_root: Repository root path
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples

    Returns:
        PreflightResult with all check outcomes
    """
    result = PreflightResult(passed=True)

    # Check for missing worktrees based on tasks in kitty-specs
    expected_graph = build_dependency_graph(repo_root / KITTY_SPECS_DIR / feature_slug)
    expected_wps = set(expected_graph.keys())
    discovered_wps = {wp_id for _, wp_id, _ in wp_workspaces}
    missing_wps = sorted(expected_wps - discovered_wps)
    if missing_wps:
        for wp_id in missing_wps:
            lane = _wp_lane_from_feature(repo_root, feature_slug, wp_id)
            if lane == "done":
                result.warnings.append(
                    f"Skipping missing worktree check for {wp_id} (lane=done)."
                )
                break

            result.passed = False
            expected_path = repo_root / WORKTREES_DIR / f"{feature_slug}-{wp_id}"
            error = f"Missing worktree for {wp_id}. Expected at {expected_path.name}. Run: spec-kitty agent workflow implement {wp_id}"
            result.wp_statuses.append(
                WPStatus(
                    wp_id=wp_id,
                    worktree_path=expected_path,
                    branch_name=f"{feature_slug}-{wp_id}",
                    is_clean=False,
                    error=error,
                )
            )
            result.errors.append(error)

    # Check all worktrees
    for wt_path, wp_id, branch in wp_workspaces:
        status = check_worktree_status(wt_path, wp_id, branch)
        result.wp_statuses.append(status)
        if not status.is_clean:
            result.passed = False
            result.errors.append(status.error or f"{wp_id} has uncommitted changes")

    # Check target divergence
    diverged, msg = check_target_divergence(target_branch, repo_root)
    result.target_diverged = diverged
    result.target_divergence_msg = msg
    if diverged:
        result.passed = False
        result.errors.append(msg or f"{target_branch} has diverged from origin")

    return result


def x_run_preflight__mutmut_26(
    feature_slug: str,
    target_branch: str,
    repo_root: Path,
    wp_workspaces: list[tuple[Path, str, str]],
) -> PreflightResult:
    """Run all pre-flight checks before merge.

    Args:
        feature_slug: Feature identifier (e.g., "017-smarter-feature-merge")
        target_branch: Branch to merge into (e.g., "main")
        repo_root: Repository root path
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples

    Returns:
        PreflightResult with all check outcomes
    """
    result = PreflightResult(passed=True)

    # Check for missing worktrees based on tasks in kitty-specs
    expected_graph = build_dependency_graph(repo_root / KITTY_SPECS_DIR / feature_slug)
    expected_wps = set(expected_graph.keys())
    discovered_wps = {wp_id for _, wp_id, _ in wp_workspaces}
    missing_wps = sorted(expected_wps - discovered_wps)
    if missing_wps:
        for wp_id in missing_wps:
            lane = _wp_lane_from_feature(repo_root, feature_slug, wp_id)
            if lane == "done":
                result.warnings.append(
                    f"Skipping missing worktree check for {wp_id} (lane=done)."
                )
                continue

            result.passed = None
            expected_path = repo_root / WORKTREES_DIR / f"{feature_slug}-{wp_id}"
            error = f"Missing worktree for {wp_id}. Expected at {expected_path.name}. Run: spec-kitty agent workflow implement {wp_id}"
            result.wp_statuses.append(
                WPStatus(
                    wp_id=wp_id,
                    worktree_path=expected_path,
                    branch_name=f"{feature_slug}-{wp_id}",
                    is_clean=False,
                    error=error,
                )
            )
            result.errors.append(error)

    # Check all worktrees
    for wt_path, wp_id, branch in wp_workspaces:
        status = check_worktree_status(wt_path, wp_id, branch)
        result.wp_statuses.append(status)
        if not status.is_clean:
            result.passed = False
            result.errors.append(status.error or f"{wp_id} has uncommitted changes")

    # Check target divergence
    diverged, msg = check_target_divergence(target_branch, repo_root)
    result.target_diverged = diverged
    result.target_divergence_msg = msg
    if diverged:
        result.passed = False
        result.errors.append(msg or f"{target_branch} has diverged from origin")

    return result


def x_run_preflight__mutmut_27(
    feature_slug: str,
    target_branch: str,
    repo_root: Path,
    wp_workspaces: list[tuple[Path, str, str]],
) -> PreflightResult:
    """Run all pre-flight checks before merge.

    Args:
        feature_slug: Feature identifier (e.g., "017-smarter-feature-merge")
        target_branch: Branch to merge into (e.g., "main")
        repo_root: Repository root path
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples

    Returns:
        PreflightResult with all check outcomes
    """
    result = PreflightResult(passed=True)

    # Check for missing worktrees based on tasks in kitty-specs
    expected_graph = build_dependency_graph(repo_root / KITTY_SPECS_DIR / feature_slug)
    expected_wps = set(expected_graph.keys())
    discovered_wps = {wp_id for _, wp_id, _ in wp_workspaces}
    missing_wps = sorted(expected_wps - discovered_wps)
    if missing_wps:
        for wp_id in missing_wps:
            lane = _wp_lane_from_feature(repo_root, feature_slug, wp_id)
            if lane == "done":
                result.warnings.append(
                    f"Skipping missing worktree check for {wp_id} (lane=done)."
                )
                continue

            result.passed = True
            expected_path = repo_root / WORKTREES_DIR / f"{feature_slug}-{wp_id}"
            error = f"Missing worktree for {wp_id}. Expected at {expected_path.name}. Run: spec-kitty agent workflow implement {wp_id}"
            result.wp_statuses.append(
                WPStatus(
                    wp_id=wp_id,
                    worktree_path=expected_path,
                    branch_name=f"{feature_slug}-{wp_id}",
                    is_clean=False,
                    error=error,
                )
            )
            result.errors.append(error)

    # Check all worktrees
    for wt_path, wp_id, branch in wp_workspaces:
        status = check_worktree_status(wt_path, wp_id, branch)
        result.wp_statuses.append(status)
        if not status.is_clean:
            result.passed = False
            result.errors.append(status.error or f"{wp_id} has uncommitted changes")

    # Check target divergence
    diverged, msg = check_target_divergence(target_branch, repo_root)
    result.target_diverged = diverged
    result.target_divergence_msg = msg
    if diverged:
        result.passed = False
        result.errors.append(msg or f"{target_branch} has diverged from origin")

    return result


def x_run_preflight__mutmut_28(
    feature_slug: str,
    target_branch: str,
    repo_root: Path,
    wp_workspaces: list[tuple[Path, str, str]],
) -> PreflightResult:
    """Run all pre-flight checks before merge.

    Args:
        feature_slug: Feature identifier (e.g., "017-smarter-feature-merge")
        target_branch: Branch to merge into (e.g., "main")
        repo_root: Repository root path
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples

    Returns:
        PreflightResult with all check outcomes
    """
    result = PreflightResult(passed=True)

    # Check for missing worktrees based on tasks in kitty-specs
    expected_graph = build_dependency_graph(repo_root / KITTY_SPECS_DIR / feature_slug)
    expected_wps = set(expected_graph.keys())
    discovered_wps = {wp_id for _, wp_id, _ in wp_workspaces}
    missing_wps = sorted(expected_wps - discovered_wps)
    if missing_wps:
        for wp_id in missing_wps:
            lane = _wp_lane_from_feature(repo_root, feature_slug, wp_id)
            if lane == "done":
                result.warnings.append(
                    f"Skipping missing worktree check for {wp_id} (lane=done)."
                )
                continue

            result.passed = False
            expected_path = None
            error = f"Missing worktree for {wp_id}. Expected at {expected_path.name}. Run: spec-kitty agent workflow implement {wp_id}"
            result.wp_statuses.append(
                WPStatus(
                    wp_id=wp_id,
                    worktree_path=expected_path,
                    branch_name=f"{feature_slug}-{wp_id}",
                    is_clean=False,
                    error=error,
                )
            )
            result.errors.append(error)

    # Check all worktrees
    for wt_path, wp_id, branch in wp_workspaces:
        status = check_worktree_status(wt_path, wp_id, branch)
        result.wp_statuses.append(status)
        if not status.is_clean:
            result.passed = False
            result.errors.append(status.error or f"{wp_id} has uncommitted changes")

    # Check target divergence
    diverged, msg = check_target_divergence(target_branch, repo_root)
    result.target_diverged = diverged
    result.target_divergence_msg = msg
    if diverged:
        result.passed = False
        result.errors.append(msg or f"{target_branch} has diverged from origin")

    return result


def x_run_preflight__mutmut_29(
    feature_slug: str,
    target_branch: str,
    repo_root: Path,
    wp_workspaces: list[tuple[Path, str, str]],
) -> PreflightResult:
    """Run all pre-flight checks before merge.

    Args:
        feature_slug: Feature identifier (e.g., "017-smarter-feature-merge")
        target_branch: Branch to merge into (e.g., "main")
        repo_root: Repository root path
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples

    Returns:
        PreflightResult with all check outcomes
    """
    result = PreflightResult(passed=True)

    # Check for missing worktrees based on tasks in kitty-specs
    expected_graph = build_dependency_graph(repo_root / KITTY_SPECS_DIR / feature_slug)
    expected_wps = set(expected_graph.keys())
    discovered_wps = {wp_id for _, wp_id, _ in wp_workspaces}
    missing_wps = sorted(expected_wps - discovered_wps)
    if missing_wps:
        for wp_id in missing_wps:
            lane = _wp_lane_from_feature(repo_root, feature_slug, wp_id)
            if lane == "done":
                result.warnings.append(
                    f"Skipping missing worktree check for {wp_id} (lane=done)."
                )
                continue

            result.passed = False
            expected_path = repo_root / WORKTREES_DIR * f"{feature_slug}-{wp_id}"
            error = f"Missing worktree for {wp_id}. Expected at {expected_path.name}. Run: spec-kitty agent workflow implement {wp_id}"
            result.wp_statuses.append(
                WPStatus(
                    wp_id=wp_id,
                    worktree_path=expected_path,
                    branch_name=f"{feature_slug}-{wp_id}",
                    is_clean=False,
                    error=error,
                )
            )
            result.errors.append(error)

    # Check all worktrees
    for wt_path, wp_id, branch in wp_workspaces:
        status = check_worktree_status(wt_path, wp_id, branch)
        result.wp_statuses.append(status)
        if not status.is_clean:
            result.passed = False
            result.errors.append(status.error or f"{wp_id} has uncommitted changes")

    # Check target divergence
    diverged, msg = check_target_divergence(target_branch, repo_root)
    result.target_diverged = diverged
    result.target_divergence_msg = msg
    if diverged:
        result.passed = False
        result.errors.append(msg or f"{target_branch} has diverged from origin")

    return result


def x_run_preflight__mutmut_30(
    feature_slug: str,
    target_branch: str,
    repo_root: Path,
    wp_workspaces: list[tuple[Path, str, str]],
) -> PreflightResult:
    """Run all pre-flight checks before merge.

    Args:
        feature_slug: Feature identifier (e.g., "017-smarter-feature-merge")
        target_branch: Branch to merge into (e.g., "main")
        repo_root: Repository root path
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples

    Returns:
        PreflightResult with all check outcomes
    """
    result = PreflightResult(passed=True)

    # Check for missing worktrees based on tasks in kitty-specs
    expected_graph = build_dependency_graph(repo_root / KITTY_SPECS_DIR / feature_slug)
    expected_wps = set(expected_graph.keys())
    discovered_wps = {wp_id for _, wp_id, _ in wp_workspaces}
    missing_wps = sorted(expected_wps - discovered_wps)
    if missing_wps:
        for wp_id in missing_wps:
            lane = _wp_lane_from_feature(repo_root, feature_slug, wp_id)
            if lane == "done":
                result.warnings.append(
                    f"Skipping missing worktree check for {wp_id} (lane=done)."
                )
                continue

            result.passed = False
            expected_path = repo_root * WORKTREES_DIR / f"{feature_slug}-{wp_id}"
            error = f"Missing worktree for {wp_id}. Expected at {expected_path.name}. Run: spec-kitty agent workflow implement {wp_id}"
            result.wp_statuses.append(
                WPStatus(
                    wp_id=wp_id,
                    worktree_path=expected_path,
                    branch_name=f"{feature_slug}-{wp_id}",
                    is_clean=False,
                    error=error,
                )
            )
            result.errors.append(error)

    # Check all worktrees
    for wt_path, wp_id, branch in wp_workspaces:
        status = check_worktree_status(wt_path, wp_id, branch)
        result.wp_statuses.append(status)
        if not status.is_clean:
            result.passed = False
            result.errors.append(status.error or f"{wp_id} has uncommitted changes")

    # Check target divergence
    diverged, msg = check_target_divergence(target_branch, repo_root)
    result.target_diverged = diverged
    result.target_divergence_msg = msg
    if diverged:
        result.passed = False
        result.errors.append(msg or f"{target_branch} has diverged from origin")

    return result


def x_run_preflight__mutmut_31(
    feature_slug: str,
    target_branch: str,
    repo_root: Path,
    wp_workspaces: list[tuple[Path, str, str]],
) -> PreflightResult:
    """Run all pre-flight checks before merge.

    Args:
        feature_slug: Feature identifier (e.g., "017-smarter-feature-merge")
        target_branch: Branch to merge into (e.g., "main")
        repo_root: Repository root path
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples

    Returns:
        PreflightResult with all check outcomes
    """
    result = PreflightResult(passed=True)

    # Check for missing worktrees based on tasks in kitty-specs
    expected_graph = build_dependency_graph(repo_root / KITTY_SPECS_DIR / feature_slug)
    expected_wps = set(expected_graph.keys())
    discovered_wps = {wp_id for _, wp_id, _ in wp_workspaces}
    missing_wps = sorted(expected_wps - discovered_wps)
    if missing_wps:
        for wp_id in missing_wps:
            lane = _wp_lane_from_feature(repo_root, feature_slug, wp_id)
            if lane == "done":
                result.warnings.append(
                    f"Skipping missing worktree check for {wp_id} (lane=done)."
                )
                continue

            result.passed = False
            expected_path = repo_root / WORKTREES_DIR / f"{feature_slug}-{wp_id}"
            error = None
            result.wp_statuses.append(
                WPStatus(
                    wp_id=wp_id,
                    worktree_path=expected_path,
                    branch_name=f"{feature_slug}-{wp_id}",
                    is_clean=False,
                    error=error,
                )
            )
            result.errors.append(error)

    # Check all worktrees
    for wt_path, wp_id, branch in wp_workspaces:
        status = check_worktree_status(wt_path, wp_id, branch)
        result.wp_statuses.append(status)
        if not status.is_clean:
            result.passed = False
            result.errors.append(status.error or f"{wp_id} has uncommitted changes")

    # Check target divergence
    diverged, msg = check_target_divergence(target_branch, repo_root)
    result.target_diverged = diverged
    result.target_divergence_msg = msg
    if diverged:
        result.passed = False
        result.errors.append(msg or f"{target_branch} has diverged from origin")

    return result


def x_run_preflight__mutmut_32(
    feature_slug: str,
    target_branch: str,
    repo_root: Path,
    wp_workspaces: list[tuple[Path, str, str]],
) -> PreflightResult:
    """Run all pre-flight checks before merge.

    Args:
        feature_slug: Feature identifier (e.g., "017-smarter-feature-merge")
        target_branch: Branch to merge into (e.g., "main")
        repo_root: Repository root path
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples

    Returns:
        PreflightResult with all check outcomes
    """
    result = PreflightResult(passed=True)

    # Check for missing worktrees based on tasks in kitty-specs
    expected_graph = build_dependency_graph(repo_root / KITTY_SPECS_DIR / feature_slug)
    expected_wps = set(expected_graph.keys())
    discovered_wps = {wp_id for _, wp_id, _ in wp_workspaces}
    missing_wps = sorted(expected_wps - discovered_wps)
    if missing_wps:
        for wp_id in missing_wps:
            lane = _wp_lane_from_feature(repo_root, feature_slug, wp_id)
            if lane == "done":
                result.warnings.append(
                    f"Skipping missing worktree check for {wp_id} (lane=done)."
                )
                continue

            result.passed = False
            expected_path = repo_root / WORKTREES_DIR / f"{feature_slug}-{wp_id}"
            error = f"Missing worktree for {wp_id}. Expected at {expected_path.name}. Run: spec-kitty agent workflow implement {wp_id}"
            result.wp_statuses.append(
                None
            )
            result.errors.append(error)

    # Check all worktrees
    for wt_path, wp_id, branch in wp_workspaces:
        status = check_worktree_status(wt_path, wp_id, branch)
        result.wp_statuses.append(status)
        if not status.is_clean:
            result.passed = False
            result.errors.append(status.error or f"{wp_id} has uncommitted changes")

    # Check target divergence
    diverged, msg = check_target_divergence(target_branch, repo_root)
    result.target_diverged = diverged
    result.target_divergence_msg = msg
    if diverged:
        result.passed = False
        result.errors.append(msg or f"{target_branch} has diverged from origin")

    return result


def x_run_preflight__mutmut_33(
    feature_slug: str,
    target_branch: str,
    repo_root: Path,
    wp_workspaces: list[tuple[Path, str, str]],
) -> PreflightResult:
    """Run all pre-flight checks before merge.

    Args:
        feature_slug: Feature identifier (e.g., "017-smarter-feature-merge")
        target_branch: Branch to merge into (e.g., "main")
        repo_root: Repository root path
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples

    Returns:
        PreflightResult with all check outcomes
    """
    result = PreflightResult(passed=True)

    # Check for missing worktrees based on tasks in kitty-specs
    expected_graph = build_dependency_graph(repo_root / KITTY_SPECS_DIR / feature_slug)
    expected_wps = set(expected_graph.keys())
    discovered_wps = {wp_id for _, wp_id, _ in wp_workspaces}
    missing_wps = sorted(expected_wps - discovered_wps)
    if missing_wps:
        for wp_id in missing_wps:
            lane = _wp_lane_from_feature(repo_root, feature_slug, wp_id)
            if lane == "done":
                result.warnings.append(
                    f"Skipping missing worktree check for {wp_id} (lane=done)."
                )
                continue

            result.passed = False
            expected_path = repo_root / WORKTREES_DIR / f"{feature_slug}-{wp_id}"
            error = f"Missing worktree for {wp_id}. Expected at {expected_path.name}. Run: spec-kitty agent workflow implement {wp_id}"
            result.wp_statuses.append(
                WPStatus(
                    wp_id=None,
                    worktree_path=expected_path,
                    branch_name=f"{feature_slug}-{wp_id}",
                    is_clean=False,
                    error=error,
                )
            )
            result.errors.append(error)

    # Check all worktrees
    for wt_path, wp_id, branch in wp_workspaces:
        status = check_worktree_status(wt_path, wp_id, branch)
        result.wp_statuses.append(status)
        if not status.is_clean:
            result.passed = False
            result.errors.append(status.error or f"{wp_id} has uncommitted changes")

    # Check target divergence
    diverged, msg = check_target_divergence(target_branch, repo_root)
    result.target_diverged = diverged
    result.target_divergence_msg = msg
    if diverged:
        result.passed = False
        result.errors.append(msg or f"{target_branch} has diverged from origin")

    return result


def x_run_preflight__mutmut_34(
    feature_slug: str,
    target_branch: str,
    repo_root: Path,
    wp_workspaces: list[tuple[Path, str, str]],
) -> PreflightResult:
    """Run all pre-flight checks before merge.

    Args:
        feature_slug: Feature identifier (e.g., "017-smarter-feature-merge")
        target_branch: Branch to merge into (e.g., "main")
        repo_root: Repository root path
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples

    Returns:
        PreflightResult with all check outcomes
    """
    result = PreflightResult(passed=True)

    # Check for missing worktrees based on tasks in kitty-specs
    expected_graph = build_dependency_graph(repo_root / KITTY_SPECS_DIR / feature_slug)
    expected_wps = set(expected_graph.keys())
    discovered_wps = {wp_id for _, wp_id, _ in wp_workspaces}
    missing_wps = sorted(expected_wps - discovered_wps)
    if missing_wps:
        for wp_id in missing_wps:
            lane = _wp_lane_from_feature(repo_root, feature_slug, wp_id)
            if lane == "done":
                result.warnings.append(
                    f"Skipping missing worktree check for {wp_id} (lane=done)."
                )
                continue

            result.passed = False
            expected_path = repo_root / WORKTREES_DIR / f"{feature_slug}-{wp_id}"
            error = f"Missing worktree for {wp_id}. Expected at {expected_path.name}. Run: spec-kitty agent workflow implement {wp_id}"
            result.wp_statuses.append(
                WPStatus(
                    wp_id=wp_id,
                    worktree_path=None,
                    branch_name=f"{feature_slug}-{wp_id}",
                    is_clean=False,
                    error=error,
                )
            )
            result.errors.append(error)

    # Check all worktrees
    for wt_path, wp_id, branch in wp_workspaces:
        status = check_worktree_status(wt_path, wp_id, branch)
        result.wp_statuses.append(status)
        if not status.is_clean:
            result.passed = False
            result.errors.append(status.error or f"{wp_id} has uncommitted changes")

    # Check target divergence
    diverged, msg = check_target_divergence(target_branch, repo_root)
    result.target_diverged = diverged
    result.target_divergence_msg = msg
    if diverged:
        result.passed = False
        result.errors.append(msg or f"{target_branch} has diverged from origin")

    return result


def x_run_preflight__mutmut_35(
    feature_slug: str,
    target_branch: str,
    repo_root: Path,
    wp_workspaces: list[tuple[Path, str, str]],
) -> PreflightResult:
    """Run all pre-flight checks before merge.

    Args:
        feature_slug: Feature identifier (e.g., "017-smarter-feature-merge")
        target_branch: Branch to merge into (e.g., "main")
        repo_root: Repository root path
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples

    Returns:
        PreflightResult with all check outcomes
    """
    result = PreflightResult(passed=True)

    # Check for missing worktrees based on tasks in kitty-specs
    expected_graph = build_dependency_graph(repo_root / KITTY_SPECS_DIR / feature_slug)
    expected_wps = set(expected_graph.keys())
    discovered_wps = {wp_id for _, wp_id, _ in wp_workspaces}
    missing_wps = sorted(expected_wps - discovered_wps)
    if missing_wps:
        for wp_id in missing_wps:
            lane = _wp_lane_from_feature(repo_root, feature_slug, wp_id)
            if lane == "done":
                result.warnings.append(
                    f"Skipping missing worktree check for {wp_id} (lane=done)."
                )
                continue

            result.passed = False
            expected_path = repo_root / WORKTREES_DIR / f"{feature_slug}-{wp_id}"
            error = f"Missing worktree for {wp_id}. Expected at {expected_path.name}. Run: spec-kitty agent workflow implement {wp_id}"
            result.wp_statuses.append(
                WPStatus(
                    wp_id=wp_id,
                    worktree_path=expected_path,
                    branch_name=None,
                    is_clean=False,
                    error=error,
                )
            )
            result.errors.append(error)

    # Check all worktrees
    for wt_path, wp_id, branch in wp_workspaces:
        status = check_worktree_status(wt_path, wp_id, branch)
        result.wp_statuses.append(status)
        if not status.is_clean:
            result.passed = False
            result.errors.append(status.error or f"{wp_id} has uncommitted changes")

    # Check target divergence
    diverged, msg = check_target_divergence(target_branch, repo_root)
    result.target_diverged = diverged
    result.target_divergence_msg = msg
    if diverged:
        result.passed = False
        result.errors.append(msg or f"{target_branch} has diverged from origin")

    return result


def x_run_preflight__mutmut_36(
    feature_slug: str,
    target_branch: str,
    repo_root: Path,
    wp_workspaces: list[tuple[Path, str, str]],
) -> PreflightResult:
    """Run all pre-flight checks before merge.

    Args:
        feature_slug: Feature identifier (e.g., "017-smarter-feature-merge")
        target_branch: Branch to merge into (e.g., "main")
        repo_root: Repository root path
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples

    Returns:
        PreflightResult with all check outcomes
    """
    result = PreflightResult(passed=True)

    # Check for missing worktrees based on tasks in kitty-specs
    expected_graph = build_dependency_graph(repo_root / KITTY_SPECS_DIR / feature_slug)
    expected_wps = set(expected_graph.keys())
    discovered_wps = {wp_id for _, wp_id, _ in wp_workspaces}
    missing_wps = sorted(expected_wps - discovered_wps)
    if missing_wps:
        for wp_id in missing_wps:
            lane = _wp_lane_from_feature(repo_root, feature_slug, wp_id)
            if lane == "done":
                result.warnings.append(
                    f"Skipping missing worktree check for {wp_id} (lane=done)."
                )
                continue

            result.passed = False
            expected_path = repo_root / WORKTREES_DIR / f"{feature_slug}-{wp_id}"
            error = f"Missing worktree for {wp_id}. Expected at {expected_path.name}. Run: spec-kitty agent workflow implement {wp_id}"
            result.wp_statuses.append(
                WPStatus(
                    wp_id=wp_id,
                    worktree_path=expected_path,
                    branch_name=f"{feature_slug}-{wp_id}",
                    is_clean=None,
                    error=error,
                )
            )
            result.errors.append(error)

    # Check all worktrees
    for wt_path, wp_id, branch in wp_workspaces:
        status = check_worktree_status(wt_path, wp_id, branch)
        result.wp_statuses.append(status)
        if not status.is_clean:
            result.passed = False
            result.errors.append(status.error or f"{wp_id} has uncommitted changes")

    # Check target divergence
    diverged, msg = check_target_divergence(target_branch, repo_root)
    result.target_diverged = diverged
    result.target_divergence_msg = msg
    if diverged:
        result.passed = False
        result.errors.append(msg or f"{target_branch} has diverged from origin")

    return result


def x_run_preflight__mutmut_37(
    feature_slug: str,
    target_branch: str,
    repo_root: Path,
    wp_workspaces: list[tuple[Path, str, str]],
) -> PreflightResult:
    """Run all pre-flight checks before merge.

    Args:
        feature_slug: Feature identifier (e.g., "017-smarter-feature-merge")
        target_branch: Branch to merge into (e.g., "main")
        repo_root: Repository root path
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples

    Returns:
        PreflightResult with all check outcomes
    """
    result = PreflightResult(passed=True)

    # Check for missing worktrees based on tasks in kitty-specs
    expected_graph = build_dependency_graph(repo_root / KITTY_SPECS_DIR / feature_slug)
    expected_wps = set(expected_graph.keys())
    discovered_wps = {wp_id for _, wp_id, _ in wp_workspaces}
    missing_wps = sorted(expected_wps - discovered_wps)
    if missing_wps:
        for wp_id in missing_wps:
            lane = _wp_lane_from_feature(repo_root, feature_slug, wp_id)
            if lane == "done":
                result.warnings.append(
                    f"Skipping missing worktree check for {wp_id} (lane=done)."
                )
                continue

            result.passed = False
            expected_path = repo_root / WORKTREES_DIR / f"{feature_slug}-{wp_id}"
            error = f"Missing worktree for {wp_id}. Expected at {expected_path.name}. Run: spec-kitty agent workflow implement {wp_id}"
            result.wp_statuses.append(
                WPStatus(
                    wp_id=wp_id,
                    worktree_path=expected_path,
                    branch_name=f"{feature_slug}-{wp_id}",
                    is_clean=False,
                    error=None,
                )
            )
            result.errors.append(error)

    # Check all worktrees
    for wt_path, wp_id, branch in wp_workspaces:
        status = check_worktree_status(wt_path, wp_id, branch)
        result.wp_statuses.append(status)
        if not status.is_clean:
            result.passed = False
            result.errors.append(status.error or f"{wp_id} has uncommitted changes")

    # Check target divergence
    diverged, msg = check_target_divergence(target_branch, repo_root)
    result.target_diverged = diverged
    result.target_divergence_msg = msg
    if diverged:
        result.passed = False
        result.errors.append(msg or f"{target_branch} has diverged from origin")

    return result


def x_run_preflight__mutmut_38(
    feature_slug: str,
    target_branch: str,
    repo_root: Path,
    wp_workspaces: list[tuple[Path, str, str]],
) -> PreflightResult:
    """Run all pre-flight checks before merge.

    Args:
        feature_slug: Feature identifier (e.g., "017-smarter-feature-merge")
        target_branch: Branch to merge into (e.g., "main")
        repo_root: Repository root path
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples

    Returns:
        PreflightResult with all check outcomes
    """
    result = PreflightResult(passed=True)

    # Check for missing worktrees based on tasks in kitty-specs
    expected_graph = build_dependency_graph(repo_root / KITTY_SPECS_DIR / feature_slug)
    expected_wps = set(expected_graph.keys())
    discovered_wps = {wp_id for _, wp_id, _ in wp_workspaces}
    missing_wps = sorted(expected_wps - discovered_wps)
    if missing_wps:
        for wp_id in missing_wps:
            lane = _wp_lane_from_feature(repo_root, feature_slug, wp_id)
            if lane == "done":
                result.warnings.append(
                    f"Skipping missing worktree check for {wp_id} (lane=done)."
                )
                continue

            result.passed = False
            expected_path = repo_root / WORKTREES_DIR / f"{feature_slug}-{wp_id}"
            error = f"Missing worktree for {wp_id}. Expected at {expected_path.name}. Run: spec-kitty agent workflow implement {wp_id}"
            result.wp_statuses.append(
                WPStatus(
                    worktree_path=expected_path,
                    branch_name=f"{feature_slug}-{wp_id}",
                    is_clean=False,
                    error=error,
                )
            )
            result.errors.append(error)

    # Check all worktrees
    for wt_path, wp_id, branch in wp_workspaces:
        status = check_worktree_status(wt_path, wp_id, branch)
        result.wp_statuses.append(status)
        if not status.is_clean:
            result.passed = False
            result.errors.append(status.error or f"{wp_id} has uncommitted changes")

    # Check target divergence
    diverged, msg = check_target_divergence(target_branch, repo_root)
    result.target_diverged = diverged
    result.target_divergence_msg = msg
    if diverged:
        result.passed = False
        result.errors.append(msg or f"{target_branch} has diverged from origin")

    return result


def x_run_preflight__mutmut_39(
    feature_slug: str,
    target_branch: str,
    repo_root: Path,
    wp_workspaces: list[tuple[Path, str, str]],
) -> PreflightResult:
    """Run all pre-flight checks before merge.

    Args:
        feature_slug: Feature identifier (e.g., "017-smarter-feature-merge")
        target_branch: Branch to merge into (e.g., "main")
        repo_root: Repository root path
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples

    Returns:
        PreflightResult with all check outcomes
    """
    result = PreflightResult(passed=True)

    # Check for missing worktrees based on tasks in kitty-specs
    expected_graph = build_dependency_graph(repo_root / KITTY_SPECS_DIR / feature_slug)
    expected_wps = set(expected_graph.keys())
    discovered_wps = {wp_id for _, wp_id, _ in wp_workspaces}
    missing_wps = sorted(expected_wps - discovered_wps)
    if missing_wps:
        for wp_id in missing_wps:
            lane = _wp_lane_from_feature(repo_root, feature_slug, wp_id)
            if lane == "done":
                result.warnings.append(
                    f"Skipping missing worktree check for {wp_id} (lane=done)."
                )
                continue

            result.passed = False
            expected_path = repo_root / WORKTREES_DIR / f"{feature_slug}-{wp_id}"
            error = f"Missing worktree for {wp_id}. Expected at {expected_path.name}. Run: spec-kitty agent workflow implement {wp_id}"
            result.wp_statuses.append(
                WPStatus(
                    wp_id=wp_id,
                    branch_name=f"{feature_slug}-{wp_id}",
                    is_clean=False,
                    error=error,
                )
            )
            result.errors.append(error)

    # Check all worktrees
    for wt_path, wp_id, branch in wp_workspaces:
        status = check_worktree_status(wt_path, wp_id, branch)
        result.wp_statuses.append(status)
        if not status.is_clean:
            result.passed = False
            result.errors.append(status.error or f"{wp_id} has uncommitted changes")

    # Check target divergence
    diverged, msg = check_target_divergence(target_branch, repo_root)
    result.target_diverged = diverged
    result.target_divergence_msg = msg
    if diverged:
        result.passed = False
        result.errors.append(msg or f"{target_branch} has diverged from origin")

    return result


def x_run_preflight__mutmut_40(
    feature_slug: str,
    target_branch: str,
    repo_root: Path,
    wp_workspaces: list[tuple[Path, str, str]],
) -> PreflightResult:
    """Run all pre-flight checks before merge.

    Args:
        feature_slug: Feature identifier (e.g., "017-smarter-feature-merge")
        target_branch: Branch to merge into (e.g., "main")
        repo_root: Repository root path
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples

    Returns:
        PreflightResult with all check outcomes
    """
    result = PreflightResult(passed=True)

    # Check for missing worktrees based on tasks in kitty-specs
    expected_graph = build_dependency_graph(repo_root / KITTY_SPECS_DIR / feature_slug)
    expected_wps = set(expected_graph.keys())
    discovered_wps = {wp_id for _, wp_id, _ in wp_workspaces}
    missing_wps = sorted(expected_wps - discovered_wps)
    if missing_wps:
        for wp_id in missing_wps:
            lane = _wp_lane_from_feature(repo_root, feature_slug, wp_id)
            if lane == "done":
                result.warnings.append(
                    f"Skipping missing worktree check for {wp_id} (lane=done)."
                )
                continue

            result.passed = False
            expected_path = repo_root / WORKTREES_DIR / f"{feature_slug}-{wp_id}"
            error = f"Missing worktree for {wp_id}. Expected at {expected_path.name}. Run: spec-kitty agent workflow implement {wp_id}"
            result.wp_statuses.append(
                WPStatus(
                    wp_id=wp_id,
                    worktree_path=expected_path,
                    is_clean=False,
                    error=error,
                )
            )
            result.errors.append(error)

    # Check all worktrees
    for wt_path, wp_id, branch in wp_workspaces:
        status = check_worktree_status(wt_path, wp_id, branch)
        result.wp_statuses.append(status)
        if not status.is_clean:
            result.passed = False
            result.errors.append(status.error or f"{wp_id} has uncommitted changes")

    # Check target divergence
    diverged, msg = check_target_divergence(target_branch, repo_root)
    result.target_diverged = diverged
    result.target_divergence_msg = msg
    if diverged:
        result.passed = False
        result.errors.append(msg or f"{target_branch} has diverged from origin")

    return result


def x_run_preflight__mutmut_41(
    feature_slug: str,
    target_branch: str,
    repo_root: Path,
    wp_workspaces: list[tuple[Path, str, str]],
) -> PreflightResult:
    """Run all pre-flight checks before merge.

    Args:
        feature_slug: Feature identifier (e.g., "017-smarter-feature-merge")
        target_branch: Branch to merge into (e.g., "main")
        repo_root: Repository root path
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples

    Returns:
        PreflightResult with all check outcomes
    """
    result = PreflightResult(passed=True)

    # Check for missing worktrees based on tasks in kitty-specs
    expected_graph = build_dependency_graph(repo_root / KITTY_SPECS_DIR / feature_slug)
    expected_wps = set(expected_graph.keys())
    discovered_wps = {wp_id for _, wp_id, _ in wp_workspaces}
    missing_wps = sorted(expected_wps - discovered_wps)
    if missing_wps:
        for wp_id in missing_wps:
            lane = _wp_lane_from_feature(repo_root, feature_slug, wp_id)
            if lane == "done":
                result.warnings.append(
                    f"Skipping missing worktree check for {wp_id} (lane=done)."
                )
                continue

            result.passed = False
            expected_path = repo_root / WORKTREES_DIR / f"{feature_slug}-{wp_id}"
            error = f"Missing worktree for {wp_id}. Expected at {expected_path.name}. Run: spec-kitty agent workflow implement {wp_id}"
            result.wp_statuses.append(
                WPStatus(
                    wp_id=wp_id,
                    worktree_path=expected_path,
                    branch_name=f"{feature_slug}-{wp_id}",
                    error=error,
                )
            )
            result.errors.append(error)

    # Check all worktrees
    for wt_path, wp_id, branch in wp_workspaces:
        status = check_worktree_status(wt_path, wp_id, branch)
        result.wp_statuses.append(status)
        if not status.is_clean:
            result.passed = False
            result.errors.append(status.error or f"{wp_id} has uncommitted changes")

    # Check target divergence
    diverged, msg = check_target_divergence(target_branch, repo_root)
    result.target_diverged = diverged
    result.target_divergence_msg = msg
    if diverged:
        result.passed = False
        result.errors.append(msg or f"{target_branch} has diverged from origin")

    return result


def x_run_preflight__mutmut_42(
    feature_slug: str,
    target_branch: str,
    repo_root: Path,
    wp_workspaces: list[tuple[Path, str, str]],
) -> PreflightResult:
    """Run all pre-flight checks before merge.

    Args:
        feature_slug: Feature identifier (e.g., "017-smarter-feature-merge")
        target_branch: Branch to merge into (e.g., "main")
        repo_root: Repository root path
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples

    Returns:
        PreflightResult with all check outcomes
    """
    result = PreflightResult(passed=True)

    # Check for missing worktrees based on tasks in kitty-specs
    expected_graph = build_dependency_graph(repo_root / KITTY_SPECS_DIR / feature_slug)
    expected_wps = set(expected_graph.keys())
    discovered_wps = {wp_id for _, wp_id, _ in wp_workspaces}
    missing_wps = sorted(expected_wps - discovered_wps)
    if missing_wps:
        for wp_id in missing_wps:
            lane = _wp_lane_from_feature(repo_root, feature_slug, wp_id)
            if lane == "done":
                result.warnings.append(
                    f"Skipping missing worktree check for {wp_id} (lane=done)."
                )
                continue

            result.passed = False
            expected_path = repo_root / WORKTREES_DIR / f"{feature_slug}-{wp_id}"
            error = f"Missing worktree for {wp_id}. Expected at {expected_path.name}. Run: spec-kitty agent workflow implement {wp_id}"
            result.wp_statuses.append(
                WPStatus(
                    wp_id=wp_id,
                    worktree_path=expected_path,
                    branch_name=f"{feature_slug}-{wp_id}",
                    is_clean=False,
                    )
            )
            result.errors.append(error)

    # Check all worktrees
    for wt_path, wp_id, branch in wp_workspaces:
        status = check_worktree_status(wt_path, wp_id, branch)
        result.wp_statuses.append(status)
        if not status.is_clean:
            result.passed = False
            result.errors.append(status.error or f"{wp_id} has uncommitted changes")

    # Check target divergence
    diverged, msg = check_target_divergence(target_branch, repo_root)
    result.target_diverged = diverged
    result.target_divergence_msg = msg
    if diverged:
        result.passed = False
        result.errors.append(msg or f"{target_branch} has diverged from origin")

    return result


def x_run_preflight__mutmut_43(
    feature_slug: str,
    target_branch: str,
    repo_root: Path,
    wp_workspaces: list[tuple[Path, str, str]],
) -> PreflightResult:
    """Run all pre-flight checks before merge.

    Args:
        feature_slug: Feature identifier (e.g., "017-smarter-feature-merge")
        target_branch: Branch to merge into (e.g., "main")
        repo_root: Repository root path
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples

    Returns:
        PreflightResult with all check outcomes
    """
    result = PreflightResult(passed=True)

    # Check for missing worktrees based on tasks in kitty-specs
    expected_graph = build_dependency_graph(repo_root / KITTY_SPECS_DIR / feature_slug)
    expected_wps = set(expected_graph.keys())
    discovered_wps = {wp_id for _, wp_id, _ in wp_workspaces}
    missing_wps = sorted(expected_wps - discovered_wps)
    if missing_wps:
        for wp_id in missing_wps:
            lane = _wp_lane_from_feature(repo_root, feature_slug, wp_id)
            if lane == "done":
                result.warnings.append(
                    f"Skipping missing worktree check for {wp_id} (lane=done)."
                )
                continue

            result.passed = False
            expected_path = repo_root / WORKTREES_DIR / f"{feature_slug}-{wp_id}"
            error = f"Missing worktree for {wp_id}. Expected at {expected_path.name}. Run: spec-kitty agent workflow implement {wp_id}"
            result.wp_statuses.append(
                WPStatus(
                    wp_id=wp_id,
                    worktree_path=expected_path,
                    branch_name=f"{feature_slug}-{wp_id}",
                    is_clean=True,
                    error=error,
                )
            )
            result.errors.append(error)

    # Check all worktrees
    for wt_path, wp_id, branch in wp_workspaces:
        status = check_worktree_status(wt_path, wp_id, branch)
        result.wp_statuses.append(status)
        if not status.is_clean:
            result.passed = False
            result.errors.append(status.error or f"{wp_id} has uncommitted changes")

    # Check target divergence
    diverged, msg = check_target_divergence(target_branch, repo_root)
    result.target_diverged = diverged
    result.target_divergence_msg = msg
    if diverged:
        result.passed = False
        result.errors.append(msg or f"{target_branch} has diverged from origin")

    return result


def x_run_preflight__mutmut_44(
    feature_slug: str,
    target_branch: str,
    repo_root: Path,
    wp_workspaces: list[tuple[Path, str, str]],
) -> PreflightResult:
    """Run all pre-flight checks before merge.

    Args:
        feature_slug: Feature identifier (e.g., "017-smarter-feature-merge")
        target_branch: Branch to merge into (e.g., "main")
        repo_root: Repository root path
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples

    Returns:
        PreflightResult with all check outcomes
    """
    result = PreflightResult(passed=True)

    # Check for missing worktrees based on tasks in kitty-specs
    expected_graph = build_dependency_graph(repo_root / KITTY_SPECS_DIR / feature_slug)
    expected_wps = set(expected_graph.keys())
    discovered_wps = {wp_id for _, wp_id, _ in wp_workspaces}
    missing_wps = sorted(expected_wps - discovered_wps)
    if missing_wps:
        for wp_id in missing_wps:
            lane = _wp_lane_from_feature(repo_root, feature_slug, wp_id)
            if lane == "done":
                result.warnings.append(
                    f"Skipping missing worktree check for {wp_id} (lane=done)."
                )
                continue

            result.passed = False
            expected_path = repo_root / WORKTREES_DIR / f"{feature_slug}-{wp_id}"
            error = f"Missing worktree for {wp_id}. Expected at {expected_path.name}. Run: spec-kitty agent workflow implement {wp_id}"
            result.wp_statuses.append(
                WPStatus(
                    wp_id=wp_id,
                    worktree_path=expected_path,
                    branch_name=f"{feature_slug}-{wp_id}",
                    is_clean=False,
                    error=error,
                )
            )
            result.errors.append(None)

    # Check all worktrees
    for wt_path, wp_id, branch in wp_workspaces:
        status = check_worktree_status(wt_path, wp_id, branch)
        result.wp_statuses.append(status)
        if not status.is_clean:
            result.passed = False
            result.errors.append(status.error or f"{wp_id} has uncommitted changes")

    # Check target divergence
    diverged, msg = check_target_divergence(target_branch, repo_root)
    result.target_diverged = diverged
    result.target_divergence_msg = msg
    if diverged:
        result.passed = False
        result.errors.append(msg or f"{target_branch} has diverged from origin")

    return result


def x_run_preflight__mutmut_45(
    feature_slug: str,
    target_branch: str,
    repo_root: Path,
    wp_workspaces: list[tuple[Path, str, str]],
) -> PreflightResult:
    """Run all pre-flight checks before merge.

    Args:
        feature_slug: Feature identifier (e.g., "017-smarter-feature-merge")
        target_branch: Branch to merge into (e.g., "main")
        repo_root: Repository root path
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples

    Returns:
        PreflightResult with all check outcomes
    """
    result = PreflightResult(passed=True)

    # Check for missing worktrees based on tasks in kitty-specs
    expected_graph = build_dependency_graph(repo_root / KITTY_SPECS_DIR / feature_slug)
    expected_wps = set(expected_graph.keys())
    discovered_wps = {wp_id for _, wp_id, _ in wp_workspaces}
    missing_wps = sorted(expected_wps - discovered_wps)
    if missing_wps:
        for wp_id in missing_wps:
            lane = _wp_lane_from_feature(repo_root, feature_slug, wp_id)
            if lane == "done":
                result.warnings.append(
                    f"Skipping missing worktree check for {wp_id} (lane=done)."
                )
                continue

            result.passed = False
            expected_path = repo_root / WORKTREES_DIR / f"{feature_slug}-{wp_id}"
            error = f"Missing worktree for {wp_id}. Expected at {expected_path.name}. Run: spec-kitty agent workflow implement {wp_id}"
            result.wp_statuses.append(
                WPStatus(
                    wp_id=wp_id,
                    worktree_path=expected_path,
                    branch_name=f"{feature_slug}-{wp_id}",
                    is_clean=False,
                    error=error,
                )
            )
            result.errors.append(error)

    # Check all worktrees
    for wt_path, wp_id, branch in wp_workspaces:
        status = None
        result.wp_statuses.append(status)
        if not status.is_clean:
            result.passed = False
            result.errors.append(status.error or f"{wp_id} has uncommitted changes")

    # Check target divergence
    diverged, msg = check_target_divergence(target_branch, repo_root)
    result.target_diverged = diverged
    result.target_divergence_msg = msg
    if diverged:
        result.passed = False
        result.errors.append(msg or f"{target_branch} has diverged from origin")

    return result


def x_run_preflight__mutmut_46(
    feature_slug: str,
    target_branch: str,
    repo_root: Path,
    wp_workspaces: list[tuple[Path, str, str]],
) -> PreflightResult:
    """Run all pre-flight checks before merge.

    Args:
        feature_slug: Feature identifier (e.g., "017-smarter-feature-merge")
        target_branch: Branch to merge into (e.g., "main")
        repo_root: Repository root path
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples

    Returns:
        PreflightResult with all check outcomes
    """
    result = PreflightResult(passed=True)

    # Check for missing worktrees based on tasks in kitty-specs
    expected_graph = build_dependency_graph(repo_root / KITTY_SPECS_DIR / feature_slug)
    expected_wps = set(expected_graph.keys())
    discovered_wps = {wp_id for _, wp_id, _ in wp_workspaces}
    missing_wps = sorted(expected_wps - discovered_wps)
    if missing_wps:
        for wp_id in missing_wps:
            lane = _wp_lane_from_feature(repo_root, feature_slug, wp_id)
            if lane == "done":
                result.warnings.append(
                    f"Skipping missing worktree check for {wp_id} (lane=done)."
                )
                continue

            result.passed = False
            expected_path = repo_root / WORKTREES_DIR / f"{feature_slug}-{wp_id}"
            error = f"Missing worktree for {wp_id}. Expected at {expected_path.name}. Run: spec-kitty agent workflow implement {wp_id}"
            result.wp_statuses.append(
                WPStatus(
                    wp_id=wp_id,
                    worktree_path=expected_path,
                    branch_name=f"{feature_slug}-{wp_id}",
                    is_clean=False,
                    error=error,
                )
            )
            result.errors.append(error)

    # Check all worktrees
    for wt_path, wp_id, branch in wp_workspaces:
        status = check_worktree_status(None, wp_id, branch)
        result.wp_statuses.append(status)
        if not status.is_clean:
            result.passed = False
            result.errors.append(status.error or f"{wp_id} has uncommitted changes")

    # Check target divergence
    diverged, msg = check_target_divergence(target_branch, repo_root)
    result.target_diverged = diverged
    result.target_divergence_msg = msg
    if diverged:
        result.passed = False
        result.errors.append(msg or f"{target_branch} has diverged from origin")

    return result


def x_run_preflight__mutmut_47(
    feature_slug: str,
    target_branch: str,
    repo_root: Path,
    wp_workspaces: list[tuple[Path, str, str]],
) -> PreflightResult:
    """Run all pre-flight checks before merge.

    Args:
        feature_slug: Feature identifier (e.g., "017-smarter-feature-merge")
        target_branch: Branch to merge into (e.g., "main")
        repo_root: Repository root path
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples

    Returns:
        PreflightResult with all check outcomes
    """
    result = PreflightResult(passed=True)

    # Check for missing worktrees based on tasks in kitty-specs
    expected_graph = build_dependency_graph(repo_root / KITTY_SPECS_DIR / feature_slug)
    expected_wps = set(expected_graph.keys())
    discovered_wps = {wp_id for _, wp_id, _ in wp_workspaces}
    missing_wps = sorted(expected_wps - discovered_wps)
    if missing_wps:
        for wp_id in missing_wps:
            lane = _wp_lane_from_feature(repo_root, feature_slug, wp_id)
            if lane == "done":
                result.warnings.append(
                    f"Skipping missing worktree check for {wp_id} (lane=done)."
                )
                continue

            result.passed = False
            expected_path = repo_root / WORKTREES_DIR / f"{feature_slug}-{wp_id}"
            error = f"Missing worktree for {wp_id}. Expected at {expected_path.name}. Run: spec-kitty agent workflow implement {wp_id}"
            result.wp_statuses.append(
                WPStatus(
                    wp_id=wp_id,
                    worktree_path=expected_path,
                    branch_name=f"{feature_slug}-{wp_id}",
                    is_clean=False,
                    error=error,
                )
            )
            result.errors.append(error)

    # Check all worktrees
    for wt_path, wp_id, branch in wp_workspaces:
        status = check_worktree_status(wt_path, None, branch)
        result.wp_statuses.append(status)
        if not status.is_clean:
            result.passed = False
            result.errors.append(status.error or f"{wp_id} has uncommitted changes")

    # Check target divergence
    diverged, msg = check_target_divergence(target_branch, repo_root)
    result.target_diverged = diverged
    result.target_divergence_msg = msg
    if diverged:
        result.passed = False
        result.errors.append(msg or f"{target_branch} has diverged from origin")

    return result


def x_run_preflight__mutmut_48(
    feature_slug: str,
    target_branch: str,
    repo_root: Path,
    wp_workspaces: list[tuple[Path, str, str]],
) -> PreflightResult:
    """Run all pre-flight checks before merge.

    Args:
        feature_slug: Feature identifier (e.g., "017-smarter-feature-merge")
        target_branch: Branch to merge into (e.g., "main")
        repo_root: Repository root path
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples

    Returns:
        PreflightResult with all check outcomes
    """
    result = PreflightResult(passed=True)

    # Check for missing worktrees based on tasks in kitty-specs
    expected_graph = build_dependency_graph(repo_root / KITTY_SPECS_DIR / feature_slug)
    expected_wps = set(expected_graph.keys())
    discovered_wps = {wp_id for _, wp_id, _ in wp_workspaces}
    missing_wps = sorted(expected_wps - discovered_wps)
    if missing_wps:
        for wp_id in missing_wps:
            lane = _wp_lane_from_feature(repo_root, feature_slug, wp_id)
            if lane == "done":
                result.warnings.append(
                    f"Skipping missing worktree check for {wp_id} (lane=done)."
                )
                continue

            result.passed = False
            expected_path = repo_root / WORKTREES_DIR / f"{feature_slug}-{wp_id}"
            error = f"Missing worktree for {wp_id}. Expected at {expected_path.name}. Run: spec-kitty agent workflow implement {wp_id}"
            result.wp_statuses.append(
                WPStatus(
                    wp_id=wp_id,
                    worktree_path=expected_path,
                    branch_name=f"{feature_slug}-{wp_id}",
                    is_clean=False,
                    error=error,
                )
            )
            result.errors.append(error)

    # Check all worktrees
    for wt_path, wp_id, branch in wp_workspaces:
        status = check_worktree_status(wt_path, wp_id, None)
        result.wp_statuses.append(status)
        if not status.is_clean:
            result.passed = False
            result.errors.append(status.error or f"{wp_id} has uncommitted changes")

    # Check target divergence
    diverged, msg = check_target_divergence(target_branch, repo_root)
    result.target_diverged = diverged
    result.target_divergence_msg = msg
    if diverged:
        result.passed = False
        result.errors.append(msg or f"{target_branch} has diverged from origin")

    return result


def x_run_preflight__mutmut_49(
    feature_slug: str,
    target_branch: str,
    repo_root: Path,
    wp_workspaces: list[tuple[Path, str, str]],
) -> PreflightResult:
    """Run all pre-flight checks before merge.

    Args:
        feature_slug: Feature identifier (e.g., "017-smarter-feature-merge")
        target_branch: Branch to merge into (e.g., "main")
        repo_root: Repository root path
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples

    Returns:
        PreflightResult with all check outcomes
    """
    result = PreflightResult(passed=True)

    # Check for missing worktrees based on tasks in kitty-specs
    expected_graph = build_dependency_graph(repo_root / KITTY_SPECS_DIR / feature_slug)
    expected_wps = set(expected_graph.keys())
    discovered_wps = {wp_id for _, wp_id, _ in wp_workspaces}
    missing_wps = sorted(expected_wps - discovered_wps)
    if missing_wps:
        for wp_id in missing_wps:
            lane = _wp_lane_from_feature(repo_root, feature_slug, wp_id)
            if lane == "done":
                result.warnings.append(
                    f"Skipping missing worktree check for {wp_id} (lane=done)."
                )
                continue

            result.passed = False
            expected_path = repo_root / WORKTREES_DIR / f"{feature_slug}-{wp_id}"
            error = f"Missing worktree for {wp_id}. Expected at {expected_path.name}. Run: spec-kitty agent workflow implement {wp_id}"
            result.wp_statuses.append(
                WPStatus(
                    wp_id=wp_id,
                    worktree_path=expected_path,
                    branch_name=f"{feature_slug}-{wp_id}",
                    is_clean=False,
                    error=error,
                )
            )
            result.errors.append(error)

    # Check all worktrees
    for wt_path, wp_id, branch in wp_workspaces:
        status = check_worktree_status(wp_id, branch)
        result.wp_statuses.append(status)
        if not status.is_clean:
            result.passed = False
            result.errors.append(status.error or f"{wp_id} has uncommitted changes")

    # Check target divergence
    diverged, msg = check_target_divergence(target_branch, repo_root)
    result.target_diverged = diverged
    result.target_divergence_msg = msg
    if diverged:
        result.passed = False
        result.errors.append(msg or f"{target_branch} has diverged from origin")

    return result


def x_run_preflight__mutmut_50(
    feature_slug: str,
    target_branch: str,
    repo_root: Path,
    wp_workspaces: list[tuple[Path, str, str]],
) -> PreflightResult:
    """Run all pre-flight checks before merge.

    Args:
        feature_slug: Feature identifier (e.g., "017-smarter-feature-merge")
        target_branch: Branch to merge into (e.g., "main")
        repo_root: Repository root path
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples

    Returns:
        PreflightResult with all check outcomes
    """
    result = PreflightResult(passed=True)

    # Check for missing worktrees based on tasks in kitty-specs
    expected_graph = build_dependency_graph(repo_root / KITTY_SPECS_DIR / feature_slug)
    expected_wps = set(expected_graph.keys())
    discovered_wps = {wp_id for _, wp_id, _ in wp_workspaces}
    missing_wps = sorted(expected_wps - discovered_wps)
    if missing_wps:
        for wp_id in missing_wps:
            lane = _wp_lane_from_feature(repo_root, feature_slug, wp_id)
            if lane == "done":
                result.warnings.append(
                    f"Skipping missing worktree check for {wp_id} (lane=done)."
                )
                continue

            result.passed = False
            expected_path = repo_root / WORKTREES_DIR / f"{feature_slug}-{wp_id}"
            error = f"Missing worktree for {wp_id}. Expected at {expected_path.name}. Run: spec-kitty agent workflow implement {wp_id}"
            result.wp_statuses.append(
                WPStatus(
                    wp_id=wp_id,
                    worktree_path=expected_path,
                    branch_name=f"{feature_slug}-{wp_id}",
                    is_clean=False,
                    error=error,
                )
            )
            result.errors.append(error)

    # Check all worktrees
    for wt_path, wp_id, branch in wp_workspaces:
        status = check_worktree_status(wt_path, branch)
        result.wp_statuses.append(status)
        if not status.is_clean:
            result.passed = False
            result.errors.append(status.error or f"{wp_id} has uncommitted changes")

    # Check target divergence
    diverged, msg = check_target_divergence(target_branch, repo_root)
    result.target_diverged = diverged
    result.target_divergence_msg = msg
    if diverged:
        result.passed = False
        result.errors.append(msg or f"{target_branch} has diverged from origin")

    return result


def x_run_preflight__mutmut_51(
    feature_slug: str,
    target_branch: str,
    repo_root: Path,
    wp_workspaces: list[tuple[Path, str, str]],
) -> PreflightResult:
    """Run all pre-flight checks before merge.

    Args:
        feature_slug: Feature identifier (e.g., "017-smarter-feature-merge")
        target_branch: Branch to merge into (e.g., "main")
        repo_root: Repository root path
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples

    Returns:
        PreflightResult with all check outcomes
    """
    result = PreflightResult(passed=True)

    # Check for missing worktrees based on tasks in kitty-specs
    expected_graph = build_dependency_graph(repo_root / KITTY_SPECS_DIR / feature_slug)
    expected_wps = set(expected_graph.keys())
    discovered_wps = {wp_id for _, wp_id, _ in wp_workspaces}
    missing_wps = sorted(expected_wps - discovered_wps)
    if missing_wps:
        for wp_id in missing_wps:
            lane = _wp_lane_from_feature(repo_root, feature_slug, wp_id)
            if lane == "done":
                result.warnings.append(
                    f"Skipping missing worktree check for {wp_id} (lane=done)."
                )
                continue

            result.passed = False
            expected_path = repo_root / WORKTREES_DIR / f"{feature_slug}-{wp_id}"
            error = f"Missing worktree for {wp_id}. Expected at {expected_path.name}. Run: spec-kitty agent workflow implement {wp_id}"
            result.wp_statuses.append(
                WPStatus(
                    wp_id=wp_id,
                    worktree_path=expected_path,
                    branch_name=f"{feature_slug}-{wp_id}",
                    is_clean=False,
                    error=error,
                )
            )
            result.errors.append(error)

    # Check all worktrees
    for wt_path, wp_id, branch in wp_workspaces:
        status = check_worktree_status(wt_path, wp_id, )
        result.wp_statuses.append(status)
        if not status.is_clean:
            result.passed = False
            result.errors.append(status.error or f"{wp_id} has uncommitted changes")

    # Check target divergence
    diverged, msg = check_target_divergence(target_branch, repo_root)
    result.target_diverged = diverged
    result.target_divergence_msg = msg
    if diverged:
        result.passed = False
        result.errors.append(msg or f"{target_branch} has diverged from origin")

    return result


def x_run_preflight__mutmut_52(
    feature_slug: str,
    target_branch: str,
    repo_root: Path,
    wp_workspaces: list[tuple[Path, str, str]],
) -> PreflightResult:
    """Run all pre-flight checks before merge.

    Args:
        feature_slug: Feature identifier (e.g., "017-smarter-feature-merge")
        target_branch: Branch to merge into (e.g., "main")
        repo_root: Repository root path
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples

    Returns:
        PreflightResult with all check outcomes
    """
    result = PreflightResult(passed=True)

    # Check for missing worktrees based on tasks in kitty-specs
    expected_graph = build_dependency_graph(repo_root / KITTY_SPECS_DIR / feature_slug)
    expected_wps = set(expected_graph.keys())
    discovered_wps = {wp_id for _, wp_id, _ in wp_workspaces}
    missing_wps = sorted(expected_wps - discovered_wps)
    if missing_wps:
        for wp_id in missing_wps:
            lane = _wp_lane_from_feature(repo_root, feature_slug, wp_id)
            if lane == "done":
                result.warnings.append(
                    f"Skipping missing worktree check for {wp_id} (lane=done)."
                )
                continue

            result.passed = False
            expected_path = repo_root / WORKTREES_DIR / f"{feature_slug}-{wp_id}"
            error = f"Missing worktree for {wp_id}. Expected at {expected_path.name}. Run: spec-kitty agent workflow implement {wp_id}"
            result.wp_statuses.append(
                WPStatus(
                    wp_id=wp_id,
                    worktree_path=expected_path,
                    branch_name=f"{feature_slug}-{wp_id}",
                    is_clean=False,
                    error=error,
                )
            )
            result.errors.append(error)

    # Check all worktrees
    for wt_path, wp_id, branch in wp_workspaces:
        status = check_worktree_status(wt_path, wp_id, branch)
        result.wp_statuses.append(None)
        if not status.is_clean:
            result.passed = False
            result.errors.append(status.error or f"{wp_id} has uncommitted changes")

    # Check target divergence
    diverged, msg = check_target_divergence(target_branch, repo_root)
    result.target_diverged = diverged
    result.target_divergence_msg = msg
    if diverged:
        result.passed = False
        result.errors.append(msg or f"{target_branch} has diverged from origin")

    return result


def x_run_preflight__mutmut_53(
    feature_slug: str,
    target_branch: str,
    repo_root: Path,
    wp_workspaces: list[tuple[Path, str, str]],
) -> PreflightResult:
    """Run all pre-flight checks before merge.

    Args:
        feature_slug: Feature identifier (e.g., "017-smarter-feature-merge")
        target_branch: Branch to merge into (e.g., "main")
        repo_root: Repository root path
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples

    Returns:
        PreflightResult with all check outcomes
    """
    result = PreflightResult(passed=True)

    # Check for missing worktrees based on tasks in kitty-specs
    expected_graph = build_dependency_graph(repo_root / KITTY_SPECS_DIR / feature_slug)
    expected_wps = set(expected_graph.keys())
    discovered_wps = {wp_id for _, wp_id, _ in wp_workspaces}
    missing_wps = sorted(expected_wps - discovered_wps)
    if missing_wps:
        for wp_id in missing_wps:
            lane = _wp_lane_from_feature(repo_root, feature_slug, wp_id)
            if lane == "done":
                result.warnings.append(
                    f"Skipping missing worktree check for {wp_id} (lane=done)."
                )
                continue

            result.passed = False
            expected_path = repo_root / WORKTREES_DIR / f"{feature_slug}-{wp_id}"
            error = f"Missing worktree for {wp_id}. Expected at {expected_path.name}. Run: spec-kitty agent workflow implement {wp_id}"
            result.wp_statuses.append(
                WPStatus(
                    wp_id=wp_id,
                    worktree_path=expected_path,
                    branch_name=f"{feature_slug}-{wp_id}",
                    is_clean=False,
                    error=error,
                )
            )
            result.errors.append(error)

    # Check all worktrees
    for wt_path, wp_id, branch in wp_workspaces:
        status = check_worktree_status(wt_path, wp_id, branch)
        result.wp_statuses.append(status)
        if status.is_clean:
            result.passed = False
            result.errors.append(status.error or f"{wp_id} has uncommitted changes")

    # Check target divergence
    diverged, msg = check_target_divergence(target_branch, repo_root)
    result.target_diverged = diverged
    result.target_divergence_msg = msg
    if diverged:
        result.passed = False
        result.errors.append(msg or f"{target_branch} has diverged from origin")

    return result


def x_run_preflight__mutmut_54(
    feature_slug: str,
    target_branch: str,
    repo_root: Path,
    wp_workspaces: list[tuple[Path, str, str]],
) -> PreflightResult:
    """Run all pre-flight checks before merge.

    Args:
        feature_slug: Feature identifier (e.g., "017-smarter-feature-merge")
        target_branch: Branch to merge into (e.g., "main")
        repo_root: Repository root path
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples

    Returns:
        PreflightResult with all check outcomes
    """
    result = PreflightResult(passed=True)

    # Check for missing worktrees based on tasks in kitty-specs
    expected_graph = build_dependency_graph(repo_root / KITTY_SPECS_DIR / feature_slug)
    expected_wps = set(expected_graph.keys())
    discovered_wps = {wp_id for _, wp_id, _ in wp_workspaces}
    missing_wps = sorted(expected_wps - discovered_wps)
    if missing_wps:
        for wp_id in missing_wps:
            lane = _wp_lane_from_feature(repo_root, feature_slug, wp_id)
            if lane == "done":
                result.warnings.append(
                    f"Skipping missing worktree check for {wp_id} (lane=done)."
                )
                continue

            result.passed = False
            expected_path = repo_root / WORKTREES_DIR / f"{feature_slug}-{wp_id}"
            error = f"Missing worktree for {wp_id}. Expected at {expected_path.name}. Run: spec-kitty agent workflow implement {wp_id}"
            result.wp_statuses.append(
                WPStatus(
                    wp_id=wp_id,
                    worktree_path=expected_path,
                    branch_name=f"{feature_slug}-{wp_id}",
                    is_clean=False,
                    error=error,
                )
            )
            result.errors.append(error)

    # Check all worktrees
    for wt_path, wp_id, branch in wp_workspaces:
        status = check_worktree_status(wt_path, wp_id, branch)
        result.wp_statuses.append(status)
        if not status.is_clean:
            result.passed = None
            result.errors.append(status.error or f"{wp_id} has uncommitted changes")

    # Check target divergence
    diverged, msg = check_target_divergence(target_branch, repo_root)
    result.target_diverged = diverged
    result.target_divergence_msg = msg
    if diverged:
        result.passed = False
        result.errors.append(msg or f"{target_branch} has diverged from origin")

    return result


def x_run_preflight__mutmut_55(
    feature_slug: str,
    target_branch: str,
    repo_root: Path,
    wp_workspaces: list[tuple[Path, str, str]],
) -> PreflightResult:
    """Run all pre-flight checks before merge.

    Args:
        feature_slug: Feature identifier (e.g., "017-smarter-feature-merge")
        target_branch: Branch to merge into (e.g., "main")
        repo_root: Repository root path
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples

    Returns:
        PreflightResult with all check outcomes
    """
    result = PreflightResult(passed=True)

    # Check for missing worktrees based on tasks in kitty-specs
    expected_graph = build_dependency_graph(repo_root / KITTY_SPECS_DIR / feature_slug)
    expected_wps = set(expected_graph.keys())
    discovered_wps = {wp_id for _, wp_id, _ in wp_workspaces}
    missing_wps = sorted(expected_wps - discovered_wps)
    if missing_wps:
        for wp_id in missing_wps:
            lane = _wp_lane_from_feature(repo_root, feature_slug, wp_id)
            if lane == "done":
                result.warnings.append(
                    f"Skipping missing worktree check for {wp_id} (lane=done)."
                )
                continue

            result.passed = False
            expected_path = repo_root / WORKTREES_DIR / f"{feature_slug}-{wp_id}"
            error = f"Missing worktree for {wp_id}. Expected at {expected_path.name}. Run: spec-kitty agent workflow implement {wp_id}"
            result.wp_statuses.append(
                WPStatus(
                    wp_id=wp_id,
                    worktree_path=expected_path,
                    branch_name=f"{feature_slug}-{wp_id}",
                    is_clean=False,
                    error=error,
                )
            )
            result.errors.append(error)

    # Check all worktrees
    for wt_path, wp_id, branch in wp_workspaces:
        status = check_worktree_status(wt_path, wp_id, branch)
        result.wp_statuses.append(status)
        if not status.is_clean:
            result.passed = True
            result.errors.append(status.error or f"{wp_id} has uncommitted changes")

    # Check target divergence
    diverged, msg = check_target_divergence(target_branch, repo_root)
    result.target_diverged = diverged
    result.target_divergence_msg = msg
    if diverged:
        result.passed = False
        result.errors.append(msg or f"{target_branch} has diverged from origin")

    return result


def x_run_preflight__mutmut_56(
    feature_slug: str,
    target_branch: str,
    repo_root: Path,
    wp_workspaces: list[tuple[Path, str, str]],
) -> PreflightResult:
    """Run all pre-flight checks before merge.

    Args:
        feature_slug: Feature identifier (e.g., "017-smarter-feature-merge")
        target_branch: Branch to merge into (e.g., "main")
        repo_root: Repository root path
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples

    Returns:
        PreflightResult with all check outcomes
    """
    result = PreflightResult(passed=True)

    # Check for missing worktrees based on tasks in kitty-specs
    expected_graph = build_dependency_graph(repo_root / KITTY_SPECS_DIR / feature_slug)
    expected_wps = set(expected_graph.keys())
    discovered_wps = {wp_id for _, wp_id, _ in wp_workspaces}
    missing_wps = sorted(expected_wps - discovered_wps)
    if missing_wps:
        for wp_id in missing_wps:
            lane = _wp_lane_from_feature(repo_root, feature_slug, wp_id)
            if lane == "done":
                result.warnings.append(
                    f"Skipping missing worktree check for {wp_id} (lane=done)."
                )
                continue

            result.passed = False
            expected_path = repo_root / WORKTREES_DIR / f"{feature_slug}-{wp_id}"
            error = f"Missing worktree for {wp_id}. Expected at {expected_path.name}. Run: spec-kitty agent workflow implement {wp_id}"
            result.wp_statuses.append(
                WPStatus(
                    wp_id=wp_id,
                    worktree_path=expected_path,
                    branch_name=f"{feature_slug}-{wp_id}",
                    is_clean=False,
                    error=error,
                )
            )
            result.errors.append(error)

    # Check all worktrees
    for wt_path, wp_id, branch in wp_workspaces:
        status = check_worktree_status(wt_path, wp_id, branch)
        result.wp_statuses.append(status)
        if not status.is_clean:
            result.passed = False
            result.errors.append(None)

    # Check target divergence
    diverged, msg = check_target_divergence(target_branch, repo_root)
    result.target_diverged = diverged
    result.target_divergence_msg = msg
    if diverged:
        result.passed = False
        result.errors.append(msg or f"{target_branch} has diverged from origin")

    return result


def x_run_preflight__mutmut_57(
    feature_slug: str,
    target_branch: str,
    repo_root: Path,
    wp_workspaces: list[tuple[Path, str, str]],
) -> PreflightResult:
    """Run all pre-flight checks before merge.

    Args:
        feature_slug: Feature identifier (e.g., "017-smarter-feature-merge")
        target_branch: Branch to merge into (e.g., "main")
        repo_root: Repository root path
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples

    Returns:
        PreflightResult with all check outcomes
    """
    result = PreflightResult(passed=True)

    # Check for missing worktrees based on tasks in kitty-specs
    expected_graph = build_dependency_graph(repo_root / KITTY_SPECS_DIR / feature_slug)
    expected_wps = set(expected_graph.keys())
    discovered_wps = {wp_id for _, wp_id, _ in wp_workspaces}
    missing_wps = sorted(expected_wps - discovered_wps)
    if missing_wps:
        for wp_id in missing_wps:
            lane = _wp_lane_from_feature(repo_root, feature_slug, wp_id)
            if lane == "done":
                result.warnings.append(
                    f"Skipping missing worktree check for {wp_id} (lane=done)."
                )
                continue

            result.passed = False
            expected_path = repo_root / WORKTREES_DIR / f"{feature_slug}-{wp_id}"
            error = f"Missing worktree for {wp_id}. Expected at {expected_path.name}. Run: spec-kitty agent workflow implement {wp_id}"
            result.wp_statuses.append(
                WPStatus(
                    wp_id=wp_id,
                    worktree_path=expected_path,
                    branch_name=f"{feature_slug}-{wp_id}",
                    is_clean=False,
                    error=error,
                )
            )
            result.errors.append(error)

    # Check all worktrees
    for wt_path, wp_id, branch in wp_workspaces:
        status = check_worktree_status(wt_path, wp_id, branch)
        result.wp_statuses.append(status)
        if not status.is_clean:
            result.passed = False
            result.errors.append(status.error and f"{wp_id} has uncommitted changes")

    # Check target divergence
    diverged, msg = check_target_divergence(target_branch, repo_root)
    result.target_diverged = diverged
    result.target_divergence_msg = msg
    if diverged:
        result.passed = False
        result.errors.append(msg or f"{target_branch} has diverged from origin")

    return result


def x_run_preflight__mutmut_58(
    feature_slug: str,
    target_branch: str,
    repo_root: Path,
    wp_workspaces: list[tuple[Path, str, str]],
) -> PreflightResult:
    """Run all pre-flight checks before merge.

    Args:
        feature_slug: Feature identifier (e.g., "017-smarter-feature-merge")
        target_branch: Branch to merge into (e.g., "main")
        repo_root: Repository root path
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples

    Returns:
        PreflightResult with all check outcomes
    """
    result = PreflightResult(passed=True)

    # Check for missing worktrees based on tasks in kitty-specs
    expected_graph = build_dependency_graph(repo_root / KITTY_SPECS_DIR / feature_slug)
    expected_wps = set(expected_graph.keys())
    discovered_wps = {wp_id for _, wp_id, _ in wp_workspaces}
    missing_wps = sorted(expected_wps - discovered_wps)
    if missing_wps:
        for wp_id in missing_wps:
            lane = _wp_lane_from_feature(repo_root, feature_slug, wp_id)
            if lane == "done":
                result.warnings.append(
                    f"Skipping missing worktree check for {wp_id} (lane=done)."
                )
                continue

            result.passed = False
            expected_path = repo_root / WORKTREES_DIR / f"{feature_slug}-{wp_id}"
            error = f"Missing worktree for {wp_id}. Expected at {expected_path.name}. Run: spec-kitty agent workflow implement {wp_id}"
            result.wp_statuses.append(
                WPStatus(
                    wp_id=wp_id,
                    worktree_path=expected_path,
                    branch_name=f"{feature_slug}-{wp_id}",
                    is_clean=False,
                    error=error,
                )
            )
            result.errors.append(error)

    # Check all worktrees
    for wt_path, wp_id, branch in wp_workspaces:
        status = check_worktree_status(wt_path, wp_id, branch)
        result.wp_statuses.append(status)
        if not status.is_clean:
            result.passed = False
            result.errors.append(status.error or f"{wp_id} has uncommitted changes")

    # Check target divergence
    diverged, msg = None
    result.target_diverged = diverged
    result.target_divergence_msg = msg
    if diverged:
        result.passed = False
        result.errors.append(msg or f"{target_branch} has diverged from origin")

    return result


def x_run_preflight__mutmut_59(
    feature_slug: str,
    target_branch: str,
    repo_root: Path,
    wp_workspaces: list[tuple[Path, str, str]],
) -> PreflightResult:
    """Run all pre-flight checks before merge.

    Args:
        feature_slug: Feature identifier (e.g., "017-smarter-feature-merge")
        target_branch: Branch to merge into (e.g., "main")
        repo_root: Repository root path
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples

    Returns:
        PreflightResult with all check outcomes
    """
    result = PreflightResult(passed=True)

    # Check for missing worktrees based on tasks in kitty-specs
    expected_graph = build_dependency_graph(repo_root / KITTY_SPECS_DIR / feature_slug)
    expected_wps = set(expected_graph.keys())
    discovered_wps = {wp_id for _, wp_id, _ in wp_workspaces}
    missing_wps = sorted(expected_wps - discovered_wps)
    if missing_wps:
        for wp_id in missing_wps:
            lane = _wp_lane_from_feature(repo_root, feature_slug, wp_id)
            if lane == "done":
                result.warnings.append(
                    f"Skipping missing worktree check for {wp_id} (lane=done)."
                )
                continue

            result.passed = False
            expected_path = repo_root / WORKTREES_DIR / f"{feature_slug}-{wp_id}"
            error = f"Missing worktree for {wp_id}. Expected at {expected_path.name}. Run: spec-kitty agent workflow implement {wp_id}"
            result.wp_statuses.append(
                WPStatus(
                    wp_id=wp_id,
                    worktree_path=expected_path,
                    branch_name=f"{feature_slug}-{wp_id}",
                    is_clean=False,
                    error=error,
                )
            )
            result.errors.append(error)

    # Check all worktrees
    for wt_path, wp_id, branch in wp_workspaces:
        status = check_worktree_status(wt_path, wp_id, branch)
        result.wp_statuses.append(status)
        if not status.is_clean:
            result.passed = False
            result.errors.append(status.error or f"{wp_id} has uncommitted changes")

    # Check target divergence
    diverged, msg = check_target_divergence(None, repo_root)
    result.target_diverged = diverged
    result.target_divergence_msg = msg
    if diverged:
        result.passed = False
        result.errors.append(msg or f"{target_branch} has diverged from origin")

    return result


def x_run_preflight__mutmut_60(
    feature_slug: str,
    target_branch: str,
    repo_root: Path,
    wp_workspaces: list[tuple[Path, str, str]],
) -> PreflightResult:
    """Run all pre-flight checks before merge.

    Args:
        feature_slug: Feature identifier (e.g., "017-smarter-feature-merge")
        target_branch: Branch to merge into (e.g., "main")
        repo_root: Repository root path
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples

    Returns:
        PreflightResult with all check outcomes
    """
    result = PreflightResult(passed=True)

    # Check for missing worktrees based on tasks in kitty-specs
    expected_graph = build_dependency_graph(repo_root / KITTY_SPECS_DIR / feature_slug)
    expected_wps = set(expected_graph.keys())
    discovered_wps = {wp_id for _, wp_id, _ in wp_workspaces}
    missing_wps = sorted(expected_wps - discovered_wps)
    if missing_wps:
        for wp_id in missing_wps:
            lane = _wp_lane_from_feature(repo_root, feature_slug, wp_id)
            if lane == "done":
                result.warnings.append(
                    f"Skipping missing worktree check for {wp_id} (lane=done)."
                )
                continue

            result.passed = False
            expected_path = repo_root / WORKTREES_DIR / f"{feature_slug}-{wp_id}"
            error = f"Missing worktree for {wp_id}. Expected at {expected_path.name}. Run: spec-kitty agent workflow implement {wp_id}"
            result.wp_statuses.append(
                WPStatus(
                    wp_id=wp_id,
                    worktree_path=expected_path,
                    branch_name=f"{feature_slug}-{wp_id}",
                    is_clean=False,
                    error=error,
                )
            )
            result.errors.append(error)

    # Check all worktrees
    for wt_path, wp_id, branch in wp_workspaces:
        status = check_worktree_status(wt_path, wp_id, branch)
        result.wp_statuses.append(status)
        if not status.is_clean:
            result.passed = False
            result.errors.append(status.error or f"{wp_id} has uncommitted changes")

    # Check target divergence
    diverged, msg = check_target_divergence(target_branch, None)
    result.target_diverged = diverged
    result.target_divergence_msg = msg
    if diverged:
        result.passed = False
        result.errors.append(msg or f"{target_branch} has diverged from origin")

    return result


def x_run_preflight__mutmut_61(
    feature_slug: str,
    target_branch: str,
    repo_root: Path,
    wp_workspaces: list[tuple[Path, str, str]],
) -> PreflightResult:
    """Run all pre-flight checks before merge.

    Args:
        feature_slug: Feature identifier (e.g., "017-smarter-feature-merge")
        target_branch: Branch to merge into (e.g., "main")
        repo_root: Repository root path
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples

    Returns:
        PreflightResult with all check outcomes
    """
    result = PreflightResult(passed=True)

    # Check for missing worktrees based on tasks in kitty-specs
    expected_graph = build_dependency_graph(repo_root / KITTY_SPECS_DIR / feature_slug)
    expected_wps = set(expected_graph.keys())
    discovered_wps = {wp_id for _, wp_id, _ in wp_workspaces}
    missing_wps = sorted(expected_wps - discovered_wps)
    if missing_wps:
        for wp_id in missing_wps:
            lane = _wp_lane_from_feature(repo_root, feature_slug, wp_id)
            if lane == "done":
                result.warnings.append(
                    f"Skipping missing worktree check for {wp_id} (lane=done)."
                )
                continue

            result.passed = False
            expected_path = repo_root / WORKTREES_DIR / f"{feature_slug}-{wp_id}"
            error = f"Missing worktree for {wp_id}. Expected at {expected_path.name}. Run: spec-kitty agent workflow implement {wp_id}"
            result.wp_statuses.append(
                WPStatus(
                    wp_id=wp_id,
                    worktree_path=expected_path,
                    branch_name=f"{feature_slug}-{wp_id}",
                    is_clean=False,
                    error=error,
                )
            )
            result.errors.append(error)

    # Check all worktrees
    for wt_path, wp_id, branch in wp_workspaces:
        status = check_worktree_status(wt_path, wp_id, branch)
        result.wp_statuses.append(status)
        if not status.is_clean:
            result.passed = False
            result.errors.append(status.error or f"{wp_id} has uncommitted changes")

    # Check target divergence
    diverged, msg = check_target_divergence(repo_root)
    result.target_diverged = diverged
    result.target_divergence_msg = msg
    if diverged:
        result.passed = False
        result.errors.append(msg or f"{target_branch} has diverged from origin")

    return result


def x_run_preflight__mutmut_62(
    feature_slug: str,
    target_branch: str,
    repo_root: Path,
    wp_workspaces: list[tuple[Path, str, str]],
) -> PreflightResult:
    """Run all pre-flight checks before merge.

    Args:
        feature_slug: Feature identifier (e.g., "017-smarter-feature-merge")
        target_branch: Branch to merge into (e.g., "main")
        repo_root: Repository root path
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples

    Returns:
        PreflightResult with all check outcomes
    """
    result = PreflightResult(passed=True)

    # Check for missing worktrees based on tasks in kitty-specs
    expected_graph = build_dependency_graph(repo_root / KITTY_SPECS_DIR / feature_slug)
    expected_wps = set(expected_graph.keys())
    discovered_wps = {wp_id for _, wp_id, _ in wp_workspaces}
    missing_wps = sorted(expected_wps - discovered_wps)
    if missing_wps:
        for wp_id in missing_wps:
            lane = _wp_lane_from_feature(repo_root, feature_slug, wp_id)
            if lane == "done":
                result.warnings.append(
                    f"Skipping missing worktree check for {wp_id} (lane=done)."
                )
                continue

            result.passed = False
            expected_path = repo_root / WORKTREES_DIR / f"{feature_slug}-{wp_id}"
            error = f"Missing worktree for {wp_id}. Expected at {expected_path.name}. Run: spec-kitty agent workflow implement {wp_id}"
            result.wp_statuses.append(
                WPStatus(
                    wp_id=wp_id,
                    worktree_path=expected_path,
                    branch_name=f"{feature_slug}-{wp_id}",
                    is_clean=False,
                    error=error,
                )
            )
            result.errors.append(error)

    # Check all worktrees
    for wt_path, wp_id, branch in wp_workspaces:
        status = check_worktree_status(wt_path, wp_id, branch)
        result.wp_statuses.append(status)
        if not status.is_clean:
            result.passed = False
            result.errors.append(status.error or f"{wp_id} has uncommitted changes")

    # Check target divergence
    diverged, msg = check_target_divergence(target_branch, )
    result.target_diverged = diverged
    result.target_divergence_msg = msg
    if diverged:
        result.passed = False
        result.errors.append(msg or f"{target_branch} has diverged from origin")

    return result


def x_run_preflight__mutmut_63(
    feature_slug: str,
    target_branch: str,
    repo_root: Path,
    wp_workspaces: list[tuple[Path, str, str]],
) -> PreflightResult:
    """Run all pre-flight checks before merge.

    Args:
        feature_slug: Feature identifier (e.g., "017-smarter-feature-merge")
        target_branch: Branch to merge into (e.g., "main")
        repo_root: Repository root path
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples

    Returns:
        PreflightResult with all check outcomes
    """
    result = PreflightResult(passed=True)

    # Check for missing worktrees based on tasks in kitty-specs
    expected_graph = build_dependency_graph(repo_root / KITTY_SPECS_DIR / feature_slug)
    expected_wps = set(expected_graph.keys())
    discovered_wps = {wp_id for _, wp_id, _ in wp_workspaces}
    missing_wps = sorted(expected_wps - discovered_wps)
    if missing_wps:
        for wp_id in missing_wps:
            lane = _wp_lane_from_feature(repo_root, feature_slug, wp_id)
            if lane == "done":
                result.warnings.append(
                    f"Skipping missing worktree check for {wp_id} (lane=done)."
                )
                continue

            result.passed = False
            expected_path = repo_root / WORKTREES_DIR / f"{feature_slug}-{wp_id}"
            error = f"Missing worktree for {wp_id}. Expected at {expected_path.name}. Run: spec-kitty agent workflow implement {wp_id}"
            result.wp_statuses.append(
                WPStatus(
                    wp_id=wp_id,
                    worktree_path=expected_path,
                    branch_name=f"{feature_slug}-{wp_id}",
                    is_clean=False,
                    error=error,
                )
            )
            result.errors.append(error)

    # Check all worktrees
    for wt_path, wp_id, branch in wp_workspaces:
        status = check_worktree_status(wt_path, wp_id, branch)
        result.wp_statuses.append(status)
        if not status.is_clean:
            result.passed = False
            result.errors.append(status.error or f"{wp_id} has uncommitted changes")

    # Check target divergence
    diverged, msg = check_target_divergence(target_branch, repo_root)
    result.target_diverged = None
    result.target_divergence_msg = msg
    if diverged:
        result.passed = False
        result.errors.append(msg or f"{target_branch} has diverged from origin")

    return result


def x_run_preflight__mutmut_64(
    feature_slug: str,
    target_branch: str,
    repo_root: Path,
    wp_workspaces: list[tuple[Path, str, str]],
) -> PreflightResult:
    """Run all pre-flight checks before merge.

    Args:
        feature_slug: Feature identifier (e.g., "017-smarter-feature-merge")
        target_branch: Branch to merge into (e.g., "main")
        repo_root: Repository root path
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples

    Returns:
        PreflightResult with all check outcomes
    """
    result = PreflightResult(passed=True)

    # Check for missing worktrees based on tasks in kitty-specs
    expected_graph = build_dependency_graph(repo_root / KITTY_SPECS_DIR / feature_slug)
    expected_wps = set(expected_graph.keys())
    discovered_wps = {wp_id for _, wp_id, _ in wp_workspaces}
    missing_wps = sorted(expected_wps - discovered_wps)
    if missing_wps:
        for wp_id in missing_wps:
            lane = _wp_lane_from_feature(repo_root, feature_slug, wp_id)
            if lane == "done":
                result.warnings.append(
                    f"Skipping missing worktree check for {wp_id} (lane=done)."
                )
                continue

            result.passed = False
            expected_path = repo_root / WORKTREES_DIR / f"{feature_slug}-{wp_id}"
            error = f"Missing worktree for {wp_id}. Expected at {expected_path.name}. Run: spec-kitty agent workflow implement {wp_id}"
            result.wp_statuses.append(
                WPStatus(
                    wp_id=wp_id,
                    worktree_path=expected_path,
                    branch_name=f"{feature_slug}-{wp_id}",
                    is_clean=False,
                    error=error,
                )
            )
            result.errors.append(error)

    # Check all worktrees
    for wt_path, wp_id, branch in wp_workspaces:
        status = check_worktree_status(wt_path, wp_id, branch)
        result.wp_statuses.append(status)
        if not status.is_clean:
            result.passed = False
            result.errors.append(status.error or f"{wp_id} has uncommitted changes")

    # Check target divergence
    diverged, msg = check_target_divergence(target_branch, repo_root)
    result.target_diverged = diverged
    result.target_divergence_msg = None
    if diverged:
        result.passed = False
        result.errors.append(msg or f"{target_branch} has diverged from origin")

    return result


def x_run_preflight__mutmut_65(
    feature_slug: str,
    target_branch: str,
    repo_root: Path,
    wp_workspaces: list[tuple[Path, str, str]],
) -> PreflightResult:
    """Run all pre-flight checks before merge.

    Args:
        feature_slug: Feature identifier (e.g., "017-smarter-feature-merge")
        target_branch: Branch to merge into (e.g., "main")
        repo_root: Repository root path
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples

    Returns:
        PreflightResult with all check outcomes
    """
    result = PreflightResult(passed=True)

    # Check for missing worktrees based on tasks in kitty-specs
    expected_graph = build_dependency_graph(repo_root / KITTY_SPECS_DIR / feature_slug)
    expected_wps = set(expected_graph.keys())
    discovered_wps = {wp_id for _, wp_id, _ in wp_workspaces}
    missing_wps = sorted(expected_wps - discovered_wps)
    if missing_wps:
        for wp_id in missing_wps:
            lane = _wp_lane_from_feature(repo_root, feature_slug, wp_id)
            if lane == "done":
                result.warnings.append(
                    f"Skipping missing worktree check for {wp_id} (lane=done)."
                )
                continue

            result.passed = False
            expected_path = repo_root / WORKTREES_DIR / f"{feature_slug}-{wp_id}"
            error = f"Missing worktree for {wp_id}. Expected at {expected_path.name}. Run: spec-kitty agent workflow implement {wp_id}"
            result.wp_statuses.append(
                WPStatus(
                    wp_id=wp_id,
                    worktree_path=expected_path,
                    branch_name=f"{feature_slug}-{wp_id}",
                    is_clean=False,
                    error=error,
                )
            )
            result.errors.append(error)

    # Check all worktrees
    for wt_path, wp_id, branch in wp_workspaces:
        status = check_worktree_status(wt_path, wp_id, branch)
        result.wp_statuses.append(status)
        if not status.is_clean:
            result.passed = False
            result.errors.append(status.error or f"{wp_id} has uncommitted changes")

    # Check target divergence
    diverged, msg = check_target_divergence(target_branch, repo_root)
    result.target_diverged = diverged
    result.target_divergence_msg = msg
    if diverged:
        result.passed = None
        result.errors.append(msg or f"{target_branch} has diverged from origin")

    return result


def x_run_preflight__mutmut_66(
    feature_slug: str,
    target_branch: str,
    repo_root: Path,
    wp_workspaces: list[tuple[Path, str, str]],
) -> PreflightResult:
    """Run all pre-flight checks before merge.

    Args:
        feature_slug: Feature identifier (e.g., "017-smarter-feature-merge")
        target_branch: Branch to merge into (e.g., "main")
        repo_root: Repository root path
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples

    Returns:
        PreflightResult with all check outcomes
    """
    result = PreflightResult(passed=True)

    # Check for missing worktrees based on tasks in kitty-specs
    expected_graph = build_dependency_graph(repo_root / KITTY_SPECS_DIR / feature_slug)
    expected_wps = set(expected_graph.keys())
    discovered_wps = {wp_id for _, wp_id, _ in wp_workspaces}
    missing_wps = sorted(expected_wps - discovered_wps)
    if missing_wps:
        for wp_id in missing_wps:
            lane = _wp_lane_from_feature(repo_root, feature_slug, wp_id)
            if lane == "done":
                result.warnings.append(
                    f"Skipping missing worktree check for {wp_id} (lane=done)."
                )
                continue

            result.passed = False
            expected_path = repo_root / WORKTREES_DIR / f"{feature_slug}-{wp_id}"
            error = f"Missing worktree for {wp_id}. Expected at {expected_path.name}. Run: spec-kitty agent workflow implement {wp_id}"
            result.wp_statuses.append(
                WPStatus(
                    wp_id=wp_id,
                    worktree_path=expected_path,
                    branch_name=f"{feature_slug}-{wp_id}",
                    is_clean=False,
                    error=error,
                )
            )
            result.errors.append(error)

    # Check all worktrees
    for wt_path, wp_id, branch in wp_workspaces:
        status = check_worktree_status(wt_path, wp_id, branch)
        result.wp_statuses.append(status)
        if not status.is_clean:
            result.passed = False
            result.errors.append(status.error or f"{wp_id} has uncommitted changes")

    # Check target divergence
    diverged, msg = check_target_divergence(target_branch, repo_root)
    result.target_diverged = diverged
    result.target_divergence_msg = msg
    if diverged:
        result.passed = True
        result.errors.append(msg or f"{target_branch} has diverged from origin")

    return result


def x_run_preflight__mutmut_67(
    feature_slug: str,
    target_branch: str,
    repo_root: Path,
    wp_workspaces: list[tuple[Path, str, str]],
) -> PreflightResult:
    """Run all pre-flight checks before merge.

    Args:
        feature_slug: Feature identifier (e.g., "017-smarter-feature-merge")
        target_branch: Branch to merge into (e.g., "main")
        repo_root: Repository root path
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples

    Returns:
        PreflightResult with all check outcomes
    """
    result = PreflightResult(passed=True)

    # Check for missing worktrees based on tasks in kitty-specs
    expected_graph = build_dependency_graph(repo_root / KITTY_SPECS_DIR / feature_slug)
    expected_wps = set(expected_graph.keys())
    discovered_wps = {wp_id for _, wp_id, _ in wp_workspaces}
    missing_wps = sorted(expected_wps - discovered_wps)
    if missing_wps:
        for wp_id in missing_wps:
            lane = _wp_lane_from_feature(repo_root, feature_slug, wp_id)
            if lane == "done":
                result.warnings.append(
                    f"Skipping missing worktree check for {wp_id} (lane=done)."
                )
                continue

            result.passed = False
            expected_path = repo_root / WORKTREES_DIR / f"{feature_slug}-{wp_id}"
            error = f"Missing worktree for {wp_id}. Expected at {expected_path.name}. Run: spec-kitty agent workflow implement {wp_id}"
            result.wp_statuses.append(
                WPStatus(
                    wp_id=wp_id,
                    worktree_path=expected_path,
                    branch_name=f"{feature_slug}-{wp_id}",
                    is_clean=False,
                    error=error,
                )
            )
            result.errors.append(error)

    # Check all worktrees
    for wt_path, wp_id, branch in wp_workspaces:
        status = check_worktree_status(wt_path, wp_id, branch)
        result.wp_statuses.append(status)
        if not status.is_clean:
            result.passed = False
            result.errors.append(status.error or f"{wp_id} has uncommitted changes")

    # Check target divergence
    diverged, msg = check_target_divergence(target_branch, repo_root)
    result.target_diverged = diverged
    result.target_divergence_msg = msg
    if diverged:
        result.passed = False
        result.errors.append(None)

    return result


def x_run_preflight__mutmut_68(
    feature_slug: str,
    target_branch: str,
    repo_root: Path,
    wp_workspaces: list[tuple[Path, str, str]],
) -> PreflightResult:
    """Run all pre-flight checks before merge.

    Args:
        feature_slug: Feature identifier (e.g., "017-smarter-feature-merge")
        target_branch: Branch to merge into (e.g., "main")
        repo_root: Repository root path
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples

    Returns:
        PreflightResult with all check outcomes
    """
    result = PreflightResult(passed=True)

    # Check for missing worktrees based on tasks in kitty-specs
    expected_graph = build_dependency_graph(repo_root / KITTY_SPECS_DIR / feature_slug)
    expected_wps = set(expected_graph.keys())
    discovered_wps = {wp_id for _, wp_id, _ in wp_workspaces}
    missing_wps = sorted(expected_wps - discovered_wps)
    if missing_wps:
        for wp_id in missing_wps:
            lane = _wp_lane_from_feature(repo_root, feature_slug, wp_id)
            if lane == "done":
                result.warnings.append(
                    f"Skipping missing worktree check for {wp_id} (lane=done)."
                )
                continue

            result.passed = False
            expected_path = repo_root / WORKTREES_DIR / f"{feature_slug}-{wp_id}"
            error = f"Missing worktree for {wp_id}. Expected at {expected_path.name}. Run: spec-kitty agent workflow implement {wp_id}"
            result.wp_statuses.append(
                WPStatus(
                    wp_id=wp_id,
                    worktree_path=expected_path,
                    branch_name=f"{feature_slug}-{wp_id}",
                    is_clean=False,
                    error=error,
                )
            )
            result.errors.append(error)

    # Check all worktrees
    for wt_path, wp_id, branch in wp_workspaces:
        status = check_worktree_status(wt_path, wp_id, branch)
        result.wp_statuses.append(status)
        if not status.is_clean:
            result.passed = False
            result.errors.append(status.error or f"{wp_id} has uncommitted changes")

    # Check target divergence
    diverged, msg = check_target_divergence(target_branch, repo_root)
    result.target_diverged = diverged
    result.target_divergence_msg = msg
    if diverged:
        result.passed = False
        result.errors.append(msg and f"{target_branch} has diverged from origin")

    return result

x_run_preflight__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_run_preflight__mutmut_1': x_run_preflight__mutmut_1, 
    'x_run_preflight__mutmut_2': x_run_preflight__mutmut_2, 
    'x_run_preflight__mutmut_3': x_run_preflight__mutmut_3, 
    'x_run_preflight__mutmut_4': x_run_preflight__mutmut_4, 
    'x_run_preflight__mutmut_5': x_run_preflight__mutmut_5, 
    'x_run_preflight__mutmut_6': x_run_preflight__mutmut_6, 
    'x_run_preflight__mutmut_7': x_run_preflight__mutmut_7, 
    'x_run_preflight__mutmut_8': x_run_preflight__mutmut_8, 
    'x_run_preflight__mutmut_9': x_run_preflight__mutmut_9, 
    'x_run_preflight__mutmut_10': x_run_preflight__mutmut_10, 
    'x_run_preflight__mutmut_11': x_run_preflight__mutmut_11, 
    'x_run_preflight__mutmut_12': x_run_preflight__mutmut_12, 
    'x_run_preflight__mutmut_13': x_run_preflight__mutmut_13, 
    'x_run_preflight__mutmut_14': x_run_preflight__mutmut_14, 
    'x_run_preflight__mutmut_15': x_run_preflight__mutmut_15, 
    'x_run_preflight__mutmut_16': x_run_preflight__mutmut_16, 
    'x_run_preflight__mutmut_17': x_run_preflight__mutmut_17, 
    'x_run_preflight__mutmut_18': x_run_preflight__mutmut_18, 
    'x_run_preflight__mutmut_19': x_run_preflight__mutmut_19, 
    'x_run_preflight__mutmut_20': x_run_preflight__mutmut_20, 
    'x_run_preflight__mutmut_21': x_run_preflight__mutmut_21, 
    'x_run_preflight__mutmut_22': x_run_preflight__mutmut_22, 
    'x_run_preflight__mutmut_23': x_run_preflight__mutmut_23, 
    'x_run_preflight__mutmut_24': x_run_preflight__mutmut_24, 
    'x_run_preflight__mutmut_25': x_run_preflight__mutmut_25, 
    'x_run_preflight__mutmut_26': x_run_preflight__mutmut_26, 
    'x_run_preflight__mutmut_27': x_run_preflight__mutmut_27, 
    'x_run_preflight__mutmut_28': x_run_preflight__mutmut_28, 
    'x_run_preflight__mutmut_29': x_run_preflight__mutmut_29, 
    'x_run_preflight__mutmut_30': x_run_preflight__mutmut_30, 
    'x_run_preflight__mutmut_31': x_run_preflight__mutmut_31, 
    'x_run_preflight__mutmut_32': x_run_preflight__mutmut_32, 
    'x_run_preflight__mutmut_33': x_run_preflight__mutmut_33, 
    'x_run_preflight__mutmut_34': x_run_preflight__mutmut_34, 
    'x_run_preflight__mutmut_35': x_run_preflight__mutmut_35, 
    'x_run_preflight__mutmut_36': x_run_preflight__mutmut_36, 
    'x_run_preflight__mutmut_37': x_run_preflight__mutmut_37, 
    'x_run_preflight__mutmut_38': x_run_preflight__mutmut_38, 
    'x_run_preflight__mutmut_39': x_run_preflight__mutmut_39, 
    'x_run_preflight__mutmut_40': x_run_preflight__mutmut_40, 
    'x_run_preflight__mutmut_41': x_run_preflight__mutmut_41, 
    'x_run_preflight__mutmut_42': x_run_preflight__mutmut_42, 
    'x_run_preflight__mutmut_43': x_run_preflight__mutmut_43, 
    'x_run_preflight__mutmut_44': x_run_preflight__mutmut_44, 
    'x_run_preflight__mutmut_45': x_run_preflight__mutmut_45, 
    'x_run_preflight__mutmut_46': x_run_preflight__mutmut_46, 
    'x_run_preflight__mutmut_47': x_run_preflight__mutmut_47, 
    'x_run_preflight__mutmut_48': x_run_preflight__mutmut_48, 
    'x_run_preflight__mutmut_49': x_run_preflight__mutmut_49, 
    'x_run_preflight__mutmut_50': x_run_preflight__mutmut_50, 
    'x_run_preflight__mutmut_51': x_run_preflight__mutmut_51, 
    'x_run_preflight__mutmut_52': x_run_preflight__mutmut_52, 
    'x_run_preflight__mutmut_53': x_run_preflight__mutmut_53, 
    'x_run_preflight__mutmut_54': x_run_preflight__mutmut_54, 
    'x_run_preflight__mutmut_55': x_run_preflight__mutmut_55, 
    'x_run_preflight__mutmut_56': x_run_preflight__mutmut_56, 
    'x_run_preflight__mutmut_57': x_run_preflight__mutmut_57, 
    'x_run_preflight__mutmut_58': x_run_preflight__mutmut_58, 
    'x_run_preflight__mutmut_59': x_run_preflight__mutmut_59, 
    'x_run_preflight__mutmut_60': x_run_preflight__mutmut_60, 
    'x_run_preflight__mutmut_61': x_run_preflight__mutmut_61, 
    'x_run_preflight__mutmut_62': x_run_preflight__mutmut_62, 
    'x_run_preflight__mutmut_63': x_run_preflight__mutmut_63, 
    'x_run_preflight__mutmut_64': x_run_preflight__mutmut_64, 
    'x_run_preflight__mutmut_65': x_run_preflight__mutmut_65, 
    'x_run_preflight__mutmut_66': x_run_preflight__mutmut_66, 
    'x_run_preflight__mutmut_67': x_run_preflight__mutmut_67, 
    'x_run_preflight__mutmut_68': x_run_preflight__mutmut_68
}
x_run_preflight__mutmut_orig.__name__ = 'x_run_preflight'


def display_preflight_result(result: PreflightResult, console: Console) -> None:
    args = [result, console]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_display_preflight_result__mutmut_orig, x_display_preflight_result__mutmut_mutants, args, kwargs, None)


def x_display_preflight_result__mutmut_orig(result: PreflightResult, console: Console) -> None:
    """Display pre-flight results with Rich formatting.

    Args:
        result: PreflightResult to display
        console: Rich Console instance for output
    """
    console.print("\n[bold]Pre-flight Check[/bold]\n")

    # WP status table
    table = Table(show_header=True, header_style="bold")
    table.add_column("WP")
    table.add_column("Status")
    table.add_column("Issue")

    for status in result.wp_statuses:
        icon = "[green]✓[/green]" if status.is_clean else "[red]✗[/red]"
        issue = status.error or ""
        table.add_row(status.wp_id, icon, issue)

    # Target branch status
    if result.target_diverged:
        table.add_row("Target", "[red]✗[/red]", result.target_divergence_msg or "Diverged")
    else:
        table.add_row("Target", "[green]✓[/green]", "Up to date")

    console.print(table)

    if not result.passed:
        console.print("\n[bold red]Pre-flight failed.[/bold red] Fix these issues before merging:\n")
        for i, error in enumerate(result.errors, 1):
            console.print(f"  {i}. {error}")
        console.print()
    else:
        if result.warnings:
            console.print()
            for warning in result.warnings:
                console.print(f"[yellow]Warning:[/yellow] {warning}")
        console.print("\n[green]Pre-flight passed.[/green] Ready to merge.\n")


def x_display_preflight_result__mutmut_1(result: PreflightResult, console: Console) -> None:
    """Display pre-flight results with Rich formatting.

    Args:
        result: PreflightResult to display
        console: Rich Console instance for output
    """
    console.print(None)

    # WP status table
    table = Table(show_header=True, header_style="bold")
    table.add_column("WP")
    table.add_column("Status")
    table.add_column("Issue")

    for status in result.wp_statuses:
        icon = "[green]✓[/green]" if status.is_clean else "[red]✗[/red]"
        issue = status.error or ""
        table.add_row(status.wp_id, icon, issue)

    # Target branch status
    if result.target_diverged:
        table.add_row("Target", "[red]✗[/red]", result.target_divergence_msg or "Diverged")
    else:
        table.add_row("Target", "[green]✓[/green]", "Up to date")

    console.print(table)

    if not result.passed:
        console.print("\n[bold red]Pre-flight failed.[/bold red] Fix these issues before merging:\n")
        for i, error in enumerate(result.errors, 1):
            console.print(f"  {i}. {error}")
        console.print()
    else:
        if result.warnings:
            console.print()
            for warning in result.warnings:
                console.print(f"[yellow]Warning:[/yellow] {warning}")
        console.print("\n[green]Pre-flight passed.[/green] Ready to merge.\n")


def x_display_preflight_result__mutmut_2(result: PreflightResult, console: Console) -> None:
    """Display pre-flight results with Rich formatting.

    Args:
        result: PreflightResult to display
        console: Rich Console instance for output
    """
    console.print("XX\n[bold]Pre-flight Check[/bold]\nXX")

    # WP status table
    table = Table(show_header=True, header_style="bold")
    table.add_column("WP")
    table.add_column("Status")
    table.add_column("Issue")

    for status in result.wp_statuses:
        icon = "[green]✓[/green]" if status.is_clean else "[red]✗[/red]"
        issue = status.error or ""
        table.add_row(status.wp_id, icon, issue)

    # Target branch status
    if result.target_diverged:
        table.add_row("Target", "[red]✗[/red]", result.target_divergence_msg or "Diverged")
    else:
        table.add_row("Target", "[green]✓[/green]", "Up to date")

    console.print(table)

    if not result.passed:
        console.print("\n[bold red]Pre-flight failed.[/bold red] Fix these issues before merging:\n")
        for i, error in enumerate(result.errors, 1):
            console.print(f"  {i}. {error}")
        console.print()
    else:
        if result.warnings:
            console.print()
            for warning in result.warnings:
                console.print(f"[yellow]Warning:[/yellow] {warning}")
        console.print("\n[green]Pre-flight passed.[/green] Ready to merge.\n")


def x_display_preflight_result__mutmut_3(result: PreflightResult, console: Console) -> None:
    """Display pre-flight results with Rich formatting.

    Args:
        result: PreflightResult to display
        console: Rich Console instance for output
    """
    console.print("\n[bold]pre-flight check[/bold]\n")

    # WP status table
    table = Table(show_header=True, header_style="bold")
    table.add_column("WP")
    table.add_column("Status")
    table.add_column("Issue")

    for status in result.wp_statuses:
        icon = "[green]✓[/green]" if status.is_clean else "[red]✗[/red]"
        issue = status.error or ""
        table.add_row(status.wp_id, icon, issue)

    # Target branch status
    if result.target_diverged:
        table.add_row("Target", "[red]✗[/red]", result.target_divergence_msg or "Diverged")
    else:
        table.add_row("Target", "[green]✓[/green]", "Up to date")

    console.print(table)

    if not result.passed:
        console.print("\n[bold red]Pre-flight failed.[/bold red] Fix these issues before merging:\n")
        for i, error in enumerate(result.errors, 1):
            console.print(f"  {i}. {error}")
        console.print()
    else:
        if result.warnings:
            console.print()
            for warning in result.warnings:
                console.print(f"[yellow]Warning:[/yellow] {warning}")
        console.print("\n[green]Pre-flight passed.[/green] Ready to merge.\n")


def x_display_preflight_result__mutmut_4(result: PreflightResult, console: Console) -> None:
    """Display pre-flight results with Rich formatting.

    Args:
        result: PreflightResult to display
        console: Rich Console instance for output
    """
    console.print("\n[BOLD]PRE-FLIGHT CHECK[/BOLD]\n")

    # WP status table
    table = Table(show_header=True, header_style="bold")
    table.add_column("WP")
    table.add_column("Status")
    table.add_column("Issue")

    for status in result.wp_statuses:
        icon = "[green]✓[/green]" if status.is_clean else "[red]✗[/red]"
        issue = status.error or ""
        table.add_row(status.wp_id, icon, issue)

    # Target branch status
    if result.target_diverged:
        table.add_row("Target", "[red]✗[/red]", result.target_divergence_msg or "Diverged")
    else:
        table.add_row("Target", "[green]✓[/green]", "Up to date")

    console.print(table)

    if not result.passed:
        console.print("\n[bold red]Pre-flight failed.[/bold red] Fix these issues before merging:\n")
        for i, error in enumerate(result.errors, 1):
            console.print(f"  {i}. {error}")
        console.print()
    else:
        if result.warnings:
            console.print()
            for warning in result.warnings:
                console.print(f"[yellow]Warning:[/yellow] {warning}")
        console.print("\n[green]Pre-flight passed.[/green] Ready to merge.\n")


def x_display_preflight_result__mutmut_5(result: PreflightResult, console: Console) -> None:
    """Display pre-flight results with Rich formatting.

    Args:
        result: PreflightResult to display
        console: Rich Console instance for output
    """
    console.print("\n[bold]Pre-flight Check[/bold]\n")

    # WP status table
    table = None
    table.add_column("WP")
    table.add_column("Status")
    table.add_column("Issue")

    for status in result.wp_statuses:
        icon = "[green]✓[/green]" if status.is_clean else "[red]✗[/red]"
        issue = status.error or ""
        table.add_row(status.wp_id, icon, issue)

    # Target branch status
    if result.target_diverged:
        table.add_row("Target", "[red]✗[/red]", result.target_divergence_msg or "Diverged")
    else:
        table.add_row("Target", "[green]✓[/green]", "Up to date")

    console.print(table)

    if not result.passed:
        console.print("\n[bold red]Pre-flight failed.[/bold red] Fix these issues before merging:\n")
        for i, error in enumerate(result.errors, 1):
            console.print(f"  {i}. {error}")
        console.print()
    else:
        if result.warnings:
            console.print()
            for warning in result.warnings:
                console.print(f"[yellow]Warning:[/yellow] {warning}")
        console.print("\n[green]Pre-flight passed.[/green] Ready to merge.\n")


def x_display_preflight_result__mutmut_6(result: PreflightResult, console: Console) -> None:
    """Display pre-flight results with Rich formatting.

    Args:
        result: PreflightResult to display
        console: Rich Console instance for output
    """
    console.print("\n[bold]Pre-flight Check[/bold]\n")

    # WP status table
    table = Table(show_header=None, header_style="bold")
    table.add_column("WP")
    table.add_column("Status")
    table.add_column("Issue")

    for status in result.wp_statuses:
        icon = "[green]✓[/green]" if status.is_clean else "[red]✗[/red]"
        issue = status.error or ""
        table.add_row(status.wp_id, icon, issue)

    # Target branch status
    if result.target_diverged:
        table.add_row("Target", "[red]✗[/red]", result.target_divergence_msg or "Diverged")
    else:
        table.add_row("Target", "[green]✓[/green]", "Up to date")

    console.print(table)

    if not result.passed:
        console.print("\n[bold red]Pre-flight failed.[/bold red] Fix these issues before merging:\n")
        for i, error in enumerate(result.errors, 1):
            console.print(f"  {i}. {error}")
        console.print()
    else:
        if result.warnings:
            console.print()
            for warning in result.warnings:
                console.print(f"[yellow]Warning:[/yellow] {warning}")
        console.print("\n[green]Pre-flight passed.[/green] Ready to merge.\n")


def x_display_preflight_result__mutmut_7(result: PreflightResult, console: Console) -> None:
    """Display pre-flight results with Rich formatting.

    Args:
        result: PreflightResult to display
        console: Rich Console instance for output
    """
    console.print("\n[bold]Pre-flight Check[/bold]\n")

    # WP status table
    table = Table(show_header=True, header_style=None)
    table.add_column("WP")
    table.add_column("Status")
    table.add_column("Issue")

    for status in result.wp_statuses:
        icon = "[green]✓[/green]" if status.is_clean else "[red]✗[/red]"
        issue = status.error or ""
        table.add_row(status.wp_id, icon, issue)

    # Target branch status
    if result.target_diverged:
        table.add_row("Target", "[red]✗[/red]", result.target_divergence_msg or "Diverged")
    else:
        table.add_row("Target", "[green]✓[/green]", "Up to date")

    console.print(table)

    if not result.passed:
        console.print("\n[bold red]Pre-flight failed.[/bold red] Fix these issues before merging:\n")
        for i, error in enumerate(result.errors, 1):
            console.print(f"  {i}. {error}")
        console.print()
    else:
        if result.warnings:
            console.print()
            for warning in result.warnings:
                console.print(f"[yellow]Warning:[/yellow] {warning}")
        console.print("\n[green]Pre-flight passed.[/green] Ready to merge.\n")


def x_display_preflight_result__mutmut_8(result: PreflightResult, console: Console) -> None:
    """Display pre-flight results with Rich formatting.

    Args:
        result: PreflightResult to display
        console: Rich Console instance for output
    """
    console.print("\n[bold]Pre-flight Check[/bold]\n")

    # WP status table
    table = Table(header_style="bold")
    table.add_column("WP")
    table.add_column("Status")
    table.add_column("Issue")

    for status in result.wp_statuses:
        icon = "[green]✓[/green]" if status.is_clean else "[red]✗[/red]"
        issue = status.error or ""
        table.add_row(status.wp_id, icon, issue)

    # Target branch status
    if result.target_diverged:
        table.add_row("Target", "[red]✗[/red]", result.target_divergence_msg or "Diverged")
    else:
        table.add_row("Target", "[green]✓[/green]", "Up to date")

    console.print(table)

    if not result.passed:
        console.print("\n[bold red]Pre-flight failed.[/bold red] Fix these issues before merging:\n")
        for i, error in enumerate(result.errors, 1):
            console.print(f"  {i}. {error}")
        console.print()
    else:
        if result.warnings:
            console.print()
            for warning in result.warnings:
                console.print(f"[yellow]Warning:[/yellow] {warning}")
        console.print("\n[green]Pre-flight passed.[/green] Ready to merge.\n")


def x_display_preflight_result__mutmut_9(result: PreflightResult, console: Console) -> None:
    """Display pre-flight results with Rich formatting.

    Args:
        result: PreflightResult to display
        console: Rich Console instance for output
    """
    console.print("\n[bold]Pre-flight Check[/bold]\n")

    # WP status table
    table = Table(show_header=True, )
    table.add_column("WP")
    table.add_column("Status")
    table.add_column("Issue")

    for status in result.wp_statuses:
        icon = "[green]✓[/green]" if status.is_clean else "[red]✗[/red]"
        issue = status.error or ""
        table.add_row(status.wp_id, icon, issue)

    # Target branch status
    if result.target_diverged:
        table.add_row("Target", "[red]✗[/red]", result.target_divergence_msg or "Diverged")
    else:
        table.add_row("Target", "[green]✓[/green]", "Up to date")

    console.print(table)

    if not result.passed:
        console.print("\n[bold red]Pre-flight failed.[/bold red] Fix these issues before merging:\n")
        for i, error in enumerate(result.errors, 1):
            console.print(f"  {i}. {error}")
        console.print()
    else:
        if result.warnings:
            console.print()
            for warning in result.warnings:
                console.print(f"[yellow]Warning:[/yellow] {warning}")
        console.print("\n[green]Pre-flight passed.[/green] Ready to merge.\n")


def x_display_preflight_result__mutmut_10(result: PreflightResult, console: Console) -> None:
    """Display pre-flight results with Rich formatting.

    Args:
        result: PreflightResult to display
        console: Rich Console instance for output
    """
    console.print("\n[bold]Pre-flight Check[/bold]\n")

    # WP status table
    table = Table(show_header=False, header_style="bold")
    table.add_column("WP")
    table.add_column("Status")
    table.add_column("Issue")

    for status in result.wp_statuses:
        icon = "[green]✓[/green]" if status.is_clean else "[red]✗[/red]"
        issue = status.error or ""
        table.add_row(status.wp_id, icon, issue)

    # Target branch status
    if result.target_diverged:
        table.add_row("Target", "[red]✗[/red]", result.target_divergence_msg or "Diverged")
    else:
        table.add_row("Target", "[green]✓[/green]", "Up to date")

    console.print(table)

    if not result.passed:
        console.print("\n[bold red]Pre-flight failed.[/bold red] Fix these issues before merging:\n")
        for i, error in enumerate(result.errors, 1):
            console.print(f"  {i}. {error}")
        console.print()
    else:
        if result.warnings:
            console.print()
            for warning in result.warnings:
                console.print(f"[yellow]Warning:[/yellow] {warning}")
        console.print("\n[green]Pre-flight passed.[/green] Ready to merge.\n")


def x_display_preflight_result__mutmut_11(result: PreflightResult, console: Console) -> None:
    """Display pre-flight results with Rich formatting.

    Args:
        result: PreflightResult to display
        console: Rich Console instance for output
    """
    console.print("\n[bold]Pre-flight Check[/bold]\n")

    # WP status table
    table = Table(show_header=True, header_style="XXboldXX")
    table.add_column("WP")
    table.add_column("Status")
    table.add_column("Issue")

    for status in result.wp_statuses:
        icon = "[green]✓[/green]" if status.is_clean else "[red]✗[/red]"
        issue = status.error or ""
        table.add_row(status.wp_id, icon, issue)

    # Target branch status
    if result.target_diverged:
        table.add_row("Target", "[red]✗[/red]", result.target_divergence_msg or "Diverged")
    else:
        table.add_row("Target", "[green]✓[/green]", "Up to date")

    console.print(table)

    if not result.passed:
        console.print("\n[bold red]Pre-flight failed.[/bold red] Fix these issues before merging:\n")
        for i, error in enumerate(result.errors, 1):
            console.print(f"  {i}. {error}")
        console.print()
    else:
        if result.warnings:
            console.print()
            for warning in result.warnings:
                console.print(f"[yellow]Warning:[/yellow] {warning}")
        console.print("\n[green]Pre-flight passed.[/green] Ready to merge.\n")


def x_display_preflight_result__mutmut_12(result: PreflightResult, console: Console) -> None:
    """Display pre-flight results with Rich formatting.

    Args:
        result: PreflightResult to display
        console: Rich Console instance for output
    """
    console.print("\n[bold]Pre-flight Check[/bold]\n")

    # WP status table
    table = Table(show_header=True, header_style="BOLD")
    table.add_column("WP")
    table.add_column("Status")
    table.add_column("Issue")

    for status in result.wp_statuses:
        icon = "[green]✓[/green]" if status.is_clean else "[red]✗[/red]"
        issue = status.error or ""
        table.add_row(status.wp_id, icon, issue)

    # Target branch status
    if result.target_diverged:
        table.add_row("Target", "[red]✗[/red]", result.target_divergence_msg or "Diverged")
    else:
        table.add_row("Target", "[green]✓[/green]", "Up to date")

    console.print(table)

    if not result.passed:
        console.print("\n[bold red]Pre-flight failed.[/bold red] Fix these issues before merging:\n")
        for i, error in enumerate(result.errors, 1):
            console.print(f"  {i}. {error}")
        console.print()
    else:
        if result.warnings:
            console.print()
            for warning in result.warnings:
                console.print(f"[yellow]Warning:[/yellow] {warning}")
        console.print("\n[green]Pre-flight passed.[/green] Ready to merge.\n")


def x_display_preflight_result__mutmut_13(result: PreflightResult, console: Console) -> None:
    """Display pre-flight results with Rich formatting.

    Args:
        result: PreflightResult to display
        console: Rich Console instance for output
    """
    console.print("\n[bold]Pre-flight Check[/bold]\n")

    # WP status table
    table = Table(show_header=True, header_style="bold")
    table.add_column(None)
    table.add_column("Status")
    table.add_column("Issue")

    for status in result.wp_statuses:
        icon = "[green]✓[/green]" if status.is_clean else "[red]✗[/red]"
        issue = status.error or ""
        table.add_row(status.wp_id, icon, issue)

    # Target branch status
    if result.target_diverged:
        table.add_row("Target", "[red]✗[/red]", result.target_divergence_msg or "Diverged")
    else:
        table.add_row("Target", "[green]✓[/green]", "Up to date")

    console.print(table)

    if not result.passed:
        console.print("\n[bold red]Pre-flight failed.[/bold red] Fix these issues before merging:\n")
        for i, error in enumerate(result.errors, 1):
            console.print(f"  {i}. {error}")
        console.print()
    else:
        if result.warnings:
            console.print()
            for warning in result.warnings:
                console.print(f"[yellow]Warning:[/yellow] {warning}")
        console.print("\n[green]Pre-flight passed.[/green] Ready to merge.\n")


def x_display_preflight_result__mutmut_14(result: PreflightResult, console: Console) -> None:
    """Display pre-flight results with Rich formatting.

    Args:
        result: PreflightResult to display
        console: Rich Console instance for output
    """
    console.print("\n[bold]Pre-flight Check[/bold]\n")

    # WP status table
    table = Table(show_header=True, header_style="bold")
    table.add_column("XXWPXX")
    table.add_column("Status")
    table.add_column("Issue")

    for status in result.wp_statuses:
        icon = "[green]✓[/green]" if status.is_clean else "[red]✗[/red]"
        issue = status.error or ""
        table.add_row(status.wp_id, icon, issue)

    # Target branch status
    if result.target_diverged:
        table.add_row("Target", "[red]✗[/red]", result.target_divergence_msg or "Diverged")
    else:
        table.add_row("Target", "[green]✓[/green]", "Up to date")

    console.print(table)

    if not result.passed:
        console.print("\n[bold red]Pre-flight failed.[/bold red] Fix these issues before merging:\n")
        for i, error in enumerate(result.errors, 1):
            console.print(f"  {i}. {error}")
        console.print()
    else:
        if result.warnings:
            console.print()
            for warning in result.warnings:
                console.print(f"[yellow]Warning:[/yellow] {warning}")
        console.print("\n[green]Pre-flight passed.[/green] Ready to merge.\n")


def x_display_preflight_result__mutmut_15(result: PreflightResult, console: Console) -> None:
    """Display pre-flight results with Rich formatting.

    Args:
        result: PreflightResult to display
        console: Rich Console instance for output
    """
    console.print("\n[bold]Pre-flight Check[/bold]\n")

    # WP status table
    table = Table(show_header=True, header_style="bold")
    table.add_column("wp")
    table.add_column("Status")
    table.add_column("Issue")

    for status in result.wp_statuses:
        icon = "[green]✓[/green]" if status.is_clean else "[red]✗[/red]"
        issue = status.error or ""
        table.add_row(status.wp_id, icon, issue)

    # Target branch status
    if result.target_diverged:
        table.add_row("Target", "[red]✗[/red]", result.target_divergence_msg or "Diverged")
    else:
        table.add_row("Target", "[green]✓[/green]", "Up to date")

    console.print(table)

    if not result.passed:
        console.print("\n[bold red]Pre-flight failed.[/bold red] Fix these issues before merging:\n")
        for i, error in enumerate(result.errors, 1):
            console.print(f"  {i}. {error}")
        console.print()
    else:
        if result.warnings:
            console.print()
            for warning in result.warnings:
                console.print(f"[yellow]Warning:[/yellow] {warning}")
        console.print("\n[green]Pre-flight passed.[/green] Ready to merge.\n")


def x_display_preflight_result__mutmut_16(result: PreflightResult, console: Console) -> None:
    """Display pre-flight results with Rich formatting.

    Args:
        result: PreflightResult to display
        console: Rich Console instance for output
    """
    console.print("\n[bold]Pre-flight Check[/bold]\n")

    # WP status table
    table = Table(show_header=True, header_style="bold")
    table.add_column("WP")
    table.add_column(None)
    table.add_column("Issue")

    for status in result.wp_statuses:
        icon = "[green]✓[/green]" if status.is_clean else "[red]✗[/red]"
        issue = status.error or ""
        table.add_row(status.wp_id, icon, issue)

    # Target branch status
    if result.target_diverged:
        table.add_row("Target", "[red]✗[/red]", result.target_divergence_msg or "Diverged")
    else:
        table.add_row("Target", "[green]✓[/green]", "Up to date")

    console.print(table)

    if not result.passed:
        console.print("\n[bold red]Pre-flight failed.[/bold red] Fix these issues before merging:\n")
        for i, error in enumerate(result.errors, 1):
            console.print(f"  {i}. {error}")
        console.print()
    else:
        if result.warnings:
            console.print()
            for warning in result.warnings:
                console.print(f"[yellow]Warning:[/yellow] {warning}")
        console.print("\n[green]Pre-flight passed.[/green] Ready to merge.\n")


def x_display_preflight_result__mutmut_17(result: PreflightResult, console: Console) -> None:
    """Display pre-flight results with Rich formatting.

    Args:
        result: PreflightResult to display
        console: Rich Console instance for output
    """
    console.print("\n[bold]Pre-flight Check[/bold]\n")

    # WP status table
    table = Table(show_header=True, header_style="bold")
    table.add_column("WP")
    table.add_column("XXStatusXX")
    table.add_column("Issue")

    for status in result.wp_statuses:
        icon = "[green]✓[/green]" if status.is_clean else "[red]✗[/red]"
        issue = status.error or ""
        table.add_row(status.wp_id, icon, issue)

    # Target branch status
    if result.target_diverged:
        table.add_row("Target", "[red]✗[/red]", result.target_divergence_msg or "Diverged")
    else:
        table.add_row("Target", "[green]✓[/green]", "Up to date")

    console.print(table)

    if not result.passed:
        console.print("\n[bold red]Pre-flight failed.[/bold red] Fix these issues before merging:\n")
        for i, error in enumerate(result.errors, 1):
            console.print(f"  {i}. {error}")
        console.print()
    else:
        if result.warnings:
            console.print()
            for warning in result.warnings:
                console.print(f"[yellow]Warning:[/yellow] {warning}")
        console.print("\n[green]Pre-flight passed.[/green] Ready to merge.\n")


def x_display_preflight_result__mutmut_18(result: PreflightResult, console: Console) -> None:
    """Display pre-flight results with Rich formatting.

    Args:
        result: PreflightResult to display
        console: Rich Console instance for output
    """
    console.print("\n[bold]Pre-flight Check[/bold]\n")

    # WP status table
    table = Table(show_header=True, header_style="bold")
    table.add_column("WP")
    table.add_column("status")
    table.add_column("Issue")

    for status in result.wp_statuses:
        icon = "[green]✓[/green]" if status.is_clean else "[red]✗[/red]"
        issue = status.error or ""
        table.add_row(status.wp_id, icon, issue)

    # Target branch status
    if result.target_diverged:
        table.add_row("Target", "[red]✗[/red]", result.target_divergence_msg or "Diverged")
    else:
        table.add_row("Target", "[green]✓[/green]", "Up to date")

    console.print(table)

    if not result.passed:
        console.print("\n[bold red]Pre-flight failed.[/bold red] Fix these issues before merging:\n")
        for i, error in enumerate(result.errors, 1):
            console.print(f"  {i}. {error}")
        console.print()
    else:
        if result.warnings:
            console.print()
            for warning in result.warnings:
                console.print(f"[yellow]Warning:[/yellow] {warning}")
        console.print("\n[green]Pre-flight passed.[/green] Ready to merge.\n")


def x_display_preflight_result__mutmut_19(result: PreflightResult, console: Console) -> None:
    """Display pre-flight results with Rich formatting.

    Args:
        result: PreflightResult to display
        console: Rich Console instance for output
    """
    console.print("\n[bold]Pre-flight Check[/bold]\n")

    # WP status table
    table = Table(show_header=True, header_style="bold")
    table.add_column("WP")
    table.add_column("STATUS")
    table.add_column("Issue")

    for status in result.wp_statuses:
        icon = "[green]✓[/green]" if status.is_clean else "[red]✗[/red]"
        issue = status.error or ""
        table.add_row(status.wp_id, icon, issue)

    # Target branch status
    if result.target_diverged:
        table.add_row("Target", "[red]✗[/red]", result.target_divergence_msg or "Diverged")
    else:
        table.add_row("Target", "[green]✓[/green]", "Up to date")

    console.print(table)

    if not result.passed:
        console.print("\n[bold red]Pre-flight failed.[/bold red] Fix these issues before merging:\n")
        for i, error in enumerate(result.errors, 1):
            console.print(f"  {i}. {error}")
        console.print()
    else:
        if result.warnings:
            console.print()
            for warning in result.warnings:
                console.print(f"[yellow]Warning:[/yellow] {warning}")
        console.print("\n[green]Pre-flight passed.[/green] Ready to merge.\n")


def x_display_preflight_result__mutmut_20(result: PreflightResult, console: Console) -> None:
    """Display pre-flight results with Rich formatting.

    Args:
        result: PreflightResult to display
        console: Rich Console instance for output
    """
    console.print("\n[bold]Pre-flight Check[/bold]\n")

    # WP status table
    table = Table(show_header=True, header_style="bold")
    table.add_column("WP")
    table.add_column("Status")
    table.add_column(None)

    for status in result.wp_statuses:
        icon = "[green]✓[/green]" if status.is_clean else "[red]✗[/red]"
        issue = status.error or ""
        table.add_row(status.wp_id, icon, issue)

    # Target branch status
    if result.target_diverged:
        table.add_row("Target", "[red]✗[/red]", result.target_divergence_msg or "Diverged")
    else:
        table.add_row("Target", "[green]✓[/green]", "Up to date")

    console.print(table)

    if not result.passed:
        console.print("\n[bold red]Pre-flight failed.[/bold red] Fix these issues before merging:\n")
        for i, error in enumerate(result.errors, 1):
            console.print(f"  {i}. {error}")
        console.print()
    else:
        if result.warnings:
            console.print()
            for warning in result.warnings:
                console.print(f"[yellow]Warning:[/yellow] {warning}")
        console.print("\n[green]Pre-flight passed.[/green] Ready to merge.\n")


def x_display_preflight_result__mutmut_21(result: PreflightResult, console: Console) -> None:
    """Display pre-flight results with Rich formatting.

    Args:
        result: PreflightResult to display
        console: Rich Console instance for output
    """
    console.print("\n[bold]Pre-flight Check[/bold]\n")

    # WP status table
    table = Table(show_header=True, header_style="bold")
    table.add_column("WP")
    table.add_column("Status")
    table.add_column("XXIssueXX")

    for status in result.wp_statuses:
        icon = "[green]✓[/green]" if status.is_clean else "[red]✗[/red]"
        issue = status.error or ""
        table.add_row(status.wp_id, icon, issue)

    # Target branch status
    if result.target_diverged:
        table.add_row("Target", "[red]✗[/red]", result.target_divergence_msg or "Diverged")
    else:
        table.add_row("Target", "[green]✓[/green]", "Up to date")

    console.print(table)

    if not result.passed:
        console.print("\n[bold red]Pre-flight failed.[/bold red] Fix these issues before merging:\n")
        for i, error in enumerate(result.errors, 1):
            console.print(f"  {i}. {error}")
        console.print()
    else:
        if result.warnings:
            console.print()
            for warning in result.warnings:
                console.print(f"[yellow]Warning:[/yellow] {warning}")
        console.print("\n[green]Pre-flight passed.[/green] Ready to merge.\n")


def x_display_preflight_result__mutmut_22(result: PreflightResult, console: Console) -> None:
    """Display pre-flight results with Rich formatting.

    Args:
        result: PreflightResult to display
        console: Rich Console instance for output
    """
    console.print("\n[bold]Pre-flight Check[/bold]\n")

    # WP status table
    table = Table(show_header=True, header_style="bold")
    table.add_column("WP")
    table.add_column("Status")
    table.add_column("issue")

    for status in result.wp_statuses:
        icon = "[green]✓[/green]" if status.is_clean else "[red]✗[/red]"
        issue = status.error or ""
        table.add_row(status.wp_id, icon, issue)

    # Target branch status
    if result.target_diverged:
        table.add_row("Target", "[red]✗[/red]", result.target_divergence_msg or "Diverged")
    else:
        table.add_row("Target", "[green]✓[/green]", "Up to date")

    console.print(table)

    if not result.passed:
        console.print("\n[bold red]Pre-flight failed.[/bold red] Fix these issues before merging:\n")
        for i, error in enumerate(result.errors, 1):
            console.print(f"  {i}. {error}")
        console.print()
    else:
        if result.warnings:
            console.print()
            for warning in result.warnings:
                console.print(f"[yellow]Warning:[/yellow] {warning}")
        console.print("\n[green]Pre-flight passed.[/green] Ready to merge.\n")


def x_display_preflight_result__mutmut_23(result: PreflightResult, console: Console) -> None:
    """Display pre-flight results with Rich formatting.

    Args:
        result: PreflightResult to display
        console: Rich Console instance for output
    """
    console.print("\n[bold]Pre-flight Check[/bold]\n")

    # WP status table
    table = Table(show_header=True, header_style="bold")
    table.add_column("WP")
    table.add_column("Status")
    table.add_column("ISSUE")

    for status in result.wp_statuses:
        icon = "[green]✓[/green]" if status.is_clean else "[red]✗[/red]"
        issue = status.error or ""
        table.add_row(status.wp_id, icon, issue)

    # Target branch status
    if result.target_diverged:
        table.add_row("Target", "[red]✗[/red]", result.target_divergence_msg or "Diverged")
    else:
        table.add_row("Target", "[green]✓[/green]", "Up to date")

    console.print(table)

    if not result.passed:
        console.print("\n[bold red]Pre-flight failed.[/bold red] Fix these issues before merging:\n")
        for i, error in enumerate(result.errors, 1):
            console.print(f"  {i}. {error}")
        console.print()
    else:
        if result.warnings:
            console.print()
            for warning in result.warnings:
                console.print(f"[yellow]Warning:[/yellow] {warning}")
        console.print("\n[green]Pre-flight passed.[/green] Ready to merge.\n")


def x_display_preflight_result__mutmut_24(result: PreflightResult, console: Console) -> None:
    """Display pre-flight results with Rich formatting.

    Args:
        result: PreflightResult to display
        console: Rich Console instance for output
    """
    console.print("\n[bold]Pre-flight Check[/bold]\n")

    # WP status table
    table = Table(show_header=True, header_style="bold")
    table.add_column("WP")
    table.add_column("Status")
    table.add_column("Issue")

    for status in result.wp_statuses:
        icon = None
        issue = status.error or ""
        table.add_row(status.wp_id, icon, issue)

    # Target branch status
    if result.target_diverged:
        table.add_row("Target", "[red]✗[/red]", result.target_divergence_msg or "Diverged")
    else:
        table.add_row("Target", "[green]✓[/green]", "Up to date")

    console.print(table)

    if not result.passed:
        console.print("\n[bold red]Pre-flight failed.[/bold red] Fix these issues before merging:\n")
        for i, error in enumerate(result.errors, 1):
            console.print(f"  {i}. {error}")
        console.print()
    else:
        if result.warnings:
            console.print()
            for warning in result.warnings:
                console.print(f"[yellow]Warning:[/yellow] {warning}")
        console.print("\n[green]Pre-flight passed.[/green] Ready to merge.\n")


def x_display_preflight_result__mutmut_25(result: PreflightResult, console: Console) -> None:
    """Display pre-flight results with Rich formatting.

    Args:
        result: PreflightResult to display
        console: Rich Console instance for output
    """
    console.print("\n[bold]Pre-flight Check[/bold]\n")

    # WP status table
    table = Table(show_header=True, header_style="bold")
    table.add_column("WP")
    table.add_column("Status")
    table.add_column("Issue")

    for status in result.wp_statuses:
        icon = "XX[green]✓[/green]XX" if status.is_clean else "[red]✗[/red]"
        issue = status.error or ""
        table.add_row(status.wp_id, icon, issue)

    # Target branch status
    if result.target_diverged:
        table.add_row("Target", "[red]✗[/red]", result.target_divergence_msg or "Diverged")
    else:
        table.add_row("Target", "[green]✓[/green]", "Up to date")

    console.print(table)

    if not result.passed:
        console.print("\n[bold red]Pre-flight failed.[/bold red] Fix these issues before merging:\n")
        for i, error in enumerate(result.errors, 1):
            console.print(f"  {i}. {error}")
        console.print()
    else:
        if result.warnings:
            console.print()
            for warning in result.warnings:
                console.print(f"[yellow]Warning:[/yellow] {warning}")
        console.print("\n[green]Pre-flight passed.[/green] Ready to merge.\n")


def x_display_preflight_result__mutmut_26(result: PreflightResult, console: Console) -> None:
    """Display pre-flight results with Rich formatting.

    Args:
        result: PreflightResult to display
        console: Rich Console instance for output
    """
    console.print("\n[bold]Pre-flight Check[/bold]\n")

    # WP status table
    table = Table(show_header=True, header_style="bold")
    table.add_column("WP")
    table.add_column("Status")
    table.add_column("Issue")

    for status in result.wp_statuses:
        icon = "[GREEN]✓[/GREEN]" if status.is_clean else "[red]✗[/red]"
        issue = status.error or ""
        table.add_row(status.wp_id, icon, issue)

    # Target branch status
    if result.target_diverged:
        table.add_row("Target", "[red]✗[/red]", result.target_divergence_msg or "Diverged")
    else:
        table.add_row("Target", "[green]✓[/green]", "Up to date")

    console.print(table)

    if not result.passed:
        console.print("\n[bold red]Pre-flight failed.[/bold red] Fix these issues before merging:\n")
        for i, error in enumerate(result.errors, 1):
            console.print(f"  {i}. {error}")
        console.print()
    else:
        if result.warnings:
            console.print()
            for warning in result.warnings:
                console.print(f"[yellow]Warning:[/yellow] {warning}")
        console.print("\n[green]Pre-flight passed.[/green] Ready to merge.\n")


def x_display_preflight_result__mutmut_27(result: PreflightResult, console: Console) -> None:
    """Display pre-flight results with Rich formatting.

    Args:
        result: PreflightResult to display
        console: Rich Console instance for output
    """
    console.print("\n[bold]Pre-flight Check[/bold]\n")

    # WP status table
    table = Table(show_header=True, header_style="bold")
    table.add_column("WP")
    table.add_column("Status")
    table.add_column("Issue")

    for status in result.wp_statuses:
        icon = "[green]✓[/green]" if status.is_clean else "XX[red]✗[/red]XX"
        issue = status.error or ""
        table.add_row(status.wp_id, icon, issue)

    # Target branch status
    if result.target_diverged:
        table.add_row("Target", "[red]✗[/red]", result.target_divergence_msg or "Diverged")
    else:
        table.add_row("Target", "[green]✓[/green]", "Up to date")

    console.print(table)

    if not result.passed:
        console.print("\n[bold red]Pre-flight failed.[/bold red] Fix these issues before merging:\n")
        for i, error in enumerate(result.errors, 1):
            console.print(f"  {i}. {error}")
        console.print()
    else:
        if result.warnings:
            console.print()
            for warning in result.warnings:
                console.print(f"[yellow]Warning:[/yellow] {warning}")
        console.print("\n[green]Pre-flight passed.[/green] Ready to merge.\n")


def x_display_preflight_result__mutmut_28(result: PreflightResult, console: Console) -> None:
    """Display pre-flight results with Rich formatting.

    Args:
        result: PreflightResult to display
        console: Rich Console instance for output
    """
    console.print("\n[bold]Pre-flight Check[/bold]\n")

    # WP status table
    table = Table(show_header=True, header_style="bold")
    table.add_column("WP")
    table.add_column("Status")
    table.add_column("Issue")

    for status in result.wp_statuses:
        icon = "[green]✓[/green]" if status.is_clean else "[RED]✗[/RED]"
        issue = status.error or ""
        table.add_row(status.wp_id, icon, issue)

    # Target branch status
    if result.target_diverged:
        table.add_row("Target", "[red]✗[/red]", result.target_divergence_msg or "Diverged")
    else:
        table.add_row("Target", "[green]✓[/green]", "Up to date")

    console.print(table)

    if not result.passed:
        console.print("\n[bold red]Pre-flight failed.[/bold red] Fix these issues before merging:\n")
        for i, error in enumerate(result.errors, 1):
            console.print(f"  {i}. {error}")
        console.print()
    else:
        if result.warnings:
            console.print()
            for warning in result.warnings:
                console.print(f"[yellow]Warning:[/yellow] {warning}")
        console.print("\n[green]Pre-flight passed.[/green] Ready to merge.\n")


def x_display_preflight_result__mutmut_29(result: PreflightResult, console: Console) -> None:
    """Display pre-flight results with Rich formatting.

    Args:
        result: PreflightResult to display
        console: Rich Console instance for output
    """
    console.print("\n[bold]Pre-flight Check[/bold]\n")

    # WP status table
    table = Table(show_header=True, header_style="bold")
    table.add_column("WP")
    table.add_column("Status")
    table.add_column("Issue")

    for status in result.wp_statuses:
        icon = "[green]✓[/green]" if status.is_clean else "[red]✗[/red]"
        issue = None
        table.add_row(status.wp_id, icon, issue)

    # Target branch status
    if result.target_diverged:
        table.add_row("Target", "[red]✗[/red]", result.target_divergence_msg or "Diverged")
    else:
        table.add_row("Target", "[green]✓[/green]", "Up to date")

    console.print(table)

    if not result.passed:
        console.print("\n[bold red]Pre-flight failed.[/bold red] Fix these issues before merging:\n")
        for i, error in enumerate(result.errors, 1):
            console.print(f"  {i}. {error}")
        console.print()
    else:
        if result.warnings:
            console.print()
            for warning in result.warnings:
                console.print(f"[yellow]Warning:[/yellow] {warning}")
        console.print("\n[green]Pre-flight passed.[/green] Ready to merge.\n")


def x_display_preflight_result__mutmut_30(result: PreflightResult, console: Console) -> None:
    """Display pre-flight results with Rich formatting.

    Args:
        result: PreflightResult to display
        console: Rich Console instance for output
    """
    console.print("\n[bold]Pre-flight Check[/bold]\n")

    # WP status table
    table = Table(show_header=True, header_style="bold")
    table.add_column("WP")
    table.add_column("Status")
    table.add_column("Issue")

    for status in result.wp_statuses:
        icon = "[green]✓[/green]" if status.is_clean else "[red]✗[/red]"
        issue = status.error and ""
        table.add_row(status.wp_id, icon, issue)

    # Target branch status
    if result.target_diverged:
        table.add_row("Target", "[red]✗[/red]", result.target_divergence_msg or "Diverged")
    else:
        table.add_row("Target", "[green]✓[/green]", "Up to date")

    console.print(table)

    if not result.passed:
        console.print("\n[bold red]Pre-flight failed.[/bold red] Fix these issues before merging:\n")
        for i, error in enumerate(result.errors, 1):
            console.print(f"  {i}. {error}")
        console.print()
    else:
        if result.warnings:
            console.print()
            for warning in result.warnings:
                console.print(f"[yellow]Warning:[/yellow] {warning}")
        console.print("\n[green]Pre-flight passed.[/green] Ready to merge.\n")


def x_display_preflight_result__mutmut_31(result: PreflightResult, console: Console) -> None:
    """Display pre-flight results with Rich formatting.

    Args:
        result: PreflightResult to display
        console: Rich Console instance for output
    """
    console.print("\n[bold]Pre-flight Check[/bold]\n")

    # WP status table
    table = Table(show_header=True, header_style="bold")
    table.add_column("WP")
    table.add_column("Status")
    table.add_column("Issue")

    for status in result.wp_statuses:
        icon = "[green]✓[/green]" if status.is_clean else "[red]✗[/red]"
        issue = status.error or "XXXX"
        table.add_row(status.wp_id, icon, issue)

    # Target branch status
    if result.target_diverged:
        table.add_row("Target", "[red]✗[/red]", result.target_divergence_msg or "Diverged")
    else:
        table.add_row("Target", "[green]✓[/green]", "Up to date")

    console.print(table)

    if not result.passed:
        console.print("\n[bold red]Pre-flight failed.[/bold red] Fix these issues before merging:\n")
        for i, error in enumerate(result.errors, 1):
            console.print(f"  {i}. {error}")
        console.print()
    else:
        if result.warnings:
            console.print()
            for warning in result.warnings:
                console.print(f"[yellow]Warning:[/yellow] {warning}")
        console.print("\n[green]Pre-flight passed.[/green] Ready to merge.\n")


def x_display_preflight_result__mutmut_32(result: PreflightResult, console: Console) -> None:
    """Display pre-flight results with Rich formatting.

    Args:
        result: PreflightResult to display
        console: Rich Console instance for output
    """
    console.print("\n[bold]Pre-flight Check[/bold]\n")

    # WP status table
    table = Table(show_header=True, header_style="bold")
    table.add_column("WP")
    table.add_column("Status")
    table.add_column("Issue")

    for status in result.wp_statuses:
        icon = "[green]✓[/green]" if status.is_clean else "[red]✗[/red]"
        issue = status.error or ""
        table.add_row(None, icon, issue)

    # Target branch status
    if result.target_diverged:
        table.add_row("Target", "[red]✗[/red]", result.target_divergence_msg or "Diverged")
    else:
        table.add_row("Target", "[green]✓[/green]", "Up to date")

    console.print(table)

    if not result.passed:
        console.print("\n[bold red]Pre-flight failed.[/bold red] Fix these issues before merging:\n")
        for i, error in enumerate(result.errors, 1):
            console.print(f"  {i}. {error}")
        console.print()
    else:
        if result.warnings:
            console.print()
            for warning in result.warnings:
                console.print(f"[yellow]Warning:[/yellow] {warning}")
        console.print("\n[green]Pre-flight passed.[/green] Ready to merge.\n")


def x_display_preflight_result__mutmut_33(result: PreflightResult, console: Console) -> None:
    """Display pre-flight results with Rich formatting.

    Args:
        result: PreflightResult to display
        console: Rich Console instance for output
    """
    console.print("\n[bold]Pre-flight Check[/bold]\n")

    # WP status table
    table = Table(show_header=True, header_style="bold")
    table.add_column("WP")
    table.add_column("Status")
    table.add_column("Issue")

    for status in result.wp_statuses:
        icon = "[green]✓[/green]" if status.is_clean else "[red]✗[/red]"
        issue = status.error or ""
        table.add_row(status.wp_id, None, issue)

    # Target branch status
    if result.target_diverged:
        table.add_row("Target", "[red]✗[/red]", result.target_divergence_msg or "Diverged")
    else:
        table.add_row("Target", "[green]✓[/green]", "Up to date")

    console.print(table)

    if not result.passed:
        console.print("\n[bold red]Pre-flight failed.[/bold red] Fix these issues before merging:\n")
        for i, error in enumerate(result.errors, 1):
            console.print(f"  {i}. {error}")
        console.print()
    else:
        if result.warnings:
            console.print()
            for warning in result.warnings:
                console.print(f"[yellow]Warning:[/yellow] {warning}")
        console.print("\n[green]Pre-flight passed.[/green] Ready to merge.\n")


def x_display_preflight_result__mutmut_34(result: PreflightResult, console: Console) -> None:
    """Display pre-flight results with Rich formatting.

    Args:
        result: PreflightResult to display
        console: Rich Console instance for output
    """
    console.print("\n[bold]Pre-flight Check[/bold]\n")

    # WP status table
    table = Table(show_header=True, header_style="bold")
    table.add_column("WP")
    table.add_column("Status")
    table.add_column("Issue")

    for status in result.wp_statuses:
        icon = "[green]✓[/green]" if status.is_clean else "[red]✗[/red]"
        issue = status.error or ""
        table.add_row(status.wp_id, icon, None)

    # Target branch status
    if result.target_diverged:
        table.add_row("Target", "[red]✗[/red]", result.target_divergence_msg or "Diverged")
    else:
        table.add_row("Target", "[green]✓[/green]", "Up to date")

    console.print(table)

    if not result.passed:
        console.print("\n[bold red]Pre-flight failed.[/bold red] Fix these issues before merging:\n")
        for i, error in enumerate(result.errors, 1):
            console.print(f"  {i}. {error}")
        console.print()
    else:
        if result.warnings:
            console.print()
            for warning in result.warnings:
                console.print(f"[yellow]Warning:[/yellow] {warning}")
        console.print("\n[green]Pre-flight passed.[/green] Ready to merge.\n")


def x_display_preflight_result__mutmut_35(result: PreflightResult, console: Console) -> None:
    """Display pre-flight results with Rich formatting.

    Args:
        result: PreflightResult to display
        console: Rich Console instance for output
    """
    console.print("\n[bold]Pre-flight Check[/bold]\n")

    # WP status table
    table = Table(show_header=True, header_style="bold")
    table.add_column("WP")
    table.add_column("Status")
    table.add_column("Issue")

    for status in result.wp_statuses:
        icon = "[green]✓[/green]" if status.is_clean else "[red]✗[/red]"
        issue = status.error or ""
        table.add_row(icon, issue)

    # Target branch status
    if result.target_diverged:
        table.add_row("Target", "[red]✗[/red]", result.target_divergence_msg or "Diverged")
    else:
        table.add_row("Target", "[green]✓[/green]", "Up to date")

    console.print(table)

    if not result.passed:
        console.print("\n[bold red]Pre-flight failed.[/bold red] Fix these issues before merging:\n")
        for i, error in enumerate(result.errors, 1):
            console.print(f"  {i}. {error}")
        console.print()
    else:
        if result.warnings:
            console.print()
            for warning in result.warnings:
                console.print(f"[yellow]Warning:[/yellow] {warning}")
        console.print("\n[green]Pre-flight passed.[/green] Ready to merge.\n")


def x_display_preflight_result__mutmut_36(result: PreflightResult, console: Console) -> None:
    """Display pre-flight results with Rich formatting.

    Args:
        result: PreflightResult to display
        console: Rich Console instance for output
    """
    console.print("\n[bold]Pre-flight Check[/bold]\n")

    # WP status table
    table = Table(show_header=True, header_style="bold")
    table.add_column("WP")
    table.add_column("Status")
    table.add_column("Issue")

    for status in result.wp_statuses:
        icon = "[green]✓[/green]" if status.is_clean else "[red]✗[/red]"
        issue = status.error or ""
        table.add_row(status.wp_id, issue)

    # Target branch status
    if result.target_diverged:
        table.add_row("Target", "[red]✗[/red]", result.target_divergence_msg or "Diverged")
    else:
        table.add_row("Target", "[green]✓[/green]", "Up to date")

    console.print(table)

    if not result.passed:
        console.print("\n[bold red]Pre-flight failed.[/bold red] Fix these issues before merging:\n")
        for i, error in enumerate(result.errors, 1):
            console.print(f"  {i}. {error}")
        console.print()
    else:
        if result.warnings:
            console.print()
            for warning in result.warnings:
                console.print(f"[yellow]Warning:[/yellow] {warning}")
        console.print("\n[green]Pre-flight passed.[/green] Ready to merge.\n")


def x_display_preflight_result__mutmut_37(result: PreflightResult, console: Console) -> None:
    """Display pre-flight results with Rich formatting.

    Args:
        result: PreflightResult to display
        console: Rich Console instance for output
    """
    console.print("\n[bold]Pre-flight Check[/bold]\n")

    # WP status table
    table = Table(show_header=True, header_style="bold")
    table.add_column("WP")
    table.add_column("Status")
    table.add_column("Issue")

    for status in result.wp_statuses:
        icon = "[green]✓[/green]" if status.is_clean else "[red]✗[/red]"
        issue = status.error or ""
        table.add_row(status.wp_id, icon, )

    # Target branch status
    if result.target_diverged:
        table.add_row("Target", "[red]✗[/red]", result.target_divergence_msg or "Diverged")
    else:
        table.add_row("Target", "[green]✓[/green]", "Up to date")

    console.print(table)

    if not result.passed:
        console.print("\n[bold red]Pre-flight failed.[/bold red] Fix these issues before merging:\n")
        for i, error in enumerate(result.errors, 1):
            console.print(f"  {i}. {error}")
        console.print()
    else:
        if result.warnings:
            console.print()
            for warning in result.warnings:
                console.print(f"[yellow]Warning:[/yellow] {warning}")
        console.print("\n[green]Pre-flight passed.[/green] Ready to merge.\n")


def x_display_preflight_result__mutmut_38(result: PreflightResult, console: Console) -> None:
    """Display pre-flight results with Rich formatting.

    Args:
        result: PreflightResult to display
        console: Rich Console instance for output
    """
    console.print("\n[bold]Pre-flight Check[/bold]\n")

    # WP status table
    table = Table(show_header=True, header_style="bold")
    table.add_column("WP")
    table.add_column("Status")
    table.add_column("Issue")

    for status in result.wp_statuses:
        icon = "[green]✓[/green]" if status.is_clean else "[red]✗[/red]"
        issue = status.error or ""
        table.add_row(status.wp_id, icon, issue)

    # Target branch status
    if result.target_diverged:
        table.add_row(None, "[red]✗[/red]", result.target_divergence_msg or "Diverged")
    else:
        table.add_row("Target", "[green]✓[/green]", "Up to date")

    console.print(table)

    if not result.passed:
        console.print("\n[bold red]Pre-flight failed.[/bold red] Fix these issues before merging:\n")
        for i, error in enumerate(result.errors, 1):
            console.print(f"  {i}. {error}")
        console.print()
    else:
        if result.warnings:
            console.print()
            for warning in result.warnings:
                console.print(f"[yellow]Warning:[/yellow] {warning}")
        console.print("\n[green]Pre-flight passed.[/green] Ready to merge.\n")


def x_display_preflight_result__mutmut_39(result: PreflightResult, console: Console) -> None:
    """Display pre-flight results with Rich formatting.

    Args:
        result: PreflightResult to display
        console: Rich Console instance for output
    """
    console.print("\n[bold]Pre-flight Check[/bold]\n")

    # WP status table
    table = Table(show_header=True, header_style="bold")
    table.add_column("WP")
    table.add_column("Status")
    table.add_column("Issue")

    for status in result.wp_statuses:
        icon = "[green]✓[/green]" if status.is_clean else "[red]✗[/red]"
        issue = status.error or ""
        table.add_row(status.wp_id, icon, issue)

    # Target branch status
    if result.target_diverged:
        table.add_row("Target", None, result.target_divergence_msg or "Diverged")
    else:
        table.add_row("Target", "[green]✓[/green]", "Up to date")

    console.print(table)

    if not result.passed:
        console.print("\n[bold red]Pre-flight failed.[/bold red] Fix these issues before merging:\n")
        for i, error in enumerate(result.errors, 1):
            console.print(f"  {i}. {error}")
        console.print()
    else:
        if result.warnings:
            console.print()
            for warning in result.warnings:
                console.print(f"[yellow]Warning:[/yellow] {warning}")
        console.print("\n[green]Pre-flight passed.[/green] Ready to merge.\n")


def x_display_preflight_result__mutmut_40(result: PreflightResult, console: Console) -> None:
    """Display pre-flight results with Rich formatting.

    Args:
        result: PreflightResult to display
        console: Rich Console instance for output
    """
    console.print("\n[bold]Pre-flight Check[/bold]\n")

    # WP status table
    table = Table(show_header=True, header_style="bold")
    table.add_column("WP")
    table.add_column("Status")
    table.add_column("Issue")

    for status in result.wp_statuses:
        icon = "[green]✓[/green]" if status.is_clean else "[red]✗[/red]"
        issue = status.error or ""
        table.add_row(status.wp_id, icon, issue)

    # Target branch status
    if result.target_diverged:
        table.add_row("Target", "[red]✗[/red]", None)
    else:
        table.add_row("Target", "[green]✓[/green]", "Up to date")

    console.print(table)

    if not result.passed:
        console.print("\n[bold red]Pre-flight failed.[/bold red] Fix these issues before merging:\n")
        for i, error in enumerate(result.errors, 1):
            console.print(f"  {i}. {error}")
        console.print()
    else:
        if result.warnings:
            console.print()
            for warning in result.warnings:
                console.print(f"[yellow]Warning:[/yellow] {warning}")
        console.print("\n[green]Pre-flight passed.[/green] Ready to merge.\n")


def x_display_preflight_result__mutmut_41(result: PreflightResult, console: Console) -> None:
    """Display pre-flight results with Rich formatting.

    Args:
        result: PreflightResult to display
        console: Rich Console instance for output
    """
    console.print("\n[bold]Pre-flight Check[/bold]\n")

    # WP status table
    table = Table(show_header=True, header_style="bold")
    table.add_column("WP")
    table.add_column("Status")
    table.add_column("Issue")

    for status in result.wp_statuses:
        icon = "[green]✓[/green]" if status.is_clean else "[red]✗[/red]"
        issue = status.error or ""
        table.add_row(status.wp_id, icon, issue)

    # Target branch status
    if result.target_diverged:
        table.add_row("[red]✗[/red]", result.target_divergence_msg or "Diverged")
    else:
        table.add_row("Target", "[green]✓[/green]", "Up to date")

    console.print(table)

    if not result.passed:
        console.print("\n[bold red]Pre-flight failed.[/bold red] Fix these issues before merging:\n")
        for i, error in enumerate(result.errors, 1):
            console.print(f"  {i}. {error}")
        console.print()
    else:
        if result.warnings:
            console.print()
            for warning in result.warnings:
                console.print(f"[yellow]Warning:[/yellow] {warning}")
        console.print("\n[green]Pre-flight passed.[/green] Ready to merge.\n")


def x_display_preflight_result__mutmut_42(result: PreflightResult, console: Console) -> None:
    """Display pre-flight results with Rich formatting.

    Args:
        result: PreflightResult to display
        console: Rich Console instance for output
    """
    console.print("\n[bold]Pre-flight Check[/bold]\n")

    # WP status table
    table = Table(show_header=True, header_style="bold")
    table.add_column("WP")
    table.add_column("Status")
    table.add_column("Issue")

    for status in result.wp_statuses:
        icon = "[green]✓[/green]" if status.is_clean else "[red]✗[/red]"
        issue = status.error or ""
        table.add_row(status.wp_id, icon, issue)

    # Target branch status
    if result.target_diverged:
        table.add_row("Target", result.target_divergence_msg or "Diverged")
    else:
        table.add_row("Target", "[green]✓[/green]", "Up to date")

    console.print(table)

    if not result.passed:
        console.print("\n[bold red]Pre-flight failed.[/bold red] Fix these issues before merging:\n")
        for i, error in enumerate(result.errors, 1):
            console.print(f"  {i}. {error}")
        console.print()
    else:
        if result.warnings:
            console.print()
            for warning in result.warnings:
                console.print(f"[yellow]Warning:[/yellow] {warning}")
        console.print("\n[green]Pre-flight passed.[/green] Ready to merge.\n")


def x_display_preflight_result__mutmut_43(result: PreflightResult, console: Console) -> None:
    """Display pre-flight results with Rich formatting.

    Args:
        result: PreflightResult to display
        console: Rich Console instance for output
    """
    console.print("\n[bold]Pre-flight Check[/bold]\n")

    # WP status table
    table = Table(show_header=True, header_style="bold")
    table.add_column("WP")
    table.add_column("Status")
    table.add_column("Issue")

    for status in result.wp_statuses:
        icon = "[green]✓[/green]" if status.is_clean else "[red]✗[/red]"
        issue = status.error or ""
        table.add_row(status.wp_id, icon, issue)

    # Target branch status
    if result.target_diverged:
        table.add_row("Target", "[red]✗[/red]", )
    else:
        table.add_row("Target", "[green]✓[/green]", "Up to date")

    console.print(table)

    if not result.passed:
        console.print("\n[bold red]Pre-flight failed.[/bold red] Fix these issues before merging:\n")
        for i, error in enumerate(result.errors, 1):
            console.print(f"  {i}. {error}")
        console.print()
    else:
        if result.warnings:
            console.print()
            for warning in result.warnings:
                console.print(f"[yellow]Warning:[/yellow] {warning}")
        console.print("\n[green]Pre-flight passed.[/green] Ready to merge.\n")


def x_display_preflight_result__mutmut_44(result: PreflightResult, console: Console) -> None:
    """Display pre-flight results with Rich formatting.

    Args:
        result: PreflightResult to display
        console: Rich Console instance for output
    """
    console.print("\n[bold]Pre-flight Check[/bold]\n")

    # WP status table
    table = Table(show_header=True, header_style="bold")
    table.add_column("WP")
    table.add_column("Status")
    table.add_column("Issue")

    for status in result.wp_statuses:
        icon = "[green]✓[/green]" if status.is_clean else "[red]✗[/red]"
        issue = status.error or ""
        table.add_row(status.wp_id, icon, issue)

    # Target branch status
    if result.target_diverged:
        table.add_row("XXTargetXX", "[red]✗[/red]", result.target_divergence_msg or "Diverged")
    else:
        table.add_row("Target", "[green]✓[/green]", "Up to date")

    console.print(table)

    if not result.passed:
        console.print("\n[bold red]Pre-flight failed.[/bold red] Fix these issues before merging:\n")
        for i, error in enumerate(result.errors, 1):
            console.print(f"  {i}. {error}")
        console.print()
    else:
        if result.warnings:
            console.print()
            for warning in result.warnings:
                console.print(f"[yellow]Warning:[/yellow] {warning}")
        console.print("\n[green]Pre-flight passed.[/green] Ready to merge.\n")


def x_display_preflight_result__mutmut_45(result: PreflightResult, console: Console) -> None:
    """Display pre-flight results with Rich formatting.

    Args:
        result: PreflightResult to display
        console: Rich Console instance for output
    """
    console.print("\n[bold]Pre-flight Check[/bold]\n")

    # WP status table
    table = Table(show_header=True, header_style="bold")
    table.add_column("WP")
    table.add_column("Status")
    table.add_column("Issue")

    for status in result.wp_statuses:
        icon = "[green]✓[/green]" if status.is_clean else "[red]✗[/red]"
        issue = status.error or ""
        table.add_row(status.wp_id, icon, issue)

    # Target branch status
    if result.target_diverged:
        table.add_row("target", "[red]✗[/red]", result.target_divergence_msg or "Diverged")
    else:
        table.add_row("Target", "[green]✓[/green]", "Up to date")

    console.print(table)

    if not result.passed:
        console.print("\n[bold red]Pre-flight failed.[/bold red] Fix these issues before merging:\n")
        for i, error in enumerate(result.errors, 1):
            console.print(f"  {i}. {error}")
        console.print()
    else:
        if result.warnings:
            console.print()
            for warning in result.warnings:
                console.print(f"[yellow]Warning:[/yellow] {warning}")
        console.print("\n[green]Pre-flight passed.[/green] Ready to merge.\n")


def x_display_preflight_result__mutmut_46(result: PreflightResult, console: Console) -> None:
    """Display pre-flight results with Rich formatting.

    Args:
        result: PreflightResult to display
        console: Rich Console instance for output
    """
    console.print("\n[bold]Pre-flight Check[/bold]\n")

    # WP status table
    table = Table(show_header=True, header_style="bold")
    table.add_column("WP")
    table.add_column("Status")
    table.add_column("Issue")

    for status in result.wp_statuses:
        icon = "[green]✓[/green]" if status.is_clean else "[red]✗[/red]"
        issue = status.error or ""
        table.add_row(status.wp_id, icon, issue)

    # Target branch status
    if result.target_diverged:
        table.add_row("TARGET", "[red]✗[/red]", result.target_divergence_msg or "Diverged")
    else:
        table.add_row("Target", "[green]✓[/green]", "Up to date")

    console.print(table)

    if not result.passed:
        console.print("\n[bold red]Pre-flight failed.[/bold red] Fix these issues before merging:\n")
        for i, error in enumerate(result.errors, 1):
            console.print(f"  {i}. {error}")
        console.print()
    else:
        if result.warnings:
            console.print()
            for warning in result.warnings:
                console.print(f"[yellow]Warning:[/yellow] {warning}")
        console.print("\n[green]Pre-flight passed.[/green] Ready to merge.\n")


def x_display_preflight_result__mutmut_47(result: PreflightResult, console: Console) -> None:
    """Display pre-flight results with Rich formatting.

    Args:
        result: PreflightResult to display
        console: Rich Console instance for output
    """
    console.print("\n[bold]Pre-flight Check[/bold]\n")

    # WP status table
    table = Table(show_header=True, header_style="bold")
    table.add_column("WP")
    table.add_column("Status")
    table.add_column("Issue")

    for status in result.wp_statuses:
        icon = "[green]✓[/green]" if status.is_clean else "[red]✗[/red]"
        issue = status.error or ""
        table.add_row(status.wp_id, icon, issue)

    # Target branch status
    if result.target_diverged:
        table.add_row("Target", "XX[red]✗[/red]XX", result.target_divergence_msg or "Diverged")
    else:
        table.add_row("Target", "[green]✓[/green]", "Up to date")

    console.print(table)

    if not result.passed:
        console.print("\n[bold red]Pre-flight failed.[/bold red] Fix these issues before merging:\n")
        for i, error in enumerate(result.errors, 1):
            console.print(f"  {i}. {error}")
        console.print()
    else:
        if result.warnings:
            console.print()
            for warning in result.warnings:
                console.print(f"[yellow]Warning:[/yellow] {warning}")
        console.print("\n[green]Pre-flight passed.[/green] Ready to merge.\n")


def x_display_preflight_result__mutmut_48(result: PreflightResult, console: Console) -> None:
    """Display pre-flight results with Rich formatting.

    Args:
        result: PreflightResult to display
        console: Rich Console instance for output
    """
    console.print("\n[bold]Pre-flight Check[/bold]\n")

    # WP status table
    table = Table(show_header=True, header_style="bold")
    table.add_column("WP")
    table.add_column("Status")
    table.add_column("Issue")

    for status in result.wp_statuses:
        icon = "[green]✓[/green]" if status.is_clean else "[red]✗[/red]"
        issue = status.error or ""
        table.add_row(status.wp_id, icon, issue)

    # Target branch status
    if result.target_diverged:
        table.add_row("Target", "[RED]✗[/RED]", result.target_divergence_msg or "Diverged")
    else:
        table.add_row("Target", "[green]✓[/green]", "Up to date")

    console.print(table)

    if not result.passed:
        console.print("\n[bold red]Pre-flight failed.[/bold red] Fix these issues before merging:\n")
        for i, error in enumerate(result.errors, 1):
            console.print(f"  {i}. {error}")
        console.print()
    else:
        if result.warnings:
            console.print()
            for warning in result.warnings:
                console.print(f"[yellow]Warning:[/yellow] {warning}")
        console.print("\n[green]Pre-flight passed.[/green] Ready to merge.\n")


def x_display_preflight_result__mutmut_49(result: PreflightResult, console: Console) -> None:
    """Display pre-flight results with Rich formatting.

    Args:
        result: PreflightResult to display
        console: Rich Console instance for output
    """
    console.print("\n[bold]Pre-flight Check[/bold]\n")

    # WP status table
    table = Table(show_header=True, header_style="bold")
    table.add_column("WP")
    table.add_column("Status")
    table.add_column("Issue")

    for status in result.wp_statuses:
        icon = "[green]✓[/green]" if status.is_clean else "[red]✗[/red]"
        issue = status.error or ""
        table.add_row(status.wp_id, icon, issue)

    # Target branch status
    if result.target_diverged:
        table.add_row("Target", "[red]✗[/red]", result.target_divergence_msg and "Diverged")
    else:
        table.add_row("Target", "[green]✓[/green]", "Up to date")

    console.print(table)

    if not result.passed:
        console.print("\n[bold red]Pre-flight failed.[/bold red] Fix these issues before merging:\n")
        for i, error in enumerate(result.errors, 1):
            console.print(f"  {i}. {error}")
        console.print()
    else:
        if result.warnings:
            console.print()
            for warning in result.warnings:
                console.print(f"[yellow]Warning:[/yellow] {warning}")
        console.print("\n[green]Pre-flight passed.[/green] Ready to merge.\n")


def x_display_preflight_result__mutmut_50(result: PreflightResult, console: Console) -> None:
    """Display pre-flight results with Rich formatting.

    Args:
        result: PreflightResult to display
        console: Rich Console instance for output
    """
    console.print("\n[bold]Pre-flight Check[/bold]\n")

    # WP status table
    table = Table(show_header=True, header_style="bold")
    table.add_column("WP")
    table.add_column("Status")
    table.add_column("Issue")

    for status in result.wp_statuses:
        icon = "[green]✓[/green]" if status.is_clean else "[red]✗[/red]"
        issue = status.error or ""
        table.add_row(status.wp_id, icon, issue)

    # Target branch status
    if result.target_diverged:
        table.add_row("Target", "[red]✗[/red]", result.target_divergence_msg or "XXDivergedXX")
    else:
        table.add_row("Target", "[green]✓[/green]", "Up to date")

    console.print(table)

    if not result.passed:
        console.print("\n[bold red]Pre-flight failed.[/bold red] Fix these issues before merging:\n")
        for i, error in enumerate(result.errors, 1):
            console.print(f"  {i}. {error}")
        console.print()
    else:
        if result.warnings:
            console.print()
            for warning in result.warnings:
                console.print(f"[yellow]Warning:[/yellow] {warning}")
        console.print("\n[green]Pre-flight passed.[/green] Ready to merge.\n")


def x_display_preflight_result__mutmut_51(result: PreflightResult, console: Console) -> None:
    """Display pre-flight results with Rich formatting.

    Args:
        result: PreflightResult to display
        console: Rich Console instance for output
    """
    console.print("\n[bold]Pre-flight Check[/bold]\n")

    # WP status table
    table = Table(show_header=True, header_style="bold")
    table.add_column("WP")
    table.add_column("Status")
    table.add_column("Issue")

    for status in result.wp_statuses:
        icon = "[green]✓[/green]" if status.is_clean else "[red]✗[/red]"
        issue = status.error or ""
        table.add_row(status.wp_id, icon, issue)

    # Target branch status
    if result.target_diverged:
        table.add_row("Target", "[red]✗[/red]", result.target_divergence_msg or "diverged")
    else:
        table.add_row("Target", "[green]✓[/green]", "Up to date")

    console.print(table)

    if not result.passed:
        console.print("\n[bold red]Pre-flight failed.[/bold red] Fix these issues before merging:\n")
        for i, error in enumerate(result.errors, 1):
            console.print(f"  {i}. {error}")
        console.print()
    else:
        if result.warnings:
            console.print()
            for warning in result.warnings:
                console.print(f"[yellow]Warning:[/yellow] {warning}")
        console.print("\n[green]Pre-flight passed.[/green] Ready to merge.\n")


def x_display_preflight_result__mutmut_52(result: PreflightResult, console: Console) -> None:
    """Display pre-flight results with Rich formatting.

    Args:
        result: PreflightResult to display
        console: Rich Console instance for output
    """
    console.print("\n[bold]Pre-flight Check[/bold]\n")

    # WP status table
    table = Table(show_header=True, header_style="bold")
    table.add_column("WP")
    table.add_column("Status")
    table.add_column("Issue")

    for status in result.wp_statuses:
        icon = "[green]✓[/green]" if status.is_clean else "[red]✗[/red]"
        issue = status.error or ""
        table.add_row(status.wp_id, icon, issue)

    # Target branch status
    if result.target_diverged:
        table.add_row("Target", "[red]✗[/red]", result.target_divergence_msg or "DIVERGED")
    else:
        table.add_row("Target", "[green]✓[/green]", "Up to date")

    console.print(table)

    if not result.passed:
        console.print("\n[bold red]Pre-flight failed.[/bold red] Fix these issues before merging:\n")
        for i, error in enumerate(result.errors, 1):
            console.print(f"  {i}. {error}")
        console.print()
    else:
        if result.warnings:
            console.print()
            for warning in result.warnings:
                console.print(f"[yellow]Warning:[/yellow] {warning}")
        console.print("\n[green]Pre-flight passed.[/green] Ready to merge.\n")


def x_display_preflight_result__mutmut_53(result: PreflightResult, console: Console) -> None:
    """Display pre-flight results with Rich formatting.

    Args:
        result: PreflightResult to display
        console: Rich Console instance for output
    """
    console.print("\n[bold]Pre-flight Check[/bold]\n")

    # WP status table
    table = Table(show_header=True, header_style="bold")
    table.add_column("WP")
    table.add_column("Status")
    table.add_column("Issue")

    for status in result.wp_statuses:
        icon = "[green]✓[/green]" if status.is_clean else "[red]✗[/red]"
        issue = status.error or ""
        table.add_row(status.wp_id, icon, issue)

    # Target branch status
    if result.target_diverged:
        table.add_row("Target", "[red]✗[/red]", result.target_divergence_msg or "Diverged")
    else:
        table.add_row(None, "[green]✓[/green]", "Up to date")

    console.print(table)

    if not result.passed:
        console.print("\n[bold red]Pre-flight failed.[/bold red] Fix these issues before merging:\n")
        for i, error in enumerate(result.errors, 1):
            console.print(f"  {i}. {error}")
        console.print()
    else:
        if result.warnings:
            console.print()
            for warning in result.warnings:
                console.print(f"[yellow]Warning:[/yellow] {warning}")
        console.print("\n[green]Pre-flight passed.[/green] Ready to merge.\n")


def x_display_preflight_result__mutmut_54(result: PreflightResult, console: Console) -> None:
    """Display pre-flight results with Rich formatting.

    Args:
        result: PreflightResult to display
        console: Rich Console instance for output
    """
    console.print("\n[bold]Pre-flight Check[/bold]\n")

    # WP status table
    table = Table(show_header=True, header_style="bold")
    table.add_column("WP")
    table.add_column("Status")
    table.add_column("Issue")

    for status in result.wp_statuses:
        icon = "[green]✓[/green]" if status.is_clean else "[red]✗[/red]"
        issue = status.error or ""
        table.add_row(status.wp_id, icon, issue)

    # Target branch status
    if result.target_diverged:
        table.add_row("Target", "[red]✗[/red]", result.target_divergence_msg or "Diverged")
    else:
        table.add_row("Target", None, "Up to date")

    console.print(table)

    if not result.passed:
        console.print("\n[bold red]Pre-flight failed.[/bold red] Fix these issues before merging:\n")
        for i, error in enumerate(result.errors, 1):
            console.print(f"  {i}. {error}")
        console.print()
    else:
        if result.warnings:
            console.print()
            for warning in result.warnings:
                console.print(f"[yellow]Warning:[/yellow] {warning}")
        console.print("\n[green]Pre-flight passed.[/green] Ready to merge.\n")


def x_display_preflight_result__mutmut_55(result: PreflightResult, console: Console) -> None:
    """Display pre-flight results with Rich formatting.

    Args:
        result: PreflightResult to display
        console: Rich Console instance for output
    """
    console.print("\n[bold]Pre-flight Check[/bold]\n")

    # WP status table
    table = Table(show_header=True, header_style="bold")
    table.add_column("WP")
    table.add_column("Status")
    table.add_column("Issue")

    for status in result.wp_statuses:
        icon = "[green]✓[/green]" if status.is_clean else "[red]✗[/red]"
        issue = status.error or ""
        table.add_row(status.wp_id, icon, issue)

    # Target branch status
    if result.target_diverged:
        table.add_row("Target", "[red]✗[/red]", result.target_divergence_msg or "Diverged")
    else:
        table.add_row("Target", "[green]✓[/green]", None)

    console.print(table)

    if not result.passed:
        console.print("\n[bold red]Pre-flight failed.[/bold red] Fix these issues before merging:\n")
        for i, error in enumerate(result.errors, 1):
            console.print(f"  {i}. {error}")
        console.print()
    else:
        if result.warnings:
            console.print()
            for warning in result.warnings:
                console.print(f"[yellow]Warning:[/yellow] {warning}")
        console.print("\n[green]Pre-flight passed.[/green] Ready to merge.\n")


def x_display_preflight_result__mutmut_56(result: PreflightResult, console: Console) -> None:
    """Display pre-flight results with Rich formatting.

    Args:
        result: PreflightResult to display
        console: Rich Console instance for output
    """
    console.print("\n[bold]Pre-flight Check[/bold]\n")

    # WP status table
    table = Table(show_header=True, header_style="bold")
    table.add_column("WP")
    table.add_column("Status")
    table.add_column("Issue")

    for status in result.wp_statuses:
        icon = "[green]✓[/green]" if status.is_clean else "[red]✗[/red]"
        issue = status.error or ""
        table.add_row(status.wp_id, icon, issue)

    # Target branch status
    if result.target_diverged:
        table.add_row("Target", "[red]✗[/red]", result.target_divergence_msg or "Diverged")
    else:
        table.add_row("[green]✓[/green]", "Up to date")

    console.print(table)

    if not result.passed:
        console.print("\n[bold red]Pre-flight failed.[/bold red] Fix these issues before merging:\n")
        for i, error in enumerate(result.errors, 1):
            console.print(f"  {i}. {error}")
        console.print()
    else:
        if result.warnings:
            console.print()
            for warning in result.warnings:
                console.print(f"[yellow]Warning:[/yellow] {warning}")
        console.print("\n[green]Pre-flight passed.[/green] Ready to merge.\n")


def x_display_preflight_result__mutmut_57(result: PreflightResult, console: Console) -> None:
    """Display pre-flight results with Rich formatting.

    Args:
        result: PreflightResult to display
        console: Rich Console instance for output
    """
    console.print("\n[bold]Pre-flight Check[/bold]\n")

    # WP status table
    table = Table(show_header=True, header_style="bold")
    table.add_column("WP")
    table.add_column("Status")
    table.add_column("Issue")

    for status in result.wp_statuses:
        icon = "[green]✓[/green]" if status.is_clean else "[red]✗[/red]"
        issue = status.error or ""
        table.add_row(status.wp_id, icon, issue)

    # Target branch status
    if result.target_diverged:
        table.add_row("Target", "[red]✗[/red]", result.target_divergence_msg or "Diverged")
    else:
        table.add_row("Target", "Up to date")

    console.print(table)

    if not result.passed:
        console.print("\n[bold red]Pre-flight failed.[/bold red] Fix these issues before merging:\n")
        for i, error in enumerate(result.errors, 1):
            console.print(f"  {i}. {error}")
        console.print()
    else:
        if result.warnings:
            console.print()
            for warning in result.warnings:
                console.print(f"[yellow]Warning:[/yellow] {warning}")
        console.print("\n[green]Pre-flight passed.[/green] Ready to merge.\n")


def x_display_preflight_result__mutmut_58(result: PreflightResult, console: Console) -> None:
    """Display pre-flight results with Rich formatting.

    Args:
        result: PreflightResult to display
        console: Rich Console instance for output
    """
    console.print("\n[bold]Pre-flight Check[/bold]\n")

    # WP status table
    table = Table(show_header=True, header_style="bold")
    table.add_column("WP")
    table.add_column("Status")
    table.add_column("Issue")

    for status in result.wp_statuses:
        icon = "[green]✓[/green]" if status.is_clean else "[red]✗[/red]"
        issue = status.error or ""
        table.add_row(status.wp_id, icon, issue)

    # Target branch status
    if result.target_diverged:
        table.add_row("Target", "[red]✗[/red]", result.target_divergence_msg or "Diverged")
    else:
        table.add_row("Target", "[green]✓[/green]", )

    console.print(table)

    if not result.passed:
        console.print("\n[bold red]Pre-flight failed.[/bold red] Fix these issues before merging:\n")
        for i, error in enumerate(result.errors, 1):
            console.print(f"  {i}. {error}")
        console.print()
    else:
        if result.warnings:
            console.print()
            for warning in result.warnings:
                console.print(f"[yellow]Warning:[/yellow] {warning}")
        console.print("\n[green]Pre-flight passed.[/green] Ready to merge.\n")


def x_display_preflight_result__mutmut_59(result: PreflightResult, console: Console) -> None:
    """Display pre-flight results with Rich formatting.

    Args:
        result: PreflightResult to display
        console: Rich Console instance for output
    """
    console.print("\n[bold]Pre-flight Check[/bold]\n")

    # WP status table
    table = Table(show_header=True, header_style="bold")
    table.add_column("WP")
    table.add_column("Status")
    table.add_column("Issue")

    for status in result.wp_statuses:
        icon = "[green]✓[/green]" if status.is_clean else "[red]✗[/red]"
        issue = status.error or ""
        table.add_row(status.wp_id, icon, issue)

    # Target branch status
    if result.target_diverged:
        table.add_row("Target", "[red]✗[/red]", result.target_divergence_msg or "Diverged")
    else:
        table.add_row("XXTargetXX", "[green]✓[/green]", "Up to date")

    console.print(table)

    if not result.passed:
        console.print("\n[bold red]Pre-flight failed.[/bold red] Fix these issues before merging:\n")
        for i, error in enumerate(result.errors, 1):
            console.print(f"  {i}. {error}")
        console.print()
    else:
        if result.warnings:
            console.print()
            for warning in result.warnings:
                console.print(f"[yellow]Warning:[/yellow] {warning}")
        console.print("\n[green]Pre-flight passed.[/green] Ready to merge.\n")


def x_display_preflight_result__mutmut_60(result: PreflightResult, console: Console) -> None:
    """Display pre-flight results with Rich formatting.

    Args:
        result: PreflightResult to display
        console: Rich Console instance for output
    """
    console.print("\n[bold]Pre-flight Check[/bold]\n")

    # WP status table
    table = Table(show_header=True, header_style="bold")
    table.add_column("WP")
    table.add_column("Status")
    table.add_column("Issue")

    for status in result.wp_statuses:
        icon = "[green]✓[/green]" if status.is_clean else "[red]✗[/red]"
        issue = status.error or ""
        table.add_row(status.wp_id, icon, issue)

    # Target branch status
    if result.target_diverged:
        table.add_row("Target", "[red]✗[/red]", result.target_divergence_msg or "Diverged")
    else:
        table.add_row("target", "[green]✓[/green]", "Up to date")

    console.print(table)

    if not result.passed:
        console.print("\n[bold red]Pre-flight failed.[/bold red] Fix these issues before merging:\n")
        for i, error in enumerate(result.errors, 1):
            console.print(f"  {i}. {error}")
        console.print()
    else:
        if result.warnings:
            console.print()
            for warning in result.warnings:
                console.print(f"[yellow]Warning:[/yellow] {warning}")
        console.print("\n[green]Pre-flight passed.[/green] Ready to merge.\n")


def x_display_preflight_result__mutmut_61(result: PreflightResult, console: Console) -> None:
    """Display pre-flight results with Rich formatting.

    Args:
        result: PreflightResult to display
        console: Rich Console instance for output
    """
    console.print("\n[bold]Pre-flight Check[/bold]\n")

    # WP status table
    table = Table(show_header=True, header_style="bold")
    table.add_column("WP")
    table.add_column("Status")
    table.add_column("Issue")

    for status in result.wp_statuses:
        icon = "[green]✓[/green]" if status.is_clean else "[red]✗[/red]"
        issue = status.error or ""
        table.add_row(status.wp_id, icon, issue)

    # Target branch status
    if result.target_diverged:
        table.add_row("Target", "[red]✗[/red]", result.target_divergence_msg or "Diverged")
    else:
        table.add_row("TARGET", "[green]✓[/green]", "Up to date")

    console.print(table)

    if not result.passed:
        console.print("\n[bold red]Pre-flight failed.[/bold red] Fix these issues before merging:\n")
        for i, error in enumerate(result.errors, 1):
            console.print(f"  {i}. {error}")
        console.print()
    else:
        if result.warnings:
            console.print()
            for warning in result.warnings:
                console.print(f"[yellow]Warning:[/yellow] {warning}")
        console.print("\n[green]Pre-flight passed.[/green] Ready to merge.\n")


def x_display_preflight_result__mutmut_62(result: PreflightResult, console: Console) -> None:
    """Display pre-flight results with Rich formatting.

    Args:
        result: PreflightResult to display
        console: Rich Console instance for output
    """
    console.print("\n[bold]Pre-flight Check[/bold]\n")

    # WP status table
    table = Table(show_header=True, header_style="bold")
    table.add_column("WP")
    table.add_column("Status")
    table.add_column("Issue")

    for status in result.wp_statuses:
        icon = "[green]✓[/green]" if status.is_clean else "[red]✗[/red]"
        issue = status.error or ""
        table.add_row(status.wp_id, icon, issue)

    # Target branch status
    if result.target_diverged:
        table.add_row("Target", "[red]✗[/red]", result.target_divergence_msg or "Diverged")
    else:
        table.add_row("Target", "XX[green]✓[/green]XX", "Up to date")

    console.print(table)

    if not result.passed:
        console.print("\n[bold red]Pre-flight failed.[/bold red] Fix these issues before merging:\n")
        for i, error in enumerate(result.errors, 1):
            console.print(f"  {i}. {error}")
        console.print()
    else:
        if result.warnings:
            console.print()
            for warning in result.warnings:
                console.print(f"[yellow]Warning:[/yellow] {warning}")
        console.print("\n[green]Pre-flight passed.[/green] Ready to merge.\n")


def x_display_preflight_result__mutmut_63(result: PreflightResult, console: Console) -> None:
    """Display pre-flight results with Rich formatting.

    Args:
        result: PreflightResult to display
        console: Rich Console instance for output
    """
    console.print("\n[bold]Pre-flight Check[/bold]\n")

    # WP status table
    table = Table(show_header=True, header_style="bold")
    table.add_column("WP")
    table.add_column("Status")
    table.add_column("Issue")

    for status in result.wp_statuses:
        icon = "[green]✓[/green]" if status.is_clean else "[red]✗[/red]"
        issue = status.error or ""
        table.add_row(status.wp_id, icon, issue)

    # Target branch status
    if result.target_diverged:
        table.add_row("Target", "[red]✗[/red]", result.target_divergence_msg or "Diverged")
    else:
        table.add_row("Target", "[GREEN]✓[/GREEN]", "Up to date")

    console.print(table)

    if not result.passed:
        console.print("\n[bold red]Pre-flight failed.[/bold red] Fix these issues before merging:\n")
        for i, error in enumerate(result.errors, 1):
            console.print(f"  {i}. {error}")
        console.print()
    else:
        if result.warnings:
            console.print()
            for warning in result.warnings:
                console.print(f"[yellow]Warning:[/yellow] {warning}")
        console.print("\n[green]Pre-flight passed.[/green] Ready to merge.\n")


def x_display_preflight_result__mutmut_64(result: PreflightResult, console: Console) -> None:
    """Display pre-flight results with Rich formatting.

    Args:
        result: PreflightResult to display
        console: Rich Console instance for output
    """
    console.print("\n[bold]Pre-flight Check[/bold]\n")

    # WP status table
    table = Table(show_header=True, header_style="bold")
    table.add_column("WP")
    table.add_column("Status")
    table.add_column("Issue")

    for status in result.wp_statuses:
        icon = "[green]✓[/green]" if status.is_clean else "[red]✗[/red]"
        issue = status.error or ""
        table.add_row(status.wp_id, icon, issue)

    # Target branch status
    if result.target_diverged:
        table.add_row("Target", "[red]✗[/red]", result.target_divergence_msg or "Diverged")
    else:
        table.add_row("Target", "[green]✓[/green]", "XXUp to dateXX")

    console.print(table)

    if not result.passed:
        console.print("\n[bold red]Pre-flight failed.[/bold red] Fix these issues before merging:\n")
        for i, error in enumerate(result.errors, 1):
            console.print(f"  {i}. {error}")
        console.print()
    else:
        if result.warnings:
            console.print()
            for warning in result.warnings:
                console.print(f"[yellow]Warning:[/yellow] {warning}")
        console.print("\n[green]Pre-flight passed.[/green] Ready to merge.\n")


def x_display_preflight_result__mutmut_65(result: PreflightResult, console: Console) -> None:
    """Display pre-flight results with Rich formatting.

    Args:
        result: PreflightResult to display
        console: Rich Console instance for output
    """
    console.print("\n[bold]Pre-flight Check[/bold]\n")

    # WP status table
    table = Table(show_header=True, header_style="bold")
    table.add_column("WP")
    table.add_column("Status")
    table.add_column("Issue")

    for status in result.wp_statuses:
        icon = "[green]✓[/green]" if status.is_clean else "[red]✗[/red]"
        issue = status.error or ""
        table.add_row(status.wp_id, icon, issue)

    # Target branch status
    if result.target_diverged:
        table.add_row("Target", "[red]✗[/red]", result.target_divergence_msg or "Diverged")
    else:
        table.add_row("Target", "[green]✓[/green]", "up to date")

    console.print(table)

    if not result.passed:
        console.print("\n[bold red]Pre-flight failed.[/bold red] Fix these issues before merging:\n")
        for i, error in enumerate(result.errors, 1):
            console.print(f"  {i}. {error}")
        console.print()
    else:
        if result.warnings:
            console.print()
            for warning in result.warnings:
                console.print(f"[yellow]Warning:[/yellow] {warning}")
        console.print("\n[green]Pre-flight passed.[/green] Ready to merge.\n")


def x_display_preflight_result__mutmut_66(result: PreflightResult, console: Console) -> None:
    """Display pre-flight results with Rich formatting.

    Args:
        result: PreflightResult to display
        console: Rich Console instance for output
    """
    console.print("\n[bold]Pre-flight Check[/bold]\n")

    # WP status table
    table = Table(show_header=True, header_style="bold")
    table.add_column("WP")
    table.add_column("Status")
    table.add_column("Issue")

    for status in result.wp_statuses:
        icon = "[green]✓[/green]" if status.is_clean else "[red]✗[/red]"
        issue = status.error or ""
        table.add_row(status.wp_id, icon, issue)

    # Target branch status
    if result.target_diverged:
        table.add_row("Target", "[red]✗[/red]", result.target_divergence_msg or "Diverged")
    else:
        table.add_row("Target", "[green]✓[/green]", "UP TO DATE")

    console.print(table)

    if not result.passed:
        console.print("\n[bold red]Pre-flight failed.[/bold red] Fix these issues before merging:\n")
        for i, error in enumerate(result.errors, 1):
            console.print(f"  {i}. {error}")
        console.print()
    else:
        if result.warnings:
            console.print()
            for warning in result.warnings:
                console.print(f"[yellow]Warning:[/yellow] {warning}")
        console.print("\n[green]Pre-flight passed.[/green] Ready to merge.\n")


def x_display_preflight_result__mutmut_67(result: PreflightResult, console: Console) -> None:
    """Display pre-flight results with Rich formatting.

    Args:
        result: PreflightResult to display
        console: Rich Console instance for output
    """
    console.print("\n[bold]Pre-flight Check[/bold]\n")

    # WP status table
    table = Table(show_header=True, header_style="bold")
    table.add_column("WP")
    table.add_column("Status")
    table.add_column("Issue")

    for status in result.wp_statuses:
        icon = "[green]✓[/green]" if status.is_clean else "[red]✗[/red]"
        issue = status.error or ""
        table.add_row(status.wp_id, icon, issue)

    # Target branch status
    if result.target_diverged:
        table.add_row("Target", "[red]✗[/red]", result.target_divergence_msg or "Diverged")
    else:
        table.add_row("Target", "[green]✓[/green]", "Up to date")

    console.print(None)

    if not result.passed:
        console.print("\n[bold red]Pre-flight failed.[/bold red] Fix these issues before merging:\n")
        for i, error in enumerate(result.errors, 1):
            console.print(f"  {i}. {error}")
        console.print()
    else:
        if result.warnings:
            console.print()
            for warning in result.warnings:
                console.print(f"[yellow]Warning:[/yellow] {warning}")
        console.print("\n[green]Pre-flight passed.[/green] Ready to merge.\n")


def x_display_preflight_result__mutmut_68(result: PreflightResult, console: Console) -> None:
    """Display pre-flight results with Rich formatting.

    Args:
        result: PreflightResult to display
        console: Rich Console instance for output
    """
    console.print("\n[bold]Pre-flight Check[/bold]\n")

    # WP status table
    table = Table(show_header=True, header_style="bold")
    table.add_column("WP")
    table.add_column("Status")
    table.add_column("Issue")

    for status in result.wp_statuses:
        icon = "[green]✓[/green]" if status.is_clean else "[red]✗[/red]"
        issue = status.error or ""
        table.add_row(status.wp_id, icon, issue)

    # Target branch status
    if result.target_diverged:
        table.add_row("Target", "[red]✗[/red]", result.target_divergence_msg or "Diverged")
    else:
        table.add_row("Target", "[green]✓[/green]", "Up to date")

    console.print(table)

    if result.passed:
        console.print("\n[bold red]Pre-flight failed.[/bold red] Fix these issues before merging:\n")
        for i, error in enumerate(result.errors, 1):
            console.print(f"  {i}. {error}")
        console.print()
    else:
        if result.warnings:
            console.print()
            for warning in result.warnings:
                console.print(f"[yellow]Warning:[/yellow] {warning}")
        console.print("\n[green]Pre-flight passed.[/green] Ready to merge.\n")


def x_display_preflight_result__mutmut_69(result: PreflightResult, console: Console) -> None:
    """Display pre-flight results with Rich formatting.

    Args:
        result: PreflightResult to display
        console: Rich Console instance for output
    """
    console.print("\n[bold]Pre-flight Check[/bold]\n")

    # WP status table
    table = Table(show_header=True, header_style="bold")
    table.add_column("WP")
    table.add_column("Status")
    table.add_column("Issue")

    for status in result.wp_statuses:
        icon = "[green]✓[/green]" if status.is_clean else "[red]✗[/red]"
        issue = status.error or ""
        table.add_row(status.wp_id, icon, issue)

    # Target branch status
    if result.target_diverged:
        table.add_row("Target", "[red]✗[/red]", result.target_divergence_msg or "Diverged")
    else:
        table.add_row("Target", "[green]✓[/green]", "Up to date")

    console.print(table)

    if not result.passed:
        console.print(None)
        for i, error in enumerate(result.errors, 1):
            console.print(f"  {i}. {error}")
        console.print()
    else:
        if result.warnings:
            console.print()
            for warning in result.warnings:
                console.print(f"[yellow]Warning:[/yellow] {warning}")
        console.print("\n[green]Pre-flight passed.[/green] Ready to merge.\n")


def x_display_preflight_result__mutmut_70(result: PreflightResult, console: Console) -> None:
    """Display pre-flight results with Rich formatting.

    Args:
        result: PreflightResult to display
        console: Rich Console instance for output
    """
    console.print("\n[bold]Pre-flight Check[/bold]\n")

    # WP status table
    table = Table(show_header=True, header_style="bold")
    table.add_column("WP")
    table.add_column("Status")
    table.add_column("Issue")

    for status in result.wp_statuses:
        icon = "[green]✓[/green]" if status.is_clean else "[red]✗[/red]"
        issue = status.error or ""
        table.add_row(status.wp_id, icon, issue)

    # Target branch status
    if result.target_diverged:
        table.add_row("Target", "[red]✗[/red]", result.target_divergence_msg or "Diverged")
    else:
        table.add_row("Target", "[green]✓[/green]", "Up to date")

    console.print(table)

    if not result.passed:
        console.print("XX\n[bold red]Pre-flight failed.[/bold red] Fix these issues before merging:\nXX")
        for i, error in enumerate(result.errors, 1):
            console.print(f"  {i}. {error}")
        console.print()
    else:
        if result.warnings:
            console.print()
            for warning in result.warnings:
                console.print(f"[yellow]Warning:[/yellow] {warning}")
        console.print("\n[green]Pre-flight passed.[/green] Ready to merge.\n")


def x_display_preflight_result__mutmut_71(result: PreflightResult, console: Console) -> None:
    """Display pre-flight results with Rich formatting.

    Args:
        result: PreflightResult to display
        console: Rich Console instance for output
    """
    console.print("\n[bold]Pre-flight Check[/bold]\n")

    # WP status table
    table = Table(show_header=True, header_style="bold")
    table.add_column("WP")
    table.add_column("Status")
    table.add_column("Issue")

    for status in result.wp_statuses:
        icon = "[green]✓[/green]" if status.is_clean else "[red]✗[/red]"
        issue = status.error or ""
        table.add_row(status.wp_id, icon, issue)

    # Target branch status
    if result.target_diverged:
        table.add_row("Target", "[red]✗[/red]", result.target_divergence_msg or "Diverged")
    else:
        table.add_row("Target", "[green]✓[/green]", "Up to date")

    console.print(table)

    if not result.passed:
        console.print("\n[bold red]pre-flight failed.[/bold red] fix these issues before merging:\n")
        for i, error in enumerate(result.errors, 1):
            console.print(f"  {i}. {error}")
        console.print()
    else:
        if result.warnings:
            console.print()
            for warning in result.warnings:
                console.print(f"[yellow]Warning:[/yellow] {warning}")
        console.print("\n[green]Pre-flight passed.[/green] Ready to merge.\n")


def x_display_preflight_result__mutmut_72(result: PreflightResult, console: Console) -> None:
    """Display pre-flight results with Rich formatting.

    Args:
        result: PreflightResult to display
        console: Rich Console instance for output
    """
    console.print("\n[bold]Pre-flight Check[/bold]\n")

    # WP status table
    table = Table(show_header=True, header_style="bold")
    table.add_column("WP")
    table.add_column("Status")
    table.add_column("Issue")

    for status in result.wp_statuses:
        icon = "[green]✓[/green]" if status.is_clean else "[red]✗[/red]"
        issue = status.error or ""
        table.add_row(status.wp_id, icon, issue)

    # Target branch status
    if result.target_diverged:
        table.add_row("Target", "[red]✗[/red]", result.target_divergence_msg or "Diverged")
    else:
        table.add_row("Target", "[green]✓[/green]", "Up to date")

    console.print(table)

    if not result.passed:
        console.print("\n[BOLD RED]PRE-FLIGHT FAILED.[/BOLD RED] FIX THESE ISSUES BEFORE MERGING:\n")
        for i, error in enumerate(result.errors, 1):
            console.print(f"  {i}. {error}")
        console.print()
    else:
        if result.warnings:
            console.print()
            for warning in result.warnings:
                console.print(f"[yellow]Warning:[/yellow] {warning}")
        console.print("\n[green]Pre-flight passed.[/green] Ready to merge.\n")


def x_display_preflight_result__mutmut_73(result: PreflightResult, console: Console) -> None:
    """Display pre-flight results with Rich formatting.

    Args:
        result: PreflightResult to display
        console: Rich Console instance for output
    """
    console.print("\n[bold]Pre-flight Check[/bold]\n")

    # WP status table
    table = Table(show_header=True, header_style="bold")
    table.add_column("WP")
    table.add_column("Status")
    table.add_column("Issue")

    for status in result.wp_statuses:
        icon = "[green]✓[/green]" if status.is_clean else "[red]✗[/red]"
        issue = status.error or ""
        table.add_row(status.wp_id, icon, issue)

    # Target branch status
    if result.target_diverged:
        table.add_row("Target", "[red]✗[/red]", result.target_divergence_msg or "Diverged")
    else:
        table.add_row("Target", "[green]✓[/green]", "Up to date")

    console.print(table)

    if not result.passed:
        console.print("\n[bold red]Pre-flight failed.[/bold red] Fix these issues before merging:\n")
        for i, error in enumerate(None, 1):
            console.print(f"  {i}. {error}")
        console.print()
    else:
        if result.warnings:
            console.print()
            for warning in result.warnings:
                console.print(f"[yellow]Warning:[/yellow] {warning}")
        console.print("\n[green]Pre-flight passed.[/green] Ready to merge.\n")


def x_display_preflight_result__mutmut_74(result: PreflightResult, console: Console) -> None:
    """Display pre-flight results with Rich formatting.

    Args:
        result: PreflightResult to display
        console: Rich Console instance for output
    """
    console.print("\n[bold]Pre-flight Check[/bold]\n")

    # WP status table
    table = Table(show_header=True, header_style="bold")
    table.add_column("WP")
    table.add_column("Status")
    table.add_column("Issue")

    for status in result.wp_statuses:
        icon = "[green]✓[/green]" if status.is_clean else "[red]✗[/red]"
        issue = status.error or ""
        table.add_row(status.wp_id, icon, issue)

    # Target branch status
    if result.target_diverged:
        table.add_row("Target", "[red]✗[/red]", result.target_divergence_msg or "Diverged")
    else:
        table.add_row("Target", "[green]✓[/green]", "Up to date")

    console.print(table)

    if not result.passed:
        console.print("\n[bold red]Pre-flight failed.[/bold red] Fix these issues before merging:\n")
        for i, error in enumerate(result.errors, None):
            console.print(f"  {i}. {error}")
        console.print()
    else:
        if result.warnings:
            console.print()
            for warning in result.warnings:
                console.print(f"[yellow]Warning:[/yellow] {warning}")
        console.print("\n[green]Pre-flight passed.[/green] Ready to merge.\n")


def x_display_preflight_result__mutmut_75(result: PreflightResult, console: Console) -> None:
    """Display pre-flight results with Rich formatting.

    Args:
        result: PreflightResult to display
        console: Rich Console instance for output
    """
    console.print("\n[bold]Pre-flight Check[/bold]\n")

    # WP status table
    table = Table(show_header=True, header_style="bold")
    table.add_column("WP")
    table.add_column("Status")
    table.add_column("Issue")

    for status in result.wp_statuses:
        icon = "[green]✓[/green]" if status.is_clean else "[red]✗[/red]"
        issue = status.error or ""
        table.add_row(status.wp_id, icon, issue)

    # Target branch status
    if result.target_diverged:
        table.add_row("Target", "[red]✗[/red]", result.target_divergence_msg or "Diverged")
    else:
        table.add_row("Target", "[green]✓[/green]", "Up to date")

    console.print(table)

    if not result.passed:
        console.print("\n[bold red]Pre-flight failed.[/bold red] Fix these issues before merging:\n")
        for i, error in enumerate(1):
            console.print(f"  {i}. {error}")
        console.print()
    else:
        if result.warnings:
            console.print()
            for warning in result.warnings:
                console.print(f"[yellow]Warning:[/yellow] {warning}")
        console.print("\n[green]Pre-flight passed.[/green] Ready to merge.\n")


def x_display_preflight_result__mutmut_76(result: PreflightResult, console: Console) -> None:
    """Display pre-flight results with Rich formatting.

    Args:
        result: PreflightResult to display
        console: Rich Console instance for output
    """
    console.print("\n[bold]Pre-flight Check[/bold]\n")

    # WP status table
    table = Table(show_header=True, header_style="bold")
    table.add_column("WP")
    table.add_column("Status")
    table.add_column("Issue")

    for status in result.wp_statuses:
        icon = "[green]✓[/green]" if status.is_clean else "[red]✗[/red]"
        issue = status.error or ""
        table.add_row(status.wp_id, icon, issue)

    # Target branch status
    if result.target_diverged:
        table.add_row("Target", "[red]✗[/red]", result.target_divergence_msg or "Diverged")
    else:
        table.add_row("Target", "[green]✓[/green]", "Up to date")

    console.print(table)

    if not result.passed:
        console.print("\n[bold red]Pre-flight failed.[/bold red] Fix these issues before merging:\n")
        for i, error in enumerate(result.errors, ):
            console.print(f"  {i}. {error}")
        console.print()
    else:
        if result.warnings:
            console.print()
            for warning in result.warnings:
                console.print(f"[yellow]Warning:[/yellow] {warning}")
        console.print("\n[green]Pre-flight passed.[/green] Ready to merge.\n")


def x_display_preflight_result__mutmut_77(result: PreflightResult, console: Console) -> None:
    """Display pre-flight results with Rich formatting.

    Args:
        result: PreflightResult to display
        console: Rich Console instance for output
    """
    console.print("\n[bold]Pre-flight Check[/bold]\n")

    # WP status table
    table = Table(show_header=True, header_style="bold")
    table.add_column("WP")
    table.add_column("Status")
    table.add_column("Issue")

    for status in result.wp_statuses:
        icon = "[green]✓[/green]" if status.is_clean else "[red]✗[/red]"
        issue = status.error or ""
        table.add_row(status.wp_id, icon, issue)

    # Target branch status
    if result.target_diverged:
        table.add_row("Target", "[red]✗[/red]", result.target_divergence_msg or "Diverged")
    else:
        table.add_row("Target", "[green]✓[/green]", "Up to date")

    console.print(table)

    if not result.passed:
        console.print("\n[bold red]Pre-flight failed.[/bold red] Fix these issues before merging:\n")
        for i, error in enumerate(result.errors, 2):
            console.print(f"  {i}. {error}")
        console.print()
    else:
        if result.warnings:
            console.print()
            for warning in result.warnings:
                console.print(f"[yellow]Warning:[/yellow] {warning}")
        console.print("\n[green]Pre-flight passed.[/green] Ready to merge.\n")


def x_display_preflight_result__mutmut_78(result: PreflightResult, console: Console) -> None:
    """Display pre-flight results with Rich formatting.

    Args:
        result: PreflightResult to display
        console: Rich Console instance for output
    """
    console.print("\n[bold]Pre-flight Check[/bold]\n")

    # WP status table
    table = Table(show_header=True, header_style="bold")
    table.add_column("WP")
    table.add_column("Status")
    table.add_column("Issue")

    for status in result.wp_statuses:
        icon = "[green]✓[/green]" if status.is_clean else "[red]✗[/red]"
        issue = status.error or ""
        table.add_row(status.wp_id, icon, issue)

    # Target branch status
    if result.target_diverged:
        table.add_row("Target", "[red]✗[/red]", result.target_divergence_msg or "Diverged")
    else:
        table.add_row("Target", "[green]✓[/green]", "Up to date")

    console.print(table)

    if not result.passed:
        console.print("\n[bold red]Pre-flight failed.[/bold red] Fix these issues before merging:\n")
        for i, error in enumerate(result.errors, 1):
            console.print(None)
        console.print()
    else:
        if result.warnings:
            console.print()
            for warning in result.warnings:
                console.print(f"[yellow]Warning:[/yellow] {warning}")
        console.print("\n[green]Pre-flight passed.[/green] Ready to merge.\n")


def x_display_preflight_result__mutmut_79(result: PreflightResult, console: Console) -> None:
    """Display pre-flight results with Rich formatting.

    Args:
        result: PreflightResult to display
        console: Rich Console instance for output
    """
    console.print("\n[bold]Pre-flight Check[/bold]\n")

    # WP status table
    table = Table(show_header=True, header_style="bold")
    table.add_column("WP")
    table.add_column("Status")
    table.add_column("Issue")

    for status in result.wp_statuses:
        icon = "[green]✓[/green]" if status.is_clean else "[red]✗[/red]"
        issue = status.error or ""
        table.add_row(status.wp_id, icon, issue)

    # Target branch status
    if result.target_diverged:
        table.add_row("Target", "[red]✗[/red]", result.target_divergence_msg or "Diverged")
    else:
        table.add_row("Target", "[green]✓[/green]", "Up to date")

    console.print(table)

    if not result.passed:
        console.print("\n[bold red]Pre-flight failed.[/bold red] Fix these issues before merging:\n")
        for i, error in enumerate(result.errors, 1):
            console.print(f"  {i}. {error}")
        console.print()
    else:
        if result.warnings:
            console.print()
            for warning in result.warnings:
                console.print(None)
        console.print("\n[green]Pre-flight passed.[/green] Ready to merge.\n")


def x_display_preflight_result__mutmut_80(result: PreflightResult, console: Console) -> None:
    """Display pre-flight results with Rich formatting.

    Args:
        result: PreflightResult to display
        console: Rich Console instance for output
    """
    console.print("\n[bold]Pre-flight Check[/bold]\n")

    # WP status table
    table = Table(show_header=True, header_style="bold")
    table.add_column("WP")
    table.add_column("Status")
    table.add_column("Issue")

    for status in result.wp_statuses:
        icon = "[green]✓[/green]" if status.is_clean else "[red]✗[/red]"
        issue = status.error or ""
        table.add_row(status.wp_id, icon, issue)

    # Target branch status
    if result.target_diverged:
        table.add_row("Target", "[red]✗[/red]", result.target_divergence_msg or "Diverged")
    else:
        table.add_row("Target", "[green]✓[/green]", "Up to date")

    console.print(table)

    if not result.passed:
        console.print("\n[bold red]Pre-flight failed.[/bold red] Fix these issues before merging:\n")
        for i, error in enumerate(result.errors, 1):
            console.print(f"  {i}. {error}")
        console.print()
    else:
        if result.warnings:
            console.print()
            for warning in result.warnings:
                console.print(f"[yellow]Warning:[/yellow] {warning}")
        console.print(None)


def x_display_preflight_result__mutmut_81(result: PreflightResult, console: Console) -> None:
    """Display pre-flight results with Rich formatting.

    Args:
        result: PreflightResult to display
        console: Rich Console instance for output
    """
    console.print("\n[bold]Pre-flight Check[/bold]\n")

    # WP status table
    table = Table(show_header=True, header_style="bold")
    table.add_column("WP")
    table.add_column("Status")
    table.add_column("Issue")

    for status in result.wp_statuses:
        icon = "[green]✓[/green]" if status.is_clean else "[red]✗[/red]"
        issue = status.error or ""
        table.add_row(status.wp_id, icon, issue)

    # Target branch status
    if result.target_diverged:
        table.add_row("Target", "[red]✗[/red]", result.target_divergence_msg or "Diverged")
    else:
        table.add_row("Target", "[green]✓[/green]", "Up to date")

    console.print(table)

    if not result.passed:
        console.print("\n[bold red]Pre-flight failed.[/bold red] Fix these issues before merging:\n")
        for i, error in enumerate(result.errors, 1):
            console.print(f"  {i}. {error}")
        console.print()
    else:
        if result.warnings:
            console.print()
            for warning in result.warnings:
                console.print(f"[yellow]Warning:[/yellow] {warning}")
        console.print("XX\n[green]Pre-flight passed.[/green] Ready to merge.\nXX")


def x_display_preflight_result__mutmut_82(result: PreflightResult, console: Console) -> None:
    """Display pre-flight results with Rich formatting.

    Args:
        result: PreflightResult to display
        console: Rich Console instance for output
    """
    console.print("\n[bold]Pre-flight Check[/bold]\n")

    # WP status table
    table = Table(show_header=True, header_style="bold")
    table.add_column("WP")
    table.add_column("Status")
    table.add_column("Issue")

    for status in result.wp_statuses:
        icon = "[green]✓[/green]" if status.is_clean else "[red]✗[/red]"
        issue = status.error or ""
        table.add_row(status.wp_id, icon, issue)

    # Target branch status
    if result.target_diverged:
        table.add_row("Target", "[red]✗[/red]", result.target_divergence_msg or "Diverged")
    else:
        table.add_row("Target", "[green]✓[/green]", "Up to date")

    console.print(table)

    if not result.passed:
        console.print("\n[bold red]Pre-flight failed.[/bold red] Fix these issues before merging:\n")
        for i, error in enumerate(result.errors, 1):
            console.print(f"  {i}. {error}")
        console.print()
    else:
        if result.warnings:
            console.print()
            for warning in result.warnings:
                console.print(f"[yellow]Warning:[/yellow] {warning}")
        console.print("\n[green]pre-flight passed.[/green] ready to merge.\n")


def x_display_preflight_result__mutmut_83(result: PreflightResult, console: Console) -> None:
    """Display pre-flight results with Rich formatting.

    Args:
        result: PreflightResult to display
        console: Rich Console instance for output
    """
    console.print("\n[bold]Pre-flight Check[/bold]\n")

    # WP status table
    table = Table(show_header=True, header_style="bold")
    table.add_column("WP")
    table.add_column("Status")
    table.add_column("Issue")

    for status in result.wp_statuses:
        icon = "[green]✓[/green]" if status.is_clean else "[red]✗[/red]"
        issue = status.error or ""
        table.add_row(status.wp_id, icon, issue)

    # Target branch status
    if result.target_diverged:
        table.add_row("Target", "[red]✗[/red]", result.target_divergence_msg or "Diverged")
    else:
        table.add_row("Target", "[green]✓[/green]", "Up to date")

    console.print(table)

    if not result.passed:
        console.print("\n[bold red]Pre-flight failed.[/bold red] Fix these issues before merging:\n")
        for i, error in enumerate(result.errors, 1):
            console.print(f"  {i}. {error}")
        console.print()
    else:
        if result.warnings:
            console.print()
            for warning in result.warnings:
                console.print(f"[yellow]Warning:[/yellow] {warning}")
        console.print("\n[GREEN]PRE-FLIGHT PASSED.[/GREEN] READY TO MERGE.\n")

x_display_preflight_result__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_display_preflight_result__mutmut_1': x_display_preflight_result__mutmut_1, 
    'x_display_preflight_result__mutmut_2': x_display_preflight_result__mutmut_2, 
    'x_display_preflight_result__mutmut_3': x_display_preflight_result__mutmut_3, 
    'x_display_preflight_result__mutmut_4': x_display_preflight_result__mutmut_4, 
    'x_display_preflight_result__mutmut_5': x_display_preflight_result__mutmut_5, 
    'x_display_preflight_result__mutmut_6': x_display_preflight_result__mutmut_6, 
    'x_display_preflight_result__mutmut_7': x_display_preflight_result__mutmut_7, 
    'x_display_preflight_result__mutmut_8': x_display_preflight_result__mutmut_8, 
    'x_display_preflight_result__mutmut_9': x_display_preflight_result__mutmut_9, 
    'x_display_preflight_result__mutmut_10': x_display_preflight_result__mutmut_10, 
    'x_display_preflight_result__mutmut_11': x_display_preflight_result__mutmut_11, 
    'x_display_preflight_result__mutmut_12': x_display_preflight_result__mutmut_12, 
    'x_display_preflight_result__mutmut_13': x_display_preflight_result__mutmut_13, 
    'x_display_preflight_result__mutmut_14': x_display_preflight_result__mutmut_14, 
    'x_display_preflight_result__mutmut_15': x_display_preflight_result__mutmut_15, 
    'x_display_preflight_result__mutmut_16': x_display_preflight_result__mutmut_16, 
    'x_display_preflight_result__mutmut_17': x_display_preflight_result__mutmut_17, 
    'x_display_preflight_result__mutmut_18': x_display_preflight_result__mutmut_18, 
    'x_display_preflight_result__mutmut_19': x_display_preflight_result__mutmut_19, 
    'x_display_preflight_result__mutmut_20': x_display_preflight_result__mutmut_20, 
    'x_display_preflight_result__mutmut_21': x_display_preflight_result__mutmut_21, 
    'x_display_preflight_result__mutmut_22': x_display_preflight_result__mutmut_22, 
    'x_display_preflight_result__mutmut_23': x_display_preflight_result__mutmut_23, 
    'x_display_preflight_result__mutmut_24': x_display_preflight_result__mutmut_24, 
    'x_display_preflight_result__mutmut_25': x_display_preflight_result__mutmut_25, 
    'x_display_preflight_result__mutmut_26': x_display_preflight_result__mutmut_26, 
    'x_display_preflight_result__mutmut_27': x_display_preflight_result__mutmut_27, 
    'x_display_preflight_result__mutmut_28': x_display_preflight_result__mutmut_28, 
    'x_display_preflight_result__mutmut_29': x_display_preflight_result__mutmut_29, 
    'x_display_preflight_result__mutmut_30': x_display_preflight_result__mutmut_30, 
    'x_display_preflight_result__mutmut_31': x_display_preflight_result__mutmut_31, 
    'x_display_preflight_result__mutmut_32': x_display_preflight_result__mutmut_32, 
    'x_display_preflight_result__mutmut_33': x_display_preflight_result__mutmut_33, 
    'x_display_preflight_result__mutmut_34': x_display_preflight_result__mutmut_34, 
    'x_display_preflight_result__mutmut_35': x_display_preflight_result__mutmut_35, 
    'x_display_preflight_result__mutmut_36': x_display_preflight_result__mutmut_36, 
    'x_display_preflight_result__mutmut_37': x_display_preflight_result__mutmut_37, 
    'x_display_preflight_result__mutmut_38': x_display_preflight_result__mutmut_38, 
    'x_display_preflight_result__mutmut_39': x_display_preflight_result__mutmut_39, 
    'x_display_preflight_result__mutmut_40': x_display_preflight_result__mutmut_40, 
    'x_display_preflight_result__mutmut_41': x_display_preflight_result__mutmut_41, 
    'x_display_preflight_result__mutmut_42': x_display_preflight_result__mutmut_42, 
    'x_display_preflight_result__mutmut_43': x_display_preflight_result__mutmut_43, 
    'x_display_preflight_result__mutmut_44': x_display_preflight_result__mutmut_44, 
    'x_display_preflight_result__mutmut_45': x_display_preflight_result__mutmut_45, 
    'x_display_preflight_result__mutmut_46': x_display_preflight_result__mutmut_46, 
    'x_display_preflight_result__mutmut_47': x_display_preflight_result__mutmut_47, 
    'x_display_preflight_result__mutmut_48': x_display_preflight_result__mutmut_48, 
    'x_display_preflight_result__mutmut_49': x_display_preflight_result__mutmut_49, 
    'x_display_preflight_result__mutmut_50': x_display_preflight_result__mutmut_50, 
    'x_display_preflight_result__mutmut_51': x_display_preflight_result__mutmut_51, 
    'x_display_preflight_result__mutmut_52': x_display_preflight_result__mutmut_52, 
    'x_display_preflight_result__mutmut_53': x_display_preflight_result__mutmut_53, 
    'x_display_preflight_result__mutmut_54': x_display_preflight_result__mutmut_54, 
    'x_display_preflight_result__mutmut_55': x_display_preflight_result__mutmut_55, 
    'x_display_preflight_result__mutmut_56': x_display_preflight_result__mutmut_56, 
    'x_display_preflight_result__mutmut_57': x_display_preflight_result__mutmut_57, 
    'x_display_preflight_result__mutmut_58': x_display_preflight_result__mutmut_58, 
    'x_display_preflight_result__mutmut_59': x_display_preflight_result__mutmut_59, 
    'x_display_preflight_result__mutmut_60': x_display_preflight_result__mutmut_60, 
    'x_display_preflight_result__mutmut_61': x_display_preflight_result__mutmut_61, 
    'x_display_preflight_result__mutmut_62': x_display_preflight_result__mutmut_62, 
    'x_display_preflight_result__mutmut_63': x_display_preflight_result__mutmut_63, 
    'x_display_preflight_result__mutmut_64': x_display_preflight_result__mutmut_64, 
    'x_display_preflight_result__mutmut_65': x_display_preflight_result__mutmut_65, 
    'x_display_preflight_result__mutmut_66': x_display_preflight_result__mutmut_66, 
    'x_display_preflight_result__mutmut_67': x_display_preflight_result__mutmut_67, 
    'x_display_preflight_result__mutmut_68': x_display_preflight_result__mutmut_68, 
    'x_display_preflight_result__mutmut_69': x_display_preflight_result__mutmut_69, 
    'x_display_preflight_result__mutmut_70': x_display_preflight_result__mutmut_70, 
    'x_display_preflight_result__mutmut_71': x_display_preflight_result__mutmut_71, 
    'x_display_preflight_result__mutmut_72': x_display_preflight_result__mutmut_72, 
    'x_display_preflight_result__mutmut_73': x_display_preflight_result__mutmut_73, 
    'x_display_preflight_result__mutmut_74': x_display_preflight_result__mutmut_74, 
    'x_display_preflight_result__mutmut_75': x_display_preflight_result__mutmut_75, 
    'x_display_preflight_result__mutmut_76': x_display_preflight_result__mutmut_76, 
    'x_display_preflight_result__mutmut_77': x_display_preflight_result__mutmut_77, 
    'x_display_preflight_result__mutmut_78': x_display_preflight_result__mutmut_78, 
    'x_display_preflight_result__mutmut_79': x_display_preflight_result__mutmut_79, 
    'x_display_preflight_result__mutmut_80': x_display_preflight_result__mutmut_80, 
    'x_display_preflight_result__mutmut_81': x_display_preflight_result__mutmut_81, 
    'x_display_preflight_result__mutmut_82': x_display_preflight_result__mutmut_82, 
    'x_display_preflight_result__mutmut_83': x_display_preflight_result__mutmut_83
}
x_display_preflight_result__mutmut_orig.__name__ = 'x_display_preflight_result'
