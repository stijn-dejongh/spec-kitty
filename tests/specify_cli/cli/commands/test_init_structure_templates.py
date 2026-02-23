"""Tests for optional structure template generation during init."""

from __future__ import annotations

from pathlib import Path

from rich.console import Console

from specify_cli.cli.commands import init as init_module


class _MemoryConsole(Console):
    def __init__(self) -> None:
        super().__init__(force_terminal=False, width=120)


def test_skips_generation_in_non_interactive(tmp_path: Path, monkeypatch) -> None:
    structure_dir = tmp_path / "structure"
    structure_dir.mkdir()
    (structure_dir / "REPO_MAP.md").write_text("repo", encoding="utf-8")
    (structure_dir / "SURFACES.md").write_text("surfaces", encoding="utf-8")

    monkeypatch.setattr(init_module, "_get_structure_templates_dir", lambda: structure_dir)

    init_module._maybe_generate_structure_templates(tmp_path, non_interactive=True, console=_MemoryConsole())

    assert not (tmp_path / "REPO_MAP.md").exists()
    assert not (tmp_path / "SURFACES.md").exists()


def test_generates_templates_when_user_accepts(tmp_path: Path, monkeypatch) -> None:
    structure_dir = tmp_path / "structure"
    structure_dir.mkdir()
    (structure_dir / "REPO_MAP.md").write_text("repo-template", encoding="utf-8")
    (structure_dir / "SURFACES.md").write_text("surface-template", encoding="utf-8")

    monkeypatch.setattr(init_module, "_get_structure_templates_dir", lambda: structure_dir)
    monkeypatch.setattr(init_module.typer, "confirm", lambda *args, **kwargs: True)

    init_module._maybe_generate_structure_templates(tmp_path, non_interactive=False, console=_MemoryConsole())

    assert (tmp_path / "REPO_MAP.md").read_text(encoding="utf-8") == "repo-template"
    assert (tmp_path / "SURFACES.md").read_text(encoding="utf-8") == "surface-template"


def test_respects_existing_files(tmp_path: Path, monkeypatch) -> None:
    structure_dir = tmp_path / "structure"
    structure_dir.mkdir()
    (structure_dir / "REPO_MAP.md").write_text("repo-template", encoding="utf-8")
    (structure_dir / "SURFACES.md").write_text("surface-template", encoding="utf-8")

    (tmp_path / "REPO_MAP.md").write_text("existing", encoding="utf-8")

    monkeypatch.setattr(init_module, "_get_structure_templates_dir", lambda: structure_dir)
    monkeypatch.setattr(init_module.typer, "confirm", lambda *args, **kwargs: True)

    init_module._maybe_generate_structure_templates(tmp_path, non_interactive=False, console=_MemoryConsole())

    assert (tmp_path / "REPO_MAP.md").read_text(encoding="utf-8") == "existing"
    assert (tmp_path / "SURFACES.md").read_text(encoding="utf-8") == "surface-template"
