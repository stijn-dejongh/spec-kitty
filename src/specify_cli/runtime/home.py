"""Compatibility path resolution utilities for the runtime layer.

The canonical implementations live in ``kernel.paths``, but this module keeps
stable monkeypatch points for older tests and callers that still patch
``specify_cli.runtime.home`` directly.
"""

from __future__ import annotations

import importlib.resources
import os
import tempfile
from pathlib import Path

from kernel.paths import _is_windows as _kernel_is_windows


def _is_windows() -> bool:
    """Return True when running on Windows."""
    return _kernel_is_windows()


def get_kittify_home() -> Path:
    """Return the user-global runtime directory."""
    if env_home := os.environ.get("SPEC_KITTY_HOME"):
        return Path(env_home)

    if os.environ.get("SPEC_KITTY_TEST_MODE") == "1":
        return Path(tempfile.gettempdir()) / "spec-kitty-test-home"

    if _is_windows():
        from platformdirs import user_data_dir  # noqa: PLC0415

        return Path(user_data_dir("kittify"))

    return Path.home() / ".kittify"


def get_package_asset_root() -> Path:
    """Return the package's bundled missions directory."""
    if env_root := os.environ.get("SPEC_KITTY_TEMPLATE_ROOT"):
        root = Path(env_root)
        if root.is_dir():
            return root
        raise FileNotFoundError(f"SPEC_KITTY_TEMPLATE_ROOT path does not exist: {env_root}")

    try:
        doctrine_missions = Path(str(importlib.resources.files("doctrine") / "missions"))
        if doctrine_missions.is_dir():
            return doctrine_missions
    except (ModuleNotFoundError, TypeError):
        pass

    dev_root = Path(__file__).resolve().parents[2] / "doctrine" / "missions"
    if dev_root.is_dir():
        return dev_root

    raise FileNotFoundError(
        "Cannot locate package mission assets. Set SPEC_KITTY_TEMPLATE_ROOT or reinstall spec-kitty-cli."
    )


__all__ = ["_is_windows", "get_kittify_home", "get_package_asset_root"]
