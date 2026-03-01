"""Core data models for glossary semantic integrity."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, List, Optional
from typing import Annotated
from typing import Callable
from typing import ClassVar

MutantDict = Annotated[dict[str, Callable], "Mutant"] # type: ignore


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None): # type: ignore
    """Forward call to original or mutated function, depending on the environment"""
    import os # type: ignore
    mutant_under_test = os.environ['MUTANT_UNDER_TEST'] # type: ignore
    if mutant_under_test == 'fail': # type: ignore
        from mutmut.__main__ import MutmutProgrammaticFailException # type: ignore
        raise MutmutProgrammaticFailException('Failed programmatically')       # type: ignore
    elif mutant_under_test == 'stats': # type: ignore
        from mutmut.__main__ import record_trampoline_hit # type: ignore
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__) # type: ignore
        # (for class methods, orig is bound and thus does not need the explicit self argument)
        result = orig(*call_args, **call_kwargs) # type: ignore
        return result # type: ignore
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_' # type: ignore
    if not mutant_under_test.startswith(prefix): # type: ignore
        result = orig(*call_args, **call_kwargs) # type: ignore
        return result # type: ignore
    mutant_name = mutant_under_test.rpartition('.')[-1] # type: ignore
    if self_arg is not None: # type: ignore
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs) # type: ignore
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs) # type: ignore
    return result # type: ignore


@dataclass(frozen=True)
class TermSurface:
    """Raw string representation of a term."""
    surface_text: str  # e.g., "workspace"

    def __post_init__(self) -> None:
        # Validate: must be normalized (lowercase, trimmed)
        if self.surface_text != self.surface_text.lower().strip():
            raise ValueError(f"TermSurface must be normalized: {self.surface_text}")


class SenseStatus(Enum):
    """Status of a TermSense."""
    DRAFT = "draft"          # Auto-extracted, low confidence
    ACTIVE = "active"        # Promoted by user or high confidence
    DEPRECATED = "deprecated"  # Kept in history, not in active resolution


@dataclass
class Provenance:
    """Provenance metadata for a TermSense."""
    actor_id: str      # e.g., "user:alice" or "llm:claude-sonnet-4"
    timestamp: datetime
    source: str        # e.g., "user_clarification", "metadata_hint", "auto_extraction"


@dataclass
class TermSense:
    """Meaning of a TermSurface within a specific GlossaryScope."""
    surface: TermSurface
    scope: str  # GlossaryScope enum value (defined in scope.py)
    definition: str
    provenance: Provenance
    confidence: float  # 0.0-1.0
    status: SenseStatus = SenseStatus.DRAFT

    def __post_init__(self) -> None:
        # Validate confidence range
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError(f"Confidence must be 0.0-1.0: {self.confidence}")
        # Validate definition not empty
        if not self.definition.strip():
            raise ValueError("Definition cannot be empty")


class ConflictType(Enum):
    """Type of semantic conflict."""
    UNKNOWN = "unknown"                      # No match in any scope
    AMBIGUOUS = "ambiguous"                  # Multiple active senses, unqualified usage
    INCONSISTENT = "inconsistent"            # LLM output contradicts active glossary
    UNRESOLVED_CRITICAL = "unresolved_critical"  # Unknown critical term, low confidence


class Severity(Enum):
    """Severity level of a semantic conflict."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass
class SenseRef:
    """Reference to a TermSense (used in conflict candidates)."""
    surface: str
    scope: str
    definition: str
    confidence: float


@dataclass
class SemanticConflict:
    """Classification of a term conflict."""
    term: TermSurface
    conflict_type: ConflictType
    severity: Severity
    confidence: float  # 0.0-1.0 (confidence in conflict detection)
    candidate_senses: List[SenseRef] = field(default_factory=list)
    context: str = ""  # Usage location (e.g., "step input: description field")

    def __post_init__(self) -> None:
        # Validate: AMBIGUOUS type must have candidates
        if self.conflict_type == ConflictType.AMBIGUOUS and not self.candidate_senses:
            raise ValueError("AMBIGUOUS conflict must have candidate_senses")


# Serialization helpers for event emission

def term_surface_to_dict(ts: TermSurface) -> dict[str, Any]:
    args = [ts]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_term_surface_to_dict__mutmut_orig, x_term_surface_to_dict__mutmut_mutants, args, kwargs, None)


