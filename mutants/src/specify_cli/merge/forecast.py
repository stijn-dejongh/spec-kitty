"""Conflict prediction for merge dry-run.

Implements FR-005 through FR-007: predicting which files will conflict
during merge and identifying auto-resolvable status files.
"""

from __future__ import annotations

import fnmatch
import subprocess
from dataclasses import dataclass
from pathlib import Path

from rich.console import Console
from rich.table import Table

__all__ = [
    "ConflictPrediction",
    "predict_conflicts",
    "is_status_file",
    "build_file_wp_mapping",
    "display_conflict_forecast",
]


# Patterns for status files that can be auto-resolved
STATUS_FILE_PATTERNS = [
    "kitty-specs/*/tasks/*.md",  # WP files: kitty-specs/017-feature/tasks/WP01.md
    "kitty-specs/*/tasks.md",  # Main tasks: kitty-specs/017-feature/tasks.md
    "kitty-specs/*/*/tasks/*.md",  # Nested: kitty-specs/features/017/tasks/WP01.md
    "kitty-specs/*/*/tasks.md",  # Nested main
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
class ConflictPrediction:
    """Predicted conflict for a file.

    Attributes:
        file_path: Path to the file that may conflict
        conflicting_wps: List of WP IDs that modify this file
        is_status_file: True if file matches status file pattern
        confidence: Prediction confidence ("certain", "likely", "possible")
    """

    file_path: str
    conflicting_wps: list[str]
    is_status_file: bool
    confidence: str  # "certain", "likely", "possible"

    @property
    def auto_resolvable(self) -> bool:
        """Status files can be auto-resolved."""
        return self.is_status_file


def is_status_file(file_path: str) -> bool:
    args = [file_path]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_is_status_file__mutmut_orig, x_is_status_file__mutmut_mutants, args, kwargs, None)


def x_is_status_file__mutmut_orig(file_path: str) -> bool:
    """Check if file matches status file patterns.

    Status files contain lane/checkbox/history that can be auto-resolved
    during merge because their content is procedurally generated.

    Args:
        file_path: Path to check (relative to repo root)

    Returns:
        True if file matches a status file pattern
    """
    for pattern in STATUS_FILE_PATTERNS:
        if fnmatch.fnmatch(file_path, pattern):
            return True
    return False


def x_is_status_file__mutmut_1(file_path: str) -> bool:
    """Check if file matches status file patterns.

    Status files contain lane/checkbox/history that can be auto-resolved
    during merge because their content is procedurally generated.

    Args:
        file_path: Path to check (relative to repo root)

    Returns:
        True if file matches a status file pattern
    """
    for pattern in STATUS_FILE_PATTERNS:
        if fnmatch.fnmatch(None, pattern):
            return True
    return False


def x_is_status_file__mutmut_2(file_path: str) -> bool:
    """Check if file matches status file patterns.

    Status files contain lane/checkbox/history that can be auto-resolved
    during merge because their content is procedurally generated.

    Args:
        file_path: Path to check (relative to repo root)

    Returns:
        True if file matches a status file pattern
    """
    for pattern in STATUS_FILE_PATTERNS:
        if fnmatch.fnmatch(file_path, None):
            return True
    return False


def x_is_status_file__mutmut_3(file_path: str) -> bool:
    """Check if file matches status file patterns.

    Status files contain lane/checkbox/history that can be auto-resolved
    during merge because their content is procedurally generated.

    Args:
        file_path: Path to check (relative to repo root)

    Returns:
        True if file matches a status file pattern
    """
    for pattern in STATUS_FILE_PATTERNS:
        if fnmatch.fnmatch(pattern):
            return True
    return False


def x_is_status_file__mutmut_4(file_path: str) -> bool:
    """Check if file matches status file patterns.

    Status files contain lane/checkbox/history that can be auto-resolved
    during merge because their content is procedurally generated.

    Args:
        file_path: Path to check (relative to repo root)

    Returns:
        True if file matches a status file pattern
    """
    for pattern in STATUS_FILE_PATTERNS:
        if fnmatch.fnmatch(file_path, ):
            return True
    return False


def x_is_status_file__mutmut_5(file_path: str) -> bool:
    """Check if file matches status file patterns.

    Status files contain lane/checkbox/history that can be auto-resolved
    during merge because their content is procedurally generated.

    Args:
        file_path: Path to check (relative to repo root)

    Returns:
        True if file matches a status file pattern
    """
    for pattern in STATUS_FILE_PATTERNS:
        if fnmatch.fnmatch(file_path, pattern):
            return False
    return False


def x_is_status_file__mutmut_6(file_path: str) -> bool:
    """Check if file matches status file patterns.

    Status files contain lane/checkbox/history that can be auto-resolved
    during merge because their content is procedurally generated.

    Args:
        file_path: Path to check (relative to repo root)

    Returns:
        True if file matches a status file pattern
    """
    for pattern in STATUS_FILE_PATTERNS:
        if fnmatch.fnmatch(file_path, pattern):
            return True
    return True

x_is_status_file__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_is_status_file__mutmut_1': x_is_status_file__mutmut_1, 
    'x_is_status_file__mutmut_2': x_is_status_file__mutmut_2, 
    'x_is_status_file__mutmut_3': x_is_status_file__mutmut_3, 
    'x_is_status_file__mutmut_4': x_is_status_file__mutmut_4, 
    'x_is_status_file__mutmut_5': x_is_status_file__mutmut_5, 
    'x_is_status_file__mutmut_6': x_is_status_file__mutmut_6
}
x_is_status_file__mutmut_orig.__name__ = 'x_is_status_file'


def build_file_wp_mapping(
    wp_workspaces: list[tuple[Path, str, str]],
    target_branch: str,
    repo_root: Path,
) -> dict[str, list[str]]:
    args = [wp_workspaces, target_branch, repo_root]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_build_file_wp_mapping__mutmut_orig, x_build_file_wp_mapping__mutmut_mutants, args, kwargs, None)


def x_build_file_wp_mapping__mutmut_orig(
    wp_workspaces: list[tuple[Path, str, str]],
    target_branch: str,
    repo_root: Path,
) -> dict[str, list[str]]:
    """Build mapping of file paths to WPs that modify them.

    Uses git diff to identify which files each WP branch modifies
    relative to the target branch.

    Args:
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples
        target_branch: Branch being merged into (e.g., "main")
        repo_root: Repository root for running git commands

    Returns:
        Dict mapping file_path → [wp_ids that modify it]
    """
    file_to_wps: dict[str, list[str]] = {}

    for _, wp_id, branch_name in wp_workspaces:
        try:
            result = subprocess.run(
                ["git", "diff", "--name-only", f"{target_branch}...{branch_name}"],
                cwd=str(repo_root),
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )

            if result.returncode == 0:
                for line in result.stdout.strip().split("\n"):
                    if line:
                        if line not in file_to_wps:
                            file_to_wps[line] = []
                        file_to_wps[line].append(wp_id)
        except Exception:
            continue  # Skip this WP if diff fails

    return file_to_wps


def x_build_file_wp_mapping__mutmut_1(
    wp_workspaces: list[tuple[Path, str, str]],
    target_branch: str,
    repo_root: Path,
) -> dict[str, list[str]]:
    """Build mapping of file paths to WPs that modify them.

    Uses git diff to identify which files each WP branch modifies
    relative to the target branch.

    Args:
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples
        target_branch: Branch being merged into (e.g., "main")
        repo_root: Repository root for running git commands

    Returns:
        Dict mapping file_path → [wp_ids that modify it]
    """
    file_to_wps: dict[str, list[str]] = None

    for _, wp_id, branch_name in wp_workspaces:
        try:
            result = subprocess.run(
                ["git", "diff", "--name-only", f"{target_branch}...{branch_name}"],
                cwd=str(repo_root),
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )

            if result.returncode == 0:
                for line in result.stdout.strip().split("\n"):
                    if line:
                        if line not in file_to_wps:
                            file_to_wps[line] = []
                        file_to_wps[line].append(wp_id)
        except Exception:
            continue  # Skip this WP if diff fails

    return file_to_wps


def x_build_file_wp_mapping__mutmut_2(
    wp_workspaces: list[tuple[Path, str, str]],
    target_branch: str,
    repo_root: Path,
) -> dict[str, list[str]]:
    """Build mapping of file paths to WPs that modify them.

    Uses git diff to identify which files each WP branch modifies
    relative to the target branch.

    Args:
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples
        target_branch: Branch being merged into (e.g., "main")
        repo_root: Repository root for running git commands

    Returns:
        Dict mapping file_path → [wp_ids that modify it]
    """
    file_to_wps: dict[str, list[str]] = {}

    for _, wp_id, branch_name in wp_workspaces:
        try:
            result = None

            if result.returncode == 0:
                for line in result.stdout.strip().split("\n"):
                    if line:
                        if line not in file_to_wps:
                            file_to_wps[line] = []
                        file_to_wps[line].append(wp_id)
        except Exception:
            continue  # Skip this WP if diff fails

    return file_to_wps


def x_build_file_wp_mapping__mutmut_3(
    wp_workspaces: list[tuple[Path, str, str]],
    target_branch: str,
    repo_root: Path,
) -> dict[str, list[str]]:
    """Build mapping of file paths to WPs that modify them.

    Uses git diff to identify which files each WP branch modifies
    relative to the target branch.

    Args:
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples
        target_branch: Branch being merged into (e.g., "main")
        repo_root: Repository root for running git commands

    Returns:
        Dict mapping file_path → [wp_ids that modify it]
    """
    file_to_wps: dict[str, list[str]] = {}

    for _, wp_id, branch_name in wp_workspaces:
        try:
            result = subprocess.run(
                None,
                cwd=str(repo_root),
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )

            if result.returncode == 0:
                for line in result.stdout.strip().split("\n"):
                    if line:
                        if line not in file_to_wps:
                            file_to_wps[line] = []
                        file_to_wps[line].append(wp_id)
        except Exception:
            continue  # Skip this WP if diff fails

    return file_to_wps


def x_build_file_wp_mapping__mutmut_4(
    wp_workspaces: list[tuple[Path, str, str]],
    target_branch: str,
    repo_root: Path,
) -> dict[str, list[str]]:
    """Build mapping of file paths to WPs that modify them.

    Uses git diff to identify which files each WP branch modifies
    relative to the target branch.

    Args:
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples
        target_branch: Branch being merged into (e.g., "main")
        repo_root: Repository root for running git commands

    Returns:
        Dict mapping file_path → [wp_ids that modify it]
    """
    file_to_wps: dict[str, list[str]] = {}

    for _, wp_id, branch_name in wp_workspaces:
        try:
            result = subprocess.run(
                ["git", "diff", "--name-only", f"{target_branch}...{branch_name}"],
                cwd=None,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )

            if result.returncode == 0:
                for line in result.stdout.strip().split("\n"):
                    if line:
                        if line not in file_to_wps:
                            file_to_wps[line] = []
                        file_to_wps[line].append(wp_id)
        except Exception:
            continue  # Skip this WP if diff fails

    return file_to_wps


def x_build_file_wp_mapping__mutmut_5(
    wp_workspaces: list[tuple[Path, str, str]],
    target_branch: str,
    repo_root: Path,
) -> dict[str, list[str]]:
    """Build mapping of file paths to WPs that modify them.

    Uses git diff to identify which files each WP branch modifies
    relative to the target branch.

    Args:
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples
        target_branch: Branch being merged into (e.g., "main")
        repo_root: Repository root for running git commands

    Returns:
        Dict mapping file_path → [wp_ids that modify it]
    """
    file_to_wps: dict[str, list[str]] = {}

    for _, wp_id, branch_name in wp_workspaces:
        try:
            result = subprocess.run(
                ["git", "diff", "--name-only", f"{target_branch}...{branch_name}"],
                cwd=str(repo_root),
                capture_output=None,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )

            if result.returncode == 0:
                for line in result.stdout.strip().split("\n"):
                    if line:
                        if line not in file_to_wps:
                            file_to_wps[line] = []
                        file_to_wps[line].append(wp_id)
        except Exception:
            continue  # Skip this WP if diff fails

    return file_to_wps


def x_build_file_wp_mapping__mutmut_6(
    wp_workspaces: list[tuple[Path, str, str]],
    target_branch: str,
    repo_root: Path,
) -> dict[str, list[str]]:
    """Build mapping of file paths to WPs that modify them.

    Uses git diff to identify which files each WP branch modifies
    relative to the target branch.

    Args:
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples
        target_branch: Branch being merged into (e.g., "main")
        repo_root: Repository root for running git commands

    Returns:
        Dict mapping file_path → [wp_ids that modify it]
    """
    file_to_wps: dict[str, list[str]] = {}

    for _, wp_id, branch_name in wp_workspaces:
        try:
            result = subprocess.run(
                ["git", "diff", "--name-only", f"{target_branch}...{branch_name}"],
                cwd=str(repo_root),
                capture_output=True,
                text=None,
                encoding="utf-8",
                errors="replace",
                check=False,
            )

            if result.returncode == 0:
                for line in result.stdout.strip().split("\n"):
                    if line:
                        if line not in file_to_wps:
                            file_to_wps[line] = []
                        file_to_wps[line].append(wp_id)
        except Exception:
            continue  # Skip this WP if diff fails

    return file_to_wps


def x_build_file_wp_mapping__mutmut_7(
    wp_workspaces: list[tuple[Path, str, str]],
    target_branch: str,
    repo_root: Path,
) -> dict[str, list[str]]:
    """Build mapping of file paths to WPs that modify them.

    Uses git diff to identify which files each WP branch modifies
    relative to the target branch.

    Args:
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples
        target_branch: Branch being merged into (e.g., "main")
        repo_root: Repository root for running git commands

    Returns:
        Dict mapping file_path → [wp_ids that modify it]
    """
    file_to_wps: dict[str, list[str]] = {}

    for _, wp_id, branch_name in wp_workspaces:
        try:
            result = subprocess.run(
                ["git", "diff", "--name-only", f"{target_branch}...{branch_name}"],
                cwd=str(repo_root),
                capture_output=True,
                text=True,
                encoding=None,
                errors="replace",
                check=False,
            )

            if result.returncode == 0:
                for line in result.stdout.strip().split("\n"):
                    if line:
                        if line not in file_to_wps:
                            file_to_wps[line] = []
                        file_to_wps[line].append(wp_id)
        except Exception:
            continue  # Skip this WP if diff fails

    return file_to_wps


def x_build_file_wp_mapping__mutmut_8(
    wp_workspaces: list[tuple[Path, str, str]],
    target_branch: str,
    repo_root: Path,
) -> dict[str, list[str]]:
    """Build mapping of file paths to WPs that modify them.

    Uses git diff to identify which files each WP branch modifies
    relative to the target branch.

    Args:
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples
        target_branch: Branch being merged into (e.g., "main")
        repo_root: Repository root for running git commands

    Returns:
        Dict mapping file_path → [wp_ids that modify it]
    """
    file_to_wps: dict[str, list[str]] = {}

    for _, wp_id, branch_name in wp_workspaces:
        try:
            result = subprocess.run(
                ["git", "diff", "--name-only", f"{target_branch}...{branch_name}"],
                cwd=str(repo_root),
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors=None,
                check=False,
            )

            if result.returncode == 0:
                for line in result.stdout.strip().split("\n"):
                    if line:
                        if line not in file_to_wps:
                            file_to_wps[line] = []
                        file_to_wps[line].append(wp_id)
        except Exception:
            continue  # Skip this WP if diff fails

    return file_to_wps


def x_build_file_wp_mapping__mutmut_9(
    wp_workspaces: list[tuple[Path, str, str]],
    target_branch: str,
    repo_root: Path,
) -> dict[str, list[str]]:
    """Build mapping of file paths to WPs that modify them.

    Uses git diff to identify which files each WP branch modifies
    relative to the target branch.

    Args:
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples
        target_branch: Branch being merged into (e.g., "main")
        repo_root: Repository root for running git commands

    Returns:
        Dict mapping file_path → [wp_ids that modify it]
    """
    file_to_wps: dict[str, list[str]] = {}

    for _, wp_id, branch_name in wp_workspaces:
        try:
            result = subprocess.run(
                ["git", "diff", "--name-only", f"{target_branch}...{branch_name}"],
                cwd=str(repo_root),
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=None,
            )

            if result.returncode == 0:
                for line in result.stdout.strip().split("\n"):
                    if line:
                        if line not in file_to_wps:
                            file_to_wps[line] = []
                        file_to_wps[line].append(wp_id)
        except Exception:
            continue  # Skip this WP if diff fails

    return file_to_wps


def x_build_file_wp_mapping__mutmut_10(
    wp_workspaces: list[tuple[Path, str, str]],
    target_branch: str,
    repo_root: Path,
) -> dict[str, list[str]]:
    """Build mapping of file paths to WPs that modify them.

    Uses git diff to identify which files each WP branch modifies
    relative to the target branch.

    Args:
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples
        target_branch: Branch being merged into (e.g., "main")
        repo_root: Repository root for running git commands

    Returns:
        Dict mapping file_path → [wp_ids that modify it]
    """
    file_to_wps: dict[str, list[str]] = {}

    for _, wp_id, branch_name in wp_workspaces:
        try:
            result = subprocess.run(
                cwd=str(repo_root),
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )

            if result.returncode == 0:
                for line in result.stdout.strip().split("\n"):
                    if line:
                        if line not in file_to_wps:
                            file_to_wps[line] = []
                        file_to_wps[line].append(wp_id)
        except Exception:
            continue  # Skip this WP if diff fails

    return file_to_wps


def x_build_file_wp_mapping__mutmut_11(
    wp_workspaces: list[tuple[Path, str, str]],
    target_branch: str,
    repo_root: Path,
) -> dict[str, list[str]]:
    """Build mapping of file paths to WPs that modify them.

    Uses git diff to identify which files each WP branch modifies
    relative to the target branch.

    Args:
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples
        target_branch: Branch being merged into (e.g., "main")
        repo_root: Repository root for running git commands

    Returns:
        Dict mapping file_path → [wp_ids that modify it]
    """
    file_to_wps: dict[str, list[str]] = {}

    for _, wp_id, branch_name in wp_workspaces:
        try:
            result = subprocess.run(
                ["git", "diff", "--name-only", f"{target_branch}...{branch_name}"],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )

            if result.returncode == 0:
                for line in result.stdout.strip().split("\n"):
                    if line:
                        if line not in file_to_wps:
                            file_to_wps[line] = []
                        file_to_wps[line].append(wp_id)
        except Exception:
            continue  # Skip this WP if diff fails

    return file_to_wps


def x_build_file_wp_mapping__mutmut_12(
    wp_workspaces: list[tuple[Path, str, str]],
    target_branch: str,
    repo_root: Path,
) -> dict[str, list[str]]:
    """Build mapping of file paths to WPs that modify them.

    Uses git diff to identify which files each WP branch modifies
    relative to the target branch.

    Args:
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples
        target_branch: Branch being merged into (e.g., "main")
        repo_root: Repository root for running git commands

    Returns:
        Dict mapping file_path → [wp_ids that modify it]
    """
    file_to_wps: dict[str, list[str]] = {}

    for _, wp_id, branch_name in wp_workspaces:
        try:
            result = subprocess.run(
                ["git", "diff", "--name-only", f"{target_branch}...{branch_name}"],
                cwd=str(repo_root),
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )

            if result.returncode == 0:
                for line in result.stdout.strip().split("\n"):
                    if line:
                        if line not in file_to_wps:
                            file_to_wps[line] = []
                        file_to_wps[line].append(wp_id)
        except Exception:
            continue  # Skip this WP if diff fails

    return file_to_wps


def x_build_file_wp_mapping__mutmut_13(
    wp_workspaces: list[tuple[Path, str, str]],
    target_branch: str,
    repo_root: Path,
) -> dict[str, list[str]]:
    """Build mapping of file paths to WPs that modify them.

    Uses git diff to identify which files each WP branch modifies
    relative to the target branch.

    Args:
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples
        target_branch: Branch being merged into (e.g., "main")
        repo_root: Repository root for running git commands

    Returns:
        Dict mapping file_path → [wp_ids that modify it]
    """
    file_to_wps: dict[str, list[str]] = {}

    for _, wp_id, branch_name in wp_workspaces:
        try:
            result = subprocess.run(
                ["git", "diff", "--name-only", f"{target_branch}...{branch_name}"],
                cwd=str(repo_root),
                capture_output=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )

            if result.returncode == 0:
                for line in result.stdout.strip().split("\n"):
                    if line:
                        if line not in file_to_wps:
                            file_to_wps[line] = []
                        file_to_wps[line].append(wp_id)
        except Exception:
            continue  # Skip this WP if diff fails

    return file_to_wps


def x_build_file_wp_mapping__mutmut_14(
    wp_workspaces: list[tuple[Path, str, str]],
    target_branch: str,
    repo_root: Path,
) -> dict[str, list[str]]:
    """Build mapping of file paths to WPs that modify them.

    Uses git diff to identify which files each WP branch modifies
    relative to the target branch.

    Args:
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples
        target_branch: Branch being merged into (e.g., "main")
        repo_root: Repository root for running git commands

    Returns:
        Dict mapping file_path → [wp_ids that modify it]
    """
    file_to_wps: dict[str, list[str]] = {}

    for _, wp_id, branch_name in wp_workspaces:
        try:
            result = subprocess.run(
                ["git", "diff", "--name-only", f"{target_branch}...{branch_name}"],
                cwd=str(repo_root),
                capture_output=True,
                text=True,
                errors="replace",
                check=False,
            )

            if result.returncode == 0:
                for line in result.stdout.strip().split("\n"):
                    if line:
                        if line not in file_to_wps:
                            file_to_wps[line] = []
                        file_to_wps[line].append(wp_id)
        except Exception:
            continue  # Skip this WP if diff fails

    return file_to_wps


def x_build_file_wp_mapping__mutmut_15(
    wp_workspaces: list[tuple[Path, str, str]],
    target_branch: str,
    repo_root: Path,
) -> dict[str, list[str]]:
    """Build mapping of file paths to WPs that modify them.

    Uses git diff to identify which files each WP branch modifies
    relative to the target branch.

    Args:
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples
        target_branch: Branch being merged into (e.g., "main")
        repo_root: Repository root for running git commands

    Returns:
        Dict mapping file_path → [wp_ids that modify it]
    """
    file_to_wps: dict[str, list[str]] = {}

    for _, wp_id, branch_name in wp_workspaces:
        try:
            result = subprocess.run(
                ["git", "diff", "--name-only", f"{target_branch}...{branch_name}"],
                cwd=str(repo_root),
                capture_output=True,
                text=True,
                encoding="utf-8",
                check=False,
            )

            if result.returncode == 0:
                for line in result.stdout.strip().split("\n"):
                    if line:
                        if line not in file_to_wps:
                            file_to_wps[line] = []
                        file_to_wps[line].append(wp_id)
        except Exception:
            continue  # Skip this WP if diff fails

    return file_to_wps


def x_build_file_wp_mapping__mutmut_16(
    wp_workspaces: list[tuple[Path, str, str]],
    target_branch: str,
    repo_root: Path,
) -> dict[str, list[str]]:
    """Build mapping of file paths to WPs that modify them.

    Uses git diff to identify which files each WP branch modifies
    relative to the target branch.

    Args:
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples
        target_branch: Branch being merged into (e.g., "main")
        repo_root: Repository root for running git commands

    Returns:
        Dict mapping file_path → [wp_ids that modify it]
    """
    file_to_wps: dict[str, list[str]] = {}

    for _, wp_id, branch_name in wp_workspaces:
        try:
            result = subprocess.run(
                ["git", "diff", "--name-only", f"{target_branch}...{branch_name}"],
                cwd=str(repo_root),
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                )

            if result.returncode == 0:
                for line in result.stdout.strip().split("\n"):
                    if line:
                        if line not in file_to_wps:
                            file_to_wps[line] = []
                        file_to_wps[line].append(wp_id)
        except Exception:
            continue  # Skip this WP if diff fails

    return file_to_wps


def x_build_file_wp_mapping__mutmut_17(
    wp_workspaces: list[tuple[Path, str, str]],
    target_branch: str,
    repo_root: Path,
) -> dict[str, list[str]]:
    """Build mapping of file paths to WPs that modify them.

    Uses git diff to identify which files each WP branch modifies
    relative to the target branch.

    Args:
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples
        target_branch: Branch being merged into (e.g., "main")
        repo_root: Repository root for running git commands

    Returns:
        Dict mapping file_path → [wp_ids that modify it]
    """
    file_to_wps: dict[str, list[str]] = {}

    for _, wp_id, branch_name in wp_workspaces:
        try:
            result = subprocess.run(
                ["XXgitXX", "diff", "--name-only", f"{target_branch}...{branch_name}"],
                cwd=str(repo_root),
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )

            if result.returncode == 0:
                for line in result.stdout.strip().split("\n"):
                    if line:
                        if line not in file_to_wps:
                            file_to_wps[line] = []
                        file_to_wps[line].append(wp_id)
        except Exception:
            continue  # Skip this WP if diff fails

    return file_to_wps


def x_build_file_wp_mapping__mutmut_18(
    wp_workspaces: list[tuple[Path, str, str]],
    target_branch: str,
    repo_root: Path,
) -> dict[str, list[str]]:
    """Build mapping of file paths to WPs that modify them.

    Uses git diff to identify which files each WP branch modifies
    relative to the target branch.

    Args:
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples
        target_branch: Branch being merged into (e.g., "main")
        repo_root: Repository root for running git commands

    Returns:
        Dict mapping file_path → [wp_ids that modify it]
    """
    file_to_wps: dict[str, list[str]] = {}

    for _, wp_id, branch_name in wp_workspaces:
        try:
            result = subprocess.run(
                ["GIT", "diff", "--name-only", f"{target_branch}...{branch_name}"],
                cwd=str(repo_root),
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )

            if result.returncode == 0:
                for line in result.stdout.strip().split("\n"):
                    if line:
                        if line not in file_to_wps:
                            file_to_wps[line] = []
                        file_to_wps[line].append(wp_id)
        except Exception:
            continue  # Skip this WP if diff fails

    return file_to_wps


def x_build_file_wp_mapping__mutmut_19(
    wp_workspaces: list[tuple[Path, str, str]],
    target_branch: str,
    repo_root: Path,
) -> dict[str, list[str]]:
    """Build mapping of file paths to WPs that modify them.

    Uses git diff to identify which files each WP branch modifies
    relative to the target branch.

    Args:
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples
        target_branch: Branch being merged into (e.g., "main")
        repo_root: Repository root for running git commands

    Returns:
        Dict mapping file_path → [wp_ids that modify it]
    """
    file_to_wps: dict[str, list[str]] = {}

    for _, wp_id, branch_name in wp_workspaces:
        try:
            result = subprocess.run(
                ["git", "XXdiffXX", "--name-only", f"{target_branch}...{branch_name}"],
                cwd=str(repo_root),
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )

            if result.returncode == 0:
                for line in result.stdout.strip().split("\n"):
                    if line:
                        if line not in file_to_wps:
                            file_to_wps[line] = []
                        file_to_wps[line].append(wp_id)
        except Exception:
            continue  # Skip this WP if diff fails

    return file_to_wps


def x_build_file_wp_mapping__mutmut_20(
    wp_workspaces: list[tuple[Path, str, str]],
    target_branch: str,
    repo_root: Path,
) -> dict[str, list[str]]:
    """Build mapping of file paths to WPs that modify them.

    Uses git diff to identify which files each WP branch modifies
    relative to the target branch.

    Args:
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples
        target_branch: Branch being merged into (e.g., "main")
        repo_root: Repository root for running git commands

    Returns:
        Dict mapping file_path → [wp_ids that modify it]
    """
    file_to_wps: dict[str, list[str]] = {}

    for _, wp_id, branch_name in wp_workspaces:
        try:
            result = subprocess.run(
                ["git", "DIFF", "--name-only", f"{target_branch}...{branch_name}"],
                cwd=str(repo_root),
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )

            if result.returncode == 0:
                for line in result.stdout.strip().split("\n"):
                    if line:
                        if line not in file_to_wps:
                            file_to_wps[line] = []
                        file_to_wps[line].append(wp_id)
        except Exception:
            continue  # Skip this WP if diff fails

    return file_to_wps


def x_build_file_wp_mapping__mutmut_21(
    wp_workspaces: list[tuple[Path, str, str]],
    target_branch: str,
    repo_root: Path,
) -> dict[str, list[str]]:
    """Build mapping of file paths to WPs that modify them.

    Uses git diff to identify which files each WP branch modifies
    relative to the target branch.

    Args:
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples
        target_branch: Branch being merged into (e.g., "main")
        repo_root: Repository root for running git commands

    Returns:
        Dict mapping file_path → [wp_ids that modify it]
    """
    file_to_wps: dict[str, list[str]] = {}

    for _, wp_id, branch_name in wp_workspaces:
        try:
            result = subprocess.run(
                ["git", "diff", "XX--name-onlyXX", f"{target_branch}...{branch_name}"],
                cwd=str(repo_root),
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )

            if result.returncode == 0:
                for line in result.stdout.strip().split("\n"):
                    if line:
                        if line not in file_to_wps:
                            file_to_wps[line] = []
                        file_to_wps[line].append(wp_id)
        except Exception:
            continue  # Skip this WP if diff fails

    return file_to_wps


def x_build_file_wp_mapping__mutmut_22(
    wp_workspaces: list[tuple[Path, str, str]],
    target_branch: str,
    repo_root: Path,
) -> dict[str, list[str]]:
    """Build mapping of file paths to WPs that modify them.

    Uses git diff to identify which files each WP branch modifies
    relative to the target branch.

    Args:
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples
        target_branch: Branch being merged into (e.g., "main")
        repo_root: Repository root for running git commands

    Returns:
        Dict mapping file_path → [wp_ids that modify it]
    """
    file_to_wps: dict[str, list[str]] = {}

    for _, wp_id, branch_name in wp_workspaces:
        try:
            result = subprocess.run(
                ["git", "diff", "--NAME-ONLY", f"{target_branch}...{branch_name}"],
                cwd=str(repo_root),
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )

            if result.returncode == 0:
                for line in result.stdout.strip().split("\n"):
                    if line:
                        if line not in file_to_wps:
                            file_to_wps[line] = []
                        file_to_wps[line].append(wp_id)
        except Exception:
            continue  # Skip this WP if diff fails

    return file_to_wps


