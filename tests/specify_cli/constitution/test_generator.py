"""Tests for deterministic constitution generator."""

from pathlib import Path

import pytest

from specify_cli.constitution.generator import build_constitution_draft, write_constitution


def test_build_constitution_draft_defaults() -> None:
    """Defaults fall back to full catalog when configured entries are absent from doctrine."""
    from specify_cli.constitution.catalog import load_doctrine_catalog

    catalog = load_doctrine_catalog()
    draft = build_constitution_draft(mission="software-dev")
    assert draft.template_set == "software-dev-default"
    # When configured mission-defaults are not present in the catalog, the compiler
    # falls back to the full set of available directives (sorted).
    assert draft.selected_directives == sorted(catalog.directives)
    # Paradigm fallback: empty when none are available in the catalog.
    assert draft.selected_paradigms == sorted(catalog.paradigms)
    assert "selected_directives" in draft.markdown


def test_build_constitution_draft_invalid_template_set_raises() -> None:
    with pytest.raises(ValueError):
        build_constitution_draft(mission="software-dev", template_set="not-real")


def test_write_constitution_respects_force(tmp_path: Path) -> None:
    path = tmp_path / "constitution.md"
    write_constitution(path, "# One", force=False)

    with pytest.raises(FileExistsError):
        write_constitution(path, "# Two", force=False)

    write_constitution(path, "# Two", force=True)
    assert path.read_text(encoding="utf-8") == "# Two"
