"""
VCS Detection Module
====================

This module provides tool detection and the get_vcs() factory function.
It detects which VCS tools (git, jj) are available and returns the
appropriate implementation.

See kitty-specs/015-first-class-jujutsu-vcs-integration/contracts/vcs-protocol.py
for the factory function contract.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
from functools import lru_cache
from pathlib import Path
from typing import TYPE_CHECKING

from .exceptions import (
    VCSBackendMismatchError,
    VCSNotFoundError,
)
from .types import VCSBackend

if TYPE_CHECKING:
    from .protocol import VCSProtocol
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


# =============================================================================
# Tool Detection Functions
# =============================================================================


@lru_cache(maxsize=1)
def is_jj_available() -> bool:
    """
    Check if jj is installed and working.

    DISABLED: jj colocated mode is incompatible with sparse checkouts.
    This function now always returns False to prevent jj detection.

    Returns:
        False (jj detection disabled)
    """
    # DISABLED: jj is not compatible with sparse checkouts
    # Keeping function signature for VCS abstraction layer compatibility
    return False

    # Original implementation (commented out for reference):
    # if shutil.which("jj") is None:
    #     return False
    # try:
    #     result = subprocess.run(
    #         ["jj", "--version"],
    #         capture_output=True,
    #         timeout=5,
    #     )
    #     return result.returncode == 0
    # except (subprocess.TimeoutExpired, OSError):
    #     return False


@lru_cache(maxsize=1)
def is_git_available() -> bool:
    """
    Check if git is installed and working.

    Returns:
        True if git is installed and responds to --version, False otherwise.
    """
    if shutil.which("git") is None:
        return False
    try:
        result = subprocess.run(
            ["git", "--version"],
            capture_output=True,
            timeout=5,
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, OSError):
        return False


@lru_cache(maxsize=1)
def get_jj_version() -> str | None:
    """
    Get installed jj version, or None if not installed.

    DISABLED: jj detection is disabled (incompatible with sparse checkouts).

    Returns:
        None (jj detection disabled)
    """
    # DISABLED: jj is not compatible with sparse checkouts
    return None


@lru_cache(maxsize=1)
def get_git_version() -> str | None:
    """
    Get installed git version, or None if not installed.

    Returns:
        Version string (e.g., "2.43.0") or None if git is not available.
    """
    if not is_git_available():
        return None
    try:
        result = subprocess.run(
            ["git", "--version"],
            capture_output=True,
            timeout=5,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        if result.returncode != 0:
            return None
        # git version format: "git version 2.43.0" or "git version 2.43.0.windows.1"
        output = result.stdout.strip()
        match = re.search(r"git version\s+(\d+\.\d+\.\d+)", output)
        if match:
            return match.group(1)
        # Fallback: return everything after "git version "
        if "git version " in output:
            return output.split("git version ")[1].strip()
        return "unknown"
    except (subprocess.TimeoutExpired, OSError):
        return None


def detect_available_backends() -> list[VCSBackend]:
    args = []# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_detect_available_backends__mutmut_orig, x_detect_available_backends__mutmut_mutants, args, kwargs, None)


def x_detect_available_backends__mutmut_orig() -> list[VCSBackend]:
    """
    Detect which VCS tools are installed and available.

    Returns:
        List of available backends, in preference order (jj first if available).
    """
    backends = []
    if is_jj_available():
        backends.append(VCSBackend.JUJUTSU)
    if is_git_available():
        backends.append(VCSBackend.GIT)
    return backends


def x_detect_available_backends__mutmut_1() -> list[VCSBackend]:
    """
    Detect which VCS tools are installed and available.

    Returns:
        List of available backends, in preference order (jj first if available).
    """
    backends = None
    if is_jj_available():
        backends.append(VCSBackend.JUJUTSU)
    if is_git_available():
        backends.append(VCSBackend.GIT)
    return backends


def x_detect_available_backends__mutmut_2() -> list[VCSBackend]:
    """
    Detect which VCS tools are installed and available.

    Returns:
        List of available backends, in preference order (jj first if available).
    """
    backends = []
    if is_jj_available():
        backends.append(None)
    if is_git_available():
        backends.append(VCSBackend.GIT)
    return backends


def x_detect_available_backends__mutmut_3() -> list[VCSBackend]:
    """
    Detect which VCS tools are installed and available.

    Returns:
        List of available backends, in preference order (jj first if available).
    """
    backends = []
    if is_jj_available():
        backends.append(VCSBackend.JUJUTSU)
    if is_git_available():
        backends.append(None)
    return backends

x_detect_available_backends__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_detect_available_backends__mutmut_1': x_detect_available_backends__mutmut_1, 
    'x_detect_available_backends__mutmut_2': x_detect_available_backends__mutmut_2, 
    'x_detect_available_backends__mutmut_3': x_detect_available_backends__mutmut_3
}
x_detect_available_backends__mutmut_orig.__name__ = 'x_detect_available_backends'


# =============================================================================
# Factory Function
# =============================================================================


def _get_locked_vcs_from_feature(path: Path) -> VCSBackend | None:
    args = [path]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x__get_locked_vcs_from_feature__mutmut_orig, x__get_locked_vcs_from_feature__mutmut_mutants, args, kwargs, None)


# =============================================================================
# Factory Function
# =============================================================================


def x__get_locked_vcs_from_feature__mutmut_orig(path: Path) -> VCSBackend | None:
    """
    Read VCS from feature meta.json if path is inside that feature.

    Args:
        path: A path that might be within a feature directory.

    Returns:
        The locked VCSBackend if path is inside a feature with locked VCS, None otherwise.

    Note:
        Only returns a locked VCS if `path` is actually inside the feature directory
        (either in kitty-specs/###-feature/ or in a worktree for that feature).
        Does NOT return VCS for unrelated features.
    """
    current = path.resolve()

    # Strategy 1: Check if path is directly inside kitty-specs/###-feature/
    # e.g., /repo/kitty-specs/015-feature/tasks/WP01.md
    for parent in [current, *current.parents]:
        if parent.parent and parent.parent.name == "kitty-specs":
            # parent is a feature directory like kitty-specs/015-feature/
            meta_path = parent / "meta.json"
            if meta_path.is_file():
                try:
                    meta = json.loads(meta_path.read_text())
                    if "vcs" in meta:
                        return VCSBackend(meta["vcs"])
                except (json.JSONDecodeError, ValueError, OSError):
                    pass
            # Path is in a feature dir but no valid meta.json
            return None

    # Strategy 2: Check if we're in a worktree for a feature
    # e.g., .worktrees/015-feature-name-WP01/src/file.py
    if ".worktrees" in str(current):
        # Find the worktree root (direct child of .worktrees/)
        worktree_root = None
        for parent in [current, *current.parents]:
            if parent.parent and parent.parent.name == ".worktrees":
                worktree_root = parent
                break

        if worktree_root:
            # Extract feature number from worktree name
            # Pattern: ###-feature-name-WP##
            worktree_name = worktree_root.name
            match = re.match(r"(\d{3})-", worktree_name)
            if match:
                feature_num = match.group(1)
                # Find main repo (parent of .worktrees)
                main_repo = worktree_root.parent.parent
                kitty_specs = main_repo / "kitty-specs"
                if kitty_specs.is_dir():
                    # Find the specific feature directory matching feature_num
                    for feature_dir in kitty_specs.iterdir():
                        if feature_dir.is_dir() and feature_dir.name.startswith(
                            f"{feature_num}-"
                        ):
                            meta_path = feature_dir / "meta.json"
                            if meta_path.is_file():
                                try:
                                    meta = json.loads(meta_path.read_text())
                                    if "vcs" in meta:
                                        return VCSBackend(meta["vcs"])
                                except (json.JSONDecodeError, ValueError, OSError):
                                    pass
                            # Found feature dir but no valid meta.json
                            return None

    # Path is not inside any feature
    return None


# =============================================================================
# Factory Function
# =============================================================================


def x__get_locked_vcs_from_feature__mutmut_1(path: Path) -> VCSBackend | None:
    """
    Read VCS from feature meta.json if path is inside that feature.

    Args:
        path: A path that might be within a feature directory.

    Returns:
        The locked VCSBackend if path is inside a feature with locked VCS, None otherwise.

    Note:
        Only returns a locked VCS if `path` is actually inside the feature directory
        (either in kitty-specs/###-feature/ or in a worktree for that feature).
        Does NOT return VCS for unrelated features.
    """
    current = None

    # Strategy 1: Check if path is directly inside kitty-specs/###-feature/
    # e.g., /repo/kitty-specs/015-feature/tasks/WP01.md
    for parent in [current, *current.parents]:
        if parent.parent and parent.parent.name == "kitty-specs":
            # parent is a feature directory like kitty-specs/015-feature/
            meta_path = parent / "meta.json"
            if meta_path.is_file():
                try:
                    meta = json.loads(meta_path.read_text())
                    if "vcs" in meta:
                        return VCSBackend(meta["vcs"])
                except (json.JSONDecodeError, ValueError, OSError):
                    pass
            # Path is in a feature dir but no valid meta.json
            return None

    # Strategy 2: Check if we're in a worktree for a feature
    # e.g., .worktrees/015-feature-name-WP01/src/file.py
    if ".worktrees" in str(current):
        # Find the worktree root (direct child of .worktrees/)
        worktree_root = None
        for parent in [current, *current.parents]:
            if parent.parent and parent.parent.name == ".worktrees":
                worktree_root = parent
                break

        if worktree_root:
            # Extract feature number from worktree name
            # Pattern: ###-feature-name-WP##
            worktree_name = worktree_root.name
            match = re.match(r"(\d{3})-", worktree_name)
            if match:
                feature_num = match.group(1)
                # Find main repo (parent of .worktrees)
                main_repo = worktree_root.parent.parent
                kitty_specs = main_repo / "kitty-specs"
                if kitty_specs.is_dir():
                    # Find the specific feature directory matching feature_num
                    for feature_dir in kitty_specs.iterdir():
                        if feature_dir.is_dir() and feature_dir.name.startswith(
                            f"{feature_num}-"
                        ):
                            meta_path = feature_dir / "meta.json"
                            if meta_path.is_file():
                                try:
                                    meta = json.loads(meta_path.read_text())
                                    if "vcs" in meta:
                                        return VCSBackend(meta["vcs"])
                                except (json.JSONDecodeError, ValueError, OSError):
                                    pass
                            # Found feature dir but no valid meta.json
                            return None

    # Path is not inside any feature
    return None


# =============================================================================
# Factory Function
# =============================================================================


def x__get_locked_vcs_from_feature__mutmut_2(path: Path) -> VCSBackend | None:
    """
    Read VCS from feature meta.json if path is inside that feature.

    Args:
        path: A path that might be within a feature directory.

    Returns:
        The locked VCSBackend if path is inside a feature with locked VCS, None otherwise.

    Note:
        Only returns a locked VCS if `path` is actually inside the feature directory
        (either in kitty-specs/###-feature/ or in a worktree for that feature).
        Does NOT return VCS for unrelated features.
    """
    current = path.resolve()

    # Strategy 1: Check if path is directly inside kitty-specs/###-feature/
    # e.g., /repo/kitty-specs/015-feature/tasks/WP01.md
    for parent in [current, *current.parents]:
        if parent.parent or parent.parent.name == "kitty-specs":
            # parent is a feature directory like kitty-specs/015-feature/
            meta_path = parent / "meta.json"
            if meta_path.is_file():
                try:
                    meta = json.loads(meta_path.read_text())
                    if "vcs" in meta:
                        return VCSBackend(meta["vcs"])
                except (json.JSONDecodeError, ValueError, OSError):
                    pass
            # Path is in a feature dir but no valid meta.json
            return None

    # Strategy 2: Check if we're in a worktree for a feature
    # e.g., .worktrees/015-feature-name-WP01/src/file.py
    if ".worktrees" in str(current):
        # Find the worktree root (direct child of .worktrees/)
        worktree_root = None
        for parent in [current, *current.parents]:
            if parent.parent and parent.parent.name == ".worktrees":
                worktree_root = parent
                break

        if worktree_root:
            # Extract feature number from worktree name
            # Pattern: ###-feature-name-WP##
            worktree_name = worktree_root.name
            match = re.match(r"(\d{3})-", worktree_name)
            if match:
                feature_num = match.group(1)
                # Find main repo (parent of .worktrees)
                main_repo = worktree_root.parent.parent
                kitty_specs = main_repo / "kitty-specs"
                if kitty_specs.is_dir():
                    # Find the specific feature directory matching feature_num
                    for feature_dir in kitty_specs.iterdir():
                        if feature_dir.is_dir() and feature_dir.name.startswith(
                            f"{feature_num}-"
                        ):
                            meta_path = feature_dir / "meta.json"
                            if meta_path.is_file():
                                try:
                                    meta = json.loads(meta_path.read_text())
                                    if "vcs" in meta:
                                        return VCSBackend(meta["vcs"])
                                except (json.JSONDecodeError, ValueError, OSError):
                                    pass
                            # Found feature dir but no valid meta.json
                            return None

    # Path is not inside any feature
    return None


# =============================================================================
# Factory Function
# =============================================================================


def x__get_locked_vcs_from_feature__mutmut_3(path: Path) -> VCSBackend | None:
    """
    Read VCS from feature meta.json if path is inside that feature.

    Args:
        path: A path that might be within a feature directory.

    Returns:
        The locked VCSBackend if path is inside a feature with locked VCS, None otherwise.

    Note:
        Only returns a locked VCS if `path` is actually inside the feature directory
        (either in kitty-specs/###-feature/ or in a worktree for that feature).
        Does NOT return VCS for unrelated features.
    """
    current = path.resolve()

    # Strategy 1: Check if path is directly inside kitty-specs/###-feature/
    # e.g., /repo/kitty-specs/015-feature/tasks/WP01.md
    for parent in [current, *current.parents]:
        if parent.parent and parent.parent.name != "kitty-specs":
            # parent is a feature directory like kitty-specs/015-feature/
            meta_path = parent / "meta.json"
            if meta_path.is_file():
                try:
                    meta = json.loads(meta_path.read_text())
                    if "vcs" in meta:
                        return VCSBackend(meta["vcs"])
                except (json.JSONDecodeError, ValueError, OSError):
                    pass
            # Path is in a feature dir but no valid meta.json
            return None

    # Strategy 2: Check if we're in a worktree for a feature
    # e.g., .worktrees/015-feature-name-WP01/src/file.py
    if ".worktrees" in str(current):
        # Find the worktree root (direct child of .worktrees/)
        worktree_root = None
        for parent in [current, *current.parents]:
            if parent.parent and parent.parent.name == ".worktrees":
                worktree_root = parent
                break

        if worktree_root:
            # Extract feature number from worktree name
            # Pattern: ###-feature-name-WP##
            worktree_name = worktree_root.name
            match = re.match(r"(\d{3})-", worktree_name)
            if match:
                feature_num = match.group(1)
                # Find main repo (parent of .worktrees)
                main_repo = worktree_root.parent.parent
                kitty_specs = main_repo / "kitty-specs"
                if kitty_specs.is_dir():
                    # Find the specific feature directory matching feature_num
                    for feature_dir in kitty_specs.iterdir():
                        if feature_dir.is_dir() and feature_dir.name.startswith(
                            f"{feature_num}-"
                        ):
                            meta_path = feature_dir / "meta.json"
                            if meta_path.is_file():
                                try:
                                    meta = json.loads(meta_path.read_text())
                                    if "vcs" in meta:
                                        return VCSBackend(meta["vcs"])
                                except (json.JSONDecodeError, ValueError, OSError):
                                    pass
                            # Found feature dir but no valid meta.json
                            return None

    # Path is not inside any feature
    return None


# =============================================================================
# Factory Function
# =============================================================================


def x__get_locked_vcs_from_feature__mutmut_4(path: Path) -> VCSBackend | None:
    """
    Read VCS from feature meta.json if path is inside that feature.

    Args:
        path: A path that might be within a feature directory.

    Returns:
        The locked VCSBackend if path is inside a feature with locked VCS, None otherwise.

    Note:
        Only returns a locked VCS if `path` is actually inside the feature directory
        (either in kitty-specs/###-feature/ or in a worktree for that feature).
        Does NOT return VCS for unrelated features.
    """
    current = path.resolve()

    # Strategy 1: Check if path is directly inside kitty-specs/###-feature/
    # e.g., /repo/kitty-specs/015-feature/tasks/WP01.md
    for parent in [current, *current.parents]:
        if parent.parent and parent.parent.name == "XXkitty-specsXX":
            # parent is a feature directory like kitty-specs/015-feature/
            meta_path = parent / "meta.json"
            if meta_path.is_file():
                try:
                    meta = json.loads(meta_path.read_text())
                    if "vcs" in meta:
                        return VCSBackend(meta["vcs"])
                except (json.JSONDecodeError, ValueError, OSError):
                    pass
            # Path is in a feature dir but no valid meta.json
            return None

    # Strategy 2: Check if we're in a worktree for a feature
    # e.g., .worktrees/015-feature-name-WP01/src/file.py
    if ".worktrees" in str(current):
        # Find the worktree root (direct child of .worktrees/)
        worktree_root = None
        for parent in [current, *current.parents]:
            if parent.parent and parent.parent.name == ".worktrees":
                worktree_root = parent
                break

        if worktree_root:
            # Extract feature number from worktree name
            # Pattern: ###-feature-name-WP##
            worktree_name = worktree_root.name
            match = re.match(r"(\d{3})-", worktree_name)
            if match:
                feature_num = match.group(1)
                # Find main repo (parent of .worktrees)
                main_repo = worktree_root.parent.parent
                kitty_specs = main_repo / "kitty-specs"
                if kitty_specs.is_dir():
                    # Find the specific feature directory matching feature_num
                    for feature_dir in kitty_specs.iterdir():
                        if feature_dir.is_dir() and feature_dir.name.startswith(
                            f"{feature_num}-"
                        ):
                            meta_path = feature_dir / "meta.json"
                            if meta_path.is_file():
                                try:
                                    meta = json.loads(meta_path.read_text())
                                    if "vcs" in meta:
                                        return VCSBackend(meta["vcs"])
                                except (json.JSONDecodeError, ValueError, OSError):
                                    pass
                            # Found feature dir but no valid meta.json
                            return None

    # Path is not inside any feature
    return None


# =============================================================================
# Factory Function
# =============================================================================


def x__get_locked_vcs_from_feature__mutmut_5(path: Path) -> VCSBackend | None:
    """
    Read VCS from feature meta.json if path is inside that feature.

    Args:
        path: A path that might be within a feature directory.

    Returns:
        The locked VCSBackend if path is inside a feature with locked VCS, None otherwise.

    Note:
        Only returns a locked VCS if `path` is actually inside the feature directory
        (either in kitty-specs/###-feature/ or in a worktree for that feature).
        Does NOT return VCS for unrelated features.
    """
    current = path.resolve()

    # Strategy 1: Check if path is directly inside kitty-specs/###-feature/
    # e.g., /repo/kitty-specs/015-feature/tasks/WP01.md
    for parent in [current, *current.parents]:
        if parent.parent and parent.parent.name == "KITTY-SPECS":
            # parent is a feature directory like kitty-specs/015-feature/
            meta_path = parent / "meta.json"
            if meta_path.is_file():
                try:
                    meta = json.loads(meta_path.read_text())
                    if "vcs" in meta:
                        return VCSBackend(meta["vcs"])
                except (json.JSONDecodeError, ValueError, OSError):
                    pass
            # Path is in a feature dir but no valid meta.json
            return None

    # Strategy 2: Check if we're in a worktree for a feature
    # e.g., .worktrees/015-feature-name-WP01/src/file.py
    if ".worktrees" in str(current):
        # Find the worktree root (direct child of .worktrees/)
        worktree_root = None
        for parent in [current, *current.parents]:
            if parent.parent and parent.parent.name == ".worktrees":
                worktree_root = parent
                break

        if worktree_root:
            # Extract feature number from worktree name
            # Pattern: ###-feature-name-WP##
            worktree_name = worktree_root.name
            match = re.match(r"(\d{3})-", worktree_name)
            if match:
                feature_num = match.group(1)
                # Find main repo (parent of .worktrees)
                main_repo = worktree_root.parent.parent
                kitty_specs = main_repo / "kitty-specs"
                if kitty_specs.is_dir():
                    # Find the specific feature directory matching feature_num
                    for feature_dir in kitty_specs.iterdir():
                        if feature_dir.is_dir() and feature_dir.name.startswith(
                            f"{feature_num}-"
                        ):
                            meta_path = feature_dir / "meta.json"
                            if meta_path.is_file():
                                try:
                                    meta = json.loads(meta_path.read_text())
                                    if "vcs" in meta:
                                        return VCSBackend(meta["vcs"])
                                except (json.JSONDecodeError, ValueError, OSError):
                                    pass
                            # Found feature dir but no valid meta.json
                            return None

    # Path is not inside any feature
    return None


# =============================================================================
# Factory Function
# =============================================================================


def x__get_locked_vcs_from_feature__mutmut_6(path: Path) -> VCSBackend | None:
    """
    Read VCS from feature meta.json if path is inside that feature.

    Args:
        path: A path that might be within a feature directory.

    Returns:
        The locked VCSBackend if path is inside a feature with locked VCS, None otherwise.

    Note:
        Only returns a locked VCS if `path` is actually inside the feature directory
        (either in kitty-specs/###-feature/ or in a worktree for that feature).
        Does NOT return VCS for unrelated features.
    """
    current = path.resolve()

    # Strategy 1: Check if path is directly inside kitty-specs/###-feature/
    # e.g., /repo/kitty-specs/015-feature/tasks/WP01.md
    for parent in [current, *current.parents]:
        if parent.parent and parent.parent.name == "kitty-specs":
            # parent is a feature directory like kitty-specs/015-feature/
            meta_path = None
            if meta_path.is_file():
                try:
                    meta = json.loads(meta_path.read_text())
                    if "vcs" in meta:
                        return VCSBackend(meta["vcs"])
                except (json.JSONDecodeError, ValueError, OSError):
                    pass
            # Path is in a feature dir but no valid meta.json
            return None

    # Strategy 2: Check if we're in a worktree for a feature
    # e.g., .worktrees/015-feature-name-WP01/src/file.py
    if ".worktrees" in str(current):
        # Find the worktree root (direct child of .worktrees/)
        worktree_root = None
        for parent in [current, *current.parents]:
            if parent.parent and parent.parent.name == ".worktrees":
                worktree_root = parent
                break

        if worktree_root:
            # Extract feature number from worktree name
            # Pattern: ###-feature-name-WP##
            worktree_name = worktree_root.name
            match = re.match(r"(\d{3})-", worktree_name)
            if match:
                feature_num = match.group(1)
                # Find main repo (parent of .worktrees)
                main_repo = worktree_root.parent.parent
                kitty_specs = main_repo / "kitty-specs"
                if kitty_specs.is_dir():
                    # Find the specific feature directory matching feature_num
                    for feature_dir in kitty_specs.iterdir():
                        if feature_dir.is_dir() and feature_dir.name.startswith(
                            f"{feature_num}-"
                        ):
                            meta_path = feature_dir / "meta.json"
                            if meta_path.is_file():
                                try:
                                    meta = json.loads(meta_path.read_text())
                                    if "vcs" in meta:
                                        return VCSBackend(meta["vcs"])
                                except (json.JSONDecodeError, ValueError, OSError):
                                    pass
                            # Found feature dir but no valid meta.json
                            return None

    # Path is not inside any feature
    return None


# =============================================================================
# Factory Function
# =============================================================================


def x__get_locked_vcs_from_feature__mutmut_7(path: Path) -> VCSBackend | None:
    """
    Read VCS from feature meta.json if path is inside that feature.

    Args:
        path: A path that might be within a feature directory.

    Returns:
        The locked VCSBackend if path is inside a feature with locked VCS, None otherwise.

    Note:
        Only returns a locked VCS if `path` is actually inside the feature directory
        (either in kitty-specs/###-feature/ or in a worktree for that feature).
        Does NOT return VCS for unrelated features.
    """
    current = path.resolve()

    # Strategy 1: Check if path is directly inside kitty-specs/###-feature/
    # e.g., /repo/kitty-specs/015-feature/tasks/WP01.md
    for parent in [current, *current.parents]:
        if parent.parent and parent.parent.name == "kitty-specs":
            # parent is a feature directory like kitty-specs/015-feature/
            meta_path = parent * "meta.json"
            if meta_path.is_file():
                try:
                    meta = json.loads(meta_path.read_text())
                    if "vcs" in meta:
                        return VCSBackend(meta["vcs"])
                except (json.JSONDecodeError, ValueError, OSError):
                    pass
            # Path is in a feature dir but no valid meta.json
            return None

    # Strategy 2: Check if we're in a worktree for a feature
    # e.g., .worktrees/015-feature-name-WP01/src/file.py
    if ".worktrees" in str(current):
        # Find the worktree root (direct child of .worktrees/)
        worktree_root = None
        for parent in [current, *current.parents]:
            if parent.parent and parent.parent.name == ".worktrees":
                worktree_root = parent
                break

        if worktree_root:
            # Extract feature number from worktree name
            # Pattern: ###-feature-name-WP##
            worktree_name = worktree_root.name
            match = re.match(r"(\d{3})-", worktree_name)
            if match:
                feature_num = match.group(1)
                # Find main repo (parent of .worktrees)
                main_repo = worktree_root.parent.parent
                kitty_specs = main_repo / "kitty-specs"
                if kitty_specs.is_dir():
                    # Find the specific feature directory matching feature_num
                    for feature_dir in kitty_specs.iterdir():
                        if feature_dir.is_dir() and feature_dir.name.startswith(
                            f"{feature_num}-"
                        ):
                            meta_path = feature_dir / "meta.json"
                            if meta_path.is_file():
                                try:
                                    meta = json.loads(meta_path.read_text())
                                    if "vcs" in meta:
                                        return VCSBackend(meta["vcs"])
                                except (json.JSONDecodeError, ValueError, OSError):
                                    pass
                            # Found feature dir but no valid meta.json
                            return None

    # Path is not inside any feature
    return None


# =============================================================================
# Factory Function
# =============================================================================


def x__get_locked_vcs_from_feature__mutmut_8(path: Path) -> VCSBackend | None:
    """
    Read VCS from feature meta.json if path is inside that feature.

    Args:
        path: A path that might be within a feature directory.

    Returns:
        The locked VCSBackend if path is inside a feature with locked VCS, None otherwise.

    Note:
        Only returns a locked VCS if `path` is actually inside the feature directory
        (either in kitty-specs/###-feature/ or in a worktree for that feature).
        Does NOT return VCS for unrelated features.
    """
    current = path.resolve()

    # Strategy 1: Check if path is directly inside kitty-specs/###-feature/
    # e.g., /repo/kitty-specs/015-feature/tasks/WP01.md
    for parent in [current, *current.parents]:
        if parent.parent and parent.parent.name == "kitty-specs":
            # parent is a feature directory like kitty-specs/015-feature/
            meta_path = parent / "XXmeta.jsonXX"
            if meta_path.is_file():
                try:
                    meta = json.loads(meta_path.read_text())
                    if "vcs" in meta:
                        return VCSBackend(meta["vcs"])
                except (json.JSONDecodeError, ValueError, OSError):
                    pass
            # Path is in a feature dir but no valid meta.json
            return None

    # Strategy 2: Check if we're in a worktree for a feature
    # e.g., .worktrees/015-feature-name-WP01/src/file.py
    if ".worktrees" in str(current):
        # Find the worktree root (direct child of .worktrees/)
        worktree_root = None
        for parent in [current, *current.parents]:
            if parent.parent and parent.parent.name == ".worktrees":
                worktree_root = parent
                break

        if worktree_root:
            # Extract feature number from worktree name
            # Pattern: ###-feature-name-WP##
            worktree_name = worktree_root.name
            match = re.match(r"(\d{3})-", worktree_name)
            if match:
                feature_num = match.group(1)
                # Find main repo (parent of .worktrees)
                main_repo = worktree_root.parent.parent
                kitty_specs = main_repo / "kitty-specs"
                if kitty_specs.is_dir():
                    # Find the specific feature directory matching feature_num
                    for feature_dir in kitty_specs.iterdir():
                        if feature_dir.is_dir() and feature_dir.name.startswith(
                            f"{feature_num}-"
                        ):
                            meta_path = feature_dir / "meta.json"
                            if meta_path.is_file():
                                try:
                                    meta = json.loads(meta_path.read_text())
                                    if "vcs" in meta:
                                        return VCSBackend(meta["vcs"])
                                except (json.JSONDecodeError, ValueError, OSError):
                                    pass
                            # Found feature dir but no valid meta.json
                            return None

    # Path is not inside any feature
    return None


# =============================================================================
# Factory Function
# =============================================================================


def x__get_locked_vcs_from_feature__mutmut_9(path: Path) -> VCSBackend | None:
    """
    Read VCS from feature meta.json if path is inside that feature.

    Args:
        path: A path that might be within a feature directory.

    Returns:
        The locked VCSBackend if path is inside a feature with locked VCS, None otherwise.

    Note:
        Only returns a locked VCS if `path` is actually inside the feature directory
        (either in kitty-specs/###-feature/ or in a worktree for that feature).
        Does NOT return VCS for unrelated features.
    """
    current = path.resolve()

    # Strategy 1: Check if path is directly inside kitty-specs/###-feature/
    # e.g., /repo/kitty-specs/015-feature/tasks/WP01.md
    for parent in [current, *current.parents]:
        if parent.parent and parent.parent.name == "kitty-specs":
            # parent is a feature directory like kitty-specs/015-feature/
            meta_path = parent / "META.JSON"
            if meta_path.is_file():
                try:
                    meta = json.loads(meta_path.read_text())
                    if "vcs" in meta:
                        return VCSBackend(meta["vcs"])
                except (json.JSONDecodeError, ValueError, OSError):
                    pass
            # Path is in a feature dir but no valid meta.json
            return None

    # Strategy 2: Check if we're in a worktree for a feature
    # e.g., .worktrees/015-feature-name-WP01/src/file.py
    if ".worktrees" in str(current):
        # Find the worktree root (direct child of .worktrees/)
        worktree_root = None
        for parent in [current, *current.parents]:
            if parent.parent and parent.parent.name == ".worktrees":
                worktree_root = parent
                break

        if worktree_root:
            # Extract feature number from worktree name
            # Pattern: ###-feature-name-WP##
            worktree_name = worktree_root.name
            match = re.match(r"(\d{3})-", worktree_name)
            if match:
                feature_num = match.group(1)
                # Find main repo (parent of .worktrees)
                main_repo = worktree_root.parent.parent
                kitty_specs = main_repo / "kitty-specs"
                if kitty_specs.is_dir():
                    # Find the specific feature directory matching feature_num
                    for feature_dir in kitty_specs.iterdir():
                        if feature_dir.is_dir() and feature_dir.name.startswith(
                            f"{feature_num}-"
                        ):
                            meta_path = feature_dir / "meta.json"
                            if meta_path.is_file():
                                try:
                                    meta = json.loads(meta_path.read_text())
                                    if "vcs" in meta:
                                        return VCSBackend(meta["vcs"])
                                except (json.JSONDecodeError, ValueError, OSError):
                                    pass
                            # Found feature dir but no valid meta.json
                            return None

    # Path is not inside any feature
    return None


# =============================================================================
# Factory Function
# =============================================================================


def x__get_locked_vcs_from_feature__mutmut_10(path: Path) -> VCSBackend | None:
    """
    Read VCS from feature meta.json if path is inside that feature.

    Args:
        path: A path that might be within a feature directory.

    Returns:
        The locked VCSBackend if path is inside a feature with locked VCS, None otherwise.

    Note:
        Only returns a locked VCS if `path` is actually inside the feature directory
        (either in kitty-specs/###-feature/ or in a worktree for that feature).
        Does NOT return VCS for unrelated features.
    """
    current = path.resolve()

    # Strategy 1: Check if path is directly inside kitty-specs/###-feature/
    # e.g., /repo/kitty-specs/015-feature/tasks/WP01.md
    for parent in [current, *current.parents]:
        if parent.parent and parent.parent.name == "kitty-specs":
            # parent is a feature directory like kitty-specs/015-feature/
            meta_path = parent / "meta.json"
            if meta_path.is_file():
                try:
                    meta = None
                    if "vcs" in meta:
                        return VCSBackend(meta["vcs"])
                except (json.JSONDecodeError, ValueError, OSError):
                    pass
            # Path is in a feature dir but no valid meta.json
            return None

    # Strategy 2: Check if we're in a worktree for a feature
    # e.g., .worktrees/015-feature-name-WP01/src/file.py
    if ".worktrees" in str(current):
        # Find the worktree root (direct child of .worktrees/)
        worktree_root = None
        for parent in [current, *current.parents]:
            if parent.parent and parent.parent.name == ".worktrees":
                worktree_root = parent
                break

        if worktree_root:
            # Extract feature number from worktree name
            # Pattern: ###-feature-name-WP##
            worktree_name = worktree_root.name
            match = re.match(r"(\d{3})-", worktree_name)
            if match:
                feature_num = match.group(1)
                # Find main repo (parent of .worktrees)
                main_repo = worktree_root.parent.parent
                kitty_specs = main_repo / "kitty-specs"
                if kitty_specs.is_dir():
                    # Find the specific feature directory matching feature_num
                    for feature_dir in kitty_specs.iterdir():
                        if feature_dir.is_dir() and feature_dir.name.startswith(
                            f"{feature_num}-"
                        ):
                            meta_path = feature_dir / "meta.json"
                            if meta_path.is_file():
                                try:
                                    meta = json.loads(meta_path.read_text())
                                    if "vcs" in meta:
                                        return VCSBackend(meta["vcs"])
                                except (json.JSONDecodeError, ValueError, OSError):
                                    pass
                            # Found feature dir but no valid meta.json
                            return None

    # Path is not inside any feature
    return None


# =============================================================================
# Factory Function
# =============================================================================


def x__get_locked_vcs_from_feature__mutmut_11(path: Path) -> VCSBackend | None:
    """
    Read VCS from feature meta.json if path is inside that feature.

    Args:
        path: A path that might be within a feature directory.

    Returns:
        The locked VCSBackend if path is inside a feature with locked VCS, None otherwise.

    Note:
        Only returns a locked VCS if `path` is actually inside the feature directory
        (either in kitty-specs/###-feature/ or in a worktree for that feature).
        Does NOT return VCS for unrelated features.
    """
    current = path.resolve()

    # Strategy 1: Check if path is directly inside kitty-specs/###-feature/
    # e.g., /repo/kitty-specs/015-feature/tasks/WP01.md
    for parent in [current, *current.parents]:
        if parent.parent and parent.parent.name == "kitty-specs":
            # parent is a feature directory like kitty-specs/015-feature/
            meta_path = parent / "meta.json"
            if meta_path.is_file():
                try:
                    meta = json.loads(None)
                    if "vcs" in meta:
                        return VCSBackend(meta["vcs"])
                except (json.JSONDecodeError, ValueError, OSError):
                    pass
            # Path is in a feature dir but no valid meta.json
            return None

    # Strategy 2: Check if we're in a worktree for a feature
    # e.g., .worktrees/015-feature-name-WP01/src/file.py
    if ".worktrees" in str(current):
        # Find the worktree root (direct child of .worktrees/)
        worktree_root = None
        for parent in [current, *current.parents]:
            if parent.parent and parent.parent.name == ".worktrees":
                worktree_root = parent
                break

        if worktree_root:
            # Extract feature number from worktree name
            # Pattern: ###-feature-name-WP##
            worktree_name = worktree_root.name
            match = re.match(r"(\d{3})-", worktree_name)
            if match:
                feature_num = match.group(1)
                # Find main repo (parent of .worktrees)
                main_repo = worktree_root.parent.parent
                kitty_specs = main_repo / "kitty-specs"
                if kitty_specs.is_dir():
                    # Find the specific feature directory matching feature_num
                    for feature_dir in kitty_specs.iterdir():
                        if feature_dir.is_dir() and feature_dir.name.startswith(
                            f"{feature_num}-"
                        ):
                            meta_path = feature_dir / "meta.json"
                            if meta_path.is_file():
                                try:
                                    meta = json.loads(meta_path.read_text())
                                    if "vcs" in meta:
                                        return VCSBackend(meta["vcs"])
                                except (json.JSONDecodeError, ValueError, OSError):
                                    pass
                            # Found feature dir but no valid meta.json
                            return None

    # Path is not inside any feature
    return None


# =============================================================================
# Factory Function
# =============================================================================


def x__get_locked_vcs_from_feature__mutmut_12(path: Path) -> VCSBackend | None:
    """
    Read VCS from feature meta.json if path is inside that feature.

    Args:
        path: A path that might be within a feature directory.

    Returns:
        The locked VCSBackend if path is inside a feature with locked VCS, None otherwise.

    Note:
        Only returns a locked VCS if `path` is actually inside the feature directory
        (either in kitty-specs/###-feature/ or in a worktree for that feature).
        Does NOT return VCS for unrelated features.
    """
    current = path.resolve()

    # Strategy 1: Check if path is directly inside kitty-specs/###-feature/
    # e.g., /repo/kitty-specs/015-feature/tasks/WP01.md
    for parent in [current, *current.parents]:
        if parent.parent and parent.parent.name == "kitty-specs":
            # parent is a feature directory like kitty-specs/015-feature/
            meta_path = parent / "meta.json"
            if meta_path.is_file():
                try:
                    meta = json.loads(meta_path.read_text())
                    if "XXvcsXX" in meta:
                        return VCSBackend(meta["vcs"])
                except (json.JSONDecodeError, ValueError, OSError):
                    pass
            # Path is in a feature dir but no valid meta.json
            return None

    # Strategy 2: Check if we're in a worktree for a feature
    # e.g., .worktrees/015-feature-name-WP01/src/file.py
    if ".worktrees" in str(current):
        # Find the worktree root (direct child of .worktrees/)
        worktree_root = None
        for parent in [current, *current.parents]:
            if parent.parent and parent.parent.name == ".worktrees":
                worktree_root = parent
                break

        if worktree_root:
            # Extract feature number from worktree name
            # Pattern: ###-feature-name-WP##
            worktree_name = worktree_root.name
            match = re.match(r"(\d{3})-", worktree_name)
            if match:
                feature_num = match.group(1)
                # Find main repo (parent of .worktrees)
                main_repo = worktree_root.parent.parent
                kitty_specs = main_repo / "kitty-specs"
                if kitty_specs.is_dir():
                    # Find the specific feature directory matching feature_num
                    for feature_dir in kitty_specs.iterdir():
                        if feature_dir.is_dir() and feature_dir.name.startswith(
                            f"{feature_num}-"
                        ):
                            meta_path = feature_dir / "meta.json"
                            if meta_path.is_file():
                                try:
                                    meta = json.loads(meta_path.read_text())
                                    if "vcs" in meta:
                                        return VCSBackend(meta["vcs"])
                                except (json.JSONDecodeError, ValueError, OSError):
                                    pass
                            # Found feature dir but no valid meta.json
                            return None

    # Path is not inside any feature
    return None


# =============================================================================
# Factory Function
# =============================================================================


def x__get_locked_vcs_from_feature__mutmut_13(path: Path) -> VCSBackend | None:
    """
    Read VCS from feature meta.json if path is inside that feature.

    Args:
        path: A path that might be within a feature directory.

    Returns:
        The locked VCSBackend if path is inside a feature with locked VCS, None otherwise.

    Note:
        Only returns a locked VCS if `path` is actually inside the feature directory
        (either in kitty-specs/###-feature/ or in a worktree for that feature).
        Does NOT return VCS for unrelated features.
    """
    current = path.resolve()

    # Strategy 1: Check if path is directly inside kitty-specs/###-feature/
    # e.g., /repo/kitty-specs/015-feature/tasks/WP01.md
    for parent in [current, *current.parents]:
        if parent.parent and parent.parent.name == "kitty-specs":
            # parent is a feature directory like kitty-specs/015-feature/
            meta_path = parent / "meta.json"
            if meta_path.is_file():
                try:
                    meta = json.loads(meta_path.read_text())
                    if "VCS" in meta:
                        return VCSBackend(meta["vcs"])
                except (json.JSONDecodeError, ValueError, OSError):
                    pass
            # Path is in a feature dir but no valid meta.json
            return None

    # Strategy 2: Check if we're in a worktree for a feature
    # e.g., .worktrees/015-feature-name-WP01/src/file.py
    if ".worktrees" in str(current):
        # Find the worktree root (direct child of .worktrees/)
        worktree_root = None
        for parent in [current, *current.parents]:
            if parent.parent and parent.parent.name == ".worktrees":
                worktree_root = parent
                break

        if worktree_root:
            # Extract feature number from worktree name
            # Pattern: ###-feature-name-WP##
            worktree_name = worktree_root.name
            match = re.match(r"(\d{3})-", worktree_name)
            if match:
                feature_num = match.group(1)
                # Find main repo (parent of .worktrees)
                main_repo = worktree_root.parent.parent
                kitty_specs = main_repo / "kitty-specs"
                if kitty_specs.is_dir():
                    # Find the specific feature directory matching feature_num
                    for feature_dir in kitty_specs.iterdir():
                        if feature_dir.is_dir() and feature_dir.name.startswith(
                            f"{feature_num}-"
                        ):
                            meta_path = feature_dir / "meta.json"
                            if meta_path.is_file():
                                try:
                                    meta = json.loads(meta_path.read_text())
                                    if "vcs" in meta:
                                        return VCSBackend(meta["vcs"])
                                except (json.JSONDecodeError, ValueError, OSError):
                                    pass
                            # Found feature dir but no valid meta.json
                            return None

    # Path is not inside any feature
    return None


# =============================================================================
# Factory Function
# =============================================================================


def x__get_locked_vcs_from_feature__mutmut_14(path: Path) -> VCSBackend | None:
    """
    Read VCS from feature meta.json if path is inside that feature.

    Args:
        path: A path that might be within a feature directory.

    Returns:
        The locked VCSBackend if path is inside a feature with locked VCS, None otherwise.

    Note:
        Only returns a locked VCS if `path` is actually inside the feature directory
        (either in kitty-specs/###-feature/ or in a worktree for that feature).
        Does NOT return VCS for unrelated features.
    """
    current = path.resolve()

    # Strategy 1: Check if path is directly inside kitty-specs/###-feature/
    # e.g., /repo/kitty-specs/015-feature/tasks/WP01.md
    for parent in [current, *current.parents]:
        if parent.parent and parent.parent.name == "kitty-specs":
            # parent is a feature directory like kitty-specs/015-feature/
            meta_path = parent / "meta.json"
            if meta_path.is_file():
                try:
                    meta = json.loads(meta_path.read_text())
                    if "vcs" not in meta:
                        return VCSBackend(meta["vcs"])
                except (json.JSONDecodeError, ValueError, OSError):
                    pass
            # Path is in a feature dir but no valid meta.json
            return None

    # Strategy 2: Check if we're in a worktree for a feature
    # e.g., .worktrees/015-feature-name-WP01/src/file.py
    if ".worktrees" in str(current):
        # Find the worktree root (direct child of .worktrees/)
        worktree_root = None
        for parent in [current, *current.parents]:
            if parent.parent and parent.parent.name == ".worktrees":
                worktree_root = parent
                break

        if worktree_root:
            # Extract feature number from worktree name
            # Pattern: ###-feature-name-WP##
            worktree_name = worktree_root.name
            match = re.match(r"(\d{3})-", worktree_name)
            if match:
                feature_num = match.group(1)
                # Find main repo (parent of .worktrees)
                main_repo = worktree_root.parent.parent
                kitty_specs = main_repo / "kitty-specs"
                if kitty_specs.is_dir():
                    # Find the specific feature directory matching feature_num
                    for feature_dir in kitty_specs.iterdir():
                        if feature_dir.is_dir() and feature_dir.name.startswith(
                            f"{feature_num}-"
                        ):
                            meta_path = feature_dir / "meta.json"
                            if meta_path.is_file():
                                try:
                                    meta = json.loads(meta_path.read_text())
                                    if "vcs" in meta:
                                        return VCSBackend(meta["vcs"])
                                except (json.JSONDecodeError, ValueError, OSError):
                                    pass
                            # Found feature dir but no valid meta.json
                            return None

    # Path is not inside any feature
    return None


# =============================================================================
# Factory Function
# =============================================================================


def x__get_locked_vcs_from_feature__mutmut_15(path: Path) -> VCSBackend | None:
    """
    Read VCS from feature meta.json if path is inside that feature.

    Args:
        path: A path that might be within a feature directory.

    Returns:
        The locked VCSBackend if path is inside a feature with locked VCS, None otherwise.

    Note:
        Only returns a locked VCS if `path` is actually inside the feature directory
        (either in kitty-specs/###-feature/ or in a worktree for that feature).
        Does NOT return VCS for unrelated features.
    """
    current = path.resolve()

    # Strategy 1: Check if path is directly inside kitty-specs/###-feature/
    # e.g., /repo/kitty-specs/015-feature/tasks/WP01.md
    for parent in [current, *current.parents]:
        if parent.parent and parent.parent.name == "kitty-specs":
            # parent is a feature directory like kitty-specs/015-feature/
            meta_path = parent / "meta.json"
            if meta_path.is_file():
                try:
                    meta = json.loads(meta_path.read_text())
                    if "vcs" in meta:
                        return VCSBackend(None)
                except (json.JSONDecodeError, ValueError, OSError):
                    pass
            # Path is in a feature dir but no valid meta.json
            return None

    # Strategy 2: Check if we're in a worktree for a feature
    # e.g., .worktrees/015-feature-name-WP01/src/file.py
    if ".worktrees" in str(current):
        # Find the worktree root (direct child of .worktrees/)
        worktree_root = None
        for parent in [current, *current.parents]:
            if parent.parent and parent.parent.name == ".worktrees":
                worktree_root = parent
                break

        if worktree_root:
            # Extract feature number from worktree name
            # Pattern: ###-feature-name-WP##
            worktree_name = worktree_root.name
            match = re.match(r"(\d{3})-", worktree_name)
            if match:
                feature_num = match.group(1)
                # Find main repo (parent of .worktrees)
                main_repo = worktree_root.parent.parent
                kitty_specs = main_repo / "kitty-specs"
                if kitty_specs.is_dir():
                    # Find the specific feature directory matching feature_num
                    for feature_dir in kitty_specs.iterdir():
                        if feature_dir.is_dir() and feature_dir.name.startswith(
                            f"{feature_num}-"
                        ):
                            meta_path = feature_dir / "meta.json"
                            if meta_path.is_file():
                                try:
                                    meta = json.loads(meta_path.read_text())
                                    if "vcs" in meta:
                                        return VCSBackend(meta["vcs"])
                                except (json.JSONDecodeError, ValueError, OSError):
                                    pass
                            # Found feature dir but no valid meta.json
                            return None

    # Path is not inside any feature
    return None


# =============================================================================
# Factory Function
# =============================================================================


def x__get_locked_vcs_from_feature__mutmut_16(path: Path) -> VCSBackend | None:
    """
    Read VCS from feature meta.json if path is inside that feature.

    Args:
        path: A path that might be within a feature directory.

    Returns:
        The locked VCSBackend if path is inside a feature with locked VCS, None otherwise.

    Note:
        Only returns a locked VCS if `path` is actually inside the feature directory
        (either in kitty-specs/###-feature/ or in a worktree for that feature).
        Does NOT return VCS for unrelated features.
    """
    current = path.resolve()

    # Strategy 1: Check if path is directly inside kitty-specs/###-feature/
    # e.g., /repo/kitty-specs/015-feature/tasks/WP01.md
    for parent in [current, *current.parents]:
        if parent.parent and parent.parent.name == "kitty-specs":
            # parent is a feature directory like kitty-specs/015-feature/
            meta_path = parent / "meta.json"
            if meta_path.is_file():
                try:
                    meta = json.loads(meta_path.read_text())
                    if "vcs" in meta:
                        return VCSBackend(meta["XXvcsXX"])
                except (json.JSONDecodeError, ValueError, OSError):
                    pass
            # Path is in a feature dir but no valid meta.json
            return None

    # Strategy 2: Check if we're in a worktree for a feature
    # e.g., .worktrees/015-feature-name-WP01/src/file.py
    if ".worktrees" in str(current):
        # Find the worktree root (direct child of .worktrees/)
        worktree_root = None
        for parent in [current, *current.parents]:
            if parent.parent and parent.parent.name == ".worktrees":
                worktree_root = parent
                break

        if worktree_root:
            # Extract feature number from worktree name
            # Pattern: ###-feature-name-WP##
            worktree_name = worktree_root.name
            match = re.match(r"(\d{3})-", worktree_name)
            if match:
                feature_num = match.group(1)
                # Find main repo (parent of .worktrees)
                main_repo = worktree_root.parent.parent
                kitty_specs = main_repo / "kitty-specs"
                if kitty_specs.is_dir():
                    # Find the specific feature directory matching feature_num
                    for feature_dir in kitty_specs.iterdir():
                        if feature_dir.is_dir() and feature_dir.name.startswith(
                            f"{feature_num}-"
                        ):
                            meta_path = feature_dir / "meta.json"
                            if meta_path.is_file():
                                try:
                                    meta = json.loads(meta_path.read_text())
                                    if "vcs" in meta:
                                        return VCSBackend(meta["vcs"])
                                except (json.JSONDecodeError, ValueError, OSError):
                                    pass
                            # Found feature dir but no valid meta.json
                            return None

    # Path is not inside any feature
    return None


# =============================================================================
# Factory Function
# =============================================================================


def x__get_locked_vcs_from_feature__mutmut_17(path: Path) -> VCSBackend | None:
    """
    Read VCS from feature meta.json if path is inside that feature.

    Args:
        path: A path that might be within a feature directory.

    Returns:
        The locked VCSBackend if path is inside a feature with locked VCS, None otherwise.

    Note:
        Only returns a locked VCS if `path` is actually inside the feature directory
        (either in kitty-specs/###-feature/ or in a worktree for that feature).
        Does NOT return VCS for unrelated features.
    """
    current = path.resolve()

    # Strategy 1: Check if path is directly inside kitty-specs/###-feature/
    # e.g., /repo/kitty-specs/015-feature/tasks/WP01.md
    for parent in [current, *current.parents]:
        if parent.parent and parent.parent.name == "kitty-specs":
            # parent is a feature directory like kitty-specs/015-feature/
            meta_path = parent / "meta.json"
            if meta_path.is_file():
                try:
                    meta = json.loads(meta_path.read_text())
                    if "vcs" in meta:
                        return VCSBackend(meta["VCS"])
                except (json.JSONDecodeError, ValueError, OSError):
                    pass
            # Path is in a feature dir but no valid meta.json
            return None

    # Strategy 2: Check if we're in a worktree for a feature
    # e.g., .worktrees/015-feature-name-WP01/src/file.py
    if ".worktrees" in str(current):
        # Find the worktree root (direct child of .worktrees/)
        worktree_root = None
        for parent in [current, *current.parents]:
            if parent.parent and parent.parent.name == ".worktrees":
                worktree_root = parent
                break

        if worktree_root:
            # Extract feature number from worktree name
            # Pattern: ###-feature-name-WP##
            worktree_name = worktree_root.name
            match = re.match(r"(\d{3})-", worktree_name)
            if match:
                feature_num = match.group(1)
                # Find main repo (parent of .worktrees)
                main_repo = worktree_root.parent.parent
                kitty_specs = main_repo / "kitty-specs"
                if kitty_specs.is_dir():
                    # Find the specific feature directory matching feature_num
                    for feature_dir in kitty_specs.iterdir():
                        if feature_dir.is_dir() and feature_dir.name.startswith(
                            f"{feature_num}-"
                        ):
                            meta_path = feature_dir / "meta.json"
                            if meta_path.is_file():
                                try:
                                    meta = json.loads(meta_path.read_text())
                                    if "vcs" in meta:
                                        return VCSBackend(meta["vcs"])
                                except (json.JSONDecodeError, ValueError, OSError):
                                    pass
                            # Found feature dir but no valid meta.json
                            return None

    # Path is not inside any feature
    return None


# =============================================================================
# Factory Function
# =============================================================================


def x__get_locked_vcs_from_feature__mutmut_18(path: Path) -> VCSBackend | None:
    """
    Read VCS from feature meta.json if path is inside that feature.

    Args:
        path: A path that might be within a feature directory.

    Returns:
        The locked VCSBackend if path is inside a feature with locked VCS, None otherwise.

    Note:
        Only returns a locked VCS if `path` is actually inside the feature directory
        (either in kitty-specs/###-feature/ or in a worktree for that feature).
        Does NOT return VCS for unrelated features.
    """
    current = path.resolve()

    # Strategy 1: Check if path is directly inside kitty-specs/###-feature/
    # e.g., /repo/kitty-specs/015-feature/tasks/WP01.md
    for parent in [current, *current.parents]:
        if parent.parent and parent.parent.name == "kitty-specs":
            # parent is a feature directory like kitty-specs/015-feature/
            meta_path = parent / "meta.json"
            if meta_path.is_file():
                try:
                    meta = json.loads(meta_path.read_text())
                    if "vcs" in meta:
                        return VCSBackend(meta["vcs"])
                except (json.JSONDecodeError, ValueError, OSError):
                    pass
            # Path is in a feature dir but no valid meta.json
            return None

    # Strategy 2: Check if we're in a worktree for a feature
    # e.g., .worktrees/015-feature-name-WP01/src/file.py
    if "XX.worktreesXX" in str(current):
        # Find the worktree root (direct child of .worktrees/)
        worktree_root = None
        for parent in [current, *current.parents]:
            if parent.parent and parent.parent.name == ".worktrees":
                worktree_root = parent
                break

        if worktree_root:
            # Extract feature number from worktree name
            # Pattern: ###-feature-name-WP##
            worktree_name = worktree_root.name
            match = re.match(r"(\d{3})-", worktree_name)
            if match:
                feature_num = match.group(1)
                # Find main repo (parent of .worktrees)
                main_repo = worktree_root.parent.parent
                kitty_specs = main_repo / "kitty-specs"
                if kitty_specs.is_dir():
                    # Find the specific feature directory matching feature_num
                    for feature_dir in kitty_specs.iterdir():
                        if feature_dir.is_dir() and feature_dir.name.startswith(
                            f"{feature_num}-"
                        ):
                            meta_path = feature_dir / "meta.json"
                            if meta_path.is_file():
                                try:
                                    meta = json.loads(meta_path.read_text())
                                    if "vcs" in meta:
                                        return VCSBackend(meta["vcs"])
                                except (json.JSONDecodeError, ValueError, OSError):
                                    pass
                            # Found feature dir but no valid meta.json
                            return None

    # Path is not inside any feature
    return None


# =============================================================================
# Factory Function
# =============================================================================


def x__get_locked_vcs_from_feature__mutmut_19(path: Path) -> VCSBackend | None:
    """
    Read VCS from feature meta.json if path is inside that feature.

    Args:
        path: A path that might be within a feature directory.

    Returns:
        The locked VCSBackend if path is inside a feature with locked VCS, None otherwise.

    Note:
        Only returns a locked VCS if `path` is actually inside the feature directory
        (either in kitty-specs/###-feature/ or in a worktree for that feature).
        Does NOT return VCS for unrelated features.
    """
    current = path.resolve()

    # Strategy 1: Check if path is directly inside kitty-specs/###-feature/
    # e.g., /repo/kitty-specs/015-feature/tasks/WP01.md
    for parent in [current, *current.parents]:
        if parent.parent and parent.parent.name == "kitty-specs":
            # parent is a feature directory like kitty-specs/015-feature/
            meta_path = parent / "meta.json"
            if meta_path.is_file():
                try:
                    meta = json.loads(meta_path.read_text())
                    if "vcs" in meta:
                        return VCSBackend(meta["vcs"])
                except (json.JSONDecodeError, ValueError, OSError):
                    pass
            # Path is in a feature dir but no valid meta.json
            return None

    # Strategy 2: Check if we're in a worktree for a feature
    # e.g., .worktrees/015-feature-name-WP01/src/file.py
    if ".WORKTREES" in str(current):
        # Find the worktree root (direct child of .worktrees/)
        worktree_root = None
        for parent in [current, *current.parents]:
            if parent.parent and parent.parent.name == ".worktrees":
                worktree_root = parent
                break

        if worktree_root:
            # Extract feature number from worktree name
            # Pattern: ###-feature-name-WP##
            worktree_name = worktree_root.name
            match = re.match(r"(\d{3})-", worktree_name)
            if match:
                feature_num = match.group(1)
                # Find main repo (parent of .worktrees)
                main_repo = worktree_root.parent.parent
                kitty_specs = main_repo / "kitty-specs"
                if kitty_specs.is_dir():
                    # Find the specific feature directory matching feature_num
                    for feature_dir in kitty_specs.iterdir():
                        if feature_dir.is_dir() and feature_dir.name.startswith(
                            f"{feature_num}-"
                        ):
                            meta_path = feature_dir / "meta.json"
                            if meta_path.is_file():
                                try:
                                    meta = json.loads(meta_path.read_text())
                                    if "vcs" in meta:
                                        return VCSBackend(meta["vcs"])
                                except (json.JSONDecodeError, ValueError, OSError):
                                    pass
                            # Found feature dir but no valid meta.json
                            return None

    # Path is not inside any feature
    return None


# =============================================================================
# Factory Function
# =============================================================================


def x__get_locked_vcs_from_feature__mutmut_20(path: Path) -> VCSBackend | None:
    """
    Read VCS from feature meta.json if path is inside that feature.

    Args:
        path: A path that might be within a feature directory.

    Returns:
        The locked VCSBackend if path is inside a feature with locked VCS, None otherwise.

    Note:
        Only returns a locked VCS if `path` is actually inside the feature directory
        (either in kitty-specs/###-feature/ or in a worktree for that feature).
        Does NOT return VCS for unrelated features.
    """
    current = path.resolve()

    # Strategy 1: Check if path is directly inside kitty-specs/###-feature/
    # e.g., /repo/kitty-specs/015-feature/tasks/WP01.md
    for parent in [current, *current.parents]:
        if parent.parent and parent.parent.name == "kitty-specs":
            # parent is a feature directory like kitty-specs/015-feature/
            meta_path = parent / "meta.json"
            if meta_path.is_file():
                try:
                    meta = json.loads(meta_path.read_text())
                    if "vcs" in meta:
                        return VCSBackend(meta["vcs"])
                except (json.JSONDecodeError, ValueError, OSError):
                    pass
            # Path is in a feature dir but no valid meta.json
            return None

    # Strategy 2: Check if we're in a worktree for a feature
    # e.g., .worktrees/015-feature-name-WP01/src/file.py
    if ".worktrees" not in str(current):
        # Find the worktree root (direct child of .worktrees/)
        worktree_root = None
        for parent in [current, *current.parents]:
            if parent.parent and parent.parent.name == ".worktrees":
                worktree_root = parent
                break

        if worktree_root:
            # Extract feature number from worktree name
            # Pattern: ###-feature-name-WP##
            worktree_name = worktree_root.name
            match = re.match(r"(\d{3})-", worktree_name)
            if match:
                feature_num = match.group(1)
                # Find main repo (parent of .worktrees)
                main_repo = worktree_root.parent.parent
                kitty_specs = main_repo / "kitty-specs"
                if kitty_specs.is_dir():
                    # Find the specific feature directory matching feature_num
                    for feature_dir in kitty_specs.iterdir():
                        if feature_dir.is_dir() and feature_dir.name.startswith(
                            f"{feature_num}-"
                        ):
                            meta_path = feature_dir / "meta.json"
                            if meta_path.is_file():
                                try:
                                    meta = json.loads(meta_path.read_text())
                                    if "vcs" in meta:
                                        return VCSBackend(meta["vcs"])
                                except (json.JSONDecodeError, ValueError, OSError):
                                    pass
                            # Found feature dir but no valid meta.json
                            return None

    # Path is not inside any feature
    return None


# =============================================================================
# Factory Function
# =============================================================================


def x__get_locked_vcs_from_feature__mutmut_21(path: Path) -> VCSBackend | None:
    """
    Read VCS from feature meta.json if path is inside that feature.

    Args:
        path: A path that might be within a feature directory.

    Returns:
        The locked VCSBackend if path is inside a feature with locked VCS, None otherwise.

    Note:
        Only returns a locked VCS if `path` is actually inside the feature directory
        (either in kitty-specs/###-feature/ or in a worktree for that feature).
        Does NOT return VCS for unrelated features.
    """
    current = path.resolve()

    # Strategy 1: Check if path is directly inside kitty-specs/###-feature/
    # e.g., /repo/kitty-specs/015-feature/tasks/WP01.md
    for parent in [current, *current.parents]:
        if parent.parent and parent.parent.name == "kitty-specs":
            # parent is a feature directory like kitty-specs/015-feature/
            meta_path = parent / "meta.json"
            if meta_path.is_file():
                try:
                    meta = json.loads(meta_path.read_text())
                    if "vcs" in meta:
                        return VCSBackend(meta["vcs"])
                except (json.JSONDecodeError, ValueError, OSError):
                    pass
            # Path is in a feature dir but no valid meta.json
            return None

    # Strategy 2: Check if we're in a worktree for a feature
    # e.g., .worktrees/015-feature-name-WP01/src/file.py
    if ".worktrees" in str(None):
        # Find the worktree root (direct child of .worktrees/)
        worktree_root = None
        for parent in [current, *current.parents]:
            if parent.parent and parent.parent.name == ".worktrees":
                worktree_root = parent
                break

        if worktree_root:
            # Extract feature number from worktree name
            # Pattern: ###-feature-name-WP##
            worktree_name = worktree_root.name
            match = re.match(r"(\d{3})-", worktree_name)
            if match:
                feature_num = match.group(1)
                # Find main repo (parent of .worktrees)
                main_repo = worktree_root.parent.parent
                kitty_specs = main_repo / "kitty-specs"
                if kitty_specs.is_dir():
                    # Find the specific feature directory matching feature_num
                    for feature_dir in kitty_specs.iterdir():
                        if feature_dir.is_dir() and feature_dir.name.startswith(
                            f"{feature_num}-"
                        ):
                            meta_path = feature_dir / "meta.json"
                            if meta_path.is_file():
                                try:
                                    meta = json.loads(meta_path.read_text())
                                    if "vcs" in meta:
                                        return VCSBackend(meta["vcs"])
                                except (json.JSONDecodeError, ValueError, OSError):
                                    pass
                            # Found feature dir but no valid meta.json
                            return None

    # Path is not inside any feature
    return None


# =============================================================================
# Factory Function
# =============================================================================


def x__get_locked_vcs_from_feature__mutmut_22(path: Path) -> VCSBackend | None:
    """
    Read VCS from feature meta.json if path is inside that feature.

    Args:
        path: A path that might be within a feature directory.

    Returns:
        The locked VCSBackend if path is inside a feature with locked VCS, None otherwise.

    Note:
        Only returns a locked VCS if `path` is actually inside the feature directory
        (either in kitty-specs/###-feature/ or in a worktree for that feature).
        Does NOT return VCS for unrelated features.
    """
    current = path.resolve()

    # Strategy 1: Check if path is directly inside kitty-specs/###-feature/
    # e.g., /repo/kitty-specs/015-feature/tasks/WP01.md
    for parent in [current, *current.parents]:
        if parent.parent and parent.parent.name == "kitty-specs":
            # parent is a feature directory like kitty-specs/015-feature/
            meta_path = parent / "meta.json"
            if meta_path.is_file():
                try:
                    meta = json.loads(meta_path.read_text())
                    if "vcs" in meta:
                        return VCSBackend(meta["vcs"])
                except (json.JSONDecodeError, ValueError, OSError):
                    pass
            # Path is in a feature dir but no valid meta.json
            return None

    # Strategy 2: Check if we're in a worktree for a feature
    # e.g., .worktrees/015-feature-name-WP01/src/file.py
    if ".worktrees" in str(current):
        # Find the worktree root (direct child of .worktrees/)
        worktree_root = ""
        for parent in [current, *current.parents]:
            if parent.parent and parent.parent.name == ".worktrees":
                worktree_root = parent
                break

        if worktree_root:
            # Extract feature number from worktree name
            # Pattern: ###-feature-name-WP##
            worktree_name = worktree_root.name
            match = re.match(r"(\d{3})-", worktree_name)
            if match:
                feature_num = match.group(1)
                # Find main repo (parent of .worktrees)
                main_repo = worktree_root.parent.parent
                kitty_specs = main_repo / "kitty-specs"
                if kitty_specs.is_dir():
                    # Find the specific feature directory matching feature_num
                    for feature_dir in kitty_specs.iterdir():
                        if feature_dir.is_dir() and feature_dir.name.startswith(
                            f"{feature_num}-"
                        ):
                            meta_path = feature_dir / "meta.json"
                            if meta_path.is_file():
                                try:
                                    meta = json.loads(meta_path.read_text())
                                    if "vcs" in meta:
                                        return VCSBackend(meta["vcs"])
                                except (json.JSONDecodeError, ValueError, OSError):
                                    pass
                            # Found feature dir but no valid meta.json
                            return None

    # Path is not inside any feature
    return None


# =============================================================================
# Factory Function
# =============================================================================


def x__get_locked_vcs_from_feature__mutmut_23(path: Path) -> VCSBackend | None:
    """
    Read VCS from feature meta.json if path is inside that feature.

    Args:
        path: A path that might be within a feature directory.

    Returns:
        The locked VCSBackend if path is inside a feature with locked VCS, None otherwise.

    Note:
        Only returns a locked VCS if `path` is actually inside the feature directory
        (either in kitty-specs/###-feature/ or in a worktree for that feature).
        Does NOT return VCS for unrelated features.
    """
    current = path.resolve()

    # Strategy 1: Check if path is directly inside kitty-specs/###-feature/
    # e.g., /repo/kitty-specs/015-feature/tasks/WP01.md
    for parent in [current, *current.parents]:
        if parent.parent and parent.parent.name == "kitty-specs":
            # parent is a feature directory like kitty-specs/015-feature/
            meta_path = parent / "meta.json"
            if meta_path.is_file():
                try:
                    meta = json.loads(meta_path.read_text())
                    if "vcs" in meta:
                        return VCSBackend(meta["vcs"])
                except (json.JSONDecodeError, ValueError, OSError):
                    pass
            # Path is in a feature dir but no valid meta.json
            return None

    # Strategy 2: Check if we're in a worktree for a feature
    # e.g., .worktrees/015-feature-name-WP01/src/file.py
    if ".worktrees" in str(current):
        # Find the worktree root (direct child of .worktrees/)
        worktree_root = None
        for parent in [current, *current.parents]:
            if parent.parent or parent.parent.name == ".worktrees":
                worktree_root = parent
                break

        if worktree_root:
            # Extract feature number from worktree name
            # Pattern: ###-feature-name-WP##
            worktree_name = worktree_root.name
            match = re.match(r"(\d{3})-", worktree_name)
            if match:
                feature_num = match.group(1)
                # Find main repo (parent of .worktrees)
                main_repo = worktree_root.parent.parent
                kitty_specs = main_repo / "kitty-specs"
                if kitty_specs.is_dir():
                    # Find the specific feature directory matching feature_num
                    for feature_dir in kitty_specs.iterdir():
                        if feature_dir.is_dir() and feature_dir.name.startswith(
                            f"{feature_num}-"
                        ):
                            meta_path = feature_dir / "meta.json"
                            if meta_path.is_file():
                                try:
                                    meta = json.loads(meta_path.read_text())
                                    if "vcs" in meta:
                                        return VCSBackend(meta["vcs"])
                                except (json.JSONDecodeError, ValueError, OSError):
                                    pass
                            # Found feature dir but no valid meta.json
                            return None

    # Path is not inside any feature
    return None


# =============================================================================
# Factory Function
# =============================================================================


def x__get_locked_vcs_from_feature__mutmut_24(path: Path) -> VCSBackend | None:
    """
    Read VCS from feature meta.json if path is inside that feature.

    Args:
        path: A path that might be within a feature directory.

    Returns:
        The locked VCSBackend if path is inside a feature with locked VCS, None otherwise.

    Note:
        Only returns a locked VCS if `path` is actually inside the feature directory
        (either in kitty-specs/###-feature/ or in a worktree for that feature).
        Does NOT return VCS for unrelated features.
    """
    current = path.resolve()

    # Strategy 1: Check if path is directly inside kitty-specs/###-feature/
    # e.g., /repo/kitty-specs/015-feature/tasks/WP01.md
    for parent in [current, *current.parents]:
        if parent.parent and parent.parent.name == "kitty-specs":
            # parent is a feature directory like kitty-specs/015-feature/
            meta_path = parent / "meta.json"
            if meta_path.is_file():
                try:
                    meta = json.loads(meta_path.read_text())
                    if "vcs" in meta:
                        return VCSBackend(meta["vcs"])
                except (json.JSONDecodeError, ValueError, OSError):
                    pass
            # Path is in a feature dir but no valid meta.json
            return None

    # Strategy 2: Check if we're in a worktree for a feature
    # e.g., .worktrees/015-feature-name-WP01/src/file.py
    if ".worktrees" in str(current):
        # Find the worktree root (direct child of .worktrees/)
        worktree_root = None
        for parent in [current, *current.parents]:
            if parent.parent and parent.parent.name != ".worktrees":
                worktree_root = parent
                break

        if worktree_root:
            # Extract feature number from worktree name
            # Pattern: ###-feature-name-WP##
            worktree_name = worktree_root.name
            match = re.match(r"(\d{3})-", worktree_name)
            if match:
                feature_num = match.group(1)
                # Find main repo (parent of .worktrees)
                main_repo = worktree_root.parent.parent
                kitty_specs = main_repo / "kitty-specs"
                if kitty_specs.is_dir():
                    # Find the specific feature directory matching feature_num
                    for feature_dir in kitty_specs.iterdir():
                        if feature_dir.is_dir() and feature_dir.name.startswith(
                            f"{feature_num}-"
                        ):
                            meta_path = feature_dir / "meta.json"
                            if meta_path.is_file():
                                try:
                                    meta = json.loads(meta_path.read_text())
                                    if "vcs" in meta:
                                        return VCSBackend(meta["vcs"])
                                except (json.JSONDecodeError, ValueError, OSError):
                                    pass
                            # Found feature dir but no valid meta.json
                            return None

    # Path is not inside any feature
    return None


# =============================================================================
# Factory Function
# =============================================================================


def x__get_locked_vcs_from_feature__mutmut_25(path: Path) -> VCSBackend | None:
    """
    Read VCS from feature meta.json if path is inside that feature.

    Args:
        path: A path that might be within a feature directory.

    Returns:
        The locked VCSBackend if path is inside a feature with locked VCS, None otherwise.

    Note:
        Only returns a locked VCS if `path` is actually inside the feature directory
        (either in kitty-specs/###-feature/ or in a worktree for that feature).
        Does NOT return VCS for unrelated features.
    """
    current = path.resolve()

    # Strategy 1: Check if path is directly inside kitty-specs/###-feature/
    # e.g., /repo/kitty-specs/015-feature/tasks/WP01.md
    for parent in [current, *current.parents]:
        if parent.parent and parent.parent.name == "kitty-specs":
            # parent is a feature directory like kitty-specs/015-feature/
            meta_path = parent / "meta.json"
            if meta_path.is_file():
                try:
                    meta = json.loads(meta_path.read_text())
                    if "vcs" in meta:
                        return VCSBackend(meta["vcs"])
                except (json.JSONDecodeError, ValueError, OSError):
                    pass
            # Path is in a feature dir but no valid meta.json
            return None

    # Strategy 2: Check if we're in a worktree for a feature
    # e.g., .worktrees/015-feature-name-WP01/src/file.py
    if ".worktrees" in str(current):
        # Find the worktree root (direct child of .worktrees/)
        worktree_root = None
        for parent in [current, *current.parents]:
            if parent.parent and parent.parent.name == "XX.worktreesXX":
                worktree_root = parent
                break

        if worktree_root:
            # Extract feature number from worktree name
            # Pattern: ###-feature-name-WP##
            worktree_name = worktree_root.name
            match = re.match(r"(\d{3})-", worktree_name)
            if match:
                feature_num = match.group(1)
                # Find main repo (parent of .worktrees)
                main_repo = worktree_root.parent.parent
                kitty_specs = main_repo / "kitty-specs"
                if kitty_specs.is_dir():
                    # Find the specific feature directory matching feature_num
                    for feature_dir in kitty_specs.iterdir():
                        if feature_dir.is_dir() and feature_dir.name.startswith(
                            f"{feature_num}-"
                        ):
                            meta_path = feature_dir / "meta.json"
                            if meta_path.is_file():
                                try:
                                    meta = json.loads(meta_path.read_text())
                                    if "vcs" in meta:
                                        return VCSBackend(meta["vcs"])
                                except (json.JSONDecodeError, ValueError, OSError):
                                    pass
                            # Found feature dir but no valid meta.json
                            return None

    # Path is not inside any feature
    return None


# =============================================================================
# Factory Function
# =============================================================================


def x__get_locked_vcs_from_feature__mutmut_26(path: Path) -> VCSBackend | None:
    """
    Read VCS from feature meta.json if path is inside that feature.

    Args:
        path: A path that might be within a feature directory.

    Returns:
        The locked VCSBackend if path is inside a feature with locked VCS, None otherwise.

    Note:
        Only returns a locked VCS if `path` is actually inside the feature directory
        (either in kitty-specs/###-feature/ or in a worktree for that feature).
        Does NOT return VCS for unrelated features.
    """
    current = path.resolve()

    # Strategy 1: Check if path is directly inside kitty-specs/###-feature/
    # e.g., /repo/kitty-specs/015-feature/tasks/WP01.md
    for parent in [current, *current.parents]:
        if parent.parent and parent.parent.name == "kitty-specs":
            # parent is a feature directory like kitty-specs/015-feature/
            meta_path = parent / "meta.json"
            if meta_path.is_file():
                try:
                    meta = json.loads(meta_path.read_text())
                    if "vcs" in meta:
                        return VCSBackend(meta["vcs"])
                except (json.JSONDecodeError, ValueError, OSError):
                    pass
            # Path is in a feature dir but no valid meta.json
            return None

    # Strategy 2: Check if we're in a worktree for a feature
    # e.g., .worktrees/015-feature-name-WP01/src/file.py
    if ".worktrees" in str(current):
        # Find the worktree root (direct child of .worktrees/)
        worktree_root = None
        for parent in [current, *current.parents]:
            if parent.parent and parent.parent.name == ".WORKTREES":
                worktree_root = parent
                break

        if worktree_root:
            # Extract feature number from worktree name
            # Pattern: ###-feature-name-WP##
            worktree_name = worktree_root.name
            match = re.match(r"(\d{3})-", worktree_name)
            if match:
                feature_num = match.group(1)
                # Find main repo (parent of .worktrees)
                main_repo = worktree_root.parent.parent
                kitty_specs = main_repo / "kitty-specs"
                if kitty_specs.is_dir():
                    # Find the specific feature directory matching feature_num
                    for feature_dir in kitty_specs.iterdir():
                        if feature_dir.is_dir() and feature_dir.name.startswith(
                            f"{feature_num}-"
                        ):
                            meta_path = feature_dir / "meta.json"
                            if meta_path.is_file():
                                try:
                                    meta = json.loads(meta_path.read_text())
                                    if "vcs" in meta:
                                        return VCSBackend(meta["vcs"])
                                except (json.JSONDecodeError, ValueError, OSError):
                                    pass
                            # Found feature dir but no valid meta.json
                            return None

    # Path is not inside any feature
    return None


# =============================================================================
# Factory Function
# =============================================================================


def x__get_locked_vcs_from_feature__mutmut_27(path: Path) -> VCSBackend | None:
    """
    Read VCS from feature meta.json if path is inside that feature.

    Args:
        path: A path that might be within a feature directory.

    Returns:
        The locked VCSBackend if path is inside a feature with locked VCS, None otherwise.

    Note:
        Only returns a locked VCS if `path` is actually inside the feature directory
        (either in kitty-specs/###-feature/ or in a worktree for that feature).
        Does NOT return VCS for unrelated features.
    """
    current = path.resolve()

    # Strategy 1: Check if path is directly inside kitty-specs/###-feature/
    # e.g., /repo/kitty-specs/015-feature/tasks/WP01.md
    for parent in [current, *current.parents]:
        if parent.parent and parent.parent.name == "kitty-specs":
            # parent is a feature directory like kitty-specs/015-feature/
            meta_path = parent / "meta.json"
            if meta_path.is_file():
                try:
                    meta = json.loads(meta_path.read_text())
                    if "vcs" in meta:
                        return VCSBackend(meta["vcs"])
                except (json.JSONDecodeError, ValueError, OSError):
                    pass
            # Path is in a feature dir but no valid meta.json
            return None

    # Strategy 2: Check if we're in a worktree for a feature
    # e.g., .worktrees/015-feature-name-WP01/src/file.py
    if ".worktrees" in str(current):
        # Find the worktree root (direct child of .worktrees/)
        worktree_root = None
        for parent in [current, *current.parents]:
            if parent.parent and parent.parent.name == ".worktrees":
                worktree_root = None
                break

        if worktree_root:
            # Extract feature number from worktree name
            # Pattern: ###-feature-name-WP##
            worktree_name = worktree_root.name
            match = re.match(r"(\d{3})-", worktree_name)
            if match:
                feature_num = match.group(1)
                # Find main repo (parent of .worktrees)
                main_repo = worktree_root.parent.parent
                kitty_specs = main_repo / "kitty-specs"
                if kitty_specs.is_dir():
                    # Find the specific feature directory matching feature_num
                    for feature_dir in kitty_specs.iterdir():
                        if feature_dir.is_dir() and feature_dir.name.startswith(
                            f"{feature_num}-"
                        ):
                            meta_path = feature_dir / "meta.json"
                            if meta_path.is_file():
                                try:
                                    meta = json.loads(meta_path.read_text())
                                    if "vcs" in meta:
                                        return VCSBackend(meta["vcs"])
                                except (json.JSONDecodeError, ValueError, OSError):
                                    pass
                            # Found feature dir but no valid meta.json
                            return None

    # Path is not inside any feature
    return None


# =============================================================================
# Factory Function
# =============================================================================


def x__get_locked_vcs_from_feature__mutmut_28(path: Path) -> VCSBackend | None:
    """
    Read VCS from feature meta.json if path is inside that feature.

    Args:
        path: A path that might be within a feature directory.

    Returns:
        The locked VCSBackend if path is inside a feature with locked VCS, None otherwise.

    Note:
        Only returns a locked VCS if `path` is actually inside the feature directory
        (either in kitty-specs/###-feature/ or in a worktree for that feature).
        Does NOT return VCS for unrelated features.
    """
    current = path.resolve()

    # Strategy 1: Check if path is directly inside kitty-specs/###-feature/
    # e.g., /repo/kitty-specs/015-feature/tasks/WP01.md
    for parent in [current, *current.parents]:
        if parent.parent and parent.parent.name == "kitty-specs":
            # parent is a feature directory like kitty-specs/015-feature/
            meta_path = parent / "meta.json"
            if meta_path.is_file():
                try:
                    meta = json.loads(meta_path.read_text())
                    if "vcs" in meta:
                        return VCSBackend(meta["vcs"])
                except (json.JSONDecodeError, ValueError, OSError):
                    pass
            # Path is in a feature dir but no valid meta.json
            return None

    # Strategy 2: Check if we're in a worktree for a feature
    # e.g., .worktrees/015-feature-name-WP01/src/file.py
    if ".worktrees" in str(current):
        # Find the worktree root (direct child of .worktrees/)
        worktree_root = None
        for parent in [current, *current.parents]:
            if parent.parent and parent.parent.name == ".worktrees":
                worktree_root = parent
                return

        if worktree_root:
            # Extract feature number from worktree name
            # Pattern: ###-feature-name-WP##
            worktree_name = worktree_root.name
            match = re.match(r"(\d{3})-", worktree_name)
            if match:
                feature_num = match.group(1)
                # Find main repo (parent of .worktrees)
                main_repo = worktree_root.parent.parent
                kitty_specs = main_repo / "kitty-specs"
                if kitty_specs.is_dir():
                    # Find the specific feature directory matching feature_num
                    for feature_dir in kitty_specs.iterdir():
                        if feature_dir.is_dir() and feature_dir.name.startswith(
                            f"{feature_num}-"
                        ):
                            meta_path = feature_dir / "meta.json"
                            if meta_path.is_file():
                                try:
                                    meta = json.loads(meta_path.read_text())
                                    if "vcs" in meta:
                                        return VCSBackend(meta["vcs"])
                                except (json.JSONDecodeError, ValueError, OSError):
                                    pass
                            # Found feature dir but no valid meta.json
                            return None

    # Path is not inside any feature
    return None


# =============================================================================
# Factory Function
# =============================================================================


def x__get_locked_vcs_from_feature__mutmut_29(path: Path) -> VCSBackend | None:
    """
    Read VCS from feature meta.json if path is inside that feature.

    Args:
        path: A path that might be within a feature directory.

    Returns:
        The locked VCSBackend if path is inside a feature with locked VCS, None otherwise.

    Note:
        Only returns a locked VCS if `path` is actually inside the feature directory
        (either in kitty-specs/###-feature/ or in a worktree for that feature).
        Does NOT return VCS for unrelated features.
    """
    current = path.resolve()

    # Strategy 1: Check if path is directly inside kitty-specs/###-feature/
    # e.g., /repo/kitty-specs/015-feature/tasks/WP01.md
    for parent in [current, *current.parents]:
        if parent.parent and parent.parent.name == "kitty-specs":
            # parent is a feature directory like kitty-specs/015-feature/
            meta_path = parent / "meta.json"
            if meta_path.is_file():
                try:
                    meta = json.loads(meta_path.read_text())
                    if "vcs" in meta:
                        return VCSBackend(meta["vcs"])
                except (json.JSONDecodeError, ValueError, OSError):
                    pass
            # Path is in a feature dir but no valid meta.json
            return None

    # Strategy 2: Check if we're in a worktree for a feature
    # e.g., .worktrees/015-feature-name-WP01/src/file.py
    if ".worktrees" in str(current):
        # Find the worktree root (direct child of .worktrees/)
        worktree_root = None
        for parent in [current, *current.parents]:
            if parent.parent and parent.parent.name == ".worktrees":
                worktree_root = parent
                break

        if worktree_root:
            # Extract feature number from worktree name
            # Pattern: ###-feature-name-WP##
            worktree_name = None
            match = re.match(r"(\d{3})-", worktree_name)
            if match:
                feature_num = match.group(1)
                # Find main repo (parent of .worktrees)
                main_repo = worktree_root.parent.parent
                kitty_specs = main_repo / "kitty-specs"
                if kitty_specs.is_dir():
                    # Find the specific feature directory matching feature_num
                    for feature_dir in kitty_specs.iterdir():
                        if feature_dir.is_dir() and feature_dir.name.startswith(
                            f"{feature_num}-"
                        ):
                            meta_path = feature_dir / "meta.json"
                            if meta_path.is_file():
                                try:
                                    meta = json.loads(meta_path.read_text())
                                    if "vcs" in meta:
                                        return VCSBackend(meta["vcs"])
                                except (json.JSONDecodeError, ValueError, OSError):
                                    pass
                            # Found feature dir but no valid meta.json
                            return None

    # Path is not inside any feature
    return None


# =============================================================================
# Factory Function
# =============================================================================


def x__get_locked_vcs_from_feature__mutmut_30(path: Path) -> VCSBackend | None:
    """
    Read VCS from feature meta.json if path is inside that feature.

    Args:
        path: A path that might be within a feature directory.

    Returns:
        The locked VCSBackend if path is inside a feature with locked VCS, None otherwise.

    Note:
        Only returns a locked VCS if `path` is actually inside the feature directory
        (either in kitty-specs/###-feature/ or in a worktree for that feature).
        Does NOT return VCS for unrelated features.
    """
    current = path.resolve()

    # Strategy 1: Check if path is directly inside kitty-specs/###-feature/
    # e.g., /repo/kitty-specs/015-feature/tasks/WP01.md
    for parent in [current, *current.parents]:
        if parent.parent and parent.parent.name == "kitty-specs":
            # parent is a feature directory like kitty-specs/015-feature/
            meta_path = parent / "meta.json"
            if meta_path.is_file():
                try:
                    meta = json.loads(meta_path.read_text())
                    if "vcs" in meta:
                        return VCSBackend(meta["vcs"])
                except (json.JSONDecodeError, ValueError, OSError):
                    pass
            # Path is in a feature dir but no valid meta.json
            return None

    # Strategy 2: Check if we're in a worktree for a feature
    # e.g., .worktrees/015-feature-name-WP01/src/file.py
    if ".worktrees" in str(current):
        # Find the worktree root (direct child of .worktrees/)
        worktree_root = None
        for parent in [current, *current.parents]:
            if parent.parent and parent.parent.name == ".worktrees":
                worktree_root = parent
                break

        if worktree_root:
            # Extract feature number from worktree name
            # Pattern: ###-feature-name-WP##
            worktree_name = worktree_root.name
            match = None
            if match:
                feature_num = match.group(1)
                # Find main repo (parent of .worktrees)
                main_repo = worktree_root.parent.parent
                kitty_specs = main_repo / "kitty-specs"
                if kitty_specs.is_dir():
                    # Find the specific feature directory matching feature_num
                    for feature_dir in kitty_specs.iterdir():
                        if feature_dir.is_dir() and feature_dir.name.startswith(
                            f"{feature_num}-"
                        ):
                            meta_path = feature_dir / "meta.json"
                            if meta_path.is_file():
                                try:
                                    meta = json.loads(meta_path.read_text())
                                    if "vcs" in meta:
                                        return VCSBackend(meta["vcs"])
                                except (json.JSONDecodeError, ValueError, OSError):
                                    pass
                            # Found feature dir but no valid meta.json
                            return None

    # Path is not inside any feature
    return None


# =============================================================================
# Factory Function
# =============================================================================


def x__get_locked_vcs_from_feature__mutmut_31(path: Path) -> VCSBackend | None:
    """
    Read VCS from feature meta.json if path is inside that feature.

    Args:
        path: A path that might be within a feature directory.

    Returns:
        The locked VCSBackend if path is inside a feature with locked VCS, None otherwise.

    Note:
        Only returns a locked VCS if `path` is actually inside the feature directory
        (either in kitty-specs/###-feature/ or in a worktree for that feature).
        Does NOT return VCS for unrelated features.
    """
    current = path.resolve()

    # Strategy 1: Check if path is directly inside kitty-specs/###-feature/
    # e.g., /repo/kitty-specs/015-feature/tasks/WP01.md
    for parent in [current, *current.parents]:
        if parent.parent and parent.parent.name == "kitty-specs":
            # parent is a feature directory like kitty-specs/015-feature/
            meta_path = parent / "meta.json"
            if meta_path.is_file():
                try:
                    meta = json.loads(meta_path.read_text())
                    if "vcs" in meta:
                        return VCSBackend(meta["vcs"])
                except (json.JSONDecodeError, ValueError, OSError):
                    pass
            # Path is in a feature dir but no valid meta.json
            return None

    # Strategy 2: Check if we're in a worktree for a feature
    # e.g., .worktrees/015-feature-name-WP01/src/file.py
    if ".worktrees" in str(current):
        # Find the worktree root (direct child of .worktrees/)
        worktree_root = None
        for parent in [current, *current.parents]:
            if parent.parent and parent.parent.name == ".worktrees":
                worktree_root = parent
                break

        if worktree_root:
            # Extract feature number from worktree name
            # Pattern: ###-feature-name-WP##
            worktree_name = worktree_root.name
            match = re.match(None, worktree_name)
            if match:
                feature_num = match.group(1)
                # Find main repo (parent of .worktrees)
                main_repo = worktree_root.parent.parent
                kitty_specs = main_repo / "kitty-specs"
                if kitty_specs.is_dir():
                    # Find the specific feature directory matching feature_num
                    for feature_dir in kitty_specs.iterdir():
                        if feature_dir.is_dir() and feature_dir.name.startswith(
                            f"{feature_num}-"
                        ):
                            meta_path = feature_dir / "meta.json"
                            if meta_path.is_file():
                                try:
                                    meta = json.loads(meta_path.read_text())
                                    if "vcs" in meta:
                                        return VCSBackend(meta["vcs"])
                                except (json.JSONDecodeError, ValueError, OSError):
                                    pass
                            # Found feature dir but no valid meta.json
                            return None

    # Path is not inside any feature
    return None


# =============================================================================
# Factory Function
# =============================================================================


def x__get_locked_vcs_from_feature__mutmut_32(path: Path) -> VCSBackend | None:
    """
    Read VCS from feature meta.json if path is inside that feature.

    Args:
        path: A path that might be within a feature directory.

    Returns:
        The locked VCSBackend if path is inside a feature with locked VCS, None otherwise.

    Note:
        Only returns a locked VCS if `path` is actually inside the feature directory
        (either in kitty-specs/###-feature/ or in a worktree for that feature).
        Does NOT return VCS for unrelated features.
    """
    current = path.resolve()

    # Strategy 1: Check if path is directly inside kitty-specs/###-feature/
    # e.g., /repo/kitty-specs/015-feature/tasks/WP01.md
    for parent in [current, *current.parents]:
        if parent.parent and parent.parent.name == "kitty-specs":
            # parent is a feature directory like kitty-specs/015-feature/
            meta_path = parent / "meta.json"
            if meta_path.is_file():
                try:
                    meta = json.loads(meta_path.read_text())
                    if "vcs" in meta:
                        return VCSBackend(meta["vcs"])
                except (json.JSONDecodeError, ValueError, OSError):
                    pass
            # Path is in a feature dir but no valid meta.json
            return None

    # Strategy 2: Check if we're in a worktree for a feature
    # e.g., .worktrees/015-feature-name-WP01/src/file.py
    if ".worktrees" in str(current):
        # Find the worktree root (direct child of .worktrees/)
        worktree_root = None
        for parent in [current, *current.parents]:
            if parent.parent and parent.parent.name == ".worktrees":
                worktree_root = parent
                break

        if worktree_root:
            # Extract feature number from worktree name
            # Pattern: ###-feature-name-WP##
            worktree_name = worktree_root.name
            match = re.match(r"(\d{3})-", None)
            if match:
                feature_num = match.group(1)
                # Find main repo (parent of .worktrees)
                main_repo = worktree_root.parent.parent
                kitty_specs = main_repo / "kitty-specs"
                if kitty_specs.is_dir():
                    # Find the specific feature directory matching feature_num
                    for feature_dir in kitty_specs.iterdir():
                        if feature_dir.is_dir() and feature_dir.name.startswith(
                            f"{feature_num}-"
                        ):
                            meta_path = feature_dir / "meta.json"
                            if meta_path.is_file():
                                try:
                                    meta = json.loads(meta_path.read_text())
                                    if "vcs" in meta:
                                        return VCSBackend(meta["vcs"])
                                except (json.JSONDecodeError, ValueError, OSError):
                                    pass
                            # Found feature dir but no valid meta.json
                            return None

    # Path is not inside any feature
    return None


# =============================================================================
# Factory Function
# =============================================================================


def x__get_locked_vcs_from_feature__mutmut_33(path: Path) -> VCSBackend | None:
    """
    Read VCS from feature meta.json if path is inside that feature.

    Args:
        path: A path that might be within a feature directory.

    Returns:
        The locked VCSBackend if path is inside a feature with locked VCS, None otherwise.

    Note:
        Only returns a locked VCS if `path` is actually inside the feature directory
        (either in kitty-specs/###-feature/ or in a worktree for that feature).
        Does NOT return VCS for unrelated features.
    """
    current = path.resolve()

    # Strategy 1: Check if path is directly inside kitty-specs/###-feature/
    # e.g., /repo/kitty-specs/015-feature/tasks/WP01.md
    for parent in [current, *current.parents]:
        if parent.parent and parent.parent.name == "kitty-specs":
            # parent is a feature directory like kitty-specs/015-feature/
            meta_path = parent / "meta.json"
            if meta_path.is_file():
                try:
                    meta = json.loads(meta_path.read_text())
                    if "vcs" in meta:
                        return VCSBackend(meta["vcs"])
                except (json.JSONDecodeError, ValueError, OSError):
                    pass
            # Path is in a feature dir but no valid meta.json
            return None

    # Strategy 2: Check if we're in a worktree for a feature
    # e.g., .worktrees/015-feature-name-WP01/src/file.py
    if ".worktrees" in str(current):
        # Find the worktree root (direct child of .worktrees/)
        worktree_root = None
        for parent in [current, *current.parents]:
            if parent.parent and parent.parent.name == ".worktrees":
                worktree_root = parent
                break

        if worktree_root:
            # Extract feature number from worktree name
            # Pattern: ###-feature-name-WP##
            worktree_name = worktree_root.name
            match = re.match(worktree_name)
            if match:
                feature_num = match.group(1)
                # Find main repo (parent of .worktrees)
                main_repo = worktree_root.parent.parent
                kitty_specs = main_repo / "kitty-specs"
                if kitty_specs.is_dir():
                    # Find the specific feature directory matching feature_num
                    for feature_dir in kitty_specs.iterdir():
                        if feature_dir.is_dir() and feature_dir.name.startswith(
                            f"{feature_num}-"
                        ):
                            meta_path = feature_dir / "meta.json"
                            if meta_path.is_file():
                                try:
                                    meta = json.loads(meta_path.read_text())
                                    if "vcs" in meta:
                                        return VCSBackend(meta["vcs"])
                                except (json.JSONDecodeError, ValueError, OSError):
                                    pass
                            # Found feature dir but no valid meta.json
                            return None

    # Path is not inside any feature
    return None


# =============================================================================
# Factory Function
# =============================================================================


def x__get_locked_vcs_from_feature__mutmut_34(path: Path) -> VCSBackend | None:
    """
    Read VCS from feature meta.json if path is inside that feature.

    Args:
        path: A path that might be within a feature directory.

    Returns:
        The locked VCSBackend if path is inside a feature with locked VCS, None otherwise.

    Note:
        Only returns a locked VCS if `path` is actually inside the feature directory
        (either in kitty-specs/###-feature/ or in a worktree for that feature).
        Does NOT return VCS for unrelated features.
    """
    current = path.resolve()

    # Strategy 1: Check if path is directly inside kitty-specs/###-feature/
    # e.g., /repo/kitty-specs/015-feature/tasks/WP01.md
    for parent in [current, *current.parents]:
        if parent.parent and parent.parent.name == "kitty-specs":
            # parent is a feature directory like kitty-specs/015-feature/
            meta_path = parent / "meta.json"
            if meta_path.is_file():
                try:
                    meta = json.loads(meta_path.read_text())
                    if "vcs" in meta:
                        return VCSBackend(meta["vcs"])
                except (json.JSONDecodeError, ValueError, OSError):
                    pass
            # Path is in a feature dir but no valid meta.json
            return None

    # Strategy 2: Check if we're in a worktree for a feature
    # e.g., .worktrees/015-feature-name-WP01/src/file.py
    if ".worktrees" in str(current):
        # Find the worktree root (direct child of .worktrees/)
        worktree_root = None
        for parent in [current, *current.parents]:
            if parent.parent and parent.parent.name == ".worktrees":
                worktree_root = parent
                break

        if worktree_root:
            # Extract feature number from worktree name
            # Pattern: ###-feature-name-WP##
            worktree_name = worktree_root.name
            match = re.match(r"(\d{3})-", )
            if match:
                feature_num = match.group(1)
                # Find main repo (parent of .worktrees)
                main_repo = worktree_root.parent.parent
                kitty_specs = main_repo / "kitty-specs"
                if kitty_specs.is_dir():
                    # Find the specific feature directory matching feature_num
                    for feature_dir in kitty_specs.iterdir():
                        if feature_dir.is_dir() and feature_dir.name.startswith(
                            f"{feature_num}-"
                        ):
                            meta_path = feature_dir / "meta.json"
                            if meta_path.is_file():
                                try:
                                    meta = json.loads(meta_path.read_text())
                                    if "vcs" in meta:
                                        return VCSBackend(meta["vcs"])
                                except (json.JSONDecodeError, ValueError, OSError):
                                    pass
                            # Found feature dir but no valid meta.json
                            return None

    # Path is not inside any feature
    return None


# =============================================================================
# Factory Function
# =============================================================================


def x__get_locked_vcs_from_feature__mutmut_35(path: Path) -> VCSBackend | None:
    """
    Read VCS from feature meta.json if path is inside that feature.

    Args:
        path: A path that might be within a feature directory.

    Returns:
        The locked VCSBackend if path is inside a feature with locked VCS, None otherwise.

    Note:
        Only returns a locked VCS if `path` is actually inside the feature directory
        (either in kitty-specs/###-feature/ or in a worktree for that feature).
        Does NOT return VCS for unrelated features.
    """
    current = path.resolve()

    # Strategy 1: Check if path is directly inside kitty-specs/###-feature/
    # e.g., /repo/kitty-specs/015-feature/tasks/WP01.md
    for parent in [current, *current.parents]:
        if parent.parent and parent.parent.name == "kitty-specs":
            # parent is a feature directory like kitty-specs/015-feature/
            meta_path = parent / "meta.json"
            if meta_path.is_file():
                try:
                    meta = json.loads(meta_path.read_text())
                    if "vcs" in meta:
                        return VCSBackend(meta["vcs"])
                except (json.JSONDecodeError, ValueError, OSError):
                    pass
            # Path is in a feature dir but no valid meta.json
            return None

    # Strategy 2: Check if we're in a worktree for a feature
    # e.g., .worktrees/015-feature-name-WP01/src/file.py
    if ".worktrees" in str(current):
        # Find the worktree root (direct child of .worktrees/)
        worktree_root = None
        for parent in [current, *current.parents]:
            if parent.parent and parent.parent.name == ".worktrees":
                worktree_root = parent
                break

        if worktree_root:
            # Extract feature number from worktree name
            # Pattern: ###-feature-name-WP##
            worktree_name = worktree_root.name
            match = re.match(r"XX(\d{3})-XX", worktree_name)
            if match:
                feature_num = match.group(1)
                # Find main repo (parent of .worktrees)
                main_repo = worktree_root.parent.parent
                kitty_specs = main_repo / "kitty-specs"
                if kitty_specs.is_dir():
                    # Find the specific feature directory matching feature_num
                    for feature_dir in kitty_specs.iterdir():
                        if feature_dir.is_dir() and feature_dir.name.startswith(
                            f"{feature_num}-"
                        ):
                            meta_path = feature_dir / "meta.json"
                            if meta_path.is_file():
                                try:
                                    meta = json.loads(meta_path.read_text())
                                    if "vcs" in meta:
                                        return VCSBackend(meta["vcs"])
                                except (json.JSONDecodeError, ValueError, OSError):
                                    pass
                            # Found feature dir but no valid meta.json
                            return None

    # Path is not inside any feature
    return None


# =============================================================================
# Factory Function
# =============================================================================


def x__get_locked_vcs_from_feature__mutmut_36(path: Path) -> VCSBackend | None:
    """
    Read VCS from feature meta.json if path is inside that feature.

    Args:
        path: A path that might be within a feature directory.

    Returns:
        The locked VCSBackend if path is inside a feature with locked VCS, None otherwise.

    Note:
        Only returns a locked VCS if `path` is actually inside the feature directory
        (either in kitty-specs/###-feature/ or in a worktree for that feature).
        Does NOT return VCS for unrelated features.
    """
    current = path.resolve()

    # Strategy 1: Check if path is directly inside kitty-specs/###-feature/
    # e.g., /repo/kitty-specs/015-feature/tasks/WP01.md
    for parent in [current, *current.parents]:
        if parent.parent and parent.parent.name == "kitty-specs":
            # parent is a feature directory like kitty-specs/015-feature/
            meta_path = parent / "meta.json"
            if meta_path.is_file():
                try:
                    meta = json.loads(meta_path.read_text())
                    if "vcs" in meta:
                        return VCSBackend(meta["vcs"])
                except (json.JSONDecodeError, ValueError, OSError):
                    pass
            # Path is in a feature dir but no valid meta.json
            return None

    # Strategy 2: Check if we're in a worktree for a feature
    # e.g., .worktrees/015-feature-name-WP01/src/file.py
    if ".worktrees" in str(current):
        # Find the worktree root (direct child of .worktrees/)
        worktree_root = None
        for parent in [current, *current.parents]:
            if parent.parent and parent.parent.name == ".worktrees":
                worktree_root = parent
                break

        if worktree_root:
            # Extract feature number from worktree name
            # Pattern: ###-feature-name-WP##
            worktree_name = worktree_root.name
            match = re.match(r"(\d{3})-", worktree_name)
            if match:
                feature_num = None
                # Find main repo (parent of .worktrees)
                main_repo = worktree_root.parent.parent
                kitty_specs = main_repo / "kitty-specs"
                if kitty_specs.is_dir():
                    # Find the specific feature directory matching feature_num
                    for feature_dir in kitty_specs.iterdir():
                        if feature_dir.is_dir() and feature_dir.name.startswith(
                            f"{feature_num}-"
                        ):
                            meta_path = feature_dir / "meta.json"
                            if meta_path.is_file():
                                try:
                                    meta = json.loads(meta_path.read_text())
                                    if "vcs" in meta:
                                        return VCSBackend(meta["vcs"])
                                except (json.JSONDecodeError, ValueError, OSError):
                                    pass
                            # Found feature dir but no valid meta.json
                            return None

    # Path is not inside any feature
    return None


# =============================================================================
# Factory Function
# =============================================================================


def x__get_locked_vcs_from_feature__mutmut_37(path: Path) -> VCSBackend | None:
    """
    Read VCS from feature meta.json if path is inside that feature.

    Args:
        path: A path that might be within a feature directory.

    Returns:
        The locked VCSBackend if path is inside a feature with locked VCS, None otherwise.

    Note:
        Only returns a locked VCS if `path` is actually inside the feature directory
        (either in kitty-specs/###-feature/ or in a worktree for that feature).
        Does NOT return VCS for unrelated features.
    """
    current = path.resolve()

    # Strategy 1: Check if path is directly inside kitty-specs/###-feature/
    # e.g., /repo/kitty-specs/015-feature/tasks/WP01.md
    for parent in [current, *current.parents]:
        if parent.parent and parent.parent.name == "kitty-specs":
            # parent is a feature directory like kitty-specs/015-feature/
            meta_path = parent / "meta.json"
            if meta_path.is_file():
                try:
                    meta = json.loads(meta_path.read_text())
                    if "vcs" in meta:
                        return VCSBackend(meta["vcs"])
                except (json.JSONDecodeError, ValueError, OSError):
                    pass
            # Path is in a feature dir but no valid meta.json
            return None

    # Strategy 2: Check if we're in a worktree for a feature
    # e.g., .worktrees/015-feature-name-WP01/src/file.py
    if ".worktrees" in str(current):
        # Find the worktree root (direct child of .worktrees/)
        worktree_root = None
        for parent in [current, *current.parents]:
            if parent.parent and parent.parent.name == ".worktrees":
                worktree_root = parent
                break

        if worktree_root:
            # Extract feature number from worktree name
            # Pattern: ###-feature-name-WP##
            worktree_name = worktree_root.name
            match = re.match(r"(\d{3})-", worktree_name)
            if match:
                feature_num = match.group(None)
                # Find main repo (parent of .worktrees)
                main_repo = worktree_root.parent.parent
                kitty_specs = main_repo / "kitty-specs"
                if kitty_specs.is_dir():
                    # Find the specific feature directory matching feature_num
                    for feature_dir in kitty_specs.iterdir():
                        if feature_dir.is_dir() and feature_dir.name.startswith(
                            f"{feature_num}-"
                        ):
                            meta_path = feature_dir / "meta.json"
                            if meta_path.is_file():
                                try:
                                    meta = json.loads(meta_path.read_text())
                                    if "vcs" in meta:
                                        return VCSBackend(meta["vcs"])
                                except (json.JSONDecodeError, ValueError, OSError):
                                    pass
                            # Found feature dir but no valid meta.json
                            return None

    # Path is not inside any feature
    return None


# =============================================================================
# Factory Function
# =============================================================================


def x__get_locked_vcs_from_feature__mutmut_38(path: Path) -> VCSBackend | None:
    """
    Read VCS from feature meta.json if path is inside that feature.

    Args:
        path: A path that might be within a feature directory.

    Returns:
        The locked VCSBackend if path is inside a feature with locked VCS, None otherwise.

    Note:
        Only returns a locked VCS if `path` is actually inside the feature directory
        (either in kitty-specs/###-feature/ or in a worktree for that feature).
        Does NOT return VCS for unrelated features.
    """
    current = path.resolve()

    # Strategy 1: Check if path is directly inside kitty-specs/###-feature/
    # e.g., /repo/kitty-specs/015-feature/tasks/WP01.md
    for parent in [current, *current.parents]:
        if parent.parent and parent.parent.name == "kitty-specs":
            # parent is a feature directory like kitty-specs/015-feature/
            meta_path = parent / "meta.json"
            if meta_path.is_file():
                try:
                    meta = json.loads(meta_path.read_text())
                    if "vcs" in meta:
                        return VCSBackend(meta["vcs"])
                except (json.JSONDecodeError, ValueError, OSError):
                    pass
            # Path is in a feature dir but no valid meta.json
            return None

    # Strategy 2: Check if we're in a worktree for a feature
    # e.g., .worktrees/015-feature-name-WP01/src/file.py
    if ".worktrees" in str(current):
        # Find the worktree root (direct child of .worktrees/)
        worktree_root = None
        for parent in [current, *current.parents]:
            if parent.parent and parent.parent.name == ".worktrees":
                worktree_root = parent
                break

        if worktree_root:
            # Extract feature number from worktree name
            # Pattern: ###-feature-name-WP##
            worktree_name = worktree_root.name
            match = re.match(r"(\d{3})-", worktree_name)
            if match:
                feature_num = match.group(2)
                # Find main repo (parent of .worktrees)
                main_repo = worktree_root.parent.parent
                kitty_specs = main_repo / "kitty-specs"
                if kitty_specs.is_dir():
                    # Find the specific feature directory matching feature_num
                    for feature_dir in kitty_specs.iterdir():
                        if feature_dir.is_dir() and feature_dir.name.startswith(
                            f"{feature_num}-"
                        ):
                            meta_path = feature_dir / "meta.json"
                            if meta_path.is_file():
                                try:
                                    meta = json.loads(meta_path.read_text())
                                    if "vcs" in meta:
                                        return VCSBackend(meta["vcs"])
                                except (json.JSONDecodeError, ValueError, OSError):
                                    pass
                            # Found feature dir but no valid meta.json
                            return None

    # Path is not inside any feature
    return None


# =============================================================================
# Factory Function
# =============================================================================


def x__get_locked_vcs_from_feature__mutmut_39(path: Path) -> VCSBackend | None:
    """
    Read VCS from feature meta.json if path is inside that feature.

    Args:
        path: A path that might be within a feature directory.

    Returns:
        The locked VCSBackend if path is inside a feature with locked VCS, None otherwise.

    Note:
        Only returns a locked VCS if `path` is actually inside the feature directory
        (either in kitty-specs/###-feature/ or in a worktree for that feature).
        Does NOT return VCS for unrelated features.
    """
    current = path.resolve()

    # Strategy 1: Check if path is directly inside kitty-specs/###-feature/
    # e.g., /repo/kitty-specs/015-feature/tasks/WP01.md
    for parent in [current, *current.parents]:
        if parent.parent and parent.parent.name == "kitty-specs":
            # parent is a feature directory like kitty-specs/015-feature/
            meta_path = parent / "meta.json"
            if meta_path.is_file():
                try:
                    meta = json.loads(meta_path.read_text())
                    if "vcs" in meta:
                        return VCSBackend(meta["vcs"])
                except (json.JSONDecodeError, ValueError, OSError):
                    pass
            # Path is in a feature dir but no valid meta.json
            return None

    # Strategy 2: Check if we're in a worktree for a feature
    # e.g., .worktrees/015-feature-name-WP01/src/file.py
    if ".worktrees" in str(current):
        # Find the worktree root (direct child of .worktrees/)
        worktree_root = None
        for parent in [current, *current.parents]:
            if parent.parent and parent.parent.name == ".worktrees":
                worktree_root = parent
                break

        if worktree_root:
            # Extract feature number from worktree name
            # Pattern: ###-feature-name-WP##
            worktree_name = worktree_root.name
            match = re.match(r"(\d{3})-", worktree_name)
            if match:
                feature_num = match.group(1)
                # Find main repo (parent of .worktrees)
                main_repo = None
                kitty_specs = main_repo / "kitty-specs"
                if kitty_specs.is_dir():
                    # Find the specific feature directory matching feature_num
                    for feature_dir in kitty_specs.iterdir():
                        if feature_dir.is_dir() and feature_dir.name.startswith(
                            f"{feature_num}-"
                        ):
                            meta_path = feature_dir / "meta.json"
                            if meta_path.is_file():
                                try:
                                    meta = json.loads(meta_path.read_text())
                                    if "vcs" in meta:
                                        return VCSBackend(meta["vcs"])
                                except (json.JSONDecodeError, ValueError, OSError):
                                    pass
                            # Found feature dir but no valid meta.json
                            return None

    # Path is not inside any feature
    return None


# =============================================================================
# Factory Function
# =============================================================================


def x__get_locked_vcs_from_feature__mutmut_40(path: Path) -> VCSBackend | None:
    """
    Read VCS from feature meta.json if path is inside that feature.

    Args:
        path: A path that might be within a feature directory.

    Returns:
        The locked VCSBackend if path is inside a feature with locked VCS, None otherwise.

    Note:
        Only returns a locked VCS if `path` is actually inside the feature directory
        (either in kitty-specs/###-feature/ or in a worktree for that feature).
        Does NOT return VCS for unrelated features.
    """
    current = path.resolve()

    # Strategy 1: Check if path is directly inside kitty-specs/###-feature/
    # e.g., /repo/kitty-specs/015-feature/tasks/WP01.md
    for parent in [current, *current.parents]:
        if parent.parent and parent.parent.name == "kitty-specs":
            # parent is a feature directory like kitty-specs/015-feature/
            meta_path = parent / "meta.json"
            if meta_path.is_file():
                try:
                    meta = json.loads(meta_path.read_text())
                    if "vcs" in meta:
                        return VCSBackend(meta["vcs"])
                except (json.JSONDecodeError, ValueError, OSError):
                    pass
            # Path is in a feature dir but no valid meta.json
            return None

    # Strategy 2: Check if we're in a worktree for a feature
    # e.g., .worktrees/015-feature-name-WP01/src/file.py
    if ".worktrees" in str(current):
        # Find the worktree root (direct child of .worktrees/)
        worktree_root = None
        for parent in [current, *current.parents]:
            if parent.parent and parent.parent.name == ".worktrees":
                worktree_root = parent
                break

        if worktree_root:
            # Extract feature number from worktree name
            # Pattern: ###-feature-name-WP##
            worktree_name = worktree_root.name
            match = re.match(r"(\d{3})-", worktree_name)
            if match:
                feature_num = match.group(1)
                # Find main repo (parent of .worktrees)
                main_repo = worktree_root.parent.parent
                kitty_specs = None
                if kitty_specs.is_dir():
                    # Find the specific feature directory matching feature_num
                    for feature_dir in kitty_specs.iterdir():
                        if feature_dir.is_dir() and feature_dir.name.startswith(
                            f"{feature_num}-"
                        ):
                            meta_path = feature_dir / "meta.json"
                            if meta_path.is_file():
                                try:
                                    meta = json.loads(meta_path.read_text())
                                    if "vcs" in meta:
                                        return VCSBackend(meta["vcs"])
                                except (json.JSONDecodeError, ValueError, OSError):
                                    pass
                            # Found feature dir but no valid meta.json
                            return None

    # Path is not inside any feature
    return None


# =============================================================================
# Factory Function
# =============================================================================


def x__get_locked_vcs_from_feature__mutmut_41(path: Path) -> VCSBackend | None:
    """
    Read VCS from feature meta.json if path is inside that feature.

    Args:
        path: A path that might be within a feature directory.

    Returns:
        The locked VCSBackend if path is inside a feature with locked VCS, None otherwise.

    Note:
        Only returns a locked VCS if `path` is actually inside the feature directory
        (either in kitty-specs/###-feature/ or in a worktree for that feature).
        Does NOT return VCS for unrelated features.
    """
    current = path.resolve()

    # Strategy 1: Check if path is directly inside kitty-specs/###-feature/
    # e.g., /repo/kitty-specs/015-feature/tasks/WP01.md
    for parent in [current, *current.parents]:
        if parent.parent and parent.parent.name == "kitty-specs":
            # parent is a feature directory like kitty-specs/015-feature/
            meta_path = parent / "meta.json"
            if meta_path.is_file():
                try:
                    meta = json.loads(meta_path.read_text())
                    if "vcs" in meta:
                        return VCSBackend(meta["vcs"])
                except (json.JSONDecodeError, ValueError, OSError):
                    pass
            # Path is in a feature dir but no valid meta.json
            return None

    # Strategy 2: Check if we're in a worktree for a feature
    # e.g., .worktrees/015-feature-name-WP01/src/file.py
    if ".worktrees" in str(current):
        # Find the worktree root (direct child of .worktrees/)
        worktree_root = None
        for parent in [current, *current.parents]:
            if parent.parent and parent.parent.name == ".worktrees":
                worktree_root = parent
                break

        if worktree_root:
            # Extract feature number from worktree name
            # Pattern: ###-feature-name-WP##
            worktree_name = worktree_root.name
            match = re.match(r"(\d{3})-", worktree_name)
            if match:
                feature_num = match.group(1)
                # Find main repo (parent of .worktrees)
                main_repo = worktree_root.parent.parent
                kitty_specs = main_repo * "kitty-specs"
                if kitty_specs.is_dir():
                    # Find the specific feature directory matching feature_num
                    for feature_dir in kitty_specs.iterdir():
                        if feature_dir.is_dir() and feature_dir.name.startswith(
                            f"{feature_num}-"
                        ):
                            meta_path = feature_dir / "meta.json"
                            if meta_path.is_file():
                                try:
                                    meta = json.loads(meta_path.read_text())
                                    if "vcs" in meta:
                                        return VCSBackend(meta["vcs"])
                                except (json.JSONDecodeError, ValueError, OSError):
                                    pass
                            # Found feature dir but no valid meta.json
                            return None

    # Path is not inside any feature
    return None


# =============================================================================
# Factory Function
# =============================================================================


def x__get_locked_vcs_from_feature__mutmut_42(path: Path) -> VCSBackend | None:
    """
    Read VCS from feature meta.json if path is inside that feature.

    Args:
        path: A path that might be within a feature directory.

    Returns:
        The locked VCSBackend if path is inside a feature with locked VCS, None otherwise.

    Note:
        Only returns a locked VCS if `path` is actually inside the feature directory
        (either in kitty-specs/###-feature/ or in a worktree for that feature).
        Does NOT return VCS for unrelated features.
    """
    current = path.resolve()

    # Strategy 1: Check if path is directly inside kitty-specs/###-feature/
    # e.g., /repo/kitty-specs/015-feature/tasks/WP01.md
    for parent in [current, *current.parents]:
        if parent.parent and parent.parent.name == "kitty-specs":
            # parent is a feature directory like kitty-specs/015-feature/
            meta_path = parent / "meta.json"
            if meta_path.is_file():
                try:
                    meta = json.loads(meta_path.read_text())
                    if "vcs" in meta:
                        return VCSBackend(meta["vcs"])
                except (json.JSONDecodeError, ValueError, OSError):
                    pass
            # Path is in a feature dir but no valid meta.json
            return None

    # Strategy 2: Check if we're in a worktree for a feature
    # e.g., .worktrees/015-feature-name-WP01/src/file.py
    if ".worktrees" in str(current):
        # Find the worktree root (direct child of .worktrees/)
        worktree_root = None
        for parent in [current, *current.parents]:
            if parent.parent and parent.parent.name == ".worktrees":
                worktree_root = parent
                break

        if worktree_root:
            # Extract feature number from worktree name
            # Pattern: ###-feature-name-WP##
            worktree_name = worktree_root.name
            match = re.match(r"(\d{3})-", worktree_name)
            if match:
                feature_num = match.group(1)
                # Find main repo (parent of .worktrees)
                main_repo = worktree_root.parent.parent
                kitty_specs = main_repo / "XXkitty-specsXX"
                if kitty_specs.is_dir():
                    # Find the specific feature directory matching feature_num
                    for feature_dir in kitty_specs.iterdir():
                        if feature_dir.is_dir() and feature_dir.name.startswith(
                            f"{feature_num}-"
                        ):
                            meta_path = feature_dir / "meta.json"
                            if meta_path.is_file():
                                try:
                                    meta = json.loads(meta_path.read_text())
                                    if "vcs" in meta:
                                        return VCSBackend(meta["vcs"])
                                except (json.JSONDecodeError, ValueError, OSError):
                                    pass
                            # Found feature dir but no valid meta.json
                            return None

    # Path is not inside any feature
    return None


# =============================================================================
# Factory Function
# =============================================================================


def x__get_locked_vcs_from_feature__mutmut_43(path: Path) -> VCSBackend | None:
    """
    Read VCS from feature meta.json if path is inside that feature.

    Args:
        path: A path that might be within a feature directory.

    Returns:
        The locked VCSBackend if path is inside a feature with locked VCS, None otherwise.

    Note:
        Only returns a locked VCS if `path` is actually inside the feature directory
        (either in kitty-specs/###-feature/ or in a worktree for that feature).
        Does NOT return VCS for unrelated features.
    """
    current = path.resolve()

    # Strategy 1: Check if path is directly inside kitty-specs/###-feature/
    # e.g., /repo/kitty-specs/015-feature/tasks/WP01.md
    for parent in [current, *current.parents]:
        if parent.parent and parent.parent.name == "kitty-specs":
            # parent is a feature directory like kitty-specs/015-feature/
            meta_path = parent / "meta.json"
            if meta_path.is_file():
                try:
                    meta = json.loads(meta_path.read_text())
                    if "vcs" in meta:
                        return VCSBackend(meta["vcs"])
                except (json.JSONDecodeError, ValueError, OSError):
                    pass
            # Path is in a feature dir but no valid meta.json
            return None

    # Strategy 2: Check if we're in a worktree for a feature
    # e.g., .worktrees/015-feature-name-WP01/src/file.py
    if ".worktrees" in str(current):
        # Find the worktree root (direct child of .worktrees/)
        worktree_root = None
        for parent in [current, *current.parents]:
            if parent.parent and parent.parent.name == ".worktrees":
                worktree_root = parent
                break

        if worktree_root:
            # Extract feature number from worktree name
            # Pattern: ###-feature-name-WP##
            worktree_name = worktree_root.name
            match = re.match(r"(\d{3})-", worktree_name)
            if match:
                feature_num = match.group(1)
                # Find main repo (parent of .worktrees)
                main_repo = worktree_root.parent.parent
                kitty_specs = main_repo / "KITTY-SPECS"
                if kitty_specs.is_dir():
                    # Find the specific feature directory matching feature_num
                    for feature_dir in kitty_specs.iterdir():
                        if feature_dir.is_dir() and feature_dir.name.startswith(
                            f"{feature_num}-"
                        ):
                            meta_path = feature_dir / "meta.json"
                            if meta_path.is_file():
                                try:
                                    meta = json.loads(meta_path.read_text())
                                    if "vcs" in meta:
                                        return VCSBackend(meta["vcs"])
                                except (json.JSONDecodeError, ValueError, OSError):
                                    pass
                            # Found feature dir but no valid meta.json
                            return None

    # Path is not inside any feature
    return None


# =============================================================================
# Factory Function
# =============================================================================


def x__get_locked_vcs_from_feature__mutmut_44(path: Path) -> VCSBackend | None:
    """
    Read VCS from feature meta.json if path is inside that feature.

    Args:
        path: A path that might be within a feature directory.

    Returns:
        The locked VCSBackend if path is inside a feature with locked VCS, None otherwise.

    Note:
        Only returns a locked VCS if `path` is actually inside the feature directory
        (either in kitty-specs/###-feature/ or in a worktree for that feature).
        Does NOT return VCS for unrelated features.
    """
    current = path.resolve()

    # Strategy 1: Check if path is directly inside kitty-specs/###-feature/
    # e.g., /repo/kitty-specs/015-feature/tasks/WP01.md
    for parent in [current, *current.parents]:
        if parent.parent and parent.parent.name == "kitty-specs":
            # parent is a feature directory like kitty-specs/015-feature/
            meta_path = parent / "meta.json"
            if meta_path.is_file():
                try:
                    meta = json.loads(meta_path.read_text())
                    if "vcs" in meta:
                        return VCSBackend(meta["vcs"])
                except (json.JSONDecodeError, ValueError, OSError):
                    pass
            # Path is in a feature dir but no valid meta.json
            return None

    # Strategy 2: Check if we're in a worktree for a feature
    # e.g., .worktrees/015-feature-name-WP01/src/file.py
    if ".worktrees" in str(current):
        # Find the worktree root (direct child of .worktrees/)
        worktree_root = None
        for parent in [current, *current.parents]:
            if parent.parent and parent.parent.name == ".worktrees":
                worktree_root = parent
                break

        if worktree_root:
            # Extract feature number from worktree name
            # Pattern: ###-feature-name-WP##
            worktree_name = worktree_root.name
            match = re.match(r"(\d{3})-", worktree_name)
            if match:
                feature_num = match.group(1)
                # Find main repo (parent of .worktrees)
                main_repo = worktree_root.parent.parent
                kitty_specs = main_repo / "kitty-specs"
                if kitty_specs.is_dir():
                    # Find the specific feature directory matching feature_num
                    for feature_dir in kitty_specs.iterdir():
                        if feature_dir.is_dir() or feature_dir.name.startswith(
                            f"{feature_num}-"
                        ):
                            meta_path = feature_dir / "meta.json"
                            if meta_path.is_file():
                                try:
                                    meta = json.loads(meta_path.read_text())
                                    if "vcs" in meta:
                                        return VCSBackend(meta["vcs"])
                                except (json.JSONDecodeError, ValueError, OSError):
                                    pass
                            # Found feature dir but no valid meta.json
                            return None

    # Path is not inside any feature
    return None


# =============================================================================
# Factory Function
# =============================================================================


def x__get_locked_vcs_from_feature__mutmut_45(path: Path) -> VCSBackend | None:
    """
    Read VCS from feature meta.json if path is inside that feature.

    Args:
        path: A path that might be within a feature directory.

    Returns:
        The locked VCSBackend if path is inside a feature with locked VCS, None otherwise.

    Note:
        Only returns a locked VCS if `path` is actually inside the feature directory
        (either in kitty-specs/###-feature/ or in a worktree for that feature).
        Does NOT return VCS for unrelated features.
    """
    current = path.resolve()

    # Strategy 1: Check if path is directly inside kitty-specs/###-feature/
    # e.g., /repo/kitty-specs/015-feature/tasks/WP01.md
    for parent in [current, *current.parents]:
        if parent.parent and parent.parent.name == "kitty-specs":
            # parent is a feature directory like kitty-specs/015-feature/
            meta_path = parent / "meta.json"
            if meta_path.is_file():
                try:
                    meta = json.loads(meta_path.read_text())
                    if "vcs" in meta:
                        return VCSBackend(meta["vcs"])
                except (json.JSONDecodeError, ValueError, OSError):
                    pass
            # Path is in a feature dir but no valid meta.json
            return None

    # Strategy 2: Check if we're in a worktree for a feature
    # e.g., .worktrees/015-feature-name-WP01/src/file.py
    if ".worktrees" in str(current):
        # Find the worktree root (direct child of .worktrees/)
        worktree_root = None
        for parent in [current, *current.parents]:
            if parent.parent and parent.parent.name == ".worktrees":
                worktree_root = parent
                break

        if worktree_root:
            # Extract feature number from worktree name
            # Pattern: ###-feature-name-WP##
            worktree_name = worktree_root.name
            match = re.match(r"(\d{3})-", worktree_name)
            if match:
                feature_num = match.group(1)
                # Find main repo (parent of .worktrees)
                main_repo = worktree_root.parent.parent
                kitty_specs = main_repo / "kitty-specs"
                if kitty_specs.is_dir():
                    # Find the specific feature directory matching feature_num
                    for feature_dir in kitty_specs.iterdir():
                        if feature_dir.is_dir() and feature_dir.name.startswith(
                            None
                        ):
                            meta_path = feature_dir / "meta.json"
                            if meta_path.is_file():
                                try:
                                    meta = json.loads(meta_path.read_text())
                                    if "vcs" in meta:
                                        return VCSBackend(meta["vcs"])
                                except (json.JSONDecodeError, ValueError, OSError):
                                    pass
                            # Found feature dir but no valid meta.json
                            return None

    # Path is not inside any feature
    return None


# =============================================================================
# Factory Function
# =============================================================================


def x__get_locked_vcs_from_feature__mutmut_46(path: Path) -> VCSBackend | None:
    """
    Read VCS from feature meta.json if path is inside that feature.

    Args:
        path: A path that might be within a feature directory.

    Returns:
        The locked VCSBackend if path is inside a feature with locked VCS, None otherwise.

    Note:
        Only returns a locked VCS if `path` is actually inside the feature directory
        (either in kitty-specs/###-feature/ or in a worktree for that feature).
        Does NOT return VCS for unrelated features.
    """
    current = path.resolve()

    # Strategy 1: Check if path is directly inside kitty-specs/###-feature/
    # e.g., /repo/kitty-specs/015-feature/tasks/WP01.md
    for parent in [current, *current.parents]:
        if parent.parent and parent.parent.name == "kitty-specs":
            # parent is a feature directory like kitty-specs/015-feature/
            meta_path = parent / "meta.json"
            if meta_path.is_file():
                try:
                    meta = json.loads(meta_path.read_text())
                    if "vcs" in meta:
                        return VCSBackend(meta["vcs"])
                except (json.JSONDecodeError, ValueError, OSError):
                    pass
            # Path is in a feature dir but no valid meta.json
            return None

    # Strategy 2: Check if we're in a worktree for a feature
    # e.g., .worktrees/015-feature-name-WP01/src/file.py
    if ".worktrees" in str(current):
        # Find the worktree root (direct child of .worktrees/)
        worktree_root = None
        for parent in [current, *current.parents]:
            if parent.parent and parent.parent.name == ".worktrees":
                worktree_root = parent
                break

        if worktree_root:
            # Extract feature number from worktree name
            # Pattern: ###-feature-name-WP##
            worktree_name = worktree_root.name
            match = re.match(r"(\d{3})-", worktree_name)
            if match:
                feature_num = match.group(1)
                # Find main repo (parent of .worktrees)
                main_repo = worktree_root.parent.parent
                kitty_specs = main_repo / "kitty-specs"
                if kitty_specs.is_dir():
                    # Find the specific feature directory matching feature_num
                    for feature_dir in kitty_specs.iterdir():
                        if feature_dir.is_dir() and feature_dir.name.startswith(
                            f"{feature_num}-"
                        ):
                            meta_path = None
                            if meta_path.is_file():
                                try:
                                    meta = json.loads(meta_path.read_text())
                                    if "vcs" in meta:
                                        return VCSBackend(meta["vcs"])
                                except (json.JSONDecodeError, ValueError, OSError):
                                    pass
                            # Found feature dir but no valid meta.json
                            return None

    # Path is not inside any feature
    return None


# =============================================================================
# Factory Function
# =============================================================================


def x__get_locked_vcs_from_feature__mutmut_47(path: Path) -> VCSBackend | None:
    """
    Read VCS from feature meta.json if path is inside that feature.

    Args:
        path: A path that might be within a feature directory.

    Returns:
        The locked VCSBackend if path is inside a feature with locked VCS, None otherwise.

    Note:
        Only returns a locked VCS if `path` is actually inside the feature directory
        (either in kitty-specs/###-feature/ or in a worktree for that feature).
        Does NOT return VCS for unrelated features.
    """
    current = path.resolve()

    # Strategy 1: Check if path is directly inside kitty-specs/###-feature/
    # e.g., /repo/kitty-specs/015-feature/tasks/WP01.md
    for parent in [current, *current.parents]:
        if parent.parent and parent.parent.name == "kitty-specs":
            # parent is a feature directory like kitty-specs/015-feature/
            meta_path = parent / "meta.json"
            if meta_path.is_file():
                try:
                    meta = json.loads(meta_path.read_text())
                    if "vcs" in meta:
                        return VCSBackend(meta["vcs"])
                except (json.JSONDecodeError, ValueError, OSError):
                    pass
            # Path is in a feature dir but no valid meta.json
            return None

    # Strategy 2: Check if we're in a worktree for a feature
    # e.g., .worktrees/015-feature-name-WP01/src/file.py
    if ".worktrees" in str(current):
        # Find the worktree root (direct child of .worktrees/)
        worktree_root = None
        for parent in [current, *current.parents]:
            if parent.parent and parent.parent.name == ".worktrees":
                worktree_root = parent
                break

        if worktree_root:
            # Extract feature number from worktree name
            # Pattern: ###-feature-name-WP##
            worktree_name = worktree_root.name
            match = re.match(r"(\d{3})-", worktree_name)
            if match:
                feature_num = match.group(1)
                # Find main repo (parent of .worktrees)
                main_repo = worktree_root.parent.parent
                kitty_specs = main_repo / "kitty-specs"
                if kitty_specs.is_dir():
                    # Find the specific feature directory matching feature_num
                    for feature_dir in kitty_specs.iterdir():
                        if feature_dir.is_dir() and feature_dir.name.startswith(
                            f"{feature_num}-"
                        ):
                            meta_path = feature_dir * "meta.json"
                            if meta_path.is_file():
                                try:
                                    meta = json.loads(meta_path.read_text())
                                    if "vcs" in meta:
                                        return VCSBackend(meta["vcs"])
                                except (json.JSONDecodeError, ValueError, OSError):
                                    pass
                            # Found feature dir but no valid meta.json
                            return None

    # Path is not inside any feature
    return None


# =============================================================================
# Factory Function
# =============================================================================


def x__get_locked_vcs_from_feature__mutmut_48(path: Path) -> VCSBackend | None:
    """
    Read VCS from feature meta.json if path is inside that feature.

    Args:
        path: A path that might be within a feature directory.

    Returns:
        The locked VCSBackend if path is inside a feature with locked VCS, None otherwise.

    Note:
        Only returns a locked VCS if `path` is actually inside the feature directory
        (either in kitty-specs/###-feature/ or in a worktree for that feature).
        Does NOT return VCS for unrelated features.
    """
    current = path.resolve()

    # Strategy 1: Check if path is directly inside kitty-specs/###-feature/
    # e.g., /repo/kitty-specs/015-feature/tasks/WP01.md
    for parent in [current, *current.parents]:
        if parent.parent and parent.parent.name == "kitty-specs":
            # parent is a feature directory like kitty-specs/015-feature/
            meta_path = parent / "meta.json"
            if meta_path.is_file():
                try:
                    meta = json.loads(meta_path.read_text())
                    if "vcs" in meta:
                        return VCSBackend(meta["vcs"])
                except (json.JSONDecodeError, ValueError, OSError):
                    pass
            # Path is in a feature dir but no valid meta.json
            return None

    # Strategy 2: Check if we're in a worktree for a feature
    # e.g., .worktrees/015-feature-name-WP01/src/file.py
    if ".worktrees" in str(current):
        # Find the worktree root (direct child of .worktrees/)
        worktree_root = None
        for parent in [current, *current.parents]:
            if parent.parent and parent.parent.name == ".worktrees":
                worktree_root = parent
                break

        if worktree_root:
            # Extract feature number from worktree name
            # Pattern: ###-feature-name-WP##
            worktree_name = worktree_root.name
            match = re.match(r"(\d{3})-", worktree_name)
            if match:
                feature_num = match.group(1)
                # Find main repo (parent of .worktrees)
                main_repo = worktree_root.parent.parent
                kitty_specs = main_repo / "kitty-specs"
                if kitty_specs.is_dir():
                    # Find the specific feature directory matching feature_num
                    for feature_dir in kitty_specs.iterdir():
                        if feature_dir.is_dir() and feature_dir.name.startswith(
                            f"{feature_num}-"
                        ):
                            meta_path = feature_dir / "XXmeta.jsonXX"
                            if meta_path.is_file():
                                try:
                                    meta = json.loads(meta_path.read_text())
                                    if "vcs" in meta:
                                        return VCSBackend(meta["vcs"])
                                except (json.JSONDecodeError, ValueError, OSError):
                                    pass
                            # Found feature dir but no valid meta.json
                            return None

    # Path is not inside any feature
    return None


# =============================================================================
# Factory Function
# =============================================================================


def x__get_locked_vcs_from_feature__mutmut_49(path: Path) -> VCSBackend | None:
    """
    Read VCS from feature meta.json if path is inside that feature.

    Args:
        path: A path that might be within a feature directory.

    Returns:
        The locked VCSBackend if path is inside a feature with locked VCS, None otherwise.

    Note:
        Only returns a locked VCS if `path` is actually inside the feature directory
        (either in kitty-specs/###-feature/ or in a worktree for that feature).
        Does NOT return VCS for unrelated features.
    """
    current = path.resolve()

    # Strategy 1: Check if path is directly inside kitty-specs/###-feature/
    # e.g., /repo/kitty-specs/015-feature/tasks/WP01.md
    for parent in [current, *current.parents]:
        if parent.parent and parent.parent.name == "kitty-specs":
            # parent is a feature directory like kitty-specs/015-feature/
            meta_path = parent / "meta.json"
            if meta_path.is_file():
                try:
                    meta = json.loads(meta_path.read_text())
                    if "vcs" in meta:
                        return VCSBackend(meta["vcs"])
                except (json.JSONDecodeError, ValueError, OSError):
                    pass
            # Path is in a feature dir but no valid meta.json
            return None

    # Strategy 2: Check if we're in a worktree for a feature
    # e.g., .worktrees/015-feature-name-WP01/src/file.py
    if ".worktrees" in str(current):
        # Find the worktree root (direct child of .worktrees/)
        worktree_root = None
        for parent in [current, *current.parents]:
            if parent.parent and parent.parent.name == ".worktrees":
                worktree_root = parent
                break

        if worktree_root:
            # Extract feature number from worktree name
            # Pattern: ###-feature-name-WP##
            worktree_name = worktree_root.name
            match = re.match(r"(\d{3})-", worktree_name)
            if match:
                feature_num = match.group(1)
                # Find main repo (parent of .worktrees)
                main_repo = worktree_root.parent.parent
                kitty_specs = main_repo / "kitty-specs"
                if kitty_specs.is_dir():
                    # Find the specific feature directory matching feature_num
                    for feature_dir in kitty_specs.iterdir():
                        if feature_dir.is_dir() and feature_dir.name.startswith(
                            f"{feature_num}-"
                        ):
                            meta_path = feature_dir / "META.JSON"
                            if meta_path.is_file():
                                try:
                                    meta = json.loads(meta_path.read_text())
                                    if "vcs" in meta:
                                        return VCSBackend(meta["vcs"])
                                except (json.JSONDecodeError, ValueError, OSError):
                                    pass
                            # Found feature dir but no valid meta.json
                            return None

    # Path is not inside any feature
    return None


# =============================================================================
# Factory Function
# =============================================================================


def x__get_locked_vcs_from_feature__mutmut_50(path: Path) -> VCSBackend | None:
    """
    Read VCS from feature meta.json if path is inside that feature.

    Args:
        path: A path that might be within a feature directory.

    Returns:
        The locked VCSBackend if path is inside a feature with locked VCS, None otherwise.

    Note:
        Only returns a locked VCS if `path` is actually inside the feature directory
        (either in kitty-specs/###-feature/ or in a worktree for that feature).
        Does NOT return VCS for unrelated features.
    """
    current = path.resolve()

    # Strategy 1: Check if path is directly inside kitty-specs/###-feature/
    # e.g., /repo/kitty-specs/015-feature/tasks/WP01.md
    for parent in [current, *current.parents]:
        if parent.parent and parent.parent.name == "kitty-specs":
            # parent is a feature directory like kitty-specs/015-feature/
            meta_path = parent / "meta.json"
            if meta_path.is_file():
                try:
                    meta = json.loads(meta_path.read_text())
                    if "vcs" in meta:
                        return VCSBackend(meta["vcs"])
                except (json.JSONDecodeError, ValueError, OSError):
                    pass
            # Path is in a feature dir but no valid meta.json
            return None

    # Strategy 2: Check if we're in a worktree for a feature
    # e.g., .worktrees/015-feature-name-WP01/src/file.py
    if ".worktrees" in str(current):
        # Find the worktree root (direct child of .worktrees/)
        worktree_root = None
        for parent in [current, *current.parents]:
            if parent.parent and parent.parent.name == ".worktrees":
                worktree_root = parent
                break

        if worktree_root:
            # Extract feature number from worktree name
            # Pattern: ###-feature-name-WP##
            worktree_name = worktree_root.name
            match = re.match(r"(\d{3})-", worktree_name)
            if match:
                feature_num = match.group(1)
                # Find main repo (parent of .worktrees)
                main_repo = worktree_root.parent.parent
                kitty_specs = main_repo / "kitty-specs"
                if kitty_specs.is_dir():
                    # Find the specific feature directory matching feature_num
                    for feature_dir in kitty_specs.iterdir():
                        if feature_dir.is_dir() and feature_dir.name.startswith(
                            f"{feature_num}-"
                        ):
                            meta_path = feature_dir / "meta.json"
                            if meta_path.is_file():
                                try:
                                    meta = None
                                    if "vcs" in meta:
                                        return VCSBackend(meta["vcs"])
                                except (json.JSONDecodeError, ValueError, OSError):
                                    pass
                            # Found feature dir but no valid meta.json
                            return None

    # Path is not inside any feature
    return None


# =============================================================================
# Factory Function
# =============================================================================


def x__get_locked_vcs_from_feature__mutmut_51(path: Path) -> VCSBackend | None:
    """
    Read VCS from feature meta.json if path is inside that feature.

    Args:
        path: A path that might be within a feature directory.

    Returns:
        The locked VCSBackend if path is inside a feature with locked VCS, None otherwise.

    Note:
        Only returns a locked VCS if `path` is actually inside the feature directory
        (either in kitty-specs/###-feature/ or in a worktree for that feature).
        Does NOT return VCS for unrelated features.
    """
    current = path.resolve()

    # Strategy 1: Check if path is directly inside kitty-specs/###-feature/
    # e.g., /repo/kitty-specs/015-feature/tasks/WP01.md
    for parent in [current, *current.parents]:
        if parent.parent and parent.parent.name == "kitty-specs":
            # parent is a feature directory like kitty-specs/015-feature/
            meta_path = parent / "meta.json"
            if meta_path.is_file():
                try:
                    meta = json.loads(meta_path.read_text())
                    if "vcs" in meta:
                        return VCSBackend(meta["vcs"])
                except (json.JSONDecodeError, ValueError, OSError):
                    pass
            # Path is in a feature dir but no valid meta.json
            return None

    # Strategy 2: Check if we're in a worktree for a feature
    # e.g., .worktrees/015-feature-name-WP01/src/file.py
    if ".worktrees" in str(current):
        # Find the worktree root (direct child of .worktrees/)
        worktree_root = None
        for parent in [current, *current.parents]:
            if parent.parent and parent.parent.name == ".worktrees":
                worktree_root = parent
                break

        if worktree_root:
            # Extract feature number from worktree name
            # Pattern: ###-feature-name-WP##
            worktree_name = worktree_root.name
            match = re.match(r"(\d{3})-", worktree_name)
            if match:
                feature_num = match.group(1)
                # Find main repo (parent of .worktrees)
                main_repo = worktree_root.parent.parent
                kitty_specs = main_repo / "kitty-specs"
                if kitty_specs.is_dir():
                    # Find the specific feature directory matching feature_num
                    for feature_dir in kitty_specs.iterdir():
                        if feature_dir.is_dir() and feature_dir.name.startswith(
                            f"{feature_num}-"
                        ):
                            meta_path = feature_dir / "meta.json"
                            if meta_path.is_file():
                                try:
                                    meta = json.loads(None)
                                    if "vcs" in meta:
                                        return VCSBackend(meta["vcs"])
                                except (json.JSONDecodeError, ValueError, OSError):
                                    pass
                            # Found feature dir but no valid meta.json
                            return None

    # Path is not inside any feature
    return None


# =============================================================================
# Factory Function
# =============================================================================


def x__get_locked_vcs_from_feature__mutmut_52(path: Path) -> VCSBackend | None:
    """
    Read VCS from feature meta.json if path is inside that feature.

    Args:
        path: A path that might be within a feature directory.

    Returns:
        The locked VCSBackend if path is inside a feature with locked VCS, None otherwise.

    Note:
        Only returns a locked VCS if `path` is actually inside the feature directory
        (either in kitty-specs/###-feature/ or in a worktree for that feature).
        Does NOT return VCS for unrelated features.
    """
    current = path.resolve()

    # Strategy 1: Check if path is directly inside kitty-specs/###-feature/
    # e.g., /repo/kitty-specs/015-feature/tasks/WP01.md
    for parent in [current, *current.parents]:
        if parent.parent and parent.parent.name == "kitty-specs":
            # parent is a feature directory like kitty-specs/015-feature/
            meta_path = parent / "meta.json"
            if meta_path.is_file():
                try:
                    meta = json.loads(meta_path.read_text())
                    if "vcs" in meta:
                        return VCSBackend(meta["vcs"])
                except (json.JSONDecodeError, ValueError, OSError):
                    pass
            # Path is in a feature dir but no valid meta.json
            return None

    # Strategy 2: Check if we're in a worktree for a feature
    # e.g., .worktrees/015-feature-name-WP01/src/file.py
    if ".worktrees" in str(current):
        # Find the worktree root (direct child of .worktrees/)
        worktree_root = None
        for parent in [current, *current.parents]:
            if parent.parent and parent.parent.name == ".worktrees":
                worktree_root = parent
                break

        if worktree_root:
            # Extract feature number from worktree name
            # Pattern: ###-feature-name-WP##
            worktree_name = worktree_root.name
            match = re.match(r"(\d{3})-", worktree_name)
            if match:
                feature_num = match.group(1)
                # Find main repo (parent of .worktrees)
                main_repo = worktree_root.parent.parent
                kitty_specs = main_repo / "kitty-specs"
                if kitty_specs.is_dir():
                    # Find the specific feature directory matching feature_num
                    for feature_dir in kitty_specs.iterdir():
                        if feature_dir.is_dir() and feature_dir.name.startswith(
                            f"{feature_num}-"
                        ):
                            meta_path = feature_dir / "meta.json"
                            if meta_path.is_file():
                                try:
                                    meta = json.loads(meta_path.read_text())
                                    if "XXvcsXX" in meta:
                                        return VCSBackend(meta["vcs"])
                                except (json.JSONDecodeError, ValueError, OSError):
                                    pass
                            # Found feature dir but no valid meta.json
                            return None

    # Path is not inside any feature
    return None


# =============================================================================
# Factory Function
# =============================================================================


def x__get_locked_vcs_from_feature__mutmut_53(path: Path) -> VCSBackend | None:
    """
    Read VCS from feature meta.json if path is inside that feature.

    Args:
        path: A path that might be within a feature directory.

    Returns:
        The locked VCSBackend if path is inside a feature with locked VCS, None otherwise.

    Note:
        Only returns a locked VCS if `path` is actually inside the feature directory
        (either in kitty-specs/###-feature/ or in a worktree for that feature).
        Does NOT return VCS for unrelated features.
    """
    current = path.resolve()

    # Strategy 1: Check if path is directly inside kitty-specs/###-feature/
    # e.g., /repo/kitty-specs/015-feature/tasks/WP01.md
    for parent in [current, *current.parents]:
        if parent.parent and parent.parent.name == "kitty-specs":
            # parent is a feature directory like kitty-specs/015-feature/
            meta_path = parent / "meta.json"
            if meta_path.is_file():
                try:
                    meta = json.loads(meta_path.read_text())
                    if "vcs" in meta:
                        return VCSBackend(meta["vcs"])
                except (json.JSONDecodeError, ValueError, OSError):
                    pass
            # Path is in a feature dir but no valid meta.json
            return None

    # Strategy 2: Check if we're in a worktree for a feature
    # e.g., .worktrees/015-feature-name-WP01/src/file.py
    if ".worktrees" in str(current):
        # Find the worktree root (direct child of .worktrees/)
        worktree_root = None
        for parent in [current, *current.parents]:
            if parent.parent and parent.parent.name == ".worktrees":
                worktree_root = parent
                break

        if worktree_root:
            # Extract feature number from worktree name
            # Pattern: ###-feature-name-WP##
            worktree_name = worktree_root.name
            match = re.match(r"(\d{3})-", worktree_name)
            if match:
                feature_num = match.group(1)
                # Find main repo (parent of .worktrees)
                main_repo = worktree_root.parent.parent
                kitty_specs = main_repo / "kitty-specs"
                if kitty_specs.is_dir():
                    # Find the specific feature directory matching feature_num
                    for feature_dir in kitty_specs.iterdir():
                        if feature_dir.is_dir() and feature_dir.name.startswith(
                            f"{feature_num}-"
                        ):
                            meta_path = feature_dir / "meta.json"
                            if meta_path.is_file():
                                try:
                                    meta = json.loads(meta_path.read_text())
                                    if "VCS" in meta:
                                        return VCSBackend(meta["vcs"])
                                except (json.JSONDecodeError, ValueError, OSError):
                                    pass
                            # Found feature dir but no valid meta.json
                            return None

    # Path is not inside any feature
    return None


# =============================================================================
# Factory Function
# =============================================================================


def x__get_locked_vcs_from_feature__mutmut_54(path: Path) -> VCSBackend | None:
    """
    Read VCS from feature meta.json if path is inside that feature.

    Args:
        path: A path that might be within a feature directory.

    Returns:
        The locked VCSBackend if path is inside a feature with locked VCS, None otherwise.

    Note:
        Only returns a locked VCS if `path` is actually inside the feature directory
        (either in kitty-specs/###-feature/ or in a worktree for that feature).
        Does NOT return VCS for unrelated features.
    """
    current = path.resolve()

    # Strategy 1: Check if path is directly inside kitty-specs/###-feature/
    # e.g., /repo/kitty-specs/015-feature/tasks/WP01.md
    for parent in [current, *current.parents]:
        if parent.parent and parent.parent.name == "kitty-specs":
            # parent is a feature directory like kitty-specs/015-feature/
            meta_path = parent / "meta.json"
            if meta_path.is_file():
                try:
                    meta = json.loads(meta_path.read_text())
                    if "vcs" in meta:
                        return VCSBackend(meta["vcs"])
                except (json.JSONDecodeError, ValueError, OSError):
                    pass
            # Path is in a feature dir but no valid meta.json
            return None

    # Strategy 2: Check if we're in a worktree for a feature
    # e.g., .worktrees/015-feature-name-WP01/src/file.py
    if ".worktrees" in str(current):
        # Find the worktree root (direct child of .worktrees/)
        worktree_root = None
        for parent in [current, *current.parents]:
            if parent.parent and parent.parent.name == ".worktrees":
                worktree_root = parent
                break

        if worktree_root:
            # Extract feature number from worktree name
            # Pattern: ###-feature-name-WP##
            worktree_name = worktree_root.name
            match = re.match(r"(\d{3})-", worktree_name)
            if match:
                feature_num = match.group(1)
                # Find main repo (parent of .worktrees)
                main_repo = worktree_root.parent.parent
                kitty_specs = main_repo / "kitty-specs"
                if kitty_specs.is_dir():
                    # Find the specific feature directory matching feature_num
                    for feature_dir in kitty_specs.iterdir():
                        if feature_dir.is_dir() and feature_dir.name.startswith(
                            f"{feature_num}-"
                        ):
                            meta_path = feature_dir / "meta.json"
                            if meta_path.is_file():
                                try:
                                    meta = json.loads(meta_path.read_text())
                                    if "vcs" not in meta:
                                        return VCSBackend(meta["vcs"])
                                except (json.JSONDecodeError, ValueError, OSError):
                                    pass
                            # Found feature dir but no valid meta.json
                            return None

    # Path is not inside any feature
    return None


# =============================================================================
# Factory Function
# =============================================================================


def x__get_locked_vcs_from_feature__mutmut_55(path: Path) -> VCSBackend | None:
    """
    Read VCS from feature meta.json if path is inside that feature.

    Args:
        path: A path that might be within a feature directory.

    Returns:
        The locked VCSBackend if path is inside a feature with locked VCS, None otherwise.

    Note:
        Only returns a locked VCS if `path` is actually inside the feature directory
        (either in kitty-specs/###-feature/ or in a worktree for that feature).
        Does NOT return VCS for unrelated features.
    """
    current = path.resolve()

    # Strategy 1: Check if path is directly inside kitty-specs/###-feature/
    # e.g., /repo/kitty-specs/015-feature/tasks/WP01.md
    for parent in [current, *current.parents]:
        if parent.parent and parent.parent.name == "kitty-specs":
            # parent is a feature directory like kitty-specs/015-feature/
            meta_path = parent / "meta.json"
            if meta_path.is_file():
                try:
                    meta = json.loads(meta_path.read_text())
                    if "vcs" in meta:
                        return VCSBackend(meta["vcs"])
                except (json.JSONDecodeError, ValueError, OSError):
                    pass
            # Path is in a feature dir but no valid meta.json
            return None

    # Strategy 2: Check if we're in a worktree for a feature
    # e.g., .worktrees/015-feature-name-WP01/src/file.py
    if ".worktrees" in str(current):
        # Find the worktree root (direct child of .worktrees/)
        worktree_root = None
        for parent in [current, *current.parents]:
            if parent.parent and parent.parent.name == ".worktrees":
                worktree_root = parent
                break

        if worktree_root:
            # Extract feature number from worktree name
            # Pattern: ###-feature-name-WP##
            worktree_name = worktree_root.name
            match = re.match(r"(\d{3})-", worktree_name)
            if match:
                feature_num = match.group(1)
                # Find main repo (parent of .worktrees)
                main_repo = worktree_root.parent.parent
                kitty_specs = main_repo / "kitty-specs"
                if kitty_specs.is_dir():
                    # Find the specific feature directory matching feature_num
                    for feature_dir in kitty_specs.iterdir():
                        if feature_dir.is_dir() and feature_dir.name.startswith(
                            f"{feature_num}-"
                        ):
                            meta_path = feature_dir / "meta.json"
                            if meta_path.is_file():
                                try:
                                    meta = json.loads(meta_path.read_text())
                                    if "vcs" in meta:
                                        return VCSBackend(None)
                                except (json.JSONDecodeError, ValueError, OSError):
                                    pass
                            # Found feature dir but no valid meta.json
                            return None

    # Path is not inside any feature
    return None


# =============================================================================
# Factory Function
# =============================================================================


def x__get_locked_vcs_from_feature__mutmut_56(path: Path) -> VCSBackend | None:
    """
    Read VCS from feature meta.json if path is inside that feature.

    Args:
        path: A path that might be within a feature directory.

    Returns:
        The locked VCSBackend if path is inside a feature with locked VCS, None otherwise.

    Note:
        Only returns a locked VCS if `path` is actually inside the feature directory
        (either in kitty-specs/###-feature/ or in a worktree for that feature).
        Does NOT return VCS for unrelated features.
    """
    current = path.resolve()

    # Strategy 1: Check if path is directly inside kitty-specs/###-feature/
    # e.g., /repo/kitty-specs/015-feature/tasks/WP01.md
    for parent in [current, *current.parents]:
        if parent.parent and parent.parent.name == "kitty-specs":
            # parent is a feature directory like kitty-specs/015-feature/
            meta_path = parent / "meta.json"
            if meta_path.is_file():
                try:
                    meta = json.loads(meta_path.read_text())
                    if "vcs" in meta:
                        return VCSBackend(meta["vcs"])
                except (json.JSONDecodeError, ValueError, OSError):
                    pass
            # Path is in a feature dir but no valid meta.json
            return None

    # Strategy 2: Check if we're in a worktree for a feature
    # e.g., .worktrees/015-feature-name-WP01/src/file.py
    if ".worktrees" in str(current):
        # Find the worktree root (direct child of .worktrees/)
        worktree_root = None
        for parent in [current, *current.parents]:
            if parent.parent and parent.parent.name == ".worktrees":
                worktree_root = parent
                break

        if worktree_root:
            # Extract feature number from worktree name
            # Pattern: ###-feature-name-WP##
            worktree_name = worktree_root.name
            match = re.match(r"(\d{3})-", worktree_name)
            if match:
                feature_num = match.group(1)
                # Find main repo (parent of .worktrees)
                main_repo = worktree_root.parent.parent
                kitty_specs = main_repo / "kitty-specs"
                if kitty_specs.is_dir():
                    # Find the specific feature directory matching feature_num
                    for feature_dir in kitty_specs.iterdir():
                        if feature_dir.is_dir() and feature_dir.name.startswith(
                            f"{feature_num}-"
                        ):
                            meta_path = feature_dir / "meta.json"
                            if meta_path.is_file():
                                try:
                                    meta = json.loads(meta_path.read_text())
                                    if "vcs" in meta:
                                        return VCSBackend(meta["XXvcsXX"])
                                except (json.JSONDecodeError, ValueError, OSError):
                                    pass
                            # Found feature dir but no valid meta.json
                            return None

    # Path is not inside any feature
    return None


# =============================================================================
# Factory Function
# =============================================================================


def x__get_locked_vcs_from_feature__mutmut_57(path: Path) -> VCSBackend | None:
    """
    Read VCS from feature meta.json if path is inside that feature.

    Args:
        path: A path that might be within a feature directory.

    Returns:
        The locked VCSBackend if path is inside a feature with locked VCS, None otherwise.

    Note:
        Only returns a locked VCS if `path` is actually inside the feature directory
        (either in kitty-specs/###-feature/ or in a worktree for that feature).
        Does NOT return VCS for unrelated features.
    """
    current = path.resolve()

    # Strategy 1: Check if path is directly inside kitty-specs/###-feature/
    # e.g., /repo/kitty-specs/015-feature/tasks/WP01.md
    for parent in [current, *current.parents]:
        if parent.parent and parent.parent.name == "kitty-specs":
            # parent is a feature directory like kitty-specs/015-feature/
            meta_path = parent / "meta.json"
            if meta_path.is_file():
                try:
                    meta = json.loads(meta_path.read_text())
                    if "vcs" in meta:
                        return VCSBackend(meta["vcs"])
                except (json.JSONDecodeError, ValueError, OSError):
                    pass
            # Path is in a feature dir but no valid meta.json
            return None

    # Strategy 2: Check if we're in a worktree for a feature
    # e.g., .worktrees/015-feature-name-WP01/src/file.py
    if ".worktrees" in str(current):
        # Find the worktree root (direct child of .worktrees/)
        worktree_root = None
        for parent in [current, *current.parents]:
            if parent.parent and parent.parent.name == ".worktrees":
                worktree_root = parent
                break

        if worktree_root:
            # Extract feature number from worktree name
            # Pattern: ###-feature-name-WP##
            worktree_name = worktree_root.name
            match = re.match(r"(\d{3})-", worktree_name)
            if match:
                feature_num = match.group(1)
                # Find main repo (parent of .worktrees)
                main_repo = worktree_root.parent.parent
                kitty_specs = main_repo / "kitty-specs"
                if kitty_specs.is_dir():
                    # Find the specific feature directory matching feature_num
                    for feature_dir in kitty_specs.iterdir():
                        if feature_dir.is_dir() and feature_dir.name.startswith(
                            f"{feature_num}-"
                        ):
                            meta_path = feature_dir / "meta.json"
                            if meta_path.is_file():
                                try:
                                    meta = json.loads(meta_path.read_text())
                                    if "vcs" in meta:
                                        return VCSBackend(meta["VCS"])
                                except (json.JSONDecodeError, ValueError, OSError):
                                    pass
                            # Found feature dir but no valid meta.json
                            return None

    # Path is not inside any feature
    return None

x__get_locked_vcs_from_feature__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x__get_locked_vcs_from_feature__mutmut_1': x__get_locked_vcs_from_feature__mutmut_1, 
    'x__get_locked_vcs_from_feature__mutmut_2': x__get_locked_vcs_from_feature__mutmut_2, 
    'x__get_locked_vcs_from_feature__mutmut_3': x__get_locked_vcs_from_feature__mutmut_3, 
    'x__get_locked_vcs_from_feature__mutmut_4': x__get_locked_vcs_from_feature__mutmut_4, 
    'x__get_locked_vcs_from_feature__mutmut_5': x__get_locked_vcs_from_feature__mutmut_5, 
    'x__get_locked_vcs_from_feature__mutmut_6': x__get_locked_vcs_from_feature__mutmut_6, 
    'x__get_locked_vcs_from_feature__mutmut_7': x__get_locked_vcs_from_feature__mutmut_7, 
    'x__get_locked_vcs_from_feature__mutmut_8': x__get_locked_vcs_from_feature__mutmut_8, 
    'x__get_locked_vcs_from_feature__mutmut_9': x__get_locked_vcs_from_feature__mutmut_9, 
    'x__get_locked_vcs_from_feature__mutmut_10': x__get_locked_vcs_from_feature__mutmut_10, 
    'x__get_locked_vcs_from_feature__mutmut_11': x__get_locked_vcs_from_feature__mutmut_11, 
    'x__get_locked_vcs_from_feature__mutmut_12': x__get_locked_vcs_from_feature__mutmut_12, 
    'x__get_locked_vcs_from_feature__mutmut_13': x__get_locked_vcs_from_feature__mutmut_13, 
    'x__get_locked_vcs_from_feature__mutmut_14': x__get_locked_vcs_from_feature__mutmut_14, 
    'x__get_locked_vcs_from_feature__mutmut_15': x__get_locked_vcs_from_feature__mutmut_15, 
    'x__get_locked_vcs_from_feature__mutmut_16': x__get_locked_vcs_from_feature__mutmut_16, 
    'x__get_locked_vcs_from_feature__mutmut_17': x__get_locked_vcs_from_feature__mutmut_17, 
    'x__get_locked_vcs_from_feature__mutmut_18': x__get_locked_vcs_from_feature__mutmut_18, 
    'x__get_locked_vcs_from_feature__mutmut_19': x__get_locked_vcs_from_feature__mutmut_19, 
    'x__get_locked_vcs_from_feature__mutmut_20': x__get_locked_vcs_from_feature__mutmut_20, 
    'x__get_locked_vcs_from_feature__mutmut_21': x__get_locked_vcs_from_feature__mutmut_21, 
    'x__get_locked_vcs_from_feature__mutmut_22': x__get_locked_vcs_from_feature__mutmut_22, 
    'x__get_locked_vcs_from_feature__mutmut_23': x__get_locked_vcs_from_feature__mutmut_23, 
    'x__get_locked_vcs_from_feature__mutmut_24': x__get_locked_vcs_from_feature__mutmut_24, 
    'x__get_locked_vcs_from_feature__mutmut_25': x__get_locked_vcs_from_feature__mutmut_25, 
    'x__get_locked_vcs_from_feature__mutmut_26': x__get_locked_vcs_from_feature__mutmut_26, 
    'x__get_locked_vcs_from_feature__mutmut_27': x__get_locked_vcs_from_feature__mutmut_27, 
    'x__get_locked_vcs_from_feature__mutmut_28': x__get_locked_vcs_from_feature__mutmut_28, 
    'x__get_locked_vcs_from_feature__mutmut_29': x__get_locked_vcs_from_feature__mutmut_29, 
    'x__get_locked_vcs_from_feature__mutmut_30': x__get_locked_vcs_from_feature__mutmut_30, 
    'x__get_locked_vcs_from_feature__mutmut_31': x__get_locked_vcs_from_feature__mutmut_31, 
    'x__get_locked_vcs_from_feature__mutmut_32': x__get_locked_vcs_from_feature__mutmut_32, 
    'x__get_locked_vcs_from_feature__mutmut_33': x__get_locked_vcs_from_feature__mutmut_33, 
    'x__get_locked_vcs_from_feature__mutmut_34': x__get_locked_vcs_from_feature__mutmut_34, 
    'x__get_locked_vcs_from_feature__mutmut_35': x__get_locked_vcs_from_feature__mutmut_35, 
    'x__get_locked_vcs_from_feature__mutmut_36': x__get_locked_vcs_from_feature__mutmut_36, 
    'x__get_locked_vcs_from_feature__mutmut_37': x__get_locked_vcs_from_feature__mutmut_37, 
    'x__get_locked_vcs_from_feature__mutmut_38': x__get_locked_vcs_from_feature__mutmut_38, 
    'x__get_locked_vcs_from_feature__mutmut_39': x__get_locked_vcs_from_feature__mutmut_39, 
    'x__get_locked_vcs_from_feature__mutmut_40': x__get_locked_vcs_from_feature__mutmut_40, 
    'x__get_locked_vcs_from_feature__mutmut_41': x__get_locked_vcs_from_feature__mutmut_41, 
    'x__get_locked_vcs_from_feature__mutmut_42': x__get_locked_vcs_from_feature__mutmut_42, 
    'x__get_locked_vcs_from_feature__mutmut_43': x__get_locked_vcs_from_feature__mutmut_43, 
    'x__get_locked_vcs_from_feature__mutmut_44': x__get_locked_vcs_from_feature__mutmut_44, 
    'x__get_locked_vcs_from_feature__mutmut_45': x__get_locked_vcs_from_feature__mutmut_45, 
    'x__get_locked_vcs_from_feature__mutmut_46': x__get_locked_vcs_from_feature__mutmut_46, 
    'x__get_locked_vcs_from_feature__mutmut_47': x__get_locked_vcs_from_feature__mutmut_47, 
    'x__get_locked_vcs_from_feature__mutmut_48': x__get_locked_vcs_from_feature__mutmut_48, 
    'x__get_locked_vcs_from_feature__mutmut_49': x__get_locked_vcs_from_feature__mutmut_49, 
    'x__get_locked_vcs_from_feature__mutmut_50': x__get_locked_vcs_from_feature__mutmut_50, 
    'x__get_locked_vcs_from_feature__mutmut_51': x__get_locked_vcs_from_feature__mutmut_51, 
    'x__get_locked_vcs_from_feature__mutmut_52': x__get_locked_vcs_from_feature__mutmut_52, 
    'x__get_locked_vcs_from_feature__mutmut_53': x__get_locked_vcs_from_feature__mutmut_53, 
    'x__get_locked_vcs_from_feature__mutmut_54': x__get_locked_vcs_from_feature__mutmut_54, 
    'x__get_locked_vcs_from_feature__mutmut_55': x__get_locked_vcs_from_feature__mutmut_55, 
    'x__get_locked_vcs_from_feature__mutmut_56': x__get_locked_vcs_from_feature__mutmut_56, 
    'x__get_locked_vcs_from_feature__mutmut_57': x__get_locked_vcs_from_feature__mutmut_57
}
x__get_locked_vcs_from_feature__mutmut_orig.__name__ = 'x__get_locked_vcs_from_feature'


def _instantiate_backend(backend: VCSBackend) -> "VCSProtocol":
    args = [backend]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x__instantiate_backend__mutmut_orig, x__instantiate_backend__mutmut_mutants, args, kwargs, None)


def x__instantiate_backend__mutmut_orig(backend: VCSBackend) -> "VCSProtocol":
    """
    Instantiate the appropriate VCS implementation.

    Args:
        backend: The backend to instantiate.

    Returns:
        A VCSProtocol implementation.

    Raises:
        VCSNotFoundError: If the requested backend is not available.
    """
    if backend == VCSBackend.JUJUTSU:
        if not is_jj_available():
            raise VCSNotFoundError(
                "jj is not available. Install jj from https://github.com/martinvonz/jj"
            )
        # Lazy import to avoid circular imports
        from .jujutsu import JujutsuVCS

        return JujutsuVCS()
    elif backend == VCSBackend.GIT:
        if not is_git_available():
            raise VCSNotFoundError("git is not available. Please install git.")
        # Lazy import to avoid circular imports
        from .git import GitVCS

        return GitVCS()
    else:
        raise VCSNotFoundError(f"Unknown VCS backend: {backend}")


def x__instantiate_backend__mutmut_1(backend: VCSBackend) -> "VCSProtocol":
    """
    Instantiate the appropriate VCS implementation.

    Args:
        backend: The backend to instantiate.

    Returns:
        A VCSProtocol implementation.

    Raises:
        VCSNotFoundError: If the requested backend is not available.
    """
    if backend != VCSBackend.JUJUTSU:
        if not is_jj_available():
            raise VCSNotFoundError(
                "jj is not available. Install jj from https://github.com/martinvonz/jj"
            )
        # Lazy import to avoid circular imports
        from .jujutsu import JujutsuVCS

        return JujutsuVCS()
    elif backend == VCSBackend.GIT:
        if not is_git_available():
            raise VCSNotFoundError("git is not available. Please install git.")
        # Lazy import to avoid circular imports
        from .git import GitVCS

        return GitVCS()
    else:
        raise VCSNotFoundError(f"Unknown VCS backend: {backend}")


def x__instantiate_backend__mutmut_2(backend: VCSBackend) -> "VCSProtocol":
    """
    Instantiate the appropriate VCS implementation.

    Args:
        backend: The backend to instantiate.

    Returns:
        A VCSProtocol implementation.

    Raises:
        VCSNotFoundError: If the requested backend is not available.
    """
    if backend == VCSBackend.JUJUTSU:
        if is_jj_available():
            raise VCSNotFoundError(
                "jj is not available. Install jj from https://github.com/martinvonz/jj"
            )
        # Lazy import to avoid circular imports
        from .jujutsu import JujutsuVCS

        return JujutsuVCS()
    elif backend == VCSBackend.GIT:
        if not is_git_available():
            raise VCSNotFoundError("git is not available. Please install git.")
        # Lazy import to avoid circular imports
        from .git import GitVCS

        return GitVCS()
    else:
        raise VCSNotFoundError(f"Unknown VCS backend: {backend}")


def x__instantiate_backend__mutmut_3(backend: VCSBackend) -> "VCSProtocol":
    """
    Instantiate the appropriate VCS implementation.

    Args:
        backend: The backend to instantiate.

    Returns:
        A VCSProtocol implementation.

    Raises:
        VCSNotFoundError: If the requested backend is not available.
    """
    if backend == VCSBackend.JUJUTSU:
        if not is_jj_available():
            raise VCSNotFoundError(
                None
            )
        # Lazy import to avoid circular imports
        from .jujutsu import JujutsuVCS

        return JujutsuVCS()
    elif backend == VCSBackend.GIT:
        if not is_git_available():
            raise VCSNotFoundError("git is not available. Please install git.")
        # Lazy import to avoid circular imports
        from .git import GitVCS

        return GitVCS()
    else:
        raise VCSNotFoundError(f"Unknown VCS backend: {backend}")


def x__instantiate_backend__mutmut_4(backend: VCSBackend) -> "VCSProtocol":
    """
    Instantiate the appropriate VCS implementation.

    Args:
        backend: The backend to instantiate.

    Returns:
        A VCSProtocol implementation.

    Raises:
        VCSNotFoundError: If the requested backend is not available.
    """
    if backend == VCSBackend.JUJUTSU:
        if not is_jj_available():
            raise VCSNotFoundError(
                "XXjj is not available. Install jj from https://github.com/martinvonz/jjXX"
            )
        # Lazy import to avoid circular imports
        from .jujutsu import JujutsuVCS

        return JujutsuVCS()
    elif backend == VCSBackend.GIT:
        if not is_git_available():
            raise VCSNotFoundError("git is not available. Please install git.")
        # Lazy import to avoid circular imports
        from .git import GitVCS

        return GitVCS()
    else:
        raise VCSNotFoundError(f"Unknown VCS backend: {backend}")


def x__instantiate_backend__mutmut_5(backend: VCSBackend) -> "VCSProtocol":
    """
    Instantiate the appropriate VCS implementation.

    Args:
        backend: The backend to instantiate.

    Returns:
        A VCSProtocol implementation.

    Raises:
        VCSNotFoundError: If the requested backend is not available.
    """
    if backend == VCSBackend.JUJUTSU:
        if not is_jj_available():
            raise VCSNotFoundError(
                "jj is not available. install jj from https://github.com/martinvonz/jj"
            )
        # Lazy import to avoid circular imports
        from .jujutsu import JujutsuVCS

        return JujutsuVCS()
    elif backend == VCSBackend.GIT:
        if not is_git_available():
            raise VCSNotFoundError("git is not available. Please install git.")
        # Lazy import to avoid circular imports
        from .git import GitVCS

        return GitVCS()
    else:
        raise VCSNotFoundError(f"Unknown VCS backend: {backend}")


def x__instantiate_backend__mutmut_6(backend: VCSBackend) -> "VCSProtocol":
    """
    Instantiate the appropriate VCS implementation.

    Args:
        backend: The backend to instantiate.

    Returns:
        A VCSProtocol implementation.

    Raises:
        VCSNotFoundError: If the requested backend is not available.
    """
    if backend == VCSBackend.JUJUTSU:
        if not is_jj_available():
            raise VCSNotFoundError(
                "JJ IS NOT AVAILABLE. INSTALL JJ FROM HTTPS://GITHUB.COM/MARTINVONZ/JJ"
            )
        # Lazy import to avoid circular imports
        from .jujutsu import JujutsuVCS

        return JujutsuVCS()
    elif backend == VCSBackend.GIT:
        if not is_git_available():
            raise VCSNotFoundError("git is not available. Please install git.")
        # Lazy import to avoid circular imports
        from .git import GitVCS

        return GitVCS()
    else:
        raise VCSNotFoundError(f"Unknown VCS backend: {backend}")


def x__instantiate_backend__mutmut_7(backend: VCSBackend) -> "VCSProtocol":
    """
    Instantiate the appropriate VCS implementation.

    Args:
        backend: The backend to instantiate.

    Returns:
        A VCSProtocol implementation.

    Raises:
        VCSNotFoundError: If the requested backend is not available.
    """
    if backend == VCSBackend.JUJUTSU:
        if not is_jj_available():
            raise VCSNotFoundError(
                "jj is not available. Install jj from https://github.com/martinvonz/jj"
            )
        # Lazy import to avoid circular imports
        from .jujutsu import JujutsuVCS

        return JujutsuVCS()
    elif backend != VCSBackend.GIT:
        if not is_git_available():
            raise VCSNotFoundError("git is not available. Please install git.")
        # Lazy import to avoid circular imports
        from .git import GitVCS

        return GitVCS()
    else:
        raise VCSNotFoundError(f"Unknown VCS backend: {backend}")


def x__instantiate_backend__mutmut_8(backend: VCSBackend) -> "VCSProtocol":
    """
    Instantiate the appropriate VCS implementation.

    Args:
        backend: The backend to instantiate.

    Returns:
        A VCSProtocol implementation.

    Raises:
        VCSNotFoundError: If the requested backend is not available.
    """
    if backend == VCSBackend.JUJUTSU:
        if not is_jj_available():
            raise VCSNotFoundError(
                "jj is not available. Install jj from https://github.com/martinvonz/jj"
            )
        # Lazy import to avoid circular imports
        from .jujutsu import JujutsuVCS

        return JujutsuVCS()
    elif backend == VCSBackend.GIT:
        if is_git_available():
            raise VCSNotFoundError("git is not available. Please install git.")
        # Lazy import to avoid circular imports
        from .git import GitVCS

        return GitVCS()
    else:
        raise VCSNotFoundError(f"Unknown VCS backend: {backend}")


def x__instantiate_backend__mutmut_9(backend: VCSBackend) -> "VCSProtocol":
    """
    Instantiate the appropriate VCS implementation.

    Args:
        backend: The backend to instantiate.

    Returns:
        A VCSProtocol implementation.

    Raises:
        VCSNotFoundError: If the requested backend is not available.
    """
    if backend == VCSBackend.JUJUTSU:
        if not is_jj_available():
            raise VCSNotFoundError(
                "jj is not available. Install jj from https://github.com/martinvonz/jj"
            )
        # Lazy import to avoid circular imports
        from .jujutsu import JujutsuVCS

        return JujutsuVCS()
    elif backend == VCSBackend.GIT:
        if not is_git_available():
            raise VCSNotFoundError(None)
        # Lazy import to avoid circular imports
        from .git import GitVCS

        return GitVCS()
    else:
        raise VCSNotFoundError(f"Unknown VCS backend: {backend}")


def x__instantiate_backend__mutmut_10(backend: VCSBackend) -> "VCSProtocol":
    """
    Instantiate the appropriate VCS implementation.

    Args:
        backend: The backend to instantiate.

    Returns:
        A VCSProtocol implementation.

    Raises:
        VCSNotFoundError: If the requested backend is not available.
    """
    if backend == VCSBackend.JUJUTSU:
        if not is_jj_available():
            raise VCSNotFoundError(
                "jj is not available. Install jj from https://github.com/martinvonz/jj"
            )
        # Lazy import to avoid circular imports
        from .jujutsu import JujutsuVCS

        return JujutsuVCS()
    elif backend == VCSBackend.GIT:
        if not is_git_available():
            raise VCSNotFoundError("XXgit is not available. Please install git.XX")
        # Lazy import to avoid circular imports
        from .git import GitVCS

        return GitVCS()
    else:
        raise VCSNotFoundError(f"Unknown VCS backend: {backend}")


def x__instantiate_backend__mutmut_11(backend: VCSBackend) -> "VCSProtocol":
    """
    Instantiate the appropriate VCS implementation.

    Args:
        backend: The backend to instantiate.

    Returns:
        A VCSProtocol implementation.

    Raises:
        VCSNotFoundError: If the requested backend is not available.
    """
    if backend == VCSBackend.JUJUTSU:
        if not is_jj_available():
            raise VCSNotFoundError(
                "jj is not available. Install jj from https://github.com/martinvonz/jj"
            )
        # Lazy import to avoid circular imports
        from .jujutsu import JujutsuVCS

        return JujutsuVCS()
    elif backend == VCSBackend.GIT:
        if not is_git_available():
            raise VCSNotFoundError("git is not available. please install git.")
        # Lazy import to avoid circular imports
        from .git import GitVCS

        return GitVCS()
    else:
        raise VCSNotFoundError(f"Unknown VCS backend: {backend}")


def x__instantiate_backend__mutmut_12(backend: VCSBackend) -> "VCSProtocol":
    """
    Instantiate the appropriate VCS implementation.

    Args:
        backend: The backend to instantiate.

    Returns:
        A VCSProtocol implementation.

    Raises:
        VCSNotFoundError: If the requested backend is not available.
    """
    if backend == VCSBackend.JUJUTSU:
        if not is_jj_available():
            raise VCSNotFoundError(
                "jj is not available. Install jj from https://github.com/martinvonz/jj"
            )
        # Lazy import to avoid circular imports
        from .jujutsu import JujutsuVCS

        return JujutsuVCS()
    elif backend == VCSBackend.GIT:
        if not is_git_available():
            raise VCSNotFoundError("GIT IS NOT AVAILABLE. PLEASE INSTALL GIT.")
        # Lazy import to avoid circular imports
        from .git import GitVCS

        return GitVCS()
    else:
        raise VCSNotFoundError(f"Unknown VCS backend: {backend}")


def x__instantiate_backend__mutmut_13(backend: VCSBackend) -> "VCSProtocol":
    """
    Instantiate the appropriate VCS implementation.

    Args:
        backend: The backend to instantiate.

    Returns:
        A VCSProtocol implementation.

    Raises:
        VCSNotFoundError: If the requested backend is not available.
    """
    if backend == VCSBackend.JUJUTSU:
        if not is_jj_available():
            raise VCSNotFoundError(
                "jj is not available. Install jj from https://github.com/martinvonz/jj"
            )
        # Lazy import to avoid circular imports
        from .jujutsu import JujutsuVCS

        return JujutsuVCS()
    elif backend == VCSBackend.GIT:
        if not is_git_available():
            raise VCSNotFoundError("git is not available. Please install git.")
        # Lazy import to avoid circular imports
        from .git import GitVCS

        return GitVCS()
    else:
        raise VCSNotFoundError(None)

x__instantiate_backend__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x__instantiate_backend__mutmut_1': x__instantiate_backend__mutmut_1, 
    'x__instantiate_backend__mutmut_2': x__instantiate_backend__mutmut_2, 
    'x__instantiate_backend__mutmut_3': x__instantiate_backend__mutmut_3, 
    'x__instantiate_backend__mutmut_4': x__instantiate_backend__mutmut_4, 
    'x__instantiate_backend__mutmut_5': x__instantiate_backend__mutmut_5, 
    'x__instantiate_backend__mutmut_6': x__instantiate_backend__mutmut_6, 
    'x__instantiate_backend__mutmut_7': x__instantiate_backend__mutmut_7, 
    'x__instantiate_backend__mutmut_8': x__instantiate_backend__mutmut_8, 
    'x__instantiate_backend__mutmut_9': x__instantiate_backend__mutmut_9, 
    'x__instantiate_backend__mutmut_10': x__instantiate_backend__mutmut_10, 
    'x__instantiate_backend__mutmut_11': x__instantiate_backend__mutmut_11, 
    'x__instantiate_backend__mutmut_12': x__instantiate_backend__mutmut_12, 
    'x__instantiate_backend__mutmut_13': x__instantiate_backend__mutmut_13
}
x__instantiate_backend__mutmut_orig.__name__ = 'x__instantiate_backend'


def get_vcs(
    path: Path,
    backend: VCSBackend | None = None,
    prefer_jj: bool = True,
) -> "VCSProtocol":
    args = [path, backend, prefer_jj]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_get_vcs__mutmut_orig, x_get_vcs__mutmut_mutants, args, kwargs, None)


def x_get_vcs__mutmut_orig(
    path: Path,
    backend: VCSBackend | None = None,
    prefer_jj: bool = True,
) -> "VCSProtocol":
    """
    Factory function to get appropriate VCS implementation.

    Args:
        path: Path within a repository or feature directory.
        backend: Explicit backend choice (None = auto-detect).
        prefer_jj: If auto-detecting, prefer jj over git when both available.

    Returns:
        VCSProtocol implementation (GitVCS or JujutsuVCS).

    Raises:
        VCSNotFoundError: Neither jj nor git available.
        VCSBackendMismatchError: Requested backend doesn't match feature's locked VCS.

    Detection order:
        1. If backend specified, use that
        2. If path is in a feature, read meta.json for locked VCS
        3. If jj available and prefer_jj=True, use jj
        4. If git available, use git
        5. Raise VCSNotFoundError
    """
    # 1. If explicit backend specified, use that
    if backend is not None:
        # Check if there's a locked VCS that conflicts
        locked = _get_locked_vcs_from_feature(path)
        if locked is not None and locked != backend:
            raise VCSBackendMismatchError(
                f"Requested backend '{backend.value}' doesn't match feature's "
                f"locked VCS '{locked.value}'. "
                f"Features must use the same VCS throughout their lifecycle."
            )
        return _instantiate_backend(backend)

    # 2. Check for locked VCS in feature meta.json
    locked = _get_locked_vcs_from_feature(path)
    if locked is not None:
        return _instantiate_backend(locked)

    # 3. Auto-detect based on availability
    # DISABLED: jj detection disabled (incompatible with sparse checkouts)
    # if prefer_jj and is_jj_available():
    #     # Lazy import to avoid circular imports
    #     from .jujutsu import JujutsuVCS
    #
    #     return JujutsuVCS()

    if is_git_available():
        # Lazy import to avoid circular imports
        from .git import GitVCS

        return GitVCS()

    # 4. git not available
    raise VCSNotFoundError(
        "git is not available. "
        "Please install git: https://git-scm.com/downloads"
    )


def x_get_vcs__mutmut_1(
    path: Path,
    backend: VCSBackend | None = None,
    prefer_jj: bool = False,
) -> "VCSProtocol":
    """
    Factory function to get appropriate VCS implementation.

    Args:
        path: Path within a repository or feature directory.
        backend: Explicit backend choice (None = auto-detect).
        prefer_jj: If auto-detecting, prefer jj over git when both available.

    Returns:
        VCSProtocol implementation (GitVCS or JujutsuVCS).

    Raises:
        VCSNotFoundError: Neither jj nor git available.
        VCSBackendMismatchError: Requested backend doesn't match feature's locked VCS.

    Detection order:
        1. If backend specified, use that
        2. If path is in a feature, read meta.json for locked VCS
        3. If jj available and prefer_jj=True, use jj
        4. If git available, use git
        5. Raise VCSNotFoundError
    """
    # 1. If explicit backend specified, use that
    if backend is not None:
        # Check if there's a locked VCS that conflicts
        locked = _get_locked_vcs_from_feature(path)
        if locked is not None and locked != backend:
            raise VCSBackendMismatchError(
                f"Requested backend '{backend.value}' doesn't match feature's "
                f"locked VCS '{locked.value}'. "
                f"Features must use the same VCS throughout their lifecycle."
            )
        return _instantiate_backend(backend)

    # 2. Check for locked VCS in feature meta.json
    locked = _get_locked_vcs_from_feature(path)
    if locked is not None:
        return _instantiate_backend(locked)

    # 3. Auto-detect based on availability
    # DISABLED: jj detection disabled (incompatible with sparse checkouts)
    # if prefer_jj and is_jj_available():
    #     # Lazy import to avoid circular imports
    #     from .jujutsu import JujutsuVCS
    #
    #     return JujutsuVCS()

    if is_git_available():
        # Lazy import to avoid circular imports
        from .git import GitVCS

        return GitVCS()

    # 4. git not available
    raise VCSNotFoundError(
        "git is not available. "
        "Please install git: https://git-scm.com/downloads"
    )


def x_get_vcs__mutmut_2(
    path: Path,
    backend: VCSBackend | None = None,
    prefer_jj: bool = True,
) -> "VCSProtocol":
    """
    Factory function to get appropriate VCS implementation.

    Args:
        path: Path within a repository or feature directory.
        backend: Explicit backend choice (None = auto-detect).
        prefer_jj: If auto-detecting, prefer jj over git when both available.

    Returns:
        VCSProtocol implementation (GitVCS or JujutsuVCS).

    Raises:
        VCSNotFoundError: Neither jj nor git available.
        VCSBackendMismatchError: Requested backend doesn't match feature's locked VCS.

    Detection order:
        1. If backend specified, use that
        2. If path is in a feature, read meta.json for locked VCS
        3. If jj available and prefer_jj=True, use jj
        4. If git available, use git
        5. Raise VCSNotFoundError
    """
    # 1. If explicit backend specified, use that
    if backend is None:
        # Check if there's a locked VCS that conflicts
        locked = _get_locked_vcs_from_feature(path)
        if locked is not None and locked != backend:
            raise VCSBackendMismatchError(
                f"Requested backend '{backend.value}' doesn't match feature's "
                f"locked VCS '{locked.value}'. "
                f"Features must use the same VCS throughout their lifecycle."
            )
        return _instantiate_backend(backend)

    # 2. Check for locked VCS in feature meta.json
    locked = _get_locked_vcs_from_feature(path)
    if locked is not None:
        return _instantiate_backend(locked)

    # 3. Auto-detect based on availability
    # DISABLED: jj detection disabled (incompatible with sparse checkouts)
    # if prefer_jj and is_jj_available():
    #     # Lazy import to avoid circular imports
    #     from .jujutsu import JujutsuVCS
    #
    #     return JujutsuVCS()

    if is_git_available():
        # Lazy import to avoid circular imports
        from .git import GitVCS

        return GitVCS()

    # 4. git not available
    raise VCSNotFoundError(
        "git is not available. "
        "Please install git: https://git-scm.com/downloads"
    )


def x_get_vcs__mutmut_3(
    path: Path,
    backend: VCSBackend | None = None,
    prefer_jj: bool = True,
) -> "VCSProtocol":
    """
    Factory function to get appropriate VCS implementation.

    Args:
        path: Path within a repository or feature directory.
        backend: Explicit backend choice (None = auto-detect).
        prefer_jj: If auto-detecting, prefer jj over git when both available.

    Returns:
        VCSProtocol implementation (GitVCS or JujutsuVCS).

    Raises:
        VCSNotFoundError: Neither jj nor git available.
        VCSBackendMismatchError: Requested backend doesn't match feature's locked VCS.

    Detection order:
        1. If backend specified, use that
        2. If path is in a feature, read meta.json for locked VCS
        3. If jj available and prefer_jj=True, use jj
        4. If git available, use git
        5. Raise VCSNotFoundError
    """
    # 1. If explicit backend specified, use that
    if backend is not None:
        # Check if there's a locked VCS that conflicts
        locked = None
        if locked is not None and locked != backend:
            raise VCSBackendMismatchError(
                f"Requested backend '{backend.value}' doesn't match feature's "
                f"locked VCS '{locked.value}'. "
                f"Features must use the same VCS throughout their lifecycle."
            )
        return _instantiate_backend(backend)

    # 2. Check for locked VCS in feature meta.json
    locked = _get_locked_vcs_from_feature(path)
    if locked is not None:
        return _instantiate_backend(locked)

    # 3. Auto-detect based on availability
    # DISABLED: jj detection disabled (incompatible with sparse checkouts)
    # if prefer_jj and is_jj_available():
    #     # Lazy import to avoid circular imports
    #     from .jujutsu import JujutsuVCS
    #
    #     return JujutsuVCS()

    if is_git_available():
        # Lazy import to avoid circular imports
        from .git import GitVCS

        return GitVCS()

    # 4. git not available
    raise VCSNotFoundError(
        "git is not available. "
        "Please install git: https://git-scm.com/downloads"
    )


def x_get_vcs__mutmut_4(
    path: Path,
    backend: VCSBackend | None = None,
    prefer_jj: bool = True,
) -> "VCSProtocol":
    """
    Factory function to get appropriate VCS implementation.

    Args:
        path: Path within a repository or feature directory.
        backend: Explicit backend choice (None = auto-detect).
        prefer_jj: If auto-detecting, prefer jj over git when both available.

    Returns:
        VCSProtocol implementation (GitVCS or JujutsuVCS).

    Raises:
        VCSNotFoundError: Neither jj nor git available.
        VCSBackendMismatchError: Requested backend doesn't match feature's locked VCS.

    Detection order:
        1. If backend specified, use that
        2. If path is in a feature, read meta.json for locked VCS
        3. If jj available and prefer_jj=True, use jj
        4. If git available, use git
        5. Raise VCSNotFoundError
    """
    # 1. If explicit backend specified, use that
    if backend is not None:
        # Check if there's a locked VCS that conflicts
        locked = _get_locked_vcs_from_feature(None)
        if locked is not None and locked != backend:
            raise VCSBackendMismatchError(
                f"Requested backend '{backend.value}' doesn't match feature's "
                f"locked VCS '{locked.value}'. "
                f"Features must use the same VCS throughout their lifecycle."
            )
        return _instantiate_backend(backend)

    # 2. Check for locked VCS in feature meta.json
    locked = _get_locked_vcs_from_feature(path)
    if locked is not None:
        return _instantiate_backend(locked)

    # 3. Auto-detect based on availability
    # DISABLED: jj detection disabled (incompatible with sparse checkouts)
    # if prefer_jj and is_jj_available():
    #     # Lazy import to avoid circular imports
    #     from .jujutsu import JujutsuVCS
    #
    #     return JujutsuVCS()

    if is_git_available():
        # Lazy import to avoid circular imports
        from .git import GitVCS

        return GitVCS()

    # 4. git not available
    raise VCSNotFoundError(
        "git is not available. "
        "Please install git: https://git-scm.com/downloads"
    )


def x_get_vcs__mutmut_5(
    path: Path,
    backend: VCSBackend | None = None,
    prefer_jj: bool = True,
) -> "VCSProtocol":
    """
    Factory function to get appropriate VCS implementation.

    Args:
        path: Path within a repository or feature directory.
        backend: Explicit backend choice (None = auto-detect).
        prefer_jj: If auto-detecting, prefer jj over git when both available.

    Returns:
        VCSProtocol implementation (GitVCS or JujutsuVCS).

    Raises:
        VCSNotFoundError: Neither jj nor git available.
        VCSBackendMismatchError: Requested backend doesn't match feature's locked VCS.

    Detection order:
        1. If backend specified, use that
        2. If path is in a feature, read meta.json for locked VCS
        3. If jj available and prefer_jj=True, use jj
        4. If git available, use git
        5. Raise VCSNotFoundError
    """
    # 1. If explicit backend specified, use that
    if backend is not None:
        # Check if there's a locked VCS that conflicts
        locked = _get_locked_vcs_from_feature(path)
        if locked is not None or locked != backend:
            raise VCSBackendMismatchError(
                f"Requested backend '{backend.value}' doesn't match feature's "
                f"locked VCS '{locked.value}'. "
                f"Features must use the same VCS throughout their lifecycle."
            )
        return _instantiate_backend(backend)

    # 2. Check for locked VCS in feature meta.json
    locked = _get_locked_vcs_from_feature(path)
    if locked is not None:
        return _instantiate_backend(locked)

    # 3. Auto-detect based on availability
    # DISABLED: jj detection disabled (incompatible with sparse checkouts)
    # if prefer_jj and is_jj_available():
    #     # Lazy import to avoid circular imports
    #     from .jujutsu import JujutsuVCS
    #
    #     return JujutsuVCS()

    if is_git_available():
        # Lazy import to avoid circular imports
        from .git import GitVCS

        return GitVCS()

    # 4. git not available
    raise VCSNotFoundError(
        "git is not available. "
        "Please install git: https://git-scm.com/downloads"
    )


def x_get_vcs__mutmut_6(
    path: Path,
    backend: VCSBackend | None = None,
    prefer_jj: bool = True,
) -> "VCSProtocol":
    """
    Factory function to get appropriate VCS implementation.

    Args:
        path: Path within a repository or feature directory.
        backend: Explicit backend choice (None = auto-detect).
        prefer_jj: If auto-detecting, prefer jj over git when both available.

    Returns:
        VCSProtocol implementation (GitVCS or JujutsuVCS).

    Raises:
        VCSNotFoundError: Neither jj nor git available.
        VCSBackendMismatchError: Requested backend doesn't match feature's locked VCS.

    Detection order:
        1. If backend specified, use that
        2. If path is in a feature, read meta.json for locked VCS
        3. If jj available and prefer_jj=True, use jj
        4. If git available, use git
        5. Raise VCSNotFoundError
    """
    # 1. If explicit backend specified, use that
    if backend is not None:
        # Check if there's a locked VCS that conflicts
        locked = _get_locked_vcs_from_feature(path)
        if locked is None and locked != backend:
            raise VCSBackendMismatchError(
                f"Requested backend '{backend.value}' doesn't match feature's "
                f"locked VCS '{locked.value}'. "
                f"Features must use the same VCS throughout their lifecycle."
            )
        return _instantiate_backend(backend)

    # 2. Check for locked VCS in feature meta.json
    locked = _get_locked_vcs_from_feature(path)
    if locked is not None:
        return _instantiate_backend(locked)

    # 3. Auto-detect based on availability
    # DISABLED: jj detection disabled (incompatible with sparse checkouts)
    # if prefer_jj and is_jj_available():
    #     # Lazy import to avoid circular imports
    #     from .jujutsu import JujutsuVCS
    #
    #     return JujutsuVCS()

    if is_git_available():
        # Lazy import to avoid circular imports
        from .git import GitVCS

        return GitVCS()

    # 4. git not available
    raise VCSNotFoundError(
        "git is not available. "
        "Please install git: https://git-scm.com/downloads"
    )


def x_get_vcs__mutmut_7(
    path: Path,
    backend: VCSBackend | None = None,
    prefer_jj: bool = True,
) -> "VCSProtocol":
    """
    Factory function to get appropriate VCS implementation.

    Args:
        path: Path within a repository or feature directory.
        backend: Explicit backend choice (None = auto-detect).
        prefer_jj: If auto-detecting, prefer jj over git when both available.

    Returns:
        VCSProtocol implementation (GitVCS or JujutsuVCS).

    Raises:
        VCSNotFoundError: Neither jj nor git available.
        VCSBackendMismatchError: Requested backend doesn't match feature's locked VCS.

    Detection order:
        1. If backend specified, use that
        2. If path is in a feature, read meta.json for locked VCS
        3. If jj available and prefer_jj=True, use jj
        4. If git available, use git
        5. Raise VCSNotFoundError
    """
    # 1. If explicit backend specified, use that
    if backend is not None:
        # Check if there's a locked VCS that conflicts
        locked = _get_locked_vcs_from_feature(path)
        if locked is not None and locked == backend:
            raise VCSBackendMismatchError(
                f"Requested backend '{backend.value}' doesn't match feature's "
                f"locked VCS '{locked.value}'. "
                f"Features must use the same VCS throughout their lifecycle."
            )
        return _instantiate_backend(backend)

    # 2. Check for locked VCS in feature meta.json
    locked = _get_locked_vcs_from_feature(path)
    if locked is not None:
        return _instantiate_backend(locked)

    # 3. Auto-detect based on availability
    # DISABLED: jj detection disabled (incompatible with sparse checkouts)
    # if prefer_jj and is_jj_available():
    #     # Lazy import to avoid circular imports
    #     from .jujutsu import JujutsuVCS
    #
    #     return JujutsuVCS()

    if is_git_available():
        # Lazy import to avoid circular imports
        from .git import GitVCS

        return GitVCS()

    # 4. git not available
    raise VCSNotFoundError(
        "git is not available. "
        "Please install git: https://git-scm.com/downloads"
    )


def x_get_vcs__mutmut_8(
    path: Path,
    backend: VCSBackend | None = None,
    prefer_jj: bool = True,
) -> "VCSProtocol":
    """
    Factory function to get appropriate VCS implementation.

    Args:
        path: Path within a repository or feature directory.
        backend: Explicit backend choice (None = auto-detect).
        prefer_jj: If auto-detecting, prefer jj over git when both available.

    Returns:
        VCSProtocol implementation (GitVCS or JujutsuVCS).

    Raises:
        VCSNotFoundError: Neither jj nor git available.
        VCSBackendMismatchError: Requested backend doesn't match feature's locked VCS.

    Detection order:
        1. If backend specified, use that
        2. If path is in a feature, read meta.json for locked VCS
        3. If jj available and prefer_jj=True, use jj
        4. If git available, use git
        5. Raise VCSNotFoundError
    """
    # 1. If explicit backend specified, use that
    if backend is not None:
        # Check if there's a locked VCS that conflicts
        locked = _get_locked_vcs_from_feature(path)
        if locked is not None and locked != backend:
            raise VCSBackendMismatchError(
                None
            )
        return _instantiate_backend(backend)

    # 2. Check for locked VCS in feature meta.json
    locked = _get_locked_vcs_from_feature(path)
    if locked is not None:
        return _instantiate_backend(locked)

    # 3. Auto-detect based on availability
    # DISABLED: jj detection disabled (incompatible with sparse checkouts)
    # if prefer_jj and is_jj_available():
    #     # Lazy import to avoid circular imports
    #     from .jujutsu import JujutsuVCS
    #
    #     return JujutsuVCS()

    if is_git_available():
        # Lazy import to avoid circular imports
        from .git import GitVCS

        return GitVCS()

    # 4. git not available
    raise VCSNotFoundError(
        "git is not available. "
        "Please install git: https://git-scm.com/downloads"
    )


def x_get_vcs__mutmut_9(
    path: Path,
    backend: VCSBackend | None = None,
    prefer_jj: bool = True,
) -> "VCSProtocol":
    """
    Factory function to get appropriate VCS implementation.

    Args:
        path: Path within a repository or feature directory.
        backend: Explicit backend choice (None = auto-detect).
        prefer_jj: If auto-detecting, prefer jj over git when both available.

    Returns:
        VCSProtocol implementation (GitVCS or JujutsuVCS).

    Raises:
        VCSNotFoundError: Neither jj nor git available.
        VCSBackendMismatchError: Requested backend doesn't match feature's locked VCS.

    Detection order:
        1. If backend specified, use that
        2. If path is in a feature, read meta.json for locked VCS
        3. If jj available and prefer_jj=True, use jj
        4. If git available, use git
        5. Raise VCSNotFoundError
    """
    # 1. If explicit backend specified, use that
    if backend is not None:
        # Check if there's a locked VCS that conflicts
        locked = _get_locked_vcs_from_feature(path)
        if locked is not None and locked != backend:
            raise VCSBackendMismatchError(
                f"Requested backend '{backend.value}' doesn't match feature's "
                f"locked VCS '{locked.value}'. "
                f"Features must use the same VCS throughout their lifecycle."
            )
        return _instantiate_backend(None)

    # 2. Check for locked VCS in feature meta.json
    locked = _get_locked_vcs_from_feature(path)
    if locked is not None:
        return _instantiate_backend(locked)

    # 3. Auto-detect based on availability
    # DISABLED: jj detection disabled (incompatible with sparse checkouts)
    # if prefer_jj and is_jj_available():
    #     # Lazy import to avoid circular imports
    #     from .jujutsu import JujutsuVCS
    #
    #     return JujutsuVCS()

    if is_git_available():
        # Lazy import to avoid circular imports
        from .git import GitVCS

        return GitVCS()

    # 4. git not available
    raise VCSNotFoundError(
        "git is not available. "
        "Please install git: https://git-scm.com/downloads"
    )


def x_get_vcs__mutmut_10(
    path: Path,
    backend: VCSBackend | None = None,
    prefer_jj: bool = True,
) -> "VCSProtocol":
    """
    Factory function to get appropriate VCS implementation.

    Args:
        path: Path within a repository or feature directory.
        backend: Explicit backend choice (None = auto-detect).
        prefer_jj: If auto-detecting, prefer jj over git when both available.

    Returns:
        VCSProtocol implementation (GitVCS or JujutsuVCS).

    Raises:
        VCSNotFoundError: Neither jj nor git available.
        VCSBackendMismatchError: Requested backend doesn't match feature's locked VCS.

    Detection order:
        1. If backend specified, use that
        2. If path is in a feature, read meta.json for locked VCS
        3. If jj available and prefer_jj=True, use jj
        4. If git available, use git
        5. Raise VCSNotFoundError
    """
    # 1. If explicit backend specified, use that
    if backend is not None:
        # Check if there's a locked VCS that conflicts
        locked = _get_locked_vcs_from_feature(path)
        if locked is not None and locked != backend:
            raise VCSBackendMismatchError(
                f"Requested backend '{backend.value}' doesn't match feature's "
                f"locked VCS '{locked.value}'. "
                f"Features must use the same VCS throughout their lifecycle."
            )
        return _instantiate_backend(backend)

    # 2. Check for locked VCS in feature meta.json
    locked = None
    if locked is not None:
        return _instantiate_backend(locked)

    # 3. Auto-detect based on availability
    # DISABLED: jj detection disabled (incompatible with sparse checkouts)
    # if prefer_jj and is_jj_available():
    #     # Lazy import to avoid circular imports
    #     from .jujutsu import JujutsuVCS
    #
    #     return JujutsuVCS()

    if is_git_available():
        # Lazy import to avoid circular imports
        from .git import GitVCS

        return GitVCS()

    # 4. git not available
    raise VCSNotFoundError(
        "git is not available. "
        "Please install git: https://git-scm.com/downloads"
    )


def x_get_vcs__mutmut_11(
    path: Path,
    backend: VCSBackend | None = None,
    prefer_jj: bool = True,
) -> "VCSProtocol":
    """
    Factory function to get appropriate VCS implementation.

    Args:
        path: Path within a repository or feature directory.
        backend: Explicit backend choice (None = auto-detect).
        prefer_jj: If auto-detecting, prefer jj over git when both available.

    Returns:
        VCSProtocol implementation (GitVCS or JujutsuVCS).

    Raises:
        VCSNotFoundError: Neither jj nor git available.
        VCSBackendMismatchError: Requested backend doesn't match feature's locked VCS.

    Detection order:
        1. If backend specified, use that
        2. If path is in a feature, read meta.json for locked VCS
        3. If jj available and prefer_jj=True, use jj
        4. If git available, use git
        5. Raise VCSNotFoundError
    """
    # 1. If explicit backend specified, use that
    if backend is not None:
        # Check if there's a locked VCS that conflicts
        locked = _get_locked_vcs_from_feature(path)
        if locked is not None and locked != backend:
            raise VCSBackendMismatchError(
                f"Requested backend '{backend.value}' doesn't match feature's "
                f"locked VCS '{locked.value}'. "
                f"Features must use the same VCS throughout their lifecycle."
            )
        return _instantiate_backend(backend)

    # 2. Check for locked VCS in feature meta.json
    locked = _get_locked_vcs_from_feature(None)
    if locked is not None:
        return _instantiate_backend(locked)

    # 3. Auto-detect based on availability
    # DISABLED: jj detection disabled (incompatible with sparse checkouts)
    # if prefer_jj and is_jj_available():
    #     # Lazy import to avoid circular imports
    #     from .jujutsu import JujutsuVCS
    #
    #     return JujutsuVCS()

    if is_git_available():
        # Lazy import to avoid circular imports
        from .git import GitVCS

        return GitVCS()

    # 4. git not available
    raise VCSNotFoundError(
        "git is not available. "
        "Please install git: https://git-scm.com/downloads"
    )


def x_get_vcs__mutmut_12(
    path: Path,
    backend: VCSBackend | None = None,
    prefer_jj: bool = True,
) -> "VCSProtocol":
    """
    Factory function to get appropriate VCS implementation.

    Args:
        path: Path within a repository or feature directory.
        backend: Explicit backend choice (None = auto-detect).
        prefer_jj: If auto-detecting, prefer jj over git when both available.

    Returns:
        VCSProtocol implementation (GitVCS or JujutsuVCS).

    Raises:
        VCSNotFoundError: Neither jj nor git available.
        VCSBackendMismatchError: Requested backend doesn't match feature's locked VCS.

    Detection order:
        1. If backend specified, use that
        2. If path is in a feature, read meta.json for locked VCS
        3. If jj available and prefer_jj=True, use jj
        4. If git available, use git
        5. Raise VCSNotFoundError
    """
    # 1. If explicit backend specified, use that
    if backend is not None:
        # Check if there's a locked VCS that conflicts
        locked = _get_locked_vcs_from_feature(path)
        if locked is not None and locked != backend:
            raise VCSBackendMismatchError(
                f"Requested backend '{backend.value}' doesn't match feature's "
                f"locked VCS '{locked.value}'. "
                f"Features must use the same VCS throughout their lifecycle."
            )
        return _instantiate_backend(backend)

    # 2. Check for locked VCS in feature meta.json
    locked = _get_locked_vcs_from_feature(path)
    if locked is None:
        return _instantiate_backend(locked)

    # 3. Auto-detect based on availability
    # DISABLED: jj detection disabled (incompatible with sparse checkouts)
    # if prefer_jj and is_jj_available():
    #     # Lazy import to avoid circular imports
    #     from .jujutsu import JujutsuVCS
    #
    #     return JujutsuVCS()

    if is_git_available():
        # Lazy import to avoid circular imports
        from .git import GitVCS

        return GitVCS()

    # 4. git not available
    raise VCSNotFoundError(
        "git is not available. "
        "Please install git: https://git-scm.com/downloads"
    )


def x_get_vcs__mutmut_13(
    path: Path,
    backend: VCSBackend | None = None,
    prefer_jj: bool = True,
) -> "VCSProtocol":
    """
    Factory function to get appropriate VCS implementation.

    Args:
        path: Path within a repository or feature directory.
        backend: Explicit backend choice (None = auto-detect).
        prefer_jj: If auto-detecting, prefer jj over git when both available.

    Returns:
        VCSProtocol implementation (GitVCS or JujutsuVCS).

    Raises:
        VCSNotFoundError: Neither jj nor git available.
        VCSBackendMismatchError: Requested backend doesn't match feature's locked VCS.

    Detection order:
        1. If backend specified, use that
        2. If path is in a feature, read meta.json for locked VCS
        3. If jj available and prefer_jj=True, use jj
        4. If git available, use git
        5. Raise VCSNotFoundError
    """
    # 1. If explicit backend specified, use that
    if backend is not None:
        # Check if there's a locked VCS that conflicts
        locked = _get_locked_vcs_from_feature(path)
        if locked is not None and locked != backend:
            raise VCSBackendMismatchError(
                f"Requested backend '{backend.value}' doesn't match feature's "
                f"locked VCS '{locked.value}'. "
                f"Features must use the same VCS throughout their lifecycle."
            )
        return _instantiate_backend(backend)

    # 2. Check for locked VCS in feature meta.json
    locked = _get_locked_vcs_from_feature(path)
    if locked is not None:
        return _instantiate_backend(None)

    # 3. Auto-detect based on availability
    # DISABLED: jj detection disabled (incompatible with sparse checkouts)
    # if prefer_jj and is_jj_available():
    #     # Lazy import to avoid circular imports
    #     from .jujutsu import JujutsuVCS
    #
    #     return JujutsuVCS()

    if is_git_available():
        # Lazy import to avoid circular imports
        from .git import GitVCS

        return GitVCS()

    # 4. git not available
    raise VCSNotFoundError(
        "git is not available. "
        "Please install git: https://git-scm.com/downloads"
    )


def x_get_vcs__mutmut_14(
    path: Path,
    backend: VCSBackend | None = None,
    prefer_jj: bool = True,
) -> "VCSProtocol":
    """
    Factory function to get appropriate VCS implementation.

    Args:
        path: Path within a repository or feature directory.
        backend: Explicit backend choice (None = auto-detect).
        prefer_jj: If auto-detecting, prefer jj over git when both available.

    Returns:
        VCSProtocol implementation (GitVCS or JujutsuVCS).

    Raises:
        VCSNotFoundError: Neither jj nor git available.
        VCSBackendMismatchError: Requested backend doesn't match feature's locked VCS.

    Detection order:
        1. If backend specified, use that
        2. If path is in a feature, read meta.json for locked VCS
        3. If jj available and prefer_jj=True, use jj
        4. If git available, use git
        5. Raise VCSNotFoundError
    """
    # 1. If explicit backend specified, use that
    if backend is not None:
        # Check if there's a locked VCS that conflicts
        locked = _get_locked_vcs_from_feature(path)
        if locked is not None and locked != backend:
            raise VCSBackendMismatchError(
                f"Requested backend '{backend.value}' doesn't match feature's "
                f"locked VCS '{locked.value}'. "
                f"Features must use the same VCS throughout their lifecycle."
            )
        return _instantiate_backend(backend)

    # 2. Check for locked VCS in feature meta.json
    locked = _get_locked_vcs_from_feature(path)
    if locked is not None:
        return _instantiate_backend(locked)

    # 3. Auto-detect based on availability
    # DISABLED: jj detection disabled (incompatible with sparse checkouts)
    # if prefer_jj and is_jj_available():
    #     # Lazy import to avoid circular imports
    #     from .jujutsu import JujutsuVCS
    #
    #     return JujutsuVCS()

    if is_git_available():
        # Lazy import to avoid circular imports
        from .git import GitVCS

        return GitVCS()

    # 4. git not available
    raise VCSNotFoundError(
        None
    )


def x_get_vcs__mutmut_15(
    path: Path,
    backend: VCSBackend | None = None,
    prefer_jj: bool = True,
) -> "VCSProtocol":
    """
    Factory function to get appropriate VCS implementation.

    Args:
        path: Path within a repository or feature directory.
        backend: Explicit backend choice (None = auto-detect).
        prefer_jj: If auto-detecting, prefer jj over git when both available.

    Returns:
        VCSProtocol implementation (GitVCS or JujutsuVCS).

    Raises:
        VCSNotFoundError: Neither jj nor git available.
        VCSBackendMismatchError: Requested backend doesn't match feature's locked VCS.

    Detection order:
        1. If backend specified, use that
        2. If path is in a feature, read meta.json for locked VCS
        3. If jj available and prefer_jj=True, use jj
        4. If git available, use git
        5. Raise VCSNotFoundError
    """
    # 1. If explicit backend specified, use that
    if backend is not None:
        # Check if there's a locked VCS that conflicts
        locked = _get_locked_vcs_from_feature(path)
        if locked is not None and locked != backend:
            raise VCSBackendMismatchError(
                f"Requested backend '{backend.value}' doesn't match feature's "
                f"locked VCS '{locked.value}'. "
                f"Features must use the same VCS throughout their lifecycle."
            )
        return _instantiate_backend(backend)

    # 2. Check for locked VCS in feature meta.json
    locked = _get_locked_vcs_from_feature(path)
    if locked is not None:
        return _instantiate_backend(locked)

    # 3. Auto-detect based on availability
    # DISABLED: jj detection disabled (incompatible with sparse checkouts)
    # if prefer_jj and is_jj_available():
    #     # Lazy import to avoid circular imports
    #     from .jujutsu import JujutsuVCS
    #
    #     return JujutsuVCS()

    if is_git_available():
        # Lazy import to avoid circular imports
        from .git import GitVCS

        return GitVCS()

    # 4. git not available
    raise VCSNotFoundError(
        "XXgit is not available. XX"
        "Please install git: https://git-scm.com/downloads"
    )


def x_get_vcs__mutmut_16(
    path: Path,
    backend: VCSBackend | None = None,
    prefer_jj: bool = True,
) -> "VCSProtocol":
    """
    Factory function to get appropriate VCS implementation.

    Args:
        path: Path within a repository or feature directory.
        backend: Explicit backend choice (None = auto-detect).
        prefer_jj: If auto-detecting, prefer jj over git when both available.

    Returns:
        VCSProtocol implementation (GitVCS or JujutsuVCS).

    Raises:
        VCSNotFoundError: Neither jj nor git available.
        VCSBackendMismatchError: Requested backend doesn't match feature's locked VCS.

    Detection order:
        1. If backend specified, use that
        2. If path is in a feature, read meta.json for locked VCS
        3. If jj available and prefer_jj=True, use jj
        4. If git available, use git
        5. Raise VCSNotFoundError
    """
    # 1. If explicit backend specified, use that
    if backend is not None:
        # Check if there's a locked VCS that conflicts
        locked = _get_locked_vcs_from_feature(path)
        if locked is not None and locked != backend:
            raise VCSBackendMismatchError(
                f"Requested backend '{backend.value}' doesn't match feature's "
                f"locked VCS '{locked.value}'. "
                f"Features must use the same VCS throughout their lifecycle."
            )
        return _instantiate_backend(backend)

    # 2. Check for locked VCS in feature meta.json
    locked = _get_locked_vcs_from_feature(path)
    if locked is not None:
        return _instantiate_backend(locked)

    # 3. Auto-detect based on availability
    # DISABLED: jj detection disabled (incompatible with sparse checkouts)
    # if prefer_jj and is_jj_available():
    #     # Lazy import to avoid circular imports
    #     from .jujutsu import JujutsuVCS
    #
    #     return JujutsuVCS()

    if is_git_available():
        # Lazy import to avoid circular imports
        from .git import GitVCS

        return GitVCS()

    # 4. git not available
    raise VCSNotFoundError(
        "GIT IS NOT AVAILABLE. "
        "Please install git: https://git-scm.com/downloads"
    )


def x_get_vcs__mutmut_17(
    path: Path,
    backend: VCSBackend | None = None,
    prefer_jj: bool = True,
) -> "VCSProtocol":
    """
    Factory function to get appropriate VCS implementation.

    Args:
        path: Path within a repository or feature directory.
        backend: Explicit backend choice (None = auto-detect).
        prefer_jj: If auto-detecting, prefer jj over git when both available.

    Returns:
        VCSProtocol implementation (GitVCS or JujutsuVCS).

    Raises:
        VCSNotFoundError: Neither jj nor git available.
        VCSBackendMismatchError: Requested backend doesn't match feature's locked VCS.

    Detection order:
        1. If backend specified, use that
        2. If path is in a feature, read meta.json for locked VCS
        3. If jj available and prefer_jj=True, use jj
        4. If git available, use git
        5. Raise VCSNotFoundError
    """
    # 1. If explicit backend specified, use that
    if backend is not None:
        # Check if there's a locked VCS that conflicts
        locked = _get_locked_vcs_from_feature(path)
        if locked is not None and locked != backend:
            raise VCSBackendMismatchError(
                f"Requested backend '{backend.value}' doesn't match feature's "
                f"locked VCS '{locked.value}'. "
                f"Features must use the same VCS throughout their lifecycle."
            )
        return _instantiate_backend(backend)

    # 2. Check for locked VCS in feature meta.json
    locked = _get_locked_vcs_from_feature(path)
    if locked is not None:
        return _instantiate_backend(locked)

    # 3. Auto-detect based on availability
    # DISABLED: jj detection disabled (incompatible with sparse checkouts)
    # if prefer_jj and is_jj_available():
    #     # Lazy import to avoid circular imports
    #     from .jujutsu import JujutsuVCS
    #
    #     return JujutsuVCS()

    if is_git_available():
        # Lazy import to avoid circular imports
        from .git import GitVCS

        return GitVCS()

    # 4. git not available
    raise VCSNotFoundError(
        "git is not available. "
        "XXPlease install git: https://git-scm.com/downloadsXX"
    )


def x_get_vcs__mutmut_18(
    path: Path,
    backend: VCSBackend | None = None,
    prefer_jj: bool = True,
) -> "VCSProtocol":
    """
    Factory function to get appropriate VCS implementation.

    Args:
        path: Path within a repository or feature directory.
        backend: Explicit backend choice (None = auto-detect).
        prefer_jj: If auto-detecting, prefer jj over git when both available.

    Returns:
        VCSProtocol implementation (GitVCS or JujutsuVCS).

    Raises:
        VCSNotFoundError: Neither jj nor git available.
        VCSBackendMismatchError: Requested backend doesn't match feature's locked VCS.

    Detection order:
        1. If backend specified, use that
        2. If path is in a feature, read meta.json for locked VCS
        3. If jj available and prefer_jj=True, use jj
        4. If git available, use git
        5. Raise VCSNotFoundError
    """
    # 1. If explicit backend specified, use that
    if backend is not None:
        # Check if there's a locked VCS that conflicts
        locked = _get_locked_vcs_from_feature(path)
        if locked is not None and locked != backend:
            raise VCSBackendMismatchError(
                f"Requested backend '{backend.value}' doesn't match feature's "
                f"locked VCS '{locked.value}'. "
                f"Features must use the same VCS throughout their lifecycle."
            )
        return _instantiate_backend(backend)

    # 2. Check for locked VCS in feature meta.json
    locked = _get_locked_vcs_from_feature(path)
    if locked is not None:
        return _instantiate_backend(locked)

    # 3. Auto-detect based on availability
    # DISABLED: jj detection disabled (incompatible with sparse checkouts)
    # if prefer_jj and is_jj_available():
    #     # Lazy import to avoid circular imports
    #     from .jujutsu import JujutsuVCS
    #
    #     return JujutsuVCS()

    if is_git_available():
        # Lazy import to avoid circular imports
        from .git import GitVCS

        return GitVCS()

    # 4. git not available
    raise VCSNotFoundError(
        "git is not available. "
        "please install git: https://git-scm.com/downloads"
    )


def x_get_vcs__mutmut_19(
    path: Path,
    backend: VCSBackend | None = None,
    prefer_jj: bool = True,
) -> "VCSProtocol":
    """
    Factory function to get appropriate VCS implementation.

    Args:
        path: Path within a repository or feature directory.
        backend: Explicit backend choice (None = auto-detect).
        prefer_jj: If auto-detecting, prefer jj over git when both available.

    Returns:
        VCSProtocol implementation (GitVCS or JujutsuVCS).

    Raises:
        VCSNotFoundError: Neither jj nor git available.
        VCSBackendMismatchError: Requested backend doesn't match feature's locked VCS.

    Detection order:
        1. If backend specified, use that
        2. If path is in a feature, read meta.json for locked VCS
        3. If jj available and prefer_jj=True, use jj
        4. If git available, use git
        5. Raise VCSNotFoundError
    """
    # 1. If explicit backend specified, use that
    if backend is not None:
        # Check if there's a locked VCS that conflicts
        locked = _get_locked_vcs_from_feature(path)
        if locked is not None and locked != backend:
            raise VCSBackendMismatchError(
                f"Requested backend '{backend.value}' doesn't match feature's "
                f"locked VCS '{locked.value}'. "
                f"Features must use the same VCS throughout their lifecycle."
            )
        return _instantiate_backend(backend)

    # 2. Check for locked VCS in feature meta.json
    locked = _get_locked_vcs_from_feature(path)
    if locked is not None:
        return _instantiate_backend(locked)

    # 3. Auto-detect based on availability
    # DISABLED: jj detection disabled (incompatible with sparse checkouts)
    # if prefer_jj and is_jj_available():
    #     # Lazy import to avoid circular imports
    #     from .jujutsu import JujutsuVCS
    #
    #     return JujutsuVCS()

    if is_git_available():
        # Lazy import to avoid circular imports
        from .git import GitVCS

        return GitVCS()

    # 4. git not available
    raise VCSNotFoundError(
        "git is not available. "
        "PLEASE INSTALL GIT: HTTPS://GIT-SCM.COM/DOWNLOADS"
    )

x_get_vcs__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_get_vcs__mutmut_1': x_get_vcs__mutmut_1, 
    'x_get_vcs__mutmut_2': x_get_vcs__mutmut_2, 
    'x_get_vcs__mutmut_3': x_get_vcs__mutmut_3, 
    'x_get_vcs__mutmut_4': x_get_vcs__mutmut_4, 
    'x_get_vcs__mutmut_5': x_get_vcs__mutmut_5, 
    'x_get_vcs__mutmut_6': x_get_vcs__mutmut_6, 
    'x_get_vcs__mutmut_7': x_get_vcs__mutmut_7, 
    'x_get_vcs__mutmut_8': x_get_vcs__mutmut_8, 
    'x_get_vcs__mutmut_9': x_get_vcs__mutmut_9, 
    'x_get_vcs__mutmut_10': x_get_vcs__mutmut_10, 
    'x_get_vcs__mutmut_11': x_get_vcs__mutmut_11, 
    'x_get_vcs__mutmut_12': x_get_vcs__mutmut_12, 
    'x_get_vcs__mutmut_13': x_get_vcs__mutmut_13, 
    'x_get_vcs__mutmut_14': x_get_vcs__mutmut_14, 
    'x_get_vcs__mutmut_15': x_get_vcs__mutmut_15, 
    'x_get_vcs__mutmut_16': x_get_vcs__mutmut_16, 
    'x_get_vcs__mutmut_17': x_get_vcs__mutmut_17, 
    'x_get_vcs__mutmut_18': x_get_vcs__mutmut_18, 
    'x_get_vcs__mutmut_19': x_get_vcs__mutmut_19
}
x_get_vcs__mutmut_orig.__name__ = 'x_get_vcs'


# =============================================================================
# Cache Management (for testing)
# =============================================================================


def _clear_detection_cache() -> None:
    """
    Clear the detection cache. For testing purposes only.

    This clears the cached results of is_jj_available, is_git_available,
    get_jj_version, and get_git_version.
    """
    is_jj_available.cache_clear()
    is_git_available.cache_clear()
    get_jj_version.cache_clear()
    get_git_version.cache_clear()
