"""Tests for doctrine catalog loading."""

from __future__ import annotations

from pathlib import Path

import specify_cli.constitution.catalog as catalog_module
from specify_cli.constitution.catalog import (
    _load_yaml_id_catalog,
    _load_yaml_id_catalog_with_presence,
    load_doctrine_catalog,
)


def test_catalog_loads_packaged_directives() -> None:
    catalog = load_doctrine_catalog()
    assert len(catalog.directives) > 0, "Expected at least one directive"


def test_catalog_includes_mission_template_sets() -> None:
    catalog = load_doctrine_catalog()
    assert "software-dev-default" in catalog.template_sets


def test_catalog_has_expanded_fields() -> None:
    catalog = load_doctrine_catalog()
    assert isinstance(catalog.tactics, frozenset)
    assert isinstance(catalog.styleguides, frozenset)
    assert isinstance(catalog.toolguides, frozenset)
    assert isinstance(catalog.procedures, frozenset)
    assert isinstance(catalog.agent_profiles, frozenset)


def test_catalog_loads_agent_profiles() -> None:
    catalog = load_doctrine_catalog()
    assert len(catalog.agent_profiles) > 0, "Expected at least one agent profile"
    assert "architect" in catalog.agent_profiles


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
        "agent_profiles",
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
    subdir = tmp_path / "nested"
    subdir.mkdir()
    (subdir / "nested.tactic.yaml").write_text("id: nested-tactic\n")
    result = _load_yaml_id_catalog(tmp_path, "**/*.tactic.yaml")
    assert "nested-tactic" in result


def test_load_yaml_id_catalog_prefers_shipped_only_when_structure_exists(tmp_path: Path) -> None:
    shipped = tmp_path / "shipped"
    proposed = tmp_path / "_proposed"
    shipped.mkdir()
    proposed.mkdir()
    (shipped / "stable.tactic.yaml").write_text("id: stable-tactic\n")
    (proposed / "candidate.tactic.yaml").write_text("id: candidate-tactic\n")

    result = _load_yaml_id_catalog(tmp_path, "*.tactic.yaml")

    assert result == {"stable-tactic"}


def test_load_yaml_id_catalog_can_include_proposed_when_requested(tmp_path: Path) -> None:
    shipped = tmp_path / "shipped"
    proposed = tmp_path / "_proposed"
    shipped.mkdir()
    proposed.mkdir()
    (shipped / "stable.tactic.yaml").write_text("id: stable-tactic\n")
    (proposed / "candidate.tactic.yaml").write_text("id: candidate-tactic\n")

    result = _load_yaml_id_catalog(tmp_path, "*.tactic.yaml", include_proposed=True)

    assert result == {"stable-tactic", "candidate-tactic"}


def test_load_doctrine_catalog_excludes_proposed_by_default(tmp_path: Path, monkeypatch) -> None:
    doctrine_root = tmp_path / "doctrine"
    (doctrine_root / "directives" / "shipped").mkdir(parents=True)
    (doctrine_root / "directives" / "_proposed").mkdir(parents=True)
    (doctrine_root / "directives" / "shipped" / "stable.directive.yaml").write_text("id: stable-directive\n")
    (doctrine_root / "directives" / "_proposed" / "candidate.directive.yaml").write_text("id: candidate-directive\n")
    (doctrine_root / "agent_profiles" / "shipped").mkdir(parents=True)
    (doctrine_root / "agent_profiles" / "shipped" / "reviewer.agent.yaml").write_text(
        "profile-id: reviewer\nname: Reviewer\n"
    )
    (doctrine_root / "missions" / "software-dev").mkdir(parents=True)
    (doctrine_root / "missions" / "software-dev" / "mission.yaml").write_text("name: software-dev\n")

    monkeypatch.setattr(catalog_module, "resolve_doctrine_root", lambda: doctrine_root)

    catalog = load_doctrine_catalog()

    assert catalog.directives == frozenset({"stable-directive"})


def test_load_doctrine_catalog_can_include_proposed(tmp_path: Path, monkeypatch) -> None:
    doctrine_root = tmp_path / "doctrine"
    (doctrine_root / "directives" / "shipped").mkdir(parents=True)
    (doctrine_root / "directives" / "_proposed").mkdir(parents=True)
    (doctrine_root / "directives" / "shipped" / "stable.directive.yaml").write_text("id: stable-directive\n")
    (doctrine_root / "directives" / "_proposed" / "candidate.directive.yaml").write_text("id: candidate-directive\n")
    (doctrine_root / "agent_profiles" / "shipped").mkdir(parents=True)
    (doctrine_root / "agent_profiles" / "shipped" / "reviewer.agent.yaml").write_text(
        "profile-id: reviewer\nname: Reviewer\n"
    )
    (doctrine_root / "missions" / "software-dev").mkdir(parents=True)
    (doctrine_root / "missions" / "software-dev" / "mission.yaml").write_text("name: software-dev\n")

    monkeypatch.setattr(catalog_module, "resolve_doctrine_root", lambda: doctrine_root)

    catalog = load_doctrine_catalog(include_proposed=True)

    assert catalog.directives == frozenset({"candidate-directive", "stable-directive"})


def test_doctrine_catalog_is_hashable() -> None:
    catalog = load_doctrine_catalog()
    _ = hash(catalog)


# ---------------------------------------------------------------------------
# T017: Regression tests — shipped-only scan, _proposed opt-in, domains_present
# ---------------------------------------------------------------------------


def test_load_yaml_id_catalog_with_presence_returns_false_when_dir_missing(tmp_path: Path) -> None:
    """Domain absent from filesystem → present=False (skip validation, not fail)."""
    ids, present = _load_yaml_id_catalog_with_presence(tmp_path / "nonexistent", "*.yaml")
    assert present is False
    assert ids == set()


