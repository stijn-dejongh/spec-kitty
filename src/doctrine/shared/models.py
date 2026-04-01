"""Shared Pydantic models used across multiple doctrine artifact types."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class Contradiction(BaseModel):
    """An anti-pattern or conflicting approach that opposes an artifact.

    Used by paradigms, directives, and tactics to declare explicit
    opposition to named anti-patterns or incompatible approaches.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    type: Literal["directive", "tactic", "paradigm"]
    id: str = Field(min_length=1)
    reason: str = Field(min_length=1)


class FailureMode(BaseModel):
    """A named failure mode with a description.

    Replaces the previous ``list[str]`` representation on tactics with a
    structured value object.  Used by tactics, directives, and procedures.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    name: str = Field(min_length=1)
    description: str = Field(min_length=1)


class ArtefactTags(BaseModel):
    """Thin wrapper around ``list[str]`` for artifact classification tags.

    Provides a canonical frozen value object for the optional ``tags``
    field present on all doctrine artifact models.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    values: list[str] = Field(default_factory=list)


__all__ = ["ArtefactTags", "Contradiction", "FailureMode"]
