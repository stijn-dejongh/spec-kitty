"""Enhanced path resolution for spec-kitty CLI with worktree detection."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional, Tuple

from .constants import KITTIFY_DIR, WORKTREES_DIR
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


def _is_worktree_gitdir(gitdir: Path) -> bool:
    args = [gitdir]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x__is_worktree_gitdir__mutmut_orig, x__is_worktree_gitdir__mutmut_mutants, args, kwargs, None)


def x__is_worktree_gitdir__mutmut_orig(gitdir: Path) -> bool:
    """Check if a gitdir path has the .git/worktrees/<name> topology.

    True git worktrees point to ``<main>/.git/worktrees/<wt-name>``.
    Bare-repo worktrees point to ``<repo>.git/worktrees/<wt-name>``.
    Submodules point to ``../.git/modules/<mod>`` and separate-git-dir
    clones point to an arbitrary directory.  Only the first two cases
    are worktrees.
    """
    # gitdir = …/.git/worktrees/<name>        (non-bare)
    # gitdir = …/<repo>.git/worktrees/<name>  (bare)
    #   gitdir.parent.name  == "worktrees"
    #   gitdir.parent.parent.name endswith ".git"
    return (
        gitdir.parent.name == "worktrees"
        and gitdir.parent.parent.name.endswith(".git")
    )


def x__is_worktree_gitdir__mutmut_1(gitdir: Path) -> bool:
    """Check if a gitdir path has the .git/worktrees/<name> topology.

    True git worktrees point to ``<main>/.git/worktrees/<wt-name>``.
    Bare-repo worktrees point to ``<repo>.git/worktrees/<wt-name>``.
    Submodules point to ``../.git/modules/<mod>`` and separate-git-dir
    clones point to an arbitrary directory.  Only the first two cases
    are worktrees.
    """
    # gitdir = …/.git/worktrees/<name>        (non-bare)
    # gitdir = …/<repo>.git/worktrees/<name>  (bare)
    #   gitdir.parent.name  == "worktrees"
    #   gitdir.parent.parent.name endswith ".git"
    return (
        gitdir.parent.name == "worktrees" or gitdir.parent.parent.name.endswith(".git")
    )


def x__is_worktree_gitdir__mutmut_2(gitdir: Path) -> bool:
    """Check if a gitdir path has the .git/worktrees/<name> topology.

    True git worktrees point to ``<main>/.git/worktrees/<wt-name>``.
    Bare-repo worktrees point to ``<repo>.git/worktrees/<wt-name>``.
    Submodules point to ``../.git/modules/<mod>`` and separate-git-dir
    clones point to an arbitrary directory.  Only the first two cases
    are worktrees.
    """
    # gitdir = …/.git/worktrees/<name>        (non-bare)
    # gitdir = …/<repo>.git/worktrees/<name>  (bare)
    #   gitdir.parent.name  == "worktrees"
    #   gitdir.parent.parent.name endswith ".git"
    return (
        gitdir.parent.name != "worktrees"
        and gitdir.parent.parent.name.endswith(".git")
    )


def x__is_worktree_gitdir__mutmut_3(gitdir: Path) -> bool:
    """Check if a gitdir path has the .git/worktrees/<name> topology.

    True git worktrees point to ``<main>/.git/worktrees/<wt-name>``.
    Bare-repo worktrees point to ``<repo>.git/worktrees/<wt-name>``.
    Submodules point to ``../.git/modules/<mod>`` and separate-git-dir
    clones point to an arbitrary directory.  Only the first two cases
    are worktrees.
    """
    # gitdir = …/.git/worktrees/<name>        (non-bare)
    # gitdir = …/<repo>.git/worktrees/<name>  (bare)
    #   gitdir.parent.name  == "worktrees"
    #   gitdir.parent.parent.name endswith ".git"
    return (
        gitdir.parent.name == "XXworktreesXX"
        and gitdir.parent.parent.name.endswith(".git")
    )


def x__is_worktree_gitdir__mutmut_4(gitdir: Path) -> bool:
    """Check if a gitdir path has the .git/worktrees/<name> topology.

    True git worktrees point to ``<main>/.git/worktrees/<wt-name>``.
    Bare-repo worktrees point to ``<repo>.git/worktrees/<wt-name>``.
    Submodules point to ``../.git/modules/<mod>`` and separate-git-dir
    clones point to an arbitrary directory.  Only the first two cases
    are worktrees.
    """
    # gitdir = …/.git/worktrees/<name>        (non-bare)
    # gitdir = …/<repo>.git/worktrees/<name>  (bare)
    #   gitdir.parent.name  == "worktrees"
    #   gitdir.parent.parent.name endswith ".git"
    return (
        gitdir.parent.name == "WORKTREES"
        and gitdir.parent.parent.name.endswith(".git")
    )


def x__is_worktree_gitdir__mutmut_5(gitdir: Path) -> bool:
    """Check if a gitdir path has the .git/worktrees/<name> topology.

    True git worktrees point to ``<main>/.git/worktrees/<wt-name>``.
    Bare-repo worktrees point to ``<repo>.git/worktrees/<wt-name>``.
    Submodules point to ``../.git/modules/<mod>`` and separate-git-dir
    clones point to an arbitrary directory.  Only the first two cases
    are worktrees.
    """
    # gitdir = …/.git/worktrees/<name>        (non-bare)
    # gitdir = …/<repo>.git/worktrees/<name>  (bare)
    #   gitdir.parent.name  == "worktrees"
    #   gitdir.parent.parent.name endswith ".git"
    return (
        gitdir.parent.name == "worktrees"
        and gitdir.parent.parent.name.endswith(None)
    )


def x__is_worktree_gitdir__mutmut_6(gitdir: Path) -> bool:
    """Check if a gitdir path has the .git/worktrees/<name> topology.

    True git worktrees point to ``<main>/.git/worktrees/<wt-name>``.
    Bare-repo worktrees point to ``<repo>.git/worktrees/<wt-name>``.
    Submodules point to ``../.git/modules/<mod>`` and separate-git-dir
    clones point to an arbitrary directory.  Only the first two cases
    are worktrees.
    """
    # gitdir = …/.git/worktrees/<name>        (non-bare)
    # gitdir = …/<repo>.git/worktrees/<name>  (bare)
    #   gitdir.parent.name  == "worktrees"
    #   gitdir.parent.parent.name endswith ".git"
    return (
        gitdir.parent.name == "worktrees"
        and gitdir.parent.parent.name.endswith("XX.gitXX")
    )


def x__is_worktree_gitdir__mutmut_7(gitdir: Path) -> bool:
    """Check if a gitdir path has the .git/worktrees/<name> topology.

    True git worktrees point to ``<main>/.git/worktrees/<wt-name>``.
    Bare-repo worktrees point to ``<repo>.git/worktrees/<wt-name>``.
    Submodules point to ``../.git/modules/<mod>`` and separate-git-dir
    clones point to an arbitrary directory.  Only the first two cases
    are worktrees.
    """
    # gitdir = …/.git/worktrees/<name>        (non-bare)
    # gitdir = …/<repo>.git/worktrees/<name>  (bare)
    #   gitdir.parent.name  == "worktrees"
    #   gitdir.parent.parent.name endswith ".git"
    return (
        gitdir.parent.name == "worktrees"
        and gitdir.parent.parent.name.endswith(".GIT")
    )

x__is_worktree_gitdir__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x__is_worktree_gitdir__mutmut_1': x__is_worktree_gitdir__mutmut_1, 
    'x__is_worktree_gitdir__mutmut_2': x__is_worktree_gitdir__mutmut_2, 
    'x__is_worktree_gitdir__mutmut_3': x__is_worktree_gitdir__mutmut_3, 
    'x__is_worktree_gitdir__mutmut_4': x__is_worktree_gitdir__mutmut_4, 
    'x__is_worktree_gitdir__mutmut_5': x__is_worktree_gitdir__mutmut_5, 
    'x__is_worktree_gitdir__mutmut_6': x__is_worktree_gitdir__mutmut_6, 
    'x__is_worktree_gitdir__mutmut_7': x__is_worktree_gitdir__mutmut_7
}
x__is_worktree_gitdir__mutmut_orig.__name__ = 'x__is_worktree_gitdir'


def locate_project_root(start: Path | None = None) -> Optional[Path]:
    args = [start]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_locate_project_root__mutmut_orig, x_locate_project_root__mutmut_mutants, args, kwargs, None)


def x_locate_project_root__mutmut_orig(start: Path | None = None) -> Optional[Path]:
    """
    Locate the MAIN spec-kitty project root directory, even from within worktrees.

    This function correctly handles git worktrees by detecting when .git is a
    file (worktree pointer) vs a directory (main repo), and following the
    pointer back to the main repository.

    Resolution order:
    1. SPECIFY_REPO_ROOT environment variable (highest priority)
    2. Walk up directory tree, detecting worktree .git files and following to main repo
    3. Fall back to .kittify/ marker search

    Args:
        start: Starting directory for search (defaults to current working directory)

    Returns:
        Path to MAIN project root (not worktree), or None if not found

    Examples:
        >>> # From main repo
        >>> root = locate_project_root()
        >>> assert (root / ".kittify").exists()

        >>> # From worktree - returns MAIN repo, not worktree
        >>> root = locate_project_root(Path(".worktrees/my-feature"))
        >>> assert ".worktrees" not in str(root)
    """
    # Tier 1: Check environment variable (allows override for CI/CD)
    if env_root := os.getenv("SPECIFY_REPO_ROOT"):
        env_path = Path(env_root).resolve()
        if env_path.exists() and (env_path / KITTIFY_DIR).is_dir():
            return env_path
        # Invalid env var - fall through to other methods

    # Tier 2: Walk up directory tree, handling worktree .git files
    current = (start or Path.cwd()).resolve()

    for candidate in [current, *current.parents]:
        git_path = candidate / ".git"

        if git_path.is_file():
            # .git files with gitdir: pointers appear in worktrees,
            # submodules, and separate-git-dir clones.  Only follow the
            # pointer when it has the .git/worktrees/<name> topology.
            try:
                content = git_path.read_text().strip()
                if content.startswith("gitdir:"):
                    gitdir = Path(content.split(":", 1)[1].strip())
                    if _is_worktree_gitdir(gitdir):
                        # Navigate: .git/worktrees/name -> .git -> main repo root
                        main_git_dir = gitdir.parent.parent
                        main_repo = main_git_dir.parent
                        if main_repo.exists() and (main_repo / KITTIFY_DIR).is_dir():
                            return main_repo
            except (OSError, ValueError):
                # If we can't read or parse the .git file, continue searching
                pass

        elif git_path.is_dir():
            # This is the main repo (or a regular git repo)
            if (candidate / KITTIFY_DIR).is_dir():
                return candidate

        # Also check for .kittify marker (fallback for non-git scenarios)
        kittify_path = candidate / KITTIFY_DIR
        if kittify_path.is_symlink() and not kittify_path.exists():
            # Broken symlink - skip this candidate
            continue
        if kittify_path.is_dir():
            return candidate

    return None


def x_locate_project_root__mutmut_1(start: Path | None = None) -> Optional[Path]:
    """
    Locate the MAIN spec-kitty project root directory, even from within worktrees.

    This function correctly handles git worktrees by detecting when .git is a
    file (worktree pointer) vs a directory (main repo), and following the
    pointer back to the main repository.

    Resolution order:
    1. SPECIFY_REPO_ROOT environment variable (highest priority)
    2. Walk up directory tree, detecting worktree .git files and following to main repo
    3. Fall back to .kittify/ marker search

    Args:
        start: Starting directory for search (defaults to current working directory)

    Returns:
        Path to MAIN project root (not worktree), or None if not found

    Examples:
        >>> # From main repo
        >>> root = locate_project_root()
        >>> assert (root / ".kittify").exists()

        >>> # From worktree - returns MAIN repo, not worktree
        >>> root = locate_project_root(Path(".worktrees/my-feature"))
        >>> assert ".worktrees" not in str(root)
    """
    # Tier 1: Check environment variable (allows override for CI/CD)
    if env_root := os.getenv(None):
        env_path = Path(env_root).resolve()
        if env_path.exists() and (env_path / KITTIFY_DIR).is_dir():
            return env_path
        # Invalid env var - fall through to other methods

    # Tier 2: Walk up directory tree, handling worktree .git files
    current = (start or Path.cwd()).resolve()

    for candidate in [current, *current.parents]:
        git_path = candidate / ".git"

        if git_path.is_file():
            # .git files with gitdir: pointers appear in worktrees,
            # submodules, and separate-git-dir clones.  Only follow the
            # pointer when it has the .git/worktrees/<name> topology.
            try:
                content = git_path.read_text().strip()
                if content.startswith("gitdir:"):
                    gitdir = Path(content.split(":", 1)[1].strip())
                    if _is_worktree_gitdir(gitdir):
                        # Navigate: .git/worktrees/name -> .git -> main repo root
                        main_git_dir = gitdir.parent.parent
                        main_repo = main_git_dir.parent
                        if main_repo.exists() and (main_repo / KITTIFY_DIR).is_dir():
                            return main_repo
            except (OSError, ValueError):
                # If we can't read or parse the .git file, continue searching
                pass

        elif git_path.is_dir():
            # This is the main repo (or a regular git repo)
            if (candidate / KITTIFY_DIR).is_dir():
                return candidate

        # Also check for .kittify marker (fallback for non-git scenarios)
        kittify_path = candidate / KITTIFY_DIR
        if kittify_path.is_symlink() and not kittify_path.exists():
            # Broken symlink - skip this candidate
            continue
        if kittify_path.is_dir():
            return candidate

    return None


def x_locate_project_root__mutmut_2(start: Path | None = None) -> Optional[Path]:
    """
    Locate the MAIN spec-kitty project root directory, even from within worktrees.

    This function correctly handles git worktrees by detecting when .git is a
    file (worktree pointer) vs a directory (main repo), and following the
    pointer back to the main repository.

    Resolution order:
    1. SPECIFY_REPO_ROOT environment variable (highest priority)
    2. Walk up directory tree, detecting worktree .git files and following to main repo
    3. Fall back to .kittify/ marker search

    Args:
        start: Starting directory for search (defaults to current working directory)

    Returns:
        Path to MAIN project root (not worktree), or None if not found

    Examples:
        >>> # From main repo
        >>> root = locate_project_root()
        >>> assert (root / ".kittify").exists()

        >>> # From worktree - returns MAIN repo, not worktree
        >>> root = locate_project_root(Path(".worktrees/my-feature"))
        >>> assert ".worktrees" not in str(root)
    """
    # Tier 1: Check environment variable (allows override for CI/CD)
    if env_root := os.getenv("XXSPECIFY_REPO_ROOTXX"):
        env_path = Path(env_root).resolve()
        if env_path.exists() and (env_path / KITTIFY_DIR).is_dir():
            return env_path
        # Invalid env var - fall through to other methods

    # Tier 2: Walk up directory tree, handling worktree .git files
    current = (start or Path.cwd()).resolve()

    for candidate in [current, *current.parents]:
        git_path = candidate / ".git"

        if git_path.is_file():
            # .git files with gitdir: pointers appear in worktrees,
            # submodules, and separate-git-dir clones.  Only follow the
            # pointer when it has the .git/worktrees/<name> topology.
            try:
                content = git_path.read_text().strip()
                if content.startswith("gitdir:"):
                    gitdir = Path(content.split(":", 1)[1].strip())
                    if _is_worktree_gitdir(gitdir):
                        # Navigate: .git/worktrees/name -> .git -> main repo root
                        main_git_dir = gitdir.parent.parent
                        main_repo = main_git_dir.parent
                        if main_repo.exists() and (main_repo / KITTIFY_DIR).is_dir():
                            return main_repo
            except (OSError, ValueError):
                # If we can't read or parse the .git file, continue searching
                pass

        elif git_path.is_dir():
            # This is the main repo (or a regular git repo)
            if (candidate / KITTIFY_DIR).is_dir():
                return candidate

        # Also check for .kittify marker (fallback for non-git scenarios)
        kittify_path = candidate / KITTIFY_DIR
        if kittify_path.is_symlink() and not kittify_path.exists():
            # Broken symlink - skip this candidate
            continue
        if kittify_path.is_dir():
            return candidate

    return None


def x_locate_project_root__mutmut_3(start: Path | None = None) -> Optional[Path]:
    """
    Locate the MAIN spec-kitty project root directory, even from within worktrees.

    This function correctly handles git worktrees by detecting when .git is a
    file (worktree pointer) vs a directory (main repo), and following the
    pointer back to the main repository.

    Resolution order:
    1. SPECIFY_REPO_ROOT environment variable (highest priority)
    2. Walk up directory tree, detecting worktree .git files and following to main repo
    3. Fall back to .kittify/ marker search

    Args:
        start: Starting directory for search (defaults to current working directory)

    Returns:
        Path to MAIN project root (not worktree), or None if not found

    Examples:
        >>> # From main repo
        >>> root = locate_project_root()
        >>> assert (root / ".kittify").exists()

        >>> # From worktree - returns MAIN repo, not worktree
        >>> root = locate_project_root(Path(".worktrees/my-feature"))
        >>> assert ".worktrees" not in str(root)
    """
    # Tier 1: Check environment variable (allows override for CI/CD)
    if env_root := os.getenv("specify_repo_root"):
        env_path = Path(env_root).resolve()
        if env_path.exists() and (env_path / KITTIFY_DIR).is_dir():
            return env_path
        # Invalid env var - fall through to other methods

    # Tier 2: Walk up directory tree, handling worktree .git files
    current = (start or Path.cwd()).resolve()

    for candidate in [current, *current.parents]:
        git_path = candidate / ".git"

        if git_path.is_file():
            # .git files with gitdir: pointers appear in worktrees,
            # submodules, and separate-git-dir clones.  Only follow the
            # pointer when it has the .git/worktrees/<name> topology.
            try:
                content = git_path.read_text().strip()
                if content.startswith("gitdir:"):
                    gitdir = Path(content.split(":", 1)[1].strip())
                    if _is_worktree_gitdir(gitdir):
                        # Navigate: .git/worktrees/name -> .git -> main repo root
                        main_git_dir = gitdir.parent.parent
                        main_repo = main_git_dir.parent
                        if main_repo.exists() and (main_repo / KITTIFY_DIR).is_dir():
                            return main_repo
            except (OSError, ValueError):
                # If we can't read or parse the .git file, continue searching
                pass

        elif git_path.is_dir():
            # This is the main repo (or a regular git repo)
            if (candidate / KITTIFY_DIR).is_dir():
                return candidate

        # Also check for .kittify marker (fallback for non-git scenarios)
        kittify_path = candidate / KITTIFY_DIR
        if kittify_path.is_symlink() and not kittify_path.exists():
            # Broken symlink - skip this candidate
            continue
        if kittify_path.is_dir():
            return candidate

    return None


def x_locate_project_root__mutmut_4(start: Path | None = None) -> Optional[Path]:
    """
    Locate the MAIN spec-kitty project root directory, even from within worktrees.

    This function correctly handles git worktrees by detecting when .git is a
    file (worktree pointer) vs a directory (main repo), and following the
    pointer back to the main repository.

    Resolution order:
    1. SPECIFY_REPO_ROOT environment variable (highest priority)
    2. Walk up directory tree, detecting worktree .git files and following to main repo
    3. Fall back to .kittify/ marker search

    Args:
        start: Starting directory for search (defaults to current working directory)

    Returns:
        Path to MAIN project root (not worktree), or None if not found

    Examples:
        >>> # From main repo
        >>> root = locate_project_root()
        >>> assert (root / ".kittify").exists()

        >>> # From worktree - returns MAIN repo, not worktree
        >>> root = locate_project_root(Path(".worktrees/my-feature"))
        >>> assert ".worktrees" not in str(root)
    """
    # Tier 1: Check environment variable (allows override for CI/CD)
    if env_root := os.getenv("SPECIFY_REPO_ROOT"):
        env_path = None
        if env_path.exists() and (env_path / KITTIFY_DIR).is_dir():
            return env_path
        # Invalid env var - fall through to other methods

    # Tier 2: Walk up directory tree, handling worktree .git files
    current = (start or Path.cwd()).resolve()

    for candidate in [current, *current.parents]:
        git_path = candidate / ".git"

        if git_path.is_file():
            # .git files with gitdir: pointers appear in worktrees,
            # submodules, and separate-git-dir clones.  Only follow the
            # pointer when it has the .git/worktrees/<name> topology.
            try:
                content = git_path.read_text().strip()
                if content.startswith("gitdir:"):
                    gitdir = Path(content.split(":", 1)[1].strip())
                    if _is_worktree_gitdir(gitdir):
                        # Navigate: .git/worktrees/name -> .git -> main repo root
                        main_git_dir = gitdir.parent.parent
                        main_repo = main_git_dir.parent
                        if main_repo.exists() and (main_repo / KITTIFY_DIR).is_dir():
                            return main_repo
            except (OSError, ValueError):
                # If we can't read or parse the .git file, continue searching
                pass

        elif git_path.is_dir():
            # This is the main repo (or a regular git repo)
            if (candidate / KITTIFY_DIR).is_dir():
                return candidate

        # Also check for .kittify marker (fallback for non-git scenarios)
        kittify_path = candidate / KITTIFY_DIR
        if kittify_path.is_symlink() and not kittify_path.exists():
            # Broken symlink - skip this candidate
            continue
        if kittify_path.is_dir():
            return candidate

    return None


def x_locate_project_root__mutmut_5(start: Path | None = None) -> Optional[Path]:
    """
    Locate the MAIN spec-kitty project root directory, even from within worktrees.

    This function correctly handles git worktrees by detecting when .git is a
    file (worktree pointer) vs a directory (main repo), and following the
    pointer back to the main repository.

    Resolution order:
    1. SPECIFY_REPO_ROOT environment variable (highest priority)
    2. Walk up directory tree, detecting worktree .git files and following to main repo
    3. Fall back to .kittify/ marker search

    Args:
        start: Starting directory for search (defaults to current working directory)

    Returns:
        Path to MAIN project root (not worktree), or None if not found

    Examples:
        >>> # From main repo
        >>> root = locate_project_root()
        >>> assert (root / ".kittify").exists()

        >>> # From worktree - returns MAIN repo, not worktree
        >>> root = locate_project_root(Path(".worktrees/my-feature"))
        >>> assert ".worktrees" not in str(root)
    """
    # Tier 1: Check environment variable (allows override for CI/CD)
    if env_root := os.getenv("SPECIFY_REPO_ROOT"):
        env_path = Path(None).resolve()
        if env_path.exists() and (env_path / KITTIFY_DIR).is_dir():
            return env_path
        # Invalid env var - fall through to other methods

    # Tier 2: Walk up directory tree, handling worktree .git files
    current = (start or Path.cwd()).resolve()

    for candidate in [current, *current.parents]:
        git_path = candidate / ".git"

        if git_path.is_file():
            # .git files with gitdir: pointers appear in worktrees,
            # submodules, and separate-git-dir clones.  Only follow the
            # pointer when it has the .git/worktrees/<name> topology.
            try:
                content = git_path.read_text().strip()
                if content.startswith("gitdir:"):
                    gitdir = Path(content.split(":", 1)[1].strip())
                    if _is_worktree_gitdir(gitdir):
                        # Navigate: .git/worktrees/name -> .git -> main repo root
                        main_git_dir = gitdir.parent.parent
                        main_repo = main_git_dir.parent
                        if main_repo.exists() and (main_repo / KITTIFY_DIR).is_dir():
                            return main_repo
            except (OSError, ValueError):
                # If we can't read or parse the .git file, continue searching
                pass

        elif git_path.is_dir():
            # This is the main repo (or a regular git repo)
            if (candidate / KITTIFY_DIR).is_dir():
                return candidate

        # Also check for .kittify marker (fallback for non-git scenarios)
        kittify_path = candidate / KITTIFY_DIR
        if kittify_path.is_symlink() and not kittify_path.exists():
            # Broken symlink - skip this candidate
            continue
        if kittify_path.is_dir():
            return candidate

    return None


def x_locate_project_root__mutmut_6(start: Path | None = None) -> Optional[Path]:
    """
    Locate the MAIN spec-kitty project root directory, even from within worktrees.

    This function correctly handles git worktrees by detecting when .git is a
    file (worktree pointer) vs a directory (main repo), and following the
    pointer back to the main repository.

    Resolution order:
    1. SPECIFY_REPO_ROOT environment variable (highest priority)
    2. Walk up directory tree, detecting worktree .git files and following to main repo
    3. Fall back to .kittify/ marker search

    Args:
        start: Starting directory for search (defaults to current working directory)

    Returns:
        Path to MAIN project root (not worktree), or None if not found

    Examples:
        >>> # From main repo
        >>> root = locate_project_root()
        >>> assert (root / ".kittify").exists()

        >>> # From worktree - returns MAIN repo, not worktree
        >>> root = locate_project_root(Path(".worktrees/my-feature"))
        >>> assert ".worktrees" not in str(root)
    """
    # Tier 1: Check environment variable (allows override for CI/CD)
    if env_root := os.getenv("SPECIFY_REPO_ROOT"):
        env_path = Path(env_root).resolve()
        if env_path.exists() or (env_path / KITTIFY_DIR).is_dir():
            return env_path
        # Invalid env var - fall through to other methods

    # Tier 2: Walk up directory tree, handling worktree .git files
    current = (start or Path.cwd()).resolve()

    for candidate in [current, *current.parents]:
        git_path = candidate / ".git"

        if git_path.is_file():
            # .git files with gitdir: pointers appear in worktrees,
            # submodules, and separate-git-dir clones.  Only follow the
            # pointer when it has the .git/worktrees/<name> topology.
            try:
                content = git_path.read_text().strip()
                if content.startswith("gitdir:"):
                    gitdir = Path(content.split(":", 1)[1].strip())
                    if _is_worktree_gitdir(gitdir):
                        # Navigate: .git/worktrees/name -> .git -> main repo root
                        main_git_dir = gitdir.parent.parent
                        main_repo = main_git_dir.parent
                        if main_repo.exists() and (main_repo / KITTIFY_DIR).is_dir():
                            return main_repo
            except (OSError, ValueError):
                # If we can't read or parse the .git file, continue searching
                pass

        elif git_path.is_dir():
            # This is the main repo (or a regular git repo)
            if (candidate / KITTIFY_DIR).is_dir():
                return candidate

        # Also check for .kittify marker (fallback for non-git scenarios)
        kittify_path = candidate / KITTIFY_DIR
        if kittify_path.is_symlink() and not kittify_path.exists():
            # Broken symlink - skip this candidate
            continue
        if kittify_path.is_dir():
            return candidate

    return None


def x_locate_project_root__mutmut_7(start: Path | None = None) -> Optional[Path]:
    """
    Locate the MAIN spec-kitty project root directory, even from within worktrees.

    This function correctly handles git worktrees by detecting when .git is a
    file (worktree pointer) vs a directory (main repo), and following the
    pointer back to the main repository.

    Resolution order:
    1. SPECIFY_REPO_ROOT environment variable (highest priority)
    2. Walk up directory tree, detecting worktree .git files and following to main repo
    3. Fall back to .kittify/ marker search

    Args:
        start: Starting directory for search (defaults to current working directory)

    Returns:
        Path to MAIN project root (not worktree), or None if not found

    Examples:
        >>> # From main repo
        >>> root = locate_project_root()
        >>> assert (root / ".kittify").exists()

        >>> # From worktree - returns MAIN repo, not worktree
        >>> root = locate_project_root(Path(".worktrees/my-feature"))
        >>> assert ".worktrees" not in str(root)
    """
    # Tier 1: Check environment variable (allows override for CI/CD)
    if env_root := os.getenv("SPECIFY_REPO_ROOT"):
        env_path = Path(env_root).resolve()
        if env_path.exists() and (env_path * KITTIFY_DIR).is_dir():
            return env_path
        # Invalid env var - fall through to other methods

    # Tier 2: Walk up directory tree, handling worktree .git files
    current = (start or Path.cwd()).resolve()

    for candidate in [current, *current.parents]:
        git_path = candidate / ".git"

        if git_path.is_file():
            # .git files with gitdir: pointers appear in worktrees,
            # submodules, and separate-git-dir clones.  Only follow the
            # pointer when it has the .git/worktrees/<name> topology.
            try:
                content = git_path.read_text().strip()
                if content.startswith("gitdir:"):
                    gitdir = Path(content.split(":", 1)[1].strip())
                    if _is_worktree_gitdir(gitdir):
                        # Navigate: .git/worktrees/name -> .git -> main repo root
                        main_git_dir = gitdir.parent.parent
                        main_repo = main_git_dir.parent
                        if main_repo.exists() and (main_repo / KITTIFY_DIR).is_dir():
                            return main_repo
            except (OSError, ValueError):
                # If we can't read or parse the .git file, continue searching
                pass

        elif git_path.is_dir():
            # This is the main repo (or a regular git repo)
            if (candidate / KITTIFY_DIR).is_dir():
                return candidate

        # Also check for .kittify marker (fallback for non-git scenarios)
        kittify_path = candidate / KITTIFY_DIR
        if kittify_path.is_symlink() and not kittify_path.exists():
            # Broken symlink - skip this candidate
            continue
        if kittify_path.is_dir():
            return candidate

    return None


def x_locate_project_root__mutmut_8(start: Path | None = None) -> Optional[Path]:
    """
    Locate the MAIN spec-kitty project root directory, even from within worktrees.

    This function correctly handles git worktrees by detecting when .git is a
    file (worktree pointer) vs a directory (main repo), and following the
    pointer back to the main repository.

    Resolution order:
    1. SPECIFY_REPO_ROOT environment variable (highest priority)
    2. Walk up directory tree, detecting worktree .git files and following to main repo
    3. Fall back to .kittify/ marker search

    Args:
        start: Starting directory for search (defaults to current working directory)

    Returns:
        Path to MAIN project root (not worktree), or None if not found

    Examples:
        >>> # From main repo
        >>> root = locate_project_root()
        >>> assert (root / ".kittify").exists()

        >>> # From worktree - returns MAIN repo, not worktree
        >>> root = locate_project_root(Path(".worktrees/my-feature"))
        >>> assert ".worktrees" not in str(root)
    """
    # Tier 1: Check environment variable (allows override for CI/CD)
    if env_root := os.getenv("SPECIFY_REPO_ROOT"):
        env_path = Path(env_root).resolve()
        if env_path.exists() and (env_path / KITTIFY_DIR).is_dir():
            return env_path
        # Invalid env var - fall through to other methods

    # Tier 2: Walk up directory tree, handling worktree .git files
    current = None

    for candidate in [current, *current.parents]:
        git_path = candidate / ".git"

        if git_path.is_file():
            # .git files with gitdir: pointers appear in worktrees,
            # submodules, and separate-git-dir clones.  Only follow the
            # pointer when it has the .git/worktrees/<name> topology.
            try:
                content = git_path.read_text().strip()
                if content.startswith("gitdir:"):
                    gitdir = Path(content.split(":", 1)[1].strip())
                    if _is_worktree_gitdir(gitdir):
                        # Navigate: .git/worktrees/name -> .git -> main repo root
                        main_git_dir = gitdir.parent.parent
                        main_repo = main_git_dir.parent
                        if main_repo.exists() and (main_repo / KITTIFY_DIR).is_dir():
                            return main_repo
            except (OSError, ValueError):
                # If we can't read or parse the .git file, continue searching
                pass

        elif git_path.is_dir():
            # This is the main repo (or a regular git repo)
            if (candidate / KITTIFY_DIR).is_dir():
                return candidate

        # Also check for .kittify marker (fallback for non-git scenarios)
        kittify_path = candidate / KITTIFY_DIR
        if kittify_path.is_symlink() and not kittify_path.exists():
            # Broken symlink - skip this candidate
            continue
        if kittify_path.is_dir():
            return candidate

    return None


def x_locate_project_root__mutmut_9(start: Path | None = None) -> Optional[Path]:
    """
    Locate the MAIN spec-kitty project root directory, even from within worktrees.

    This function correctly handles git worktrees by detecting when .git is a
    file (worktree pointer) vs a directory (main repo), and following the
    pointer back to the main repository.

    Resolution order:
    1. SPECIFY_REPO_ROOT environment variable (highest priority)
    2. Walk up directory tree, detecting worktree .git files and following to main repo
    3. Fall back to .kittify/ marker search

    Args:
        start: Starting directory for search (defaults to current working directory)

    Returns:
        Path to MAIN project root (not worktree), or None if not found

    Examples:
        >>> # From main repo
        >>> root = locate_project_root()
        >>> assert (root / ".kittify").exists()

        >>> # From worktree - returns MAIN repo, not worktree
        >>> root = locate_project_root(Path(".worktrees/my-feature"))
        >>> assert ".worktrees" not in str(root)
    """
    # Tier 1: Check environment variable (allows override for CI/CD)
    if env_root := os.getenv("SPECIFY_REPO_ROOT"):
        env_path = Path(env_root).resolve()
        if env_path.exists() and (env_path / KITTIFY_DIR).is_dir():
            return env_path
        # Invalid env var - fall through to other methods

    # Tier 2: Walk up directory tree, handling worktree .git files
    current = (start and Path.cwd()).resolve()

    for candidate in [current, *current.parents]:
        git_path = candidate / ".git"

        if git_path.is_file():
            # .git files with gitdir: pointers appear in worktrees,
            # submodules, and separate-git-dir clones.  Only follow the
            # pointer when it has the .git/worktrees/<name> topology.
            try:
                content = git_path.read_text().strip()
                if content.startswith("gitdir:"):
                    gitdir = Path(content.split(":", 1)[1].strip())
                    if _is_worktree_gitdir(gitdir):
                        # Navigate: .git/worktrees/name -> .git -> main repo root
                        main_git_dir = gitdir.parent.parent
                        main_repo = main_git_dir.parent
                        if main_repo.exists() and (main_repo / KITTIFY_DIR).is_dir():
                            return main_repo
            except (OSError, ValueError):
                # If we can't read or parse the .git file, continue searching
                pass

        elif git_path.is_dir():
            # This is the main repo (or a regular git repo)
            if (candidate / KITTIFY_DIR).is_dir():
                return candidate

        # Also check for .kittify marker (fallback for non-git scenarios)
        kittify_path = candidate / KITTIFY_DIR
        if kittify_path.is_symlink() and not kittify_path.exists():
            # Broken symlink - skip this candidate
            continue
        if kittify_path.is_dir():
            return candidate

    return None


def x_locate_project_root__mutmut_10(start: Path | None = None) -> Optional[Path]:
    """
    Locate the MAIN spec-kitty project root directory, even from within worktrees.

    This function correctly handles git worktrees by detecting when .git is a
    file (worktree pointer) vs a directory (main repo), and following the
    pointer back to the main repository.

    Resolution order:
    1. SPECIFY_REPO_ROOT environment variable (highest priority)
    2. Walk up directory tree, detecting worktree .git files and following to main repo
    3. Fall back to .kittify/ marker search

    Args:
        start: Starting directory for search (defaults to current working directory)

    Returns:
        Path to MAIN project root (not worktree), or None if not found

    Examples:
        >>> # From main repo
        >>> root = locate_project_root()
        >>> assert (root / ".kittify").exists()

        >>> # From worktree - returns MAIN repo, not worktree
        >>> root = locate_project_root(Path(".worktrees/my-feature"))
        >>> assert ".worktrees" not in str(root)
    """
    # Tier 1: Check environment variable (allows override for CI/CD)
    if env_root := os.getenv("SPECIFY_REPO_ROOT"):
        env_path = Path(env_root).resolve()
        if env_path.exists() and (env_path / KITTIFY_DIR).is_dir():
            return env_path
        # Invalid env var - fall through to other methods

    # Tier 2: Walk up directory tree, handling worktree .git files
    current = (start or Path.cwd()).resolve()

    for candidate in [current, *current.parents]:
        git_path = None

        if git_path.is_file():
            # .git files with gitdir: pointers appear in worktrees,
            # submodules, and separate-git-dir clones.  Only follow the
            # pointer when it has the .git/worktrees/<name> topology.
            try:
                content = git_path.read_text().strip()
                if content.startswith("gitdir:"):
                    gitdir = Path(content.split(":", 1)[1].strip())
                    if _is_worktree_gitdir(gitdir):
                        # Navigate: .git/worktrees/name -> .git -> main repo root
                        main_git_dir = gitdir.parent.parent
                        main_repo = main_git_dir.parent
                        if main_repo.exists() and (main_repo / KITTIFY_DIR).is_dir():
                            return main_repo
            except (OSError, ValueError):
                # If we can't read or parse the .git file, continue searching
                pass

        elif git_path.is_dir():
            # This is the main repo (or a regular git repo)
            if (candidate / KITTIFY_DIR).is_dir():
                return candidate

        # Also check for .kittify marker (fallback for non-git scenarios)
        kittify_path = candidate / KITTIFY_DIR
        if kittify_path.is_symlink() and not kittify_path.exists():
            # Broken symlink - skip this candidate
            continue
        if kittify_path.is_dir():
            return candidate

    return None


def x_locate_project_root__mutmut_11(start: Path | None = None) -> Optional[Path]:
    """
    Locate the MAIN spec-kitty project root directory, even from within worktrees.

    This function correctly handles git worktrees by detecting when .git is a
    file (worktree pointer) vs a directory (main repo), and following the
    pointer back to the main repository.

    Resolution order:
    1. SPECIFY_REPO_ROOT environment variable (highest priority)
    2. Walk up directory tree, detecting worktree .git files and following to main repo
    3. Fall back to .kittify/ marker search

    Args:
        start: Starting directory for search (defaults to current working directory)

    Returns:
        Path to MAIN project root (not worktree), or None if not found

    Examples:
        >>> # From main repo
        >>> root = locate_project_root()
        >>> assert (root / ".kittify").exists()

        >>> # From worktree - returns MAIN repo, not worktree
        >>> root = locate_project_root(Path(".worktrees/my-feature"))
        >>> assert ".worktrees" not in str(root)
    """
    # Tier 1: Check environment variable (allows override for CI/CD)
    if env_root := os.getenv("SPECIFY_REPO_ROOT"):
        env_path = Path(env_root).resolve()
        if env_path.exists() and (env_path / KITTIFY_DIR).is_dir():
            return env_path
        # Invalid env var - fall through to other methods

    # Tier 2: Walk up directory tree, handling worktree .git files
    current = (start or Path.cwd()).resolve()

    for candidate in [current, *current.parents]:
        git_path = candidate * ".git"

        if git_path.is_file():
            # .git files with gitdir: pointers appear in worktrees,
            # submodules, and separate-git-dir clones.  Only follow the
            # pointer when it has the .git/worktrees/<name> topology.
            try:
                content = git_path.read_text().strip()
                if content.startswith("gitdir:"):
                    gitdir = Path(content.split(":", 1)[1].strip())
                    if _is_worktree_gitdir(gitdir):
                        # Navigate: .git/worktrees/name -> .git -> main repo root
                        main_git_dir = gitdir.parent.parent
                        main_repo = main_git_dir.parent
                        if main_repo.exists() and (main_repo / KITTIFY_DIR).is_dir():
                            return main_repo
            except (OSError, ValueError):
                # If we can't read or parse the .git file, continue searching
                pass

        elif git_path.is_dir():
            # This is the main repo (or a regular git repo)
            if (candidate / KITTIFY_DIR).is_dir():
                return candidate

        # Also check for .kittify marker (fallback for non-git scenarios)
        kittify_path = candidate / KITTIFY_DIR
        if kittify_path.is_symlink() and not kittify_path.exists():
            # Broken symlink - skip this candidate
            continue
        if kittify_path.is_dir():
            return candidate

    return None


def x_locate_project_root__mutmut_12(start: Path | None = None) -> Optional[Path]:
    """
    Locate the MAIN spec-kitty project root directory, even from within worktrees.

    This function correctly handles git worktrees by detecting when .git is a
    file (worktree pointer) vs a directory (main repo), and following the
    pointer back to the main repository.

    Resolution order:
    1. SPECIFY_REPO_ROOT environment variable (highest priority)
    2. Walk up directory tree, detecting worktree .git files and following to main repo
    3. Fall back to .kittify/ marker search

    Args:
        start: Starting directory for search (defaults to current working directory)

    Returns:
        Path to MAIN project root (not worktree), or None if not found

    Examples:
        >>> # From main repo
        >>> root = locate_project_root()
        >>> assert (root / ".kittify").exists()

        >>> # From worktree - returns MAIN repo, not worktree
        >>> root = locate_project_root(Path(".worktrees/my-feature"))
        >>> assert ".worktrees" not in str(root)
    """
    # Tier 1: Check environment variable (allows override for CI/CD)
    if env_root := os.getenv("SPECIFY_REPO_ROOT"):
        env_path = Path(env_root).resolve()
        if env_path.exists() and (env_path / KITTIFY_DIR).is_dir():
            return env_path
        # Invalid env var - fall through to other methods

    # Tier 2: Walk up directory tree, handling worktree .git files
    current = (start or Path.cwd()).resolve()

    for candidate in [current, *current.parents]:
        git_path = candidate / "XX.gitXX"

        if git_path.is_file():
            # .git files with gitdir: pointers appear in worktrees,
            # submodules, and separate-git-dir clones.  Only follow the
            # pointer when it has the .git/worktrees/<name> topology.
            try:
                content = git_path.read_text().strip()
                if content.startswith("gitdir:"):
                    gitdir = Path(content.split(":", 1)[1].strip())
                    if _is_worktree_gitdir(gitdir):
                        # Navigate: .git/worktrees/name -> .git -> main repo root
                        main_git_dir = gitdir.parent.parent
                        main_repo = main_git_dir.parent
                        if main_repo.exists() and (main_repo / KITTIFY_DIR).is_dir():
                            return main_repo
            except (OSError, ValueError):
                # If we can't read or parse the .git file, continue searching
                pass

        elif git_path.is_dir():
            # This is the main repo (or a regular git repo)
            if (candidate / KITTIFY_DIR).is_dir():
                return candidate

        # Also check for .kittify marker (fallback for non-git scenarios)
        kittify_path = candidate / KITTIFY_DIR
        if kittify_path.is_symlink() and not kittify_path.exists():
            # Broken symlink - skip this candidate
            continue
        if kittify_path.is_dir():
            return candidate

    return None


def x_locate_project_root__mutmut_13(start: Path | None = None) -> Optional[Path]:
    """
    Locate the MAIN spec-kitty project root directory, even from within worktrees.

    This function correctly handles git worktrees by detecting when .git is a
    file (worktree pointer) vs a directory (main repo), and following the
    pointer back to the main repository.

    Resolution order:
    1. SPECIFY_REPO_ROOT environment variable (highest priority)
    2. Walk up directory tree, detecting worktree .git files and following to main repo
    3. Fall back to .kittify/ marker search

    Args:
        start: Starting directory for search (defaults to current working directory)

    Returns:
        Path to MAIN project root (not worktree), or None if not found

    Examples:
        >>> # From main repo
        >>> root = locate_project_root()
        >>> assert (root / ".kittify").exists()

        >>> # From worktree - returns MAIN repo, not worktree
        >>> root = locate_project_root(Path(".worktrees/my-feature"))
        >>> assert ".worktrees" not in str(root)
    """
    # Tier 1: Check environment variable (allows override for CI/CD)
    if env_root := os.getenv("SPECIFY_REPO_ROOT"):
        env_path = Path(env_root).resolve()
        if env_path.exists() and (env_path / KITTIFY_DIR).is_dir():
            return env_path
        # Invalid env var - fall through to other methods

    # Tier 2: Walk up directory tree, handling worktree .git files
    current = (start or Path.cwd()).resolve()

    for candidate in [current, *current.parents]:
        git_path = candidate / ".GIT"

        if git_path.is_file():
            # .git files with gitdir: pointers appear in worktrees,
            # submodules, and separate-git-dir clones.  Only follow the
            # pointer when it has the .git/worktrees/<name> topology.
            try:
                content = git_path.read_text().strip()
                if content.startswith("gitdir:"):
                    gitdir = Path(content.split(":", 1)[1].strip())
                    if _is_worktree_gitdir(gitdir):
                        # Navigate: .git/worktrees/name -> .git -> main repo root
                        main_git_dir = gitdir.parent.parent
                        main_repo = main_git_dir.parent
                        if main_repo.exists() and (main_repo / KITTIFY_DIR).is_dir():
                            return main_repo
            except (OSError, ValueError):
                # If we can't read or parse the .git file, continue searching
                pass

        elif git_path.is_dir():
            # This is the main repo (or a regular git repo)
            if (candidate / KITTIFY_DIR).is_dir():
                return candidate

        # Also check for .kittify marker (fallback for non-git scenarios)
        kittify_path = candidate / KITTIFY_DIR
        if kittify_path.is_symlink() and not kittify_path.exists():
            # Broken symlink - skip this candidate
            continue
        if kittify_path.is_dir():
            return candidate

    return None


def x_locate_project_root__mutmut_14(start: Path | None = None) -> Optional[Path]:
    """
    Locate the MAIN spec-kitty project root directory, even from within worktrees.

    This function correctly handles git worktrees by detecting when .git is a
    file (worktree pointer) vs a directory (main repo), and following the
    pointer back to the main repository.

    Resolution order:
    1. SPECIFY_REPO_ROOT environment variable (highest priority)
    2. Walk up directory tree, detecting worktree .git files and following to main repo
    3. Fall back to .kittify/ marker search

    Args:
        start: Starting directory for search (defaults to current working directory)

    Returns:
        Path to MAIN project root (not worktree), or None if not found

    Examples:
        >>> # From main repo
        >>> root = locate_project_root()
        >>> assert (root / ".kittify").exists()

        >>> # From worktree - returns MAIN repo, not worktree
        >>> root = locate_project_root(Path(".worktrees/my-feature"))
        >>> assert ".worktrees" not in str(root)
    """
    # Tier 1: Check environment variable (allows override for CI/CD)
    if env_root := os.getenv("SPECIFY_REPO_ROOT"):
        env_path = Path(env_root).resolve()
        if env_path.exists() and (env_path / KITTIFY_DIR).is_dir():
            return env_path
        # Invalid env var - fall through to other methods

    # Tier 2: Walk up directory tree, handling worktree .git files
    current = (start or Path.cwd()).resolve()

    for candidate in [current, *current.parents]:
        git_path = candidate / ".git"

        if git_path.is_file():
            # .git files with gitdir: pointers appear in worktrees,
            # submodules, and separate-git-dir clones.  Only follow the
            # pointer when it has the .git/worktrees/<name> topology.
            try:
                content = None
                if content.startswith("gitdir:"):
                    gitdir = Path(content.split(":", 1)[1].strip())
                    if _is_worktree_gitdir(gitdir):
                        # Navigate: .git/worktrees/name -> .git -> main repo root
                        main_git_dir = gitdir.parent.parent
                        main_repo = main_git_dir.parent
                        if main_repo.exists() and (main_repo / KITTIFY_DIR).is_dir():
                            return main_repo
            except (OSError, ValueError):
                # If we can't read or parse the .git file, continue searching
                pass

        elif git_path.is_dir():
            # This is the main repo (or a regular git repo)
            if (candidate / KITTIFY_DIR).is_dir():
                return candidate

        # Also check for .kittify marker (fallback for non-git scenarios)
        kittify_path = candidate / KITTIFY_DIR
        if kittify_path.is_symlink() and not kittify_path.exists():
            # Broken symlink - skip this candidate
            continue
        if kittify_path.is_dir():
            return candidate

    return None


def x_locate_project_root__mutmut_15(start: Path | None = None) -> Optional[Path]:
    """
    Locate the MAIN spec-kitty project root directory, even from within worktrees.

    This function correctly handles git worktrees by detecting when .git is a
    file (worktree pointer) vs a directory (main repo), and following the
    pointer back to the main repository.

    Resolution order:
    1. SPECIFY_REPO_ROOT environment variable (highest priority)
    2. Walk up directory tree, detecting worktree .git files and following to main repo
    3. Fall back to .kittify/ marker search

    Args:
        start: Starting directory for search (defaults to current working directory)

    Returns:
        Path to MAIN project root (not worktree), or None if not found

    Examples:
        >>> # From main repo
        >>> root = locate_project_root()
        >>> assert (root / ".kittify").exists()

        >>> # From worktree - returns MAIN repo, not worktree
        >>> root = locate_project_root(Path(".worktrees/my-feature"))
        >>> assert ".worktrees" not in str(root)
    """
    # Tier 1: Check environment variable (allows override for CI/CD)
    if env_root := os.getenv("SPECIFY_REPO_ROOT"):
        env_path = Path(env_root).resolve()
        if env_path.exists() and (env_path / KITTIFY_DIR).is_dir():
            return env_path
        # Invalid env var - fall through to other methods

    # Tier 2: Walk up directory tree, handling worktree .git files
    current = (start or Path.cwd()).resolve()

    for candidate in [current, *current.parents]:
        git_path = candidate / ".git"

        if git_path.is_file():
            # .git files with gitdir: pointers appear in worktrees,
            # submodules, and separate-git-dir clones.  Only follow the
            # pointer when it has the .git/worktrees/<name> topology.
            try:
                content = git_path.read_text().strip()
                if content.startswith(None):
                    gitdir = Path(content.split(":", 1)[1].strip())
                    if _is_worktree_gitdir(gitdir):
                        # Navigate: .git/worktrees/name -> .git -> main repo root
                        main_git_dir = gitdir.parent.parent
                        main_repo = main_git_dir.parent
                        if main_repo.exists() and (main_repo / KITTIFY_DIR).is_dir():
                            return main_repo
            except (OSError, ValueError):
                # If we can't read or parse the .git file, continue searching
                pass

        elif git_path.is_dir():
            # This is the main repo (or a regular git repo)
            if (candidate / KITTIFY_DIR).is_dir():
                return candidate

        # Also check for .kittify marker (fallback for non-git scenarios)
        kittify_path = candidate / KITTIFY_DIR
        if kittify_path.is_symlink() and not kittify_path.exists():
            # Broken symlink - skip this candidate
            continue
        if kittify_path.is_dir():
            return candidate

    return None


def x_locate_project_root__mutmut_16(start: Path | None = None) -> Optional[Path]:
    """
    Locate the MAIN spec-kitty project root directory, even from within worktrees.

    This function correctly handles git worktrees by detecting when .git is a
    file (worktree pointer) vs a directory (main repo), and following the
    pointer back to the main repository.

    Resolution order:
    1. SPECIFY_REPO_ROOT environment variable (highest priority)
    2. Walk up directory tree, detecting worktree .git files and following to main repo
    3. Fall back to .kittify/ marker search

    Args:
        start: Starting directory for search (defaults to current working directory)

    Returns:
        Path to MAIN project root (not worktree), or None if not found

    Examples:
        >>> # From main repo
        >>> root = locate_project_root()
        >>> assert (root / ".kittify").exists()

        >>> # From worktree - returns MAIN repo, not worktree
        >>> root = locate_project_root(Path(".worktrees/my-feature"))
        >>> assert ".worktrees" not in str(root)
    """
    # Tier 1: Check environment variable (allows override for CI/CD)
    if env_root := os.getenv("SPECIFY_REPO_ROOT"):
        env_path = Path(env_root).resolve()
        if env_path.exists() and (env_path / KITTIFY_DIR).is_dir():
            return env_path
        # Invalid env var - fall through to other methods

    # Tier 2: Walk up directory tree, handling worktree .git files
    current = (start or Path.cwd()).resolve()

    for candidate in [current, *current.parents]:
        git_path = candidate / ".git"

        if git_path.is_file():
            # .git files with gitdir: pointers appear in worktrees,
            # submodules, and separate-git-dir clones.  Only follow the
            # pointer when it has the .git/worktrees/<name> topology.
            try:
                content = git_path.read_text().strip()
                if content.startswith("XXgitdir:XX"):
                    gitdir = Path(content.split(":", 1)[1].strip())
                    if _is_worktree_gitdir(gitdir):
                        # Navigate: .git/worktrees/name -> .git -> main repo root
                        main_git_dir = gitdir.parent.parent
                        main_repo = main_git_dir.parent
                        if main_repo.exists() and (main_repo / KITTIFY_DIR).is_dir():
                            return main_repo
            except (OSError, ValueError):
                # If we can't read or parse the .git file, continue searching
                pass

        elif git_path.is_dir():
            # This is the main repo (or a regular git repo)
            if (candidate / KITTIFY_DIR).is_dir():
                return candidate

        # Also check for .kittify marker (fallback for non-git scenarios)
        kittify_path = candidate / KITTIFY_DIR
        if kittify_path.is_symlink() and not kittify_path.exists():
            # Broken symlink - skip this candidate
            continue
        if kittify_path.is_dir():
            return candidate

    return None


def x_locate_project_root__mutmut_17(start: Path | None = None) -> Optional[Path]:
    """
    Locate the MAIN spec-kitty project root directory, even from within worktrees.

    This function correctly handles git worktrees by detecting when .git is a
    file (worktree pointer) vs a directory (main repo), and following the
    pointer back to the main repository.

    Resolution order:
    1. SPECIFY_REPO_ROOT environment variable (highest priority)
    2. Walk up directory tree, detecting worktree .git files and following to main repo
    3. Fall back to .kittify/ marker search

    Args:
        start: Starting directory for search (defaults to current working directory)

    Returns:
        Path to MAIN project root (not worktree), or None if not found

    Examples:
        >>> # From main repo
        >>> root = locate_project_root()
        >>> assert (root / ".kittify").exists()

        >>> # From worktree - returns MAIN repo, not worktree
        >>> root = locate_project_root(Path(".worktrees/my-feature"))
        >>> assert ".worktrees" not in str(root)
    """
    # Tier 1: Check environment variable (allows override for CI/CD)
    if env_root := os.getenv("SPECIFY_REPO_ROOT"):
        env_path = Path(env_root).resolve()
        if env_path.exists() and (env_path / KITTIFY_DIR).is_dir():
            return env_path
        # Invalid env var - fall through to other methods

    # Tier 2: Walk up directory tree, handling worktree .git files
    current = (start or Path.cwd()).resolve()

    for candidate in [current, *current.parents]:
        git_path = candidate / ".git"

        if git_path.is_file():
            # .git files with gitdir: pointers appear in worktrees,
            # submodules, and separate-git-dir clones.  Only follow the
            # pointer when it has the .git/worktrees/<name> topology.
            try:
                content = git_path.read_text().strip()
                if content.startswith("GITDIR:"):
                    gitdir = Path(content.split(":", 1)[1].strip())
                    if _is_worktree_gitdir(gitdir):
                        # Navigate: .git/worktrees/name -> .git -> main repo root
                        main_git_dir = gitdir.parent.parent
                        main_repo = main_git_dir.parent
                        if main_repo.exists() and (main_repo / KITTIFY_DIR).is_dir():
                            return main_repo
            except (OSError, ValueError):
                # If we can't read or parse the .git file, continue searching
                pass

        elif git_path.is_dir():
            # This is the main repo (or a regular git repo)
            if (candidate / KITTIFY_DIR).is_dir():
                return candidate

        # Also check for .kittify marker (fallback for non-git scenarios)
        kittify_path = candidate / KITTIFY_DIR
        if kittify_path.is_symlink() and not kittify_path.exists():
            # Broken symlink - skip this candidate
            continue
        if kittify_path.is_dir():
            return candidate

    return None


def x_locate_project_root__mutmut_18(start: Path | None = None) -> Optional[Path]:
    """
    Locate the MAIN spec-kitty project root directory, even from within worktrees.

    This function correctly handles git worktrees by detecting when .git is a
    file (worktree pointer) vs a directory (main repo), and following the
    pointer back to the main repository.

    Resolution order:
    1. SPECIFY_REPO_ROOT environment variable (highest priority)
    2. Walk up directory tree, detecting worktree .git files and following to main repo
    3. Fall back to .kittify/ marker search

    Args:
        start: Starting directory for search (defaults to current working directory)

    Returns:
        Path to MAIN project root (not worktree), or None if not found

    Examples:
        >>> # From main repo
        >>> root = locate_project_root()
        >>> assert (root / ".kittify").exists()

        >>> # From worktree - returns MAIN repo, not worktree
        >>> root = locate_project_root(Path(".worktrees/my-feature"))
        >>> assert ".worktrees" not in str(root)
    """
    # Tier 1: Check environment variable (allows override for CI/CD)
    if env_root := os.getenv("SPECIFY_REPO_ROOT"):
        env_path = Path(env_root).resolve()
        if env_path.exists() and (env_path / KITTIFY_DIR).is_dir():
            return env_path
        # Invalid env var - fall through to other methods

    # Tier 2: Walk up directory tree, handling worktree .git files
    current = (start or Path.cwd()).resolve()

    for candidate in [current, *current.parents]:
        git_path = candidate / ".git"

        if git_path.is_file():
            # .git files with gitdir: pointers appear in worktrees,
            # submodules, and separate-git-dir clones.  Only follow the
            # pointer when it has the .git/worktrees/<name> topology.
            try:
                content = git_path.read_text().strip()
                if content.startswith("gitdir:"):
                    gitdir = None
                    if _is_worktree_gitdir(gitdir):
                        # Navigate: .git/worktrees/name -> .git -> main repo root
                        main_git_dir = gitdir.parent.parent
                        main_repo = main_git_dir.parent
                        if main_repo.exists() and (main_repo / KITTIFY_DIR).is_dir():
                            return main_repo
            except (OSError, ValueError):
                # If we can't read or parse the .git file, continue searching
                pass

        elif git_path.is_dir():
            # This is the main repo (or a regular git repo)
            if (candidate / KITTIFY_DIR).is_dir():
                return candidate

        # Also check for .kittify marker (fallback for non-git scenarios)
        kittify_path = candidate / KITTIFY_DIR
        if kittify_path.is_symlink() and not kittify_path.exists():
            # Broken symlink - skip this candidate
            continue
        if kittify_path.is_dir():
            return candidate

    return None


def x_locate_project_root__mutmut_19(start: Path | None = None) -> Optional[Path]:
    """
    Locate the MAIN spec-kitty project root directory, even from within worktrees.

    This function correctly handles git worktrees by detecting when .git is a
    file (worktree pointer) vs a directory (main repo), and following the
    pointer back to the main repository.

    Resolution order:
    1. SPECIFY_REPO_ROOT environment variable (highest priority)
    2. Walk up directory tree, detecting worktree .git files and following to main repo
    3. Fall back to .kittify/ marker search

    Args:
        start: Starting directory for search (defaults to current working directory)

    Returns:
        Path to MAIN project root (not worktree), or None if not found

    Examples:
        >>> # From main repo
        >>> root = locate_project_root()
        >>> assert (root / ".kittify").exists()

        >>> # From worktree - returns MAIN repo, not worktree
        >>> root = locate_project_root(Path(".worktrees/my-feature"))
        >>> assert ".worktrees" not in str(root)
    """
    # Tier 1: Check environment variable (allows override for CI/CD)
    if env_root := os.getenv("SPECIFY_REPO_ROOT"):
        env_path = Path(env_root).resolve()
        if env_path.exists() and (env_path / KITTIFY_DIR).is_dir():
            return env_path
        # Invalid env var - fall through to other methods

    # Tier 2: Walk up directory tree, handling worktree .git files
    current = (start or Path.cwd()).resolve()

    for candidate in [current, *current.parents]:
        git_path = candidate / ".git"

        if git_path.is_file():
            # .git files with gitdir: pointers appear in worktrees,
            # submodules, and separate-git-dir clones.  Only follow the
            # pointer when it has the .git/worktrees/<name> topology.
            try:
                content = git_path.read_text().strip()
                if content.startswith("gitdir:"):
                    gitdir = Path(None)
                    if _is_worktree_gitdir(gitdir):
                        # Navigate: .git/worktrees/name -> .git -> main repo root
                        main_git_dir = gitdir.parent.parent
                        main_repo = main_git_dir.parent
                        if main_repo.exists() and (main_repo / KITTIFY_DIR).is_dir():
                            return main_repo
            except (OSError, ValueError):
                # If we can't read or parse the .git file, continue searching
                pass

        elif git_path.is_dir():
            # This is the main repo (or a regular git repo)
            if (candidate / KITTIFY_DIR).is_dir():
                return candidate

        # Also check for .kittify marker (fallback for non-git scenarios)
        kittify_path = candidate / KITTIFY_DIR
        if kittify_path.is_symlink() and not kittify_path.exists():
            # Broken symlink - skip this candidate
            continue
        if kittify_path.is_dir():
            return candidate

    return None


def x_locate_project_root__mutmut_20(start: Path | None = None) -> Optional[Path]:
    """
    Locate the MAIN spec-kitty project root directory, even from within worktrees.

    This function correctly handles git worktrees by detecting when .git is a
    file (worktree pointer) vs a directory (main repo), and following the
    pointer back to the main repository.

    Resolution order:
    1. SPECIFY_REPO_ROOT environment variable (highest priority)
    2. Walk up directory tree, detecting worktree .git files and following to main repo
    3. Fall back to .kittify/ marker search

    Args:
        start: Starting directory for search (defaults to current working directory)

    Returns:
        Path to MAIN project root (not worktree), or None if not found

    Examples:
        >>> # From main repo
        >>> root = locate_project_root()
        >>> assert (root / ".kittify").exists()

        >>> # From worktree - returns MAIN repo, not worktree
        >>> root = locate_project_root(Path(".worktrees/my-feature"))
        >>> assert ".worktrees" not in str(root)
    """
    # Tier 1: Check environment variable (allows override for CI/CD)
    if env_root := os.getenv("SPECIFY_REPO_ROOT"):
        env_path = Path(env_root).resolve()
        if env_path.exists() and (env_path / KITTIFY_DIR).is_dir():
            return env_path
        # Invalid env var - fall through to other methods

    # Tier 2: Walk up directory tree, handling worktree .git files
    current = (start or Path.cwd()).resolve()

    for candidate in [current, *current.parents]:
        git_path = candidate / ".git"

        if git_path.is_file():
            # .git files with gitdir: pointers appear in worktrees,
            # submodules, and separate-git-dir clones.  Only follow the
            # pointer when it has the .git/worktrees/<name> topology.
            try:
                content = git_path.read_text().strip()
                if content.startswith("gitdir:"):
                    gitdir = Path(content.split(None, 1)[1].strip())
                    if _is_worktree_gitdir(gitdir):
                        # Navigate: .git/worktrees/name -> .git -> main repo root
                        main_git_dir = gitdir.parent.parent
                        main_repo = main_git_dir.parent
                        if main_repo.exists() and (main_repo / KITTIFY_DIR).is_dir():
                            return main_repo
            except (OSError, ValueError):
                # If we can't read or parse the .git file, continue searching
                pass

        elif git_path.is_dir():
            # This is the main repo (or a regular git repo)
            if (candidate / KITTIFY_DIR).is_dir():
                return candidate

        # Also check for .kittify marker (fallback for non-git scenarios)
        kittify_path = candidate / KITTIFY_DIR
        if kittify_path.is_symlink() and not kittify_path.exists():
            # Broken symlink - skip this candidate
            continue
        if kittify_path.is_dir():
            return candidate

    return None


def x_locate_project_root__mutmut_21(start: Path | None = None) -> Optional[Path]:
    """
    Locate the MAIN spec-kitty project root directory, even from within worktrees.

    This function correctly handles git worktrees by detecting when .git is a
    file (worktree pointer) vs a directory (main repo), and following the
    pointer back to the main repository.

    Resolution order:
    1. SPECIFY_REPO_ROOT environment variable (highest priority)
    2. Walk up directory tree, detecting worktree .git files and following to main repo
    3. Fall back to .kittify/ marker search

    Args:
        start: Starting directory for search (defaults to current working directory)

    Returns:
        Path to MAIN project root (not worktree), or None if not found

    Examples:
        >>> # From main repo
        >>> root = locate_project_root()
        >>> assert (root / ".kittify").exists()

        >>> # From worktree - returns MAIN repo, not worktree
        >>> root = locate_project_root(Path(".worktrees/my-feature"))
        >>> assert ".worktrees" not in str(root)
    """
    # Tier 1: Check environment variable (allows override for CI/CD)
    if env_root := os.getenv("SPECIFY_REPO_ROOT"):
        env_path = Path(env_root).resolve()
        if env_path.exists() and (env_path / KITTIFY_DIR).is_dir():
            return env_path
        # Invalid env var - fall through to other methods

    # Tier 2: Walk up directory tree, handling worktree .git files
    current = (start or Path.cwd()).resolve()

    for candidate in [current, *current.parents]:
        git_path = candidate / ".git"

        if git_path.is_file():
            # .git files with gitdir: pointers appear in worktrees,
            # submodules, and separate-git-dir clones.  Only follow the
            # pointer when it has the .git/worktrees/<name> topology.
            try:
                content = git_path.read_text().strip()
                if content.startswith("gitdir:"):
                    gitdir = Path(content.split(":", None)[1].strip())
                    if _is_worktree_gitdir(gitdir):
                        # Navigate: .git/worktrees/name -> .git -> main repo root
                        main_git_dir = gitdir.parent.parent
                        main_repo = main_git_dir.parent
                        if main_repo.exists() and (main_repo / KITTIFY_DIR).is_dir():
                            return main_repo
            except (OSError, ValueError):
                # If we can't read or parse the .git file, continue searching
                pass

        elif git_path.is_dir():
            # This is the main repo (or a regular git repo)
            if (candidate / KITTIFY_DIR).is_dir():
                return candidate

        # Also check for .kittify marker (fallback for non-git scenarios)
        kittify_path = candidate / KITTIFY_DIR
        if kittify_path.is_symlink() and not kittify_path.exists():
            # Broken symlink - skip this candidate
            continue
        if kittify_path.is_dir():
            return candidate

    return None


def x_locate_project_root__mutmut_22(start: Path | None = None) -> Optional[Path]:
    """
    Locate the MAIN spec-kitty project root directory, even from within worktrees.

    This function correctly handles git worktrees by detecting when .git is a
    file (worktree pointer) vs a directory (main repo), and following the
    pointer back to the main repository.

    Resolution order:
    1. SPECIFY_REPO_ROOT environment variable (highest priority)
    2. Walk up directory tree, detecting worktree .git files and following to main repo
    3. Fall back to .kittify/ marker search

    Args:
        start: Starting directory for search (defaults to current working directory)

    Returns:
        Path to MAIN project root (not worktree), or None if not found

    Examples:
        >>> # From main repo
        >>> root = locate_project_root()
        >>> assert (root / ".kittify").exists()

        >>> # From worktree - returns MAIN repo, not worktree
        >>> root = locate_project_root(Path(".worktrees/my-feature"))
        >>> assert ".worktrees" not in str(root)
    """
    # Tier 1: Check environment variable (allows override for CI/CD)
    if env_root := os.getenv("SPECIFY_REPO_ROOT"):
        env_path = Path(env_root).resolve()
        if env_path.exists() and (env_path / KITTIFY_DIR).is_dir():
            return env_path
        # Invalid env var - fall through to other methods

    # Tier 2: Walk up directory tree, handling worktree .git files
    current = (start or Path.cwd()).resolve()

    for candidate in [current, *current.parents]:
        git_path = candidate / ".git"

        if git_path.is_file():
            # .git files with gitdir: pointers appear in worktrees,
            # submodules, and separate-git-dir clones.  Only follow the
            # pointer when it has the .git/worktrees/<name> topology.
            try:
                content = git_path.read_text().strip()
                if content.startswith("gitdir:"):
                    gitdir = Path(content.split(1)[1].strip())
                    if _is_worktree_gitdir(gitdir):
                        # Navigate: .git/worktrees/name -> .git -> main repo root
                        main_git_dir = gitdir.parent.parent
                        main_repo = main_git_dir.parent
                        if main_repo.exists() and (main_repo / KITTIFY_DIR).is_dir():
                            return main_repo
            except (OSError, ValueError):
                # If we can't read or parse the .git file, continue searching
                pass

        elif git_path.is_dir():
            # This is the main repo (or a regular git repo)
            if (candidate / KITTIFY_DIR).is_dir():
                return candidate

        # Also check for .kittify marker (fallback for non-git scenarios)
        kittify_path = candidate / KITTIFY_DIR
        if kittify_path.is_symlink() and not kittify_path.exists():
            # Broken symlink - skip this candidate
            continue
        if kittify_path.is_dir():
            return candidate

    return None


def x_locate_project_root__mutmut_23(start: Path | None = None) -> Optional[Path]:
    """
    Locate the MAIN spec-kitty project root directory, even from within worktrees.

    This function correctly handles git worktrees by detecting when .git is a
    file (worktree pointer) vs a directory (main repo), and following the
    pointer back to the main repository.

    Resolution order:
    1. SPECIFY_REPO_ROOT environment variable (highest priority)
    2. Walk up directory tree, detecting worktree .git files and following to main repo
    3. Fall back to .kittify/ marker search

    Args:
        start: Starting directory for search (defaults to current working directory)

    Returns:
        Path to MAIN project root (not worktree), or None if not found

    Examples:
        >>> # From main repo
        >>> root = locate_project_root()
        >>> assert (root / ".kittify").exists()

        >>> # From worktree - returns MAIN repo, not worktree
        >>> root = locate_project_root(Path(".worktrees/my-feature"))
        >>> assert ".worktrees" not in str(root)
    """
    # Tier 1: Check environment variable (allows override for CI/CD)
    if env_root := os.getenv("SPECIFY_REPO_ROOT"):
        env_path = Path(env_root).resolve()
        if env_path.exists() and (env_path / KITTIFY_DIR).is_dir():
            return env_path
        # Invalid env var - fall through to other methods

    # Tier 2: Walk up directory tree, handling worktree .git files
    current = (start or Path.cwd()).resolve()

    for candidate in [current, *current.parents]:
        git_path = candidate / ".git"

        if git_path.is_file():
            # .git files with gitdir: pointers appear in worktrees,
            # submodules, and separate-git-dir clones.  Only follow the
            # pointer when it has the .git/worktrees/<name> topology.
            try:
                content = git_path.read_text().strip()
                if content.startswith("gitdir:"):
                    gitdir = Path(content.split(":", )[1].strip())
                    if _is_worktree_gitdir(gitdir):
                        # Navigate: .git/worktrees/name -> .git -> main repo root
                        main_git_dir = gitdir.parent.parent
                        main_repo = main_git_dir.parent
                        if main_repo.exists() and (main_repo / KITTIFY_DIR).is_dir():
                            return main_repo
            except (OSError, ValueError):
                # If we can't read or parse the .git file, continue searching
                pass

        elif git_path.is_dir():
            # This is the main repo (or a regular git repo)
            if (candidate / KITTIFY_DIR).is_dir():
                return candidate

        # Also check for .kittify marker (fallback for non-git scenarios)
        kittify_path = candidate / KITTIFY_DIR
        if kittify_path.is_symlink() and not kittify_path.exists():
            # Broken symlink - skip this candidate
            continue
        if kittify_path.is_dir():
            return candidate

    return None


def x_locate_project_root__mutmut_24(start: Path | None = None) -> Optional[Path]:
    """
    Locate the MAIN spec-kitty project root directory, even from within worktrees.

    This function correctly handles git worktrees by detecting when .git is a
    file (worktree pointer) vs a directory (main repo), and following the
    pointer back to the main repository.

    Resolution order:
    1. SPECIFY_REPO_ROOT environment variable (highest priority)
    2. Walk up directory tree, detecting worktree .git files and following to main repo
    3. Fall back to .kittify/ marker search

    Args:
        start: Starting directory for search (defaults to current working directory)

    Returns:
        Path to MAIN project root (not worktree), or None if not found

    Examples:
        >>> # From main repo
        >>> root = locate_project_root()
        >>> assert (root / ".kittify").exists()

        >>> # From worktree - returns MAIN repo, not worktree
        >>> root = locate_project_root(Path(".worktrees/my-feature"))
        >>> assert ".worktrees" not in str(root)
    """
    # Tier 1: Check environment variable (allows override for CI/CD)
    if env_root := os.getenv("SPECIFY_REPO_ROOT"):
        env_path = Path(env_root).resolve()
        if env_path.exists() and (env_path / KITTIFY_DIR).is_dir():
            return env_path
        # Invalid env var - fall through to other methods

    # Tier 2: Walk up directory tree, handling worktree .git files
    current = (start or Path.cwd()).resolve()

    for candidate in [current, *current.parents]:
        git_path = candidate / ".git"

        if git_path.is_file():
            # .git files with gitdir: pointers appear in worktrees,
            # submodules, and separate-git-dir clones.  Only follow the
            # pointer when it has the .git/worktrees/<name> topology.
            try:
                content = git_path.read_text().strip()
                if content.startswith("gitdir:"):
                    gitdir = Path(content.rsplit(":", 1)[1].strip())
                    if _is_worktree_gitdir(gitdir):
                        # Navigate: .git/worktrees/name -> .git -> main repo root
                        main_git_dir = gitdir.parent.parent
                        main_repo = main_git_dir.parent
                        if main_repo.exists() and (main_repo / KITTIFY_DIR).is_dir():
                            return main_repo
            except (OSError, ValueError):
                # If we can't read or parse the .git file, continue searching
                pass

        elif git_path.is_dir():
            # This is the main repo (or a regular git repo)
            if (candidate / KITTIFY_DIR).is_dir():
                return candidate

        # Also check for .kittify marker (fallback for non-git scenarios)
        kittify_path = candidate / KITTIFY_DIR
        if kittify_path.is_symlink() and not kittify_path.exists():
            # Broken symlink - skip this candidate
            continue
        if kittify_path.is_dir():
            return candidate

    return None


def x_locate_project_root__mutmut_25(start: Path | None = None) -> Optional[Path]:
    """
    Locate the MAIN spec-kitty project root directory, even from within worktrees.

    This function correctly handles git worktrees by detecting when .git is a
    file (worktree pointer) vs a directory (main repo), and following the
    pointer back to the main repository.

    Resolution order:
    1. SPECIFY_REPO_ROOT environment variable (highest priority)
    2. Walk up directory tree, detecting worktree .git files and following to main repo
    3. Fall back to .kittify/ marker search

    Args:
        start: Starting directory for search (defaults to current working directory)

    Returns:
        Path to MAIN project root (not worktree), or None if not found

    Examples:
        >>> # From main repo
        >>> root = locate_project_root()
        >>> assert (root / ".kittify").exists()

        >>> # From worktree - returns MAIN repo, not worktree
        >>> root = locate_project_root(Path(".worktrees/my-feature"))
        >>> assert ".worktrees" not in str(root)
    """
    # Tier 1: Check environment variable (allows override for CI/CD)
    if env_root := os.getenv("SPECIFY_REPO_ROOT"):
        env_path = Path(env_root).resolve()
        if env_path.exists() and (env_path / KITTIFY_DIR).is_dir():
            return env_path
        # Invalid env var - fall through to other methods

    # Tier 2: Walk up directory tree, handling worktree .git files
    current = (start or Path.cwd()).resolve()

    for candidate in [current, *current.parents]:
        git_path = candidate / ".git"

        if git_path.is_file():
            # .git files with gitdir: pointers appear in worktrees,
            # submodules, and separate-git-dir clones.  Only follow the
            # pointer when it has the .git/worktrees/<name> topology.
            try:
                content = git_path.read_text().strip()
                if content.startswith("gitdir:"):
                    gitdir = Path(content.split("XX:XX", 1)[1].strip())
                    if _is_worktree_gitdir(gitdir):
                        # Navigate: .git/worktrees/name -> .git -> main repo root
                        main_git_dir = gitdir.parent.parent
                        main_repo = main_git_dir.parent
                        if main_repo.exists() and (main_repo / KITTIFY_DIR).is_dir():
                            return main_repo
            except (OSError, ValueError):
                # If we can't read or parse the .git file, continue searching
                pass

        elif git_path.is_dir():
            # This is the main repo (or a regular git repo)
            if (candidate / KITTIFY_DIR).is_dir():
                return candidate

        # Also check for .kittify marker (fallback for non-git scenarios)
        kittify_path = candidate / KITTIFY_DIR
        if kittify_path.is_symlink() and not kittify_path.exists():
            # Broken symlink - skip this candidate
            continue
        if kittify_path.is_dir():
            return candidate

    return None


def x_locate_project_root__mutmut_26(start: Path | None = None) -> Optional[Path]:
    """
    Locate the MAIN spec-kitty project root directory, even from within worktrees.

    This function correctly handles git worktrees by detecting when .git is a
    file (worktree pointer) vs a directory (main repo), and following the
    pointer back to the main repository.

    Resolution order:
    1. SPECIFY_REPO_ROOT environment variable (highest priority)
    2. Walk up directory tree, detecting worktree .git files and following to main repo
    3. Fall back to .kittify/ marker search

    Args:
        start: Starting directory for search (defaults to current working directory)

    Returns:
        Path to MAIN project root (not worktree), or None if not found

    Examples:
        >>> # From main repo
        >>> root = locate_project_root()
        >>> assert (root / ".kittify").exists()

        >>> # From worktree - returns MAIN repo, not worktree
        >>> root = locate_project_root(Path(".worktrees/my-feature"))
        >>> assert ".worktrees" not in str(root)
    """
    # Tier 1: Check environment variable (allows override for CI/CD)
    if env_root := os.getenv("SPECIFY_REPO_ROOT"):
        env_path = Path(env_root).resolve()
        if env_path.exists() and (env_path / KITTIFY_DIR).is_dir():
            return env_path
        # Invalid env var - fall through to other methods

    # Tier 2: Walk up directory tree, handling worktree .git files
    current = (start or Path.cwd()).resolve()

    for candidate in [current, *current.parents]:
        git_path = candidate / ".git"

        if git_path.is_file():
            # .git files with gitdir: pointers appear in worktrees,
            # submodules, and separate-git-dir clones.  Only follow the
            # pointer when it has the .git/worktrees/<name> topology.
            try:
                content = git_path.read_text().strip()
                if content.startswith("gitdir:"):
                    gitdir = Path(content.split(":", 2)[1].strip())
                    if _is_worktree_gitdir(gitdir):
                        # Navigate: .git/worktrees/name -> .git -> main repo root
                        main_git_dir = gitdir.parent.parent
                        main_repo = main_git_dir.parent
                        if main_repo.exists() and (main_repo / KITTIFY_DIR).is_dir():
                            return main_repo
            except (OSError, ValueError):
                # If we can't read or parse the .git file, continue searching
                pass

        elif git_path.is_dir():
            # This is the main repo (or a regular git repo)
            if (candidate / KITTIFY_DIR).is_dir():
                return candidate

        # Also check for .kittify marker (fallback for non-git scenarios)
        kittify_path = candidate / KITTIFY_DIR
        if kittify_path.is_symlink() and not kittify_path.exists():
            # Broken symlink - skip this candidate
            continue
        if kittify_path.is_dir():
            return candidate

    return None


def x_locate_project_root__mutmut_27(start: Path | None = None) -> Optional[Path]:
    """
    Locate the MAIN spec-kitty project root directory, even from within worktrees.

    This function correctly handles git worktrees by detecting when .git is a
    file (worktree pointer) vs a directory (main repo), and following the
    pointer back to the main repository.

    Resolution order:
    1. SPECIFY_REPO_ROOT environment variable (highest priority)
    2. Walk up directory tree, detecting worktree .git files and following to main repo
    3. Fall back to .kittify/ marker search

    Args:
        start: Starting directory for search (defaults to current working directory)

    Returns:
        Path to MAIN project root (not worktree), or None if not found

    Examples:
        >>> # From main repo
        >>> root = locate_project_root()
        >>> assert (root / ".kittify").exists()

        >>> # From worktree - returns MAIN repo, not worktree
        >>> root = locate_project_root(Path(".worktrees/my-feature"))
        >>> assert ".worktrees" not in str(root)
    """
    # Tier 1: Check environment variable (allows override for CI/CD)
    if env_root := os.getenv("SPECIFY_REPO_ROOT"):
        env_path = Path(env_root).resolve()
        if env_path.exists() and (env_path / KITTIFY_DIR).is_dir():
            return env_path
        # Invalid env var - fall through to other methods

    # Tier 2: Walk up directory tree, handling worktree .git files
    current = (start or Path.cwd()).resolve()

    for candidate in [current, *current.parents]:
        git_path = candidate / ".git"

        if git_path.is_file():
            # .git files with gitdir: pointers appear in worktrees,
            # submodules, and separate-git-dir clones.  Only follow the
            # pointer when it has the .git/worktrees/<name> topology.
            try:
                content = git_path.read_text().strip()
                if content.startswith("gitdir:"):
                    gitdir = Path(content.split(":", 1)[2].strip())
                    if _is_worktree_gitdir(gitdir):
                        # Navigate: .git/worktrees/name -> .git -> main repo root
                        main_git_dir = gitdir.parent.parent
                        main_repo = main_git_dir.parent
                        if main_repo.exists() and (main_repo / KITTIFY_DIR).is_dir():
                            return main_repo
            except (OSError, ValueError):
                # If we can't read or parse the .git file, continue searching
                pass

        elif git_path.is_dir():
            # This is the main repo (or a regular git repo)
            if (candidate / KITTIFY_DIR).is_dir():
                return candidate

        # Also check for .kittify marker (fallback for non-git scenarios)
        kittify_path = candidate / KITTIFY_DIR
        if kittify_path.is_symlink() and not kittify_path.exists():
            # Broken symlink - skip this candidate
            continue
        if kittify_path.is_dir():
            return candidate

    return None


def x_locate_project_root__mutmut_28(start: Path | None = None) -> Optional[Path]:
    """
    Locate the MAIN spec-kitty project root directory, even from within worktrees.

    This function correctly handles git worktrees by detecting when .git is a
    file (worktree pointer) vs a directory (main repo), and following the
    pointer back to the main repository.

    Resolution order:
    1. SPECIFY_REPO_ROOT environment variable (highest priority)
    2. Walk up directory tree, detecting worktree .git files and following to main repo
    3. Fall back to .kittify/ marker search

    Args:
        start: Starting directory for search (defaults to current working directory)

    Returns:
        Path to MAIN project root (not worktree), or None if not found

    Examples:
        >>> # From main repo
        >>> root = locate_project_root()
        >>> assert (root / ".kittify").exists()

        >>> # From worktree - returns MAIN repo, not worktree
        >>> root = locate_project_root(Path(".worktrees/my-feature"))
        >>> assert ".worktrees" not in str(root)
    """
    # Tier 1: Check environment variable (allows override for CI/CD)
    if env_root := os.getenv("SPECIFY_REPO_ROOT"):
        env_path = Path(env_root).resolve()
        if env_path.exists() and (env_path / KITTIFY_DIR).is_dir():
            return env_path
        # Invalid env var - fall through to other methods

    # Tier 2: Walk up directory tree, handling worktree .git files
    current = (start or Path.cwd()).resolve()

    for candidate in [current, *current.parents]:
        git_path = candidate / ".git"

        if git_path.is_file():
            # .git files with gitdir: pointers appear in worktrees,
            # submodules, and separate-git-dir clones.  Only follow the
            # pointer when it has the .git/worktrees/<name> topology.
            try:
                content = git_path.read_text().strip()
                if content.startswith("gitdir:"):
                    gitdir = Path(content.split(":", 1)[1].strip())
                    if _is_worktree_gitdir(None):
                        # Navigate: .git/worktrees/name -> .git -> main repo root
                        main_git_dir = gitdir.parent.parent
                        main_repo = main_git_dir.parent
                        if main_repo.exists() and (main_repo / KITTIFY_DIR).is_dir():
                            return main_repo
            except (OSError, ValueError):
                # If we can't read or parse the .git file, continue searching
                pass

        elif git_path.is_dir():
            # This is the main repo (or a regular git repo)
            if (candidate / KITTIFY_DIR).is_dir():
                return candidate

        # Also check for .kittify marker (fallback for non-git scenarios)
        kittify_path = candidate / KITTIFY_DIR
        if kittify_path.is_symlink() and not kittify_path.exists():
            # Broken symlink - skip this candidate
            continue
        if kittify_path.is_dir():
            return candidate

    return None


def x_locate_project_root__mutmut_29(start: Path | None = None) -> Optional[Path]:
    """
    Locate the MAIN spec-kitty project root directory, even from within worktrees.

    This function correctly handles git worktrees by detecting when .git is a
    file (worktree pointer) vs a directory (main repo), and following the
    pointer back to the main repository.

    Resolution order:
    1. SPECIFY_REPO_ROOT environment variable (highest priority)
    2. Walk up directory tree, detecting worktree .git files and following to main repo
    3. Fall back to .kittify/ marker search

    Args:
        start: Starting directory for search (defaults to current working directory)

    Returns:
        Path to MAIN project root (not worktree), or None if not found

    Examples:
        >>> # From main repo
        >>> root = locate_project_root()
        >>> assert (root / ".kittify").exists()

        >>> # From worktree - returns MAIN repo, not worktree
        >>> root = locate_project_root(Path(".worktrees/my-feature"))
        >>> assert ".worktrees" not in str(root)
    """
    # Tier 1: Check environment variable (allows override for CI/CD)
    if env_root := os.getenv("SPECIFY_REPO_ROOT"):
        env_path = Path(env_root).resolve()
        if env_path.exists() and (env_path / KITTIFY_DIR).is_dir():
            return env_path
        # Invalid env var - fall through to other methods

    # Tier 2: Walk up directory tree, handling worktree .git files
    current = (start or Path.cwd()).resolve()

    for candidate in [current, *current.parents]:
        git_path = candidate / ".git"

        if git_path.is_file():
            # .git files with gitdir: pointers appear in worktrees,
            # submodules, and separate-git-dir clones.  Only follow the
            # pointer when it has the .git/worktrees/<name> topology.
            try:
                content = git_path.read_text().strip()
                if content.startswith("gitdir:"):
                    gitdir = Path(content.split(":", 1)[1].strip())
                    if _is_worktree_gitdir(gitdir):
                        # Navigate: .git/worktrees/name -> .git -> main repo root
                        main_git_dir = None
                        main_repo = main_git_dir.parent
                        if main_repo.exists() and (main_repo / KITTIFY_DIR).is_dir():
                            return main_repo
            except (OSError, ValueError):
                # If we can't read or parse the .git file, continue searching
                pass

        elif git_path.is_dir():
            # This is the main repo (or a regular git repo)
            if (candidate / KITTIFY_DIR).is_dir():
                return candidate

        # Also check for .kittify marker (fallback for non-git scenarios)
        kittify_path = candidate / KITTIFY_DIR
        if kittify_path.is_symlink() and not kittify_path.exists():
            # Broken symlink - skip this candidate
            continue
        if kittify_path.is_dir():
            return candidate

    return None


def x_locate_project_root__mutmut_30(start: Path | None = None) -> Optional[Path]:
    """
    Locate the MAIN spec-kitty project root directory, even from within worktrees.

    This function correctly handles git worktrees by detecting when .git is a
    file (worktree pointer) vs a directory (main repo), and following the
    pointer back to the main repository.

    Resolution order:
    1. SPECIFY_REPO_ROOT environment variable (highest priority)
    2. Walk up directory tree, detecting worktree .git files and following to main repo
    3. Fall back to .kittify/ marker search

    Args:
        start: Starting directory for search (defaults to current working directory)

    Returns:
        Path to MAIN project root (not worktree), or None if not found

    Examples:
        >>> # From main repo
        >>> root = locate_project_root()
        >>> assert (root / ".kittify").exists()

        >>> # From worktree - returns MAIN repo, not worktree
        >>> root = locate_project_root(Path(".worktrees/my-feature"))
        >>> assert ".worktrees" not in str(root)
    """
    # Tier 1: Check environment variable (allows override for CI/CD)
    if env_root := os.getenv("SPECIFY_REPO_ROOT"):
        env_path = Path(env_root).resolve()
        if env_path.exists() and (env_path / KITTIFY_DIR).is_dir():
            return env_path
        # Invalid env var - fall through to other methods

    # Tier 2: Walk up directory tree, handling worktree .git files
    current = (start or Path.cwd()).resolve()

    for candidate in [current, *current.parents]:
        git_path = candidate / ".git"

        if git_path.is_file():
            # .git files with gitdir: pointers appear in worktrees,
            # submodules, and separate-git-dir clones.  Only follow the
            # pointer when it has the .git/worktrees/<name> topology.
            try:
                content = git_path.read_text().strip()
                if content.startswith("gitdir:"):
                    gitdir = Path(content.split(":", 1)[1].strip())
                    if _is_worktree_gitdir(gitdir):
                        # Navigate: .git/worktrees/name -> .git -> main repo root
                        main_git_dir = gitdir.parent.parent
                        main_repo = None
                        if main_repo.exists() and (main_repo / KITTIFY_DIR).is_dir():
                            return main_repo
            except (OSError, ValueError):
                # If we can't read or parse the .git file, continue searching
                pass

        elif git_path.is_dir():
            # This is the main repo (or a regular git repo)
            if (candidate / KITTIFY_DIR).is_dir():
                return candidate

        # Also check for .kittify marker (fallback for non-git scenarios)
        kittify_path = candidate / KITTIFY_DIR
        if kittify_path.is_symlink() and not kittify_path.exists():
            # Broken symlink - skip this candidate
            continue
        if kittify_path.is_dir():
            return candidate

    return None


def x_locate_project_root__mutmut_31(start: Path | None = None) -> Optional[Path]:
    """
    Locate the MAIN spec-kitty project root directory, even from within worktrees.

    This function correctly handles git worktrees by detecting when .git is a
    file (worktree pointer) vs a directory (main repo), and following the
    pointer back to the main repository.

    Resolution order:
    1. SPECIFY_REPO_ROOT environment variable (highest priority)
    2. Walk up directory tree, detecting worktree .git files and following to main repo
    3. Fall back to .kittify/ marker search

    Args:
        start: Starting directory for search (defaults to current working directory)

    Returns:
        Path to MAIN project root (not worktree), or None if not found

    Examples:
        >>> # From main repo
        >>> root = locate_project_root()
        >>> assert (root / ".kittify").exists()

        >>> # From worktree - returns MAIN repo, not worktree
        >>> root = locate_project_root(Path(".worktrees/my-feature"))
        >>> assert ".worktrees" not in str(root)
    """
    # Tier 1: Check environment variable (allows override for CI/CD)
    if env_root := os.getenv("SPECIFY_REPO_ROOT"):
        env_path = Path(env_root).resolve()
        if env_path.exists() and (env_path / KITTIFY_DIR).is_dir():
            return env_path
        # Invalid env var - fall through to other methods

    # Tier 2: Walk up directory tree, handling worktree .git files
    current = (start or Path.cwd()).resolve()

    for candidate in [current, *current.parents]:
        git_path = candidate / ".git"

        if git_path.is_file():
            # .git files with gitdir: pointers appear in worktrees,
            # submodules, and separate-git-dir clones.  Only follow the
            # pointer when it has the .git/worktrees/<name> topology.
            try:
                content = git_path.read_text().strip()
                if content.startswith("gitdir:"):
                    gitdir = Path(content.split(":", 1)[1].strip())
                    if _is_worktree_gitdir(gitdir):
                        # Navigate: .git/worktrees/name -> .git -> main repo root
                        main_git_dir = gitdir.parent.parent
                        main_repo = main_git_dir.parent
                        if main_repo.exists() or (main_repo / KITTIFY_DIR).is_dir():
                            return main_repo
            except (OSError, ValueError):
                # If we can't read or parse the .git file, continue searching
                pass

        elif git_path.is_dir():
            # This is the main repo (or a regular git repo)
            if (candidate / KITTIFY_DIR).is_dir():
                return candidate

        # Also check for .kittify marker (fallback for non-git scenarios)
        kittify_path = candidate / KITTIFY_DIR
        if kittify_path.is_symlink() and not kittify_path.exists():
            # Broken symlink - skip this candidate
            continue
        if kittify_path.is_dir():
            return candidate

    return None


def x_locate_project_root__mutmut_32(start: Path | None = None) -> Optional[Path]:
    """
    Locate the MAIN spec-kitty project root directory, even from within worktrees.

    This function correctly handles git worktrees by detecting when .git is a
    file (worktree pointer) vs a directory (main repo), and following the
    pointer back to the main repository.

    Resolution order:
    1. SPECIFY_REPO_ROOT environment variable (highest priority)
    2. Walk up directory tree, detecting worktree .git files and following to main repo
    3. Fall back to .kittify/ marker search

    Args:
        start: Starting directory for search (defaults to current working directory)

    Returns:
        Path to MAIN project root (not worktree), or None if not found

    Examples:
        >>> # From main repo
        >>> root = locate_project_root()
        >>> assert (root / ".kittify").exists()

        >>> # From worktree - returns MAIN repo, not worktree
        >>> root = locate_project_root(Path(".worktrees/my-feature"))
        >>> assert ".worktrees" not in str(root)
    """
    # Tier 1: Check environment variable (allows override for CI/CD)
    if env_root := os.getenv("SPECIFY_REPO_ROOT"):
        env_path = Path(env_root).resolve()
        if env_path.exists() and (env_path / KITTIFY_DIR).is_dir():
            return env_path
        # Invalid env var - fall through to other methods

    # Tier 2: Walk up directory tree, handling worktree .git files
    current = (start or Path.cwd()).resolve()

    for candidate in [current, *current.parents]:
        git_path = candidate / ".git"

        if git_path.is_file():
            # .git files with gitdir: pointers appear in worktrees,
            # submodules, and separate-git-dir clones.  Only follow the
            # pointer when it has the .git/worktrees/<name> topology.
            try:
                content = git_path.read_text().strip()
                if content.startswith("gitdir:"):
                    gitdir = Path(content.split(":", 1)[1].strip())
                    if _is_worktree_gitdir(gitdir):
                        # Navigate: .git/worktrees/name -> .git -> main repo root
                        main_git_dir = gitdir.parent.parent
                        main_repo = main_git_dir.parent
                        if main_repo.exists() and (main_repo * KITTIFY_DIR).is_dir():
                            return main_repo
            except (OSError, ValueError):
                # If we can't read or parse the .git file, continue searching
                pass

        elif git_path.is_dir():
            # This is the main repo (or a regular git repo)
            if (candidate / KITTIFY_DIR).is_dir():
                return candidate

        # Also check for .kittify marker (fallback for non-git scenarios)
        kittify_path = candidate / KITTIFY_DIR
        if kittify_path.is_symlink() and not kittify_path.exists():
            # Broken symlink - skip this candidate
            continue
        if kittify_path.is_dir():
            return candidate

    return None


def x_locate_project_root__mutmut_33(start: Path | None = None) -> Optional[Path]:
    """
    Locate the MAIN spec-kitty project root directory, even from within worktrees.

    This function correctly handles git worktrees by detecting when .git is a
    file (worktree pointer) vs a directory (main repo), and following the
    pointer back to the main repository.

    Resolution order:
    1. SPECIFY_REPO_ROOT environment variable (highest priority)
    2. Walk up directory tree, detecting worktree .git files and following to main repo
    3. Fall back to .kittify/ marker search

    Args:
        start: Starting directory for search (defaults to current working directory)

    Returns:
        Path to MAIN project root (not worktree), or None if not found

    Examples:
        >>> # From main repo
        >>> root = locate_project_root()
        >>> assert (root / ".kittify").exists()

        >>> # From worktree - returns MAIN repo, not worktree
        >>> root = locate_project_root(Path(".worktrees/my-feature"))
        >>> assert ".worktrees" not in str(root)
    """
    # Tier 1: Check environment variable (allows override for CI/CD)
    if env_root := os.getenv("SPECIFY_REPO_ROOT"):
        env_path = Path(env_root).resolve()
        if env_path.exists() and (env_path / KITTIFY_DIR).is_dir():
            return env_path
        # Invalid env var - fall through to other methods

    # Tier 2: Walk up directory tree, handling worktree .git files
    current = (start or Path.cwd()).resolve()

    for candidate in [current, *current.parents]:
        git_path = candidate / ".git"

        if git_path.is_file():
            # .git files with gitdir: pointers appear in worktrees,
            # submodules, and separate-git-dir clones.  Only follow the
            # pointer when it has the .git/worktrees/<name> topology.
            try:
                content = git_path.read_text().strip()
                if content.startswith("gitdir:"):
                    gitdir = Path(content.split(":", 1)[1].strip())
                    if _is_worktree_gitdir(gitdir):
                        # Navigate: .git/worktrees/name -> .git -> main repo root
                        main_git_dir = gitdir.parent.parent
                        main_repo = main_git_dir.parent
                        if main_repo.exists() and (main_repo / KITTIFY_DIR).is_dir():
                            return main_repo
            except (OSError, ValueError):
                # If we can't read or parse the .git file, continue searching
                pass

        elif git_path.is_dir():
            # This is the main repo (or a regular git repo)
            if (candidate * KITTIFY_DIR).is_dir():
                return candidate

        # Also check for .kittify marker (fallback for non-git scenarios)
        kittify_path = candidate / KITTIFY_DIR
        if kittify_path.is_symlink() and not kittify_path.exists():
            # Broken symlink - skip this candidate
            continue
        if kittify_path.is_dir():
            return candidate

    return None


def x_locate_project_root__mutmut_34(start: Path | None = None) -> Optional[Path]:
    """
    Locate the MAIN spec-kitty project root directory, even from within worktrees.

    This function correctly handles git worktrees by detecting when .git is a
    file (worktree pointer) vs a directory (main repo), and following the
    pointer back to the main repository.

    Resolution order:
    1. SPECIFY_REPO_ROOT environment variable (highest priority)
    2. Walk up directory tree, detecting worktree .git files and following to main repo
    3. Fall back to .kittify/ marker search

    Args:
        start: Starting directory for search (defaults to current working directory)

    Returns:
        Path to MAIN project root (not worktree), or None if not found

    Examples:
        >>> # From main repo
        >>> root = locate_project_root()
        >>> assert (root / ".kittify").exists()

        >>> # From worktree - returns MAIN repo, not worktree
        >>> root = locate_project_root(Path(".worktrees/my-feature"))
        >>> assert ".worktrees" not in str(root)
    """
    # Tier 1: Check environment variable (allows override for CI/CD)
    if env_root := os.getenv("SPECIFY_REPO_ROOT"):
        env_path = Path(env_root).resolve()
        if env_path.exists() and (env_path / KITTIFY_DIR).is_dir():
            return env_path
        # Invalid env var - fall through to other methods

    # Tier 2: Walk up directory tree, handling worktree .git files
    current = (start or Path.cwd()).resolve()

    for candidate in [current, *current.parents]:
        git_path = candidate / ".git"

        if git_path.is_file():
            # .git files with gitdir: pointers appear in worktrees,
            # submodules, and separate-git-dir clones.  Only follow the
            # pointer when it has the .git/worktrees/<name> topology.
            try:
                content = git_path.read_text().strip()
                if content.startswith("gitdir:"):
                    gitdir = Path(content.split(":", 1)[1].strip())
                    if _is_worktree_gitdir(gitdir):
                        # Navigate: .git/worktrees/name -> .git -> main repo root
                        main_git_dir = gitdir.parent.parent
                        main_repo = main_git_dir.parent
                        if main_repo.exists() and (main_repo / KITTIFY_DIR).is_dir():
                            return main_repo
            except (OSError, ValueError):
                # If we can't read or parse the .git file, continue searching
                pass

        elif git_path.is_dir():
            # This is the main repo (or a regular git repo)
            if (candidate / KITTIFY_DIR).is_dir():
                return candidate

        # Also check for .kittify marker (fallback for non-git scenarios)
        kittify_path = None
        if kittify_path.is_symlink() and not kittify_path.exists():
            # Broken symlink - skip this candidate
            continue
        if kittify_path.is_dir():
            return candidate

    return None


def x_locate_project_root__mutmut_35(start: Path | None = None) -> Optional[Path]:
    """
    Locate the MAIN spec-kitty project root directory, even from within worktrees.

    This function correctly handles git worktrees by detecting when .git is a
    file (worktree pointer) vs a directory (main repo), and following the
    pointer back to the main repository.

    Resolution order:
    1. SPECIFY_REPO_ROOT environment variable (highest priority)
    2. Walk up directory tree, detecting worktree .git files and following to main repo
    3. Fall back to .kittify/ marker search

    Args:
        start: Starting directory for search (defaults to current working directory)

    Returns:
        Path to MAIN project root (not worktree), or None if not found

    Examples:
        >>> # From main repo
        >>> root = locate_project_root()
        >>> assert (root / ".kittify").exists()

        >>> # From worktree - returns MAIN repo, not worktree
        >>> root = locate_project_root(Path(".worktrees/my-feature"))
        >>> assert ".worktrees" not in str(root)
    """
    # Tier 1: Check environment variable (allows override for CI/CD)
    if env_root := os.getenv("SPECIFY_REPO_ROOT"):
        env_path = Path(env_root).resolve()
        if env_path.exists() and (env_path / KITTIFY_DIR).is_dir():
            return env_path
        # Invalid env var - fall through to other methods

    # Tier 2: Walk up directory tree, handling worktree .git files
    current = (start or Path.cwd()).resolve()

    for candidate in [current, *current.parents]:
        git_path = candidate / ".git"

        if git_path.is_file():
            # .git files with gitdir: pointers appear in worktrees,
            # submodules, and separate-git-dir clones.  Only follow the
            # pointer when it has the .git/worktrees/<name> topology.
            try:
                content = git_path.read_text().strip()
                if content.startswith("gitdir:"):
                    gitdir = Path(content.split(":", 1)[1].strip())
                    if _is_worktree_gitdir(gitdir):
                        # Navigate: .git/worktrees/name -> .git -> main repo root
                        main_git_dir = gitdir.parent.parent
                        main_repo = main_git_dir.parent
                        if main_repo.exists() and (main_repo / KITTIFY_DIR).is_dir():
                            return main_repo
            except (OSError, ValueError):
                # If we can't read or parse the .git file, continue searching
                pass

        elif git_path.is_dir():
            # This is the main repo (or a regular git repo)
            if (candidate / KITTIFY_DIR).is_dir():
                return candidate

        # Also check for .kittify marker (fallback for non-git scenarios)
        kittify_path = candidate * KITTIFY_DIR
        if kittify_path.is_symlink() and not kittify_path.exists():
            # Broken symlink - skip this candidate
            continue
        if kittify_path.is_dir():
            return candidate

    return None


def x_locate_project_root__mutmut_36(start: Path | None = None) -> Optional[Path]:
    """
    Locate the MAIN spec-kitty project root directory, even from within worktrees.

    This function correctly handles git worktrees by detecting when .git is a
    file (worktree pointer) vs a directory (main repo), and following the
    pointer back to the main repository.

    Resolution order:
    1. SPECIFY_REPO_ROOT environment variable (highest priority)
    2. Walk up directory tree, detecting worktree .git files and following to main repo
    3. Fall back to .kittify/ marker search

    Args:
        start: Starting directory for search (defaults to current working directory)

    Returns:
        Path to MAIN project root (not worktree), or None if not found

    Examples:
        >>> # From main repo
        >>> root = locate_project_root()
        >>> assert (root / ".kittify").exists()

        >>> # From worktree - returns MAIN repo, not worktree
        >>> root = locate_project_root(Path(".worktrees/my-feature"))
        >>> assert ".worktrees" not in str(root)
    """
    # Tier 1: Check environment variable (allows override for CI/CD)
    if env_root := os.getenv("SPECIFY_REPO_ROOT"):
        env_path = Path(env_root).resolve()
        if env_path.exists() and (env_path / KITTIFY_DIR).is_dir():
            return env_path
        # Invalid env var - fall through to other methods

    # Tier 2: Walk up directory tree, handling worktree .git files
    current = (start or Path.cwd()).resolve()

    for candidate in [current, *current.parents]:
        git_path = candidate / ".git"

        if git_path.is_file():
            # .git files with gitdir: pointers appear in worktrees,
            # submodules, and separate-git-dir clones.  Only follow the
            # pointer when it has the .git/worktrees/<name> topology.
            try:
                content = git_path.read_text().strip()
                if content.startswith("gitdir:"):
                    gitdir = Path(content.split(":", 1)[1].strip())
                    if _is_worktree_gitdir(gitdir):
                        # Navigate: .git/worktrees/name -> .git -> main repo root
                        main_git_dir = gitdir.parent.parent
                        main_repo = main_git_dir.parent
                        if main_repo.exists() and (main_repo / KITTIFY_DIR).is_dir():
                            return main_repo
            except (OSError, ValueError):
                # If we can't read or parse the .git file, continue searching
                pass

        elif git_path.is_dir():
            # This is the main repo (or a regular git repo)
            if (candidate / KITTIFY_DIR).is_dir():
                return candidate

        # Also check for .kittify marker (fallback for non-git scenarios)
        kittify_path = candidate / KITTIFY_DIR
        if kittify_path.is_symlink() or not kittify_path.exists():
            # Broken symlink - skip this candidate
            continue
        if kittify_path.is_dir():
            return candidate

    return None


def x_locate_project_root__mutmut_37(start: Path | None = None) -> Optional[Path]:
    """
    Locate the MAIN spec-kitty project root directory, even from within worktrees.

    This function correctly handles git worktrees by detecting when .git is a
    file (worktree pointer) vs a directory (main repo), and following the
    pointer back to the main repository.

    Resolution order:
    1. SPECIFY_REPO_ROOT environment variable (highest priority)
    2. Walk up directory tree, detecting worktree .git files and following to main repo
    3. Fall back to .kittify/ marker search

    Args:
        start: Starting directory for search (defaults to current working directory)

    Returns:
        Path to MAIN project root (not worktree), or None if not found

    Examples:
        >>> # From main repo
        >>> root = locate_project_root()
        >>> assert (root / ".kittify").exists()

        >>> # From worktree - returns MAIN repo, not worktree
        >>> root = locate_project_root(Path(".worktrees/my-feature"))
        >>> assert ".worktrees" not in str(root)
    """
    # Tier 1: Check environment variable (allows override for CI/CD)
    if env_root := os.getenv("SPECIFY_REPO_ROOT"):
        env_path = Path(env_root).resolve()
        if env_path.exists() and (env_path / KITTIFY_DIR).is_dir():
            return env_path
        # Invalid env var - fall through to other methods

    # Tier 2: Walk up directory tree, handling worktree .git files
    current = (start or Path.cwd()).resolve()

    for candidate in [current, *current.parents]:
        git_path = candidate / ".git"

        if git_path.is_file():
            # .git files with gitdir: pointers appear in worktrees,
            # submodules, and separate-git-dir clones.  Only follow the
            # pointer when it has the .git/worktrees/<name> topology.
            try:
                content = git_path.read_text().strip()
                if content.startswith("gitdir:"):
                    gitdir = Path(content.split(":", 1)[1].strip())
                    if _is_worktree_gitdir(gitdir):
                        # Navigate: .git/worktrees/name -> .git -> main repo root
                        main_git_dir = gitdir.parent.parent
                        main_repo = main_git_dir.parent
                        if main_repo.exists() and (main_repo / KITTIFY_DIR).is_dir():
                            return main_repo
            except (OSError, ValueError):
                # If we can't read or parse the .git file, continue searching
                pass

        elif git_path.is_dir():
            # This is the main repo (or a regular git repo)
            if (candidate / KITTIFY_DIR).is_dir():
                return candidate

        # Also check for .kittify marker (fallback for non-git scenarios)
        kittify_path = candidate / KITTIFY_DIR
        if kittify_path.is_symlink() and kittify_path.exists():
            # Broken symlink - skip this candidate
            continue
        if kittify_path.is_dir():
            return candidate

    return None


def x_locate_project_root__mutmut_38(start: Path | None = None) -> Optional[Path]:
    """
    Locate the MAIN spec-kitty project root directory, even from within worktrees.

    This function correctly handles git worktrees by detecting when .git is a
    file (worktree pointer) vs a directory (main repo), and following the
    pointer back to the main repository.

    Resolution order:
    1. SPECIFY_REPO_ROOT environment variable (highest priority)
    2. Walk up directory tree, detecting worktree .git files and following to main repo
    3. Fall back to .kittify/ marker search

    Args:
        start: Starting directory for search (defaults to current working directory)

    Returns:
        Path to MAIN project root (not worktree), or None if not found

    Examples:
        >>> # From main repo
        >>> root = locate_project_root()
        >>> assert (root / ".kittify").exists()

        >>> # From worktree - returns MAIN repo, not worktree
        >>> root = locate_project_root(Path(".worktrees/my-feature"))
        >>> assert ".worktrees" not in str(root)
    """
    # Tier 1: Check environment variable (allows override for CI/CD)
    if env_root := os.getenv("SPECIFY_REPO_ROOT"):
        env_path = Path(env_root).resolve()
        if env_path.exists() and (env_path / KITTIFY_DIR).is_dir():
            return env_path
        # Invalid env var - fall through to other methods

    # Tier 2: Walk up directory tree, handling worktree .git files
    current = (start or Path.cwd()).resolve()

    for candidate in [current, *current.parents]:
        git_path = candidate / ".git"

        if git_path.is_file():
            # .git files with gitdir: pointers appear in worktrees,
            # submodules, and separate-git-dir clones.  Only follow the
            # pointer when it has the .git/worktrees/<name> topology.
            try:
                content = git_path.read_text().strip()
                if content.startswith("gitdir:"):
                    gitdir = Path(content.split(":", 1)[1].strip())
                    if _is_worktree_gitdir(gitdir):
                        # Navigate: .git/worktrees/name -> .git -> main repo root
                        main_git_dir = gitdir.parent.parent
                        main_repo = main_git_dir.parent
                        if main_repo.exists() and (main_repo / KITTIFY_DIR).is_dir():
                            return main_repo
            except (OSError, ValueError):
                # If we can't read or parse the .git file, continue searching
                pass

        elif git_path.is_dir():
            # This is the main repo (or a regular git repo)
            if (candidate / KITTIFY_DIR).is_dir():
                return candidate

        # Also check for .kittify marker (fallback for non-git scenarios)
        kittify_path = candidate / KITTIFY_DIR
        if kittify_path.is_symlink() and not kittify_path.exists():
            # Broken symlink - skip this candidate
            break
        if kittify_path.is_dir():
            return candidate

    return None

x_locate_project_root__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_locate_project_root__mutmut_1': x_locate_project_root__mutmut_1, 
    'x_locate_project_root__mutmut_2': x_locate_project_root__mutmut_2, 
    'x_locate_project_root__mutmut_3': x_locate_project_root__mutmut_3, 
    'x_locate_project_root__mutmut_4': x_locate_project_root__mutmut_4, 
    'x_locate_project_root__mutmut_5': x_locate_project_root__mutmut_5, 
    'x_locate_project_root__mutmut_6': x_locate_project_root__mutmut_6, 
    'x_locate_project_root__mutmut_7': x_locate_project_root__mutmut_7, 
    'x_locate_project_root__mutmut_8': x_locate_project_root__mutmut_8, 
    'x_locate_project_root__mutmut_9': x_locate_project_root__mutmut_9, 
    'x_locate_project_root__mutmut_10': x_locate_project_root__mutmut_10, 
    'x_locate_project_root__mutmut_11': x_locate_project_root__mutmut_11, 
    'x_locate_project_root__mutmut_12': x_locate_project_root__mutmut_12, 
    'x_locate_project_root__mutmut_13': x_locate_project_root__mutmut_13, 
    'x_locate_project_root__mutmut_14': x_locate_project_root__mutmut_14, 
    'x_locate_project_root__mutmut_15': x_locate_project_root__mutmut_15, 
    'x_locate_project_root__mutmut_16': x_locate_project_root__mutmut_16, 
    'x_locate_project_root__mutmut_17': x_locate_project_root__mutmut_17, 
    'x_locate_project_root__mutmut_18': x_locate_project_root__mutmut_18, 
    'x_locate_project_root__mutmut_19': x_locate_project_root__mutmut_19, 
    'x_locate_project_root__mutmut_20': x_locate_project_root__mutmut_20, 
    'x_locate_project_root__mutmut_21': x_locate_project_root__mutmut_21, 
    'x_locate_project_root__mutmut_22': x_locate_project_root__mutmut_22, 
    'x_locate_project_root__mutmut_23': x_locate_project_root__mutmut_23, 
    'x_locate_project_root__mutmut_24': x_locate_project_root__mutmut_24, 
    'x_locate_project_root__mutmut_25': x_locate_project_root__mutmut_25, 
    'x_locate_project_root__mutmut_26': x_locate_project_root__mutmut_26, 
    'x_locate_project_root__mutmut_27': x_locate_project_root__mutmut_27, 
    'x_locate_project_root__mutmut_28': x_locate_project_root__mutmut_28, 
    'x_locate_project_root__mutmut_29': x_locate_project_root__mutmut_29, 
    'x_locate_project_root__mutmut_30': x_locate_project_root__mutmut_30, 
    'x_locate_project_root__mutmut_31': x_locate_project_root__mutmut_31, 
    'x_locate_project_root__mutmut_32': x_locate_project_root__mutmut_32, 
    'x_locate_project_root__mutmut_33': x_locate_project_root__mutmut_33, 
    'x_locate_project_root__mutmut_34': x_locate_project_root__mutmut_34, 
    'x_locate_project_root__mutmut_35': x_locate_project_root__mutmut_35, 
    'x_locate_project_root__mutmut_36': x_locate_project_root__mutmut_36, 
    'x_locate_project_root__mutmut_37': x_locate_project_root__mutmut_37, 
    'x_locate_project_root__mutmut_38': x_locate_project_root__mutmut_38
}
x_locate_project_root__mutmut_orig.__name__ = 'x_locate_project_root'


def is_worktree_context(path: Path) -> bool:
    args = [path]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_is_worktree_context__mutmut_orig, x_is_worktree_context__mutmut_mutants, args, kwargs, None)


def x_is_worktree_context__mutmut_orig(path: Path) -> bool:
    """
    Detect if the given path is within a git worktree directory.

    Checks two conditions:
    1. '.worktrees' appears in the path hierarchy (spec-kitty managed worktrees)
    2. The nearest .git entry is a file with a gitdir: pointer (generic git worktree)

    Args:
        path: Path to check (typically current working directory)

    Returns:
        True if path is within any git worktree, False otherwise

    Examples:
        >>> is_worktree_context(Path("/repo/.worktrees/feature-001"))
        True
        >>> is_worktree_context(Path("/repo/kitty-specs"))
        False
        >>> # Also detects external worktrees (e.g. under /tmp)
        >>> is_worktree_context(Path("/tmp/my-worktree"))  # if .git is a gitdir pointer
        True
    """
    # Fast path: spec-kitty managed worktrees
    if WORKTREES_DIR in path.parts:
        return True

    # Generic detection: walk up to find .git file with gitdir pointer
    # Only recognise true worktrees (.git/worktrees/<name> topology),
    # NOT submodules (.git/modules/<mod>) or separate-git-dir clones.
    resolved = path.resolve()
    for candidate in [resolved, *resolved.parents]:
        git_path = candidate / ".git"
        if git_path.is_file():
            try:
                content = git_path.read_text().strip()
                if content.startswith("gitdir:"):
                    gitdir = Path(content.split(":", 1)[1].strip())
                    if _is_worktree_gitdir(gitdir):
                        return True
            except OSError:
                pass
            break
        elif git_path.is_dir():
            # Main repo .git directory — not a worktree
            break

    return False


def x_is_worktree_context__mutmut_1(path: Path) -> bool:
    """
    Detect if the given path is within a git worktree directory.

    Checks two conditions:
    1. '.worktrees' appears in the path hierarchy (spec-kitty managed worktrees)
    2. The nearest .git entry is a file with a gitdir: pointer (generic git worktree)

    Args:
        path: Path to check (typically current working directory)

    Returns:
        True if path is within any git worktree, False otherwise

    Examples:
        >>> is_worktree_context(Path("/repo/.worktrees/feature-001"))
        True
        >>> is_worktree_context(Path("/repo/kitty-specs"))
        False
        >>> # Also detects external worktrees (e.g. under /tmp)
        >>> is_worktree_context(Path("/tmp/my-worktree"))  # if .git is a gitdir pointer
        True
    """
    # Fast path: spec-kitty managed worktrees
    if WORKTREES_DIR not in path.parts:
        return True

    # Generic detection: walk up to find .git file with gitdir pointer
    # Only recognise true worktrees (.git/worktrees/<name> topology),
    # NOT submodules (.git/modules/<mod>) or separate-git-dir clones.
    resolved = path.resolve()
    for candidate in [resolved, *resolved.parents]:
        git_path = candidate / ".git"
        if git_path.is_file():
            try:
                content = git_path.read_text().strip()
                if content.startswith("gitdir:"):
                    gitdir = Path(content.split(":", 1)[1].strip())
                    if _is_worktree_gitdir(gitdir):
                        return True
            except OSError:
                pass
            break
        elif git_path.is_dir():
            # Main repo .git directory — not a worktree
            break

    return False


def x_is_worktree_context__mutmut_2(path: Path) -> bool:
    """
    Detect if the given path is within a git worktree directory.

    Checks two conditions:
    1. '.worktrees' appears in the path hierarchy (spec-kitty managed worktrees)
    2. The nearest .git entry is a file with a gitdir: pointer (generic git worktree)

    Args:
        path: Path to check (typically current working directory)

    Returns:
        True if path is within any git worktree, False otherwise

    Examples:
        >>> is_worktree_context(Path("/repo/.worktrees/feature-001"))
        True
        >>> is_worktree_context(Path("/repo/kitty-specs"))
        False
        >>> # Also detects external worktrees (e.g. under /tmp)
        >>> is_worktree_context(Path("/tmp/my-worktree"))  # if .git is a gitdir pointer
        True
    """
    # Fast path: spec-kitty managed worktrees
    if WORKTREES_DIR in path.parts:
        return False

    # Generic detection: walk up to find .git file with gitdir pointer
    # Only recognise true worktrees (.git/worktrees/<name> topology),
    # NOT submodules (.git/modules/<mod>) or separate-git-dir clones.
    resolved = path.resolve()
    for candidate in [resolved, *resolved.parents]:
        git_path = candidate / ".git"
        if git_path.is_file():
            try:
                content = git_path.read_text().strip()
                if content.startswith("gitdir:"):
                    gitdir = Path(content.split(":", 1)[1].strip())
                    if _is_worktree_gitdir(gitdir):
                        return True
            except OSError:
                pass
            break
        elif git_path.is_dir():
            # Main repo .git directory — not a worktree
            break

    return False


def x_is_worktree_context__mutmut_3(path: Path) -> bool:
    """
    Detect if the given path is within a git worktree directory.

    Checks two conditions:
    1. '.worktrees' appears in the path hierarchy (spec-kitty managed worktrees)
    2. The nearest .git entry is a file with a gitdir: pointer (generic git worktree)

    Args:
        path: Path to check (typically current working directory)

    Returns:
        True if path is within any git worktree, False otherwise

    Examples:
        >>> is_worktree_context(Path("/repo/.worktrees/feature-001"))
        True
        >>> is_worktree_context(Path("/repo/kitty-specs"))
        False
        >>> # Also detects external worktrees (e.g. under /tmp)
        >>> is_worktree_context(Path("/tmp/my-worktree"))  # if .git is a gitdir pointer
        True
    """
    # Fast path: spec-kitty managed worktrees
    if WORKTREES_DIR in path.parts:
        return True

    # Generic detection: walk up to find .git file with gitdir pointer
    # Only recognise true worktrees (.git/worktrees/<name> topology),
    # NOT submodules (.git/modules/<mod>) or separate-git-dir clones.
    resolved = None
    for candidate in [resolved, *resolved.parents]:
        git_path = candidate / ".git"
        if git_path.is_file():
            try:
                content = git_path.read_text().strip()
                if content.startswith("gitdir:"):
                    gitdir = Path(content.split(":", 1)[1].strip())
                    if _is_worktree_gitdir(gitdir):
                        return True
            except OSError:
                pass
            break
        elif git_path.is_dir():
            # Main repo .git directory — not a worktree
            break

    return False


def x_is_worktree_context__mutmut_4(path: Path) -> bool:
    """
    Detect if the given path is within a git worktree directory.

    Checks two conditions:
    1. '.worktrees' appears in the path hierarchy (spec-kitty managed worktrees)
    2. The nearest .git entry is a file with a gitdir: pointer (generic git worktree)

    Args:
        path: Path to check (typically current working directory)

    Returns:
        True if path is within any git worktree, False otherwise

    Examples:
        >>> is_worktree_context(Path("/repo/.worktrees/feature-001"))
        True
        >>> is_worktree_context(Path("/repo/kitty-specs"))
        False
        >>> # Also detects external worktrees (e.g. under /tmp)
        >>> is_worktree_context(Path("/tmp/my-worktree"))  # if .git is a gitdir pointer
        True
    """
    # Fast path: spec-kitty managed worktrees
    if WORKTREES_DIR in path.parts:
        return True

    # Generic detection: walk up to find .git file with gitdir pointer
    # Only recognise true worktrees (.git/worktrees/<name> topology),
    # NOT submodules (.git/modules/<mod>) or separate-git-dir clones.
    resolved = path.resolve()
    for candidate in [resolved, *resolved.parents]:
        git_path = None
        if git_path.is_file():
            try:
                content = git_path.read_text().strip()
                if content.startswith("gitdir:"):
                    gitdir = Path(content.split(":", 1)[1].strip())
                    if _is_worktree_gitdir(gitdir):
                        return True
            except OSError:
                pass
            break
        elif git_path.is_dir():
            # Main repo .git directory — not a worktree
            break

    return False


def x_is_worktree_context__mutmut_5(path: Path) -> bool:
    """
    Detect if the given path is within a git worktree directory.

    Checks two conditions:
    1. '.worktrees' appears in the path hierarchy (spec-kitty managed worktrees)
    2. The nearest .git entry is a file with a gitdir: pointer (generic git worktree)

    Args:
        path: Path to check (typically current working directory)

    Returns:
        True if path is within any git worktree, False otherwise

    Examples:
        >>> is_worktree_context(Path("/repo/.worktrees/feature-001"))
        True
        >>> is_worktree_context(Path("/repo/kitty-specs"))
        False
        >>> # Also detects external worktrees (e.g. under /tmp)
        >>> is_worktree_context(Path("/tmp/my-worktree"))  # if .git is a gitdir pointer
        True
    """
    # Fast path: spec-kitty managed worktrees
    if WORKTREES_DIR in path.parts:
        return True

    # Generic detection: walk up to find .git file with gitdir pointer
    # Only recognise true worktrees (.git/worktrees/<name> topology),
    # NOT submodules (.git/modules/<mod>) or separate-git-dir clones.
    resolved = path.resolve()
    for candidate in [resolved, *resolved.parents]:
        git_path = candidate * ".git"
        if git_path.is_file():
            try:
                content = git_path.read_text().strip()
                if content.startswith("gitdir:"):
                    gitdir = Path(content.split(":", 1)[1].strip())
                    if _is_worktree_gitdir(gitdir):
                        return True
            except OSError:
                pass
            break
        elif git_path.is_dir():
            # Main repo .git directory — not a worktree
            break

    return False


def x_is_worktree_context__mutmut_6(path: Path) -> bool:
    """
    Detect if the given path is within a git worktree directory.

    Checks two conditions:
    1. '.worktrees' appears in the path hierarchy (spec-kitty managed worktrees)
    2. The nearest .git entry is a file with a gitdir: pointer (generic git worktree)

    Args:
        path: Path to check (typically current working directory)

    Returns:
        True if path is within any git worktree, False otherwise

    Examples:
        >>> is_worktree_context(Path("/repo/.worktrees/feature-001"))
        True
        >>> is_worktree_context(Path("/repo/kitty-specs"))
        False
        >>> # Also detects external worktrees (e.g. under /tmp)
        >>> is_worktree_context(Path("/tmp/my-worktree"))  # if .git is a gitdir pointer
        True
    """
    # Fast path: spec-kitty managed worktrees
    if WORKTREES_DIR in path.parts:
        return True

    # Generic detection: walk up to find .git file with gitdir pointer
    # Only recognise true worktrees (.git/worktrees/<name> topology),
    # NOT submodules (.git/modules/<mod>) or separate-git-dir clones.
    resolved = path.resolve()
    for candidate in [resolved, *resolved.parents]:
        git_path = candidate / "XX.gitXX"
        if git_path.is_file():
            try:
                content = git_path.read_text().strip()
                if content.startswith("gitdir:"):
                    gitdir = Path(content.split(":", 1)[1].strip())
                    if _is_worktree_gitdir(gitdir):
                        return True
            except OSError:
                pass
            break
        elif git_path.is_dir():
            # Main repo .git directory — not a worktree
            break

    return False


def x_is_worktree_context__mutmut_7(path: Path) -> bool:
    """
    Detect if the given path is within a git worktree directory.

    Checks two conditions:
    1. '.worktrees' appears in the path hierarchy (spec-kitty managed worktrees)
    2. The nearest .git entry is a file with a gitdir: pointer (generic git worktree)

    Args:
        path: Path to check (typically current working directory)

    Returns:
        True if path is within any git worktree, False otherwise

    Examples:
        >>> is_worktree_context(Path("/repo/.worktrees/feature-001"))
        True
        >>> is_worktree_context(Path("/repo/kitty-specs"))
        False
        >>> # Also detects external worktrees (e.g. under /tmp)
        >>> is_worktree_context(Path("/tmp/my-worktree"))  # if .git is a gitdir pointer
        True
    """
    # Fast path: spec-kitty managed worktrees
    if WORKTREES_DIR in path.parts:
        return True

    # Generic detection: walk up to find .git file with gitdir pointer
    # Only recognise true worktrees (.git/worktrees/<name> topology),
    # NOT submodules (.git/modules/<mod>) or separate-git-dir clones.
    resolved = path.resolve()
    for candidate in [resolved, *resolved.parents]:
        git_path = candidate / ".GIT"
        if git_path.is_file():
            try:
                content = git_path.read_text().strip()
                if content.startswith("gitdir:"):
                    gitdir = Path(content.split(":", 1)[1].strip())
                    if _is_worktree_gitdir(gitdir):
                        return True
            except OSError:
                pass
            break
        elif git_path.is_dir():
            # Main repo .git directory — not a worktree
            break

    return False


def x_is_worktree_context__mutmut_8(path: Path) -> bool:
    """
    Detect if the given path is within a git worktree directory.

    Checks two conditions:
    1. '.worktrees' appears in the path hierarchy (spec-kitty managed worktrees)
    2. The nearest .git entry is a file with a gitdir: pointer (generic git worktree)

    Args:
        path: Path to check (typically current working directory)

    Returns:
        True if path is within any git worktree, False otherwise

    Examples:
        >>> is_worktree_context(Path("/repo/.worktrees/feature-001"))
        True
        >>> is_worktree_context(Path("/repo/kitty-specs"))
        False
        >>> # Also detects external worktrees (e.g. under /tmp)
        >>> is_worktree_context(Path("/tmp/my-worktree"))  # if .git is a gitdir pointer
        True
    """
    # Fast path: spec-kitty managed worktrees
    if WORKTREES_DIR in path.parts:
        return True

    # Generic detection: walk up to find .git file with gitdir pointer
    # Only recognise true worktrees (.git/worktrees/<name> topology),
    # NOT submodules (.git/modules/<mod>) or separate-git-dir clones.
    resolved = path.resolve()
    for candidate in [resolved, *resolved.parents]:
        git_path = candidate / ".git"
        if git_path.is_file():
            try:
                content = None
                if content.startswith("gitdir:"):
                    gitdir = Path(content.split(":", 1)[1].strip())
                    if _is_worktree_gitdir(gitdir):
                        return True
            except OSError:
                pass
            break
        elif git_path.is_dir():
            # Main repo .git directory — not a worktree
            break

    return False


def x_is_worktree_context__mutmut_9(path: Path) -> bool:
    """
    Detect if the given path is within a git worktree directory.

    Checks two conditions:
    1. '.worktrees' appears in the path hierarchy (spec-kitty managed worktrees)
    2. The nearest .git entry is a file with a gitdir: pointer (generic git worktree)

    Args:
        path: Path to check (typically current working directory)

    Returns:
        True if path is within any git worktree, False otherwise

    Examples:
        >>> is_worktree_context(Path("/repo/.worktrees/feature-001"))
        True
        >>> is_worktree_context(Path("/repo/kitty-specs"))
        False
        >>> # Also detects external worktrees (e.g. under /tmp)
        >>> is_worktree_context(Path("/tmp/my-worktree"))  # if .git is a gitdir pointer
        True
    """
    # Fast path: spec-kitty managed worktrees
    if WORKTREES_DIR in path.parts:
        return True

    # Generic detection: walk up to find .git file with gitdir pointer
    # Only recognise true worktrees (.git/worktrees/<name> topology),
    # NOT submodules (.git/modules/<mod>) or separate-git-dir clones.
    resolved = path.resolve()
    for candidate in [resolved, *resolved.parents]:
        git_path = candidate / ".git"
        if git_path.is_file():
            try:
                content = git_path.read_text().strip()
                if content.startswith(None):
                    gitdir = Path(content.split(":", 1)[1].strip())
                    if _is_worktree_gitdir(gitdir):
                        return True
            except OSError:
                pass
            break
        elif git_path.is_dir():
            # Main repo .git directory — not a worktree
            break

    return False


def x_is_worktree_context__mutmut_10(path: Path) -> bool:
    """
    Detect if the given path is within a git worktree directory.

    Checks two conditions:
    1. '.worktrees' appears in the path hierarchy (spec-kitty managed worktrees)
    2. The nearest .git entry is a file with a gitdir: pointer (generic git worktree)

    Args:
        path: Path to check (typically current working directory)

    Returns:
        True if path is within any git worktree, False otherwise

    Examples:
        >>> is_worktree_context(Path("/repo/.worktrees/feature-001"))
        True
        >>> is_worktree_context(Path("/repo/kitty-specs"))
        False
        >>> # Also detects external worktrees (e.g. under /tmp)
        >>> is_worktree_context(Path("/tmp/my-worktree"))  # if .git is a gitdir pointer
        True
    """
    # Fast path: spec-kitty managed worktrees
    if WORKTREES_DIR in path.parts:
        return True

    # Generic detection: walk up to find .git file with gitdir pointer
    # Only recognise true worktrees (.git/worktrees/<name> topology),
    # NOT submodules (.git/modules/<mod>) or separate-git-dir clones.
    resolved = path.resolve()
    for candidate in [resolved, *resolved.parents]:
        git_path = candidate / ".git"
        if git_path.is_file():
            try:
                content = git_path.read_text().strip()
                if content.startswith("XXgitdir:XX"):
                    gitdir = Path(content.split(":", 1)[1].strip())
                    if _is_worktree_gitdir(gitdir):
                        return True
            except OSError:
                pass
            break
        elif git_path.is_dir():
            # Main repo .git directory — not a worktree
            break

    return False


def x_is_worktree_context__mutmut_11(path: Path) -> bool:
    """
    Detect if the given path is within a git worktree directory.

    Checks two conditions:
    1. '.worktrees' appears in the path hierarchy (spec-kitty managed worktrees)
    2. The nearest .git entry is a file with a gitdir: pointer (generic git worktree)

    Args:
        path: Path to check (typically current working directory)

    Returns:
        True if path is within any git worktree, False otherwise

    Examples:
        >>> is_worktree_context(Path("/repo/.worktrees/feature-001"))
        True
        >>> is_worktree_context(Path("/repo/kitty-specs"))
        False
        >>> # Also detects external worktrees (e.g. under /tmp)
        >>> is_worktree_context(Path("/tmp/my-worktree"))  # if .git is a gitdir pointer
        True
    """
    # Fast path: spec-kitty managed worktrees
    if WORKTREES_DIR in path.parts:
        return True

    # Generic detection: walk up to find .git file with gitdir pointer
    # Only recognise true worktrees (.git/worktrees/<name> topology),
    # NOT submodules (.git/modules/<mod>) or separate-git-dir clones.
    resolved = path.resolve()
    for candidate in [resolved, *resolved.parents]:
        git_path = candidate / ".git"
        if git_path.is_file():
            try:
                content = git_path.read_text().strip()
                if content.startswith("GITDIR:"):
                    gitdir = Path(content.split(":", 1)[1].strip())
                    if _is_worktree_gitdir(gitdir):
                        return True
            except OSError:
                pass
            break
        elif git_path.is_dir():
            # Main repo .git directory — not a worktree
            break

    return False


def x_is_worktree_context__mutmut_12(path: Path) -> bool:
    """
    Detect if the given path is within a git worktree directory.

    Checks two conditions:
    1. '.worktrees' appears in the path hierarchy (spec-kitty managed worktrees)
    2. The nearest .git entry is a file with a gitdir: pointer (generic git worktree)

    Args:
        path: Path to check (typically current working directory)

    Returns:
        True if path is within any git worktree, False otherwise

    Examples:
        >>> is_worktree_context(Path("/repo/.worktrees/feature-001"))
        True
        >>> is_worktree_context(Path("/repo/kitty-specs"))
        False
        >>> # Also detects external worktrees (e.g. under /tmp)
        >>> is_worktree_context(Path("/tmp/my-worktree"))  # if .git is a gitdir pointer
        True
    """
    # Fast path: spec-kitty managed worktrees
    if WORKTREES_DIR in path.parts:
        return True

    # Generic detection: walk up to find .git file with gitdir pointer
    # Only recognise true worktrees (.git/worktrees/<name> topology),
    # NOT submodules (.git/modules/<mod>) or separate-git-dir clones.
    resolved = path.resolve()
    for candidate in [resolved, *resolved.parents]:
        git_path = candidate / ".git"
        if git_path.is_file():
            try:
                content = git_path.read_text().strip()
                if content.startswith("gitdir:"):
                    gitdir = None
                    if _is_worktree_gitdir(gitdir):
                        return True
            except OSError:
                pass
            break
        elif git_path.is_dir():
            # Main repo .git directory — not a worktree
            break

    return False


def x_is_worktree_context__mutmut_13(path: Path) -> bool:
    """
    Detect if the given path is within a git worktree directory.

    Checks two conditions:
    1. '.worktrees' appears in the path hierarchy (spec-kitty managed worktrees)
    2. The nearest .git entry is a file with a gitdir: pointer (generic git worktree)

    Args:
        path: Path to check (typically current working directory)

    Returns:
        True if path is within any git worktree, False otherwise

    Examples:
        >>> is_worktree_context(Path("/repo/.worktrees/feature-001"))
        True
        >>> is_worktree_context(Path("/repo/kitty-specs"))
        False
        >>> # Also detects external worktrees (e.g. under /tmp)
        >>> is_worktree_context(Path("/tmp/my-worktree"))  # if .git is a gitdir pointer
        True
    """
    # Fast path: spec-kitty managed worktrees
    if WORKTREES_DIR in path.parts:
        return True

    # Generic detection: walk up to find .git file with gitdir pointer
    # Only recognise true worktrees (.git/worktrees/<name> topology),
    # NOT submodules (.git/modules/<mod>) or separate-git-dir clones.
    resolved = path.resolve()
    for candidate in [resolved, *resolved.parents]:
        git_path = candidate / ".git"
        if git_path.is_file():
            try:
                content = git_path.read_text().strip()
                if content.startswith("gitdir:"):
                    gitdir = Path(None)
                    if _is_worktree_gitdir(gitdir):
                        return True
            except OSError:
                pass
            break
        elif git_path.is_dir():
            # Main repo .git directory — not a worktree
            break

    return False


def x_is_worktree_context__mutmut_14(path: Path) -> bool:
    """
    Detect if the given path is within a git worktree directory.

    Checks two conditions:
    1. '.worktrees' appears in the path hierarchy (spec-kitty managed worktrees)
    2. The nearest .git entry is a file with a gitdir: pointer (generic git worktree)

    Args:
        path: Path to check (typically current working directory)

    Returns:
        True if path is within any git worktree, False otherwise

    Examples:
        >>> is_worktree_context(Path("/repo/.worktrees/feature-001"))
        True
        >>> is_worktree_context(Path("/repo/kitty-specs"))
        False
        >>> # Also detects external worktrees (e.g. under /tmp)
        >>> is_worktree_context(Path("/tmp/my-worktree"))  # if .git is a gitdir pointer
        True
    """
    # Fast path: spec-kitty managed worktrees
    if WORKTREES_DIR in path.parts:
        return True

    # Generic detection: walk up to find .git file with gitdir pointer
    # Only recognise true worktrees (.git/worktrees/<name> topology),
    # NOT submodules (.git/modules/<mod>) or separate-git-dir clones.
    resolved = path.resolve()
    for candidate in [resolved, *resolved.parents]:
        git_path = candidate / ".git"
        if git_path.is_file():
            try:
                content = git_path.read_text().strip()
                if content.startswith("gitdir:"):
                    gitdir = Path(content.split(None, 1)[1].strip())
                    if _is_worktree_gitdir(gitdir):
                        return True
            except OSError:
                pass
            break
        elif git_path.is_dir():
            # Main repo .git directory — not a worktree
            break

    return False


def x_is_worktree_context__mutmut_15(path: Path) -> bool:
    """
    Detect if the given path is within a git worktree directory.

    Checks two conditions:
    1. '.worktrees' appears in the path hierarchy (spec-kitty managed worktrees)
    2. The nearest .git entry is a file with a gitdir: pointer (generic git worktree)

    Args:
        path: Path to check (typically current working directory)

    Returns:
        True if path is within any git worktree, False otherwise

    Examples:
        >>> is_worktree_context(Path("/repo/.worktrees/feature-001"))
        True
        >>> is_worktree_context(Path("/repo/kitty-specs"))
        False
        >>> # Also detects external worktrees (e.g. under /tmp)
        >>> is_worktree_context(Path("/tmp/my-worktree"))  # if .git is a gitdir pointer
        True
    """
    # Fast path: spec-kitty managed worktrees
    if WORKTREES_DIR in path.parts:
        return True

    # Generic detection: walk up to find .git file with gitdir pointer
    # Only recognise true worktrees (.git/worktrees/<name> topology),
    # NOT submodules (.git/modules/<mod>) or separate-git-dir clones.
    resolved = path.resolve()
    for candidate in [resolved, *resolved.parents]:
        git_path = candidate / ".git"
        if git_path.is_file():
            try:
                content = git_path.read_text().strip()
                if content.startswith("gitdir:"):
                    gitdir = Path(content.split(":", None)[1].strip())
                    if _is_worktree_gitdir(gitdir):
                        return True
            except OSError:
                pass
            break
        elif git_path.is_dir():
            # Main repo .git directory — not a worktree
            break

    return False


def x_is_worktree_context__mutmut_16(path: Path) -> bool:
    """
    Detect if the given path is within a git worktree directory.

    Checks two conditions:
    1. '.worktrees' appears in the path hierarchy (spec-kitty managed worktrees)
    2. The nearest .git entry is a file with a gitdir: pointer (generic git worktree)

    Args:
        path: Path to check (typically current working directory)

    Returns:
        True if path is within any git worktree, False otherwise

    Examples:
        >>> is_worktree_context(Path("/repo/.worktrees/feature-001"))
        True
        >>> is_worktree_context(Path("/repo/kitty-specs"))
        False
        >>> # Also detects external worktrees (e.g. under /tmp)
        >>> is_worktree_context(Path("/tmp/my-worktree"))  # if .git is a gitdir pointer
        True
    """
    # Fast path: spec-kitty managed worktrees
    if WORKTREES_DIR in path.parts:
        return True

    # Generic detection: walk up to find .git file with gitdir pointer
    # Only recognise true worktrees (.git/worktrees/<name> topology),
    # NOT submodules (.git/modules/<mod>) or separate-git-dir clones.
    resolved = path.resolve()
    for candidate in [resolved, *resolved.parents]:
        git_path = candidate / ".git"
        if git_path.is_file():
            try:
                content = git_path.read_text().strip()
                if content.startswith("gitdir:"):
                    gitdir = Path(content.split(1)[1].strip())
                    if _is_worktree_gitdir(gitdir):
                        return True
            except OSError:
                pass
            break
        elif git_path.is_dir():
            # Main repo .git directory — not a worktree
            break

    return False


def x_is_worktree_context__mutmut_17(path: Path) -> bool:
    """
    Detect if the given path is within a git worktree directory.

    Checks two conditions:
    1. '.worktrees' appears in the path hierarchy (spec-kitty managed worktrees)
    2. The nearest .git entry is a file with a gitdir: pointer (generic git worktree)

    Args:
        path: Path to check (typically current working directory)

    Returns:
        True if path is within any git worktree, False otherwise

    Examples:
        >>> is_worktree_context(Path("/repo/.worktrees/feature-001"))
        True
        >>> is_worktree_context(Path("/repo/kitty-specs"))
        False
        >>> # Also detects external worktrees (e.g. under /tmp)
        >>> is_worktree_context(Path("/tmp/my-worktree"))  # if .git is a gitdir pointer
        True
    """
    # Fast path: spec-kitty managed worktrees
    if WORKTREES_DIR in path.parts:
        return True

    # Generic detection: walk up to find .git file with gitdir pointer
    # Only recognise true worktrees (.git/worktrees/<name> topology),
    # NOT submodules (.git/modules/<mod>) or separate-git-dir clones.
    resolved = path.resolve()
    for candidate in [resolved, *resolved.parents]:
        git_path = candidate / ".git"
        if git_path.is_file():
            try:
                content = git_path.read_text().strip()
                if content.startswith("gitdir:"):
                    gitdir = Path(content.split(":", )[1].strip())
                    if _is_worktree_gitdir(gitdir):
                        return True
            except OSError:
                pass
            break
        elif git_path.is_dir():
            # Main repo .git directory — not a worktree
            break

    return False


def x_is_worktree_context__mutmut_18(path: Path) -> bool:
    """
    Detect if the given path is within a git worktree directory.

    Checks two conditions:
    1. '.worktrees' appears in the path hierarchy (spec-kitty managed worktrees)
    2. The nearest .git entry is a file with a gitdir: pointer (generic git worktree)

    Args:
        path: Path to check (typically current working directory)

    Returns:
        True if path is within any git worktree, False otherwise

    Examples:
        >>> is_worktree_context(Path("/repo/.worktrees/feature-001"))
        True
        >>> is_worktree_context(Path("/repo/kitty-specs"))
        False
        >>> # Also detects external worktrees (e.g. under /tmp)
        >>> is_worktree_context(Path("/tmp/my-worktree"))  # if .git is a gitdir pointer
        True
    """
    # Fast path: spec-kitty managed worktrees
    if WORKTREES_DIR in path.parts:
        return True

    # Generic detection: walk up to find .git file with gitdir pointer
    # Only recognise true worktrees (.git/worktrees/<name> topology),
    # NOT submodules (.git/modules/<mod>) or separate-git-dir clones.
    resolved = path.resolve()
    for candidate in [resolved, *resolved.parents]:
        git_path = candidate / ".git"
        if git_path.is_file():
            try:
                content = git_path.read_text().strip()
                if content.startswith("gitdir:"):
                    gitdir = Path(content.rsplit(":", 1)[1].strip())
                    if _is_worktree_gitdir(gitdir):
                        return True
            except OSError:
                pass
            break
        elif git_path.is_dir():
            # Main repo .git directory — not a worktree
            break

    return False


def x_is_worktree_context__mutmut_19(path: Path) -> bool:
    """
    Detect if the given path is within a git worktree directory.

    Checks two conditions:
    1. '.worktrees' appears in the path hierarchy (spec-kitty managed worktrees)
    2. The nearest .git entry is a file with a gitdir: pointer (generic git worktree)

    Args:
        path: Path to check (typically current working directory)

    Returns:
        True if path is within any git worktree, False otherwise

    Examples:
        >>> is_worktree_context(Path("/repo/.worktrees/feature-001"))
        True
        >>> is_worktree_context(Path("/repo/kitty-specs"))
        False
        >>> # Also detects external worktrees (e.g. under /tmp)
        >>> is_worktree_context(Path("/tmp/my-worktree"))  # if .git is a gitdir pointer
        True
    """
    # Fast path: spec-kitty managed worktrees
    if WORKTREES_DIR in path.parts:
        return True

    # Generic detection: walk up to find .git file with gitdir pointer
    # Only recognise true worktrees (.git/worktrees/<name> topology),
    # NOT submodules (.git/modules/<mod>) or separate-git-dir clones.
    resolved = path.resolve()
    for candidate in [resolved, *resolved.parents]:
        git_path = candidate / ".git"
        if git_path.is_file():
            try:
                content = git_path.read_text().strip()
                if content.startswith("gitdir:"):
                    gitdir = Path(content.split("XX:XX", 1)[1].strip())
                    if _is_worktree_gitdir(gitdir):
                        return True
            except OSError:
                pass
            break
        elif git_path.is_dir():
            # Main repo .git directory — not a worktree
            break

    return False


def x_is_worktree_context__mutmut_20(path: Path) -> bool:
    """
    Detect if the given path is within a git worktree directory.

    Checks two conditions:
    1. '.worktrees' appears in the path hierarchy (spec-kitty managed worktrees)
    2. The nearest .git entry is a file with a gitdir: pointer (generic git worktree)

    Args:
        path: Path to check (typically current working directory)

    Returns:
        True if path is within any git worktree, False otherwise

    Examples:
        >>> is_worktree_context(Path("/repo/.worktrees/feature-001"))
        True
        >>> is_worktree_context(Path("/repo/kitty-specs"))
        False
        >>> # Also detects external worktrees (e.g. under /tmp)
        >>> is_worktree_context(Path("/tmp/my-worktree"))  # if .git is a gitdir pointer
        True
    """
    # Fast path: spec-kitty managed worktrees
    if WORKTREES_DIR in path.parts:
        return True

    # Generic detection: walk up to find .git file with gitdir pointer
    # Only recognise true worktrees (.git/worktrees/<name> topology),
    # NOT submodules (.git/modules/<mod>) or separate-git-dir clones.
    resolved = path.resolve()
    for candidate in [resolved, *resolved.parents]:
        git_path = candidate / ".git"
        if git_path.is_file():
            try:
                content = git_path.read_text().strip()
                if content.startswith("gitdir:"):
                    gitdir = Path(content.split(":", 2)[1].strip())
                    if _is_worktree_gitdir(gitdir):
                        return True
            except OSError:
                pass
            break
        elif git_path.is_dir():
            # Main repo .git directory — not a worktree
            break

    return False


def x_is_worktree_context__mutmut_21(path: Path) -> bool:
    """
    Detect if the given path is within a git worktree directory.

    Checks two conditions:
    1. '.worktrees' appears in the path hierarchy (spec-kitty managed worktrees)
    2. The nearest .git entry is a file with a gitdir: pointer (generic git worktree)

    Args:
        path: Path to check (typically current working directory)

    Returns:
        True if path is within any git worktree, False otherwise

    Examples:
        >>> is_worktree_context(Path("/repo/.worktrees/feature-001"))
        True
        >>> is_worktree_context(Path("/repo/kitty-specs"))
        False
        >>> # Also detects external worktrees (e.g. under /tmp)
        >>> is_worktree_context(Path("/tmp/my-worktree"))  # if .git is a gitdir pointer
        True
    """
    # Fast path: spec-kitty managed worktrees
    if WORKTREES_DIR in path.parts:
        return True

    # Generic detection: walk up to find .git file with gitdir pointer
    # Only recognise true worktrees (.git/worktrees/<name> topology),
    # NOT submodules (.git/modules/<mod>) or separate-git-dir clones.
    resolved = path.resolve()
    for candidate in [resolved, *resolved.parents]:
        git_path = candidate / ".git"
        if git_path.is_file():
            try:
                content = git_path.read_text().strip()
                if content.startswith("gitdir:"):
                    gitdir = Path(content.split(":", 1)[2].strip())
                    if _is_worktree_gitdir(gitdir):
                        return True
            except OSError:
                pass
            break
        elif git_path.is_dir():
            # Main repo .git directory — not a worktree
            break

    return False


def x_is_worktree_context__mutmut_22(path: Path) -> bool:
    """
    Detect if the given path is within a git worktree directory.

    Checks two conditions:
    1. '.worktrees' appears in the path hierarchy (spec-kitty managed worktrees)
    2. The nearest .git entry is a file with a gitdir: pointer (generic git worktree)

    Args:
        path: Path to check (typically current working directory)

    Returns:
        True if path is within any git worktree, False otherwise

    Examples:
        >>> is_worktree_context(Path("/repo/.worktrees/feature-001"))
        True
        >>> is_worktree_context(Path("/repo/kitty-specs"))
        False
        >>> # Also detects external worktrees (e.g. under /tmp)
        >>> is_worktree_context(Path("/tmp/my-worktree"))  # if .git is a gitdir pointer
        True
    """
    # Fast path: spec-kitty managed worktrees
    if WORKTREES_DIR in path.parts:
        return True

    # Generic detection: walk up to find .git file with gitdir pointer
    # Only recognise true worktrees (.git/worktrees/<name> topology),
    # NOT submodules (.git/modules/<mod>) or separate-git-dir clones.
    resolved = path.resolve()
    for candidate in [resolved, *resolved.parents]:
        git_path = candidate / ".git"
        if git_path.is_file():
            try:
                content = git_path.read_text().strip()
                if content.startswith("gitdir:"):
                    gitdir = Path(content.split(":", 1)[1].strip())
                    if _is_worktree_gitdir(None):
                        return True
            except OSError:
                pass
            break
        elif git_path.is_dir():
            # Main repo .git directory — not a worktree
            break

    return False


def x_is_worktree_context__mutmut_23(path: Path) -> bool:
    """
    Detect if the given path is within a git worktree directory.

    Checks two conditions:
    1. '.worktrees' appears in the path hierarchy (spec-kitty managed worktrees)
    2. The nearest .git entry is a file with a gitdir: pointer (generic git worktree)

    Args:
        path: Path to check (typically current working directory)

    Returns:
        True if path is within any git worktree, False otherwise

    Examples:
        >>> is_worktree_context(Path("/repo/.worktrees/feature-001"))
        True
        >>> is_worktree_context(Path("/repo/kitty-specs"))
        False
        >>> # Also detects external worktrees (e.g. under /tmp)
        >>> is_worktree_context(Path("/tmp/my-worktree"))  # if .git is a gitdir pointer
        True
    """
    # Fast path: spec-kitty managed worktrees
    if WORKTREES_DIR in path.parts:
        return True

    # Generic detection: walk up to find .git file with gitdir pointer
    # Only recognise true worktrees (.git/worktrees/<name> topology),
    # NOT submodules (.git/modules/<mod>) or separate-git-dir clones.
    resolved = path.resolve()
    for candidate in [resolved, *resolved.parents]:
        git_path = candidate / ".git"
        if git_path.is_file():
            try:
                content = git_path.read_text().strip()
                if content.startswith("gitdir:"):
                    gitdir = Path(content.split(":", 1)[1].strip())
                    if _is_worktree_gitdir(gitdir):
                        return False
            except OSError:
                pass
            break
        elif git_path.is_dir():
            # Main repo .git directory — not a worktree
            break

    return False


def x_is_worktree_context__mutmut_24(path: Path) -> bool:
    """
    Detect if the given path is within a git worktree directory.

    Checks two conditions:
    1. '.worktrees' appears in the path hierarchy (spec-kitty managed worktrees)
    2. The nearest .git entry is a file with a gitdir: pointer (generic git worktree)

    Args:
        path: Path to check (typically current working directory)

    Returns:
        True if path is within any git worktree, False otherwise

    Examples:
        >>> is_worktree_context(Path("/repo/.worktrees/feature-001"))
        True
        >>> is_worktree_context(Path("/repo/kitty-specs"))
        False
        >>> # Also detects external worktrees (e.g. under /tmp)
        >>> is_worktree_context(Path("/tmp/my-worktree"))  # if .git is a gitdir pointer
        True
    """
    # Fast path: spec-kitty managed worktrees
    if WORKTREES_DIR in path.parts:
        return True

    # Generic detection: walk up to find .git file with gitdir pointer
    # Only recognise true worktrees (.git/worktrees/<name> topology),
    # NOT submodules (.git/modules/<mod>) or separate-git-dir clones.
    resolved = path.resolve()
    for candidate in [resolved, *resolved.parents]:
        git_path = candidate / ".git"
        if git_path.is_file():
            try:
                content = git_path.read_text().strip()
                if content.startswith("gitdir:"):
                    gitdir = Path(content.split(":", 1)[1].strip())
                    if _is_worktree_gitdir(gitdir):
                        return True
            except OSError:
                pass
            return
        elif git_path.is_dir():
            # Main repo .git directory — not a worktree
            break

    return False


def x_is_worktree_context__mutmut_25(path: Path) -> bool:
    """
    Detect if the given path is within a git worktree directory.

    Checks two conditions:
    1. '.worktrees' appears in the path hierarchy (spec-kitty managed worktrees)
    2. The nearest .git entry is a file with a gitdir: pointer (generic git worktree)

    Args:
        path: Path to check (typically current working directory)

    Returns:
        True if path is within any git worktree, False otherwise

    Examples:
        >>> is_worktree_context(Path("/repo/.worktrees/feature-001"))
        True
        >>> is_worktree_context(Path("/repo/kitty-specs"))
        False
        >>> # Also detects external worktrees (e.g. under /tmp)
        >>> is_worktree_context(Path("/tmp/my-worktree"))  # if .git is a gitdir pointer
        True
    """
    # Fast path: spec-kitty managed worktrees
    if WORKTREES_DIR in path.parts:
        return True

    # Generic detection: walk up to find .git file with gitdir pointer
    # Only recognise true worktrees (.git/worktrees/<name> topology),
    # NOT submodules (.git/modules/<mod>) or separate-git-dir clones.
    resolved = path.resolve()
    for candidate in [resolved, *resolved.parents]:
        git_path = candidate / ".git"
        if git_path.is_file():
            try:
                content = git_path.read_text().strip()
                if content.startswith("gitdir:"):
                    gitdir = Path(content.split(":", 1)[1].strip())
                    if _is_worktree_gitdir(gitdir):
                        return True
            except OSError:
                pass
            break
        elif git_path.is_dir():
            # Main repo .git directory — not a worktree
            return

    return False


def x_is_worktree_context__mutmut_26(path: Path) -> bool:
    """
    Detect if the given path is within a git worktree directory.

    Checks two conditions:
    1. '.worktrees' appears in the path hierarchy (spec-kitty managed worktrees)
    2. The nearest .git entry is a file with a gitdir: pointer (generic git worktree)

    Args:
        path: Path to check (typically current working directory)

    Returns:
        True if path is within any git worktree, False otherwise

    Examples:
        >>> is_worktree_context(Path("/repo/.worktrees/feature-001"))
        True
        >>> is_worktree_context(Path("/repo/kitty-specs"))
        False
        >>> # Also detects external worktrees (e.g. under /tmp)
        >>> is_worktree_context(Path("/tmp/my-worktree"))  # if .git is a gitdir pointer
        True
    """
    # Fast path: spec-kitty managed worktrees
    if WORKTREES_DIR in path.parts:
        return True

    # Generic detection: walk up to find .git file with gitdir pointer
    # Only recognise true worktrees (.git/worktrees/<name> topology),
    # NOT submodules (.git/modules/<mod>) or separate-git-dir clones.
    resolved = path.resolve()
    for candidate in [resolved, *resolved.parents]:
        git_path = candidate / ".git"
        if git_path.is_file():
            try:
                content = git_path.read_text().strip()
                if content.startswith("gitdir:"):
                    gitdir = Path(content.split(":", 1)[1].strip())
                    if _is_worktree_gitdir(gitdir):
                        return True
            except OSError:
                pass
            break
        elif git_path.is_dir():
            # Main repo .git directory — not a worktree
            break

    return True

x_is_worktree_context__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_is_worktree_context__mutmut_1': x_is_worktree_context__mutmut_1, 
    'x_is_worktree_context__mutmut_2': x_is_worktree_context__mutmut_2, 
    'x_is_worktree_context__mutmut_3': x_is_worktree_context__mutmut_3, 
    'x_is_worktree_context__mutmut_4': x_is_worktree_context__mutmut_4, 
    'x_is_worktree_context__mutmut_5': x_is_worktree_context__mutmut_5, 
    'x_is_worktree_context__mutmut_6': x_is_worktree_context__mutmut_6, 
    'x_is_worktree_context__mutmut_7': x_is_worktree_context__mutmut_7, 
    'x_is_worktree_context__mutmut_8': x_is_worktree_context__mutmut_8, 
    'x_is_worktree_context__mutmut_9': x_is_worktree_context__mutmut_9, 
    'x_is_worktree_context__mutmut_10': x_is_worktree_context__mutmut_10, 
    'x_is_worktree_context__mutmut_11': x_is_worktree_context__mutmut_11, 
    'x_is_worktree_context__mutmut_12': x_is_worktree_context__mutmut_12, 
    'x_is_worktree_context__mutmut_13': x_is_worktree_context__mutmut_13, 
    'x_is_worktree_context__mutmut_14': x_is_worktree_context__mutmut_14, 
    'x_is_worktree_context__mutmut_15': x_is_worktree_context__mutmut_15, 
    'x_is_worktree_context__mutmut_16': x_is_worktree_context__mutmut_16, 
    'x_is_worktree_context__mutmut_17': x_is_worktree_context__mutmut_17, 
    'x_is_worktree_context__mutmut_18': x_is_worktree_context__mutmut_18, 
    'x_is_worktree_context__mutmut_19': x_is_worktree_context__mutmut_19, 
    'x_is_worktree_context__mutmut_20': x_is_worktree_context__mutmut_20, 
    'x_is_worktree_context__mutmut_21': x_is_worktree_context__mutmut_21, 
    'x_is_worktree_context__mutmut_22': x_is_worktree_context__mutmut_22, 
    'x_is_worktree_context__mutmut_23': x_is_worktree_context__mutmut_23, 
    'x_is_worktree_context__mutmut_24': x_is_worktree_context__mutmut_24, 
    'x_is_worktree_context__mutmut_25': x_is_worktree_context__mutmut_25, 
    'x_is_worktree_context__mutmut_26': x_is_worktree_context__mutmut_26
}
x_is_worktree_context__mutmut_orig.__name__ = 'x_is_worktree_context'


def resolve_with_context(start: Path | None = None) -> Tuple[Optional[Path], bool]:
    args = [start]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_resolve_with_context__mutmut_orig, x_resolve_with_context__mutmut_mutants, args, kwargs, None)


def x_resolve_with_context__mutmut_orig(start: Path | None = None) -> Tuple[Optional[Path], bool]:
    """
    Resolve project root and detect worktree context in one call.

    Args:
        start: Starting directory for search (defaults to current working directory)

    Returns:
        Tuple of (project_root, is_worktree)
        - project_root: Path to repo root or None if not found
        - is_worktree: True if executing from within .worktrees/

    Examples:
        >>> # From main repo
        >>> root, in_worktree = resolve_with_context()
        >>> assert in_worktree is False

        >>> # From worktree
        >>> root, in_worktree = resolve_with_context(Path(".worktrees/my-feature"))
        >>> assert in_worktree is True
    """
    current = (start or Path.cwd()).resolve()
    root = locate_project_root(current)
    in_worktree = is_worktree_context(current)
    return root, in_worktree


def x_resolve_with_context__mutmut_1(start: Path | None = None) -> Tuple[Optional[Path], bool]:
    """
    Resolve project root and detect worktree context in one call.

    Args:
        start: Starting directory for search (defaults to current working directory)

    Returns:
        Tuple of (project_root, is_worktree)
        - project_root: Path to repo root or None if not found
        - is_worktree: True if executing from within .worktrees/

    Examples:
        >>> # From main repo
        >>> root, in_worktree = resolve_with_context()
        >>> assert in_worktree is False

        >>> # From worktree
        >>> root, in_worktree = resolve_with_context(Path(".worktrees/my-feature"))
        >>> assert in_worktree is True
    """
    current = None
    root = locate_project_root(current)
    in_worktree = is_worktree_context(current)
    return root, in_worktree


def x_resolve_with_context__mutmut_2(start: Path | None = None) -> Tuple[Optional[Path], bool]:
    """
    Resolve project root and detect worktree context in one call.

    Args:
        start: Starting directory for search (defaults to current working directory)

    Returns:
        Tuple of (project_root, is_worktree)
        - project_root: Path to repo root or None if not found
        - is_worktree: True if executing from within .worktrees/

    Examples:
        >>> # From main repo
        >>> root, in_worktree = resolve_with_context()
        >>> assert in_worktree is False

        >>> # From worktree
        >>> root, in_worktree = resolve_with_context(Path(".worktrees/my-feature"))
        >>> assert in_worktree is True
    """
    current = (start and Path.cwd()).resolve()
    root = locate_project_root(current)
    in_worktree = is_worktree_context(current)
    return root, in_worktree


def x_resolve_with_context__mutmut_3(start: Path | None = None) -> Tuple[Optional[Path], bool]:
    """
    Resolve project root and detect worktree context in one call.

    Args:
        start: Starting directory for search (defaults to current working directory)

    Returns:
        Tuple of (project_root, is_worktree)
        - project_root: Path to repo root or None if not found
        - is_worktree: True if executing from within .worktrees/

    Examples:
        >>> # From main repo
        >>> root, in_worktree = resolve_with_context()
        >>> assert in_worktree is False

        >>> # From worktree
        >>> root, in_worktree = resolve_with_context(Path(".worktrees/my-feature"))
        >>> assert in_worktree is True
    """
    current = (start or Path.cwd()).resolve()
    root = None
    in_worktree = is_worktree_context(current)
    return root, in_worktree


def x_resolve_with_context__mutmut_4(start: Path | None = None) -> Tuple[Optional[Path], bool]:
    """
    Resolve project root and detect worktree context in one call.

    Args:
        start: Starting directory for search (defaults to current working directory)

    Returns:
        Tuple of (project_root, is_worktree)
        - project_root: Path to repo root or None if not found
        - is_worktree: True if executing from within .worktrees/

    Examples:
        >>> # From main repo
        >>> root, in_worktree = resolve_with_context()
        >>> assert in_worktree is False

        >>> # From worktree
        >>> root, in_worktree = resolve_with_context(Path(".worktrees/my-feature"))
        >>> assert in_worktree is True
    """
    current = (start or Path.cwd()).resolve()
    root = locate_project_root(None)
    in_worktree = is_worktree_context(current)
    return root, in_worktree


def x_resolve_with_context__mutmut_5(start: Path | None = None) -> Tuple[Optional[Path], bool]:
    """
    Resolve project root and detect worktree context in one call.

    Args:
        start: Starting directory for search (defaults to current working directory)

    Returns:
        Tuple of (project_root, is_worktree)
        - project_root: Path to repo root or None if not found
        - is_worktree: True if executing from within .worktrees/

    Examples:
        >>> # From main repo
        >>> root, in_worktree = resolve_with_context()
        >>> assert in_worktree is False

        >>> # From worktree
        >>> root, in_worktree = resolve_with_context(Path(".worktrees/my-feature"))
        >>> assert in_worktree is True
    """
    current = (start or Path.cwd()).resolve()
    root = locate_project_root(current)
    in_worktree = None
    return root, in_worktree


def x_resolve_with_context__mutmut_6(start: Path | None = None) -> Tuple[Optional[Path], bool]:
    """
    Resolve project root and detect worktree context in one call.

    Args:
        start: Starting directory for search (defaults to current working directory)

    Returns:
        Tuple of (project_root, is_worktree)
        - project_root: Path to repo root or None if not found
        - is_worktree: True if executing from within .worktrees/

    Examples:
        >>> # From main repo
        >>> root, in_worktree = resolve_with_context()
        >>> assert in_worktree is False

        >>> # From worktree
        >>> root, in_worktree = resolve_with_context(Path(".worktrees/my-feature"))
        >>> assert in_worktree is True
    """
    current = (start or Path.cwd()).resolve()
    root = locate_project_root(current)
    in_worktree = is_worktree_context(None)
    return root, in_worktree

x_resolve_with_context__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_resolve_with_context__mutmut_1': x_resolve_with_context__mutmut_1, 
    'x_resolve_with_context__mutmut_2': x_resolve_with_context__mutmut_2, 
    'x_resolve_with_context__mutmut_3': x_resolve_with_context__mutmut_3, 
    'x_resolve_with_context__mutmut_4': x_resolve_with_context__mutmut_4, 
    'x_resolve_with_context__mutmut_5': x_resolve_with_context__mutmut_5, 
    'x_resolve_with_context__mutmut_6': x_resolve_with_context__mutmut_6
}
x_resolve_with_context__mutmut_orig.__name__ = 'x_resolve_with_context'


def check_broken_symlink(path: Path) -> bool:
    args = [path]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_check_broken_symlink__mutmut_orig, x_check_broken_symlink__mutmut_mutants, args, kwargs, None)


def x_check_broken_symlink__mutmut_orig(path: Path) -> bool:
    """
    Check if a path is a broken symlink (symlink pointing to non-existent target).

    This helper is useful for graceful error handling when dealing with
    worktree symlinks that may become invalid.

    Args:
        path: Path to check

    Returns:
        True if path is a broken symlink, False otherwise

    Note:
        A broken symlink returns True for is_symlink() but False for exists().
        Always check is_symlink() before exists() to detect this condition.
    """
    return path.is_symlink() and not path.exists()


def x_check_broken_symlink__mutmut_1(path: Path) -> bool:
    """
    Check if a path is a broken symlink (symlink pointing to non-existent target).

    This helper is useful for graceful error handling when dealing with
    worktree symlinks that may become invalid.

    Args:
        path: Path to check

    Returns:
        True if path is a broken symlink, False otherwise

    Note:
        A broken symlink returns True for is_symlink() but False for exists().
        Always check is_symlink() before exists() to detect this condition.
    """
    return path.is_symlink() or not path.exists()


def x_check_broken_symlink__mutmut_2(path: Path) -> bool:
    """
    Check if a path is a broken symlink (symlink pointing to non-existent target).

    This helper is useful for graceful error handling when dealing with
    worktree symlinks that may become invalid.

    Args:
        path: Path to check

    Returns:
        True if path is a broken symlink, False otherwise

    Note:
        A broken symlink returns True for is_symlink() but False for exists().
        Always check is_symlink() before exists() to detect this condition.
    """
    return path.is_symlink() and path.exists()

x_check_broken_symlink__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_check_broken_symlink__mutmut_1': x_check_broken_symlink__mutmut_1, 
    'x_check_broken_symlink__mutmut_2': x_check_broken_symlink__mutmut_2
}
x_check_broken_symlink__mutmut_orig.__name__ = 'x_check_broken_symlink'


def get_main_repo_root(current_path: Path) -> Path:
    args = [current_path]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_get_main_repo_root__mutmut_orig, x_get_main_repo_root__mutmut_mutants, args, kwargs, None)


def x_get_main_repo_root__mutmut_orig(current_path: Path) -> Path:
    """
    Get the main repository root, even if called from a worktree.

    When in a worktree, .git is a file pointing to the main repo's .git directory.
    This function follows that pointer to find the main repo root.

    Args:
        current_path: Current repo root (may be worktree or main repo)

    Returns:
        Path to the main repository root (resolves worktree pointers)

    Examples:
        >>> # From main repo - returns same path
        >>> get_main_repo_root(Path("/repo"))
        Path('/repo')

        >>> # From worktree - returns main repo
        >>> get_main_repo_root(Path("/repo/.worktrees/feature-001"))
        Path('/repo')
    """
    git_file = current_path / ".git"

    if git_file.is_file():
        try:
            git_content = git_file.read_text().strip()
            if git_content.startswith("gitdir:"):
                gitdir = Path(git_content.split(":", 1)[1].strip())
                # Navigate: .git/worktrees/name -> .git -> main repo root
                main_git_dir = gitdir.parent.parent
                main_repo_root = main_git_dir.parent
                return main_repo_root
        except (OSError, ValueError):
            pass

    return current_path


def x_get_main_repo_root__mutmut_1(current_path: Path) -> Path:
    """
    Get the main repository root, even if called from a worktree.

    When in a worktree, .git is a file pointing to the main repo's .git directory.
    This function follows that pointer to find the main repo root.

    Args:
        current_path: Current repo root (may be worktree or main repo)

    Returns:
        Path to the main repository root (resolves worktree pointers)

    Examples:
        >>> # From main repo - returns same path
        >>> get_main_repo_root(Path("/repo"))
        Path('/repo')

        >>> # From worktree - returns main repo
        >>> get_main_repo_root(Path("/repo/.worktrees/feature-001"))
        Path('/repo')
    """
    git_file = None

    if git_file.is_file():
        try:
            git_content = git_file.read_text().strip()
            if git_content.startswith("gitdir:"):
                gitdir = Path(git_content.split(":", 1)[1].strip())
                # Navigate: .git/worktrees/name -> .git -> main repo root
                main_git_dir = gitdir.parent.parent
                main_repo_root = main_git_dir.parent
                return main_repo_root
        except (OSError, ValueError):
            pass

    return current_path


def x_get_main_repo_root__mutmut_2(current_path: Path) -> Path:
    """
    Get the main repository root, even if called from a worktree.

    When in a worktree, .git is a file pointing to the main repo's .git directory.
    This function follows that pointer to find the main repo root.

    Args:
        current_path: Current repo root (may be worktree or main repo)

    Returns:
        Path to the main repository root (resolves worktree pointers)

    Examples:
        >>> # From main repo - returns same path
        >>> get_main_repo_root(Path("/repo"))
        Path('/repo')

        >>> # From worktree - returns main repo
        >>> get_main_repo_root(Path("/repo/.worktrees/feature-001"))
        Path('/repo')
    """
    git_file = current_path * ".git"

    if git_file.is_file():
        try:
            git_content = git_file.read_text().strip()
            if git_content.startswith("gitdir:"):
                gitdir = Path(git_content.split(":", 1)[1].strip())
                # Navigate: .git/worktrees/name -> .git -> main repo root
                main_git_dir = gitdir.parent.parent
                main_repo_root = main_git_dir.parent
                return main_repo_root
        except (OSError, ValueError):
            pass

    return current_path


def x_get_main_repo_root__mutmut_3(current_path: Path) -> Path:
    """
    Get the main repository root, even if called from a worktree.

    When in a worktree, .git is a file pointing to the main repo's .git directory.
    This function follows that pointer to find the main repo root.

    Args:
        current_path: Current repo root (may be worktree or main repo)

    Returns:
        Path to the main repository root (resolves worktree pointers)

    Examples:
        >>> # From main repo - returns same path
        >>> get_main_repo_root(Path("/repo"))
        Path('/repo')

        >>> # From worktree - returns main repo
        >>> get_main_repo_root(Path("/repo/.worktrees/feature-001"))
        Path('/repo')
    """
    git_file = current_path / "XX.gitXX"

    if git_file.is_file():
        try:
            git_content = git_file.read_text().strip()
            if git_content.startswith("gitdir:"):
                gitdir = Path(git_content.split(":", 1)[1].strip())
                # Navigate: .git/worktrees/name -> .git -> main repo root
                main_git_dir = gitdir.parent.parent
                main_repo_root = main_git_dir.parent
                return main_repo_root
        except (OSError, ValueError):
            pass

    return current_path


def x_get_main_repo_root__mutmut_4(current_path: Path) -> Path:
    """
    Get the main repository root, even if called from a worktree.

    When in a worktree, .git is a file pointing to the main repo's .git directory.
    This function follows that pointer to find the main repo root.

    Args:
        current_path: Current repo root (may be worktree or main repo)

    Returns:
        Path to the main repository root (resolves worktree pointers)

    Examples:
        >>> # From main repo - returns same path
        >>> get_main_repo_root(Path("/repo"))
        Path('/repo')

        >>> # From worktree - returns main repo
        >>> get_main_repo_root(Path("/repo/.worktrees/feature-001"))
        Path('/repo')
    """
    git_file = current_path / ".GIT"

    if git_file.is_file():
        try:
            git_content = git_file.read_text().strip()
            if git_content.startswith("gitdir:"):
                gitdir = Path(git_content.split(":", 1)[1].strip())
                # Navigate: .git/worktrees/name -> .git -> main repo root
                main_git_dir = gitdir.parent.parent
                main_repo_root = main_git_dir.parent
                return main_repo_root
        except (OSError, ValueError):
            pass

    return current_path


def x_get_main_repo_root__mutmut_5(current_path: Path) -> Path:
    """
    Get the main repository root, even if called from a worktree.

    When in a worktree, .git is a file pointing to the main repo's .git directory.
    This function follows that pointer to find the main repo root.

    Args:
        current_path: Current repo root (may be worktree or main repo)

    Returns:
        Path to the main repository root (resolves worktree pointers)

    Examples:
        >>> # From main repo - returns same path
        >>> get_main_repo_root(Path("/repo"))
        Path('/repo')

        >>> # From worktree - returns main repo
        >>> get_main_repo_root(Path("/repo/.worktrees/feature-001"))
        Path('/repo')
    """
    git_file = current_path / ".git"

    if git_file.is_file():
        try:
            git_content = None
            if git_content.startswith("gitdir:"):
                gitdir = Path(git_content.split(":", 1)[1].strip())
                # Navigate: .git/worktrees/name -> .git -> main repo root
                main_git_dir = gitdir.parent.parent
                main_repo_root = main_git_dir.parent
                return main_repo_root
        except (OSError, ValueError):
            pass

    return current_path


def x_get_main_repo_root__mutmut_6(current_path: Path) -> Path:
    """
    Get the main repository root, even if called from a worktree.

    When in a worktree, .git is a file pointing to the main repo's .git directory.
    This function follows that pointer to find the main repo root.

    Args:
        current_path: Current repo root (may be worktree or main repo)

    Returns:
        Path to the main repository root (resolves worktree pointers)

    Examples:
        >>> # From main repo - returns same path
        >>> get_main_repo_root(Path("/repo"))
        Path('/repo')

        >>> # From worktree - returns main repo
        >>> get_main_repo_root(Path("/repo/.worktrees/feature-001"))
        Path('/repo')
    """
    git_file = current_path / ".git"

    if git_file.is_file():
        try:
            git_content = git_file.read_text().strip()
            if git_content.startswith(None):
                gitdir = Path(git_content.split(":", 1)[1].strip())
                # Navigate: .git/worktrees/name -> .git -> main repo root
                main_git_dir = gitdir.parent.parent
                main_repo_root = main_git_dir.parent
                return main_repo_root
        except (OSError, ValueError):
            pass

    return current_path


def x_get_main_repo_root__mutmut_7(current_path: Path) -> Path:
    """
    Get the main repository root, even if called from a worktree.

    When in a worktree, .git is a file pointing to the main repo's .git directory.
    This function follows that pointer to find the main repo root.

    Args:
        current_path: Current repo root (may be worktree or main repo)

    Returns:
        Path to the main repository root (resolves worktree pointers)

    Examples:
        >>> # From main repo - returns same path
        >>> get_main_repo_root(Path("/repo"))
        Path('/repo')

        >>> # From worktree - returns main repo
        >>> get_main_repo_root(Path("/repo/.worktrees/feature-001"))
        Path('/repo')
    """
    git_file = current_path / ".git"

    if git_file.is_file():
        try:
            git_content = git_file.read_text().strip()
            if git_content.startswith("XXgitdir:XX"):
                gitdir = Path(git_content.split(":", 1)[1].strip())
                # Navigate: .git/worktrees/name -> .git -> main repo root
                main_git_dir = gitdir.parent.parent
                main_repo_root = main_git_dir.parent
                return main_repo_root
        except (OSError, ValueError):
            pass

    return current_path


def x_get_main_repo_root__mutmut_8(current_path: Path) -> Path:
    """
    Get the main repository root, even if called from a worktree.

    When in a worktree, .git is a file pointing to the main repo's .git directory.
    This function follows that pointer to find the main repo root.

    Args:
        current_path: Current repo root (may be worktree or main repo)

    Returns:
        Path to the main repository root (resolves worktree pointers)

    Examples:
        >>> # From main repo - returns same path
        >>> get_main_repo_root(Path("/repo"))
        Path('/repo')

        >>> # From worktree - returns main repo
        >>> get_main_repo_root(Path("/repo/.worktrees/feature-001"))
        Path('/repo')
    """
    git_file = current_path / ".git"

    if git_file.is_file():
        try:
            git_content = git_file.read_text().strip()
            if git_content.startswith("GITDIR:"):
                gitdir = Path(git_content.split(":", 1)[1].strip())
                # Navigate: .git/worktrees/name -> .git -> main repo root
                main_git_dir = gitdir.parent.parent
                main_repo_root = main_git_dir.parent
                return main_repo_root
        except (OSError, ValueError):
            pass

    return current_path


def x_get_main_repo_root__mutmut_9(current_path: Path) -> Path:
    """
    Get the main repository root, even if called from a worktree.

    When in a worktree, .git is a file pointing to the main repo's .git directory.
    This function follows that pointer to find the main repo root.

    Args:
        current_path: Current repo root (may be worktree or main repo)

    Returns:
        Path to the main repository root (resolves worktree pointers)

    Examples:
        >>> # From main repo - returns same path
        >>> get_main_repo_root(Path("/repo"))
        Path('/repo')

        >>> # From worktree - returns main repo
        >>> get_main_repo_root(Path("/repo/.worktrees/feature-001"))
        Path('/repo')
    """
    git_file = current_path / ".git"

    if git_file.is_file():
        try:
            git_content = git_file.read_text().strip()
            if git_content.startswith("gitdir:"):
                gitdir = None
                # Navigate: .git/worktrees/name -> .git -> main repo root
                main_git_dir = gitdir.parent.parent
                main_repo_root = main_git_dir.parent
                return main_repo_root
        except (OSError, ValueError):
            pass

    return current_path


def x_get_main_repo_root__mutmut_10(current_path: Path) -> Path:
    """
    Get the main repository root, even if called from a worktree.

    When in a worktree, .git is a file pointing to the main repo's .git directory.
    This function follows that pointer to find the main repo root.

    Args:
        current_path: Current repo root (may be worktree or main repo)

    Returns:
        Path to the main repository root (resolves worktree pointers)

    Examples:
        >>> # From main repo - returns same path
        >>> get_main_repo_root(Path("/repo"))
        Path('/repo')

        >>> # From worktree - returns main repo
        >>> get_main_repo_root(Path("/repo/.worktrees/feature-001"))
        Path('/repo')
    """
    git_file = current_path / ".git"

    if git_file.is_file():
        try:
            git_content = git_file.read_text().strip()
            if git_content.startswith("gitdir:"):
                gitdir = Path(None)
                # Navigate: .git/worktrees/name -> .git -> main repo root
                main_git_dir = gitdir.parent.parent
                main_repo_root = main_git_dir.parent
                return main_repo_root
        except (OSError, ValueError):
            pass

    return current_path


def x_get_main_repo_root__mutmut_11(current_path: Path) -> Path:
    """
    Get the main repository root, even if called from a worktree.

    When in a worktree, .git is a file pointing to the main repo's .git directory.
    This function follows that pointer to find the main repo root.

    Args:
        current_path: Current repo root (may be worktree or main repo)

    Returns:
        Path to the main repository root (resolves worktree pointers)

    Examples:
        >>> # From main repo - returns same path
        >>> get_main_repo_root(Path("/repo"))
        Path('/repo')

        >>> # From worktree - returns main repo
        >>> get_main_repo_root(Path("/repo/.worktrees/feature-001"))
        Path('/repo')
    """
    git_file = current_path / ".git"

    if git_file.is_file():
        try:
            git_content = git_file.read_text().strip()
            if git_content.startswith("gitdir:"):
                gitdir = Path(git_content.split(None, 1)[1].strip())
                # Navigate: .git/worktrees/name -> .git -> main repo root
                main_git_dir = gitdir.parent.parent
                main_repo_root = main_git_dir.parent
                return main_repo_root
        except (OSError, ValueError):
            pass

    return current_path


def x_get_main_repo_root__mutmut_12(current_path: Path) -> Path:
    """
    Get the main repository root, even if called from a worktree.

    When in a worktree, .git is a file pointing to the main repo's .git directory.
    This function follows that pointer to find the main repo root.

    Args:
        current_path: Current repo root (may be worktree or main repo)

    Returns:
        Path to the main repository root (resolves worktree pointers)

    Examples:
        >>> # From main repo - returns same path
        >>> get_main_repo_root(Path("/repo"))
        Path('/repo')

        >>> # From worktree - returns main repo
        >>> get_main_repo_root(Path("/repo/.worktrees/feature-001"))
        Path('/repo')
    """
    git_file = current_path / ".git"

    if git_file.is_file():
        try:
            git_content = git_file.read_text().strip()
            if git_content.startswith("gitdir:"):
                gitdir = Path(git_content.split(":", None)[1].strip())
                # Navigate: .git/worktrees/name -> .git -> main repo root
                main_git_dir = gitdir.parent.parent
                main_repo_root = main_git_dir.parent
                return main_repo_root
        except (OSError, ValueError):
            pass

    return current_path


def x_get_main_repo_root__mutmut_13(current_path: Path) -> Path:
    """
    Get the main repository root, even if called from a worktree.

    When in a worktree, .git is a file pointing to the main repo's .git directory.
    This function follows that pointer to find the main repo root.

    Args:
        current_path: Current repo root (may be worktree or main repo)

    Returns:
        Path to the main repository root (resolves worktree pointers)

    Examples:
        >>> # From main repo - returns same path
        >>> get_main_repo_root(Path("/repo"))
        Path('/repo')

        >>> # From worktree - returns main repo
        >>> get_main_repo_root(Path("/repo/.worktrees/feature-001"))
        Path('/repo')
    """
    git_file = current_path / ".git"

    if git_file.is_file():
        try:
            git_content = git_file.read_text().strip()
            if git_content.startswith("gitdir:"):
                gitdir = Path(git_content.split(1)[1].strip())
                # Navigate: .git/worktrees/name -> .git -> main repo root
                main_git_dir = gitdir.parent.parent
                main_repo_root = main_git_dir.parent
                return main_repo_root
        except (OSError, ValueError):
            pass

    return current_path


def x_get_main_repo_root__mutmut_14(current_path: Path) -> Path:
    """
    Get the main repository root, even if called from a worktree.

    When in a worktree, .git is a file pointing to the main repo's .git directory.
    This function follows that pointer to find the main repo root.

    Args:
        current_path: Current repo root (may be worktree or main repo)

    Returns:
        Path to the main repository root (resolves worktree pointers)

    Examples:
        >>> # From main repo - returns same path
        >>> get_main_repo_root(Path("/repo"))
        Path('/repo')

        >>> # From worktree - returns main repo
        >>> get_main_repo_root(Path("/repo/.worktrees/feature-001"))
        Path('/repo')
    """
    git_file = current_path / ".git"

    if git_file.is_file():
        try:
            git_content = git_file.read_text().strip()
            if git_content.startswith("gitdir:"):
                gitdir = Path(git_content.split(":", )[1].strip())
                # Navigate: .git/worktrees/name -> .git -> main repo root
                main_git_dir = gitdir.parent.parent
                main_repo_root = main_git_dir.parent
                return main_repo_root
        except (OSError, ValueError):
            pass

    return current_path


def x_get_main_repo_root__mutmut_15(current_path: Path) -> Path:
    """
    Get the main repository root, even if called from a worktree.

    When in a worktree, .git is a file pointing to the main repo's .git directory.
    This function follows that pointer to find the main repo root.

    Args:
        current_path: Current repo root (may be worktree or main repo)

    Returns:
        Path to the main repository root (resolves worktree pointers)

    Examples:
        >>> # From main repo - returns same path
        >>> get_main_repo_root(Path("/repo"))
        Path('/repo')

        >>> # From worktree - returns main repo
        >>> get_main_repo_root(Path("/repo/.worktrees/feature-001"))
        Path('/repo')
    """
    git_file = current_path / ".git"

    if git_file.is_file():
        try:
            git_content = git_file.read_text().strip()
            if git_content.startswith("gitdir:"):
                gitdir = Path(git_content.rsplit(":", 1)[1].strip())
                # Navigate: .git/worktrees/name -> .git -> main repo root
                main_git_dir = gitdir.parent.parent
                main_repo_root = main_git_dir.parent
                return main_repo_root
        except (OSError, ValueError):
            pass

    return current_path


def x_get_main_repo_root__mutmut_16(current_path: Path) -> Path:
    """
    Get the main repository root, even if called from a worktree.

    When in a worktree, .git is a file pointing to the main repo's .git directory.
    This function follows that pointer to find the main repo root.

    Args:
        current_path: Current repo root (may be worktree or main repo)

    Returns:
        Path to the main repository root (resolves worktree pointers)

    Examples:
        >>> # From main repo - returns same path
        >>> get_main_repo_root(Path("/repo"))
        Path('/repo')

        >>> # From worktree - returns main repo
        >>> get_main_repo_root(Path("/repo/.worktrees/feature-001"))
        Path('/repo')
    """
    git_file = current_path / ".git"

    if git_file.is_file():
        try:
            git_content = git_file.read_text().strip()
            if git_content.startswith("gitdir:"):
                gitdir = Path(git_content.split("XX:XX", 1)[1].strip())
                # Navigate: .git/worktrees/name -> .git -> main repo root
                main_git_dir = gitdir.parent.parent
                main_repo_root = main_git_dir.parent
                return main_repo_root
        except (OSError, ValueError):
            pass

    return current_path


def x_get_main_repo_root__mutmut_17(current_path: Path) -> Path:
    """
    Get the main repository root, even if called from a worktree.

    When in a worktree, .git is a file pointing to the main repo's .git directory.
    This function follows that pointer to find the main repo root.

    Args:
        current_path: Current repo root (may be worktree or main repo)

    Returns:
        Path to the main repository root (resolves worktree pointers)

    Examples:
        >>> # From main repo - returns same path
        >>> get_main_repo_root(Path("/repo"))
        Path('/repo')

        >>> # From worktree - returns main repo
        >>> get_main_repo_root(Path("/repo/.worktrees/feature-001"))
        Path('/repo')
    """
    git_file = current_path / ".git"

    if git_file.is_file():
        try:
            git_content = git_file.read_text().strip()
            if git_content.startswith("gitdir:"):
                gitdir = Path(git_content.split(":", 2)[1].strip())
                # Navigate: .git/worktrees/name -> .git -> main repo root
                main_git_dir = gitdir.parent.parent
                main_repo_root = main_git_dir.parent
                return main_repo_root
        except (OSError, ValueError):
            pass

    return current_path


def x_get_main_repo_root__mutmut_18(current_path: Path) -> Path:
    """
    Get the main repository root, even if called from a worktree.

    When in a worktree, .git is a file pointing to the main repo's .git directory.
    This function follows that pointer to find the main repo root.

    Args:
        current_path: Current repo root (may be worktree or main repo)

    Returns:
        Path to the main repository root (resolves worktree pointers)

    Examples:
        >>> # From main repo - returns same path
        >>> get_main_repo_root(Path("/repo"))
        Path('/repo')

        >>> # From worktree - returns main repo
        >>> get_main_repo_root(Path("/repo/.worktrees/feature-001"))
        Path('/repo')
    """
    git_file = current_path / ".git"

    if git_file.is_file():
        try:
            git_content = git_file.read_text().strip()
            if git_content.startswith("gitdir:"):
                gitdir = Path(git_content.split(":", 1)[2].strip())
                # Navigate: .git/worktrees/name -> .git -> main repo root
                main_git_dir = gitdir.parent.parent
                main_repo_root = main_git_dir.parent
                return main_repo_root
        except (OSError, ValueError):
            pass

    return current_path


def x_get_main_repo_root__mutmut_19(current_path: Path) -> Path:
    """
    Get the main repository root, even if called from a worktree.

    When in a worktree, .git is a file pointing to the main repo's .git directory.
    This function follows that pointer to find the main repo root.

    Args:
        current_path: Current repo root (may be worktree or main repo)

    Returns:
        Path to the main repository root (resolves worktree pointers)

    Examples:
        >>> # From main repo - returns same path
        >>> get_main_repo_root(Path("/repo"))
        Path('/repo')

        >>> # From worktree - returns main repo
        >>> get_main_repo_root(Path("/repo/.worktrees/feature-001"))
        Path('/repo')
    """
    git_file = current_path / ".git"

    if git_file.is_file():
        try:
            git_content = git_file.read_text().strip()
            if git_content.startswith("gitdir:"):
                gitdir = Path(git_content.split(":", 1)[1].strip())
                # Navigate: .git/worktrees/name -> .git -> main repo root
                main_git_dir = None
                main_repo_root = main_git_dir.parent
                return main_repo_root
        except (OSError, ValueError):
            pass

    return current_path


def x_get_main_repo_root__mutmut_20(current_path: Path) -> Path:
    """
    Get the main repository root, even if called from a worktree.

    When in a worktree, .git is a file pointing to the main repo's .git directory.
    This function follows that pointer to find the main repo root.

    Args:
        current_path: Current repo root (may be worktree or main repo)

    Returns:
        Path to the main repository root (resolves worktree pointers)

    Examples:
        >>> # From main repo - returns same path
        >>> get_main_repo_root(Path("/repo"))
        Path('/repo')

        >>> # From worktree - returns main repo
        >>> get_main_repo_root(Path("/repo/.worktrees/feature-001"))
        Path('/repo')
    """
    git_file = current_path / ".git"

    if git_file.is_file():
        try:
            git_content = git_file.read_text().strip()
            if git_content.startswith("gitdir:"):
                gitdir = Path(git_content.split(":", 1)[1].strip())
                # Navigate: .git/worktrees/name -> .git -> main repo root
                main_git_dir = gitdir.parent.parent
                main_repo_root = None
                return main_repo_root
        except (OSError, ValueError):
            pass

    return current_path

x_get_main_repo_root__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_get_main_repo_root__mutmut_1': x_get_main_repo_root__mutmut_1, 
    'x_get_main_repo_root__mutmut_2': x_get_main_repo_root__mutmut_2, 
    'x_get_main_repo_root__mutmut_3': x_get_main_repo_root__mutmut_3, 
    'x_get_main_repo_root__mutmut_4': x_get_main_repo_root__mutmut_4, 
    'x_get_main_repo_root__mutmut_5': x_get_main_repo_root__mutmut_5, 
    'x_get_main_repo_root__mutmut_6': x_get_main_repo_root__mutmut_6, 
    'x_get_main_repo_root__mutmut_7': x_get_main_repo_root__mutmut_7, 
    'x_get_main_repo_root__mutmut_8': x_get_main_repo_root__mutmut_8, 
    'x_get_main_repo_root__mutmut_9': x_get_main_repo_root__mutmut_9, 
    'x_get_main_repo_root__mutmut_10': x_get_main_repo_root__mutmut_10, 
    'x_get_main_repo_root__mutmut_11': x_get_main_repo_root__mutmut_11, 
    'x_get_main_repo_root__mutmut_12': x_get_main_repo_root__mutmut_12, 
    'x_get_main_repo_root__mutmut_13': x_get_main_repo_root__mutmut_13, 
    'x_get_main_repo_root__mutmut_14': x_get_main_repo_root__mutmut_14, 
    'x_get_main_repo_root__mutmut_15': x_get_main_repo_root__mutmut_15, 
    'x_get_main_repo_root__mutmut_16': x_get_main_repo_root__mutmut_16, 
    'x_get_main_repo_root__mutmut_17': x_get_main_repo_root__mutmut_17, 
    'x_get_main_repo_root__mutmut_18': x_get_main_repo_root__mutmut_18, 
    'x_get_main_repo_root__mutmut_19': x_get_main_repo_root__mutmut_19, 
    'x_get_main_repo_root__mutmut_20': x_get_main_repo_root__mutmut_20
}
x_get_main_repo_root__mutmut_orig.__name__ = 'x_get_main_repo_root'


# DEPRECATED: find_feature_slug() has been removed
# Use detect_feature_slug() from specify_cli.core.feature_detection instead
#
# Migration:
#   from specify_cli.core.feature_detection import detect_feature_slug
#   slug = detect_feature_slug(repo_root)
#
# The new centralized implementation provides:
# - Deterministic behavior (no "highest numbered" guessing)
# - Explicit error messages guiding users to --feature flag
# - Consistent behavior across all commands


__all__ = [
    "locate_project_root",
    "is_worktree_context",
    "resolve_with_context",
    "check_broken_symlink",
    "get_main_repo_root",
    # find_feature_slug has been removed - use detect_feature_slug from core.feature_detection
]