def x_build_file_wp_mapping__mutmut_23(
    wp_workspaces: list[tuple[Path, str, str]],
    target_branch: str,
    repo_root: Path,
) -> dict[str, list[str]]:
    """Build mapping of file paths to WPs that modify them.

    Uses git diff to identify which files each WP branch modifies
    relative to the target branch.

    Args:
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples
        target_branch: Branch being merged into (e.g., "main")
        repo_root: Repository root for running git commands

    Returns:
        Dict mapping file_path → [wp_ids that modify it]
    """
    file_to_wps: dict[str, list[str]] = {}

    for _, wp_id, branch_name in wp_workspaces:
        try:
            result = subprocess.run(
                ["git", "diff", "--name-only", f"{target_branch}...{branch_name}"],
                cwd=str(None),
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )

            if result.returncode == 0:
                for line in result.stdout.strip().split("\n"):
                    if line:
                        if line not in file_to_wps:
                            file_to_wps[line] = []
                        file_to_wps[line].append(wp_id)
        except Exception:
            continue  # Skip this WP if diff fails

    return file_to_wps


def x_build_file_wp_mapping__mutmut_24(
    wp_workspaces: list[tuple[Path, str, str]],
    target_branch: str,
    repo_root: Path,
) -> dict[str, list[str]]:
    """Build mapping of file paths to WPs that modify them.

    Uses git diff to identify which files each WP branch modifies
    relative to the target branch.

    Args:
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples
        target_branch: Branch being merged into (e.g., "main")
        repo_root: Repository root for running git commands

    Returns:
        Dict mapping file_path → [wp_ids that modify it]
    """
    file_to_wps: dict[str, list[str]] = {}

    for _, wp_id, branch_name in wp_workspaces:
        try:
            result = subprocess.run(
                ["git", "diff", "--name-only", f"{target_branch}...{branch_name}"],
                cwd=str(repo_root),
                capture_output=False,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )

            if result.returncode == 0:
                for line in result.stdout.strip().split("\n"):
                    if line:
                        if line not in file_to_wps:
                            file_to_wps[line] = []
                        file_to_wps[line].append(wp_id)
        except Exception:
            continue  # Skip this WP if diff fails

    return file_to_wps


def x_build_file_wp_mapping__mutmut_25(
    wp_workspaces: list[tuple[Path, str, str]],
    target_branch: str,
    repo_root: Path,
) -> dict[str, list[str]]:
    """Build mapping of file paths to WPs that modify them.

    Uses git diff to identify which files each WP branch modifies
    relative to the target branch.

    Args:
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples
        target_branch: Branch being merged into (e.g., "main")
        repo_root: Repository root for running git commands

    Returns:
        Dict mapping file_path → [wp_ids that modify it]
    """
    file_to_wps: dict[str, list[str]] = {}

    for _, wp_id, branch_name in wp_workspaces:
        try:
            result = subprocess.run(
                ["git", "diff", "--name-only", f"{target_branch}...{branch_name}"],
                cwd=str(repo_root),
                capture_output=True,
                text=False,
                encoding="utf-8",
                errors="replace",
                check=False,
            )

            if result.returncode == 0:
                for line in result.stdout.strip().split("\n"):
                    if line:
                        if line not in file_to_wps:
                            file_to_wps[line] = []
                        file_to_wps[line].append(wp_id)
        except Exception:
            continue  # Skip this WP if diff fails

    return file_to_wps


def x_build_file_wp_mapping__mutmut_26(
    wp_workspaces: list[tuple[Path, str, str]],
    target_branch: str,
    repo_root: Path,
) -> dict[str, list[str]]:
    """Build mapping of file paths to WPs that modify them.

    Uses git diff to identify which files each WP branch modifies
    relative to the target branch.

    Args:
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples
        target_branch: Branch being merged into (e.g., "main")
        repo_root: Repository root for running git commands

    Returns:
        Dict mapping file_path → [wp_ids that modify it]
    """
    file_to_wps: dict[str, list[str]] = {}

    for _, wp_id, branch_name in wp_workspaces:
        try:
            result = subprocess.run(
                ["git", "diff", "--name-only", f"{target_branch}...{branch_name}"],
                cwd=str(repo_root),
                capture_output=True,
                text=True,
                encoding="XXutf-8XX",
                errors="replace",
                check=False,
            )

            if result.returncode == 0:
                for line in result.stdout.strip().split("\n"):
                    if line:
                        if line not in file_to_wps:
                            file_to_wps[line] = []
                        file_to_wps[line].append(wp_id)
        except Exception:
            continue  # Skip this WP if diff fails

    return file_to_wps


def x_build_file_wp_mapping__mutmut_27(
    wp_workspaces: list[tuple[Path, str, str]],
    target_branch: str,
    repo_root: Path,
) -> dict[str, list[str]]:
    """Build mapping of file paths to WPs that modify them.

    Uses git diff to identify which files each WP branch modifies
    relative to the target branch.

    Args:
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples
        target_branch: Branch being merged into (e.g., "main")
        repo_root: Repository root for running git commands

    Returns:
        Dict mapping file_path → [wp_ids that modify it]
    """
    file_to_wps: dict[str, list[str]] = {}

    for _, wp_id, branch_name in wp_workspaces:
        try:
            result = subprocess.run(
                ["git", "diff", "--name-only", f"{target_branch}...{branch_name}"],
                cwd=str(repo_root),
                capture_output=True,
                text=True,
                encoding="UTF-8",
                errors="replace",
                check=False,
            )

            if result.returncode == 0:
                for line in result.stdout.strip().split("\n"):
                    if line:
                        if line not in file_to_wps:
                            file_to_wps[line] = []
                        file_to_wps[line].append(wp_id)
        except Exception:
            continue  # Skip this WP if diff fails

    return file_to_wps


def x_build_file_wp_mapping__mutmut_28(
    wp_workspaces: list[tuple[Path, str, str]],
    target_branch: str,
    repo_root: Path,
) -> dict[str, list[str]]:
    """Build mapping of file paths to WPs that modify them.

    Uses git diff to identify which files each WP branch modifies
    relative to the target branch.

    Args:
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples
        target_branch: Branch being merged into (e.g., "main")
        repo_root: Repository root for running git commands

    Returns:
        Dict mapping file_path → [wp_ids that modify it]
    """
    file_to_wps: dict[str, list[str]] = {}

    for _, wp_id, branch_name in wp_workspaces:
        try:
            result = subprocess.run(
                ["git", "diff", "--name-only", f"{target_branch}...{branch_name}"],
                cwd=str(repo_root),
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="XXreplaceXX",
                check=False,
            )

            if result.returncode == 0:
                for line in result.stdout.strip().split("\n"):
                    if line:
                        if line not in file_to_wps:
                            file_to_wps[line] = []
                        file_to_wps[line].append(wp_id)
        except Exception:
            continue  # Skip this WP if diff fails

    return file_to_wps


def x_build_file_wp_mapping__mutmut_29(
    wp_workspaces: list[tuple[Path, str, str]],
    target_branch: str,
    repo_root: Path,
) -> dict[str, list[str]]:
    """Build mapping of file paths to WPs that modify them.

    Uses git diff to identify which files each WP branch modifies
    relative to the target branch.

    Args:
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples
        target_branch: Branch being merged into (e.g., "main")
        repo_root: Repository root for running git commands

    Returns:
        Dict mapping file_path → [wp_ids that modify it]
    """
    file_to_wps: dict[str, list[str]] = {}

    for _, wp_id, branch_name in wp_workspaces:
        try:
            result = subprocess.run(
                ["git", "diff", "--name-only", f"{target_branch}...{branch_name}"],
                cwd=str(repo_root),
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="REPLACE",
                check=False,
            )

            if result.returncode == 0:
                for line in result.stdout.strip().split("\n"):
                    if line:
                        if line not in file_to_wps:
                            file_to_wps[line] = []
                        file_to_wps[line].append(wp_id)
        except Exception:
            continue  # Skip this WP if diff fails

    return file_to_wps


def x_build_file_wp_mapping__mutmut_30(
    wp_workspaces: list[tuple[Path, str, str]],
    target_branch: str,
    repo_root: Path,
) -> dict[str, list[str]]:
    """Build mapping of file paths to WPs that modify them.

    Uses git diff to identify which files each WP branch modifies
    relative to the target branch.

    Args:
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples
        target_branch: Branch being merged into (e.g., "main")
        repo_root: Repository root for running git commands

    Returns:
        Dict mapping file_path → [wp_ids that modify it]
    """
    file_to_wps: dict[str, list[str]] = {}

    for _, wp_id, branch_name in wp_workspaces:
        try:
            result = subprocess.run(
                ["git", "diff", "--name-only", f"{target_branch}...{branch_name}"],
                cwd=str(repo_root),
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=True,
            )

            if result.returncode == 0:
                for line in result.stdout.strip().split("\n"):
                    if line:
                        if line not in file_to_wps:
                            file_to_wps[line] = []
                        file_to_wps[line].append(wp_id)
        except Exception:
            continue  # Skip this WP if diff fails

    return file_to_wps


def x_build_file_wp_mapping__mutmut_31(
    wp_workspaces: list[tuple[Path, str, str]],
    target_branch: str,
    repo_root: Path,
) -> dict[str, list[str]]:
    """Build mapping of file paths to WPs that modify them.

    Uses git diff to identify which files each WP branch modifies
    relative to the target branch.

    Args:
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples
        target_branch: Branch being merged into (e.g., "main")
        repo_root: Repository root for running git commands

    Returns:
        Dict mapping file_path → [wp_ids that modify it]
    """
    file_to_wps: dict[str, list[str]] = {}

    for _, wp_id, branch_name in wp_workspaces:
        try:
            result = subprocess.run(
                ["git", "diff", "--name-only", f"{target_branch}...{branch_name}"],
                cwd=str(repo_root),
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )

            if result.returncode != 0:
                for line in result.stdout.strip().split("\n"):
                    if line:
                        if line not in file_to_wps:
                            file_to_wps[line] = []
                        file_to_wps[line].append(wp_id)
        except Exception:
            continue  # Skip this WP if diff fails

    return file_to_wps


def x_build_file_wp_mapping__mutmut_32(
    wp_workspaces: list[tuple[Path, str, str]],
    target_branch: str,
    repo_root: Path,
) -> dict[str, list[str]]:
    """Build mapping of file paths to WPs that modify them.

    Uses git diff to identify which files each WP branch modifies
    relative to the target branch.

    Args:
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples
        target_branch: Branch being merged into (e.g., "main")
        repo_root: Repository root for running git commands

    Returns:
        Dict mapping file_path → [wp_ids that modify it]
    """
    file_to_wps: dict[str, list[str]] = {}

    for _, wp_id, branch_name in wp_workspaces:
        try:
            result = subprocess.run(
                ["git", "diff", "--name-only", f"{target_branch}...{branch_name}"],
                cwd=str(repo_root),
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )

            if result.returncode == 1:
                for line in result.stdout.strip().split("\n"):
                    if line:
                        if line not in file_to_wps:
                            file_to_wps[line] = []
                        file_to_wps[line].append(wp_id)
        except Exception:
            continue  # Skip this WP if diff fails

    return file_to_wps


def x_build_file_wp_mapping__mutmut_33(
    wp_workspaces: list[tuple[Path, str, str]],
    target_branch: str,
    repo_root: Path,
) -> dict[str, list[str]]:
    """Build mapping of file paths to WPs that modify them.

    Uses git diff to identify which files each WP branch modifies
    relative to the target branch.

    Args:
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples
        target_branch: Branch being merged into (e.g., "main")
        repo_root: Repository root for running git commands

    Returns:
        Dict mapping file_path → [wp_ids that modify it]
    """
    file_to_wps: dict[str, list[str]] = {}

    for _, wp_id, branch_name in wp_workspaces:
        try:
            result = subprocess.run(
                ["git", "diff", "--name-only", f"{target_branch}...{branch_name}"],
                cwd=str(repo_root),
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )

            if result.returncode == 0:
                for line in result.stdout.strip().split(None):
                    if line:
                        if line not in file_to_wps:
                            file_to_wps[line] = []
                        file_to_wps[line].append(wp_id)
        except Exception:
            continue  # Skip this WP if diff fails

    return file_to_wps


def x_build_file_wp_mapping__mutmut_34(
    wp_workspaces: list[tuple[Path, str, str]],
    target_branch: str,
    repo_root: Path,
) -> dict[str, list[str]]:
    """Build mapping of file paths to WPs that modify them.

    Uses git diff to identify which files each WP branch modifies
    relative to the target branch.

    Args:
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples
        target_branch: Branch being merged into (e.g., "main")
        repo_root: Repository root for running git commands

    Returns:
        Dict mapping file_path → [wp_ids that modify it]
    """
    file_to_wps: dict[str, list[str]] = {}

    for _, wp_id, branch_name in wp_workspaces:
        try:
            result = subprocess.run(
                ["git", "diff", "--name-only", f"{target_branch}...{branch_name}"],
                cwd=str(repo_root),
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )

            if result.returncode == 0:
                for line in result.stdout.strip().split("XX\nXX"):
                    if line:
                        if line not in file_to_wps:
                            file_to_wps[line] = []
                        file_to_wps[line].append(wp_id)
        except Exception:
            continue  # Skip this WP if diff fails

    return file_to_wps


def x_build_file_wp_mapping__mutmut_35(
    wp_workspaces: list[tuple[Path, str, str]],
    target_branch: str,
    repo_root: Path,
) -> dict[str, list[str]]:
    """Build mapping of file paths to WPs that modify them.

    Uses git diff to identify which files each WP branch modifies
    relative to the target branch.

    Args:
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples
        target_branch: Branch being merged into (e.g., "main")
        repo_root: Repository root for running git commands

    Returns:
        Dict mapping file_path → [wp_ids that modify it]
    """
    file_to_wps: dict[str, list[str]] = {}

    for _, wp_id, branch_name in wp_workspaces:
        try:
            result = subprocess.run(
                ["git", "diff", "--name-only", f"{target_branch}...{branch_name}"],
                cwd=str(repo_root),
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )

            if result.returncode == 0:
                for line in result.stdout.strip().split("\n"):
                    if line:
                        if line in file_to_wps:
                            file_to_wps[line] = []
                        file_to_wps[line].append(wp_id)
        except Exception:
            continue  # Skip this WP if diff fails

    return file_to_wps


def x_build_file_wp_mapping__mutmut_36(
    wp_workspaces: list[tuple[Path, str, str]],
    target_branch: str,
    repo_root: Path,
) -> dict[str, list[str]]:
    """Build mapping of file paths to WPs that modify them.

    Uses git diff to identify which files each WP branch modifies
    relative to the target branch.

    Args:
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples
        target_branch: Branch being merged into (e.g., "main")
        repo_root: Repository root for running git commands

    Returns:
        Dict mapping file_path → [wp_ids that modify it]
    """
    file_to_wps: dict[str, list[str]] = {}

    for _, wp_id, branch_name in wp_workspaces:
        try:
            result = subprocess.run(
                ["git", "diff", "--name-only", f"{target_branch}...{branch_name}"],
                cwd=str(repo_root),
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )

            if result.returncode == 0:
                for line in result.stdout.strip().split("\n"):
                    if line:
                        if line not in file_to_wps:
                            file_to_wps[line] = None
                        file_to_wps[line].append(wp_id)
        except Exception:
            continue  # Skip this WP if diff fails

    return file_to_wps


def x_build_file_wp_mapping__mutmut_37(
    wp_workspaces: list[tuple[Path, str, str]],
    target_branch: str,
    repo_root: Path,
) -> dict[str, list[str]]:
    """Build mapping of file paths to WPs that modify them.

    Uses git diff to identify which files each WP branch modifies
    relative to the target branch.

    Args:
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples
        target_branch: Branch being merged into (e.g., "main")
        repo_root: Repository root for running git commands

    Returns:
        Dict mapping file_path → [wp_ids that modify it]
    """
    file_to_wps: dict[str, list[str]] = {}

    for _, wp_id, branch_name in wp_workspaces:
        try:
            result = subprocess.run(
                ["git", "diff", "--name-only", f"{target_branch}...{branch_name}"],
                cwd=str(repo_root),
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )

            if result.returncode == 0:
                for line in result.stdout.strip().split("\n"):
                    if line:
                        if line not in file_to_wps:
                            file_to_wps[line] = []
                        file_to_wps[line].append(None)
        except Exception:
            continue  # Skip this WP if diff fails

    return file_to_wps


def x_build_file_wp_mapping__mutmut_38(
    wp_workspaces: list[tuple[Path, str, str]],
    target_branch: str,
    repo_root: Path,
) -> dict[str, list[str]]:
    """Build mapping of file paths to WPs that modify them.

    Uses git diff to identify which files each WP branch modifies
    relative to the target branch.

    Args:
        wp_workspaces: List of (worktree_path, wp_id, branch_name) tuples
        target_branch: Branch being merged into (e.g., "main")
        repo_root: Repository root for running git commands

    Returns:
        Dict mapping file_path → [wp_ids that modify it]
    """
    file_to_wps: dict[str, list[str]] = {}

    for _, wp_id, branch_name in wp_workspaces:
        try:
            result = subprocess.run(
                ["git", "diff", "--name-only", f"{target_branch}...{branch_name}"],
                cwd=str(repo_root),
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )

            if result.returncode == 0:
                for line in result.stdout.strip().split("\n"):
                    if line:
                        if line not in file_to_wps:
                            file_to_wps[line] = []
                        file_to_wps[line].append(wp_id)
        except Exception:
            break  # Skip this WP if diff fails

    return file_to_wps

x_build_file_wp_mapping__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_build_file_wp_mapping__mutmut_1': x_build_file_wp_mapping__mutmut_1, 
    'x_build_file_wp_mapping__mutmut_2': x_build_file_wp_mapping__mutmut_2, 
    'x_build_file_wp_mapping__mutmut_3': x_build_file_wp_mapping__mutmut_3, 
    'x_build_file_wp_mapping__mutmut_4': x_build_file_wp_mapping__mutmut_4, 
    'x_build_file_wp_mapping__mutmut_5': x_build_file_wp_mapping__mutmut_5, 
    'x_build_file_wp_mapping__mutmut_6': x_build_file_wp_mapping__mutmut_6, 
    'x_build_file_wp_mapping__mutmut_7': x_build_file_wp_mapping__mutmut_7, 
    'x_build_file_wp_mapping__mutmut_8': x_build_file_wp_mapping__mutmut_8, 
    'x_build_file_wp_mapping__mutmut_9': x_build_file_wp_mapping__mutmut_9, 
    'x_build_file_wp_mapping__mutmut_10': x_build_file_wp_mapping__mutmut_10, 
    'x_build_file_wp_mapping__mutmut_11': x_build_file_wp_mapping__mutmut_11, 
    'x_build_file_wp_mapping__mutmut_12': x_build_file_wp_mapping__mutmut_12, 
    'x_build_file_wp_mapping__mutmut_13': x_build_file_wp_mapping__mutmut_13, 
    'x_build_file_wp_mapping__mutmut_14': x_build_file_wp_mapping__mutmut_14, 
    'x_build_file_wp_mapping__mutmut_15': x_build_file_wp_mapping__mutmut_15, 
    'x_build_file_wp_mapping__mutmut_16': x_build_file_wp_mapping__mutmut_16, 
    'x_build_file_wp_mapping__mutmut_17': x_build_file_wp_mapping__mutmut_17, 
    'x_build_file_wp_mapping__mutmut_18': x_build_file_wp_mapping__mutmut_18, 
    'x_build_file_wp_mapping__mutmut_19': x_build_file_wp_mapping__mutmut_19, 
    'x_build_file_wp_mapping__mutmut_20': x_build_file_wp_mapping__mutmut_20, 
    'x_build_file_wp_mapping__mutmut_21': x_build_file_wp_mapping__mutmut_21, 
    'x_build_file_wp_mapping__mutmut_22': x_build_file_wp_mapping__mutmut_22, 
    'x_build_file_wp_mapping__mutmut_23': x_build_file_wp_mapping__mutmut_23, 
    'x_build_file_wp_mapping__mutmut_24': x_build_file_wp_mapping__mutmut_24, 
    'x_build_file_wp_mapping__mutmut_25': x_build_file_wp_mapping__mutmut_25, 
    'x_build_file_wp_mapping__mutmut_26': x_build_file_wp_mapping__mutmut_26, 
    'x_build_file_wp_mapping__mutmut_27': x_build_file_wp_mapping__mutmut_27, 
    'x_build_file_wp_mapping__mutmut_28': x_build_file_wp_mapping__mutmut_28, 
    'x_build_file_wp_mapping__mutmut_29': x_build_file_wp_mapping__mutmut_29, 
    'x_build_file_wp_mapping__mutmut_30': x_build_file_wp_mapping__mutmut_30, 
    'x_build_file_wp_mapping__mutmut_31': x_build_file_wp_mapping__mutmut_31, 
    'x_build_file_wp_mapping__mutmut_32': x_build_file_wp_mapping__mutmut_32, 
    'x_build_file_wp_mapping__mutmut_33': x_build_file_wp_mapping__mutmut_33, 
    'x_build_file_wp_mapping__mutmut_34': x_build_file_wp_mapping__mutmut_34, 
    'x_build_file_wp_mapping__mutmut_35': x_build_file_wp_mapping__mutmut_35, 
    'x_build_file_wp_mapping__mutmut_36': x_build_file_wp_mapping__mutmut_36, 
    'x_build_file_wp_mapping__mutmut_37': x_build_file_wp_mapping__mutmut_37, 
    'x_build_file_wp_mapping__mutmut_38': x_build_file_wp_mapping__mutmut_38
}
x_build_file_wp_mapping__mutmut_orig.__name__ = 'x_build_file_wp_mapping'


def predict_conflicts(
    wp_workspaces: list[tuple[Path, str, str]],
    target_branch: str,
    repo_root: Path,
) -> list[ConflictPrediction]:
    args = [wp_workspaces, target_branch, repo_root]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_predict_conflicts__mutmut_orig, x_predict_conflicts__mutmut_mutants, args, kwargs, None)


def x_predict_conflicts__mutmut_orig(
    wp_workspaces: list[tuple[Path, str, str]],
    target_branch: str,
    repo_root: Path,
) -> list[ConflictPrediction]:
    """Predict which files will conflict during merge.

    Identifies files modified by multiple WPs, which may result in
    merge conflicts. Status files are marked as auto-resolvable.

    Args:
        wp_workspaces: Ordered list of (worktree_path, wp_id, branch_name) tuples
        target_branch: Branch being merged into (e.g., "main")
        repo_root: Repository root for running git commands

    Returns:
        List of ConflictPrediction for files with potential conflicts
    """
    file_to_wps = build_file_wp_mapping(wp_workspaces, target_branch, repo_root)

    predictions = []
    for file_path, wp_ids in sorted(file_to_wps.items()):
        if len(wp_ids) >= 2:
            predictions.append(
                ConflictPrediction(
                    file_path=file_path,
                    conflicting_wps=wp_ids,
                    is_status_file=is_status_file(file_path),
                    confidence="possible",  # Can enhance with merge-tree in future
                )
            )

    return predictions


def x_predict_conflicts__mutmut_1(
    wp_workspaces: list[tuple[Path, str, str]],
    target_branch: str,
    repo_root: Path,
) -> list[ConflictPrediction]:
    """Predict which files will conflict during merge.

    Identifies files modified by multiple WPs, which may result in
    merge conflicts. Status files are marked as auto-resolvable.

    Args:
        wp_workspaces: Ordered list of (worktree_path, wp_id, branch_name) tuples
        target_branch: Branch being merged into (e.g., "main")
        repo_root: Repository root for running git commands

    Returns:
        List of ConflictPrediction for files with potential conflicts
    """
    file_to_wps = None

    predictions = []
    for file_path, wp_ids in sorted(file_to_wps.items()):
        if len(wp_ids) >= 2:
            predictions.append(
                ConflictPrediction(
                    file_path=file_path,
                    conflicting_wps=wp_ids,
                    is_status_file=is_status_file(file_path),
                    confidence="possible",  # Can enhance with merge-tree in future
                )
            )

    return predictions


def x_predict_conflicts__mutmut_2(
    wp_workspaces: list[tuple[Path, str, str]],
    target_branch: str,
    repo_root: Path,
) -> list[ConflictPrediction]:
    """Predict which files will conflict during merge.

    Identifies files modified by multiple WPs, which may result in
    merge conflicts. Status files are marked as auto-resolvable.

    Args:
        wp_workspaces: Ordered list of (worktree_path, wp_id, branch_name) tuples
        target_branch: Branch being merged into (e.g., "main")
        repo_root: Repository root for running git commands

    Returns:
        List of ConflictPrediction for files with potential conflicts
    """
    file_to_wps = build_file_wp_mapping(None, target_branch, repo_root)

    predictions = []
    for file_path, wp_ids in sorted(file_to_wps.items()):
        if len(wp_ids) >= 2:
            predictions.append(
                ConflictPrediction(
                    file_path=file_path,
                    conflicting_wps=wp_ids,
                    is_status_file=is_status_file(file_path),
                    confidence="possible",  # Can enhance with merge-tree in future
                )
            )

    return predictions


def x_predict_conflicts__mutmut_3(
    wp_workspaces: list[tuple[Path, str, str]],
    target_branch: str,
    repo_root: Path,
) -> list[ConflictPrediction]:
    """Predict which files will conflict during merge.

    Identifies files modified by multiple WPs, which may result in
    merge conflicts. Status files are marked as auto-resolvable.

    Args:
        wp_workspaces: Ordered list of (worktree_path, wp_id, branch_name) tuples
        target_branch: Branch being merged into (e.g., "main")
        repo_root: Repository root for running git commands

    Returns:
        List of ConflictPrediction for files with potential conflicts
    """
    file_to_wps = build_file_wp_mapping(wp_workspaces, None, repo_root)

    predictions = []
    for file_path, wp_ids in sorted(file_to_wps.items()):
        if len(wp_ids) >= 2:
            predictions.append(
                ConflictPrediction(
                    file_path=file_path,
                    conflicting_wps=wp_ids,
                    is_status_file=is_status_file(file_path),
                    confidence="possible",  # Can enhance with merge-tree in future
                )
            )

    return predictions


def x_predict_conflicts__mutmut_4(
    wp_workspaces: list[tuple[Path, str, str]],
    target_branch: str,
    repo_root: Path,
) -> list[ConflictPrediction]:
    """Predict which files will conflict during merge.

    Identifies files modified by multiple WPs, which may result in
    merge conflicts. Status files are marked as auto-resolvable.

    Args:
        wp_workspaces: Ordered list of (worktree_path, wp_id, branch_name) tuples
        target_branch: Branch being merged into (e.g., "main")
        repo_root: Repository root for running git commands

    Returns:
        List of ConflictPrediction for files with potential conflicts
    """
    file_to_wps = build_file_wp_mapping(wp_workspaces, target_branch, None)

    predictions = []
    for file_path, wp_ids in sorted(file_to_wps.items()):
        if len(wp_ids) >= 2:
            predictions.append(
                ConflictPrediction(
                    file_path=file_path,
                    conflicting_wps=wp_ids,
                    is_status_file=is_status_file(file_path),
                    confidence="possible",  # Can enhance with merge-tree in future
                )
            )

    return predictions


def x_predict_conflicts__mutmut_5(
    wp_workspaces: list[tuple[Path, str, str]],
    target_branch: str,
    repo_root: Path,
) -> list[ConflictPrediction]:
    """Predict which files will conflict during merge.

    Identifies files modified by multiple WPs, which may result in
    merge conflicts. Status files are marked as auto-resolvable.

    Args:
        wp_workspaces: Ordered list of (worktree_path, wp_id, branch_name) tuples
        target_branch: Branch being merged into (e.g., "main")
        repo_root: Repository root for running git commands

    Returns:
        List of ConflictPrediction for files with potential conflicts
    """
    file_to_wps = build_file_wp_mapping(target_branch, repo_root)

    predictions = []
    for file_path, wp_ids in sorted(file_to_wps.items()):
        if len(wp_ids) >= 2:
            predictions.append(
                ConflictPrediction(
                    file_path=file_path,
                    conflicting_wps=wp_ids,
                    is_status_file=is_status_file(file_path),
                    confidence="possible",  # Can enhance with merge-tree in future
                )
            )

    return predictions


def x_predict_conflicts__mutmut_6(
    wp_workspaces: list[tuple[Path, str, str]],
    target_branch: str,
    repo_root: Path,
) -> list[ConflictPrediction]:
    """Predict which files will conflict during merge.

    Identifies files modified by multiple WPs, which may result in
    merge conflicts. Status files are marked as auto-resolvable.

    Args:
        wp_workspaces: Ordered list of (worktree_path, wp_id, branch_name) tuples
        target_branch: Branch being merged into (e.g., "main")
        repo_root: Repository root for running git commands

    Returns:
        List of ConflictPrediction for files with potential conflicts
    """
    file_to_wps = build_file_wp_mapping(wp_workspaces, repo_root)

    predictions = []
    for file_path, wp_ids in sorted(file_to_wps.items()):
        if len(wp_ids) >= 2:
            predictions.append(
                ConflictPrediction(
                    file_path=file_path,
                    conflicting_wps=wp_ids,
                    is_status_file=is_status_file(file_path),
                    confidence="possible",  # Can enhance with merge-tree in future
                )
            )

    return predictions


def x_predict_conflicts__mutmut_7(
    wp_workspaces: list[tuple[Path, str, str]],
    target_branch: str,
    repo_root: Path,
) -> list[ConflictPrediction]:
    """Predict which files will conflict during merge.

    Identifies files modified by multiple WPs, which may result in
    merge conflicts. Status files are marked as auto-resolvable.

    Args:
        wp_workspaces: Ordered list of (worktree_path, wp_id, branch_name) tuples
        target_branch: Branch being merged into (e.g., "main")
        repo_root: Repository root for running git commands

    Returns:
        List of ConflictPrediction for files with potential conflicts
    """
    file_to_wps = build_file_wp_mapping(wp_workspaces, target_branch, )

    predictions = []
    for file_path, wp_ids in sorted(file_to_wps.items()):
        if len(wp_ids) >= 2:
            predictions.append(
                ConflictPrediction(
                    file_path=file_path,
                    conflicting_wps=wp_ids,
                    is_status_file=is_status_file(file_path),
                    confidence="possible",  # Can enhance with merge-tree in future
                )
            )

    return predictions


