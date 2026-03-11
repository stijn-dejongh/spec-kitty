"""Unit tests for Directive model and Enforcement enum."""

import pytest
from pydantic import ValidationError

from doctrine.directives.models import Directive, Enforcement


class TestEnforcement:
    def test_required_value(self) -> None:
        assert Enforcement.REQUIRED == "required"

    def test_advisory_value(self) -> None:
        assert Enforcement.ADVISORY == "advisory"


class TestDirective:
    def test_minimal_construction(self, sample_directive_data: dict) -> None:
        directive = Directive.model_validate(sample_directive_data)
        assert directive.id == "DIRECTIVE_999"
        assert directive.title == "Test Directive"
        assert directive.enforcement == Enforcement.REQUIRED
        assert directive.tactic_refs == []
        assert directive.scope is None
        assert directive.procedures == []
        assert directive.integrity_rules == []
        assert directive.validation_criteria == []

    def test_enriched_construction(self, enriched_directive_data: dict) -> None:
        directive = Directive.model_validate(enriched_directive_data)
        assert directive.scope == "Applies to all test scenarios."
        assert len(directive.procedures) == 2
        assert len(directive.integrity_rules) == 1
        assert len(directive.validation_criteria) == 1
        assert "zombies-tdd" in directive.tactic_refs

    def test_frozen_model(self, sample_directive_data: dict) -> None:
        directive = Directive.model_validate(sample_directive_data)
        with pytest.raises(ValidationError):
            directive.title = "changed"  # type: ignore[misc]

    def test_missing_required_field_raises(self) -> None:
        with pytest.raises(ValidationError):
            Directive.model_validate({"id": "DIRECTIVE_001", "title": "Test"})

    def test_invalid_enforcement_raises(self, sample_directive_data: dict) -> None:
        sample_directive_data["enforcement"] = "invalid"
        with pytest.raises(ValidationError):
            Directive.model_validate(sample_directive_data)
