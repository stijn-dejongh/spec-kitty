"""
Tactics domain model - public API.

This package provides the Tactic domain entity, supporting models,
and TacticRepository for loading, querying, and saving tactic YAML files.
"""

from doctrine.tactics.models import (
    ReferenceType,
    Tactic,
    TacticReference,
    TacticStep,
)
from doctrine.tactics.repository import TacticRepository

__all__ = [
    "ReferenceType",
    "Tactic",
    "TacticReference",
    "TacticRepository",
    "TacticStep",
]