# Serialization helpers for event emission

def x_term_surface_to_dict__mutmut_orig(ts: TermSurface) -> dict[str, Any]:
    """Serialize TermSurface to dict."""
    return {"surface_text": ts.surface_text}


# Serialization helpers for event emission

def x_term_surface_to_dict__mutmut_1(ts: TermSurface) -> dict[str, Any]:
    """Serialize TermSurface to dict."""
    return {"XXsurface_textXX": ts.surface_text}


# Serialization helpers for event emission

def x_term_surface_to_dict__mutmut_2(ts: TermSurface) -> dict[str, Any]:
    """Serialize TermSurface to dict."""
    return {"SURFACE_TEXT": ts.surface_text}

x_term_surface_to_dict__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_term_surface_to_dict__mutmut_1': x_term_surface_to_dict__mutmut_1, 
    'x_term_surface_to_dict__mutmut_2': x_term_surface_to_dict__mutmut_2
}
x_term_surface_to_dict__mutmut_orig.__name__ = 'x_term_surface_to_dict'


def term_sense_to_dict(ts: TermSense) -> dict[str, Any]:
    args = [ts]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_term_sense_to_dict__mutmut_orig, x_term_sense_to_dict__mutmut_mutants, args, kwargs, None)


def x_term_sense_to_dict__mutmut_orig(ts: TermSense) -> dict[str, Any]:
    """Serialize TermSense to dict."""
    return {
        "surface": term_surface_to_dict(ts.surface),
        "scope": ts.scope,
        "definition": ts.definition,
        "provenance": {
            "actor_id": ts.provenance.actor_id,
            "timestamp": ts.provenance.timestamp.isoformat(),
            "source": ts.provenance.source,
        },
        "confidence": ts.confidence,
        "status": ts.status.value,
    }


def x_term_sense_to_dict__mutmut_1(ts: TermSense) -> dict[str, Any]:
    """Serialize TermSense to dict."""
    return {
        "XXsurfaceXX": term_surface_to_dict(ts.surface),
        "scope": ts.scope,
        "definition": ts.definition,
        "provenance": {
            "actor_id": ts.provenance.actor_id,
            "timestamp": ts.provenance.timestamp.isoformat(),
            "source": ts.provenance.source,
        },
        "confidence": ts.confidence,
        "status": ts.status.value,
    }


def x_term_sense_to_dict__mutmut_2(ts: TermSense) -> dict[str, Any]:
    """Serialize TermSense to dict."""
    return {
        "SURFACE": term_surface_to_dict(ts.surface),
        "scope": ts.scope,
        "definition": ts.definition,
        "provenance": {
            "actor_id": ts.provenance.actor_id,
            "timestamp": ts.provenance.timestamp.isoformat(),
            "source": ts.provenance.source,
        },
        "confidence": ts.confidence,
        "status": ts.status.value,
    }


def x_term_sense_to_dict__mutmut_3(ts: TermSense) -> dict[str, Any]:
    """Serialize TermSense to dict."""
    return {
        "surface": term_surface_to_dict(None),
        "scope": ts.scope,
        "definition": ts.definition,
        "provenance": {
            "actor_id": ts.provenance.actor_id,
            "timestamp": ts.provenance.timestamp.isoformat(),
            "source": ts.provenance.source,
        },
        "confidence": ts.confidence,
        "status": ts.status.value,
    }


def x_term_sense_to_dict__mutmut_4(ts: TermSense) -> dict[str, Any]:
    """Serialize TermSense to dict."""
    return {
        "surface": term_surface_to_dict(ts.surface),
        "XXscopeXX": ts.scope,
        "definition": ts.definition,
        "provenance": {
            "actor_id": ts.provenance.actor_id,
            "timestamp": ts.provenance.timestamp.isoformat(),
            "source": ts.provenance.source,
        },
        "confidence": ts.confidence,
        "status": ts.status.value,
    }


def x_term_sense_to_dict__mutmut_5(ts: TermSense) -> dict[str, Any]:
    """Serialize TermSense to dict."""
    return {
        "surface": term_surface_to_dict(ts.surface),
        "SCOPE": ts.scope,
        "definition": ts.definition,
        "provenance": {
            "actor_id": ts.provenance.actor_id,
            "timestamp": ts.provenance.timestamp.isoformat(),
            "source": ts.provenance.source,
        },
        "confidence": ts.confidence,
        "status": ts.status.value,
    }