def x_predict_conflicts__mutmut_8(
    wp_workspaces: list[tuple[Path, str, str]],
    target_branch: str,
    repo_root: Path,
) -> list[ConflictPrediction]:
    """Predict which files will conflict during merge.

    Identifies files modified by multiple WPs, which may result in
    merge conflicts. Status files are marked as auto-resolvable.

    Args:
        wp_workspaces: Ordered list of (worktree_path, wp_id, branch_name) tuples
        target_branch: Branch being merged into (e.g., "main")
        repo_root: Repository root for running git commands

    Returns:
        List of ConflictPrediction for files with potential conflicts
    """
    file_to_wps = build_file_wp_mapping(wp_workspaces, target_branch, repo_root)

    predictions = None
    for file_path, wp_ids in sorted(file_to_wps.items()):
        if len(wp_ids) >= 2:
            predictions.append(
                ConflictPrediction(
                    file_path=file_path,
                    conflicting_wps=wp_ids,
                    is_status_file=is_status_file(file_path),
                    confidence="possible",  # Can enhance with merge-tree in future
                )
            )

    return predictions


def x_predict_conflicts__mutmut_9(
    wp_workspaces: list[tuple[Path, str, str]],
    target_branch: str,
    repo_root: Path,
) -> list[ConflictPrediction]:
    """Predict which files will conflict during merge.

    Identifies files modified by multiple WPs, which may result in
    merge conflicts. Status files are marked as auto-resolvable.

    Args:
        wp_workspaces: Ordered list of (worktree_path, wp_id, branch_name) tuples
        target_branch: Branch being merged into (e.g., "main")
        repo_root: Repository root for running git commands

    Returns:
        List of ConflictPrediction for files with potential conflicts
    """
    file_to_wps = build_file_wp_mapping(wp_workspaces, target_branch, repo_root)

    predictions = []
    for file_path, wp_ids in sorted(None):
        if len(wp_ids) >= 2:
            predictions.append(
                ConflictPrediction(
                    file_path=file_path,
                    conflicting_wps=wp_ids,
                    is_status_file=is_status_file(file_path),
                    confidence="possible",  # Can enhance with merge-tree in future
                )
            )

    return predictions


def x_predict_conflicts__mutmut_10(
    wp_workspaces: list[tuple[Path, str, str]],
    target_branch: str,
    repo_root: Path,
) -> list[ConflictPrediction]:
    """Predict which files will conflict during merge.

    Identifies files modified by multiple WPs, which may result in
    merge conflicts. Status files are marked as auto-resolvable.

    Args:
        wp_workspaces: Ordered list of (worktree_path, wp_id, branch_name) tuples
        target_branch: Branch being merged into (e.g., "main")
        repo_root: Repository root for running git commands

    Returns:
        List of ConflictPrediction for files with potential conflicts
    """
    file_to_wps = build_file_wp_mapping(wp_workspaces, target_branch, repo_root)

    predictions = []
    for file_path, wp_ids in sorted(file_to_wps.items()):
        if len(wp_ids) > 2:
            predictions.append(
                ConflictPrediction(
                    file_path=file_path,
                    conflicting_wps=wp_ids,
                    is_status_file=is_status_file(file_path),
                    confidence="possible",  # Can enhance with merge-tree in future
                )
            )

    return predictions


def x_predict_conflicts__mutmut_11(
    wp_workspaces: list[tuple[Path, str, str]],
    target_branch: str,
    repo_root: Path,
) -> list[ConflictPrediction]:
    """Predict which files will conflict during merge.

    Identifies files modified by multiple WPs, which may result in
    merge conflicts. Status files are marked as auto-resolvable.

    Args:
        wp_workspaces: Ordered list of (worktree_path, wp_id, branch_name) tuples
        target_branch: Branch being merged into (e.g., "main")
        repo_root: Repository root for running git commands

    Returns:
        List of ConflictPrediction for files with potential conflicts
    """
    file_to_wps = build_file_wp_mapping(wp_workspaces, target_branch, repo_root)

    predictions = []
    for file_path, wp_ids in sorted(file_to_wps.items()):
        if len(wp_ids) >= 3:
            predictions.append(
                ConflictPrediction(
                    file_path=file_path,
                    conflicting_wps=wp_ids,
                    is_status_file=is_status_file(file_path),
                    confidence="possible",  # Can enhance with merge-tree in future
                )
            )

    return predictions


def x_predict_conflicts__mutmut_12(
    wp_workspaces: list[tuple[Path, str, str]],
    target_branch: str,
    repo_root: Path,
) -> list[ConflictPrediction]:
    """Predict which files will conflict during merge.

    Identifies files modified by multiple WPs, which may result in
    merge conflicts. Status files are marked as auto-resolvable.

    Args:
        wp_workspaces: Ordered list of (worktree_path, wp_id, branch_name) tuples
        target_branch: Branch being merged into (e.g., "main")
        repo_root: Repository root for running git commands

    Returns:
        List of ConflictPrediction for files with potential conflicts
    """
    file_to_wps = build_file_wp_mapping(wp_workspaces, target_branch, repo_root)

    predictions = []
    for file_path, wp_ids in sorted(file_to_wps.items()):
        if len(wp_ids) >= 2:
            predictions.append(
                None
            )

    return predictions


def x_predict_conflicts__mutmut_13(
    wp_workspaces: list[tuple[Path, str, str]],
    target_branch: str,
    repo_root: Path,
) -> list[ConflictPrediction]:
    """Predict which files will conflict during merge.

    Identifies files modified by multiple WPs, which may result in
    merge conflicts. Status files are marked as auto-resolvable.

    Args:
        wp_workspaces: Ordered list of (worktree_path, wp_id, branch_name) tuples
        target_branch: Branch being merged into (e.g., "main")
        repo_root: Repository root for running git commands

    Returns:
        List of ConflictPrediction for files with potential conflicts
    """
    file_to_wps = build_file_wp_mapping(wp_workspaces, target_branch, repo_root)

    predictions = []
    for file_path, wp_ids in sorted(file_to_wps.items()):
        if len(wp_ids) >= 2:
            predictions.append(
                ConflictPrediction(
                    file_path=None,
                    conflicting_wps=wp_ids,
                    is_status_file=is_status_file(file_path),
                    confidence="possible",  # Can enhance with merge-tree in future
                )
            )

    return predictions


def x_predict_conflicts__mutmut_14(
    wp_workspaces: list[tuple[Path, str, str]],
    target_branch: str,
    repo_root: Path,
) -> list[ConflictPrediction]:
    """Predict which files will conflict during merge.

    Identifies files modified by multiple WPs, which may result in
    merge conflicts. Status files are marked as auto-resolvable.

    Args:
        wp_workspaces: Ordered list of (worktree_path, wp_id, branch_name) tuples
        target_branch: Branch being merged into (e.g., "main")
        repo_root: Repository root for running git commands

    Returns:
        List of ConflictPrediction for files with potential conflicts
    """
    file_to_wps = build_file_wp_mapping(wp_workspaces, target_branch, repo_root)

    predictions = []
    for file_path, wp_ids in sorted(file_to_wps.items()):
        if len(wp_ids) >= 2:
            predictions.append(
                ConflictPrediction(
                    file_path=file_path,
                    conflicting_wps=None,
                    is_status_file=is_status_file(file_path),
                    confidence="possible",  # Can enhance with merge-tree in future
                )
            )

    return predictions


def x_predict_conflicts__mutmut_15(
    wp_workspaces: list[tuple[Path, str, str]],
    target_branch: str,
    repo_root: Path,
) -> list[ConflictPrediction]:
    """Predict which files will conflict during merge.

    Identifies files modified by multiple WPs, which may result in
    merge conflicts. Status files are marked as auto-resolvable.

    Args:
        wp_workspaces: Ordered list of (worktree_path, wp_id, branch_name) tuples
        target_branch: Branch being merged into (e.g., "main")
        repo_root: Repository root for running git commands

    Returns:
        List of ConflictPrediction for files with potential conflicts
    """
    file_to_wps = build_file_wp_mapping(wp_workspaces, target_branch, repo_root)

    predictions = []
    for file_path, wp_ids in sorted(file_to_wps.items()):
        if len(wp_ids) >= 2:
            predictions.append(
                ConflictPrediction(
                    file_path=file_path,
                    conflicting_wps=wp_ids,
                    is_status_file=None,
                    confidence="possible",  # Can enhance with merge-tree in future
                )
            )

    return predictions


def x_predict_conflicts__mutmut_16(
    wp_workspaces: list[tuple[Path, str, str]],
    target_branch: str,
    repo_root: Path,
) -> list[ConflictPrediction]:
    """Predict which files will conflict during merge.

    Identifies files modified by multiple WPs, which may result in
    merge conflicts. Status files are marked as auto-resolvable.

    Args:
        wp_workspaces: Ordered list of (worktree_path, wp_id, branch_name) tuples
        target_branch: Branch being merged into (e.g., "main")
        repo_root: Repository root for running git commands

    Returns:
        List of ConflictPrediction for files with potential conflicts
    """
    file_to_wps = build_file_wp_mapping(wp_workspaces, target_branch, repo_root)

    predictions = []
    for file_path, wp_ids in sorted(file_to_wps.items()):
        if len(wp_ids) >= 2:
            predictions.append(
                ConflictPrediction(
                    file_path=file_path,
                    conflicting_wps=wp_ids,
                    is_status_file=is_status_file(file_path),
                    confidence=None,  # Can enhance with merge-tree in future
                )
            )

    return predictions


def x_predict_conflicts__mutmut_17(
    wp_workspaces: list[tuple[Path, str, str]],
    target_branch: str,
    repo_root: Path,
) -> list[ConflictPrediction]:
    """Predict which files will conflict during merge.

    Identifies files modified by multiple WPs, which may result in
    merge conflicts. Status files are marked as auto-resolvable.

    Args:
        wp_workspaces: Ordered list of (worktree_path, wp_id, branch_name) tuples
        target_branch: Branch being merged into (e.g., "main")
        repo_root: Repository root for running git commands

    Returns:
        List of ConflictPrediction for files with potential conflicts
    """
    file_to_wps = build_file_wp_mapping(wp_workspaces, target_branch, repo_root)

    predictions = []
    for file_path, wp_ids in sorted(file_to_wps.items()):
        if len(wp_ids) >= 2:
            predictions.append(
                ConflictPrediction(
                    conflicting_wps=wp_ids,
                    is_status_file=is_status_file(file_path),
                    confidence="possible",  # Can enhance with merge-tree in future
                )
            )

    return predictions


def x_predict_conflicts__mutmut_18(
    wp_workspaces: list[tuple[Path, str, str]],
    target_branch: str,
    repo_root: Path,
) -> list[ConflictPrediction]:
    """Predict which files will conflict during merge.

    Identifies files modified by multiple WPs, which may result in
    merge conflicts. Status files are marked as auto-resolvable.

    Args:
        wp_workspaces: Ordered list of (worktree_path, wp_id, branch_name) tuples
        target_branch: Branch being merged into (e.g., "main")
        repo_root: Repository root for running git commands

    Returns:
        List of ConflictPrediction for files with potential conflicts
    """
    file_to_wps = build_file_wp_mapping(wp_workspaces, target_branch, repo_root)

    predictions = []
    for file_path, wp_ids in sorted(file_to_wps.items()):
        if len(wp_ids) >= 2:
            predictions.append(
                ConflictPrediction(
                    file_path=file_path,
                    is_status_file=is_status_file(file_path),
                    confidence="possible",  # Can enhance with merge-tree in future
                )
            )

    return predictions


def x_predict_conflicts__mutmut_19(
    wp_workspaces: list[tuple[Path, str, str]],
    target_branch: str,
    repo_root: Path,
) -> list[ConflictPrediction]:
    """Predict which files will conflict during merge.

    Identifies files modified by multiple WPs, which may result in
    merge conflicts. Status files are marked as auto-resolvable.

    Args:
        wp_workspaces: Ordered list of (worktree_path, wp_id, branch_name) tuples
        target_branch: Branch being merged into (e.g., "main")
        repo_root: Repository root for running git commands

    Returns:
        List of ConflictPrediction for files with potential conflicts
    """
    file_to_wps = build_file_wp_mapping(wp_workspaces, target_branch, repo_root)

    predictions = []
    for file_path, wp_ids in sorted(file_to_wps.items()):
        if len(wp_ids) >= 2:
            predictions.append(
                ConflictPrediction(
                    file_path=file_path,
                    conflicting_wps=wp_ids,
                    confidence="possible",  # Can enhance with merge-tree in future
                )
            )

    return predictions


def x_predict_conflicts__mutmut_20(
    wp_workspaces: list[tuple[Path, str, str]],
    target_branch: str,
    repo_root: Path,
) -> list[ConflictPrediction]:
    """Predict which files will conflict during merge.

    Identifies files modified by multiple WPs, which may result in
    merge conflicts. Status files are marked as auto-resolvable.

    Args:
        wp_workspaces: Ordered list of (worktree_path, wp_id, branch_name) tuples
        target_branch: Branch being merged into (e.g., "main")
        repo_root: Repository root for running git commands

    Returns:
        List of ConflictPrediction for files with potential conflicts
    """
    file_to_wps = build_file_wp_mapping(wp_workspaces, target_branch, repo_root)

    predictions = []
    for file_path, wp_ids in sorted(file_to_wps.items()):
        if len(wp_ids) >= 2:
            predictions.append(
                ConflictPrediction(
                    file_path=file_path,
                    conflicting_wps=wp_ids,
                    is_status_file=is_status_file(file_path),
                    )
            )

    return predictions


def x_predict_conflicts__mutmut_21(
    wp_workspaces: list[tuple[Path, str, str]],
    target_branch: str,
    repo_root: Path,
) -> list[ConflictPrediction]:
    """Predict which files will conflict during merge.

    Identifies files modified by multiple WPs, which may result in
    merge conflicts. Status files are marked as auto-resolvable.

    Args:
        wp_workspaces: Ordered list of (worktree_path, wp_id, branch_name) tuples
        target_branch: Branch being merged into (e.g., "main")
        repo_root: Repository root for running git commands

    Returns:
        List of ConflictPrediction for files with potential conflicts
    """
    file_to_wps = build_file_wp_mapping(wp_workspaces, target_branch, repo_root)

    predictions = []
    for file_path, wp_ids in sorted(file_to_wps.items()):
        if len(wp_ids) >= 2:
            predictions.append(
                ConflictPrediction(
                    file_path=file_path,
                    conflicting_wps=wp_ids,
                    is_status_file=is_status_file(None),
                    confidence="possible",  # Can enhance with merge-tree in future
                )
            )

    return predictions


def x_predict_conflicts__mutmut_22(
    wp_workspaces: list[tuple[Path, str, str]],
    target_branch: str,
    repo_root: Path,
) -> list[ConflictPrediction]:
    """Predict which files will conflict during merge.

    Identifies files modified by multiple WPs, which may result in
    merge conflicts. Status files are marked as auto-resolvable.

    Args:
        wp_workspaces: Ordered list of (worktree_path, wp_id, branch_name) tuples
        target_branch: Branch being merged into (e.g., "main")
        repo_root: Repository root for running git commands

    Returns:
        List of ConflictPrediction for files with potential conflicts
    """
    file_to_wps = build_file_wp_mapping(wp_workspaces, target_branch, repo_root)

    predictions = []
    for file_path, wp_ids in sorted(file_to_wps.items()):
        if len(wp_ids) >= 2:
            predictions.append(
                ConflictPrediction(
                    file_path=file_path,
                    conflicting_wps=wp_ids,
                    is_status_file=is_status_file(file_path),
                    confidence="XXpossibleXX",  # Can enhance with merge-tree in future
                )
            )

    return predictions


def x_predict_conflicts__mutmut_23(
    wp_workspaces: list[tuple[Path, str, str]],
    target_branch: str,
    repo_root: Path,
) -> list[ConflictPrediction]:
    """Predict which files will conflict during merge.

    Identifies files modified by multiple WPs, which may result in
    merge conflicts. Status files are marked as auto-resolvable.

    Args:
        wp_workspaces: Ordered list of (worktree_path, wp_id, branch_name) tuples
        target_branch: Branch being merged into (e.g., "main")
        repo_root: Repository root for running git commands

    Returns:
        List of ConflictPrediction for files with potential conflicts
    """
    file_to_wps = build_file_wp_mapping(wp_workspaces, target_branch, repo_root)

    predictions = []
    for file_path, wp_ids in sorted(file_to_wps.items()):
        if len(wp_ids) >= 2:
            predictions.append(
                ConflictPrediction(
                    file_path=file_path,
                    conflicting_wps=wp_ids,
                    is_status_file=is_status_file(file_path),
                    confidence="POSSIBLE",  # Can enhance with merge-tree in future
                )
            )

    return predictions

x_predict_conflicts__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_predict_conflicts__mutmut_1': x_predict_conflicts__mutmut_1, 
    'x_predict_conflicts__mutmut_2': x_predict_conflicts__mutmut_2, 
    'x_predict_conflicts__mutmut_3': x_predict_conflicts__mutmut_3, 
    'x_predict_conflicts__mutmut_4': x_predict_conflicts__mutmut_4, 
    'x_predict_conflicts__mutmut_5': x_predict_conflicts__mutmut_5, 
    'x_predict_conflicts__mutmut_6': x_predict_conflicts__mutmut_6, 
    'x_predict_conflicts__mutmut_7': x_predict_conflicts__mutmut_7, 
    'x_predict_conflicts__mutmut_8': x_predict_conflicts__mutmut_8, 
    'x_predict_conflicts__mutmut_9': x_predict_conflicts__mutmut_9, 
    'x_predict_conflicts__mutmut_10': x_predict_conflicts__mutmut_10, 
    'x_predict_conflicts__mutmut_11': x_predict_conflicts__mutmut_11, 
    'x_predict_conflicts__mutmut_12': x_predict_conflicts__mutmut_12, 
    'x_predict_conflicts__mutmut_13': x_predict_conflicts__mutmut_13, 
    'x_predict_conflicts__mutmut_14': x_predict_conflicts__mutmut_14, 
    'x_predict_conflicts__mutmut_15': x_predict_conflicts__mutmut_15, 
    'x_predict_conflicts__mutmut_16': x_predict_conflicts__mutmut_16, 
    'x_predict_conflicts__mutmut_17': x_predict_conflicts__mutmut_17, 
    'x_predict_conflicts__mutmut_18': x_predict_conflicts__mutmut_18, 
    'x_predict_conflicts__mutmut_19': x_predict_conflicts__mutmut_19, 
    'x_predict_conflicts__mutmut_20': x_predict_conflicts__mutmut_20, 
    'x_predict_conflicts__mutmut_21': x_predict_conflicts__mutmut_21, 
    'x_predict_conflicts__mutmut_22': x_predict_conflicts__mutmut_22, 
    'x_predict_conflicts__mutmut_23': x_predict_conflicts__mutmut_23
}
x_predict_conflicts__mutmut_orig.__name__ = 'x_predict_conflicts'


def display_conflict_forecast(
    predictions: list[ConflictPrediction],
    console: Console,
) -> None:
    args = [predictions, console]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_display_conflict_forecast__mutmut_orig, x_display_conflict_forecast__mutmut_mutants, args, kwargs, None)


def x_display_conflict_forecast__mutmut_orig(
    predictions: list[ConflictPrediction],
    console: Console,
) -> None:
    """Display conflict predictions with Rich formatting.

    Groups predictions into auto-resolvable (status files) and
    manual-required categories for clear user guidance.

    Args:
        predictions: List of ConflictPrediction objects
        console: Rich Console instance for output
    """
    if not predictions:
        console.print("\n[green]No conflicts predicted[/green]\n")
        return

    console.print("\n[bold]Conflict Forecast[/bold]\n")

    auto_resolvable = [p for p in predictions if p.auto_resolvable]
    manual_required = [p for p in predictions if not p.auto_resolvable]

    # Summary counts
    total = len(predictions)
    auto_count = len(auto_resolvable)
    manual_count = len(manual_required)

    console.print(f"[dim]Found {total} potential conflict(s): {auto_count} auto-resolvable, {manual_count} manual[/dim]\n")

    # Create table for conflicts
    if manual_required:
        table = Table(show_header=True, header_style="bold yellow")
        table.add_column("File")
        table.add_column("WPs")
        table.add_column("Confidence")

        for pred in manual_required:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps, pred.confidence)

        console.print("[yellow]May require manual resolution:[/yellow]")
        console.print(table)
        console.print()

    if auto_resolvable:
        table = Table(show_header=True, header_style="bold dim")
        table.add_column("Status File")
        table.add_column("WPs")

        for pred in auto_resolvable:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps)

        console.print("[dim]Auto-resolvable (status files):[/dim]")
        console.print(table)
        console.print()

    # Summary guidance
    if manual_count == 0:
        console.print("[green]All conflicts can be auto-resolved.[/green]\n")
    else:
        console.print(
            f"[yellow]Prepare to resolve {manual_count} conflict(s) manually during merge.[/yellow]\n"
        )


def x_display_conflict_forecast__mutmut_1(
    predictions: list[ConflictPrediction],
    console: Console,
) -> None:
    """Display conflict predictions with Rich formatting.

    Groups predictions into auto-resolvable (status files) and
    manual-required categories for clear user guidance.

    Args:
        predictions: List of ConflictPrediction objects
        console: Rich Console instance for output
    """
    if predictions:
        console.print("\n[green]No conflicts predicted[/green]\n")
        return

    console.print("\n[bold]Conflict Forecast[/bold]\n")

    auto_resolvable = [p for p in predictions if p.auto_resolvable]
    manual_required = [p for p in predictions if not p.auto_resolvable]

    # Summary counts
    total = len(predictions)
    auto_count = len(auto_resolvable)
    manual_count = len(manual_required)

    console.print(f"[dim]Found {total} potential conflict(s): {auto_count} auto-resolvable, {manual_count} manual[/dim]\n")

    # Create table for conflicts
    if manual_required:
        table = Table(show_header=True, header_style="bold yellow")
        table.add_column("File")
        table.add_column("WPs")
        table.add_column("Confidence")

        for pred in manual_required:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps, pred.confidence)

        console.print("[yellow]May require manual resolution:[/yellow]")
        console.print(table)
        console.print()

    if auto_resolvable:
        table = Table(show_header=True, header_style="bold dim")
        table.add_column("Status File")
        table.add_column("WPs")

        for pred in auto_resolvable:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps)

        console.print("[dim]Auto-resolvable (status files):[/dim]")
        console.print(table)
        console.print()

    # Summary guidance
    if manual_count == 0:
        console.print("[green]All conflicts can be auto-resolved.[/green]\n")
    else:
        console.print(
            f"[yellow]Prepare to resolve {manual_count} conflict(s) manually during merge.[/yellow]\n"
        )


def x_display_conflict_forecast__mutmut_2(
    predictions: list[ConflictPrediction],
    console: Console,
) -> None:
    """Display conflict predictions with Rich formatting.

    Groups predictions into auto-resolvable (status files) and
    manual-required categories for clear user guidance.

    Args:
        predictions: List of ConflictPrediction objects
        console: Rich Console instance for output
    """
    if not predictions:
        console.print(None)
        return

    console.print("\n[bold]Conflict Forecast[/bold]\n")

    auto_resolvable = [p for p in predictions if p.auto_resolvable]
    manual_required = [p for p in predictions if not p.auto_resolvable]

    # Summary counts
    total = len(predictions)
    auto_count = len(auto_resolvable)
    manual_count = len(manual_required)

    console.print(f"[dim]Found {total} potential conflict(s): {auto_count} auto-resolvable, {manual_count} manual[/dim]\n")

    # Create table for conflicts
    if manual_required:
        table = Table(show_header=True, header_style="bold yellow")
        table.add_column("File")
        table.add_column("WPs")
        table.add_column("Confidence")

        for pred in manual_required:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps, pred.confidence)

        console.print("[yellow]May require manual resolution:[/yellow]")
        console.print(table)
        console.print()

    if auto_resolvable:
        table = Table(show_header=True, header_style="bold dim")
        table.add_column("Status File")
        table.add_column("WPs")

        for pred in auto_resolvable:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps)

        console.print("[dim]Auto-resolvable (status files):[/dim]")
        console.print(table)
        console.print()

    # Summary guidance
    if manual_count == 0:
        console.print("[green]All conflicts can be auto-resolved.[/green]\n")
    else:
        console.print(
            f"[yellow]Prepare to resolve {manual_count} conflict(s) manually during merge.[/yellow]\n"
        )


def x_display_conflict_forecast__mutmut_3(
    predictions: list[ConflictPrediction],
    console: Console,
) -> None:
    """Display conflict predictions with Rich formatting.

    Groups predictions into auto-resolvable (status files) and
    manual-required categories for clear user guidance.

    Args:
        predictions: List of ConflictPrediction objects
        console: Rich Console instance for output
    """
    if not predictions:
        console.print("XX\n[green]No conflicts predicted[/green]\nXX")
        return

    console.print("\n[bold]Conflict Forecast[/bold]\n")

    auto_resolvable = [p for p in predictions if p.auto_resolvable]
    manual_required = [p for p in predictions if not p.auto_resolvable]

    # Summary counts
    total = len(predictions)
    auto_count = len(auto_resolvable)
    manual_count = len(manual_required)

    console.print(f"[dim]Found {total} potential conflict(s): {auto_count} auto-resolvable, {manual_count} manual[/dim]\n")

    # Create table for conflicts
    if manual_required:
        table = Table(show_header=True, header_style="bold yellow")
        table.add_column("File")
        table.add_column("WPs")
        table.add_column("Confidence")

        for pred in manual_required:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps, pred.confidence)

        console.print("[yellow]May require manual resolution:[/yellow]")
        console.print(table)
        console.print()

    if auto_resolvable:
        table = Table(show_header=True, header_style="bold dim")
        table.add_column("Status File")
        table.add_column("WPs")

        for pred in auto_resolvable:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps)

        console.print("[dim]Auto-resolvable (status files):[/dim]")
        console.print(table)
        console.print()

    # Summary guidance
    if manual_count == 0:
        console.print("[green]All conflicts can be auto-resolved.[/green]\n")
    else:
        console.print(
            f"[yellow]Prepare to resolve {manual_count} conflict(s) manually during merge.[/yellow]\n"
        )


def x_display_conflict_forecast__mutmut_4(
    predictions: list[ConflictPrediction],
    console: Console,
) -> None:
    """Display conflict predictions with Rich formatting.

    Groups predictions into auto-resolvable (status files) and
    manual-required categories for clear user guidance.

    Args:
        predictions: List of ConflictPrediction objects
        console: Rich Console instance for output
    """
    if not predictions:
        console.print("\n[green]no conflicts predicted[/green]\n")
        return

    console.print("\n[bold]Conflict Forecast[/bold]\n")

    auto_resolvable = [p for p in predictions if p.auto_resolvable]
    manual_required = [p for p in predictions if not p.auto_resolvable]

    # Summary counts
    total = len(predictions)
    auto_count = len(auto_resolvable)
    manual_count = len(manual_required)

    console.print(f"[dim]Found {total} potential conflict(s): {auto_count} auto-resolvable, {manual_count} manual[/dim]\n")

    # Create table for conflicts
    if manual_required:
        table = Table(show_header=True, header_style="bold yellow")
        table.add_column("File")
        table.add_column("WPs")
        table.add_column("Confidence")

        for pred in manual_required:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps, pred.confidence)

        console.print("[yellow]May require manual resolution:[/yellow]")
        console.print(table)
        console.print()

    if auto_resolvable:
        table = Table(show_header=True, header_style="bold dim")
        table.add_column("Status File")
        table.add_column("WPs")

        for pred in auto_resolvable:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps)

        console.print("[dim]Auto-resolvable (status files):[/dim]")
        console.print(table)
        console.print()

    # Summary guidance
    if manual_count == 0:
        console.print("[green]All conflicts can be auto-resolved.[/green]\n")
    else:
        console.print(
            f"[yellow]Prepare to resolve {manual_count} conflict(s) manually during merge.[/yellow]\n"
        )


def x_display_conflict_forecast__mutmut_5(
    predictions: list[ConflictPrediction],
    console: Console,
) -> None:
    """Display conflict predictions with Rich formatting.

    Groups predictions into auto-resolvable (status files) and
    manual-required categories for clear user guidance.

    Args:
        predictions: List of ConflictPrediction objects
        console: Rich Console instance for output
    """
    if not predictions:
        console.print("\n[GREEN]NO CONFLICTS PREDICTED[/GREEN]\n")
        return

    console.print("\n[bold]Conflict Forecast[/bold]\n")

    auto_resolvable = [p for p in predictions if p.auto_resolvable]
    manual_required = [p for p in predictions if not p.auto_resolvable]

    # Summary counts
    total = len(predictions)
    auto_count = len(auto_resolvable)
    manual_count = len(manual_required)

    console.print(f"[dim]Found {total} potential conflict(s): {auto_count} auto-resolvable, {manual_count} manual[/dim]\n")

    # Create table for conflicts
    if manual_required:
        table = Table(show_header=True, header_style="bold yellow")
        table.add_column("File")
        table.add_column("WPs")
        table.add_column("Confidence")

        for pred in manual_required:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps, pred.confidence)

        console.print("[yellow]May require manual resolution:[/yellow]")
        console.print(table)
        console.print()

    if auto_resolvable:
        table = Table(show_header=True, header_style="bold dim")
        table.add_column("Status File")
        table.add_column("WPs")

        for pred in auto_resolvable:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps)

        console.print("[dim]Auto-resolvable (status files):[/dim]")
        console.print(table)
        console.print()

    # Summary guidance
    if manual_count == 0:
        console.print("[green]All conflicts can be auto-resolved.[/green]\n")
    else:
        console.print(
            f"[yellow]Prepare to resolve {manual_count} conflict(s) manually during merge.[/yellow]\n"
        )


