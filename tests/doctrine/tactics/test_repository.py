"""Unit tests for TacticRepository."""

from pathlib import Path

import pytest
from ruamel.yaml import YAML

from doctrine.tactics.repository import TacticRepository


class TestTacticRepository:
    def test_list_all_from_shipped(self) -> None:
        """Acceptance: list_all returns all shipped tactics."""
        repo = TacticRepository()
        tactics = repo.list_all()
        assert len(tactics) >= 4

    def test_get_by_id(self) -> None:
        """get() with kebab-case ID returns the tactic."""
        repo = TacticRepository()
        tactic = repo.get("zombies-tdd")
        assert tactic is not None
        assert tactic.name == "ZOMBIES TDD"
        assert len(tactic.steps) == 7

    def test_get_returns_none_for_unknown(self) -> None:
        repo = TacticRepository()
        assert repo.get("nonexistent-tactic") is None

    def test_load_from_custom_shipped_dir(self, tmp_tactic_dir: Path) -> None:
        repo = TacticRepository(shipped_dir=tmp_tactic_dir)
        tactics = repo.list_all()
        assert len(tactics) == 1
        assert tactics[0].id == "test-tactic"

    def test_malformed_yaml_skipped_with_warning(self, tmp_path: Path) -> None:
        """Malformed YAML files are skipped, not crash."""
        shipped = tmp_path / "shipped"
        shipped.mkdir()
        bad_file = shipped / "bad.tactic.yaml"
        bad_file.write_text("not: valid: yaml: [")

        with pytest.warns(UserWarning, match="Skipping invalid"):
            repo = TacticRepository(shipped_dir=shipped)

        assert repo.list_all() == []

    def test_save_writes_valid_yaml(
        self, tmp_path: Path, sample_tactic_data: dict
    ) -> None:
        from doctrine.tactics.models import Tactic

        project_dir = tmp_path / "project"
        repo = TacticRepository(
            shipped_dir=tmp_path / "empty", project_dir=project_dir
        )

        tactic = Tactic.model_validate(sample_tactic_data)
        path = repo.save(tactic)

        assert path.exists()
        assert path.suffix == ".yaml"

        yaml = YAML(typ="safe")
        data = yaml.load(path)
        assert data["id"] == "test-tactic"

    def test_save_raises_without_project_dir(
        self, sample_tactic_data: dict
    ) -> None:
        from doctrine.tactics.models import Tactic

        repo = TacticRepository()
        tactic = Tactic.model_validate(sample_tactic_data)
        with pytest.raises(ValueError, match="project_dir not configured"):
            repo.save(tactic)

    def test_field_level_merge_with_project_override(
        self, tmp_path: Path
    ) -> None:
        """Project tactic overrides shipped fields at field level."""
        shipped = tmp_path / "shipped"
        shipped.mkdir()
        project = tmp_path / "project"
        project.mkdir()

        yaml = YAML()
        yaml.default_flow_style = False

        base = {
            "schema_version": "1.0",
            "id": "merge-test",
            "name": "Base Name",
            "steps": [{"title": "Base Step"}],
        }
        override = {
            "schema_version": "1.0",
            "id": "merge-test",
            "name": "Overridden Name",
            "purpose": "Added purpose",
            "steps": [{"title": "Overridden Step"}],
        }

        with (shipped / "merge-test.tactic.yaml").open("w") as f:
            yaml.dump(base, f)
        with (project / "merge-test.tactic.yaml").open("w") as f:
            yaml.dump(override, f)

        repo = TacticRepository(shipped_dir=shipped, project_dir=project)
        tactic = repo.get("merge-test")
        assert tactic is not None
        assert tactic.name == "Overridden Name"
        assert tactic.purpose == "Added purpose"

    def test_nested_models_parse_from_shipped(self) -> None:
        """Acceptance: shipped tactics with steps parse nested models."""
        repo = TacticRepository()
        tactic = repo.get("zombies-tdd")
        assert tactic is not None
        assert tactic.steps[0].title == "Z - Zero"
        assert len(tactic.steps[0].examples) > 0

    def test_save_and_reload_preserves_fields(
        self, tmp_path: Path, enriched_tactic_data: dict
    ) -> None:
        """Acceptance: saving and reloading preserves all fields."""
        from doctrine.tactics.models import Tactic

        project_dir = tmp_path / "project"
        repo = TacticRepository(
            shipped_dir=tmp_path / "empty", project_dir=project_dir
        )

        tactic = Tactic.model_validate(enriched_tactic_data)
        repo.save(tactic)

        repo2 = TacticRepository(
            shipped_dir=tmp_path / "empty", project_dir=project_dir
        )
        loaded = repo2.get("enriched-tactic")
        assert loaded is not None
        assert loaded.name == tactic.name
        assert loaded.purpose == tactic.purpose
        assert len(loaded.steps) == len(tactic.steps)
        assert len(loaded.references) == len(tactic.references)