def x_term_sense_to_dict__mutmut_6(ts: TermSense) -> dict[str, Any]:
    """Serialize TermSense to dict."""
    return {
        "surface": term_surface_to_dict(ts.surface),
        "scope": ts.scope,
        "XXdefinitionXX": ts.definition,
        "provenance": {
            "actor_id": ts.provenance.actor_id,
            "timestamp": ts.provenance.timestamp.isoformat(),
            "source": ts.provenance.source,
        },
        "confidence": ts.confidence,
        "status": ts.status.value,
    }


def x_term_sense_to_dict__mutmut_7(ts: TermSense) -> dict[str, Any]:
    """Serialize TermSense to dict."""
    return {
        "surface": term_surface_to_dict(ts.surface),
        "scope": ts.scope,
        "DEFINITION": ts.definition,
        "provenance": {
            "actor_id": ts.provenance.actor_id,
            "timestamp": ts.provenance.timestamp.isoformat(),
            "source": ts.provenance.source,
        },
        "confidence": ts.confidence,
        "status": ts.status.value,
    }


def x_term_sense_to_dict__mutmut_8(ts: TermSense) -> dict[str, Any]:
    """Serialize TermSense to dict."""
    return {
        "surface": term_surface_to_dict(ts.surface),
        "scope": ts.scope,
        "definition": ts.definition,
        "XXprovenanceXX": {
            "actor_id": ts.provenance.actor_id,
            "timestamp": ts.provenance.timestamp.isoformat(),
            "source": ts.provenance.source,
        },
        "confidence": ts.confidence,
        "status": ts.status.value,
    }


def x_term_sense_to_dict__mutmut_9(ts: TermSense) -> dict[str, Any]:
    """Serialize TermSense to dict."""
    return {
        "surface": term_surface_to_dict(ts.surface),
        "scope": ts.scope,
        "definition": ts.definition,
        "PROVENANCE": {
            "actor_id": ts.provenance.actor_id,
            "timestamp": ts.provenance.timestamp.isoformat(),
            "source": ts.provenance.source,
        },
        "confidence": ts.confidence,
        "status": ts.status.value,
    }


def x_term_sense_to_dict__mutmut_10(ts: TermSense) -> dict[str, Any]:
    """Serialize TermSense to dict."""
    return {
        "surface": term_surface_to_dict(ts.surface),
        "scope": ts.scope,
        "definition": ts.definition,
        "provenance": {
            "XXactor_idXX": ts.provenance.actor_id,
            "timestamp": ts.provenance.timestamp.isoformat(),
            "source": ts.provenance.source,
        },
        "confidence": ts.confidence,
        "status": ts.status.value,
    }


def x_term_sense_to_dict__mutmut_11(ts: TermSense) -> dict[str, Any]:
    """Serialize TermSense to dict."""
    return {
        "surface": term_surface_to_dict(ts.surface),
        "scope": ts.scope,
        "definition": ts.definition,
        "provenance": {
            "ACTOR_ID": ts.provenance.actor_id,
            "timestamp": ts.provenance.timestamp.isoformat(),
            "source": ts.provenance.source,
        },
        "confidence": ts.confidence,
        "status": ts.status.value,
    }


def x_term_sense_to_dict__mutmut_12(ts: TermSense) -> dict[str, Any]:
    """Serialize TermSense to dict."""
    return {
        "surface": term_surface_to_dict(ts.surface),
        "scope": ts.scope,
        "definition": ts.definition,
        "provenance": {
            "actor_id": ts.provenance.actor_id,
            "XXtimestampXX": ts.provenance.timestamp.isoformat(),
            "source": ts.provenance.source,
        },
        "confidence": ts.confidence,
        "status": ts.status.value,
    }


def x_term_sense_to_dict__mutmut_13(ts: TermSense) -> dict[str, Any]:
    """Serialize TermSense to dict."""
    return {
        "surface": term_surface_to_dict(ts.surface),
        "scope": ts.scope,
        "definition": ts.definition,
        "provenance": {
            "actor_id": ts.provenance.actor_id,
            "TIMESTAMP": ts.provenance.timestamp.isoformat(),
            "source": ts.provenance.source,
        },
        "confidence": ts.confidence,
        "status": ts.status.value,
    }