def x_display_conflict_forecast__mutmut_6(
    predictions: list[ConflictPrediction],
    console: Console,
) -> None:
    """Display conflict predictions with Rich formatting.

    Groups predictions into auto-resolvable (status files) and
    manual-required categories for clear user guidance.

    Args:
        predictions: List of ConflictPrediction objects
        console: Rich Console instance for output
    """
    if not predictions:
        console.print("\n[green]No conflicts predicted[/green]\n")
        return

    console.print(None)

    auto_resolvable = [p for p in predictions if p.auto_resolvable]
    manual_required = [p for p in predictions if not p.auto_resolvable]

    # Summary counts
    total = len(predictions)
    auto_count = len(auto_resolvable)
    manual_count = len(manual_required)

    console.print(f"[dim]Found {total} potential conflict(s): {auto_count} auto-resolvable, {manual_count} manual[/dim]\n")

    # Create table for conflicts
    if manual_required:
        table = Table(show_header=True, header_style="bold yellow")
        table.add_column("File")
        table.add_column("WPs")
        table.add_column("Confidence")

        for pred in manual_required:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps, pred.confidence)

        console.print("[yellow]May require manual resolution:[/yellow]")
        console.print(table)
        console.print()

    if auto_resolvable:
        table = Table(show_header=True, header_style="bold dim")
        table.add_column("Status File")
        table.add_column("WPs")

        for pred in auto_resolvable:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps)

        console.print("[dim]Auto-resolvable (status files):[/dim]")
        console.print(table)
        console.print()

    # Summary guidance
    if manual_count == 0:
        console.print("[green]All conflicts can be auto-resolved.[/green]\n")
    else:
        console.print(
            f"[yellow]Prepare to resolve {manual_count} conflict(s) manually during merge.[/yellow]\n"
        )


def x_display_conflict_forecast__mutmut_7(
    predictions: list[ConflictPrediction],
    console: Console,
) -> None:
    """Display conflict predictions with Rich formatting.

    Groups predictions into auto-resolvable (status files) and
    manual-required categories for clear user guidance.

    Args:
        predictions: List of ConflictPrediction objects
        console: Rich Console instance for output
    """
    if not predictions:
        console.print("\n[green]No conflicts predicted[/green]\n")
        return

    console.print("XX\n[bold]Conflict Forecast[/bold]\nXX")

    auto_resolvable = [p for p in predictions if p.auto_resolvable]
    manual_required = [p for p in predictions if not p.auto_resolvable]

    # Summary counts
    total = len(predictions)
    auto_count = len(auto_resolvable)
    manual_count = len(manual_required)

    console.print(f"[dim]Found {total} potential conflict(s): {auto_count} auto-resolvable, {manual_count} manual[/dim]\n")

    # Create table for conflicts
    if manual_required:
        table = Table(show_header=True, header_style="bold yellow")
        table.add_column("File")
        table.add_column("WPs")
        table.add_column("Confidence")

        for pred in manual_required:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps, pred.confidence)

        console.print("[yellow]May require manual resolution:[/yellow]")
        console.print(table)
        console.print()

    if auto_resolvable:
        table = Table(show_header=True, header_style="bold dim")
        table.add_column("Status File")
        table.add_column("WPs")

        for pred in auto_resolvable:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps)

        console.print("[dim]Auto-resolvable (status files):[/dim]")
        console.print(table)
        console.print()

    # Summary guidance
    if manual_count == 0:
        console.print("[green]All conflicts can be auto-resolved.[/green]\n")
    else:
        console.print(
            f"[yellow]Prepare to resolve {manual_count} conflict(s) manually during merge.[/yellow]\n"
        )


def x_display_conflict_forecast__mutmut_8(
    predictions: list[ConflictPrediction],
    console: Console,
) -> None:
    """Display conflict predictions with Rich formatting.

    Groups predictions into auto-resolvable (status files) and
    manual-required categories for clear user guidance.

    Args:
        predictions: List of ConflictPrediction objects
        console: Rich Console instance for output
    """
    if not predictions:
        console.print("\n[green]No conflicts predicted[/green]\n")
        return

    console.print("\n[bold]conflict forecast[/bold]\n")

    auto_resolvable = [p for p in predictions if p.auto_resolvable]
    manual_required = [p for p in predictions if not p.auto_resolvable]

    # Summary counts
    total = len(predictions)
    auto_count = len(auto_resolvable)
    manual_count = len(manual_required)

    console.print(f"[dim]Found {total} potential conflict(s): {auto_count} auto-resolvable, {manual_count} manual[/dim]\n")

    # Create table for conflicts
    if manual_required:
        table = Table(show_header=True, header_style="bold yellow")
        table.add_column("File")
        table.add_column("WPs")
        table.add_column("Confidence")

        for pred in manual_required:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps, pred.confidence)

        console.print("[yellow]May require manual resolution:[/yellow]")
        console.print(table)
        console.print()

    if auto_resolvable:
        table = Table(show_header=True, header_style="bold dim")
        table.add_column("Status File")
        table.add_column("WPs")

        for pred in auto_resolvable:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps)

        console.print("[dim]Auto-resolvable (status files):[/dim]")
        console.print(table)
        console.print()

    # Summary guidance
    if manual_count == 0:
        console.print("[green]All conflicts can be auto-resolved.[/green]\n")
    else:
        console.print(
            f"[yellow]Prepare to resolve {manual_count} conflict(s) manually during merge.[/yellow]\n"
        )


def x_display_conflict_forecast__mutmut_9(
    predictions: list[ConflictPrediction],
    console: Console,
) -> None:
    """Display conflict predictions with Rich formatting.

    Groups predictions into auto-resolvable (status files) and
    manual-required categories for clear user guidance.

    Args:
        predictions: List of ConflictPrediction objects
        console: Rich Console instance for output
    """
    if not predictions:
        console.print("\n[green]No conflicts predicted[/green]\n")
        return

    console.print("\n[BOLD]CONFLICT FORECAST[/BOLD]\n")

    auto_resolvable = [p for p in predictions if p.auto_resolvable]
    manual_required = [p for p in predictions if not p.auto_resolvable]

    # Summary counts
    total = len(predictions)
    auto_count = len(auto_resolvable)
    manual_count = len(manual_required)

    console.print(f"[dim]Found {total} potential conflict(s): {auto_count} auto-resolvable, {manual_count} manual[/dim]\n")

    # Create table for conflicts
    if manual_required:
        table = Table(show_header=True, header_style="bold yellow")
        table.add_column("File")
        table.add_column("WPs")
        table.add_column("Confidence")

        for pred in manual_required:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps, pred.confidence)

        console.print("[yellow]May require manual resolution:[/yellow]")
        console.print(table)
        console.print()

    if auto_resolvable:
        table = Table(show_header=True, header_style="bold dim")
        table.add_column("Status File")
        table.add_column("WPs")

        for pred in auto_resolvable:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps)

        console.print("[dim]Auto-resolvable (status files):[/dim]")
        console.print(table)
        console.print()

    # Summary guidance
    if manual_count == 0:
        console.print("[green]All conflicts can be auto-resolved.[/green]\n")
    else:
        console.print(
            f"[yellow]Prepare to resolve {manual_count} conflict(s) manually during merge.[/yellow]\n"
        )


def x_display_conflict_forecast__mutmut_10(
    predictions: list[ConflictPrediction],
    console: Console,
) -> None:
    """Display conflict predictions with Rich formatting.

    Groups predictions into auto-resolvable (status files) and
    manual-required categories for clear user guidance.

    Args:
        predictions: List of ConflictPrediction objects
        console: Rich Console instance for output
    """
    if not predictions:
        console.print("\n[green]No conflicts predicted[/green]\n")
        return

    console.print("\n[bold]Conflict Forecast[/bold]\n")

    auto_resolvable = None
    manual_required = [p for p in predictions if not p.auto_resolvable]

    # Summary counts
    total = len(predictions)
    auto_count = len(auto_resolvable)
    manual_count = len(manual_required)

    console.print(f"[dim]Found {total} potential conflict(s): {auto_count} auto-resolvable, {manual_count} manual[/dim]\n")

    # Create table for conflicts
    if manual_required:
        table = Table(show_header=True, header_style="bold yellow")
        table.add_column("File")
        table.add_column("WPs")
        table.add_column("Confidence")

        for pred in manual_required:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps, pred.confidence)

        console.print("[yellow]May require manual resolution:[/yellow]")
        console.print(table)
        console.print()

    if auto_resolvable:
        table = Table(show_header=True, header_style="bold dim")
        table.add_column("Status File")
        table.add_column("WPs")

        for pred in auto_resolvable:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps)

        console.print("[dim]Auto-resolvable (status files):[/dim]")
        console.print(table)
        console.print()

    # Summary guidance
    if manual_count == 0:
        console.print("[green]All conflicts can be auto-resolved.[/green]\n")
    else:
        console.print(
            f"[yellow]Prepare to resolve {manual_count} conflict(s) manually during merge.[/yellow]\n"
        )


def x_display_conflict_forecast__mutmut_11(
    predictions: list[ConflictPrediction],
    console: Console,
) -> None:
    """Display conflict predictions with Rich formatting.

    Groups predictions into auto-resolvable (status files) and
    manual-required categories for clear user guidance.

    Args:
        predictions: List of ConflictPrediction objects
        console: Rich Console instance for output
    """
    if not predictions:
        console.print("\n[green]No conflicts predicted[/green]\n")
        return

    console.print("\n[bold]Conflict Forecast[/bold]\n")

    auto_resolvable = [p for p in predictions if p.auto_resolvable]
    manual_required = None

    # Summary counts
    total = len(predictions)
    auto_count = len(auto_resolvable)
    manual_count = len(manual_required)

    console.print(f"[dim]Found {total} potential conflict(s): {auto_count} auto-resolvable, {manual_count} manual[/dim]\n")

    # Create table for conflicts
    if manual_required:
        table = Table(show_header=True, header_style="bold yellow")
        table.add_column("File")
        table.add_column("WPs")
        table.add_column("Confidence")

        for pred in manual_required:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps, pred.confidence)

        console.print("[yellow]May require manual resolution:[/yellow]")
        console.print(table)
        console.print()

    if auto_resolvable:
        table = Table(show_header=True, header_style="bold dim")
        table.add_column("Status File")
        table.add_column("WPs")

        for pred in auto_resolvable:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps)

        console.print("[dim]Auto-resolvable (status files):[/dim]")
        console.print(table)
        console.print()

    # Summary guidance
    if manual_count == 0:
        console.print("[green]All conflicts can be auto-resolved.[/green]\n")
    else:
        console.print(
            f"[yellow]Prepare to resolve {manual_count} conflict(s) manually during merge.[/yellow]\n"
        )


def x_display_conflict_forecast__mutmut_12(
    predictions: list[ConflictPrediction],
    console: Console,
) -> None:
    """Display conflict predictions with Rich formatting.

    Groups predictions into auto-resolvable (status files) and
    manual-required categories for clear user guidance.

    Args:
        predictions: List of ConflictPrediction objects
        console: Rich Console instance for output
    """
    if not predictions:
        console.print("\n[green]No conflicts predicted[/green]\n")
        return

    console.print("\n[bold]Conflict Forecast[/bold]\n")

    auto_resolvable = [p for p in predictions if p.auto_resolvable]
    manual_required = [p for p in predictions if p.auto_resolvable]

    # Summary counts
    total = len(predictions)
    auto_count = len(auto_resolvable)
    manual_count = len(manual_required)

    console.print(f"[dim]Found {total} potential conflict(s): {auto_count} auto-resolvable, {manual_count} manual[/dim]\n")

    # Create table for conflicts
    if manual_required:
        table = Table(show_header=True, header_style="bold yellow")
        table.add_column("File")
        table.add_column("WPs")
        table.add_column("Confidence")

        for pred in manual_required:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps, pred.confidence)

        console.print("[yellow]May require manual resolution:[/yellow]")
        console.print(table)
        console.print()

    if auto_resolvable:
        table = Table(show_header=True, header_style="bold dim")
        table.add_column("Status File")
        table.add_column("WPs")

        for pred in auto_resolvable:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps)

        console.print("[dim]Auto-resolvable (status files):[/dim]")
        console.print(table)
        console.print()

    # Summary guidance
    if manual_count == 0:
        console.print("[green]All conflicts can be auto-resolved.[/green]\n")
    else:
        console.print(
            f"[yellow]Prepare to resolve {manual_count} conflict(s) manually during merge.[/yellow]\n"
        )


def x_display_conflict_forecast__mutmut_13(
    predictions: list[ConflictPrediction],
    console: Console,
) -> None:
    """Display conflict predictions with Rich formatting.

    Groups predictions into auto-resolvable (status files) and
    manual-required categories for clear user guidance.

    Args:
        predictions: List of ConflictPrediction objects
        console: Rich Console instance for output
    """
    if not predictions:
        console.print("\n[green]No conflicts predicted[/green]\n")
        return

    console.print("\n[bold]Conflict Forecast[/bold]\n")

    auto_resolvable = [p for p in predictions if p.auto_resolvable]
    manual_required = [p for p in predictions if not p.auto_resolvable]

    # Summary counts
    total = None
    auto_count = len(auto_resolvable)
    manual_count = len(manual_required)

    console.print(f"[dim]Found {total} potential conflict(s): {auto_count} auto-resolvable, {manual_count} manual[/dim]\n")

    # Create table for conflicts
    if manual_required:
        table = Table(show_header=True, header_style="bold yellow")
        table.add_column("File")
        table.add_column("WPs")
        table.add_column("Confidence")

        for pred in manual_required:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps, pred.confidence)

        console.print("[yellow]May require manual resolution:[/yellow]")
        console.print(table)
        console.print()

    if auto_resolvable:
        table = Table(show_header=True, header_style="bold dim")
        table.add_column("Status File")
        table.add_column("WPs")

        for pred in auto_resolvable:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps)

        console.print("[dim]Auto-resolvable (status files):[/dim]")
        console.print(table)
        console.print()

    # Summary guidance
    if manual_count == 0:
        console.print("[green]All conflicts can be auto-resolved.[/green]\n")
    else:
        console.print(
            f"[yellow]Prepare to resolve {manual_count} conflict(s) manually during merge.[/yellow]\n"
        )


def x_display_conflict_forecast__mutmut_14(
    predictions: list[ConflictPrediction],
    console: Console,
) -> None:
    """Display conflict predictions with Rich formatting.

    Groups predictions into auto-resolvable (status files) and
    manual-required categories for clear user guidance.

    Args:
        predictions: List of ConflictPrediction objects
        console: Rich Console instance for output
    """
    if not predictions:
        console.print("\n[green]No conflicts predicted[/green]\n")
        return

    console.print("\n[bold]Conflict Forecast[/bold]\n")

    auto_resolvable = [p for p in predictions if p.auto_resolvable]
    manual_required = [p for p in predictions if not p.auto_resolvable]

    # Summary counts
    total = len(predictions)
    auto_count = None
    manual_count = len(manual_required)

    console.print(f"[dim]Found {total} potential conflict(s): {auto_count} auto-resolvable, {manual_count} manual[/dim]\n")

    # Create table for conflicts
    if manual_required:
        table = Table(show_header=True, header_style="bold yellow")
        table.add_column("File")
        table.add_column("WPs")
        table.add_column("Confidence")

        for pred in manual_required:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps, pred.confidence)

        console.print("[yellow]May require manual resolution:[/yellow]")
        console.print(table)
        console.print()

    if auto_resolvable:
        table = Table(show_header=True, header_style="bold dim")
        table.add_column("Status File")
        table.add_column("WPs")

        for pred in auto_resolvable:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps)

        console.print("[dim]Auto-resolvable (status files):[/dim]")
        console.print(table)
        console.print()

    # Summary guidance
    if manual_count == 0:
        console.print("[green]All conflicts can be auto-resolved.[/green]\n")
    else:
        console.print(
            f"[yellow]Prepare to resolve {manual_count} conflict(s) manually during merge.[/yellow]\n"
        )


def x_display_conflict_forecast__mutmut_15(
    predictions: list[ConflictPrediction],
    console: Console,
) -> None:
    """Display conflict predictions with Rich formatting.

    Groups predictions into auto-resolvable (status files) and
    manual-required categories for clear user guidance.

    Args:
        predictions: List of ConflictPrediction objects
        console: Rich Console instance for output
    """
    if not predictions:
        console.print("\n[green]No conflicts predicted[/green]\n")
        return

    console.print("\n[bold]Conflict Forecast[/bold]\n")

    auto_resolvable = [p for p in predictions if p.auto_resolvable]
    manual_required = [p for p in predictions if not p.auto_resolvable]

    # Summary counts
    total = len(predictions)
    auto_count = len(auto_resolvable)
    manual_count = None

    console.print(f"[dim]Found {total} potential conflict(s): {auto_count} auto-resolvable, {manual_count} manual[/dim]\n")

    # Create table for conflicts
    if manual_required:
        table = Table(show_header=True, header_style="bold yellow")
        table.add_column("File")
        table.add_column("WPs")
        table.add_column("Confidence")

        for pred in manual_required:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps, pred.confidence)

        console.print("[yellow]May require manual resolution:[/yellow]")
        console.print(table)
        console.print()

    if auto_resolvable:
        table = Table(show_header=True, header_style="bold dim")
        table.add_column("Status File")
        table.add_column("WPs")

        for pred in auto_resolvable:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps)

        console.print("[dim]Auto-resolvable (status files):[/dim]")
        console.print(table)
        console.print()

    # Summary guidance
    if manual_count == 0:
        console.print("[green]All conflicts can be auto-resolved.[/green]\n")
    else:
        console.print(
            f"[yellow]Prepare to resolve {manual_count} conflict(s) manually during merge.[/yellow]\n"
        )


def x_display_conflict_forecast__mutmut_16(
    predictions: list[ConflictPrediction],
    console: Console,
) -> None:
    """Display conflict predictions with Rich formatting.

    Groups predictions into auto-resolvable (status files) and
    manual-required categories for clear user guidance.

    Args:
        predictions: List of ConflictPrediction objects
        console: Rich Console instance for output
    """
    if not predictions:
        console.print("\n[green]No conflicts predicted[/green]\n")
        return

    console.print("\n[bold]Conflict Forecast[/bold]\n")

    auto_resolvable = [p for p in predictions if p.auto_resolvable]
    manual_required = [p for p in predictions if not p.auto_resolvable]

    # Summary counts
    total = len(predictions)
    auto_count = len(auto_resolvable)
    manual_count = len(manual_required)

    console.print(None)

    # Create table for conflicts
    if manual_required:
        table = Table(show_header=True, header_style="bold yellow")
        table.add_column("File")
        table.add_column("WPs")
        table.add_column("Confidence")

        for pred in manual_required:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps, pred.confidence)

        console.print("[yellow]May require manual resolution:[/yellow]")
        console.print(table)
        console.print()

    if auto_resolvable:
        table = Table(show_header=True, header_style="bold dim")
        table.add_column("Status File")
        table.add_column("WPs")

        for pred in auto_resolvable:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps)

        console.print("[dim]Auto-resolvable (status files):[/dim]")
        console.print(table)
        console.print()

    # Summary guidance
    if manual_count == 0:
        console.print("[green]All conflicts can be auto-resolved.[/green]\n")
    else:
        console.print(
            f"[yellow]Prepare to resolve {manual_count} conflict(s) manually during merge.[/yellow]\n"
        )


def x_display_conflict_forecast__mutmut_17(
    predictions: list[ConflictPrediction],
    console: Console,
) -> None:
    """Display conflict predictions with Rich formatting.

    Groups predictions into auto-resolvable (status files) and
    manual-required categories for clear user guidance.

    Args:
        predictions: List of ConflictPrediction objects
        console: Rich Console instance for output
    """
    if not predictions:
        console.print("\n[green]No conflicts predicted[/green]\n")
        return

    console.print("\n[bold]Conflict Forecast[/bold]\n")

    auto_resolvable = [p for p in predictions if p.auto_resolvable]
    manual_required = [p for p in predictions if not p.auto_resolvable]

    # Summary counts
    total = len(predictions)
    auto_count = len(auto_resolvable)
    manual_count = len(manual_required)

    console.print(f"[dim]Found {total} potential conflict(s): {auto_count} auto-resolvable, {manual_count} manual[/dim]\n")

    # Create table for conflicts
    if manual_required:
        table = None
        table.add_column("File")
        table.add_column("WPs")
        table.add_column("Confidence")

        for pred in manual_required:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps, pred.confidence)

        console.print("[yellow]May require manual resolution:[/yellow]")
        console.print(table)
        console.print()

    if auto_resolvable:
        table = Table(show_header=True, header_style="bold dim")
        table.add_column("Status File")
        table.add_column("WPs")

        for pred in auto_resolvable:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps)

        console.print("[dim]Auto-resolvable (status files):[/dim]")
        console.print(table)
        console.print()

    # Summary guidance
    if manual_count == 0:
        console.print("[green]All conflicts can be auto-resolved.[/green]\n")
    else:
        console.print(
            f"[yellow]Prepare to resolve {manual_count} conflict(s) manually during merge.[/yellow]\n"
        )


def x_display_conflict_forecast__mutmut_18(
    predictions: list[ConflictPrediction],
    console: Console,
) -> None:
    """Display conflict predictions with Rich formatting.

    Groups predictions into auto-resolvable (status files) and
    manual-required categories for clear user guidance.

    Args:
        predictions: List of ConflictPrediction objects
        console: Rich Console instance for output
    """
    if not predictions:
        console.print("\n[green]No conflicts predicted[/green]\n")
        return

    console.print("\n[bold]Conflict Forecast[/bold]\n")

    auto_resolvable = [p for p in predictions if p.auto_resolvable]
    manual_required = [p for p in predictions if not p.auto_resolvable]

    # Summary counts
    total = len(predictions)
    auto_count = len(auto_resolvable)
    manual_count = len(manual_required)

    console.print(f"[dim]Found {total} potential conflict(s): {auto_count} auto-resolvable, {manual_count} manual[/dim]\n")

    # Create table for conflicts
    if manual_required:
        table = Table(show_header=None, header_style="bold yellow")
        table.add_column("File")
        table.add_column("WPs")
        table.add_column("Confidence")

        for pred in manual_required:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps, pred.confidence)

        console.print("[yellow]May require manual resolution:[/yellow]")
        console.print(table)
        console.print()

    if auto_resolvable:
        table = Table(show_header=True, header_style="bold dim")
        table.add_column("Status File")
        table.add_column("WPs")

        for pred in auto_resolvable:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps)

        console.print("[dim]Auto-resolvable (status files):[/dim]")
        console.print(table)
        console.print()

    # Summary guidance
    if manual_count == 0:
        console.print("[green]All conflicts can be auto-resolved.[/green]\n")
    else:
        console.print(
            f"[yellow]Prepare to resolve {manual_count} conflict(s) manually during merge.[/yellow]\n"
        )


def x_display_conflict_forecast__mutmut_19(
    predictions: list[ConflictPrediction],
    console: Console,
) -> None:
    """Display conflict predictions with Rich formatting.

    Groups predictions into auto-resolvable (status files) and
    manual-required categories for clear user guidance.

    Args:
        predictions: List of ConflictPrediction objects
        console: Rich Console instance for output
    """
    if not predictions:
        console.print("\n[green]No conflicts predicted[/green]\n")
        return

    console.print("\n[bold]Conflict Forecast[/bold]\n")

    auto_resolvable = [p for p in predictions if p.auto_resolvable]
    manual_required = [p for p in predictions if not p.auto_resolvable]

    # Summary counts
    total = len(predictions)
    auto_count = len(auto_resolvable)
    manual_count = len(manual_required)

    console.print(f"[dim]Found {total} potential conflict(s): {auto_count} auto-resolvable, {manual_count} manual[/dim]\n")

    # Create table for conflicts
    if manual_required:
        table = Table(show_header=True, header_style=None)
        table.add_column("File")
        table.add_column("WPs")
        table.add_column("Confidence")

        for pred in manual_required:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps, pred.confidence)

        console.print("[yellow]May require manual resolution:[/yellow]")
        console.print(table)
        console.print()

    if auto_resolvable:
        table = Table(show_header=True, header_style="bold dim")
        table.add_column("Status File")
        table.add_column("WPs")

        for pred in auto_resolvable:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps)

        console.print("[dim]Auto-resolvable (status files):[/dim]")
        console.print(table)
        console.print()

    # Summary guidance
    if manual_count == 0:
        console.print("[green]All conflicts can be auto-resolved.[/green]\n")
    else:
        console.print(
            f"[yellow]Prepare to resolve {manual_count} conflict(s) manually during merge.[/yellow]\n"
        )


def x_display_conflict_forecast__mutmut_20(
    predictions: list[ConflictPrediction],
    console: Console,
) -> None:
    """Display conflict predictions with Rich formatting.

    Groups predictions into auto-resolvable (status files) and
    manual-required categories for clear user guidance.

    Args:
        predictions: List of ConflictPrediction objects
        console: Rich Console instance for output
    """
    if not predictions:
        console.print("\n[green]No conflicts predicted[/green]\n")
        return

    console.print("\n[bold]Conflict Forecast[/bold]\n")

    auto_resolvable = [p for p in predictions if p.auto_resolvable]
    manual_required = [p for p in predictions if not p.auto_resolvable]

    # Summary counts
    total = len(predictions)
    auto_count = len(auto_resolvable)
    manual_count = len(manual_required)

    console.print(f"[dim]Found {total} potential conflict(s): {auto_count} auto-resolvable, {manual_count} manual[/dim]\n")

    # Create table for conflicts
    if manual_required:
        table = Table(header_style="bold yellow")
        table.add_column("File")
        table.add_column("WPs")
        table.add_column("Confidence")

        for pred in manual_required:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps, pred.confidence)

        console.print("[yellow]May require manual resolution:[/yellow]")
        console.print(table)
        console.print()

    if auto_resolvable:
        table = Table(show_header=True, header_style="bold dim")
        table.add_column("Status File")
        table.add_column("WPs")

        for pred in auto_resolvable:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps)

        console.print("[dim]Auto-resolvable (status files):[/dim]")
        console.print(table)
        console.print()

    # Summary guidance
    if manual_count == 0:
        console.print("[green]All conflicts can be auto-resolved.[/green]\n")
    else:
        console.print(
            f"[yellow]Prepare to resolve {manual_count} conflict(s) manually during merge.[/yellow]\n"
        )


def x_display_conflict_forecast__mutmut_21(
    predictions: list[ConflictPrediction],
    console: Console,
) -> None:
    """Display conflict predictions with Rich formatting.

    Groups predictions into auto-resolvable (status files) and
    manual-required categories for clear user guidance.

    Args:
        predictions: List of ConflictPrediction objects
        console: Rich Console instance for output
    """
    if not predictions:
        console.print("\n[green]No conflicts predicted[/green]\n")
        return

    console.print("\n[bold]Conflict Forecast[/bold]\n")

    auto_resolvable = [p for p in predictions if p.auto_resolvable]
    manual_required = [p for p in predictions if not p.auto_resolvable]

    # Summary counts
    total = len(predictions)
    auto_count = len(auto_resolvable)
    manual_count = len(manual_required)

    console.print(f"[dim]Found {total} potential conflict(s): {auto_count} auto-resolvable, {manual_count} manual[/dim]\n")

    # Create table for conflicts
    if manual_required:
        table = Table(show_header=True, )
        table.add_column("File")
        table.add_column("WPs")
        table.add_column("Confidence")

        for pred in manual_required:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps, pred.confidence)

        console.print("[yellow]May require manual resolution:[/yellow]")
        console.print(table)
        console.print()

    if auto_resolvable:
        table = Table(show_header=True, header_style="bold dim")
        table.add_column("Status File")
        table.add_column("WPs")

        for pred in auto_resolvable:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps)

        console.print("[dim]Auto-resolvable (status files):[/dim]")
        console.print(table)
        console.print()

    # Summary guidance
    if manual_count == 0:
        console.print("[green]All conflicts can be auto-resolved.[/green]\n")
    else:
        console.print(
            f"[yellow]Prepare to resolve {manual_count} conflict(s) manually during merge.[/yellow]\n"
        )


def x_display_conflict_forecast__mutmut_22(
    predictions: list[ConflictPrediction],
    console: Console,
) -> None:
    """Display conflict predictions with Rich formatting.

    Groups predictions into auto-resolvable (status files) and
    manual-required categories for clear user guidance.

    Args:
        predictions: List of ConflictPrediction objects
        console: Rich Console instance for output
    """
    if not predictions:
        console.print("\n[green]No conflicts predicted[/green]\n")
        return

    console.print("\n[bold]Conflict Forecast[/bold]\n")

    auto_resolvable = [p for p in predictions if p.auto_resolvable]
    manual_required = [p for p in predictions if not p.auto_resolvable]

    # Summary counts
    total = len(predictions)
    auto_count = len(auto_resolvable)
    manual_count = len(manual_required)

    console.print(f"[dim]Found {total} potential conflict(s): {auto_count} auto-resolvable, {manual_count} manual[/dim]\n")

    # Create table for conflicts
    if manual_required:
        table = Table(show_header=False, header_style="bold yellow")
        table.add_column("File")
        table.add_column("WPs")
        table.add_column("Confidence")

        for pred in manual_required:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps, pred.confidence)

        console.print("[yellow]May require manual resolution:[/yellow]")
        console.print(table)
        console.print()

    if auto_resolvable:
        table = Table(show_header=True, header_style="bold dim")
        table.add_column("Status File")
        table.add_column("WPs")

        for pred in auto_resolvable:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps)

        console.print("[dim]Auto-resolvable (status files):[/dim]")
        console.print(table)
        console.print()

    # Summary guidance
    if manual_count == 0:
        console.print("[green]All conflicts can be auto-resolved.[/green]\n")
    else:
        console.print(
            f"[yellow]Prepare to resolve {manual_count} conflict(s) manually during merge.[/yellow]\n"
        )