def test_load_yaml_id_catalog_with_presence_returns_true_when_shipped_dir_exists(tmp_path: Path) -> None:
    """shipped/ directory exists but is empty → present=True, ids=empty (all selections invalid)."""
    (tmp_path / "shipped").mkdir()
    ids, present = _load_yaml_id_catalog_with_presence(tmp_path, "*.yaml")
    assert present is True
    assert ids == set()


def test_load_yaml_id_catalog_with_presence_returns_true_when_proposed_dir_exists(tmp_path: Path) -> None:
    """_proposed/ directory exists (shipped missing) → present=True."""
    (tmp_path / "_proposed").mkdir()
    ids, present = _load_yaml_id_catalog_with_presence(tmp_path, "*.yaml")
    assert present is True
    assert ids == set()


def test_shipped_only_scan_excludes_proposed_by_default(tmp_path: Path) -> None:
    """Default scan reads shipped/ only, ignoring _proposed/ content."""
    shipped = tmp_path / "shipped"
    proposed = tmp_path / "_proposed"
    shipped.mkdir()
    proposed.mkdir()
    (shipped / "a.tactic.yaml").write_text("id: shipped-a\n")
    (proposed / "b.tactic.yaml").write_text("id: proposed-b\n")

    ids, present = _load_yaml_id_catalog_with_presence(tmp_path, "*.tactic.yaml")

    assert present is True
    assert ids == {"shipped-a"}
    assert "proposed-b" not in ids


def test_explicit_proposed_opt_in_includes_proposed_artifacts(tmp_path: Path) -> None:
    """include_proposed=True adds _proposed/ artifacts on top of shipped/."""
    shipped = tmp_path / "shipped"
    proposed = tmp_path / "_proposed"
    shipped.mkdir()
    proposed.mkdir()
    (shipped / "a.tactic.yaml").write_text("id: shipped-a\n")
    (proposed / "b.tactic.yaml").write_text("id: proposed-b\n")

    ids, present = _load_yaml_id_catalog_with_presence(
        tmp_path, "*.tactic.yaml", include_proposed=True
    )

    assert present is True
    assert ids == {"shipped-a", "proposed-b"}


def test_doctrine_catalog_domains_present_tracks_shipped_dirs(
    tmp_path: Path, monkeypatch
) -> None:
    """domains_present correctly records which artifact domains have shipped/ dirs."""
    doctrine_root = tmp_path / "doctrine"
    # paradigms: shipped dir present (but empty)
    (doctrine_root / "paradigms" / "shipped").mkdir(parents=True)
    # directives: flat layout (no shipped/ subdir)
    (doctrine_root / "directives").mkdir(parents=True)
    (doctrine_root / "directives" / "x.directive.yaml").write_text("id: x\n")
    # agent_profiles: missing entirely
    # missions: present with one mission
    (doctrine_root / "missions" / "software-dev").mkdir(parents=True)
    (doctrine_root / "missions" / "software-dev" / "mission.yaml").write_text("name: software-dev\n")

    monkeypatch.setattr(catalog_module, "resolve_doctrine_root", lambda: doctrine_root)

    catalog = load_doctrine_catalog()

    assert "paradigms" in catalog.domains_present
    assert "directives" in catalog.domains_present
    assert "template_sets" in catalog.domains_present
    assert "agent_profiles" not in catalog.domains_present  # agent_profiles dir missing


def test_doctrine_catalog_excludes_proposed_in_default_load(
    tmp_path: Path, monkeypatch
) -> None:
    """Default load_doctrine_catalog() does not include _proposed/ artifacts."""
    doctrine_root = tmp_path / "doctrine"
    (doctrine_root / "paradigms" / "shipped").mkdir(parents=True)
    (doctrine_root / "paradigms" / "_proposed").mkdir(parents=True)
    (doctrine_root / "paradigms" / "_proposed" / "candidate.paradigm.yaml").write_text(
        "id: candidate-paradigm\n"
    )
    (doctrine_root / "directives" / "shipped").mkdir(parents=True)
    (doctrine_root / "agent_profiles" / "shipped").mkdir(parents=True)
    (doctrine_root / "missions" / "software-dev").mkdir(parents=True)
    (doctrine_root / "missions" / "software-dev" / "mission.yaml").write_text("name: software-dev\n")

    monkeypatch.setattr(catalog_module, "resolve_doctrine_root", lambda: doctrine_root)

    catalog = load_doctrine_catalog()

    assert "candidate-paradigm" not in catalog.paradigms
    assert "paradigms" in catalog.domains_present  # domain IS present, just empty shipped set


def test_doctrine_catalog_includes_proposed_when_opted_in(
    tmp_path: Path, monkeypatch
) -> None:
    """include_proposed=True exposes _proposed/ artifacts."""
    doctrine_root = tmp_path / "doctrine"
    (doctrine_root / "paradigms" / "shipped").mkdir(parents=True)
    (doctrine_root / "paradigms" / "_proposed").mkdir(parents=True)
    (doctrine_root / "paradigms" / "_proposed" / "candidate.paradigm.yaml").write_text(
        "id: candidate-paradigm\n"
    )
    (doctrine_root / "directives" / "shipped").mkdir(parents=True)
    (doctrine_root / "agent_profiles" / "shipped").mkdir(parents=True)
    (doctrine_root / "missions" / "software-dev").mkdir(parents=True)
    (doctrine_root / "missions" / "software-dev" / "mission.yaml").write_text("name: software-dev\n")

    monkeypatch.setattr(catalog_module, "resolve_doctrine_root", lambda: doctrine_root)

    catalog = load_doctrine_catalog(include_proposed=True)

    assert "candidate-paradigm" in catalog.paradigms