def x_term_sense_to_dict__mutmut_14(ts: TermSense) -> dict[str, Any]:
    """Serialize TermSense to dict."""
    return {
        "surface": term_surface_to_dict(ts.surface),
        "scope": ts.scope,
        "definition": ts.definition,
        "provenance": {
            "actor_id": ts.provenance.actor_id,
            "timestamp": ts.provenance.timestamp.isoformat(),
            "XXsourceXX": ts.provenance.source,
        },
        "confidence": ts.confidence,
        "status": ts.status.value,
    }


def x_term_sense_to_dict__mutmut_15(ts: TermSense) -> dict[str, Any]:
    """Serialize TermSense to dict."""
    return {
        "surface": term_surface_to_dict(ts.surface),
        "scope": ts.scope,
        "definition": ts.definition,
        "provenance": {
            "actor_id": ts.provenance.actor_id,
            "timestamp": ts.provenance.timestamp.isoformat(),
            "SOURCE": ts.provenance.source,
        },
        "confidence": ts.confidence,
        "status": ts.status.value,
    }


def x_term_sense_to_dict__mutmut_16(ts: TermSense) -> dict[str, Any]:
    """Serialize TermSense to dict."""
    return {
        "surface": term_surface_to_dict(ts.surface),
        "scope": ts.scope,
        "definition": ts.definition,
        "provenance": {
            "actor_id": ts.provenance.actor_id,
            "timestamp": ts.provenance.timestamp.isoformat(),
            "source": ts.provenance.source,
        },
        "XXconfidenceXX": ts.confidence,
        "status": ts.status.value,
    }


def x_term_sense_to_dict__mutmut_17(ts: TermSense) -> dict[str, Any]:
    """Serialize TermSense to dict."""
    return {
        "surface": term_surface_to_dict(ts.surface),
        "scope": ts.scope,
        "definition": ts.definition,
        "provenance": {
            "actor_id": ts.provenance.actor_id,
            "timestamp": ts.provenance.timestamp.isoformat(),
            "source": ts.provenance.source,
        },
        "CONFIDENCE": ts.confidence,
        "status": ts.status.value,
    }


def x_term_sense_to_dict__mutmut_18(ts: TermSense) -> dict[str, Any]:
    """Serialize TermSense to dict."""
    return {
        "surface": term_surface_to_dict(ts.surface),
        "scope": ts.scope,
        "definition": ts.definition,
        "provenance": {
            "actor_id": ts.provenance.actor_id,
            "timestamp": ts.provenance.timestamp.isoformat(),
            "source": ts.provenance.source,
        },
        "confidence": ts.confidence,
        "XXstatusXX": ts.status.value,
    }


def x_term_sense_to_dict__mutmut_19(ts: TermSense) -> dict[str, Any]:
    """Serialize TermSense to dict."""
    return {
        "surface": term_surface_to_dict(ts.surface),
        "scope": ts.scope,
        "definition": ts.definition,
        "provenance": {
            "actor_id": ts.provenance.actor_id,
            "timestamp": ts.provenance.timestamp.isoformat(),
            "source": ts.provenance.source,
        },
        "confidence": ts.confidence,
        "STATUS": ts.status.value,
    }