def x_display_conflict_forecast__mutmut_23(
    predictions: list[ConflictPrediction],
    console: Console,
) -> None:
    """Display conflict predictions with Rich formatting.

    Groups predictions into auto-resolvable (status files) and
    manual-required categories for clear user guidance.

    Args:
        predictions: List of ConflictPrediction objects
        console: Rich Console instance for output
    """
    if not predictions:
        console.print("\n[green]No conflicts predicted[/green]\n")
        return

    console.print("\n[bold]Conflict Forecast[/bold]\n")

    auto_resolvable = [p for p in predictions if p.auto_resolvable]
    manual_required = [p for p in predictions if not p.auto_resolvable]

    # Summary counts
    total = len(predictions)
    auto_count = len(auto_resolvable)
    manual_count = len(manual_required)

    console.print(f"[dim]Found {total} potential conflict(s): {auto_count} auto-resolvable, {manual_count} manual[/dim]\n")

    # Create table for conflicts
    if manual_required:
        table = Table(show_header=True, header_style="XXbold yellowXX")
        table.add_column("File")
        table.add_column("WPs")
        table.add_column("Confidence")

        for pred in manual_required:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps, pred.confidence)

        console.print("[yellow]May require manual resolution:[/yellow]")
        console.print(table)
        console.print()

    if auto_resolvable:
        table = Table(show_header=True, header_style="bold dim")
        table.add_column("Status File")
        table.add_column("WPs")

        for pred in auto_resolvable:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps)

        console.print("[dim]Auto-resolvable (status files):[/dim]")
        console.print(table)
        console.print()

    # Summary guidance
    if manual_count == 0:
        console.print("[green]All conflicts can be auto-resolved.[/green]\n")
    else:
        console.print(
            f"[yellow]Prepare to resolve {manual_count} conflict(s) manually during merge.[/yellow]\n"
        )


def x_display_conflict_forecast__mutmut_24(
    predictions: list[ConflictPrediction],
    console: Console,
) -> None:
    """Display conflict predictions with Rich formatting.

    Groups predictions into auto-resolvable (status files) and
    manual-required categories for clear user guidance.

    Args:
        predictions: List of ConflictPrediction objects
        console: Rich Console instance for output
    """
    if not predictions:
        console.print("\n[green]No conflicts predicted[/green]\n")
        return

    console.print("\n[bold]Conflict Forecast[/bold]\n")

    auto_resolvable = [p for p in predictions if p.auto_resolvable]
    manual_required = [p for p in predictions if not p.auto_resolvable]

    # Summary counts
    total = len(predictions)
    auto_count = len(auto_resolvable)
    manual_count = len(manual_required)

    console.print(f"[dim]Found {total} potential conflict(s): {auto_count} auto-resolvable, {manual_count} manual[/dim]\n")

    # Create table for conflicts
    if manual_required:
        table = Table(show_header=True, header_style="BOLD YELLOW")
        table.add_column("File")
        table.add_column("WPs")
        table.add_column("Confidence")

        for pred in manual_required:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps, pred.confidence)

        console.print("[yellow]May require manual resolution:[/yellow]")
        console.print(table)
        console.print()

    if auto_resolvable:
        table = Table(show_header=True, header_style="bold dim")
        table.add_column("Status File")
        table.add_column("WPs")

        for pred in auto_resolvable:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps)

        console.print("[dim]Auto-resolvable (status files):[/dim]")
        console.print(table)
        console.print()

    # Summary guidance
    if manual_count == 0:
        console.print("[green]All conflicts can be auto-resolved.[/green]\n")
    else:
        console.print(
            f"[yellow]Prepare to resolve {manual_count} conflict(s) manually during merge.[/yellow]\n"
        )


def x_display_conflict_forecast__mutmut_25(
    predictions: list[ConflictPrediction],
    console: Console,
) -> None:
    """Display conflict predictions with Rich formatting.

    Groups predictions into auto-resolvable (status files) and
    manual-required categories for clear user guidance.

    Args:
        predictions: List of ConflictPrediction objects
        console: Rich Console instance for output
    """
    if not predictions:
        console.print("\n[green]No conflicts predicted[/green]\n")
        return

    console.print("\n[bold]Conflict Forecast[/bold]\n")

    auto_resolvable = [p for p in predictions if p.auto_resolvable]
    manual_required = [p for p in predictions if not p.auto_resolvable]

    # Summary counts
    total = len(predictions)
    auto_count = len(auto_resolvable)
    manual_count = len(manual_required)

    console.print(f"[dim]Found {total} potential conflict(s): {auto_count} auto-resolvable, {manual_count} manual[/dim]\n")

    # Create table for conflicts
    if manual_required:
        table = Table(show_header=True, header_style="bold yellow")
        table.add_column(None)
        table.add_column("WPs")
        table.add_column("Confidence")

        for pred in manual_required:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps, pred.confidence)

        console.print("[yellow]May require manual resolution:[/yellow]")
        console.print(table)
        console.print()

    if auto_resolvable:
        table = Table(show_header=True, header_style="bold dim")
        table.add_column("Status File")
        table.add_column("WPs")

        for pred in auto_resolvable:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps)

        console.print("[dim]Auto-resolvable (status files):[/dim]")
        console.print(table)
        console.print()

    # Summary guidance
    if manual_count == 0:
        console.print("[green]All conflicts can be auto-resolved.[/green]\n")
    else:
        console.print(
            f"[yellow]Prepare to resolve {manual_count} conflict(s) manually during merge.[/yellow]\n"
        )


def x_display_conflict_forecast__mutmut_26(
    predictions: list[ConflictPrediction],
    console: Console,
) -> None:
    """Display conflict predictions with Rich formatting.

    Groups predictions into auto-resolvable (status files) and
    manual-required categories for clear user guidance.

    Args:
        predictions: List of ConflictPrediction objects
        console: Rich Console instance for output
    """
    if not predictions:
        console.print("\n[green]No conflicts predicted[/green]\n")
        return

    console.print("\n[bold]Conflict Forecast[/bold]\n")

    auto_resolvable = [p for p in predictions if p.auto_resolvable]
    manual_required = [p for p in predictions if not p.auto_resolvable]

    # Summary counts
    total = len(predictions)
    auto_count = len(auto_resolvable)
    manual_count = len(manual_required)

    console.print(f"[dim]Found {total} potential conflict(s): {auto_count} auto-resolvable, {manual_count} manual[/dim]\n")

    # Create table for conflicts
    if manual_required:
        table = Table(show_header=True, header_style="bold yellow")
        table.add_column("XXFileXX")
        table.add_column("WPs")
        table.add_column("Confidence")

        for pred in manual_required:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps, pred.confidence)

        console.print("[yellow]May require manual resolution:[/yellow]")
        console.print(table)
        console.print()

    if auto_resolvable:
        table = Table(show_header=True, header_style="bold dim")
        table.add_column("Status File")
        table.add_column("WPs")

        for pred in auto_resolvable:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps)

        console.print("[dim]Auto-resolvable (status files):[/dim]")
        console.print(table)
        console.print()

    # Summary guidance
    if manual_count == 0:
        console.print("[green]All conflicts can be auto-resolved.[/green]\n")
    else:
        console.print(
            f"[yellow]Prepare to resolve {manual_count} conflict(s) manually during merge.[/yellow]\n"
        )


def x_display_conflict_forecast__mutmut_27(
    predictions: list[ConflictPrediction],
    console: Console,
) -> None:
    """Display conflict predictions with Rich formatting.

    Groups predictions into auto-resolvable (status files) and
    manual-required categories for clear user guidance.

    Args:
        predictions: List of ConflictPrediction objects
        console: Rich Console instance for output
    """
    if not predictions:
        console.print("\n[green]No conflicts predicted[/green]\n")
        return

    console.print("\n[bold]Conflict Forecast[/bold]\n")

    auto_resolvable = [p for p in predictions if p.auto_resolvable]
    manual_required = [p for p in predictions if not p.auto_resolvable]

    # Summary counts
    total = len(predictions)
    auto_count = len(auto_resolvable)
    manual_count = len(manual_required)

    console.print(f"[dim]Found {total} potential conflict(s): {auto_count} auto-resolvable, {manual_count} manual[/dim]\n")

    # Create table for conflicts
    if manual_required:
        table = Table(show_header=True, header_style="bold yellow")
        table.add_column("file")
        table.add_column("WPs")
        table.add_column("Confidence")

        for pred in manual_required:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps, pred.confidence)

        console.print("[yellow]May require manual resolution:[/yellow]")
        console.print(table)
        console.print()

    if auto_resolvable:
        table = Table(show_header=True, header_style="bold dim")
        table.add_column("Status File")
        table.add_column("WPs")

        for pred in auto_resolvable:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps)

        console.print("[dim]Auto-resolvable (status files):[/dim]")
        console.print(table)
        console.print()

    # Summary guidance
    if manual_count == 0:
        console.print("[green]All conflicts can be auto-resolved.[/green]\n")
    else:
        console.print(
            f"[yellow]Prepare to resolve {manual_count} conflict(s) manually during merge.[/yellow]\n"
        )


def x_display_conflict_forecast__mutmut_28(
    predictions: list[ConflictPrediction],
    console: Console,
) -> None:
    """Display conflict predictions with Rich formatting.

    Groups predictions into auto-resolvable (status files) and
    manual-required categories for clear user guidance.

    Args:
        predictions: List of ConflictPrediction objects
        console: Rich Console instance for output
    """
    if not predictions:
        console.print("\n[green]No conflicts predicted[/green]\n")
        return

    console.print("\n[bold]Conflict Forecast[/bold]\n")

    auto_resolvable = [p for p in predictions if p.auto_resolvable]
    manual_required = [p for p in predictions if not p.auto_resolvable]

    # Summary counts
    total = len(predictions)
    auto_count = len(auto_resolvable)
    manual_count = len(manual_required)

    console.print(f"[dim]Found {total} potential conflict(s): {auto_count} auto-resolvable, {manual_count} manual[/dim]\n")

    # Create table for conflicts
    if manual_required:
        table = Table(show_header=True, header_style="bold yellow")
        table.add_column("FILE")
        table.add_column("WPs")
        table.add_column("Confidence")

        for pred in manual_required:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps, pred.confidence)

        console.print("[yellow]May require manual resolution:[/yellow]")
        console.print(table)
        console.print()

    if auto_resolvable:
        table = Table(show_header=True, header_style="bold dim")
        table.add_column("Status File")
        table.add_column("WPs")

        for pred in auto_resolvable:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps)

        console.print("[dim]Auto-resolvable (status files):[/dim]")
        console.print(table)
        console.print()

    # Summary guidance
    if manual_count == 0:
        console.print("[green]All conflicts can be auto-resolved.[/green]\n")
    else:
        console.print(
            f"[yellow]Prepare to resolve {manual_count} conflict(s) manually during merge.[/yellow]\n"
        )


def x_display_conflict_forecast__mutmut_29(
    predictions: list[ConflictPrediction],
    console: Console,
) -> None:
    """Display conflict predictions with Rich formatting.

    Groups predictions into auto-resolvable (status files) and
    manual-required categories for clear user guidance.

    Args:
        predictions: List of ConflictPrediction objects
        console: Rich Console instance for output
    """
    if not predictions:
        console.print("\n[green]No conflicts predicted[/green]\n")
        return

    console.print("\n[bold]Conflict Forecast[/bold]\n")

    auto_resolvable = [p for p in predictions if p.auto_resolvable]
    manual_required = [p for p in predictions if not p.auto_resolvable]

    # Summary counts
    total = len(predictions)
    auto_count = len(auto_resolvable)
    manual_count = len(manual_required)

    console.print(f"[dim]Found {total} potential conflict(s): {auto_count} auto-resolvable, {manual_count} manual[/dim]\n")

    # Create table for conflicts
    if manual_required:
        table = Table(show_header=True, header_style="bold yellow")
        table.add_column("File")
        table.add_column(None)
        table.add_column("Confidence")

        for pred in manual_required:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps, pred.confidence)

        console.print("[yellow]May require manual resolution:[/yellow]")
        console.print(table)
        console.print()

    if auto_resolvable:
        table = Table(show_header=True, header_style="bold dim")
        table.add_column("Status File")
        table.add_column("WPs")

        for pred in auto_resolvable:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps)

        console.print("[dim]Auto-resolvable (status files):[/dim]")
        console.print(table)
        console.print()

    # Summary guidance
    if manual_count == 0:
        console.print("[green]All conflicts can be auto-resolved.[/green]\n")
    else:
        console.print(
            f"[yellow]Prepare to resolve {manual_count} conflict(s) manually during merge.[/yellow]\n"
        )


def x_display_conflict_forecast__mutmut_30(
    predictions: list[ConflictPrediction],
    console: Console,
) -> None:
    """Display conflict predictions with Rich formatting.

    Groups predictions into auto-resolvable (status files) and
    manual-required categories for clear user guidance.

    Args:
        predictions: List of ConflictPrediction objects
        console: Rich Console instance for output
    """
    if not predictions:
        console.print("\n[green]No conflicts predicted[/green]\n")
        return

    console.print("\n[bold]Conflict Forecast[/bold]\n")

    auto_resolvable = [p for p in predictions if p.auto_resolvable]
    manual_required = [p for p in predictions if not p.auto_resolvable]

    # Summary counts
    total = len(predictions)
    auto_count = len(auto_resolvable)
    manual_count = len(manual_required)

    console.print(f"[dim]Found {total} potential conflict(s): {auto_count} auto-resolvable, {manual_count} manual[/dim]\n")

    # Create table for conflicts
    if manual_required:
        table = Table(show_header=True, header_style="bold yellow")
        table.add_column("File")
        table.add_column("XXWPsXX")
        table.add_column("Confidence")

        for pred in manual_required:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps, pred.confidence)

        console.print("[yellow]May require manual resolution:[/yellow]")
        console.print(table)
        console.print()

    if auto_resolvable:
        table = Table(show_header=True, header_style="bold dim")
        table.add_column("Status File")
        table.add_column("WPs")

        for pred in auto_resolvable:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps)

        console.print("[dim]Auto-resolvable (status files):[/dim]")
        console.print(table)
        console.print()

    # Summary guidance
    if manual_count == 0:
        console.print("[green]All conflicts can be auto-resolved.[/green]\n")
    else:
        console.print(
            f"[yellow]Prepare to resolve {manual_count} conflict(s) manually during merge.[/yellow]\n"
        )


def x_display_conflict_forecast__mutmut_31(
    predictions: list[ConflictPrediction],
    console: Console,
) -> None:
    """Display conflict predictions with Rich formatting.

    Groups predictions into auto-resolvable (status files) and
    manual-required categories for clear user guidance.

    Args:
        predictions: List of ConflictPrediction objects
        console: Rich Console instance for output
    """
    if not predictions:
        console.print("\n[green]No conflicts predicted[/green]\n")
        return

    console.print("\n[bold]Conflict Forecast[/bold]\n")

    auto_resolvable = [p for p in predictions if p.auto_resolvable]
    manual_required = [p for p in predictions if not p.auto_resolvable]

    # Summary counts
    total = len(predictions)
    auto_count = len(auto_resolvable)
    manual_count = len(manual_required)

    console.print(f"[dim]Found {total} potential conflict(s): {auto_count} auto-resolvable, {manual_count} manual[/dim]\n")

    # Create table for conflicts
    if manual_required:
        table = Table(show_header=True, header_style="bold yellow")
        table.add_column("File")
        table.add_column("wps")
        table.add_column("Confidence")

        for pred in manual_required:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps, pred.confidence)

        console.print("[yellow]May require manual resolution:[/yellow]")
        console.print(table)
        console.print()

    if auto_resolvable:
        table = Table(show_header=True, header_style="bold dim")
        table.add_column("Status File")
        table.add_column("WPs")

        for pred in auto_resolvable:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps)

        console.print("[dim]Auto-resolvable (status files):[/dim]")
        console.print(table)
        console.print()

    # Summary guidance
    if manual_count == 0:
        console.print("[green]All conflicts can be auto-resolved.[/green]\n")
    else:
        console.print(
            f"[yellow]Prepare to resolve {manual_count} conflict(s) manually during merge.[/yellow]\n"
        )


def x_display_conflict_forecast__mutmut_32(
    predictions: list[ConflictPrediction],
    console: Console,
) -> None:
    """Display conflict predictions with Rich formatting.

    Groups predictions into auto-resolvable (status files) and
    manual-required categories for clear user guidance.

    Args:
        predictions: List of ConflictPrediction objects
        console: Rich Console instance for output
    """
    if not predictions:
        console.print("\n[green]No conflicts predicted[/green]\n")
        return

    console.print("\n[bold]Conflict Forecast[/bold]\n")

    auto_resolvable = [p for p in predictions if p.auto_resolvable]
    manual_required = [p for p in predictions if not p.auto_resolvable]

    # Summary counts
    total = len(predictions)
    auto_count = len(auto_resolvable)
    manual_count = len(manual_required)

    console.print(f"[dim]Found {total} potential conflict(s): {auto_count} auto-resolvable, {manual_count} manual[/dim]\n")

    # Create table for conflicts
    if manual_required:
        table = Table(show_header=True, header_style="bold yellow")
        table.add_column("File")
        table.add_column("WPS")
        table.add_column("Confidence")

        for pred in manual_required:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps, pred.confidence)

        console.print("[yellow]May require manual resolution:[/yellow]")
        console.print(table)
        console.print()

    if auto_resolvable:
        table = Table(show_header=True, header_style="bold dim")
        table.add_column("Status File")
        table.add_column("WPs")

        for pred in auto_resolvable:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps)

        console.print("[dim]Auto-resolvable (status files):[/dim]")
        console.print(table)
        console.print()

    # Summary guidance
    if manual_count == 0:
        console.print("[green]All conflicts can be auto-resolved.[/green]\n")
    else:
        console.print(
            f"[yellow]Prepare to resolve {manual_count} conflict(s) manually during merge.[/yellow]\n"
        )


def x_display_conflict_forecast__mutmut_33(
    predictions: list[ConflictPrediction],
    console: Console,
) -> None:
    """Display conflict predictions with Rich formatting.

    Groups predictions into auto-resolvable (status files) and
    manual-required categories for clear user guidance.

    Args:
        predictions: List of ConflictPrediction objects
        console: Rich Console instance for output
    """
    if not predictions:
        console.print("\n[green]No conflicts predicted[/green]\n")
        return

    console.print("\n[bold]Conflict Forecast[/bold]\n")

    auto_resolvable = [p for p in predictions if p.auto_resolvable]
    manual_required = [p for p in predictions if not p.auto_resolvable]

    # Summary counts
    total = len(predictions)
    auto_count = len(auto_resolvable)
    manual_count = len(manual_required)

    console.print(f"[dim]Found {total} potential conflict(s): {auto_count} auto-resolvable, {manual_count} manual[/dim]\n")

    # Create table for conflicts
    if manual_required:
        table = Table(show_header=True, header_style="bold yellow")
        table.add_column("File")
        table.add_column("WPs")
        table.add_column(None)

        for pred in manual_required:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps, pred.confidence)

        console.print("[yellow]May require manual resolution:[/yellow]")
        console.print(table)
        console.print()

    if auto_resolvable:
        table = Table(show_header=True, header_style="bold dim")
        table.add_column("Status File")
        table.add_column("WPs")

        for pred in auto_resolvable:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps)

        console.print("[dim]Auto-resolvable (status files):[/dim]")
        console.print(table)
        console.print()

    # Summary guidance
    if manual_count == 0:
        console.print("[green]All conflicts can be auto-resolved.[/green]\n")
    else:
        console.print(
            f"[yellow]Prepare to resolve {manual_count} conflict(s) manually during merge.[/yellow]\n"
        )


def x_display_conflict_forecast__mutmut_34(
    predictions: list[ConflictPrediction],
    console: Console,
) -> None:
    """Display conflict predictions with Rich formatting.

    Groups predictions into auto-resolvable (status files) and
    manual-required categories for clear user guidance.

    Args:
        predictions: List of ConflictPrediction objects
        console: Rich Console instance for output
    """
    if not predictions:
        console.print("\n[green]No conflicts predicted[/green]\n")
        return

    console.print("\n[bold]Conflict Forecast[/bold]\n")

    auto_resolvable = [p for p in predictions if p.auto_resolvable]
    manual_required = [p for p in predictions if not p.auto_resolvable]

    # Summary counts
    total = len(predictions)
    auto_count = len(auto_resolvable)
    manual_count = len(manual_required)

    console.print(f"[dim]Found {total} potential conflict(s): {auto_count} auto-resolvable, {manual_count} manual[/dim]\n")

    # Create table for conflicts
    if manual_required:
        table = Table(show_header=True, header_style="bold yellow")
        table.add_column("File")
        table.add_column("WPs")
        table.add_column("XXConfidenceXX")

        for pred in manual_required:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps, pred.confidence)

        console.print("[yellow]May require manual resolution:[/yellow]")
        console.print(table)
        console.print()

    if auto_resolvable:
        table = Table(show_header=True, header_style="bold dim")
        table.add_column("Status File")
        table.add_column("WPs")

        for pred in auto_resolvable:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps)

        console.print("[dim]Auto-resolvable (status files):[/dim]")
        console.print(table)
        console.print()

    # Summary guidance
    if manual_count == 0:
        console.print("[green]All conflicts can be auto-resolved.[/green]\n")
    else:
        console.print(
            f"[yellow]Prepare to resolve {manual_count} conflict(s) manually during merge.[/yellow]\n"
        )


def x_display_conflict_forecast__mutmut_35(
    predictions: list[ConflictPrediction],
    console: Console,
) -> None:
    """Display conflict predictions with Rich formatting.

    Groups predictions into auto-resolvable (status files) and
    manual-required categories for clear user guidance.

    Args:
        predictions: List of ConflictPrediction objects
        console: Rich Console instance for output
    """
    if not predictions:
        console.print("\n[green]No conflicts predicted[/green]\n")
        return

    console.print("\n[bold]Conflict Forecast[/bold]\n")

    auto_resolvable = [p for p in predictions if p.auto_resolvable]
    manual_required = [p for p in predictions if not p.auto_resolvable]

    # Summary counts
    total = len(predictions)
    auto_count = len(auto_resolvable)
    manual_count = len(manual_required)

    console.print(f"[dim]Found {total} potential conflict(s): {auto_count} auto-resolvable, {manual_count} manual[/dim]\n")

    # Create table for conflicts
    if manual_required:
        table = Table(show_header=True, header_style="bold yellow")
        table.add_column("File")
        table.add_column("WPs")
        table.add_column("confidence")

        for pred in manual_required:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps, pred.confidence)

        console.print("[yellow]May require manual resolution:[/yellow]")
        console.print(table)
        console.print()

    if auto_resolvable:
        table = Table(show_header=True, header_style="bold dim")
        table.add_column("Status File")
        table.add_column("WPs")

        for pred in auto_resolvable:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps)

        console.print("[dim]Auto-resolvable (status files):[/dim]")
        console.print(table)
        console.print()

    # Summary guidance
    if manual_count == 0:
        console.print("[green]All conflicts can be auto-resolved.[/green]\n")
    else:
        console.print(
            f"[yellow]Prepare to resolve {manual_count} conflict(s) manually during merge.[/yellow]\n"
        )


def x_display_conflict_forecast__mutmut_36(
    predictions: list[ConflictPrediction],
    console: Console,
) -> None:
    """Display conflict predictions with Rich formatting.

    Groups predictions into auto-resolvable (status files) and
    manual-required categories for clear user guidance.

    Args:
        predictions: List of ConflictPrediction objects
        console: Rich Console instance for output
    """
    if not predictions:
        console.print("\n[green]No conflicts predicted[/green]\n")
        return

    console.print("\n[bold]Conflict Forecast[/bold]\n")

    auto_resolvable = [p for p in predictions if p.auto_resolvable]
    manual_required = [p for p in predictions if not p.auto_resolvable]

    # Summary counts
    total = len(predictions)
    auto_count = len(auto_resolvable)
    manual_count = len(manual_required)

    console.print(f"[dim]Found {total} potential conflict(s): {auto_count} auto-resolvable, {manual_count} manual[/dim]\n")

    # Create table for conflicts
    if manual_required:
        table = Table(show_header=True, header_style="bold yellow")
        table.add_column("File")
        table.add_column("WPs")
        table.add_column("CONFIDENCE")

        for pred in manual_required:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps, pred.confidence)

        console.print("[yellow]May require manual resolution:[/yellow]")
        console.print(table)
        console.print()

    if auto_resolvable:
        table = Table(show_header=True, header_style="bold dim")
        table.add_column("Status File")
        table.add_column("WPs")

        for pred in auto_resolvable:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps)

        console.print("[dim]Auto-resolvable (status files):[/dim]")
        console.print(table)
        console.print()

    # Summary guidance
    if manual_count == 0:
        console.print("[green]All conflicts can be auto-resolved.[/green]\n")
    else:
        console.print(
            f"[yellow]Prepare to resolve {manual_count} conflict(s) manually during merge.[/yellow]\n"
        )


def x_display_conflict_forecast__mutmut_37(
    predictions: list[ConflictPrediction],
    console: Console,
) -> None:
    """Display conflict predictions with Rich formatting.

    Groups predictions into auto-resolvable (status files) and
    manual-required categories for clear user guidance.

    Args:
        predictions: List of ConflictPrediction objects
        console: Rich Console instance for output
    """
    if not predictions:
        console.print("\n[green]No conflicts predicted[/green]\n")
        return

    console.print("\n[bold]Conflict Forecast[/bold]\n")

    auto_resolvable = [p for p in predictions if p.auto_resolvable]
    manual_required = [p for p in predictions if not p.auto_resolvable]

    # Summary counts
    total = len(predictions)
    auto_count = len(auto_resolvable)
    manual_count = len(manual_required)

    console.print(f"[dim]Found {total} potential conflict(s): {auto_count} auto-resolvable, {manual_count} manual[/dim]\n")

    # Create table for conflicts
    if manual_required:
        table = Table(show_header=True, header_style="bold yellow")
        table.add_column("File")
        table.add_column("WPs")
        table.add_column("Confidence")

        for pred in manual_required:
            wps = None
            table.add_row(pred.file_path, wps, pred.confidence)

        console.print("[yellow]May require manual resolution:[/yellow]")
        console.print(table)
        console.print()

    if auto_resolvable:
        table = Table(show_header=True, header_style="bold dim")
        table.add_column("Status File")
        table.add_column("WPs")

        for pred in auto_resolvable:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps)

        console.print("[dim]Auto-resolvable (status files):[/dim]")
        console.print(table)
        console.print()

    # Summary guidance
    if manual_count == 0:
        console.print("[green]All conflicts can be auto-resolved.[/green]\n")
    else:
        console.print(
            f"[yellow]Prepare to resolve {manual_count} conflict(s) manually during merge.[/yellow]\n"
        )


def x_display_conflict_forecast__mutmut_38(
    predictions: list[ConflictPrediction],
    console: Console,
) -> None:
    """Display conflict predictions with Rich formatting.

    Groups predictions into auto-resolvable (status files) and
    manual-required categories for clear user guidance.

    Args:
        predictions: List of ConflictPrediction objects
        console: Rich Console instance for output
    """
    if not predictions:
        console.print("\n[green]No conflicts predicted[/green]\n")
        return

    console.print("\n[bold]Conflict Forecast[/bold]\n")

    auto_resolvable = [p for p in predictions if p.auto_resolvable]
    manual_required = [p for p in predictions if not p.auto_resolvable]

    # Summary counts
    total = len(predictions)
    auto_count = len(auto_resolvable)
    manual_count = len(manual_required)

    console.print(f"[dim]Found {total} potential conflict(s): {auto_count} auto-resolvable, {manual_count} manual[/dim]\n")

    # Create table for conflicts
    if manual_required:
        table = Table(show_header=True, header_style="bold yellow")
        table.add_column("File")
        table.add_column("WPs")
        table.add_column("Confidence")

        for pred in manual_required:
            wps = ", ".join(None)
            table.add_row(pred.file_path, wps, pred.confidence)

        console.print("[yellow]May require manual resolution:[/yellow]")
        console.print(table)
        console.print()

    if auto_resolvable:
        table = Table(show_header=True, header_style="bold dim")
        table.add_column("Status File")
        table.add_column("WPs")

        for pred in auto_resolvable:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps)

        console.print("[dim]Auto-resolvable (status files):[/dim]")
        console.print(table)
        console.print()

    # Summary guidance
    if manual_count == 0:
        console.print("[green]All conflicts can be auto-resolved.[/green]\n")
    else:
        console.print(
            f"[yellow]Prepare to resolve {manual_count} conflict(s) manually during merge.[/yellow]\n"
        )


def x_display_conflict_forecast__mutmut_39(
    predictions: list[ConflictPrediction],
    console: Console,
) -> None:
    """Display conflict predictions with Rich formatting.

    Groups predictions into auto-resolvable (status files) and
    manual-required categories for clear user guidance.

    Args:
        predictions: List of ConflictPrediction objects
        console: Rich Console instance for output
    """
    if not predictions:
        console.print("\n[green]No conflicts predicted[/green]\n")
        return

    console.print("\n[bold]Conflict Forecast[/bold]\n")

    auto_resolvable = [p for p in predictions if p.auto_resolvable]
    manual_required = [p for p in predictions if not p.auto_resolvable]

    # Summary counts
    total = len(predictions)
    auto_count = len(auto_resolvable)
    manual_count = len(manual_required)

    console.print(f"[dim]Found {total} potential conflict(s): {auto_count} auto-resolvable, {manual_count} manual[/dim]\n")

    # Create table for conflicts
    if manual_required:
        table = Table(show_header=True, header_style="bold yellow")
        table.add_column("File")
        table.add_column("WPs")
        table.add_column("Confidence")

        for pred in manual_required:
            wps = "XX, XX".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps, pred.confidence)

        console.print("[yellow]May require manual resolution:[/yellow]")
        console.print(table)
        console.print()

    if auto_resolvable:
        table = Table(show_header=True, header_style="bold dim")
        table.add_column("Status File")
        table.add_column("WPs")

        for pred in auto_resolvable:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps)

        console.print("[dim]Auto-resolvable (status files):[/dim]")
        console.print(table)
        console.print()

    # Summary guidance
    if manual_count == 0:
        console.print("[green]All conflicts can be auto-resolved.[/green]\n")
    else:
        console.print(
            f"[yellow]Prepare to resolve {manual_count} conflict(s) manually during merge.[/yellow]\n"
        )


