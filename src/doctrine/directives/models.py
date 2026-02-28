"""
Directive domain model and value objects.

Defines the Directive Pydantic model with all governance fields including
optional enrichment fields (scope, procedures, integrity_rules, validation_criteria).
"""

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class Enforcement(StrEnum):
    """Enforcement level for a directive."""

    REQUIRED = "required"
    ADVISORY = "advisory"


class Directive(BaseModel):
    """
    A constraint-oriented governance rule.

    Directives define WHAT must be done (or avoided) with an enforcement
    level and optional references to tactics that describe HOW.
    """

    model_config = ConfigDict(frozen=True, populate_by_name=True)

    # Required fields
    id: str
    schema_version: str = Field(alias="schema_version")
    title: str
    intent: str
    enforcement: Enforcement

    # Optional core field
    tactic_refs: list[str] = Field(default_factory=list, alias="tactic_refs")

    # Optional enrichment fields
    scope: str | None = None
    procedures: list[str] = Field(default_factory=list)
    integrity_rules: list[str] = Field(default_factory=list, alias="integrity_rules")
    validation_criteria: list[str] = Field(
        default_factory=list, alias="validation_criteria"
    )