x_term_sense_to_dict__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_term_sense_to_dict__mutmut_1': x_term_sense_to_dict__mutmut_1, 
    'x_term_sense_to_dict__mutmut_2': x_term_sense_to_dict__mutmut_2, 
    'x_term_sense_to_dict__mutmut_3': x_term_sense_to_dict__mutmut_3, 
    'x_term_sense_to_dict__mutmut_4': x_term_sense_to_dict__mutmut_4, 
    'x_term_sense_to_dict__mutmut_5': x_term_sense_to_dict__mutmut_5, 
    'x_term_sense_to_dict__mutmut_6': x_term_sense_to_dict__mutmut_6, 
    'x_term_sense_to_dict__mutmut_7': x_term_sense_to_dict__mutmut_7, 
    'x_term_sense_to_dict__mutmut_8': x_term_sense_to_dict__mutmut_8, 
    'x_term_sense_to_dict__mutmut_9': x_term_sense_to_dict__mutmut_9, 
    'x_term_sense_to_dict__mutmut_10': x_term_sense_to_dict__mutmut_10, 
    'x_term_sense_to_dict__mutmut_11': x_term_sense_to_dict__mutmut_11, 
    'x_term_sense_to_dict__mutmut_12': x_term_sense_to_dict__mutmut_12, 
    'x_term_sense_to_dict__mutmut_13': x_term_sense_to_dict__mutmut_13, 
    'x_term_sense_to_dict__mutmut_14': x_term_sense_to_dict__mutmut_14, 
    'x_term_sense_to_dict__mutmut_15': x_term_sense_to_dict__mutmut_15, 
    'x_term_sense_to_dict__mutmut_16': x_term_sense_to_dict__mutmut_16, 
    'x_term_sense_to_dict__mutmut_17': x_term_sense_to_dict__mutmut_17, 
    'x_term_sense_to_dict__mutmut_18': x_term_sense_to_dict__mutmut_18, 
    'x_term_sense_to_dict__mutmut_19': x_term_sense_to_dict__mutmut_19
}
x_term_sense_to_dict__mutmut_orig.__name__ = 'x_term_sense_to_dict'


def semantic_conflict_to_dict(sc: SemanticConflict) -> dict[str, Any]:
    args = [sc]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_semantic_conflict_to_dict__mutmut_orig, x_semantic_conflict_to_dict__mutmut_mutants, args, kwargs, None)


def x_semantic_conflict_to_dict__mutmut_orig(sc: SemanticConflict) -> dict[str, Any]:
    """Serialize SemanticConflict to dict."""
    return {
        "term": term_surface_to_dict(sc.term),
        "conflict_type": sc.conflict_type.value,
        "severity": sc.severity.value,
        "confidence": sc.confidence,
        "candidate_senses": [
            {
                "surface": c.surface,
                "scope": c.scope,
                "definition": c.definition,
                "confidence": c.confidence,
            }
            for c in sc.candidate_senses
        ],
        "context": sc.context,
    }


def x_semantic_conflict_to_dict__mutmut_1(sc: SemanticConflict) -> dict[str, Any]:
    """Serialize SemanticConflict to dict."""
    return {
        "XXtermXX": term_surface_to_dict(sc.term),
        "conflict_type": sc.conflict_type.value,
        "severity": sc.severity.value,
        "confidence": sc.confidence,
        "candidate_senses": [
            {
                "surface": c.surface,
                "scope": c.scope,
                "definition": c.definition,
                "confidence": c.confidence,
            }
            for c in sc.candidate_senses
        ],
        "context": sc.context,
    }


def x_semantic_conflict_to_dict__mutmut_2(sc: SemanticConflict) -> dict[str, Any]:
    """Serialize SemanticConflict to dict."""
    return {
        "TERM": term_surface_to_dict(sc.term),
        "conflict_type": sc.conflict_type.value,
        "severity": sc.severity.value,
        "confidence": sc.confidence,
        "candidate_senses": [
            {
                "surface": c.surface,
                "scope": c.scope,
                "definition": c.definition,
                "confidence": c.confidence,
            }
            for c in sc.candidate_senses
        ],
        "context": sc.context,
    }


def x_semantic_conflict_to_dict__mutmut_3(sc: SemanticConflict) -> dict[str, Any]:
    """Serialize SemanticConflict to dict."""
    return {
        "term": term_surface_to_dict(None),
        "conflict_type": sc.conflict_type.value,
        "severity": sc.severity.value,
        "confidence": sc.confidence,
        "candidate_senses": [
            {
                "surface": c.surface,
                "scope": c.scope,
                "definition": c.definition,
                "confidence": c.confidence,
            }
            for c in sc.candidate_senses
        ],
        "context": sc.context,
    }


def x_semantic_conflict_to_dict__mutmut_4(sc: SemanticConflict) -> dict[str, Any]:
    """Serialize SemanticConflict to dict."""
    return {
        "term": term_surface_to_dict(sc.term),
        "XXconflict_typeXX": sc.conflict_type.value,
        "severity": sc.severity.value,
        "confidence": sc.confidence,
        "candidate_senses": [
            {
                "surface": c.surface,
                "scope": c.scope,
                "definition": c.definition,
                "confidence": c.confidence,
            }
            for c in sc.candidate_senses
        ],
        "context": sc.context,
    }