def x_display_conflict_forecast__mutmut_40(
    predictions: list[ConflictPrediction],
    console: Console,
) -> None:
    """Display conflict predictions with Rich formatting.

    Groups predictions into auto-resolvable (status files) and
    manual-required categories for clear user guidance.

    Args:
        predictions: List of ConflictPrediction objects
        console: Rich Console instance for output
    """
    if not predictions:
        console.print("\n[green]No conflicts predicted[/green]\n")
        return

    console.print("\n[bold]Conflict Forecast[/bold]\n")

    auto_resolvable = [p for p in predictions if p.auto_resolvable]
    manual_required = [p for p in predictions if not p.auto_resolvable]

    # Summary counts
    total = len(predictions)
    auto_count = len(auto_resolvable)
    manual_count = len(manual_required)

    console.print(f"[dim]Found {total} potential conflict(s): {auto_count} auto-resolvable, {manual_count} manual[/dim]\n")

    # Create table for conflicts
    if manual_required:
        table = Table(show_header=True, header_style="bold yellow")
        table.add_column("File")
        table.add_column("WPs")
        table.add_column("Confidence")

        for pred in manual_required:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(None, wps, pred.confidence)

        console.print("[yellow]May require manual resolution:[/yellow]")
        console.print(table)
        console.print()

    if auto_resolvable:
        table = Table(show_header=True, header_style="bold dim")
        table.add_column("Status File")
        table.add_column("WPs")

        for pred in auto_resolvable:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps)

        console.print("[dim]Auto-resolvable (status files):[/dim]")
        console.print(table)
        console.print()

    # Summary guidance
    if manual_count == 0:
        console.print("[green]All conflicts can be auto-resolved.[/green]\n")
    else:
        console.print(
            f"[yellow]Prepare to resolve {manual_count} conflict(s) manually during merge.[/yellow]\n"
        )


def x_display_conflict_forecast__mutmut_41(
    predictions: list[ConflictPrediction],
    console: Console,
) -> None:
    """Display conflict predictions with Rich formatting.

    Groups predictions into auto-resolvable (status files) and
    manual-required categories for clear user guidance.

    Args:
        predictions: List of ConflictPrediction objects
        console: Rich Console instance for output
    """
    if not predictions:
        console.print("\n[green]No conflicts predicted[/green]\n")
        return

    console.print("\n[bold]Conflict Forecast[/bold]\n")

    auto_resolvable = [p for p in predictions if p.auto_resolvable]
    manual_required = [p for p in predictions if not p.auto_resolvable]

    # Summary counts
    total = len(predictions)
    auto_count = len(auto_resolvable)
    manual_count = len(manual_required)

    console.print(f"[dim]Found {total} potential conflict(s): {auto_count} auto-resolvable, {manual_count} manual[/dim]\n")

    # Create table for conflicts
    if manual_required:
        table = Table(show_header=True, header_style="bold yellow")
        table.add_column("File")
        table.add_column("WPs")
        table.add_column("Confidence")

        for pred in manual_required:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, None, pred.confidence)

        console.print("[yellow]May require manual resolution:[/yellow]")
        console.print(table)
        console.print()

    if auto_resolvable:
        table = Table(show_header=True, header_style="bold dim")
        table.add_column("Status File")
        table.add_column("WPs")

        for pred in auto_resolvable:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps)

        console.print("[dim]Auto-resolvable (status files):[/dim]")
        console.print(table)
        console.print()

    # Summary guidance
    if manual_count == 0:
        console.print("[green]All conflicts can be auto-resolved.[/green]\n")
    else:
        console.print(
            f"[yellow]Prepare to resolve {manual_count} conflict(s) manually during merge.[/yellow]\n"
        )


def x_display_conflict_forecast__mutmut_42(
    predictions: list[ConflictPrediction],
    console: Console,
) -> None:
    """Display conflict predictions with Rich formatting.

    Groups predictions into auto-resolvable (status files) and
    manual-required categories for clear user guidance.

    Args:
        predictions: List of ConflictPrediction objects
        console: Rich Console instance for output
    """
    if not predictions:
        console.print("\n[green]No conflicts predicted[/green]\n")
        return

    console.print("\n[bold]Conflict Forecast[/bold]\n")

    auto_resolvable = [p for p in predictions if p.auto_resolvable]
    manual_required = [p for p in predictions if not p.auto_resolvable]

    # Summary counts
    total = len(predictions)
    auto_count = len(auto_resolvable)
    manual_count = len(manual_required)

    console.print(f"[dim]Found {total} potential conflict(s): {auto_count} auto-resolvable, {manual_count} manual[/dim]\n")

    # Create table for conflicts
    if manual_required:
        table = Table(show_header=True, header_style="bold yellow")
        table.add_column("File")
        table.add_column("WPs")
        table.add_column("Confidence")

        for pred in manual_required:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps, None)

        console.print("[yellow]May require manual resolution:[/yellow]")
        console.print(table)
        console.print()

    if auto_resolvable:
        table = Table(show_header=True, header_style="bold dim")
        table.add_column("Status File")
        table.add_column("WPs")

        for pred in auto_resolvable:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps)

        console.print("[dim]Auto-resolvable (status files):[/dim]")
        console.print(table)
        console.print()

    # Summary guidance
    if manual_count == 0:
        console.print("[green]All conflicts can be auto-resolved.[/green]\n")
    else:
        console.print(
            f"[yellow]Prepare to resolve {manual_count} conflict(s) manually during merge.[/yellow]\n"
        )


def x_display_conflict_forecast__mutmut_43(
    predictions: list[ConflictPrediction],
    console: Console,
) -> None:
    """Display conflict predictions with Rich formatting.

    Groups predictions into auto-resolvable (status files) and
    manual-required categories for clear user guidance.

    Args:
        predictions: List of ConflictPrediction objects
        console: Rich Console instance for output
    """
    if not predictions:
        console.print("\n[green]No conflicts predicted[/green]\n")
        return

    console.print("\n[bold]Conflict Forecast[/bold]\n")

    auto_resolvable = [p for p in predictions if p.auto_resolvable]
    manual_required = [p for p in predictions if not p.auto_resolvable]

    # Summary counts
    total = len(predictions)
    auto_count = len(auto_resolvable)
    manual_count = len(manual_required)

    console.print(f"[dim]Found {total} potential conflict(s): {auto_count} auto-resolvable, {manual_count} manual[/dim]\n")

    # Create table for conflicts
    if manual_required:
        table = Table(show_header=True, header_style="bold yellow")
        table.add_column("File")
        table.add_column("WPs")
        table.add_column("Confidence")

        for pred in manual_required:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(wps, pred.confidence)

        console.print("[yellow]May require manual resolution:[/yellow]")
        console.print(table)
        console.print()

    if auto_resolvable:
        table = Table(show_header=True, header_style="bold dim")
        table.add_column("Status File")
        table.add_column("WPs")

        for pred in auto_resolvable:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps)

        console.print("[dim]Auto-resolvable (status files):[/dim]")
        console.print(table)
        console.print()

    # Summary guidance
    if manual_count == 0:
        console.print("[green]All conflicts can be auto-resolved.[/green]\n")
    else:
        console.print(
            f"[yellow]Prepare to resolve {manual_count} conflict(s) manually during merge.[/yellow]\n"
        )


def x_display_conflict_forecast__mutmut_44(
    predictions: list[ConflictPrediction],
    console: Console,
) -> None:
    """Display conflict predictions with Rich formatting.

    Groups predictions into auto-resolvable (status files) and
    manual-required categories for clear user guidance.

    Args:
        predictions: List of ConflictPrediction objects
        console: Rich Console instance for output
    """
    if not predictions:
        console.print("\n[green]No conflicts predicted[/green]\n")
        return

    console.print("\n[bold]Conflict Forecast[/bold]\n")

    auto_resolvable = [p for p in predictions if p.auto_resolvable]
    manual_required = [p for p in predictions if not p.auto_resolvable]

    # Summary counts
    total = len(predictions)
    auto_count = len(auto_resolvable)
    manual_count = len(manual_required)

    console.print(f"[dim]Found {total} potential conflict(s): {auto_count} auto-resolvable, {manual_count} manual[/dim]\n")

    # Create table for conflicts
    if manual_required:
        table = Table(show_header=True, header_style="bold yellow")
        table.add_column("File")
        table.add_column("WPs")
        table.add_column("Confidence")

        for pred in manual_required:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, pred.confidence)

        console.print("[yellow]May require manual resolution:[/yellow]")
        console.print(table)
        console.print()

    if auto_resolvable:
        table = Table(show_header=True, header_style="bold dim")
        table.add_column("Status File")
        table.add_column("WPs")

        for pred in auto_resolvable:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps)

        console.print("[dim]Auto-resolvable (status files):[/dim]")
        console.print(table)
        console.print()

    # Summary guidance
    if manual_count == 0:
        console.print("[green]All conflicts can be auto-resolved.[/green]\n")
    else:
        console.print(
            f"[yellow]Prepare to resolve {manual_count} conflict(s) manually during merge.[/yellow]\n"
        )


def x_display_conflict_forecast__mutmut_45(
    predictions: list[ConflictPrediction],
    console: Console,
) -> None:
    """Display conflict predictions with Rich formatting.

    Groups predictions into auto-resolvable (status files) and
    manual-required categories for clear user guidance.

    Args:
        predictions: List of ConflictPrediction objects
        console: Rich Console instance for output
    """
    if not predictions:
        console.print("\n[green]No conflicts predicted[/green]\n")
        return

    console.print("\n[bold]Conflict Forecast[/bold]\n")

    auto_resolvable = [p for p in predictions if p.auto_resolvable]
    manual_required = [p for p in predictions if not p.auto_resolvable]

    # Summary counts
    total = len(predictions)
    auto_count = len(auto_resolvable)
    manual_count = len(manual_required)

    console.print(f"[dim]Found {total} potential conflict(s): {auto_count} auto-resolvable, {manual_count} manual[/dim]\n")

    # Create table for conflicts
    if manual_required:
        table = Table(show_header=True, header_style="bold yellow")
        table.add_column("File")
        table.add_column("WPs")
        table.add_column("Confidence")

        for pred in manual_required:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps, )

        console.print("[yellow]May require manual resolution:[/yellow]")
        console.print(table)
        console.print()

    if auto_resolvable:
        table = Table(show_header=True, header_style="bold dim")
        table.add_column("Status File")
        table.add_column("WPs")

        for pred in auto_resolvable:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps)

        console.print("[dim]Auto-resolvable (status files):[/dim]")
        console.print(table)
        console.print()

    # Summary guidance
    if manual_count == 0:
        console.print("[green]All conflicts can be auto-resolved.[/green]\n")
    else:
        console.print(
            f"[yellow]Prepare to resolve {manual_count} conflict(s) manually during merge.[/yellow]\n"
        )


def x_display_conflict_forecast__mutmut_46(
    predictions: list[ConflictPrediction],
    console: Console,
) -> None:
    """Display conflict predictions with Rich formatting.

    Groups predictions into auto-resolvable (status files) and
    manual-required categories for clear user guidance.

    Args:
        predictions: List of ConflictPrediction objects
        console: Rich Console instance for output
    """
    if not predictions:
        console.print("\n[green]No conflicts predicted[/green]\n")
        return

    console.print("\n[bold]Conflict Forecast[/bold]\n")

    auto_resolvable = [p for p in predictions if p.auto_resolvable]
    manual_required = [p for p in predictions if not p.auto_resolvable]

    # Summary counts
    total = len(predictions)
    auto_count = len(auto_resolvable)
    manual_count = len(manual_required)

    console.print(f"[dim]Found {total} potential conflict(s): {auto_count} auto-resolvable, {manual_count} manual[/dim]\n")

    # Create table for conflicts
    if manual_required:
        table = Table(show_header=True, header_style="bold yellow")
        table.add_column("File")
        table.add_column("WPs")
        table.add_column("Confidence")

        for pred in manual_required:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps, pred.confidence)

        console.print(None)
        console.print(table)
        console.print()

    if auto_resolvable:
        table = Table(show_header=True, header_style="bold dim")
        table.add_column("Status File")
        table.add_column("WPs")

        for pred in auto_resolvable:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps)

        console.print("[dim]Auto-resolvable (status files):[/dim]")
        console.print(table)
        console.print()

    # Summary guidance
    if manual_count == 0:
        console.print("[green]All conflicts can be auto-resolved.[/green]\n")
    else:
        console.print(
            f"[yellow]Prepare to resolve {manual_count} conflict(s) manually during merge.[/yellow]\n"
        )


def x_display_conflict_forecast__mutmut_47(
    predictions: list[ConflictPrediction],
    console: Console,
) -> None:
    """Display conflict predictions with Rich formatting.

    Groups predictions into auto-resolvable (status files) and
    manual-required categories for clear user guidance.

    Args:
        predictions: List of ConflictPrediction objects
        console: Rich Console instance for output
    """
    if not predictions:
        console.print("\n[green]No conflicts predicted[/green]\n")
        return

    console.print("\n[bold]Conflict Forecast[/bold]\n")

    auto_resolvable = [p for p in predictions if p.auto_resolvable]
    manual_required = [p for p in predictions if not p.auto_resolvable]

    # Summary counts
    total = len(predictions)
    auto_count = len(auto_resolvable)
    manual_count = len(manual_required)

    console.print(f"[dim]Found {total} potential conflict(s): {auto_count} auto-resolvable, {manual_count} manual[/dim]\n")

    # Create table for conflicts
    if manual_required:
        table = Table(show_header=True, header_style="bold yellow")
        table.add_column("File")
        table.add_column("WPs")
        table.add_column("Confidence")

        for pred in manual_required:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps, pred.confidence)

        console.print("XX[yellow]May require manual resolution:[/yellow]XX")
        console.print(table)
        console.print()

    if auto_resolvable:
        table = Table(show_header=True, header_style="bold dim")
        table.add_column("Status File")
        table.add_column("WPs")

        for pred in auto_resolvable:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps)

        console.print("[dim]Auto-resolvable (status files):[/dim]")
        console.print(table)
        console.print()

    # Summary guidance
    if manual_count == 0:
        console.print("[green]All conflicts can be auto-resolved.[/green]\n")
    else:
        console.print(
            f"[yellow]Prepare to resolve {manual_count} conflict(s) manually during merge.[/yellow]\n"
        )


def x_display_conflict_forecast__mutmut_48(
    predictions: list[ConflictPrediction],
    console: Console,
) -> None:
    """Display conflict predictions with Rich formatting.

    Groups predictions into auto-resolvable (status files) and
    manual-required categories for clear user guidance.

    Args:
        predictions: List of ConflictPrediction objects
        console: Rich Console instance for output
    """
    if not predictions:
        console.print("\n[green]No conflicts predicted[/green]\n")
        return

    console.print("\n[bold]Conflict Forecast[/bold]\n")

    auto_resolvable = [p for p in predictions if p.auto_resolvable]
    manual_required = [p for p in predictions if not p.auto_resolvable]

    # Summary counts
    total = len(predictions)
    auto_count = len(auto_resolvable)
    manual_count = len(manual_required)

    console.print(f"[dim]Found {total} potential conflict(s): {auto_count} auto-resolvable, {manual_count} manual[/dim]\n")

    # Create table for conflicts
    if manual_required:
        table = Table(show_header=True, header_style="bold yellow")
        table.add_column("File")
        table.add_column("WPs")
        table.add_column("Confidence")

        for pred in manual_required:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps, pred.confidence)

        console.print("[yellow]may require manual resolution:[/yellow]")
        console.print(table)
        console.print()

    if auto_resolvable:
        table = Table(show_header=True, header_style="bold dim")
        table.add_column("Status File")
        table.add_column("WPs")

        for pred in auto_resolvable:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps)

        console.print("[dim]Auto-resolvable (status files):[/dim]")
        console.print(table)
        console.print()

    # Summary guidance
    if manual_count == 0:
        console.print("[green]All conflicts can be auto-resolved.[/green]\n")
    else:
        console.print(
            f"[yellow]Prepare to resolve {manual_count} conflict(s) manually during merge.[/yellow]\n"
        )


def x_display_conflict_forecast__mutmut_49(
    predictions: list[ConflictPrediction],
    console: Console,
) -> None:
    """Display conflict predictions with Rich formatting.

    Groups predictions into auto-resolvable (status files) and
    manual-required categories for clear user guidance.

    Args:
        predictions: List of ConflictPrediction objects
        console: Rich Console instance for output
    """
    if not predictions:
        console.print("\n[green]No conflicts predicted[/green]\n")
        return

    console.print("\n[bold]Conflict Forecast[/bold]\n")

    auto_resolvable = [p for p in predictions if p.auto_resolvable]
    manual_required = [p for p in predictions if not p.auto_resolvable]

    # Summary counts
    total = len(predictions)
    auto_count = len(auto_resolvable)
    manual_count = len(manual_required)

    console.print(f"[dim]Found {total} potential conflict(s): {auto_count} auto-resolvable, {manual_count} manual[/dim]\n")

    # Create table for conflicts
    if manual_required:
        table = Table(show_header=True, header_style="bold yellow")
        table.add_column("File")
        table.add_column("WPs")
        table.add_column("Confidence")

        for pred in manual_required:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps, pred.confidence)

        console.print("[YELLOW]MAY REQUIRE MANUAL RESOLUTION:[/YELLOW]")
        console.print(table)
        console.print()

    if auto_resolvable:
        table = Table(show_header=True, header_style="bold dim")
        table.add_column("Status File")
        table.add_column("WPs")

        for pred in auto_resolvable:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps)

        console.print("[dim]Auto-resolvable (status files):[/dim]")
        console.print(table)
        console.print()

    # Summary guidance
    if manual_count == 0:
        console.print("[green]All conflicts can be auto-resolved.[/green]\n")
    else:
        console.print(
            f"[yellow]Prepare to resolve {manual_count} conflict(s) manually during merge.[/yellow]\n"
        )


def x_display_conflict_forecast__mutmut_50(
    predictions: list[ConflictPrediction],
    console: Console,
) -> None:
    """Display conflict predictions with Rich formatting.

    Groups predictions into auto-resolvable (status files) and
    manual-required categories for clear user guidance.

    Args:
        predictions: List of ConflictPrediction objects
        console: Rich Console instance for output
    """
    if not predictions:
        console.print("\n[green]No conflicts predicted[/green]\n")
        return

    console.print("\n[bold]Conflict Forecast[/bold]\n")

    auto_resolvable = [p for p in predictions if p.auto_resolvable]
    manual_required = [p for p in predictions if not p.auto_resolvable]

    # Summary counts
    total = len(predictions)
    auto_count = len(auto_resolvable)
    manual_count = len(manual_required)

    console.print(f"[dim]Found {total} potential conflict(s): {auto_count} auto-resolvable, {manual_count} manual[/dim]\n")

    # Create table for conflicts
    if manual_required:
        table = Table(show_header=True, header_style="bold yellow")
        table.add_column("File")
        table.add_column("WPs")
        table.add_column("Confidence")

        for pred in manual_required:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps, pred.confidence)

        console.print("[yellow]May require manual resolution:[/yellow]")
        console.print(None)
        console.print()

    if auto_resolvable:
        table = Table(show_header=True, header_style="bold dim")
        table.add_column("Status File")
        table.add_column("WPs")

        for pred in auto_resolvable:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps)

        console.print("[dim]Auto-resolvable (status files):[/dim]")
        console.print(table)
        console.print()

    # Summary guidance
    if manual_count == 0:
        console.print("[green]All conflicts can be auto-resolved.[/green]\n")
    else:
        console.print(
            f"[yellow]Prepare to resolve {manual_count} conflict(s) manually during merge.[/yellow]\n"
        )


def x_display_conflict_forecast__mutmut_51(
    predictions: list[ConflictPrediction],
    console: Console,
) -> None:
    """Display conflict predictions with Rich formatting.

    Groups predictions into auto-resolvable (status files) and
    manual-required categories for clear user guidance.

    Args:
        predictions: List of ConflictPrediction objects
        console: Rich Console instance for output
    """
    if not predictions:
        console.print("\n[green]No conflicts predicted[/green]\n")
        return

    console.print("\n[bold]Conflict Forecast[/bold]\n")

    auto_resolvable = [p for p in predictions if p.auto_resolvable]
    manual_required = [p for p in predictions if not p.auto_resolvable]

    # Summary counts
    total = len(predictions)
    auto_count = len(auto_resolvable)
    manual_count = len(manual_required)

    console.print(f"[dim]Found {total} potential conflict(s): {auto_count} auto-resolvable, {manual_count} manual[/dim]\n")

    # Create table for conflicts
    if manual_required:
        table = Table(show_header=True, header_style="bold yellow")
        table.add_column("File")
        table.add_column("WPs")
        table.add_column("Confidence")

        for pred in manual_required:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps, pred.confidence)

        console.print("[yellow]May require manual resolution:[/yellow]")
        console.print(table)
        console.print()

    if auto_resolvable:
        table = None
        table.add_column("Status File")
        table.add_column("WPs")

        for pred in auto_resolvable:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps)

        console.print("[dim]Auto-resolvable (status files):[/dim]")
        console.print(table)
        console.print()

    # Summary guidance
    if manual_count == 0:
        console.print("[green]All conflicts can be auto-resolved.[/green]\n")
    else:
        console.print(
            f"[yellow]Prepare to resolve {manual_count} conflict(s) manually during merge.[/yellow]\n"
        )


def x_display_conflict_forecast__mutmut_52(
    predictions: list[ConflictPrediction],
    console: Console,
) -> None:
    """Display conflict predictions with Rich formatting.

    Groups predictions into auto-resolvable (status files) and
    manual-required categories for clear user guidance.

    Args:
        predictions: List of ConflictPrediction objects
        console: Rich Console instance for output
    """
    if not predictions:
        console.print("\n[green]No conflicts predicted[/green]\n")
        return

    console.print("\n[bold]Conflict Forecast[/bold]\n")

    auto_resolvable = [p for p in predictions if p.auto_resolvable]
    manual_required = [p for p in predictions if not p.auto_resolvable]

    # Summary counts
    total = len(predictions)
    auto_count = len(auto_resolvable)
    manual_count = len(manual_required)

    console.print(f"[dim]Found {total} potential conflict(s): {auto_count} auto-resolvable, {manual_count} manual[/dim]\n")

    # Create table for conflicts
    if manual_required:
        table = Table(show_header=True, header_style="bold yellow")
        table.add_column("File")
        table.add_column("WPs")
        table.add_column("Confidence")

        for pred in manual_required:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps, pred.confidence)

        console.print("[yellow]May require manual resolution:[/yellow]")
        console.print(table)
        console.print()

    if auto_resolvable:
        table = Table(show_header=None, header_style="bold dim")
        table.add_column("Status File")
        table.add_column("WPs")

        for pred in auto_resolvable:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps)

        console.print("[dim]Auto-resolvable (status files):[/dim]")
        console.print(table)
        console.print()

    # Summary guidance
    if manual_count == 0:
        console.print("[green]All conflicts can be auto-resolved.[/green]\n")
    else:
        console.print(
            f"[yellow]Prepare to resolve {manual_count} conflict(s) manually during merge.[/yellow]\n"
        )


def x_display_conflict_forecast__mutmut_53(
    predictions: list[ConflictPrediction],
    console: Console,
) -> None:
    """Display conflict predictions with Rich formatting.

    Groups predictions into auto-resolvable (status files) and
    manual-required categories for clear user guidance.

    Args:
        predictions: List of ConflictPrediction objects
        console: Rich Console instance for output
    """
    if not predictions:
        console.print("\n[green]No conflicts predicted[/green]\n")
        return

    console.print("\n[bold]Conflict Forecast[/bold]\n")

    auto_resolvable = [p for p in predictions if p.auto_resolvable]
    manual_required = [p for p in predictions if not p.auto_resolvable]

    # Summary counts
    total = len(predictions)
    auto_count = len(auto_resolvable)
    manual_count = len(manual_required)

    console.print(f"[dim]Found {total} potential conflict(s): {auto_count} auto-resolvable, {manual_count} manual[/dim]\n")

    # Create table for conflicts
    if manual_required:
        table = Table(show_header=True, header_style="bold yellow")
        table.add_column("File")
        table.add_column("WPs")
        table.add_column("Confidence")

        for pred in manual_required:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps, pred.confidence)

        console.print("[yellow]May require manual resolution:[/yellow]")
        console.print(table)
        console.print()

    if auto_resolvable:
        table = Table(show_header=True, header_style=None)
        table.add_column("Status File")
        table.add_column("WPs")

        for pred in auto_resolvable:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps)

        console.print("[dim]Auto-resolvable (status files):[/dim]")
        console.print(table)
        console.print()

    # Summary guidance
    if manual_count == 0:
        console.print("[green]All conflicts can be auto-resolved.[/green]\n")
    else:
        console.print(
            f"[yellow]Prepare to resolve {manual_count} conflict(s) manually during merge.[/yellow]\n"
        )


def x_display_conflict_forecast__mutmut_54(
    predictions: list[ConflictPrediction],
    console: Console,
) -> None:
    """Display conflict predictions with Rich formatting.

    Groups predictions into auto-resolvable (status files) and
    manual-required categories for clear user guidance.

    Args:
        predictions: List of ConflictPrediction objects
        console: Rich Console instance for output
    """
    if not predictions:
        console.print("\n[green]No conflicts predicted[/green]\n")
        return

    console.print("\n[bold]Conflict Forecast[/bold]\n")

    auto_resolvable = [p for p in predictions if p.auto_resolvable]
    manual_required = [p for p in predictions if not p.auto_resolvable]

    # Summary counts
    total = len(predictions)
    auto_count = len(auto_resolvable)
    manual_count = len(manual_required)

    console.print(f"[dim]Found {total} potential conflict(s): {auto_count} auto-resolvable, {manual_count} manual[/dim]\n")

    # Create table for conflicts
    if manual_required:
        table = Table(show_header=True, header_style="bold yellow")
        table.add_column("File")
        table.add_column("WPs")
        table.add_column("Confidence")

        for pred in manual_required:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps, pred.confidence)

        console.print("[yellow]May require manual resolution:[/yellow]")
        console.print(table)
        console.print()

    if auto_resolvable:
        table = Table(header_style="bold dim")
        table.add_column("Status File")
        table.add_column("WPs")

        for pred in auto_resolvable:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps)

        console.print("[dim]Auto-resolvable (status files):[/dim]")
        console.print(table)
        console.print()

    # Summary guidance
    if manual_count == 0:
        console.print("[green]All conflicts can be auto-resolved.[/green]\n")
    else:
        console.print(
            f"[yellow]Prepare to resolve {manual_count} conflict(s) manually during merge.[/yellow]\n"
        )


def x_display_conflict_forecast__mutmut_55(
    predictions: list[ConflictPrediction],
    console: Console,
) -> None:
    """Display conflict predictions with Rich formatting.

    Groups predictions into auto-resolvable (status files) and
    manual-required categories for clear user guidance.

    Args:
        predictions: List of ConflictPrediction objects
        console: Rich Console instance for output
    """
    if not predictions:
        console.print("\n[green]No conflicts predicted[/green]\n")
        return

    console.print("\n[bold]Conflict Forecast[/bold]\n")

    auto_resolvable = [p for p in predictions if p.auto_resolvable]
    manual_required = [p for p in predictions if not p.auto_resolvable]

    # Summary counts
    total = len(predictions)
    auto_count = len(auto_resolvable)
    manual_count = len(manual_required)

    console.print(f"[dim]Found {total} potential conflict(s): {auto_count} auto-resolvable, {manual_count} manual[/dim]\n")

    # Create table for conflicts
    if manual_required:
        table = Table(show_header=True, header_style="bold yellow")
        table.add_column("File")
        table.add_column("WPs")
        table.add_column("Confidence")

        for pred in manual_required:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps, pred.confidence)

        console.print("[yellow]May require manual resolution:[/yellow]")
        console.print(table)
        console.print()

    if auto_resolvable:
        table = Table(show_header=True, )
        table.add_column("Status File")
        table.add_column("WPs")

        for pred in auto_resolvable:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps)

        console.print("[dim]Auto-resolvable (status files):[/dim]")
        console.print(table)
        console.print()

    # Summary guidance
    if manual_count == 0:
        console.print("[green]All conflicts can be auto-resolved.[/green]\n")
    else:
        console.print(
            f"[yellow]Prepare to resolve {manual_count} conflict(s) manually during merge.[/yellow]\n"
        )


def x_display_conflict_forecast__mutmut_56(
    predictions: list[ConflictPrediction],
    console: Console,
) -> None:
    """Display conflict predictions with Rich formatting.

    Groups predictions into auto-resolvable (status files) and
    manual-required categories for clear user guidance.

    Args:
        predictions: List of ConflictPrediction objects
        console: Rich Console instance for output
    """
    if not predictions:
        console.print("\n[green]No conflicts predicted[/green]\n")
        return

    console.print("\n[bold]Conflict Forecast[/bold]\n")

    auto_resolvable = [p for p in predictions if p.auto_resolvable]
    manual_required = [p for p in predictions if not p.auto_resolvable]

    # Summary counts
    total = len(predictions)
    auto_count = len(auto_resolvable)
    manual_count = len(manual_required)

    console.print(f"[dim]Found {total} potential conflict(s): {auto_count} auto-resolvable, {manual_count} manual[/dim]\n")

    # Create table for conflicts
    if manual_required:
        table = Table(show_header=True, header_style="bold yellow")
        table.add_column("File")
        table.add_column("WPs")
        table.add_column("Confidence")

        for pred in manual_required:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps, pred.confidence)

        console.print("[yellow]May require manual resolution:[/yellow]")
        console.print(table)
        console.print()

    if auto_resolvable:
        table = Table(show_header=False, header_style="bold dim")
        table.add_column("Status File")
        table.add_column("WPs")

        for pred in auto_resolvable:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps)

        console.print("[dim]Auto-resolvable (status files):[/dim]")
        console.print(table)
        console.print()

    # Summary guidance
    if manual_count == 0:
        console.print("[green]All conflicts can be auto-resolved.[/green]\n")
    else:
        console.print(
            f"[yellow]Prepare to resolve {manual_count} conflict(s) manually during merge.[/yellow]\n"
        )


