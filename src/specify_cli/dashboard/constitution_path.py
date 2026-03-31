"""Constitution path resolution helpers for dashboard features/API."""

from __future__ import annotations

from pathlib import Path

from kernel.paths import resolve_project_constitution_path as _resolve_project_constitution_path


def resolve_project_constitution_path(project_dir: Path) -> Path | None:
    """Resolve the project-level constitution file path."""
    return _resolve_project_constitution_path(project_dir)
