"""Parametrized tests verifying tags and failure_modes on artifact models.

These tests run BEFORE the implementation exists (TDD). They verify:
- ``tags`` is an optional ``list[str]`` field on all doctrine artifact models.
- ``failure_modes`` is an optional ``list[FailureMode]`` field on Tactic,
  Directive, and Procedure models.
- Missing / None / empty values are accepted for optional fields.
- Invalid types are rejected.
"""

from __future__ import annotations

from typing import Any

import pytest
from pydantic import ValidationError

pytestmark = [pytest.mark.fast, pytest.mark.doctrine]


# ---------------------------------------------------------------------------
# Minimal valid data dicts for each artifact model that should accept ``tags``
# ---------------------------------------------------------------------------

TACTIC_DATA: dict[str, Any] = {
    "schema_version": "1.0",
    "id": "tag-test-tactic",
    "name": "Tag Test Tactic",
    "steps": [{"title": "Step One"}],
}

DIRECTIVE_DATA: dict[str, Any] = {
    "schema_version": "1.0",
    "id": "DIRECTIVE_TEST",
    "title": "Tag Test Directive",
    "intent": "Test tags on directives.",
    "enforcement": "advisory",
}

PROCEDURE_DATA: dict[str, Any] = {
    "schema_version": "1.0",
    "id": "tag-test-procedure",
    "name": "Tag Test Procedure",
    "purpose": "Test tags on procedures.",
    "entry_condition": "Always",
    "exit_condition": "Done",
    "steps": [{"title": "Step One"}],
}

PARADIGM_DATA: dict[str, Any] = {
    "schema_version": "1.0",
    "id": "tag-test-paradigm",
    "name": "Tag Test Paradigm",
    "summary": "Test tags on paradigms.",
}

STYLEGUIDE_DATA: dict[str, Any] = {
    "schema_version": "1.0",
    "id": "tag-test-styleguide",
    "title": "Tag Test Styleguide",
    "scope": "code",
    "principles": ["Be consistent"],
}

TOOLGUIDE_DATA: dict[str, Any] = {
    "schema_version": "1.0",
    "id": "tag-test-toolguide",
    "tool": "pytest",
    "title": "Tag Test Toolguide",
    "guide_path": "src/doctrine/guides/test-tool.md",
    "summary": "Test tags on toolguides.",
}

MISSION_DATA: dict[str, Any] = {
    "schema_version": "1.0",
    "key": "tag-test-mission",
    "name": "Tag Test Mission",
    "orchestration": {
        "states": ["planned"],
        "transitions": [{"from": "planned", "to": "done", "on": "complete"}],
        "required_artifacts": ["spec"],
    },
}

AGENT_PROFILE_DATA: dict[str, Any] = {
    "profile-id": "tag-test-agent",
    "name": "Tag Test Agent",
    "purpose": "Test tags on agent profiles.",
    "specialization": {"primary-focus": "Testing"},
}

MISSION_STEP_CONTRACT_DATA: dict[str, Any] = {
    "schema_version": "1.0",
    "id": "tag-test-contract",
    "action": "implement",
    "mission": "software-dev",
    "steps": [{"id": "s1", "description": "Step one"}],
}


def _import_model(model_name: str):
    """Dynamically import an artifact model class by name."""
    mapping = {
        "Tactic": "doctrine.tactics.models",
        "Directive": "doctrine.directives.models",
        "Procedure": "doctrine.procedures.models",
        "Paradigm": "doctrine.paradigms.models",
        "Styleguide": "doctrine.styleguides.models",
        "Toolguide": "doctrine.toolguides.models",
        "Mission": "doctrine.missions.models",
        "AgentProfileSchema": "doctrine.agent_profiles.schema_models",
        "MissionStepContract": "doctrine.mission_step_contracts.models",
    }
    import importlib

    module = importlib.import_module(mapping[model_name])
    return getattr(module, model_name)


# ---------------------------------------------------------------------------
# Tags tests — parametrized across ALL artifact models
# ---------------------------------------------------------------------------

_TAG_PARAMS = [
    ("Tactic", TACTIC_DATA),
    ("Directive", DIRECTIVE_DATA),
    ("Procedure", PROCEDURE_DATA),
    ("Paradigm", PARADIGM_DATA),
    ("Styleguide", STYLEGUIDE_DATA),
    ("Toolguide", TOOLGUIDE_DATA),
    ("Mission", MISSION_DATA),
    ("AgentProfileSchema", AGENT_PROFILE_DATA),
    ("MissionStepContract", MISSION_STEP_CONTRACT_DATA),
]