def x_display_conflict_forecast__mutmut_57(
    predictions: list[ConflictPrediction],
    console: Console,
) -> None:
    """Display conflict predictions with Rich formatting.

    Groups predictions into auto-resolvable (status files) and
    manual-required categories for clear user guidance.

    Args:
        predictions: List of ConflictPrediction objects
        console: Rich Console instance for output
    """
    if not predictions:
        console.print("\n[green]No conflicts predicted[/green]\n")
        return

    console.print("\n[bold]Conflict Forecast[/bold]\n")

    auto_resolvable = [p for p in predictions if p.auto_resolvable]
    manual_required = [p for p in predictions if not p.auto_resolvable]

    # Summary counts
    total = len(predictions)
    auto_count = len(auto_resolvable)
    manual_count = len(manual_required)

    console.print(f"[dim]Found {total} potential conflict(s): {auto_count} auto-resolvable, {manual_count} manual[/dim]\n")

    # Create table for conflicts
    if manual_required:
        table = Table(show_header=True, header_style="bold yellow")
        table.add_column("File")
        table.add_column("WPs")
        table.add_column("Confidence")

        for pred in manual_required:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps, pred.confidence)

        console.print("[yellow]May require manual resolution:[/yellow]")
        console.print(table)
        console.print()

    if auto_resolvable:
        table = Table(show_header=True, header_style="XXbold dimXX")
        table.add_column("Status File")
        table.add_column("WPs")

        for pred in auto_resolvable:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps)

        console.print("[dim]Auto-resolvable (status files):[/dim]")
        console.print(table)
        console.print()

    # Summary guidance
    if manual_count == 0:
        console.print("[green]All conflicts can be auto-resolved.[/green]\n")
    else:
        console.print(
            f"[yellow]Prepare to resolve {manual_count} conflict(s) manually during merge.[/yellow]\n"
        )


def x_display_conflict_forecast__mutmut_58(
    predictions: list[ConflictPrediction],
    console: Console,
) -> None:
    """Display conflict predictions with Rich formatting.

    Groups predictions into auto-resolvable (status files) and
    manual-required categories for clear user guidance.

    Args:
        predictions: List of ConflictPrediction objects
        console: Rich Console instance for output
    """
    if not predictions:
        console.print("\n[green]No conflicts predicted[/green]\n")
        return

    console.print("\n[bold]Conflict Forecast[/bold]\n")

    auto_resolvable = [p for p in predictions if p.auto_resolvable]
    manual_required = [p for p in predictions if not p.auto_resolvable]

    # Summary counts
    total = len(predictions)
    auto_count = len(auto_resolvable)
    manual_count = len(manual_required)

    console.print(f"[dim]Found {total} potential conflict(s): {auto_count} auto-resolvable, {manual_count} manual[/dim]\n")

    # Create table for conflicts
    if manual_required:
        table = Table(show_header=True, header_style="bold yellow")
        table.add_column("File")
        table.add_column("WPs")
        table.add_column("Confidence")

        for pred in manual_required:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps, pred.confidence)

        console.print("[yellow]May require manual resolution:[/yellow]")
        console.print(table)
        console.print()

    if auto_resolvable:
        table = Table(show_header=True, header_style="BOLD DIM")
        table.add_column("Status File")
        table.add_column("WPs")

        for pred in auto_resolvable:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps)

        console.print("[dim]Auto-resolvable (status files):[/dim]")
        console.print(table)
        console.print()

    # Summary guidance
    if manual_count == 0:
        console.print("[green]All conflicts can be auto-resolved.[/green]\n")
    else:
        console.print(
            f"[yellow]Prepare to resolve {manual_count} conflict(s) manually during merge.[/yellow]\n"
        )


def x_display_conflict_forecast__mutmut_59(
    predictions: list[ConflictPrediction],
    console: Console,
) -> None:
    """Display conflict predictions with Rich formatting.

    Groups predictions into auto-resolvable (status files) and
    manual-required categories for clear user guidance.

    Args:
        predictions: List of ConflictPrediction objects
        console: Rich Console instance for output
    """
    if not predictions:
        console.print("\n[green]No conflicts predicted[/green]\n")
        return

    console.print("\n[bold]Conflict Forecast[/bold]\n")

    auto_resolvable = [p for p in predictions if p.auto_resolvable]
    manual_required = [p for p in predictions if not p.auto_resolvable]

    # Summary counts
    total = len(predictions)
    auto_count = len(auto_resolvable)
    manual_count = len(manual_required)

    console.print(f"[dim]Found {total} potential conflict(s): {auto_count} auto-resolvable, {manual_count} manual[/dim]\n")

    # Create table for conflicts
    if manual_required:
        table = Table(show_header=True, header_style="bold yellow")
        table.add_column("File")
        table.add_column("WPs")
        table.add_column("Confidence")

        for pred in manual_required:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps, pred.confidence)

        console.print("[yellow]May require manual resolution:[/yellow]")
        console.print(table)
        console.print()

    if auto_resolvable:
        table = Table(show_header=True, header_style="bold dim")
        table.add_column(None)
        table.add_column("WPs")

        for pred in auto_resolvable:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps)

        console.print("[dim]Auto-resolvable (status files):[/dim]")
        console.print(table)
        console.print()

    # Summary guidance
    if manual_count == 0:
        console.print("[green]All conflicts can be auto-resolved.[/green]\n")
    else:
        console.print(
            f"[yellow]Prepare to resolve {manual_count} conflict(s) manually during merge.[/yellow]\n"
        )


def x_display_conflict_forecast__mutmut_60(
    predictions: list[ConflictPrediction],
    console: Console,
) -> None:
    """Display conflict predictions with Rich formatting.

    Groups predictions into auto-resolvable (status files) and
    manual-required categories for clear user guidance.

    Args:
        predictions: List of ConflictPrediction objects
        console: Rich Console instance for output
    """
    if not predictions:
        console.print("\n[green]No conflicts predicted[/green]\n")
        return

    console.print("\n[bold]Conflict Forecast[/bold]\n")

    auto_resolvable = [p for p in predictions if p.auto_resolvable]
    manual_required = [p for p in predictions if not p.auto_resolvable]

    # Summary counts
    total = len(predictions)
    auto_count = len(auto_resolvable)
    manual_count = len(manual_required)

    console.print(f"[dim]Found {total} potential conflict(s): {auto_count} auto-resolvable, {manual_count} manual[/dim]\n")

    # Create table for conflicts
    if manual_required:
        table = Table(show_header=True, header_style="bold yellow")
        table.add_column("File")
        table.add_column("WPs")
        table.add_column("Confidence")

        for pred in manual_required:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps, pred.confidence)

        console.print("[yellow]May require manual resolution:[/yellow]")
        console.print(table)
        console.print()

    if auto_resolvable:
        table = Table(show_header=True, header_style="bold dim")
        table.add_column("XXStatus FileXX")
        table.add_column("WPs")

        for pred in auto_resolvable:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps)

        console.print("[dim]Auto-resolvable (status files):[/dim]")
        console.print(table)
        console.print()

    # Summary guidance
    if manual_count == 0:
        console.print("[green]All conflicts can be auto-resolved.[/green]\n")
    else:
        console.print(
            f"[yellow]Prepare to resolve {manual_count} conflict(s) manually during merge.[/yellow]\n"
        )


def x_display_conflict_forecast__mutmut_61(
    predictions: list[ConflictPrediction],
    console: Console,
) -> None:
    """Display conflict predictions with Rich formatting.

    Groups predictions into auto-resolvable (status files) and
    manual-required categories for clear user guidance.

    Args:
        predictions: List of ConflictPrediction objects
        console: Rich Console instance for output
    """
    if not predictions:
        console.print("\n[green]No conflicts predicted[/green]\n")
        return

    console.print("\n[bold]Conflict Forecast[/bold]\n")

    auto_resolvable = [p for p in predictions if p.auto_resolvable]
    manual_required = [p for p in predictions if not p.auto_resolvable]

    # Summary counts
    total = len(predictions)
    auto_count = len(auto_resolvable)
    manual_count = len(manual_required)

    console.print(f"[dim]Found {total} potential conflict(s): {auto_count} auto-resolvable, {manual_count} manual[/dim]\n")

    # Create table for conflicts
    if manual_required:
        table = Table(show_header=True, header_style="bold yellow")
        table.add_column("File")
        table.add_column("WPs")
        table.add_column("Confidence")

        for pred in manual_required:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps, pred.confidence)

        console.print("[yellow]May require manual resolution:[/yellow]")
        console.print(table)
        console.print()

    if auto_resolvable:
        table = Table(show_header=True, header_style="bold dim")
        table.add_column("status file")
        table.add_column("WPs")

        for pred in auto_resolvable:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps)

        console.print("[dim]Auto-resolvable (status files):[/dim]")
        console.print(table)
        console.print()

    # Summary guidance
    if manual_count == 0:
        console.print("[green]All conflicts can be auto-resolved.[/green]\n")
    else:
        console.print(
            f"[yellow]Prepare to resolve {manual_count} conflict(s) manually during merge.[/yellow]\n"
        )


def x_display_conflict_forecast__mutmut_62(
    predictions: list[ConflictPrediction],
    console: Console,
) -> None:
    """Display conflict predictions with Rich formatting.

    Groups predictions into auto-resolvable (status files) and
    manual-required categories for clear user guidance.

    Args:
        predictions: List of ConflictPrediction objects
        console: Rich Console instance for output
    """
    if not predictions:
        console.print("\n[green]No conflicts predicted[/green]\n")
        return

    console.print("\n[bold]Conflict Forecast[/bold]\n")

    auto_resolvable = [p for p in predictions if p.auto_resolvable]
    manual_required = [p for p in predictions if not p.auto_resolvable]

    # Summary counts
    total = len(predictions)
    auto_count = len(auto_resolvable)
    manual_count = len(manual_required)

    console.print(f"[dim]Found {total} potential conflict(s): {auto_count} auto-resolvable, {manual_count} manual[/dim]\n")

    # Create table for conflicts
    if manual_required:
        table = Table(show_header=True, header_style="bold yellow")
        table.add_column("File")
        table.add_column("WPs")
        table.add_column("Confidence")

        for pred in manual_required:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps, pred.confidence)

        console.print("[yellow]May require manual resolution:[/yellow]")
        console.print(table)
        console.print()

    if auto_resolvable:
        table = Table(show_header=True, header_style="bold dim")
        table.add_column("STATUS FILE")
        table.add_column("WPs")

        for pred in auto_resolvable:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps)

        console.print("[dim]Auto-resolvable (status files):[/dim]")
        console.print(table)
        console.print()

    # Summary guidance
    if manual_count == 0:
        console.print("[green]All conflicts can be auto-resolved.[/green]\n")
    else:
        console.print(
            f"[yellow]Prepare to resolve {manual_count} conflict(s) manually during merge.[/yellow]\n"
        )


def x_display_conflict_forecast__mutmut_63(
    predictions: list[ConflictPrediction],
    console: Console,
) -> None:
    """Display conflict predictions with Rich formatting.

    Groups predictions into auto-resolvable (status files) and
    manual-required categories for clear user guidance.

    Args:
        predictions: List of ConflictPrediction objects
        console: Rich Console instance for output
    """
    if not predictions:
        console.print("\n[green]No conflicts predicted[/green]\n")
        return

    console.print("\n[bold]Conflict Forecast[/bold]\n")

    auto_resolvable = [p for p in predictions if p.auto_resolvable]
    manual_required = [p for p in predictions if not p.auto_resolvable]

    # Summary counts
    total = len(predictions)
    auto_count = len(auto_resolvable)
    manual_count = len(manual_required)

    console.print(f"[dim]Found {total} potential conflict(s): {auto_count} auto-resolvable, {manual_count} manual[/dim]\n")

    # Create table for conflicts
    if manual_required:
        table = Table(show_header=True, header_style="bold yellow")
        table.add_column("File")
        table.add_column("WPs")
        table.add_column("Confidence")

        for pred in manual_required:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps, pred.confidence)

        console.print("[yellow]May require manual resolution:[/yellow]")
        console.print(table)
        console.print()

    if auto_resolvable:
        table = Table(show_header=True, header_style="bold dim")
        table.add_column("Status File")
        table.add_column(None)

        for pred in auto_resolvable:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps)

        console.print("[dim]Auto-resolvable (status files):[/dim]")
        console.print(table)
        console.print()

    # Summary guidance
    if manual_count == 0:
        console.print("[green]All conflicts can be auto-resolved.[/green]\n")
    else:
        console.print(
            f"[yellow]Prepare to resolve {manual_count} conflict(s) manually during merge.[/yellow]\n"
        )


def x_display_conflict_forecast__mutmut_64(
    predictions: list[ConflictPrediction],
    console: Console,
) -> None:
    """Display conflict predictions with Rich formatting.

    Groups predictions into auto-resolvable (status files) and
    manual-required categories for clear user guidance.

    Args:
        predictions: List of ConflictPrediction objects
        console: Rich Console instance for output
    """
    if not predictions:
        console.print("\n[green]No conflicts predicted[/green]\n")
        return

    console.print("\n[bold]Conflict Forecast[/bold]\n")

    auto_resolvable = [p for p in predictions if p.auto_resolvable]
    manual_required = [p for p in predictions if not p.auto_resolvable]

    # Summary counts
    total = len(predictions)
    auto_count = len(auto_resolvable)
    manual_count = len(manual_required)

    console.print(f"[dim]Found {total} potential conflict(s): {auto_count} auto-resolvable, {manual_count} manual[/dim]\n")

    # Create table for conflicts
    if manual_required:
        table = Table(show_header=True, header_style="bold yellow")
        table.add_column("File")
        table.add_column("WPs")
        table.add_column("Confidence")

        for pred in manual_required:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps, pred.confidence)

        console.print("[yellow]May require manual resolution:[/yellow]")
        console.print(table)
        console.print()

    if auto_resolvable:
        table = Table(show_header=True, header_style="bold dim")
        table.add_column("Status File")
        table.add_column("XXWPsXX")

        for pred in auto_resolvable:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps)

        console.print("[dim]Auto-resolvable (status files):[/dim]")
        console.print(table)
        console.print()

    # Summary guidance
    if manual_count == 0:
        console.print("[green]All conflicts can be auto-resolved.[/green]\n")
    else:
        console.print(
            f"[yellow]Prepare to resolve {manual_count} conflict(s) manually during merge.[/yellow]\n"
        )


def x_display_conflict_forecast__mutmut_65(
    predictions: list[ConflictPrediction],
    console: Console,
) -> None:
    """Display conflict predictions with Rich formatting.

    Groups predictions into auto-resolvable (status files) and
    manual-required categories for clear user guidance.

    Args:
        predictions: List of ConflictPrediction objects
        console: Rich Console instance for output
    """
    if not predictions:
        console.print("\n[green]No conflicts predicted[/green]\n")
        return

    console.print("\n[bold]Conflict Forecast[/bold]\n")

    auto_resolvable = [p for p in predictions if p.auto_resolvable]
    manual_required = [p for p in predictions if not p.auto_resolvable]

    # Summary counts
    total = len(predictions)
    auto_count = len(auto_resolvable)
    manual_count = len(manual_required)

    console.print(f"[dim]Found {total} potential conflict(s): {auto_count} auto-resolvable, {manual_count} manual[/dim]\n")

    # Create table for conflicts
    if manual_required:
        table = Table(show_header=True, header_style="bold yellow")
        table.add_column("File")
        table.add_column("WPs")
        table.add_column("Confidence")

        for pred in manual_required:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps, pred.confidence)

        console.print("[yellow]May require manual resolution:[/yellow]")
        console.print(table)
        console.print()

    if auto_resolvable:
        table = Table(show_header=True, header_style="bold dim")
        table.add_column("Status File")
        table.add_column("wps")

        for pred in auto_resolvable:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps)

        console.print("[dim]Auto-resolvable (status files):[/dim]")
        console.print(table)
        console.print()

    # Summary guidance
    if manual_count == 0:
        console.print("[green]All conflicts can be auto-resolved.[/green]\n")
    else:
        console.print(
            f"[yellow]Prepare to resolve {manual_count} conflict(s) manually during merge.[/yellow]\n"
        )


def x_display_conflict_forecast__mutmut_66(
    predictions: list[ConflictPrediction],
    console: Console,
) -> None:
    """Display conflict predictions with Rich formatting.

    Groups predictions into auto-resolvable (status files) and
    manual-required categories for clear user guidance.

    Args:
        predictions: List of ConflictPrediction objects
        console: Rich Console instance for output
    """
    if not predictions:
        console.print("\n[green]No conflicts predicted[/green]\n")
        return

    console.print("\n[bold]Conflict Forecast[/bold]\n")

    auto_resolvable = [p for p in predictions if p.auto_resolvable]
    manual_required = [p for p in predictions if not p.auto_resolvable]

    # Summary counts
    total = len(predictions)
    auto_count = len(auto_resolvable)
    manual_count = len(manual_required)

    console.print(f"[dim]Found {total} potential conflict(s): {auto_count} auto-resolvable, {manual_count} manual[/dim]\n")

    # Create table for conflicts
    if manual_required:
        table = Table(show_header=True, header_style="bold yellow")
        table.add_column("File")
        table.add_column("WPs")
        table.add_column("Confidence")

        for pred in manual_required:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps, pred.confidence)

        console.print("[yellow]May require manual resolution:[/yellow]")
        console.print(table)
        console.print()

    if auto_resolvable:
        table = Table(show_header=True, header_style="bold dim")
        table.add_column("Status File")
        table.add_column("WPS")

        for pred in auto_resolvable:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps)

        console.print("[dim]Auto-resolvable (status files):[/dim]")
        console.print(table)
        console.print()

    # Summary guidance
    if manual_count == 0:
        console.print("[green]All conflicts can be auto-resolved.[/green]\n")
    else:
        console.print(
            f"[yellow]Prepare to resolve {manual_count} conflict(s) manually during merge.[/yellow]\n"
        )


def x_display_conflict_forecast__mutmut_67(
    predictions: list[ConflictPrediction],
    console: Console,
) -> None:
    """Display conflict predictions with Rich formatting.

    Groups predictions into auto-resolvable (status files) and
    manual-required categories for clear user guidance.

    Args:
        predictions: List of ConflictPrediction objects
        console: Rich Console instance for output
    """
    if not predictions:
        console.print("\n[green]No conflicts predicted[/green]\n")
        return

    console.print("\n[bold]Conflict Forecast[/bold]\n")

    auto_resolvable = [p for p in predictions if p.auto_resolvable]
    manual_required = [p for p in predictions if not p.auto_resolvable]

    # Summary counts
    total = len(predictions)
    auto_count = len(auto_resolvable)
    manual_count = len(manual_required)

    console.print(f"[dim]Found {total} potential conflict(s): {auto_count} auto-resolvable, {manual_count} manual[/dim]\n")

    # Create table for conflicts
    if manual_required:
        table = Table(show_header=True, header_style="bold yellow")
        table.add_column("File")
        table.add_column("WPs")
        table.add_column("Confidence")

        for pred in manual_required:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps, pred.confidence)

        console.print("[yellow]May require manual resolution:[/yellow]")
        console.print(table)
        console.print()

    if auto_resolvable:
        table = Table(show_header=True, header_style="bold dim")
        table.add_column("Status File")
        table.add_column("WPs")

        for pred in auto_resolvable:
            wps = None
            table.add_row(pred.file_path, wps)

        console.print("[dim]Auto-resolvable (status files):[/dim]")
        console.print(table)
        console.print()

    # Summary guidance
    if manual_count == 0:
        console.print("[green]All conflicts can be auto-resolved.[/green]\n")
    else:
        console.print(
            f"[yellow]Prepare to resolve {manual_count} conflict(s) manually during merge.[/yellow]\n"
        )


def x_display_conflict_forecast__mutmut_68(
    predictions: list[ConflictPrediction],
    console: Console,
) -> None:
    """Display conflict predictions with Rich formatting.

    Groups predictions into auto-resolvable (status files) and
    manual-required categories for clear user guidance.

    Args:
        predictions: List of ConflictPrediction objects
        console: Rich Console instance for output
    """
    if not predictions:
        console.print("\n[green]No conflicts predicted[/green]\n")
        return

    console.print("\n[bold]Conflict Forecast[/bold]\n")

    auto_resolvable = [p for p in predictions if p.auto_resolvable]
    manual_required = [p for p in predictions if not p.auto_resolvable]

    # Summary counts
    total = len(predictions)
    auto_count = len(auto_resolvable)
    manual_count = len(manual_required)

    console.print(f"[dim]Found {total} potential conflict(s): {auto_count} auto-resolvable, {manual_count} manual[/dim]\n")

    # Create table for conflicts
    if manual_required:
        table = Table(show_header=True, header_style="bold yellow")
        table.add_column("File")
        table.add_column("WPs")
        table.add_column("Confidence")

        for pred in manual_required:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps, pred.confidence)

        console.print("[yellow]May require manual resolution:[/yellow]")
        console.print(table)
        console.print()

    if auto_resolvable:
        table = Table(show_header=True, header_style="bold dim")
        table.add_column("Status File")
        table.add_column("WPs")

        for pred in auto_resolvable:
            wps = ", ".join(None)
            table.add_row(pred.file_path, wps)

        console.print("[dim]Auto-resolvable (status files):[/dim]")
        console.print(table)
        console.print()

    # Summary guidance
    if manual_count == 0:
        console.print("[green]All conflicts can be auto-resolved.[/green]\n")
    else:
        console.print(
            f"[yellow]Prepare to resolve {manual_count} conflict(s) manually during merge.[/yellow]\n"
        )


def x_display_conflict_forecast__mutmut_69(
    predictions: list[ConflictPrediction],
    console: Console,
) -> None:
    """Display conflict predictions with Rich formatting.

    Groups predictions into auto-resolvable (status files) and
    manual-required categories for clear user guidance.

    Args:
        predictions: List of ConflictPrediction objects
        console: Rich Console instance for output
    """
    if not predictions:
        console.print("\n[green]No conflicts predicted[/green]\n")
        return

    console.print("\n[bold]Conflict Forecast[/bold]\n")

    auto_resolvable = [p for p in predictions if p.auto_resolvable]
    manual_required = [p for p in predictions if not p.auto_resolvable]

    # Summary counts
    total = len(predictions)
    auto_count = len(auto_resolvable)
    manual_count = len(manual_required)

    console.print(f"[dim]Found {total} potential conflict(s): {auto_count} auto-resolvable, {manual_count} manual[/dim]\n")

    # Create table for conflicts
    if manual_required:
        table = Table(show_header=True, header_style="bold yellow")
        table.add_column("File")
        table.add_column("WPs")
        table.add_column("Confidence")

        for pred in manual_required:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps, pred.confidence)

        console.print("[yellow]May require manual resolution:[/yellow]")
        console.print(table)
        console.print()

    if auto_resolvable:
        table = Table(show_header=True, header_style="bold dim")
        table.add_column("Status File")
        table.add_column("WPs")

        for pred in auto_resolvable:
            wps = "XX, XX".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps)

        console.print("[dim]Auto-resolvable (status files):[/dim]")
        console.print(table)
        console.print()

    # Summary guidance
    if manual_count == 0:
        console.print("[green]All conflicts can be auto-resolved.[/green]\n")
    else:
        console.print(
            f"[yellow]Prepare to resolve {manual_count} conflict(s) manually during merge.[/yellow]\n"
        )


def x_display_conflict_forecast__mutmut_70(
    predictions: list[ConflictPrediction],
    console: Console,
) -> None:
    """Display conflict predictions with Rich formatting.

    Groups predictions into auto-resolvable (status files) and
    manual-required categories for clear user guidance.

    Args:
        predictions: List of ConflictPrediction objects
        console: Rich Console instance for output
    """
    if not predictions:
        console.print("\n[green]No conflicts predicted[/green]\n")
        return

    console.print("\n[bold]Conflict Forecast[/bold]\n")

    auto_resolvable = [p for p in predictions if p.auto_resolvable]
    manual_required = [p for p in predictions if not p.auto_resolvable]

    # Summary counts
    total = len(predictions)
    auto_count = len(auto_resolvable)
    manual_count = len(manual_required)

    console.print(f"[dim]Found {total} potential conflict(s): {auto_count} auto-resolvable, {manual_count} manual[/dim]\n")

    # Create table for conflicts
    if manual_required:
        table = Table(show_header=True, header_style="bold yellow")
        table.add_column("File")
        table.add_column("WPs")
        table.add_column("Confidence")

        for pred in manual_required:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps, pred.confidence)

        console.print("[yellow]May require manual resolution:[/yellow]")
        console.print(table)
        console.print()

    if auto_resolvable:
        table = Table(show_header=True, header_style="bold dim")
        table.add_column("Status File")
        table.add_column("WPs")

        for pred in auto_resolvable:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(None, wps)

        console.print("[dim]Auto-resolvable (status files):[/dim]")
        console.print(table)
        console.print()

    # Summary guidance
    if manual_count == 0:
        console.print("[green]All conflicts can be auto-resolved.[/green]\n")
    else:
        console.print(
            f"[yellow]Prepare to resolve {manual_count} conflict(s) manually during merge.[/yellow]\n"
        )


def x_display_conflict_forecast__mutmut_71(
    predictions: list[ConflictPrediction],
    console: Console,
) -> None:
    """Display conflict predictions with Rich formatting.

    Groups predictions into auto-resolvable (status files) and
    manual-required categories for clear user guidance.

    Args:
        predictions: List of ConflictPrediction objects
        console: Rich Console instance for output
    """
    if not predictions:
        console.print("\n[green]No conflicts predicted[/green]\n")
        return

    console.print("\n[bold]Conflict Forecast[/bold]\n")

    auto_resolvable = [p for p in predictions if p.auto_resolvable]
    manual_required = [p for p in predictions if not p.auto_resolvable]

    # Summary counts
    total = len(predictions)
    auto_count = len(auto_resolvable)
    manual_count = len(manual_required)

    console.print(f"[dim]Found {total} potential conflict(s): {auto_count} auto-resolvable, {manual_count} manual[/dim]\n")

    # Create table for conflicts
    if manual_required:
        table = Table(show_header=True, header_style="bold yellow")
        table.add_column("File")
        table.add_column("WPs")
        table.add_column("Confidence")

        for pred in manual_required:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps, pred.confidence)

        console.print("[yellow]May require manual resolution:[/yellow]")
        console.print(table)
        console.print()

    if auto_resolvable:
        table = Table(show_header=True, header_style="bold dim")
        table.add_column("Status File")
        table.add_column("WPs")

        for pred in auto_resolvable:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, None)

        console.print("[dim]Auto-resolvable (status files):[/dim]")
        console.print(table)
        console.print()

    # Summary guidance
    if manual_count == 0:
        console.print("[green]All conflicts can be auto-resolved.[/green]\n")
    else:
        console.print(
            f"[yellow]Prepare to resolve {manual_count} conflict(s) manually during merge.[/yellow]\n"
        )


def x_display_conflict_forecast__mutmut_72(
    predictions: list[ConflictPrediction],
    console: Console,
) -> None:
    """Display conflict predictions with Rich formatting.

    Groups predictions into auto-resolvable (status files) and
    manual-required categories for clear user guidance.

    Args:
        predictions: List of ConflictPrediction objects
        console: Rich Console instance for output
    """
    if not predictions:
        console.print("\n[green]No conflicts predicted[/green]\n")
        return

    console.print("\n[bold]Conflict Forecast[/bold]\n")

    auto_resolvable = [p for p in predictions if p.auto_resolvable]
    manual_required = [p for p in predictions if not p.auto_resolvable]

    # Summary counts
    total = len(predictions)
    auto_count = len(auto_resolvable)
    manual_count = len(manual_required)

    console.print(f"[dim]Found {total} potential conflict(s): {auto_count} auto-resolvable, {manual_count} manual[/dim]\n")

    # Create table for conflicts
    if manual_required:
        table = Table(show_header=True, header_style="bold yellow")
        table.add_column("File")
        table.add_column("WPs")
        table.add_column("Confidence")

        for pred in manual_required:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps, pred.confidence)

        console.print("[yellow]May require manual resolution:[/yellow]")
        console.print(table)
        console.print()

    if auto_resolvable:
        table = Table(show_header=True, header_style="bold dim")
        table.add_column("Status File")
        table.add_column("WPs")

        for pred in auto_resolvable:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(wps)

        console.print("[dim]Auto-resolvable (status files):[/dim]")
        console.print(table)
        console.print()

    # Summary guidance
    if manual_count == 0:
        console.print("[green]All conflicts can be auto-resolved.[/green]\n")
    else:
        console.print(
            f"[yellow]Prepare to resolve {manual_count} conflict(s) manually during merge.[/yellow]\n"
        )


def x_display_conflict_forecast__mutmut_73(
    predictions: list[ConflictPrediction],
    console: Console,
) -> None:
    """Display conflict predictions with Rich formatting.

    Groups predictions into auto-resolvable (status files) and
    manual-required categories for clear user guidance.

    Args:
        predictions: List of ConflictPrediction objects
        console: Rich Console instance for output
    """
    if not predictions:
        console.print("\n[green]No conflicts predicted[/green]\n")
        return

    console.print("\n[bold]Conflict Forecast[/bold]\n")

    auto_resolvable = [p for p in predictions if p.auto_resolvable]
    manual_required = [p for p in predictions if not p.auto_resolvable]

    # Summary counts
    total = len(predictions)
    auto_count = len(auto_resolvable)
    manual_count = len(manual_required)

    console.print(f"[dim]Found {total} potential conflict(s): {auto_count} auto-resolvable, {manual_count} manual[/dim]\n")

    # Create table for conflicts
    if manual_required:
        table = Table(show_header=True, header_style="bold yellow")
        table.add_column("File")
        table.add_column("WPs")
        table.add_column("Confidence")

        for pred in manual_required:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps, pred.confidence)

        console.print("[yellow]May require manual resolution:[/yellow]")
        console.print(table)
        console.print()

    if auto_resolvable:
        table = Table(show_header=True, header_style="bold dim")
        table.add_column("Status File")
        table.add_column("WPs")

        for pred in auto_resolvable:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, )

        console.print("[dim]Auto-resolvable (status files):[/dim]")
        console.print(table)
        console.print()

    # Summary guidance
    if manual_count == 0:
        console.print("[green]All conflicts can be auto-resolved.[/green]\n")
    else:
        console.print(
            f"[yellow]Prepare to resolve {manual_count} conflict(s) manually during merge.[/yellow]\n"
        )


