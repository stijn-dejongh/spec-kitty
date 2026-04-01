"""Unit tests for the ArtefactTags value object.

ArtefactTags is a frozen Pydantic BaseModel wrapping list[str] that serves
as the canonical type for the optional ``tags`` field on all doctrine
artifact models.
"""

import pytest
from pydantic import ValidationError

pytestmark = [pytest.mark.fast, pytest.mark.doctrine]


class TestArtefactTagsConstruction:
    """ArtefactTags wraps a list[str] with frozen semantics."""

    def test_accepts_list_of_strings(self) -> None:
        from doctrine.shared.models import ArtefactTags

        tags = ArtefactTags(values=["refactoring", "ddd", "event-sourcing"])
        assert tags.values == ["refactoring", "ddd", "event-sourcing"]

    def test_empty_list_is_valid(self) -> None:
        from doctrine.shared.models import ArtefactTags

        tags = ArtefactTags(values=[])
        assert tags.values == []

    def test_single_tag_is_valid(self) -> None:
        from doctrine.shared.models import ArtefactTags

        tags = ArtefactTags(values=["performance"])
        assert tags.values == ["performance"]

    def test_frozen_rejects_mutation(self) -> None:
        from doctrine.shared.models import ArtefactTags

        tags = ArtefactTags(values=["a", "b"])
        with pytest.raises(ValidationError):
            tags.values = ["c"]  # type: ignore[misc]


class TestArtefactTagsValidation:
    """ArtefactTags rejects non-string entries and wrong types."""

    def test_rejects_int_in_list(self) -> None:
        from doctrine.shared.models import ArtefactTags

        with pytest.raises(ValidationError):
            ArtefactTags(values=[42])  # type: ignore[list-item]

    def test_rejects_none_in_list(self) -> None:
        from doctrine.shared.models import ArtefactTags

        with pytest.raises(ValidationError):
            ArtefactTags(values=[None])  # type: ignore[list-item]

    def test_rejects_dict_in_list(self) -> None:
        from doctrine.shared.models import ArtefactTags

        with pytest.raises(ValidationError):
            ArtefactTags(values=[{"key": "val"}])  # type: ignore[list-item]

    def test_rejects_non_list_type(self) -> None:
        from doctrine.shared.models import ArtefactTags

        with pytest.raises(ValidationError):
            ArtefactTags(values="not-a-list")  # type: ignore[arg-type]

    def test_extra_fields_rejected(self) -> None:
        from doctrine.shared.models import ArtefactTags

        with pytest.raises(ValidationError):
            ArtefactTags(values=["ok"], extra_field="bad")  # type: ignore[call-arg]


class TestArtefactTagsEquality:
    """ArtefactTags supports value equality as a frozen model."""

    def test_equal_tags(self) -> None:
        from doctrine.shared.models import ArtefactTags

        a = ArtefactTags(values=["x", "y"])
        b = ArtefactTags(values=["x", "y"])
        assert a == b

    def test_order_matters(self) -> None:
        from doctrine.shared.models import ArtefactTags

        a = ArtefactTags(values=["x", "y"])
        b = ArtefactTags(values=["y", "x"])
        assert a != b
