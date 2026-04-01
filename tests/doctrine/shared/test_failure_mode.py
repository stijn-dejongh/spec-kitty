"""Unit tests for the FailureMode value object.

FailureMode is a frozen Pydantic BaseModel with {name: str, description: str}
that replaces the previous bare-string failure_modes on tactics and adds
structured failure mode support to directives and procedures.
"""

import pytest
from pydantic import ValidationError

pytestmark = [pytest.mark.fast, pytest.mark.doctrine]


class TestFailureModeConstruction:
    """FailureMode wraps a name + description with frozen semantics."""

    def test_construction(self) -> None:
        from doctrine.shared.models import FailureMode

        fm = FailureMode(name="Over-analysis", description="Spending too much effort.")
        assert fm.name == "Over-analysis"
        assert fm.description == "Spending too much effort."

    def test_frozen_rejects_mutation(self) -> None:
        from doctrine.shared.models import FailureMode

        fm = FailureMode(name="A", description="B")
        with pytest.raises(ValidationError):
            fm.name = "changed"  # type: ignore[misc]

    def test_frozen_rejects_description_mutation(self) -> None:
        from doctrine.shared.models import FailureMode

        fm = FailureMode(name="A", description="B")
        with pytest.raises(ValidationError):
            fm.description = "changed"  # type: ignore[misc]


class TestFailureModeValidation:
    """FailureMode requires both name and description as non-empty strings."""

    def test_missing_name_raises(self) -> None:
        from doctrine.shared.models import FailureMode

        with pytest.raises(ValidationError):
            FailureMode(description="desc only")  # type: ignore[call-arg]

    def test_missing_description_raises(self) -> None:
        from doctrine.shared.models import FailureMode

        with pytest.raises(ValidationError):
            FailureMode(name="name only")  # type: ignore[call-arg]

    def test_empty_name_raises(self) -> None:
        from doctrine.shared.models import FailureMode

        with pytest.raises(ValidationError):
            FailureMode(name="", description="desc")

    def test_empty_description_raises(self) -> None:
        from doctrine.shared.models import FailureMode

        with pytest.raises(ValidationError):
            FailureMode(name="name", description="")

    def test_extra_fields_rejected(self) -> None:
        from doctrine.shared.models import FailureMode

        with pytest.raises(ValidationError):
            FailureMode(
                name="A",
                description="B",
                severity="high",  # type: ignore[call-arg]
            )

    def test_int_name_rejected(self) -> None:
        from doctrine.shared.models import FailureMode

        with pytest.raises(ValidationError):
            FailureMode(name=42, description="desc")  # type: ignore[arg-type]


class TestFailureModeEquality:
    """FailureMode supports value equality as a frozen model."""

    def test_equal_failure_modes(self) -> None:
        from doctrine.shared.models import FailureMode

        a = FailureMode(name="X", description="Y")
        b = FailureMode(name="X", description="Y")
        assert a == b

    def test_different_name(self) -> None:
        from doctrine.shared.models import FailureMode

        a = FailureMode(name="X", description="Y")
        b = FailureMode(name="Z", description="Y")
        assert a != b

    def test_different_description(self) -> None:
        from doctrine.shared.models import FailureMode

        a = FailureMode(name="X", description="Y")
        b = FailureMode(name="X", description="Z")
        assert a != b
