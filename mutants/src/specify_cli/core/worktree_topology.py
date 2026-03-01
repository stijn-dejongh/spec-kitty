"""Worktree topology analysis for stacked work package branches.

When WPs branch from other WPs (stacking), agents need visibility into the
dependency stack to understand that being "behind main" is expected behavior.
This module materializes the full worktree topology and renders it as structured
JSON for prompt injection.

Key concepts:
- A WP is "stacked" if its base_branch (from workspace context) points to
  another WP's branch rather than the feature's target branch.
- Topology is only injected into prompts when has_stacking is True.
- JSON output is wrapped in HTML comment markers for reliable agent parsing.
"""

from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from specify_cli.core.feature_detection import get_feature_target_branch
from specify_cli.core.dependency_graph import build_dependency_graph, topological_sort
from specify_cli.core.paths import get_main_repo_root
from specify_cli.workspace_context import list_contexts
from specify_cli.frontmatter import read_frontmatter
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
class WPTopologyEntry:
    """Per-WP topology information."""

    wp_id: str
    branch_name: Optional[str]  # None if worktree not yet created
    base_branch: Optional[str]  # None if worktree not yet created
    base_wp: Optional[str]  # WP ID of base, or None if based on target branch
    dependencies: list[str] = field(default_factory=list)
    lane: str = "planned"
    worktree_exists: bool = False
    commits_ahead_of_base: int = 0


@dataclass
class FeatureTopology:
    """Full feature worktree topology."""

    feature_slug: str
    target_branch: str
    entries: list[WPTopologyEntry] = field(default_factory=list)

    @property
    def has_stacking(self) -> bool:
        """True if any WP bases on another WP rather than target branch."""
        return any(e.base_wp is not None for e in self.entries)

    def get_entry(self, wp_id: str) -> Optional[WPTopologyEntry]:
        """Get entry for a specific WP."""
        for entry in self.entries:
            if entry.wp_id == wp_id:
                return entry
        return None

    def get_actual_base_for_wp(self, wp_id: str) -> str:
        """Get the actual base branch for a WP (may be another WP's branch)."""
        entry = self.get_entry(wp_id)
        if entry and entry.base_branch:
            return entry.base_branch
        return self.target_branch


def _resolve_base_wp(
    base_branch: str,
    feature_slug: str,
    wp_branches: dict[str, str],
) -> Optional[str]:
    args = [base_branch, feature_slug, wp_branches]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x__resolve_base_wp__mutmut_orig, x__resolve_base_wp__mutmut_mutants, args, kwargs, None)


def x__resolve_base_wp__mutmut_orig(
    base_branch: str,
    feature_slug: str,
    wp_branches: dict[str, str],
) -> Optional[str]:
    """Determine if base_branch is another WP's branch.

    Args:
        base_branch: The base branch name from workspace context
        feature_slug: Feature slug for pattern matching
        wp_branches: Map of WP ID -> branch name

    Returns:
        WP ID if base is another WP, None if base is target branch
    """
    for wp_id, branch in wp_branches.items():
        if branch == base_branch:
            return wp_id
    return None


def x__resolve_base_wp__mutmut_1(
    base_branch: str,
    feature_slug: str,
    wp_branches: dict[str, str],
) -> Optional[str]:
    """Determine if base_branch is another WP's branch.

    Args:
        base_branch: The base branch name from workspace context
        feature_slug: Feature slug for pattern matching
        wp_branches: Map of WP ID -> branch name

    Returns:
        WP ID if base is another WP, None if base is target branch
    """
    for wp_id, branch in wp_branches.items():
        if branch != base_branch:
            return wp_id
    return None

x__resolve_base_wp__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x__resolve_base_wp__mutmut_1': x__resolve_base_wp__mutmut_1
}
x__resolve_base_wp__mutmut_orig.__name__ = 'x__resolve_base_wp'


def _count_commits_ahead(
    worktree_path: Path,
    base_branch: str,
) -> int:
    args = [worktree_path, base_branch]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x__count_commits_ahead__mutmut_orig, x__count_commits_ahead__mutmut_mutants, args, kwargs, None)