class TestTagsOnArtifactModels:
    """tags is an optional list[str] on every doctrine artifact model."""

    @pytest.mark.parametrize("model_name,data", _TAG_PARAMS, ids=[p[0] for p in _TAG_PARAMS])
    def test_tags_absent_is_valid(self, model_name: str, data: dict) -> None:
        model_cls = _import_model(model_name)
        instance = model_cls.model_validate(data)
        assert instance.tags is None or instance.tags == []

    @pytest.mark.parametrize("model_name,data", _TAG_PARAMS, ids=[p[0] for p in _TAG_PARAMS])
    def test_tags_with_strings(self, model_name: str, data: dict) -> None:
        model_cls = _import_model(model_name)
        tagged = {**data, "tags": ["refactoring", "ddd"]}
        instance = model_cls.model_validate(tagged)
        assert instance.tags == ["refactoring", "ddd"]

    @pytest.mark.parametrize("model_name,data", _TAG_PARAMS, ids=[p[0] for p in _TAG_PARAMS])
    def test_tags_empty_list(self, model_name: str, data: dict) -> None:
        model_cls = _import_model(model_name)
        tagged = {**data, "tags": []}
        instance = model_cls.model_validate(tagged)
        assert instance.tags == []

    @pytest.mark.parametrize("model_name,data", _TAG_PARAMS, ids=[p[0] for p in _TAG_PARAMS])
    def test_tags_rejects_non_string_items(self, model_name: str, data: dict) -> None:
        model_cls = _import_model(model_name)
        with pytest.raises(ValidationError):
            model_cls.model_validate({**data, "tags": [42]})

    @pytest.mark.parametrize("model_name,data", _TAG_PARAMS, ids=[p[0] for p in _TAG_PARAMS])
    def test_tags_rejects_non_list_type(self, model_name: str, data: dict) -> None:
        model_cls = _import_model(model_name)
        with pytest.raises(ValidationError):
            model_cls.model_validate({**data, "tags": "not-a-list"})


# ---------------------------------------------------------------------------
# FailureMode tests — parametrized across Tactic, Directive, Procedure
# ---------------------------------------------------------------------------

_FM_PARAMS = [
    ("Tactic", TACTIC_DATA),
    ("Directive", DIRECTIVE_DATA),
    ("Procedure", PROCEDURE_DATA),
]


class TestFailureModesOnArtifactModels:
    """failure_modes is an optional list[FailureMode] on Tactic/Directive/Procedure."""

    @pytest.mark.parametrize("model_name,data", _FM_PARAMS, ids=[p[0] for p in _FM_PARAMS])
    def test_failure_modes_absent_is_valid(self, model_name: str, data: dict) -> None:
        model_cls = _import_model(model_name)
        instance = model_cls.model_validate(data)
        assert instance.failure_modes == []

    @pytest.mark.parametrize("model_name,data", _FM_PARAMS, ids=[p[0] for p in _FM_PARAMS])
    def test_failure_modes_with_structured_objects(self, model_name: str, data: dict) -> None:
        model_cls = _import_model(model_name)
        fm_data = {
            **data,
            "failure_modes": [
                {"name": "Over-analysis", "description": "Too much effort on low-stakes decisions."},
                {"name": "Skipped pre-mortem", "description": "Optimism bias causes step to be skipped."},
            ],
        }
        instance = model_cls.model_validate(fm_data)
        assert len(instance.failure_modes) == 2
        assert instance.failure_modes[0].name == "Over-analysis"
        assert instance.failure_modes[1].description == "Optimism bias causes step to be skipped."

    @pytest.mark.parametrize("model_name,data", _FM_PARAMS, ids=[p[0] for p in _FM_PARAMS])
    def test_failure_modes_empty_list(self, model_name: str, data: dict) -> None:
        model_cls = _import_model(model_name)
        fm_data = {**data, "failure_modes": []}
        instance = model_cls.model_validate(fm_data)
        assert instance.failure_modes == []

    @pytest.mark.parametrize("model_name,data", _FM_PARAMS, ids=[p[0] for p in _FM_PARAMS])
    def test_failure_modes_rejects_bare_strings(self, model_name: str, data: dict) -> None:
        """Bare strings are no longer valid; must be structured {name, description}."""
        model_cls = _import_model(model_name)
        with pytest.raises(ValidationError):
            model_cls.model_validate({**data, "failure_modes": ["bare string"]})

    @pytest.mark.parametrize("model_name,data", _FM_PARAMS, ids=[p[0] for p in _FM_PARAMS])
    def test_failure_modes_rejects_missing_name(self, model_name: str, data: dict) -> None:
        model_cls = _import_model(model_name)
        with pytest.raises(ValidationError):
            model_cls.model_validate({**data, "failure_modes": [{"description": "no name"}]})

    @pytest.mark.parametrize("model_name,data", _FM_PARAMS, ids=[p[0] for p in _FM_PARAMS])
    def test_failure_modes_rejects_missing_description(self, model_name: str, data: dict) -> None:
        model_cls = _import_model(model_name)
        with pytest.raises(ValidationError):
            model_cls.model_validate({**data, "failure_modes": [{"name": "no desc"}]})
