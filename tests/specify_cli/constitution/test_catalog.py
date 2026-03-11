"""Tests for doctrine catalog loading."""

from __future__ import annotations

from pathlib import Path

from specify_cli.constitution.catalog import _load_yaml_id_catalog, load_doctrine_catalog


def test_catalog_loads_packaged_directives_and_paradigms() -> None:
    catalog = load_doctrine_catalog()
    assert len(catalog.directives) > 0, "Expected at least one directive"
    assert "test-first" in catalog.paradigms


def test_catalog_includes_mission_template_sets() -> None:
    catalog = load_doctrine_catalog()
    assert "software-dev-default" in catalog.template_sets


def test_catalog_has_expanded_fields() -> None:
    catalog = load_doctrine_catalog()
    assert isinstance(catalog.tactics, frozenset)
    assert isinstance(catalog.styleguides, frozenset)
    assert isinstance(catalog.toolguides, frozenset)
    assert isinstance(catalog.procedures, frozenset)
    assert isinstance(catalog.profiles, frozenset)


def test_catalog_loads_agent_profiles() -> None:
    catalog = load_doctrine_catalog()
    assert len(catalog.profiles) > 0, "Expected at least one agent profile"
    assert "architect" in catalog.profiles


def test_catalog_loads_tactics() -> None:
    catalog = load_doctrine_catalog()
    assert len(catalog.tactics) > 0, "Expected at least one tactic"


def test_catalog_all_fields_are_frozensets() -> None:
    catalog = load_doctrine_catalog()
    for field_name in (
        "paradigms",
        "directives",
        "template_sets",
        "tactics",
        "styleguides",
        "toolguides",
        "procedures",
        "profiles",
    ):
        value = getattr(catalog, field_name)
        assert isinstance(value, frozenset), f"{field_name} should be frozenset, got {type(value)}"


def test_load_yaml_id_catalog_empty_dir(tmp_path: Path) -> None:
    result = _load_yaml_id_catalog(tmp_path, "*.yaml")
    assert result == set()


def test_load_yaml_id_catalog_nonexistent_dir(tmp_path: Path) -> None:
    result = _load_yaml_id_catalog(tmp_path / "nonexistent", "*.yaml")
    assert result == set()


def test_load_yaml_id_catalog_uses_id_field(tmp_path: Path) -> None:
    (tmp_path / "test.directive.yaml").write_text("id: my-directive\ntitle: Test\n")
    result = _load_yaml_id_catalog(tmp_path, "*.directive.yaml")
    assert "my-directive" in result


def test_load_yaml_id_catalog_custom_id_field(tmp_path: Path) -> None:
    (tmp_path / "reviewer.agent.yaml").write_text("profile-id: reviewer\nname: Reviewer\n")
    result = _load_yaml_id_catalog(tmp_path, "*.agent.yaml", id_field="profile-id")
    assert "reviewer" in result


def test_load_yaml_id_catalog_fallback_to_stem(tmp_path: Path) -> None:
    (tmp_path / "my-tactic.tactic.yaml").write_text("title: Something\n")
    result = _load_yaml_id_catalog(tmp_path, "*.tactic.yaml")
    assert "my-tactic" in result


def test_load_yaml_id_catalog_recursive(tmp_path: Path) -> None:
    subdir = tmp_path / "_proposed"
    subdir.mkdir()
    (subdir / "nested.tactic.yaml").write_text("id: nested-tactic\n")
    result = _load_yaml_id_catalog(tmp_path, "**/*.tactic.yaml")
    assert "nested-tactic" in result


def test_doctrine_catalog_is_hashable() -> None:
    catalog = load_doctrine_catalog()
    _ = hash(catalog)