def x_semantic_conflict_to_dict__mutmut_5(sc: SemanticConflict) -> dict[str, Any]:
    """Serialize SemanticConflict to dict."""
    return {
        "term": term_surface_to_dict(sc.term),
        "CONFLICT_TYPE": sc.conflict_type.value,
        "severity": sc.severity.value,
        "confidence": sc.confidence,
        "candidate_senses": [
            {
                "surface": c.surface,
                "scope": c.scope,
                "definition": c.definition,
                "confidence": c.confidence,
            }
            for c in sc.candidate_senses
        ],
        "context": sc.context,
    }


def x_semantic_conflict_to_dict__mutmut_6(sc: SemanticConflict) -> dict[str, Any]:
    """Serialize SemanticConflict to dict."""
    return {
        "term": term_surface_to_dict(sc.term),
        "conflict_type": sc.conflict_type.value,
        "XXseverityXX": sc.severity.value,
        "confidence": sc.confidence,
        "candidate_senses": [
            {
                "surface": c.surface,
                "scope": c.scope,
                "definition": c.definition,
                "confidence": c.confidence,
            }
            for c in sc.candidate_senses
        ],
        "context": sc.context,
    }


def x_semantic_conflict_to_dict__mutmut_7(sc: SemanticConflict) -> dict[str, Any]:
    """Serialize SemanticConflict to dict."""
    return {
        "term": term_surface_to_dict(sc.term),
        "conflict_type": sc.conflict_type.value,
        "SEVERITY": sc.severity.value,
        "confidence": sc.confidence,
        "candidate_senses": [
            {
                "surface": c.surface,
                "scope": c.scope,
                "definition": c.definition,
                "confidence": c.confidence,
            }
            for c in sc.candidate_senses
        ],
        "context": sc.context,
    }


def x_semantic_conflict_to_dict__mutmut_8(sc: SemanticConflict) -> dict[str, Any]:
    """Serialize SemanticConflict to dict."""
    return {
        "term": term_surface_to_dict(sc.term),
        "conflict_type": sc.conflict_type.value,
        "severity": sc.severity.value,
        "XXconfidenceXX": sc.confidence,
        "candidate_senses": [
            {
                "surface": c.surface,
                "scope": c.scope,
                "definition": c.definition,
                "confidence": c.confidence,
            }
            for c in sc.candidate_senses
        ],
        "context": sc.context,
    }


def x_semantic_conflict_to_dict__mutmut_9(sc: SemanticConflict) -> dict[str, Any]:
    """Serialize SemanticConflict to dict."""
    return {
        "term": term_surface_to_dict(sc.term),
        "conflict_type": sc.conflict_type.value,
        "severity": sc.severity.value,
        "CONFIDENCE": sc.confidence,
        "candidate_senses": [
            {
                "surface": c.surface,
                "scope": c.scope,
                "definition": c.definition,
                "confidence": c.confidence,
            }
            for c in sc.candidate_senses
        ],
        "context": sc.context,
    }


def x_semantic_conflict_to_dict__mutmut_10(sc: SemanticConflict) -> dict[str, Any]:
    """Serialize SemanticConflict to dict."""
    return {
        "term": term_surface_to_dict(sc.term),
        "conflict_type": sc.conflict_type.value,
        "severity": sc.severity.value,
        "confidence": sc.confidence,
        "XXcandidate_sensesXX": [
            {
                "surface": c.surface,
                "scope": c.scope,
                "definition": c.definition,
                "confidence": c.confidence,
            }
            for c in sc.candidate_senses
        ],
        "context": sc.context,
    }


def x_semantic_conflict_to_dict__mutmut_11(sc: SemanticConflict) -> dict[str, Any]:
    """Serialize SemanticConflict to dict."""
    return {
        "term": term_surface_to_dict(sc.term),
        "conflict_type": sc.conflict_type.value,
        "severity": sc.severity.value,
        "confidence": sc.confidence,
        "CANDIDATE_SENSES": [
            {
                "surface": c.surface,
                "scope": c.scope,
                "definition": c.definition,
                "confidence": c.confidence,
            }
            for c in sc.candidate_senses
        ],
        "context": sc.context,
    }