def x__count_commits_ahead__mutmut_orig(
    worktree_path: Path,
    base_branch: str,
) -> int:
    """Count commits ahead of base branch in worktree.

    Returns 0 on any error.
    """
    result = subprocess.run(
        ["git", "rev-list", "--count", f"{base_branch}..HEAD"],
        cwd=worktree_path,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if result.returncode == 0 and result.stdout.strip():
        try:
            return int(result.stdout.strip())
        except ValueError:
            pass
    return 0


def x__count_commits_ahead__mutmut_1(
    worktree_path: Path,
    base_branch: str,
) -> int:
    """Count commits ahead of base branch in worktree.

    Returns 0 on any error.
    """
    result = None
    if result.returncode == 0 and result.stdout.strip():
        try:
            return int(result.stdout.strip())
        except ValueError:
            pass
    return 0


def x__count_commits_ahead__mutmut_2(
    worktree_path: Path,
    base_branch: str,
) -> int:
    """Count commits ahead of base branch in worktree.

    Returns 0 on any error.
    """
    result = subprocess.run(
        None,
        cwd=worktree_path,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if result.returncode == 0 and result.stdout.strip():
        try:
            return int(result.stdout.strip())
        except ValueError:
            pass
    return 0


def x__count_commits_ahead__mutmut_3(
    worktree_path: Path,
    base_branch: str,
) -> int:
    """Count commits ahead of base branch in worktree.

    Returns 0 on any error.
    """
    result = subprocess.run(
        ["git", "rev-list", "--count", f"{base_branch}..HEAD"],
        cwd=None,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if result.returncode == 0 and result.stdout.strip():
        try:
            return int(result.stdout.strip())
        except ValueError:
            pass
    return 0


def x__count_commits_ahead__mutmut_4(
    worktree_path: Path,
    base_branch: str,
) -> int:
    """Count commits ahead of base branch in worktree.

    Returns 0 on any error.
    """
    result = subprocess.run(
        ["git", "rev-list", "--count", f"{base_branch}..HEAD"],
        cwd=worktree_path,
        capture_output=None,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if result.returncode == 0 and result.stdout.strip():
        try:
            return int(result.stdout.strip())
        except ValueError:
            pass
    return 0


def x__count_commits_ahead__mutmut_5(
    worktree_path: Path,
    base_branch: str,
) -> int:
    """Count commits ahead of base branch in worktree.

    Returns 0 on any error.
    """
    result = subprocess.run(
        ["git", "rev-list", "--count", f"{base_branch}..HEAD"],
        cwd=worktree_path,
        capture_output=True,
        text=None,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if result.returncode == 0 and result.stdout.strip():
        try:
            return int(result.stdout.strip())
        except ValueError:
            pass
    return 0


def x__count_commits_ahead__mutmut_6(
    worktree_path: Path,
    base_branch: str,
) -> int:
    """Count commits ahead of base branch in worktree.

    Returns 0 on any error.
    """
    result = subprocess.run(
        ["git", "rev-list", "--count", f"{base_branch}..HEAD"],
        cwd=worktree_path,
        capture_output=True,
        text=True,
        encoding=None,
        errors="replace",
        check=False,
    )
    if result.returncode == 0 and result.stdout.strip():
        try:
            return int(result.stdout.strip())
        except ValueError:
            pass
    return 0


def x__count_commits_ahead__mutmut_7(
    worktree_path: Path,
    base_branch: str,
) -> int:
    """Count commits ahead of base branch in worktree.

    Returns 0 on any error.
    """
    result = subprocess.run(
        ["git", "rev-list", "--count", f"{base_branch}..HEAD"],
        cwd=worktree_path,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors=None,
        check=False,
    )
    if result.returncode == 0 and result.stdout.strip():
        try:
            return int(result.stdout.strip())
        except ValueError:
            pass
    return 0


def x__count_commits_ahead__mutmut_8(
    worktree_path: Path,
    base_branch: str,
) -> int:
    """Count commits ahead of base branch in worktree.

    Returns 0 on any error.
    """
    result = subprocess.run(
        ["git", "rev-list", "--count", f"{base_branch}..HEAD"],
        cwd=worktree_path,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=None,
    )
    if result.returncode == 0 and result.stdout.strip():
        try:
            return int(result.stdout.strip())
        except ValueError:
            pass
    return 0


def x__count_commits_ahead__mutmut_9(
    worktree_path: Path,
    base_branch: str,
) -> int:
    """Count commits ahead of base branch in worktree.

    Returns 0 on any error.
    """
    result = subprocess.run(
        cwd=worktree_path,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if result.returncode == 0 and result.stdout.strip():
        try:
            return int(result.stdout.strip())
        except ValueError:
            pass
    return 0


def x__count_commits_ahead__mutmut_10(
    worktree_path: Path,
    base_branch: str,
) -> int:
    """Count commits ahead of base branch in worktree.

    Returns 0 on any error.
    """
    result = subprocess.run(
        ["git", "rev-list", "--count", f"{base_branch}..HEAD"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if result.returncode == 0 and result.stdout.strip():
        try:
            return int(result.stdout.strip())
        except ValueError:
            pass
    return 0


def x__count_commits_ahead__mutmut_11(
    worktree_path: Path,
    base_branch: str,
) -> int:
    """Count commits ahead of base branch in worktree.

    Returns 0 on any error.
    """
    result = subprocess.run(
        ["git", "rev-list", "--count", f"{base_branch}..HEAD"],
        cwd=worktree_path,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if result.returncode == 0 and result.stdout.strip():
        try:
            return int(result.stdout.strip())
        except ValueError:
            pass
    return 0


def x__count_commits_ahead__mutmut_12(
    worktree_path: Path,
    base_branch: str,
) -> int:
    """Count commits ahead of base branch in worktree.

    Returns 0 on any error.
    """
    result = subprocess.run(
        ["git", "rev-list", "--count", f"{base_branch}..HEAD"],
        cwd=worktree_path,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if result.returncode == 0 and result.stdout.strip():
        try:
            return int(result.stdout.strip())
        except ValueError:
            pass
    return 0


def x__count_commits_ahead__mutmut_13(
    worktree_path: Path,
    base_branch: str,
) -> int:
    """Count commits ahead of base branch in worktree.

    Returns 0 on any error.
    """
    result = subprocess.run(
        ["git", "rev-list", "--count", f"{base_branch}..HEAD"],
        cwd=worktree_path,
        capture_output=True,
        text=True,
        errors="replace",
        check=False,
    )
    if result.returncode == 0 and result.stdout.strip():
        try:
            return int(result.stdout.strip())
        except ValueError:
            pass
    return 0


def x__count_commits_ahead__mutmut_14(
    worktree_path: Path,
    base_branch: str,
) -> int:
    """Count commits ahead of base branch in worktree.

    Returns 0 on any error.
    """
    result = subprocess.run(
        ["git", "rev-list", "--count", f"{base_branch}..HEAD"],
        cwd=worktree_path,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )
    if result.returncode == 0 and result.stdout.strip():
        try:
            return int(result.stdout.strip())
        except ValueError:
            pass
    return 0


def x__count_commits_ahead__mutmut_15(
    worktree_path: Path,
    base_branch: str,
) -> int:
    """Count commits ahead of base branch in worktree.

    Returns 0 on any error.
    """
    result = subprocess.run(
        ["git", "rev-list", "--count", f"{base_branch}..HEAD"],
        cwd=worktree_path,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        )
    if result.returncode == 0 and result.stdout.strip():
        try:
            return int(result.stdout.strip())
        except ValueError:
            pass
    return 0


def x__count_commits_ahead__mutmut_16(
    worktree_path: Path,
    base_branch: str,
) -> int:
    """Count commits ahead of base branch in worktree.

    Returns 0 on any error.
    """
    result = subprocess.run(
        ["XXgitXX", "rev-list", "--count", f"{base_branch}..HEAD"],
        cwd=worktree_path,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if result.returncode == 0 and result.stdout.strip():
        try:
            return int(result.stdout.strip())
        except ValueError:
            pass
    return 0


def x__count_commits_ahead__mutmut_17(
    worktree_path: Path,
    base_branch: str,
) -> int:
    """Count commits ahead of base branch in worktree.

    Returns 0 on any error.
    """
    result = subprocess.run(
        ["GIT", "rev-list", "--count", f"{base_branch}..HEAD"],
        cwd=worktree_path,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if result.returncode == 0 and result.stdout.strip():
        try:
            return int(result.stdout.strip())
        except ValueError:
            pass
    return 0


def x__count_commits_ahead__mutmut_18(
    worktree_path: Path,
    base_branch: str,
) -> int:
    """Count commits ahead of base branch in worktree.

    Returns 0 on any error.
    """
    result = subprocess.run(
        ["git", "XXrev-listXX", "--count", f"{base_branch}..HEAD"],
        cwd=worktree_path,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if result.returncode == 0 and result.stdout.strip():
        try:
            return int(result.stdout.strip())
        except ValueError:
            pass
    return 0


def x__count_commits_ahead__mutmut_19(
    worktree_path: Path,
    base_branch: str,
) -> int:
    """Count commits ahead of base branch in worktree.

    Returns 0 on any error.
    """
    result = subprocess.run(
        ["git", "REV-LIST", "--count", f"{base_branch}..HEAD"],
        cwd=worktree_path,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if result.returncode == 0 and result.stdout.strip():
        try:
            return int(result.stdout.strip())
        except ValueError:
            pass
    return 0


def x__count_commits_ahead__mutmut_20(
    worktree_path: Path,
    base_branch: str,
) -> int:
    """Count commits ahead of base branch in worktree.

    Returns 0 on any error.
    """
    result = subprocess.run(
        ["git", "rev-list", "XX--countXX", f"{base_branch}..HEAD"],
        cwd=worktree_path,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if result.returncode == 0 and result.stdout.strip():
        try:
            return int(result.stdout.strip())
        except ValueError:
            pass
    return 0


def x__count_commits_ahead__mutmut_21(
    worktree_path: Path,
    base_branch: str,
) -> int:
    """Count commits ahead of base branch in worktree.

    Returns 0 on any error.
    """
    result = subprocess.run(
        ["git", "rev-list", "--COUNT", f"{base_branch}..HEAD"],
        cwd=worktree_path,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if result.returncode == 0 and result.stdout.strip():
        try:
            return int(result.stdout.strip())
        except ValueError:
            pass
    return 0


def x__count_commits_ahead__mutmut_22(
    worktree_path: Path,
    base_branch: str,
) -> int:
    """Count commits ahead of base branch in worktree.

    Returns 0 on any error.
    """
    result = subprocess.run(
        ["git", "rev-list", "--count", f"{base_branch}..HEAD"],
        cwd=worktree_path,
        capture_output=False,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if result.returncode == 0 and result.stdout.strip():
        try:
            return int(result.stdout.strip())
        except ValueError:
            pass
    return 0


def x__count_commits_ahead__mutmut_23(
    worktree_path: Path,
    base_branch: str,
) -> int:
    """Count commits ahead of base branch in worktree.

    Returns 0 on any error.
    """
    result = subprocess.run(
        ["git", "rev-list", "--count", f"{base_branch}..HEAD"],
        cwd=worktree_path,
        capture_output=True,
        text=False,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if result.returncode == 0 and result.stdout.strip():
        try:
            return int(result.stdout.strip())
        except ValueError:
            pass
    return 0


def x__count_commits_ahead__mutmut_24(
    worktree_path: Path,
    base_branch: str,
) -> int:
    """Count commits ahead of base branch in worktree.

    Returns 0 on any error.
    """
    result = subprocess.run(
        ["git", "rev-list", "--count", f"{base_branch}..HEAD"],
        cwd=worktree_path,
        capture_output=True,
        text=True,
        encoding="XXutf-8XX",
        errors="replace",
        check=False,
    )
    if result.returncode == 0 and result.stdout.strip():
        try:
            return int(result.stdout.strip())
        except ValueError:
            pass
    return 0


def x__count_commits_ahead__mutmut_25(
    worktree_path: Path,
    base_branch: str,
) -> int:
    """Count commits ahead of base branch in worktree.

    Returns 0 on any error.
    """
    result = subprocess.run(
        ["git", "rev-list", "--count", f"{base_branch}..HEAD"],
        cwd=worktree_path,
        capture_output=True,
        text=True,
        encoding="UTF-8",
        errors="replace",
        check=False,
    )
    if result.returncode == 0 and result.stdout.strip():
        try:
            return int(result.stdout.strip())
        except ValueError:
            pass
    return 0


def x__count_commits_ahead__mutmut_26(
    worktree_path: Path,
    base_branch: str,
) -> int:
    """Count commits ahead of base branch in worktree.

    Returns 0 on any error.
    """
    result = subprocess.run(
        ["git", "rev-list", "--count", f"{base_branch}..HEAD"],
        cwd=worktree_path,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="XXreplaceXX",
        check=False,
    )
    if result.returncode == 0 and result.stdout.strip():
        try:
            return int(result.stdout.strip())
        except ValueError:
            pass
    return 0


def x__count_commits_ahead__mutmut_27(
    worktree_path: Path,
    base_branch: str,
) -> int:
    """Count commits ahead of base branch in worktree.

    Returns 0 on any error.
    """
    result = subprocess.run(
        ["git", "rev-list", "--count", f"{base_branch}..HEAD"],
        cwd=worktree_path,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="REPLACE",
        check=False,
    )
    if result.returncode == 0 and result.stdout.strip():
        try:
            return int(result.stdout.strip())
        except ValueError:
            pass
    return 0


def x__count_commits_ahead__mutmut_28(
    worktree_path: Path,
    base_branch: str,
) -> int:
    """Count commits ahead of base branch in worktree.

    Returns 0 on any error.
    """
    result = subprocess.run(
        ["git", "rev-list", "--count", f"{base_branch}..HEAD"],
        cwd=worktree_path,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=True,
    )
    if result.returncode == 0 and result.stdout.strip():
        try:
            return int(result.stdout.strip())
        except ValueError:
            pass
    return 0


def x__count_commits_ahead__mutmut_29(
    worktree_path: Path,
    base_branch: str,
) -> int:
    """Count commits ahead of base branch in worktree.

    Returns 0 on any error.
    """
    result = subprocess.run(
        ["git", "rev-list", "--count", f"{base_branch}..HEAD"],
        cwd=worktree_path,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if result.returncode == 0 or result.stdout.strip():
        try:
            return int(result.stdout.strip())
        except ValueError:
            pass
    return 0


def x__count_commits_ahead__mutmut_30(
    worktree_path: Path,
    base_branch: str,
) -> int:
    """Count commits ahead of base branch in worktree.

    Returns 0 on any error.
    """
    result = subprocess.run(
        ["git", "rev-list", "--count", f"{base_branch}..HEAD"],
        cwd=worktree_path,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if result.returncode != 0 and result.stdout.strip():
        try:
            return int(result.stdout.strip())
        except ValueError:
            pass
    return 0


def x__count_commits_ahead__mutmut_31(
    worktree_path: Path,
    base_branch: str,
) -> int:
    """Count commits ahead of base branch in worktree.

    Returns 0 on any error.
    """
    result = subprocess.run(
        ["git", "rev-list", "--count", f"{base_branch}..HEAD"],
        cwd=worktree_path,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if result.returncode == 1 and result.stdout.strip():
        try:
            return int(result.stdout.strip())
        except ValueError:
            pass
    return 0


def x__count_commits_ahead__mutmut_32(
    worktree_path: Path,
    base_branch: str,
) -> int:
    """Count commits ahead of base branch in worktree.

    Returns 0 on any error.
    """
    result = subprocess.run(
        ["git", "rev-list", "--count", f"{base_branch}..HEAD"],
        cwd=worktree_path,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if result.returncode == 0 and result.stdout.strip():
        try:
            return int(None)
        except ValueError:
            pass
    return 0


def x__count_commits_ahead__mutmut_33(
    worktree_path: Path,
    base_branch: str,
) -> int:
    """Count commits ahead of base branch in worktree.

    Returns 0 on any error.
    """
    result = subprocess.run(
        ["git", "rev-list", "--count", f"{base_branch}..HEAD"],
        cwd=worktree_path,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if result.returncode == 0 and result.stdout.strip():
        try:
            return int(result.stdout.strip())
        except ValueError:
            pass
    return 1

x__count_commits_ahead__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x__count_commits_ahead__mutmut_1': x__count_commits_ahead__mutmut_1, 
    'x__count_commits_ahead__mutmut_2': x__count_commits_ahead__mutmut_2, 
    'x__count_commits_ahead__mutmut_3': x__count_commits_ahead__mutmut_3, 
    'x__count_commits_ahead__mutmut_4': x__count_commits_ahead__mutmut_4, 
    'x__count_commits_ahead__mutmut_5': x__count_commits_ahead__mutmut_5, 
    'x__count_commits_ahead__mutmut_6': x__count_commits_ahead__mutmut_6, 
    'x__count_commits_ahead__mutmut_7': x__count_commits_ahead__mutmut_7, 
    'x__count_commits_ahead__mutmut_8': x__count_commits_ahead__mutmut_8, 
    'x__count_commits_ahead__mutmut_9': x__count_commits_ahead__mutmut_9, 
    'x__count_commits_ahead__mutmut_10': x__count_commits_ahead__mutmut_10, 
    'x__count_commits_ahead__mutmut_11': x__count_commits_ahead__mutmut_11, 
    'x__count_commits_ahead__mutmut_12': x__count_commits_ahead__mutmut_12, 
    'x__count_commits_ahead__mutmut_13': x__count_commits_ahead__mutmut_13, 
    'x__count_commits_ahead__mutmut_14': x__count_commits_ahead__mutmut_14, 
    'x__count_commits_ahead__mutmut_15': x__count_commits_ahead__mutmut_15, 
    'x__count_commits_ahead__mutmut_16': x__count_commits_ahead__mutmut_16, 
    'x__count_commits_ahead__mutmut_17': x__count_commits_ahead__mutmut_17, 
    'x__count_commits_ahead__mutmut_18': x__count_commits_ahead__mutmut_18, 
    'x__count_commits_ahead__mutmut_19': x__count_commits_ahead__mutmut_19, 
    'x__count_commits_ahead__mutmut_20': x__count_commits_ahead__mutmut_20, 
    'x__count_commits_ahead__mutmut_21': x__count_commits_ahead__mutmut_21, 
    'x__count_commits_ahead__mutmut_22': x__count_commits_ahead__mutmut_22, 
    'x__count_commits_ahead__mutmut_23': x__count_commits_ahead__mutmut_23, 
    'x__count_commits_ahead__mutmut_24': x__count_commits_ahead__mutmut_24, 
    'x__count_commits_ahead__mutmut_25': x__count_commits_ahead__mutmut_25, 
    'x__count_commits_ahead__mutmut_26': x__count_commits_ahead__mutmut_26, 
    'x__count_commits_ahead__mutmut_27': x__count_commits_ahead__mutmut_27, 
    'x__count_commits_ahead__mutmut_28': x__count_commits_ahead__mutmut_28, 
    'x__count_commits_ahead__mutmut_29': x__count_commits_ahead__mutmut_29, 
    'x__count_commits_ahead__mutmut_30': x__count_commits_ahead__mutmut_30, 
    'x__count_commits_ahead__mutmut_31': x__count_commits_ahead__mutmut_31, 
    'x__count_commits_ahead__mutmut_32': x__count_commits_ahead__mutmut_32, 
    'x__count_commits_ahead__mutmut_33': x__count_commits_ahead__mutmut_33
}
x__count_commits_ahead__mutmut_orig.__name__ = 'x__count_commits_ahead'


def materialize_worktree_topology(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    args = [repo_root, feature_slug]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_materialize_worktree_topology__mutmut_orig, x_materialize_worktree_topology__mutmut_mutants, args, kwargs, None)


def x_materialize_worktree_topology__mutmut_orig(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_1(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = None
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_2(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(None)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_3(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = None

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_4(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(None, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_5(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, None)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_6(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_7(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, )

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_8(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = None
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_9(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" * feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_10(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root * "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_11(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "XXkitty-specsXX" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_12(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "KITTY-SPECS" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_13(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = None

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_14(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(None)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_15(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = None
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_16(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(None)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_17(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = None

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_18(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(None)

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_19(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = None
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_20(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(None)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_21(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = None

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_22(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug != feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_23(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = None
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_24(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = None

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_25(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = None
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_26(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir * "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_27(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "XXtasksXX"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_28(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "TASKS"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_29(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = None
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_30(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob(None):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_31(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("XXWP*.mdXX"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_32(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("wp*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_33(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.MD"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_34(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = None
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_35(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(None)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_36(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = None
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_37(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get(None, wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_38(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", None)
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_39(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get(wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_40(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", )
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_41(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("XXwork_package_idXX", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_42(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("WORK_PACKAGE_ID", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_43(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split(None)[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_44(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("XX-XX")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_45(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[1])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_46(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = None
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_47(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get(None, "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_48(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", None)
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_49(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_50(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", )
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_51(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("XXlaneXX", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_52(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("LANE", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_53(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "XXplannedXX")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_54(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "PLANNED")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_55(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = None
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_56(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = None
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_57(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(None)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_58(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_59(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_60(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = None
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_61(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(None, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_62(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, None)
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_63(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get([])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_64(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, )
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_65(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = None

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_66(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(None, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_67(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, None)

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_68(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get("planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_69(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, )

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_70(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "XXplannedXX")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_71(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "PLANNED")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_72(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = ""
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_73(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = None

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_74(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(None, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_75(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, None, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_76(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, None)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_77(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_78(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_79(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, )

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_80(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = None
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_81(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 1
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_82(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = None
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_83(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" * f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_84(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root * ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_85(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / "XX.worktreesXX" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_86(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".WORKTREES" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_87(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = None
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_88(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists or base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_89(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = None

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_90(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(None, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_91(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, None)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_92(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_93(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, )

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_94(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(None)

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_95(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=None,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_96(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=None,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_97(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=None,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_98(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=None,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_99(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=None,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_100(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=None,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_101(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=None,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_102(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=None,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_103(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_104(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_105(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_106(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_107(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_108(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_109(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_110(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_111(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=None,
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_112(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=None,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_113(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        entries=None,
    )


def x_materialize_worktree_topology__mutmut_114(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        target_branch=target_branch,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_115(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        entries=entries,
    )


def x_materialize_worktree_topology__mutmut_116(
    repo_root: Path,
    feature_slug: str,
) -> FeatureTopology:
    """Gather the full worktree topology for a feature.

    Combines workspace contexts, WP frontmatter, dependency graph,
    and git rev-list counts into a complete topology view.

    Args:
        repo_root: Main repository root path
        feature_slug: Feature slug (e.g., "002-event-driven")

    Returns:
        FeatureTopology with all WP entries in topological order
    """
    main_repo_root = get_main_repo_root(repo_root)
    target_branch = get_feature_target_branch(main_repo_root, feature_slug)

    feature_dir = main_repo_root / "kitty-specs" / feature_slug
    graph = build_dependency_graph(feature_dir)

    # Get topological order (dependencies before dependents)
    try:
        topo_order = topological_sort(graph)
    except ValueError:
        # Cycle detected — fall back to sorted keys
        topo_order = sorted(graph.keys())

    # Build WP branch map from workspace contexts
    contexts = list_contexts(main_repo_root)
    feature_contexts = {
        ctx.wp_id: ctx
        for ctx in contexts
        if ctx.feature_slug == feature_slug
    }

    # Map WP ID -> branch name for base resolution
    wp_branches: dict[str, str] = {}
    for wp_id, ctx in feature_contexts.items():
        wp_branches[wp_id] = ctx.branch_name

    # Read lane status from WP frontmatter
    tasks_dir = feature_dir / "tasks"
    wp_lanes: dict[str, str] = {}
    if tasks_dir.exists():
        for wp_file in tasks_dir.glob("WP*.md"):
            try:
                fm, _ = read_frontmatter(wp_file)
                wp_id = fm.get("work_package_id", wp_file.stem.split("-")[0])
                wp_lanes[wp_id] = fm.get("lane", "planned")
            except Exception:
                pass

    # Build topology entries
    entries: list[WPTopologyEntry] = []
    for wp_id in topo_order:
        ctx = feature_contexts.get(wp_id)
        branch_name = ctx.branch_name if ctx else None
        base_branch = ctx.base_branch if ctx else None
        dependencies = graph.get(wp_id, [])
        lane = wp_lanes.get(wp_id, "planned")

        # Determine if base is another WP
        base_wp = None
        if base_branch:
            base_wp = _resolve_base_wp(base_branch, feature_slug, wp_branches)

        # Count commits ahead of base
        commits_ahead = 0
        worktree_path = main_repo_root / ".worktrees" / f"{feature_slug}-{wp_id}"
        worktree_exists = worktree_path.exists()
        if worktree_exists and base_branch:
            commits_ahead = _count_commits_ahead(worktree_path, base_branch)

        entries.append(WPTopologyEntry(
            wp_id=wp_id,
            branch_name=branch_name,
            base_branch=base_branch,
            base_wp=base_wp,
            dependencies=dependencies,
            lane=lane,
            worktree_exists=worktree_exists,
            commits_ahead_of_base=commits_ahead,
        ))

    return FeatureTopology(
        feature_slug=feature_slug,
        target_branch=target_branch,
        )

x_materialize_worktree_topology__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_materialize_worktree_topology__mutmut_1': x_materialize_worktree_topology__mutmut_1, 
    'x_materialize_worktree_topology__mutmut_2': x_materialize_worktree_topology__mutmut_2, 
    'x_materialize_worktree_topology__mutmut_3': x_materialize_worktree_topology__mutmut_3, 
    'x_materialize_worktree_topology__mutmut_4': x_materialize_worktree_topology__mutmut_4, 
    'x_materialize_worktree_topology__mutmut_5': x_materialize_worktree_topology__mutmut_5, 
    'x_materialize_worktree_topology__mutmut_6': x_materialize_worktree_topology__mutmut_6, 
    'x_materialize_worktree_topology__mutmut_7': x_materialize_worktree_topology__mutmut_7, 
    'x_materialize_worktree_topology__mutmut_8': x_materialize_worktree_topology__mutmut_8, 
    'x_materialize_worktree_topology__mutmut_9': x_materialize_worktree_topology__mutmut_9, 
    'x_materialize_worktree_topology__mutmut_10': x_materialize_worktree_topology__mutmut_10, 
    'x_materialize_worktree_topology__mutmut_11': x_materialize_worktree_topology__mutmut_11, 
    'x_materialize_worktree_topology__mutmut_12': x_materialize_worktree_topology__mutmut_12, 
    'x_materialize_worktree_topology__mutmut_13': x_materialize_worktree_topology__mutmut_13, 
    'x_materialize_worktree_topology__mutmut_14': x_materialize_worktree_topology__mutmut_14, 
    'x_materialize_worktree_topology__mutmut_15': x_materialize_worktree_topology__mutmut_15, 
    'x_materialize_worktree_topology__mutmut_16': x_materialize_worktree_topology__mutmut_16, 
    'x_materialize_worktree_topology__mutmut_17': x_materialize_worktree_topology__mutmut_17, 
    'x_materialize_worktree_topology__mutmut_18': x_materialize_worktree_topology__mutmut_18, 
    'x_materialize_worktree_topology__mutmut_19': x_materialize_worktree_topology__mutmut_19, 
    'x_materialize_worktree_topology__mutmut_20': x_materialize_worktree_topology__mutmut_20, 
    'x_materialize_worktree_topology__mutmut_21': x_materialize_worktree_topology__mutmut_21, 
    'x_materialize_worktree_topology__mutmut_22': x_materialize_worktree_topology__mutmut_22, 
    'x_materialize_worktree_topology__mutmut_23': x_materialize_worktree_topology__mutmut_23, 
    'x_materialize_worktree_topology__mutmut_24': x_materialize_worktree_topology__mutmut_24, 
    'x_materialize_worktree_topology__mutmut_25': x_materialize_worktree_topology__mutmut_25, 
    'x_materialize_worktree_topology__mutmut_26': x_materialize_worktree_topology__mutmut_26, 
    'x_materialize_worktree_topology__mutmut_27': x_materialize_worktree_topology__mutmut_27, 
    'x_materialize_worktree_topology__mutmut_28': x_materialize_worktree_topology__mutmut_28, 
    'x_materialize_worktree_topology__mutmut_29': x_materialize_worktree_topology__mutmut_29, 
    'x_materialize_worktree_topology__mutmut_30': x_materialize_worktree_topology__mutmut_30, 
    'x_materialize_worktree_topology__mutmut_31': x_materialize_worktree_topology__mutmut_31, 
    'x_materialize_worktree_topology__mutmut_32': x_materialize_worktree_topology__mutmut_32, 
    'x_materialize_worktree_topology__mutmut_33': x_materialize_worktree_topology__mutmut_33, 
    'x_materialize_worktree_topology__mutmut_34': x_materialize_worktree_topology__mutmut_34, 
    'x_materialize_worktree_topology__mutmut_35': x_materialize_worktree_topology__mutmut_35, 
    'x_materialize_worktree_topology__mutmut_36': x_materialize_worktree_topology__mutmut_36, 
    'x_materialize_worktree_topology__mutmut_37': x_materialize_worktree_topology__mutmut_37, 
    'x_materialize_worktree_topology__mutmut_38': x_materialize_worktree_topology__mutmut_38, 
    'x_materialize_worktree_topology__mutmut_39': x_materialize_worktree_topology__mutmut_39, 
    'x_materialize_worktree_topology__mutmut_40': x_materialize_worktree_topology__mutmut_40, 
    'x_materialize_worktree_topology__mutmut_41': x_materialize_worktree_topology__mutmut_41, 
    'x_materialize_worktree_topology__mutmut_42': x_materialize_worktree_topology__mutmut_42, 
    'x_materialize_worktree_topology__mutmut_43': x_materialize_worktree_topology__mutmut_43, 
    'x_materialize_worktree_topology__mutmut_44': x_materialize_worktree_topology__mutmut_44, 
    'x_materialize_worktree_topology__mutmut_45': x_materialize_worktree_topology__mutmut_45, 
    'x_materialize_worktree_topology__mutmut_46': x_materialize_worktree_topology__mutmut_46, 
    'x_materialize_worktree_topology__mutmut_47': x_materialize_worktree_topology__mutmut_47, 
    'x_materialize_worktree_topology__mutmut_48': x_materialize_worktree_topology__mutmut_48, 
    'x_materialize_worktree_topology__mutmut_49': x_materialize_worktree_topology__mutmut_49, 
    'x_materialize_worktree_topology__mutmut_50': x_materialize_worktree_topology__mutmut_50, 
    'x_materialize_worktree_topology__mutmut_51': x_materialize_worktree_topology__mutmut_51, 
    'x_materialize_worktree_topology__mutmut_52': x_materialize_worktree_topology__mutmut_52, 
    'x_materialize_worktree_topology__mutmut_53': x_materialize_worktree_topology__mutmut_53, 
    'x_materialize_worktree_topology__mutmut_54': x_materialize_worktree_topology__mutmut_54, 
    'x_materialize_worktree_topology__mutmut_55': x_materialize_worktree_topology__mutmut_55, 
    'x_materialize_worktree_topology__mutmut_56': x_materialize_worktree_topology__mutmut_56, 
    'x_materialize_worktree_topology__mutmut_57': x_materialize_worktree_topology__mutmut_57, 
    'x_materialize_worktree_topology__mutmut_58': x_materialize_worktree_topology__mutmut_58, 
    'x_materialize_worktree_topology__mutmut_59': x_materialize_worktree_topology__mutmut_59, 
    'x_materialize_worktree_topology__mutmut_60': x_materialize_worktree_topology__mutmut_60, 
    'x_materialize_worktree_topology__mutmut_61': x_materialize_worktree_topology__mutmut_61, 
    'x_materialize_worktree_topology__mutmut_62': x_materialize_worktree_topology__mutmut_62, 
    'x_materialize_worktree_topology__mutmut_63': x_materialize_worktree_topology__mutmut_63, 
    'x_materialize_worktree_topology__mutmut_64': x_materialize_worktree_topology__mutmut_64, 
    'x_materialize_worktree_topology__mutmut_65': x_materialize_worktree_topology__mutmut_65, 
    'x_materialize_worktree_topology__mutmut_66': x_materialize_worktree_topology__mutmut_66, 
    'x_materialize_worktree_topology__mutmut_67': x_materialize_worktree_topology__mutmut_67, 
    'x_materialize_worktree_topology__mutmut_68': x_materialize_worktree_topology__mutmut_68, 
    'x_materialize_worktree_topology__mutmut_69': x_materialize_worktree_topology__mutmut_69, 
    'x_materialize_worktree_topology__mutmut_70': x_materialize_worktree_topology__mutmut_70, 
    'x_materialize_worktree_topology__mutmut_71': x_materialize_worktree_topology__mutmut_71, 
    'x_materialize_worktree_topology__mutmut_72': x_materialize_worktree_topology__mutmut_72, 
    'x_materialize_worktree_topology__mutmut_73': x_materialize_worktree_topology__mutmut_73, 
    'x_materialize_worktree_topology__mutmut_74': x_materialize_worktree_topology__mutmut_74, 
    'x_materialize_worktree_topology__mutmut_75': x_materialize_worktree_topology__mutmut_75, 
    'x_materialize_worktree_topology__mutmut_76': x_materialize_worktree_topology__mutmut_76, 
    'x_materialize_worktree_topology__mutmut_77': x_materialize_worktree_topology__mutmut_77, 
    'x_materialize_worktree_topology__mutmut_78': x_materialize_worktree_topology__mutmut_78, 
    'x_materialize_worktree_topology__mutmut_79': x_materialize_worktree_topology__mutmut_79, 
    'x_materialize_worktree_topology__mutmut_80': x_materialize_worktree_topology__mutmut_80, 
    'x_materialize_worktree_topology__mutmut_81': x_materialize_worktree_topology__mutmut_81, 
    'x_materialize_worktree_topology__mutmut_82': x_materialize_worktree_topology__mutmut_82, 
    'x_materialize_worktree_topology__mutmut_83': x_materialize_worktree_topology__mutmut_83, 
    'x_materialize_worktree_topology__mutmut_84': x_materialize_worktree_topology__mutmut_84, 
    'x_materialize_worktree_topology__mutmut_85': x_materialize_worktree_topology__mutmut_85, 
    'x_materialize_worktree_topology__mutmut_86': x_materialize_worktree_topology__mutmut_86, 
    'x_materialize_worktree_topology__mutmut_87': x_materialize_worktree_topology__mutmut_87, 
    'x_materialize_worktree_topology__mutmut_88': x_materialize_worktree_topology__mutmut_88, 
    'x_materialize_worktree_topology__mutmut_89': x_materialize_worktree_topology__mutmut_89, 
    'x_materialize_worktree_topology__mutmut_90': x_materialize_worktree_topology__mutmut_90, 
    'x_materialize_worktree_topology__mutmut_91': x_materialize_worktree_topology__mutmut_91, 
    'x_materialize_worktree_topology__mutmut_92': x_materialize_worktree_topology__mutmut_92, 
    'x_materialize_worktree_topology__mutmut_93': x_materialize_worktree_topology__mutmut_93, 
    'x_materialize_worktree_topology__mutmut_94': x_materialize_worktree_topology__mutmut_94, 
    'x_materialize_worktree_topology__mutmut_95': x_materialize_worktree_topology__mutmut_95, 
    'x_materialize_worktree_topology__mutmut_96': x_materialize_worktree_topology__mutmut_96, 
    'x_materialize_worktree_topology__mutmut_97': x_materialize_worktree_topology__mutmut_97, 
    'x_materialize_worktree_topology__mutmut_98': x_materialize_worktree_topology__mutmut_98, 
    'x_materialize_worktree_topology__mutmut_99': x_materialize_worktree_topology__mutmut_99, 
    'x_materialize_worktree_topology__mutmut_100': x_materialize_worktree_topology__mutmut_100, 
    'x_materialize_worktree_topology__mutmut_101': x_materialize_worktree_topology__mutmut_101, 
    'x_materialize_worktree_topology__mutmut_102': x_materialize_worktree_topology__mutmut_102, 
    'x_materialize_worktree_topology__mutmut_103': x_materialize_worktree_topology__mutmut_103, 
    'x_materialize_worktree_topology__mutmut_104': x_materialize_worktree_topology__mutmut_104, 
    'x_materialize_worktree_topology__mutmut_105': x_materialize_worktree_topology__mutmut_105, 
    'x_materialize_worktree_topology__mutmut_106': x_materialize_worktree_topology__mutmut_106, 
    'x_materialize_worktree_topology__mutmut_107': x_materialize_worktree_topology__mutmut_107, 
    'x_materialize_worktree_topology__mutmut_108': x_materialize_worktree_topology__mutmut_108, 
    'x_materialize_worktree_topology__mutmut_109': x_materialize_worktree_topology__mutmut_109, 
    'x_materialize_worktree_topology__mutmut_110': x_materialize_worktree_topology__mutmut_110, 
    'x_materialize_worktree_topology__mutmut_111': x_materialize_worktree_topology__mutmut_111, 
    'x_materialize_worktree_topology__mutmut_112': x_materialize_worktree_topology__mutmut_112, 
    'x_materialize_worktree_topology__mutmut_113': x_materialize_worktree_topology__mutmut_113, 
    'x_materialize_worktree_topology__mutmut_114': x_materialize_worktree_topology__mutmut_114, 
    'x_materialize_worktree_topology__mutmut_115': x_materialize_worktree_topology__mutmut_115, 
    'x_materialize_worktree_topology__mutmut_116': x_materialize_worktree_topology__mutmut_116
}
x_materialize_worktree_topology__mutmut_orig.__name__ = 'x_materialize_worktree_topology'


def render_topology_json(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    args = [topology, current_wp_id]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_render_topology_json__mutmut_orig, x_render_topology_json__mutmut_mutants, args, kwargs, None)


def x_render_topology_json__mutmut_orig(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as structured JSON for prompt injection.

    Only call this when topology.has_stacking is True.
    Output is wrapped in HTML comment markers for reliable agent parsing.

    Args:
        topology: Feature topology data
        current_wp_id: The WP being implemented/reviewed

    Returns:
        List of lines to append to prompt
    """
    current_entry = topology.get_entry(current_wp_id)

    # Build base info for current WP
    your_base = None
    if current_entry and current_entry.base_wp:
        your_base = {
            "branch": current_entry.base_branch,
            "wp": current_entry.base_wp,
        }

    # Build diff command
    diff_base = topology.get_actual_base_for_wp(current_wp_id)
    diff_command = f"git diff {diff_base}..HEAD"

    # Build entries list
    entries_json = []
    for entry in topology.entries:
        entry_data: dict = {
            "wp": entry.wp_id,
            "lane": entry.lane,
            "branch": entry.branch_name,
            "base": entry.base_wp if entry.base_wp else topology.target_branch,
        }
        if entry.worktree_exists:
            entry_data["commits_ahead"] = entry.commits_ahead_of_base
        if entry.dependencies and not entry.worktree_exists:
            entry_data["dependencies"] = entry.dependencies
        entries_json.append(entry_data)

    payload = {
        "feature": topology.feature_slug,
        "target_branch": topology.target_branch,
        "current_wp": current_wp_id,
        "your_base": your_base,
        "diff_command": diff_command,
        "stacked": True,
        "note": f"Your branch stacks on {current_entry.base_wp}, NOT {topology.target_branch}. Do not worry about being 'behind {topology.target_branch}'."
            if current_entry and current_entry.base_wp
            else f"Your branch is based on {topology.target_branch}. Other WPs in this feature use stacking.",
        "entries": entries_json,
    }

    lines = [
        "<!-- WORKTREE_TOPOLOGY -->",
        json.dumps(payload, indent=2),
        "<!-- /WORKTREE_TOPOLOGY -->",
    ]
    return lines


def x_render_topology_json__mutmut_1(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as structured JSON for prompt injection.

    Only call this when topology.has_stacking is True.
    Output is wrapped in HTML comment markers for reliable agent parsing.

    Args:
        topology: Feature topology data
        current_wp_id: The WP being implemented/reviewed

    Returns:
        List of lines to append to prompt
    """
    current_entry = None

    # Build base info for current WP
    your_base = None
    if current_entry and current_entry.base_wp:
        your_base = {
            "branch": current_entry.base_branch,
            "wp": current_entry.base_wp,
        }

    # Build diff command
    diff_base = topology.get_actual_base_for_wp(current_wp_id)
    diff_command = f"git diff {diff_base}..HEAD"

    # Build entries list
    entries_json = []
    for entry in topology.entries:
        entry_data: dict = {
            "wp": entry.wp_id,
            "lane": entry.lane,
            "branch": entry.branch_name,
            "base": entry.base_wp if entry.base_wp else topology.target_branch,
        }
        if entry.worktree_exists:
            entry_data["commits_ahead"] = entry.commits_ahead_of_base
        if entry.dependencies and not entry.worktree_exists:
            entry_data["dependencies"] = entry.dependencies
        entries_json.append(entry_data)

    payload = {
        "feature": topology.feature_slug,
        "target_branch": topology.target_branch,
        "current_wp": current_wp_id,
        "your_base": your_base,
        "diff_command": diff_command,
        "stacked": True,
        "note": f"Your branch stacks on {current_entry.base_wp}, NOT {topology.target_branch}. Do not worry about being 'behind {topology.target_branch}'."
            if current_entry and current_entry.base_wp
            else f"Your branch is based on {topology.target_branch}. Other WPs in this feature use stacking.",
        "entries": entries_json,
    }

    lines = [
        "<!-- WORKTREE_TOPOLOGY -->",
        json.dumps(payload, indent=2),
        "<!-- /WORKTREE_TOPOLOGY -->",
    ]
    return lines


def x_render_topology_json__mutmut_2(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as structured JSON for prompt injection.

    Only call this when topology.has_stacking is True.
    Output is wrapped in HTML comment markers for reliable agent parsing.

    Args:
        topology: Feature topology data
        current_wp_id: The WP being implemented/reviewed

    Returns:
        List of lines to append to prompt
    """
    current_entry = topology.get_entry(None)

    # Build base info for current WP
    your_base = None
    if current_entry and current_entry.base_wp:
        your_base = {
            "branch": current_entry.base_branch,
            "wp": current_entry.base_wp,
        }

    # Build diff command
    diff_base = topology.get_actual_base_for_wp(current_wp_id)
    diff_command = f"git diff {diff_base}..HEAD"

    # Build entries list
    entries_json = []
    for entry in topology.entries:
        entry_data: dict = {
            "wp": entry.wp_id,
            "lane": entry.lane,
            "branch": entry.branch_name,
            "base": entry.base_wp if entry.base_wp else topology.target_branch,
        }
        if entry.worktree_exists:
            entry_data["commits_ahead"] = entry.commits_ahead_of_base
        if entry.dependencies and not entry.worktree_exists:
            entry_data["dependencies"] = entry.dependencies
        entries_json.append(entry_data)

    payload = {
        "feature": topology.feature_slug,
        "target_branch": topology.target_branch,
        "current_wp": current_wp_id,
        "your_base": your_base,
        "diff_command": diff_command,
        "stacked": True,
        "note": f"Your branch stacks on {current_entry.base_wp}, NOT {topology.target_branch}. Do not worry about being 'behind {topology.target_branch}'."
            if current_entry and current_entry.base_wp
            else f"Your branch is based on {topology.target_branch}. Other WPs in this feature use stacking.",
        "entries": entries_json,
    }

    lines = [
        "<!-- WORKTREE_TOPOLOGY -->",
        json.dumps(payload, indent=2),
        "<!-- /WORKTREE_TOPOLOGY -->",
    ]
    return lines


def x_render_topology_json__mutmut_3(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as structured JSON for prompt injection.

    Only call this when topology.has_stacking is True.
    Output is wrapped in HTML comment markers for reliable agent parsing.

    Args:
        topology: Feature topology data
        current_wp_id: The WP being implemented/reviewed

    Returns:
        List of lines to append to prompt
    """
    current_entry = topology.get_entry(current_wp_id)

    # Build base info for current WP
    your_base = ""
    if current_entry and current_entry.base_wp:
        your_base = {
            "branch": current_entry.base_branch,
            "wp": current_entry.base_wp,
        }

    # Build diff command
    diff_base = topology.get_actual_base_for_wp(current_wp_id)
    diff_command = f"git diff {diff_base}..HEAD"

    # Build entries list
    entries_json = []
    for entry in topology.entries:
        entry_data: dict = {
            "wp": entry.wp_id,
            "lane": entry.lane,
            "branch": entry.branch_name,
            "base": entry.base_wp if entry.base_wp else topology.target_branch,
        }
        if entry.worktree_exists:
            entry_data["commits_ahead"] = entry.commits_ahead_of_base
        if entry.dependencies and not entry.worktree_exists:
            entry_data["dependencies"] = entry.dependencies
        entries_json.append(entry_data)

    payload = {
        "feature": topology.feature_slug,
        "target_branch": topology.target_branch,
        "current_wp": current_wp_id,
        "your_base": your_base,
        "diff_command": diff_command,
        "stacked": True,
        "note": f"Your branch stacks on {current_entry.base_wp}, NOT {topology.target_branch}. Do not worry about being 'behind {topology.target_branch}'."
            if current_entry and current_entry.base_wp
            else f"Your branch is based on {topology.target_branch}. Other WPs in this feature use stacking.",
        "entries": entries_json,
    }

    lines = [
        "<!-- WORKTREE_TOPOLOGY -->",
        json.dumps(payload, indent=2),
        "<!-- /WORKTREE_TOPOLOGY -->",
    ]
    return lines


def x_render_topology_json__mutmut_4(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as structured JSON for prompt injection.

    Only call this when topology.has_stacking is True.
    Output is wrapped in HTML comment markers for reliable agent parsing.

    Args:
        topology: Feature topology data
        current_wp_id: The WP being implemented/reviewed

    Returns:
        List of lines to append to prompt
    """
    current_entry = topology.get_entry(current_wp_id)

    # Build base info for current WP
    your_base = None
    if current_entry or current_entry.base_wp:
        your_base = {
            "branch": current_entry.base_branch,
            "wp": current_entry.base_wp,
        }

    # Build diff command
    diff_base = topology.get_actual_base_for_wp(current_wp_id)
    diff_command = f"git diff {diff_base}..HEAD"

    # Build entries list
    entries_json = []
    for entry in topology.entries:
        entry_data: dict = {
            "wp": entry.wp_id,
            "lane": entry.lane,
            "branch": entry.branch_name,
            "base": entry.base_wp if entry.base_wp else topology.target_branch,
        }
        if entry.worktree_exists:
            entry_data["commits_ahead"] = entry.commits_ahead_of_base
        if entry.dependencies and not entry.worktree_exists:
            entry_data["dependencies"] = entry.dependencies
        entries_json.append(entry_data)

    payload = {
        "feature": topology.feature_slug,
        "target_branch": topology.target_branch,
        "current_wp": current_wp_id,
        "your_base": your_base,
        "diff_command": diff_command,
        "stacked": True,
        "note": f"Your branch stacks on {current_entry.base_wp}, NOT {topology.target_branch}. Do not worry about being 'behind {topology.target_branch}'."
            if current_entry and current_entry.base_wp
            else f"Your branch is based on {topology.target_branch}. Other WPs in this feature use stacking.",
        "entries": entries_json,
    }

    lines = [
        "<!-- WORKTREE_TOPOLOGY -->",
        json.dumps(payload, indent=2),
        "<!-- /WORKTREE_TOPOLOGY -->",
    ]
    return lines


def x_render_topology_json__mutmut_5(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as structured JSON for prompt injection.

    Only call this when topology.has_stacking is True.
    Output is wrapped in HTML comment markers for reliable agent parsing.

    Args:
        topology: Feature topology data
        current_wp_id: The WP being implemented/reviewed

    Returns:
        List of lines to append to prompt
    """
    current_entry = topology.get_entry(current_wp_id)

    # Build base info for current WP
    your_base = None
    if current_entry and current_entry.base_wp:
        your_base = None

    # Build diff command
    diff_base = topology.get_actual_base_for_wp(current_wp_id)
    diff_command = f"git diff {diff_base}..HEAD"

    # Build entries list
    entries_json = []
    for entry in topology.entries:
        entry_data: dict = {
            "wp": entry.wp_id,
            "lane": entry.lane,
            "branch": entry.branch_name,
            "base": entry.base_wp if entry.base_wp else topology.target_branch,
        }
        if entry.worktree_exists:
            entry_data["commits_ahead"] = entry.commits_ahead_of_base
        if entry.dependencies and not entry.worktree_exists:
            entry_data["dependencies"] = entry.dependencies
        entries_json.append(entry_data)

    payload = {
        "feature": topology.feature_slug,
        "target_branch": topology.target_branch,
        "current_wp": current_wp_id,
        "your_base": your_base,
        "diff_command": diff_command,
        "stacked": True,
        "note": f"Your branch stacks on {current_entry.base_wp}, NOT {topology.target_branch}. Do not worry about being 'behind {topology.target_branch}'."
            if current_entry and current_entry.base_wp
            else f"Your branch is based on {topology.target_branch}. Other WPs in this feature use stacking.",
        "entries": entries_json,
    }

    lines = [
        "<!-- WORKTREE_TOPOLOGY -->",
        json.dumps(payload, indent=2),
        "<!-- /WORKTREE_TOPOLOGY -->",
    ]
    return lines


def x_render_topology_json__mutmut_6(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as structured JSON for prompt injection.

    Only call this when topology.has_stacking is True.
    Output is wrapped in HTML comment markers for reliable agent parsing.

    Args:
        topology: Feature topology data
        current_wp_id: The WP being implemented/reviewed

    Returns:
        List of lines to append to prompt
    """
    current_entry = topology.get_entry(current_wp_id)

    # Build base info for current WP
    your_base = None
    if current_entry and current_entry.base_wp:
        your_base = {
            "XXbranchXX": current_entry.base_branch,
            "wp": current_entry.base_wp,
        }

    # Build diff command
    diff_base = topology.get_actual_base_for_wp(current_wp_id)
    diff_command = f"git diff {diff_base}..HEAD"

    # Build entries list
    entries_json = []
    for entry in topology.entries:
        entry_data: dict = {
            "wp": entry.wp_id,
            "lane": entry.lane,
            "branch": entry.branch_name,
            "base": entry.base_wp if entry.base_wp else topology.target_branch,
        }
        if entry.worktree_exists:
            entry_data["commits_ahead"] = entry.commits_ahead_of_base
        if entry.dependencies and not entry.worktree_exists:
            entry_data["dependencies"] = entry.dependencies
        entries_json.append(entry_data)

    payload = {
        "feature": topology.feature_slug,
        "target_branch": topology.target_branch,
        "current_wp": current_wp_id,
        "your_base": your_base,
        "diff_command": diff_command,
        "stacked": True,
        "note": f"Your branch stacks on {current_entry.base_wp}, NOT {topology.target_branch}. Do not worry about being 'behind {topology.target_branch}'."
            if current_entry and current_entry.base_wp
            else f"Your branch is based on {topology.target_branch}. Other WPs in this feature use stacking.",
        "entries": entries_json,
    }

    lines = [
        "<!-- WORKTREE_TOPOLOGY -->",
        json.dumps(payload, indent=2),
        "<!-- /WORKTREE_TOPOLOGY -->",
    ]
    return lines


def x_render_topology_json__mutmut_7(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as structured JSON for prompt injection.

    Only call this when topology.has_stacking is True.
    Output is wrapped in HTML comment markers for reliable agent parsing.

    Args:
        topology: Feature topology data
        current_wp_id: The WP being implemented/reviewed

    Returns:
        List of lines to append to prompt
    """
    current_entry = topology.get_entry(current_wp_id)

    # Build base info for current WP
    your_base = None
    if current_entry and current_entry.base_wp:
        your_base = {
            "BRANCH": current_entry.base_branch,
            "wp": current_entry.base_wp,
        }

    # Build diff command
    diff_base = topology.get_actual_base_for_wp(current_wp_id)
    diff_command = f"git diff {diff_base}..HEAD"

    # Build entries list
    entries_json = []
    for entry in topology.entries:
        entry_data: dict = {
            "wp": entry.wp_id,
            "lane": entry.lane,
            "branch": entry.branch_name,
            "base": entry.base_wp if entry.base_wp else topology.target_branch,
        }
        if entry.worktree_exists:
            entry_data["commits_ahead"] = entry.commits_ahead_of_base
        if entry.dependencies and not entry.worktree_exists:
            entry_data["dependencies"] = entry.dependencies
        entries_json.append(entry_data)

    payload = {
        "feature": topology.feature_slug,
        "target_branch": topology.target_branch,
        "current_wp": current_wp_id,
        "your_base": your_base,
        "diff_command": diff_command,
        "stacked": True,
        "note": f"Your branch stacks on {current_entry.base_wp}, NOT {topology.target_branch}. Do not worry about being 'behind {topology.target_branch}'."
            if current_entry and current_entry.base_wp
            else f"Your branch is based on {topology.target_branch}. Other WPs in this feature use stacking.",
        "entries": entries_json,
    }

    lines = [
        "<!-- WORKTREE_TOPOLOGY -->",
        json.dumps(payload, indent=2),
        "<!-- /WORKTREE_TOPOLOGY -->",
    ]
    return lines


def x_render_topology_json__mutmut_8(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as structured JSON for prompt injection.

    Only call this when topology.has_stacking is True.
    Output is wrapped in HTML comment markers for reliable agent parsing.

    Args:
        topology: Feature topology data
        current_wp_id: The WP being implemented/reviewed

    Returns:
        List of lines to append to prompt
    """
    current_entry = topology.get_entry(current_wp_id)

    # Build base info for current WP
    your_base = None
    if current_entry and current_entry.base_wp:
        your_base = {
            "branch": current_entry.base_branch,
            "XXwpXX": current_entry.base_wp,
        }

    # Build diff command
    diff_base = topology.get_actual_base_for_wp(current_wp_id)
    diff_command = f"git diff {diff_base}..HEAD"

    # Build entries list
    entries_json = []
    for entry in topology.entries:
        entry_data: dict = {
            "wp": entry.wp_id,
            "lane": entry.lane,
            "branch": entry.branch_name,
            "base": entry.base_wp if entry.base_wp else topology.target_branch,
        }
        if entry.worktree_exists:
            entry_data["commits_ahead"] = entry.commits_ahead_of_base
        if entry.dependencies and not entry.worktree_exists:
            entry_data["dependencies"] = entry.dependencies
        entries_json.append(entry_data)

    payload = {
        "feature": topology.feature_slug,
        "target_branch": topology.target_branch,
        "current_wp": current_wp_id,
        "your_base": your_base,
        "diff_command": diff_command,
        "stacked": True,
        "note": f"Your branch stacks on {current_entry.base_wp}, NOT {topology.target_branch}. Do not worry about being 'behind {topology.target_branch}'."
            if current_entry and current_entry.base_wp
            else f"Your branch is based on {topology.target_branch}. Other WPs in this feature use stacking.",
        "entries": entries_json,
    }

    lines = [
        "<!-- WORKTREE_TOPOLOGY -->",
        json.dumps(payload, indent=2),
        "<!-- /WORKTREE_TOPOLOGY -->",
    ]
    return lines


def x_render_topology_json__mutmut_9(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as structured JSON for prompt injection.

    Only call this when topology.has_stacking is True.
    Output is wrapped in HTML comment markers for reliable agent parsing.

    Args:
        topology: Feature topology data
        current_wp_id: The WP being implemented/reviewed

    Returns:
        List of lines to append to prompt
    """
    current_entry = topology.get_entry(current_wp_id)

    # Build base info for current WP
    your_base = None
    if current_entry and current_entry.base_wp:
        your_base = {
            "branch": current_entry.base_branch,
            "WP": current_entry.base_wp,
        }

    # Build diff command
    diff_base = topology.get_actual_base_for_wp(current_wp_id)
    diff_command = f"git diff {diff_base}..HEAD"

    # Build entries list
    entries_json = []
    for entry in topology.entries:
        entry_data: dict = {
            "wp": entry.wp_id,
            "lane": entry.lane,
            "branch": entry.branch_name,
            "base": entry.base_wp if entry.base_wp else topology.target_branch,
        }
        if entry.worktree_exists:
            entry_data["commits_ahead"] = entry.commits_ahead_of_base
        if entry.dependencies and not entry.worktree_exists:
            entry_data["dependencies"] = entry.dependencies
        entries_json.append(entry_data)

    payload = {
        "feature": topology.feature_slug,
        "target_branch": topology.target_branch,
        "current_wp": current_wp_id,
        "your_base": your_base,
        "diff_command": diff_command,
        "stacked": True,
        "note": f"Your branch stacks on {current_entry.base_wp}, NOT {topology.target_branch}. Do not worry about being 'behind {topology.target_branch}'."
            if current_entry and current_entry.base_wp
            else f"Your branch is based on {topology.target_branch}. Other WPs in this feature use stacking.",
        "entries": entries_json,
    }

    lines = [
        "<!-- WORKTREE_TOPOLOGY -->",
        json.dumps(payload, indent=2),
        "<!-- /WORKTREE_TOPOLOGY -->",
    ]
    return lines


def x_render_topology_json__mutmut_10(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as structured JSON for prompt injection.

    Only call this when topology.has_stacking is True.
    Output is wrapped in HTML comment markers for reliable agent parsing.

    Args:
        topology: Feature topology data
        current_wp_id: The WP being implemented/reviewed

    Returns:
        List of lines to append to prompt
    """
    current_entry = topology.get_entry(current_wp_id)

    # Build base info for current WP
    your_base = None
    if current_entry and current_entry.base_wp:
        your_base = {
            "branch": current_entry.base_branch,
            "wp": current_entry.base_wp,
        }

    # Build diff command
    diff_base = None
    diff_command = f"git diff {diff_base}..HEAD"

    # Build entries list
    entries_json = []
    for entry in topology.entries:
        entry_data: dict = {
            "wp": entry.wp_id,
            "lane": entry.lane,
            "branch": entry.branch_name,
            "base": entry.base_wp if entry.base_wp else topology.target_branch,
        }
        if entry.worktree_exists:
            entry_data["commits_ahead"] = entry.commits_ahead_of_base
        if entry.dependencies and not entry.worktree_exists:
            entry_data["dependencies"] = entry.dependencies
        entries_json.append(entry_data)

    payload = {
        "feature": topology.feature_slug,
        "target_branch": topology.target_branch,
        "current_wp": current_wp_id,
        "your_base": your_base,
        "diff_command": diff_command,
        "stacked": True,
        "note": f"Your branch stacks on {current_entry.base_wp}, NOT {topology.target_branch}. Do not worry about being 'behind {topology.target_branch}'."
            if current_entry and current_entry.base_wp
            else f"Your branch is based on {topology.target_branch}. Other WPs in this feature use stacking.",
        "entries": entries_json,
    }

    lines = [
        "<!-- WORKTREE_TOPOLOGY -->",
        json.dumps(payload, indent=2),
        "<!-- /WORKTREE_TOPOLOGY -->",
    ]
    return lines


def x_render_topology_json__mutmut_11(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as structured JSON for prompt injection.

    Only call this when topology.has_stacking is True.
    Output is wrapped in HTML comment markers for reliable agent parsing.

    Args:
        topology: Feature topology data
        current_wp_id: The WP being implemented/reviewed

    Returns:
        List of lines to append to prompt
    """
    current_entry = topology.get_entry(current_wp_id)

    # Build base info for current WP
    your_base = None
    if current_entry and current_entry.base_wp:
        your_base = {
            "branch": current_entry.base_branch,
            "wp": current_entry.base_wp,
        }

    # Build diff command
    diff_base = topology.get_actual_base_for_wp(None)
    diff_command = f"git diff {diff_base}..HEAD"

    # Build entries list
    entries_json = []
    for entry in topology.entries:
        entry_data: dict = {
            "wp": entry.wp_id,
            "lane": entry.lane,
            "branch": entry.branch_name,
            "base": entry.base_wp if entry.base_wp else topology.target_branch,
        }
        if entry.worktree_exists:
            entry_data["commits_ahead"] = entry.commits_ahead_of_base
        if entry.dependencies and not entry.worktree_exists:
            entry_data["dependencies"] = entry.dependencies
        entries_json.append(entry_data)

    payload = {
        "feature": topology.feature_slug,
        "target_branch": topology.target_branch,
        "current_wp": current_wp_id,
        "your_base": your_base,
        "diff_command": diff_command,
        "stacked": True,
        "note": f"Your branch stacks on {current_entry.base_wp}, NOT {topology.target_branch}. Do not worry about being 'behind {topology.target_branch}'."
            if current_entry and current_entry.base_wp
            else f"Your branch is based on {topology.target_branch}. Other WPs in this feature use stacking.",
        "entries": entries_json,
    }

    lines = [
        "<!-- WORKTREE_TOPOLOGY -->",
        json.dumps(payload, indent=2),
        "<!-- /WORKTREE_TOPOLOGY -->",
    ]
    return lines


def x_render_topology_json__mutmut_12(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as structured JSON for prompt injection.

    Only call this when topology.has_stacking is True.
    Output is wrapped in HTML comment markers for reliable agent parsing.

    Args:
        topology: Feature topology data
        current_wp_id: The WP being implemented/reviewed

    Returns:
        List of lines to append to prompt
    """
    current_entry = topology.get_entry(current_wp_id)

    # Build base info for current WP
    your_base = None
    if current_entry and current_entry.base_wp:
        your_base = {
            "branch": current_entry.base_branch,
            "wp": current_entry.base_wp,
        }

    # Build diff command
    diff_base = topology.get_actual_base_for_wp(current_wp_id)
    diff_command = None

    # Build entries list
    entries_json = []
    for entry in topology.entries:
        entry_data: dict = {
            "wp": entry.wp_id,
            "lane": entry.lane,
            "branch": entry.branch_name,
            "base": entry.base_wp if entry.base_wp else topology.target_branch,
        }
        if entry.worktree_exists:
            entry_data["commits_ahead"] = entry.commits_ahead_of_base
        if entry.dependencies and not entry.worktree_exists:
            entry_data["dependencies"] = entry.dependencies
        entries_json.append(entry_data)

    payload = {
        "feature": topology.feature_slug,
        "target_branch": topology.target_branch,
        "current_wp": current_wp_id,
        "your_base": your_base,
        "diff_command": diff_command,
        "stacked": True,
        "note": f"Your branch stacks on {current_entry.base_wp}, NOT {topology.target_branch}. Do not worry about being 'behind {topology.target_branch}'."
            if current_entry and current_entry.base_wp
            else f"Your branch is based on {topology.target_branch}. Other WPs in this feature use stacking.",
        "entries": entries_json,
    }

    lines = [
        "<!-- WORKTREE_TOPOLOGY -->",
        json.dumps(payload, indent=2),
        "<!-- /WORKTREE_TOPOLOGY -->",
    ]
    return lines


def x_render_topology_json__mutmut_13(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as structured JSON for prompt injection.

    Only call this when topology.has_stacking is True.
    Output is wrapped in HTML comment markers for reliable agent parsing.

    Args:
        topology: Feature topology data
        current_wp_id: The WP being implemented/reviewed

    Returns:
        List of lines to append to prompt
    """
    current_entry = topology.get_entry(current_wp_id)

    # Build base info for current WP
    your_base = None
    if current_entry and current_entry.base_wp:
        your_base = {
            "branch": current_entry.base_branch,
            "wp": current_entry.base_wp,
        }

    # Build diff command
    diff_base = topology.get_actual_base_for_wp(current_wp_id)
    diff_command = f"git diff {diff_base}..HEAD"

    # Build entries list
    entries_json = None
    for entry in topology.entries:
        entry_data: dict = {
            "wp": entry.wp_id,
            "lane": entry.lane,
            "branch": entry.branch_name,
            "base": entry.base_wp if entry.base_wp else topology.target_branch,
        }
        if entry.worktree_exists:
            entry_data["commits_ahead"] = entry.commits_ahead_of_base
        if entry.dependencies and not entry.worktree_exists:
            entry_data["dependencies"] = entry.dependencies
        entries_json.append(entry_data)

    payload = {
        "feature": topology.feature_slug,
        "target_branch": topology.target_branch,
        "current_wp": current_wp_id,
        "your_base": your_base,
        "diff_command": diff_command,
        "stacked": True,
        "note": f"Your branch stacks on {current_entry.base_wp}, NOT {topology.target_branch}. Do not worry about being 'behind {topology.target_branch}'."
            if current_entry and current_entry.base_wp
            else f"Your branch is based on {topology.target_branch}. Other WPs in this feature use stacking.",
        "entries": entries_json,
    }

    lines = [
        "<!-- WORKTREE_TOPOLOGY -->",
        json.dumps(payload, indent=2),
        "<!-- /WORKTREE_TOPOLOGY -->",
    ]
    return lines


def x_render_topology_json__mutmut_14(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as structured JSON for prompt injection.

    Only call this when topology.has_stacking is True.
    Output is wrapped in HTML comment markers for reliable agent parsing.

    Args:
        topology: Feature topology data
        current_wp_id: The WP being implemented/reviewed

    Returns:
        List of lines to append to prompt
    """
    current_entry = topology.get_entry(current_wp_id)

    # Build base info for current WP
    your_base = None
    if current_entry and current_entry.base_wp:
        your_base = {
            "branch": current_entry.base_branch,
            "wp": current_entry.base_wp,
        }

    # Build diff command
    diff_base = topology.get_actual_base_for_wp(current_wp_id)
    diff_command = f"git diff {diff_base}..HEAD"

    # Build entries list
    entries_json = []
    for entry in topology.entries:
        entry_data: dict = None
        if entry.worktree_exists:
            entry_data["commits_ahead"] = entry.commits_ahead_of_base
        if entry.dependencies and not entry.worktree_exists:
            entry_data["dependencies"] = entry.dependencies
        entries_json.append(entry_data)

    payload = {
        "feature": topology.feature_slug,
        "target_branch": topology.target_branch,
        "current_wp": current_wp_id,
        "your_base": your_base,
        "diff_command": diff_command,
        "stacked": True,
        "note": f"Your branch stacks on {current_entry.base_wp}, NOT {topology.target_branch}. Do not worry about being 'behind {topology.target_branch}'."
            if current_entry and current_entry.base_wp
            else f"Your branch is based on {topology.target_branch}. Other WPs in this feature use stacking.",
        "entries": entries_json,
    }

    lines = [
        "<!-- WORKTREE_TOPOLOGY -->",
        json.dumps(payload, indent=2),
        "<!-- /WORKTREE_TOPOLOGY -->",
    ]
    return lines


def x_render_topology_json__mutmut_15(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as structured JSON for prompt injection.

    Only call this when topology.has_stacking is True.
    Output is wrapped in HTML comment markers for reliable agent parsing.

    Args:
        topology: Feature topology data
        current_wp_id: The WP being implemented/reviewed

    Returns:
        List of lines to append to prompt
    """
    current_entry = topology.get_entry(current_wp_id)

    # Build base info for current WP
    your_base = None
    if current_entry and current_entry.base_wp:
        your_base = {
            "branch": current_entry.base_branch,
            "wp": current_entry.base_wp,
        }

    # Build diff command
    diff_base = topology.get_actual_base_for_wp(current_wp_id)
    diff_command = f"git diff {diff_base}..HEAD"

    # Build entries list
    entries_json = []
    for entry in topology.entries:
        entry_data: dict = {
            "XXwpXX": entry.wp_id,
            "lane": entry.lane,
            "branch": entry.branch_name,
            "base": entry.base_wp if entry.base_wp else topology.target_branch,
        }
        if entry.worktree_exists:
            entry_data["commits_ahead"] = entry.commits_ahead_of_base
        if entry.dependencies and not entry.worktree_exists:
            entry_data["dependencies"] = entry.dependencies
        entries_json.append(entry_data)

    payload = {
        "feature": topology.feature_slug,
        "target_branch": topology.target_branch,
        "current_wp": current_wp_id,
        "your_base": your_base,
        "diff_command": diff_command,
        "stacked": True,
        "note": f"Your branch stacks on {current_entry.base_wp}, NOT {topology.target_branch}. Do not worry about being 'behind {topology.target_branch}'."
            if current_entry and current_entry.base_wp
            else f"Your branch is based on {topology.target_branch}. Other WPs in this feature use stacking.",
        "entries": entries_json,
    }

    lines = [
        "<!-- WORKTREE_TOPOLOGY -->",
        json.dumps(payload, indent=2),
        "<!-- /WORKTREE_TOPOLOGY -->",
    ]
    return lines


def x_render_topology_json__mutmut_16(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as structured JSON for prompt injection.

    Only call this when topology.has_stacking is True.
    Output is wrapped in HTML comment markers for reliable agent parsing.

    Args:
        topology: Feature topology data
        current_wp_id: The WP being implemented/reviewed

    Returns:
        List of lines to append to prompt
    """
    current_entry = topology.get_entry(current_wp_id)

    # Build base info for current WP
    your_base = None
    if current_entry and current_entry.base_wp:
        your_base = {
            "branch": current_entry.base_branch,
            "wp": current_entry.base_wp,
        }

    # Build diff command
    diff_base = topology.get_actual_base_for_wp(current_wp_id)
    diff_command = f"git diff {diff_base}..HEAD"

    # Build entries list
    entries_json = []
    for entry in topology.entries:
        entry_data: dict = {
            "WP": entry.wp_id,
            "lane": entry.lane,
            "branch": entry.branch_name,
            "base": entry.base_wp if entry.base_wp else topology.target_branch,
        }
        if entry.worktree_exists:
            entry_data["commits_ahead"] = entry.commits_ahead_of_base
        if entry.dependencies and not entry.worktree_exists:
            entry_data["dependencies"] = entry.dependencies
        entries_json.append(entry_data)

    payload = {
        "feature": topology.feature_slug,
        "target_branch": topology.target_branch,
        "current_wp": current_wp_id,
        "your_base": your_base,
        "diff_command": diff_command,
        "stacked": True,
        "note": f"Your branch stacks on {current_entry.base_wp}, NOT {topology.target_branch}. Do not worry about being 'behind {topology.target_branch}'."
            if current_entry and current_entry.base_wp
            else f"Your branch is based on {topology.target_branch}. Other WPs in this feature use stacking.",
        "entries": entries_json,
    }

    lines = [
        "<!-- WORKTREE_TOPOLOGY -->",
        json.dumps(payload, indent=2),
        "<!-- /WORKTREE_TOPOLOGY -->",
    ]
    return lines


def x_render_topology_json__mutmut_17(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as structured JSON for prompt injection.

    Only call this when topology.has_stacking is True.
    Output is wrapped in HTML comment markers for reliable agent parsing.

    Args:
        topology: Feature topology data
        current_wp_id: The WP being implemented/reviewed

    Returns:
        List of lines to append to prompt
    """
    current_entry = topology.get_entry(current_wp_id)

    # Build base info for current WP
    your_base = None
    if current_entry and current_entry.base_wp:
        your_base = {
            "branch": current_entry.base_branch,
            "wp": current_entry.base_wp,
        }

    # Build diff command
    diff_base = topology.get_actual_base_for_wp(current_wp_id)
    diff_command = f"git diff {diff_base}..HEAD"

    # Build entries list
    entries_json = []
    for entry in topology.entries:
        entry_data: dict = {
            "wp": entry.wp_id,
            "XXlaneXX": entry.lane,
            "branch": entry.branch_name,
            "base": entry.base_wp if entry.base_wp else topology.target_branch,
        }
        if entry.worktree_exists:
            entry_data["commits_ahead"] = entry.commits_ahead_of_base
        if entry.dependencies and not entry.worktree_exists:
            entry_data["dependencies"] = entry.dependencies
        entries_json.append(entry_data)

    payload = {
        "feature": topology.feature_slug,
        "target_branch": topology.target_branch,
        "current_wp": current_wp_id,
        "your_base": your_base,
        "diff_command": diff_command,
        "stacked": True,
        "note": f"Your branch stacks on {current_entry.base_wp}, NOT {topology.target_branch}. Do not worry about being 'behind {topology.target_branch}'."
            if current_entry and current_entry.base_wp
            else f"Your branch is based on {topology.target_branch}. Other WPs in this feature use stacking.",
        "entries": entries_json,
    }

    lines = [
        "<!-- WORKTREE_TOPOLOGY -->",
        json.dumps(payload, indent=2),
        "<!-- /WORKTREE_TOPOLOGY -->",
    ]
    return lines


def x_render_topology_json__mutmut_18(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as structured JSON for prompt injection.

    Only call this when topology.has_stacking is True.
    Output is wrapped in HTML comment markers for reliable agent parsing.

    Args:
        topology: Feature topology data
        current_wp_id: The WP being implemented/reviewed

    Returns:
        List of lines to append to prompt
    """
    current_entry = topology.get_entry(current_wp_id)

    # Build base info for current WP
    your_base = None
    if current_entry and current_entry.base_wp:
        your_base = {
            "branch": current_entry.base_branch,
            "wp": current_entry.base_wp,
        }

    # Build diff command
    diff_base = topology.get_actual_base_for_wp(current_wp_id)
    diff_command = f"git diff {diff_base}..HEAD"

    # Build entries list
    entries_json = []
    for entry in topology.entries:
        entry_data: dict = {
            "wp": entry.wp_id,
            "LANE": entry.lane,
            "branch": entry.branch_name,
            "base": entry.base_wp if entry.base_wp else topology.target_branch,
        }
        if entry.worktree_exists:
            entry_data["commits_ahead"] = entry.commits_ahead_of_base
        if entry.dependencies and not entry.worktree_exists:
            entry_data["dependencies"] = entry.dependencies
        entries_json.append(entry_data)

    payload = {
        "feature": topology.feature_slug,
        "target_branch": topology.target_branch,
        "current_wp": current_wp_id,
        "your_base": your_base,
        "diff_command": diff_command,
        "stacked": True,
        "note": f"Your branch stacks on {current_entry.base_wp}, NOT {topology.target_branch}. Do not worry about being 'behind {topology.target_branch}'."
            if current_entry and current_entry.base_wp
            else f"Your branch is based on {topology.target_branch}. Other WPs in this feature use stacking.",
        "entries": entries_json,
    }

    lines = [
        "<!-- WORKTREE_TOPOLOGY -->",
        json.dumps(payload, indent=2),
        "<!-- /WORKTREE_TOPOLOGY -->",
    ]
    return lines


def x_render_topology_json__mutmut_19(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as structured JSON for prompt injection.

    Only call this when topology.has_stacking is True.
    Output is wrapped in HTML comment markers for reliable agent parsing.

    Args:
        topology: Feature topology data
        current_wp_id: The WP being implemented/reviewed

    Returns:
        List of lines to append to prompt
    """
    current_entry = topology.get_entry(current_wp_id)

    # Build base info for current WP
    your_base = None
    if current_entry and current_entry.base_wp:
        your_base = {
            "branch": current_entry.base_branch,
            "wp": current_entry.base_wp,
        }

    # Build diff command
    diff_base = topology.get_actual_base_for_wp(current_wp_id)
    diff_command = f"git diff {diff_base}..HEAD"

    # Build entries list
    entries_json = []
    for entry in topology.entries:
        entry_data: dict = {
            "wp": entry.wp_id,
            "lane": entry.lane,
            "XXbranchXX": entry.branch_name,
            "base": entry.base_wp if entry.base_wp else topology.target_branch,
        }
        if entry.worktree_exists:
            entry_data["commits_ahead"] = entry.commits_ahead_of_base
        if entry.dependencies and not entry.worktree_exists:
            entry_data["dependencies"] = entry.dependencies
        entries_json.append(entry_data)

    payload = {
        "feature": topology.feature_slug,
        "target_branch": topology.target_branch,
        "current_wp": current_wp_id,
        "your_base": your_base,
        "diff_command": diff_command,
        "stacked": True,
        "note": f"Your branch stacks on {current_entry.base_wp}, NOT {topology.target_branch}. Do not worry about being 'behind {topology.target_branch}'."
            if current_entry and current_entry.base_wp
            else f"Your branch is based on {topology.target_branch}. Other WPs in this feature use stacking.",
        "entries": entries_json,
    }

    lines = [
        "<!-- WORKTREE_TOPOLOGY -->",
        json.dumps(payload, indent=2),
        "<!-- /WORKTREE_TOPOLOGY -->",
    ]
    return lines


def x_render_topology_json__mutmut_20(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as structured JSON for prompt injection.

    Only call this when topology.has_stacking is True.
    Output is wrapped in HTML comment markers for reliable agent parsing.

    Args:
        topology: Feature topology data
        current_wp_id: The WP being implemented/reviewed

    Returns:
        List of lines to append to prompt
    """
    current_entry = topology.get_entry(current_wp_id)

    # Build base info for current WP
    your_base = None
    if current_entry and current_entry.base_wp:
        your_base = {
            "branch": current_entry.base_branch,
            "wp": current_entry.base_wp,
        }

    # Build diff command
    diff_base = topology.get_actual_base_for_wp(current_wp_id)
    diff_command = f"git diff {diff_base}..HEAD"

    # Build entries list
    entries_json = []
    for entry in topology.entries:
        entry_data: dict = {
            "wp": entry.wp_id,
            "lane": entry.lane,
            "BRANCH": entry.branch_name,
            "base": entry.base_wp if entry.base_wp else topology.target_branch,
        }
        if entry.worktree_exists:
            entry_data["commits_ahead"] = entry.commits_ahead_of_base
        if entry.dependencies and not entry.worktree_exists:
            entry_data["dependencies"] = entry.dependencies
        entries_json.append(entry_data)

    payload = {
        "feature": topology.feature_slug,
        "target_branch": topology.target_branch,
        "current_wp": current_wp_id,
        "your_base": your_base,
        "diff_command": diff_command,
        "stacked": True,
        "note": f"Your branch stacks on {current_entry.base_wp}, NOT {topology.target_branch}. Do not worry about being 'behind {topology.target_branch}'."
            if current_entry and current_entry.base_wp
            else f"Your branch is based on {topology.target_branch}. Other WPs in this feature use stacking.",
        "entries": entries_json,
    }

    lines = [
        "<!-- WORKTREE_TOPOLOGY -->",
        json.dumps(payload, indent=2),
        "<!-- /WORKTREE_TOPOLOGY -->",
    ]
    return lines


def x_render_topology_json__mutmut_21(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as structured JSON for prompt injection.

    Only call this when topology.has_stacking is True.
    Output is wrapped in HTML comment markers for reliable agent parsing.

    Args:
        topology: Feature topology data
        current_wp_id: The WP being implemented/reviewed

    Returns:
        List of lines to append to prompt
    """
    current_entry = topology.get_entry(current_wp_id)

    # Build base info for current WP
    your_base = None
    if current_entry and current_entry.base_wp:
        your_base = {
            "branch": current_entry.base_branch,
            "wp": current_entry.base_wp,
        }

    # Build diff command
    diff_base = topology.get_actual_base_for_wp(current_wp_id)
    diff_command = f"git diff {diff_base}..HEAD"

    # Build entries list
    entries_json = []
    for entry in topology.entries:
        entry_data: dict = {
            "wp": entry.wp_id,
            "lane": entry.lane,
            "branch": entry.branch_name,
            "XXbaseXX": entry.base_wp if entry.base_wp else topology.target_branch,
        }
        if entry.worktree_exists:
            entry_data["commits_ahead"] = entry.commits_ahead_of_base
        if entry.dependencies and not entry.worktree_exists:
            entry_data["dependencies"] = entry.dependencies
        entries_json.append(entry_data)

    payload = {
        "feature": topology.feature_slug,
        "target_branch": topology.target_branch,
        "current_wp": current_wp_id,
        "your_base": your_base,
        "diff_command": diff_command,
        "stacked": True,
        "note": f"Your branch stacks on {current_entry.base_wp}, NOT {topology.target_branch}. Do not worry about being 'behind {topology.target_branch}'."
            if current_entry and current_entry.base_wp
            else f"Your branch is based on {topology.target_branch}. Other WPs in this feature use stacking.",
        "entries": entries_json,
    }

    lines = [
        "<!-- WORKTREE_TOPOLOGY -->",
        json.dumps(payload, indent=2),
        "<!-- /WORKTREE_TOPOLOGY -->",
    ]
    return lines


def x_render_topology_json__mutmut_22(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as structured JSON for prompt injection.

    Only call this when topology.has_stacking is True.
    Output is wrapped in HTML comment markers for reliable agent parsing.

    Args:
        topology: Feature topology data
        current_wp_id: The WP being implemented/reviewed

    Returns:
        List of lines to append to prompt
    """
    current_entry = topology.get_entry(current_wp_id)

    # Build base info for current WP
    your_base = None
    if current_entry and current_entry.base_wp:
        your_base = {
            "branch": current_entry.base_branch,
            "wp": current_entry.base_wp,
        }

    # Build diff command
    diff_base = topology.get_actual_base_for_wp(current_wp_id)
    diff_command = f"git diff {diff_base}..HEAD"

    # Build entries list
    entries_json = []
    for entry in topology.entries:
        entry_data: dict = {
            "wp": entry.wp_id,
            "lane": entry.lane,
            "branch": entry.branch_name,
            "BASE": entry.base_wp if entry.base_wp else topology.target_branch,
        }
        if entry.worktree_exists:
            entry_data["commits_ahead"] = entry.commits_ahead_of_base
        if entry.dependencies and not entry.worktree_exists:
            entry_data["dependencies"] = entry.dependencies
        entries_json.append(entry_data)

    payload = {
        "feature": topology.feature_slug,
        "target_branch": topology.target_branch,
        "current_wp": current_wp_id,
        "your_base": your_base,
        "diff_command": diff_command,
        "stacked": True,
        "note": f"Your branch stacks on {current_entry.base_wp}, NOT {topology.target_branch}. Do not worry about being 'behind {topology.target_branch}'."
            if current_entry and current_entry.base_wp
            else f"Your branch is based on {topology.target_branch}. Other WPs in this feature use stacking.",
        "entries": entries_json,
    }

    lines = [
        "<!-- WORKTREE_TOPOLOGY -->",
        json.dumps(payload, indent=2),
        "<!-- /WORKTREE_TOPOLOGY -->",
    ]
    return lines


def x_render_topology_json__mutmut_23(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as structured JSON for prompt injection.

    Only call this when topology.has_stacking is True.
    Output is wrapped in HTML comment markers for reliable agent parsing.

    Args:
        topology: Feature topology data
        current_wp_id: The WP being implemented/reviewed

    Returns:
        List of lines to append to prompt
    """
    current_entry = topology.get_entry(current_wp_id)

    # Build base info for current WP
    your_base = None
    if current_entry and current_entry.base_wp:
        your_base = {
            "branch": current_entry.base_branch,
            "wp": current_entry.base_wp,
        }

    # Build diff command
    diff_base = topology.get_actual_base_for_wp(current_wp_id)
    diff_command = f"git diff {diff_base}..HEAD"

    # Build entries list
    entries_json = []
    for entry in topology.entries:
        entry_data: dict = {
            "wp": entry.wp_id,
            "lane": entry.lane,
            "branch": entry.branch_name,
            "base": entry.base_wp if entry.base_wp else topology.target_branch,
        }
        if entry.worktree_exists:
            entry_data["commits_ahead"] = None
        if entry.dependencies and not entry.worktree_exists:
            entry_data["dependencies"] = entry.dependencies
        entries_json.append(entry_data)

    payload = {
        "feature": topology.feature_slug,
        "target_branch": topology.target_branch,
        "current_wp": current_wp_id,
        "your_base": your_base,
        "diff_command": diff_command,
        "stacked": True,
        "note": f"Your branch stacks on {current_entry.base_wp}, NOT {topology.target_branch}. Do not worry about being 'behind {topology.target_branch}'."
            if current_entry and current_entry.base_wp
            else f"Your branch is based on {topology.target_branch}. Other WPs in this feature use stacking.",
        "entries": entries_json,
    }

    lines = [
        "<!-- WORKTREE_TOPOLOGY -->",
        json.dumps(payload, indent=2),
        "<!-- /WORKTREE_TOPOLOGY -->",
    ]
    return lines


def x_render_topology_json__mutmut_24(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as structured JSON for prompt injection.

    Only call this when topology.has_stacking is True.
    Output is wrapped in HTML comment markers for reliable agent parsing.

    Args:
        topology: Feature topology data
        current_wp_id: The WP being implemented/reviewed

    Returns:
        List of lines to append to prompt
    """
    current_entry = topology.get_entry(current_wp_id)

    # Build base info for current WP
    your_base = None
    if current_entry and current_entry.base_wp:
        your_base = {
            "branch": current_entry.base_branch,
            "wp": current_entry.base_wp,
        }

    # Build diff command
    diff_base = topology.get_actual_base_for_wp(current_wp_id)
    diff_command = f"git diff {diff_base}..HEAD"

    # Build entries list
    entries_json = []
    for entry in topology.entries:
        entry_data: dict = {
            "wp": entry.wp_id,
            "lane": entry.lane,
            "branch": entry.branch_name,
            "base": entry.base_wp if entry.base_wp else topology.target_branch,
        }
        if entry.worktree_exists:
            entry_data["XXcommits_aheadXX"] = entry.commits_ahead_of_base
        if entry.dependencies and not entry.worktree_exists:
            entry_data["dependencies"] = entry.dependencies
        entries_json.append(entry_data)

    payload = {
        "feature": topology.feature_slug,
        "target_branch": topology.target_branch,
        "current_wp": current_wp_id,
        "your_base": your_base,
        "diff_command": diff_command,
        "stacked": True,
        "note": f"Your branch stacks on {current_entry.base_wp}, NOT {topology.target_branch}. Do not worry about being 'behind {topology.target_branch}'."
            if current_entry and current_entry.base_wp
            else f"Your branch is based on {topology.target_branch}. Other WPs in this feature use stacking.",
        "entries": entries_json,
    }

    lines = [
        "<!-- WORKTREE_TOPOLOGY -->",
        json.dumps(payload, indent=2),
        "<!-- /WORKTREE_TOPOLOGY -->",
    ]
    return lines


def x_render_topology_json__mutmut_25(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as structured JSON for prompt injection.

    Only call this when topology.has_stacking is True.
    Output is wrapped in HTML comment markers for reliable agent parsing.

    Args:
        topology: Feature topology data
        current_wp_id: The WP being implemented/reviewed

    Returns:
        List of lines to append to prompt
    """
    current_entry = topology.get_entry(current_wp_id)

    # Build base info for current WP
    your_base = None
    if current_entry and current_entry.base_wp:
        your_base = {
            "branch": current_entry.base_branch,
            "wp": current_entry.base_wp,
        }

    # Build diff command
    diff_base = topology.get_actual_base_for_wp(current_wp_id)
    diff_command = f"git diff {diff_base}..HEAD"

    # Build entries list
    entries_json = []
    for entry in topology.entries:
        entry_data: dict = {
            "wp": entry.wp_id,
            "lane": entry.lane,
            "branch": entry.branch_name,
            "base": entry.base_wp if entry.base_wp else topology.target_branch,
        }
        if entry.worktree_exists:
            entry_data["COMMITS_AHEAD"] = entry.commits_ahead_of_base
        if entry.dependencies and not entry.worktree_exists:
            entry_data["dependencies"] = entry.dependencies
        entries_json.append(entry_data)

    payload = {
        "feature": topology.feature_slug,
        "target_branch": topology.target_branch,
        "current_wp": current_wp_id,
        "your_base": your_base,
        "diff_command": diff_command,
        "stacked": True,
        "note": f"Your branch stacks on {current_entry.base_wp}, NOT {topology.target_branch}. Do not worry about being 'behind {topology.target_branch}'."
            if current_entry and current_entry.base_wp
            else f"Your branch is based on {topology.target_branch}. Other WPs in this feature use stacking.",
        "entries": entries_json,
    }

    lines = [
        "<!-- WORKTREE_TOPOLOGY -->",
        json.dumps(payload, indent=2),
        "<!-- /WORKTREE_TOPOLOGY -->",
    ]
    return lines


def x_render_topology_json__mutmut_26(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as structured JSON for prompt injection.

    Only call this when topology.has_stacking is True.
    Output is wrapped in HTML comment markers for reliable agent parsing.

    Args:
        topology: Feature topology data
        current_wp_id: The WP being implemented/reviewed

    Returns:
        List of lines to append to prompt
    """
    current_entry = topology.get_entry(current_wp_id)

    # Build base info for current WP
    your_base = None
    if current_entry and current_entry.base_wp:
        your_base = {
            "branch": current_entry.base_branch,
            "wp": current_entry.base_wp,
        }

    # Build diff command
    diff_base = topology.get_actual_base_for_wp(current_wp_id)
    diff_command = f"git diff {diff_base}..HEAD"

    # Build entries list
    entries_json = []
    for entry in topology.entries:
        entry_data: dict = {
            "wp": entry.wp_id,
            "lane": entry.lane,
            "branch": entry.branch_name,
            "base": entry.base_wp if entry.base_wp else topology.target_branch,
        }
        if entry.worktree_exists:
            entry_data["commits_ahead"] = entry.commits_ahead_of_base
        if entry.dependencies or not entry.worktree_exists:
            entry_data["dependencies"] = entry.dependencies
        entries_json.append(entry_data)

    payload = {
        "feature": topology.feature_slug,
        "target_branch": topology.target_branch,
        "current_wp": current_wp_id,
        "your_base": your_base,
        "diff_command": diff_command,
        "stacked": True,
        "note": f"Your branch stacks on {current_entry.base_wp}, NOT {topology.target_branch}. Do not worry about being 'behind {topology.target_branch}'."
            if current_entry and current_entry.base_wp
            else f"Your branch is based on {topology.target_branch}. Other WPs in this feature use stacking.",
        "entries": entries_json,
    }

    lines = [
        "<!-- WORKTREE_TOPOLOGY -->",
        json.dumps(payload, indent=2),
        "<!-- /WORKTREE_TOPOLOGY -->",
    ]
    return lines


def x_render_topology_json__mutmut_27(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as structured JSON for prompt injection.

    Only call this when topology.has_stacking is True.
    Output is wrapped in HTML comment markers for reliable agent parsing.

    Args:
        topology: Feature topology data
        current_wp_id: The WP being implemented/reviewed

    Returns:
        List of lines to append to prompt
    """
    current_entry = topology.get_entry(current_wp_id)

    # Build base info for current WP
    your_base = None
    if current_entry and current_entry.base_wp:
        your_base = {
            "branch": current_entry.base_branch,
            "wp": current_entry.base_wp,
        }

    # Build diff command
    diff_base = topology.get_actual_base_for_wp(current_wp_id)
    diff_command = f"git diff {diff_base}..HEAD"

    # Build entries list
    entries_json = []
    for entry in topology.entries:
        entry_data: dict = {
            "wp": entry.wp_id,
            "lane": entry.lane,
            "branch": entry.branch_name,
            "base": entry.base_wp if entry.base_wp else topology.target_branch,
        }
        if entry.worktree_exists:
            entry_data["commits_ahead"] = entry.commits_ahead_of_base
        if entry.dependencies and entry.worktree_exists:
            entry_data["dependencies"] = entry.dependencies
        entries_json.append(entry_data)

    payload = {
        "feature": topology.feature_slug,
        "target_branch": topology.target_branch,
        "current_wp": current_wp_id,
        "your_base": your_base,
        "diff_command": diff_command,
        "stacked": True,
        "note": f"Your branch stacks on {current_entry.base_wp}, NOT {topology.target_branch}. Do not worry about being 'behind {topology.target_branch}'."
            if current_entry and current_entry.base_wp
            else f"Your branch is based on {topology.target_branch}. Other WPs in this feature use stacking.",
        "entries": entries_json,
    }

    lines = [
        "<!-- WORKTREE_TOPOLOGY -->",
        json.dumps(payload, indent=2),
        "<!-- /WORKTREE_TOPOLOGY -->",
    ]
    return lines


def x_render_topology_json__mutmut_28(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as structured JSON for prompt injection.

    Only call this when topology.has_stacking is True.
    Output is wrapped in HTML comment markers for reliable agent parsing.

    Args:
        topology: Feature topology data
        current_wp_id: The WP being implemented/reviewed

    Returns:
        List of lines to append to prompt
    """
    current_entry = topology.get_entry(current_wp_id)

    # Build base info for current WP
    your_base = None
    if current_entry and current_entry.base_wp:
        your_base = {
            "branch": current_entry.base_branch,
            "wp": current_entry.base_wp,
        }

    # Build diff command
    diff_base = topology.get_actual_base_for_wp(current_wp_id)
    diff_command = f"git diff {diff_base}..HEAD"

    # Build entries list
    entries_json = []
    for entry in topology.entries:
        entry_data: dict = {
            "wp": entry.wp_id,
            "lane": entry.lane,
            "branch": entry.branch_name,
            "base": entry.base_wp if entry.base_wp else topology.target_branch,
        }
        if entry.worktree_exists:
            entry_data["commits_ahead"] = entry.commits_ahead_of_base
        if entry.dependencies and not entry.worktree_exists:
            entry_data["dependencies"] = None
        entries_json.append(entry_data)

    payload = {
        "feature": topology.feature_slug,
        "target_branch": topology.target_branch,
        "current_wp": current_wp_id,
        "your_base": your_base,
        "diff_command": diff_command,
        "stacked": True,
        "note": f"Your branch stacks on {current_entry.base_wp}, NOT {topology.target_branch}. Do not worry about being 'behind {topology.target_branch}'."
            if current_entry and current_entry.base_wp
            else f"Your branch is based on {topology.target_branch}. Other WPs in this feature use stacking.",
        "entries": entries_json,
    }

    lines = [
        "<!-- WORKTREE_TOPOLOGY -->",
        json.dumps(payload, indent=2),
        "<!-- /WORKTREE_TOPOLOGY -->",
    ]
    return lines


def x_render_topology_json__mutmut_29(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as structured JSON for prompt injection.

    Only call this when topology.has_stacking is True.
    Output is wrapped in HTML comment markers for reliable agent parsing.

    Args:
        topology: Feature topology data
        current_wp_id: The WP being implemented/reviewed

    Returns:
        List of lines to append to prompt
    """
    current_entry = topology.get_entry(current_wp_id)

    # Build base info for current WP
    your_base = None
    if current_entry and current_entry.base_wp:
        your_base = {
            "branch": current_entry.base_branch,
            "wp": current_entry.base_wp,
        }

    # Build diff command
    diff_base = topology.get_actual_base_for_wp(current_wp_id)
    diff_command = f"git diff {diff_base}..HEAD"

    # Build entries list
    entries_json = []
    for entry in topology.entries:
        entry_data: dict = {
            "wp": entry.wp_id,
            "lane": entry.lane,
            "branch": entry.branch_name,
            "base": entry.base_wp if entry.base_wp else topology.target_branch,
        }
        if entry.worktree_exists:
            entry_data["commits_ahead"] = entry.commits_ahead_of_base
        if entry.dependencies and not entry.worktree_exists:
            entry_data["XXdependenciesXX"] = entry.dependencies
        entries_json.append(entry_data)

    payload = {
        "feature": topology.feature_slug,
        "target_branch": topology.target_branch,
        "current_wp": current_wp_id,
        "your_base": your_base,
        "diff_command": diff_command,
        "stacked": True,
        "note": f"Your branch stacks on {current_entry.base_wp}, NOT {topology.target_branch}. Do not worry about being 'behind {topology.target_branch}'."
            if current_entry and current_entry.base_wp
            else f"Your branch is based on {topology.target_branch}. Other WPs in this feature use stacking.",
        "entries": entries_json,
    }

    lines = [
        "<!-- WORKTREE_TOPOLOGY -->",
        json.dumps(payload, indent=2),
        "<!-- /WORKTREE_TOPOLOGY -->",
    ]
    return lines


def x_render_topology_json__mutmut_30(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as structured JSON for prompt injection.

    Only call this when topology.has_stacking is True.
    Output is wrapped in HTML comment markers for reliable agent parsing.

    Args:
        topology: Feature topology data
        current_wp_id: The WP being implemented/reviewed

    Returns:
        List of lines to append to prompt
    """
    current_entry = topology.get_entry(current_wp_id)

    # Build base info for current WP
    your_base = None
    if current_entry and current_entry.base_wp:
        your_base = {
            "branch": current_entry.base_branch,
            "wp": current_entry.base_wp,
        }

    # Build diff command
    diff_base = topology.get_actual_base_for_wp(current_wp_id)
    diff_command = f"git diff {diff_base}..HEAD"

    # Build entries list
    entries_json = []
    for entry in topology.entries:
        entry_data: dict = {
            "wp": entry.wp_id,
            "lane": entry.lane,
            "branch": entry.branch_name,
            "base": entry.base_wp if entry.base_wp else topology.target_branch,
        }
        if entry.worktree_exists:
            entry_data["commits_ahead"] = entry.commits_ahead_of_base
        if entry.dependencies and not entry.worktree_exists:
            entry_data["DEPENDENCIES"] = entry.dependencies
        entries_json.append(entry_data)

    payload = {
        "feature": topology.feature_slug,
        "target_branch": topology.target_branch,
        "current_wp": current_wp_id,
        "your_base": your_base,
        "diff_command": diff_command,
        "stacked": True,
        "note": f"Your branch stacks on {current_entry.base_wp}, NOT {topology.target_branch}. Do not worry about being 'behind {topology.target_branch}'."
            if current_entry and current_entry.base_wp
            else f"Your branch is based on {topology.target_branch}. Other WPs in this feature use stacking.",
        "entries": entries_json,
    }

    lines = [
        "<!-- WORKTREE_TOPOLOGY -->",
        json.dumps(payload, indent=2),
        "<!-- /WORKTREE_TOPOLOGY -->",
    ]
    return lines


def x_render_topology_json__mutmut_31(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as structured JSON for prompt injection.

    Only call this when topology.has_stacking is True.
    Output is wrapped in HTML comment markers for reliable agent parsing.

    Args:
        topology: Feature topology data
        current_wp_id: The WP being implemented/reviewed

    Returns:
        List of lines to append to prompt
    """
    current_entry = topology.get_entry(current_wp_id)

    # Build base info for current WP
    your_base = None
    if current_entry and current_entry.base_wp:
        your_base = {
            "branch": current_entry.base_branch,
            "wp": current_entry.base_wp,
        }

    # Build diff command
    diff_base = topology.get_actual_base_for_wp(current_wp_id)
    diff_command = f"git diff {diff_base}..HEAD"

    # Build entries list
    entries_json = []
    for entry in topology.entries:
        entry_data: dict = {
            "wp": entry.wp_id,
            "lane": entry.lane,
            "branch": entry.branch_name,
            "base": entry.base_wp if entry.base_wp else topology.target_branch,
        }
        if entry.worktree_exists:
            entry_data["commits_ahead"] = entry.commits_ahead_of_base
        if entry.dependencies and not entry.worktree_exists:
            entry_data["dependencies"] = entry.dependencies
        entries_json.append(None)

    payload = {
        "feature": topology.feature_slug,
        "target_branch": topology.target_branch,
        "current_wp": current_wp_id,
        "your_base": your_base,
        "diff_command": diff_command,
        "stacked": True,
        "note": f"Your branch stacks on {current_entry.base_wp}, NOT {topology.target_branch}. Do not worry about being 'behind {topology.target_branch}'."
            if current_entry and current_entry.base_wp
            else f"Your branch is based on {topology.target_branch}. Other WPs in this feature use stacking.",
        "entries": entries_json,
    }

    lines = [
        "<!-- WORKTREE_TOPOLOGY -->",
        json.dumps(payload, indent=2),
        "<!-- /WORKTREE_TOPOLOGY -->",
    ]
    return lines


def x_render_topology_json__mutmut_32(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as structured JSON for prompt injection.

    Only call this when topology.has_stacking is True.
    Output is wrapped in HTML comment markers for reliable agent parsing.

    Args:
        topology: Feature topology data
        current_wp_id: The WP being implemented/reviewed

    Returns:
        List of lines to append to prompt
    """
    current_entry = topology.get_entry(current_wp_id)

    # Build base info for current WP
    your_base = None
    if current_entry and current_entry.base_wp:
        your_base = {
            "branch": current_entry.base_branch,
            "wp": current_entry.base_wp,
        }

    # Build diff command
    diff_base = topology.get_actual_base_for_wp(current_wp_id)
    diff_command = f"git diff {diff_base}..HEAD"

    # Build entries list
    entries_json = []
    for entry in topology.entries:
        entry_data: dict = {
            "wp": entry.wp_id,
            "lane": entry.lane,
            "branch": entry.branch_name,
            "base": entry.base_wp if entry.base_wp else topology.target_branch,
        }
        if entry.worktree_exists:
            entry_data["commits_ahead"] = entry.commits_ahead_of_base
        if entry.dependencies and not entry.worktree_exists:
            entry_data["dependencies"] = entry.dependencies
        entries_json.append(entry_data)

    payload = None

    lines = [
        "<!-- WORKTREE_TOPOLOGY -->",
        json.dumps(payload, indent=2),
        "<!-- /WORKTREE_TOPOLOGY -->",
    ]
    return lines


def x_render_topology_json__mutmut_33(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as structured JSON for prompt injection.

    Only call this when topology.has_stacking is True.
    Output is wrapped in HTML comment markers for reliable agent parsing.

    Args:
        topology: Feature topology data
        current_wp_id: The WP being implemented/reviewed

    Returns:
        List of lines to append to prompt
    """
    current_entry = topology.get_entry(current_wp_id)

    # Build base info for current WP
    your_base = None
    if current_entry and current_entry.base_wp:
        your_base = {
            "branch": current_entry.base_branch,
            "wp": current_entry.base_wp,
        }

    # Build diff command
    diff_base = topology.get_actual_base_for_wp(current_wp_id)
    diff_command = f"git diff {diff_base}..HEAD"

    # Build entries list
    entries_json = []
    for entry in topology.entries:
        entry_data: dict = {
            "wp": entry.wp_id,
            "lane": entry.lane,
            "branch": entry.branch_name,
            "base": entry.base_wp if entry.base_wp else topology.target_branch,
        }
        if entry.worktree_exists:
            entry_data["commits_ahead"] = entry.commits_ahead_of_base
        if entry.dependencies and not entry.worktree_exists:
            entry_data["dependencies"] = entry.dependencies
        entries_json.append(entry_data)

    payload = {
        "XXfeatureXX": topology.feature_slug,
        "target_branch": topology.target_branch,
        "current_wp": current_wp_id,
        "your_base": your_base,
        "diff_command": diff_command,
        "stacked": True,
        "note": f"Your branch stacks on {current_entry.base_wp}, NOT {topology.target_branch}. Do not worry about being 'behind {topology.target_branch}'."
            if current_entry and current_entry.base_wp
            else f"Your branch is based on {topology.target_branch}. Other WPs in this feature use stacking.",
        "entries": entries_json,
    }

    lines = [
        "<!-- WORKTREE_TOPOLOGY -->",
        json.dumps(payload, indent=2),
        "<!-- /WORKTREE_TOPOLOGY -->",
    ]
    return lines


def x_render_topology_json__mutmut_34(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as structured JSON for prompt injection.

    Only call this when topology.has_stacking is True.
    Output is wrapped in HTML comment markers for reliable agent parsing.

    Args:
        topology: Feature topology data
        current_wp_id: The WP being implemented/reviewed

    Returns:
        List of lines to append to prompt
    """
    current_entry = topology.get_entry(current_wp_id)

    # Build base info for current WP
    your_base = None
    if current_entry and current_entry.base_wp:
        your_base = {
            "branch": current_entry.base_branch,
            "wp": current_entry.base_wp,
        }

    # Build diff command
    diff_base = topology.get_actual_base_for_wp(current_wp_id)
    diff_command = f"git diff {diff_base}..HEAD"

    # Build entries list
    entries_json = []
    for entry in topology.entries:
        entry_data: dict = {
            "wp": entry.wp_id,
            "lane": entry.lane,
            "branch": entry.branch_name,
            "base": entry.base_wp if entry.base_wp else topology.target_branch,
        }
        if entry.worktree_exists:
            entry_data["commits_ahead"] = entry.commits_ahead_of_base
        if entry.dependencies and not entry.worktree_exists:
            entry_data["dependencies"] = entry.dependencies
        entries_json.append(entry_data)

    payload = {
        "FEATURE": topology.feature_slug,
        "target_branch": topology.target_branch,
        "current_wp": current_wp_id,
        "your_base": your_base,
        "diff_command": diff_command,
        "stacked": True,
        "note": f"Your branch stacks on {current_entry.base_wp}, NOT {topology.target_branch}. Do not worry about being 'behind {topology.target_branch}'."
            if current_entry and current_entry.base_wp
            else f"Your branch is based on {topology.target_branch}. Other WPs in this feature use stacking.",
        "entries": entries_json,
    }

    lines = [
        "<!-- WORKTREE_TOPOLOGY -->",
        json.dumps(payload, indent=2),
        "<!-- /WORKTREE_TOPOLOGY -->",
    ]
    return lines


def x_render_topology_json__mutmut_35(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as structured JSON for prompt injection.

    Only call this when topology.has_stacking is True.
    Output is wrapped in HTML comment markers for reliable agent parsing.

    Args:
        topology: Feature topology data
        current_wp_id: The WP being implemented/reviewed

    Returns:
        List of lines to append to prompt
    """
    current_entry = topology.get_entry(current_wp_id)

    # Build base info for current WP
    your_base = None
    if current_entry and current_entry.base_wp:
        your_base = {
            "branch": current_entry.base_branch,
            "wp": current_entry.base_wp,
        }

    # Build diff command
    diff_base = topology.get_actual_base_for_wp(current_wp_id)
    diff_command = f"git diff {diff_base}..HEAD"

    # Build entries list
    entries_json = []
    for entry in topology.entries:
        entry_data: dict = {
            "wp": entry.wp_id,
            "lane": entry.lane,
            "branch": entry.branch_name,
            "base": entry.base_wp if entry.base_wp else topology.target_branch,
        }
        if entry.worktree_exists:
            entry_data["commits_ahead"] = entry.commits_ahead_of_base
        if entry.dependencies and not entry.worktree_exists:
            entry_data["dependencies"] = entry.dependencies
        entries_json.append(entry_data)

    payload = {
        "feature": topology.feature_slug,
        "XXtarget_branchXX": topology.target_branch,
        "current_wp": current_wp_id,
        "your_base": your_base,
        "diff_command": diff_command,
        "stacked": True,
        "note": f"Your branch stacks on {current_entry.base_wp}, NOT {topology.target_branch}. Do not worry about being 'behind {topology.target_branch}'."
            if current_entry and current_entry.base_wp
            else f"Your branch is based on {topology.target_branch}. Other WPs in this feature use stacking.",
        "entries": entries_json,
    }

    lines = [
        "<!-- WORKTREE_TOPOLOGY -->",
        json.dumps(payload, indent=2),
        "<!-- /WORKTREE_TOPOLOGY -->",
    ]
    return lines


def x_render_topology_json__mutmut_36(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as structured JSON for prompt injection.

    Only call this when topology.has_stacking is True.
    Output is wrapped in HTML comment markers for reliable agent parsing.

    Args:
        topology: Feature topology data
        current_wp_id: The WP being implemented/reviewed

    Returns:
        List of lines to append to prompt
    """
    current_entry = topology.get_entry(current_wp_id)

    # Build base info for current WP
    your_base = None
    if current_entry and current_entry.base_wp:
        your_base = {
            "branch": current_entry.base_branch,
            "wp": current_entry.base_wp,
        }

    # Build diff command
    diff_base = topology.get_actual_base_for_wp(current_wp_id)
    diff_command = f"git diff {diff_base}..HEAD"

    # Build entries list
    entries_json = []
    for entry in topology.entries:
        entry_data: dict = {
            "wp": entry.wp_id,
            "lane": entry.lane,
            "branch": entry.branch_name,
            "base": entry.base_wp if entry.base_wp else topology.target_branch,
        }
        if entry.worktree_exists:
            entry_data["commits_ahead"] = entry.commits_ahead_of_base
        if entry.dependencies and not entry.worktree_exists:
            entry_data["dependencies"] = entry.dependencies
        entries_json.append(entry_data)

    payload = {
        "feature": topology.feature_slug,
        "TARGET_BRANCH": topology.target_branch,
        "current_wp": current_wp_id,
        "your_base": your_base,
        "diff_command": diff_command,
        "stacked": True,
        "note": f"Your branch stacks on {current_entry.base_wp}, NOT {topology.target_branch}. Do not worry about being 'behind {topology.target_branch}'."
            if current_entry and current_entry.base_wp
            else f"Your branch is based on {topology.target_branch}. Other WPs in this feature use stacking.",
        "entries": entries_json,
    }

    lines = [
        "<!-- WORKTREE_TOPOLOGY -->",
        json.dumps(payload, indent=2),
        "<!-- /WORKTREE_TOPOLOGY -->",
    ]
    return lines


def x_render_topology_json__mutmut_37(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as structured JSON for prompt injection.

    Only call this when topology.has_stacking is True.
    Output is wrapped in HTML comment markers for reliable agent parsing.

    Args:
        topology: Feature topology data
        current_wp_id: The WP being implemented/reviewed

    Returns:
        List of lines to append to prompt
    """
    current_entry = topology.get_entry(current_wp_id)

    # Build base info for current WP
    your_base = None
    if current_entry and current_entry.base_wp:
        your_base = {
            "branch": current_entry.base_branch,
            "wp": current_entry.base_wp,
        }

    # Build diff command
    diff_base = topology.get_actual_base_for_wp(current_wp_id)
    diff_command = f"git diff {diff_base}..HEAD"

    # Build entries list
    entries_json = []
    for entry in topology.entries:
        entry_data: dict = {
            "wp": entry.wp_id,
            "lane": entry.lane,
            "branch": entry.branch_name,
            "base": entry.base_wp if entry.base_wp else topology.target_branch,
        }
        if entry.worktree_exists:
            entry_data["commits_ahead"] = entry.commits_ahead_of_base
        if entry.dependencies and not entry.worktree_exists:
            entry_data["dependencies"] = entry.dependencies
        entries_json.append(entry_data)

    payload = {
        "feature": topology.feature_slug,
        "target_branch": topology.target_branch,
        "XXcurrent_wpXX": current_wp_id,
        "your_base": your_base,
        "diff_command": diff_command,
        "stacked": True,
        "note": f"Your branch stacks on {current_entry.base_wp}, NOT {topology.target_branch}. Do not worry about being 'behind {topology.target_branch}'."
            if current_entry and current_entry.base_wp
            else f"Your branch is based on {topology.target_branch}. Other WPs in this feature use stacking.",
        "entries": entries_json,
    }

    lines = [
        "<!-- WORKTREE_TOPOLOGY -->",
        json.dumps(payload, indent=2),
        "<!-- /WORKTREE_TOPOLOGY -->",
    ]
    return lines


def x_render_topology_json__mutmut_38(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as structured JSON for prompt injection.

    Only call this when topology.has_stacking is True.
    Output is wrapped in HTML comment markers for reliable agent parsing.

    Args:
        topology: Feature topology data
        current_wp_id: The WP being implemented/reviewed

    Returns:
        List of lines to append to prompt
    """
    current_entry = topology.get_entry(current_wp_id)

    # Build base info for current WP
    your_base = None
    if current_entry and current_entry.base_wp:
        your_base = {
            "branch": current_entry.base_branch,
            "wp": current_entry.base_wp,
        }

    # Build diff command
    diff_base = topology.get_actual_base_for_wp(current_wp_id)
    diff_command = f"git diff {diff_base}..HEAD"

    # Build entries list
    entries_json = []
    for entry in topology.entries:
        entry_data: dict = {
            "wp": entry.wp_id,
            "lane": entry.lane,
            "branch": entry.branch_name,
            "base": entry.base_wp if entry.base_wp else topology.target_branch,
        }
        if entry.worktree_exists:
            entry_data["commits_ahead"] = entry.commits_ahead_of_base
        if entry.dependencies and not entry.worktree_exists:
            entry_data["dependencies"] = entry.dependencies
        entries_json.append(entry_data)

    payload = {
        "feature": topology.feature_slug,
        "target_branch": topology.target_branch,
        "CURRENT_WP": current_wp_id,
        "your_base": your_base,
        "diff_command": diff_command,
        "stacked": True,
        "note": f"Your branch stacks on {current_entry.base_wp}, NOT {topology.target_branch}. Do not worry about being 'behind {topology.target_branch}'."
            if current_entry and current_entry.base_wp
            else f"Your branch is based on {topology.target_branch}. Other WPs in this feature use stacking.",
        "entries": entries_json,
    }

    lines = [
        "<!-- WORKTREE_TOPOLOGY -->",
        json.dumps(payload, indent=2),
        "<!-- /WORKTREE_TOPOLOGY -->",
    ]
    return lines


def x_render_topology_json__mutmut_39(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as structured JSON for prompt injection.

    Only call this when topology.has_stacking is True.
    Output is wrapped in HTML comment markers for reliable agent parsing.

    Args:
        topology: Feature topology data
        current_wp_id: The WP being implemented/reviewed

    Returns:
        List of lines to append to prompt
    """
    current_entry = topology.get_entry(current_wp_id)

    # Build base info for current WP
    your_base = None
    if current_entry and current_entry.base_wp:
        your_base = {
            "branch": current_entry.base_branch,
            "wp": current_entry.base_wp,
        }

    # Build diff command
    diff_base = topology.get_actual_base_for_wp(current_wp_id)
    diff_command = f"git diff {diff_base}..HEAD"

    # Build entries list
    entries_json = []
    for entry in topology.entries:
        entry_data: dict = {
            "wp": entry.wp_id,
            "lane": entry.lane,
            "branch": entry.branch_name,
            "base": entry.base_wp if entry.base_wp else topology.target_branch,
        }
        if entry.worktree_exists:
            entry_data["commits_ahead"] = entry.commits_ahead_of_base
        if entry.dependencies and not entry.worktree_exists:
            entry_data["dependencies"] = entry.dependencies
        entries_json.append(entry_data)

    payload = {
        "feature": topology.feature_slug,
        "target_branch": topology.target_branch,
        "current_wp": current_wp_id,
        "XXyour_baseXX": your_base,
        "diff_command": diff_command,
        "stacked": True,
        "note": f"Your branch stacks on {current_entry.base_wp}, NOT {topology.target_branch}. Do not worry about being 'behind {topology.target_branch}'."
            if current_entry and current_entry.base_wp
            else f"Your branch is based on {topology.target_branch}. Other WPs in this feature use stacking.",
        "entries": entries_json,
    }

    lines = [
        "<!-- WORKTREE_TOPOLOGY -->",
        json.dumps(payload, indent=2),
        "<!-- /WORKTREE_TOPOLOGY -->",
    ]
    return lines


def x_render_topology_json__mutmut_40(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as structured JSON for prompt injection.

    Only call this when topology.has_stacking is True.
    Output is wrapped in HTML comment markers for reliable agent parsing.

    Args:
        topology: Feature topology data
        current_wp_id: The WP being implemented/reviewed

    Returns:
        List of lines to append to prompt
    """
    current_entry = topology.get_entry(current_wp_id)

    # Build base info for current WP
    your_base = None
    if current_entry and current_entry.base_wp:
        your_base = {
            "branch": current_entry.base_branch,
            "wp": current_entry.base_wp,
        }

    # Build diff command
    diff_base = topology.get_actual_base_for_wp(current_wp_id)
    diff_command = f"git diff {diff_base}..HEAD"

    # Build entries list
    entries_json = []
    for entry in topology.entries:
        entry_data: dict = {
            "wp": entry.wp_id,
            "lane": entry.lane,
            "branch": entry.branch_name,
            "base": entry.base_wp if entry.base_wp else topology.target_branch,
        }
        if entry.worktree_exists:
            entry_data["commits_ahead"] = entry.commits_ahead_of_base
        if entry.dependencies and not entry.worktree_exists:
            entry_data["dependencies"] = entry.dependencies
        entries_json.append(entry_data)

    payload = {
        "feature": topology.feature_slug,
        "target_branch": topology.target_branch,
        "current_wp": current_wp_id,
        "YOUR_BASE": your_base,
        "diff_command": diff_command,
        "stacked": True,
        "note": f"Your branch stacks on {current_entry.base_wp}, NOT {topology.target_branch}. Do not worry about being 'behind {topology.target_branch}'."
            if current_entry and current_entry.base_wp
            else f"Your branch is based on {topology.target_branch}. Other WPs in this feature use stacking.",
        "entries": entries_json,
    }

    lines = [
        "<!-- WORKTREE_TOPOLOGY -->",
        json.dumps(payload, indent=2),
        "<!-- /WORKTREE_TOPOLOGY -->",
    ]
    return lines


def x_render_topology_json__mutmut_41(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as structured JSON for prompt injection.

    Only call this when topology.has_stacking is True.
    Output is wrapped in HTML comment markers for reliable agent parsing.

    Args:
        topology: Feature topology data
        current_wp_id: The WP being implemented/reviewed

    Returns:
        List of lines to append to prompt
    """
    current_entry = topology.get_entry(current_wp_id)

    # Build base info for current WP
    your_base = None
    if current_entry and current_entry.base_wp:
        your_base = {
            "branch": current_entry.base_branch,
            "wp": current_entry.base_wp,
        }

    # Build diff command
    diff_base = topology.get_actual_base_for_wp(current_wp_id)
    diff_command = f"git diff {diff_base}..HEAD"

    # Build entries list
    entries_json = []
    for entry in topology.entries:
        entry_data: dict = {
            "wp": entry.wp_id,
            "lane": entry.lane,
            "branch": entry.branch_name,
            "base": entry.base_wp if entry.base_wp else topology.target_branch,
        }
        if entry.worktree_exists:
            entry_data["commits_ahead"] = entry.commits_ahead_of_base
        if entry.dependencies and not entry.worktree_exists:
            entry_data["dependencies"] = entry.dependencies
        entries_json.append(entry_data)

    payload = {
        "feature": topology.feature_slug,
        "target_branch": topology.target_branch,
        "current_wp": current_wp_id,
        "your_base": your_base,
        "XXdiff_commandXX": diff_command,
        "stacked": True,
        "note": f"Your branch stacks on {current_entry.base_wp}, NOT {topology.target_branch}. Do not worry about being 'behind {topology.target_branch}'."
            if current_entry and current_entry.base_wp
            else f"Your branch is based on {topology.target_branch}. Other WPs in this feature use stacking.",
        "entries": entries_json,
    }

    lines = [
        "<!-- WORKTREE_TOPOLOGY -->",
        json.dumps(payload, indent=2),
        "<!-- /WORKTREE_TOPOLOGY -->",
    ]
    return lines


def x_render_topology_json__mutmut_42(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as structured JSON for prompt injection.

    Only call this when topology.has_stacking is True.
    Output is wrapped in HTML comment markers for reliable agent parsing.

    Args:
        topology: Feature topology data
        current_wp_id: The WP being implemented/reviewed

    Returns:
        List of lines to append to prompt
    """
    current_entry = topology.get_entry(current_wp_id)

    # Build base info for current WP
    your_base = None
    if current_entry and current_entry.base_wp:
        your_base = {
            "branch": current_entry.base_branch,
            "wp": current_entry.base_wp,
        }

    # Build diff command
    diff_base = topology.get_actual_base_for_wp(current_wp_id)
    diff_command = f"git diff {diff_base}..HEAD"

    # Build entries list
    entries_json = []
    for entry in topology.entries:
        entry_data: dict = {
            "wp": entry.wp_id,
            "lane": entry.lane,
            "branch": entry.branch_name,
            "base": entry.base_wp if entry.base_wp else topology.target_branch,
        }
        if entry.worktree_exists:
            entry_data["commits_ahead"] = entry.commits_ahead_of_base
        if entry.dependencies and not entry.worktree_exists:
            entry_data["dependencies"] = entry.dependencies
        entries_json.append(entry_data)

    payload = {
        "feature": topology.feature_slug,
        "target_branch": topology.target_branch,
        "current_wp": current_wp_id,
        "your_base": your_base,
        "DIFF_COMMAND": diff_command,
        "stacked": True,
        "note": f"Your branch stacks on {current_entry.base_wp}, NOT {topology.target_branch}. Do not worry about being 'behind {topology.target_branch}'."
            if current_entry and current_entry.base_wp
            else f"Your branch is based on {topology.target_branch}. Other WPs in this feature use stacking.",
        "entries": entries_json,
    }

    lines = [
        "<!-- WORKTREE_TOPOLOGY -->",
        json.dumps(payload, indent=2),
        "<!-- /WORKTREE_TOPOLOGY -->",
    ]
    return lines


def x_render_topology_json__mutmut_43(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as structured JSON for prompt injection.

    Only call this when topology.has_stacking is True.
    Output is wrapped in HTML comment markers for reliable agent parsing.

    Args:
        topology: Feature topology data
        current_wp_id: The WP being implemented/reviewed

    Returns:
        List of lines to append to prompt
    """
    current_entry = topology.get_entry(current_wp_id)

    # Build base info for current WP
    your_base = None
    if current_entry and current_entry.base_wp:
        your_base = {
            "branch": current_entry.base_branch,
            "wp": current_entry.base_wp,
        }

    # Build diff command
    diff_base = topology.get_actual_base_for_wp(current_wp_id)
    diff_command = f"git diff {diff_base}..HEAD"

    # Build entries list
    entries_json = []
    for entry in topology.entries:
        entry_data: dict = {
            "wp": entry.wp_id,
            "lane": entry.lane,
            "branch": entry.branch_name,
            "base": entry.base_wp if entry.base_wp else topology.target_branch,
        }
        if entry.worktree_exists:
            entry_data["commits_ahead"] = entry.commits_ahead_of_base
        if entry.dependencies and not entry.worktree_exists:
            entry_data["dependencies"] = entry.dependencies
        entries_json.append(entry_data)

    payload = {
        "feature": topology.feature_slug,
        "target_branch": topology.target_branch,
        "current_wp": current_wp_id,
        "your_base": your_base,
        "diff_command": diff_command,
        "XXstackedXX": True,
        "note": f"Your branch stacks on {current_entry.base_wp}, NOT {topology.target_branch}. Do not worry about being 'behind {topology.target_branch}'."
            if current_entry and current_entry.base_wp
            else f"Your branch is based on {topology.target_branch}. Other WPs in this feature use stacking.",
        "entries": entries_json,
    }

    lines = [
        "<!-- WORKTREE_TOPOLOGY -->",
        json.dumps(payload, indent=2),
        "<!-- /WORKTREE_TOPOLOGY -->",
    ]
    return lines


def x_render_topology_json__mutmut_44(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as structured JSON for prompt injection.

    Only call this when topology.has_stacking is True.
    Output is wrapped in HTML comment markers for reliable agent parsing.

    Args:
        topology: Feature topology data
        current_wp_id: The WP being implemented/reviewed

    Returns:
        List of lines to append to prompt
    """
    current_entry = topology.get_entry(current_wp_id)

    # Build base info for current WP
    your_base = None
    if current_entry and current_entry.base_wp:
        your_base = {
            "branch": current_entry.base_branch,
            "wp": current_entry.base_wp,
        }

    # Build diff command
    diff_base = topology.get_actual_base_for_wp(current_wp_id)
    diff_command = f"git diff {diff_base}..HEAD"

    # Build entries list
    entries_json = []
    for entry in topology.entries:
        entry_data: dict = {
            "wp": entry.wp_id,
            "lane": entry.lane,
            "branch": entry.branch_name,
            "base": entry.base_wp if entry.base_wp else topology.target_branch,
        }
        if entry.worktree_exists:
            entry_data["commits_ahead"] = entry.commits_ahead_of_base
        if entry.dependencies and not entry.worktree_exists:
            entry_data["dependencies"] = entry.dependencies
        entries_json.append(entry_data)

    payload = {
        "feature": topology.feature_slug,
        "target_branch": topology.target_branch,
        "current_wp": current_wp_id,
        "your_base": your_base,
        "diff_command": diff_command,
        "STACKED": True,
        "note": f"Your branch stacks on {current_entry.base_wp}, NOT {topology.target_branch}. Do not worry about being 'behind {topology.target_branch}'."
            if current_entry and current_entry.base_wp
            else f"Your branch is based on {topology.target_branch}. Other WPs in this feature use stacking.",
        "entries": entries_json,
    }

    lines = [
        "<!-- WORKTREE_TOPOLOGY -->",
        json.dumps(payload, indent=2),
        "<!-- /WORKTREE_TOPOLOGY -->",
    ]
    return lines


def x_render_topology_json__mutmut_45(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as structured JSON for prompt injection.

    Only call this when topology.has_stacking is True.
    Output is wrapped in HTML comment markers for reliable agent parsing.

    Args:
        topology: Feature topology data
        current_wp_id: The WP being implemented/reviewed

    Returns:
        List of lines to append to prompt
    """
    current_entry = topology.get_entry(current_wp_id)

    # Build base info for current WP
    your_base = None
    if current_entry and current_entry.base_wp:
        your_base = {
            "branch": current_entry.base_branch,
            "wp": current_entry.base_wp,
        }

    # Build diff command
    diff_base = topology.get_actual_base_for_wp(current_wp_id)
    diff_command = f"git diff {diff_base}..HEAD"

    # Build entries list
    entries_json = []
    for entry in topology.entries:
        entry_data: dict = {
            "wp": entry.wp_id,
            "lane": entry.lane,
            "branch": entry.branch_name,
            "base": entry.base_wp if entry.base_wp else topology.target_branch,
        }
        if entry.worktree_exists:
            entry_data["commits_ahead"] = entry.commits_ahead_of_base
        if entry.dependencies and not entry.worktree_exists:
            entry_data["dependencies"] = entry.dependencies
        entries_json.append(entry_data)

    payload = {
        "feature": topology.feature_slug,
        "target_branch": topology.target_branch,
        "current_wp": current_wp_id,
        "your_base": your_base,
        "diff_command": diff_command,
        "stacked": False,
        "note": f"Your branch stacks on {current_entry.base_wp}, NOT {topology.target_branch}. Do not worry about being 'behind {topology.target_branch}'."
            if current_entry and current_entry.base_wp
            else f"Your branch is based on {topology.target_branch}. Other WPs in this feature use stacking.",
        "entries": entries_json,
    }

    lines = [
        "<!-- WORKTREE_TOPOLOGY -->",
        json.dumps(payload, indent=2),
        "<!-- /WORKTREE_TOPOLOGY -->",
    ]
    return lines


def x_render_topology_json__mutmut_46(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as structured JSON for prompt injection.

    Only call this when topology.has_stacking is True.
    Output is wrapped in HTML comment markers for reliable agent parsing.

    Args:
        topology: Feature topology data
        current_wp_id: The WP being implemented/reviewed

    Returns:
        List of lines to append to prompt
    """
    current_entry = topology.get_entry(current_wp_id)

    # Build base info for current WP
    your_base = None
    if current_entry and current_entry.base_wp:
        your_base = {
            "branch": current_entry.base_branch,
            "wp": current_entry.base_wp,
        }

    # Build diff command
    diff_base = topology.get_actual_base_for_wp(current_wp_id)
    diff_command = f"git diff {diff_base}..HEAD"

    # Build entries list
    entries_json = []
    for entry in topology.entries:
        entry_data: dict = {
            "wp": entry.wp_id,
            "lane": entry.lane,
            "branch": entry.branch_name,
            "base": entry.base_wp if entry.base_wp else topology.target_branch,
        }
        if entry.worktree_exists:
            entry_data["commits_ahead"] = entry.commits_ahead_of_base
        if entry.dependencies and not entry.worktree_exists:
            entry_data["dependencies"] = entry.dependencies
        entries_json.append(entry_data)

    payload = {
        "feature": topology.feature_slug,
        "target_branch": topology.target_branch,
        "current_wp": current_wp_id,
        "your_base": your_base,
        "diff_command": diff_command,
        "stacked": True,
        "XXnoteXX": f"Your branch stacks on {current_entry.base_wp}, NOT {topology.target_branch}. Do not worry about being 'behind {topology.target_branch}'."
            if current_entry and current_entry.base_wp
            else f"Your branch is based on {topology.target_branch}. Other WPs in this feature use stacking.",
        "entries": entries_json,
    }

    lines = [
        "<!-- WORKTREE_TOPOLOGY -->",
        json.dumps(payload, indent=2),
        "<!-- /WORKTREE_TOPOLOGY -->",
    ]
    return lines


def x_render_topology_json__mutmut_47(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as structured JSON for prompt injection.

    Only call this when topology.has_stacking is True.
    Output is wrapped in HTML comment markers for reliable agent parsing.

    Args:
        topology: Feature topology data
        current_wp_id: The WP being implemented/reviewed

    Returns:
        List of lines to append to prompt
    """
    current_entry = topology.get_entry(current_wp_id)

    # Build base info for current WP
    your_base = None
    if current_entry and current_entry.base_wp:
        your_base = {
            "branch": current_entry.base_branch,
            "wp": current_entry.base_wp,
        }

    # Build diff command
    diff_base = topology.get_actual_base_for_wp(current_wp_id)
    diff_command = f"git diff {diff_base}..HEAD"

    # Build entries list
    entries_json = []
    for entry in topology.entries:
        entry_data: dict = {
            "wp": entry.wp_id,
            "lane": entry.lane,
            "branch": entry.branch_name,
            "base": entry.base_wp if entry.base_wp else topology.target_branch,
        }
        if entry.worktree_exists:
            entry_data["commits_ahead"] = entry.commits_ahead_of_base
        if entry.dependencies and not entry.worktree_exists:
            entry_data["dependencies"] = entry.dependencies
        entries_json.append(entry_data)

    payload = {
        "feature": topology.feature_slug,
        "target_branch": topology.target_branch,
        "current_wp": current_wp_id,
        "your_base": your_base,
        "diff_command": diff_command,
        "stacked": True,
        "NOTE": f"Your branch stacks on {current_entry.base_wp}, NOT {topology.target_branch}. Do not worry about being 'behind {topology.target_branch}'."
            if current_entry and current_entry.base_wp
            else f"Your branch is based on {topology.target_branch}. Other WPs in this feature use stacking.",
        "entries": entries_json,
    }

    lines = [
        "<!-- WORKTREE_TOPOLOGY -->",
        json.dumps(payload, indent=2),
        "<!-- /WORKTREE_TOPOLOGY -->",
    ]
    return lines


def x_render_topology_json__mutmut_48(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as structured JSON for prompt injection.

    Only call this when topology.has_stacking is True.
    Output is wrapped in HTML comment markers for reliable agent parsing.

    Args:
        topology: Feature topology data
        current_wp_id: The WP being implemented/reviewed

    Returns:
        List of lines to append to prompt
    """
    current_entry = topology.get_entry(current_wp_id)

    # Build base info for current WP
    your_base = None
    if current_entry and current_entry.base_wp:
        your_base = {
            "branch": current_entry.base_branch,
            "wp": current_entry.base_wp,
        }

    # Build diff command
    diff_base = topology.get_actual_base_for_wp(current_wp_id)
    diff_command = f"git diff {diff_base}..HEAD"

    # Build entries list
    entries_json = []
    for entry in topology.entries:
        entry_data: dict = {
            "wp": entry.wp_id,
            "lane": entry.lane,
            "branch": entry.branch_name,
            "base": entry.base_wp if entry.base_wp else topology.target_branch,
        }
        if entry.worktree_exists:
            entry_data["commits_ahead"] = entry.commits_ahead_of_base
        if entry.dependencies and not entry.worktree_exists:
            entry_data["dependencies"] = entry.dependencies
        entries_json.append(entry_data)

    payload = {
        "feature": topology.feature_slug,
        "target_branch": topology.target_branch,
        "current_wp": current_wp_id,
        "your_base": your_base,
        "diff_command": diff_command,
        "stacked": True,
        "note": f"Your branch stacks on {current_entry.base_wp}, NOT {topology.target_branch}. Do not worry about being 'behind {topology.target_branch}'."
            if current_entry or current_entry.base_wp
            else f"Your branch is based on {topology.target_branch}. Other WPs in this feature use stacking.",
        "entries": entries_json,
    }

    lines = [
        "<!-- WORKTREE_TOPOLOGY -->",
        json.dumps(payload, indent=2),
        "<!-- /WORKTREE_TOPOLOGY -->",
    ]
    return lines


def x_render_topology_json__mutmut_49(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as structured JSON for prompt injection.

    Only call this when topology.has_stacking is True.
    Output is wrapped in HTML comment markers for reliable agent parsing.

    Args:
        topology: Feature topology data
        current_wp_id: The WP being implemented/reviewed

    Returns:
        List of lines to append to prompt
    """
    current_entry = topology.get_entry(current_wp_id)

    # Build base info for current WP
    your_base = None
    if current_entry and current_entry.base_wp:
        your_base = {
            "branch": current_entry.base_branch,
            "wp": current_entry.base_wp,
        }

    # Build diff command
    diff_base = topology.get_actual_base_for_wp(current_wp_id)
    diff_command = f"git diff {diff_base}..HEAD"

    # Build entries list
    entries_json = []
    for entry in topology.entries:
        entry_data: dict = {
            "wp": entry.wp_id,
            "lane": entry.lane,
            "branch": entry.branch_name,
            "base": entry.base_wp if entry.base_wp else topology.target_branch,
        }
        if entry.worktree_exists:
            entry_data["commits_ahead"] = entry.commits_ahead_of_base
        if entry.dependencies and not entry.worktree_exists:
            entry_data["dependencies"] = entry.dependencies
        entries_json.append(entry_data)

    payload = {
        "feature": topology.feature_slug,
        "target_branch": topology.target_branch,
        "current_wp": current_wp_id,
        "your_base": your_base,
        "diff_command": diff_command,
        "stacked": True,
        "note": f"Your branch stacks on {current_entry.base_wp}, NOT {topology.target_branch}. Do not worry about being 'behind {topology.target_branch}'."
            if current_entry and current_entry.base_wp
            else f"Your branch is based on {topology.target_branch}. Other WPs in this feature use stacking.",
        "XXentriesXX": entries_json,
    }

    lines = [
        "<!-- WORKTREE_TOPOLOGY -->",
        json.dumps(payload, indent=2),
        "<!-- /WORKTREE_TOPOLOGY -->",
    ]
    return lines


def x_render_topology_json__mutmut_50(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as structured JSON for prompt injection.

    Only call this when topology.has_stacking is True.
    Output is wrapped in HTML comment markers for reliable agent parsing.

    Args:
        topology: Feature topology data
        current_wp_id: The WP being implemented/reviewed

    Returns:
        List of lines to append to prompt
    """
    current_entry = topology.get_entry(current_wp_id)

    # Build base info for current WP
    your_base = None
    if current_entry and current_entry.base_wp:
        your_base = {
            "branch": current_entry.base_branch,
            "wp": current_entry.base_wp,
        }

    # Build diff command
    diff_base = topology.get_actual_base_for_wp(current_wp_id)
    diff_command = f"git diff {diff_base}..HEAD"

    # Build entries list
    entries_json = []
    for entry in topology.entries:
        entry_data: dict = {
            "wp": entry.wp_id,
            "lane": entry.lane,
            "branch": entry.branch_name,
            "base": entry.base_wp if entry.base_wp else topology.target_branch,
        }
        if entry.worktree_exists:
            entry_data["commits_ahead"] = entry.commits_ahead_of_base
        if entry.dependencies and not entry.worktree_exists:
            entry_data["dependencies"] = entry.dependencies
        entries_json.append(entry_data)

    payload = {
        "feature": topology.feature_slug,
        "target_branch": topology.target_branch,
        "current_wp": current_wp_id,
        "your_base": your_base,
        "diff_command": diff_command,
        "stacked": True,
        "note": f"Your branch stacks on {current_entry.base_wp}, NOT {topology.target_branch}. Do not worry about being 'behind {topology.target_branch}'."
            if current_entry and current_entry.base_wp
            else f"Your branch is based on {topology.target_branch}. Other WPs in this feature use stacking.",
        "ENTRIES": entries_json,
    }

    lines = [
        "<!-- WORKTREE_TOPOLOGY -->",
        json.dumps(payload, indent=2),
        "<!-- /WORKTREE_TOPOLOGY -->",
    ]
    return lines


def x_render_topology_json__mutmut_51(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as structured JSON for prompt injection.

    Only call this when topology.has_stacking is True.
    Output is wrapped in HTML comment markers for reliable agent parsing.

    Args:
        topology: Feature topology data
        current_wp_id: The WP being implemented/reviewed

    Returns:
        List of lines to append to prompt
    """
    current_entry = topology.get_entry(current_wp_id)

    # Build base info for current WP
    your_base = None
    if current_entry and current_entry.base_wp:
        your_base = {
            "branch": current_entry.base_branch,
            "wp": current_entry.base_wp,
        }

    # Build diff command
    diff_base = topology.get_actual_base_for_wp(current_wp_id)
    diff_command = f"git diff {diff_base}..HEAD"

    # Build entries list
    entries_json = []
    for entry in topology.entries:
        entry_data: dict = {
            "wp": entry.wp_id,
            "lane": entry.lane,
            "branch": entry.branch_name,
            "base": entry.base_wp if entry.base_wp else topology.target_branch,
        }
        if entry.worktree_exists:
            entry_data["commits_ahead"] = entry.commits_ahead_of_base
        if entry.dependencies and not entry.worktree_exists:
            entry_data["dependencies"] = entry.dependencies
        entries_json.append(entry_data)

    payload = {
        "feature": topology.feature_slug,
        "target_branch": topology.target_branch,
        "current_wp": current_wp_id,
        "your_base": your_base,
        "diff_command": diff_command,
        "stacked": True,
        "note": f"Your branch stacks on {current_entry.base_wp}, NOT {topology.target_branch}. Do not worry about being 'behind {topology.target_branch}'."
            if current_entry and current_entry.base_wp
            else f"Your branch is based on {topology.target_branch}. Other WPs in this feature use stacking.",
        "entries": entries_json,
    }

    lines = None
    return lines


def x_render_topology_json__mutmut_52(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as structured JSON for prompt injection.

    Only call this when topology.has_stacking is True.
    Output is wrapped in HTML comment markers for reliable agent parsing.

    Args:
        topology: Feature topology data
        current_wp_id: The WP being implemented/reviewed

    Returns:
        List of lines to append to prompt
    """
    current_entry = topology.get_entry(current_wp_id)

    # Build base info for current WP
    your_base = None
    if current_entry and current_entry.base_wp:
        your_base = {
            "branch": current_entry.base_branch,
            "wp": current_entry.base_wp,
        }

    # Build diff command
    diff_base = topology.get_actual_base_for_wp(current_wp_id)
    diff_command = f"git diff {diff_base}..HEAD"

    # Build entries list
    entries_json = []
    for entry in topology.entries:
        entry_data: dict = {
            "wp": entry.wp_id,
            "lane": entry.lane,
            "branch": entry.branch_name,
            "base": entry.base_wp if entry.base_wp else topology.target_branch,
        }
        if entry.worktree_exists:
            entry_data["commits_ahead"] = entry.commits_ahead_of_base
        if entry.dependencies and not entry.worktree_exists:
            entry_data["dependencies"] = entry.dependencies
        entries_json.append(entry_data)

    payload = {
        "feature": topology.feature_slug,
        "target_branch": topology.target_branch,
        "current_wp": current_wp_id,
        "your_base": your_base,
        "diff_command": diff_command,
        "stacked": True,
        "note": f"Your branch stacks on {current_entry.base_wp}, NOT {topology.target_branch}. Do not worry about being 'behind {topology.target_branch}'."
            if current_entry and current_entry.base_wp
            else f"Your branch is based on {topology.target_branch}. Other WPs in this feature use stacking.",
        "entries": entries_json,
    }

    lines = [
        "XX<!-- WORKTREE_TOPOLOGY -->XX",
        json.dumps(payload, indent=2),
        "<!-- /WORKTREE_TOPOLOGY -->",
    ]
    return lines


def x_render_topology_json__mutmut_53(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as structured JSON for prompt injection.

    Only call this when topology.has_stacking is True.
    Output is wrapped in HTML comment markers for reliable agent parsing.

    Args:
        topology: Feature topology data
        current_wp_id: The WP being implemented/reviewed

    Returns:
        List of lines to append to prompt
    """
    current_entry = topology.get_entry(current_wp_id)

    # Build base info for current WP
    your_base = None
    if current_entry and current_entry.base_wp:
        your_base = {
            "branch": current_entry.base_branch,
            "wp": current_entry.base_wp,
        }

    # Build diff command
    diff_base = topology.get_actual_base_for_wp(current_wp_id)
    diff_command = f"git diff {diff_base}..HEAD"

    # Build entries list
    entries_json = []
    for entry in topology.entries:
        entry_data: dict = {
            "wp": entry.wp_id,
            "lane": entry.lane,
            "branch": entry.branch_name,
            "base": entry.base_wp if entry.base_wp else topology.target_branch,
        }
        if entry.worktree_exists:
            entry_data["commits_ahead"] = entry.commits_ahead_of_base
        if entry.dependencies and not entry.worktree_exists:
            entry_data["dependencies"] = entry.dependencies
        entries_json.append(entry_data)

    payload = {
        "feature": topology.feature_slug,
        "target_branch": topology.target_branch,
        "current_wp": current_wp_id,
        "your_base": your_base,
        "diff_command": diff_command,
        "stacked": True,
        "note": f"Your branch stacks on {current_entry.base_wp}, NOT {topology.target_branch}. Do not worry about being 'behind {topology.target_branch}'."
            if current_entry and current_entry.base_wp
            else f"Your branch is based on {topology.target_branch}. Other WPs in this feature use stacking.",
        "entries": entries_json,
    }

    lines = [
        "<!-- worktree_topology -->",
        json.dumps(payload, indent=2),
        "<!-- /WORKTREE_TOPOLOGY -->",
    ]
    return lines


def x_render_topology_json__mutmut_54(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as structured JSON for prompt injection.

    Only call this when topology.has_stacking is True.
    Output is wrapped in HTML comment markers for reliable agent parsing.

    Args:
        topology: Feature topology data
        current_wp_id: The WP being implemented/reviewed

    Returns:
        List of lines to append to prompt
    """
    current_entry = topology.get_entry(current_wp_id)

    # Build base info for current WP
    your_base = None
    if current_entry and current_entry.base_wp:
        your_base = {
            "branch": current_entry.base_branch,
            "wp": current_entry.base_wp,
        }

    # Build diff command
    diff_base = topology.get_actual_base_for_wp(current_wp_id)
    diff_command = f"git diff {diff_base}..HEAD"

    # Build entries list
    entries_json = []
    for entry in topology.entries:
        entry_data: dict = {
            "wp": entry.wp_id,
            "lane": entry.lane,
            "branch": entry.branch_name,
            "base": entry.base_wp if entry.base_wp else topology.target_branch,
        }
        if entry.worktree_exists:
            entry_data["commits_ahead"] = entry.commits_ahead_of_base
        if entry.dependencies and not entry.worktree_exists:
            entry_data["dependencies"] = entry.dependencies
        entries_json.append(entry_data)

    payload = {
        "feature": topology.feature_slug,
        "target_branch": topology.target_branch,
        "current_wp": current_wp_id,
        "your_base": your_base,
        "diff_command": diff_command,
        "stacked": True,
        "note": f"Your branch stacks on {current_entry.base_wp}, NOT {topology.target_branch}. Do not worry about being 'behind {topology.target_branch}'."
            if current_entry and current_entry.base_wp
            else f"Your branch is based on {topology.target_branch}. Other WPs in this feature use stacking.",
        "entries": entries_json,
    }

    lines = [
        "<!-- WORKTREE_TOPOLOGY -->",
        json.dumps(None, indent=2),
        "<!-- /WORKTREE_TOPOLOGY -->",
    ]
    return lines


def x_render_topology_json__mutmut_55(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as structured JSON for prompt injection.

    Only call this when topology.has_stacking is True.
    Output is wrapped in HTML comment markers for reliable agent parsing.

    Args:
        topology: Feature topology data
        current_wp_id: The WP being implemented/reviewed

    Returns:
        List of lines to append to prompt
    """
    current_entry = topology.get_entry(current_wp_id)

    # Build base info for current WP
    your_base = None
    if current_entry and current_entry.base_wp:
        your_base = {
            "branch": current_entry.base_branch,
            "wp": current_entry.base_wp,
        }

    # Build diff command
    diff_base = topology.get_actual_base_for_wp(current_wp_id)
    diff_command = f"git diff {diff_base}..HEAD"

    # Build entries list
    entries_json = []
    for entry in topology.entries:
        entry_data: dict = {
            "wp": entry.wp_id,
            "lane": entry.lane,
            "branch": entry.branch_name,
            "base": entry.base_wp if entry.base_wp else topology.target_branch,
        }
        if entry.worktree_exists:
            entry_data["commits_ahead"] = entry.commits_ahead_of_base
        if entry.dependencies and not entry.worktree_exists:
            entry_data["dependencies"] = entry.dependencies
        entries_json.append(entry_data)

    payload = {
        "feature": topology.feature_slug,
        "target_branch": topology.target_branch,
        "current_wp": current_wp_id,
        "your_base": your_base,
        "diff_command": diff_command,
        "stacked": True,
        "note": f"Your branch stacks on {current_entry.base_wp}, NOT {topology.target_branch}. Do not worry about being 'behind {topology.target_branch}'."
            if current_entry and current_entry.base_wp
            else f"Your branch is based on {topology.target_branch}. Other WPs in this feature use stacking.",
        "entries": entries_json,
    }

    lines = [
        "<!-- WORKTREE_TOPOLOGY -->",
        json.dumps(payload, indent=None),
        "<!-- /WORKTREE_TOPOLOGY -->",
    ]
    return lines


def x_render_topology_json__mutmut_56(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as structured JSON for prompt injection.

    Only call this when topology.has_stacking is True.
    Output is wrapped in HTML comment markers for reliable agent parsing.

    Args:
        topology: Feature topology data
        current_wp_id: The WP being implemented/reviewed

    Returns:
        List of lines to append to prompt
    """
    current_entry = topology.get_entry(current_wp_id)

    # Build base info for current WP
    your_base = None
    if current_entry and current_entry.base_wp:
        your_base = {
            "branch": current_entry.base_branch,
            "wp": current_entry.base_wp,
        }

    # Build diff command
    diff_base = topology.get_actual_base_for_wp(current_wp_id)
    diff_command = f"git diff {diff_base}..HEAD"

    # Build entries list
    entries_json = []
    for entry in topology.entries:
        entry_data: dict = {
            "wp": entry.wp_id,
            "lane": entry.lane,
            "branch": entry.branch_name,
            "base": entry.base_wp if entry.base_wp else topology.target_branch,
        }
        if entry.worktree_exists:
            entry_data["commits_ahead"] = entry.commits_ahead_of_base
        if entry.dependencies and not entry.worktree_exists:
            entry_data["dependencies"] = entry.dependencies
        entries_json.append(entry_data)

    payload = {
        "feature": topology.feature_slug,
        "target_branch": topology.target_branch,
        "current_wp": current_wp_id,
        "your_base": your_base,
        "diff_command": diff_command,
        "stacked": True,
        "note": f"Your branch stacks on {current_entry.base_wp}, NOT {topology.target_branch}. Do not worry about being 'behind {topology.target_branch}'."
            if current_entry and current_entry.base_wp
            else f"Your branch is based on {topology.target_branch}. Other WPs in this feature use stacking.",
        "entries": entries_json,
    }

    lines = [
        "<!-- WORKTREE_TOPOLOGY -->",
        json.dumps(indent=2),
        "<!-- /WORKTREE_TOPOLOGY -->",
    ]
    return lines


def x_render_topology_json__mutmut_57(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as structured JSON for prompt injection.

    Only call this when topology.has_stacking is True.
    Output is wrapped in HTML comment markers for reliable agent parsing.

    Args:
        topology: Feature topology data
        current_wp_id: The WP being implemented/reviewed

    Returns:
        List of lines to append to prompt
    """
    current_entry = topology.get_entry(current_wp_id)

    # Build base info for current WP
    your_base = None
    if current_entry and current_entry.base_wp:
        your_base = {
            "branch": current_entry.base_branch,
            "wp": current_entry.base_wp,
        }

    # Build diff command
    diff_base = topology.get_actual_base_for_wp(current_wp_id)
    diff_command = f"git diff {diff_base}..HEAD"

    # Build entries list
    entries_json = []
    for entry in topology.entries:
        entry_data: dict = {
            "wp": entry.wp_id,
            "lane": entry.lane,
            "branch": entry.branch_name,
            "base": entry.base_wp if entry.base_wp else topology.target_branch,
        }
        if entry.worktree_exists:
            entry_data["commits_ahead"] = entry.commits_ahead_of_base
        if entry.dependencies and not entry.worktree_exists:
            entry_data["dependencies"] = entry.dependencies
        entries_json.append(entry_data)

    payload = {
        "feature": topology.feature_slug,
        "target_branch": topology.target_branch,
        "current_wp": current_wp_id,
        "your_base": your_base,
        "diff_command": diff_command,
        "stacked": True,
        "note": f"Your branch stacks on {current_entry.base_wp}, NOT {topology.target_branch}. Do not worry about being 'behind {topology.target_branch}'."
            if current_entry and current_entry.base_wp
            else f"Your branch is based on {topology.target_branch}. Other WPs in this feature use stacking.",
        "entries": entries_json,
    }

    lines = [
        "<!-- WORKTREE_TOPOLOGY -->",
        json.dumps(payload, ),
        "<!-- /WORKTREE_TOPOLOGY -->",
    ]
    return lines


def x_render_topology_json__mutmut_58(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as structured JSON for prompt injection.

    Only call this when topology.has_stacking is True.
    Output is wrapped in HTML comment markers for reliable agent parsing.

    Args:
        topology: Feature topology data
        current_wp_id: The WP being implemented/reviewed

    Returns:
        List of lines to append to prompt
    """
    current_entry = topology.get_entry(current_wp_id)

    # Build base info for current WP
    your_base = None
    if current_entry and current_entry.base_wp:
        your_base = {
            "branch": current_entry.base_branch,
            "wp": current_entry.base_wp,
        }

    # Build diff command
    diff_base = topology.get_actual_base_for_wp(current_wp_id)
    diff_command = f"git diff {diff_base}..HEAD"

    # Build entries list
    entries_json = []
    for entry in topology.entries:
        entry_data: dict = {
            "wp": entry.wp_id,
            "lane": entry.lane,
            "branch": entry.branch_name,
            "base": entry.base_wp if entry.base_wp else topology.target_branch,
        }
        if entry.worktree_exists:
            entry_data["commits_ahead"] = entry.commits_ahead_of_base
        if entry.dependencies and not entry.worktree_exists:
            entry_data["dependencies"] = entry.dependencies
        entries_json.append(entry_data)

    payload = {
        "feature": topology.feature_slug,
        "target_branch": topology.target_branch,
        "current_wp": current_wp_id,
        "your_base": your_base,
        "diff_command": diff_command,
        "stacked": True,
        "note": f"Your branch stacks on {current_entry.base_wp}, NOT {topology.target_branch}. Do not worry about being 'behind {topology.target_branch}'."
            if current_entry and current_entry.base_wp
            else f"Your branch is based on {topology.target_branch}. Other WPs in this feature use stacking.",
        "entries": entries_json,
    }

    lines = [
        "<!-- WORKTREE_TOPOLOGY -->",
        json.dumps(payload, indent=3),
        "<!-- /WORKTREE_TOPOLOGY -->",
    ]
    return lines


def x_render_topology_json__mutmut_59(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as structured JSON for prompt injection.

    Only call this when topology.has_stacking is True.
    Output is wrapped in HTML comment markers for reliable agent parsing.

    Args:
        topology: Feature topology data
        current_wp_id: The WP being implemented/reviewed

    Returns:
        List of lines to append to prompt
    """
    current_entry = topology.get_entry(current_wp_id)

    # Build base info for current WP
    your_base = None
    if current_entry and current_entry.base_wp:
        your_base = {
            "branch": current_entry.base_branch,
            "wp": current_entry.base_wp,
        }

    # Build diff command
    diff_base = topology.get_actual_base_for_wp(current_wp_id)
    diff_command = f"git diff {diff_base}..HEAD"

    # Build entries list
    entries_json = []
    for entry in topology.entries:
        entry_data: dict = {
            "wp": entry.wp_id,
            "lane": entry.lane,
            "branch": entry.branch_name,
            "base": entry.base_wp if entry.base_wp else topology.target_branch,
        }
        if entry.worktree_exists:
            entry_data["commits_ahead"] = entry.commits_ahead_of_base
        if entry.dependencies and not entry.worktree_exists:
            entry_data["dependencies"] = entry.dependencies
        entries_json.append(entry_data)

    payload = {
        "feature": topology.feature_slug,
        "target_branch": topology.target_branch,
        "current_wp": current_wp_id,
        "your_base": your_base,
        "diff_command": diff_command,
        "stacked": True,
        "note": f"Your branch stacks on {current_entry.base_wp}, NOT {topology.target_branch}. Do not worry about being 'behind {topology.target_branch}'."
            if current_entry and current_entry.base_wp
            else f"Your branch is based on {topology.target_branch}. Other WPs in this feature use stacking.",
        "entries": entries_json,
    }

    lines = [
        "<!-- WORKTREE_TOPOLOGY -->",
        json.dumps(payload, indent=2),
        "XX<!-- /WORKTREE_TOPOLOGY -->XX",
    ]
    return lines


def x_render_topology_json__mutmut_60(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as structured JSON for prompt injection.

    Only call this when topology.has_stacking is True.
    Output is wrapped in HTML comment markers for reliable agent parsing.

    Args:
        topology: Feature topology data
        current_wp_id: The WP being implemented/reviewed

    Returns:
        List of lines to append to prompt
    """
    current_entry = topology.get_entry(current_wp_id)

    # Build base info for current WP
    your_base = None
    if current_entry and current_entry.base_wp:
        your_base = {
            "branch": current_entry.base_branch,
            "wp": current_entry.base_wp,
        }

    # Build diff command
    diff_base = topology.get_actual_base_for_wp(current_wp_id)
    diff_command = f"git diff {diff_base}..HEAD"

    # Build entries list
    entries_json = []
    for entry in topology.entries:
        entry_data: dict = {
            "wp": entry.wp_id,
            "lane": entry.lane,
            "branch": entry.branch_name,
            "base": entry.base_wp if entry.base_wp else topology.target_branch,
        }
        if entry.worktree_exists:
            entry_data["commits_ahead"] = entry.commits_ahead_of_base
        if entry.dependencies and not entry.worktree_exists:
            entry_data["dependencies"] = entry.dependencies
        entries_json.append(entry_data)

    payload = {
        "feature": topology.feature_slug,
        "target_branch": topology.target_branch,
        "current_wp": current_wp_id,
        "your_base": your_base,
        "diff_command": diff_command,
        "stacked": True,
        "note": f"Your branch stacks on {current_entry.base_wp}, NOT {topology.target_branch}. Do not worry about being 'behind {topology.target_branch}'."
            if current_entry and current_entry.base_wp
            else f"Your branch is based on {topology.target_branch}. Other WPs in this feature use stacking.",
        "entries": entries_json,
    }

    lines = [
        "<!-- WORKTREE_TOPOLOGY -->",
        json.dumps(payload, indent=2),
        "<!-- /worktree_topology -->",
    ]
    return lines

x_render_topology_json__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_render_topology_json__mutmut_1': x_render_topology_json__mutmut_1, 
    'x_render_topology_json__mutmut_2': x_render_topology_json__mutmut_2, 
    'x_render_topology_json__mutmut_3': x_render_topology_json__mutmut_3, 
    'x_render_topology_json__mutmut_4': x_render_topology_json__mutmut_4, 
    'x_render_topology_json__mutmut_5': x_render_topology_json__mutmut_5, 
    'x_render_topology_json__mutmut_6': x_render_topology_json__mutmut_6, 
    'x_render_topology_json__mutmut_7': x_render_topology_json__mutmut_7, 
    'x_render_topology_json__mutmut_8': x_render_topology_json__mutmut_8, 
    'x_render_topology_json__mutmut_9': x_render_topology_json__mutmut_9, 
    'x_render_topology_json__mutmut_10': x_render_topology_json__mutmut_10, 
    'x_render_topology_json__mutmut_11': x_render_topology_json__mutmut_11, 
    'x_render_topology_json__mutmut_12': x_render_topology_json__mutmut_12, 
    'x_render_topology_json__mutmut_13': x_render_topology_json__mutmut_13, 
    'x_render_topology_json__mutmut_14': x_render_topology_json__mutmut_14, 
    'x_render_topology_json__mutmut_15': x_render_topology_json__mutmut_15, 
    'x_render_topology_json__mutmut_16': x_render_topology_json__mutmut_16, 
    'x_render_topology_json__mutmut_17': x_render_topology_json__mutmut_17, 
    'x_render_topology_json__mutmut_18': x_render_topology_json__mutmut_18, 
    'x_render_topology_json__mutmut_19': x_render_topology_json__mutmut_19, 
    'x_render_topology_json__mutmut_20': x_render_topology_json__mutmut_20, 
    'x_render_topology_json__mutmut_21': x_render_topology_json__mutmut_21, 
    'x_render_topology_json__mutmut_22': x_render_topology_json__mutmut_22, 
    'x_render_topology_json__mutmut_23': x_render_topology_json__mutmut_23, 
    'x_render_topology_json__mutmut_24': x_render_topology_json__mutmut_24, 
    'x_render_topology_json__mutmut_25': x_render_topology_json__mutmut_25, 
    'x_render_topology_json__mutmut_26': x_render_topology_json__mutmut_26, 
    'x_render_topology_json__mutmut_27': x_render_topology_json__mutmut_27, 
    'x_render_topology_json__mutmut_28': x_render_topology_json__mutmut_28, 
    'x_render_topology_json__mutmut_29': x_render_topology_json__mutmut_29, 
    'x_render_topology_json__mutmut_30': x_render_topology_json__mutmut_30, 
    'x_render_topology_json__mutmut_31': x_render_topology_json__mutmut_31, 
    'x_render_topology_json__mutmut_32': x_render_topology_json__mutmut_32, 
    'x_render_topology_json__mutmut_33': x_render_topology_json__mutmut_33, 
    'x_render_topology_json__mutmut_34': x_render_topology_json__mutmut_34, 
    'x_render_topology_json__mutmut_35': x_render_topology_json__mutmut_35, 
    'x_render_topology_json__mutmut_36': x_render_topology_json__mutmut_36, 
    'x_render_topology_json__mutmut_37': x_render_topology_json__mutmut_37, 
    'x_render_topology_json__mutmut_38': x_render_topology_json__mutmut_38, 
    'x_render_topology_json__mutmut_39': x_render_topology_json__mutmut_39, 
    'x_render_topology_json__mutmut_40': x_render_topology_json__mutmut_40, 
    'x_render_topology_json__mutmut_41': x_render_topology_json__mutmut_41, 
    'x_render_topology_json__mutmut_42': x_render_topology_json__mutmut_42, 
    'x_render_topology_json__mutmut_43': x_render_topology_json__mutmut_43, 
    'x_render_topology_json__mutmut_44': x_render_topology_json__mutmut_44, 
    'x_render_topology_json__mutmut_45': x_render_topology_json__mutmut_45, 
    'x_render_topology_json__mutmut_46': x_render_topology_json__mutmut_46, 
    'x_render_topology_json__mutmut_47': x_render_topology_json__mutmut_47, 
    'x_render_topology_json__mutmut_48': x_render_topology_json__mutmut_48, 
    'x_render_topology_json__mutmut_49': x_render_topology_json__mutmut_49, 
    'x_render_topology_json__mutmut_50': x_render_topology_json__mutmut_50, 
    'x_render_topology_json__mutmut_51': x_render_topology_json__mutmut_51, 
    'x_render_topology_json__mutmut_52': x_render_topology_json__mutmut_52, 
    'x_render_topology_json__mutmut_53': x_render_topology_json__mutmut_53, 
    'x_render_topology_json__mutmut_54': x_render_topology_json__mutmut_54, 
    'x_render_topology_json__mutmut_55': x_render_topology_json__mutmut_55, 
    'x_render_topology_json__mutmut_56': x_render_topology_json__mutmut_56, 
    'x_render_topology_json__mutmut_57': x_render_topology_json__mutmut_57, 
    'x_render_topology_json__mutmut_58': x_render_topology_json__mutmut_58, 
    'x_render_topology_json__mutmut_59': x_render_topology_json__mutmut_59, 
    'x_render_topology_json__mutmut_60': x_render_topology_json__mutmut_60
}
x_render_topology_json__mutmut_orig.__name__ = 'x_render_topology_json'


def render_topology_text(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    args = [topology, current_wp_id]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_render_topology_text__mutmut_orig, x_render_topology_text__mutmut_mutants, args, kwargs, None)


def x_render_topology_text__mutmut_orig(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as human-readable text for CLI output.

    Utility function for human-facing displays (not used in prompts).

    Args:
        topology: Feature topology data
        current_wp_id: The WP to highlight

    Returns:
        List of lines for console output
    """
    lines = []
    lines.append("╔" + "═" * 78 + "╗")
    lines.append("║  WORKTREE TOPOLOGY" + " " * 59 + "║")
    lines.append("╠" + "═" * 78 + "╣")
    lines.append(f"║  Feature: {topology.feature_slug:<66} ║")
    lines.append(f"║  Target:  {topology.target_branch:<66} ║")
    lines.append("║" + " " * 78 + "║")

    for entry in topology.entries:
        marker = "→" if entry.wp_id == current_wp_id else " "
        base_label = entry.base_wp if entry.base_wp else topology.target_branch
        branch_label = entry.branch_name or "(not created)"
        status = entry.lane

        line_text = f"{marker} {entry.wp_id} [{status}] base={base_label} branch={branch_label}"
        if entry.worktree_exists and entry.commits_ahead_of_base > 0:
            line_text += f" (+{entry.commits_ahead_of_base})"

        # Pad to fit box
        padded = line_text[:76].ljust(76)
        lines.append(f"║  {padded}║")

    lines.append("╚" + "═" * 78 + "╝")
    return lines


def x_render_topology_text__mutmut_1(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as human-readable text for CLI output.

    Utility function for human-facing displays (not used in prompts).

    Args:
        topology: Feature topology data
        current_wp_id: The WP to highlight

    Returns:
        List of lines for console output
    """
    lines = None
    lines.append("╔" + "═" * 78 + "╗")
    lines.append("║  WORKTREE TOPOLOGY" + " " * 59 + "║")
    lines.append("╠" + "═" * 78 + "╣")
    lines.append(f"║  Feature: {topology.feature_slug:<66} ║")
    lines.append(f"║  Target:  {topology.target_branch:<66} ║")
    lines.append("║" + " " * 78 + "║")

    for entry in topology.entries:
        marker = "→" if entry.wp_id == current_wp_id else " "
        base_label = entry.base_wp if entry.base_wp else topology.target_branch
        branch_label = entry.branch_name or "(not created)"
        status = entry.lane

        line_text = f"{marker} {entry.wp_id} [{status}] base={base_label} branch={branch_label}"
        if entry.worktree_exists and entry.commits_ahead_of_base > 0:
            line_text += f" (+{entry.commits_ahead_of_base})"

        # Pad to fit box
        padded = line_text[:76].ljust(76)
        lines.append(f"║  {padded}║")

    lines.append("╚" + "═" * 78 + "╝")
    return lines


def x_render_topology_text__mutmut_2(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as human-readable text for CLI output.

    Utility function for human-facing displays (not used in prompts).

    Args:
        topology: Feature topology data
        current_wp_id: The WP to highlight

    Returns:
        List of lines for console output
    """
    lines = []
    lines.append(None)
    lines.append("║  WORKTREE TOPOLOGY" + " " * 59 + "║")
    lines.append("╠" + "═" * 78 + "╣")
    lines.append(f"║  Feature: {topology.feature_slug:<66} ║")
    lines.append(f"║  Target:  {topology.target_branch:<66} ║")
    lines.append("║" + " " * 78 + "║")

    for entry in topology.entries:
        marker = "→" if entry.wp_id == current_wp_id else " "
        base_label = entry.base_wp if entry.base_wp else topology.target_branch
        branch_label = entry.branch_name or "(not created)"
        status = entry.lane

        line_text = f"{marker} {entry.wp_id} [{status}] base={base_label} branch={branch_label}"
        if entry.worktree_exists and entry.commits_ahead_of_base > 0:
            line_text += f" (+{entry.commits_ahead_of_base})"

        # Pad to fit box
        padded = line_text[:76].ljust(76)
        lines.append(f"║  {padded}║")

    lines.append("╚" + "═" * 78 + "╝")
    return lines


def x_render_topology_text__mutmut_3(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as human-readable text for CLI output.

    Utility function for human-facing displays (not used in prompts).

    Args:
        topology: Feature topology data
        current_wp_id: The WP to highlight

    Returns:
        List of lines for console output
    """
    lines = []
    lines.append("╔" + "═" * 78 - "╗")
    lines.append("║  WORKTREE TOPOLOGY" + " " * 59 + "║")
    lines.append("╠" + "═" * 78 + "╣")
    lines.append(f"║  Feature: {topology.feature_slug:<66} ║")
    lines.append(f"║  Target:  {topology.target_branch:<66} ║")
    lines.append("║" + " " * 78 + "║")

    for entry in topology.entries:
        marker = "→" if entry.wp_id == current_wp_id else " "
        base_label = entry.base_wp if entry.base_wp else topology.target_branch
        branch_label = entry.branch_name or "(not created)"
        status = entry.lane

        line_text = f"{marker} {entry.wp_id} [{status}] base={base_label} branch={branch_label}"
        if entry.worktree_exists and entry.commits_ahead_of_base > 0:
            line_text += f" (+{entry.commits_ahead_of_base})"

        # Pad to fit box
        padded = line_text[:76].ljust(76)
        lines.append(f"║  {padded}║")

    lines.append("╚" + "═" * 78 + "╝")
    return lines


def x_render_topology_text__mutmut_4(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as human-readable text for CLI output.

    Utility function for human-facing displays (not used in prompts).

    Args:
        topology: Feature topology data
        current_wp_id: The WP to highlight

    Returns:
        List of lines for console output
    """
    lines = []
    lines.append("╔" - "═" * 78 + "╗")
    lines.append("║  WORKTREE TOPOLOGY" + " " * 59 + "║")
    lines.append("╠" + "═" * 78 + "╣")
    lines.append(f"║  Feature: {topology.feature_slug:<66} ║")
    lines.append(f"║  Target:  {topology.target_branch:<66} ║")
    lines.append("║" + " " * 78 + "║")

    for entry in topology.entries:
        marker = "→" if entry.wp_id == current_wp_id else " "
        base_label = entry.base_wp if entry.base_wp else topology.target_branch
        branch_label = entry.branch_name or "(not created)"
        status = entry.lane

        line_text = f"{marker} {entry.wp_id} [{status}] base={base_label} branch={branch_label}"
        if entry.worktree_exists and entry.commits_ahead_of_base > 0:
            line_text += f" (+{entry.commits_ahead_of_base})"

        # Pad to fit box
        padded = line_text[:76].ljust(76)
        lines.append(f"║  {padded}║")

    lines.append("╚" + "═" * 78 + "╝")
    return lines


def x_render_topology_text__mutmut_5(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as human-readable text for CLI output.

    Utility function for human-facing displays (not used in prompts).

    Args:
        topology: Feature topology data
        current_wp_id: The WP to highlight

    Returns:
        List of lines for console output
    """
    lines = []
    lines.append("XX╔XX" + "═" * 78 + "╗")
    lines.append("║  WORKTREE TOPOLOGY" + " " * 59 + "║")
    lines.append("╠" + "═" * 78 + "╣")
    lines.append(f"║  Feature: {topology.feature_slug:<66} ║")
    lines.append(f"║  Target:  {topology.target_branch:<66} ║")
    lines.append("║" + " " * 78 + "║")

    for entry in topology.entries:
        marker = "→" if entry.wp_id == current_wp_id else " "
        base_label = entry.base_wp if entry.base_wp else topology.target_branch
        branch_label = entry.branch_name or "(not created)"
        status = entry.lane

        line_text = f"{marker} {entry.wp_id} [{status}] base={base_label} branch={branch_label}"
        if entry.worktree_exists and entry.commits_ahead_of_base > 0:
            line_text += f" (+{entry.commits_ahead_of_base})"

        # Pad to fit box
        padded = line_text[:76].ljust(76)
        lines.append(f"║  {padded}║")

    lines.append("╚" + "═" * 78 + "╝")
    return lines


def x_render_topology_text__mutmut_6(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as human-readable text for CLI output.

    Utility function for human-facing displays (not used in prompts).

    Args:
        topology: Feature topology data
        current_wp_id: The WP to highlight

    Returns:
        List of lines for console output
    """
    lines = []
    lines.append("╔" + "═" / 78 + "╗")
    lines.append("║  WORKTREE TOPOLOGY" + " " * 59 + "║")
    lines.append("╠" + "═" * 78 + "╣")
    lines.append(f"║  Feature: {topology.feature_slug:<66} ║")
    lines.append(f"║  Target:  {topology.target_branch:<66} ║")
    lines.append("║" + " " * 78 + "║")

    for entry in topology.entries:
        marker = "→" if entry.wp_id == current_wp_id else " "
        base_label = entry.base_wp if entry.base_wp else topology.target_branch
        branch_label = entry.branch_name or "(not created)"
        status = entry.lane

        line_text = f"{marker} {entry.wp_id} [{status}] base={base_label} branch={branch_label}"
        if entry.worktree_exists and entry.commits_ahead_of_base > 0:
            line_text += f" (+{entry.commits_ahead_of_base})"

        # Pad to fit box
        padded = line_text[:76].ljust(76)
        lines.append(f"║  {padded}║")

    lines.append("╚" + "═" * 78 + "╝")
    return lines


def x_render_topology_text__mutmut_7(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as human-readable text for CLI output.

    Utility function for human-facing displays (not used in prompts).

    Args:
        topology: Feature topology data
        current_wp_id: The WP to highlight

    Returns:
        List of lines for console output
    """
    lines = []
    lines.append("╔" + "XX═XX" * 78 + "╗")
    lines.append("║  WORKTREE TOPOLOGY" + " " * 59 + "║")
    lines.append("╠" + "═" * 78 + "╣")
    lines.append(f"║  Feature: {topology.feature_slug:<66} ║")
    lines.append(f"║  Target:  {topology.target_branch:<66} ║")
    lines.append("║" + " " * 78 + "║")

    for entry in topology.entries:
        marker = "→" if entry.wp_id == current_wp_id else " "
        base_label = entry.base_wp if entry.base_wp else topology.target_branch
        branch_label = entry.branch_name or "(not created)"
        status = entry.lane

        line_text = f"{marker} {entry.wp_id} [{status}] base={base_label} branch={branch_label}"
        if entry.worktree_exists and entry.commits_ahead_of_base > 0:
            line_text += f" (+{entry.commits_ahead_of_base})"

        # Pad to fit box
        padded = line_text[:76].ljust(76)
        lines.append(f"║  {padded}║")

    lines.append("╚" + "═" * 78 + "╝")
    return lines


def x_render_topology_text__mutmut_8(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as human-readable text for CLI output.

    Utility function for human-facing displays (not used in prompts).

    Args:
        topology: Feature topology data
        current_wp_id: The WP to highlight

    Returns:
        List of lines for console output
    """
    lines = []
    lines.append("╔" + "═" * 79 + "╗")
    lines.append("║  WORKTREE TOPOLOGY" + " " * 59 + "║")
    lines.append("╠" + "═" * 78 + "╣")
    lines.append(f"║  Feature: {topology.feature_slug:<66} ║")
    lines.append(f"║  Target:  {topology.target_branch:<66} ║")
    lines.append("║" + " " * 78 + "║")

    for entry in topology.entries:
        marker = "→" if entry.wp_id == current_wp_id else " "
        base_label = entry.base_wp if entry.base_wp else topology.target_branch
        branch_label = entry.branch_name or "(not created)"
        status = entry.lane

        line_text = f"{marker} {entry.wp_id} [{status}] base={base_label} branch={branch_label}"
        if entry.worktree_exists and entry.commits_ahead_of_base > 0:
            line_text += f" (+{entry.commits_ahead_of_base})"

        # Pad to fit box
        padded = line_text[:76].ljust(76)
        lines.append(f"║  {padded}║")

    lines.append("╚" + "═" * 78 + "╝")
    return lines


def x_render_topology_text__mutmut_9(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as human-readable text for CLI output.

    Utility function for human-facing displays (not used in prompts).

    Args:
        topology: Feature topology data
        current_wp_id: The WP to highlight

    Returns:
        List of lines for console output
    """
    lines = []
    lines.append("╔" + "═" * 78 + "XX╗XX")
    lines.append("║  WORKTREE TOPOLOGY" + " " * 59 + "║")
    lines.append("╠" + "═" * 78 + "╣")
    lines.append(f"║  Feature: {topology.feature_slug:<66} ║")
    lines.append(f"║  Target:  {topology.target_branch:<66} ║")
    lines.append("║" + " " * 78 + "║")

    for entry in topology.entries:
        marker = "→" if entry.wp_id == current_wp_id else " "
        base_label = entry.base_wp if entry.base_wp else topology.target_branch
        branch_label = entry.branch_name or "(not created)"
        status = entry.lane

        line_text = f"{marker} {entry.wp_id} [{status}] base={base_label} branch={branch_label}"
        if entry.worktree_exists and entry.commits_ahead_of_base > 0:
            line_text += f" (+{entry.commits_ahead_of_base})"

        # Pad to fit box
        padded = line_text[:76].ljust(76)
        lines.append(f"║  {padded}║")

    lines.append("╚" + "═" * 78 + "╝")
    return lines


def x_render_topology_text__mutmut_10(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as human-readable text for CLI output.

    Utility function for human-facing displays (not used in prompts).

    Args:
        topology: Feature topology data
        current_wp_id: The WP to highlight

    Returns:
        List of lines for console output
    """
    lines = []
    lines.append("╔" + "═" * 78 + "╗")
    lines.append(None)
    lines.append("╠" + "═" * 78 + "╣")
    lines.append(f"║  Feature: {topology.feature_slug:<66} ║")
    lines.append(f"║  Target:  {topology.target_branch:<66} ║")
    lines.append("║" + " " * 78 + "║")

    for entry in topology.entries:
        marker = "→" if entry.wp_id == current_wp_id else " "
        base_label = entry.base_wp if entry.base_wp else topology.target_branch
        branch_label = entry.branch_name or "(not created)"
        status = entry.lane

        line_text = f"{marker} {entry.wp_id} [{status}] base={base_label} branch={branch_label}"
        if entry.worktree_exists and entry.commits_ahead_of_base > 0:
            line_text += f" (+{entry.commits_ahead_of_base})"

        # Pad to fit box
        padded = line_text[:76].ljust(76)
        lines.append(f"║  {padded}║")

    lines.append("╚" + "═" * 78 + "╝")
    return lines


def x_render_topology_text__mutmut_11(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as human-readable text for CLI output.

    Utility function for human-facing displays (not used in prompts).

    Args:
        topology: Feature topology data
        current_wp_id: The WP to highlight

    Returns:
        List of lines for console output
    """
    lines = []
    lines.append("╔" + "═" * 78 + "╗")
    lines.append("║  WORKTREE TOPOLOGY" + " " * 59 - "║")
    lines.append("╠" + "═" * 78 + "╣")
    lines.append(f"║  Feature: {topology.feature_slug:<66} ║")
    lines.append(f"║  Target:  {topology.target_branch:<66} ║")
    lines.append("║" + " " * 78 + "║")

    for entry in topology.entries:
        marker = "→" if entry.wp_id == current_wp_id else " "
        base_label = entry.base_wp if entry.base_wp else topology.target_branch
        branch_label = entry.branch_name or "(not created)"
        status = entry.lane

        line_text = f"{marker} {entry.wp_id} [{status}] base={base_label} branch={branch_label}"
        if entry.worktree_exists and entry.commits_ahead_of_base > 0:
            line_text += f" (+{entry.commits_ahead_of_base})"

        # Pad to fit box
        padded = line_text[:76].ljust(76)
        lines.append(f"║  {padded}║")

    lines.append("╚" + "═" * 78 + "╝")
    return lines


def x_render_topology_text__mutmut_12(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as human-readable text for CLI output.

    Utility function for human-facing displays (not used in prompts).

    Args:
        topology: Feature topology data
        current_wp_id: The WP to highlight

    Returns:
        List of lines for console output
    """
    lines = []
    lines.append("╔" + "═" * 78 + "╗")
    lines.append("║  WORKTREE TOPOLOGY" - " " * 59 + "║")
    lines.append("╠" + "═" * 78 + "╣")
    lines.append(f"║  Feature: {topology.feature_slug:<66} ║")
    lines.append(f"║  Target:  {topology.target_branch:<66} ║")
    lines.append("║" + " " * 78 + "║")

    for entry in topology.entries:
        marker = "→" if entry.wp_id == current_wp_id else " "
        base_label = entry.base_wp if entry.base_wp else topology.target_branch
        branch_label = entry.branch_name or "(not created)"
        status = entry.lane

        line_text = f"{marker} {entry.wp_id} [{status}] base={base_label} branch={branch_label}"
        if entry.worktree_exists and entry.commits_ahead_of_base > 0:
            line_text += f" (+{entry.commits_ahead_of_base})"

        # Pad to fit box
        padded = line_text[:76].ljust(76)
        lines.append(f"║  {padded}║")

    lines.append("╚" + "═" * 78 + "╝")
    return lines


def x_render_topology_text__mutmut_13(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as human-readable text for CLI output.

    Utility function for human-facing displays (not used in prompts).

    Args:
        topology: Feature topology data
        current_wp_id: The WP to highlight

    Returns:
        List of lines for console output
    """
    lines = []
    lines.append("╔" + "═" * 78 + "╗")
    lines.append("XX║  WORKTREE TOPOLOGYXX" + " " * 59 + "║")
    lines.append("╠" + "═" * 78 + "╣")
    lines.append(f"║  Feature: {topology.feature_slug:<66} ║")
    lines.append(f"║  Target:  {topology.target_branch:<66} ║")
    lines.append("║" + " " * 78 + "║")

    for entry in topology.entries:
        marker = "→" if entry.wp_id == current_wp_id else " "
        base_label = entry.base_wp if entry.base_wp else topology.target_branch
        branch_label = entry.branch_name or "(not created)"
        status = entry.lane

        line_text = f"{marker} {entry.wp_id} [{status}] base={base_label} branch={branch_label}"
        if entry.worktree_exists and entry.commits_ahead_of_base > 0:
            line_text += f" (+{entry.commits_ahead_of_base})"

        # Pad to fit box
        padded = line_text[:76].ljust(76)
        lines.append(f"║  {padded}║")

    lines.append("╚" + "═" * 78 + "╝")
    return lines


def x_render_topology_text__mutmut_14(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as human-readable text for CLI output.

    Utility function for human-facing displays (not used in prompts).

    Args:
        topology: Feature topology data
        current_wp_id: The WP to highlight

    Returns:
        List of lines for console output
    """
    lines = []
    lines.append("╔" + "═" * 78 + "╗")
    lines.append("║  worktree topology" + " " * 59 + "║")
    lines.append("╠" + "═" * 78 + "╣")
    lines.append(f"║  Feature: {topology.feature_slug:<66} ║")
    lines.append(f"║  Target:  {topology.target_branch:<66} ║")
    lines.append("║" + " " * 78 + "║")

    for entry in topology.entries:
        marker = "→" if entry.wp_id == current_wp_id else " "
        base_label = entry.base_wp if entry.base_wp else topology.target_branch
        branch_label = entry.branch_name or "(not created)"
        status = entry.lane

        line_text = f"{marker} {entry.wp_id} [{status}] base={base_label} branch={branch_label}"
        if entry.worktree_exists and entry.commits_ahead_of_base > 0:
            line_text += f" (+{entry.commits_ahead_of_base})"

        # Pad to fit box
        padded = line_text[:76].ljust(76)
        lines.append(f"║  {padded}║")

    lines.append("╚" + "═" * 78 + "╝")
    return lines


def x_render_topology_text__mutmut_15(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as human-readable text for CLI output.

    Utility function for human-facing displays (not used in prompts).

    Args:
        topology: Feature topology data
        current_wp_id: The WP to highlight

    Returns:
        List of lines for console output
    """
    lines = []
    lines.append("╔" + "═" * 78 + "╗")
    lines.append("║  WORKTREE TOPOLOGY" + " " / 59 + "║")
    lines.append("╠" + "═" * 78 + "╣")
    lines.append(f"║  Feature: {topology.feature_slug:<66} ║")
    lines.append(f"║  Target:  {topology.target_branch:<66} ║")
    lines.append("║" + " " * 78 + "║")

    for entry in topology.entries:
        marker = "→" if entry.wp_id == current_wp_id else " "
        base_label = entry.base_wp if entry.base_wp else topology.target_branch
        branch_label = entry.branch_name or "(not created)"
        status = entry.lane

        line_text = f"{marker} {entry.wp_id} [{status}] base={base_label} branch={branch_label}"
        if entry.worktree_exists and entry.commits_ahead_of_base > 0:
            line_text += f" (+{entry.commits_ahead_of_base})"

        # Pad to fit box
        padded = line_text[:76].ljust(76)
        lines.append(f"║  {padded}║")

    lines.append("╚" + "═" * 78 + "╝")
    return lines


def x_render_topology_text__mutmut_16(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as human-readable text for CLI output.

    Utility function for human-facing displays (not used in prompts).

    Args:
        topology: Feature topology data
        current_wp_id: The WP to highlight

    Returns:
        List of lines for console output
    """
    lines = []
    lines.append("╔" + "═" * 78 + "╗")
    lines.append("║  WORKTREE TOPOLOGY" + "XX XX" * 59 + "║")
    lines.append("╠" + "═" * 78 + "╣")
    lines.append(f"║  Feature: {topology.feature_slug:<66} ║")
    lines.append(f"║  Target:  {topology.target_branch:<66} ║")
    lines.append("║" + " " * 78 + "║")

    for entry in topology.entries:
        marker = "→" if entry.wp_id == current_wp_id else " "
        base_label = entry.base_wp if entry.base_wp else topology.target_branch
        branch_label = entry.branch_name or "(not created)"
        status = entry.lane

        line_text = f"{marker} {entry.wp_id} [{status}] base={base_label} branch={branch_label}"
        if entry.worktree_exists and entry.commits_ahead_of_base > 0:
            line_text += f" (+{entry.commits_ahead_of_base})"

        # Pad to fit box
        padded = line_text[:76].ljust(76)
        lines.append(f"║  {padded}║")

    lines.append("╚" + "═" * 78 + "╝")
    return lines


def x_render_topology_text__mutmut_17(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as human-readable text for CLI output.

    Utility function for human-facing displays (not used in prompts).

    Args:
        topology: Feature topology data
        current_wp_id: The WP to highlight

    Returns:
        List of lines for console output
    """
    lines = []
    lines.append("╔" + "═" * 78 + "╗")
    lines.append("║  WORKTREE TOPOLOGY" + " " * 60 + "║")
    lines.append("╠" + "═" * 78 + "╣")
    lines.append(f"║  Feature: {topology.feature_slug:<66} ║")
    lines.append(f"║  Target:  {topology.target_branch:<66} ║")
    lines.append("║" + " " * 78 + "║")

    for entry in topology.entries:
        marker = "→" if entry.wp_id == current_wp_id else " "
        base_label = entry.base_wp if entry.base_wp else topology.target_branch
        branch_label = entry.branch_name or "(not created)"
        status = entry.lane

        line_text = f"{marker} {entry.wp_id} [{status}] base={base_label} branch={branch_label}"
        if entry.worktree_exists and entry.commits_ahead_of_base > 0:
            line_text += f" (+{entry.commits_ahead_of_base})"

        # Pad to fit box
        padded = line_text[:76].ljust(76)
        lines.append(f"║  {padded}║")

    lines.append("╚" + "═" * 78 + "╝")
    return lines


def x_render_topology_text__mutmut_18(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as human-readable text for CLI output.

    Utility function for human-facing displays (not used in prompts).

    Args:
        topology: Feature topology data
        current_wp_id: The WP to highlight

    Returns:
        List of lines for console output
    """
    lines = []
    lines.append("╔" + "═" * 78 + "╗")
    lines.append("║  WORKTREE TOPOLOGY" + " " * 59 + "XX║XX")
    lines.append("╠" + "═" * 78 + "╣")
    lines.append(f"║  Feature: {topology.feature_slug:<66} ║")
    lines.append(f"║  Target:  {topology.target_branch:<66} ║")
    lines.append("║" + " " * 78 + "║")

    for entry in topology.entries:
        marker = "→" if entry.wp_id == current_wp_id else " "
        base_label = entry.base_wp if entry.base_wp else topology.target_branch
        branch_label = entry.branch_name or "(not created)"
        status = entry.lane

        line_text = f"{marker} {entry.wp_id} [{status}] base={base_label} branch={branch_label}"
        if entry.worktree_exists and entry.commits_ahead_of_base > 0:
            line_text += f" (+{entry.commits_ahead_of_base})"

        # Pad to fit box
        padded = line_text[:76].ljust(76)
        lines.append(f"║  {padded}║")

    lines.append("╚" + "═" * 78 + "╝")
    return lines


def x_render_topology_text__mutmut_19(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as human-readable text for CLI output.

    Utility function for human-facing displays (not used in prompts).

    Args:
        topology: Feature topology data
        current_wp_id: The WP to highlight

    Returns:
        List of lines for console output
    """
    lines = []
    lines.append("╔" + "═" * 78 + "╗")
    lines.append("║  WORKTREE TOPOLOGY" + " " * 59 + "║")
    lines.append(None)
    lines.append(f"║  Feature: {topology.feature_slug:<66} ║")
    lines.append(f"║  Target:  {topology.target_branch:<66} ║")
    lines.append("║" + " " * 78 + "║")

    for entry in topology.entries:
        marker = "→" if entry.wp_id == current_wp_id else " "
        base_label = entry.base_wp if entry.base_wp else topology.target_branch
        branch_label = entry.branch_name or "(not created)"
        status = entry.lane

        line_text = f"{marker} {entry.wp_id} [{status}] base={base_label} branch={branch_label}"
        if entry.worktree_exists and entry.commits_ahead_of_base > 0:
            line_text += f" (+{entry.commits_ahead_of_base})"

        # Pad to fit box
        padded = line_text[:76].ljust(76)
        lines.append(f"║  {padded}║")

    lines.append("╚" + "═" * 78 + "╝")
    return lines


def x_render_topology_text__mutmut_20(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as human-readable text for CLI output.

    Utility function for human-facing displays (not used in prompts).

    Args:
        topology: Feature topology data
        current_wp_id: The WP to highlight

    Returns:
        List of lines for console output
    """
    lines = []
    lines.append("╔" + "═" * 78 + "╗")
    lines.append("║  WORKTREE TOPOLOGY" + " " * 59 + "║")
    lines.append("╠" + "═" * 78 - "╣")
    lines.append(f"║  Feature: {topology.feature_slug:<66} ║")
    lines.append(f"║  Target:  {topology.target_branch:<66} ║")
    lines.append("║" + " " * 78 + "║")

    for entry in topology.entries:
        marker = "→" if entry.wp_id == current_wp_id else " "
        base_label = entry.base_wp if entry.base_wp else topology.target_branch
        branch_label = entry.branch_name or "(not created)"
        status = entry.lane

        line_text = f"{marker} {entry.wp_id} [{status}] base={base_label} branch={branch_label}"
        if entry.worktree_exists and entry.commits_ahead_of_base > 0:
            line_text += f" (+{entry.commits_ahead_of_base})"

        # Pad to fit box
        padded = line_text[:76].ljust(76)
        lines.append(f"║  {padded}║")

    lines.append("╚" + "═" * 78 + "╝")
    return lines


def x_render_topology_text__mutmut_21(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as human-readable text for CLI output.

    Utility function for human-facing displays (not used in prompts).

    Args:
        topology: Feature topology data
        current_wp_id: The WP to highlight

    Returns:
        List of lines for console output
    """
    lines = []
    lines.append("╔" + "═" * 78 + "╗")
    lines.append("║  WORKTREE TOPOLOGY" + " " * 59 + "║")
    lines.append("╠" - "═" * 78 + "╣")
    lines.append(f"║  Feature: {topology.feature_slug:<66} ║")
    lines.append(f"║  Target:  {topology.target_branch:<66} ║")
    lines.append("║" + " " * 78 + "║")

    for entry in topology.entries:
        marker = "→" if entry.wp_id == current_wp_id else " "
        base_label = entry.base_wp if entry.base_wp else topology.target_branch
        branch_label = entry.branch_name or "(not created)"
        status = entry.lane

        line_text = f"{marker} {entry.wp_id} [{status}] base={base_label} branch={branch_label}"
        if entry.worktree_exists and entry.commits_ahead_of_base > 0:
            line_text += f" (+{entry.commits_ahead_of_base})"

        # Pad to fit box
        padded = line_text[:76].ljust(76)
        lines.append(f"║  {padded}║")

    lines.append("╚" + "═" * 78 + "╝")
    return lines


def x_render_topology_text__mutmut_22(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as human-readable text for CLI output.

    Utility function for human-facing displays (not used in prompts).

    Args:
        topology: Feature topology data
        current_wp_id: The WP to highlight

    Returns:
        List of lines for console output
    """
    lines = []
    lines.append("╔" + "═" * 78 + "╗")
    lines.append("║  WORKTREE TOPOLOGY" + " " * 59 + "║")
    lines.append("XX╠XX" + "═" * 78 + "╣")
    lines.append(f"║  Feature: {topology.feature_slug:<66} ║")
    lines.append(f"║  Target:  {topology.target_branch:<66} ║")
    lines.append("║" + " " * 78 + "║")

    for entry in topology.entries:
        marker = "→" if entry.wp_id == current_wp_id else " "
        base_label = entry.base_wp if entry.base_wp else topology.target_branch
        branch_label = entry.branch_name or "(not created)"
        status = entry.lane

        line_text = f"{marker} {entry.wp_id} [{status}] base={base_label} branch={branch_label}"
        if entry.worktree_exists and entry.commits_ahead_of_base > 0:
            line_text += f" (+{entry.commits_ahead_of_base})"

        # Pad to fit box
        padded = line_text[:76].ljust(76)
        lines.append(f"║  {padded}║")

    lines.append("╚" + "═" * 78 + "╝")
    return lines


def x_render_topology_text__mutmut_23(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as human-readable text for CLI output.

    Utility function for human-facing displays (not used in prompts).

    Args:
        topology: Feature topology data
        current_wp_id: The WP to highlight

    Returns:
        List of lines for console output
    """
    lines = []
    lines.append("╔" + "═" * 78 + "╗")
    lines.append("║  WORKTREE TOPOLOGY" + " " * 59 + "║")
    lines.append("╠" + "═" / 78 + "╣")
    lines.append(f"║  Feature: {topology.feature_slug:<66} ║")
    lines.append(f"║  Target:  {topology.target_branch:<66} ║")
    lines.append("║" + " " * 78 + "║")

    for entry in topology.entries:
        marker = "→" if entry.wp_id == current_wp_id else " "
        base_label = entry.base_wp if entry.base_wp else topology.target_branch
        branch_label = entry.branch_name or "(not created)"
        status = entry.lane

        line_text = f"{marker} {entry.wp_id} [{status}] base={base_label} branch={branch_label}"
        if entry.worktree_exists and entry.commits_ahead_of_base > 0:
            line_text += f" (+{entry.commits_ahead_of_base})"

        # Pad to fit box
        padded = line_text[:76].ljust(76)
        lines.append(f"║  {padded}║")

    lines.append("╚" + "═" * 78 + "╝")
    return lines


def x_render_topology_text__mutmut_24(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as human-readable text for CLI output.

    Utility function for human-facing displays (not used in prompts).

    Args:
        topology: Feature topology data
        current_wp_id: The WP to highlight

    Returns:
        List of lines for console output
    """
    lines = []
    lines.append("╔" + "═" * 78 + "╗")
    lines.append("║  WORKTREE TOPOLOGY" + " " * 59 + "║")
    lines.append("╠" + "XX═XX" * 78 + "╣")
    lines.append(f"║  Feature: {topology.feature_slug:<66} ║")
    lines.append(f"║  Target:  {topology.target_branch:<66} ║")
    lines.append("║" + " " * 78 + "║")

    for entry in topology.entries:
        marker = "→" if entry.wp_id == current_wp_id else " "
        base_label = entry.base_wp if entry.base_wp else topology.target_branch
        branch_label = entry.branch_name or "(not created)"
        status = entry.lane

        line_text = f"{marker} {entry.wp_id} [{status}] base={base_label} branch={branch_label}"
        if entry.worktree_exists and entry.commits_ahead_of_base > 0:
            line_text += f" (+{entry.commits_ahead_of_base})"

        # Pad to fit box
        padded = line_text[:76].ljust(76)
        lines.append(f"║  {padded}║")

    lines.append("╚" + "═" * 78 + "╝")
    return lines


def x_render_topology_text__mutmut_25(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as human-readable text for CLI output.

    Utility function for human-facing displays (not used in prompts).

    Args:
        topology: Feature topology data
        current_wp_id: The WP to highlight

    Returns:
        List of lines for console output
    """
    lines = []
    lines.append("╔" + "═" * 78 + "╗")
    lines.append("║  WORKTREE TOPOLOGY" + " " * 59 + "║")
    lines.append("╠" + "═" * 79 + "╣")
    lines.append(f"║  Feature: {topology.feature_slug:<66} ║")
    lines.append(f"║  Target:  {topology.target_branch:<66} ║")
    lines.append("║" + " " * 78 + "║")

    for entry in topology.entries:
        marker = "→" if entry.wp_id == current_wp_id else " "
        base_label = entry.base_wp if entry.base_wp else topology.target_branch
        branch_label = entry.branch_name or "(not created)"
        status = entry.lane

        line_text = f"{marker} {entry.wp_id} [{status}] base={base_label} branch={branch_label}"
        if entry.worktree_exists and entry.commits_ahead_of_base > 0:
            line_text += f" (+{entry.commits_ahead_of_base})"

        # Pad to fit box
        padded = line_text[:76].ljust(76)
        lines.append(f"║  {padded}║")

    lines.append("╚" + "═" * 78 + "╝")
    return lines


def x_render_topology_text__mutmut_26(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as human-readable text for CLI output.

    Utility function for human-facing displays (not used in prompts).

    Args:
        topology: Feature topology data
        current_wp_id: The WP to highlight

    Returns:
        List of lines for console output
    """
    lines = []
    lines.append("╔" + "═" * 78 + "╗")
    lines.append("║  WORKTREE TOPOLOGY" + " " * 59 + "║")
    lines.append("╠" + "═" * 78 + "XX╣XX")
    lines.append(f"║  Feature: {topology.feature_slug:<66} ║")
    lines.append(f"║  Target:  {topology.target_branch:<66} ║")
    lines.append("║" + " " * 78 + "║")

    for entry in topology.entries:
        marker = "→" if entry.wp_id == current_wp_id else " "
        base_label = entry.base_wp if entry.base_wp else topology.target_branch
        branch_label = entry.branch_name or "(not created)"
        status = entry.lane

        line_text = f"{marker} {entry.wp_id} [{status}] base={base_label} branch={branch_label}"
        if entry.worktree_exists and entry.commits_ahead_of_base > 0:
            line_text += f" (+{entry.commits_ahead_of_base})"

        # Pad to fit box
        padded = line_text[:76].ljust(76)
        lines.append(f"║  {padded}║")

    lines.append("╚" + "═" * 78 + "╝")
    return lines


def x_render_topology_text__mutmut_27(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as human-readable text for CLI output.

    Utility function for human-facing displays (not used in prompts).

    Args:
        topology: Feature topology data
        current_wp_id: The WP to highlight

    Returns:
        List of lines for console output
    """
    lines = []
    lines.append("╔" + "═" * 78 + "╗")
    lines.append("║  WORKTREE TOPOLOGY" + " " * 59 + "║")
    lines.append("╠" + "═" * 78 + "╣")
    lines.append(None)
    lines.append(f"║  Target:  {topology.target_branch:<66} ║")
    lines.append("║" + " " * 78 + "║")

    for entry in topology.entries:
        marker = "→" if entry.wp_id == current_wp_id else " "
        base_label = entry.base_wp if entry.base_wp else topology.target_branch
        branch_label = entry.branch_name or "(not created)"
        status = entry.lane

        line_text = f"{marker} {entry.wp_id} [{status}] base={base_label} branch={branch_label}"
        if entry.worktree_exists and entry.commits_ahead_of_base > 0:
            line_text += f" (+{entry.commits_ahead_of_base})"

        # Pad to fit box
        padded = line_text[:76].ljust(76)
        lines.append(f"║  {padded}║")

    lines.append("╚" + "═" * 78 + "╝")
    return lines


def x_render_topology_text__mutmut_28(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as human-readable text for CLI output.

    Utility function for human-facing displays (not used in prompts).

    Args:
        topology: Feature topology data
        current_wp_id: The WP to highlight

    Returns:
        List of lines for console output
    """
    lines = []
    lines.append("╔" + "═" * 78 + "╗")
    lines.append("║  WORKTREE TOPOLOGY" + " " * 59 + "║")
    lines.append("╠" + "═" * 78 + "╣")
    lines.append(f"║  Feature: {topology.feature_slug:<66} ║")
    lines.append(None)
    lines.append("║" + " " * 78 + "║")

    for entry in topology.entries:
        marker = "→" if entry.wp_id == current_wp_id else " "
        base_label = entry.base_wp if entry.base_wp else topology.target_branch
        branch_label = entry.branch_name or "(not created)"
        status = entry.lane

        line_text = f"{marker} {entry.wp_id} [{status}] base={base_label} branch={branch_label}"
        if entry.worktree_exists and entry.commits_ahead_of_base > 0:
            line_text += f" (+{entry.commits_ahead_of_base})"

        # Pad to fit box
        padded = line_text[:76].ljust(76)
        lines.append(f"║  {padded}║")

    lines.append("╚" + "═" * 78 + "╝")
    return lines


def x_render_topology_text__mutmut_29(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as human-readable text for CLI output.

    Utility function for human-facing displays (not used in prompts).

    Args:
        topology: Feature topology data
        current_wp_id: The WP to highlight

    Returns:
        List of lines for console output
    """
    lines = []
    lines.append("╔" + "═" * 78 + "╗")
    lines.append("║  WORKTREE TOPOLOGY" + " " * 59 + "║")
    lines.append("╠" + "═" * 78 + "╣")
    lines.append(f"║  Feature: {topology.feature_slug:<66} ║")
    lines.append(f"║  Target:  {topology.target_branch:<66} ║")
    lines.append(None)

    for entry in topology.entries:
        marker = "→" if entry.wp_id == current_wp_id else " "
        base_label = entry.base_wp if entry.base_wp else topology.target_branch
        branch_label = entry.branch_name or "(not created)"
        status = entry.lane

        line_text = f"{marker} {entry.wp_id} [{status}] base={base_label} branch={branch_label}"
        if entry.worktree_exists and entry.commits_ahead_of_base > 0:
            line_text += f" (+{entry.commits_ahead_of_base})"

        # Pad to fit box
        padded = line_text[:76].ljust(76)
        lines.append(f"║  {padded}║")

    lines.append("╚" + "═" * 78 + "╝")
    return lines


def x_render_topology_text__mutmut_30(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as human-readable text for CLI output.

    Utility function for human-facing displays (not used in prompts).

    Args:
        topology: Feature topology data
        current_wp_id: The WP to highlight

    Returns:
        List of lines for console output
    """
    lines = []
    lines.append("╔" + "═" * 78 + "╗")
    lines.append("║  WORKTREE TOPOLOGY" + " " * 59 + "║")
    lines.append("╠" + "═" * 78 + "╣")
    lines.append(f"║  Feature: {topology.feature_slug:<66} ║")
    lines.append(f"║  Target:  {topology.target_branch:<66} ║")
    lines.append("║" + " " * 78 - "║")

    for entry in topology.entries:
        marker = "→" if entry.wp_id == current_wp_id else " "
        base_label = entry.base_wp if entry.base_wp else topology.target_branch
        branch_label = entry.branch_name or "(not created)"
        status = entry.lane

        line_text = f"{marker} {entry.wp_id} [{status}] base={base_label} branch={branch_label}"
        if entry.worktree_exists and entry.commits_ahead_of_base > 0:
            line_text += f" (+{entry.commits_ahead_of_base})"

        # Pad to fit box
        padded = line_text[:76].ljust(76)
        lines.append(f"║  {padded}║")

    lines.append("╚" + "═" * 78 + "╝")
    return lines


def x_render_topology_text__mutmut_31(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as human-readable text for CLI output.

    Utility function for human-facing displays (not used in prompts).

    Args:
        topology: Feature topology data
        current_wp_id: The WP to highlight

    Returns:
        List of lines for console output
    """
    lines = []
    lines.append("╔" + "═" * 78 + "╗")
    lines.append("║  WORKTREE TOPOLOGY" + " " * 59 + "║")
    lines.append("╠" + "═" * 78 + "╣")
    lines.append(f"║  Feature: {topology.feature_slug:<66} ║")
    lines.append(f"║  Target:  {topology.target_branch:<66} ║")
    lines.append("║" - " " * 78 + "║")

    for entry in topology.entries:
        marker = "→" if entry.wp_id == current_wp_id else " "
        base_label = entry.base_wp if entry.base_wp else topology.target_branch
        branch_label = entry.branch_name or "(not created)"
        status = entry.lane

        line_text = f"{marker} {entry.wp_id} [{status}] base={base_label} branch={branch_label}"
        if entry.worktree_exists and entry.commits_ahead_of_base > 0:
            line_text += f" (+{entry.commits_ahead_of_base})"

        # Pad to fit box
        padded = line_text[:76].ljust(76)
        lines.append(f"║  {padded}║")

    lines.append("╚" + "═" * 78 + "╝")
    return lines


def x_render_topology_text__mutmut_32(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as human-readable text for CLI output.

    Utility function for human-facing displays (not used in prompts).

    Args:
        topology: Feature topology data
        current_wp_id: The WP to highlight

    Returns:
        List of lines for console output
    """
    lines = []
    lines.append("╔" + "═" * 78 + "╗")
    lines.append("║  WORKTREE TOPOLOGY" + " " * 59 + "║")
    lines.append("╠" + "═" * 78 + "╣")
    lines.append(f"║  Feature: {topology.feature_slug:<66} ║")
    lines.append(f"║  Target:  {topology.target_branch:<66} ║")
    lines.append("XX║XX" + " " * 78 + "║")

    for entry in topology.entries:
        marker = "→" if entry.wp_id == current_wp_id else " "
        base_label = entry.base_wp if entry.base_wp else topology.target_branch
        branch_label = entry.branch_name or "(not created)"
        status = entry.lane

        line_text = f"{marker} {entry.wp_id} [{status}] base={base_label} branch={branch_label}"
        if entry.worktree_exists and entry.commits_ahead_of_base > 0:
            line_text += f" (+{entry.commits_ahead_of_base})"

        # Pad to fit box
        padded = line_text[:76].ljust(76)
        lines.append(f"║  {padded}║")

    lines.append("╚" + "═" * 78 + "╝")
    return lines


def x_render_topology_text__mutmut_33(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as human-readable text for CLI output.

    Utility function for human-facing displays (not used in prompts).

    Args:
        topology: Feature topology data
        current_wp_id: The WP to highlight

    Returns:
        List of lines for console output
    """
    lines = []
    lines.append("╔" + "═" * 78 + "╗")
    lines.append("║  WORKTREE TOPOLOGY" + " " * 59 + "║")
    lines.append("╠" + "═" * 78 + "╣")
    lines.append(f"║  Feature: {topology.feature_slug:<66} ║")
    lines.append(f"║  Target:  {topology.target_branch:<66} ║")
    lines.append("║" + " " / 78 + "║")

    for entry in topology.entries:
        marker = "→" if entry.wp_id == current_wp_id else " "
        base_label = entry.base_wp if entry.base_wp else topology.target_branch
        branch_label = entry.branch_name or "(not created)"
        status = entry.lane

        line_text = f"{marker} {entry.wp_id} [{status}] base={base_label} branch={branch_label}"
        if entry.worktree_exists and entry.commits_ahead_of_base > 0:
            line_text += f" (+{entry.commits_ahead_of_base})"

        # Pad to fit box
        padded = line_text[:76].ljust(76)
        lines.append(f"║  {padded}║")

    lines.append("╚" + "═" * 78 + "╝")
    return lines


def x_render_topology_text__mutmut_34(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as human-readable text for CLI output.

    Utility function for human-facing displays (not used in prompts).

    Args:
        topology: Feature topology data
        current_wp_id: The WP to highlight

    Returns:
        List of lines for console output
    """
    lines = []
    lines.append("╔" + "═" * 78 + "╗")
    lines.append("║  WORKTREE TOPOLOGY" + " " * 59 + "║")
    lines.append("╠" + "═" * 78 + "╣")
    lines.append(f"║  Feature: {topology.feature_slug:<66} ║")
    lines.append(f"║  Target:  {topology.target_branch:<66} ║")
    lines.append("║" + "XX XX" * 78 + "║")

    for entry in topology.entries:
        marker = "→" if entry.wp_id == current_wp_id else " "
        base_label = entry.base_wp if entry.base_wp else topology.target_branch
        branch_label = entry.branch_name or "(not created)"
        status = entry.lane

        line_text = f"{marker} {entry.wp_id} [{status}] base={base_label} branch={branch_label}"
        if entry.worktree_exists and entry.commits_ahead_of_base > 0:
            line_text += f" (+{entry.commits_ahead_of_base})"

        # Pad to fit box
        padded = line_text[:76].ljust(76)
        lines.append(f"║  {padded}║")

    lines.append("╚" + "═" * 78 + "╝")
    return lines


def x_render_topology_text__mutmut_35(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as human-readable text for CLI output.

    Utility function for human-facing displays (not used in prompts).

    Args:
        topology: Feature topology data
        current_wp_id: The WP to highlight

    Returns:
        List of lines for console output
    """
    lines = []
    lines.append("╔" + "═" * 78 + "╗")
    lines.append("║  WORKTREE TOPOLOGY" + " " * 59 + "║")
    lines.append("╠" + "═" * 78 + "╣")
    lines.append(f"║  Feature: {topology.feature_slug:<66} ║")
    lines.append(f"║  Target:  {topology.target_branch:<66} ║")
    lines.append("║" + " " * 79 + "║")

    for entry in topology.entries:
        marker = "→" if entry.wp_id == current_wp_id else " "
        base_label = entry.base_wp if entry.base_wp else topology.target_branch
        branch_label = entry.branch_name or "(not created)"
        status = entry.lane

        line_text = f"{marker} {entry.wp_id} [{status}] base={base_label} branch={branch_label}"
        if entry.worktree_exists and entry.commits_ahead_of_base > 0:
            line_text += f" (+{entry.commits_ahead_of_base})"

        # Pad to fit box
        padded = line_text[:76].ljust(76)
        lines.append(f"║  {padded}║")

    lines.append("╚" + "═" * 78 + "╝")
    return lines


def x_render_topology_text__mutmut_36(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as human-readable text for CLI output.

    Utility function for human-facing displays (not used in prompts).

    Args:
        topology: Feature topology data
        current_wp_id: The WP to highlight

    Returns:
        List of lines for console output
    """
    lines = []
    lines.append("╔" + "═" * 78 + "╗")
    lines.append("║  WORKTREE TOPOLOGY" + " " * 59 + "║")
    lines.append("╠" + "═" * 78 + "╣")
    lines.append(f"║  Feature: {topology.feature_slug:<66} ║")
    lines.append(f"║  Target:  {topology.target_branch:<66} ║")
    lines.append("║" + " " * 78 + "XX║XX")

    for entry in topology.entries:
        marker = "→" if entry.wp_id == current_wp_id else " "
        base_label = entry.base_wp if entry.base_wp else topology.target_branch
        branch_label = entry.branch_name or "(not created)"
        status = entry.lane

        line_text = f"{marker} {entry.wp_id} [{status}] base={base_label} branch={branch_label}"
        if entry.worktree_exists and entry.commits_ahead_of_base > 0:
            line_text += f" (+{entry.commits_ahead_of_base})"

        # Pad to fit box
        padded = line_text[:76].ljust(76)
        lines.append(f"║  {padded}║")

    lines.append("╚" + "═" * 78 + "╝")
    return lines


def x_render_topology_text__mutmut_37(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as human-readable text for CLI output.

    Utility function for human-facing displays (not used in prompts).

    Args:
        topology: Feature topology data
        current_wp_id: The WP to highlight

    Returns:
        List of lines for console output
    """
    lines = []
    lines.append("╔" + "═" * 78 + "╗")
    lines.append("║  WORKTREE TOPOLOGY" + " " * 59 + "║")
    lines.append("╠" + "═" * 78 + "╣")
    lines.append(f"║  Feature: {topology.feature_slug:<66} ║")
    lines.append(f"║  Target:  {topology.target_branch:<66} ║")
    lines.append("║" + " " * 78 + "║")

    for entry in topology.entries:
        marker = None
        base_label = entry.base_wp if entry.base_wp else topology.target_branch
        branch_label = entry.branch_name or "(not created)"
        status = entry.lane

        line_text = f"{marker} {entry.wp_id} [{status}] base={base_label} branch={branch_label}"
        if entry.worktree_exists and entry.commits_ahead_of_base > 0:
            line_text += f" (+{entry.commits_ahead_of_base})"

        # Pad to fit box
        padded = line_text[:76].ljust(76)
        lines.append(f"║  {padded}║")

    lines.append("╚" + "═" * 78 + "╝")
    return lines


def x_render_topology_text__mutmut_38(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as human-readable text for CLI output.

    Utility function for human-facing displays (not used in prompts).

    Args:
        topology: Feature topology data
        current_wp_id: The WP to highlight

    Returns:
        List of lines for console output
    """
    lines = []
    lines.append("╔" + "═" * 78 + "╗")
    lines.append("║  WORKTREE TOPOLOGY" + " " * 59 + "║")
    lines.append("╠" + "═" * 78 + "╣")
    lines.append(f"║  Feature: {topology.feature_slug:<66} ║")
    lines.append(f"║  Target:  {topology.target_branch:<66} ║")
    lines.append("║" + " " * 78 + "║")

    for entry in topology.entries:
        marker = "XX→XX" if entry.wp_id == current_wp_id else " "
        base_label = entry.base_wp if entry.base_wp else topology.target_branch
        branch_label = entry.branch_name or "(not created)"
        status = entry.lane

        line_text = f"{marker} {entry.wp_id} [{status}] base={base_label} branch={branch_label}"
        if entry.worktree_exists and entry.commits_ahead_of_base > 0:
            line_text += f" (+{entry.commits_ahead_of_base})"

        # Pad to fit box
        padded = line_text[:76].ljust(76)
        lines.append(f"║  {padded}║")

    lines.append("╚" + "═" * 78 + "╝")
    return lines


def x_render_topology_text__mutmut_39(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as human-readable text for CLI output.

    Utility function for human-facing displays (not used in prompts).

    Args:
        topology: Feature topology data
        current_wp_id: The WP to highlight

    Returns:
        List of lines for console output
    """
    lines = []
    lines.append("╔" + "═" * 78 + "╗")
    lines.append("║  WORKTREE TOPOLOGY" + " " * 59 + "║")
    lines.append("╠" + "═" * 78 + "╣")
    lines.append(f"║  Feature: {topology.feature_slug:<66} ║")
    lines.append(f"║  Target:  {topology.target_branch:<66} ║")
    lines.append("║" + " " * 78 + "║")

    for entry in topology.entries:
        marker = "→" if entry.wp_id != current_wp_id else " "
        base_label = entry.base_wp if entry.base_wp else topology.target_branch
        branch_label = entry.branch_name or "(not created)"
        status = entry.lane

        line_text = f"{marker} {entry.wp_id} [{status}] base={base_label} branch={branch_label}"
        if entry.worktree_exists and entry.commits_ahead_of_base > 0:
            line_text += f" (+{entry.commits_ahead_of_base})"

        # Pad to fit box
        padded = line_text[:76].ljust(76)
        lines.append(f"║  {padded}║")

    lines.append("╚" + "═" * 78 + "╝")
    return lines


def x_render_topology_text__mutmut_40(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as human-readable text for CLI output.

    Utility function for human-facing displays (not used in prompts).

    Args:
        topology: Feature topology data
        current_wp_id: The WP to highlight

    Returns:
        List of lines for console output
    """
    lines = []
    lines.append("╔" + "═" * 78 + "╗")
    lines.append("║  WORKTREE TOPOLOGY" + " " * 59 + "║")
    lines.append("╠" + "═" * 78 + "╣")
    lines.append(f"║  Feature: {topology.feature_slug:<66} ║")
    lines.append(f"║  Target:  {topology.target_branch:<66} ║")
    lines.append("║" + " " * 78 + "║")

    for entry in topology.entries:
        marker = "→" if entry.wp_id == current_wp_id else "XX XX"
        base_label = entry.base_wp if entry.base_wp else topology.target_branch
        branch_label = entry.branch_name or "(not created)"
        status = entry.lane

        line_text = f"{marker} {entry.wp_id} [{status}] base={base_label} branch={branch_label}"
        if entry.worktree_exists and entry.commits_ahead_of_base > 0:
            line_text += f" (+{entry.commits_ahead_of_base})"

        # Pad to fit box
        padded = line_text[:76].ljust(76)
        lines.append(f"║  {padded}║")

    lines.append("╚" + "═" * 78 + "╝")
    return lines


def x_render_topology_text__mutmut_41(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as human-readable text for CLI output.

    Utility function for human-facing displays (not used in prompts).

    Args:
        topology: Feature topology data
        current_wp_id: The WP to highlight

    Returns:
        List of lines for console output
    """
    lines = []
    lines.append("╔" + "═" * 78 + "╗")
    lines.append("║  WORKTREE TOPOLOGY" + " " * 59 + "║")
    lines.append("╠" + "═" * 78 + "╣")
    lines.append(f"║  Feature: {topology.feature_slug:<66} ║")
    lines.append(f"║  Target:  {topology.target_branch:<66} ║")
    lines.append("║" + " " * 78 + "║")

    for entry in topology.entries:
        marker = "→" if entry.wp_id == current_wp_id else " "
        base_label = None
        branch_label = entry.branch_name or "(not created)"
        status = entry.lane

        line_text = f"{marker} {entry.wp_id} [{status}] base={base_label} branch={branch_label}"
        if entry.worktree_exists and entry.commits_ahead_of_base > 0:
            line_text += f" (+{entry.commits_ahead_of_base})"

        # Pad to fit box
        padded = line_text[:76].ljust(76)
        lines.append(f"║  {padded}║")

    lines.append("╚" + "═" * 78 + "╝")
    return lines


def x_render_topology_text__mutmut_42(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as human-readable text for CLI output.

    Utility function for human-facing displays (not used in prompts).

    Args:
        topology: Feature topology data
        current_wp_id: The WP to highlight

    Returns:
        List of lines for console output
    """
    lines = []
    lines.append("╔" + "═" * 78 + "╗")
    lines.append("║  WORKTREE TOPOLOGY" + " " * 59 + "║")
    lines.append("╠" + "═" * 78 + "╣")
    lines.append(f"║  Feature: {topology.feature_slug:<66} ║")
    lines.append(f"║  Target:  {topology.target_branch:<66} ║")
    lines.append("║" + " " * 78 + "║")

    for entry in topology.entries:
        marker = "→" if entry.wp_id == current_wp_id else " "
        base_label = entry.base_wp if entry.base_wp else topology.target_branch
        branch_label = None
        status = entry.lane

        line_text = f"{marker} {entry.wp_id} [{status}] base={base_label} branch={branch_label}"
        if entry.worktree_exists and entry.commits_ahead_of_base > 0:
            line_text += f" (+{entry.commits_ahead_of_base})"

        # Pad to fit box
        padded = line_text[:76].ljust(76)
        lines.append(f"║  {padded}║")

    lines.append("╚" + "═" * 78 + "╝")
    return lines


def x_render_topology_text__mutmut_43(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as human-readable text for CLI output.

    Utility function for human-facing displays (not used in prompts).

    Args:
        topology: Feature topology data
        current_wp_id: The WP to highlight

    Returns:
        List of lines for console output
    """
    lines = []
    lines.append("╔" + "═" * 78 + "╗")
    lines.append("║  WORKTREE TOPOLOGY" + " " * 59 + "║")
    lines.append("╠" + "═" * 78 + "╣")
    lines.append(f"║  Feature: {topology.feature_slug:<66} ║")
    lines.append(f"║  Target:  {topology.target_branch:<66} ║")
    lines.append("║" + " " * 78 + "║")

    for entry in topology.entries:
        marker = "→" if entry.wp_id == current_wp_id else " "
        base_label = entry.base_wp if entry.base_wp else topology.target_branch
        branch_label = entry.branch_name and "(not created)"
        status = entry.lane

        line_text = f"{marker} {entry.wp_id} [{status}] base={base_label} branch={branch_label}"
        if entry.worktree_exists and entry.commits_ahead_of_base > 0:
            line_text += f" (+{entry.commits_ahead_of_base})"

        # Pad to fit box
        padded = line_text[:76].ljust(76)
        lines.append(f"║  {padded}║")

    lines.append("╚" + "═" * 78 + "╝")
    return lines


def x_render_topology_text__mutmut_44(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as human-readable text for CLI output.

    Utility function for human-facing displays (not used in prompts).

    Args:
        topology: Feature topology data
        current_wp_id: The WP to highlight

    Returns:
        List of lines for console output
    """
    lines = []
    lines.append("╔" + "═" * 78 + "╗")
    lines.append("║  WORKTREE TOPOLOGY" + " " * 59 + "║")
    lines.append("╠" + "═" * 78 + "╣")
    lines.append(f"║  Feature: {topology.feature_slug:<66} ║")
    lines.append(f"║  Target:  {topology.target_branch:<66} ║")
    lines.append("║" + " " * 78 + "║")

    for entry in topology.entries:
        marker = "→" if entry.wp_id == current_wp_id else " "
        base_label = entry.base_wp if entry.base_wp else topology.target_branch
        branch_label = entry.branch_name or "XX(not created)XX"
        status = entry.lane

        line_text = f"{marker} {entry.wp_id} [{status}] base={base_label} branch={branch_label}"
        if entry.worktree_exists and entry.commits_ahead_of_base > 0:
            line_text += f" (+{entry.commits_ahead_of_base})"

        # Pad to fit box
        padded = line_text[:76].ljust(76)
        lines.append(f"║  {padded}║")

    lines.append("╚" + "═" * 78 + "╝")
    return lines


def x_render_topology_text__mutmut_45(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as human-readable text for CLI output.

    Utility function for human-facing displays (not used in prompts).

    Args:
        topology: Feature topology data
        current_wp_id: The WP to highlight

    Returns:
        List of lines for console output
    """
    lines = []
    lines.append("╔" + "═" * 78 + "╗")
    lines.append("║  WORKTREE TOPOLOGY" + " " * 59 + "║")
    lines.append("╠" + "═" * 78 + "╣")
    lines.append(f"║  Feature: {topology.feature_slug:<66} ║")
    lines.append(f"║  Target:  {topology.target_branch:<66} ║")
    lines.append("║" + " " * 78 + "║")

    for entry in topology.entries:
        marker = "→" if entry.wp_id == current_wp_id else " "
        base_label = entry.base_wp if entry.base_wp else topology.target_branch
        branch_label = entry.branch_name or "(NOT CREATED)"
        status = entry.lane

        line_text = f"{marker} {entry.wp_id} [{status}] base={base_label} branch={branch_label}"
        if entry.worktree_exists and entry.commits_ahead_of_base > 0:
            line_text += f" (+{entry.commits_ahead_of_base})"

        # Pad to fit box
        padded = line_text[:76].ljust(76)
        lines.append(f"║  {padded}║")

    lines.append("╚" + "═" * 78 + "╝")
    return lines


def x_render_topology_text__mutmut_46(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as human-readable text for CLI output.

    Utility function for human-facing displays (not used in prompts).

    Args:
        topology: Feature topology data
        current_wp_id: The WP to highlight

    Returns:
        List of lines for console output
    """
    lines = []
    lines.append("╔" + "═" * 78 + "╗")
    lines.append("║  WORKTREE TOPOLOGY" + " " * 59 + "║")
    lines.append("╠" + "═" * 78 + "╣")
    lines.append(f"║  Feature: {topology.feature_slug:<66} ║")
    lines.append(f"║  Target:  {topology.target_branch:<66} ║")
    lines.append("║" + " " * 78 + "║")

    for entry in topology.entries:
        marker = "→" if entry.wp_id == current_wp_id else " "
        base_label = entry.base_wp if entry.base_wp else topology.target_branch
        branch_label = entry.branch_name or "(not created)"
        status = None

        line_text = f"{marker} {entry.wp_id} [{status}] base={base_label} branch={branch_label}"
        if entry.worktree_exists and entry.commits_ahead_of_base > 0:
            line_text += f" (+{entry.commits_ahead_of_base})"

        # Pad to fit box
        padded = line_text[:76].ljust(76)
        lines.append(f"║  {padded}║")

    lines.append("╚" + "═" * 78 + "╝")
    return lines


def x_render_topology_text__mutmut_47(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as human-readable text for CLI output.

    Utility function for human-facing displays (not used in prompts).

    Args:
        topology: Feature topology data
        current_wp_id: The WP to highlight

    Returns:
        List of lines for console output
    """
    lines = []
    lines.append("╔" + "═" * 78 + "╗")
    lines.append("║  WORKTREE TOPOLOGY" + " " * 59 + "║")
    lines.append("╠" + "═" * 78 + "╣")
    lines.append(f"║  Feature: {topology.feature_slug:<66} ║")
    lines.append(f"║  Target:  {topology.target_branch:<66} ║")
    lines.append("║" + " " * 78 + "║")

    for entry in topology.entries:
        marker = "→" if entry.wp_id == current_wp_id else " "
        base_label = entry.base_wp if entry.base_wp else topology.target_branch
        branch_label = entry.branch_name or "(not created)"
        status = entry.lane

        line_text = None
        if entry.worktree_exists and entry.commits_ahead_of_base > 0:
            line_text += f" (+{entry.commits_ahead_of_base})"

        # Pad to fit box
        padded = line_text[:76].ljust(76)
        lines.append(f"║  {padded}║")

    lines.append("╚" + "═" * 78 + "╝")
    return lines


def x_render_topology_text__mutmut_48(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as human-readable text for CLI output.

    Utility function for human-facing displays (not used in prompts).

    Args:
        topology: Feature topology data
        current_wp_id: The WP to highlight

    Returns:
        List of lines for console output
    """
    lines = []
    lines.append("╔" + "═" * 78 + "╗")
    lines.append("║  WORKTREE TOPOLOGY" + " " * 59 + "║")
    lines.append("╠" + "═" * 78 + "╣")
    lines.append(f"║  Feature: {topology.feature_slug:<66} ║")
    lines.append(f"║  Target:  {topology.target_branch:<66} ║")
    lines.append("║" + " " * 78 + "║")

    for entry in topology.entries:
        marker = "→" if entry.wp_id == current_wp_id else " "
        base_label = entry.base_wp if entry.base_wp else topology.target_branch
        branch_label = entry.branch_name or "(not created)"
        status = entry.lane

        line_text = f"{marker} {entry.wp_id} [{status}] base={base_label} branch={branch_label}"
        if entry.worktree_exists or entry.commits_ahead_of_base > 0:
            line_text += f" (+{entry.commits_ahead_of_base})"

        # Pad to fit box
        padded = line_text[:76].ljust(76)
        lines.append(f"║  {padded}║")

    lines.append("╚" + "═" * 78 + "╝")
    return lines


def x_render_topology_text__mutmut_49(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as human-readable text for CLI output.

    Utility function for human-facing displays (not used in prompts).

    Args:
        topology: Feature topology data
        current_wp_id: The WP to highlight

    Returns:
        List of lines for console output
    """
    lines = []
    lines.append("╔" + "═" * 78 + "╗")
    lines.append("║  WORKTREE TOPOLOGY" + " " * 59 + "║")
    lines.append("╠" + "═" * 78 + "╣")
    lines.append(f"║  Feature: {topology.feature_slug:<66} ║")
    lines.append(f"║  Target:  {topology.target_branch:<66} ║")
    lines.append("║" + " " * 78 + "║")

    for entry in topology.entries:
        marker = "→" if entry.wp_id == current_wp_id else " "
        base_label = entry.base_wp if entry.base_wp else topology.target_branch
        branch_label = entry.branch_name or "(not created)"
        status = entry.lane

        line_text = f"{marker} {entry.wp_id} [{status}] base={base_label} branch={branch_label}"
        if entry.worktree_exists and entry.commits_ahead_of_base >= 0:
            line_text += f" (+{entry.commits_ahead_of_base})"

        # Pad to fit box
        padded = line_text[:76].ljust(76)
        lines.append(f"║  {padded}║")

    lines.append("╚" + "═" * 78 + "╝")
    return lines


def x_render_topology_text__mutmut_50(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as human-readable text for CLI output.

    Utility function for human-facing displays (not used in prompts).

    Args:
        topology: Feature topology data
        current_wp_id: The WP to highlight

    Returns:
        List of lines for console output
    """
    lines = []
    lines.append("╔" + "═" * 78 + "╗")
    lines.append("║  WORKTREE TOPOLOGY" + " " * 59 + "║")
    lines.append("╠" + "═" * 78 + "╣")
    lines.append(f"║  Feature: {topology.feature_slug:<66} ║")
    lines.append(f"║  Target:  {topology.target_branch:<66} ║")
    lines.append("║" + " " * 78 + "║")

    for entry in topology.entries:
        marker = "→" if entry.wp_id == current_wp_id else " "
        base_label = entry.base_wp if entry.base_wp else topology.target_branch
        branch_label = entry.branch_name or "(not created)"
        status = entry.lane

        line_text = f"{marker} {entry.wp_id} [{status}] base={base_label} branch={branch_label}"
        if entry.worktree_exists and entry.commits_ahead_of_base > 1:
            line_text += f" (+{entry.commits_ahead_of_base})"

        # Pad to fit box
        padded = line_text[:76].ljust(76)
        lines.append(f"║  {padded}║")

    lines.append("╚" + "═" * 78 + "╝")
    return lines


def x_render_topology_text__mutmut_51(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as human-readable text for CLI output.

    Utility function for human-facing displays (not used in prompts).

    Args:
        topology: Feature topology data
        current_wp_id: The WP to highlight

    Returns:
        List of lines for console output
    """
    lines = []
    lines.append("╔" + "═" * 78 + "╗")
    lines.append("║  WORKTREE TOPOLOGY" + " " * 59 + "║")
    lines.append("╠" + "═" * 78 + "╣")
    lines.append(f"║  Feature: {topology.feature_slug:<66} ║")
    lines.append(f"║  Target:  {topology.target_branch:<66} ║")
    lines.append("║" + " " * 78 + "║")

    for entry in topology.entries:
        marker = "→" if entry.wp_id == current_wp_id else " "
        base_label = entry.base_wp if entry.base_wp else topology.target_branch
        branch_label = entry.branch_name or "(not created)"
        status = entry.lane

        line_text = f"{marker} {entry.wp_id} [{status}] base={base_label} branch={branch_label}"
        if entry.worktree_exists and entry.commits_ahead_of_base > 0:
            line_text = f" (+{entry.commits_ahead_of_base})"

        # Pad to fit box
        padded = line_text[:76].ljust(76)
        lines.append(f"║  {padded}║")

    lines.append("╚" + "═" * 78 + "╝")
    return lines


def x_render_topology_text__mutmut_52(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as human-readable text for CLI output.

    Utility function for human-facing displays (not used in prompts).

    Args:
        topology: Feature topology data
        current_wp_id: The WP to highlight

    Returns:
        List of lines for console output
    """
    lines = []
    lines.append("╔" + "═" * 78 + "╗")
    lines.append("║  WORKTREE TOPOLOGY" + " " * 59 + "║")
    lines.append("╠" + "═" * 78 + "╣")
    lines.append(f"║  Feature: {topology.feature_slug:<66} ║")
    lines.append(f"║  Target:  {topology.target_branch:<66} ║")
    lines.append("║" + " " * 78 + "║")

    for entry in topology.entries:
        marker = "→" if entry.wp_id == current_wp_id else " "
        base_label = entry.base_wp if entry.base_wp else topology.target_branch
        branch_label = entry.branch_name or "(not created)"
        status = entry.lane

        line_text = f"{marker} {entry.wp_id} [{status}] base={base_label} branch={branch_label}"
        if entry.worktree_exists and entry.commits_ahead_of_base > 0:
            line_text -= f" (+{entry.commits_ahead_of_base})"

        # Pad to fit box
        padded = line_text[:76].ljust(76)
        lines.append(f"║  {padded}║")

    lines.append("╚" + "═" * 78 + "╝")
    return lines


def x_render_topology_text__mutmut_53(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as human-readable text for CLI output.

    Utility function for human-facing displays (not used in prompts).

    Args:
        topology: Feature topology data
        current_wp_id: The WP to highlight

    Returns:
        List of lines for console output
    """
    lines = []
    lines.append("╔" + "═" * 78 + "╗")
    lines.append("║  WORKTREE TOPOLOGY" + " " * 59 + "║")
    lines.append("╠" + "═" * 78 + "╣")
    lines.append(f"║  Feature: {topology.feature_slug:<66} ║")
    lines.append(f"║  Target:  {topology.target_branch:<66} ║")
    lines.append("║" + " " * 78 + "║")

    for entry in topology.entries:
        marker = "→" if entry.wp_id == current_wp_id else " "
        base_label = entry.base_wp if entry.base_wp else topology.target_branch
        branch_label = entry.branch_name or "(not created)"
        status = entry.lane

        line_text = f"{marker} {entry.wp_id} [{status}] base={base_label} branch={branch_label}"
        if entry.worktree_exists and entry.commits_ahead_of_base > 0:
            line_text += f" (+{entry.commits_ahead_of_base})"

        # Pad to fit box
        padded = None
        lines.append(f"║  {padded}║")

    lines.append("╚" + "═" * 78 + "╝")
    return lines


def x_render_topology_text__mutmut_54(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as human-readable text for CLI output.

    Utility function for human-facing displays (not used in prompts).

    Args:
        topology: Feature topology data
        current_wp_id: The WP to highlight

    Returns:
        List of lines for console output
    """
    lines = []
    lines.append("╔" + "═" * 78 + "╗")
    lines.append("║  WORKTREE TOPOLOGY" + " " * 59 + "║")
    lines.append("╠" + "═" * 78 + "╣")
    lines.append(f"║  Feature: {topology.feature_slug:<66} ║")
    lines.append(f"║  Target:  {topology.target_branch:<66} ║")
    lines.append("║" + " " * 78 + "║")

    for entry in topology.entries:
        marker = "→" if entry.wp_id == current_wp_id else " "
        base_label = entry.base_wp if entry.base_wp else topology.target_branch
        branch_label = entry.branch_name or "(not created)"
        status = entry.lane

        line_text = f"{marker} {entry.wp_id} [{status}] base={base_label} branch={branch_label}"
        if entry.worktree_exists and entry.commits_ahead_of_base > 0:
            line_text += f" (+{entry.commits_ahead_of_base})"

        # Pad to fit box
        padded = line_text[:76].ljust(None)
        lines.append(f"║  {padded}║")

    lines.append("╚" + "═" * 78 + "╝")
    return lines


def x_render_topology_text__mutmut_55(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as human-readable text for CLI output.

    Utility function for human-facing displays (not used in prompts).

    Args:
        topology: Feature topology data
        current_wp_id: The WP to highlight

    Returns:
        List of lines for console output
    """
    lines = []
    lines.append("╔" + "═" * 78 + "╗")
    lines.append("║  WORKTREE TOPOLOGY" + " " * 59 + "║")
    lines.append("╠" + "═" * 78 + "╣")
    lines.append(f"║  Feature: {topology.feature_slug:<66} ║")
    lines.append(f"║  Target:  {topology.target_branch:<66} ║")
    lines.append("║" + " " * 78 + "║")

    for entry in topology.entries:
        marker = "→" if entry.wp_id == current_wp_id else " "
        base_label = entry.base_wp if entry.base_wp else topology.target_branch
        branch_label = entry.branch_name or "(not created)"
        status = entry.lane

        line_text = f"{marker} {entry.wp_id} [{status}] base={base_label} branch={branch_label}"
        if entry.worktree_exists and entry.commits_ahead_of_base > 0:
            line_text += f" (+{entry.commits_ahead_of_base})"

        # Pad to fit box
        padded = line_text[:76].rjust(76)
        lines.append(f"║  {padded}║")

    lines.append("╚" + "═" * 78 + "╝")
    return lines


def x_render_topology_text__mutmut_56(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as human-readable text for CLI output.

    Utility function for human-facing displays (not used in prompts).

    Args:
        topology: Feature topology data
        current_wp_id: The WP to highlight

    Returns:
        List of lines for console output
    """
    lines = []
    lines.append("╔" + "═" * 78 + "╗")
    lines.append("║  WORKTREE TOPOLOGY" + " " * 59 + "║")
    lines.append("╠" + "═" * 78 + "╣")
    lines.append(f"║  Feature: {topology.feature_slug:<66} ║")
    lines.append(f"║  Target:  {topology.target_branch:<66} ║")
    lines.append("║" + " " * 78 + "║")

    for entry in topology.entries:
        marker = "→" if entry.wp_id == current_wp_id else " "
        base_label = entry.base_wp if entry.base_wp else topology.target_branch
        branch_label = entry.branch_name or "(not created)"
        status = entry.lane

        line_text = f"{marker} {entry.wp_id} [{status}] base={base_label} branch={branch_label}"
        if entry.worktree_exists and entry.commits_ahead_of_base > 0:
            line_text += f" (+{entry.commits_ahead_of_base})"

        # Pad to fit box
        padded = line_text[:77].ljust(76)
        lines.append(f"║  {padded}║")

    lines.append("╚" + "═" * 78 + "╝")
    return lines


def x_render_topology_text__mutmut_57(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as human-readable text for CLI output.

    Utility function for human-facing displays (not used in prompts).

    Args:
        topology: Feature topology data
        current_wp_id: The WP to highlight

    Returns:
        List of lines for console output
    """
    lines = []
    lines.append("╔" + "═" * 78 + "╗")
    lines.append("║  WORKTREE TOPOLOGY" + " " * 59 + "║")
    lines.append("╠" + "═" * 78 + "╣")
    lines.append(f"║  Feature: {topology.feature_slug:<66} ║")
    lines.append(f"║  Target:  {topology.target_branch:<66} ║")
    lines.append("║" + " " * 78 + "║")

    for entry in topology.entries:
        marker = "→" if entry.wp_id == current_wp_id else " "
        base_label = entry.base_wp if entry.base_wp else topology.target_branch
        branch_label = entry.branch_name or "(not created)"
        status = entry.lane

        line_text = f"{marker} {entry.wp_id} [{status}] base={base_label} branch={branch_label}"
        if entry.worktree_exists and entry.commits_ahead_of_base > 0:
            line_text += f" (+{entry.commits_ahead_of_base})"

        # Pad to fit box
        padded = line_text[:76].ljust(77)
        lines.append(f"║  {padded}║")

    lines.append("╚" + "═" * 78 + "╝")
    return lines


def x_render_topology_text__mutmut_58(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as human-readable text for CLI output.

    Utility function for human-facing displays (not used in prompts).

    Args:
        topology: Feature topology data
        current_wp_id: The WP to highlight

    Returns:
        List of lines for console output
    """
    lines = []
    lines.append("╔" + "═" * 78 + "╗")
    lines.append("║  WORKTREE TOPOLOGY" + " " * 59 + "║")
    lines.append("╠" + "═" * 78 + "╣")
    lines.append(f"║  Feature: {topology.feature_slug:<66} ║")
    lines.append(f"║  Target:  {topology.target_branch:<66} ║")
    lines.append("║" + " " * 78 + "║")

    for entry in topology.entries:
        marker = "→" if entry.wp_id == current_wp_id else " "
        base_label = entry.base_wp if entry.base_wp else topology.target_branch
        branch_label = entry.branch_name or "(not created)"
        status = entry.lane

        line_text = f"{marker} {entry.wp_id} [{status}] base={base_label} branch={branch_label}"
        if entry.worktree_exists and entry.commits_ahead_of_base > 0:
            line_text += f" (+{entry.commits_ahead_of_base})"

        # Pad to fit box
        padded = line_text[:76].ljust(76)
        lines.append(None)

    lines.append("╚" + "═" * 78 + "╝")
    return lines


def x_render_topology_text__mutmut_59(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as human-readable text for CLI output.

    Utility function for human-facing displays (not used in prompts).

    Args:
        topology: Feature topology data
        current_wp_id: The WP to highlight

    Returns:
        List of lines for console output
    """
    lines = []
    lines.append("╔" + "═" * 78 + "╗")
    lines.append("║  WORKTREE TOPOLOGY" + " " * 59 + "║")
    lines.append("╠" + "═" * 78 + "╣")
    lines.append(f"║  Feature: {topology.feature_slug:<66} ║")
    lines.append(f"║  Target:  {topology.target_branch:<66} ║")
    lines.append("║" + " " * 78 + "║")

    for entry in topology.entries:
        marker = "→" if entry.wp_id == current_wp_id else " "
        base_label = entry.base_wp if entry.base_wp else topology.target_branch
        branch_label = entry.branch_name or "(not created)"
        status = entry.lane

        line_text = f"{marker} {entry.wp_id} [{status}] base={base_label} branch={branch_label}"
        if entry.worktree_exists and entry.commits_ahead_of_base > 0:
            line_text += f" (+{entry.commits_ahead_of_base})"

        # Pad to fit box
        padded = line_text[:76].ljust(76)
        lines.append(f"║  {padded}║")

    lines.append(None)
    return lines


def x_render_topology_text__mutmut_60(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as human-readable text for CLI output.

    Utility function for human-facing displays (not used in prompts).

    Args:
        topology: Feature topology data
        current_wp_id: The WP to highlight

    Returns:
        List of lines for console output
    """
    lines = []
    lines.append("╔" + "═" * 78 + "╗")
    lines.append("║  WORKTREE TOPOLOGY" + " " * 59 + "║")
    lines.append("╠" + "═" * 78 + "╣")
    lines.append(f"║  Feature: {topology.feature_slug:<66} ║")
    lines.append(f"║  Target:  {topology.target_branch:<66} ║")
    lines.append("║" + " " * 78 + "║")

    for entry in topology.entries:
        marker = "→" if entry.wp_id == current_wp_id else " "
        base_label = entry.base_wp if entry.base_wp else topology.target_branch
        branch_label = entry.branch_name or "(not created)"
        status = entry.lane

        line_text = f"{marker} {entry.wp_id} [{status}] base={base_label} branch={branch_label}"
        if entry.worktree_exists and entry.commits_ahead_of_base > 0:
            line_text += f" (+{entry.commits_ahead_of_base})"

        # Pad to fit box
        padded = line_text[:76].ljust(76)
        lines.append(f"║  {padded}║")

    lines.append("╚" + "═" * 78 - "╝")
    return lines


def x_render_topology_text__mutmut_61(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as human-readable text for CLI output.

    Utility function for human-facing displays (not used in prompts).

    Args:
        topology: Feature topology data
        current_wp_id: The WP to highlight

    Returns:
        List of lines for console output
    """
    lines = []
    lines.append("╔" + "═" * 78 + "╗")
    lines.append("║  WORKTREE TOPOLOGY" + " " * 59 + "║")
    lines.append("╠" + "═" * 78 + "╣")
    lines.append(f"║  Feature: {topology.feature_slug:<66} ║")
    lines.append(f"║  Target:  {topology.target_branch:<66} ║")
    lines.append("║" + " " * 78 + "║")

    for entry in topology.entries:
        marker = "→" if entry.wp_id == current_wp_id else " "
        base_label = entry.base_wp if entry.base_wp else topology.target_branch
        branch_label = entry.branch_name or "(not created)"
        status = entry.lane

        line_text = f"{marker} {entry.wp_id} [{status}] base={base_label} branch={branch_label}"
        if entry.worktree_exists and entry.commits_ahead_of_base > 0:
            line_text += f" (+{entry.commits_ahead_of_base})"

        # Pad to fit box
        padded = line_text[:76].ljust(76)
        lines.append(f"║  {padded}║")

    lines.append("╚" - "═" * 78 + "╝")
    return lines


def x_render_topology_text__mutmut_62(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as human-readable text for CLI output.

    Utility function for human-facing displays (not used in prompts).

    Args:
        topology: Feature topology data
        current_wp_id: The WP to highlight

    Returns:
        List of lines for console output
    """
    lines = []
    lines.append("╔" + "═" * 78 + "╗")
    lines.append("║  WORKTREE TOPOLOGY" + " " * 59 + "║")
    lines.append("╠" + "═" * 78 + "╣")
    lines.append(f"║  Feature: {topology.feature_slug:<66} ║")
    lines.append(f"║  Target:  {topology.target_branch:<66} ║")
    lines.append("║" + " " * 78 + "║")

    for entry in topology.entries:
        marker = "→" if entry.wp_id == current_wp_id else " "
        base_label = entry.base_wp if entry.base_wp else topology.target_branch
        branch_label = entry.branch_name or "(not created)"
        status = entry.lane

        line_text = f"{marker} {entry.wp_id} [{status}] base={base_label} branch={branch_label}"
        if entry.worktree_exists and entry.commits_ahead_of_base > 0:
            line_text += f" (+{entry.commits_ahead_of_base})"

        # Pad to fit box
        padded = line_text[:76].ljust(76)
        lines.append(f"║  {padded}║")

    lines.append("XX╚XX" + "═" * 78 + "╝")
    return lines


def x_render_topology_text__mutmut_63(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as human-readable text for CLI output.

    Utility function for human-facing displays (not used in prompts).

    Args:
        topology: Feature topology data
        current_wp_id: The WP to highlight

    Returns:
        List of lines for console output
    """
    lines = []
    lines.append("╔" + "═" * 78 + "╗")
    lines.append("║  WORKTREE TOPOLOGY" + " " * 59 + "║")
    lines.append("╠" + "═" * 78 + "╣")
    lines.append(f"║  Feature: {topology.feature_slug:<66} ║")
    lines.append(f"║  Target:  {topology.target_branch:<66} ║")
    lines.append("║" + " " * 78 + "║")

    for entry in topology.entries:
        marker = "→" if entry.wp_id == current_wp_id else " "
        base_label = entry.base_wp if entry.base_wp else topology.target_branch
        branch_label = entry.branch_name or "(not created)"
        status = entry.lane

        line_text = f"{marker} {entry.wp_id} [{status}] base={base_label} branch={branch_label}"
        if entry.worktree_exists and entry.commits_ahead_of_base > 0:
            line_text += f" (+{entry.commits_ahead_of_base})"

        # Pad to fit box
        padded = line_text[:76].ljust(76)
        lines.append(f"║  {padded}║")

    lines.append("╚" + "═" / 78 + "╝")
    return lines


def x_render_topology_text__mutmut_64(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as human-readable text for CLI output.

    Utility function for human-facing displays (not used in prompts).

    Args:
        topology: Feature topology data
        current_wp_id: The WP to highlight

    Returns:
        List of lines for console output
    """
    lines = []
    lines.append("╔" + "═" * 78 + "╗")
    lines.append("║  WORKTREE TOPOLOGY" + " " * 59 + "║")
    lines.append("╠" + "═" * 78 + "╣")
    lines.append(f"║  Feature: {topology.feature_slug:<66} ║")
    lines.append(f"║  Target:  {topology.target_branch:<66} ║")
    lines.append("║" + " " * 78 + "║")

    for entry in topology.entries:
        marker = "→" if entry.wp_id == current_wp_id else " "
        base_label = entry.base_wp if entry.base_wp else topology.target_branch
        branch_label = entry.branch_name or "(not created)"
        status = entry.lane

        line_text = f"{marker} {entry.wp_id} [{status}] base={base_label} branch={branch_label}"
        if entry.worktree_exists and entry.commits_ahead_of_base > 0:
            line_text += f" (+{entry.commits_ahead_of_base})"

        # Pad to fit box
        padded = line_text[:76].ljust(76)
        lines.append(f"║  {padded}║")

    lines.append("╚" + "XX═XX" * 78 + "╝")
    return lines


def x_render_topology_text__mutmut_65(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as human-readable text for CLI output.

    Utility function for human-facing displays (not used in prompts).

    Args:
        topology: Feature topology data
        current_wp_id: The WP to highlight

    Returns:
        List of lines for console output
    """
    lines = []
    lines.append("╔" + "═" * 78 + "╗")
    lines.append("║  WORKTREE TOPOLOGY" + " " * 59 + "║")
    lines.append("╠" + "═" * 78 + "╣")
    lines.append(f"║  Feature: {topology.feature_slug:<66} ║")
    lines.append(f"║  Target:  {topology.target_branch:<66} ║")
    lines.append("║" + " " * 78 + "║")

    for entry in topology.entries:
        marker = "→" if entry.wp_id == current_wp_id else " "
        base_label = entry.base_wp if entry.base_wp else topology.target_branch
        branch_label = entry.branch_name or "(not created)"
        status = entry.lane

        line_text = f"{marker} {entry.wp_id} [{status}] base={base_label} branch={branch_label}"
        if entry.worktree_exists and entry.commits_ahead_of_base > 0:
            line_text += f" (+{entry.commits_ahead_of_base})"

        # Pad to fit box
        padded = line_text[:76].ljust(76)
        lines.append(f"║  {padded}║")

    lines.append("╚" + "═" * 79 + "╝")
    return lines


def x_render_topology_text__mutmut_66(
    topology: FeatureTopology,
    current_wp_id: str,
) -> list[str]:
    """Render topology as human-readable text for CLI output.

    Utility function for human-facing displays (not used in prompts).

    Args:
        topology: Feature topology data
        current_wp_id: The WP to highlight

    Returns:
        List of lines for console output
    """
    lines = []
    lines.append("╔" + "═" * 78 + "╗")
    lines.append("║  WORKTREE TOPOLOGY" + " " * 59 + "║")
    lines.append("╠" + "═" * 78 + "╣")
    lines.append(f"║  Feature: {topology.feature_slug:<66} ║")
    lines.append(f"║  Target:  {topology.target_branch:<66} ║")
    lines.append("║" + " " * 78 + "║")

    for entry in topology.entries:
        marker = "→" if entry.wp_id == current_wp_id else " "
        base_label = entry.base_wp if entry.base_wp else topology.target_branch
        branch_label = entry.branch_name or "(not created)"
        status = entry.lane

        line_text = f"{marker} {entry.wp_id} [{status}] base={base_label} branch={branch_label}"
        if entry.worktree_exists and entry.commits_ahead_of_base > 0:
            line_text += f" (+{entry.commits_ahead_of_base})"

        # Pad to fit box
        padded = line_text[:76].ljust(76)
        lines.append(f"║  {padded}║")

    lines.append("╚" + "═" * 78 + "XX╝XX")
    return lines

x_render_topology_text__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_render_topology_text__mutmut_1': x_render_topology_text__mutmut_1, 
    'x_render_topology_text__mutmut_2': x_render_topology_text__mutmut_2, 
    'x_render_topology_text__mutmut_3': x_render_topology_text__mutmut_3, 
    'x_render_topology_text__mutmut_4': x_render_topology_text__mutmut_4, 
    'x_render_topology_text__mutmut_5': x_render_topology_text__mutmut_5, 
    'x_render_topology_text__mutmut_6': x_render_topology_text__mutmut_6, 
    'x_render_topology_text__mutmut_7': x_render_topology_text__mutmut_7, 
    'x_render_topology_text__mutmut_8': x_render_topology_text__mutmut_8, 
    'x_render_topology_text__mutmut_9': x_render_topology_text__mutmut_9, 
    'x_render_topology_text__mutmut_10': x_render_topology_text__mutmut_10, 
    'x_render_topology_text__mutmut_11': x_render_topology_text__mutmut_11, 
    'x_render_topology_text__mutmut_12': x_render_topology_text__mutmut_12, 
    'x_render_topology_text__mutmut_13': x_render_topology_text__mutmut_13, 
    'x_render_topology_text__mutmut_14': x_render_topology_text__mutmut_14, 
    'x_render_topology_text__mutmut_15': x_render_topology_text__mutmut_15, 
    'x_render_topology_text__mutmut_16': x_render_topology_text__mutmut_16, 
    'x_render_topology_text__mutmut_17': x_render_topology_text__mutmut_17, 
    'x_render_topology_text__mutmut_18': x_render_topology_text__mutmut_18, 
    'x_render_topology_text__mutmut_19': x_render_topology_text__mutmut_19, 
    'x_render_topology_text__mutmut_20': x_render_topology_text__mutmut_20, 
    'x_render_topology_text__mutmut_21': x_render_topology_text__mutmut_21, 
    'x_render_topology_text__mutmut_22': x_render_topology_text__mutmut_22, 
    'x_render_topology_text__mutmut_23': x_render_topology_text__mutmut_23, 
    'x_render_topology_text__mutmut_24': x_render_topology_text__mutmut_24, 
    'x_render_topology_text__mutmut_25': x_render_topology_text__mutmut_25, 
    'x_render_topology_text__mutmut_26': x_render_topology_text__mutmut_26, 
    'x_render_topology_text__mutmut_27': x_render_topology_text__mutmut_27, 
    'x_render_topology_text__mutmut_28': x_render_topology_text__mutmut_28, 
    'x_render_topology_text__mutmut_29': x_render_topology_text__mutmut_29, 
    'x_render_topology_text__mutmut_30': x_render_topology_text__mutmut_30, 
    'x_render_topology_text__mutmut_31': x_render_topology_text__mutmut_31, 
    'x_render_topology_text__mutmut_32': x_render_topology_text__mutmut_32, 
    'x_render_topology_text__mutmut_33': x_render_topology_text__mutmut_33, 
    'x_render_topology_text__mutmut_34': x_render_topology_text__mutmut_34, 
    'x_render_topology_text__mutmut_35': x_render_topology_text__mutmut_35, 
    'x_render_topology_text__mutmut_36': x_render_topology_text__mutmut_36, 
    'x_render_topology_text__mutmut_37': x_render_topology_text__mutmut_37, 
    'x_render_topology_text__mutmut_38': x_render_topology_text__mutmut_38, 
    'x_render_topology_text__mutmut_39': x_render_topology_text__mutmut_39, 
    'x_render_topology_text__mutmut_40': x_render_topology_text__mutmut_40, 
    'x_render_topology_text__mutmut_41': x_render_topology_text__mutmut_41, 
    'x_render_topology_text__mutmut_42': x_render_topology_text__mutmut_42, 
    'x_render_topology_text__mutmut_43': x_render_topology_text__mutmut_43, 
    'x_render_topology_text__mutmut_44': x_render_topology_text__mutmut_44, 
    'x_render_topology_text__mutmut_45': x_render_topology_text__mutmut_45, 
    'x_render_topology_text__mutmut_46': x_render_topology_text__mutmut_46, 
    'x_render_topology_text__mutmut_47': x_render_topology_text__mutmut_47, 
    'x_render_topology_text__mutmut_48': x_render_topology_text__mutmut_48, 
    'x_render_topology_text__mutmut_49': x_render_topology_text__mutmut_49, 
    'x_render_topology_text__mutmut_50': x_render_topology_text__mutmut_50, 
    'x_render_topology_text__mutmut_51': x_render_topology_text__mutmut_51, 
    'x_render_topology_text__mutmut_52': x_render_topology_text__mutmut_52, 
    'x_render_topology_text__mutmut_53': x_render_topology_text__mutmut_53, 
    'x_render_topology_text__mutmut_54': x_render_topology_text__mutmut_54, 
    'x_render_topology_text__mutmut_55': x_render_topology_text__mutmut_55, 
    'x_render_topology_text__mutmut_56': x_render_topology_text__mutmut_56, 
    'x_render_topology_text__mutmut_57': x_render_topology_text__mutmut_57, 
    'x_render_topology_text__mutmut_58': x_render_topology_text__mutmut_58, 
    'x_render_topology_text__mutmut_59': x_render_topology_text__mutmut_59, 
    'x_render_topology_text__mutmut_60': x_render_topology_text__mutmut_60, 
    'x_render_topology_text__mutmut_61': x_render_topology_text__mutmut_61, 
    'x_render_topology_text__mutmut_62': x_render_topology_text__mutmut_62, 
    'x_render_topology_text__mutmut_63': x_render_topology_text__mutmut_63, 
    'x_render_topology_text__mutmut_64': x_render_topology_text__mutmut_64, 
    'x_render_topology_text__mutmut_65': x_render_topology_text__mutmut_65, 
    'x_render_topology_text__mutmut_66': x_render_topology_text__mutmut_66
}
x_render_topology_text__mutmut_orig.__name__ = 'x_render_topology_text'


__all__ = [
    "WPTopologyEntry",
    "FeatureTopology",
    "materialize_worktree_topology",
    "render_topology_json",
    "render_topology_text",
]
