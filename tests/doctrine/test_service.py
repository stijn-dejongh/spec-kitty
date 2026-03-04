"""Tests for DoctrineService lazy aggregation behavior."""

from __future__ import annotations

from pathlib import Path

from ruamel.yaml import YAML

from doctrine.service import DoctrineService


def _write_yaml(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    yaml = YAML()
    yaml.default_flow_style = False
    with path.open("w", encoding="utf-8") as handle:
        yaml.dump(data, handle)


def test_service_loads_all_repositories_from_shipped_defaults() -> None:
    service = DoctrineService()

    assert service.directives.list_all()
    assert service.tactics.get("zombies-tdd") is not None
    assert service.styleguides.get("kitty-glossary-writing") is not None
    assert service.toolguides.get("powershell-syntax") is not None
    assert service.paradigms.get("test-first") is not None
    assert service.agent_profiles.get("implementer") is not None


def test_service_repositories_are_lazily_cached() -> None:
    service = DoctrineService()
    assert service._cache == {}

    first_directives = service.directives
    assert "directives" in service._cache
    assert "tactics" not in service._cache

    second_directives = service.directives
    assert first_directives is second_directives

    _ = service.tactics
    assert "tactics" in service._cache


def test_service_honors_custom_shipped_and_project_roots(tmp_path: Path) -> None:
    shipped_root = tmp_path / "shipped-root"
    project_root = tmp_path / "project-root"

    shipped_directive = {
        "schema_version": "1.0",
        "id": "DIRECTIVE_CUSTOM",
        "title": "Base Directive",
        "intent": "Base intent.",
        "enforcement": "required",
    }
    project_override = {
        "schema_version": "1.0",
        "id": "DIRECTIVE_CUSTOM",
        "title": "Overridden Directive",
        "intent": "Overridden intent.",
        "enforcement": "advisory",
    }

    _write_yaml(
        shipped_root / "directives" / "shipped" / "001-custom.directive.yaml",
        shipped_directive,
    )
    _write_yaml(
        project_root / "directives" / "custom.directive.yaml",
        project_override,
    )

    service = DoctrineService(shipped_root=shipped_root, project_root=project_root)
    directive = service.directives.get("DIRECTIVE_CUSTOM")
    assert directive is not None
    assert directive.title == "Overridden Directive"
    assert directive.enforcement.value == "advisory"


def test_service_resolves_directive_tactic_refs_across_repositories() -> None:
    service = DoctrineService()
    directive = service.directives.get("TEST_FIRST")
    assert directive is not None
    assert directive.tactic_refs

    for tactic_id in directive.tactic_refs:
        assert service.tactics.get(tactic_id) is not None