def x_semantic_conflict_to_dict__mutmut_12(sc: SemanticConflict) -> dict[str, Any]:
    """Serialize SemanticConflict to dict."""
    return {
        "term": term_surface_to_dict(sc.term),
        "conflict_type": sc.conflict_type.value,
        "severity": sc.severity.value,
        "confidence": sc.confidence,
        "candidate_senses": [
            {
                "XXsurfaceXX": c.surface,
                "scope": c.scope,
                "definition": c.definition,
                "confidence": c.confidence,
            }
            for c in sc.candidate_senses
        ],
        "context": sc.context,
    }


def x_semantic_conflict_to_dict__mutmut_13(sc: SemanticConflict) -> dict[str, Any]:
    """Serialize SemanticConflict to dict."""
    return {
        "term": term_surface_to_dict(sc.term),
        "conflict_type": sc.conflict_type.value,
        "severity": sc.severity.value,
        "confidence": sc.confidence,
        "candidate_senses": [
            {
                "SURFACE": c.surface,
                "scope": c.scope,
                "definition": c.definition,
                "confidence": c.confidence,
            }
            for c in sc.candidate_senses
        ],
        "context": sc.context,
    }


def x_semantic_conflict_to_dict__mutmut_14(sc: SemanticConflict) -> dict[str, Any]:
    """Serialize SemanticConflict to dict."""
    return {
        "term": term_surface_to_dict(sc.term),
        "conflict_type": sc.conflict_type.value,
        "severity": sc.severity.value,
        "confidence": sc.confidence,
        "candidate_senses": [
            {
                "surface": c.surface,
                "XXscopeXX": c.scope,
                "definition": c.definition,
                "confidence": c.confidence,
            }
            for c in sc.candidate_senses
        ],
        "context": sc.context,
    }


def x_semantic_conflict_to_dict__mutmut_15(sc: SemanticConflict) -> dict[str, Any]:
    """Serialize SemanticConflict to dict."""
    return {
        "term": term_surface_to_dict(sc.term),
        "conflict_type": sc.conflict_type.value,
        "severity": sc.severity.value,
        "confidence": sc.confidence,
        "candidate_senses": [
            {
                "surface": c.surface,
                "SCOPE": c.scope,
                "definition": c.definition,
                "confidence": c.confidence,
            }
            for c in sc.candidate_senses
        ],
        "context": sc.context,
    }


def x_semantic_conflict_to_dict__mutmut_16(sc: SemanticConflict) -> dict[str, Any]:
    """Serialize SemanticConflict to dict."""
    return {
        "term": term_surface_to_dict(sc.term),
        "conflict_type": sc.conflict_type.value,
        "severity": sc.severity.value,
        "confidence": sc.confidence,
        "candidate_senses": [
            {
                "surface": c.surface,
                "scope": c.scope,
                "XXdefinitionXX": c.definition,
                "confidence": c.confidence,
            }
            for c in sc.candidate_senses
        ],
        "context": sc.context,
    }


def x_semantic_conflict_to_dict__mutmut_17(sc: SemanticConflict) -> dict[str, Any]:
    """Serialize SemanticConflict to dict."""
    return {
        "term": term_surface_to_dict(sc.term),
        "conflict_type": sc.conflict_type.value,
        "severity": sc.severity.value,
        "confidence": sc.confidence,
        "candidate_senses": [
            {
                "surface": c.surface,
                "scope": c.scope,
                "DEFINITION": c.definition,
                "confidence": c.confidence,
            }
            for c in sc.candidate_senses
        ],
        "context": sc.context,
    }


def x_semantic_conflict_to_dict__mutmut_18(sc: SemanticConflict) -> dict[str, Any]:
    """Serialize SemanticConflict to dict."""
    return {
        "term": term_surface_to_dict(sc.term),
        "conflict_type": sc.conflict_type.value,
        "severity": sc.severity.value,
        "confidence": sc.confidence,
        "candidate_senses": [
            {
                "surface": c.surface,
                "scope": c.scope,
                "definition": c.definition,
                "XXconfidenceXX": c.confidence,
            }
            for c in sc.candidate_senses
        ],
        "context": sc.context,
    }