def x_display_conflict_forecast__mutmut_74(
    predictions: list[ConflictPrediction],
    console: Console,
) -> None:
    """Display conflict predictions with Rich formatting.

    Groups predictions into auto-resolvable (status files) and
    manual-required categories for clear user guidance.

    Args:
        predictions: List of ConflictPrediction objects
        console: Rich Console instance for output
    """
    if not predictions:
        console.print("\n[green]No conflicts predicted[/green]\n")
        return

    console.print("\n[bold]Conflict Forecast[/bold]\n")

    auto_resolvable = [p for p in predictions if p.auto_resolvable]
    manual_required = [p for p in predictions if not p.auto_resolvable]

    # Summary counts
    total = len(predictions)
    auto_count = len(auto_resolvable)
    manual_count = len(manual_required)

    console.print(f"[dim]Found {total} potential conflict(s): {auto_count} auto-resolvable, {manual_count} manual[/dim]\n")

    # Create table for conflicts
    if manual_required:
        table = Table(show_header=True, header_style="bold yellow")
        table.add_column("File")
        table.add_column("WPs")
        table.add_column("Confidence")

        for pred in manual_required:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps, pred.confidence)

        console.print("[yellow]May require manual resolution:[/yellow]")
        console.print(table)
        console.print()

    if auto_resolvable:
        table = Table(show_header=True, header_style="bold dim")
        table.add_column("Status File")
        table.add_column("WPs")

        for pred in auto_resolvable:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps)

        console.print(None)
        console.print(table)
        console.print()

    # Summary guidance
    if manual_count == 0:
        console.print("[green]All conflicts can be auto-resolved.[/green]\n")
    else:
        console.print(
            f"[yellow]Prepare to resolve {manual_count} conflict(s) manually during merge.[/yellow]\n"
        )


def x_display_conflict_forecast__mutmut_75(
    predictions: list[ConflictPrediction],
    console: Console,
) -> None:
    """Display conflict predictions with Rich formatting.

    Groups predictions into auto-resolvable (status files) and
    manual-required categories for clear user guidance.

    Args:
        predictions: List of ConflictPrediction objects
        console: Rich Console instance for output
    """
    if not predictions:
        console.print("\n[green]No conflicts predicted[/green]\n")
        return

    console.print("\n[bold]Conflict Forecast[/bold]\n")

    auto_resolvable = [p for p in predictions if p.auto_resolvable]
    manual_required = [p for p in predictions if not p.auto_resolvable]

    # Summary counts
    total = len(predictions)
    auto_count = len(auto_resolvable)
    manual_count = len(manual_required)

    console.print(f"[dim]Found {total} potential conflict(s): {auto_count} auto-resolvable, {manual_count} manual[/dim]\n")

    # Create table for conflicts
    if manual_required:
        table = Table(show_header=True, header_style="bold yellow")
        table.add_column("File")
        table.add_column("WPs")
        table.add_column("Confidence")

        for pred in manual_required:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps, pred.confidence)

        console.print("[yellow]May require manual resolution:[/yellow]")
        console.print(table)
        console.print()

    if auto_resolvable:
        table = Table(show_header=True, header_style="bold dim")
        table.add_column("Status File")
        table.add_column("WPs")

        for pred in auto_resolvable:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps)

        console.print("XX[dim]Auto-resolvable (status files):[/dim]XX")
        console.print(table)
        console.print()

    # Summary guidance
    if manual_count == 0:
        console.print("[green]All conflicts can be auto-resolved.[/green]\n")
    else:
        console.print(
            f"[yellow]Prepare to resolve {manual_count} conflict(s) manually during merge.[/yellow]\n"
        )


def x_display_conflict_forecast__mutmut_76(
    predictions: list[ConflictPrediction],
    console: Console,
) -> None:
    """Display conflict predictions with Rich formatting.

    Groups predictions into auto-resolvable (status files) and
    manual-required categories for clear user guidance.

    Args:
        predictions: List of ConflictPrediction objects
        console: Rich Console instance for output
    """
    if not predictions:
        console.print("\n[green]No conflicts predicted[/green]\n")
        return

    console.print("\n[bold]Conflict Forecast[/bold]\n")

    auto_resolvable = [p for p in predictions if p.auto_resolvable]
    manual_required = [p for p in predictions if not p.auto_resolvable]

    # Summary counts
    total = len(predictions)
    auto_count = len(auto_resolvable)
    manual_count = len(manual_required)

    console.print(f"[dim]Found {total} potential conflict(s): {auto_count} auto-resolvable, {manual_count} manual[/dim]\n")

    # Create table for conflicts
    if manual_required:
        table = Table(show_header=True, header_style="bold yellow")
        table.add_column("File")
        table.add_column("WPs")
        table.add_column("Confidence")

        for pred in manual_required:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps, pred.confidence)

        console.print("[yellow]May require manual resolution:[/yellow]")
        console.print(table)
        console.print()

    if auto_resolvable:
        table = Table(show_header=True, header_style="bold dim")
        table.add_column("Status File")
        table.add_column("WPs")

        for pred in auto_resolvable:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps)

        console.print("[dim]auto-resolvable (status files):[/dim]")
        console.print(table)
        console.print()

    # Summary guidance
    if manual_count == 0:
        console.print("[green]All conflicts can be auto-resolved.[/green]\n")
    else:
        console.print(
            f"[yellow]Prepare to resolve {manual_count} conflict(s) manually during merge.[/yellow]\n"
        )


def x_display_conflict_forecast__mutmut_77(
    predictions: list[ConflictPrediction],
    console: Console,
) -> None:
    """Display conflict predictions with Rich formatting.

    Groups predictions into auto-resolvable (status files) and
    manual-required categories for clear user guidance.

    Args:
        predictions: List of ConflictPrediction objects
        console: Rich Console instance for output
    """
    if not predictions:
        console.print("\n[green]No conflicts predicted[/green]\n")
        return

    console.print("\n[bold]Conflict Forecast[/bold]\n")

    auto_resolvable = [p for p in predictions if p.auto_resolvable]
    manual_required = [p for p in predictions if not p.auto_resolvable]

    # Summary counts
    total = len(predictions)
    auto_count = len(auto_resolvable)
    manual_count = len(manual_required)

    console.print(f"[dim]Found {total} potential conflict(s): {auto_count} auto-resolvable, {manual_count} manual[/dim]\n")

    # Create table for conflicts
    if manual_required:
        table = Table(show_header=True, header_style="bold yellow")
        table.add_column("File")
        table.add_column("WPs")
        table.add_column("Confidence")

        for pred in manual_required:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps, pred.confidence)

        console.print("[yellow]May require manual resolution:[/yellow]")
        console.print(table)
        console.print()

    if auto_resolvable:
        table = Table(show_header=True, header_style="bold dim")
        table.add_column("Status File")
        table.add_column("WPs")

        for pred in auto_resolvable:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps)

        console.print("[DIM]AUTO-RESOLVABLE (STATUS FILES):[/DIM]")
        console.print(table)
        console.print()

    # Summary guidance
    if manual_count == 0:
        console.print("[green]All conflicts can be auto-resolved.[/green]\n")
    else:
        console.print(
            f"[yellow]Prepare to resolve {manual_count} conflict(s) manually during merge.[/yellow]\n"
        )


def x_display_conflict_forecast__mutmut_78(
    predictions: list[ConflictPrediction],
    console: Console,
) -> None:
    """Display conflict predictions with Rich formatting.

    Groups predictions into auto-resolvable (status files) and
    manual-required categories for clear user guidance.

    Args:
        predictions: List of ConflictPrediction objects
        console: Rich Console instance for output
    """
    if not predictions:
        console.print("\n[green]No conflicts predicted[/green]\n")
        return

    console.print("\n[bold]Conflict Forecast[/bold]\n")

    auto_resolvable = [p for p in predictions if p.auto_resolvable]
    manual_required = [p for p in predictions if not p.auto_resolvable]

    # Summary counts
    total = len(predictions)
    auto_count = len(auto_resolvable)
    manual_count = len(manual_required)

    console.print(f"[dim]Found {total} potential conflict(s): {auto_count} auto-resolvable, {manual_count} manual[/dim]\n")

    # Create table for conflicts
    if manual_required:
        table = Table(show_header=True, header_style="bold yellow")
        table.add_column("File")
        table.add_column("WPs")
        table.add_column("Confidence")

        for pred in manual_required:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps, pred.confidence)

        console.print("[yellow]May require manual resolution:[/yellow]")
        console.print(table)
        console.print()

    if auto_resolvable:
        table = Table(show_header=True, header_style="bold dim")
        table.add_column("Status File")
        table.add_column("WPs")

        for pred in auto_resolvable:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps)

        console.print("[dim]Auto-resolvable (status files):[/dim]")
        console.print(None)
        console.print()

    # Summary guidance
    if manual_count == 0:
        console.print("[green]All conflicts can be auto-resolved.[/green]\n")
    else:
        console.print(
            f"[yellow]Prepare to resolve {manual_count} conflict(s) manually during merge.[/yellow]\n"
        )


def x_display_conflict_forecast__mutmut_79(
    predictions: list[ConflictPrediction],
    console: Console,
) -> None:
    """Display conflict predictions with Rich formatting.

    Groups predictions into auto-resolvable (status files) and
    manual-required categories for clear user guidance.

    Args:
        predictions: List of ConflictPrediction objects
        console: Rich Console instance for output
    """
    if not predictions:
        console.print("\n[green]No conflicts predicted[/green]\n")
        return

    console.print("\n[bold]Conflict Forecast[/bold]\n")

    auto_resolvable = [p for p in predictions if p.auto_resolvable]
    manual_required = [p for p in predictions if not p.auto_resolvable]

    # Summary counts
    total = len(predictions)
    auto_count = len(auto_resolvable)
    manual_count = len(manual_required)

    console.print(f"[dim]Found {total} potential conflict(s): {auto_count} auto-resolvable, {manual_count} manual[/dim]\n")

    # Create table for conflicts
    if manual_required:
        table = Table(show_header=True, header_style="bold yellow")
        table.add_column("File")
        table.add_column("WPs")
        table.add_column("Confidence")

        for pred in manual_required:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps, pred.confidence)

        console.print("[yellow]May require manual resolution:[/yellow]")
        console.print(table)
        console.print()

    if auto_resolvable:
        table = Table(show_header=True, header_style="bold dim")
        table.add_column("Status File")
        table.add_column("WPs")

        for pred in auto_resolvable:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps)

        console.print("[dim]Auto-resolvable (status files):[/dim]")
        console.print(table)
        console.print()

    # Summary guidance
    if manual_count != 0:
        console.print("[green]All conflicts can be auto-resolved.[/green]\n")
    else:
        console.print(
            f"[yellow]Prepare to resolve {manual_count} conflict(s) manually during merge.[/yellow]\n"
        )


def x_display_conflict_forecast__mutmut_80(
    predictions: list[ConflictPrediction],
    console: Console,
) -> None:
    """Display conflict predictions with Rich formatting.

    Groups predictions into auto-resolvable (status files) and
    manual-required categories for clear user guidance.

    Args:
        predictions: List of ConflictPrediction objects
        console: Rich Console instance for output
    """
    if not predictions:
        console.print("\n[green]No conflicts predicted[/green]\n")
        return

    console.print("\n[bold]Conflict Forecast[/bold]\n")

    auto_resolvable = [p for p in predictions if p.auto_resolvable]
    manual_required = [p for p in predictions if not p.auto_resolvable]

    # Summary counts
    total = len(predictions)
    auto_count = len(auto_resolvable)
    manual_count = len(manual_required)

    console.print(f"[dim]Found {total} potential conflict(s): {auto_count} auto-resolvable, {manual_count} manual[/dim]\n")

    # Create table for conflicts
    if manual_required:
        table = Table(show_header=True, header_style="bold yellow")
        table.add_column("File")
        table.add_column("WPs")
        table.add_column("Confidence")

        for pred in manual_required:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps, pred.confidence)

        console.print("[yellow]May require manual resolution:[/yellow]")
        console.print(table)
        console.print()

    if auto_resolvable:
        table = Table(show_header=True, header_style="bold dim")
        table.add_column("Status File")
        table.add_column("WPs")

        for pred in auto_resolvable:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps)

        console.print("[dim]Auto-resolvable (status files):[/dim]")
        console.print(table)
        console.print()

    # Summary guidance
    if manual_count == 1:
        console.print("[green]All conflicts can be auto-resolved.[/green]\n")
    else:
        console.print(
            f"[yellow]Prepare to resolve {manual_count} conflict(s) manually during merge.[/yellow]\n"
        )


def x_display_conflict_forecast__mutmut_81(
    predictions: list[ConflictPrediction],
    console: Console,
) -> None:
    """Display conflict predictions with Rich formatting.

    Groups predictions into auto-resolvable (status files) and
    manual-required categories for clear user guidance.

    Args:
        predictions: List of ConflictPrediction objects
        console: Rich Console instance for output
    """
    if not predictions:
        console.print("\n[green]No conflicts predicted[/green]\n")
        return

    console.print("\n[bold]Conflict Forecast[/bold]\n")

    auto_resolvable = [p for p in predictions if p.auto_resolvable]
    manual_required = [p for p in predictions if not p.auto_resolvable]

    # Summary counts
    total = len(predictions)
    auto_count = len(auto_resolvable)
    manual_count = len(manual_required)

    console.print(f"[dim]Found {total} potential conflict(s): {auto_count} auto-resolvable, {manual_count} manual[/dim]\n")

    # Create table for conflicts
    if manual_required:
        table = Table(show_header=True, header_style="bold yellow")
        table.add_column("File")
        table.add_column("WPs")
        table.add_column("Confidence")

        for pred in manual_required:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps, pred.confidence)

        console.print("[yellow]May require manual resolution:[/yellow]")
        console.print(table)
        console.print()

    if auto_resolvable:
        table = Table(show_header=True, header_style="bold dim")
        table.add_column("Status File")
        table.add_column("WPs")

        for pred in auto_resolvable:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps)

        console.print("[dim]Auto-resolvable (status files):[/dim]")
        console.print(table)
        console.print()

    # Summary guidance
    if manual_count == 0:
        console.print(None)
    else:
        console.print(
            f"[yellow]Prepare to resolve {manual_count} conflict(s) manually during merge.[/yellow]\n"
        )


def x_display_conflict_forecast__mutmut_82(
    predictions: list[ConflictPrediction],
    console: Console,
) -> None:
    """Display conflict predictions with Rich formatting.

    Groups predictions into auto-resolvable (status files) and
    manual-required categories for clear user guidance.

    Args:
        predictions: List of ConflictPrediction objects
        console: Rich Console instance for output
    """
    if not predictions:
        console.print("\n[green]No conflicts predicted[/green]\n")
        return

    console.print("\n[bold]Conflict Forecast[/bold]\n")

    auto_resolvable = [p for p in predictions if p.auto_resolvable]
    manual_required = [p for p in predictions if not p.auto_resolvable]

    # Summary counts
    total = len(predictions)
    auto_count = len(auto_resolvable)
    manual_count = len(manual_required)

    console.print(f"[dim]Found {total} potential conflict(s): {auto_count} auto-resolvable, {manual_count} manual[/dim]\n")

    # Create table for conflicts
    if manual_required:
        table = Table(show_header=True, header_style="bold yellow")
        table.add_column("File")
        table.add_column("WPs")
        table.add_column("Confidence")

        for pred in manual_required:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps, pred.confidence)

        console.print("[yellow]May require manual resolution:[/yellow]")
        console.print(table)
        console.print()

    if auto_resolvable:
        table = Table(show_header=True, header_style="bold dim")
        table.add_column("Status File")
        table.add_column("WPs")

        for pred in auto_resolvable:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps)

        console.print("[dim]Auto-resolvable (status files):[/dim]")
        console.print(table)
        console.print()

    # Summary guidance
    if manual_count == 0:
        console.print("XX[green]All conflicts can be auto-resolved.[/green]\nXX")
    else:
        console.print(
            f"[yellow]Prepare to resolve {manual_count} conflict(s) manually during merge.[/yellow]\n"
        )


def x_display_conflict_forecast__mutmut_83(
    predictions: list[ConflictPrediction],
    console: Console,
) -> None:
    """Display conflict predictions with Rich formatting.

    Groups predictions into auto-resolvable (status files) and
    manual-required categories for clear user guidance.

    Args:
        predictions: List of ConflictPrediction objects
        console: Rich Console instance for output
    """
    if not predictions:
        console.print("\n[green]No conflicts predicted[/green]\n")
        return

    console.print("\n[bold]Conflict Forecast[/bold]\n")

    auto_resolvable = [p for p in predictions if p.auto_resolvable]
    manual_required = [p for p in predictions if not p.auto_resolvable]

    # Summary counts
    total = len(predictions)
    auto_count = len(auto_resolvable)
    manual_count = len(manual_required)

    console.print(f"[dim]Found {total} potential conflict(s): {auto_count} auto-resolvable, {manual_count} manual[/dim]\n")

    # Create table for conflicts
    if manual_required:
        table = Table(show_header=True, header_style="bold yellow")
        table.add_column("File")
        table.add_column("WPs")
        table.add_column("Confidence")

        for pred in manual_required:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps, pred.confidence)

        console.print("[yellow]May require manual resolution:[/yellow]")
        console.print(table)
        console.print()

    if auto_resolvable:
        table = Table(show_header=True, header_style="bold dim")
        table.add_column("Status File")
        table.add_column("WPs")

        for pred in auto_resolvable:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps)

        console.print("[dim]Auto-resolvable (status files):[/dim]")
        console.print(table)
        console.print()

    # Summary guidance
    if manual_count == 0:
        console.print("[green]all conflicts can be auto-resolved.[/green]\n")
    else:
        console.print(
            f"[yellow]Prepare to resolve {manual_count} conflict(s) manually during merge.[/yellow]\n"
        )


def x_display_conflict_forecast__mutmut_84(
    predictions: list[ConflictPrediction],
    console: Console,
) -> None:
    """Display conflict predictions with Rich formatting.

    Groups predictions into auto-resolvable (status files) and
    manual-required categories for clear user guidance.

    Args:
        predictions: List of ConflictPrediction objects
        console: Rich Console instance for output
    """
    if not predictions:
        console.print("\n[green]No conflicts predicted[/green]\n")
        return

    console.print("\n[bold]Conflict Forecast[/bold]\n")

    auto_resolvable = [p for p in predictions if p.auto_resolvable]
    manual_required = [p for p in predictions if not p.auto_resolvable]

    # Summary counts
    total = len(predictions)
    auto_count = len(auto_resolvable)
    manual_count = len(manual_required)

    console.print(f"[dim]Found {total} potential conflict(s): {auto_count} auto-resolvable, {manual_count} manual[/dim]\n")

    # Create table for conflicts
    if manual_required:
        table = Table(show_header=True, header_style="bold yellow")
        table.add_column("File")
        table.add_column("WPs")
        table.add_column("Confidence")

        for pred in manual_required:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps, pred.confidence)

        console.print("[yellow]May require manual resolution:[/yellow]")
        console.print(table)
        console.print()

    if auto_resolvable:
        table = Table(show_header=True, header_style="bold dim")
        table.add_column("Status File")
        table.add_column("WPs")

        for pred in auto_resolvable:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps)

        console.print("[dim]Auto-resolvable (status files):[/dim]")
        console.print(table)
        console.print()

    # Summary guidance
    if manual_count == 0:
        console.print("[GREEN]ALL CONFLICTS CAN BE AUTO-RESOLVED.[/GREEN]\n")
    else:
        console.print(
            f"[yellow]Prepare to resolve {manual_count} conflict(s) manually during merge.[/yellow]\n"
        )


def x_display_conflict_forecast__mutmut_85(
    predictions: list[ConflictPrediction],
    console: Console,
) -> None:
    """Display conflict predictions with Rich formatting.

    Groups predictions into auto-resolvable (status files) and
    manual-required categories for clear user guidance.

    Args:
        predictions: List of ConflictPrediction objects
        console: Rich Console instance for output
    """
    if not predictions:
        console.print("\n[green]No conflicts predicted[/green]\n")
        return

    console.print("\n[bold]Conflict Forecast[/bold]\n")

    auto_resolvable = [p for p in predictions if p.auto_resolvable]
    manual_required = [p for p in predictions if not p.auto_resolvable]

    # Summary counts
    total = len(predictions)
    auto_count = len(auto_resolvable)
    manual_count = len(manual_required)

    console.print(f"[dim]Found {total} potential conflict(s): {auto_count} auto-resolvable, {manual_count} manual[/dim]\n")

    # Create table for conflicts
    if manual_required:
        table = Table(show_header=True, header_style="bold yellow")
        table.add_column("File")
        table.add_column("WPs")
        table.add_column("Confidence")

        for pred in manual_required:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps, pred.confidence)

        console.print("[yellow]May require manual resolution:[/yellow]")
        console.print(table)
        console.print()

    if auto_resolvable:
        table = Table(show_header=True, header_style="bold dim")
        table.add_column("Status File")
        table.add_column("WPs")

        for pred in auto_resolvable:
            wps = ", ".join(pred.conflicting_wps)
            table.add_row(pred.file_path, wps)

        console.print("[dim]Auto-resolvable (status files):[/dim]")
        console.print(table)
        console.print()

    # Summary guidance
    if manual_count == 0:
        console.print("[green]All conflicts can be auto-resolved.[/green]\n")
    else:
        console.print(
            None
        )

x_display_conflict_forecast__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_display_conflict_forecast__mutmut_1': x_display_conflict_forecast__mutmut_1, 
    'x_display_conflict_forecast__mutmut_2': x_display_conflict_forecast__mutmut_2, 
    'x_display_conflict_forecast__mutmut_3': x_display_conflict_forecast__mutmut_3, 
    'x_display_conflict_forecast__mutmut_4': x_display_conflict_forecast__mutmut_4, 
    'x_display_conflict_forecast__mutmut_5': x_display_conflict_forecast__mutmut_5, 
    'x_display_conflict_forecast__mutmut_6': x_display_conflict_forecast__mutmut_6, 
    'x_display_conflict_forecast__mutmut_7': x_display_conflict_forecast__mutmut_7, 
    'x_display_conflict_forecast__mutmut_8': x_display_conflict_forecast__mutmut_8, 
    'x_display_conflict_forecast__mutmut_9': x_display_conflict_forecast__mutmut_9, 
    'x_display_conflict_forecast__mutmut_10': x_display_conflict_forecast__mutmut_10, 
    'x_display_conflict_forecast__mutmut_11': x_display_conflict_forecast__mutmut_11, 
    'x_display_conflict_forecast__mutmut_12': x_display_conflict_forecast__mutmut_12, 
    'x_display_conflict_forecast__mutmut_13': x_display_conflict_forecast__mutmut_13, 
    'x_display_conflict_forecast__mutmut_14': x_display_conflict_forecast__mutmut_14, 
    'x_display_conflict_forecast__mutmut_15': x_display_conflict_forecast__mutmut_15, 
    'x_display_conflict_forecast__mutmut_16': x_display_conflict_forecast__mutmut_16, 
    'x_display_conflict_forecast__mutmut_17': x_display_conflict_forecast__mutmut_17, 
    'x_display_conflict_forecast__mutmut_18': x_display_conflict_forecast__mutmut_18, 
    'x_display_conflict_forecast__mutmut_19': x_display_conflict_forecast__mutmut_19, 
    'x_display_conflict_forecast__mutmut_20': x_display_conflict_forecast__mutmut_20, 
    'x_display_conflict_forecast__mutmut_21': x_display_conflict_forecast__mutmut_21, 
    'x_display_conflict_forecast__mutmut_22': x_display_conflict_forecast__mutmut_22, 
    'x_display_conflict_forecast__mutmut_23': x_display_conflict_forecast__mutmut_23, 
    'x_display_conflict_forecast__mutmut_24': x_display_conflict_forecast__mutmut_24, 
    'x_display_conflict_forecast__mutmut_25': x_display_conflict_forecast__mutmut_25, 
    'x_display_conflict_forecast__mutmut_26': x_display_conflict_forecast__mutmut_26, 
    'x_display_conflict_forecast__mutmut_27': x_display_conflict_forecast__mutmut_27, 
    'x_display_conflict_forecast__mutmut_28': x_display_conflict_forecast__mutmut_28, 
    'x_display_conflict_forecast__mutmut_29': x_display_conflict_forecast__mutmut_29, 
    'x_display_conflict_forecast__mutmut_30': x_display_conflict_forecast__mutmut_30, 
    'x_display_conflict_forecast__mutmut_31': x_display_conflict_forecast__mutmut_31, 
    'x_display_conflict_forecast__mutmut_32': x_display_conflict_forecast__mutmut_32, 
    'x_display_conflict_forecast__mutmut_33': x_display_conflict_forecast__mutmut_33, 
    'x_display_conflict_forecast__mutmut_34': x_display_conflict_forecast__mutmut_34, 
    'x_display_conflict_forecast__mutmut_35': x_display_conflict_forecast__mutmut_35, 
    'x_display_conflict_forecast__mutmut_36': x_display_conflict_forecast__mutmut_36, 
    'x_display_conflict_forecast__mutmut_37': x_display_conflict_forecast__mutmut_37, 
    'x_display_conflict_forecast__mutmut_38': x_display_conflict_forecast__mutmut_38, 
    'x_display_conflict_forecast__mutmut_39': x_display_conflict_forecast__mutmut_39, 
    'x_display_conflict_forecast__mutmut_40': x_display_conflict_forecast__mutmut_40, 
    'x_display_conflict_forecast__mutmut_41': x_display_conflict_forecast__mutmut_41, 
    'x_display_conflict_forecast__mutmut_42': x_display_conflict_forecast__mutmut_42, 
    'x_display_conflict_forecast__mutmut_43': x_display_conflict_forecast__mutmut_43, 
    'x_display_conflict_forecast__mutmut_44': x_display_conflict_forecast__mutmut_44, 
    'x_display_conflict_forecast__mutmut_45': x_display_conflict_forecast__mutmut_45, 
    'x_display_conflict_forecast__mutmut_46': x_display_conflict_forecast__mutmut_46, 
    'x_display_conflict_forecast__mutmut_47': x_display_conflict_forecast__mutmut_47, 
    'x_display_conflict_forecast__mutmut_48': x_display_conflict_forecast__mutmut_48, 
    'x_display_conflict_forecast__mutmut_49': x_display_conflict_forecast__mutmut_49, 
    'x_display_conflict_forecast__mutmut_50': x_display_conflict_forecast__mutmut_50, 
    'x_display_conflict_forecast__mutmut_51': x_display_conflict_forecast__mutmut_51, 
    'x_display_conflict_forecast__mutmut_52': x_display_conflict_forecast__mutmut_52, 
    'x_display_conflict_forecast__mutmut_53': x_display_conflict_forecast__mutmut_53, 
    'x_display_conflict_forecast__mutmut_54': x_display_conflict_forecast__mutmut_54, 
    'x_display_conflict_forecast__mutmut_55': x_display_conflict_forecast__mutmut_55, 
    'x_display_conflict_forecast__mutmut_56': x_display_conflict_forecast__mutmut_56, 
    'x_display_conflict_forecast__mutmut_57': x_display_conflict_forecast__mutmut_57, 
    'x_display_conflict_forecast__mutmut_58': x_display_conflict_forecast__mutmut_58, 
    'x_display_conflict_forecast__mutmut_59': x_display_conflict_forecast__mutmut_59, 
    'x_display_conflict_forecast__mutmut_60': x_display_conflict_forecast__mutmut_60, 
    'x_display_conflict_forecast__mutmut_61': x_display_conflict_forecast__mutmut_61, 
    'x_display_conflict_forecast__mutmut_62': x_display_conflict_forecast__mutmut_62, 
    'x_display_conflict_forecast__mutmut_63': x_display_conflict_forecast__mutmut_63, 
    'x_display_conflict_forecast__mutmut_64': x_display_conflict_forecast__mutmut_64, 
    'x_display_conflict_forecast__mutmut_65': x_display_conflict_forecast__mutmut_65, 
    'x_display_conflict_forecast__mutmut_66': x_display_conflict_forecast__mutmut_66, 
    'x_display_conflict_forecast__mutmut_67': x_display_conflict_forecast__mutmut_67, 
    'x_display_conflict_forecast__mutmut_68': x_display_conflict_forecast__mutmut_68, 
    'x_display_conflict_forecast__mutmut_69': x_display_conflict_forecast__mutmut_69, 
    'x_display_conflict_forecast__mutmut_70': x_display_conflict_forecast__mutmut_70, 
    'x_display_conflict_forecast__mutmut_71': x_display_conflict_forecast__mutmut_71, 
    'x_display_conflict_forecast__mutmut_72': x_display_conflict_forecast__mutmut_72, 
    'x_display_conflict_forecast__mutmut_73': x_display_conflict_forecast__mutmut_73, 
    'x_display_conflict_forecast__mutmut_74': x_display_conflict_forecast__mutmut_74, 
    'x_display_conflict_forecast__mutmut_75': x_display_conflict_forecast__mutmut_75, 
    'x_display_conflict_forecast__mutmut_76': x_display_conflict_forecast__mutmut_76, 
    'x_display_conflict_forecast__mutmut_77': x_display_conflict_forecast__mutmut_77, 
    'x_display_conflict_forecast__mutmut_78': x_display_conflict_forecast__mutmut_78, 
    'x_display_conflict_forecast__mutmut_79': x_display_conflict_forecast__mutmut_79, 
    'x_display_conflict_forecast__mutmut_80': x_display_conflict_forecast__mutmut_80, 
    'x_display_conflict_forecast__mutmut_81': x_display_conflict_forecast__mutmut_81, 
    'x_display_conflict_forecast__mutmut_82': x_display_conflict_forecast__mutmut_82, 
    'x_display_conflict_forecast__mutmut_83': x_display_conflict_forecast__mutmut_83, 
    'x_display_conflict_forecast__mutmut_84': x_display_conflict_forecast__mutmut_84, 
    'x_display_conflict_forecast__mutmut_85': x_display_conflict_forecast__mutmut_85
}
x_display_conflict_forecast__mutmut_orig.__name__ = 'x_display_conflict_forecast'
