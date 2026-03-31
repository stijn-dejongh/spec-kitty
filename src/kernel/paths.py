"""Cross-platform path resolution for the spec-kitty runtime.

Provides the canonical functions for locating:
- The user-global ~/.kittify/ directory (cross-platform)
- The package-bundled mission assets (for ensure_runtime to copy from)
- Project-local .kittify/constitution/ bundle paths

These functions have no spec-kitty-specific dependencies and are consumed
by multiple packages in the stack (specify_cli, constitution).  They live
in kernel so that neither package needs to import from the other.
"""

from __future__ import annotations

import importlib.resources
import os
import tempfile
from pathlib import Path


def _is_windows() -> bool:
    """Return True when running on Windows."""
    return os.name == "nt"


def get_kittify_home() -> Path:
    """Return the path to the user-global ~/.kittify/ directory.

    Resolution order:
    1. SPEC_KITTY_HOME environment variable (all platforms)
    2. ~/.kittify/ on macOS/Linux (Path.home() / ".kittify")
    3. %LOCALAPPDATA%\\kittify\\ on Windows (via platformdirs)

    Returns:
        Path: Absolute path to the global runtime directory.

    Raises:
        RuntimeError: If the home directory cannot be determined.
    """
    if env_home := os.environ.get("SPEC_KITTY_HOME"):
        return Path(env_home)

    if os.environ.get("SPEC_KITTY_TEST_MODE") == "1":
        return Path(tempfile.gettempdir()) / "spec-kitty-test-home"

    if _is_windows():
        # platformdirs is the only sanctioned third-party import in kernel/.
        # It is imported lazily here for Windows-only home directory resolution.
        # On Linux/macOS this branch is never executed. See architecture/2.x docs.
        from platformdirs import user_data_dir  # noqa: PLC0415

        return Path(user_data_dir("kittify"))

    return Path.home() / ".kittify"


def get_package_asset_root() -> Path:
    """Return the path to the package's bundled mission assets.

    Resolution order:
    1. SPEC_KITTY_TEMPLATE_ROOT environment variable (CI/testing)
    2. importlib.resources.files("doctrine") / "missions" (canonical location)

    Returns:
        Path: Absolute path to the missions directory in the doctrine package.

    Raises:
        FileNotFoundError: If no valid asset root can be found.
    """
    # CI/testing override
    if env_root := os.environ.get("SPEC_KITTY_TEMPLATE_ROOT"):
        root = Path(env_root)
        if root.is_dir():
            return root
        raise FileNotFoundError(f"SPEC_KITTY_TEMPLATE_ROOT path does not exist: {env_root}")

    # Canonical location: doctrine.missions
    try:
        doctrine_missions = Path(str(importlib.resources.files("doctrine") / "missions"))
        if doctrine_missions.is_dir():
            return doctrine_missions
    except (TypeError, ModuleNotFoundError):
        pass

    raise FileNotFoundError("Cannot locate package mission assets. Set SPEC_KITTY_TEMPLATE_ROOT or reinstall spec-kitty-cli.")


def get_project_kittify_dir(repo_root: Path) -> Path:
    """Return the project-local ``.kittify/`` directory for a repo root."""
    return Path(repo_root) / ".kittify"


def get_project_constitution_dir(repo_root: Path) -> Path:
    """Return the canonical project-local constitution bundle directory."""
    return get_project_kittify_dir(repo_root) / "constitution"


def get_project_constitution_path(repo_root: Path) -> Path:
    """Return the canonical project-local ``constitution.md`` path."""
    return get_project_constitution_dir(repo_root) / "constitution.md"


def get_project_constitution_references_path(repo_root: Path) -> Path:
    """Return the canonical project-local ``references.yaml`` path."""
    return get_project_constitution_dir(repo_root) / "references.yaml"


def get_project_constitution_interview_path(repo_root: Path) -> Path:
    """Return the canonical project-local constitution interview answers path."""
    return get_project_constitution_dir(repo_root) / "interview" / "answers.yaml"


def get_project_constitution_context_state_path(repo_root: Path) -> Path:
    """Return the canonical project-local constitution context state path."""
    return get_project_constitution_dir(repo_root) / "context-state.json"


def get_project_constitution_agents_dir(repo_root: Path) -> Path:
    """Return the canonical project-local constitution agents directory."""
    return get_project_constitution_dir(repo_root) / "agents"


def resolve_project_constitution_path(repo_root: Path) -> Path | None:
    """Resolve the project constitution path, preferring canonical over legacy."""
    canonical = get_project_constitution_path(repo_root)
    if canonical.exists():
        return canonical

    legacy = get_project_kittify_dir(repo_root) / "memory" / "constitution.md"
    if legacy.exists():
        return legacy

    return None


__all__ = [
    "get_kittify_home",
    "get_package_asset_root",
    "get_project_kittify_dir",
    "get_project_constitution_dir",
    "get_project_constitution_path",
    "get_project_constitution_references_path",
    "get_project_constitution_interview_path",
    "get_project_constitution_context_state_path",
    "get_project_constitution_agents_dir",
    "resolve_project_constitution_path",
]