def x_semantic_conflict_to_dict__mutmut_19(sc: SemanticConflict) -> dict[str, Any]:
    """Serialize SemanticConflict to dict."""
    return {
        "term": term_surface_to_dict(sc.term),
        "conflict_type": sc.conflict_type.value,
        "severity": sc.severity.value,
        "confidence": sc.confidence,
        "candidate_senses": [
            {
                "surface": c.surface,
                "scope": c.scope,
                "definition": c.definition,
                "CONFIDENCE": c.confidence,
            }
            for c in sc.candidate_senses
        ],
        "context": sc.context,
    }


def x_semantic_conflict_to_dict__mutmut_20(sc: SemanticConflict) -> dict[str, Any]:
    """Serialize SemanticConflict to dict."""
    return {
        "term": term_surface_to_dict(sc.term),
        "conflict_type": sc.conflict_type.value,
        "severity": sc.severity.value,
        "confidence": sc.confidence,
        "candidate_senses": [
            {
                "surface": c.surface,
                "scope": c.scope,
                "definition": c.definition,
                "confidence": c.confidence,
            }
            for c in sc.candidate_senses
        ],
        "XXcontextXX": sc.context,
    }


def x_semantic_conflict_to_dict__mutmut_21(sc: SemanticConflict) -> dict[str, Any]:
    """Serialize SemanticConflict to dict."""
    return {
        "term": term_surface_to_dict(sc.term),
        "conflict_type": sc.conflict_type.value,
        "severity": sc.severity.value,
        "confidence": sc.confidence,
        "candidate_senses": [
            {
                "surface": c.surface,
                "scope": c.scope,
                "definition": c.definition,
                "confidence": c.confidence,
            }
            for c in sc.candidate_senses
        ],
        "CONTEXT": sc.context,
    }

x_semantic_conflict_to_dict__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_semantic_conflict_to_dict__mutmut_1': x_semantic_conflict_to_dict__mutmut_1, 
    'x_semantic_conflict_to_dict__mutmut_2': x_semantic_conflict_to_dict__mutmut_2, 
    'x_semantic_conflict_to_dict__mutmut_3': x_semantic_conflict_to_dict__mutmut_3, 
    'x_semantic_conflict_to_dict__mutmut_4': x_semantic_conflict_to_dict__mutmut_4, 
    'x_semantic_conflict_to_dict__mutmut_5': x_semantic_conflict_to_dict__mutmut_5, 
    'x_semantic_conflict_to_dict__mutmut_6': x_semantic_conflict_to_dict__mutmut_6, 
    'x_semantic_conflict_to_dict__mutmut_7': x_semantic_conflict_to_dict__mutmut_7, 
    'x_semantic_conflict_to_dict__mutmut_8': x_semantic_conflict_to_dict__mutmut_8, 
    'x_semantic_conflict_to_dict__mutmut_9': x_semantic_conflict_to_dict__mutmut_9, 
    'x_semantic_conflict_to_dict__mutmut_10': x_semantic_conflict_to_dict__mutmut_10, 
    'x_semantic_conflict_to_dict__mutmut_11': x_semantic_conflict_to_dict__mutmut_11, 
    'x_semantic_conflict_to_dict__mutmut_12': x_semantic_conflict_to_dict__mutmut_12, 
    'x_semantic_conflict_to_dict__mutmut_13': x_semantic_conflict_to_dict__mutmut_13, 
    'x_semantic_conflict_to_dict__mutmut_14': x_semantic_conflict_to_dict__mutmut_14, 
    'x_semantic_conflict_to_dict__mutmut_15': x_semantic_conflict_to_dict__mutmut_15, 
    'x_semantic_conflict_to_dict__mutmut_16': x_semantic_conflict_to_dict__mutmut_16, 
    'x_semantic_conflict_to_dict__mutmut_17': x_semantic_conflict_to_dict__mutmut_17, 
    'x_semantic_conflict_to_dict__mutmut_18': x_semantic_conflict_to_dict__mutmut_18, 
    'x_semantic_conflict_to_dict__mutmut_19': x_semantic_conflict_to_dict__mutmut_19, 
    'x_semantic_conflict_to_dict__mutmut_20': x_semantic_conflict_to_dict__mutmut_20, 
    'x_semantic_conflict_to_dict__mutmut_21': x_semantic_conflict_to_dict__mutmut_21
}
x_semantic_conflict_to_dict__mutmut_orig.__name__ = 'x_semantic_conflict_to_dict'
